"""Tensor24's load, the Node-clock's initialization: the board and its Meshes, every gear on its train's rows, the square found by its kinds' character
with its 0i rows odd, the chosen strengths read, each refusal named, the round's promise at the edges of its dial, and the plans laid from the kinds' tables."""

import itertools
import json
from pathlib import Path

import numpy as np

from tensor24 import main
from tensor24.engine.state import State
from tensor24.runner import load as loading
from tensor24.runner.board import board
from tensor24.runner.files import AXES, held_departures, sites_of, vocabulary
from tensor24.runner.run import promises
from tests import frame

UNIVERSE = Path(__file__).resolve().parents[1] / "examples" / "tensor24" / "universe.json"
INTEGERS = json.loads(UNIVERSE.read_text(encoding="utf-8"))["integers"]
SHAPE = (3, 4, 5)  # a board of sides that differ, so no two axes are taken for each other
SITES = sites_of(SHAPE)
NAMES, PARTS = "light spin axial stress potential field".split(), (2, 1, 1, 1, 2, 1)
KINDS = (["A1"], ["T1"], ["A2"], ["T2"], ["A1", "T1"], ["T1", "A1"])  # each kind but E, two of two
TRAINS = [{"name": n, "kinds": k, "part": p} for n, k, p in zip(NAMES, KINDS, PARTS, strict=True)]
SQUARE, LIKE = ("A1", "T1", "A1", "E", "T2"), ("T1", "T1", "T1", "A1")  # the square, and as many rows
METRIC = {"name": "metric", "kinds": list(SQUARE), "part": 1}
HAND, PAIR = {"name": "held", "kinds": ["A1", "A2"], "part": 1}, {"kinds": ["T1", "T2"], "part": 1}
FIVE = [TRAINS[0], METRIC, HAND, {"name": "giver", **PAIR}, {"name": "taker", **PAIR}]  # the click world
CHOSEN = {"key": 1, "push": 0, "notch": 0, "hold": 0, "tie": 0, "mesh": 0}  # read from the file
SITE, WIDE = 3, 1 << 70  # where the gears are laid, and their counts, past 64 bits
MADE = main.made(loading.star(len(AXES)))  # the kinds, tables and square by main.py's one joint


def loaded(trains, gears=(), chosen=CHOSEN, sites=SITES):
    """The files held against the engine's kinds, then loaded, as the run does: the departures, or the loaded and none."""
    kinds, c, square = MADE
    universe = {"integers": INTEGERS, "trains": [dict(t) for t in trains], "chosen": dict(chosen)}
    setting = {"gears": [list(g) for g in gears]}
    found = held_departures(universe, setting, vocabulary(kinds, square))
    held, found = (None, found) if found else loading.load(universe, setting, sites, kinds, c, square)
    return (None if found else held), found


