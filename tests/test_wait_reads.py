"""The wait reads the amplitude, a declared coupling option (wait-reads-v1;
Highlights 5.4, the model owner's paragraph "The wait reads the amplitude, a
coupling to derive" of 2026-09-18; derivations round 5, sections 34 to 38;
feature 16f).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The wait reads the
amplitude") before the first run. A world MAY declare `wait_reads`: "amount"
(the default: the wait of point 23 counts the whole quanta of push read, as
today) or "amplitude": the wait counts the size of the coherent sum of the
pushing owner's shadows arriving at the thing's Node this interval, the sum the
mixing forms, in whole units of amplitude (32 at the engine's scale is one
quantum's), read as the push reads the amount (point 16); the push itself reads
the amount as before. (a) absent or amount: byte-identical to main; (b) 81
quanta of one owner in phase give amplitude 9, so a thing of content 1 with w =
1 owes 9 intervals where amount owes 81, 9 quanta give 3, two owners' shares do
not sum; (c) one owner's shares in antiphase from two Ports give the size of
their difference, 192 of 32nds for 81 and 9, six units against 90 quanta; (d)
the dense layer and the engine alone agree.

Part 2 (feature 16f, derivations round 6, section 42): the units of amplitude
below a whole one accumulate on the thing (`wait_remainder`, in 32nds of one
quantum's amplitude, one accumulator across the groups it reads, as the
electricity reading keeps `push_remainder`), a whole unit charged as soon as
the accumulator reaches 32, exact integers, nothing lost; the `amount` reading
is untouched. (e) a thing reading 10 units per interval (2 and 3 quanta of one
owner in antiphase, 55 - 45) owes floor(10 k / 32) after k intervals, its
first interval at the fourth; (f) over 100 intervals of varying amplitudes the
total owed is floor(total units / 32), 140 of 4506, the remainder 26, where
amount owes the 447 quanta of push; (g) in a world the remainder rides on the
thing (10 after one push, no wait) and every thing of an amount run carries 0.
"""

import hashlib
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe.core.disturbance_state import CostMeter
from event_universe.core.spatial_state import BIT_SHADOW, BIT_THING, WAIT_READS, Ray, arrival_amplitude
from event_universe.fields.ray_interactions import apply_ray_interactions
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_bit_law import HEADINGS, MINUS_X, X, body, document, lamp, run, shadow

ROOT = Path(__file__).resolve().parents[1]
MINUS_Y = [0, -1, 0]
EIGHTY_ONE = (shadow((3, 2, 2), MINUS_X, amount=81, owner=3, steps=0),)


def world(shadows, option=None, ticks=12, phase_bits=0):
    """A thing of 1 leaving its lamp at (1,2,2) on +X, at (2,2,2) after tick 1;
    the bodies of 81 at (9,2,2) (owner 3) and (9,1,2) (owner 4), without a
    table, the owners of the shadows given with the board; w = 1; the rule
    reading the charge, one unit of push per quantum of shadow; the share
    turned back held at the thing's Node by the shadow's wait."""
    kind, emission, seed = lamp("lamp", 1, (1, 2, 2))
    doc = document(
        ticks=ticks,
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        bodies=[body((9, 2, 2), 3, amount=81), body((9, 1, 2), 4, amount=81)],
        shadows=[deepcopy(entry) for entry in shadows],
        phase_bits=phase_bits,
    )
    doc["wait_per_quantum"] = 1
    # The field of 81 spreads over twelve ticks: the slots of test_return_field (a).
    doc["spatial_fields"][0]["ray_slots"] = 32
    # The share turned back is held at the thing's Node by the shadow's wait
    # (shadow-wait-v1, read by the thing: 81 intervals for 81 quanta, met by
    # nothing while it waits), so that nothing of the field returns to the
    # thing within the window and its own wait alone decides its departure.
    doc["shadow_wait"] = {"per_quantum": 1, "reads": "thing"}
    if option is not None:
        doc["wait_reads"] = option
    return doc


