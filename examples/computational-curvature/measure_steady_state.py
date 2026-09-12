"""Measure the established computation-field clock gradient in one long world."""

from __future__ import annotations

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
TICKS = 64
STEADY_START = 32


def _position(value: object) -> tuple[int, int, int]:
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        raise ValueError("expected a three-dimensional position")
    return int(value[0]), int(value[1]), int(value[2])


def _world_definition() -> dict[str, object]:
    raw = parse_json_document((HERE / "configuration.json").read_bytes())
    raw["ticks"] = TICKS
    raw["normal_budget"] = 32
    raw["model_id"] = "computational-curvature-steady-state-m512-b32"
    for seed in raw["seeds"]:
        if seed["type"] == "mass_source":
            seed["values"] = {"mass": 512}
    parse_initial_state(raw)
    return raw


def _spatial_value(world: Simulation, position: tuple[int, int, int], field: str) -> int:
    return int(world.spatial_values(position)[field]["value"][0])


def _cycle_series(
    events: list[dict[str, object]], position: tuple[int, int, int]
) -> list[dict[str, int]]:
    return [
        {
            "tick": int(event["tick"]),
            "cost": int(event["cost"]),
            "ready_tick": int(event["ready_tick"]),
            "next_tick": int(event["next_tick"]),
            "period": int(event["next_tick"]) - int(event["tick"]),
        }
        for event in events
        if event["event"] == "cycle_started"
        and _position(event["position"]) == position
        and int(event["tick"]) >= STEADY_START
    ]


def main() -> None:
    output = Path("artifacts/computational-curvature-steady")
    output.mkdir(parents=True, exist_ok=False)
    raw = _world_definition()
    (output / "initialization.json").write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")

    events: list[dict[str, object]] = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    frames = [world.snapshot()]
    field_samples: list[dict[str, int]] = []
    wave_detector_tick: int | None = None
    for _ in range(TICKS):
        world.step()
        frames.append(world.snapshot())
        if wave_detector_tick is None and _spatial_value(world, (DETECTOR_X, *WAVE_LINE), "wave"):
            wave_detector_tick = world.tick
        if world.tick >= STEADY_START:
            field_samples.append(
                {
                    "tick": world.tick,
                    "near": _spatial_value(world, NEAR_CLOCK, "computation_field"),
                    "far": _spatial_value(world, FAR_CLOCK, "computation_field"),
                    "impact": _spatial_value(world, (MASS_POSITION[0], *RAY_LINE), "computation_field"),
                }
            )

    near_cycles = _cycle_series(events, NEAR_CLOCK)
    far_cycles = _cycle_series(events, FAR_CLOCK)
    ray_receives = [
        event
        for event in events
        if event["event"] == "received" and event.get("disturbance") == "massless_ray"
    ]
    ray_detector_tick = next(
        (
            int(event["tick"])
            for event in ray_receives
            if _position(event["position"]) == (DETECTOR_X, *RAY_LINE)
        ),
        None,
    )
    ray_final_x = max((_position(event["position"])[0] for event in ray_receives), default=1)
    link_durations = sorted(
        {
            int(event["arrival_tick"]) - int(event["tick"])
            for event in events
            if event["event"] == "sent" and event.get("disturbance") == "massless_ray"
        }
    )
    ray_positions = [_position(event["position"]) for event in ray_receives]
    ray_deflection = max(
        (abs(position[1] - RAY_LINE[0]) + abs(position[2] - RAY_LINE[1]) for position in ray_positions),
        default=0,
    )

    summary = {
        "ticks": TICKS,
        "steady_start": STEADY_START,
        "mass": 512,
        "normal_budget": 32,
        "near_clock": NEAR_CLOCK,
        "far_clock": FAR_CLOCK,
        "near_field_range": [
            min(sample["near"] for sample in field_samples),
            max(sample["near"] for sample in field_samples),
        ],
        "far_field_range": [
            min(sample["far"] for sample in field_samples),
            max(sample["far"] for sample in field_samples),
        ],
        "near_cycles": near_cycles,
        "far_cycles": far_cycles,
        "near_steady_periods": sorted({cycle["period"] for cycle in near_cycles}),
        "far_steady_periods": sorted({cycle["period"] for cycle in far_cycles}),
        "ray_detector_tick": ray_detector_tick,
        "ray_final_x": ray_final_x,
        "ray_deflection": ray_deflection,
        "ray_link_transit_ticks": link_durations,
        "wave_detector_tick": wave_detector_tick,
        "persistent_clock_gradient": sorted({cycle["period"] for cycle in near_cycles})
        != sorted({cycle["period"] for cycle in far_cycles}),
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:
        for event in events:
            stream.write(json.dumps(event) + "\n")
    (output / "field_samples.json").write_text(
        json.dumps(field_samples, indent=2) + "\n", encoding="utf-8"
    )
    render_disturbances(
        frames,
        output / "run.html",
        {
            "model": raw["model_id"],
            "shape": raw["shape"],
            "link_ticks": raw["link_ticks"],
            "display": "disturbances",
            "experiment": "steady-state-computational-curvature",
        },
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
