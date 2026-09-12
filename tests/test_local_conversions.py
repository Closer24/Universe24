"""Bounded type conversion is inventory transfer, not established annihilation."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_state

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/known-entities/conversion.json"


def document():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def owned(world):
    records = [r for c in world.cells.values() for r in c.records if r is not None]
    records += [p.record for ps in world.links.values() for p in ps if p is not None]
    return sorted((r.type_index, world.record_values(r)) for r in records)


def test_conversion_preserves_inventory_and_transports_two_outputs_causally():
    events = []
    world = Simulation(parse_initial_state(document()), observer=events.append)
    for _ in range(6):
        world.step()
        assert world.totals() == {"stock": (5,), "momentum": (0, 0, 0)}
        assert world.source_totals() == {"stock": (0,), "momentum": (0, 0, 0)}
        assert owned(world) == [
            (2, {"stock": (2,), "momentum": (1, 0, 0)}),
            (3, {"stock": (3,), "momentum": (-1, 0, 0)}),
        ]
    sent = [e for e in events if e["event"] == "sent"]
    assert sent and all(e["arrival_tick"] == e["tick"] + 2 for e in sent)
    assert any(r is not None for r in world.cells[(7, 4, 4)].records)
    assert any(r is not None for r in world.cells[(1, 4, 4)].records)


def test_conversion_wait_keeps_original_owners_and_does_not_apply_output_defaults():
    raw = document()
    raw["normal_budget"] = 1
    for kind in raw["disturbance_types"][2:]:
        kind["defaults"]["stock"] = 999
    world = Simulation(parse_initial_state(raw))
    world.step()
    cell = world.cells[(4, 4, 4)]
    assert cell.pending is not None
    assert [i for i, _ in owned(world)] == [0, 1]
    for _ in range(200):
        world.step()
        if [i for i, _ in owned(world)] == [2, 3]:
            break
    assert [i for i, _ in owned(world)] == [2, 3]
    assert world.totals()["stock"] == (5,)


@pytest.mark.parametrize("failure", ["conservation", "invariant", "residual"])
def test_conversion_rejection_has_no_partial_type_change_or_pending_plan(failure):
    raw = document()
    if failure in ("conservation", "invariant"):
        raw["interactions"][0]["assignments"][0]["expression"] = 1
        if failure == "invariant":
            raw["fields"][0]["conserved"] = False
    initial = parse_initial_state(raw)
    if failure == "residual":
        first, second = initial.seeds
        initial = replace(
            initial, seeds=(replace(first, record=replace(first.record, rate_remainder_code=2)), second)
        )
    world = Simulation(initial)
    before = world.snapshot()
    with pytest.raises(ValueError, match="conservation|invariant|zero carried"):
        world.step()
    assert world.snapshot() == before
    assert all(cell.pending is None for cell in world.cells.values())


@pytest.mark.parametrize(
    "carried",
    [
        {"route_count_codes": (2, 1, 1, 1, 1, 1), "route_weight_codes": (2, 1, 2, 1, 1, 1)},
        {"route_weight_codes": (2, 1, 2, 1, 1, 1)},
        {"rate_credit_denominator": 2},
    ],
)
def test_conversion_cannot_discard_new_routing_registers(carried):
    initial = parse_initial_state(document())
    first, second = initial.seeds
    initial = replace(initial, seeds=(replace(first, record=replace(first.record, **carried)), second))
    world = Simulation(initial)
    before = world.snapshot()
    with pytest.raises(ValueError, match="zero carried"):
        world.step()
    assert world.snapshot() == before
    assert all(cell.pending is None for cell in world.cells.values())


@pytest.mark.parametrize(
    "failure", ["missing_payload", "same_type", "different_fields", "split", "exchange", "capacity"]
)
def test_conversion_rejects_unsupported_ownership_at_initialization(failure):
    raw = document()
    if failure == "missing_payload":
        raw["interactions"][0]["assignments"].pop()
    elif failure == "same_type":
        raw["interactions"][0]["output_types"]["left"] = "stored A"
    elif failure == "different_fields":
        kind = raw["disturbance_types"][2]
        kind["fields"].remove("stock")
        del kind["defaults"]["stock"]
    elif failure == "split":
        raw["disturbance_types"][2]["transport"] = {"mode": "split", "weights": [1, 1, 1, 1, 1, 1]}
    elif failure == "exchange":
        raw["couplings"] = [
            {
                "name": "exchange",
                "left_type": "stored A",
                "right_type": "stored B",
                "field": "stock",
                "amount": 0,
            }
        ]
    else:
        raw["slots_per_cell"] = 1
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_arbitrary_type_names_and_declaration_order_do_not_supply_conversion_physics():
    raw = document()
    baseline = Simulation(parse_initial_state(raw))
    renamed = {
        k["name"]: n
        for k, n in zip(
            raw["disturbance_types"], ["constructor", "output_types", "left", "__proto__"], strict=True
        )
    }
    for kind in raw["disturbance_types"]:
        kind["name"] = renamed[kind["name"]]
    for seed in raw["seeds"]:
        seed["type"] = renamed[seed["type"]]
    rule = raw["interactions"][0]
    for key in ("left_type", "right_type"):
        rule[key] = renamed[rule[key]]
    rule["output_types"] = {side: renamed[name] for side, name in rule["output_types"].items()}
    raw["disturbance_types"].reverse()
    variant = Simulation(parse_initial_state(raw))
    for _ in range(6):
        baseline.step()
        variant.step()
        assert baseline.totals() == variant.totals()
        assert sorted(v["stock"] for _, v in owned(baseline)) == sorted(
            v["stock"] for _, v in owned(variant)
        )
        assert sorted(3 - i for i, _ in owned(variant)) == [i for i, _ in owned(baseline)]


def test_incoming_carriers_convert_after_real_neighbor_arrival_and_reverse():
    raw = document()
    for kind in raw["disturbance_types"][:2]:
        kind["transport"] = {
            "mode": "move",
            "direction_field": "momentum",
            "rate": 1,
            "rate_denominator": 1,
        }
    raw["seeds"][0]["position"] = [3, 4, 4]
    raw["seeds"][1]["position"] = [5, 4, 4]
    for assignment in raw["interactions"][0]["assignments"]:
        if assignment["field"] == "momentum":
            assignment["expression"]["side"] = "right" if assignment["side"] == "left" else "left"
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    assert [i for i, _ in owned(world)] == [0, 1]
    world.step()
    arrivals = [r for r in world.cells[(4, 4, 4)].records if r is not None]
    assert {r.channel_code for r in arrivals} == {2, 3}
    assert {r.type_index for r in arrivals} == {0, 1}
    for _ in range(4):
        world.step()
        assert owned(world) == [
            (2, {"stock": (2,), "momentum": (-1, 0, 0)}),
            (3, {"stock": (3,), "momentum": (1, 0, 0)}),
        ]
        assert world.totals() == {"stock": (5,), "momentum": (0, 0, 0)}
    assert any(r is not None for r in world.cells[(2, 4, 4)].records)
    assert any(r is not None for r in world.cells[(6, 4, 4)].records)
    sent = [e for e in events if e["event"] == "sent"]
    assert sent and all(e["arrival_tick"] == e["tick"] + 2 for e in sent)
