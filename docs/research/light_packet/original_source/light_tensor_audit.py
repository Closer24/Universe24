"""Research candidate: fixed-six, 18-channel Maxwell test field.

Run with Universe24 e582960 on PYTHONPATH, numpy and sympy installed.
This is a new proposal, NOT an accepted coupled Einstein model.
Only the unchanged Universe24 Engine advances retained states.
The exact Maxwell interpretation is proved on a finite prepared horizon.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run

SOURCE_PIN = "e582960f6c9d2d134d3d6b28c08494e8bfafa86a"
PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
CG = {pair: 12 + i for i, pair in enumerate(PAIRS)}
CG.update({(j, i): CG[i, j] for i, j in PAIRS})
EPS = ((0, 1, 2, 1), (0, 2, 1, -1), (1, 2, 0, 1),
       (1, 0, 2, -1), (2, 0, 1, 1), (2, 1, 0, -1))
ZERO = (0, 0, 0)


def tensor():
    names = [f"{bank}_{field}{i}" for bank in ("X", "Y")
             for field in ("D", "B") for i in range(3)]
    names += [f"C{i}{j}" for i, j in PAIRS]
    terms = []
    for bank, sign in ((0, 1), (1, -1)):
        dst, src = 6*bank, 6*(1-bank)
        for field in (0, 3):
            for i in range(3):
                terms.append((dst+field+i, 6, [(src+field+i, ZERO, "b")]))
            for i, j, k, epsilon in EPS:
                for ell in range(3):
                    for shift in (-1, 1):
                        offset = tuple(shift if a == j else 0 for a in range(3))
                        terms.append((dst+field+i, sign*epsilon*shift,
                                      [(CG[k, ell], offset, "b"),
                                       (src+(3-field)+ell, offset, "b")]))
    for g in range(12, 18):
        terms.append((g, 6, [(g, ZERO, "b")]))
    return Tensor([GearType(name, "audit") for name in names], terms,
                  strict_support=True)


def curl(v, L):
    """Independent array oracle: D_j=S_j^+ - S_j^- (no 1/(2h))."""
    grid = np.asarray(v, dtype=object).reshape(3, L, L, L)
    out = np.zeros_like(grid)
    for i, j, k, sign in EPS:
        out[i] += sign*(np.roll(grid[k], -1, axis=j)-np.roll(grid[k], 1, axis=j))
    return out.reshape(3, L**3)


def divergence(v, L):
    grid = np.asarray(v, dtype=object).reshape(3, L, L, L)
    return sum(np.roll(grid[j], -1, axis=j)-np.roll(grid[j], 1, axis=j)
               for j in range(3)).reshape(L**3)


def constitutive(rows, v):
    return np.asarray([sum(rows[CG[i, j]]*v[j] for j in range(3))
                       for i in range(3)], dtype=object)


def divided_three(v):
    assert all(int(x) % 3 == 0 for x in v.flat), "exact preparation horizon exhausted"
    return v//3


def ideal(current, L, inverse=False):
    # F(X,Y)=(K(Y),L(X)); F^-1(X,Y)=(L^-1(Y),K^-1(X)).
    current = np.asarray(current, dtype=object)
    out = current.copy()
    out[:6], out[6:12] = current[6:12].copy(), current[:6].copy()
    if not inverse:
        out[:3] += divided_three(curl(constitutive(current, current[9:12]), L))
        out[9:12] -= divided_three(curl(constitutive(current, current[:3]), L))
    else:
        out[3:6] += divided_three(curl(constitutive(current, current[6:9]), L))
        out[6:9] -= divided_three(curl(constitutive(current, current[3:6]), L))
    return out


def prepare(L, ticks, C, seed_number=24, spatial=False):
    assert ticks % 2 == 0
    Q = 3**(ticks+1)
    rng = np.random.default_rng(seed_number)
    current = np.zeros((18, L**3), dtype=object)
    for i, j in PAIRS:
        current[CG[i, j], :] = int(C[i, j])
    if spatial:
        x = np.indices((L, L, L))[0].reshape(-1)
        current[CG[0, 0]] += (x == L//2).astype(object)
    # One physical population: X at even ticks, Y at odd circuit stages.
    current[:3] = Q*curl(rng.integers(-3, 4, (3, L**3)).astype(object), L)
    current[3:6] = Q*curl(rng.integers(-3, 4, (3, L**3)).astype(object), L)
    previous = ideal(current, L, inverse=True)
    carries = np.asarray([[(g+n) % 6 for n in range(L**3)] for g in range(18)], dtype=object)
    return State(L, previous, current, carries), Q


def energy_ledger(current, L):
    D, B = current[:3], current[3:6]
    CD, CB = constitutive(current, D), constitutive(current, B)
    cross = constitutive(current, curl(CB, L))
    # Six times the modified symplectic energy. Exact, not the continuum energy.
    return int(3*sum((D*CD+B*CB).flat)-sum((D*cross).flat))


def symbolic_identity():
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    x, y, z = sp.symbols("kx ky kz")
    C = sp.Matrix([[a, d, e], [d, b, f], [e, f, c]])
    k = sp.Matrix([x, y, z])
    cross = sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    adj = C.adjugate()
    kappa2 = (k.T*adj*k)[0]
    residual = -cross*C*cross*C-kappa2*sp.eye(3)+(adj*k)*k.T
    assert all(sp.expand(v) == 0 for v in residual)
    # Verify the symplectic macro's exact invariant, independently as a 2x2 mode.
    q = sp.symbols("q", real=True)
    M = sp.Matrix([[1-q*q, q], [-q, 1]])
    W = sp.Matrix([[1, -q/2], [-q/2, 1]])
    assert sp.simplify(M.T*W*M-W) == sp.zeros(2)
    return {"general_symmetric_C_identity": "passed", "nine_residuals": [0]*9,
            "transverse_dispersion": "omega^2 = k^T adj(C) k",
            "physical_polarizations": 2, "modified_energy_identity": "passed",
            "metric": "g = Omega^2 diag(-1, C/det(C)); C positive definite",
            "conformal_scale_from_light_alone": "undetermined"}


def exact_engine_audit(law, C, ticks=60, L=7, spatial=False):
    state, Q = prepare(L, ticks, C, spatial=spatial)
    seed, engine = state.copy(), Engine(law)
    initial_energy = energy_ledger(state.b, L)
    peak_bits = 0
    changed_nodes = 0
    for tick in range(ticks):
        oracle = ideal(state.b, L)
        following = engine.step(state)
        assert np.array_equal(following.b, oracle)
        assert np.array_equal(following.r, seed.r)
        assert engine.inverse_step(following).same_as(state)
        changed_nodes += int(np.count_nonzero(np.any(following.b[:12] != state.b[:12], axis=0)))
        state = following
        peak_bits = max(peak_bits, max(abs(int(v)).bit_length()
                       for bank in (state.a, state.b) for v in bank.flat))
        active = 0 if (tick+1) % 2 == 0 else 6
        assert not any(divergence(state.b[active:active+3], L))
        assert not any(divergence(state.b[active+3:active+6], L))
        if (tick+1) % 2 == 0:
            assert energy_ledger(state.b, L) == initial_energy
            assert not any(state.b[6:12].flat)
    assert engine.rewind(state, ticks).same_as(seed)
    return {"L": L, "ticks": ticks, "macrosteps": ticks//2,
            "C": np.asarray(C).tolist(), "Q": str(Q), "Q_bits": Q.bit_length(),
            "spatial_Cxx_step": spatial,
            "peak_integer_bits": peak_bits, "field_comparisons": ticks*12*L**3,
            "changed_node_ticks": changed_nodes, "exact_first_order_oracle": "passed",
            "complete_inverse_and_rewind": "passed", "all_six_carries_retained": "passed",
            "both_divergence_constraints": "passed", "modified_energy_conservation": "passed",
            "scope": "finite prepared horizon; static integer C; no Einstein source closure"}


def dispersion(C):
    adj = np.array(sp.Matrix(C.tolist()).adjugate(), dtype=float)
    k = np.array([1., 1., 2.])
    continuum = math.sqrt(float(k@adj@k))
    rows = []
    for N in (16, 32, 64, 128):
        h = 2*math.pi/N
        s = np.sin(h*k)
        omega = (3/h)*math.asin(math.sqrt(float(s@adj@s))/3)
        rows.append({"N": N, "omega": omega, "relative_error": abs(omega/continuum-1)})
    ratios = [rows[i]["relative_error"]/rows[i+1]["relative_error"] for i in range(3)]
    assert all(3.8 < value < 4.2 for value in ratios)
    corners = [np.array([x, y, z]) for x in (-1., 1.) for y in (-1., 1.) for z in (-1., 1.)]
    max_q = max(float(s@adj@s) for s in corners)
    assert max_q < 9, "strict frozen-coefficient CFL fails"
    return {"direction": k.tolist(), "continuum_omega": continuum,
            "rows": rows, "error_ratios": ratios,
            "max_s_adjugate_s": max_q, "stability_requires_less_than": 9,
            "method": "analytic discrete symbol, not refined Engine packet trajectories",
            "grid_artifact": "centered curl has additional zero modes at Nyquist; long-wave sector only"}


def negative_controls(law):
    C = np.array([[2, 1, 0], [1, 1, 0], [0, 0, 1]])
    k = sp.Matrix([1, 1, 2])
    correct = int((k.T*sp.Matrix(C.tolist()).adjugate()*k)[0])
    wrong = int((k.T*k)[0])
    assert correct == 5 and wrong == 6
    same_field_1, _ = prepare(5, 4, np.eye(3, dtype=int))
    same_field_2, _ = prepare(5, 4, C)
    assert np.array_equal(same_field_1.b[:12], same_field_2.b[:12])
    next_1 = Engine(law).run(same_field_1, 2)
    next_2 = Engine(law).run(same_field_2, 2)
    geometry_sensitive = int(np.count_nonzero(next_1.b[:6] != next_2.b[:6]))
    assert geometry_sensitive > 0
    seed, _ = prepare(5, 4, np.eye(3, dtype=int))
    bad = seed.copy()
    bad.a[0, 0] += 1
    after = Engine(law).step(bad)
    oracle = ideal(bad.b, 5)
    assert not np.array_equal(after.b, oracle)
    assert Engine(law).inverse_step(after).same_as(bad)
    # Empty tensor is mechanically legal and does not propagate: Rule3 alone is insufficient.
    empty = Tensor([GearType("scalar", "audit")], [], strict_support=True)
    initial = np.zeros((1, 27), dtype=object)
    initial[0, 0] = 1
    s = State(3, initial, initial.copy(), np.zeros_like(initial))
    for _ in range(8):
        s = Engine(empty).step(s)
        assert not any(s.b[0, 1:])
    return {"wrong_identity_metric_rejected": {"correct_omega_squared": correct, "wrong": wrong},
            "same_field_different_C_changes_actual_Engine": geometry_sensitive,
            "off_preparation_breaks_Maxwell_but_rewinds": True,
            "Rule3_without_coupling_has_no_transport": True,
            "large_C_counterexample": "C=2I gives max(s^T adj(C)s)=12>9: unstable modes"}


def saved_run(law, out):
    seed, Q = prepare(5, 6, np.eye(3, dtype=int))
    channels = [{"index": i, "name": g.name, "label": g.label,
                 "owner": "electromagnetic_staging" if i < 12 else "static_optical_geometry",
                 "purpose": "finite-horizon research test field"} for i, g in enumerate(law.gears)]
    bundle = create_bundle(law, seed, channels=channels, protocol=default_protocol(),
                           model={"id": "research-maxwell18-static-optical", "version": "1",
                                  "domain": "finite prepared horizon; no gravity backreaction",
                                  "Q": str(Q), "microticks_per_macro": 2})
    run_bundle(bundle, out, steps=6)
    verified = verify_run(out)
    return verified


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    law = tensor()
    assert law.G == 18 and law.rank-1 == 2 and not law.support_violations()
    report = {"status": "research_proposal_not_general_physical_acceptance",
              "source_pin": SOURCE_PIN, "tensor_hash": law.fingerprint,
              "channels": law.G, "retained_integers_per_node": 3*law.G,
              "monomials": len(law.monomials), "max_degree": law.rank-1,
              "strict_face_locality": "passed", "old_a_dependencies": False,
              "symbolic": symbolic_identity(), "cases": []}
    for C in (np.eye(3, dtype=int), np.array([[2, 1, 0], [1, 1, 0], [0, 0, 1]])):
        report["cases"].append({"engine": exact_engine_audit(law, C), "dispersion": dispersion(C)})
    report["static_nonuniform_case"] = exact_engine_audit(
        law, np.eye(3, dtype=int), ticks=24, L=5, spatial=True)
    report["negative_controls"] = negative_controls(law)
    report["saved_run_verification"] = saved_run(law, args.out/"runtime")
    report["unresolved"] = ["dynamic and Einstein-sourced C", "operational material clocks and detectors",
                             "conformal scale", "infinite-time interpretation with fixed Q",
                             "full packet trajectory convergence on nonuniform curved backgrounds",
                             "removal or physical exclusion of high-frequency lattice species",
                             "quantum photon statistics"]
    (args.out/"tensor.json").write_text(json.dumps(law.to_dict(), indent=2))
    report["audit_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (args.out/"results.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"channels": report["channels"], "monomials": report["monomials"],
                      "cases": report["cases"], "saved_run": report["saved_run_verification"]}, indent=2))


if __name__ == "__main__":
    main()
