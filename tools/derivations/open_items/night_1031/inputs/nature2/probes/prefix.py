"""NATURE2: is a shorter run's record the prefix of a longer run's? The click lines of the short record against the
longer record's click lines at the same rounds, byte for byte as JSON text. Whole numbers only.

Usage: python3 -I prefix.py <short record .jsonl> <long record .jsonl>
"""

import json
import sys
from pathlib import Path


def clicks(path):
    return [t for t in Path(path).read_text(encoding="utf-8").splitlines() if '"kind": "click"' in t]


short, long_ = clicks(sys.argv[1]), clicks(sys.argv[2])
last = max(json.loads(t)["round"] for t in short) if short else 0
head = [t for t in long_ if json.loads(t)["round"] <= last]
alike = sum(1 for a, b in zip(short, head) if a == b)
print(f"short: {len(short)} click lines to round {last}; long: {len(head)} click lines to that round;"
      f" alike in order {alike}; the prefix {'SHOWN' if alike == len(short) == len(head) else 'NOT SHOWN'}")
