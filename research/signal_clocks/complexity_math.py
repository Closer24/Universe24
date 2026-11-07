"""Exact, passive mathematics helpers; never an engine path-selection rule."""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product


def cooperation_score(base, singles, pairs):
    """Fraction of nonzero exact mixed outlet vectors for predeclared probes.

    The caller supplies already recorded integer vectors, not evolving states.
    Missing calibration trajectories are an error, not a zero response.
    """
    base = tuple(base)
    labels = tuple(sorted(singles))
    if len(labels) < 2:
        raise ValueError('At least two fixed perturbation addresses are required')
    expected = set(combinations(labels, 2))
    if set(pairs) != expected:
        raise ValueError('Every distinct calibration pair must be supplied exactly once')
    vectors = [base, *map(tuple, singles.values()), *map(tuple, pairs.values())]
    if any(len(vector) != len(base) for vector in vectors):
        raise ValueError('All exact outlet vectors must have the same fixed coordinates')
    if not base or any(type(value) is not int for vector in vectors for value in vector):
        raise ValueError('Outlet vectors must contain exact integers and be nonempty')
    nonzero = []
    for i, j in sorted(expected):
        mixed = tuple(pairs[(i, j)][k] - singles[i][k] - singles[j][k] + base[k]
                      for k in range(len(base)))
        if any(mixed):
            nonzero.append((i, j))
    return Fraction(len(nonzero), len(expected)), tuple(nonzero)


def event_indices(events):
    """External history-derived event index; it is not an internal state field."""
    result = [0]
    for event in events:
        if type(event) is not int or event not in (0, 1):
            raise ValueError('Events must be exact 0/1 values')
        result.append(result[-1] + event)
    return tuple(result)


def quiet_record_capacity(channels):
    """Distinct quiet remainder records in one fixed-parity sector."""
    if type(channels) is not int or channels < 0:
        raise ValueError('Channel count must be a nonnegative integer')
    return 3 ** channels


def finite_checks():
    """Supplementary finite checks of identities proved in the documentation."""
    carries = []
    for theta in range(3):
        q = tuple((theta + u) // 3 for u in range(3))
        mixed = q[2] - 2 * q[1] + q[0]
        carries.append({'theta': theta, 'q': q, 'mixed': mixed})
    assert [entry['mixed'] for entry in carries] == [0, 1, -1]
    # Opposite response signs receive the same non-additivity score.
    positive, _ = cooperation_score((0,), {0: (0,), 1: (0,)}, {(0, 1): (1,)})
    negative, _ = cooperation_score((0,), {0: (1,), 1: (1,)}, {(0, 1): (1,)})
    assert positive == negative == 1
    finite_permutations = 0
    for permutation in permutations(range(4)):
        for scores in product(range(3), repeat=4):
            increments = [scores[permutation[i]] - scores[i] for i in range(4)]
            assert sum(increments) == 0
            if all(value >= 0 for value in increments):
                assert not any(increments)
            finite_permutations += 1
    events = (0, 0, 1, 0, 0, 0, 1, 0)
    indices = event_indices(events)
    assert indices == (0, 0, 0, 1, 1, 1, 1, 2, 2)
    records = {tuple(values) for values in product((0, 2, 4), repeat=3)}
    assert len(records) == quiet_record_capacity(3) == 27
    return {'format': 'universe24-complexity-math-check-v1', 'passed': True,
            'scope': 'Finite checks supplement exact proofs; no full-board routing or physical-light claim',
            'carry_table': carries, 'permutation_score_checks': finite_permutations,
            'event_indices': indices, 'three_channel_quiet_record_capacity': len(records)}


if __name__ == '__main__':
    import json
    print(json.dumps(finite_checks(), sort_keys=True))
