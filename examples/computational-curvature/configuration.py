"""Prepare six-mode timing experiments using the existing local reflection law.

The previous fixed +X forwarding probe was a timing control, not a bending test.
This configuration reuses the locally mixing candidate instead of inserting a
force or rotating a recorded path. Its short pulses do not establish ray optics.
"""

import argparse
import importlib.util
import json
from pathlib import Path

from event_universe.core.disturbance_state import bounded
from event_universe.initialization import parse_initial_state, parse_json_document

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "curvature_wave_law", HERE.parent / "maxwell" / "configuration.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("the shared six-mode candidate is unavailable")
WAVE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WAVE)


def settings(path: Path = HERE / "configuration.json") -> dict:
    raw = parse_json_document(path.read_bytes())
    expected = {
        "shape",
        "ticks",
        "normal_budget",
        "link_ticks",
        "source_position",
        "source_strength",
        "wave_seed_positions",
        "near_clock",
        "far_clock",
        "observer_position",
        "directional_delay",
        "delay_control",
    }
    if set(raw) != expected:
        raise ValueError("experiment settings must contain exactly the documented keys")
    for name in ("source_strength", "ticks", "normal_budget", "link_ticks"):
        if bounded(raw[name]) < (1 if name in ("normal_budget", "link_ticks") else 0):
            raise ValueError(f"invalid {name}")
    shape = raw["shape"]
    if not isinstance(shape, list) or len(shape) != 3 or any(bounded(n) < 1 for n in shape):
        raise ValueError("shape must contain three positive extents")
    if not isinstance(raw["wave_seed_positions"], list) or not raw["wave_seed_positions"]:
        raise ValueError("wave_seed_positions must be a nonempty list")
    positions = [
        raw[name] for name in ("source_position", "near_clock", "far_clock", "observer_position")
    ]
    positions.extend(raw["wave_seed_positions"])
    for position in positions:
        if (
            not isinstance(position, list)
            or len(position) != 3
            or any(
                not 0 <= bounded(value) < extent for value, extent in zip(position, shape, strict=True)
            )
        ):
            raise ValueError("every measurement and seed position must be inside the configured shape")
    if len({tuple(p) for p in raw["wave_seed_positions"]}) != len(raw["wave_seed_positions"]):
        raise ValueError("wave seed positions must be unique")
    return raw


def configuration(
    options: dict, *, mass: int | None = None, delay: dict | None = None, mixing: bool = True
) -> dict:
    raw = WAVE.build_configuration(
        tuple(options["shape"]), options["ticks"], [], boundary="open", scatter_enabled=mixing
    )
    raw.update(
        model_id="computational-directional-delay-probe-v2",
        slots_per_cell=4,
        normal_budget=options["normal_budget"],
        link_ticks=options["link_ticks"],
        directional_delay=options["directional_delay"] if delay is None else delay,
    )
    raw["spatial_seeds"] = [
        {
            "position": list(position),
            "field": WAVE.NAMES[0],
            "populations": [[0, WAVE.AMPLITUDE_SCALE, 0], *[[0, 0, 0] for _ in range(7)]],
        }
        for position in options["wave_seed_positions"]
    ]
    for name, conserved, extensive, units in (
        ("mass", True, True, "configured source inventory unit; not SI mass"),
        ("computation_field", True, True, "transported source inventory unit"),
        ("clock_count", False, False, "completed local carrier transactions"),
        ("measured_cycle_cost", False, False, "priced model operations"),
    ):
        raw["fields"].append(
            {
                "name": name,
                "components": 1,
                "signed": False,
                "conserved": conserved,
                "extensive": extensive,
                "units": units,
            }
        )
    raw["disturbance_types"].extend(
        [
            {
                "name": "mass_source",
                "fields": ["mass"],
                "transport": {"mode": "hold"},
                "defaults": {"mass": options["source_strength"] if mass is None else mass},
            },
            {
                "name": "local_clock",
                "fields": ["clock_count", "measured_cycle_cost"],
                "transport": {"mode": "hold"},
                "cost_field": "measured_cycle_cost",
                "updates": [
                    {
                        "field": "clock_count",
                        "expression": {"op": "add", "args": [{"field": "clock_count"}, 1]},
                    }
                ],
            },
        ]
    )
    raw["seeds"] = [{"position": options["source_position"], "type": "mass_source"}]
    raw["seeds"].extend(
        {"position": options[name], "type": "local_clock"}
        for name in ("near_clock", "far_clock", "observer_position")
    )
    raw["spatial_fields"].append({"field": "computation_field", "baseline": 0, "transport": "outward"})
    raw["emissions"] = [
        {
            "type": "mass_source",
            "field": "computation_field",
            "source": True,
            "amount": {"field": "mass"},
            "denominator": 1,
        }
    ]
    control = options["delay_control"]
    if not isinstance(control, dict) or set(control) != {"field", "spatial_field", "rule"}:
        raise ValueError("delay_control requires field, spatial_field and rule definitions")
    raw["fields"].append(control["field"])
    raw["spatial_fields"].append(control["spatial_field"])
    raw["field_rules"].insert(0, control["rule"])
    parse_initial_state(raw)
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, default=HERE / "configuration.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = configuration(settings(args.settings))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(raw, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
