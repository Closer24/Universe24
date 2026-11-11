"""Exact, isolated constraint checks for the 48-channel research team.

Run from the repository root:
    python experiments/geometry/team48/constraints_audit.py

This is not a replacement evolution law. The positive ADM result is linearized
and algebraic; the nonlinear, stable, refinable 48-channel Einstein gate stays
open. No floating arithmetic is used in the Engine experiment.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import sympy as sp
import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice


def linearized_null_beam_engine():
    """Exact sourced linearized GR subsector, signed perturbations on a torus.

    hyy=hzz=v, hxx=w, Kyy=Kzz=k, Kxx=l, p=Dv/2, jx=Sxx=rho.
    Other metric, curvature, current and stress components vanish. At h=dx=1,
    prepared right-moving solutions translate one x-cell per Engine step.
    The period-four sign lift was derived by the integer mathematics agent.
    """
    names = ["clock", "hxx", "v", "l", "k", "p", "rho"]
    idx = {name: n for n, name in enumerate(names)}
    zero, plus, minus = (0, 0, 0), (1, 0, 0), (-1, 0, 0)
    # Each coefficient below is 6*f, since u=6*clock.a*clock.b*f(z).
    rhs_terms = [
        ("hxx", -12, "l", zero), ("v", -12, "k", zero),
        ("l", -6, "p", plus), ("l", 6, "p", minus),
        ("l", -6, "rho", zero),
        ("k", -3, "p", plus), ("k", 3, "p", minus),
        ("p", -3, "k", plus), ("p", 3, "k", minus),
        ("rho", -3, "rho", plus), ("rho", 3, "rho", minus),
    ]

    def compile_terms(freeze_density=False):
        terms = [(idx[target], coefficient,
                  ((0, zero, "a"), (0, zero, "b"), (idx[source], offset, "b")))
                 for target, coefficient, source, offset in rhs_terms
                 if not (freeze_density and target == "rho")]
        return Tensor([f"constraints.linear.{name}" for name in names],
                      terms, strict_support=True)

    tensor = compile_terms()
    engine = Engine(tensor)
    lat = lattice(5)
    x = lat.all_coords()[:, 0]
    profile = np.array([0, 4, 0, -4, 0], dtype=object)
    v = profile[x]
    p = (profile[(x+1) % lat.L] - profile[(x-1) % lat.L]) // 4
    rho = -(p[lat.shift_index(plus)] - p[lat.shift_index(minus)])
    zeros = np.zeros(lat.N, dtype=object)
    current = np.stack([zeros, v, zeros, p, p, rho])
    previous = current[:, lat.shift_index(plus)]
    initial = State(5, np.vstack([np.ones(lat.N, dtype=object), -previous]),
                    np.vstack([np.ones(lat.N, dtype=object), current]),
                    [[(g+n) % 6 for n in range(lat.N)] for g in range(7)])

    def decode(state):
        return state.a[0][None, :] * state.b[1:]

    def residuals(physical):
        # Indices here exclude the clock. D2=2*D at dx=1.
        def D2(row):
            return row[lat.shift_index(plus)] - row[lat.shift_index(minus)]
        vv, kk, pp, rr = physical[1], physical[3], physical[4], physical[5]
        values = (-2*D2(pp)-2*rr, -D2(kk)-rr, 4*pp-D2(vv))
        return [max(abs(int(value)) for value in row) for row in values]

    state = initial.copy()
    history = []
    for step in range(21):
        decoded = decode(state)
        expected = current[:, lat.shift_index((-step % lat.L, 0, 0))]
        # shift_index accepts general periodic offsets; tensor factors remain faces.
        assert np.array_equal(decoded, expected)
        residual = residuals(decoded)
        assert residual == [0, 0, 0]
        history.append({"step": step, "H_M_reduction_max_abs": residual})
        if step < 20:
            state = engine.step(state)
    assert np.array_equal(state.r, initial.r)
    for _ in range(20):
        state = engine.inverse_step(state)
    assert state.same_as(initial)

    broken = Engine(compile_terms(freeze_density=True)).step(initial)
    broken_residual = residuals(decode(broken))
    assert broken_residual[0] > 0 and broken_residual[1] > 0
    return {
        "kind": "positive_exact_engine_linearized_sector_with_negative_control",
        "gears": tensor.G, "degree": max(m.degree for m in tensor.monomials),
        "monomials": len(tensor.monomials), "lattice_side": lat.L,
        "steps": 20, "complete_state_rewind": True,
        "integer_density_min_max": [int(rho.min()), int(rho.max())],
        "density_sum": int(sum(rho)),
        "constraint_history": history,
        "frozen_density_control_H_M_reduction": broken_residual,
        "source": "jx=Sxx=rho, rho_dot=-D_x*rho",
        "constraints": ["H=-4*D_x*p-2*rho", "Mx=-2*D_x*k-rho", "p=D_x*v/2"],
        "claim_limits": [
            "Linearized Einstein and signed matter perturbation, not full nonlinear positive matter",
            "One-dimensional prepared exact translation branch at h=dx=1",
            "No generic stability or arbitrary integer refinement conclusion",
            "No matter positivity, quantum, antimatter or dark-matter claim",
        ],
    }


def damping_counterexample():
    """A legitimate fixed-six lift of a damped ODE has a growing mode."""
    # Let d=2*h*kappa=1. R(x,y)=(y,x-d*y), R^-1(x,y)=(y+d*x,x).
    # Engine b advances R when initialized with a=R^-1(b). Its r is retained.
    zero = (0, 0, 0)
    tensor = Tensor(
        ["constraints.damping.previous", "constraints.damping.current"],
        [(0, 6, ((1, zero, "b"),)),
         (0, 3, ((0, zero, "b"),)),
         (1, 6, ((0, zero, "b"),)),
         (1, -3, ((1, zero, "b"),))],
        strict_support=True,
    )
    engine = Engine(tensor)
    initial = State(3, [[2]*27, [1]*27], [[1]*27, [1]*27], [[1]*27, [4]*27])
    state = initial.copy()
    pair = (1, 1)
    history = [list(pair)]
    for _ in range(16):
        pair = (pair[1], pair[0] - pair[1])
        state = engine.step(state)
        assert [int(state.b[i, 0]) for i in range(2)] == list(pair)
        assert state.r.tolist() == initial.r.tolist()
        history.append(list(pair))
    terminal = state.copy()
    for _ in range(16):
        state = engine.inverse_step(state)
    assert state.same_as(initial)

    c = sp.symbols("c", positive=True)  # c=h*kappa
    root_minus = -c - sp.sqrt(1 + c*c)
    root_plus = -c + sp.sqrt(1 + c*c)
    assert sp.simplify(root_minus*root_plus) == -1
    return {
        "kind": "negative_control",
        "continuum_equation": "z_dot=-kappa*z, kappa>0",
        "leapfrog_equation": "z[n+1]=z[n-1]-2*h*kappa*z[n]",
        "roots": [str(root_plus), str(root_minus)],
        "unstable_for_every_positive_h_kappa": True,
        "reason": "abs(root_minus)=c+sqrt(1+c*c)>1 for c>0",
        "engine_gears": tensor.G,
        "integer_history": history,
        "terminal_max_abs": terminal.max_abs(),
        "complete_state_rewind": True,
        "claim_limit": "Rejects naive damping under this leapfrog, not all reversible constraint control",
    }


def linearized_sourced_constraints():
    """Prove a polynomial operator identity for arbitrary commuting D_i.

    Spatial symbol variables are abstract commuting difference operators. This
    proves the identity for actual commuting centered face differences too.
    Units: Einstein coupling kappa=1, lapse=1, shift=0, background delta_ij.
    """
    d = sp.symbols("d0:3")
    rho = sp.Symbol("rho")
    j = sp.symbols("j0:3")

    def symmetric(prefix):
        values = {(i, k): sp.Symbol(f"{prefix}{i}{k}")
                  for i in range(3) for k in range(i, 3)}
        return sp.Matrix(3, 3, lambda i, k: values[min(i, k), max(i, k)])

    h, K, S = symmetric("h"), symmetric("K"), symmetric("S")
    lap = sum(x*x for x in d)

    def ricci(field):
        return sp.Matrix(3, 3, lambda i, k: sp.Rational(1, 2) * (
            sum(d[a]*d[i]*field[k, a] + d[a]*d[k]*field[i, a]
                for a in range(3))
            - lap*field[i, k] - d[i]*d[k]*sp.trace(field)))

    R = ricci(h)
    H = sp.trace(R) - 2*rho
    M = [sum(d[k]*K[i, k] for k in range(3)) - d[i]*sp.trace(K) - j[i]
         for i in range(3)]
    hdot = -2*K
    Kdot = R - S + sp.eye(3)*(sp.trace(S)-rho)/2
    rhodot = -sum(d[i]*j[i] for i in range(3))
    jdot = [-sum(d[k]*S[i, k] for k in range(3)) for i in range(3)]
    Hdot = sp.trace(ricci(hdot)) - 2*rhodot
    Mdot = [sum(d[k]*Kdot[i, k] for k in range(3))
            - d[i]*sp.trace(Kdot) - jdot[i] for i in range(3)]

    bianchi = [sp.expand(sum(d[k]*R[i, k] for k in range(3))
                         - d[i]*sp.trace(R)/2) for i in range(3)]
    H_defect = sp.expand(Hdot + 2*sum(d[i]*M[i] for i in range(3)))
    M_defect = [sp.expand(Mdot[i] + d[i]*H/2) for i in range(3)]
    assert bianchi == [0, 0, 0] and H_defect == 0 and M_defect == [0, 0, 0]

    # A source with externally frozen density violates the propagation identity.
    broken_Hdot = sp.trace(ricci(hdot))
    broken_H_defect = sp.expand(broken_Hdot + 2*sum(d[i]*M[i] for i in range(3)))
    assert sp.expand(broken_H_defect + 2*sum(d[i]*j[i] for i in range(3))) == 0
    assert broken_H_defect != 0
    return {
        "kind": "positive_algebraic_linearized_result_with_negative_control",
        "contracted_linear_bianchi_defect": list(map(str, bianchi)),
        "hamiltonian_propagation_defect": str(H_defect),
        "momentum_propagation_defect": list(map(str, M_defect)),
        "identities": ["H_dot=-2*D_i*M_i", "M_i_dot=-D_i*H/2"],
        "required_source_equations": ["rho_dot=-D_i*j_i", "j_i_dot=-D_j*S_ij"],
        "leapfrog_consequence": "H and M zero at both initial slices imply zero at every unrounded linear step",
        "broken_continuity_defect": str(broken_H_defect),
        "conditional_first_order_null_beam_field_budget": {
            "h_symmetric": 6, "K_symmetric": 6, "half_gradient_h": 18,
            "null_beam_density": 1, "period_four_sign_clock": 1, "total": 32,
        },
        "claim_limits": [
            "Linearized flat-background identity, not nonlinear Einstein preservation",
            "Requires commuting spatial differences and compatible gradient initial data",
            "Two-level data must both satisfy all linear constraints",
            "Channel count alone does not prove stable integer refinement",
            "Periodic linearized H=0 forces zero mean density perturbation",
        ],
    }


def spatial_product_defect():
    x, dx = sp.symbols("x dx", real=True)
    f = x*x

    def centered(expr):
        return sp.expand((expr.subs(x, x+dx)-expr.subs(x, x-dx))/(2*dx))

    defect = sp.factor(centered(f*f) - 2*f*centered(f))
    assert defect == 4*dx*dx*x
    fplus, fminus, gplus, gminus = sp.symbols("fp fm gp gm")
    flux = (fplus*gplus-fminus*gminus)/(2*dx)
    averaged_rule = ((fplus+fminus)*(gplus-gminus)
                     + (gplus+gminus)*(fplus-fminus))/(4*dx)
    assert sp.expand(flux-averaged_rule) == 0
    return {
        "ordinary_centered_leibniz_defect_f_equals_g_equals_x_squared": str(defect),
        "at_x_1_dx_1": str(defect.subs({x: 1, dx: 1})),
        "shifted_average_product_rule_exact": True,
        "finite_node_algebra_obstruction":
            "For each point idempotent e, D(e)=D(e^2)=2eD(e); componentwise D(e)=0, so every derivation is zero",
        "claim_limit": "Does not exclude flux identities, modified products, variational or modified constraints",
    }


def direct_quadratic_resolution_bound():
    # For K=s*k, dot K=K^2, leapfrog increment is m*k^2, m=2*h*s.
    # Nonzero integer m and k imply abs(h*K)=abs(m*k)/2>=1/2.
    m, k = sp.symbols("m k", integer=True, nonzero=True)
    bound_expression = sp.Abs(m*k)/2
    return {
        "kind": "limited_exact_obstruction",
        "assumptions": [
            "Direct fixed physical scaling K=s*k with k integer and s>0",
            "Same physical-time leapfrog applied to dot K=K^2",
            "Its nonzero quadratic increment coefficient m=2*h*s is an integer",
            "No extra divisibility arithmetic, retiming or nonlinear readout",
        ],
        "identity": "abs(h*K)=abs(m*k)/2",
        "symbolic_right_side": str(bound_expression),
        "nonzero_lower_bound": "1/2",
        "conclusion": "No h*abs(K)->0 family for nonzero K within these assumptions",
        "claim_limit": "Not a no-go theorem for all 48-channel encodings or all Rule3 models",
    }


def main():
    report = {
        "status": "research_audit_not_production_model",
        "source_sha256": {
            str(path): hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
            for path in [Path("universe24/core/engine.py"),
                         Path("universe24/layers/frame48.py")]
        },
        "damping": damping_counterexample(),
        "linearized_null_beam_engine": linearized_null_beam_engine(),
        "linearized_sourced_constraints": linearized_sourced_constraints(),
        "discrete_product": spatial_product_defect(),
        "direct_quadratic_resolution": direct_quadratic_resolution_bound(),
        "full_nonlinear_48_channel_einstein_constraint_gate": False,
    }
    target = ROOT / "runs/team48/constraints/results.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"report": str(target.relative_to(ROOT)),
                      "all_audit_assertions_pass": True,
                      "full_nonlinear_einstein_gate": False}, indent=2))


if __name__ == "__main__":
    main()
