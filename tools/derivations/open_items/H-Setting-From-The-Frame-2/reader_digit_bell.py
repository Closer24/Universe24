"""The standing comparison beside the hand's reading: the Reader's row 56 form on reader-5 (predicates.bell: the setting a digit pair (p, q) of the reader, the outcome sign(p re_now + q im_now) of the frame, every pair read under every setting pair, S = e0 - e1 + e2 + e3 over n pairs with e the same less opposite counts), re-spelled here on the same pairs the hand's reader finds, integers only. Usage: python reader_digit_bell.py <record.json> [...]"""

import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
sys.set_int_max_str_digits(0)

from bell_setting import pairs_of  # noqa: E402

SETTINGS = ((1, 0), (1, 1), (4, 3), (3, 4))  # the Reader's (p, q) on reader-5, two per end
PAIR = 2


def frames_of(record, pairs):
    credits = [e for e in record["log"] if e["event"] == "credit"]
    found = []
    for p in pairs:
        ends = []
        for end in ("minus", "plus"):
            d = p[end]
            c = next(c for c in credits if int(c["i"]) == d["i"] and c["node"] == d["node"])
            ends.append(c["frame"])
        found.append(ends)
    return found


for path in sys.argv[1:]:
    record = json.load(open(path, encoding="utf-8"))
    pairs = pairs_of(record)
    frames = frames_of(record, pairs)
    e = []
    for p, q in SETTINGS[:PAIR]:
        for r, t in SETTINGS[PAIR:]:
            same = opposite = 0
            for m, n in frames:
                u = (p * m["re_now"] + q * m["im_now"]) * (r * n["re_now"] + t * n["im_now"])
                same += u > 0
                opposite += u < 0
            e.append(same - opposite)
    s, n = e[0] - e[1] + e[2] + e[3], len(pairs)
    band = "band" if 4 * n * n < s * s <= 8 * n * n else "at 4" if s * s == 4 * n * n else "below 4"
    print(path.split("/")[-1], "pairs", n, "e (same - opposite) per setting pair", e, "S", [s, n], "S^2", [s * s, n * n], band)
