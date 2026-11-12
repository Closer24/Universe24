"""Independent symbolic checks of the integration controls, not a new law."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp


def audit():
    coefficient, p, q, old_p, old_q = sp.symbols("coefficient p q old_p old_q")
    after_w = (coefficient*p-old_p)*q-(coefficient*q-old_q)*p
    assert sp.expand(after_w-(p*old_q-q*old_p)) == 0

    a = sp.symbols("a0:4")
    b = sp.symbols("b0:4")
    coupling = sp.symbols("coupling")
    difference = (b[0]-b[2], b[1]-b[3])
    force = (-coupling*difference[0], -coupling*difference[1],
             coupling*difference[0], coupling*difference[1])
    following = tuple(2*y-x+f for x, y, f in zip(a, b, force))

    def charge(x, y):
        return sum(x[i]*y[i+1]-x[i+1]*y[i] for i in (0, 2))

    assert sp.expand(charge(b, following)-charge(a, b)) == 0
    for component in (0, 1):
        assert sp.expand(sum(following[i]-b[i]-(b[i]-a[i])
                             for i in (component, component+2))) == 0

    def polarized(x, y):
        return sum((v-u)**2 for u, v in zip(x, y)) + sum(
            (x[i]-x[i+2])*(y[i]-y[i+2]) for i in (0, 1))

    linear = tuple(x.subs(coupling, 1) for x in following)
    assert sp.expand(polarized(b, linear)-polarized(a, b)) == 0
    # Independent global phase symmetry does not prove a local gauge symmetry.
    # A 90-degree rotation at one endpoint changes an untransported response.
    assert (1+1)**2 == 4 and 1**2+1**2 == 2

    fm, f0, fp, gm, g0, gp = sp.symbols("fm f0 fp gm g0 gp")
    defect = (fp*gp-fm*gm)/2-f0*(gp-gm)/2-g0*(fp-fm)/2
    correction = ((fp-f0)*(gp-g0)-(fm-f0)*(gm-g0))/2
    assert sp.expand(defect-correction) == 0

    scaled_ratios = []
    for scale in (1, 2):
        denominator, numerator = 3*scale, 2*scale
        old_denominator, old_numerator = scale, scale
        scaled_ratios.append(Fraction(2*denominator*numerator-old_numerator,
                                     2*denominator**2-old_denominator))
    assert scaled_ratios == [Fraction(11, 17), Fraction(23, 35)]

    threshold_cases = []
    for x in (0, 1):
        for y in (0, 1):
            assert x*(1-y) == int(x > y)
            assert x+y-x*y == max(x, y)
            threshold_cases.append([x, y, x*(1-y), x+y-x*y])
    old, now = 0, 0
    cycle = []
    for _ in range(4):
        old, now = now, 1-old
        cycle.append([old, now])
    assert cycle == [[0, 1], [1, 1], [1, 0], [0, 0]]

    root = Path(__file__).resolve().parents[2]
    reviewed_sources = [root / "validation" / "synthesis" / (name + ".py") for name in (
        "heldout_geometry", "bitgrowth_algebra", "gauge_clock_bridge", "complexity_selection",
        "compatible_geometry", "matter_backreaction")]
    return {
        "schema": "universe24/independent-integration-algebra/1",
        "status": "passed_scoped_symbolic_checks",
        "reviewed_base": "621fc1f55800e50e1db5f6a30ce24bb83716a49a",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reviewed_source_sha256": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                                   for path in reviewed_sources},
        "symbolic_zero_identities": ["protected pair Wronskian", "reciprocal pair U(1) charge",
                                     "reciprocal pair translation in both components",
                                     "linear polarized pair invariant", "centered product correction"],
        "raw_scale_next_ratios": list(map(str, scaled_ratios)),
        "boolean_truth_table": threshold_cases,
        "prepared_response_period_four": cycle,
        "limits": ["Independent symbolic/scalar checks, not additional Engine transition tests",
                   "No general Einstein, physical energy, local gauge, clock or complexity acceptance",
                   "Pair identities cannot substitute for a compiled reciprocal 44-channel coupling"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/synthesis/independent_review.json"))
    args = parser.parse_args()
    result = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "out": str(args.out)}))


if __name__ == "__main__":
    main()
