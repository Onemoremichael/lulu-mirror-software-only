#!/usr/bin/env python3
"""Build Android in an isolated working image/tree; never flashes a device."""
import argparse
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build.prepare import fingerprint
from recovery.artifacts import image_info, sha256, write_json

ROOT = Path(__file__).resolve().parent.parent
CONTAINER = 'alleen/apq8016_bm@sha256:b1d5749735cd5e8c3a8915cbc2d06f4d74da62be1082534528da1e6b127fac6c'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument('--tree', type=Path, help='Disposable Linux case-sensitive Android source checkout')
    source.add_argument('--legacy-image', type=Path, help='Existing build filesystem; cloned before modification')
    p.add_argument('--work-image', type=Path, help='New path for a clone of --legacy-image')
    p.add_argument('--public-key', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--jobs', type=int, default=4)
    args = p.parse_args()
    key = args.public_key.resolve(strict=True)
    if key.suffix != '.pub':
        p.error('Use only the ADB .pub public key.')
    fingerprint(key)
    if not 1 <= args.jobs <= 32:
        p.error('Choose 1–32 build jobs.')
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    command = ['docker', 'run', '--rm', '--platform', 'linux/amd64',
               '-e', f'BUILD_JOBS={args.jobs}', '-v', f'{ROOT / "build"}:/inputs:ro',
               '-v', f'{key}:/owner.pub:ro', '-v', f'{output}:/artifacts']
    if args.legacy_image:
        if not args.work_image:
            p.error('--legacy-image requires a new --work-image path.')
        original = args.legacy_image.resolve(strict=True)
        working = args.work_image.resolve()
        if working.exists() or original == working:
            p.error('Working image must be a new file; the original build stays unchanged.')
        working.parent.mkdir(parents=True, exist_ok=True)
        if platform.system() == 'Darwin':
            # APFS clone: do not silently fall back to a 100 GiB physical copy.
            subprocess.run(['cp', '-c', '-n', str(original), str(working)], check=True)
        else:
            subprocess.run(['cp', '--reflink=always', '--sparse=always', str(original), str(working)], check=True)
        command += ['--privileged', '-v', f'{working}:/source.img']
        source_kind = 'cloned legacy workspace; not a clean-source reproduction'
    else:
        tree = args.tree.resolve(strict=True)
        command += ['--privileged', '-v', f'{tree}:/source']
        source_kind = 'owner-supplied source checkout; verify against build/manifest.xml'
    command += [CONTAINER, 'bash', '/inputs/container-build.sh']
    print('Building Android; follow the log in ' + str(output / 'build.log'), flush=True)
    with (output / 'build.log').open('x') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError('Build failed; original input is preserved. Inspect ' + str(output / 'build.log'))
    image = output / 'system.img'
    report = {'schema': 1, 'profile': 'mir63a0-revp21', 'container': CONTAINER,
              'source_kind': source_kind, 'image': image_info(image), 'sha256': sha256(image),
              'owner_public_key_sha256': sha256(key), 'hardware_verified': False,
              'camera': 'Generic vendor stack only; camera recovery is not included in this baseline.'}
    write_json(output / 'build-report.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
