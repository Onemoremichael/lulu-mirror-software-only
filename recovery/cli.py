import argparse
import json
from pathlib import Path
import platform
import shutil
import sys
from .device import RecoveryError, devices, inspect


def main(argv=None):
    parser = argparse.ArgumentParser(description='MIRROR Android recovery and verification')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor', help='Check host prerequisites without changing anything')
    sub.add_parser('devices', help='List ADB and fastboot devices')
    p = sub.add_parser('inspect', help='Read device identity; --board attests the physical label')
    p.add_argument('--serial', required=True)
    p.add_argument('--board', required=True, choices=['mir63a0-revp21'])
    p.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == 'doctor':
            result = {'host': platform.system(), 'python': platform.python_version(),
                      'tools': {t: shutil.which(t) for t in ['adb', 'fastboot', 'git', 'docker']}}
            result['ready_for_inspection'] = bool(result['tools']['adb'] and result['tools']['fastboot'])
        elif args.command == 'devices':
            result = devices()
        else:
            result = inspect(args.serial, args.board)
        output = json.dumps(result, indent=2) + '\n'
        if getattr(args, 'output', None):
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open('x') as f:
                f.write(output)
        print(output, end='')
        return 0
    except (RecoveryError, OSError, ValueError) as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1
