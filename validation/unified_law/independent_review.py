"""Independent complete-state and physical review of the selected spinor law.

Run after the common/component audits. No reviewer-generated state is fed into
the candidate evolution. Wrong-law controls deliberately keep C=0 while failing
the physical equations, so algebraic closure cannot certify itself.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

from universe24.core import Engine, State
from universe24.core.lattice import ZERO
from validation.completion import formulation
from validation.geometry.team48 import refinement_integer_projective as projective
from . import common, constrained_coordinates as coordinates

ROOT = Path(__file__).resolve().parents[2]


def pair_mul(left, right):
    """Independent arithmetic in R[w]/(w^2+3), with rational coefficients."""
    return (left[0]*right[0]-3*left[1]*right[1],
            left[0]*right[1]+left[1]*right[0])


def physical_oracle(values):
    a,b,c,e,beta = (values[name] for name in coordinates.FIELDS)
    norm_u, norm_v = a*a+3*b*b, c*c+3*e*e
    inner, area = a*c+3*b*e, b*c-a*e
    return {'k': -norm_u/2-norm_v/12, 'p': inner,
            'phi': norm_u-norm_v/6-area,
            'dust': norm_u/2-norm_v/12+area, 'beta': beta}


def drift_oracle(values):
    """Two complex-pair matrix products, independent of the source RHS."""
    a,b,c,e = (values[name] for name in coordinates.FIELDS[:4])
    physical = physical_oracle(values)
    k,phi,dust = (physical[name] for name in ('k','phi','dust'))
    diagonal, offdiag = dust+2*phi, dust-phi
    block11 = (F(3,2)*k+diagonal/4, F(-1,6))
    block12 = (F(1,6), offdiag/12)
    block21 = (-1, -offdiag/2)
    block22 = (F(3,2)*k-diagonal/4, F(1,6))
    du1,du2 = pair_mul(block11,(a,b)), pair_mul(block12,(c,e))
    dv1,dv2 = pair_mul(block21,(a,b)), pair_mul(block22,(c,e))
    return dict(zip(coordinates.FIELDS,
        (du1[0]+du2[0],du1[1]+du2[1],dv1[0]+dv2[0],dv1[1]+dv2[1],k)))


def physical_constraint(values):
    return 6*values['k']**2-values['p']**2-values['phi']**2-2*values['dust']**2


def independent_symbolic_audit():
    values = dict(zip(coordinates.FIELDS, s.symbols('a b c e beta', real=True)))
    a,b,c,e = tuple(values.values())[:4]
    physical = physical_oracle(values)
    drift = drift_oracle(values)
    # Rank-one Hermitian determinant identity, not the component C function.
    assert s.expand((a*a+3*b*b)*(c*c+3*e*e)-(a*c+3*b*e)**2-3*(b*c-a*e)**2) == 0
    assert s.expand(physical_constraint(physical)) == 0
    assert all(s.expand(physical[name]-coordinates.physical(values)[name]) == 0 for name in physical)
    assert all(s.expand(drift[name]-coordinates.equations(values)[name]) == 0 for name in values)
    derivative = lambda expr: s.expand(sum(s.diff(expr,values[name])*drift[name] for name in values))
    k,p,phi,dust = (physical[name] for name in ('k','p','phi','dust'))
    # Independent FLRW/Klein-Gordon/comoving-dust target in lapse one.
    targets = {'k': (p*p+dust*dust)/2, 'p':3*k*p-phi,
               'phi':p, 'dust':F(3,2)*k*dust, 'beta':k}
    assert all(s.expand(derivative(physical[name])-targets[name]) == 0 for name in targets)
    norm = a*a+3*b*b+c*c/6+e*e/2
    assert s.expand(norm+2*k) == 0
    assert s.expand(derivative(norm)+p*p+dust*dust) == 0
    # Einstein spatial pressure also follows, independently of C itself.
    pressure = (p*p-phi*phi)/2
    assert s.expand(2*derivative(k)-3*k*k-pressure) == 0
    # A direct call to the actual full44 builder, without calling either
    # component audit or its reference_rhs helper.
    frame = s.symbols('B', positive=True)
    full = dict.fromkeys(formulation.FIELDS, s.Integer(0))
    for axis in range(3):
        full[f'B{axis}{axis}'], full[f'K{axis}{axis}'] = frame, k
    full.update(phi=phi, Pi_phi=p, dust_amplitude=dust)
    source, constraints, _ = formulation.equations(full, lambda *_: s.Integer(0), mass_squared=1)
    target = dict.fromkeys(formulation.FIELDS, s.Integer(0))
    for axis in range(3):
        target[f'B{axis}{axis}'] = frame*derivative(physical['beta'])
        target[f'K{axis}{axis}'] = derivative(k)
    target.update(phi=derivative(phi), Pi_phi=derivative(p), dust_amplitude=derivative(dust))
    assert len(source) == 44 and len(constraints) == 33
    assert all(s.expand(source[name]-target[name]) == 0 for name in source)
    assert all(s.expand(value) == 0 for value in constraints.values())
    return {'rank_one_cone_identity':True, 'independent_complex_pair_drift':True,
        'all_five_physical_evolution_equations':True,
        'direct_actual_full44_source_and_all33_constraints':True,
        'spatial_Einstein_pressure':True,
        'weighted_norm_decay':'d(-2k)/dt=-(p^2+dust^2)',
        'future_continuum_domain':'Bounded spinor norm; finite beta on every finite proper-time interval',
        'rational_seed_scope':'New representable seed; no exact rational lift of every prior full45 seed is asserted'}


def scalar_step_oracle(program, state):
    """Exact rational homogeneous recurrence, no Tensor or source evaluator."""
    after_b = np.empty_like(state.b,dtype=object)
    for node in range(state.N):
        denominator = int(state.b[0,node])
        values = {name:F(int(state.b[index+1,node]),denominator)
                  for index,name in enumerate(coordinates.FIELDS)}
        derivative = drift_oracle(values)
        predicted = [F(program.multiplier*denominator**3)]
        predicted += [program.multiplier*denominator**3*(values[name]+program.dt*derivative[name])
                      for name in coordinates.FIELDS]
        for channel, value in enumerate(predicted):
            assert value.denominator == 1
            # u=3*value, hence divmod(2u+r,6) returns(value,r) for ALL legal r.
            quotient,remainder = divmod(6*value.numerator+int(state.r[channel,node]),6)
            assert remainder == int(state.r[channel,node])
            after_b[channel,node] = quotient-int(state.a[channel,node])
    return State(state.L,state.b,after_b,state.r)


def actual_state_audit():
    program = common.build()
    assert program.tensor.G == 6 and program.degree == 3
    assert not program.tensor.support_violations()
    assert all(f.offset == ZERO and f.field == 'b' for term in program.tensor.monomials for f in term.factors)
    fixtures = [(None,4), ({'sa':F(-1,2),'sb':F(1,3),'sc':F(1,4),'se':F(-1,5),'beta':F(1,7)},420)]
    rows=[]
    for values, denominator in fixtures:
        seed = common.prepare(program,denominator=denominator,values=values)
        state,engine = seed,Engine(program.tensor)
        bits=[common.complete_bits(seed)]
        before_physical = physical_oracle(common.decode_coordinates(program,seed))
        for _ in range(3):
            old=state
            state=engine.step(old)
            assert state.same_as(scalar_step_oracle(program,old))
            assert engine.inverse_step(state).same_as(old)
            now=physical_oracle(common.decode_coordinates(program,state))
            assert now == common.decode(program,state)
            assert physical_constraint(now) == 0
            assert now['k'] <= 0 and now['beta'] <= before_physical['beta']
            before_physical=now
            bits.append(common.complete_bits(state))
        assert engine.rewind(state,3).same_as(seed)
        rows.append({**common.identity(program,seed),'steps':3,'nodes':27,
            'independent_complete_register_comparisons':3*27*6*3,
            'all_six_remainders_retained':True,'full_rewind':True,
            'exact_constraint_each_step':True,'beta_monotone':True,'bits':bits})
    return {'rows':rows,'onsite_only':True,
            'interpretation':'One homogeneous sector; no spatial packet coupling in this tensor'}


def wrong_dynamics_audit():
    seed_program=common.build()
    seed=common.prepare(seed_program)
    controls=[]
    for omitted in ('sc','beta'):
        def wrong_rhs(values,partial):
            result=drift_oracle(values)
            result[omitted]=0
            return result
        program=projective.compile_projective(coordinates.FIELDS,wrong_rhs,dt=seed_program.dt,dx=1,degree=3)
        engine=Engine(program.tensor)
        state=seed
        for _ in range(3):
            old=state
            state=engine.step(state)
            assert engine.inverse_step(state).same_as(old)
            assert physical_constraint(physical_oracle(common.decode_coordinates(program,state))) == 0
        assert engine.rewind(state,3).same_as(seed)
        initial=common.decode_coordinates(seed_program,seed)
        expected=drift_oracle(initial)
        assert expected[omitted] != 0
        physical=physical_oracle(common.decode_coordinates(program,state))
        if omitted=='beta':
            assert physical['beta']==0 and physical['k']<0
            assert (physical['p']**2+physical['phi']**2)/2+physical['dust']**2 > 0
            failure='Frozen flat metric has zero Einstein tensor but nonzero positive matter density'
        else:
            variables = dict(zip(coordinates.FIELDS,s.symbols('a b c e beta')))
            wrong_drift = wrong_rhs(variables,None)
            pdot = sum(s.diff(physical_oracle(variables)['p'],variables[name])*wrong_drift[name]
                       for name in variables)
            at_seed = {variables[name]:initial[name] for name in variables}
            assert pdot.subs(at_seed) == 0
            assert 3*physical_oracle(initial)['k']*physical_oracle(initial)['p']-physical_oracle(initial)['phi'] == -1
            failure='At the seed, pdot=0 from the wrong map, while Klein-Gordon requires pdot=-1'
        controls.append({'omitted_coordinate_velocity':omitted,'tensor_sha256':program.tensor.fingerprint,
            'actual_Engine_steps':3,'constraint_still_zero':True,'complete_rewind':True,
            'wrong_dynamics_rejected':True,'reason':failure})
    return controls


def exact_input_audit():
    # Cache equality must never bypass the public exact-type guard.
    for exact, inexact in ((F(1,32),0.03125),(F(1),True)):
        common.build(dt=exact)
        try:
            common.build(dt=inexact)
        except TypeError:
            pass
        else:
            raise AssertionError('Warm cache admitted an inexact timestep')
    return {'warm_cache_float_and_boolean_rejected':True,
            'regression':'Validate exact input types before cache lookup'}


def evidence_review():
    paths={'common':ROOT/'runs/unified_law/00_common.json',
           'coordinates':ROOT/'runs/unified_law/01_coordinates.json',
           'hamiltonian':ROOT/'runs/unified_law/02_hamiltonian.json',
           'native':ROOT/'runs/unified_law/03_native_scheduler.json',
           'invariant':ROOT/'runs/unified_law/04_invariant_map.json',
           'metric':ROOT/'runs/unified_law/05_spatial_metric.json',
           'clock':ROOT/'runs/unified_law/06_clock_acceptance.json'}
    reports={name:json.loads(path.read_text()) for name,path in paths.items()}
    source_checks=0
    source_files={'coordinates':'validation/unified_law/constrained_coordinates.py',
                  'native':'validation/unified_law/native_scheduler.py'}
    for name,report in reports.items():
        source=report['source_sha256']
        source={source_files[name]:source} if isinstance(source,str) else source
        for filename,expected in source.items():
            actual=hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()
            assert actual==expected, f'Stale evidence in {name}: {filename}'
            source_checks+=1
    program=common.build()
    seed=common.prepare(program)
    expected=common.identity(program,seed)
    keys=('tensor_sha256','seed_sha256')
    same=lambda row: all(row[key]==expected[key] for key in keys)
    assert same(reports['common'])
    assert same(reports['invariant']['actual_common_engine'])
    metric_rows=reports['metric']['actual_shared_metric']
    clock=reports['clock']['actual_shared_candidate']
    assert same(metric_rows[0]) and same(clock['rows'][0])
    assert len(metric_rows)==len(clock['rows'])==3
    invariant_rows=reports['invariant']['physical_refinement']['rows']
    assert len(invariant_rows)==3
    for metric,row,invariant in zip(metric_rows,clock['rows'],invariant_rows):
        assert all(metric[key]==row[key] for key in (*keys,'dt','steps','channels'))
        assert invariant['tensor_sha256']==row['tensor_sha256']
        assert invariant['h']==row['dt'] and invariant['steps']==row['steps']
        assert abs(invariant['physical_max_error']-row['max_field_error']) < 1e-12
        candidate=common.build(dt=F(row['dt']))
        actual=common.identity(candidate,common.prepare(candidate))
        assert all(actual[key]==row[key] for key in keys)
        assert row['exact_constraint_zero_every_macro_sample']
    assert clock['exact_discrete_dust_mass_conservation'].startswith('failed')
    assert all(row['dust_mass_error']>0 for row in clock['rows'])
    assert clock['efficient_refinement_bit_cost'].startswith('failed')
    assert clock['operational_clock_and_signal_transport']=='not_tested'
    assert reports['common']['existing_runtime_complete_states_match_scalar_oracle']
    assert all(reports['common']['runtime_report']['acceptance_gates'][g]['status']=='not_tested' for g in 'CDEF')
    native=reports['native']['actual_sourced_first_order_system']
    assert native['tensor_sha256'] != expected['tensor_sha256']
    assert native['exact_constraint_preservation']=='failed'
    assert native['fixed_time_refinement']=='not_tested'
    first={name:F(value) for name,value in native['rows'][0]['fields'].items()}
    native_constraint=-F(3,4)*first['P']**2+F(1,2)*(first['Pi']**2+first['r']**2)+first['v']
    assert native_constraint==F(-4,9)==F(native['rows'][0]['constraint'])
    # Invalid same-run claims: another h or another complete carried seed.
    wrong=dict(expected,tensor_sha256=common.build(dt=F(1,32)).tensor.fingerprint)
    assert not same(wrong)
    changed=seed.copy() if hasattr(seed,'copy') else State(seed.L,seed.a.copy(),seed.b.copy(),seed.r.copy())
    changed.r[0,0]=(int(changed.r[0,0])+1)%6
    assert not same(common.identity(program,changed))
    return {'source_hash_checks':source_checks,'default_identity':expected,
        'common_metric_clock_exact_same_run':True,
        'three_resolution_family_joins':True,'wrong_timestep_or_carry_join_rejected':True,
        'finite_step_dust_drift_remains_failed':True,
        'separate_native_first_constraint_failure':'-4/9; not joined to the spinor theorem',
        'generic_physical_gates_not_promoted':True,
        'evidence_sha256':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths.values()}}


def main():
    result={'selected_candidate':'spinor_beta_mass1','independent_symbolic':independent_symbolic_audit(),
        'actual_state':actual_state_audit(),'wrong_dynamics_controls':wrong_dynamics_audit(),
        'exact_input':exact_input_audit(),
        'provenance':evidence_review(),
        'source_sha256':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (Path(__file__),Path(common.__file__),Path(coordinates.__file__),
                         Path(formulation.__file__),Path(formulation.previous.__file__),
                         Path(projective.__file__),ROOT/'universe24/core/engine.py')},
        'review':'passed for the declared homogeneous candidate and its evidence boundaries',
        'open_gates':['Exact finite-step Einstein dynamics/source conservation is not claimed.',
            'The compiled projective bit cost remains exponential in tick count.',
            'No general spatial Einstein system, transported material packet or operational detector is implemented.',
            'Any native harmonic alternative must be checked on its own tensor and decoder.']}
    path=ROOT/'runs/unified_law/07_review.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
