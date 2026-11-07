"""Fresh finite-halo confirmation; v1 files are retained without modification."""
from __future__ import annotations
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import subprocess
import time

from universe24.core import Coupling, Cube, Engine, State
from universe24.experiments.config import checkpoint_data
from .structure_study import ROOT, canonical, digest_state, put_pair, project

PROTOCOL = Path(__file__).with_name('structure_protocol_v2.json')


def torus_distance(position, target, side):
    return sum(min(abs(a-b), side-abs(a-b)) for a,b in zip(position,target))


def run_case(side, signs, phase, count, protocol, start):
    origin=(side//2,)*3
    positions=[(origin[0]+j,origin[1],origin[2]) for j in range(count)]
    a,b=phase
    cells={}
    for position in positions:
        put_pair(cells,position,[(a,b,0),(-a,-b,4)])
    initial=State(Cube(side),cells=cells)
    engine=Engine(Coupling(signs))
    states=[initial]
    state=initial
    inverse=True
    for _ in range(protocol['steps']):
        if time.process_time()-start>protocol['budget']['cpu_seconds']:
            raise TimeoutError('Registered CPU budget exceeded')
        if len(state.cells)>protocol['budget']['max_sparse_channels']:
            raise TimeoutError('Registered sparse support budget exceeded')
        nxt=engine.advance(state)
        inverse &= engine.rewind(nxt)==state
        states.append(nxt)
        state=nxt
    restored=state
    for _ in range(protocol['steps']):
        restored=engine.rewind(restored)
    inverse &= restored==initial
    first=next((t for t in range(1,protocol['first_return_search']+1) if states[t]==initial),None)
    repeats=bool(first and all(states[t]==states[t+first] for t in range(len(states)-first)))
    max_radius=max(min(torus_distance(addr[:3],p,side) for p in positions) for s in states for addr in s.cells)
    min_boundary=min(min(v,side-1-v) for s in states for addr in s.cells for v in addr[:3])
    halo_only_remainders=all(triple.a==0 and triple.b==0 for s in states for addr,triple in s.cells.items() if addr[:3] not in positions)
    result={
        'side':side,'signs':list(signs),'phase':list(phase),'motif_sites':count,
        'coupling_fingerprint':engine.coupling.fingerprint,
        'initial':checkpoint_data(initial,engine,0),'final':checkpoint_data(state,engine,protocol['steps']),
        'first_full_state_return':first,'all_sampled_period_repetitions':repeats,
        'max_complete_state_radius':max_radius,'radius_one_pass':max_radius<=1,
        'halo_contains_only_remainder_changes':halo_only_remainders,
        'minimum_active_boundary_distance':min_boundary,
        'max_sparse_channels':max(len(s.cells) for s in states),
        'all_one_step_and_full_inverses':inverse,
        'finite_cluster_pass':bool(first is not None and repeats and max_radius<=1 and inverse),
        'trace_sha256':[digest_state(s) for s in states],
        'target_trace':[project(s,positions) for s in states],
    }
    assert inverse
    return result,states


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists(): raise FileExistsError(f'Refusing to overwrite {args.output}')
    protocol=json.loads(PROTOCOL.read_text())
    files=sorted((ROOT/'universe24').rglob('*.py'))+[Path(__file__).resolve(),PROTOCOL,Path(__file__).with_name('structure_study.py')]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    result={'protocol':protocol,'source_sha256':hashes,'python':platform.python_version(),
            'checkout_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'working_tree_dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT)),
            'execution_status':'completed','cases':[]}
    start=time.process_time()
    try:
        for side in protocol['sides']:
            for signs in product((-1,1),repeat=3):
                for phase in protocol['initial_preparation']['channel0_counter_phases']:
                    isolated,isolated_states=run_case(side,signs,phase,1,protocol,start)
                    adjacent,adjacent_states=run_case(side,signs,phase,2,protocol,start)
                    origin=(side//2,)*3
                    adjacent['first_target_difference_from_isolated']=next((t for t in range(protocol['steps']+1)
                        if any(adjacent_states[t].at((origin[0]+j,*origin[1:],g))!=isolated_states[t].at((*origin,g))
                               for j in (0,1) for g in (0,14))),None)
                    result['cases'] += [isolated,adjacent]
    except TimeoutError as error:
        result.update(execution_status='inconclusive',reason=str(error))
    result['cpu_seconds']=time.process_time()-start
    result['case_count']=len(result['cases'])
    result['finite_clusters_passed']=sum(c['finite_cluster_pass'] for c in result['cases'])
    result['all_completed_full_inverses_pass']=all(c['all_one_step_and_full_inverses'] for c in result['cases'])
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as handle:
        json.dump(result,handle,indent=2);handle.write('\n')
    print(json.dumps({k:result[k] for k in ('execution_status','case_count','finite_clusters_passed','all_completed_full_inverses_pass','cpu_seconds')},indent=2))
    if result['execution_status']!='completed':raise SystemExit(2)


if __name__=='__main__':main()
