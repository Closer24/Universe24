"""Preregistered two-harmonic held-out audit of the unchanged PR47 law.

Research only: passive floating diagnostics/reference never update the Engine.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json
import time

import numpy as np

from universe24.core import Engine
from universe24.core.lattice import lattice
from validation.geometry.team48.refinement_integer_projective import build_charged, prepare
from validation.geometry.team48.validation_repair_projective import binary_state_hash, planar_rhs
from validation.geometry.team48.validation_repair_seed import (
    PI, diagnostic_fields, literal_metric_constraints, nearest, sine_rational,
)

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = {
    "schema": "universe24/heldout-spatial/1",
    "source_pin": "621fc1f55800e50e1db5f6a30ce24bb83716a49a",
    "preregistration": "https://github.com/Closer24/Universe24/issues/40#issuecomment-6804502332",
    "profile": "sin(2*pi*x)/32 + cos(4*pi*x)/64",
    "pi_phi": "3/2", "K11_K22": "2+3*phi/4", "domain": [0, 1],
    "final_time": "1/32", "levels": [[8, 2], [12, 3], [16, 4]],
    "preparation_denominator": 2**24,
    "acceptance": "Every unscaled H/M/gradient/connection-metric residual and independent RK4 field error strictly decreases in both adjacent comparisons; exact rewind, unchanged carries and first-step Euler agreement pass.",
    "limits": "Short plane-symmetric neutral-scalar/dust test; not general GR, apparatus or asymptotic stability. No post-result tuning.",
}


def seed_values(names, n, resolution):
    """Exact sampled momentum/gradient constraints; H has disclosed sqrt error."""
    q = resolution
    values = np.zeros((len(names), n), dtype=object)
    f = dict(zip(names, values))
    for axis in range(3):
        f[f"B{axis}{axis}"][:] = q
    phi = np.asarray([
        4*nearest(F(q, 4)*(sine_rational(2*PI*F(j,n))/32
                           + sine_rational(4*PI*F(j,n)+PI/2)/64))
        for j in range(n)], dtype=object)
    psi = (n//2)*(np.roll(phi, -1)-np.roll(phi, 1))
    k = 2*q+3*phi//4
    density = k*k-9*q*q//8-psi*psi//2
    assert all(int(v) > 0 for v in density)
    dust = np.asarray([isqrt(int(v)) for v in density], dtype=object)
    f["phi"][:] = phi
    f["Pi_phi"][:] = 3*q//2
    f["Xi_phi0"][:] = psi
    f["K11"][:] = k
    f["K22"][:] = k
    f["dust_amplitude"][:] = dust
    momentum = -n*(np.roll(k,-1)-np.roll(k,1)) + 3*psi//2
    assert all(int(v) == 0 for v in momentum)
    defect = [F(2*(int(v)-int(d)**2),q*q) for v,d in zip(density,dust)]
    return values, {"initial_H_peak_exact": str(max(defect)),
                    "initial_M0_peak_exact": "0", "initial_gradient_peak_exact": "0",
                    "phi_quantization": "nearest multiple of four numerator; error <=2/resolution",
                    "minimum_dust_density": str(min(F(int(d)**2,q*q) for d in dust))}


def reference(n, steps):
    names = build_charged().fields
    x = np.arange(n)/n
    f = {name: np.zeros(n) for name in names}
    for axis in range(3):
        f[f"B{axis}{axis}"][:] = 1
    f["phi"] = np.sin(2*np.pi*x)/32+np.cos(4*np.pi*x)/64
    f["Pi_phi"][:] = 1.5
    f["Xi_phi0"] = 2*np.pi*np.cos(2*np.pi*x)/32-4*np.pi*np.sin(4*np.pi*x)/64
    f["K11"] = 2+0.75*f["phi"]
    f["K22"] = f["K11"].copy()
    f["dust_amplitude"] = np.sqrt(f["K11"]**2-1.125-f["Xi_phi0"]**2/2)
    h = float(F(PROTOCOL["final_time"]))/steps
    for _ in range(steps):
        k1 = planar_rhs(f,1/n)
        k2 = planar_rhs({name:v+h*k1[name]/2 for name,v in f.items()},1/n)
        k3 = planar_rhs({name:v+h*k2[name]/2 for name,v in f.items()},1/n)
        k4 = planar_rhs({name:v+h*k3[name] for name,v in f.items()},1/n)
        f = {name:v+h*(k1[name]+2*k2[name]+2*k3[name]+k4[name])/6 for name,v in f.items()}
    return f


def run_case(n, steps, fine):
    started = time.monotonic()
    final_time = F(PROTOCOL["final_time"])
    dt = final_time/steps
    resolution = PROTOCOL["preparation_denominator"]
    program = build_charged(dt=dt,dx=F(1,n))
    numerators, seed_report = seed_values(program.fields,n,resolution)
    lat = lattice(n)
    x = lat.all_coords()[:,0]
    current = np.asarray([[F(int(v),resolution) for v in row[x]] for row in numerators],dtype=object)
    carries = np.asarray([[int((i+j)%6) for j in range(lat.N)] for i in range(program.tensor.G)],dtype=object)
    state = seed = prepare(program,current,L=n,denominator=resolution,remainders=carries)
    engine = Engine(program.tensor)
    line = np.asarray([lat.index(j,0,0) for j in range(n)])
    initial = diagnostic_fields(program.fields,state.b[1:,line],state.b[0,line])
    rhs = planar_rhs(initial,1/n)
    first_expected = {name:v+float(dt)*rhs[name] for name,v in initial.items()}
    bits = []
    first_error = None
    for tick in range(steps):
        previous = state
        state = engine.step(state)
        assert engine.inverse_step(state).same_as(previous)
        assert np.array_equal(state.r,seed.r)
        assert np.all(state.b[0] == state.b[0,0]) and int(state.b[0,0]) > 0
        if tick == 0:
            first = diagnostic_fields(program.fields,state.b[1:,line],state.b[0,line])
            first_error = max(float(np.max(np.abs(first[name]-v))) for name,v in first_expected.items())
            assert first_error < 1e-12
        bits.append(max(abs(int(v)).bit_length() for v in state.b[:,line].flat))
    final = diagnostic_fields(program.fields,state.b[1:,line],state.b[0,line])
    final_hash = binary_state_hash(state)
    assert engine.rewind(state,steps).same_as(seed)
    stride = len(next(iter(fine.values())))//n
    field_error = max(float(np.max(np.abs(v-fine[name][::stride]))) for name,v in final.items())
    return {"n": n, "updates": steps, "dt": str(dt), "dx": str(F(1,n)),
            "final_time": str(final_time), "channels": program.tensor.G,
            "degree": program.degree, "monomials": len(program.tensor.monomials),
            "static_multiplier": program.multiplier, "seed": seed_report,
            "initial_literal_metric": literal_metric_constraints(initial,F(1,n)),
            "final_literal_metric": literal_metric_constraints(final,F(1,n)),
            "independent_first_step_Euler_error": first_error,
            "independent_RK4_field_error_linf": field_error,
            "max_bits_per_update": bits, "complete_exact_rewind": True,
            "every_step_inverse": True, "all_six_carries_unchanged": True,
            "strict_face_support": not bool(program.tensor.support_violations()),
            "tensor_sha256": hashlib.sha256(json.dumps(program.tensor.to_dict(),sort_keys=True).encode()).hexdigest(),
            "seed_binary_sha256": binary_state_hash(seed), "final_binary_sha256": final_hash,
            "seconds": time.monotonic()-started}


def run(out):
    destination = Path(out)
    report_path = destination if destination.suffix == ".json" else destination/"report.json"
    out = destination.with_suffix("") if destination.suffix == ".json" else destination
    out.mkdir(parents=True,exist_ok=True)
    encoded = json.dumps(PROTOCOL,sort_keys=True,indent=2)+"\n"
    (out/"protocol.json").write_text(encoded)
    fine = reference(384,1024)
    medium = reference(192,512)
    reference_difference = max(float(np.max(np.abs(fine[name][::2]-v))) for name,v in medium.items())
    rows = []
    for n,steps in PROTOCOL["levels"]:
        row = run_case(n,steps,fine)
        rows.append(row)
        print(json.dumps(row),flush=True)
        (out/"progress.json").write_text(json.dumps(rows,indent=2)+"\n")
    residuals = ("H_linf","M0_linf","gradient_linf","connection_metric_linf")
    gates = {name: all(rows[i+1]["final_literal_metric"][name] < rows[i]["final_literal_metric"][name]
                       for i in range(len(rows)-1)) for name in residuals}
    gates["RK4_field_error_linf"] = all(rows[i+1]["independent_RK4_field_error_linf"] < rows[i]["independent_RK4_field_error_linf"] for i in range(len(rows)-1))
    source_paths = [Path(__file__), ROOT/"validation/geometry/team48/refinement_integer_projective.py",
                    ROOT/"validation/geometry/team48/validation_repair_projective.py",
                    ROOT/"validation/geometry/team48/validation_repair_seed.py"]
    # Isolated algebraic control, not another Engine evolution or a fitted repair.
    # Euler's product update creates a scalar-gradient defect even when C=0.
    h, b, k, dphi, dpi = F(1,4), F(1), F(1), F(2), F(1)
    psi = b*dphi
    c_next = psi+h*(b*dpi+k*psi)-(b+h*k*b)*(dphi+h*dpi)
    assert c_next == -h*h*k*b*dpi == F(-1,16)
    result = {"status": "completed", "scope": "Held-out short-time sourced plane-symmetric refinement of unchanged 41-channel projective law",
              "command": f"python -m validation.synthesis.heldout_geometry --out {destination}",
              "source_pin": PROTOCOL["source_pin"],
              "physical_limits": ["Only neutral scalar and square dust in plane symmetry", "Short endpoint 1/32; no long-time stability proof", "Reference/diagnostics use floating arithmetic outside Engine", "No physical clock, detector, Born law or complexity selection"],
              "protocol": PROTOCOL, "protocol_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
              "source_sha256": {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
              "cases": rows, "strict_decrease_gates": gates,
              "preregistered_acceptance": "passed" if all(gates.values()) else "failed",
              "reference": {"method": "independent planar RHS, floating RK4; never Engine input",
                            "fine_grid": 384, "fine_updates": 1024, "medium_grid": 192,
                            "medium_updates": 512, "nested_field_difference_linf": reference_difference},
              "isolated_Euler_gradient_product_control": {
                  "identity": "C_next=(1+h*k)*C-h^2*k*b*D(pi), C=psi-b*D(phi)",
                  "exact_counterexample": str(c_next),
                  "scope": "Euler factor-product algebra only; not a complete attribution for projective retained-history update",
                  "candidate_not_implemented": "A cubic h^2*k*b*D(pi) correction cancels this reduced Euler defect; generic 3D support, projective history and physical convergence remain to be derived."},
              "general_Einstein_acceptance": "not_established"}
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(result,indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",default="runs/synthesis/heldout_geometry.json")
    args = parser.parse_args()
    result = run(args.out)
    print(json.dumps({"acceptance":result["preregistered_acceptance"], "gates":result["strict_decrease_gates"]}))
