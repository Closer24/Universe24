"""Check the existing mixing-wave invariant under asynchronous origin waits."""

import argparse
import importlib.util
import json
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease


def configurations():
    path = Path(__file__).parents[1] / "maxwell/configuration.py"
    spec = importlib.util.spec_from_file_location("shared_wave_configuration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name, load in (("control", None), ("zero_wait", [0, 0, 0]), ("directional_wait", [2, 0, 0])):
        raw = module.build_configuration(
            shape=(33, 33, 33), ticks=12, moments=[((16, 16, 16), (0, 1, 0), (0, 0, 1))], boundary="open"
        )
        if load is not None:
            raw["fields"].append(
                {
                    "name": "load",
                    "components": 3,
                    "units": "test load",
                    "signed": True,
                    "conserved": True,
                }
            )
            raw["spatial_fields"].append({"field": "load", "baseline": load, "transport": "local"})
            raw["directional_delay"] = {
                "model_id": "positive-projection-origin-wait-v1",
                "field": "load",
                "divisor": 1,
            }
        yield name, raw, module.NAMES


def norm(frame, names):
    retained = sum(
        sum(v * v for v in cell["fields"][name]["value"])
        for cell in frame["spatial_fields"]
        for name in names
    )
    transfers = sum(
        sum(sum(pop[i] for pop in packet["fields"][name]) ** 2 for i in range(3))
        for packet in frame["spatial_transfers"]
        for name in names
    )
    return retained + transfers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        summary = {}
        for name, raw, names in configurations():
            world = Simulation(parse_initial_state(raw))
            rows = []
            failure = None
            for tick in range(raw["ticks"] + 1):
                if tick:
                    try:
                        world.step()
                    except (ValueError, RuntimeError) as exc:
                        failure = str(exc)
                        break
                frame = world.snapshot()
                rows.append(
                    {
                        "tick": world.tick,
                        "owned_mode_norm": norm(frame, names),
                        "waiting_packets": sum(
                            p.get("phase") == "waiting" for p in frame["spatial_transfers"]
                        ),
                    }
                )
            result = {
                "failure": failure,
                "rows": rows,
                "norm_preserved": all(r["owned_mode_norm"] == rows[0]["owned_mode_norm"] for r in rows),
            }
            summary[name] = result
            (args.output / (name + ".json")).write_text(
                json.dumps({"initial": raw, "result": result}, indent=2)
            )
            print(name, result["norm_preserved"], failure, rows[-1], flush=True)
        (args.output / "summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