def test_the_load_lays_the_board_and_every_gear_on_its_trains_rows_and_names_each_refusal(monkeypatch):
    """Yes: the board and its Meshes as numpy wraps them, every gear on its train's rows past 64 bits, the square by its kinds' character in every order
    with its 0i rows odd, the chosen key and notch read, no term of J but the notch's. No: each refusal named with nothing loaded and no raise (the reviews'
    gear off a later train, its tooth, its b at every site, a bound read on train 0, 64-bit arrays, the MemoryError dropped from the lay's guard, each passed every test once); a tooth at or below its dial named by the promise."""
    spokes, meshes = loading.geometry(nb := board(SHAPE), len(SHAPE))
    assert (nb == frame.board(SHAPE)).all() and (spokes == frame.spokes(len(SHAPE))).all()
    assert (meshes == frame.meshes_of(nb)).all()
    labels, dims, _ = vocabulary(MADE[0], MADE[-1])
    rows = [sum(dims[labels.index(k)] for k in t["kinds"]) * t["part"] for t in TRAINS]
    _, row, _, *counts = light = (0, rows[0] - 1, SITE, WIDE, WIDE + 1, WIDE + 2)
    held, found = loaded(TRAINS, laid := [light, (len(rows) - 1, rows[-1] - 1, SITE, WIDE + 1, WIDE, 0)])
    a, b, r, rd, k = held.state
    assert found == [] and all(x.dtype == object for x in held.state) and not held.potential[0].any()
    assert all(x.shape == (sum(rows), SITES) for x in (a, b, r, rd)) and k.shape == (len(TRAINS), SITES)
    assert (a[row, SITE], b[row, SITE], r[row, SITE]) == tuple(counts)  # the light's last row, as laid
    assert (a[-1, SITE], b[-1, SITE]) == (WIDE + 1, WIDE) and not k.any()  # the last train's last row
    assert (a != 0).sum() == (b != 0).sum() == len(laid) and (r != 0).sum() == 1 and not rd.any()
    assert not any(np.shares_memory(*pair) for pair in itertools.combinations(held.state, 1 + 1))
    assert (held.click[-1] == CHOSEN["key"]).all() and held.click[-1].shape == (len(TRAINS), 1)
    universe, rate = {"integers": INTEGERS, "trains": TRAINS, "chosen": CHOSEN}, INTEGERS["full_rate"]
    grip, spokes = INTEGERS["den"] * rate * rate, len(frame.spokes(len(SHAPE)))  # den Gamma^2
    _, _, _, grips, (rest, *ones, even), *_ = loading.laid_out(universe, list(SHAPE), held)
    # the teeth at rest 6 den Gamma^2, each grip den Gamma^2, s, T_k, T_d at 1 (the audit's loaders at 7 den Gamma^2 and at 2 den Gamma^2 a grip passed every test); no square: every row even
    assert (rest == spokes * grip).all() and (grips == grip).all() and all((x == 1).all() for x in ones)
    assert (even == 1).all()
    for kinds in [*sorted(set(itertools.permutations(SQUARE))), LIKE]:
        held, found = loaded([*TRAINS, {**METRIC, "kinds": list(kinds)}])
        assert found == [] and held.trains.square.tolist() == [0] * len(TRAINS) + [int(kinds != LIKE)]
    # the square's 0i rows, the three after its 00 slot, odd under the mirror, every other row even; the notch's monomials at the chosen h: 2 h on the 00 slot squared, h on each pair of ii slots, on the square train alone
    held, _ = loaded([*TRAINS, METRIC], chosen={**CHOSEN, "notch": 3})
    _, _, _, _, (*_, even), *_ = loading.laid_out(universe, list(SHAPE), held)
    zero = int(held.trains.first[-1])
    assert even[zero + 1 : zero + 4].tolist() == [[0]] * 3
    assert np.delete(even[:, 0], range(zero + 1, zero + 4)).tolist() == [1] * (sum(rows) + 7)
    factor, (one, two, *_) = held.potential
    named = set(one[factor != 0].tolist()) | set(two[factor != 0].tolist())  # the square's legs alone
    assert sorted(set(factor.tolist())) == [0, 3, 6] and named <= set(range(zero, zero + 10))
    refused = [
        ([{**TRAINS[1], "kinds": ["E1/2"]}], [], "'E1/2' is none of the 24's kinds"),
        ([{**TRAINS[1], "kinds": ["E"]}], [], "'E' has no whole basis the 24 permute"),
        ([{**TRAINS[1], "kinds": list(SQUARE), "part": 2}], [], "'E' has no whole basis the 24 permute"),
        ([TRAINS[0]], [(0, rows[0], 0, 1, 0, 0)], f"component {rows[0]} off train 0's {rows[0]} rows"),
        ([*TRAINS, METRIC, {**METRIC, "name": "twin"}], [], "one metric family: 'metric', 'twin'"),
    ]
    for trains, gears, named in refused:
        held, found = loaded(trains, gears)
        assert held is None and any(named in line for line in found), found
    # the promise names a tooth at its edge's dial and one below it, sites 1 and 2, and holds one at D - 1, past 64 bits (the eighth review's fifth, carried to the fine tooth at 8b43839a1)
    d, w, off = 2 * WIDE, WIDE + 0 * np.arange(3, dtype=object)[None, :], {1: 2 * WIDE, 2: -2 * WIDE - 1}
    held = State(w + 1, w, np.array([[d - 1, off[1], off[2]]], dtype=object), 0 * w, 0 * w)
    dial = f"not within the edge's dial [-{d}, {d}) of the teeth {WIDE} and {WIDE}"
    assert promises(held, w, w) == [f"row 0, site {x}: the tooth {t} {dial}" for x, t in off.items()]
    _, found = loaded(TRAINS, sites=1 << 64)
    assert len(found) == 1 and found[0].startswith(f"piece.shape: {sum(rows)} rows at")
    monkeypatch.setattr(np, "zeros", lambda *a, **k: (_ for _ in ()).throw(MemoryError("no room")))
    _, found = loaded(TRAINS)
    named = f"piece.shape: {sum(rows)} rows at {SITES} sites, more than the arrays of this machine hold"
    assert found == [f"{named} (no room)"]


