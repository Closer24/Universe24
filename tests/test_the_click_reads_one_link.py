"""The click's read of the board, one Link and one number (ALGEBRA.md, The click's read of the board, the sentence of 2026-10-24; `digits.lattice_of`, `digits.read_of`): at the first whether the hole-seed 3-cube draws at den 1,021, each neighbour's Link lattice F_ij is a multiple of the neighbour's own lattice F_j and the coarse index is the floor of the fine one over the two lattices' ratio, and the number is one function of the Node's read and the set of its six Links' reads: a permutation of the frame's neighbours leaves it unchanged, and a frame naming a Node beyond no Port is refused by name."""

from __future__ import annotations

import pytest

from event_universe import digits, meeting_board, registry, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_universe import bare_torus


def test_the_link_lattice_is_the_neighbours_own_coarsened_and_no_port_order_enters_the_number(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """Inside the board's own close at the first draw, on the interval's start the close reads: for every record of quanta of every family read, F_j divides F_ij at every neighbour and the neighbour's digit r div F_ij is (r div F_j) div (F_ij div F_j) on every line; the frame's neighbours reversed, and rolled by one, read the same number; the Port of a Node beyond none of the Node's Ports is refused."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(bare_torus(tmp_path, 3, 20)), output=lambda line: None)
    shape, periodic, real, checked = board.shape, board.world.periodic, meeting_board.read_of, []

    def read(b, reads, label):  # type: ignore[no-untyped-def]
        number = real(b, reads, label)
        for index, frame in reads:
            ports = digits.ports_of(frame, shape, periodic)
            for record in registry.quanta_records(b.families, b.states, index):
                rule, pairs = digits.rule_and_pairs(b, index, record)
                lattice = digits.lattice_of(rule, frame, pairs, ports)
                for link, there in zip(lattice[1:], frame[1:], strict=True):
                    own = digits.frame_of(there, shape, periodic)
                    fine = digits.lattice_of(rule, own, pairs, digits.ports_of(own, shape, periodic))[0]
                    assert link % fine == 0
                    for line in b.lines_of(index, record):
                        kept = int(line.remainder[there])
                        assert kept // link == (kept // fine) // (link // fine)
        reversed_ = [(index, [frame[0], *frame[:0:-1]]) for index, frame in reads]
        rolled = [(index, [frame[0], *frame[2:], frame[1]]) for index, frame in reads]
        assert digits.read_of(b, reversed_, label) == digits.read_of(b, rolled, label) == number
        checked.append(number)
        return number

    monkeypatch.setattr(meeting_board, "read_of", read)
    while not checked and board.interval < 20:
        board.step()
    assert checked
    with pytest.raises(ValueError, match="beyond none of its Ports"):
        digits.ports_of([(0, 0, 0), (1, 1, 0)], shape, periodic)
