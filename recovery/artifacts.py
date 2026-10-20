"""Validate recovery artifacts before any fastboot write."""
import hashlib
import json
from pathlib import Path
import struct
from .device import RecoveryError, profile

MAGIC = 0xED26FF3A


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def image_info(path):
    """Parse the complete Android sparse container; never trust header size alone."""
    path = Path(path)
    size = path.stat().st_size
    if size < 4096:
        raise RecoveryError(f'Image is empty or too small: {path.name}')
    with path.open('rb') as f:
        header = f.read(28)
        if struct.unpack_from('<I', header)[0] != MAGIC:
            # ext4 superblock magic, not an arbitrary file with an .img suffix.
            f.seek(1024 + 56)
            if f.read(2) != b'\x53\xef':
                raise RecoveryError('Expected Android sparse or raw ext4 image.')
            return {'format': 'ext4', 'bytes': size, 'expanded_bytes': size}
        magic, major, minor, fh, ch, block, total, chunks, checksum = struct.unpack('<IHHHHIIII', header)
        if major != 1 or minor != 0 or fh < 28 or ch < 12 or block != 4096 or not total or not chunks:
            raise RecoveryError('Unsupported or empty Android sparse header.')
        if fh > size or chunks > size // ch:
            raise RecoveryError('Sparse headers exceed file size.')
        f.seek(fh)
        covered = 0
        kinds = set()
        for _ in range(chunks):
            raw = f.read(ch)
            if len(raw) != ch:
                raise RecoveryError('Truncated sparse chunk header.')
            kind, reserved, count, chunk_size = struct.unpack_from('<HHII', raw)
            expected = {0xCAC1: count * block, 0xCAC2: 4, 0xCAC3: 0, 0xCAC4: 4}.get(kind)
            if reserved or expected is None or chunk_size != ch + expected:
                raise RecoveryError('Invalid sparse chunk.')
            if kind == 0xCAC4:
                if count != 0:
                    raise RecoveryError('Invalid CRC chunk block count.')
            else:
                covered += count
            kinds.add(kind)
            if f.tell() + expected > size:
                raise RecoveryError('Truncated sparse payload.')
            f.seek(expected, 1)
        if covered != total or f.tell() != size:
            raise RecoveryError('Sparse coverage or trailing data mismatch.')
        return {'format': 'android-sparse', 'bytes': size,
                'expanded_bytes': total * block, 'chunk_types': sorted(kinds)}


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def create_bundle(directory, board, system, userdata=None, provenance=None):
    """Reference locally owned files; do not upload firmware or copy multi-GB images."""
    config = profile(board)
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    images = {}
    for partition, source in [('system', system), ('userdata', userdata)]:
        if source is None:
            continue
        source = Path(source).resolve(strict=True)
        info = image_info(source)
        if partition == 'userdata' and info['format'] == 'android-sparse' and 0xCAC2 in info['chunk_types']:
            raise RecoveryError('Use the tested RAW/DONT_CARE userdata converter; FILL chunks are unsupported here.')
        images[partition] = {'path': str(source), 'sha256': sha256(source), **info}
    manifest = {'schema': 1, 'profile': config['id'], 'images': images,
                'provenance': provenance or 'Local owner-supplied build; not a published project release.',
                'userdata_policy': 'Fresh unencrypted userdata; sparse free blocks are not securely erased.'}
    write_json(directory / 'bundle.json', manifest)
    return manifest


def validate_bundle(path, board):
    path = Path(path).resolve(strict=True)
    data = json.loads(path.read_text())
    config = profile(board)
    if data.get('schema') != 1 or data.get('profile') != config['id']:
        raise RecoveryError('Bundle schema or hardware profile mismatch.')
    images = data.get('images', {})
    if not isinstance(images, dict) or 'system' not in images or set(images) - set(config['writable_partitions']):
        raise RecoveryError('Bundle must contain system and may contain only userdata in addition.')
    resolved = {}
    for partition, item in images.items():
        image = Path(item['path'])
        image = image if image.is_absolute() else path.parent / image
        image = image.resolve(strict=True)
        info = image_info(image)
        if any(item.get(k) != info[k] for k in ('format', 'bytes', 'expanded_bytes')):
            raise RecoveryError(f'{partition}: image geometry differs from bundle.')
        if sha256(image) != item.get('sha256'):
            raise RecoveryError(f'{partition}: image checksum mismatch.')
        if partition == 'userdata' and 0xCAC2 in info.get('chunk_types', []):
            raise RecoveryError('Userdata FILL chunks are not accepted.')
        resolved[partition] = {**item, **info, 'path': str(image)}
    return {**data, 'images': resolved}
