"""Host orchestration tests: Docker and image parsing are explicitly mocked."""
import base64
import contextlib
import io
import json
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from build.camera_artifacts import FILES, SDK_REVISION, SOURCE_HASHES
from recovery.artifacts import sha256


class SystemBuildTests(unittest.TestCase):
    def test_camera_inputs_are_frozen_mounted_and_reported(self):
        entry = runpy.run_path(str(Path(__file__).resolve().parent.parent / 'tools/build-system.py'))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            for directory in ['build', 'camera', 'native', 'tree']:
                (root / directory).mkdir()
            (root / 'build/container-build.sh').write_text('fixture recipe')
            (root / 'camera/fix.patch').write_text('fixture patch')
            key = root / 'owner.pub'
            key.write_text(base64.b64encode(bytes(524)).decode() + ' test-owner')
            for name in FILES:
                (root / 'native' / name).write_bytes(name.encode())
            camera = {'schema': 1, 'profile': 'mir63a0-revp21', 'sdk_revision': SDK_REVISION,
                      'vendor_input_hashes': SOURCE_HASHES, 'exposure_override': False,
                      'diagnostic_kernel_module': False, 'hardware_verified': False,
                      'files': {name: sha256(root / 'native' / name) for name in FILES}}
            (root / 'native/camera-report.json').write_text(json.dumps(camera))
            output = root / 'result'
            calls = []

            def docker_run(command, **kwargs):
                calls.append(command)
                # Simulate output only; this is not a native/image acceptance test.
                (output / 'system.img').write_bytes(b'mocked image')
                return subprocess.CompletedProcess(command, 0)

            arguments = ['build-system.py', '--tree', str(root / 'tree'),
                         '--public-key', str(key), '--output-dir', str(output),
                         '--camera-artifacts', str(root / 'native')]
            with patch.dict(entry['main'].__globals__, {
                'ROOT': root, 'image_info': lambda image: {'mocked': True}
            }), patch('sys.argv', arguments), patch('subprocess.run', side_effect=docker_run), \
                    contextlib.redirect_stdout(io.StringIO()):
                entry['main']()
            self.assertEqual(len(calls), 1)
            command = calls[0]
            for binding in [f'{output}/inputs/build:/inputs:ro',
                            f'{output}/inputs/owner.pub:/owner.pub:ro',
                            f'{output}/inputs/camera-artifacts:/camera-artifacts:ro',
                            f'{output}/inputs/camera-patches:/camera-patches:ro']:
                self.assertIn(binding, command)
            self.assertIn('CAMERA_ENABLED=1', command)
            self.assertIn('BUILD_JOBS=2', command)
            self.assertNotIn(str(key) + ':/owner.pub:ro', command)
            report = json.loads((output / 'build-report.json').read_text())
            self.assertEqual(report['camera'], camera)
            self.assertFalse(report['hardware_verified'])
            self.assertIn('camera-artifacts/mm-qcamera-daemon', report['input_hashes'])
            self.assertEqual(report['input_hashes'],
                             json.loads((output / 'input-hashes.json').read_text()))
