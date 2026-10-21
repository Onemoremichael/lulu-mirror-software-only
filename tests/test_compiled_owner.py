import base64
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from build.prepare import fingerprint


class CompiledOwnerTests(unittest.TestCase):
    def test_compiled_fingerprint_and_branch_are_both_required(self):
        root = Path(__file__).resolve().parent.parent
        with patch.object(sys, 'path', [str(root / 'build'), *sys.path]):
            check = runpy.run_path(str(root / 'build/check-owner.py'))['check']
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / 'framework').mkdir()
            key = directory / 'key.pub'
            key.write_text(base64.b64encode(bytes(524)).decode() + ' fixture')
            owner = fingerprint(key).encode('ascii')
            marker = b"Authorizing the Mirror owner's ADB key"
            for data, valid in [(owner + marker, True), (owner, False), (marker, False)]:
                with zipfile.ZipFile(directory / 'framework/services.jar', 'w') as jar:
                    jar.writestr('classes.dex', data)
                if valid:
                    self.assertFalse(check(directory, key)['hardware_authorization_tested'])
                else:
                    with self.assertRaises(ValueError):
                        check(directory, key)
