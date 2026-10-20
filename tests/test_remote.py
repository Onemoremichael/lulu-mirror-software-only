import unittest
from unittest.mock import patch
from recovery.device import RecoveryError
from recovery.remote import action


class RemoteTests(unittest.TestCase):
    def test_wake_does_not_open_menu(self):
        with patch('recovery.remote.adb', return_value='') as adb:
            action('unit', {'action': 'key', 'key': 'wake'})
            self.assertEqual(adb.call_args_list[0].args, ('unit', 'shell', 'input', 'keyevent', '224'))
            self.assertEqual(adb.call_args_list[1].args, ('unit', 'shell', 'wm', 'dismiss-keyguard'))

    def test_no_arbitrary_commands(self):
        for body in [{'action': 'shell', 'command': 'reboot'}, {'action': 'key', 'key': '82'},
                     {'action': 'app', 'app': 'unknown'}, {'action': 'tap', 'x': '1;reboot', 'y': 5}]:
            with patch('recovery.remote.adb') as adb:
                with self.assertRaises(RecoveryError):
                    action('unit', body)
                adb.assert_not_called()

    def test_text_is_shell_quoted_and_serial_scoped(self):
        with patch('recovery.remote.adb', return_value='') as adb:
            action('unit', {'action': 'text', 'text': 'x;reboot $(id)'})
            self.assertEqual(adb.call_args.args, ('unit', 'shell', 'input', 'text', "'x;reboot%s$(id)'"))
