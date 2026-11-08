"""Independent exact-matrix/native-state audit of finite internal channel modes."""
from __future__ import annotations
import argparse,itertools,json,time
from pathlib import Path
from research.clock_selection.audit import Snapshot,coupling,file_digest,load,ROOT,canonical,all_events,audit_record
SHA='ff58a9cae8b106975a662c719af46496260ff8b807d6435f83554f4e3d50a449'

def oracle(case,t,v):
 h=case['duration'];sg=case['amplitude_sign'];m=case['stationary_uniform_offset'];c=[1,1]
 for _ in range(11):c.append(2*c[-1]-9*c[-2])
 a=sg*3**(h-1) if not t else sg*3**(h-t+1)*c[t-1];b=sg*3**(h-t)*c[t]
 return tuple((a*x+m,b*x+m,case['remainder']) for x in v)

def audit(study,output,budget=180):
 study=Path(study);output=Path(output);assert not output.exists();start=time.process_time();report=dict(passed=False,failure=None,protocol_sha256=SHA,auditor_sha256=file_digest(__file__),records=[],groups=[])
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==SHA
  assert result['completed_cases']==20 and result['status']=='completed';v=p['integer_eigenvector'];cp=coupling((1,1,1));assert len(v)==48 and sum(x!=0 for x in v)==18
  assert all(sum(cp.weights[d][g]*v[cp.ports[d][g]] for d in range(6))==2*v[g] for g in range(48))
  assert file_digest(study/'executed_internal_gap_demo.py')==reg['source_sha256']['research/clock_selection/internal_gap_demo.py']
  for name,sha in reg['source_sha256'].items():assert file_digest(ROOT/name)==sha
  report['source_sha256']=reg['source_sha256'];batch=[]
  modes=[('gap_plus',1,0,2),('gap_minus',-1,0,2),('uniform_only',0,1,2),('gap_plus_offset',1,1,2),('gap_plus_parity',1,0,3)]
  cases=[dict(id=f'internal-gap-L{L}-H{H}-{name}',side=L,duration=H,mode=name,amplitude_sign=sg,stationary_uniform_offset=M,remainder=R) for L,H,(name,sg,M,R) in itertools.product((3,5),(8,12),modes)]
  for case,entry in zip(cases,result['cases']):
   path=study/entry['record'];assert file_digest(path)==entry['sha256'];row=load(path);assert row['case']==case and entry['id']==case['id'];L=case['side'];sites=list(itertools.product(range(L),repeat=3));values=oracle(case,0,v);seed=Snapshot(L,(0,0,2),{(*xyz,g):values[g] for xyz in sites for g in range(48)})
   spec=dict(board=dict(side=L,body_signs=[1,1,1],background=[0,0,2]),steps=case['duration'],components=[dict(name='independent_initial',recipe='Patch',at=[0,0,0],params=dict(kind='initial',cells=[[*a,*q] for a,q in seed.cells.items()]))])
   integrity,states=audit_record(dict(spec=spec,experiment=row['experiment']),expected_initial=seed,deadline=start+budget)
   traces=[]
   for t,state in enumerate(states):
    expected=oracle(case,t,v);traces.append([list(q) for q in expected]);assert all(state.at((*xyz,g))==expected[g] for xyz in sites for g in range(48))
   events=[dict(step=e['step'],address=e['address'],kind=e['kind'],ell=int(e['quotient'])) for e in all_events(states)[0]];expected_events=[];checks=[]
   for t in range(1,len(states)):
    before=oracle(case,t-1,v);after=oracle(case,t,v);local=[]
    for g in range(48):
     u=sum(cp.weights[d][g]*before[cp.ports[d][g]][1] for d in range(6));ell,rem=divmod(2*u+before[g][2],6);assert after[g]==(before[g][1],ell-before[g][0],rem)
     if ell and before[g]!=after[g]:local.append((g,u%3,ell))
    assert len(local)==(0 if case['amplitude_sign']==0 else 18) and all(k==0 for g,k,q in local)
    expected_events.extend(dict(step=t,address=[*xyz,g],kind=k,ell=q) for xyz in sites for g,k,q in local)
    checks.append(dict(update=t,all_addresses_classes_quotients_equal=True,actual_count=L**3*len(local),expected_count=L**3*len(local)))
   assert events==expected_events
   observed=dict(full_oracle_mismatches=[],all_triples_match_oracle=True,spatial_uniformity=True,all_event_addresses_classes_quotients_match=True,event_checks=checks,all_C=events,C_counts={str(k):sum(e['kind']==k for e in events) for k in range(3)},complete_channel_trace_at_origin=traces,remainders_match_registered_value=True,max_sparse_channels=max(len(s.cells) for s in states))
   assert observed==row['observations'],('observations',entry['id'],[k for k in observed if observed[k]!=row['observations'].get(k)])
   report['records'].append(dict(id=entry['id'],record_sha256=file_digest(path),integrity=integrity,all_oracles_equal=True,raw_C_counts=observed['C_counts']));batch.append((case,states,events))
   if len(batch)==5:
    by={c['mode']:(s,e) for c,s,e in batch}
    for t in range(len(states)):
     for xyz in sites:
      for g in range(48):
       a,b,m,x,q=[by[k][0][t].at((*xyz,g)) for k in ('gap_plus','gap_minus','uniform_only','gap_plus_offset','gap_plus_parity')]
       assert b==(-a[0],-a[1],a[2]);assert x==(a[0]+m[0],a[1]+m[1],2);assert q==(a[0],a[1],a[2]+1)
    assert by['gap_plus'][1]==by['gap_plus_parity'][1]
    group=dict(side=L,duration=case['duration'],all_full_state_oracles_pass=True,all_raw_event_oracles_pass=True,exact_sign_control=True,exact_stationary_uniform_offset_independence=True,exact_inert_parity_counter_and_remainder_identity=True,exact_inert_parity_native_events=True,physical_mass_or_transport_established=False)
    assert group==result['groups'][len(report['groups'])];report['groups'].append(group);batch=[]
   print(canonical(dict(audited=len(report['records']),total=20)),flush=True)
  assert not batch and len(report['records'])==20
  report.update(passed=True,states=sum(r['integrity']['states'] for r in report['records']),transitions=sum(r['integrity']['forward_transitions'] for r in report['records']),full_rewinds=20,scope='Exact finite-H global internal mode plus stationary offset and inert parity; no physical mass, localized object, transport or route-selection result.')
 except Exception as exc:report['failure']=repr(exc)
 report['cpu_seconds']=time.process_time()-start;output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');return report

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();r=audit(args.study,args.output);print(canonical({k:r[k] for k in ('passed','failure','cpu_seconds')}));raise SystemExit(0 if r['passed'] else 1)
