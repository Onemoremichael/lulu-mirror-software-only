"""Read-only ELF truncation checks; compatible with the legacy Python 2 builder."""
from __future__ import print_function
import argparse
import json
import os
import struct


def check(path):
    size = os.path.getsize(path)
    with open(path, 'rb') as stream:
        ident = stream.read(16)
        # Kbuild legitimately uses archive-format built-in.o for empty groups;
        # LTO can also leave LLVM bitcode in a .o. Neither is an ELF truncation.
        if str(path).endswith('.o') and (ident.startswith(b'!<arch>\n') or ident.startswith(b'BC\xc0\xde')):
            return None
        if len(ident) < 16 or ident[:4] != b'\x7fELF':
            return 'Missing ELF header'
        fields = bytearray(ident)
        if fields[4] not in (1, 2) or fields[5] not in (1, 2):
            return 'Unsupported ELF class/byte order'
        prefix = '<' if fields[5] == 1 else '>'
        fmt = prefix + ('16sHHIIIIIHHHHHH' if fields[4] == 1 else '16sHHIQQQIHHHHHH')
        stream.seek(0)
        header = stream.read(struct.calcsize(fmt))
        if len(header) != struct.calcsize(fmt):
            return 'Truncated ELF header'
        value = struct.unpack(fmt, header)
        phoff, shoff, phsize, phnum, shsize, shnum = value[5], value[6], value[9], value[10], value[11], value[12]
        if phoff + phsize * phnum > size or shoff + shsize * shnum > size:
            return 'ELF header table extends past end of file'
        program_fmt = prefix + ('IIIIIIII' if fields[4] == 1 else 'IIQQQQQQ')
        if phnum and phsize != struct.calcsize(program_fmt):
            return 'Unexpected ELF program entry size'
        for index in range(phnum):
            stream.seek(phoff + index * phsize)
            program = struct.unpack(program_fmt, stream.read(phsize))
            offset, length = (program[1], program[4]) if fields[4] == 1 else (program[2], program[5])
            if program[0] != 0 and length and offset + length > size:
                return 'ELF segment extends past end of file'
        section_fmt = prefix + ('IIIIIIIIII' if fields[4] == 1 else 'IIQQQQIIQQ')
        section_size = struct.calcsize(section_fmt)
        if shnum and shsize != section_size:
            return 'Unexpected ELF section entry size'
        for index in range(shnum):
            stream.seek(shoff + index * shsize)
            section = struct.unpack(section_fmt, stream.read(section_size))
            # NOBITS represents memory-only data, not bytes in the file.
            if section[1] not in (0, 8) and section[5] and section[4] + section[5] > size:
                return 'ELF section extends past end of file'
    return None


def audit(root):
    if not os.path.isdir(root):
        raise ValueError('ELF audit root must be an existing directory')
    invalid = []
    for directory, unused_dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith(('.so', '.o')):
                continue
            path = os.path.join(directory, name)
            if os.path.islink(path):
                continue
            reason = check(path)
            if reason:
                invalid.append({'path': os.path.relpath(path, root), 'reason': reason})
    return invalid


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root')
    args = parser.parse_args()
    invalid = audit(args.root)
    print(json.dumps(invalid, indent=2))
    raise SystemExit(1 if invalid else 0)
