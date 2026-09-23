"""COMPUTATION (not an engine run): the conserved form I of MASSIVE_RECORD.md section 3
on a board of any extents, and the EXACT invariant of the coupled first-difference scheme
of section 7 (the builder's two findings on the build's STEP 2, the Boss's 16:21Z).

(1) The form on a board with an axis of extent 1: the rule reads the Node itself as its
    two neighbours on that axis (a_U = a_D = a_now, DESIGN.md section 2), so the Link
    sum of I is the sum over the six DIRECTED reads, self-reads included:
    I = SUM_i (den_i / num_i) (a_next,i^2 + a_now,i^2) - SUM_i SUM_d a_next,i a_now,n_d(i).
    Checked in int64 with the remainder carried: I(t) - I(t - 1) equals the remainders'
    term SUM_i (a_next,i - a_before,i) (r_before,i - r_now,i) exactly (no tolerance),
    on a 6 x 6 x 1 periodic board and on a chain (two axes of extent 1).
(2) The coupled scheme of the relay script (`massive_light_clock_relay.py`): the massive
    step with light's backward difference, g (a_l,now - a_l,before), then light's step with
    the massive forward difference, -G (a_m,next - a_m,now), on the coupled cells. It is
    the Euler-Lagrange scheme of the two-point Lagrangian
    L = -a_m,t . W a_m,t+1 + a_m,t . K a_m,t / 2 + alpha (-a_l,t . a_l,t+1 + a_l,t . K a_l,t / 2)
        + g a_m,t+1 . W P (a_l,t+1 - a_l,t),   W = den / num on the cells, alpha = g W / G,
    and so symplectic; its exact quadratic invariant (the linear map's z . J Phi z) is
    J = I_m + alpha I_l + g W SUM_cells (a_m,t+1 - a_m,t) (a_l,t+1 - a_l,t):
    the continuum's E_l + (G / g) E_m PLUS the cross term of the two first differences on
    the cells, which oscillates at the percent level while J is exact. Requires one pair on
    the coupled cells (alpha one number), the block's declaration.

    PYTHONPATH=src python docs/designs/detector_law/massive_conserved_form.py
"""

import numpy as np

rng = np.random.default_rng(3)


def reads(a, extents):
    """The six directed reads of the rule on a periodic board of the given extents
    (an axis of extent 1 reads the Node itself twice; extent 2 reads the same Node twice)."""
    out = []
    for ax in range(3):
        for sh in (1, -1):
            out.append(np.roll(a, sh, axis=ax))
    return out


def form_int(a_next, a_now, num, den, extents):
    """3 num I in integers for one pair: 3 den SUM (a_next^2 + a_now^2) - num SUM reads."""
    nodes = 3 * den * (np.sum(a_next.astype(object) ** 2) + np.sum(a_now.astype(object) ** 2))
    links = sum(np.sum(a_next.astype(object) * rd.astype(object)) for rd in reads(a_now, extents))
    return nodes - num * links


def integer_check(extents, num, den, steps=60):
    a_b = rng.integers(-50, 51, size=extents)
    a = rng.integers(-50, 51, size=extents)
    r = np.zeros(extents, dtype=np.int64)
    worst = 0
    for _ in range(steps):
        s6 = sum(reads(a, extents))
        rhs = num * s6 - 3 * den * a_b + r
        a_n, r_n = np.divmod(rhs, 3 * den)  # 3 den a_next + r' = rhs, 0 <= r' < 3 den
        d_form = form_int(a_n, a, num, den, extents) - form_int(a, a_b, num, den, extents)
        rem_term = np.sum(
            (a_n.astype(object) - a_b.astype(object)) * (r.astype(object) - r_n.astype(object))
        )
        worst = max(worst, abs(int(d_form - rem_term)))
        a_b, a, r = a, a_n, r_n
    return worst


def coupled_chain(n=400, steps=600, g=1 / 20, G=1.0):
    num, den = 156, 157
    num_in, den_in = 314, 315
    cells = np.arange(200, 212)
    r = np.full(n, num / den)
    r[cells] = num_in / den_in
    w = 1 / r
    coupled = np.zeros(n, bool)
    coupled[cells] = True
    alpha = g * (den_in / num_in) / G
    x = np.arange(n)
    al = np.exp(-((x - 100) ** 2) / 200.0) * np.cos(0.2 * x)
    al_b = np.exp(-((x - 100 + 1 / np.sqrt(3)) ** 2) / 200.0) * np.cos(0.2 * (x - 1 / np.sqrt(3)))
    am = rng.normal(0, 1e-3, n)
    am_b = am.copy()

    def i_form(a_n, a, wt):
        s6 = np.roll(a, 1) + np.roll(a, -1) + 4 * a
        return np.sum(wt * (a_n**2 + a**2)) - np.sum(a_n * s6) / 3

    naive, exact = [], []
    for _ in range(steps):
        s6 = np.roll(am, 1) + np.roll(am, -1) + 4 * am
        am_n = (r / 3) * s6 - am_b + np.where(coupled, g * (al - al_b), 0.0)
        s6l = np.roll(al, 1) + np.roll(al, -1) + 4 * al
        al_n = s6l / 3 - al_b - np.where(coupled, G * (am_n - am), 0.0)
        am_b, am = am, am_n
        al_b, al = al, al_n
        i_m = i_form(am, am_b, w)
        i_l = i_form(al, al_b, 1.0)
        cross = g * np.sum((w * (am - am_b) * (al - al_b))[cells])
        naive.append(i_m + alpha * i_l)
        exact.append(i_m + alpha * i_l + cross)
    naive = np.array(naive)
    exact = np.array(exact)
    return (
        np.ptp(naive) / abs(exact[-1]),
        np.ptp(exact) / abs(exact[-1]),
        np.max(np.abs(naive - exact)) / abs(exact[-1]),
    )


if __name__ == "__main__":
    print("(1) the form with the remainders' term, exact in integers (worst residual, must be 0):")
    for ext, pair in (((6, 6, 1), (156, 157)), ((40, 1, 1), (2, 3)), ((6, 6, 6), (800, 809))):
        print(f"    extents {ext}, pair {pair}: residual {integer_check(ext, *pair)}")
    print("(2) the coupled scheme on the chain, 600 intervals, G = 1 (peak-to-peak drift over |J|):")
    for g in (1 / 20, 1 / 5):
        d_naive, d_exact, cross = coupled_chain(g=g)
        print(
            f"    g = {g:.2f}: I_m + alpha I_l drifts {d_naive:.2e}; J exact to {d_exact:.1e};"
            f" the cross term up to {cross:.2e} of J"
        )
