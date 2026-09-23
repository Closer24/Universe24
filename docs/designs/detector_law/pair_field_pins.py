"""COMPUTATION (not an engine run): the pins of the hypothesis THE PAIR AS A FIELD
(docs/designs/detector_law/PAIR_FIELD.md, the identity pair-field-v1, outside the law),
computed from the algebra before any run, on the owner's word of 2026-09-23 (about
20:40Z, "go for it").

The hypothesis: the pair's deviation is a third record kind on the board, massless (the
pair [1, 1]), under the same six-neighbour rule, sourced by every block's content M at
its cells (a static source); every Node reads it as its own pair: the massive kind's
pitch is lowered, omega_0(r) = max(omega_0 - delta(r), 0) (the pair cannot pass light,
cos <= 1), and light reads it through the medium's declared coupling. Its static shape
is the lattice Green's function of the six-neighbour Laplacian, phi(r), which tends to
1 / (4 pi r); delta(r) = 4 pi kappa phi(r) with kappa the source's declared strength.

Printed, each a COMPUTATION with its kind:
  (a) the field's shape: phi on a periodic box (a unit source, the background subtracted),
      gauged to the infinite lattice by Watson's constant phi(0) = 0.252731 (the exact
      value; the identity 6 phi(0) - 6 phi(1) = 1 is checked), r phi(r) along an axis and
      a diagonal against 1 / (4 pi) (isotropy under the 48);
  (b) the clock in the field (row 12's form): the pitch's shift at r and 2 r, the ratio
      2.00 for a 1 / r field, and the lattice's number;
  (c) the bending against the clock (row 13): the medium's index n_m^2 = 1 + G g /
      (omega_0^2 - omega^2) shifts with the pitch; 1 + gamma_eff = (dn / d omega_0) omega_0
      / n_m in the long-wave limit = (n_m^2 - 1) / n_m: ONE declared input (the medium's
      coupling) fixes it; nature's 2 needs n_m = 1 + sqrt 2;
  (d) the 1 / r well's ladder (row 6): the massive kind's lowest modes in the field of a
      point source; the Bohr radius a_B = c^2 cot omega_0 / kappa Links, the reduced
      Compton length lambda_C = c / omega_0 = 3.87 Links, alpha_eff = lambda_C / a_B;
      the rungs n = 1 (one level) and n = 2 (four), E_1 / E_2 against hydrogen's 4 in
      the weak limit (alpha_eff -> 0; the weak limit is the Schroedinger ladder, a
      theorem, not computed here); the n >= 3 rungs need a larger board (HOST);
  (e) two and four sources at contact (rows 7a, 7b): the lowest mode's binding per
      source against one source; the alpha-to-deuteron ratio per nucleon (nature 6.4).

    PYTHONPATH=src python docs/designs/detector_law/pair_field_pins.py
"""

import math
import time

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

MU = 0.15
COS_W0 = 1 / (1 + MU**2 / 2)
W0 = math.acos(COS_W0)
C2 = 1 / 3
WATSON = 0.2527310098  # the simple cubic lattice's Green's function at the source


def green(n):
    """The lattice Green's function of the six-neighbour Laplacian: a unit source at the
    origin on a periodic n^3 box (FFT, the uniform background subtracted), gauged to the
    infinite lattice by phi(0) = WATSON; the periodic images' error is O(r^2 / n^3)."""
    k = 2 * np.pi * np.fft.fftfreq(n)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    lam = 6 - 2 * (np.cos(kx) + np.cos(ky) + np.cos(kz))
    src = np.zeros((n, n, n))
    src[0, 0, 0] = 1.0
    src -= 1.0 / n**3
    f = np.fft.fftn(src)
    with np.errstate(divide="ignore", invalid="ignore"):
        g = np.where(lam > 1e-12, f / lam, 0.0)
    phi = np.real(np.fft.ifftn(g))
    return phi + (WATSON - phi[0, 0, 0])


def pitch_cos(delta):
    """The massive kind's cosine at each Node: the pitch lowered by delta, floored at 0."""
    return np.cos(np.maximum(W0 - delta, 0.0))


def lowest_modes(n, cosw, k, tol=1e-8):
    """The lowest k modes of the massive kind with the per-Node cosine cosw:
    2 cosw a = S_6 a / 3 at each Node; the symmetric form A = C^-1/2 (S_6 / 3) C^-1/2
    with C = 1 / cosw, the largest eigenvalues 2 cos omega."""
    d = np.sqrt(cosw)

    def matvec(v):
        a = d * v.reshape(n, n, n)
        s6 = sum(np.roll(a, sh, ax) for ax in range(3) for sh in (1, -1))
        return (d * s6 / 3).ravel()

    A = LinearOperator((n**3, n**3), matvec=matvec, dtype=float)
    vals = eigsh(
        A, k=k, which="LA", tol=tol, ncv=max(2 * k + 1, 40), maxiter=20000, return_eigenvectors=False
    )
    return np.sort(np.arccos(np.clip(vals / 2, -1, 1)))


