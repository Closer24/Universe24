"""kl2's tests (under 15 s): (1) the one-Node theorem at a far end: a lay of (d_now, d_before) on the taken row's line at a neighbour of a Node changes the row's lattice momentum by exactly momentum_of (the standing gradient's three components), measured by the board's P before and after on the hole world's seed; (2) the integer solver exact and size-reduced on a solvable system of the inverse's shape (6 equations, 24 unknowns, the columns the far ends' gradients)."""
import json
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("KL2_SRC", "/dev/shm/tmp/kl2/src_kl2")
sys.path.insert(0, SRC)
sys.path.insert(0, HERE)
sys.set_int_max_str_digits(0)

from event_universe.core.ports import AXES, PORTS, across, port_of  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.take import lay, momentum_of, neighbour  # noqa: E402
from kl2_inverse import cross3, size_reduce, solve_integer  # noqa: E402


def board_p(row):
    num = row.pair[0]
    out = []
    for a in range(AXES):
        s = 0
        for z in row.lines:
            s = s + across(z.now, port_of(a, 0)) * z.before - z.now * across(z.before, port_of(a, 0))
        out.append(2 * num * int(np.sum(s)))
    return out


def test_far_end_lay_books_momentum_of_exactly():
    u, w = load_world(os.path.join(HERE, "../../../../tests/worlds/world_hole.json"))
    node = Node(u, w)
    rec = node.records().index(node.emitter())
    row = node.records()[rec]
    rng = random.Random(7)
    at = (1, 1, 2)
    for port in range(PORTS):
        far = neighbour(node, at, port)
        d_now, d_before = rng.randint(-300, 300), rng.randint(-300, 300)
        z = row.lines[0]
        before = board_p(row)
        expected = momentum_of(node, z.now, z.before, far, d_now=d_now, d_before=d_before, num=row.pair[0])
        lay(node, rec, far, (d_now, d_before, 0, 0))
        after = board_p(row)
        assert [b - a for a, b in zip(before, after, strict=True)] == expected
        lay(node, rec, far, (d_now, d_before, 0, 0), -1)
        assert board_p(row) == before


def test_solver_exact_on_the_inverse_shape():
    rng = random.Random(3)
    cols = []
    for port in range(PORTS):
        arm = [0, 0, 0]
        arm[port // 2] = 2 * (1 if port % 2 == 0 else -1)
        for _ in range(4):
            v = [rng.randint(-2000, 2000) for _ in range(3)]
            cols.append(v + cross3(arm, v))
    A = [[cols[k][i] for k in range(24)] for i in range(6)]
    x_true = [rng.randint(-50, 50) for _ in range(24)]
    b = [sum(A[i][k] * x_true[k] for k in range(24)) for i in range(6)]
    x, rem, kernel = solve_integer(A, b)
    assert rem == [0] * 6 and len(kernel) == 18
    y = size_reduce(x, kernel)
    assert [sum(A[i][k] * y[k] for k in range(24)) for i in range(6)] == b
    assert max(abs(v) for v in y) <= max(abs(v) for v in x)
