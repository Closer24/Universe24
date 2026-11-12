"""Same-candidate logarithmic geometry, source and proper-time contracts.

The five-coordinate spinor/beta equations are the single source authority.
Only the coordinator's unchanged Engine advances retained state. Exponentials,
Christoffels and clock/geodesic formulas below are passive proof/readout work.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

from . import constrained_coordinates as coordinates

ROOT = Path(__file__).resolve().parents[2]


def metric_from_beta(beta, lapse=1):
    """Homogeneous ds²=-N²dt²+exp(-2 beta) dx²; no runtime feedback."""
    return s.diag(-lapse*lapse, *(s.exp(-2*beta) for _ in range(3)))


def ratio_record(value):
    """Bounded passive evidence; the exact assertion still uses the full ratio."""
    value = F(value)
    size = max(abs(value.numerator).bit_length(), value.denominator.bit_length())
    if size <= 256:
        return str(value)
    payload = str(value.numerator < 0).encode()+b':'
    for integer in (abs(value.numerator), value.denominator):
        raw = integer.to_bytes(max(1, (integer.bit_length()+7)//8), 'big')
        payload += len(raw).to_bytes(8, 'big')+raw
    return {'approximation': float(value),
            'numerator_bits': abs(value.numerator).bit_length(),
            'denominator_bits': value.denominator.bit_length(),
            'binary_ratio_sha256': hashlib.sha256(payload).hexdigest()}


def continuum_geometry_audit():
    """Independent four-dimensional Christoffel/Ricci contraction."""
    t = s.symbols('t', real=True)
    beta, lapse = s.Function('beta')(t), s.Function('lapse')(t)
    metric = metric_from_beta(beta, lapse)
    inverse = s.diag(-1/lapse**2, *(s.exp(2*beta) for _ in range(3)))
    partial = lambda expression, axis: s.diff(expression, t) if axis == 0 else s.Integer(0)
    connection = [[[s.simplify(sum(inverse[a,d]*(partial(metric[d,c],b)
        +partial(metric[d,b],c)-partial(metric[b,c],d)) for d in range(4))/2)
        for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = s.zeros(4)
    for a in range(4):
        for b in range(4):
            ricci[a,b] = s.simplify(sum(partial(connection[c][a][b],c)
                -partial(connection[c][a][c],b)
                +sum(connection[c][c][d]*connection[d][a][b]
                     -connection[c][b][d]*connection[d][a][c] for d in range(4))
                for c in range(4)))
    scalar = s.simplify(sum(inverse[a,b]*ricci[a,b] for a in range(4) for b in range(4)))
    einstein = (ricci-metric*scalar/2).applyfunc(s.simplify)
    k, kdot = s.symbols('k kdot', real=True)
    replace = {s.diff(beta,t,2): s.diff(lapse,t)*k+lapse**2*kdot,
               s.diff(beta,t): lapse*k}
    assert s.simplify(einstein[0,0].subs(replace)/lapse**2-3*k*k) == 0
    for i in range(1,4):
        assert s.simplify(einstein[i,i].subs(replace)*s.exp(2*beta)-(2*kdot-3*k*k)) == 0
    assert all(einstein[a,b] == 0 for a in range(4) for b in range(4) if a != b)
    # The comoving dust worldline is geodesic for arbitrary homogeneous lapse.
    velocity = [1/lapse, 0, 0, 0]
    acceleration = [s.simplify(sum(velocity[b]*partial(velocity[a],b) for b in range(4))
        +sum(connection[a][b][c]*velocity[b]*velocity[c] for b in range(4) for c in range(4)))
        for a in range(4)]
    assert acceleration == [0,0,0,0]
    assert (s.Matrix(velocity).T*metric*s.Matrix(velocity))[0] == -1

    values, drift, decoded = coordinates.symbolic_candidate()
    derivative = lambda expression: s.expand(sum(s.diff(expression, values[name])*drift[name]
                                                 for name in coordinates.FIELDS))
    physical_k = decoded['k']
    density = (decoded['p']**2+decoded['phi']**2)/2+decoded['dust']**2
    pressure = (decoded['p']**2-decoded['phi']**2)/2
    assert s.expand(derivative(decoded['beta'])-physical_k) == 0
    assert s.expand(3*physical_k**2-density) == 0
    assert s.expand(2*derivative(physical_k)-3*physical_k**2-pressure) == 0
    assert s.expand(derivative(density)-3*physical_k*(density+pressure)) == 0
    assert s.expand(derivative(decoded['dust']**2)-3*physical_k*decoded['dust']**2) == 0
    assert s.expand(derivative(physical_k)-(decoded['p']**2+decoded['dust']**2)/2) == 0
    # The source constraint alone cannot validate a frozen, mismatched metric.
    assert s.expand(density) != 0
    wrong_geometry_einstein00 = -density
    assert s.expand(wrong_geometry_einstein00) != 0
    return {'independent_full4D_Einstein_tensor': True,
        'G00_orthonormal': '3*k^2', 'Gii_orthonormal': '2*dk/dtau-3*k^2',
        'actual_spinor_source_equals_Einstein_tensor': True,
        'same_beta_velocity_equals_k': True,
        'total_energy_continuity': True,
        'dust_comoving_amount': 'dust^2*exp(-3*beta) is constant in the exact continuum ODE',
        'comoving_dust_geodesic': True, 'comoving_proper_time': 'dtau=N*dt; chosen candidate N=1',
        'frozen_geometry_rejected_despite_zero_algebraic_constraint': True,
        'continuum_future_bound': 'k0<=k(t)<=0; beta0+k0*t<=beta(t)<=beta0 for t>=0',
        'global_future_ODE_domain': 'The positive definite weighted spinor norm -k is nonincreasing; no finite future blowup.',
        'scope': 'Exact homogeneous isotropic continuum pushforward; not finite-step Einstein evolution.'}


def geodesic_reference_audit():
    """Conditional same-metric mass shell; these are not retained probe tracks."""
    beta = s.symbols('beta', real=True)
    lapse = s.symbols('lapse', positive=True)
    mass = s.symbols('mass', positive=True)
    px,py,pz = s.symbols('px py pz', real=True)
    norm2 = px*px+py*py+pz*pz
    energy = s.sqrt(mass*mass+s.exp(2*beta)*norm2)
    inverse = s.diag(-1/lapse**2, *(s.exp(2*beta) for _ in range(3)))
    covector = s.Matrix([-lapse*energy,px,py,pz])
    assert s.simplify((covector.T*inverse*covector)[0]+mass*mass) == 0
    coordinate_velocity = s.Matrix([lapse*s.exp(2*beta)*p/energy for p in (px,py,pz)])
    proper_rate = lapse*mass/energy
    assert s.simplify(proper_rate**2-lapse**2
        +s.exp(-2*beta)*(coordinate_velocity.T*coordinate_velocity)[0]) == 0
    assert s.simplify(proper_rate.subs({px:0,py:0,pz:0})-lapse) == 0
    # Wrong coordinate-tick identification is detected at nonzero momentum.
    assert proper_rate.subs({beta:0,lapse:1,mass:4,px:3,py:0,pz:0}) == F(4,5)
    return {'same_metric_mass_shell': True,
        'spatial_covector_constants': 'p_i constant for a homogeneous metric',
        'coordinate_velocity': 'dx^i/dt=N*exp(2beta)*p_i/sqrt(m^2+exp(2beta)|p|^2)',
        'proper_time_rate': 'dtaumoving/dt=N*m/sqrt(m^2+exp(2beta)|p|^2)',
        'null_coordinate_speed': 'N*exp(beta)',
        'wrong_coordinate_tick_control': 'flat m=4, |p|=3 gives 4/5, not 1',
        'actual_retained_moving_probe': 'not_tested',
        'actual_spatial_matter_or_signal_propagation': 'not_tested'}


def audit_metric_states(program, states):
    """Exact same-law retained-history metric certificate for a supplied trace.

    This reads complete states; it never advances, mutates or repairs them.
    Each state must use the shared positive uniform projective denominator.
    """
    from . import common
    assert tuple(program.fields) == coordinates.FIELDS and program.degree == 3
    assert len(states) >= 2
    h = F(program.dt)
    samples = []
    for tick, state in enumerate(states):
        assert all(np.all(row == row[0]) for row in state.b)
        fields = common.decode_coordinates(program, state)
        decoded = coordinates.physical(fields)
        assert coordinates.constraint(decoded) == 0 and decoded['k'] <= 0
        samples.append(decoded)
    assert int(states[0].a[0,0]) == 0 and np.all(states[0].a == 0)
    assert int(states[0].b[0,0]) >= 2 and program.multiplier >= 2
    increments, epsilons = [], []
    for n, (before, after) in enumerate(zip(states, states[1:])):
        assert np.array_equal(after.a, before.b)
        epsilon = F(int(before.a[0,0]), int(after.b[0,0]))
        assert 0 <= epsilon <= F(1,7)
        current = samples[n]
        previous_beta = samples[n-1]['beta'] if n else F(0)
        expected = (1+epsilon)*(current['beta']+h*current['k'])-epsilon*previous_beta
        assert samples[n+1]['beta'] == expected
        increment = samples[n+1]['beta']-current['beta']
        expected_increment = ((1+epsilon)*h*current['k']
                              +epsilon*(increments[n-1] if n else 0))
        assert increment == expected_increment <= 0
        increments.append(increment)
        epsilons.append(epsilon)
    max_curvature = max(abs(row['k']) for row in samples[:-1])
    assert all(-F(4,3)*h*max_curvature <= value <= 0 for value in increments)
    initial_beta, final_beta = samples[0]['beta'], samples[-1]['beta']
    lower = initial_beta-F(4,3)*(len(samples)-1)*h*max_curvature
    assert lower <= final_beta <= initial_beta
    return {'tensor_sha256': program.tensor.fingerprint, 'channels': program.tensor.G,
        'steps': len(states)-1, 'nodes': states[0].N,
        'metric_decoder': 'B=exp(beta), gamma_inverse=exp(2beta)*I',
        'every_snapshot_constraint_zero': True, 'beta_monotone_nonincreasing': True,
        'actual_complete_history_recurrence': True,
        'metric_positive_at_every_finite_snapshot': True,
        'epsilon_bound': '0<=epsilon<=1/7',
        'beta_initial': ratio_record(initial_beta), 'beta_final': ratio_record(final_beta),
        'beta_lower_bound': ratio_record(lower), 'maximum_abs_k_on_interval': ratio_record(max_curvature),
        'fixed_time_lower_metric_bound': 'lambda_min(gamma_inverse)>=exp(2beta0-8*T*Kmax/3)',
        'positive_metric_is_not_uniform_infinite_time_bound': True,
        'finite_step_Einstein_evolution': 'not_asserted',
        'additional_retained_metric_or_probe_channels': 0}


def main():
    from . import common
    from universe24.core import State
    runs = []
    for count in (3,4,6):
        data = common.trace(dt=F(1,8*count), steps=count)
        record = audit_metric_states(data['program'], data['states'])
        record.update(common.identity(data['program'], data['seed']))
        record['complete_bits'] = data['bits']
        record['physical_time'] = '1/8'
        runs.append(record)
        if count == 3:
            original = data['states'][1]
            corrupted = State(original.L, original.a.copy(), original.b.copy(), original.r.copy())
            beta_channel = data['program'].fields.index('beta')+1
            corrupted.b[beta_channel,:] += 1
            assert coordinates.constraint(common.decode(data['program'], corrupted)) == 0
            try:
                audit_metric_states(data['program'], [data['seed'], corrupted])
            except AssertionError:
                pass
            else:
                raise AssertionError('Wrong metric evolution passed the complete-history check')
    result = {'candidate': 'spinor_beta_mass1',
        'continuum_geometry': continuum_geometry_audit(),
        'geodesic_reference': geodesic_reference_audit(),
        'actual_shared_metric': runs,
        'wrong_beta_state_rejected_despite_zero_constraint': True,
        'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (Path(__file__), Path(coordinates.__file__), Path(common.__file__))},
        'limitations': ['Homogeneity removes spatial momentum/curvature modes.',
            'Passive trajectories and mass shell do not allocate a material probe.',
            'Algebraic positivity and exact constraint do not establish finite-step source dynamics.',
            'The common projective integer cost remains a separate issue.']}
    output = ROOT/'runs/unified_law/05_spatial_metric.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
