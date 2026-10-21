from pathlib import Path
import struct
import tempfile
import unittest
from build.elf import check, audit


class ElfBoundsTests(unittest.TestCase):
    def test_missing_audit_root_does_not_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                audit(Path(temporary) / 'missing')

    def test_32_bit_segment_bounds(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'fixture.so'
            ident = b'\x7fELF\x01\x01\x01' + bytes(9)
            header = struct.pack('<16sHHIIIIIHHHHHH', ident, 3, 40, 1,
                                 0, 52, 0, 0, 52, 32, 1, 40, 0, 0)
            program = struct.pack('<IIIIIIII', 1, 0, 0, 0, 84, 4096, 5, 4096)
            path.write_bytes(header + program)
            self.assertIsNone(check(path))
            program = struct.pack('<IIIIIIII', 1, 0, 0, 0, 85, 4096, 5, 4096)
            path.write_bytes(header + program)
            self.assertIn('segment extends', check(path))

    def test_bounds_and_nobits(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'fixture.so'
            ident = b'\x7fELF\x02\x01\x01' + bytes(9)
            header = struct.pack('<16sHHIQQQIHHHHHH', ident, 3, 183, 1,
                                 0, 0, 64, 0, 64, 56, 0, 64, 1, 0)
            section = struct.pack('<IIQQQQIIQQ', 0, 8, 0, 0, 4096, 4096, 0, 0, 0, 0)
            path.write_bytes(header + section)
            self.assertIsNone(check(path))
            path.write_bytes((header + section)[:-1])
            self.assertIn('table extends', check(path))
            section = struct.pack('<IIQQQQIIQQ', 0, 1, 0, 0, 4096, 4096, 0, 0, 0, 0)
            path.write_bytes(header + section)
            self.assertIn('section extends', check(path))
            path.write_bytes(b'')
            self.assertIn('Missing', check(path))
            archive = Path(temporary) / 'built-in.o'
            archive.write_bytes(b'!<arch>\n')
            self.assertIsNone(check(archive))
            archive.write_bytes(b'BC\xc0\xde')
            self.assertIsNone(check(archive))
