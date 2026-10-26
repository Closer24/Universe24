"""The helicity from the twist (H-Helicity-From-The-Twist-2): a reader of the record's log and Node lines alone; no act, no flag, integers only.

The twist of a Link from its lower end k along +a (links.row_twist): h(k, a) = cross(u_b(k), u_c(k), u_b(k + a), u_c(k + a)) with
(b, c) = (a + 1, a - 1) mod 3 and u_b(k) = F(k, k - b) - F(k, k + b) the net transverse current of the gap-0 line, F(k, k + b) the
Node line's `current[b][k]` of the interval before (the state at the interval's start; the line i - 1 for an event at i). The
helicity vector of a Link is H = h e_a along +a from the lower end (a pseudo-vector of the oriented Link: the same object read
from either end since h and e both flip). The helicity scalar along an arm d is sign(H . d).

(1) The reading at the birth: the born Link, its lower end, h from the Node line, checked against the log's own orientation (the
take's Node is the end the current flows into; the + child's end is `into` where h > 0, the other end where h < 0: close.meet).
(2) The carriage: each child's credits (its plane at its Node after the birth: the first one, the Bell pair's rule; every one
until the next birth of the plane at that Node; and every credit of the plane within the one-Link cone of the child), at each
the click's Link (the arrival Link: the gap-0 inflow's largest Port; and the Link toward the twin) with its twist's sign:
the vector kept (the same axis and the same sign), the scalar along the arm kept (the arrival's inward direction against the
child's own arm at the birth, from the twin to the child).
(3) Bell with the axis: the outcome at an end sign(a_c . a_d) under the readings of a_c (the birth's H; the twin Link's twist at
the credit) and a_d (the arrival Link's twist; the twin Link's twist), the setting the detector's own datum (bs2's list), the four
cells, S = [num, den] with its quotient and remainder, S^2 against 4 den^2 and 8 den^2, under the four labellings.
(4) The twist's unit: |h| at the births against (T div 2)^2 and T^2 as a quotient with its remainder, and the gcd over the births.

Usage: python helicity_reader.py <record.json> <out.json>
"""

from __future__ import annotations

import json
import sys
from math import gcd, lcm
from typing import Any

sys.set_int_max_str_digits(0)

AXES = 3
PORT_SIDES = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]
SETTINGS = ("arrival_side", "arrival_twin", "arrival_axis_is_birth_axis", "taken_line", "turned", "link_frame", "phase_half", "proper_parity")


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def cross(xi: int, yi: int, xj: int, yj: int) -> int:
    return xi * yj - yi * xj


class Board:
    def __init__(self, record: dict[str, Any]) -> None:
        self.cube = int(record["cube"])
        self.lines = {int(line["i"]): line for line in record["nodes"]}

    def index(self, at: list[int]) -> int:
        c = self.cube
        return at[0] * c * c + at[1] * c + at[2]

    def shift(self, at: list[int], axis: int, step: int) -> list[int]:
        found = list(at)
        found[axis] = (found[axis] + step) % self.cube
        return found

    def start_line(self, i: int) -> dict[str, Any] | None:
        return self.lines.get(i - 1)

    def flow(self, line: dict[str, Any], k: list[int], axis: int) -> int:
        """F(k, k + a) of the gap-0 line."""
        return int(line["current"][axis][self.index(k)])

    def net(self, line: dict[str, Any], k: list[int], b: int) -> int:
        """u_b(k) = F(k, k - b) - F(k, k + b); F(k, k - b) = -F(k - b, k)."""
        return -self.flow(line, self.shift(k, b, -1), b) - self.flow(line, k, b)

    def twist(self, line: dict[str, Any], k: list[int], a: int) -> int:
        b, c = (a + 1) % AXES, (a - 1) % AXES
        j = self.shift(k, a, 1)
        return cross(self.net(line, k, b), self.net(line, k, c), self.net(line, j, b), self.net(line, j, c))

    def inflows(self, line: dict[str, Any], at: list[int]) -> list[int]:
        found = []
        for axis, side in PORT_SIDES:
            if side == 1:
                found.append(-self.flow(line, at, axis))
            else:
                found.append(self.flow(line, self.shift(at, axis, -1), axis))
        return found

    def link_of(self, at: list[int], port: int) -> tuple[list[int], int]:
        """The Link at a Node's Port as (its lower end, its axis)."""
        axis, side = PORT_SIDES[port]
        return (at if side == 1 else self.shift(at, axis, -1)), axis

    def port_toward(self, at: list[int], other: list[int]) -> int | None:
        for port, (axis, side) in enumerate(PORT_SIDES):
            if self.shift(at, axis, side) == list(other):
                return port
        return None

    def distance(self, a: list[int], b: list[int]) -> int:
        c = self.cube
        return sum(min((a[x] - b[x]) % c, (b[x] - a[x]) % c) for x in range(AXES))

    def link_between(self, p: list[int], q: list[int]) -> tuple[list[int], int] | None:
        """The Link joining two Nodes as (its lower end, its axis), None unless one Link apart."""
        port = self.port_toward(p, q)
        if port is None:
            return None
        return self.link_of(p, port)


