"""Closed-board demonstration of the proved period-four, zero-click motif."""
import argparse
import hashlib
import json
from pathlib import Path
import time

from universe24 import Channel,Coupling,Cube,Engine,State
from universe24.observation.clicks import clicks
from .complexity_study import states_from
from .run import run_case,write_json


def prepare_single(case,mask):
    origin=(case['side']//2,)*3
    engine=Engine(Coupling(tuple(case['body_signs'])))
    address=(*origin,case['channel'])
    state=State(Cube(case['side']),Channel(0,0,2),
                {address:Channel(0,1 if mask[0] else 0,2)})
    return engine,state,{'origin':origin,'sources':[origin],
        'detector':[address,(*origin,(case['channel']+1)%48)]}


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    cases=[{'id':'period-four-positive','side':41,'steps':16,'body_signs':[1,1,1],'channel':0},
           {'id':'period-four-signed','side':41,'steps':16,'body_signs':[-1,1,-1],'channel':47}]
    protocol={'format':'universe24-period-control-v1','question':'Does the proved single-unit motif have full-state period four and zero guarded arithmetic events?',
        'cases':cases,'fixed_checks':['all complete states repeat at offset4','steps1,2,3 differ frominitial','zero global guarded arithmetic events','fullstate inverse and rewind'],
        'scope':'Demonstration of the algebra proof, not a two-arrival waiting component or physical light clock.',
        'budget_cpu_seconds':30}
    write_json(output/'protocol.json',protocol);started=time.process_time();results=[]
    for case in cases:
        folder=output/'cases'/case['id']
        result=run_case(case,(True,),deadline_cpu=started+30,audit=True,output=folder,prepare_function=prepare_single)
        states=states_from(folder/'states.jsonl')
        checks={'exact_period_four':all(states[t]==states[t-4] for t in range(4,len(states))),
                'no_smaller_positive_period':all(states[t]!=states[0] for t in (1,2,3)),
                'zero_global_guarded_clicks':all(not list(clicks(a,b,t)) for t,(a,b) in enumerate(zip(states,states[1:]),1)),
                'full_one_step_inverses':result['all_one_step_inverses'],
                'complete_rewind':result['complete_rewind']}
        results.append({'id':case['id'],'checks':checks,'passed':all(checks.values()),
                        'complete_frames':len(states),'trace_sha256':hashlib.sha256((folder/'states.jsonl').read_bytes()).hexdigest()})
    report={'cases':results,'passed':all(r['passed'] for r in results),
            'cpu_seconds':time.process_time()-started,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'physical_validation':False}
    write_json(output/'result.json',report);return report


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(run(args.output),indent=2))


if __name__=='__main__':
    main()
