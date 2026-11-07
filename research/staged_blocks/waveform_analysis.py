"""Read actual Rule3 input words; never generate or alter a trajectory.

python -m research.staged_blocks.waveform_analysis --output NEW_DIRECTORY
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time

from research.experiments.run import recorded_states
from universe24 import Coupling
from universe24.observation.clicks import classify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / 'waveform_protocol.json'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selection(protocol):
    spec = protocol['selection']
    result = [('composition', name, ROOT/spec['composition_directory']/(name+'.json.gz'))
              for name in spec['composition_ids']]
    result.extend(('interaction', name+'-'+control,
                   ROOT/spec['interaction_directory']/(name+'-'+control+'.json.gz'))
                  for name in spec['interaction_geometries'] for control in spec['controls'])
    return result


def lobes(values):
    result = []
    for update, value in enumerate(values, start=1):
        if not value:
            continue
        sign = 1 if value > 0 else -1
        if result and result[-1]['sign'] == sign and result[-1]['last_update'] == update-1:
            result[-1]['last_update'] = update
            result[-1]['sum_u'] += value
        else:
            result.append({'first_update': update, 'last_update': update, 'sign': sign, 'sum_u': value})
    return result


def node_trace(states, coupling, position):
    snapshots = [[list(state.at((*position, g))) for g in range(48)] for state in states]
    transitions, cumulative_u, cumulative_ell = [], [0]*48, [0]*48
    for old_time, (old, new) in enumerate(zip(states, states[1:])):
        rows = []
        for g in range(48):
            address = (*position, g)
            before, after = old.at(address), new.at(address)
            terms = []
            for direction in range(6):
                sender = old.cube.adjacent(address, direction, coupling.ports[direction][g])
                weight = coupling.weights[direction][g]
                terms.append({'direction': direction, 'sender': list(sender), 'weight': weight,
                              'b': old.at(sender).b, 'term': weight*old.at(sender).b})
            u = sum(row['term'] for row in terms)
            ell = after.b + before.a
            assert after.a == before.b
            assert divmod(2*u+before.r, 6) == (ell, after.r), (position,g,old_time)
            cumulative_u[g] += u
            cumulative_ell[g] += ell
            assert after.r-snapshots[0][g][2] == 2*cumulative_u[g]-6*cumulative_ell[g]
            assert after.a**2+after.b**2-before.a**2-before.b**2 == ell**2-2*before.a*ell
            event = classify(before, after)
            rows.append({'channel': g, 'u': u, 'ell': ell, 'terms': terms,
                         'cumulative_u': cumulative_u[g], 'cumulative_ell': cumulative_ell[g],
                         'C': None if event is None else {'kind': event[0], 'ell': event[1]},
                         'r_change': after.r-before.r,
                         'counter_change': before[:2] != after[:2],
                         'returns_to_initial_triple': list(after) == snapshots[0][g]})
        transitions.append({'old_state': old_time, 'new_state': old_time+1, 'channels': rows})
    summaries = []
    for g in range(48):
        word = [step['channels'][g]['u'] for step in transitions]
        active = [i+1 for i, u in enumerate(word) if u]
        first = active[0] if active else None
        zero_returns = [i+1 for i, step in enumerate(transitions)
                        if first is not None and i+1 > first and step['channels'][g]['cumulative_u'] == 0]
        events = [{'update': i+1, **step['channels'][g]['C']} for i, step in enumerate(transitions)
                  if step['channels'][g]['C'] is not None]
        summaries.append({'channel': g, 'first_nonzero_input_update': first,
                          'last_nonzero_input_update': active[-1] if active else None,
                          'input_word': word, 'lobes': lobes(word), 'sum_u': sum(word),
                          'sum_ell': sum(step['channels'][g]['ell'] for step in transitions),
                          'first_zero_area_return_state': zero_returns[0] if zero_returns else None,
                          'events': events,
                          'initial': snapshots[0][g], 'final': snapshots[-1][g]})
    return {'position': list(position), 'states': snapshots, 'transitions': transitions,
            'channels': summaries, 'all_local_identities_exact': True}


def quiet_pair(trace, sign):
    states, steps = trace['states'], trace['transitions']
    ready = [[0,0,2] for _ in range(48)]
    ready[0][2], ready[14][2] = (2,4) if sign == 1 else (4,2)
    if states[0] != ready:
        return {'sign': sign, 'status': 'not_applicable_initial_state', 'ready_required': ready}
    words = [[row['u'] for row in step['channels']] for step in steps]
    first = next((i for i, row in enumerate(words) if any(row)), None)
    if first is None:
        return {'sign': sign, 'status': 'no_write_observed'}
    desired = [0]*48
    desired[0], desired[14] = sign, -sign
    pending = [row[:] for row in ready]
    pending[0][2], pending[14][2] = ready[14][2], ready[0][2]
    result = {'sign': sign, 'write_update': first+1, 'write_input_matches': words[first] == desired,
              'write_state_matches': states[first+1] == pending,
              'first_input': words[first]}
    if not result['write_input_matches'] or not result['write_state_matches']:
        return {**result, 'status': 'first_write_contract_failed'}
    stop = first+1+8
    if stop >= len(states):
        return {**result, 'status': 'insufficient_wait_horizon'}
    bad = next((i for i in range(first+1,stop) if any(words[i]) or states[i+1] != pending), None)
    result['pending_states_required'] = [first+1,stop]
    if bad is not None:
        return {**result, 'status': 'waiting_contract_failed', 'first_failure_update': bad+1,
                'failure_input': words[bad], 'failure_state': states[bad+1],
                'failure_C': [row for row in steps[bad]['channels'] if row['C'] is not None]}
    read = next((i for i in range(stop,len(words)) if any(words[i])), None)
    if read is None:
        return {**result, 'status': 'quiet_write_wait_observed_no_read_in_record'}
    target = [[0,0,2] for _ in range(48)]
    target[0][2] = target[14][2] = 0
    winner = 0 if sign == 1 else 14
    target[winner][1] = 1
    result.update({'read_update': read+1, 'read_input': words[read], 'winner_channel': winner})
    if words[read] != desired or states[read+1] != target:
        return {**result, 'status': 'read_contract_failed'}
    if read+1+8 >= len(states):
        return {**result, 'status': 'read_observed_insufficient_retention_horizon'}
    if any(any(row) for row in words[read+1:read+9]):
        return {**result, 'status': 'read_retention_input_failed'}
    return {**result, 'status': 'conditional_word_present_in_record', 'scope': 'Observed actual input word only; not independent message generation or unique approval'}


def quiet_single(trace, g, sign):
    states, word = trace['states'], trace['channels'][g]['input_word']
    if states[0][g] != [0,0,2]:
        return {'channel': g, 'sign': sign, 'status': 'not_applicable_initial_state'}
    first = next((i for i,u in enumerate(word) if u), None)
    if first is None:
        return {'channel': g, 'sign': sign, 'status': 'no_write_observed'}
    target = [0,0,2+2*sign]
    result = {'channel': g, 'sign': sign, 'write_update': first+1}
    if word[first] != sign or states[first+1][g] != target:
        return {**result,'status':'first_write_contract_failed'}
    stop = first+9
    if stop >= len(states):
        return {**result,'status':'insufficient_wait_horizon'}
    bad = next((i for i in range(first+1,stop) if word[i] or states[i+1][g] != target), None)
    if bad is not None:
        return {**result,'status':'waiting_contract_failed','first_failure_update':bad+1,
                'failure_u':word[bad],'failure_state':states[bad+1][g]}
    read = next((i for i in range(stop,len(word)) if word[i]),None)
    if read is None:
        return {**result,'status':'quiet_write_wait_observed_no_read_in_record'}
    expected = [0,sign,0 if sign == 1 else 4]
    return {**result,'read_update':read+1,'read_u':word[read],
            'status':'conditional_read_observed' if word[read] == sign and states[read+1][g] == expected else 'read_contract_failed'}


def phase_diagnostic(joint, reference, g):
    values = []
    for t,(row,ref) in enumerate(zip(joint['states'],reference['states'])):
        a,b,r = row[g]
        c,d,rr = ref[g]
        rotations = ((c,d),(d,-c),(-c,-d),(-d,c))
        phase = next((k for k,pair in enumerate(rotations) if pair == (a,b)),None) if c*c+d*d else None
        values.append({'state':t,'phase_relative_to01':phase,'I':a*a+b*b,'r':r,'reference_r':rr,
                       'D':a*c+b*d,'X':a*d-b*c})
    intervals = []
    start = 0
    def key(row):
        return tuple(row[k] for k in ('phase_relative_to01','I','r','reference_r','D','X'))
    for end in range(1,len(values)+1):
        same = end < len(values) and key(values[end]) == key(values[start])
        if end < len(values):
            transition = joint['transitions'][end-1]['channels'][g]
            same = same and transition['u'] == 0 and transition['C'] is None
        if not same:
            if end-1-start >= 8 and values[start]['phase_relative_to01'] in (1,2,3):
                intervals.append({'start_state':start,'end_state':end-1,'quiet_updates':end-1-start,
                                  'record':values[start],'right_censored':end==len(values)})
            start = end
    return {'scope':'Post-hoc center-phase diagnostic against separately recorded matched01 control; not an internal phase-comparator implementation',
            'values':values,'nontrivial_eight_update_quiet_intervals':intervals,
            'all_center_C':joint['channels'][g]['events'], 'all_center_input_lobes':joint['channels'][g]['lobes']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    started = time.process_time()
    protocol_bytes = PROTOCOL.read_bytes()
    protocol = json.loads(protocol_bytes)
    planned = selection(protocol)
    assert len(planned) == protocol['budget']['max_records']
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'records').mkdir()
    (args.output/'protocol.json').write_bytes(protocol_bytes)
    registration = {'protocol_sha256':hashlib.sha256(protocol_bytes).hexdigest(),
                    'observer_source_sha256':file_hash(Path(__file__)),
                    'sources':[{'kind':kind,'id':name,'path':str(path.relative_to(ROOT)),
                                'sha256':file_hash(path) if path.exists() else None}
                               for kind,name,path in planned]}
    (args.output/'registration.json').write_text(canonical(registration)+'\n')
    analyses, missing, summaries = {}, [], []
    for kind,name,path in planned:
        if time.process_time()-started > protocol['budget']['max_cpu_seconds']:
            raise RuntimeError('Registered waveform-analysis CPU budget exceeded')
        if not path.exists():
            missing.append(name)
            continue
        record = json.loads(gzip.decompress(path.read_bytes()))
        states = recorded_states(record['experiment'])
        tensor = record['assembly']['tensor']
        coupling = Coupling(tuple(tensor['body_signs']))
        assert coupling.fingerprint == tensor['fingerprint']
        ports = record['assembly']['ports']
        if kind == 'composition':
            center = ports['clock.center'][0]
            probes = {'receiver':ports['memory.node'][0][:3], 'clock':center[:3]}
        else:
            center = ports['apparatus.clock'][0]
            probes = {'clock':center[:3], 'guide_contact':[center[0],center[1]-1,center[2]]}
        data = {'id':name,'source_record':str(path.relative_to(ROOT)), 'source_sha256':file_hash(path),
                'source_experiment_status_unchanged':True,'clock_channel':center[3], 'probes':{}}
        for label,position in probes.items():
            trace = node_trace(states,coupling,tuple(position))
            trace['quiet_pair_contracts'] = [quiet_pair(trace,sign) for sign in (1,-1)]
            trace['quiet_single_contracts'] = [quiet_single(trace,g,sign) for g in range(48) for sign in (1,-1)]
            data['probes'][label] = trace
        analyses[name] = data
        summaries.append({'id':name,'clock_channel':center[3],
                          'clock_initial':data['probes']['clock']['channels'][center[3]]['initial'],
                          'clock_final':data['probes']['clock']['channels'][center[3]]['final'],
                          'clock_C':data['probes']['clock']['channels'][center[3]]['events'],
                          'clock_lobes':data['probes']['clock']['channels'][center[3]]['lobes'],
                          'probe_pair_statuses':{label:[row['status'] for row in trace['quiet_pair_contracts']]
                                                 for label,trace in data['probes'].items()}})
    phase_reports = {}
    for geometry in protocol['selection']['interaction_geometries']:
        if geometry+'-11' in analyses and geometry+'-01' in analyses:
            joint,ref = analyses[geometry+'-11'],analyses[geometry+'-01']
            phase_reports[geometry] = phase_diagnostic(joint['probes']['clock'],ref['probes']['clock'],joint['clock_channel'])
    for name,data in analyses.items():
        (args.output/'records'/(name+'.json.gz')).write_bytes(gzip.compress(canonical(data).encode(),mtime=0))
    assert PROTOCOL.read_bytes() == protocol_bytes
    assert file_hash(Path(__file__)) == registration['observer_source_sha256']
    for row in registration['sources']:
        if row['sha256'] is not None:
            assert file_hash(ROOT/row['path']) == row['sha256']
    result = {'format':'universe24-waveform-analysis-result-v1','status':'completed',
              'protocol_sha256':registration['protocol_sha256'],'records_analyzed':len(analyses),
              'missing_selected_records':missing,'all_selected_scalar_identities_exact':True,
              'summaries':summaries,'phase_diagnostics':phase_reports,
              'new_trajectories_generated':0,'original_acceptance_criteria_changed':False,
              'new_component_validated':False,'cpu_seconds':time.process_time()-started}
    (args.output/'result.json').write_text(canonical(result)+'\n')
    if result['cpu_seconds'] > protocol['budget']['max_cpu_seconds']:
        raise RuntimeError('Registered waveform-analysis CPU budget exceeded')
    if sum(p.stat().st_size for p in args.output.rglob('*') if p.is_file()) > protocol['budget']['max_output_bytes']:
        raise RuntimeError('Registered waveform-analysis output budget exceeded')
    print(canonical({key:value for key,value in result.items() if key not in ('summaries','phase_diagnostics')}))


if __name__ == '__main__':
    main()
