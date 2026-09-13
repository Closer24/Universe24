"""Property selection and passive validation across existing local rule owners."""

from copy import deepcopy
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.coupling_selectors import selected_types
from event_universe.core.disturbance_state import pack, unpack
from event_universe.initialization import parse_initial_state

from .test_local_field_rules import ORIGIN, document, field, invariant, local, operation
from .test_spatial_coupling_budget import apply, fixture
from .test_spatial_interactions import exchange


def record_values(world, position=ORIGIN):
    return [
        world.record_values(record) for record in world.cells[position].records if record is not None
    ]


def pair_configuration(kind):
    raw = document([field("quantity", conserved=True), field("extra")])
    raw.pop("spatial_fields")
    raw.pop("spatial_seeds")
    raw["disturbance_types"] = [
        {"name": "first", "fields": ["quantity"], "transport": {"mode": "hold"}},
        {"name": "second", "fields": ["quantity", "extra"], "transport": {"mode": "hold"}},
    ]
    raw["seeds"] = [
        {"position": list(ORIGIN), "type": "first", "values": {"quantity": 5}},
        {"position": list(ORIGIN), "type": "second", "values": {"quantity": 2}},
    ]
    left, right = {"field": "quantity"}, {"field": "quantity", "side": "right"}
    selector = {"name": "one_transfer", "left_requires": ["quantity"], "right_requires": ["quantity"]}
    if kind == "couplings":
        raw[kind] = [{**selector, "field": "quantity", "amount": 1}]
    else:
        raw[kind] = [
            {
                **selector,
                "assignments": [
                    {"side": "left", "field": "quantity", "expression": operation("sub", left, 1)},
                    {"side": "right", "field": "quantity", "expression": operation("add", right, 1)},
                ],
                "invariants": [invariant("joint_stock", operation("add", left, right))],
            }
        ]
    return raw


@pytest.mark.parametrize("kind", ["couplings", "interactions"])
def test_property_pair_visits_each_pair_once_across_different_layout_names(kind):
    raw = pair_configuration(kind)
    initial = parse_initial_state(raw)
    assert getattr(initial, kind)[0].left_types == (0, 1)
    world = Simulation(initial)
    world.step()
    assert [record["quantity"] for record in record_values(world)] == [(4,), (3,)]
    assert world.totals()["quantity"] == (7,)


@pytest.mark.parametrize("kind", ["couplings", "interactions"])
def test_partial_selector_overlap_preserves_oriented_roles_without_duplicate_exchange(kind):
    raw = pair_configuration(kind)
    raw[kind][0]["right_requires"].append("extra")
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert [record["quantity"] for record in record_values(world)] == [(4,), (3,)]


def test_spatial_rules_match_properties_and_both_drivers_update_the_same_quantity():
    raw = exchange()
    raw["fields"] += [field("responsive"), field("driver_one"), field("driver_two")]
    raw["disturbance_types"][0]["fields"].append("responsive")
    raw["disturbance_types"][0]["defaults"]["responsive"] = 1
    second = deepcopy(raw["disturbance_types"][0])
    second["name"] = "different_label"
    raw["disturbance_types"].append(second)
    raw["disturbance_types"].append(
        {
            "name": "missing_property",
            "fields": ["quantity"],
            "defaults": {"quantity": 5},
            "transport": {"mode": "hold"},
        }
    )
    positions = [ORIGIN, (1, 1, 1), (3, 3, 3)]
    raw["seeds"] = [
        {"position": list(p), "type": t["name"]}
        for p, t in zip(positions, raw["disturbance_types"], strict=True)
    ]
    raw["spatial_fields"] += [
        {"field": name, "baseline": value, "transport": "local"}
        for name, value in (("driver_one", 1), ("driver_two", 2))
    ]
    raw["spatial_interactions"] = []
    for name in ("driver_one", "driver_two"):
        amount = operation("mul", {"field": "responsive"}, local(name))
        raw["spatial_interactions"].append(
            {
                "name": name,
                "requires": ["quantity", "responsive"],
                "assignments": [
                    {
                        "side": "left",
                        "field": "quantity",
                        "expression": operation("add", {"field": "quantity"}, amount),
                    },
                    {
                        "side": "right",
                        "field": "quantity",
                        "expression": operation("sub", local("quantity"), amount),
                    },
                ],
                "invariants": [
                    invariant("joint_stock", operation("add", {"field": "quantity"}, local("quantity")))
                ],
            }
        )
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert [record_values(world, p)[0]["quantity"] for p in positions] == [(8,), (8,), (5,)]
    assert [world.spatial_values(p)["quantity"]["value"] for p in positions] == [(-1,), (-3,), (0,)]
    assert world.totals()["quantity"] == (17,)


