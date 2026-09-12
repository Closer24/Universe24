"""Assemble a saved candidate law and named initial conditions as ordinary JSON."""

import argparse
import copy
import json
from pathlib import Path

from event_universe.initialization import parse_initial_state, parse_json_document

HERE = Path(__file__).resolve().parent


def configuration(case: str) -> dict:
    """Select data only; the existing simulator evaluates every physical rule."""
    raw = parse_json_document((HERE / "law.json").read_bytes())
    definitions = parse_json_document((HERE / "definition.json").read_bytes())
    cases = parse_json_document((HERE / "experiments.json").read_bytes())
    if case not in cases:
        raise ValueError(f"unknown experiment: {case}")
    selected = copy.deepcopy(cases[case])
    if set(selected) - {"seeds", "ticks", "shape", "link_ticks", "collision"}:
        raise ValueError("unsupported experiment option")
    for option in ("ticks", "shape", "link_ticks"):
        if option in selected:
            raw[option] = selected[option]
    enabled = selected.get("collision", True)
    if type(enabled) is not bool:
        raise ValueError("collision must be a boolean")
    if not enabled:
        disabled = set(definitions["collision_rules"])
        raw["field_rules"] = [rule for rule in raw["field_rules"] if rule["name"] not in disabled]
        raw["model_id"] += "-free"
    raw["spatial_seeds"] = [
        {"position": seed["position"], "field": field, "populations": [value] + [[0, 0, 0]] * 7}
        for seed in selected["seeds"]
        for field, value in seed["values"].items()
    ]
    parse_initial_state(raw)
    limit = definitions["max_abs_component"]
    if any(
        abs(component) > limit
        for seed in raw["spatial_seeds"]
        for value in seed["populations"]
        for component in value
    ):
        raise ValueError("seed exceeds the candidate amplitude bound")
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default="approach_unequal")
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
