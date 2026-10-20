import http.client
import json
import threading
import unittest
from unittest.mock import patch
from recovery.remote import make_server


class RemoteHTTPTests(unittest.TestCase):
    def setUp(self):
        with patch('recovery.remote.inspect', return_value={'transport': 'adb', 'compatible': True}):
            self.server = make_server('unit', 'mir63a0-revp21', port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop)
        self.host = '127.0.0.1:' + str(self.server.server_address[1])

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_address[1])
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return response.status, data

    def test_remote_page_and_cross_site_action_boundary(self):
        code, page = self.request('GET', '/')
        self.assertEqual(code, 200)
        self.assertIn(b'Your mirror, within reach.', page)
        with patch('recovery.remote.adb', return_value='') as adb:
            body = json.dumps({'action': 'key', 'key': 'home'})
            headers = {'Origin': 'https://unrelated.example', 'Content-Type': 'application/json'}
            self.assertEqual(self.request('POST', '/api/action', body, headers)[0], 403)
            adb.assert_not_called()
            headers['Origin'] = 'http://' + self.host
            self.assertEqual(self.request('POST', '/api/action', body, headers)[0], 200)
            adb.assert_called_once_with('unit', 'shell', 'input', 'keyevent', '3')

    def test_host_and_request_size_checks(self):
        self.assertEqual(self.request('GET', '/', headers={'Host': 'unrelated.example'})[0], 403)
        headers = {'Origin': 'http://' + self.host, 'Content-Type': 'application/json'}
        self.assertEqual(self.request('POST', '/api/action', 'x' * 4097, headers)[0], 413)
