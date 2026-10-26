"""(b) The 48 on the three shapes (BRIEF_u, item (b); ALGEBRA.md, The cube's symmetry): on the engine's own hole seed (the bare 3-cube at den 1,021, the volume holder gapped) stepped through its births, the count per interval of the 48 elements under which the board's image equals the image's board bit for bit (tests/test_the_board_is_the_cube_48.py's `carried` and `apart`); the induced signed permutation of every line under every element, read by carrying a label board (each line one constant), so that each object's lines are shown to go among themselves (no mixing, no line outside), the volume's axis lines permuted with no sign (a symmetric tensor's diagonal, A_1g + E_g), the sign's odd lines permuted with the axis's sign (a vector, T_1u), the time lines and the plane's two lines fixed (scalars); the characters' sums over the 48 as integers (the count of the trivial representation in each object, SUM chi over 48); and the negative control, the plane's senses exchanged with the image (im -> -im), counted under the 42 negating elements. Integers only.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Three-Shapes-2/b_the_48.py
"""

from __future__ import annotations

import json
from dataclasses import replace

import numpy as np

from u2lib import CUBE48, bare_board, write

from event_universe import records, registry
from event_universe.core.ports import AXES

IDENTITY = CUBE48.IDENTITY


def label_board(board):  # type: ignore[no-untyped-def]
    """Every line of every family at one distinct positive constant over the board (now = before = label, the remainder 0), the write remainders and phase lines at their own labels: a board whose carry reads as a signed permutation of the labels."""
    label = 0
    names = {}
    states = []
    for index, state in enumerate(board.states):
        lines = []
        for n, line in enumerate(state.lines):
            label += 1
            names[label] = (index, "line", n)
            lines.append(
                records.Record(
                    np.full(board.shape, label, dtype=object),
                    np.full(board.shape, label, dtype=object),
                    np.full(board.shape, 0, dtype=object),
                )
            )
        writes = []
        for n, _w in enumerate(state.write_remainders):
            label += 1
            names[label] = (index, "write", n)
            writes.append(np.full(board.shape, label, dtype=object))
        phases = []
        for row, lines_row in enumerate(state.phases):
            found = []
            for n, _line in enumerate(lines_row):
                label += 1
                names[label] = (index, "phase", row, n)
                found.append(
                    records.Record(
                        np.full(board.shape, label, dtype=object),
                        np.full(board.shape, label, dtype=object),
                        np.full(board.shape, 0, dtype=object),
                    )
                )
            phases.append(found)
        states.append(records.NodeState(lines, writes, phases))
    return states, names


def induced(board, m, names):  # type: ignore[no-untyped-def]
    """The signed permutation of the line labels one element induces on the level arrays: per output line (family, kind, index) the input label it holds and its sign, read at the origin."""
    carried = CUBE48.carried(board, m, None)
    found = {}
    for index, (lines, writes, phases) in enumerate(carried):
        for n, line in enumerate(lines):
            value = int(np.asarray(line[0], dtype=object)[0, 0, 0])
            found[(index, "line", n)] = (names[abs(value)], 1 if value > 0 else -1)
        for n, w in enumerate(writes):
            value = int(np.asarray(w, dtype=object)[0, 0, 0])
            found[(index, "write", n)] = (names[abs(value)] if abs(value) in names else None, 1 if value > 0 else -1)
    return found


