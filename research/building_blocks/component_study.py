"""Prepared source-driven components; the engine and observer semantics are unchanged."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

from universe24 import Channel, Coupling, Cube, Engine, State

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def state_rows(state, origin):
    return sorted([[a[0]-origin[0], a[1]-origin[1], a[2]-origin[2], a[3], *v]
                   for a, v in state.cells.items()])


def prepare(case, coupling):
    n, side = case['N'], case['L']
    origin = (side//2-n//2, side//2, side//2)
    x, y, z = origin
    cells = {}
    for j in range(1, n+1):
        cells[(x+j,y,z,0)] = Channel(0,0,4)
        cells[(x+j,y,z,14)] = Channel(0,0,0)
    if case.get('data', True):
        a,b = case.get('source_ab', [0,1])
        cells[(x,y,z,0)] = Channel(a,b,2)
        cells[(x,y,z,14)] = Channel(-a,-b,2)
    if 'target_remainders' in case:
        for j in case['targets']:
            for g,r in zip((0,14),case['target_remainders']):
                cells[(x+j,y,z,g)] = Channel(0,0,r)
    if 'gate_j' in case:
        k=case['gate_j']
        cells.pop((x+k,y,z,0),None)
        cells.pop((x+k,y,z,14),None)
        if case.get('control',False):
            a,b=case['control_ab']; amp=case['control_amplitude']
            cells[(x+k,y+1,z,coupling.ports[2][0])] = Channel(amp*a,amp*b,2)
            cells[(x+k,y+1,z,coupling.ports[2][14])] = Channel(-amp*a,-amp*b,2)
    return State(Cube(side),cells=cells), origin


def first_run(values):
    start=next((i for i,v in enumerate(values) if v), None)
    if start is None:
        return None
    stop=next((i for i in range(start+1,len(values)) if not values[i]),len(values))
    return [start,stop]


def run_case(case, engine, protocol, start_cpu, start_wall):
    def budget():
        if time.process_time()-start_cpu > protocol['budget']['cpu_seconds']:
            raise RuntimeError('CPU budget exceeded')
        if time.monotonic()-start_wall > protocol['budget']['wall_seconds']:
            raise RuntimeError('wall budget exceeded')
    initial, origin = prepare(case,engine.coupling)
    state=initial
    traces={str(j):[] for j in case['targets']}
    state_hashes=[]
    max_cells=0
    inverse_ok=True
    all_static=True
    minimum_boundary_margin=case['L']
    gate_witness=None
    for t in range(case['steps']+1):
        budget()
        if len(state.cells)>protocol['budget']['max_explicit_channels']:
            raise RuntimeError('explicit-channel budget exceeded')
        max_cells=max(max_cells,len(state.cells))
        all_static &= state==initial
        if state.cells:
            minimum_boundary_margin=min(minimum_boundary_margin,
                min(min(v,case['L']-1-v) for addr in state.cells for v in addr[:3]))
        state_hashes.append(digest(state_rows(state,origin)))
        for j in case['targets']:
            p=(origin[0]+j,origin[1],origin[2])
            c0=state.at((*p,0)); c14=state.at((*p,14))
            traces[str(j)].append([t,*c0,*c14,int(c0.r==0 and c14.r==4)])
        if 'gate_j' in case and t==case['gate_j']-1:
            p=(origin[0]+case['gate_j'],origin[1],origin[2])
            c0=state.at((*p,0));c14=state.at((*p,14))
            inputs=engine.input_sums(state)
            gate_witness={'t':t,'g0':list(c0),'g14':list(c14),
                          'u0':inputs.get((*p,0),0),'u14':inputs.get((*p,14),0),
                          'rest_armed_zero_input':c0==Channel(0,0,4) and c14==Channel(0,0,0)
                            and inputs.get((*p,0),0)==0 and inputs.get((*p,14),0)==0}
        if t<case['steps']:
            next_state=engine.advance(state)
            inverse_ok &= engine.rewind(next_state)==state
            state=next_state
    final=state
    for _ in range(case['steps']):
        budget();state=engine.rewind(state)
    outputs={}
    phases=((0,1),(1,0),(0,-1),(-1,0))
    for j in case['targets']:
        trace=traces[str(j)]
        end=2*(case['N']+1)-j
        outputs[str(j)]={
            'first_activation':next((r[0] for r in trace if r[2]!=0),None),
            'clicks':[b[0] for a,b in zip(trace,trace[1:]) if a[7]==0 and b[7]==1],
            'first_memory_run':first_run([r[7] for r in trace]),
            'window':[j,end],
            'expected_window_samples':end-j,
            'record_first_window_exact':all(r[7]==int(j<=r[0]<end) for r in trace if r[0]<=end),
            'clock_first_window_exact':all(tuple(r[1:3])==phases[(r[0]-j)%4] and
                 tuple(r[4:6])==tuple(-v for v in phases[(r[0]-j)%4])
                 for r in trace if j<=r[0]<end),
            'trace_columns':['t','a0','b0','r0','a14','b14','r14','M'],
            'trace':trace}
    return {'preparation':case,'initial_sha256':state_hashes[0],
            'final_sha256':digest(state_rows(final,origin)),
            'normalized_full_trace_sha256':digest(state_hashes),
            'full_one_step_inverses':inverse_ok,'full_rewind':state==initial,
            'all_states_equal_initial':all_static,'max_explicit_channels':max_cells,
            'minimum_nonbackground_boundary_margin':minimum_boundary_margin,
            'gate_before_data_arrival':gate_witness,'targets':outputs}


def composition_accept(result):
    return all(v['first_activation']==int(j) and v['record_first_window_exact'] and
               v['clock_first_window_exact'] for j,v in result['targets'].items())


def clutch_verdict(results, gate):
    target=str(gate+3)
    outcomes={(r['preparation']['data'],r['preparation']['control']):r for r in results}
    both=outcomes[True,True]['targets'][target]
    interval=both['first_memory_run']
    only_both=(bool(both['clicks']) and both['clicks'][0]<=gate+8 and interval is not None and
               interval[1]-interval[0]>=4 and
               all(not outcomes[key]['targets'][target]['clicks'] for key in ((False,False),(True,False),(False,True))))
    stored=only_both and outcomes[False,True]['gate_before_data_arrival']['rest_armed_zero_input']
    return {'only_both_sources_record':only_both,'stored_control_before_arrival':stored,
            'target_first_clicks':{f'data_{int(d)}_control_{int(c)}':outcomes[d,c]['targets'][target]['clicks']
                                   for d,c in outcomes}}


def study(protocol):
    start_cpu=time.process_time();start_wall=time.monotonic()
    engine=Engine(Coupling(tuple(protocol['signs'])))
    results={'composition':[],'perturbations':[],'clutch_candidates':[],'clutch_holdouts':[]}
    failure=None
    try:
        for spec in protocol['composition_cases']:
            for data in (True,False):
                case=dict(spec,data=data,id=spec['id']+('_source' if data else '_no_source'))
                result=run_case(case,engine,protocol,start_cpu,start_wall)
                result['criterion_pass']=composition_accept(result) if data else result['all_states_equal_initial']
                results['composition'].append(result)
        family=protocol['perturbation_family']
        for ab in family['source_ab']:
            for remainders in family['target_remainder_pairs']:
                case={k:family[k] for k in ('N','L','targets','steps')}
                case.update(id=f'perturb_ab{ab}_r{remainders}',source_ab=ab,target_remainders=remainders)
                result=run_case(case,engine,protocol,start_cpu,start_wall)
                result['criterion_pass']=composition_accept(result)
                results['perturbations'].append(result)
        family=protocol['clutch_search']
        for gate in family['gate_j']:
            for ab in family['control_ab']:
                for amp in family['control_amplitude']:
                    trial=[]
                    for data in (False,True):
                        for control in (False,True):
                            case={k:family[k] for k in ('N','L','steps')}
                            case.update(id=f'clutch_k{gate}_ab{ab}_amp{amp}_d{int(data)}_c{int(control)}',
                                targets=[gate+3],gate_j=gate,control_ab=ab,control_amplitude=amp,data=data,control=control)
                            trial.append(run_case(case,engine,protocol,start_cpu,start_wall))
                    verdict=clutch_verdict(trial,gate)
                    results['clutch_candidates'].append({'gate_j':gate,'control_ab':ab,'control_amplitude':amp,
                        **verdict,'runs':trial})
        for candidate in results['clutch_candidates']:
            if not candidate['stored_control_before_arrival']:
                continue
            gate=candidate['gate_j']+4
            trial=[]
            for data in (False,True):
                for control in (False,True):
                    case={'N':family['N']+4,'L':family['L']+20,'steps':family['steps'],
                          'id':f'holdout_k{gate}_ab{candidate["control_ab"]}_amp{candidate["control_amplitude"]}_d{int(data)}_c{int(control)}',
                          'targets':[gate+3],'gate_j':gate,'control_ab':candidate['control_ab'],
                          'control_amplitude':candidate['control_amplitude'],'data':data,'control':control}
                    trial.append(run_case(case,engine,protocol,start_cpu,start_wall))
            results['clutch_holdouts'].append({'parent_gate_j':candidate['gate_j'],'gate_j':gate,
                'control_ab':candidate['control_ab'],'control_amplitude':candidate['control_amplitude'],
                **clutch_verdict(trial,gate),'runs':trial})
    except RuntimeError as exc:
        failure=str(exc)
    all_runs=results['composition']+results['perturbations']+[
        r for group in ('clutch_candidates','clutch_holdouts') for trial in results[group] for r in trial['runs']]
    summary={
        'execution_status':'completed' if failure is None else 'inconclusive',
        'budget_failure':failure,'run_count':len(all_runs),
        'forward_steps':sum(r['preparation']['steps'] for r in all_runs),
        'all_full_inverses':all(r['full_one_step_inverses'] and r['full_rewind'] for r in all_runs),
        'composition_cases_passed':sum(r['criterion_pass'] for r in results['composition']),
        'composition_cases_total':len(results['composition']),
        'perturbation_cases_passed':sum(r['criterion_pass'] for r in results['perturbations']),
        'perturbation_cases_total':len(results['perturbations']),
        'coincidence_candidates':sum(r['only_both_sources_record'] for r in results['clutch_candidates']),
        'stored_control_candidates':sum(r['stored_control_before_arrival'] for r in results['clutch_candidates']),
        'stored_control_holdouts_passed':sum(r['stored_control_before_arrival'] for r in results['clutch_holdouts']),
        'stored_control_holdouts_total':len(results['clutch_holdouts']),
        'all_observed_support_away_from_boundary':all(r['minimum_nonbackground_boundary_margin']>1 for r in all_runs),
        'cpu_seconds':time.process_time()-start_cpu,'wall_seconds':time.monotonic()-start_wall}
    return {'summary':summary,**results}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'component_results.json')
    args=parser.parse_args()
    if args.output.exists():
        raise SystemExit(f'Refusing to overwrite {args.output}; choose a new output path')
    raw=(HERE/'component_protocol.json').read_bytes();protocol=json.loads(raw)
    results=study(protocol)
    results.update(protocol_id=protocol['protocol_id'],protocol_sha256=hashlib.sha256(raw).hexdigest(),
        engine_commit=protocol['engine_commit'],python=platform.python_version(),random_seed=None,
        coupling_fingerprint=Coupling(tuple(protocol['signs'])).fingerprint,
        source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted((ROOT/'universe24').rglob('*.py'))},
        runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.write_text(json.dumps(results,separators=(',',':'))+'\n')
    print(json.dumps(results['summary'],indent=2))
    if results['summary']['execution_status']!='completed' or not results['summary']['all_full_inverses']:
        raise SystemExit(1)

if __name__=='__main__':
    main()
