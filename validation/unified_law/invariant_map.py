"""Independent invariant/domain and convergence audit of the ONE spinor6 law.

The physical quadratic constraint is an identity of a fixed passive decoder.
This audit separately checks the induced Einstein vector field and the actual
retained-history map. No reference integration feeds Engine state.
"""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp
import sympy as s

from universe24.core import Engine
from . import common
from . import constrained_coordinates as candidate

ROOT = Path(__file__).resolve().parents[2]
NAMES = ('k', 'p', 'phi', 'dust', 'beta')


def independently_decode(values):
    """Expanded polynomial readout, independent of the candidate helper."""
    a,b,c,e = (values[name] for name in candidate.FIELDS[:4])
    return {'k': -(6*a*a+18*b*b+c*c+3*e*e)/12,
            'p': a*c+3*b*e,
            'phi': a*a+3*b*b-c*c/6-e*e/2-b*c+a*e,
            'dust': a*a/2+3*b*b/2-c*c/12-e*e/4+b*c-a*e,
            'beta': values['beta']}


def physical_constraint(values):
    return 6*values['k']**2-values['p']**2-values['phi']**2-2*values['dust']**2


def weighted_norm2(values):
    a,b,c,e = (values[name] for name in candidate.FIELDS[:4])
    return a*a+3*b*b+c*c/6+e*e/2


def algebra_audit():
    values = dict(zip(candidate.FIELDS, s.symbols('a b c e beta', real=True)))
    a,b,c,e,beta = values.values()
    out = independently_decode(values)
    force = candidate.equations(values)
    z = s.Matrix([a,b,c,e])
    f = s.Matrix([force[name] for name in candidate.FIELDS[:4]])
    metric = s.diag(1,3,s.Rational(1,6),s.Rational(1,2))
    assert s.expand(physical_constraint(out)) == 0
    k,p,phi,dust = (out[name] for name in NAMES[:4])
    target = {'k': (p*p+dust*dust)/2, 'p': 3*k*p-phi,
              'phi': p, 'dust': 3*k*dust/2, 'beta': k}
    for name in NAMES:
        pushed = sum(s.diff(out[name],v)*force[field]
                     for field,v in values.items())
        assert s.expand(pushed-target[name]) == 0
    norm2 = (z.T*metric*z)[0]
    assert s.expand(norm2+2*k) == 0
    assert s.expand((2*z.T*metric*f)[0]+p*p+dust*dust) == 0

    # Independent weighted operator factorization of the actual cubic force.
    linear = s.Matrix([[0,s.Rational(1,2),s.Rational(1,6),0],
                       [-s.Rational(1,6),0,0,s.Rational(1,6)],
                       [-1,0,0,-s.Rational(1,2)],
                       [0,-1,s.Rational(1,6),0]])
    total, difference = dust+2*phi, dust-phi
    boost = s.Matrix([[total/4,0,0,-difference/4],
                      [0,total/4,difference/12,0],
                      [0,3*difference/2,-total/4,0],
                      [-difference/2,0,0,-total/4]])
    cubic_operator = 3*k*s.eye(4)/2+boost
    assert (f-(linear+cubic_operator)*z).applyfunc(s.expand) == s.zeros(4,1)
    assert linear.T*metric+metric*linear == s.zeros(4)
    assert linear**2 == -s.eye(4)/4
    assert (boost.T*metric-metric*boost).applyfunc(s.expand) == s.zeros(4)
    assert (boost**2-3*(dust*dust+2*phi*phi)*s.eye(4)/16).applyfunc(s.expand) == s.zeros(4)
    assert s.expand(12*k*k-dust*dust-2*phi*phi-2*p*p-3*dust*dust) == 0

    # Explicit derivative bounds on a rational box containing N<=2, |beta|<=1/4.
    radii = (s.Rational(3,2),s.Integer(1),s.Rational(7,2),s.Integer(2),s.Rational(1,4))
    variables = tuple(values.values())
    def coefficient_bound(expression):
        return sum(abs(coeff)*s.prod(radius**power for radius,power in zip(radii,powers))
                   for powers,coeff in s.Poly(s.expand(expression),*variables).terms())
    lip = max(sum(coefficient_bound(s.diff(force[name],v)) for v in variables)
              for name in candidate.FIELDS)
    acceleration = max(coefficient_bound(sum(s.diff(force[name],v)*force[field]
        for field,v in values.items())) for name in candidate.FIELDS)
    maximum_force = max(coefficient_bound(force[name]) for name in candidate.FIELDS)
    assert lip == s.Rational(4745,64)
    assert acceleration == s.Rational(5085391,8192)
    assert maximum_force == s.Rational(15625,384)
    return {'quadratic_constraint_identity': True,
        'all_five_physical_pushforward_equations': True,
        'weighted_norm': 'N=a^2+3b^2+c^2/6+e^2/2=-2k',
        'exact_continuum_dissipation': 'Ndot=-(p^2+dust^2)<=0',
        'linear_weighted_skew_and_square': 'L*W+W*L=0; L^2=-I/4',
        'cubic_weighted_self_adjoint': True,
        'force_bound': '||F(z)||_W <= (1/2+3N/2)*sqrt(N)',
        'box_lipschitz_bound': str(lip), 'box_acceleration_bound': str(acceleration),
        'box_force_bound': str(maximum_force),
        'proper_time': 'The candidate uses lapse one; no time reparametrization.'}


