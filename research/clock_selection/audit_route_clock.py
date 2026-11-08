"""Independent native replay and frozen route-to-clock composition predicates."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from research.clock_selection.audit import Snapshot,DIRECTIONS,coupling,input_terms,all_events,audit_record,load,file_digest,ROOT,canonical
from research.clock_selection.audit_route_clock_preflight import SHA,PHASES,initial,clock_region,planned,directions


def pattern(case,d):return case['patterns'][0 if d==-1 else 1]
def terms(state,address):
 sums,rows=input_terms(state,[address],(1,1,1))
 return [dict(source=r['address'],term=r['weight']*int(r['b'])) for r in rows[0]]

def observe(case,states):
 c=case['side']//2;cp=coupling((1,1,1));inverse=[{g:h for h,g in enumerate(row)} for row in cp.ports];events=[]
 for event in all_events(states)[0]:
  t=event['step'];six=terms(states[t-1],tuple(event['address']));events.append(dict(step=t,address=event['address'],kind=event['kind'],ell=int(event['quotient']),six_terms=six,u=sum(x['term'] for x in six)))
 event_map={(e['step'],tuple(e['address'])):e for e in events};routes={};clocks={}
 for d in directions(case):
  key=str(d);routes[key]={name:[[list(s.at((c+distance*d,c,c,g))) for g in range(48)] for s in states] for name,distance in (('upstream',6),('outlet',8))}
  if case['stage']=='bare':continue
  region=sorted(clock_region(case,d));nodes={a[:3] for a in region};center=(c+8*d,c+1,c,2);trace=[[list(s.at(a)) for a in region] for s in states];ctr=[list(s.at(center)) for s in states];inputs=[];boundary=[]
  for t,(old,new) in enumerate(zip(states,states[1:]),1):
   six=terms(old,center);inputs.append(dict(update=t,six_terms=six,u=sum(x['term'] for x in six),ell=new.at(center)[1]+old.at(center)[0],contact_term=six[3]['term']));external=[]
   for a,v in old.cells.items():
    if not v[1] or a[:3] in nodes:continue
    for dd,delta in enumerate(DIRECTIONS):
     node=tuple((a[j]+delta[j])%old.side for j in range(3))
     if node in nodes:
      h=inverse[dd^1][a[3]];external.append(dict(source=list(a),target=[*node,h],term=cp.weights[dd^1][h]*v[1]))
   boundary.append(dict(update=t,terms=external))
  quiet=dict(full_region_period4=all(trace[t]==trace[t+4] for t in range(64,77)),only_center_counter_activity=all(not any(v[:2]) for row in trace[64:81] for a,v in zip(region,row) if a!=center),constant_center_remainder=len({v[2] for v in ctr[64:81]})==1,exact_quarter_turn=all(ctr[t+1][:2]==[ctr[t][1],-ctr[t][0]] for t in range(64,80)),zero_center_input_and_quotient=all(inputs[t]['u']==inputs[t]['ell']==0 for t in range(64,80)),zero_individual_external_terms=all(not boundary[t]['terms'] for t in range(64,80)))
  hold=ctr[64:81];unit=all(a*a+b*b==1 for a,b,r in hold);broad=all(0<abs(a)+abs(b)<=2 for a,b,r in hold);amp='unit' if unit else 'axis_two' if all((a==0)!=(b==0) and max(abs(a),abs(b))==2 for a,b,r in hold) else 'diagonal' if all(abs(a)==abs(b)==1 for a,b,r in hold) else None
  canonical_null=all(all(s.at(a)==v for a,v in clock_region(dict(case,stage='primary'),d,t).items()) for t,s in enumerate(states));activation=None;first=next((t for t,v in enumerate(ctr) if any(v[:2])),None)
  if not any(ctr[0][:2]) and first is not None:
   t=first;inp=inputs[t-1];event=event_map.get((t,center));activation=dict(update=t,before=ctr[t-1],after=ctr[t],**{k:v for k,v in inp.items() if k!='update'},native_C=event,zero_to_counter_guard_consistent=bool(ctr[t][0]==0 and ctr[t][1]==inp['ell'] and inp['ell']!=0 and inp['u']!=0 and event is not None))
  clocks[key]=dict(region_addresses=[list(a) for a in region],region_trace=trace,center_trace=ctr,center_inputs=inputs,external_inputs=boundary,quiet_predicates=quiet,quiet_common=all(quiet.values()),unit_center=unit,bounded_nonzero_center=broad,amplitude_class=amp,retained_center_remainder=hold[0][2] if quiet['constant_center_remainder'] else None,primary_unit_r0_quiet=all(quiet.values()) and unit and all(v[2]==0 for v in hold),secondary_even_quiet=all(quiet.values()) and broad and all(v[2] in (0,2,4) for v in hold),complete_canonical_null_orbit=canonical_null,all_region_counters_zero=all(not any(v[:2]) for row in trace for v in row),first_activation=activation)
 return dict(routes=routes,clocks=clocks,all_C=events,C_counts={str(k):sum(e['kind']==k for e in events) for k in range(3)},whole_board_stationary=all(s==states[0] for s in states),active_boundary_hit=any(any(q in (0,case['side']-1) for q in a[:3]) for s in states for a,v in s.cells.items() if any(v[:2])),max_sparse_channels=max(len(s.cells) for s in states))


def assess(rows,bare):
 by={r['case']['source_present']:r for r in rows};off,on=by[False],by[True];case=on['case'];out=dict(case={k:v for k,v in case.items() if k!='source_present'},stage=case['stage'],clocks={})
 if case['stage']=='bare':
  checks={}
  for d in directions(case):
   key=str(d);a,b=on['observations']['routes'][key]['outlet'],off['observations']['routes'][key]['outlet'];checks[key]=dict(pattern=pattern(case,d),source_caused_counter_output=any(any(v[:2]!=w[:2] and any(v[:2]) for v,w in zip(a[t],b[t])) for t in range(1,33)),entire_outlet_matches_null=all(a[t]==b[t] for t in range(1,33)))
  valid=all(r['source_caused_counter_output'] if r['pattern']=='OR' else r['entire_outlet_matches_null'] for r in checks.values()) and off['observations']['whole_board_stationary'];out.update(bare_valid=valid,outlets=checks,null_stationary=off['observations']['whole_board_stationary']);return out
 nulls=[];early=[];deliveries={}
 for d in directions(case):
  key=str(d);a,b=on['observations']['clocks'][key],off['observations']['clocks'][key];null=b['complete_canonical_null_orbit'] if case['stage']=='primary' else off['observations']['whole_board_stationary'] and b['all_region_counters_zero'];nulls.append(null)
  u,v=on['observations']['routes'][key]['upstream'],off['observations']['routes'][key]['upstream'];arrival=next((t for t in range(1,33) if any(x[:2]!=y[:2] and any(x[:2]) for x,y in zip(u[t],v[t]))),None);contact=next((t+1 for t in range(48) if a['center_inputs'][t]['contact_term']!=0 and a['center_inputs'][t]['contact_term']!=b['center_inputs'][t]['contact_term']),None);depart=next((t for t in range(81) if a['center_trace'][t]!=b['center_trace'][t]),None);rdepart=next((t for t in range(81) if a['region_trace'][t]!=b['region_trace'][t]),None);delivery=arrival is not None and contact is not None and depart is not None and contact<=depart;deliveries[key]=delivery
  compatible=True if case['isolated_direction'] else all(row['observations']['routes'][key]['upstream'][:11]==bare['rows'][present]['observations']['routes'][key]['upstream'][:11] for present,row in by.items());early.append(compatible)
  changed=all(a['center_trace'][t][:2]!=b['center_trace'][t][:2] for t in range(64,81));rel=[]
  for t in range(64,81):
   x,y=tuple(a['center_trace'][t][:2]),tuple(b['center_trace'][t][:2]);rel.append((PHASES.index(x)-PHASES.index(y))%4 if x in PHASES and y in PHASES else None)
  fixed=len(set(rel))==1 and rel[0] in (1,2,3)
  out['clocks'][key]=dict(pattern=pattern(case,d),null_valid=null,early_upstream_matches_bare=compatible,first_upstream_counter_arrival=arrival,first_source_caused_contact_input=contact,first_center_departure=depart,first_region_departure=rdepart,delivery_valid=delivery,quiet_predicates=a['quiet_predicates'],unit_r0_quiet=a['primary_unit_r0_quiet'],retained_changed_phase=bool(a['primary_unit_r0_quiet'] and changed and fixed),relative_phase_during_hold=rel,full_hold_matches_null=a['region_trace'][64:81]==b['region_trace'][64:81],secondary_even_quiet=a['secondary_even_quiet'],amplitude_class=a['amplitude_class'],retained_remainder=a['retained_center_remainder'],first_activation=a['first_activation'])
 bare_valid=True if case['isolated_direction'] else bare['assessment']['bare_valid'];winner=[str(d) for d in directions(case) if case['isolated_direction'] or pattern(case,d)=='OR'];loser=[str(d) for d in directions(case) if not case['isolated_direction'] and pattern(case,d)=='NO'];eligible=bare_valid and all(early) and all(nulls) and all(deliveries[k] for k in winner);retained=all(out['clocks'][k]['full_hold_matches_null'] for k in loser);primary=case['stage']=='primary' and eligible and retained and all(out['clocks'][k]['retained_changed_phase'] for k in winner);secondary=case['stage']=='clock_off' and eligible and retained and all(out['clocks'][k]['secondary_even_quiet'] and out['clocks'][k]['first_activation'] and out['clocks'][k]['first_activation']['zero_to_counter_guard_consistent'] for k in winner)
 out.update(eligible=bool(eligible),bare_route_valid=bare_valid,loser_retained=retained,primary_phase_memory_pass=bool(primary),secondary_activation_pass=bool(secondary),secondary_unit_activation_pass=bool(secondary and all(out['clocks'][k]['amplitude_class']=='unit' for k in winner)));return out


def audit(study,output,budget=600):
 study=Path(study);output=Path(output);assert not output.exists();start=time.process_time();report=dict(passed=False,failure=None,auditor_sha256=file_digest(__file__),preflight_helper_sha256=file_digest(ROOT/'research/clock_selection/audit_route_clock_preflight.py'),protocol_sha256=SHA,records=[],pairs=[])
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==SHA;assert result['completed_cases']==64 and result['status']=='completed';assert file_digest(study/'executed_route_clock.py')==reg['source_sha256']['research/clock_selection/route_clock.py']
  for name,sha in reg['source_sha256'].items():assert file_digest(ROOT/name)==sha
  for name,sha in load(study/'archive_hashes.json').items():assert file_digest(study/name)==sha
  report['source_sha256']=reg['source_sha256'];cases=planned();bare_bank={};pair=[]
  assert len(result['cases'])==len(result['native_checkpoints'])==64 and result['not_run_cases']==result['captured_not_observed']==[]
  for case,entry,native in zip(cases,result['cases'],result['native_checkpoints']):
   path=study/entry['record'];rawpath=study/native['record'];assert file_digest(path)==entry['sha256'] and file_digest(rawpath)==native['sha256'];row=load(path);checkpoint=load(rawpath);assert row['case']==case and row['spec']['controls']==case and row['spec']['steps']==80
   assert checkpoint=={k:row[k] for k in ('case','spec','assembly','experiment')};seed=initial(case);spec=dict(board=dict(side=case['side'],body_signs=[1,1,1],background=[0,0,2]),steps=80,components=[dict(name='independent_complete_initial',recipe='Patch',at=[0,0,0],params=dict(kind='initial',cells=[[*a,*v] for a,v in seed.cells.items()]))]);integrity,states=audit_record(dict(spec=spec,assembly=row['assembly'],experiment=row['experiment']),expected_initial=seed,deadline=start+budget)
   observations=observe(case,states);assert observations==row['observations'],('observation mismatch',entry['id'],[k for k in observations if observations[k]!=row['observations'].get(k)]);assert not observations['active_boundary_hit'];assert entry['full_rewind_equal']
   hits=integrity.pop('boundary_counter_hits');assert not hits;integrity['boundary_counter_hit_count']=0;report['records'].append(dict(id=entry['id'],record_sha256=file_digest(path),native_checkpoint_sha256=file_digest(rawpath),integrity=integrity,all_observations_equal=True,C_counts=observations['C_counts'],max_sparse_channels=observations['max_sparse_channels']));pair.append(dict(case=case,observations=observations))
   if len(pair)==2:
    key=(case['side'],tuple(case['patterns']));assessment=assess(pair,bare_bank.get(key));assert assessment==result['pairs'][len(report['pairs'])];report['pairs'].append(assessment)
    if case['stage']=='bare':bare_bank[key]=dict(rows={r['case']['source_present']:r for r in pair},assessment=assessment)
    pair=[]
   if len(report['records'])%2==0:print(canonical(dict(audited=len(report['records']),total=64)),flush=True)
  primary={str(phase):all(g['primary_phase_memory_pass'] for g in report['pairs'] if g['stage']=='primary' and g['case']['phase']==phase) for phase in (1,2)};assert primary==result['primary_family_by_phase'] and any(primary.values())==result['primary_family_pass'];secondary=[g for g in report['pairs'] if g['stage']=='clock_off'];assert len(secondary)==4 and all(g['secondary_activation_pass'] for g in secondary)==result['secondary_family_pass'] and all(g['secondary_unit_activation_pass'] for g in secondary)==result['secondary_unit_family_pass'];outer=load(study/'outer_budget.json');assert outer['all_work_completed'] and outer['whole_workflow_cpu_seconds']<=300 and outer['budget_passed'] and outer['protocol_sha256']==SHA
  report.update(passed=True,states=5184,transitions=5120,full_rewinds=64,primary_family_by_phase=primary,secondary_family_pass=result['secondary_family_pass'],whole_workflow_budget_receipt=outer,scope=result['scope'])
 except Exception as exc:report['failure']=repr(exc)
 report['cpu_seconds']=time.process_time()-start;output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();r=audit(args.study,args.output);print(canonical({k:r[k] for k in ('passed','failure','cpu_seconds')}));raise SystemExit(0 if r['passed'] else 1)
