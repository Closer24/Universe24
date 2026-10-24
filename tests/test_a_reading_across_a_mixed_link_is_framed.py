"""A reading of a turned record across a Link whose two ends stand in different frames takes the two ends in one frame, as the step does (ALGEBRA.md, The swap at the top, the frame clause; readings.turned_currents_of through `Turned.frames`, board_readings.turned_read): on the deliberately split charged board of tests/test_the_swap_with_a_charge (the dust's amplitude 869 on the layer x = 0 and 400 on the others, the tops over 34 to 37), stepped through the first three fire intervals (34, 35 and 36: 1, 8 and 9 Nodes) so that Links between a turned and an unturned Node stand, (1) the Wronskian's flux through every Link is one number read from both ends in the frame every record was born in: (-1)^b_i F_i(+a) = -(-1)^b_j F_j(-a) exactly at every Link, mixed Links among them, with b the phase row's remainder at the wall 2; (2) at least one mixed Link carries a flux other than 0, so the clause is read and not vacuous; (3) the same reading with the frames left out (the former reading, the neighbour's value as its own frame holds it) breaks (1) at a mixed Link. Since 2026-10-24 (the charge the Wronskian per quantum, alpha E_h T / Gamma, the read weight one) the framed read cancels to the bit where the Link's two ends stand in one frame and at 63 of the board's 68 mixed Links, and at the other five to a residue of 39, 65 and 75 levels (the five Links' currents 1,006 to 30,860; the mixed Links' reach 299,803): there the two ends read two pairs for the one Link (flux.pairs_of through plane.phase_links; (303103, -50004) against (303153, -49700) at the record 0, the axis x, the Node (2, 1, 1), the exact numerators 4,211,912 against -4,224,160 before any rounding), against the law's sentence that the pair the two ends read is one and the same whichever end turned (ALGEBRA.md, The swap at the top, the frame clause); the residue measured and printed, its cause owed by name, no inequality asserted; the exact cancellation at every mixed Link to 2026-10-24 kept by name."""

import numpy as np

from event_universe import board_readings, node, readings, world_files
from event_universe.core.ports import AXES, arrival
from event_universe.lattice import Lattice
from event_universe.loader.derived import row_of
from event_universe.world_files import load_world
from tests.laws_charged import GAP, LAY, charged_world


def test_a_turned_records_current_across_a_mixed_link_is_one_number_in_one_frame(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(Lattice, "gate", lambda board: None)
    board = Lattice(load_world(charged_world(tmp_path, GAP, 21, 0, divisor=LAY, layers=(869, 400, 400))))
    board.output = lambda line: None
    for _ in range(36):
        board.step()
    assert [s[0] for s in board.swaps if s[1] == 1 and s[0] > 5] == [34, 35, 36], board.swaps
    index = [i for i, f in enumerate(board.families) if f.name == "charged"][0]
    holder = node.sign_holder(index, board.families)
    mixed, broken = 0, 0
    for record in range(board.families[index].records):
        row = row_of(board.families, index, record)
        assert row is not None
        frame = np.asarray(board.states[holder].phases[row][node.PHI].remainder, dtype=object)
        sign = 1 - 2 * frame  # (-1)^b at every Node
        turned = board_readings.turned_read(board, index, record)
        lines = board.lines_of(index, record)
        framed = readings.turned_currents_of(lines, board.wrap, turned)
        former = readings.turned_currents_of(lines, board.wrap, turned._replace(frames=None))
        for axis in range(AXES):
            far_sign = arrival(sign, axis, 1, board.wrap)
            differ = far_sign != sign  # the Link's two ends in different frames
            residues = {}
            for read, kept in ((framed, True), (former, False)):
                own = sign * np.asarray(read[2 * axis], dtype=object)
                far = far_sign * arrival(
                    np.asarray(read[2 * axis + 1], dtype=object), axis, 1, board.wrap
                )
                residues[kept] = np.abs(own + far)
                if kept:
                    framed_own, framed_far = own, far
                    agree = ~np.asarray(differ)
                    assert np.all((own + far)[agree] == 0), (
                        record,
                        axis,
                    )  # (1) one number from both ends where the frames agree
                    mixed += int(np.count_nonzero(np.asarray(differ) & (own != 0)))  # (2)
                else:
                    broken += int(np.count_nonzero(np.asarray(differ) & (own + far != 0)))  # (3)
            at = np.asarray(differ) & (residues[True] != 0)
            for where in zip(*np.nonzero(at), strict=True):
                print(
                    record,
                    axis,
                    where,
                    int(residues[True][where]),
                    int(residues[False][where]),
                    int(framed_own[where]),
                    int(framed_far[where]),
                )  # the residue at a mixed Link, owed by name (five Links of 68 on this board: 39, 65 and 75 levels; 0 to 2026-10-24); the unframed read's beside it, measured, no inequality asserted
    assert mixed > 0 and broken > 0, (mixed, broken)
