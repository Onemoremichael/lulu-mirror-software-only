"""Freeze build recipes and validated camera files for one build invocation."""
import shutil
from pathlib import Path
from .camera_artifacts import FILES, validate


def snapshot(root, output, camera=None):
    root, output = Path(root), Path(output)
    destination = output / 'inputs'
    destination.mkdir(exist_ok=False)
    shutil.copytree(root / 'build', destination / 'build',
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    report = None
    if camera is not None:
        # Validate both before and after copying: later host edits cannot change
        # what the container consumes, and a change during copying is rejected.
        validate(camera)
        files = destination / 'camera-artifacts'
        files.mkdir()
        for name in (*FILES, 'camera-report.json'):
            shutil.copyfile(Path(camera) / name, files / name)
        report = validate(files)
        shutil.copytree(root / 'camera', destination / 'camera-patches')
    return destination, report
