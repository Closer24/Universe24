"""Read the two cavity worlds under the record click (`amplitude-v1`, the
world key `amplitude`; the worlds `worlds/cavity_*_click.json` beside this file, which a source without the key refuses): the
world is the list of gathers in `run.json`'s `world`, one per record, one
record per birth of a lamp, and the mass of a lamp is what its partner's
clicks carry, the `content` of each gather (E = h f: h x the emitter's
turn at the birth). Every line is labelled DETECTOR (a gather: its set, its
u, its content) or GAMEBOARD (a lamp's held content in `state.json`, the
lattice's view, a labelled control). Usage:

    PYTHONPATH=<the amplitude branch's src> python docs/designs/masses/cavity_click_read.py RUNS_DIR

with `RUNS_DIR/cavity_unequal/` and `RUNS_DIR/cavity_equal/` the runner's
outputs of the `_click` worlds on `claude/amplitude-impl` (62369cb8). The
output beside this file (`cavity_click.out`) is what it printed on the
runs of 2026-09-20.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def read(run: Path) -> None:
    record = json.loads((run / "run.json").read_text(encoding="utf-8"))
    state = json.loads((run / "state.json").read_text(encoding="utf-8"))
    world = record["world"]
    print(
        f"--- {run.name}: {record['model']}, {record['completed_ticks']} intervals,"
        f" hypotheses {record['hypotheses']}, the books balanced at every tick:"
        f" {record['conserved_at_every_completed_tick']}"
    )
    print(
        f"DETECTOR  the world's list: {len(world)} gathers, {len(record['open'])} records open at the end"
    )
    by_set: dict[str, list[dict[str, object]]] = {}
    for gather in world:
        chosen = gather["chosen"]
        assert len(chosen) == 1 and gather["T"] == 1, (
            "one row per record, one offer: the cell is certain"
        )
        by_set.setdefault(chosen[0][0], []).append(gather)
    for name in sorted(by_set):
        rows = by_set[name]
        ticks = [int(g["tick"]) for g in rows]
        contents = [int(g["content"]) for g in rows]
        samples = [
            (ticks[i], contents[i])
            for i in (0, len(rows) // 4, len(rows) // 2, 3 * len(rows) // 4, len(rows) - 1)
        ]
        print(
            f"DETECTOR  set {name}: {len(rows)} clicks from tick {ticks[0]} to {ticks[-1]};"
            f" the content per click (tick, content) {samples}; the sum of the contents clicked {sum(contents)}"
        )
        us = sorted({int(g["u"]) for g in rows})
        print(
            f"DETECTOR  set {name}: the emitter's turn read as the content of a click, first {contents[0]},"
            f" last {contents[-1]}; the birth phases u seen {len(us)} of N"
        )
    for entry in state["measured"]:
        print(
            f"GAMEBOARD lamp {entry['number']} at {entry['position']}: held {entry['held']} (a control)"
        )
    books = record["audit"][-1]["families"]["light"]
    held = [entry["held"][0] for entry in state["measured"]]
    print(
        f"DETECTOR  the books at tick {record['audit'][-1]['tick']}: on the lamps {books['measured']['current']},"
        f" in transit {books['content']['current']}, cancelled {books.get('cancelled', 0)},"
        f" initial {books['measured']['initial']}; the lamps' sum {sum(held)}"
    )


def main() -> None:
    root = Path(sys.argv[1])
    for name in ("cavity_unequal", "cavity_equal"):
        read(root / name)
        print()


if __name__ == "__main__":
    main()
