"""Tensor24's generic node, G0 of decision 40: the loaded rows geared by one formula of their own numbers, the file's order
of its trains nothing to the run, the loaded act alike under the 24 turns and the translations; what the engine still holds
apart is named by column and record, with the stage of the build that takes it out."""

import json
from pathlib import Path

import numpy as np

from tensor24.engine import state, step
from tensor24.main import layout, made
from tensor24.runner.files import sites_of
from tensor24.runner.load import load
from tests import frame

UNIVERSE = Path(__file__).resolve().parents[1] / "examples" / "tensor24" / "universe.json"
CUBE, SHAPE = (3, 3, 3), (2, 3, 4)  # a board the 24 turn, and a board of three sides
TICKS, SEEDS = 6, range(3)  # the run's ticks, and the worlds the images are read on
# Where the clock's own time gear, laid after the file's trains, still stands apart, each with the stage of decision 40's
# build that takes it out: its own teeth, stretch and spring, its count read by no ruler, and the records that name its row
# and the rows that read it, at G1; its kick and its drive at fixed teeth (places 5 and 6 of the keeper's reading) at G3.
APART = {
    "w": "G1",
    "wp": "G1",
    "stretch": "G1",
    "spring": "G1",
    "reads": "G1",
    "kick": "G3",
    "drive": "G3",
}
RECORDS = {"Ruler.row": "G1", "Ruler.reads": "G1", "LAID": "G1"}


def loaded(universe, shape, gears=()):
    """The universe laid on the board with the setting's gears: the trains' rows, the layout and the state laid."""
    held, found = load(universe, {"gears": list(gears)}, sites_of(list(shape)), *made(shape))
    assert found == [] and held is not None
    return held, layout(universe, list(shape), held), state.State(*held.state)


def seed():
    """The example's universe, its one train the seed."""
    return json.loads(UNIVERSE.read_text(encoding="utf-8"))


def test_every_row_is_geared_by_one_formula_but_the_named_columns_of_the_time_gear():
    """Every train of a file is the seed (its pinion den, decision 37) and the law lays no mass, so the one formula gives
    every row the same coefficients; the rows that depart are the time gear's alone, in the columns named."""
    held, laid, _ = loaded(seed(), CUBE)
    rows, time = len(laid.ruler.reads), held.trains[-1]
    named = dict(zip(state.Gearing._fields, laid.gearing, strict=True)) | {"reads": laid.ruler.reads}
    departs = {}
    for name, column in named.items():
        values = np.broadcast_to(column, (rows, 1))[:, 0].tolist()
        assert len(set(values[: time.first])) == 1, name  # the file's rows alike
        departs[name] = [row for row, value in enumerate(values) if value != values[0]]
    assert {name for name, at in departs.items() if at} == set(APART)
    assert all(at == list(range(time.first, rows)) for at in departs.values() if at)
    kept = {f"Ruler.{field}" for field in ("row", "reads") if field in state.Ruler._fields}
    assert kept | ({"LAID"} if hasattr(state, "LAID") else set()) == set(RECORDS)


def run(universe, gears):
    """The universe's run of TICKS rounds from its gears on the board of three sides, every due beat firing."""
    _, laid, s = loaded(universe, SHAPE, gears)
    every = np.ones((1, laid.nb.shape[1]), dtype=object)
    for _ in range(TICKS):
        s, _ = step.tick(laid, s, every)
    return laid, s


def test_the_files_order_of_its_trains_orders_the_runs_rows_alike():
    """Two seed trains, a hand of A1 and a gear of T1, given in either order with the same gears: the run's rows are the
    other order's rows, and the clock's own rows, laid after the file's, the same (decision 38: no row by position)."""
    universe = seed()
    den = universe["integers"]["den"]
    light, vector = universe["trains"][0], {"name": "vector", "kinds": ["T1"], "part": 1, "pinion": den}
    rng = np.random.default_rng(0)
    sites, rows = sites_of(list(SHAPE)), (light["part"], len(vector["kinds"]) * 3)
    gears = [
        [train, component, site, *rng.integers(-(1 << 40), 1 << 40, 1 + 1).tolist(), 0]
        for train, count in enumerate(rows)
        for component in range(count)
        for site in range(sites)
    ]
    swapped = [[1 - train, *rest] for train, *rest in gears]
    (laid, ran), (_, back) = (
        run(dict(universe, trains=[light, vector]), gears),
        run(dict(universe, trains=[vector, light]), swapped),
    )
    clock = slice(sum(rows), None)  # the clock's own row, laid after the file's
    here, there = (
        (slice(0, rows[0]), slice(rows[0], sum(rows)), clock),
        (slice(rows[1], sum(rows)), slice(0, rows[1]), clock),
    )
    for x, y in zip(ran, back, strict=True):  # a gear's rows mapped; a Node-clock's one row alike
        geared = len(x) == len(ran.a)
        assert (
            frame.same([x[at] for at in here], [y[at] for at in there])
            if geared
            else frame.same([x], [y])
        )
    assert len(laid.ruler.reads) - sum(rows) == 1


def test_the_loaded_act_is_alike_under_the_boards_24_turns_and_its_translations():
    """The seed and the clock's own row on a board the 24 turn: every turn and every unit translation of the sites moves
    the loaded act alike (the frame's images), each Node-clock reading its own counts on the ruler."""
    _, laid, _ = loaded(seed(), CUBE)
    rows, n = len(laid.ruler.reads), laid.nb.shape[1]
    every = np.ones((1, n), dtype=object)
    teeth = np.broadcast_to(laid.gearing.w, (rows, n))

    def world(rng, shape, trains):
        a, b = frame.wide(rng, (rows, n)), frame.wide(rng, (rows, n))
        a[laid.ruler.row], b[laid.ruler.row] = (
            rng.integers(0, laid.ruler.last + 1, n).astype(object) for _ in "ab"
        )
        c = rng.integers(0, 1 + 1, (1, n)).astype(object)
        teeth_drawn = frame.wide(rng, (rows, n)) % teeth
        dial = rng.integers(0, laid.gamma, (1, n)).astype(object)
        return state.State(
            a, b, teeth_drawn, 0 * a, 0 * a, dial, c, c - rng.integers(0, 1 + 1, (1, n)).astype(object)
        )

    e = frame.Engine(lambda nb, s: step.tick(laid, state.State(*s), every), None, world, None)
    assert all(frame.turned(lambda: e, CUBE, np.random.default_rng(seed_), rows) for seed_ in SEEDS)
