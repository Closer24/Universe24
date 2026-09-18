"""Meeting of rays with N-to-M outputs (ray-meeting-conversion-v1): two rays in,
declared outputs out with every family's stock exact, the split by a declared
table indexed by the phase difference, and a rule whose outputs break an
invariant rejected before any owner changes.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Ray meetings with
outputs") before the first run: two lamps fire one ray each of family a at one
Node under the shared Detector admission.
"""

import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import CostMeter, OperationCosts
from event_universe.core.spatial_state import RAY_EVENT_STATE, RAY_LAYERS, RAY_MEETING, Ray
from event_universe.fields.ray_interactions import apply_ray_interactions
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

CENTER = (7, 7, 7)
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# The steering table of a family of 8 phase steps, written by the engine from the
# width (phase-spread-v1, 2026-09-18: never declared): cos^2(d/2) in eighths, rounded.
TABLE = [8, 7, 4, 1, 0, 1, 4, 7]
COSTS = OperationCosts((1,) * 9)


def ray_field(participant, name):
    return {"field": name, "participant": participant}


def rule(outputs, invariants):
    """Two rays of family a with equal amounts and opposite headings meet."""
    same_amount = {"op": "eq", "args": [ray_field(0, "amount"), ray_field(1, "amount")]}
    heading_sum = {"op": "add", "args": [ray_field(0, "heading"), ray_field(1, "heading")]}
    head_on = {"op": "eq", "args": [{"op": "dot", "args": [heading_sum, heading_sum]}, 0]}
    return {
        "name": "meeting",
        "participants": [{"type": "a"}, {"type": "a"}],
        "when": {"op": "mul", "args": [same_amount, head_on]},
        "outputs": outputs,
        "invariants": invariants,
    }


ENERGY = {"name": "energy", "expression": {"field": "amount"}}
MOMENTUM = {
    "name": "momentum",
    "expression": {"op": "mul", "args": [{"field": "amount"}, {"field": "heading"}]},
}


def four(amounts=(2, 2, 3, 3), ports=(2, 3, 4, 5)):
    return [
        {"field": "a", "amount": amounts[0], "heading": ports[0]},
        {"field": "a", "amount": amounts[1], "heading": ports[1], "input": 1, "phase": {"of": 1}},
        {"field": "a", "amount": amounts[2], "heading": ports[2], "phase": 3},
        {
            "field": "a",
            "amount": amounts[3],
            "heading": ports[3],
            "phase": {"of": 1, "offset": 7},
            "delay": 0,
        },
    ]


def table_split(table=None, rest_of=0):
    amount = {"of": "sum", "index": "phase_difference"}
    if table is not None:
        amount["table"] = table
    return [
        {"field": "a", "amount": amount, "heading": 2},
        {"field": "a", "amount": {"rest_of": rest_of}, "heading": 3, "phase": {"of": 1}},
    ]


def document(outputs, invariants, delta, audit=True, ticks=4):
    """The board; `audit` declares the local energy/momentum audit. A split by a
    table between two Ports moves ray momentum that has no owner before the field
    ray of feature 7, so the table cases run without that audit."""
    lamps = (((5, 7, 7), 0, 0), ((9, 7, 7), 1, delta))
    conservation = {
        "name": "quanta",
        "energy_units": "quantum",
        "momentum_units": "quantum times heading",
        "carriers": [
            {
                "requires": ["a", "momentum"],
                "energy": {"field": "a"},
                "momentum": {"field": "momentum"},
            }
        ],
        "spatial": {
            "energy": {"field": "a", "side": "right"},
            "momentum": {"op": "vector", "args": [0, 0, 0]},
        },
    }
    return {
        "schema_version": 1,
        "model_id": "ray-meeting-test-v1",
        "shape": [15, 15, 15],
        "boundary": "periodic",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": "a",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": ["a", "momentum"],
                "defaults": {"a": 5, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for index in range(2)
        ],
        "spatial_fields": [
            {
                "field": "a",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 1,
                "ray_slots": 8,
                "metric": "links",
                "pace": [1, 1],
                "kerengonen": {"phase_steps": 8},
            }
        ],
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": "a",
                "amount": 5,
                "denominator": 1,
                "heading": HEADINGS[heading],
                "kerengonen_phase": phase,
            }
            for index, (_, heading, phase) in enumerate(lamps)
        ],
        "seeds": [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (position, _, _) in enumerate(lamps)
        ],
        "ray_interactions": [rule(outputs, invariants)],
    } | ({"conservation": conservation} if audit else {})


