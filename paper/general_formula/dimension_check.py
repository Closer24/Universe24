"""The bodies one hollow allows, by dimension: the energy of a body of M quanta of the matter pair [4000, 6000] at the width R under the binding row [5760, 6000] at the divisor 2, Gamma 6,000, on a chain, a plane and a box, from Rule3's band (the pressure), the row's static kernel (the well) and the conformal line (the well's effect on the rotation, the level once in the clock and twice on the Link); a body where the energy has its minimum at a width of one Link or more with the well under the horizon Gamma / 2, a cloud where the minimum lies at the largest width, a collapse where the well at the minimum passes the horizon."""

import math

import numpy as np

NUM, DEN = 4000, 6000
NB, DB, E = 5760, 6000, 2
GAMMA = 6000
WIDTHS = [1.0, 1.4, 2, 2.8, 4, 5.7, 8, 11, 16, 23]


def energy(d: int, M: int, N: int, R: float) -> tuple[float, float]:
    """The energy of a Gaussian body of width R and its well's peak."""
    ks = [2 * np.pi * np.fft.fftfreq(N) for _ in range(d)]
    grid = np.meshgrid(*ks, indexing="ij")
    cos_sum = sum(np.cos(k) for k in grid)
    kernel_k = 3 * DB / (NB * 2 * (d - cos_sum) + 6 * (DB - NB))
    coords = np.meshgrid(*[np.arange(N) - N // 2 for _ in range(d)], indexing="ij")
    r2 = sum(c.astype(float) ** 2 for c in coords)
    phi = np.exp(-r2 / (2 * R * R))
    phi /= np.sqrt((phi**2).sum())
    rho = phi**2
    well = np.real(np.fft.ifftn(kernel_k * np.fft.fftn(rho))) * M / E
    weaken = np.clip(1 - 2 * well / GAMMA, 0, None) ** 2
    pressure = 0.0
    for axis in range(d):
        diff = phi - np.roll(phi, 1, axis)
        pressure += float(np.sum(diff**2 * weaken)) * (NUM / (3 * DEN))
    gain = 2 * (1 - (1 - well / GAMMA) ** 2) * (DEN - NUM) / DEN
    return M * pressure - 0.5 * M * float(np.sum(rho * gain)), float(well.max())


def kind(d: int, M: int, N: int) -> tuple[str, float, float]:
    """The body's kind at M: a body, a cloud or a collapse, with its width and its well."""
    curve = [(R, *energy(d, M, N, R)) for R in WIDTHS]
    R, F, peak = min(curve, key=lambda t: t[1])
    if R == WIDTHS[-1] or F >= 0:
        return "cloud", R, peak
    if peak > GAMMA / 2:
        return "collapse", R, peak
    return "body", R, peak


if __name__ == "__main__":
    for d, N, Ms in (
        (1, 4096, (50, 100, 200, 500, 1000, 1200, 1500, 2000)),
        (2, 256, (1000, 2000, 2500, 3000, 4000, 5000, 6000, 7000, 8000, 10000)),
        (3, 64, (10000, 20000, 25000, 28000, 29000, 30000, 31000, 32000, 35000, 40000)),
    ):
        rows = [(M, *kind(d, M, N)) for M in Ms]
        bodies = [M for M, k, _, _ in rows if k == "body"]
        window = f"{min(bodies)} to {max(bodies)}" if bodies else "none"
        print(f"d = {d}: bodies at M {window}")
        for M, k, R, peak in rows:
            print(f"   M {M:>6}: {k:8} width {R:>4} Links, the well's peak {peak:7.0f}")
