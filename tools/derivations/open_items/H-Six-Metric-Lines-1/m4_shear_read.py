"""m4 (hand y1): the shears are read by no act and the fluxes by the planes alone. Two flagged boards (U24_METRIC=1) of the bare 3-cube hole seed stepped 6 intervals alike (through the births at 4); on the second the three shear lines are set to 0 (both levels) at the interval's start; both stepped one interval; every array compared: the arrays that differ are the shear lines and their write remainders and nothing else (the theorem: a one-Link stencil's symbol is separable, no k_a k_b term, so no shear enters any reach, pair or level). The same with the three flux lines zeroed: the plane records' lines differ (the fold reads them), light's and the sign's rows' Rule3 steps do not read them (the sign's write does, through the planes' changed Wronskian, named). Integers only."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import y1lib  # noqa: E402

assert os.environ.get("U24_METRIC") == "1"
from event_universe import records  # noqa: E402

out: dict = {}
for label, zeroed in (("shears_zeroed", (7, 8, 9)), ("fluxes_zeroed", (4, 5, 6))):
    a = y1lib.board_of(Path(f"/dev/shm/tmp/y1_m4a_{label}"))
    b = y1lib.board_of(Path(f"/dev/shm/tmp/y1_m4b_{label}"))
    for _ in range(6):
        a.step()
        b.step()
    assert y1lib.digest(y1lib.snapshot(a)) == y1lib.digest(y1lib.snapshot(b))
    volume = b.held[0]
    lines = list(b.states[volume].lines)
    nonzero_before = {n: int(np.count_nonzero(np.asarray(lines[n].now, dtype=object))) for n in zeroed}
    for n in zeroed:
        zeros = np.zeros(b.shape, dtype=object)
        lines[n] = records.Record(zeros, zeros.copy(), lines[n].remainder)
    b.states[volume].lines = lines
    a.step()
    b.step()
    sa, sb = y1lib.snapshot(a), y1lib.snapshot(b)
    differ = sorted(key for key in sa if sa[key] != sb[key])
    by_family: dict[str, int] = {}
    for key in differ:
        by_family[key.split(" ")[0]] = by_family.get(key.split(" ")[0], 0) + 1
    out[label] = {"zeroed_lines": list(zeroed), "nonzero_nodes_before_zeroing": nonzero_before, "arrays_total": len(sa) - 1, "arrays_differing": len(differ), "differing_by_family": by_family, "differing_arrays": differ}
    print(label, json.dumps({k: v for k, v in out[label].items() if k != "differing_arrays"}))
(HERE / "m4_shear_read.json").write_text(json.dumps(out, indent=1))