def main() -> None:
    lines_out: list = []
    board, patch = bare_board(intervals=8, lines=lines_out)
    try:
        group = CUBE48.cube_48()
        non_trivial = [m for m in group if not np.array_equal(m, IDENTITY)]
        negating = CUBE48.negating()
        turns = CUBE48.turns_of(board, None)
        per_interval = []
        control = []
        for _ in range(8):
            board.step()
            turns = CUBE48.turns_of(board, turns)
            state = CUBE48.carried(board, IDENTITY)
            held = sum(1 for m in non_trivial if not CUBE48.apart(CUBE48.carried(board, m, turns), state)) + 1
            births = CUBE48.births_at(lines_out, board.interval)
            # the negative control: the plane's senses exchanged with the image (im -> -im on every plane record)
            exchanged = 0
            for m in negating:
                image = CUBE48.carried(board, m, turns)
                swapped = []
                for index, (lines, writes, phases) in enumerate(image):
                    family = board.families[index]
                    if family.plane and not family.held:
                        lines = [
                            (-np.asarray(t[0], dtype=object), -np.asarray(t[1], dtype=object), t[2]) if n % 2 == 1 else t
                            for n, t in enumerate(lines)
                        ]
                    swapped.append((lines, writes, phases))
                if not CUBE48.apart(swapped, state):
                    exchanged += 1
            planes_live = sum(
                registry.records_of(f, board.states[i].lines) for i, f in enumerate(board.families) if f.plane and not f.held
            )
            per_interval.append({"interval": board.interval, "held_of_48": held, "births": len(births), "plane_records_live": planes_live})
            control.append({"interval": board.interval, "senses_exchanged_held_of_42": exchanged})
        # the induced permutations on the lines, read from a label board (every element)
        real_states = board.states
        states, names = label_board(board)
        board.states = states
        try:
            mixing = 0
            axis_no_sign = 0
            odd_with_sign = 0
            scalars_fixed = 0
            per_element = []
            volume = board.families.index(next(f for f in board.families if f.held and not f.wronskian))
            sign = board.families.index(next(f for f in board.families if f.held and f.wronskian))
            for m in group:
                pi, s = CUBE48.axis_map(m)
                table = induced(board, m, names)
                mixed = sum(1 for key, (source, _sg) in table.items() if source is not None and source[0] != key[0])
                mixing += mixed > 0
                ok_axis = all(
                    table[(volume, "line", 1 + pi[a])] == ((volume, "line", 1 + a), 1) for a in range(AXES)
                )
                axis_no_sign += ok_axis
                rows = registry.records_of(board.families[sign], real_states[sign].lines)
                ok_odd = all(
                    table[(sign, "line", row * board.families[sign].width + 1 + pi[a])]
                    == ((sign, "line", row * board.families[sign].width + 1 + a), s[a])
                    for row in range(rows)
                    for a in range(AXES)
                )
                odd_with_sign += ok_odd
                ok_scalars = table[(volume, "line", 0)] == ((volume, "line", 0), 1) and all(
                    table[(i, "line", n)] == ((i, "line", n), 1)
                    for i, f in enumerate(board.families)
                    if not f.held
                    for n in range(len(real_states[i].lines))
                )
                scalars_fixed += ok_scalars
                per_element.append(
                    {"pi": pi, "s": s, "mixed": mixed, "axis_lines_permuted_no_sign": ok_axis, "odd_lines_permuted_with_sign": ok_odd, "scalars_fixed": ok_scalars}
                )
        finally:
            board.states = real_states
        # the characters' sums over the 48 (the count of the trivial representation times 48)
        chi_time = 0
        chi_diag = 0
        chi_vector = 0
        chi_shear = 0
        chi_plane = 0
        det_sum = 0
        for m in group:
            pi, s = CUBE48.axis_map(m)
            fixed = [a for a in range(AXES) if pi[a] == a]
            chi_time += 1
            chi_diag += len(fixed)
            chi_vector += sum(s[a] for a in fixed)
            # the three shears xy, yz, zx: the pair {a, b} fixed iff pi maps it to itself; the sign s_a s_b
            for a in range(AXES):
                for b in range(a + 1, AXES):
                    if {pi[a], pi[b]} == {a, b}:
                        chi_shear += s[a] * s[b]  # the shear line ab carried to itself with the sign s_a s_b
            chi_plane += 2
            det_sum += int(round(float(np.linalg.det(m))))
        report = {
            "den": board.world.families[0].pair[1],
            "group_order": len(group),
            "negating_elements": len(negating),
            "per_interval": per_interval,
            "negative_control_senses_exchanged": control,
            "elements_with_mixing_between_families": mixing,
            "elements_axis_lines_permuted_with_no_sign_of_48": axis_no_sign,
            "elements_odd_lines_permuted_with_the_axis_sign_of_48": odd_with_sign,
            "elements_time_lines_and_plane_lines_fixed_of_48": scalars_fixed,
            "character_sums_over_48": {
                "time_line_scalar_A1g": chi_time,
                "three_axis_lines_diagonal_permuted": chi_diag,
                "three_odd_lines_vector": chi_vector,
                "three_shears_xy_yz_zx": chi_shear,
                "plane_two_scalars": chi_plane,
                "determinant_sum": det_sum,
            },
            "trivial_copies": {
                "time_line": chi_time // 48,
                "three_axis_lines": chi_diag // 48,
                "three_odd_lines": chi_vector // 48,
                "three_shears": chi_shear // 48,
                "plane": chi_plane // 48,
                "metric_10_as_1_plus_3_plus_6": (chi_time + chi_vector + chi_diag + chi_shear) // 48,
                "potential_4_as_1_plus_3": (chi_time + chi_vector) // 48,
            },
            "per_element": per_element,
        }
        write("b_the_48.json", json.dumps(report, indent=1))
    finally:
        patch.undo()


if __name__ == "__main__":
    main()
