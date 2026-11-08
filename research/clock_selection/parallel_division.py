"""Preregistered initial-only Rule3 fanout demonstration; no new evolution law.

Prepare without evolution, obtain approval, then run the immutable registration:
python -m research.clock_selection.parallel_division --prepare --output NEW_DIR
python -m research.clock_selection.parallel_division --run --output SAME_DIR
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import time

from research.experiments.run import assemble, canonical, digest, recorded_states, run_experiment, source_hashes
from research.presenter.export import bundle
from research.presenter.build import build
from universe24 import Coupling
from universe24.core.state import Cube
from universe24.observation.clicks import classify

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'parallel_division_protocol.json'
ROOT = HERE.parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.write_text(canonical(value) + '\n', encoding='ascii')


def geometry(side):
    c = side // 2
    center = (c,c,c,0)
    cube, tensor = Cube(side), Coupling((1,1,1))
    neighbors = [cube.adjacent(center,d,tensor.ports[d][0]) for d in range(6)]
    assert len(set(neighbors)) == 6
    for d, address in enumerate(neighbors):
        assert cube.adjacent(address,d^1,tensor.ports[d^1][address[3]]) == center
        assert tensor.weights[d][0] == tensor.weights[d^1][address[3]] == 1
    return center, neighbors


def spec(case, protocol_sha):
    center, neighbors = geometry(case['side'])
    if case['family'] == 'single':
        cells = [[*center,0,case['amplitude'],2]]
        label = f"One donor b={case['amplitude']}: six recipients"
    else:
        cells = [[*address,0,1 if case['mask'] & (1<<d) else 0,2]
                 for d,address in enumerate(neighbors)]
        label = f"Six donor mask {case['mask']}: {case['mask'].bit_count()} prepared units"
    return {'format':'universe24-assembly-experiment-v1','id':case['id'],
            'title':label,'description':'Unchanged Rule3; initial counters only. Native C classes are passive arithmetic labels, not route selection or physical photons.',
            'question':'Compare integer division, simultaneous inputs and every native C event.',
            'board':{'side':case['side'],'background':[0,0,2],'body_signs':[1,1,1]},
            'steps':12,'components':[{'name':'preparation','recipe':'Patch','at':[0,0,0],
            'params':{'kind':'parallel-initial-donors','cells':cells,
                      'ports':{'target':[center],'neighbors':neighbors}}}],
            'detectors':[],'view':{'port':'preparation.target'},'controls':case,
            'seed':None,'provenance':{'protocol_sha256':protocol_sha,'initial_only':True},
            'budget':{'max_frames':13,'max_cells':200000,'max_bytes':2097152,'max_seconds':10}}


def cases(protocol):
    result = []
    for side in protocol['single_donor']['sides']:
        for amplitude in protocol['single_donor']['amplitudes']:
            result.append({'id':f'single-L{side}-A{amplitude}','family':'single','side':side,'amplitude':amplitude})
    for mask in range(64):
        result.append({'id':f'six-L29-M{mask}','family':'six','side':29,'mask':mask})
    return result


def prepare(output):
    output.mkdir(parents=True,exist_ok=False)
    protocol_raw = PROTOCOL.read_bytes()
    protocol = json.loads(protocol_raw)
    protocol_sha = sha(protocol_raw)
    definitions = [spec(case,protocol_sha) for case in cases(protocol)]
    # Pure immutable assembly only. Neither Engine.advance nor Engine.rewind is called.
    checks = []
    for definition in definitions:
        prepared = assemble(definition)
        checks.append({'id':definition['id'],'manifest_sha256':digest(prepared.manifest),
                       'spec_sha256':digest(definition),'initial_cells':len(prepared.initial.cells)})
    (output/'protocol.json').write_bytes(protocol_raw)
    (output/'producer.py').write_bytes(Path(__file__).read_bytes())
    write(output/'specs.json',definitions)
    registration = {'format':'universe24-parallel-division-registration-v1',
                    'created_utc':datetime.now(timezone.utc).isoformat(),
                    'protocol_sha256':protocol_sha,'producer_sha256':sha(Path(__file__).read_bytes()),
                    'specs_sha256':sha((output/'specs.json').read_bytes()),
                    'source_sha256':source_hashes(),
                    'checkout_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                    'cases':checks,'evolution_steps_performed':0}
    write(output/'registration.json',registration)
    print(canonical({k:v for k,v in registration.items() if k not in ('source_sha256','cases')}))


def centered_state(state):
    c = state.cube.side // 2
    return [[x-c,y-c,z-c,g,v.a,v.b,v.r] for (x,y,z,g),v in sorted(state.cells.items())]


def assess(definition, recorded):
    case = definition['controls']
    states = recorded_states(recorded['experiment'])
    center, neighbors = geometry(case['side'])
    events = []
    for t,(before,after) in enumerate(zip(states,states[1:]),1):
        for address in sorted(before.cells.keys() | after.cells.keys()):
            event = classify(before.at(address),after.at(address))
            if event is not None:
                kind, quotient = event
                events.append({'step':t,'address':list(address),'kind':kind,'quotient':str(quotient)})
    u = case['amplitude'] if case['family']=='single' else case['mask'].bit_count()
    ell,r = divmod(2*u+2,6)
    expected = (0,ell,r)
    target_addresses = neighbors if case['family']=='single' else [center]
    first_target = all(states[1].at(a)==expected for a in target_addresses)
    expected_kind = u % 3 if ell else None
    first_events = [e for e in events if e['step']==1]
    if case['family']=='single':
        actual = {(tuple(e['address']),e['kind'],int(e['quotient'])) for e in first_events}
        wanted = {(a,expected_kind,ell) for a in neighbors} if ell else set()
        first_C = actual == wanted
        source_rotation = states[1].at(center) == (u,0,2)
    else:
        actual = [e for e in first_events if tuple(e['address'])==center]
        wanted = [{'step':1,'address':list(center),'kind':expected_kind,'quotient':str(ell)}] if ell else []
        first_C = actual == wanted
        source_rotation = None
    q = [sum(6*(v.b-v.a)+v.r-2 for v in state.cells.values()) for state in states]
    c = case['side']//2
    radius = 0 if case['family']=='single' else 1
    support_ok = all(sum(abs(a[j]-c) for j in range(3)) <= radius+t
                     for t,state in enumerate(states) for a in state.cells)
    boundary = [(t,list(a)) for t,state in enumerate(states) for a in state.cells
                if any(a[j] in (0,case['side']-1) for j in range(3))]
    inverse = recorded['experiment']['provenance']['full_rewind_equal'] and all(
        frame['audit']['inverse_equal'] is True for frame in recorded['experiment']['frames'][1:])
    checks = {'first_step_target_exact':first_target,'first_step_C_exact':first_C,
              'initial_Q_exact':q[0]==6*u,'Q_conserved':len(set(q))==1,
              'causal_support_bound':support_ok,'no_boundary_contact':not boundary,
              'full_inverse':inverse}
    if source_rotation is not None: checks['source_quarter_turn'] = source_rotation
    return {'id':case['id'],'case':case,'checks':checks,'all_checks':all(checks.values()),
            'first_step_prediction':{'u':u,'ell':ell,'r_next':r,'C_kind':expected_kind},
            'first_step_world_C':first_events,'world_C':events,
            'world_C_counts':dict(sorted(Counter(e['kind'] for e in events).items())),
            'Q_trace':[str(v) for v in q],'boundary_contacts':boundary,
            'centered_frame_sha256':[digest(centered_state(s)) for s in states]}


def run(output):
    registration = json.loads((output/'registration.json').read_text())
    protocol = json.loads((output/'protocol.json').read_text())
    assert sha(PROTOCOL.read_bytes()) == registration['protocol_sha256']
    assert sha(Path(__file__).read_bytes()) == registration['producer_sha256']
    assert sha((output/'specs.json').read_bytes()) == registration['specs_sha256']
    assert source_hashes() == registration['source_sha256']
    if (output/'run_started.json').exists():raise FileExistsError('A registered run cannot be restarted or overwritten')
    definitions = json.loads((output/'specs.json').read_text())
    write(output/'run_started.json',{'started_utc':datetime.now(timezone.utc).isoformat(),'registration_sha256':sha((output/'registration.json').read_bytes())})
    (output/'records').mkdir()
    start_cpu,start_wall = time.process_time(),time.monotonic()
    rows,selected,errors = [],[],[]
    def budget():
        if time.process_time()-start_cpu > protocol['budget']['max_cpu_seconds']:raise TimeoutError('CPU budget exhausted')
        if time.monotonic()-start_wall > protocol['budget']['max_wall_seconds']:raise TimeoutError('Wall budget exhausted')
        if sum(p.stat().st_size for p in output.rglob('*') if p.is_file()) > protocol['budget']['max_output_bytes']:raise MemoryError('Recorded-output byte budget exhausted')
    try:
        for definition in definitions:
            budget()
            recorded = run_experiment(definition)
            report = assess(definition,recorded)
            record_path = 'records/'+definition['id']+'.json.gz'
            raw = gzip.compress((canonical({'recorded':recorded,'analysis':report})+'\n').encode('ascii'),mtime=0)
            (output/record_path).write_bytes(raw)
            rows.append({k:v for k,v in report.items() if k not in ('world_C',)})
            rows[-1].update({'record':record_path,'record_sha256':sha(raw)})
            if definition['id'] in protocol['presenter_ids']:selected.append(recorded['experiment'])
            budget()
        write(output/'presenter_experiments.json',bundle(selected,title='Parallel inputs and native Rule3 clicks'))
        budget()
        build(output/'presenter_experiments.json',output/'The_Presenter.html')
        budget()
    except Exception as exc:
        errors.append({'type':type(exc).__name__,'message':str(exc)})
    comparisons = []
    for amplitude in protocol['single_donor']['amplitudes']:
        pair = [r for r in rows if r['case']['family']=='single' and r['case']['amplitude']==amplitude]
        comparisons.append({'amplitude':amplitude,'complete':len(pair)==2,
                            'equal':len(pair)==2 and pair[0]['centered_frame_sha256']==pair[1]['centered_frame_sha256']})
    final = {'format':'universe24-parallel-division-result-v1',
             'status':'completed' if len(rows)==90 and not errors else 'inconclusive',
             'registered_cases':90,'completed_cases':len(rows),'cases':rows,
             'not_run':[d['id'] for d in definitions if d['id'] not in {r['id'] for r in rows}],
             'all_case_checks':len(rows)==90 and all(r['all_checks'] for r in rows),
             'cross_size_comparisons':comparisons,'all_cross_size_equal':all(r['equal'] for r in comparisons),
             'source_unchanged':source_hashes()==registration['source_sha256'] and sha(Path(__file__).read_bytes())==registration['producer_sha256'],
             'protocol_sha256':registration['protocol_sha256'],'producer_sha256':registration['producer_sha256'],
             'errors':errors,'cpu_seconds':time.process_time()-start_cpu,'wall_seconds':time.monotonic()-start_wall,
             'claim_limits':protocol['claim_limits']}
    write(output/'result.json',final)
    print(canonical({k:v for k,v in final.items() if k not in ('cases','cross_size_comparisons','claim_limits')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--prepare',action='store_true');action.add_argument('--run',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    (prepare if args.prepare else run)(args.output)
