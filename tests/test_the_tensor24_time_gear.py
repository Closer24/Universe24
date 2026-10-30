"""Tensor24's clock, G1 and G1b: the 00 slot of the metric family the file writes, every gear's teeth its rest and that
slot's count at the now slot, a still clock the act at fixed teeth, and the run back exact while every kept tooth stands
below the next round's teeth, departing where a falling clock breaks that, which the metric's stage owes."""

import itertools
import json
from pathlib import Path

import numpy as np

from tensor24.engine import step
from tensor24.engine.state import State
from tensor24.main import layout, made, ran
from tensor24.runner.files import sites_of
from tensor24.runner.load import load, mesh_unit, star
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tensor24.runner.run import ledger_of
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
    """A state on the layout: light's gears across 2**256, the clock's slot a wave of counts in [0, REACH) with its
    strides, or still at 0; each fine tooth within its teeth."""
    rows, n = len(laid.gearing.rest), laid.nb.shape[1]
    a, b = frame.wide(rng, (rows, n)), frame.wide(rng, (rows, n))
    clock = frame.dense(laid.clock, rows, rows)[0].tolist().index(1)
    a[clock + 1 : clock + 10], b[clock + 1 : clock + 10] = (
        0,
        0,
    )  # the family past its 00 slot at rest, the flat metric
    a[clock] = rng.integers(0, REACH, n).astype(object) * moving
    b[clock] = a[clock] - rng.integers(-(1 << 20), 1 << 20, n).astype(object) * moving
    teeth = frame.wide(rng, (rows, n)) % step.weight(laid.gearing, laid.clock, a)
    return State(a, b, teeth, 0 * a)


def reached(laid, s, n):
    """The states after each of n rounds of the tick."""
    return list(rounds(step.tick, laid, s, n))


def test_every_coefficient_is_the_files_integers_by_one_formula_the_metric_familys_rows_among_them():
    """T = 6 den Gamma^2 G^2 at rest for every row, s = 1, no spring (no row holds a term of its own), the force's path
    (T_k = T_d = 1); every row reads its teeth from the 00 slot of the metric family, the train the file writes."""
    u, held, laid = built()
    den, gamma = u["integers"]["den"], u["integers"]["full_rate"]
    g, spokes = mesh_unit(gamma), len(laid.nb)
    rest, s, kick, drive = (
        np.broadcast_to(x, (len(laid.gearing.rest), 1))[:, 0].tolist() for x in laid.gearing
    )
    rows = len(rest)
    assert rest == [spokes * den * gamma * gamma * g * g] * rows
    assert s == kick == drive == [1] * rows
    (clock,) = [x.first for x in held.trains if x.square]
    read, ones = frame.dense(laid.clock, rows, rows), np.ones(rows, dtype=int)
    assert (read == np.outer(ones, np.eye(rows, dtype=int)[clock])).all()


def test_every_gears_teeth_are_its_rest_and_the_clocks_count_at_the_now_slot_and_not_the_before_slot():
    """One round of every gear at a moving clock: each gear steps at W = W+ = its rest and the clock's now count; the
    same step at the clock's before count is not the act."""
    _, held, laid = built()
    s = world(np.random.default_rng(1), laid)
    now = step.tick(laid, s)
    force, j = step.sources(laid, s.a)
    q, _ = step.drive(j, laid.gearing.drive, s.rd)
    push = step.driven(laid.gearing, force, q)
    (clock,) = (x.first for x in held.trains if x.square)  # the 00 slot of the four-vector's square
    assert (s.a[clock] != s.b[clock]).any()
    for slot, act in ((s.a, True), (s.b, False)):
        w = laid.gearing.rest + slot[clock]
        assert frame.same(step.gear(s.a, s.b, s.r, w, push), [now.a, now.b, now.r]) is act


def test_a_clock_standing_at_one_count_gives_the_act_of_a_board_at_its_rest_and_that_count():
    """The clock's slot still at one count everywhere: the act is the act at fixed teeth, rest plus that count, read
    by no clock; at the count 0 it is the board at rest."""
    _, held, laid = built()
    rng = np.random.default_rng(2)
    (clock,) = (x.first for x in held.trains if x.square)  # the 00 slot of the four-vector's square
    for count in (0, int(rng.integers(1, REACH))):
        s = world(rng, laid, moving=False)
        s.a[clock], s.b[clock] = count, count
        fixed = laid._replace(
            gearing=laid.gearing._replace(rest=laid.gearing.rest + count), clock=frame.unread()
        )
        assert frame.same(step.tick(laid, s), step.tick(fixed, s))


