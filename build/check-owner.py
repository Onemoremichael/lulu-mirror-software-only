"""Verify compiled owner authorization markers; no device access (Python 2/3)."""
from __future__ import print_function
import argparse
import json
import os
import zipfile
from prepare import fingerprint


def check(system, key):
    owner = fingerprint(key).encode('ascii')
    with zipfile.ZipFile(os.path.join(str(system), 'framework/services.jar')) as jar:
        dex = jar.read('classes.dex')
    if owner not in dex or b"Authorizing the Mirror owner's ADB key" not in dex:
        raise ValueError('Compiled Android services do not contain the expected owner authorization markers.')
    return {'owner_fingerprint_present': True, 'authorization_branch_marker': True,
            'hardware_authorization_tested': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--system', required=True)
    parser.add_argument('--public-key', required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.system, args.public_key), indent=2))
