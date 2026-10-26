"""The writer's command line, `python -m event_universe.run <world.json> <out.json> [back N]` (ENGINE.md's standard): the world file loaded, the record written by record.record (the one module of the record since NL-S1's third stroke, 2026-10-26) and dumped as JSON."""

import json
import sys

from event_universe.loader.world import load_world
from event_universe.record import record


def main(argv: list[str]) -> None:
    """The writer from the command line: the world file, the output file, `back N` for the run back."""
    sys.set_int_max_str_digits(0)
    _, world_path, out_path, *_rest = argv
    universe, world = load_world(world_path)
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    found = record(universe, world, back, lambda line: print(line, flush=True))
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(found, out)


if __name__ == "__main__":
    main(sys.argv)
