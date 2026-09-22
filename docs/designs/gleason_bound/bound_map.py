"""Host arithmetic on the tables for BOUND.md (the Gleason Bound Mathematician,
2026-09-22): the N = 64 tables as integers, the referee's example, the sum
lemma's numbers, and the weight of a mixture the register's Malus reading
cannot exclude. No run; every number is GAMEBOARD by formula unless it is
quoted from the register (DETECTOR, with its line). Run from the repository
root: `.venv/bin/python docs/designs/gleason_bound/bound_map.py`."""

from __future__ import annotations

import math
from fractions import Fraction

from event_universe.core.phase import phase_cosines, phase_sines

SCALE = 256


def exact_tables(n: int) -> tuple[list[int], list[int]]:
    """round(256 cos(2 pi p / n)), round(256 sin(2 pi p / n)) by the host's floats."""
    c = [round(SCALE * math.cos(2 * math.pi * p / n)) for p in range(n)]
    s = [round(SCALE * math.sin(2 * math.pi * p / n)) for p in range(n)]
    return c, s


def pointer(rows: dict[int, int], c: list[int], s: list[int]) -> tuple[int, int]:
    """X = sum f_p C[p], Y = sum f_p S[p] over the rows {phase: amount}."""
    n = len(c)
    return (sum(a * c[p % n] for p, a in rows.items()), sum(a * s[p % n] for p, a in rows.items()))


def exact_pointer(rows: dict[int, int], n: int) -> tuple[float, float]:
    """256 ev(f) by the host's floats."""
    return (
        sum(a * SCALE * math.cos(2 * math.pi * p / n) for p, a in rows.items()),
        sum(a * SCALE * math.sin(2 * math.pi * p / n) for p, a in rows.items()),
    )


