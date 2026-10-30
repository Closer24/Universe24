"""Tensor24's load, the loader's generic parts: each refusal by name with its edge, the gears laid on their rows, the
square found by its kinds' character alone, the promise the run back's own condition, and no term of J, as no file
declares a coupling."""

import copy
import itertools

import numpy as np
import pytest

from tensor24.engine.state import State
from tensor24.engine.step import tick, untick
from tensor24.main import made as joint
from tensor24.runner.board import board
from tensor24.runner.files import held_departures, vocabulary
from tensor24.runner.load import geometry, load, star
from tensor24.runner.run import promises
from tests.frame import plain

D = 3
SITES = 8
TRAINS = [
    {"name": "light", "kinds": ["A1"], "part": 2},
    {"name": "spin", "kinds": ["T1"], "part": 1},
    {"name": "axial", "kinds": ["A2"], "part": 1},
    {"name": "stress", "kinds": ["T2"], "part": 1},
    {"name": "potential", "kinds": ["A1", "T1"], "part": 2},
    {"name": "field", "kinds": ["T1", "A1"], "part": 1},
]
DIMS = {"A1": 1, "A2": 1, "T1": 3, "T2": 3}
ROWS = sum(
    sum(DIMS[k] for k in t["kinds"]) * t["part"] for t in TRAINS
)  # every train's rows, counted afresh
LAID = ROWS  # every row a file's train's: the load lays no row of its own


def gears(rows=LAID):
    """The gears' shape, at 0: what J lands in."""
    return np.zeros((rows, SITES), dtype=object)


@pytest.fixture(scope="module")
def made():
    """The kinds and tables as main.py, the one joint, makes them for the load."""
    return joint(star(D))


def universe(trains=TRAINS):
    return {"trains": copy.deepcopy(trains), "chosen": {"key": 1, "push": 0, "notch": 0}}


def loaded(made, u, gears=()):
    """The files held against the engine's kinds, then loaded, as the run does: the departures, or the loaded and none."""
    ks, c, square = made
    setting = {"gears": [list(g) for g in gears]}
    found = held_departures(u, setting, vocabulary(ks, square))
    held, found = (None, found) if found else load(u, setting, SITES, ks, c, square)
    return (None if found else held), found


def edits():
    """One edit per refusal of the load: the edit, the departure named, or None at the refusal's edge."""

    def train(at, **fields):
        return lambda u: u["trains"][at].update(fields)

    def square(part=1):  # the four-vector's square appended
        family = {"name": "metric", "kinds": ["A1", "T1", "A1", "E", "T2"], "part": part}
        return lambda u: u["trains"].append(family)

    return {
        "a kind none of the 24's": (
            train(1, kinds=["E1/2"]),
            "universe.trains[1].kinds[0]: 'E1/2' is none of the 24's kinds",
        ),
        "E alone": (
            train(1, kinds=["E"]),
            "universe.trains[1].kinds[0]: 'E' has no whole basis the 24 permute",
        ),
        "E in the four-vector's square": (square(), None),
        "the square's kinds at part 2, its character twice the square's": (
            square(part=1 + 1),
            f"universe.trains[{len(TRAINS)}].kinds[3]: 'E' has no whole basis the 24 permute",
        ),
        "a twin hand, the act generic in the part": (train(1, part=4), None),
        "a part of 3": (train(1, part=3), None),
        "a hand of T1": (train(1, part=2), None),
    }


def refused(made, rule):
    """The rule's edit loaded: its departure named with nothing loaded, or, at its edge, loaded with none named."""
    edit, named = edits()[rule]
    u = universe()
    edit(u)
    held, found = loaded(made, u)
    return (
        (any(named in line for line in found) and held is None)
        if named
        else (found == [] and held is not None)
    )


