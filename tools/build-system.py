#!/usr/bin/env python3
"""Build Android in an isolated working image/tree; never flashes a device."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build.prepare import fingerprint
from build.resources import docker_build_command
from build.inputs import snapshot
from recovery.artifacts import image_info, sha256, write_json

ROOT = Path(__file__).resolve().parent.parent
CONTAINER = 'alleen/apq8016_bm@sha256:b1d5749735cd5e8c3a8915cbc2d06f4d74da62be1082534528da1e6b127fac6c'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument('--tree', type=Path, help='Disposable Linux case-sensitive Android source checkout')
    source.add_argument('--legacy-image', type=Path, help='Existing build filesystem; cloned before modification')
    source.add_argument('--resume-image', type=Path, help='Previously cloned working image; continue in that disposable copy')
    p.add_argument('--work-image', type=Path, help='New path for a clone of --legacy-image')
    p.add_argument('--public-key', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--jobs', type=int, default=2)
    args = p.parse_args()
    key = args.public_key.resolve(strict=True)
    if key.suffix != '.pub':
        p.error('Use only the ADB .pub public key.')
    fingerprint(key)
    owner_key_hash = hashlib.sha256(base64.b64decode(key.read_text().split()[0])).hexdigest()
    if not 1 <= args.jobs <= 32:
        p.error('Choose 1–32 build jobs.')
    output = args.output_dir.resolve()
    if output.exists():
        p.error('Choose a new output directory so previous build logs/artifacts are preserved.')
    command = docker_build_command() + [
               '-e', f'BUILD_JOBS={args.jobs}', '-v', f'{output}:/artifacts']
    if args.legacy_image or args.resume_image:
        original = args.legacy_image.resolve(strict=True) if args.legacy_image else None
        if args.resume_image:
            working = args.resume_image.resolve(strict=True)
        else:
            if not args.work_image:
                p.error('--legacy-image requires a new --work-image path.')
            working = args.work_image.resolve()
            if working.exists() or original == working:
                p.error('Working image must be a new file; the original build stays unchanged.')
        # Never mount a workspace that another live Docker job is using. Recheck
        # the actual container mounts rather than treating a stale lock as proof.
        active = subprocess.check_output(['docker', 'ps', '-q'], text=True, timeout=20).split()
        if active:
            containers = json.loads(subprocess.check_output(['docker', 'inspect', *active], text=True, timeout=20))
            inputs = {str(path) for path in [working, original] if path is not None}
            for container in containers:
                for mount in container.get('Mounts', []):
                    value = mount.get('Source', '').removeprefix('/host_mnt')
                    if value in inputs:
                        p.error('A live Docker job is using this image; wait for that job to finish.')
        if original:
            working.parent.mkdir(parents=True, exist_ok=True)
            if platform.system() == 'Darwin':
                # APFS clone: do not silently fall back to a 100 GiB physical copy.
                subprocess.run(['cp', '-c', '-n', str(original), str(working)], check=True)
            else:
                subprocess.run(['cp', '--reflink=always', '--sparse=always', str(original), str(working)], check=True)
        command += ['--privileged', '-v', f'{working}:/source.img']
        source_kind = ('resumed disposable legacy workspace' if args.resume_image else
                       'cloned legacy workspace; not a clean-source reproduction')
    else:
        tree = args.tree.resolve(strict=True)
        command += ['--privileged', '-v', f'{tree}:/source']
        source_kind = 'owner-supplied source checkout; verify against build/manifest.xml'
    output.mkdir(parents=True, exist_ok=False)
    inputs, unused_camera = snapshot(ROOT, output)
    frozen_key = inputs / 'owner.pub'
    shutil.copyfile(key, frozen_key)
    if hashlib.sha256(base64.b64decode(frozen_key.read_text().split()[0])).hexdigest() != owner_key_hash:
        raise ValueError('Owner public key changed while preparing build inputs.')
    input_hashes = {str(path.relative_to(inputs)): sha256(path)
                    for path in sorted(inputs.rglob('*')) if path.is_file()}
    write_json(output / 'input-hashes.json', input_hashes)
    command += ['-v', f'{inputs / "build"}:/inputs:ro',
                '-v', f'{frozen_key}:/owner.pub:ro',
                CONTAINER, 'bash', '/inputs/container-build.sh']
    print('Building Android; follow the log in ' + str(output / 'build.log'), flush=True)
    with (output / 'build.log').open('x') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError('Build failed; original input is preserved. Inspect ' + str(output / 'build.log'))
    image = output / 'system.img'
    report = {'schema': 1, 'profile': 'mir63a0-revp21', 'container': CONTAINER,
              'source_kind': source_kind, 'image': image_info(image), 'sha256': sha256(image),
              'owner_public_key_sha256': owner_key_hash, 'hardware_verified': False,
              'input_hashes': input_hashes,
              'camera': 'Generic vendor stack only; camera recovery is not included in this baseline.'}
    write_json(output / 'build-report.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
