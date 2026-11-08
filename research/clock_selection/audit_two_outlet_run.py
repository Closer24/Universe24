"""Independent full-state, full-input and outlet audit for the frozen two-input study."""
from __future__ import annotations
import argparse,gzip,hashlib,json,time
from pathlib import Path
from functools import lru_cache
from research.clock_selection.audit import Snapshot,DIRECTIONS,coupling,input_terms,all_events,audit_record,load,file_digest,native_digest,canonical,ROOT,source_control
from research.clock_selection.audit_two_outlet import PROTOCOL_SHA,AXES,initial,packet,sources,planned

@lru_cache(maxsize=4096)
def template(name,origin,direction=1):
 axis,g,h=AXES[name];cells={}
 for k in range(-1,5):
  at=list(origin);at[axis]+=k
  cells[(*at,g)]=(0,0,0);cells[(*at,h)]=(0,0,4)
 cells.update(packet(name,origin))
 if direction==-1:cells={a:(-v[1],-v[0],v[2]) for a,v in cells.items()}
 return {a:v for a,v in cells.items() if v!=(0,0,2)}

def match(state,name,origin,direction=1):
 axis=AXES[name][0]
 crop={a:v for a,v in state.cells.items() if all(origin[j]-1<=a[j]<=origin[j]+(4 if j==axis else 1) for j in range(3))}
 return crop==template(name,tuple(origin),direction)

def observe(case,states):
 if case['stage']=='isolated':
  axis=AXES[case['axis']][0];s0=states[0]
  def translated(t):
   cells={tuple((a[j]+t)%s0.side if j==axis else a[j] for j in range(4)):v for a,v in s0.cells.items()}
   return Snapshot(s0.side,s0.background,cells)
  return {'complete_translation':all(s==translated(t) for t,s in enumerate(states))}
 c=case['side']//2;center=(c,c,c);nodes=(center,*(tuple(c+d[j] for j in range(3)) for d in DIRECTIONS));positions=set(nodes)
 addresses=[(*n,g) for n in nodes for g in range(48)];region=[[list(s.at(a)) for a in addresses] for s in states];ctr=[list(s.at((*center,2))) for s in states]
 cp=coupling((1,1,1));inv=[{g:h for h,g in enumerate(row)} for row in cp.ports]
 events=[dict(step=e['step'],address=e['address'],kind=e['kind'],ell=int(e['quotient'])) for e in all_events(states)[0]]
 boundary=[];inputs=[]
 for t,old in enumerate(states[:-1],1):
  external=[]
  for a,v in sorted(old.cells.items()):
   if not v[1] or a[:3] in positions:continue
   for d,delta in enumerate(DIRECTIONS):
    node=tuple((a[j]+delta[j])%old.side for j in range(3))
    if node in positions:
     g=inv[d^1][a[3]];external.append(dict(target=[*node,g],source=list(a),term=cp.weights[d^1][g]*v[1]))
  boundary.append(dict(update=t,nonzero_external_terms=external))
  sums,terms=input_terms(old,[(*center,2)],(1,1,1))
  inputs.append(dict(update=t,terms=[dict(source=x['address'],term=x['weight']*int(x['b'])) for x in terms[0]],u=sums[0]))
 carriers=[]
 for direction,x in ((1,c+8),(-1,c-8)):
  for t in range(18,len(states)-3):
   if all(match(states[t+k],'X',(x+direction*k,c-1,c),direction) for k in range(4)):
    carriers.append(dict(start=t,direction=direction,outlet_x=x,through=t+3,full_local_template_equal=True))
 incoming={}
 for name,origin in sources(case).items():
  axis=AXES[name][0];delay=case['gap'] if name=='Y' else 0;rows=[]
  for label,offsets in (('early',(4,5,6,7)),('near',(11,12,13))):
   for dt in offsets:
    t=delay+dt;at=list(origin);at[axis]+=t
    rows.append(dict(kind=label,step=t,origin=at,match=match(states[t],name,at)))
  incoming[name]=rows
 outputs={}
 for epoch,T in (('writer',27),('probe',27+case['gap'])):
  rows=[]
  for name,origin in (('X',(c+8,c-1,c)),('Y',(c+1,c+8,c))):
   axis,g,_=AXES[name]
   for lag in range(-4,9):
    t=T+lag;frames=[]
    for k in range(4):
     at=list(origin);at[axis]+=k;frames.append(dict(step=t+k,origin=at,match=match(states[t+k],name,at)))
    ev=[{key:e[key] for key in ('step','kind','ell')} for e in events if e['address']==[*origin,g] and t-3<=e['step']<=t+4]
    expected=[dict(step=t-3,kind=2,ell=-1),dict(step=t+1,kind=1,ell=1)]
    rows.append(dict(port=name,origin_step=t,latency=lag,carrier_states=frames,exact_carrier=all(f['match'] for f in frames),C_events=ev,expected_C=expected,exact_C=ev==expected))
  outputs[epoch]=rows
 hits=[dict(step=t,address=list(a)) for t,s in enumerate(states) for a,v in s.cells.items() if any(v[:2]) and any(q in (0,s.side-1) for q in a[:3])]
 margin=min((min(q,case['side']-1-q) for a,v in states[0].cells.items() if any(v[:2]) for q in a[:3]),default=None)
 hold=dict(complete_region_period4=all(region[t]==region[t+4] for t in range(32,37)),center_unit_counter_norm=all(a*a+b*b==1 for a,b,r in ctr[32:41]),other_counter_pairs_zero=all(not any(v[:2]) for row in region[32:41] for i,v in enumerate(row) if i!=2),every_external_term_zero=all(not row['nonzero_external_terms'] for row in boundary[32:40]))
 return dict(region_nodes=[list(n) for n in nodes],region_addresses=[list(a) for a in addresses],region_trace=region,center_address=[*center,2],center_trace=ctr,center_inputs=inputs,boundary_inputs=boundary,all_C=events,center_C=[e for e in events if e['address']==[*center,2]],candidate_holds=[],outgoing_carriers=carriers,active_boundary_hits=hits,incoming=incoming,outputs=outputs,hold=hold,initial_active_boundary_margin=margin)

