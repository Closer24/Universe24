"""Hand V1 (2026-10-25), item (a) continued: the uniform sea under the write, the close on and the close off.

The bare 3-cube of the tests' small universe with the uniform sea (no hole), the volume laid rising (X_before = X_now - 1) from X_0; (i) the close on (Lattice.step): every output line counted by event and cause per interval, the sea's drift, the sea's quanta read by the engine and the static formula at the X the board holds, every family's quanta; (ii) the close off (Lattice.advanced_to_the_close alone, the click act skipped, every other act taken): the same readings. The two runs separate the read's unit (the frame weight at the X the board holds) from the acts on the light (the births' takes and the swap).

Run: PYTHONPATH=<worktree>/src:<worktree> TMPDIR=/dev/shm/tmp python tools/derivations/v1/pump_dynamics.py
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from event_universe import records, seed, world_files
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features import volume
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_universe import SMALL, time_line_set

GAMMA, T, DEN = SMALL["integers"]["node_clock"], SMALL["integers"]["quantum_action"], SMALL["integers"]["den"]
HERE = Path(__file__).resolve().parent


def board_of(folder: Path, lines: list) -> Lattice:
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    (folder / "u.json").write_text(json.dumps(SMALL), encoding="utf-8")
    (folder / "bare.json").write_text(
        json.dumps({"universe": "u.json", "shape": [3, 3, 3], "intervals": 4000}), encoding="utf-8"
    )
    return Lattice(load_world(folder / "bare.json"), output=lines.append)


def uniform_sea(board: Lattice) -> int:
    light = board.world.seed
    v = seed.drift_of(board.world.quantum_action)
    state = board.states[light]
    state.lines[0] = records.Record(
        records.full(board.shape, v, board.kind), records.zeros(board.shape, board.kind), state.lines[0].remainder
    )
    return v


def formula(x: int, v: int, unit: int) -> int:
    c = int(volume.level_of(GAMMA, np.array([x], dtype=object))[0])
    pi = paces.link_pace(GAMMA, c)
    if pi == 0:
        return -1
    e = int(division_forward(3 * DEN * GAMMA * GAMMA * v * v, pi * pi, 0)[0])
    return int(division_forward(e + division_forward(unit, 2, 0)[0], unit, 0)[0])


def run(close: bool, start_u: float, intervals: int, folder: Path) -> dict:
    lines: list = []
    board = board_of(folder, lines)
    light, held = board.world.seed, board.held[0]
    v = uniform_sea(board)
    unit = int(board.credit.units[light])
    x0 = int(round(GAMMA * math.exp(4 * start_u)))
    time_line_set(board, x0, x0 - 1)
    series, events = [], Counter()
    names = [f.name for f in board.families]
    for t in range(intervals + 1):
        x_now = int(board.states[held].lines[0].now[0, 0, 0])
        line = board.states[light].lines[0]
        drift = np.asarray(line.now, dtype=object) - np.asarray(line.before, dtype=object)
        quanta, cold = board.quanta(light)
        others = {}
        for i, f in enumerate(board.families):
            if i != light and f.quanta and len(board.states[i].lines) > 0:
                q, _c = board.quanta(i)
                total = int(np.asarray(q, dtype=object).sum())
                if total:
                    others[f.name] = total
        row = {
            "t": t, "X": x_now, "U": math.log(x_now / GAMMA) / 4, "quanta_node": int(quanta[0, 0, 0]),
            "quanta_total": int(np.asarray(quanta, dtype=object).sum()), "formula_at_X_v189": formula(x_now, v, unit),
            "formula_at_X_drift": formula(x_now, abs(int(drift[0, 0, 0])), unit),
            "drift_min": int(drift.min()), "drift_max": int(drift.max()), "turned": int(board.turned.sum()),
            "others": others, "events_so_far": dict(events),
        }
        series.append(row)
        if t % 20 == 0 or t == intervals:
            print(f"close {close} U0 {start_u}: t {t} X {x_now} U {row['U']:.4f} drift [{row['drift_min']}, {row['drift_max']}] light/Node {row['quanta_node']} total {row['quanta_total']} formula(v) {row['formula_at_X_v189']} formula(drift) {row['formula_at_X_drift']} turned {row['turned']} others {others} events {dict(events)}")
        if t == intervals:
            break
        before = len(lines)
        if close:
            board.step()
        else:
            board.advanced_to_the_close()
        for li in lines[before:]:
            key = li["event"] + ("/" + str(li.get("cause", li.get("reason", ""))) if li["event"] == "refused" else "")
            events[key] += 1
    return {"close": close, "start_U": start_u, "X_0": x0, "families": names, "series": series, "events": dict(events),
            "first_lines": [li for li in lines[:12]]}


def main() -> None:
    folder = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / "v1_pump_dyn"
    out = [
        run(True, 0.0, 320, folder / "a"),
        run(False, 0.0, 320, folder / "b"),
        run(True, 0.5, 200, folder / "c"),
        run(False, 0.5, 200, folder / "d"),
    ]
    (HERE / "pump_dynamics.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print("written", HERE / "pump_dynamics.json")


if __name__ == "__main__":
    sys.exit(main())
