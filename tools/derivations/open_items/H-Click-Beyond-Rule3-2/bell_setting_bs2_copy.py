"""Bell's S with the setting read from the detector's own click (H-Setting-From-The-Frame-2): a reader of the record's log and Node lines alone, no act, no flag, integers only.

For every birth the two ends (the - child's Node and the + child's Node) and each end's first credit after the birth at that Node on the children's plane (the reader's rule of predicates.bell on reader-5). At each end the OUTCOME is read as the law gives it (the credit's sense, the sign of the plane's Wronskian at the detector Node after its click; beside it the laid sense -1 / +1 and the take's direction), and the SETTING is one two-valued datum of the detector Node at its click, set by its own past: the reversal's record (the credit's turned bit), the take's direction on the slot (the taker's before above or below its now), the side of the plane's re and im levels at the click (the beat's crossing side), the frame sign of the Link toward the twin, the Link of the six the taken light arrives on (the gap-0 current's largest inflow at the interval's start, from the record's Node lines: its side, and whether it is the Link toward the twin), the proper clock's parity, the sign level's sign, the taken line. Never a digit of the reader.

S = E(a, b) - E(a, b') + E(a', b) + E(a', b') with E(x, y) = (same - opposite) / n over the pairs whose - end read x and + end read y: the four cells partition the pairs (each pair has one setting per end), S = num / den with den the least common multiple of the four counts, S^2 against 4 and 8 as 4 den^2 < num^2 <= 8 den^2 (nature's band), num^2 = 4 den^2 (the local bound), below. The four labellings (which value of each end is called a or a', b or b') are all read; the setting's agreement through the root is the count of pairs whose two ends' settings are equal against the pairs whose settings differ.

Usage: python bell_setting.py <record.json> [<record.json> ...]
"""

from __future__ import annotations

import json
import sys
from math import lcm
from typing import Any

from event_universe.core.ports import AXES, PORT_SIDES, PORTS

sys.set_int_max_str_digits(0)

OUTCOMES = ("sense", "laid", "take_dir")
SETTINGS = (
    "turned",
    "take_dir",
    "re_side",
    "im_side",
    "link_frame",
    "arrival_side",
    "arrival_twin",
    "proper_parity",
    "sign_level",
    "taken_line",
)


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def port_toward(cube: int, at: list[int], other: list[int]) -> int | None:
    """The Port of `at` whose Link reaches `other` on the torus, None unless `other` is one Link away."""
    found = None
    for port, (axis, side) in enumerate(PORT_SIDES):
        target = [(at[a] + (side if a == axis else 0)) % cube for a in range(AXES)]
        if target == list(other):
            found = port
    return found


def index_of(cube: int, at: list[int]) -> int:
    return at[0] * cube * cube + at[1] * cube + at[2]


def neighbour_index(cube: int, at: list[int], port: int) -> int:
    axis, side = PORT_SIDES[port]
    return index_of(cube, [(at[a] + (side if a == axis else 0)) % cube for a in range(AXES)])


def inflows(record: dict[str, Any], credit: dict[str, Any]) -> list[int] | None:
    """The gap-0 line's current flowing into the credit's Node on each of its six Links at the interval's start (the Node line of the interval before: F from the Node along +a is the line's `current`; into the Node on +a is -F_(i, i+a), on -a it is +F_(i-a, i))."""
    i, cube = int(credit["i"]), int(record["cube"])
    if i < 2:
        return None
    line = record["nodes"][i - 2]
    assert int(line["i"]) == i - 1
    at = credit["node"]
    found = []
    for port, (axis, side) in enumerate(PORT_SIDES):
        if side == 1:
            found.append(-int(line["current"][axis][index_of(cube, at)]))
        else:
            found.append(int(line["current"][axis][neighbour_index(cube, at, port)]))
    return found


def end_data(record: dict[str, Any], credit: dict[str, Any], twin: list[int], laid: int) -> dict[str, Any]:
    """One end's outcomes and settings at its click."""
    f = credit["frame"]
    now_was, before, _levels = credit["taker"]
    cube = int(record["cube"])
    toward = port_toward(cube, credit["node"], twin)
    flows = inflows(record, credit)
    arrival = None
    if flows is not None:
        top = max(flows)
        if top > 0 and flows.count(top) == 1:
            arrival = flows.index(top)
    return {
        "i": int(credit["i"]),
        "node": list(credit["node"]),
        "taker": list(credit["taker"]),
        "inflows": flows,
        "outcomes": {
            "sense": int(credit["sense"]),
            "laid": laid,
            "take_dir": sign(before - now_was),
        },
        "settings": {
            "turned": 1 if credit["turned"] else 0,
            "take_dir": None if before == now_was else (1 if before > now_was else 0),
            "re_side": None if f["re_now"] == 0 else (1 if f["re_now"] > 0 else 0),
            "im_side": None if f["im_now"] == 0 else (1 if f["im_now"] > 0 else 0),
            "link_frame": None if toward is None else (1 if f["frames"][toward] > 0 else 0),
            "arrival_side": None if arrival is None else (1 if PORT_SIDES[arrival][1] > 0 else 0),
            "arrival_twin": None if arrival is None or toward is None else (1 if arrival == toward else 0),
            "proper_parity": int(credit["proper"]) % 2,
            "sign_level": None if credit["sign_level"] == 0 else (1 if credit["sign_level"] > 0 else 0),
            "taken_line": int(credit["taken_line"]),
        },
        "twin_one_link_away": toward is not None,
    }


