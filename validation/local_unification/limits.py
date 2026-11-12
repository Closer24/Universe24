"""Exact limits of the selected local carrier--record law.

These are scoped constructive certificates and counterexamples, not a no-go
theorem for all Rule3 models.  In particular, the twelve-channel geometry is
unbounded; only its autonomous prepared eight-rail projection is finite.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np

from universe24.core import DIRECTIONS, Engine, State, exact_json
from validation.local_unification import native


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an exact integer >= {minimum}")
    return value


def _population(values):
    values = np.asarray(values, dtype=object)
    if values.ndim != 2 or values.shape[0] != 8:
        raise ValueError("eight current Boolean rail rows are required")
    if any(isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, np.integer))
           or int(v) not in (0, 1) for v in values.flat):
        raise ValueError("the free-stream theorem requires the Boolean sector")
    return (values[0]+values[2]+values[4]+values[6],
            values[1]+values[3]+values[5]+values[7])


def _literal_collision(bits):
    # Independent table, not the candidate polynomial or native.gate.
    bits = tuple(bits)
    return ((0, 1, 1, 0) if bits == (1, 0, 0, 1) else
            (1, 0, 0, 1) if bits == (0, 1, 1, 0) else bits)


def local_proof():
    rows = []
    drifts = {"ready": [], "used": [], "all": []}
    for bits in product((0, 1), repeat=4):
        out = _literal_collision(bits)
        assert _literal_collision(out) == bits
        assert bits[0]+bits[2] == out[0]+out[2]
        assert bits[1]+bits[3] == out[1]+out[3]
        change = (out[2]-out[3])-(bits[2]-bits[3])
        drifts["all"].append(change)
        if bits[:2] == (1, 0):
            drifts["ready"].append(change)
        if bits[:2] == (0, 1):
            drifts["used"].append(change)
        rows.append({"input": list(bits), "output": list(out), "carrier_order_change": change})
    means = {name: Fraction(sum(values), len(values)) for name, values in drifts.items()}
    assert means == {"ready": Fraction(1, 2), "used": Fraction(-1, 2), "all": Fraction(0)}
    return {"truth_table": rows, "conditional_order_drift": means,
            "order_proxy": "carrier_plus - carrier_minus; not structural complexity",
            "stationary_ensemble_identity": "E_mu[C(F(s))-C(s)]=0 for invariant mu",
            "finite_projection": "fixed carries and prepared Boolean prefix: at most 2^(8N) states",
            "twelve_channel_finite_state_claim": False}


def _profile(data, name):
    if type(data) is not dict or not data:
        raise ValueError(f"{name} must be a nonempty finite occupancy mapping")
    result = {}
    for position, count in data.items():
        if type(position) is not int:
            raise ValueError("unwrapped positions must be exact signed integers")
        _integer(count, "occupancy")
        if count:
            result[position] = count
    return result


def spread_polynomial(plus, minus):
    """Return exact Q(m)=E*second_moment(m)-first_moment(m)^2.

    Coordinates are unwrapped integers, not periodic distances. Q2=4E+E-
    rules out a uniformly localized positive two-stream energy distribution
    around its inertial centroid on the infinite line.
    """
    plus, minus = _profile(plus, "plus"), _profile(minus, "minus")
    Ep, Em = sum(plus.values()), sum(minus.values())
    E, P = Ep+Em, Ep-Em
    if not E:
        raise ValueError("a nonzero finite energy distribution is required")
    Mp = sum(x*n for x, n in plus.items())
    Mm = sum(x*n for x, n in minus.items())
    M = Mp+Mm
    second = sum(x*x*n for row in (plus, minus) for x, n in row.items())
    return {"E": E, "P": P, "Q0": E*second-M*M,
            "Q1": 2*(E*(Mp-Mm)-P*M), "Q2": E*E-P*P,
            "centroid_velocity": Fraction(P, E),
            "mass_squared": 4*Ep*Em}


def moment_certificate():
    cases = []
    for plus, minus in (({0: 1}, {0: 1}),
                        ({-2: 2, 1: 1}, {3: 2}),
                        ({-1: 1, 2: 2}, {0: 0})):
        proof = spread_polynomial(plus, minus)
        assert proof["Q2"] == proof["mass_squared"]
        checks = []
        for m in (0, 1, 2, 7, 100):
            first = sum((x+m)*n for x, n in plus.items()) + sum((x-m)*n for x, n in minus.items())
            second = sum((x+m)**2*n for x, n in plus.items()) + sum((x-m)**2*n for x, n in minus.items())
            actual = proof["E"]*second-first*first
            expected = proof["Q0"]+proof["Q1"]*m+proof["Q2"]*m*m
            assert actual == expected
            checks.append({"macro": m, "centered_moment_times_energy": actual})
        cases.append({"proof": proof, "checks": checks})
    return {"cases": cases, "domain": "finite nonnegative unwrapped support; no confinement or periodic wrapping",
            "conclusion": "E>|P| implies unbounded quadratic energy spread about the centroid",
            "excluded_claims": ["no statement about torus refocusing",
                                "no prohibition on transient label correlations",
                                "not a no-go theorem for other Rule3 laws"]}


def free_stream_audit():
    rng = np.random.default_rng(630110)
    comparisons = transitions = 0
    for direction in DIRECTIONS:
        current = rng.integers(0, 2, size=(8, 27)).astype(object)
        carries = np.asarray([[(g+n) % 6 for n in range(27)] for g in range(8)], dtype=object)
        seed = native.prepare_state(current, 3, direction, remainders=carries)
        engine = Engine(native.build_tensor(direction))
        state = seed
        initial = _population(seed.b)
        for tick in range(1, 7):
            after = engine.step(state)
            assert engine.inverse_step(after).same_as(state)
            assert np.array_equal(after.r, carries)
            state = after
            transitions += 1
            if tick % 2 == 0:
                macro = tick//2
                populations = _population(state.b)
                for sign in (0, 1):
                    offset = tuple((-1 if sign == 0 else 1)*d for d in direction)
                    indices = np.arange(state.N)
                    for _ in range(macro):
                        indices = indices[state.lattice.shift_index(offset)]
                    expected = initial[sign][indices]
                    assert np.array_equal(populations[sign], expected)
                    comparisons += state.N
        assert engine.rewind(state, 6).same_as(seed)
    return {"Engine_transitions": transitions, "exact_density_comparisons": comparisons,
            "directions": 6, "ticks_per_macro": 2,
            "identity": "n_plus(m,x)=n_plus(0,x-m*d); n_minus(m,x)=n_minus(0,x+m*d)",
            "geometry_feedback_into_packet_prefix": False}


def offset_geometry(state, constant):
    """An exact full-state symmetry; leaves all eight packet histories intact."""
    _integer(constant, "positive profile offset", 1)
    if not isinstance(state, State):
        raise ValueError("a complete State is required")
    state = State(state.L, state.a, state.b, state.r)
    if state.b.shape[0] != 12:
        raise ValueError("the selected source construction has twelve channels")
    after = state.copy()
    after.a[8:12] += constant
    after.b[8:12] += constant
    return after


def _center_R(state):
    # At an integer coordinate the independent cubic B-spline weights are
    # (1/6, 4/6, 1/6). The default chart is planar in the positive x direction.
    center = state.L//2
    values = []
    for x in (center-1, center, center+1):
        node = state.lattice.index(x, 0, 0)
        values.append(sum(int(state.b[g, node]) for g in range(8, 12)))
    return Fraction(values[0]+4*values[1]+values[2], 6)


def clock_offset_audit():
    from validation.local_unification import geometry

    law, seed, protocol = geometry.prepare_fixture(L=11, steps=2)
    constant = 100
    shifted_seed = offset_geometry(seed, constant)
    state, shifted = seed, shifted_seed
    engine = Engine(law)
    packet_checks = profile_checks = 0
    rates = []
    for tick in range(3):
        for name in ("a", "b", "r"):
            left, right = getattr(state, name), getattr(shifted, name)
            assert np.array_equal(left[:8], right[:8])
            packet_checks += 8*state.N
        for name in ("a", "b"):
            assert np.all(getattr(shifted, name)[8:]-getattr(state, name)[8:] == constant)
            profile_checks += 4*state.N
        assert np.array_equal(shifted.r, state.r)
        assert np.array_equal(geometry.profile_constraints(state),
                              geometry.profile_constraints(shifted))
        if tick % 2 == 0:
            R, shifted_R = _center_R(state), _center_R(shifted)
            assert R > 0 and shifted_R == R+4*constant
            # (d tau_shift / d tau)^4=R/(R+4C), strictly less than1.
            ratio4 = R/shifted_R
            assert 0 < ratio4 < 1
            rates.append({"microtick": tick, "R": R, "shifted_R": shifted_R,
                          "proper_rate_ratio_fourth_power": ratio4})
        if tick < 2:
            next_state, next_shifted = engine.step(state), engine.step(shifted)
            assert engine.inverse_step(next_state).same_as(state)
            assert engine.inverse_step(next_shifted).same_as(shifted)
            state, shifted = next_state, next_shifted
    assert engine.rewind(state, 2).same_as(seed)
    assert engine.rewind(shifted, 2).same_as(shifted_seed)
    return {"tensor_hash": law.fingerprint, "lattice_size": seed.L, "microticks": 2,
            "packet_register_comparisons": packet_checks,
            "profile_offset_comparisons": profile_checks,
            "constant_per_profile": constant, "R_shift": 4*constant,
            "rate_comparisons": rates,
            "claim": "unchanged packet records alone do not determine metric proper time",
            "not_claimed": ["violation of the equivalence principle",
                            "same apparatus at fixed proper size",
                            "impossibility of a future geometry-sensitive material clock"]}


def _json(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict):
        return {str(k): _json(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json(v) for v in value]
    return value


def audit(out=None):
    report = {"schema": "universe24/local-unification/limits/1",
              "local_and_stationary": local_proof(),
              "free_stream": free_stream_audit(),
              "massive_localization": moment_certificate(),
              "packet_clock_counterexample": clock_offset_audit(),
              "acceptance": {
                  "repeated_source_consistent_null_scattering": "supported by other joined audits",
                  "localized_bound_massive_source_in_this_free_stream_sector": "excluded on the stated unwrapped domain",
                  "universal_packet_only_proper_clock": "failed",
                  "indefinite_strict_packet_state_complexity_growth": "excluded on the finite prepared projection",
                  "global_twelve_channel_finite_state_theorem": "not_claimed",
                  "new_burst_or_global_future_optimizer": "not_implemented"},
              "next_construction_obligations": [
                  "A bound massive source needs interactions that change total directional source flow and satisfy a new source/metric proof.",
                  "A material clock needs a retained mechanism with a declared physical calibration, source and response to the same geometry.",
                  "Organization growth needs a specified preparation, resource account, finite horizon or justified escaping sector, and independent controls.",
                  "No external reset, passive score callback or implicit widening of the declared source chart is admissible."]}
    report = _json(report)
    if out is not None:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(exact_json.dumps(report, sort_keys=True)+"\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification/limits.json"))
    args = parser.parse_args(argv)
    report = audit(args.out)
    print(exact_json.dumps(report["acceptance"], sort_keys=True))


if __name__ == "__main__":
    main()
