"""Exact finite Z2 connection exchange through the unchanged Rule3 Engine.

This is a ten-channel, period-three proof control, not Maxwell or QED.  For
each positive face k the first-order sign-domain map is

    chi_k' = eta_k; eta_k' = U_k * ref_neighbor;
    U_k' = chi_k * ref_neighbor; ref' = ref.

It cycles three gauge-covariant registers.  The reference sign is stationary;
there is no electric field, Gauss constraint, energy/stress interpretation or
propagating photon claim.  Embedding u=3*(F+F^-1), a=F^-1(b), and legal carries
gives the exact first-order map without a callback or discarded history.
"""
from __future__ import annotations

import itertools
import random

import numpy as np

from validation.padding import sector_state
from universe24.core import Engine, GearType, State, Tensor, lattice

ZERO = (0, 0, 0)
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
NAMES = ("dynamic.ref", "dynamic.chi_x", "dynamic.eta_x", "dynamic.U_x",
         "dynamic.chi_y", "dynamic.eta_y", "dynamic.U_y",
         "dynamic.chi_z", "dynamic.eta_z", "dynamic.U_z")
REF = 0
CHI = (1, 4, 7)
ETA = (2, 5, 8)
LINKS = (3, 6, 9)


def build_tensor():
    """One immutable ten-channel, degree-two, strict-face law."""
    gears = [GearType(name, "audit", LINKS.index(i) if i in LINKS else None)
             for i, name in enumerate(NAMES)]
    terms = [(REF, 6, [(REF, ZERO, "b")])]
    for axis, (chi, eta, link) in enumerate(zip(CHI, ETA, LINKS)):
        neighbor = (REF, AXES[axis], "b")
        terms.extend([
            (chi, 3, [(eta, ZERO, "b")]),
            (chi, 3, [(link, ZERO, "b"), neighbor]),
            (eta, 3, [(chi, ZERO, "b")]),
            (eta, 3, [(link, ZERO, "b"), neighbor]),
            (link, 3, [(chi, ZERO, "b"), neighbor]),
            (link, 3, [(eta, ZERO, "b"), neighbor]),
        ])
    return Tensor(gears, terms, strict_support=True)


def _sign_array(values, shape, label):
    arr = np.asarray(values, dtype=object)
    if arr.shape != shape or any(isinstance(v, (bool, np.bool_)) or
                                not isinstance(v, (int, np.integer)) or
                                int(v) not in (-1, 1) for v in arr.flat):
        raise ValueError(f"{label} must contain exact signs with shape {shape}")
    return arr.copy()


def flow(values, L, inverse=False):
    """Independent direct first-order oracle on the complete sign domain."""
    grid = lattice(L)
    current = _sign_array(values, (len(NAMES), grid.N), "current")
    after = current.copy()
    for axis, (chi, eta, link) in enumerate(zip(CHI, ETA, LINKS)):
        remote = current[REF, grid.shift_index(AXES[axis])]
        if inverse:
            after[chi] = current[link] * remote
            after[eta] = current[chi]
            after[link] = current[eta] * remote
        else:
            after[chi] = current[eta]
            after[eta] = current[link] * remote
            after[link] = current[chi] * remote
    return after


def inverse_flow(values, L):
    return flow(values, L, inverse=True)


def prepare_state(current, L, remainders=None):
    b = _sign_array(current, (len(NAMES), lattice(L).N), "current")
    if remainders is None:
        remainders = [[(g+n) % 6 for n in range(L**3)] for g in range(len(NAMES))]
    r = np.asarray(remainders, dtype=object)
    if r.shape != b.shape or any(isinstance(v, (bool, np.bool_)) or
                                not isinstance(v, (int, np.integer)) or
                                not 0 <= int(v) < 6 for v in r.flat):
        raise ValueError("every retained remainder must be an exact integer in 0..5")
    return State(L, inverse_flow(b, L), b, r)


def prepare_fixture(L=3, seed=16427):
    rng = random.Random(seed)
    current = [[rng.choice((-1, 1)) for _ in range(L**3)] for _ in NAMES]
    return prepare_state(current, L)


def _checked_complete_banks(state):
    """Validate even a State whose mutable arrays were altered after creation."""
    if not isinstance(state, State):
        raise ValueError("provide a complete State")
    state = sector_state(state, len(NAMES))
    grid = lattice(state.L)
    shape = (len(NAMES), grid.N)
    banks = []
    for field in ("a", "b", "r"):
        values = np.asarray(getattr(state, field), dtype=object)
        if values.shape != shape or any(isinstance(v, (bool, np.bool_)) or
                                      not isinstance(v, (int, np.integer))
                                      for v in values.flat):
            raise ValueError(f"complete {field} bank must contain exact integers with shape {shape}")
        if field == "r" and any(not 0 <= int(v) < 6 for v in values.flat):
            raise ValueError("complete remainder bank must stay in 0..5")
        banks.append(values.copy())
    return tuple(banks)