def assess(case,out):
 if case['stage']=='isolated':return {'pristine_translation':out['complete_translation']}
 candidates={epoch:[{k:x[k] for k in ('port','origin_step','exact_C')} for x in out['outputs'][epoch] if x['exact_carrier']] for epoch in ('writer','probe')}
 union={(x['port'],x['origin_step']):x for values in candidates.values() for x in values}
 result=dict(input_contracts={name:all(x['match']==(case['control'][i]=='1') for x in out['incoming'][name]) for i,name in enumerate(('X','Y'))},complete_hold=all(out['hold'].values()),strict_initial_causal_margin=out['initial_active_boundary_margin'] is None or out['initial_active_boundary_margin']>88,no_active_boundary_contact=not out['active_boundary_hits'],writer_candidates=candidates['writer'],probe_candidates=candidates['probe'],unique_carrier_candidates=[union[k] for k in sorted(union)])
 for name,epoch in (('X','writer'),('Y','probe')):
  natural=next(x for x in out['outputs'][epoch] if x['port']==name and x['latency']==0)
  result['natural_'+name]=natural['exact_carrier'];result['natural_'+name+'_C']=natural['exact_C']
 return result

def preparation(rows):
 by={r['case']['control']:r['states'][0] for r in rows};case=rows[0]['case'];alladdr=set().union(*(s.cells for s in by.values()));tests=[]
 for index,name in enumerate(('X','Y')):
  origin=sources(case)[name];allowed=set(packet(name,origin));axis,g,h=AXES[name]
  for other in '01':
   off='0'+other if index==0 else other+'0';on='1'+other if index==0 else other+'1';changed={a for a in alladdr if by[off].at(a)!=by[on].at(a)}
   def pristine(a):
    row=all(a[j]==origin[j] for j in range(3) if j!=axis)
    return (0,0,0 if row and a[3]==g else 4 if row and a[3]==h else 2)
   tests.append(dict(source=name,other_present=other,changed_addresses=len(changed),outside_equal=changed<=allowed,absent_footprint_pristine=all(by[off].at(a)==pristine(a) for a in allowed)))
 return dict(checks=tests,passed=all(r['outside_equal'] and r['absent_footprint_pristine'] for r in tests))

