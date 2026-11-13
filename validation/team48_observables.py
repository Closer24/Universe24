"""Exact passive geometry/matter diagnostics of the pinned saved 44-channel run.

No proposal evolution code is imported. The one runtime verifies its bundle and
complete trace before this reader interprets the declared retained fields. These
are state diagnostics, not quantities measured from operational detector clicks.
Run: python -m validation.team48_observables --audit runs/team48-contract-final
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import gzip
import hashlib
from pathlib import Path
import subprocess

from universe24.system.bundle import pad_state
from validation.padding import sector_state, sector_tensor
from universe24.core import exact_json
from universe24.core.engine import State
from universe24.core.lattice import lattice
from universe24.system.bundle import load_bundle, read_json, state_from_data
from universe24.system.runtime import verify_run

SCHEMA = "universe24/validation/team48-observables/1"
SOURCE_COMMIT = "49b896c795203914a939e465d6d39e5b99343259"
TENSOR_HASH = "cd91d0c9bd9de41de1f60061e79b6e43932dcc032b7a7d86e0de4f3ef9534c2b"
SOURCE_HASHES = {
    "experiments/geometry/team48/matter_equations.py": "394efe21ec4637d541a79c283d040f6afad0f36ba0143d190358b984396ba18e",
    "experiments/geometry/team48/matter_charged.py": "8d57dc7b583ab9f0c657d5372ba3fa35f0b08cb8959eae2e6c03cca16d322fbc",
    "experiments/geometry/team48/matter_dust_square.py": "a32c65d536c14be036f8b9c02b87584decf333971fdb5e00eff4f7769c96ac3c",
    "experiments/geometry/team48/geometry_positive_pairs.py": "a76bb2496888a55cb80b8af2e6de08d1814598aa484feffd2359b1c9d9994077",
    "experiments/geometry/team48/geometry_triangular.py": "71daf226d9ff699144a3dfc1ceeba42483c4736425baed3568d9db17e98abc1f",
    "experiments/geometry/team48/integer_staggered.py": "fc3395bf3c731c1a8c3e51b72a86292c90200f2cbd23becd5256068accda16c0",
    "experiments/geometry/team48/candidate.py": "96ec6383dfea1dc899790256bad2f7115715472e1df85b036ad88acb7003a176",
}
FRAME_SOURCE = "universe24/algebra/frame_equations.py"
FRAME_HASH = "0414e93591cfaf7d1ab3c1c3ac45d958fa120a83c5a3bb337063622106162845"
AXES = range(3)


def _fraction(value):
    if type(value) is not int and not isinstance(value, F):
        raise TypeError("exact integer or Fraction required")
    return F(value)


def rational(value):
    """JSON rationals are exact signed numerator/positive denominator pairs."""
    if isinstance(value, F) or type(value) is int:
        value = F(value)
        return {"num": value.numerator, "den": value.denominator}
    if type(value) is dict:
        return {key: rational(item) for key, item in value.items()}
    if type(value) in (list, tuple):
        return [rational(item) for item in value]
    if value is None or type(value) in (str, bool):
        return value
    raise TypeError("observable arithmetic must remain exact")


def epsilon(a, b, c):
    return 0 if len({a, b, c}) != 3 else (b-a)*(c-a)*(c-b)//2


def inverse(matrix):
    """Exact small-matrix inverse; singular geometry is explicitly reported."""
    n = len(matrix)
    work = [[F(v) for v in row] + [F(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for i in range(n):
        pivot = next((j for j in range(i, n) if work[j][i]), None)
        if pivot is None:
            return None
        work[i], work[pivot] = work[pivot], work[i]
        divisor = work[i][i]
        work[i] = [value/divisor for value in work[i]]
        for j in range(n):
            if j != i:
                scale = work[j][i]
                work[j] = [a-scale*b for a, b in zip(work[j], work[i])]
    return [row[n:] for row in work]


def decode_fields(state: State, channel_names, manifest: dict) -> tuple[dict, list[int]]:
    """Decode the current slice using only uniform retained signs and static offsets."""
    state = State(state.L, state.a, state.b, state.r)
    names = list(channel_names)
    if (state.G != 44 or names != manifest.get("channels_by_index")
            or len(names) != state.G or names[0] != "phase.staggered"
            or manifest.get("phase_index") != 0 or manifest.get("model") != "charged_positive"):
        raise ValueError("unexpected 44-channel field manifest")
    fields = [name.removeprefix("field.") for name in names[1:]]
    if any(not name.startswith("field.") for name in names[1:]):
        raise ValueError("non-field channel in declared physical map")
    expected_offsets = {name: int(name.startswith(("G", "Xi_", "M"))
                                  or name in ("B01", "B02", "B12")) for name in fields}
    offsets = manifest.get("phase_offsets")
    if (not isinstance(offsets, dict) or offsets != expected_offsets
            or any(type(offset) is not int for offset in offsets.values())):
        raise ValueError("unsupported or altered field phase offsets")
    sa, sb = state.gear(0, 0)[:2]
    if sa not in (-1, 1) or sb not in (-1, 1):
        raise ValueError("retained phase is outside the proved sign sector")
    if any(state.gear(0, n)[:2] != (sa, sb) for n in range(state.N)):
        raise ValueError("retained computational phase is not uniform")
    decoded = {name: [(sa if offsets[name] == 0 else sb)*int(state.b[g, n])
                      for n in range(state.N)] for g, name in enumerate(fields, 1)}
    return decoded, [sa, sb]


def expand_fields(decoded: dict) -> dict:
    """Algebraically reconstruct B before taking any sampled spatial derivative."""
    result = {key: [_fraction(value) for value in values] for key, values in decoded.items()}
    n = len(result["phi"])
    if any(len(values) != n for values in result.values()):
        raise ValueError("field arrays have different node counts")
    for a in AXES:
        result[f"B{a}{a}"] = [p*p+q*q for p, q in zip(result[f"diag_p{a}"], result[f"diag_q{a}"])]
    for name in ("B10", "B20", "B21"):
        result[name] = [F(0)]*n
    result["G021"] = list(result["G012"])
    return result


def matter_observables(fields: dict, *, mass_squared=1, coupling=1) -> dict:
    """Local orthonormal-frame stress and charged-scalar current, all exact."""
    m2, g = _fraction(mass_squared), _fraction(coupling)
    fields = {key: _fraction(value) for key, value in fields.items()}
    components = [(fields[name], fields[f"Pi_{name}"],
                   [fields[f"Xi_{name}{a}"] for a in AXES]) for name in ("phi", "chi")]
    pi2 = sum(pi*pi for _, pi, _ in components)
    xi2 = sum(x*x for _, _, xi in components for x in xi)
    potential = m2*sum(phi*phi for phi, _, _ in components)/2
    scalar_rho = (pi2+xi2)/2+potential
    scalar_j = [-sum(pi*xi[a] for _, pi, xi in components) for a in AXES]
    scalar_s = [[sum(xi[a]*xi[b] for _, _, xi in components)
                 + int(a == b)*((pi2-xi2)/2-potential) for b in AXES] for a in AXES]
    electric, magnetic = ([fields[f"{name}{a}"] for a in AXES] for name in ("E", "M"))
    em_rho = sum(e*e+m*m for e, m in zip(electric, magnetic))/2
    em_j = [sum(epsilon(a, b, c)*electric[b]*magnetic[c] for b in AXES for c in AXES) for a in AXES]
    em_s = [[int(a == b)*em_rho-electric[a]*electric[b]-magnetic[a]*magnetic[b]
             for b in AXES] for a in AXES]
    dust = fields["dust_amplitude"]**2
    charge = -g*(fields["phi"]*fields["Pi_chi"]-fields["chi"]*fields["Pi_phi"])
    current = [g*(fields["phi"]*fields[f"Xi_chi{a}"]-fields["chi"]*fields[f"Xi_phi{a}"]) for a in AXES]
    return {"rho_scalar": scalar_rho, "rho_dust": dust, "rho_maxwell": em_rho,
            "rho_total": scalar_rho+dust+em_rho, "potential": potential,
            "momentum_frame": [scalar_j[a]+em_j[a] for a in AXES],
            "stress_frame": [[scalar_s[a][b]+em_s[a][b] for b in AXES] for a in AXES],
            "scalar_momentum_frame": scalar_j, "maxwell_momentum_frame": em_j,
            "scalar_stress_frame": scalar_s, "maxwell_stress_frame": em_s,
            "electric_charge": charge, "electric_current_frame": current,
            "charge_sector": "positive" if charge > 0 else "negative" if charge < 0 else "zero"}


def node_observables(expanded: dict, *, L: int, node: int, dx=1,
                     mass_squared=1, coupling=1, cosmological=0) -> dict:
    """One local exact diagnostic using centered face-neighbor samples only."""
    lat, dx = lattice(L), _fraction(dx)
    cosmological = _fraction(cosmological)
    if dx <= 0 or any(len(row) != lat.N for row in expanded.values()):
        raise ValueError("invalid spatial samples or spacing")
    f = {name: _fraction(values[node]) for name, values in expanded.items()}
    B = [[f[f"B{a}{i}"] for i in AXES] for a in AXES]
    K = [[f[f"K{min(a,b)}{max(a,b)}"] for b in AXES] for a in AXES]
    gamma_inv = [[sum(B[a][i]*B[a][j] for a in AXES) for j in AXES] for i in AXES]
    gamma = inverse(gamma_inv)
    det_B = B[0][0]*B[1][1]*B[2][2]
    geometry = {"B": B, "gamma_inv": gamma_inv, "gamma": gamma, "K_frame": K,
                "det_gamma": 1/(det_B*det_B) if det_B else None,
                "metric_status": "positive_definite" if det_B else "degenerate",
                "lapse": F(1), "shift": [F(0)]*3,
                "four_metric": ([[F(-1), F(0), F(0), F(0)]]
                                + [[F(0)]+row for row in gamma]) if gamma is not None else None}
    if gamma is not None:
        geometry["face_link_squared_lengths"] = [dx*dx*gamma[i][i] for i in AXES]
        geometry["face_angle_cosine_squared"] = {
            f"{i}{j}": gamma[i][j]**2/(gamma[i][i]*gamma[j][j])
            for i in AXES for j in range(i+1, 3)}
        geometry["face_angle_cosine_sign"] = {
            f"{i}{j}": (1 if gamma[i][j] > 0 else -1 if gamma[i][j] < 0 else 0)
            for i in AXES for j in range(i+1, 3)}
    matter = matter_observables(f, mass_squared=mass_squared, coupling=coupling)

    def partial(name, i):
        return (expanded[name][lat.neighbour(node, 2*i)]
                -expanded[name][lat.neighbour(node, 2*i+1)])/(2*dx)

    def direction(name, a):
        return sum(B[a][i]*partial(name, i) for i in AXES)

    def connection(a, b, c):
        return 0 if a == b else (1 if a < b else -1)*f[f"G{min(a,b)}{max(a,b)}{c}"]

    def dg(a, b, c, d):
        return 0 if a == b else (1 if a < b else -1)*direction(f"G{min(a,b)}{max(a,b)}{c}", d)

    def dk(a, b, d):
        return direction(f"K{min(a,b)}{max(a,b)}", d)-sum(
            connection(c, a, d)*K[c][b]+connection(c, b, d)*K[a][c] for c in AXES)

    def structure(a, b, c):
        return connection(a, c, b)-connection(a, b, c)

    def curvature(a, b, c, d):
        return dg(a, b, d, c)-dg(a, b, c, d)+sum(
            connection(a, e, c)*connection(e, b, d)-connection(a, e, d)*connection(e, b, c)
            -structure(e, c, d)*connection(a, b, e) for e in AXES)

    ricci = [[sum(curvature(c, a, c, b) for c in AXES) for b in AXES] for a in AXES]
    trace = sum(K[a][a] for a in AXES)
    constraints = {"H": sum(ricci[a][a] for a in AXES)+trace*trace
                   -sum(K[a][b]**2 for a in AXES for b in AXES)
                   -2*matter["rho_total"]-2*cosmological}
    constraints.update({f"M{a}": sum(dk(a, b, b)-dk(b, b, a) for b in AXES)
                        -matter["momentum_frame"][a] for a in AXES})
    constraints.update({f"C{a}{b}{i}": sum(B[a][j]*partial(f"B{b}{i}", j)
                        -B[b][j]*partial(f"B{a}{i}", j) for j in AXES)
                        -sum(structure(c, a, b)*B[c][i] for c in AXES)
                        for a in AXES for b in range(a+1, 3) for i in AXES})
    constraints.update({f"Ricci_antisym{a}{b}": ricci[a][b]-ricci[b][a]
                        for a in AXES for b in range(a+1, 3)})
    for prefix in ("E", "M"):
        constraints[f"Gauss_{prefix}"] = sum(direction(f"{prefix}{a}", a)
            -sum(connection(b, a, a)*f[f"{prefix}{b}"] for b in AXES) for a in AXES)
    constraints["Gauss_E"] -= matter["electric_charge"]
    for a in AXES:
        constraints[f"magnetic_potential{a}"] = f[f"M{a}"]-sum(
            epsilon(a, b, c)*(direction(f"A{c}", b)-sum(connection(d, c, b)*f[f"A{d}"] for d in AXES))
            for b in AXES for c in AXES)
        constraints[f"gradient_phi{a}"] = f[f"Xi_phi{a}"]-direction("phi", a)-F(coupling)*f[f"A{a}"]*f["chi"]
        constraints[f"gradient_chi{a}"] = f[f"Xi_chi{a}"]-direction("chi", a)+F(coupling)*f[f"A{a}"]*f["phi"]
    return {"node": node, "xyz": list(lat.coords(node)), "geometry": rational(geometry),
            "matter": rational(matter), "constraints": rational(constraints),
            "connection_ricci_frame": rational(ricci), "retained_decoded_fields": rational(f)}


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_provenance(integration: dict, reference: dict, bundle, report: dict,
                        source_dir=None) -> dict:
    """Check the exact pinned readout authority, not just self-consistent hashes."""
    if integration.get("source_commit") != SOURCE_COMMIT:
        raise ValueError("unsupported proposal source commit")
    if (integration.get("tensor_hash") != bundle.tensor.fingerprint or sector_tensor(bundle.tensor, 44).fingerprint != TENSOR_HASH
            or reference.get("manifest", {}).get("fingerprint") != TENSOR_HASH):
        raise ValueError("pinned tensor fingerprint mismatch")
    for key in ("run_id", "bundle_id", "steps"):
        if integration.get(key) != report.get(key):
            raise ValueError(f"integration {key} does not identify the verified run")
    if integration.get("bundle_id") != bundle.bundle_id:
        raise ValueError("bundle identity mismatch")
    if exact_json.dumps(integration.get("parameters"), sort_keys=True) != exact_json.dumps(
            {"dt": 1, "dx": 1, "mass_squared": 1, "coupling": 1, "cosmological": 0}, sort_keys=True):
        raise ValueError("unsupported pinned parameter set")
    hashes = integration.get("proposal_source_sha256")
    if type(hashes) is not dict or hashes != reference.get("source_sha256"):
        raise ValueError("proposal source hash metadata mismatch")
    for path, expected in SOURCE_HASHES.items():
        if hashes.get(path) != expected:
            raise ValueError(f"unsupported formula source hash: {path}")
    verification = {"pinned_commit_and_formula_hash_metadata": True, "checkout_files_checked": False}
    if source_dir is not None:
        source = Path(source_dir).resolve()
        commit = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"], check=True,
                                text=True, stdout=subprocess.PIPE).stdout.strip()
        if commit != SOURCE_COMMIT:
            raise ValueError("formula checkout is not the pinned commit")
        for path, expected in {**hashes, FRAME_SOURCE: FRAME_HASH}.items():
            file = (source/path).resolve()
            if not file.is_relative_to(source) or _sha(file) != expected:
                raise ValueError(f"formula checkout hash mismatch: {path}")
        verification["checkout_files_checked"] = True
    return verification


def generate_observables(audit_dir: str | Path, *, source_dir=None) -> dict:
    """Read an already saved run; never construct or advance a competing model."""
    audit = Path(audit_dir)
    report = verify_run(audit/"run")
    bundle = load_bundle(audit/"run/bundle")
    integration, reference = (read_json(audit/path) for path in
                              ("integration.json", "proposal-inputs/reference.json"))
    provenance = validate_provenance(integration, reference, bundle, report, source_dir)
    manifest = reference["manifest"]
    snapshots = []
    states = [(0, bundle.seed)]
    with gzip.open(audit/"run/full_trace.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            record = exact_json.loads(line)
            states.append((record["step"], state_from_data(record["after"])))
    if len(reference.get("states", [])) != len(states):
        raise ValueError("proposal reference snapshot count differs from verified trace")
    for step, state in states:
        if exact_json.dumps(state.to_dict(), sort_keys=True) != exact_json.dumps(pad_state(state_from_data(reference["states"][step])).to_dict(), sort_keys=True):
            raise ValueError("proposal reference state differs from verified retained trace")
        fields, phase = decode_fields(sector_state(state, 44), sector_tensor(bundle.tensor, 44).names, manifest)
        expanded = expand_fields(fields)
        nodes = [node_observables(expanded, L=state.L, node=node) for node in range(state.N)]
        snapshots.append({"step": step, "phase": phase, "nodes": nodes})
    return {"schema": SCHEMA, "run_id": report["run_id"], "bundle_id": bundle.bundle_id,
            "tensor_hash": bundle.tensor.fingerprint, "source_commit": SOURCE_COMMIT,
            "source_pr": integration["source_pr"], "source_sha256": {**SOURCE_HASHES, FRAME_SOURCE: FRAME_HASH},
            "observer_source_sha256": _sha(__file__), "source_verification": provenance,
            "input_hashes": {name: _sha(audit/name) for name in ("integration.json", "proposal-inputs/reference.json")},
            "trace_sha256": _sha(audit/"run/full_trace.jsonl.gz"),
            "channels_per_node": bundle.tensor.G, "L": bundle.seed.L, "steps": report["steps"],
            "parameters": integration["parameters"], "snapshots": snapshots,
            "units": "c=8*pi*G=1; signature -+++; synchronous lapse=1, shift=0; frame components are orthonormal",
            "rational_format": "Every diagnostic number is {num: integer, den: positive integer}; indices/phase remain integers.",
            "interpretation": "Passive retained-state diagnostics of the SAME verified 44-channel trace; not operational click measurements. Computational phase is not a proper-time clock.",
            "charge_interpretation": "Positive and negative electric U(1) density are classical conjugate charge sectors. These are not quantum antiparticles or annihilation events.",
            "curvature_interpretation": "Ricci and H use the retained independent frame connection. Torsion and Ricci antisymmetry defects are exposed; agreement with curvature independently reconstructed from the metric is not established.",
            "constraint_method": "Literal centered face differences of reconstructed composite B, no chain-rule substitution, projection or repair.",
            "physical_acceptance_gates": {key: {"status": "not_established", "reason": reason} for key, reason in {
                "C": "Sampled constraint defects are diagnostics; no full Einstein equivalence or constraint preservation is inferred.",
                "D": "No controlled spacetime or quantization refinement study is performed.",
                "E": "No independently ticking operational clock or detector is introduced.",
                "F": "This observer reads hidden retained fields, not physical detector clicks; no Born/Bell result is inferred."}.items()}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    result = generate_observables(args.audit, source_dir=args.source)
    out = args.out or args.audit/"observables.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(exact_json.dumps(result, sort_keys=True)+"\n", encoding="utf-8")
    print(exact_json.dumps({"output": str(out), "snapshots": len(result["snapshots"]),
                           "nodes_per_snapshot": result["L"]**3, "run_id": result["run_id"]}))


if __name__ == "__main__":
    main()
