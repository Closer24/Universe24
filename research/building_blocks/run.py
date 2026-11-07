"""Run the frozen clockwork assembly protocol and export exact read-only replay.

Every forward transition is Engine.advance. Observers never supply a state update.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

from universe24.experiments.config import checkpoint_data
from .preparation import prepare, pair, memory

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = Path(__file__).with_name('protocol.json')
CYCLE = ((0,1),(1,0),(0,-1),(-1,0))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        handle.write(canonical(value) + '\n')


def normalized_state(state, origin):
    return {'background':list(state.background), 'cells':[
        [*[addr[k]-origin[k] for k in range(3)],addr[3],*triple]
        for addr,triple in sorted(state.cells.items())]}


def source_hashes():
    paths = list((ROOT/'universe24').rglob('*.py')) + [PROTOCOL,Path(__file__),Path(__file__).with_name('preparation.py'), Path(__file__).with_name('verify_bundle.py'), ROOT/'research/clockwork/viewer.html', ROOT/'research/reproducibility/bundle.py']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def run_case(case, output, started, budget):
    engine, initial, origin = prepare(case)
    state = initial
    frames, norms, states = [], [], []
    checkpoints = []
    first = {j:None for j in range(1,case['N']+1)}
    prev_memory = [0]*(case['N']+1)
    no_boundary = True
    all_inverses = True
    for t in range(case['steps']+1):
        if time.process_time()-started > budget['cpu_seconds']:
            raise TimeoutError('Registered CPU budget exceeded')
        if len(state.cells)>budget['max_sparse_channels']:
            raise TimeoutError('Registered sparse-support budget exceeded')
        values = [pair(state,origin,j) for j in range(case['N']+1)]
        memories = [memory(p) for p in values]
        for j in first:
            if first[j] is None and values[j][0].b != 0:
                first[j]=t
        cp = checkpoint_data(state,engine,t)
        states.append(state)
        checkpoints.append(cp)
        norms.append(digest(normalized_state(state,origin)))
        no_boundary &= all(all(0<c<case['side']-1 for c in addr[:3]) for addr in state.cells)
        transitions=[]
        if t:
            previous=states[-2]
            sums=engine.input_sums(previous)
            for j in range(case['N']+1):
                address=(origin[0]+j,origin[1],origin[2],0)
                old=previous.at(address)
                new=state.at(address)
                ell=new.b+old.a
                u=sums.get(address,0)
                assert 2*u+old.r == 6*ell+new.r
                assert new.a==old.b and new.b==ell-old.a
                transitions.append({'u':u,'ell':ell,'old':list(old),'next':list(new)})
        frames.append({'t':t,'state_hash':digest(cp),'active_channels':len(state.cells),
                       'memory':memories,'clicks':[j for j in range(len(memories)) if t and memories[j] and not prev_memory[j]],
                       'cells':[[list(v) for v in p] for p in values],
                       'transitions':transitions,'inverse_ok':True})
        prev_memory=memories
        if t<case['steps']:
            new=engine.advance(state)
            ok=engine.rewind(new)==state
            all_inverses &= ok
            if not ok:
                frames[-1]['inverse_ok']=False
                raise AssertionError('Complete-state one-step inverse mismatch')
            state=new
    rewound=state
    for _ in range(case['steps']):
        rewound=engine.rewind(rewound)
    checks={'all_step_inverses':all_inverses,'complete_rewind':rewound==initial,
            'no_active_boundary_contact':bool(no_boundary)}
    detectors={}
    for j in case['detectors']:
        end=2*(case['N']+1)-j
        interval=range(j,min(end,case['steps']+1))
        cycle_ok=all(tuple(frames[t]['cells'][j][0][:2])==CYCLE[(t-j)%4]
            and tuple(frames[t]['cells'][j][1][:2])==tuple(-v for v in CYCLE[(t-j)%4]) for t in interval)
        window_ok=all(frames[t]['memory'][j]==int(j<=t<end) for t in range(min(end,case['steps'])+1))
        detectors[str(j)]={'arrival':first[j],'expected_arrival':j,'first_record_window':[j,end],
                         'required_retention_samples':end-j,'counter_cycle_matches':cycle_ok,
                         'first_window_matches':window_ok,
                         'click_times':[f['t'] for f in frames if j in f['clicks']],
                         'record_on_samples':sum(f['memory'][j] for f in frames)}
    mode=case['mode']
    if mode=='guide':
        checks['retention_horizon_covers_endpoints']=all(case['steps']>=2*(case['N']+1)-j for j in case['detectors'])
        checks['unit_speed_all_receivers']=all(first[j]==j for j in first)
        checks['composed_clock_records']=all(v['arrival']==v['expected_arrival'] and v['counter_cycle_matches'] and v['first_window_matches'] for v in detectors.values())
    elif mode=='no_source':
        checks['entire_board_stationary']=all(s==initial for s in states)
        checks['no_detector_click']=all(not v['click_times'] for v in detectors.values())
    elif mode=='source_only':
        checks['no_detector_click']=all(not v['click_times'] for v in detectors.values())
    elif mode=='gap':
        checks['downstream_inactive']=first[12] is None
        checks['downstream_no_record']=not detectors['12']['click_times']
    elif mode=='odd_remainder':
        checks['retention_horizon_covers_endpoints']=all(case['steps']>=2*(case['N']+1)-j for j in case['detectors'])
        j=case['perturb_at']
        checks['perturbed_clock_starts']=first[j]==j
        checks['fixed_memory_never_fires']=all(f['memory'][j]==0 for f in frames)
        checks['perturbed_clock_cycle_survives']=detectors[str(j)]['counter_cycle_matches']
    case_dir=output/'cases'/case['id']
    case_dir.mkdir(parents=True)
    write_json(case_dir/'initial.json',checkpoints[0])
    write_json(case_dir/'final.json',checkpoints[-1])
    # Each line is a full retained checkpoint, including the off-guide remainder field.
    with (case_dir/'states.jsonl').open('x',encoding='utf-8') as handle:
        for cp in checkpoints:
            handle.write(canonical(cp)+'\n')
    result={'id':case['id'],'configuration':case,'coupling_fingerprint':engine.coupling.fingerprint,
            'checks':checks,'accepted':all(checks.values()),'detectors':detectors,
            'first_arrivals':first,'normalized_full_state_hashes':norms,
            'initial_hash':digest(checkpoints[0]),'final_hash':digest(checkpoints[-1]),
            'max_stored_deviations':max(f['active_channels'] for f in frames)}
    write_json(case_dir/'result.json',result)
    description={
        'guide':'A source perturbation traverses a prepared medium, starts local counter cycles and writes finite remainder records.',
        'no_source':'The same prepared receivers have zero counters and remain exactly stationary without the initial source.',
        'source_only':'Removing the prepared medium leaves no click at either predefined receiver during this run.',
        'gap':'One initially unarmed site delays transfer, but later downstream activity defeats the registered no-transfer prediction. This is not an autonomous control-signal clutch.',
        'odd_remainder':'An odd-parity receiver starts its counter clock but can never satisfy the fixed even-parity record predicate.'}[mode]
    scenario={'id':case['id'],'title':('Unarmed site: delayed activation' if mode=='gap' else case['title']),'description':description,'kind':case['kind'],
              'side':case['side'],'signs':[1,1,1],'steps':case['steps'],'source_index':0,
              'detectors':case['detectors'],'sites':[{'index':j,'label':'Source' if j==0 else f'Receiver {j}',
              'position':[origin[0]+j,origin[1],origin[2]]} for j in range(case['N']+1)],
              'frames':frames,'metrics':{'accepted':result['accepted'],'checks':checks,'detectors':detectors,
              'max_stored_deviations':result['max_stored_deviations'],
              'scientific_status':'Finite prepared result; no claim of physical light or permanent memory.'}}
    return scenario,result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True,help='New output directory; existing evidence is never overwritten')
    parser.add_argument('--skip-viewer',action='store_true',help='Generate scientific evidence without packaging HTML')
    args=parser.parse_args(argv)
    args.output.mkdir(parents=True,exist_ok=False)
    protocol=json.loads(PROTOCOL.read_text())
    hashes=source_hashes()
    baseline=json.loads((ROOT/'research/reproducibility/base_engine.json').read_text())
    baseline_hashes=baseline['source_sha256']
    core_matches=all(hashes.get(p)==h for p,h in baseline_hashes.items())
    if not core_matches:
        raise ValueError('Engine source differs from pinned baseline')
    started=time.process_time()
    records=[];scenarios=[]
    failure=None
    try:
        for case in protocol['cases']:
            scenario,result=run_case(case,args.output,started,protocol['budget'])
            scenarios.append(scenario);records.append(result)
    except (TimeoutError,AssertionError) as exc:
        failure={'type':type(exc).__name__,'message':str(exc)}
    size_equal=(len(records)>=2 and records[0]['normalized_full_state_hashes']==records[1]['normalized_full_state_hashes'])
    source_unchanged=hashes==source_hashes()
    accepted=(failure is None and len(records)==len(protocol['cases']) and all(r['accepted'] for r in records) and size_equal and source_unchanged)
    summary={'protocol_id':protocol['protocol_id'],'execution_status':'inconclusive' if failure and failure['type']=='TimeoutError' else ('failed' if failure else 'completed'),
             'accepted':accepted,'core_unchanged':core_matches,'source_unchanged_during_run':source_unchanged,
             'normalized_size_traces_equal':size_equal,'cases':[{k:r[k] for k in ('id','accepted','checks','detectors')} for r in records],
             'failure':failure,'physical_validation':False,
             'limitations':['Prepared medium required in tested controls.','Finite records reset and may click again.','Odd remainder perturbation defeats fixed memory readout.','An initially unarmed site delays rather than universally blocks transfer.','Initial-state transfer contrast is not an autonomous clutch.']}
    dataset={'schema_version':'u24-clockwork-v1','engine_commit':protocol['engine_baseline'],
             'protocol_id':protocol['protocol_id'],'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
             'scenarios':scenarios,'summary':summary}
    manifest={'engine_commit':protocol['engine_baseline'],'reliability_parent':protocol['reliability_parent'],
              'checkout_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              'working_tree_dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()),
              'protocol_sha256':dataset['protocol_sha256'],'source_sha256':hashes,
              'python':platform.python_version(),'command':sys.argv,'seed':None,
              'seed_policy':'Deterministic complete initial checkpoints; no random search in this protocol.',
              'coupling_policy':'Fixed +++ throughout; all other tensor studies are separately registered.'}
    write_json(args.output/'protocol.json',protocol)
    write_json(args.output/'manifest.json',manifest)
    write_json(args.output/'result.json',summary)
    write_json(args.output/'replay_data.json',dataset)
    write_json(args.output/'runtime.json',{'cpu_seconds':time.process_time()-started})
    if not args.skip_viewer:
        template=ROOT/'research/clockwork/viewer.html'
        text=template.read_text(encoding='utf-8')
        marker='/*__U24_DATA__*/ null'
        if text.count(marker)!=1:
            raise ValueError('Expected exactly one viewer data sentinel')
        # Escaping '<' also protects script context if textual metadata changes later.
        html=text.replace(marker,canonical(dataset).replace('<','\\u003c'))
        with (args.output/'clockwork.html').open('x',encoding='utf-8') as handle:
            handle.write(html)
    print(json.dumps({'accepted':accepted,'cases':len(records),'size_equal':size_equal,'failure':failure,'output':str(args.output)}))
    return 0 if accepted else 1


if __name__=='__main__':
    raise SystemExit(main())
