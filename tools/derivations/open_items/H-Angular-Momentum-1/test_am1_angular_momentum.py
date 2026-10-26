"""H-Angular-Momentum-1's test (under 15 s): the orbital moment 2 L_c of MV-S1's Link momentum density, read on three shipped worlds for a few intervals.
(a) the uniform board (world_pair_3): 2L = 0 and P = 0 at every interval (no current at all);
(b) the symmetric lay (world_bodies, two packets mirrored about the centre): 2L = 0 and P = 0 to the bit through turns and clicks (the cube's 48 about the centre);
(c) the hole (world_hole, the lay on the x axis through the hole): P_y = P_z = 0 and 2L_x = 0 to the bit, 2L_y = -2L_z (the transposition y <-> z of the exact six carries the pseudovector) before any birth."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))

from am_reader import moment, positions, row_p  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402


def read(world_file, intervals, centre=None):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(os.path.join(ROOT, "tests", "worlds", world_file))
    shape = tuple(int(x) for x in world["shape"])
    centre = centre or [n // 2 for n in shape]
    node = Node(universe, world)
    d = positions(shape, centre)
    out = []
    for _ in range(intervals):
        node.step()
        L = [0, 0, 0]
        P = [0, 0, 0]
        for row in node.records():
            l, p, _b = moment(row_p(row, int(row.pair[0])), d, shape)
            L = [L[k] + l[k] for k in range(3)]
            P = [P[k] + p[k] for k in range(3)]
        out.append((L, P, int(node.counts["births"])))
    return out


def test_uniform_board_has_no_moment():
    for L, P, _ in read("world_pair_3.json", 6):
        assert L == [0, 0, 0] and P == [0, 0, 0]


def test_symmetric_lay_keeps_the_moment_zero_to_the_bit():
    for L, P, _ in read("world_bodies.json", 4):
        assert L == [0, 0, 0] and P == [0, 0, 0]


def test_hole_keeps_the_axis_moment_and_the_transposition():
    rows = read("world_hole.json", 4)
    assert all(b == 0 for _, _, b in rows)
    for L, P, _ in rows:
        assert P[1] == 0 and P[2] == 0
        assert L[0] == 0
        assert L[1] == -L[2]
    assert any(L != [0, 0, 0] for L, _, _ in rows)


def test_moving_lay_moment_is_zero_about_its_centre_and_r_cross_p_about_another():
    """The light packet laid at [6, 4, 4] with a wave along y (the folder's world): 2 L about its own centre 0 to the bit, and 2 L about [4, 4, 4] equal to the doubled (c - c') x P = (0, 0, 4 P_y) exactly while no current reaches the seam."""
    sys.set_int_max_str_digits(0)
    universe, world = load_world(os.path.join(HERE, "world_packet_wave.json"))
    shape = tuple(int(x) for x in world["shape"])
    node = Node(universe, world)
    d_own, d_other = positions(shape, [6, 4, 4]), positions(shape, [4, 4, 4])
    for _ in range(2):
        node.step()
        L_own, L_other, P = [0, 0, 0], [0, 0, 0], [0, 0, 0]
        for row in node.records():
            p = row_p(row, int(row.pair[0]))
            l1, p1, _ = moment(p, d_own, shape)
            l2, _p2, _ = moment(p, d_other, shape)
            L_own = [L_own[k] + l1[k] for k in range(3)]
            L_other = [L_other[k] + l2[k] for k in range(3)]
            P = [P[k] + p1[k] for k in range(3)]
        assert L_own == [0, 0, 0]
        assert P[0] == 0 and P[2] == 0 and P[1] != 0
        assert L_other == [0, 0, 4 * P[1]]
