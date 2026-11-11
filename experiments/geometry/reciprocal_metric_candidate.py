"""Reciprocal integer candidates, with explicit failures of the gravity target.

The existing Engine is used without modifications.  The edge candidate completes
all derivatives of a phase-decoded metric-shaped interaction.  Its general seed
loses the old TT constraints.  A checkerboard preparation preserves only the
algebraic TT sector.  A separate Q=1 reciprocal oscillator has an exact bounded
period-five orbit; its positive gamma is a chosen readout, not a derived metric.
The final candidate extends that bounded construction to positive spatial link
stiffnesses; its invariant standing pattern is still not Einstein geometry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.core.reciprocity import check_reciprocity
from universe24.core.tensor import GearType
from experiments.geometry.linear_spin2_check import build as curl_tensor
from experiments.geometry.linear_spin2_check import constraints, curl, phase_seed

ZERO = (0, 0, 0)


def derivative_terms(coefficient, variables):
    """Differentiate a translated integer potential monomial at every slot.

    Repeated slots deliberately produce repeated terms, which Tensor merges.
    The resulting terms contain integer coefficients exclusively.
    """
    terms = []
    for index, (target, origin) in enumerate(variables):
        factors = tuple((gear, tuple(x-y for x, y in zip(offset, origin)), "b")
                        for j, (gear, offset) in enumerate(variables) if j != index)
        terms.append((target, coefficient, factors))
    return terms


def build_edge_candidate(Q=1, kappa=1):
    """Phi_int=kappa sum_xy_edges sigma (F_x+F_y)(chi_y-chi_x)^2.

    F=c(E00-E11)+s(B01+B10).  All four metric derivatives and both
    phase derivatives are included.  The free matter input is Q sum_neighbors
    chi_y, equivalently D chi + Q Laplacian chi with D=6Q.
    """
    if type(Q) is not int or Q < 1 or type(kappa) is not int:
        raise ValueError("Q must be a positive integer and kappa an integer")
    base = curl_tensor(Q)
    names = ["metric."+n for n in base.names]
    gears = [GearType(n, "audit") for n in names]
    gears += [GearType("phase.c", "audit"), GearType("phase.s", "audit"),
              GearType("matter")]
    terms = [(names[m.target], m.coeff,
              tuple((names[f.gear], f.offset, f.field) for f in m.factors))
             for m in base.monomials]
    for axis in range(3):
        for sign in (-1, 1):
            offset = tuple(sign if i == axis else 0 for i in range(3))
            terms.append(("matter", Q, (("matter", offset, "b"),)))
    for axis, sigma in ((0, 1), (1, -1)):
        edge = tuple(1 if i == axis else 0 for i in range(3))
        for endpoint in (ZERO, edge):
            for phase, metric, polarity in (("phase.c", "metric.E00", 1),
                                             ("phase.c", "metric.E11", -1),
                                             ("phase.s", "metric.B01", 1),
                                             ("phase.s", "metric.B10", 1)):
                for left, right, weight in ((edge, edge, 1), (ZERO, ZERO, 1),
                                             (edge, ZERO, -2)):
                    variables = ((phase, endpoint), (metric, endpoint),
                                 ("matter", left), ("matter", right))
                    terms.extend(derivative_terms(kappa*sigma*polarity*weight, variables))
    return Tensor(gears, terms, Q=Q, strict_support=True)


def phase_readout(state):
    b = state.b.astype(object)
    return b[18]*(b[0]-b[4])+b[19]*(b[10]+b[12])


def edge_input_oracle(state, Q=1, kappa=1):
    """Independent direct equations, including the reciprocal sources."""
    b = state.b.astype(object)
    lat = state.lattice
    u = np.zeros_like(b, dtype=object)
    u[:9] = (3*Q)*curl(b[9:18].reshape(3, 3, -1), lat).reshape(9, -1)
    u[9:18] = (3*Q)*curl(b[:9].reshape(3, 3, -1), lat).reshape(9, -1)
    F = phase_readout(state)
    H = np.zeros(lat.N, dtype=object)
    for axis in range(3):
        for sign in (-1, 1):
            offset = tuple(sign if i == axis else 0 for i in range(3))
            neighbor = lat.shift_index(offset)
            change = b[20, neighbor]-b[20]
            u[20] += Q*b[20, neighbor]
            sigma = (1, -1, 0)[axis]
            H += sigma*change**2
            u[20] -= 2*kappa*sigma*(F+F[neighbor])*change
    u[0] += kappa*b[18]*H
    u[4] -= kappa*b[18]*H
    u[10] += kappa*b[19]*H
    u[12] += kappa*b[19]*H
    u[18] = kappa*(b[0]-b[4])*H
    u[19] = kappa*(b[10]+b[12])*H
    return u


def prepare_edge(tensor, metric=True, matter="pulse", L=4):
    engine = Engine(tensor, tensor.Q)
    D = 6*tensor.Q
    lat = lattice(L)
    coordinates = np.array([lat.coords(i) for i in range(lat.N)], dtype=int)
    z = coordinates[:, 2]
    profile = np.array([1, -1, 0, 0], dtype=object)
    if L != 4:
        raise ValueError("The explicit integer preparation uses L=4")
    E = np.zeros((3, 3, lat.N), dtype=object)
    B = E.copy()
    if metric:
        E[0, 0] = profile[z]
        E[1, 1] = -profile[z]
        B[0, 1] = profile[(z+1) % L]
        B[1, 0] = B[0, 1]
    core = phase_seed(E, B, tensor.Q, L)
    state = engine.vacuum(L, [D//2-1]*tensor.G)
    state.a[:18] = core.a
    state.b[:18] = core.b
    # Exact signed equality under floor division needs complementary carries.
    state.r[4] = D-1-state.r[0]
    state.b[18] = 1
    state.a[19] = -1
    if matter == "pulse":
        state.b[20] = (coordinates[:, 0] == 0).astype(int)
    elif matter == "checkerboard":
        state.b[20] = np.array([1 if x % 2 == 0 else -1 for x in coordinates[:, 0]])
        state.r[20, coordinates[:, 0] % 2 == 1] = D-1-state.r[20, coordinates[:, 0] % 2 == 1]
    elif matter != "none":
        raise ValueError(matter)
    state.a[20] = state.b[20]
    return state


def maximum(values):
    return max((abs(int(x)) for x in values.flat), default=0)


def state_bytes(state):
    return json.dumps(state.to_dict(), sort_keys=True, separators=(",", ":")).encode("ascii")


def history_fingerprints(history):
    trace = hashlib.sha256()
    for state in history:
        trace.update(state_bytes(state))
        trace.update(b"\n")
    return {"seed_state_sha256": hashlib.sha256(state_bytes(history[0])).hexdigest(),
            "final_state_sha256": hashlib.sha256(state_bytes(history[-1])).hexdigest(),
            "complete_trace_sha256": trace.hexdigest(),
            "trace_hash_convention": "SHA256 of compact sort_keys JSON State.to_dict() plus LF for each state, including the seed"}


def official_quotients(engine, before, after, tick):
    """Only observed official records, including the changed-triple condition."""
    log = engine.clicks(before, after, tick, "official").select("official")
    samples = np.zeros_like(after.b, dtype=object)
    for gear, node, quotient in zip(log.gear, log.node, log.quotient):
        samples[int(gear), int(node)] = int(quotient)
    return log, samples


def audit_tensor(tensor):
    reciprocal = check_reciprocity(tensor)
    reciprocal.raise_if_failed()
    assert not reciprocal.designated
    assert not tensor.support_violations()
    assert all(f.field == "b" for m in tensor.monomials for f in m.factors)
    return {"fingerprint": tensor.fingerprint, "Q": tensor.Q, "D": 6*tensor.Q,
            "gears": tensor.G, "monomials": len(tensor.monomials), "rank": tensor.rank,
            "strict_single_physical_edge_support": True, "reciprocity": True,
            "designated_one_way_terms": 0, "old_a_reads": 0,
            "all_tensor_coefficients_are_integers": True}


def checked_step(engine, before):
    after = engine.step(before)
    u = engine.inputs(before).astype(object)
    ell = after.b.astype(object)+before.a.astype(object)
    assert np.array_equal(2*u+before.r, engine.D*ell+after.r)
    assert np.array_equal(after.a, before.b)
    assert np.all((after.r >= 0) & (after.r < engine.D))
    assert engine.inverse_step(after).same_as(before)
    return after, ell


def run_edge_case(tensor, metric, matter, steps, kappa=1):
    engine = Engine(tensor, tensor.Q)
    seed = prepare_edge(tensor, metric, matter)
    state = seed
    history = [state]
    rows = []
    official = []
    first_TT_failure = None
    first_phase_change = None
    first_readout_shift_failure = None
    initial_F = phase_readout(seed)
    for tick in range(1, steps+1):
        assert np.array_equal(engine.inputs(state), edge_input_oracle(state, tensor.Q, kappa))
        state, ell = checked_step(engine, state)
        history.append(state)
        residual = {key: 0 for key in ("symmetry", "trace", "divergence")}
        for field in (state.a, state.b):
            for start in (0, 9):
                values = constraints(field[start:start+9].astype(object).reshape(3, 3, -1), state.lattice)
                residual = {key: max(residual[key], values[key]) for key in residual}
        if any(residual.values()) and first_TT_failure is None:
            first_TT_failure = tick
        c, s = ((1, 0), (0, 1), (-1, 0), (0, -1))[tick % 4]
        if (np.any(state.b[18] != c) or np.any(state.b[19] != s)) and first_phase_change is None:
            first_phase_change = tick
        expected_F = np.roll(initial_F.reshape(4, 4, 4), -tick, axis=2).reshape(-1)
        if not np.array_equal(phase_readout(state), expected_F) and first_readout_shift_failure is None:
            first_readout_shift_failure = tick
        log, measured = official_quotients(engine, history[-2], state, tick)
        official.append([int(x) for x in measured[20]])
        rows.append({"tick": tick, "peak_counter": state.max_abs(),
                     "peak_counter_bits": state.max_abs().bit_length(),
                     "TT_residual": residual, "official_record_count": len(log),
                     "phase_quotient_nonzero_sites": int(np.count_nonzero(ell[18:20]))})
    assert engine.rewind(state, steps).same_as(seed)
    return {"initial_metric_wave": metric, "initial_matter": matter, "steps": steps,
            **history_fingerprints(history),
            "samples": rows, "first_raw_TT_failure": first_TT_failure,
            "first_phase_carrier_change": first_phase_change,
            "first_metric_shift_identity_failure": first_readout_shift_failure,
            "all_direct_input_oracles": True, "all_exact_divmod_ledgers": True,
            "every_step_inverse_and_full_rewind": True,
            "official_matter_quotients_by_tick_and_node": official}, history


def first_history_difference(left, right, selected):
    for tick, (a, b) in enumerate(zip(left, right)):
        if tick == 0:
            continue
        if any(not np.array_equal(getattr(a, field)[selected], getattr(b, field)[selected])
               for field in ("a", "b", "r")):
            return tick
    return None


def off_sector_audit(tensor, kappa=1):
    engine = Engine(tensor, tensor.Q)
    checks = []
    for scale in (1, 1 << 80):
        a = np.array([((i*7) % 13)-6 for i in range(tensor.G*27)], dtype=object).reshape(tensor.G, 27)*scale
        b = np.array([((i*11) % 17)-8 for i in range(tensor.G*27)], dtype=object).reshape(tensor.G, 27)*scale
        r = np.array([i % (6*tensor.Q) for i in range(tensor.G*27)], dtype=object).reshape(tensor.G, 27)
        seed = State(3, a, b, r)
        assert np.array_equal(engine.inputs(seed), edge_input_oracle(seed, tensor.Q, kappa))
        after, _ = checked_step(engine, seed)
        checks.append({"initial_scale": scale, "direct_input_oracle": True,
                       "exact_divmod_ledger_and_inverse": True,
                       "result_counter_bits": after.max_abs().bit_length(),
                       **history_fingerprints([seed, after])})
    return checks


def edge_controls(steps=5):
    tensor = build_edge_candidate(Q=1)
    joint, joint_history = run_edge_case(tensor, True, "pulse", steps)
    no_metric, no_metric_history = run_edge_case(tensor, False, "pulse", steps)
    no_matter, no_matter_history = run_edge_case(tensor, True, "none", steps)
    checker, checker_history = run_edge_case(tensor, True, "checkerboard", steps)
    geometry_changes_matter = first_history_difference(joint_history, no_metric_history, slice(20, 21))
    matter_changes_geometry = first_history_difference(joint_history, no_matter_history, slice(0, 20))
    assert geometry_changes_matter is not None and matter_changes_geometry is not None
    assert joint["first_raw_TT_failure"] is not None
    assert checker["first_raw_TT_failure"] is None
    assert checker["first_phase_carrier_change"] is not None
    return {"tensor": audit_tensor(tensor), "generic_off_sector_checks": off_sector_audit(tensor),
            "potential_interaction":
            "kappa sum_positive_xy_edges sigma_i (F_x+F_y)(chi_y-chi_x)^2; kappa=1",
            "F": "c(E00-E11)+s(B01+B10)",
            "geometry_to_matter_first_complete_state_change": geometry_changes_matter,
            "matter_to_geometry_first_complete_state_change": matter_changes_geometry,
            "controls_change_initial_data_only": True,
            "joint": joint, "metric_absent_initially": no_metric,
            "matter_absent_initially": no_matter, "planar_checkerboard": checker,
            "checkerboard_invariant_sector":
            "Even L; chi=(-1)^x psi(z), metric and phase fields z-only, "
            "E00=-E11 and B01=B10, all other metric counters zero; equal or "
            "complementary carries match these signed equalities. H=8 psi(z)^2. "
            "Integer divmod preserves all signed equalities with their carries.",
            "limitations": ["Generic transverse matter breaks the raw TT divergence constraint.",
              "Reciprocal phase sources invalidate the free phase carrier and metric translation proof.",
              "Checkerboard preservation is an algebraic TT invariant sector, not Einstein constraint propagation.",
              "A nonzero matter energy source cannot satisfy the old vacuum TT Hamiltonian constraint merely because raw TT survives.",
              "The direct candidate has rapid growth in these finite runs; reversibility does not supply boundedness.",
              "No common characteristic metric, nonlinear Einstein equation, or universal matter coupling is established."]}


def build_oscillator():
    potential = [(2, (("e", ZERO), ("e", ZERO))),
                 (2, (("chi", ZERO), ("chi", ZERO))),
                 (-1, (("e", ZERO), ("e", ZERO), ("chi", ZERO), ("chi", ZERO)))]
    terms = []
    for coefficient, variables in potential:
        terms.extend(derivative_terms(coefficient, variables))
    return Tensor(["e", "chi"], terms, Q=1, strict_support=True)


def oscillator_controls():
    tensor = build_oscillator()
    engine = Engine(tensor, 1)
    def prepare(e, chi):
        return State(3, [[e]*27, [chi]*27], [[e]*27, [chi]*27], [[0]*27, [0]*27])
    def run(seed, steps):
        state = seed
        history = [seed]
        rows = []
        period = None
        for tick in range(1, steps+1):
            e, chi = [int(row[0]) for row in state.b]
            assert np.array_equal(engine.inputs(state),
                                  [[4*e-2*e*chi**2]*27, [4*chi-2*e**2*chi]*27])
            state, ell = checked_step(engine, state)
            history.append(state)
            log, measured = official_quotients(engine, history[-2], state, tick)
            rows.append({"tick": tick, "a": [int(v) for v in state.a[:, 0]],
                         "b": [int(v) for v in state.b[:, 0]],
                         "r": [int(v) for v in state.r[:, 0]],
                         "raw_signed_quotients": [int(v) for v in ell[:, 0]],
                         "official_signed_quotients": [int(v) for v in measured[:, 0]],
                         "official_record_count": len(log),
                         "chosen_positive_gamma": 1+int(state.b[0, 0])**2})
            if period is None and state.same_as(seed):
                period = tick
        assert engine.rewind(state, steps).same_as(seed)
        return {"steps": steps, "first_complete_state_return": period, "samples": rows,
                **history_fingerprints(history),
                "all_input_oracles_and_divmod_ledgers": True,
                "every_step_inverse_and_full_rewind": True}, history
    joint, joint_history = run(prepare(-1, -1), 15)
    no_matter, no_matter_history = run(prepare(-1, 0), 5)
    no_geometry, no_geometry_history = run(prepare(0, -1), 5)
    assert joint["first_complete_state_return"] == 5
    assert all(abs(v) <= 1 for row in joint["samples"] for key in ("a", "b") for v in row[key])
    assert all(row["chosen_positive_gamma"] in (1, 2) for row in joint["samples"])
    assert any(v for row in joint["samples"] for v in row["official_signed_quotients"])
    matter_changes_geometry = first_history_difference(joint_history, no_matter_history, slice(0, 1))
    geometry_changes_matter = first_history_difference(joint_history, no_geometry_history, slice(1, 2))
    assert matter_changes_geometry is not None and geometry_changes_matter is not None
    return {"tensor": audit_tensor(tensor), "potential": "2(e^2+chi^2)-e^2 chi^2",
            "inputs": ["u_e=4e-2e chi^2", "u_chi=4chi-2e^2 chi"],
            "fundamental_state_and_coefficients": "Integers only; Q=1; D=6; no external clock or intervention.",
            "prepared_joint_state": {"a": [-1, -1], "b": [-1, -1], "r": [0, 0]},
            "joint": joint, "matter_absent_initially": no_matter,
            "geometry_absent_initially": no_geometry,
            "matter_to_geometry_first_complete_state_change": matter_changes_geometry,
            "geometry_to_matter_first_complete_state_change": geometry_changes_matter,
            "controls_change_initial_data_only": True,
            "exact_all_time_bound": "The complete state returns after five steps. Determinism proves repetition forever; |a|,|b|<=1 and gamma=1+e^2 in {1,2} on this orbit.",
            "limitations": ["This is a reciprocal nonlinear oscillator, not a gravity solution.",
              "Gamma is a chosen positive local polynomial readout, not an operationally derived metric.",
              "The finite periodic orbit does not prove a stable open neighborhood or generic boundedness.",
              "No spatial propagation, Einstein constraints, geodesics, or common characteristic cone are present."]}


def build_positive_stiffness_candidate():
    """Integer Phi=sum(3e^2+7chi^2)-sum_edges(1+ex^2+ey^2)(chiy-chix)^2."""
    terms = []
    for name, coefficient in (("e", 3), ("chi", 7)):
        terms.extend(derivative_terms(coefficient, ((name, ZERO), (name, ZERO))))
    for axis in range(3):
        edge = tuple(1 if i == axis else 0 for i in range(3))
        for left, right, coefficient in ((edge, edge, 1), (ZERO, ZERO, 1),
                                          (edge, ZERO, -2)):
            difference = (("chi", left), ("chi", right))
            terms.extend(derivative_terms(-coefficient, difference))
            for endpoint in (ZERO, edge):
                variables = (("e", endpoint), ("e", endpoint))+difference
                terms.extend(derivative_terms(-coefficient, variables))
    return Tensor(["e", "chi"], terms, Q=1, strict_support=True)


def positive_stiffness_input_oracle(state):
    b = state.b.astype(object)
    u = np.array([6*b[0], 14*b[1]], dtype=object)
    for axis in range(3):
        for sign in (-1, 1):
            offset = tuple(sign if i == axis else 0 for i in range(3))
            neighbor = state.lattice.shift_index(offset)
            change = b[1, neighbor]-b[1]
            u[0] -= 2*b[0]*change**2
            u[1] += 2*(1+b[0]**2+b[0, neighbor]**2)*change
    return u


def positive_stiffness_controls():
    tensor = build_positive_stiffness_candidate()
    engine = Engine(tensor, 1)
    lat = lattice(4)
    x = np.array([lat.coords(i)[0] for i in range(lat.N)], dtype=int)
    profile = np.array([1, 0, -1, 0], dtype=object)[x]
    def prepare(geometry, matter):
        a = np.zeros((2, lat.N), dtype=object)
        a[0] = -int(geometry)
        a[1] = -profile if matter else 0
        r = np.zeros_like(a)
        r[1, profile == -1] = 5
        return State(4, a, a.copy(), r)
    def one(geometry, matter, steps):
        seed = prepare(geometry, matter)
        state = seed
        history = [seed]
        rows = []
        period = None
        for tick in range(1, steps+1):
            assert np.array_equal(engine.inputs(state), positive_stiffness_input_oracle(state))
            after, ell = checked_step(engine, state)
            log, measured = official_quotients(engine, state, after, tick)
            history.append(after)
            state = after
            stiffnesses = []
            for axis in range(3):
                offset = tuple(1 if i == axis else 0 for i in range(3))
                neighbor = lat.shift_index(offset)
                e = state.b[0].astype(object)
                stiffnesses.extend(int(value) for value in 1+e**2+e[neighbor]**2)
            assert min(stiffnesses) >= 1
            if geometry and matter:
                for field in (state.a, state.b):
                    q = int(field[0, 0])
                    assert abs(q) <= 1
                    assert np.all(field[0] == q)
                    assert np.array_equal(field[1], q*profile)
                assert np.all(state.r[0] == state.r[0, 0])
                assert np.all(state.r[1, profile == 1] == state.r[0, 0])
                assert np.all(state.r[1, profile == -1] == 5-state.r[0, 0])
                assert np.all(state.r[1, profile == 0] == 0)
            rows.append({"tick": tick, "peak_counter": state.max_abs(),
                         "e_a_b_r_at_origin": [int(state.a[0, 0]), int(state.b[0, 0]), int(state.r[0, 0])],
                         "raw_signed_quotients_at_origin": [int(value) for value in ell[:, 0]],
                         "official_signed_quotients_at_origin": [int(value) for value in measured[:, 0]],
                         "official_signed_quotients_by_gear_node": [[int(value) for value in row] for row in measured],
                         "official_record_count": len(log),
                         "minimum_positive_link_stiffness": min(stiffnesses),
                         "maximum_positive_link_stiffness": max(stiffnesses)})
            if period is None and state.same_as(seed):
                period = tick
        assert engine.rewind(state, steps).same_as(seed)
        return {"steps": steps, "initial_geometry_present": geometry,
                "initial_matter_present": matter, "first_complete_state_return": period,
                "samples": rows, "official_record_count": sum(row["official_record_count"] for row in rows),
                "every_step_input_oracle_divmod_ledger_inverse": True,
                "complete_rewind": True, **history_fingerprints(history)}, history
    joint, joint_history = one(True, True, 15)
    no_matter, no_matter_history = one(True, False, 5)
    no_geometry, no_geometry_history = one(False, True, 5)
    assert joint["first_complete_state_return"] == 5
    assert max(row["peak_counter"] for row in joint["samples"]) == 1
    assert {row["minimum_positive_link_stiffness"] for row in joint["samples"]} == {1, 3}
    matter_changes_geometry = first_history_difference(joint_history, no_matter_history, slice(0, 1))
    geometry_changes_matter = first_history_difference(joint_history, no_geometry_history, slice(1, 2))
    assert matter_changes_geometry == 1 and geometry_changes_matter == 1
    for index, control in ((0, no_matter), (1, no_geometry)):
        assert joint["samples"][0]["official_signed_quotients_at_origin"][index] != control["samples"][0]["official_signed_quotients_at_origin"][index]
    generic_checks = []
    for scale in (1, 1 << 80):
        a = np.array([i % 5-2 for i in range(54)], dtype=object).reshape(2, 27)*scale
        b = np.array([(i*7) % 13-6 for i in range(54)], dtype=object).reshape(2, 27)*scale
        r = np.array([i % 6 for i in range(54)], dtype=object).reshape(2, 27)
        seed = State(3, a, b, r)
        assert np.array_equal(engine.inputs(seed), positive_stiffness_input_oracle(seed))
        after, _ = checked_step(engine, seed)
        generic_checks.append({"initial_scale": scale, "input_oracle_divmod_ledger_inverse": True,
                               "result_counter_bits": after.max_abs().bit_length(),
                               **history_fingerprints([seed, after])})
    # An exact carrying counterexample to global boundedness, fixed before run.
    unstable_seed = State(3, [[0]*27, [1]*27], [[0]*27, [1]*27], [[0]*27, [0]*27])
    unstable = unstable_seed
    unstable_history = [unstable]
    unstable_samples = []
    for tick in range(1, 7):
        previous = unstable
        assert np.array_equal(engine.inputs(previous), positive_stiffness_input_oracle(previous))
        unstable, _ = checked_step(engine, previous)
        assert np.all(unstable.a[0] == 0) and np.all(unstable.b[0] == 0)
        assert int(unstable.b[1, 0]) >= 3*int(previous.b[1, 0])
        unstable_history.append(unstable)
        unstable_samples.append({"tick": tick, "a_chi": int(unstable.a[1, 0]),
                                 "b_chi": int(unstable.b[1, 0]), "r_chi": int(unstable.r[1, 0])})
    assert engine.rewind(unstable, 6).same_as(unstable_seed)
    return {"tensor": audit_tensor(tensor),
            "potential": "sum_nodes(3 e^2+7 chi^2)-sum_positive_face_edges(1+e_x^2+e_y^2)(chi_y-chi_x)^2",
            "inputs": ["u_e=6e-2e sum_neighbors(chi_y-chi)^2",
                       "u_chi=14chi+2 sum_neighbors(1+e^2+e_y^2)(chi_y-chi)"],
            "prepared_state": {"L": 4, "x_profile_f": [1, 0, -1, 0],
                               "a_e": -1, "b_e": -1, "r_e": 0,
                               "a_chi": "-f(x)", "b_chi": "-f(x)",
                               "r_chi": "5 where f=-1; 0 otherwise"},
            "proof": ["For chi=q f(x), sum_neighbors(chi_y-chi)^2=2q^2 at every node, including nodes with f=0.",
                      "The nearest-neighbor Laplacian of f is -2f. Uniform e=q therefore gives u_e=6q-4q^3 and u_chi=(10-8q^2)q f.",
                      "On q in {-1,0,1}, both inputs equal 2q times their respective profile (1 or f).",
                      "The exact q retained triples cycle (-1,-1,0),(-1,0,2),(0,1,2),(1,1,0),(1,-1,4), then return.",
                      "At f=-1 the complete scalar triple is the signed reflection of q with remainder 5-r; divmod(-2u+5-r,6)=(-ell,5-r_next). At f=0 both counters and the remainder remain zero.",
                      "Thus the complete lattice state returns after five updates; determinism gives the same orbit for all future time and exact inversion gives all past time. All |a| and |b| are at most one.",
                      "The chosen link coefficient K_xy=1+e_x^2+e_y^2 is always a positive integer for arbitrary integer states, and equals one or three on this orbit."],
            "joint": joint, "matter_absent_initially": no_matter,
            "geometry_absent_initially": no_geometry,
            "matter_to_geometry_first_complete_state_change": matter_changes_geometry,
            "geometry_to_matter_first_complete_state_change": geometry_changes_matter,
            "both_directions_change_actual_official_origin_records_at_step": 1,
            "controls_change_initial_data_only": True,
            "generic_off_sector_checks": generic_checks,
            "exact_unbounded_control": {
                "initial_data": "L=3; e has a=b=r=0; chi has a=b=1,r=0 uniformly",
                "samples": unstable_samples, "every_step_input_oracle_ledger_inverse": True,
                "complete_rewind": True, **history_fingerprints(unstable_history),
                "proof": "Uniform chi has zero edge gradients and e remains zero, so u_chi=14b. If b>=a>=1 then ell=floor((28b+r)/6)>=4b for every 0<=r<6, hence b_next=ell-a>=3b. Induction proves unbounded growth of this integer carrying orbit."},
            "limitations": ["Positive K is a chosen scalar link stiffness, not a derived metric or coframe satisfying Einstein equations.",
              "The exact bounded construction is a prepared standing pattern; no travelling packet, calibrated clock, geodesic, or arrival-time experiment is established.",
              "An isolated periodic orbit is not a stable open neighborhood; the same tensor has an exactly proved exponentially growing integer carrying orbit, recorded in exact_unbounded_control.",
              "No Einstein Hamiltonian or momentum constraint, source conservation identity, common characteristic metric, or universal matter coupling has been proved."]}


def run(steps=5):
    if type(steps) is not int or not 2 <= steps <= 6:
        raise ValueError("Use 2..6 fixed steps for this rapidly growing edge candidate")
    return {"scope": "Exact reciprocal constructions and explicit unclosed gravitational requirements",
            "default_engine_tensor_seed_changed": False,
            "one_common_Q_per_run": True, "all_fundamental_values_integer": True,
            "edge_candidate": edge_controls(steps), "bounded_Q1_oscillator": oscillator_controls(),
            "bounded_Q1_positive_stiffness_links": positive_stiffness_controls()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=5)
    parser.add_argument("--out", type=Path,
                        default=Path("runs/reciprocal-geometry/reciprocal_metric_candidate.json"))
    args = parser.parse_args()
    result = run(args.steps)
    result["implementation_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"output": str(args.out),
                      "edge_tensor": result["edge_candidate"]["tensor"],
                      "edge_TT_first_failure": result["edge_candidate"]["joint"]["first_raw_TT_failure"],
                      "checkerboard_TT_first_failure": result["edge_candidate"]["planar_checkerboard"]["first_raw_TT_failure"],
                      "oscillator_period": result["bounded_Q1_oscillator"]["joint"]["first_complete_state_return"],
                      "positive_stiffness_link_period": result["bounded_Q1_positive_stiffness_links"]["joint"]["first_complete_state_return"]}, indent=2))
