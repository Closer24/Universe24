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
      form's number, a PREDICTION, not a pin (the spread is not in it);
  (e) THE LIGHT CLOCK'S RETURN IN THE CLICK'S OWN FORM (DECLARATIONS.md section 10;
      Reviewer 3's line A of 00:50Z): the same map on an OPEN chain of 673 (zero faces; the
      block A at [600, 612) seeded in its mode at the engine's amplitude 2^20, G = [1, 1],
      g = [1, 50000], the face at 672 the mirror). ONE RECORD: the light the source term
      inserts during A's first cycle (the train, 70 intervals), then free; its NORM the
      squared motion inserted (SUM over the cells and the train of (G delta m)^2). The
      receiver is A's OWN cells under the cycle sentence (DESIGN.md section 5): its Ports
      take nothing of its own record during the train and for N_s after (declared N_s =
      one period), and the POINTER then accumulates the record's offer at A's cells (the
      Port's motion squared, (a_l(t + 1) - a_l(t))^2); the click is the first rung,
      pointer x W >= norm, W the declared wheel. Printed: the click's interval from the
      record's birth at W = 64, 256, 1024, 4096 against 2 L / c = 207.85, and the same
      with the receiver read at the face cell alone; also the RECEIVE of another body's
      record for row R2 at rest (B at [772, 784) emitting one cycle, A's cells the
      receiver, L = 60 face to face): the first rung against L / c = 103.9.
  (f) R2'S RISE PER DIRECTION (DECLARATIONS.md section 13; Reviewer 3's line B of 00:45Z,
      record 1543): the same one record with BOTH blocks stepping to k = 3 on +x
      (`one_record_moving`: the cells and their wells move, the rows stay, the coupling's
      operands along the path on a hop interval as massive_moving_index.py's adjoint_r3
      convention; the emitter seeded in its rest mode and ramped 1500 intervals before its
      train of one cycle). Printed per direction (A's record chasing B ahead of it; B's
      record meeting A behind it) and for the control at rest: the first rung from the
      birth at W = 64, 256, 1024, 4096, the front's transit L / (c -+ v), the RISE (the
      click less the transit) at the declared W = 64, and the Sagnac ratio read three ways:
      from the clicks alone, with the rest rise subtracted from both (Reviewer 3's caution),
      and with each direction's OWN rise subtracted (the reader of record), with the band
      from one interval of the click's grain on each side.

  (g) THE DECLARED COUPLING WITHIN THE LOAD BOUND (DECLARATIONS.md section 15 M1-1): (e)'s
      light clock and (f)'s four R2 cases re-run at G = [1, 50], g = [1, 1000] and the seed
      50 x 2^20, the same world as G = [1, 1], g = [1, 50000], seed 2^20 by the exact
      rescaling of the massive rows by 50; the clicks printed against (e)'s and (f)'s.

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


def block_mode_near(t_map, omega, cells, k=12):
    """The map's eigenvalue nearest exp(i omega) whose eigenvector has the largest massive
    weight on the block's cells: the block's own coupled mode among light's modes."""
    n = t_map.shape[0]
    sig = np.exp(1j * omega)
    lu = splu((t_map - sig * sp.identity(n)).tocsc().astype(complex))
    op = LinearOperator((n, n), matvec=lu.solve, dtype=complex)
    v, vecs = eigs(op, k=k, which="LM")
    lam = sig + 1 / v
    m = n // 4
    best, best_w = None, -1.0
    for j in range(len(lam)):
        vec = vecs[:, j]
        w = np.sum(np.abs(vec[:m][cells > 0]) ** 2) / (np.sum(np.abs(vec) ** 2) + 1e-30)
        if np.angle(lam[j]) > 0 and w > best_w:
            best, best_w = lam[j], w
    return best, best_w


def open_chain_reads(n):
    """The six reads on an open n x 1 x 1 chain: the two neighbours (none past the ends)
    and four self-reads; the ends are zero faces, kept at zero by the caller."""
    o = np.ones(n - 1)
    return (sp.diags([o, o], [-1, 1], shape=(n, n)) + 4 * sp.identity(n)).tocsr()


def one_record(n, steps, emitter_lo, receiver_lo, s=12, g=1 / 50000, big_g=1.0, amp=2**20, train=70):
    """One light record on an open chain of n: the block at emitter_lo (side s, seeded in its
    mode at amplitude amp) drives light through the source term during the train only;
    then light runs free. Returns the record's norm (the inserted squared motion), the
    per-interval offer at the receiver block's cells (the light's motion squared summed
    over its s cells) and at the receiver's face cell alone."""
    reads = open_chain_reads(n)
    idx = np.arange(n)
    cells_e = ((idx >= emitter_lo) & (idx < emitter_lo + s)).astype(float)
    cells_r = (idx >= receiver_lo) & (idx < receiver_lo + s)
    inside = (cells_e > 0) | cells_r
    d_node = well_d(inside, 800, 809, 800, 800)
    omega_b, prof = bare_mode(reads, np.where(cells_e > 0, 1.0, 809 / 800))
    prof = prof / np.abs(prof).max() * amp
    if prof[emitter_lo + s // 2] < 0:
        prof = -prof
    m_now, m_bef = prof.copy(), prof * math.cos(omega_b)
    l_now, l_bef = np.zeros(n), np.zeros(n)
    inv_d = 1 / d_node
    norm = 0.0
    offer_cells = np.empty(steps)
    offer_face = np.empty(steps)
    face = receiver_lo + s if receiver_lo < emitter_lo or receiver_lo == emitter_lo else receiver_lo
    for t in range(steps):
        m_next = inv_d * (reads @ m_now) / 3 - m_bef + g * cells_e * (l_now - l_bef)
        source = big_g * cells_e * (m_next - m_now) if t < train else 0.0
        l_next = (reads @ l_now) / 3 - l_bef - source
        l_next[0] = 0.0
        l_next[-1] = 0.0
        if t < train:
            norm += float(np.sum(source**2))
        motion = l_next - l_now
        offer_cells[t] = float(np.sum(motion[cells_r] ** 2))
        offer_face[t] = float(motion[face] ** 2)
        m_bef, m_now = m_now, m_next
        l_bef, l_now = l_now, l_next
    return omega_b, norm, offer_cells, offer_face


def sagnac_ratio(t_plus, t_minus):
    """The Sagnac ratio of two one-way intervals, their difference over their sum."""
    return (t_plus - t_minus) / (t_plus + t_minus)


def first_rung(offer, norm, wheel, start):
    """The interval at which the pointer (the offer accumulated from `start`) crosses the
    first rung, pointer x wheel >= norm; None if never."""
    pointer = 0.0
    for t in range(start, len(offer)):
        pointer += offer[t]
        if pointer * wheel >= norm:
            return t
    return None


def one_record_moving(
    n, steps, emitter_lo, receiver_lo, s=12, k=3, ramp=1500, g=1 / 50000, big_g=1.0, amp=2**20, train=70
):
    """R2's map (Reviewer 3's line B of 00:45Z): the one record of `one_record` with BOTH blocks
    stepping one Link every k intervals on +x from t = 0 (the cells and their wells move, the
    rows stay, the coupling's operands taken along the path on a hop interval, the convention
    of massive_moving_index.py's adjoint_r3); the emitter seeded in its rest mode and ramped
    `ramp` intervals before its train (the record's birth at t = ramp). Returns the mode's
    frequency, the birth, the norm, the per-interval offer at the receiver's CURRENT cells and
    the offer at the free Node adjacent to the receiver's face toward the emitter (as (e); printed beside: the light
    clock's receiving set is A's face cell, DECLARATIONS.md section 10 item 9; R2's sets stay the
    blocks' cells with own_grace the hold, section 13 item 1), so that the first rung from the
    birth is the click of that direction."""
    reads = open_chain_reads(n)
    idx = np.arange(n)
    lo_e, lo_r = emitter_lo, receiver_lo

    def cells(lo):
        return (idx >= lo) & (idx < lo + s)

    d_node = well_d(cells(lo_e) | cells(lo_r), 800, 809, 800, 800)
    omega_b, prof = bare_mode(reads, np.where(cells(lo_e), 1.0, 809 / 800))
    prof = prof / np.abs(prof).max() * amp
    if prof[lo_e + s // 2] < 0:
        prof = -prof
    m_now, m_bef = prof.copy(), prof * math.cos(omega_b)
    l_now, l_bef = np.zeros(n), np.zeros(n)
    norm = 0.0
    offer = np.empty(steps)
    offer_face = np.empty(steps)
    acc = 0
    for t in range(steps):
        hop_now = False
        acc += 1
        if acc == k:
            acc = 0
            lo_e += 1
            lo_r += 1
            d_node = well_d(cells(lo_e) | cells(lo_r), 800, 809, 800, 800)
            hop_now = True
        hop_next = acc == k - 1
        ce = cells(lo_e).astype(float)
        l_prev = np.roll(l_bef, 1) if hop_now else l_bef
        m_next = (reads @ m_now) / d_node / 3 - m_bef + g * ce * (l_now - l_prev)
        m_fwd = np.roll(m_next, -1) if hop_next else m_next
        in_train = ramp <= t < ramp + train
        source = big_g * ce * (m_fwd - m_now) if in_train else 0.0
        l_next = (reads @ l_now) / 3 - l_bef - source
        l_next[0] = 0.0
        l_next[-1] = 0.0
        if in_train:
            norm += float(np.sum(source**2))
        motion = l_next - l_now
        offer[t] = float(np.sum(motion[cells(lo_r)] ** 2))
        face = (
            lo_r + s if lo_r < lo_e else lo_r - 1
        )  # the free Node adjacent to the receiver's face, as (e)
        offer_face[t] = float(motion[face] ** 2)
        m_bef, m_now = m_now, m_next
        l_bef, l_now = l_now, l_next
    return omega_b, ramp, norm, offer, offer_face


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
    t_map = coupled_map(reads, d_node, inside.astype(float), 1 / 200, 1.0)
    near = eigenvalues_near(t_map, omega_b)
    nearest = near[np.argmin(np.abs(np.angle(near) - omega_b))]
    second, second_w = block_mode_near(t_map, 0.1380, inside.astype(float))
    print(
        f"(a) the atom's lines: the 64^2 layer, side {s} at full depth, G = [1, 1], g = [1, 200]:"
        f" the bare mode {omega_b:.5f}; the coupled map's eigenvalue nearest it {np.angle(nearest):.5f}"
        f" (|lambda| {abs(nearest):.6f}); the block's summed record's peak {peak:.5f} ({peak / omega_b:.4f} of the bare);"
        f" the envelope's decay {rate:.2e} per interval. The PIN of the atom's world: its lines at the COUPLED"
        f" modes; the bare 0.09097 is not the line."
    )
    print(
        f"    the SECOND coupled mode (the bare pair at 0.1380 of massive_layer_pins.py): the map's eigenvalue nearest it"
        f" with the largest block weight {np.angle(second):.5f} (the weight {second_w:.4f}; the pair's line, none at the"
        f" difference {np.angle(second) - np.angle(nearest):.4f} in the probe's amplitude by the rule)"
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
    # (e) the light clock's return, and R2's receive at rest, in the click's own form
    train, n_s = 70, 70
    omega_a, norm, offer_cells, offer_face = one_record(673, 700, 600, 600, train=train)
    grace = train + n_s
    clicks_cells = {w: first_rung(offer_cells, norm, w, grace) for w in (64, 256, 1024, 4096)}
    clicks_face = {w: first_rung(offer_face, norm, w, grace) for w in (64, 256, 1024, 4096)}
    print(
        f"(e) the light clock in the click's own form (one record, the train {train}, the grace {grace} = the train + N_s"
        f" with N_s one period; the norm {norm:.3g}): the first rung at A's own cells after the grace, by W:"
        f" {clicks_cells} (2 L / c = {120 * math.sqrt(3):.2f}); at A's face cell alone: {clicks_face}."
        f" THE PIN at W = 64 on A's cells: {clicks_cells[64]} intervals from the record's birth, the band +- 2 (the rung's"
        f" rise between W = 64 and 4096: {clicks_cells[4096]} to {clicks_cells[64]})"
    )
    omega_b2, norm2, offer_a, _ = one_record(2200, 500, 772, 700, train=train)
    clicks_r2 = {w: first_rung(offer_a, norm2, w, 0) for w in (64, 256, 1024, 4096)}
    print(
        f"    R2 at rest (B at [772, 784) emits one cycle, A's cells at [700, 712) the receiver, L = 60): the first rung by W:"
        f" {clicks_r2} against L / c = {60 * math.sqrt(3):.2f}: the rung's rise at W = 64 is {clicks_r2[64] - 60 * math.sqrt(3):+.1f}"
        f" intervals (WITHOUT the ramp; (f) below, with the world's ramp, is the reader's map)"
    )
    # (f) R2's rise per direction: both blocks stepping to k = 3, the emitter's one record
    c_pace, v_pace, gap = 1 / math.sqrt(3), 1 / 3, 60
    wheels = (64, 256, 1024, 4096)
    cases = {
        "rest, B to A": (772, 700, 10**9, gap / c_pace),
        "rest, A to B": (700, 772, 10**9, gap / c_pace),
        "k = 3, A chases B": (700, 772, 3, gap / (c_pace - v_pace)),
        "k = 3, B meets A": (772, 700, 3, gap / (c_pace + v_pace)),
    }
    rises = {}
    r2_f = {}
    r2_face = {}
    print(
        "(f) R2's rise per direction, the click's own form on the chain of 2200 (the blocks at [700, 712) and [772, 784),"
    )
    print(
        "    L = 60, W the wheel; a click is the first rung from the record's birth after a ramp of 1500):"
    )
    for name, (e_lo, r_lo, k_step, transit) in cases.items():
        omega_r2, birth, norm_r2, offer_r2, face_r2 = one_record_moving(
            2200, 1950, e_lo, r_lo, k=k_step, train=train
        )
        clicks = {w: first_rung(offer_r2, norm_r2, w, birth) - birth for w in wheels}
        clicks_face = {w: first_rung(face_r2, norm_r2, w, birth) - birth for w in wheels}
        rises[name] = clicks[64] - transit
        r2_f[name] = clicks
        r2_face[name] = clicks_face
        print(
            f"    {name}: the clicks by W {clicks}; the front's transit {transit:.1f}; the rise at W = 64 {rises[name]:+.1f}"
            f" (omega_b {omega_r2:.5f}, the norm {norm_r2:.3g}); at the free Node adjacent to the receiver's face toward the emitter,"
            f" printed beside and NOT R2's declared set (section 13 item 1: the set stays the block's cells, its own"
            f" records excluded by own_grace = the hold): {clicks_face}"
        )
    t_plus = cases["k = 3, A chases B"][3] + rises["k = 3, A chases B"]
    t_minus = cases["k = 3, B meets A"][3] + rises["k = 3, B meets A"]
    rest_rise = rises["rest, B to A"]
    exact = v_pace / c_pace
    own = sagnac_ratio(cases["k = 3, A chases B"][3], cases["k = 3, B meets A"][3])
    grain = max(
        abs(sagnac_ratio(t_plus + da, t_minus + db) - sagnac_ratio(t_plus, t_minus))
        for da in (-1, 1)
        for db in (-1, 1)
    )
    print(
        f"    THE RATIO at W = 64: from the clicks alone {sagnac_ratio(t_plus, t_minus):.4f}; with the rest rise {rest_rise:+.1f}"
        f" subtracted from both {sagnac_ratio(t_plus - rest_rise, t_minus - rest_rise):.4f}; with each direction's OWN rise"
        f" subtracted {own:.4f} = v / c = {exact:.4f} exactly (the reader of record: the click per direction less"
        f" that direction's rise from this map, COMPUTATION); one interval of the click's grain on each side moves"
        f" the ratio by up to {grain:.4f}, so the band +- 0.01 holds"
    )
    # (g) the declared coupling within the load bound (DECLARATIONS.md section 15 M1-1)
    g_d, big_d, amp_d = 1 / 1000, 1 / 50, 50 * 2**20
    omega_g, norm_g, offer_g, _ = one_record(
        673, 700, 600, 600, g=g_d, big_g=big_d, amp=amp_d, train=train
    )
    clicks_g = {w: first_rung(offer_g, norm_g, w, grace) for w in wheels}
    r2_g = {}
    for name, (e_lo, r_lo, k_step, _transit) in cases.items():
        _, birth_g, norm_r, offer_r, _face_g = one_record_moving(
            2200, 1950, e_lo, r_lo, k=k_step, g=g_d, big_g=big_d, amp=amp_d, train=train
        )
        r2_g[name] = {w: first_rung(offer_r, norm_r, w, birth_g) - birth_g for w in wheels}
    same = clicks_g == clicks_cells and r2_g == r2_f
    print(
        f"(g) the declared coupling G = [1, 50], g = [1, 1000], the seed 50 x 2^20 (the same world as G = [1, 1],"
        f" g = [1, 50000], seed 2^20 by the exact rescaling of the massive rows by 50): the light clock's first"
        f" rung by W {clicks_g} against (e)'s {clicks_cells}; R2's clicks by case "
        + "; ".join(f"{k}: {v}" for k, v in r2_g.items())
        + f" against (f)'s: {'IDENTICAL' if same else 'DIFFERENT'} (the light's norm {norm_g:.4g} against {norm:.4g})"
    )
    print(f"HOST {time.time() - t0:.0f} s")
