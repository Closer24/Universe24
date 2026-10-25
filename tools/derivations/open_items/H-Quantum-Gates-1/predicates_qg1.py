"""The three quantum gates as predicates of the decoder's table (the hand qg1; the ledger's rows 55 to 57), one function of the Record each, in gates.py's shape: a dict with the numbers and a `verdict` of SHOWN, or NOT SHOWN or NOT READ with the cause by name. No act of the engine is touched; the record is read from the two files and the log alone.

55 the two slits: the light's clicks (the births whose taken row is the gap-0 row, at the take Node) counted per transverse row on the far plane along the wave's axis, against the law's near-field rows (the paths' difference half a wavelength by the integer comparison); the wave number from the seed's `wave` key of a gap-0 lay and the two sources from two such lays with one wave; NOT READ where the record's light carries no wave number (the sea's drift at k = 0 has no wavelength).
56 Bell: every born pair, the two children's first credits at their own Nodes; the outcomes sign(p re_now + q im_now) in the plane's own frame at the settings (1, 0), (1, 1) on the minus side and (12, 5), (5, 12) on the plus side; S = E(a, b) - E(a, b') + E(a', b) + E(a', b'); the per-pair identity in {-2, 2} bounds |S| by 2 for the four readings on one record; beside it the readers' frames as the settings (the credit's frame bit at the Port +x picks the setting at each end, four subsamples); SHOWN only where |S| exceeds 2 over at least 16 pairs.
57 GHZ: a close whose children stand at three ends; NOT SHOWN where every close has an even count of ends (two per birth).

Usage: python predicates_qg1.py <record.json> [...]; one JSON line per gate per record.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from typing import Any

from event_universe.core.rule3 import largest_below, quotient
from event_universe.decoder import Record

SETTINGS_A = ((1, 0), (1, 1))
SETTINGS_B = ((12, 5), (5, 12))
FEWEST_PAIRS = 16


def sign(x: int) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def thousandths(num: int, den: int) -> int | None:
    if den == 0:
        return None
    s = 1 if num >= 0 else -1
    return s * int(quotient(1000 * abs(num), den))


def wavelength_of(h: int, den: int) -> tuple[int, int]:
    """The wavelength in Links as a rational (num, den) from the lay's h = den sin(k / 2): lambda = 2 pi / k; read in integers as the band's cosine den cos k = (den^2 - 2 h^2) div den and the wavelength of the three lattice points cos k = 1/2 (6 Links), 0 (4), -1/2 (3), -1 (2) nearest by the cosine; (0, 1) at h = 0."""
    if h == 0:
        return (0, 1)
    cos_k = quotient(den * den - 2 * h * h, den)
    points = [(quotient(den, 2), (6, 1)), (0, (4, 1)), (-quotient(den, 2), (3, 1)), (-den, (2, 1)), (den, (0, 1))]
    return min(points, key=lambda p: abs(p[0] - cos_k))[1]


def half_rows(cube: int, length: int, y_a: int, y_b: int, lam: tuple[int, int]) -> list[int]:
    """The rows of the far plane where the two paths first differ by half a wavelength, from the midline outward, by the integer comparison on the squared paths (the torus distance)."""

    def tdist(a: int, b: int) -> int:
        d = abs(a - b)
        return min(d, cube - d)

    ln, ld = lam
    found = []
    for y in range(cube):
        s1 = length * length + tdist(y, y_a) ** 2
        s2 = length * length + tdist(y, y_b) ** 2
        if s1 < s2:
            s1, s2 = s2, s1
        left = 4 * ld * ld * (s1 - s2) - ln * ln
        if left >= 0 and left * left >= 16 * ld * ld * ln * ln * s2:
            found.append(y)
    mid = quotient(y_a + y_b, 2)
    return sorted(found, key=lambda y: min(abs(y - mid), cube - abs(y - mid)))[:2]


def two_slits(record: Record) -> dict[str, Any]:
    """Row 55: the two slits read from the light's clicks on the far plane."""
    cube = int(record.run["cube"])
    seed = record.run["world"].get("seed", [])
    gap0_rec = record.line_num.index(record.den)
    waves = [
        lay for lay in seed if lay.get("lay") == "at" and lay.get("wave") is not None and int(lay["row"]) == gap0_rec
    ]
    light_births = [b for b in record.births if int(b["taken_row"]) == gap0_rec]
    found: dict[str, Any] = {"light clicks (gap-0 takes at births)": len(light_births), "light lays with a wave": len(waves)}
    if not waves:
        found["verdict"] = (
            "NOT READ: the record's light carries no wave number (the sea's drift at k = 0 has no wavelength); the predicate: the light's clicks per row on the far plane, the midline row above the half-wavelength rows"
        )
        return found
    if len({tuple(w["wave"]) for w in waves}) != 1 or len(waves) != 2:
        found["verdict"] = "NOT READ: the two slits are two gap-0 lays with one wave; the record holds another count"
        return found
    wave = [int(x) for x in waves[0]["wave"]]
    axis = max(range(3), key=lambda a: abs(wave[a]))
    lam = wavelength_of(abs(wave[axis]), record.den)
    centres = [tuple(int(x) for x in w["centre"]) for w in waves]
    trans = [a for a in range(3) if a != axis and centres[0][a] != centres[1][a]]
    if len(trans) != 1:
        found["verdict"] = "NOT READ: the two sources part along one transverse axis"
        return found
    t = trans[0]
    other = [a for a in range(3) if a not in (axis, t)][0]
    x_s = centres[0][axis]
    y_a, y_b = centres[0][t], centres[1][t]
    mid = quotient(y_a + y_b, 2)
    # the far plane: the plane along the wave's axis beyond the sources with the most light clicks
    by_plane = Counter((int(b["node"][axis]) - x_s) % cube for b in light_births)
    beyond = [k for k in range(2, quotient(cube, 2) + 1) if by_plane.get(k, 0) > 0]
    found |= {"wavelength (Links, num/den)": list(lam), "sources": centres, "light clicks by plane beyond the sources (offset: count)": {str(k): by_plane.get(k, 0) for k in range(cube)}}
    if not beyond:
        found["verdict"] = "NOT SHOWN: no light click on any plane two or more Links beyond the sources"
        return found
    length = max(beyond, key=lambda k: by_plane[k])
    x_far = (x_s + length) % cube
    rows = [sum(1 for b in light_births if int(b["node"][axis]) == x_far and int(b["node"][t]) == y) for y in range(cube)]
    halves = half_rows(cube, length, y_a, y_b, lam)
    found |= {"far plane (offset, plane)": [length, x_far], "light clicks per transverse row on the far plane": rows, "midline row": mid, "half-wavelength rows": halves, "transverse axis": t, "the other axis": other}
    shown = bool(halves) and all(rows[mid] > rows[y] for y in halves) and rows[mid] > 0
    found["verdict"] = (
        "SHOWN: the midline row's clicks above the half-wavelength rows' on the far plane"
        if shown
        else "NOT SHOWN: the midline row's clicks not above the half-wavelength rows' on the far plane"
    )
    return found


