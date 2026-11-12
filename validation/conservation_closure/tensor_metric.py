"""Independent curvature audit of the single retained Bianchi-I candidate.

The metric is a passive interpretation of the common native state. This module
never supplies values to Engine and does not infer Einstein evolution from a
vanishing scalar constraint alone.
"""
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import mpmath
import sympy as sp
from universe24.system.bundle import canonical_bytes

ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=1)
def metric_curvature():
    """Compute Gamma, Riemann, Ricci and G from a generic diagonal metric."""
    a = sp.symbols("a1:4", positive=True)
    h = sp.symbols("h1:4", real=True)
    dh = sp.symbols("dh1:4", real=True)
    g = sp.diag(-1, *(x*x for x in a))
    gi = g.inv()

    def derivative(expr, coordinate):
        if coordinate:
            return sp.S.Zero
        return sp.expand(sum(sp.diff(expr, a[i])*a[i]*h[i]
                             + sp.diff(expr, h[i])*dh[i] for i in range(3)))

    gamma = {}
    for upper in range(4):
        for lower1 in range(4):
            for lower2 in range(4):
                gamma[upper, lower1, lower2] = sp.simplify(sum(
                    gi[upper, k]*(derivative(g[k, lower2], lower1)
                    + derivative(g[k, lower1], lower2)
                    - derivative(g[lower1, lower2], k))/2 for k in range(4)))
    riemann = {}
    for upper in range(4):
        for lower in range(4):
            for mu in range(4):
                for nu in range(4):
                    riemann[upper, lower, mu, nu] = sp.simplify(
                        derivative(gamma[upper, nu, lower], mu)
                        - derivative(gamma[upper, mu, lower], nu)
                        + sum(gamma[upper, mu, k]*gamma[k, nu, lower]
                              - gamma[upper, nu, k]*gamma[k, mu, lower]
                              for k in range(4)))
    ricci = sp.Matrix(4, 4, lambda i, j: sp.simplify(sum(
        riemann[k, i, k, j] for k in range(4))))
    scalar = sp.simplify(sum(gi[i, j]*ricci[i, j]
                            for i in range(4) for j in range(4)))
    einstein = sp.simplify(ricci - g*scalar/2)
    electric = []
    for i in range(1, 4):
        r_i0i0 = sum(g[i, k]*riemann[k, 0, i, 0] for k in range(4))
        c_i0i0 = (r_i0i0 - (g[i, i]*ricci[0, 0]
                           + g[0, 0]*ricci[i, i])/2
                    + scalar*g[i, i]*g[0, 0]/6)
        electric.append(sp.simplify(c_i0i0/g[i, i]))
    require(sp.simplify(sum(electric)) == 0, "Weyl electric trace")
    return a, h, dh, g, gamma, riemann, ricci, scalar, einstein, electric


