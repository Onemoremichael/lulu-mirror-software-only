"""Structural registry checks, not proof of owner evidence or runtime acceptance.

Research records must not silently become executable recovery permissions.
"""
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from recovery.device import RecoveryError, profile

ROOT = Path(__file__).resolve().parent.parent
LEVELS = {'reported', 'identified', 'investigating', 'research-unit-recovered', 'repeatable-recovery'}


class HardwareRegistryTests(unittest.TestCase):
    def test_research_identity_does_not_grant_runtime_permissions(self):
        # Neither adding a record nor sharing a chipset may bypass the CLI's
        # separately reviewed profile whitelist. Reject before filesystem/device access.
        with patch('pathlib.Path.read_text') as read, patch('recovery.device.run') as run:
            for candidate in ['new-board-research', 'msm8916', '../mir63a0-revp21']:
                with self.subTest(candidate=candidate), self.assertRaises(RecoveryError):
                    profile(candidate)
            read.assert_not_called()
            run.assert_not_called()

    def test_registry_has_evidenced_records_and_explicit_profile_boundary(self):
        registry = json.loads((ROOT / 'hardware/registry.json').read_text())
        self.assertEqual(registry['schema'], 1)
        self.assertTrue(registry['boards'])
        seen = set()
        for board in registry['boards']:
            with self.subTest(board=board.get('id')):
                self.assertRegex(board['id'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
                self.assertNotIn(board['id'], seen)
                seen.add(board['id'])
                self.assertTrue(board['board_label'])
                self.assertIn(board['evidence_level'], LEVELS)
                self.assertIsInstance(board['repeatable_recovery'], bool)
                self.assertEqual(board['repeatable_recovery'],
                                 board['evidence_level'] == 'repeatable-recovery')
                self.assertEqual(board['record'], 'boards/' + board['id'] + '.md')
                record = ROOT / 'hardware' / board['record']
                self.assertTrue(record.is_file())
                self.assertIn(board['board_label'], record.read_text())
                profile_id = board['recovery_profile']
                if profile_id is not None:
                    self.assertRegex(profile_id, r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
                    profile = json.loads((ROOT / 'profiles' / (profile_id + '.json')).read_text())
                    self.assertEqual(profile['id'], profile_id)
                    self.assertEqual(profile['board_label'], board['board_label'])

    def test_each_executable_profile_has_a_research_record(self):
        boards = json.loads((ROOT / 'hardware/registry.json').read_text())['boards']
        registered = {board['recovery_profile'] for board in boards if board['recovery_profile']}
        self.assertEqual(registered, {path.stem for path in (ROOT / 'profiles').glob('*.json')})

    def test_contribution_and_hardware_local_links_resolve(self):
        documents = [ROOT / 'CONTRIBUTING.md', ROOT / 'docs/PORTING.md',
                     ROOT / 'docs/COMPATIBILITY.md', ROOT / 'README.md',
                     *(ROOT / 'hardware').rglob('*.md')]
        for document in documents:
            for link in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' in link or link.startswith('#'):
                    continue
                target = link.split('#', 1)[0]
                with self.subTest(document=str(document), target=target):
                    self.assertTrue((document.parent / target).exists())
