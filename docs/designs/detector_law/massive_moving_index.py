"""COMPUTATION on a chain (not an engine run): the index of a moving block against the
resting one (MASSIVE_RECORD.md section 7, the index in motion; Reviewer 3's 12.5 (b)
precision (2) and his 14:29Z item 6).

The block: s cells of the massive kind (the medium's pair [156, 157] on every cell, the
well of depth mu^2 / 2 on the block's cells), coupled to light at its cells by g, G in
the first-difference form (section 7). Light: a sine train of frequency omega from a
source; the transmitted phase at a probe downstream, against the same train without
the block, gives the block's phase delay dphi (rung 2, the phase read by projection on
the window). At rest: n(omega) = 1 + dphi / (k s), k = omega / c. In motion at one Link
every K = 3 intervals (beta_c = c / 3 ... the pace 1 / 3 Links per interval, beta = 1 /
(3 c) = 0.577 of c, gamma_m = 1.2247), the block's cells, its pair region and its
massive rows translate together by the step verb; light meets the block head-on (the
block toward the source) or from behind (the block away). The covariant expectation,
from the phase's invariance: the lab delay equals the delay in the block's frame,
(n(omega') - 1) omega' gamma_m s / c, with omega' = gamma_m omega (1 +- beta) the
light's frequency in the block's frame and n(omega') the RESTING block's index read on
this same chain at omega' (so no formula is trusted, only the chain's own rest
readings). Two couplings: the declared G g carried unchanged, and G g carried as G g x
[K^2, K^2 - 3] = G g gamma_m^2 (the drive's rational pair, no root).

    PYTHONPATH=src python docs/designs/detector_law/massive_moving_index.py
"""

import numpy as np

C = 1 / np.sqrt(3)
K = 3
BETA = 1 / (3 * C)  # the pace 1 / 3 Links per interval over c
GAMMA2 = K * K / (K * K - 3)  # the drive's rational gamma_m^2 = 1.5
GAMMA = np.sqrt(GAMMA2)


def chain(n, steps, omega, source, probe, block0, s, ratio_out, ratio_in, g, G, direction, t_move, gain):
    """Light's row al and the massive row am on n cells; the block's cells start at block0
    and step one Link every K intervals in `direction` (-1 toward the source, +1 away, 0 at
    rest) from t_move on; `gain` multiplies G (the compensation)."""
    r = np.full(n, ratio_out)
    coupled = np.zeros(n, bool)
    lo = block0
    if s > 0:
        r[lo : lo + s] = ratio_in
        coupled[lo : lo + s] = True
    al = np.zeros(n)
    al_b = np.zeros(n)
    am = np.zeros(n)
    am_b = np.zeros(n)
    out = np.zeros(steps)
    acc = 0
    for t in range(steps):
        if s > 0 and direction != 0 and t >= t_move:
            acc += 1
            if acc == K:
                acc = 0
                lo += direction
                r = np.full(n, ratio_out)
                r[lo : lo + s] = ratio_in
                coupled = np.zeros(n, bool)
                coupled[lo : lo + s] = True
                am = np.roll(am, direction)
                am_b = np.roll(am_b, direction)
        al[source] = np.sin(omega * t)
        s6 = np.roll(am, 1) + np.roll(am, -1) + 4 * am
        am_n = (r / 3) * s6 - am_b + np.where(coupled, g * (al - al_b), 0.0)
        s6l = np.roll(al, 1) + np.roll(al, -1) + 4 * al
        al_n = s6l / 3 - al_b - np.where(coupled, gain * G * (am_n - am), 0.0)
        al_n[0] = al_n[-1] = 0.0
        am_b, am = am, am_n
        al_b, al = al, al_n
        out[t] = al[probe]
    return out, lo


def phase(sig, omega, t0, t1):
    ts = np.arange(t0, t1)
    seg = sig[t0:t1]
    return np.arctan2(np.sum(seg * np.cos(omega * ts)), np.sum(seg * np.sin(omega * ts)))


