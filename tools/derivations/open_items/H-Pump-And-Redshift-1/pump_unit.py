"""Hand V1 (2026-10-25), item (a): the quanta of the massless uniform sea against the volume's level X, read statically (no dynamics) and under the write.

A uniform massless sea (now = v, before = 0 at every Node, v^2 <= T, no hole) on the bare 3-cube of the tests' small universe (den 1,021, Gamma 1,000, T 36,000); the volume's time line set by hand to X at every Node (tests.laws_universe.time_line_set), X = Gamma e^(4 U) in the engine's own variable (features/volume: X = Gamma (Gamma / p_0)^(d + 1), d + 1 = 4); the count of quanta read through Lattice.quanta (the share over W_c) at each X with nothing stepped; then from one X the board run with the write on (Lattice.step, the close included) and the count read every interval beside the static formula at the X the board holds.

Run: PYTHONPATH=<worktree>/src:<worktree> TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Pump-And-Redshift-1/pump_unit.py
"""

from __future__ import annotations

import json
import math
import os
import sys
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


def board_of(cube: int, folder: Path) -> Lattice:
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    (folder / "u.json").write_text(json.dumps(SMALL), encoding="utf-8")
    (folder / "bare.json").write_text(
        json.dumps({"universe": "u.json", "shape": [cube] * 3, "intervals": 4000}), encoding="utf-8"
    )
    return Lattice(load_world(folder / "bare.json"))


def uniform_sea(board: Lattice) -> int:
    """The light's record replaced by the uniform sea at the drift v on every Node (the origin included): the law's seed to 2026-10-24, laid by name."""
    light = board.world.seed
    v = seed.drift_of(board.world.quantum_action)
    state = board.states[light]
    now = records.full(board.shape, v, board.kind)
    before = records.zeros(board.shape, board.kind)
    state.lines[0] = records.Record(now, before, state.lines[0].remainder)
    return v


def static_count(x: int, v: int, unit: int) -> tuple[int, int, int, int, int]:
    """The share per Node of the sea by the law's formula at the volume X: c = level_of(X), p_0 = clock(c), p_i = p_0^2 / Gamma rounded, e = (6 den Gamma^2 G^2 v^2) div (2 p_i^2 G^2) = (3 den Gamma^2 v^2) div p_i^2; in quanta (e + W_c div 2) div W_c."""
    c = int(volume.level_of(GAMMA, np.array([x], dtype=object))[0])
    p0, pi = paces.clock(GAMMA, c), paces.link_pace(GAMMA, c)
    e = int(division_forward(3 * DEN * GAMMA * GAMMA * v * v, pi * pi, 0)[0])
    q = int(division_forward(e + division_forward(unit, 2, 0)[0], unit, 0)[0])
    return c, p0, pi, e, q


def main() -> None:
    out = {"universe": SMALL["integers"], "static": [], "dynamic": []}
    folder = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / "v1_pump"
    board = board_of(3, folder)
    light, held = board.world.seed, board.held[0]
    v = uniform_sea(board)
    unit = int(board.credit.units[light])
    out["drift_v"], out["unit_W_rec"], out["W_c"] = v, unit, 3 * DEN * T
    out["frozen_content"] = paces.frozen_content(GAMMA)
    print(f"den {DEN} Gamma {GAMMA} T {T} v {v} v^2 {v * v} W_rec {unit} W_c {3 * DEN * T} frozen {out['frozen_content']}")
    print("U, X, c, p_0, p_i, X/Gamma, (Gamma/p_i)^2, share/Node (engine), share/Node (formula), quanta/Node (engine), quanta/Node (formula), total quanta, after one interval written")
    nodes = int(np.prod(board.shape))
    for k in range(0, 17):
        x = GAMMA * 2**k  # X = Gamma e^(4 U): U = k ln 2 / 4
        u = math.log(x / GAMMA) / 4
        c, p0, pi, e_f, q_f = static_count(x, v, unit)
        if pi == 0:
            print(f"U {u:.4f} X {x}: frozen (p_i 0), not read")
            break
        time_line_set(board, x, x)
        content, _factors = board.read(light, 1, 0)
        shares, cold = board.share_of(light)
        quanta, _cold = board.quanta(light)
        assert int(content.reshape(-1)[0]) == c and not cold.any()
        e_engine, q_engine = int(shares[0, 0, 0]), int(quanta[0, 0, 0])
        assert (np.asarray(shares, dtype=object) == e_engine).all()
        row = {
            "U": u, "X": x, "c": c, "p_0": p0, "p_i": pi, "X_over_Gamma": x // GAMMA,
            "frame_weight": (GAMMA / pi) ** 2, "share_engine": e_engine, "share_formula": e_f,
            "quanta_engine": q_engine, "quanta_formula": q_f, "total_quanta": int(np.asarray(quanta, dtype=object).sum()),
        }
        out["static"].append(row)
        print(f"U {u:.4f} X {x} c {c} p_0 {p0} p_i {pi} X/G {x // GAMMA} (G/p_i)^2 {(GAMMA / pi) ** 2:.2f} share {e_engine} formula {e_f} quanta {q_engine} formula {q_f} total {row['total_quanta']}")
    # the dynamics: from X_0 at U = 0.5 (X = Gamma e^2 rounded) the write on, the close included, 300 intervals
    for start_u in (0.0, 0.5, 1.0):
        x0 = int(round(GAMMA * math.exp(4 * start_u)))
        board = board_of(3, folder / f"dyn_{start_u}")
        v = uniform_sea(board)
        time_line_set(board, x0, x0)
        series = []
        for t in range(301):
            x_now = int(board.states[held].lines[0].now[0, 0, 0])
            x_before = int(board.states[held].lines[0].before[0, 0, 0])
            line = board.states[light].lines[0]
            drift = np.asarray(line.now, dtype=object) - np.asarray(line.before, dtype=object)
            quanta, cold = board.quanta(light)
            c, p0, pi, e_f, q_f = static_count(x_now, v, unit)
            same_x = bool((np.asarray(board.states[held].lines[0].now, dtype=object) == x_now).all())
            row = {
                "t": t, "X": x_now, "X_before": x_before, "U": math.log(x_now / GAMMA) / 4, "c": c, "p_i": pi,
                "quanta_node": int(quanta[0, 0, 0]), "quanta_formula_at_X": q_f,
                "total": int(np.asarray(quanta, dtype=object).sum()), "drift_min": int(drift.min()), "drift_max": int(drift.max()),
                "uniform_X": same_x, "frozen": bool(cold.any()),
            }
            series.append(row)
            if t % 25 == 0:
                print(f"start U {start_u}: t {t} X {x_now} U {row['U']:.4f} c {c} p_i {pi} quanta/Node {row['quanta_node']} formula {q_f} total {row['total']} drift [{row['drift_min']}, {row['drift_max']}] uniform {same_x} turned {int(board.turned.sum())}")
            if t == 300:
                break
            board.step()
        out["dynamic"].append({"start_U": start_u, "X_0": x0, "series": series})
    (HERE / "pump_unit.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written", HERE / "pump_unit.json")


if __name__ == "__main__":
    sys.exit(main())
