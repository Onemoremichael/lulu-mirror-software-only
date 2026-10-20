import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent


class RecoveryError(Exception):
    pass


def run(args, timeout=20, check=True):
    try:
        p = subprocess.run([str(x) for x in args], capture_output=True,
                           text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise RecoveryError(f'{args[0]}: {e}') from e
    if check and p.returncode:
        raise RecoveryError(f'{args[0]} failed: {(p.stderr or p.stdout).strip()}')
    return p


def executable(name):
    path = os.environ.get(name.upper() + '_PATH') or shutil.which(name)
    if not path:
        raise RecoveryError(f'Install {name} and add it to PATH (or set {name.upper()}_PATH).')
    return path


def validate_serial(serial):
    if not re.fullmatch(r'[A-Za-z0-9_.:\-]{1,150}', serial):
        raise RecoveryError('Invalid device serial.')
    return serial


def profile(name):
    if name != 'mir63a0-revp21':
        raise RecoveryError('Unsupported board profile; inspect the printed board label.')
    return json.loads((ROOT / 'profiles' / f'{name}.json').read_text())


def devices():
    found = []
    for tool, command in [('adb', ['devices', '-l']), ('fastboot', ['devices'])]:
        try:
            output = run([executable(tool), *command]).stdout
        except RecoveryError as e:
            found.append({'transport': tool, 'error': str(e)})
            continue
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 2 and not line.startswith(('List of', '*')):
                found.append({'transport': tool, 'serial': parts[0], 'state': parts[1]})
    return found


def target(serial, transport=None):
    validate_serial(serial)
    matches = [d for d in devices() if d.get('serial') == serial
               and (transport is None or d['transport'] == transport)]
    if len(matches) != 1:
        raise RecoveryError('Exactly one matching device must be connected; check devices and USB.')
    match = matches[0]
    if match['state'] not in ('device', 'fastboot'):
        raise RecoveryError(f"Device is {match['state']}; authorize ADB on Android or use the recovery guide.")
    return match['transport']


def adb(serial, *args, timeout=20):
    return run([executable('adb'), '-s', validate_serial(serial), *args], timeout).stdout.strip()


def getvar(serial, name):
    p = run([executable('fastboot'), '-s', validate_serial(serial), 'getvar', name], check=False)
    text = p.stdout + '\n' + p.stderr
    if p.returncode or 'FAILED' in text:
        return None
    for line in text.splitlines():
        value = re.sub(r'^\(bootloader\)\s*', '', line).strip()
        if value.startswith(name + ':'):
            return value[len(name) + 1:].strip() or None
    return None


def integer(value):
    if value is None:
        return None
    try:
        return int(value, 16 if value.lower().startswith('0x') else 10)
    except ValueError:
        return None


def inspect(serial, board):
    config = profile(board)
    transport = target(serial)
    result = {'schema': 1, 'serial': serial, 'profile': config['id'],
              'board_label_attested': config['board_label'], 'transport': transport}
    if transport == 'adb':
        keys = ['ro.board.platform', 'ro.product.device', 'ro.build.version.release',
                'ro.build.fingerprint', 'ro.build.type', 'ro.debuggable',
                'ro.adb.secure', 'sys.boot_completed', 'ro.crypto.state']
        result['properties'] = {k: adb(serial, 'shell', 'getprop', k) for k in keys}
        result['kernel'] = adb(serial, 'shell', 'uname', '-r')
        result['compatible'] = (result['properties']['ro.board.platform'] in config['platforms']
                                and result['kernel'] == config['kernel_release'])
    else:
        result['variables'] = {k: getvar(serial, k) for k in
                               ['product', 'secure', 'unlocked', 'max-download-size',
                                'partition-size:system', 'partition-size:userdata']}
        result['compatible'] = result['variables']['product'] in config['fastboot_products']
        result['partition_bytes'] = {p: integer(result['variables']['partition-size:' + p])
                                      for p in config['writable_partitions']}
    result['compatibility_note'] = ('Matching observed values plus owner-attested board label; '
                                    'not proof of image compatibility or a full factory backup.')
    return result
