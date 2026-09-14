"""Opt-in funded envelope emission: the wave's own stock pays for its classical field."""

import json
from copy import deepcopy

import pytest

from event_universe.core.disturbance_state import unpack
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_causal_contact_fields import DETECTOR, MIDDLE, SOURCE, causal_configuration
from .test_localized_quantum_contact import localized, step, world_for

INVERSE = [[5, 0, 0, 0], [0, 3, 4, 0], [0, -4, 3, 0], [0, 0, 0, 5]]
SWAP = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
STOCK = 3000
BUDGET = 1000
FIELD = "electric_signal"


def funded_configuration(*, tickets=(0,), stock=STOCK, budget=BUDGET, ticks=14):
    raw = causal_configuration()
    raw["ticks"] = ticks
    raw["event_program"]["tickets"] = list(tickets)
    for kind in raw["disturbance_types"]:
        if kind["name"] in ("incoming_charge", "localized_charge"):
            kind["fields"].append(FIELD)
            kind["defaults"][FIELD] = stock
    for emission in raw["emissions"]:
        emission["source"] = False
        emission["budget"] = budget
        emission["amount"] = 25
    domain = raw["event_program"]["domains"][0]
    domain["phases"] = [
        [{"register_indices": [0, 1], "matrix": domain["phases"][0][0]["matrix"]}],
        [{"register_indices": [1], "matrix": [[1, 0], [0, -1]]}],
        [{"register_indices": [0, 1], "matrix": INVERSE}],
        [{"register_indices": [1, 2], "matrix": SWAP}],
        *([[]] * 12),
    ]
    return raw


def stock_of(world, address, type_index):
    node = world._nodes[address]
    field = [f.name for f in world.initial.fields].index(FIELD)
    return [
        unpack(record.values[field])[0]
        for record in node.records
        if record is not None and record.type_index == type_index
    ]


def test_funded_octant_emission_is_accepted_when_the_type_owns_the_field():
    raw = funded_configuration()
    initial = parse_initial_state(raw)
    assert all(rule.funded for rule in initial.emissions)
    bad = deepcopy(raw)
    for kind in bad["disturbance_types"]:
        if kind["name"] == "incoming_charge":
            kind["fields"].remove(FIELD)
            del kind["defaults"][FIELD]
    with pytest.raises(ValueError, match="own the emitted field"):
        parse_initial_state(bad)


def test_source_stock_must_cover_every_mode_budget():
    with pytest.raises(ValueError, match="cover every mode's budget"):
        parse_initial_state(funded_configuration(stock=2999))
    parse_initial_state(funded_configuration(stock=3000))
    raw = funded_configuration()
    raw["event_program"]["model"] = "localized-contact-quantum-v1"
    with pytest.raises(ValueError, match="funded envelope emission requires the causal"):
        parse_initial_state(raw)


def test_totals_stay_constant_without_sources_while_the_wave_pays(monkeypatch):
    world, resolver = world_for(funded_configuration())
    field = [f.name for f in world.initial.fields].index(FIELD)
    assert world.totals()[FIELD] == (STOCK,)
    for _ in range(7):
        step(world, 1)
        assert world.totals()[FIELD] == (STOCK,)
        assert world.source_totals()[FIELD] == (0,)
        assert all(value["balanced"] for value in world.spatial_accounting().values())
        paid = resolver.report()["funded_emission"]["charge_mode"]["paid"][FIELD][0]
        assert resolver.inventory()[field] == (STOCK - paid,)
    # Tick 0 emission by the ordinary record (25) counted as already paid at preparation,
    # and every envelope emission since then: 9 + 16 per tick on the arms.
    assert resolver.report()["funded_emission"]["charge_mode"]["paid"][FIELD][0] > 25 + 4 * 25


def test_localized_winner_inherits_the_unspent_stock_and_keeps_paying():
    world, resolver = world_for(funded_configuration(tickets=(600,)))
    step(world, 8)
    assert localized(world) == [(DETECTOR, 1)]
    report = resolver.report()["funded_emission"]["charge_mode"]
    paid = report["paid"][FIELD][0]
    assert stock_of(world, DETECTOR, 1) == [STOCK - paid]
    assert resolver.inventory() == tuple((0,) * f.components for f in world.initial.fields)
    step(world, 6)
    # The localized record pays its own ordinary funded emission from the same stock.
    assert stock_of(world, DETECTOR, 1) == [STOCK - paid - 6 * 25]
    residual = report["after_capture"][FIELD][0]
    assert world.source_totals()[FIELD] == (
        resolver.report()["funded_emission"]["charge_mode"]["after_capture"][FIELD][0],
    )
    assert world.totals()[FIELD] == (STOCK + world.source_totals()[FIELD][0],)
    assert residual >= 0


def test_retarded_emission_after_capture_is_an_explicit_external_residual(tmp_path):
    initial = tmp_path / "funded.json"
    initial.write_text(json.dumps(funded_configuration(tickets=(600,))), encoding="utf-8")
    run_initialization(initial, tmp_path / "run")
    report = json.loads((tmp_path / "run/run.json").read_text(encoding="utf-8"))
    funded = report["computation"]["resolver"]["funded_emission"]["charge_mode"]
    assert report["conserved_at_every_completed_tick"]
    assert report["accounting_balanced_at_every_completed_tick"]
    assert report["source_totals"][FIELD] == funded["after_capture"][FIELD]
    assert funded["after_capture"][FIELD][0] > 0
    assert report["final_totals"][FIELD][0] == STOCK + funded["after_capture"][FIELD][0]


def test_default_profile_reports_no_funded_emission():
    world, resolver = world_for(causal_configuration())
    assert resolver.report()["funded_emission"] == {}
    step(world, 2)
    assert world.source_totals()[FIELD] != (0,)
    assert MIDDLE in resolver.source_nodes() and SOURCE in resolver.source_nodes()
