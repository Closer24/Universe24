"""COMPUTATION on a chain (not an engine run): the dielectric index of a block under the
coupling of MASSIVE_RECORD.md section 7, printed from the pair and the coupling before any
build; the second-difference form of the coupling (the engine's first-difference form has the
same dispersion, Reviewer 3's 12.5 (b) at 198a9bfe).

    PYTHONPATH=src python docs/designs/detector_law/massive_dielectric_index.py

The Lorentz-oscillator index of a block under the linear coupling g (verb B, the coupling
matrix [[0, g], [g, 0]] between light's row and the massive row at the block's cells): light of
frequency omega through a block of s cells whose massive record rests at omega_0; the response
n^2 - 1 = g^2 / (omega_0^2 - omega^2) in the units where both rules have c^2 = 1 / 3, read as the
transmitted phase delay on a chain against the formula.
"""

from __future__ import annotations

import math

import numpy as np

C2 = 1.0 / 3.0
G_COUPLE = 1.0  # the light side's coupling to the massive acceleration (the product G g sets the index)


def chain_run(
    length: int,
    steps: int,
    pair_m: tuple[int, int],
    g: float,
    block: range,
    omega: float,
    source: int,
    probe: int,
):
    """Two rows per Node (light a_l, the massive a_m), the leapfrog rules coupled at the block's
    cells by g (a float here; the integer pair form is the engine's), a sine source of light at
    `source`; returns light's amplitude at `probe` over time (the phase delay read from it)."""
    p, q = pair_m
    mu2 = p / q
    al = np.zeros(length)
    al_b = np.zeros(length)
    am = np.zeros(length)
    am_b = np.zeros(length)
    inside = np.zeros(length, bool)
    inside[list(block)] = True
    out = []
    for t in range(steps):
        al[source] = math.sin(omega * t)
        lap_l = np.roll(al, 1) + np.roll(al, -1) - 2 * al
        lap_m = np.roll(am, 1) + np.roll(am, -1) - 2 * am
        # THE FINDING (2026-09-23): a coupling of light's row to the massive AMPLITUDE (light: + g a_m) is
        # TACHYONIC: at k = 0 the coupled mass matrix [[0, -g], [-g, w0^2]] has a negative eigenvalue and
        # the transmitted amplitude explodes (10^4 to 10^63 in the first run of this script). The stable
        # linear coupling is the Lorentz-dielectric one: the massive row is driven by light's amplitude
        # (a_m: + g a_l) and light's row by the massive record's ACCELERATION, its second difference in
        # time (a_l: - G (a_m,next - 2 a_m + a_m,before)), both local to the cell, the order within the
        # interval: the massive step first, then light's. The dispersion then reads
        # n^2 = 1 + G g / (omega_0^2 - omega^2), the classical dielectric, and the zero mode stays a zero mode.
        am_n = np.where(inside, 2 * am - am_b + C2 * lap_m - mu2 * am + g * al, 0.0)
        accel_m = am_n - 2 * am + am_b
        al_n = 2 * al - al_b + C2 * lap_l - np.where(inside, G_COUPLE * accel_m, 0.0)
        al_n[0] = al_n[-1] = 0.0
        al_b, al = al, al_n
        am_b, am = am, am_n
        out.append(al[probe])
    return np.array(out)


def phase_delay(signal: np.ndarray, omega: float, t0: int, t1: int) -> float:
    ts = np.arange(t0, t1)
    seg = signal[t0:t1]
    c = np.sum(seg * np.cos(omega * ts))
    s = np.sum(seg * np.sin(omega * ts))
    return math.atan2(c, s)  # the phase of sin(omega t - phi): phi


def index_check(pair_m=(1, 4), g=0.05, s=12, omega=0.15):
    # the geometry keeps every end reflection out of the read window: the source at 600, the block at
    # 900, the probe at 1100 on a chain of 1400; the direct wave reaches the probe at 866, the right
    # end's reflection at 1903, the left end's at 2946; the window 900 to 1800.
    length = 1400
    source = 600
    block = range(900, 900 + s)
    probe = 1100
    steps = 1850
    ref = chain_run(length, steps, pair_m, 0.0, block, omega, source, probe)
    sig = chain_run(length, steps, pair_m, g, block, omega, source, probe)
    t0, t1 = 1000, 1800
    # phase_delay returns -phi for sin(omega t - phi): the extra delay through the block is ref - sig
    dphi = phase_delay(ref, omega, t0, t1) - phase_delay(sig, omega, t0, t1)
    dphi = (dphi + math.pi) % (2 * math.pi) - math.pi
    k = omega / math.sqrt(C2)
    n_read = 1 + dphi / (k * s)
    w0 = math.sqrt(pair_m[0] / pair_m[1])
    # the coupled dispersion of the stable form: (c^2 k^2 - omega^2) (omega_0^2 - omega^2) = G g omega^2, so
    # n^2 = 1 + G g / (omega_0^2 - omega^2), the classical dielectric (n > 1 below the resonance)
    n2 = 1 + G_COUPLE * g / (w0 * w0 - omega * omega)
    amp = float(np.max(np.abs(sig[t0:t1])) / np.max(np.abs(ref[t0:t1])))
    print(
        f"the Lorentz-oscillator index: pair {pair_m} (omega_0 = {w0:.4f}), g = {g}, s = {s}, omega = {omega}: the chain's transmitted"
        f" phase delay {dphi:+.4f} rad over {s} cells -> n = {n_read:.4f}; the formula sqrt(1 + G g / (omega_0^2 - omega^2)) ="
        f" {math.sqrt(n2):.4f}; the transmitted amplitude {amp:.3f} of the reference (the Fresnel steps at the two faces)"
    )


if __name__ == "__main__":
    for g in (0.02, 0.05, 0.1):
        index_check(g=g)
    index_check(pair_m=(1, 16), g=0.05, omega=0.15)
