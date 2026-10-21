"""Read-only manifest/checkout HEAD comparison (Python 2/3, including old Git)."""
from __future__ import print_function
import argparse
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


def git(directory, arguments):
    # cwd works with the pinned container's Git 1.7, which predates git -C.
    process = subprocess.Popen(['git'] + arguments, cwd=directory,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    output, unused_error = process.communicate()
    return output.strip() if process.returncode == 0 else None


def audit(tree, manifest):
    tree = os.path.realpath(str(tree))
    if not os.path.isdir(tree):
        raise ValueError('Source root must be an existing directory.')
    root = ET.parse(str(manifest)).getroot()
    if root.tag != 'manifest' or root.find('include') is not None:
        raise ValueError('Use an expanded manifest without include elements.')
    projects = root.findall('project')
    if not projects:
        raise ValueError('Manifest contains no projects.')
    report = {'schema': 1, 'projects': len(projects), 'matching_heads': 0,
              'head_mismatches': [], 'unavailable': [],
              'working_tree_contents_verified': False, 'vendor_inputs_verified': False}
    seen = set()
    for project in projects:
        relative = project.get('path') or project.get('name', '')
        revision = project.get('revision', '')
        if (os.path.isabs(relative) or any(part in ('', '.', '..') for part in relative.split('/'))
                or relative in seen or not re.match(r'^[0-9a-f]{40}$', revision)):
            raise ValueError('Manifest paths must be unique/relative and revisions pinned: ' + relative)
        seen.add(relative)
        directory = os.path.join(tree, relative)
        reason = None
        if not os.path.isdir(directory):
            reason = 'directory_missing'
        else:
            top = git(directory, ['rev-parse', '--show-toplevel'])
            if top is None:
                reason = 'git_metadata_unavailable'
            elif os.path.realpath(top) != os.path.realpath(directory):
                reason = 'checkout_root_mismatch'
        if reason:
            report['unavailable'].append({'path': relative, 'reason': reason})
            continue
        observed = git(directory, ['rev-parse', '--verify', 'HEAD'])
        if observed == revision:
            report['matching_heads'] += 1
        else:
            report['head_mismatches'].append({'path': relative, 'expected': revision, 'observed': observed})
    report['all_heads_match'] = report['matching_heads'] == report['projects']
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tree', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--output', required=True, help='New report path; existing files are preserved')
    parser.add_argument('--require-pins', action='store_true')
    args = parser.parse_args()
    report = audit(args.tree, args.manifest)
    descriptor = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print('Manifest HEAD matches: %d/%d; report: %s' %
          (report['matching_heads'], report['projects'], args.output))
    if args.require_pins and not report['all_heads_match']:
        raise ValueError('Checkout HEADs do not match the manifest; inspect the source report before building.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, ET.ParseError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
