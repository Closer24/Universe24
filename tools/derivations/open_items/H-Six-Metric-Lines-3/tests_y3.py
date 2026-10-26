"""Y-S3, the six metric lines written, read and run back exactly through a top (the hand H-Six-Metric-Lines-3, 2026-10-26; for tests/test_the_board.py with its room): on the hole seed of the 5-cube to 20 the six lines' write stands in their write remainders (the flux lines' source the light's own velocities in and out against its gradient, the shears' its two gradients' product; at this den the quotient below one level to 60, every level 0 and the remainders off their half at the Nodes where light flows), the count per Node 98 and the bits within 128 as before, and the run back is exact 10 of 10 through the turns; on the uniform sea of the 3-cube to 120 through the whole-board top at 58 and the exact return at 115 the six lines stay 0 at every Node (the flux 0 by symmetry) and the run back is exact 10 of 10 through the top; a change of the flux lines two Links from a Node leaves its step and its step back bit for bit (the one-Link reach)."""

from __future__ import annotations

import copy

import numpy as np

from event_universe.core.ports import AXES
from event_universe.rows import CARRIER
from tests.laws import node_of, run_back_exact, state_of


def test_the_six_metric_lines_are_written_read_and_run_back_exactly_through_a_top_y_s3() -> None:
    node = node_of("world_hole.json")
    assert run_back_exact(node, 10) == 10
    for _ in range(10):
        node.step()
    lines = node.row(CARRIER).lines
    assert len(lines) == 1 + 3 * AXES and node.census() == (98, 115)
    flux, shears = lines[1 + AXES : 1 + 2 * AXES], lines[1 + 2 * AXES :]
    assert all(int(x) == 0 for line in (*flux, *shears) for x in line.now.reshape(-1))
    assert all(any(int(x) != line.wwall // 2 for x in line.wr.reshape(-1)) for line in (*flux, *shears))
    assert node.counts["turns"] > 0 and node.counts["births"] > 0

    sea = node_of("world_sea_3.json")
    for _ in range(110):
        sea.step()
    kept = [state_of(sea)]
    tops = []
    for _ in range(10):
        sea.step()
        kept.append(state_of(sea))
        if sea.turned.any():
            tops.append((sea.interval, int(sea.turned.sum())))
    six = sea.row(CARRIER).lines[1 + AXES :]
    assert all(int(x) == 0 for line in six for a in (line.now, line.before) for x in a.reshape(-1))
    assert sum(state_of(sea) == kept[9 - k] for k in range(10) if not sea.step_back()) == 10

    base = node_of("world_hole.json")
    for _ in range(6):
        base.step()
    far = copy.deepcopy(base)
    centre = (2, 2, 2)
    for k in range(1 + AXES, 1 + 3 * AXES):
        line = far.row(CARRIER).lines[k]
        for at in np.ndindex(*far.shape):
            if sum(min(abs(a - c), far.cube - abs(a - c)) for a, c in zip(at, centre, strict=True)) >= 2:
                line.now[at] = int(line.now[at]) + k

    def at_centre(n):
        return [(int(line.now[centre]), int(line.before[centre]), int(line.rem[centre])) for row in n.rows() for line in row]
    base.step()
    far.step()
    assert at_centre(base) == at_centre(far)
    base.step_back()
    far.step_back()
    assert at_centre(base) == at_centre(far)
