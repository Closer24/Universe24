"""(a) The count and the closure (BRIEF_u, item (a); ALGEBRA.md, The Node: the fixed state; ENGINE.md section 2): the lines the engine holds per row on the bare 3-cube at den 1,021, read from the loader's rows and from the board's arrays (tools/node_integers.py's own functions), before the first birth and after it; each line placed under one of the owner's three shapes (the metric's 10, the potential's 4, the plane's 2) or named as an extra; what is missing of the 10 and the 4; the integers per Node the engine holds against the shape key's count. Integers only.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Three-Shapes-2/a_count_and_closure.py
"""

from __future__ import annotations

import json

from u2lib import NODE_INTEGERS, bare_board, write

from event_universe import registry
from event_universe.core.ports import AXES
from event_universe.loader.circle import circle_points
from event_universe.loader.derived import held_write_of
from event_universe.records import Record
from dataclasses import fields, replace

LEVELS = len(fields(Record))  # now, before, remainder


def rows_table(board):  # type: ignore[no-untyped-def]
    found = []
    for index, family in enumerate(board.families):
        state = board.states[index]
        rows = registry.records_of(family, state.lines)
        found.append(
            {
                "index": index,
                "name": family.name,
                "pair": list(family.pair),
                "held": family.held,
                "wronskian": family.wronskian,
                "rotation": family.rotation,
                "plane": family.plane,
                "axes": family.axes,
                "flux": family.flux,
                "motion_volume": family.motion_volume,
                "width": family.width,
                "parts": family.parts,
                "records_live": rows,
                "lines_live": len(state.lines),
                "write_remainders": len(state.write_remainders),
                "phase_lines": sum(len(r) for r in state.phases),
                "walls": [int(w) for w in board.writes[index].walls] if family.held else [],
            }
        )
    return found


def shapes_of(board):  # type: ignore[no-untyped-def]
    """Every line of every family placed: the metric's row (the volume holder: time line g_00, three axis lines the diagonal stress T_aa, a symmetric tensor's diagonal), the potential's row (the sign holder: time line A_0, three odd lines A_a), the planes (re, im per record), and the extras by name."""
    placed = {"metric_10": [], "potential_4": [], "plane_2": [], "extras": []}
    for index, family in enumerate(board.families):
        state = board.states[index]
        rows = registry.records_of(family, state.lines)
        if family.held and not family.wronskian:
            placed["metric_10"].append(("g_00 time line (the volume X)", f"{family.name} line 0"))
            for a in range(AXES):
                placed["metric_10"].append(
                    (f"g_{'xyz'[a]}{'xyz'[a]} axis line (the traceless diagonal stress)", f"{family.name} line {1 + a}")
                )
            for n in range(len(state.write_remainders)):
                placed["extras"].append(("write remainder (the line's third integer of the write)", f"{family.name} write {n}"))
        elif family.held and family.wronskian:
            for row in range(rows):
                base = row * family.width
                label = "A_0 time line" if row == 0 else f"row {row} time line (one row per record, struck by name)"
                target = "potential_4" if row == 0 else "extras"
                placed[target].append((label, f"{family.name} line {base}"))
                for a in range(AXES):
                    label = f"A_{'xyz'[a]} odd line" if row == 0 else f"row {row} odd line {'xyz'[a]}"
                    placed[target].append((label, f"{family.name} line {base + 1 + a}"))
            for n in range(len(state.write_remainders)):
                placed["extras"].append(("write remainder", f"{family.name} write {n}"))
            for row, lines in enumerate(state.phases):
                for n in range(len(lines)):
                    kind = "pair line (cos/sin per Link)" if n < 2 * AXES else ("count line" if n < 3 * AXES else "phase row Phi")
                    placed["extras"].append((f"phase {kind}, a Link's state", f"{family.name} row {row} phase {n}"))
        elif family.plane:
            for record in range(rows):
                placed["plane_2"].append((f"re of record {record}", f"{family.name} line {2 * record}"))
                placed["plane_2"].append((f"im of record {record}", f"{family.name} line {2 * record + 1}"))
        else:
            for n in range(len(state.lines)):
                placed["extras"].append(("light, one real line (a plane with im = 0, no own shape among the three)", f"{family.name} line {n}"))
    return placed


