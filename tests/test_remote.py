import unittest
from unittest.mock import patch
from recovery.device import RecoveryError
from recovery.remote import action, validate_host, make_server


class RemoteTests(unittest.TestCase):
    def test_bind_contract_accepts_only_loopback_and_explicit_private_lan(self):
        for host in ['127.0.0.1', '10.0.0.3', '172.16.0.2', '172.31.255.254', '192.168.0.29']:
            validate_host(host)
        for host in ['0.0.0.0', '8.8.8.8', '172.32.0.1', '169.254.0.1',
                     '192.0.0.1', '224.0.0.1', '::1', 'localhost']:
            with self.subTest(host=host), self.assertRaises(RecoveryError):
                validate_host(host)

    def test_invalid_bind_does_not_contact_android(self):
        with patch('recovery.remote.inspect') as inspect:
            with self.assertRaises(RecoveryError):
                make_server('unit', 'mir63a0-revp21', host='0.0.0.0')
            inspect.assert_not_called()

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
