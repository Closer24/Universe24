"""Independent matrix-derived structure audit, including the observer defect."""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path
import time
from research.clock_selection.audit import (ROOT, Snapshot, canonical, file_digest, load,
    declared_initial, coupling, DIRECTIONS, matches as packet_matches, input_terms,
    audit_record, all_events, native_digest)

PROTOCOL_SHA = '49a6ae786de1b4afd67dfae59c8cfaad55d5ed293e8ca1b824b0226ab135e018'
PAIR = ((-1,-1,0),(-1,0,4),(0,1,4),(1,1,0),(1,-1,2))
SINGLE = ((-1,-1,0),(-1,1,0),(1,1,0),(1,-1,0))

def add(a,b): return tuple(x+y for x,y in zip(a,b))

@lru_cache(None)
def template(kind,phase):
    centers = ((0,0,0),(0,0,1)) if kind=='pair' else ((0,0,0),)
    cycle, halos = (PAIR,(2,0,0,2,4)) if kind=='pair' else (SINGLE,(2,0,2,4))
    nodes = set(centers)
    for center in centers: nodes.update(add(center,d) for d in DIRECTIONS)
    cells = {(*node,g):(0,0,2) for node in nodes for g in range(48)}
    a,b,r = cycle[phase]
    matrix = coupling((1,1,1))
    for center in centers:
        cells[(*center,2)] = (a,b,r)
        cells[(*center,24)] = (-a,-b,4-r)
        for direction,delta in enumerate(DIRECTIONS):
            target = add(center,delta)
            if target in centers: continue
            for donor, remainder in ((2,halos[phase]),(24,4-halos[phase])):
                receivers = [g for g in range(48) if matrix.ports[direction^1][g]==donor]
                assert len(receivers)==1
                cells[(*target,receivers[0])] = (0,0,remainder)
    return tuple(sorted(cells.items()))

def expected_initial(case):
    L=case['side']; c=L//2; x=c-16-case['delay']; mask=case['control']
    seed=declared_initial({'board':{'side':L},'components':[
        {'name':'guide','recipe':'GuideSegment','at':[0,c,c],
         'params':{'start':0,'stop':L-1,'sockets':list(range(x,x+4)),'remainder_pair':[0,4]}},
        {'name':'packet','recipe':'GuidedPacketSource','at':[x,c,c],
         'params':{'present':mask[0]=='1'}}]})
    if case['kind']=='pristine': return seed
    cells=dict(seed.cells)
    for address,value in template('pair',case['phase']):
        target=(*add(address[:3],(c,c+1,c)),address[3])
        if mask[1]=='0': value=(0,0,value[2])
        if target in cells: assert cells[target]==value, ('Initial overlap',target)
        cells[target]=value
    return Snapshot(L,(0,0,2),cells)

def object_matches(state,origin,kind,phase):
    cycle=PAIR if kind=='pair' else SINGLE
    if state.at((*origin,2))!=cycle[phase]: return False
    return all(state.at((*add(a[:3],origin),a[3]))==v for a,v in template(kind,phase))

def external(state,nodes):
    matrix=coupling((1,1,1)); output=[]
    for source,value in sorted(state.cells.items()):
        if not value[1] or source[:3] in nodes: continue
        for direction,delta in enumerate(DIRECTIONS):
            target=tuple((source[j]+delta[j])%state.side for j in range(3))
            if target not in nodes: continue
            recipients=[g for g in range(48) if matrix.ports[direction^1][g]==source[3]]
            assert len(recipients)==1
            g=recipients[0]
            output.append({'source':list(source),'target':[*target,g],
                'term':matrix.weights[direction^1][g]*value[1]})
    return output

