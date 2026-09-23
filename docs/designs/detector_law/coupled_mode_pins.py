"""COMPUTATION (not an engine run): the pins that need the coupled scheme of
MASSIVE_RECORD.md section 7 as built (the massive step first with light's a_now -
a_before, light's step with the massive a_next - a_now, the coupling on the block's
cells), computed by the linear one-step map of that scheme on the GameBoard before any
run; and the declared box's gradient ratio for Newton's fall (ALGEBRAIC_CLOSURE.md
section 2, under the hypothesis pair-field-v1).

Printed, each with its kind:
  (a) THE ATOM'S LINES (ALGEBRA.md 8.9, prediction 6; PLAN.md item 7): the block of
      side 20 at full depth on the 64^2 layer, G = [1, 1], g = [1, 200], seeded in its
      bare mode: the coupled map's eigenvalue nearest the bare mode and the block's
      summed record's peak over 6000 intervals, against the bare mode 0.09097; the
      envelope's decay (the radiative width);
  (b) THE EMITTER'S RADIATIVE DAMPING on a chain of 1400 (the light clock, row (d); the
      redshift, row 4b): the block of side 12 at full depth, the envelope's decay per
      interval against G g, over the window before light's return (2425 intervals);
  (c) ROW 4b's ONE FORMULA ON ITS DECLARED WORLD (DECLARATIONS.md section 4: the chain
      of 2200, the medium [156, 157], the well [314, 315], side 12, k = 3): f / f0 =
      omega_b(gamma_m s) / (gamma_m omega_b(s)) with gamma_m at the massive kind's exact
      cone, and 1 + z = (1 + beta_c) / (f / f0); the free emitter's gamma_m (1 + beta_c)
      beside as the (K) limit; light's phase and group pace on the chain at the line;
  (d) NEWTON'S FALL ON THE DECLARED BOX (Reviewer 3's lines of 21:36Z and 21:52Z): on a
      periodic 96^3 box the field carries the images' term beside 1 / (4 pi r): the
      box's own gradient ratio at r and 2 r from the periodic Green's function of
      pair_field_pins.py (a), Newton's 4.00 the limit the ratio tends to; and the
      point packet's fall by the ray equations of the exact band with the local pitch
      omega_0 - delta(x) (the mass m(x) = 3 tan(omega_0 - delta(x)) is the local
      pitch's, not a constant): the fall times from rest at r = 10 and 20 to four
      Links inward and the accelerations at the start, at kappa = 1.0 and 0.277; the
      form's number, a PREDICTION, not a pin (the spread is not in it).

    PYTHONPATH=src python docs/designs/detector_law/coupled_mode_pins.py
"""

import math
import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator, eigs, eigsh, splu


def periodic_s1(n):
    o = np.ones(n - 1)
    return sp.diags([o, o, [1.0], [1.0]], [-1, 1, n - 1, -(n - 1)], shape=(n, n))


def chain_reads(n):
    """The six reads on an n x 1 x 1 chain: the two neighbours and four self-reads."""
    return (periodic_s1(n) + 4 * sp.identity(n)).tocsr()


def layer_reads(n):
    """The six reads on an n x n x 1 layer: S_4 and two self-reads."""
    s1 = periodic_s1(n)
    i1 = sp.identity(n)
    return (sp.kron(s1, i1) + sp.kron(i1, s1) + 2 * sp.identity(n * n)).tocsr()


def bare_mode(reads, d_node):
    """The lowest mode of the massive kind with the per-Node D = den / num: the record's
    profile a and its omega_b; the symmetric form D^-1/2 (S_6 / 3) D^-1/2."""
    d = 1 / np.sqrt(d_node)
    a_sym = sp.diags(d) @ (reads / 3) @ sp.diags(d)
    val, vec = eigsh(a_sym, k=1, which="LA", tol=1e-10, ncv=40, maxiter=50000)
    return math.acos(val[0] / 2), d * vec[:, 0]


def coupled_map(reads, d_node, cells, g, big_g):
    """The one-step map of section 7's scheme on z = (m_now, m_before, l_now, l_before):
    m_next = (S_6 m_now) / (3 D) - m_before + g P (l_now - l_before);
    l_next = (S_6 l_now) / 3 - l_before - G P (m_next - m_now)."""
    n = reads.shape[0]
    ident = sp.identity(n, format="csr")
    zero = sp.csr_matrix((n, n))
    a_m = sp.diags(1 / d_node) @ (reads / 3)
    p_g = sp.diags(g * cells)
    p_big = sp.diags(big_g * cells)
    row_m = sp.hstack([a_m, -ident, p_g, -p_g])
    row_l = sp.hstack([zero, zero, reads / 3, -ident]) - p_big @ (
        row_m - sp.hstack([ident, zero, zero, zero])
    )
    return sp.vstack(
        [row_m, sp.hstack([ident, zero, zero, zero]), row_l, sp.hstack([zero, zero, ident, zero])]
    ).tocsc()