def symbolic_audit():
    a, h, dh, g, gamma, riemann, ricci, scalar, einstein, electric = metric_curvature()
    V, U, D, P = sp.symbols("V U D P", real=True, nonzero=True)
    s1, s2 = sp.symbols("S1 S2", real=True)
    shear = (s1, s2, -s1-s2)
    shear2 = sum(s*s for s in shear)
    constraint_residual = U*U-3*D*V-sp.Rational(3, 2)*(P*P+shear2)
    H = [(U/3+s)/V for s in shear]
    Hdot = [D/(2*V)-U*(U/3+s)/(V*V) for s in shear]
    substitutions = {**dict(zip(h, H)), **dict(zip(dh, Hdot))}
    rho, pressure = P*P/(2*V*V)+D/V, P*P/(2*V*V)
    stress = sp.diag(rho, *(a[i]**2*pressure for i in range(3)))
    residual = (einstein.subs(substitutions)-stress).applyfunc(sp.simplify)
    expected = sp.diag(constraint_residual/(3*V*V), *(a[i]**2*constraint_residual/(3*V*V) for i in range(3)))
    require((residual-expected).applyfunc(sp.simplify) == sp.zeros(4),
            "all sixteen metric-derived Einstein/source identities")
    require(sp.simplify(sp.diff(constraint_residual,V)*U+sp.diff(constraint_residual,U)*3*D/2) == 0,
            "constraint transported by continuum field")
    require(sp.simplify(sp.diff(rho,V)*U + U/V*(rho+pressure)) == 0,
            "total source continuity")
    require(sp.simplify(sp.diff(P/V,V)*U + U/V*(P/V)) == 0,
            "homogeneous massless scalar wave equation")
    require(sp.simplify(sp.diff(D/V,V)*U+U/V*(D/V)) == 0,
            "dust source continuity")
    # sigma^i_j is mixed; lower indices introduce a_i^2 and connection terms.
    lower_shear = [a[i]**2*shear[i]/V for i in range(3)]
    for i in range(3):
        lower_dt = sp.diff(lower_shear[i], V)*U + sp.diff(lower_shear[i], a[i])*a[i]*H[i]
        require(sp.simplify(lower_dt-(2*H[i]-U/V)*lower_shear[i]) == 0,
                "lower-index shear needs metric factor")
        require(sp.simplify(sp.diff(shear[i]/V,V)*U+U/V*shear[i]/V) == 0,
                "mixed-index shear charge conserved")
    # A retained-volume anchor determines I, never an external tick argument.
    K, U0 = sp.symbols("K U0", positive=True)
    root = sp.sqrt(K)
    I = sp.log((U-root)*(U0+root)/((U+root)*(U0-root)))/root
    Idot = sp.diff(I,U)*3*D/2
    require(sp.simplify(Idot.subs(K,U*U-3*D*V)-1/V) == 0,
            "retained-anchor logarithm differentiates to 1/V")
    # Exact, nonzero tidal witness in the default anisotropic sourced geometry.
    seed = {V:sp.Rational(7,3), U:4, D:1, P:2, s1:1, s2:-1}
    electric_physical = [sp.factor(x.subs(substitutions)) for x in electric]
    electric_seed = [sp.simplify(x.subs(seed)) for x in electric_physical]
    require(any(x != 0 for x in electric_seed), "anisotropy has a tidal witness")
    require(sp.simplify(sum(electric_seed)) == 0, "electric tidal trace-free")
    weyl_square_seed = sp.simplify(8*sum(x*x for x in electric_seed))
    require(weyl_square_seed > 0, "Bianchi-I magnetic Weyl is zero; C^2=8E^2")
    # Spatial curl is zero: direct all-spatial/one-time Riemann entries vanish.
    require(all(riemann[mu,0,j,k] == 0 for mu in range(1,4)
                for j in range(1,4) for k in range(1,4)), "magnetic Weyl zero")
    require(all(sp.simplify(x.subs({s1:0,s2:0})) == 0
                for x in electric_physical), "isotropic Weyl limit")
    erased = {**dict(zip(h,[U/(3*V)]*3)),
              **dict(zip(dh,[D/(2*V)-U*U/(3*V*V)]*3))}
    erased_error = sp.simplify((einstein[0,0].subs(erased)-rho).subs(seed))
    frozen_error = sp.simplify(-rho.subs(seed))
    require(erased_error != 0 and frozen_error != 0,
            "zero state Q does not validate an erased/frozen metric")
    # Coordinate covariance, distinct from conservation or a new spatial mode.
    L = sp.Matrix([[1,1,0],[0,1,1],[0,0,1]])
    metric3 = sp.diag(*(x*x for x in a))
    shear_mixed = sp.diag(*(s/V for s in shear))
    transformed_metric = L.inv().T*metric3*L.inv()
    transformed_shear = L*shear_mixed*L.inv()
    require(sp.simplify(sp.trace(transformed_shear**2)-sp.trace(shear_mixed**2)) == 0,
            "mixed tensor scalar contraction under basis change")
    p = sp.Matrix(sp.symbols("p1:4"))
    p_new = L.inv().T*p
    require(sp.simplify((p_new.T*transformed_metric.inv()*p_new)[0]
                       -(p.T*metric3.inv()*p)[0]) == 0,
            "covector/metric inverse contraction invariant")
    return {
        "all_16_einstein_component_residuals": "diag(1,a1^2,a2^2,a3^2)*Q/(3*V^2)",
        "curvature_derived_from_metric": True,
        "source_continuity_massless_wave_dust_balance": True,
        "mixed_shear_charges_and_lower_index_metric_factors": True,
        "retained_anchor_integral_derivative": "dI/dt=1/V",
        "electric_weyl_default": [str(x) for x in electric_seed],
        "weyl_square_default": str(weyl_square_seed),
        "isotropic_weyl_limit": True,
        "wrong_metric_controls": {"erased_shear_G00_minus_rho":str(erased_error),
                                  "frozen_metric_G00_minus_rho":str(frozen_error)},
        "tensor_and_covector_basis_covariance": True,
        "gamma_nonzero_count":sum(x != 0 for x in gamma.values()),
        "riemann_nonzero_count":sum(x != 0 for x in riemann.values()),
    }


def exact_curvature_state(row):
    """Independent rational curvature/source components of a decoded state."""
    V,U,D,P = (F(row[k]) for k in ("V","U","D","P"))
    S = tuple(F(x) for x in row["S"])
    require(sum(S) == 0 and V > 0, "trace-free shear and positive volume")
    H = tuple((U/3+s)/V for s in S)
    Hd = tuple(D/(2*V)-U*(U/3+s)/(V*V) for s in S)
    G00 = sum(H[i]*H[j] for i in range(3) for j in range(i+1,3))
    spatial = []
    for i in range(3):
        j,k = [x for x in range(3) if x != i]
        spatial.append(-(Hd[j]+Hd[k]+H[j]**2+H[k]**2+H[j]*H[k]))
    rho,pressure = P*P/(2*V*V)+D/V,P*P/(2*V*V)
    constraint_residual = U*U-3*D*V-F(3,2)*(P*P+sum(s*s for s in S))
    errors = (G00-rho,*(x-pressure for x in spatial))
    require(all(x == constraint_residual/(3*V*V) for x in errors), "all diagonal Einstein identities")
    return {"Q":constraint_residual,"H":H,"G00":G00,"rho":rho,"pressure":pressure,
            "normalized_diagonal_errors":errors,"off_diagonal_errors":(F(0),)*12}


