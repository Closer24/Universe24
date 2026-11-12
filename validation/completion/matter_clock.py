"""Massive clock diagnostic on the common full45 law; no retained detector.

Run ``python -m validation.completion.matter_clock``. The longer dt=1/4
experiment is explicitly a different immutable tensor/protocol from the
shared dt=1/64 candidate. Neither trajectory establishes a proper-time clock.
"""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine
from universe24.system.bundle import canonical_bytes
from universe24.tests.test_migration import scalar_step
from validation.geometry.team48.refinement_integer_projective import prepare, readout
from validation.completion import common45, formulation

ROOT = Path(__file__).resolve().parents[2]


def state_digest(state):
    """Same complete-seed canonical hash as the common runtime handoff."""
    return hashlib.sha256(canonical_bytes(state.to_dict())).hexdigest()


def rotate(fields, values):
    answer = values.copy()
    pairs = [('phi', 'chi'), ('Pi_phi', 'Pi_chi')]
    pairs += [(f'Xi_phi{j}', f'Xi_chi{j}') for j in range(3)]
    for left, right in pairs:
        i, j = fields.index(left), fields.index(right)
        answer[i] = F(3, 5)*values[i]-F(4, 5)*values[j]
        answer[j] = F(4, 5)*values[i]+F(3, 5)*values[j]
    return answer


def observables(values):
    x, y, px, py = (values[n] for n in ('phi', 'chi', 'Pi_phi', 'Pi_chi'))
    return {'I': x*x+y*y, 'S': x*px+y*py, 'P2': px*px+py*py,
            'charge': x*py-y*px}


def continuum_identities():
    """Derive identities from this actual massive builder, with no gradients."""
    x, y, px, py, k, m = sp.symbols('x y px py K m', real=True)
    values = {name: sp.Integer(0) for name in formulation.FIELDS}
    for a in range(3):
        values[f'B{a}{a}'] = sp.Integer(1)
        values[f'K{a}{a}'] = k/3
    values.update(phi=x, chi=y, Pi_phi=px, Pi_chi=py)
    # Builder mass is a static rational parameter, so prove at the specified m=1.
    rhs, _, _ = formulation.equations(values, lambda *_: sp.Integer(0), mass_squared=1)
    variables = (x, y, px, py)
    velocity = tuple(rhs[n] for n in ('phi', 'chi', 'Pi_phi', 'Pi_chi'))
    derivative = lambda f: sp.expand(sum(sp.diff(f, z)*v for z, v in zip(variables, velocity)))
    invariant = observables(values)
    ii, ss, pp, charge = (invariant[n] for n in ('I', 'S', 'P2', 'charge'))
    E, quadrature_real, R = ii+pp, ii-pp, -2*ss
    assert sp.expand(derivative(ii)-2*ss) == 0
    assert sp.expand(derivative(ss)-(pp+k*ss-ii)) == 0
    assert sp.expand(derivative(charge)-k*charge) == 0
    assert sp.expand(quadrature_real**2+R*R-E*E+4*charge*charge) == 0
    # Twice the phase derivative: (Q R' - R Q')/(Q²+R²).
    assert sp.expand(quadrature_real*derivative(R)-R*derivative(quadrature_real)
                     -2*(quadrature_real**2+R*R)-k*E*R) == 0
    assert sp.expand(E*E-4*ss*ss-(quadrature_real**2+4*charge*charge)) == 0
    # The general-m identity follows directly from phi'=Pi, Pi'=K Pi-m² phi.
    general_velocity = (px, py, k*px-m*m*x, k*py-m*m*y)
    dg = lambda f: sp.expand(sum(sp.diff(f, z)*v for z, v in zip(variables, general_velocity)))
    Eg, Qg, Rg = m*m*ii+pp, m*m*ii-pp, -2*m*ss
    assert sp.expand(Qg*dg(Rg)-Rg*dg(Qg)-2*m*(Qg*Qg+Rg*Rg)-k*Eg*Rg) == 0
    assert sp.expand(Qg*Qg+Rg*Rg-Eg*Eg+4*m*m*charge*charge) == 0
    # Flat continuum controls, not self-consistent nonzero-source flat solutions.
    t, aa, bb = sp.symbols('tau A B', real=True)
    intensity = aa**2*sp.cos(m*t)**2+bb**2*sp.sin(m*t)**2
    expected = (aa**2+bb**2)/2+(aa**2-bb**2)*sp.cos(2*m*t)/2
    assert sp.trigsimp(intensity-expected) == 0
    assert sp.trigsimp(intensity.subs(bb, aa)-aa**2) == 0
    # Pointwise simultaneous SO(2) action leaves diagnostics invariant.
    rotated = dict(values)
    rotated.update(phi=F(3, 5)*x-F(4, 5)*y, chi=F(4, 5)*x+F(3, 5)*y,
                   Pi_phi=F(3, 5)*px-F(4, 5)*py, Pi_chi=F(4, 5)*px+F(3, 5)*py)
    assert all(sp.expand(invariant[n]-observables(rotated)[n]) == 0 for n in invariant)
    return {'same_builder_mass1_exact_identities': True,
            'pointwise_covariant_SO2_invariants': True,
            'I_derivative': '2*S', 'charge_derivative': 'trK*charge',
            'phase': 'theta=arg(Q+iR)/2; E=m²I+P², Q=m²I-P², R=-2mS',
            'phase_derivative': 'm+trK*E*R/(2*(Q²+R²))',
            'neutral_radial_phase_derivative': 'm-trK*m*S/E',
            'neutral_radial_domain': 'm>0, E>0, zero charge, homogeneous covariant gradients; |trK|<2m ensures strict monotonicity',
            'proper_time_relation': 'theta(tau2)-theta(tau1)=m*(tau2-tau1)-integral(trK*m*S/E d_tau) in the radial sector',
            'flat_non_circular_intensity_period': 'pi/m',
            'flat_circular_I_constant': True,
            'circular_domain_warning': 'Nonzero homogeneous charged circle violates periodic Gauss unless compensated; not accepted full45 data.',
            'universal_theta_over_m_proper_time': 'failed',
            'scope': 'Continuum algebra and conditional normal-proper-time interpretation; no lattice calibration theorem.'}


