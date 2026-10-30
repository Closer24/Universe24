"""Tensor24's generic node, G0 to G1b: every row of every kind and part geared by one formula, every row's teeth read at
the 00 slot of the train whose kinds are the four-vector's square, found by no name, place or role, the trains' order
nothing to the layout or the run, no term the load lays, and the loaded act alike under the 24's turns."""

import itertools
import json
from pathlib import Path

import numpy as np

from tensor24.engine import kinds, state, step
from tensor24.main import layout, made
from tensor24.runner import load as loading
from tensor24.runner.files import sites_of
from tensor24.runner.load import load, star
from tests import frame

UNIVERSE = Path(__file__).resolve().parents[1] / "examples" / "tensor24" / "universe.json"
CUBE, SHAPE = (3, 3, 3), (2, 3, 4)  # a board the 24 turn, and a board of three sides
# the run's ticks, the images' worlds, the clock's counts drawn below it
TICKS, SEEDS, REACH = 6, range(3), 1 << 40
# the four-vector's square, A1 + T1 + A1 + E + T2: its first row the clock
SQUARE = (("A1", "T1", "A1", "E", "T2"), 1)
# the kinds, the tables and the square, derived once from the star of three axes
RULES = made(star(len(CUBE)))


def loaded(universe, shape, gears=()):
    """The universe laid on the board with the setting's gears: the trains' rows, the layout and the state laid."""
    held, found = load(universe, {"gears": list(gears)}, sites_of(list(shape)), *RULES)
    assert found == [] and held is not None
    return held, layout(universe, list(shape), held), state.State(*held.state)


def seeded(*shapes):
    """The example's universe with seed trains, one per (kinds, part), each massless, its pinion den."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    den = universe["integers"]["den"]
    named = [{"name": f"{k}{p}", "kinds": list(k), "part": p, "pinion": den} for k, p in shapes]
    return dict(universe, trains=named)


def clock_of(held):
    """The clock's row: the first row of the one train whose kinds are the four-vector's square."""
    (first,) = [t.first for t in held.trains if t.square]
    return first


def test_every_row_of_every_kind_and_part_is_geared_by_one_formula_and_the_load_lays_no_term():
    """Every train a seed, the square among them, so the one formula gives every row the same coefficients, grips and
    read of the clock, the square's 00 slot; the load lays no term of J; no record or function holds a row apart."""
    shapes = [((k,), p) for k in ("A1", "A2", "T1", "T2") for p in (1, 1 + 1)]
    held, laid, _ = loaded(seeded(*shapes, SQUARE), CUBE)
    rows = len(laid.gearing.rest)
    for name, column in zip(state.Gearing._fields, laid.gearing, strict=True):
        assert len(set(np.broadcast_to(column, (rows, 1))[:, 0].tolist())) == 1, name
    assert len(set(laid.grip.ravel().tolist())) == 1 and all(len(x) == 0 for x in laid.plan)
    first, factor, target = (x.tolist() for x in laid.clock)
    assert set(first) == {clock_of(held)} and set(factor) == {1} and target == list(range(rows))
    assert not {"Ruler", "LAID"} & set(dir(state)) and not {"ruled", "reading", "at"} & set(dir(step))


def orders_alike():
    """A hand of A1, a gear of T1, one of A2 and the square, in all 24 orders, the same small gears and the square's 00
    slot moving: each train's rows in the layout and in the run are its rows in every other order."""
    shapes = [(("A1",), 1 + 1), (("T1",), 1), (("A2",), 1), SQUARE]
    rng = np.random.default_rng(0)
    sizes = [loaded(seeded(shape), SHAPE)[0].trains[0].rows() for shape in shapes]
    gears = [
        [t, c, x, *rng.integers(-8, 9, 1 + 1).tolist(), 0]
        for t, size in enumerate(sizes)
        for c in range(size if shapes[t] != SQUARE else 1)
        for x in range(sites_of(list(SHAPE)))
    ]
    runs = []
    for order in itertools.permutations(range(len(shapes))):
        moved = [[order.index(t), *r] for t, *r in gears]
        held, laid, s = loaded(seeded(*(shapes[t] for t in order)), SHAPE, moved)
        for _ in range(TICKS):
            s = step.tick(laid, s)
        place = [held.trains[order.index(t)].first for t in range(len(shapes))]
        rows = np.concatenate([np.arange(f, f + n) for f, n in zip(place, sizes, strict=True)])
        gearing = [np.broadcast_to(x, s.a.shape)[rows] for x in laid.gearing]
        runs.append([*gearing, *(x[rows] for x in s)])
    alike = all(frame.same(each, runs[0]) for each in runs[1:])
    return alike and (runs[0][len(state.Gearing._fields)] != 0).any()


def test_every_order_of_the_trains_runs_alike_and_a_clock_found_by_place_does_not(monkeypatch):
    """The orders run alike; with the clock read at the last train's first row, its place, they do not (the B2 mutant)."""
    assert orders_alike()
    geared = loading.geared

    def by_place(universe, trains, spokes):
        gearing, (first, factor, target), grip = geared(universe, trains, spokes)
        return gearing, (0 * first + trains[-1].first, factor, target), grip

    monkeypatch.setattr(loading, "geared", by_place)
    assert not orders_alike()


def turned(m, laid, held, s, teeth):
    """The state turned by m: sites moved, each train's components by its kind's matrix, a negated component's tooth
    flipped at the teeth it was carried at."""
    xyz, sides = np.indices(CUBE).reshape(3, -1), np.array(CUBE)[:, None]
    site = np.ravel_multi_index(tuple((m @ xyz) % sides), CUBE)
    acting = kinds.kinds(m[None, :, :])
    rows = len(laid.gearing.rest)
    turn = np.eye(rows, dtype=object)
    for train in held.trains:
        matrix = kinds.square(acting)[0] if train.square else acting[train.kinds[0]][0]
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
    """Seeds of the kinds A1 and A2, T1 and T2, and the square with its 00 slot moving, on a board the 24 turn: every turn of
    the state, its components by their kinds' matrices and the square's rows by the square, turns the act alike."""
    held, laid, _ = loaded(seeded(*(((k,), 1) for k in ("A1", "A2", "T1", "T2")), SQUARE), CUBE)
    rows, n = len(laid.gearing.rest), laid.nb.shape[1]
    assert np.array_equal(laid.nb, frame.board(CUBE))
    for seed_ in SEEDS:
        rng = np.random.default_rng(seed_)
        a, b = frame.wide(rng, (rows, n)), frame.wide(rng, (rows, n))
        clock = clock_of(held)
        a[clock], b[clock] = (rng.integers(0, REACH, n).astype(object) for _ in "ab")
        teeth = step.weight(laid.gearing, laid.clock, a)
        s = state.State(a, b, frame.wide(rng, (rows, n)) % teeth, 0 * a)
        out = step.tick(laid, s)
        for m in frame.turns():
            there, _ = turned(m, laid, held, s, teeth)
            moved, _ = turned(m, laid, held, out, teeth)
            assert frame.same(step.tick(laid, there), moved), m.tolist()
