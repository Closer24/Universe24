"""Independent integration review; run after the component completion audits.

This compares exact evidence identities and proves/reexecutes selected controls.
It does not turn different passing subproblems into one accepted physical law.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

from universe24.core import Engine, State, Tensor
from universe24.system.bundle import BundleError, canonical_bytes, create_bundle
from universe24.system.decoder import default_protocol
from . import common45, native_compiler

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT/'runs/completion'


def read(name):
    return json.loads((EVIDENCE/name).read_text())


def claim_join(left, right):
    """Same-run claims require both immutable law and complete preparation."""
    keys = ('tensor_sha256', 'seed_sha256')
    if any(not left.get(k) or left[k] != right.get(k) for k in keys):
        raise ValueError('Different law or complete seed: physical evidence cannot be joined')


def rejected(action, expected=(ValueError,)):
    try:
        action()
    except expected:
        return True
    raise AssertionError('A declared negative control was incorrectly accepted')


def identity_audit():
    core = read('00_common45.json')
    clock = read('04_matter_clock.json')
    geodesic = read('05_geodesic_signals.json')
    metric = read('03_metric_domain.json')
    native = read('native_compiler.json')
    wave = read('time_stability.json')
    closure = read('07_constraint_closure.json')
    program = common45.build45()
    seed = common45.weak_seed(program)
    actual = {'tensor_sha256': program.tensor.fingerprint,
              'seed_sha256': hashlib.sha256(canonical_bytes(seed.to_dict())).hexdigest()}
    for evidence in (core, clock['common45'], geodesic['actual_snapshots'], closure['common45']):
        claim_join(actual, evidence)
    assert core['mass_squared'] == clock['common45']['mass_squared'] == 1
    assert core['channels'] == clock['common45']['channels'] == geodesic['actual_snapshots']['channels'] == 45
    assert core['dt'] == clock['common45']['dt'] == '1/64'
    assert core['dx'] == clock['common45']['dx'] == '1/4'
    assert core['existing_system_runtime_and_saved_trace_equal']
    assert clock['common45']['added_clock_channels'] == 0
    assert geodesic['actual_snapshots']['additional_retained_probe_channels'] == 0
    # A wrong tensor cannot be concealed by copying the true seed identity.
    distinct = {
        'coarse_clock': clock['coarse_oscillation']['tensor_sha256'],
        'massless_control': clock['negative_controls']['massless_tensor_sha256'],
        'cubic_metric': metric['actual_Engine']['tensor_sha256'],
        'native_potential': native['potential_flow_refinement']['tensor_sha256'],
        'native_wave': wave['native_scalar_oracle']['tensor_fingerprint'],
        'native_joint_compiler': native_compiler.make_quotient_tensor(coupling=1).fingerprint,
        'reduced_constraint_history_lift': closure['actual_reduced_history_lift']['tensor_sha256']}
    for fingerprint in distinct.values():
        assert rejected(lambda fingerprint=fingerprint: claim_join(actual,
            {'tensor_sha256': fingerprint, 'seed_sha256': actual['seed_sha256']}))
    altered = dict(actual, seed_sha256='0'*64)
    assert rejected(lambda: claim_join(actual, altered))
    # Runtime has no permission to promote physics from model names or replay.
    assert all(core['runtime_report']['acceptance_gates'][g]['status'] == 'not_tested'
               for g in 'CDEF')
    assert clock['coarse_oscillation']['constraint_preservation'] == 'failed'
    assert clock['common45']['proper_time_calibration'] == 'not_tested'
    assert geodesic['actual_snapshots']['moving_matter_packet'] == 'not_tested'
    assert metric['negative_control']['original_global_metric_preservation'] == 'failed'
    assert metric['constraint_defect']['finite_h_continuum_constraint_invariance_for_cubic_candidate'] == 'failed'
    assert closure['common45']['discrete_constraint_gate'] == 'failed'
    assert closure['actual_reduced_history_lift']['second_tick_constraint_gate'] == 'failed'
    closure_rows = closure['actual_reduced_history_lift']['rows']
    assert F(closure_rows[0]['constraint']) == 0 and F(closure_rows[1]['constraint']) != 0
    assert native['joint_nonlinear_compiler']['channels'] == 7
    assert native['joint_nonlinear_compiler']['drop_in_corrected45'] is False
    return {'status': 'passed', **actual, 'common_clock_signals_runtime_same_run': True,
            'rejected_distinct_law_transfers': distinct, 'wrong_seed_rejected': True,
            'shared_channels': 45, 'shared_retained_integers_per_node': 135,
            'joint_unallocated_channels': 3, 'physical_acceptance': 'not_established'}


def input_guards():
    program = common45.build45()
    seed = common45.weak_seed(program)
    massless = common45.build45(mass_squared=0)
    assert rejected(lambda: common45.make_bundle(massless, common45.weak_seed(massless)))
    changed = seed.copy()
    changed.r[0, 0] = (int(changed.r[0, 0])+1) % 6
    assert rejected(lambda: common45.make_bundle(program, changed))
    # 45 shared fields + a proposed 3-channel module + another 1-channel clock.
    too_many = Tensor([f'review.{i}' for i in range(49)], [], strict_support=True)
    arrays = [np.zeros((49, 27), dtype=object) for _ in range(3)]
    state = State(3, *arrays)
    try:
        create_bundle(too_many, state, channels=[], protocol=default_protocol(), model={})
    except BundleError as error:
        assert 'at most 48' in str(error)
    else:
        raise AssertionError('49 channels passed the actual system bundle boundary')
    return {'status': 'passed', 'massless_law_under_massive_metadata_rejected': True,
            'changed_complete_seed_under_fixed_metadata_rejected': True,
            '49_channel_joint_allocation_rejected_by_real_bundle': True,
            '45_plus_3_budget_only': '48 fits arithmetically; no compatible coupling has been supplied'}


def independent_native_lift():
    """Independent edge loop and macro formulas; no component force/oracle call."""
    rng = np.random.default_rng(8122026)
    rows = []
    for coupling, drift in ((-3, -2), (0, 4), (2, 3)):
        a = rng.integers(-9, 10, (3, 27)).astype(object)
        b = rng.integers(-9, 10, (3, 27)).astype(object)
        a[2] = 0
        b[2] = 0
        carry = np.array([j % 6 for j in range(81)], dtype=object).reshape(3, 27)
        seed = State(3, a, b, carry)
        q = seed.a[:2]+seed.b[:2]
        oldp = 6*seed.a[:2]+seed.r[:2]
        force = np.zeros((2, 27), dtype=object)
        # Sum each undirected positive x edge once, with both endpoint forces.
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    i, j = (x*3+y)*3+z, (((x+1)%3)*3+y)*3+z
                    difference = int(q[0, j]-q[0, i])
                    scalar = 2*coupling*int(q[1, i]+q[1, j])*difference
                    geometry = -coupling*difference*difference
                    force[0, i] += scalar
                    force[0, j] -= scalar
                    force[1, i] += geometry
                    force[1, j] += geometry
        tensor = native_compiler.make_tensor(coupling=coupling, drift=drift)
        engine, state = Engine(tensor), seed
        for _ in range(3):
            state = engine.step(state)
        newp = 6*state.a[:2]+state.r[:2]
        assert np.array_equal(newp, oldp+2*force)
        assert np.array_equal(state.a[:2]+state.b[:2], q+drift*state.a[:2])
        assert np.array_equal(state.a[2], seed.a[2]) and np.array_equal(state.b[2], seed.b[2])
        assert np.array_equal(state.r[2], seed.r[2])
        assert sum(newp[0]) == sum(oldp[0])
        assert engine.rewind(state, 3).same_as(seed)
        rows.append({'coupling': coupling, 'drift': drift,
                     'maximum_bits': state.max_abs().bit_length(),
                     'macro_identity_and_rewind': True})
    return {'status': 'passed', 'nodes': 27, 'cases': rows,
            'independent_edge_potential_force': True,
            'scope': 'Three-channel mechanical primitive; no Einstein metric or proper clock'}


def independent_nine_tick_compiler():
    """Review the later joint compiler using a fresh edge-potential derivative."""
    rng = np.random.default_rng(9182026)
    rows = []
    for coupling in (-3, 2):
        arrays = [np.zeros((7, 27), dtype=object) for _ in range(3)]
        a, b, carry = arrays
        a[:2] = rng.integers(-17, 18, (2, 27)).astype(object)
        b[:2] = rng.integers(-9, 10, (2, 27)).astype(object)
        carry[:2] = np.array([j % 6 for j in range(54)], dtype=object).reshape(2, 27)
        carry[2:4] = np.array([j % 2 for j in range(54)], dtype=object).reshape(2, 27)
        carry[4:] = np.array([j % 6 for j in range(81)], dtype=object).reshape(3, 27)
        seed = State(3, a, b, carry)
        oldp = 6*seed.a[:2]+seed.r[:2]
        drifted = seed.a[:2]+seed.b[:2]+oldp//18
        forces = np.zeros((2, 27), dtype=object)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    i, j = (x*3+y)*3+z, (((x+1)%3)*3+y)*3+z
                    delta = int(drifted[0, j]-drifted[0, i])
                    scalar = 2*coupling*int(drifted[1, i]+drifted[1, j])*delta
                    mechanical = -coupling*delta*delta
                    forces[0, i] += scalar
                    forces[0, j] -= scalar
                    forces[1, i] += mechanical
                    forces[1, j] += mechanical
        tensor = native_compiler.make_quotient_tensor(coupling=coupling)
        engine, state = Engine(tensor), seed
        peak = seed.max_abs().bit_length()
        for _ in range(9):
            after = engine.step(state)
            assert engine.inverse_step(after).same_as(state)
            state = after
            peak = max(peak, state.max_abs().bit_length())
        newp = 6*state.a[:2]+state.r[:2]
        assert np.array_equal(newp, oldp+2*forces)
        assert np.array_equal(state.a[:2]+state.b[:2], drifted)
        for actual, initial in zip((state.a, state.b, state.r), (seed.a, seed.b, seed.r)):
            assert np.array_equal(actual[2:], initial[2:])
        assert sum(newp[0]) == sum(oldp[0])
        assert engine.rewind(state, 9).same_as(seed)
        rows.append({'coupling': coupling, 'tensor_sha256': tensor.fingerprint,
                     'maximum_bits': peak, 'independent_macro_identity_and_rewind': True})
    return {'status': 'passed', 'channels': 7, 'retained_integers_per_node': 21,
            'data_channels': 2, 'workspace_channels': 2, 'scheduler_channels': 3,
            'nodes': 27, 'microticks': 9, 'prepared_workspace_carries': [0, 1],
            'all_workspace_and_scheduler_triples_restored': True,
            'macro_map': 'S*=S+floor(P/18); Pnew=P+2F(S*); Snew=S*',
            'cases': rows,
            'arbitrary_refinement_or_full45_drop_in': 'not_established'}


def independent_math():
    # Carry parity is an exact invariant of the fixed-six law. Thus the actual
    # maximum single-tick remainder change is four, tightening five to four.
    changes = []
    for u in range(-36, 37):
        for r in range(6):
            _, following = divmod(2*u+r, 6)
            assert (following-r) % 2 == 0
            changes.append(abs(following-r))
    assert max(changes) == 4
    alpha = s.symbols('alpha', real=True)
    M = s.Matrix([[2*s.I*alpha, 1], [1, 0]])
    H = s.Matrix([[1, -s.I*alpha], [s.I*alpha, 1]])
    assert s.simplify(M.conjugate().T*H*M-H) == s.zeros(2)
    # The metric invariant closes because its norm map stays strictly within 2.
    epsilon = s.symbols('epsilon', nonnegative=True)
    lower = s.Rational(3, 4)*(1+epsilon)-2*epsilon
    assert lower.subs(epsilon, s.Rational(1, 7)) == s.Rational(4, 7)
    assert 1/lower.subs(epsilon, s.Rational(1, 7)) < 2
    # Independent neutral scalar phase derivative, from atan2(-p,m*x).
    x, p, k, m = s.symbols('x p k m', real=True)
    xx, yy = m*x, -p
    dx, dy = m*p, -k*p+m*m*x
    numerator = s.expand(xx*dy-yy*dx)
    denominator = m*m*x*x+p*p
    assert s.expand(numerator-(m*denominator-k*m*x*p)) == 0
    # |m*x*p| <= E/2; hence |k|<2m gives positive phase derivative.
    assert s.expand(denominator**2-4*m*m*x*x*p*p-(m*m*x*x-p*p)**2) == 0
    return {'status': 'passed', 'native_wave_symmetrizer_rederived': True,
            'sharper_carry_bound': '|eta|<=2/(3*S), because r_next and r have the same parity',
            'sharper_native_pair_error_bound': '||e_N||<=sqrt(2)*2*N/(3*S)',
            'original_5_over_6_bound': 'valid but not sharp',
            'metric_history_lower_bound_at_worst_epsilon': '4/7',
            'metric_history_next_inverse_norm_bound': '7/4 < 2',
            'neutral_phase_derivative_independently_rederived': 'm-k*m*x*p/(m²*x²+p²)',
            'theta_over_m_is_not_universal_proper_time': True}


def independent_shared_constraint():
    """Actual first shared step compared with an independent reduced equation."""
    k, field, momentum, dust, h = s.symbols('k field momentum dust h', real=True)
    variables = (k, field, momentum, dust)
    velocity = (3*k*k-(field*field+dust*dust)/2, momentum,
                3*k*momentum-field, s.Rational(3, 2)*k*dust)
    constraint = 6*k*k-momentum*momentum-field*field-2*dust*dust
    derivative = sum(s.diff(constraint, x)*v for x, v in zip(variables, velocity))
    assert s.expand(derivative-6*k*constraint) == 0
    euler = constraint.subs(dict(zip(variables, [x+h*v for x, v in zip(variables, velocity)])), simultaneous=True)
    defect = 6*velocity[0]**2-velocity[2]**2-velocity[1]**2-2*velocity[3]**2
    assert s.expand(euler-(1+6*h*k)*constraint-h*h*defect) == 0
    point = {k: -s.Rational(1, 10), field: s.Rational(1, 5), momentum: 0, dust: s.Rational(1, 10)}
    assert constraint.subs(point) == 0
    assert defect.subs(point) == -s.Rational(403, 10000)
    program = common45.build45()
    seed = common45.weak_seed(program)
    engine = Engine(program.tensor)
    after = engine.step(seed)
    values = common45.decode_fields(program, after)
    actual = 6*values['K00']**2-values['Pi_phi']**2-values['phi']**2-2*values['dust_amplitude']**2
    expected = -F(403, 10000)*program.dt**2
    assert actual == expected and actual != 0
    assert engine.inverse_step(after).same_as(seed)
    return {'status': 'passed_negative_control', 'tensor_sha256': program.tensor.fingerprint,
            'continuum_constraint_identity': 'Cdot=6*k*C',
            'exact_Euler_identity': 'Cnext=(1+6*h*k)*C+h²*(6*vk²-vp²-vphi²-2*vd²)',
            'shared_seed_first_step_H': str(actual),
            'nonlinear_discrete_constraint_preservation': 'failed',
            'scope': 'Actual common45 weak homogeneous preparation and its first Engine step'}


def provenance_audit():
    pairs = [('01_formulation.json', None), ('03_metric_domain.json', None),
             ('04_matter_clock.json', None), ('05_geodesic_signals.json', None),
             ('07_constraint_closure.json', None),
             ('native_compiler.json', 'validation/completion/native_compiler.py'),
             ('time_stability.json', 'validation/completion/time_stability.py')]
    checks = []
    for filename, single in pairs:
        record = read(filename)
        declared = record['source_sha256']
        if single:
            declared = {single: declared}
        for path, expected in declared.items():
            actual = hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
            if actual != expected:
                raise AssertionError(f'Stale source/evidence: rerun {filename} after editing {path}')
            checks.append({'evidence': filename, 'source': path, 'sha256': actual})
    return {'status': 'passed', 'source_evidence_hash_checks': checks}


def main():
    result = {'baseline': common45.BASE_PIN,
              'same_run_identity': identity_audit(), 'input_guards': input_guards(),
              'independent_native_lift': independent_native_lift(),
              'independent_nine_tick_compiler': independent_nine_tick_compiler(),
              'independent_math': independent_math(),
              'independent_shared_constraint': independent_shared_constraint(),
              'provenance': provenance_audit(),
              'final_physical_acceptance': 'not_established',
              'remaining_dependencies': ['Nonlinear same-law Einstein constraint closure.',
                  'A stable, refinable nonlinear native compiler within the joint 48-channel budget.',
                  'Localized material motion and operational clock/detector calibration.'],
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    path = EVIDENCE/'08_integration_review.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'output': str(path), 'same_run': result['same_run_identity'],
                      'independent_math': result['independent_math'],
                      'final_physical_acceptance': result['final_physical_acceptance']}, indent=2))


if __name__ == '__main__':
    main()
