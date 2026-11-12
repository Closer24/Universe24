"""Exact native Rule3 lattice-map audit; no Einstein/clock acceptance claim.

Run from repository root:
python -m validation.research_eight.01_native_lattice_audit
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice


def bits(state):
    return max(abs(int(x)).bit_length() for arr in (state.a, state.b, state.r)
               for x in arr.flat)


def direct(a, b, r, force):
    """Independent scalar law and its conjugate integer kick--drift form."""
    ell, rn = divmod(2 * (6 * b + force) + r, 6)
    q, p = b, 6 * (b - a) + r
    pn = p + 2 * force
    qn = q + pn // 6
    assert (b, ell - a, rn) == (q, qn, pn % 6)
    assert pn == 6 * (qn - q) + rn
    assert (q - p // 6, q, p % 6) == (a, b, r)
    return q, qn, rn


def scalar_identity():
    count = 0
    for a in range(-12, 13):
        for b in range(-12, 13):
            for r in range(6):
                for force in (-10001, -27, -1, 0, 1, 27, 10001):
                    direct(a, b, r, force)
                    count += 1
    def kinetic(p):
        m, s = divmod(p, 6)
        return 3 * m * (m - 1) + m * s
    for p in range(-10000, 10001):
        assert kinetic(p + 1) - kinetic(p) == p // 6
    return {"status": "passed", "comparisons": count, "all_six_remainders": True,
            "integer_kinetic_difference_checks": 20001}


def oscillator():
    tensor = Tensor([GearType("q", label="audit")],
                    [("q", 3, (("q", ZERO, "b"),))], strict_support=True)
    engine = Engine(tensor)
    rng = np.random.default_rng(11012026)
    a = rng.integers(-1000, 1001, size=(1, 27)).astype(object)
    b = rng.integers(-1000, 1001, size=(1, 27)).astype(object)
    r = np.array([[i % 6 for i in range(27)]], dtype=object)
    seed = State(3, a, b, r)
    invariant = seed.a ** 2 - seed.a * seed.b + seed.b ** 2
    state, max_bits = seed, bits(seed)
    for n in range(1, 601):
        old = state
        state = engine.step(old)
        assert np.array_equal(state.b, old.b - old.a)
        assert np.array_equal(state.r, r)
        assert np.array_equal(state.a ** 2 - state.a * state.b + state.b ** 2,
                              invariant)
        assert engine.inverse_step(state).same_as(old)
        if n % 6 == 0:
            assert state.same_as(seed)
        max_bits = max(max_bits, bits(state))
    assert engine.rewind(state, 600).same_as(seed)
    return {"status": "passed", "channels": 1, "degree": 1, "steps": 600,
            "nodes": 27, "period_divides": 6, "max_retained_bits": max_bits,
            "full_rewind": True, "physical_clock": "not_tested"}


def flat_wave():
    tensor = Tensor([GearType("q", label="audit")], [
        ("q", 3, (("q", (1, 0, 0), "b"),)),
        ("q", 3, (("q", (-1, 0, 0), "b"),)),
    ], strict_support=True)
    engine = Engine(tensor)
    L, steps = 5, 1000
    rng = np.random.default_rng(11012027)
    f = [int(x) for x in rng.integers(-(1 << 20), 1 << 20, size=L)]
    g = [int(x) for x in rng.integers(-(1 << 20), 1 << 20, size=L)]
    xyz = lattice(L).all_coords()

    def exact(n):
        return np.array([[f[(int(x) + n) % L] + g[(int(x) - n) % L]
                          for x, _, _ in xyz]], dtype=object)

    remainder = np.array([[i % 6 for i in range(L ** 3)]], dtype=object)
    seed = State(L, exact(-1), exact(0), remainder)
    state, max_bits = seed, bits(seed)
    for n in range(1, steps + 1):
        old = state
        state = engine.step(old)
        assert np.array_equal(state.b, exact(n))
        assert np.array_equal(state.r, remainder)
        assert engine.inverse_step(state).same_as(old)
        max_bits = max(max_bits, bits(state))
    assert engine.rewind(state, steps).same_as(seed)
    # Honest negative control: unconstrained two-slice data has a secular mode.
    ones = np.ones((1, L ** 3), dtype=object)
    zeros = np.zeros_like(ones)
    bad_seed = State(L, ones, zeros, remainder)
    bad = engine.run(bad_seed, steps)
    assert np.all(bad.b == -steps)
    assert engine.rewind(bad, steps).same_as(bad_seed)
    return {"status": "passed", "channels": 1, "degree": 1, "steps": steps,
            "nodes": L ** 3, "max_retained_bits": max_bits,
            "independent_exact_transport": True, "all_six_remainders": True,
            "full_rewind": True, "unbounded_zero_mode_control": {
                "status": "failed_boundedness_as_expected", "q_at_final": -steps},
            "curved_geometry_and_backreaction": "not_tested"}


def nonlinear_negative():
    # u=5q-q^3, or F=-q-q^3; reversibility does not imply boundedness.
    tensor = Tensor([GearType("q", label="audit")], [
        ("q", 5, (("q", ZERO, "b"),)),
        ("q", -1, (("q", ZERO, "b"),) * 3),
    ], strict_support=True)
    engine = Engine(tensor)
    seed = State(3, np.full((1, 27), 0, dtype=object),
                 np.full((1, 27), 4, dtype=object),
                 np.array([[i % 6 for i in range(27)]], dtype=object))
    state, sizes = seed, [bits(seed)]
    for _ in range(8):
        old = state
        state = engine.step(old)
        for j in range(27):
            aa, bb, rr = old.gear(0, j)
            assert state.gear(0, j) == direct(aa, bb, rr, -bb - bb ** 3)
        assert engine.inverse_step(state).same_as(old)
        sizes.append(bits(state))
    assert engine.rewind(state, 8).same_as(seed)
    return {"status": "failed_boundedness_as_expected", "channels": 1,
            "bits_by_step": sizes, "exact_native_identity": True,
            "full_rewind": True}


def coefficient_obstruction():
    # For x=q/S and target x''=c_d*x^d, the raw force coefficient is
    # k_d=3*h^2*c_d/S^(d-1). This is a direct-force, common-scale obstruction,
    # not a theorem against alternative representations or multi-tick circuits.
    rows = []
    for S in (2, 4, 8, 16, 32):
        h = Fraction(1, S)
        row = {"S": S, "h": str(h)}
        for d in (1, 2, 3):
            c = 3 * h * h / S ** (d - 1)
            row[f"degree_{d}_coefficient"] = str(c)
            row[f"degree_{d}_integer"] = c.denominator == 1
        rows.append(row)
    assert all(not row[f"degree_{d}_integer"] for row in rows for d in (1, 2, 3))
    return {"status": "blocked_for_direct_scaled_force", "rows": rows}


def main():
    here = Path(__file__).resolve()
    result = {"schema": "universe24/research-eight/native-lattice/1",
              "source_sha256": hashlib.sha256(here.read_bytes()).hexdigest(),
              "runtime_change": False, "new_physical_model": False,
              "identity": scalar_identity(), "oscillator": oscillator(),
              "flat_wave": flat_wave(), "nonlinear_negative": nonlinear_negative(),
              "direct_refinement_obstruction": coefficient_obstruction()}
    output = Path("runs/research_eight/01_native_lattice_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
