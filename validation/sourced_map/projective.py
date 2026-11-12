"""Exact integer scaling for the joined sourced massless volume map.

No projective denominator update or competing tensor is introduced. The
phase-space coordinate J is decoded from the native volume's two histories.
Run: python -m validation.sourced_map.projective
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PIN = "f4f64e062f07b3ca119eccf655df746be206908b"


def _integer(value, name):
    if type(value) is not int:
        raise ValueError(f"{name} must be an exact Python integer")
    return value


def _resolution(N):
    _integer(N, "N")
    if N <= 0:
        raise ValueError("N must be positive")


def history_to_phase(old_volume: int, volume: int, dust_charge: int) -> int:
    """J=4N U from both volume histories, on the constant-source graph."""
    for value, name in ((old_volume, "old_volume"), (volume, "volume"),
                        (dust_charge, "dust_charge")):
        _integer(value, name)
    return volume-old_volume+3*dust_charge


def phase_to_history(volume: int, velocity: int, dust_charge: int) -> int:
    for value, name in ((volume, "volume"), (velocity, "velocity"),
                        (dust_charge, "dust_charge")):
        _integer(value, name)
    return volume-velocity+3*dust_charge


def affine_step(volume: int, velocity: int, dust_charge: int, *, inverse=False):
    for value, name in ((volume, "volume"), (velocity, "velocity"),
                        (dust_charge, "dust_charge")):
        _integer(value, name)
    if type(inverse) is not bool:
        raise ValueError("inverse must be Boolean")
    if inverse:
        return volume-velocity+3*dust_charge, velocity-6*dust_charge
    return volume+velocity+3*dust_charge, velocity+6*dust_charge


def invariant_jet(volume: int, velocity: int, dust_charge: int, scalar_charge: int, N: int) -> int:
    _resolution(N)
    for value, name in ((volume, "volume"), (velocity, "velocity"),
                        (dust_charge, "dust_charge"), (scalar_charge, "scalar_charge")):
        _integer(value, name)
    return velocity*velocity-12*dust_charge*volume-24*N*N*scalar_charge*scalar_charge


def constraint_numerator(old_volume: int, volume: int, dust_charge: int, scalar_charge: int, N: int) -> int:
    return invariant_jet(volume, history_to_phase(old_volume, volume, dust_charge),
                         dust_charge, scalar_charge, N)


def encode_initial(V, U, D: int, P: int, N: int):
    """M=1 unit convention; explicit exact representability, no rounding."""
    _resolution(N)
    _integer(D, "D")
    _integer(P, "P")
    if isinstance(V, (float, bool)) or isinstance(U, (float, bool)):
        raise ValueError("Use exact rational initial V and U")
    V, U = F(V), F(U)
    if V <= 0 or D < 0:
        raise ValueError("Physical preparation needs V>0 and D>=0")
    q, j = 4*N*N*V, 4*N*U
    if q.denominator != 1 or j.denominator != 1:
        raise ValueError("Initial V or U is not exactly representable at this N")
    q, j = int(q), int(j)
    if invariant_jet(q, j, D, P, N) != 0:
        raise ValueError("Initial Einstein constraint is nonzero")
    return {"old_volume": phase_to_history(q, j, D), "volume": q,
            "velocity": j, "dust_charge": D, "scalar_charge": P,
            "reference_velocity": j}


def symbolic_audit():
    q, old, j, D, P, N = s.symbols("q old j D P N", real=True)
    I = j*j-12*D*q-24*N*N*P*P
    qnext, jnext = q+j+3*D, j+6*D
    assert s.expand(I.subs({q: qnext, j: jnext}, simultaneous=True)-I) == 0
    qprev, jprev = q-j+3*D, j-6*D
    assert s.expand(qnext.subs({q: qprev, j: jprev}, simultaneous=True)-q) == 0
    assert s.expand(jnext.subs({q: qprev, j: jprev}, simultaneous=True)-j) == 0
    jhistory = q-old+3*D
    native_next = 2*q+6*D-old
    assert s.expand(native_next-(qnext.subs(j, jhistory))) == 0
    assert s.expand(native_next-q+3*D-(jhistory+6*D)) == 0

    V, U, h = s.symbols("V U h", nonzero=True, real=True)
    C = U*U-s.Rational(3, 2)*P*P-3*D*V
    Vnext, Unext = V+h*U+s.Rational(3, 4)*D*h*h, U+s.Rational(3, 2)*D*h
    assert s.expand(C.subs({V: Vnext, U: Unext}, simultaneous=True)-C) == 0
    assert s.simplify((4*N*N*Vnext).subs(h, 1/N)
                      -(4*N*N*V+4*N*U+3*D)) == 0
    assert s.simplify((4*N*Unext).subs(h, 1/N)-(4*N*U+6*D)) == 0
    k, p = -U/(3*V), P/V
    dt = lambda expr: s.diff(expr, V)*U+s.diff(expr, U)*3*D/2
    assert s.simplify(dt(k)-(3*k*k-D/(2*V))) == 0
    assert s.simplify(dt(p)-3*k*p) == 0
    assert s.simplify(dt(D/V)-3*k*D/V) == 0
    # Differentiating B=V^(-1/3), d=sqrt(D/V) gives Bdot=kB,
    # ddot=3kd/2 on the positive real branches; use logarithmic derivatives.
    assert s.simplify(-U/(3*V)-k) == 0
    assert s.simplify(-U/(2*V)-3*k/2) == 0
    H = 6*k*k-p*p-2*D/V
    assert s.simplify(H-2*C/(3*V*V)) == 0
    rawH = H.subs({V: q/(4*N*N), U: j/(4*N)}, simultaneous=True)
    assert s.simplify(rawH-2*N*N*I/(3*q*q)) == 0
    # The exact six-field massive source has an additional -mu*phi^2 term.
    mu, phi = s.symbols("mu phi", real=True)
    assert s.simplify((6*k*k-p*p-mu*phi*phi-2*D/V)-H) == -mu*phi*phi
    return {"affine_inverse": True, "constraint_invariant": True,
            "history_phase_bijection": True,
            "physical_constraint": "H = 2*N^2*I/(3*q^2)",
            "I": "(b_volume-a_volume+3D)^2-12D*b_volume-24N^2*P^2",
            "exact_flow": "V'=V+hU+3Dh^2/4; U'=U+3Dh/2",
            "native_volume": "b'=2b+6D-a; u=6b+18D",
            "source_ODE_identities": "kdot=3k^2-d^2/2; pdot=3kp; ddot=3kd/2; Bdot=kB",
            "massive_gate": "not this law: mass_squared must be zero"}


def arithmetic_audit():
    rows = []
    for D in (1, 2, 5):
        for P in (-3, -1, 0, 2):
            for sign in (-1, 1):
                U = F(sign*(2*abs(P)+3))
                V = (U*U-F(3, 2)*P*P)/(3*D)
                N = 6*V.denominator
                seed = encode_initial(V, U, D, P, N)
                q, j = seed["volume"], seed["velocity"]
                q0, j0 = q, j
                for _ in range(5):
                    old = phase_to_history(q, j, D)
                    nQ, nJ = affine_step(q, j, D)
                    assert nQ == 2*q+6*D-old
                    assert history_to_phase(q, nQ, D) == nJ
                    assert affine_step(nQ, nJ, D, inverse=True) == (q, j)
                    assert invariant_jet(nQ, nJ, D, P, N) == 0
                    q, j = nQ, nJ
                for _ in range(5):
                    q, j = affine_step(q, j, D, inverse=True)
                assert (q, j) == (q0, j0)
                rows.append({"D": D, "P": P, "V": str(V), "U": str(U),
                             "N": N, "constraint": 0, "steps": 5})
    refinement = []
    for N in (24, 48, 96):
        initial = encode_initial(F(1), F(3), 1, 2, N)
        q, j = initial["volume"], initial["velocity"]
        for _ in range(N//8):
            q, j = affine_step(q, j, 1)
        V, U = F(q, 4*N*N), F(j, 4*N)
        assert V == F(355, 256) and U == F(51, 16)
        refinement.append({"N": N, "steps": N//8, "T": "1/8", "V": str(V), "U": str(U)})

    negatives = {}
    for label, args in (("unrepresentable_resolution", (F(1, 7), F(1), 1, 0, 1)),
                        ("constraint_failure", (F(1), F(2), 1, 2, 24)),
                        ("nonpositive_volume", (F(0), F(3), 1, 2, 24))):
        try:
            encode_initial(*args)
        except ValueError as exc:
            negatives[label] = str(exc)
        else:
            raise AssertionError("Invalid exact preparation accepted")
    # A constant source needs both source histories equal. If a_D differs,
    # even the second update is not the claimed affine constant-D flow.
    q, old, D, oldD, P, N = 16, -5, 1, 0, 2, 2
    qnext = 2*q+6*D-old
    Dnext = 2*D-oldD
    jnext_actual = qnext-q+3*Dnext
    jnext_claim = history_to_phase(old, q, D)+6*D
    assert jnext_actual-jnext_claim == 3
    negatives["nonconstant_dust_old_history"] = {"actual_velocity": jnext_actual,
        "constant_source_prediction": jnext_claim, "difference": 3,
        "interpretation": "The exact physical map requires a_D=b_D, not only an acceptable current source."}
    return {"exact_representable_families": rows, "fixed_endpoint_refinement": refinement,
            "negative_controls": negatives,
            "scope": "Independent integer-coordinate oracle; actual Engine proof belongs to the joined native audit."}


def audit():
    result = {"schema": "universe24/sourced-map/projective/1",
              "source_pin": SOURCE_PIN,
              "symbolic": symbolic_audit(), "arithmetic": arithmetic_audit(),
              "actual_domain": {"N": "positive integer", "D_P": "integer conserved coefficients; D>=0",
                "initial": "V>0 rational, U rational, 4N^2 V and4N U integer; U^2=3P^2/2+3DV",
                "pure_massless": "D=0 andP!=0 excluded over rational U,P since(U/P)^2=3/2",
                "branches": "B>0 and positive dust-amplitude decode; contracted/expanded branch must not cross V=0",
                "mass_squared": 0},
              "limitations": ["Same sourced massless six-channel model as native.py; no massive Cayley implementation.",
                 "B,d and scalar phi require passive algebraic/logarithmic readouts; no exact rational field-value claim.",
                 "Source and reference constants must be retained with both histories equal; no hidden initial reference.",
                 "No inference to general spatial Einstein geometry, apparatus or source/matter quantum behavior."]}
    result["source_sha256"] = {str(Path(__file__).relative_to(ROOT)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT/"runs/sourced-map/projective.json")
    args = parser.parse_args()
    report = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"output": str(args.out), "symbolic_invariant": "passed",
                      "exact_seed_families": len(report["arithmetic"]["exact_representable_families"]),
                      "fixed_endpoint_checks": 3, "mass_squared": 0}))


if __name__ == "__main__":
    main()
