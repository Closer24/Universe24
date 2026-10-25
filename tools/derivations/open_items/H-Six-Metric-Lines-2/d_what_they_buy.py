"""(d) What the six lines buy, measured under U24_METRIC=1 on the bare 3-cube at den 1,021 (BRIEF_y (d)): (1) the flux lines' read: the volume row's g_0x set by hand to V at every Node (the fold's tangent within the guard, 6 K (2 V) <= Gamma^2), every point born and a plane record of the lift (779, 1021) laid at the centre and its neighbours, the light line at the hole seed's drift with one quantum more at the centre; one interval stepped from the same state with V = 0 and with V, the arrays compared: the massless line's output the same bit for bit (0 Nodes differ: light is not dragged, the law's prediction, K = 0 at the massless pair) and the plane's output differing (the Nodes that differ, the turn's reading: the plane's point pair 2 cos Omega at the centre with V = 0 and with V, and the sign holder's Link pair's odd part X^s at the centre's +x Link, 0 without and the fold's integer with), K the rotation to the unit by `plane.rotation_unit`; (2) the shears' write: one quantum of light at (1, 1, 1) alone against two quanta at (1, 1, 1) and (2, 2, 1): the g_xy source D_x D_y at the Node (2, 1, 1) and the g_xx source there, read by `readings.axis_sources_of`; (3) the lattice momentum in the flux lines: light laid as a travelling wave along x (the drift at now, the drift shifted one Link at before), the flux source's board sum against num x P_x (`readings.momentum_of`) exactly, and after one interval the written g_0x levels' board change against the same, to the remainders. Integers only.

Run: U24_METRIC=1 PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Six-Metric-Lines-2/d_what_they_buy.py
"""

from __future__ import annotations

import json

import numpy as np

from y2lib import bare_board, snapshot, write

from event_universe import flux, node, readings, records, registry, seed
from event_universe.core.ports import AXES
from event_universe.loader.derived import METRIC
from event_universe.plane import rotation_unit
from event_universe.reports import point_of

CENTRE = (1, 1, 1)


def differing(a, b) -> int:  # type: ignore[no-untyped-def]
    """The Nodes at which two arrays differ."""
    return int((np.asarray(a, dtype=object) != np.asarray(b, dtype=object)).sum())


def set_line(board, index, number, now, before=None):  # type: ignore[no-untyped-def]
    state = board.states[index]
    line = state.lines[number]
    now_a = np.asarray(now, dtype=board.kind)
    before_a = line.before if before is None else np.asarray(before, dtype=board.kind)
    state.lines[number] = records.Record(now_a, before_a, line.remainder)


def one_interval_from(board, flux_value: int):  # type: ignore[no-untyped-def]
    """The board's volume row's g_0x set to `flux_value` at every Node (both levels), one interval stepped (the acts before the close), the state after."""
    held = board.held[0]
    level = np.full(board.shape, flux_value, dtype=object)
    set_line(board, held, 1 + AXES, level, level.copy())
    board.advanced_to_the_close()
    return snapshot(board)


def prepared(lines_out):  # type: ignore[no-untyped-def]
    """A board with every point born, the lift's record laid at the centre and its six neighbours (the re line at 400, the im at 300, the before at 380 and 320), light at the drift plus one quantum at the centre."""
    board = bare_board(intervals=8, lines=lines_out)
    for index in board.turning:
        board.born_point(index)
    lift = max(board.turning)
    span = records.record_slice(board.families[lift], 0)
    mask = np.zeros(board.shape, dtype=bool)
    mask[CENTRE] = True
    for a in range(AXES):
        for side in (1, -1):
            there = tuple((CENTRE[i] + side) % board.shape[i] if i == a else CENTRE[i] for i in range(AXES))
            mask[there] = True
    re_now, im_now = np.where(mask, 400, 0), np.where(mask, 300, 0)
    re_before, im_before = np.where(mask, 380, 0), np.where(mask, 320, 0)
    set_line(board, lift, span.start, re_now, re_before)
    set_line(board, lift, span.start + 1, im_now, im_before)
    light = board.world.seed
    drift = seed.drift_of(board.world.quantum_action)
    now = np.full(board.shape, drift, dtype=object)
    now[CENTRE] = 2 * drift
    set_line(board, light, 0, now, now.copy())
    return board, lift, span


