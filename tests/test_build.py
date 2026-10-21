import base64
import hashlib
from pathlib import Path
import runpy
import tempfile
import unittest
from build.prepare import fingerprint
from build.resources import docker_build_command


class BuildInputTests(unittest.TestCase):
    def test_builds_share_exclusive_name_and_resource_limits(self):
        command = docker_build_command()
        for flag, expected in [('--name', 'lulu-android-build'), ('--cpus', '2'),
                               ('--memory', '4g'), ('--memory-swap', '4g'),
                               ('--pids-limit', '1024'), ('--restart', 'no')]:
            self.assertEqual(command[command.index(flag) + 1], expected)
        self.assertIn('--rm', command)

    def test_owner_fingerprint_matches_android_format(self):
        with tempfile.TemporaryDirectory() as temp:
            key = Path(temp) / 'adbkey.pub'
            data = bytes(range(256)) * 2 + bytes(12)
            key.write_text(base64.b64encode(data).decode() + ' ignored-owner-comment\n')
            expected = hashlib.md5(data).hexdigest().upper()
            self.assertEqual(fingerprint(key), ':'.join(expected[i:i + 2] for i in range(0, 32, 2)))
            for invalid in ['', 'not a key', 'abc\nabc']:
                key.write_text(invalid)
                with self.assertRaises(ValueError):
                    fingerprint(key)

    def test_source_manifest_is_pinned(self):
        root = Path(__file__).resolve().parent.parent
        check = runpy.run_path(str(root / 'tools/check-manifest.py'))['check']
        self.assertEqual(check(root / 'build/manifest.xml')['projects'], 447)
