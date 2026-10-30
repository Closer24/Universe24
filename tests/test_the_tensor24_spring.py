"""Tensor24's spring, the node's term 6 (Animate's ANIMATE-SPRING), on the act itself. In clocks: each gear's hairspring,
its stiffness the held count's, and a spring that stiffens as it winds and bounds the swing. In algebra: J's terms of zero
to three readings from one potential through the 24's own table, by the engine's vertex law; the strengths OPEN at G3."""

import functools

import numpy as np
import pytest

from tensor24.engine import contract, step
from tensor24.engine.state import State
from tensor24.main import made
from tensor24.runner import load as loading
from tests import frame

X, K, UNIT = (
    0,
    3,
    -1,
)  # a T1 family's first gear, then an A1 held count; the unit, the readings' last row
N = 10**6  # the held count's steady count, as in David's m3 and Animate's probe
GAMMA = 200 * N  # the vertex's strength: the spring at the steady count, 2 GAMMA N, is W / 400
W = 800 * GAMMA * N  # the teeth at rest: the spring 2 GAMMA N beats about every 126 rounds
NU = 25 * GAMMA * N  # the held count's own spring, 2 NU = W / 16
BOUND = 2  # the four-leg strength at the bound, 4 BOUND NU = GAMMA^2: below it V has no floor
NONE, HALF, TWICE = 0, BOUND // 2, BOUND + BOUND  # the four-leg strengths the runs take
SMALL, LARGE = 10**5, 10**7  # a small swing and a large one, as Animate's probe lays them
ROUNDS = 1000  # the rounds of a run
OFF = (6 * LARGE // 10, 8 * LARGE // 10, 0)  # the large swing's length, off every axis


def plan(monomials):
    """J's terms by the engine's vertex law from one potential's monomials, (factor, legs), each leg a gear's value row,
    the unit for each of the four a monomial lacks; a monomial of more legs than four is refused by the unpacking."""
    legs = [
        (*legs, *(UNIT,) * (4 - len(legs))) for _, legs in monomials
    ]  # the vertex law reads four legs
    factor = np.array([factor for factor, _ in monomials], dtype=object)
    return contract.pushes(
        factor, tuple(np.array(leg, dtype=np.intp) for leg in zip(*legs, strict=True))
    )


@functools.cache
def dot():
    """The 24's table of T1 with T1 onto A1, as its nonzero entries: c = x . x."""
    kinds, tables, _ = made(loading.star(3))
    labels = [name.upper() for name in kinds._fields]
    table = tables[(labels.index("T1"), labels.index("T1"), labels.index("A1"))][0]
    return tuple((int(table[j, i]), (X + j, X + i)) for j, i in np.argwhere(table))


def potential(mu):
    """V = GAMMA k c + mu c c + NU (k - N)^2, its constant dropped: the vertex of three legs, the term of four, and the
    held count's own spring about its steady count."""
    c = dot()
    return [
        *((GAMMA * f, (K, *legs)) for f, legs in c),
        *((mu * f * h, (*one, *two)) for f, one in c for h, two in c),
        (NU, (K, K)),
        (-2 * NU * N, (K,)),
    ]


def node(monomials):
    """One Node-clock whose neighbours are itself, so that no Mesh pulls it, at the teeth W on the force's path."""
    nb, ones = frame.board((1, 1, 1)), np.ones((1, 1), dtype=object)
    y = frame.plain(nb, frame.meshes_of(nb), ones.repeat(3, axis=1), W * ones)
    return y._replace(plan=plan(monomials))


def run(monomials, lay, rounds, cap=10**60):
    """The counts round by round from the lay at rest, the held count at N; a run past the cap is read as run away and
    stopped there, by the test and never by the step."""
    y, a = node(monomials), np.array([*lay, N], dtype=object).reshape(-1, 1)
    s, counts = State(a, a.copy(), 0 * a, 0 * a), []
    for _ in range(rounds):
        s = step.tick(y, s)
        counts.append(s.a[:, 0].tolist())
        if max(map(abs, counts[-1])) > cap:
            break
    return counts


def crossings(values):
    """The rounds where a count changes sign, 0 read with neither sign."""
    signed = [(t, v > 0) for t, v in enumerate(values) if v]
    return [t for (_, was), (t, now) in zip(signed, signed[1:], strict=False) if was != now]


def exact(lay):
    """The gear on its spring alone by the exact recurrence x+ = 2 x - x- - (2 GAMMA N / W) x from rest, in whole
    numbers: x_t times W^(t + 1), whose sign is x_t's."""
    before, now, counts = lay, W * lay, []
    for _ in range(ROUNDS):
        before, now = now, (2 * W - 2 * GAMMA * N) * now - W * W * before
        counts.append(now)
    return counts


def near(one, other):
    """Two runs' sign changes, as many and each within a round of the other's."""
    return len(one) == len(other) and all(abs(t - u) <= 1 for t, u in zip(one, other, strict=True))


def test_the_vertex_at_the_held_counts_steady_count_beats_as_the_gears_own_spring():
    """The mass is the spring at the steady count, 2 GAMMA N = W / 400 (a beat of 2 pi 20 rounds): at a small swing the
    gear on that spring alone, a term of one reading, changes sign within a round of the exact recurrence's, and the
    vertex's gear within a round of it at every four-leg strength."""
    alone = crossings([x for x, *_ in run([(GAMMA * N, (X, X))], (SMALL, 0, 0), ROUNDS)])
    assert alone and near(alone, crossings(exact(SMALL)))
    for mu in (NONE, HALF, TWICE):
        assert near(crossings([x for x, *_ in run(potential(mu), (SMALL, 0, 0), ROUNDS)]), alone)


def test_the_four_leg_term_bounds_the_swing_that_runs_away_below_the_bound():
    """Below the bound V has no floor: laid at 10^7 or 2 10^7 the gear runs away with no four-leg term and at half the
    bound. At twice it V's floor (V at the held count's least), GAMMA N c + BOUND c c, never passes the lay's own V, and the
    push's coefficient per count, the vertex's and the four legs', stays below the held count's own, 2 NU = W / 16."""
    for lay in (LARGE, LARGE + LARGE):
        assert all(len(run(potential(mu), (lay, 0, 0), ROUNDS)) < ROUNDS for mu in (NONE, HALF))
        held = run(potential(TWICE), (lay, 0, 0), ROUNDS)
        floor = [GAMMA * N * c + BOUND * c * c for c in (x * x for x, *_ in held)]
        top = GAMMA * N * lay * lay + TWICE * lay * lay * lay * lay  # V at the lay, the held count at N
        springs = [2 * GAMMA * abs(k) + 4 * TWICE * x * x for x, _, _, k in held]
        assert len(held) == ROUNDS and max(floor) <= top and max(springs) < NU + NU


def test_the_run_is_turned_by_the_24_and_beats_alike_along_an_axis_and_off_it():
    """The 24's threefold turn about the cube's diagonal turns the run gear for gear, exactly; and the four-leg term
    through A1, (x . x)^2, beats alike laid along an axis and off it at one length: the gears' sum changes sign at the
    same rounds both ways."""
    held, lay = potential(TWICE), (LARGE, 3 * SMALL, -5 * SMALL)
    turned = run(held, (lay[2], lay[0], lay[1]), ROUNDS)
    assert turned == [[z, x, y, k] for x, y, z, k in run(held, lay, ROUNDS)]
    along, off = (crossings([sum(c[:3]) for c in run(held, at, ROUNDS)]) for at in ((LARGE, 0, 0), OFF))
    assert along and along == off


def test_the_run_back_returns_every_gear_through_the_four_legs():
    """J reads the now slot alone, so the mirrored tick runs every round back, its terms of three readings too: 600
    rounds laid off every axis from a moving start, forth and back, return the state bit for bit."""
    y, a = node(potential(TWICE)), np.array([[LARGE + LARGE], [3], [-5], [N]], dtype=object)
    start = s = State(a, a - 1, 0 * a, 0 * a)
    for act in (step.tick, step.untick):
        for _ in range(600):
            s = act(y, s)
    assert frame.same(s, start)


MUTANTS = {  # the contraction broken where the spring and the four legs read it, and the law that must catch it
    "the unit read as 0": (
        lambda p, r, g: contract.contract(p, np.concatenate((r[:-1], 0 * r[-1:])), g),
        test_the_vertex_at_the_held_counts_steady_count_beats_as_the_gears_own_spring,
    ),
    "the third reading ignored, the unit in its place": (
        lambda p, r, g: contract.contract(p._replace(third=0 * p.third + len(r) - 1), r, g),
        test_the_four_leg_term_bounds_the_swing_that_runs_away_below_the_bound,
    ),
}


@pytest.mark.parametrize("name", MUTANTS)
def test_each_law_fails_on_its_mutant(monkeypatch, name):
    """Each mutant of the contraction, put where the step calls it, fails the law it was written for."""
    mutant, law = MUTANTS[name]
    monkeypatch.setattr(step, "contract", mutant)
    with pytest.raises(AssertionError):
        law()
