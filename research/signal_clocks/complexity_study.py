"""Frozen matched-branch cooperation test using only initial preparations.

The score is evaluated after complete trajectories exist. It is never passed
to Engine.advance and cannot select a path during evolution.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import time

from universe24 import Channel,Coupling,Cube,Engine,State
from universe24.experiments.config import from_dict
from .complexity_math import cooperation_score
from .run import canonical,run_case,write_json
from .search import source_hashes

HERE=Path(__file__).resolve().parent


def prepare_fork(case, source_mask):
    side=case['side'];o=(side//2,)*3;cells={};present=source_mask[0]
    for direction,v in zip((-1,1),case['variants']):
        if case.get('isolated_side') is not None and direction!=case['isolated_side']:
            continue
        for j in range(1,7):
            pos=(o[0]+direction*j,o[1],o[2])
            r=v if j in (2,3) else 4
            if direction==case.get('test_side') and j in case.get('flips',[]):
                r=(r+2)%6
            cells[(*pos,0)]=Channel(0,0,r)
            cells[(*pos,14)]=Channel(0,0,0)
    for key,values in case['probe']['source_at_origin'].items():
        a,b,r=values
        cells[(*o,int(key))]=Channel(a if present else 0,b if present else 0,r)
    engine=Engine(Coupling((1,1,1)))
    return engine,State(Cube(side),Channel(0,0,2),cells),{
        'origin':o,'detector':[(*o,0),(*o,14)],'sources':[o],
        'outlets':[(o[0]-6,o[1],o[2]),(o[0]+6,o[1],o[2])]}


def cases_for(protocol):
    cases=[];P0=protocol['calibration']['probe'];side=protocol['geometry']['side']
    for sign in protocol['calibration']['tested_arm_sides']:
        for variant in protocol['calibration']['variants']:
            for subset,flips in (('none',[]),('i',[2]),('j',[3]),('ij',[2,3])):
                variants=[4,4];variants[0 if sign<0 else 1]=variant
                cases.append({'id':f'cal-{sign}-{variant}-{subset}','kind':'calibration',
                    'side':side,'steps':9,'variants':variants,'probe':P0,
                    'test_side':sign,'variant':variant,'subset':subset,'flips':flips,
                    'source_present':True})
    for left,right in protocol['heldout']['ordered_variant_pairs']:
        cases.append({'id':f'null-{left}-{right}','kind':'no_source','side':side,
            'steps':15,'variants':[left,right],'probe':P0,'source_present':False})
    for sign in (-1,1):
        for variant in (0,2,4):
            for probe in protocol['heldout']['probes']:
                variants=[4,4];variants[0 if sign<0 else 1]=variant
                cases.append({'id':f'isolated-{sign}-{variant}-{probe["id"]}',
                    'kind':'isolated','side':side,'steps':15,'variants':variants,
                    'isolated_side':sign,'variant':variant,'probe':probe,'source_present':True})
    for left,right in protocol['heldout']['ordered_variant_pairs']:
        for probe in protocol['heldout']['probes']:
            cases.append({'id':f'joint-{left}-{right}-{probe["id"]}','kind':'joint',
                'side':side,'steps':15,'variants':[left,right],'probe':probe,'source_present':True})
    if len(cases)!=protocol['budget']['run_count']:
        raise ValueError('Run manifest disagrees with frozen count')
    return cases


def states_from(path):
    return [from_dict(json.loads(line)['experiment']).initial for line in Path(path).read_text().splitlines()]


def outlet_vector(states,sign,window):
    o=(states[0].cube.side//2,)*3;pos=(o[0]+sign*6,o[1],o[2])
    return [states[t].at((*pos,g)).b for t in range(window[0],window[1]+1) for g in range(48)]


def terms(state,engine,address):
    return [{'direction':d,'address':list(state.cube.adjacent(address,d,engine.coupling.ports[d][address[3]])),
             'weight':engine.coupling.weights[d][address[3]],
             'b':state.at(state.cube.adjacent(address,d,engine.coupling.ports[d][address[3]])).b}
            for d in range(6)]


def cancellation_witnesses(joint,isolated,side,window):
    engine=Engine(Coupling((1,1,1)));o=joint[0].cube.side//2;position=(o+side*6,o,o);witnesses=[]
    for t in range(window[0],window[1]+1):
        for g in range(48):
            address=(*position,g);old=joint[t-1].at(address);new=joint[t].at(address)
            if old.a or old.b or new.b:
                continue
            jt=terms(joint[t-1],engine,address);products=[v['weight']*v['b'] for v in jt]
            if sum(products)!=0 or not any(products):
                continue
            it=terms(isolated[t-1],engine,address);iu=sum(v['weight']*v['b'] for v in it)
            io=isolated[t-1].at(address);inn=isolated[t].at(address)
            if iu==0 or inn.b==0:
                continue
            witnesses.append({'step':t,'address':list(address),
                'joint':{'old':list(old),'next':list(new),'u':0,'ell':new.b+old.a,'terms':jt},
                'isolated':{'old':list(io),'next':list(inn),'u':iu,'ell':inn.b+io.a,'terms':it}})
    return witnesses


def study(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    protocol_path=HERE/'complexity_protocol.json';raw=protocol_path.read_bytes();protocol=json.loads(raw)
    if protocol['status']!='frozen_before_calibration_and_probe_runs':
        raise ValueError('Protocol is not frozen')
    cases=cases_for(protocol);write_json(output/'protocol.json',protocol)
    write_json(output/'candidate_manifest.json',{'protocol_sha256':hashlib.sha256(raw).hexdigest(),
        'cases':cases,'selection':'All registered cases retained; no output-based case selection.'})
    hashes=source_hashes([protocol_path,Path(__file__),HERE/'complexity_math.py'])
    started=time.process_time();wall=time.monotonic();deadline=started+protocol['budget']['cpu_seconds']
    records={};states={};scores={};failure=None
    for index,case in enumerate(cases):
        try:
            if time.monotonic()-wall>protocol['budget']['wall_seconds']:
                raise TimeoutError('Registered cooperation wall budget exhausted')
            folder=output/'cases'/case['id']
            result=run_case(case,(case['source_present'],),deadline_cpu=deadline,
                max_cells=protocol['budget']['stored_channels_per_state'],audit=True,
                output=folder,prepare_function=prepare_fork)
            records[case['id']]=result;states[case['id']]=states_from(folder/'states.jsonl')
            if index==23:
                for sign in (-1,1):
                    for v in (0,2,4):
                        vectors={s:outlet_vector(states[f'cal-{sign}-{v}-{s}'],sign,[6,9])
                                 for s in ('none','i','j','ij')}
                        score,pairs=cooperation_score(vectors['none'],{0:vectors['i'],1:vectors['j']},{(0,1):vectors['ij']})
                        scores[f'{sign},{v}']={'score':str(score),'nonzero_pairs':list(pairs),'vectors':vectors}
                # Frozen calibration result exists before any held-out run.
                write_json(output/'calibration_scores.json',scores)
            print(canonical({'completed':index+1,'total':len(cases),'id':case['id'],
                             'cpu_seconds':round(time.process_time()-started,3)}),flush=True)
        except (TimeoutError,MemoryError) as exc:
            failure={'id':case['id'],'type':type(exc).__name__,'message':str(exc)};break
    comparisons=[]
    for case in cases:
        if case['kind']!='joint' or case['id'] not in states:
            continue
        left,right=case['variants'];probe=case['probe']['id'];control=f'null-{left}-{right}'
        if control not in states:
            continue
        kout=[int(scores[f'-1,{left}']['score']),int(scores[f'1,{right}']['score'])]
        vectors={};early={};isolated_vectors={}
        for sign,v in ((-1,left),(1,right)):
            baseline=outlet_vector(states[control],sign,[10,15]);signal=outlet_vector(states[case['id']],sign,[10,15])
            vectors[str(sign)]=[a-b for a,b in zip(signal,baseline)]
            early[str(sign)]=outlet_vector(states[case['id']],sign,[6,9])
            isolate=f'isolated-{sign}-{v}-{probe}'
            isolated_vectors[str(sign)]=outlet_vector(states[isolate],sign,[10,15])
        eligible=kout[0]!=kout[1];high=-1 if kout[0]>kout[1] else 1;low=-high
        active={s:any(values) for s,values in vectors.items()}
        strict=eligible and active[str(high)] and not active[str(low)]
        suppression=eligible and not active[str(low)] and any(isolated_vectors[str(low)])
        witnesses=(cancellation_witnesses(states[case['id']],states[f'isolated-{low}-{left if low<0 else right}-{probe}'],low,[10,15]) if eligible else [])
        category=('tie' if not eligible else 'higher_only' if strict else
                  'both_transmit' if all(active.values()) else 'both_quiet' if not any(active.values()) else 'lower_only')
        comparisons.append({'id':case['id'],'variants':[left,right],'probe':probe,'scores':kout,
            'eligible':eligible,'category':category,'strict_higher_score_only':strict,
            'isolated_to_joint_suppression':suppression,'input_cancellation_witnesses':witnesses,
            'strong_cancellation_selection':strict and suppression and bool(witnesses),
            'late_probe_induced_b_vectors':vectors,'early_b_vectors':early,
            'late_isolated_b_vectors':isolated_vectors,
            'counter_L1_at_source':case['probe']['total_initial_counter_L1']})
    eligible=[c for c in comparisons if c['eligible']]
    summary={'execution_status':'completed' if failure is None else 'inconclusive',
        'runs_completed':len(records),'runs_registered':len(cases),'failure':failure,
        'forward_steps':sum(r['preparation']['steps'] for r in records.values()),
        'all_full_inverses':all(r['all_one_step_inverses'] and r['complete_rewind'] for r in records.values()),
        'all_no_source_stationary':all(records[c['id']]['entire_board_stationary'] for c in cases if c['kind']=='no_source' and c['id'] in records),
        'eligible_comparisons':len(eligible),'ties':sum(not c['eligible'] for c in comparisons),
        'strict_higher_only':sum(c['strict_higher_score_only'] for c in comparisons),
        'strong_cancellation_selection':sum(c['strong_cancellation_selection'] for c in comparisons),
        'prediction_status':('inconclusive' if failure else 'unresolved_tied_scores' if not eligible else
                             'finite_prediction_passed' if all(c['strict_higher_score_only'] for c in eligible) else 'finite_prediction_refuted'),
        'cpu_seconds':time.process_time()-started,'wall_seconds':time.monotonic()-wall,
        'source_unchanged':hashes==source_hashes([protocol_path,Path(__file__),HERE/'complexity_math.py']),
        'physical_validation':False,'autonomously_written_memory_router':False}
    write_json(output/'result.json',{'summary':summary,'calibration_scores':scores,'comparisons':comparisons,
        'protocol_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':hashes,
        'state_traces':{key:f'cases/{key}/states.jsonl' for key in records}})
    print(canonical(summary),flush=True)
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();summary=study(args.output)
    return 0 if summary['execution_status']=='completed' and summary['all_full_inverses'] else 2


if __name__=='__main__':
    raise SystemExit(main())
