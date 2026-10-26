"""H-Quartet-Children-1's reader of a record under the flag HQ_S1 (a reader of the log; the quartet's matrices read through gram of the flagged copy for the axial bilinear at the birth): the births by the children's shape, every quartet child's charge and axial bilinear per axis at the birth (the lay's levels from the birth line's stood plus the lay recomputed) and along its track (the credits of its record at its Node after the birth: the axis sign on the born Link's axis kept at N of M, the dominant axis kept at N2 of M), the plane children's none; Bell's cells and S for the pairs clicked at both ends with the outcome the sign of the child's axial vector on the twin Link's axis (and on the axis the detector's datum names), the setting each two-valued datum of the detector's own Node at its click, the control with the sense as the outcome. Integers only; S as [num, den] with S^2 against 4 den^2 and 8 den^2.
Usage: python hq_reader.py <record.json> <src of the flagged copy> <out.json>"""

import json
import sys
from collections import Counter
from math import lcm

sys.path.insert(0, sys.argv[2])
from event_universe import gram  # noqa: E402  (the quartet's matrices, derived at the load; a reader's import)

PORT_SIDES = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]
AXES = 3


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def link_of(minus, plus, cube):
    for axis, side in PORT_SIDES:
        if all(((minus[a] + (side if a == axis else 0)) % cube) == plus[a] % cube for a in range(AXES)):
            return axis, side
    raise ValueError("the twin is not one Link away")


def settings_of(c):
    now, before, _ = (int(x) for x in c["taker"])
    return {
        "turned": 1 if c["turned"] else -1,
        "take_sign": sign(before - now),
        "line_named": -1 if int(c["taken_line"]) == 0 else 1,
        "sign_level": sign(int(c["sign_level"])),
        "proper_parity": 1 if int(c["proper"]) % 2 else -1,
        "closes_parity": 1 if int(c["closes"]) % 2 else -1,
    }


