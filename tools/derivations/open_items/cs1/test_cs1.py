"""cs1's one-Node test (the 4-cube is the one-Node line on a uniform seed): the zigzag light without the sea, 160 intervals, under 15 s. The pass predicate, by shape and number: X uniform (min = max) at 160 of 160; the top's mean 2,786 at i 77 with 64 Nodes turning at 78; every Node at Gamma at 154 and 155; the light's current not 0 on 192 of 192 Links and the twist not 0 on exactly 128 (the x- and y-Links) at i 1; refused by the lay 128 and by the twist 64 at i 1; births 0; run back 5 of 5; bits at most 116.

Usage: python test_cs1.py (from this folder; PYTHONPATH the worktree's src)."""

from __future__ import annotations

import json
import os
import sys
import time

from event_universe.loader.world import load_world

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs_run import CsNode  # noqa: E402

from event_universe import run  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    sys.set_int_max_str_digits(0)
    t0 = time.monotonic_ns()
    universe, world = load_world(os.path.join(HERE, "worlds", "empty4_400.json"))
    world = dict(world, intervals=160)
    with open(os.path.join(HERE, "worlds", "zigzag_m.json"), encoding="utf-8") as f:
        pattern = json.load(f)
    node = CsNode(universe, world, pattern)
    rows, nodes, hashes = run.forward(node, 160, 5, lambda line: None)
    back = run.run_back(node, hashes)
    diag = node.diag
    failures = []
    if any(d["X_min"] != d["X_max"] for d in diag):
        failures.append("the board is not uniform at some interval")
    if diag[77]["X_mean"] != 2786 or diag[78]["turned"] != 64:
        failures.append(f"the top: mean {diag[77]['X_mean']} at 77, turned {diag[78]['turned']} at 78")
    if not (diag[154]["X_min"] == diag[154]["X_max"] == 1000 and diag[155]["X_min"] == diag[155]["X_max"] == 1000):
        failures.append(f"the return: {diag[154]['X_min']}..{diag[154]['X_max']} at 154, {diag[155]['X_min']}..{diag[155]['X_max']} at 155")
    if diag[1]["F_links_nonzero_per_axis"] != [64, 64, 64] or diag[1]["twist_links_nonzero_per_axis"] != [64, 64, 0]:
        failures.append(f"the current and the twist at 1: {diag[1]['F_links_nonzero_per_axis']} {diag[1]['twist_links_nonzero_per_axis']}")
    if diag[1]["refused_lay"] != 128 or diag[1]["refused_twist"] != 64 or diag[1]["refused_orientation"] != 0:
        failures.append(f"the refusals at 1: lay {diag[1]['refused_lay']} twist {diag[1]['refused_twist']} orientation {diag[1]['refused_orientation']}")
    if node.counts["births"] != 0:
        failures.append(f"births {node.counts['births']}")
    if back["exact"] != 5:
        failures.append(f"run back {back}")
    bits = max(d["bits"] for d in diag)
    if bits > 116:
        failures.append(f"bits {bits}")
    ms = (time.monotonic_ns() - t0) // 1000000
    print(json.dumps({"failures": failures, "milliseconds": ms, "bits": bits, "counts": {k: str(v) for k, v in node.counts.items()}, "run back": back}))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
