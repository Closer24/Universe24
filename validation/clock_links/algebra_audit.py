"""Independent integer phase-link identities and reversible receiver controls.

The six-channel analytic control below is validation-only: two free carrier
quadratures and four receiver equations. It is not another supported runtime
or evidence of a proper-time oscillator. The integrated construction is owned
by ``validation.clock_links.model``.
"""
from __future__ import annotations

import argparse
from itertools import product
import hashlib
from pathlib import Path

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core import exact_json


AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ZERO = (0, 0, 0)


def pair_values(left, right):
    """Exact fixed-gauge identities, independent of tensor evaluation."""
    x, y = map(int, left)
    p, q = map(int, right)
    local, other = x*x+y*y, p*p+q*q
    dot, cross = x*p+y*q, x*q-y*p
    coherent = (x+p)**2+(y+q)**2
    return local, other, dot, cross, coherent


def _quarter_turn(pair):
    return -pair[1], pair[0]


def _control_tensor():
    """Independent explicit polynomial for the four receiver equations."""
    gears = [GearType(name, "audit") for name in
             ("control.phi", "control.chi", "control.local_intensity",
              "control.link_x", "control.link_y", "control.link_z")]
    terms = []
    for carrier in (0, 1):
        terms.append((2, 3, ((carrier, ZERO, "b"), (carrier, ZERO, "b"))))
    for output, offset in enumerate(AXES, 3):
        for carrier in (0, 1):
            terms.extend([
                (output, 3, ((carrier, ZERO, "b"), (carrier, ZERO, "b"))),
                (output, 3, ((carrier, offset, "b"), (carrier, offset, "b"))),
                (output, 6, ((carrier, ZERO, "b"), (carrier, offset, "b"))),
            ])
    return Tensor(gears, terms, strict_support=True)


def _analytic_step(state):
    """Equation oracle: no production tensor evaluation or Engine.step."""
    a = np.asarray(state.b, dtype=object).copy()
    b = -np.asarray(state.a, dtype=object).copy()
    for node in range(state.N):
        here = (int(state.b[0, node]), int(state.b[1, node]))
        b[2, node] += here[0]**2+here[1]**2
        for output, direction in enumerate((0, 2, 4), 3):
            other = state.lattice.neighbour(node, direction)
            pair = (int(state.b[0, other]), int(state.b[1, other]))
            b[output, node] += (here[0]+pair[0])**2+(here[1]+pair[1])**2
    return State(state.L, a, b, np.asarray(state.r, dtype=object).copy())


