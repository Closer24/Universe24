"""Gauge-invariant matter clock port, not an operational clock acceptance test.

Run from the repository root. The existing massive protected44 law is unchanged.
The exact experiment compares rationally phase-rotated preparations through
the real Engine. Independent identities and a no-clock control use SymPy.
"""
from fractions import Fraction as F
from functools import partial
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

from universe24.core import Engine
from universe24.tests.test_migration import scalar_step
from validation.geometry.team48 import geometry_positive_pairs as positive
from validation.geometry.team48 import matter_charged as charged
from validation.geometry.team48 import matter_dust_square as square
from validation.geometry.team48.refinement_integer_projective import (
    compile_projective, prepare, readout,
)


def identities():
    x, y, px, py = sp.symbols('x y px py', real=True)
    c, s = sp.Rational(3, 5), sp.Rational(4, 5)
    xr, yr = c*x-s*y, s*x+c*y
    pxr, pyr = c*px-s*py, s*px+c*py
    invariants = (x*x+y*y, x*px+y*py, x*py-y*px)
    rotated = (xr*xr+yr*yr, xr*pxr+yr*pyr, xr*pyr-yr*pxr)
    assert all(sp.expand(a-b) == 0 for a, b in zip(invariants, rotated))
    assert sp.diff(invariants[0], x)*px+sp.diff(invariants[0], y)*py == 2*invariants[1]
    t, m, aa, bb = sp.symbols('t m A B', real=True)
    phi, chi = aa*sp.cos(m*t), bb*sp.sin(m*t)
    intensity = sp.expand_trig(phi**2+chi**2)
    expected = (aa**2+bb**2)/2+(aa**2-bb**2)*sp.cos(2*m*t)/2
    assert sp.trigsimp(intensity-expected) == 0
    assert sp.trigsimp(intensity.subs(bb, aa)) == aa**2
    # FLRW scalar normal-time equation adds K*pi. I is not an ideal universal clock.
    h = sp.symbols('H', real=True)
    radial_accel = 2*(px**2+py**2)-2*m**2*(x*x+y*y)-6*h*(x*px+y*py)
    assert sp.expand(radial_accel-2*(px**2+py**2+x*(-3*h*px-m*m*x)+y*(-3*h*py-m*m*y))) == 0
    return {'rational_rotation_invariant_I_S_charge': True,
            'normal_time_derivative_I_equals_2S': True,
            'elliptic_flat_intensity_frequency': '2*m',
            'circular_flat_intensity_constant': True,
            'expansion_changes_clock_dynamics': True,
            'scope': 'continuum/flat algebra; not a lattice proper-clock theorem'}


def rotate(fields, values):
    answer = values.copy()
    pairs = [('phi', 'chi'), ('Pi_phi', 'Pi_chi')]
    pairs += [(f'Xi_phi{j}', f'Xi_chi{j}') for j in range(3)]
    for left, right in pairs:
        i, j = fields.index(left), fields.index(right)
        answer[i] = F(3, 5)*values[i]-F(4, 5)*values[j]
        answer[j] = F(4, 5)*values[i]+F(3, 5)*values[j]
    return answer


def actual44():
    fields = positive.replace_fields(square.FIELDS_CHARGED)
    builder = partial(positive.equations, fermi_equations=square.equations,
                      base_equations=charged.equations, mass_squared=1, coupling=1)
    program = compile_projective(fields, builder, dt=F(1, 64), degree=3)
    current = np.full((len(fields), 27), F(0), dtype=object)
    for axis in range(3):
        current[fields.index(f'diag_p{axis}')] = F(1)
        current[fields.index(f'K{axis}{axis}')] = F(-1)
    current[fields.index('phi')] = F(2)
    current[fields.index('dust_amplitude')] = F(1)
    carry = np.array([int(i % 6) for i in range(44*27)], dtype=object).reshape(44, 27)
    seeds = [prepare(program, v, L=3, denominator=100, remainders=carry)
             for v in (current, rotate(fields, current))]
    for seed in seeds:
        for axis in range(3):
            seed.a[1+fields.index(f'diag_q{axis}')] = 1
    states = [s.copy() for s in seeds]
    engine = Engine(program.tensor)
    bit_counts = []
    for tick in range(4):
        left, right = (readout(program, s) for s in states)
        assert np.array_equal(rotate(fields, left), right)
        for name in fields:
            if name not in ('phi', 'chi', 'Pi_phi', 'Pi_chi') and not name.startswith('Xi_'):
                assert np.array_equal(left[fields.index(name)], right[fields.index(name)])
        for value in (left, right):
            phi, chi, pi, pj = (value[fields.index(name)] for name in ('phi', 'chi', 'Pi_phi', 'Pi_chi'))
            assert np.all(phi*pj-chi*pi == 0)
        bit_counts.append(max(s.max_abs().bit_length() for s in states))
        if tick == 3:
            break
        for i, state in enumerate(states):
            following = engine.step(state)
            assert following.same_as(scalar_step(program.tensor, state))
            assert np.array_equal(following.r, carry)
            assert engine.inverse_step(following).same_as(state)
            states[i] = following
    assert all(engine.rewind(state, 3).same_as(seed) for state, seed in zip(states, seeds))
    return {'channels': program.tensor.G, 'retained_integers_per_node': 3*program.tensor.G,
            'mass_squared': 1, 'dt': str(program.dt), 'sites': 27, 'updates': 3,
            'monomials': len(program.tensor), 'tensor_sha256': program.tensor.fingerprint,
            'single_face_violations': len(program.tensor.support_violations()),
            'global_rational_U1_rotation_equivariance': True,
            'same_geometry_dust_Maxwell': True, 'all_remainders_checked': True,
            'independent_scalar_oracle': True, 'exact_rewind': True,
            'maximum_state_bits_seed_then_updates': bit_counts,
            'moving_clock_gate': 'not_tested', 'click_only_clock_gate': 'not_tested',
            'redshift_gate': 'not_tested', 'general_Einstein_gate': 'not_tested',
            'scope': 'global phase equivariance; not local lattice gauge symmetry or physical acceptance'}


def main():
    report = {'identities': identities(), 'actual44': actual44(),
              'allocation': {'reuse_existing_matter': 44,
                             'direct_extra_real_scalar_with_3_gradients': 49,
                             'same_extra_scalar_with_unprotected41': 46},
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = Path('runs/research_eight/05_clock_port.json')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
