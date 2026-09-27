"""COMPUTATION on a scratch ONE-LAYER board (z = 1; not an engine run): the pins of the
massive record's worlds re-declared for a layer, on the owner's word (2026-09-23, on the
chief physicist's z = 1 answer: "if it works algebraically, and on the times it clearly
does, then yes"; MASSIVE_RECORD.md section 11 item 7).

On a layer the rule is unchanged: the folded axis reads the Node itself twice (a_U =
a_D = a_now, DESIGN.md section 2), so the six reads are S_4 + 2 a_now and the mode is
2 cos omega_b D a = (S_4 + 2) a / 3, A = D^-1/2 (S_4 + 2) D^-1/2 / 3 symmetric (the form I
of section 3 exact on the layer, `massive_conserved_form.py`). The tail along an axis
keeps cosh kappa = 3 D_out cos omega_b - 2 (the two folded reads and the one transverse
axis give 2 + 2 in place of 4). What the layer does not test: the 3-D corner (blind, as
the chains were) and the cube's binding threshold (a square well on a layer binds at
every depth; eps differs from the cube's at the same s and g). Printed per (mu, s, g):
omega_b, omega_0, eps, the extent, the side by the margin rule (s + 4 / kappa for a pin
world), HOST per interval on the layer, and for the first pin world the block's clock
in motion at k = 3 on the layer itself (the cells stepped by the accumulator over a
ramp, the record re-forming), read at the co-moving centre against the one formula
of section 8 (1 / gamma_m to the residual eps (gamma_m^2 - 1) / 2).

    PYTHONPATH=src python docs/designs/detector_law/massive_layer_pins.py
"""

import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh


def periodic_s1(n):
    o = np.ones(n - 1)
    return sp.diags([o, o, [1.0], [1.0]], [-1, 1, n - 1, -(n - 1)], shape=(n, n))


def layer_reads(n):
    """The six reads on an n x n x 1 periodic layer: S_4 plus the two self-reads."""
    S1 = periodic_s1(n)
    I1 = sp.identity(n)
    return (sp.kron(S1, I1) + sp.kron(I1, S1) + 2 * sp.identity(n * n)).tocsr()


