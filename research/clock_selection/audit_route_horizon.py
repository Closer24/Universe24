"""Passive horizon extension check on audited bare route controls."""
import json
from pathlib import Path
from research.clock_selection.audit import ROOT,load,file_digest,all_events
from research.staged_blocks.audit import read_states

def main():
 study=ROOT/'research/clock_selection/evidence/route_clock_v1';certificate=ROOT/'research/clock_selection/evidence/independent_audit/route_clock_v1.json';assert load(certificate)['passed'];result=load(study/'result.json');by={r['id']:r for r in result['cases']};rows=[]
 for entry in result['cases']:
  if '-bare-' not in entry['id'] or not entry['id'].endswith('-s1'):continue
  offentry=by[entry['id'][:-1]+'0'];on=load(study/entry['record']);off=load(study/offentry['record']);assert file_digest(study/entry['record'])==entry['sha256'];assert file_digest(study/offentry['record'])==offentry['sha256'];a,b=read_states(on['experiment']),read_states(off['experiment']);case=on['case'];c=case['side']//2;d=-1 if case['patterns'][0]=='NO' else 1;node=(c+8*d,c,c);trace=[[list(s.at((*node,g))) for g in range(48)] for s in a];null=[[list(s.at((*node,g))) for g in range(48)] for s in b];first=next((t for t in range(81) if trace[t]!=null[t]),None);first_counter=next((t for t in range(81) if any(any(v[:2]) for v in trace[t])),None);assert first==first_counter==60
  events=[e for e in all_events(a)[0] if tuple(e['address'][:3])==node]
  rows.append(dict(id=entry['id'],source_on_record_sha256=entry['sha256'],source_off_record_sha256=offentry['sha256'],NO_outlet=list(node),equal_to_full48_null_through=59,first_full48_departure=first,first_nonzero_counter=first_counter,prior_full48=trace[59],first_active_full48=trace[60],all_outlet_C=events))
 assert len(rows)==4
 out=certificate.with_name('route_horizon_extension.json');data=dict(passed=True,auditor_sha256=file_digest(__file__),parent_certificate_sha256=file_digest(certificate),new_trajectories=0,new_forward_inverse_steps=0,comparisons=rows,scope='Newly audited bare boards extend the observation horizon. The prior finite OR/NO competition window remains valid; permanent NO-route cancellation is not established and fails in these preparations by update60.')
 with out.open('x') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(dict(passed=True,comparisons=4,first_NO_counter=60)))
if __name__=='__main__':main()