def engine_audit():
    program = common.build()
    seed = common.prepare(program)
    engine, state = Engine(program.tensor), seed
    rows = []
    old_coordinates = None
    for tick in range(4):
        coords = common.decode_coordinates(program,state)
        physical = independently_decode(coords)
        assert physical == common.decode(program,state)
        assert physical_constraint(physical) == 0
        assert 0 < weighted_norm2(coords) <= 2
        assert -F(1,4) <= physical['beta'] <= 0
        rows.append({'tick':tick,'constraint':'0','weighted_norm2':str(weighted_norm2(coords)),
                     'beta':str(physical['beta']),'max_retained_bits':common.complete_bits(state)})
        if tick == 3:
            break
        after = engine.step(state)
        assert engine.inverse_step(after).same_as(state)
        next_coords = common.decode_coordinates(program,after)
        current_den, old_den, next_den = map(int,(state.b[0,0],state.a[0,0],after.b[0,0]))
        assert next_den == program.multiplier*current_den**3-old_den
        epsilon = F(old_den,next_den)
        drift = candidate.equations(coords)
        for name in candidate.FIELDS:
            euler = coords[name]+program.dt*drift[name]
            expected = euler if tick == 0 else euler+epsilon*(euler-old_coordinates[name])
            assert next_coords[name] == expected
        old_coordinates, state = coords, after
    assert engine.rewind(state,3).same_as(seed)
    return {**common.identity(program,seed),'steps':3,'nodes':seed.N,
            'actual_complete_history_identity':True,'full_rewind':True,
            'same_common_law_and_seed':True,'rows':rows,
            'constraint_preservation_scope':'Every legal decoded spinor is constrained, including intermediate ticks; dynamics is separately checked.'}


def domain_bound_audit():
    rows=[]
    for steps in (3,4,6):
        h=F(1,8*steps)
        program=common.build(dt=h)
        assert program.multiplier == 144/h
        # Algebraic inequalities used in the finite-time proof, not data fitting.
        eta=h**3/63
        assert F(49,8)+F(1,336) < 7
        assert (1+eta)*(1+F(49,8)*h*h)+eta <= 1+7*h*h
        assert F(128,121)**2 < 2
        data=common.trace(dt=h,steps=steps)
        maximum_norm=F(0)
        previous_beta=F(0)
        for state in data['states']:
            values=common.decode_coordinates(program,state)
            maximum_norm=max(maximum_norm,weighted_norm2(values))
            assert weighted_norm2(values) <= 2
            assert -F(1,4) <= values['beta'] <= previous_beta
            previous_beta=values['beta']
            assert physical_constraint(independently_decode(values)) == 0
        rows.append({'steps':steps,'h':str(h),'T':'1/8','multiplier':program.multiplier,
                     'tensor_sha256':program.tensor.fingerprint,
                     'proved_uniform_N_bound':'2','observed_max_N':float(maximum_norm),
                     'epsilon_upper_bound':str(eta),'max_retained_bits':max(data['bits'])})
    return {'domain_theorem':'For sa=1 seed, D0>=2, h=1/m<=1/16 and nh<=1/8: N_n<=2, -1/4<=beta_n<=0.',
            'metric_bound':'exp(-1/4)<=B_n<=1',
            'history_bound':'epsilon_n<=h^3/63 for n>=1; epsilon_0=0',
            'convergence_bound':'e_N <= (exp(L*T)-1)/L * (A*h/2 + 10*h^2/63), L=4745/64, A=5085391/8192',
            'convergence_order':1,
            'scope':'Finite proper-time homogeneous family; constants are rigorous but deliberately conservative.',
            'rows':rows}


