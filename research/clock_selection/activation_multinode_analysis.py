"""Post-capture region periodicity scan; never evolves a board."""
from __future__ import annotations
import argparse,gzip,hashlib,json,time
from pathlib import Path
from research.experiments.run import recorded_states,assemble
from research.staged_blocks.interactions import canonical

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PROTOCOL=HERE/'protocol_activation_multinode_analysis.json'


def run(output):
    start=time.process_time();rawp=PROTOCOL.read_bytes();p=json.loads(rawp);output=Path(output)
    output.mkdir(parents=True,exist_ok=False);(output/'protocol.json').write_bytes(rawp)
    code=Path(__file__).read_bytes();(output/'executed_analysis.py').write_bytes(code)
    registration={'protocol_sha256':hashlib.sha256(rawp).hexdigest(),'analysis_sha256':hashlib.sha256(code).hexdigest(),
        'registered_before_new_region_inspection':True,'post_capture_exploratory':True,'new_evolution_updates':0}
    (output/'registration.json').write_text(canonical(registration)+'\n')
    study=ROOT/p['source_study'];ledger={r['id']:r for r in json.loads((study/'result.json').read_text())['cases']}
    records=[];regions=[];tests=[]
    for identity in p['cases']:
        source=study/ledger[identity]['record'];compressed=source.read_bytes();raw=gzip.decompress(compressed)
        if hashlib.sha256(compressed).hexdigest()!=ledger[identity]['record_gzip_sha256'] or hashlib.sha256(raw).hexdigest()!=ledger[identity]['record_sha256']:
            raise ValueError('Source recording hash differs from its frozen ledger')
        record=json.loads(raw)
        if record['protocol_sha256']!=p['source_protocol_sha256']:raise ValueError('Wrong parent protocol')
        states=recorded_states(record['experiment']);prepared=assemble(record['spec']);coupling=prepared.engine.coupling
        L=record['case']['side'];c=L//2;center=(c,c+1,c)
        records.append({'id':identity,'record':str(source.relative_to(ROOT)),'record_sha256':hashlib.sha256(raw).hexdigest(),
                        'record_gzip_sha256':hashlib.sha256(compressed).hexdigest()})
        for radius in p['radii']:
            inside=lambda a:all(abs(a[j]-center[j])<=radius for j in range(3))
            frames=[{a:v for a,v in states[t].cells.items() if inside(a)} for t in range(p['start_state'],p['end_state']+1)]
            activity=[sum(bool(v.a or v.b) for v in f.values()) for f in frames]
            term_counts=[];first_term=None
            for t in range(p['start_state'],p['end_state']):
                count=0;state=states[t]
                for a,v in state.cells.items():
                    if not v.b or inside(a):continue
                    for d in range(6):
                        target=state.cube.adjacent(a,d,coupling.ports[d][a[3]])
                        if inside(target):
                            term=coupling.weights[d][a[3]]*v.b
                            if term:
                                count+=1
                                if first_term is None:first_term={'update':t+1,'source':list(a),'target':list(target),'term':term}
                term_counts.append(count)
            active=all(n>0 for n in activity);isolated=not any(term_counts)
            region_id=f'{identity}-R{radius}'
            regions.append({'id':region_id,'source_case':identity,'radius':radius,'center':list(center),
                'complete_nodes':(2*radius+1)**3,'complete_triples':48*(2*radius+1)**3,
                'nonzero_counter_counts':activity,'external_nonzero_term_counts':term_counts,
                'first_external_term':first_term,'active_every_state':active,'isolated_all_updates':isolated})
            for period in p['periods']:
                mismatch=None
                for k in range(len(frames)-period):
                    if frames[k]!=frames[k+period]:
                        a=next(a for a in sorted(frames[k].keys()|frames[k+period].keys())
                            if frames[k].get(a,states[0].background)!=frames[k+period].get(a,states[0].background))
                        mismatch={'state':p['start_state']+k,'compared_state':p['start_state']+k+period,'address':list(a),
                            'before':list(frames[k].get(a,states[0].background)),'after':list(frames[k+period].get(a,states[0].background))}
                        break
                enough=(p['end_state']-p['start_state'])//period>=3
                periodic=mismatch is None
                tests.append({'region':region_id,'period':period,'at_least_three_periods':enough,'full_region_periodic':periodic,
                    'first_mismatch':mismatch,'active_every_state':active,'isolated_all_updates':isolated,
                    'discovery_candidate':enough and periodic and active and isolated})
            if time.process_time()-start>p['budget']['max_cpu_seconds']:raise TimeoutError('Passive analysis CPU budget reached')
    result={**registration,'status':'completed','source_records':records,'regions':regions,'tests':tests,
        'test_count':len(tests),'discovery_candidates':sum(t['discovery_candidate'] for t in tests),
        'cpu_seconds':time.process_time()-start,'original_activation_verdict_unchanged':True,
        'scope':'Post-capture discovery scan only; any hit requires a separately frozen validation.'}
    (output/'result.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    size=sum(f.stat().st_size for f in output.iterdir() if f.is_file())
    if size>p['budget']['max_recorded_bytes']:raise RuntimeError('Passive artifact budget exceeded')
    print(canonical({'tests':len(tests),'candidates':result['discovery_candidates'],'cpu_seconds':result['cpu_seconds'],'bytes':size,'new_updates':0}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
