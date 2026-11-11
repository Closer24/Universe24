"""Optional exact pp-wave decoding with autonomous integer tidal probes.

python experiments/geometry/pp_wave_solution.py --out runs/geometry/pp_wave

This is a chosen vacuum/test-body sector, NOT default ONE or sourced Einstein
gravity. Source transport is the existing prepared two-bank Rule3 construction.
Only Engine.step updates states. Geometry, RK4 references and diagnostics are passive.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import argparse
from fractions import Fraction
import hashlib
import json
import math
import platform
import numpy as np
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice, ZERO
from universe24.core.reciprocity import check_reciprocity
from experiments.geometry.retimed_tensor_wave import build as build_carrier
from experiments.geometry.pp_wave_geometry import audit, boundary_audit

REFINEMENTS=(1,2,4,8)
SCALE_BASE=1<<20
PERIOD=6
PROBES=('arm1.x','arm1.y','arm2.x','arm2.y')
ONE_WAY='Vacuum pp-wave test-body limit: prescribed prepared carrier drives tidal probes; probe stress/backreaction is omitted.'


def build(n):
    if type(n) is not int or n not in REFINEMENTS:
        raise ValueError(f'n must be one of {REFINEMENTS}')
    P=4096*n*n; Q=2*P*n*n; D=6*Q
    base=build_carrier(Q,2)
    terms=[(base.names[m.target],m.coeff,tuple((base.names[f.gear],f.offset,f.field) for f in m.factors))
           for m in base.monomials]
    f=lambda g:(g,ZERO,'b')
    for x,y in (PROBES[:2],PROBES[2:]):
        terms += [(x,D,(f(x),)),(y,D,(f(y),)),
                  (x,6,(f('p.X'),f(x)),{'designated_one_way':ONE_WAY}),
                  (x,6,(f('q.X'),f(y)),{'designated_one_way':ONE_WAY}),
                  (y,6,(f('q.X'),f(x)),{'designated_one_way':ONE_WAY}),
                  (y,-6,(f('p.X'),f(y)),{'designated_one_way':ONE_WAY})]
    tensor=Tensor(list(base.names)+list(PROBES),terms,Q=Q,strict_support=True)
    assert tensor.rank==3 and check_reciprocity(tensor).ok
    return tensor,dict(n=n,L=3*n,P=P,Q=Q,D=D,steps=PERIOD*n,scale=SCALE_BASE*n**4,dt=f'1/{n}')


def profiles(p,kind):
    if kind not in ('flat','plus','mixed'):
        raise ValueError('kind must be flat, plus or mixed')
    # Floating point selects initial integers only; exported seed is authoritative.
    phase=2*np.pi*np.arange(2*p['L'])/(2*p['L'])
    plus=np.rint(p['P']*np.sin(phase)/50).astype(np.int64)
    cross=np.rint(p['P']*np.cos(phase)/75).astype(np.int64)
    if kind=='flat': plus[:]=0
    if kind!='mixed': cross[:]=0
    return np.stack([plus,cross])


def expected_carrier(p,profile,tick):
    z=lattice(p['L']).all_coords()[:,2]
    return np.array([profile[j,(2*z+bank+tick)%(2*p['L'])] for j in range(2) for bank in (0,1)],dtype=np.int64)


def prepare(tensor,p,profile):
    L=p['L']; a=np.zeros((8,L**3),dtype=np.int64); b=a.copy()
    a[:4]=expected_carrier(p,profile,-1); b[:4]=expected_carrier(p,profile,0)
    r=(np.arange(b.size,dtype=np.int64).reshape(b.shape)*17+5)%p['D']
    for start in (4,6):
        b[start+(start==6)]=p['scale']
        for node in range(L**3):
            x,y=int(b[start,node]),int(b[start+1,node])
            A,B=int(b[0,node]),int(b[2,node])
            # Both basis arms have initial radial affine velocity 1/16.
            a[start,node]=x-x//(16*p['n'])+round(Fraction(A*x+B*y,2*p['P']*p['n']**2))
            a[start+1,node]=y-y//(16*p['n'])+round(Fraction(B*x-A*y,2*p['P']*p['n']**2))
    return State(L,a,b,r)


def reference(p,profile,substeps):
    """Independent continuum geodesics for a declared smooth trigonometric decoder.

    Each arm stores (x,y,dx/du,dy/du,v); u itself is affine proper time.
    The FFT defines interpolation of the seed, never a runtime update.
    """
    coeff=np.fft.fft(profile/p['P'],axis=1)/profile.shape[1]
    frequencies=2*np.pi*np.fft.fftfreq(profile.shape[1],d=1/p['n'])
    def rhs(t,vec):
        A,B=np.real(coeff@np.exp(1j*frequencies*t))
        x,y,vx,vy,_=vec.T
        H=A*(x*x-y*y)+2*B*x*y
        return np.stack([vx,vy,A*x+B*y,B*x-A*y,(1+vx*vx+vy*vy+H)/2],axis=1)
    vec=np.array([[1,0,1/16,0,0],[0,1,0,1/16,0]],dtype=float)
    samples=[vec.copy()]; h=1/(p['n']*substeps); t=0.
    for _ in range(p['steps']):
        for __ in range(substeps):
            k1=rhs(t,vec); k2=rhs(t+h/2,vec+h*k1/2)
            k3=rhs(t+h/2,vec+h*k2/2); k4=rhs(t+h,vec+h*k3)
            vec=vec+h*(k1+2*k2+2*k3+k4)/6; t+=h
        samples.append(vec.copy())
    return np.array(samples)


def run_case(n,kind,out=None):
    tensor,p=build(n); profile=profiles(p,kind); seed=prepare(tensor,p,profile)
    engine=Engine(tensor,p['Q']); state=seed
    # Full snapshots, including all remainders, are preserved for reproducibility.
    history=[np.stack([seed.a,seed.b,seed.r])]
    positions=[seed.b[4:,0].astype(float)/p['scale']]; official=[]
    decoded_a=seed.a[4:,0].copy(); decoded_b=seed.b[4:,0].copy()
    max_ledger=0; max_rforce=0.
    for tick in range(1,p['steps']+1):
        following=engine.step(state)
        assert np.array_equal(following.b[:4],expected_carrier(p,profile,tick))
        assert np.array_equal(following.a[:4],expected_carrier(p,profile,tick-1))
        assert np.array_equal(following.r[:4],seed.r[:4])
        A,B=state.b[0],state.b[2]
        for start in (4,6):
            x,y=state.b[start:start+2]
            force=np.stack([A*x+B*y,B*x-A*y])
            residual=p['D']*(following.b[start:start+2]-2*state.b[start:start+2]+state.a[start:start+2])-12*force-(state.r[start:start+2]-following.r[start:start+2])
            value=int(np.max(np.abs(residual))); max_ledger=max(max_ledger,value)
            assert value==0
        log=engine.clicks(state,following,tick).select('official')
        rows={int(g):int(q) for g,node,q in zip(log.gear,log.node,log.quotient) if int(node)==0 and int(g)>=4}
        ell=np.array([rows.get(g,0) for g in range(4,8)],dtype=np.int64)
        # Audit absent rows independently. No hidden replacement values enter decoder.
        assert np.array_equal(ell,following.b[4:,0]+state.a[4:,0])
        decoded_a,decoded_b=decoded_b,ell-decoded_a
        assert np.array_equal(decoded_b,following.b[4:,0])
        official.append(ell.tolist()); positions.append(decoded_b.astype(float)/p['scale'])
        max_rforce=max(max_rforce,float(np.max(np.abs(state.r[4:]-following.r[4:])))*n*n/(p['D']*p['scale']))
        history.append(np.stack([following.a,following.b,following.r]));state=following
    assert engine.rewind(state,p['steps']).same_as(seed)
    positions=np.array(positions)
    ref=reference(p,profile,64); finer=reference(p,profile,128)
    oracle_error=float(np.max(abs(ref-finer)))
    assert oracle_error<1e-8
    refpositions=finer[:,:,:2].reshape(-1,4)
    error=float(np.max(abs(positions-refpositions)))
    if kind=='flat': assert error<1e-12
    patch_radius=3
    assert float(np.max(abs(positions)))<patch_radius
    complete=np.stack(history)
    file_hash=None
    if out is not None:
        out=Path(out);out.mkdir(parents=True,exist_ok=True)
        path=out/f'{kind}_n{n}.npz'
        np.savez_compressed(path,states=complete,profile=profile,positions=positions,reference_geodesics=finer,
                            official_quotients=np.array(official,dtype=np.int64))
        file_hash=hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(kind=kind,parameters=p,gears=tensor.G,rank=tensor.rank,monomials=len(tensor.monomials),
                designated_test_body_terms=len(tensor.designations),strict_support=True,
                reciprocity_excluding_designated_terms=True,tensor_fingerprint=tensor.fingerprint,
                exact_carrier_shift_every_step=True,carrier_remainders_constant=True,exact_rewind=True,
                tidal_integer_ledger_max_residual=max_ledger,official_only_position_decoder_exact=True,
                maximum_position_error=error,reference_halving_error=oracle_error,
                maximum_remainder_acceleration=max_rforce,position_patch_radius=patch_radius,
                peak_abs_position=float(np.max(abs(positions))),
                final_positions=positions[-1].tolist(),reference_final_positions=refpositions[-1].tolist(),
                minimum_reference_v=float(np.min(finer[:,:,4])),
                full_trace_shape=list(complete.shape),full_trace_values_sha256=hashlib.sha256(complete.tobytes()).hexdigest(),
                trace_file_sha256=file_hash,profile_integer_samples=profile.tolist(),
                engine_arithmetic_counts=engine.stats)


def off_sector_control():
    tensor,p=build(1); seed=prepare(tensor,p,profiles(p,'mixed'))
    seed.a[0,0]+=1
    engine=Engine(tensor,p['Q']); after=engine.step(seed)
    assert not np.array_equal(after.b[:4],expected_carrier(p,profiles(p,'mixed'),1))
    assert engine.inverse_step(after).same_as(seed)
    return dict(prepared_transport_identity_fails=True,exact_inverse_still_passes=True,
                meaning='Invertibility alone does not certify the pp-wave prepared sector.')


def run(out,refinements=REFINEMENTS):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    cases=[]
    for n in refinements:
        for kind in ('flat','mixed'):
            row=run_case(n,kind,out); cases.append(row)
            print(json.dumps(dict(n=n,kind=kind,max_error=row['maximum_position_error'],rewind=True)),flush=True)
    errors=[c['maximum_position_error'] for c in cases if c['kind']=='mixed']
    orders=[math.log(errors[i]/errors[i+1])/math.log(refinements[i+1]/refinements[i]) for i in range(len(errors)-1)]
    report=dict(schema='pp-wave-solution-v1',scope='Full nonlinear continuum vacuum pp-wave decoder plus convergent autonomous integer test-body probes; not general or sourced Einstein evolution.',
                geometry=audit(),boundary=boundary_audit(),off_sector_control=off_sector_control(),cases=cases,
                observed_position_convergence_orders=orders,
                refinements=list(refinements),
                decoder='A=p.X/P, B=q.X/P at sampled u=(tick+2z)/n. Smooth periodic trigonometric interpolation is fixed by the complete initial fine-ring profile.',
                coordinates='u is affine proper time for the reference timelike geodesics. Stored arms are transverse separations in the Brinkmann chart. v is computed by the independent reference, not stored in the automaton.',
                integer_law='u_x=D*x+6*(p.X*x+q.X*y); u_y=D*y+6*(q.X*x-p.X*y); D=12*P*n^2.',
                acceptance=dict(finest_n=refinements[-1],finest_position_error_below_0_005=(cases[-1]['maximum_position_error']<0.005),
                                last_observed_order_above_1_5=(orders[-1]>1.5 if orders else None)),
                limitations=['The metric is a declared new decoder, not the old TT metric and not inferred from all matter species.',
                 'Only the prepared axis-travelling sector is used; off-sector data need not be vacuum geometry.',
                 'Geometry is exact in the smooth decoded continuum; finite-step detector motion has measured discretization and remainder errors.',
                 'Test bodies do not source the carrier. No massive matter source, Einstein constraint propagation for arbitrary states, or universal coupling is established.',
                 'The transverse metric is valid on a local patch and is not periodically glued across the cube; this is not a global torus solution.',
                 'The reference reconstructs longitudinal v; runtime gears measure transverse tidal motion only.'],
                provenance=dict(base_commit='1c11a4f63f2d570277cdd4e4451e35b4e1cbcac8',python=platform.python_version(),numpy=np.__version__,
                  files={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),Path(__file__).with_name('pp_wave_geometry.py'),Path(__file__).with_name('retimed_tensor_wave.py'),ROOT/'universe24/core/engine.py',ROOT/'universe24/core/tensor.py']}))
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'runs/geometry/pp_wave')
    parser.add_argument('--refinements',type=int,nargs='+',choices=REFINEMENTS,default=list(REFINEMENTS))
    args=parser.parse_args()
    if args.refinements!=sorted(set(args.refinements)):
        parser.error('refinements must be strictly increasing')
    result=run(args.out,tuple(args.refinements))
    print(json.dumps(dict(output=str(args.out),orders=result['observed_position_convergence_orders'],acceptance=result['acceptance'])),flush=True)