@pytest.mark.parametrize(
    "failure",
    [
        "both",
        "neither",
        "unknown",
        "duplicate",
        "empty",
        "no_match",
        "undeclared_read",
        "undeclared_write",
        "split",
    ],
)
def test_property_selector_rejects_incomplete_or_ambiguous_ownership(failure):
    raw = exchange()
    rule = raw["spatial_interactions"][0]
    rule.pop("type")
    rule["requires"] = ["quantity"]
    raw["fields"].append(field("extra"))
    raw["disturbance_types"][0]["fields"].append("extra")
    if failure == "both":
        rule["type"] = "held"
    elif failure == "neither":
        rule.pop("requires")
    elif failure == "unknown":
        rule["requires"] = ["unknown"]
    elif failure == "duplicate":
        rule["requires"] *= 2
    elif failure == "empty":
        rule["requires"] = []
    elif failure == "no_match":
        rule["requires"] = ["extra"]
        raw["disturbance_types"][0]["fields"].remove("extra")
    elif failure == "undeclared_read":
        rule["when"] = {"field": "extra"}
    elif failure == "undeclared_write":
        rule["assignments"][0]["field"] = "extra"
    else:
        raw["disturbance_types"][0]["transport"] = {"mode": "split"}
    original = deepcopy(raw)
    with pytest.raises(ValueError):
        parse_initial_state(raw)
    assert raw == original


def test_property_selected_spatial_fraction_and_allowance_follow_every_compatible_layout():
    law, record = fixture((5,), (2,), denominator=2)
    law = replace(law, definitions=(replace(law.definitions[0], types=(0, 1)),))
    record = replace(record, type_index=1)
    for request, expected, fraction, allowance in ((1, 5, 1, 2), (1, 4, 0, 1), (2, 3, 0, 0)):
        _, record = apply(law, record, (request,))
        assert unpack(record.values[0]) == (expected,)
        assert unpack(record.spatial_remainders[0]) == (fraction,)
        assert unpack(record.spatial_remaining[0]) == (allowance,)
    _, exhausted = apply(law, record, (9,))
    assert exhausted == record
    other = replace(law.definitions[0], name="other", type_index=2, types=(2,), budget=None)
    mixed = replace(law, definitions=(*law.definitions, other))
    foreign = replace(
        record,
        type_index=2,
        spatial_remainders=(pack((1,)), pack((0,))),
        spatial_remaining=(pack((0,)), pack((0,))),
    )
    with pytest.raises(ValueError):
        apply(mixed, foreign, (1,))


