"""Frozen all-channel test of prepared paired-memory open/block interfaces."""
import argparse
import hashlib
import json
from pathlib import Path
import time

from universe24 import Channel,Coupling,Cube,Engine,State
from .complexity_study import states_from,cancellation_witnesses
from .run import run_case,write_json,canonical
from .search import source_hashes

HERE=Path(__file__).resolve().parent
PAIRS={'O':(4,0),'N':(2,2),'R':(0,4)}


def prepare_paired(case,mask):
    o=(case['side']//2,)*3;cells={}
    for sign,label in zip((-1,1),case['variants']):
        if case.get('isolated_side')is not None and sign!=case['isolated_side']:continue
        for j in range(1,7):
            pair=PAIRS[label]if j in(2,3)else PAIRS['O']
            for g,r in zip((0,14),pair):cells[(o[0]+sign*j,o[1],o[2],g)]=Channel(0,0,r)
    cells[(*o,0)]=Channel(0,1 if mask[0]else 0,2)
    cells[(*o,14)]=Channel(0,-1 if mask[0]else 0,2)
    return Engine(Coupling((1,1,1))),State(Cube(case['side']),Channel(0,0,2),cells),{
        'origin':o,'sources':[o],'detector':[(*o,0),(*o,14)],
        'outlets':[(o[0]-6,o[1],o[2]),(o[0]+6,o[1],o[2])]}


def outlet_report(states,baseline,sign):
    o=states[0].cube.side//2;pos=(o+sign*6,o,o);first=None;deltas=[]
    for t in range(6,41):
        row=[]
        for g in range(48):
            value=states[t].at((*pos,g));base=baseline[t].at((*pos,g));delta=[a-b for a,b in zip(value,base)];row.append(delta)
            if first is None and any(delta):
                component=next(i for i,v in enumerate(delta)if v)
                first={'step':t,'channel':g,'component':'abr'[component],
                       'difference':delta[component],'actual':list(value),'baseline':list(base)}
        deltas.append(row)
    counter=any(row[g][1]for row in deltas for g in range(48))
    return {'counter_transmission':counter,'weak_b_block':not counter,
            'strong_complete_outlet_block':first is None,'first_leak':first,
            'window':[6,40],'all_48_delta_triples':deltas}


def execute(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    path=HERE/'paired_blocker_protocol.json';raw=path.read_bytes();protocol=json.loads(raw)
    with(output/'protocol.json').open('xb')as f:f.write(raw)
    cases=[]
    for left,right in protocol['preparations']['joint_ordered_variant_pairs']:
        for present in(True,False):
            cases.append({'id':f'paired-{left}-{right}-s{int(present)}','kind':'joint',
                'side':101,'steps':40,'variants':[left,right],'source_present':present})
    for sign in(-1,1):
        for label in('O','N','R'):
            variants=['O','O'];variants[0 if sign<0 else 1]=label
            cases.append({'id':f'paired-isolated-{sign}-{label}','kind':'isolated',
                'side':101,'steps':40,'variants':variants,'isolated_side':sign,
                'source_present':True})
    write_json(output/'candidate_manifest.json',{'cases':cases,'protocol_sha256':hashlib.sha256(raw).hexdigest()})
    sources=source_hashes([path,Path(__file__),HERE/'complexity_study.py']);start=time.process_time();wall=time.monotonic();runs={};states={};failure=None
    for case in cases:
        try:
            if time.monotonic()-wall>300:raise TimeoutError('Paired-blocker wall budget exhausted')
            folder=output/'cases'/case['id']
            runs[case['id']]=run_case(case,(case['source_present'],),deadline_cpu=start+120,
                max_cells=20000,audit=True,output=folder,prepare_function=prepare_paired)
            states[case['id']]=states_from(folder/'states.jsonl')
        except(TimeoutError,MemoryError)as exc:
            failure={'id':case['id'],'message':str(exc)};break
    observations={}
    for case in cases:
        identifier=case['id']
        if identifier not in states or not case['source_present']:continue
        if case['kind']=='joint':
            baseline_id=f'paired-{case["variants"][0]}-{case["variants"][1]}-s0'
            if baseline_id not in states:continue
            baseline=states[baseline_id];signs=(-1,1)
        else:
            _,initial,_=prepare_paired(case,(False,));baseline=[initial]*41;signs=(case['isolated_side'],)
        observations[identifier]={str(s):outlet_report(states[identifier],baseline,s)for s in signs}
    isolated_ok=all(observations.get(f'paired-isolated-{s}-O',{}).get(str(s),{}).get('counter_transmission',False)
        and observations.get(f'paired-isolated-{s}-N',{}).get(str(s),{}).get('strong_complete_outlet_block',False)for s in(-1,1))
    composition_ok=(observations.get('paired-O-N-s1',{}).get('-1',{}).get('counter_transmission',False)
        and observations.get('paired-O-N-s1',{}).get('1',{}).get('strong_complete_outlet_block',False)
        and observations.get('paired-N-O-s1',{}).get('1',{}).get('counter_transmission',False)
        and observations.get('paired-N-O-s1',{}).get('-1',{}).get('strong_complete_outlet_block',False))
    cancellation=[]
    for case in cases:
        if case['kind']!='joint'or not case['source_present']or case['id']not in observations:continue
        for sign,label in zip((-1,1),case['variants']):
            isolate=f'paired-isolated-{sign}-{label}'
            if isolate not in observations:continue
            active_alone=observations[isolate][str(sign)]['counter_transmission']
            quiet_joint=observations[case['id']][str(sign)]['strong_complete_outlet_block']
            if active_alone and quiet_joint:
                witnesses=cancellation_witnesses(states[case['id']],states[isolate],sign,[6,40])
                cancellation.append({'joint':case['id'],'isolated':isolate,'side':sign,
                                     'input_witnesses':witnesses,'demonstrated_input_cancellation':bool(witnesses)})
    stationary=all(r['entire_board_stationary']for key,r in runs.items()if key.endswith('-s0'))
    summary={'execution_status':'completed'if failure is None else'inconclusive','runs_completed':len(runs),
        'forward_steps':sum(r['preparation']['steps']for r in runs.values()),
        'nominal_isolated_passed':isolated_ok,'nominal_composition_passed':composition_ok,
        'overall_passed':len(runs)==24 and isolated_ok and composition_ok and stationary,
        'all_no_source_stationary':stationary,
        'all_full_inverses':all(r['all_one_step_inverses']and r['complete_rewind']for r in runs.values()),
        'counterfactual_cancellation_comparisons':len(cancellation),
        'demonstrated_input_cancellations':sum(c['demonstrated_input_cancellation']for c in cancellation),
        'failure':failure,'cpu_seconds':time.process_time()-start,
        'source_unchanged':sources==source_hashes([path,Path(__file__),HERE/'complexity_study.py']),
        'written_memory_router_claim':False,'old_K_prediction_changed':False}
    write_json(output/'result.json',{'summary':summary,'observations':observations,'cancellation':cancellation,
                                   'source_sha256':sources,'protocol_sha256':hashlib.sha256(raw).hexdigest()})
    print(canonical(summary),flush=True);return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    execute(parser.parse_args().output)
