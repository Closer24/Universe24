"""Independent arithmetic and physical gates for the 25/36-channel sign lift.

Actual integer Engine trajectories are compared with the existing 48-channel
vacuum encoding and a direct Fraction-valued evaluation of the physical RHS.
A periodic integer matter slice has independently derived H=M=0, nonzero
momentum and exactly closed scalar gradients. Its initial *pair* is not claimed
to be two samples of an exact Einstein solution. No production code is changed.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from experiments.geometry.team48.integer_sign_lift import compile_quadratic, prepare as sign_prepare, physical_slices, invariant_summary
from experiments.geometry.team48.matter_equations import FIELDS as MATTER_FIELDS, equations as matter_equations
from universe24.algebra.frame_equations import FIELDS as VACUUM_FIELDS, equations as vacuum_equations
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.layers.frame48 import compile_frame48
from universe24.observe.frame48 import bank_values, diagnostics
from universe24.prepare.frame48 import flat_values, prepare as frame_prepare


def sampled(names, builder, values, L, dx=F(1)):
    lat = lattice(L)
    field = dict(zip(names, np.asarray(values, dtype=object)))
    def partial(name, axis):
        off = tuple(int(i == axis) for i in range(3))
        neg = tuple(-v for v in off)
        return (field[name][lat.shift_index(off)] - field[name][lat.shift_index(neg)])/(2*dx)
    return builder(field, partial)


def matter_builder(fields, partial):
    return matter_equations(fields, partial, mass_squared=0)


def as_array(rhs, names, N):
    return np.asarray([np.broadcast_to(rhs[name], (N,)) for name in names], dtype=object)


def vacuum_equivalence():
    L, N = 3, 27
    reports = []
    for label, dt, dx in [('arbitrary_nonuniform', F(1), F(1)), ('exact_milne_pair', F(1,2), F(1,2))]:
        old, now = flat_values(L), flat_values(L)
        if label == 'exact_milne_pair':
            old[VACUUM_FIELDS.index('B00')] = 2
            old[VACUUM_FIELDS.index('K00')] = -2
            now[VACUUM_FIELDS.index('K00')] = -1
        else:
            # Arbitrary invalid data test the full algebraic stencil, including
            # nonuniform/off-diagonal products, not the Einstein constraint gate.
            rng = np.random.default_rng(7024)
            old += rng.integers(-1,2,old.shape).astype(object)
            now += rng.integers(-1,2,now.shape).astype(object)
        small = compile_quadratic(VACUUM_FIELDS, vacuum_equations, dt=dt, dx=dx)
        large = compile_frame48(dt=dt, dx=dx)
        phase_results = []
        for phase in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            seed_s = sign_prepare(small, old, now, L=L, phase=phase,
                remainders=np.arange(25*N).reshape(25,N)%6)
            seed_l = frame_prepare(large,old,now,L=L,
                remainders=np.arange(48*N).reshape(48,N)%6)
            state_s, state_l = seed_s, seed_l
            engine_s, engine_l = Engine(small.tensor), Engine(large.tensor)
            singular=[]
            for step in range(5):
                p,c = physical_slices(small,state_s)
                assert np.array_equal(p,bank_values(state_l,'X'))
                assert np.array_equal(c,bank_values(state_l,'Y'))
                if label == 'exact_milne_pair':
                    report = diagnostics(c,L=L,dx=dx)
                    assert report['all_discrete_constraints_zero']
                    if report['singular_nodes']: singular.append(step)
                assert np.array_equal(state_s.r, seed_s.r)
                if step < 4:
                    state_s, state_l = engine_s.step(state_s), engine_l.step(state_l)
            assert engine_s.rewind(state_s,4).same_as(seed_s)
            assert engine_l.rewind(state_l,4).same_as(seed_l)
            phase_results.append({'phase':phase,'updates_equal':4,'exact_rewind':True,
                                  'singular_updates':singular})
        reports.append({'case':label,'channels_old':48,'channels_new':25,
                        'phase_results':phase_results})
    return reports


def momentum_seed(L=5):
    """Integer constrained slice by a direct flat-frame calculation.

    phi=4*f(x), Pi=2, psi=Dphi, k=phi+10, K=diag(0,k,k),
    dust=k^2-(4+psi^2)/2. Then H_geom=2k^2=2rho and
    Mx=-2Dk=-2psi=jx; all gradient/torsion/curl constraints vanish.
    These are finite-difference identities, not exact continuum sampling.
    """
    lat=lattice(L)
    values=np.zeros((len(MATTER_FIELDS),lat.N),dtype=object)
    for axis in range(3): values[MATTER_FIELDS.index(f'B{axis}{axis}')]=1
    field=dict(zip(MATTER_FIELDS,values))
    # Lattice x-coordinate independently recovered from the public coordinates.
    profile=np.asarray([0,1,2,1,0],dtype=object)
    assert L==5
    field['phi'][:]=4*profile[lat.all_coords()[:,0]]
    off=(1,0,0); neg=(-1,0,0)
    psi=F(1,2)*(field['phi'][lat.shift_index(off)]-field['phi'][lat.shift_index(neg)])
    assert all(F(v).denominator==1 for v in psi)
    field['Psi_phi0'][:]=psi
    field['Pi_phi'][:]=2
    k=field['phi']+10
    field['K11'][:]=k; field['K22'][:]=k
    rho_scalar=F(1,2)*(4+psi*psi)
    field['rho_dust'][:]=k*k-rho_scalar
    # Independent ADM normal-frame source components on this slice.
    expected_rho=k*k
    expected_j=[-2*psi,np.zeros(lat.N,dtype=object),np.zeros(lat.N,dtype=object)]
    expected_S=[[np.zeros(lat.N,dtype=object) for _ in range(3)] for _ in range(3)]
    expected_S[0][0]=F(1,2)*(4+psi*psi)
    expected_S[1][1]=expected_S[2][2]=F(1,2)*(4-psi*psi)
    assert all(v>=0 for v in field['rho_dust'])
    rhs,constraints,source=sampled(MATTER_FIELDS,matter_builder,values,L)
    assert np.array_equal(source['rho'],expected_rho)
    assert all(np.array_equal(source['momentum'][a],expected_j[a]) for a in range(3))
    assert all(np.array_equal(source['stress'][a][b],expected_S[a][b]) for a in range(3) for b in range(3))
    assert all(not any(np.broadcast_to(v,(lat.N,))) for v in constraints.values())
    assert max(abs(v) for v in source['momentum'][0])>0
    assert all(F(v).denominator==1 for v in values.flat)
    values=np.asarray([[int(v) for v in row] for row in values],dtype=object)
    return values, {'L':L,'phi_profile':[0,4,8,4,0], 'k_profile':[10,14,18,14,10],
                    'Pi_phi':2,'peak_abs_jx':str(max(abs(v) for v in expected_j[0])),
                    'rho_dust_min':str(min(field['rho_dust'])),
                    'source_rho_j_S_independently_verified':True,
                    'all_discrete_constraints_initially_zero':True,
                    'temporal_pair_is_exact_continuum_history':False}


def numerical_summary(values,L):
    _,constraints,source=sampled(MATTER_FIELDS,matter_builder,values,L)
    peak={name:str(max(abs(v) for v in np.broadcast_to(row,(L**3,)))) for name,row in constraints.items()}
    geometry=diagnostics(values[:24],L=L)
    return {'peak_constraints':peak,
            'all_discrete_constraints_zero': all(F(v)==0 for v in peak.values()),
            'peak_abs_jx':str(max(abs(v) for v in source['momentum'][0])),
            'minimum_rho':str(min(source['rho'])),
            'singular_nodes':geometry['singular_nodes'],
            'minimum_abs_det_B':geometry['minimum_abs_det_B'],
            'max_field_absolute_value':str(max(abs(v) for v in values.flat))}


def sourced_runs(out):
    L,N=5,125
    current,seed_report=momentum_seed(L)
    program=compile_quadratic(MATTER_FIELDS,matter_builder)
    rhs,_,_=sampled(MATTER_FIELDS,matter_builder,current,L)
    derivative=as_array(rhs,MATTER_FIELDS,N)
    assert all(F(v).denominator==1 for v in derivative.flat)
    derivative=np.asarray([[int(v) for v in row] for row in derivative],dtype=object)
    cases=[]
    for label,previous in [('repeated_constrained_slices',current.copy()),
                           ('backward_first_order_derivative_match',current-derivative)]:
        seed=sign_prepare(program,previous,current,L=L,
                          remainders=np.arange(36*N).reshape(36,N)%6)
        state,engine=seed,Engine(program.tensor)
        reference_previous,reference_current=previous.copy(),current.copy()
        trace=[{'tensor':program.tensor.to_dict(),'state':seed.to_dict()}]
        rows=[]
        previous_report=numerical_summary(previous,L)
        for step in range(4):
            decoded_previous,decoded_current=physical_slices(program,state)
            assert np.array_equal(decoded_previous,reference_previous)
            assert np.array_equal(decoded_current,reference_current)
            assert all(isinstance(v,(int,np.integer)) for v in state.a.flat)
            assert all(isinstance(v,(int,np.integer)) for v in state.b.flat)
            assert np.array_equal(state.r,seed.r)
            rows.append({'update':step,**numerical_summary(decoded_current,L)})
            if step<3:
                rhs,_,_=sampled(MATTER_FIELDS,matter_builder,reference_current,L)
                reference_previous,reference_current=reference_current,reference_previous+2*as_array(rhs,MATTER_FIELDS,N)
                following=engine.step(state)
                assert engine.inverse_step(following).same_as(state)
                state=following
                trace.append({'state':state.to_dict()})
        assert engine.rewind(state,3).same_as(seed)
        replay=Engine(Tensor.from_dict(trace[0]['tensor']))
        replayed=State.from_dict(trace[0]['state'])
        for row in trace[1:]:
            replayed=replay.step(replayed)
            assert replayed.same_as(State.from_dict(row['state']))
        (out/f'{label}_full_trace.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in trace))
        assert rows[0]['all_discrete_constraints_zero']
        assert not rows[1]['all_discrete_constraints_zero']
        cases.append({'case':label,'previous_slice':previous_report,'samples':rows,
                      'actual_engine_equals_direct_exact_rhs_updates':True,
                      'rewind_and_complete_trace_replay_exact':True})
    return {'invariant_summary':invariant_summary(program),'initial_slice':seed_report,'cases':cases}


def run(out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    report={'scope':'Actual Engine arithmetic equivalence and independent discrete sourced initial-data falsification; no general-GR claim',
            'vacuum':vacuum_equivalence(),'sourced':sourced_runs(out)}
    paths=[Path(__file__).relative_to(ROOT),Path('experiments/geometry/team48/integer_sign_lift.py'),
           Path('experiments/geometry/team48/matter_equations.py'),Path('universe24/core/engine.py')]
    report['source_sha256']={str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    (out/'sign_validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    result=run(ROOT/'runs/team48/numerical')
    print(json.dumps({'vacuum_cases':len(result['vacuum']),
          'sourced':result['sourced']['invariant_summary'],
          'initial_slice':result['sourced']['initial_slice'],
          'first_update':[{ 'case':c['case'], 'H':c['samples'][1]['peak_constraints']['H'],
                            'M0':c['samples'][1]['peak_constraints']['M0'],
                            'gradient_phi0':c['samples'][1]['peak_constraints']['gradient_phi0'],
                            'singular_nodes':c['samples'][1]['singular_nodes']} for c in result['sourced']['cases']]},indent=2))
