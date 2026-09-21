"""Section 17 of DERIVATIONS_BEAM.md: the law above Newton and Einstein,
the theorem of covariant readings. Host arithmetic; no run.

(A) Einstein's 1905 argument run with the law's Doppler (1 -+ beta) and
    with the covariant one gamma (1 -+ beta).
(B) The dispersion: today's v = p / (m + p / c) against the covariant
    v = p c^2 / E, and both against Newton's v = p / m: the order of the
    departure in v / c.
(C) The energy accumulator dE = c^2 p . dp / E integrated from rest under
    pushes: E^2 - p^2 c^2 stays E_0^2 (the invariant kept without a root).
(D) The proper-time clock E_0 / E: the muon of J4; the Doppler per turn
    gamma (1 - n . beta).
"""

from __future__ import annotations

import math
from pathlib import Path

C = 1 / math.sqrt(3)  # Links per interval


def gamma(beta: float) -> float:
    return 1 / math.sqrt(1 - beta * beta)


def main() -> None:
    out = []
    out.append("(A) Einstein 1905: a body at rest emits two pulses of energy L / 2 forward and back")
    for beta in (0.2148, 0.4297):
        g = gamma(beta)
        lattice = 0.5 * (1 - beta) + 0.5 * (1 + beta)
        cov = 0.5 * g * (1 - beta) + 0.5 * g * (1 + beta)
        out.append(
            f"  beta {beta:.4f}: the pulses' energy in the moving frame over L: the law's Doppler {lattice:.4f}"
            f" (the difference 0: no inertia lost), the covariant {cov:.4f} = gamma (the difference"
            f" {cov - 1:.4f} L = (gamma - 1) L: the inertia lost L / c^2)"
        )

    out.append("")
    out.append("(B) The dispersion in the units of section 4.4 (m = Q S M, the cap 1 Link per interval)")
    out.append("p / m    today p/(m+p)   covariant p/sqrt(m^2+p^2)   Newton p/m")
    for r in (0.25, 1.0, 3.0, 9.0):
        out.append(f"{r:<8} {r / (1 + r):<15.3f} {r / math.sqrt(1 + r * r):<27.3f} {r:.3f}")
    out.append("the departure from Newton's p = m v at small v / c:")
    out.append("v / c    today p = m v / (1 - v/c): excess   covariant p = gamma m v: excess")
    for b in (0.05, 0.1, 0.2):
        out.append(f"{b:<8} {1 / (1 - b) - 1:<38.4f} {gamma(b) - 1:.4f}")

    out.append("")
    out.append("(C) The energy accumulator under pushes: dE = c^2 p . dp / E (midpoint), from rest")
    m = 1.0
    e0 = m * C * C
    for steps, dp in ((4000, 1e-4), (40000, 1e-5)):
        e, p = e0, 0.0
        for _ in range(steps):
            p_mid = p + dp / 2
            e_mid = e + C * C * p_mid * dp / (2 * e)
            e += C * C * p_mid * dp / e_mid
            p += dp
        inv = e * e - C * C * p * p
        v = p * C * C / e
        out.append(
            f"  {steps} steps of dp = {dp}: p / (m c) = {p / (m * C):.3f}, E / E_0 = {e / e0:.6f}"
            f" (gamma {gamma(v / C):.6f}), v / c = {v / C:.6f}, (E^2 - c^2 p^2) / E_0^2 - 1 = {inv / e0**2 - 1:.2e}"
        )

    out.append("")
    out.append("(D) The proper-time clock E_0 / E = 1 / gamma, and the count per turn")
    for beta in (0.4297, 0.8594):
        g = gamma(beta)
        out.append(
            f"  beta {beta:.4f}: gamma {g:.4f}; the muon's 64th turn at tick {64 * g:.1f} (lorentz-v1: 71, 126);"
            f" the count per turn head-on gamma (1 + beta) = {g * (1 + beta):.4f}, behind {g * (1 - beta):.4f},"
            f" across gamma = {g:.4f}; today's per interval 1 + beta = {1 + beta:.4f}, {1 - beta:.4f}, 1"
        )
    out.append(
        f"  E = h f and E = m c^2 as one E at rest: h (n / d) = Q S c^2 = Q S / 3 ({64 / 3:.3f} at Q = 64, S = 1)"
    )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