def layer_mode(n, s, mu, g, sx=None):
    """The lowest mode of a well of s cells across (and sx along x, s by default) on the layer."""
    sx = s if sx is None else sx
    L = layer_reads(n)
    idx = np.arange(n)
    # exactly sx cells along x and s across, as index ranges (a half-width test on an even
    # board folds an odd width onto the even one below it)
    ax = (idx >= (n - sx) // 2) & (idx < (n - sx) // 2 + sx)
    ac = (idx >= (n - s) // 2) & (idx < (n - s) // 2 + s)
    X, Y = np.meshgrid(ax, ac, indexing="ij")
    inside = (X & Y).ravel()
    D_out = 1 + mu**2 / 2
    D = np.where(inside, 1 + (mu**2 - g) / 2, D_out)
    d = 1 / np.sqrt(D)
    A = sp.diags(d) @ (L / 3) @ sp.diags(d)
    val, vec = eigsh(A, k=1, which="LA", tol=1e-10, ncv=40, maxiter=50000)
    omega_b = np.arccos(val[0] / 2)
    omega_0 = np.arccos(1 / D_out)
    eps = 1 - (omega_b / omega_0) ** 2
    ck = 3 * D_out * np.cos(omega_b) - 2
    kappa = np.arccosh(ck) if ck > 1 else 0.0
    v = np.abs(vec[:, 0]).reshape(n, n)
    c = n // 2
    face = (n - sx) // 2 + sx  # the first Node outside the well along +x
    line = v[face:, c] / v[face, c]
    over = np.where(line < np.e**-1)[0]
    extent_read = float(over[0]) if len(over) else float("nan")
    return omega_b, omega_0, eps, kappa, extent_read, vec[:, 0].reshape(n, n), inside.reshape(n, n)


def host_interval(n):
    a = np.random.default_rng(0).standard_normal((n, n))
    b = a.copy()
    num = np.full((n, n), 800.0)
    den = np.full((n, n), 809.0)
    t0 = time.time()
    for _ in range(5):
        s6 = np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1) + 2 * a
        nxt = (num * s6) / (3 * den) - b
        b, a = a, nxt
        s6 = np.roll(b, 1, 0) + np.roll(b, -1, 0) + np.roll(b, 1, 1) + np.roll(b, -1, 1) + 2 * b
        _ = s6 / 3 - a
    return (time.time() - t0) / 5


def read_peak(series):
    x = series - series.mean()
    w = np.hanning(len(x))
    n = 1 << (int(np.ceil(np.log2(len(x)))) + 3)
    F = np.abs(np.fft.rfft(x * w, n))
    i = np.argmax(F[1:]) + 1
    y0, y1, y2 = np.log(F[i - 1]), np.log(F[i]), np.log(F[i + 1])
    di = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
    return 2 * np.pi * (i + di) / n


def moving_on_layer(n, s, mu, g, k=3, ramp=1500, hold=8000):
    """The block pushed to k on the layer: the cells' set and the pair region step by the
    accumulator; the record stays on its Nodes and re-forms (section 5); the clock read at
    the co-moving centre over the hold by the spectral peak."""
    omega_b, omega_0, eps, kappa, _, v, inside0 = layer_mode(n, s, mu, g)
    D_out = 1 + mu**2 / 2
    D_in = 1 + (mu**2 - g) / 2
    v = v / np.abs(v).max()
    a_before = v * np.cos(-omega_b)
    a_now = v.copy()
    inside = inside0.copy()
    shift = 0
    acc = 0
    centre = []
    c = n // 2
    t0 = time.time()
    for t in range(ramp + hold):
        D = np.where(inside, D_in, D_out)
        s6 = (
            np.roll(a_now, 1, 0)
            + np.roll(a_now, -1, 0)
            + np.roll(a_now, 1, 1)
            + np.roll(a_now, -1, 1)
            + 2 * a_now
        )
        a_next = s6 / (3 * D) - a_before
        a_before, a_now = a_now, a_next
        p = min(t, ramp) / ramp  # the momentum reached over the ramp, the pace 1 / k after it
        acc += p
        if acc >= k:
            acc -= k
            shift += 1
            inside = np.roll(inside0, shift, axis=0)
        if t >= ramp:
            centre.append(a_now[(c + shift) % n, c])
    dt = time.time() - t0
    omega_moving = read_peak(np.array(centre))
    beta = 1 / k / (1 / np.sqrt(3))  # the pace over light's c
    # the one formula's gamma is the massive kind's own, at c_m = c sqrt(cos omega_0) (Reviewer 3's
    # MUST on PR #1053, decided by derivation in MASSIVE_RECORD.md section 8); gamma(c) a CONTROL beside
    cos_omega_0 = 1 / (1 + mu**2 / 2)
    omega_0 = np.arccos(cos_omega_0)
    gamma_c = 1 / np.sqrt(1 - beta**2)  # light's, a CONTROL
    gamma_m = 1 / np.sqrt(1 - beta**2 / cos_omega_0)  # the second-order cone, a CONTROL
    # the named gamma at the exact cone of the band's bottom, c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2
    # (Reviewer 3's token on 26674947, the exact form of the same derivation)
    gamma = 1 / np.sqrt(1 - beta**2 / (cos_omega_0 * omega_0 / np.sin(omega_0)))
    residual = eps * (gamma**2 - 1) / 2
    # the one formula of section 8: the moving block a resting well of width gamma s ALONG x
    # (s across), its phase read at 1 / gamma; the non-integer width interpolated
    w = gamma * s
    lo, hi = int(np.floor(w)), int(np.ceil(w))
    ob_lo = layer_mode(n, s, mu, g, sx=lo)[0]
    ob_hi = layer_mode(n, s, mu, g, sx=hi)[0] if hi != lo else ob_lo
    ob_w = ob_lo + (ob_hi - ob_lo) * (w - lo)
    formula = ob_w / (gamma * omega_b)

    def control_with(gamma_x):
        wc = gamma_x * s
        lo_c, hi_c = int(np.floor(wc)), int(np.ceil(wc))
        ob_lo_c = layer_mode(n, s, mu, g, sx=lo_c)[0]
        ob_hi_c = layer_mode(n, s, mu, g, sx=hi_c)[0] if hi_c != lo_c else ob_lo_c
        return (ob_lo_c + (ob_hi_c - ob_lo_c) * (wc - lo_c)) / (gamma_x * omega_b)

    control = (control_with(gamma_m), control_with(gamma_c))
    return (
        omega_b,
        eps,
        omega_moving / omega_b,
        1 / gamma,
        1 / gamma * (1 - residual),
        formula,
        residual,
        dt,
        control,
    )


print(
    "the square well's bound mode on a ONE-LAYER periodic board (z = 1, form (B)), and the margin rule"
)
print(
    "mu | s | g | layer n | omega_b | omega_0 | eps | kappa | extent 1/kappa | extent read | the side s + 4/kappa (a pin world)"
)
rows = [
    (0.15, 10, 0.15**2, 256),
    (0.15, 14, 0.15**2 / 2, 256),
    (0.15, 20, 0.15**2, 256),
    (0.15, 28, 0.15**2 / 2, 256),
    (0.05, 30, 0.05**2, 512),
    (0.05, 42, 0.05**2 / 2, 512),
    (0.05, 60, 0.05**2, 512),
    (0.15, 14, 0.15**2 / 4, 256),
    (0.15, 10, 0.15**2 / 4, 256),
    (0.15, 8, 0.15**2 / 2, 256),
    (0.05, 42, 0.05**2 / 4, 512),
    (0.05, 30, 0.05**2 / 4, 512),
]
for mu, s, g, n in rows:
    ob, o0, eps, kappa, ext_read, _, _ = layer_mode(n, s, mu, g)
    ext = 1 / kappa if kappa > 0 else float("inf")
    print(
        f"{mu} | {s} | {g:.5f} | {n} | {ob:.5f} | {o0:.5f} | {eps:.4f} | {kappa:.5f} | {ext:.1f} | {ext_read:.0f} | {s + 4 * ext:.0f}"
    )

print("\nHOST: one interval of the two rules on an n x n x 1 layer (numpy, this machine):")
for n in (128, 200, 300):
    t = host_interval(n)
    print(
        f"  n = {n} ({n * n:,} Nodes): {t * 1e3:.2f} ms per interval; a moving world of 9500 intervals {9500 * t:.0f} s"
    )

print(
    "\nthe block's clock in motion ON THE LAYER at k = 3 (ramp 1500, hold 8000), against the one formula:"
)
print(
    "mu | s | g | layer n | omega_b | eps | f/f0 read | 1/gamma (gamma at c_eff) | first order 1/gamma_m (1 - residual)"
    " | the one formula (the well of width gamma s along x, gamma at c_eff) | residual | s | the controls (gamma at c_m, at c)"
)
for mu, s, g, n in ((0.15, 10, 0.15**2, 200), (0.15, 14, 0.15**2 / 4, 200), (0.15, 20, 0.15**2, 64)):
    ob, eps, ratio, inv_g, first, formula, res, dt, control = moving_on_layer(n, s, mu, g)
    print(
        f"{mu} | {s} | {g:.5f} | {n} | {ob:.5f} | {eps:.4f} | {ratio:.4f} | {inv_g:.4f} | {first:.4f}"
        f" | {formula:.4f} | {res:.4f} | {dt:.0f} | the CONTROLS: with gamma(c_m) {control[0]:.4f}, with gamma(c) {control[1]:.4f}"
    )
