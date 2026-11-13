"""Packet and canonical-click experiment on the unchanged 18-channel candidate.

All physical runs execute the original Engine on full cubic arrays. Plane
symmetry is checked at every step and used ONLY for lossless trace compression.
No detector, threshold, boundary fix, or runtime source is introduced.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
from light_tensor_audit import tensor, CG, PAIRS, SOURCE_PIN
from universe24.core import Engine, State
from universe24.system.decoder import make_transition, decode_transition


def line_curl(C, v):
    # Independent 1D oracle of the planar restriction; not used for advancement.
    cv = np.asarray([sum(C[i,j]*v[j] for j in range(3)) for i in range(3)], dtype=object)
    dx = np.roll(cv, -1, axis=1)-np.roll(cv, 1, axis=1)
    out = np.zeros_like(v, dtype=object)
    out[1], out[2] = -dx[2], dx[1]
    return out


def matrix(plane):
    return np.asarray([[plane[CG[i,j]] for j in range(3)] for i in range(3)], dtype=object)


def inverse_prepare(plane):
    C = matrix(plane)
    p = np.asarray(plane, dtype=object)
    out = p.copy()
    out[:6],out[6:12] = p[6:12].copy(),p[:6].copy()
    c1, c2 = line_curl(C,p[6:9]), line_curl(C,p[3:6])
    assert not any((c1 % 3).flat) and not any((c2 % 3).flat)
    out[3:6] += c1//3
    out[6:9] -= c2//3
    return out


def ideal_next(p):
    p=np.asarray(p,dtype=object)
    C = matrix(p)
    out = p.copy()
    out[:6],out[6:12] = p[6:12].copy(),p[:6].copy()
    c1,c2 = line_curl(C,p[9:12]),line_curl(C,p[:3])
    assert not any((c1 % 3).flat) and not any((c2 % 3).flat)
    out[:3] += c1//3
    out[9:12] -= c2//3
    return out


def expand(p, L):
    return np.repeat(p, L*L, axis=1)


def compress(state):
    out = []
    for bank in (state.a,state.b,state.r):
        grid=bank.reshape(18,state.L,state.L*state.L)
        line=grid[:,:,0]
        assert np.all(grid == line[:,:,None]), 'transverse symmetry lost; cannot compress'
        out.append(line.copy())
    return out


def make_seed(L,H,geometry,amplitude=1,precision=None,order=12,center=10):
    Q = 3**(H+1) if precision is None else precision
    f=np.zeros(L,dtype=object)
    start=center-order//2
    for j in range(order+1):
        f[(start+j)%L] = math.comb(order,j)
    q=np.ones(L,dtype=object)
    if geometry=='fast': q[:]=2
    if geometry=='step': q[14:]=2
    p=np.zeros((18,L),dtype=object)
    p[CG[0,0]]=1
    p[CG[1,1]]=q
    p[CG[2,2]]=q
    p[1]=6*f*Q*amplitude
    # Center the magnetic field in the first half-step to reduce an artificial
    # backward pulse: B = D + (1/6) D_x(q D), with D_x=S+ - S-.
    qD=q*p[1]
    derivative=np.roll(qD,-1)-np.roll(qD,1)
    assert not any(derivative % 6)
    p[5]=p[1]+derivative//6
    a=inverse_prepare(p)
    carry=np.asarray([[(g+x)%6 for x in range(L)] for g in range(18)],dtype=object)
    seed=State(L,expand(a,L),expand(p,L),expand(carry,L))
    return seed,Q,q


def exact_ledger(p):
    C=matrix(p)
    D,B=p[:3],p[3:6]
    CD=np.asarray([sum(C[i,j]*D[j] for j in range(3)) for i in range(3)],dtype=object)
    CB=np.asarray([sum(C[i,j]*B[j] for j in range(3)) for i in range(3)],dtype=object)
    cB=line_curl(C,B)
    CcB=np.asarray([sum(C[i,j]*cB[j] for j in range(3)) for i in range(3)],dtype=object)
    return int(3*sum((D*CD+B*CB).flat)-sum((D*CcB).flat))


def readout(p,Q,tick):
    active=0 if tick%2==0 else 6
    # Float conversion is observation only, after exact Engine evolution.
    C=np.asarray(matrix(p),dtype=float)
    D=np.asarray(p[active:active+3],dtype=float)/Q
    B=np.asarray(p[active+3:active+6],dtype=float)/Q
    energy=.5*sum(D[i]*sum(C[i,j]*D[j] for j in range(3))+
                  B[i]*sum(C[i,j]*B[j] for j in range(3)) for i in range(3))
    return D,B,energy


def fields_hash(p):
    return hashlib.sha256(json.dumps(p.tolist(),separators=(',',':')).encode()).hexdigest()


def run_case(out, name, L=41,H=24,geometry='flat',amplitude=1,precision=None,order=12,center=10, canonical=False):
    out.mkdir(parents=True,exist_ok=False)
    law=tensor(); eng=Engine(law)
    seed,Q,q=make_seed(L,H,geometry,amplitude,precision,order,center)
    a,p,r=compress(seed)
    initial_support=np.flatnonzero(np.any(a[:12]!=0,axis=0)|np.any(p[:12]!=0,axis=0))
    x=np.arange(L)
    dist=np.min(np.minimum((x[:,None]-initial_support[None,:])%L,
                           (initial_support[None,:]-x[:,None])%L),axis=1)
    setup={'name':name,'L':L,'nodes':L**3,'steps':H,'geometry':geometry,
           'Q':str(Q),'order':order,'center':center,'amplitude':amplitude,
           'q_profile':[int(z) for z in q],'tensor_hash':law.fingerprint,'source_pin':SOURCE_PIN,
           'macro_time_per_two_ticks':2/3,'length_per_cell':1,
           'initial_complete_field_support':initial_support.tolist(),
           'trace_encoding':'Each a,b,r array is 18 by L. Expand each x column L^2 times in y,z order. Homogeneity checked against EVERY full-array value at EVERY step.',
           'click_encoding':'Each row at x,gear represents all L^2 y,z coordinates with the exact same quotient and kind. No threshold or record filtering.',
           'scope':'plane-symmetric classical test-field pulse; static optical geometry; no operational detector or Einstein source closure'}
    (out/'protocol.json').write_text(json.dumps(setup,indent=2))
    (out/'tensor.json').write_text(json.dumps(law.to_dict(),indent=2))
    tr=gzip.open(out/'full_trace_planes.jsonl.gz','wt')
    cl=gzip.open(out/'canonical_click_planes.jsonl.gz','wt')
    def save(tick,aa,pp,rr):
        tr.write(json.dumps({'tick':tick,'a':aa.tolist(),'b':pp.tolist(),'r':rr.tolist()},separators=(',',':'))+'\n')
    save(0,a,p,r)
    D,B,E=readout(p,Q,0)
    energy=[E.tolist()]; electric=[D[1].tolist()]; magnetic=[B[2].tolist()]; times=[0.]
    clicks_time=[];weights_time=[];click_classes=[0,0,0];outside=[];events_zero_field=0
    arrivals=[None]*L;weighted_centers=[];states=seed;energy0=exact_ledger(p)
    peak_bits=0;fixed_carry=True;exact_oracle=True;zero_quotient_changes=0
    start=time.monotonic();last_p=p
    raw_click_total=0;all_checks=0
    for tick in range(1,H+1):
        following=eng.step(states)
        assert eng.inverse_step(following).same_as(states)
        aa,pp,rr=compress(following)
        same_r=np.array_equal(rr,r)
        fixed_carry &= same_r
        if precision is None:
            assert np.array_equal(pp,ideal_next(last_p))
            assert same_r
        else:
            try: exact_oracle &= np.array_equal(pp,ideal_next(last_p))
            except AssertionError: exact_oracle=False
        log=eng.clicks(states,following,step=tick)
        assert np.all(log.gear<12), 'unchanged optical background should have no clicks'
        counts=np.bincount(log.node//(L*L),minlength=L)
        assert not any(counts % (L*L))
        line_counts=counts//(L*L)
        raw_click_total+=len(log)
        click_classes=[v+int(np.count_nonzero(log.kind==i)) for i,v in enumerate(click_classes)]
        mask=log.node % (L*L)==0
        rows=[];weights=np.zeros(L)
        for node,g,kind,quo in zip(log.node[mask],log.gear[mask],log.kind[mask],log.quotient[mask]):
            xx=int(node)//(L*L)
            rows.append([xx,int(g),int(kind),int(quo)])
            weights[xx]+=abs(int(quo))/Q
            if arrivals[xx] is None: arrivals[xx]=tick
        cl.write(json.dumps({'tick':tick,'multiplicity':L*L,'rows':rows},separators=(',',':'))+'\n')
        clicks_time.append(line_counts.tolist());weights_time.append(weights.tolist())
        # The true computational support starts from BOTH prepared histories.
        assert not any(line_counts[dist>tick])
        fullchanged=(states.a!=following.a)|(states.b!=following.b)|(states.r!=following.r)
        quotient=following.b+states.a
        zero_quotient_changes += int(np.count_nonzero(fullchanged & (quotient==0)))
        D,B,E=readout(pp,Q,tick)
        events_zero_field+=int(sum(counts[E==0]))
        if canonical and tick==1:
            record=make_transition(law,states,following,run_id='c'*64,step=tick)
            decoded=decode_transition(record,law)
            assert len(decoded)==len(log)
            assert all((d['node'],d['channel'],d['kind'],d['quotient'])==
                       (int(n),int(g),'C'+str(int(k)),int(v))
                       for d,n,g,k,v in zip(decoded,log.node,log.gear,log.kind,log.quotient))
        if tick%2==0:
            energy.append(E.tolist());electric.append(D[1].tolist());magnetic.append(B[2].tolist());times.append(tick/3)
            if precision is None:
                assert exact_ledger(pp)==energy0
                assert not any(pp[6:12].flat)
                assert not any(pp[[0,2,3,4]].flat)
            if geometry=='flat':
                outside_mask=dist>tick/3+1e-12
                outside.append({'tick':tick,'time':tick/3,
                                'clicks_outside_target_null_cone':int(sum(counts[outside_mask])),
                                'energy_fraction_outside_target_null_cone':float(sum(E[outside_mask])/sum(E))})
        save(tick,aa,pp,rr)
        peak_bits=max(peak_bits,max(abs(int(v)).bit_length() for v in pp.flat))
        last_p=pp; states=following;all_checks+=18*L**3*3
        if tick%6==0:
            print(json.dumps({'case':name,'tick':tick,'seconds':round(time.monotonic()-start,2),'clicks':raw_click_total}),flush=True)
    tr.close();cl.close()
    assert eng.rewind(states,H).same_as(seed)
    if precision is None: assert fixed_carry
    Es=np.asarray(energy)
    centers=(Es*x).sum(axis=1)/Es.sum(axis=1)
    variances=(Es*(x[None,:]-centers[:,None])**2).sum(axis=1)/Es.sum(axis=1)
    positive_centers=[]
    # Spatial energy centroid is coordinate-dependent; it is not an operational clock.
    slope=float(np.polyfit(times,centers,1)[0])
    late_slope=float(np.polyfit(times[-5:],centers[-5:],1)[0])
    summary={'name':name,'nodes':L**3,'steps':H,'macrosteps':H//2,
             'clicks':raw_click_total,'click_classes':dict(zip(('C0','C1','C2'),click_classes)),
             'first_click_ticks':arrivals,'initial_centroid':float(centers[0]),'final_centroid':float(centers[-1]),
             'coordinate_centroid_speed_fit':slope,'late_coordinate_speed_fit':late_slope,
             'initial_width_std':float(np.sqrt(variances[0])),'final_width_std':float(np.sqrt(variances[-1])),
             'peak_integer_bits':peak_bits,'fixed_carry':bool(fixed_carry),'exact_prepared_sector':bool(exact_oracle),
             'complete_step_inverse':'passed','full_rewind':'passed','strict_computational_cone':'passed',
             'lossless_plane_checks':all_checks,'canonical_decoder_crosscheck':bool(canonical),
             'clicks_at_zero_current_field_energy':events_zero_field,
             'changed_triples_with_zero_quotient':zero_quotient_changes,
             'target_cone_observations':outside,
             'initial_modified_energy_integer':str(energy0),'final_modified_energy_integer':str(exact_ledger(last_p)),
             'max_edge_energy_fraction':float(np.max((Es[:,:2].sum(axis=1)+Es[:,-2:].sum(axis=1))/Es.sum(axis=1))),
             'time_seconds':time.monotonic()-start,'final_plane_hash':fields_hash(last_p)}
    payload={'protocol':setup,'summary':summary,'times':times,'energy':energy,
             'D_y':electric,'B_z':magnetic,'clicks_per_node_per_tick':clicks_time,
             'absolute_quotient_per_node_per_tick':weights_time,'centroids':centers.tolist()}
    (out/'observations.json').write_text(json.dumps(payload,separators=(',',':')))
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    return payload


def vacuum_control():
    law=tensor(); eng=Engine(law); L=5
    seed,_,_=make_seed(L,6,'flat',order=2,center=2)
    seed.a[:12]=0;seed.b[:12]=0
    state=seed
    for tick in range(1,7):
        nxt=eng.step(state)
        assert len(eng.clicks(state,nxt,step=tick))==0
        assert nxt.same_as(seed)
        state=nxt
    return {'steps':6,'clicks':0,'background_unchanged':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    protocol={'purpose':'Actual packet propagation and unfiltered canonical arithmetic clicks',
              'main_cases':['flat','fast','step'],'L':41,'ticks':24,'binomial_order':12,'center':10,
              'cases_same_tensor':True,'interventions':'Only complete seeds differ',
              'metrics':['coordinate energy centroid and width','C0/C1/C2 count','first click time',
                         'quotient magnitude','zero-field clicks','full-support graph cone','flat target metric cone'],
              'controls':['empty field','double amplitude','low initial precision'],
              'no_detector_or_photon_claim':True}
    (args.out/'preregistered_protocol.json').write_text(json.dumps(protocol,indent=2))
    results={}
    for name in ('flat','fast','step'):
        results[name]=run_case(args.out/name,name,geometry=name)
    controls={}
    for name,amp in [('amplitude_1',1),('amplitude_2',2)]:
        controls[name]=run_case(args.out/name,name,L=9,H=12,order=4,center=4,amplitude=amp,canonical=True)
    c1,c2=controls.values()
    assert c1['clicks_per_node_per_tick']==c2['clicks_per_node_per_tick']
    assert c1['summary']['click_classes']==c2['summary']['click_classes']
    assert np.allclose(np.asarray(c2['energy']),4*np.asarray(c1['energy']),rtol=1e-14,atol=0)
    assert np.allclose(np.asarray(c2['absolute_quotient_per_node_per_tick']),2*np.asarray(c1['absolute_quotient_per_node_per_tick']),rtol=1e-14,atol=0)
    low=run_case(args.out/'low_precision','low_precision',L=9,H=12,order=4,center=4,precision=3,canonical=True)
    aggregate={'source_pin':SOURCE_PIN,'tensor_hash':tensor().fingerprint,
               'main':{k:v['summary'] for k,v in results.items()},
               'amplitude_control':{'counts_and_positions_identical':True,'energy_factor':4,'quotient_factor':2,
                                    'clicks_each':c1['summary']['clicks']},
               'vacuum':vacuum_control(),'low_precision':low['summary'],
               'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.out/'aggregate.json').write_text(json.dumps(aggregate,indent=2))
    print(json.dumps(aggregate,indent=2),flush=True)


if __name__=='__main__':main()
