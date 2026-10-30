"""Tensor24's load, the Node-clock's initialization: the board and its Meshes, every gear on its train's rows, the
square found by its kinds' character, each refusal named, and the round's promise at its edges."""

import itertools
import json
from pathlib import Path

import numpy as np

from tensor24.main import made as joint
from tensor24.runner import load as loading
from tensor24.runner.board import board
from tensor24.runner.files import AXES, held_departures, sites_of, vocabulary
from tensor24.runner.load import geometry, load, star
from tensor24.runner.run import promises
from tests import frame

UNIVERSE = Path(__file__).resolve().parents[1] / "examples" / "tensor24" / "universe.json"

SHAPE = (3, 4, 5)  # a board of sides that differ, so no two axes are taken for each other
TRAINS = [
    {"name": "light", "kinds": ["A1"], "part": 2},
    {"name": "spin", "kinds": ["T1"], "part": 1},
    {"name": "axial", "kinds": ["A2"], "part": 1},
    {"name": "stress", "kinds": ["T2"], "part": 1},
    {"name": "potential", "kinds": ["A1", "T1"], "part": 2},
    {"name": "field", "kinds": ["T1", "A1"], "part": 1},
]
SQUARE, LIKE = (
    ("A1", "T1", "A1", "E", "T2"),
    ("T1", "T1", "T1", "A1"),
)  # the four-vector's square, and as many rows
SITE, WIDE = 3, 1 << 70  # where the gears are laid, and their counts, past 64 bits


def loaded(made, trains, gears=()):
    """The files held against the engine's kinds, then loaded, as the run does: the departures, or the loaded and none."""
    kinds, c, square = made
    universe, setting = {"trains": [dict(t) for t in trains]}, {"gears": [list(g) for g in gears]}
    found = held_departures(universe, setting, vocabulary(kinds, square))
    held, found = (None, found) if found else load(universe, setting, sites_of(SHAPE), kinds, c, square)
    return (None if found else held), found


def no_room(*args, **kwargs):
    raise MemoryError("no room")


def test_the_load_lays_the_board_and_every_gear_on_its_trains_rows_and_names_each_refusal(monkeypatch):
    """Yes: the board and its Meshes as numpy wraps them, every gear on its train's rows past 64 bits, the square found
    by its kinds' character in every order, no term of J. No: each refusal named, with nothing loaded and no raise,
    and a fine tooth at its teeth or below 0 named by the round's promise."""
    nb, made = board(SHAPE), joint(star(len(AXES)))
    spokes, meshes = geometry(nb, len(SHAPE))
    assert (nb == frame.board(SHAPE)).all() and (spokes == frame.spokes(len(SHAPE))).all()
    assert (meshes == frame.meshes_of(nb)).all()
    labels, dims, _ = vocabulary(made[0], made[-1])
    rows = [sum(dims[labels.index(k)] for k in t["kinds"]) * t["part"] for t in TRAINS]
    first, last = (
        (0, rows[0] - 1, SITE, WIDE, WIDE + 1, WIDE + 2),
        (len(TRAINS) - 1, rows[-1] - 1, SITE, WIDE + 1, WIDE, 0),
    )
    held, found = loaded(made, TRAINS, laid := [first, last])
    a, b, r, rd = held.state
    pairs = list(itertools.combinations(held.state, 2))
    # the eighth to tenth reviews (927071a14, 0ff2ae0dc, fc8c810ff): a gear off a later train, its tooth, its b laid
    # at every site, a bound read on train 0 and arrays of 64 bits each passed every test
    assert found == [] and all(
        x.shape == (sum(rows), sites_of(SHAPE)) and x.dtype == object for x in held.state
    )
    _, row, site, *counts = first
    assert (a[row, site], b[row, site], r[row, site]) == tuple(counts)
    assert (a[sum(rows) - 1, site], b[sum(rows) - 1, site]) == (
        WIDE + 1,
        WIDE,
    )  # the last train's last row
    assert (a != 0).sum() == (b != 0).sum() == len(laid) and (r != 0).sum() == 1 and not rd.any()
    assert not any(np.shares_memory(x, y) for x, y in pairs) and not len(held.potential[0])
    integers = json.loads(UNIVERSE.read_text(encoding="utf-8"))["integers"]
    universe, rate = {"integers": integers, "trains": TRAINS}, integers["full_rate"]
    # den Gamma^2 from the files' integers, and the star's Spokes, counted
    grip, spokes = integers["den"] * rate * rate, len(frame.spokes(len(SHAPE)))
    _, _, _, grips, (rest, *ones), *_ = loading.laid_out(universe, list(SHAPE), held)
    # every row's teeth at rest 6 den Gamma^2, each grip den Gamma^2, s, T_k and T_d at 1: the audit found a loader
    # with the teeth at rest 7 den Gamma^2, or every grip 2 den Gamma^2, passing every test on main
    assert (rest == spokes * grip).all() and (grips == grip).all() and all((x == 1).all() for x in ones)
    for kinds in [*sorted(set(itertools.permutations(SQUARE))), LIKE]:
        held, found = loaded(made, [*TRAINS, {"name": "metric", "kinds": list(kinds), "part": 1}])
        assert found == [] and held.trains.square.tolist() == [0] * len(TRAINS) + [int(kinds != LIKE)]
    refused = [
        ([{**TRAINS[1], "kinds": ["E1/2"]}], [], "'E1/2' is none of the 24's kinds"),
        ([{**TRAINS[1], "kinds": ["E"]}], [], "'E' has no whole basis the 24 permute"),
        # f85c271d0's case: the square's kinds at part 2, their character twice the square's, so E stands outside it
        ([{**TRAINS[1], "kinds": list(SQUARE), "part": 2}], [], "'E' has no whole basis the 24 permute"),
        ([TRAINS[0]], [(0, rows[0], 0, 1, 0, 0)], f"component {rows[0]} off train 0's {rows[0]} rows"),
    ]
    for trains, gears, named in refused:
        held, found = loaded(made, trains, gears)
        assert held is None and any(named in line for line in found), found
    # the eighth review's fifth (927071a14), carried to the fine tooth at 8b43839a1, a bound one past survived: the
    # promise names a tooth at its teeth and one below 0, sites 1 and 2, and holds one at w - 1, here past 64 bits
    assert promises(np.array([[WIDE - 1, WIDE, -1]], dtype=object), WIDE) == [
        f"row 0, site 1: the fine tooth {WIDE} not within [0, {WIDE})",
        f"row 0, site 2: the fine tooth -1 not within [0, {WIDE})",
    ]
    kinds, c, square = made
    _, found = load({"trains": TRAINS}, {"gears": []}, 1 << 64, kinds, c, square)
    assert len(found) == 1 and found[0].startswith(f"piece.shape: {sum(rows)} rows at")
    # the ninth review (0ff2ae0dc): a MemoryError dropped from the lay's guard passed every test
    monkeypatch.setattr(np, "zeros", no_room)
    _, found = load({"trains": TRAINS}, {"gears": []}, sites_of(SHAPE), kinds, c, square)
    named = f"piece.shape: {sum(rows)} rows at {sites_of(SHAPE)} sites, more than the arrays of this machine hold"
    assert found == [f"{named} (no room)"]
