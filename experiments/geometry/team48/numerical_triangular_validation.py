"""Independent constrained-data evolution gates for triangular32 and Maxwell38.

These integer trajectories use spatially nonuniform sourced initial slices
with independently derived nonzero energy and momentum. Repeating that slice
as both levels is deliberately labelled; it is not an exact temporal history.
The diagonal plane-symmetric sector additionally permits exact agreement with
unreduced Fermi36/42 trajectories, without a rotating-frame interpolation.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from experiments.geometry.team48 import geometry_triangular as triangular
from experiments.geometry.team48.integer_sign_lift import compile_quadratic,prepare,physical_slices,invariant_summary
from experiments.geometry.team48.matter_equations import FIELDS,FIELDS_WITH_MAXWELL,equations as matter_equations
from experiments.geometry.team48.numerical_sign_validation import momentum_seed,sampled,as_array
from universe24.algebra.frame_equations import FIELDS as GEOMETRY_FIELDS
from universe24.core import Engine,State,Tensor
from universe24.core.lattice import lattice
from universe24.observe.frame48 import diagnostics


def builders(maxwell):
    def fermi(fields,partial):
        return matter_equations(fields,partial,mass_squared=0,maxwell=maxwell)
    def reduced(fields,partial):
        return triangular.equations(fields,partial,fermi_equations=matter_equations,
                                    mass_squared=0,maxwell=maxwell)
    return fermi,reduced


def complete_seed(maxwell=False):
    values,report=momentum_seed()
    names=FIELDS_WITH_MAXWELL if maxwell else FIELDS
    if maxwell:
        values=np.concatenate([values,np.zeros((6,125),dtype=object)])
        fields=dict(zip(names,values)); psi=fields['Psi_phi0']; k=fields['K11']
        fields['Pi_phi'][:]=4; fields['chi'][:]=1
        fields['E1'][:]=2; fields['M2'][:]=psi
        fields['rho_dust'][:]=k*k-10-psi*psi
        _,constraints,source=sampled(names,builders(True)[0],values,5)
        assert np.array_equal(source['rho'],k*k)
        assert np.array_equal(source['momentum'][0],-2*psi)
        assert not any(source['momentum'][1]) and not any(source['momentum'][2])
        expected_diagonal=[10+psi*psi,np.full(125,6,dtype=object),10-psi*psi]
        assert all(np.array_equal(source['stress'][a][a],expected_diagonal[a]) for a in range(3))
        assert all(not any(source['stress'][a][b]) for a in range(3) for b in range(3) if a!=b)
        assert all(v==-4 for v in source['charge'])
        assert all(v>=0 for v in fields['rho_dust'])
        assert all(not any(np.broadcast_to(v,(125,))) for v in constraints.values())
        report={**report,'Pi_phi':4,'chi':1,'global_U1_charge_density':-4,
                'E1':2,'M2':'Psi_phi0','rho_dust_min':str(min(fields['rho_dust'])),
                'all_sectors_active':True,'Gauss_E_and_M_zero':True,
                'independent_stress_diagonal':['10+Psi_x^2','6','10-Psi_x^2']}
    return names,values,report


def expand_values(names,values,full_names):
    fields=dict(zip(names,values))
    expanded,_=triangular.expand(fields,lambda name,axis:0)
    return np.asarray([np.broadcast_to(expanded[name],(values.shape[1],)) for name in full_names],dtype=object)


def summary(names,builder,values,full_names,L=5):
    _,constraints,source=sampled(names,builder,values,L)
    peak={name:str(max(abs(v) for v in np.broadcast_to(value,(L**3,)))) for name,value in constraints.items()}
    full=expand_values(names,values,full_names)
    metric=diagnostics(full[:24],L=L)
    return {'peak_constraints':peak,'all_discrete_constraints_zero':all(F(v)==0 for v in peak.values()),
            'singular_nodes':metric['singular_nodes'],'minimum_abs_det_B':metric['minimum_abs_det_B'],
            'minimum_rho':str(min(source['rho'])),
            'peak_abs_jx':str(max(abs(v) for v in source['momentum'][0])),
            'max_field_absolute_value':str(max(abs(v) for v in values.flat))}


def run(out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    reports=[]
    for maxwell in (False,True):
        full_names,full_values,seed_report=complete_seed(maxwell)
        names=tuple(n for n in full_names if n not in triangular.ZERO_FIELDS and n not in triangular.ALIASES)
        values=full_values[[full_names.index(n) for n in names]]
        fermi,reduced=builders(maxwell)
        program=compile_quadratic(names,reduced)
        full_program=compile_quadratic(full_names,fermi)
        assert program.tensor.G==(38 if maxwell else 32)
        seed=prepare(program,values,values,L=5,remainders=np.arange(program.tensor.G*125).reshape(program.tensor.G,125)%6)
        full_seed=prepare(full_program,full_values,full_values,L=5,remainders=np.arange(full_program.tensor.G*125).reshape(full_program.tensor.G,125)%6)
        engine,full_engine=Engine(program.tensor),Engine(full_program.tensor)
        state,full_state=seed,full_seed
        prev,now=values.copy(),values.copy()
        trace=[{'tensor':program.tensor.to_dict(),'state':seed.to_dict()}]
        rows=[]
        for step in range(4):
            old,current=physical_slices(program,state)
            old_full,current_full=physical_slices(full_program,full_state)
            assert np.array_equal(old,prev) and np.array_equal(current,now)
            assert np.array_equal(expand_values(names,old,full_names),old_full)
            assert np.array_equal(expand_values(names,current,full_names),current_full)
            assert np.array_equal(state.r,seed.r)
            rows.append({'update':step,**summary(names,reduced,current,full_names)})
            if step<3:
                rhs,_,_=sampled(names,reduced,now,5)
                prev,now=now,prev+2*as_array(rhs,names,125)
                state,full_state=engine.step(state),full_engine.step(full_state)
                trace.append({'state':state.to_dict()})
        assert engine.rewind(state,3).same_as(seed)
        assert full_engine.rewind(full_state,3).same_as(full_seed)
        replay=Engine(Tensor.from_dict(trace[0]['tensor']))
        replayed=State.from_dict(trace[0]['state'])
        for row in trace[1:]:
            replayed=replay.step(replayed)
            assert replayed.same_as(State.from_dict(row['state']))
        assert rows[0]['all_discrete_constraints_zero']
        assert not rows[1]['all_discrete_constraints_zero']
        label='triangular38_maxwell' if maxwell else 'triangular32_scalar_dust'
        (out/f'{label}_full_trace.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in trace))
        reports.append({'case':label,'invariant_summary':invariant_summary(program),
                        'seed':seed_report,'initial_pair':'Two identical individually constrained slices; no exact temporal-history claim',
                        'samples':rows,'exact_agreement_with_unreduced_channels':full_program.tensor.G,
                        'exact_agreement_scope':'This diagonal plane-symmetric sourced sector has Omega=0; not arbitrary rotating-frame equivalence',
                        'actual_integer_engine_agrees_with_direct_exact_rhs':True,
                        'complete_rewind_and_trace_replay_exact':True})
    paths=[Path(__file__).relative_to(ROOT),Path('experiments/geometry/team48/numerical_sign_validation.py'),
           Path('experiments/geometry/team48/geometry_triangular.py'),Path('experiments/geometry/team48/matter_equations.py'),
           Path('experiments/geometry/team48/integer_sign_lift.py')]
    report={'scope':'Independent sourced constraints and actual Engine negative gates for32/38 integer-channel encodings',
            'cases':reports,'source_sha256':{str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}}
    (out/'triangular_validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    result=run(ROOT/'runs/team48/numerical')
    print(json.dumps([{'case':r['case'],'channels':r['invariant_summary']['channels'],
                       'initial_H':r['samples'][0]['peak_constraints']['H'],
                       'initial_M0':r['samples'][0]['peak_constraints']['M0'],
                       'initial_peak_jx':r['samples'][0]['peak_abs_jx'],
                       'first_H':r['samples'][1]['peak_constraints']['H'],
                       'first_M0':r['samples'][1]['peak_constraints']['M0'],
                       'singular_nodes':[s['singular_nodes'] for s in r['samples']]} for r in result['cases']],indent=2))
