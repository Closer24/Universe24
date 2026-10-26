"""mf2: the matter count and the draw's flips from a record's log (no engine import).
Usage: count_mf2.py <record.json> <bang starts, e.g. 1,219,443> [planes 3]
Per bang: births; + child at the take's Node (plus == node) against the other end (minus == node);
W_children by sense; the draws matched to the births: the plain composition against the mirror's
(every remainder r -> w - 1 - r), the plane drawn under each, the births whose plane flips;
the brief's digit test per digit: d = r div F against (b - 1) - ((w - 1 - r) div F); the half read's plane."""
import json
import sys


def compose(digits, modulus):
    carry, room = 0, 1
    for d, b in sorted(digits):
        carry = (carry * b + d) % modulus
        room = min(room * b, modulus)
    return carry, room


def plane_of(number, unit, planes):
    return (number // unit) % planes


def main():
    rec = json.load(open(sys.argv[1]))
    starts = [int(x) for x in sys.argv[2].split(",")]
    planes = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    log = rec["log"]
    draws = {}
    for e in log:
        if e["event"] == "draw":
            draws.setdefault((e["i"], tuple(e["node"])), []).append(e)
    births = [e for e in log if e["event"] == "birth"]
    last = max([e["i"] for e in log] + [rec.get("intervals", 0)])
    edges = starts + [10 ** 9]
    out = {"record": sys.argv[1], "births": len(births), "bangs": []}
    tot = {"at_take": 0, "other": 0, "flip_plane": 0, "flip_digit_births": 0, "digits": 0, "digits_flipped": 0, "half_flip": 0, "matched": 0, "Wp": 0, "Wm": 0}
    for k in range(len(starts)):
        lo, hi = edges[k], edges[k + 1]
        bb = [e for e in births if lo <= e["i"] < hi]
        row = {"bang": k + 1, "from": lo, "births": len(bb), "plus_at_take": 0, "minus_at_take": 0, "neither": 0,
               "W_sum": 0, "flip_plane": 0, "flip_digit_births": 0, "digits": 0, "digits_flipped": 0, "half_flip": 0, "matched": 0, "planes_plain": [0] * planes, "planes_mirror": [0] * planes, "emitter_births": 0, "emitter_flip_plane": 0, "by_taken_row": {}}
        for e in bb:
            at = tuple(e["node"])
            if tuple(e["plus"]) == at:
                row["plus_at_take"] += 1
            elif tuple(e["minus"]) == at:
                row["minus_at_take"] += 1
            else:
                row["neither"] += 1
            row["W_sum"] += sum(e["W_children"])
            row["by_taken_row"][str(e["taken_row"])] = row["by_taken_row"].get(str(e["taken_row"]), 0) + 1
            ds = draws.get((e["i"], at))
            if not ds:
                continue
            d = ds[0]
            if d["origin"] or d["coarse"]:
                continue
            row["matched"] += 1
            unit, modulus = d["unit"], d["modulus"]
            plain = [(r // f, w // f + 1) for r, f, w in d["raw"]]
            mirror = [((w - 1 - r) // f, w // f + 1) for r, f, w in d["raw"]]
            halfr = [(abs(r + r + 1 - w) // (f + f), (w - 1) // (f + f) + 1) for r, f, w in d["raw"]]
            halfm = [(abs((w - 1 - r) * 2 + 1 - w) // (f + f), (w - 1) // (f + f) + 1) for r, f, w in d["raw"]]
            n_plain = compose(plain, modulus)[0]
            n_mirror = compose(mirror, modulus)[0]
            p1, p2 = plane_of(n_plain, unit, planes), plane_of(n_mirror, unit, planes)
            row["planes_plain"][p1] += 1
            row["planes_mirror"][p2] += 1
            row["flip_plane"] += p1 != p2
            if e["taken_row"] == 0:
                row["emitter_births"] += 1
                row["emitter_flip_plane"] += p1 != p2
            # the brief's test in the base of the values a remainder reaches, b' = (w - 1) div F + 1 (the engine's base w div F + 1 is one too large where F divides w)
            flipped = sum(1 for (r, f, w) in d["raw"] if (r // f) != ((w - 1) // f) - ((w - 1 - r) // f))
            flipped_engine_base = sum(1 for (dp, b), (dm, _b) in zip(plain, mirror) if dp != (b - 1) - dm)
            row["digits_flipped_engine_base"] = row.get("digits_flipped_engine_base", 0) + flipped_engine_base
            row["digits_F_divides_w"] = row.get("digits_F_divides_w", 0) + sum(1 for (r, f, w) in d["raw"] if w % f == 0)
            row["digits_F_1"] = row.get("digits_F_1", 0) + sum(1 for (r, f, w) in d["raw"] if f == 1)
            row["digits"] += len(plain)
            row["digits_flipped"] += flipped
            row["flip_digit_births"] += flipped > 0
            h1 = plane_of(compose(halfr, modulus)[0], unit, planes)
            h2 = plane_of(compose(halfm, modulus)[0], unit, planes)
            row["half_flip"] += h1 != h2
        row["excess_plus_at_take"] = row["plus_at_take"] - row["minus_at_take"]
        out["bangs"].append(row)
        for key, src in (("at_take", "plus_at_take"), ("other", "minus_at_take"), ("flip_plane", "flip_plane"), ("flip_digit_births", "flip_digit_births"), ("digits", "digits"), ("digits_flipped", "digits_flipped"), ("half_flip", "half_flip"), ("matched", "matched")):
            tot[key] += row[src]
    senses = [w for e in births for w in e["W_children"]]
    tot["Wp"] = sum(1 for w in senses if w > 0)
    tot["Wm"] = sum(1 for w in senses if w < 0)
    tot["W0"] = sum(1 for w in senses if w == 0)
    tot["excess_plus_at_take"] = tot["at_take"] - tot["other"]
    out["total"] = tot
    out["counts"] = {k: v for k, v in rec.get("counts", {}).items() if k in ("births", "met", "refused_origin", "refused_lay", "refused_sense", "refused_twist", "refused_orientation", "taken", "booked", "turns")}
    out["last_interval"] = last
    print(json.dumps(out))


main()