def validate_prepared_domain(state):
    """Reject incomplete/forged histories; certify precisely the sign sector.

    The period-three and normalized-link theorem requires both complete sign
    histories, a=F^-1(b), and each legal retained carry.  Matching b alone is
    insufficient.  This check is passive and never repairs a seed or run.
    """
    a, b, _ = _checked_complete_banks(state)
    _sign_array(a, a.shape, "old history")
    _sign_array(b, b.shape, "current history")
    if not np.array_equal(a, inverse_flow(b, state.L)):
        raise ValueError("complete history violates a=F^-1(b)")
    return True


def gauge_transform(state, node_signs):
    """Time-independent local Z2 on ALL histories and carries, not just b."""
    old_a, old_b, old_r = _checked_complete_banks(state)
    signs = _sign_array(node_signs, (state.N,), "node gauge")
    characters = np.array([signs.copy() for _ in NAMES], dtype=object)
    for axis, link in enumerate(LINKS):
        characters[link] = signs * signs[state.lattice.shift_index(AXES[axis])]
    a = characters * old_a
    b = characters * old_b
    r = np.where(characters == 1, old_r, 5-old_r).astype(object)
    return State(state.L, a, b, r)


def wilson_plaquettes(state):
    """Passive Z2 plaquettes, rejecting non-sign links and malformed banks.

    Complete prepared-history membership is not needed for this one-snapshot
    observable, but each current link must be a unit sign so its inverse is
    itself.  General integer link products are not interpreted as holonomy.
    """
    _, current, _ = _checked_complete_banks(state)
    _sign_array(current[list(LINKS)], (3, state.N), "current Z2 links")
    result = {}
    for i, j in itertools.combinations(range(3), 2):
        ui, uj = current[LINKS[i]], current[LINKS[j]]
        values = ui * uj[state.lattice.shift_index(AXES[i])] * \
            ui[state.lattice.shift_index(AXES[j])] * uj
        result[f"{i}{j}"] = [int(x) for x in values]
    return result


def _frozen_link_control_tensor():
    """A declared different law used only to disconnect link response."""
    tensor = build_tensor()
    terms = [m for m in tensor.monomials if m.target not in LINKS]
    terms.extend((link, 6, [(link, ZERO, "b")]) for link in LINKS)
    return Tensor(tensor.gears, terms, strict_support=True)


def _feedback_controls():
    # The two prepared seeds differ only in complete matter registers.  All
    # link a,b,r and all reference registers agree before the intervention.
    L = 3
    current = np.ones((len(NAMES), L**3), dtype=object)
    changed = current.copy()
    changed[CHI[0], 0] = -1
    left, right = prepare_state(current, L), prepare_state(changed, L)
    for field in ("a", "b", "r"):
        assert np.array_equal(getattr(left, field)[list(LINKS)],
                              getattr(right, field)[list(LINKS)])
        assert np.array_equal(getattr(left, field)[REF], getattr(right, field)[REF])
    engine = Engine(build_tensor())
    first_left, first_right = engine.step(left), engine.step(right)
    assert first_left.b[LINKS[0], 0] != first_right.b[LINKS[0], 0]
    assert wilson_plaquettes(first_left) != wilson_plaquettes(first_right)
    second_left, second_right = engine.step(first_left), engine.step(first_right)
    assert second_left.b[ETA[0], 0] != second_right.b[ETA[0], 0]

    # Freeze the links under a separately identified negative-control tensor,
    # starting from the EXACT same changed seed.  The future eta response
    # disappears.  This control law is not claimed to preserve the native
    # prepared sign sector in general.
    frozen_tensor = _frozen_link_control_tensor()
    frozen_engine = Engine(frozen_tensor)
    frozen_first = frozen_engine.step(right)
    frozen_second = frozen_engine.step(frozen_first)
    assert frozen_first.b[LINKS[0], 0] == 1
    assert frozen_second.b[ETA[0], 0] == second_left.b[ETA[0], 0]
    assert frozen_engine.rewind(frozen_second, 2).same_as(right)

    # Direct complete-state intervention: change one link b, preserve ALL
    # matter a,b,r.  This is deliberately off the first-order prepared sector;
    # it tests the Engine dependency, not unit-link preservation there.
    direct = left.copy()
    direct.b[LINKS[0], 0] = -1
    direct_after = engine.step(direct)
    assert direct_after.b[ETA[0], 0] != first_left.b[ETA[0], 0]
    assert engine.inverse_step(direct_after).same_as(direct)
    return {
        "equal_complete_initial_links": True,
        "matter_changes_link_at_step": 1,
        "changed_link_changes_matter_at_step": 2,
        "matter_changes_gauge_invariant_plaquettes": True,
        "frozen_link_removes_delayed_response": True,
        "frozen_link_control_tensor": frozen_tensor.fingerprint,
        "direct_link_only_full_state_intervention": True,
        "direct_link_intervention_domain": "off prepared sign-history sector; dependency and inverse only",
        "frozen_control_domain": "separate tensor; no general sign-sector claim",
    }


