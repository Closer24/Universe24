"""Independent full-state audit of initial clock-region counterfactuals."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import time
from research.clock_selection import audit_v2 as previous
from research.clock_selection.audit import (ROOT,Snapshot,load,file_digest,native_digest,geometry,audit_record,canonical)
from research.staged_blocks.audit import read_states

PROTOCOL_SHA='8211d2fc55294d8453cc1816f2b2e7475b65864650e60d52f67167ac2b93a4bb'
PARENT_AUDIT_SHA='8b303f68e6663c7d14582204b280c2079d7a1ab3a038a6c978d2fbb6900d16c2'

def planned():
    return [dict(id=f'mediation-L{L}-gap{gap}-E{E}-R{R}',side=L,gap=gap,exterior_source=E,region_source=R)
        for L,gap,E,R in itertools.product((337,353),(36,38),('01','11'),('01','11'))]

def observed(case,states):
    adjusted=dict(side=case['side'],gap=case['gap']-40,writer_delay=2,stage='encounter',control='11',
        clock_present=True,clock_remainder=0,phase=0,guide_target_channel=0,compensation_direction=None)
    out=previous.observations(adjusted,states)
    del out['hold'];del out['initial_active_counter_count']
    out['incoming']=[dict(step=v['step'],match=v['match']) for v in out['incoming']]
    out['initial_hold']=dict(complete_region_period4=out['region_trace'][0]==out['region_trace'][4],
        center_unit_counter_norm=all(a*a+b*b==1 for a,b,r in out['center_trace'][:5]),
        other_counter_pairs_zero=all(not any(v[:2]) for frame in out['region_trace'][:5] for i,v in enumerate(frame) if i!=2),
        every_external_term_zero=all(not row['nonzero_external_terms'] for row in out['boundary_inputs'][:4]))
    return out

def assess(case,out,split,native):
    pred=case['gap']==(38 if case['region_source']=='11' else 36)
    carrier=all(v['match'] for v in out['registered_output']);raw=out['registered_output_C']==out['expected_output_C']
    margin=out['initial_active_boundary_margin']
    return dict(split_equivalence=all(split.values()),incoming_contract=all(v['match'] for v in out['incoming']),
        near_incoming_contract=all(v['match'] for v in out['near_incoming']),initial_hold=all(out['initial_hold'].values()),
        strict_initial_causal_margin=margin is None or margin>48,no_active_boundary_contact=not out['active_boundary_hits'],
        native_suffix_equal=native,predicted_output=pred,exact_output_carrier=carrier,exact_output_C_signature=raw,
        carrier_follows_region=carrier==pred,C_follows_region=raw==pred)

def assess_group(rows):
    cases={r['case']['exterior_source']+'/'+r['case']['region_source']:r['assessment'] for r in rows}
    complete=set(cases)=={'01/01','01/11','11/01','11/11'}
    eligible=complete and all(a[k] for a in cases.values() for k in ('split_equivalence','incoming_contract',
        'near_incoming_contract','initial_hold','strict_initial_causal_margin','no_active_boundary_contact'))
    native=all(cases[k]['native_suffix_equal'] is True for k in ('01/01','11/11'))
    carrier=all(v['carrier_follows_region'] for v in cases.values());raw=all(v['C_follows_region'] for v in cases.values())
    return dict(side=rows[0]['case']['side'],gap=rows[0]['case']['gap'],complete_control_group=complete,eligible=eligible,
        native_suffix_controls_pass=native,all_full_state_inverses=True,carrier_follows_region_all_exteriors=carrier,
        C_follows_region_all_exteriors=raw,accepted_clock_region_mediation=eligible and native and carrier and raw,cases=cases)

def audit(study,output,budget=300):
    study,output=Path(study),Path(output);assert not output.exists();start=time.process_time()
    report=dict(passed=False,auditor_sha256=file_digest(__file__),helper_sha256=file_digest(previous.__file__),
        protocol_sha256=PROTOCOL_SHA,parent_audit_sha256=PARENT_AUDIT_SHA,records=[],groups=[],failure=None)
    try:
        protocol,result,registration=(load(study/f) for f in ('protocol.json','result.json','registration.json'))
        assert file_digest(study/'protocol.json')==registration['protocol_sha256']==PROTOCOL_SHA
        assert file_digest(study/'parent_independent_audit.json')==registration['parent_audit_sha256']==PARENT_AUDIT_SHA
        assert load(study/'parent_independent_audit.json')['passed'] is True
        assert registration['cases']==planned() and result['registered_cases']==result['completed_cases']==16
        assert result['not_run_cases']==[] and result['status']=='completed'
        manifest=load(study/'source_provenance'/'manifest.json')
        for path,sha in manifest['source_sha256'].items():
            assert file_digest(ROOT/path)==file_digest(study/'source_provenance'/'source'/path)==sha,path
        parent_study=ROOT/protocol['parent']['study'];parent_ledger={r['id']:r for r in load(parent_study/'result.json')['cases']}
        grouped=[];parent_cache={}
        for case,entry in zip(planned(),result['cases']):
            assert entry['case']==case
            file=study/entry['record'];assert file_digest(file)==entry['record_gzip_sha256']
            raw=gzip.decompress(file.read_bytes());assert hashlib.sha256(raw).hexdigest()==entry['record_sha256']
            record=json.loads(raw);assert record['case']==case and record['protocol_sha256']==PROTOCOL_SHA
            key=(case['side'],case['gap'])
            if key not in parent_cache:
                originals={};metadata={}
                for mask in ('01','11'):
                    identity=f'write-probe-L{case["side"]}-r0-p0-d2-gap{case["gap"]}-clock1-{mask}'
                    source=parent_ledger[identity];path=parent_study/source['record']
                    assert file_digest(path)==source['record_gzip_sha256']
                    source_raw=gzip.decompress(path.read_bytes());assert hashlib.sha256(source_raw).hexdigest()==source['record_sha256']
                    originals[mask]=read_states(json.loads(source_raw)['experiment'])
                    metadata[mask]=dict(record=str(path.relative_to(ROOT)),record_gzip_sha256=file_digest(path),
                        record_sha256=hashlib.sha256(source_raw).hexdigest(),anchor_state_sha256=native_digest(originals[mask][40]))
                parent_cache[key]=(originals,metadata)
            originals,metadata=parent_cache[key];assert record['source_records']==metadata
            nodes=geometry(case)[4-1];region={(*n,g) for n in nodes for g in range(48)};assert len(region)==336
            E,R=case['exterior_source'],case['region_source'];exterior=originals[E][40];inside=originals[R][40]
            cells={a:v for a,v in exterior.cells.items() if a not in region}
            cells.update({a:inside.at(a) for a in region});expected=Snapshot(case['side'],(0,0,2),cells)
            integrity,states=audit_record({k:v for k,v in record.items() if k!='observations'},expected_initial=expected,deadline=start+budget)
            split=dict(region_equal_source=all(states[0].at(a)==inside.at(a) for a in region),
                outside_equal_source=all(states[0].at(a)==exterior.at(a) for a in set(states[0].cells)|set(exterior.cells) if a not in region),
                finalized_initial_equal=states[0]==expected)
            assert split==record['split_checks']
            out=observed(case,states)
            assert out==record['observations'],[k for k in out if out[k]!=record['observations'].get(k)]
            native=states==originals[E][40:89] if E==R else None
            assessment=assess(case,out,split,native);assert assessment==entry['assessment']==record['assessment']
            report['records'].append(dict(case=case,integrity=integrity,assessment=assessment,source_records=metadata))
            grouped.append(dict(case=case,assessment=assessment,saved_group=record['group_assessment']))
            if len(grouped)==4:
                group=assess_group(grouped);assert all(r['saved_group']==group for r in grouped)
                assert result['groups'][len(report['groups'])]==group;report['groups'].append(group);grouped=[]
            print(canonical({'audited_mediation_records':len(report['records']),'registered':16}),flush=True)
        assert not grouped and result['accepted_groups']==sum(g['accepted_clock_region_mediation'] for g in report['groups'])
        report.update(passed=True,full_states=16*49,transitions=16*48,full_rewinds=16,
            accepted_groups=result['accepted_groups'],scope=protocol['claim'],sources_unchanged=True)
    except Exception as exc:report['failure']=f'{type(exc).__name__}: {exc}'
    report['cpu_seconds']=time.process_time()-start;output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    report=audit(args.study,args.output);print(canonical({k:report[k] for k in ('passed','failure','cpu_seconds')}))
    raise SystemExit(0 if report['passed'] else 1)
