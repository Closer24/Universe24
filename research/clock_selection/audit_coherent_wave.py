"""Independent all-channel replay and integer/interval wave comparison audit."""
from __future__ import annotations
import argparse,gc,gzip,hashlib,itertools,json,math,time
from pathlib import Path
from research.clock_selection.audit import Snapshot,load,file_digest,ROOT,audit_record,all_events,canonical
SHA='c027015b1ecfa2f157ef2f54fb9564c21a507f055d287189f6d215d3447e44f0'

def neighbors(field,L):
 return {x:sum(field[tuple((x[j]+d if j==axis else x[j])%L for j in range(3))] for axis in range(3) for d in (-1,1)) for x in field}

def audit(study,output,budget=900):
 import mpmath as mp
 mp.mp.dps=160;mp.iv.dps=120;iv=mp.iv
 study=Path(study);output=Path(output);assert not output.exists();start=time.process_time();report=dict(passed=False,failure=None,protocol_sha256=SHA,auditor_sha256=file_digest(__file__),records=[],cpu_budget_seconds=budget)
 try:
  p,result,reg=[load(study/f) for f in ('protocol.json','result.json','registration.json')];assert file_digest(study/'protocol.json')==SHA==reg['protocol_sha256'];assert result['status']=='completed' and result['completed_cases']==16
  for name,sha in reg['source_sha256'].items():assert file_digest(study/'source_provenance/source'/name)==sha==file_digest(ROOT/name)
  dep=load(study/'dependency_provenance/manifest.json');assert dep['version']==mp.__version__=='1.3.0' and dep['backend']==mp.libmp.BACKEND=='python'
  for name,sha in dep['source_sha256'].items():assert file_digest(study/'dependency_provenance/mpmath'/name)==sha==file_digest(Path(mp.__file__).parent/name)
  report['source_sha256']=reg['source_sha256'];report['dependency_manifest_sha256']=file_digest(study/'dependency_provenance/manifest.json')
  cases=[dict(id=f'coherent-L{L}-n{"".join(map(str,n))}-N{N}',side=L,n=list(n),amplitude=N) for L,n,N in itertools.product((7,9),((1,0,0),(1,1,0),(1,1,1),(2,0,0)),(1000,100000))];assert reg['cases']==cases
  for case,entry in zip(cases,result['cases']):
   assert entry['case']==case;path=study/entry['record'];raw=gzip.decompress(path.read_bytes());assert hashlib.sha256(raw).hexdigest()==entry['record_sha256'] and file_digest(path)==entry['record_gzip_sha256'];row=json.loads(raw);assert row['case']==case;L,N,n=case['side'],case['amplitude'],case['n'];sites=list(itertools.product(range(L),repeat=3));gamma=sum(iv.cos(2*iv.pi*q/L) for q in n)/3;omega=iv.atan2(iv.sqrt(1-gamma**2),gamma);profile=[]
   endpoint=lambda x:mp.mpf(x)
   for phase in range(L):
    phi=2*iv.pi*phase/L;aa=N*iv.cos(phi+omega);bb=N*iv.cos(phi);values=[]
    witness=row['rounding_certificate']['phase_classes'][phase]
    for label,value in (('a',aa),('b',bb)):
     lo,hi=endpoint(value.a),endpoint(value.b);a=int(mp.floor(lo+mp.mpf('.5')));b=int(mp.floor(hi+mp.mpf('.5')));assert a==b==witness[label]
     plo,phi=map(mp.mpf,witness[label+'_scaled_interval']);assert plo<=lo<=hi<=phi;values.append(a)
    profile.append((*values,2))
   seed=Snapshot(L,(0,0,2),{(*xyz,g):profile[sum(n[j]*xyz[j] for j in range(3))%L] for xyz in sites for g in range(48)})
   integrity,states=audit_record({k:v for k,v in row.items() if k!='observations'},expected_initial=seed,deadline=start+budget);obs=row['observations'];assert len(states)==13 and entry['frames']==13 and entry['transitions']==12
   w={xyz:seed.at((*xyz,0))[1] for xyz in sites};old_a={xyz:seed.at((*xyz,0))[0] for xyz in sites};wprev=None;checked=[];Q=[]
   for t,state in enumerate(states):
    field={xyz:state.at((*xyz,0)) for xyz in sites};coherent=all(state.at((*xyz,g))==field[xyz] for xyz in sites for g in range(48));assert coherent;assert all(v[2]%2==0 for v in state.cells.values());Q.append(str(sum(6*(v[1]-v[0])+v[2]-2 for v in state.cells.values())))
    numerator=sum((3**t*field[xyz][1]-w[xyz])**2 for xyz in sites);bound=0 if t==0 else L**3*t*t*(t+1)**2*3**(2*t-2);assert numerator<=bound
    target=[iv.cos(2*iv.pi*phase/L-t*omega) for phase in range(L)];residual=sum((iv.mpf(field[xyz][1])/N-target[sum(n[j]*xyz[j] for j in range(3))%L])**2 for xyz in sites);rms=iv.sqrt(residual/(L**3));lo,hi=endpoint(rms.a),endpoint(rms.b);envelope=mp.mpf(2*t+1)/(2*N)+mp.mpf(t*(t+1))/(3*N);assert hi<=envelope+mp.mpf('1e-50')
    saved=obs['frames'][t];assert saved['step']==t and saved['all48_coherent'] and saved['exact_equation'] and saved['exact_rounded_initial_bound_pass'] and saved['ideal_mode_bound_pass'];assert saved['rounded_initial_error_squared_numerator']==str(numerator) and saved['exact_bound_numerator']==str(bound)
    slo,shi=map(mp.mpf,saved['ideal_mode_RMS_interval']);assert slo<=lo<=hi<=shi,('reported interval',case['id'],t)
    assert abs(mp.mpf(saved['ideal_mode_envelope'])-envelope)<mp.mpf('1e-85') and saved['fixed_numerical_slack']=='1e-50'
    actual_rms=math.sqrt(numerator/(L**3))/(N*3**t);assert math.isclose(saved['rounded_initial_RMS'],actual_rms,rel_tol=1e-14,abs_tol=1e-20);assert saved['rounded_initial_envelope']==t*(t+1)/(3*N)
    if t:
     before={xyz:states[t-1].at((*xyz,0)) for xyz in sites};a=neighbors({xyz:v[1] for xyz,v in before.items()},L);assert all(6*(field[x][1]+before[x][0])==2*a[x]+before[x][2]-field[x][2] for x in sites)
    checked.append(dict(step=t,exact_error_numerator=str(numerator),exact_bound=str(bound),independent_ideal_interval=[mp.nstr(lo,125),mp.nstr(hi,125)],all48_equal=True))
    if t<12:
     aw=neighbors(w,L);nxt={x:aw[x]-3*old_a[x] if t==0 else aw[x]-9*wprev[x] for x in sites};wprev,w=w,nxt
   events=[[e['step'],*e['address'],e['kind'],e['quotient']] for e in all_events(states)[0]];assert events==obs['all_C'];counts={str(k):sum(e[5]==k for e in events) for k in range(3)};assert counts==obs['all_C_counts']==entry['all_C_counts'];assert Q==obs['Q_trace'] and len(set(Q))==1
   assert all(obs[k] for k in ('all48_coherent','exact_reduced_equation','remainder_parity_preserved','all_rounded_initial_bounds','all_ideal_mode_bounds','Q_conserved'));assert entry['accepted_comparison'] and entry['full_state_inverse'];assert entry['complete_sparse_rows']==sum(len(s.cells) for s in states)
   if 'native' in entry:
    bundle=load(study/entry['native']);assert file_digest(study/entry['native'])==entry['native_sha256'] and bundle['experiments']==[row['experiment']]
   report['records'].append(dict(id=entry['id'],record_sha256=file_digest(path),integrity=integrity,frames=checked,raw_C_counts=counts));print(canonical(dict(audited=len(report['records']),total=16)),flush=True)
   del row,states,events,raw;gc.collect()
  receipt=load(study/'budget_receipt.json');assert receipt['cpu_overrun']==max(0,result['cpu_seconds']-300);report['producer_budget_receipt']=receipt;report['producer_cpu_seconds']=result['cpu_seconds'];report['producer_resource_contract_passed']=not any(receipt[k] for k in ('cpu_overrun','wall_overrun','byte_overrun'))
  report.update(passed=True,states=sum(r['integrity']['states'] for r in report['records']),transitions=sum(r['integrity']['forward_transitions'] for r in report['records']),full_rewinds=16,scope=p['scope_limits'],interval_oracle='Independent120-digit direct phase cosine, versus producer80-digit recurrence; exact integer RMS bound checked separately.')
 except Exception as exc:report['failure']=repr(exc)
 report['cpu_seconds']=time.process_time()-start;output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');return report

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);ap.add_argument('--max-cpu-seconds',type=float,default=900);args=ap.parse_args();r=audit(args.study,args.output,args.max_cpu_seconds);print(canonical({k:r[k] for k in ('passed','failure','cpu_seconds')}));raise SystemExit(0 if r['passed'] else 1)
