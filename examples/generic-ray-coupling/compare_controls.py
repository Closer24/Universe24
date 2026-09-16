"""Run the preregistered finite-residence and open-boundary controls.

Expectations follow docs/SHARED_RAY_COUPLING.md. The fixture starts with funded
sources, so the rays meet at tick 1; the retained intervals end at ticks 2 and 3.
No parameter is fitted to these runs. The wide control changes only distant
boundaries, so it exposes the configured phase cycle before either ray escapes.
"""

import argparse
import copy
import json
from pathlib import Path

from evidence import compare_expected
from run_experiments import run_document


def controls(document):
    configurations = {"residence": copy.deepcopy(document)}
    disabled = copy.deepcopy(document)
    disabled["ray_interactions"] = []
    configurations["uncoupled"] = disabled
    phase = copy.deepcopy(document)
    for emission in phase["emissions"]:
        emission["kerengonen_phase"] = 0
    configurations["phase_control"] = phase
    wide = copy.deepcopy(document)
    wide["shape"][0] = 21
    for seed in wide["seeds"]:
        seed["position"][0] += 5
    configurations["wide"] = wide
    return configurations


def score(directory, name):
    recording = json.loads((directory / "ray-recording.json").read_text(encoding="utf-8"))
    frames = recording["frames"]
    expected = {
        1: {"amount": 10, "momentum": [0, 0, 0], "phases": [0, 0], "delays": [0, 0]},
        2: {"amount": 10, "momentum": [0, 0, 0], "phases": [1, 1], "delays": [1, 1]},
        3: {"amount": 10, "momentum": [0, 0, 0], "phases": [2, 2], "delays": [0, 0]},
        4: {"amount": 10, "momentum": [0, 0, 0], "phases": [3, 3], "delays": [0, 0]},
    }
    if name == "uncoupled":
        expected = {2: {"amount": 10, "phases": [1, 1], "delays": [0, 0]}}
    elif name == "phase_control":
        expected = {2: {"amount": 10, "phases": [2, 2], "delays": [0, 0]}}
    elif name == "wide":
        expected[9] = {"amount": 10, "phases": [0, 0], "delays": [0, 0]}
    result = compare_expected(frames, expected, field="wave")
    indexed = {frame["tick"]: frame for frame in frames}
    center = 10 if name == "wide" else 5

    def positions(tick):
        return sorted(item["position"] for item in indexed[tick]["rays"] if item["owner"] == "node")

    if name in ("residence", "wide"):
        location_checks = {
            "two_retained_intervals": positions(2) == positions(3) == [[center, 3, 3]] * 2,
            "released_to_neighbors": positions(4) == [[center - 1, 3, 3], [center + 1, 3, 3]],
        }
    else:
        location_checks = {"no_retention": positions(2) == [[4, 3, 3], [6, 3, 3]]}
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
    sent = [event for event in events if event["event"] == "spatial_sent"]
    location_checks["causal_link_time"] = bool(sent) and all(
        event["arrival_tick"] - event["tick"] == 1 for event in sent
    )
    if name in ("residence", "wide"):
        release = [event for event in sent if event["position"] == [center, 3, 3] and event["tick"] == 3]
        location_checks["release_timestamp"] = len(release) == 2 and all(
            event["arrival_tick"] == 4 for event in release
        )
    location_checks["funded_stock_preserved"] = all(
        frame["totals"]["wave"][0] + frame["escaped_totals"]["wave"][0] == 10 for frame in frames
    )
    result.update(
        status="pass" if result["pass"] and all(location_checks.values()) else "fail",
        checks=location_checks,
        source_sha256=recording["source_sha256"],
        initialization_sha256=recording["initialization_sha256"],
        phase_period_intervals=8 if name == "wide" else None,
        spatial_recurrence="not observed; released rays separate",
        stable_nucleus="not established",
        electron_bound_state="not exercised",
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    fixture = Path(__file__).with_name("finite-residence.json")
    document = json.loads(fixture.read_text(encoding="utf-8"))
    results = {}
    for name, configuration in controls(document).items():
        directory = args.output / name
        run_document(configuration, directory)
        results[name] = score(directory, name)
    (args.output / "acceptance.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))
    if any(result["status"] != "pass" for result in results.values()):
        raise SystemExit("One or more preregistered controls failed")


if __name__ == "__main__":
    main()