def test_compiled_property_emission_and_finite_spatial_budgets_include_second_layout():
    from .test_spatial_coupling_budget import initialization

    raw = initialization(emitting=True)
    second = deepcopy(raw["disturbance_types"][0])
    second["name"] = "same_properties"
    raw["disturbance_types"].append(second)
    raw["seeds"][0]["type"] = second["name"]
    for key in ("emissions", "spatial_couplings"):
        raw[key][0].pop("type")
        raw[key][0]["requires"] = ["inventory"]
    initial = parse_initial_state(raw)
    assert selected_types(initial.emissions[0]) == (0, 1)
    assert selected_types(initial.spatial_couplings[0]) == (0, 1)
    world = Simulation(initial)
    world.step()
    records = [packet.record for group in world.links.values() for packet in group if packet is not None]
    records += [record for cell in world.cells.values() for record in cell.records if record is not None]
    assert len(records) == 1
    assert unpack(records[0].values[0]) == (0, 5, 0)
    assert unpack(records[0].spatial_remaining[0]) == (0, 0, 0)
    assert unpack(records[0].emission_remaining[0]) == (0, 0, 16)


def test_property_emission_fraction_is_owned_by_each_matching_carrier():
    from .test_spatial_engine import ORIGIN as SOURCE
    from .test_spatial_engine import document as source_document

    raw = source_document(source=True)
    raw["disturbance_types"][0]["defaults"]["strength"] = 1
    second = deepcopy(raw["disturbance_types"][0])
    second["name"] = "second_source"
    raw["disturbance_types"].append(second)
    raw["seeds"][0]["type"] = second["name"]
    raw["emissions"][0].pop("type")
    raw["emissions"][0].update(requires=["strength"], denominator=2)
    world = Simulation(parse_initial_state(raw))
    world.step()
    record = next(record for record in world.cells[SOURCE].records if record is not None)
    assert unpack(record.emission_remainders[0]) == (1,)
    assert world.source_totals()["radiation"] == (0,)
    world.step()
    record = next(record for record in world.cells[SOURCE].records if record is not None)
    assert unpack(record.emission_remainders[0]) == (0,)
    assert world.source_totals()["radiation"] == (1,)


def test_left_owned_pair_fraction_requires_disjoint_roles_and_survives_layout_variants():
    raw = pair_configuration("couplings")
    raw["fields"].append(field("left_role"))
    raw["disturbance_types"][0]["fields"].append("left_role")
    rule = raw["couplings"][0]
    rule.update(
        left_requires=["quantity", "left_role"],
        right_requires=["quantity", "extra"],
        denominator=2,
        remainder_owner="left",
    )
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert [v["quantity"] for v in record_values(world)] == [(5,), (2,)]
    world.step()
    assert [v["quantity"] for v in record_values(world)] == [(4,), (3,)]
    raw["disturbance_types"][1]["fields"].append("left_role")
    with pytest.raises(ValueError, match="disjoint"):
        parse_initial_state(raw)


def test_property_selected_conversion_is_explicitly_unsupported():
    raw = pair_configuration("interactions")
    raw["interactions"][0]["output_types"] = {"left": "first", "right": "second"}
    with pytest.raises(ValueError, match="explicit type selectors"):
        parse_initial_state(raw)


def complex_identity(expression):
    result = deepcopy(expression)
    for _ in range(8):
        result = operation("add", result, 0)
    return result


@pytest.mark.parametrize("stage", ["joint", "pair", "field", "carrier"])
def test_equivalent_validation_complexity_cannot_change_physical_cost_or_commit_tick(stage):
    raw = pair_configuration("interactions") if stage == "pair" else exchange()
    raw["normal_budget"] = 1
    if stage == "field":
        raw["field_rules"] = [
            {
                "name": "identity",
                "assignments": [{"field": "quantity", "expression": local("quantity")}],
                "invariants": [invariant("stock", local("quantity"))],
            }
        ]
    elif stage == "carrier":
        raw["disturbance_types"][0]["checks"] = [invariant("positive", 1)]
    changed = deepcopy(raw)
    collection = {"joint": "spatial_interactions", "pair": "interactions", "field": "field_rules"}
    if stage == "carrier":
        check = changed["disturbance_types"][0]["checks"][0]
    else:
        check = changed[collection[stage]][0]["invariants"][0]
    check["expression"] = complex_identity(check["expression"])
    worlds = [Simulation(parse_initial_state(value)) for value in (raw, changed)]
    for world in worlds:
        world.step()
        assert world.cells[ORIGIN].pending is not None
    pending = [world.cells[ORIGIN].pending for world in worlds]
    assert pending[0].plan.cost == pending[1].plan.cost
    assert pending[0].ready_tick == pending[1].ready_tick
    ready = pending[0].ready_tick
    for world in worlds:
        while world.tick < ready:
            world.step()
    assert record_values(worlds[0]) == record_values(worlds[1])