def observe(case,states):
    c=case['side']//2; origin=(c,c+1,c); start,end=32,48
    addresses=[(*add(a[:3],origin),a[3]) for a,v in template('pair',0)]
    nodes={a[:3] for a in addresses}; core={origin,add(origin,(0,0,1))}; skin=nodes-core
    trace=[[list(s.at(a)) for a in addresses] for s in states]
    boundary=[{'update':t+1,'terms':external(s,nodes)} for t,s in enumerate(states[:-1])]
    periods=[q for q in range(1,9) if all(trace[t]==trace[t+q] for t in range(start,end-q+1))]
    origins=[add(origin,d) for d in itertools.product(range(-4,5),repeat=3)]
    objects=[{'state':t,'matches':[{'origin':list(o),'phase':q} for o in origins for q in range(5)
              if object_matches(s,o,'pair',q)]} for t,s in enumerate(states)]
    unique=all(len(row['matches'])==1 for row in objects)
    continuous=bool(unique and all(objects[t+1]['matches'][0]['phase']==(objects[t]['matches'][0]['phase']+1)%5
        and sum(abs(a-b) for a,b in zip(objects[t+1]['matches'][0]['origin'],objects[t]['matches'][0]['origin']))<=1
        for t in range(len(objects)-1)))
    products=[]
    for o in origins:
        for q in range(4):
            if not all(object_matches(states[t],o,'single',(q+t-start)%4) for t in range(start,end+1)): continue
            product_nodes={add(a[:3],o) for a,v in template('single',0)}
            if all(not external(states[t],product_nodes) for t in range(start,end)):
                products.append({'origin':list(o),'phase_at_start':q})
    product_pairs=[[a,b] for a,b in itertools.combinations(products,2)
        if sum(abs(x-y) for x,y in zip(a['origin'],b['origin']))>=3]
    incoming=[{'step':t,'matches':packet_matches(states[t],c-16-case['delay']+t,c,c)}
        for t in range(case['delay']+4,case['delay']+8)]
    events=[]; counts={r:{str(k):0 for k in range(3)} for r in ('core','skin','exterior')}
    for event in all_events(states)[0]:
        t=event['step']; a=tuple(event['address']); region='core' if a[:3] in core else 'skin' if a[:3] in skin else 'exterior'
        sums,terms=input_terms(states[t-1],[a],(1,1,1))
        events.append({'step':t,'address':list(a),'kind':event['kind'],'ell':int(event['quotient']),
            'region':region,'six_terms':[{'source':v['address'],'term':v['weight']*int(v['b'])} for v in terms[0]],'u':sums[0]})
        counts[region][str(event['kind'])]+=1
    event_counts=Counter((e['step'],e['kind']) for e in events)
    coexist=[]
    for lag in range(5):
        class_pairs=[]
        for a,b in itertools.product(range(3),repeat=2):
            count=sum(event_counts[t,a]*event_counts[t+lag,b]-(event_counts[t,a] if lag==0 and a==b else 0)
                for t in range(1,len(states)))
            class_pairs.append([a,b,count])
        coexist.append({'lag':lag,'ordered_distinct_event_pairs':class_pairs})
    margin=min((min(v,case['side']-1-v) for a,x in states[0].cells.items() if any(x[:2]) for v in a[:3]),default=case['side'])
    return {'region_addresses':[list(a) for a in addresses],'core_nodes':[list(a) for a in sorted(core)],
        'skin_nodes':[list(a) for a in sorted(skin)],'region_trace':trace,'boundary_inputs':boundary,
        'hold_periods':periods,'hold_nonzero':any(any(v[:2]) for f in trace[start:end+1] for v in f),
        'hold_individually_isolated':all(not boundary[t]['terms'] for t in range(start,end)),
        'incoming':incoming,'incoming_valid':all(v['matches'] for v in incoming),
        'canonical_object_trace':objects,'unique_continuous_object':continuous,
        'moving_composite':bool(continuous and any(v['matches'][0]['origin']!=objects[0]['matches'][0]['origin'] for v in objects)),
        'isolated_product_templates':products,'separated_product_pairs':product_pairs,
        'separated_products_without_parent':bool(product_pairs and all(not v['matches'] for v in objects[start:end+1])),
        'all_C':events,'C_counts':counts,'C_class_lag_coexistence':coexist,
        'initial_active_boundary_margin':margin,
        'active_boundary_hit':any(any(v in (0,case['side']-1) for v in a[:3]) for s in states for a,x in s.cells.items() if any(x[:2]))}

def assess(rows):
    by={r['case']['control']:r for r in rows}; initial={m:r['states'][0] for m,r in by.items()}
    addresses=set().union(*(s.cells for s in initial.values()))
    remainder=all(len({s.at(a)[2] for s in initial.values()})==1 for a in addresses)
    masks=all(initial['11'].at(a)[j]==initial['10'].at(a)[j]+initial['01'].at(a)[j]-initial['00'].at(a)[j]
        for a in addresses for j in (0,1))
    validity={m:(r['out']['incoming_valid'] if m[0]=='1' else not any(v['matches'] for v in r['out']['incoming'])) for m,r in by.items()}
    eligible=remainder and masks and all(validity.values())
    clock,on,packet,null=(by[m]['out'] for m in ('01','11','10','00'))
    def retained(out): return bool(out['hold_periods'] and out['hold_nonzero'] and out['hold_individually_isolated'])
    return {'geometry':{k:v for k,v in rows[0]['case'].items() if k!='control'},
        'matched_remainders':remainder,'counter_masks_commute':masks,'incoming_controls':validity,
        'eligible_source_comparison':eligible,
        'clock_only_period5':all(clock['region_trace'][t]==clock['region_trace'][t+5] for t in range(44)),
        'clock_only_complete_template':all(len(v['matches'])==1 and v['matches'][0]['phase']==(by['01']['case']['phase']+v['state'])%5 for v in clock['canonical_object_trace']),
        'signal_created_recurrent_region':bool(eligible and retained(packet) and not any(any(v[:2]) for f in null['region_trace'] for v in f)),
        'signal_reconfigured_recurrent_region':bool(eligible and retained(on) and on['region_trace'][32:49]!=clock['region_trace'][32:49]),
        'joint_canonical_cluster_retained_in_hold':all(v['matches'] for v in on['canonical_object_trace'][32:49]),
        'source_induced_separated_clock_products':bool(eligible and on['separated_products_without_parent'] and not clock['separated_products_without_parent']),
        'motion_attraction_repulsion':'not_tested_no_two_initial_moving_objects','physical_binding_or_dissociation_established':False}

