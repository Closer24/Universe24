"""Independent exact arithmetic audits; run with python -m <this module>."""
from fractions import Fraction
from functools import partial as bind
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine
from universe24.core.lattice import lattice
from universe24.algebra.frame_equations import FIELDS as VACUUM_FIELDS, equations as vacuum_equations
from universe24.layers.frame48 import compile_frame48
from universe24.prepare.frame48 import prepare as prepare_frame48
from universe24.tests.test_migration import scalar_step

from . import integer_division as division
from .integer_sign_lift import compile_quadratic, prepare, physical_slices, invariant_summary
from . import matter_equations as matter
from . import geometry_triangular as triangular


def physical_increment(program, builder, values, lat):
    """Evaluate the original physical RHS, independently of tensor terms."""
    fields = dict(zip(program.fields, values))

    def derivative(name, axis):
        plus = tuple(int(i == axis) for i in range(3))
        minus = tuple(-v for v in plus)
        return Fraction(1, 2)/program.dx*(fields[name][lat.shift_index(plus)]
                                          -fields[name][lat.shift_index(minus)])

    result = builder(fields, derivative)
    rhs = result[0] if isinstance(result, tuple) else result
    rows = [np.broadcast_to(2*program.dt*rhs[name], (lat.N,)) for name in program.fields]
    array = np.array(rows, dtype=object)
    assert all(getattr(v, 'denominator', 1) == 1 for v in array.flat)
    return np.array([int(v) for v in array.flat], dtype=object).reshape(array.shape)


def generic_equations(fields, derivative):
    x, y = fields['x'], fields['y']
    return {'x': 2+3*x-x*x+x*derivative('y', 0),
            'y': -1-2*y+x*y+derivative('x', 2)}


def check_encoding(name, fields, builder, *, phases=((1, 1),), bigint=False):
    program = compile_quadratic(fields, builder)
    engine = Engine(program.tensor)
    lat = lattice(3)
    rng = np.random.default_rng(478)
    previous = rng.integers(-2, 3, size=(len(fields), lat.N)).astype(object)
    current = rng.integers(-2, 3, size=previous.shape).astype(object)
    if bigint:
        previous[0, 0] = -(1 << 83)
        current[-1, 3] = 1 << 97
    for phase in phases:
        remainders = rng.integers(0, 6, size=(program.tensor.G, lat.N)).astype(object)
        initial = prepare(program, previous, current, L=3, phase=phase, remainders=remainders)
        state = oracle = initial
        old, now = previous, current
        for _ in range(3):
            following = old+physical_increment(program, builder, now, lat)
            state = engine.step(state)
            oracle = scalar_step(program.tensor, oracle)
            assert state.same_as(oracle), (name, 'scalar oracle')
            decoded_old, decoded_now = physical_slices(program, state)
            assert np.array_equal(decoded_old, now), (name, 'previous slice')
            assert np.array_equal(decoded_now, following), (name, 'physical RHS')
            assert np.array_equal(state.r, remainders), (name, 'carry changed')
            old, now = now, following
        assert engine.rewind(state, 3).same_as(initial), (name, 'rewind')
    return {'name': name, **invariant_summary(program), 'monomials': len(program.tensor),
            'all_tests_passed': True, 'tested_sign_phases': [list(p) for p in phases],
            'arbitrary_signed_data_not_constraint_prepared': True,
            'independent_scalar_oracle': True, 'original_rhs_oracle': True,
            'complete_state_rewind': True, 'nonzero_remainders_preserved': True}


def check_frame48_equivalence():
    program = compile_quadratic(VACUUM_FIELDS, vacuum_equations)
    old_program = compile_frame48()
    rng = np.random.default_rng(908)
    previous = rng.integers(-2, 3, size=(24, 27)).astype(object)
    current = rng.integers(-2, 3, size=(24, 27)).astype(object)
    state = prepare(program, previous, current, L=3)
    old_state = prepare_frame48(old_program, previous, current, L=3)
    engine, old_engine = Engine(program.tensor), Engine(old_program.tensor)
    for _ in range(5):
        actual_previous, actual_current = physical_slices(program, state)
        assert np.array_equal(actual_previous, old_state.b[:24])
        assert np.array_equal(actual_current, old_state.b[24:])
        state, old_state = engine.step(state), old_engine.step(old_state)
    return {'five_slice_comparisons_passed': True, 'old_channels': 48,
            'new_channels': 25, 'encoded_physical_map_identical': True,
            'complete_counter_histories_identical': False}


