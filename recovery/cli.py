import argparse
import json
from pathlib import Path
import platform
import shutil
import sys
from .device import RecoveryError, devices, inspect
from .artifacts import create_bundle, write_json
from .flash import plan, execute
from .verify import verify


def main(argv=None):
    parser = argparse.ArgumentParser(description='MIRROR Android recovery and verification')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor', help='Check host prerequisites without changing anything')
    sub.add_parser('devices', help='List ADB and fastboot devices')
    p = sub.add_parser('inspect', help='Read device identity; --board attests the physical label')
    p.add_argument('--serial', required=True)
    p.add_argument('--board', required=True, choices=['mir63a0-revp21'])
    p.add_argument('--output', type=Path)
    p = sub.add_parser('bundle', help='Validate and describe locally supplied firmware')
    p.add_argument('--board', required=True, choices=['mir63a0-revp21'])
    p.add_argument('--system', type=Path, required=True)
    p.add_argument('--userdata', type=Path)
    p.add_argument('--directory', type=Path, required=True)
    p.add_argument('--provenance')
    p = sub.add_parser('plan', help='Read fastboot and produce an explicit recovery plan; no writes')
    p.add_argument('--serial', required=True)
    p.add_argument('--board', required=True, choices=['mir63a0-revp21'])
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p = sub.add_parser('flash', help='Execute a revalidated plan; replaces the listed partitions')
    p.add_argument('--plan', type=Path, required=True)
    p.add_argument('--confirm', required=True, help='Exact RECOVER SERIAL text from the plan')
    p.add_argument('--journal', type=Path, required=True)
    p = sub.add_parser('verify', help='Check boot, Android, launcher, storage, Wi-Fi driver and ADB')
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
        elif args.command == 'inspect':
            result = inspect(args.serial, args.board)
        elif args.command == 'bundle':
            result = create_bundle(args.directory, args.board, args.system, args.userdata, args.provenance)
        elif args.command == 'plan':
            result = plan(args.serial, args.board, args.bundle)
        elif args.command == 'flash':
            result = execute(args.plan, args.confirm, args.journal)
        else:
            result = verify(args.serial, args.board)
        output = json.dumps(result, indent=2) + '\n'
        if getattr(args, 'output', None):
            write_json(args.output, result)
        print(output, end='')
        return 1 if args.command == 'verify' and not result['automated_checks_passed'] else 0
    except (RecoveryError, OSError, ValueError, KeyError, TypeError) as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1
