"""H-Angular-Momentum-In-The-Clicks-1: the angular momentum read in the clicks alone (a reader over the record's log, integers only, no act).

For every credit line the moment (r - c) x dP_take of the take's momentum about the centre c at the credited Node; for every
birth line the moment of its take at the take's Node and the moment of the children's lay (dP_lay, the one vector the line
carries) booked at the same Node; the spin part the senses (the credit's sense, the two children's senses), summed.
With no centre the moment is about the board's centre in doubled coordinates R = 2 r - (cube - 1), an integer (am2's L2);
with a centre c the arm is r - c. Per close (interval) and over the record.
Usage: python moment_of_clicks.py <record.json> [<out.json>]"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from typing import Any

EPS = {0: (1, 2), 1: (2, 0), 2: (0, 1)}  # (c, a, b) with eps_cab = +1


def cross(r: list[int], p: list[int]) -> list[int]:
    return [r[a] * p[b] - r[b] * p[a] for (a, b) in (EPS[0], EPS[1], EPS[2])]


def add(x: list[int], y: list[int]) -> list[int]:
    return [u + v for u, v in zip(x, y, strict=True)]


def arm(node: list[int], cube: int, centre: list[int] | None) -> list[int]:
    if centre is None:
        return [2 * x - (cube - 1) for x in node]
    return [x - c for x, c in zip(node, centre, strict=True)]


def moment_of_clicks(record: Any, centre: list[int] | None = None) -> dict[str, Any]:
    """The clicks' J: the orbital part per close and summed (the takes', the lays'), the senses summed, the counts."""
    log = record.log if hasattr(record, "log") else record["log"]
    cube = int(record.cube if hasattr(record, "cube") else record["cube"])
    per: dict[int, dict[str, list[int]]] = defaultdict(lambda: {"take": [0, 0, 0], "lay": [0, 0, 0]})
    senses_credits, senses_births, counts = 0, 0, defaultdict(int)
    for e in log:
        if e["event"] == "credit":
            r = arm(e["node"], cube, centre)
            per[int(e["i"])]["take"] = add(per[int(e["i"])]["take"], cross(r, e["dP_take"]))
            senses_credits += int(e["sense"])
            counts["credits"] += 1
            counts["credits laid back"] += "laid_back" in e
        elif e["event"] == "birth":
            r = arm(e["node"], cube, centre)
            per[int(e["i"])]["take"] = add(per[int(e["i"])]["take"], cross(r, e["dP_take"]))
            per[int(e["i"])]["lay"] = add(per[int(e["i"])]["lay"], cross(r, e["dP_lay"]))
            senses_births += sum(int(s) for s in e["senses"])
            counts["births"] += 1
            counts["births with dP_lay not 0"] += any(e["dP_lay"])
            counts["births with a child on standing light"] += any(any(s) for s in e.get("stood", []))
    total_take, total_lay = [0, 0, 0], [0, 0, 0]
    closes = {}
    for i in sorted(per):
        t, l = per[i]["take"], per[i]["lay"]
        total_take, total_lay = add(total_take, t), add(total_lay, l)
        closes[i] = {"J_take": t, "J_lay": l, "J": add(t, l)}
    return {
        "cube": cube,
        "centre": centre if centre is not None else "the board's centre, doubled coordinates",
        "counts": dict(counts),
        "closes with a click": len(closes),
        "closes with J not 0": sum(1 for v in closes.values() if any(v["J"])),
        "J_take summed": total_take,
        "J_lay summed": total_lay,
        "J summed": add(total_take, total_lay),
        "J max abs over the closes": max((max(abs(x) for x in v["J"]) for v in closes.values()), default=0),
        "senses summed over the credits": senses_credits,
        "senses summed over the births' children": senses_births,
        "per close": closes,
    }


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as f:
        record = json.load(f)
    found = moment_of_clicks(record)
    found["record"] = argv[1]
    shown = {k: v for k, v in found.items() if k != "per close"}
    print(json.dumps(shown))
    if len(argv) > 2:
        with open(argv[2], "w", encoding="utf-8") as f:
            json.dump(found, f)


if __name__ == "__main__":
    main(sys.argv)
