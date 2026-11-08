"""Independent full-state and four-mask carry audit; native dynamics are read only."""
import argparse,hashlib,itertools,json,signal,time
from collections import Counter
from pathlib import Path
from research.invariant_families_v1.overlap_preflight import initial,addresses,values,SHA,PRODUCER,WRAPPER
from research.invariant_families_v1.reference import orbit,conjugate_remainder
from research.reference.algebra import coupling,DIRECTIONS
from research.clock_selection.audit import ROOT,load,file_digest,canonical,audit_record


def observe(mask,states):
 aa=addresses();index={a:k for k,a in enumerate(aa)};cp=coupling((1,1,1));dd=[[index[tuple((a[j]+d[j])%4 for j in range(3))+(cp.ports[i][a[3]],)] for i,d in enumerate(DIRECTIONS)] for a in aa];dense=[[s.at(a) for a in aa] for s in states];trace,_=orbit('period4',0,1,2,12);allinputs=[];events=[];checks=[]
 if mask!='11':
  for t,row in enumerate(dense):
   for a,v in zip(aa,row):
    sign=0 if mask=='00' else values(a)[0 if mask=='10' else 1];x,y,r=trace[t];expected=(x,y,r) if sign==1 else (-x,-y,conjugate_remainder(r)) if sign==-1 else (0,0,2);assert v==expected,('singleton',mask,t,a)
 for t in range(1,13):
  old,new=dense[t-1],dense[t];sums=[];count=0
  for k,(a,donors) in enumerate(zip(aa,dd)):
   six=[cp.weights[d][a[3]]*old[j][1] for d,j in enumerate(donors)];u=sum(six);before,after=old[k],new[k];ell=before[0]+after[1];sums.append(u)
   if t==1:assert u==4*(int(mask[0])*values(a)[0]+int(mask[1])*values(a)[1])
   if ell and before!=after:
    kind=((after[2]-before[2])//2)%3;assert kind==u%3;events.append(dict(step=t,address=list(a),kind=kind,ell=ell,before=list(before),after=list(after),u=u,six_signed_donor_values=six));count+=1
  allinputs.append(sums);checks.append(dict(update=t,complete_list_equal=True,native_count=count,expected_count=count))
 equal=[[i,j] for i in range(13) for j in range(i+1,13) if states[i]==states[j]]
 return dict(mask=mask,address_order='lexicographic x,y,z,g; all 3072 addresses',all_native_input_sums=allinputs,all_C=events,C_counts={str(k):sum(e['kind']==k for e in events) for k in range(3)},event_checks=checks,mismatch_counts={},first16_counterexamples=[],all_registered_checks_pass=True,scalar_oracle=[list(x) for x in trace] if mask!='11' else None,exact_whole_state_equalities=equal),dense


def audit(study,output):
 study=Path(study);output=Path(output);assert not output.exists();report=dict(passed=False,failure=None,protocol_sha256=SHA,auditor_sha256=file_digest(__file__),reference_sha256=file_digest(ROOT/'research/invariant_families_v1/reference.py'),records=[])
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==SHA;assert result['status']=='completed' and result['completed_cases']==4 and result['accepted'] and result['sources_unchanged'] and result['captured_but_not_observed']==result['not_captured']==[];assert reg['registered_before_first_native_step'];report['source_sha256']=reg['source_sha256'];assert reg['source_sha256']['research/invariant_families_v1/overlap.py']==PRODUCER and reg['source_sha256']['research/invariant_families_v1/overlap_budget.py']==WRAPPER
  for name,sha in reg['source_sha256'].items():assert file_digest(ROOT/name)==sha==file_digest(study/'executed_sources'/name)
  for name,sha in load(study/'archive_hashes.json').items():assert file_digest(study/name)==sha
  assert len(result['cases'])==len(result['native_checkpoints'])==4;frames={}
  for mask,entry,native in zip(('00','10','01','11'),result['cases'],result['native_checkpoints']):
   if time.process_time()>8.5:raise TimeoutError('Independent audit CPU reserve reached')
   record=study/entry['record'];np=study/native['record'];assert file_digest(record)==entry['sha256'] and file_digest(np)==native['sha256'];row=load(record);raw=load(np);case=dict(id='overlap-'+mask,mask=mask,side=4,steps=12,seed=None);assert row['case']==raw['case']==case and row['native_record']==native['record'] and row['native_sha256']==native['sha256'];experiment=raw['experiment'];assert experiment['provenance']['protocol_sha256']==SHA and experiment['provenance']['overlap_case']==case
   seed=initial(mask);spec=dict(board=dict(side=4,body_signs=[1,1,1],background=[0,0,2]),steps=12,components=[dict(name='independent_initial',recipe='Patch',at=[0,0,0],params=dict(kind='initial',cells=[[*a,*v] for a,v in seed.cells.items()]))]);integrity,states=audit_record(dict(spec=spec,experiment=experiment),expected_initial=seed,deadline=8.5);out,frames[mask]=observe(mask,states);assert out==row['observations'],('observations',mask,[k for k in out if out[k]!=row['observations'].get(k)]);assert entry['full_rewind_equal'] and entry['all_inverse_frames_equal'] and entry['all_registered_checks_pass'] and entry['C_counts']==out['C_counts'];boundary=integrity.pop('boundary_counter_hits');integrity['periodic_boundary_counter_hits']=len(boundary);integrity['periodic_boundary_counter_hit_sha256']=hashlib.sha256(canonical(boundary).encode()).hexdigest();report['records'].append(dict(case=case,record_sha256=file_digest(record),native_sha256=file_digest(np),integrity=integrity,all_observations_equal=True,C_counts=out['C_counts'],input_sums_sha256=hashlib.sha256(canonical(out['all_native_input_sums']).encode()).hexdigest(),raw_C_six_terms_sha256=hashlib.sha256(canonical(out['all_C']).encode()).hexdigest(),exact_whole_state_equalities=out['exact_whole_state_equalities']));print(canonical(dict(audited=len(report['records']),total=4)),flush=True)
  rows=[]
  for t in range(13):
   D=[[frames['11'][t][k][j]-frames['10'][t][k][j]-frames['01'][t][k][j]+frames['00'][t][k][j] for k in range(3072)] for j in range(3)];rows.append(dict(state=t,D_a=D[0],D_b=D[1],D_r=D[2],histograms={n:{str(k):v for k,v in sorted(Counter(vals).items())} for n,vals in zip(('D_a','D_b','D_r'),D)}))
  prediction=[1 if values(a)==(1,1) else -1 if values(a)==(-1,-1) else 0 for a in addresses()];assert rows[1]['D_a']==[0]*3072 and rows[1]['D_b']==prediction and rows[1]['D_r']==[-6*v for v in prediction];observed=dict(address_order='lexicographic x,y,z,g; all 3072 addresses',states=rows,first_step_predictions_pass=True,later_arrays_scope='Descriptive fixed follow-up; no later additive closure is assumed.');assert observed==load(study/'interaction_defects.json.gz');outer=load(study/'outer_budget.json');assert outer['all_native_work_completed'] and outer['producer_budget_passed'] and outer['whole_producer_cpu_seconds']<=20 and outer['protocol_sha256']==SHA
  report.update(passed=True,states=52,transitions=48,full_rewinds=4,all_13_full_defect_arrays_equal=True,first_defect_histograms=rows[1]['histograms'],interaction_defects_sha256=file_digest(study/'interaction_defects.json.gz'),producer_budget_receipt=outer,scope=p['scope'])
 except Exception as exc:report['failure']=repr(exc)
 report['auditor_cpu_seconds_before_serialization_including_imports']=time.process_time();report['audit_share_requires_outer_receipt']=True
 with output.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 return report
if __name__=='__main__':
 def timeout(signum,frame):raise TimeoutError('Independent audit CPU soft limit')
 signal.signal(signal.SIGXCPU,timeout);ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();r=audit(a.study,a.output);print(canonical({k:r[k] for k in ('passed','failure','auditor_cpu_seconds_before_serialization_including_imports')}));raise SystemExit(0 if r['passed'] else 1)
