"""Independent replay and full-region terminal-memory checks for the frozen chain."""
import argparse,json,time
from pathlib import Path
from research.clock_selection.audit import DIRECTIONS,coupling,all_events,audit_record,load,file_digest,ROOT,canonical,matches
from research.clock_selection.audit_route_clock import terms
from research.clock_selection.audit_carrier_memory_preflight import initial,region,planned,preparation,PHASES
SHA='6309eea6e455a533258d235e884d835bb0759302f455d98659e77b035721c1ce'


def observe(case,states):
 c=case['side']//2;cp=coupling((1,1,1));inverse=[{g:h for h,g in enumerate(row)} for row in cp.ports];events=[]
 for event in all_events(states)[0]:
  t=event['step'];six=terms(states[t-1],tuple(event['address']));events.append(dict(step=t,address=event['address'],kind=event['kind'],ell=int(event['quotient']),six_terms=six,u=sum(x['term'] for x in six)))
 clocks={}
 for name,dx in (('controller',0),('receiver',20)):
  addresses=sorted(region(case,name));nodes={a[:3] for a in addresses};ca=(c+dx,c+1,c,2);trace=[[list(s.at(a)) for a in addresses] for s in states];centers=[list(s.at(ca)) for s in states];inputs=[];boundary=[]
  for t,(old,new) in enumerate(zip(states,states[1:]),1):
   six=terms(old,ca);inputs.append(dict(update=t,six_terms=six,u=sum(x['term'] for x in six),ell=new.at(ca)[1]+old.at(ca)[0]));ext=[]
   for a,v in old.cells.items():
    if not v[1] or a[:3] in nodes:continue
    for d,delta in enumerate(DIRECTIONS):
     n=tuple((a[j]+delta[j])%old.side for j in range(3))
     if n in nodes:
      h=inverse[d^1][a[3]];ext.append(dict(source=list(a),target=[*n,h],term=cp.weights[d^1][h]*v[1]))
   boundary.append(dict(update=t,terms=ext))
  windows={'controller_hold':(32,40)} if name=='controller' else {'pre_late':(52,60),'terminal':(96,112)};holds={}
  for label,(lo,hi) in windows.items():
   predicates=dict(full336_period4=all(trace[t]==trace[t+4] for t in range(lo,hi-3)),only_center_counters=all(not any(v[:2]) for row in trace[lo:hi+1] for a,v in zip(addresses,row) if a!=ca),unit_center_r0=all(a*a+b*b==1 and r==0 for a,b,r in centers[lo:hi+1]),exact_quarter_turn=all(centers[t+1][:2]==[centers[t][1],-centers[t][0]] for t in range(lo,hi)),zero_center_input_quotient=all(x['u']==x['ell']==0 for x in inputs[lo:hi]),zero_individual_external_terms=all(not x['terms'] for x in boundary[lo:hi]));holds[label]=dict(states=[lo,hi],predicates=predicates,passed=all(predicates.values()))
  clocks[name]=dict(region_addresses=[list(a) for a in addresses],region_trace=trace,center_trace=centers,center_inputs=inputs,external_inputs=boundary,complete_canonical_orbit=all(all(s.at(a)==v for a,v in region(case,name,t).items()) for t,s in enumerate(states)),holds=holds)
 incoming={}
 for name,offset,delay,bit in (('writer',18,0,0),('probe',56,38,1)):
  frames=[dict(time=delay+k,origin=c-offset+delay+k,match=matches(states[delay+k],c-offset+delay+k,c,c,1)) for k in range(4,8)];present=case['control'][bit]=='1';incoming[name]=dict(frames=frames,expected_present=present,passed=all(x['match']==present for x in frames))
 epochs={}
 for name,delay in (('early',0),('late',38)):
  frames=[dict(time=28+delay+k,origin=c+10+k,match=matches(states[28+delay+k],c+10+k,c,c,1)) for k in range(4)];raw=[{k:e[k] for k in ('step','kind','ell')} for e in events if e['address']==[c+12,c,c,0] and 27+delay<=e['step']<=34+delay];expected=[dict(step=27+delay,kind=2,ell=-1),dict(step=31+delay,kind=1,ell=1)];present=case['control'][0]=='1' if name=='early' else case['control']=='11';exact=all(x['match'] for x in frames);signature=raw==expected
  epochs[name]=dict(carrier_frames=frames,raw_C=raw,expected_C=expected,exact_carrier=exact,exact_C_signature=signature,carrier_plus_C=exact and signature,predicted_present=present,truth_table_pass=all(x['match']==present for x in frames) and raw==(expected if present else []))
 return dict(clocks=clocks,incoming=incoming,epochs=epochs,all_C=events,C_counts={str(k):sum(e['kind']==k for e in events) for k in range(3)},whole_board_period4=all(states[t]==states[t+4] for t in range(117)),active_boundary_hit=any(any(q in (0,case['side']-1) for q in a[:3]) for s in states for a,v in s.cells.items() if any(v[:2])),max_sparse_channels=max(len(s.cells) for s in states))


