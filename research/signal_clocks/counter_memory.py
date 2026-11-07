"""Prospective exact counter-magnitude memory confirmation on fresh geometry."""
import argparse
import hashlib
import json
from pathlib import Path
import time

from .run import run_case,write_json,canonical
from .search import source_hashes
from .toggle_confirm import check_run

HERE=Path(__file__).resolve().parent


def execute(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    path=HERE/'counter_memory_protocol.json';raw=path.read_bytes();protocol=json.loads(raw)
    with(output/'protocol.json').open('xb')as f:f.write(raw)
    cases=[]
    for d1,d2 in protocol['preparation']['distance_pairs']:
        case={'id':f'counter-memory-{d1}-{d2}','side':221,'extent':40,'steps':48,
            'body_signs':[1,1,1],'source_offsets':[-d1,d2],
            'source_ab':[[0,1],[0,1]],'target_remainders':[4,0],
            'guide_mode':'between_sources','arrival_windows':[[d1,d1],[d2+2,d2+2]]}
        for mask in protocol['preparation']['source_masks']:
            cases.append({'case':case,'mask':mask,'id':case['id']+f'-s{int(mask[0])}{int(mask[1])}'})
    write_json(output/'candidate_manifest.json',{'runs':cases,'protocol_sha256':hashlib.sha256(raw).hexdigest()})
    sources=source_hashes([path,Path(__file__),HERE/'toggle_confirm.py']);start=time.process_time();results={};failure=None
    for item in cases:
        try:
            results[item['id']]=run_case(item['case'],tuple(item['mask']),deadline_cpu=start+60,
                max_cells=20000,audit=True,output=output/'cases'/item['id'])
        except(TimeoutError,MemoryError)as exc:
            failure={'id':item['id'],'message':str(exc)};break
    groups=[]
    for d1,d2 in protocol['preparation']['distance_pairs']:
        ids=[f'counter-memory-{d1}-{d2}-s{s}'for s in('00','10','01','11')]
        if not all(i in results for i in ids):continue
        per_run={}
        for mask,expected in [('00',[]),('10',[d1]),('01',[d2]),('11',[d1,d2+2])]:
            result=results[f'counter-memory-{d1}-{d2}-s{mask}'];checks=check_run(result,expected)
            magnitudes=[[a*a+b*b for a,b,r in row['detector']]for row in result['trace']]
            ideal=[(0 if not expected or t<expected[0] else 4 if len(expected)==2 and t>=expected[1] else 1)for t in range(49)]
            checks['exact_magnitude_record']=all(v==[level,level]for v,level in zip(magnitudes,ideal))
            changes=[t for t in range(1,len(magnitudes))if magnitudes[t]!=magnitudes[t-1]]
            checks['no_extra_magnitude_changes']=changes==expected
            identities=[]
            for before,after in zip(result['trace'],result['trace'][1:]):
                for (a,b,r),(aa,bb,rr)in zip(before['detector'],after['detector']):
                    ell=bb+a;identities.append(aa*aa+bb*bb-a*a-b*b==ell*ell-2*a*ell)
            checks['exact_magnitude_balance_identity']=all(identities)
            per_run[mask]={'checks':checks,'passed':all(checks.values()),'magnitudes':magnitudes,
                'magnitude_change_times':changes,'record_event_times':result['record_event_times'],
                'arithmetic_bank_times':sorted({e['step']for e in result['arithmetic_events']})}
        both=results[ids[3]];one=results[ids[1]];two=results[ids[2]]
        contrast=[both['trace'][d1-1]['next_input']!=two['trace'][d1-1]['next_input'],
                  both['trace'][d2+1]['next_input']!=one['trace'][d2+1]['next_input']]
        first_terms=next((t for t in range(48)if both['trace'][t]['six_inputs']!=one['trace'][t]['six_inputs']),None)
        first_net=next((t for t in range(48)if both['trace'][t]['next_input']!=one['trace'][t]['next_input']),None)
        groups.append({'distance_pair':[d1,d2],'runs':per_run,'source_counterfactuals':contrast,
            'first_second_source_term_difference_old_step':first_terms,'first_second_source_net_difference_old_step':first_net,
            'passed':all(v['passed']for v in per_run.values())and all(contrast)})
    summary={'execution_status':'completed'if failure is None else'inconclusive','runs_completed':len(results),
        'forward_steps':sum(r['preparation']['steps']for r in results.values()),
        'passed':len(groups)==2 and all(g['passed']for g in groups),
        'all_full_inverses':all(r['all_one_step_inverses']and r['complete_rewind']for r in results.values()),
        'failure':failure,'cpu_seconds':time.process_time()-start,
        'source_unchanged':sources==source_hashes([path,Path(__file__),HERE/'toggle_confirm.py']),
        'physical_energy_claim':False,'old_remainder_only_milestone_accepted':False}
    write_json(output/'result.json',{'summary':summary,'groups':groups,'source_sha256':sources,'protocol_sha256':hashlib.sha256(raw).hexdigest()})
    print(canonical(summary),flush=True);return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    execute(parser.parse_args().output)
