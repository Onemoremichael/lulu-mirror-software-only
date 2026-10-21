#!/usr/bin/env python3
"""Validate the documentary catalog without contacting sources or any device."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from hardware.research.validation import validate_catalog


if __name__ == '__main__':
    try:
        result = validate_catalog(json.loads((ROOT / 'hardware/research/catalog.json').read_text()), ROOT)
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