def pairs_of(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Every born pair clicked at both ends: the - end's and the + end's data at their first credits after the birth."""
    log = record["log"]
    credits = [e for e in log if e["event"] == "credit"]
    births = [e for e in log if e["event"] == "birth"]
    found = []
    for b in births:
        ends = []
        for where, laid in ((b["minus"], -1), (b["plus"], 1)):
            first = next(
                (
                    c
                    for c in credits
                    if c["node"] == where
                    and int(c["line"]) == int(b["line_pair"])
                    and int(c["i"]) > int(b["i"])
                    and "re_now" in c["frame"]
                ),
                None,
            )
            ends.append(None if first is None else (first, laid))
        if ends[0] is None or ends[1] is None:
            continue
        found.append(
            {
                "birth_i": int(b["i"]),
                "minus": end_data(record, ends[0][0], b["plus"], -1),
                "plus": end_data(record, ends[1][0], b["minus"], 1),
            }
        )
    return found


def chsh(pairs: list[dict[str, Any]], outcome: str, setting: str) -> dict[str, Any]:
    """The four cells' counts and S under the four labellings, integers only."""
    cells: dict[tuple[int, int], list[int]] = {(x, y): [0, 0, 0] for x in (0, 1) for y in (0, 1)}
    agree = differ = dropped = 0
    for p in pairs:
        a, b = p["minus"]["settings"][setting], p["plus"]["settings"][setting]
        oa, ob = p["minus"]["outcomes"][outcome], p["plus"]["outcomes"][outcome]
        if a is None or b is None or oa == 0 or ob == 0:
            dropped += 1
            continue
        agree += a == b
        differ += a != b
        cell = cells[(a, b)]
        cell[0] += 1
        cell[1 if oa * ob > 0 else 2] += 1
    used = agree + differ
    labellings = {}
    for swap_a in (0, 1):
        for swap_b in (0, 1):
            a0, a1 = (0, 1) if swap_a == 0 else (1, 0)
            b0, b1 = (0, 1) if swap_b == 0 else (1, 0)
            terms = [(a0, b0, 1), (a0, b1, -1), (a1, b0, 1), (a1, b1, 1)]
            if any(cells[(x, y)][0] == 0 for x, y, _s in terms):
                labellings[f"a={a0} b={b0}"] = {"S": None, "empty cell": True}
                continue
            den = 1
            for x, y, _s in terms:
                den = lcm(den, cells[(x, y)][0])
            num = 0
            for x, y, s in terms:
                n, same, opp = cells[(x, y)]
                num += s * (same - opp) * (den // n)
            num2, d2 = num * num, den * den
            band = (
                "in nature's band 4 < S^2 <= 8"
                if 4 * d2 < num2 <= 8 * d2
                else "at the local bound S^2 = 4"
                if num2 == 4 * d2
                else "below the local bound S^2 < 4"
                if num2 < 4 * d2
                else "above nature's band S^2 > 8"
            )
            labellings[f"a={a0} b={b0}"] = {
                "S": [num, den],
                "S^2": [num2, d2],
                "band": band,
            }
    return {
        "outcome": outcome,
        "setting": setting,
        "pairs used": used,
        "pairs dropped (a setting or an outcome undefined)": dropped,
        "settings agree / differ through the root": [agree, differ],
        "cells (- end, + end): [n, same, opposite]": {f"{x}{y}": v for (x, y), v in cells.items()},
        "labellings": labellings,
    }


def read(path: str) -> dict[str, Any]:
    record = json.load(open(path, encoding="utf-8"))
    pairs = pairs_of(record)
    births = sum(1 for e in record["log"] if e["event"] == "birth")
    credits = sum(1 for e in record["log"] if e["event"] == "credit")
    sense_equals_laid = [
        sum(p[end]["outcomes"]["sense"] == p[end]["outcomes"]["laid"] for p in pairs) for end in ("minus", "plus")
    ]
    sense_zero = sum(p[end]["outcomes"]["sense"] == 0 for p in pairs for end in ("minus", "plus"))
    one_link = sum(p["minus"]["twin_one_link_away"] and p["plus"]["twin_one_link_away"] for p in pairs)
    same_interval = sum(p["minus"]["i"] == p["plus"]["i"] for p in pairs)
    out: dict[str, Any] = {
        "record": path,
        "intervals": int(record["intervals"]),
        "cube": int(record["cube"]),
        "births": births,
        "credits": credits,
        "pairs clicked at both ends": len(pairs),
        "twin one Link away at both ends": one_link,
        "the two ends clicking in one interval": same_interval,
        "credit's sense equal to the laid sense (- end, + end)": sense_equals_laid,
        "credit's sense 0 (ends)": sense_zero,
        "run_back": record.get("run_back"),
        "readings": [],
    }
    for outcome in OUTCOMES:
        for setting in SETTINGS:
            if outcome == setting:
                continue
            out["readings"].append(chsh(pairs, outcome, setting))
    return out


def main(argv: list[str]) -> None:
    for path in argv[1:]:
        found = read(path)
        print(json.dumps(found))


if __name__ == "__main__":
    main(sys.argv)
