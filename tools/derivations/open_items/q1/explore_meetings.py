"""Hand q1, the exploration: the bare 3-cube torus of the tests' small universe (den 1,021) under the engine's own hole seed, run through its first births; per interval the light's share per Node in quanta, the births, and per Link the light's current F_ij = num (now_i before_j - before_i now_j) at the interval's start (the odd reading of the Link's two ends), so that the Link meetings and whether the odd reading is 0 there can be read.

Usage: PYTHONPATH=<worktree>/src python tools/derivations/q1/explore_meetings.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from event_universe import records, world_files  # noqa: E402
from event_universe.core.ports import AXES, arrival  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import bare_torus  # noqa: E402

OUT = Path(__file__).resolve().parent


def currents(board: Lattice, index: int) -> dict[str, object]:
    """F_ij on every +a Link of every Node from the levels the interval starts from: num (now_i before_j - before_i now_j)."""
    family = board.families[index]
    num = family.pair[0]
    line = board.states[index].lines[records.record_slice(family, 0)][0]
    now, before = np.asarray(line.now, dtype=object), np.asarray(line.before, dtype=object)
    found = {}
    for a in range(AXES):
        now_j, before_j = arrival(now, a, 1), arrival(before, a, 1)
        f = num * (now * before_j - before * now_j)
        found[a] = f
    return found


def main() -> None:
    folder = Path("/dev/shm/tmp/q1_explore")
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    lines: list[dict] = []
    board = Lattice(load_world(bare_torus(folder, 3, 12)), output=lines.append)
    light = board.world.seed
    unit = board.credit.units[light]
    report = []
    for _ in range(8):
        shares, frozen = board.share_of(light)
        f = currents(board, light)
        nodes = {}
        for at in np.ndindex(*board.shape):
            nodes[str(at)] = {
                "quanta": round(int(shares[at]) / unit, 3),
                "F": [int(f[a][at]) for a in range(AXES)],
            }
        whole = [k for k, v in nodes.items() if v["quanta"] >= 1]
        zero_links = sum(1 for v in nodes.values() for x in v["F"] if x == 0)
        report.append(
            {
                "interval_start": board.interval,
                "nodes_with_a_whole_quantum": whole,
                "links_with_F_0": zero_links,
                "nodes": nodes,
            }
        )
        board.step()
        report[-1]["births_this_interval"] = [
            (x["nodes"], x["children"], x["senses"]) for x in lines if x.get("event") == "birth" and x["interval"] == board.interval
        ]
        report[-1]["refused"] = [
            (x.get("node"), x.get("cause")) for x in lines if x.get("event") == "refused" and x["interval"] == board.interval
        ]
    (OUT / "explore_meetings.json").write_text(json.dumps(report, indent=1))
    for r in report:
        print(
            r["interval_start"],
            "whole:",
            len(r["nodes_with_a_whole_quantum"]),
            "F=0 links:",
            r["links_with_F_0"],
            "of 81; births:",
            r["births_this_interval"],
            "refused:",
            r["refused"][:3],
        )
    print("unit W_c", unit)


if __name__ == "__main__":
    main()
