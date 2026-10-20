import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from build.inputs import snapshot
from build.camera_artifacts import FILES, SDK_REVISION, SOURCE_HASHES
from recovery.artifacts import sha256


class InputSnapshotTests(unittest.TestCase):
    def test_recipes_are_frozen_and_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'build/__pycache__').mkdir(parents=True)
            (root / 'build/run.sh').write_text('original')
            (root / 'build/__pycache__/ignored.pyc').write_bytes(b'cache')
            output = root / 'output'
            output.mkdir()
            frozen, report = snapshot(root, output)
            (root / 'build/run.sh').write_text('changed')
            self.assertEqual((frozen / 'build/run.sh').read_text(), 'original')
            self.assertFalse((frozen / 'build/__pycache__').exists())
            self.assertIsNone(report)
            with self.assertRaises(FileExistsError):
                snapshot(root, output)

    def test_camera_snapshot_and_mutation_during_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory in ['build', 'camera', 'artifacts', 'output', 'raced']:
                (root / directory).mkdir()
            (root / 'camera/fix.patch').write_text('fixture')
            for name in FILES:
                (root / 'artifacts' / name).write_bytes(name.encode())
            report = {'schema': 1, 'profile': 'mir63a0-revp21',
                      'sdk_revision': SDK_REVISION, 'vendor_input_hashes': SOURCE_HASHES,
                      'exposure_override': False, 'diagnostic_kernel_module': False,
                      'files': {name: sha256(root / 'artifacts' / name) for name in FILES}}
            (root / 'artifacts/camera-report.json').write_text(json.dumps(report))
            frozen, result = snapshot(root, root / 'output', root / 'artifacts')
            self.assertEqual(result, report)
            self.assertTrue((frozen / 'camera-patches/fix.patch').exists())
            import shutil
            copyfile = shutil.copyfile

            def corrupt_copy(source, destination, *args, **kwargs):
                result = copyfile(source, destination, *args, **kwargs)
                if Path(destination).name == FILES[0]:
                    Path(destination).write_bytes(b'changed during copy')
                return result

            with patch('build.inputs.shutil.copyfile', side_effect=corrupt_copy):
                with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                    snapshot(root, root / 'raced', root / 'artifacts')