def emitter_index(record: dict[str, Any]) -> int:
    """The emitter's index among the records (the log's `taken_row` counts node.records(): the record's `planes` key lists their nums in that order; the emitter's num is den)."""
    den = int(record["den"])
    return [int(x) for x in record["planes"]].index(den)


def read_births(record: dict[str, Any], board: Board, gap0: int) -> list[dict[str, Any]]:
    found = []
    for b in record["log"]:
        if b["event"] != "birth":
            continue
        i = int(b["i"])
        minus, plus, node = list(b["minus"]), list(b["plus"]), list(b["node"])
        link = board.link_between(minus, plus)
        entry: dict[str, Any] = {"i": i, "node": node, "minus": minus, "plus": plus, "line_pair": int(b["line_pair"]), "taken_row": int(b["taken_row"])}
        if link is None:
            entry["readable"] = "ends not one Link apart"
            found.append(entry)
            continue
        k, a = link
        j = board.shift(k, a, 1)
        h_log = 1 if plus == node else -1
        entry.update({"lower": k, "axis": a, "h_log": h_log})
        line = board.start_line(i)
        if line is None or int(b["taken_row"]) != gap0:
            entry["readable"] = "no Node line" if line is None else "the taken row is not the gap-0 row (its current is not in the Node line)"
            entry["h_sign"] = h_log
            entry["h_from"] = "log"
        else:
            flow = board.flow(line, k, a)
            h = board.twist(line, k, a)
            into = j if flow > 0 else k
            entry.update(
                {
                    "readable": "state",
                    "flow": flow,
                    "h": h,
                    "h_sign": sign(h),
                    "h_from": "Node line",
                    "into_matches_log": into == node,
                    "h_sign_matches_log": sign(h) == h_log,
                    "rest": flow == 0,
                }
            )
        # the children's arms: from the twin to the child; the child at the upper end j has the arm +a
        entry["arm"] = {"minus": 1 if minus == j else -1, "plus": 1 if plus == j else -1}
        entry["lambda"] = {end: entry["h_sign"] * entry["arm"][end] for end in ("minus", "plus")}
        found.append(entry)
    return found


def link_integer(births: list[dict[str, Any]], lower: list[int], axis: int, before: int) -> int | None:
    """hd2's integer per Link read from the log alone: the sign of the twist at the last birth on this Link at an interval before `before` (None where no birth crossed it); its dynamics is a write at the birth and nothing else, so the reading needs no flag."""
    last = None
    for b in births:
        if "axis" in b and b["lower"] == lower and b["axis"] == axis and b["i"] < before:
            if last is None or b["i"] > last["i"]:
                last = b
    return None if last is None else last["h_sign"]


def click_links(board: Board, line: dict[str, Any] | None, at: list[int], twin: list[int]) -> dict[str, Any]:
    """The click's Links at a credit: the arrival Link (the largest unique positive inflow) and the Link toward the twin, each with its twist's vector (axis, sign) and the inward direction along +axis."""
    out: dict[str, Any] = {"arrival": None, "twin": None}
    if line is None:
        return out
    flows = board.inflows(line, at)
    top = max(flows)
    if top > 0 and flows.count(top) == 1:
        port = flows.index(top)
        k, a = board.link_of(at, port)
        h = board.twist(line, k, a)
        out["arrival"] = {"port": port, "axis": a, "h": h, "h_sign": sign(h), "inward": -PORT_SIDES[port][1], "side": PORT_SIDES[port][1]}
    port = board.port_toward(at, twin)
    if port is not None:
        k, a = board.link_of(at, port)
        h = board.twist(line, k, a)
        out["twin"] = {"port": port, "axis": a, "h": h, "h_sign": sign(h), "inward": -PORT_SIDES[port][1], "side": PORT_SIDES[port][1]}
    out["inflows"] = flows
    return out


