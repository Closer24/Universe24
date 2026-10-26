"""The helicity from the twist, read on a record and its twists' file (H-Helicity-From-The-Twist-1): a reader, no act, integers only.

(1) The reading. For every birth the born Link (the - child's Node and the + child's Node, one Link apart on the torus: its axis a,
its lower end lo with hi = lo + e_a), and the twist h of the taken record on that Link at the interval's start, read from the state
the close read (twists_run.py: the sign of links.row_twist per record, per axis, per Node after every step; the start of the birth's
interval i is the state after i - 1). The reading is checked against the click's own choice (close.py meet: the + child at the end the
current flows into, the birth's `node`, where h > 0, at the other end where h < 0): the sign read equals the choice at every birth
that is not at rest. The pair's helicity along the Link's direction: H = sign(h) along +a, the one pseudo-vector h e_lo,hi (read from hi
the twist is -h along -a: the same vector); the + child's arm is the direction from the - end to the + end, arm_plus = +1 where the +
child stands at hi, else -1; the - child's arm the opposite; a child's helicity along its arm is H arm_c.
Then the born Link's own twist after the birth (the children's record and the taken record) at the intervals that follow, and the
track of each child: the credits of the children's record at the child's Node after the birth, until a later birth lays a child of
that record at that Node. At each credit the twist of the children's record on the click's Link at the interval's start: (a) the Link
toward the twin (the born Link itself; along the track's direction, from the twin into the detector, its sign is sign(t) arm_c) and
(b) the arrival Link (the Port of the largest inflow of the gap-0 current at the interval's start, from the record's Node lines, the
Bell pair's datum; along the track's direction into the detector, sign(t') (-side)). Carried at a credit where the sign along the
track equals the birth's H arm_c.
(2) Bell with the axis. The pairs clicked at both ends (each end's first credit of the children's record at the child's Node after the
birth), the outcome at an end A = a_c . a_d with a_c the child's helicity (at the birth, H arm_c; or at the credit, the twin Link's
sign along the track) and a_d the detector's twist sign on the click's Link along the track's direction (the twin Link or the arrival
Link), the setting one datum of the detector's own click (the Bell pair's list, and the detector's twist signs themselves); the four
cells [n, same, opposite], S = E(a, b) - E(a, b') + E(a', b) + E(a', b') as [num, den] under the four labellings, S^2 against 4 and 8.
Usage: python helicity_reader.py <record.json> <twists.json> <label> <out.json>
"""

from __future__ import annotations

import json
import sys
from math import lcm
from typing import Any

AXES = 3
PORT_SIDES = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]
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
    "twist_twin_side",
    "twist_arrival_side",
)
OUTCOMES = (
    "sense",
    "H_birth x twist_twin",
    "H_birth x twist_arrival",
    "H_credit_twin x twist_arrival",
    "H_credit_arrival x twist_twin",
)


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def index_of(cube: int, at: list[int]) -> int:
    return at[0] * cube * cube + at[1] * cube + at[2]


def moved(cube: int, at: list[int], axis: int, side: int) -> list[int]:
    return [(at[a] + (side if a == axis else 0)) % cube for a in range(AXES)]


def port_toward(cube: int, at: list[int], other: list[int]) -> int | None:
    for port, (axis, side) in enumerate(PORT_SIDES):
        if moved(cube, at, axis, side) == list(other):
            return port
    return None


def link_of(cube: int, at: list[int], port: int) -> tuple[int, list[int]]:
    """The +axis Link the Port names: its axis and its lower end lo (the Port's own Node on the + side, the neighbour on the - side)."""
    axis, side = PORT_SIDES[port]
    return axis, (list(at) if side == 1 else moved(cube, at, axis, -1))


def twist_at(twists: dict, interval: int, rec: int, axis: int, cube: int, lo: list[int]) -> int | None:
    """The sign of the record's twist on the +axis Link from lo at the start of `interval` (the state after interval - 1)."""
    kept = twists.get(str(interval - 1))
    if kept is None:
        return None
    return int(kept[rec][axis][index_of(cube, lo)])


def inflows(record: dict, credit: dict) -> list[int] | None:
    """The gap-0 line's current into the credit's Node on each of its six Links at the interval's start (the Bell pair's reading)."""
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
            found.append(int(line["current"][axis][index_of(cube, moved(cube, at, axis, -1))]))
    return found


