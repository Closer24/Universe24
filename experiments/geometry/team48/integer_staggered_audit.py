"""Actual Engine checks for the restricted cubic sign encoding and44 gears."""
from functools import partial as bind
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine
from universe24.core.lattice import lattice
from universe24.tests.test_migration import scalar_step

from . import geometry_positive_pairs as geometry
from . import matter_charged as charged
from . import matter_dust_square as square
from .integer_audit import physical_increment
from . import integer_staggered as staggered


def candidate():
    fields = geometry.replace_fields(square.FIELDS_CHARGED)
    sourced = bind(square.equations, base_equations=charged.equations)
    equations = bind(geometry.equations, fermi_equations=sourced)
    return staggered.compile_staggered(fields, equations,
                                      phase_offsets=geometry.phase_offsets(fields)), equations


def generic_equations(fields, derivative):
    x, y = fields['x'], fields['y']
    return {'x': 1+2*y+x*y+x*x*y+x*x*derivative('y', 0),
            'y': -2+3*x+x*y-x*y*y+y*y*derivative('x', 2)}


def check_rejections():
    for offset in (0, 1):
        try:
            staggered.compile_staggered(('x',), lambda f, d: {'x': f['x']**3},
                                         phase_offsets={'x': offset})
        except ValueError as error:
            assert 'cubic' in str(error)
        else:
            raise AssertionError('A self-cubic has no legal phase assignment')
    return {'self_cubic_rejected_for_both_offsets': True}


def check_generic():
    program = staggered.compile_staggered(('x', 'y'), generic_equations,
                                          phase_offsets={'x': 0, 'y': 1})
    engine = Engine(program.tensor)
    lat, rng = lattice(3), np.random.default_rng(763)
    for phase in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        old, now = [rng.integers(-2, 3, size=(2, 27)).astype(object) for _ in range(2)]
        old[0, 0], now[1, 4] = -(1 << 61), 1 << 67
        carry = rng.integers(0, 6, size=(3, 27)).astype(object)
        initial = staggered.prepare(program, old, now, L=3, phase=phase, remainders=carry)
        state = oracle = initial
        for _ in range(3):
            following = old+physical_increment(program, generic_equations, now, lat)
            state, oracle = engine.step(state), scalar_step(program.tensor, oracle)
            assert state.same_as(oracle)
            actual_old, actual_now = staggered.physical_slices(program, state)
            assert np.array_equal(actual_old, now) and np.array_equal(actual_now, following)
            assert np.array_equal(state.r, carry)
            old, now = now, following
        assert engine.rewind(state, 3).same_as(initial)
    return {'all_degrees_zero_through_three_tested': True,
            'all_four_phase_sectors': True, 'signed_bigints': True,
            'spatial_stencil_and_nonzero_carries': True,
            'physical_rhs_and_scalar_oracles': True, 'complete_rewind': True}


def pair_diagnostics(program, old, now):
    previous, current = dict(zip(program.fields, old)), dict(zip(program.fields, now))
    areas = np.array(geometry.wronskians(previous, current), dtype=object)
    diagonal = np.array([current[f'diag_p{a}']**2+current[f'diag_q{a}']**2 for a in range(3)], dtype=object)
    determinant = diagonal[0]*diagonal[1]*diagonal[2]
    return areas, diagonal, determinant


def check_candidate():
    program, builder = candidate()
    assert program.tensor.G == 44
    assert program.tensor.rank-1 == 3
    assert not program.tensor.support_violations()
    engine = Engine(program.tensor)
    lat, rng = lattice(3), np.random.default_rng(4439)
    previous, current = [rng.integers(-1, 2, size=(43, 27)).astype(object) for _ in range(2)]
    for axis in range(3):
        p, q = (program.fields.index(f'diag_{label}{axis}') for label in ('p', 'q'))
        previous[p], previous[q], current[p], current[q] = 1, 1, 1, 0
    initial_areas, _, _ = pair_diagnostics(program, previous, current)
    assert np.all(initial_areas == 1)
    minimum_diagonal, minimum_determinant = None, None
    for phase in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        carry = rng.integers(0, 6, size=(44, 27)).astype(object)
        initial = staggered.prepare(program, previous, current, L=3, phase=phase, remainders=carry)
        state = oracle = initial
        old, now = previous, current
        for tick in range(4):
            areas, diagonal, determinant = pair_diagnostics(program, old, now)
            assert np.array_equal(areas, (-1)**tick*initial_areas)
            assert np.all(diagonal > 0) and np.all(determinant > 0)
            md, mt = min(diagonal.flat), min(determinant.flat)
            minimum_diagonal = md if minimum_diagonal is None else min(minimum_diagonal, md)
            minimum_determinant = mt if minimum_determinant is None else min(minimum_determinant, mt)
            if tick < 3:
                following = old+physical_increment(program, builder, now, lat)
                state, oracle = engine.step(state), scalar_step(program.tensor, oracle)
                assert state.same_as(oracle)
                actual_old, actual_now = staggered.physical_slices(program, state)
                assert np.array_equal(actual_old, now) and np.array_equal(actual_now, following)
                assert np.array_equal(state.r, carry)
                old, now = now, following
        assert engine.rewind(state, 3).same_as(initial)
    return {**staggered.invariant_summary(program), 'monomials': len(program.tensor),
            'charged_scalar_maxwell_signed_square_dust': True,
            'parameters': {'dt': 1, 'dx': 1, 'mass_squared': 1, 'coupling': 1},
            'all_four_phase_sectors': True, 'steps_per_sector': 3, 'nodes': 27,
            'independent_scalar_oracle': True, 'original_cubic_rhs_oracle': True,
            'nonzero_carries_preserved': True, 'complete_rewind': True,
            'all_three_wronskians_flip_exactly': True,
            'minimum_positive_diagonal': str(minimum_diagonal),
            'minimum_positive_det_B': str(minimum_determinant),
            'no_hidden_or_reserved_channels_in_count': True,
            'seed_has_nonzero_computational_second_mode': True,
            'seed_is_a_continuum_einstein_solution_pair': False,
            'builder_chain_rule_constraints_used_as_discrete_diagnostics': False,
            'generic_hamiltonian_momentum_constraint_preservation': False,
            'normalized_wronskian_vanishes_under_controlled_refinement': False}


def audit():
    paths = [Path(__file__), Path(staggered.__file__), Path(geometry.__file__),
             Path(square.__file__), Path(charged.__file__),
             Path('experiments/geometry/team48/matter_equations.py'),
             Path('experiments/geometry/team48/geometry_triangular.py'),
             Path('universe24/core/engine.py')]
    return {'status': 'actual44_channel_cubic_encoding_and_positive_pair_invariant_passed',
            'generic_compiler': check_generic(), 'rejections': check_rejections(),
            'candidate44': check_candidate(),
            'source_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
            'full_einstein_solution_claim': False}


if __name__ == '__main__':
    result = audit()
    output = Path('runs/team48/integer/staggered_audit.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'channels': result['candidate44']['channels'],
                      'input_degree': result['candidate44']['input_degree'], 'output': str(output)}, indent=2))