def outcome(credit: dict[str, Any], setting: tuple[int, int]) -> int:
    f = credit["frame"]
    return sign(setting[0] * int(f["re_now"]) + setting[1] * int(f["im_now"]))


def pairs_of(record: Record) -> list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]]:
    """Every born pair with both children credited: the birth and each child's first credit at its own Node on its own plane after the birth."""
    credits = sorted(record.credits, key=lambda c: int(c["i"]))
    by_place: dict[tuple[tuple[int, ...], int], list[dict[str, Any]]] = {}
    for c in credits:
        by_place.setdefault((tuple(c["node"]), int(c["line"])), []).append(c)
    pairs = []
    for b in record.births:
        line = int(b["line_pair"])
        ends = []
        for end in ("minus", "plus"):
            later = [c for c in by_place.get((tuple(b[end]), line), []) if int(c["i"]) > int(b["i"])]
            ends.append(later[0] if later else None)
        if ends[0] is not None and ends[1] is not None:
            pairs.append((b, ends[0], ends[1]))
    return pairs


def bell(record: Record) -> dict[str, Any]:
    """Row 56: Bell's S over the born pairs' two credits."""
    pairs = pairs_of(record)
    n = len(pairs)
    found: dict[str, Any] = {"births": len(record.births), "pairs with both children credited": n}
    if n == 0:
        found["verdict"] = "NOT READ: no born pair with both children credited; the predicate: |S| above 2 over at least 16 pairs"
        return found
    sums = {(sa, sb): sum(outcome(cm, sa) * outcome(cp, sb) for _b, cm, cp in pairs) for sa in SETTINGS_A for sb in SETTINGS_B}
    s_num = sums[(SETTINGS_A[0], SETTINGS_B[0])] - sums[(SETTINGS_A[0], SETTINGS_B[1])] + sums[(SETTINGS_A[1], SETTINGS_B[0])] + sums[(SETTINGS_A[1], SETTINGS_B[1])]
    identity = Counter()
    for _b, cm, cp in pairs:
        a0, a1 = outcome(cm, SETTINGS_A[0]), outcome(cm, SETTINGS_A[1])
        b0, b1 = outcome(cp, SETTINGS_B[0]), outcome(cp, SETTINGS_B[1])
        identity[a0 * b0 - a0 * b1 + a1 * b0 + a1 * b1] += 1
    sense = sum(int(cm["sense"]) * int(cp["sense"]) for _b, cm, cp in pairs)
    # the readers' frames as the settings: the frame bit at the Port +x of each end's credit
    sub: dict[tuple[int, int], tuple[int, int]] = {}
    for _b, cm, cp in pairs:
        ka = 1 if int(cm["frame"]["frames"][0]) > 0 else 0
        kb = 1 if int(cp["frame"]["frames"][0]) > 0 else 0
        num, den = sub.get((ka, kb), (0, 0))
        sub[(ka, kb)] = (num + outcome(cm, SETTINGS_A[ka]) * outcome(cp, SETTINGS_B[kb]), den + 1)
    sub_s = None
    keys = ((0, 0), (0, 1), (1, 0), (1, 1))
    if all(sub.get(k, (0, 0))[1] for k in keys):
        d = 1
        for k in keys:
            d *= sub[k][1]
        num = sum(sgn * sub[k][0] * quotient(d, sub[k][1]) for k, sgn in zip(keys, (1, -1, 1, 1), strict=True))
        sub_s = thousandths(num, d)
    found |= {
        "E(sense) in thousandths": thousandths(sense, n),
        "E(a, b) at the four settings in thousandths": {f"{sa} {sb}": thousandths(v, n) for (sa, sb), v in sums.items()},
        "S as a rational [num, pairs]": [s_num, n],
        "S in thousandths": thousandths(s_num, n),
        "per-pair identity (value: count)": {str(k): v for k, v in identity.items()},
        "settings by the readers' frames: subsample counts": {f"{k}": v[1] for k, v in sub.items()},
        "settings by the readers' frames: E per subsample (thousandths)": {f"{k}": thousandths(v[0], v[1]) for k, v in sub.items()},
        "settings by the readers' frames: S (thousandths)": sub_s,
        "classical bound 2, nature's 2 sqrt 2 in thousandths": [2000, largest_below(8 * 1000 * 1000)],
    }
    if n < FEWEST_PAIRS:
        found["verdict"] = f"NOT SHOWN: {n} pairs, fewer than {FEWEST_PAIRS}; |S| = {abs(s_num)} / {n} at most 2 by the per-pair identity"
    elif abs(s_num) > 2 * n:
        found["verdict"] = "SHOWN: |S| above 2"
    else:
        found["verdict"] = "NOT SHOWN: |S| at most 2 by the per-pair identity (the four readings on the same two credit lines); nature's 2 sqrt 2 unreachable by any reading of the record"
    return found


def ghz(record: Record) -> dict[str, Any]:
    """Row 57: a close with three ends."""
    by_close = Counter((int(b["i"]), tuple(b["node"])) for b in record.births)
    ends = Counter(2 * v for v in by_close.values())
    odd = sum(v for k, v in ends.items() if k % 2)
    found = {"ends per take Node and close (ends: closes)": {str(k): v for k, v in sorted(ends.items())}, "closes with an odd count of ends": odd}
    found["verdict"] = (
        "NOT SHOWN: every close an even count of ends, two per birth; a three-end close needs the conversion (N-S6), not in the engine"
        if not odd
        else "a three-end close exists: the three readings owed"
    )
    return found


TABLE = {"55 the two slits": two_slits, "56 Bell": bell, "57 GHZ": ghz}


def main() -> None:
    for path in sys.argv[1:]:
        record = Record(json.loads(open(path).read()))
        print(json.dumps({"record": path, "intervals": record.intervals}))
        for name, row in TABLE.items():
            print(json.dumps({name: row(record)}, default=str))


if __name__ == "__main__":
    main()