def arrival_port(record: dict, credit: dict) -> int | None:
    flows = inflows(record, credit)
    if flows is None:
        return None
    top = max(flows)
    if top > 0 and flows.count(top) == 1:
        return flows.index(top)
    return None


def credit_data(record: dict, twists: dict, c: dict, rec: int, twin: list[int], arm: int, h_birth: int) -> dict[str, Any]:
    """One credit's twist readings on the click's Links: the twin Link and the arrival Link, each along +axis and along the track into the detector."""
    cube = int(record["cube"])
    i = int(c["i"])
    toward = port_toward(cube, c["node"], twin)
    out: dict[str, Any] = {"i": i, "node": list(c["node"]), "sense": int(c["sense"])}
    if toward is not None:
        axis, lo = link_of(cube, c["node"], toward)
        t = twist_at(twists, i, rec, axis, cube, lo)
        out["twin_axis"] = axis
        out["twist_twin_plus"] = t
        # the track into the detector along the twin Link is arm_c along +axis (the arm from the twin to the child)
        out["twist_twin_track"] = None if t is None else t * arm
    else:
        out["twist_twin_plus"] = out["twist_twin_track"] = None
    port = arrival_port(record, c)
    out["arrival_port"] = port
    if port is not None:
        axis, lo = link_of(cube, c["node"], port)
        t = twist_at(twists, i, rec, axis, cube, lo)
        out["twist_arrival_plus"] = t
        out["twist_arrival_track"] = None if t is None else t * (-PORT_SIDES[port][1])
    else:
        out["twist_arrival_plus"] = out["twist_arrival_track"] = None
    helicity = h_birth * arm
    out["carried_twin"] = None if out["twist_twin_track"] is None else int(out["twist_twin_track"] == helicity)
    out["carried_arrival"] = None if out["twist_arrival_track"] is None else int(out["twist_arrival_track"] == helicity)
    out["twin_plus_equals_birth"] = None if out["twist_twin_plus"] is None else int(out["twist_twin_plus"] == h_birth)
    f = c["frame"]
    now_was, before, _levels = (int(x) for x in c["taker"])
    out["settings"] = {
        "turned": 1 if c["turned"] else 0,
        "take_dir": None if before == now_was else (1 if before > now_was else 0),
        "re_side": None if int(f["re_now"]) == 0 else (1 if int(f["re_now"]) > 0 else 0),
        "im_side": None if int(f["im_now"]) == 0 else (1 if int(f["im_now"]) > 0 else 0),
        "link_frame": None if toward is None else (1 if int(f["frames"][toward]) > 0 else 0),
        "arrival_side": None if port is None else (1 if PORT_SIDES[port][1] > 0 else 0),
        "arrival_twin": None if port is None or toward is None else (1 if port == toward else 0),
        "proper_parity": int(c["proper"]) % 2,
        "sign_level": None if int(c["sign_level"]) == 0 else (1 if int(c["sign_level"]) > 0 else 0),
        "taken_line": int(c["taken_line"]),
        "twist_twin_side": None if not out["twist_twin_track"] else (1 if out["twist_twin_track"] > 0 else 0),
        "twist_arrival_side": None if not out["twist_arrival_track"] else (1 if out["twist_arrival_track"] > 0 else 0),
    }
    hb = helicity
    tt, ta = out["twist_twin_track"], out["twist_arrival_track"]
    out["outcomes"] = {
        "sense": int(c["sense"]),
        "H_birth x twist_twin": 0 if tt is None else hb * tt,
        "H_birth x twist_arrival": 0 if ta is None else hb * ta,
        "H_credit_twin x twist_arrival": 0 if tt is None or ta is None else tt * ta,
        "H_credit_arrival x twist_twin": 0 if tt is None or ta is None else ta * tt,
    }
    return out