def test_the_run_back_is_exact_with_the_clock_moving_wherever_every_kept_tooth_stands_within_its_next_teeth():
    """ROUNDS rounds, light across 2**256 and the clock's slot moving by its strides: every kept tooth stands within
    the teeth the next round reads, and the run back by the tick on the mirrored state reaches the start bit for bit."""
    _, held, laid = built()
    s = world(np.random.default_rng(3), laid)
    ends = reached(laid, s, ROUNDS)
    (clock,) = (x.first for x in held.trains if x.square)  # the 00 slot of the four-vector's square
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
    """Light at rest at one count, the clock's slot moving by a stride alike everywhere, every tooth at its teeth
    less 1: rising, ROUNDS rounds run back to the start; falling, the first round's kept tooth stands past the next
    teeth, so its round runs back and the second does not: W = W+'s limit on the run back, G2's to close by design."""
    _, held, laid = built()
    (clock,) = (x.first for x in held.trains if x.square)  # the 00 slot of the four-vector's square
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


def test_every_order_of_the_familys_kinds_lays_and_runs_alike():
    """The metric family's rows are the square's basis in whatever order the file writes its kinds: every order lays
    the same reads of the clock and the grips, and runs the same rounds from one state, its 00 slot moving."""
    u, held, laid = built()
    (at,) = np.flatnonzero(held.trains.square)
    rules, s, ends = made(star(len(SHAPE))), world(np.random.default_rng(6), laid), []
    for kinds in sorted(set(itertools.permutations(u["trains"][at]["kinds"]))):
        u["trains"][at]["kinds"] = list(kinds)
        again, found = load(u, {"gears": []}, sites_of(list(SHAPE)), *rules)
        there = layout(u, list(SHAPE), again)
        reads = zip(there.clock + there.stretch, laid.clock + laid.stretch, strict=True)
        assert found == [] and all(np.array_equal(x, y) for x, y in reads)
        ends.append(reached(there, s, 1 + 1)[-1])
    assert all(frame.same(x, ends[0]) for x in ends)


def test_a_setting_breaking_the_promise_is_named_at_its_round_and_leaves_no_file(tmp_path):
    """The 00 slot laid at minus the rest, W 0, is named before the first round; laid falling by a stride under a tooth
    at the rest less 1, it is named at the second round; neither raises, nor leaves a record or a ledger."""
    u, held, laid = built()
    at, rest = int(np.flatnonzero(held.trains.square)[0]), int(laid.gearing.rest[0, 0])
    for gears, named in (
        ([[at, 0, 0, -rest, -rest, 0]], "row"),
        ([[at, 0, 0, 0, STRIDE, 0], [0, 0, 0, 0, 0, rest - 1]], "round 2: row"),
    ):
        setting = {"version": 1, "ticks": ROUNDS, "gears": gears}
        files = {"universe": u, "piece": {"version": 1, "shape": list(SHAPE)}, "setting": setting}
        for name, body in files.items():
            (tmp_path / f"{name}.json").write_text(json.dumps(body), encoding="utf-8")
        record = tmp_path / "record.json"
        found = ran([tmp_path / f"{name}.json" for name in files], record)
        assert found and found[0].startswith(named), found
        assert not record.exists() and not ledger_of(record).exists()


def test_two_families_the_files_choice_are_both_read_each_by_its_00_slot():
    """Two trains of the square's kinds, the files' choice: every row's teeth read both 00 slots, each at the factor 1."""
    u, held, _ = built()
    u["trains"].append(dict(u["trains"][int(np.flatnonzero(held.trains.square)[0])], name="again"))
    two, found = load(u, {"gears": []}, sites_of(list(SHAPE)), *made(star(len(SHAPE))))
    laid, clocks = layout(u, list(SHAPE), two), [x.first for x in two.trains if x.square]
    rows = len(laid.gearing.rest)
    read, ones = frame.dense(laid.clock, rows, rows), np.ones(rows, dtype=int)
    assert found == [] and len(clocks) == 1 + 1
    assert (read == np.outer(ones, np.eye(rows, dtype=int)[clocks].sum(axis=0))).all()
