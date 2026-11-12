"""Independent homogeneous constraint diagnostic for the shared massive45 run.

This audit deliberately preserves a physical failure: the first Engine update
injects an exactly known Hamiltonian defect even from constrained initial data.
No state is repaired, normalized or projected by this passive diagnostic.
"""
from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine
from validation.geometry.team48 import refinement_integer_projective as projective


def reduced_rhs(values, mass_squared=1):
    """Independent spatially-flat FLRW reduction in the declared -+++ gauge.

    B is the inverse scale factor and K_ab=k delta_ab. This formula retains
    the off-constraint K equation; replacing it with the Friedmann-constrained
    Raychaudhuri equation would incorrectly hide the very defect being tested.
    """
    B, k, phi, pi, dust = values
    return (k*B, 3*k*k-F(1, 2)*(mass_squared*phi*phi+dust*dust),
            pi, 3*k*pi-mass_squared*phi, F(3, 2)*k*dust)


def hamiltonian(values, mass_squared=1):
    _, k, phi, pi, dust = values
    return 6*k*k-pi*pi-mass_squared*phi*phi-2*dust*dust


def reduced_values(fields):
    """Read one node only after verifying the homogeneous/isotropic sector."""
    for row in fields.values():
        assert all(value == row[0] for value in row), 'not homogeneous'
    for axis in range(3):
        assert fields[f'B{axis}{axis}'][0] == fields['B00'][0]
        assert fields[f'K{axis}{axis}'][0] == fields['K00'][0]
    active = {*(f'B{i}{i}' for i in range(3)), *(f'K{i}{i}' for i in range(3)),
              'phi', 'Pi_phi', 'dust_amplitude'}
    assert all(row[0] == 0 for key, row in fields.items() if key not in active)
    return tuple(F(fields[name][0]) for name in
                 ('B00', 'K00', 'phi', 'Pi_phi', 'dust_amplitude'))


def continuum_identity():
    B, k, phi, pi, dust, mass_squared = sp.symbols('B k phi pi dust m2')
    values = (B, k, phi, pi, dust)
    constraint = hamiltonian(values, mass_squared)
    derivative = sum(sp.diff(constraint, x)*dx for x, dx in
                     zip(values, reduced_rhs(values, mass_squared)))
    assert sp.expand(derivative-6*k*constraint) == 0
    h = sp.Symbol('h')
    defects = {}
    for name, initial, m2, expected in (
        ('massive', (1, -1, 2, 0, 1), 1, -7*h*h),
        ('massless', (1, -1, 0, 2, 1), 0, -3*h*h),
        ('flat', (1, 0, 0, 0, 0), 1, 0)):
        assert hamiltonian(initial, m2) == 0
        after = tuple(x+h*dx for x, dx in zip(initial, reduced_rhs(initial, m2)))
        defect = sp.expand(hamiltonian(after, m2))
        assert sp.expand(defect-expected) == 0
        defects[name] = str(defect)
    return {'homogeneous_continuum_identity': 'dC/dt = 6 k C',
            'first_Euler_step_defects': defects,
            'constraint_added_rhs_cannot_change_this_first_step': True}


def audit_case(name='massive', *, steps=4, final_time=F(1, 8), L=3):
    # Shared builder/preparer: no second tensor or physical runtime is added.
    from .run import build_program, prepare_seed, fields_readout
    m2 = 0 if name == 'massless' else 1
    dt = F(final_time, steps)
    program = build_program(dt=dt, dx=F(1, 4), mass_squared=m2)
    seed = prepare_seed(program, L=L, denominator=32)
    if name in ('massless', 'flat'):
        physical = projective.readout(program, seed)
        physical[:] = F(0)
        for axis in range(3):
            physical[program.fields.index(f'B{axis}{axis}')] = F(1)
            physical[program.fields.index(f'K{axis}{axis}')] = F(-1 if name == 'massless' else 0)
        if name == 'massless':
            physical[program.fields.index('Pi_phi')] = F(2)
            physical[program.fields.index('dust_amplitude')] = F(1)
        seed = projective.prepare(program, physical, L=L, denominator=32,
                                  remainders=seed.r)
    engine, state = Engine(program.tensor), seed
    decode = lambda value: dict(zip(program.fields, fields_readout(program, value)))
    initial = reduced_values(decode(seed))
    assert hamiltonian(initial, m2) == 0
    previous = None
    defects, positive_metric, max_bits = [], True, 0
    for step in range(steps):
        values = reduced_values(decode(state))
        euler = tuple(x+dt*dx for x, dx in zip(values, reduced_rhs(values, m2)))
        after = engine.step(state)
        D_old, D_next = int(state.a[0, 0]), int(after.b[0, 0])
        epsilon = F(D_old, D_next)
        expected = euler if previous is None else tuple(
            x+epsilon*(x-old) for x, old in zip(euler, previous))
        actual = reduced_values(decode(after))
        assert actual == expected, 'independent homogeneous ratio recurrence'
        defect = hamiltonian(actual, m2)
        if step == 0:
            coefficient = {'massive': -7, 'massless': -3, 'flat': 0}[name]
            assert defect == coefficient*dt*dt
        assert engine.inverse_step(after).same_as(state)
        assert np.array_equal(after.r, seed.r)
        defects.append(defect)
        positive_metric = positive_metric and actual[0] != 0
        max_bits = max(max_bits, after.max_abs().bit_length())
        previous, state = values, after
    assert engine.rewind(state, steps).same_as(seed)
    if name == 'flat':
        assert all(value == 0 for value in defects)
    return {'case': name, 'channels': program.tensor.G,
            'tensor_sha256': program.tensor.fingerprint,
            'steps': steps, 'nodes': seed.N, 'dt': str(dt),
            'final_time': str(final_time), 'first_constraint': str(defects[0]),
            'final_constraint_abs': float(abs(defects[-1])),
            'first_constraint_exact': True,
            'independent_reduced_recurrence_exact': True,
            'all_remainders_and_complete_rewind': True,
            'metric_nondegenerate_on_this_run': bool(positive_metric),
            'maximum_retained_bits': max_bits,
            'exact_discrete_constraint_preservation': 'passed' if name == 'flat' else 'failed'}


def audit():
    cases = [audit_case(name) for name in ('massive', 'massless', 'flat')]
    refinement = [audit_case('massive', steps=steps, L=3) for steps in (2, 4, 8)]
    errors = [row['final_constraint_abs'] for row in refinement]
    return {'schema': 'universe24/geodesic-board/constraints/1',
            'scope': 'same-law homogeneous diagnostic, not general Einstein convergence',
            'algebra': continuum_identity(), 'controls': cases,
            'fixed_time_refinement': refinement,
            'fixed_time_constraint_decreases': all(a > b for a, b in zip(errors, errors[1:])),
            'spatial_convergence': 'not_tested',
            'nonlinear_discrete_constraint_gate': 'failed',
            'next_required_change': 'constraint-compatible temporal encoding; vanishing constraint RHS additions alone cannot remove the first-step defect'}


def main():
    result = audit()
    output = Path('runs/geodesic-board/constraint-audit.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
