"""Source-only coupling/clock/geometry controls, not an accepted physical model.

One face potential generates both endpoint responses and the link response.
Its reciprocal polynomial symmetry is not a theorem of integer-state energy
conservation, proper-clock behavior, synchronization, or Einstein dynamics.
The kinematic controls show that a phase covector or causal cone alone does
not determine elapsed proper time or spacetime curvature.
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor, check_reciprocity


def build_reciprocal_edge(axis: int = 0) -> Tensor:
    """Return the 3-channel, 14-term gradient of one translated face potential.

    With y=x+e_axis, Phi_e=-h_e**2*((X_y-X_x)**2+(Y_y-Y_x)**2)/2.
    X,Y are node values and h is a link value stored at its base endpoint.
    ``axis`` must be a Python int in 0..2; no inexact coercion is performed.
    This is a coupling example, not an allocation within the common45 law.
    """
    if type(axis) is not int:
        raise TypeError("axis must be a Python int")
    if not 0 <= axis < 3:
        raise ValueError("axis must be 0, 1 or 2")
    zero = (0, 0, 0)
    edge = tuple(int(i == axis) for i in range(3))
    reverse = tuple(-v for v in edge)

    def factor(gear, offset=zero):
        return (gear, offset, "b")

    terms = []
    for field in ("X", "Y"):
        terms.extend([
            (field, 1, [factor("h"), factor("h"), factor(field, edge)]),
            (field, -1, [factor("h"), factor("h"), factor(field)]),
            (field, 1, [factor("h", reverse), factor("h", reverse), factor(field, reverse)]),
            (field, -1, [factor("h", reverse), factor("h", reverse), factor(field)]),
            ("h", -1, [factor("h"), factor(field, edge), factor(field, edge)]),
            ("h", 2, [factor("h"), factor(field, edge), factor(field)]),
            ("h", -1, [factor("h"), factor(field), factor(field)]),
        ])
    return Tensor([GearType("X", label="audit"), GearType("Y", label="audit"),
                   GearType("h", label="audit", link=axis)], terms, strict_support=True)


def _require(condition, message):
    if not condition:
        raise AssertionError(message)


def _potential_checks():
    left_x, left_y, right_x, right_y, weight = sp.symbols("lx ly rx ry h", real=True)
    delta_x, delta_y = right_x-left_x, right_y-left_y
    potential = -weight**2*(delta_x**2+delta_y**2)/2
    variables = (left_x, left_y, right_x, right_y, weight)
    expected = (weight**2*delta_x, weight**2*delta_y,
                -weight**2*delta_x, -weight**2*delta_y,
                -weight*(delta_x**2+delta_y**2))
    for variable, response in zip(variables, expected):
        _require(sp.expand(sp.diff(potential, variable)-response) == 0,
                 "independent potential derivative failed")
    rotation = (left_x*sp.diff(potential, left_y)-left_y*sp.diff(potential, left_x)
                + right_x*sp.diff(potential, right_y)-right_y*sp.diff(potential, right_x))
    _require(sp.expand(rotation) == 0, "polynomial common-rotation identity failed")
    return {"gradient_identity": True, "polynomial_common_rotation_identity": True,
            "continuous_rotation_is_generic_integer_state_symmetry": False,
            "discrete_energy_conservation_proved": False}


def _scalar_inputs(state, axis):
    """Independent edge-force oracle with explicit periodic coordinate indexing."""
    side = state.L
    old = state.b
    result = np.zeros(old.shape, dtype=object)
    for x in range(side):
        for y in range(side):
            for z in range(side):
                coords = [x, y, z]
                here = (x*side+y)*side+z
                ahead, behind = coords.copy(), coords.copy()
                ahead[axis] = (ahead[axis]+1) % side
                behind[axis] = (behind[axis]-1) % side
                nxt = (ahead[0]*side+ahead[1])*side+ahead[2]
                prev = (behind[0]*side+behind[1])*side+behind[2]
                weight, previous_weight = int(old[2, here]), int(old[2, prev])
                for field in (0, 1):
                    jump = int(old[field, nxt])-int(old[field, here])
                    previous_jump = int(old[field, prev])-int(old[field, here])
                    result[field, here] = weight**2*jump+previous_weight**2*previous_jump
                    result[2, here] -= weight*jump**2
    return result


def _edge_run(axis):
    tensor = build_reciprocal_edge(axis)
    _require(check_reciprocity(tensor).ok, "edge reciprocity failed")
    without_reaction = Tensor(tensor.gears, [m for m in tensor.monomials if m.target != 2],
                              strict_support=True)
    _require(not check_reciprocity(without_reaction).ok,
             "deleted-reaction control did not reject reciprocity")
    rng = np.random.default_rng(71625)
    shape = (3, 27)
    seed = State(3, rng.integers(-1, 2, size=shape), rng.integers(-1, 2, size=shape),
                 np.arange(81).reshape(shape) % 6)
    carries = sorted(set(int(v) for v in seed.r.flat))
    _require(carries == list(range(6)), "all six legal carries must be present")
    engine, state = Engine(tensor), seed.copy()
    comparisons, changed_carries, bit_lengths = 0, 0, []
    for _ in range(5):
        inputs = _scalar_inputs(state, axis)
        _require(np.array_equal(inputs, engine.inputs(state)), "edge force oracle mismatch")
        quotient, remainder = np.empty(shape, dtype=object), np.empty(shape, dtype=object)
        for index in np.ndindex(shape):
            quotient[index], remainder[index] = divmod(2*int(inputs[index])+int(state.r[index]), 6)
        oracle = State(3, state.b.copy(), quotient-state.a, remainder)
        nxt = engine.step(state)
        _require(nxt.same_as(oracle), "scalar retained-state oracle mismatch")
        _require(engine.inverse_step(nxt).same_as(state), "one-step rewind mismatch")
        changed_carries += int(np.count_nonzero(nxt.r != state.r))
        comparisons += 3*nxt.G*nxt.N
        bit_lengths.append(max(abs(int(v)).bit_length()
                               for values in (nxt.a, nxt.b, nxt.r) for v in values.flat))
        state = nxt
    _require(changed_carries > 0, "carry control did not exercise remainder changes")
    _require(engine.rewind(state, 5).same_as(seed), "complete rewind mismatch")
    return {"axis": axis, "channels": tensor.G, "retained_integers_per_node": 3*tensor.G,
            "monomials": len(tensor.monomials), "degree": max(m.degree for m in tensor.monomials),
            "tensor_sha256": tensor.fingerprint, "strict_support": not tensor.support_violations(),
            "reciprocity": True, "deleted_reaction_rejected": True,
            "steps": 5, "nodes": seed.N, "initial_carries": carries,
            "scalar_register_comparisons": comparisons, "changed_remainder_entries": changed_carries,
            "max_bits_per_step": bit_lengths, "full_rewind": True}


def _clock_controls():
    zero, edge, reverse = (0, 0, 0), (1, 0, 0), (-1, 0, 0)
    oscillator = Tensor([GearType("oscillator", label="audit")],
                        [(0, 3, [(0, zero, "b")])], strict_support=True)
    engine = Engine(oscillator)
    seed = State(3, np.zeros((1, 27), dtype=int), np.ones((1, 27), dtype=int),
                 np.arange(27).reshape(1, 27) % 6)
    state, first_return, b_values = seed.copy(), None, [1]
    for tick in range(1, 7):
        state = engine.step(state)
        b_values.append(int(state.b[0, 0]))
        _require(np.array_equal(state.r, seed.r), "six-period oscillator changed carries")
        if first_return is None and state.same_as(seed):
            first_return = tick
    _require(first_return == 6, "oscillator is not an exact minimal six-step cycle")
    _require(engine.rewind(state, 6).same_as(seed), "oscillator rewind failed")

    pair = Tensor([GearType("left", label="audit"), GearType("right", label="audit")],
                  [(0, 3, [(1, edge, "b")]), (1, 3, [(0, reverse, "b")])],
                  strict_support=True)
    _require(check_reciprocity(pair).ok, "connected pair must be reciprocal")
    engine = Engine(pair)
    seed = State(3, np.zeros((2, 27), dtype=int),
                 np.array([[1]*27, [-1]*27], dtype=int), np.arange(54).reshape(2, 27) % 6)
    state, first_return, sample_pairs = seed.copy(), None, []
    for tick in range(1, 4):
        state = engine.step(state)
        # Equal instantaneous b at one phase would not mean synchronized histories.
        _require(not (np.array_equal(state.a[0], state.a[1])
                      and np.array_equal(state.b[0], state.b[1])),
                 "antisymmetric histories unexpectedly synchronized")
        _require(np.array_equal(state.r, seed.r), "connected pair changed carries")
        sample_pairs.append([[int(state.a[g, 0]), int(state.b[g, 0])] for g in (0, 1)])
        if first_return is None and state.same_as(seed):
            first_return = tick
    _require(first_return == 3, "antisymmetric pair is not an exact period-three cycle")
    _require(engine.rewind(state, 3).same_as(seed), "connected-pair rewind failed")
    return {"six_step_oscillator": {"channels": 1, "minimal_period": 6,
                                    "b_samples_including_initial": b_values,
                                    "all_six_carries_retained": True, "full_rewind": True},
            "reciprocal_nonsynchronizing_pair": {"channels": 2, "face_connected": True,
                                                 "reciprocity": True, "minimal_period": 3,
                                                 "sample_two_slice_pairs": sample_pairs,
                                                 "synchronized_histories": False,
                                                 "all_six_carries_retained": True,
                                                 "full_rewind": True},
            "physical_proper_clock": "not_established"}


def _flat_covector_control():
    covector = (1, 0, 0, -1)
    rest = (1, 0, 0, 0)
    moving = (1, Fraction(3, 5), 0, 0)
    phase = lambda tangent: sum(a*b for a, b in zip(covector, tangent))
    rate_squared = lambda tangent: tangent[0]**2-sum(v*v for v in tangent[1:])
    _require(-covector[0]**2+sum(v*v for v in covector[1:]) == 0, "covector is not null")
    _require(phase(rest) == phase(moving) == 1, "transverse phase comparison failed")
    _require(rate_squared(rest) == 1 and rate_squared(moving) == Fraction(16, 25),
             "independent Minkowski proper-rate calculation failed")
    return {"covector": list(covector), "transverse_velocity": "3/5",
            "rest_phase_rate": "1", "moving_phase_rate": "1",
            "rest_proper_rate": "1", "moving_proper_rate": "4/5",
            "phase_covector_does_not_determine_proper_time": True}


def _conformal_control():
    # A small exact Christoffel/Ricci contraction, independent of the FLRW formula.
    t, x, y, z = sp.symbols("t x y z", real=True)
    coordinates = (t, x, y, z)
    scale = 1+t*t
    minkowski = sp.diag(-1, 1, 1, 1)
    metric = scale**2*minkowski
    inverse = metric.inv()
    connection = [[[sp.simplify(sum(inverse[i, ell]*(
        sp.diff(metric[ell, j], coordinates[k])+sp.diff(metric[ell, k], coordinates[j])
        - sp.diff(metric[j, k], coordinates[ell])) for ell in range(4))/2)
        for k in range(4)] for j in range(4)] for i in range(4)]
    ricci = sp.zeros(4)
    for i in range(4):
        for j in range(4):
            ricci[i, j] = sp.simplify(sum(
                sp.diff(connection[k][i][j], coordinates[k])
                - sp.diff(connection[k][i][k], coordinates[j])
                + sum(connection[k][i][j]*connection[ell][k][ell]
                      - connection[ell][i][k]*connection[k][j][ell] for ell in range(4))
                for k in range(4)))
    curvature = sp.factor(sum(inverse[i, j]*ricci[i, j] for i in range(4) for j in range(4)))
    _require(sp.simplify(curvature-12/scale**3) == 0, "conformal curvature oracle mismatch")
    tangent = sp.Matrix(sp.symbols("v0:4"))
    _require(sp.expand((tangent.T*metric*tangent)[0]
                       - scale**2*(tangent.T*minkowski*tangent)[0]) == 0,
             "conformal null-set identity failed")
    return {"metric": "(1+t^2)^2 diag(-1,1,1,1)", "positive_conformal_factor": True,
            "same_null_set_as_minkowski": True, "stationary_proper_rate": "1+t^2",
            "ricci_scalar": "12/(1+t^2)^3", "minkowski_ricci_scalar": "0",
            "ricci_scalar_at_zero": str(curvature.subs(t, 0)),
            "ricci_scalar_at_one": str(curvature.subs(t, 1)),
            "null_cone_does_not_determine_clock_scale_or_curvature": True}


def audit() -> dict:
    """Run deterministic source-only controls and return a JSON-serializable report.

    No files are read or written, no runtime state is retained outside the
    declared test seeds, and no tensor is promoted to a physical default.
    """
    return {"status": "passed", "scope": "exact coupling and kinematic controls only",
            "potential": _potential_checks(), "edge_runs": [_edge_run(axis) for axis in range(3)],
            "clock_controls": _clock_controls(), "flat_covector": _flat_covector_control(),
            "conformal_ambiguity": _conformal_control(),
            "three_axis_extension_channels": 5, "integrated_with_common45": False,
            "physical_acceptance": "not_established"}
