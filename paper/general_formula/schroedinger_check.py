"""Schroedinger's equation as the slow limit of Rule3's line: the packet check of S.63.

A Gaussian packet of a matter family is stepped by the line without the remainder on a chain
with the two other axes folded (four reads on the Node itself, two axial Ports), laid with the
exact band's before level so that every component is advanced by its own rotation. Its envelope's
centre and rms width after T intervals are printed beside Schroedinger's with the band's inertia
m* = 3 tan omega_0 (the group velocity k_0 / m*, the spread a(T)^2 = a^2 + (T / (2 m* a))^2 for the
density's width a = sigma_0 / sqrt 2, sigma_0 the amplitude's) and beside the exact band's group
velocity. Real arithmetic, no run of the engine, no file read.

    python paper/general_formula/schroedinger_check.py
"""

from __future__ import annotations

import math

import numpy as np


def main(
    num: int = 2,
    den: int = 3,
    nodes: int = 4000,
    sigma_0: float = 40.0,
    k_0: float = 0.08,
    steps: int = 3000,
) -> None:
    c_0 = num / (3 * den)
    omega_0 = math.acos(num / den)
    inertia = 3 * math.tan(omega_0)
    x = np.arange(nodes) - nodes // 2
    k = 2 * np.pi * np.fft.fftfreq(nodes)
    omega = np.arccos(c_0 * (2 + np.cos(k)))  # the band along the axis, the folded axes at k = 0
    spectrum = np.fft.fft(np.exp(-((x / sigma_0) ** 2) / 2) * np.exp(1j * k_0 * x))
    now = np.real(np.fft.ifft(spectrum))
    before = np.real(np.fft.ifft(spectrum * np.exp(1j * omega)))  # every component one rotation earlier
    for _ in range(steps):
        following = c_0 * (4 * now + np.roll(now, 1) + np.roll(now, -1)) - before
        before, now = now, following
    envelope = np.abs(np.fft.ifft(np.fft.fft(now) * (k > 0) * 2))  # the analytic signal's modulus
    density = envelope**2
    centre = float((x * density).sum() / density.sum())
    width = math.sqrt(float(((x - centre) ** 2 * density).sum() / density.sum()))
    density_width_0 = sigma_0 / math.sqrt(2)  # the density's rms width at the start
    predicted_width = density_width_0 * math.sqrt(1 + (steps / (2 * inertia * density_width_0**2)) ** 2)
    group = c_0 * math.sin(k_0) / math.sin(math.acos(c_0 * (2 + math.cos(k_0))))
    print(f"the pair [{num}, {den}]: omega_0 = {omega_0:.4f}, m* = 3 tan omega_0 = {inertia:.4f}")
    print(
        f"after {steps} intervals the envelope's centre is {centre:.1f} Links against Schroedinger's"
        f" k_0 T / m* = {k_0 * steps / inertia:.1f} and the exact band's group velocity times T = {group * steps:.1f}"
    )
    print(
        f"the density's rms width is {width:.2f} Links against Schroedinger's {predicted_width:.2f}"
        f" (from {density_width_0:.2f} at the start)"
    )


if __name__ == "__main__":
    main()
