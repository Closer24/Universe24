"""Charge per thing (charge-per-thing-v1; Highlights 5.4 point 16 as amended by
the model owner on 2026-09-18, feature 16g): the charge of a thing is one
declared number of its family, whatever its content (an electron -1, a proton
+1, a body its own declared charge), never a charge per quantum; it is what a
thing multiplies an electric message by, whole; it adds when two things of one
family become one ray (point 25) and every table conserves it. The source's
charge over its content stays in the reading (point 18): that quotient is the
field's charge per quantum, the message a shadow carries.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Charge per thing")
before the first run, as Highlights 5.5 requires: (a) the worked example of
point 16, exact, under both readings; (b) a body of 1000 quanta with charge 1
pushed by a shadow of 9 takes 9 x (the source's charge over its content) x 1,
not 9000, and never moves faster than a ray; (c) charge adds on the merge of
two things of one family, on a lane and through a table that joins them; (d)
the catalog's electron of 20 does not turn at its first push; (e) the parser
reads a family's charge as the charge of a thing, admits a pushed body whose
charge is not a multiple of its amount, and the runner records the marker.
"""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import CostMeter, pack
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    BIT_THING,
    CHARGE_PER_THING,
    Ray,
    push_of,
    ray_charge,
    thing_charge,
)
from event_universe.fields.disturbances import evaluate
from event_universe.fields.rays import LaneClaims, merge_lane
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_bit_law import COSTS, HEADINGS, MINUS_X, X, body, document, field, lamp, rays_at, run, shadow

ZERO = (0, 0, 0)
MINUS_Y = [0, -1, 0]


