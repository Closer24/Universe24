"""Verify replay evidence, including the registered prediction that failed.

A zero exit certifies exact reproduction/integrity. It does NOT make the original
no-transfer prediction true or turn this into physical validation.
"""
import argparse
import hashlib
import json
from pathlib import Path

from universe24.experiments.config import checkpoint_data
from research.reproducibility.bundle import loads_strict, read_json
from .preparation import prepare, pair, memory
from .run import ROOT, PROTOCOL, CYCLE, digest, normalized_state, source_hashes


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(output):
    protocol=read_json(PROTOCOL)
    require(read_json(output/'protocol.json')==protocol,'Frozen protocol mismatch')
    manifest=read_json(output/'manifest.json')
    require(manifest['protocol_sha256']==hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),'Protocol digest mismatch')
    require(manifest['source_sha256']==source_hashes(),'Incomplete or mismatched source identities')
    pinned=read_json(ROOT/'research/reproducibility/base_engine.json')['source_sha256']
    require(all(manifest['source_sha256'].get(k)==v for k,v in pinned.items()),'Core differs from pinned baseline')
    require(manifest['engine_commit']==protocol['engine_baseline'] and manifest['reliability_parent']==protocol['reliability_parent'],'Engine/parent identity mismatch')
    for name,sha in manifest['source_sha256'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,'Source mismatch: '+name)
    replay=read_json(output/'replay_data.json')
    summary=read_json(output/'result.json')
    require(replay['summary']==summary,'Replay summary mismatch')
    require(replay['protocol_id']==protocol['protocol_id'] and replay['engine_commit']==protocol['engine_baseline'] and replay['protocol_sha256']==manifest['protocol_sha256'],'Replay protocol/source identity mismatch')
    require([s['id'] for s in replay['scenarios']]==[c['id'] for c in protocol['cases']],'Case set/order mismatch')
    full_steps=0; inspected_frames=0; normalized={}
    for case,scenario in zip(protocol['cases'],replay['scenarios']):
        engine,initial,origin=prepare(case)
        require(scenario['side']==case['side'] and scenario['signs']==[1,1,1] and scenario['steps']==case['steps'] and scenario['detectors']==case['detectors'] and scenario['source_index']==0,'Replay geometry/tensor metadata mismatch')
        expected_sites=[{'index':j,'label':'Source' if j==0 else f'Receiver {j}','position':[origin[0]+j,origin[1],origin[2]]} for j in range(case['N']+1)]
        require(scenario['sites']==expected_sites,'Replay displayed positions mismatch')
        folder=output/'cases'/case['id']
        records=[loads_strict(line) for line in (folder/'states.jsonl').read_text().splitlines()]
        frames=scenario['frames']
        result=read_json(folder/'result.json')
        require(len(records)==len(frames)==case['steps']+1,'Truncated trajectory: '+case['id'])
        require(records[0]==read_json(folder/'initial.json') and records[-1]==read_json(folder/'final.json'),'Checkpoint endpoint mismatch')
        expected=initial;previous_memory=[0]*(case['N']+1);norms=[];states=[]
        for t,(cp,frame) in enumerate(zip(records,frames)):
            require(cp==checkpoint_data(expected,engine,t),'Full evolution/checkpoint mismatch at '+case['id']+':'+str(t))
            require(frame['t']==t and frame['state_hash']==digest(cp),'Frame identity mismatch')
            require(frame['active_channels']==len(expected.cells),'Full support count mismatch')
            values=[pair(expected,origin,j) for j in range(case['N']+1)]
            m=[memory(p) for p in values]
            require(frame['cells']==[[list(v) for v in p] for p in values],'Displayed counters differ from full state')
            require(frame['memory']==m,'Memory readout mismatch')
            clicks=[j for j in range(len(m)) if t and m[j] and not previous_memory[j]]
            require(frame['clicks']==clicks,'Rising-edge click mismatch')
            if t:
                previous=states[-1];sums=engine.input_sums(previous)
                require(len(frame['transitions'])==case['N']+1,'Missing displayed transitions')
                for j,transition in enumerate(frame['transitions']):
                    addr=(origin[0]+j,origin[1],origin[2],0)
                    old=previous.at(addr);new=expected.at(addr);u=sums.get(addr,0);ell=new.b+old.a
                    require(transition=={'u':u,'ell':ell,'old':list(old),'next':list(new)},'Displayed gear values mismatch')
                    require(2*u+old.r==6*ell+new.r and new.a==old.b,'Gear identity failed')
            else:
                require(frame['transitions']==[],'Initial frame has a synthetic update')
            require(frame['inverse_ok'] is True,'Frame inverse not certified')
            states.append(expected);norms.append(digest(normalized_state(expected,origin)))
            previous_memory=m;inspected_frames+=1
            if t<case['steps']:
                new=engine.advance(expected)
                require(engine.rewind(new)==expected,'Full step inverse failed')
                expected=new;full_steps+=1
        back=states[-1]
        for _ in range(case['steps']): back=engine.rewind(back)
        require(back==initial,'Full rewind failed')
        require(result['normalized_full_state_hashes']==norms,'Normalized state trace mismatch')
        normalized[case['id']]=norms
        require(result['configuration']==case,'Case configuration mismatch')
        require(result['coupling_fingerprint']==engine.coupling.fingerprint,'Result tensor fingerprint mismatch')
        arrivals={str(j):next((f['t'] for f in frames if f['cells'][j][0][1]!=0),None) for j in range(1,case['N']+1)}
        require(result['first_arrivals']==arrivals,'Complete receiver arrival map mismatch')
        max_support=max(len(s.cells) for s in states)
        require(result['max_stored_deviations']==max_support and scenario['metrics']['max_stored_deviations']==max_support,'Maximum support mismatch')
        require(result['initial_hash']==digest(records[0]) and result['final_hash']==digest(records[-1]),'Result state digests mismatch')
        for j in case['detectors']:
            observations=result['detectors'][str(j)]
            arrival=next((f['t'] for f in frames if f['cells'][j][0][1]!=0),None)
            end=2*(case['N']+1)-j
            require(case['steps']>=end,'Retention horizon too short')
            cycle=all(tuple(frames[t]['cells'][j][0][:2])==CYCLE[(t-j)%4] and tuple(frames[t]['cells'][j][1][:2])==tuple(-v for v in CYCLE[(t-j)%4]) for t in range(j,end))
            window=all(frames[t]['memory'][j]==int(j<=t<end) for t in range(end+1))
            require(observations=={'arrival':arrival,'expected_arrival':j,'first_record_window':[j,end],
                'required_retention_samples':end-j,'counter_cycle_matches':cycle,'first_window_matches':window,
                'click_times':[f['t'] for f in frames if j in f['clicks']],
                'record_on_samples':sum(f['memory'][j] for f in frames)},'Detector statistics mismatch')
        # Verification expectations were recorded after the frozen scientific test.
        # Preserve its negative outcome instead of changing its acceptance criterion.
        if case['mode']=='gap':
            require(result['accepted'] is False,'Original no-transfer failure was hidden')
            require(result['detectors']['12']['arrival']==32,'Gap leakage arrival changed')
            require(result['detectors']['12']['click_times']==[32,38,42,50],'Gap leakage record changed')
            require(result['checks']['downstream_inactive'] is False and result['checks']['downstream_no_record'] is False,'Failed gap checks were relabelled')
        else:
            require(result['accepted'] is True and all(result['checks'].values()),'Unexpected case failure')
        if case['mode']=='no_source': require(all(s==initial for s in states),'Source-free apparatus moved')
        if case['mode']=='source_only': require(all(not result['detectors'][str(j)]['click_times'] for j in case['detectors']),'Source-only target clicked')
        if case['mode']=='guide': require(all(result['detectors'][str(j)]['first_window_matches'] and result['detectors'][str(j)]['counter_cycle_matches'] for j in case['detectors']),'Prepared assembly failed')
        if case['mode']=='odd_remainder': require(all(f['memory'][case['perturb_at']]==0 for f in frames),'Parity failure disappeared')
        require(scenario['metrics']['accepted']==result['accepted'] and scenario['metrics']['checks']==result['checks'] and scenario['metrics']['detectors']==result['detectors'],'Replay acceptance mismatch')
        recorded=next(c for c in summary['cases'] if c['id']==case['id'])
        require(recorded=={k:result[k] for k in ('id','accepted','checks','detectors')},'Bundle result differs from case result')
    require(normalized['guide_N24']==normalized['guide_N24_larger'],'Size comparison failed')
    require(summary['accepted'] is False and summary['physical_validation'] is False,'Scientific scope or failed criterion changed')
    require(summary['failure'] is None and summary['execution_status']=='completed','Incomplete execution')
    require(summary['core_unchanged'] and summary['source_unchanged_during_run'] and summary['normalized_size_traces_equal'],'Provenance/size check failed')
    html=output/'clockwork.html'
    if html.exists():
        from .run import canonical
        template=(ROOT/'research/clockwork/viewer.html').read_text()
        expected=template.replace('/*__U24_DATA__*/ null',canonical(replay).replace('<','\\u003c'))
        require(html.read_text()==expected,'HTML is not the recorded template/data export')
    return {'verification':'passed','cases':len(protocol['cases']),'complete_forward_steps':full_steps,
            'displayed_frames_verified':inspected_frames,'scientific_protocol_accepted':False,
            'expected_failed_prediction':'Gap at j10 does not prevent downstream activation; j12 first activates at t32.',
            'physical_validation':False}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle',type=Path,required=True)
    args=parser.parse_args(argv)
    print(json.dumps(verify(args.bundle),indent=2))


if __name__=='__main__': main()
