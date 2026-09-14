"""Explicit duration, indexed vector rules and property policies in the Node profile."""

from copy import deepcopy
from dataclasses import replace

import pytest

from event_universe.core.coupling_selectors import participant_groups
from event_universe.core.disturbance_state import MAX_VALUE, CostMeter, Expression, pack, unpack
from event_universe.core.spatial_state import zero_spatial_state
from event_universe.fields.disturbances import DisturbanceLaw, evaluate
from event_universe.fields.record_operations import RecordOperations
from event_universe.fields.spatial_interactions import JointSpatialCouplingLaw
from event_universe.fields.spatial_plan import SpatialLaw
from event_universe.initialization import _Expressions, parse_initial_state

from .test_disturbance_engine import document, field, kind
from .test_local_field_rules import document as spatial_document
from .test_local_field_rules import invariant, local, operation
from .test_spatial_interactions import exchange


def node_profile(raw):
    raw["node_execution"] = True
    for definition in raw["fields"]:
        definition["aggregation"] = "sum" if definition["components"] == 1 else "vector_sum"
    quantity = raw["fields"][0]
    readout = {
        "name": "declared stock",
        "components": quantity["components"],
        "units": "configured unit",
        "carriers": [{"requires": [quantity["name"]], "value": {"field": quantity["name"]}}],
    }
    if raw.get("spatial_fields"):
        readout["spatial"] = local(quantity["name"])
    raw["conservation_contract"] = {"name": "closed test", "quantities": [readout]}
    return raw


@pytest.mark.parametrize(
    "aggregation", ["keep_equal", "phase_bins", "interaction_state", "nonmergeable"]
)
def test_spatial_receipt_rejects_nonadditive_ownership(aggregation):
    raw = node_profile(spatial_document([field("quantity")]))
    raw["fields"][0]["aggregation"] = aggregation
    with pytest.raises(ValueError, match="spatial ownership requires additive"):
        parse_initial_state(raw)


def indexed_document(*, width=3, count=6, roles=6, k=5):
    values = [1] * width if width != 1 else 1
    raw = node_profile(
        document(
            [kind("parcel", values={"quantity": values})],
            [((0, 0, 0), "parcel")] * count,
            fields=[field("quantity", width)],
        )
    )
    for index, seed in enumerate(raw["seeds"]):
        seed["values"] = {"quantity": [index + 1] * width if width != 1 else index + 1}
    references = [{"field": "quantity", "participant": i} for i in range(roles)]
    total = references[0]
    for reference in references[1:]:
        total = operation("add", total, reference)
    raw["interactions"] = [
        {
            "name": "rotate group",
            "participants": [{"requires": ["quantity"]} for _ in range(roles)],
            "k": k,
            "assignments": [
                {"participant": i, "field": "quantity", "expression": references[(i + 1) % roles]}
                for i in range(roles)
            ],
            "invariants": [invariant("total", total)],
        }
    ]
    return raw


def plan(raw):
    initial = parse_initial_state(raw)
    records = tuple(seed.record for seed in initial.seeds)
    law = DisturbanceLaw(
        initial.fields, initial.disturbances, (), initial.operation_costs, initial.interactions
    )
    return initial, records, law(records, (), 0)


@pytest.mark.parametrize("width", [1, 2, 3, 4, 32])
def test_six_distinct_records_rotate_from_one_frozen_snapshot(width):
    initial, before, result = plan(indexed_document(width=width))
    assert result.interaction_ticks == 5
    assert [unpack(record.values[0]) for _, record in result.replacements] == [
        (index,) * width for index in (2, 3, 4, 5, 6, 1)
    ]
    assert [unpack(record.values[0])[0] for record in before] == list(range(1, 7))
    assert len(initial.interactions[0].participants) == 6


def test_disjoint_groups_and_sequential_rules_add_only_fired_durations():
    raw = indexed_document(count=12)
    skipped = deepcopy(raw["interactions"][0])
    skipped.update(name="skip", k=MAX_VALUE, when=0)
    raw["interactions"].append(skipped)
    next_rule = deepcopy(raw["interactions"][0])
    next_rule.update(name="second rotation", k=2)
    raw["interactions"].append(next_rule)
    initial, records, result = plan(raw)
    assert participant_groups(initial.interactions[0], records) == (tuple(range(6)), tuple(range(6, 12)))
    assert result.interaction_ticks == 14
    assert [unpack(record.values[0])[0] for _, record in result.replacements] == [
        3,
        4,
        5,
        6,
        1,
        2,
        9,
        10,
        11,
        12,
        7,
        8,
    ]


