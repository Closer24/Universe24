"""Hand V1 (2026-10-25), item (b): the massless line's dispersion and the redshift on a chain torus whose frame is set by hand, integer readings only.

The chain [28, 1, 1] of the tests' small universe (den 1,021, Gamma 1,000, T 36,000; the y and z axes of one layer fold); the light's record replaced by a travelling wave at the wave number k = pi / 2 (cos k = 0, the wavelength 4 Links; the law's dispersion there 1 - cos omega = p_i^2 / (3 Gamma^2), a rational), amplitude A, laid at the dispersion of the hand-set content with the law's own integer sine (rule3.largest_below); the frame held by hand at every interval's start: the volume's time line at X = Gamma m^4 (so the Link's length Gamma / p_0 is the integer m to the clock's rounding, tests.laws_universe.time_line_set) and the held row's three tension lines at 0; every act of the interval but the close taken (Lattice.advanced_to_the_close; the click act skipped by name so that no birth takes from the wave). Readings, integers: the upward zero crossings n of the level at Node 0 over a span of S intervals; the engine's proper count over the span (Lattice.proper_count, the Node's clock p_0 summed); the share and the count in W_c at the span's ends; the amplitude. The redshift predicate in integers: the proper period scales with m, SUM p_0 (m) x n(1) against SUM p_0 (1) x n(m) x m, within one crossing. A float stands only as a check beside its integer reading (marked check_).

Run: PYTHONPATH=<worktree>/src:<worktree> TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Pump-And-Redshift-1/redshift_chain.py
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

from event_universe import records, world_files
from event_universe.core import paces
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.features import volume
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_universe import SMALL, time_line_set

GAMMA, T, DEN = SMALL["integers"]["node_clock"], SMALL["integers"]["quantum_action"], SMALL["integers"]["den"]
HERE = Path(__file__).resolve().parent
N, A = 28, 1500  # the chain's Nodes (k = pi / 2 fits 7 wavelengths), the amplitude
SPAN = 2000


def board_of(folder: Path) -> Lattice:
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    (folder / "u.json").write_text(json.dumps(SMALL), encoding="utf-8")
    (folder / "chain.json").write_text(
        json.dumps({"universe": "u.json", "shape": [N, 1, 1], "intervals": 100000}), encoding="utf-8"
    )
    return Lattice(load_world(folder / "chain.json"))


def paces_of(x: int) -> tuple[int, int, int]:
    c = int(volume.level_of(GAMMA, np.array([x], dtype=object))[0])
    return c, paces.clock(GAMMA, c), paces.link_pace(GAMMA, c)


def hold_frame(board: Lattice, x: int) -> None:
    """The frame by hand: the time line at X, laid rising (X_before = X - 1000, or X div 2 at X <= 1000, so that the volume's own step never reaches a weak maximum under a negative write and the swap stays off; the first run at X_before = X - 1 turned every Node every interval from m 3, the swap time-reversing the wave) and the three tension lines at 0."""
    time_line_set(board, x, x - 1000 if x > 1000 else x // 2)
    state = board.states[board.held[0]]
    zeros = records.zeros(board.shape, board.kind)
    for n in range(1, 4):
        state.lines[n] = records.Record(zeros.copy(), zeros.copy(), state.lines[n].remainder)


def lay_wave(board: Lattice, x: int) -> dict:
    """The travelling wave at k = pi / 2: now = (A, 0, -A, 0, ...), before = (A cos omega, -A sin omega, -A cos omega, A sin omega, ...) with cos omega = (3 Gamma^2 - p_i^2) / (3 Gamma^2) and A sin omega the law's integer sine, largest_below(A^2 ((3 Gamma^2)^2 - (3 Gamma^2 - p_i^2)^2)) div (3 Gamma^2)."""
    light = board.world.seed
    _c, _p0, pi = paces_of(x)
    wall = 3 * GAMMA * GAMMA
    cos_num = wall - pi * pi
    a_cos = int(division_forward(A * cos_num, wall, 0)[0])
    a_sin = int(division_forward(largest_below(A * A * (wall * wall - cos_num * cos_num)), wall, 0)[0])
    pattern_now, pattern_before = (A, 0, -A, 0), (a_cos, -a_sin, -a_cos, a_sin)
    now = np.array([[[pattern_now[i % 4]]] for i in range(N)], dtype=object)
    before = np.array([[[pattern_before[i % 4]]] for i in range(N)], dtype=object)
    state = board.states[light]
    state.lines[0] = records.Record(
        np.asarray(now, dtype=board.kind), np.asarray(before, dtype=board.kind), state.lines[0].remainder
    )
    return {"cos_omega_pair": [cos_num, wall], "A_cos": a_cos, "A_sin": a_sin}


def readings(board: Lattice) -> dict:
    light = board.world.seed
    line = board.states[light].lines[0]
    shares, cold = board.share_of(light)
    quanta, _c = board.quanta(light)
    return {
        "share_total": int(np.asarray(shares, dtype=object).sum()),
        "quanta_total": int(np.asarray(quanta, dtype=object).sum()),
        "amplitude": int(np.abs(np.asarray(line.now, dtype=object)).max()),
        "frozen": bool(cold.any()),
    }


def run_span(board: Lattice, x_of_t, start: int, span: int) -> dict:
    """The span [start, start + span): the frame held each interval, the level at Node 0 recorded, the crossings counted, the engine's proper count differenced."""
    light = board.world.seed
    proper_0 = int(np.asarray(board.proper_count, dtype=object).reshape(-1)[0]) if np.ndim(board.proper_count) else int(board.proper_count)
    levels, turned = [], 0
    for t in range(start, start + span):
        hold_frame(board, x_of_t(t))
        levels.append(int(board.states[light].lines[0].now[0, 0, 0]))
        board.advanced_to_the_close()
        turned += int(board.turned.sum())
    proper_1 = int(np.asarray(board.proper_count, dtype=object).reshape(-1)[0]) if np.ndim(board.proper_count) else int(board.proper_count)
    n = sum(1 for a, b in zip(levels, levels[1:]) if a < 0 <= b)
    return {"crossings": n, "proper_sum_p0": proper_1 - proper_0, "levels_head": levels[:12], "turned_node_intervals": turned,
            "amplitude_max": max(abs(v) for v in levels)}


def fixed(folder: Path) -> list[dict]:
    out = []
    for m in (1, 2, 3, 4, 5, 6):
        x = GAMMA * m**4
        board = board_of(folder / f"m{m}")
        c, p0, pi = paces_of(x)
        lay = lay_wave(board, x)
        hold_frame(board, x)
        before = readings(board)
        span = run_span(board, lambda t, x=x: x, 0, SPAN)
        after = readings(board)
        n = span["crossings"]
        period_q, period_r = (divmod(SPAN, n) if n else (None, None))
        proper_period_q, proper_period_r = (divmod(span["proper_sum_p0"], n * GAMMA) if n else (None, None))
        row = {
            "m": m, "X": x, "c": c, "p_0": p0, "p_i": pi, "lay": lay, "span": SPAN, "crossings": n,
            "period_intervals": [period_q, period_r], "proper_sum_p0": span["proper_sum_p0"],
            "proper_period_intervals": [proper_period_q, proper_period_r],
            "share_start": before["share_total"], "share_end": after["share_total"],
            "quanta_start": before["quanta_total"], "quanta_end": after["quanta_total"],
            "amplitude_start": before["amplitude"], "amplitude_end": after["amplitude"], "amplitude_max": span["amplitude_max"],
            "turned": span["turned_node_intervals"], "frozen": after["frozen"],
            "check_omega_law_float": math.acos(1 - pi * pi / (3 * GAMMA * GAMMA)),
            "check_period_law_float": 2 * math.pi / math.acos(1 - pi * pi / (3 * GAMMA * GAMMA)),
        }
        out.append(row)
        print(f"m {m} X {x} c {c} p_0 {p0} p_i {pi}: crossings {n} over {SPAN}, period {period_q} r {period_r} (law {row['check_period_law_float']:.2f}), proper sum p_0 {span['proper_sum_p0']}, proper period {proper_period_q} r {proper_period_r}, share {before['share_total']} -> {after['share_total']}, quanta {before['quanta_total']} -> {after['quanta_total']}, amp {before['amplitude']} -> {after['amplitude']} (max {span['amplitude_max']}), turned {span['turned_node_intervals']}")
    base = out[0]
    for row in out:
        m, n = row["m"], row["crossings"]
        left = row["proper_sum_p0"] * base["crossings"]
        right = base["proper_sum_p0"] * n * m
        row["redshift_predicate"] = {"left_proper_m_times_n_1": left, "right_proper_1_times_n_m_times_m": right,
                                     "difference": left - right, "one_crossing_tolerance": base["proper_sum_p0"] * m,
                                     "pass": abs(left - right) <= base["proper_sum_p0"] * m + row["proper_sum_p0"]}
        print(f"  predicate m {m}: {left} against {right}, difference {left - right}, tolerance {base['proper_sum_p0'] * m + row['proper_sum_p0']}, pass {row['redshift_predicate']['pass']}")
    return out


def ride(folder: Path, tau: int, windows: int, width: int) -> dict:
    """The wave laid at m = 1 and X raised by hand along X(t) = (Gamma (tau + t)^4) div tau^4 (the Link's length (tau + t) / tau), windows of `width` intervals: the crossings, the proper sum, the share, the count, the amplitude per window."""
    board = board_of(folder / "ride")
    lay = lay_wave(board, GAMMA)

    def x_of_t(t: int) -> int:
        return int(division_forward(GAMMA * (tau + t) ** 4, tau**4, 0)[0])

    rows = []
    for k in range(windows):
        start = k * width
        hold_frame(board, x_of_t(start))
        before = readings(board)
        span = run_span(board, x_of_t, start, width)
        mid = start + width // 2
        x = x_of_t(mid)
        c, p0, pi = paces_of(x)
        n = span["crossings"]
        row = {
            "window": k, "t_mid": mid, "m_pair": [tau + mid, tau], "X_mid": x, "c": c, "p_0": p0, "p_i": pi,
            "crossings": n, "proper_sum_p0": span["proper_sum_p0"], "share_start": before["share_total"],
            "quanta_start": before["quanta_total"], "amplitude_max": span["amplitude_max"], "turned": span["turned_node_intervals"],
            # the integer invariants: E e^U ~ n (tau + t) / (tau x proper sum); the count over m^4 ~ quanta tau^4 / (tau + t)^4
            "E_eU_scaled": list(divmod(n * (tau + mid) * 10**6, tau * span["proper_sum_p0"])) if span["proper_sum_p0"] else None,
            "E_proper_scaled": list(divmod(n * GAMMA * 10**6, span["proper_sum_p0"])) if span["proper_sum_p0"] else None,
            "quanta_over_m4_scaled": list(divmod(before["quanta_total"] * tau**4 * 1000, (tau + start) ** 4)),
            "share_over_m2_scaled": list(divmod(before["share_total"] * tau**2, (tau + start) ** 2)),
            "amplitude_over_m_scaled": list(divmod(span["amplitude_max"] * tau * 1000, tau + mid)),
        }
        rows.append(row)
        print(f"ride window {k} t_mid {mid} m {tau + mid}/{tau} X {x} p_0 {p0} p_i {pi}: crossings {n}, proper sum {span['proper_sum_p0']}, E e^U x1e6 {row['E_eU_scaled']}, E_proper x1e6 {row['E_proper_scaled']}, share {before['share_total']}, share/m^2 {row['share_over_m2_scaled'][0]}, quanta {before['quanta_total']}, quanta/m^4 x1e3 {row['quanta_over_m4_scaled'][0]}, amp {span['amplitude_max']}, amp/m x1e3 {row['amplitude_over_m_scaled'][0]}, turned {span['turned_node_intervals']}")
    return {"tau": tau, "width": width, "lay": lay, "windows": rows}


def main() -> None:
    folder = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / "v1_chain2"
    out = {"chain": [N, 1, 1], "k": "pi/2", "A": A, "universe": SMALL["integers"], "span": SPAN}
    out["fixed"] = fixed(folder)
    out["ride"] = ride(folder, 2000, 12, 400)
    (HERE / "redshift_chain.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written", HERE / "redshift_chain.json")


if __name__ == "__main__":
    sys.exit(main())