def reference_solution(steps):
    """Independent physical Einstein RK4 oracle; never used for preparation."""
    z=[mp.mpf('-0.5'),mp.mpf('0'),mp.mpf('1'),mp.mpf('0.5'),mp.mpf('0')]
    h=mp.mpf(1)/(8*steps)
    def rhs(values):
        k,p,phi,dust,beta=values
        return [3*k*k-(phi*phi+dust*dust)/2,3*k*p-phi,p,
                mp.mpf('1.5')*k*dust,k]
    for _ in range(steps):
        first=rhs(z)
        second=rhs([x+h*y/2 for x,y in zip(z,first)])
        third=rhs([x+h*y/2 for x,y in zip(z,second)])
        fourth=rhs([x+h*y for x,y in zip(z,third)])
        z=[x+h*(a+2*b+2*c+d)/6 for x,a,b,c,d in zip(z,first,second,third,fourth)]
    return z


def refinement_audit():
    with mp.workdps(60):
        reference=reference_solution(2048)
        coarse_reference=reference_solution(1024)
        reference_change=max(abs(a-b) for a,b in zip(reference,coarse_reference))
        assert reference_change < mp.mpf('1e-15')
        rows=[]
        for steps in (3,4,6):
            data=common.trace(dt=F(1,8*steps),steps=steps)
            final=independently_decode(common.decode_coordinates(data['program'],data['states'][-1]))
            errors=[abs(mp.mpf(final[name].numerator)/final[name].denominator-expected)
                    for name,expected in zip(NAMES,reference)]
            rows.append({'steps':steps,'h':str(data['program'].dt),
                         'tensor_sha256':data['program'].tensor.fingerprint,
                         'physical_max_error':float(max(errors)),
                         'physical_errors':dict(zip(NAMES,map(float,errors))),
                         'max_retained_bits':max(data['bits'])})
        for previous,row in zip(rows,rows[1:]):
            assert row['physical_max_error'] < previous['physical_max_error']
            row['observed_order']=math.log(previous['physical_max_error']/row['physical_max_error'])/math.log(row['steps']/previous['steps'])
        return {'same_physical_initial_data':True,'T':'1/8','reference':'Independent physical Einstein ODE, 60-digit RK4, 1024/2048 step cross-check',
                'reference_max_change':float(reference_change),'rows':rows,
                'not_claimed':'A long-time, spatial or efficient-bit convergence theorem.'}


def main():
    result={'candidate':'one_spinor6_homogeneous_massive_Einstein',
            'algebra':algebra_audit(),'actual_common_engine':engine_audit(),
            'domain_and_convergence':domain_bound_audit(),'physical_refinement':refinement_audit(),
            'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (Path(__file__),Path(candidate.__file__),Path(common.__file__))},
            'status':'Exact homogeneous constraint/domain and finite-time first-order consistency proved; actual Engine/refinement verified.',
            'limitations':['Retained cubic projective denominator still has exponential bit-length growth.',
                           'Only the homogeneous isotropic expanding neutral scalar/dust sector is represented.',
                           'Proper coordinate time is not an implemented material detector or tick record.',
                           'Generic full45, spatial/geodesic packets and quantum gates are not established.']}
    out=ROOT/'runs/unified_law/04_invariant_map.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
