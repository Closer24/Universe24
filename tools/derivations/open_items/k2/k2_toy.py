"""Hand K2, the toy measurements (BRIEF_k (d)): the bare 3-cube torus of tests/laws_universe.bare_torus at a den
and (Gamma, T) given on the command line, G the engine's: the derived width, the amplitude bound A, the state's
largest bit length over the run (tools/node_integers.largest_bits), Rule3's total's bits at A (the constant-3
test's form), the forward run of N intervals and the run back by the engine's own inverse (MATCH count =
intervals), the births; and the exact bands' closure on core/rule3.rule3 at the vacuum's paces with uniform
arrivals (the periods 4 at [0, den], 6 at [den/2, den] and 3 at [-den/2, den] where den is even), at G 16
and at G 1 and at the given Gamma, remainders 0 throughout. Integers only.

Run: PYTHONPATH=<worktree>/src python tools/derivations/k2/k2_toy.py DEN GAMMA T INTERVALS CUBE
"""

from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

from event_universe import world_files
from event_universe.core import paces, rule3
from event_universe.core.ports import LINK_UNIT
from event_universe.lattice import Lattice
from event_universe.world_files import load_world

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from tests import laws_universe  # noqa: E402
from tests.laws import ROOT, board_state, load_file, same_state  # noqa: E402

TOOL = load_file("node_integers", ROOT / "tools" / "node_integers.py")


def exact_band_period(num: int, den: int, gamma: int, unit: int) -> tuple[int, int]:
    """The first return of (now, before, remainder) from (1000, 0, 0) under rule3 with uniform arrivals (flux 0), and the largest remainder seen."""
    clock, pace = paces.node_paces(gamma, 0)
    rule = rule3.rule_integers(num, den, gamma, clock, pace, None, unit)
    start = (1000, 0, 0)
    now, before, r = start
    largest_r = 0
    for k in range(1, 100):
        nxt, r = rule3.rule3(0, rule.mass, rule.wall, now, before, r)
        now, before = int(nxt), now
        r = int(r)
        largest_r = max(largest_r, r)
        if (now, before, r) == start:
            return k, largest_r
    return 0, largest_r


def main() -> None:
    den, gamma, action, intervals, cube = (int(a) for a in sys.argv[1:6])
    out: dict[str, object] = {"den": den, "Gamma": gamma, "T": action, "G": LINK_UNIT, "cube": cube}
    t0 = time.time()
    folder = Path(tempfile.mkdtemp(prefix="k2toy_"))
    world_files.REPOSITORY_ROOT = folder
    laws_universe.SMALL["integers"] = {"den": den, "node_clock": gamma, "quantum_action": action}
    world = load_world(laws_universe.bare_torus(folder, cube, intervals))
    out["load_seconds"] = int(time.time() - t0)
    out["width_bits"] = world.width.bit_length()
    out["A"] = world.amplitude_bound
    out["A_bits"] = world.amplitude_bound.bit_length()
    out["rows"] = len(world.families)
    out["kind"] = world.kind.__name__
    light = world.seed
    num0, den0 = world.families[light].pair
    totals = []
    for content in (0, paces.frozen_content(gamma) - 1, -gamma):
        clock, pace = paces.node_paces(gamma, content)
        rule = rule3.rule_integers(num0, den0, gamma, clock, pace, None, LINK_UNIT)
        total = rule3.flux_total(
            sum(r * (-2 * world.amplitude_bound) for r in rule.reaches),
            rule.mass,
            rule.wall,
            world.amplitude_bound,
            -world.amplitude_bound,
        )
        totals.append((abs(int(total)) + int(rule.wall)).bit_length())
    out["rule3_total_bits_at_A_(vac,frozen-1,-Gamma)"] = totals
    out["wall_bits"] = int(rule3.wall_of(den, gamma, LINK_UNIT)).bit_length()
    lines: list[dict] = []
    board = Lattice(world, output=lines.append)
    states = [board_state(board)]
    largest = TOOL.largest_bits(board)[0]
    count = TOOL.total_of(board)
    for _ in range(intervals):
        board.step()
        states.append(board_state(board))
        largest = max(largest, TOOL.largest_bits(board)[0])
    out["state_largest_bits_over_run"] = largest
    out["integers_per_node_at_start"] = count
    out["integers_per_node_at_end"] = TOOL.total_of(board)
    out["same_count_at_every_node"] = TOOL.same_shape(board)
    out["births"] = {str(k): v for k, v in board.born_at.items()}
    out["credits"] = sum(1 for li in lines if li.get("event") == "credit")
    out["births_lines"] = sum(1 for li in lines if li.get("event") == "birth")
    during: list[dict] = []
    board.output = during.append
    back = 0
    for k in range(intervals):
        board.step_inverse()
        back += same_state(board_state(board), states[intervals - 1 - k])
    out["run_back_MATCH_intervals"] = back
    out["run_back_lines_during"] = len(during)
    out["interval_after_back"] = board.interval
    out["run_seconds"] = int(time.time() - t0)
    bands = {}
    for g in (LINK_UNIT, 1):
        row = {"period_0_over_den": exact_band_period(0, den, gamma, g)}
        if den % 2 == 0:
            row["period_half"] = exact_band_period(den // 2, den, gamma, g)
            row["period_minus_half"] = exact_band_period(-(den // 2), den, gamma, g)
        else:
            row["period_half_at_2den"] = exact_band_period(den, 2 * den, gamma, g)
            row["period_minus_half_at_2den"] = exact_band_period(-den, 2 * den, gamma, g)
        bands[f"G_{g}"] = row
    out["exact_bands"] = bands
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
