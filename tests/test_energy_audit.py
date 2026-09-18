"""Funded ray emission with recoil under the local energy/momentum audit."""

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

CENTER = 7


def document(
    *, headings, rays_per_tick, energy=600, amount=2, ticks=6, source=False, recoil=True, signed=False
):
    raw = {
        "schema_version": 1,
        "model_id": "funded-ray-emission-audit-v1",
        "shape": [15, 15, 15],
        "boundary": "open",
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
                "name": "energy",
                "components": 1,
                "units": "quantum",
                "signed": signed,
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
                "name": "emitter",
                "fields": ["energy", "momentum"],
                "defaults": {"energy": energy, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "energy",
                "baseline": 0,
                "transport": "ray",
                "headings": headings,
                "rays_per_tick": rays_per_tick,
                "ray_slots": 64,
            },
        ],
        "emissions": [
            {
                "type": "emitter",
                "field": "energy",
                "amount": amount,
                "denominator": 1,
                # node-is-ports-v1: an emission on a ray family is paid from the
                # type's content and recoils into its momentum; `source` is only
                # written to be rejected.
                **({"source": True} if source else {}),
            }
        ],
        "seeds": [{"position": [CENTER] * 3, "type": "emitter"}],
        "conservation": {
            "name": "quanta",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["energy", "momentum"],
                    "energy": {"field": "energy"},
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {"field": "energy", "side": "right"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        },
    }
    return raw


def emitter(world):
    return next(world.record_values(r) for node in world.nodes.values() for r in node.records if r)


def test_funded_emission_pays_from_the_record_and_recoils_by_amount_times_heading():
    world = Simulation(parse_initial_state(document(headings=[[1, 0, 0], [0, 2, 0]], rays_per_tick=2)))
    for tick in range(1, 7):
        world.step()
        values = emitter(world)
        assert values["energy"] == (600 - 2 * tick,)
        # Each tick one unit leaves along (1,0,0) and one along (0,2,0).
        assert values["momentum"] == (-tick, -2 * tick, 0)
        assert world.totals()["energy"] == (600,)
    report = world.conservation_report()
    assert report["status"] == "passed" and report["checked_node_events"] > 0
    assert report["current"]["energy"] == 600 and tuple(report["current"]["momentum"]) == (0, 0, 0)


def test_funded_emission_is_clipped_to_the_record_stock():
    world = Simulation(
        parse_initial_state(document(headings=[[1, 0, 0]], rays_per_tick=1, energy=5, amount=2, ticks=4))
    )
    energies = []
    for _ in range(4):
        world.step()
        energies.append(emitter(world)["energy"][0])
    assert energies == [3, 1, 0, 0]
    assert world.totals()["energy"] == (5,)
    assert world.conservation_report()["status"] == "passed"


def test_audit_still_rejects_external_sources_and_recoil_needs_funding():
    # node-is-ports-v1: a source is a thing that spends its content; an unfunded
    # source and a declared recoil field are the retired form.
    with pytest.raises(ValueError, match="node-is-ports-v1"):
        parse_initial_state(document(headings=[[1, 0, 0]], rays_per_tick=1, source=True))
    raw = document(headings=[[1, 0, 0]], rays_per_tick=1)
    del raw["conservation"]
    raw["emissions"][0]["recoil_field"] = "momentum"
    with pytest.raises(ValueError, match="node-is-ports-v1"):
        parse_initial_state(raw)
    raw = document(headings=[[1, 0, 0]], rays_per_tick=1)
    raw["disturbance_types"][0]["fields"] = ["energy"]
    del raw["disturbance_types"][0]["defaults"]["momentum"]
    with pytest.raises(ValueError, match="momentum field"):
        parse_initial_state(raw)
    # Edge case: the escaping ray quanta are counted as measured escape, not loss.
    world = Simulation(
        parse_initial_state(document(headings=[[1, 0, 0]], rays_per_tick=1, amount=1, ticks=12))
    )
    for _ in range(12):
        world.step()
    report = world.conservation_report()
    assert report["status"] == "passed"
    assert report["escaped"]["energy"] == 12 - CENTER
    assert tuple(report["escaped"]["momentum"]) == (12 - CENTER, 0, 0)


