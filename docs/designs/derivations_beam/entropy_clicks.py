"""The entropy of the click on the register (read-only, the derivation
mathematician, 2026-09-21; DERIVATIONS_BEAM.md section 14): per world the
bits a click reads (the Shannon entropy H of the cell distribution over
the 64 births) and the bits it erases about the birth phase u (log2 N -
H), from the registered click counts of expectations.json; no run.

Run from the repository root:

    python docs/designs/derivations_beam/entropy_clicks.py > docs/designs/derivations_beam/entropy_clicks.out
"""

from __future__ import annotations

import json
import math
from pathlib import Path

N = 64
ROOT = Path(__file__).resolve().parents[3] / "examples" / "events" / "amplitude"
expectations = json.loads((ROOT / "expectations.json").read_text())


def entropy(counts: list[int]) -> float:
    total = sum(counts)
    return -sum(c / total * math.log2(c / total) for c in counts if c)


cases = {
    "mz_equal (L1)": [64, 0],
    "mz_quarter (L1)": [32, 32],
    "mz_345 (L1)": [63, 1],
    "bell 16_24, the pair (L3)": [27, 5, 5, 27],
    "path 16_24, the pair read (L3)": [2, 14, 2, 14, 14, 2, 14, 2],
    "slits_low (L2)": list(expectations["two_slits"]["clicks"].values()),
}
units = {
    "mz_equal (L1)": 82,
    "mz_quarter (L1)": 82,
    "mz_345 (L1)": 14,
    "bell 16_24, the pair (L3)": 4,
    "path 16_24, the pair read (L3)": 4,
    "slits_low (L2)": 185,
}
print("THE CLICK'S ENTROPY ON THE REGISTER (N = 64 births, u spanning the circle once)")
print(
    "world | cells (the registered clicks) | bits read H | bits erased about u, log2 N - H | log2 (cells) | the units at the ends (6.1)"
)
for name, counts in cases.items():
    h = entropy(counts)
    cells = len(counts)
    print(
        f"{name} | {counts} | {h:.3f} | {math.log2(N) - h:.3f} | {math.log2(cells):.2f} | {units[name]}"
    )
print("identity: bits read + bits erased about u = log2 N = 6 per record, on every row above")
