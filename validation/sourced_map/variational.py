"""Independent massive-source alternatives and exact rejection evidence.

Run: python -m validation.sourced_map.variational
These are symbolic/reference maps, not Engine updates or accepted compilers.
No reference solver supplies the production state or the massless candidate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

from validation.completion.constraint_closure import symbolic_target

ROOT = Path(__file__).resolve().parents[2]
BASE = "f4f64e062f07b3ca119eccf655df746be206908b"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def volume_algebra():
    z, _, mu, _, force, *_ = symbolic_target()
    k, p, phi, dust = z
    B = s.symbols("B", positive=True)
    old = s.Matrix([B, k, p, phi, dust])
    rhs = s.Matrix([B*k, *force])
    V, U, P, D = B**-3, -3*k*B**-3, p*B**-3, dust**2*B**-3
    transformed = s.Matrix([V, U, P, phi, D])
    derived = transformed.jacobian(old)*rhs
    expected = s.Matrix([U, s.Rational(3, 2)*(D+mu*phi**2*V), -mu*phi*V, P/V, 0])
    require(all(s.simplify(v) == 0 for v in derived-expected), "physical volume change of variables")
    v, u, momentum, f, density = s.symbols("V U P phi D")
    invariant_form = u*u-s.Rational(3, 2)*momentum**2-s.Rational(3, 2)*mu*f*f*v*v-3*density*v
    vf = s.Matrix([u, s.Rational(3, 2)*(density+mu*f*f*v), -mu*f*v, momentum/v, 0])
    coordinates = s.Matrix([v, u, momentum, f, density])
    require(s.simplify((s.Matrix([invariant_form]).jacobian(coordinates)*vf)[0]) == 0, "proper-time Q first integral")
    original_C = 6*k*k-p*p-mu*phi*phi-2*dust*dust
    require(s.simplify(invariant_form.subs(dict(zip(coordinates, transformed)), simultaneous=True)
                       -s.Rational(3, 2)*V*V*original_C) == 0, "Einstein constraint correspondence")

    X, tau = s.symbols("X tau")
    lapse_coordinates = s.Matrix([v, u, momentum, X, density, tau])
    lapse_rhs = s.Matrix([v*u, s.Rational(3, 2)*(density*v+mu*X*X),
                         -mu*X*v, momentum*v+X*u, 0, v])
    quadratic_Q = u*u-s.Rational(3, 2)*momentum**2-s.Rational(3, 2)*mu*X*X-3*density*v
    require(s.expand((s.Matrix([quadratic_Q]).jacobian(lapse_coordinates)*lapse_rhs)[0]) == 0,
            "lapse-time quadratic invariant")
    require(max(s.Poly(e, *lapse_coordinates).total_degree() for e in lapse_rhs) == 2, "lapse degree")
    pi = s.symbols("pi")
    H = -3*v*pi*pi/4+momentum*momentum/(2*v)+mu*f*f*v/2+density
    canonical_q = s.Matrix([v, pi, f, momentum])
    canonical_rhs = s.Matrix([s.diff(H, pi), -s.diff(H, v),
                              s.diff(H, momentum), -s.diff(H, f)])
    canonical_U = -3*v*pi/2
    canonical_Udot = (s.Matrix([canonical_U]).jacobian(canonical_q)*canonical_rhs)[0]
    require(s.simplify(canonical_Udot.subs(pi, -2*u/(3*v))
                       -s.Rational(3, 2)*(density+mu*f*f*v)-invariant_form/(2*v)) == 0,
            "canonical off-constraint distinction")
    require(s.simplify(-3*v*H.subs(pi, -2*u/(3*v))-invariant_form) == 0,
            "canonical Hamiltonian/Einstein constraint relation")
    return {"proper_time_fields": [str(e) for e in coordinates], "proper_time_rhs": [str(e) for e in vf],
            "constraint_Q": str(invariant_form), "Q_relation": "Q=(3/2)*V^2*C", "Qdot": "0",
            "massive_comoving_momentum_derivative": "Pdot=-mu*phi*V",
            "massive_volume_acceleration": "Udot=(3/2)*(D+mu*phi^2*V)",
            "massless_affine_map_extension": "failed: P is not constant and Udot is not constant for mu>0",
            "canonical_equivalence_identity": "Udot_canonical-Udot_reduced=Q/(2V); -3V*H=Q",
            "lapse_time_rhs": [str(e) for e in lapse_rhs], "lapse_time_invariant": str(quadratic_Q),
            "lapse_time_relation": "d(tau)/d(s)=V; require V>0 and count tau as retained if used dynamically",
            "lapse_time_degree": 2, "native_massive_realization": "not_implemented"}


def kahan_step(variables, force, values, h):
    substitutions = dict(zip(variables, values))
    F = force.subs(substitutions, simultaneous=True)
    matrix = s.eye(len(variables))-h*force.jacobian(variables).subs(substitutions, simultaneous=True)/2
    require(matrix.det() != 0, "Kahan chart denominator zero")
    return (s.Matrix(values)+h*matrix.inv()*F).applyfunc(s.cancel)


def kahan_audit():
    variables, h, mu, _, force, *_ = symbolic_target()
    k, p, phi, dust = variables
    C = 6*k*k-p*p-mu*phi*phi-2*dust*dust
    cases = []
    for mass, initial in ((0, [-1, 2, 0, 1]), (1, [-1, 0, 2, 1])):
        fixed_force = force.subs(mu, mass)
        after = kahan_step(variables, fixed_force, initial, h)
        defect = s.factor(C.subs(mu, mass).subs(dict(zip(variables, after)), simultaneous=True))
        require(defect != 0, "known Kahan constraint failure missing")
        exact_after = after.subs(h, s.Rational(1, 16))
        recovered = kahan_step(variables, fixed_force, exact_after, -s.Rational(1, 16))
        require(recovered == s.Matrix(initial), "Kahan exact inverse")
        cases.append({"mu": mass, "seed": initial, "exact_constraint_defect": str(defect),
                      "at_h_1_16": str(defect.subs(h, s.Rational(1, 16))),
                      "inverse_at_h_1_16": True, "Einstein_zero_set": "failed"})

    v, u, pp, x, d = s.symbols("V U P X D")
    coordinates = s.Matrix([v, u, pp, x, d])
    lapse_rhs = s.Matrix([v*u, 3*(d*v+x*x)/2, -x*v, pp*v+x*u, 0])
    initial = s.Matrix([1, 3, 0, 2, 1])
    after = kahan_step(coordinates, lapse_rhs, initial, h)
    invariant_form = u*u-s.Rational(3, 2)*(pp*pp+x*x)-3*d*v
    defect = s.factor(invariant_form.subs(dict(zip(coordinates, after)), simultaneous=True))
    require(defect != 0, "lapse Kahan constraint failure missing")
    return {"proper_time_cases": cases, "lapse_time_massive": {"seed": list(map(int, initial)),
            "exact_Q_defect": str(defect), "Einstein_zero_set": "failed"},
            "scope": "birational reference maps; inverses exist only on nonsingular forward/backward charts; no Engine compiler"}


def midpoint_audit():
    v, u, pp, x, d = s.symbols("V U P X D")
    z = s.Matrix([v, u, pp, x, d])
    zp = s.Matrix(s.symbols("Vnext Unext Pnext Xnext Dnext"))
    invariant_form = lambda y: y[1]**2-s.Rational(3, 2)*(y[2]**2+y[3]**2)-3*y[4]*y[0]
    midpoint = (z+zp)/2
    grad = s.Matrix([s.diff(invariant_form(z), a) for a in z]).subs(dict(zip(z, midpoint)), simultaneous=True)
    require(s.expand(invariant_form(zp)-invariant_form(z)-(grad.T*(zp-z))[0]) == 0, "quadratic midpoint identity")
    vf = s.Matrix([v*u, 3*(d*v+x*x)/2, -x*v, pp*v+x*u, 0])
    require(s.expand((s.Matrix([invariant_form(z)]).jacobian(z)*vf)[0]) == 0, "midpoint conservation premise")

    # Strong massive constrained seed, lapse-time step 1/16. Eliminate midpoint
    # U,P,X using the V,P,X equations; the U equation gives this degree-8 factor.
    w = s.symbols("midpoint_volume")
    midU, midX = 32*(w-1)/w, 2048*w/(w**3+1024)
    midP = -midX*w/32
    residual = 2*(midU-3)-s.Rational(3, 32)*(w+midX**2)
    polynomial = s.Poly(s.expand((1856*w-2048-3*w*w)*(w**3+1024)**2-12582912*w**3), w)
    require(s.factor(residual-polynomial.as_expr()/(32*w*(w**3+1024)**2)) == 0, "midpoint elimination")
    require(polynomial.degree() == 8 and polynomial.is_irreducible, "degree-eight irreducibility")
    require(polynomial.count_roots(1, s.Rational(9, 8)) == 1, "unique positive local branch")
    with mp.workdps(65):
        fun = s.lambdify(w, polynomial.as_expr(), "mpmath")
        root = mp.findroot(fun, (mp.mpf(1), mp.mpf(9)/8))
        numerical_Q = s.lambdify(w, invariant_form(s.Matrix([2*w-1, 2*midU-3, 2*midP, 2*midX-2, 1])), "mpmath")(root)
        require(abs(numerical_Q) < mp.mpf("1e-55"), "midpoint independent numeric identity")
        root_text, defect_text = mp.nstr(root, 45), mp.nstr(numerical_Q, 8)
    return {"quadratic_invariant_midpoint_theorem": "passed", "self_adjoint_on_selected_unique_branch": True,
            "sample_mu": 1, "sample_seed_V_U_P_X_D": [1, 3, 0, 2, 1], "lapse_step": "1/16",
            "midpoint_volume_polynomial": str(polynomial.as_expr()), "degree": 8,
            "irreducible_over_Q": True, "unique_root_interval": ["1", "9/8"],
            "midpoint_volume_approx": root_text, "Q_numeric_crosscheck": defect_text,
            "exact_rational_readout_realization": "blocked for this midpoint map: every root is irrational",
            "scope": "not a no-go for alternative maps or algebraic encodings; nonlinear runtime solve is not permitted"}


def gravity_flow(z, h):
    V, pi, phi, P = z
    factor = 1-3*h*pi/4
    if factor == 0:
        raise ValueError("gravity subflow pole")
    return (V*factor*factor, pi/factor, phi, P)


def kinetic_flow(z, h):
    V, pi, phi, P = z
    if V == 0:
        raise ValueError("zero volume")
    return (V, pi+h*P*P/(2*V*V), phi+h*P/V, P)


def potential_flow(z, h):
    V, pi, phi, P = z
    return (V, pi-h*phi*phi/2, phi, P-h*phi*V)


def symmetric_split(z, h):
    for fn, dt in ((gravity_flow, h/2), (kinetic_flow, h/2), (potential_flow, h),
                   (kinetic_flow, h/2), (gravity_flow, h/2)):
        z = fn(z, dt)
    return z


def hamiltonian(z):
    V, pi, phi, P = z
    return -3*V*pi*pi/4+P*P/(2*V)+phi*phi*V/2+1


def reference(steps, endpoint):
    # Direct proper-time volume equations, independently of canonical splitting.
    z = [mp.mpf(1), mp.mpf(3), mp.mpf(0), mp.mpf(2)]  # V,U,P,phi; D=mu=1.
    def rhs(y):
        V, U, P, phi = y
        return [U, 3*(1+phi*phi*V)/2, -phi*V, P/V]
    dt = endpoint/steps
    for _ in range(steps):
        a = rhs(z)
        b = rhs([z[i]+dt*a[i]/2 for i in range(4)])
        c = rhs([z[i]+dt*b[i]/2 for i in range(4)])
        d = rhs([z[i]+dt*c[i] for i in range(4)])
        z = [z[i]+dt*(a[i]+2*b[i]+2*c[i]+d[i])/6 for i in range(4)]
    return z


def splitting_audit():
    z0 = tuple(map(s.Integer, (1, -2, 2, 0)))
    h = s.symbols("h")
    exact = symmetric_split(z0, s.Rational(1, 16))
    recovered = symmetric_split(exact, -s.Rational(1, 16))
    require(all(s.cancel(a-b) == 0 for a, b in zip(recovered, z0)), "split inverse")
    defect = s.factor(hamiltonian(symmetric_split(z0, h)))
    leading = s.limit(defect/h**3, h, 0)
    require(leading == -s.Rational(3, 4), "split leading Hamiltonian defect")
    require(hamiltonian(exact) != 0, "split constraint failure missing")
    with mp.workdps(60):
        T = mp.mpf(1)/8
        coarse, fine = reference(2048, T), reference(4096, T)
        reference_gap = max(abs(a-b) for a, b in zip(coarse, fine))
        require(reference_gap < mp.mpf("1e-16"), "reference refinement insufficient")
        rows = []
        prior = None
        for n in (2, 4, 8, 16):
            z = tuple(map(mp.mpf, (1, -2, 2, 0)))
            for _ in range(n):
                z = symmetric_split(z, T/n)
            V, pi, phi, P = z
            decoded = (V, -3*V*pi/2, P, phi)
            error = max(abs(a-b) for a, b in zip(decoded, fine))
            rows.append({"steps": n, "dt": mp.nstr(T/n, 20), "max_field_error": mp.nstr(error, 24),
                         "abs_H": mp.nstr(abs(hamiltonian(z)), 24),
                         "observed_order": None if prior is None else mp.nstr(mp.log(prior/error, 2), 15)})
            require(prior is None or error < prior, "split refinement not decreasing")
            prior = error
        reference_gap_text = mp.nstr(reference_gap, 20)
    return {"method": "G(h/2),K(h/2),W(h),K(h/2),G(h/2)",
            "hamiltonian": "H=-3*V*pi^2/4+P^2/(2V)+mu*phi^2*V/2+D",
            "canonical_momentum": "pi=2*k=-2*U/(3*V)", "physical_constraint": "Q=-3*V*H",
            "physical_equivalence_domain": "H=0; off it canonical Udot differs from reduced Einstein Udot by Q/(2V)",
            "exact_subflows_and_inverse": True, "domain": "V>0; each gravity factor 1-3*dt*pi/4 nonzero",
            "seed": [1, -2, 2, 0], "mu": 1, "D": 1,
            "exact_H_defect_h_1_16": str(s.factor(hamiltonian(exact))),
            "leading_H_defect": "-3*h^3/4 + O(h^4)", "Einstein_zero_set": "failed",
            "proper_endpoint": "1/8", "reference_RK4_steps": [2048, 4096],
            "reference_endpoint_difference": reference_gap_text, "refinement": rows,
            "scope": "numerical proper-time convergence evidence only; no Engine execution/constraint-preserving native map"}


def audit():
    return {"schema": "universe24/sourced-map/variational-alternatives/1", "base_commit": BASE,
            "volume_and_lapse_algebra": volume_algebra(), "Kahan": kahan_audit(),
            "implicit_midpoint": midpoint_audit(), "symmetric_split": splitting_audit(),
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "accepted_massive_native_candidate": False,
            "conclusion": "massless construction does not transfer unchanged to massive matter; tested explicit alternatives fail exact Einstein constraint"}


def main():
    report = audit()
    path = ROOT/"runs/sourced-map/variational.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"output": str(path), "massive_native": "not_implemented",
                      "midpoint_irreducible_degree": report["implicit_midpoint"]["degree"],
                      "split_refinement": report["symmetric_split"]["refinement"]}, indent=2))


if __name__ == "__main__":
    main()