def test_passive_bad_invariant_still_rejects_atomically():
    raw = exchange()
    raw["spatial_interactions"][0]["invariants"] = [
        invariant("carrier_unchanged", {"field": "quantity"})
    ]
    world = Simulation(parse_initial_state(raw))
    with pytest.raises(ValueError, match="carrier_unchanged"):
        world.step()
    assert record_values(world)[0]["quantity"] == (5,)
    assert world.spatial_values(ORIGIN)["quantity"]["value"] == (2,)


def test_missing_property_is_not_a_zero_value_that_can_activate_a_rule():
    raw = exchange()
    raw["fields"].append(field("eligibility"))
    raw["disturbance_types"][0]["fields"].append("eligibility")
    raw["disturbance_types"].append(
        {
            "name": "missing",
            "fields": ["quantity"],
            "defaults": {"quantity": 5},
            "transport": {"mode": "hold"},
        }
    )
    raw["seeds"].append({"position": [1, 1, 1], "type": "missing"})
    rule = raw["spatial_interactions"][0]
    rule.pop("type")
    rule.update(requires=["quantity", "eligibility"], when=operation("eq", {"field": "eligibility"}, 0))
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert record_values(world)[0]["quantity"] == (2,)
    assert record_values(world, (1, 1, 1))[0]["quantity"] == (5,)
    assert world.spatial_values((1, 1, 1))["quantity"]["value"] == (0,)


@pytest.mark.parametrize("kind", ["couplings", "emissions", "spatial_couplings", "spatial_interactions"])
def test_legacy_conversion_conflict_checks_every_property_selected_layout(kind):
    from .test_local_conversions import document as conversion_document

    raw = conversion_document()
    raw["fields"][0]["signed"] = True
    raw["disturbance_types"].insert(
        0,
        {
            "name": "unrelated_first_match",
            "fields": ["stock", "momentum"],
            "transport": {"mode": "hold"},
        },
    )
    raw["spatial_fields"] = [{"field": "stock", "baseline": 0, "transport": "local"}]
    if kind == "couplings":
        raw[kind] = [
            {
                "name": "property_exchange",
                "left_requires": ["stock"],
                "right_requires": ["stock"],
                "field": "stock",
                "amount": 0,
            }
        ]
    elif kind == "emissions":
        raw[kind] = [{"requires": ["stock"], "field": "stock", "amount": 0, "source": True}]
    elif kind == "spatial_couplings":
        raw[kind] = [
            {
                "name": "property_exchange",
                "requires": ["stock"],
                "field": "stock",
                "mode": "exchange",
                "amount": 0,
            }
        ]
    else:
        raw[kind] = [
            {
                "name": "property_exchange",
                "requires": ["stock"],
                "assignments": [{"side": "left", "field": "stock", "expression": {"field": "stock"}}],
                "invariants": [invariant("stock", {"field": "stock"})],
            }
        ]
    with pytest.raises(ValueError, match="conversion types cannot participate"):
        parse_initial_state(raw)


def test_overlapping_property_and_legacy_emission_cannot_double_the_same_source():
    from .test_spatial_engine import document as source_document

    raw = source_document(source=True)
    overlapping = deepcopy(raw["emissions"][0])
    overlapping.pop("type")
    overlapping["requires"] = ["strength"]
    raw["emissions"].append(overlapping)
    with pytest.raises(ValueError, match="duplicate emission"):
        parse_initial_state(raw)
