"""Tensor24's load: each refusal by name with its edge, the gears laid on their rows, the promise, the square found by
its kinds' character alone, and no term of J, as no file declares a coupling."""

import copy
import itertools

import numpy as np
import pytest

from tensor24.engine.state import State
from tensor24.engine.step import tick, untick
from tensor24.main import made as joint
from tensor24.runner.board import board
from tensor24.runner.files import held_departures, promises, vocabulary
from tensor24.runner.load import geometry, load, star
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
    return {"trains": copy.deepcopy(trains)}


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


@pytest.mark.parametrize("rule", sorted(edits()))
def test_each_refusal_of_the_load_names_its_own_broken_file_and_its_edge_loads(rule, made):
    assert loaded(made, universe())[1] == []
    edit, named = edits()[rule]
    u = universe()
    edit(u)
    held, found = loaded(made, u)
    assert (
        (any(named in line for line in found) and held is None)
        if named
        else (found == [] and held is not None)
    ), found


def test_a_gear_off_its_trains_rows_is_named_and_the_last_row_is_laid(made):
    """A gear lands on its train's own rows, the first train's with its fine tooth and the last's at its last component,
    every integer whole past 64 bits; the rest is 0."""
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
    a, b, r, rd = held.state
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
    assert not rd.any()
    assert (a != 0).sum() == (b != 0).sum() == len(laid) and (r != 0).sum() == 1
    held, found = loaded(made, universe(), [(0, rows, site, now, before, 0)])
    assert held is None and found == [f"setting.gears[0]: component {rows} off train 0's {rows} rows"]


def rewound(r, w):
    """One round of every gear on a ring of sites and its run back: the start back exactly, or not."""
    nb = board((SITES, 1, 1))
    _, meshes = geometry(nb, D)
    layout = plain(nb, meshes, np.ones(D * SITES, dtype=object), w)
    a = np.arange(SITES, dtype=object)[None, :] + 0
    s = State(a, a - 1, r, 0 * a)
    return all((x == y).all() for x, y in zip(untick(layout, tick(layout, s)), s, strict=True))


def test_the_promise_is_named_where_it_fails_and_is_the_run_backs_own_condition():
    w = 5
    for tooth in (w, w + 1, -1):
        r = np.zeros((1, SITES), dtype=object)
        r[0, 2] = tooth
        assert promises(r, w) == [f"row 0, site 2: the fine tooth {tooth} not within [0, {w})"]
        assert not rewound(r, w)
    r = np.zeros((1, SITES), dtype=object) + w - 1
    assert promises(r, w) == [] and rewound(r, w)


def test_the_files_the_checker_holds_load_or_are_named_and_none_raises(made):
    """Sofer's fuzz of stage 6: no gears key loads as none and lays no term of J, and a board past one array is named."""
    ks, c, square = made
    held, found = load(universe(), {}, SITES, ks, c, square)
    assert found == [] and not any(len(x) for x in held.plan)
    _, found = load(universe(), {"gears": []}, 1 << 64, ks, c, square)
    assert len(found) == 1 and found[0].startswith(f"piece.shape: {LAID} rows at")


def test_a_board_the_machine_cannot_hold_is_named(made, monkeypatch):
    """Where the machine's memory refuses the lay's arrays, the board is named and nothing raises."""
    ks, c, square = made

    def refused(*args, **kwargs):
        raise MemoryError("no room")

    monkeypatch.setattr(np, "zeros", refused)
    _, found = load(universe(), {"gears": []}, SITES, ks, c, square)
    assert found == [
        f"piece.shape: {LAID} rows at {SITES} sites, more than the arrays of this machine hold (no room)"
    ]


def test_the_square_is_found_by_its_kinds_character_in_every_order_and_by_nothing_else(made):
    """A train is marked the four-vector's square where its part times its kinds' character is the square's: in every
    order of the square's five kinds, and not for ten rows of three T1 kinds and one of A1."""
    family, other = ("A1", "T1", "A1", "E", "T2"), ("T1", "T1", "T1", "A1")
    for kinds in [*sorted(set(itertools.permutations(family))), other]:
        u = universe()
        u["trains"].append({"name": "metric", "kinds": list(kinds), "part": 1})
        held, found = loaded(made, u)
        assert found == [] and held.trains.square.tolist() == [0] * len(TRAINS) + [int(kinds != other)]
