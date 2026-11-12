"""Shift-aware cubic flux algebra and actual fixed-six mechanical control.

This is independent research evidence, not an Einstein update or a production
model. Every Engine state uses one retained channel and the exact core law.
"""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random

import numpy as np

from universe24.core.engine import Engine, State
from universe24.core.lattice import lattice
from universe24.core.tensor import Factor, GearType, LocalityError, Monomial, Tensor

ROOT = Path(__file__).resolve().parents[2]
ZERO = (0, 0, 0)
PLUS = (1, 0, 0)
MINUS = (-1, 0, 0)


def shift_identities():
    rng = random.Random(20261111)
    for _ in range(10000):
        f, fp, g, gp, h, hp = [rng.randrange(-50, 51) for _ in range(6)]
        assert fp * gp - f * g == fp * (gp - g) + g * (fp - f)
        assert fp * gp * hp - f * g * h == (
            fp * gp * (hp - h) + fp * h * (gp - g) + g * h * (fp - f)
        )
    k = list(map(F, [10, 14, 18, 14, 10]))
    q = list(map(F, [2, 4, 0, -4, -2]))

    def centered(row):
        return [(row[(i + 1) % 5] - row[(i - 1) % 5]) / 2 for i in range(5)]

    def avg(row):
        return [(row[(i + 1) % 5] + row[(i - 1) % 5]) / 2 for i in range(5)]

    def defect(row, shifted):
        square_derivative = centered([x * x for x in row])
        multiplier = avg(row) if shifted else row
        return [ds - 2 * m * d for ds, m, d in zip(square_derivative, multiplier, centered(row))]

    old = [-3 * a - b / 2 for a, b in zip(defect(k, False), defect(q, False))]
    shifted = [-3 * a - b / 2 for a, b in zip(defect(k, True), defect(q, True))]
    assert max(map(abs, old)) == 21
    assert all(x == 0 for x in shifted)
    return {
        "exact_random_pair_and_triple_identity_checks": 10000,
        "old_fixture_product_defect_peak": str(max(map(abs, old))),
        "shifted_identity_defect_peak": str(max(map(abs, shifted))),
        "scope": "Algebraic cancellation only; no corrected Einstein RHS or constraints are asserted.",
    }


def make_tensor(conservative):
    b = Factor(0, ZERO, "b")
    bp = Factor(0, PLUS, "b")
    bm = Factor(0, MINUS, "b")
    terms = [Monomial(0, 6, (b,))]
    if conservative:
        # ell = 2b + b_plus^3 - b_minus^3, so r stays fixed.
        terms += [Monomial(0, 3, (bp, bp, bp)), Monomial(0, -3, (bm, bm, bm))]
    else:
        # Matched naive chain rule: D(b^3) -> 3 b^2 D(b).
        terms += [Monomial(0, 9, (b, b, bp)), Monomial(0, -9, (b, b, bm))]
    return Tensor([GearType("audit.cubic_flux", label="audit")], terms, strict_support=True)


def oracle(state, conservative):
    n = state.N
    lat = lattice(state.L)
    plus, minus = lat.shift_index(PLUS), lat.shift_index(MINUS)
    aa = [int(x) for x in state.a[0]]
    bb = [int(x) for x in state.b[0]]
    rr = [int(x) for x in state.r[0]]
    bnew, rnew = [], []
    for i in range(n):
        divflux = bb[plus[i]] ** 3 - bb[minus[i]] ** 3 if conservative else (
            3 * bb[i] ** 2 * (bb[plus[i]] - bb[minus[i]])
        )
        u = 6 * bb[i] + 3 * divflux
        ell, rn = divmod(2 * u + rr[i], 6)
        bnew.append(ell - aa[i])
        rnew.append(rn)
    return State(state.L, [bb], [bnew], [rnew])


def run_control(conservative):
    tensor = make_tensor(conservative)
    engine = Engine(tensor)
    L = 5
    lat = lattice(L)
    profile = [0, 1, 3, -1, 2]
    seedrow = [profile[int(x)] for x in lat.all_coords()[:, 0]]
    results = []
    for remainder in (*range(6), "mixed"):
        remainder_row = [i % 6 for i in range(lat.N)] if remainder == "mixed" else [remainder] * lat.N
        seed = State(L, [seedrow], [seedrow], [remainder_row])
        state = seed.copy()
        sums, bits = [sum(map(int, state.b[0]))], [state.max_abs().bit_length()]
        for _ in range(4):
            expected = oracle(state, conservative)
            after = engine.step(state)
            assert after.same_as(expected)
            assert engine.inverse_step(after).same_as(state)
            assert np.array_equal(after.r, seed.r)
            state = after
            sums.append(sum(map(int, state.b[0])))
            bits.append(state.max_abs().bit_length())
        for _ in range(4):
            state = engine.inverse_step(state)
        assert state.same_as(seed)
        if conservative:
            assert all(x == sums[0] for x in sums)
        else:
            assert sums[1] != sums[0]
        results.append({"remainder": remainder, "sums": sums, "integer_bits": bits})
    return {"channels": tensor.G, "integers_per_node": 3 * tensor.G,
            "degree": max(m.degree for m in tensor.monomials),
            "strict_support_violations": len(tensor.support_violations()),
            "all_remainders_scalar_oracle_inverse_rewind": True,
            "tensor_hash": hashlib.sha256(json.dumps(tensor.to_dict(), sort_keys=True).encode()).hexdigest(),
            "runs": results}


def locality_control():
    # A direct plaquette has the diagonal vertex n+ex+ey; rejected before run.
    try:
        Tensor([GearType("audit.plaquette")],
               [Monomial(0, 1, (Factor(0, (1, 1, 0), "b"),))],
               strict_support=True)
    except LocalityError:
        return {"direct_diagonal_plaquette_factor_rejected": True}
    raise AssertionError("illegal plaquette accepted")


def main():
    report = {"scope": "Cubic conservative flux algebra and one-channel actual Engine control; not gravity.",
              "identities": shift_identities(), "conservative": run_control(True),
              "naive_chain_rule_negative": run_control(False), "locality": locality_control(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    path = ROOT / "runs/research_eight/02_shift_flux.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