def assess(rows):
 by={r['case']['control']:r['observations'] for r in rows};case=rows[0]['case'];eligible=all(v['incoming'][n]['passed'] for v in by.values() for n in ('writer','probe')) and not any(v['active_boundary_hit'] for v in by.values());null=by['00']['whole_board_period4'] and all(v['complete_canonical_orbit'] for v in by['00']['clocks'].values());gates=all(v['epochs'][n]['truth_table_pass'] for v in by.values() for n in ('early','late'));quiet=all(v['clocks']['receiver']['holds']['terminal']['passed'] for v in by.values());comparisons={};joint=by['11']['clocks']['receiver']
 for mask in ('00','10','01'):
  other=by[mask]['clocks']['receiver'];rel=[]
  for t in range(96,113):
   a,b=tuple(joint['center_trace'][t][:2]),tuple(other['center_trace'][t][:2]);rel.append((PHASES.index(a)-PHASES.index(b))%4 if a in PHASES and b in PHASES else None)
  comparisons[mask]=dict(full336_differs_every_state=all(joint['region_trace'][t]!=other['region_trace'][t] for t in range(96,113)),relative_center_phases=rel,fixed_nonzero_phase=len(set(rel))==1 and rel[0] in (1,2,3))
 departures={m:{name:next((t for t,(x,y) in enumerate(zip(v['clocks']['receiver'][key],by['00']['clocks']['receiver'][key])) if x!=y),None) for name,key in (('first_center','center_trace'),('first_region','region_trace'))} for m,v in by.items()};good=lambda m:comparisons[m]['full336_differs_every_state'] and comparisons[m]['fixed_nonzero_phase'];base=eligible and null and gates and quiet
 return dict(side=case['side'],receiver_phase=case['receiver_phase'],source_inputs_and_boundary_valid=eligible,canonical_null_valid=null,early_and_late_truth_tables_valid=gates,all_terminal_receivers_quiet=quiet,comparisons_11_against=comparisons,departures_from_null=departures,primary_terminal_record=bool(base and all(good(m) for m in ('00','10','01'))),weaker_writer_armed_record=bool(base and good('10')),cases={m:dict(incoming=v['incoming'],epochs=v['epochs'],holds={k:x['holds'] for k,x in v['clocks'].items()},C_counts=v['C_counts']) for m,v in by.items()})


def audit(study,output,budget=400):
 study=Path(study);output=Path(output);assert not output.exists();start=time.process_time();report=dict(passed=False,failure=None,protocol_sha256=SHA,auditor_sha256=file_digest(__file__),preflight_helper_sha256=file_digest(ROOT/'research/clock_selection/audit_carrier_memory_preflight.py'),records=[],groups=[])
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==SHA;assert result['completed_cases']==32 and result['status']=='completed' and result['not_run_cases']==result['captured_not_observed']==[];report['source_sha256']=reg['source_sha256']
  for name,sha in reg['source_sha256'].items():assert file_digest(ROOT/name)==sha==file_digest(study/'executed_sources'/name)
  for name,sha in load(study/'archive_hashes.json').items():assert file_digest(study/name)==sha
  cases=planned();assert len(result['cases'])==len(result['native_checkpoints'])==32;group=[]
  for case,entry,checkpoint in zip(cases,result['cases'],result['native_checkpoints']):
   path=study/entry['record'];native=study/checkpoint['record'];assert file_digest(path)==entry['sha256'] and file_digest(native)==checkpoint['sha256'];row=load(path);assert row['case']==case and row['spec']['controls']==case and row['spec']['steps']==120;assert load(native)=={k:row[k] for k in ('case','spec','assembly','experiment')};integrity,states=audit_record({k:v for k,v in row.items() if k!='observations'},expected_initial=initial(case),deadline=start+budget);out=observe(case,states);assert out==row['observations'],('observation mismatch',case['id'],[k for k in out if out[k]!=row['observations'].get(k)]);assert entry['full_rewind_equal'];hits=integrity.pop('boundary_counter_hits');assert not hits;integrity['boundary_counter_hit_count']=0;report['records'].append(dict(id=case['id'],record_sha256=file_digest(path),native_checkpoint_sha256=file_digest(native),integrity=integrity,all_observations_equal=True,C_counts=out['C_counts'],max_sparse_channels=out['max_sparse_channels']));group.append(dict(case=case,observations=out))
   if len(group)==4:
    a=assess(group);assert a==result['groups'][len(report['groups'])];assert preparation([r['case'] for r in group])==reg['preflight']['groups'][len(report['groups'])];report['groups'].append(a);group=[];print(canonical(dict(audited=len(report['records']),total=32)),flush=True)
  family={str(phase):all(g['primary_terminal_record'] for g in report['groups'] if g['receiver_phase']==phase) for phase in range(4)};assert family==result['primary_family_by_phase'] and any(family.values())==result['primary_family_pass'];outer=load(study/'outer_budget.json');assert outer['all_work_completed'] and outer['budget_passed'] and outer['whole_workflow_cpu_seconds']<=240 and outer['protocol_sha256']==SHA;report.update(passed=True,states=3872,transitions=3840,full_rewinds=32,primary_family_by_phase=family,whole_workflow_budget_receipt=outer,scope=result['scope'])
 except Exception as exc:report['failure']=repr(exc)
 report['cpu_seconds']=time.process_time()-start;output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();r=audit(args.study,args.output);print(canonical({k:r[k] for k in ('passed','failure','cpu_seconds')}));raise SystemExit(0 if r['passed'] else 1)
