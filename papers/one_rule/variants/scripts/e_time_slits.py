"""E. The time slits in the law's algebra (README.md, section E; docs/ALGEBRA.md, the band's line, The
click writes on the lattice (5), the two-quadrature line): two laid packets of light separated along a
chain by d Links, the second the first's copy, stepped by Rule3's line for light at the vacuum's paces in
real arithmetic with the engine's coefficients (core.rule3.coefficients; y and z folded, cos omega = (2 +
cos k) / 3), read at a far Node by a body's two quadratures over the window, X = SUM_t a_t cos(omega_d t),
Y = SUM_t a_t sin(omega_d t), the plane's size squared P^2 = X^2 + Y^2 (the body's turn over its window),
for a row of bodies' resonances omega_d across the band: the single packet's P^2 the envelope, the two
packets' P^2 the envelope times 4 cos^2(k(omega_d) d / 2), the beats nature's frequency fringes (Tirole et
al. 2023).

    PYTHONPATH=src python papers/one_rule/variants/scripts/e_time_slits.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.rule3 import coefficients  # noqa: E402

OUT = HERE.parent / "out"
GAMMA = 6000  # the shipped universes' Node clock
PAIR = (6000, 6000)  # light's pair
CHAIN, PROBE, INTERVALS = 1200, 400, 700
EDGE, COLUMN, SEPARATION = 8, 200, 60  # the packets 17 Nodes long, d = 60 Links apart
WAVELENGTH = 8  # k = pi / 4, the gates' wave
HALF_SPAN, POINTS = 0.25, 201  # the resonances read, about the carrier


def line_light() -> tuple[float, float]:
    """Rule3's coefficients for light at the vacuum's paces over the wall: R / w per Port, S / w."""
    reads, self_coefficient, wall = coefficients(*PAIR, GAMMA, GAMMA, GAMMA)
    return reads[0] / wall, self_coefficient / wall


def raised_cosine(n: int, top: tuple[int, int], edge: int) -> np.ndarray:
    at = np.arange(n)
    away = np.maximum(np.maximum(top[0] - at, at - top[1]), 0)
    taper = (1 + np.cos(np.pi * np.minimum(away, edge) / edge)) / 2
    return np.where(away == 0, 1.0, np.where(away <= edge, taper, 0.0))


def lay(
    n: int, k: float, omega: float, column: int, edge: int, amplitude: float, shift: int = 0
) -> tuple[np.ndarray, np.ndarray]:
    """A packet along the chain at the wave number k moving toward +x: now = A e cos(k x), before = A e
    cos(k x + omega) (the level before the level now turned back by the band's rotation: a wave moving
    toward +x); with `shift` d the packet's copy d Links behind, psi(x + d) with its carrier's phase cos(k
    (x + d)), the same packet laid d Links earlier along the beam (two laid packets separated in time by d
    / v_g)."""
    x = np.arange(n).astype(float)
    e = raised_cosine(n, (column - shift, column - shift), edge)
    return amplitude * e * np.cos(k * (x + shift)), amplitude * e * np.cos(k * (x + shift) + omega)


def stepped(
    now: np.ndarray, before: np.ndarray, read: float, self_over_wall: float, intervals: int, probe: int
) -> np.ndarray:
    """The chain stepped in real arithmetic (y and z folded: four of the six arrivals are the Node itself),
    the open x faces far away; the level at the probe Node per interval."""
    trace = np.zeros(intervals + 1)
    for t in range(intervals + 1):
        trace[t] = now[probe]
        if t == intervals:
            break
        arrivals = 4 * now
        arrivals[1:] += now[:-1]
        arrivals[:-1] += now[1:]
        nxt = read * arrivals + self_over_wall * now - before
        before, now = now, nxt
    return trace


def quadratures(trace: np.ndarray, omega_d: float) -> float:
    t = np.arange(len(trace))
    x = float((trace * np.cos(omega_d * t)).sum())
    y = float((trace * np.sin(omega_d * t)).sum())
    return x * x + y * y


def main() -> None:
    read, self_over_wall = line_light()
    k = 2 * math.pi / WAVELENGTH
    # the band, 2 w cos omega = S + 2 SUM_a R_a cos k_a, one term per axis, the folded axes at k = 0:
    # cos omega = S / (2 w) + (R / w) (cos k + 2); the group pace (R / w) sin k / sin omega
    cos_omega = read * (math.cos(k) + 2) + self_over_wall / 2
    omega = math.acos(cos_omega)
    v_g = read * math.sin(k) / math.sin(omega)
    d = SEPARATION
    a1 = lay(CHAIN, k, omega, COLUMN, EDGE, 1000.0)
    a2 = lay(CHAIN, k, omega, COLUMN, EDGE, 1000.0, shift=d)  # the first's copy, d / v_g later
    single = stepped(a1[0].copy(), a1[1].copy(), read, self_over_wall, INTERVALS, PROBE)
    double = stepped(a1[0] + a2[0], a1[1] + a2[1], read, self_over_wall, INTERVALS, PROBE)
    tau = d / v_g
    grid = np.linspace(omega - HALF_SPAN, omega + HALF_SPAN, POINTS)
    p1 = np.array([quadratures(single, w) for w in grid])
    p2 = np.array([quadratures(double, w) for w in grid])
    ratio = p2 / np.where(p1 > 1e-9 * p1.max(), p1, np.nan)
    # the second packet is the first's copy d Links behind, so every mode of the record carries the factor
    # 1 + e^(-i k d) with k the band's wave number at the body's frequency, cos k = 3 cos omega_d - 2: the
    # beats 4 cos^2(k(omega_d) d / 2), the fringe spacing in omega 2 pi / tau at the carrier
    k_of = np.arccos(np.clip(3 * np.cos(grid) - 2, -1, 1))
    beats = 4 * np.cos(k_of * d / 2) ** 2
    good = p1 > 0.02 * p1.max()
    minima = [
        float(grid[i])
        for i in range(1, len(grid) - 1)
        if p2[i] < p2[i - 1] and p2[i] < p2[i + 1] and good[i]
    ]
    zeros = sorted(
        math.acos((2 + math.cos(kz)) / 3)
        for kz in ((2 * m + 1) * math.pi / d for m in range(d))
        if kz <= math.pi and grid[0] <= math.acos((2 + math.cos(kz)) / 3) <= grid[-1]
    )
    report = {
        "band": {
            "k": k,
            "cos_omega": cos_omega,
            "omega": omega,
            "v_g": v_g,
            "period_intervals": 2 * math.pi / omega,
        },
        "packets": {"length_nodes": 2 * EDGE + 1, "separation_links": d, "tau_arrival_intervals": tau},
        "fringe_spacing_in_omega_2pi_over_tau": 2 * math.pi / tau,
        "single_P2_peak_at": float(grid[p1.argmax()]),
        "double_P2_minima": [round(m, 4) for m in minima],
        "beats_zeros_k(omega)d=(2m+1)pi": [round(z, 4) for z in zeros],
        "ratio_P2double_over_P2single_vs_4cos2": [
            {
                "omega_d": round(float(w), 4),
                "ratio": round(float(r), 3),
                "4cos^2(k d/2)": round(float(b), 3),
                "P2single_rel": round(float(e), 4),
            }
            for w, r, b, e in zip(grid[::5], ratio[::5], beats[::5], p1[::5] / p1.max(), strict=True)
            if not np.isnan(r) and e > 0.02
        ],
        "max_abs_ratio_minus_beats_where_envelope_above_2pc": float(
            np.nanmax(np.abs(ratio[good] - beats[good]))
        ),
        "envelope_width_above_2pc_in_omega": float(grid[good].max() - grid[good].min()),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "e_time_slits.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
