"""The draw's digits under the remainder's mirror, read from a record run with MF1_DRAW_LOG=1 (every draw logged with its raw (rem, F, wall, values) per line): per line the digit r div F against (w - 1 - r) div F complemented, B - 1 - d (B = w div F); per draw the composed number of the head's rule on the mirrored digits against the head's, and the plane drawn ((number div unit) mod planes) against the mirror's; per birth whether its draw's plane flips. Usage: python flips.py <record.json>"""
import json
import sys

sys.set_int_max_str_digits(0)


def compose(digits, modulus):
    carry, room = 0, 1
    for d, b in sorted(digits):
        carry = (carry * b + d) % modulus
        room = min(room * b, modulus)
    return carry, room


def main(path):
    run = json.load(open(path, encoding="utf-8"))
    planes = sum(1 for r in run["universe"]["rows"] if int(r["shape"]) == 2)
    draws = [e for e in run["log"] if e["event"] == "draw"]
    births = [e for e in run["log"] if e["event"] == "birth"]
    lines = lines_flipped = 0
    wall_not_multiple = 0
    draw_number_flipped = draw_plane_flipped = 0
    by_key = {}
    for e in draws:
        digits, mirror = [], []
        for rem, f, wl, values in e["raw"]:
            rem, f, wl, values = int(rem), int(f), int(wl), int(values)
            d, dm = rem // f, (wl - 1 - rem) // f
            b = wl // f
            lines += 1
            wall_not_multiple += wl % f != 0
            lines_flipped += dm != b - 1 - d
            digits.append((d, values + 1))
            mirror.append((dm, values + 1))
        n, _ = compose(digits, int(e["modulus"]))
        nm, _ = compose(mirror, int(e["modulus"]))
        assert n == int(e["carry"])
        unit = int(e["unit"])
        plane, plane_m = (n // unit) % planes, (nm // unit) % planes
        draw_number_flipped += n != nm
        draw_plane_flipped += plane != plane_m
        by_key[(int(e["i"]), tuple(e["node"]), unit)] = (plane, plane_m, n, nm)
    births_with_draw = births_flipped = 0
    per_interval = {}
    for b in births:
        key = next((k for k in by_key if k[0] == int(b["i"]) and k[1] == tuple(b["node"])), None)
        if key is None:
            continue
        births_with_draw += 1
        plane, plane_m, n, nm = by_key[key]
        flipped = plane != plane_m
        births_flipped += flipped
        row = per_interval.setdefault(int(b["i"]), [0, 0, 0])
        row[0] += 1
        row[1] += flipped
        row[2] += 1 if b["plus"] == b["node"] else -1
    print(json.dumps({
        "record": path,
        "draws": len(draws),
        "lines_read": lines,
        "lines_with_wall_not_a_multiple_of_F": wall_not_multiple,
        "lines_digit_flipped_under_mirror": lines_flipped,
        "draws_number_changed_under_mirror": draw_number_flipped,
        "draws_plane_changed_under_mirror": draw_plane_flipped,
        "births": len(births),
        "births_with_a_draw": births_with_draw,
        "births_plane_flipped": births_flipped,
        "excess": sum(1 if b["plus"] == b["node"] else -1 for b in births),
        "per_interval (births, flipped, excess)": {str(k): v for k, v in sorted(per_interval.items())},
    }))


if __name__ == "__main__":
    main(sys.argv[1])
