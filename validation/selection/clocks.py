"""Native integer clocks and an exact local gate embedding in fixed-six Rule3.

Research validation only. The compiler below adds no Engine mode and no
runtime selector: it returns one immutable polynomial tensor. A reversible
three-bit gate and one streamed lane determine its complete law before a run.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
from pathlib import Path

import numpy as np

from universe24.core import DIRECTIONS, Engine, GearType, State, Tensor, lattice
from universe24.core import exact_json


ZERO = (0, 0, 0)


def native_coordinates(a, b, r):
    a, b, r = (np.asarray(value, dtype=object) for value in (a, b, r))
    return b.copy(), 6*(b-a)+r


def clock_invariant(a, b):
    a, b = np.asarray(a, dtype=object), np.asarray(b, dtype=object)
    return a*a+b*b-a*b


def clock_tensor():
    return Tensor([GearType('clock.native', 'audit')],
                  [(0, 3, [(0, ZERO, 'b')])], strict_support=True)


def _direction(direction):
    direction = tuple(direction)
    if direction not in DIRECTIONS:
        raise ValueError('one physical face direction is required')
    return direction


def matched_clock_tensor(direction=(1, 0, 0)):
    direction = _direction(direction)
    opposite = tuple(-x for x in direction)
    return Tensor([GearType('clock.left', 'audit'), GearType('clock.right', 'audit')],
                  [(0, 3, [(1, direction, 'b')]),
                   (1, 3, [(0, opposite, 'b')])], strict_support=True)


def _matched(values, lat, direction):
    return np.array([values[1, lat.shift_index(direction)],
                     values[0, lat.shift_index(tuple(-x for x in direction))]], dtype=object)


def matched_invariant(state, direction=(1, 0, 0)):
    a, b = state.a.astype(object), state.b.astype(object)
    return sum(int(x) for x in (a*a+b*b-a*_matched(b, state.lattice, direction)).flat)


def checked_gate(gate_table):
    table = tuple(tuple(row) for row in gate_table)
    if (len(table) != 8 or any(len(row) != 3 for row in table)
            or any(type(bit) is not int or bit not in (0, 1) for row in table for bit in row)
            or len(set(table)) != 8):
        raise ValueError('gate_table must be a permutation of all eight integer three-bit states')
    return table


def inverse_gate(gate_table):
    table = checked_gate(gate_table)
    inverse = [None]*8
    for index, row in enumerate(table):
        inverse[4*row[0]+2*row[1]+row[2]] = (index//4, (index//2) % 2, index % 2)
    return tuple(inverse)


def multilinear_coefficients(gate_table, output):
    """Integer Mobius interpolation on the declared Boolean cube."""
    table = checked_gate(gate_table)
    result = []
    for mask in range(8):
        value = 0
        for sub in range(8):
            if sub & ~mask:
                continue
            bits = tuple((sub >> j) & 1 for j in range(3))
            index = 4*bits[0]+2*bits[1]+bits[2]
            value += (-1)**((mask ^ sub).bit_count())*table[index][output]
        if value:
            result.append((value, tuple(j for j in range(3) if mask & (1 << j))))
    return tuple(result)


def build_native_gate(gate_table, direction=(1, 0, 0), name='selection'):
    """Embed F=S_x G via u=3(F+F^-1); only lane1 is streamed.

    Forward local-gate monomials are entirely at target or its incoming face.
    Inverse monomials use lane1 at the outgoing face and other inputs at target.
    Consequently each term uses one face edge even when degree is three.
    """
    table = checked_gate(gate_table)
    direction = _direction(direction)
    incoming = tuple(-x for x in direction)
    terms = []
    for output in range(3):
        forward_offset = incoming if output == 1 else ZERO
        for coefficient, inputs in multilinear_coefficients(table, output):
            terms.append((output, 3*coefficient, [(j, forward_offset, 'b') for j in inputs]))
        for coefficient, inputs in multilinear_coefficients(inverse_gate(table), output):
            terms.append((output, 3*coefficient,
                          [(j, direction if j == 1 else ZERO, 'b') for j in inputs]))
    return Tensor([GearType(f'{name}.{suffix}', 'audit')
                   for suffix in ('memory', 'moving', 'local')], terms, strict_support=True)


def first_order(values, gate_table, L, direction=(1, 0, 0), inverse=False):
    """Independent table/shift oracle, never evaluates the compiled tensor."""
    table = checked_gate(gate_table)
    direction = _direction(direction)
    lat = lattice(L)
    values = np.asarray(values, dtype=object)
    if (values.shape != (3, lat.N)
            or any((type(x) is not int and not isinstance(x, np.integer))
                   or int(x) not in (0, 1) for x in values.flat)):
        raise ValueError('first-order gate oracle requires exactly three Boolean lanes')
    values = values.copy()
    if inverse:
        values[1] = values[1, lat.shift_index(direction)]
        table = inverse_gate(table)
    indices = 4*values[0]+2*values[1]+values[2]
    result = np.array([table[int(i)] for i in indices], dtype=object).T
    if not inverse:
        result[1] = result[1, lat.shift_index(tuple(-x for x in direction))]
    return result


def prepare_gate(gate_table, current, L, direction=(1, 0, 0), remainders=None):
    current = np.asarray(current, dtype=object)
    previous = first_order(current, gate_table, L, direction, inverse=True)
    r = np.zeros_like(current) if remainders is None else np.asarray(remainders, dtype=object)
    if r.shape != current.shape or any(type(x) is not int or x < 0 or x > 5 for x in r.flat):
        raise ValueError('provide every valid remainder explicitly or use zero preparation')
    return State(L, previous, current, r)


def validate_prepared_state(state, gate_table, direction=(1, 0, 0)):
    expected = first_order(state.b, gate_table, state.L, direction, inverse=True)
    if not np.array_equal(state.a, expected):
        raise ValueError('state is outside the invariant sector a=F^-1(b)')
    if any(int(x) < 0 or int(x) > 5 for x in state.r.flat):
        raise ValueError('invalid retained remainder')
    return True


def _clock_checks():
    tensor = clock_tensor()
    engine = Engine(tensor)
    scalar_cases = 0
    for a, b, r in product(range(-5, 6), range(-5, 6), range(6)):
        old_a, old_b = a, b
        invariant = a*a+b*b-a*b
        for _ in range(6):
            quotient, next_r = divmod(6*b+r, 6)
            after_a, after_b = b, quotient-a
            q, p = b, 6*(b-a)+r
            next_p = p-6*q
            assert after_b == q+next_p//6
            assert next_r == next_p % 6 == r
            assert after_a*after_a+after_b*after_b-after_a*after_b == invariant
            a, b = after_a, after_b
        assert (a, b) == (old_a, old_b)
        scalar_cases += 1
    rng = np.random.default_rng(118203)
    a = rng.integers(-5, 6, size=(1, 27)).astype(object)
    b = rng.integers(-5, 6, size=(1, 27)).astype(object)
    a[0, 0], b[0, 1] = -(1 << 90), 1 << 100
    r = np.array([[n % 6 for n in range(27)]], dtype=object)
    seed = State(3, a, b, r)
    state = seed
    for _ in range(6):
        following = engine.step(state)
        assert np.array_equal(following.a, state.b)
        assert np.array_equal(following.b, state.b-state.a)
        assert np.array_equal(clock_invariant(following.a, following.b), clock_invariant(seed.a, seed.b))
        state = following
    assert state.same_as(seed)
    assert engine.rewind(state, 6).same_as(seed)
    matched = 0
    for direction in DIRECTIONS:
        tensor = matched_clock_tensor(direction)
        engine = Engine(tensor)
        a, b = [rng.integers(-5, 6, size=(2, 27)).astype(object) for _ in range(2)]
        r = np.array([[(g+n) % 6 for n in range(27)] for g in range(2)], dtype=object)
        seed = State(3, a, b, r)
        initial_invariant = matched_invariant(seed, direction)
        state = seed
        for step in range(1, 7):
            expected = _matched(state.b.astype(object), state.lattice, direction)-state.a
            state = engine.step(state)
            assert np.array_equal(state.b, expected)
            assert matched_invariant(state, direction) == initial_invariant
            if step == 3:
                assert np.array_equal(state.a, -_matched(seed.a, seed.lattice, direction))
                assert np.array_equal(state.b, -_matched(seed.b, seed.lattice, direction))
            matched += 1
        assert state.same_as(seed)
        assert engine.rewind(state, 6).same_as(seed)
    return {'exhaustive_scalar_clock_cases': scalar_cases,
            'native_clock_period': 6, 'native_clock_positive_invariant': 'a^2+b^2-a*b',
            'all_remainders': list(range(6)), 'matched_face_states': matched,
            'matched_directions': 6, 'matched_clock_period': 6,
            'matched_clock_three_steps': 'signed face exchange of both retained slices',
            'proper_time_clock_demonstrated': False}


def audit(gate_table=None):
    if gate_table is None:
        # Lane4's independently specified reversible sorting table, in m,x,y order.
        gate_table = ((0, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1),
                      (1, 0, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1))
    gate_table = checked_gate(gate_table)
    inverse = inverse_gate(gate_table)
    assert inverse != gate_table  # This audit must exercise a genuinely noninvolutive gate.
    for index, row in enumerate(gate_table):
        assert inverse[4*row[0]+2*row[1]+row[2]] == (index//4, (index//2) % 2, index % 2)
    rng = np.random.default_rng(126007)
    states = events = rewinds = off_sector_rewinds = 0
    tensors = []
    for direction in DIRECTIONS:
        tensor = build_native_gate(gate_table, direction)
        engine = Engine(tensor)
        assert tensor.G == 3 and tensor.rank-1 <= 3 and not tensor.support_violations()
        assert not any(f.field == 'a' for monomial in tensor.monomials for f in monomial.factors)
        tensors.append({'direction': list(direction), 'tensor_hash': tensor.fingerprint,
                        'monomials': len(tensor), 'degree': tensor.rank-1})
        for run in range(8):
            current = rng.integers(0, 2, size=(3, 27)).astype(object)
            remainders = np.array([[(g+n+run) % 6 for n in range(27)] for g in range(3)], dtype=object)
            seed = prepare_gate(gate_table, current, 3, direction, remainders)
            validate_prepared_state(seed, gate_table, direction)
            state = seed
            particles = int(sum(current[1:].flat))
            for step in range(1, 25):
                expected = first_order(state.b, gate_table, state.L, direction)
                following = engine.step(state)
                assert np.array_equal(following.a, state.b)
                assert np.array_equal(following.b, expected)
                assert np.array_equal(following.r, remainders)
                validate_prepared_state(following, gate_table, direction)
                assert int(sum(following.b[1:].flat)) == particles
                assert engine.inverse_step(following).same_as(state)
                clicks = engine.clicks(state, following, step)
                assert all(int(kind) == 0 for kind in clicks.kind)
                events += len(clicks)
                state = following
                states += 1
            assert engine.rewind(state, 24).same_as(seed)
            rewinds += 1
        bad = seed.copy()
        bad.a[0, 0] = 1-int(bad.a[0, 0])
        try:
            validate_prepared_state(bad, gate_table, direction)
        except ValueError:
            pass
        else:
            raise AssertionError('unprepared state must not inherit the Boolean invariant claim')
        # The full Rule3 polynomial still rewinds outside the prepared Boolean
        # sector; only the first-order gate interpretation is withheld there.
        unprepared = State(3, rng.integers(-2, 3, size=(3, 27)).astype(object),
                           rng.integers(-2, 3, size=(3, 27)).astype(object), remainders)
        off_state = unprepared
        for _ in range(3):
            following = engine.step(off_state)
            assert engine.inverse_step(following).same_as(off_state)
            off_state = following
        assert engine.rewind(off_state, 3).same_as(unprepared)
        off_sector_rewinds += 1
    return {'schema': 'universe24/validation/native-clocks-selection/1',
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'clocks': _clock_checks(),
            'gate_table': [list(row) for row in gate_table],
            'inverse_gate_table': [list(row) for row in inverse],
            'noninvolutive_gate_checked': True,
            'gate_states_against_independent_first_order_oracle': states,
            'complete_24_step_rewinds': rewinds,
            'off_sector_complete_3_step_rewinds': off_sector_rewinds,
            'canonical_C0_events': events,
            'prepared_sector': 'Boolean b; a=F^-1(b); arbitrary 0<=r<6',
            'prepared_sector_preserved': True, 'unprepared_state_rejected': True,
            'data_particle_number_conserved': True,
            'data_a_b_max_bits': 1, 'retained_remainder_max_bits': 3,
            'channels': 3, 'retained_integers_per_node': 9,
            'compiled_tensors': tensors,
            'degree_max': 3, 'strict_support_violations': 0,
            'runtime_callbacks': 0, 'old_a_input_dependencies': [],
            'claim_scope': 'Exact bounded local clock and prepared Boolean memory/transport mechanism in the existing Engine. Not coupled to the corrected45 metric or source, not another installed runtime.',
            'physical_claims': {'proper_time': 'not_tested', 'shared_metric_stress': 'not_tested',
                                'born': 'not_tested', 'bell': 'not_tested',
                                'indefinite_complexity_growth': 'not_established'}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/selection/clocks'))
    args = parser.parse_args(argv)
    report = audit()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'clocks.json').write_text(exact_json.dumps(report, sort_keys=True)+'\n')
    print(exact_json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