def check_division():
    tensor = division.division_tensor()
    engine = Engine(tensor)
    values = [-(10**70)-1, -100, -10, -1, 0, 1, 10, 100, 10**70+1]
    values = (values*3)[:27]
    initial = division.prepare(values)
    state = oracle = initial
    initial_values = np.array(values, dtype=object).reshape(1, 27)
    for tick in range(81):
        decoded = division.readout(state)
        assert np.array_equal(decoded.quotient, initial_values//3**tick)
        a, b, r = division.coordinate_inverse(decoded.quotient, decoded.history, decoded.digit)
        assert np.array_equal(a, state.a) and np.array_equal(b, state.b) and np.array_equal(r, state.r)
        if tick:
            inverse = division.coordinate_inverse_step(decoded)
            assert all(np.array_equal(getattr(inverse, name), getattr(previous, name))
                       for name in ('quotient', 'history', 'digit'))
        previous = decoded
        if tick < 80:
            state = engine.step(state)
            oracle = scalar_step(tensor, oracle)
            assert state.same_as(oracle)
    assert engine.rewind(state, 80).same_as(initial)
    return {'channels': 1, 'integer_entries_per_node': 3, 'clock_channels': 0,
            'scratch_channels': 0, 'old_a_reads': [], 'input_degree': 1,
            'single_edge_violations': len(tensor.support_violations()),
            'steps': 80, 'nodes': 27, 'signed_inputs_up_to_digits': 71,
            'identity': 'z_k=floor(N/3**k)', 'all_tests_passed': True,
            'complete_state_rewind': True, 'independent_scalar_oracle': True,
            'independent_coordinate_inverse': True,
            'bounded_channel_count': True, 'bounded_bit_memory': False,
            'autonomous_quotient_handoff_implemented': False,
            'coupled_sourced_einstein_refinement_established': False}


def check_rejections():
    checks = {}
    for dt, dx in ((Fraction(1, 4), Fraction(1, 4)), (Fraction(1, 8), 1)):
        try:
            compile_quadratic(VACUUM_FIELDS, vacuum_equations, dt=dt, dx=dx)
        except ValueError as error:
            checks[f'dt={dt},dx={dx}'] = str(error)
        else:
            raise AssertionError('Unsupported fractional coefficient was silently accepted')
    return checks


def audit():
    fermi_maxwell = bind(matter.equations, maxwell=True)
    triangular_matter = bind(triangular.equations, fermi_equations=matter.equations)
    triangular_maxwell = bind(triangular.equations, fermi_equations=matter.equations, maxwell=True)
    scalar_fields = matter.SCALAR_FIELDS+matter.DUST_FIELDS
    models = [
        ('vacuum25', VACUUM_FIELDS, vacuum_equations),
        ('matter36', matter.FIELDS, matter.equations),
        ('matter_maxwell42', matter.FIELDS_WITH_MAXWELL, fermi_maxwell),
        ('triangular_matter32', triangular.FIELDS+scalar_fields, triangular_matter),
        ('triangular_matter_maxwell38', triangular.FIELDS+scalar_fields+matter.MAXWELL_FIELDS, triangular_maxwell),
    ]
    programs = [check_encoding(name, fields, builder) for name, fields, builder in models]
    programs.append(check_encoding('mixed_degree_bigint', ('x', 'y'), generic_equations,
                                   phases=((1, 1), (1, -1), (-1, 1), (-1, -1)), bigint=True))
    files = [Path(__file__), Path(__file__).with_name('integer_sign_lift.py'),
             Path(__file__).with_name('integer_division.py'),
             Path(matter.__file__), Path(triangular.__file__),
             Path('universe24/core/engine.py'), Path('universe24/algebra/frame_equations.py')]
    return {'status': 'exact_encoding_and_division_tests_passed',
            'programs': programs, 'frame48_comparison': check_frame48_equivalence(),
            'division': check_division(), 'expected_refinement_rejections': check_rejections(),
            'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
            'full_einstein_physical_acceptance': False}


if __name__ == '__main__':
    result = audit()
    output = Path('runs/team48/integer/audit.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'program_channels': {
        row['name']: row['channels'] for row in result['programs']},
        'division_channels': result['division']['channels'], 'output': str(output)}, indent=2))
