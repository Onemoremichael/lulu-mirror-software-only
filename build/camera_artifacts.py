"""Validate owner-built camera artifacts before adding them to firmware."""
import json
from pathlib import Path
from recovery.artifacts import sha256

FILES = ('libmmcamera_ov5640.so', 'libmmcamera_mirror_haf.so',
         'mm-qcamera-daemon', 'libmmcamera2_cpp_module.so')
SDK_REVISION = 'ed0e50a102c7ee115c6999ba0a26ce50537c616e'
SOURCE_HASHES = {'mm-qcamera-daemon': 'ceb969d8534addcf3bff0d741dc073d6d49eeec702d55a9b94ac441649c31f6f',
                 'libmmcamera2_cpp_module.so': '94ce0a02766a34ed62f7eee08eb78ea573af2002f45cca8fa70ce98103ec6a7e'}


def validate(directory):
    directory = Path(directory).resolve(strict=True)
    report = json.loads((directory / 'camera-report.json').read_text())
    if (report.get('schema') != 1 or report.get('profile') != 'mir63a0-revp21'
            or report.get('sdk_revision') != SDK_REVISION
            or report.get('vendor_input_hashes') != SOURCE_HASHES
            or report.get('exposure_override') is not False
            or report.get('diagnostic_kernel_module') is not False
            or not isinstance(report.get('files'), dict)
            or set(report['files']) != set(FILES)):
        raise ValueError('Camera report is not the supported minimal compatibility build.')
    for name in FILES:
        path = directory / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
            raise ValueError('Camera artifact must be a nonempty regular file: ' + name)
        if sha256(path) != report['files'][name]:
            raise ValueError('Camera artifact hash mismatch: ' + name)
    return report