def main():
    from . import common
    from universe24.core import Engine
    symbolic = symbolic_audit()
    samples = []
    for N in (24,48,96):
        program = common.build(N=N)
        seed = common.prepare(program)
        state = seed
        engine = Engine(program.tensor)
        count = N//8
        initial = common.read_conserved(program,seed)
        identities = []
        for tick in range(count+1):
            row = common.read_conserved(program,state)
            curvature = exact_curvature_state(row)
            require(curvature["Q"] == 0, "same-state sourced physical constraint")
            require(row["D"] == initial["D"] and row["P"] == initial["P"]
                    and tuple(row["S"]) == tuple(initial["S"]), "retained source/shear charges")
            readout = common.physical(program,state,dps=70)
            mp = mpmath.mp.clone(); mp.dps = 65
            aa = tuple(mp.mpf(x) for x in readout["a"])
            vv = mp.mpf(row["V"].numerator)/row["V"].denominator
            require(all(x > 0 for x in aa), "positive anisotropic spatial metric")
            require(abs(mp.fprod(aa)-vv) < mp.mpf("1e-58"), "same passive metric volume")
            require(all(abs(mp.mpf(readout["H"][i].numerator)/readout["H"][i].denominator-
                        mp.mpf(curvature["H"][i].numerator)/curvature["H"][i].denominator)
                        < mp.mpf("1e-58") for i in range(3)), "same directional expansion")
            identities.append({"tick":tick,"V":str(row["V"]),"U":str(row["U"]),
                               "Q":str(curvature["Q"]),"diagonal_residuals":[str(x) for x in curvature["normalized_diagonal_errors"]],
                               "a":[mp.nstr(x,60) for x in readout["a"]]})
            if tick < count:
                old = state; state = engine.step(old)
                require(engine.inverse_step(state).same_as(old),"complete inverse")
        require(engine.rewind(state,count).same_as(seed),"complete rewind")
        samples.append({"N":N,"steps":count,"tensor_sha256":program.tensor.fingerprint,
                        "seed_sha256":hashlib.sha256(canonical_bytes(seed.to_dict())).hexdigest(),
                        "samples":identities})
    # Alter the actual retained scalar charge without changing the geometry.
    # The decoder must keep this exact source/geometry discrepancy visible.
    program = common.build(N=24)
    wrong_seed = common.prepare(program,P=1)
    wrong = wrong_seed
    wrong_rows = []
    for tick in range(3):
        row = common.read_conserved(program,wrong)
        check = exact_curvature_state(row)
        require(check["Q"] == F(9,2), "wrong retained charge remains off constraint")
        require(all(x != 0 for x in check["normalized_diagonal_errors"]),
                "wrong actual source rejected by curvature")
        physical = common.physical(program,wrong,dps=50)
        require(physical["Q"] == F(9,2), "passive root/log readout cannot repair Q")
        wrong_rows.append({"tick":tick,"Q":str(check["Q"]),
                           "G00_minus_rho":str(check["normalized_diagonal_errors"][0])})
        if tick < 2:
            old = wrong; wrong = Engine(program.tensor).step(old)
            require(Engine(program.tensor).inverse_step(wrong).same_as(old),"negative still reverses")
    result = {"schema":"universe24-conservation-closure-tensor-metric-v1",
              "symbolic":symbolic,"shared_native_traces":samples,
              "wrong_actual_scalar_source":wrong_rows,
              "domain_theorem":{"hypotheses":"V0>0,D>0,U0>sqrt(K),K=3(P^2+sum S^2)/2>0",
                    "volume":"V(t)=V0+U0*t+3*D*t^2/4>0 for every t>=0",
                    "integral":"0<=I(t)<log((U0+sqrt(K))/(U0-sqrt(K)))/sqrt(K)",
                    "metric":"a_i=V^(1/3)*exp(S_i*I)>0 at every finite future t",
                    "scope":"positive total volume; individual axes need not all expand"},
              "source_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in (Path(__file__),Path(common.__file__))},
              "status":{"same_metric_all_Einstein_components":"passed",
                        "anisotropic_tidal_curvature":"passed",
                        "spatial_inhomogeneity":"not_tested",
                        "operational_detector":"not_tested"}}
    out = ROOT/"runs/conservation_closure/tensor_metric.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"symbolic":symbolic,"trace_count":len(samples),
                      "state_count":sum(len(x["samples"]) for x in samples),"output":str(out)},indent=2))


if __name__ == "__main__":
    main()
