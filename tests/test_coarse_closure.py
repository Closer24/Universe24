"""Real-engine flux comparisons and independent restricted closure expectations."""

import importlib
from copy import deepcopy
from dataclasses import FrozenInstanceError, fields

import pytest

from event_universe import Simulation
from event_universe.core.integer import MAX_WORK_INT
from event_universe.initialization import parse_initial_state

closure = importlib.import_module("examples.coarse-graining.closure")
Wave = closure.Wave


@pytest.mark.parametrize("side", [2, 4, 8])
@pytest.mark.parametrize("link_ticks", [1, 2])
def test_parallel_blocks_preserve_additive_inventory_and_completed_boundary_flux(side, link_ticks):
    waves = tuple(Wave((x, y, 0), 2, (2, 0, 0)) for x in range(side) for y in range(side))
    result = closure.compare_free(side, waves, link_ticks=link_ticks)
    assert result["nodes"] == side * side
    assert result["initial_bins"] == side
    for row in result["rows"]:
        completed_columns = row["tick"] // link_ticks
        energy = 2 * side * (side - completed_columns)
        assert row["inventory"] == (energy, (energy, 0, 0))
        assert row["flux"] == (
            ((0, 0, 2 * side, (2 * side, 0, 0)),) if row["tick"] % link_ticks == 0 else ()
        )


@pytest.mark.parametrize("port,momentum", list(enumerate(closure.DIRECTIONS)))
def test_each_of_six_boundary_directions_has_independent_expected_arrival(port, momentum):
    result = closure.compare_free(4, (Wave((1, 2, 0), 1, momentum),), link_ticks=2)
    expected_arrival = (6, 4, 4, 6, 2, 2)[port]
    assert [(row["tick"], row["flux"]) for row in result["rows"] if row["flux"]] == [
        (expected_arrival, ((port, 0, 1, momentum),))
    ]


def test_different_phases_remain_distinguishable_and_never_release_early():
    early = closure.compress_free(closure.stream_configuration(4, (Wave((3, 0, 0), 2, (2, 0, 0)),)))
    late = closure.compress_free(closure.stream_configuration(4, (Wave((1, 0, 0), 2, (2, 0, 0)),)))
    assert early.inventory() == late.inventory() == (2, (2, 0, 0))
    assert early != late
    _, early_flux = early.advance()
    assert closure.flux_signature(early_flux) == ((0, 0, 2, (2, 0, 0)),)
    for _ in range(2):
        late, outgoing = late.advance()
        assert outgoing == ()
        assert late.inventory() == (2, (2, 0, 0))
    late, outgoing = late.advance()
    assert closure.flux_signature(outgoing) == ((0, 0, 2, (2, 0, 0)),)
    assert late.inventory() == (0, (0, 0, 0))


def test_independent_macro_never_reopens_micro_and_discards_only_free_irrelevant_members(monkeypatch):
    raw = closure.stream_configuration(4, tuple(Wave((3, y, 0), 1, (1, 0, 0)) for y in range(4)))
    macro = closure.compress_free(raw)
    assert len(macro.bins) == 1
    assert {item.name for item in fields(macro)} == {"bins"}
    assert {item.name for item in fields(macro.bins[0])} == {
        "remaining_delay",
        "direction",
        "channel",
        "energy",
        "momentum",
    }
    with pytest.raises(FrozenInstanceError):
        macro.bins = ()

    def forbidden(*args, **kwargs):
        raise AssertionError("macro step attempted to reopen microscopic state")

    monkeypatch.setattr(closure, "Simulation", forbidden)
    monkeypatch.setattr(closure, "parse_initial_state", forbidden)
    monkeypatch.setattr(closure, "aggregate_properties", forbidden)
    raw.clear()
    macro, outgoing = macro.advance()
    assert closure.flux_signature(outgoing) == ((0, 0, 4, (4, 0, 0)),)
    assert macro.advance() == (macro, ())


@pytest.mark.parametrize("change", ["interaction", "update", "budget", "boundary", "rate"])
def test_free_macro_rejects_unproved_future_dependent_laws(change):
    raw = closure.stream_configuration(4, (Wave((1, 1, 0), 1, (1, 0, 0)),))
    if change == "interaction":
        raw["interactions"] = [closure.encounter_rule()]
    elif change == "update":
        raw["disturbance_types"][0]["updates"] = [{"field": "energy", "expression": {"field": "energy"}}]
    elif change == "budget":
        raw["normal_budget"] = 1
    elif change == "boundary":
        raw["boundary"] = "periodic"
    else:
        raw["disturbance_types"][0]["transport"]["rate"] = 0
    with pytest.raises(ValueError):
        closure.compress_free(raw)


