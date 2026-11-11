"""Reproducible audit of the tensor, seed, forward cone and click-only readout.

Run: python -m universe24.tools.audit_contract --L 4 --steps 120 --out runs/contract
No diagnostic feeds back into evolution. Saved tensor and initial state are the
complete run inputs; the report explicitly separates events from carry weights.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import numpy as np
from ..core import Engine, State, Tensor
from ..core.engine import OBJ
from ..core.lattice import DIRECTIONS, ZERO, lattice
from ..demos.one.run_one import build
from ..observe.one import CosmicLedger, CosmicView, state_hash
from ..observe.readout import official_clicks
from ..observe.gravity import click_series, crossing_times, rate_from_crossings


def save_json(path, value):
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        json.dump(value, f, separators=(',', ':'))


def tensor_report(tensor):
    bad = tensor.support_violations()
    max_diameter = 0
    for m in tensor.monomials:
        pts = tensor.physical_support(m)
        max_diameter = max(max_diameter, max(sum(abs(a-b) for a,b in zip(p,q)) for p in pts for q in pts))
    return dict(gears=tensor.G, rank=tensor.rank, max_input_degree=tensor.rank-1,
                shared_Q=tensor.Q, shared_D=6*tensor.Q,
                monomials=len(tensor), census=tensor.census(),
                storage_local=all(all(f.offset in (ZERO,)+DIRECTIONS for f in m.factors)
                                  and len({f.offset for f in m.factors}-{ZERO})<=1 for m in tensor.monomials),
                inverse_stage_sizes=list(map(len,tensor.stages)),
                link_gear_types=sum(g.link is not None for g in tensor.gears),
                strict_one_link_physical_support_violations=len(bad),
                physical_support_max_manhattan_diameter=max_diameter,
                physical_violations_by_output=dict(Counter(tensor.names[m.target].split('.')[0] for m in bad)),
                dynamics_fingerprint=tensor.dynamics_fingerprint,
                full_tensor_fingerprint=tensor.fingerprint)


def scalar_crosscheck(tensor, Q, L=3):
    """Independent receiver loops: no compiled input evaluator is used by oracle."""
    lat=lattice(L); rng=np.random.default_rng(47); checked=0
    e=Engine(tensor,Q)
    samples=(0,1,lat.index(1,1,1))
    for huge in (False,True):
        a=rng.integers(-4,5,size=(tensor.G,lat.N)).astype(OBJ)
        b=rng.integers(-4,5,size=a.shape).astype(OBJ)
        r=rng.integers(0,6*Q,size=a.shape).astype(OBJ)
        if huge: a[0,:]=2**80; b[0,:]=-(2**81)
        s=State(L,a,b,r); actual=e.inputs(s); nxt=e.step(s)
        for n in samples:
            xyz=lat.coords(n); u=[0]*tensor.G
            for m in tensor.monomials:
                v=m.coeff
                for f in m.factors:
                    nb=tuple((xyz[k]+f.offset[k])%L for k in range(3))
                    v*=int(getattr(s,f.field)[f.gear,lat.index(*nb)])
                u[m.target]+=v
            for g in range(tensor.G):
                quotient,remainder=divmod(2*u[g]+int(s.r[g,n]),6*Q)
                expected=(int(s.b[g,n]),quotient-int(s.a[g,n]),remainder)
                if int(actual[g,n])!=u[g] or nxt.gear(g,n)!=expected:
                    raise AssertionError(('scalar oracle mismatch',huge,g,n))
                checked+=1
        if not e.inverse_step(nxt).same_as(s):raise AssertionError('oracle seed rewind')
    return dict(gear_transitions=checked,ordinary_and_bigint=True,mismatches=0)


def cone_check(single_edge=False, stiffness=None):
    """Difference of two complete runs whose seeds differ at exactly one site."""
    _,T,E,s,_=build(7,'none',13)
    field='cosmic.M1'
    if single_edge:
        from ..layers.strict_edge import single_edge_realization
        from ..prepare.strict_edge import lift_seed
        realization=single_edge_realization(T,stiffness=stiffness)
        s=lift_seed(s,realization);T=realization.tensor;E=Engine(T,T.Q)
        field='em.A_x'
    altered=s.copy();origin=(3,3,3);n=lattice(7).index(*origin)
    altered.b[T.gear_index(field),n]+=1024
    lat=lattice(7)
    dist=np.array([sum(min(abs(a-b),7-abs(a-b)) for a,b in zip(lat.coords(i),origin)) for i in range(lat.N)])
    rows=[]
    for step in range(1,4):
        s,altered=E.step(s),E.step(altered)
        changed=np.any((s.a!=altered.a)|(s.b!=altered.b)|(s.r!=altered.r),axis=0)
        outside=int(np.sum(changed & (dist>step)))
        if outside:raise AssertionError('forward cone exceeded')
        rows.append(dict(step=step,changed_sites=int(changed.sum()),outside_cone=outside))
    return dict(L=7,origin=origin,perturbation=field+' b += 1024 in initial state only',steps=rows)


def replay(directory):
    p=Path(directory);report=json.loads((p/'report.json').read_text())
    strict=report.get('construction',{}).get('kind')=='single-physical-edge experiment'
    t=Tensor.from_json((p/'tensor.json').read_text(),strict_support=strict)
    with gzip.open(p/'initial_state.json.gz','rt') as f:s=State.from_dict(json.load(f))
    with gzip.open(p/'final_state.json.gz','rt') as f:expected=State.from_dict(json.load(f))
    e=Engine(t,t.Q)
    if (t.fingerprint!=report['tensor']['full_tensor_fingerprint']
            or state_hash(s,np.arange(t.G))!=report['run']['initial_hash']
            or state_hash(expected,np.arange(t.G))!=report['run']['final_hash']):
        raise AssertionError('saved-input manifest mismatch')
    actual=e.run(s,report['run']['steps'])
    if not actual.same_as(expected):raise AssertionError('saved-input replay differs')
    return dict(exact=True,steps=report['run']['steps'],tensor=t.dynamics_fingerprint)


def decode_saved_clicks(path):
    """Decode exported observations without accessing tensor amplitudes or state."""
    counts=Counter();weights=Counter();classes=Counter();clock_t=[];clock_q=[]
    last_step=0;seen=set()
    with gzip.open(path,'rt',encoding='utf-8') as f:
        for line in f:
            row=json.loads(line)
            step,q,kind=row['step'],row['quotient'],row['kind']
            xyz=row['xyz'];gear=row['gear']
            if (type(step) is not int or step<1 or step<last_step or type(q) is not int or q==0
                    or type(kind) is not int or kind not in (0,1,2) or row['label']!='official'
                    or not isinstance(gear,str) or not gear or len(xyz)!=3
                    or any(type(x) is not int or x<0 for x in xyz)):
                raise ValueError('invalid official click record')
            if step!=last_step:seen.clear()
            key=(gear,tuple(xyz))
            if key in seen:raise ValueError('duplicate click record in update')
            seen.add(key);last_step=step
            ns=gear.split('.')[0];counts[ns]+=1;weights[ns]+=q;classes[str(kind)]+=1
            if gear=='cosmic.M1' and xyz==[0,0,0]:clock_t.append(step);clock_q.append(q)
    return dict(records=sum(counts.values()),by_namespace=dict(counts),
                signed_quotient_sum_by_namespace=dict(weights),by_class=dict(classes),
                clock_times=clock_t,clock_sizes=clock_q)


def run(L,steps,rng_seed,out,*,single_edge=False,stiffness=None,max_bits=256):
    if type(steps) is not int or steps<1:raise ValueError('steps must be positive')
    if type(max_bits) is not int or max_bits<1:raise ValueError('max_bits must be positive')
    if not single_edge and stiffness is not None:raise ValueError('stiffness requires single_edge')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    S,T,E,seed,prep=build(L,'jpure',rng_seed)
    construction=dict(kind='baseline',source_fingerprint=T.fingerprint)
    if single_edge:
        from ..layers.strict_edge import single_edge_realization
        from ..prepare.strict_edge import lift_seed
        realization=single_edge_realization(T,stiffness=stiffness)
        seed=lift_seed(seed,realization);T=realization.tensor;E=Engine(T,S.Q)
        construction=dict(kind='single-physical-edge experiment',
                          source_fingerprint=realization.source_fingerprint,
                          source_gears=realization.source_gears,stiffness=stiffness,
                          link_mediators=[[T.names[g],T.names[h]] for g,h in realization.link_mediators],
                          seed_lift='H.a,b,r copied once from U.a,b,r; independent thereafter',
                          equivalent_to_source_dynamics=False,
                          physical_acceptance='not accepted as a physics-preserving replacement; see physics_gate')
    initial=seed.copy();fp=T.fingerprint
    (out/'tensor.json').write_text(T.to_json())
    save_json(out/'initial_state.json.gz',seed.to_dict())
    led=CosmicLedger(CosmicView(T),seed,S.info['one']['cosmic_params']['h'],S.info['one']['cosmic_params']['c_pair'])
    counts=Counter();weights=Counter();classes=Counter();audit_rows=0;dropped=0
    clock_g=T.gear_index('cosmic.M1');times=[];sizes=[]
    snapshots_hash=state_hash(seed,np.arange(T.G))
    total_records=0;per_update=[];state=seed;peak_bits=0;stopped_for_growth=False
    with gzip.open(out/'official_clicks.jsonl.gz','wt',encoding='utf-8') as f:
        for step in range(1,steps+1):
            nxt=E.step(state)
            before=state_hash(nxt,np.arange(T.G))
            log=official_clicks(E,state,nxt,step)
            raw=E.clicks(state,nxt,step,stream='raw')
            audit_rows+=sum(l=='audit' for l in raw.label)
            dropped+=sum(not c for c,l in zip(raw.changed,raw.label) if l=='official')
            ts,qs=click_series([log],clock_g,0);times.extend(ts);sizes.extend(qs)
            # Decoder sees only declared click records, not amplitudes or hidden fields.
            for row in log.rows():
                _,xyz,g,kind,q,label=row
                name=T.names[g];ns=name.split('.')[0]
                counts[ns]+=1;weights[ns]+=q;classes[str(kind)]+=1
                f.write(json.dumps(dict(step=step,xyz=xyz,gear=name,kind=kind,quotient=q,label=label))+'\n')
            total_records+=len(log);per_update.append(len(log))
            led.update(state,nxt)
            if state_hash(nxt,np.arange(T.G))!=before:raise AssertionError('observer mutated snapshot')
            if not np.array_equal(nxt.r%2,seed.r%2):raise AssertionError('remainder parity')
            state=nxt
            bits=max(abs(int(v)).bit_length() for arr in (state.a,state.b,state.r) for v in arr.flat)
            peak_bits=max(bits,peak_bits)
            if bits>max_bits:
                stopped_for_growth=True
                break
    if T.fingerprint!=fp or state_hash(initial,np.arange(T.G))!=snapshots_hash:raise AssertionError('law/seed changed')
    completed=step
    exact=E.rewind(state,completed).same_as(seed)
    if not exact or any(led.fail.values()):raise AssertionError('rewind/ledger failure')
    save_json(out/'final_state.json.gz',state.to_dict())
    decoded=decode_saved_clicks(out/'official_clicks.jsonl.gz')
    if (decoded['records']!=total_records or decoded['by_namespace']!=dict(counts)
            or decoded['signed_quotient_sum_by_namespace']!=dict(weights)
            or decoded['by_class']!=dict(classes) or decoded['clock_times']!=times or decoded['clock_sizes']!=sizes):
        raise AssertionError('saved-event decoder disagrees with online readout')
    crossings=crossing_times(times,sizes);omega=rate_from_crossings(crossings)
    report=dict(construction=construction,tensor=tensor_report(T),scalar_oracle=scalar_crosscheck(T,S.Q),
                forward_cone=cone_check(single_edge,stiffness),
                run=dict(L=L,steps=completed,requested_steps=steps,rng_seed=rng_seed,seed_report=prep,
                         peak_state_bits=peak_bits,bit_limit=max_bits,stopped_for_growth=stopped_for_growth,
                         initial_hash=snapshots_hash,final_hash=state_hash(state,np.arange(T.G)),
                         hash_format='universe24-state-values-v2',exact_rewind=exact,observers_passive=True,
                         tensor_unchanged=True,remainder_parity=True),
                clicks=dict(saved_event_decoder_matches=True,official_records=total_records,by_namespace=dict(counts),by_class=dict(classes),
                            signed_quotient_sum_by_namespace=dict(weights),records_per_update=per_update,
                            excluded_raw_audit_rows=audit_rows,excluded_official_fixed_point_carries=dropped,
                            decoder_inputs='official click records, tensor names and computational step indices only'),
                clock=dict(gear='cosmic.M1',node=[0,0,0],events=len(times),sign_crossings=len(crossings),
                           angular_rate_per_update=omega if np.isfinite(omega) else None,
                           interpretation='diagnostic frequency; no proper-time or physical-unit calibration'),
                state_only_diagnostics=dict(cosmic_ledger_failures=led.fail,
                    carry_weight_frequencies=led.born_frequencies(seed,S.info['one']['cosmic_params']['load_sum']),
                    interpretation='uses hidden state and quotient weights; NOT click-record probabilities'),
                physics_status='local reversible dynamics and candidate observable patterns; QM/GR not established')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    report['saved_input_replay']=replay(out)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--L',type=int,default=4);p.add_argument('--steps',type=int,default=120)
    p.add_argument('--rng',type=int,default=13);p.add_argument('--out',default='runs/contract')
    p.add_argument('--replay',metavar='DIRECTORY')
    p.add_argument('--single-edge',action='store_true',help='experimental node/link mediator tensor; changes dynamics')
    p.add_argument('--stiffness',type=int,help='explicit fixed mediator coefficient, required with --single-edge')
    p.add_argument('--max-bits',type=int,default=256,help='stop and record growth above this bit length')
    args=p.parse_args()
    if not args.replay and args.single_edge and args.stiffness is None:
        p.error('--single-edge requires an explicit --stiffness')
    r=replay(args.replay) if args.replay else run(args.L,args.steps,args.rng,args.out,
        single_edge=args.single_edge,stiffness=args.stiffness,max_bits=args.max_bits)
    print(json.dumps(r,indent=2))
    if r.get('run',{}).get('stopped_for_growth'):raise SystemExit(2)
if __name__=='__main__':main()