def test_rule_duration_is_independent_of_declared_operation_tariffs():
    raw = indexed_document()
    first = plan(raw)[2]
    raw["operation_costs"] = {name: price * 7 for name, price in raw["operation_costs"].items()}
    second = plan(raw)[2]
    assert first.interaction_ticks == second.interaction_ticks == 5
    assert second.cost == first.cost * 7
    assert first.replacements == second.replacements


def test_incomplete_group_keeps_records_and_does_not_price_an_interaction():
    initial, records, result = plan(indexed_document(count=5))
    assert participant_groups(initial.interactions[0], records) == ()
    assert tuple(record for _, record in result.replacements) == records
    assert result.interaction_ticks == 0


def test_role_selection_is_greedy_without_combinatorial_reassignment():
    raw = indexed_document(count=2, roles=2)
    raw["disturbance_types"].append(kind("other", values={"quantity": [7, 0, 0]}))
    raw["seeds"][1]["type"] = "other"
    raw["interactions"][0]["participants"][1] = {"type": "parcel"}
    initial, records, result = plan(raw)
    assert participant_groups(initial.interactions[0], records) == ()
    assert result.interaction_ticks == 0


@pytest.mark.parametrize("k", [None, 0, -1, True, 1.5, MAX_VALUE + 1])
def test_node_rules_reject_missing_or_invalid_duration(k):
    raw = indexed_document()
    if k is None:
        del raw["interactions"][0]["k"]
    else:
        raw["interactions"][0]["k"] = k
    with pytest.raises(ValueError, match="k|integer"):
        parse_initial_state(raw)


@pytest.mark.parametrize("target", ["assignment", "reference", "duplicate", "pair", "roles"])
def test_indexed_rules_validate_targets_shapes_and_exclusive_selectors(target):
    raw = indexed_document()
    rule = raw["interactions"][0]
    if target == "assignment":
        rule["assignments"][0]["participant"] = 6
    elif target == "reference":
        rule["assignments"][0]["expression"]["participant"] = 6
    elif target == "duplicate":
        rule["assignments"].append(deepcopy(rule["assignments"][0]))
    elif target == "pair":
        rule["left_type"] = "parcel"
    else:
        raw["slots_per_node"] = 5
        raw["seeds"] = raw["seeds"][:5]
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_failed_group_preserves_all_inputs_and_overflow_cannot_cancel():
    raw = indexed_document()
    raw["interactions"][0]["assignments"][0]["expression"] = [0, 0, 0]
    initial = parse_initial_state(raw)
    records = tuple(seed.record for seed in initial.seeds)
    law = DisturbanceLaw(
        initial.fields, initial.disturbances, (), initial.operation_costs, initial.interactions
    )
    with pytest.raises(ValueError, match="conservation"):
        law(records, (), 0)
    assert [unpack(record.values[0])[0] for record in records] == list(range(1, 7))
    wide = parse_initial_state(indexed_document(width=32))
    parser = _Expressions(wide.fields, (0,))
    dot = parser.parse(operation("dot", [MAX_VALUE] * 32, [MAX_VALUE] * 16 + [-MAX_VALUE] * 16))
    with pytest.raises(OverflowError):
        evaluate(dot, (), (), CostMeter(wide.operation_costs))


def test_wide_vectors_keep_three_dimensional_operations_explicit():
    initial = parse_initial_state(indexed_document(width=4))
    for expression in (
        operation("cross", [1, 2, 3, 4], [4, 3, 2, 1]),
        {"op": "transform", "args": [[1, 2, 3, 4]], "matrix": [[1, 0, 0]] * 3},
    ):
        with pytest.raises(ValueError):
            _Expressions(initial.fields, (0,)).parse(expression)
    dot = _Expressions(initial.fields, (0,)).parse(operation("dot", [1, 2, 3, 4], [4, 3, 2, 1]))
    assert evaluate(dot, (), (), CostMeter(initial.operation_costs)) == (20,)
    raw = indexed_document(width=4)
    raw.pop("node_execution")
    with pytest.raises(ValueError, match="1 or 3"):
        parse_initial_state(raw)


