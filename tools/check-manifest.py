#!/usr/bin/env python3
"""Check that Android source revisions are explicit and checkout paths are unique."""
import json
from pathlib import Path, PurePosixPath
import re
import sys
import xml.etree.ElementTree as ET


def check(path):
    document = ET.parse(path).getroot()
    remotes = {r.attrib['name']: r.attrib['fetch'] for r in document.findall('remote')}
    default = document.find('default').attrib['remote']
    projects = document.findall('project')
    if len(projects) != 447:
        raise ValueError('Expected the 447-project source manifest.')
    paths = set()
    for project in projects:
        revision = project.attrib.get('revision', '')
        path = PurePosixPath(project.attrib.get('path', project.attrib['name']))
        if not re.fullmatch('[0-9a-f]{40}', revision):
            raise ValueError('Unpinned source project: ' + str(path))
        if path.is_absolute() or '..' in path.parts or str(path) in paths:
            raise ValueError('Unsafe or duplicate checkout path: ' + str(path))
        remote = remotes[project.attrib.get('remote', default)]
        if not remote.startswith('https://'):
            raise ValueError('Expected HTTPS source remote.')
        paths.add(str(path))
    return {'projects': len(projects), 'all_revisions_pinned': True,
            'note': 'Static validation only; does not establish remote availability or vendor licensing.'}


if __name__ == '__main__':
    try:
        print(json.dumps(check(Path(__file__).resolve().parent.parent / 'build/manifest.xml'), indent=2))
    except (ValueError, KeyError, ET.ParseError) as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