def eigenvalues_near(t_map, omega, k=8):
    """The map's eigenvalues nearest exp(i omega) by shift-invert (a complex LU)."""
    n = t_map.shape[0]
    sig = np.exp(1j * omega)
    lu = splu((t_map - sig * sp.identity(n)).tocsc().astype(complex))
    op = LinearOperator((n, n), matvec=lu.solve, dtype=complex)
    v = eigs(op, k=k, which="LM", return_eigenvectors=False)
    return sig + 1 / v


def block_record(reads, d_node, cells, g, big_g, steps):
    """The block seeded in its bare mode (a standing start), the map iterated, the
    block's summed massive record over the cells at each interval."""
    omega_b, prof = bare_mode(reads, d_node)
    t_map = coupled_map(reads, d_node, cells, g, big_g).tocsr()
    n = reads.shape[0]
    z = np.concatenate([prof, prof * math.cos(omega_b), np.zeros(n), np.zeros(n)])
    sums = np.empty(steps)
    for t in range(steps):
        sums[t] = z[:n][cells > 0].sum()
        z = t_map @ z
    return omega_b, sums


def peak_and_decay(sums, omega_b):
    """The summed record's spectral peak inside the mode's band and the envelope's decay
    per interval (both COMPUTATION, the map's numbers before any run, not clicks)."""
    x = sums - sums.mean()
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)), n=len(x) * 8))
    w = 2 * math.pi * np.fft.rfftfreq(len(x) * 8)
    band = (w > 0.5 * omega_b) & (w < 1.6 * omega_b)
    peak = w[band][np.argmax(spec[band])]
    period = int(2 * math.pi / omega_b)
    env = np.array([np.abs(x[i : i + period]).max() for i in range(0, len(x) - period, period)])
    q = max(1, len(env) // 4)
    rate = -math.log(env[-q:].mean() / env[:q].mean()) / ((len(env) - q) * period)
    return peak, rate


def well_d(inside, num_out, den_out, num_in, den_in):
    """D = den / num per Node from the pairs [num, den] of the medium and the well."""
    return np.where(inside, den_in / num_in, den_out / num_out)


if __name__ == "__main__":
    t0 = time.time()
    # (a) the atom's lines on the 64^2 layer
    n, s = 64, 20
    reads = layer_reads(n)
    idx = np.arange(n)
    axis = (idx >= (n - s) // 2) & (idx < (n - s) // 2 + s)
    xx, yy = np.meshgrid(axis, axis, indexing="ij")
    inside = (xx & yy).ravel()
    d_node = well_d(inside, 800, 809, 800, 800)
    omega_b, sums = block_record(reads, d_node, inside.astype(float), 1 / 200, 1.0, 6000)
    peak, rate = peak_and_decay(sums, omega_b)
    near = eigenvalues_near(coupled_map(reads, d_node, inside.astype(float), 1 / 200, 1.0), omega_b)
    nearest = near[np.argmin(np.abs(np.angle(near) - omega_b))]
    print(
        f"(a) the atom's lines: the 64^2 layer, side {s} at full depth, G = [1, 1], g = [1, 200]:"
        f" the bare mode {omega_b:.5f}; the coupled map's eigenvalue nearest it {np.angle(nearest):.5f}"
        f" (|lambda| {abs(nearest):.6f}); the block's summed record's peak {peak:.5f} ({peak / omega_b:.4f} of the bare);"
        f" the envelope's decay {rate:.2e} per interval. The PIN of the atom's world: its lines at the COUPLED"
        f" modes; the bare 0.09097 is not the line."
    )
    # (b) the emitter's radiative damping on the chain of 1400
    n, s = 1400, 12
    reads = chain_reads(n)
    idx = np.arange(n)
    cells = ((idx >= n // 2 - s // 2) & (idx < n // 2 + s // 2)).astype(float)
    d_node = well_d(cells > 0, 800, 809, 800, 800)
    print(
        f"(b) the emitter's radiative damping on the chain of {n}, side {s} at full depth (the window 2300, before light's return):"
    )
    for gg in (0.2, 0.02, 0.002, 0.0002, 0.00002):
        omega_b, sums = block_record(reads, d_node, cells, gg, 1.0, 2300)
        peak, rate = peak_and_decay(sums, omega_b)
        print(
            f"    G g = {gg:<8g}: the peak {peak:.5f} ({peak / omega_b:.4f} of the bare {omega_b:.5f}),"
            f" the decay {rate:.2e} per interval = {rate * 2 * math.pi / omega_b:.4f} per period"
        )
    # (c) row 4b's one formula on its declared world
    n, s = 2200, 12
    reads = chain_reads(n)
    idx = np.arange(n)
    num_out, den_out, num_in, den_in = 156, 157, 314, 315
    omega_0 = math.acos(num_out / den_out)
    c2 = 1 / 3
    c_eff2 = (num_out / den_out) * (omega_0 / math.sin(omega_0)) * c2
    beta = (1 / 3) / math.sqrt(c2)
    gamma_m = 1 / math.sqrt(1 - (1 / 9) / c_eff2)

    def omega_of(width):
        m = (idx >= n // 2 - width // 2) & (idx < n // 2 - width // 2 + width)
        return bare_mode(reads, well_d(m, num_out, den_out, num_in, den_in))[0]

    w_s = omega_of(s)
    gs = gamma_m * s
    lo, hi = int(math.floor(gs)), int(math.ceil(gs))
    w_gs = omega_of(lo) + (omega_of(hi) - omega_of(lo)) * (gs - lo)
    ratio = w_gs / (gamma_m * w_s)
    eps = 1 - (w_s / omega_0) ** 2
    k_line = math.acos(3 * math.cos(w_s) - 2)
    gamma_cm = 1 / math.sqrt(1 - (1 / 9) / ((num_out / den_out) * c2))
    gamma_c = 1 / math.sqrt(1 - (1 / 9) / c2)
    print(
        f"(c) row 4b on its declared world (the chain of {n}, the medium [{num_out}, {den_out}], the well"
        f" [{num_in}, {den_in}], side {s}, k = 3): omega_0 = {omega_0:.5f}, the well's mode {w_s:.5f} (eps {eps:.3f});"
        f" gamma_m at the exact cone {gamma_m:.5f}; the one formula f / f0 = {ratio:.4f} (the free emitter's 1 / gamma_m"
        f" {1 / gamma_m:.4f}); THE PIN 1 + z = (1 + beta_c) / (f / f0) = {(1 + beta) / ratio:.4f}; the free limit"
        f" gamma_m (1 + beta_c) = {gamma_m * (1 + beta):.4f} beside (K), with the CONTROLS at this medium's second-order"
        f" cone {gamma_cm * (1 + beta):.4f} and at light's {gamma_c * (1 + beta):.4f}; light on the chain at the line: phase pace"
        f" {w_s / k_line:.4f}, group pace {math.sin(k_line) / (3 * math.sin(w_s)):.4f} against c = {math.sqrt(c2):.4f}"
    )
    # (d) Newton's fall on the declared box: the periodic Green's function's gradient ratio
    n = 96
    k = 2 * np.pi * np.fft.fftfreq(n)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    lam = 6 - 2 * (np.cos(kx) + np.cos(ky) + np.cos(kz))
    src = np.zeros((n, n, n))
    src[0, 0, 0] = 1.0
    src -= 1.0 / n**3
    with np.errstate(divide="ignore", invalid="ignore"):
        g_hat = np.where(lam > 1e-12, np.fft.fftn(src) / lam, 0.0)
    phi = np.real(np.fft.ifftn(g_hat))

    def grad(r):
        return (phi[r - 1, 0, 0] - phi[r + 1, 0, 0]) / 2

    for r in (10, 20):
        ratio_box = grad(r) / grad(2 * r)
        print(
            f"(d) Newton's fall on the periodic {n}^3 box: the field's gradient at r = {r} over 2 r = {2 * r}:"
            f" {ratio_box:.4f} (the declared box's own; Newton's 4.00 the limit as the box grows;"
            f" the images' term makes the difference)"
        )
    omega_0 = math.acos(800 / 809)
    axis = phi[:, 0, 0] - phi[0, 0, 0] + 0.2527310098  # the axis line gauged to the infinite lattice
    xs = np.arange(n)

    def pitch(x):
        d = 4 * math.pi * kappa_fall * np.interp(x, xs, axis)
        return max(omega_0 - d, 0.0)

    def omega_of(x, k):
        return math.acos(math.cos(pitch(x)) * (2 * math.cos(k) + 4) / 6)

    def fall(x0, x_end, dt=0.05):
        x, k, t = float(x0), 0.0, 0.0
        h = 1e-3
        while x > x_end and t < 5000:
            dxdt = (omega_of(x, k + h) - omega_of(x, k - h)) / (2 * h)
            dkdt = -(omega_of(x + h, k) - omega_of(x - h, k)) / (2 * h)
            x += dxdt * dt
            k += dkdt * dt
            t += dt
        return t

    for kappa_fall in (1.0, 0.277):
        acc = {}
        for r in (10, 20):
            h = 1e-3
            m_loc = 3 * math.tan(pitch(r))
            acc[r] = -(pitch(r + h) - pitch(r - h)) / (2 * h) / m_loc
        t10, t20 = fall(10, 6), fall(20, 16)
        print(
            f"(d) the point packet's fall by the ray equations at kappa = {kappa_fall}: the local mass m(10) / m(20) ="
            f" {3 * math.tan(pitch(10)) / (3 * math.tan(pitch(20))):.4f}; the accelerations at the start"
            f" {acc[10]:.4e} and {acc[20]:.4e} Link per interval^2 (the ratio {acc[10] / acc[20]:.3f});"
            f" the fall times to four Links inward {t10:.1f} and {t20:.1f} intervals ((t20 / t10)^2 = {(t20 / t10) ** 2:.3f});"
            f" a PREDICTION of the form, not a pin (the spread and the floor are not in it)"
        )
    print(f"HOST {time.time() - t0:.0f} s")