def tracks(record: dict[str, Any], board: Board, births: list[dict[str, Any]]) -> list[dict[str, Any]]:
    credits = [e for e in record["log"] if e["event"] == "credit"]
    births_raw = [e for e in record["log"] if e["event"] == "birth"]
    found = []
    for b in births:
        if "axis" not in b:
            continue
        s, i0 = b["line_pair"], b["i"]
        for end in ("minus", "plus"):
            at, twin = b[end], b["plus" if end == "minus" else "minus"]
            next_birth = min(
                (int(x["i"]) for x in births_raw if int(x["line_pair"]) == s and int(x["i"]) > i0 and (list(x["minus"]) == at or list(x["plus"]) == at)),
                default=None,
            )
            own = [c for c in credits if list(c["node"]) == at and int(c["line"]) == s and int(c["i"]) > i0 and "re_now" in c["frame"]]
            until = [c for c in own if next_birth is None or int(c["i"]) < next_birth]
            cone = [c for c in credits if int(c["line"]) == s and int(c["i"]) > i0 and "re_now" in c["frame"] and board.distance(list(c["node"]), at) <= int(c["i"]) - i0]
            track = {"birth_i": i0, "end": end, "node": at, "line_pair": s, "H_birth": [b["axis"], b["h_sign"]], "lambda_birth": b["lambda"][end], "credits": {}}
            for name, group in (("first", own[:1]), ("own_until_next_birth", until), ("cone", cone)):
                rows = []
                for c in group:
                    line = board.start_line(int(c["i"]))
                    links = click_links(board, line, list(c["node"]), twin)
                    row: dict[str, Any] = {"i": int(c["i"]), "node": list(c["node"]), "sense": int(c["sense"])}
                    for which in ("arrival", "twin"):
                        L = links[which]
                        if L is None:
                            row[which] = None
                            continue
                        same_axis = L["axis"] == b["axis"]
                        integer = link_integer(births, board.link_of(list(c["node"]), L["port"])[0], L["axis"], int(c["i"]))
                        row[which] = {
                            "integer": integer,
                            "integer_kept": integer is not None and same_axis and integer == b["h_sign"],
                            "axis": L["axis"],
                            "h_sign": L["h_sign"],
                            "h_zero": L["h"] == 0,
                            "vector_kept": same_axis and L["h_sign"] == b["h_sign"],
                            "same_axis": same_axis,
                            "lambda": L["h_sign"] * L["inward"],
                            "scalar_kept": L["h_sign"] * L["inward"] == b["lambda"][end],
                        }
                    rows.append(row)
                track["credits"][name] = rows
            found.append(track)
    return found


