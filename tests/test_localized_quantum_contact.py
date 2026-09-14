"""Independent inventory, timing and interference checks for localized contacts."""

import json
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from threading import Event

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import unpack
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.initialization import parse_initial_state
from event_universe.integration.contact_runtime import ContactEventResolver
from event_universe.quantum.event_rules import LocalInstrument, LocalUnitary
from event_universe.runner import run_initialization

from .test_quantum_event_network import matrix, probability

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/quantum/localized_charge.json"
ROTATION = [[5, 0, 0, 0], [0, 3, -4, 0], [0, 4, 3, 0], [0, 0, 0, 5]]
INVERSE = [[5, 0, 0, 0], [0, 3, 4, 0], [0, -4, 3, 0], [0, 0, 0, 5]]


def configuration(fields=True):
    raw = json.loads(EXAMPLE.read_text())
    if not fields:
        raw.pop("spatial_fields")
        raw.pop("emissions")
    return raw


def world_for(raw):
    world = Simulation(parse_initial_state(raw))
    assert isinstance(world._resolver, ContactEventResolver)
    return world, world._resolver


def step(world, count):
    for _ in range(count):
        world.step()
        assert world.totals()["charge"] == (-1,)
        assert world.totals()["mass"] == (1,)


def localized(world):
    return [
        (address, r.type_index)
        for address, node in world.nodes.items()
        for r in node.records
        if r is not None and r.type_index in (0, 1)
    ]


def test_contact_birth_capture_and_finite_local_field_source():
    world, resolver = world_for(configuration())
    assert not resolver.space.waves.names
    step(world, 1)
    assert localized(world) == []
    assert {tuple(node["position"]) for node in world.snapshot()["event_support"]} == {
        (1, 1, 1),
        (2, 1, 1),
    }
    assert resolver.report()["quantum_inventory"]["charge"] == (-1,)
    origin = resolver.space.waves.names["charge_mode"]
    assert world.event_space.event(origin).tick == 0
    assert probability(resolver.space.query(1)) == 1
    assert world.source_totals()["electric_signal"] == (-6,)
    step(world, 1)
    assert probability(resolver.space.query(2)) == 1
    assert localized(world) == []
    assert world.source_totals()["electric_signal"] == (-6,)
    step(world, 1)
    assert localized(world) == [((3, 1, 1), 1)]
    assert resolver.report()["quantum_inventory"]["charge"] == (0,)
    assert all(probability(resolver.space.query(q)) == 0 for q in range(3))
    assert world.event_space.resolution(origin) is not None
    assert resolver.draws == 0
    # Capture at tick 2 occurs after the field source phase. Its new source
    # first runs at tick 3, without editing or duplicating previously emitted stock.
    assert world.source_totals()["electric_signal"] == (-6,)
    step(world, 17)
    assert world.source_totals()["electric_signal"] == (-18,)
    assert all(not bank.origins for bank in resolver.space.waves.banks.values())
    assert resolver.wave_control_cost > 0
    assert all(not node_state_violations(node) for node in world._nodes.values())


@pytest.mark.parametrize("missing", ["partner", "unknown_marker"])
def test_no_contact_or_defined_zero_momentum_does_not_activate(missing):
    raw = configuration(False)
    raw["fields"].append(
        {
            "name": "momentum",
            "components": 3,
            "units": "test",
            "signed": True,
            "conserved": False,
            "extensive": False,
        }
    )
    for kind in raw["disturbance_types"][:2]:
        kind["fields"].append("momentum")
        kind["defaults"]["momentum"] = [0, 0, 0]
    if missing == "partner":
        raw["seeds"].pop(1)
    else:
        raw["seeds"][0]["values"] = {"momentum_known": 1}
    world, resolver = world_for(raw)
    step(world, 4)
    assert not resolver.space.waves.names
    assert localized(world) == [((1, 1, 1), 0)]
    assert all(probability(resolver.space.query(q)) == 0 for q in range(3))


