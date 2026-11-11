"""Passive exact checks: Bianchi identity, torus source obstruction, lattice stress.

This is not an Engine construction or a proof of an Einstein matter sector.
"""
from pathlib import Path
import hashlib
import json
import numpy as np


def d(f, mu):
    return np.roll(f, -1, axis=mu) - np.roll(f, 1, axis=mu)


def dd(f, mu, nu):
    return d(d(f, nu), mu)


def peak(f):
    return max(abs(int(v)) for v in f.flat)


def run():
    L = 5
    eta = [-1, 1, 1, 1]
    rng = np.random.default_rng(73239)
    raw = rng.integers(-3, 4, size=(4, 4, L, L, L, L)).astype(object)
    h = raw + raw.swapaxes(0, 1)
    trace = sum(eta[m] * h[m, m] for m in range(4))
    R2 = np.empty_like(h)
    for m in range(4):
        for n in range(4):
            R2[m, n] = sum(eta[s] * (dd(h[s, m], s, n) + dd(h[s, n], s, m))
                           for s in range(4)) - dd(trace, m, n) \
                       - sum(eta[s] * dd(h[m, n], s, s) for s in range(4))
    scalar2 = sum(eta[m] * R2[m, m] for m in range(4))
    G4 = 2 * R2
    for m in range(4):
        G4[m, m] -= eta[m] * scalar2
    divG = [sum(eta[m] * d(G4[m, n], m) for m in range(4)) for n in range(4)]
    assert all(peak(f) == 0 for f in divG)
    spatial_trace = sum(h[i, i] for i in range(1, 4))
    C = sum(dd(h[i, j], i, j) for i in range(1, 4) for j in range(1, 4)) \
        - sum(dd(spatial_trace, i, i) for i in range(1, 4))
    assert np.array_equal(G4[0, 0], 2 * C)
    mean00 = [int(sum(G4[0, 0, t].flat)) for t in range(L)]
    assert mean00 == [0] * L

    # Two non-collinear, exact lattice-null scalar waves. They solve Box chi=0,
    # but their ordinary pointwise continuum-form stress is not conserved.
    t, x, y, z = np.indices((L, L, L, L))
    f = np.array([0, 1, -2, 3, -1], dtype=object)
    g = np.array([2, -1, 0, 1, -2], dtype=object)
    chi = f[(t + x) % L] + g[(t + y) % L]
    box = sum(eta[m] * dd(chi, m, m) for m in range(4))
    assert peak(box) == 0
    derivatives = [d(chi, m) for m in range(4)]
    kinetic = sum(eta[m] * derivatives[m] ** 2 for m in range(4))
    T2 = np.empty_like(h)
    for m in range(4):
        for n in range(4):
            T2[m, n] = 2 * derivatives[m] * derivatives[n]
            if m == n:
                T2[m, n] -= eta[m] * kinetic
    divT = [sum(eta[m] * d(T2[m, n], m) for m in range(4)) for n in range(4)]
    assert any(peak(v) for v in divT)
    assert all(int(v) >= 0 for v in T2[0, 0].flat)
    energy = [int(sum(T2[0, 0, t].flat)) for t in range(L)]
    assert all(v > 0 for v in energy)

    # Direct phase-probe reciprocal source at c=1,s=0: diag(H,-H,0).
    pulse = np.zeros((L, L, L), dtype=object)
    pulse[0, 0, 0] = 1
    H = sum(sign * (np.roll(pulse, shift, axis=axis) - pulse) ** 2
            for axis, sign in [(0, 1), (1, -1)] for shift in [-1, 1])
    source_div = [d(H, 0), -d(H, 1), np.zeros_like(H)]
    assert any(peak(v) for v in source_div)

    # Nontrivial algebraic repair: transverse checkerboard gives planar H.
    Le = 4
    x, y, z = np.indices((Le, Le, Le))
    psi = np.array([1, -2, 0, 3], dtype=object)
    checker = (-1) ** x * psi[z]
    Hcheck = sum(sign * (np.roll(checker, shift, axis=axis) - checker) ** 2
                 for axis, sign in [(0, 1), (1, -1)] for shift in [-1, 1])
    assert np.array_equal(Hcheck, 8 * psi[z] ** 2)
    assert peak(d(Hcheck, 0)) == peak(d(Hcheck, 1)) == 0
    return {
        "scope": "Exact passive algebra, not Engine or physical Einstein-sector certification",
        "L": L,
        "difference": "delta_mu = shift_plus_mu - shift_minus_mu; common rescalings omitted",
        "random_symmetric_metric_bianchi_residuals": [peak(v) for v in divG],
        "Hamiltonian_identity_G4_00_equals_2_C": True,
        "spatial_sums_G4_00": mean00,
        "two_crossing_scalar_waves_Box_residual": peak(box),
        "ordinary_pointwise_scalar_stress_divergence_peaks": [peak(v) for v in divT],
        "positive_scalar_energy_sums_T2_00": energy,
        "direct_reciprocal_TT_source_divergence_peaks": [peak(v) for v in source_div],
        "checkerboard_restricted_source_H_equals_8_psi_squared": True,
        "checkerboard_restricted_source_transverse_divergence_zero": True,
        "limitations": [
            "The Bianchi and torus identities follow algebraically for all periodic h; random h is only an executable control.",
            "A shifted/staggered stress could repair pointwise stress conservation; none is supplied here.",
            "The checkerboard source preserves raw planar TT shape, not the metric phase decoder, sourced Einstein equations, or positive metric signature.",
            "Neither Q nor a coefficient resolution lift changes these compatibility identities."
        ],
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=Path("runs/constraint-geometry/exact_constraint_audit.json"))
    args = parser.parse_args()
    result = run()
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path = args.out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