def rays_at(world, position):
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    if node is None or not node.rays:
        return []
    # bit-law-v1 (2026-09-18): a ray carries the identity of the thing that emitted
    # it (`owner`); this module pins lines and events, not identities (test_bit_law does).
    return sorted(
        (replace(ray, owner=0) for bundle in node.rays for ray in bundle), key=lambda ray: ray.heading
    )


def lamp(world, type_index):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    )


def emitted(heading, steps, phase):
    """A lamp's ray: the emission is one event on the heading's Port."""
    shares = [0] * 6
    shares[heading] = 5
    return Ray(
        heading,
        (0, 0, 0),
        5,
        phase=phase,
        steps=steps,
        event_ports=1 << heading,
        event_shares=tuple(shares),
    )


def product(heading, amount, phase, mask, shares, steps=0):
    """An output of the meeting: a new event ray carrying the meeting's mask and shares."""
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        steps=steps,
        event_ports=mask,
        event_shares=shares,
    )


def meet(initial, residents):
    return apply_ray_interactions(
        (tuple(residents),),
        initial.spatial_fields,
        initial.fields,
        initial.ray_interactions,
        CostMeter(COSTS),
        COSTS,
    )


# (a) four events out on four Ports; (b) the table split at d = 0, 4, 2 and 1.
FOUR_SHARES = (0, 0, 2, 2, 3, 3)
CASES = {
    "four": (
        four(),
        [ENERGY, MOMENTUM],
        0,
        (
            # The inputs' phases are 0 since clock-readings-v1 (2026-09-18: the
            # family declares no clock), so the outputs read 0, 0, 3 and 7.
            product(2, 2, 0, 60, FOUR_SHARES),
            product(3, 2, 0, 60, FOUR_SHARES),
            product(4, 3, 3, 60, FOUR_SHARES),
            product(5, 3, 7, 60, FOUR_SHARES),
        ),
    ),
    "table_0": (table_split(), [ENERGY], 0, (product(2, 10, 0, 4, (0, 0, 10, 0, 0, 0)),)),
    "table_4": (table_split(), [ENERGY], 4, (product(3, 10, 4, 8, (0, 0, 0, 10, 0, 0)),)),
    "table_2": (
        table_split(),
        [ENERGY],
        2,
        (product(2, 5, 0, 12, (0, 0, 5, 5, 0, 0)), product(3, 5, 2, 12, (0, 0, 5, 5, 0, 0))),
    ),
    "table_1": (
        table_split(),
        [ENERGY],
        1,
        (product(2, 8, 0, 12, (0, 0, 8, 2, 0, 0)), product(3, 2, 1, 12, (0, 0, 8, 2, 0, 0))),
    ),
}
# The momentum a split moves between the two Ports, booked as an accounted source.
STEERED = {
    "four": (0, 0, 0),
    "table_0": (0, 10, 0),
    "table_4": (0, -10, 0),
    "table_2": (0, 0, 0),
    "table_1": (0, 6, 0),
}
# Where each product is after its first and second Link, by heading.
NEIGHBORS = {
    2: ((7, 8, 7), (7, 9, 7)),
    3: ((7, 6, 7), (7, 5, 7)),
    4: ((7, 7, 8), (7, 7, 9)),
    5: ((7, 7, 6), (7, 7, 5)),
}