def delay(n, steps, omega, source, probe, block0, s, ro, ri, g, G, direction, t_move, gain, t0, t1):
    ref, _ = chain(n, steps, omega, source, probe, block0, 0, ro, ri, g, G, 0, t_move, 1.0)
    sig, lo_end = chain(n, steps, omega, source, probe, block0, s, ro, ri, g, G, direction, t_move, gain)
    d = phase(ref, omega, t0, t1) - phase(sig, omega, t0, t1)
    d = (d + np.pi) % (2 * np.pi) - np.pi
    tm = (t0 + t1) // 2
    halves = []
    for a, b in ((t0, tm), (tm, t1)):
        dd = phase(ref, omega, a, b) - phase(sig, omega, a, b)
        halves.append((dd + np.pi) % (2 * np.pi) - np.pi)
    amp = np.max(np.abs(sig[t0:t1])) / np.max(np.abs(ref[t0:t1]))
    print(
        f"      (the phase in the window's two halves: {halves[0]:+.4f}, {halves[1]:+.4f} rad: steady if equal)"
    )
    return d, amp, lo_end


def main():
    n = 2200
    source, probe = 300, 1500
    s = 24
    ro = 156 / 157
    mu = np.arccos(ro)
    ri = 1 / (1 + mu**2 / 4)
    g, G = 0.005, 1.0  # a weak index, n about 1.2 at rest, so that the moving slab stays a slab
    omega = 0.035
    steps = 4400  # the window well after the onset's transient and before the source's re-reflection (about 4850)
    t_move = 2600
    t0, t1 = 3400, 4300
    print(
        f"the chain: n = {n}, the source at {source}, the probe at {probe}; the block s = {s} cells, the medium's pair"
        f" [156, 157] (omega_0 = {mu:.4f}), the well mu_in^2 = mu^2 / 2; g = {g}, G = {G}; light at omega = {omega}"
        f" (lambda = {2 * np.pi * C / omega:.0f} Links); K = {K}, beta = {BETA:.3f} c, gamma_m = {GAMMA:.4f}; the window [{t0}, {t1}]"
    )
    # the resting block's index at omega and at the two block-frame frequencies
    rest = {}
    for label, om in (
        ("omega", omega),
        ("omega' toward", GAMMA * omega * (1 + BETA)),
        ("omega' away", GAMMA * omega * (1 - BETA)),
    ):
        d, amp, _ = delay(n, steps, om, source, probe, 1100, s, ro, ri, g, G, 0, t_move, 1.0, t0, t1)
        k = om / C
        nn = 1 + d / (k * s)
        rest[label] = (om, d, nn)
        print(
            f"  at rest, light at {label} = {om:.4f}: the phase delay {d:+.4f} rad over {s} cells -> n = {nn:.4f} (transmitted amplitude {amp:.3f})"
        )
    for direction, label in (
        (-1, "toward the source (head-on)"),
        (+1, "away from the source (from behind)"),
    ):
        om_p, _, n_p = rest["omega' toward" if direction == -1 else "omega' away"]
        expected = (n_p - 1) * om_p * GAMMA * s / C
        for gain, glabel in (
            (1.0, "G g carried unchanged"),
            (GAMMA2, "G g x [K^2, K^2 - 3] (gamma_m^2)"),
        ):
            start = (
                1300 if direction == -1 else 700
            )  # the block stays between the source and the probe over the run
            d, amp, lo_end = delay(
                n, steps, omega, source, probe, start, s, ro, ri, g, G, direction, t_move, gain, t0, t1
            )
            print(
                f"  moving {label}, {glabel}: the lab phase delay {d:+.4f} rad (the block from {start} to {lo_end} over the run;"
                f" transmitted amplitude {amp:.3f}); the covariant expectation (n(omega') - 1) omega' gamma_m s / c = {expected:+.4f} rad"
                f" with n(omega') = {n_p:.4f} from the rest reading; the ratio read / expected = {d / expected:.3f}"
            )


if __name__ == "__main__":
    main()