def checked_step(program, engine, state):
    following = engine.step(state)
    assert following.same_as(scalar_step(program.tensor, state))
    assert np.array_equal(following.r, state.r)
    assert engine.inverse_step(following).same_as(state)
    return following


def actual_common45():
    program = common45.build45()
    seed = common45.weak_seed(program)
    values = common45.weak_values(program)
    rotated_seed = prepare(program, rotate(program.fields, values), L=seed.L,
                           denominator=int(seed.b[0, 0]), remainders=seed.r)
    states = [seed.copy(), rotated_seed.copy()]
    engine = Engine(program.tensor)
    initial = common45.decode_fields(program, seed)
    _, constraints, diagnostic = formulation.equations(initial, lambda *_: F(0))
    assert all(v == 0 for v in constraints.values())
    assert diagnostic['rho'] == F(3, 100)
    bit_counts, samples, click_count = [], [], 0
    for tick in range(4):
        left, right = (readout(program, state) for state in states)
        assert np.array_equal(rotate(program.fields, left), right)
        decoded = [common45.decode_fields(program, state) for state in states]
        obs = [observables(v) for v in decoded]
        assert obs[0] == obs[1] and obs[0]['charge'] == 0
        diagnostics = [formulation.equations(v, lambda *_: F(0))[2] for v in decoded]
        assert diagnostics[0] == diagnostics[1]
        for name in program.fields:
            if name not in ('phi', 'chi', 'Pi_phi', 'Pi_chi') and not name.startswith('Xi_'):
                assert decoded[0][name] == decoded[1][name]
        bit_counts.append(max(s.max_abs().bit_length() for s in states))
        samples.append({'tick': tick, 'I': str(obs[0]['I']), 'S': str(obs[0]['S'])})
        if tick < 3:
            following = [checked_step(program, engine, state) for state in states]
            clicks = engine.clicks(states[0], following[0], tick+1)
            assert np.all(clicks.kind == 0)
            click_count += len(clicks)
            states = following
    assert all(engine.rewind(state, 3).same_as(start)
               for state, start in zip(states, (seed, rotated_seed)))
    # Removing the scalar while retaining the same geometric/dust preparation
    # must change K on the first actual Engine update: source is not bypassed.
    no_scalar = values.copy()
    for name in ('phi', 'chi', 'Pi_phi', 'Pi_chi'):
        no_scalar[program.fields.index(name)] = F(0)
    counter_seed = prepare(program, no_scalar, L=seed.L, denominator=100, remainders=seed.r)
    with_source, without_source = (engine.step(s) for s in (seed, counter_seed))
    changes = {f'K{a}{a}': str(common45.decode_fields(program, with_source)[f'K{a}{a}']
                              -common45.decode_fields(program, without_source)[f'K{a}{a}'])
               for a in range(3)}
    assert all(F(value) != 0 for value in changes.values())
    return {'mass_squared': 1, 'dt': str(program.dt), 'dx': str(program.dx),
            'tensor_sha256': program.tensor.fingerprint, 'seed_sha256': state_digest(seed),
            'phase_rotated_seed_sha256': state_digest(rotated_seed),
            'channels': program.tensor.G, 'retained_integers_per_node': 3*program.tensor.G,
            'added_clock_channels': 0, 'sites': seed.N, 'updates': 3,
            'monomials': len(program.tensor), 'single_face_violations': len(program.tensor.support_violations()),
            'initial_all_constraints_zero': True, 'initial_rho': str(diagnostic['rho']),
            'exact_phase_equivariance_I_S_stress_geometry': True,
            'nonzero_carries_oracle_inverse_and_full_rewind': True,
            'maximum_state_bits': bit_counts, 'samples': samples,
            'scalar_source_changes_first_K_update': changes,
            'source_removal_control_constraint_warning': 'Same geometric seed with scalar removed is intentionally off the Einstein constraint surface.',
            'official_arithmetic_clicks': click_count, 'all_click_kinds_C0': True,
            'click_only_physical_clock': 'not_tested', 'proper_time_calibration': 'not_tested',
            'resolved_oscillation_on_shared_dt_1_64': 'not_tested',
            'scope': 'Global phase equivariance does not establish local lattice gauge symmetry or a retained detector.'}


