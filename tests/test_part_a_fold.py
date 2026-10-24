"""Part A, gravity's odd lines in the fold form (ALGEBRA.md, The clock family on the Ports; the two hands' joint line of 2026-10-09): a holder of the content declaring the source `flux` carries three odd lines after its tension lines, written by the count's flux through the axis's two Links summed unhalved over twice the count's wall, and every plane reading it has each Link's read folded into the pair (X^c, X^s) with X^s_ji = -X^s_ij; without the key the engine is bit for bit the frozen one."""

from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe import node, world_files
from event_universe.core import paces
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.plane import link_pairs, odd_links
from event_universe.world_files import load_world
from tests.laws import CHARGED, arrays, flux_world, packet
from tests.laws import LINE_KEYS as KEYS


def test_the_odd_line_is_odd(tmp_path, monkeypatch):
    """(b) On a periodic cube of 7^3 with a packet moving along +x: after eight intervals the x odd line is written and nonzero, V_ji = -V_ij on every Link (the +a Port's read at i equals minus the -a Port's read at i + a) and X^s_ji = -X^s_ij exactly, the Link quantity read the same size from both ends with the opposite sign; the vector test: the same packet laid along +y gives the same state transposed bit for bit, every line of every family, the odd lines as a vector (the three axes alike, the step knowing no axis and no name)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = flux_world(tmp_path, (7, 7, 7))
    boards = []
    for axis in (0, 1):
        board = Lattice(load_world(world))
        packet(board, axis, (1, 4), 3, 2)
        for _ in range(8):
            board.step()
        boards.append(board)
    board = boards[0]
    index = [f.name for f in board.families].index(CHARGED["name"])
    gravity = board.states[[f.name for f in board.families].index("gravity")]
    assert (
        gravity.lines[4].now.any() and not gravity.lines[5].now.any() and not gravity.lines[6].now.any()
    )
    links = odd_links(index, board.families, board.states, 1, board.wrap)
    content, factors = board.read(index)
    pairs = link_pairs(board.families[index].pair, board.world.node_clock, content, factors, links, None)
    assert pairs is not None
    odd = pairs[1]
    pace = paces.link_pace_of(board.world.node_clock, content)
    assert links is not None and any(np.asarray(link).any() for link in links)
    for axis in range(3):
        ahead, behind = links[2 * axis], np.roll(links[2 * axis + 1], -1, axis)
        assert np.array_equal(ahead, -behind)
        sizes = [odd[2 * axis] // (pace * pace), np.roll(odd[2 * axis + 1] // (pace * pace), -1, axis)]
        assert np.array_equal(sizes[0], -sizes[1]) and (axis > 0 or np.asarray(sizes[0]).any())
    axes = (1, 0, 2)
    for state, other in zip(boards[0].states, boards[1].states, strict=True):
        lines = list(state.lines)
        if len(lines) == 7:  # the odd lines and the tension lines as vectors: x and y exchanged
            lines = [lines[0], lines[2], lines[1], lines[3], lines[5], lines[4], lines[6]]
        elif (
            len(lines) == 8
        ):  # the holder of the sign's two rows of 1 + 3 lines: the odd lines x and y exchanged
            lines = [lines[0], lines[2], lines[1], lines[3], lines[4], lines[6], lines[5], lines[7]]
        for line, image in zip(lines, other.lines, strict=True):
            for key in KEYS:
                assert np.array_equal(np.transpose(getattr(line, key), axes), getattr(image, key))


def test_the_back_step_is_exact_with_the_fold(tmp_path, monkeypatch):
    """(c) A chain of 25 with a flux holder and a moving packet: 30 intervals forward and 30 back by `step_inverse`, every line's two levels and remainder and every write remainder bit for bit, the fold's pair recomputed from the held rows' levels at each interval's start."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = flux_world(tmp_path, (25, 1, 1))
    board = Lattice(load_world(world))
    packet(board, 0, (1, 4), 7, 3)
    board.amplitude = node.seed_phases(
        board, board.world
    )  # the pairs re-read from the laid state (the centred count, 2026-10-23)
    begun = arrays(board)
    for _ in range(30):
        board.step()
    gravity = board.states[[f.name for f in board.families].index("gravity")]
    assert gravity.lines[4].now.any()  # the odd line was written along the packet's way
    for _ in range(30):
        board.step_inverse()
    assert all(np.array_equal(a, b) for a, b in zip(begun, arrays(board), strict=True))


def test_the_rotation_unit_by_the_rotation_act():
    """The family's rest rotation to the unit, K = omega_0 Gamma, found by a bisection on the rotation act and no root (the two hands' (d) of 2026-10-09; features/phase at the fixed angle theta_0 = 1 / Gamma): 5,046 at [4000, 6000] and Gamma 6,000 (arccos(2 / 3) x 6,000 = 5,046.4), 0 at the massless pair [1, 1], and at [2, 3] within one unit of Gamma arccos(2 / 3); the value checked against the phase line itself in Python's fractions at an independent amplitude, the cosine line's level over X above 2 / 3 one act before K and below it one act after, the crossing within one unit of K; and core/paces.py takes no root."""
    gamma = 6000
    assert phase.rotation_unit(4000, 6000, gamma) == 5046
    assert phase.rotation_unit(1, 1, gamma) == 0
    found = phase.rotation_unit(2, 3, gamma)
    assert abs(found - gamma * np.arccos(2 / 3)) <= 1
    amplitude = (2**36 // gamma) * gamma  # an amplitude of the test's own, a multiple of Gamma
    pair = phase.iterate(phase.seed(amplitude, gamma), found - 1, gamma)
    before = Fraction(int(phase.read(pair)[0]), amplitude)
    after = Fraction(int(phase.read(phase.iterate(pair, 2, gamma))[0]), amplitude)
    assert before > Fraction(2, 3) > after, (before, after)
    source = Path(paces.__file__).read_text(encoding="utf-8")
    assert "division_fixed_point" not in source
