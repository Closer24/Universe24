"""COMPUTATION (not an engine run): the pins of the two matter-wave rows (DECLARATIONS.md
section 12; SCHEDULE.md rows M1 and M2), on the model owner's word of 2026-09-23 and the
Boss's decision of 23:32Z, with Reviewer 3's read of 00:05Z folded: a lamp of the MATTER
family (the kind [800, 809], mu = 0.15) at x = 20 on a 128 x 128 x 1 layer, x open (zero
faces), sends a stock of records, each a train at the declared omega above omega_0,
through two openings in a mirror line at x = 40; the screen at x = 104 clicks once per
record.

The band (ALGEBRA.md 8.1): cos omega = cos omega_0 cos omega_l(k), along a direction
(cos theta, sin theta) in the plane cos omega_l(k) = (cos(k cos theta) + cos(k sin theta)
+ 1) / 3. Printed:
  (a) DE BROGLIE (K): for the declared omega the wavenumber k on the axis, lambda_dB = 2 pi
      / k, and the screen's maxima on the declared geometry by the two-source sum with the
      band's k PER RAY DIRECTION (the anisotropy of the band, Reviewer 3's line D; the
      one-k sum beside), exact, no far-field step; the expected counts per Node at the
      declared stock of records and the statistic that puts the side maximum at its Node
      (Reviewer 3's MUST B);
  (b) THE ENERGY OF A MOVING MASS (K in the form): the group pace v_g = d omega / dk at
      that k on the axis, the direct front's transit from the lamp to the screen's centre,
      and its FIRST CLICK by the linear map of the massive rule on a chain (a switched-on
      train, the rung at a fraction of the steady amplitude; Reviewer 3's MUST C); the
      inertia m = k / v_g as the band's number in the form of a moving mass (not nature's
      gamma m at this k); the rest limit m -> 3 tan omega_0 and the identity m c_eff^2 =
      omega_0 EXACTLY at the kind's own cone (E = m c^2 a derivation; the ratio omega_0 /
      (m c^2) = c_eff^2 / c^2 is row A's two-pace ratio, no new prediction; line E).

    PYTHONPATH=src python docs/designs/detector_law/matter_wave_pins.py
"""

import math

import numpy as np

NUM, DEN = 800, 809
OMEGA_0 = math.acos(NUM / DEN)
C2 = 1 / 3
C = math.sqrt(C2)


def omega_of_k(k, theta=0.0):
    cx, sy = math.cos(theta), math.sin(theta)
    return math.acos((NUM / DEN) * (math.cos(k * cx) + math.cos(k * sy) + 1) / 3)


def k_of_omega(omega, theta=0.0, lo=1e-6, hi=math.pi - 1e-6):
    for _ in range(200):
        mid = (lo + hi) / 2
        if omega_of_k(mid, theta) < omega:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def group_pace(k, theta=0.0, h=1e-6):
    return (omega_of_k(k + h, theta) - omega_of_k(k - h, theta)) / (2 * h)


def screen_pattern(omega, d, length, half_width, per_direction):
    """The two-source sum on the screen at distance `length` from the openings at y = +-
    d / 2: |e^{i k1 r1} / sqrt r1 + e^{i k2 r2} / sqrt r2|^2 per screen Node, k_i the band's
    wavenumber at omega along each ray (per_direction) or the axis's k for both."""
    ys = np.arange(-half_width, half_width + 1)
    k_axis = k_of_omega(omega)
    amp = np.zeros(len(ys), complex)
    for y0 in (d / 2, -d / 2):
        dy = ys - y0
        r = np.hypot(length, dy)
        if per_direction:
            ks = np.array([k_of_omega(omega, math.atan2(abs(v), length)) for v in dy])
        else:
            ks = np.full(len(ys), k_axis)
        amp += np.exp(1j * ks * r) / np.sqrt(r)
    return ys, np.abs(amp) ** 2


def maxima_of(ys, pat):
    return [int(ys[i]) for i in range(1, len(ys) - 1) if pat[i] > pat[i - 1] and pat[i] >= pat[i + 1]]


def chain_first_rung(omega, x_source, x_probe, train_periods, wheels, n=400, steps=600):
    """M2 in the click's own form (Reviewer 3's line A): the massive rule on an open chain
    with a lamp at x_source inserting a train of `train_periods` periods (a hard level
    sin(omega t) for the train, then off; the record's NORM the squared motion it inserts),
    a detector at x_probe whose POINTER accumulates the record's offer there (the motion
    squared); the click is the first rung, pointer x W >= norm. Returns the click's
    interval from the birth per wheel W, and the record's transit by the group pace."""
    a_now = np.zeros(n)
    a_bef = np.zeros(n)
    ratio = NUM / DEN
    train = int(round(train_periods * 2 * math.pi / omega))
    norm = 0.0
    offer = np.empty(steps)
    prev_probe = 0.0
    for t in range(steps):
        if t < train:
            a_now[x_source] = math.sin(omega * t)
            norm += (math.sin(omega * (t + 1)) - math.sin(omega * t)) ** 2
        s6 = np.zeros(n)
        s6[1:-1] = a_now[:-2] + a_now[2:] + 4 * a_now[1:-1]
        a_next = ratio * s6 / 3 - a_bef
        a_next[0] = 0.0
        a_next[-1] = 0.0
        if t < train:
            a_next[x_source] = math.sin(omega * (t + 1))
        offer[t] = (a_next[x_probe] - prev_probe) ** 2
        prev_probe = a_next[x_probe]
        a_bef, a_now = a_now, a_next
    clicks = {}
    for w in wheels:
        pointer = 0.0
        clicks[w] = None
        for t in range(steps):
            pointer += offer[t]
            if pointer * w >= norm:
                clicks[w] = t
                break
    return train, clicks