def test_equal_totals_and_initial_phase_flux_hide_a_real_collision_vs_parallel_pass():
    result = closure.interaction_counterexample()
    assert result["initial_summary"].inventory() == (2, (0, 0, 0))
    assert [(row["tick"], row["flux"]) for row in result["collision"] if row["flux"]] == [
        (3, ((3, 0, 1, (0, -1, 0)),)),
        (4, ((2, 0, 1, (0, 1, 0)),)),
    ]
    assert [(row["tick"], row["flux"]) for row in result["parallel"] if row["flux"]] == [
        (3, ((1, 0, 1, (-1, 0, 0)),)),
        (4, ((0, 0, 1, (1, 0, 0)),)),
    ]


def test_exhaustive_finite_closure_search_finds_minimum_only_in_its_declared_family():
    result = closure.closure_search()
    assert result["domain_configurations"] == 325  # 1 empty + 24 single + 24*25/2 pairs.
    assert result["transitions"] == 650
    assert result["candidates"] == ("totals", "direction", "direction_phase")
    assert result["conflicts"]["totals"] > 0
    assert result["conflicts"]["direction"] > 0
    assert result["conflicts"]["direction_phase"] == 0
    assert set(result["witnesses"]) == {"totals", "direction"}
    assert result["smallest_in_declared_family"] == "direction_phase"
    assert "no interacting closure" in result["scope"]


def test_invariant_mass_is_read_only_system_result_not_a_carried_mass():
    waves = (Wave((0, 0, 0), 3, (3, 0, 0)), Wave((2, 0, 0), 3, (-3, 0, 0)))
    raw = closure.stream_configuration(4, waves)
    before = deepcopy(raw)
    assert all(closure.invariant_mass_squared(wave.energy, wave.momentum) == 0 for wave in waves)
    macro = closure.compress_free(raw)
    assert macro.inventory() == (6, (0, 0, 0))
    assert closure.invariant_mass_squared(*macro.inventory()) == 36
    assert raw == before
    assert {item["name"] for item in raw["fields"]} == {"energy", "momentum"}
    # A spacelike candidate is reported honestly, without a square root or clamp.
    assert closure.invariant_mass_squared(1, (2, 0, 0)) == -3


@pytest.mark.parametrize(
    "energy,momentum,error",
    [
        (True, (0, 0, 0), TypeError),
        (1, (False, 0, 0), TypeError),
        (MAX_WORK_INT, (MAX_WORK_INT, 0, 0), OverflowError),
        (1, (MAX_WORK_INT, 0, 0), OverflowError),
        (-1, (0, 0, 0), ValueError),
    ],
)
def test_mass_readout_bounds_every_product_before_any_cancellation(energy, momentum, error):
    with pytest.raises(error):
        closure.invariant_mass_squared(energy, momentum)


@pytest.mark.parametrize("momentum", [(0, 0, 0), (1, 1, 0)])
def test_free_closure_rejects_unproved_rest_or_oblique_admission(momentum):
    with pytest.raises(ValueError, match="nonzero cardinal"):
        Wave((0, 0, 0), 1, momentum)


def test_fixed_block_and_slot_capacity_fail_without_discarding_owners():
    with pytest.raises(ValueError, match="4, 16 or 64"):
        closure.stream_configuration(3, ())
    with pytest.raises(ValueError, match="Node capacity"):
        closure.stream_configuration(2, (Wave((0, 0, 0), 1, (1, 0, 0)),) * 3)
    with pytest.raises(ValueError, match="block capacity"):
        closure.FreeMacro((closure.ExitBin(1, 0, 0, 1, (1, 0, 0)),) * 129)


def test_geometry_cannot_be_discarded_when_three_free_arrivals_exceed_capacity():
    raw = closure.stream_configuration(
        4,
        (
            Wave((0, 1, 0), 1, (1, 0, 0)),
            Wave((2, 1, 0), 1, (-1, 0, 0)),
            Wave((1, 0, 0), 1, (0, 1, 0)),
        ),
    )
    with pytest.raises(ValueError, match="receiving-capacity proof"):
        closure.compress_free(raw)
    world = Simulation(parse_initial_state(raw))
    with pytest.raises(ValueError, match="receiving capacity exhausted"):
        world.step()
    assert world.totals() == {"energy": (3,), "momentum": (0, 1, 0)}