def main() -> None:
    assert METRIC, "run with U24_METRIC=1"
    gamma = 1000
    report: dict = {}
    # (1) the flux lines' read
    lift_pair = (779, 1021)
    k_lift, k_light = rotation_unit(lift_pair, gamma), rotation_unit((1021, 1021), gamma)
    v = 50
    report["rotation_unit_K"] = {"lift_779_1021": k_lift, "massless_1021_1021": k_light, "guard_6K_2V_le_Gamma2": 6 * k_lift * 2 * v <= gamma * gamma, "V": v}
    outcomes = {}
    boards = {}
    for value in (0, v):
        lines_out: list = []
        board, lift, span = prepared(lines_out)
        before_step = snapshot(board)
        # the plane's Link pairs at the centre (+x Port) before the step, the odd part read by the fold
        content, factors = board.read(lift, 1, 0)
        held = board.held[0]
        level = np.full(board.shape, value, dtype=object)
        set_line(board, held, 1 + AXES, level, level.copy())
        pairs = flux.pairs_of(lift, board.families, board.states, 1, gamma, content, factors, 0, board.amplitude)
        odd_plus_x = int(np.asarray(pairs[1][0], dtype=object)[CENTRE]) if pairs is not None else None
        even_plus_x = int(np.asarray(pairs[0][0], dtype=object)[CENTRE]) if pairs is not None else None
        after = one_interval_from(board, value)
        outcomes[value] = (before_step, after, span, lift, odd_plus_x, even_plus_x, int(board.turned.sum()))
        boards[value] = board
    (b0, a0, span, lift, odd0, even0, t0), (b1, a1, _s, _l, odd1, even1, t1) = outcomes[0], outcomes[v]
    light = boards[0].world.seed
    sign = boards[0].held[1]
    light_diff = [differing(a0[light][0][0][p], a1[light][0][0][p]) for p in range(3)]
    plane_diff = [[differing(a0[lift][0][n][p], a1[lift][0][n][p]) for p in range(3)] for n in range(span.start, span.stop)]
    sign_diff = sum(differing(a0[sign][0][n][p], a1[sign][0][n][p]) for n in range(len(a0[sign][0])) for p in range(3))
    volume_diff = [sum(differing(a0[0][0][n][p], a1[0][0][n][p]) for p in range(3)) for n in range(10)]
    points = {}
    for value, (b, a, *_rest) in ((0, outcomes[0]), (v, outcomes[v])):
        re_b, re_a = b[lift][0][span.start], a[lift][0][span.start]
        im_b, im_a = b[lift][0][span.start + 1], a[lift][0][span.start + 1]
        points[value] = {
            "re_point_2cos_at_centre": point_of(int(re_b[1][CENTRE]), int(re_b[0][CENTRE]), int(re_a[0][CENTRE])),
            "im_point_2cos_at_centre": point_of(int(im_b[1][CENTRE]), int(im_b[0][CENTRE]), int(im_a[0][CENTRE])),
            "re_now_after_at_centre": int(re_a[0][CENTRE]),
            "im_now_after_at_centre": int(im_a[0][CENTRE]),
            "light_now_after_at_centre": int(a[light][0][0][0][CENTRE]),
        }
    report["flux_read"] = {
        "light_line_nodes_differing_V_against_0": light_diff,
        "plane_lines_nodes_differing_V_against_0_re_im": plane_diff,
        "sign_rows_arrays_differing": sign_diff,
        "volume_row_lines_nodes_differing": volume_diff,
        "link_pair_plus_x_at_centre_even_odd_V0": [even0, odd0],
        "link_pair_plus_x_at_centre_even_odd_V": [even1, odd1],
        "turned_nodes": [t0, t1],
        "points": points,
    }
    # (2) the shears' write: one quantum against two
    shear_report = {}
    for label, nodes in (("one_at_111", [CENTRE]), ("two_at_111_and_221", [CENTRE, (2, 2, 1)])):
        board = bare_board(intervals=8)
        light = board.world.seed
        drift = seed.drift_of(board.world.quantum_action)
        now = np.zeros(board.shape, dtype=object)
        for at in nodes:
            now[at] = drift
        set_line(board, light, 0, now, now.copy())
        parts = readings.axis_sources_of(board.families[light].pair[0], board.lines_of(light, 0))
        at = (2, 1, 1)
        shear_report[label] = {
            "g_xx_source_T_xx_at_211": int(np.asarray(parts[0], dtype=object)[at]),
            "g_xy_source_DxDy_at_211": int(np.asarray(parts[2 * AXES], dtype=object)[at]),
            "g_yz_source_at_211": int(np.asarray(parts[2 * AXES + 1], dtype=object)[at]),
            "g_zx_source_at_211": int(np.asarray(parts[2 * AXES + 2], dtype=object)[at]),
            "g_xy_source_nonzero_nodes": int((np.asarray(parts[2 * AXES], dtype=object) != 0).sum()),
            "g_xx_source_nonzero_nodes": int((np.asarray(parts[0], dtype=object) != 0).sum()),
        }
    report["shear_write_two_body"] = shear_report
    # (3) the lattice momentum in the flux lines on a moving lay of light
    board = bare_board(intervals=8)
    light, held = board.world.seed, board.held[0]
    num = board.families[light].pair[0]
    drift = seed.drift_of(board.world.quantum_action)
    now = np.zeros(board.shape, dtype=object)
    now[1, :, :] = drift  # a layer of light at x = 1
    now[2, 1, 1] = drift  # one quantum more off the layer's mirror
    before = np.roll(now, -1, axis=0)  # the same layer one Link behind: a lay moving toward +x
    set_line(board, light, 0, now, before)
    lines = board.lines_of(light, 0)
    parts = readings.axis_sources_of(num, lines)
    p = readings.momentum_of(num, lines)
    source_sums = [int(np.asarray(parts[AXES + a], dtype=object).sum()) for a in range(AXES)]
    g0_before = [np.asarray(board.states[held].lines[1 + AXES + a].now, dtype=object).copy() for a in range(AXES)]
    board.advanced_to_the_close()
    g0_after = [np.asarray(board.states[held].lines[1 + AXES + a].now, dtype=object) for a in range(AXES)]
    written = [int((g0_after[a] - g0_before[a]).sum()) for a in range(AXES)]
    wall = int(np.asarray(board.write_walls[held][1 + AXES], dtype=object).reshape(-1).max())
    report["flux_lines_carry_the_lattice_momentum"] = {
        "flux_source_board_sums": source_sums,
        "num_times_P": [int(num * x) for x in p],
        "equal_exactly": source_sums == [int(num * x) for x in p],
        "P_x_light": int(p[0]),
        "written_g_0a_board_change_after_one_interval_levels": written,
        "write_wall_largest_at_the_node": wall,
        "g_0x_nonzero_nodes_after": int((g0_after[0] != 0).sum()),
        "turned_nodes": int(board.turned.sum()),
    }
    write("d_what_they_buy.json", json.dumps(report, indent=1, default=str))


if __name__ == "__main__":
    main()