def negative_controls():
    program = common45.build45()
    values = common45.weak_values(program)
    for i, name in enumerate(program.fields):
        values[i] = F(int(name.startswith('B') and name[1] == name[2]))
    seed = prepare(program, values, L=3, denominator=100,
                   remainders=common45.weak_seed(program).r)
    engine, state = Engine(program.tensor), seed.copy()
    for _ in range(3):
        state = checked_step(program, engine, state)
        assert np.array_equal(readout(program, state), values)
    assert engine.rewind(state, 3).same_as(seed)
    massless = common45.build45(mass_squared=0)
    seed0 = common45.weak_seed(massless)
    state0, engine0 = seed0.copy(), Engine(massless.tensor)
    initial_i = observables(common45.decode_fields(massless, seed0))['I']
    for _ in range(3):
        state0 = checked_step(massless, engine0, state0)
        obs = observables(common45.decode_fields(massless, state0))
        assert obs['I'] == initial_i and obs['S'] == 0
    assert engine0.rewind(state0, 3).same_as(seed0)
    return {'massive_zero_source_flat_state_stationary': True,
            'massive_tensor_sha256': program.tensor.fingerprint,
            'massless_stationary_scalar_not_a_clock': True,
            'massless_tensor_sha256': massless.tensor.fingerprint,
            'massless_is_separate_control_law': True,
            'massless_seed_constraint_warning': 'Holding the massive geometric/dust seed fixed after mass removal is off-constraint; this is an algebraic no-oscillator control.',
            'flat_circular_control': 'proved analytically; I constant and Q=R=0, so the intensity-phase clock is undefined'}


