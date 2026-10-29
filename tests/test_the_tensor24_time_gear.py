"""Tensor24's clock, G1 of decision 40: its own gear laid by the load as every row, every gear's teeth its rest and the
clock's count at the now slot by no table and at no bound, a still clock the act at fixed teeth, the run back exact."""

import json
from pathlib import Path

import numpy as np

from tensor24.engine import step
from tensor24.engine.state import State
from tensor24.main import layout, made
from tensor24.runner.files import sites_of
from tensor24.runner.load import load, mesh_unit
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests import frame

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"
SHAPE, GAMMA, ROUNDS = (3, 3, 3), 50, 12  # a small board, a small full rate, the rounds of a run back
REACH = 1 << 40  # the clock's counts are drawn below it, its strides below its square root


def built(gamma=GAMMA, shape=SHAPE):
    """The example's files at the full rate gamma, loaded, and their layout: (the universe, the loaded, the layout)."""
    u = json.loads((EXAMPLES / "universe.json").read_text(encoding="utf-8"))
    u["integers"]["full_rate"] = gamma
    held, found = load(u, {"gears": []}, sites_of(list(shape)), *made(shape))
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
    zero = np.zeros((1, n), dtype=object)
    teeth = frame.wide(rng, (rows, n)) % step.weight(laid.gearing, laid.clock, a)
    return State(a, b, teeth, 0 * a, 0 * a, zero, zero.copy(), zero.copy())


def test_every_coefficient_is_the_files_integers_by_one_formula_the_clocks_own_gear_among_them():
    """T = 6 den Gamma^2 G^2 at rest for every row, s = 1, no spring (masses are measured in clicks), the force's path (T_k = T_d =
    1); every row reads its teeth from the clock's own gear, the train the load lays after the file's."""
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
    now, out = step.tick(laid, s, 1)
    force, j = step.sources(laid, s)
    q, _ = step.drive(j, laid.gearing.drive, s.rd)
    push = step.driven(laid.gearing, force, q)
    clock = held.trains[-1].first
    assert out.k.all() and (s.a[clock] != s.b[clock]).any()
    for slot, act in ((s.a, True), (s.b, False)):
        w = laid.gearing.rest + slot[clock]
        assert frame.same(step.gear(s.a, s.b, s.r, s.go, w, w, push), [now.a, now.b, now.r]) is act


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
        assert frame.same(frame.flat(step.tick(laid, s, 1)), frame.flat(step.tick(fixed, s, 1)))


def test_the_run_back_is_exact_with_the_clock_moving_under_random_masks():
    """ROUNDS rounds under random masks, light across 2**256 and the clock's own gear moving: the run back from the
    outs reaches the start bit for bit, the clock's counts moved."""
    _, held, laid = built()
    rng = np.random.default_rng(3)
    s = world(rng, laid)
    masks = [rng.integers(0, 1 + 1, (1, laid.nb.shape[1])).astype(object) for _ in range(ROUNDS)]
    end, outs = rounds(step.tick, laid, s, masks)
    clock = held.trains[-1].first
    assert any(o.k.any() for o in outs) and (end.a[clock] != s.a[clock]).any()
    assert frame.same(rewind(step.untick, laid, end, outs), s)