if __name__ == "__main__":
    print(
        f"the matter family [{NUM}, {DEN}]: omega_0 = {OMEGA_0:.5f}; the rest limit m = 3 tan omega_0 = {3 * math.tan(OMEGA_0):.5f};"
        f" c_eff^2 / c^2 = cos omega_0 (omega_0 / sin omega_0) = {(NUM / DEN) * OMEGA_0 / math.sin(OMEGA_0):.5f} = omega_0 / tan omega_0"
        f" (row A's two-pace ratio); m c_eff^2 = {3 * math.tan(OMEGA_0) * (NUM / DEN) * OMEGA_0 / math.sin(OMEGA_0) * C2:.5f} = omega_0 exactly"
    )
    d, length, half_width = 32, 64, 60
    x_lamp, x_openings, x_screen = 20, 40, 104
    stock = 2048
    for lam in (12.0, 16.0):
        k = 2 * math.pi / lam
        omega = omega_of_k(k)
        k_diag = k_of_omega(omega, math.pi / 4)
        vg = group_pace(k)
        m = k / vg
        ys, pat1 = screen_pattern(omega, d, length, half_width, per_direction=False)
        _, pat = screen_pattern(omega, d, length, half_width, per_direction=True)
        max1, maxd = maxima_of(ys, pat1), maxima_of(ys, pat)
        w = pat / pat.sum()
        counts = stock * w
        i26 = int(np.argmax(pat[ys > 5]) + np.sum(ys <= 5))
        side = int(ys[i26])
        nb = counts[i26] - max(counts[i26 - 1], counts[i26 + 1])
        sigma = math.sqrt(counts[i26] + max(counts[i26 - 1], counts[i26 + 1]))
        # the side lobe's centroid: the statistic of the counts that locates the maximum between Nodes
        lo_y, hi_y = int(round(0.5 * side)), int(round(1.5 * side))
        lobe = (ys >= lo_y) & (ys <= hi_y)
        w_lobe = w[lobe] / w[lobe].sum()
        y_c = float(np.sum(ys[lobe] * w_lobe))
        n_lobe = stock * w[lobe].sum()
        sd_c = math.sqrt(float(np.sum((ys[lobe] - y_c) ** 2 * w_lobe)) / n_lobe)
        print(
            f"(a) DE BROGLIE at the declared omega = {omega:.5f} (the period {2 * math.pi / omega:.2f} intervals): k = {k:.5f}"
            f" per Link on the axis (lambda_dB = {lam:.3f} Links), {k_diag:.5f} on the plane's diagonal (the band's anisotropy"
            f" {100 * (k_diag / k - 1):+.2f} percent at fixed omega); the screen at L = {length} with the openings d = {d}"
            f" apart: the maxima at y = {maxd} with the band's k per ray direction (THE PIN; with one k for both rays {max1});"
            f" the far-field lambda L / d = {lam * length / d:.1f} is not the pin"
        )
        print(
            f"    the counts at the stock of {stock} records (one click per record on the screen's {len(ys)} Nodes):"
            f" the centre {counts[ys == 0][0]:.0f}, the side maximum at y = {side}: {counts[i26]:.0f} against its higher"
            f" neighbour {max(counts[i26 - 1], counts[i26 + 1]):.0f} (the difference {nb:.0f}, {nb / sigma:.1f} Poisson sigmas:"
            f" the maximum falls between two Nodes, so the Node of the peak is not the statistic); THE PIN'S STATISTIC is the"
            f" side lobe's count centroid over y in [{lo_y}, {hi_y}]: {y_c:.2f} with the Poisson sd {sd_c:.2f} at this stock"
            f" ({n_lobe:.0f} clicks in the lobe), so the band of one Node is a {1 / sd_c:.1f}-sigma statistic"
        )
        train, clicks = chain_first_rung(omega, x_lamp, x_screen, 8, (64, 256, 1024, 4096))
        transit = (x_screen - x_lamp) / vg
        print(
            f"(b) E OF A MOVING MASS at that k, in the click's own form on a chain (the lamp at x = {x_lamp} inserting a"
            f" train of 8 periods, {train} intervals; the detector at x = {x_screen}, 84 Links; the pointer the record's"
            f" motion squared there against its norm over W): v_g = {vg:.5f} Link per interval, the group transit"
            f" {transit:.1f} intervals; THE FIRST RUNG by W: {clicks} intervals from the birth; THE PIN at W = 64:"
            f" {clicks[64]}, the band +- 2 (the rise between W = 64 and 4096); m = k / v_g = {m:.5f}, the band's number in"
            f" the form of a moving mass (the continuum's omega / c_m^2 = {omega / ((NUM / DEN) * C2):.4f} at this k, not"
            f" nature's gamma m)"
        )
    print(
        "    the form (K): omega_0 = m c_eff^2 exactly at the kind's own cone (m = 3 tan omega_0), E = m c^2 a derivation;"
        " omega_0 / (m c^2) = c_eff^2 / c^2 is row A's two-pace ratio, already on the schedule: no new prediction here."
    )
