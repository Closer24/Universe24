"""Section 22 of DERIVATIONS_BEAM.md: the uncertainty relation from the six
verbs. Host arithmetic; no run.

(A) The support bound on the circle Z_N (Donoho and Stark): a record
    vector f in Z[Z_N] supported on s phases has an evaluation at the
    N-th roots supported on at least N / s of them; checked by
    enumeration at N = 64 on the register's records (a single phase, an
    antiphase pair, a run of s phases).
(B) The Weyl relation on Z_N: the shift U and the phase multiplication V
    satisfy U V = omega V U with omega the primitive N-th root; the
    finite form of the commutator, exact.
(C) The single opening (A10's geometry: w = 27 Nodes one Link apart, the
    screen L = 108 Links behind, 161 pixels, the wavelength lambda = c x
    8 with c = 32 / 55): the Fraunhofer array factor's full width at half
    maximum in s = sin theta, and the exact near-field sum over the 27
    emitters at L = 108 (the Fresnel number w^2 / (lambda L) = 1.45),
    both as w x FWHM / lambda against Nairz's 0.886.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path

N = 64
C = 32 / 55
LAMBDA = 8 * C
W = 27
L = 108


def support_bound(f: list[complex]) -> tuple[int, int]:
    n = len(f)
    fhat = [sum(f[x] * cmath.exp(-2j * math.pi * k * x / n) for x in range(n)) for k in range(n)]
    supp_f = sum(1 for v in f if abs(v) > 1e-9)
    supp_fhat = sum(1 for v in fhat if abs(v) > 1e-9)
    return supp_f, supp_fhat


def fwhm(xs: list[float], ys: list[float]) -> float:
    peak = max(ys)
    i = ys.index(peak)
    half = peak / 2
    left = i
    while left > 0 and ys[left] > half:
        left -= 1
    right = i
    while right < len(ys) - 1 and ys[right] > half:
        right += 1

    def cross(a: int, b: int) -> float:
        return xs[a] + (half - ys[a]) * (xs[b] - xs[a]) / (ys[b] - ys[a])

    return cross(right - 1, right) - cross(left, left + 1)


def main() -> None:
    out = ["(A) The support bound on Z_64: |supp f| x |supp f_hat| >= 64"]
    records = {
        "one phase (a row of one label)": [1 if x == 0 else 0 for x in range(N)],
        "an antiphase pair (the cancel)": [1 if x == 0 else (-1 if x == 32 else 0) for x in range(N)],
        "a run of 8 phases": [1 if x < 8 else 0 for x in range(N)],
        "a run of 16 phases": [1 if x < 16 else 0 for x in range(N)],
        "every 8th phase (a comb of 8)": [1 if x % 8 == 0 else 0 for x in range(N)],
    }
    for name, f in records.items():
        a, b = support_bound([complex(v) for v in f])
        out.append(
            f"  {name:<34} |supp f| = {a:<3} |supp f_hat| = {b:<3} product {a * b} (>= 64: {a * b >= 64})"
        )

    out.append("")
    out.append(
        "(B) The Weyl relation on Z_N: (V U - omega U V) applied to every basis vector, the largest entry"
    )
    omega = cmath.exp(2j * math.pi / N)
    worst = 0.0
    for x in range(N):
        e = [1 if y == x else 0 for y in range(N)]
        v_e = [omega**y * e[y] for y in range(N)]
        uv = [v_e[(y - 1) % N] for y in range(N)]
        u_e = [e[(y - 1) % N] for y in range(N)]
        vu = [omega**y * u_e[y] for y in range(N)]
        worst = max(worst, max(abs(omega * uv[y] - vu[y]) for y in range(N)))
    out.append(
        f"  max |V U - omega U V| = {worst:.1e}: the finite commutator exact (U the shift by one phase, V the multiplication by omega^y)"
    )

    out.append("")
    out.append(
        f"(C) The single opening: w = {W} Nodes, lambda = 8 c = {LAMBDA:.3f} Links, the screen at L = {L}"
    )
    fresnel = W * W / (LAMBDA * L)
    out.append(f"  the Fresnel number w^2 / (lambda L) = {fresnel:.2f}")
    ss = [i / 4000 - 0.5 for i in range(4001)]
    far = []
    for s in ss:
        d = math.sin(math.pi * s / LAMBDA)
        far.append(1.0 if abs(d) < 1e-12 else (math.sin(math.pi * W * s / LAMBDA) / (W * d)) ** 2)
    f_far = fwhm(ss, far)
    out.append(
        f"  Fraunhofer (the array factor): FWHM in sin theta {f_far:.4f}, w x FWHM / lambda = {W * f_far / LAMBDA:.3f} (Nairz 0.886)"
    )
    ys = list(range(-80, 81))
    near = []
    for y in ys:
        amp = sum(
            cmath.exp(2j * math.pi * math.hypot(L, y - e) / LAMBDA) / math.hypot(L, y - e)
            for e in range(-(W // 2), W // 2 + 1)
        )
        near.append(abs(amp) ** 2)
    s_pix = [y / math.hypot(L, y) for y in ys]
    f_near = fwhm(s_pix, near)
    out.append(
        f"  the exact sum over the 27 emitters at L = 108 (161 pixels): FWHM in sin theta {f_near:.4f}, w x FWHM / lambda = {W * f_near / LAMBDA:.3f}"
    )
    out.append(
        f"  the fan's grain: 47 directions with a + |b| <= 12 give a spacing of about {1 / 12:.3f} in s near the axis, {(1 / 12) / f_far:.1f} of the FWHM; a fan of 1423 by angle about {1 / 380:.4f}"
    )
    out.append("  the register's crowd-form reading at w = 27: 1.08 (NATURE row 10, kept as history)")
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
