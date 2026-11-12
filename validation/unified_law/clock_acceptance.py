"""Same-candidate scalar clock and source-continuity acceptance.

This is passive validation of the shared spinor+beta Engine law. The independent
proper-time ODE and phase calculations never feed a retained state update.
"""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as s

from . import constrained_coordinates as coordinates

ROOT = Path(__file__).resolve().parents[2]
PHYSICAL_ORDER = ('beta', 'k', 'phi', 'p', 'dust')
TARGET_TIME = F(1, 8)
COUNTS = (3, 4, 6)


def continuum_clock_audit():
    """Independent physical-coordinate derivation, including the same dust source."""
    beta, k, phi, p, dust, mass = s.symbols('beta k phi p dust mass', real=True)
    variables = (beta, k, phi, p, dust)
    velocity = (k, 3*k*k-(mass*mass*phi*phi+dust*dust)/2,
                p, 3*k*p-mass*mass*phi, s.Rational(3, 2)*k*dust)
    derivative = lambda expr: s.simplify(sum(s.diff(expr, x)*v for x, v in zip(variables, velocity)))
    scalar_rho = (p*p+mass*mass*phi*phi)/2
    pressure = (p*p-mass*mass*phi*phi)/2
    rho = scalar_rho+dust*dust
    assert derivative(rho)-3*k*(rho+pressure) == 0
    assert derivative(dust*dust*s.exp(-3*beta)) == 0
    energy = p*p+mass*mass*phi*phi
    phase_rate = mass*(phi*velocity[3]*-1+p*velocity[2])/energy
    expected_rate = mass-3*k*mass*phi*p/energy
    assert s.simplify(phase_rate-expected_rate) == 0
    assert s.expand(energy**2-(2*mass*phi*p)**2-(p*p-mass*mass*phi*phi)**2) == 0
    constraint = 6*k*k-p*p-mass*mass*phi*phi-2*dust*dust
    assert s.expand(derivative(constraint)-6*k*constraint) == 0
    assert s.expand(velocity[1]-(p*p+dust*dust)/2-constraint/2) == 0
    return {'energy_continuity': 'rho_dot=3*k*(rho+pressure)',
            'comoving_dust_mass': 'D=dust^2*exp(-3*beta); D_dot=0',
            'phase': 'theta=atan2(-p,mass*phi) on the nonzero neutral radial sector',
            'phase_proper_rate': 'mass-3*k*mass*phi*p/(mass^2*phi^2+p^2)',
            'monotonic_sufficient_condition': '|3*k|<2*mass, mass>0, scalar energy>0',
            'metric': 'ds^2=-dt^2+exp(-2*beta)*(dx^2+dy^2+dz^2)',
            'proper_time_gauge': 'lapse1; comoving normal proper time equals continuum t',
            'selected_continuum_clock_domain': 'C=0 and k0=-1/2 give k_dot=(p^2+dust^2)/2>=0; decoder k<=0, so |3k|<=3/2 and theta_dot>=1/4 globally forward',
            'scope': 'Continuum identities; no retained detector, winding counter or correction-integral register.'}


def reference_velocity(vector):
    """Independent physical equations; does not import the spinor RHS."""
    beta, k, phi, p, dust = vector
    return (k, 3*k*k-(phi*phi+dust*dust)/2,
            p, 3*k*p-phi, 1.5*k*dust)


def reference(initial, *, duration=float(TARGET_TIME), steps=4096):
    """Passive fourth-order physical-coordinate reference with a checked refinement."""
    vector = np.array([float(initial[name]) for name in PHYSICAL_ORDER])
    dt = duration/steps
    for _ in range(steps):
        first = np.array(reference_velocity(vector))
        second = np.array(reference_velocity(vector+dt*first/2))
        third = np.array(reference_velocity(vector+dt*second/2))
        fourth = np.array(reference_velocity(vector+dt*third))
        vector += dt*(first+2*second+2*third+fourth)/6
    return dict(zip(PHYSICAL_ORDER, map(float, vector)))


def observable_fields(physical):
    """One metric and source ledger; all nonrational quantities are passive."""
    beta, k, phi, p, dust = (float(physical[name]) for name in PHYSICAL_ORDER)
    energy = phi*phi+p*p
    assert energy > 0
    return {'frame_B': math.exp(beta),
            'spatial_metric_diagonal': math.exp(-2*beta),
            'scalar_rho': energy/2,
            'scalar_pressure': (p*p-phi*phi)/2,
            'dust_density': dust*dust,
            'comoving_dust_mass': dust*dust*math.exp(-3*beta),
            'phase': math.atan2(-p, phi),
            'phase_proper_rate': 1-3*k*phi*p/energy,
            'phase_monotonic_margin': 2-abs(3*k)}


def positive_exp_bounds(value, terms=14):
    """Rational lower/upper bounds, for a nonnegative rational exponent.

    Every omitted Taylor term ratio is at most value/(terms+2); bounding the
    positive tail by that geometric series gives an exact interval.
    """
    value = F(value)
    if value < 0 or value >= terms+2:
        raise ValueError('The declared positive Taylor-tail domain is required')
    term, lower = F(1), F(1)
    for degree in range(1, terms+1):
        term *= value/degree
        lower += term
    next_term = term*value/(terms+1)
    upper = lower+next_term/(1-value/(terms+2))
    return lower, upper


