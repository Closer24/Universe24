"""Exact, source-only obstruction controls; not a candidate Einstein model.

Run from repository root with:
    python validation/research_eight/06_algebra_obstructions.py
The artifact is written to runs/research_eight/06_algebra_obstructions.json.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from math import gcd
from pathlib import Path
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO


def derivation_control():
    """Idempotent equations kill all N*N entries of any pointwise derivation."""
    dimensions = (1, 2, 3, 7, 12)
    ranks = []
    for size in dimensions:
        # D(e_j**2)_i=2*(e_j)_i*D(e_j)_i means
        # (1-2*delta_ij)*D_ij=0. Each coefficient is +1 or -1.
        constraints = {(i, j): 1-2*int(i == j)
                       for i in range(size) for j in range(size)}
        assert all(abs(value) == 1 for value in constraints.values())
        assert len(constraints) == size*size
        ranks.append({'sites': size, 'unknowns': size*size,
                      'independent_constraints': len(constraints), 'nullity': 0})
    rng = random.Random(602026)
    exact_checks = 0
    ordinary_failures = 0
    for size in (3, 7, 12):
        for _ in range(100):
            f = [rng.randrange(-20, 21) for _ in range(size)]
            g = [rng.randrange(-20, 21) for _ in range(size)]
            for i in range(size):
                j = (i+1) % size
                delta_fg = f[j]*g[j]-f[i]*g[i]
                shifted = f[j]*(g[j]-g[i])+g[i]*(f[j]-f[i])
                polarized_twice = ((f[j]+f[i])*(g[j]-g[i])
                                   +(g[j]+g[i])*(f[j]-f[i]))
                ordinary = f[i]*(g[j]-g[i])+g[i]*(f[j]-f[i])
                assert delta_fg == shifted
                assert 2*delta_fg == polarized_twice
                ordinary_failures += int(delta_fg != ordinary)
                exact_checks += 1
    assert ordinary_failures
    return {'status': 'passed', 'finite_algebra': ranks,
            'shifted_and_polarized_edge_checks': exact_checks,
            'ordinary_pointwise_product_failures': ordinary_failures,
            'general_einstein_constraint_closure': 'not_tested'}


def engine_growth_case(degree, multiplier, denominator, steps=8):
    names = ('denominator', 'pair.p', 'pair.q')
    factors_d = ((names[0], ZERO, 'b'),)*degree
    terms = [(names[0], 3*multiplier, factors_d)]
    for name in names[1:]:
        terms.append((name, 3*multiplier,
                      ((names[0], ZERO, 'b'),)*(degree-1)
                      +((name, ZERO, 'b'),)))
    tensor = Tensor([GearType(name, label='audit') for name in names], terms,
                    strict_support=True)
    assert not tensor.support_violations()
    a = np.zeros((3, 27), dtype=object)
    b = np.zeros_like(a)
    a[2, :] = 1
    b[0, :] = denominator
    b[1, :] = denominator
    r = np.array([[(g+n) % 6 for n in range(27)] for g in range(3)], dtype=object)
    initial = State(3, a, b, r)
    current = initial
    engine = Engine(tensor)
    rows = []
    for tick in range(steps+1):
        d = int(current.b[0, 0])
        p, q = int(current.b[1, 0]), int(current.b[2, 0])
        p_old, q_old = int(current.a[1, 0]), int(current.a[2, 0])
        wronskian = p*q_old-p_old*q
        pair_gcd = gcd(p, q)
        assert wronskian == denominator
        assert wronskian % pair_gcd == 0
        assert pair_gcd <= abs(wronskian)
        assert d >= denominator**(degree**tick)
        rows.append({'tick': tick, 'denominator_bits': d.bit_length(),
                     'largest_retained_bits': max(abs(int(v)).bit_length()
                         for arr in (current.a, current.b, current.r) for v in arr.flat),
                     'pair_gcd': pair_gcd, 'wronskian': wronskian})
        if tick == steps:
            break
        old = current
        following = engine.step(old)
        # Scalar recurrence constructed directly; no production Engine RHS call.
        for node in range(27):
            d_old_current = int(old.b[0, node])
            amplification = multiplier*d_old_current**(degree-1)
            expected = [multiplier*d_old_current**degree-int(old.a[0, node]),
                        amplification*int(old.b[1, node])-int(old.a[1, node]),
                        amplification*int(old.b[2, node])-int(old.a[2, node])]
            assert all(int(following.b[g, node]) == expected[g] for g in range(3))
            assert expected[0] >= d_old_current**degree
        assert np.array_equal(following.a, old.b)
        assert np.array_equal(following.r, r)
        assert engine.inverse_step(following).same_as(old)
        current = following
    assert engine.rewind(current, steps).same_as(initial)
    return {'status': 'passed', 'degree': degree, 'multiplier': multiplier,
            'initial_denominator': denominator, 'channels': 3,
            'retained_integers_per_node': 9, 'nodes': 27, 'updates': steps,
            'all_six_remainders': True, 'full_rewind': True,
            'single_face_support': True, 'scalar_oracle_agreement': True,
            'rows': rows, 'einstein_model': False}


def normalization_collision():
    # Two legal retained states (same six-valued carry) collide if a and b
    # are divided by their common gcd without retaining the scale.
    states = ((2, 4, 0), (4, 8, 0))
    def normalize(state):
        old, now, carry = state
        factor = gcd(old, now)
        return old//factor, now//factor, carry
    assert states[0] != states[1]
    assert normalize(states[0]) == normalize(states[1])
    return {'status': 'passed', 'input_states': states,
            'colliding_output': normalize(states[0]),
            'claim': 'Unrecorded gcd normalization is not injective on general legal states.',
            'restricted_sector_normalization_no_go': False}


def clock_degree_control():
    # This counts formal degree, not a purported no-go for every scheduler.
    force_factors = ('x', 'y', 'z')
    gated_factors = ('gate',)+force_factors
    assert len(force_factors) == 3 and len(gated_factors) == 4
    return {'status': 'passed', 'original_degree': len(force_factors),
            'direct_boolean_gate_degree': len(gated_factors),
            'naive_gated_cubic_contract': 'failed',
            'alternative_clock_compilation': 'not_tested'}


def main():
    root_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                          text=True).strip()
    source_files = [Path(__file__), ROOT/'universe24/core/engine.py',
                    ROOT/'universe24/core/tensor.py',
                    ROOT/'validation/geometry/team48/refinement_integer_projective.py']
    report = {'scope': 'Targeted algebraic obstructions and constructive edge identities; no full GR model.',
              'local_base_sha': root_commit,
              'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in source_files},
              'derivation': derivation_control(),
              'growth_cases': [engine_growth_case(degree, multiplier, denominator)
                               for degree, multiplier, denominator in itertools.product((2, 3), (2, 3), (2, 5))],
              'normalization': normalization_collision(),
              'clock_degree': clock_degree_control(),
              'physical_acceptance': 'not_tested'}
    out = ROOT/'runs/research_eight/06_algebra_obstructions.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'artifact': str(out), 'cases': len(report['growth_cases']),
                      'edge_checks': report['derivation']['shifted_and_polarized_edge_checks'],
                      'ordinary_product_failures': report['derivation']['ordinary_pointwise_product_failures'],
                      'max_bits': max(row['largest_retained_bits']
                                      for case in report['growth_cases'] for row in case['rows']),
                      'physical_acceptance': report['physical_acceptance']}, indent=2))


if __name__ == '__main__':
    main()
