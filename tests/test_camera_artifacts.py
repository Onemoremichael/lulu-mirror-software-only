import copy
import json
from pathlib import Path
import tempfile
import unittest

from build.camera_artifacts import FILES, SDK_REVISION, SOURCE_HASHES, validate
from recovery.artifacts import sha256


class CameraArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        for name in FILES:
            (self.directory / name).write_bytes(('fixture ' + name).encode())
        self.report = {'schema': 1, 'profile': 'mir63a0-revp21',
                       'sdk_revision': SDK_REVISION, 'vendor_input_hashes': SOURCE_HASHES,
                       'exposure_override': False, 'diagnostic_kernel_module': False,
                       'hardware_verified': False,
                       'files': {name: sha256(self.directory / name) for name in FILES}}
        self.save(self.report)

    def save(self, report):
        (self.directory / 'camera-report.json').write_text(json.dumps(report))

    def test_supported_bundle_checks_every_file(self):
        self.assertEqual(validate(self.directory), self.report)
        for name in FILES:
            path = self.directory / name
            original = path.read_bytes()
            path.write_bytes(original + b'changed')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                validate(self.directory)
            path.write_bytes(original)

    def test_rejects_unknown_or_experimental_builds(self):
        for field, value in [('profile', 'other'), ('sdk_revision', 'other'),
                             ('exposure_override', True), ('diagnostic_kernel_module', True),
                             ('vendor_input_hashes', {}), ('files', {})]:
            report = copy.deepcopy(self.report)
            report[field] = value
            self.save(report)
            with self.assertRaises(ValueError):
                validate(self.directory)

    def test_symlink_is_not_an_artifact(self):
        path = self.directory / FILES[0]
        target = self.directory / 'elsewhere'
        path.rename(target)
        path.symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'regular file'):
            validate(self.directory)
