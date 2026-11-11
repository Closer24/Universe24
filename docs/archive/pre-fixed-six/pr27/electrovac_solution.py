"""Optional sourced pp-wave experiment using only the unchanged integer Engine.

python experiments/geometry/electrovac_solution.py --out runs/geometry/electrovac
The smooth metric/Maxwell decoder and reference solver are passive analysis.
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import argparse
from fractions import Fraction
import hashlib
import json
import math
import platform
import numpy as np
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import ZERO, lattice
from universe24.core.reciprocity import check_reciprocity
from experiments.geometry.retimed_tensor_wave import build as build_carrier
from experiments.geometry.electrovac_geometry import audit

REFINEMENTS = (1,2,4,8)
PROBES = ('neutral1.x','neutral1.y','neutral2.x','neutral2.y','charged.x','charged.y')
CHARGES = (0,0,1)
ONE_WAY = 'Aligned Einstein-Maxwell plane-wave background; test particles carry negligible stress and current. Their backreaction is omitted.'


def build(n, reciprocal_control=False):
    if type(n) is not int or n not in REFINEMENTS:
        raise ValueError(f'n must be one of {REFINEMENTS}')
    P = 128*n*n; Q = 2*P*P*n*n; D = 6*Q; scale = (1<<13)*n**4
    base = build_carrier(Q,2)
    terms = [(base.names[m.target],m.coeff,tuple((base.names[f.gear],f.offset,f.field)
              for f in m.factors)) for m in base.monomials]
    factor = lambda name:(name,ZERO,'b')
    meta = {} if reciprocal_control else {'designated_one_way':ONE_WAY}
    for arm,charge in enumerate(CHARGES):
        for component in range(2):
            probe = PROBES[2*arm+component]
            terms.append((probe,D,(factor(probe),)))
            for source in ('p.X','q.X'):
                terms.append((probe,-3,(factor(source),factor(source),factor(probe)),meta))
                if reciprocal_control:
                    terms.append((source,-3,(factor(source),factor(probe),factor(probe))))
            if charge:
                source = ('p.X','q.X')[component]
                coeff = -6*P*scale*charge
                terms.append((probe,coeff,(factor(source),),meta))
                if reciprocal_control:
                    terms.append((source,coeff,(factor(probe),)))
    tensor = Tensor(list(base.names)+list(PROBES),terms,Q=Q,strict_support=True)
    assert tensor.rank==4 and check_reciprocity(tensor).ok
    return tensor,dict(n=n,L=3*n,P=P,Q=Q,D=D,scale=scale,steps=6*n,dt=f'1/{n}')


def profiles(p,kind):
    if kind not in ('flat','constant','linear','circular'):
        raise ValueError('unknown field preparation')
    phase = 2*np.pi*np.arange(2*p['L'])/(2*p['L'])
    values = np.stack([np.cos(phase),np.sin(phase)])*p['P']/8
    result = np.rint(values).astype(np.int64)
    if kind in ('flat','linear','constant'):result[1]=0
    if kind=='flat':result[0]=0
    if kind=='constant':result[0]=p['P']//8
    return result


def expected(p,profile,tick):
    z = lattice(p['L']).all_coords()[:,2]
    return np.array([profile[j,(2*z+bank+tick)%(2*p['L'])]
                     for j in range(2) for bank in (0,1)],dtype=np.int64)


def prepare(p,profile):
    b = np.zeros((10,p['L']**3),dtype=np.int64); a=b.copy()
    b[:4]=expected(p,profile,0); a[:4]=expected(p,profile,-1)
    r=(17*np.arange(b.size,dtype=np.int64).reshape(b.shape)+5)%p['D']
    b[4]=p['scale']; b[7]=p['scale']; b[8]=p['scale']
    for arm,charge in enumerate(CHARGES):
        for component in range(2):
            gear=4+2*arm+component
            for node in range(p['L']**3):
                value=int(b[gear,node]); e=int(b[0,node]); f=int(b[2,node])
                force=-(e*e+f*f)*value-2*charge*p['P']*p['scale']*(e,f)[component]
                a[gear,node]=value-value//(16*p['n'])+round(Fraction(force,4*p['P']**2*p['n']**2))
    return State(p['L'],a,b,r)


def reference(p,profile,substeps=64):
    coeff=np.fft.fft(profile/p['P'],axis=1)/profile.shape[1]
    frequencies=2*np.pi*np.fft.fftfreq(profile.shape[1],d=1/p['n'])
    charge=np.array(CHARGES)
    def rhs(t,vec):
        e,f=np.real(coeff@np.exp(1j*frequencies*t)); C=-(e*e+f*f)/2
        x,y,vx,vy,_=vec.T; H=C*(x*x+y*y)
        return np.stack([vx,vy,C*x-charge*e,C*y-charge*f,(1+vx*vx+vy*vy+H)/2],axis=1)
    vec=np.array([[1,0,1/16,0,0],[0,1,0,1/16,0],[1,0,1/16,0,0]],dtype=float)
    samples=[vec.copy()]; h=1/(p['n']*substeps); t=0.
    for _ in range(p['steps']):
        for __ in range(substeps):
            k1=rhs(t,vec); k2=rhs(t+h/2,vec+h*k1/2)
            k3=rhs(t+h/2,vec+h*k2/2); k4=rhs(t+h,vec+h*k3)
            vec=vec+h*(k1+2*k2+2*k3+k4)/6; t+=h
        samples.append(vec.copy())
    return np.array(samples)


def energy_banks(state):
    # Python integers make this diagnostic safe even in a deliberately bad control.
    b=state.b[:4].astype(object)
    return b[0]**2+b[2]**2,b[1]**2+b[3]**2


def continuity_residual(before,after):
    rx,ry=energy_banks(before); nx,ny=energy_banks(after)
    shift=before.lattice.shift_index((0,0,1))
    return nx+ny-rx-ry-(rx[shift]-rx)


def run_case(n,kind,out=None,polarity=1,amplitude=1):
    if polarity not in (-1,1) or type(amplitude) is not int or amplitude<1:
        raise ValueError('polarity must be +/-1 and amplitude a positive integer')
    tensor,p=build(n); profile=profiles(p,kind)*polarity*amplitude
    seed=prepare(p,profile); engine=Engine(tensor,p['Q']); state=seed
    history=[np.stack([seed.a,seed.b,seed.r])]
    positions=[seed.b[4:,0].astype(float)/p['scale']]; events=[]
    da=seed.a[4:,0].copy(); db=seed.b[4:,0].copy()
    energy0=sum(sum(row) for row in energy_banks(seed))
    max_ledger=max_continuity=0; peak_density=0
    for tick in range(1,p['steps']+1):
        after=engine.step(state)
        assert np.array_equal(after.b[:4],expected(p,profile,tick))
        assert np.array_equal(after.a[:4],expected(p,profile,tick-1))
        assert np.array_equal(after.r[:4],seed.r[:4])
        residual=continuity_residual(state,after)
        max_continuity=max(max_continuity,max(abs(int(v)) for v in residual))
        assert max_continuity==0 and sum(sum(row) for row in energy_banks(after))==energy0
        old=state.b.astype(object); new=after.b.astype(object)
        density=old[0]**2+old[2]**2
        peak_density=max(peak_density,max(int(v) for v in density))
        for arm,charge in enumerate(CHARGES):
            for component in range(2):
                gear=4+2*arm+component
                forcing=-6*density*old[gear]-12*charge*p['P']*p['scale']*old[2*component]
                ledger=p['D']*(new[gear]-2*old[gear]+state.a[gear].astype(object))-forcing-state.r[gear].astype(object)+after.r[gear].astype(object)
                max_ledger=max(max_ledger,max(abs(int(v)) for v in ledger))
        assert max_ledger==0
        log=engine.clicks(state,after,tick).select('official')
        rows={int(g):int(q) for g,node,q in zip(log.gear,log.node,log.quotient) if int(node)==0 and int(g)>=4}
        ell=np.array([rows.get(g,0) for g in range(4,10)],dtype=np.int64)
        assert np.array_equal(ell,after.b[4:,0]+state.a[4:,0])
        da,db=db,ell-da
        assert np.array_equal(db,after.b[4:,0])
        positions.append(db.astype(float)/p['scale']);events.append(ell)
        snapshot=np.stack([after.a,after.b,after.r])
        assert max(abs(int(snapshot.min())),abs(int(snapshot.max())))<2**63
        history.append(snapshot.astype(np.int64)); state=after
    assert engine.rewind(state,p['steps']).same_as(seed)
    ref=reference(p,profile,64); fine=reference(p,profile,128)
    reference_error=float(np.max(abs(ref-fine))); assert reference_error<1e-8
    pos=np.array(positions); refpos=fine[:,:,:2].reshape(-1,6)
    errors=np.max(abs(pos-refpos),axis=0)
    if kind=='flat':assert max(errors)<1e-12
    assert np.max(abs(pos))<3
    complete=np.stack(history); file_hash=None
    label=f'{kind}_n{n}_sign{polarity}_amp{amplitude}'
    if out is not None:
        out=Path(out);out.mkdir(parents=True,exist_ok=True); path=out/f'{label}.npz'
        np.savez_compressed(path,states=complete,profile=profile,positions=pos,
                            reference_geodesics=fine,official_quotients=np.array(events))
        file_hash=hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(kind=kind,polarity=polarity,amplitude=amplitude,parameters=p,
        gears=tensor.G,monomials=len(tensor.monomials),rank=tensor.rank,
        tensor_fingerprint=tensor.fingerprint,strict_support=True,
        designated_test_body_terms=len(tensor.designations),reciprocity_with_designations=True,
        all_carrier_translations_exact=True,all_rewinds_exact=True,
        max_integer_force_ledger_residual=max_ledger,max_integer_energy_continuity_residual=max_continuity,
        initial_total_carrier_energy_integer=str(energy0),peak_Tuu=peak_density/p['P']**2,
        official_only_decoder_exact=True,neutral_max_error=float(max(errors[:4])),
        charged_max_error=float(max(errors[4:])),reference_halving_error=reference_error,
        final_positions=pos[-1].tolist(),reference_final_positions=refpos[-1].tolist(),
        peak_abs_position=float(np.max(abs(pos))),profile=profile.tolist(),
        full_trace_shape=list(complete.shape),trace_file_sha256=file_hash,
        full_trace_values_sha256=hashlib.sha256(complete.tobytes()).hexdigest(),
        engine_arithmetic_counts=engine.stats)


def reciprocal_control():
    tensor,p=build(1,True); seed=prepare(p,profiles(p,'circular'))
    seed.a[4:]=0;seed.b[4:]=0;seed.a[4]=1;seed.b[4]=1
    engine=Engine(tensor,p['Q']);after=engine.step(seed)
    mismatch=int(np.count_nonzero(after.b[:4]!=expected(p,profiles(p,'circular'),1)))
    residual=max(abs(int(v)) for v in continuity_residual(seed,after))
    assert mismatch>0 and residual>0 and engine.inverse_step(after).same_as(seed)
    assert check_reciprocity(tensor).ok and len(tensor.designations)==0
    return dict(fully_reciprocal=True,designated_terms=0,exact_rewind=True,
        carrier_mismatch_components=mismatch,continuity_residual=residual,
        conclusion='The direct reciprocal completion breaks this prepared transport and continuity sector. It is not a proof that every reciprocal Einstein encoding is impossible.')


def run(out,refinements=REFINEMENTS):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);cases=[]
    for n in refinements:
        for kind in ('flat','linear','circular'):
            row=run_case(n,kind,out);cases.append(row)
            print(json.dumps({k:row[k] for k in ('kind','neutral_max_error','charged_max_error')}|{'n':n}),flush=True)
    controls=[run_case(2,'circular',out,polarity=-1),run_case(2,'circular',out,amplitude=2)]
    standard=next((c for c in cases if c['kind']=='circular' and c['parameters']['n']==2),None)
    if standard is None:standard=run_case(2,'circular')
    assert controls[0]['final_positions'][:4]==standard['final_positions'][:4]
    assert controls[1]['peak_Tuu']==4*standard['peak_Tuu']
    # Compare every retained neutral detector state, not merely its final point.
    standard_path=out/'circular_n2_sign1_amp1.npz'
    if not standard_path.exists():
        standard=run_case(2,'circular',out)
    with np.load(standard_path,allow_pickle=False) as plus, np.load(out/'circular_n2_sign-1_amp1.npz',allow_pickle=False) as minus:
        assert np.array_equal(plus['states'][:,:,4:8],minus['states'][:,:,4:8])
    orders={}
    for kind in ('linear','circular'):
        rows=[c for c in cases if c['kind']==kind]
        for probe in ('neutral','charged'):
            error=[r[f'{probe}_max_error'] for r in rows]
            orders[f'{kind}_{probe}']=[math.log(error[i]/error[i+1])/math.log(refinements[i+1]/refinements[i]) for i in range(len(error)-1)]
    report=dict(schema='electrovac-v1',scope='Exact continuum Einstein-Maxwell plane-wave decoder and autonomous neutral/charged test particles; not general reciprocal matter-gravity evolution.',
        geometry=audit(),cases=cases,source_controls=controls,reciprocal_control=reciprocal_control(),orders=orders,
        polarity_reversal_preserves_neutral_trajectory_exactly=True,
        doubled_field_amplitude_quadruples_Tuu_exactly=True,
        acceptance=dict(finest_errors_below_0_005=all(max(c['neutral_max_error'],c['charged_max_error'])<.005 for c in cases if c['parameters']['n']==refinements[-1]),
                        last_orders_above_1_5=all(v[-1]>1.5 for v in orders.values()) if len(refinements)>1 else None),
        limitations=['The source is an aligned source-free Maxwell radiation field, not massive matter or a finite beam.',
            'The declared metric decoder satisfies coupled continuum equations. It is not a separately evolved metric or a reconstruction from clocks.',
            'Test particles carry negligible stress/current. General reciprocal backreaction is not implemented.',
            'The longitudinal coordinate v is reconstructed by the reference, not a runtime gear.',
            'The transverse chart is local, not periodically glued. Carrier energy is a discrete transport invariant, not global GR energy.',
            'Each refinement decodes its own rounded field profile. Measured convergence is finite and does not prove stability for arbitrary data.'],
        provenance=dict(base_commit='7441d401dd79b0505d4741cb1ae46155a8ab8ab5',python=platform.python_version(),numpy=np.__version__,
            files={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),Path(__file__).with_name('electrovac_geometry.py'),ROOT/'universe24/core/engine.py',Path(__file__).with_name('retimed_tensor_wave.py')]}))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'runs/geometry/electrovac')
    parser.add_argument('--refinements',type=int,nargs='+',choices=REFINEMENTS,default=list(REFINEMENTS))
    args=parser.parse_args()
    if args.refinements!=sorted(set(args.refinements)):parser.error('refinements must be increasing')
    result=run(args.out,tuple(args.refinements))
    print(json.dumps(dict(output=str(args.out),orders=result['orders'],acceptance=result['acceptance'])),flush=True)
