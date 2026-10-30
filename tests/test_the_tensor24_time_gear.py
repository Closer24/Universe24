"""Tensor24's clock, G1 of decision 40: its own gear laid by the load as every row, every gear's teeth its rest and the
clock's count at the now slot by no table, a still clock the act at fixed teeth, the run back exact while every kept tooth
stands below the next round's teeth, and departing where a falling clock breaks that, which the metric's stage owes."""

import json
from pathlib import Path

import numpy as np

from tensor24.engine import step
from tensor24.engine.state import State
from tensor24.main import layout, made
from tensor24.runner.files import sites_of
from tensor24.runner.load import load, mesh_unit, star
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests import frame

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"
SHAPE, GAMMA, ROUNDS = (3, 3, 3), 50, 12  # a small board, a small full rate, the rounds of a run back
REACH = 1 << 40  # the clock's counts are drawn below it, its strides below its square root
STRIDE = 1000  # the clock's stride where it moves alike everywhere


def built(gamma=GAMMA, shape=SHAPE):
    """The example's files at the full rate gamma, loaded, and their layout: (the universe, the loaded, the layout)."""
    u = json.loads((EXAMPLES / "universe.json").read_text(encoding="utf-8"))
    u["integers"]["full_rate"] = gamma
    held, found = load(u, {"gears": []}, sites_of(list(shape)), *made(star(len(shape))))
    assert found == [] and held is not None
    return u, held, layout(u, list(shape), held)


def world(rng, laid, moving=True):
    """A state on the layout: light's gears across 2**256, the clock's own gear a wave of counts in [0, REACH) with its
    strides, or still at 0; each fine tooth within its teeth."""
    rows, n = len(laid.gearing.rest), laid.nb.shape[1]
    a, b = frame.wide(rng, (rows, n)), frame.wide(rng, (rows, n))
    clock = laid.clock.first[0]
    a[clock] = rng.integers(0, REACH, n).astype(object) * moving
    b[clock] = a[clock] - rng.integers(-(1 << 20), 1 << 20, n).astype(object) * moving
    teeth = frame.wide(rng, (rows, n)) % step.weight(laid.gearing, laid.clock, a)
    return State(a, b, teeth, 0 * a)


def reached(laid, s, n):
    """The states after each of n rounds of the tick."""
    return list(rounds(step.tick, laid, s, n))


def test_every_coefficient_is_the_files_integers_by_one_formula_the_clocks_own_gear_among_them():
    """T = 6 den Gamma^2 G^2 at rest for every row, s = 1, no spring (no row holds a term of its own), the force's path
    (T_k = T_d = 1); every row reads its teeth from the clock's own gear, the train the load lays after the file's."""
    u, held, laid = built()
    den, gamma = u["integers"]["den"], u["integers"]["full_rate"]
    g, spokes = mesh_unit(gamma), len(laid.nb)
    rest, s, kick, drive = (
        np.broadcast_to(x, (len(laid.gearing.rest), 1))[:, 0].tolist() for x in laid.gearing
    )
    rows = len(rest)
    assert rest == [spokes * den * gamma * gamma * g * g] * rows
    assert s == kick == drive == [1] * rows
    first, factor, target = (x.tolist() for x in laid.clock)
    assert (
        first == [held.trains[-1].first] * rows and factor == [1] * rows and target == list(range(rows))
    )


def test_every_gears_teeth_are_its_rest_and_the_clocks_count_at_the_now_slot_and_not_the_before_slot():
    """One round of every gear at a moving clock: each gear steps at W = W+ = its rest and the clock's now count; the
    same step at the clock's before count is not the act."""
    _, held, laid = built()
    s = world(np.random.default_rng(1), laid)
    now = step.tick(laid, s)
    force, j = step.sources(laid, s.a)
    q, _ = step.drive(j, laid.gearing.drive, s.rd)
    push = step.driven(laid.gearing, force, q)
    clock = held.trains[-1].first
    assert (s.a[clock] != s.b[clock]).any()
    for slot, act in ((s.a, True), (s.b, False)):
        w = laid.gearing.rest + slot[clock]
        assert frame.same(step.gear(s.a, s.b, s.r, w, push), [now.a, now.b, now.r]) is act