def squared_and_promised(made):
    """A train is marked the four-vector's square where its part times its kinds' character is the square's: in every
    order of the square's five kinds, and not for ten rows of three T1 kinds and one of A1. The promise, every tooth
    within its edge's dial, -D <= s < D, is named where it fails, and the run back is exact where it holds."""
    w, d = 5, 5 + 5  # the teeth and the edge's dial
    a = np.arange(SITES, dtype=object)[None, :] + 0  # velocities of 1
    held = lambda r: promises(State(a, a - 1, r, 0 * a, 0 * a), w + 0 * a, w + 0 * a)  # noqa: E731
    for tooth in (d + 1, -d - 1, d):
        r = np.zeros((1, SITES), dtype=object)
        r[0, 2] = tooth
        edge = f"row 0, site 2: the tooth {tooth} not within the edge's dial [-{d}, {d})"
        assert held(r) == [f"{edge} of the teeth {w} and {w}"] and not rewound(r, w)
    r = np.zeros((1, SITES), dtype=object) + d - 1
    assert held(r) == [] and rewound(r, w)
    family, other = ("A1", "T1", "A1", "E", "T2"), ("T1", "T1", "T1", "A1")
    for kinds in [*sorted(set(itertools.permutations(family))), other]:
        u = universe()
        u["trains"].append({"name": "metric", "kinds": list(kinds), "part": 1})
        held, found = loaded(made, u)
        assert found == [] and held.trains.square.tolist() == [0] * len(TRAINS) + [int(kinds != other)]


def test_the_load_lays_every_gear_on_its_trains_rows_or_names_each_refusal_and_raises_none(
    made, monkeypatch
):
    """Each refusal names its broken file and its edge loads; a gear lands on its train's rows, whole past 64 bits, and
    off them is named; Sofer's fuzz, a board past the arrays or the memory named, nothing raised; the square found by
    its kinds' character; the promise the run back's own condition."""
    assert loaded(made, universe())[1] == [] and all(refused(made, rule) for rule in edits())
    squared_and_promised(made)
    rows, site, now, before, tooth = (
        2,
        3,
        1 << 70,
        (1 << 70) + 1,
        (1 << 70) + 2,
    )  # the light's hand: two rows
    last = sum(DIMS[k] for k in TRAINS[-1]["kinds"]) * TRAINS[-1]["part"]  # the last train's rows
    laid = [(0, rows - 1, site, now, before, tooth), (len(TRAINS) - 1, last - 1, site, before, now, 0)]
    held, found = loaded(made, universe(), laid)
    a, b, r, rd, k = held.state
    assert found == [] and (a[rows - 1, site], b[rows - 1, site], r[rows - 1, site]) == (
        now,
        before,
        tooth,
    )
    assert (a[ROWS - 1, site], b[ROWS - 1, site]) == (before, now)
    assert (a.shape, b.shape, r.shape, rd.shape) == ((LAID, SITES),) * len("abrd")
    assert all(x.dtype == object for x in held.state)
    assert not any(
        np.shares_memory(x, y) for x, y in itertools.combinations(held.state, 1 + 1)
    )  # every array its own: no write reaches two
    assert not rd.any() and not k.any() and k.shape == (len(TRAINS), SITES)
    assert (a != 0).sum() == (b != 0).sum() == len(laid) and (r != 0).sum() == 1
    held, found = loaded(made, universe(), [(0, rows, site, now, before, 0)])
    assert held is None and found == [f"setting.gears[0]: component {rows} off train 0's {rows} rows"]
    ks, c, square = made
    held, found = load(universe(), {}, SITES, ks, c, square)
    assert (
        found == [] and not held.potential[0].any()
    )  # the notch's monomials alone, at the factor 0 here
    _, found = load(universe(), {"gears": []}, 1 << 64, ks, c, square)
    assert len(found) == 1 and found[0].startswith(f"piece.shape: {LAID} rows at")

    def no_room(*args, **kwargs):
        raise MemoryError("no room")

    monkeypatch.setattr(np, "zeros", no_room)
    _, found = load(universe(), {"gears": []}, SITES, ks, c, square)
    assert found == [
        f"piece.shape: {LAID} rows at {SITES} sites, more than the arrays of this machine hold (no room)"
    ]


def rewound(r, w):
    """One round of every gear on a ring of sites and its run back: the start back exactly, or not."""
    nb = board((SITES, 1, 1))
    _, meshes = geometry(nb, D)
    layout = plain(nb, meshes, np.ones(D * SITES, dtype=object), w)
    a = np.arange(SITES, dtype=object)[None, :] + 0
    s = State(a, a - 1, r, 0 * a, 0 * a)
    return all((x == y).all() for x, y in zip(untick(layout, tick(layout, s)), s, strict=True))
