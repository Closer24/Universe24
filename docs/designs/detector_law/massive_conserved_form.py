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
(3) The same in the ENGINE'S INTEGERS with the coupling folded into the rule's one division
    (Reviewer 3's MUST A through the Boss, 17:00Z): the massive row
    3 den g_d a_next + r' = num g_d S_6 - 3 den g_d a_before + 3 den g_n P (a_l,now - a_l,before) + r,
    0 <= r' < 3 den g_d (one D per row per interval, the wall 3 den g_d), and light's row
    3 G_d a_next + r' = G_d S_6 - 3 G_d a_before - 3 G_n P (a_m,next - a_m,now) + r, the wall
    3 G_d. Then J(t) - J(t - 1) = SUM_i (a_m,next - a_m,before)_i (r - r')_i / (3 num_i g_d)
    + alpha SUM_i (a_l,next - a_l,before)_i (r - r')_i / (3 G_d) EXACTLY (checked in exact
    rationals on a chain, the residual 0): the remainders' term of section 3 per record, each
    with its own wall, is the whole correction; nothing else.

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


def coupled_chain_exact(n=40, steps=120, g=(1, 20), G=(1, 1)):
    """The folded-division integer scheme on a chain, the identity checked in Fractions."""
    from fractions import Fraction as F

    num_out, den_out, num_in, den_in = 156, 157, 314, 315
    cells = range(15, 25)
    num = [num_out] * n
    den = [den_out] * n
    P = [0] * n
    for i in cells:
        num[i], den[i], P[i] = num_in, den_in, 1
    g_n, g_d = g
    G_n, G_d = G
    alpha = F(g_n, g_d) * F(den_in, num_in) / F(G_n, G_d)
    x_b = [int(v) for v in rng.integers(-40, 41, n)]
    x = [int(v) for v in rng.integers(-40, 41, n)]
    y_b = [int(v) for v in rng.integers(-40, 41, n)]
    y = [int(v) for v in rng.integers(-40, 41, n)]
    r_m = [0] * n
    r_l = [0] * n

    def s6(a, i):
        return a[i - 1] + a[(i + 1) % n] + 4 * a[i]

    def form(a_n, a, wt):
        return (
            sum(wt[i] * (F(a_n[i]) ** 2 + F(a[i]) ** 2) for i in range(n))
            - sum(F(a_n[i]) * s6(a, i) for i in range(n)) / 3
        )

    w_m = [F(den[i], num[i]) for i in range(n)]
    w_l = [F(1)] * n

    def J(x_n, x, y_n, y):
        cross = F(g_n, g_d) * sum(w_m[i] * (x_n[i] - x[i]) * (y_n[i] - y[i]) for i in cells)
        return form(x_n, x, w_m) + alpha * form(y_n, y, w_l) + cross

    worst = F(0)
    j_prev = J(x, x_b, y, y_b)
    for _ in range(steps):
        x_n, r_m2 = [0] * n, [0] * n
        for i in range(n):
            rhs = (
                num[i] * g_d * s6(x, i)
                - 3 * den[i] * g_d * x_b[i]
                + 3 * den[i] * g_n * P[i] * (y[i] - y_b[i])
                + r_m[i]
            )
            x_n[i], r_m2[i] = divmod(rhs, 3 * den[i] * g_d)
        y_n, r_l2 = [0] * n, [0] * n
        for i in range(n):
            rhs = G_d * s6(y, i) - 3 * G_d * y_b[i] - 3 * G_n * P[i] * (x_n[i] - x[i]) + r_l[i]
            y_n[i], r_l2[i] = divmod(rhs, 3 * G_d)
        j_now = J(x_n, x, y_n, y)
        rem = sum(
            F((x_n[i] - x_b[i]) * (r_m[i] - r_m2[i]), 3 * num[i] * g_d) for i in range(n)
        ) + alpha * sum(F((y_n[i] - y_b[i]) * (r_l[i] - r_l2[i]), 3 * G_d) for i in range(n))
        worst = max(worst, abs(j_now - j_prev - rem))
        j_prev = j_now
        x_b, x, y_b, y, r_m, r_l = x, x_n, y, y_n, r_m2, r_l2
    return worst


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
    print("(3) the folded-division integer scheme on a chain, 120 intervals, exact rationals:")
    for g in ((1, 20), (1, 5)):
        print(
            f"    g = {g[0]}/{g[1]}, G = 1: J(t) - J(t-1) less the two remainder terms, worst residual {coupled_chain_exact(g=g)}"
        )
