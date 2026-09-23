"""COMPUTATION on a chain (not an engine run): the block's clock in motion,
Reviewer 3's C8 (PUSH_BALANCE.md section 12.2 at f5752667) on an independent
chain, and the one closed form of MASSIVE_RECORD.md section 8.

    PYTHONPATH=src python docs/designs/detector_law/massive_block_clock_motion.py A block of s cells lowers the massive gap by g (mu^2 -> mu^2 - g);
the chain rule (Reviewer 3's H, stable in one dimension):
    a_next + a_before = (1/3)(a_{j-1} + a_{j+1}) + (4/3 - mu^2 + g_j) a_now.
The block's lowest mode at rest is the largest eigenvector of the one-interval
map (the smallest eigenvalue of H); then the cells are stepped by an accumulator
(one Link every k intervals after a ramp), and the clock is read at the block's
co-moving centre by the spectral peak (Hann window, parabolic interpolation).
The closed form checked against the reading: f/f0 = omega_b(gamma s, g) /
(gamma omega_b(s, g)), the moving block a resting block of width gamma s with
the same g, its phase read at 1/gamma (the boost of the continuum's operator).
"""

import numpy as np
from scipy.linalg import eigh_tridiagonal

MU = 0.05
C = 1 / np.sqrt(3)


def rest_mode(n, s, g, mu=MU):
    """The lowest mode of H on a chain of n cells with the block centred."""
    gj = np.zeros(n)
    lo = n // 2 - s // 2
    gj[lo : lo + s] = g
    d = mu**2 - gj + 2 / 3
    e = -np.ones(n - 1) / 3
    lam, vec = eigh_tridiagonal(d, e, select="i", select_range=(0, 0))
    lam = lam[0]
    omega = 2 * np.arcsin(np.sqrt(max(lam, 0)) / 2)
    v = vec[:, 0]
    v /= np.abs(v).max()
    return omega, v, lam


def read_peak(series, dt=1.0):
    x = series - series.mean()
    w = np.hanning(len(x))
    n = 1 << (int(np.ceil(np.log2(len(x)))) + 3)
    F = np.abs(np.fft.rfft(x * w, n))
    i = np.argmax(F[1:]) + 1
    y0, y1, y2 = np.log(F[i - 1]), np.log(F[i]), np.log(F[i + 1])
    di = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
    return 2 * np.pi * (i + di) / (n * dt)


def moving_block(s, g, k=3, ramp=1500, hold=8000, mu=MU):
    n = 7000
    omega0, v, lam = rest_mode(n, s, g, mu)
    # the block's cells: an integer position stepped by an accumulator
    lo0 = n // 2 - s // 2
    # initial two levels from the mode at rest: a(t) = v cos(omega t)
    a_before = v * np.cos(-omega0)
    a_now = v.copy()
    acc = 0
    pos = 0
    centre = []
    # the ramp: the hop period from very slow to k, then hold at k
    T = ramp + hold
    for t in range(T):
        # the accumulator: rate r/T_k with the period falling linearly during the ramp
        period = k + (k * 20 - k) * max(0.0, 1 - t / ramp)  # from 60 intervals per Link down to k
        acc += 1.0
        if acc >= period:
            acc -= period
            pos += 1
        gj = np.zeros(n)
        lo = lo0 + pos
        gj[lo : lo + s] = g
        nb = np.roll(a_now, 1) + np.roll(a_now, -1)
        a_next = nb / 3 + (4 / 3 - mu**2 + gj) * a_now - a_before
        a_before, a_now = a_now, a_next
        if t >= ramp:
            centre.append(a_now[lo + s // 2])
    om = read_peak(np.array(centre))
    return omega0, om, pos


gam = 1 / np.sqrt(1 - (1 / 3) ** 2 / C**2)
print(
    f"k = 3: beta = 1/3, c = {C:.4f}, gamma_m = {gam:.4f}, 1/gamma_m = {1 / gam:.4f}, 1/gamma_m^2 = {1 / gam**2:.4f}"
)
print(
    "s | g | eps at rest | f/f0 READ (chain, spectral peak) | closed form omega_b(gamma s, g)/(gamma omega_b(s, g)) | Reviewer 3's reading"
)
r3 = {
    (1, 0.0183): 0.7949,
    (12, 0.5 * MU**2): 0.8060,
    (12, MU**2): 0.7796,
    (24, MU**2): 0.7461,
    (48, MU**2): 0.7107,
}
for s, g in [(1, 0.0183), (12, 0.5 * MU**2), (12, MU**2), (24, MU**2), (48, MU**2)]:
    om0, om, pos = moving_block(s, g)
    eps = 1 - om0**2 / MU**2
    # the closed form: the resting block of width gamma s (real width: interpolate between integers)
    sw = gam * s
    s1, s2 = int(np.floor(sw)), int(np.ceil(sw))
    o1 = rest_mode(7000, s1, g)[0]
    o2 = rest_mode(7000, s2, g)[0]
    ob = o1 + (o2 - o1) * (sw - s1) if s2 > s1 else o1
    closed = ob / (gam * om0)
    print(
        f"{s:2d} | {g:.5f} | {eps:.3f} | {om / om0:.4f} | {closed:.4f} | {r3[(s, g)]:.4f}   (travelled {pos} Links)"
    )
print(
    "the well limit of the closed form is 1/gamma_m (omega_b independent of s), the cavity limit 1/gamma_m^2 (omega_b proportional to 1/s)"
)
