"""Compare spatial-wave moments with local capture re-encoding and response.

Every density query and inventory sum is an external audit. Only the self-contained
initialization, local outcomes and generic pair laws control the native world.
"""

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.integration.contact_runtime import ContactEventResolver
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint
from examples.quantum.position_moment_response import configuration
from examples.quantum.spatial_measurement_controls import measurement_controls
from examples.quantum.spatial_momentum import spatial_moments


def _json(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: _json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(item) for item in value]
    return value


def _ordinary_moments(values):
    """Require actual payloads; absent values are not definite zero momentum."""
    mean = values["coarse_momentum"]
    variance = values["momentum_spread"][0]
    second = sum(component * component for component in mean) + variance
    assert values["mass"][0] == 1 or (values["mass"][0] == 0 and second == 0)
    return mean, second


def audit_case(raw, *, inspect_wave=True):
    prepared = prepare_initialization(raw)
    events = []
    domain = raw["event_program"]["domains"][0]
    modes = tuple(domain["register_indices"])
    edges = tuple(zip(modes, modes[1:], strict=False))
    positions = raw["event_program"]["addresses"]
    axis = next(axis for axis in range(3) if positions[0][axis] != positions[1][axis])
    capture_register = domain["capture"]["register_indices"][0]
    capture_position = tuple(positions[capture_register])
    capture_type = domain["capture"]["output"]["type"]
    target = next(kind for kind in raw["disturbance_types"] if kind["name"] == capture_type)
    expected_spread = target["defaults"]["momentum_spread"]
    escaped_mean = [0, 0, 0]
    escaped_second = 0

    def record(event):
        nonlocal escaped_second
        events.append(event)
        if event["event"] == "escaped":
            mean, second = _ordinary_moments(event["values"])
            escaped_second += second
            for component in range(3):
                escaped_mean[component] += mean[component]

    captures = []
    response = None
    path = []
    wave_samples = []
    total_samples = []
    pending_samples = 0
    with Simulation(prepared.initial, observer=record) as world:
        resolver = world._resolver
        assert isinstance(resolver, ContactEventResolver)
        original = world.totals()
        has_reservoir = any(seed["type"] == "arriving_reservoir" for seed in raw["seeds"])
        wave = None
        if inspect_wave:
            initial_ordinary = [
                _ordinary_moments(world.record_values(record))
                for node in world.nodes.values()
                for record in node.records
                if record is not None
            ]
            total_samples.append(
                {
                    "audit_tick": 0,
                    "mean": [sum(mean[c] for mean, _ in initial_ordinary) for c in range(3)],
                    "second_moment": sum(second for _, second in initial_ordinary),
                }
            )
        for _ in range(raw["ticks"]):
            world.step()
            residents = [
                (address, record)
                for address, node in world.nodes.items()
                for record in node.records
                if record is not None
            ]
            records = [record for _, record in residents]
            records.extend(
                packet.record
                for packets in world.links.values()
                for packet in packets
                if packet is not None
            )
            values = [world.record_values(record) for record in records]
            for field in ("mass", "charge"):
                assert (
                    tuple(
                        a + b
                        for a, b in zip(
                            world.totals()[field], world.escaped_totals()[field], strict=True
                        )
                    )
                    == original[field]
                )
            # Query the actual evolved wave while it can exist, and once after
            # capture to confirm vacuum. Never query or copy a template inventory.
            if inspect_wave and (not captures or wave is None or wave["status"] != "vacuum"):
                before = (resolver.space.tick, resolver.space.events, resolver.space.records)
                wave = spatial_moments(resolver.space, modes, edges)
                assert before == (resolver.space.tick, resolver.space.events, resolver.space.records)
                wave_samples.append({"audit_tick": world.tick, **wave})
            for address, record in residents:
                kind = prepared.initial.disturbances[record.type_index].name
                payload = world.record_values(record)
                if kind == capture_type:
                    assert address == capture_position
                    assert payload["coarse_momentum"] == (0, 0, 0)
                    assert payload["momentum_spread"] == (expected_spread,)
                    assert payload["momentum_known"] == (0,)
                    if not captures:
                        captures.append(
                            {
                                "audit_tick": world.tick,
                                "position": address,
                                "mean": (0, 0, 0),
                                "variance": expected_spread,
                            }
                        )
                    node = world.nodes[address]
                    if node.pending is not None and any(
                        other is not None
                        and prepared.initial.disturbances[other.type_index].name == "arriving_reservoir"
                        for other in node.records
                    ):
                        pending_samples += 1
                elif kind == "moving_output":
                    assert payload["momentum_spread"] == (0,)
                    response = response or {"audit_tick": world.tick, "values": payload}
                    if not path or path[-1]["position"] != address:
                        path.append({"audit_tick": world.tick, "position": address})
                elif kind in ("spent_reservoir", "stored_recoil"):
                    assert payload["momentum_spread"] == (expected_spread,)
                    assert payload["coarse_momentum"] == (0, 0, 0)
            ordinary = [_ordinary_moments(payload) for payload in values]
            total_mean = [sum(mean[c] for mean, _ in ordinary) + escaped_mean[c] for c in range(3)]
            total_second = sum(second for _, second in ordinary) + escaped_second
            if inspect_wave and wave["status"] != "vacuum":
                weight = wave["occupation_probability"]
                total_mean[axis] += weight * wave["mean_momentum"]
                total_second += weight * wave["second_moment"]
            if inspect_wave and (
                not total_samples
                or total_samples[-1]["mean"] != total_mean
                or total_samples[-1]["second_moment"] != total_second
            ):
                total_samples.append(
                    {"audit_tick": world.tick, "mean": total_mean, "second_moment": total_second}
                )
            if captures:
                # Only the post-capture ordinary sector claims closure here.
                assert total_second == (9 if has_reservoir else 0) + expected_spread
                expected_mean = [0, 0, 0]
                if has_reservoir:
                    seed = next(
                        kind for kind in raw["disturbance_types"] if kind["name"] == "arriving_reservoir"
                    )
                    expected_mean = seed["defaults"]["coarse_momentum"]
                assert total_mean == expected_mean
            if world.escaped_totals()["charge"] == (-1,):
                break
        assert captures
        assert (response is not None) == has_reservoir
        sends = [event for event in events if event["event"] == "sent"]
        assert all(event["arrival_tick"] == event["tick"] + raw["link_ticks"] for event in sends)
        output_sends = [event for event in sends if event["disturbance"] == "moving_output"]
        if has_reservoir:
            assert world.escaped_totals()["charge"] == (-1,)
            assert len({event["port"] for event in output_sends}) == 1
        else:
            assert not output_sends
        report = world.computation_report()
        assert report["model_operations_cost"] == report["event_ledger_cost"]
        return {
            "completed_ticks": world.tick,
            "capture": captures[0],
            "response": response,
            "path": path,
            "wave_samples": wave_samples,
            "observed_combined_moment_changes": total_samples,
            "pending_owned_samples": pending_samples,
            "post_capture_ordinary_moments_balanced": True,
            "quantum_and_apparatus_closure": "not_established",
            "contact_transfers": report["resolver"]["contact_transfers"],
            "output_sends": output_sends,
            "events": events,
            "cost": report["model_operations_cost"],
            "final_totals": world.totals(),
            "escaped_totals": world.escaped_totals(),
        }


