from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
from build.source_inventory import audit


class SourceInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / 'project'
        self.project.mkdir()
        self.git('init')
        (self.project / 'file').write_text('fixture')
        self.git('add', 'file')
        self.git('-c', 'commit.gpgsign=false', '-c', 'user.name=Fixture',
                 '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'Fixture')
        self.head = self.git('rev-parse', 'HEAD').strip()
        self.manifest = self.root / 'manifest.xml'

    def git(self, *arguments):
        return subprocess.check_output(['git', *arguments], cwd=self.project,
                                       text=True, stderr=subprocess.PIPE)

    def check(self, path='project', revision=None):
        self.manifest.write_text('<manifest><project path="%s" revision="%s"/></manifest>' %
                                 (path, revision or self.head))
        return audit(self.root, self.manifest)

    def test_pinned_head_is_not_working_tree_attestation(self):
        report = self.check()
        self.assertTrue(report['all_heads_match'])
        self.assertEqual(report['matching_heads'], 1)
        (self.project / 'file').write_text('locally modified')
        report = self.check()
        self.assertTrue(report['all_heads_match'])
        self.assertFalse(report['working_tree_contents_verified'])
        self.assertFalse(report['vendor_inputs_verified'])

    def test_wrong_revision_and_missing_directory_fail_pin_check(self):
        report = self.check(revision='0' * 40)
        self.assertFalse(report['all_heads_match'])
        self.assertEqual(report['head_mismatches'][0]['observed'], self.head)
        report = self.check(path='missing')
        self.assertEqual(report['unavailable'][0]['reason'], 'directory_missing')

    def test_nested_directory_does_not_borrow_parent_git_identity(self):
        (self.project / 'nested').mkdir()
        report = self.check(path='project/nested')
        self.assertFalse(report['all_heads_match'])
        self.assertEqual(report['unavailable'][0]['reason'], 'checkout_root_mismatch')

    def test_invalid_manifest_paths_and_unpinned_revisions_are_rejected(self):
        for path, revision in [('../outside', self.head), ('/outside', self.head), ('project', 'main')]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.check(path, revision)

    def test_unexpanded_manifest_cannot_silently_verify_a_subset(self):
        self.check()
        contents = self.manifest.read_text().replace('</manifest>', '<include name="extra.xml"/></manifest>')
        self.manifest.write_text(contents)
        with self.assertRaises(ValueError):
            audit(self.root, self.manifest)

    def test_required_mismatch_retains_report_and_never_overwrites_it(self):
        self.check(revision='0' * 40)
        script = Path(__file__).resolve().parent.parent / 'build/source_inventory.py'
        output = self.root / 'report.json'
        command = [sys.executable, str(script), '--tree', str(self.root),
                   '--manifest', str(self.manifest), '--output', str(output), '--require-pins']
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        original = output.read_bytes()
        self.assertFalse(json.loads(original)['all_heads_match'])
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_bytes(), original)
