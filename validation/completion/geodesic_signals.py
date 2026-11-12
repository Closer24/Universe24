"""Same-equation characteristic, phase and conditional geodesic audits.

All worldline calculations are independent oracles, never Engine state or
callbacks. No propagated packet or operational moving clock is certified.
Run: python -m validation.completion.geodesic_signals
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

from universe24.core import Engine
from universe24.system.bundle import canonical_bytes
from validation.completion import formulation
from validation.geometry.team48 import refinement_integer_projective as projective

ROOT = Path(__file__).resolve().parents[2]
FIELDS = formulation.FIELDS


def zero(matrix):
    return matrix.applyfunc(s.expand) == s.zeros(*matrix.shape)


def state_hash(state):
    return hashlib.sha256(canonical_bytes(state.to_dict())).hexdigest()


def metric(fields):
    """Passive reconstruction, only from the very same retained frame."""
    B = s.Matrix(3, 3, lambda a, i: fields[f'B{a}{i}'])
    if B.det() == 0:
        raise ValueError('Degenerate frame; no inverse metric exists')
    inverse = B.T * B
    return B, inverse, inverse.inv()


def matter_symbols(fields, direction):
    A = formulation.principal(fields, direction)
    blocks = {}
    for name in ('phi', 'chi'):
        indices = [FIELDS.index(f'Pi_{name}')]
        indices += [FIELDS.index(f'Xi_{name}{a}') for a in range(3)]
        blocks[name] = A.extract(indices, indices)
    indices = [FIELDS.index(f'{name}{a}') for name in ('E', 'M') for a in range(3)]
    blocks['maxwell'] = A.extract(indices, indices)
    return blocks


def cone_audit():
    fields = dict(zip(FIELDS, s.symbols('f:44', real=True)))
    n = s.Matrix(s.symbols('nx ny nz', real=True))
    B = s.Matrix(3, 3, lambda a, i: fields[f'B{a}{i}'])
    w = B*n
    radius = (w.T*w)[0]
    blocks = matter_symbols(fields, n)
    kg = s.zeros(4)
    kg[0, 1:] = w.T
    kg[1:, 0] = w
    cross = s.Matrix([[0, -w[2], w[1]], [w[2], 0, -w[0]], [-w[1], w[0], 0]])
    em = s.zeros(6)
    em[:3, 3:], em[3:, :3] = cross, -cross
    assert blocks['phi'] == kg == blocks['chi']
    assert blocks['maxwell'] == em
    assert zero(kg**3-radius*kg) and zero(em**3-radius*em)
    assert s.expand(s.trace(kg**2)-2*radius) == 0
    assert s.expand(s.trace(em**2)-4*radius) == 0
    assert s.expand(radius-(n.T*(B.T*B)*n)[0]) == 0
    # Nonorthogonal full frame and oblique covector reject a Euclidean decoder.
    probe = {name: s.Integer(0) for name in FIELDS}
    held_B = s.Matrix([[2, s.Rational(1, 3), 0], [s.Rational(1, 5), 1, 0], [0, s.Rational(1, 4), 3]])
    for a in range(3):
        for i in range(3):
            probe[f'B{a}{i}'] = held_B[a, i]
    held_n = s.Matrix([1, 2, -1])
    actual = matter_symbols(probe, held_n)
    expected = (held_B*held_n).dot(held_B*held_n)
    wrong = held_n.dot(held_n)
    assert expected != wrong
    for block in actual.values():
        assert zero(block**3-expected*block)
        assert not zero(block**3-wrong*block)
    return {'status': 'passed', 'arbitrary_frame_covector_and_background': True,
            'scalar_speeds': '0 (x2), +/-sqrt(n.T*B.T*B*n), per real component',
            'maxwell_speeds': '0 (x2), +/-sqrt(n.T*B.T*B*n) (each x2)',
            'massive_KG_principal_characteristics': 'null, not timelike',
            'wrong_metric_control_rejected': True, 'heldout_cone_squared': str(expected),
            'wrong_Euclidean_cone_squared': str(wrong),
            'scope': 'Continuum principal equations from the shared builder, not a discrete dispersion theorem.'}


def phase_stress_audit():
    phi, chi, p, q = s.symbols('phi chi p q', real=True)
    assert s.expand((phi**2+chi**2)*(p**2+q**2)-(phi*p+chi*q)**2-(phi*q-chi*p)**2) == 0
    amplitude, omega = s.symbols('R omega', positive=True)
    mass = s.Integer(1)  # The actual shared law has fixed mass_squared=1.
    k = s.Matrix(s.symbols('kx ky kz', real=True))
    fields = {name: s.Integer(0) for name in FIELDS}
    for a in range(3):
        fields[f'B{a}{a}'] = s.Integer(1)
        fields[f'Xi_chi{a}'] = amplitude*k[a]
    fields['phi'], fields['Pi_chi'] = amplitude, -amplitude*omega
    _, _, diagnostic = formulation.equations(fields, lambda *_: s.Integer(0), mass_squared=mass**2)
    shell = {omega**2: mass**2+k.dot(k)}
    assert s.expand(diagnostic['rho']-amplitude**2*omega**2).subs(shell).expand() == 0
    for a in range(3):
        assert s.expand(diagnostic['momentum'][a]-amplitude**2*omega*k[a]) == 0
        for b in range(3):
            assert s.expand(diagnostic['stress'][a][b]-amplitude**2*k[a]*k[b]).subs(shell).expand() == 0
    assert s.expand(diagnostic['electric_charge']-amplitude**2*omega) == 0
    assert all(s.expand(diagnostic['electric_current'][a]-amplitude**2*k[a]) == 0 for a in range(3))
    # Gauge-covariant k_mu = d_mu S - q A_mu, not bare scalar phase.
    dS, charge, potential, gauge_derivative = s.symbols('dS charge A dlambda')
    assert s.expand((dS+charge*gauge_derivative)-charge*(potential+gauge_derivative)-(dS-charge*potential)) == 0
    assert s.expand(dS+charge*gauge_derivative-dS) != 0
    sigma, m = s.symbols('sigma m', positive=True)
    energy = s.sqrt(m*m+sigma)
    rate = m/energy
    phase_rate = -energy+sigma/energy
    assert s.simplify(phase_rate/rate+m) == 0
    assert s.simplify(rate**2-(1-sigma/energy**2)) == 0
    return {'status': 'passed', 'amplitude_phase_decomposition': True,
            'actual_builder_plane_wave_stress': 'T_ab=R^2 k_a k_b on k.k=-m^2, constant amplitude',
            'actual_builder_current': 'J^a=q R^2 k^a',
            'covariant_phase_rate': '(dS-q A_mu dx^mu)/d_tau=-m, at leading semiclassical order',
            'proper_time_rate': 'd_tau/dt=m/sqrt(m^2+n.T*gamma_inverse*n)',
            'bare_phase_gauge_control_rejected': True,
            'scope': 'Local mass-shell conditional identity, not an Engine packet or detector.'}


def christoffel(g, coordinates):
    inverse = g.inv()
    return [[[s.simplify(sum(inverse[a, d]*(s.diff(g[d, c], coordinates[b])
                +s.diff(g[d, b], coordinates[c])-s.diff(g[b, c], coordinates[d]))/2
                for d in range(len(coordinates)))) for c in range(len(coordinates))]
                for b in range(len(coordinates))] for a in range(len(coordinates))]


def geodesic_audit():
    t, x, y, z = s.symbols('t x y z', real=True)
    a = s.Function('a', positive=True)(t)
    px, py, pz = s.symbols('px py pz', positive=True)
    momenta = s.Matrix([px, py, pz])
    p2 = momenta.dot(momenta)
    g = s.diag(-1, a*a, a*a, a*a)
    gamma = christoffel(g, (t, x, y, z))
    ut = s.sqrt(1+p2/a**2)
    timelike = s.Matrix([ut, *(momenta/a**2)])
    null = s.Matrix([s.sqrt(p2)/a, *(momenta/a**2)])
    for name, velocity, norm in (('timelike', timelike, -1), ('null', null, 0)):
        assert s.simplify((velocity.T*g*velocity)[0]-norm) == 0
        for mu in range(4):
            residual = velocity[0]*s.diff(velocity[mu], t)+sum(
                gamma[mu][b][c]*velocity[b]*velocity[c] for b in range(4) for c in range(4))
            assert s.simplify(residual) == 0, (name, mu, residual)
    # Milne 1+1 control is a nonconstant synchronous metric with exact tau(t).
    T, P = s.symbols('T P', positive=True)
    tau = s.sqrt(T*T+P*P)
    coordinate_x = s.log(T/(s.sqrt(T*T+P*P)+P))
    assert s.simplify(s.diff(tau, T)-1/s.sqrt(1+P*P/T**2)) == 0
    assert s.simplify(s.diff(coordinate_x, T)-P/(T*s.sqrt(T*T+P*P))) == 0
    # Held-out rational endpoints: t=3,8, P=4 -> proper time sqrt(80)-5.
    elapsed = s.sqrt(80)-5
    assert 0 < float(elapsed) < 5
    # Nonzero field test separates charged trajectories from geodesics.
    X, energy, charge, field, mass = s.symbols('X E q F m', positive=True)
    kinetic_time = energy+charge*field*X
    kinetic_x = s.sqrt(kinetic_time**2-mass**2)
    accel_x = s.simplify(kinetic_x*s.diff(kinetic_x, X))
    assert s.simplify(accel_x-charge*field*kinetic_time) == 0
    assert accel_x != 0 and accel_x.subs(charge, 0) == 0
    # Curvature in the generic FLRW control is nonzero for a=1+t^2/50.
    held_a = 1+t*t/50
    scalar_curvature = s.simplify(6*(s.diff(held_a, t, 2)/held_a+(s.diff(held_a,t)/held_a)**2))
    assert scalar_curvature != 0
    return {'status': 'passed', 'generic_FLRW_null_and_timelike_geodesic_residuals': 0,
            'heldout_curved_scale_factor': 'a(t)=1+t^2/50',
            'heldout_Ricci_scalar': str(scalar_curvature),
            'Milne_moving_clock': {'t0': 3, 't1': 8, 'P': 4,
                'coordinate_elapsed': 5, 'proper_elapsed': str(elapsed),
                'proper_elapsed_decimal': float(elapsed)},
            'charged_geodesic_negative_control': 'nonzero k^nu*d_nu k^x=q F (E+q F X); Lorentz residual zero',
            'scope': 'Independent continuum metric/trajectory oracles; no trajectory is supplied to the Engine.'}


def actual_snapshot_audit():
    from validation.completion import common45
    program = common45.build45()
    seed = common45.weak_seed(program)
    engine, state = Engine(program.tensor), seed
    rows = []
    direction = s.Matrix([1, 2, 3])
    for step in range(4):
        before = state_hash(state)
        current = projective.readout(program, state)
        fields = dict(zip(program.fields, current[:, 0]))
        B, inverse, spatial = metric(fields)
        radius = (direction.T*inverse*direction)[0]
        blocks = matter_symbols(fields, direction)
        for block in blocks.values():
            assert zero(block**3-radius*block)
        assert zero(spatial*inverse-s.eye(3))
        mass2, energy2 = s.Integer(1), 1+radius
        # Ratios only: no numerical root enters any retained channel.
        rate2 = mass2/energy2
        assert 0 < rate2 < 1
        wrong_metric_rejected = not zero(blocks['phi']**3-direction.dot(direction)*blocks['phi'])
        if step > 0:
            assert wrong_metric_rejected
        rows.append({'step': step, 'frame_determinant': str(B.det()),
                     'null_frequency_squared': str(radius),
                     'conditional_moving_proper_rate_squared': str(rate2),
                     'wrong_fixed_Euclidean_metric_rejected': wrong_metric_rejected,
                     'max_bits': max(abs(int(v)).bit_length() for ar in (state.a,state.b,state.r) for v in ar.flat)})
        assert state_hash(state) == before
        if step < 3:
            state = engine.step(state)
    assert engine.rewind(state, 3).same_as(seed)
    return {'status': 'passed', 'tensor_sha256': program.tensor.fingerprint,
            'seed_sha256': state_hash(seed), 'channels': state.G,
            'additional_retained_probe_channels': 0, 'actual_Engine_steps': 3,
            'all_snapshot_cones_use_retained_B': True, 'rewind_exact': True,
            'snapshots': rows, 'moving_matter_packet': 'not_tested',
            'operational_moving_clock': 'not_tested',
            'scope': 'Actual evolving metric snapshots, with conditional passive rates only.'}


def main():
    result = {'baseline': formulation.BASE_PIN, 'cones': cone_audit(),
              'phase_stress': phase_stress_audit(), 'geodesic_oracles': geodesic_audit(),
              'actual_snapshots': actual_snapshot_audit(),
              'physical_geodesic_and_clock_acceptance': 'not_tested'}
    sources = (Path(__file__), ROOT/'validation/completion/formulation.py',
               ROOT/'validation/completion/common45.py',
               ROOT/'validation/geometry/team48/matter_equations.py',
               ROOT/'validation/geometry/team48/matter_charged.py')
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    path = ROOT/'runs/completion/05_geodesic_signals.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
