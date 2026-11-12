"""Three-tick native nonlinear lifting compiler; source-only research audit.

Run: python -m validation.completion.native_compiler
No runtime quotient/force callback is installed. Engine alone advances state.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PIN = "62202fdccdd9a40d5dbbec104de6f97d9587a999"
NAMES = ("phi", "g", "phase")


def make_tensor(*, coupling=1, drift=0):
    """One immutable tensor, 3 channels including the restored scheduler.

    Physical/auxiliary variables are NOT appended to corrected45. All monomials
    are onsite or on exactly one face. Only the clock's old a is read.
    """
    assert isinstance(coupling, int) and isinstance(drift, int)
    terms = [("phase", 3, ()), ("phase", -3, (("phase", ZERO, "b"),))]
    for name in NAMES[:2]:
        terms.append((name, -3, ((name, ZERO, "b"),)))
        if drift:
            terms.append((name, 3*drift,
                          (("phase", ZERO, "a"), (name, ZERO, "b"))))

    def term(name, coefficient, factors):
        if coefficient:
            terms.append((name, coefficient,
                          (("phase", ZERO, "b"),)+tuple((f, o, "b") for f, o in factors)))

    for sign in (-1, 1):
        edge = (sign, 0, 0)
        for gpos in (ZERO, edge):
            term("phi", 2*coupling, [("g", gpos), ("phi", edge)])
            term("phi", -2*coupling, [("g", gpos), ("phi", ZERO)])
        term("g", -coupling, [("phi", edge), ("phi", edge)])
        term("g", 2*coupling, [("phi", edge), ("phi", ZERO)])
        term("g", -coupling, [("phi", ZERO), ("phi", ZERO)])
    return Tensor([GearType(name, label="audit") for name in NAMES], terms,
                  strict_support=True)


def forces(q, lat, *, coupling=1):
    """Independent edge-potential derivative; validation only."""
    phi, g = np.asarray(q, dtype=object)
    fphi, fg = np.zeros_like(phi), np.zeros_like(g)
    for sign in (-1, 1):
        ix = lat.shift_index((sign, 0, 0))
        delta = phi[ix]-phi
        fphi += 2*coupling*(g+g[ix])*delta
        fg -= coupling*delta*delta
    return np.asarray([fphi, fg], dtype=object)


def macro_oracle(state, *, coupling=1, drift=0):
    q = state.a[:2].astype(object)+state.b[:2].astype(object)
    f = forces(q, lattice(state.L), coupling=coupling)
    total = 2*f+state.r[:2]
    quotient, rem = total//6, total % 6
    an, bn, rn = (arr.astype(object) for arr in (state.a, state.b, state.r))
    an[:2] += quotient
    bn[:2] = q + drift*an[:2] - an[:2]
    rn[:2] = rem
    return State(state.L, an, bn, rn)


def inverse_macro_oracle(after, *, coupling=1, drift=0):
    oldq = after.a[:2].astype(object)+after.b[:2].astype(object)-drift*after.a[:2].astype(object)
    f = forces(oldq, lattice(after.L), coupling=coupling)
    oldr = (after.r[:2]-2*f) % 6
    quotient = (2*f+oldr-after.r[:2])//6
    a, b, r = (arr.astype(object) for arr in (after.a, after.b, after.r))
    a[:2] -= quotient
    b[:2] = oldq-a[:2]
    r[:2] = oldr
    return State(after.L, a, b, r)


def complete_bits(state):
    return max(abs(int(v)).bit_length() for arr in (state.a, state.b, state.r)
               for v in arr.flat)


def seed_all_remainders(L=6):
    lat = lattice(L)
    assert lat.N >= 216
    combos = list(itertools.product(range(6), repeat=3))
    a = np.zeros((3, lat.N), dtype=object)
    b = np.zeros_like(a)
    r = np.zeros_like(a)
    for i in range(lat.N):
        a[0, i], a[1, i] = i % 5-2, (i//5) % 5-2
        b[0, i], b[1, i] = (i//7) % 5-2, (i//11) % 5-2
        r[:, i] = combos[i % 216]
    return State(L, a, b, r)


def signed_audit():
    rows = []
    for coupling, drift in itertools.product((-2, -1, 0, 1, 2), (-1, 0, 1, 2)):
        tensor = make_tensor(coupling=coupling, drift=drift)
        engine = Engine(tensor)
        seed = seed_all_remainders()
        state = seed
        peak = complete_bits(seed)
        charge = int(sum(6*seed.a[0].astype(object)+seed.r[0]))
        for period in range(6):
            before = state
            expected = macro_oracle(before, coupling=coupling, drift=drift)
            for _ in range(3):
                after = engine.step(state)
                assert engine.inverse_step(after).same_as(state)
                state = after
                peak = max(peak, complete_bits(state))
            assert state.same_as(expected)
            assert inverse_macro_oracle(state, coupling=coupling, drift=drift).same_as(before)
            assert all(int(v) == 0 for arr in (state.a[2], state.b[2]) for v in arr)
            assert np.array_equal(state.r[2], seed.r[2])
            assert int(sum(6*state.a[0].astype(object)+state.r[0])) == charge
        assert engine.rewind(state, 18).same_as(seed)
        assert not tensor.support_violations()
        rows.append({"coupling": coupling, "drift": drift, "periods": 6,
                     "nodes": seed.N, "all_216_remainder_triples": True,
                     "macro_oracle_and_inverse": True, "all_step_inverses_and_rewind": True,
                     "scheduler_full_state_restored": True, "phi_shift_charge": charge,
                     "peak_complete_bits": peak, "tensor_sha256": tensor.fingerprint})
    return rows


def potential_refinement():
    """Exact potential-only subflow with h=1/Q, not a full ODE integrator."""
    tensor = make_tensor()
    engine = Engine(tensor)
    lat = lattice(3)
    xcoord = lat.all_coords()[:, 0].astype(int)
    rows = []
    for scale in (3, 9, 27, 81, 243):
        momentum_scale = 2*scale**3
        a = np.zeros((3, lat.N), dtype=object)
        b = np.asarray([[scale*(int(x)-1) for x in xcoord],
                        [scale]*lat.N, [0]*lat.N], dtype=object)
        r = np.asarray([[(i+j) % 6 for i in range(lat.N)] for j in range(3)], dtype=object)
        seed = State(3, a, b, r)
        state = seed
        q0 = seed.a[:2]+seed.b[:2]
        p0 = 6*seed.a[:2]+seed.r[:2]
        f0 = forces(q0, lat)
        peak = complete_bits(seed)
        for _ in range(scale):
            expected = macro_oracle(state)
            for _ in range(3):
                state = engine.step(state)
                peak = max(peak, complete_bits(state))
            assert state.same_as(expected)
        assert np.array_equal(state.a[:2]+state.b[:2], q0)
        assert np.array_equal(6*state.a[:2]+state.r[:2], p0+2*scale*f0)
        # T=Nh=1 and F is homogeneous of degree two: exact physical momentum change.
        for p, initp, force in zip((6*state.a[:2]+state.r[:2]).flat, p0.flat, f0.flat):
            assert Fraction(int(p-initp), momentum_scale) == Fraction(int(force), scale**2)
        assert engine.rewind(state, 3*scale).same_as(seed)
        rows.append({"position_scale": scale, "momentum_scale": momentum_scale,
                     "h": str(Fraction(1, scale)), "T": 1, "periods": scale,
                     "microticks": 3*scale, "exact_potential_flow_error": "0",
                     "full_rewind": True, "peak_complete_bits": peak})
    return {"status": "passed_for_potential_subflow_only", "tensor_sha256": tensor.fingerprint,
            "rows": rows, "kinetic_plus_potential_refinement": "blocked_in_this_ansatz"}


def identities_and_negative_controls():
    x, y, g, k, lam = sp.symbols("x y g k lam")
    v = lam*(g+k)*(y-x)**2
    f = [-sp.diff(v, z) for z in (x, y, g, k)]
    assert sp.expand(f[0]+f[1]) == 0
    assert sp.expand(sp.diff(f[0], g)-sp.diff(f[2], x)) == 0
    assert sp.expand(f[0]-2*lam*(g+k)*(y-x)) == 0
    assert sp.expand(f[2]+lam*(y-x)**2) == 0
    # Clock x cubic force is degree four; actual Tensor must reject it.
    try:
        Tensor(NAMES, [("phi", 1, (("phase", ZERO, "b"),
                                   ("phi", ZERO, "b"), ("g", ZERO, "b"),
                                   ("g", ZERO, "b")))], strict_support=True)
    except (ValueError, TypeError):
        quartic_rejected = True
    else:
        raise AssertionError("quartic force gate unexpectedly accepted")
    # Nonzero L,k integer and positive Q: h^2=L*k*Q/3 for fixed quadratic force.
    obstruction = [{"Q": coordinate_amplitude, "requested_h": str(Fraction(1, coordinate_amplitude)),
                    "required_force_multiplier_at_L1": str(Fraction(3, coordinate_amplitude**3)),
                    "is_integer": Fraction(3, coordinate_amplitude**3).denominator == 1}
                   for coordinate_amplitude in (3, 9, 27, 81)]
    assert all(not item["is_integer"] for item in obstruction)
    return {"edge_potential": "lambda*(g_i+g_j)*(phi_j-phi_i)^2",
            "negative_gradient_reciprocity_and_shift_charge": "passed",
            "clock_times_cubic_force_rejected": quartic_rejected,
            "full_drift_refinement_obstruction": obstruction,
            "scope": "three-tick quadratic force plus integer drift and one common position scale"}


def make_quotient_tensor(*, coupling=None):
    """Nine-tick compute/copy/uncompute for two independent floor(a/3) drifts.

    Total: 2 data + 2 quotient work + 2 internal clocks = 6 channels.
    The macro oracle's quotient is never called by the Engine.
    """
    names = ("phi", "g", "w_phi", "w_g", "fast", "slow")
    if coupling is not None:
        names += ("pulse",)
    terms = []

    def add(target, coeff, *factors):
        terms.append((target, coeff, tuple((name, ZERO, layer) for name, layer in factors)))

    add("fast", 3)
    add("fast", -3, ("fast", "b"))
    add("slow", -3, ("slow", "b"))
    add("slow", 9, ("fast", "b"), ("slow", "b"))
    add("slow", 3, ("fast", "b"))
    add("slow", 3, ("fast", "a"), ("slow", "b"))
    for data, work in (("phi", "w_phi"), ("g", "w_g")):
        add(data, -3, (data, "b"))
        add(data, -3, ("fast", "a"), ("slow", "a"), (work, "b"))
        add(work, -3, (work, "b"))
        # -b_fast*(1-2*a_slow+b_slow)*(a_data+b_data).
        for layer in ("a", "b"):
            add(work, -1, ("fast", "b"), (data, layer))
            add(work, 2, ("fast", "b"), ("slow", "a"), (data, layer))
            add(work, -1, ("fast", "b"), ("slow", "b"), (data, layer))
    if coupling is not None:
        # H=t_next+t_old for a period9 pulse t=1 only at microphase7.
        # H=2*a_fast*a_slow-2*a_fast*b_slow+a_fast-b_fast*b_slow+b_slow.
        add("pulse", 6, ("fast", "a"), ("slow", "a"))
        add("pulse", -6, ("fast", "a"), ("slow", "b"))
        add("pulse", 3, ("fast", "a"))
        add("pulse", -3, ("fast", "b"), ("slow", "b"))
        add("pulse", 3, ("slow", "b"))

        def potential_term(target, coefficient, factors):
            if coefficient:
                terms.append((target, coefficient, (("pulse", ZERO, "b"),)+
                              tuple((name, offset, "b") for name, offset in factors)))

        for sign in (-1, 1):
            edge = (sign, 0, 0)
            for gpos in (ZERO, edge):
                potential_term("phi", 2*coupling, [("g", gpos), ("phi", edge)])
                potential_term("phi", -2*coupling, [("g", gpos), ("phi", ZERO)])
            potential_term("g", -coupling, [("phi", edge), ("phi", edge)])
            potential_term("g", 2*coupling, [("phi", edge), ("phi", ZERO)])
            potential_term("g", -coupling, [("phi", ZERO), ("phi", ZERO)])
    return Tensor([GearType(n, label="audit") for n in names], terms, strict_support=True)


def quotient_audit():
    tensor = make_quotient_tensor()
    engine = Engine(tensor)
    lat = lattice(6)
    rows = []
    for work_remainder in range(6):
        a, b, r = (np.zeros((6, lat.N), dtype=object) for _ in range(3))
        for i in range(lat.N):
            a[0, i], a[1, i] = i-108, 108-i
            b[0, i], b[1, i] = i % 13-6, i % 7-3
            r[0, i], r[1, i] = i % 6, (i//6) % 6
            r[2, i] = r[3, i] = work_remainder
            r[4, i], r[5, i] = (i//36) % 6, (i//6) % 6
        seed = State(6, a, b, r)
        state = seed
        increments = (2*seed.a[:2].astype(object)+work_remainder)//6
        peak = complete_bits(seed)
        for period in range(12):
            before = state
            for _ in range(9):
                after = engine.step(state)
                assert engine.inverse_step(after).same_as(state)
                state = after
                peak = max(peak, complete_bits(state))
            assert np.array_equal(state.a, seed.a)
            assert np.array_equal(state.r, seed.r)
            assert np.array_equal(state.b[:2], before.b[:2].astype(object)+increments)
            assert np.array_equal(state.b[2:], seed.b[2:])
            if work_remainder in (0, 1):
                assert np.array_equal(increments, seed.a[:2]//3)
        assert engine.rewind(state, 108).same_as(seed)
        rows.append({"work_remainder": work_remainder, "periods": 12,
                     "microticks": 108, "signed_data_a_range": [-108, 108],
                     "all_six_data_and_clock_remainders": True,
                     "oracle_step_inverses_full_rewind": True,
                     "all_workspace_and_clock_state_restored_every_period": True,
                     "unbiased_floor_a_over3": work_remainder in (0, 1),
                     "peak_complete_bits": peak})
    return {"status": "passed", "channels": tensor.G, "integers_per_node": 3*tensor.G,
            "terms": len(tensor), "degree": tensor.rank-1,
            "strict_single_face": not tensor.support_violations(),
            "tensor_sha256": tensor.fingerprint, "rows": rows,
            "exact_prepared_map": "S_j -> S_j+floor(a_j/3); a_j,r_j unchanged; workspace/clock restored",
            "joint_nonlinear_potential_schedule": "see_seven_channel_joint_audit",
            "arbitrary_k_division": "not_implemented",
            "drop_in_corrected45": False}


def joint_nonlinear_audit():
    """One immutable 7-channel law combines quotient drift and reciprocal kick."""
    rows = []
    for coupling, work_mode in itertools.product((-2, -1, 0, 1, 2), ("prepared_zero", "all_six")):
        tensor = make_quotient_tensor(coupling=coupling)
        engine = Engine(tensor)
        lat = lattice(6)
        a, b, r = (np.zeros((7, lat.N), dtype=object) for _ in range(3))
        for i in range(lat.N):
            a[0, i], a[1, i] = i % 7-3, (i//7) % 7-3
            b[0, i], b[1, i] = i % 5-2, (i//5) % 5-2
            r[0, i], r[1, i] = i % 6, (i//6) % 6
            if work_mode == "all_six":
                r[2, i], r[3, i] = (i//36) % 6, (i//6) % 6
            r[4:, i] = [(i+j) % 6 for j in range(3)]
        seed = State(6, a, b, r)
        state = seed
        peak = complete_bits(seed)
        bit_history = [peak]
        for period in range(6):
            old = state
            olda, oldb = old.a[:2].astype(object), old.b[:2].astype(object)
            drifted = olda+oldb+(2*olda+old.r[2:4])//6
            if work_mode == "prepared_zero":
                assert np.array_equal(drifted, olda+oldb+(6*olda+old.r[:2])//18)
            newp = 6*olda+old.r[:2]+2*forces(drifted, lat, coupling=coupling)
            expected_a = newp//6
            expected_b = drifted-expected_a
            for phase in range(9):
                assert all(int(value) == int(phase == 7) for value in state.b[6])
                after = engine.step(state)
                assert engine.inverse_step(after).same_as(state)
                state = after
                peak = max(peak, complete_bits(state))
            assert np.array_equal(state.a[:2], expected_a)
            assert np.array_equal(state.b[:2], expected_b)
            assert np.array_equal(state.r[:2], newp % 6)
            for arr, original in zip((state.a, state.b, state.r), (seed.a, seed.b, seed.r)):
                assert np.array_equal(arr[2:], original[2:])
            assert int(sum(6*state.a[0].astype(object)+state.r[0])) == int(sum(6*seed.a[0]+seed.r[0]))
            bit_history.append(complete_bits(state))
        assert engine.rewind(state, 54).same_as(seed)
        rows.append({"coupling": coupling, "work_remainders": work_mode,
                     "periods": 6, "microticks": 54,
                     "nodes": lat.N, "all_six_data_and_clock_remainders": True,
                     "all_six_work_remainders": work_mode == "all_six",
                     "oracle_all_step_inverses_and_full_rewind": True,
                     "scheduler_workspace_full_state_restored": True,
                     "phi_shift_charge_conserved": True,
                     "boundary_complete_bits": bit_history, "peak_complete_bits": peak,
                     "tensor_sha256": tensor.fingerprint})
    return {"status": "passed_finite_k1_nonlinear_compiler", "channels": 7,
            "data_channels": 2, "workspace_channels": 2, "scheduler_channels": 3,
            "integers_per_node": 21, "terms": len(make_quotient_tensor(coupling=1)),
            "degree": 3, "microticks_per_period": 9,
            "strict_single_face": not make_quotient_tensor(coupling=1).support_violations(),
            "prepared_work_remainders": "0 or 1 gives exact floor(P/18) drift",
            "macro_map": "S*=S+floor(P/18); P'=P+2*F(S*); S'=S*",
            "arbitrary_k_or_continuum_refinement": "not_implemented",
            "drop_in_corrected45": False, "rows": rows}


def main():
    tensor = make_tensor(drift=1)
    report = {"source_pin": SOURCE_PIN,
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "status": "native k1 nonlinear compiler passed; arbitrary refinement blocked",
              "allocation": {"data_channels": 2, "scheduler_channels": 1,
                             "workspace_channels": 0, "total_channels": tensor.G,
                             "integers_per_node": 3*tensor.G, "terms_with_drift": len(tensor),
                             "degree": tensor.rank-1, "strict_single_face": not tensor.support_violations(),
                             "retained_denominator_channels": 0,
                             "compatible_drop_in_to_corrected45": False},
              "identities": identities_and_negative_controls(),
              "signed_all_remainders": signed_audit(),
              "native_quotient_compute_copy_uncompute": quotient_audit(),
              "joint_nonlinear_compiler": joint_nonlinear_audit(),
              "potential_flow_refinement": potential_refinement(),
              "not_claimed": ["kinetic/nonlinear full-equation convergence", "Einstein geometry",
                              "physical momentum or energy conservation", "metric positivity",
                              "proper-time clock", "general cubic-force arithmetic compiler"]}
    out = ROOT/"runs/completion/native_compiler.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"out": str(out), "status": report["status"],
                      "allocation": report["allocation"],
                      "signed_parameter_cases": len(report["signed_all_remainders"]),
                      "quotient_primitive": {k:v for k,v in report["native_quotient_compute_copy_uncompute"].items()
                                             if k != "rows"},
                      "joint_nonlinear_compiler": {k:v for k,v in report["joint_nonlinear_compiler"].items()
                                                  if k != "rows"},
                      "potential_rows": report["potential_flow_refinement"]["rows"]}))


if __name__ == "__main__":
    main()
