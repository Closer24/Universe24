"""Read the record of a helium-orbit run (E8) and print the electron tick by tick.

A Renderer in the sense of Highlights 3.29: it reads ``run.json``,
``initialization.json`` and ``events.jsonl`` that the runner wrote and never the
engine. For every tick it prints the electron's Node, its offset and distance
from the nucleus (L1 and Euclidean), its momentum register (the last ``ray_push``
record's ``after``; the default amount x heading before any push), the pushes of
the tick (count and vector sum), what the nucleus's sink took and the body's
momentum after it. Then the verdict: the launch tick, whether the electron
reached the nucleus's Node, escaped, or returned to a Node it had visited with the
same register (a closed orbit), the observed period as the interval between its
crossings of the +X half-axis, the radial range, and the ledger.

Run:  python examples/nature/helium_orbit_table.py RUN [--family electron]
where RUN is a ``run.json`` file or the directory that holds it.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def load(directory: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    initialization = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    return metadata, initialization


def read_rows(directory: Path, metadata: dict[str, Any], family: str, nucleus: tuple[int, ...]):
    """One row per tick from the event stream, read line by line (the stream is large)."""
    positions: dict[int, tuple[int, ...]] = {}
    pushes: dict[int, list[dict[str, Any]]] = {}
    sink: dict[int, list[dict[str, Any]]] = {}
    escaped: list[dict[str, Any]] = []
    with (directory / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            event = json.loads(line)
            kind = event.get("event")
            tick = int(event.get("tick", -1))
            if kind == "spatial_received":
                for readings in event.get("received_fields") or ():
                    if readings and readings.get(family, [0])[0]:
                        positions[tick] = tuple(event["position"])
            elif kind == "ray_push" and event.get("family") == family:
                pushes.setdefault(tick, []).append(event)
            elif kind == "external_body_absorbed" and tuple(event["position"]) == nucleus:
                sink.setdefault(tick, []).append(event)
            elif kind == "spatial_escaped" and (event.get("escaped") or {}).get(family, [0])[0]:
                escaped.append(event)
    return positions, pushes, sink, escaped


def table(directory: Path, family: str) -> dict[str, Any]:
    metadata, initialization = load(directory)
    body = metadata["external_bodies"][0]
    nucleus = tuple(body["initial_position"])
    emission = next(e for e in initialization["emissions"] if e["field"] == family)
    amount = int(emission["amount"])
    heading = emission["heading"]
    register = tuple(amount * h for h in heading)
    positions, pushes, sink, escaped = read_rows(directory, metadata, family, nucleus)
    ticks = int(metadata["completed_ticks"])
    at = None
    rows = []
    momentum = tuple(body["initial_momentum"])
    for tick in range(1, ticks + 1):
        if tick in positions:
            at = positions[tick]
        if at is None:
            continue
        tick_pushes = pushes.get(tick, [])
        total = [0, 0, 0]
        for push in tick_pushes:
            for axis in range(3):
                total[axis] += push["after"][axis] - push["before"][axis]
            register = tuple(push["after"])
        taken = sum(int(e["amount"]) for e in sink.get(tick, []))
        if sink.get(tick):
            momentum = tuple(sink[tick][-1]["momentum"])
        offset = tuple(at[i] - nucleus[i] for i in range(3))
        rows.append(
            {
                "tick": tick,
                "position": at,
                "offset": offset,
                "l1": sum(abs(v) for v in offset),
                "euclid": math.sqrt(sum(v * v for v in offset)),
                "register": register,
                "pushes": len(tick_pushes),
                "push": tuple(total),
                "sink": taken,
                "body_momentum": momentum,
            }
        )
    return {
        "metadata": metadata,
        "nucleus": nucleus,
        "rows": rows,
        "escaped": escaped,
        "launcher": tuple(metadata["external_bodies"][1]["initial_position"])
        if len(metadata["external_bodies"]) > 1
        else None,
    }


def verdict(result: dict[str, Any]) -> dict[str, Any]:
    rows = result["rows"]
    nucleus = result["nucleus"]
    launcher = result["launcher"]
    launch = next(
        (r["tick"] for r in rows if launcher is None or r["position"] != launcher),
        None,
    )
    if launch is not None:
        launch = next((r["tick"] for r in rows if r["tick"] > 1 and r["position"] != launcher), None)
    moving = [r for r in rows if launch is not None and r["tick"] >= launch]
    fall = next((r["tick"] for r in moving if r["position"] == nucleus), None)
    escape = result["escaped"][0]["tick"] if result["escaped"] else None
    crossings = []
    previous = None
    for r in moving:
        dx, dy, _ = r["offset"]
        if previous is not None and previous < 0 <= dy and dx > 0:
            crossings.append(r["tick"])
        previous = dy
    # A closed orbit: a Node visited again with the same register after at least one
    # circuit around the nucleus (a crossing of the +X half-axis in between); the
    # two-Link cage of E4 through the nucleus repeats its state and is not one.
    seen: dict[tuple[Any, Any], int] = {}
    closed = None
    for r in moving:
        key = (r["position"], r["register"])
        first = seen.get(key)
        if (
            first is not None
            and closed is None
            and any(first < crossing <= r["tick"] for crossing in crossings)
        ):
            closed = (first, r["tick"])
        seen.setdefault(key, r["tick"])
    periods = [b - a for a, b in zip(crossings, crossings[1:], strict=False)]
    distances = [r["euclid"] for r in moving]
    l1s = [r["l1"] for r in moving]
    pushed = [r for r in moving if r["pushes"]]
    audit = result["metadata"].get("audit") or []
    return {
        "launch_tick": launch,
        "fall_tick": fall,
        "escape_tick": escape,
        "closed": closed,
        "axis_crossings": crossings,
        "observed_periods": periods,
        "euclid_min": min(distances) if distances else None,
        "euclid_max": max(distances) if distances else None,
        "l1_min": min(l1s) if l1s else None,
        "l1_max": max(l1s) if l1s else None,
        "ticks_moving": len(moving),
        "ticks_pushed": len(pushed),
        "pushes": sum(r["pushes"] for r in moving),
        "push_sum": tuple(sum(r["push"][axis] for r in moving) for axis in range(3)),
        "ledger_ticks_balanced": sum(1 for line in audit if line.get("balanced")),
        "ledger_ticks": len(audit),
        "conserved": result["metadata"].get("conserved_at_every_completed_tick"),
        "accounting": result["metadata"].get("accounting_balanced_at_every_completed_tick"),
        "final_totals": result["metadata"].get("final_totals"),
        "escaped_totals": result["metadata"].get("escaped_totals"),
        "sink_totals": result["metadata"].get("external_body_totals"),
        "body_momentum": result["metadata"].get("external_body_momentum"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="run.json or the directory that holds it")
    parser.add_argument("--family", default="electron", help="the orbiting family")
    parser.add_argument("--json", action="store_true", help="print the rows and the verdict as JSON")
    args = parser.parse_args()
    directory = args.run if args.run.is_dir() else args.run.parent
    result = table(directory, args.family)
    summary = verdict(result)
    if args.json:
        print(json.dumps({"rows": result["rows"], "verdict": summary}, default=list))
        return
    print(f"nucleus at {result['nucleus']}, launcher at {result['launcher']}")
    print("tick position offset L1 euclid register pushes push_sum sink body_momentum")
    for r in result["rows"]:
        print(
            f"{r['tick']:4d} {r['position']} {r['offset']} {r['l1']:2d} {r['euclid']:6.2f} "
            f"{r['register']} {r['pushes']:2d} {r['push']} {r['sink']:5d} {r['body_momentum']}"
        )
    for key, value in summary.items():
        print(f"{key}: {value}")
    what = (
        "closed orbit"
        if summary["closed"]
        else "fall"
        if summary["fall_tick"] is not None
        else "escape"
        if summary["escape_tick"] is not None
        else "circulating, not closed"
        if len(summary["axis_crossings"]) > 1
        else "no full circuit"
    )
    print(f"verdict: {what}")


if __name__ == "__main__":
    main()
