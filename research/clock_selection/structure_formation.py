"""Frozen initial preparations and passive study of stationary clock formation.

Preflight mode never advances the engine. Execution mode records the native
engine only, with the protocol and exact producer frozen before capture.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import itertools
import json
import shutil
import subprocess
import time
from pathlib import Path
from universe24 import Coupling
from universe24.core.group_2o import DIRECTIONS
from research.components import BoardSpec, Patch, place, finalize, plain
from research.experiments.run import assemble, run_experiment, recorded_states
from research.presenter.export import bundle
from universe24.observation.clicks import clicks

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'structure_formation_protocol_v1.json'
CP = Coupling((1, 1, 1))
ROOT = HERE.parents[1]
CYCLE = ((1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0))
HALO = (2, 4, 2, 0)

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def complete_template(phase):
    nodes = {(0, 0, 0), *DIRECTIONS}
    cells = {(*node, channel): (0, 0, 2) for node in nodes for channel in range(48)}
    a, b, r = CYCLE[phase]
    cells[(0, 0, 0, 0)] = (a, b, r)
    cells[(0, 0, 0, 14)] = (-a, -b, 4-r)
    for direction, delta in enumerate(DIRECTIONS):
        cells[(*delta, CP.ports[direction][0])] = (0, 0, HALO[phase])
        cells[(*delta, CP.ports[direction][14])] = (0, 0, 4-HALO[phase])
    return cells

def geometry(side, distance):
    c = side//2
    first = (c-distance//2, c, c)
    second = add(first, (distance, 0, 0))
    segment = {add(first, (x, 0, 0)) for x in range(distance+1)}
    target = segment | {add(node, delta) for node in segment for delta in DIRECTIONS}
    return first, second, target

def prepared(side, distance, second_sign, mask):
    if distance not in (2, 3, 4) or second_sign not in (-1, 1) or mask not in ('00', '10', '01', '11'):
        raise ValueError('Outside the registered preparation family')
    first, second, target = geometry(side, distance)
    placements = []
    for name, origin, phase, enabled in zip(('A', 'B'), (first, second), (0, 0 if second_sign == 1 else 2), mask):
        cells = complete_template(phase)
        if enabled == '0':
            cells = {address: (0, 0, triple[2]) for address, triple in cells.items()}
        patch = Patch('complete-isolated-clock', cells,
                      ports={'core': ((0,0,0,0), (0,0,0,14))},
                      sources={'clock': ((0,0,0,0), (0,0,0,14))},
                      evidence_domains=('Immutable complete initial clock template; assembly is not a dynamical guarantee.',))
        placements.append(place(patch, name=name, at=origin))
    return finalize(BoardSpec(side), placements)

def matches(state, origin, phase):
    return all(tuple(state.at((*add(origin, address[:3]), address[3]))) == value
               for address, value in complete_template(phase).items())

def preflight():
    protocol = json.loads(PROTOCOL.read_text())
    rows = []
    assert CP.ports[0][0] == CP.ports[1][0] == 0
    assert CP.ports[0][14] == CP.ports[1][14] == 14
    for side, distance, sign in itertools.product(protocol['family']['sides'], protocol['family']['distances'], protocol['family']['second_counter_signs']):
        first, second, target = geometry(side, distance)
        boards = {mask: prepared(side, distance, sign, mask) for mask in protocol['family']['controls']}
        states = {mask: board.initial for mask, board in boards.items()}
        phase_b = 0 if sign == 1 else 2
        assert matches(states['11'], first, 0) and matches(states['11'], second, phase_b)
        assert matches(states['10'], first, 0) and matches(states['01'], second, phase_b)
        addresses = set().union(*(state.cells for state in states.values()))
        assert all(len({state.at(address).r for state in states.values()}) == 1 for address in addresses)
        assert all(states['11'].at(address)[j] == states['10'].at(address)[j] + states['01'].at(address)[j] - states['00'].at(address)[j]
                   for address in addresses for j in (0, 1))
        halos = [{add(origin, node) for node in {(0,0,0), *DIRECTIONS}} for origin in (first, second)]
        shared = halos[0] & halos[1]
        assert len(shared) == (1 if distance == 2 else 0)
        assert len(target) == 5*distance+7
        margin = min(min(v, side-1-v) for address, value in states['11'].cells.items() if value.a or value.b for v in address[:3])
        assert margin > protocol['steps']
        rows.append({'side': side, 'distance': distance, 'second_sign': sign,
                     'both_complete_initial_templates_valid': True, 'matched_remainders': True,
                     'commuting_counter_masks': True, 'shared_halo_nodes': [list(x) for x in sorted(shared)],
                     'target_nodes': len(target), 'target_triples': 48*len(target),
                     'initial_active_boundary_margin': margin,
                     'assembly_hashes': {mask: hashlib.sha256(json.dumps(plain(board.manifest), sort_keys=True).encode()).hexdigest() for mask, board in boards.items()}})
    return {'status': 'passed_initial_assembly_only', 'new_trajectories': 0,
            'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            'preflight_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'prepared_cases': len(rows)*4, 'groups': rows}

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))

def write_json(path, value):
    with Path(path).open('x') as handle:
        handle.write(canonical(value)+'\n')

def experiment_spec(case, protocol):
    first, second, target = geometry(case['side'], case['distance'])
    components = []
    for name, origin, phase, enabled in zip(('A', 'B'), (first, second), (0, 0 if case['second_sign'] == 1 else 2), case['control']):
        cells = complete_template(phase)
        if enabled == '0':
            cells = {address: (0,0,value[2]) for address, value in cells.items()}
        components.append({'name': name, 'recipe': 'Patch', 'at': list(origin),
            'params': {'kind': 'complete-isolated-clock',
                       'cells': [[*address,*value] for address,value in sorted(cells.items())],
                       'ports': {'core': [[0,0,0,0],[0,0,0,14]]},
                       'sources': {'clock': [[0,0,0,0],[0,0,0,14]]}}})
    return {'format': 'universe24-assembly-experiment-v1',
        'id': case['id']+'-'+case['control'],
        'title': 'Initially separated clocks: '+case['id']+'-'+case['control'],
        'description': 'Complete initial clocks under unchanged Rule3; stationary formation is a passive finite criterion, not a physical force.',
        'question': protocol['question'], 'board': {**protocol['board'],'side':case['side']},
        'steps': protocol['steps'], 'seed': None, 'components': components,
        'detectors': [], 'view': {'port':'A.core'}, 'controls': case,
        'provenance': {'initial_only': True, 'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()},
        'budget': {'max_frames':protocol['steps']+1, 'max_cells':protocol['budget']['max_cumulative_native_rows_per_record'],
                   'max_seconds':protocol['budget']['max_seconds_per_record'], 'max_bytes':protocol['budget']['max_recorded_bytes']}}

def external_terms(state, target):
    terms = []
    for address,value in state.cells.items():
        if not value.b or address[:3] in target:
            continue
        for direction in range(6):
            destination = state.cube.adjacent(address,direction,CP.ports[direction][address[3]])
            if destination[:3] in target:
                terms.append({'source':list(address),'target':list(destination),
                              'term':CP.weights[direction][address[3]]*value.b})
    return terms

def observe(case, states, protocol):
    first,second,target = geometry(case['side'],case['distance'])
    endpoint = {first,second}
    bridge = {add(first,(x,0,0)) for x in range(1,case['distance'])}
    halo = target-endpoint-bridge
    region = [(*node,g) for node in sorted(target) for g in range(48)]
    trace = [[list(state.at(address)) for address in region] for state in states]
    start,end = protocol['readouts']['hold_states']
    periods = [period for period in protocol['readouts']['periods']
               if all(trace[t] == trace[t+period] for t in range(start,end-period+1))]
    boundary = [{'update':t+1,'terms':external_terms(state,target)} for t,state in enumerate(states[:-1])]
    bridge_trace = [[[*address,*state.at(address)] for address in sorted(state.cells)
                     if address[:3] in bridge and (state.at(address).a or state.at(address).b)] for state in states]
    phase_b = 0 if case['second_sign'] == 1 else 2
    identity = {name:[{'state':t,'matches':[p for p in range(4) if matches(state,origin,p)]}
                      for t,state in enumerate(states)] for name,origin in (('A',first),('B',second))}
    core_trace = {name:[[[state.at((*origin,g)).a,state.at((*origin,g)).b] for g in range(48)] for state in states]
                  for name,origin in (('A',first),('B',second))}
    exact = {name:all(row['matches'] == [(initial_phase+row['state'])%4] for row in identity[name])
             for name,initial_phase in (('A',0),('B',phase_b))}
    events=[]
    counts={name:{str(k):0 for k in range(3)} for name in ('endpoint','bridge','halo','exterior')}
    for t,(old,new) in enumerate(zip(states,states[1:]),1):
        for event in clicks(old,new,t):
            node=event.address[:3]
            label='endpoint' if node in endpoint else 'bridge' if node in bridge else 'halo' if node in halo else 'exterior'
            terms=[]
            for direction in range(6):
                address=old.cube.adjacent(event.address,direction,CP.ports[direction][event.address[3]])
                terms.append({'source':list(address),'term':CP.weights[direction][event.address[3]]*old.at(address).b})
            events.append({'step':t,'address':list(event.address),'kind':event.kind,'ell':event.quotient,
                           'region':label,'six_terms':terms,'u':sum(term['term'] for term in terms)})
            counts[label][str(event.kind)]+=1
    return {'region_addresses':[list(address) for address in region], 'region_trace':trace,
        'boundary_inputs':boundary, 'hold_periods':periods,
        'hold_individually_isolated':all(not boundary[t]['terms'] for t in range(start,end)),
        'hold_nonzero':any(value[0] or value[1] for frame in trace[start:end+1] for value in frame),
        'bridge_nodes':[list(x) for x in sorted(bridge)], 'bridge_trace':bridge_trace,
        'first_bridge_counter_activity':next((t for t,rows in enumerate(bridge_trace) if rows),None),
        'recurrent_bridge_periods':[period for period in periods if any(bridge_trace[t] for t in range(start,start+period))],
        'complete_initial_identities':{name:identity[name][0]['matches'] for name in identity},
        'identity_traces':identity, 'expected_complete_identity_all_states':exact, 'core_counter_traces':core_trace,
        'first_full_state_return':next((t for t,state in enumerate(states[1:],1) if state==states[0]),None),
        'whole_state_period4_all_states':all(states[t]==states[t+4] for t in range(len(states)-4)),
        'all_C':events, 'C_counts':counts,
        'active_boundary_hit':any(any(v in (0,case['side']-1) for v in address[:3])
                                 for state in states for address,value in state.cells.items() if value.a or value.b),
        'max_sparse_channels':max(len(state.cells) for state in states)}

def assess(rows, protocol):
    by={row['case']['control']:row for row in rows}
    states={mask:recorded_states(row['experiment'])[0] for mask,row in by.items()}
    obs={mask:row['observations'] for mask,row in by.items()}
    addresses=set().union(*(state.cells for state in states.values()))
    same_remainders=all(len({state.at(address).r for state in states.values()})==1 for address in addresses)
    commuting=all(states['11'].at(address)[i]==states['10'].at(address)[i]+states['01'].at(address)[i]-states['00'].at(address)[i]
                  for address in addresses for i in (0,1))
    initial=bool(obs['11']['complete_initial_identities']['A'] and obs['11']['complete_initial_identities']['B'])
    singleton=obs['10']['expected_complete_identity_all_states']['A'] and obs['01']['expected_complete_identity_all_states']['B']
    inactive=all(not any(a or b for frame in obs[mask]['core_counter_traces'][name] for a,b in frame)
                 for mask,name in (('10','B'),('01','A'),('00','A'),('00','B')))
    controls_quiet=all(not any(obs[mask]['bridge_trace']) for mask in ('00','10','01'))
    eligible=initial and same_remainders and commuting and singleton and inactive and controls_quiet
    start,end=protocol['readouts']['hold_states']
    causal={name:any(obs['11']['core_counter_traces'][name][t]!=obs[mask]['core_counter_traces'][name][t] for t in range(start,end+1))
            for name,mask in (('A','10'),('B','01'))}
    joint=obs['11']
    new_bridge=joint['first_bridge_counter_activity'] is not None and joint['first_bridge_counter_activity']>0 and controls_quiet
    recurrence=bool(joint['hold_periods'] and joint['hold_nonzero'])
    formed=bool(eligible and recurrence and joint['hold_individually_isolated'] and new_bridge and joint['recurrent_bridge_periods'] and all(causal.values()))
    geometry_case={key:value for key,value in rows[0]['case'].items() if key!='control'}
    predicted_negative=geometry_case['distance']>=3 or geometry_case['second_sign']==-1
    return {'geometry':geometry_case,'both_initial_complete_identities':initial,'matched_remainders':same_remainders,
        'counter_masks_commute':commuting,'singleton_complete_identities_preserved':singleton,
        'inactive_core_controls_quiet':inactive,'all_control_bridge_traces_quiet':controls_quiet,'eligible':eligible,
        'joint_hold_periods':joint['hold_periods'],'joint_individually_isolated':joint['hold_individually_isolated'],
        'new_bridge':new_bridge,'new_recurrent_bridge':bool(new_bridge and joint['recurrent_bridge_periods']),
        'late_core_causal_difference':causal,'finite_stationary_composite_formed':formed,
        'predicted_negative':predicted_negative,
        'exact_negative_control_agrees':bool(joint['whole_state_period4_all_states'] and not any(joint['bridge_trace'])) if predicted_negative else None,
        'physical_binding_or_force_established':False}

def source_hashes():
    files=[Path(__file__),PROTOCOL]
    for directory in ('universe24','research/components','research/experiments','research/presenter'):
        files.extend((ROOT/directory).rglob('*.py'))
    return {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(files))}

def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'records').mkdir()
    protocol=json.loads(PROTOCOL.read_text());frozen=source_hashes();cpu=time.process_time();wall=time.monotonic()
    shutil.copyfile(PROTOCOL,output/'protocol.json');shutil.copyfile(Path(__file__),output/'executed_structure_formation.py')
    write_json(output/'registration.json',{'source_sha256':frozen,'protocol_sha256':frozen[str(PROTOCOL.relative_to(ROOT))],
        'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'registered_before_capture':True,
        'initial_preflight':preflight()})
    ledger=[];groups=[];examples=[];failure=None
    try:
        for side,distance,sign in itertools.product(protocol['family']['sides'],protocol['family']['distances'],protocol['family']['second_counter_signs']):
            if time.process_time()-cpu>protocol['budget']['max_cpu_seconds']-30 or time.monotonic()-wall>protocol['budget']['max_wall_seconds']-45:
                failure={'type':'budget_stop_before_group','group':[side,distance,sign]};break
            rows=[]
            for mask in protocol['family']['controls']:
                case={'id':f'formation-L{side}-d{distance}-s{sign:+d}','side':side,'distance':distance,'second_sign':sign,'control':mask}
                spec=experiment_spec(case,protocol)
                assert assemble(spec).initial==prepared(side,distance,sign,mask).initial
                captured=run_experiment(spec);states=recorded_states(captured['experiment'])
                if any(len(state.cells)>protocol['budget']['max_sparse_channels_per_state'] for state in states):
                    raise RuntimeError('Registered per-state sparse channel cap exceeded')
                row={'case':case,'spec':spec,'assembly':captured['assembly'],'experiment':captured['experiment'],'observations':observe(case,states,protocol)}
                path=output/'records'/(spec['id']+'.json.gz')
                path.write_bytes(gzip.compress(canonical(row).encode(),mtime=0))
                ledger.append({'id':spec['id'],'record':str(path.relative_to(output)),
                               'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                               'full_rewind_equal':captured['experiment']['provenance']['full_rewind_equal']})
                rows.append(row)
                if side==225 and ((distance==2 and sign==1) or (mask=='11' and ((distance==2 and sign==-1) or (distance==3 and sign==1)))):
                    examples.append(captured['experiment'])
                if sum(path.stat().st_size for path in output.rglob('*') if path.is_file())>protocol['budget']['max_recorded_bytes']-16000000:
                    raise RuntimeError('Recorded evidence budget reached; native records retained')
            groups.append(assess(rows,protocol));print(f'{len(ledger)}/48 {case["id"]}',flush=True)
    except Exception as error:
        failure={'type':type(error).__name__,'message':str(error),'case':locals().get('case')}
        write_json(output/'failure.json',failure)
    assert frozen==source_hashes(),'Frozen sources changed'
    if examples:write_json(output/'experiments.json',bundle(examples,title='The Presenter: initially separated clocks'))
    result={'status':'completed' if len(ledger)==48 and failure is None else 'inconclusive','failure':failure,
        'completed_cases':len(ledger),'cases':ledger,'groups':groups,'new_trajectories':len(ledger),
        'all_full_rewinds':all(row['full_rewind_equal'] for row in ledger),'sources_unchanged':True,
        'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.monotonic()-wall,
        'scope':'Finite stationary formation criterion; no attraction, repulsion, physical matter or chemical binding inferred.'}
    result['budget_passed']=result['cpu_seconds']<=protocol['budget']['max_cpu_seconds'] and result['wall_seconds']<=protocol['budget']['max_wall_seconds'] and sum(path.stat().st_size for path in output.rglob('*') if path.is_file())<=protocol['budget']['max_recorded_bytes']
    write_json(output/'result.json',result)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--preflight-output', type=Path)
    modes.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output:
        run(args.output)
        return
    result = preflight()
    args.preflight_output.parent.mkdir(parents=True, exist_ok=True)
    with args.preflight_output.open('x') as handle:
        json.dump(result, handle, sort_keys=True, indent=2)
        handle.write('\n')
    print(json.dumps({key: result[key] for key in ('status', 'new_trajectories', 'protocol_sha256', 'prepared_cases')}))

if __name__ == '__main__':
    main()
