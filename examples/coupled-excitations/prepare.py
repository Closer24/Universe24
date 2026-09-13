"""Assemble the explicit unit exchange law and validate its finite input envelope."""

import argparse
import copy
import json
from pathlib import Path

from event_universe.initialization import parse_initial_state, parse_json_document

HERE = Path(__file__).resolve().parent


def validate_configuration(raw: dict) -> None:
    """Check the generic schema and this candidate's initial ownership envelope."""
    parse_initial_state(raw)
    definition = parse_json_document((HERE / "definition.json").read_bytes())
    allowed = {tuple(value) for value in definition["allowed_amplitudes"]}
    limits = definition["limits"]
    if raw.get("boundary", "periodic") not in limits["supported_boundaries"]:
        raise ValueError("the unit exchange probe requires a periodic boundary")
    if raw.get("emissions"):
        raise ValueError("the unit exchange probe does not admit ongoing sources")
    seeds = raw.get("seeds", [])
    if len(seeds) > limits["max_carriers"]:
        raise ValueError("the unit exchange probe admits at most one carrier")
    types = {item["name"]: item for item in raw["disturbance_types"]}
    for seed in seeds:
        values = {**types[seed["type"]].get("defaults", {}), **seed.get("values", {})}
        if seed["type"] != definition["carrier_type"]:
            raise ValueError("the unit exchange probe requires its explicit carrier type")
        if tuple(values.get("internal", [0, 0, 0])) not in allowed:
            raise ValueError("internal state must be empty or a unit transverse vector")
        if values.get("coupling", 0) not in definition["allowed_couplings"]:
            raise ValueError("coupling must be -1, 0 or 1")
    for field in raw.get("spatial_fields", []):
        baseline = field.get("baseline", 0)
        components = baseline if isinstance(baseline, list) else [baseline]
        if any(components):
            raise ValueError("the unit exchange probe requires zero spatial baselines")
    packets = 0
    gates = []
    emission_trigger = False
    for seed in raw.get("spatial_seeds", []):
        if seed["field"] == "amplitude":
            for value in seed["populations"]:
                if tuple(value) not in allowed:
                    raise ValueError("amplitude must be empty or a unit transverse vector")
                packets += int(any(value))
        elif seed["field"] == "gate":
            value = sum(seed["populations"])
            if value not in (0, 1, 2):
                raise ValueError("gate must be 0, 1 or 2")
            if any(item not in (0, 1, 2) for item in seed["populations"]):
                raise ValueError("gate populations must be 0, 1 or 2")
            emission_trigger = emission_trigger or value == 2
            if value:
                gates.append(seed["position"])
        else:
            raise ValueError("the unit exchange probe admits only amplitude and gate stock")
    if packets > limits["max_initial_amplitude_packets"]:
        raise ValueError("the unit exchange probe admits at most one initial amplitude packet")
    if emission_trigger and packets:
        raise ValueError("an emission trigger cannot coexist with an initial amplitude packet")
    if len(gates) > limits["max_nonzero_gates"]:
        raise ValueError("the unit exchange probe admits at most one nonzero gate")
    if seeds and any(position != seeds[0]["position"] for position in gates):
        raise ValueError("the local gate must occupy the carrier's node")


def configuration(case: str = "incoming_positive") -> dict:
    """Select initial data; all physical updates remain in the saved JSON law."""
    raw = parse_json_document((HERE / "law.json").read_bytes())
    cases = parse_json_document((HERE / "experiments.json").read_bytes())
    if case not in cases:
        raise ValueError(f"unknown experiment: {case}")
    selected = copy.deepcopy(cases[case])
    if set(selected) - {"seeds", "spatial_seeds", "ticks", "normal_budget", "link_ticks", "shape"}:
        raise ValueError("unsupported experiment option")
    raw.update(selected)
    validate_configuration(raw)
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default="incoming_positive")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = configuration(args.case)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(raw, stream, indent=2)
        stream.write("\n")
    print(args.output)


if __name__ == "__main__":
    main()