def group(rows,p,calibration):
 by={r['case']['control']:r for r in rows};case=rows[0]['case'];a={m:r['assessment'] for m,r in by.items()};prep=preparation(rows)
 baseline=all(x==y for x,y in zip(by['00']['states'],by['00']['states'][4:]));inputs=all(all(x['input_contracts'].values()) for x in a.values());safe=all(x['strict_initial_causal_margin'] and x['no_active_boundary_contact'] for x in a.values());null=not(a['00']['writer_candidates'] or a['00']['probe_candidates']);common=prep['passed'] and baseline and inputs and safe and null
 single=all(a[m][k] for m,keys in (('10',('natural_X','natural_X_C')),('01',('natural_Y','natural_Y_C'))) for k in keys)
 crossed=single and all(a['11'][k] for k in ('natural_X','natural_X_C','natural_Y','natural_Y_C'));jc=a['11']['probe_candidates'];pc=a['01']['probe_candidates'];unique=a['11']['unique_carrier_candidates']
 exclusive=case['clock_mode']=='on' and common and single and bool(calibration and calibration['crossed_natural_calibration']) and case['gap']==0 and len(unique)==1 and unique[0]['exact_C']
 hold=all(x['complete_hold'] for x in a.values());changed=all(by['11']['observations']['region_trace'][t]!=by['01']['observations']['region_trace'][t] for t in range(32,41));no_leak=not(a['00']['probe_candidates'] or a['10']['probe_candidates']);keys=lambda values:[(x['port'],x['origin_step']) for x in values]
 history=case['gap'] in (34,36) and case['clock_mode']=='on' and common and hold and changed and no_leak and keys(jc)!=keys(pc)
 direction=None
 if history:direction='enabled' if not pc and jc else 'suppressed' if pc and not jc else 'changed_ports' if {x['port'] for x in pc}!={x['port'] for x in jc} else 'changed_latency_or_count'
 category='carrier_with_unmatched_C' if any(not x['exact_C'] for x in jc) else 'no_exact_output' if not jc else 'one_registered_outlet' if len(jc)==1 else 'multiple_candidates'
 return dict(geometry={k:v for k,v in case.items() if k!='control'},complete_control_group=True,preparation_equivalence=prep,null_period_divides4=baseline,both_input_contracts=inputs,safe_and_reversible=safe,null_output_absent=null,common_eligible=common,crossed_natural_calibration=case['clock_mode']=='bare' and common and crossed,calibration_geometry=calibration['geometry']['id'] if calibration else None,independent_single_continuations=single,simultaneous_exclusivity=exclusive,all_complete_holds=hold,retained_region_differs=changed,no_late_writer_only_carrier=no_leak,history_discriminator=history,history_carrier_C_discriminator=history and all(x['exact_C'] for x in jc+pc),history_change=direction,redirected_output_candidate=history and a['01']['natural_Y'] and a['01']['natural_Y_C'] and len(jc)==1 and jc[0]['port']=='X' and jc[0]['exact_C'],joint_late_category=category,cases=a,clock_off_comparison_only=case['clock_mode']=='counter_off',claim_limit=p['claim'])

