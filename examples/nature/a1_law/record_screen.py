"""Record what the marks of a screen receive, tick by tick, by replaying a run (a
Recorder in the sense of Highlights 3.29 and 3.30, like the ray viewer's
`record_sidecar.py`: it reads the engine to store evidence and changes nothing).

A mark that only returns shadows publishes no record (a mark's record is kept
when it absorbs a thing or a shadow comes home to it, `core/spatial_node.py`),
so the shadows a screen returns and the push a thing at the mark's Node would
read are not in the runner's files. This tool replays the run's preserved
`initialization.json` through the Simulation API for its completed ticks,
checks the source fingerprint against `run.json` and the replay's events
against `events.jsonl` line for line, and after every tick reads, at each mark
of the screen (the marks at `--screen-x`), the shadows the mark turned back in
that interval (the mark's resident rays with bit 0 and steps 0, each leaving
on the reverse of the heading it arrived by): their amount n, the push
J = sum of amount x arrival heading (a returning share counted with the
opposite sign, return-field-v1), their phases and owners; the things resident
there; the shadows the other marks (the wall) turned back in all; and the
amount resident at declared probe Nodes of the dense region (`--probe x,y,z`),
with the amount in the region beyond the screen-side of the wall.

Run:  PYTHONPATH=src python examples/nature/a1_law/record_screen.py RUN --screen-x 40
      [--wall-x 16] [--probe 17,24,8 ...] [--out FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.json_documents import parse_json_document
from event_universe.runner import source_fingerprint

COPIED_KEYS = (
    "model",
    "source_sha256",
    "initialization_sha256",
    "status",
    "completed_ticks",
    "requested_ticks",
    "shape",
    "boundary",
)


def _address(text: str) -> tuple[int, int, int]:
    x, y, z = (int(v) for v in text.split(","))
    return (x, y, z)


def record(
    run: Path, screen_x: int, wall_x: int | None, probes: list[tuple[int, int, int]]
) -> dict[str, Any]:
    directory = run if run.is_dir() else run.parent
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    source = (directory / "initialization.json").read_bytes()
    if hashlib.sha256(source).hexdigest() != metadata["initialization_sha256"]:
        raise ValueError("initialization.json differs from the run's initialization_sha256")
    if source_fingerprint() != metadata["source_sha256"]:
        raise ValueError("this source tree is not the one that made the run (source_sha256)")
    initial = prepare_initialization(parse_json_document(source)).initial
    families = [
        (index, definition)
        for index, definition in enumerate(initial.spatial_fields)
        if definition.rays and definition.spread
    ]
    if len(families) != 1:
        raise ValueError("one family with a shadow set is expected")
    family_index, definition = families[0]
    headings = definition.headings
    screen = sorted(
        (mark.position for mark in initial.detectors if mark.position[0] == screen_x),
        key=lambda p: (p[1], p[2]),
    )
    wall = [mark.position for mark in initial.detectors if mark.position[0] != screen_x]
    if not screen:
        raise ValueError(f"no mark at x = {screen_x}")
    ticks = int(metadata["completed_ticks"])
    n = [[0] * len(screen) for _ in range(ticks + 1)]
    j = [[[0, 0, 0] for _ in screen] for _ in range(ticks + 1)]
    things = [[0] * len(screen) for _ in range(ticks + 1)]
    phases: list[Counter[int]] = [Counter() for _ in screen]
    owners: list[Counter[int]] = [Counter() for _ in screen]
    wall_returned = [0] * (ticks + 1)
    probe_rows = {"{},{},{}".format(*p): [0] * (ticks + 1) for p in probes}
    beyond = [0] * (ticks + 1)
    events: list[dict[str, Any]] = []

    def read_mark(
        spatial: Any, position: tuple[int, int, int]
    ) -> tuple[int, list[int], int, Counter, Counter]:
        node = spatial.nodes.get(position)
        amount, push, resident = 0, [0, 0, 0], 0
        phase_count: Counter[int] = Counter()
        owner_count: Counter[int] = Counter()
        if node is None or not node.rays:
            return amount, push, resident, phase_count, owner_count
        for ray in node.rays[family_index]:
            if ray.parked:
                continue
            if ray.detector != 0:
                resident += ray.amount
                continue
            if ray.steps != 0:
                continue
            # Turned back this interval: it leaves on the reverse of its arrival.
            arrival = tuple(-c for c in headings[ray.heading])
            sign = 1 if ray.outbound else -1
            amount += ray.amount
            for axis in range(3):
                push[axis] += sign * ray.amount * arrival[axis]
            phase_count[ray.phase] += ray.amount
            owner_count[ray.owner] += ray.amount
        return amount, push, resident, phase_count, owner_count

    with Simulation(initial, observer=events.append) as world:
        spatial = world._spatial
        region = spatial.dense
        family = None if region is None else region.families.get(family_index)
        for tick in range(1, ticks + 1):
            world.step()
            for k, position in enumerate(screen):
                amount, push, resident, phase_count, owner_count = read_mark(spatial, position)
                n[tick][k] = amount
                j[tick][k] = push
                things[tick][k] = resident
                phases[k].update(phase_count)
                owners[k].update(owner_count)
            total = 0
            for position in wall:
                total += read_mark(spatial, position)[0]
            wall_returned[tick] = total
            for position in probes:
                key = "{},{},{}".format(*position)
                node = spatial.nodes.get(position)
                if node is not None and node.rays:
                    probe_rows[key][tick] = sum(
                        ray.amount
                        for ray in node.rays[family_index]
                        if ray.detector == 0 and not ray.parked
                    )
                elif family is not None:
                    probe_rows[key][tick] = int(family.arr_amt[position].sum())
            if family is not None and wall_x is not None:
                beyond[tick] = int(family.arr_amt[wall_x + 1 :].sum())
        finals = {name: list(values) for name, values in world.totals().items()}
    if metadata["status"] == "completed" and finals != {
        k: list(v) for k, v in metadata["final_totals"].items()
    }:
        raise ValueError("the replay's final totals differ from run.json")
    recorded = [
        json.loads(line)
        for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    replayed = [json.loads(json.dumps(event)) for event in events]
    # A failed record also holds the events of the tick that failed; the replay
    # stops at the last completed tick, so it must be the record's prefix.
    if replayed != recorded[: len(replayed)] or (
        metadata["status"] == "completed" and len(replayed) != len(recorded)
    ):
        raise ValueError(f"the replay's {len(replayed)} events differ from the {len(recorded)} recorded")
    return {
        **{key: metadata.get(key) for key in COPIED_KEYS},
        "recorded_by": "examples/nature/a1_law/record_screen.py: replay through Simulation",
        "family": initial.fields[definition.field].name,
        "phase_width": definition.phase_modulus,
        "screen_x": screen_x,
        "wall_x": wall_x,
        "screen": [list(p) for p in screen],
        "wall_marks": len(wall),
        "ticks": ticks,
        "n": n,
        "j": j,
        "things_resident": things,
        "phases": [{str(k): v for k, v in sorted(c.items())} for c in phases],
        "owners": [{str(k): v for k, v in sorted(c.items())} for c in owners],
        "wall_returned": wall_returned,
        "probes": probe_rows,
        "beyond_wall": beyond,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="run.json or the directory that holds it")
    parser.add_argument("--screen-x", type=int, required=True)
    parser.add_argument("--wall-x", type=int)
    parser.add_argument("--probe", action="append", default=[], help="x,y,z of a Node to read")
    parser.add_argument("--out", type=Path, help="default: screen.json beside run.json")
    args = parser.parse_args()
    directory = args.run if args.run.is_dir() else args.run.parent
    document = record(args.run, args.screen_x, args.wall_x, [_address(p) for p in args.probe])
    target = args.out or directory / "screen.json"
    target.write_text(json.dumps(document) + "\n", encoding="utf-8")
    print(
        json.dumps({"screen": str(target), "bytes": target.stat().st_size, "ticks": document["ticks"]})
    )


if __name__ == "__main__":
    main()
