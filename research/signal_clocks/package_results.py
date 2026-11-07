"""Create a generic presentation descriptor for all retained study types."""
import argparse
import hashlib
import json
import os
from pathlib import Path

from .build_presenter import package
from .run import write_json


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compose(evidence,descriptor):
    evidence=Path(evidence).resolve();descriptor=Path(descriptor).resolve()
    root=descriptor.parent;cases=[]
    def reference(path):
        return {'path':os.path.relpath(path,root),'sha256':sha(path)}
    for group in ('endpoint_toggle','records'):
        original=evidence/group/'presentation.json';data=json.loads(original.read_text())
        for c in data['cases']:
            entry=dict(c)
            path=original.parent/c['trace'];entry['trace']=os.path.relpath(path,root)
            entry['protocol']=reference(original.parent/data['protocol']['path'])
            if group=='endpoint_toggle':
                entry['title']=('Two signals, two ticks: finite toggle' if c['id'].endswith('s11') else 'Toggle control: '+c['title'])
                entry['description']='Exploratory endpoint-064: two guarded bank ticks at 12 and 22, with a record that toggles back. The registered three-distinct-record and second-arrival-window criteria failed. Full controls and every microscopic state are retained.'
            cases.append(entry)
    period=evidence/'period_control';period_result=json.loads((period/'result.json').read_text())
    period_protocol=json.loads((period/'protocol.json').read_text())
    for result,case in zip(period_result['cases'],period_protocol['cases']):
        folder=period/'cases'/case['id'];o=case['side']//2;g=case['channel']
        cases.append({'id':case['id'],'title':'Period-four motion, zero arithmetic clicks'+(' (signed tensor)' if g==47 else ''),
            'description':'A single initially prepared unit counter and its retained remainder halo recur exactly every four board updates. No guarded arithmetic C event occurs anywhere. This is the proved microscopic-motion control, not an arrival-triggered physical light clock.',
            'trace':os.path.relpath(folder/'states.jsonl',root),'trace_sha256':sha(folder/'states.jsonl'),
            'protocol':reference(period/'protocol.json'),'readouts':[],
            'view':{'position':[o,o,o],'channel':g}})
    cooperation=evidence/'cooperation';manifest=json.loads((cooperation/'candidate_manifest.json').read_text())
    outcomes={c['id']:c for c in json.loads((cooperation/'result.json').read_text())['comparisons']}
    for case in manifest['cases']:
        path=cooperation/'cases'/case['id']/'states.jsonl';o=case['side']//2
        readouts=[]
        for sign,label in ((-1,'Left'),(1,'Right')):
            for v in (0,2,4):
                readouts.append({'id':f'memory-{sign}-{v}','label':f'{label} memory pair ({v}, {v})','kind':'all_equal',
                    'clauses':[{'address':[o+sign*j,o,o,0],'component':'r','equals':str(v)} for j in (2,3)]})
            readouts.append({'id':f'quiet-{sign}','label':f'{label} outlet: every b counter zero','kind':'all_equal',
                'clauses':[{'address':[o+sign*6,o,o,g],'component':'b','equals':'0'} for g in range(48)]})
        comparison=outcomes.get(case['id']);detail=(f" Calibrated left/right K={comparison['scores']}; held-out result: {comparison['category']}." if comparison else '')
        cases.append({'id':case['id'],'title':f"Cooperation {case['kind']}: {case['id']}",
            'description':'Matched initial remainder preparations under one fixed tensor. All 48 outlet channels and the full three-dimensional state are retained; the score never controls evolution.'+detail,
            'trace':os.path.relpath(path,root),'trace_sha256':sha(path),
            'protocol':reference(cooperation/'protocol.json'),'readouts':readouts,
            'view':{'position':[o-6,o,o],'channel':14}})
    # Explanatory ordering changes only presentation metadata, never selection
    # of scientific runs or acceptance criteria. All 54 cooperation runs remain.
    front=['endpoint-064-s11','endpoint-064-s00','endpoint-064-s10','endpoint-064-s01',
           'joint-0-2-P1','period-four-positive']
    order={identifier:i for i,identifier in enumerate(front)}
    cases.sort(key=lambda c:order.get(c['id'],len(front)))
    if len(cases)!=64 or len({c['id'] for c in cases})!=64:
        raise ValueError('Expected exactly 64 distinct retained reference experiments')
    data={'format':'universe24-signal-clock-presentation-v1',
          'title':'Signal clocks: constructions, controls and limits',
          'protocol':reference(evidence/'training/protocol.json'),'cases':cases,
          'scope':'All54cooperationruns, fourprimarycontrols, fourexploratoryendpointtogglecontrols, twoperiodcontrols. Originalacceptancefailuresunchanged.'}
    write_json(descriptor,data);return descriptor


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence',required=True,type=Path)
    parser.add_argument('--descriptor',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();path=compose(args.evidence,args.descriptor)
    print(package(path,args.output))


if __name__=='__main__':
    main()
