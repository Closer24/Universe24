"""The ruler's length L(Gamma) walked by the engine's own runner/load.ruler_of, for many Gamma, against a closed form.

usage: python3 -I ruler.py > ruler.txt, at tensor24-review 8a476db17, the head it was made at (its calls into src are that head's)

Derivation chain (nothing fitted): ruler_of walks the hollow side p0(c) = round(Gamma (1 - 1/Gamma)^c) (exact carries,
Gamma^3 at the resolution Gamma^2) and stops at the first c where round(p0^2 / Gamma) = 0, i.e. 2 p0^2 < Gamma (half
up).  So the last count is the last c with p0(c) >= m, m = ceil(sqrt(Gamma / 2)), i.e. Gamma (1-1/Gamma)^c >= m - 1/2:
    L(Gamma) = 1 + floor( ln(Gamma / (m - 1/2)) / -ln(1 - 1/Gamma) )            (closed form, a prediction)
and since -1/ln(1-1/G) = G - 1/2 - 1/(12 G) ..., ln(G/(m-1/2)) = (1/2) ln(2G) - delta, |delta| <~ 1/sqrt(2G):
    L(Gamma) = (Gamma/2) ln(2 Gamma) + O(sqrt Gamma).
The probe can fail: any Gamma where the walk differs from the closed form by more than 1 (the carries' drift).
Also printed, per Gamma, every dimensionless number the clocks make from Gamma and the six Spokes alone.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "src"))  # the worktree's committed act

from tensor24.runner.load import mesh_unit, ruler_of  # noqa: E402

SPOKES = 6


def closed(gamma: int) -> int:
    m = math.isqrt(gamma // 2)
    while 2 * m * m < gamma:  # least m with 2 m^2 >= Gamma
        m += 1
    return 1 + math.floor(math.log(gamma / (m - 0.5)) / -math.log1p(-1.0 / gamma))


def main() -> None:
    out = []
    out.append(
        "The ruler's length L(Gamma) from runner/load.ruler_of (tensor24-review), against the closed form"
    )
    out.append("")
    gammas = list(range(3, 401)) + [
        500,
        600,
        700,
        800,
        900,
        918,
        930,
        1000,
        1001,
        1024,
        2000,
        4096,
        6000,
        10000,
        20000,
        50000,
        100000,
    ]
    worst = 0
    rows = []
    for g in gammas:
        ruler = ruler_of(g)
        n = len(ruler)
        c = closed(g)
        worst = max(worst, abs(n - c))
        rows.append((g, n, c, ruler))
    out.append(
        f"Gamma 3..400 and 17 larger: {len(gammas)} values; largest |walk - closed form| = {worst}"
    )
    out.append("")
    hdr = (
        "Gamma",
        "L walk",
        "L closed",
        "(G/2)ln(2G)",
        "L/G",
        "Y_last/G",
        "(Y_last/G)^2",
        "2G",
        "(Y_last/G)^4",
        "G mesh_unit",
        "T/den=6G^2g^2",
        "P=2pi/w_t",
        "L/P",
    )
    out.append(" | ".join(hdr))
    for g, n, c, ruler in rows:
        if g > 12 and g not in (16, 32, 64, 100, 128, 250, 256) and g < 500:
            continue
        y = Fraction(ruler[-1], g)
        gu = mesh_unit(g)
        w_t = math.acos(
            1 - 1 / g
        )  # the time gear's pinion den - den div Gamma at a large den: cos w = 1 - 1/Gamma
        p = 2 * math.pi / w_t
        out.append(
            " | ".join(
                [
                    f"{g}",
                    f"{n}",
                    f"{c}",
                    f"{g / 2 * math.log(2 * g):.1f}",
                    f"{n / g:.4f}",
                    f"{float(y):.4f}",
                    f"{float(y * y):.1f}",
                    f"{2 * g}",
                    f"{float(y**4):.4g}",
                    f"{gu}",
                    f"{SPOKES * g * g * gu * gu:.4g}",
                    f"{p:.3f}",
                    f"{n / p:.2f}",
                ]
            )
        )
    out.append("")
    # the residual against the leading asymptotic form: should be O(sqrt Gamma), oscillating
    out.append("Residual L - (Gamma/2) ln(2 Gamma), over sqrt(Gamma):")
    for g, n, _c, _ruler in rows:
        if g in (10, 50, 100, 200, 400, 1000, 2000, 4096, 6000, 10000, 20000, 50000, 100000):
            res = n - g / 2 * math.log(2 * g)
            out.append(
                f"   Gamma {g}: L = {n}, residual {res:.1f}, residual / sqrt(Gamma) = {res / math.sqrt(g):.3f}"
            )
    out.append("")
    # the law's frozen load at Gamma = 6000 (ALGEBRA.md: 28,206 at Gamma 6,000, about (Gamma/2) ln(2 Gamma) = 28,178)
    six = [r for r in rows if r[0] == 6000][0]
    out.append(
        f"Cross-check with the law: Gamma 6,000 walks {six[1]} counts (last {six[1] - 1}); the law's 28,206 "
        f"(another rate line, R208) and (Gamma/2) ln(2 Gamma) = {6000 / 2 * math.log(12000):.0f}"
    )
    out.append("")
    # what Gamma would make each clock number equal nature's 1836.15: a fit of Gamma, not a derivation (tries counted)
    out.append(
        "Tries against nature's m_p/m_e = 1836.15267 (each a choice of Gamma, i.e. a fit; listed to count them):"
    )
    target = 1836.15267
    for name, f in (
        ("L(Gamma)", lambda r: len(r[3])),
        ("L(Gamma)/2", lambda r: len(r[3]) / 2),
        ("(Y_last/Gamma)^2 (light's slowing at the horizon)", lambda r: (r[3][-1] / r[0]) ** 2),
        ("2 pi sqrt(Gamma/2) (the period)", lambda r: 2 * math.pi * math.sqrt(r[0] / 2)),
    ):
        best = min((abs(f(r) - target), r[0], f(r)) for r in rows if r[0] <= 100000)
        out.append(
            f"   {name}: nearest over the {len(rows)} Gammas listed is Gamma {best[1]} giving {best[2]:.2f}"
        )
    print("\n".join(out))


if __name__ == "__main__":
    main()
