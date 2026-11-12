"""Source-only reciprocal apparatus proposal for the corrected massive full frame.

The two-field apparatus is a homogeneous normal-frame source. Spatially varying
tests are algebraic locality/response probes, not a covariant moving detector.
The current projective compiler and unchanged single Engine retain every input.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import importlib
import gzip
from pathlib import Path
import subprocess
import sys

import numpy as np
import sympy as sp

from universe24.core import Engine, State, exact_json
from universe24.core.lattice import lattice
from universe24.system.bundle import create_bundle, state_from_data, tensor_from_data
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run

REFERENCE_COMMIT = "62202fdccdd9a40d5dbbec104de6f97d9587a999"
APPARATUS_FIELDS = ("apparatus_q", "apparatus_p")


@dataclass(frozen=True)
class CoupledModel:
    program: object
    mass_squared: F
    omega_squared: F
    interaction: F
    charge_coupling: F
    reference: object
    source_hashes: dict

    def equations(self, fields, partial):
        return coupled_equations(self.reference.corrected_charged, fields, partial,
                                 mass_squared=self.mass_squared,
                                 omega_squared=self.omega_squared,
                                 interaction=self.interaction,
                                 charge_coupling=self.charge_coupling)


def coupled_equations(base_equations, fields, partial, *, mass_squared=1,
                      omega_squared=1, interaction=F(1, 4), charge_coupling=1):
    """Reciprocal onsite forces and homogeneous source from one potential.

    No q spatial-gradient fields are retained, hence the j=0 source is physically
    asserted only on the homogeneous sector. Generic local intervention remains
    a declared equation probe and must retain its momentum/constraint failures.
    """
    m2, omega2, g, charge = map(F,(mass_squared,omega_squared,interaction,charge_coupling))
    rhs,constraints,diagnostic=base_equations(fields,partial,
                                            mass_squared=m2,coupling=charge)
    rhs,constraints,diagnostic=dict(rhs),dict(constraints),dict(diagnostic)
    q,p=(fields[name] for name in APPARATUS_FIELDS)
    intensity=fields['phi']**2+fields['chi']**2
    potential=F(1,2)*omega2*q*q+g*q*intensity
    rho=F(1,2)*p*p+potential
    pressure=F(1,2)*p*p-potential
    trace=sum(fields[f'K{axis}{axis}'] for axis in range(3))
    rhs['apparatus_q']=p
    rhs['apparatus_p']=trace*p-omega2*q-g*intensity
    for field in ('phi','chi'):
        rhs['Pi_'+field]-=2*g*q*fields[field]
    for axis in range(3):
        rhs[f'K{axis}{axis}']-=potential
    constraints['H']-=2*rho
    diagnostic['rho']+=rho
    diagnostic['stress']=[[diagnostic['stress'][a][b]+int(a==b)*pressure
                           for b in range(3)] for a in range(3)]
    diagnostic.update(apparatus_rho=rho,apparatus_pressure=pressure,
                      apparatus_potential=potential,interaction_potential=g*q*intensity,
                      apparatus_momentum=[0,0,0],
                      apparatus_scope='homogeneous normal-frame only; spatial momentum completion absent')
    return rhs,constraints,diagnostic


def _load_reference(reference: str | Path | None):
    """Builder-only use in the isolated, pinned source subprocess."""
    if reference is not None:
        raise ValueError('reference builders run only inside the isolated exporter; use audit(reference=...)')
    module=importlib.import_module('validation.research_eight.07_hyperbolic_symbol')
    return module


def build_coupled(*, reference=None, dt=F(1,32), dx=1, mass_squared=1,
                  omega_squared=1, interaction=F(1,4), charge_coupling=1):
    for value in (dt,dx,mass_squared,omega_squared,interaction,charge_coupling):
        if isinstance(value,(float,bool,np.floating,np.bool_)):
            raise TypeError('exact rational physical parameters required')
    if F(mass_squared)<0 or F(omega_squared)<=0:
        raise ValueError('carrier mass squared must be nonnegative and oscillator positive')
    ref=_load_reference(reference)
    fields=tuple(ref.matter_dust_square.FIELDS_CHARGED)+APPARATUS_FIELDS
    assert len(fields)==46
    def rhs(values,partial):
        return coupled_equations(ref.corrected_charged,values,partial,
                                 mass_squared=mass_squared,omega_squared=omega_squared,
                                 interaction=interaction,charge_coupling=charge_coupling)
    program=ref.projective.compile_projective(fields,rhs,dt=dt,dx=dx,degree=3)
    assert program.tensor.G==47
    modules=(ref,ref.projective,ref.matter_dust_square,ref.matter_charged,
             importlib.import_module('validation.geometry.team48.matter_equations'),
             importlib.import_module('universe24.algebra.frame_equations'))
    reference_root=Path(ref.__file__).resolve().parents[2]
    hashes={str(Path(module.__file__).resolve().relative_to(reference_root)):hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
            for module in modules}
    return CoupledModel(program,F(mass_squared),F(omega_squared),F(interaction),
                        F(charge_coupling),ref,hashes)


def prepare_example(model: CoupledModel, *, L=3, history_sign=1, local_history=False,
                    phase_texture=False, denominator=64):
    """Exact zero-charge source, with a retained p-history intervention.

    Homogeneous default has phi=1/2, q=0, p=+/-1/4 and K=(-4,-4,-3)/16;
    with m=omega=1 it exactly satisfies H=M=Gauss=0 initially. Both signs
    have the same initial source stress. Local history flips only p at node0.
    Spatial phase texture is a separate unconstrained diagnostic preparation.
    """
    if history_sign not in (-1,1):
        raise ValueError('history sign must be -1 or +1')
    values=np.zeros((len(model.program.fields),lattice(L).N),dtype=object)
    by={name:i for i,name in enumerate(model.program.fields)}
    for axis in range(3):
        values[by[f'B{axis}{axis}']]=1
        values[by[f'K{axis}{axis}']]=F(-3 if axis==2 else -4,16)
    values[by['phi']]=F(1,2)
    values[by['apparatus_p']]=F(1,4)
    if local_history:
        values[by['apparatus_p'],0]=history_sign*F(1,4)
    else:
        values[by['apparatus_p']]=history_sign*F(1,4)
    if phase_texture:
        lat=lattice(L)
        for node in range(lat.N):
            x,y,z=lat.coords(node)
            values[by['phi'],node]=F((x-y)%3-1,4)
            values[by['chi'],node]=F((y-z)%3-1,4)
        for field in ('phi','chi'):
            for axis in range(3):
                plus=lat.shift_index(tuple(int(j==axis) for j in range(3)))
                minus=lat.shift_index(tuple(-int(j==axis) for j in range(3)))
                values[by[f'Xi_{field}{axis}']]=(values[by[field],plus]-values[by[field],minus])/(2*model.program.dx)
    carries=np.asarray([[(g+node)%6 for node in range(L**3)] for g in range(47)],dtype=object)
    return model.reference.projective.prepare(model.program,values,L=L,
                                             denominator=denominator,remainders=carries)


def bundle_for(model: CoupledModel, seed: State):
    tensor=model.program.tensor
    channels=[]
    for i,gear in enumerate(tensor.gears):
        owner=('projective_encoding' if i==0 else 'homogeneous_apparatus'
               if gear.name.removeprefix('projective.') in APPARATUS_FIELDS else 'corrected_frame_matter')
        channels.append(dict(index=i,name=gear.name,label=gear.label,owner=owner,
                             purpose='Declared reciprocal homogeneous source proposal; not accepted generic physics'))
    return create_bundle(tensor,seed,channels=channels,protocol=default_protocol(),
                         model=dict(id='selection-reciprocal47',version='1',
                                    domain='Homogeneous normal apparatus source; generic inhomogeneous source/Einstein gates open',
                                    source_commit=REFERENCE_COMMIT,
                                    mass_squared=str(model.mass_squared),omega_squared=str(model.omega_squared),
                                    interaction=str(model.interaction),charge_coupling=str(model.charge_coupling),
                                    physical_dt=str(model.program.dt),physical_dx=str(model.program.dx),
                                    readout='current numerator/current denominator; D_old=0 is retained boundary memory'))


def _fields_at(model,state,node=0):
    data=model.reference.projective.readout(model.program,state)
    return {name:data[i,node] for i,name in enumerate(model.program.fields)}


def source_diagnostic(model,state,node=0):
    values=model.reference.projective.readout(model.program,state)
    names={name:i for i,name in enumerate(model.program.fields)}
    lat=state.lattice
    fields={name:values[i,node] for name,i in names.items()}
    def partial(name,axis):
        return (values[names[name],lat.neighbour(node,2*axis)]-
                values[names[name],lat.neighbour(node,2*axis+1)])/(2*model.program.dx)
    _,constraints,diagnostics=model.equations(fields,partial)
    determinant=sp.det(sp.Matrix([[fields[f'B{a}{i}'] for i in range(3)] for a in range(3)]))
    return {'constraints':{k:str(constraints[k]) for k in ('H','M0','M1','M2','Gauss_E','Gauss_M')},
            'rho':str(diagnostics['rho']),'apparatus_rho':str(diagnostics['apparatus_rho']),
            'determinant_frame':str(determinant),
            'finite_potential_domain':bool(model.mass_squared/2+model.interaction*fields['apparatus_q']>=0)}


def identities():
    q,p,phi,chi,pi_phi,pi_chi,g,omega2,m2,trace=sp.symbols('q p phi chi pi_phi pi_chi g omega2 m2 K')
    intensity=phi**2+chi**2
    potential=omega2*q*q/2+g*q*intensity
    rho_app=p*p/2+potential
    rate={q:p,p:trace*p-omega2*q-g*intensity,phi:pi_phi,chi:pi_chi}
    app_rate=sp.expand(sum(sp.diff(rho_app,var)*speed for var,speed in rate.items()))
    exchange=2*g*q*(phi*pi_phi+chi*pi_chi)
    assert sp.expand(app_rate-trace*p*p-exchange)==0
    assert sp.expand(phi*(-2*g*q*chi)-chi*(-2*g*q*phi))==0
    # This globally unbounded valley is retained as a counterexample.
    eliminated=sp.expand(potential.subs(q,-g*intensity/omega2))
    assert sp.expand(eliminated+g*g*intensity**2/(2*omega2))==0
    # Without spatial q gradients, momentum conservation cannot generally hold.
    # At q=0, p nonuniform, all carrier fields zero: j_app=0 but grad P=p grad p.
    return {'homogeneous_exchange_identity':True,'neutral_interaction_charge_torque':0,
            'eliminated_potential':str(eliminated),
            'unbounded_potential_counterexample':{'phi':8,'chi':0,'q':-16,'omega_squared':1,'interaction':'1/4','total_potential_at_m_squared_1':-96},
            'inhomogeneous_momentum_counterexample':'q=0, carrier=0, p=1, partial_x(p)=1 gives partial_x pressure=1 while j_app=0 and no apparatus momentum equation',
            'globally_bounded':False,'generic_covariant_apparatus':False}


def _reference_export(*,out,steps=4):
    out=Path(out)
    if out.exists() and any(out.iterdir()):
        raise FileExistsError('fresh audit directory required')
    out.mkdir(parents=True,exist_ok=True)
    if type(steps) is not int or not 3<=steps<=5:
        raise ValueError('finite preregistered horizon is three through five updates')
    models={label:build_coupled(interaction=g)
            for label,g in (('connected',F(1,4)),('disconnected',F(0)))}
    cases=[]
    exports=[]
    for texture in (False,True):
        for label,model in models.items():
            states=[prepare_example(model,history_sign=sign,local_history=texture,
                                    phase_texture=texture) for sign in (1,-1)]
            seeds=[state.copy() for state in states]
            complete_histories=[[state.to_dict()] for state in states]
            if not texture:
                for state in states:
                    initial=source_diagnostic(model,state)
                    assert all(F(value)==0 for value in initial['constraints'].values())
            source_indices=[i for i,name in enumerate(model.program.tensor.names)
                            if not name.startswith('projective.apparatus_')]
            carrier_indices=[model.program.tensor.gear_index('projective.'+name)
                             for name in ('phi','chi','Pi_phi','Pi_chi')]
            engine=Engine(model.program.tensor)
            differences=[]
            diagnostics=[]
            for tick in range(1,steps+1):
                following=[]
                for state in states:
                    actual=engine.step(state)
                    expected=model.reference.scalar_oracle(model.program.tensor,state)
                    assert actual.same_as(expected)
                    assert engine.inverse_step(actual).same_as(state)
                    assert np.array_equal(actual.r,state.r)
                    following.append(actual)
                states=following
                for history,state in zip(complete_histories,states):
                    history.append(state.to_dict())
                source_different=any(not np.array_equal(getattr(states[0],key)[source_indices],getattr(states[1],key)[source_indices])
                                     for key in ('a','b','r'))
                carrier_different=any(not np.array_equal(getattr(states[0],key)[carrier_indices],getattr(states[1],key)[carrier_indices])
                                      for key in ('a','b','r'))
                phase_current_different=any(not np.array_equal(states[0].b[model.program.tensor.gear_index('projective.'+name)],
                                                               states[1].b[model.program.tensor.gear_index('projective.'+name)])
                                            for name in ('phi','chi'))
                differences.append(dict(tick=tick,source_changed=source_different,
                                        carrier_changed=carrier_different,carrier_position_changed=phase_current_different))
                diagnostics.append([source_diagnostic(model,state) for state in states])
            assert any(row['carrier_position_changed'] for row in differences) if label=='connected' else not any(row['source_changed'] for row in differences)
            for sign,seed,final,history in zip((1,-1),seeds,states,complete_histories):
                assert engine.rewind(final,steps).same_as(seed)
                bundle=bundle_for(model,seed)
                exports.append(dict(name=f'{label}-{"texture" if texture else "homogeneous"}-{sign:+d}',
                                    tensor=bundle.tensor.to_dict(),seed=bundle.seed.to_dict(),
                                    channels=list(bundle.channels),protocol=bundle.protocol,model=bundle.model,
                                    states=history,steps=steps))
            cases.append(dict(connection=label,phase_texture=texture,comparisons=differences,
                              source_diagnostics=diagnostics,
                              tensor_hash=model.program.tensor.fingerprint,channels=47,
                              monomials=len(model.program.tensor),degree=model.program.degree,
                              maximum_bits=max(abs(int(v)).bit_length() for state in states for array in (state.a,state.b,state.r) for v in array.flat)))
    # Literal zero-source invariant and massless controls are distinct prepared
    # inputs. They are not used to claim a resolved material-clock period.
    controls=[]
    for name,model in (('zero-source',models['connected']),
                       ('massless-control',build_coupled(mass_squared=0))):
        values=np.zeros((len(model.program.fields),27),dtype=object)
        for axis in range(3):
            values[model.program.fields.index(f'B{axis}{axis}')]=1
        if name=='massless-control':
            values[model.program.fields.index('phi')]=F(1,2)
        seed=model.reference.projective.prepare(model.program,values,L=3,denominator=64,
                    remainders=np.asarray([[(g+n)%6 for n in range(27)] for g in range(47)],dtype=object))
        state=seed;history=[seed.to_dict()];engine=Engine(model.program.tensor)
        for _ in range(steps):
            following=engine.step(state)
            assert following.same_as(model.reference.scalar_oracle(model.program.tensor,state))
            state=following;history.append(state.to_dict())
        assert engine.rewind(state,steps).same_as(seed)
        if name=='zero-source':
            decoded=model.reference.projective.readout(model.program,state)
            assert np.array_equal(decoded,values)
        bundle=bundle_for(model,seed)
        exports.append(dict(name=name,tensor=bundle.tensor.to_dict(),seed=bundle.seed.to_dict(),
                            channels=list(bundle.channels),protocol=bundle.protocol,model=bundle.model,
                            states=history,steps=steps))
        controls.append(dict(name=name,mass_squared=str(model.mass_squared),
                             tensor_hash=model.program.tensor.fingerprint,
                             final=source_diagnostic(model,state)))
    report=dict(schema='universe24/selection/reciprocal47/1',reference_commit=REFERENCE_COMMIT,
                algebra=identities(),cases=cases,controls=controls,all_carries_oracle_rewind=True,
                current_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                reference_sha256=models['connected'].source_hashes,
                degree_support='cubic, strict face-local, no old-a tensor reads',
                physical_status='homogeneous reciprocal exchange only; full Einstein/inhomogeneous apparatus/selection/Born/Bell not established')
    (out/'coupled.json').write_text(exact_json.dumps(report,sort_keys=True)+'\n')
    (out/'raw-reference.json.gz').write_bytes(gzip.compress(exact_json.dumps(exports,sort_keys=True).encode(),mtime=0))
    return report


def audit(*,reference,out='runs/selection/coupled',steps=4):
    """Export pinned equations in isolation, then execute only main's runtime."""
    reference,out=Path(reference).resolve(),Path(out).resolve()
    actual=subprocess.run(['git','-C',str(reference),'rev-parse','HEAD'],check=True,
                          text=True,capture_output=True).stdout.strip()
    if actual!=REFERENCE_COMMIT:
        raise ValueError('reference checkout must have the exact declared PR50 commit')
    changed=subprocess.run(['git','-C',str(reference),'status','--porcelain','--untracked-files=no'],
                           check=True,text=True,capture_output=True).stdout
    if changed:
        raise ValueError('reference checkout has tracked modifications')
    # Sparse checkout flags may hide changes from status. Validate the bytes of
    # every materialized Python source against the actual pinned Git tree too.
    listing=subprocess.run(['git','-C',str(reference),'ls-tree','-r','HEAD'],
                           check=True,text=True,capture_output=True).stdout
    verified_source_blobs={}
    for row in listing.splitlines():
        metadata,name=row.split('\t',1)
        _,kind,expected=metadata.split()
        path=reference/name
        if kind!='blob' or not name.endswith('.py') or not path.is_file():
            continue
        data=path.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if digest!=expected:
            raise ValueError('reference source bytes differ from pinned tree: '+name)
        verified_source_blobs[name]=digest
    if out.exists() and any(out.iterdir()):
        raise FileExistsError('fresh audit output required')
    out.mkdir(parents=True,exist_ok=True)
    source=Path(__file__).resolve()
    script='''import importlib.util,pathlib,sys
root,script,out,steps=sys.argv[1:]
sys.path.insert(0,root)
spec=importlib.util.spec_from_file_location("selection_coupled_export",script)
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
spec.loader.exec_module(module)
module._reference_export(out=out,steps=int(steps))
'''
    raw=out/'reference'
    result=subprocess.run([sys.executable,'-I','-c',script,str(reference),str(source),str(raw),str(steps)],
                          cwd=reference,capture_output=True,text=True)
    if result.returncode:
        raise RuntimeError('isolated reference export failed:\n'+result.stderr)
    exports=exact_json.loads(gzip.decompress((raw/'raw-reference.json.gz').read_bytes()))
    report=exact_json.loads((raw/'coupled.json').read_text())
    checked=0
    for case in exports:
        tensor=tensor_from_data(case['tensor']);seed=state_from_data(case['seed'])
        bundle=create_bundle(tensor,seed,channels=case['channels'],protocol=case['protocol'],model=case['model'])
        target=out/case['name']
        runtime=run_bundle(bundle,target,steps=case['steps'])
        verify_run(target)
        with gzip.open(target/'full_trace.jsonl.gz','rt') as stream:
            for index,line in enumerate(stream,1):
                record=exact_json.loads(line)
                assert record['before']==case['states'][index-1]
                assert record['after']==case['states'][index]
                checked+=1
        if case['name']=='connected-homogeneous-+1':
            report['primary_bundle_path']=str(target/'bundle')
            report['primary_bundle_id']=bundle.bundle_id
    report['current_main_full_state_comparisons']=checked
    report['current_main_runtime_and_replay']=True
    report['verified_reference_python_blobs']=verified_source_blobs
    report['raw_reference_sha256']=hashlib.sha256((raw/'raw-reference.json.gz').read_bytes()).hexdigest()
    (out/'coupled.json').write_text(exact_json.dumps(report,sort_keys=True)+'\n')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference',required=True,type=Path)
    parser.add_argument('--out',type=Path,default=Path('runs/selection/coupled'))
    parser.add_argument('--steps',type=int,default=4)
    args=parser.parse_args()
    result=audit(reference=args.reference,out=args.out,steps=args.steps)
    print(exact_json.dumps({'channels':47,'case_count':len(result['cases']),
                           'all_carries_oracle_rewind':True}))


if __name__=='__main__':
    main()