def pair_world(electron, proton):
    """Two families, e of charge -1 and p of charge +1, each with the full release
    (a shadow per heading of its thing's whole content, the set proportional to
    the content, point 18); a lamp of each, `electron` and `proton` quanta, each
    a thing emitted once (things 1 and 2); the two tables of point 16, e read by
    p's shadows and p by e's, attraction (-1), one reading each."""

    def family(name, charge):
        return {
            "field": name,
            "baseline": 0,
            "transport": "ray",
            "headings": HEADINGS,
            "rays_per_tick": 1,
            "metric": "links",
            "pace": [1, 1],
            "charge": charge,
            "release": [1, 1],
        }

    def kind(name, field_name, amount):
        return {
            "name": name,
            "fields": [field_name, "momentum"],
            "defaults": {field_name: amount, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }

    def emission(name, field_name, amount, heading):
        return {
            "type": name,
            "field": field_name,
            "amount": amount,
            "denominator": 1,
            "heading": heading,
            "kerengonen_phase": 0,
        }

    def table(name, thing, other, reads):
        return {
            "name": name,
            "participants": [{"type": thing}, {"type": other}],
            "momentum_table": {other: -1},
            "reads": reads,
            "invariants": [
                {
                    "name": "energy",
                    "expression": {
                        "op": "add",
                        "args": [
                            {"field": "amount", "participant": 0},
                            {"field": "amount", "participant": 1},
                        ],
                    },
                }
            ],
        }

    return {
        "schema_version": 1,
        "model_id": "charge-per-thing-test-v1",
        "shape": [10, 5, 5],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 2,
        "operation_costs": dict.fromkeys(COSTS, 1),
        "wait_per_quantum": 0,
        "fields": [field("e"), field("p"), field("momentum", 3)],
        "disturbance_types": [kind("lamp_e", "e", electron), kind("lamp_p", "p", proton)],
        "spatial_fields": [family("e", -1), family("p", 1)],
        "emissions": [emission("lamp_e", "e", electron, X), emission("lamp_p", "p", proton, MINUS_X)],
        "seeds": [{"position": [2, 2, 2], "type": "lamp_e"}, {"position": [7, 2, 2], "type": "lamp_p"}],
        "ray_interactions": [
            table("e_reads_p", "e", "p", "charge"),
            table("p_reads_e", "p", "e", "charge"),
        ],
        "external_bodies": [],
        "detectors": [],
    }


@pytest.mark.parametrize(("electron", "proton"), [(32, 64), (256, 1024)])
def test_the_worked_example_of_point_16_holds_exactly_under_both_readings(electron, proton):
    """(a) An electron of content 32 and charge -1 and a proton of content 64 and
    charge +1, their shadow sets proportional to their contents (the full
    release: a shadow of 32 and a shadow of 64), push each other by equal and
    opposite amounts under both readings. Electricity: the proton, read by the
    electron's shadow of 32 arriving on +X, takes -1 x 32 x (+X) x (-1 / 32) x
    (+1) = (1, 0, 0), the electron, read by the proton's shadow of 64 arriving on
    -X, -1 x 64 x (-X) x (1 / 64) x (-1) = (-1, 0, 0): the product of the
    charges, whatever the contents (the same at 256 and 1024, where the
    per-quantum reading gave the proton four times the electron's push).
    Gravity: -1 x 32 x (+X) x 64 = (-2048, 0, 0) on the proton and -1 x 64 x
    (-X) x 32 = (2048, 0, 0) on the electron, the product of the contents. The
    owner table: a thing's charge is its family's, whole, over its content."""
    initial = parse_initial_state(pair_world(electron, proton))
    e_def, p_def = initial.spatial_fields
    assert (e_def.owner_content(1), e_def.owner_charge(1)) == (electron, -1)
    assert (p_def.owner_content(2), p_def.owner_charge(2)) == (proton, 1)
    assert e_def.push_denominator == p_def.push_denominator == proton
    shadow_e = Ray(0, ZERO, electron, detector=BIT_SHADOW, source_sign=-1, owner=1)
    shadow_p = Ray(1, ZERO, proton, detector=BIT_SHADOW, source_sign=1, owner=2)
    on_proton = push_of(-1, shadow_e, e_def, "charge", proton, 1)
    on_electron = push_of(-1, shadow_p, p_def, "charge", electron, -1)
    assert on_proton == ((1, 0, 0), ZERO)
    assert on_electron == ((-1, 0, 0), ZERO)
    assert push_of(-1, shadow_e, e_def, "content", proton, 1) == ((-electron * proton, 0, 0), ZERO)
    assert push_of(-1, shadow_p, p_def, "content", electron, -1) == ((electron * proton, 0, 0), ZERO)
    # A push below one quantum accumulates exactly, the remainder in units of 1 /
    # D: a shadow of 1 of the electron gives the proton (1 / 32, 0, 0), D / 32
    # units, and 32 of them are the quantum.
    whole, remainder = push_of(
        -1, Ray(0, ZERO, 1, detector=BIT_SHADOW, owner=1), e_def, "charge", proton, 1
    )
    assert (whole, remainder) == (ZERO, (proton // electron, 0, 0))
    for _ in range(electron - 1):
        whole, remainder = push_of(
            -1, Ray(0, ZERO, 1, detector=BIT_SHADOW, owner=1), e_def, "charge", proton, 1, remainder
        )
    assert (whole, remainder) == ((1, 0, 0), ZERO)


def test_a_body_of_a_thousand_quanta_with_charge_one_takes_the_message_times_one():
    """(b) The world of test_return_field (b): A, a body of 81 with the charge -81
    (its message -81 / 81 = -1 per quantum of shadow), and B, a body of 1000
    quanta with the whole charge 1 under the table {"m": 1}, A's shadow of 9
    fresh at (1,2,2) on +X. In the cycle of tick 1 B takes 1 x 9 x (+X) x (-1) x
    1 = (-9, 0, 0), nine units and not nine thousand (the cleanup's measurement
    under the per-quantum reading, "faster than a ray"), and holds it: 9 below
    its content, B stays where it is, and a body never moves faster than one
    Link per interval; the shadow turns back carrying (9, 0, 0), the ledger
    balanced at every tick."""
    doc = document(
        ticks=6,
        bodies=[
            body((0, 2, 2), 3, amount=81),
            body((2, 2, 2), 4, table={"m": 1}, amount=1000, charge=1),
        ],
        shadows=[shadow((1, 2, 2), X, amount=9, owner=3, steps=0)],
    )
    m_def = parse_initial_state(doc).spatial_fields[0]
    assert (m_def.owner_charge(3), m_def.owner_content(3)) == (-81, 81)
    assert (m_def.owner_charge(4), m_def.owner_content(4)) == (1, 1000)
    unit = Ray(0, ZERO, 9, detector=BIT_SHADOW, source_sign=-1, owner=3)
    assert push_of(1, unit, m_def, "charge", 1000, 1) == ((-9, 0, 0), ZERO)
    result = run(doc, 6)
    # After ticks 1 and 2 B holds the nine units; the share turned back, fresh at
    # B's Node after tick 1 and one Link on after tick 2, carries (9, 0, 0); from
    # the cycle of tick 3 it mixes at (1,2,2) and its ninths push B again (the
    # return is a field, return-field-v1), which this test does not pin.
    assert result["bodies_per_tick"][:2] == [[[0, 0, 0], [-9, 0, 0]]] * 2
    assert [entry["position"] for entry in result["bodies"]] == [[0, 2, 2], [2, 2, 2]]
    assert all(not entry["stepping"] for entry in result["bodies"])
    for tick, position, steps in ((1, (2, 2, 2), 0), (2, (1, 2, 2), 1)):
        returned = [r for r in rays_at(result["inventories"][tick - 1], position) if not r.parked]
        assert [(r.detector, r.owner, r.outbound, r.momentum, r.steps) for r in returned] == [
            (BIT_SHADOW, 3, 0, (9, 0, 0), steps)
        ]
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])


JOIN = {
    "name": "join",
    "participants": [{"type": "m"}, {"type": "m"}],
    "outputs": [{"field": "m", "amount": {"of": "sum"}, "heading": 0, "phase": {"of": 0}}],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}


def test_charge_adds_when_two_things_of_one_family_become_one_ray():
    """(c) Point 25: two things of `m` (charge -1), of 4 and 1 quanta and of
    owners 1 and 2, given one out-lane are one real ray of 5 carrying both, its
    charge -2, read off the identities it carries and not off its quanta. A
    table that joins two things (2 to 1, the sum of the inputs) keeps both the
    same way: lamps e (thing 1) and f (thing 2) of 2 quanta, at (1,2,2) on +X and
    (5,2,2) on -X, meet at (3,2,2) after tick 2; in the cycle of tick 3 the join
    puts out one ray of 4 on +X, owner 1 with the further owner 2, at (4,2,2)
    after tick 3; the world reads -2 at every tick, nothing sourced, and the
    charge invariant the parser appends sums the things' charges (-2 before and
    after, checked like the declared ones)."""
    doc = document(ticks=4, rules=(JOIN,))
    definition = parse_initial_state(doc).spatial_fields[0]
    first = Ray(0, ZERO, 4, steps=1, owner=1)
    second = Ray(0, ZERO, 1, steps=0, owner=2)
    claims = LaneClaims()
    claims.claim(0, 0, first)
    (merged,) = merge_lane((first, second), 0, claims, definition)
    assert (merged.amount, merged.owner, merged.owners, merged.detector) == (5, 1, (2,), BIT_THING)
    assert thing_charge(merged, definition) == ray_charge((merged,), definition) == -2
    kind_e, emission_e, seed_e = lamp("e", 2, (1, 2, 2))
    kind_f, emission_f, seed_f = lamp("f", 2, (5, 2, 2), heading=MINUS_X)
    doc = document(
        ticks=4,
        types=[kind_e, kind_f],
        emissions=[emission_e, emission_f],
        seeds=[seed_e, seed_f],
        rules=(JOIN,),
    )
    initial = parse_initial_state(doc)
    (rule,) = initial.ray_interactions
    assert rule.output_identities == ((0, 1),)
    charge = next(invariant for invariant in rule.invariants if invariant.name == "charge")
    # A meeting's invariant is a per-ray readout summed over the inputs and over
    # the outputs: the charge of the thing the ray is, -1 for a thing of `m` and
    # -2 for a ray carrying two, whatever their amounts.
    for charge_of_thing, amount in ((-1, 2), (-2, 4), (-1, 4)):
        view = (
            pack((amount,)),
            pack((1, 0, 0)),
            pack((0,)),
            pack((-1,)),
            pack((0,)),
            pack((0,)),
            pack((charge_of_thing,)),
            pack((1,)),
            pack((-1,)),
        )
        meter = CostMeter(initial.operation_costs)
        assert evaluate(charge.expression, view, view, meter) == (charge_of_thing,)
    result = run(doc, 4)
    (joined,) = [r for r in rays_at(result["inventories"][2], (4, 2, 2)) if not r.parked]
    assert (joined.amount, joined.owner, joined.owners, joined.detector) == (4, 1, (2,), BIT_THING)
    assert HEADINGS[joined.heading] == X
    assert [ledger["charge"]["m"]["current"] for ledger in result["ledgers"]] == [-2] * 4
    assert [ledger["charge"]["m"]["sourced"] for ledger in result["ledgers"]] == [0] * 4
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [4] * 4


def electron_world():
    """The smallest board of the catalog's electron: `m` of charge -3 with a
    clock, K 20; a lamp of 20 (thing 1) at (1,2,2) on +X, a second lamp of 20
    (thing 2) at (8,4,4) that holds its thing, and a shadow of 1 of thing 2 fresh
    at (2,3,2) on -Y, meeting the thing at (2,2,2) after tick 1; the table
    {"m": 1} read by charge."""
    kind, emission, seed = lamp("lamp", 20, (1, 2, 2))
    other, other_emission, other_seed = lamp("other", 20, (8, 4, 4))
    other_emission = other_emission | {"dissolve": {"after_ticks": 1000, "over_ticks": 1}}
    doc = document(
        ticks=3,
        types=[kind, other],
        emissions=[emission, other_emission],
        seeds=[seed, other_seed],
        shadows=[shadow((2, 3, 2), MINUS_Y, owner=2, steps=0)],
        clock=20,
    )
    doc["spatial_fields"][0]["charge"] = -3
    return doc


def test_the_catalogs_electron_does_not_turn_at_its_first_push():
    """(d) The electron of 20 (charge -3, whole) meets the shadow of 1 of a second
    electron of 20 (its message -3 / 20) in the cycle of tick 2: the push, 1 x 1
    x (0,-1,0) x (-3 / 20) x (-3), is 9 / 20 of a quantum, nothing into the
    momentum and (0, -9, 0) in units of 1 / 20 on the thing, so it goes on
    along +X (a turn needs its content, 20, on one axis; the per-quantum reading
    gave (0, -9, 0) whole, and the cleanup's whole-charge measurement 180, a
    turn at the first push); the shadow turns back carrying nothing. The world
    reads two electrons, -6, at every tick, the one in its lamp counted whole."""
    doc = electron_world()
    initial = parse_initial_state(doc)
    definition = initial.spatial_fields[0]
    assert (definition.charge, definition.clock) == (-3, 20)
    assert (definition.owner_charge(2), definition.owner_content(2)) == (-3, 20)
    result = run(doc, 3)
    for tick, x in ((1, 2), (2, 3), (3, 4)):
        (thing,) = [
            r for r in rays_at(result["inventories"][tick - 1], (x, 2, 2)) if r.detector == BIT_THING
        ]
        assert (HEADINGS[thing.heading], thing.amount, thing.momentum) == (X, 20, None)
        assert thing.push_remainder == ((0, -9, 0) if tick >= 2 else ZERO)
    # The things' momentum lists the things on the board: the electron on +X
    # with nothing carried; the second electron is in its lamp.
    assert result["momentum"] == [{1: [20, 0, 0]}] * 3
    (returned,) = [r for r in rays_at(result["inventories"][1], (2, 3, 2)) if not r.parked]
    assert (returned.detector, returned.owner, returned.outbound, returned.momentum) == (
        BIT_SHADOW,
        2,
        0,
        None,
    )
    assert [ledger["charge"]["m"]["current"] for ledger in result["ledgers"]] == [-6] * 3
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])


