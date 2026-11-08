"""Independent exact-matrix replay of all registered integer-donor masks."""
from __future__ import annotations
import argparse,itertools,json,time
from collections import Counter
from pathlib import Path
from research.clock_selection.audit import (ROOT,Snapshot,load,file_digest,digest,canonical,coupling,DIRECTIONS,audit_record,all_events)

PROTOCOL_SHA='890abeac74ae4bc164b5cec832901230f2ddcc2c763ddb7d189cc9be459d662d'

def geometry(side):
    c=side//2;center=(c,c,c,0);matrix=coupling((1,1,1))
    neighbors=[(*(c+delta[j] for j in range(3)),matrix.ports[d][0]) for d,delta in enumerate(DIRECTIONS)]
    assert len(set(neighbors))==6
    for d,a in enumerate(neighbors): assert matrix.ports[d^1][a[3]]==0 and matrix.weights[d][0]==1
    return center,neighbors

def planned():
    return [dict(id=f'single-L{L}-A{A}',family='single',side=L,amplitude=A) for L,A in itertools.product((29,33),range(-6,7))]+[
        dict(id=f'six-L29-M{mask}',family='six',side=29,mask=mask) for mask in range(64)]

def expected_initial(case):
    center,neighbors=geometry(case['side'])
    cells={center:(0,case['amplitude'],2)} if case['family']=='single' else {
        a:(0,1 if case['mask']&(1<<d) else 0,2) for d,a in enumerate(neighbors)}
    return Snapshot(case['side'],(0,0,2),cells)

def analysis(case,states):
    center,neighbors=geometry(case['side']);events=all_events(states)[0]
    u=case['amplitude'] if case['family']=='single' else case['mask'].bit_count()
    quotient=(2*u+2)//6;remainder=2*u+2-6*quotient;kind=u%3 if quotient else None
    targets=neighbors if case['family']=='single' else [center]
    target_ok=all(states[1].at(a)==(0,quotient,remainder) for a in targets)
    first=[e for e in events if e['step']==1]
    if case['family']=='single':
        actual={(tuple(e['address']),e['kind'],int(e['quotient'])) for e in first}
        wanted={(a,kind,quotient) for a in neighbors} if quotient else set();event_ok=actual==wanted
    else:
        actual=[e for e in first if tuple(e['address'])==center]
        wanted=[dict(step=1,address=list(center),kind=kind,quotient=str(quotient))] if quotient else [];event_ok=actual==wanted
    Q=[sum(6*(b-a)+r-2 for a,b,r in s.cells.values()) for s in states]
    c=case['side']//2;radius=0 if case['family']=='single' else 1
    support=all(sum(abs(a[j]-c) for j in range(3))<=radius+t for t,s in enumerate(states) for a in s.cells)
    boundary=[[t,list(a)] for t,s in enumerate(states) for a in s.cells if any(a[j] in (0,s.side-1) for j in range(3))]
    checks=dict(first_step_target_exact=target_ok,first_step_C_exact=event_ok,initial_Q_exact=Q[0]==6*u,
        Q_conserved=len(set(Q))==1,causal_support_bound=support,no_boundary_contact=not boundary,full_inverse=True)
    if case['family']=='single':checks['source_quarter_turn']=states[1].at(center)==(u,0,2)
    centered=[[[x-c,y-c,z-c,g,*v] for (x,y,z,g),v in sorted(s.cells.items())] for s in states]
    return dict(id=case['id'],case=case,checks=checks,all_checks=all(checks.values()),
        first_step_prediction=dict(u=u,ell=quotient,r_next=remainder,C_kind=kind),first_step_world_C=first,
        world_C=events,world_C_counts={str(k):v for k,v in sorted(Counter(e['kind'] for e in events).items())},
        Q_trace=[str(v) for v in Q],boundary_contacts=boundary,centered_frame_sha256=[digest(f) for f in centered])

def audit(study,output,budget=180):
    study,output=Path(study),Path(output);assert not output.exists();start=time.process_time()
    report=dict(passed=False,auditor_sha256=file_digest(__file__),protocol_sha256=PROTOCOL_SHA,records=[],failure=None)
    try:
        p,result,registration,specs=(load(study/f) for f in ('protocol.json','result.json','registration.json','specs.json'))
        assert file_digest(study/'protocol.json')==registration['protocol_sha256']==PROTOCOL_SHA
        assert file_digest(study/'producer.py')==file_digest(ROOT/'research/clock_selection/parallel_division.py')==registration['producer_sha256']
        assert file_digest(study/'specs.json')==registration['specs_sha256']
        assert result['completed_cases']==result['registered_cases']==90 and not result['not_run'] and not result['errors']
        assert len(specs)==len(result['cases'])==len(registration['cases'])==90
        for path,sha in registration['source_sha256'].items():assert file_digest(ROOT/path)==sha,path
        centered={}
        for case,spec,entry,registered in zip(planned(),specs,result['cases'],registration['cases']):
            assert spec['controls']==entry['case']==case and digest(spec)==registered['spec_sha256']
            path=study/entry['record'];assert file_digest(path)==entry['record_sha256'];row=load(path)
            recorded=row['recorded'];assert recorded['spec_sha256']==digest(spec)
            integrity,states=audit_record(dict(recorded,spec=spec),expected_initial=expected_initial(case),deadline=start+budget)
            assert digest(recorded['assembly'])==registered['manifest_sha256']
            out=analysis(case,states);assert out==row['analysis'],[k for k in out if out[k]!=row['analysis'].get(k)]
            saved={k:v for k,v in entry.items() if k not in ('record','record_sha256')}
            assert saved=={k:v for k,v in out.items() if k!='world_C'}
            centered[case['id']]=out['centered_frame_sha256']
            report['records'].append(dict(case=case,integrity=integrity,checks=out['checks'],first_step_prediction=out['first_step_prediction']))
        comparisons=[dict(amplitude=A,complete=True,equal=centered[f'single-L29-A{A}']==centered[f'single-L33-A{A}']) for A in range(-6,7)]
        assert comparisons==result['cross_size_comparisons'] and all(v['equal'] for v in comparisons)
        assert all(all(r['checks'].values()) for r in report['records']) and result['all_case_checks'] is True
        report.update(passed=True,full_states=1170,transitions=1080,full_rewinds=90,cross_size_comparisons=comparisons,
            scope='Finite arithmetic fanout and parallel-sum demonstration; no physical photon or route preference inferred.')
    except Exception as exc:report['failure']=f'{type(exc).__name__}: {exc}'
    report['cpu_seconds']=time.process_time()-start;output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    report=audit(args.study,args.output);print(canonical({k:report[k] for k in ('passed','failure','cpu_seconds')}))
    raise SystemExit(0 if report['passed'] else 1)
