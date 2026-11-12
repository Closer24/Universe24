"""Exact compatible-derivative controls, not an Einstein evolution law.

Run with ``python -m validation.synthesis.compatible_geometry``.
"""
from __future__ import annotations

import hashlib
import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

from universe24.core import Engine, State, Tensor
from universe24.core.tensor import GearType, LocalityError
from validation.system_smoke import scalar_step


def nodes(L):
    return list(itertools.product(range(L), repeat=3))


def shift(p, axis, amount, L):
    q = list(p)
    q[axis] = (q[axis] + amount) % L
    return tuple(q)


def difference(f, axis, L, centered=False):
    return {p: (f[shift(p, axis, 1, L)] -
                f[shift(p, axis, -1 if centered else 0, L)]) /
               Fraction(2 if centered else 1) for p in nodes(L)}


def curl(v, L):
    return [{p: difference(v[(i+2) % 3], (i+1) % 3, L)[p] -
             difference(v[(i+1) % 3], (i+2) % 3, L)[p]
             for p in nodes(L)} for i in range(3)]


def divergence(v, L):
    ds = [difference(v[i], i, L) for i in range(3)]
    return {p: sum(d[p] for d in ds) for p in nodes(L)}


def incidence_controls():
    """Exact rational periodic-lattice d*d identities and matched defects."""
    L = 5
    ps = nodes(L)
    f = {p: Fraction(2*p[0]**2 - 3*p[1]*p[2] + 7, 3) for p in ps}
    g = {p: Fraction(p[0]**3 + p[1]**2 - 2*p[2] + 1, 5) for p in ps}
    v = [f, g, {p: f[p]*g[p] for p in ps}]
    commutators = []
    for centered in (False, True):
        for i, j in itertools.product(range(3), repeat=2):
            ij = difference(difference(f, i, L, centered), j, L, centered)
            ji = difference(difference(f, j, L, centered), i, L, centered)
            commutators.extend(ij[p]-ji[p] for p in ps)
    assert all(x == 0 for x in commutators)
    assert all(x == 0 for x in divergence(curl(v, L), L).values())

    defects, repaired, shifted = [], [], []
    for i in range(3):
        df, dg = difference(f, i, L, True), difference(g, i, L, True)
        dfg = difference({p: f[p]*g[p] for p in ps}, i, L, True)
        for p in ps:
            plus, minus = shift(p, i, 1, L), shift(p, i, -1, L)
            defect = dfg[p] - f[p]*dg[p] - g[p]*df[p]
            correction = ((f[plus]-f[p])*(g[plus]-g[p]) -
                          (f[minus]-f[p])*(g[minus]-g[p])) / 2
            defects.append(defect)
            repaired.append(defect-correction)
            # Forward difference obeys a shifted Leibniz identity exactly.
            shifted.append((f[plus]*g[plus]-f[p]*g[p]) -
                           (f[plus]*(g[plus]-g[p]) + g[p]*(f[plus]-f[p])))
    assert max(map(abs, defects)) > 0
    assert all(x == 0 for x in repaired + shifted)
    # Break one orientation of curl: a matched negative control.
    broken = curl(v, L)
    dx_vz = difference(v[2], 0, L)
    broken[1] = {p: broken[1][p] + 2*dx_vz[p] for p in ps}
    bad = max(map(abs, divergence(broken, L).values()))
    assert bad > 0
    return {"commutator_checks": len(commutators), "commutator_max": "0",
            "div_curl_max": "0", "wrong_orientation_div_curl_max": str(bad),
            "pointwise_product_defect_max": str(max(map(abs, defects))),
            "corrected_product_defect_max": "0", "shifted_product_defect_max": "0"}


def tensor_control(broken=False):
    """Six node fields; no geometrically extended link metadata is claimed."""
    names = [f"A{i}" for i in range(3)] + [f"B{i}" for i in range(3)]
    terms = [(n, 6, [(n, (0, 0, 0), "b")]) for n in names]
    for i in range(3):
        for axis, component, sign in (((i+1) % 3, (i+2) % 3, 1),
                                     ((i+2) % 3, (i+1) % 3, -1)):
            if broken and i == 1 and axis == 0:
                sign *= -1
            off = tuple(int(k == axis) for k in range(3))
            terms.extend([(f"B{i}", 3*sign, [(f"A{component}", off, "b")]),
                          (f"B{i}", -3*sign, [(f"A{component}", (0,0,0), "b")])])
    return Tensor([GearType(n, label="audit") for n in names], terms, strict_support=True)


