"""The quartet children read from a record's log (H-Quartet-Children-2; the Bell part re-cut from H-Setting-From-The-Frame-2/bell_setting.py): the births by row, the quartet children's axis at the birth from the levels laid (the spin density N.G Gamma_a.N in the law's integers, its sign along the born Link's axis against the sense, the pair's two axes summed), the axis along the track (every credit of the quartet row inside the child's cone, nearest to that child: the sign along the birth's axis kept or not), and Bell's S over the quartet pairs with the outcome the sign of the child's axis projected on the click's Link (the arrival Link, the twin Link) and the setting the detector's own datum, the sense as the control. Integers only. Usage: python quartet_reader.py <record.json> [...]"""

from __future__ import annotations

import json
import sys
from math import lcm
from typing import Any

from event_universe.core.ports import AXES, PORT_SIDES
from event_universe.quartet import quartet

sys.set_int_max_str_digits(0)
Q = quartet()


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def mm(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def quad(m: list[list[int]], u: list[int]) -> int:
    return sum(u[i] * m[i][j] * u[j] for i in range(len(u)) for j in range(len(u)))


GG = [mm(Q.G, g) for g in Q.gamma]
GJ = mm(Q.G, Q.J)


def density(nows: list[int]) -> list[int]:
    return [quad(m, nows) for m in GG]


def charge(nows: list[int], befores: list[int]) -> int:
    return sum(befores[i] * GJ[i][j] * nows[j] for i in range(len(nows)) for j in range(len(nows)))


def torus(cube: int, a: list[int], b: list[int]) -> int:
    return sum(min((x - y) % cube, (y - x) % cube) for x, y in zip(a, b, strict=True))


def axis_of(minus: list[int], plus: list[int]) -> int:
    return next(a for a in range(AXES) if minus[a] != plus[a])


def quartet_index(record: dict[str, Any]) -> int | None:
    """The quartet's index among the records in the acts' order (rows.rows_of: the records writing nothing in the file's order, then the emitter, which writes its one line)."""
    den = int(record["universe"]["integers"]["den"])
    rows = [r for r in record["universe"]["rows"] if int(r["shape"]) in (2, 8)]
    gapped = [r for r in rows if [int(x) for x in r["pair"]] != [den, den]]
    found = [k for k, r in enumerate(gapped) if int(r["shape"]) == 8]
    return found[0] if found else None


def index_of(cube: int, at: list[int]) -> int:
    return at[0] * cube * cube + at[1] * cube + at[2]


def neighbour_index(cube: int, at: list[int], port: int) -> int:
    axis, side = PORT_SIDES[port]
    return index_of(cube, [(at[a] + (side if a == axis else 0)) % cube for a in range(AXES)])


def port_toward(cube: int, at: list[int], other: list[int]) -> int | None:
    found = None
    for port, (axis, side) in enumerate(PORT_SIDES):
        target = [(at[a] + (side if a == axis else 0)) % cube for a in range(AXES)]
        if target == list(other):
            found = port
    return found


def inflows(record: dict[str, Any], credit: dict[str, Any]) -> list[int] | None:
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


def projected(axial: list[int], port: int | None) -> int:
    """The sign of the child's axis projected on the Link of the Port (the axis's component times the Port's side), 0 with no Port."""
    if port is None:
        return 0
    axis, side = PORT_SIDES[port]
    return sign(axial[axis] * side)


def end_data(record: dict[str, Any], credit: dict[str, Any], twin: list[int], laid: int) -> dict[str, Any]:
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
    axial = [int(x) for x in f["axial"]]
    return {
        "i": int(credit["i"]),
        "node": list(credit["node"]),
        "axial": axial,
        "outcomes": {
            "axis_on_arrival": projected(axial, arrival),
            "axis_on_twin": projected(axial, toward),
            "sense": int(credit["sense"]),
            "laid": laid,
        },
        "settings": {
            "turned": 1 if credit["turned"] else 0,
            "take_dir": None if before == now_was else (1 if before > now_was else 0),
            "arrival_side": None if arrival is None else (1 if PORT_SIDES[arrival][1] > 0 else 0),
            "arrival_axis_is_twin": None if arrival is None or toward is None else (1 if arrival == toward else 0),
            "proper_parity": int(credit["proper"]) % 2,
            "sign_level": None if credit["sign_level"] == 0 else (1 if credit["sign_level"] > 0 else 0),
            "taken_line": int(credit["taken_line"]),
        },
        "twin_one_link_away": toward is not None,
    }


def chsh(pairs: list[dict[str, Any]], outcome: str, setting: str) -> dict[str, Any]:
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
            labellings[f"a={a0} b={b0}"] = {"S": [num, den], "S^2": [num2, d2], "band": band}
    return {
        "outcome": outcome,
        "setting": setting,
        "pairs used": agree + differ,
        "dropped": dropped,
        "settings agree / differ": [agree, differ],
        "cells (- end, + end): [n, same, opposite]": {f"{x}{y}": v for (x, y), v in cells.items()},
        "labellings": labellings,
    }


def read(path: str) -> dict[str, Any]:
    record = json.load(open(path, encoding="utf-8"))
    cube, qi = int(record["cube"]), quartet_index(record)
    log = record["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    by_row: dict[int, int] = {}
    for b in births:
        by_row[int(b["line_pair"])] = by_row.get(int(b["line_pair"]), 0) + 1
    out: dict[str, Any] = {
        "record": path,
        "cube": cube,
        "intervals": int(record["intervals"]),
        "run_back": record.get("run_back"),
        "quartet row index among the records": qi,
        "births by children's row": {str(k): v for k, v in sorted(by_row.items())},
        "credits by row": {},
        "A B T": [int(record["counts"].get("A", 0)) if "A" in record["counts"] else None],
    }
    for c in credits:
        out["credits by row"][str(c["line"])] = out["credits by row"].get(str(c["line"]), 0) + 1
    if qi is None:
        return out
    qb = [b for b in births if int(b["line_pair"]) == qi]
    qc = [c for c in credits if int(c["line"]) == qi]
    children: list[dict[str, Any]] = []
    birth_rows = []
    for b in qb:
        axis = axis_of(b["minus"], b["plus"])
        levels = b.get("levels_laid")
        ends = []
        for k, (where, sense) in enumerate(((b["minus"], -1), (b["plus"], 1))):
            nows, befores = [int(x) for x in levels[k][0::2]], [int(x) for x in levels[k][1::2]]
            dens, w = density(nows), charge(nows, befores)
            ends.append({"sense": sense, "node": where, "density": dens, "W": w, "W_logged": int(b["W_children"][k]),
                         "sign along axis equals sense": sign(dens[axis]) == sense,
                         "other axes zero": all(dens[a] == 0 for a in range(AXES) if a != axis)})
            children.append({"birth_i": int(b["i"]), "node": list(where), "sense": sense, "axis": axis, "birth_density": dens, "W": w, "credits": []})
        birth_rows.append({"i": int(b["i"]), "take node": b["node"], "axis": axis, "minus": ends[0], "plus": ends[1],
                           "pair density sum": [x + y for x, y in zip(ends[0]["density"], ends[1]["density"], strict=True)],
                           "pair W sum": ends[0]["W"] + ends[1]["W"], "amplitude": b["amplitude"], "content": b["content"]})
    for c in qc:
        i, at = int(c["i"]), c["node"]
        near = []
        for ch in children:
            d = torus(cube, at, ch["node"])
            if i > ch["birth_i"] and d <= i - ch["birth_i"]:
                near.append((d, ch))
        if not near:
            continue
        least = min(d for d, _ in near)
        for d, ch in near:
            if d == least:
                axial = [int(x) for x in c["frame"]["axial"]]
                ch["credits"].append({"i": i, "node": at, "distance": d, "axial": axial, "W": int(c["frame"]["W"]), "sense": int(c["sense"]),
                                      "kept": sign(axial[ch["axis"]]) == ch["sense"], "dominant axis": max(range(AXES), key=lambda a: abs(axial[a]))})
    kept = sum(cr["kept"] for ch in children for cr in ch["credits"])
    total = sum(len(ch["credits"]) for ch in children)
    first_kept = sum(ch["credits"][0]["kept"] for ch in children if ch["credits"])
    first_total = sum(1 for ch in children if ch["credits"])
    own_node = [(ch, next((cr for cr in ch["credits"] if cr["node"] == ch["node"]), None)) for ch in children]
    own_kept = sum(cr["kept"] for _ch, cr in own_node if cr is not None)
    own_total = sum(1 for _ch, cr in own_node if cr is not None)
    out.update({
        "quartet births": len(qb),
        "quartet credits": len(qc),
        "births": birth_rows,
        "axis at birth: sign along the born axis equals the sense": [sum(1 for r in birth_rows for e in (r["minus"], r["plus"]) if e["sign along axis equals sense"]), 2 * len(qb)],
        "axis at birth: other axes zero": [sum(1 for r in birth_rows for e in (r["minus"], r["plus"]) if e["other axes zero"]), 2 * len(qb)],
        "pair density summing 0": [sum(1 for r in birth_rows if all(x == 0 for x in r["pair density sum"])), len(qb)],
        "pair W summing 0": [sum(1 for r in birth_rows if r["pair W sum"] == 0), len(qb)],
        "W logged equals W of the levels": [sum(1 for r in birth_rows for e in (r["minus"], r["plus"]) if e["W"] == e["W_logged"]), 2 * len(qb)],
        "axis carried, all credits in the cone nearest the child: kept N of M": [kept, total],
        "axis carried at the first credit: kept N of M": [first_kept, first_total],
        "axis carried at the child's own Node: kept N of M": [own_kept, own_total],
        "children with a credit": [first_total, len(children)],
        "children": children,
    })
    # Bell over the quartet pairs: each end's first credit at its own Node on the quartet row
    pairs = []
    for b in qb:
        ends = []
        for where, laid in ((b["minus"], -1), (b["plus"], 1)):
            first = next((c for c in qc if c["node"] == where and int(c["i"]) > int(b["i"])), None)
            ends.append(None if first is None else (first, laid))
        if ends[0] is None or ends[1] is None:
            continue
        pairs.append({"birth_i": int(b["i"]), "minus": end_data(record, ends[0][0], b["plus"], -1), "plus": end_data(record, ends[1][0], b["minus"], 1)})
    out["bell"] = {
        "pairs clicked at both ends (own Node)": len(pairs),
        "twin one Link away at both ends": sum(p["minus"]["twin_one_link_away"] and p["plus"]["twin_one_link_away"] for p in pairs),
        "readings": [chsh(pairs, o, s) for o in ("axis_on_arrival", "axis_on_twin", "sense") for s in ("turned", "take_dir", "arrival_side", "arrival_axis_is_twin", "proper_parity", "sign_level", "taken_line")],
        "pairs": pairs,
    }
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(read(p)))
