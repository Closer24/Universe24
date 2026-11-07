"""Retain complete closed-board controls selected by the frozen search policy."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import time

from .run import run_case, write_json
from .search import MASKS, group_verdict, source_hashes


def retain(training, output, candidate_id=None):
    training=Path(training).resolve();output=Path(output).resolve()
    selected=json.loads((training/'selected_preparation.json').read_text())
    if candidate_id is not None:
        candidates=json.loads((training/'search_results.json').read_text())['candidates']
        found=next((c for c in candidates if c['case']['id']==candidate_id),None)
        if found is None:
            raise ValueError('Exploratory example must be a completed registered candidate')
        selected={'case':found['case'],'selection_reason':'Post-search exploratory example selected for inspection; registered acceptance is unchanged.',
                  'training_guarded_pass':found['verdict']['guarded_click_criteria_passed']}
    case=selected['case']
    if case is None:
        raise ValueError('No completed candidate is available to retain')
    protocol=json.loads((training/'protocol.json').read_text())
    output.mkdir(parents=True,exist_ok=False)
    available=protocol['budgets']['confirmation_cpu_seconds']
    if not isinstance(available,(int,float)):
        used=json.loads((training/'search_results.json').read_text())['summary']['cpu_seconds']
        available=protocol['budgets']['combined_search_and_confirmation_cpu_seconds']-used
    if available<=0:
        raise TimeoutError('No registered confirmation budget remains')
    started=time.process_time();deadline=started+available
    runs={};entries=[]
    for mask in MASKS:
        identifier=f'{case["id"]}-s{int(mask[0])}{int(mask[1])}'
        folder=output/'cases'/identifier
        result=run_case(case,mask,deadline_cpu=deadline,
            max_cells=protocol['budgets']['maximum_stored_channels_per_state'],
            audit=True,output=folder)
        runs[mask]=result
        target=result['locations']['detector']
        readouts=[{'id':f'memory-{a}-{b}','label':f'Memory ({a}, {b})','kind':'all_equal',
                   'clauses':[{'address':target[0],'component':'r','equals':str(a)},
                              {'address':target[1],'component':'r','equals':str(b)}]}
                  for a in (0,2,4) for b in (0,2,4)]
        label={(False,False):'No source: stationary control',
               (True,False):'First source only',
               (False,True):'Second source only',
               (True,True):'Two initial sources: registered criterion fails'}[mask]
        trace=folder/'states.jsonl'
        entries.append({'id':identifier,'title':label,
            'description':'Frozen candidate '+case['id']+'. All disturbances were prepared at step zero. Every remainder change is retained; arithmetic C events keep their original guard. This candidate does not establish a two-arrival waiting component.',
            'trace':str(trace.relative_to(output)),
            'trace_sha256':hashlib.sha256(trace.read_bytes()).hexdigest(),
            'readouts':readouts,'view':{'position':target[0][:3],'channel':target[0][3]}})
    verdict=group_verdict(case,runs)
    summary={'selection':selected,'verdict':verdict,
        'scope':'Exact retained training controls; no failed candidate is promoted to a confirmed component.',
        'cpu_seconds':time.process_time()-started,'source_sha256':source_hashes(),
        'retainer_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'trace_count':len(entries),'complete_frames':sum(len(r['trace']) for r in runs.values()),
        'forward_transitions':sum(r['preparation']['steps'] for r in runs.values()),
        'fresh_holdouts_executed':False,'reason_no_holdouts':'Training did not pass the frozen milestone.' if not selected['training_guarded_pass'] else 'This exporter only retains training controls; confirmation must be reported separately.'}
    write_json(output/'result.json',summary)
    protocol_path=training/'protocol.json'
    import os
    descriptor={'format':'universe24-signal-clock-presentation-v1',
        'title':'Signal clocks: registered construction tests',
        'protocol':{'path':os.path.relpath(protocol_path,output),
                    'sha256':hashlib.sha256(protocol_path.read_bytes()).hexdigest()},
        'cases':entries}
    write_json(output/'presentation.json',descriptor)
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--training',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--candidate',help='Explicit post-search example; never changes registered acceptance')
    args=parser.parse_args()
    print(json.dumps(retain(args.training,args.output,args.candidate),indent=2))


if __name__=='__main__':
    main()
