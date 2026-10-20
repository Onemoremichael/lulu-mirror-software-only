import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
from recovery.artifacts import create_bundle, image_info, validate_bundle, write_json
from recovery.device import RecoveryError
from recovery.flash import plan, execute


def sparse(path, kind=0xCAC1, truncated=False):
    payload = bytes(4096) if kind == 0xCAC1 else bytes(4) if kind == 0xCAC2 else b''
    data = struct.pack('<IHHHHIIII', 0xED26FF3A, 1, 0, 28, 12, 4096, 2, 2, 0)
    data += struct.pack('<HHII', kind, 0, 1, 12 + len(payload)) + payload
    data += struct.pack('<HHII', 0xCAC1, 0, 1, 4108) + bytes(4096)
    path.write_bytes(data[:-1] if truncated else data)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.system = self.root / 'system.img'
        sparse(self.system)
        create_bundle(self.root / 'bundle', 'mir63a0-revp21', self.system)
        self.bundle = self.root / 'bundle/bundle.json'
        self.evidence = {'transport': 'fastboot', 'compatible': True,
                         'variables': {'max-download-size': '0x10000000'},
                         'partition_bytes': {'system': 100000, 'userdata': 100000}}

    def test_rejects_truncated_sparse(self):
        sparse(self.system, truncated=True)
        with self.assertRaises(RecoveryError):
            image_info(self.system)

    def test_checksum_changes_stop_recovery(self):
        data = bytearray(self.system.read_bytes())
        data[-1] = 1
        self.system.write_bytes(data)
        with self.assertRaisesRegex(RecoveryError, 'checksum'):
            validate_bundle(self.bundle, 'mir63a0-revp21')

    def test_partition_injection_rejected(self):
        data = json.loads(self.bundle.read_text())
        data['images']['boot'] = data['images']['system']
        self.bundle.write_text(json.dumps(data))
        with self.assertRaises(RecoveryError):
            validate_bundle(self.bundle, 'mir63a0-revp21')

    def test_unknown_or_small_partition_refuses_plan(self):
        for value in [None, 4096]:
            self.evidence['partition_bytes']['system'] = value
            with patch('recovery.flash.inspect', return_value=self.evidence):
                with self.assertRaises(RecoveryError):
                    plan('unit', 'mir63a0-revp21', self.bundle)

    def test_plan_never_writes_and_stale_device_stops_flash(self):
        with patch('recovery.flash.inspect', return_value=self.evidence), patch('recovery.flash.run') as runner:
            value = plan('unit', 'mir63a0-revp21', self.bundle)
            self.assertEqual([s['partition'] for s in value['steps']], ['system'])
            runner.assert_not_called()
            path = self.root / 'plan.json'
            write_json(path, value)
            self.evidence['partition_bytes']['system'] += 4096
            with self.assertRaisesRegex(RecoveryError, 'changed'):
                execute(path, 'RECOVER unit', self.root / 'journal.json')
            runner.assert_not_called()

    def test_bad_confirmation_stops_before_device_access(self):
        path = self.root / 'plan.json'
        path.write_text(json.dumps({'serial': 'unit'}))
        with patch('recovery.flash.plan') as planner:
            with self.assertRaises(RecoveryError):
                execute(path, 'yes', self.root / 'journal.json')
            planner.assert_not_called()

    def test_userdata_fill_chunks_refused(self):
        userdata = self.root / 'userdata.img'
        sparse(userdata, kind=0xCAC2)
        with self.assertRaisesRegex(RecoveryError, 'FILL'):
            create_bundle(self.root / 'filled', 'mir63a0-revp21', self.system, userdata)

    def test_write_failure_stops_before_next_partition(self):
        userdata = self.root / 'userdata.img'
        sparse(userdata)
        create_bundle(self.root / 'both', 'mir63a0-revp21', self.system, userdata)
        with patch('recovery.flash.inspect', return_value=self.evidence):
            value = plan('unit', 'mir63a0-revp21', self.root / 'both/bundle.json')
            path = self.root / 'plan.json'
            write_json(path, value)
            from subprocess import CompletedProcess
            with patch('recovery.flash.target'), patch('recovery.flash.executable', return_value='fastboot'), patch(
                    'recovery.flash.run', return_value=CompletedProcess([], 1, '', 'FAILED')) as runner:
                with self.assertRaisesRegex(RecoveryError, 'Write failed'):
                    execute(path, 'RECOVER unit', self.root / 'journal.json')
                self.assertEqual(runner.call_count, 1)
                events = json.loads((self.root / 'journal.json').read_text())['events']
                self.assertEqual(events[0]['partition'], 'system')
