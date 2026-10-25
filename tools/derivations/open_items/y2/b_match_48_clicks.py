"""(c), (e) The run back and the 48 with the six lines written and read (BRIEF_y (c), (e)): under U24_METRIC=1 the hole seed on the bare 3-cube at den 1,021, 8 intervals forward through the first birth and the turns and 8 back, every array compared bit for bit (MATCH per interval); per interval the elements of the 48 under which the board's image equals the image's board with the ten lines carried as one object (y2lib.carried_ten), and the two negative controls (the flux lines carried with no sign; the shears carried with no sign); the flux and shear lines' sums over the board (0 for the odd ones on the symmetric seed) and their nonzero Nodes; in the clicks the births' senses summed, the exact take and the credits' momentum; the integers per Node and the largest bit length. Integers only.

Run: U24_METRIC=1 PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/y2/b_match_48_clicks.py
"""

from __future__ import annotations

import json

import numpy as np

from y2lib import CUBE48, NODE_INTEGERS, bare_board, carried_ten, same, snapshot, write

from event_universe import records, registry
from event_universe.core.ports import AXES
from event_universe.loader.derived import METRIC

IDENTITY = CUBE48.IDENTITY
INTERVALS = 8


def main() -> None:
    assert METRIC, "run with U24_METRIC=1"
    lines_out: list = []
    board = bare_board(intervals=INTERVALS, lines=lines_out)
    volume = board.held[0]
    group = CUBE48.cube_48()
    non_trivial = [m for m in group if not np.array_equal(m, IDENTITY)]
    negating = CUBE48.negating()
    turns = CUBE48.turns_of(board, None)
    history = [snapshot(board)]
    per_interval = []
    for _ in range(INTERVALS):
        board.step()
        turns = CUBE48.turns_of(board, turns)
        state = carried_ten(board, IDENTITY, turns)
        held = 1 + sum(1 for m in non_trivial if not CUBE48.apart(carried_ten(board, m, turns), state))
        test_carry = 1 + sum(1 for m in non_trivial if not CUBE48.apart(CUBE48.carried(board, m, turns), state))
        no_sign_flux = sum(1 for m in negating if not CUBE48.apart(carried_ten(board, m, turns, "flux"), state))
        no_sign_shear = sum(1 for m in negating if not CUBE48.apart(carried_ten(board, m, turns, "shear"), state))
        st = board.states[volume]
        flux_sums = [int(np.asarray(st.lines[1 + AXES + a].now, dtype=object).sum()) for a in range(AXES)]
        flux_nonzero = [int((np.asarray(st.lines[1 + AXES + a].now, dtype=object) != 0).sum()) for a in range(AXES)]
        shear_sums = [int(np.asarray(st.lines[1 + 2 * AXES + k].now, dtype=object).sum()) for k in range(AXES)]
        shear_nonzero = [int((np.asarray(st.lines[1 + 2 * AXES + k].now, dtype=object) != 0).sum()) for k in range(AXES)]
        tension_nonzero = [int((np.asarray(st.lines[1 + a].now, dtype=object) != 0).sum()) for a in range(AXES)]
        charge = 0
        for index, family in enumerate(board.families):
            if family.plane and not family.held:
                for record in range(registry.records_of(family, board.states[index].lines)):
                    charge += int(np.asarray(records.wronskian(board.lines_of(index, record), True), dtype=object).sum())
        per_interval.append(
            {
                "interval": board.interval,
                "held_of_48_ten_as_one_object": held,
                "held_of_48_tests_own_carry_no_sign_on_the_six": test_carry,
                "control_flux_no_sign_held_of_42": no_sign_flux,
                "control_shear_no_sign_held_of_42": no_sign_shear,
                "turned_nodes": int(board.turned.sum()),
                "flux_lines_board_sums": flux_sums,
                "flux_lines_nonzero_nodes": flux_nonzero,
                "shear_lines_board_sums": shear_sums,
                "shear_lines_nonzero_nodes": shear_nonzero,
                "tension_lines_nonzero_nodes": tension_nonzero,
                "charge_sum_W": charge,
            }
        )
        history.append(snapshot(board))
    end = NODE_INTEGERS.line_of(board)
    matches = 0
    for k in range(INTERVALS, 0, -1):
        board.step_inverse()
        matches += same(snapshot(board), history[k - 1])
    births = [li for li in lines_out if li.get("event") == "birth"]
    credits = [li for li in lines_out if li.get("event") == "credit"]
    refused = [li for li in lines_out if li.get("event") == "refused"]
    report = {
        "den": board.world.families[0].pair[1],
        "intervals_forward": INTERVALS,
        "run_back_match_of_8": matches,
        "interval_after_run_back": board.interval,
        "per_interval": per_interval,
        "clicks": {
            "birth_lines": len(births),
            "credit_lines": len(credits),
            "refused_lines": len(refused),
            "senses_summed_over_births": sum(sum(li["senses"]) for li in births),
            "births_with_taken_equal_walls_plus_excess": sum(1 for li in births if li["taken"] == li["walls"] + li["excess"]),
            "taken_walls_excess_step_per_birth": [(li["taken"], li["walls"], li["excess"], li["step"]) for li in births],
            "credit_momentum": [li.get("momentum") for li in credits],
            "credit_beat_proper": [(li.get("beat"), li.get("proper")) for li in credits],
        },
        "integers_per_node_at_8": end["integers"],
        "largest_bit_length_at_8": [end["largest_bit_length"], end["largest_at"]],
        "same_at_every_node": end["same_at_every_node"],
    }
    write("b_match_48_clicks.json", json.dumps(report, indent=1, default=str))


if __name__ == "__main__":
    main()
