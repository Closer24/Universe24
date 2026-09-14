"""Crossing null notices: two nulls decided before either notice arrives, and the correction.

Configuration on `causal-contact-fields-v1` with `"null_notices": true`. One
excitation is split over three registers S, M and D by two 3:4 mixers, so the
weights are 225/625, 144/625 and 256/625. Two moving probes reach M and D on
the same tick and both record a null. Each Node sends its own factor at once:
M's from the exact scale, D's from the stale one, because M's notice has not
arrived yet. The product of the two delivered factors is not the conditional
scale 25/9 at S; the Node whose null is ordered later by (tick, position)
answers the earlier notice with the exact correction, and S reaches 25/9 two
Links later. Offsetting the second probe by one or two ticks gives the
sequential case, where no correction is needed. Every number is a read-only
audit of the runtime report; the analytic values are computed independently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, CostMeter, OperationCosts
from event_universe.core.source_envelope_state import NullRecord
from event_universe.fields.source_envelope import null_correction
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

TEMPLATE = Path(__file__).with_name("causal_charge.json")
ROTATION = [[5, 0, 0, 0], [0, 3, -4, 0], [0, 4, 3, 0], [0, 0, 0, 5]]
SOURCE, MIDDLE, DETECTOR = (1, 1, 1), (2, 1, 1), (3, 1, 1)
WEIGHTS = {SOURCE: Fraction(225, 625), MIDDLE: Fraction(144, 625), DETECTOR: Fraction(256, 625)}
START = 4  # links the probes travel before they reach the arms
TICKS = 12
OFFSETS = (0, 1, 2)


def configuration(offset: int, *, notices: bool = True, ticks: int = TICKS) -> dict:
    """Two mixers, two moving probes; the second probe arrives `offset` ticks later."""
    raw = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    raw["model_id"] = "crossing-null-notices-v1"
    raw["shape"] = [7, 3 + START + max(OFFSETS), 3]
    raw["ticks"] = ticks
    program = raw["event_program"]
    program["model"] = "causal-contact-fields-v1"
    program["null_notices"] = notices
    program["tickets"] = [0, 0, 0, 0]
    domain = program["domains"][0]
    domain["phases"] = [
        [{"register_indices": [0, 1], "matrix": ROTATION}],
        [{"register_indices": [1, 2], "matrix": ROTATION}],
        *([[]] * 14),
    ]
    domain["capture"]["register_indices"] = [1, 2]
    for emission in raw["emissions"]:
        emission["amount"] = -25
        emission["budget"] = 1000
    raw["fields"].append(
        {"name": "heading", "components": 3, "units": "step", "signed": True, "conserved": False}
    )
    for kind in raw["disturbance_types"]:
        if kind["name"] == "contact_probe":
            kind["fields"].append("heading")
            kind["defaults"]["heading"] = [0, 0, 0]
            kind["transport"] = {"mode": "move", "direction_field": "heading"}
    raw["seeds"] = [
        {"position": list(SOURCE), "type": "incoming_charge"},
        {"position": list(SOURCE), "type": "contact_probe"},
        {
            "position": [MIDDLE[0], 1 + START, 1],
            "type": "contact_probe",
            "values": {"heading": [0, -1, 0]},
        },
        {
            "position": [DETECTOR[0], 1 + START + offset, 1],
            "type": "contact_probe",
            "values": {"heading": [0, -1, 0]},
        },
    ]
    return raw


def run(raw: dict) -> dict:
    world = Simulation(parse_initial_state(raw))
    resolver = world._resolver
    scales: list[dict[str, list[int]]] = []
    for _ in range(raw["ticks"]):
        world.step()
        report = resolver.report()
        row = {}
        for envelope in report["source_envelopes"]:
            real, imag, denominator = envelope["amplitude"]
            row[str(tuple(envelope["position"]))] = [
                real * real + imag * imag,
                denominator * denominator,
                *envelope["weight_scale"],
            ]
        scales.append(row)
    report = resolver.report()
    decisions = [
        (record.decision.tick, record.decision.register_index, list(record.decision.weights))
        for record in resolver.space.records
        if sum(w > 0 for w in record.decision.weights) > 1
    ]
    return {
        "scales": scales,
        "decisions": decisions,
        "null_corrections": report["null_corrections"],
        "final_source_scale": scales[-1][str(SOURCE)][2:],
        "balanced": all(value["balanced"] for value in world.spatial_accounting().values()),
    }


def analytic() -> dict:
    """The conditional scale, the stale product and the correction, independently of the runtime."""
    exact = 1 / (1 - WEIGHTS[MIDDLE] - WEIGHTS[DETECTOR])
    first = 1 / (1 - WEIGHTS[MIDDLE])
    stale = 1 / (1 - WEIGHTS[DETECTOR])
    conditional = 1 / (1 - WEIGHTS[DETECTOR] * first)
    meter = CostMeter(OperationCosts((1,) * len(OPERATIONS)))
    record = NullRecord(4, WEIGHTS[DETECTOR].numerator, WEIGHTS[DETECTOR].denominator)
    correction = null_correction(record, (first.numerator, first.denominator), meter)
    assert correction is not None
    quotient = Fraction(*correction[0])
    assert first * stale * quotient == exact == first * conditional
    return {
        "exact_source_scale": exact,
        "first_factor": first,
        "stale_second_factor": stale,
        "conditional_second_factor": conditional,
        "stale_product": first * stale,
        "correction": quotient,
    }


def serial(value: object) -> object:
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator, "value": float(value)}
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    targets = analytic()
    runs = {}
    for offset in OFFSETS:
        raw = configuration(offset)
        (args.output / f"offset_{offset}.json").write_text(json.dumps(raw, indent=1) + "\n")
        runs[f"offset_{offset}"] = run(raw)
    result = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "analytic": targets,
        "runs": runs,
    }
    (args.output / "summary.json").write_text(json.dumps(serial(result), indent=2) + "\n")
    print("analytic", {k: str(v) for k, v in targets.items()})
    for name, world in runs.items():
        source = [row[str(SOURCE)][2:] for row in world["scales"]]
        print(
            name,
            "S scale per tick",
            [f"{n}/{d}" for n, d in source],
            "corrections",
            world["null_corrections"],
        )
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
