"""Independent exact-matrix audit of the generic prepared QuietClock family."""
import argparse,itertools,json,time
from pathlib import Path
from research.clock_selection.audit import Snapshot,DIRECTIONS,coupling,load,file_digest,ROOT,audit_record,all_events,canonical
SHA='a0198c4f4e79c1c1afe6ecd34620ec49615e338152038d9cb8f16610ab04d7af'

def expected(case,t):
 L=case['side'];c=L//2;g=case['channel'];cp=coupling(tuple(case['signs']));a,b=case['a'],case['b'];phase=t%4;ab=((a,b),(b,-a),(-a,-b),(-b,a))[phase];cells={(*[c]*3,g):(*ab,case['r'])};prefix=(0,b,b-a,-a)
 for d,delta in enumerate(DIRECTIONS):
  h=next(h for h in range(48) if cp.ports[d^1][h]==g);w=cp.weights[d^1][h];allowed=[r for r in range(6) if r%2==case['parity'] and all(0<=r+2*w*s<6 for s in prefix)];r=min(allowed,key=lambda r:(abs(r-2),-r));address=tuple(c+delta[j] for j in range(3))+(h,);cells[address]=(0,0,r+2*w*prefix[phase])
 return Snapshot(L,(0,0,2),cells)

def audit(study,output):
 study=Path(study);output=Path(output);assert not output.exists();start=time.process_time();report=dict(passed=False,failure=None,protocol_sha256=SHA,auditor_sha256=file_digest(__file__),records=[],parity_comparisons=[])
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==SHA==reg['protocol_sha256'];assert file_digest(study/'producer.py')==reg['producer_sha256']==file_digest(ROOT/'research/clock_selection/quiet_clock.py');assert result['status']=='completed' and result['completed_cases']==48
  for name,sha in reg['source_sha256'].items():assert file_digest(study/'source'/name)==sha==file_digest(ROOT/name)
  report['source_sha256']=reg['source_sha256'];cases=[]
  for si,signs in enumerate(itertools.product((-1,1),repeat=3)):
   for oi,(a,b) in enumerate(((0,1),(0,2),(1,1))):
    for parity in (0,1):cases.append(dict(id=f'quiet-s{si}-o{oi}-p{parity}',sign_index=si,orbit_index=oi,signs=list(signs),channel=si*6+oi,a=a,b=b,r=2+parity,parity=parity,side=5 if si%2==0 else 7))
  pairs={}
  for case,entry in zip(cases,result['cases']):
   path=study/entry['record'];assert file_digest(path)==entry['record_sha256'];record=load(path);assert record['case']==case==entry['case'];integrity,states=audit_record(record,expected_initial=expected(case,0),deadline=start+60)
   assert len(states)==9 and all(s==expected(case,t) for t,s in enumerate(states));assert states[4]==states[0] and all(states[t]!=states[0] for t in (1,2,3));assert all_events(states)[0]==[]
   center=(*[case['side']//2]*3,case['channel']);assert all(not any(v[:2]) or a==center for s in states for a,v in s.cells.items());assert all(all(0<q<s.side-1 for q in a[:3]) for s in states for a in s.cells)
   checks=dict(full_analytic_state=True,minimal_period4=True,no_guarded_C=True,only_center_counters=True,full_inverse=True,no_nonbackground_boundary_contact=True);analysis=dict(case=case,checks=checks,all_checks=True,all_world_C=[],center_trace=[list(s.at(center)) for s in states]);assert analysis==record['analysis'];assert all(entry[k]==v for k,v in analysis.items())
   # Dense boundary lists are checked by audit_record; retain counts/hashes in certificates.
   hits=integrity.pop('boundary_counter_hits');assert hits==[];integrity['boundary_counter_hit_count']=0
   report['records'].append(dict(id=entry['id'],record_sha256=file_digest(path),integrity=integrity,analysis=analysis));pairs[(case['sign_index'],case['orbit_index'],case['parity'])]=states
  for si,oi in itertools.product(range(8),range(3)):
   for a,b in zip(pairs[si,oi,0],pairs[si,oi,1]):
    addresses=a.cells.keys()|b.cells.keys();assert all(a.at(x)[:2]==b.at(x)[:2] for x in addresses);diff=[b.at(x)[2]-a.at(x)[2] for x in addresses if a.at(x)[2]!=b.at(x)[2]];assert len(diff)==7 and set(diff)=={1}
   report['parity_comparisons'].append(dict(sign_index=si,orbit_index=oi,same_counter_trace=True,seven_remainders_offset1=True))
  assert report['parity_comparisons']==result['parity_comparisons'];report.update(passed=True,states=432,transitions=384,full_rewinds=48,scope=p['claim_limits'],timing_receipt=load(study/'capture_process_time.json'))
 except Exception as exc:report['failure']=repr(exc)
 report['cpu_seconds']=time.process_time()-start;output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();r=audit(args.study,args.output);print(canonical({k:r[k] for k in ('passed','failure','cpu_seconds')}));raise SystemExit(0 if r['passed'] else 1)