def thing_at(inventory, position):
    """The thing at a Node: (heading, steps, owed, momentum)."""
    (thing,) = [r for r in inventory.get(tuple(position), ((),))[0] if r.detector == BIT_THING]
    return HEADINGS[thing.heading], thing.steps, thing.owed, thing.momentum


def digests(out):
    return {
        name: hashlib.sha256((out / name).read_bytes()).hexdigest()
        for name in ("events.jsonl", "state.json")
    }


def written(tmp_path, name, doc, ticks):
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    run_initialization(path, tmp_path / name, ticks=ticks)
    return tmp_path / name


def test_absent_or_amount_is_byte_identical_to_main(tmp_path):
    """(a): no key and the default declared are one world with one record; the
    other value is refused; amplitude declared is recorded."""
    ring = tmp_path / "ring"
    run_initialization(ROOT / "examples/nature/ring.json", ring, ticks=8)
    assert digests(ring) == {
        "events.jsonl": "091f6666d75ec307bf5d13f3f82123fab34c1d68524bade9b59d9fdbdcf20420",
        "state.json": "830345cd108b11d540bdac3639126aae482c330330cb31eeb2f035e56f20fd40",
    }
    assert "wait_reads" not in json.loads((ring / "run.json").read_text(encoding="utf-8"))
    absent = run(world(EIGHTY_ONE), 4)
    explicit = run(world(EIGHTY_ONE, "amount"), 4)
    for key in ("inventories", "ledgers", "momentum", "bodies_per_tick", "shadows"):
        assert absent[key] == explicit[key], key
    without = written(tmp_path, "without", world(EIGHTY_ONE), 4)
    declared = written(tmp_path, "amount", world(EIGHTY_ONE, "amount"), 4)
    assert digests(without) == digests(declared)
    for out in (without, declared):
        metadata = json.loads((out / "run.json").read_text(encoding="utf-8"))
        assert "wait_reads" not in metadata and "wait_reads_option" not in metadata
    initial = parse_initial_state(world(EIGHTY_ONE))
    assert initial.wait_reads == "amount" and initial.spatial_fields[0].wait_reads == "amount"
    with pytest.raises(ValueError, match="wait-reads-v1"):
        parse_initial_state(world(EIGHTY_ONE, "flux"))
    amplitude = written(tmp_path, "amplitude", world(EIGHTY_ONE, "amplitude"), 2)
    metadata = json.loads((amplitude / "run.json").read_text(encoding="utf-8"))
    assert metadata["wait_reads"] == WAIT_READS == "wait-reads-v1"
    assert metadata["wait_reads_option"] == "amplitude"


def test_eighty_one_quanta_in_phase_give_amplitude_nine():
    """(b): the push is the amount's under both readings; the wait is 81 under
    amount and 9 under amplitude; 9 quanta give 3; two owners' shares are two
    sums, 9 and 9, never one of 162."""
    amount = run(world(EIGHTY_ONE), 12)
    amplitude = run(world(EIGHTY_ONE, "amplitude"), 12)
    for result in (amount, amplitude):
        assert result["momentum"][1] == {1: [-80, 0, 0], 3: [0, 0, 0], 4: [0, 0, 0]}
        assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    assert thing_at(amount["inventories"][1], (2, 2, 2)) == (X, 1, 80, (-81, 0, 0))
    assert thing_at(amount["inventories"][11], (2, 2, 2)) == (X, 1, 70, (-81, 0, 0))
    for t in range(2, 11):
        assert thing_at(amplitude["inventories"][t - 1], (2, 2, 2)) == (X, 1, 10 - t, (-81, 0, 0))
    assert thing_at(amplitude["inventories"][10], (1, 2, 2)) == (MINUS_X, 2, 0, (-80, 0, 0))
    nine = run(world((shadow((3, 2, 2), MINUS_X, amount=9, owner=3, steps=0),), "amplitude"), 6)
    assert thing_at(nine["inventories"][1], (2, 2, 2)) == (X, 1, 2, (-9, 0, 0))
    assert thing_at(nine["inventories"][4], (1, 2, 2)) == (MINUS_X, 2, 0, (-8, 0, 0))
    two = run(
        world(
            (
                shadow((3, 2, 2), MINUS_X, amount=81, owner=3, steps=0),
                shadow((3, 2, 2), MINUS_X, amount=81, owner=4, steps=0),
            ),
            "amplitude",
        ),
        3,
    )
    assert thing_at(two["inventories"][1], (2, 2, 2)) == (X, 1, 17, (-162, 0, 0))


