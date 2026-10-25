"""a48: the one-Node tests of the remainder's mirror and the draw's even read (pytest; under 15 s; integers only).
Run from tools/derivations/a48: PYTHONPATH=src_a48:. python -m pytest test_a48_even_read.py -q
(the flagged copy's engine, the flag read at call time from A48_READ, so one process tests both paths)."""
import json
import os
import random

import numpy as np
import pytest

from a48_48 import image, world_image
from event_universe import close, take
from event_universe.core.rule3 import carried_division, half
from event_universe.loader.world import load_world
from event_universe.node import Node

HERE = os.path.dirname(os.path.abspath(__file__))
W_EVEN = 6 * 15162856759112389 * 1000**3 * 16**2  # the mean wall at the seed, (w div 2)(2 Gamma) with G = 16
W_ODD = W_EVEN + 1


def kick(wall, da, r, force):
    """The riding line's division as interval.py writes it: P_in = W da + r - half(W), P_out = P_in + force,
    (quotient, remainder) = division of P_out with the carry half(W) at the wall W."""
    p = wall * da + r - half(wall) + force
    return carried_division(p, wall, half(wall), 1)


def test_the_ones_complement_is_the_exact_mirror_of_the_riding_division_at_every_numerator():
    """r* = W - 1 - r (the one rule's mirror, rule3.mirrored) with the line negated: the quotient -q and the remainder
    W - 1 - s at every one of 10,000 random numerators, at an even wall and at an odd one."""
    rng = random.Random(48)
    for wall in (W_EVEN, W_ODD):
        exact = 0
        for _ in range(10_000):
            da, r, f = rng.randrange(-5, 6), rng.randrange(wall), rng.randrange(-3 * wall, 3 * wall)
            q, s = kick(wall, da, r, f)
            q2, s2 = kick(wall, -da, wall - 1 - r, -f)
            exact += q2 == -q and s2 == wall - 1 - s
        assert exact == 10_000, (wall % 2, exact)


def test_the_twos_complement_mirror_fails_at_the_remainder_0_alone():
    """r* = 2 half(W) - r (the mirror the half-wall seed imposes on a reversed line): at an even wall the quotient -q and the
    remainder 2 half(W) - s wherever s > 0, and at s = 0 the quotient 1 - q (the law's note); at an odd wall the two
    mirrors are one and exact."""
    rng = random.Random(24)
    wall = W_EVEN
    exact = defects = 0
    for _ in range(10_000):
        da, r, f = rng.randrange(-5, 6), rng.randrange(1, wall), rng.randrange(-3 * wall, 3 * wall)
        q, s = kick(wall, da, r, f)
        q2, s2 = kick(wall, -da, 2 * half(wall) - r, -f)
        if s > 0:
            exact += q2 == -q and s2 == 2 * half(wall) - s
        else:
            defects += q2 == 1 - q and s2 == 0
    assert exact + defects == 10_000
    # the defect by construction: a numerator at s = 0
    r = half(wall) + 7
    f = -(wall * 1 + r - half(wall) + half(wall)) + 3 * wall  # P_out + half(W) = 3 W exactly
    q, s = kick(wall, 1, r, f)
    q2, s2 = kick(wall, -1, 2 * half(wall) - r, -f)
    assert s == 0 and q2 == 1 - q and s2 == 0
    assert 2 * half(W_ODD) - 5 == W_ODD - 1 - 5


def test_the_even_read_is_invariant_under_the_mirror_it_is_read_for():
    """|r - half(W)| is the same at r and at 2 half(W) - r (every r); min(r, W - 1 - r) the same at r and W - 1 - r; the
    two reads differ by at most 1 at an even wall and are one read at an odd wall."""
    rng = random.Random(7)
    for wall in (W_EVEN, W_ODD):
        h = half(wall)
        for _ in range(10_000):
            r = rng.randrange(1, wall)
            assert abs(r - h) == abs((2 * h - r) - h)
            assert min(r, wall - 1 - r) == min(wall - 1 - r, r)
            assert 0 <= (h - abs(r - h)) - min(r, wall - 1 - r) <= (wall + 1) % 2


def nodes_of(flag):
    """The chiral 5-cube and its x-reflection run to the interval of the first parting draw, with the draws logged."""
    os.environ.pop("A48_READ", None)
    os.environ.pop("A48_SWAP", None)
    if flag:
        os.environ["A48_READ"] = flag
        os.environ["A48_SWAP"] = "half"
    universe, world = load_world(os.path.join(HERE, "worlds", "chiral_5cube_24.json"))
    m = np.diag([-1, 1, 1]).astype(int)
    eye = np.eye(3, dtype=int)
    from a48_parting import DRAWS, wrapped_read

    DRAWS.clear()
    base = Node(json.loads(json.dumps(universe)), world_image(world, eye, 5, 7))
    img = Node(json.loads(json.dumps(universe)), world_image(world, m, 5, 7))
    for _ in range(7):
        close.read_number = wrapped_read("base")
        base.step()
        close.read_number = wrapped_read("image")
        img.step()
    close.read_number = take.read_number
    os.environ.pop("A48_READ", None)
    os.environ.pop("A48_SWAP", None)
    draws = {"base": {(d[0], d[1]): d for d in DRAWS["base"]}, "image": {(d[0], d[1]): d for d in DRAWS["image"]}}
    return base, img, draws, m


def draws_apart(draws, m):
    apart = 0
    for (i, at), d in draws["base"].items():
        e = draws["image"].get((i, image(m, at, 5)))
        if e is None or sorted((x[5], x[6]) for x in d[2]) != sorted((x[5], x[6]) for x in e[2]) or d[3] != e[3]:
            apart += 1
    return apart


def test_the_one_node_draw_parts_under_the_engine_and_holds_under_the_even_read():
    """The engine's path (the flags unset): the first draw apart at interval 6, Node (1, 0, 2), one digit (an im line's
    remainder read at 2 half(W) - r), and the births at interval 7 differ (1 against 0). The even read with the swap's mirror about the birth (A48_READ=even, A48_SWAP=half): every draw of the
    first 7 intervals equal through the image, the births equal with the ends exchanged."""
    base, img, draws, m = nodes_of(None)
    assert draws_apart(draws, m) > 0
    births_b = [e for e in base.log if e["event"] == "birth" and e["i"] == 7]
    births_i = [e for e in img.log if e["event"] == "birth" and e["i"] == 7]
    assert (len(births_b), len(births_i)) == (1, 0)
    base, img, draws, m = nodes_of("even")
    # the per-draw digit sets through the image are read by a48_parting.py (0 apart over 24 intervals, out/parting_both_5cube_24_mx.json);
    # here the births (the ends exchanged) and the credits (the senses exchanged) are compared
    c_b = sorted((e["i"], image(m, tuple(e["node"]), 5), e["line"], -e["sense"], e["beat"]) for e in base.log if e["event"] == "credit")
    c_i = sorted((e["i"], tuple(e["node"]), e["line"], e["sense"], e["beat"]) for e in img.log if e["event"] == "credit")
    assert c_b == c_i
    b = sorted((e["i"], image(m, tuple(e["node"]), 5), e["line_pair"], image(m, tuple(e["plus"]), 5), image(m, tuple(e["minus"]), 5)) for e in base.log if e["event"] == "birth")
    i = sorted((e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"])) for e in img.log if e["event"] == "birth")
    assert b == i and len(b) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
