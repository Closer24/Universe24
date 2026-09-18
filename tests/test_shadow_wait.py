"""The shadow's wait, a declared option (shadow-wait-v1; Highlights 5.4, the model
owner's paragraph "The shadow's wait, a declared option to confront" of
2026-09-18; feature 16e).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The shadow's wait")
before the first run. A world MAY declare `shadow_wait: {"per_quantum": n or
[n, d], "reads": "thing" or "field"}`; absent, a shadow owes nothing and a
world's record is byte for byte the record of main (a). With the reading `thing`
a share read by a thing (it pushes and turns back) owes n / d intervals per
whole quantum of the push it gave before it leaves that Node (b); with `field` a
share owes n / d intervals for every whole quantum of another owner's shadows
that arrived at the Node it crosses this interval, the parked ninths never
counting (c); the count is exact, d spent per interval, a debt below one
interval paid by the interval (d); the dense layer and the engine alone agree
(e). The worlds are those of the law of the bit and the return as a field.
"""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import BIT_SHADOW, SHADOW_WAIT
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_bit_law import HEADINGS, MINUS_X, X, body, document, run, shadow
from .test_return_field import moving_at

ROOT = Path(__file__).resolve().parents[1]
THING = {"per_quantum": 1, "reads": "thing"}
FIELD = {"per_quantum": 1, "reads": "field"}
PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z = [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]


def world_b(amount, option=None, ticks=6):
    """The geometry of test_return_field (b): A (owner 3) at (0,2,2), C (owner 5)
    and B (owner 4) with the table {"m": 1} at (1,2,2) and (2,2,2); A's shadow of
    `amount` fresh at (1,2,2) on +X, pushing B by (amount, 0, 0) at tick 1."""
    doc = document(
        ticks=ticks,
        bodies=[
            body((0, 2, 2), 3, amount=81),
            # charge-per-thing-v1 (2026-09-18): a pushed body multiplies A's
            # message (-81 / 81) by its whole charge, -1, one unit per quantum.
            body((1, 2, 2), 5, table={"m": 1}, amount=1000, charge=-1),
            body((2, 2, 2), 4, table={"m": 1}, amount=1000, charge=-1),
        ],
        shadows=[shadow((1, 2, 2), X, amount=amount, owner=3, steps=0)],
    )
    if option is not None:
        doc["shadow_wait"] = option
    return doc


def world_c(second, option=None, ticks=12):
    """Two owners' fields crossing at (4,2,2): P (owner 2) at (0,2,2) and Q (owner
    3) at (9,2,2), bodies without a table; P's share of 9 fresh at (3,2,2) on +X,
    at (4,2,2) after tick 1. Q's `second`: "arrival", a shadow of 3 fresh at
    (5,2,2) on -X, at (4,2,2) with P's; "parked", a shadow of 2 with a Link
    walked at (4,2,2), mixed in the cycle of tick 1 into its ninths (8 on +X, 2
    on each other heading), nothing of it arriving when P's share mixes."""
    if second == "arrival":
        other = shadow((5, 2, 2), MINUS_X, amount=3, owner=3, steps=0)
    else:
        other = shadow((4, 2, 2), MINUS_X, amount=2, owner=3, steps=1)
    doc = document(
        ticks=ticks,
        bodies=[body((0, 2, 2), 2, amount=81), body((9, 2, 2), 3, amount=81)],
        shadows=[shadow((3, 2, 2), X, amount=9, owner=2, steps=0), other],
    )
    if option is not None:
        doc["shadow_wait"] = option
    return doc


def waiting_at(inventory, position):
    """The shares at a Node, on their way or waiting: (heading, amount, owner,
    steps, owed), sorted."""
    return sorted(
        (HEADINGS[r.heading], r.amount, r.owner, r.steps, r.owed)
        for r in inventory.get(tuple(position), ((),))[0]
        if r.detector == BIT_SHADOW and not r.parked
    )


def momenta(result, index):
    """One body's momentum on x per tick."""
    return [b[index][0] for b in result["bodies_per_tick"]]