def test_shares_in_antiphase_from_two_ports_give_the_size_of_their_difference():
    """(c): 81 at phase 0 from +X and 9 at phase 2 (half a turn of four steps)
    from +Y: the sum's size is 288 - 96 = 192 of 32nds, six units, where the
    amounts are 90."""
    shadows = (
        shadow((3, 2, 2), MINUS_X, amount=81, owner=3, steps=0),
        shadow((2, 3, 2), MINUS_Y, amount=9, owner=3, steps=0) | {"phase": 2},
    )
    amount = run(world(shadows, phase_bits=2), 3)
    amplitude = run(world(shadows, "amplitude", phase_bits=2), 3)
    assert thing_at(amount["inventories"][1], (2, 2, 2)) == (X, 1, 89, (-81, -9, 0))
    assert thing_at(amplitude["inventories"][1], (2, 2, 2)) == (X, 1, 5, (-81, -9, 0))
    definition = parse_initial_state(world(shadows, "amplitude", phase_bits=2)).spatial_fields[0]
    first = Ray(
        definition.headings.index((-1, 0, 0)),
        (0, 0, 0),
        81,
        steps=1,
        detector=BIT_SHADOW,
        source_sign=-1,
        owner=3,
    )
    second = replace(first, heading=definition.headings.index((0, -1, 0)), amount=9, phase=2)
    assert arrival_amplitude((first, second), definition) == 192
    assert arrival_amplitude((first,), definition) == 288
    assert arrival_amplitude((first, replace(second, phase=0)), definition) == 384
    assert arrival_amplitude((), definition) == 0


def test_the_dense_layer_agrees_with_the_engine():
    """(d): the world of (b) under amplitude, the engine alone and the shadow
    layer: one board, one ledger, one momentum, one wait."""
    doc = world(EIGHTY_ONE, "amplitude")
    assert parse_initial_state(deepcopy(doc)).dense_field
    engine = run(deepcopy(doc) | {"dense_field": False}, 12)
    dense = run(deepcopy(doc), 12)
    for key in ("inventories", "ledgers", "momentum", "bodies_per_tick", "shadows"):
        assert engine[key] == dense[key], key
    assert engine["snapshot"]["parked"] == dense["snapshot"]["parked"]
    assert thing_at(dense["inventories"][10], (1, 2, 2)) == (MINUS_X, 2, 0, (-80, 0, 0))


def remainder_at(inventory, position):
    """The thing at a Node: (owed, wait_remainder)."""
    (thing,) = [r for r in inventory.get(tuple(position), ((),))[0] if r.detector == BIT_THING]
    return thing.owed, thing.wait_remainder


def harness(option):
    """The meeting alone, cycle after cycle: the thing of (b) at its Node, met by
    the shadows fed to it, through `apply_ray_interactions` on the world's
    rules; returns the thing after each meeting, its momentum, its wait and its
    remainder carried on, nothing walked."""
    initial = parse_initial_state(world(EIGHTY_ONE, option, phase_bits=2))
    definition = initial.spatial_fields[0]
    thing = Ray(definition.headings.index((1, 0, 0)), (0, 0, 0), 1, steps=1, owner=1)

    def share(heading, amount, phase=0):
        return Ray(
            definition.headings.index(heading),
            (0, 0, 0),
            amount,
            phase=phase,
            steps=1,
            detector=BIT_SHADOW,
            source_sign=-1,
            owner=3,
        )

    def meet(current, shadows):
        (bundle,) = apply_ray_interactions(
            ((current, *shadows),),
            initial.spatial_fields,
            initial.fields,
            initial.ray_interactions,
            CostMeter(initial.operation_costs),
            initial.operation_costs,
        )
        (after,) = [ray for ray in bundle if ray.detector == BIT_THING]
        return after

    return thing, share, meet