def same_candidate_audit():
    """One common equation/decoder family; each prepared h has its own tensor hash."""
    from . import common
    rows = []
    initial = coordinates.physical({'sa': F(1), 'sb': F(0), 'sc': F(0),
                                    'se': F(0), 'beta': F(0)})
    target = reference(initial)
    reference_half = reference(initial, steps=2048)
    reference_agreement = max(abs(target[name]-reference_half[name]) for name in PHYSICAL_ORDER)
    assert reference_agreement < 1e-11
    target_observables = observable_fields(target)
    initial_observables = observable_fields(initial)
    initial_dust_mass = initial_observables['comoving_dust_mass']
    for count in COUNTS:
        dt = TARGET_TIME/count
        trace = common.trace(dt=dt, steps=count, oracle=True)
        program, seed = trace['program'], trace['seed']
        assert trace['physical'][0] == initial
        phases, dust_masses, margins = [], [], []
        for physical in trace['physical']:
            assert coordinates.constraint(physical) == 0
            assert physical['phi'] > 0 and physical['dust'] > 0
            observed = observable_fields(physical)
            assert observed['frame_B'] > 0 and observed['spatial_metric_diagonal'] > 0
            assert observed['phase_monotonic_margin'] > 0 and observed['phase_proper_rate'] > 0
            phases.append(observed['phase'])
            dust_masses.append(observed['comoving_dust_mass'])
            margins.append(observed['phase_monotonic_margin'])
        assert all(new > old for old, new in zip(phases, phases[1:]))
        final = trace['physical'][-1]
        observed = observable_fields(final)
        exp_lower, exp_upper = positive_exp_bounds(-3*final['beta'])
        dust_lower = final['dust']**2*exp_lower-F(1, 4)
        dust_upper = final['dust']**2*exp_upper-F(1, 4)
        assert 0 < dust_lower <= dust_upper
        # For x>0, atan(x)<x, so this is an exact clock-calibration negative.
        assert 0 < -final['p']/final['phi'] < TARGET_TIME
        field_errors = {name: abs(float(final[name])-target[name]) for name in PHYSICAL_ORDER}
        rows.append({**common.identity(program, seed),
            'steps': count, 'target_proper_time': str(TARGET_TIME),
            'nodes': seed.N, 'monomials': len(program.tensor),
            'same_initial_physical_fields': True,
            'exact_constraint_zero_every_macro_sample': True,
            'independent_scalar_oracle_each_tick': True, 'full_state_rewind': True,
            'all_six_initial_remainders': True, 'max_retained_bits': trace['bits'],
            'metric_positive_all_samples': True, 'phase_strictly_increases_all_samples': True,
            'minimum_sampled_clock_monotonic_margin': min(margins),
            'final_physical_fields': {name: float(final[name]) for name in PHYSICAL_ORDER},
            'final_observables': observed, 'field_absolute_errors': field_errors,
            'max_field_error': max(field_errors.values()),
            'phase_error': abs(observed['phase']-target_observables['phase']),
            'dust_mass_error': abs(observed['comoving_dust_mass']-initial_dust_mass),
            'dust_mass_drift_positive_exact_rational_certificate': True,
            'dust_mass_drift_certified_interval': [float(dust_lower), float(dust_upper)],
            'dust_mass_interval_width': float(dust_upper-dust_lower),
            'maximum_sampled_dust_mass_error': max(abs(value-initial_dust_mass) for value in dust_masses),
            'universal_phase_equals_proper_time': False,
            'phase_less_than_proper_time_exact_rational_witness': True,
            'phase_minus_proper_time': observed['phase']-float(TARGET_TIME)})
    for error in ('max_field_error', 'phase_error', 'dust_mass_error'):
        assert all(fine[error] < coarse[error] for coarse, fine in zip(rows, rows[1:])), error
    # These thresholds and sample counts were declared before the actual run.
    assert rows[-1]['dust_mass_error']/initial_dust_mass < 0.05
    assert rows[-1]['phase_error'] < 0.005
    orders = [{error: math.log(coarse[error]/fine[error])/math.log(fine['steps']/coarse['steps'])
               for error in ('max_field_error', 'phase_error', 'dust_mass_error')}
              for coarse, fine in zip(rows, rows[1:])]
    assert abs(target_observables['phase']-float(TARGET_TIME)) > 0.005
    return {'equations': 'shared spinor_beta_mass1', 'duration': str(TARGET_TIME),
        'predeclared_steps': list(COUNTS), 'predeclared_finest_phase_error_bound': 0.005,
        'predeclared_finest_relative_dust_mass_error_bound': 0.05,
        'shared_default_tensor_sha256': rows[0]['tensor_sha256'],
        'shared_default_seed_sha256': rows[0]['seed_sha256'],
        'reference': {'method': 'independent proper-time physical-coordinate RK4; passive only',
                      'steps': 4096, 'half_resolution_agreement': reference_agreement,
                      'initial': {name: str(initial[name]) for name in PHYSICAL_ORDER},
                      'final': target, 'observables': target_observables},
        'rows': rows, 'observed_orders': orders,
        'exact_discrete_constraint': 'passed on every complete-state sample',
        'source_clock_fixed_time_refinement': 'passed observed three-resolution control',
        'exact_discrete_dust_mass_conservation': 'failed by rational exponential bounds; drift converges in this family',
        'universal_scalar_phase_over_mass_as_proper_time': 'failed even in the target continuum solution',
        'operational_clock_and_signal_transport': 'not_tested',
        'spatial_or_general_Einstein_acceptance': 'not_tested',
        'efficient_refinement_bit_cost': 'failed; cubic projective growth remains',
        'scope': 'Each h is a separately fingerprinted immutable tensor in the same homogeneous equation/decoder family.'}


def main():
    from . import common
    result = {'candidate': 'spinor_beta_mass1', 'continuum': continuum_clock_audit(),
              'actual_shared_candidate': same_candidate_audit(),
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (Path(__file__), Path(coordinates.__file__), Path(common.__file__))},
              'physical_acceptance': 'restricted homogeneous convergence evidence; operational clock not established'}
    out = ROOT/'runs/unified_law/06_clock_acceptance.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
