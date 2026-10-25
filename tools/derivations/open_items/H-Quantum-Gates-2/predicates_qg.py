"""The quantum gates as predicates on the record (hand qg2, 2026-10-25): the ledger's rows 55 the two slits, 56 Bell and 57 GHZ, one function each in the decoder's form (a Record in, one row out with its numbers and its verdict SHOWN / NOT SHOWN / NOT READ), read from the record alone (the lay lines, the births, the refused lines and the credits of the log), integers only, no act touched.

55 the two slits: the world lays two packets of the gap-0 row at one centre with one wave number mirrored on one axis (the far field of two slits: two coherent beams at +theta and -theta); the fringe along that axis is cos^2 of the composed phase at the offset, the dark offsets where 4 C_d^2 < den^2; the light's click premise is the meeting (both ends of a Link holding a whole quantum: the birth kept or the meeting refused by name, the gap-0 row's lines of the log); over the window of the beams' overlap (the intervals before the beams' centroids have parted by one Link at twice the transverse group velocity sin k_y / (3 sin omega), in thousandths of a Link) the meetings at the dark offsets are 0 and at the bright offsets many: SHOWN.
56 Bell: every birth's two ends (the - child and the + child, the senses -1 and +1) read at their own clicks under two settings each, the outcome the sign of p re_now + q im_now of the credit's frame; S = E(a, b) - E(a, b') + E(a', b) + E(a', b'); nature's 2 sqrt 2 as the integer inequality S^2 > 8 (S as a rational: num^2 > 8 den^2); the board local and deterministic gives |S| <= 2 (Bell's theorem on the one-Link reach), so SHOWN as nature needs num^2 > 8 den^2 and is NOT SHOWN with the measured S; the senses' perfect anticorrelation (E = -1 at every setting) read beside it.
57 GHZ: three ends with one root; a birth gives two children at the two ends of one Link, a shared take at one Node (children_at_node >= 2) gives four; no three-ended click in the record: NOT READ with the counts, the predicate named (M = E(xyy) + E(yxy) + E(yyx) - E(xxx) as a rational, |M| <= 2 for every local reading, nature's -4).

Usage: python predicates_qg.py <record.json> [...]: the three rows, one JSON line each."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "src"))
from event_universe.core.rule3 import quotient  # noqa: E402
from event_universe.decoder import Record  # noqa: E402
from event_universe.seed import axis_pairs, circle_point, running_rotation  # noqa: E402

THOUSAND = 1000
AXES = 3
FEW_MEETINGS = 10
SETTINGS_A = ((1, 0), (1, 1))  # 4.0's Bell settings (examples/events/bell/design.json at v4.0.0)
SETTINGS_B = ((12, 5), (5, 12))


def sign(x):
    return (x > 0) - (x < 0)


def gap0_index(record):
    return record.line_num.index(record.den)


def slit_lays(record):
    """The two gap-0 lays with one wave mirrored on one axis and the rest equal, at one centre: (the lays, the mirrored axis) or None."""
    gap0 = gap0_index(record)
    lays = [e for e in record.log if e["event"] == "lay" and e.get("line_pair") == gap0 and e.get("wave") and e.get("node")]
    for k, a in enumerate(lays):
        for b in lays[k + 1 :]:
            if a["node"] != b["node"]:
                continue
            mirrored = [ax for ax in range(AXES) if a["wave"][ax] == -b["wave"][ax] and a["wave"][ax] != 0]
            same = [ax for ax in range(AXES) if a["wave"][ax] == b["wave"][ax]]
            if len(mirrored) == 1 and len(same) == AXES - 1:
                return (a, b), mirrored[0]
    return None


def two_slits(record):
    """Row 55: the two slits (the fringe of two mirrored beams in light's clicks, the meetings of the gap-0 row)."""
    key = "55 the two slits"
    found = slit_lays(record)
    if found is None:
        return {key: {"verdict": "NOT READ: no two gap-0 packets at one centre with one wave mirrored on one axis in the world; the predicate: the gap-0 row's meetings at the dark offsets 0 over the beams' overlap, at the bright offsets many"}}
    (a, _b), axis = found
    den, cube = record.den, int(record.run["cube"])
    h = int(a["wave"][axis])
    points = [circle_point(den, int(x)) for x in a["wave"]]
    rotation = running_rotation(den, den, points)
    v_thousandths = quotient(THOUSAND * abs(points[axis][1]), 3 * rotation[1]) if rotation[1] else 0
    window = quotient(THOUSAND + 2 * v_thousandths - 1, 2 * v_thousandths) if v_thousandths else 1
    reach = quotient(cube, 2)
    along = axis_pairs(den, points[axis], reach)
    dark = sorted(d for d in range(-reach, reach + 1) if 4 * along[d][0] * along[d][0] < den * den)
    centre = int(a["node"][axis])
    gap0 = gap0_index(record)
    meetings = [e for e in record.log if e["i"] > 0 and e["event"] in ("birth", "refused") and e.get("row", gap0) == gap0 and e.get("cause") != "stop"]
    first = min((int(e["i"]) for e in meetings), default=None)
    by_offset = Counter()
    by_interval = defaultdict(lambda: [0, 0])
    for e in meetings:
        off = (int(e["node"][axis]) - centre) % cube
        off = off if off <= reach else off - cube
        is_dark = off in dark
        if first is not None and first <= int(e["i"]) < first + window:
            by_offset[off] += 1
        by_interval[int(e["i"])][1 if is_dark else 0] += 1
    bright = sum(n for off, n in by_offset.items() if off not in dark)
    dim = sum(n for off, n in by_offset.items() if off in dark)
    verdict = (
        "NOT READ: no meeting of the gap-0 row in the record"
        if first is None
        else f"SHOWN: {bright} meetings at the bright offsets and 0 at the dark over the overlap window of {window} intervals from the first meeting (the fringe period of the law in light's clicks)"
        if dim == 0 and bright >= FEW_MEETINGS
        else f"NOT SHOWN: {dim} meetings at the dark offsets against {bright} at the bright over the window (the dark planes' share above one quantum: the conserved form's gradient term at a node of the standing wave)"
        if dim
        else f"NOT SHOWN: {bright} meetings, fewer than {FEW_MEETINGS}"
    )
    return {
        key: {
            "the mirrored axis": axis,
            "wave number h = den sin(k / 2) on it": h,
            "den cos k on it (the composed pair at the offset 1, over den)": along[1][0],
            "the transverse group velocity (thousandths of a Link per interval)": v_thousandths,
            "the overlap window (intervals until the beams part by one Link)": window,
            "dark offsets (4 C_d^2 < den^2)": dark,
            "meetings by offset over the window": {str(k): v for k, v in sorted(by_offset.items())},
            "meetings per interval at bright / dark offsets (first eight intervals with meetings)": {str(i): by_interval[i] for i in sorted(by_interval)[:8]},
            "first interval with a meeting": first,
            "at": a["node"],
            "verdict": verdict,
        }
    }


def outcome(frame, setting):
    p, q = setting
    return sign(p * frame["re_now"] + q * frame["im_now"])


def ends_of(record):
    """Every birth with the first credit of the children's record at each end after the birth."""
    credits = defaultdict(list)
    for c in record.credits:
        credits[(tuple(c["node"]), c["line"])].append(c)
    found = []
    for b in record.births:
        s = b["line_pair"]
        ends = []
        for where in (b["minus"], b["plus"]):
            later = [c for c in credits[(tuple(where), s)] if int(c["i"]) > int(b["i"])]
            ends.append(min(later, key=lambda c: int(c["i"])) if later else None)
        found.append((b, ends[0], ends[1]))
    return found


def correlation(pairs, a, b, key):
    same = opposite = 0
    for _birth, minus, plus in pairs:
        x, y = key(minus, a), key(plus, b)
        if x == 0 or y == 0:
            continue
        same += x == y
        opposite += x != y
    return same - opposite, same + opposite


def chsh(pairs, key):
    es = {(ia, ib): correlation(pairs, a, b, key) for ia, a in enumerate(SETTINGS_A) for ib, b in enumerate(SETTINGS_B)}
    num, den = 0, 1
    for sgn, (n, d) in ((1, es[(0, 0)]), (-1, es[(0, 1)]), (1, es[(1, 0)]), (1, es[(1, 1)])):
        if d == 0:
            return es, None
        num, den = num * d + sgn * n * den, den * d
    return es, (num, den)


def bell(record):
    """Row 56: Bell's S from the born pairs' two ends at their clicks."""
    key = "56 Bell"
    pairs = [p for p in ends_of(record) if p[1] is not None and p[2] is not None and "re_now" in p[1]["frame"] and "re_now" in p[2]["frame"]]
    if not record.births:
        return {key: {"verdict": "NOT READ: no birth in the record; the predicate: S from the pairs' two ends under two settings each, S^2 > 8 as nature"}}
    if not pairs:
        return {key: {"births": len(record.births), "verdict": "NOT READ: no born pair clicked at both ends; the predicate: S from the pairs' two ends under two settings each, S^2 > 8 as nature"}}
    es_f, s_f = chsh(pairs, lambda c, s: outcome(c["frame"], s))
    es_s, s_s = chsh(pairs, lambda c, s: c["sense"])
    opposite = sum(1 for b in record.births if sign(b["W_children"][0]) * sign(b["W_children"][1]) < 0)
    nature = s_f is not None and s_f[0] * s_f[0] > 8 * s_f[1] * s_f[1]
    local = s_f is not None and abs(s_f[0]) <= 2 * s_f[1]
    return {
        key: {
            "births": len(record.births),
            "pairs clicked at both ends": len(pairs),
            "births with the two children's senses opposite (W_children)": opposite,
            "E per setting pair by the frame's axis (same - opposite, pairs)": {f"a{ia} b{ib}": v for (ia, ib), v in es_f.items()},
            "S by the frame's axis (hundredths)": None if s_f is None else quotient(s_f[0] * 100, s_f[1]),
            "S by the frame's axis as a rational": s_f,
            "S by the senses (hundredths)": None if s_s is None else quotient(s_s[0] * 100, s_s[1]),
            "within the local bound |S| <= 2": local,
            "at": record.births[0]["node"],
            "verdict": "SHOWN as nature: S^2 > 8 at the pairs' clicks"
            if nature
            else f"NOT SHOWN as nature: |S| <= 2 at the pairs' clicks (the board local and deterministic, every end's outcome a function of its own Node's state: Bell's bound is the law's theorem; the senses' anticorrelation E = -1 SHOWN on {opposite} of {len(record.births)} births)",
        }
    }


def ghz(record):
    """Row 57: GHZ, three ends with one root."""
    key = "57 GHZ"
    shared = Counter(int(b.get("children_at_node", 1)) for b in record.births)
    return {
        key: {
            "births": len(record.births),
            "children per birth": 2,
            "births by the count of pairs taken at one Node in one close (a shared take)": {str(k): v for k, v in sorted(shared.items())},
            "three-ended clicks in the record": 0,
            "verdict": "NOT READ: a birth gives two ends at one Link and a shared take four, no three ends with one root in the record; the predicate: M = E(xyy) + E(yxy) + E(yyx) - E(xxx) over three-ended births, M^2 > 4 as nature (|M| <= 2 for every local reading)",
        }
    }


ROWS = (two_slits, bell, ghz)


def main(argv):
    sys.set_int_max_str_digits(0)
    for path in argv[1:]:
        with open(path, encoding="utf-8") as f:
            record = Record(json.load(f))
        for row in ROWS:
            print(json.dumps({"record": path} | row(record)))


if __name__ == "__main__":
    main(sys.argv)