def audit(study,output,budget=600):
 study=Path(study);output=Path(output);assert not output.exists();start=time.process_time();report=dict(passed=False,failure=None,auditor_sha256=file_digest(__file__),protocol_sha256=PROTOCOL_SHA,records=[],groups=[])
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==PROTOCOL_SHA==reg['protocol_sha256'];cases=planned();assert reg['cases']==cases and result['completed_cases']==128 and result['status']=='completed'
  manifest=load(study/'source_provenance/manifest.json');report['sources']=manifest['source_sha256']
  for name,sha in report['sources'].items():assert file_digest(study/'source_provenance/source'/name)==sha==file_digest(ROOT/name)
  equivalence=load(study/'preparation_equivalence.json');batch=[];calibrations={};on={};clockchecks=[]
  for i,entry in enumerate(result['cases']):
   case=cases[i];assert entry['case']==case;path=study/entry['record'];raw=gzip.decompress(path.read_bytes());assert hashlib.sha256(raw).hexdigest()==entry['record_sha256'] and file_digest(path)==entry['record_gzip_sha256'];record=json.loads(raw);assert record['case']==case and record['protocol_sha256']==PROTOCOL_SHA
   integrity,states=audit_record({k:v for k,v in record.items() if k!='observations'},expected_initial=initial(case),deadline=start+budget)
   out=observe(case,states);assert out==record['observations'],('observations',entry['id'],[k for k in out if out[k]!=record['observations'].get(k)])
   assessment=assess(case,out);assert assessment==entry['assessment']==record['assessment'];assert native_digest(states[0])==entry['initial_state_sha256'] and native_digest(states[-1])==entry['final_state_sha256'];assert entry['frames']==len(states)==(13 if i<4 else 89) and entry['full_state_inverse']
   report['records'].append(dict(id=entry['id'],case=case,integrity=integrity,assessment=assessment))
   if i<4:assert record['group_assessment'] is None
   else:
    key=(case['side'],case['phase'],case['gap'],case['control'])
    if case['clock_mode']=='on':on[key]=states[0]
    elif case['clock_mode']=='counter_off':
     c=case['side']//2;source_control(on[key],states[0],[(c,c,c,2)]);clockchecks.append(dict(id=case['id'].replace('counter_off','on')+'-'+case['control'],passed=True))
    batch.append(dict(case=case,states=states,observations=out,assessment=assessment,saved=record['group_assessment']))
    if len(batch)==4:
     expected=group(batch,p,calibrations.get((case['side'],case['gap'])));assert all(r['saved']==expected for r in batch);assert result['groups'][len(report['groups'])]==expected;assert equivalence['groups'][case['id']]==expected['preparation_equivalence'];report['groups'].append(expected)
     if case['clock_mode']=='bare':calibrations[(case['side'],case['gap'])]=expected
     batch=[]
   if (i+1)%4==0:print(canonical(dict(audited=i+1,total=128)),flush=True)
  assert clockchecks==equivalence['clock_masks'] and not batch
  for resultkey,groupkey in (('crossed_calibrations','crossed_natural_calibration'),('simultaneous_exclusivity_groups','simultaneous_exclusivity'),('history_discriminator_groups','history_discriminator'),('history_carrier_C_groups','history_carrier_C_discriminator'),('redirected_output_groups','redirected_output_candidate')):assert result[resultkey]==sum(g[groupkey] for g in report['groups'])
  assert result['isolated_translation_passes']==sum(r['assessment'].get('pristine_translation',False) for r in report['records'])
  overlap=[];prior=study.parent/'two_outlet_v1'
  if (study/'previous_interruption_receipt.json').exists():
   assert (study/'previous_interruption_receipt.json').read_bytes()==(prior/'interruption_receipt.json').read_bytes()
   for entry in result['cases']:
    oldpath=prior/'records'/(entry['id']+'.json.gz')
    if not oldpath.exists():continue
    old,new=load(oldpath),load(study/entry['record'])
    check=dict(id=entry['id'],full_frames_equal=old['experiment']['frames']==new['experiment']['frames'],spec_equal=old['spec']==new['spec'],assessment_equal=old['assessment']==new['assessment'])
    assert all(v for k,v in check.items() if k!='id');overlap.append(check)
   assert overlap==result['retry_overlap'] and len(overlap)==4
  receipt=load(study/'budget_receipt.json');assert receipt['cpu_overrun']==max(0,result['cpu_seconds']-600)
  report.update(retry_overlap=overlap,producer_budget_receipt=receipt,producer_resource_contract_passed=not any(receipt[k] for k in ('cpu_overrun','wall_overrun','byte_overrun')),interrupted_prior_attempt_cpu='unknown; no session-total budget claim')
  report.update(passed=True,states=sum(r['integrity']['states'] for r in report['records']),transitions=sum(r['integrity']['forward_transitions'] for r in report['records']),full_rewinds=128,scope=p['claim'])
 except Exception as e:report['failure']=repr(e)
 report['cpu_seconds']=time.process_time()-start;output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');return report

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);ap.add_argument('--max-cpu-seconds',type=float,default=600);args=ap.parse_args();r=audit(args.study,args.output,args.max_cpu_seconds);print(canonical({k:r[k] for k in ('passed','failure','cpu_seconds')}));raise SystemExit(0 if r['passed'] else 1)
