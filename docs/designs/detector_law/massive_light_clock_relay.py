"""COMPUTATION on a chain (not an engine run): the light clock on two objects of the
design, at rest, and the rung-crossing time of a driven mode (MASSIVE_RECORD.md
section 9 row (d), Reviewer 3's MUST (ii) of his gate).

The chain carries two records: light (the pair [1, 1]) and the massive kind in
form (B) with the medium's background pair [num, den] on every cell and the
LOWERED pair on the two objects' cells (a well of depth g_well); the coupling of
section 7 at the objects' cells in the first-difference form both ways (the
massive row gains g (a_l,now - a_l,before); light's row gains -G (a_m,now -
a_m,before)). Object A starts in its bound mode at amplitude A_0 (the emitter);
object B is quiet (the receiver). Readings, each a COMPUTATION for the declared
(pair, s, g_well, g, G, W, A_0, L):
  - the norm of A's emitted train: light's E (3 SUM (a_now - a_before)^2 + the
    strain over the Links) on the chain at the end of A's insert (the interval at
    which the train's front reaches B's near face), the rung 1 / W of it;
  - B's pointer: 3 SUM over B's cells of (a_m,now - a_m,before)^2 accumulated
    across intervals from the front's arrival; delta_rung(B) the intervals from the
    front's arrival at B's near face to the pointer's crossing of the rung;
  - A's receive of B's re-emission: A's own record rings, so the RECEIVED part is
    the difference between A's record with B present and A alone (the same chain
    without B; the rules are linear); the pointer of that difference against the
    same rung; N_0 the interval of its crossing, counted from A's start;
  - the budget of row (d): N_0 against 2 L / c = 207.85 (L = 60) and the
    register's 206 +- 2, said met or not met for these declarations.

    PYTHONPATH=src python docs/designs/detector_law/massive_light_clock_relay.py
"""

import numpy as np
from scipy.linalg import eigh_tridiagonal

C = 1 / np.sqrt(3)
C2 = 1 / 3


def bound_mode(n, cells, ratio_out, ratio_in):
    """The lowest mode of the massive kind in form (B) on the chain with the pair ratio
    r = num / den per cell: 2 cos omega D a = (1/3)(a_{j-1} + a_{j+1}) + (4/3) a ... in the
    chain's form of the rule a_next + a_before = (r / 3)(a_{j-1} + a_{j+1}) + (4 r / 3) a_now
    (the two absent axes folded as a_U = a_D = a_now, DESIGN.md section 2); the symmetric
    generalised problem M a = 2 cos omega a with M = R^(1/2) L R^(1/2), L the chain operator."""
    r = np.full(n, ratio_out)
    r[cells] = ratio_in
    sq = np.sqrt(r)
    d = (4 / 3) * r
    e = (1 / 3) * sq[:-1] * sq[1:]
    lam, vec = eigh_tridiagonal(d, e, select="i", select_range=(n - 1, n - 1))
    v = vec[:, 0] / sq  # back from the symmetric variable to the record's amplitude
    v /= np.abs(v).max()
    return np.arccos(lam[0] / 2), v


def run(n, cells_a, cells_b, ratio_out, ratio_in, g, G, A0, steps, with_b=True, mirror_ratio=None):
    om, v = bound_mode(n, cells_a, ratio_out, ratio_in)
    r = np.full(n, ratio_out)
    r[cells_a] = ratio_in
    coupled = np.zeros(n, bool)
    coupled[cells_a] = True
    rl = np.ones(n)  # light's pair ratio per cell, 1 everywhere but on an (M) mirror
    if with_b and mirror_ratio is None:
        r[cells_b] = ratio_in
        coupled[cells_b] = True
    if with_b and mirror_ratio is not None:
        rl[cells_b] = mirror_ratio
    am_b = A0 * v * np.cos(-om)
    am = A0 * v.copy()
    al = np.zeros(n)
    al_b = np.zeros(n)
    hist_am = np.zeros((steps, n))
    hist_al = np.zeros((steps, n))
    for t in range(steps):
        # the massive step (form (B) on the chain, the pair ratio per cell), with the receive
        s6 = np.roll(am, 1) + np.roll(am, -1) + 4 * am
        am_n = (r / 3) * s6 - am_b + np.where(coupled, g * (al - al_b), 0.0)
        # light's step, with the source term (the massive current, the step just taken)
        s6l = np.roll(al, 1) + np.roll(al, -1) + 4 * al
        al_n = (rl / 3) * s6l - al_b - np.where(coupled, G * (am_n - am), 0.0)
        al_n[0] = al_n[-1] = 0.0
        am_b, am = am, am_n
        al_b, al = al, al_n
        hist_am[t] = am
        hist_al[t] = al
    return om, hist_am, hist_al


def light_norm(al_now, al_before):
    motion = 3 * np.sum((al_now - al_before) ** 2)
    strain = np.sum((al_now[1:] - al_now[:-1]) * (al_before[1:] - al_before[:-1]))
    return motion + strain