def main() -> None:
    board, patch = bare_board(intervals=8)
    try:
        start = NODE_INTEGERS.line_of(board)
        rows_start = rows_table(board)
        placed_start = shapes_of(board)
        while not board.born_at:
            board.step()
        birth = board.interval
        after = NODE_INTEGERS.line_of(board)
        rows_after = rows_table(board)
        placed_after = shapes_of(board)
        for _ in range(8 - board.interval):
            board.step()
        end = NODE_INTEGERS.line_of(board)
    finally:
        patch.undo()

    # the shape key's count for a universe of three planes, against the engine's
    volume = next(f for f in board.families if f.held and not f.wronskian)
    sign = next(f for f in board.families if f.held and f.wronskian)
    per_record = after["integers"] - start["integers"]
    born = board.born_at[birth]
    records_born = sum(board.families[i].records for i in born)
    per_record_each = per_record // records_born
    key = {
        "metric_10": {"lines": 10, "integers": 10 * LEVELS + 10},
        "potential_4": {"lines": 4, "integers": 4 * LEVELS + 4},
        "plane_2": {"lines": 2, "integers": 2 * LEVELS},
        "light_1": {"lines": 1, "integers": LEVELS},
    }
    three_planes_key = key["metric_10"]["integers"] + key["potential_4"]["integers"] + 3 * key["plane_2"]["integers"] + key["light_1"]["integers"]
    three_planes_engine = start["integers"] + 3 * per_record_each
    # the walls the loader would derive for a 10-line held row of the content (lines 1..3 the tensions, 4..9 the flux's odd lines and three more)
    ten = replace(volume, lines=10, flux=True)
    families_ten = tuple(ten if f is volume else f for f in board.families)
    walls_ten = held_write_of(families_ten, board.families.index(volume), board.world.quantum_action).walls
    points_1105 = [(list(vector), int(num), int(sine)) for vector, num, sine in circle_points(1105)]

    report = {
        "den": board.world.families[0].pair[1],
        "shape": list(board.shape),
        "interval_of_first_birth": birth,
        "born_points": [board.families[i].name for i in born],
        "records_per_born_point": records_born,
        "integers_at_start": start["integers"],
        "integers_after_birth": after["integers"],
        "integers_per_record_born": per_record_each,
        "integers_at_interval_8": end["integers"],
        "same_at_every_node": [start["same_at_every_node"], after["same_at_every_node"], end["same_at_every_node"]],
        "largest_bit_length": [start["largest_bit_length"], after["largest_bit_length"], end["largest_bit_length"]],
        "largest_at": [start["largest_at"], after["largest_at"], end["largest_at"]],
        "per_family_start": start["per_family"],
        "per_family_after": after["per_family"],
        "rows_start": rows_start,
        "rows_after": rows_after,
        "placed_start": {k: len(v) for k, v in placed_start.items()},
        "placed_after": {k: len(v) for k, v in placed_after.items()},
        "placed_after_list": placed_after,
        "metric_missing_lines": {
            "g_0a vector lines (T_1u; the flux holder's odd lines V_a, FamilyRule.flux False on every row)": AXES,
            "g_ab shear lines a != b (T_2g; the former `shear` word, no row of the family-less loader)": AXES,
            "held": 1 + AXES,
            "total_of_the_10": 10,
        },
        "potential_missing_lines": {"held": 1 + AXES, "total_of_the_4": 4},
        "shape_key_integers": key,
        "three_planes_integers_shape_key": three_planes_key,
        "three_planes_integers_engine": three_planes_engine,
        "volume_walls_engine": [int(w) for w in board.writes[board.families.index(volume)].walls],
        "sign_walls_engine_one_row": [int(w) for w in board.writes[board.families.index(sign)].walls[: sign.width]],
        "walls_loader_would_derive_for_a_10_line_content_row": [int(w) for w in walls_ten],
        "den_1105_circle_points_open_quadrant": points_1105,
    }
    write("a_count_and_closure.json", json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
