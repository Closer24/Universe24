"""The census: windings per swing measured on the committed act, and every number the act makes, with its Gamma-form.

usage: python3 -I census.py > census.txt

1. Windings of the matter hand per swing (its phase advance, atan2 of (re, im) summed tick by tick, over one swing
   from the bang to the next bottom), against w sqrt(Gamma/2) (the hand's beat w times the swing's 2 pi sqrt(Gamma/2)
   over 2 pi, slowed by N = e^-U along the swing): a power of Gamma times the declared w.
2. The hierarchy the act implies at the 7b gearing, derived on paper from the act's coefficients (the time gear's
   s grip / W = 1/6, D / W = 2 / Gamma, push per quantum q = 2 tan(w/2) per tick, measured through the swing's depth):
   the static load of one quantum, c(r) = 6 q G(r), G(r) -> 1/(4 pi r); the rate shift U = c / Gamma read by a second
   quantum as the redshift of its energy hbar w; so V(r) = (6 / 4 pi) hbar q w / (Gamma r) and, with light's speed
   c0 = 1/sqrt 6, alpha_g = G m^2 / (hbar c) = (6 sqrt 6 / 4 pi) q w / Gamma ~ 1.17 w^2 / Gamma.  With the swing's
   N_t = w sqrt(Gamma / 2) beats of the quantum per swing: alpha_g N_t^2 = 0.585 w^4 (q -> w), no Gamma in it.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py

import rig  # noqa: E402

from tensor24.engine import step  # noqa: E402
from tensor24.runner.load import ruler_of  # noqa: E402


def windings(gamma: int, off: int, n: Fraction):
    layout, s, info = rig.matter_hand(gamma, n, pinion_off=off)
    allowed = np.ones((1, 1), dtype=object)
    row = layout.ruler.row
    prev = math.atan2(int(s.a[1, 0]), int(s.a[0, 0]))
    counts, phases = [0], [0.0]
    period = 2 * math.pi * math.sqrt(gamma / 2)
    for _t in range(1, int(1.5 * period)):
        s, _ = step.tick(layout, s, allowed)
        ang = math.atan2(int(s.a[1, 0]), int(s.a[0, 0]))
        phases.append(phases[-1] + (ang - prev + math.pi) % (2 * math.pi) - math.pi)
        prev = ang
        counts.append(int(s.a[row, 0]))
    half = int(period / 2)
    low = min(counts[half:])  # the next bottom: the least load in the swing's second half and after
    t = half + counts[half:].index(low)
    return info, abs(phases[t]) / (2 * math.pi), t, max(counts[: t + 1])


def main() -> None:
    out = ["The census of the act's numbers (tensor24-review's committed act)", ""]
    out.append(
        "1. Windings of the matter hand per swing (n = 1 quantum per Node-clock), against w sqrt(Gamma/2)"
    )
    for gamma in (250, 1000, 4000):
        for off in (50, 1000):
            info, wind, ticks, top = windings(gamma, off, Fraction(1))
            pred = info["w"] * math.sqrt(gamma / 2)
            out.append(
                f"   Gamma {gamma:5d}, w = {info['w']:.4f}, n = {info['quanta_per_node']:.2f}: {wind:.3f} windings in the "
                f"{ticks} ticks from the bang to the next bottom (top U {top / gamma:.3f}); w sqrt(Gamma/2) = {pred:.3f}, ratio {wind / pred:.3f}"
            )
    out.append("")
    out.append("2. The hierarchy implied at the 7b gearing (derived on paper; the static probe owed)")
    q_measured = (
        0.217  # U_top per quantum at w = 0.2003 (swing.txt, part A, Gamma 250 to 4000), = q per tick
    )
    w = math.acos(1 - 1 / 50)
    for gamma in (1000,):
        a_g = 6 * math.sqrt(6) / (4 * math.pi) * q_measured * w / gamma
        out.append(
            f"   at Gamma {gamma}, w = {w:.4f}: alpha_g = (6 sqrt6 / 4 pi) q w / Gamma = {a_g:.3e} (q = {q_measured}, measured); "
            f"1.17 w^2 / Gamma = {1.17 * w * w / gamma:.3e}"
        )
    a_e, a_p = 1.751e-45, 5.906e-39
    out.append(
        f"   Gamma that nature's electron hierarchy {a_e} would need: 1.17 w_e^2 / alpha_g = {1.17 / a_e:.2e} w_e^2;"
        f" the proton's {a_p}: {1.17 / a_p:.2e} w_p^2"
    )
    age, h = 4.35e17, 6.62607015e-34
    me, mp, c = 9.1093837e-31, 1.67262192e-27, 2.99792458e8
    for name, a, m in (("electron", a_e, me), ("proton", a_p, mp)):
        n_t = age / (h / (m * c * c))
        out.append(
            f"   nature, {name}: N_t = age / (h / m c^2) = {n_t:.2e}; alpha_g N_t^2 = {a * n_t * n_t:.2e}, "
            f"against the act's 0.585 w^4 <= 0.585 pi^4 = {0.585 * math.pi**4:.0f}"
        )
    out.append("")
    out.append(
        "3. Every number of the act at Gamma 1000, with its Gamma-form (den, key and the pinions excluded: the file's)"
    )
    g = 1000
    ruler = ruler_of(g)
    R = ruler[-1] / g
    rows = [
        (
            "rotations; kinds; tables; table entries",
            "24; 5 (dims 1,1,2,3,3); 43 of 125; +-1, +-2",
            "none",
        ),
        ("the Spokes; light's speed squared; W/grip", "6; 1/6; 12", "none"),
        (
            "the ruler's length L",
            f"{len(ruler)}",
            "(Gamma/2) ln(2 Gamma) + O(sqrt Gamma), exact closed form",
        ),
        (
            "the massive beat's slowing at the horizon Y_last/Gamma",
            f"{R:.3f}",
            "sqrt(2 Gamma)(1 + O(Gamma^-1/2))",
        ),
        ("light's slowing / the cone's width e^(2U) at the horizon", f"{R * R:.1f}", "2 Gamma"),
        ("the inertia's range Z_last / Z_0", f"{R**4:.4g}", "4 Gamma^2"),
        (
            "the swing's period in ticks",
            f"{2 * math.pi / math.acos(1 - 1 / g):.2f}",
            "2 pi sqrt(Gamma/2)",
        ),
        (
            "gravity's reach (the time gear's Yukawa range) in Meshes",
            f"{math.sqrt(g / 12):.2f}",
            "sqrt(Gamma/12) = c0 P / 2 pi",
        ),
        (
            "the mesh unit G; T / den",
            f"16; {6 * g * g * 256:.4g}",
            "~ sqrt(Gamma)/2; 6 Gamma^2 G^2 ~ (3/2) Gamma^3",
        ),
        ("the swing's depth per quantum per Node-clock", "0.217 (w = 0.2003)", "2 tan(w/2): no Gamma"),
        (
            "the runaway threshold n_crit (quanta per Node-clock)",
            "5.7 (w = 0.2003)",
            "~ ln(w sqrt(Gamma/2)) / (2 tan(w/2))",
        ),
        (
            "the runaway's factor per swing F",
            "8.504e7 (w = 0.2003)",
            "~ Gamma^2.4, and the pinion's (2.8e5 to 4.1e8 over w)",
        ),
        (
            "the time gear's exact return (whole swings)",
            "1 to 117",
            "erratic in (Gamma, v0): a discretized rotation",
        ),
        ("windings of a quantum per swing", "4.5 (w = 0.2003)", "w sqrt(Gamma/2)"),
    ]
    for name, value, form in rows:
        out.append(f"   {name}: {value}  [{form}]")
    print("\n".join(out))


if __name__ == "__main__":
    main()
