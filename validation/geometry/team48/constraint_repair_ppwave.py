"""Exact sourced pp-wave transport control in five unchanged Engine channels.

This is a prepared exact Einstein/null-dust sector and independent validation
control, not a replacement for the general charged-scalar/frame candidate.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import numpy as np
import sympy as sp
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice

ROOT=Path(__file__).resolve().parents[3]
NAMES=('ppwave.rho','ppwave.plus','ppwave.cross','ppwave.X','ppwave.Y')
ZERO=(0,0,0)


def build():
    terms=[]
    for name in NAMES[:3]:
        for offset in ((0,0,1),(0,0,-1)):
            terms.append((name,3,((name,offset,'b'),)))
    for name in NAMES[3:]:
        terms.append((name,6,((name,ZERO,'b'),)))
    return Tensor(NAMES,terms,strict_support=True)


def profile_at(z):
    z=F(z)%1
    w=(z+F(1,4))%1
    bump=64*z**4*(1-z)**4
    return (1+bump,bump/16,4*w**4*(1-w)**4)


def prepare(L,source_scale=None):
    if type(L) is not int or L<4 or L%4:
        raise ValueError('lattice side must be a positive multiple of four')
    lat=lattice(L)
    xyz=lat.all_coords()
    source_resolution=16*L**8 if source_scale is None else source_scale
    if type(source_resolution) is not int or source_resolution<1:raise ValueError('positive integer source calibration required')
    def profiles(z):
        # Quantization occurs once during preparation, never during evolution.
        return tuple((value*source_resolution).numerator//(value*source_resolution).denominator
                     for value in profile_at(F(z,L)))
    b=np.asarray([[0]*lat.N for _ in NAMES],dtype=object)
    for n,(x,y,z) in enumerate(xyz):
        b[:3,n]=profiles(int(z))
        b[3,n]=2*int(x)-L
        b[4,n]=2*int(y)-L
    a=b.copy()
    a[:3]=b[:3,lat.shift_index((0,0,1))]
    r=np.arange(len(NAMES)*lat.N).reshape(len(NAMES),lat.N)%6
    return State(L,a,b,r),{'source_resolution':source_resolution,'coordinate_denominator':2*L,'dx':F(1,L),'dt':F(1,L)}


def readout(state,calibration):
    q=calibration['source_resolution'];c=calibration['coordinate_denominator']
    rho,p,cross=(np.asarray([F(int(v),q) for v in state.b[i]],dtype=object) for i in range(3))
    x,y=(np.asarray([F(int(v),c) for v in state.b[i]],dtype=object) for i in (3,4))
    H=-rho*(x*x+y*y)/2+p*(x*x-y*y)+2*cross*x*y
    return rho,p,cross,x,y,H


def symbolic_geometry():
    t,x,y,z=sp.symbols('t x y z',real=True)
    coordinates=(t,x,y,z)
    # Engine prepares profiles F(z-t); equivalently the arbitrary function
    # rho(u) below is F(-u). No restriction is imposed by that reflection.
    rho=sp.Function('rho')(t-z)
    p=sp.Function('p')(t-z)
    c=sp.Function('c')(t-z)
    H=-rho*(x*x+y*y)/2+p*(x*x-y*y)+2*c*x*y
    ell=sp.Matrix([1,0,0,-1])
    eta=sp.diag(-1,1,1,1)
    metric=eta+H*(ell*ell.T)
    ell_up=eta*ell
    inverse=eta-H*(ell_up*ell_up.T)
    assert sp.simplify(metric*inverse)==sp.eye(4)
    assert sp.simplify(metric.det())==-1
    G=[[[sp.simplify(sum(inverse[a,d]*(sp.diff(metric[d,c],coordinates[b])
             +sp.diff(metric[d,b],coordinates[c])-sp.diff(metric[b,c],coordinates[d]))/2
             for d in range(4))) for c in range(4)] for b in range(4)] for a in range(4)]
    ricci=sp.Matrix(4,4,lambda b,d:sp.simplify(sum(
        sp.diff(G[a][b][d],coordinates[a])-sp.diff(G[a][b][a],coordinates[d])
        +sum(G[a][a][c]*G[c][b][d]-G[a][d][c]*G[c][b][a] for c in range(4))
        for a in range(4))))
    scalar=sp.simplify(sum(inverse[a,b]*ricci[a,b] for a in range(4) for b in range(4)))
    stress=rho*(ell*ell.T)
    einstein=ricci-metric*scalar/2
    assert sp.simplify(einstein-stress)==sp.zeros(4)
    assert scalar==0
    k=sp.Matrix([1,0,0,1])
    assert sp.simplify((k.T*metric*k)[0])==0
    assert all(sp.simplify(sum(G[a][b][c]*k[c] for c in range(4)))==0
               for a in range(4) for b in range(4))
    raised=sp.simplify(inverse*stress*inverse)
    divergence=[sp.simplify(sum(sp.diff(raised[a,b],coordinates[a])
                    +sum(G[a][a][c]*raised[c,b]+G[b][a][c]*raised[a,c]
                         for c in range(4)) for a in range(4))) for b in range(4)]
    assert divergence==[0]*4
    # The four Einstein constraint projections and six evolution projections
    # vanish because their full independently reconstructed tensor is zero.
    # A nonzero polarization supplies Weyl curvature, not only pure Ricci.
    Rtxtx=sp.simplify(sum(metric[0,a]*(sp.diff(G[a][1][1],t)
                    -sp.diff(G[a][1][0],x)+sum(G[a][0][c]*G[c][1][1]
                    -G[a][1][c]*G[c][1][0] for c in range(4))) for a in range(4)))
    assert sp.simplify(Rtxtx-(rho/2-p))==0
    return {'metric':'eta+H*(dt-dz)^2',
            'H':'-rho(u)*(x*x+y*y)/2+p(u)*(x*x-y*y)+2*c(u)*x*y; u=t-z',
            'determinant':'-1','all_16_Einstein_minus_null_dust_components_zero':True,
            'all_4_stress_divergence_components_zero':True,
            'parallel_null_source_vector':'(1,0,0,1)',
            'R_txtx':'rho(u)/2-p(u)','Weyl_txtx':'-p(u)',
            'Einstein_constraints_and_evolution':'All four/six projections vanish identically on the stated continuum family.'}


def audit(out):
    tensor=build();engine=Engine(tensor)
    rows=[]
    for L in (4,8,16,32):
        seed,cal=prepare(L);state=seed.copy();lat=lattice(L)
        steps=L//4
        initial_readout=readout(seed,cal)
        min_rho=None;min_spatial=None;max_bits=0
        for step in range(steps+1):
            shifted=lat.shift_index((0,0,-step))
            assert np.array_equal(state.b[:3],seed.b[:3,shifted])
            assert np.array_equal(state.b[3:],seed.b[3:])
            assert np.array_equal(state.r,seed.r)
            rho,p,c,x,y,H=readout(state,cal)
            assert all(v>0 for v in rho)
            assert all(1+v>0 for v in H)
            min_rho=min(rho) if min_rho is None else min(min_rho,min(rho))
            min_spatial=min(1+v for v in H) if min_spatial is None else min(min_spatial,min(1+v for v in H))
            max_bits=max(max_bits,max(abs(int(v)).bit_length() for v in state.a.flat),
                         max(abs(int(v)).bit_length() for v in state.b.flat))
            # At interior transverse nodes the literal nearest-neighbor
            # Laplacian of reconstructed H gives exact rho. Boundary chart
            # seams are explicitly excluded, not claimed to satisfy EFE.
            X=lat.all_coords()[:,0];Y=lat.all_coords()[:,1]
            interior=(X>0)&(X<L-1)&(Y>0)&(Y<L-1)
            lap=np.zeros(lat.N,dtype=object)
            for off in ((1,0,0),(0,1,0)):
                neg=tuple(-v for v in off)
                lap+=(H[lat.shift_index(off)]-2*H+H[lat.shift_index(neg)])/(cal['dx']**2)
            assert all((-lap/2-rho)[interior]==0)
            if step<steps:
                before=state;state=engine.step(state)
                assert engine.inverse_step(state).same_as(before)
        assert engine.rewind(state,steps).same_as(seed)
        # Exact independently sampled source at final physical t=1/4.
        final_readout=readout(state,cal)
        for n,(xi,yi,zi) in enumerate(lat.all_coords()):
            expected=profile_at(F(int(zi),L)-F(1,4))
            assert all(final_readout[i][n]==expected[i] for i in range(3))
            xx,yy=F(2*int(xi)-L,2*L),F(2*int(yi)-L,2*L)
            expected_H=-expected[0]*(xx*xx+yy*yy)/2+expected[1]*(xx*xx-yy*yy)+2*expected[2]*xx*yy
            assert final_readout[5][n]==expected_H
        serialized=Tensor.from_dict(tensor.to_dict())
        replay=State.from_dict(seed.to_dict())
        for _ in range(steps):replay=Engine(serialized).step(replay)
        assert replay.same_as(state)
        rows.append({'L':L,'dt=dx':str(cal['dt']),'physical_final_time':'1/4',
                     'steps':steps,'min_positive_null_density':str(min_rho),
                     'minimum_spatial_gzz':str(min_spatial),
                     'source_sample_error':'0','metric_sample_error':'0',
                     'literal_transverse_Einstein_residual_interior':'0',
                     'full_state_replay_and_rewind':True,'max_retained_integer_bits':max_bits})
    quantization=[]
    for source_resolution in (16,64,256,1024,4096,16384):
        initial,cal=prepare(8,source_resolution);state=initial
        for _ in range(2):state=engine.step(state)
        decoded=readout(state,cal)
        errors=[]
        for n,(_,_,z) in enumerate(lattice(8).all_coords()):
            expected=profile_at(F(int(z),8)-F(1,4))
            errors.extend(abs(decoded[i][n]-expected[i]) for i in range(3))
        err=max(errors)
        assert err<F(1,source_resolution) and min(decoded[0])>0
        assert engine.rewind(state,2).same_as(initial)
        quantization.append({'source_scale':source_resolution,'fixed_L':8,'fixed_final_time':'1/4',
                             'max_profile_error':str(err),'bound':str(F(1,source_resolution)),
                             'complete_rewind':True})
    assert F(quantization[-1]['max_profile_error'])<F(quantization[0]['max_profile_error'])
    # Wrong temporal branch remains reversible but ceases to be parallel null
    # transport. This failure must not be relabeled an Einstein trajectory.
    bad,cal=prepare(8);bad.a[:3]=bad.b[:3]
    bad_next=engine.step(bad)
    off_manifold=not np.array_equal(bad_next.b[:3],bad.b[:3,lattice(8).shift_index((0,0,-1))])
    assert off_manifold and engine.inverse_step(bad_next).same_as(bad)
    # Transverse modulation is not part of the prepared pp-wave source
    # family. It remains reversible but the literal metric/source relation
    # fails, preventing an ansatz-only oracle from silently accepting it.
    nonplane,cal=prepare(8);lat=lattice(8)
    spot=next(n for n,xyz in enumerate(lat.all_coords()) if tuple(xyz)==(3,3,3))
    nonplane.b[0,spot]+=cal['source_resolution']
    nonplane.a[0]=nonplane.b[0,lat.shift_index((0,0,1))]
    changed=engine.step(nonplane);rho,_,_,_,_,H=readout(changed,cal)
    lap=np.zeros(lat.N,dtype=object)
    for off in ((1,0,0),(0,1,0)):
        lap+=(H[lat.shift_index(off)]-2*H+H[lat.shift_index(tuple(-v for v in off))])/(cal['dx']**2)
    coords=lat.all_coords();interior=(coords[:,0]>0)&(coords[:,0]<7)&(coords[:,1]>0)&(coords[:,1]<7)
    transverse_failure=max(abs(v) for v in (-lap/2-rho)[interior])
    assert transverse_failure>0 and engine.inverse_step(changed).same_as(nonplane)
    report={'scope':'exact nonlinear pp-wave/null-dust prepared control, not general Einstein repair',
        'channels':tensor.G,'retained_integers_per_node':3*tensor.G,
        'monomials':len(tensor),'degree':max(m.degree for m in tensor.monomials),
        'tensor_fingerprint':tensor.fingerprint,'single_face_support':not tensor.support_violations(),
        'engine_profile_convention':'F(z-t); symbolic rho(u)=F(-u) with u=t-z',
        'nonplane_source_negative_control_residual':str(transverse_failure),
        'same_fixed_six_tensor_all_resolutions':True,'symbolic_geometry':symbolic_geometry(),
        'refinement':rows,'independent_seed_quantization_refinement':quantization,'off_prepared_temporal_branch_negative_control_detected':off_manifold,
        'limitations':['Only parallel null dust and two pp-wave polarizations; no scalar, dark dust, charged matter or general geometry.',
            'Metric is a proved passive algebraic readout of retained profiles and transverse coordinates, not the general frame integrator.',
            'Exact spatial and temporal refinement is joint at dt=dz. Arbitrary independent timestep and space refinement is not demonstrated.',
            'Periodic transport is in z; x/y coordinate seams are not a global periodic solution. Geometry claims cover the declared interior coordinate patch.',
            'No material apparatus, click-only clock/detector, or arbitrary-seed stability claim.'],
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    print(json.dumps(audit(ROOT/'runs/team48/constraint_repair/ppwave.json'),indent=2))
