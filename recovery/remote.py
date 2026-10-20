"""Small non-touch Android remote, bound to an explicitly chosen host/device."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import ipaddress
import json
from pathlib import Path
import shlex
import subprocess
from urllib.parse import urlsplit
from .device import ROOT, RecoveryError, adb, executable, inspect

KEYS = {'back': 4, 'home': 3, 'recents': 187, 'up': 19, 'down': 20,
        'left': 21, 'right': 22, 'select': 23, 'enter': 66,
        'volume-up': 24, 'volume-down': 25, 'wake': 224, 'sleep': 223}
APPS = {'settings': 'android.settings.SETTINGS',
        'wifi': 'android.settings.WIFI_SETTINGS'}


def action(serial, body):
    name = body.get('action')
    if name == 'key' and body.get('key') in KEYS:
        result = adb(serial, 'shell', 'input', 'keyevent', str(KEYS[body['key']]))
        if body['key'] == 'wake':
            # MENU opens the Afterglow modal; waking must not synthesize MENU.
            adb(serial, 'shell', 'wm', 'dismiss-keyguard')
        return result
    if name == 'app' and body.get('app') in APPS:
        return adb(serial, 'shell', 'am', 'start', '-a', APPS[body['app']])
    if name == 'text':
        text = body.get('text')
        if not isinstance(text, str) or not 1 <= len(text) <= 300 or any(ord(c) < 32 for c in text):
            raise RecoveryError('Enter 1–300 printable characters.')
        return adb(serial, 'shell', 'input', 'text', shlex.quote(text.replace(' ', '%s')))
    if name in ('tap', 'swipe'):
        coords = [body.get(k) for k in (['x', 'y'] if name == 'tap' else ['x', 'y', 'toX', 'toY'])]
        if any(type(n) is not int or not 0 <= n <= 8192 for n in coords):
            raise RecoveryError('Invalid screen coordinates.')
        args = ['shell', 'input', name, *map(str, coords)]
        if name == 'swipe':
            args.append('350')
        return adb(serial, *args)
    raise RecoveryError('Unknown remote control action.')


def make_server(serial, board, host='127.0.0.1', port=8765):
    identity = inspect(serial, board)
    if identity['transport'] != 'adb' or not identity['compatible']:
        raise RecoveryError('Connect the compatible Mirror through authorized ADB first.')
    if not ipaddress.ip_address(host).is_private or ':' in host:
        raise RecoveryError('Choose an explicit private IPv4 address or 127.0.0.1.')
    allowed_hosts = set()
    assets = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'),
              '/style.css': ('style.css', 'text/css')}

    class Handler(BaseHTTPRequestHandler):
        def reply(self, code, data, mime='application/json'):
            payload = data if isinstance(data, bytes) else json.dumps(data).encode()
            self.send_response(code)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; img-src 'self' blob:; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(payload)

        def valid_host(self):
            if self.headers.get('Host') not in allowed_hosts:
                self.reply(403, {'error': 'Use the printed local remote address.'})
                return False
            return True

        def do_GET(self):
            if not self.valid_host():
                return
            path = urlsplit(self.path).path
            try:
                if path in assets:
                    file, mime = assets[path]
                    return self.reply(200, (ROOT / 'remote' / file).read_bytes(), mime)
                if path == '/api/status':
                    return self.reply(200, {'serial': serial, 'board': board,
                                           'android': adb(serial, 'shell', 'getprop', 'sys.boot_completed') == '1'})
                if path == '/api/screen':
                    process = subprocess.run([executable('adb'), '-s', serial, 'exec-out', 'screencap', '-p'],
                                             capture_output=True, timeout=30)
                    data = process.stdout
                    if process.returncode or not data.startswith(b'\x89PNG\r\n\x1a\n'):
                        raise RecoveryError('Could not capture Android screen; check USB and authorization.')
                    return self.reply(200, data, 'image/png')
                self.reply(404, {'error': 'Not found'})
            except (RecoveryError, OSError, subprocess.TimeoutExpired) as e:
                self.reply(503, {'error': str(e)})

        def do_POST(self):
            if not self.valid_host():
                return
            request_origin = self.headers.get('Origin')
            expected_origin = 'http://' + self.headers.get('Host', '')
            if request_origin != expected_origin or self.headers.get('Content-Type') != 'application/json':
                return self.reply(403, {'error': 'Same-origin JSON required.'})
            if self.path != '/api/action':
                return self.reply(404, {'error': 'Not found'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 4096:
                    return self.reply(413, {'error': 'Request size out of range.'})
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise RecoveryError('Expected action object.')
                self.reply(200, {'ok': True, 'detail': action(serial, body)})
            except (RecoveryError, ValueError, OSError) as e:
                self.reply(400, {'error': str(e)})

        def log_message(self, *args):
            pass  # Do not log text input, screen contents or credentials.

    server = ThreadingHTTPServer((host, port), Handler)
    actual_port = server.server_address[1]
    allowed_hosts.add(f'{host}:{actual_port}')
    if host == '127.0.0.1':
        allowed_hosts.add(f'localhost:{actual_port}')
    return server


def serve(serial, board, host='127.0.0.1', port=8765):
    server = make_server(serial, board, host, port)
    origin = f'http://{host}:{server.server_address[1]}'
    print(f'Android remote: {origin}\nDevice: {serial}\nCtrl+C stops the remote.', flush=True)
    if host != '127.0.0.1':
        print('This remote allows control from your trusted LAN without a login. Stop it when finished.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
