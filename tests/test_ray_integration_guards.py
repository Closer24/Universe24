"""Independent integration boundaries for funded and phased local ray rules."""

import json
import math
import sys
from copy import deepcopy
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import CostMeter, pack, unpack
from event_universe.core.spatial_state import Ray, SpatialFieldDefinition, phase_cosines, phase_sines
from event_universe.fields.spatial_plan import SpatialLaw
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_energy_audit import CENTER, absorbing_document, document, records_of
from .test_kerengonen import two_lamps


def _record(world, type_index):
    return next(
        record
        for node in world.nodes.values()
        for record in node.records
        if record is not None and record.type_index == type_index
    )


def _law(initial):
    return SpatialLaw(
        initial.fields,
        initial.spatial_fields,
        initial.emissions,
        initial.operation_costs,
        absorptions=tuple(rule for rule in initial.spatial_couplings if rule.mode == "absorb"),
        sampling_profile=initial.sampling_profile,
    )


def test_runner_counts_funded_ray_momentum_through_absorption_and_escape(tmp_path):
    raw = absorbing_document(
        headings=[[1, 0, 0], [0, 2, 0]],
        rays_per_tick=2,
        absorber_position=[3, 0, 0],
        ticks=12,
    )
    raw["spatial_fields"][0]["kerengonen"] = {"phase_steps": 4, "phase_advance": 1}
    source = tmp_path / "funded.json"
    source.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(source, tmp_path / "run", ticks=12)
    metadata = json.loads((tmp_path / "run" / "run.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "completed"
    assert metadata["completed_ticks"] == 12
    # This legacy flag compares only in-domain totals; open escape changes them.
    # The accounting flag and local event audit include the escaped inventory.
    assert not metadata["conserved_at_every_completed_tick"]
    assert metadata["accounting_balanced_at_every_completed_tick"]
    audit = metadata["local_conservation"]
    assert audit["status"] == "passed"
    # The +x stream is absorbed. Five +y rays have escaped, each carrying
    # one quantum and the configured heading (0, 2, 0).
    assert audit["escaped"] == {"energy": 5, "momentum": [0, 10, 0]}
    assert audit["current"] == {"energy": 595, "momentum": [0, -10, 0]}
    assert metadata["final_totals"]["momentum"] == [0, -10, 0]
    assert metadata["escaped_totals"]["momentum"] == [0, 10, 0]


def test_physical_stepping_never_constructs_trigonometric_law_tables():
    from event_universe.core import spatial_state

    # A fresh phase count and empty old caches make the first-step regression
    # visible even when other tests constructed simpler phase tables already.
    for name in ("_COSINE_TABLES", "_SINE_TABLES"):
        table = getattr(spatial_state, name, None)
        if table is not None:
            table.clear()
    # 32 phase steps: a power of two (the phase modulus is a mask) that no other
    # test prepares.
    world = Simulation(parse_initial_state(two_lamps(32, 1, absorber=0)))
    # Prepared laws remain sufficient even after all host cache entries disappear.
    for builder in (spatial_state.phase_cosines, spatial_state.phase_sines):
        clear = getattr(builder, "cache_clear", None)
        if clear is not None:
            clear()

    def reject_table_construction(frame, event, arg):
        if event == "call" and frame.f_code.co_name in ("_fixed_cosine", "_fixed_sine"):
            raise AssertionError("physical stepping constructed trigonometric law data")

    previous = sys.getprofile()
    sys.setprofile(reject_table_construction)
    try:
        for _ in range(5):
            world.step()
    finally:
        sys.setprofile(previous)
    assert world.conservation_report()["status"] == "passed"


@pytest.mark.parametrize("steps", [3, 37, 4096])
def test_prepared_phase_tables_match_an_independent_circle_at_supported_bounds(steps):
    # The table builders take any count from 2 to 4096; a field declares a power of
    # two (wave-ray-family-v1: the phase modulus is a mask), so the odd counts are
    # checked through the builders and the maximum through a field as well.
    tables = (phase_cosines(steps), phase_sines(steps))
    if steps & (steps - 1) == 0:
        definition = SpatialFieldDefinition(
            0,
            pack((0,)),
            transport="ray",
            headings=((1, 0, 0),),
            rays_per_tick=1,
            ray_slots=1,
            phase_steps=steps,
        )
        assert (definition.cosine_table, definition.sine_table) == tables
        assert definition.phase_bits == steps.bit_length() - 1
    else:
        with pytest.raises(ValueError, match="power of two"):
            SpatialFieldDefinition(
                0,
                pack((0,)),
                transport="ray",
                headings=((1, 0, 0),),
                rays_per_tick=1,
                ray_slots=1,
                phase_steps=steps,
            )
    # Floating point is confined to this independent observer expectation; the
    # prepared law contains only bounded integer entries, including at maximum P.
    for table, function in zip(tables, (math.cos, math.sin), strict=True):
        assert type(table) is tuple and len(table) == steps
        assert all(type(value) is int and -256 <= value <= 256 for value in table)
        assert table == tuple(round(256 * function(2 * math.pi * step / steps)) for step in range(steps))


def test_self_exclusion_distinguishes_a_foreign_wave_phase_on_the_same_line():
    raw = two_lamps(4, 1)
    raw["spatial_fields"][0]["self_exclusion"] = True
    raw["spatial_couplings"][0]["type"] = "lamp_a"
    initial = parse_initial_state(raw)
    record = replace(
        _record(Simulation(initial), 0),
        channel_code=2,
        emission_departed=(pack((4, 0, 0, -1)), pack((0, 0, 0, 0))),
    )
    # The own ray carries its emission event (2 through +X and 2 through -X) and
    # one Link walked; the foreign ray differs in its wave phase only.
    own = Ray(0, (0, 0, 0), 2, 1, steps=1, event_ports=0b000011, event_shares=(2, 2, 0, 0, 0, 0))
    foreign = replace(own, phase=2)
    residents, records = [own, foreign], [record]
    taken = _law(initial)._absorb(0, residents, records, CostMeter(initial.operation_costs))
    # The two wave phases differ by a quarter turn: coherence is one half.
    # Only the phase-1 ray matches the emitter's previous local departure.
    assert taken == 1
    assert residents == [own, replace(foreign, amount=1)]
    assert unpack(records[0].values[0]) == (401,)
    assert unpack(records[0].values[1]) == (1, 0, 0)


def test_self_exclusion_keeps_the_departed_advance_and_distinguishes_a_foreign_one():
    raw = two_lamps(16, 1)
    raw["spatial_fields"][0]["self_exclusion"] = True
    raw["spatial_couplings"][0]["type"] = "lamp_a"
    raw["emissions"][0]["kerengonen_advance"] = {
        "amount": {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]},
        "denominator": 1,
    }
    initial = parse_initial_state(raw)
    record = replace(
        _record(Simulation(initial), 0),
        values=(pack((400,)), pack((7, 0, 0))),
        channel_code=2,
        emission_departed=(pack((4, 0, 0, 3)), pack((0, 0, 0, 0))),
    )
    own = Ray(0, (0, 0, 0), 2, 3, 3, steps=1, event_ports=0b000011, event_shares=(2, 2, 0, 0, 0, 0))
    foreign = replace(own, advance=5)
    residents, records = [own, foreign], [record]
    taken = _law(initial)._absorb(0, residents, records, CostMeter(initial.operation_costs))
    # Both rays have the same phase here, so coherence is one. The emitter's
    # current momentum would select advance 7; its actual departed ray carried 3.
    # The foreign ray with advance 5 is distinguishable and must be absorbed.
    assert taken == 2 and residents == [own]
    assert unpack(records[0].values[0]) == (402,)
    assert unpack(records[0].values[1]) == (9, 0, 0)
    assert unpack(records[0].absorbed_phases[0]) == (3, 5, 0)


@pytest.mark.parametrize("advance,next_phase", [(-1, 6), (0, 5), (7, 12)])
def test_carried_phase_uses_the_largest_absorbed_share_advance(advance, next_phase):
    initial = parse_initial_state(two_lamps(16, 1, absorber=0))
    records = [_record(Simulation(initial), 2)]
    residents = [Ray(0, (0, 0, 0), 1, 5, 2), Ray(1, (0, 0, 0), 3, 5, advance)]
    law = _law(initial)
    assert law._absorb(0, residents, records, CostMeter(initial.operation_costs)) == 4
    assert not residents
    assert unpack(records[0].values[0]) == (4,)
    assert unpack(records[0].values[1]) == (-2, 0, 0)
    # Largest-share inheritance is the configured candidate's policy. Explicit
    # zero must remain zero; only -1 selects the field's one-step advance.
    assert unpack(records[0].absorbed_phases[0]) == (5, advance, 1)
    assert law._carried_phase(records[0], initial.spatial_fields[0]) == (next_phase, advance, 1)


def test_exhausted_emission_clears_departure_bookkeeping_before_a_later_move():
    raw = document(headings=[[1, 0, 0]], rays_per_tick=1, amount=1, source=True, recoil=False)
    del raw["conservation"]
    raw["schema_version"] = 2
    raw["spatial_fields"][0].update(
        {
            "self_exclusion": True,
            "kerengonen": {"phase_steps": 4, "phase_advance": 1},
            "decay": {"retain_numerator": 0, "retain_denominator": 1, "residue": "dissipate"},
        }
    )
    raw["emissions"][0].update({"budget": 1, "kerengonen_phase": 2})
    raw["disturbance_types"][0]["defaults"]["momentum"] = [1, 0, 0]
    raw["disturbance_types"][0]["transport"] = {
        "mode": "move",
        "direction_field": "momentum",
        "rate": 1,
        "rate_denominator": 3,
    }
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert unpack(_record(world, 0).emission_last[0]) == (1, 0, 2, -1)
    assert unpack(_record(world, 0).emission_remaining[0]) == (0,)
    world.step()
    assert unpack(_record(world, 0).emission_last[0]) == (0, 0, 0, 0)
    world.step()
    # Departure happens two cycles after the only emission. It cannot claim
    # that an old, already dissipated ray traveled alongside this move.
    assert unpack(_record(world, 0).emission_departed[0]) == (0, 0, 0, 0)


@pytest.mark.parametrize("moving", [False, True])
def test_delayed_funded_owner_is_rejected_before_a_stale_plan_can_commit(moving):
    raw = document(headings=[[1, 0, 0], [-1, 0, 0]], rays_per_tick=2, amount=2)
    raw["normal_budget"] = 10
    if moving:
        raw["disturbance_types"][0]["defaults"]["momentum"] = [1, 0, 0]
        raw["disturbance_types"][0]["transport"] = {
            "mode": "move",
            "direction_field": "momentum",
            "rate": 1,
            "rate_denominator": 1,
        }
    world = Simulation(parse_initial_state(raw))
    with pytest.raises(ValueError, match="delay|independent"):
        world.step()
    assert all(node.pending is None for node in world.nodes.values())
    assert world.totals()["energy"] == (600,)
    assert world.conservation_report()["status"] == "passed"


def test_each_absorption_field_takes_its_own_whole_rays_without_a_draw():
    raw = absorbing_document(headings=[[1, 0, 0]], rays_per_tick=1, absorber_position=[1, 0, 0])
    del raw["conservation"]
    raw["fields"].append({**raw["fields"][0], "name": "other_quanta"})
    absorber = raw["disturbance_types"][1]
    absorber["fields"].append("other_quanta")
    absorber["defaults"]["other_quanta"] = 0
    raw["spatial_fields"].append({**raw["spatial_fields"][0], "field": "other_quanta"})
    for field in raw["spatial_fields"]:
        field["kerengonen"] = {"phase_steps": 4, "phase_advance": 1, "capture": "threshold"}
    raw["spatial_couplings"].append(
        {**raw["spatial_couplings"][0], "name": "other_absorption", "field": "other_quanta"}
    )
    initial = parse_initial_state(raw)
    records = [_record(Simulation(initial), 1)]
    law = _law(initial)
    names = [field.name for field in initial.fields]
    for index, name in ((0, raw["spatial_fields"][0]["field"]), (1, "other_quanta")):
        rays = [Ray(0, (0, 0, 0), 1, 0)]
        before = unpack(records[0].values[names.index(name)])[0]
        assert law._absorb(index, rays, records, CostMeter(initial.operation_costs)) == 1
        assert not rays
        # A lone ray is fully coherent, so the threshold takes it whole on its own
        # field; the record keeps no ticket row because nothing here draws.
        assert unpack(records[0].values[names.index(name)])[0] == before + 1
    assert not hasattr(records[0], "absorb_tickets")


@pytest.mark.parametrize("stock,remaining,momentum", [(0, 0, 0), (1, 1, 0), (2, 0, -2)])
def test_negative_threshold_capture_takes_a_whole_funded_ray_or_nothing(stock, remaining, momentum):
    raw = absorbing_document(
        headings=[[1, 0, 0]],
        rays_per_tick=1,
        absorber_position=[3, 0, 0],
        amount=-2,
        stock=stock,
        signed=True,
        ticks=4,
    )
    raw["spatial_fields"][0]["kerengonen"] = {
        "phase_steps": 4,
        "phase_advance": 1,
        "capture": "threshold",
    }
    world = Simulation(parse_initial_state(raw))
    for _ in range(4):
        world.step()
    body = records_of(world, 1)[0]
    assert body["energy"] == (remaining,)
    assert body["momentum"] == (momentum, 0, 0)
    expected_ray = 0 if stock == 2 else -2
    assert world.spatial_values((CENTER + 4, CENTER, CENTER))["energy"]["value"] == (expected_ray,)
    assert world.conservation_report()["status"] == "passed"


@pytest.mark.parametrize("target", ["routing", "unrelated_field"])
def test_funded_field_plan_cannot_modify_unrelated_carrier_state(target):
    raw = document(headings=[[1, 0, 0], [-1, 0, 0]], rays_per_tick=2, amount=2)
    raw["fields"].append({**raw["fields"][0], "name": "other_stock"})
    raw["disturbance_types"][0]["fields"].append("other_stock")
    raw["disturbance_types"][0]["defaults"]["other_stock"] = 0
    world = Simulation(parse_initial_state(raw))
    before = _record(world, 0)
    planner = world._spatial.planner

    def corrupt(*args):
        plan = planner(*args)
        records = list(plan.emission_records)
        record = records[0]
        if target == "routing":
            records[0] = replace(record, channel_code=7)
        else:
            values = list(record.values)
            values[2] = pack((1,))
            records[0] = replace(record, values=tuple(values))
        return replace(plan, emission_records=tuple(records))

    world._spatial._services = replace(world._spatial._services, planner=corrupt)
    with pytest.raises(ValueError):
        world.step()
    assert _record(world, 0) == before
    assert world.totals()["energy"] == (600,)


def test_phased_self_exclusion_cannot_use_a_scalar_response_subtraction():
    raw = two_lamps(4, 1)
    del raw["conservation"]
    for emission in raw["emissions"]:
        del emission["recoil_field"]
    del raw["spatial_couplings"][0]["momentum_field"]
    raw["spatial_fields"].append({"field": "momentum", "transport": "outward", "baseline": [0, 0, 0]})
    raw["spatial_couplings"].append(
        {
            "name": "respond_to_ray_flux",
            "type": "lamp_a",
            "field": "momentum",
            "mode": "exchange",
            "amount": {"flux": "quanta"},
            "denominator": 1,
        }
    )
    assert parse_initial_state(raw)
    raw["spatial_fields"][0]["self_exclusion"] = True
    with pytest.raises(ValueError, match="self.exclusion|phased|kerengonen"):
        parse_initial_state(raw)


def test_attenuated_self_exclusion_cannot_subtract_the_original_emission():
    raw = two_lamps(4, 1)
    del raw["conservation"]
    raw["schema_version"] = 2
    del raw["spatial_fields"][0]["kerengonen"]
    decay = {"retain_numerator": 0, "retain_denominator": 1, "residue": "dissipate"}
    raw["spatial_fields"][0]["decay"] = decay
    raw["spatial_fields"].append(
        {"field": "momentum", "transport": "outward", "baseline": [0, 0, 0], "decay": decay}
    )
    for emission in raw["emissions"]:
        emission.update({"source": True, "budget": 8})
        del emission["recoil_field"]
        emission.pop("kerengonen_phase", None)
    raw["spatial_couplings"] = [
        {
            "name": "respond_to_attenuated_flux",
            "type": "lamp_a",
            "field": "momentum",
            "mode": "exchange",
            "amount": {"flux": "quanta"},
            "denominator": 1,
            "budget": [8, 8, 8],
        }
    ]
    assert parse_initial_state(raw)
    raw["spatial_fields"][0]["self_exclusion"] = True
    # The original emission has nonzero stock; its delivered remnant is zero.
    # Subtracting the original amount cannot represent this receiver's own ray.
    with pytest.raises(ValueError, match="self.exclusion|attenuat|decay"):
        parse_initial_state(raw)


def test_ray_momentum_accounting_rejects_conflicting_owned_vector_bindings():
    raw = absorbing_document(headings=[[1, 0, 0]], rays_per_tick=1, absorber_position=[3, 0, 0])
    alternate = deepcopy(raw["fields"][1])
    alternate["name"] = "other_momentum"
    raw["fields"].append(alternate)
    raw["disturbance_types"][1]["fields"].append("other_momentum")
    raw["disturbance_types"][1]["defaults"]["other_momentum"] = [0, 0, 0]
    raw["spatial_couplings"][0]["momentum_field"] = "other_momentum"
    with pytest.raises(ValueError, match="momentum|binding"):
        parse_initial_state(raw)
