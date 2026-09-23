"""COMPUTATION on a chain (not an engine run): the index of a moving block against the
resting one (MASSIVE_RECORD.md section 7, the index in motion; Reviewer 3's 12.5 (b)
precision (2) and his 14:29Z item 6).

The block: s cells of the massive kind (the medium's pair [156, 157] on every cell, the
well of depth mu^2 / 2 on the block's cells), coupled to light at its cells by g, G in
the first-difference form (section 7). Light: a sine train of frequency omega from a
source; the transmitted phase at a probe downstream, against the same train without
the block, gives the block's phase delay dphi (rung 2, the phase read by projection on
the window). At rest: n(omega) = 1 + dphi / (k s), k = omega / c. In motion at one Link
every K = 3 intervals (the pace 1 / 3 Links per interval, beta = 0.577 of c, gamma_m =
1.2247), the step verb translates the block's CELLS and its pair region only; the
massive rows stay on their Nodes and follow by the rule (the design's reading, Reviewer
3's MUST on 7a82c155, record 1431: a carried record is a hop, not the design); the coupling on
a hop is the ADJOINT pair of the discrete Lagrangian (Reviewer 3's MUST on 4f74bf2a):
light's step first; the source term in light's row the BACKWARD difference of the
massive levels along the cell's path (the cell's Node now less the cell's previous Node
before) on the hop interval; the receive in the massive row the FORWARD difference of
light along the path (light's next level at the cell's next Node less light's now at
the cell) on the interval before a hop; the same-Node differences otherwise, and the
same-Node pair printed beside it (a first path form that took the backward difference
in both rows pumped light without bound: not adjoint, superseded); G g is carried
as G g x [K^2, K^2 - 3] = G g gamma_m^2 (the drive's rational pair), and the unchanged
G g is printed beside it for the record. Light meets the block head-on (the block toward
the source) or from behind (the block away). The covariant expectation,
from the phase's invariance: the lab delay equals the delay in the block's frame,
(n(omega') - 1) omega' gamma_m s / c, with omega' = gamma_m omega (1 +- beta) the
light's frequency in the block's frame and n(omega') the RESTING block's index read on
this same chain at omega' (so no formula is trusted, only the chain's own rest
readings). A first version of this script (7a82c155) carried the massive rows with the cells and
read 0.47 and 0.63 of the covariant delay head-on: the reading of a carried record, not
of the design; superseded by this one.

    PYTHONPATH=src python docs/designs/detector_law/massive_moving_index.py
"""

import numpy as np

C = 1 / np.sqrt(3)
K = 3
BETA = 1 / (3 * C)  # the pace 1 / 3 Links per interval over c
GAMMA2 = K * K / (K * K - 3)  # the drive's rational gamma_m^2 = 1.5
GAMMA = np.sqrt(GAMMA2)


COUPLING = "adjoint_r3"  # "adjoint_r3": Reviewer 3's co-moving pair (the massive step first); "adjoint": the roles swapped, light first; "same_node": the same-Node differences, light first


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
    e_light = np.zeros(steps)
    e_mass = np.zeros(steps)
    acc = 0
    moving = s > 0 and direction != 0
    for t in range(steps):
        hop_now = False
        if moving and t >= t_move:
            acc += 1
            if acc == K:
                acc = 0
                lo += direction
                r = np.full(n, ratio_out)
                r[lo : lo + s] = ratio_in
                coupled = np.zeros(n, bool)
                coupled[lo : lo + s] = True
                hop_now = True  # the cells and the pair region moved at the start of this interval; the rows stay
        hop_next = (
            moving and t + 1 >= t_move and acc == K - 1
        )  # the cells move at the start of the next interval
        al[source] = np.sin(omega * t)
        if COUPLING == "adjoint_r3":
            # Reviewer 3's operands in the script's own convention (the Boss's 15:56Z): the MASSIVE step first; the
            # receive on a hop interval is light's now here less light's BEFORE at the previous Node; the source on the
            # interval BEFORE a hop is the massive NEXT at the cell's next Node (x + direction) less the massive now here;
            # the same-Node differences on every other interval. The Lagrangian -G SUM a_l(x_t, t) [a_m(x_{t+1}, t+1) - a_m(x_t, t)].
            al_prev = np.roll(al_b, direction) if hop_now else al_b
            s6 = np.roll(am, 1) + np.roll(am, -1) + 4 * am
            am_n = (r / 3) * s6 - am_b + np.where(coupled, g * (al - al_prev), 0.0)
            am_n_fwd = np.roll(am_n, -direction) if hop_next else am_n
            s6l = np.roll(al, 1) + np.roll(al, -1) + 4 * al
            al_n = s6l / 3 - al_b - np.where(coupled, gain * G * (am_n_fwd - am), 0.0)
            al_n[0] = al_n[-1] = 0.0
        else:
            path = COUPLING == "adjoint"
            # light's step first: the source term the backward difference of the massive levels, along the path on a hop
            am_prev = np.roll(am_b, direction) if (hop_now and path) else am_b
            s6l = np.roll(al, 1) + np.roll(al, -1) + 4 * al
            al_n = s6l / 3 - al_b - np.where(coupled, gain * G * (am - am_prev), 0.0)
            al_n[0] = al_n[-1] = 0.0
            # the massive step: the receive the forward difference of light, along the path on the interval before a hop
            al_fwd = np.roll(al_n, -direction) if (hop_next and path) else al_n
            s6 = np.roll(am, 1) + np.roll(am, -1) + 4 * am
            am_n = (r / 3) * s6 - am_b + np.where(coupled, g * (al_fwd - al), 0.0)
        am_b, am = am, am_n
        al_b, al = al, al_n
        out[t] = al[probe]
        e_light[t] = 3 * np.sum((al - al_b) ** 2) + np.sum((al[1:] - al[:-1]) * (al_b[1:] - al_b[:-1]))
        e_mass[t] = 3 * np.sum((am - am_b) ** 2 / r) + np.sum(
            (am[1:] - am[:-1]) * (am_b[1:] - am_b[:-1])
        )
    return out, lo, e_light, e_mass