def test_the_parser_reads_the_charge_of_a_thing_and_the_runner_records_the_marker(tmp_path):
    """(e) A family's `charge` is the charge of one of its things, whole: a lamp
    of 20 quanta of `m` with charge -3 is an owner of charge -3 (not -60); a
    body of 1000 quanta with the whole charge 1 under a table parses (the
    per-quantum reading refused a charge that was not a multiple of the amount)
    and its charge is 1; a body's shadows carry its charge over its content, the
    body of 81 with charge -81 the message -1 per quantum; the runner records
    `charge_per_thing` as charge-per-thing-v1."""
    initial = parse_initial_state(electron_world())
    assert initial.spatial_fields[0].owner_charges == (-3, -3)
    assert initial.spatial_fields[0].owner_contents == (20, 20)
    doc = document(
        ticks=1,
        bodies=[
            body((0, 2, 2), 3, amount=81),
            body((2, 2, 2), 4, table={"m": 1}, amount=1000, charge=1),
        ],
    )
    initial = parse_initial_state(doc)
    assert [(b.amount, b.charge) for b in initial.external_bodies] == [(81, -81), (1000, 1)]
    # The owners of `m`: the board's type (thing 1, a thing of the family's
    # charge -1 over its declared stock of 4, seeded nowhere) and the two bodies.
    assert initial.spatial_fields[0].owners == (1, 3, 4)
    assert initial.spatial_fields[0].owner_charges == (-1, -81, 1)
    assert initial.spatial_fields[0].owner_contents == (4, 81, 1000)
    refused = deepcopy(doc)
    refused["external_bodies"][1]["charge"] = "one"
    with pytest.raises(ValueError, match="external body charge"):
        parse_initial_state(refused)
    source = tmp_path / "world.json"
    source.write_text(json.dumps(electron_world()), encoding="utf-8")
    run_initialization(source, tmp_path / "out", ticks=2)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["charge_per_thing"] == CHARGE_PER_THING == "charge-per-thing-v1"
    assert metadata["conserved_at_every_completed_tick"]
    assert [ledger["charge"]["m"]["current"] for ledger in metadata["audit"]] == [-6, -6]
    with Simulation(initial) as world:
        assert world.charge_totals() == {"m": 0}