def main():
    n = 1400
    s = 12
    L = 60
    a0 = 500
    cells_a = np.arange(a0, a0 + s)
    cells_b = np.arange(a0 + s - 1 + L, a0 + s - 1 + L + s)  # the facing cells L apart
    # the medium's pair with lambda_0 = 32 Links (the register's), cos omega_0 = num / den
    ratio_out = 156 / 157
    mu = np.arccos(ratio_out)
    # the well: mu_in^2 = mu^2 / 2 (eps about 0.06 on the chain), den' / num' = 1 + mu_in^2 / 2
    ratio_in = 1 / (1 + mu**2 / 4)
    A0 = 2.0**20
    W = 64
    steps = 700
    print(
        f"the chain: n = {n}, two objects of s = {s} cells, L = {L} between the near faces; the medium's pair"
        f" [156, 157] (omega_0 = {mu:.4f}, lambda_0 = {2 * np.pi * C / mu:.1f} Links); the well mu_in^2 = mu^2 / 2;"
        f" A_0 = 2^20; W = {W}; 2 L / c = {2 * L / C:.2f}; the arrival at B taken as L / c = {L / C:.1f} from A's near face"
    )
    mirror_gap = 0.3  # the (M) wall: the pair on light's record at B's cells with cos omega_gap = num / den, light at 0.10 evanescent inside
    for g, G, kind in (
        (0.02, 1.0, "W"),
        (0.05, 1.0, "W"),
        (0.1, 1.0, "W"),
        (0.2, 1.0, "W"),
        (0.05, 1.0, "M"),
        (0.2, 1.0, "M"),
    ):
        mirror = np.cos(mirror_gap) if kind == "M" else None
        om, am_with, al_with = run(
            n, cells_a, cells_b, ratio_out, ratio_in, g, G, A0, steps, True, mirror
        )
        _, am_alone, al_alone = run(n, cells_a, cells_b, ratio_out, ratio_in, g, G, A0, steps, False)
        # A's emitted train: its front reaches B's near face at t_front (light at c from A's far face)
        arrival = int(
            round(L / C)
        )  # the geometric arrival of the front at B's near face (the lattice's precursor runs ahead of it at the 10^-6 level)
        norm = light_norm(al_alone[arrival], al_alone[arrival - 1])
        rung = norm / W
        # B's pointer: its own record's motion across its cells, accumulated from the front's arrival
        motion_b = 3 * np.sum((am_with[1:, cells_b] - am_with[:-1, cells_b]) ** 2, axis=1)
        pointer_b = np.cumsum(np.where(np.arange(1, steps) >= arrival, motion_b, 0.0))
        cross_b = next((t + 1 for t in range(steps - 1) if pointer_b[t] >= rung), None)
        delta_rung = (cross_b - arrival) if (cross_b and kind == "W") else None
        # A's receive: the difference with and without B, its motion across A's cells
        diff = am_with[:, cells_a] - am_alone[:, cells_a]
        motion_a = 3 * np.sum((diff[1:] - diff[:-1]) ** 2, axis=1)
        pointer_a = np.cumsum(motion_a)
        cross_a = next((t + 1 for t in range(steps - 1) if pointer_a[t] >= rung), None)
        # the lifetime of A's mode alone (the radiative decay): the envelope's e-fold
        env = np.abs(am_alone[:, cells_a[s // 2]])
        peak = np.array([env[max(0, t - 30) : t + 30].max() for t in range(steps)])
        efold = next((t for t in range(steps) if peak[t] < peak[40] / np.e), None)
        budget = None if cross_a is None else cross_a - 2 * L / C
        print(
            f"B a {'BODY (W), the well of the pair with the receive' if kind == 'W' else 'MIRROR (M), the pair on lights record at its cells, the gap 0.3'}; "
            f"g = {g}, G = {G}: A's mode omega_b = {om:.4f} (N_b = {2 * np.pi / om:.1f}); the front at B after {arrival} intervals"
            f" (L / c = {L / C:.1f} plus A's far-to-near {s} cells); the train's norm at the end of the insert {norm:.3e} in the"
            f" amplitude unit squared, the rung {rung:.3e}; B's pointer crosses the rung {delta_rung if kind == 'W' else 'n/a (a mirror has no record)'} intervals after the front"
            f" (delta_rung); A's received part crosses at N_0 = {cross_a} intervals from A's start against 2 L / c = {2 * L / C:.2f}:"
            f" N_0 - 2 L / c = {budget if budget is None else round(budget, 2)}; the register's 206 +- 2:"
            f" {'MET' if cross_a is not None and 204 <= cross_a <= 208 else 'NOT MET'}; A's mode alone e-folds in"
            f" {efold} intervals ({(efold / (2 * np.pi / om)) if efold else float('nan'):.1f} periods)"
        )


if __name__ == "__main__":
    main()
