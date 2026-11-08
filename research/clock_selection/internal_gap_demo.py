"""Frozen native baseline demonstration of a finite internal eigenmode.

The integer recurrence is an observation oracle only. Engine.advance is the
sole evolution rule, through the existing native complete-state recorder.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import time
from universe24 import Coupling, Cube, State, Channel, Engine
from universe24.observation.clicks import clicks
from research.presenter.export import capture, bundle
from research.experiments.run import recorded_states

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROTOCOL=HERE/'internal_gap_protocol.json'
CP=Coupling((1,1,1))

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))

def write_json(path,value):
    with Path(path).open('x') as handle:handle.write(canonical(value)+'\n')

def oracle(case,t,p):
    h=case['duration'];sign=case['amplitude_sign'];offset=case['stationary_uniform_offset']
    cs=p['oracle']['C_values_0_through_12']
    if not 0<=t<=h:raise ValueError('Oracle is registered only through H')
    a=sign*3**(h-1) if t==0 else sign*3**(h-t+1)*cs[t-1]
    b=sign*3**(h-t)*cs[t]
    return tuple(Channel(a*v+offset,b*v+offset,case['remainder']) for v in p['integer_eigenvector'])

def initial(case,p):
    values=oracle(case,0,p)
    return State(Cube(case['side']),cells={(*xyz,g):values[g]
        for xyz in itertools.product(range(case['side']),repeat=3) for g in range(48)})

def planned(p):
    for side,duration,mode in itertools.product(p['family']['sides'],p['family']['durations'],p['family']['modes']):
        yield {'id':f'internal-gap-L{side}-H{duration}-{mode["id"]}',
               'side':side,'duration':duration,'mode':mode['id'],
               'amplitude_sign':mode['amplitude_sign'],'stationary_uniform_offset':mode['stationary_uniform_offset'],'remainder':mode['remainder']}

def preflight(p):
    vector=p['integer_eigenvector'];cv=p['oracle']['C_values_0_through_12']
    assert len(vector)==48 and sum(bool(x) for x in vector)==18
    assert all(sum(CP.weights[d][g]*vector[CP.ports[d][g]] for d in range(6))==2*vector[g] for g in range(48))
    assert all(sum(CP.weights[d][g] for d in range(6))==6 for g in range(48))
    assert cv[:2]==[1,1] and all(cv[t+1]==2*cv[t]-9*cv[t-1] for t in range(1,12))
    cases=[]
    for case in planned(p):
        for t in range(case['duration']):
            old,new=oracle(case,t,p),oracle(case,t+1,p)
            for g,v in enumerate(vector):
                B=case['amplitude_sign']*3**(case['duration']-t)*cv[t]
                assert B%3==0
                u=2*B*v+6*case['stationary_uniform_offset'];ell=2*B*v//3+2*case['stationary_uniform_offset']
                assert (ell,case['remainder'])==divmod(2*u+case['remainder'],6)
                assert new[g]==Channel(old[g].b,ell-old[g].a,case['remainder'])
        cases.append(case)
    return {'initial_algebra_checks_passed':True,'new_engine_trajectories':0,
            'cases':cases,'vector_nonzero_channels':18,
            'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def observe(case,states,p):
    vector=p['integer_eigenvector'];h=case['duration'];side=case['side']
    mismatches=[];uniform=True;event_equal=True;counts={str(k):0 for k in range(3)};trace=[]
    sites=list(itertools.product(range(side),repeat=3))
    for t,state in enumerate(states):
        expected=oracle(case,t,p);actual=tuple(state.at((0,0,0,g)) for g in range(48))
        trace.append([list(value) for value in actual])
        for xyz in sites:
            row=tuple(state.at((*xyz,g)) for g in range(48))
            uniform=uniform and row==actual
            for g in range(48):
                if row[g]!=expected[g]:mismatches.append({'state':t,'address':[*xyz,g],'actual':list(row[g]),'expected':list(expected[g])})
    event_checks=[];all_events=[]
    for t,(old,new) in enumerate(zip(states,states[1:]),1):
        actual_events=sorted((event.address,event.kind,event.quotient) for event in clicks(old,new,t))
        all_events.extend({'step':t,'address':list(address),'kind':kind,'ell':ell} for address,kind,ell in actual_events)
        old_values,new_values=oracle(case,t-1,p),oracle(case,t,p)
        B=case['amplitude_sign']*3**(h-t+1)*p['oracle']['C_values_0_through_12'][t-1]
        expected_events=[]
        for xyz in sites:
            for g,v in enumerate(vector):
                u=2*B*v+6*case['stationary_uniform_offset'];ell=2*B*v//3+2*case['stationary_uniform_offset']
                if ell and new_values[g]!=old_values[g]:expected_events.append(((*xyz,g),u%3,ell))
        expected_events.sort();same=actual_events==expected_events;event_equal=event_equal and same
        for _,kind,_ in actual_events:counts[str(kind)]+=1
        event_checks.append({'update':t,'all_addresses_classes_quotients_equal':same,
                             'actual_count':len(actual_events),'expected_count':len(expected_events)})
    return {'full_oracle_mismatches':mismatches,'all_triples_match_oracle':not mismatches,
            'spatial_uniformity':uniform,'all_event_addresses_classes_quotients_match':event_equal,
            'event_checks':event_checks,'all_C':all_events,'C_counts':counts,'complete_channel_trace_at_origin':trace,
            'remainders_match_registered_value':all(value.r==case['remainder'] for state in states for value in state.cells.values()),
            'max_sparse_channels':max(len(state.cells) for state in states)}

def assess(rows):
    by={row['case']['mode']:row for row in rows}
    states={name:recorded_states(row['experiment']) for name,row in by.items()}
    sign_equal=True;offset_equal=True;parity_equal=True
    for t in range(len(states['gap_plus'])):
        a,b,s,m,q=(states[name][t] for name in ('gap_plus','gap_minus','uniform_only','gap_plus_offset','gap_plus_parity'))
        for xyz in itertools.product(range(a.cube.side),repeat=3):
            for g in range(48):
                address=(*xyz,g);positive,negative,offset,mixed=(state.at(address) for state in (a,b,s,m))
                sign_equal=sign_equal and (negative.a,negative.b,negative.r)==(-positive.a,-positive.b,2)
                offset_equal=offset_equal and (mixed.a-offset.a,mixed.b-offset.b)==(positive.a,positive.b) and positive.r==offset.r==mixed.r==2
                parity=q.at(address)
                parity_equal=parity_equal and (parity.a,parity.b,parity.r)==(positive.a,positive.b,positive.r+1)
    return {'side':rows[0]['case']['side'],'duration':rows[0]['case']['duration'],
            'all_full_state_oracles_pass':all(row['observations']['all_triples_match_oracle'] for row in rows),
            'all_raw_event_oracles_pass':all(row['observations']['all_event_addresses_classes_quotients_match'] for row in rows),
            'exact_sign_control':sign_equal,'exact_stationary_uniform_offset_independence':offset_equal,
            'exact_inert_parity_counter_and_remainder_identity':parity_equal,
            'exact_inert_parity_native_events':by['gap_plus']['observations']['all_C']==by['gap_plus_parity']['observations']['all_C'],
            'physical_mass_or_transport_established':False}

def source_hashes():
    paths=[Path(__file__),PROTOCOL,ROOT/'research/experiments/run.py']
    for directory in ('universe24','research/presenter'):
        paths.extend((ROOT/directory).rglob('*.py'))
    return {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(paths))}

def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir()
    p=json.loads(PROTOCOL.read_text());frozen=source_hashes();cpu=time.process_time();wall=time.monotonic()
    shutil.copyfile(PROTOCOL,output/'protocol.json');shutil.copyfile(Path(__file__),output/'executed_internal_gap_demo.py')
    write_json(output/'registration.json',{'source_sha256':frozen,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'registered_before_capture':True,'preflight':preflight(p)})
    ledger=[];groups=[];examples=[];rows=[];failure=None
    try:
        for case in planned(p):
            if time.process_time()-cpu>p['budget']['max_cpu_seconds']-15 or time.monotonic()-wall>p['budget']['max_wall_seconds']-20:
                failure={'type':'budget_stop_before_case','case':case};break
            experiment=capture(Engine(CP),initial(case,p),case['duration'],id=case['id'],title='Internal channel mode: '+case['mode'],
                description='Global finite-duration exact baseline mode; no transport or physical mass claim.',
                view={'position':[0,0,0],'channel':0},max_frames=case['duration']+1,
                max_cells=p['budget']['max_cumulative_native_rows_per_record'],max_bytes=p['budget']['max_recorded_bytes'],
                max_seconds=p['budget']['max_seconds_per_record'])
            experiment['provenance']['internal_gap_case']=case
            experiment['provenance']['protocol_sha256']=frozen[str(PROTOCOL.relative_to(ROOT))]
            states=recorded_states(experiment)
            if any(len(state.cells)>p['budget']['max_sparse_channels_per_state'] for state in states):raise RuntimeError('Per-state channel budget exceeded')
            row={'case':case,'experiment':experiment,'observations':observe(case,states,p)}
            path=output/'records'/(case['id']+'.json.gz');path.write_bytes(gzip.compress(canonical(row).encode(),mtime=0))
            ledger.append({'id':case['id'],'record':str(path.relative_to(output)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                           'full_rewind_equal':experiment['provenance']['full_rewind_equal']})
            rows.append(row)
            if len(rows)==len(p['family']['modes']):groups.append(assess(rows));rows=[]
            if case['side']==3 and case['duration']==8:examples.append(experiment)
            print(f'{len(ledger)}/20 {case["id"]}',flush=True)
            if sum(path.stat().st_size for path in output.rglob('*') if path.is_file())>p['budget']['max_recorded_bytes']-8000000:raise RuntimeError('Recorded evidence budget reached')
    except Exception as error:
        failure={'type':type(error).__name__,'message':str(error),'case':locals().get('case')};write_json(output/'failure.json',failure)
    assert source_hashes()==frozen,'Frozen sources changed'
    if examples:write_json(output/'experiments.json',bundle(examples,title='The Presenter: internal channel modes'))
    result={'status':'completed' if len(ledger)==20 and failure is None else 'inconclusive','failure':failure,'completed_cases':len(ledger),
        'cases':ledger,'groups':groups,'all_full_rewinds':all(row['full_rewind_equal'] for row in ledger),
        'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.monotonic()-wall,'sources_unchanged':True,
        'scope':'Exact finite global internal-mode demonstration; no physical mass, transport or complexity preference.'}
    result['budget_passed']=result['cpu_seconds']<=p['budget']['max_cpu_seconds'] and result['wall_seconds']<=p['budget']['max_wall_seconds'] and sum(path.stat().st_size for path in output.rglob('*') if path.is_file())<=p['budget']['max_recorded_bytes']
    write_json(output/'result.json',result);return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--preflight-output',type=Path);modes.add_argument('--output',type=Path);args=parser.parse_args()
    if args.output:run(args.output)
    else:
        args.preflight_output.parent.mkdir(parents=True,exist_ok=True)
        write_json(args.preflight_output,preflight(json.loads(PROTOCOL.read_text())))

if __name__=='__main__':main()