def main() -> None:
    print(
        "1. THE ENGINE'S TABLES AGAINST round(256 cos), round(256 sin), EVERY POWER OF TWO N FROM 4 TO 65536"
    )
    worst = 0
    for k in range(2, 17):
        n = 2**k
        c, s = list(phase_cosines(n)), list(phase_sines(n))
        ce, se = exact_tables(n)
        bad = sum(1 for p in range(n) if c[p] != ce[p] or s[p] != se[p])
        norm = [c[p] ** 2 + s[p] ** 2 for p in range(n)]
        worst = max(worst, max(abs(v - SCALE**2) for v in norm))
        print(
            f"   N = {n:5d}: entries differing from the exact rounding {bad}; "
            f"C^2 + S^2 in [{min(norm)}, {max(norm)}]"
        )
    print(f"   the largest |C^2 + S^2 - 65536| over these N: {worst}")

    n = 64
    c, s = list(phase_cosines(n)), list(phase_sines(n))
    print()
    print("2. THE TABLES AT N = 64 AS INTEGERS (the scale 256; the entry p is at 2 pi p / 64)")
    print("   C[0..63] =", " ".join(str(v) for v in c))
    print("   S[0..63] =", " ".join(str(v) for v in s))
    print("   C[8] = S[8] =", c[8], " (256 cos(pi / 4) = 256 / sqrt 2 =", f"{SCALE / math.sqrt(2):.5f})")
    print(
        "   the norms C[p]^2 + S[p]^2 take the values",
        sorted(set(c[p] ** 2 + s[p] ** 2 for p in range(n))),
    )

    print()
    print("3. THE REFEREE'S EXAMPLE: f = 256 x^8 - 181 (1 + x^16) AT N = 64")
    print("   after the cancel x^32 = -1 the rows are 256 at the phase 8, 181 at 32, 181 at 48")
    rows = {8: 256, 32: 181, 48: 181}
    total = sum(abs(a) for a in rows.values())
    for shift, name in (
        (0, "as written"),
        (8, "rotated by 8 steps (x^8 f)"),
        (1, "rotated by 1 step (x f)"),
    ):
        r = {(p + shift) % n: a for p, a in rows.items()}
        x, y = pointer(r, c, s)
        xe, ye = exact_pointer(r, n)
        terms = ", ".join(f"{a} x ({c[p]}, {s[p]})" for p, a in sorted(r.items()))
        print(f"   {name}: rows {dict(sorted(r.items()))}; the terms {terms}")
        print(
            f"      tables: (X, Y) = ({x}, {y}), R = X^2 + Y^2 = {x * x + y * y}, R / 65536 = {(x * x + y * y) / 65536:.5f}"
        )
        print(
            f"      exact:  256 ev = ({xe:.4f}, {ye:.4f}), R* = {xe * xe + ye * ye:.4f}, R* / 65536 = {(xe * xe + ye * ye) / 65536:.6f}"
        )
        print(
            f"      the pointer's error ({x - xe:+.4f}, {y - ye:+.4f}); the lemma's bound A / 2 = {total / 2} per component (A = {total})"
        )
    xe, ye = exact_pointer(rows, n)
    r_star = xe * xe + ye * ye
    print(
        f"   |ev(f)|^2 exactly, the tables' scale as the unit = (256 - 181 sqrt 2)^2 = {(256 - 181 * math.sqrt(2)) ** 2:.6f}"
        f" = R* / 65536 (the referee's 0.00075); the tables read 0, 196 / 65536 = 0.00299 and 25028 / 65536 = 0.38190 at the three rotations"
    )
    print(
        f"   lemma 3's bound on |R - R*|: A sqrt(2 R*) + A^2 / 2 = {total * math.sqrt(2 * r_star):.1f} + {total * total / 2:.1f}"
        f" = {total * math.sqrt(2 * r_star) + total * total / 2:.1f}; the readings' errors 49.0 and 147.0 lie inside it"
    )
    print(
        "   hypothesis (a), R(x f) = R(f), on the built click at this f: R(f) = 0, R(x^8 f) = 196, R(x f) = 25028; the exact R* = 49.005 is one number at every rotation"
    )

    print()
    print(
        "4. THE SUM LEMMA ON THE PAPER'S SUMS (k terms of magnitude up to M: the pointer off by at most k M / 2 per component)"
    )
    print(
        "   one row (k = 1, M = 1): |R - 65536| <= 256 sqrt 2 + 1 / 2 = 362.5 by lemma 3; the tables' extreme at N = 64 is 237 (65773 - 65536)"
    )
    print(
        "   the aligned record of total amount A: relative error of R at most sqrt 2 / 256 + 1 / 131072 = "
        f"{math.sqrt(2) / 256 + 1 / 131072:.5f} (a part in {1 / (math.sqrt(2) / 256 + 1 / 131072):.0f})"
    )
    print(
        "   the Mach-Zehnder's dark port (k = 2, phases D = 32 apart, equal M): the sum is exactly 0 by C[p + 32] = -C[p], S[p + 32] = -S[p]:",
        all(c[p + 32] == -c[p] and s[p + 32] == -s[p] for p in range(32)),
    )
    print(
        "   the quarter turn (k = 2, D = 16, equal M): R = M^2 ((C[p] + C[p+16])^2 + (S[p] + S[p+16])^2), over p in [",
        min((c[p] + c[(p + 16) % n]) ** 2 + (s[p] + s[(p + 16) % n]) ** 2 for p in range(n)),
        ",",
        max((c[p] + c[(p + 16) % n]) ** 2 + (s[p] + s[(p + 16) % n]) ** 2 for p in range(n)),
        "] against the exact 131072",
    )
    print(
        "   a cancelling sum (the referee's k = 3, M = 256): no relative bound; the absolute bound A / 2 = 309 per component covers a reading of 0"
    )

    print()
    print(
        "5. MALUS AT 22.5 DEGREES ON THE HALF-ANGLE TABLES (2N = 512 AT N = W = 256; malus_map.out section 2), BY HARMONIC j"
    )
    c2, s2 = list(phase_cosines(512)), list(phase_sines(512))
    window = 32  # 22.5 degrees on the 512-circle
    wheel = 256
    print(
        "   j | C'[32 j] | S'[32 j] | plus weight C'^2 | minus weight S'^2 | the pass x 256 / (C'^2 + S'^2) | the rung's count of 256"
    )
    weights = {}
    for j in range(1, 32, 2):
        cj, sj = c2[(window * j) % 512], s2[(window * j) % 512]
        plus, minus = cj * cj, sj * sj
        tot = plus + minus
        count = (2 * wheel * plus + tot) // (2 * tot)
        weights[j] = (plus, minus, tot)
        print(
            f"   {j:2d} | {cj:4d} | {sj:4d} | {plus:5d} | {minus:5d} | {Fraction(256 * plus, tot)} = {256 * plus / tot:.3f} | {count}"
        )
    plus1, minus1, tot = weights[1]
    plus3 = weights[3][0]
    assert all(weights[j][2] == tot for j in weights)
    assert all(weights[j][0] == plus1 for j in weights if j % 8 in (1, 7))
    assert all(weights[j][0] == plus3 for j in weights if j % 8 in (3, 5))
    print(
        f"   the classes: j = +-1 mod 8 read the plus weight {plus1}, j = +-3 mod 8 read {plus3}; the total {tot} for every j"
    )
    # The mixture (1 - w) on the class +-1 (any spread), w on the class +-3 (any spread): the cumulative plus weight
    # plus1 - w (plus1 - plus3); the rung's count stays 219 iff 512 C + tot >= 219 x 2 tot.
    pinned = 219  # DETECTOR: A12 at 22.5 degrees, record 395; paper main.tex lines 1208 and 1261
    boundary = Fraction(pinned * 2 * tot - tot, 2 * wheel)
    w_star = (plus1 - boundary) / (plus1 - plus3)
    print(
        f"   the built Born number 256 x {plus1} / {tot} = {256 * plus1 / tot:.4f}; the exact cos^2(22.5 deg) x 256 = {256 * math.cos(math.pi / 8) ** 2:.4f}; the pinned count {pinned} (DETECTOR)"
    )
    print(
        f"   the rung keeps {pinned} iff the plus weight >= {boundary} = {float(boundary):.3f}, a margin of {float(plus1 - boundary):.3f} on the weight ({256 * float(plus1 - boundary) / tot:.4f} of a cell)"
    )
    print(
        f"   the shift per unit weight w on the class +-3: {plus1 - plus3} on the weight, {256 * (plus1 - plus3) / tot:.2f} cells of 1 / 256"
    )
    print(
        f"   w* (the polariser) = {w_star} = {float(w_star):.6f} = 1 / {1 / float(w_star):.0f}: above it the reading is 218, not 219; below it the reading is 219"
    )
    # The chain (malus_map.out section 4): the cell 0+ weight is plus^2 for the member, the total tot^2.
    tot2 = tot * tot
    chain_pinned = 187  # DETECTOR: A12's chain, record 395; DERIVATIONS_BEAM 24.3 row 4
    boundary2 = Fraction(chain_pinned * 2 * tot2 - tot2, 2 * wheel)
    w_chain = (Fraction(plus1 * plus1) - boundary2) / (plus1 * plus1 - plus3 * plus3)
    print(
        f"   the chain's cell 0+: Born {plus1**2} of {tot2} (256 x = {256 * plus1**2 / tot2:.4f}, the pinned {chain_pinned}); the class +-3 {plus3**2};"
        f" w* (the chain) = {float(w_chain):.6f} = 1 / {1 / float(w_chain):.0f}"
    )
    print(
        f"   the margin-free bound (a shift of one whole cell, whatever the margin): w = {tot} / ({(plus1 - plus3)} x 256) = {tot / ((plus1 - plus3) * 256):.6f} = 1 / {(plus1 - plus3) * 256 / tot:.1f}"
    )
    print(
        "   the class +-1 mod 8 (j = 7, 9, 15, 17, 23, 25, 31): the same weights as j = 1 at 22.5, 45 and 90 degrees; Malus bounds nothing on it"
    )

    print()
    print(
        "6. THE TWO-SLIT BANDS (L2b; DETECTOR: the bright pixels 19 to 51 clicks of 4096 births, the rungs within one; paper main.tex line 1204)"
    )
    peak = 51
    print(
        "   the member j reads 1 + cos(2 pi j D / 64) where Born reads 1 + cos(2 pi D / 64); a weight w on j != 1 moves a pixel's count by at most"
    )
    print(
        f"   w x |cos(j t) - cos(t)| x (peak / (1 + V)) <= 2 w x {peak} / 1.966 = {2 * peak / 1.966:.1f} w clicks (V = 0.966 the registered visibility); one click is the cell, so"
    )
    print(
        f"   a change of one whole click needs w >= 1 / {2 * peak / 1.966:.1f} = {1.966 / (2 * peak):.4f}; below that the bands cannot be relied on to exclude it (the pixels' margins not read here)"
    )


if __name__ == "__main__":
    main()
