"""THE EIGHTH HARD QUESTION (record 2140; ALGEBRA.md 9.103 (4)), THE RUN'S NUMBER: the clicks
at the receiver per giving, read from the one command's outputs (`tools/run_inputs.py --out
DIR docs/designs/rule_alone/worlds/*.json`), the well against the free cube of the same side,
and the cube's geometric share of the beam's cross-section beside them (COMPUTATION: side^2
over the board's 21 x 21, the share of a beam that fills the cross-section). DETECTOR unless
marked; no pin, no verdict here.

    PYTHONPATH=src python docs/designs/rule_alone/item8_rate_read.py DIR
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

SIDES = (5, 9, 13)
CROSS_SECTION = 21 * 21
STOCK = 100


def read(out: Path, kind: str, side: int) -> dict:
    path = out / f"item8-rate-{kind}-s{side}.output.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    clicks = data.get("clicks", [])
    at = [c for c in clicks if c["detector"] == kind]
    waits = sorted(c["interval"] - c["giving"] for c in at if "giving" in c)
    mean = sum(waits) / len(waits) if waits else float("nan")
    rms = math.sqrt(sum((w - mean) ** 2 for w in waits) / len(waits)) if waits else float("nan")
    return {
        "verdict": data.get("verdict"),
        "counts": data.get("counts"),
        "at": len(at),
        "given": len({c["record"] for c in clicks}),
        "wait_mean": mean,
        "wait_rms": rms,
        "wait_least": waits[0] if waits else None,
    }


def main() -> None:
    out = Path(sys.argv[1])
    print("== THE RATE ROW: the clicks at the receiver per 100 givings (DETECTOR)")
    print(
        "| side | receiver | clicks at it | records clicked anywhere | counts | wait mean +- rms (least) | geometric share x 100 (COMPUTATION) |"
    )
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for side in SIDES:
        share = 100.0 * side * side / CROSS_SECTION
        for kind in ("well", "cube"):
            r = read(out, kind, side)
            if not r:
                print(f"| {side} | {kind} | (no output) | | | | {share:.1f} |")
                continue
            print(
                f"| {side} | {kind} | {r['at']} | {r['given']} | {r['counts']} | "
                f"{r['wait_mean']:.0f} +- {r['wait_rms']:.0f} ({r['wait_least']}) | {share:.1f} |"
            )
    print()
    for side in SIDES:
        well, cube = read(out, "well", side), read(out, "cube", side)
        if well and cube and cube["at"]:
            print(
                f"side {side}: well / cube = {well['at']} / {cube['at']} = {well['at'] / cube['at']:.2f} "
                f"(the spread of a count n is sqrt(n): +- {math.sqrt(max(well['at'], 1)):.1f} and "
                f"+- {math.sqrt(cube['at']):.1f})"
            )


if __name__ == "__main__":
    main()
