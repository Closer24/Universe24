"""Independent complete native replay of the newly registered invariant families."""
import argparse,hashlib,itertools,json,time
from pathlib import Path
from research.invariant_families_v1 import reference
from research.invariant_families_v1.preflight import planned,expected_initial,NAMES,PROTOCOL_SHA,PRODUCER_SHA,BUDGET_SHA
from research.clock_selection.audit import load,file_digest,canonical,audit_record,ROOT
from research.reference.algebra import coupling,DIRECTIONS


def observe(case,states):
 name=NAMES[case['pattern']];L=case['side'];addresses=list(itertools.product(range(L),range(L),range(L),range(48)));values=[reference.pattern(name,*a) for a in addresses];trace,quotients=reference.orbit(name,case['a'],case['b'],case['r'],18);cp=coupling((1,1,1));events=[];inputs=[];checks=[]
 for t,state in enumerate(states):assert state==reference.state(name,*trace[t]),('full encoded oracle',case['id'],t)
 for t,(old,new) in enumerate(zip(states,states[1:]),1):
  sums=[];count=0
  for address,v in zip(addresses,values):
   terms=[cp.weights[d][address[3]]*old.at(tuple((address[j]+delta[j])%L for j in range(3))+(cp.ports[d][address[3]],))[1] for d,delta in enumerate(DIRECTIONS)];u=sum(terms);assert u==case['lambda']*trace[t-1][1]*v;before,after=old.at(address),new.at(address);ell=before[0]+after[1];assert ell==quotients[t-1]*v;sums.append(u)
   if ell and before!=after:
    kind=((after[2]-before[2])//2)%3;assert kind==u%3;events.append(dict(step=t,address=list(address),kind=kind,ell=ell,u=u,six_signed_donor_values=terms));count+=1
  inputs.append(sums);checks.append(dict(update=t,complete_event_list_matches=True,actual_count=count,expected_count=count))
 returns=[t for t in range(1,19) if states[t]==states[0]];first=returns[0] if returns else None;lag=first is not None and all(states[t]==states[t+first] for t in range(19-first));zero=all(state.at(address)==(0,0,2) for state in states for address,v in zip(addresses,values) if v==0)
 return dict(scalar_trace=[list(x) for x in trace],full_state_mismatch_count=0,full_state_counterexamples_first16=[],input_sum_mismatch_count=0,input_counterexamples_first16=[],event_mismatch_updates=0,event_counterexamples_first16=[],event_checks=checks,all_native_input_sums=inputs,input_address_order='lexicographic x,y,z,g; all48 channels at every site',all_C=events,C_counts={str(k):sum(e['kind']==k for e in events) for k in range(3)},zero_pattern_channels_remain_fixed=zero,first_complete_state_return_within_H=first,registered_lag_matches_entire_available_window=lag,all_observed_returns_within_H=returns,max_sparse_channels=max(len(s.cells) for s in states),all_registered_oracles_pass=zero)


def audit(study,output,budget=300):
 study=Path(study);output=Path(output);assert not output.exists();start=time.process_time();report=dict(passed=False,failure=None,protocol_sha256=PROTOCOL_SHA,auditor_sha256=file_digest(__file__),reference_sha256=file_digest(Path(reference.__file__)),records=[])
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==PROTOCOL_SHA;assert result['status']=='completed' and result['completed_cases']==48 and result['not_run_cases']==result['captured_not_observed']==[] and result['all_full_rewinds'] and result['all_registered_oracles_pass'];assert len(result['cases'])==len(result['native_checkpoints'])==48;assert reg['registered_before_first_native_step'];report['source_sha256']=reg['source_sha256']
  assert reg['source_sha256']['research/invariant_families_v1/run.py']==PRODUCER_SHA and reg['source_sha256']['research/invariant_families_v1/budget.py']==BUDGET_SHA
  for name,sha in reg['source_sha256'].items():assert file_digest(ROOT/name)==sha==file_digest(study/'executed_sources'/name)
  for name,sha in load(study/'archive_hashes.json').items():assert file_digest(study/name)==sha
  expected_cases=planned();assert [x['case'] for x in reg['preflight']['cases']]==expected_cases
  for case,entry,raw in zip(expected_cases,result['cases'],result['native_checkpoints']):
   path=study/entry['record'];np=study/raw['record'];assert file_digest(path)==entry['sha256'] and file_digest(np)==raw['sha256'];row=load(path);assert row['case']==entry['case']==case and load(np)==dict(case=case,experiment=row['experiment']);assert row['experiment']['provenance']['invariant_case']==case and row['experiment']['provenance']['protocol_sha256']==PROTOCOL_SHA
   seed=expected_initial(case);spec=dict(board=dict(side=case['side'],body_signs=[1,1,1],background=[0,0,2]),steps=18,components=[dict(name='independent_complete_initial',recipe='Patch',at=[0,0,0],params=dict(kind='initial',cells=[[*a,*v] for a,v in seed.cells.items()]))]);integrity,states=audit_record(dict(spec=spec,experiment=row['experiment']),expected_initial=seed,deadline=start+budget);out=observe(case,states);assert out==row['observations'],('observations',case['id'],[k for k in out if out[k]!=row['observations'].get(k)]);assert entry['full_rewind_equal'] and entry['all_registered_oracles_pass'] and entry['C_counts']==out['C_counts'] and entry['first_complete_state_return_within_H']==out['first_complete_state_return_within_H'];boundary=integrity.pop('boundary_counter_hits');integrity['periodic_boundary_counter_hit_count']=len(boundary);integrity['periodic_boundary_counter_hit_sha256']=hashlib.sha256(canonical(boundary).encode()).hexdigest()
   report['records'].append(dict(case=case,record_sha256=file_digest(path),native_checkpoint_sha256=file_digest(np),integrity=integrity,all_oracles_equal=True,C_counts=out['C_counts'],scalar_trace=out['scalar_trace'],input_arrays_sha256=hashlib.sha256(canonical(out['all_native_input_sums']).encode()).hexdigest(),raw_C_with_six_terms_sha256=hashlib.sha256(canonical(out['all_C']).encode()).hexdigest(),first_complete_state_return_within_H=out['first_complete_state_return_within_H'],all_observed_returns_within_H=out['all_observed_returns_within_H']));print(canonical(dict(audited=len(report['records']),total=48)),flush=True)
  outer=load(study/'outer_budget.json');assert outer['all_work_completed'] and outer['budget_passed'] and outer['whole_workflow_cpu_seconds']<=180 and outer['protocol_sha256']==PROTOCOL_SHA;report.update(passed=True,states=912,transitions=864,full_rewinds=48,channel_state_triples=1586880,whole_workflow_budget_receipt=outer,scope='New complete native checks of four global periodic+++ invariant sectors,6base remainders and2counter seeds,H18. The all-state embedding proof is separate. This is not the unavailable historical48-case data, not signed native dynamics, not all6q generalized remainders, not propagation or physical mass, and not an overlap-interaction study.')
 except Exception as exc:report['failure']=repr(exc)
 report['cpu_seconds']=time.process_time()-start;output.parent.mkdir(parents=True,exist_ok=True)
 with output.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();r=audit(args.study,args.output);print(canonical({k:r[k] for k in ('passed','failure','cpu_seconds')}));raise SystemExit(0 if r['passed'] else 1)
