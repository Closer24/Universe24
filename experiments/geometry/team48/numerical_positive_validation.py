"""Independent physical gates for nondegenerate44, using literal B differences.

The fixture has positive squared dust, nonzero scalar momentum and zero
initial Einstein/gradient/Gauss constraints. The two auxiliary levels are
explicitly NOT samples of a common continuum p/q history: their nonzero
Wronskian proves this. Positivity and physical accuracy are separate gates.
"""
from fractions import Fraction as F
from functools import partial as bind
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from experiments.geometry.team48 import geometry_positive_pairs as positive
from experiments.geometry.team48 import geometry_triangular as triangular
from experiments.geometry.team48 import matter_charged as charged
from experiments.geometry.team48 import matter_dust_square as square
from experiments.geometry.team48 import integer_staggered as staggered
from experiments.geometry.team48.integer_sign_lift import compile_quadratic,prepare as old_prepare,physical_slices as old_slices
from experiments.geometry.team48.numerical_sign_validation import sampled,as_array
from universe24.core import Engine,State,Tensor
from universe24.core.lattice import lattice


SOURCE=bind(square.equations,base_equations=charged.equations,mass_squared=0)
BUILDER=bind(positive.equations,fermi_equations=SOURCE)
NAMES=positive.replace_fields(square.FIELDS_CHARGED)


def constrained_seed():
    L=4;lat=lattice(L);x=lat.all_coords()[:,0]
    values=np.zeros((len(NAMES),lat.N),dtype=object)
    f=dict(zip(NAMES,values))
    for a in range(3):f[f'diag_p{a}'][:]=1
    for name,profile in {'phi':[0,2,0,-2],'Pi_phi':[2,0,2,0],
                         'Xi_phi0':[2,0,-2,0],'K11':[2,6,2,2],
                         'K22':[2,6,2,2],'dust_amplitude':[0,6,0,2]}.items():
        f[name][:]=np.asarray(profile,dtype=object)[x]
    constraints,source=literal_constraints(values,L)
    assert all(not any(np.broadcast_to(c,(lat.N,))) for c in constraints.values())
    assert np.array_equal(source['rho'],f['K11']**2)
    assert np.array_equal(source['momentum'][0],np.asarray([-4,0,4,0],dtype=object)[x])
    expected_S=np.asarray([4,0,4,0],dtype=object)[x]
    assert np.array_equal(source['stress'][0][0],expected_S)
    assert not any(source['stress'][1][1]) and not any(source['stress'][2][2])
    assert all(v>=0 for v in source['dust_density'])
    previous=values.copy();p=dict(zip(NAMES,previous))
    for a in range(3):p[f'diag_p{a}'][:]=0;p[f'diag_q{a}'][:]=1
    old_constraints,_=literal_constraints(previous,L)
    assert all(not any(np.broadcast_to(c,(lat.N,))) for c in old_constraints.values())
    return previous,values


def literal_constraints(values,L):
    # Independent reconstruction before spatial differences: do not invoke
    # positive.expand's continuum chain rule in a discrete metric observer.
    fields=dict(zip(NAMES,values))
    full=dict(fields)
    for a in range(3):full[f'B{a}{a}']=fields[f'diag_p{a}']**2+fields[f'diag_q{a}']**2
    names=tuple(n for n in square.FIELDS_CHARGED if n not in triangular.ZERO_FIELDS and n not in triangular.ALIASES)
    array=np.asarray([np.broadcast_to(full[n],(L**3,)) for n in names],dtype=object)
    _,constraints,source=sampled(names,bind(triangular.equations,fermi_equations=SOURCE),array,L)
    helper_constraints,_=positive.sampled_constraints(fields,lattice(L),fermi_equations=SOURCE)
    assert all(np.array_equal(np.broadcast_to(c,(L**3,)),np.broadcast_to(helper_constraints[n],(L**3,))) for n,c in constraints.items())
    return constraints,source


def summary(previous,current,L):
    old,now=dict(zip(NAMES,previous)),dict(zip(NAMES,current))
    W=np.asarray(positive.wronskians(old,now),dtype=object)
    diagonal=np.asarray([now[f'diag_p{a}']**2+now[f'diag_q{a}']**2 for a in range(3)],dtype=object)
    determinant=diagonal[0]*diagonal[1]*diagonal[2]
    constraints,source=literal_constraints(current,L)
    _,chain_constraints,_=sampled(NAMES,BUILDER,current,L)
    peaks={n:str(max(abs(v) for v in np.broadcast_to(c,(L**3,)))) for n,c in constraints.items()}
    defect={n:str(max(abs(v) for v in np.broadcast_to(c-chain_constraints[n],(L**3,)))) for n,c in constraints.items()}
    return {'all_constraints_zero':all(F(v)==0 for v in peaks.values()),'constraint_peaks':peaks,
            'literal_minus_chain_rule_constraint_peaks':defect,
            'minimum_diagonal_B':str(min(diagonal.flat)),'minimum_det_B':str(min(determinant)),
            'all_Wronskians_abs_one':all(abs(v)==1 for v in W.flat),
            'minimum_dust_density':str(min(source['dust_density'])),
            'peak_abs_jx':str(max(abs(v) for v in source['momentum'][0]))}


