"""Independent full-state audit of signal-started resting-clock experiments."""
import argparse,gzip,hashlib,itertools,json,time
from pathlib import Path
from research.clock_selection.audit import DIRECTIONS,coupling,input_terms,all_events,audit_record,load,file_digest,native_digest,ROOT,canonical,matches
from research.clock_selection.audit_activation_preflight import SHA,initial,geometry,planned,check


def observe(case,states):
 c,center,nodes=geometry(case);positions=set(nodes);addresses=[(*n,g) for n in nodes for g in range(48)];region=[[list(s.at(a)) for a in addresses] for s in states];ctr=[list(s.at((*center,2))) for s in states];cp=coupling((1,1,1));inverse=[{g:h for h,g in enumerate(row)} for row in cp.ports];events=[dict(step=e['step'],address=e['address'],kind=e['kind'],ell=int(e['quotient'])) for e in all_events(states)[0]];boundary=[];inputs=[]
 for t,old in enumerate(states[:-1],1):
  ext=[]
  for a,v in sorted(old.cells.items()):
   if not v[1] or a[:3] in positions:continue
   for d,delta in enumerate(DIRECTIONS):
    n=tuple((a[j]+delta[j])%old.side for j in range(3))
    if n in positions:
     h=inverse[d^1][a[3]];ext.append(dict(target=[*n,h],source=list(a),term=cp.weights[d^1][h]*v[1]))
  boundary.append(dict(update=t,nonzero_external_terms=ext));sums,donors=input_terms(old,[(*center,2)],(1,1,1));inputs.append(dict(update=t,terms=[dict(source=r['address'],term=r['weight']*int(r['b'])) for r in donors[0]],u=sums[0]))
 carriers=[]
 for direction,x in ((1,c+8),(-1,c-8)):
  for t in range(18,len(states)-3):
   if all(matches(states[t+k],x+direction*k,c,c,direction) for k in range(4)):carriers.append(dict(start=t,direction=direction,outlet_x=x,through=t+3,full_local_template_equal=True))
 center_events=[e for e in events if e['address']==[*center,2]];first=next((t for t,v in enumerate(ctr) if any(v[:2])),None);act=None if first is None else dict(step=first,before=ctr[first-1] if first else None,after=ctr[first],input=inputs[first-1] if first else None,native_C=next((e for e in center_events if e['step']==first),None));other=next((t for t,row in enumerate(region) if any(any(v[:2]) for i,v in enumerate(row) if i!=2)),None)
 hold=dict(full336_lag4=all(region[t]==region[t+4] for t in range(64,77)),only_center_counters_nonzero=all(not any(v[:2]) for row in region[64:81] for i,v in enumerate(row) if i!=2),center_small_nonzero=all(0<abs(v[0])+abs(v[1])<=2 for v in ctr[64:81]),constant_even_remainder=len({v[2] for v in ctr[64:81]})==1 and all(v[2]%2==0 for v in ctr[64:81]),quarter_turn_each_update=all(ctr[t+1][:2]==[ctr[t][1],-ctr[t][0]] for t in range(64,80)),every_external_term_zero=all(not r['nonzero_external_terms'] for r in boundary[64:80]),no_center_C=not any(64<e['step']<=80 for e in center_events));a,b,r=ctr[64];kind='unit' if abs(a)+abs(b)==1 else 'axis2' if sorted((abs(a),abs(b)))==[0,2] else 'diagonal' if abs(a)==abs(b)==1 else None
 return dict(region_nodes=[list(n) for n in nodes],region_addresses=[list(a) for a in addresses],region_trace=region,center_address=[*center,2],center_trace=ctr,center_inputs=inputs,boundary_inputs=boundary,all_C=events,center_C=center_events,candidate_holds=[],outgoing_carriers=carriers,active_boundary_hits=[dict(step=t,address=list(a)) for t,s in enumerate(states) for a,v in s.cells.items() if any(v[:2]) and any(q in (0,s.side-1) for q in a[:3])],incoming=[dict(step=t,match=matches(states[t],c-18+t,c,c,1)) for t in (4,5,6,7)],first_center_activation=act,first_other_region_counter_activity=other,hold=hold,hold_class=kind,hold_center_initial=[a,b,r],initial_active_boundary_margin=min((min(q,case['side']-1-q) for a,v in states[0].cells.items() if any(v[:2]) for q in a[:3]),default=None))


def assess(case,states,out):
 a=out['first_center_activation'];margin=out['initial_active_boundary_margin'];activation=bool(a and a['step']>0 and a['before'][:2]==[0,0] and a['input']['u']!=0 and a['native_C'] is not None and a['native_C']['ell']!=0)
 return dict(incoming_contract=all(x['match']==case['source_present'] for x in out['incoming']),initial_region_at_rest=all(not any(v[:2]) for v in out['region_trace'][0]),whole_board_stationary=all(s==states[0] for s in states),native_contact_activation=activation,quiet_clock_hold=all(out['hold'].values()),clock_class=out['hold_class'],strict_initial_causal_margin=margin is None or margin>80,no_active_boundary_contact=not out['active_boundary_hits'])