def chsh(pairs: list[dict], outcome: str, setting: str) -> dict[str, Any]:
    """The four cells' counts and S under the four labellings, integers only (the Bell pair's count, re-cut)."""
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
            q, r = divmod(num2, d2)
            band = (
                "in nature's band 4 < S^2 <= 8"
                if 4 * d2 < num2 <= 8 * d2
                else "at the local bound S^2 = 4"
                if num2 == 4 * d2
                else "below the local bound S^2 < 4"
                if num2 < 4 * d2
                else "above nature's band S^2 > 8"
            )
            labellings[f"a={a0} b={b0}"] = {"S": [num, den], "S^2": [num2, d2], "S^2 quotient, remainder": [q, r], "band": band}
    return {
        "outcome": outcome,
        "setting": setting,
        "pairs used": agree + differ,
        "pairs dropped": dropped,
        "settings agree / differ": [agree, differ],
        "cells (- end, + end): [n, same, opposite]": {f"{x}{y}": v for (x, y), v in cells.items()},
        "labellings": labellings,
    }


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    _, record_path, twists_path, label, out_path = argv
    record = json.load(open(record_path, encoding="utf-8"))
    tw = json.load(open(twists_path, encoding="utf-8"))
    twists = tw["twists"]
    cube = int(record["cube"])
    intervals = int(record["intervals"])
    log = record["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    out: dict[str, Any] = {"record": label, "intervals": intervals, "cube": cube, "births": len(births), "credits": len(credits), "run_back": record["run_back"], "records": tw["records"]}
    # (1) the birth's reading
    read_ok = read_off = rest_like = 0
    h_signs = {"-1": 0, "0": 0, "1": 0}
    born_after = {"children next kept": 0, "children next read": 0, "taken next kept": 0, "taken next read": 0}
    run_lengths = []
    birth_rows: list[dict] = []
    tracks: list[dict] = []
    for born, b in enumerate(births):
        i, rec_taken, rec_child = int(b["i"]), int(b["taken_row"]), int(b["line_pair"])
        minus, plus = list(b["minus"]), list(b["plus"])
        port = port_toward(cube, minus, plus)
        if port is None:
            birth_rows.append({"i": i, "twin not one Link away": True})
            continue
        axis, lo = link_of(cube, minus, port)
        h = twist_at(twists, i, rec_taken, axis, cube, lo)
        h_child = twist_at(twists, i, rec_child, axis, cube, lo)
        choice = 1 if plus == list(b["node"]) else -1
        at_rest = int(b["taken"]) == 0 if "taken" in b else False
        if h == choice:
            read_ok += 1
        elif h == 0 or at_rest:
            rest_like += 1
        else:
            read_off += 1
        h_signs[str(h)] += 1
        arm_plus = 1 if plus == moved(cube, lo, axis, 1) else -1
        H = h if h != 0 else choice
        # the born Link's own twist after the birth
        nxt_child = twist_at(twists, i + 1, rec_child, axis, cube, lo)
        nxt_taken = twist_at(twists, i + 1, rec_taken, axis, cube, lo)
        if nxt_child is not None:
            born_after["children next read"] += 1
            born_after["children next kept"] += int(nxt_child == H)
        if nxt_taken is not None:
            born_after["taken next read"] += 1
            born_after["taken next kept"] += int(nxt_taken == H)
        run = 0
        k = i + 1
        while True:
            t = twist_at(twists, k, rec_child, axis, cube, lo)
            if t is None or t != H:
                break
            run += 1
            k += 1
        run_lengths.append(run)
        birth_rows.append({"i": i, "node": list(b["node"]), "minus": minus, "plus": plus, "axis": axis, "lo": lo, "h_taken": h, "h_children_record": h_child, "choice (+ at node)": choice, "H": H, "arm_plus": arm_plus, "children twist on the born Link kept for intervals": run})
        # the tracks of the two children
        for end, arm, laid in ((minus, -arm_plus, -1), (plus, arm_plus, 1)):
            later = [bb for bb in births if int(bb["i"]) > i and int(bb["line_pair"]) == rec_child and (list(bb["minus"]) == end or list(bb["plus"]) == end)]
            stop = min((int(bb["i"]) for bb in later), default=intervals + 1)
            track = [c for c in credits if list(c["node"]) == end and int(c["line"]) == rec_child and i < int(c["i"]) < stop and "re_now" in c["frame"]]
            twin = plus if laid == -1 else minus
            data = [credit_data(record, twists, c, rec_child, twin, arm, H) for c in track]
            tracks.append({"birth": born, "birth_i": i, "end": end, "laid": laid, "arm": arm, "helicity": H * arm, "stop": stop, "credits": data})
    out["births read: twist sign equals the click's choice"] = [read_ok, read_ok + read_off + rest_like]
    out["births read: off"] = read_off
    out["births read: twist 0 or at rest (the twist not read by the close)"] = rest_like
    out["h signs at the births (taken record)"] = h_signs
    out["the born Link's twist at the next interval (kept of read)"] = born_after
    out["children twist on the born Link kept for intervals (per birth)"] = run_lengths
    out["birth rows"] = birth_rows
    # the carriage counts
    def count(key: str, which: list[dict]) -> list[int]:
        read = [c[key] for t in which for c in t["credits"] if c[key] is not None]
        return [sum(read), len(read)]
    carriage = {
        "credits on the tracks": sum(len(t["credits"]) for t in tracks),
        "carried on the twin Link (sign along the track equal to the birth's helicity)": count("carried_twin", tracks),
        "twin Link twist along +axis equal to the birth's h": count("twin_plus_equals_birth", tracks),
        "carried on the arrival Link": count("carried_arrival", tracks),
        "twin Link twist 0 at the credit": sum(1 for t in tracks for c in t["credits"] if c["twist_twin_track"] == 0),
        "arrival Link undefined": sum(1 for t in tracks for c in t["credits"] if c["arrival_port"] is None),
        "first credits: carried on the twin Link": [sum(t["credits"][0]["carried_twin"] or 0 for t in tracks if t["credits"] and t["credits"][0]["carried_twin"] is not None), sum(1 for t in tracks if t["credits"] and t["credits"][0]["carried_twin"] is not None)],
        "first credits: carried on the arrival Link": [sum(t["credits"][0]["carried_arrival"] or 0 for t in tracks if t["credits"] and t["credits"][0]["carried_arrival"] is not None), sum(1 for t in tracks if t["credits"] and t["credits"][0]["carried_arrival"] is not None)],
        "tracks": len(tracks),
        "tracks with no credit": sum(1 for t in tracks if not t["credits"]),
    }
    by_sign = {}
    for t in tracks:
        for c in t["credits"]:
            if c["twist_twin_track"] is not None:
                by_sign.setdefault(f"helicity {t['helicity']}", {"twin track +": 0, "twin track -": 0, "twin track 0": 0})
                key = "twin track +" if c["twist_twin_track"] > 0 else ("twin track -" if c["twist_twin_track"] < 0 else "twin track 0")
                by_sign[f"helicity {t['helicity']}"][key] += 1
    carriage["twin Link's sign along the track by the child's birth helicity"] = by_sign
    out["carriage"] = carriage
    out["tracks"] = tracks
    # (2) Bell with the axis
    by_birth: dict[int, dict] = {}
    for t in tracks:
        if t["credits"]:
            by_birth.setdefault(t["birth"], {})["minus" if t["laid"] == -1 else "plus"] = t["credits"][0]
    pairs = [{"birth": k, **v} for k, v in sorted(by_birth.items()) if "minus" in v and "plus" in v]
    out["pairs clicked at both ends"] = len(pairs)
    out["pairs clicking in one interval"] = sum(p["minus"]["i"] == p["plus"]["i"] for p in pairs)
    out["pairs: the two ends' outcomes"] = {o: {"same": sum(p["minus"]["outcomes"][o] * p["plus"]["outcomes"][o] > 0 for p in pairs), "opposite": sum(p["minus"]["outcomes"][o] * p["plus"]["outcomes"][o] < 0 for p in pairs), "zero": sum(p["minus"]["outcomes"][o] * p["plus"]["outcomes"][o] == 0 for p in pairs)} for o in OUTCOMES}
    out["bell"] = [chsh(pairs, o, s) for o in OUTCOMES for s in SETTINGS]
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    summary = {k: v for k, v in out.items() if k not in ("birth rows", "tracks", "bell", "records")}
    print(json.dumps(summary))
    passed = []
    for r in out["bell"]:
        for lab, v in r["labellings"].items():
            if v.get("S") is not None:
                band = v["band"]
                tag = "PASS4" if "nature" in band or "above" in band else ("AT4" if "= 4" in band else "BELOW")
                if lab == "a=0 b=0" or tag == "PASS4":
                    print(label, "|", r["outcome"], "|", r["setting"], "|", lab, "| cells", r["cells (- end, + end): [n, same, opposite]"], "| S", v["S"], "| S^2 q,r", v["S^2 quotient, remainder"], "|", tag, "| dropped", r["pairs dropped"])
                if tag == "PASS4":
                    passed.append((r["outcome"], r["setting"], lab, v["S"]))
    print(label, "readings passing 4:", len(passed), passed)


if __name__ == "__main__":
    main(sys.argv)