def run_experiment(output):
    output = Path(output).resolve()
    validate_output_path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use a fresh output directory")
    output.mkdir(parents=True, exist_ok=True)
    paths = [output / "input.json", output / "summary.json"]
    for path in paths:
        path.touch()
    started = time.perf_counter()
    fingerprint = source_fingerprint()
    with ArtifactLease(output, paths):
        raw = configuration(capture="middle")
        paths[0].write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
        run_initialization(paths[0], output / "native")
        middle = audit_case(raw)
        unobserved = audit_case(raw, inspect_wave=False)
        assert middle["events"] == unobserved["events"]
        assert middle["cost"] == unobserved["cost"]
        assert middle["final_totals"] == unobserved["final_totals"]
        cases = []
        for axis in range(3):
            for sign in (-1, 1):
                case = audit_case(configuration(axis=axis, sign=sign))
                case.pop("events")
                cases.append({"axis": axis, "sign": sign, **case})
        absent = configuration(capture="middle", reservoir=False)
        absent["ticks"] = 12
        delayed = configuration(capture="middle", normal_budget=20)
        delayed["ticks"] = 1000
        controls = {
            "no_reservoir": audit_case(absent),
            "computation_delay": audit_case(delayed),
            "long_links": audit_case(configuration(capture="middle", link_ticks=3)),
        }
        for case in (middle, *controls.values()):
            case.pop("events")
        result = {
            "numerical_checks": "pass",
            "model": raw["model_id"],
            "source_sha256": fingerprint,
            "middle_capture": middle,
            "six_axis_endpoint_controls": cases,
            **controls,
            "measurement_controls": measurement_controls(),
            "diagnostics_leave_native_trace_and_cost_unchanged": True,
            "classical_limit": "not_derived",
            "closed_quantum_apparatus_energy_momentum": False,
        }
        assert source_fingerprint() == fingerprint
        result["elapsed_seconds"] = time.perf_counter() - started
        paths[1].write_text(json.dumps(_json(result), indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    result = run_experiment(parser.parse_args().output)
    print(
        json.dumps(
            {key: result[key] for key in ("numerical_checks", "classical_limit", "elapsed_seconds")}
        )
    )