@pytest.mark.parametrize("case", ["four", "table_0", "table_4", "table_2", "table_1", "broken"])
def test_a_meeting_replaces_its_rays_by_declared_outputs_split_by_the_table_or_is_rejected(
    tmp_path, case
):
    if case == "broken":
        # (c) Outputs that break an invariant are rejected before any owner changes,
        # by the meeting itself and in the run; malformed tables at initialization.
        residents = (emitted(0, 2, 0), emitted(1, 2, 0))
        for outputs, message in (
            (four(amounts=(2, 2, 3, 4)), "violates conservation of amount"),
            (four(ports=(2, 2, 4, 5)), "violates invariant momentum"),
        ):
            initial = parse_initial_state(document(outputs, [ENERGY, MOMENTUM], 0))
            with pytest.raises(ValueError, match=message):
                meet(initial, residents)
            world = Simulation(initial)
            world.step()
            world.step()
            assert rays_at(world, CENTER) == list(residents)
            with pytest.raises(ValueError, match=message):
                world.step()
        for outputs, message in (
            (table_split(table=TABLE), "it is not declared"),
            (table_split(rest_of=1), "rest_of requires an output split by a table"),
            (four(ports=(2, 3, 4, 6)), "Port index"),
        ):
            with pytest.raises(ValueError, match=message):
                parse_initial_state(document(outputs, [ENERGY], 0))
        return
    outputs, invariants, delta, products = CASES[case]
    audit = case == "four"
    initial = parse_initial_state(document(outputs, invariants, delta, audit))
    world = Simulation(initial)
    for tick in range(1, 5):
        world.step()
        # Totals and the accounting are exact at every tick: the stock of a never
        # changes, and the momentum a split steers between two Ports is booked as
        # an explicitly accounted source; with the audit, every owner's energy and
        # momentum too.
        momentum = STEERED[case] if tick >= 3 else (0, 0, 0)
        assert world.totals() == {"a": (10,), "momentum": momentum}
        assert world.source_totals() == {"a": (0,), "momentum": momentum}
        report = world.conservation_report()
        if audit:
            assert report["status"] == "passed"
            assert report["current"]["energy"] == 10
            assert tuple(report["current"]["momentum"]) == (0, 0, 0)
        else:
            assert report["status"] == "not_configured"
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        count = sum(len(rays_at(world, n.position)) for n in world.inventory_view().nodes)
        assert count == (2 if tick <= 2 else len(products))
        if tick == 1:
            assert lamp(world, 0) == {"a": (0,), "momentum": (-5, 0, 0)}
            assert lamp(world, 1) == {"a": (0,), "momentum": (5, 0, 0)}
        elif tick == 2:
            residents = rays_at(world, CENTER)
            assert residents == [emitted(0, 2, 0), emitted(1, 2, delta % 8)]
            # (a), (b) The meeting: the inputs are replaced by the declared outputs,
            # each a new event ray with steps 0 and the mask and shares of the meeting.
            assert meet(initial, residents) == (products,)
        else:
            # Nothing is left at the Node and the inputs' lines are empty.
            assert rays_at(world, CENTER) == []
            assert rays_at(world, (6, 7, 7)) == [] and rays_at(world, (8, 7, 7)) == []
            for ray in products:
                walked = product(
                    ray.heading,
                    ray.amount,
                    ray.phase,  # no clock: the phase stays (clock-readings-v1)
                    ray.event_ports,
                    ray.event_shares,
                    steps=tick - 2,
                )
                assert rays_at(world, NEIGHBORS[ray.heading][tick - 3]) == [walked]
            for heading in NEIGHBORS.keys() - {ray.heading for ray in products}:
                assert rays_at(world, NEIGHBORS[heading][tick - 3]) == []
    path = tmp_path / "meeting.json"
    path.write_text(json.dumps(document(outputs, invariants, delta, audit)), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=4)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["ray_meeting"] == RAY_MEETING == "ray-meeting-conversion-v1"
    assert metadata["ray_state"] == RAY_EVENT_STATE and metadata["ray_layers"] == RAY_LAYERS
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["final_totals"] == {"a": [10], "momentum": list(STEERED[case])}
    assert metadata["source_totals"] == {"a": [0], "momentum": list(STEERED[case])}
