"""The books of a turned record (issue #2169, finding 1; the reader's ruling of 2026-10-21; ALGEBRA.md, The share's change is the currents, the clause of 2026-10-21): a region's booking of a turned plane reads the flux line's own current with the Link's pair the step reads (`readings.turned_currents_of`, `board_readings.turned_read`), where the plain bilinear of a turned pair turns at the difference of the two Nodes' angles, the gauge's oscillation of zero mean, which the floor at 0 turned into credits by the phase of the window's sums (the builder's hydrogen_1s with a 7-Node ball: -3.07 and +2.76 W_rec over [1, 35] and [36, 70], the standing body credited to its own region at 70 and erased; the pair's booking +0.0019, -0.0005, -0.0032 and +0.00006 W_rec over the four windows of 140, no credit, the measurer's run on the branch). Here the same on a world the test lays into a tmp folder: the proton's pixel at the centre of an open cube of 5 and the electron laid standing in its well by tools/standing_lay.py (the 1s at Omega 0.7025 against omega_0 0.8411), a region of seven Nodes on the electron's, three windows; and the plain path on the node detector test's chain (tests/test_the_node_detector.py): a plain record reads no pair and its currents and its booking are the plain bilinear's as before."""

from __future__ import annotations

import numpy as np

from event_universe import board_readings, readings, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import PACKET, TOOL, slit_world

INTERVALS = 4  # the plain path on the node detector test's chain, the packet crossing the region

IRRATIONAL = "a reader of the sign writes its charge per quantum by its count unit"  # the refusal of 2026-10-24 (tests/test_the_sign_reader_with_an_irrational_sine.py)


def test_a_plain_records_currents_and_booking_stand_bit_for_bit(tmp_path, monkeypatch):
    """The plain path (`readings.currents_of` with no pairs, `board_readings.currents`, the intake of `credit.booked`) on the node detector test's chain, the light packet crossing the region of two Nodes over four intervals: the board's reading of a plain record is bit for bit the plain bilinear's through every Port (no pair, no frame, no Link at the wall on this chain), the x Ports' sums over the open chain opposite exactly (what leaves a Node through +X enters its neighbour through -X) and the y and z Ports' 0 (the chain's one Node per axis reads itself), the region's intake 0 while the packet's front stands off the region and growing once it crosses, no swap at the top (gravity massless, the swap reads the gapped time line alone) and no family turned. The former pins (2026-10-23: the +X sums -7,246,344,000, -7,236,402,000, -6,959,934,000 and -6,952,620,000 with the intakes 0, 0, 2,305,536,000 and 24,543,744,000; main 74cafb5d1's 7,236,372,000, 7,229,028,000 with 2,268,672,000, 7,223,886,000 with 25,021,440,000 before) were read on a course where the swap at the top fired at the interval 2 at two Nodes of the massless gravity row, the reading struck the same day (the swap reads the gapped time line alone; the third sum reads -7,227,342,000 since), named here and not asserted (ENGINE.md section 9)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    region, draw = [[13, 0, 0], [14, 0, 0]], {}
    packet = {**PACKET, "top": {"x": [8, 8], "y": [0, 0], "z": [0, 0]}, "edge": {"x": 4, "y": 0, "z": 0}}
    chain = dict(shape=[24, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), faces=[])
    readers = [{"name": "near", "positions": region}]
    world = slit_world(
        tmp_path, TOOL, "chain", packets=[packet], node_detectors=readers, draw=draw, **chain
    )
    board = Lattice(load_world(world))
    light = [f.name for f in board.families].index("charge")
    assert not board.turning
    found = []
    for _ in range(INTERVALS):
        through = board_readings.currents(board)[light]
        plain = readings.currents_of(board.families[light].pair[0], board.record(light), board.wrap)
        assert all(
            np.array_equal(a, b) for a, b in zip(through, plain, strict=True)
        )  # the plain bilinear's
        board.step()
        sums = [int(np.asarray(c, dtype=object).sum()) for c in through]
        intake = sum(map(sum, board.credit.intake.get((light, "near"), {}).values()))
        found.append((sums, intake))
    print(f"PLAIN {found}")
    assert all(sums[0] == -sums[1] < 0 and sums[2:] == [0] * 4 for sums, _intake in found)
    assert [intake == 0 for _sums, intake in found] == [True, True, False, False]
    assert found[2][1] > 0 and found[3][1] > found[2][1]  # the intake grows as the packet crosses
    assert board.swaps == [] and not board.turning