def dynamic_audit():
    """Exact checks with explicit physical and finite-period limitations."""
    tensor = build_tensor()
    engine = Engine(tensor)
    rng = random.Random(439817)
    runs = []
    covariance_cases = transitions = changed_plaquettes = 0
    # A local truth-table proof of F^-1 and F^3 uses all sixteen edge states.
    local_cases = 0
    for ref, chi, eta, link in itertools.product((-1, 1), repeat=4):
        start = (chi, eta, link)
        result = start
        for _ in range(3):
            x, y, u = result
            result = (y, u*ref, x*ref)
        assert result == start
        following = (eta, link*ref, chi*ref)
        x, y, u = following
        assert (u*ref, x, y*ref) == start
        local_cases += 1
    for L in (3, 4, 5):
        for trial in range(4):
            seed = prepare_fixture(L, 8100+10*L+trial)
            validate_prepared_domain(seed)
            state = seed
            initial_wilson = wilson_plaquettes(state)
            for step in range(1, 10):
                gauge = [rng.choice((-1, 1)) for _ in range(state.N)]
                transformed = gauge_transform(state, gauge)
                assert wilson_plaquettes(transformed) == wilson_plaquettes(state)
                after = engine.step(state)
                validate_prepared_domain(after)
                assert np.array_equal(after.b, flow(state.b, L))
                assert np.array_equal(after.a, state.b)
                assert np.array_equal(after.r, state.r)
                assert all(int(v) in (-1, 1) for values in (after.a, after.b)
                           for v in values.flat)
                assert engine.inverse_step(after).same_as(state)
                assert engine.step(transformed).same_as(gauge_transform(after, gauge))
                covariance_cases += 1
                transitions += 1
                changed_plaquettes += sum(a != b for key in initial_wilson
                    for a, b in zip(initial_wilson[key], wilson_plaquettes(after)[key]))
                if step % 3 == 0:
                    assert after.same_as(seed)
                state = after
            assert engine.rewind(state, 9).same_as(seed)
            runs.append({"side": L, "seed": 8100+10*L+trial, "steps": 9,
                         "complete_period_divides": 3, "full_rewind": True})
    assert changed_plaquettes > 0
    # Full-state covariance is stronger than the finite sign-domain theorem.
    # Test arbitrary signed large integers, all legal carries and full inverse.
    for trial in range(12):
        L = 3
        banks = [np.array([[rng.randrange(-17, 18) for _ in range(L**3)]
                           for _ in NAMES], dtype=object) for _ in range(2)]
        banks[0][0, 0] = (1 << 170)+trial
        banks[1][3, 1] = -(1 << 151)-trial
        r = np.array([[(n+g+trial) % 6 for n in range(L**3)] for g in range(len(NAMES))], dtype=object)
        state = State(L, banks[0], banks[1], r)
        gauge = [rng.choice((-1, 1)) for _ in range(state.N)]
        after = engine.step(state)
        assert engine.step(gauge_transform(state, gauge)).same_as(gauge_transform(after, gauge))
        assert engine.inverse_step(after).same_as(state)
        covariance_cases += 1
    return {
        "schema": "universe24/dynamic-z2-gauge-control/1",
        "tensor_sha256": tensor.fingerprint,
        "channels": len(NAMES), "integer_registers_per_node": 3*len(NAMES),
        "maximum_degree": max(m.degree for m in tensor.monomials),
        "strict_physical_face_support": not tensor.support_violations(),
        "local_truth_table_cases": local_cases,
        "prepared_engine_transitions": transitions,
        "full_state_gauge_covariance_cases": covariance_cases,
        "changed_plaquette_comparisons_to_initial": changed_plaquettes,
        "runs": runs,
        "all_six_remainders_retained": True,
        "maximum_retained_bits_on_prepared_domain": 3,
        "link_norm_exact_on_prepared_domain": True,
        "complete_history_relation": "a=F^-1(b), b in {-1,+1}^10, every r in 0..5",
        "complete_period_divides": 3,
        "gauge_group": "local time-independent Z2; all histories and carries transform",
        "feedback": _feedback_controls(),
        "scope": {
            "independent_group_valued_dynamic_links": "proved on declared prepared sign domain",
            "matter_link_feedback": "proved with complete-history and frozen-link controls",
            "physical_gauge_symmetry": "finite Z2 mathematical covariance only",
            "continuous_U1": "not established",
            "electric_field_and_Gauss_law": "not implemented",
            "Maxwell_or_propagating_photon": "not established",
            "energy_stress_and_gravity": "not established",
            "stationary_reference": "retained charged reference sign; not a physical dynamical apparatus",
            "spatial_transport": "not implemented; evolving information cycles inside each edge triplet",
            "sustained_complexity_growth": "excluded on this period-three domain",
        },
    }
