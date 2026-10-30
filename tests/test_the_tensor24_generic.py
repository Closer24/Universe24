"""Tensor24's generic node, G0 and G1 of decision 40: every loaded row of every kind and part geared by one formula, the
clock's own gear among them and every row reading its teeth from it, no term the load lays, the file's order of its trains
nothing to the layout or the run, and the loaded act alike under the 24's turns of sites and components."""

import itertools
import json
from pathlib import Path

import numpy as np

from tensor24.engine import kinds, state, step
from tensor24.main import layout, made
from tensor24.runner.files import sites_of
from tensor24.runner.load import load, star
from tests import frame

UNIVERSE = Path(__file__).resolve().parents[1] / "examples" / "tensor24" / "universe.json"
CUBE, SHAPE = (3, 3, 3), (2, 3, 4)  # a board the 24 turn, and a board of three sides
TICKS, SEEDS, REACH = (
    6,
    range(3),
    1 << 40,
)  # the run's ticks, the images' worlds, the clock's counts drawn below it


def loaded(universe, shape, gears=()):
    """The universe laid on the board with the setting's gears: the trains' rows, the layout and the state laid."""
    held, found = load(universe, {"gears": list(gears)}, sites_of(list(shape)), *made(star(len(shape))))
    assert found == [] and held is not None
    return held, layout(universe, list(shape), held), state.State(*held.state)


def seeded(*shapes):
    """The example's universe with seed trains, one per (kind, part), each massless, its pinion den."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    den = universe["integers"]["den"]
    named = [{"name": f"{k}{p}", "kinds": [k], "part": p, "pinion": den} for k, p in shapes]
    return dict(universe, trains=named)


def test_every_row_of_every_kind_and_part_is_geared_by_one_formula_and_the_load_lays_no_term():
    """Every train a seed, so the one formula gives every row, the clock's own gear's too, the same coefficients, grips
    and read of the clock; the load lays no term of J; no record or function of the engine holds a row apart."""
    shapes = [(k, p) for k in ("A1", "A2", "T1", "T2") for p in (1, 1 + 1)]
    held, laid, _ = loaded(seeded(*shapes), CUBE)
    rows = len(laid.gearing.rest)
    for name, column in zip(state.Gearing._fields, laid.gearing, strict=True):
        assert len(set(np.broadcast_to(column, (rows, 1))[:, 0].tolist())) == 1, name
    assert len(set(laid.grip.ravel().tolist())) == 1 and all(len(x) == 0 for x in laid.plan)
    first, factor, target = (x.tolist() for x in laid.clock)
    assert set(first) == {held.trains[-1].first} and set(factor) == {1} and target == list(range(rows))
    assert not {"Ruler", "LAID"} & set(dir(state)) and not {"ruled", "reading", "at"} & set(dir(step))


def run(universe, gears):
    """The universe's layout and its run of TICKS rounds from its gears on the board of three sides."""
    held, laid, s = loaded(universe, SHAPE, gears)
    for _ in range(TICKS):
        s = step.tick(laid, s)
    return held, laid, s


def test_every_order_of_three_trains_orders_the_layouts_and_the_runs_rows_alike():
    """A hand of A1, a gear of T1 and one of A2, in all six orders with the same small gears: each train's rows in the
    layout and in the run are its rows in every other order, and the clock's own row, laid after the file's, the same."""
    shapes = [("A1", 1 + 1), ("T1", 1), ("A2", 1)]
    rng = np.random.default_rng(0)
    sizes = [loaded(seeded(shape), SHAPE)[0].trains[0].rows() for shape in shapes]
    gears = [
        [t, c, x, *rng.integers(-8, 9, 1 + 1).tolist(), 0]
        for t, size in enumerate(sizes)
        for c in range(size)
        for x in range(sites_of(list(SHAPE)))
    ]
    runs = []
    for order in itertools.permutations(range(len(shapes))):
        moved = [[order.index(t), *rest] for t, *rest in gears]
        held, laid, s = run(seeded(*(shapes[t] for t in order)), moved)
        at = [
            np.arange(held.trains[order.index(t)].first, held.trains[order.index(t)].first + n)
            for t, n in enumerate(sizes)
        ]
        rows = np.concatenate([*at, np.arange(held.trains[-1].first, len(laid.gearing.rest))])
        reads = [np.array(x[rows].tolist(), dtype=object) for x in (laid.clock.first, laid.clock.factor)]
        runs.append([*(np.broadcast_to(x, s.a.shape)[rows] for x in laid.gearing), *reads])
        runs[-1] += [x[rows] for x in s]
    moved = runs[0][-len(state.State._fields)]  # the first order's run, its now slots
    assert all(frame.same(each, runs[0]) for each in runs[1:]) and (moved != 0).any()


def turned(m, laid, held, s, teeth):
    """The state turned by m: sites moved, each train's components by its kind's matrix, a negated component's tooth
    flipped at the teeth it was carried at."""
    xyz, sides = np.indices(CUBE).reshape(3, -1), np.array(CUBE)[:, None]
    site = np.ravel_multi_index(tuple((m @ xyz) % sides), CUBE)
    acting = kinds.kinds(m[None, :, :])
    rows = len(laid.gearing.rest)
    turn = np.eye(rows, dtype=object)
    for train in held.trains[:-1]:
        matrix = acting[train.kinds[0]][0]
        at = train.first + np.arange(len(matrix)) * train.part
        for part in range(train.part):
            turn[np.ix_(at + part, at + part)] = matrix
    sign = turn.sum(axis=1)[:, None]  # each row's one entry: its source row's sign
    there = state.State(*(np.empty_like(x) for x in s))
    for x, y in zip(there, s, strict=True):
        x[:, site] = y
    there.a[:, site], there.b[:, site] = turn @ s.a, turn @ s.b
    flips = (1 - sign) // (1 + 1)  # 1 where the component is negated
    r = np.abs(turn) @ s.r
    there.r[:, site] = flips * (teeth - 1 - r) + (1 - flips) * r
    return there, site


def test_the_loaded_act_is_alike_under_the_24s_turns_of_its_sites_and_components():
    """Seeds of the kinds A1 and A2, T1 and T2, and the clock's own gear moving, on a board the 24 turn: every turn of the state, its
    components by their kinds' matrices, turns the act alike; the loaded board is the frame's."""
    held, laid, _ = loaded(seeded(("A1", 1), ("A2", 1), ("T1", 1), ("T2", 1)), CUBE)
    rows, n = len(laid.gearing.rest), laid.nb.shape[1]
    assert np.array_equal(laid.nb, frame.board(CUBE))
    for seed_ in SEEDS:
        rng = np.random.default_rng(seed_)
        a, b = frame.wide(rng, (rows, n)), frame.wide(rng, (rows, n))
        clock = held.trains[-1].first
        a[clock], b[clock] = (rng.integers(0, REACH, n).astype(object) for _ in "ab")
        teeth = step.weight(laid.gearing, laid.clock, a)
        s = state.State(a, b, frame.wide(rng, (rows, n)) % teeth, 0 * a)
        out = step.tick(laid, s)
        for m in frame.turns():
            there, _ = turned(m, laid, held, s, teeth)
            moved, _ = turned(m, laid, held, out, teeth)
            assert frame.same(step.tick(laid, there), moved), m.tolist()