def test_computation_delay_preserves_source_and_capture_ownership_until_commit():
    raw = configuration(False)
    raw["normal_budget"] = 1
    domain = raw["event_program"]["domains"][0]
    domain["phases"].extend([[], [], [], []])
    world, resolver = world_for(raw)
    step(world, 1)
    pending = world.nodes[(1, 1, 1)].pending
    assert pending.ready_tick == 5  # C=6, B=1, h=1: (ceil(C/B)-1)*h.
    assert {slot for slot, _ in pending.plan.replacements} == {0, 1}
    assert not resolver.space.waves.names
    assert localized(world) == [((1, 1, 1), 0)]
    step(world, 4)
    assert localized(world) == []
    assert resolver.report()["contact_transfers"][0]["tick"] == 5
    step(world, 3)
    assert probability(resolver.space.query(2)) == 1
    assert world.nodes[(3, 1, 1)].pending.ready_tick == 11
    assert localized(world) == []
    step(world, 3)
    assert localized(world) == [((3, 1, 1), 1)]
    assert resolver.report()["contact_transfers"][-1]["tick"] == 11


def test_arrival_uses_spare_slot_while_empty_capture_output_is_reserved():
    raw = configuration(False)
    raw["normal_budget"] = 1
    raw["event_program"]["domains"][0]["phases"].extend([[], [], [], []])
    raw["disturbance_types"].append(
        {
            "name": "messenger",
            "fields": ["mass"],
            "defaults": {"mass": 0},
            "transport": {"mode": "move", "weights": [1, 0, 0, 0, 0, 0]},
        }
    )
    raw["seeds"].append({"position": [2, 1, 1], "type": "messenger"})
    world, resolver = world_for(raw)
    step(world, 1)
    pending = world.nodes[(3, 1, 1)].pending
    assert pending.ready_tick == 5
    assert {slot for slot, _ in pending.plan.replacements} == {0, 1}
    before = world.nodes[(3, 1, 1)].records
    assert before[1:] == (None, None)
    step(world, 3)
    arrived = world.nodes[(3, 1, 1)]
    assert arrived.pending == pending
    assert arrived.records[:2] == before[:2]
    assert arrived.records[2].type_index == 3
    assert all(packet is None for packets in world.links.values() for packet in packets)
    step(world, 7)
    assert localized(world) == [((3, 1, 1), 1)]
    assert world.nodes[(3, 1, 1)].records[2] == arrived.records[2]
    assert resolver.report()["contact_transfers"][-1]["tick"] == 11


def test_split_recombine_retains_phase_without_a_classical_hidden_carrier():
    raw = configuration(False)
    domain = raw["event_program"]["domains"][0]
    domain["capture"]["register_indices"] = []
    domain["phases"] = [
        [{"register_indices": [0, 1], "matrix": ROTATION}],
        [{"register_indices": [0, 1], "matrix": INVERSE}],
    ]
    world, resolver = world_for(raw)
    step(world, 1)
    assert probability(resolver.space.query(0)) == Fraction(9, 25)
    assert probability(resolver.space.query(1)) == Fraction(16, 25)
    assert localized(world) == []
    step(world, 1)
    assert probability(resolver.space.query(0)) == 1
    assert probability(resolver.space.query(1)) == 0
    assert resolver.draws == 0


def test_moving_disturbance_activates_only_after_actual_local_arrival():
    raw = configuration(False)
    raw["fields"].append(
        {
            "name": "heading",
            "components": 3,
            "units": "route",
            "signed": True,
            "conserved": False,
            "extensive": False,
        }
    )
    raw["disturbance_types"][0]["fields"].append("heading")
    raw["disturbance_types"][0]["defaults"]["heading"] = [1, 0, 0]
    raw["disturbance_types"][0]["transport"] = {"mode": "move", "direction_field": "heading"}
    raw["seeds"][0]["position"] = [0, 1, 1]
    world, resolver = world_for(raw)
    step(world, 1)
    assert not resolver.space.waves.names
    assert localized(world) == [((1, 1, 1), 0)]
    step(world, 4)
    transfers = resolver.report()["contact_transfers"]
    assert [(t["direction"], t["tick"]) for t in transfers] == [("to_quantum", 1), ("to_localized", 4)]
    assert localized(world) == [((3, 1, 1), 1)]


@pytest.mark.parametrize("ticket", list(range(25)))
def test_capture_exhaustive_born_tickets_keep_one_inventory(ticket):
    raw = configuration(False)
    domain = raw["event_program"]["domains"][0]
    domain["phases"][0][0]["matrix"] = ROTATION
    raw["event_program"]["tickets"] = [ticket]
    world, resolver = world_for(raw)
    step(world, 3)
    clicked = ticket >= 9
    assert bool(localized(world)) == clicked
    assert resolver.draws == 1
    assert resolver.report()["quantum_inventory"]["charge"] == ((0,) if clicked else (-1,))
    assert resolver.space.records[-1].decision.weights == (9, 16)
    assert resolver.space.records[-1].outcome == int(clicked)


