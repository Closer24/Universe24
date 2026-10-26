"""The setting from the click's own act (H-Setting-From-The-Frame-1): a reader of a record's log, no act.

For every born pair clicked at both ends (the first credit of the pair's line at each child's Node after the birth, the Bell
predicate's choice), the two ends' settings are read as data of the detector Node at its click, each by one generic rule,
and the two ends' outcomes by one generic rule; E(a, b) is counted per setting pair and S = E(a, b) - E(a, b') + E(a', b)
+ E(a', b') as one rational [num, den] with its quotient and remainder, S^2 against 4 and 8 as integer inequalities.
Integers only; the exact-zero outcomes are counted and left out of E.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from math import lcm


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def first_click(credits: list[dict], where: list[int], line: int, after: int) -> dict | None:
    for c in credits:
        if c["node"] == where and c["line"] == line and int(c["i"]) > after and "re_now" in c["frame"]:
            return c
    return None


PORT_SIDES = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]


def port_to(here: list[int], there: list[int], cube: int) -> int:
    """The Port of the Node `here` whose neighbour on the torus is `there` (the birth Link's own Port toward the twin)."""
    for port, (axis, side) in enumerate(PORT_SIDES):
        if all((here[a] + (side if a == axis else 0)) % cube == there[a] % cube for a in range(3)):
            return port
    raise ValueError("the twin is not one Link away")


def settings_of(c: dict, end: int, port: int = 0) -> dict[str, int]:
    """Every candidate datum of the detector Node at its click, each two-valued in {-1, +1} (0 where the datum is not read)."""
    f = c["frame"]
    now, before, _levels = (int(x) for x in c["taker"])
    cc, ss = (int(x) for x in f["phases"][port])
    frames = [int(x) for x in f["frames"]]
    parity = 1
    for x in frames:
        parity *= sign(x) if x else 1
    return {
        "slot": 1,
        "line_named": -1 if int(c["taken_line"]) == 0 else 1,
        "take_sign": sign(before - now),
        "turned": 1 if c["turned"] else -1,
        "frame_parity": parity,
        "crossing_side": sign(int(f["re_before"])) or sign(int(f["re_now"])),
        "arrival_side": end,
        "phase_half": sign(ss),
        "phase_quadrant": sign(cc * ss),
    }


def outcomes_of(c: dict, end_sense: int, port: int = 0) -> dict[str, int]:
    f = c["frame"]
    now, before, _levels = (int(x) for x in c["taker"])
    k = int(c["taken_line"])
    cc, ss = (int(x) for x in f["phases"][port])
    return {
        "level_on_phase": sign(cc * int(f["re_now"]) + ss * int(f["im_now"])),
        "sense": int(c["sense"]),
        "take_sign": sign(before - now),
        "level_on_named_line": sign(int(f["re_now"]) if k == 0 else int(f["im_now"])),
    }


def s_of(cells: dict[tuple[int, int], Counter]) -> dict:
    """E per cell as [same - opposite, n]; S as [num, den] by the common denominator; the quotient, the remainder; the band."""
    e = {}
    for a in (-1, 1):
        for b in (-1, 1):
            cnt = cells.get((a, b), Counter())
            e[(a, b)] = (cnt[1] - cnt[-1], cnt[1] + cnt[-1])
    if any(n == 0 for _, n in e.values()):
        return {"E": {f"{a},{b}": list(v) for (a, b), v in e.items()}, "S": None, "why": "an empty setting cell"}
    den = lcm(*(n for _, n in e.values()))
    terms = [(e[(-1, -1)], 1), (e[(-1, 1)], -1), (e[(1, -1)], 1), (e[(1, 1)], 1)]
    num = sum(s * (m * (den // n)) for (m, n), s in terms)
    q, r = divmod(num, den)
    return {
        "E": {f"{a},{b}": list(v) for (a, b), v in e.items()},
        "S": [num, den],
        "S quotient, remainder": [q, r],
        "S^2 as [num^2, den^2]": [num * num, den * den],
        "4 den^2 < num^2": 4 * den * den < num * num,
        "num^2 <= 8 den^2": num * num <= 8 * den * den,
        "band": "in nature's band" if 4 * den * den < num * num <= 8 * den * den else ("above 8" if num * num > 8 * den * den else ("at 4 exactly" if num * num == 4 * den * den else "below 4")),
    }


def main() -> None:
    path, label = sys.argv[1], sys.argv[2]
    rec = json.load(open(path))
    log = rec["log"]
    credits = [x for x in log if x["event"] == "credit"]
    births = [x for x in log if x["event"] == "birth"]
    pairs = []
    for b in births:
        ends = [first_click(credits, b[k], int(b["line_pair"]), int(b["i"])) for k in ("minus", "plus")]
        if ends[0] is None or ends[1] is None:
            continue
        pairs.append((b, ends[0], ends[1]))
    out = {"record": label, "births": len(births), "pairs clicked at both ends": len(pairs), "readings": {}}
    agree = {}
    datum_values = {}
    cube = int(rec["cube"])
    for b, c1, c2 in pairs:
        s1, s2 = settings_of(c1, -1, port_to(b["minus"], b["plus"], cube)), settings_of(c2, 1, port_to(b["plus"], b["minus"], cube))
        for name in s1:
            datum_values.setdefault(name, Counter())[(s1[name], s2[name])] += 1
            agree.setdefault(name, Counter())["agree" if s1[name] == s2[name] else "differ"] += 1
    out["settings agree through the root (pairs agree, differ)"] = {k: [v["agree"], v["differ"]] for k, v in agree.items()}
    out["setting values per end (minus, plus) counted"] = {k: {f"{a},{b}": n for (a, b), n in sorted(v.items())} for k, v in datum_values.items()}
    for setting in ("slot", "line_named", "take_sign", "turned", "frame_parity", "crossing_side", "arrival_side", "phase_half", "phase_quadrant"):
        for outcome in ("sense", "take_sign", "level_on_named_line", "level_on_phase"):
            cells: dict[tuple[int, int], Counter] = {}
            zeros = 0
            for b, c1, c2 in pairs:
                p1, p2 = port_to(b["minus"], b["plus"], cube), port_to(b["plus"], b["minus"], cube)
                a, bb = settings_of(c1, -1, p1)[setting], settings_of(c2, 1, p2)[setting]
                o1, o2 = outcomes_of(c1, -1, p1)[outcome], outcomes_of(c2, 1, p2)[outcome]
                if o1 == 0 or o2 == 0 or a == 0 or bb == 0:
                    zeros += 1
                    continue
                cells.setdefault((a, bb), Counter())[o1 * o2] += 1
            r = s_of(cells)
            r["pairs with a zero datum or outcome (left out)"] = zeros
            out["readings"][f"setting={setting} outcome={outcome}"] = r
    json.dump(out, open(sys.argv[3], "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "readings"}))
    for k, v in out["readings"].items():
        print(k, "E", v["E"], "S", v.get("S"), v.get("S quotient, remainder"), v.get("band", v.get("why")), "zeros", v["pairs with a zero datum or outcome (left out)"])


if __name__ == "__main__":
    main()