def audit():
    pair_checks = 0
    signed_dot = signed_cross = False
    for x, y, p, q in product(range(-4, 5), repeat=4):
        left, right = (x, y), (p, q)
        local, other, dot, cross, coherent = pair_values(left, right)
        assert dot*dot+cross*cross == local*other
        assert coherent == local+other+2*dot and coherent >= 0
        assert pair_values(_quarter_turn(left), _quarter_turn(right)) == (
            local, other, dot, cross, coherent)
        reflected = pair_values((x, -y), (p, -q))
        assert reflected == (local, other, dot, -cross, coherent)
        signed_dot |= dot < 0
        signed_cross |= cross < 0
        pair_checks += 1
    assert signed_dot and signed_cross

    # Exhaustive one-receiver recurrence over signed sources and histories.
    receiver_checks = 0
    for source, old_a, old_b, carry in product(range(-9, 10), range(-3, 4), range(-3, 4), range(6)):
        quotient, after_r = divmod(6*source+carry, 6)
        after_a, after_b = old_b, quotient-old_a
        assert quotient == source and after_r == carry
        assert (source-after_b, after_a, after_r) == (old_a, old_b, carry)
        receiver_checks += 1

    tensor = _control_tensor()
    assert not tensor.support_violations()
    assert max(m.degree for m in tensor.monomials) == 2
    assert len(tensor.stages) == 1
    engine = Engine(tensor)
    rng = np.random.default_rng(91073)
    matched_states = canonical_events = 0
    max_bits = 0
    for preparation in range(8):
        arrays = [rng.integers(-4, 5, size=(6, 27)).astype(object) for _ in range(2)]
        remainder = np.array([[(g+n+preparation) % 6 for n in range(27)] for g in range(6)], dtype=object)
        if preparation == 7:
            arrays[0][0, 0], arrays[1][1, 26] = -(1 << 100), 1 << 120
        initial = State(3, arrays[0], arrays[1], remainder)
        actual = oracle = initial
        for step in range(1, 9):
            before = actual
            actual, oracle = engine.step(actual), _analytic_step(oracle)
            assert actual.same_as(oracle)
            assert np.array_equal(actual.r, remainder)
            assert engine.inverse_step(actual).same_as(before)
            clicks = engine.clicks(before, actual, step)
            assert all(int(kind) == 0 for kind in clicks.kind)
            matched_states += 1
            canonical_events += len(clicks)
            max_bits = max(max_bits, actual.max_abs().bit_length())
        assert engine.rewind(actual, 8).same_as(initial)

    # A uniformly rotating nonzero carrier can have a stationary receiver.
    # Its positive intensity never creates a canonical receiver event.
    a = np.zeros((6, 27), dtype=object)
    b = np.zeros_like(a)
    a[0], a[1], b[0], b[1] = -1, 1, 1, 1
    a[2], b[2], a[3:], b[3:] = 1, 1, 4, 4
    stationary = State(3, a, b, np.zeros_like(a))
    state = stationary
    hidden_positive_steps = 0
    for step in range(1, 9):
        after = engine.step(state)
        quotient = after.b+state.a
        assert all(int(x) > 0 for x in quotient[2:].flat)
        assert np.array_equal(state.a[2:], after.a[2:])
        assert np.array_equal(state.b[2:], after.b[2:])
        assert not any(int(g) >= 2 for g in engine.clicks(state, after, step).gear)
        hidden_positive_steps += 1
        state = after
    assert engine.rewind(state, 8).same_as(stationary)
    # Distinct intensity ratios can produce exactly the same entire empty
    # canonical stream in this analytic family. The integrated 44-channel
    # carrier is different; its one-step receiver-only analogue follows by
    # preparing every added receiver at F/2 when F is even.
    silent_ratios = []
    for bright_node in (0, 1):
        amplitude = np.ones(27, dtype=object)
        amplitude[bright_node] = 3
        left = np.zeros((6, 27), dtype=object)
        right = np.zeros_like(left)
        left[0], left[1], right[0], right[1] = -amplitude, amplitude, amplitude, amplitude
        left[2], right[2] = amplitude*amplitude, amplitude*amplitude
        for row, direction in enumerate((0, 2, 4), 3):
            other = np.array([amplitude[stationary.lattice.neighbour(n, direction)] for n in range(27)], dtype=object)
            left[row] = right[row] = (amplitude+other)**2
        seed = State(3, left, right, np.zeros_like(left))
        current = seed
        for step in range(1, 9):
            following = engine.step(current)
            assert len(engine.clicks(current, following, step)) == 0
            current = following
        assert engine.rewind(current, 8).same_as(seed)
        silent_ratios.append([int(amplitude[0]**2), int(amplitude[1]**2)])
    assert silent_ratios == [[9, 1], [1, 9]]
    # Local independent phase rotation changes a bare face correlation.
    original = pair_values((1, 0), (1, 0))
    local_rotation = pair_values((1, 0), (0, 1))
    assert original[:2] == local_rotation[:2]
    assert original[2:] != local_rotation[2:]

    return {
        "schema": "universe24/validation/clock-link-algebra/1",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pair_identity_cases": pair_checks,
        "signed_receiver_inverse_cases": receiver_checks,
        "independent_equation_oracle_states": matched_states,
        "all_six_remainders_covered": True,
        "canonical_events_all_C0": canonical_events,
        "complete_rewinds": 9,
        "maximum_retained_bits": max_bits,
        "single_edge_support_violations": 0,
        "degree": 2,
        "standalone_validation_control_channels": 6,
        "integrated_allocation_proposed": {"base": 44, "new": 4, "total": 48},
        "analytic_control_tensor_hash": tensor.fingerprint,
        "stationary_positive_intensity_without_receiver_clicks": {
            "steps": hidden_positive_steps, "nodes": 27, "receiver_channels": 4,
            "local_intensity": 2, "link_intensity": 8,
        },
        "same_empty_observation_different_intensity_ratios": {
            "ratios": silent_ratios, "steps": 8,
            "claim": "No decoder of this empty stream can distinguish the two ratios. Integrated-carrier extension is only a one-step receiver-only argument, not an eight-step theorem about the 44-channel source.",
        },
        "independent_local_gauge_control": {
            "before": list(original), "after": list(local_rotation),
            "status": "failed_local_gauge_invariance",
        },
        "gates": {
            "phase_link_identity": "passed",
            "retained_receiver_inverse": "passed",
            "common_quarter_turn_invariance": "passed",
            "local_gauge_invariance_of_bare_link": "failed",
            "intensity_equals_canonical_event_count": "failed",
            "proper_time_clock": "not_tested",
            "born_selection": "not_tested",
            "bell": "not_tested",
            "structural_growth": "not_tested",
        },
        "interpretation": "Exact algebra and independent small validation control, not another physical runtime. Integrated 48-channel oracle checks are separate. Bare links require a declared fixed gauge; all receiver events here are C0. No probability law is inferred from intensity or event counts.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/clock_links/algebra"))
    args = parser.parse_args(argv)
    report = audit()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"algebra.json").write_text(exact_json.dumps(report, sort_keys=True)+"\n")
    print(exact_json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