def carriage_counts(tr: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for group in ("first", "own_until_next_birth", "cone"):
        for which in ("arrival", "twin"):
            n = kept_v = kept_s = same_axis = zero = defined = kept_i = with_i = 0
            for t in tr:
                for row in t["credits"][group]:
                    n += 1
                    L = row[which]
                    if L is None:
                        continue
                    defined += 1
                    zero += L["h_zero"]
                    same_axis += L["same_axis"]
                    kept_v += L["vector_kept"]
                    kept_s += L["scalar_kept"]
                    with_i += L["integer"] is not None
                    kept_i += L["integer_kept"]
            out[f"{group}/{which}"] = {"credits": n, "link defined": defined, "twist 0": zero, "same axis as the birth Link": same_axis, "vector kept (axis and sign)": kept_v, "scalar kept (along the arm)": kept_s, "hd2 integer on the Link (a birth crossed it)": with_i, "hd2 integer equal to the birth's (axis and sign)": kept_i}
    return out


def end_settings(board: Board, record: dict[str, Any], c: dict[str, Any], twin: list[int], b: dict[str, Any]) -> dict[str, Any]:
    line = board.start_line(int(c["i"]))
    links = click_links(board, line, list(c["node"]), twin)
    f = c["frame"]
    arr, tw = links["arrival"], links["twin"]
    port = board.port_toward(list(c["node"]), twin)
    ss = None if port is None else int(f["phases"][port][1])
    return {
        "arrival_side": None if arr is None else (1 if arr["side"] > 0 else 0),
        "arrival_twin": None if arr is None or port is None else (1 if arr["port"] == port else 0),
        "arrival_axis_is_birth_axis": None if arr is None else (1 if arr["axis"] == b["axis"] else 0),
        "taken_line": int(c["taken_line"]),
        "turned": 1 if c["turned"] else 0,
        "link_frame": None if port is None else (1 if int(f["frames"][port]) > 0 else 0),
        "phase_half": None if ss is None or ss == 0 else (1 if ss > 0 else 0),
        "proper_parity": int(c["proper"]) % 2,
    }, links


def bell(record: dict[str, Any], board: Board, births: list[dict[str, Any]]) -> dict[str, Any]:
    credits = [e for e in record["log"] if e["event"] == "credit"]
    pairs = []
    for b in births:
        if "axis" not in b:
            continue
        ends = {}
        for end in ("minus", "plus"):
            at, twin = b[end], b["plus" if end == "minus" else "minus"]
            first = next((c for c in credits if list(c["node"]) == at and int(c["line"]) == b["line_pair"] and int(c["i"]) > b["i"] and "re_now" in c["frame"]), None)
            if first is None:
                break
            settings, links = end_settings(board, record, first, twin, b)
            arr, tw = links["arrival"], links["twin"]
            H_b = (b["axis"], b["h_sign"])
            lam_b = b["lambda"][end]
            ia = None if arr is None else link_integer(births, board.link_of(at, arr["port"])[0], arr["axis"], int(first["i"]))
            it = None if tw is None else link_integer(births, board.link_of(at, tw["port"])[0], tw["axis"], int(first["i"]))
            outcomes = {
                "int_arrival": 0 if ia is None else ia,
                "Hbirth.Int_arrival": 0 if ia is None or arr["axis"] != H_b[0] else H_b[1] * ia,
                "lambda_birth*int_arrival_inward": 0 if ia is None else lam_b * ia * arr["inward"],
                "Hbirth.Int_twin": 0 if it is None or tw["axis"] != H_b[0] else H_b[1] * it,
                "sense": int(first["sense"]),
                "Hbirth.Harrival": 0 if arr is None or arr["axis"] != H_b[0] else H_b[1] * arr["h_sign"],
                "Hbirth.Htwin": 0 if tw is None or tw["axis"] != H_b[0] else H_b[1] * tw["h_sign"],
                "lambda_birth*lambda_arrival": 0 if arr is None else lam_b * arr["h_sign"] * arr["inward"],
                "lambda_birth*lambda_twin": 0 if tw is None else lam_b * tw["h_sign"] * tw["inward"],
                "Htwin.Harrival": 0 if arr is None or tw is None or arr["axis"] != tw["axis"] else arr["h_sign"] * tw["h_sign"],
                "lambda_twin*lambda_arrival": 0 if arr is None or tw is None else arr["h_sign"] * arr["inward"] * tw["h_sign"] * tw["inward"],
                "sign_h_arrival": 0 if arr is None else arr["h_sign"],
            }
            ends[end] = {"i": int(first["i"]), "settings": settings, "outcomes": outcomes}
        if len(ends) == 2:
            pairs.append({"birth_i": b["i"], "minus": ends["minus"], "plus": ends["plus"]})
    readings = []
    for outcome in pairs[0]["minus"]["outcomes"] if pairs else []:
        for setting in SETTINGS:
            readings.append(chsh(pairs, outcome, setting))
    return {"pairs clicked at both ends": len(pairs), "readings": readings}


def chsh(pairs: list[dict[str, Any]], outcome: str, setting: str) -> dict[str, Any]:
    cells: dict[tuple[int, int], list[int]] = {(x, y): [0, 0, 0] for x in (0, 1) for y in (0, 1)}
    dropped = 0
    for p in pairs:
        a, b = p["minus"]["settings"][setting], p["plus"]["settings"][setting]
        oa, ob = p["minus"]["outcomes"][outcome], p["plus"]["outcomes"][outcome]
        if a is None or b is None or oa == 0 or ob == 0:
            dropped += 1
            continue
        cell = cells[(a, b)]
        cell[0] += 1
        cell[1 if oa * ob > 0 else 2] += 1
    labellings = {}
    best = None
    for swap_a in (0, 1):
        for swap_b in (0, 1):
            a0, a1 = (0, 1) if swap_a == 0 else (1, 0)
            b0, b1 = (0, 1) if swap_b == 0 else (1, 0)
            terms = [(a0, b0, 1), (a0, b1, -1), (a1, b0, 1), (a1, b1, 1)]
            key = f"a={a0} b={b0}"
            if any(cells[(x, y)][0] == 0 for x, y, _s in terms):
                labellings[key] = {"S": None, "empty cell": True}
                continue
            den = 1
            for x, y, _s in terms:
                den = lcm(den, cells[(x, y)][0])
            num = 0
            for x, y, s in terms:
                n, same, opp = cells[(x, y)]
                num += s * (same - opp) * (den // n)
            q, r = divmod(num, den)
            n2, d2 = num * num, den * den
            band = "in nature's band 4 < S^2 <= 8" if 4 * d2 < n2 <= 8 * d2 else ("at the local bound S^2 = 4" if n2 == 4 * d2 else ("below the local bound S^2 < 4" if n2 < 4 * d2 else "above nature's band S^2 > 8"))
            labellings[key] = {"S": [num, den], "S quotient, remainder": [q, r], "S^2": [n2, d2], "band": band}
            if best is None or n2 * best[1] > best[0] * d2:
                best = (n2, d2, key)
    return {
        "outcome": outcome,
        "setting": setting,
        "pairs used": sum(v[0] for v in cells.values()),
        "pairs dropped": dropped,
        "cells (- end, + end): [n, same, opposite]": {f"{x}{y}": v for (x, y), v in cells.items()},
        "largest S^2 over the labellings": None if best is None else {"S^2": [best[0], best[1]], "labelling": best[2], "passes 4": 4 * best[1] < best[0], "within 8": best[0] <= 8 * best[1]},
        "labellings": labellings,
    }


def unit_reading(record: dict[str, Any], births: list[dict[str, Any]]) -> dict[str, Any]:
    T = int(record["T"])
    half = T // 2
    hs = [abs(b["h"]) for b in births if b.get("h_from") == "Node line" and b.get("h", 0) != 0]
    g = 0
    for h in hs:
        g = gcd(g, h)
    return {
        "T": T,
        "T div 2": half,
        "births with h read from the state": len(hs),
        "gcd of |h|": g,
        "gcd div (T div 2)^2, remainder": list(divmod(g, half * half)) if g else None,
        "gcd div T^2, remainder": list(divmod(g, T * T)) if g else None,
        "|h| per birth as [quotient, remainder] by (T div 2)^2": [list(divmod(h, half * half)) for h in hs],
        "bits of |h| max": max((h.bit_length() for h in hs), default=0),
    }


def main(argv: list[str]) -> None:
    record = json.load(open(argv[1], encoding="utf-8"))
    board = Board(record)
    gap0 = emitter_index(record)
    births = read_births(record, board, gap0)
    readable = [b for b in births if b.get("h_from") == "Node line"]
    tr = tracks(record, board, births)
    out: dict[str, Any] = {
        "record": argv[1],
        "cube": board.cube,
        "intervals": int(record["intervals"]),
        "run_back": record.get("run_back"),
        "gap-0 row": gap0,
        "births": len(births),
        "births with the twist read from the Node line": len(readable),
        "births read from the log alone": sum(1 for b in births if b.get("h_from") == "log"),
        "births whose ends are not one Link apart": sum(1 for b in births if "axis" not in b),
        "into matches the log (the take's Node the end the current flows into)": [sum(b["into_matches_log"] for b in readable), len(readable)],
        "h's sign matches the log (the + child's end by the twist's sign)": [sum(b["h_sign_matches_log"] for b in readable), len(readable)],
        "rest births (flow 0)": sum(b.get("rest", False) for b in readable),
        "births by the helicity's sign (h e_a along +a: +, -)": [sum(b["h_sign"] > 0 for b in births if "axis" in b), sum(b["h_sign"] < 0 for b in births if "axis" in b)],
        "births by axis": [sum(b["axis"] == a for b in births if "axis" in b) for a in range(AXES)],
        "children by lambda (the scalar along the arm: +, -)": [sum(b["lambda"][e] > 0 for b in births if "axis" in b for e in ("minus", "plus")), sum(b["lambda"][e] < 0 for b in births if "axis" in b for e in ("minus", "plus"))],
        "one hand row (every birth's h e_a of one sign)": len({b["h_sign"] for b in births if "axis" in b}) == 1,
        "carriage": carriage_counts(tr),
        "unit": unit_reading(record, births),
        "bell": bell(record, board, births),
        "births_detail": births,
        "tracks": tr,
    }
    json.dump(out, open(argv[2], "w", encoding="utf-8"), indent=1)
    brief = {k: v for k, v in out.items() if k not in ("births_detail", "tracks", "bell")}
    print(json.dumps(brief))
    print("bell pairs", out["bell"]["pairs clicked at both ends"])
    for r in out["bell"]["readings"]:
        print(r["outcome"], r["setting"], "used", r["pairs used"], "dropped", r["pairs dropped"], "cells", r["cells (- end, + end): [n, same, opposite]"], "best", r["largest S^2 over the labellings"])


if __name__ == "__main__":
    main(sys.argv)
