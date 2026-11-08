"""Passive post-capture clock illustration; no changed acceptance or evolution."""
from __future__ import annotations
import gzip
import hashlib
import json
from pathlib import Path
from research.clock_selection import carrier_memory as study

HERE=Path(__file__).resolve().parent

def phase_offset(trace,hold):
    lo,hi=hold;values=[]
    for t in range(lo,hi+1):
        pair=tuple(trace[t][:2]);values.append((study.PHASES.index(pair)-t)%4 if pair in study.PHASES else None)
    return values[0] if len(set(values))==1 else None

def run():
    original=HERE/'evidence/carrier_memory_v1';output=HERE/'evidence/carrier_memory_v1_illustration';output.mkdir(exist_ok=False)
    p=json.loads((original/'protocol.json').read_text());result=json.loads((original/'result.json').read_text());rows=[];bank={}
    for item in result['cases']:
        path=original/item['record'];row=json.loads(gzip.decompress(path.read_bytes()));case=row['case'];o=row['observations'];clock=o['clocks']['receiver'];c=case['side']//2;address=(c+20,c+1,c,2)
        all_events={(e['step'],tuple(e['address'])):e for e in o['all_C']};window=[]
        for update in range(70,83):
            window.append({'update':update,'before':clock['center_trace'][update-1],'after':clock['center_trace'][update],
                           **clock['center_inputs'][update-1],'native_C':all_events.get((update,address))})
        addresses=[tuple(a) for a in clock['region_addresses']]
        earliest=next((t for t in range(74,97) if study.quiet(clock['region_trace'],clock['center_trace'],clock['center_inputs'],clock['external_inputs'],addresses,address,[t,112])['passed']),None)
        summary={'case':case,'source_record':item['record'],'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                 'pre_late_effective_phase':phase_offset(clock['center_trace'],[52,60]),'terminal_effective_phase':phase_offset(clock['center_trace'],[96,112]),
                 'first_trailing_quiet_state_in_74_to_96_through112':earliest,
                 'late_receiver_updates70_to82':window,'early_upstream':o['epochs']['early'],'late_upstream':o['epochs']['late'],
                 'pre_late_full336_hold':clock['holds']['pre_late'],'terminal_full336_hold':clock['holds']['terminal']}
        rows.append(summary);bank[case['side'],case['receiver_phase'],case['control']]=clock['region_trace']
    equivalence=[]
    for side in p['family']['sides']:
        for phase in p['family']['receiver_phases']:
            traces={m:bank[side,phase,m] for m in p['family']['controls']}
            equivalence.append({'side':side,'receiver_phase':phase,'joint_equals_null_every_terminal_state':traces['11'][96:113]==traces['00'][96:113],
                'joint_equals_probe_only_every_terminal_state':traces['11'][96:113]==traces['01'][96:113],
                'writer_only_equals_null_every_terminal_state':traces['10'][96:113]==traces['00'][96:113]})
    report={'scope':'Post-capture passive illustration only. No new trajectories, thresholds or acceptance decisions. All original recorded events remain unfiltered in their source records.',
        'window_definition':'Updates70..82 inclusive are printed with exact before/after triples, u, quotient and six signed donor terms. The descriptive trailing-quiet time is the earliest start in74..96 whose entire336 region satisfies the already registered quiet predicate through state112; it does not alter primary hold96..112.',
        'protocol_sha256':hashlib.sha256((original/'protocol.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'independent_audit':'research/clock_selection/evidence/independent_audit/carrier_memory_v1.json','records':rows,'terminal_equivalence':equivalence}
    study.write_json(output/'illustration.json',report);return report

if __name__=='__main__':
    data=run()
    for row in data['records']:
        if row['case']['side']==393:
            print(row['case']['receiver_phase'],row['case']['control'],row['pre_late_effective_phase'],row['terminal_effective_phase'],row['first_trailing_quiet_state_in_74_to_96_through112'])