def test_without_the_key_the_record_is_byte_identical_to_main(tmp_path):
    """(a): the ring of examples/nature for eight ticks has the digests of
    test_lanes (f), main at ffa4a56 (2026-09-18); no key, no record of the
    option; the option's malformed forms are refused; declared, recorded."""
    out = tmp_path / "ring"
    run_initialization(ROOT / "examples/nature/ring.json", out, ticks=8)
    digests = {
        name: hashlib.sha256((out / name).read_bytes()).hexdigest()
        for name in ("events.jsonl", "state.json")
    }
    assert digests == {
        "events.jsonl": "091f6666d75ec307bf5d13f3f82123fab34c1d68524bade9b59d9fdbdcf20420",
        "state.json": "830345cd108b11d540bdac3639126aae482c330330cb31eeb2f035e56f20fd40",
    }
    metadata = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert "shadow_wait" not in metadata and "shadow_wait_option" not in metadata
    initial = parse_initial_state(world_b(1))
    assert initial.shadow_wait is None and initial.shadow_wait_reads == ""
    definition = initial.spatial_fields[0]
    assert (
        definition.shadow_wait_numerator,
        definition.shadow_wait_denominator,
        definition.shadow_wait_reads,
    ) == (0, 1, "")
    for option, message in (
        ({"per_quantum": 1}, "missing keys"),
        ({"per_quantum": 1, "reads": "mass"}, "shadow-wait-v1"),
        ({"per_quantum": [1, 0], "reads": "thing"}, "d at least 1"),
        ({"per_quantum": -1, "reads": "field"}, "per_quantum"),
        ({"per_quantum": 1, "reads": "thing", "extra": 0}, "unknown keys"),
    ):
        with pytest.raises(ValueError, match=message):
            parse_initial_state(world_b(1, option))
    path = tmp_path / "b.json"
    path.write_text(json.dumps(world_b(1, THING)), encoding="utf-8")
    run_initialization(path, tmp_path / "b", ticks=2)
    metadata = json.loads((tmp_path / "b" / "run.json").read_text(encoding="utf-8"))
    assert metadata["shadow_wait"] == SHADOW_WAIT == "shadow-wait-v1"
    assert metadata["shadow_wait_option"] == {"per_quantum": [1, 1], "reads": "thing"}


def test_a_share_read_by_a_thing_owes_the_wait_before_it_leaves():
    """(b): n = 1 read by a thing: the share turned back at B stays one interval,
    and C, then B again, are pushed one tick later than without the key."""
    control = run(world_b(1), 6)
    waited = run(world_b(1, THING), 6)
    assert momenta(control, 2) == [1, 1, 2, 2, 3, 3] and momenta(control, 1) == [0, 1, 1, 2, 2, 3]
    assert momenta(waited, 2) == [1, 1, 1, 1, 2, 2] and momenta(waited, 1) == [0, 0, 1, 1, 1, 1]
    at = waited["inventories"]
    assert waiting_at(at[0], (2, 2, 2)) == [(MINUS_X, 1, 3, 0, 1)]
    assert waiting_at(at[1], (2, 2, 2)) == [(MINUS_X, 1, 3, 0, 0)]
    assert waiting_at(at[1], (1, 2, 2)) == []
    assert waiting_at(at[2], (1, 2, 2)) == [(X, 1, 3, 0, 1)]
    assert waiting_at(at[2], (2, 2, 2)) == []
    assert waiting_at(at[3], (1, 2, 2)) == [(X, 1, 3, 0, 0)]
    assert waiting_at(at[4], (2, 2, 2)) == [(MINUS_X, 1, 3, 0, 1)]
    assert moving_at(at[2], (1, 2, 2)) == [(X, 1, 0, 1, -1, (-2, 0, 0))]
    assert moving_at(at[4], (2, 2, 2)) == [(MINUS_X, 1, 0, 0, 1, (-3, 0, 0))]
    # A waiting share is on the board: the books close, nothing sourced.
    for result in (control, waited):
        assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
        assert result["shadows"] == [1] * 6


