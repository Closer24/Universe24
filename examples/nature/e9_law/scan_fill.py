"""Read, through the Simulation API, which lengths of the prefill the engine admits
for E9's ring under the law (docs/EXPERIMENTS.md, E9 repeated under the law of
the bit, 2026-09-18): for each fill, whether the world is admitted, the shadows
at the start and, over `--ticks` intervals, whether the run completes or at
which tick it fails, with the message. A Recorder of the engine's answers; it
changes nothing and writes `scan.json`. (The ray slot budget the first scan
walked, at 24 and 32 slots, was retired with the lanes on 2026-09-18,
cleanup-law-v1 part 2; the scan is over the fill alone.)

Run:  PYTHONPATH=src python examples/nature/e9_law/scan_fill.py [--ticks 40] [--out FILE]
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.json_documents import parse_json_document
from event_universe.runner import source_fingerprint

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from make_worlds import ring_world  # noqa: E402


def scan(ticks: int) -> dict:
    rows = []
    for fill in (1, 2, 3, 4, 5, 6, 7, 8, 16):
        document = copy.deepcopy(ring_world(clock=True, fill=fill))
        row = {
            "fill": fill,
            "admitted": None,
            "failed_tick": None,
            "error": None,
        }
        tick = 0
        try:
            initial = prepare_initialization(parse_json_document(json.dumps(document).encode())).initial
            with Simulation(initial) as world:
                row["admitted"] = True
                row["initial_shadows"] = int(world.totals()["electron"][0])
                while tick < ticks:
                    tick += 1
                    world.step()
                row["completed_ticks"] = ticks
        except Exception as error:  # the refusal is the reading
            if row["admitted"] is None:
                row["admitted"] = False
            else:
                row["failed_tick"] = tick
            row["error"] = str(error)
        rows.append(row)
        print(json.dumps(row))
    return {"source_sha256": source_fingerprint(), "ticks": ticks, "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticks", type=int, default=40)
    parser.add_argument("--out", type=Path, default=HERE / "scan.json")
    args = parser.parse_args()
    args.out.write_text(json.dumps(scan(args.ticks), indent=1) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