def planned():
    out=[{'id':f'pristine-L{L}-d{d}','side':L,'phase':1,'delay':d,'kind':'pristine','control':'10'} for L,d in itertools.product((161,193),(4,7))]
    out.extend({'id':f'cluster-L{L}-p{p}-d{d}','side':L,'phase':p,'delay':d,'kind':'encounter','control':m}
        for L,p,d,m in itertools.product((161,193),(1,2),(4,7),('00','10','01','11')))
    return out

def audit(study,output,budget=600):
    study,output=Path(study),Path(output); assert not output.exists()
    start=time.process_time(); report={'passed':False,'records':[],'groups':[],'observer_disagreements':[],
        'auditor_sha256':file_digest(__file__),'protocol_sha256':PROTOCOL_SHA,'failure':None}
    try:
        p,result,registration=(load(study/f) for f in ('protocol.json','result.json','registration.json'))
        assert file_digest(study/'protocol.json')==registration['protocol_sha256']==PROTOCOL_SHA
        assert result['completed_cases']==36 and len(result['cases'])==36
        for path,sha in registration['source_sha256'].items():
            if path!='research/clock_selection/structure.py': assert file_digest(ROOT/path)==sha, path
        collected=[]
        for i,(case,entry) in enumerate(zip(planned(),result['cases'])):
            assert time.process_time()-start<budget
            path=study/entry['record']; assert file_digest(path)==entry['sha256']
            record=load(path); assert record['case']==case
            integrity,states=audit_record({k:v for k,v in record.items() if k!='observations'},expected_initial=expected_initial(case),deadline=start+budget)
            out=observe(case,states)
            differing=[k for k in out if out[k]!=record['observations'].get(k)]
            assert set(differing)<= {'separated_product_pairs','separated_products_without_parent'}, differing
            if differing: report['observer_disagreements'].append({'id':entry['id'],'fields':differing,
                'correct_separated_product_pairs':out['separated_product_pairs'],
                'correct_separated_products_without_parent':out['separated_products_without_parent']})
            assert out['initial_active_boundary_margin']>48 and not out['active_boundary_hit']
            report['records'].append({'id':entry['id'],'case':case,'integrity':integrity,
                'hold_periods':out['hold_periods'],'products':out['isolated_product_templates'],
                'separated_product_pairs':out['separated_product_pairs'],'C_counts':out['C_counts'],
                'initial_state_sha256':native_digest(states[0]),'final_state_sha256':native_digest(states[-1])})
            if case['kind']=='pristine': assert record['assessment']=={'pristine':True,'incoming_valid':out['incoming_valid']}
            else:
                collected.append({'case':case,'states':states,'out':out,'saved':record['assessment']})
                if len(collected)==4:
                    group=assess(collected)
                    for row in collected:
                        assert {k:v for k,v in group.items() if k!='source_induced_separated_clock_products'}=={k:v for k,v in row['saved'].items() if k!='source_induced_separated_clock_products'}
                    report['groups'].append(group); collected=[]
            print(canonical({'audited_structure_records':i+1,'registered':36}),flush=True)
        assert not collected
        report.update(passed=True,full_states=sum(r['integrity']['states'] for r in report['records']),
            transitions=sum(r['integrity']['forward_transitions'] for r in report['records']),full_rewinds=36,
            corrected_separated_product_groups=sum(g['source_induced_separated_clock_products'] for g in report['groups']),
            scope='Full native dynamics valid; original observer product fields are invalid. Independent fixed-protocol reassessment retained here.')
    except Exception as exc: report['failure']=f'{type(exc).__name__}: {exc}'
    report['cpu_seconds']=time.process_time()-start
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    report=audit(args.study,args.output);print(canonical({k:report[k] for k in ('passed','failure','cpu_seconds')}))
    raise SystemExit(0 if report['passed'] else 1)
