"""Tensor24's load: the coupling rows' plan against a naive sum, each refusal by name with its edge, and the rename law."""

import copy
import itertools

import numpy as np
import pytest

from tensor24.engine.contract import Plan, contract
from tensor24.engine.state import Layout, State
from tensor24.engine.step import tick, untick
from tensor24.main import made as joint
from tensor24.runner.board import board
from tensor24.runner.files import COUPLING, OPERANDS
from tensor24.runner.load import load, promises

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


def gears(rows=ROWS):
    """The gears' shape, at 0: what J lands in."""
    return np.zeros((rows, SITES), dtype=object)


def row(**fields):
    """A coupling row of the files' twelve fields, every one 0 but those named and a strength of 1."""
    return list((dict(zip(COUPLING, [0] * (len(COUPLING) - 1) + [1], strict=True)) | fields).values())


def op(name):
    return OPERANDS.index(name)


COUPLINGS = [
    row(
        train=1, with_train=1, target=4, strength=3
    ),  # the dot of the spin with itself, into the potential's A1
    row(
        train=1, with_train=4, with_kind=1, with_part=1, target=1, strength=-2
    ),  # the cross with the potential's T1
    row(train=2, with_train=1, target=3, strength=5),  # A2 times T1 into T2
    row(
        train=4,
        operand=op("gradient"),
        with_train=0,
        with_part=1,
        target=4,
        target_kind=1,
        target_part=1,
        strength=7,
    ),
    row(
        train=0,
        part=1,
        with_train=4,
        with_kind=1,
        with_part=1,
        operand=op("pull"),
        target=1,
        strength=11,
    ),
    row(train=0, with_train=0, with_part=1, target=0, target_part=1, strength=13),
    row(
        train=0, part=1, operand=op("gradient"), with_train=1, target=4, strength=17
    ),  # a hand's second part's
    row(
        train=5, kind=1, operand=op("gradient"), with_train=1, target=4, strength=19
    ),  # an A1 at its train's second kind
]


@pytest.fixture(scope="module")
def made():
    """The kinds and tables as main.py, the one joint, makes them for the load."""
    return joint((SITES, 1, 1))


def universe(trains=TRAINS, couplings=COUPLINGS):
    return {"trains": copy.deepcopy(trains), "couplings": copy.deepcopy(couplings)}


def naive(u, c, readings, labels):
    """J by loops over the coupling rows and the tables, each train's rows counted afresh in its kinds' order."""
    rows, at = {}, 0
    for t, train in enumerate(u["trains"]):
        for j, label in enumerate(train["kinds"]):
            for x in range(len(c[(labels.index(label), labels.index("A1"), labels.index(label))])):
                for p in range(train["part"]):
                    rows[(t, j, x, p)], at = at, at + 1
    planes = {"value": [0], "gradient": [1, 2, 3], "pull": [4], "before": [5], "after": [6]}
    j = np.zeros((at, readings.shape[-1]), dtype=object)
    for i, ki, pi, oi, k, kk, pk, ok, m, km, pm, strength in u["couplings"]:

        def reading(t, kind, part, o, component):
            if OPERANDS[o] == "gradient":
                return readings[planes["gradient"][component] * at + rows[(t, kind, 0, part)]]
            return readings[planes[OPERANDS[o]][0] * at + rows[(t, kind, component, part)]]

        a = (
            labels.index("T1")
            if OPERANDS[oi] == "gradient"
            else labels.index(u["trains"][i]["kinds"][ki])
        )
        b = (
            labels.index("T1")
            if OPERANDS[ok] == "gradient"
            else labels.index(u["trains"][k]["kinds"][kk])
        )
        table = c[(a, b, labels.index(u["trains"][m]["kinds"][km]))]
        for x, y, z in itertools.product(*map(range, table.shape)):
            j[rows[(m, km, x, pm)]] += (
                strength * table[x, y, z] * reading(i, ki, pi, oi, y) * reading(k, kk, pk, ok, z)
            )
    return j


def loaded(made, u, gears=()):
    ks, c = made
    return load(u, {"gears": [list(g) for g in gears]}, SITES, ks, c)


def test_the_plan_contracts_as_the_naive_sum_over_the_rows_and_the_tables(made):
    """At strengths of a few bits and past 64, J is the naive sum, of Python integers whatever gears it is given."""
    ks, c = made
    labels = tuple(name.upper() for name in ks._fields)
    rng = np.random.default_rng(7)
    for shift in (0, 70):
        u = universe(couplings=[[*x[:-1], x[-1] << shift] for x in COUPLINGS])
        held, found = loaded(made, u)
        assert found == [] and held is not None
        readings = (
            rng.integers(-1 << 40, 1 << 40, (len(OPERANDS) + D - 1, ROWS, SITES)).astype(object) << 70
        )
        flat, given = (
            readings.reshape(-1, SITES),
            rng.integers(1, 1 << 30, (ROWS, SITES)).astype(object) << 80,
        )
        kept, j = given.copy(), naive(u, c, flat, labels)
        assert (contract(Plan(*held.plan), flat, given) == j).all() and (given == kept).all()
        fixed = contract(Plan(*held.plan), flat, np.zeros((ROWS, SITES), dtype=np.int64))
        assert fixed.dtype == object and (fixed == j).all()