def pair(rows):
 by={r['case']['source_present']:r for r in rows};assert set(by)=={False,True};case=rows[0]['case'];checks=check(case);common=all(checks[k] for k in ('outside_source_footprint_equal','source_absent_pristine','all336_initial_counter_pairs_zero')) and all(r['assessment'][k] for r in rows for k in ('incoming_contract','initial_region_at_rest','strict_initial_causal_margin','no_active_boundary_contact'));accepted=common and by[False]['assessment']['whole_board_stationary'] and by[True]['assessment']['native_contact_activation'] and by[True]['assessment']['quiet_clock_hold']
 return dict(geometry={k:v for k,v in case.items() if k not in ('source_present','id')},complete_pair=True,initial_preparation_checks=checks,common_eligible=common,accepted_signal_started_clock=accepted,clock_class=by[True]['assessment']['clock_class'] if accepted else None,cases={str(int(k)):r['assessment'] for k,r in by.items()})

def audit(study,output,budget=300):
 study=Path(study);output=Path(output);assert not output.exists();start=time.process_time();report=dict(passed=False,failure=None,protocol_sha256=SHA,auditor_sha256=file_digest(__file__),preflight_helper_sha256=file_digest(ROOT/'research/clock_selection/audit_activation_preflight.py'),records=[],pairs=[])
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==SHA==reg['protocol_sha256'];assert result['status']=='completed' and result['completed_cases']==36 and result['failed_cases']==result['not_run_cases']==result['captured_but_unobserved_ids']==[];assert reg['cases']==planned();manifest=load(study/'source_provenance/manifest.json');report['source_sha256']=manifest['source_sha256']
  for name,sha in report['source_sha256'].items():assert file_digest(ROOT/name)==sha==file_digest(study/'source_provenance/source'/name)
  for name,sha in load(study/'archive_hashes.json').items():assert file_digest(study/name)==sha
  pre=load(study/'preparation_equivalence.json');rows=[]
  for case,entry in zip(planned(),result['cases']):
   assert entry['case']==case;path=study/entry['record'];raw=gzip.decompress(path.read_bytes());assert hashlib.sha256(raw).hexdigest()==entry['record_sha256'] and file_digest(path)==entry['record_gzip_sha256'];row=json.loads(raw);assert row['case']==case and row['protocol_sha256']==SHA;native=load(study/entry['native_capture']);assert file_digest(study/entry['native_capture'])==entry['native_capture_sha256'];assert native['spec_sha256']==hashlib.sha256(canonical(row['spec']).encode()).hexdigest() and native['assembly']==row['assembly'] and native['experiment']==row['experiment']
   integrity,states=audit_record({k:v for k,v in row.items() if k!='observations'},expected_initial=initial(case),deadline=start+budget);out=observe(case,states);assert out==row['observations'],('observations',case['id'],[k for k in out if out[k]!=row['observations'].get(k)]);assessment=assess(case,states,out);assert assessment==entry['assessment']==row['assessment'];assert check(case)==pre[case['id']];assert len(states)==entry['frames']==81 and native_digest(states[0])==entry['initial_state_sha256'] and native_digest(states[-1])==entry['final_state_sha256'] and entry['full_state_inverse'];hits=integrity.pop('boundary_counter_hits');assert not hits;integrity['boundary_counter_hit_count']=0
   report['records'].append(dict(id=entry['id'],record_sha256=file_digest(path),native_capture_sha256=file_digest(study/entry['native_capture']),integrity=integrity,assessment=assessment,first_center_activation=out['first_center_activation'],first_other_region_counter_activity=out['first_other_region_counter_activity'],hold=out['hold'],hold_center_initial=out['hold_center_initial']));rows.append(dict(case=case,assessment=assessment))
   if len(rows)==2:
    group=pair(rows);assert group==result['pairs'][len(report['pairs'])];report['pairs'].append(group);rows=[]
   if len(report['records'])%2==0:print(canonical(dict(audited=len(report['records']),total=36)),flush=True)
  accepted=[g for g in report['pairs'] if g['accepted_signal_started_clock']];assert len(accepted)==result['accepted_pairs'];assert result['classes']=={k:sum(g['clock_class']==k for g in accepted) for k in ('unit','axis2','diagonal')};replicated=[]
  for rc,rh in itertools.product((0,2,4),repeat=2):
   groups=[g for g in report['pairs'] if g['geometry']['center_remainder']==rc and g['geometry']['halo_remainder']==rh];assert len(groups)==2;ok=all(g['accepted_signal_started_clock'] for g in groups) and len({g['clock_class'] for g in groups})==1;replicated.append(dict(center_remainder=rc,halo_remainder=rh,accepted_on_both_sizes=ok,**{'class':groups[0]['clock_class'] if ok else None}))
  assert replicated==result['replicated_geometries'];outer=load(study/'outer_budget.json');assert outer['all_work_completed'] and outer['budget_passed'] and outer['whole_workflow_cpu_seconds']<=180 and outer['protocol_sha256']==SHA;report.update(passed=True,states=2916,transitions=2880,full_rewinds=36,accepted_pairs=len(accepted),replicated_geometries=replicated,whole_workflow_budget_receipt=outer,scope=p['claim'])
 except Exception as exc:report['failure']=repr(exc)
 report['cpu_seconds']=time.process_time()-start;output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();r=audit(args.study,args.output);print(canonical({k:r[k] for k in ('passed','failure','cpu_seconds')}));raise SystemExit(0 if r['passed'] else 1)
