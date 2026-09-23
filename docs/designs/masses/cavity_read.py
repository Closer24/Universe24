"""Read the two cavity runs of `examples/events/masses` (the mathematician,
2026-09-20): two lamps of one paid family facing each other, each measuring
the other's units. Every line is labelled DETECTOR (a click's `content`, the
turn of the partner's clock at the unit's birth: E = h f read at the
receiver; the books' balance) or GAMEBOARD (a lamp's held content in
`state.json`: the host's view). Usage:

    PYTHONPATH=src python docs/designs/masses/cavity_read.py RUNS_DIR

with `RUNS_DIR/cavity_unequal/` and `RUNS_DIR/cavity_equal/` the runner's
output directories (`python -m event_universe --init WORLD --output DIR`).
The output beside this file (`cavity.out`) is what it printed on the
runs of 2026-09-20.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from event_universe.trimmed_record import refuse_trimmed_record  # noqa: E402


def read(run: Path) -> None:
    record = json.loads((run / "run.json").read_text(encoding="utf-8"))
    state = json.loads((run / "state.json").read_text(encoding="utf-8"))
    print(
        f"--- {run.name}: {record['model']}, {record['completed_ticks']} intervals, K {record['K']}, N {record['N']}"
    )
    print(
        "DETECTOR  the books balanced at every completed tick:",
        record["conserved_at_every_completed_tick"],
        "; source",
        record["source_sha256"][:16],
    )
    clicks: dict[int, list[tuple[int, int]]] = {}
    refuse_trimmed_record(run)
    with (run / "events.jsonl").open(encoding="utf-8") as lines:
        for line in lines:
            event = json.loads(line)
            if event["event"] == "click":
                clicks.setdefault(event["measured"], []).append((event["tick"], event["content"]))
    for number in sorted(clicks):
        rows = clicks[number]
        first = rows[0]
        last = rows[-1]
        samples = [
            rows[i] for i in (0, len(rows) // 4, len(rows) // 2, 3 * len(rows) // 4, len(rows) - 1)
        ]
        print(
            f"DETECTOR  reader {number}: {len(rows)} clicks from tick {first[0]} to {last[0]};"
            f" content per click (tick, content): {samples}"
        )
        print(
            f"DETECTOR  reader {number}: the partner's turn read off the clicks: first {first[1]}, last {last[1]}"
            f" (E = h f: the content of a unit is h x the emitter's turn at its birth)"
        )
    for entry in state["measured"]:
        print(
            f"GAMEBOARD lamp {entry['number']} at {entry['position']}: held {entry['held']}, age {entry['age']},"
            f" phase {entry['phase']}, measured {entry.get('measured', '-')}"
        )
    held = [entry["held"][0] for entry in state["measured"]]
    # The books' content line at the last completed tick: what the released
    # rows carry, in transit (`content.current`), against the initial content.
    books = record["audit"][-1]["families"]["light"]
    transit_total = books["content"]["current"]
    print(
        f"DETECTOR  the books at tick {record['audit'][-1]['tick']}: on the lamps"
        f" {books['measured']['current']}, in transit {transit_total}, initial {books['measured']['initial']}"
    )
    print(
        f"GAMEBOARD the two contents {held}, in transit {transit_total}, the sum {sum(held) + transit_total}"
    )


def main() -> None:
    root = Path(sys.argv[1])
    for name in ("cavity_unequal", "cavity_equal"):
        read(root / name)
        print()


if __name__ == "__main__":
    main()
