"""Measure whether computation-field activity produces curvature-like observables."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from event_universe import Simulation
from event_universe.diagnostics.disturbance_render import render_disturbances
from event_universe.initialization import parse_initial_state, parse_json_document

HERE = Path(__file__).resolve().parent
MASS_POSITION = (12, 8, 3)
NEAR_CLOCK = (12, 10, 3)
FAR_CLOCK = (12, 14, 3)
RAY_LINE = (12, 4)
WAVE_LINE = (12, 2)
DETECTOR_X = 21
STEADY_START = 16
END_TICK = 28

CASES = (
    ("control", 0, 32),
    ("weak_mass", 64, 32),
    ("strong_mass", 512, 32),
    ("strong_mass_tight_budget", 512, 16),
    ("strong_mass_loose_budget", 512, 64),
)


def _position(value: object) -> tuple[int, int, int]:
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        raise ValueError("expected a three-dimensional position")
    return int(value[0]), int(value[1]), int(value[2])


def _variant(mass: int, normal_budget: int) -> dict[str, object]:
    raw = copy.deepcopy(parse_json_document((HERE / "configuration.json").read_bytes()))
    raw["normal_budget"] = normal_budget
    for seed in raw["seeds"]:
        if seed["type"] == "mass_source":
            seed["values"] = {"mass": mass}
            break
    else:
        raise ValueError("mass source seed is missing")
    raw["model_id"] = f"computational-curvature-probe-m{mass}-b{normal_budget}"
    parse_initial_state(raw)
    return raw


def _cell(snapshot: dict[str, object], position: tuple[int, int, int]) -> dict[str, object] | None:
    for item in snapshot["cells"]:
        if _position(item["position"]) == position:
            return item
    return None


def _record_value(
    snapshot: dict[str, object],
    position: tuple[int, int, int],
    disturbance: str,
    field: str,
) -> int | None:
    cell = _cell(snapshot, position)
    if cell is None:
        return None
    for record in cell["disturbances"]:
        if record["type"] == disturbance:
            values = record["values"][field]
            return int(values[0])
    return None


def _spatial_cost(snapshot: dict[str, object], position: tuple[int, int, int]) -> int:
    for item in snapshot.get("spatial_fields", []):
        if _position(item["position"]) == position:
            return int(item["cost"])
    return 0


def _spatial_value(world: Simulation, position: tuple[int, int, int], field: str) -> int:
    return int(world.spatial_values(position)[field]["value"][0])


def _wave_positions(snapshot: dict[str, object]) -> list[tuple[int, int, int]]:
    positions: set[tuple[int, int, int]] = set()
    for item in snapshot.get("spatial_fields", []):
        fields = item["fields"]
        if "wave" in fields and int(fields["wave"]["value"][0]) != 0:
            positions.add(_position(item["position"]))
    for item in snapshot.get("spatial_transfers", []):
        fields = item["fields"]
        if "wave" not in fields:
            continue
        if any(any(int(component) for component in payload) for payload in fields["wave"]):
            positions.add(_position(item["origin"]))
            target = item["target"]
            if target is not None:
                positions.add(_position(target))
    return sorted(positions)


def _clock_count(samples: list[dict[str, object]], tick: int, key: str) -> int:
    for sample in samples:
        if sample["tick"] == tick:
            value = sample[key]
            if value is None:
                raise ValueError(f"missing {key} at tick {tick}")
            return int(value)
    raise ValueError(f"missing sample at tick {tick}")


def run_case(name: str, mass: int, normal_budget: int, output: Path) -> dict[str, object]:
    raw = _variant(mass, normal_budget)
    run_dir = output / name
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "initialization.json").write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")

    events: list[dict[str, object]] = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    frames = [world.snapshot()]
    samples: list[dict[str, object]] = []
    wave_detector_tick: int | None = None

    for _ in range(int(raw["ticks"])):
        world.step()
        snapshot = world.snapshot()
        frames.append(snapshot)
        if wave_detector_tick is None and _spatial_value(world, (DETECTOR_X, *WAVE_LINE), "wave"):
            wave_detector_tick = world.tick
        samples.append(
            {
                "tick": world.tick,
                "near_computation": _spatial_value(world, NEAR_CLOCK, "computation_field"),
                "far_computation": _spatial_value(world, FAR_CLOCK, "computation_field"),
                "ray_impact_computation": _spatial_value(
                    world, (MASS_POSITION[0], *RAY_LINE), "computation_field"
                ),
                "near_spatial_cost": _spatial_cost(snapshot, NEAR_CLOCK),
                "far_spatial_cost": _spatial_cost(snapshot, FAR_CLOCK),
                "near_clock": _record_value(snapshot, NEAR_CLOCK, "local_clock", "clock_count"),
                "far_clock": _record_value(snapshot, FAR_CLOCK, "local_clock", "clock_count"),
                "near_measured_cycle_cost": _record_value(
                    snapshot, NEAR_CLOCK, "local_clock", "measured_cycle_cost"
                ),
                "far_measured_cycle_cost": _record_value(
                    snapshot, FAR_CLOCK, "local_clock", "measured_cycle_cost"
                ),
                "wave_positions": _wave_positions(snapshot),
            }
        )

    ray_events = [
        event
        for event in events
        if event["event"] in {"sent", "received"} and event.get("disturbance") == "massless_ray"
    ]
    ray_detector_tick = next(
        (
            int(event["tick"])
            for event in ray_events
            if event["event"] == "received" and _position(event["position"]) == (DETECTOR_X, *RAY_LINE)
        ),
        None,
    )
    ray_positions = [_position(event["position"]) for event in ray_events]
    ray_lateral_deflection = max(
        (abs(position[1] - RAY_LINE[0]) + abs(position[2] - RAY_LINE[1]) for position in ray_positions),
        default=0,
    )
    wave_positions = [position for sample in samples for position in sample["wave_positions"]]
    wave_lateral_deflection = max(
        (
            abs(position[1] - WAVE_LINE[0]) + abs(position[2] - WAVE_LINE[1])
            for position in wave_positions
        ),
        default=0,
    )
    sent_link_durations = sorted(
        {
            int(event["arrival_tick"]) - int(event["tick"])
            for event in events
            if event["event"] == "sent" and event.get("disturbance") == "massless_ray"
        }
    )
    near_final = _clock_count(samples, int(raw["ticks"]), "near_clock")
    far_final = _clock_count(samples, int(raw["ticks"]), "far_clock")
    near_steady = near_final - _clock_count(samples, STEADY_START, "near_clock")
    far_steady = far_final - _clock_count(samples, STEADY_START, "far_clock")

    metadata = {
        "model": raw["model_id"],
        "shape": raw["shape"],
        "link_ticks": raw["link_ticks"],
        "fields": [field["name"] for field in raw["fields"]],
        "disturbance_types": [kind["name"] for kind in raw["disturbance_types"]],
        "display": "disturbances",
        "experiment": name,
        "mass": mass,
        "normal_budget": normal_budget,
    }
    render_disturbances(frames, run_dir / "run.html", metadata)
    with (run_dir / "events.jsonl").open("w", encoding="utf-8") as stream:
        for event in events:
            stream.write(json.dumps(event) + "\n")
    (run_dir / "state.json").write_text(json.dumps(world.snapshot(), indent=2) + "\n", encoding="utf-8")
    (run_dir / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")

    return {
        "name": name,
        "mass": mass,
        "normal_budget": normal_budget,
        "ray_detector_tick": ray_detector_tick,
        "wave_detector_tick": wave_detector_tick,
        "ray_lateral_deflection": ray_lateral_deflection,
        "wave_lateral_deflection": wave_lateral_deflection,
        "ray_link_transit_ticks": sent_link_durations,
        "near_clock_final": near_final,
        "far_clock_final": far_final,
        "near_clock_steady_cycles": near_steady,
        "far_clock_steady_cycles": far_steady,
        "near_computation_max": max(int(sample["near_computation"]) for sample in samples),
        "far_computation_max": max(int(sample["far_computation"]) for sample in samples),
        "impact_computation_max": max(int(sample["ray_impact_computation"]) for sample in samples),
        "near_spatial_cost_max": max(int(sample["near_spatial_cost"]) for sample in samples),
        "far_spatial_cost_max": max(int(sample["far_spatial_cost"]) for sample in samples),
        "near_reported_cycle_cost_final": samples[-1]["near_measured_cycle_cost"],
        "far_reported_cycle_cost_final": samples[-1]["far_measured_cycle_cost"],
        "visualization": str((run_dir / "run.html").relative_to(output)),
    }


def classify(results: list[dict[str, object]]) -> dict[str, object]:
    by_name = {item["name"]: item for item in results}
    control = by_name["control"]
    weak = by_name["weak_mass"]
    strong = by_name["strong_mass"]

    def delay(item: dict[str, object], key: str) -> int | None:
        value, baseline = item[key], control[key]
        return None if value is None or baseline is None else int(value) - int(baseline)

    weak_ray_delay = delay(weak, "ray_detector_tick")
    strong_ray_delay = delay(strong, "ray_detector_tick")
    weak_wave_delay = delay(weak, "wave_detector_tick")
    strong_wave_delay = delay(strong, "wave_detector_tick")
    steady_clock_gradient = int(strong["near_clock_steady_cycles"]) < int(
        strong["far_clock_steady_cycles"]
    )
    amplitude_scaling = (
        weak_ray_delay is not None and strong_ray_delay is not None and strong_ray_delay > weak_ray_delay
    )
    full_curvature_signature = all(
        (
            strong_ray_delay is not None and strong_ray_delay > 0,
            strong_wave_delay is not None and strong_wave_delay > 0,
            int(strong["ray_lateral_deflection"]) > 0,
            int(strong["wave_lateral_deflection"]) > 0,
            steady_clock_gradient,
            amplitude_scaling,
        )
    )
    return {
        "weak_ray_delay_ticks": weak_ray_delay,
        "strong_ray_delay_ticks": strong_ray_delay,
        "weak_wave_delay_ticks": weak_wave_delay,
        "strong_wave_delay_ticks": strong_wave_delay,
        "steady_near_clock_slower_than_far": steady_clock_gradient,
        "stronger_mass_increases_ray_delay": amplitude_scaling,
        "full_curvature_signature_observed": full_curvature_signature,
        "interpretation_rule": (
            "A complete curvature-like result requires coordinate delay, spatial-wave delay, "
            "path bending, a persistent near/far clock-rate gradient and monotonic mass scaling "
            "without adding an explicit turning or gravity law."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    results = [run_case(name, mass, budget, args.output) for name, mass, budget in CASES]
    report = {
        "geometry": {
            "mass_position": MASS_POSITION,
            "near_clock": NEAR_CLOCK,
            "far_clock": FAR_CLOCK,
            "ray_line_yz": RAY_LINE,
            "wave_line_yz": WAVE_LINE,
            "detector_x": DETECTOR_X,
            "steady_rate_window": [STEADY_START, END_TICK],
        },
        "measurements": results,
        "classification": classify(results),
    }
    path = args.output / "measurements.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(path)


if __name__ == "__main__":
    main()
