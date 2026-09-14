"""Field-phase-first ordering: an isolated straight-moving emitter keeps its momentum.

POSTULATES section 7 requires that a moving isolated particle must not change
its momentum because of its own field. Under the default clock a carrier and
its departure-interval emission cross one link together and are sampled
together; the field-phase-first option completes field links before carriers
sample. Both the isolated-source control and an external-source control are
required so the option is not a force-off model.
"""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

CENTER = 3


def document(
    *,
    seeds,
    ticks=40,
    field_phase_first=True,
    link_ticks=1,
    hold=False,
    extra=None,
):
    doc = {
        "schema_version": 1,
        "model_id": "field-phase-first-contract-v1",
        "boundary": "open",
        "shape": [25, 7, 7],
        "slots_per_node": 4,
        "link_ticks": link_ticks,
        "normal_budget": 1_000_000,
        "ticks": ticks,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {"name": "charge", "components": 1, "units": "unit", "signed": True, "conserved": True},
            {
                "name": "momentum",
                "components": 3,
                "units": "unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
                "scale": 120,
            },
            {
                "name": "potential",
                "components": 1,
                "units": "unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "body",
                "fields": ["mass", "charge", "momentum"],
                "defaults": {"mass": 1, "charge": 1, "momentum": [0, 0, 0]},
                "transport": (
                    {"mode": "hold"}
                    if hold
                    else {
                        "mode": "move",
                        "direction_field": "momentum",
                        "rate": {
                            "op": "min",
                            "args": [
                                120,
                                {
                                    "op": "exact_div",
                                    "args": [
                                        {
                                            "op": "sum",
                                            "args": [{"op": "abs", "args": [{"field": "momentum"}]}],
                                        },
                                        {"field": "mass"},
                                    ],
                                },
                            ],
                        },
                        "rate_denominator": 120,
                    }
                ),
            }
        ],
        "spatial_fields": [
            {"field": "potential", "baseline": 0, "transport": "outward"},
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "outward"},
        ],
        "emissions": [
            {
                "type": "body",
                "field": "potential",
                "amount": {"op": "mul", "args": [{"field": "charge"}, 540]},
                "denominator": 1,
                "source": True,
            }
        ],
        "spatial_couplings": [
            {
                "name": "charge_times_flux",
                "type": "body",
                "field": "momentum",
                "mode": "exchange",
                "amount": {
                    "op": "neg",
                    "args": [{"op": "mul", "args": [{"field": "charge"}, {"flux": "potential"}]}],
                },
                "denominator": 10,
            }
        ],
        "seeds": [
            {"position": list(position), "type": "body", "values": values} for position, values in seeds
        ],
    }
    if field_phase_first:
        doc["field_phase_first"] = True
    doc.update(extra or {})
    return doc


def run(doc):
    world = Simulation(parse_initial_state(doc))
    for _ in range(doc["ticks"]):
        world.step()
    return world


def bodies(world):
    return sorted(
        (position, world.record_values(record)["charge"][0], world.record_values(record)["momentum"])
        for position, node in world.nodes.items()
        for record in node.records
        if record is not None
    )


@pytest.mark.parametrize(
    ("position", "momentum", "ticks"),
    [
        ((4, CENTER, CENTER), (15, 0, 0), 30),
        ((4, CENTER, CENTER), (120, 0, 0), 18),
        ((20, CENTER, CENTER), (-30, 0, 0), 30),
        ((4, 1, 1), (12, 6, 6), 30),
    ],
)
def test_isolated_moving_emitter_keeps_its_momentum(position, momentum, ticks):
    world = run(document(seeds=[(position, {"charge": 1, "momentum": list(momentum)})], ticks=ticks))
    found = bodies(world)
    assert found, "the body left the domain before the measured interval ended"
    ((_, _, final),) = found
    assert final == momentum
    assert world.totals()["momentum"] == momentum


def test_default_clock_documents_the_baseline_self_push():
    world = run(
        document(
            seeds=[((4, CENTER, CENTER), {"charge": 1, "momentum": [15, 0, 0]})],
            ticks=12,
            field_phase_first=False,
        )
    )
    ((_, _, final),) = bodies(world)
    assert final[0] > 15


def test_stationary_isolated_emitter_stays_at_rest():
    world = run(document(seeds=[((12, CENTER, CENTER), {"charge": 1, "momentum": [0, 0, 0]})], ticks=30))
    assert bodies(world) == [((12, CENTER, CENTER), 1, (0, 0, 0))]


@pytest.mark.parametrize(("right_charge", "sign"), [(1, 1), (-1, -1)])
def test_external_source_control_keeps_the_configured_sign_rule(right_charge, sign):
    left, right = (9, CENTER, CENTER), (12, CENTER, CENTER)
    world = run(
        document(
            seeds=[(left, {"charge": 1}), (right, {"charge": right_charge})],
            ticks=20,
            hold=True,
        )
    )
    found = dict((p, m) for p, _, m in bodies(world))
    # Like charges: left pushed toward -x, right toward +x. Unlike: reversed.
    assert found[left][0] * sign < 0
    assert found[right][0] * sign > 0
    assert found[left][1:] == (0, 0) and found[right][1:] == (0, 0)


def test_adjacent_receiver_reads_the_source_one_interval_earlier():
    source, receiver = (10, CENTER, CENTER), (11, CENTER, CENTER)
    seeds = [(source, {"charge": 1}), (receiver, {"charge": 0})]
    receiver_doc = document(seeds=seeds, ticks=1, hold=True)
    receiver_doc["spatial_couplings"][0]["amount"] = {"op": "neg", "args": [{"flux": "potential"}]}
    world = run(receiver_doc)
    momentum = dict((p, m) for p, _, m in bodies(world))[receiver]
    assert momentum[0] > 0
    assert world.totals()["momentum"] == (0, 0, 0)


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ({"link_ticks": 2}, "link_ticks 1"),
        ({"spatial_computation_delay": True}, "spatial_computation_delay"),
        ({"field_phase_first": "yes"}, "boolean"),
    ],
)
def test_rejected_combinations(extra, message):
    doc = document(seeds=[((4, CENTER, CENTER), {"charge": 1})])
    doc.update(extra)
    with pytest.raises(ValueError, match=message):
        parse_initial_state(doc)


def test_requires_spatial_fields():
    doc = document(seeds=[((4, CENTER, CENTER), {"charge": 1})])
    doc["spatial_fields"] = []
    doc["emissions"] = []
    doc["spatial_couplings"] = []
    with pytest.raises(ValueError, match="requires spatial fields"):
        parse_initial_state(doc)