def test_a_clock_standing_at_one_count_gives_the_act_of_a_board_at_its_rest_and_that_count():
    """The clock's own gear still at one count everywhere: the act is the act at fixed teeth, rest plus that count, read
    by no clock; at the count 0 it is the board at rest."""
    _, held, laid = built()
    rng = np.random.default_rng(2)
    clock = held.trains[-1].first
    for count in (0, int(rng.integers(1, REACH))):
        s = world(rng, laid, moving=False)
        s.a[clock], s.b[clock] = count, count
        fixed = laid._replace(
            gearing=laid.gearing._replace(rest=laid.gearing.rest + count), clock=frame.unread()
        )
        assert frame.same(step.tick(laid, s), step.tick(fixed, s))


def test_the_run_back_is_exact_with_the_clock_moving_wherever_every_kept_tooth_stands_within_its_next_teeth():
    """ROUNDS rounds, light across 2**256 and the clock's own gear moving by its strides: every kept tooth stands within
    the teeth the next round reads, and the run back by the tick on the mirrored state reaches the start bit for bit."""
    _, held, laid = built()
    s = world(np.random.default_rng(3), laid)
    ends = reached(laid, s, ROUNDS)
    clock = held.trains[-1].first
    kept = all((x.r < step.weight(laid.gearing, laid.clock, x.a)).all() for x in ends)
    assert kept and (ends[-1].a[clock] != s.a[clock]).any()
    assert frame.same(rewind(step.untick, laid, ends[-1], ROUNDS), s)


def test_the_mirror_is_its_own_inverse_where_the_clock_stands_still_and_not_where_it_moves():
    """Mirrored twice, each fine tooth moves by W(a) - W(b): the state itself where the clock stands still, and not where
    it moves, so a run runs back by its rounds' unticks and one mirror about its ticks departs from the second round."""
    _, _, laid = built()
    for moving in (False, True):
        s = world(np.random.default_rng(5), laid, moving)
        twice = step.mirror(laid, step.mirror(laid, s))
        moved = step.weight(laid.gearing, laid.clock, s.a) - step.weight(laid.gearing, laid.clock, s.b)
        assert frame.same(twice, s._replace(r=s.r + moved)) and frame.same(twice, s) is not moving
        ends = reached(laid, s, 1 + 1)
        once = step.mirror(laid, reached(laid, step.mirror(laid, ends[-1]), 1 + 1)[-1])
        assert (
            frame.same(rewind(step.untick, laid, ends[-1], 1 + 1), s)
            and frame.same(once, s) is not moving
        )


def test_the_run_back_is_exact_while_the_clock_rises_and_departs_at_the_second_round_where_it_falls():
    """Light at rest at one count, the clock's own gear moving by a stride alike everywhere, every tooth at its teeth
    less 1: rising, ROUNDS rounds run back to the start; falling, the first round's kept tooth stands past the next
    teeth, so its round runs back and the second does not: W = W+'s limit on the run back, G2's to close by design."""
    _, held, laid = built()
    clock = held.trains[-1].first
    for stride in (STRIDE, -STRIDE):
        s = world(np.random.default_rng(4), laid, moving=False)
        a = 0 * s.a + REACH
        b = a - stride * (np.arange(len(a)) == clock).astype(object)[:, None]
        s = s._replace(a=a, b=b, r=step.weight(laid.gearing, laid.clock, a) - 1)
        ends = reached(laid, s, ROUNDS)
        exact = [frame.same(rewind(step.untick, laid, ends[n - 1], n), s) for n in (1, 1 + 1, ROUNDS)]
        past = (ends[0].r >= step.weight(laid.gearing, laid.clock, ends[0].a)).any()
        want = [True, True, True] if stride > 0 else [True, False, False]
        assert exact == want and past == (stride < 0)
