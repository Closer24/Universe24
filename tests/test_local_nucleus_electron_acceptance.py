"""Independent synthetic evidence tests; these do not execute another simulator."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "nucleus_acceptance", ROOT / "examples/local-nucleus-electron/acceptance.py"
)
ACCEPTANCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ACCEPTANCE)


def record(kind, *, momentum=(0, 0, 0), remainder=(0, 0, 0)):
    return {
        "type": kind,
        "values": {"momentum": list(momentum), "motion_remainder": list(remainder)},
    }


def square_trace(*, clockwise=False, center=(20, 20, 20)):
    # A prescribed diagnostic square has exactly 64 one-cell edges and period 200.
    # It tests the scorer, not whether an engine can produce this path.
    ring = [
        *[(8, y) for y in range(8)],
        *[(x, 8) for x in range(8, -8, -1)],
        *[(-8, y) for y in range(8, -8, -1)],
        *[(x, -8) for x in range(-8, 8)],
        *[(8, y) for y in range(-8, 0)],
    ]
    assert len(ring) == 64
    states = []
    for tick in range(833):
        phase = max(0, tick - 64) * 64 // 200
        x, y = ring[(-phase if clockwise else phase) % 64]
        states.append(
            {
                "tick": tick,
                "nodes": [
                    {"position": list(center), "disturbances": [record("proton"), record("neutron")]},
                    {
                        "position": [center[0] + x, center[1] + y, center[2]],
                        "disturbances": [record("electron", momentum=(0, 2048, 0))],
                    },
                ],
                "transfers": [],
            }
        )
    return states


def test_launch_reference_gives_three_intervals_without_requiring_four_returns():
    states = square_trace()
    before = copy.deepcopy(states)
    scored = ACCEPTANCE.circulation(states)
    assert scored["status"] == "pass"
    assert scored["world_tick_periods"] == [200, 200, 200]
    assert scored["completed_positive_windings"] == 3
    assert scored["min_radius_squared"] == 64
    assert scored["max_radius_squared"] == 128
    assert scored["quantum_phase_frequency"].startswith("unavailable")
    assert states == before


def test_moving_display_coordinates_do_not_supply_or_remove_physical_circulation():
    shifted = square_trace(center=(30, 30, 30))
    for state in shifted:
        state["glyph_offsets"] = [[10000, 10000, 10000]]
    assert ACCEPTANCE.circulation(shifted)["world_tick_periods"] == [200, 200, 200]


@pytest.mark.parametrize("defect", ["missing_tick", "missing_owner", "duplicate_owner", "clockwise"])
def test_incomplete_or_wrongly_owned_or_reversed_traces_cannot_pass(defect):
    states = square_trace(clockwise=defect == "clockwise")
    if defect == "missing_tick":
        del states[99]
    elif defect == "missing_owner":
        states[99]["nodes"][1]["disturbances"] = []
    elif defect == "duplicate_owner":
        states[99]["nodes"][1]["disturbances"].append(record("electron"))
    assert ACCEPTANCE.circulation(states)["status"] != "pass"


def test_axis_jitter_is_not_a_completed_winding_and_frequency_is_unavailable():
    states = square_trace()
    for state in states:
        state["nodes"][1]["position"] = [28, 20 + (state["tick"] % 3) - 1, 20]
    states[64]["nodes"][1]["position"] = [28, 20, 20]
    scored = ACCEPTANCE.circulation(states)
    assert scored["status"] == "fail"
    assert scored["completed_positive_windings"] == 0
    assert scored["measured_recurrence_per_world_tick"] is None


def test_localization_and_full_state_return_are_separate_checks():
    states = square_trace()
    states[264]["nodes"][1]["disturbances"][0]["values"]["motion_remainder"] = [1, 0, 0]
    scored = ACCEPTANCE.circulation(states)
    assert scored["status"] == "pass"
    assert not scored["crossing_states"][0]["matches_launch_momentum_and_remainder"]
    states[100]["nodes"][1]["position"] = [33, 20, 20]
    assert ACCEPTANCE.circulation(states)["status"] == "fail"


def test_signed_displacement_identity_retains_changed_direction_and_catches_reset():
    rows = [
        {"tick": 0, "momentum": [6, 0, 0], "remainder": [6, 0, 0], "dispatched_hop": [0, 0, 0]},
        {"tick": 1, "momentum": [0, 6, 0], "remainder": [6, 6, 0], "dispatched_hop": [0, 0, 0]},
        {"tick": 2, "momentum": [4, 0, 0], "remainder": [0, 6, 0], "dispatched_hop": [1, 0, 0]},
    ]
    assert ACCEPTANCE.displacement(rows, denominator=10)["status"] == "pass"
    rows[1]["remainder"] = [0, 6, 0]
    assert ACCEPTANCE.displacement(rows, denominator=10)["failed_ticks"] == [1]


def test_deferred_zero_momentum_hop_is_old_owned_displacement_not_new_momentum():
    rows = [
        {"tick": 0, "momentum": [4, 4, 0], "remainder": [0, 10, 0], "dispatched_hop": [1, 0, 0]},
        {"tick": 1, "momentum": [0, 0, 0], "remainder": [0, 0, 0], "dispatched_hop": [0, 1, 0]},
    ]
    assert ACCEPTANCE.displacement(rows, denominator=10, initial_remainder=(6, 6, 0))["status"] == "pass"
    rows[1]["dispatched_hop"] = [1, 1, 0]
    assert ACCEPTANCE.displacement(rows, denominator=10, initial_remainder=(6, 6, 0))["status"] == "fail"


def ideal_field_probes():
    means = {tuple(8 * v for v in port): tuple(8 * v for v in port) for port in ACCEPTANCE.PORTS}
    means.update(
        {(6, 6, 0): (4, 4, 0), (4, 4, 4): (6, 6, 6), (4, 0, 0): (32, 0, 0), (16, 0, 0): (2, 0, 0)}
    )
    return means


def test_source_acceptance_does_not_refit_anisotropy_or_tangential_flux():
    means = ideal_field_probes()
    assert ACCEPTANCE.field_cycle(means)["status"] == "pass"
    means[(0, 8, 0)] = (0, 4.8, 0)
    means[(0, 0, 8)] = (0, 0, 1.6)
    scored = ACCEPTANCE.field_cycle(means)
    assert scored["status"] == "fail"
    assert scored["coefficient"] == 8
    assert scored["probes"][2]["relative_radial_error"] == pytest.approx(0.4)
    means = ideal_field_probes()
    means[(6, 6, 0)] = (0, 8, 0)
    assert ACCEPTANCE.field_cycle(means)["status"] == "fail"
    del means[(16, 0, 0)]
    assert ACCEPTANCE.field_cycle(means)["status"] == "incomplete"


def test_source_cycle_requires_all_phases_and_retains_exact_calibration():
    samples = {
        point: [{"tick": t, "flux": vector} for t in range(20, 30)]
        for point, vector in ideal_field_probes().items()
    }
    scored = ACCEPTANCE.field_cycle_samples(samples)
    assert scored["status"] == "pass"
    assert scored["f8_exact"] == [8, 1]
    assert scored["coefficient_exact"] == [8, 1]
    samples[(8, 0, 0)].pop()
    assert ACCEPTANCE.field_cycle_samples(samples)["status"] == "incomplete"


def nuclear_state(tick, *, captured=False, emitted=False, stock_error=0):
    mass = 940032
    records = []
    for kind, charge, sign in (("proton", 1, 1), ("neutron", 0, -1)):
        records.append(
            {
                "type": kind,
                "values": {
                    "mass": [mass],
                    "charge": [charge],
                    "baryon": [1],
                    "gap": [334944582],
                    "momentum": [0 if captured else sign * mass, 0, 0],
                    "radiation": [335414598 if captured and not emitted else 0],
                    "excitation": [0],
                    "bound": [int(captured)],
                    "sector": [int(captured)],
                },
            }
        )
    return {
        "tick": tick,
        "nodes": [{"position": [4, 4, 4], "disturbances": records}],
        "transfers": [],
        "accounting": {
            "totals": {"momentum": [0, 0, 0]},
            "escaped_totals": {"momentum": [0, 0, 0]},
            "dissipation_totals": {"momentum": [0, 0, 0]},
            "spatial_accounting": {
                "radiation": {
                    "current": [670829196 * int(emitted) + stock_error],
                    "escaped": [0],
                    "dissipated": [0],
                }
            },
        },
    }


def test_capture_invariant_counts_funded_radiation_after_it_leaves_material_owner():
    states = [
        nuclear_state(0),
        nuclear_state(1, captured=True),
        nuclear_state(2, captured=True, emitted=True),
    ]
    scored = ACCEPTANCE.nuclear_control(states, "nuclear_capture")
    assert scored["status"] == "pass"
    assert scored["initial_energy"] == scored["final_energy"] == 940032
    states[2]["accounting"]["spatial_accounting"]["radiation"]["current"][0] += 1
    assert ACCEPTANCE.nuclear_control(states, "nuclear_capture")["status"] == "fail"


def test_pinning_is_not_a_disabled_binding_control_and_missing_inventory_is_not_zero():
    states = [nuclear_state(0), nuclear_state(32)]
    scored = ACCEPTANCE.nuclear_control(states, "nuclear_disabled")
    assert scored["status"] == "fail"
    assert not scored["checks"]["separated"]
    del states[1]["accounting"]
    assert ACCEPTANCE.nuclear_control(states, "nuclear_disabled")["status"] == "incomplete"


def test_outgoing_sector_cannot_silently_recapture():
    states = [
        nuclear_state(0, captured=True),
        nuclear_state(1, captured=True),
        nuclear_state(2, captured=True),
    ]
    for record_ in states[1]["nodes"][0]["disturbances"]:
        record_["values"]["sector"] = [2]
    scored = ACCEPTANCE.nuclear_control(states, "nuclear_threshold_zero_kick")
    assert not scored["no_recapture_after_outgoing"]
    assert scored["status"] == "fail"


def test_absent_radiation_is_zero_only_when_initialization_has_no_spatial_owner():
    states = [nuclear_state(0), nuclear_state(32)]
    for state in states:
        state["accounting"]["spatial_accounting"] = {}
    pair = states[1]["nodes"][0]["disturbances"]
    states[1]["nodes"] = [
        {"position": [5, 4, 4], "disturbances": [pair[0]]},
        {"position": [3, 4, 4], "disturbances": [pair[1]]},
    ]
    assert ACCEPTANCE.nuclear_control(states, "nuclear_disabled")["status"] == "incomplete"
    scored = ACCEPTANCE.nuclear_control(states, "nuclear_disabled", initialization={})
    assert scored["status"] == "pass"
    assert "comparison only" in scored["scope"]
    assert (
        ACCEPTANCE.nuclear_control(
            states, "nuclear_disabled", initialization={"spatial_fields": [{"field": "radiation"}]}
        )["status"]
        == "incomplete"
    )


def test_transit_audit_rejects_same_tick_cascade_and_sampler_admission():
    assert ACCEPTANCE.event_checks([])["transit"]["status"] == "not_exercised"
    events = [{"event": "spatial_sent", "tick": 1, "arrival_tick": 1, "port": 2}]
    assert ACCEPTANCE.event_checks(events)["transit"]["status"] == "fail"
    assert ACCEPTANCE.no_sampling({"spatial_fields": [{"bond": {"seed": 1}}]}, 0)["status"] == "fail"
    assert ACCEPTANCE.no_sampling({}, 1)["status"] == "fail"
    assert ACCEPTANCE.no_sampling({}, 0)["status"] == "pass"


def test_kinematic_square_alone_never_closes_field_or_nuclear_physics(tmp_path):
    source = json.dumps({"model_id": ACCEPTANCE.MODEL}).encode()
    run = {
        "model": ACCEPTANCE.MODEL,
        "status": "completed",
        "completed_ticks": 832,
        "requested_ticks": 832,
        "source_sha256": "a" * 64,
        "initialization_sha256": hashlib.sha256(source).hexdigest(),
        "link_ticks": 1,
    }
    run["state_trace"] = {
        "path": "states.jsonl",
        "content": "carriers",
        "stride": 1,
        "rows": 833,
        **{
            key: run[key]
            for key in ("source_sha256", "initialization_sha256", "requested_ticks", "completed_ticks")
        },
    }
    (tmp_path / "initialization.json").write_bytes(source)
    (tmp_path / "run.json").write_text(json.dumps(run))
    (tmp_path / "events.jsonl").write_text("")
    (tmp_path / "state.json").write_text(json.dumps(square_trace()[-1]))
    with pytest.raises(ACCEPTANCE.EvidenceError, match="states.jsonl"):
        ACCEPTANCE.score_run(tmp_path)
    (tmp_path / "states.jsonl").write_text("\n".join(json.dumps(s) for s in square_trace()))
    scored = ACCEPTANCE.score_run(tmp_path)
    assert scored["circulation"]["status"] == "pass"
    assert scored["field_acceptance"]["status"] == "incomplete"
    assert scored["nuclear_acceptance"]["status"] == "incomplete"
    run["initialization_sha256"] = "b" * 64
    assert ACCEPTANCE.trace_checks(square_trace(), run, source)["status"] == "fail"