def engine_controls():
    L, steps = 4, 8
    ps = nodes(L)
    source = [{p: (i+1)*p[0]**2 - (i+2)*p[1]*p[2] + p[i]**3 + (i+1)*p[0]*p[1] - 7
               for p in ps} for i in range(3)]
    zero = [[0]*len(ps) for _ in range(3)]
    initial = [[source[i][p] for p in ps] for i in range(3)] + zero
    carries = [[(n+i) % 6 for n in range(len(ps))] for i in range(6)]
    seed = State(L, initial, initial, carries)
    tensor = tensor_control()
    engine = Engine(tensor)
    current = expected = seed
    max_bits = 0
    for _ in range(steps):
        current, expected = engine.step(current), scalar_step(tensor, expected)
        assert current.same_as(expected)
        b = [{p: int(current.b[3+i, n]) for n, p in enumerate(ps)} for i in range(3)]
        assert all(x == 0 for x in divergence(b, L).values())
        assert (current.r == seed.r).all()
        max_bits = max(max_bits, max(abs(int(x)).bit_length() for x in current.b.flat))
    assert engine.rewind(current, steps).same_as(seed)
    bad = Engine(tensor_control(True)).step(seed)
    b = [{p: int(bad.b[3+i,n]) for n,p in enumerate(ps)} for i in range(3)]
    bad_max = max(map(abs, divergence(b, L).values()))
    assert bad_max > 0
    return {"channels": tensor.G, "retained_integers_per_node": 3*tensor.G,
            "degree": max(m.degree for m in tensor.monomials), "monomials":len(tensor.monomials),
            "steps":steps, "nodes":len(ps), "all_six_carries": True,
            "scalar_oracle": "passed", "rewind": "passed", "divergence_max": "0",
            "wrong_orientation_divergence_max": str(bad_max), "maximum_b_bits":max_bits,
            "role":"source-only linear identity fixture; not appended to projective44"}


def locality_controls():
    # Expanded one-face quadratic correction is admissible. No unexpanded
    # product of derivatives on different faces may be substituted for it.
    terms = []
    for sign in (-1, 1):
        off = (sign, 0, 0)
        for coeff, fo, go in ((sign,off,off),(-sign,off,(0,0,0)),
                             (-sign,(0,0,0),off),(sign,(0,0,0),(0,0,0))):
            terms.append(("receiver", coeff, [("f",fo,"b"),("g",go,"b")]))
    t = Tensor(["f","g","receiver"], terms, strict_support=True)
    rejected = []
    candidates = {
        "cross_face_gradient_product":[("f",(1,0,0),"b"),("g",(0,1,0),"b")],
        "plaquette_diagonal_read":[("f",(1,1,0),"b")],
    }
    for name, factors in candidates.items():
        try:
            Tensor(["f","g","receiver"], [("receiver",1,factors)], strict_support=True)
        except LocalityError:
            rejected.append(name)
        else:
            raise AssertionError(f"unsupported locality accepted: {name}")
    return {"expanded_face_correction_degree":max(m.degree for m in t.monomials),
            "expanded_face_correction_terms":len(t.monomials), "rejected":rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/synthesis/compatible_geometry.json"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    dependencies = ["universe24/core/engine.py", "universe24/core/tensor.py",
                    "validation/system_smoke.py"]
    report = {"schema":"universe24/compatible-identity-audit/1",
              "status":"passed", "scope":"linear incidence and scalar product identities only",
              "command":f"python -m validation.synthesis.compatible_geometry --out {args.out}",
              "base_commit":"621fc1f55800e50e1db5f6a30ce24bb83716a49a",
              "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "dependency_sha256":{p:hashlib.sha256((root/p).read_bytes()).hexdigest()
                                   for p in dependencies},
              "incidence":incidence_controls(), "engine":engine_controls(),
              "locality":locality_controls(), "general_einstein_acceptance":"not_established",
              "limits":["Six-channel fixture is not coupled to projective44",
                        "Node fields are not a physical edge/plaquette field allocation",
                        "No nonlinear Einstein, metric, matter, apparatus or convergence proof",
                        "Product correction is an algebraic identity, not a consistent full-equation repair"],
              "sources":["https://arxiv.org/abs/math/0508341",
                         "https://arxiv.org/abs/2406.05383"]}
    out = args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