def test_units_below_a_whole_one_accumulate_on_the_thing():
    """(e): 2 and 3 quanta of one owner in antiphase, 55 - 45 = 10 of 32nds per
    interval: the thing owes floor(10 k / 32) after k meetings, the first
    interval at the fourth, the remainder 10 k mod 32; 31 and 8 after 100."""
    thing, share, meet = harness("amplitude")
    shadows = (share((-1, 0, 0), 2), share((0, -1, 0), 3, phase=2))
    charged = []
    for k in range(1, 101):
        thing = meet(thing, shadows)
        assert (thing.owed, thing.wait_remainder) == (10 * k // 32, 10 * k % 32), k
        assert thing.momentum == (-2 * k, -3 * k, 0) and thing.push_remainder == (0, 0, 0)
        if thing.owed > (10 * (k - 1) // 32):
            charged.append(k)
    assert (thing.owed, thing.wait_remainder) == (31, 8)
    assert charged[:6] == [4, 7, 10, 13, 16, 20]
    thing, share, meet = harness("amount")
    thing = meet(thing, shadows)
    assert (thing.owed, thing.wait_remainder) == (5, 0)


def test_the_total_owed_is_exact_over_a_hundred_intervals():
    """(f): interval k feeds 1 + (k mod 7) quanta at phase 0 from +X and, at
    every even k, one quantum in antiphase from +Y: the amplitudes 32, 45, 55,
    64, 71, 78, 84 of 1 to 7 quanta less 32 at the even intervals sum to 4506
    over 100 intervals, owed 140, the remainder 26; amount owes the 447 quanta
    of push."""
    amplitudes = {1: 32, 2: 45, 3: 55, 4: 64, 5: 71, 6: 78, 7: 84}
    thing, share, meet = harness("amplitude")
    total = 0
    quanta = 0
    for k in range(1, 101):
        amount = 1 + k % 7
        shadows = (share((-1, 0, 0), amount),)
        expected = amplitudes[amount]
        if k % 2 == 0:
            shadows += (share((0, -1, 0), 1, phase=2),)
            expected -= 32
        total += expected
        quanta += amount + (1 if k % 2 == 0 else 0)
        thing = meet(thing, shadows)
        assert (thing.owed, thing.wait_remainder) == (total // 32, total % 32), k
    assert total == 4506 and (thing.owed, thing.wait_remainder) == (140, 26)
    thing, share, meet = harness("amount")
    for k in range(1, 101):
        shadows = (share((-1, 0, 0), 1 + k % 7),)
        if k % 2 == 0:
            shadows += (share((0, -1, 0), 1, phase=2),)
        thing = meet(thing, shadows)
    assert quanta == 447 and (thing.owed, thing.wait_remainder) == (447, 0)


def test_the_remainder_rides_on_the_thing_and_amount_keeps_none():
    """(g): in a world, 2 and 3 in antiphase push the thing (-2, -3, 0), it owes
    nothing and carries 10 of 32nds on to the next Node; under amount every
    thing carries 0 and the run is the run of (a)."""
    shadows = (
        shadow((3, 2, 2), MINUS_X, amount=2, owner=3, steps=0),
        shadow((2, 3, 2), MINUS_Y, amount=3, owner=3, steps=0) | {"phase": 2},
    )
    amplitude = run(world(shadows, "amplitude", phase_bits=2), 3)
    assert remainder_at(amplitude["inventories"][1], (1, 2, 2)) == (0, 10)
    assert thing_at(amplitude["inventories"][1], (1, 2, 2)) == (MINUS_X, 2, 0, (-1, -3, 0))
    amount = run(world(shadows, phase_bits=2), 3)
    assert remainder_at(amount["inventories"][1], (2, 2, 2)) == (4, 0)
    for inventory in amount["inventories"]:
        for bundles in inventory.values():
            assert all(ray.wait_remainder == 0 for bundle in bundles for ray in bundle)
