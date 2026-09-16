"""Exercise whole-property transport and an explicit finite local ledger exchange.

This uses the active Node scheduler. It does not implement a Register scheduler,
an electron, phase evolution, a physical force, or a physical energy law.
"""

import argparse
import json
from copy import deepcopy
from pathlib import Path

import event_universe
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization, source_fingerprint

BASE = "e5b5911ab13373e08345cf971a6ae8d7e9cb462e"
CASES = ("exchange", "zero_coupling", "missing_property", "renamed", "reordered")


def configuration(case):
    raw = json.loads(Path(__file__).with_name("input.json").read_text())
    if case not in CASES:
        raise ValueError("unknown property-packet control")
    names = {field["name"]: field["name"] for field in raw["fields"]}
    if case == "zero_coupling":
        for assignment in raw["spatial_interactions"][0]["assignments"]:
            assignment["expression"]["args"][1] = [0, 0, 0] if assignment["field"] == "momentum" else 0
    if case == "missing_property":
        inert = deepcopy(raw["disturbance_types"][0])
        inert["name"] = "unresponsive_parcel"
        inert["fields"].remove("responsive")
        del inert["defaults"]["responsive"]
        raw["disturbance_types"].append(inert)
        raw["seeds"][0]["type"] = inert["name"]
    if case == "renamed":
        names = {name: f"property_{index}" for index, name in enumerate(names)}
        mapping = {**names, "parcel": "arbitrary_layout"}

        def rename(value):
            if isinstance(value, dict):
                return {mapping.get(key, key): rename(item) for key, item in value.items()}
            if isinstance(value, list):
                return [rename(item) for item in value]
            return mapping.get(value, value) if isinstance(value, str) else value

        raw = rename(raw)
    if case == "reordered":
        raw["fields"].reverse()
        raw["disturbance_types"][0]["fields"].reverse()
        raw["spatial_fields"].reverse()
        raw["spatial_interactions"][0]["assignments"].reverse()
        raw["conservation_contract"]["quantities"].reverse()
    parse_initial_state(raw)
    return raw, names


def inspect_recording(output, names):
    html = (output / "run.html").read_text()
    marker = '<script id="recording" type="application/json">'
    recording = json.loads(html.split(marker, 1)[1].split("</script>", 1)[0])
    observations = []
    for frame in recording["frames"]:
        carriers = [
            (node["position"], record["values"], "resident")
            for node in frame["nodes"]
            for record in node["disturbances"]
        ]
        carriers.extend(
            (packet["origin"], packet["values"], "in_flight") for packet in frame["transfers"]
        )
        if len(carriers) != 1:
            raise AssertionError("the property packet must have exactly one actual owner")
        position, values, ownership = carriers[0]
        reservoir = next(
            node["fields"] for node in frame["spatial_fields"] if node["position"] == [2, 2, 2]
        )
        observations.append(
            {
                "tick": frame["tick"],
                "position": position,
                "ownership": ownership,
                "carrier": {
                    name: values[encoded] for name, encoded in names.items() if encoded in values
                },
                "reservoir": {
                    name: reservoir[names[name]]["value"] for name in ("energy_ledger", "momentum")
                },
            }
        )
    return observations


def run_case(case, output):
    source = Path(__file__).resolve().parents[2]
    if Path(event_universe.__file__).resolve() != source / "src/event_universe/__init__.py":
        raise RuntimeError("PYTHONPATH must select this checkout's src")
    fingerprint = source_fingerprint()
    raw, names = configuration(case)
    output.mkdir(parents=True, exist_ok=False)
    input_path = output / "input.json"
    input_path.write_text(json.dumps(raw, indent=2) + "\n")
    run_initialization(input_path, output / "run", visualize=True)
    observations = inspect_recording(output / "run", names)
    metadata = json.loads((output / "run/run.json").read_text())
    if source_fingerprint() != fingerprint:
        raise RuntimeError("simulator source changed during the benchmark")
    result = {
        "case": case,
        "reference_base": BASE,
        "source_sha256": fingerprint,
        "status": metadata["status"],
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "observations": observations,
    }
    (output / "observations.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", choices=CASES, default="exchange")
    args = parser.parse_args()
    result = run_case(args.case, args.output)
    print(
        json.dumps(
            {
                "case": result["case"],
                "status": result["status"],
                "html": str(args.output / "run/run.html"),
            }
        )
    )


if __name__ == "__main__":
    main()
