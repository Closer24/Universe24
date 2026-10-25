"""(a) The write of the six lines and the count (BRIEF_y (a), (d) the count): under U24_METRIC=1 on the bare 3-cube at den 1,021, the loader's rows (the volume row's ten lines, its ten walls), the integers one Node holds and the largest bit length at the start, after the first birth and at the interval 8; the write's numerators of the nine axis lines at every Node after the first birth compared with the by-hand bilinears (the traceless stresses, the fluxes F_(i,i-a) - F_(i,i+a), the products D_a D_b) scaled by the same `scaled_sum` at the row's own paces: the one function with the part as the input; the board sums of the written flux lines' sources against num times the lattice momentum (the identity). Integers only.

Run: U24_METRIC=1 PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Six-Metric-Lines-2/a_write_and_count.py
"""

from __future__ import annotations

import json

import numpy as np

from y2lib import NODE_INTEGERS, PAIRS, bare_board, rows_table, write

from event_universe import board_readings, readings, records, registry
from event_universe.core import paces
from event_universe.core.ports import AXES, arrival
from event_universe.loader.derived import METRIC


def main() -> None:
    assert METRIC, "run with U24_METRIC=1"
    lines_out: list = []
    board = bare_board(intervals=8, lines=lines_out)
    start = NODE_INTEGERS.line_of(board)
    rows = rows_table(board)
    while not board.born_at:
        board.step()
    birth = board.interval
    after = NODE_INTEGERS.line_of(board)
    # the write's numerators on the board at this interval (the sources the next interval's write takes)
    held = board.held[0]
    rulers, stresses = board.rulers(1), board_readings.stresses(board)
    sourcing = registry.sourcing(board.families, board.states, held)
    numerators, walls, _ = records.write_sources(
        held, board.families, {}, stresses, board.writes[held], rulers, board.world.node_clock, sourcing, None, 1, board.fixed_walls[held]
    )
    # by hand: each axis line's numerator from its own bilinear through the same scaled_sum
    family = board.families[held]
    checks = {}
    gamma = board.world.node_clock
    by_hand_readings = {}
    for source in sourcing[0]:
        lines = board.lines_of(*source)
        num = board.families[source[0]].pair[0]
        tens = []
        flux = []
        shear = []
        for a in range(AXES):
            t = 0
            f = 0
            for line in lines:
                d = arrival(line.now, a, 1) - arrival(line.now, a, -1)
                t = t + num * d * d
                here_now, here_before = line.now, line.before
                f_minus = num * (here_now * arrival(line.before, a, -1) - here_before * arrival(line.now, a, -1))
                f_plus = num * (here_now * arrival(line.before, a, 1) - here_before * arrival(line.now, a, 1))
                f = f + (f_minus - f_plus)
            tens.append(np.asarray(t, dtype=object))
            flux.append(np.asarray(f, dtype=object))
        for a, b in PAIRS:
            p = 0
            for line in lines:
                da = arrival(line.now, a, 1) - arrival(line.now, a, -1)
                db = arrival(line.now, b, 1) - arrival(line.now, b, -1)
                p = p + num * da * db
            shear.append(np.asarray(p, dtype=object))
        by_hand_readings[source] = (*tens, *flux, *shear)
    engine_equal = {}
    for source in sourcing[0]:
        engine_equal[str(source)] = [
            bool(np.array_equal(np.asarray(stresses[source][k], dtype=object), by_hand_readings[source][k])) for k in range(AXES * AXES)
        ]
    # the numerators of positions 3..8 by the engine's scaled_sum on the by-hand readings (no projection)
    positions_equal = {}
    for position in range(AXES, AXES * AXES):
        axes = {s: by_hand_readings[s][position] for s in sourcing[0]}
        total, scale, _ = records.scaled_sum(held, board.families, axes, rulers, gamma, paces.COUNT_POWER, board.writes[held].factors, 1, 0)
        total = family.write * total
        fixed = board.fixed_walls[held][1 + position]
        wall = walls[1 + position]
        # the engine's own fixed-wall ratio rounding, as write_sources takes it
        expected = paces.odd_rounded(records.exact(total) * records.exact(fixed), records.exact(np.asarray(scale) * np.asarray(board.writes[held].walls[1 + position], dtype=object)))
        positions_equal[1 + position] = bool(np.array_equal(np.asarray(numerators[1 + position], dtype=object), np.asarray(expected, dtype=object)))
    # the identity: the flux line's source summed over the board is num x the lattice momentum, per source
    momentum_identity = {}
    for source in sourcing[0]:
        num = board.families[source[0]].pair[0]
        lines = board.lines_of(*source)
        p = readings.momentum_of(num, lines)
        sums = [int(np.asarray(stresses[source][AXES + a], dtype=object).sum()) for a in range(AXES)]
        momentum_identity[str(source)] = {"flux_source_board_sum": sums, "num_times_P": [int(num * x) for x in p], "equal": sums == [int(num * x) for x in p]}
    for _ in range(8 - board.interval):
        board.step()
    end = NODE_INTEGERS.line_of(board)
    report = {
        "den": board.world.families[0].pair[1],
        "rows": rows,
        "volume_row_lines": board.families[held].width,
        "volume_row_walls": [int(w) for w in board.writes[held].walls],
        "volume_row_fixed_walls_bits": [int(np.asarray(w, dtype=object).reshape(-1)[0]).bit_length() for w in board.fixed_walls[held]],
        "write_walls_now_bits": [int(np.asarray(w, dtype=object).reshape(-1).max()).bit_length() for w in walls],
        "integers_per_node": {"start": start["integers"], f"after_birth_at_{birth}": after["integers"], "at_8": end["integers"]},
        "per_family_start": start["per_family"],
        "same_at_every_node": [start["same_at_every_node"], after["same_at_every_node"], end["same_at_every_node"]],
        "largest_bit_length": {"start": [start["largest_bit_length"], start["largest_at"]], "after_birth": [after["largest_bit_length"], after["largest_at"]], "at_8": [end["largest_bit_length"], end["largest_at"]]},
        "derived_width_bits": start["width_bits"],
        "amplitude_bound": int(board.world.amplitude_bound),
        "readings_engine_equal_by_hand_per_source_9": engine_equal,
        "numerators_positions_4_to_9_equal_scaled_sum_of_by_hand_part": positions_equal,
        "flux_source_sum_is_num_times_lattice_momentum": momentum_identity,
        "numerators_nonzero_nodes_per_line_after_birth": [int((np.asarray(n, dtype=object) != 0).sum()) for n in numerators],
        "births": [li for li in lines_out if li.get("event") == "birth"][:2],
    }
    write("a_write_and_count.json", json.dumps(report, indent=1, default=str))


if __name__ == "__main__":
    main()
