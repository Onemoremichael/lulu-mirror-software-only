from pathlib import Path
import subprocess
import tempfile
import unittest


class RecoveryBoundaryTests(unittest.TestCase):
    def run_boundary(self, body, root):
        script = Path(__file__).resolve().parent.parent / 'build/recovery-boundary.sh'
        return subprocess.run(['bash', '-c', 'source "$1"; ' + body, 'test', str(script), str(root)],
                              capture_output=True, text=True)

    def test_generated_updaters_removed_but_other_files_untouched(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'bin').mkdir()
            (root / 'etc').mkdir()
            for name in ['bin/install-recovery.sh', 'etc/install-recovery.sh', 'recovery-from-boot.p']:
                (root / name).write_text('fixture')
            (root / 'bin/vold').write_text('keep')
            self.assertNotEqual(self.run_boundary('assert_no_recovery_update "$2"', root).returncode, 0)
            result = self.run_boundary('remove_recovery_update "$2" && assert_no_recovery_update "$2"', root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((root / 'bin/vold').read_text(), 'keep')

    def test_dangling_link_and_missing_root_do_not_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'bin').mkdir()
            (root / 'bin/install-recovery.sh').symlink_to(root / 'missing')
            self.assertNotEqual(self.run_boundary('assert_no_recovery_update "$2"', root).returncode, 0)
            self.assertNotEqual(self.run_boundary('assert_no_recovery_update "$2"', root / 'missing').returncode, 0)