def phase(sig, omega, t0, t1):
    ts = np.arange(t0, t1)
    seg = sig[t0:t1]
    return np.arctan2(np.sum(seg * np.cos(omega * ts)), np.sum(seg * np.sin(omega * ts)))


def delay(n, steps, omega, source, probe, block0, s, ro, ri, g, G, direction, t_move, gain, t0, t1):
    ref, _, e_ref, _ = chain(n, steps, omega, source, probe, block0, 0, ro, ri, g, G, 0, t_move, 1.0)
    sig, lo_end, e_l, e_m = chain(
        n, steps, omega, source, probe, block0, s, ro, ri, g, G, direction, t_move, gain
    )
    # the energy account (HOST-free, COMPUTATION): light's E on the chain and the massive kind's, the window's drift per interval
    # against the reference train's own growth (the hard source feeds the chain steadily); the coupling's conserved combination at rest is E_light + (G / g) E_m
    drift_l = (e_l[t1 - 1] - e_l[t0]) / (t1 - t0) - (e_ref[t1 - 1] - e_ref[t0]) / (t1 - t0)
    drift_m = (e_m[t1 - 1] - e_m[t0]) / (t1 - t0)
    print(
        f"      (the energy account over the window: light's E drifts {drift_l:+.3e} per interval beyond the reference train's own feed, the massive E {drift_m:+.3e}; the combination E_light + (G / g) E_m drifts {drift_l + (G / g) * drift_m:+.3e})"
    )
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


def receding_long():
    """The receding case on a longer chain with a later window (the block-frame period 350
    intervals needs several periods to settle after the motion starts)."""
    n = 4000
    source, probe = 300, 2500
    s = 24
    ro = 156 / 157
    mu = np.arccos(ro)
    ri = 1 / (1 + mu**2 / 4)
    g, G = 0.005, 1.0
    omega = 0.035
    steps = 6200
    t_move = 3000
    t0, t1 = 5000, 6000
    print(
        f"\nthe receding case on a longer chain: n = {n}, the source at {source}, the probe at {probe}, the block from 1500 moving away from {t_move}; the window [{t0}, {t1}]"
    )
    om_p = GAMMA * omega * (1 - BETA)
    d, amp, _ = delay(n, steps, om_p, source, probe, 1500, s, ro, ri, g, G, 0, t_move, 1.0, t0, t1)
    n_p = 1 + d / ((om_p / C) * s)
    print(
        f"  at rest, light at omega' away = {om_p:.4f}: n = {n_p:.4f} (transmitted amplitude {amp:.3f})"
    )
    expected = (n_p - 1) * om_p * GAMMA * s / C
    for gain, glabel in ((1.0, "G g carried unchanged"), (GAMMA2, "G g x [K^2, K^2 - 3] (gamma_m^2)")):
        d, amp, lo_end = delay(
            n, steps, omega, source, probe, 1500, s, ro, ri, g, G, +1, t_move, gain, t0, t1
        )
        print(
            f"  moving away from the source (from behind), {glabel}: the lab phase delay {d:+.4f} rad (the block from 1500 to {lo_end};"
            f" transmitted amplitude {amp:.3f}); the covariant expectation {expected:+.4f} rad; the ratio read / expected = {d / expected:.3f}"
        )


if __name__ == "__main__":
    COUPLING = "adjoint_r3"
    print(
        "=== Reviewer 3's adjoint co-moving pair in the script's own convention (the massive step first; the receive on a hop"
        " light's now here less light's before at the previous Node; the source before a hop the massive next at the next Node"
        " less the massive now here)"
    )
    main()
    receding_long()
    COUPLING = "adjoint"
    print(
        "\n=== the pair with the roles swapped (light's step first; the source the backward difference along the path on the hop,"
        " the receive the forward difference along the path before the hop), the earlier reading"
    )
    main()
    receding_long()
    COUPLING = "same_node"
    print(
        "\n=== the SAME-NODE differences on every interval, light's step first (the hop changes only the cells' set and the pair region)"
    )
    main()
    receding_long()
