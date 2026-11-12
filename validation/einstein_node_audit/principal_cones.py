"""Independent scalar/Maxwell principal-cone check of pinned PR50 equations.

Run from main with an external clean checkout, without importing that proposal
into the supported runtime::

    python -m validation.einstein_node_audit.principal_cones \
      --source ../geometry-pr50 --out runs/einstein-node/04_geometry.json

The new symbolic checks concern frozen continuum derivative blocks only.
They do not prove finite-step packet geodesics or the full coupled symbol.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

SOURCE_COMMIT = "62202fdccdd9a40d5dbbec104de6f97d9587a999"


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          text=True, capture_output=True).stdout.strip()


def _worker(source: Path) -> dict:
    # This function runs under python -I with no parent research modules loaded.
    sys.path.insert(0, str(source))
    import importlib
    import sympy as sp
    from validation.geometry.team48 import matter_charged

    assert Path(matter_charged.__file__).resolve().is_relative_to(source)
    B = sp.Matrix(3, 3, sp.symbols("b:9", real=True))
    n = sp.Matrix(sp.symbols("n:3", real=True))
    fields = {name: sp.Integer(0) for name in matter_charged.FIELDS}
    for a in range(3):
        for i in range(3):
            fields[f"B{a}{i}"] = B[a, i]
    scalar = ("phi", "Pi_phi", "Xi_phi0", "Xi_phi1", "Xi_phi2")
    maxwell = ("E0", "E1", "E2", "M0", "M1", "M2")
    names = scalar + maxwell
    jets = dict(zip(names, sp.symbols(f"j:{len(names)}")))
    rhs, _, _ = matter_charged.equations(
        fields, lambda name, axis: n[axis]*jets.get(name, 0),
        mass_squared=7, coupling=5)
    scalar_matrix = sp.Matrix([rhs[name] for name in scalar]).jacobian(
        [jets[name] for name in scalar])
    maxwell_matrix = sp.Matrix([rhs[name] for name in maxwell]).jacobian(
        [jets[name] for name in maxwell])
    wave_covector = B*n
    speed2 = (wave_covector.T*wave_covector)[0]
    for matrix, trace_factor in ((scalar_matrix, 2), (maxwell_matrix, 4)):
        assert (matrix**3-speed2*matrix).applyfunc(sp.expand) == sp.zeros(matrix.rows)
        assert sp.expand(sp.trace(matrix**2)-trace_factor*speed2) == 0

    # A nonorthogonal frame and an oblique direction defeat an accidental
    # identity-metric or axis-only implementation. These are exact controls.
    concrete_B = sp.Matrix([[2, 1, 0], [0, 3, 1], [1, 0, 2]])
    direction = sp.Matrix([1, 2, 3])
    substitutions = dict(zip(list(B), list(concrete_B)))
    substitutions.update(dict(zip(list(n), list(direction))))
    value = speed2.subs(substitutions)
    lam = sp.Symbol("lambda")
    assert concrete_B.det() == 13 and value == 146
    assert sp.expand(scalar_matrix.subs(substitutions).charpoly(lam).as_expr()
                     -lam**3*(lam**2-value)) == 0
    assert sp.expand(maxwell_matrix.subs(substitutions).charpoly(lam).as_expr()
                     -lam**2*(lam**2-value)**2) == 0
    wrong_speed = (direction.T*direction)[0]
    assert wrong_speed == 14 and wrong_speed != value

    # These are reruns of the proposal's published tests, explicitly separated
    # from the independent matter-cone checks above.
    published = importlib.import_module("validation.research_eight.07_hyperbolic_symbol")
    assert Path(published.__file__).resolve().is_relative_to(source)
    return {
        "independent_matter_principal_blocks": {
            "status": "passed",
            "symbolic_domain": "Arbitrary real full frame B and covector n; physical metric requires det(B) != 0.",
            "metric_inverse": "diag(-1, B^T B)",
            "scalar_and_Maxwell_annihilator": "A^3 - (n^T B^T B n) A = 0",
            "scalar_trace_A_squared": "2 n^T B^T B n",
            "Maxwell_trace_A_squared": "4 n^T B^T B n",
            "mass_squared": 7, "charge_coupling": 5,
            "nonorthogonal_frame": [list(map(int, concrete_B.row(i))) for i in range(3)],
            "direction": list(map(int, direction)), "frame_determinant": 13,
            "metric_speed_squared": 146,
            "scalar_characteristic_polynomial": "lambda^3 (lambda^2 - 146)",
            "Maxwell_characteristic_polynomial": "lambda^2 (lambda^2 - 146)^2",
            "wrong_identity_frame_control": {"speed_squared": 14, "matches_metric": False},
            "interpretation": "The existing continuum matter equations encode a common metric in their principal spatial derivatives. This is not derived from Rule3 alone.",
        },
        "published_PR50_symbol_audit_reexecuted": published.symbol_audit(),
        "published_PR50_45channel_audit_reexecuted": published.compile_audit(),
        "not_established": [
            "Full coupled matter/gravity symbol on nontrivial backgrounds",
            "Nonlinear discrete constraint propagation",
            "Finite-step scalar or Maxwell packet geodesics on the board",
            "Independent material proper-clock ticks and operational decoder",
            "Uniform fully discrete stability, general convergence or efficient bit growth",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=Path("runs/einstein-node/04_geometry.json"))
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    source = args.source.resolve()
    if _git(source, "rev-parse", "HEAD") != SOURCE_COMMIT:
        raise ValueError("Expected the exact published PR50 source pin")
    if _git(source, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Source checkout has modified tracked files")
    if args.worker:
        print(json.dumps(_worker(source), sort_keys=True))
        return
    result = subprocess.run(
        [sys.executable, "-I", str(Path(__file__).resolve()), "--worker", "--source", str(source)],
        check=True, capture_output=True, text=True)
    report = json.loads(result.stdout)
    paths = ("universe24/algebra/frame_equations.py",
             "universe24/core/engine.py", "universe24/core/tensor.py",
             "validation/geometry/team48/matter_charged.py",
             "validation/geometry/team48/matter_equations.py",
             "validation/geometry/team48/matter_dust_square.py",
             "validation/geometry/team48/geometry_triangular.py",
             "validation/geometry/team48/refinement_integer_projective.py",
             "validation/research_eight/07_hyperbolic_symbol.py")
    report.update(schema="universe24/einstein-node/geometry/1", source_commit=SOURCE_COMMIT,
                  source_pr="https://github.com/Closer24/Universe24/pull/50",
                  source_sha256={path: hashlib.sha256((source/path).read_bytes()).hexdigest() for path in paths},
                  audit_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"output": str(args.out), "principal_cones": "passed",
                      "published_symbol_and_45channel_audits": "passed",
                      "physical_acceptance": "not_established"}))


if __name__ == "__main__":
    main()
