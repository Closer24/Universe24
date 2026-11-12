"""Exact native-coordinate, carry and canonical-click identities.

The helpers are passive coordinate maps. Engine alone advances retained state.
Packing is not a change to the channel budget or a polynomial compiler.
"""
from __future__ import annotations

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.system.decoder import decode_transition, make_transition
from validation.system_smoke import scalar_step

ZERO = (0, 0, 0)


def pack(a: int, b: int, r: int) -> tuple[int, int]:
    """Encode one legal complete triple, without discarding its carry."""
    if any(type(value) is not int for value in (a, b, r)):
        raise TypeError('coordinates must be exact Python integers')
    if not 0 <= r < 6:
        raise ValueError('remainder must be in 0..5')
    return b, 6 * (b - a) + r


def unpack(position: int, momentum: int) -> tuple[int, int, int]:
    """Recover both histories and the carry, including negative momenta."""
    if any(type(value) is not int for value in (position, momentum)):
        raise TypeError('coordinates must be exact Python integers')
    return position - momentum // 6, position, momentum % 6


def mixed_tensor() -> Tensor:
    """A deliberately nonlinear face-local fixture with acyclic old-a reads."""
    def factor(name, offset=ZERO, field='b'):
        return name, offset, field
    return Tensor(['x', 'y', 'z'], [
        ('x', 2, [factor('x')]), ('x', 1, [factor('y', (1, 0, 0))]),
        ('x', -3, []), ('y', -1, [factor('x')]),
        ('y', 1, [factor('x', field='a'), factor('y')]),
        ('y', 2, [factor('z'), factor('z'), factor('z', (0, 1, 0))]),
        ('z', 1, [factor('z')]), ('z', -1, [factor('y', (0, 0, -1), 'a')]),
    ], strict_support=True)


def _records(tensor, before, after, step):
    return decode_transition(make_transition(tensor, before, after,
                                             run_id='generic-native-audit', step=step), tensor)


def audit() -> dict:
    """Check mixed actual Engine trajectories against independent identities."""
    tensor = mixed_tensor()
    engine = Engine(tensor)
    rng = np.random.default_rng(20261112)
    comparisons = emitted = 0
    maximum_bits = 0
    for _ in range(20):
        a = rng.integers(-3, 4, size=(3, 27))
        b = rng.integers(-3, 4, size=(3, 27))
        trit = rng.integers(0, 3, size=(3, 27))
        parity = rng.integers(0, 2, size=(3, 27))
        initial = state = State(3, a, b, 2 * trit + parity)
        twin_initial = twin = State(3, a, b, 2 * trit + 1 - parity)
        for step in range(1, 5):
            drive = engine.inputs(state).astype(object)
            following = engine.step(state)
            twin_following = engine.step(twin)
            assert following.same_as(scalar_step(tensor, state))
            assert np.array_equal(following.a, twin_following.a)
            assert np.array_equal(following.b, twin_following.b)
            assert np.array_equal(following.r // 2, (drive + state.r // 2) % 3)
            assert np.array_equal(following.r % 2, parity)
            assert np.array_equal(following.b, (drive + state.r // 2) // 3 - state.a)
            records = _records(tensor, state, following, step)
            assert records == _records(tensor, twin, twin_following, step)
            for record in records:
                assert record['kind'] == f"C{int(drive[record['channel'], record['node']] % 3)}"
            for gear in range(tensor.G):
                for node in range(state.N):
                    position, momentum = pack(*state.gear(gear, node))
                    next_momentum = momentum + 2 * int(drive[gear, node]) - 12 * position
                    assert unpack(position + next_momentum // 6, next_momentum) == following.gear(gear, node)
            emitted += len(records)
            comparisons += state.G * state.N
            maximum_bits = max(maximum_bits, *(abs(int(v)).bit_length() for v in following.b.flat))
            state, twin = following, twin_following
        assert engine.rewind(state, 4).same_as(initial)
        assert engine.rewind(twin, 4).same_as(twin_initial)

    # A changed retained oscillator can have no canonical records at all.
    silent = Tensor(['clock'], [], strict_support=True)
    silent_engine = Engine(silent)
    for carry in range(6):
        initial = state = State(3, [[1] * 27], [[0] * 27], [[carry] * 27])
        for step in range(1, 5):
            following = silent_engine.step(state)
            assert not state.same_as(following)
            assert _records(silent, state, following, step) == []
            state = following
        assert state.same_as(initial)
        assert silent_engine.rewind(state, 4).same_as(initial)

    # Fourth finite differences of a cubic vanish. Reencoded old-a reads
    # contain a floor whose fourth difference does not vanish.
    values = [p // 6 for p in range(3, 8)]
    fourth_difference = values[0] - 4 * values[1] + 6 * values[2] - 4 * values[3] + values[4]
    assert fourth_difference == -3
    assert 2 * ((2 * 2) // 6) != (2 * (2 + 2)) // 6
    return {
        'status': 'passed', 'tensor_hash': tensor.fingerprint,
        'channel_updates_compared': comparisons, 'canonical_clicks_checked': emitted,
        'maximum_integer_bits': maximum_bits, 'scalar_oracle': 'passed',
        'carry_parity_and_trit': 'passed', 'class_equals_drive_modulo_three': 'passed',
        'complete_coordinate_reconstruction': 'passed', 'complete_rewinds': 'passed',
        'silent_period_four_all_carries': 'passed', 'packed_channel_saving': 0,
        'old_history_floor_fourth_difference': fourth_difference,
        'physics_acceptance': 'not_established',
    }