AT = f"universe.couplings[{len(COUPLINGS)}]"  # where an edit's coupling row stands, after the universe's own


def edits():
    """One edit per refusal of the load: the edit, the departure named, or None at the refusal's edge."""

    def train(at, **fields):
        return lambda u: u["trains"][at].update(fields)

    def coupling(**fields):
        return lambda u: u["couplings"].append(row(**fields))

    return {
        "a kind none of the 24's": (
            train(1, kinds=["E1/2"]),
            "universe.trains[1].kinds[0]: 'E1/2' is none of the 24's kinds",
        ),
        "E alone": (
            train(1, kinds=["E"]),
            "universe.trains[1].kinds[0]: E has no whole basis the 24 permute",
        ),
        "a twin hand": (train(1, part=4), "universe.trains[1].part: 1, one gear, or 2, a hand, not 4"),
        "a part of 3": (train(1, part=3), "universe.trains[1].part: 1, one gear, or 2, a hand, not 3"),
        "a hand of T1": (train(1, part=2), None),
        "a channel the 24 forbid": (
            coupling(target=1),
            f"{AT}: the 24 hold no A1 x A1 -> T1",
        ),
        "the scalar product": (coupling(target=0), None),
        "a gradient of a T1 train": (
            coupling(train=1, operand=op("gradient"), target=4),
            f"{AT}: a gradient of a train not of A1",
        ),
        "a gradient of the potential's T1, its second kind": (
            coupling(train=4, kind=1, operand=op("gradient"), target=1),
            f"{AT}: a gradient of a train not of A1",
        ),
        "a gradient of the field's A1, its second kind": (
            coupling(train=5, kind=1, operand=op("gradient"), with_train=1, target=0),
            None,
        ),
        "a gradient of a T1 train on the second side": (
            coupling(with_train=1, with_operand=op("gradient"), target=4),
            f"{AT}: a gradient of a train not of A1",
        ),
        "a gradient of an A1 train": (coupling(operand=op("gradient"), with_train=1, target=0), None),
        "the before stride": (
            coupling(operand=op("before")),
            f"{AT}: before and after enter at stage 7",
        ),
        "the after stride": (
            coupling(with_operand=op("after")),
            f"{AT}: before and after enter at stage 7",
        ),
        "the pull": (coupling(operand=op("pull"), with_operand=op("pull")), None),
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
    a, b, r, go, *clocks = held.state
    assert found == [] and (a[rows - 1, site], b[rows - 1, site], r[rows - 1, site]) == (
        now,
        before,
        tooth,
    )
    assert (a[ROWS - 1, site], b[ROWS - 1, site]) == (before, now)
    assert (a.shape, b.shape, r.shape, go.shape) == ((ROWS, SITES),) * len("abrg")
    assert all(x.shape == (1, SITES) for x in clocks) and all(x.dtype == object for x in held.state)
    assert not go.any() and not any(x.any() for x in clocks)
    assert (a != 0).sum() == (b != 0).sum() == len(laid) and (r != 0).sum() == 1
    held, found = loaded(made, universe(), [(0, rows, site, now, before, 0)])
    assert held is None and found == [f"setting.gears[0]: component {rows} off train 0's {rows} rows"]


def test_a_coupling_the_table_lacks_holds_no_term_and_gives_0(made):
    ks, c = made
    u = universe(couplings=[row(target=1)])
    held, found = loaded(made, u)
    assert found == ["universe.couplings[0]: the 24 hold no A1 x A1 -> T1"]
    from tensor24.runner.load import plan, trains_of

    labels = tuple(name.upper() for name in ks._fields)
    trains, _ = trains_of(u["trains"], labels, tuple(k.shape[-1] for k in ks))
    planned, _ = plan(u["couplings"], trains, c, labels, D)
    readings = np.ones(((len(OPERANDS) + D - 1) * sum(t.rows() for t in trains), SITES), dtype=object)
    assert planned[0].size == 0 and not contract(Plan(*planned), readings, gears()).any()


def rewound(r, w, rate, gamma, dial=0):
    """One round of every gear on a ring of sites and its run back from the out: the start back exactly, or not."""
    nb, meshes = board((SITES, 1, 1))
    layout = Layout(nb, meshes, np.ones(D * SITES, dtype=object), w, rate, gamma)
    a = np.arange(SITES, dtype=object)[None, :] + 0
    clocks = 0 * a
    s = State(a, a - 1, r, 0 * a, clocks + dial, clocks, clocks)
    now, out = tick(layout, s, clocks + 1)
    return all((x == y).all() for x, y in zip(untick(layout, now, out), s, strict=True))


def test_the_two_promises_are_named_where_they_fail_and_are_the_run_backs_own_condition():
    w, gamma = 5, 4
    full = np.zeros((1, SITES), dtype=object) + gamma
    for tooth in (w, w + 1, -1):
        r = np.zeros((1, SITES), dtype=object)
        r[0, 2] = tooth
        assert promises(r, w, full, gamma) == [
            f"row 0, site 2: the fine tooth {tooth} not within [0, {w})"
        ]
        assert not rewound(r, w, full, gamma)
    r = np.zeros((1, SITES), dtype=object) + w - 1
    assert promises(r, w, full, gamma) == [] and rewound(r, w, full, gamma)
    rate = full + 0
    rate[0, 3] = gamma + gamma
    assert promises(0 * r, w, rate, gamma) == [
        f"site 3: the rate {gamma + gamma} not within [0, the full rate {gamma}]"
    ]
    assert not rewound(0 * r, w, rate, gamma)
    rate[0, 3] = -1
    assert promises(0 * r, w, rate, gamma) == [
        f"site 3: the rate -1 not within [0, the full rate {gamma}]"
    ]
    assert not rewound(0 * r, w, 0 * full - 1, gamma)  # every rate at -1: k is -1, no bit
    edge = full + 0  # at the dial's top, Gamma - 1, the full rate gives k = 1 and one past it k = 2
    assert rewound(0 * r, w, edge, gamma, gamma - 1)
    edge[0, 3] = gamma + 1
    assert not rewound(0 * r, w, edge, gamma, gamma - 1)
    assert promises(0 * r, w, edge, gamma) == [
        f"site 3: the rate {gamma + 1} not within [0, the full rate {gamma}]"
    ]


def renamed(made, scale=lambda strength, target: strength):
    """The trains in other orders give one plan: J moves with its trains' rows; the scale is how the load reads a strength."""

    def scaled(couplings):
        return [[*x[:-1], scale(x[-1], x[8])] for x in couplings]

    base, _ = loaded(made, universe(couplings=scaled(COUPLINGS)))
    rows = sum(t.rows() for t in base.trains)
    planes = len(OPERANDS) + D - 1
    readings = (
        np.random.default_rng(3).integers(-1 << 30, 1 << 30, (planes * rows, SITES)).astype(object)
    )
    j = contract(Plan(*base.plan), readings, gears(rows))
    for order in [(5, 4, 3, 2, 1, 0), (1, 0, 5, 4, 2, 3)]:
        place = {old: new for new, old in enumerate(order)}
        couplings = [
            [place[x[0]], *x[1:4], place[x[4]], *x[5:8], place[x[8]], *x[9:]] for x in COUPLINGS
        ]
        moved, found = loaded(made, universe([TRAINS[o] for o in order], scaled(couplings)))
        mapping = np.concatenate(
            [
                np.arange(base.trains[o].first, base.trains[o].first + base.trains[o].rows())
                for o in order
            ]
        )
        shuffled = readings.reshape(planes, rows, SITES)[:, mapping].reshape(-1, SITES)
        if found or not (contract(Plan(*moved.plan), shuffled, gears(rows)) == j[mapping]).all():
            return False
    return True


def test_the_rename_law_holds_and_fails_where_a_strength_is_read_by_its_target_trains_place(made):
    assert renamed(made)
    assert not renamed(made, lambda strength, target: strength * (target + 1))


def test_the_files_the_checker_holds_load_or_are_named_and_none_raises(made):
    """Sofer's fuzz of stage 6: no couplings or no gears key loads as none, and a board past one array is named."""
    ks, c = made
    bare = universe()
    bare.pop("couplings")
    assert load(bare, {}, SITES, ks, c)[1] == []
    held, found = load(universe(), {"gears": []}, 1 << 64, ks, c)
    assert held is None and len(found) == 1 and found[0].startswith(f"piece.shape: {ROWS} rows at")


def test_a_board_the_machine_cannot_hold_is_named(made, monkeypatch):
    """Whichever of the lay's five arrays the machine's memory refuses, the board is named and nothing raises."""
    ks, c = made
    zeros = np.zeros
    for after in range(
        len("abrgc")
    ):  # a, b, r, the going and the clocks: `after` made, the next refused
        asked = []

        def refused(*args, after=after, asked=asked, **kwargs):
            asked.append(args)
            if len(asked) > after:
                raise MemoryError("no room")
            return zeros(*args, **kwargs)

        monkeypatch.setattr(np, "zeros", refused)
        held, found = load(universe(), {"gears": []}, SITES, ks, c)
        assert len(asked) == after + 1 and held is None
        assert found == [
            f"piece.shape: {ROWS} rows at {SITES} sites, more than the arrays of this machine hold (no room)"
        ]
