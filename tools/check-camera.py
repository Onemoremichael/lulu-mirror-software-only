#!/usr/bin/env python3
"""Host memory/ABI checks; no camera, microphone, device or network access."""
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='mirror-camera-check-') as temp:
    for source, compiler in [('test-video-pack.cpp', 'c++'), ('test-isp-compat.c', 'cc')]:
        executable = shutil.which(compiler)
        if not executable:
            raise SystemExit('Install a C/C++ compiler: missing ' + compiler)
        output = str(Path(temp) / source.split('.')[0])
        subprocess.run([executable, '-Wall', '-Wextra', '-Werror', '-g',
                        '-fsanitize=address,undefined', str(root / 'camera' / source), '-o', output], check=True)
        subprocess.run([output], check=True)
