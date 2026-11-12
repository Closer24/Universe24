"""Source-only full-frame metric-domain proof and actual Rule3 controls.

The cubic candidate is a DISTINCT tensor from formulation.build45. Its local
h*K*K*B correction is consistent as h -> 0, not constraint-vanishing at finite h.
All inverses below belong to passive validation, never the compiled Engine.
Run: python -m validation.completion.metric_domain
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

from universe24.core import Engine, State
from validation.completion import formulation
from validation.geometry.team48 import refinement_integer_projective as projective

ROOT = Path(__file__).resolve().parents[2]
FIELDS = formulation.FIELDS


def equations(fields, partial, *, dt=F(1, 16), mass_squared=1,
              cosmological=0, coupling=1):
    """Prepared polynomial metric repair; unchanged matter/K/G equations."""
    rhs, constraints, diagnostic = formulation.equations(fields, partial,
        mass_squared=mass_squared, cosmological=cosmological, coupling=coupling)
    rhs = dict(rhs)
    K = lambda a, b: fields[f'K{min(a,b)}{max(a,b)}']
    for a in range(3):
        for i in range(3):
            rhs[f'B{a}{i}'] += F(dt)*sum(K(a,b)*K(b,c)*fields[f'B{c}{i}']
                for b in range(3) for c in range(3))
    return rhs, constraints, diagnostic


def build45(*, dt=F(1, 16), dx=F(1, 4), mass_squared=1,
            cosmological=0, coupling=1):
    """One local cubic integer tensor: 44 physical fields plus denominator."""
    def rhs(fields, partial):
        return equations(fields, partial, dt=dt, mass_squared=mass_squared,
            cosmological=cosmological, coupling=coupling)
    return projective.compile_projective(FIELDS, rhs, dt=dt, dx=dx, degree=3)


def matrix(values, prefix, node=0):
    def entry(a,b):
        name = f'{prefix}{min(a,b)}{max(a,b)}' if prefix == 'K' else f'{prefix}{a}{b}'
        return s.Rational(values[FIELDS.index(name), node])
    return s.Matrix(3, 3, entry)


def bits(state):
    return max(abs(int(v)).bit_length() for ar in (state.a,state.b,state.r) for v in ar.flat)


def fixture(L=3):
    """Inhomogeneous exact full frames/matter, not a constraint-solved seed."""
    values = np.empty((len(FIELDS), L**3), dtype=object)
    for j,name in enumerate(FIELDS):
        for node in range(L**3):
            values[j,node] = F(((j*7+node*11)%9)-4,16)
    for node in range(L**3):
        for a in range(3):
            values[FIELDS.index(f'B{a}{a}'),node] += 1
        assert matrix(values, 'B', node).det() > 0
    return values


def seed(program, values, L=3, denominator=16):
    r = np.array([[(g+node)%6 for node in range(L**3)] for g in range(45)],dtype=object)
    return projective.prepare(program, values, L=L, denominator=denominator, remainders=r)


def symbolic_audit():
    h=s.Symbol('h', positive=True)
    fields=dict(zip(FIELDS,s.symbols('v:44',real=True)))
    jets=dict(zip(FIELDS,s.symbols('j:44',real=True)))
    n=s.symbols('n:3',real=True)
    # equations accepts exact prepared rational h; symbolic coefficient is
    # reconstructed transparently here for its consistency/principal identity.
    K=s.Matrix(3,3,lambda a,b:fields[f'K{min(a,b)}{max(a,b)}'])
    B=s.Matrix(3,3,lambda a,i:fields[f'B{a}{i}'])
    correction=h*K*K*B
    assert correction.diff(h).subs(h,0)==K*K*B
    assert correction.subs(h,0)==s.zeros(3)
    assert correction.reshape(9,1).jacobian(list(jets.values()))==s.zeros(9,44)
    R=s.eye(3)+h*K+h*h*K*K
    assert (R-(h*K+s.eye(3)/2)**2-3*s.eye(3)/4).applyfunc(s.expand)==s.zeros(3)
    # Baseline vacuum rank-one K satisfies EVERY returned continuum constraint.
    f={name:s.Integer(0) for name in FIELDS}
    for a in range(3): f[f'B{a}{a}']=s.Integer(1)
    f['K00']=s.Integer(-16)
    _,constraints,_=formulation.equations(f,lambda *_:s.Integer(0))
    assert all(s.expand(v)==0 for v in constraints.values())
    # Positive diagonal amplitudes alone cannot protect a full determinant.
    positive_diagonal_singular=s.Matrix([[1,1,0],[1,1,0],[0,0,1]])
    assert positive_diagonal_singular.det()==0
    return {'principal_change_exactly_zero':True,'correction_vanishes_as_h_to_zero':True,
        'R_complete_square_identity':True,'vacuum_negative_seed_constraints_zero':True,
        'positive_diagonal_is_not_full_determinant_protection':True,
        'finite_h_constraint_vanishing_correction':False}


def constraint_defect_audit():
    """Exact sourced-TT witness: the cubic correction is not constraint zero."""
    q,h,t,eps=s.symbols('q h t eps',real=True)
    background=formulation.homogeneous_background(sourced=True)
    names,C,L,Cdot=formulation.linear_constraint_matrices(background,(0,0,q))
    v=s.zeros(len(FIELDS),1)
    v[FIELDS.index('K00')],v[FIELDS.index('K11')]=1,-1
    assert C*v==s.zeros(len(names),1)
    assert (Cdot+C*L)*v==s.zeros(len(names),1)
    # h*(K deltaK+deltaK K)*B at K=-I,B=I is -2h deltaK.
    added=s.zeros(len(FIELDS),1)
    added[FIELDS.index('B00')],added[FIELDS.index('B11')]=-2*h,2*h
    # Verify separately that changing the homogeneous background drift by
    # h*K²B=hI adds no Cdot contribution on this particular TT vector.
    changed={name:background[name]+eps*v[j]+t*h*int(name.startswith('B') and name[1]==name[2])
             for j,name in enumerate(FIELDS)}
    _,constraints,_=formulation.equations(changed,
        lambda name,axis:eps*s.I*(q if axis==2 else 0)*v[FIELDS.index(name)])
    assert all(s.diff(value,eps,t).subs({eps:0,t:0})==0 for value in constraints.values())
    defects={names[i]:s.simplify(value) for i,value in enumerate(C*added) if value!=0}
    assert defects=={'C020':2*s.I*h*q,'C121':-2*s.I*h*q}
    return {'status':'passed_negative_control','initial_TT_linear_constraints_zero':True,
        'original_constraint_velocity_zero_for_this_mode':True,
        'cubic_added_constraint_velocity':{name:str(value) for name,value in defects.items()},
        'finite_h_continuum_constraint_invariance_for_cubic_candidate':'failed',
        'scope':'Sourced isotropic background B=I,K=-I,Pi_phi=2,dust=1; TT K00=-K11, direction z'}


def baseline_negative_control():
    program=formulation.build45()
    values=np.zeros((len(FIELDS),27),dtype=object)
    for a in range(3): values[FIELDS.index(f'B{a}{a}')]=1
    values[FIELDS.index('K00')]=-16
    initial=seed(program,values)
    engine=Engine(program.tensor)
    after=engine.step(initial)
    assert after.same_as(formulation.previous.scalar_oracle(program.tensor,initial))
    assert engine.inverse_step(after).same_as(initial)
    B=matrix(projective.readout(program,after),'B')
    assert B==s.diag(0,1,1)
    repaired=build45()
    other=seed(repaired,values)
    restored=Engine(repaired.tensor).step(other)
    B_fixed=matrix(projective.readout(repaired,restored),'B')
    assert B_fixed==s.eye(3)
    return {'status':'passed_negative_control','original_tensor_sha256':program.tensor.fingerprint,
        'repaired_tensor_sha256':repaired.tensor.fingerprint,'original_det_after':'0',
        'repaired_det_after':str(B_fixed.det()),'continuum_B00_at_h':'1/2',
        'initial_all_continuum_constraints_zero':True,'independent_scalar_oracle':True,
        'singular_state_still_exactly_rewinds':True,'original_global_metric_preservation':'failed'}


def engine_audit(steps=4):
    program=build45()
    tensor=program.tensor
    assert tensor.G==45 and tensor.rank-1==3 and not tensor.support_violations()
    assert not any(f.field=='a' for term in tensor.monomials for f in term.factors)
    initial=seed(program,fixture())
    engine,state=Engine(tensor),initial
    records=[]
    for tick in range(steps):
        before=projective.readout(program,state)
        D,Da=int(state.b[0,0]),int(state.a[0,0])
        expected=formulation.previous.scalar_oracle(tensor,state)
        after=engine.step(state)
        assert after.same_as(expected) and engine.inverse_step(after).same_as(state)
        assert np.array_equal(after.r,initial.r)
        Dnext=int(after.b[0,0])
        assert Dnext==program.multiplier*D**3-Da and Dnext>D>=2 and 0<=Da<D
        eps=s.Rational(Da,Dnext)
        assert 0<=eps<=s.Rational(1,7)
        current=projective.readout(program,after)
        for node in range(state.N):
            B,K=matrix(before,'B',node),matrix(before,'K',node)
            Bnext=matrix(current,'B',node)
            R=s.eye(3)+s.Rational(program.dt)*K+s.Rational(program.dt)**2*K*K
            if Da:
                previous=np.array([F(int(v),Da) for v in state.a[1:].flat],dtype=object).reshape(state.a[1:].shape)
                Bold=matrix(previous,'B',node)
                predicted=(1+eps)*R*B-eps*Bold
            else:
                predicted=R*B
            assert Bnext==predicted and Bnext.det()>0
            # Exact rational Sylvester certificate for ||B*Bnext^-1||_2 < 2.
            X=B*Bnext.inv()
            norm_certificate=4*s.eye(3)-X.T*X
            assert all(norm_certificate[:j,:j].det()>0 for j in (1,2,3))
        records.append({'tick':tick+1,'denominator_bits':Dnext.bit_length(),
            'max_retained_bits':bits(after),'all_nodes_positive_orientation':True,
            'history_operator_norm_bound_2_exact':True,'epsilon_le_1_over_7_exact':True})
        state=after
    assert engine.rewind(state,steps).same_as(initial)
    # The proof requires prepared zero old memory. Legal arbitrary retained
    # memory can cancel a next frame row, even with a positive current frame.
    bad=initial.copy()
    first=engine.step(bad)
    altered_a=np.array(bad.a,dtype=object)
    for a in range(3):
        for i in range(3):
            index=1+FIELDS.index(f'B{a}{i}')
            altered_a[index]=first.b[index]
    invalid_history=State(bad.L,altered_a,bad.b,bad.r)
    cancelled=engine.step(invalid_history)
    assert matrix(projective.readout(program,cancelled),'B').det()==0
    assert engine.inverse_step(cancelled).same_as(invalid_history)
    return {'status':'passed','channels':tensor.G,'retained_integers_per_node':3*tensor.G,
        'degree':tensor.rank-1,'monomials':len(tensor),'static_multiplier':program.multiplier,
        'tensor_sha256':tensor.fingerprint,'strict_single_face_support':True,'old_a_inputs':False,
        'mass_squared':1,'nodes':initial.N,'steps':steps,'records':records,
        'independent_scalar_oracle':True,'all_six_carries_and_full_rewind':True,
        'seed':'inhomogeneous rational full frame and nonzero matter; not constraint solved',
        'zero_old_memory_assumption_negative_control':'passed: arbitrary old memory can produce det=0',
        'global_metric_domain_theorem':'passed under stated initialization, C>=2, D0>=2, symmetric K',
        'uniform_infinite_time_conditioning':'not_established',
        'nonlinear_discrete_Einstein_constraints':'not_established',
        'convergence_and_time_stability':'not_established',
        'retained_apparatus':'not_implemented','bit_cost':'cubic projective growth remains exponential'}


def main():
    result={'scope':'Distinct source-only cubic metric candidate; no accepted physical model',
        'baseline':formulation.BASE_PIN,'symbolic':symbolic_audit(),
        'constraint_defect':constraint_defect_audit(),
        'negative_control':baseline_negative_control(),'actual_Engine':engine_audit()}
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__),ROOT/'validation/completion/formulation.py',
                  ROOT/'validation/geometry/team48/refinement_integer_projective.py')}
    path=ROOT/'runs/completion/03_metric_domain.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