def resolved_coarse_oscillation():
    """One actually evolved oscillation, not an exact period or converged clock."""
    program = common45.build45(dt=F(1, 4))
    seed = common45.weak_seed(program)
    state, engine = seed.copy(), Engine(program.tensor)
    rows, signs, bits = [], [], []
    for tick in range(15):
        values = common45.decode_fields(program, state)
        obs = observables(values)
        _, constraints, diagnostic = formulation.equations(values, lambda *_: F(0))
        trace = sum(values[f'K{a}{a}'] for a in range(3))
        B = sp.Matrix([[values[f'B{a}{i}'] for i in range(3)] for a in range(3)])
        determinant = F(B.det())
        assert obs['charge'] == 0 and obs['I']+obs['P2'] > 0
        assert determinant > 0 and abs(trace) < 2
        signs.append((obs['S'] > 0)-(obs['S'] < 0))
        bits.append(state.max_abs().bit_length())
        theta = math.atan2(-float(values['Pi_phi']), float(values['phi']))
        if theta < 0:
            theta += 2*math.pi
        rows.append({'tick': tick, 'coordinate_time': float(tick*program.dt),
                     'I': float(obs['I']), 'S': float(obs['S']),
                     'traceK': float(trace), 'detB': float(determinant),
                     'rho': float(diagnostic['rho']), 'Hamiltonian_constraint': float(constraints['H']),
                     'passive_phase_minus_coordinate_time': theta-float(tick*program.dt)})
        if tick < 14:
            state = checked_step(program, engine, state)
    assert engine.rewind(state, 14).same_as(seed)
    minimum = [i for i in range(1, len(signs)) if signs[i-1] < 0 < signs[i]]
    maximum = [i for i in range(1, len(signs)) if signs[i-1] > 0 > signs[i]]
    assert minimum == [7] and maximum == [13]
    assert rows[13]['I'] > rows[12]['I'] and rows[13]['I'] > rows[14]['I']
    assert rows[-1]['Hamiltonian_constraint'] != 0
    # A periodic signal cannot be inferred from one changing sourced cycle.
    assert rows[13]['I'] != rows[0]['I']
    return {'mass_squared': 1, 'dt': str(program.dt), 'dx': str(program.dx),
            'tensor_sha256': program.tensor.fingerprint, 'seed_sha256': state_digest(seed),
            'different_protocol_from_shared_dt_1_64': True,
            'channels': program.tensor.G, 'sites': seed.N, 'updates': 14,
            'maximum_state_bits': bits, 'exact_oracle_inverse_full_rewind': True,
            'sampled_intensity_minimum_tick': 7, 'sampled_intensity_maximum_tick': 13,
            'sampled_S_sign_change_intervals': [[1.5, 1.75], [3.0, 3.25]],
            'actual_sampled_oscillation': 'passed', 'exact_recurrence_at_sampled_peak': 'failed',
            'constraint_preservation': 'failed', 'converged_proper_time_clock': 'not_tested',
            'all_sampled_detB_positive_and_abs_traceK_below_2m': True,
            'continuum_between_samples_domain_theorem': 'not_tested',
            'rows': rows,
            'fine_protocol_cost_lower_bound': 'At dt=1/64, pi/m requires at least 202 updates. D_n >= D_0^(2^n) makes a resolved fine cycle computationally blocked for this encoding.',
            'scope': 'Passive floats/atan2 appear only after Engine snapshots, never in tensor, preparation feedback, or runtime updates.'}


def main():
    result = {'baseline_pin': formulation.BASE_PIN, 'identities': continuum_identities(),
              'common45': actual_common45(), 'negative_controls': negative_controls(),
              'coarse_oscillation': resolved_coarse_oscillation()}
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__), ROOT/'validation/completion/common45.py',
                  ROOT/'validation/completion/formulation.py')}
    path = ROOT/'runs/completion/04_matter_clock.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
