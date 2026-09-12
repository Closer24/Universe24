"""Read actual delivered flux at equal Euclidean radii, without field feedback."""

import argparse
import itertools
import json
from pathlib import Path

from audit import configurations

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease


def measure(ticks=32):
    raw = dict(configurations())["radial-base"]
    raw["seeds"] = [s for s in raw["seeds"] if s["type"] != "probe"]
    world = Simulation(parse_initial_state(raw))
    offsets = sorted(set(itertools.permutations((1, 2, 2))))
    offsets += [(3, 0, 0), (0, 3, 0), (0, 0, 3), (-3, 0, 0), (0, -3, 0), (0, 0, -3)]
    rows = []
    for _ in range(ticks):
        world.step()
        for offset in offsets:
            position = tuple(x + 5 for x in offset)
            directions = world.spatial_values(position)["signal"]["directions"]
            flux = [directions[2 * i][0] - directions[2 * i + 1][0] for i in range(3)]
            radial = sum(f * x for f, x in zip(flux, offset, strict=True)) / 3
            transverse_squared = max(0, sum(f * f for f in flux) - radial * radial)
            rows.append(
                {
                    "tick": world.tick,
                    "offset": offset,
                    "flux": flux,
                    "radial": radial,
                    "transverse_squared": transverse_squared,
                }
            )
    return {"radius": 3, "samples": rows, "initial": raw}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        (args.output / "field_scan.json").write_text(json.dumps(measure(), indent=2))


if __name__ == "__main__":
    main()
