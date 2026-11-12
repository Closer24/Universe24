"""Independent metric, history, domain and representation review of sourced FLRW.

Run: python -m validation.sourced_map.review
No reader, curvature oracle or physical interpretation feeds the Engine.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as s

from universe24.core import Engine, GearType, Tensor
from universe24.core.lattice import ZERO
from universe24.system.bundle import create_bundle
from validation.completion import constraint_closure
from validation.sourced_map import domain, native, physical_map, runtime

ROOT = Path(__file__).resolve().parents[2]
BASE = 'f4f64e062f07b3ca119eccf655df746be206908b'


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def reject(callback):
    try:
        callback()
    except (ValueError, TypeError):
        return True
    raise AssertionError('Invalid review control was accepted')


def einstein_from_metric():
    """Full coordinate curvature computation, independent of any FLRW RHS."""
    t, x, y, z = s.symbols('tau x y z', real=True)
    coordinates = (t, x, y, z)
    scale = s.Function('a', positive=True)(t)
    metric = s.diag(-1, scale**2, scale**2, scale**2)
    inverse = metric.inv()
    connection = [[[s.simplify(sum(inverse[i, m]*(
        s.diff(metric[m, k], coordinates[j])+s.diff(metric[m, j], coordinates[k])
        -s.diff(metric[j, k], coordinates[m]))/2 for m in range(4)))
        for k in range(4)] for j in range(4)] for i in range(4)]
    ricci = s.Matrix(4, 4, lambda i, j: s.simplify(sum(
        s.diff(connection[k][i][j], coordinates[k])
        -s.diff(connection[k][i][k], coordinates[j])
        +sum(connection[k][i][j]*connection[m][k][m]
             -connection[m][i][k]*connection[k][j][m] for m in range(4))
        for k in range(4))))
    scalar = s.simplify(sum(inverse[i, j]*ricci[i, j] for i in range(4) for j in range(4)))
    einstein = (ricci-metric*scalar/2).applyfunc(s.simplify)
    require(einstein[0, 0] == 3*s.diff(scale, t)**2/scale**2, 'Independent metric G00')
    for i in range(1, 4):
        require(s.simplify(einstein[i, i]+2*scale*s.diff(scale, t, 2)+s.diff(scale, t)**2) == 0,
                'Independent metric spatial Einstein component')
    require(all(einstein[i, j] == 0 for i in range(4) for j in range(4) if i != j),
            'Independent off-diagonal components')

    V, U, D, P = s.symbols('V U D P', positive=True)
    a = V**s.Rational(1, 3)
    adot = U/(3*V**s.Rational(2, 3))
    addot = D/(2*V**s.Rational(2, 3))-2*U**2/(9*V**s.Rational(5, 3))
    substitutions = {scale: a, s.diff(scale, t): adot, s.diff(scale, t, 2): addot}
    geometric = einstein.subs(substitutions, simultaneous=True).applyfunc(s.simplify)
    rho, pressure = D/V+P**2/(2*V**2), P**2/(2*V**2)
    stress = s.diag(rho, a*a*pressure, a*a*pressure, a*a*pressure)
    defect = (geometric-stress).applyfunc(s.simplify)
    invariant_form = U*U-3*D*V-s.Rational(3, 2)*P*P
    require(s.simplify(defect[0, 0]-invariant_form/(3*V*V)) == 0, 'Sourced 00 residual')
    for i in range(1, 4):
        require(s.simplify(defect[i, i]/(a*a)-invariant_form/(3*V*V)) == 0, 'Sourced spatial residual')
    require(all(defect[i, j] == 0 for i in range(4) for j in range(4) if i != j), 'Sourced off-diagonal residual')
    # Matter equations are independent of the gravitational constraint test.
    derivative = lambda f: s.simplify(U*s.diff(f, V)+s.Rational(3, 2)*D*s.diff(f, U))
    H, scalar_velocity = U/(3*V), P/V
    require(s.simplify(derivative(scalar_velocity)+3*H*scalar_velocity) == 0, 'Massless KG')
    require(s.simplify(derivative(D/V)+3*H*D/V) == 0, 'Dust continuity')
    require(s.simplify(derivative(rho)+3*H*(rho+pressure)) == 0, 'Total stress continuity')
    return {'status': 'passed', 'construction': 'metric -> all Christoffel coefficients -> Ricci -> all 16 Einstein components',
            'units': 'c=1, 8*pi*G=1, Lambda=0, signature -+++; unit lapse',
            'G00': str(einstein[0, 0]), 'G11': str(einstein[1, 1]),
            'rho': str(rho), 'pressure': str(pressure),
            'G00_minus_T00': 'Q/(3*V^2)',
            'Gii_minus_Tii_divided_by_a_squared': 'Q/(3*V^2)',
            'off_diagonal_G_minus_T': 'all twelve exactly zero',
            'massless_KG_and_dust_and_total_continuity': 'passed',
            'conclusion': 'Q=0 and the exact volume flow give a genuinely sourced flat FLRW Einstein solution on V>0; this proves a restricted integrable subcase only'}


def actual_native_and_controls():
    endpoint_rows = []
    for N in (24, 48):
        program = native.build_native(N)
        seed = native.prepare_native(program)
        engine, state = Engine(program.tensor), seed.copy()
        for step in range(N//8):
            old = state
            state = engine.step(state)
            require(state.same_as(native.scalar_step(old)), 'Actual native scalar oracle')
            require(engine.inverse_step(state).same_as(old), 'Complete native inverse')
            decoded = native.read_conserved(program, state)
            V, U, D, P = (decoded[key] for key in ('V', 'U', 'D', 'P'))
            # Independently reconstructed Einstein residuals from the metric proof.
            rho, pressure = F(P*P, 2*V*V)+D/V, F(P*P, 2*V*V)
            G00, Gspace = U*U/(3*V*V), -D/V+U*U/(3*V*V)
            require(G00 == rho and Gspace == pressure, 'Actual Engine state failed metric Einstein equations')
            require(np.array_equal(state.r, seed.r), 'A carry was discarded')
        require(decoded['V'] == F(355, 256) and decoded['U'] == F(51, 16), 'Matched proper-time endpoint')
        physical = physical_map.physical_decode(decoded)
        with mp.workdps(80):
            integral = mp.quad(lambda tau: 2/(1+3*tau+mp.mpf(3)*tau*tau/4), [0, mp.mpf(1)/8])
            error = abs(physical['phi']-integral)
            require(error < mp.mpf('1e-70'), 'Scalar logarithm versus independent quadrature')
            phase_error = mp.nstr(error, 20)
        require(engine.rewind(state, N//8).same_as(seed), 'Full native rewind')
        endpoint_rows.append({'N': N, 'steps': N//8, 'tau': str(decoded['tau']),
                              'V': str(decoded['V']), 'U': str(decoded['U']),
                              'metric_Einstein_residuals': 'exactly zero',
                              'phase_vs_independent_quadrature_error': phase_error})

    program = native.build_native(24)
    seed = native.prepare_native(program)
    engine = Engine(program.tensor)
    off = seed.copy()
    off.a[0] += 1
    off.b[0] += 1
    defects = []
    for step in range(4):
        values = native.read_conserved(program, off)
        defects.append(values['invariant'])
        reject(lambda values=values: physical_map.physical_decode(values))
        if step < 3:
            off = engine.step(off)
    require(defects == [-12]*4, 'Off-constraint state was silently repaired')

    broken = Tensor([GearType(name, label='audit') for name in native.NAMES],
                    [(name, 6, ((name, ZERO, 'b'),)) for name in native.NAMES], strict_support=True)
    broken_engine = Engine(broken)
    disconnected = broken_engine.step(seed)
    defect = native.read_conserved(program, disconnected)['invariant']
    require(defect == -3420, 'Deleted source coupling did not break Einstein constraint')
    require(broken_engine.inverse_step(disconnected).same_as(seed), 'Source-disconnected inverse')
    return {'status': 'passed', 'endpoint_rows': endpoint_rows,
            'off_constraint_integer_invariant': defects,
            'off_constraint_physical_decoding': 'rejected without projection',
            'removed_dust_geometry_coupling_defect': defect,
            'removed_coupling_still_rewinds': True}


def backward_domain():
    program = native.build_native(24)
    seed = native.prepare_native(program)
    engine = Engine(program.tensor)
    before = engine.rewind(seed, 96)
    W, D, P = map(int, before.b[:3, 0])
    J = W-int(before.a[0, 0])+3*D
    V, U = F(W, 4*program.N**2), F(J, 4*program.N)
    require((V, U) == (F(1), F(-3)), 'Backward cross-and-return endpoint')
    require(J*J-12*D*W-24*program.N**2*P*P == 0, 'Backward arithmetic invariant')
    require(engine.run(before, 96).same_as(seed), 'Backward complete-state round trip')
    reject(lambda: native.read_conserved(program, before))
    certificate = domain.interval_certificate(domain.VolumePoint(1, 3, 2, 1), F(-4))
    require(certificate['both_endpoints_positive'] and not certificate['whole_interval_valid'],
            'Only endpoint positivity was checked')
    require(certificate['minimum_volume'] == '-2', 'Missed intervening singular region')
    return {'status': 'passed_negative_control', 'native_backward_ticks': 96,
            'elapsed_proper_time': '-4', 'endpoint_V': str(V), 'endpoint_U': str(U),
            'invariant': 0, 'complete_roundtrip': True,
            'physical_decoder': 'rejected outside expanding chart',
            'whole_interval': certificate,
            'interpretation': 'Mechanical reversibility across two zero-volume events is not a physical continuation'}


def decoder_precision_and_boundaries():
    # Pell integers provide a valid exact state arbitrarily close to the branch
    # root. Direct floating subtraction U-sqrt(3P²/2) loses all digits here.
    x, y = 1, 0
    for _ in range(90):
        x, y = 5*x+12*y, 2*x+5*y
    require(x*x-6*y*y == 1, 'Exact Pell fixture')
    values = {'V': F(1, 3), 'U': x, 'D': 1, 'P': 2*y,
              'Uref': x, 'phi_ref': 0, 'tau': 0}
    physical = physical_map.physical_decode(values, precision=80)
    require(mp.isfinite(physical['phi']) and physical['phi'] == 0, 'Near-root passive decoder failed')
    large_program = native.build_native(24*x)
    large_seed = native.prepare_native(large_program, V=F(1, 3), U=x, D=1, P=2*y)
    large_engine = Engine(large_program.tensor)
    large_after = large_engine.step(large_seed)
    large_values = native.read_conserved(large_program, large_after)
    moved = physical_map.physical_decode(large_values, precision=80)
    require(large_engine.inverse_step(large_after).same_as(large_seed), 'Large near-root native inverse')
    with mp.workdps(400):
        current = mp.mpf(large_values['U'].numerator)/large_values['U'].denominator
        reference = mp.mpf(x)
        root = mp.sqrt(6)*y
        independently_evaluated = (mp.mpf(2)*y/root)*mp.log(
            ((current-root)/(current+root))/((reference-root)/(reference+root)))
        near_root_error = abs(moved['phi']-independently_evaluated)
        require(moved['phi'] > 0 and near_root_error < mp.mpf('1e-70'),
                'Nonzero near-root Engine phase versus 400-digit direct oracle')
        near_root_error_text = mp.nstr(near_root_error, 20)
    # Changing only the coordinate label cannot replace the evolved geometry.
    shifted = physical_map.physical_decode(dict(values, tau=F(123456)), precision=80)
    require(all(physical[key] == shifted[key] for key in ('B', 'k', 'p', 'phi', 'd')),
            'Physical fields were reconstructed from a tick lookup')
    reject(lambda: physical_map.physical_decode(values, mass_squared=1))
    program = native.build_native(24)
    seed = native.prepare_native(program)
    bundle = runtime.make_bundle(program, seed)
    bad_mass = create_bundle(bundle.tensor, seed, channels=bundle.channels,
                             protocol=bundle.protocol, model=dict(bundle.model, mass_squared=1))
    reject(lambda: runtime._check_interpretation(bad_mass))
    changed = seed.copy()
    changed.r[0, 0] = (int(changed.r[0, 0])+1) % 6
    other = runtime.make_bundle(program, changed)
    require(bundle.bundle_id != other.bundle_id, 'Complete carry history absent from bundle identity')
    require(native.read_conserved(program, seed) == native.read_conserved(program, changed),
            'Carry-transparent physical data unexpectedly changed')
    return {'status': 'passed', 'near_root_exact_U_decimal_digits': len(str(x)),
            'exact_branch_gap_U_squared_minus_3P_squared_over_2': 1,
            'near_root_anchor_phi': '0', 'coordinate_counter_not_field_lookup': True,
            'nonzero_near_root_Engine_phase_vs_400digit_direct_error': near_root_error_text,
            'large_near_root_Engine_step_and_inverse': True,
            'massive_decoder_and_saved_metadata_rejected': True,
            'different_complete_carry_seed_has_different_bundle_identity': True}


def preserve_original_failures():
    h = s.symbols('h', real=True)
    k, p, phi, d = -1+h/2, -2*h, s.Integer(2), 1-3*h/2
    defect = s.expand(6*k*k-p*p-phi*phi-2*d*d)
    require(defect == -7*h*h, 'Old massive first Euler failure')
    legacy = constraint_closure.history_audit()
    require(legacy['rows'][0]['constraint'] == '0' and F(legacy['rows'][1]['constraint']) != 0,
            'Old reduced tick-two failure was lost')
    return {'status': 'original_failures_preserved',
            'independently_expanded_massive_Euler_defect': str(defect),
            'legacy_five_channel_tick_one': legacy['rows'][0]['constraint'],
            'legacy_five_channel_tick_two': legacy['rows'][1]['constraint'],
            'interpretation': 'The six-channel massless law is a different exact physical encoding, not a repair or relabelling of those discrete trajectories'}


def audit():
    result = {'schema': 'universe24/sourced-map/review/1', 'baseline_pin': BASE,
              'independent_metric_Einstein_tensor': einstein_from_metric(),
              'actual_native_solution': actual_native_and_controls(),
              'backward_domain': backward_domain(),
              'decoder_and_bundle_boundaries': decoder_precision_and_boundaries(),
              'original_failure_controls': preserve_original_failures(),
              'restricted_physics': 'exact spatially flat homogeneous isotropic expanding massless-scalar plus positive-dust Einstein solution',
              'not_established': ['massive scalar', 'spatial interactions or general Einstein dynamics',
                                  'operational clocks or detector records', 'physical passage through a singularity'],
              'production_changes': False}
    paths = sorted((ROOT/'validation/sourced_map').glob('*.py'))
    result['source_sha256'] = {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
                              for path in paths}
    return result


if __name__ == '__main__':
    result = audit()
    destination = ROOT/'runs/sourced-map/review.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'independent_restricted_Einstein_and_adversarial_controls_passed',
                      'evidence': str(destination.relative_to(ROOT)),
                      'general_Einstein_acceptance': 'not_established'}, indent=2))
