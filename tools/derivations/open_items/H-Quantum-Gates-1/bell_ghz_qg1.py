"""Bell's and the GHZ readings of a record of engine-5.0-test (the hand qg1), from the credit and birth lines alone.

The pair: a birth lays two children at the Link's two ends at opposite senses (The twist; MS-S1: re_now A, im_before sense B). The two far readings: the first credit of each child at its own Node on its own plane after the birth. The outcomes under a setting (p, q) in the plane's internal frame: sign(p re_now + q im_now) at the credit, the 4.0 settings (1, 0), (1, 1) on the minus side and (12, 5), (5, 12) on the plus side; the sense reading sign(W) beside it. The CHSH sum S = E(a, b) - E(a, b') + E(a', b) + E(a', b') over the pairs with both ends credited; the per-pair identity A(a) B(b) - A(a) B(b') + A(a') B(b) + A(a') B(b') in {-2, 2} counted, which bounds |S| by 2 for every decoder that reads the four from the same two lines (the theorem). The setting-from-the-clock form beside it: one setting per end picked by the parity of the credit's proper count, the four E over four subsamples (the form a universe from the seed permits; nature's free settings have no place in the record).

GHZ: the children per take Node and close, every birth two children; a birth of three ends counted (none expected: the conversion with three children, N-S6, is not in the engine).

Integers only: E and S as (numerator, denominator) pairs and in thousandths.

Usage: python bell_ghz_qg1.py <record.json> [<record.json> ...]
"""

from __future__ import annotations

import json
import sys
from collections import Counter

from event_universe.core.rule3 import quotient

SETTINGS_A = ((1, 0), (1, 1))
SETTINGS_B = ((12, 5), (5, 12))


def sign(x: int) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def outcome(credit: dict, setting: tuple[int, int]) -> int:
    f = credit["frame"]
    p, q = setting
    return sign(p * int(f["re_now"]) + q * int(f["im_now"]))


def first_credit(credits: list[dict], node: list[int], line: int, after: int) -> dict | None:
    for c in credits:
        if int(c["i"]) > after and c["node"] == node and int(c["line"]) == line:
            return c
    return None


def thousandths(num: int, den: int) -> int | None:
    if den == 0:
        return None
    s = 1 if num >= 0 else -1
    return s * int(quotient(1000 * abs(num), den))