@pytest.mark.parametrize("second", ["arrival", "parked"])
def test_a_share_owes_the_wait_for_another_owners_quanta_at_the_node_it_crosses(second):
    """(c): n = 1 read by the field: every departure of an owner from a Node owes
    an interval per whole quantum of the other owners' shadows that arrived
    there; the parked ninths of another owner count nothing."""
    control = run(world_c(second), 12)
    waited = run(world_c(second, FIELD), 12)
    at = waited["inventories"]
    if second == "arrival":
        assert waited["shadows"][0] == 12
        departures = [
            (MINUS_X, 4, 2),
            (X, 1, 2),
            (PLUS_Y, 1, 2),
            (MINUS_Y, 1, 2),
            (PLUS_Z, 1, 2),
            (MINUS_Z, 1, 2),
        ]
        for t in (2, 3, 4):
            assert waiting_at(at[t - 1], (4, 2, 2)) == sorted(
                [(h, a, o, 0, 4 - t) for h, a, o in departures] + [(X, 1, 3, 0, 10 - t)]
            )
        one_link_on = {
            (3, 2, 2): [(MINUS_X, 4, 2, 1, 0)],
            (5, 2, 2): [(X, 1, 2, 1, 0)],
            (4, 3, 2): [(PLUS_Y, 1, 2, 1, 0)],
            (4, 1, 2): [(MINUS_Y, 1, 2, 1, 0)],
            (4, 2, 3): [(PLUS_Z, 1, 2, 1, 0)],
            (4, 2, 1): [(MINUS_Z, 1, 2, 1, 0)],
        }
        for position, expected in one_link_on.items():
            assert waiting_at(at[4], position) == expected, position
            without = expected if position != (5, 2, 2) else [(X, 1, 2, 1, 0), (X, 1, 3, 1, 0)]
            assert waiting_at(control["inventories"][1], position) == without, position
        assert waiting_at(at[4], (4, 2, 2)) == [(X, 1, 3, 0, 5)]
        assert waiting_at(at[9], (4, 2, 2)) == [(X, 1, 3, 0, 0)]
        assert waiting_at(at[10], (4, 2, 2)) == []
        assert waiting_at(at[10], (5, 2, 2)) == [(X, 1, 3, 1, 0)]
        ninths = sorted(
            (tuple(e["heading"]), e["amount"])
            for e in waited["snapshot"]["parked"]
            if tuple(e["position"]) == (4, 2, 2) and e["owner"] == 3
        )
        assert [amount for _, amount in ninths] == [3] * 6
    else:
        assert waited["shadows"][0] == 11
        ninths = sorted(
            (tuple(e["heading"]), e["amount"])
            for e in waited["snapshot"]["parked"]
            if tuple(e["position"]) == (4, 2, 2) and e["owner"] == 3
        )
        assert (tuple(X), 8) in ninths and sorted(a for _, a in ninths) == [2, 2, 2, 2, 2, 8]
        assert waiting_at(at[0], (4, 2, 2)) == [(X, 9, 2, 1, 0)]
        assert waiting_at(at[1], (4, 2, 2)) == []
        assert waiting_at(at[1], (3, 2, 2)) == [(MINUS_X, 4, 2, 1, 0)]
        for key in ("inventories", "ledgers", "momentum", "bodies_per_tick", "shadows"):
            assert waited[key] == control[key], key
    for result in (control, waited):
        assert all(entry["balanced"] for entry in result["ledgers"])


def test_the_count_is_exact_d_spent_per_interval():
    """(d): [11, 9] read by a thing: a push of 9 quanta owes 99 ninths, eleven
    intervals exactly; a push of 1 owes 11, two intervals, the 2 / 9 left below
    one interval paid by the interval."""
    option = {"per_quantum": [11, 9], "reads": "thing"}
    assert parse_initial_state(world_b(1, option)).shadow_wait == (11, 9)
    nine = run(world_b(9, option, ticks=14), 14)
    assert momenta(nine, 2) == [9] * 14 and momenta(nine, 1) == [0] * 12 + [9] * 2
    owed = [waiting_at(inv, (2, 2, 2)) for inv in nine["inventories"]]
    assert owed[0] == [(MINUS_X, 9, 3, 0, 99)] and owed[1] == [(MINUS_X, 9, 3, 0, 90)]
    assert owed[11] == [(MINUS_X, 9, 3, 0, 0)] and owed[12] == []
    assert waiting_at(nine["inventories"][12], (1, 2, 2)) == [(X, 9, 3, 0, 99)]
    one = run(world_b(1, option, ticks=14), 14)
    assert momenta(one, 2) == [1] * 6 + [2] * 6 + [3] * 2
    assert momenta(one, 1) == [0] * 3 + [1] * 6 + [2] * 5
    owed = [waiting_at(inv, (2, 2, 2)) for inv in one["inventories"]]
    assert owed[:4] == [
        [(MINUS_X, 1, 3, 0, 11)],
        [(MINUS_X, 1, 3, 0, 2)],
        [(MINUS_X, 1, 3, 0, 0)],
        [],
    ]
    assert waiting_at(one["inventories"][3], (1, 2, 2)) == [(X, 1, 3, 0, 11)]
    for result in (nine, one):
        assert all(entry["balanced"] for entry in result["ledgers"])


@pytest.mark.parametrize("name", ["b", "c_arrival", "c_parked"])
def test_the_dense_layer_agrees_with_the_engine(name):
    """(e): the worlds of (b) and (c) under the engine alone and under the shadow
    layer (the default where admitted): one board, one ledger, one momentum on
    every body and shadow; under the field reading the Node where two owners'
    shadows meet is the engine's."""
    doc, ticks = {
        "b": (world_b(1, THING), 6),
        "c_arrival": (world_c("arrival", FIELD), 12),
        "c_parked": (world_c("parked", FIELD), 12),
    }[name]
    assert parse_initial_state(deepcopy(doc)).dense_field
    engine = run(deepcopy(doc) | {"dense_field": False}, ticks)
    dense = run(deepcopy(doc), ticks)
    for key in ("inventories", "ledgers", "momentum", "bodies_per_tick", "shadows"):
        assert engine[key] == dense[key], key
    assert engine["snapshot"]["parked"] == dense["snapshot"]["parked"]
    if name == "c_arrival":
        with Simulation(parse_initial_state(deepcopy(doc))) as world:
            for _ in range(2):
                world.step()
            region = world._spatial.dense
            assert region is not None and region.owner[(4, 2, 2)] == 1
