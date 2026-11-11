"""Compare PR39's actual70-channel law with its exact36-channel encoding.

This tests all35 physical fields, after explicit renaming, and distinguishes
physical-trajectory equality from equality of the different retained states.
"""
from functools import partial as bind
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.algebra import frame_matter as pr39
from universe24.core import Engine
from universe24.layers.frame_matter import compile_matter_frame
from universe24.prepare.frame_matter import prepare as prepare_pair
from universe24.tests.test_migration import scalar_step

from . import geometry_triangular as triangular
from . import matter_charged as charged
from . import matter_dust_square as square
from .integer_audit import check_encoding
from .integer_sign_lift import compile_quadratic, prepare, physical_slices, invariant_summary


PR39_HEAD = '35344a1ba5c12c857404115e893911411ece7d35'


def renamed(name):
    if name == 'Pi':
        return 'Pi_phi'
    if name in ('Q0', 'Q1', 'Q2'):
        return f'Psi_phi{name[-1]}'
    if name in ('W0', 'W1', 'W2'):
        return f'Psi_chi{name[-1]}'
    return name


def check_algebra():
    fields = {name: sp.Symbol(name) for name in square.FIELDS}
    jets = {(name, axis): sp.Symbol(f'd{axis}_{name}') for name in square.FIELDS for axis in range(3)}
    rhs, constraints, _ = square.equations(fields, lambda name, axis: jets[name, axis])
    original, original_constraints, _ = pr39.equations(
        {name: fields[renamed(name)] for name in pr39.FIELDS},
        lambda name, axis: jets[renamed(name), axis], mass_squared=1)
    assert tuple(renamed(name) for name in pr39.FIELDS) == square.FIELDS
    assert all(sp.expand(original[name]-rhs[renamed(name)]) == 0 for name in pr39.FIELDS)
    for name in ('H', 'M0', 'M1', 'M2'):
        assert sp.expand(original_constraints[name]-constraints[name]) == 0
    return {'rhs_fields_compared': 35, 'all_rhs_identical_after_renaming': True,
            'hamiltonian_and_momentum_constraints_identical': True,
            'renaming': {name: renamed(name) for name in pr39.FIELDS if name != renamed(name)}}


def check_trajectories():
    old_program = compile_matter_frame(dt=1, dx=1, mass_squared=1)
    program = compile_quadratic(square.FIELDS, square.equations, dt=1, dx=1)
    old_engine, engine = Engine(old_program.tensor), Engine(program.tensor)
    rng = np.random.default_rng(3936)
    previous = rng.integers(-2, 3, size=(35, 27)).astype(object)
    current = rng.integers(-2, 3, size=(35, 27)).astype(object)
    previous[24, 0], current[25, 1] = -(1 << 73), 1 << 81
    phases = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    old_carry = (np.arange(70*27).reshape(70, 27) % 6).astype(object)
    carry = ((np.arange(36*27).reshape(36, 27)+2) % 6).astype(object)
    for phase in phases:
        old_initial = prepare_pair(old_program, previous, current, L=3, remainders=old_carry)
        initial = prepare(program, previous, current, L=3, phase=phase, remainders=carry)
        old_state = old_oracle = old_initial
        state = oracle = initial
        for tick in range(4):
            decoded_old, decoded_now = physical_slices(program, state)
            assert np.array_equal(decoded_old, old_state.b[:35]), (phase, tick, 'previous35')
            assert np.array_equal(decoded_now, old_state.b[35:]), (phase, tick, 'current35')
            assert np.array_equal(old_state.r, old_carry)
            assert np.array_equal(state.r, carry)
            if tick < 3:
                old_state, state = old_engine.step(old_state), engine.step(state)
                old_oracle = scalar_step(old_program.tensor, old_oracle)
                oracle = scalar_step(program.tensor, oracle)
                assert old_state.same_as(old_oracle)
                assert state.same_as(oracle)
        assert old_engine.rewind(old_state, 3).same_as(old_initial)
        assert engine.rewind(state, 3).same_as(initial)
    return {'old_channels': 70, 'new_channels': 36,
            'old_integer_entries_per_node': 210, 'new_integer_entries_per_node': 108,
            'parameters': {'dt': 1, 'dx': 1, 'mass_squared': 1},
            'all_four_phase_sectors_tested': True, 'steps_per_sector': 3,
            'all35_fields_both_slices_identical': True,
            'nonzero_carries_retained_in_both_encodings': True,
            'independent_scalar_oracle_for_both_encodings': True,
            'signed_bigint_initial_data': True, 'both_complete_states_rewind': True,
            'different_encodings_have_identical_complete_states': False,
            'invariant_summary': invariant_summary(program)}


def audit():
    charged_square = bind(square.equations, base_equations=charged.equations)
    reduced_fields = tuple(name for name in square.FIELDS_CHARGED
                           if name not in triangular.ZERO_FIELDS and name not in triangular.ALIASES)
    reduced_builder = bind(triangular.equations, fermi_equations=charged_square)
    extensions = [
        check_encoding('charged_square45', square.FIELDS_CHARGED, charged_square),
        check_encoding('triangular_charged_square41', reduced_fields, reduced_builder),
    ]
    paths = [Path(__file__), Path(pr39.__file__), Path(square.__file__), Path(charged.__file__),
             Path(triangular.__file__), Path('experiments/geometry/team48/integer_sign_lift.py'),
             Path('universe24/layers/frame_matter.py'), Path('universe24/prepare/frame_matter.py'),
             Path('universe24/core/engine.py')]
    return {'status': 'PR39_exact70_to36_comparison_passed', 'reviewed_pr39_head': PR39_HEAD,
            'algebra': check_algebra(), 'trajectories': check_trajectories(),
            'square_dust_extensions': extensions,
            'source_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
            'general_einstein_constraints_and_convergence_proved': False}


if __name__ == '__main__':
    result = audit()
    output = Path('runs/team48/integer/pr39_comparison.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'old_channels': 70, 'new_channels': 36,
                      'extension_channels': [entry['channels'] for entry in result['square_dust_extensions']],
                      'output': str(output)}, indent=2))