def test_spatial_response_preserves_all_coupled_residents_in_contact_transaction():
    raw = configuration()
    raw["boundary"] = "periodic"
    raw["disturbance_types"][2]["fields"].append("charge")
    raw["disturbance_types"][2]["defaults"]["charge"] = 0
    raw["spatial_fields"].append(
        {
            "field": "charge",
            "baseline": 0,
            "transport": "outward",
            "decay": {"retain_numerator": 1, "retain_denominator": 2},
        }
    )
    raw["spatial_couplings"] = [
        {
            "name": "probe_exchange",
            "type": "contact_probe",
            "field": "charge",
            "mode": "exchange",
            "amount": 1,
            "budget": 1,
        }
    ]
    raw["seeds"].append({"position": [1, 1, 1], "type": "contact_probe"})
    world, _ = world_for(raw)
    step(world, 1)
    assert [unpack(r.values[0]) for r in world.nodes[(1, 1, 1)].records if r is not None] == [
        (-1,),
        (-1,),
    ]
    step(world, 5)


@pytest.mark.parametrize("axis", range(3))
@pytest.mark.parametrize("sign", [-1, 1])
def test_closed_domain_coherent_link_wraps_on_every_axis(axis, sign):
    raw = configuration(False)
    raw["shape"] = [3, 3, 3]
    raw["boundary"] = "periodic"
    points = []
    for offset in range(3):
        point = [1, 1, 1]
        point[axis] = ((2 if sign == 1 else 0) + sign * offset) % 3
        points.append(point)
    raw["event_program"]["addresses"] = points
    raw["seeds"][0]["position"] = points[0]
    raw["seeds"][1]["position"] = points[0]
    raw["seeds"][2]["position"] = points[2]
    world, resolver = world_for(raw)
    step(world, 3)
    assert localized(world) == [(tuple(points[2]), 1)]
    assert resolver.space.physical_ticks[2] >= 2


def test_link_transit_bounds_the_quantum_front():
    raw = configuration(False)
    raw["link_ticks"] = 3
    world, resolver = world_for(raw)
    step(world, 2)
    assert probability(resolver.space.query(0)) == 1
    assert not resolver.space.waves.banks[(2, 1, 1)].origins
    step(world, 1)
    assert probability(resolver.space.query(1)) == 1
    step(world, 2)
    assert probability(resolver.space.query(2)) == 0
    step(world, 1)
    assert probability(resolver.space.query(2)) == 1


@pytest.mark.parametrize("invalid", ["inventory", "capacity", "budget", "gate", "capture", "force"])
def test_invalid_contact_rejects_without_sampling_or_partial_conversion(invalid):
    raw = configuration(False)
    domain = raw["event_program"]["domains"][0]
    if invalid == "inventory":
        raw["seeds"][0]["values"] = {"mass": 2}
    elif invalid == "capacity":
        raw["seeds"] = [raw["seeds"][0]] + [deepcopy(raw["seeds"][2]) for _ in range(3)]
    elif invalid == "budget":
        raw = configuration()
        raw["emissions"][0].pop("budget")
    elif invalid == "gate":
        domain["phases"][0] = [{"register_indices": [0], "matrix": [[0, 1], [1, 0]]}]
    elif invalid == "capture":
        domain["capture"]["instrument"][1] = [[0, 0], [0, 1]]
    else:
        domain["source"]["force"] = 1
    if invalid not in ("inventory", "capacity"):
        with pytest.raises(ValueError):
            parse_initial_state(raw)
        return
    world, resolver = world_for(raw)
    before = world.totals()
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    assert resolver.draws == 0
    assert not resolver.space.waves.names
    assert world.totals() == before


def test_quantum_semantic_owner_rejects_nonconserving_bypass():
    world, resolver = world_for(configuration(False))
    step(world, 1)
    origin = resolver.space.waves.names["charge_mode"]
    before = resolver.space.joint_density()
    with pytest.raises(ValueError, match="preserve occupation"):
        resolver.space.step(
            ((LocalUnitary(matrix([[0, 1], [1, 0]])), (0,)),), origin_groups=((origin,),)
        )
    with pytest.raises(ValueError, match="capture requires"):
        resolver.space.prepare(900, 1, LocalInstrument((matrix([[0, 1], [1, 0]]),)))
    assert resolver.space.joint_density() == before


