"""Independent readback of the explicitly exploratory cubic-region scan."""
import gzip,hashlib,itertools,json,time
from research.clock_selection.audit import ROOT,DIRECTIONS,coupling,load,file_digest
from research.staged_blocks.audit import read_states


def audit():
 start=time.process_time();study=ROOT/'research/clock_selection/evidence/activation_multinode_exploration';d=load(study/'result.json');p=load(study/'protocol.json');assert file_digest(study/'protocol.json')==d['protocol_sha256']=='a4da64c86fa13e6bd1fc06d26d6f218d4d7822049f75fe0c8efab783b033d3e5';assert file_digest(study/'executed_analysis.py')==d['analysis_sha256'];cp=coupling((1,1,1));inv=[{g:h for h,g in enumerate(row)} for row in cp.ports];regions=[];tests=[]
 for source in d['source_records']:
  path=ROOT/source['record'];raw=gzip.decompress(path.read_bytes());assert file_digest(path)==source['record_gzip_sha256'] and hashlib.sha256(raw).hexdigest()==source['record_sha256'];record=json.loads(raw);states=read_states(record['experiment']);L=record['case']['side'];c=L//2;center=(c,c+1,c)
  for radius in (1,2,3):
   addresses=[(*xyz,g) for xyz in itertools.product(*(range(q-radius,q+radius+1) for q in center)) for g in range(48)];nodes={a[:3] for a in addresses};frames=[[s.at(a) for a in addresses] for s in states[32:81]];activity=[sum(any(v[:2]) for v in row) for row in frames];counts=[];first=None
   for t in range(32,80):
    ext=[]
    for a,v in sorted(states[t].cells.items()):
     if not v[1] or a[:3] in nodes:continue
     for direction,delta in enumerate(DIRECTIONS):
      node=tuple((a[j]+delta[j])%L for j in range(3))
      if node in nodes:
       g=inv[direction^1][a[3]];ext.append(dict(update=t+1,source=list(a),target=[*node,g],term=cp.weights[direction^1][g]*v[1]))
    counts.append(len(ext))
    if first is None and ext:first=ext[0]
   identity=source['id']+'-R'+str(radius);active=all(activity);isolated=not any(counts);regions.append(dict(id=identity,source_case=source['id'],radius=radius,center=list(center),complete_nodes=len(nodes),complete_triples=len(addresses),nonzero_counter_counts=activity,external_nonzero_term_counts=counts,first_external_term=first,active_every_state=active,isolated_all_updates=isolated))
   for period in range(1,17):
    mismatch=None
    for k in range(49-period):
     if frames[k]!=frames[k+period]:
      j=next(j for j in range(len(addresses)) if frames[k][j]!=frames[k+period][j]);mismatch=dict(state=32+k,compared_state=32+k+period,address=list(addresses[j]),before=list(frames[k][j]),after=list(frames[k+period][j]));break
    tests.append(dict(region=identity,period=period,at_least_three_periods=48//period>=3,full_region_periodic=mismatch is None,first_mismatch=mismatch,active_every_state=active,isolated_all_updates=isolated,discovery_candidate=48//period>=3 and mismatch is None and active and isolated))
 assert regions==d['regions'] and tests==d['tests'];assert d['discovery_candidates']==0 and d['test_count']==len(tests)==96 and d['new_evolution_updates']==0;out=dict(passed=True,auditor_sha256=file_digest(__file__),protocol_sha256=d['protocol_sha256'],result_sha256=file_digest(study/'result.json'),source_records=d['source_records'],regions_checked=6,period_tests_checked=96,discovery_candidates=0,new_evolution_updates=0,post_capture_exploratory=True,original_activation_verdict_unchanged=True,external_nonzero_update_counts=[sum(n>0 for n in r['external_nonzero_term_counts']) for r in regions],cpu_seconds=time.process_time()-start);dest=ROOT/'research/clock_selection/evidence/independent_audit/activation_multinode_exploration.json'
 with dest.open('x') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(out))
if __name__=='__main__':audit()