def well(phi, a_b):
    """The source of strength kappa for the Bohr radius a_b: delta(r) = 4 pi kappa phi(r)."""
    kappa = C2 / (math.tan(W0) * a_b)
    return kappa, 4 * math.pi * kappa * phi


if __name__ == "__main__":
    t0 = time.time()
    n = 120
    phi = green(n)
    print(
        f"(a) the lattice Green's function on {n}^3 (unit source, gauged to phi(0) = {WATSON}):"
        f" 6 phi(0) - 6 phi(1) = {6 * (phi[0, 0, 0] - phi[1, 0, 0]):.5f} (1 exactly on the infinite lattice)"
    )
    print(
        "    r | r phi(r) along an axis | |r| phi along a diagonal (the 1 / (4 pi) = 0.07958 limit; isotropy under the 48)"
    )
    for r in (1, 2, 3, 4, 6, 8, 12, 16, 24):
        ax = phi[r, 0, 0] * r
        diag = phi[r, r, r] * r * math.sqrt(3)
        print(f"    {r:2d} | {ax:.5f} | {diag:.5f}")
    print(
        "(b) the clock in the field (row 12): the pitch's shift delta(r) = 4 pi kappa phi(r); the ratio of the"
    )
    print(
        "    shifts at r and 2 r (a 1 / r field gives 2.00): ",
        ", ".join(f"r = {r}: {phi[r, 0, 0] / phi[2 * r, 0, 0]:.4f}" for r in (2, 4, 8, 12)),
    )
    for nm in (1.5, 2.0, 1 + math.sqrt(2), 3.0):
        print(
            f"(c) the bending against the clock (row 13): with the medium's index n_m = {nm:.4f}, 1 + gamma_eff = (n_m^2 - 1) / n_m = {(nm * nm - 1) / nm:.4f}"
            + ("  <- nature's 2" if abs(nm - 1 - math.sqrt(2)) < 1e-9 else "")
        )
    # (d) the 1 / r well's ladder
    a_b = 8.0
    kappa, delta = well(phi, a_b)
    lam_c = math.sqrt(C2) / W0
    r_cap = int(np.sum(delta[:, 0, 0][: n // 2] >= W0))
    t1 = time.time()
    modes = lowest_modes(n, pitch_cos(delta), 6)
    e = modes - W0
    print(
        f"(d) the 1 / r well's ladder on {n}^3 at a_B = {a_b} Links (kappa = {kappa:.4f}; lambda_C = {lam_c:.2f} Links,"
        f" alpha_eff = {lam_c / a_b:.3f}; the pitch floored at 0 within r <= {r_cap} of the source; eigsh {time.time() - t1:.0f} s):"
    )
    print(
        "    the 6 lowest levels E_n = omega_n - omega_0 (the rungs 1, 4 as hydrogen's n = 1, 2; then the next):"
    )
    print("    " + ", ".join(f"{x:.5f}" for x in e))
    e1 = e[0]
    e2 = np.mean(e[1:5])
    print(
        f"    E_1 / E_2 = {e1 / e2:.3f} (hydrogen 4.000 in the weak limit); the n = 2 group's spread {np.ptp(e[1:5]) / abs(e2):.3f}"
    )
    print(
        f"    the continuum's E_1 = -kappa / (2 a_B) = {-kappa / (2 * a_b):.5f} against the lattice's {e1:.5f}"
    )
    # (e) two and four sources at contact
    n2 = 64
    phi2 = green(n2)
    a_b2 = 8.0

    def field_of(points):
        f = np.zeros((n2, n2, n2))
        for p in points:
            f += np.roll(np.roll(np.roll(phi2, p[0], 0), p[1], 1), p[2], 2)
        return f

    results = {}
    d_c = 4
    for name, pts in (
        ("one", [(0, 0, 0)]),
        (f"two at d = {d_c}", [(0, 0, 0), (d_c, 0, 0)]),
        (
            f"four at d = {d_c} (the origin and its three axes)",
            [(0, 0, 0), (d_c, 0, 0), (0, d_c, 0), (0, 0, d_c)],
        ),
    ):
        _, dl = well(field_of(pts), a_b2)
        m = lowest_modes(n2, pitch_cos(dl), 1)
        results[name] = m[0] - W0
        print(
            f"(e) {name}: the lowest level E_1 = {results[name]:.5f} on {n2}^3 at a_B = {a_b2} per source"
        )
    keys = list(results)
    b2 = results[keys[0]] - results[keys[1]]
    b4 = results[keys[0]] - results[keys[2]]
    print(
        f"    the binding per source against one source: two {b2:.5f}, four {b4:.5f}; the ratio four / two = {b4 / b2:.3f}"
        " (nature's alpha / deuteron per nucleon 6.4; the algebra's number a PREDICTION of the declared contact)"
    )
    print(f"HOST {time.time() - t0:.0f} s")
