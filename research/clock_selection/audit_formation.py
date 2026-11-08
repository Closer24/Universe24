"""Independent full-state audit of initially isolated clock formation."""
from __future__ import annotations
import argparse,itertools,json,time
from functools import lru_cache
from pathlib import Path
from research.clock_selection.audit import (ROOT,Snapshot,load,file_digest,canonical,all_events,
    input_terms,DIRECTIONS,audit_record,source_control)
from research.clock_selection.audit_structure import external
from research.component_review.audit import advance

PROTOCOL_SHA='147a40c82d584990a822f4904c85f543e23f29fdf9ceba0b01870811a4383917'

def add(a,b):return tuple(x+y for x,y in zip(a,b))

@lru_cache(None)
def template(phase):
    origin=(4,4,4);initial=Snapshot(9,(0,0,2),{(*origin,0):(1,1,0),(*origin,14):(-1,-1,4)})
    states=[initial]
    for _ in range(4):states.append(advance(states[-1],(1,1,1)))
    assert states[4]==initial
    nodes={(0,0,0),*DIRECTIONS}
    assert all(tuple(a[j]-4 for j in range(3)) in nodes for s in states for a in s.cells)
    return {(*n,g):states[phase].at((*add(origin,n),g)) for n in nodes for g in range(48)}

def geometry(case):
    c=case['side']//2;d=case['distance'];A=(c-d//2,c,c);B=add(A,(d,0,0))
    segment={add(A,(x,0,0)) for x in range(d+1)}
    target=segment|{add(n,delta) for n in segment for delta in DIRECTIONS}
    return A,B,target

def initial(case):
    A,B,_=geometry(case);cells={}
    for origin,sign,enabled in zip((A,B),(1,case['second_sign']),case['control']):
        value=sign if enabled=='1' else 0
        cells[(*origin,0)]=(value,value,0);cells[(*origin,14)]=(-value,-value,4)
    return Snapshot(case['side'],(0,0,2),cells)

def matches(state,origin,phase):
    return all(state.at((*add(origin,a[:3]),a[3]))==value for a,value in template(phase).items())

def observe(case,states):
    A,B,target=geometry(case);endpoint={A,B};bridge={add(A,(x,0,0)) for x in range(1,case['distance'])};halo=target-endpoint-bridge
    addresses=[(*n,g) for n in sorted(target) for g in range(48)]
    trace=[[list(s.at(a)) for a in addresses] for s in states]
    periods=[p for p in range(1,17) if all(trace[t]==trace[t+p] for t in range(64,97-p))]
    boundary=[dict(update=t+1,terms=external(s,target)) for t,s in enumerate(states[:-1])]
    bridge_trace=[[[*a,*v] for a,v in sorted(s.cells.items()) if a[:3] in bridge and any(v[:2])] for s in states]
    identities={name:[dict(state=t,matches=[phase for phase in range(4) if matches(s,origin,phase)])
        for t,s in enumerate(states)] for name,origin in (('A',A),('B',B))}
    cores={name:[[list(s.at((*origin,g))[:2]) for g in range(48)] for s in states] for name,origin in (('A',A),('B',B))}
    expected={name:all(row['matches']==[(phase+row['state'])%4] for row in identities[name])
        for name,phase in (('A',0),('B',0 if case['second_sign']==1 else 2))}
    events=[];counts={name:{str(k):0 for k in range(3)} for name in ('endpoint','bridge','halo','exterior')}
    for event in all_events(states)[0]:
        t=event['step'];a=tuple(event['address']);node=a[:3]
        label='endpoint' if node in endpoint else 'bridge' if node in bridge else 'halo' if node in halo else 'exterior'
        sums,terms=input_terms(states[t-1],[a],(1,1,1))
        events.append(dict(step=t,address=list(a),kind=event['kind'],ell=int(event['quotient']),region=label,
            six_terms=[dict(source=v['address'],term=v['weight']*int(v['b'])) for v in terms[0]],u=sums[0]))
        counts[label][str(event['kind'])]+=1
    return dict(region_addresses=[list(a) for a in addresses],region_trace=trace,boundary_inputs=boundary,hold_periods=periods,
        hold_individually_isolated=all(not row['terms'] for row in boundary[64:96]),
        hold_nonzero=any(any(v[:2]) for f in trace[64:97] for v in f),bridge_nodes=[list(n) for n in sorted(bridge)],bridge_trace=bridge_trace,
        first_bridge_counter_activity=next((t for t,values in enumerate(bridge_trace) if values),None),
        recurrent_bridge_periods=[p for p in periods if any(bridge_trace[64:64+p])],
        complete_initial_identities={name:identities[name][0]['matches'] for name in identities},identity_traces=identities,
        expected_complete_identity_all_states=expected,core_counter_traces=cores,
        first_full_state_return=next((t for t,s in enumerate(states[1:],1) if s==states[0]),None),
        whole_state_period4_all_states=all(states[t]==states[t+4] for t in range(len(states)-4)),all_C=events,C_counts=counts,
        active_boundary_hit=any(any(v in (0,s.side-1) for v in a[:3]) for s in states for a,x in s.cells.items() if any(x[:2])),
        max_sparse_channels=max(len(s.cells) for s in states))

