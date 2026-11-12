"""Complete-state constraint certificates, with positive and negative oracles.

Run ``python -m validation.generic_structure.constraint_certificate``.
These source-only examples are mathematical fixtures, not Einstein models.
The reversible-map embedding is already used elsewhere in the repository;
this audit makes its history-domain and invariant-constraint obligations explicit.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO
from validation.completion import constraint_closure


ROOT = Path(__file__).resolve().parents[2]


def maps(kind, values, inverse=False):
    """Independent integer formulas for the target and its proved inverse."""
    sign = -1 if inverse else 1
    if kind == 'linear_lorentz':
        x, y = values
        return (2*x+sign*y, sign*3*x+2*y)
    if kind == 'cubic_null_rotation':
        x, y, z = values
        return (x, y+sign*2*x*x, z-sign*2*x*y-2*x*x*x)
    raise ValueError(kind)


def quadratic(kind, values):
    if kind == 'linear_lorentz':
        x, y = values
        return 3*x*x-y*y
    x, y, z = values
    return 2*x*z+y*y


def scalar_force(kind, values):
    """The actual tensor input u, independently of tensor interpretation."""
    if kind == 'linear_lorentz':
        return tuple(12*x for x in values)
    x, y, z = values
    return (6*x, 6*y, 6*z-12*x*x*x)


def scalar_step(kind, state):
    """Independent per-entry divmod oracle, including every retained carry."""
    a, b, r = state.a.copy(), state.b.copy(), state.r.copy()
    for node in range(state.N):
        force = scalar_force(kind, tuple(map(int, state.b[:, node])))
        for gear, u in enumerate(force):
            ell, remainder = divmod(2*u+int(state.r[gear, node]), 6)
            a[gear, node] = int(state.b[gear, node])
            b[gear, node] = ell-int(state.a[gear, node])
            r[gear, node] = remainder
    return State(state.L, a, b, r)


def build(kind):
    names = ('certificate.x', 'certificate.y')
    if kind == 'cubic_null_rotation':
        names += ('certificate.z',)
    coefficient = 12 if kind == 'linear_lorentz' else 6
    terms = [(name, coefficient, ((name, ZERO, 'b'),)) for name in names]
    if kind == 'cubic_null_rotation':
        terms.append((names[2], -12, ((names[0], ZERO, 'b'),)*3))
    return Tensor([GearType(name, label='audit') for name in names], terms,
                  strict_support=True)


def symbolic_certificate(kind):
    n = 2 if kind == 'linear_lorentz' else 3
    b = sp.symbols(f'b0:{n}')
    a = sp.symbols(f'a0:{n}')
    target, inverse = maps(kind, b), maps(kind, b, inverse=True)
    assert all(sp.expand(left-right) == 0 for left, right in zip(maps(kind, target, True), b))
    assert all(sp.expand(left-right) == 0 for left, right in zip(maps(kind, inverse), b))
    assert sp.expand(quadratic(kind, target)-quadratic(kind, b)) == 0
    # No quotient issue here: all u are multiples of 3 and 0 <= r < 6.
    actual_next = tuple(sp.expand(u/3-old) for u, old in zip(scalar_force(kind, b), a))
    compatibility = [sp.expand(a[i]-inverse[i]) for i in range(n)]
    after_constraints = [sp.expand(b[i]-maps(kind, actual_next, True)[i]) for i in range(n)]
    after_constraints.append(sp.expand(quadratic(kind, actual_next)-quadratic(kind, b)))
    # Exact polynomial membership, not merely substitution at sample seeds.
    basis = sp.groebner(compatibility, *a, *b)
    reductions = [basis.reduce(value)[1] for value in after_constraints]
    assert reductions == [0]*(n+1)
    assert all(sp.expand(actual_next[i].subs(dict(zip(a, inverse)))-target[i]) == 0
               for i in range(n))
    return {'target': list(map(str, target)), 'inverse': list(map(str, inverse)),
            'quadratic': str(quadratic(kind, b)),
            'history_generators': list(map(str, compatibility)),
            'inverse_compositions_exact': True, 'quadratic_identity_exact': True,
            'complete_history_ideal_remainders': list(map(str, reductions)),
            'commuting_encoding_identity': True}


def engine_audit(kind, ticks=24):
    tensor = build(kind)
    engine = Engine(tensor)
    n, nodes = tensor.G, 27
    # Different positive, negative, zero and null-form values at different nodes.
    values = np.array([[(node*(gear+2)+gear) % 7-3 for node in range(nodes)]
                       for gear in range(n)], dtype=object)
    if kind == 'cubic_null_rotation':
        values[:, 0] = (1, 0, 0)  # Nontrivial trajectory on the null cone.
    else:
        values[:, 0] = (1, 0)  # Q=3, not a Euclidean oscillator.
    q = [quadratic(kind, tuple(map(int, values[:, node]))) for node in range(nodes)]
    max_bits = 0
    for carry in range(6):
        previous = np.array([maps(kind, tuple(map(int, values[:, node])), True)
                             for node in range(nodes)], dtype=object).T
        seed = State(3, previous, values.copy(), np.full((n, nodes), carry, dtype=object))
        state = seed
        expected = values.copy()
        for _ in range(ticks):
            old = state
            state = engine.step(old)
            assert state.same_as(scalar_step(kind, old))
            assert engine.inverse_step(state).same_as(old)
            expected = np.array([maps(kind, tuple(map(int, expected[:, node])))
                                 for node in range(nodes)], dtype=object).T
            assert np.array_equal(state.b, expected)
            assert np.array_equal(state.r, seed.r)
            for node in range(nodes):
                point = tuple(map(int, state.b[:, node]))
                assert tuple(map(int, state.a[:, node])) == maps(kind, point, True)
                assert quadratic(kind, point) == q[node]
            max_bits = max(max_bits, *(abs(int(value)).bit_length()
                                      for array in (state.a, state.b, state.r)
                                      for value in array.flat))
        assert engine.rewind(state, ticks).same_as(seed)
    assert not tensor.support_violations()
    assert tensor.b_only
    return {'status': 'passed', 'channels': n, 'retained_integers_per_node': 3*n,
            'monomials': len(tensor), 'degree_bound': 1 if n == 2 else 3,
            'tensor_sha256': tensor.fingerprint, 'nodes': nodes,
            'complete_carry_cases': list(range(6)), 'ticks_per_case': ticks,
            'node_transitions': 6*ticks*nodes, 'max_retained_bits': max_bits,
            'independent_scalar_oracle': True, 'target_oracle': True,
            'inverse_each_step_and_full_rewind': True,
            'complete_history_invariant': True, 'quadratic_invariant': True,
            'spatial_coupling': 'onsite only; no Einstein or signal claim'}


def incompatible_histories():
    tensor = build('linear_lorentz')
    engine = Engine(tensor)
    b = np.array([[1]*27, [0]*27], dtype=object)
    failures = []
    for carry in range(6):
        seed = State(3, b.copy(), b.copy(), np.full((2, 27), carry, dtype=object))
        after = engine.step(seed)
        assert after.same_as(scalar_step('linear_lorentz', seed))
        assert engine.inverse_step(after).same_as(seed)
        assert tuple(map(int, after.b[:, 0])) == (3, 0)
        assert quadratic('linear_lorentz', seed.a[:, 0]) == 3
        assert quadratic('linear_lorentz', seed.b[:, 0]) == 3
        assert quadratic('linear_lorentz', after.b[:, 0]) == 27
        failures.append({'carry': carry, 'Q_a': 3, 'Q_b': 3, 'Q_next_b': 27,
                         'constraint_defect_relative_to_Q_3': 24})
    return {'status': 'counterexample_verified', 'complete_history_compatible': False,
            'both_individual_histories_constrained': True, 'cases': failures,
            'mechanical_inverse_still_passes': True}


def reduced_source_failure():
    result = constraint_closure.history_audit()
    expected = ('-211805381883956703960796807492009984/'
                '6648074056234057895988554997906461158237804299242833919931086162572083201')
    assert result['rows'][1]['constraint'] == expected
    assert result['rows'][0]['constraint'] == '0'
    return result


def main():
    examples = {kind: {'symbolic': symbolic_certificate(kind), 'engine': engine_audit(kind)}
                for kind in ('linear_lorentz', 'cubic_null_rotation')}
    paths = [Path(__file__), ROOT/'validation/completion/constraint_closure.py']
    result = {
        'schema': 'universe24.generic-constraint-certificate.v1',
        'positive_complete_state_examples': examples,
        'two_individually_constrained_histories_are_insufficient': incompatible_histories(),
        'continuous_vs_discrete_and_rational_target': constraint_closure.algebra_audit(),
        'actual_reduced_five_channel_failure': reduced_source_failure(),
        'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in paths},
        'claim_status': {
            'complete_state_sufficient_criterion': 'proved_conditionally',
            'onsite_integer_quadratic_constraint_examples': 'passed',
            'existing_reduced_Einstein_lift_constraint_gate': 'failed',
            'rational_Einstein_target_compiled_with_valid_history': 'not_implemented',
            'general_Einstein_constraints': 'blocked'},
        'limitations': [
            'Positive examples are onsite mathematical fixtures, not physical gravity.',
            'An invariant constraint is insufficient to identify Einstein dynamics.',
            'No rational state-dependent denominator or hidden solver is added to the Engine.',
            'General nonzero-denominator, full45 domain and constraint closure remain open.']}
    path = ROOT/'runs/generic-structure/constraints.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['claim_status'], indent=2))
    print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
