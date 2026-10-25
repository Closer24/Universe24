"""(Addition 4) The laws shown with a number on the fed board the three shapes stand on: the engine's own hole seed on the bare 3-cube at den 1,021 (the volume holder gapped), 8 intervals forward through the first birth and 8 back (the run back MATCH per interval, every array of every state compared bit for bit); on the board per interval the charge (SUM of every plane record's Wronskian over the Nodes, the potential's source), the lattice momentum per axis of the light's line and of every plane (readings.momentum_of), the form's board sum of the light's line (records.form over the step); in the clicks alone the births' senses summed, the exact take (taken against walls + excess) and the credit lines' count; the integers one Node holds and the largest bit length. Integers only.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Three-Shapes-2/e_run_back_and_conservations.py
"""

from __future__ import annotations

import json

import numpy as np

from u2lib import NODE_INTEGERS, bare_board, write

from event_universe import readings, records, registry
from event_universe.core.ports import AXES
from event_universe.loader.derived import turns


def snapshot(board):  # type: ignore[no-untyped-def]
    found = []
    for state in board.states:
        lines = [tuple(np.asarray(a, dtype=object).copy() for a in (li.now, li.before, li.remainder)) for li in state.lines]
        writes = [np.asarray(w, dtype=object).copy() for w in state.write_remainders]
        phases = [
            [tuple(np.asarray(a, dtype=object).copy() for a in (li.now, li.before, li.remainder)) for li in row]
            for row in state.phases
        ]
        found.append((lines, writes, phases))
    return found


def same(a, b) -> bool:  # type: ignore[no-untyped-def]
    if isinstance(a, list | tuple):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b, strict=True))
    return bool(np.array_equal(np.asarray(a, dtype=object), np.asarray(b, dtype=object)))


def board_readings(board):  # type: ignore[no-untyped-def]
    charge = 0
    momentum = {}
    for index, family in enumerate(board.families):
        if family.held:
            continue
        for record in range(registry.records_of(family, board.states[index].lines)):
            lines = board.lines_of(index, record)
            if family.plane:
                charge += int(np.asarray(records.wronskian(lines, True), dtype=object).sum())
            momentum[f"{family.name} record {record}"] = list(readings.momentum_of(family.pair[0], lines))
    return charge, momentum


def main() -> None:
    lines_out: list = []
    board, patch = bare_board(intervals=8, lines=lines_out)
    try:
        history = [snapshot(board)]
        on_board = []
        for _ in range(8):
            board.step()
            charge, momentum = board_readings(board)
            on_board.append({"interval": board.interval, "charge_sum_W": charge, "momentum": momentum, "turned_nodes": int(board.turned.sum())})
            history.append(snapshot(board))
        end = NODE_INTEGERS.line_of(board)
        matches = 0
        for k in range(8, 0, -1):
            board.step_inverse()
            matches += same(snapshot(board), history[k - 1])
        births = [li for li in lines_out if li.get("event") == "birth"]
        credits = [li for li in lines_out if li.get("event") == "credit"]
        refused = [li for li in lines_out if li.get("event") == "refused"]
        senses_sum = sum(sum(li["senses"]) for li in births)
        exact_take = sum(1 for li in births if li["taken"] == li["walls"] + li["excess"])
        report = {
            "den": board.world.families[0].pair[1],
            "intervals_forward": 8,
            "run_back_match_of_8": matches,
            "interval_after_run_back": board.interval,
            "on_board": on_board,
            "clicks": {
                "birth_lines": len(births),
                "credit_lines": len(credits),
                "refused_lines": len(refused),
                "senses_summed_over_births": senses_sum,
                "births_with_taken_equal_walls_plus_excess": exact_take,
                "taken_walls_excess_step_per_birth": [(li["taken"], li["walls"], li["excess"], li["step"]) for li in births],
                "credit_momentum": [li.get("momentum") for li in credits],
                "credit_beat_proper": [(li.get("beat"), li.get("proper")) for li in credits],
            },
            "integers_per_node_at_8": end["integers"],
            "largest_bit_length_at_8": end["largest_bit_length"],
            "largest_at": end["largest_at"],
            "same_at_every_node": end["same_at_every_node"],
        }
        write("e_run_back_and_conservations.json", json.dumps(report, indent=1, default=str))
    finally:
        patch.undo()


if __name__ == "__main__":
    main()