def absorbing_document(
    *, headings, rays_per_tick, absorber_position, ticks=8, mover=False, amount=2, stock=0, signed=False
):
    raw = document(
        headings=headings, rays_per_tick=rays_per_tick, ticks=ticks, amount=amount, signed=signed
    )
    raw["disturbance_types"].append(
        {
            "name": "absorber",
            "fields": ["energy", "momentum"],
            "defaults": {"energy": stock, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"}
            if not mover
            else {"mode": "move", "direction_field": "momentum", "rate": 1, "rate_denominator": 1},
        }
    )
    raw["spatial_couplings"] = [
        {
            "name": "swallow",
            "type": "absorber",
            "field": "energy",
            "mode": "absorb",
            "momentum_field": "momentum",
        }
    ]
    raw["seeds"].append({"position": [CENTER + v for v in absorber_position], "type": "absorber"})
    return raw


def records_of(world, type_index):
    return [
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    ]


def test_absorber_takes_ray_quanta_with_their_momentum_and_the_audit_stays_closed():
    raw = absorbing_document(
        headings=[[1, 0, 0], [0, 2, 0]], rays_per_tick=2, absorber_position=[3, 0, 0]
    )
    world = Simulation(parse_initial_state(raw))
    for _ in range(8):
        world.step()
    absorber = records_of(world, 1)[0]
    # Rays along +x reach x = 3 at tick 3 and are absorbed on the next five cycles;
    # each carries one quantum and heading (1,0,0).
    assert absorber["energy"] == (5,) and absorber["momentum"] == (5, 0, 0)
    assert world.spatial_values((CENTER + 4, CENTER, CENTER))["energy"]["value"] == (0,)
    report = world.conservation_report()
    # Quanta along (0,2,0) left through the open boundary; nothing else is missing.
    assert world.totals()["energy"][0] + report["escaped"]["energy"] == 600
    assert report["status"] == "passed" and report["failure"] is None
    emitter_values = records_of(world, 0)[0]
    assert emitter_values["energy"] == (600 - 16,) and emitter_values["momentum"] == (-8, -16, 0)


def test_absorber_with_self_exclusion_does_not_eat_its_own_wake():
    raw = absorbing_document(
        headings=[[1, 0, 0], [-1, 0, 0]], rays_per_tick=2, absorber_position=[1, 3, 0], mover=True
    )
    raw["spatial_fields"][0]["self_exclusion"] = True
    # The absorber also emits: funded, one quantum per tick each way, and moves +x at one hop per tick.
    raw["emissions"].append(
        {
            "type": "absorber",
            "field": "energy",
            "amount": 2,
            "denominator": 1,
        }
    )
    raw["disturbance_types"][1]["defaults"] = {"energy": 40, "momentum": [1, 0, 0]}
    world = Simulation(parse_initial_state(raw))
    energies = []
    for _ in range(5):
        world.step()
        found = records_of(world, 1)
        if not found:
            break
        energies.append(found[0]["energy"][0])
    # It moves along x = 3 off the emitter's line, so the only rays it meets are its
    # own +x quanta arriving with it at every new Node. Self-exclusion is one-Link
    # exclusion of the cycle it departed on: that quantum is never absorbed back.
    # The +x quantum of the cycle before travels with it too, but as the ray of
    # an earlier event (two Links walked) it no longer merges with the excluded
    # one (ray-event-state-v1). Re-pinned on 2026-09-18 with feature 18 (lanes-v1,
    # Highlights 5.4 point 25): the quantum of the cycle before and the one
    # emitted with it leave the Node on one lane as one real ray of two quanta
    # with the older event's record, which the one-Link exclusion does not name,
    # so from the third tick on the absorber takes the two back every other tick.
    assert energies == [38, 36, 36, 34, 34]
    assert world.conservation_report()["status"] == "passed"


def test_absorb_mode_is_validated():
    raw = absorbing_document(headings=[[1, 0, 0]], rays_per_tick=1, absorber_position=[2, 0, 0])
    raw["spatial_couplings"][0]["momentum_field"] = "energy"
    with pytest.raises(ValueError, match="momentum_field"):
        parse_initial_state(raw)
    raw = absorbing_document(headings=[[1, 0, 0]], rays_per_tick=1, absorber_position=[2, 0, 0])
    raw["spatial_couplings"][0]["amount"] = 1
    with pytest.raises(ValueError, match="unknown keys"):
        parse_initial_state(raw)


def test_a_fraction_absorbs_part_of_each_ray_and_forwards_the_rest():
    raw = absorbing_document(
        headings=[[1, 0, 0]], rays_per_tick=1, absorber_position=[3, 0, 0], amount=4, ticks=8
    )
    raw["spatial_couplings"][0].update({"fraction": 1, "fraction_denominator": 4})
    world = Simulation(parse_initial_state(raw))
    for _ in range(8):
        world.step()
    absorber = records_of(world, 1)[0]
    # Five rays of 4 quanta arrive from tick 4 on; one quantum of each is absorbed
    # and three continue: the Node beyond holds the 3-quantum remainder in flight.
    assert absorber["energy"] == (5,) and absorber["momentum"] == (5, 0, 0)
    assert world.spatial_values((CENTER + 4, CENTER, CENTER))["energy"]["value"] == (3,)
    report = world.conservation_report()
    assert report["status"] == "passed"
    assert world.totals()["energy"][0] + report["escaped"]["energy"] == 600
    # A fraction at or above one absorbs whole rays; a bare denominator is rejected.
    raw["spatial_couplings"][0].update({"fraction": 8, "fraction_denominator": 4})
    world = Simulation(parse_initial_state(raw))
    for _ in range(8):
        world.step()
    assert records_of(world, 1)[0]["energy"] == (20,)
    del raw["spatial_couplings"][0]["fraction"]
    with pytest.raises(ValueError, match="fraction_denominator requires"):
        parse_initial_state(raw)


def test_negative_quanta_pull_the_absorber_toward_the_emitter_and_it_pays_from_its_stock():
    raw = absorbing_document(
        headings=[[1, 0, 0]],
        rays_per_tick=1,
        absorber_position=[3, 0, 0],
        amount=-2,
        stock=3,
        signed=True,
        ticks=8,
    )
    world = Simulation(parse_initial_state(raw))
    stocks, momenta = [], []
    for _ in range(8):
        world.step()
        absorber = records_of(world, 1)[0]
        stocks.append(absorber["energy"][0])
        momenta.append(absorber["momentum"][0])
    # The first pull costs 2, the second is clipped to the last quantum and its
    # remainder of -1 continues; with nothing left to pay the rays pass untouched.
    assert stocks == [3, 3, 3, 1, 0, 0, 0, 0]
    assert momenta == [0, 0, 0, -2, -3, -3, -3, -3]
    assert world.spatial_values((CENTER + 4, CENTER, CENTER))["energy"]["value"] == (-2,)
    source = records_of(world, 0)[0]
    # The emitter is credited with every signed quantum and recoils along the heading.
    assert source["energy"] == (616,) and source["momentum"] == (16, 0, 0)
    report = world.conservation_report()
    assert report["status"] == "passed"
    assert world.totals()["energy"][0] + report["escaped"]["energy"] == 603


def test_a_ray_field_is_absorbed_or_exchanged_but_not_both():
    raw = absorbing_document(
        headings=[[1, 0, 0]], rays_per_tick=1, absorber_position=[2, 0, 0], signed=True
    )
    raw["spatial_couplings"].append(
        {
            "name": "also_exchange",
            "type": "absorber",
            "field": "energy",
            "mode": "exchange",
            "amount": 1,
            "denominator": 1,
        }
    )
    with pytest.raises(ValueError, match="both absorbed and exchanged"):
        parse_initial_state(raw)