def s_of(cells):
    e = {}
    for a in (-1, 1):
        for b in (-1, 1):
            cnt = cells.get((a, b), Counter())
            e[(a, b)] = (cnt[1] - cnt[-1], cnt[1] + cnt[-1])
    out = {"E (same - opposite, n)": {f"{a},{b}": list(v) for (a, b), v in e.items()}}
    if any(n == 0 for _, n in e.values()):
        out["S"] = None
        out["why"] = "an empty setting cell"
        return out
    d = lcm(*(n for _, n in e.values()))
    num = sum(f * x * (d // n) for (x, n), f in zip((e[(-1, -1)], e[(-1, 1)], e[(1, -1)], e[(1, 1)]), (1, -1, 1, 1)))
    out["S"] = [num, d]
    out["S quotient, remainder"] = [num // d, num % d]
    s2, d2 = num * num, d * d
    out["band"] = "below 4" if s2 < 4 * d2 else "4 exactly" if s2 == 4 * d2 else "in nature's band (4, 8]" if s2 <= 8 * d2 else "above 8"
    return out


def main():
    rec = json.load(open(sys.argv[1]))
    log, cube = rec["log"], int(rec["cube"])
    births = [x for x in log if x["event"] == "birth"]
    credits = [x for x in log if x["event"] == "credit"]
    out = {"record": sys.argv[1], "births": len(births), "credits": len(credits), "run_back": rec["run_back"], "counts": rec["counts"]}
    shapes = Counter(len(b["stood"][0]) // 2 for b in births)
    out["births by the children's shape"] = {str(k): v for k, v in shapes.items()}
    quartet_births = [b for b in births if len(b["stood"][0]) == 16]
    plane_births = [b for b in births if len(b["stood"][0]) == 4]
    out["W of the plane children (sum per birth)"] = Counter(sum(b["W_children"]) for b in plane_births)
    out["W of the plane children (sum per birth)"] = {str(k): v for k, v in out["W of the plane children (sum per birth)"].items()}
    children = []
    for b in quartet_births:
        s, a_, b_ = int(b["line_pair"]), int(b["amplitude"][0]), int(b["amplitude"][1])
        axis, side = link_of(b["minus"], b["plus"], cube)
        for end, sense in (("minus", -1), ("plus", 1)):
            where = b[end]
            v = gram.spin_vector(8, axis, sense * side)
            turned = gram.matvec(gram.rotation(8), list(v))
            laid = []
            for vv, jj in zip(v, turned):
                laid += [sense * a_ * vv, b_ * jj]
            stood = b["stood"][0 if end == "minus" else 1]
            levels = [int(x) + y for x, y in zip(stood, laid)]
            nows, befores = levels[0::2], levels[1::2]
            axial = [int(x) for x in gram.density(8, nows)]
            gj = gram.matmul(gram.gram(8), gram.rotation(8))
            w = int(gram.form(gj, befores, nows))
            vgv = int(gram.form(gram.gram(8), list(v), list(v)))
            aw = [int(gram.form(gj, befores, gram.matvec(ga, nows))) for ga in gram.axes(8)]
            track = [c for c in credits if int(c["line"]) == s and c["node"] == where and int(c["i"]) > int(b["i"])]
            later = [x for x in births if int(x["i"]) > int(b["i"]) and int(x["line_pair"]) == s and (x["minus"] == where or x["plus"] == where)]
            if later:
                track = [c for c in track if int(c["i"]) <= int(later[0]["i"])]
            sg0 = sign(axial[axis])
            kept = sum(1 for c in track if c["frame"]["axial_sign"][axis] == sg0)
            dominant = sum(1 for c in track if max(range(AXES), key=lambda k, c=c: abs(int(c["frame"]["axial"][k]))) == axis)
            children.append({
                "birth i": int(b["i"]), "node": where, "sense": sense, "born axis": axis, "side": side,
                "vector": v, "v.G.v": vgv, "W": w, "W_children (log)": b["W_children"], "T div 2": a_ * b_,
                "W over T div 2": [w // (a_ * b_), w % (a_ * b_)],
                "axial at birth": axial, "axial sign at birth": [sign(x) for x in axial],
                "axial wronskian at birth": aw, "axial wronskian over W": [x // w if w else None for x in aw],
                "stood at nothing": all(int(x) == 0 for x in stood),
                "credits on the track": len(track), "axis sign kept": kept, "dominant axis kept": dominant,
                "first credit": None if not track else {"i": int(track[0]["i"]), "axial": track[0]["frame"]["axial"], "axial_sign": track[0]["frame"]["axial_sign"], "W": track[0]["frame"]["W"], "sense": track[0]["sense"], "levels_now": track[0]["frame"]["levels_now"]},
            })
    out["quartet children"] = children
    out["axis sign kept, summed"] = [sum(c["axis sign kept"] for c in children), sum(c["credits on the track"] for c in children)]
    out["dominant axis kept, summed"] = [sum(c["dominant axis kept"] for c in children), sum(c["credits on the track"] for c in children)]
    out["pairs' axes summed to 0"] = sum(1 for k in range(0, len(children), 2) if all(x + y == 0 for x, y in zip(children[k]["axial at birth"], children[k + 1]["axial at birth"])))
    out["pairs' W summed to 0"] = sum(1 for k in range(0, len(children), 2) if children[k]["W"] + children[k + 1]["W"] == 0)
    # Bell on the quartet pairs clicked at both ends
    pairs = []
    for k in range(0, len(children), 2):
        c1, c2 = children[k], children[k + 1]
        if c1["first credit"] and c2["first credit"]:
            pairs.append((c1, c2))
    out["quartet pairs clicked at both ends"] = len(pairs)
    plane_pairs = []
    for b in plane_births:
        s = int(b["line_pair"])
        ends = []
        for end in ("minus", "plus"):
            t = [c for c in credits if int(c["line"]) == s and c["node"] == b[end] and int(c["i"]) > int(b["i"])]
            ends.append(t[0] if t else None)
        if all(ends):
            plane_pairs.append(ends)
    out["plane pairs clicked at both ends"] = len(plane_pairs)
    readings = {}
    for setting in ("turned", "take_sign", "line_named", "sign_level", "proper_parity", "closes_parity"):
        for outcome in ("axial on the twin Link", "axial on the detector's axis", "sense (control)"):
            cells, zeros = {}, 0
            for c1, c2 in pairs:
                k1, k2 = c1["first credit"], c2["first credit"]
                raw1 = [c for c in credits if int(c["i"]) == k1["i"] and c["node"] == c1["node"] and "axial" in c["frame"]][0]
                raw2 = [c for c in credits if int(c["i"]) == k2["i"] and c["node"] == c2["node"] and "axial" in c["frame"]][0]
                a, b = settings_of(raw1)[setting], settings_of(raw2)[setting]
                ax = c1["born axis"]
                if outcome == "axial on the twin Link":
                    o1, o2 = k1["axial_sign"][ax], k2["axial_sign"][ax]
                elif outcome == "axial on the detector's axis":
                    o1 = k1["axial_sign"][ax if a > 0 else (ax + 1) % AXES]
                    o2 = k2["axial_sign"][ax if b > 0 else (ax + 1) % AXES]
                else:
                    o1, o2 = k1["sense"], k2["sense"]
                if 0 in (a, b, o1, o2):
                    zeros += 1
                    continue
                cells.setdefault((a, b), Counter())[o1 * o2] += 1
            r = s_of(cells)
            r["pairs left out (a zero datum or outcome)"] = zeros
            readings[f"setting={setting} outcome={outcome}"] = r
    out["bell on the quartet pairs"] = readings
    json.dump(out, open(sys.argv[3], "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("quartet children", "bell on the quartet pairs", "counts")}))
    for c in children:
        print(json.dumps({k: c[k] for k in ("birth i", "node", "sense", "born axis", "side", "v.G.v", "W", "W over T div 2", "axial sign at birth", "axial wronskian over W", "stood at nothing", "credits on the track", "axis sign kept", "dominant axis kept")}))
    for k, v in readings.items():
        print(k, "S", v.get("S"), v.get("band", v.get("why")), "E", v["E (same - opposite, n)"], "out", v["pairs left out (a zero datum or outcome)"])


if __name__ == "__main__":
    main()
