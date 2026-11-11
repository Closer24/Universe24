"""Joint passive audit of local communication, C2 events and structural proxies.

C2 is the third named class, not the third chronological event. No event or
structural observer is fed back into the fixed tensor or retained state.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import argparse
from collections import Counter, deque
import gzip
import hashlib
import json
import numpy as np
from universe24.core import Engine, State, Tensor
from validation.demos.communication.run_communication import build
from universe24.observe.reference_model import state_hash
from universe24.prepare.communication import message_seed
from universe24.layers.communication import LANES, RECEIVER
from validation.cosmology.recurrent_bursts import (
    structural_snapshot, ReassemblyTracker, candidate_tensor,
)


def trace(tensor, seed, steps, out=None):
    engine=Engine(tensor)
    state=seed
    rows=[i for i,n in enumerate(tensor.names) if n.startswith('ref.')]
    history=deque(maxlen=2)
    tracker=ReassemblyTracker()
    samples=[]; hashes=[]; returns=[]; totals=Counter()
    initial,signatures=structural_snapshot(state,rows)
    history.append(signatures); initial.update(update=0,C0=0,C1=0,C2=0,carrier_C2=0)
    tracker.observe(initial);samples.append(initial)
    hashes.append(state_hash(state,range(tensor.G)))
    for tick in range(1,steps+1):
        inputs=engine.inputs(state)
        following=engine.step(state)
        # Checked at every register, including transitions omitted by the
        # official nonzero-quotient/changed-triple predicate.
        delta=(following.r.astype(object)-state.r.astype(object))%6
        assert np.array_equal(delta,(2*inputs.astype(object))%6)
        log=engine.clicks(state,following,tick).select('official')
        assert all(int(kind)==int(inputs[g,n])%3 for kind,g,n in zip(log.kind,log.gear,log.node))
        counts=Counter(map(int,log.kind));totals.update(counts)
        row,signatures=structural_snapshot(following,rows,tuple(history))
        history.append(signatures)
        row.update(update=tick,**{f'C{k}':counts[k] for k in range(3)},
                   carrier_C2=sum(int(k)==2 and tensor.names[int(g)].startswith('comm.')
                                  for g,k in zip(log.gear,log.kind)))
        tracker.observe(row);samples.append(row)
        hashes.append(state_hash(following,range(tensor.G)))
        if following.same_as(seed):returns.append(tick)
        state=following
    maximum=max(r['site_pattern_types'] for r in samples)
    first_max=next(r['update'] for r in samples if r['site_pattern_types']==maximum)
    result=dict(gears=tensor.G,steps=steps,L=seed.L,tensor_fingerprint=tensor.fingerprint,
                initial_hash=hashes[0],final_hash=hashes[-1],state_hashes=hashes,
                counts={f'C{k}':totals[k] for k in range(3)},
                first_C2_update=next((r['update'] for r in samples if r['C2']),None),
                carrier_C2=sum(r['carrier_C2'] for r in samples),
                maximum_site_pattern_types=maximum,first_site_maximum_update=first_max,
                C2_after_first_site_maximum=sum(r['C2'] for r in samples if r['update']>first_max),
                reference_reassemblies=tracker.events,full_state_returns=returns,
                exact_rewind=engine.rewind(state,steps).same_as(seed),
                observation_free_replay_matches=engine.run(seed,steps).same_as(state),samples=samples)
    assert result['exact_rewind'] and result['observation_free_replay_matches']
    if out:
        out=Path(out);out.mkdir(parents=True,exist_ok=True)
        (out/'tensor.json').write_text(tensor.to_json()+'\n')
        for name,snapshot in (('initial',seed),('final',state)):
            with gzip.open(out/(name+'.json.gz'),'wt') as f:json.dump(snapshot.to_dict(),f)
        (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def communication_case(amplitude=3, connected=True, L=5):
    _,base,_,empty,_=build(L,'none')
    tensor=base if connected else candidate_tensor(base,'disconnected')
    seed=message_seed(empty,tensor,[(lane,(L//2,)*3,amplitude) for lane in LANES])
    return tensor,seed


def c2_periodic_case(L=5):
    # u=2, (a,b,r)=(0,0,2) -> (0,1,0) -> (1,0,4) -> (0,0,2).
    # The first and third transitions have official C2; the middle has q=0.
    tensor=Tensor(['ref.uniform'],[('ref.uniform',2,())],strict_support=True)
    seed=Engine(tensor).vacuum(L,[2])
    return tensor,seed


def event_map(engine,before,after,tick,kind=None):
    log=engine.clicks(before,after,tick).select('official')
    return {(int(g),int(n)):(int(k),int(q)) for g,n,k,q in
            zip(log.gear,log.node,log.kind,log.quotient) if kind is None or int(k)==kind}


def event_cone(tensor, seed, perturbed, steps=4):
    """Compare complete preparations, including any spatial old-a footprint."""
    if seed.L!=perturbed.L or seed.G!=perturbed.G:raise ValueError('same lattice and gears required')
    changed=np.any((seed.a!=perturbed.a)|(seed.b!=perturbed.b)|(seed.r!=perturbed.r),axis=0)
    origins=list(map(int,np.flatnonzero(changed)))
    if not len(origins):raise ValueError('a nonempty complete-state perturbation is required')
    lat=seed.lattice;L=seed.L
    distance=[min(sum(min(abs(a-b),L-abs(a-b)) for a,b in zip(lat.coords(n),lat.coords(o)))
                  for o in origins) for n in range(seed.N)]
    engine=Engine(tensor);left,right=seed,perturbed
    samples=[];c2_points=[]
    for tick in range(1,steps+1):
        a,b=engine.step(left),engine.step(right)
        changed_nodes=np.flatnonzero(np.any((a.a!=b.a)|(a.b!=b.b)|(a.r!=b.r),axis=0))
        event_nodes=[];c2_nodes=[]
        for kind,target in ((None,event_nodes),(2,c2_nodes)):
            lmap=event_map(engine,left,a,tick,kind);rmap=event_map(engine,right,b,tick,kind)
            target.extend(sorted({key[1] for key in lmap.keys()|rmap.keys() if lmap.get(key)!=rmap.get(key)}))
        outside=lambda nodes:sum(distance[n]>tick for n in nodes)
        samples.append(dict(update=tick,changed_state_sites=len(changed_nodes),
                            changed_event_sites=len(event_nodes),changed_C2_sites=len(c2_nodes),
                            state_outside_cone=outside(changed_nodes),events_outside_cone=outside(event_nodes),
                            C2_outside_cone=outside(c2_nodes),
                            maximum_C2_distance=max((distance[n] for n in c2_nodes),default=None)))
        assert not outside(changed_nodes) and not outside(event_nodes) and not outside(c2_nodes)
        c2_points.extend({'update':tick,'xyz':list(map(int,lat.coords(n))),'distance':int(distance[n])}
                         for n in c2_nodes)
        left,right=a,b
    exact=engine.rewind(left,steps).same_as(seed) and engine.rewind(right,steps).same_as(perturbed)
    assert exact
    return dict(L=L,steps=steps,initial_changed_sites=[list(map(int,lat.coords(n))) for n in origins],
                tensor_fingerprint=tensor.fingerprint,samples=samples,C2_points=c2_points,
                exact_rewind=exact,scope='Periodic Manhattan distance to the full initial perturbation; computational causal bound, not an Einstein null metric.')


def reception_control():
    tensor,seed=communication_case(3)
    _,quiet=communication_case(0)
    e=Engine(tensor);on=e.step(seed);off=e.step(quiet)
    g=tensor.gear_index(RECEIVER)
    du=e.inputs(seed)[g].astype(object)-e.inputs(quiet)[g].astype(object)
    dq=(on.b[g].astype(object)+seed.a[g])-(off.b[g].astype(object)+quiet.a[g])
    assert all(int(x)%3==0 for x in du)
    assert np.array_equal(on.r[g],off.r[g]) and np.array_equal(du,3*dq)
    return dict(receiver=RECEIVER,changed_input_sites=int(np.count_nonzero(du)),
                input_changes=sorted(set(map(int,du))),quotient_changes=sorted(set(map(int,dq))),
                receiver_remainders_identical=True,
                identity='u -> u+3M implies ell -> ell+M and unchanged next r for a fixed old receiver triple; official event presence may still change.')


def run(out,main_confirmation=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    cases={}
    _,ref,_,seed,_=build(5,'pulse',model='reference')
    cases['main_reference']=trace(ref,seed,80,out/'main_reference')
    for name,amplitude,connected,steps in (
        ('communication',3,True,80),('no_messages',0,True,80),('disconnected',3,False,80),
        ('payload_one',1,True,20),('payload_nine',9,True,20)):
        tensor,seed=communication_case(amplitude,connected)
        cases[name]=trace(tensor,seed,steps,out/name)
        cases[name]['preparation']={'payload':amplitude,'connected':connected}
    tensor,seed=c2_periodic_case()
    cases['periodic_C2']=trace(tensor,seed,12,out/'periodic_C2')
    _,ref,_,seed,_=build(9,'none',model='reference')
    changed=seed.copy();changed.b[0,seed.lattice.index(4,4,4)]+=17
    cones={'single_reference_site':event_cone(ref,seed,changed)}
    tensor,pulse=communication_case(3,L=9);_,quiet=communication_case(0,L=9)
    cones['prepared_messages']=event_cone(tensor,quiet,pulse)
    main=None
    if main_confirmation:
        main=json.loads(Path(main_confirmation).read_text())
        current=cases['main_reference']
        for key in ('tensor_fingerprint','initial_hash','state_hashes','exact_rewind'):
            assert current[key]==main[key],f'main replay mismatch: {key}'
    source_names=('validation/cosmology/click_cone_audit.py','validation/cosmology/recurrent_bursts.py',
                  'universe24/core/engine.py','universe24/core/tensor.py','universe24/layers/communication.py',
                  'universe24/prepare/communication.py')
    result=dict(main_commit='8d3f15074d3f9a9344ec587dbab0222243505187',
                research_base='97b01b07c0f666975158f3a1273d4240516dd4ce',
                main_snapshot_confirmation=main,cases=cases,cones=cones,
                direct_reception_control=reception_control(),
                source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_names},
                conclusions={'third_named_class':'C2','C2_is_necessarily_structural_growth':False,
                             'C2_has_a_separate_forward_cone':False,
                             'communication_changes_future_C2_events':True,
                             'recurrent_bursts_with_growth_demonstrated':False},
                interpretation='Measured controls plus exact modular identities; no C2 callback, global scheduler or physical-light-cone claim.')
    (out/'SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('runs/click-cone'))
    parser.add_argument('--main-confirmation',type=Path)
    args=parser.parse_args();result=run(args.out,args.main_confirmation)
    print(json.dumps({name:{k:case[k] for k in ('counts','first_C2_update','maximum_site_pattern_types',
                        'first_site_maximum_update','C2_after_first_site_maximum','exact_rewind')}
                      for name,case in result['cases'].items()},indent=2))


if __name__=='__main__':main()