@pytest.mark.parametrize("member", ["aggregation", "conservation_contract", "link_ticks", "updates"])
def test_node_profile_requires_explicit_policies_and_supported_timing(member):
    raw = indexed_document()
    if member == "aggregation":
        raw["fields"][0].pop("aggregation")
    elif member == "conservation_contract":
        raw.pop(member)
    elif member == "link_ticks":
        raw[member] = 2
    else:
        raw["disturbance_types"][0]["updates"] = [{"field": "quantity", "expression": [1, 1, 1]}]
    with pytest.raises(ValueError):
        parse_initial_state(raw)


@pytest.mark.parametrize(
    "aggregation", ["keep_equal", "phase_bins", "interaction_state", "nonmergeable"]
)
def test_nonadditive_policies_are_retained_and_never_silently_split(aggregation):
    raw = indexed_document(width=1)
    raw["fields"][0]["aggregation"] = aggregation
    initial = parse_initial_state(raw)
    assert initial.fields[0].aggregation == aggregation
    policy = RecordOperations(initial.fields, initial.disturbances)
    record = initial.seeds[0].record
    assert policy.receive((record, None), (record,), frozenset()) == (record, record)
    raw["disturbance_types"][0]["transport"] = {"mode": "split"}
    with pytest.raises(ValueError, match="additive aggregation"):
        parse_initial_state(raw)


def test_additive_receipt_partitions_different_carried_bookkeeping():
    raw = indexed_document(width=1, count=1)
    raw["interactions"] = []
    raw["disturbance_types"][0]["transport"] = {"mode": "split"}
    initial = parse_initial_state(raw)
    record = initial.seeds[0].record
    policy = RecordOperations(initial.fields, initial.disturbances)
    combined = policy.receive((record, None), (record,), frozenset())
    assert unpack(combined[0].values[0]) == (2,)
    incoming = replace(record, phase_codes=(pack((1,)),))
    assert policy.receive((record, None), (incoming,), frozenset()) == (record, incoming)


def test_received_presence_distinguishes_zero_packet_and_prices_only_fired_field_rules():
    raw = node_profile(spatial_document([field("quantity")]))
    raw["field_rules"] = [
        {
            "name": "observe zero arrival",
            "k": 3,
            "when": {"received_present": "quantity", "port": 4},
            "assignments": [{"field": "quantity", "expression": local("quantity")}],
            "invariants": [invariant("stock", local("quantity"))],
        }
    ]
    initial = parse_initial_state(raw)
    law = SpatialLaw(
        initial.fields, initial.spatial_fields, (), initial.operation_costs, initial.field_rules
    )
    empty = zero_spatial_state(1)
    assert law((empty,), ()).interaction_ticks == 0
    received = replace(empty, received_mask=1 << 4)
    result = law((received,), ())
    assert result.interaction_ticks == 3
    assert result.states[0].received_mask == 0
    assert received.received_mask == 1 << 4
    expression = Expression("received_present", field=0, port=4)
    with pytest.raises(ValueError, match="explicitly supplied"):
        evaluate(expression, (), (), CostMeter(initial.operation_costs))


def test_spatial_interaction_duration_and_skipped_rule_use_same_local_clock_metadata():
    raw = node_profile(exchange())
    raw["spatial_interactions"][0]["k"] = 4
    initial = parse_initial_state(raw)
    law = JointSpatialCouplingLaw(
        initial.fields,
        (),
        initial.operation_costs,
        initial.spatial_fields,
        interactions=initial.spatial_interactions,
    )
    records = (initial.seeds[0].record,)
    sample = (pack((2,)),)
    ports = ((pack((0,)),),) * 6
    result = law(records, sample, ports=ports)
    assert result.interaction_ticks == 4
    assert unpack(result.records[0].values[0]) == (2,)
    skipped = replace(initial.spatial_interactions[0], when=Expression("literal", literal=(0,)))
    assert replace(law, interactions=(skipped,))(records, sample, ports=ports).interaction_ticks == 0


def test_legacy_profile_preserves_zero_explicit_duration():
    raw = exchange()
    initial = parse_initial_state(raw)
    assert not initial.node_execution
    assert initial.fields[0].aggregation is None
    assert initial.spatial_interactions[0].k == 0