def test_physical_labels_are_data_during_active_conversion_and_emission():
    raw = configuration()
    replacements = {
        "charge": "inventory_a",
        "mass": "inventory_b",
        "momentum_known": "validity",
        "electric_signal": "signal",
        "incoming_charge": "before",
        "localized_charge": "after",
        "contact_probe": "probe",
        "charge_mode": "mode",
    }

    def renamed(value):
        if isinstance(value, dict):
            return {replacements.get(k, k): renamed(v) for k, v in value.items()}
        if isinstance(value, list):
            return [renamed(v) for v in value]
        return replacements.get(value, value) if isinstance(value, str) else value

    left, left_resolver = world_for(raw)
    right, right_resolver = world_for(renamed(raw))
    for _ in range(8):
        left.step()
        right.step()
        assert left.nodes == right.nodes
        assert {replacements.get(k, k): v for k, v in left.totals().items()} == right.totals()
    assert (
        len(left_resolver.report()["contact_transfers"])
        == len(right_resolver.report()["contact_transfers"])
        == 2
    )


def test_primary_runner_records_localized_output_headlessly(tmp_path):
    output = tmp_path / "contact_run"
    run_initialization(EXAMPLE, output)
    report = json.loads((output / "run.json").read_text())["computation"]
    assert report["resolver"]["classical_field_source"] == "localized_events_only"
    assert len(report["resolver"]["contact_transfers"]) == 2
    assert not list(output.glob("*.html"))
    assert not list(output.glob("*.png"))


def test_new_classical_field_front_starts_at_capture_and_obeys_link_time():
    raw = configuration()
    raw["emissions"] = [raw["emissions"][1]]
    raw["emissions"][0]["amount"] = -48
    raw["emissions"][0]["budget"] = 48
    raw["spatial_fields"][0].update(
        axis_weights=[1, 0, 0], decay={"retain_numerator": 9, "retain_denominator": 10}
    )
    world, _ = world_for(raw)
    step(world, 3)
    assert world.source_totals()["electric_signal"] == (0,)
    step(world, 1)
    assert world.source_totals()["electric_signal"] == (-48,)
    assert world.spatial_values((4, 1, 1))["electric_signal"]["value"] != (0,)
    assert world.spatial_values((5, 1, 1))["electric_signal"]["value"] == (0,)
    step(world, 1)
    assert world.spatial_values((5, 1, 1))["electric_signal"]["value"] != (0,)


def test_remote_capture_does_not_change_unconditional_local_click_rate_or_cost():
    counts = []
    for remote_detector in (False, True):
        clicked = 0
        for ticket in range(25):
            raw = configuration(False)
            domain = raw["event_program"]["domains"][0]
            domain["phases"] = [[{"register_indices": [0, 1], "matrix": ROTATION}], [], []]
            domain["capture"]["register_indices"] = [0, 1] if remote_detector else [1]
            raw["seeds"][2]["position"] = [2, 1, 1]
            raw["event_program"]["tickets"] = [ticket]
            world, resolver = world_for(raw)
            step(world, 2)
            clicked += int(((2, 1, 1), 1) in localized(world))
            assert world.nodes[(2, 1, 1)].last_cost == 6
            assert resolver.draws == 1
        counts.append(clicked)
    assert counts == [16, 16]


def test_concurrent_inventory_read_cannot_observe_half_a_conversion(monkeypatch):
    world, resolver = world_for(configuration(False))
    selected, release, reading = Event(), Event(), Event()
    original = resolver.commit_choice

    def paused(context, token, following_events):
        result = original(context, token, following_events)
        if context.address == (1, 1, 1):
            selected.set()
            assert release.wait(5)
        return result

    monkeypatch.setattr(resolver, "commit_choice", paused)

    def read():
        reading.set()
        return world.totals()

    with ThreadPoolExecutor(max_workers=2) as pool:
        advancing = pool.submit(world.step)
        try:
            assert selected.wait(5)
            result = pool.submit(read)
            assert reading.wait(5)
            assert not result.done()
        finally:
            release.set()
        advancing.result(timeout=5)
        assert result.result(timeout=5)["charge"] == (-1,)
