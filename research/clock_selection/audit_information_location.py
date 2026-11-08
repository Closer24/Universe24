"""Passive independent verification of where the two V2 histories differ."""
import gzip,hashlib,json
from pathlib import Path
from research.clock_selection.audit import ROOT,DIRECTIONS,load,file_digest,native_digest
from research.staged_blocks.audit import read_states

def main():
 source=ROOT/'research/clock_selection/evidence/phase_record_information_location.json';p=load(source);assert file_digest(source)=='a93651f2ae72b550c23e8682ac06abe82947dec3a565bd6ce5a77d12fae5311d';assert file_digest(ROOT/p['source_result'])==p['source_result_sha256'];states={}
 for row in p['input_records']:
  path=ROOT/row['record'];raw=gzip.decompress(path.read_bytes());assert file_digest(path)==row['record_gzip_sha256'] and hashlib.sha256(raw).hexdigest()==row['record_sha256'];r=json.loads(raw);states[row['control']]=read_states(r['experiment']);assert native_digest(states[row['control']][0])==row['initial_state_sha256'];assert native_digest(states[row['control']][-1])==row['final_state_sha256']
 center=(168,169,168);nodes=(center,*(tuple(center[j]+delta[j] for j in range(3)) for delta in DIRECTIONS));region={(*n,g) for n in nodes for g in range(48)};assert set(map(tuple,p['region']['addresses']))==region and len(region)==336
 rows=[]
 for t in (40,61,88):
  a,b=states['01'][t],states['11'][t];assert a.background==b.background
  diffs=[dict(address=list(x),control_01=list(a.at(x)),control_11=list(b.at(x)),inside_clock_region=x in region) for x in sorted(a.cells.keys()|b.cells.keys()) if a.at(x)!=b.at(x)];inside=[d for d in diffs if d['inside_clock_region']];outside=[d for d in diffs if not d['inside_clock_region']];counter=sum(d['control_01'][:2]!=d['control_11'][:2] for d in diffs)
  row=dict(state=t,all_differences=diffs,center_equal=a.at((*center,2))==b.at((*center,2)),different_counter_pairs=counter,differing_triples=len(diffs),full_336_region_equal=not inside,inside_region_differing_triples=len(inside),outside_region_differing_triples=len(outside),remainder_only_differences=len(diffs)-counter,outside_difference_bounds_xyz=[[min(d['address'][j] for d in outside),max(d['address'][j] for d in outside)] for j in range(3)])
  assert row==p['observations'][len(rows)];rows.append({k:v for k,v in row.items() if k!='all_differences'})
 out=source.parent/'independent_audit/phase_record_information_location.json';report=dict(passed=True,auditor_sha256=file_digest(__file__),source_sha256=file_digest(source),input_records=p['input_records'],new_trajectories=0,new_forward_inverse_steps=0,observations=rows,scope=p['scope'])
 with out.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(dict(passed=True,observations=rows)))
if __name__=='__main__':main()