def continuum_temporal_gate():
    p,q,k=sp.symbols('p q k')
    # The same scale multiplies both amplitudes. Hence all exact times at a
    # fixed node are parallel, and their two-level Wronskian is zero.
    pdot,qdot=k*p/2,k*q/2
    assert sp.expand(p*qdot-q*pdot)==0
    c=sp.symbols('scale')
    assert sp.expand(p*(c*q)-q*(c*p))==0
    return {'continuum_amplitude_direction_constant':True,
            'exact_common_continuum_time_pair_requires_W_zero':True,
            'nonzero_W_seed_is_computational_second_mode':True,
            'controlled_refinement_to_physical_branch_established':False}


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    program=staggered.compile_staggered(NAMES,BUILDER,phase_offsets=positive.phase_offsets(NAMES))
    assert program.tensor.G==44 and not program.tensor.support_violations()
    previous,current=constrained_seed();L=4;N=L**3
    seed=staggered.prepare(program,previous,current,L=L,remainders=np.arange(44*N).reshape(44,N)%6)
    engine,state=Engine(program.tensor),seed
    prev,now=previous,current
    trace=[{'tensor':program.tensor.to_dict(),'state':seed.to_dict()}];rows=[]
    for step in range(4):
        p,c=staggered.physical_slices(program,state)
        assert np.array_equal(p,prev) and np.array_equal(c,now)
        rows.append({'update':step,**summary(p,c,L)})
        assert rows[-1]['all_Wronskians_abs_one'] and F(rows[-1]['minimum_det_B'])>0
        assert np.array_equal(state.r,seed.r)
        if step<3:
            rhs,_,_=sampled(NAMES,BUILDER,now,L)
            prev,now=now,prev+2*as_array(rhs,NAMES,N)
            state=engine.step(state);trace.append({'state':state.to_dict()})
    assert rows[0]['all_constraints_zero'] and not rows[1]['all_constraints_zero']
    assert engine.rewind(state,3).same_as(seed)
    replay=Engine(Tensor.from_dict(trace[0]['tensor']));replayed=State.from_dict(trace[0]['state'])
    for item in trace[1:]:
        replayed=replay.step(replayed)
        assert replayed.same_as(State.from_dict(item['state']))
    # Compare the first reconstructed B step with the earlier B-variable
    # leapfrog. A nonlinear variable change is not an identical integrator.
    old_names=tuple(n for n in square.FIELDS_CHARGED if n not in triangular.ZERO_FIELDS and n not in triangular.ALIASES)
    old_builder=bind(triangular.equations,fermi_equations=SOURCE)
    old_program=compile_quadratic(old_names,old_builder)
    expanded=dict(zip(NAMES,current));expanded.update({f'B{a}{a}':np.ones(N,dtype=object) for a in range(3)})
    old_values=np.asarray([expanded[n] for n in old_names],dtype=object)
    old_state=old_prepare(old_program,old_values,old_values,L=L)
    _,old_next=old_slices(old_program,Engine(old_program.tensor).step(old_state))
    _,positive_next=staggered.physical_slices(program,Engine(program.tensor).step(seed))
    node=lattice(L).index(1,0,0)
    physical_B_next=sum(positive_next[NAMES.index(f'diag_{label}1'),node]**2 for label in ('p','q'))
    ordinary_B_next=old_next[old_names.index('B11'),node]
    assert physical_B_next==37 and ordinary_B_next==13
    accessibility=[]
    for h in (F(1),F(1,2),F(1,4),F(1,8)):
        try:
            staggered.compile_staggered(NAMES,BUILDER,phase_offsets=positive.phase_offsets(NAMES),dt=h,dx=h)
            accessibility.append({'h_and_dx':str(h),'compiles':True})
        except ValueError as error:
            accessibility.append({'h_and_dx':str(h),'compiles':False,'reason':str(error)})
    paths=[Path(__file__).relative_to(ROOT),Path('experiments/geometry/team48/geometry_positive_pairs.py'),
           Path('experiments/geometry/team48/integer_staggered.py'),Path('experiments/geometry/team48/matter_dust_square.py')]
    report={'scope':'Independent actual44 Engine constrained-data test; positivity succeeds, Einstein constraints and physical-branch initialization do not',
            'invariant_summary':staggered.invariant_summary(program),'monomials':len(program.tensor.monomials),
            'parameters':{'dt':1,'dx':1,'mass_squared':0,'coupling':1},
            'seed':{'L':4,'phi':[0,2,0,-2],'Pi_phi':[2,0,2,0],'Xi_phi0':[2,0,-2,0],
                    'K11_and_K22':[2,6,2,2],'dust_amplitude':[0,6,0,2],
                    'initial_B':'I','initial_rho':'k²','initial_jx':[-4,0,4,0],
                    'charged_and_Maxwell_interaction_active':False,
                    'all_constraints_zero_on_each_initial_slice':True,
                    'previous_p_q':[0,1],'current_p_q':[1,0],
                    'exact_continuum_time_pair':False},
            'temporal_gate':continuum_temporal_gate(),'samples':rows,
            'first_decoded_B11_at_x1':int(physical_B_next),'ordinary41_first_B11_at_x1':int(ordinary_B_next),
            'joint_raw_integer_refinement':accessibility,
            'exact_rhs_agreement_rewind_and_trace_replay':True,
            'source_sha256':{str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}}
    (out/'positive44_report.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'positive44_full_trace.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in trace))
    return report


if __name__=='__main__':
    result=run(ROOT/'runs/team48/numerical')
    print(json.dumps({'channels':result['invariant_summary']['channels'],'monomials':result['monomials'],
                     'temporal_gate':result['temporal_gate'],
                     'first_update':result['samples'][1],
                     'joint_raw_integer_refinement':result['joint_raw_integer_refinement']},indent=2))
