"""The mass is read at the Node's content from its three outputs alone, a reading and no act (ALGEBRA.md, The masses under the click's structure, the reading paragraph of 2026-10-23), on a plain (uncharged) record where the interval stands at the Node, the fifth act not fired there (a fired Node's three outputs are the swap's exchanged pre-state, no line of Rule3; a turned record's line carries a fifth term, the Link pairs, the plane's sentence and not this one): Rule3's line at a Node, w a_next + r' = w (2 a_now - a_before) - D a_now + SUM_j R_ij (m_j - a_now) + r, read as a clock, gives 2 cos omega = (a_next + a_before) / a_now up to the remainders' rounding, equal to the four terms over the wall, 2 - D / w - SUM_j R_ij / w + SUM_j R_ij m_j / (w a_now), with D and R_ij the integers of the read at the Node's own paces (`node.rule_of`), so the mass T sin omega is the Node's content's at that interval; the file's num / den is the mass at the content 0 alone. One clause on the Universe24 universe (examples/events/universe24/universe_universe24.json, the content's declaration): the matter clump on the small 3-cube torus (tests/laws_universe.small_world), the identity exact in the rationals at every interval, the content's two terms the vacuum's at the first interval, where the content is 0, and above the vacuum's at every later one, the clump's own well slowing its clock; the swap at the top fires at many of the 27 Nodes in the first intervals of this world (board.swaps, a count per interval) and never at the clump's Node, asserted from the held time line's levels there, the exchanged pre-state the fire's mark (tools/eras.py reads the turned Nodes the same way); no number pinned."""

from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe import node, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_universe import CLUMP, small_world

AXES = 3
INTERVALS = 12


def rule_at(board: Lattice, index: int, at: tuple[int, int, int]) -> tuple[int, int, list[int]]:
    """Rule3's integers of the family's read at the Node: the wall w, the mass D and the six reaches R_ij, at the Node's own paces."""
    family = board.families[index]
    content, factors = board.read(index)
    rule = node.rule_of(family, board.world.node_clock, content, factors, board.unit)
    mass = int(np.asarray(rule.mass)[at]) if np.ndim(rule.mass) else int(rule.mass)
    reaches = [int(np.asarray(r)[at]) if np.ndim(r) else int(r) for r in rule.reaches]
    return int(rule.wall), mass, reaches


def neighbours(array: np.ndarray, at: tuple[int, int, int], shape: tuple[int, ...]) -> list[int]:
    """The six neighbours' levels of the line at the Node, through the wrap, in the Ports' order (+a, -a per axis)."""
    found = []
    for axis in range(AXES):
        for sign in (1, -1):
            there = list(at)
            there[axis] = (there[axis] + sign) % shape[axis]
            found.append(int(array[tuple(there)]))
    return found


def test_the_matter_clumps_clock_is_the_four_terms_at_its_content_at_every_interval(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The clump's Node on the small torus: at every interval of twelve, the clock read from the Node's three outputs and its two remainders, (w (a_next + a_before) + r' - r) / (w a_now), equals the four terms over the wall exactly in the rationals (Rule3's line, an identity and no act), reads 0 at the first interval, the one Node with its six neighbours empty (the dispersion cos omega = (num / (3 den)) SUM_a cos k_a at SUM_a cos k_a = 0, the mass T sin omega = T, the file's rest rotation read on a uniform lay alone), and lies within (0, 2) at every later one, a rotation with the mass T sin omega above 0; the content's part 2 - D / w - SUM R / w is the vacuum's, 2 - 2 (den - num) / den - 2 num / den = 0, at the first interval alone, where the Node's content is 0 and the mass read is the file's, and above it at every later interval, D and each R_ij below the vacuum's integers 2 w (den - num) / den and w num / (3 den) by the paces of the clump's own well (p_0 and p_i below Gamma in the content), so the mass T sin omega read there is the content's and not the file's; the reading is taken on the one line of the real record, at a Node where the fifth act did not fire (the held time line's levels there not the exchanged pre-state, now and before swapped with the fallen level the one before)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(small_world(tmp_path, detector=False)))
    matter = [f.name for f in board.families].index("matter")
    num, den = board.families[matter].pair
    at, shape = (CLUMP[0], CLUMP[1], CLUMP[2]), tuple(board.shape)
    held = board.held[0]  # the gapped time line, the one row the fifth act turns
    clocks = []
    for interval in range(INTERVALS):
        line = board.states[matter].lines[0]
        time = board.states[held].lines[0]
        t_now, t_before = int(time.now[at]), int(time.before[at])
        a, b, r = int(line.now[at]), int(line.before[at]), int(line.remainder[at])
        around = neighbours(np.asarray(line.now), at, shape)
        content = int(np.asarray(board.read(matter)[0])[at])
        wall, mass, reaches = rule_at(board, matter, at)
        board.step()
        after = board.states[matter].lines[0]
        a_next, r_next = int(after.now[at]), int(after.remainder[at])
        time = board.states[held].lines[0]
        fired = (
            int(time.before[at]) == t_now
            and int(time.now[at]) == t_before
            and t_before <= t_now != t_before
        )  # the fifth act's mark at a Node: the time line's two levels exchanged, the fallen level the one before
        assert (
            not fired
        )  # the interval stands at the clump's Node: Rule3's outputs are read, not the swap's
        assert (
            a != 0 and after.before[at] == a
        )  # the record stands at its Node, its level now the level before of the next interval; the clock is read where the level is not 0
        read = Fraction(
            wall * (a_next + b) + r_next - r, wall * a
        )  # the clock from the three outputs and the remainders
        terms = Fraction(2) - Fraction(mass, wall) - Fraction(sum(reaches), wall)
        terms += Fraction(sum(reach * m for reach, m in zip(reaches, around, strict=True)), wall * a)
        assert read == terms  # Rule3's line read as the clock: exact, an identity of the integers
        if interval == 0:
            assert (
                read == 0
            )  # the one-Node lay with its six neighbours empty: the dispersion's reading at SUM_a cos k_a = 0, cos omega = 0, the mass T sin omega = T
        else:
            assert (
                0 < read < 2
            )  # a rotation: cos omega within (0, 1), the clock slowed from the one Node's as the content fills the neighbours
        own = Fraction(2) - Fraction(mass, wall) - Fraction(sum(reaches), wall)
        vacuum = Fraction(2) - Fraction(2 * (den - num), den) - Fraction(2 * num, den)
        assert vacuum == 0  # the vacuum's two terms, the file's mass: the dispersion's rest rotation
        mass_0, reach_0 = Fraction(2 * wall * (den - num), den), Fraction(wall * num, 3 * den)
        if interval == 0:
            assert content == 0 and own == vacuum and mass == mass_0 and set(reaches) == {reach_0}
        else:
            assert content > 0 and own > vacuum  # the content's well slows the Node's clock
            assert mass < mass_0 and all(reach < reach_0 for reach in reaches)
        clocks.append(read)
    assert (
        len(set(clocks)) > 1
    )  # the clock follows the content: the clump's Node is no exact standing mode on the bang's board, each interval's reading its own content's
