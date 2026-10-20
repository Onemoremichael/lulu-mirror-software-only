#!/usr/bin/env python3
"""Build minimal camera compatibility artifacts; never accesses the Mirror."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from recovery.artifacts import sha256, write_json
from recovery.device import RecoveryError
from build.resources import docker_build_command
from build.camera_artifacts import SDK_REVISION, SOURCE_HASHES, FILES, validate

ROOT = Path(__file__).resolve().parent.parent
CONTAINER = 'alleen/apq8016_bm@sha256:b1d5749735cd5e8c3a8915cbc2d06f4d74da62be1082534528da1e6b127fac6c'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    workspace = p.add_mutually_exclusive_group(required=True)
    workspace.add_argument('--source-image', type=Path, help='Existing ext4 Android workspace, mounted read-only')
    workspace.add_argument('--source-tree', type=Path, help='Case-sensitive Linux Android checkout, mounted read-only')
    p.add_argument('--camera-source', type=Path, required=True, help='Quectel_sc20_linux_sdk checkout at the pinned revision')
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--fresh-headers', action='store_true', help='Verify the clean-checkout kernel-header export path')
    args = p.parse_args()
    patchelf = shutil.which('patchelf')
    if not patchelf:
        raise RecoveryError('Install patchelf (macOS: brew install patchelf).')
    source = args.camera_source.resolve(strict=True)
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != SDK_REVISION:
        raise RecoveryError('Camera source revision does not match the tested SDK.')
    clean = subprocess.run(['git', '-C', str(source), 'diff', '--quiet', 'HEAD', '--',
                            'camera/services/mm-camera-legacy/mm-camera2/media-controller/modules/sensors'])
    if clean.returncode:
        raise RecoveryError('Camera sensor sources have local changes; use the pinned clean checkout.')
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    command = docker_build_command() + ['--privileged',
               '-e', 'CAMERA_FRESH_HEADERS=' + ('1' if args.fresh_headers else '0'),
               '-v', f'{source}:/sdk:ro',
               '-v', f'{ROOT / "camera"}:/patches:ro',
               '-v', f'{ROOT / "build/camera-native.sh"}:/build-camera.sh:ro',
               '-v', f'{output}:/artifacts']
    if args.source_image:
        command += ['-v', f'{args.source_image.resolve(strict=True)}:/source.img:ro']
    else:
        command += ['-v', f'{args.source_tree.resolve(strict=True)}:/source:ro']
    command += [CONTAINER, 'bash', '/build-camera.sh']
    with (output / 'camera-build.log').open('x') as log:
        subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
    for name, expected in SOURCE_HASHES.items():
        if sha256(output / name) != expected:
            raise RecoveryError('Unknown vendor input; refusing camera binary modification: ' + name)
    daemon = output / 'mm-qcamera-daemon'
    subprocess.run([patchelf, '--add-needed', 'libmmcamera_mirror_haf.so', str(daemon)], check=True)
    needed = subprocess.check_output([patchelf, '--print-needed', str(daemon)], text=True).splitlines()
    if needed.count('libmmcamera_mirror_haf.so') != 1:
        raise RecoveryError('Daemon dependency verification failed.')
    cpp = output / 'libmmcamera2_cpp_module.so'
    data = bytearray(cpp.read_bytes())
    if data[0x80b8:0x80ba] != bytes.fromhex('90e0'):
        raise RecoveryError('CPP failure branch bytes differ from the tested input.')
    data[0x80b8:0x80ba] = bytes.fromhex('8fe0')
    cpp.write_bytes(data)
    # Exact input hash plus one verified Thumb branch change; no other binary bytes change.
    if cpp.read_bytes()[0x80b8:0x80ba] != bytes.fromhex('8fe0'):
        raise RecoveryError('CPP branch readback failed.')
    report = {'schema': 1, 'profile': 'mir63a0-revp21', 'sdk_revision': revision,
              'vendor_input_hashes': SOURCE_HASHES, 'exposure_override': False,
              'diagnostic_kernel_module': False, 'hardware_verified': False,
              'files': {name: sha256(output / name) for name in FILES}}
    write_json(output / 'camera-report.json', report)
    validate(output)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (RecoveryError, OSError, ValueError, subprocess.CalledProcessError) as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
