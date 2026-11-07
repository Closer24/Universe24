"""Package the 44 prospective interface/control runs with the same Presenter."""
import argparse
import hashlib
import json
import os
from pathlib import Path

from universe24.experiments.config import from_dict
from .build_presenter import package
from .run import write_json


def compose(evidence,descriptor):
    evidence=Path(evidence).resolve();descriptor=Path(descriptor).resolve();root=descriptor.parent
    def ref(path):return {'path':os.path.relpath(path,root),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    cases=[]
    original=evidence/'toggle_confirmation/presentation_verified.json';data=json.loads(original.read_text())
    for c in data['cases']:
        entry=dict(c);entry['trace']=os.path.relpath(original.parent/c['trace'],root)
        entry['description']=entry['description'].replace('step40','step 40')
        entry['protocol']=ref(original.parent/data['protocol']['path']);entry['registered_protocol']=dict(entry['protocol']);cases.append(entry)
    for group in('counter_memory','paired_blocker'):
        directory=evidence/group;manifest=json.loads((directory/'candidate_manifest.json').read_text())
        items=manifest['runs']if group=='counter_memory'else manifest['cases']
        for item in items:
            case=item['case']if group=='counter_memory'else item
            identifier=item['id'];trace=directory/'cases'/identifier/'states.jsonl'
            first=json.loads(trace.read_text().splitlines()[0]);state=from_dict(first['experiment']).initial
            o=case['side']//2;readouts=[]
            if group=='counter_memory':
                for a,b in((4,0),(0,4)):
                    readouts.append({'id':f'remainder-{a}-{b}','label':f'Remainder pair ({a}, {b})','kind':'all_equal',
                        'clauses':[{'address':[o,o,o,0],'component':'r','equals':str(a)},
                                   {'address':[o,o,o,14],'component':'r','equals':str(b)}]})
                for a,b in((0,0),(1,0),(0,1),(-1,0),(0,-1),(2,0),(0,2),(-2,0),(0,-2)):
                    level=a*a+b*b
                    readouts.append({'id':f'magnitude-phase-{a}-{b}','label':f'I={level}, phase ({a}, {b})','kind':'all_equal',
                        'clauses':[{'address':[o,o,o,0],'component':'a','equals':str(a)},
                                   {'address':[o,o,o,0],'component':'b','equals':str(b)}]})
                source_label={(False,False):'no source',(True,False):'first source only',
                              (False,True):'second source only',(True,True):'both sources'}[tuple(item['mask'])]
                title=f'Counter memory {abs(case["source_offsets"][0])} / {case["source_offsets"][1]}: {source_label}'
                description='Prospectively registered counter memory on a fresh preparation. Each detector I = a² + b² has levels 0, 1 and 4 when both sources are present, with all source-removal controls included. I is an exact state function, not physical energy. The clock hand shows normalized direction: use exact counters or fixed phase predicates to distinguish magnitudes. The earlier remainder-only milestone remains failed.'
                position=[o,o,o]
            else:
                for sign,label in((-1,'Left'),(1,'Right')):
                    pos=(o+6*sign,o,o);clauses=[]
                    for g in range(48):
                        for component,value in zip(('a','b','r'),state.at((*pos,g))):
                            clauses.append({'address':[*pos,g],'component':component,'equals':str(value)})
                    readouts.append({'id':f'baseline-outlet-{sign}','label':f'{label}: all 48 channel triples equal initial outlet','kind':'all_equal','clauses':clauses})
                names={'O':'open','N':'neutral','R':'reversed'}
                if case['kind']=='isolated':
                    side='left'if case['isolated_side']<0 else'right'
                    label=case['variants'][0 if case['isolated_side']<0 else 1]
                    title=f'Isolated {side} arm: {names[label]}'
                else:
                    title=f'Prepared transfer: {names[case["variants"][0]]} left, {names[case["variants"][1]]} right; '+('source on'if case['source_present']else'no source')
                description='The tensor is fixed; only initial remainder pairs differ. All 48 complete outlet triples are compared with source-absent controls over steps 6 through 40. The open preparation transmits, and the neutral preparation meets the registered complete-outlet blocking criterion in nominal isolated and joint placements. This is a prepared blocker; an autonomously written router and path-erasing cancellation have not been demonstrated.'
                position=[o-6,o,o]
            protocol=ref(directory/'protocol.json')
            cases.append({'id':identifier,'title':title,'description':description,'trace':os.path.relpath(trace,root),
                'trace_sha256':hashlib.sha256(trace.read_bytes()).hexdigest(),'protocol':protocol,
                'registered_protocol':dict(protocol),'readouts':readouts,'view':{'position':position,'channel':0}})
    priority=['counter-memory-20-28-s11','counter-memory-20-32-s11','paired-O-N-s1','paired-N-O-s1','toggle-16-24-s11']
    rank={key:i for i,key in enumerate(priority)};cases.sort(key=lambda c:rank.get(c['id'],len(rank)))
    if len(cases)!=44 or len({c['id']for c in cases})!=44:raise ValueError('Expected all44distinctprospectiveruns')
    write_json(descriptor,{'format':'universe24-signal-clock-presentation-v1',
        'title':'Signal-triggered records and prepared transfer interfaces',
        'protocol':cases[0]['protocol'],'cases':cases})
    return descriptor


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence',required=True,type=Path);parser.add_argument('--descriptor',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    print(package(compose(args.evidence,args.descriptor),args.output))
