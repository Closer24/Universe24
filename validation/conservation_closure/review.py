"""Independent complete-state review of the shared Bianchi-I construction.

This audit has its own integer recurrence, physical readout and source equations.
It keeps conservation, Einstein dynamics, clock calibration and transport distinct.
Run after the other five conservation_closure audits to verify their fresh joins.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

from universe24.core import Engine, State
from universe24.core.lattice import ZERO
from universe24.system.bundle import canonical_bytes
from . import common

ROOT = Path(__file__).resolve().parents[2]
RESOLUTIONS = (24, 48, 96)
SOURCES = [
    {'title': 'Khalatnikov and Kamenshchik, A generalisation of the Heckmann-Schucking cosmological solution',
     'url': 'https://arxiv.org/pdf/gr-qc/0301022',
     'read': 'Section 2 equations 14-23; section 3 equations 27-31. Conserved shear and dust/stiff-matter exact solutions.'},
    {'title': 'Noether, Invariant Variation Problems, Tavel translation',
     'url': 'https://arxiv.org/pdf/physics/0503066',
     'read': 'Section 1 theorems I and II, and the general-relativity example; section 2 equations 11-13.'},
]


def scalar_oracle(state):
    """Explicit scalar update, independent of common.scalar_step and Tensor."""
    next_a, next_b, next_r = (np.empty((state.G, state.N), dtype=object) for _ in range(3))
    for node in range(state.N):
        for gear in range(8):
            current = int(state.b[gear, node])
            forcing = 18*int(state.b[1, node]) if gear == 0 else 0
            quotient, remainder = divmod(12*current+2*forcing+int(state.r[gear, node]), 6)
            next_a[gear, node] = current
            next_b[gear, node] = quotient-int(state.a[gear, node])
            next_r[gear, node] = remainder
    for gear in range(8, state.G):
        next_a[gear], next_b[gear], next_r[gear] = state.b[gear], -state.a[gear], state.r[gear]
    return State(state.L, next_a, next_b, next_r)


def physical_oracle(program, state):
    """Independent rational projection; deliberately not a domain validator."""
    from validation.padding import sector_state
    state = sector_state(state, 8)
    values = [int(x) for x in state.b[:, 0]]
    w, dust, scalar, reference, offset, tick, s1, s2 = values
    shear = (s1, s2, -s1-s2)
    j = w-int(state.a[0, 0])+3*dust
    volume, velocity = F(w, 4*program.N**2), F(j, 4*program.N)
    h = tuple((velocity/F(3)+si)/volume for si in shear)
    pressure = F(scalar**2, 2)/volume**2
    rho = pressure+dust/volume
    q = velocity**2-3*dust*volume-F(3, 2)*(scalar**2+sum(si**2 for si in shear))
    return {'V': volume, 'U': velocity, 'D': dust, 'P': scalar, 'S': shear,
            'Uref': F(reference, 4*program.N), 'phi_ref': offset,
            'tau': F(tick, program.N), 'W': w, 'J': j, 'Q': q,
            'invariant': j*j-12*dust*w-24*program.N**2*(scalar**2+sum(si*si for si in shear)),
            'H': h, 'rho': rho, 'pressure': pressure}


def symbolic_audit():
    v, u, d, p, s1, s2, step, alpha = sp.symbols('V U D P S1 S2 h alpha')
    shear = (s1, s2, -s1-s2)
    q = u*u-3*d*v-sp.Rational(3, 2)*(p*p+sum(x*x for x in shear))
    v_next = v+alpha*step*u+sp.Rational(3, 4)*d*(alpha*step)**2
    u_next = u+sp.Rational(3, 2)*d*alpha*step
    assert sp.expand(q.subs({v:v_next, u:u_next}, simultaneous=True)-q) == 0
    # Every alpha preserves all these first integrals. Unit proper-time
    # normalization selects alpha=1 when the metric lapse is held at one.
    assert sp.diff(v_next, step).subs(step, 0) == alpha*u
    assert sp.diff(u_next, step) == sp.Rational(3, 2)*alpha*d
    # Conversely, a specified proper-time midpoint kinematic law and the
    # positive branch make conservation sufficient for this reduced map.
    up = sp.symbols('Uplus')
    midpoint_volume = v+step*(up+u)/2
    midpoint_defect = sp.factor(q.subs({v:midpoint_volume,u:up}, simultaneous=True)-q)
    midpoint_factor = (up+u)*(up-u-sp.Rational(3,2)*d*step)
    assert sp.expand(midpoint_defect-midpoint_factor) == 0
    unique_up = u+sp.Rational(3,2)*d*step
    assert sp.expand(midpoint_volume.subs(up,unique_up)-(v+step*u+sp.Rational(3,4)*d*step**2)) == 0
    h = tuple((u/3+si)/v for si in shear)
    deriv = lambda expr: sp.diff(expr, v)*u+sp.diff(expr, u)*sp.Rational(3, 2)*d
    hdot = tuple(deriv(hi) for hi in h)
    rho = p*p/(2*v*v)+d/v
    pressure = p*p/(2*v*v)
    g00 = sum(h[i]*h[j] for i in range(3) for j in range(i+1, 3))
    assert sp.simplify(g00-rho-q/(3*v*v)) == 0
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        normalized_gii = -(hdot[j]+hdot[k]+h[j]**2+h[k]**2+h[j]*h[k])
        assert sp.simplify(normalized_gii-pressure-q/(3*v*v)) == 0
    assert sp.simplify(deriv(rho)+(rho+pressure)*sum(h)) == 0
    assert sp.simplify(deriv(p/v)+sum(h)*p/v) == 0
    for i in range(3):
        assert sp.simplify(deriv(h[i]-sum(h)/3)+sum(h)*(h[i]-sum(h)/3)) == 0
    w, j, n = sp.symbols('W J N', integer=True)
    integer_q = j*j-12*d*w-24*n*n*(p*p+sum(si*si for si in shear))
    assert sp.expand(integer_q.subs({w:w+j+3*d,j:j+6*d}, simultaneous=True)-integer_q) == 0
    return {'integer_invariant_pushforward': '0',
            'independent_Einstein_diagonal_residuals': ['Q/(3*V^2)']*4,
            'source_continuity_and_massless_scalar': True, 'mixed_shear_eigenvalues_conserved': True,
            'restricted_discrete_uniqueness': {
                'assumptions':'D,P,S fixed; Q+=Q; V+-V=h*(U++U)/2; U++U>0; h is declared proper interval',
                'factorization':'Q+-Q=(U++U)*(U+-U-3*D*h/2)',
                'unique_map':'U+=U+3*D*h/2; V+=V+h*U+3*D*h^2/4',
                'scope':'Midpoint kinematics and proper-time/branch assumptions are additional input, not consequences of conservation alone.'},
            'conservation_does_not_fix_dynamics': {
                'family': 'V+=V+alpha*h*U+3*D*(alpha*h)^2/4; U+=U+3*D*alpha*h/2',
                'Q_D_P_S_preserved_for_every_alpha': True,
                'unit_proper_time_selects': 'alpha=1',
                'identity_counterexample': 'alpha=0 preserves all charges but freezes geometry with positive density',
                'scope': 'Physical flow family; no claim that every alpha has this same native integer embedding.'}}


def actual_state_review():
    rows = []
    fixtures = [({}, 3), ({'P': -2, 'S':(-1, 1, 0), 'phi_ref':3, 'tau_tick':-7}, 3),
                ({'V':F(10,3), 'U':5, 'P':2, 'S':(1,1,-2)}, 4)]
    for preparation, steps in fixtures:
        program = common.build(24)
        seed = common.prepare(program, **preparation)
        state, engine = seed, Engine(program.tensor)
        initial = physical_oracle(program, seed)
        assert initial['Q'] == 0
        max_bits = common.complete_bits(seed)
        for tick in range(steps+1):
            decoded = physical_oracle(program, state)
            shared = common.read_conserved(program, state)
            assert all(decoded[key] == shared[key] for key in decoded)
            t = tick*program.h
            assert decoded['V'] == initial['V']+initial['U']*t+F(3,4)*initial['D']*t*t
            assert decoded['U'] == initial['U']+F(3,2)*initial['D']*t
            assert decoded['tau'] == initial['tau']+t
            assert decoded['Q'] == 0 and decoded['invariant'] == 0
            assert decoded['D'] == initial['D'] and decoded['P'] == initial['P'] and decoded['S'] == initial['S']
            # Proper-time finite-volume acceleration, not merely Q, is tested.
            if tick == steps:
                break
            previous = state
            state = engine.step(previous)
            assert state.same_as(scalar_oracle(previous))
            assert engine.inverse_step(state).same_as(previous)
            assert np.array_equal(state.r, seed.r)
            max_bits = max(max_bits, common.complete_bits(state))
        assert engine.rewind(state, steps).same_as(seed)
        rows.append({**common.identity(program, seed), 'steps':steps,
                     'scalar_register_comparisons':steps*seed.N*8*3,
                     'Q_exact':True, 'source_exact':True, 'all_six_carries':True,
                     'complete_inverse_and_rewind':True, 'peak_bits':max_bits})
    tensor = common.build().tensor
    assert tensor.G == 8 and len(tensor) == 9
    assert all(term.degree == 1 and term.coeff % 3 == 0 for term in tensor.monomials)
    assert all(factor.field == 'b' and factor.offset == ZERO for term in tensor.monomials for factor in term.factors)
    assert not tensor.support_violations()
    return {'cases':rows, 'allocation':{'channels':8,'integers_per_node':24,
            'linear_monomials':9,'all_support_onsite':True,'hidden_workspace_or_scheduler':0}}


def wrong_clock_review():
    """A real Engine orbit preserves Q while its proposed clock rate is wrong."""
    program = common.build()
    seed = common.prepare(program)
    bad = seed.copy()
    bad.a[5, :] = -2  # Same source history, twice the declared marker slope.
    engine, state = Engine(program.tensor), bad
    source_times, marker_times, q_values = [], [], []
    for step in range(4):
        raw = physical_oracle(program, state)
        q_values.append(str(raw['Q']))
        marker_times.append(str(raw['tau']))
        source_times.append(str(F(raw['J']-int(state.b[3,0]),6*raw['D']*program.N)))
        assert raw['Q'] == 0
        assert raw['tau'] == F(2*step,program.N)
        try:
            common.read_conserved(program,state)
        except ValueError:
            pass
        else:
            raise AssertionError('Wrong proper-time slope passed declared physical interpretation')
        if step < 3:
            old = state
            state = engine.step(state)
            assert state.same_as(scalar_oracle(old)) and engine.inverse_step(state).same_as(old)
    assert engine.rewind(state,3).same_as(bad)
    return {'tensor_sha256':program.tensor.fingerprint,
            'seed_sha256':hashlib.sha256(canonical_bytes(bad.to_dict())).hexdigest(),
            'Q_by_step':q_values, 'source_proper_time':source_times, 'wrong_marker_time':marker_times,
            'actual_Engine_steps':3,'full_rewind':True,'physical_preparation_rejected':True,
            'reason':'Conservation and reversible execution alone do not calibrate a unit-lapse proper clock.'}


def bit_cost_review():
    program = common.build()
    seed = common.prepare(program)
    initial = physical_oracle(program,seed)
    bound_constant = max(initial['W']+initial['J']+3*initial['D'],
                         max(abs(int(x)) for ar in (seed.a,seed.b,seed.r) for x in ar.flat)+1)
    rows = []
    engine, state = Engine(program.tensor), seed
    for tick in range(257):
        assert int(state.b[0,0]) == initial['W']+tick*initial['J']+3*initial['D']*tick*tick
        bound = bound_constant*(tick+1)**2
        assert max(abs(int(x)) for ar in (state.a,state.b,state.r) for x in ar.flat) <= bound
        if tick in (0,1,16,256):
            rows.append({'tick':tick,'peak_bits':common.complete_bits(state),'bound_bits':bound.bit_length()})
        if tick < 256:
            old = state
            state = engine.step(state)
            assert state.same_as(scalar_oracle(old)) and engine.inverse_step(state).same_as(old)
    assert engine.rewind(state,256).same_as(seed)
    refinements = []
    for resolution in RESOLUTIONS:
        data = common.trace(resolution)
        assert data['readouts'][-1]['tau'] == F(1,8)
        refinements.append({'N':resolution,'steps':resolution//8,'bits':max(data['bits']),
                            'V':str(data['readouts'][-1]['V']),'U':str(data['readouts'][-1]['U'])})
    assert [r['bits'] for r in refinements] == [13,15,17]
    return {'all_forward_ticks_bound':'max retained magnitude <= C*(n+1)^2',
            'C':bound_constant,'bit_growth':'O(log(n+1)+log(N)) for the declared preparation family',
            'actual_independent_256_step_oracle':rows,'fixed_time_refinement':refinements,
            'comparison_boundary':'PR60 spinor6 is a different massive-scalar model. This efficient massless anisotropic law does not replace its massive dynamics.'}


def input_and_metric_review():
    rejected = []
    def reject(name, fn):
        try:
            fn()
        except (TypeError,ValueError):
            rejected.append(name)
        else:
            raise AssertionError('Invalid input accepted: '+name)
    for bad in (True,24.0,F(24),0,-24):
        reject('invalid_N_'+repr(bad),lambda bad=bad:common.build(bad))
    program = common.build()
    reject('float_V',lambda:common.prepare(program,V=float(F(7,3))))
    reject('boolean_shear',lambda:common.prepare(program,S=(True,-1,0)))
    reject('nonzero_trace_shear',lambda:common.prepare(program,S=(1,1,1)))
    seed = common.prepare(program)
    bad = seed.copy(); bad.a[1,:] += 1
    reject('drifting_dust_history',lambda:common.read_conserved(program,bad))
    bad_r = seed.copy(); bad_r.r[0,0]=6
    reject('illegal_carry',lambda:common.read_conserved(program,bad_r))
    off = common.prepare(program,P=1)
    assert physical_oracle(program,off)['Q'] == F(9,2)
    reject('off_constraint_bundle',lambda:common.make_bundle(program,off))
    # Valid diagnostic chart near the root, with the reference in the future.
    # This caught log1p rounding to -1 in the first version of common.physical.
    huge = common.build(10**160)
    near = common.prepare(huge,V=1,U=10**80)
    near.a[3,:] = near.b[3,:] = 4*huge.N*(10**80+1)
    diagnostic = common.physical(huge,near,dps=60)
    assert mp.isfinite(diagnostic['I']) and diagnostic['I'] < 0
    assert all(mp.isfinite(x) and x > 0 for x in diagnostic['a'])
    with mp.workdps(240):
        u = mp.mpf(10)**80
        root = mp.sqrt(u*u-3)
        reference = u+1
        independent = (mp.log(u-root)-mp.log(u+root)-mp.log(reference-root)+mp.log(reference+root))/root
        relative_error = abs((diagnostic['I']-independent)/independent)
        assert relative_error < mp.mpf('1e-55')
    return {'rejected_inputs':rejected,'off_constraint_state_remains_off_constraint':True,
            'review_found_and_fixed_backward_anchor_log_cancellation':True,
            'near_branch_I':mp.nstr(diagnostic['I'],30),
            'near_branch_relative_error':mp.nstr(relative_error,10),
            'scope':'Extreme off-constraint diagnostic chart; no false physical acceptance or rational projection.'}


def evidence_review():
    names = ('native','tensor_metric','covector_geodesics','clocks','noether_spatial')
    reports = {name:json.loads((ROOT/f'runs/conservation_closure/{name}.json').read_text()) for name in names}
    checks = []
    for name,report in reports.items():
        sources = report['source_sha256']
        for filename, expected in sources.items():
            actual = hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()
            assert actual == expected, f'Stale evidence: {name}: {filename}'
            checks.append({'report':name,'source':filename,'sha256':actual})
    paths = {'native':reports['native']['cases'][:3],
             'runtime':reports['native']['runtime'],
             'metric':reports['tensor_metric']['shared_native_traces'],
             'covector_diagnostic':reports['covector_geodesics']['same_state']['runs'],
             'clock':reports['clocks']['same_candidate_cases']}
    joins = []
    for resolution in RESOLUTIONS:
        program = common.build(resolution)
        seed = common.prepare(program)
        expected = common.identity(program,seed)
        for lane,rows in paths.items():
            matches = [row for row in rows if row['N'] == resolution]
            assert len(matches) == 1, f'Ambiguous or missing resolution {lane}:{resolution}'
            row = matches[0]
            assert row['tensor_sha256'] == expected['tensor_sha256']
            assert row['seed_sha256'] == expected['seed_sha256']
            assert row['steps'] == resolution//8
            joins.append({'lane':lane,**expected})
    assert reports['covector_geodesics']['encoding']['new_retained_probe_channels'] == 0
    assert reports['covector_geodesics']['encoding']['autonomous_worldline_or_detector'] == 'not_implemented'
    assert reports['clocks']['acceptance']['transported_material_detector_and_autonomous_record'] == 'not_tested'
    # The Noether spatial proof is read and source-hashed here but its separate
    # edge tensor must never receive the Bianchi source/metric acceptance.
    expected = common.identity(common.build(),common.prepare(common.build()))
    noether = reports['noether_spatial']
    for key in ('tensor_sha256','seed_sha256','N'):
        assert noether['same_candidate_balance'][key] == expected[key]
        assert noether['same_tensor_spatial_negative'][key] == expected[key]
    assert noether['same_tensor_spatial_negative']['negative_seed_sha256'] != expected['seed_sha256']
    assert noether['same_tensor_spatial_negative']['spatial_Einstein_acceptance'] == 'failed'
    assert noether['face_continuity']['sourced_claim'] is False
    assert noether['face_continuity']['tensor_sha256'] != expected['tensor_sha256']
    return {'fresh_source_checks':checks,'same_tensor_seed_resolution_joins':joins,
            'passive_covector_diagnostics_not_retained_probe':True,
            'Noether_same_candidate_balance_join':True,
            'different_nonuniform_seed_Q_zero_does_not_imply_spatial_Einstein':True,
            'Noether_bridge_cannot_inherit_Bianchi_Einstein_acceptance':True,
            'general_spatial_source_detector_and_massive_extension':'not established'}


def main():
    result = {'schema':'universe24-conservation-closure-review-v1',
              'symbolic':symbolic_audit(), 'actual_complete_state':actual_state_review(),
              'conserved_constraint_wrong_clock':wrong_clock_review(),
              'cost':bit_cost_review(), 'input_and_metric':input_and_metric_review(),
              'evidence':evidence_review(), 'primary_readings':SOURCES,
              'source_sha256':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in (Path(__file__),Path(common.__file__))},
              'accepted_scope':'One exact native homogeneous anisotropic massless-scalar+dust solution family; no uniqueness or general Einstein/operational detector claim'}
    target = ROOT/'runs/conservation_closure/review.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','cases':len(result['actual_complete_state']['cases']),
                      'fresh_source_checks':len(result['evidence']['fresh_source_checks']),
                      'same_state_joins':len(result['evidence']['same_tensor_seed_resolution_joins']),
                      'near_branch_regression':'passed'},indent=2))


if __name__ == '__main__':
    main()