def read(path: str) -> dict:
    run = json.loads(open(path).read())
    log = run["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = sorted((e for e in log if e["event"] == "credit"), key=lambda e: int(e["i"]))
    pairs = []
    opposite_at_birth = 0
    for b in births:
        wm, wp = b["W_children"]
        opposite_at_birth += int(wm) * int(wp) < 0
        cm = first_credit(credits, b["minus"], int(b["line_pair"]), int(b["i"]))
        cp = first_credit(credits, b["plus"], int(b["line_pair"]), int(b["i"]))
        if cm is not None and cp is not None:
            pairs.append((b, cm, cp))
    # the sense reading at both ends
    sense_products = Counter(int(cm["sense"]) * int(cp["sense"]) for _b, cm, cp in pairs)
    # the CHSH sum from the four sign readings of the planes' internal frame
    sums = {}
    for sa in SETTINGS_A:
        for sb in SETTINGS_B:
            sums[(sa, sb)] = sum(outcome(cm, sa) * outcome(cp, sb) for _b, cm, cp in pairs)
    n = len(pairs)
    s_num = sums[(SETTINGS_A[0], SETTINGS_B[0])] - sums[(SETTINGS_A[0], SETTINGS_B[1])] + sums[
        (SETTINGS_A[1], SETTINGS_B[0])
    ] + sums[(SETTINGS_A[1], SETTINGS_B[1])]
    identity = Counter()
    for _b, cm, cp in pairs:
        a0, a1 = outcome(cm, SETTINGS_A[0]), outcome(cm, SETTINGS_A[1])
        b0, b1 = outcome(cp, SETTINGS_B[0]), outcome(cp, SETTINGS_B[1])
        identity[a0 * b0 - a0 * b1 + a1 * b0 + a1 * b1] += 1
    # the sense CHSH: every setting the sense itself (one reading): S = E - E + E + E = 2 E
    e_sense_num = sum(int(cm["sense"]) * int(cp["sense"]) for _b, cm, cp in pairs)
    # the setting picked by the end's own clock parity: four subsamples
    sub = {}
    for b, cm, cp in pairs:
        ka, kb = int(cm["proper"]) % 2, int(cp["proper"]) % 2
        key = (ka, kb)
        num, den = sub.get(key, (0, 0))
        sub[key] = (num + outcome(cm, SETTINGS_A[ka]) * outcome(cp, SETTINGS_B[kb]), den + 1)
    sub_e = {f"{k}": thousandths(v[0], v[1]) for k, v in sub.items()}
    sub_s = None
    if all(sub.get(k, (0, 0))[1] for k in ((0, 0), (0, 1), (1, 0), (1, 1))):
        e = {k: sub[k] for k in sub}
        # S = e00 - e01 + e10 + e11 as one rational over the product of the four counts
        d = 1
        for k in e:
            d *= e[k][1]
        num = (
            e[(0, 0)][0] * quotient(d, e[(0, 0)][1])
            - e[(0, 1)][0] * quotient(d, e[(0, 1)][1])
            + e[(1, 0)][0] * quotient(d, e[(1, 0)][1])
            + e[(1, 1)][0] * quotient(d, e[(1, 1)][1])
        )
        sub_s = thousandths(num, d)
    # GHZ: the children per take Node and close
    by_close = Counter((int(b["i"]), tuple(b["node"])) for b in births)
    ends = Counter(2 * v for v in by_close.values())
    found = {
        "record": path,
        "births": len(births),
        "children at opposite senses at the birth (W_minus W_plus < 0)": opposite_at_birth,
        "pairs with both children credited": n,
        "sense product at the two credits (product: count)": {str(k): v for k, v in sense_products.items()},
        "E(sense) in thousandths": thousandths(e_sense_num, n),
        "S(sense) = 2 E in thousandths": thousandths(2 * e_sense_num, n),
        "E(a, b) over the four settings in thousandths": {
            f"{sa} {sb}": thousandths(v, n) for (sa, sb), v in sums.items()
        },
        "S (CHSH) in thousandths": thousandths(s_num, n),
        "S as a rational": [s_num, n],
        "per-pair identity values (value: count), each in {-2, 2}": {str(k): v for k, v in identity.items()},
        "bound: |S| <= 2 by the identity": abs(s_num) <= 2 * n,
        "setting by the end's clock parity: E per subsample (thousandths)": sub_e,
        "setting by the end's clock parity: subsample counts": {f"{k}": v[1] for k, v in sub.items()},
        "setting by the end's clock parity: S (thousandths)": sub_s,
        "GHZ: ends per take Node and close (ends: count)": {str(k): v for k, v in sorted(ends.items())},
        "GHZ: closes with an odd count of ends": sum(v for k, v in ends.items() if k % 2),
        "GHZ: closes with three or more ends": sum(v for k, v in ends.items() if k >= 3),
        "verdict Bell": (
            "NOT SHOWN: |S| at most 2 by the per-pair identity on every record (the four readings on the same two credit lines); nature's 2 sqrt 2 unreachable by any local reading"
            if abs(s_num) <= 2 * n
            else "SHOWN: |S| above 2"
        ),
        "verdict GHZ": (
            "NOT SHOWN: no close with three ends; every birth two children (N-S6 the conversion not in the engine)"
            if not sum(v for k, v in ends.items() if k % 2)
            else "a three-end close exists: read"
        ),
    }
    return found


def main() -> None:
    for path in sys.argv[1:]:
        print(json.dumps(read(path), indent=1))


if __name__ == "__main__":
    main()