def test_the_plans_are_laid_from_the_kinds_tables_the_passings_pairs_and_the_coupling_familys_frame():
    """Yes: the passing's pairs are each train's rows, kind by kind and part by part, through its kinds' table with itself onto A1 at the table's entry, the
    target the train, each pair once, the key the universe's; on the click world's shape the held hand and the tied hands are found by character, the held rows' own spring is
    rest and their grips 0, the tie hold f on the dot product's diagonal, the hands' tie tie on it once, light in no monomial. No: no pair crosses two trains or two parts; the tie off the diagonal and the hands' tie the other way are 0; the two tied hands swapped in the file lay the same plan and grips."""
    held, found = loaded(trains := [*TRAINS, METRIC])
    one, two, entry, train, key = (x.tolist() for x in held.click)
    got = dict(zip(zip(one, two, train, strict=True), entry, strict=True))
    wanted, a1 = {}, [name.upper() for name in MADE[0]._fields].index("A1")
    for n, t in enumerate(held.trains[n] for n in range(len(trains))):
        for j, (k, d) in enumerate(zip(t.kinds, t.dims, strict=True)):
            at = t.first + sum(t.dims[:j]) * t.part
            for p, x, y in itertools.product(range(t.part), range(d), range(d)):
                wanted[at + x * t.part + p, at + y * t.part + p, n] = MADE[1][k, k, a1][0][x, y]
    assert found == [] and len(got) == len(one) and got == wanted and key == [[1]] * len(trains)
    # term 6's frame on light, the square, the held hand (A1, A2) and two tied (T1, T2) hands, at hold 1 and tie 1
    chosen = {**CHOSEN, "hold": 1, "tie": 1}
    held, found = loaded(FIVE, chosen=chosen)
    light, _, hand, giver, taker = (held.trains[n] for n in range(len(FIVE)))
    span = lambda t: range(t.first, t.first + t.rows())  # noqa: E731
    factor, legs = held.potential
    kept = [x[factor != 0].tolist() for x in (factor, *legs)]  # the monomials with a factor
    v = dict(zip(zip(*kept[1:], strict=True), kept[0], strict=True))
    laid = main.layout({"integers": INTEGERS, "trains": FIVE, "chosen": chosen}, list(SHAPE), held)
    rest, f = int(laid.gearing.rest[0, 0]), int(laid.gearing.rest[0, 0]) // INTEGERS["full_rate"]
    flags = (held.trains.held.tolist(), held.trains.tied.tolist(), held.trains.gripped.tolist())
    assert flags == ([0, 0, 1, 0, 0], [0, 0, 0, 1, 1], [1, 1, 0, 1, 1])  # held, tied, gripped
    assert found == [] and len(v) == len(kept[0]) and all(v[k, k, -1, -1] == rest for k in span(hand))
    assert all(v[x, x, k, k] == f for x in span(giver) for k in span(hand))  # the tie, hold x f x 1
    both = list(zip(span(giver), span(taker), strict=True))  # the hands' rows, component by component
    assert all(v[x, y, -1, -1] == 1 and (y, x, -1, -1) not in v for x, y in both)  # the hands' tie, once
    assert not any(x != y and {x, y} <= set(span(giver)) for x, y, *_ in v)  # the tie off the diagonal
    assert not any(set(leg) & set(span(light)) for leg in v)  # light untied
    assert set(laid.grip[list(span(hand))].ravel().tolist()) == {0}  # the held hand holds no Mesh
    assert (np.delete(laid.grip, list(span(hand)), axis=0) == laid.grip[0, 0]).all()
    swapped, _ = loaded([*FIVE[:3], *reversed(FIVE[3:])], chosen=chosen)  # the two tied hands swapped
    pot, same = (swapped.potential[0], *swapped.potential[1]), (factor, *legs)
    assert all(np.array_equal(x, y) for x, y in zip(pot, same, strict=True))
