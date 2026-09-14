"""Run and audit the explicitly configured local moment-exchange candidate."""

import argparse
import json
import time
from pathlib import Path

from local_moment_exchange import configuration
from momentum_state_exchange import run_quantum_exchange_controls

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint


def _second_moment(values):
    mean = values["coarse_momentum"]
    second = sum(value * value for value in mean) + values["momentum_spread"][0]
    mass = values["mass"][0]
    assert mass == 1 or (mass == 0 and second == 0)
    return second


def audit_case(raw):
    """Observe world state without feeding any diagnostic back to its laws."""
    prepared = prepare_initialization(raw)
    events = []
    escaped_energy = 0

    def record(event):
        nonlocal escaped_energy
        events.append(event)
        if event["event"] == "escaped":
            escaped_energy += _second_moment(event["values"])

    has_reservoir = any(seed["type"] == "arriving_reservoir" for seed in raw["seeds"])
    expected_energy = 10 if has_reservoir else 1
    first_capture = None
    first_exchange = None
    path = []
    delayed_owned_samples = 0
    with Simulation(prepared.initial, observer=record) as world:
        original = world.totals()
        for _ in range(raw["ticks"]):
            world.step()
            resident = [
                (position, record)
                for position, node in world.nodes.items()
                for record in node.records
                if record is not None
            ]
            linked = [
                packet.record
                for packets in world.links.values()
                for packet in packets
                if packet is not None
            ]
            ordinary = [world.record_values(record) for _, record in resident]
            ordinary.extend(world.record_values(record) for record in linked)
            totals = world.totals()
            escaped = world.escaped_totals()
            assert all(
                tuple(value + out for value, out in zip(totals[name], escaped[name], strict=True))
                == original[name]
                for name in original
            )
            # One configured quantum carrier has zero mean and unit variance.
            # Its conserved variance inventory is not a second ordinary owner.
            quantum_spread = totals["momentum_spread"][0] - sum(
                item["momentum_spread"][0] for item in ordinary
            )
            quantum_mean = tuple(
                totals["coarse_momentum"][axis] - sum(item["coarse_momentum"][axis] for item in ordinary)
                for axis in range(3)
            )
            assert quantum_mean == (0, 0, 0) and quantum_spread in (0, 1)
            assert (
                sum(map(_second_moment, ordinary)) + quantum_spread + escaped_energy == expected_energy
            )
            for position, record in resident:
                kind = prepared.initial.disturbances[record.type_index].name
                values = world.record_values(record)
                if kind == "localized_charge":
                    assert values["coarse_momentum"] == (0, 0, 0)
                    assert values["momentum_spread"] == (1,) and values["momentum_known"] == (0,)
                    first_capture = first_capture or {"audit_tick": world.tick, "position": position}
                    node = world.nodes[position]
                    if node.pending and any(
                        other is not None
                        and prepared.initial.disturbances[other.type_index].name == "arriving_reservoir"
                        for other in node.records
                    ):
                        delayed_owned_samples += 1
                elif kind == "moving_output":
                    assert values["momentum_spread"] == (0,) and values["momentum_known"] == (1,)
                    first_exchange = first_exchange or {"audit_tick": world.tick, "position": position}
                    if not path or path[-1]["position"] != position:
                        path.append({"audit_tick": world.tick, "position": position})
                elif kind in ("spent_reservoir", "stored_recoil"):
                    assert values["coarse_momentum"] == (0, 0, 0)
                    assert values["momentum_spread"] == (1,) and values["momentum_known"] == (0,)
            if escaped["charge"] == (-1,):
                break
        report = world.computation_report()
        sends = [event for event in events if event["event"] == "sent"]
        output_sends = [event for event in sends if event["disturbance"] == "moving_output"]
        assert all(event["arrival_tick"] == event["tick"] + raw["link_ticks"] for event in sends)
        assert first_capture is not None
        if has_reservoir:
            assert first_exchange is not None and output_sends
            assert world.escaped_totals()["charge"] == (-1,)
            assert len({event["port"] for event in output_sends}) == 1
            assert all(
                b["tick"] - a["tick"] >= 100 * raw["link_ticks"]
                for a, b in zip(output_sends, output_sends[1:], strict=False)
            )
        else:
            assert first_exchange is None and not output_sends
        assert report["model_operations_cost"] == report["event_ledger_cost"]
        return {
            "completed_ticks": world.tick,
            "first_capture": first_capture,
            "first_exchange": first_exchange,
            "path": path,
            "output_sends": output_sends,
            "delayed_owned_samples": delayed_owned_samples,
            "initial_totals": original,
            "final_totals": world.totals(),
            "escaped_totals": world.escaped_totals(),
            "expected_doubled_kinetic_energy_including_escape": expected_energy,
            "mean_momentum_and_second_moment_balanced_every_tick": True,
            "contact_transfers": report["resolver"]["contact_transfers"],
            "cost": report["model_operations_cost"],
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
    before = source_fingerprint()
    started = time.perf_counter()
    with ArtifactLease(output, paths):
        raw = configuration()
        paths[0].write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
        run_initialization(paths[0], output / "native")
        cases = []
        for axis in range(3):
            for sign in (-1, 1):
                cases.append({"axis": axis, "sign": sign, **audit_case(configuration(axis, sign))})
        absent = configuration(reservoir=False)
        absent["ticks"] = 64
        delayed = configuration(normal_budget=20)
        delayed["ticks"] = 1000
        result = {
            "numerical_checks": "pass",
            "model": raw["model_id"],
            "source_sha256": before,
            "six_axis_controls": cases,
            "no_reservoir": audit_case(absent),
            "long_links": audit_case(configuration(link_ticks=3)),
            "computation_delay": audit_case(delayed),
            "quantum_state_exchange": run_quantum_exchange_controls(),
            "scope": "Local moment closure with a separate exact quantum-owner control.",
            "classical_limit": "not_derived",
            "limits": [
                "Captured momentum moments are supplied, not derived from spatial amplitudes.",
                "Ordinary response preserves means and second moments, not full quantum correlations.",
                "The uncertain outgoing reservoir has zero mean and is held; spreading is not modeled.",
                "Schema 1 conversion does not support emitter or spatial-field coupling composition.",
                "The quadratic kinetic-energy candidate assumes equal unit masses and slow transport.",
            ],
        }
        assert source_fingerprint() == before
        result["elapsed_seconds"] = time.perf_counter() - started
        paths[1].write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    result = run_experiment(arguments.output)
    print(
        json.dumps(
            {key: result[key] for key in ("numerical_checks", "classical_limit", "elapsed_seconds")}
        )
    )