def assess(rows):
    by={r['case']['control']:r for r in rows};obs={m:r['out'] for m,r in by.items()};seeds={m:r['states'][0] for m,r in by.items()}
    case=rows[0]['case'];A,B,_=geometry(case)
    for on,off in (('10','00'),('11','01')):source_control(seeds[on],seeds[off],[(*A,0),(*A,14)])
    for on,off in (('01','00'),('11','10')):source_control(seeds[on],seeds[off],[(*B,0),(*B,14)])
    addresses=set().union(*(s.cells for s in seeds.values()))
    remainders=all(len({s.at(a)[2] for s in seeds.values()})==1 for a in addresses)
    masks=all(seeds['11'].at(a)[j]==seeds['10'].at(a)[j]+seeds['01'].at(a)[j]-seeds['00'].at(a)[j] for a in addresses for j in (0,1))
    identities=bool(obs['11']['complete_initial_identities']['A'] and obs['11']['complete_initial_identities']['B'])
    single=obs['10']['expected_complete_identity_all_states']['A'] and obs['01']['expected_complete_identity_all_states']['B']
    inactive=all(not any(any(v) for frame in obs[m]['core_counter_traces'][name] for v in frame) for m,name in (('10','B'),('01','A'),('00','A'),('00','B')))
    quiet=all(not any(obs[m]['bridge_trace']) for m in ('00','10','01'))
    eligible=identities and remainders and masks and single and inactive and quiet
    causal={name:any(obs['11']['core_counter_traces'][name][t]!=obs[m]['core_counter_traces'][name][t] for t in range(64,97)) for name,m in (('A','10'),('B','01'))}
    joint=obs['11'];first=joint['first_bridge_counter_activity'];new_bridge=first is not None and first>0 and quiet
    formed=bool(eligible and joint['hold_periods'] and joint['hold_nonzero'] and joint['hold_individually_isolated'] and new_bridge and joint['recurrent_bridge_periods'] and all(causal.values()))
    negative=case['distance']>=3 or case['second_sign']==-1
    return dict(geometry={k:v for k,v in case.items() if k!='control'},both_initial_complete_identities=identities,
        matched_remainders=remainders,counter_masks_commute=masks,singleton_complete_identities_preserved=single,
        inactive_core_controls_quiet=inactive,all_control_bridge_traces_quiet=quiet,eligible=eligible,
        joint_hold_periods=joint['hold_periods'],joint_individually_isolated=joint['hold_individually_isolated'],
        new_bridge=new_bridge,new_recurrent_bridge=bool(new_bridge and joint['recurrent_bridge_periods']),late_core_causal_difference=causal,
        finite_stationary_composite_formed=formed,predicted_negative=negative,
        exact_negative_control_agrees=bool(joint['whole_state_period4_all_states'] and not any(joint['bridge_trace'])) if negative else None,
        physical_binding_or_force_established=False)

def planned():
    return [dict(id=f'formation-L{L}-d{d}-s{s:+d}',side=L,distance=d,second_sign=s,control=m)
        for L,d,s,m in itertools.product((225,257),(2,3,4),(1,-1),('00','10','01','11'))]

def audit(study,output,budget=600):
    study,output=Path(study),Path(output);assert not output.exists();start=time.process_time()
    report=dict(passed=False,auditor_sha256=file_digest(__file__),protocol_sha256=PROTOCOL_SHA,records=[],groups=[],failure=None)
    try:
        p,result,registration=(load(study/f) for f in ('protocol.json','result.json','registration.json'))
        assert file_digest(study/'protocol.json')==registration['protocol_sha256']==PROTOCOL_SHA
        assert result['status']=='completed' and result['completed_cases']==len(result['cases'])==48
        assert registration['initial_preflight']['prepared_cases']==48
        for path,sha in registration['source_sha256'].items():assert file_digest(ROOT/path)==sha,path
        assert file_digest(study/'executed_structure_formation.py')==registration['source_sha256']['research/clock_selection/structure_formation.py']
        grouped=[]
        for case,entry in zip(planned(),result['cases']):
            path=study/entry['record'];assert file_digest(path)==entry['sha256'];record=load(path);assert record['case']==case
            integrity,states=audit_record({k:v for k,v in record.items() if k!='observations'},expected_initial=initial(case),deadline=start+budget)
            out=observe(case,states);assert out==record['observations'],[k for k in out if out[k]!=record['observations'].get(k)]
            assert not out['active_boundary_hit'] and out['max_sparse_channels']<=20000
            assert all(min(q,case['side']-1-q)>96 for a,v in states[0].cells.items() if any(v[:2]) for q in a[:3])
            report['records'].append(dict(case=case,integrity=integrity,first_bridge_counter_activity=out['first_bridge_counter_activity'],
                hold_periods=out['hold_periods'],recurrent_bridge_periods=out['recurrent_bridge_periods'],C_counts=out['C_counts']))
            grouped.append(dict(case=case,states=states,out=out))
            if len(grouped)==4:
                group=assess(grouped);assert result['groups'][len(report['groups'])]==group
                report['groups'].append(group);grouped=[]
                print(canonical({'audited_formation_records':len(report['records']),'registered':48}),flush=True)
        assert not grouped
        report.update(passed=True,full_states=48*97,transitions=48*96,full_rewinds=48,
            finite_formation_groups=sum(g['finite_stationary_composite_formed'] for g in report['groups']),
            sources_unchanged=True,scope='Finite formation conjunction as frozen; complete singleton controls and all raw C retained.')
    except Exception as exc:report['failure']=f'{type(exc).__name__}: {exc}'
    report['cpu_seconds']=time.process_time()-start;output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    report=audit(args.study,args.output);print(canonical({k:report[k] for k in ('passed','failure','cpu_seconds')}))
    raise SystemExit(0 if report['passed'] else 1)
