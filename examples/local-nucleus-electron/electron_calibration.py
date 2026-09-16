"""Actual source-only calibration and read-only static-field acceptance.

Run before any orbital world. The saved initialization, events, metadata and
canonical HTML are the evidence; the geometric estimate is never substituted.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from electron_configuration import (
    NORMAL_BUDGET,
    SOURCE_HASH,
    definition,
    electric_emission,
    electric_field,
)

from event_universe.core.disturbance_state import OPERATIONS
from event_universe.runner import run_initialization

PROBES = (
    (8, 0, 0),
    (-8, 0, 0),
    (0, 8, 0),
    (0, -8, 0),
    (0, 0, 8),
    (0, 0, -8),
    (6, 6, 0),
    (4, 4, 4),
    (4, 0, 0),
    (16, 0, 0),
)
WINDOWS = ((64, 74), (74, 84))


def calibration_document() -> dict[str, object]:
    """Stationary external source; probes are passive reads, never physical owners."""
    return {
        "schema_version": 1,
        "model_id": "electron-source-calibration-last-port-v1",
        "shape": [41, 41, 41],
        "boundary": "open",
        "link_ticks": 1,
        "normal_budget": NORMAL_BUDGET,
        "slots_per_node": 2,
        "ticks": 84,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": [
            definition("charge", 1, "charge code", conserved=True, extensive=True),
            definition("bound", 1, "preparation flag", signed=False),
            definition("charge_field", 1, "unit ray stock", conserved=True, extensive=True),
        ],
        "disturbance_types": [
            {
                "name": "prepared_source",
                "fields": ["charge", "bound"],
                "defaults": {"charge": 1, "bound": 1},
                "transport": {"mode": "hold"},
            }
        ],
        "seeds": [{"position": [20, 20, 20], "type": "prepared_source"}],
        "spatial_fields": [electric_field()],
        "emissions": [electric_emission()],
    }


def delivered_flux(received_fields: list[dict[str, list[int]]]) -> tuple[int, int, int]:
    """Receiver faces are opposite the travel Port; return newly arrived flux."""
    return tuple(
        received_fields[2 * axis + 1].get("charge_field", [0])[0]
        - received_fields[2 * axis].get("charge_field", [0])[0]
        for axis in range(3)
    )


def analyze(run: Path) -> dict[str, object]:
    traces = {offset: [(0, 0, 0)] * 20 for offset in PROBES}
    max_cost, delayed, receipts = 0, 0, 0
    with (run / "events.jsonl").open() as stream:
        for line in stream:
            event = json.loads(line)
            if event["event"] in ("cycle_started", "spatial_cycle_started"):
                max_cost = max(max_cost, event.get("cost", 0))
                delayed += int(event.get("ready_tick", event["tick"]) != event["tick"])
            if event["event"] != "spatial_received" or not 64 <= event["tick"] < 84:
                continue
            offset = tuple(value - 20 for value in event["position"])
            if offset in traces:
                index = event["tick"] - 64
                incoming = delivered_flux(event["received_fields"])
                traces[offset][index] = tuple(
                    a + b for a, b in zip(traces[offset][index], incoming, strict=True)
                )
                receipts += 1
    repeated = all(values[:10] == values[10:] for values in traces.values())
    sums = {
        offset: tuple(sum(row[axis] for row in values[:10]) for axis in range(3))
        for offset, values in traces.items()
    }
    reference = sums[(8, 0, 0)][0]
    positive = reference > 0
    symmetry = positive and all(
        abs(sums[offset][axis] * sign - reference) * 20 <= reference
        for offset, axis, sign in (
            (PROBES[0], 0, 1),
            (PROBES[1], 0, -1),
            (PROBES[2], 1, 1),
            (PROBES[3], 1, -1),
            (PROBES[4], 2, 1),
            (PROBES[5], 2, -1),
        )
    )
    radial_controls = {}
    for offset in ((6, 6, 0), (4, 4, 4), (4, 0, 0), (16, 0, 0)):
        vector = sums[offset]
        radius_squared = sum(value * value for value in offset)
        dot = sum(a * b for a, b in zip(vector, offset, strict=True))
        radial = dot / math.sqrt(radius_squared)
        tangent_squared = max(0, sum(value * value for value in vector) - dot * dot / radius_squared)
        expected = reference * 64 / radius_squared
        radial_ok = positive and abs(radial - expected) <= expected / 4
        tangent_ok = dot > 0 and tangent_squared <= radial * radial / 16
        radial_controls[str(offset)] = {
            "radial_per_sweep": radial,
            "tangential_per_sweep": math.sqrt(tangent_squared),
            "reference_per_sweep": expected,
            "radial_pass": radial_ok,
            "tangential_pass": tangent_ok,
        }
    run_metadata = json.loads((run / "run.json").read_text())
    coefficient = Fraction(640, reference) if positive else None
    completed = run_metadata["status"] == "completed" and run_metadata["completed_ticks"] == 84
    result = {
        "model": "electron-source-calibration-last-port-v1",
        "source_table_sha256": SOURCE_HASH,
        "source_sha256": run_metadata["source_sha256"],
        "initialization_sha256": run_metadata["initialization_sha256"],
        "run_completed": completed,
        "windows": WINDOWS,
        "per_tick_repeats": repeated,
        "six_axis_symmetry_pass": symmetry,
        "positive_reference": positive,
        "radial_controls": radial_controls,
        "reference_F8": [reference, 10],
        "force_numerator": coefficient.numerator if coefficient else None,
        "force_denominator": coefficient.denominator if coefficient else None,
        "probe_sums": {str(offset): value for offset, value in sums.items()},
        "probe_traces": {str(offset): values for offset, values in traces.items()},
        "probe_receipts": receipts,
        "max_observed_cycle_cost": max_cost,
        "delayed_cycles": delayed,
        "accounting_pass": run_metadata["accounting_balanced_at_every_completed_tick"],
        "canonical_html": str(run / "run.html"),
        "scope": "Open prepared source; last travel Port response, not heading-vector response or closed atomic energy.",
    }
    result["field_gate_pass"] = (
        completed
        and positive
        and repeated
        and symmetry
        and delayed == 0
        and result["accounting_pass"]
        and all(
            control["radial_pass"] and control["tangential_pass"] for control in radial_controls.values()
        )
    )
    return result


def run_calibration(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    initial = output / "calibration-initialization.json"
    if initial.exists():
        raise ValueError("use a new calibration directory; earlier evidence is immutable")
    initial.write_text(json.dumps(calibration_document(), indent=2) + "\n")
    with patch(
        "event_universe.fields.spatial_plan.ticket_draw", side_effect=AssertionError("unowned draw")
    ) as draws:
        run_initialization(initial, output / "run", visualize=True, frame_stride=10)
    result = analyze(output / "run")
    result["ticket_calls"] = draws.call_count
    (output / "calibration.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    result = run_calibration(arguments.output)
    print(
        json.dumps(
            {
                name: result[name]
                for name in (
                    "field_gate_pass",
                    "force_numerator",
                    "force_denominator",
                    "ticket_calls",
                    "canonical_html",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
