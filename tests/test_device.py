import unittest
from unittest.mock import patch
from recovery.device import RecoveryError, getvar, integer, target, validate_serial
from subprocess import CompletedProcess


class DeviceTests(unittest.TestCase):
    def test_no_implicit_or_unauthorized_target(self):
        with patch('recovery.device.devices', return_value=[
                {'serial': 'other', 'transport': 'adb', 'state': 'device'},
                {'serial': 'mine', 'transport': 'adb', 'state': 'unauthorized'}]):
            for serial in ['missing', 'mine']:
                with self.assertRaises(RecoveryError):
                    target(serial)

    def test_serial_rejects_command_injection(self):
        for value in ['-s', 'x;reboot', 'a b', '', '$(whoami)']:
            with self.assertRaises(RecoveryError):
                validate_serial(value)

    def test_stderr_fastboot_values(self):
        with patch('recovery.device.executable', return_value='fastboot'), patch(
                'recovery.device.run', return_value=CompletedProcess([], 0, '',
                '(bootloader) partition-size:userdata: 0x14cd00000\nFinished. Total time: 0.001s')):
            self.assertEqual(getvar('unit', 'partition-size:userdata'), '0x14cd00000')

    def test_unsupported_getvar_is_unknown(self):
        with patch('recovery.device.executable', return_value='fastboot'), patch(
                'recovery.device.run', return_value=CompletedProcess([], 1, '', 'FAILED unknown variable')):
            self.assertIsNone(getvar('unit', 'partition-size:system'))
        self.assertIsNone(integer(None))
        self.assertIsNone(integer('unknown'))
        self.assertEqual(integer('0x10000000'), 268435456)
