"""Fresh, separately registered confirmation of a two-symbol receiver toggle."""
import argparse
import hashlib
import json
from pathlib import Path
import time

from .run import run_case,write_json,canonical
from .search import source_hashes

HERE=Path(__file__).resolve().parent


def check_run(result, expected):
    trace=result['trace'];r=result['record_event_times']
    c=sorted({e['step'] for e in result['arithmetic_events']})
    expected_symbols=[[4,0],[0,4],[4,0]][:len(expected)+1]
    actual_symbols=[trace[0]['memory']]+[trace[t]['memory'] for t in r]
    quiet=set()
    if expected:
        quiet.update(range(expected[0]-4,expected[0]-1))
        for t in expected:quiet.update(range(t,t+4))
    return {'exact_record_times':r==expected,'exact_arithmetic_bank_times':c==expected,
        'expected_alternating_symbols':actual_symbols==expected_symbols,
        'quiet_windows':all(0<=t<len(trace)-1 and trace[t]['next_input']==[0,0] for t in quiet),
        'incident_at_expected_events':all(any(trace[t-1]['next_input']) for t in expected),
        'complete_horizon':len(trace)==result['preparation']['steps']+1,
        'causal_boundary_margin':result['initial_boundary_margin']>result['preparation']['steps'],
        'full_one_step_inverses':result['all_one_step_inverses'],
        'complete_rewind':result['complete_rewind'],
        'no_source_stationary':bool(expected) or result['entire_board_stationary']}


def main_run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    protocol_path=HERE/'toggle_protocol.json';raw=protocol_path.read_bytes();protocol=json.loads(raw)
    if protocol['status']!='frozen_before_fresh_confirmation':raise ValueError('Protocol is not frozen')
    with (output/'protocol.json').open('xb') as handle:
        handle.write(raw)
    prepared=[]
    for d1,d2 in protocol['preparation']['fresh_distance_pairs']:
        case={'id':f'toggle-{d1}-{d2}','side':201,'extent':40,'steps':40,
              'body_signs':[1,1,1],'source_offsets':[-d1,d2],
              'source_ab':[[0,1],[0,1]],'target_remainders':[4,0],
              'guide_mode':'between_sources','arrival_windows':[[d1,d1],[d2+2,d2+2]]}
        for mask in protocol['preparation']['source_masks']:
            prepared.append({'case':case,'mask':mask,'id':case['id']+f'-s{int(mask[0])}{int(mask[1])}'})
    write_json(output/'candidate_manifest.json',{'protocol_sha256':hashlib.sha256(raw).hexdigest(),'runs':prepared})
    hashes=source_hashes([Path(__file__),protocol_path]);started=time.process_time();wall=time.monotonic()
    runs={};failure=None;entries=[]
    for item in prepared:
        try:
            if time.monotonic()-wall>180:raise TimeoutError('Frozen toggle wall budget exhausted')
            folder=output/'cases'/item['id'];result=run_case(item['case'],tuple(item['mask']),
                deadline_cpu=started+60,max_cells=20000,audit=True,output=folder)
            runs[item['id']]=result
            target=result['locations']['detector'];trace=folder/'states.jsonl'
            entries.append({'id':item['id'],'title':f'Fresh toggle {item["case"]["source_offsets"]}: sources {item["mask"]}',
                'description':'A separately registered two-symbol toggle confirmation on new source distances. All initial disturbances, every memory change and every guarded arithmetic event are retained. Acceptance is reported in result.json; no physical-light or irreversible-time claim.',
                'trace':str(trace.relative_to(output)),'trace_sha256':hashlib.sha256(trace.read_bytes()).hexdigest(),
                'view':{'position':target[0][:3],'channel':0},
                'readouts':[{'id':f'memory-{a}-{b}','label':f'Memory ({a}, {b})','kind':'all_equal',
                    'clauses':[{'address':target[0],'component':'r','equals':str(a)},
                               {'address':target[1],'component':'r','equals':str(b)}]}
                    for a in (0,2,4) for b in (0,2,4)]})
        except (TimeoutError,MemoryError)as exc:
            failure={'id':item['id'],'type':type(exc).__name__,'message':str(exc)};break
    groups=[]
    for d1,d2 in protocol['preparation']['fresh_distance_pairs']:
        ids=[f'toggle-{d1}-{d2}-s{s}'for s in ('00','10','01','11')]
        if not all(i in runs for i in ids):continue
        neither,one,two,both=[runs[i]for i in ids]
        checks={key:check_run(result,expected)for key,result,expected in
                [('00',neither,[]),('10',one,[d1]),('01',two,[d2]),('11',both,[d1,d2+2])]}
        contrast=[both['trace'][d1-1]['next_input']!=two['trace'][d1-1]['next_input'],
                  both['trace'][d2+1]['next_input']!=one['trace'][d2+1]['next_input']]
        term_differences=[t for t in range(40)if both['trace'][t]['six_inputs']!=one['trace'][t]['six_inputs']]
        first_terms=term_differences[0]if term_differences else None
        first_nonzero=next((t for t in range(first_terms or 0,40)if any(both['trace'][t]['next_input'])),None)
        first_netdifference=next((t for t in range(40)if both['trace'][t]['next_input']!=one['trace'][t]['next_input']),None)
        groups.append({'distance_pair':[d1,d2],'declared_role':'phase_challenge'if d2-d1==10 else'nominal_phase_aligned',
            'checks':checks,'event_source_counterfactuals':contrast,
            'passed':all(all(c.values())for c in checks.values())and all(contrast),
            'observed_record_times':{key:runs[f'toggle-{d1}-{d2}-s{key}']['record_event_times']for key in('00','10','01','11')},
            'observed_arithmetic_bank_times':{key:sorted({e['step']for e in runs[f'toggle-{d1}-{d2}-s{key}']['arithmetic_events']})for key in('00','10','01','11')},
            'second_source_input_evidence':{'first_six_term_difference_old_step':first_terms,
                'first_nonzero_joint_net_after_term_difference_old_step':first_nonzero,
                'first_net_input_difference_old_step':first_netdifference,
                'arrival_old_step':d2-1,'joint_arrival_terms':both['trace'][d2-1]['six_inputs'],
                'source1_only_arrival_terms':one['trace'][d2-1]['six_inputs'],
                'all_old_steps_with_term_differences':term_differences}})
    summary={'execution_status':'completed'if failure is None else'inconclusive','runs_completed':len(runs),
        'registered_runs':12,'forward_steps':sum(r['preparation']['steps']for r in runs.values()),
        'nominal_family_passed':len(groups)==3 and all(g['passed']for g in groups if g['declared_role']=='nominal_phase_aligned'),
        'phase_independent_extension_passed':len(groups)==3 and all(g['passed']for g in groups),
        'all_full_inverses':all(r['all_one_step_inverses']and r['complete_rewind']for r in runs.values()),
        'failure':failure,'cpu_seconds':time.process_time()-started,
        'source_unchanged':hashes==source_hashes([Path(__file__),protocol_path]),
        'original_three_symbol_milestone_accepted':False,'physical_validation':False}
    write_json(output/'result.json',{'summary':summary,'groups':groups,'source_sha256':hashes,
                                   'protocol_sha256':hashlib.sha256(raw).hexdigest()})
    write_json(output/'presentation.json',{'format':'universe24-signal-clock-presentation-v1',
        'title':'Fresh signal-toggle confirmations','protocol':{'path':'protocol.json','sha256':hashlib.sha256(raw).hexdigest()},'cases':entries})
    print(canonical(summary),flush=True);return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();main_run(args.output)
