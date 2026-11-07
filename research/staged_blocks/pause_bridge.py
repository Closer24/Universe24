"""Prospective two-lane Rule3 pause bridge; all preparation is initial data."""
from __future__ import annotations

import argparse
from collections import defaultdict
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from universe24 import Channel, Coupling, State
from universe24.core.group_2o import DIRECTIONS
from . import interactions as base
from .pulse_words import profile, train_cumulative

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / 'pause_bridge_protocol.json'
CYCLE = ((0, 1), (1, 0), (0, -1), (-1, 0))
LANES = (('lower', 0, 14, 0, (0, 4, 8)), ('upper', 6, 36, 2, (2, 6)))


def geometries(protocol):
    for side, delay in itertools.product(protocol['family']['board_sides'],
                                         protocol['family']['common_delays']):
        yield {'id': f'bridge-L{side}-d{delay}', 'side': side, 'delay': delay,
               'phase': (2-delay) % 4, 'stage': 'encounter', 'guide_target_channel': 0}


def observer_protocol(case):
    protocol = json.loads(base.PROTOCOL.read_text())
    c = case['side']//2
    protocol['board']['side'] = case['side']
    protocol['steps'] = 8 if case['stage'] == 'pristine' else 40
    protocol['geometry'] = {'row_y': c, 'row_z': c, 'packet_x': c-24-case['delay'],
                            'clock_x': c, 'clock_y': c+1, 'clock_z': c,
                            'forward_outlet_x': c+8, 'backward_outlet_x': c-8}
    protocol['readouts']['eligible_hold_starts'] = []
    return protocol


def initial_cells(case):
    """Solve the registered joint remainder constraints; never add States."""
    side, delay, mask = case['side'], case['delay'], case['control']
    c, coupling = side//2, Coupling((1, 1, 1))
    x0 = c-24-delay
    cells, debts, contributors, sources = {}, defaultdict(int), defaultdict(list), {}
    pristine = case['stage'] == 'pristine'
    for lane_index, (name, primary, companion, yoffset, starts) in enumerate(LANES):
        cumulative = train_cumulative(starts) if not pristine or mask[lane_index] == '1' else ()
        row, _ = profile(cumulative)
        sources[name] = []
        for x in range(side):
            a, b, r = row(x-x0)
            for g, sign, remainder in ((primary, 1, r), (companion, -1, 4-r)):
                address = (x, c+yoffset, c, g)
                if address in cells:
                    raise ValueError('Unexpected overlap between guide row assignments')
                if a or b:
                    sources[name].append(address)
                present = mask[lane_index] == '1'
                cells[address] = (sign*a if present else 0, sign*b if present else 0, remainder)
                i = x-x0-1
                cumulative_value = cumulative[i] if 0 <= i < len(cumulative) else 0
                if not cumulative_value:
                    continue
                for d in range(2, 6):
                    xyz = tuple(address[j]+DIRECTIONS[d][j] for j in range(3))
                    recipient = (*xyz, coupling.ports[d][g])
                    contribution = sign*coupling.weights[d][g]*cumulative_value
                    debts[recipient] += contribution
                    contributors[recipient].append({'lane': name, 'source': list(address),
                                                     'direction': d, 'contribution': contribution})
    shared = []
    for address, debt in sorted(debts.items()):
        if address in cells:
            raise ValueError('Transverse train halo overlaps a guide row')
        r = 2-2*debt
        if not 0 <= r < 6:
            raise ValueError(f'Incompatible joint train remainder at {address}: {r}')
        cells[address] = (0, 0, r)
        if len(contributors[address]) > 1:
            shared.append({'address': list(address), 'contributions': contributors[address], 'remainder': r})
    center = (c, c+1, c)
    replacements = []
    if not pristine:
        h, phase = 2, case['phase']
        clock_address = (*center, h)
        if clock_address in cells:
            raise ValueError('Clock overlaps the initially prepared train support')
        cells[clock_address] = (*CYCLE[phase], 0)
        sources['clock'] = [clock_address]
        for d, direction in enumerate(DIRECTIONS):
            xyz = tuple(center[j]+direction[j] for j in range(3))
            address = (*xyz, coupling.ports[d][h])
            r0 = 0 if d in (2, 3) else 2
            expected = (0, 0, r0)
            old = cells.get(address, (0, 0, 2))
            if old != expected:
                raise ValueError(f'Clock halo conflict at {address}: {old} != {expected}')
            value = (0, 0, r0+(2 if phase in (1, 2) else 0))
            cells[address] = value
            replacements.append({'address': list(address), 'before': list(old), 'after': list(value)})
    sources = {name: addresses for name, addresses in sources.items() if addresses}
    nodes = (center, *(tuple(center[j]+d[j] for j in range(3)) for d in DIRECTIONS))
    ports = {'clock': [(*center, 2)], 'center': [(*center, g) for g in range(48)],
             'region': [(*xyz, g) for xyz in nodes for g in range(48)],
             'lower_incoming': [(c, c, c, 0)], 'upper_incoming': [(c, c+2, c, 6)]}
    metadata = {'origin_x': x0, 'center': list(center), 'shared_halo_assignments': shared,
                'clock_joint_replacements': replacements,
                'halo_contribution_sha256': base.digest({str(a): rows for a, rows in sorted(contributors.items())}),
                'sources': {k: [list(a) for a in v] for k, v in sources.items()}}
    return cells, ports, sources, metadata


def case_spec(case, protocol=None):
    protocol = json.loads(PROTOCOL.read_text()) if protocol is None else protocol
    cells, ports, sources, metadata = initial_cells(case)
    identity = case['id']+'-'+case['control']
    steps = 8 if case['stage'] == 'pristine' else protocol['steps']
    return {'format': 'universe24-assembly-experiment-v1', 'id': identity,
            'title': 'Two-lane pause bridge: '+identity,
            'description': ('Two initially prepared packet trains and their explicit shared halo. '
                            'A driven center pause is distinguished from autonomous region memory; '
                            'all C events and full states are retained.'),
            'question': protocol['question'],
            'board': {'side': case['side'], 'background': [0, 0, 2], 'body_signs': [1, 1, 1]},
            'steps': steps, 'components': [{'name': 'apparatus', 'recipe': 'Patch', 'at': [0, 0, 0],
                'params': {'kind': 'joint-two-lane-clock-preparation',
                           'cells': [[*a, *v] for a, v in sorted(cells.items())],
                           'ports': ports, 'sources': sources}}],
            'detectors': [], 'view': {'port': 'apparatus.clock'}, 'controls': case, 'seed': None,
            'provenance': {'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                           'initial_only': True, 'joint_preparation': metadata},
            'budget': {'max_frames': steps+1, 'max_cells': 500000, 'max_bytes': 67108864,
                       'max_seconds': 90}}


def translated(state, displacement):
    return State(state.cube, state.background,
                 {((a[0]+displacement) % state.cube.side, *a[1:]): v for a, v in state.cells.items()})


def observe(case, prepared, states):
    observations = base.observe(observer_protocol(case), case, prepared, states)
    for t, row in enumerate(observations['center_inputs']):
        row['ell'] = observations['center_trace'][t+1][1]+observations['center_trace'][t][0]
    return observations


def assess_case(case, states, observations, protocol):
    if case['stage'] == 'pristine':
        wrong = next((t for t, state in enumerate(states) if state != translated(states[0], t)), None)
        return {'complete_translation': wrong is None, 'first_translation_mismatch': wrong,
                'active_boundary_hits': len(observations['active_boundary_hits'])}
    T = 14+case['delay']
    center = observations['center_trace']
    region = observations['region_trace']
    words = observations['center_inputs'][T-1:T+10]
    checks = []
    def check(name, actual, expected):
        checks.append({'condition': name, 'passed': actual == expected,
                       'actual': actual, 'expected': expected})
    check('registered_prestate', center[T-1], [-1, 0, 0])
    check('net_word', [row['u'] for row in words], protocol['timing']['target_word'])
    check('lower_word', [row['terms'][3]['term'] for row in words], protocol['timing']['lower_terms'])
    check('upper_word', [row['terms'][2]['term'] for row in words], protocol['timing']['upper_terms'])
    check('other_four_input_terms_zero',
          all(row['terms'][d]['term'] == 0 for row in words for d in (0, 1, 4, 5)), True)
    check('clock_pause_states', center[T:T+10], [[0, 0, 4]]*10)
    full_node = [frame[:48] for frame in region[T:T+10]]
    check('complete_center_node_unchanged', all(frame == full_node[0] for frame in full_node), True)
    check('complete_center_node_zero_counters', all(v[:2] == [0, 0] for frame in full_node for v in frame), True)
    check('clock_restart', center[T+10], [0, 1, 0])
    events = [{k: row[k] for k in ('step', 'kind', 'ell')} for row in observations['center_C']
              if T <= row['step'] <= T+10]
    expected_events = [{'step': T, 'kind': 2, 'ell': -1}, {'step': T+10, 'kind': 1, 'ell': 1}]
    check('registered_clock_C', events, expected_events)
    check('endpoint_quotients', [words[0]['ell'], words[-1]['ell']], [-1, 1])
    holds = []
    for start in (T, T+1):
        frames = region[start:start+9]
        holds.append({'start': start, 'through': start+8,
                      'all_336_counters_zero': all(v[:2] == [0, 0] for frame in frames for v in frame),
                      'all_336_triples_unchanged': all(frame == frames[0] for frame in frames),
                      'target_remainder4': center[start][2] == 4,
                      'every_external_term_zero': all(not observations['boundary_inputs'][t]['nonzero_external_terms']
                                                       for t in range(start, start+8))})
    strict = any(all(v for k, v in row.items() if k not in ('start', 'through')) for row in holds)
    cancellation = [{'update': row['update'], 'terms': [v['term'] for v in row['terms']]} for row in words
                    if row['u'] == 0 and any(v['term'] for v in row['terms'])]
    return {'first_update': T, 'last_update': T+10, 'outcome_A_autonomous': strict,
            'autonomous_windows': holds, 'outcome_B_word_pause_restart': all(row['passed'] for row in checks),
            'checks': checks, 'first_mismatch': next((row for row in checks if not row['passed']), None),
            'canceling_input_updates': cancellation, 'center_C_count_full_horizon': len(observations['center_C']),
            'all_C_count': len(observations['all_C']),
            'active_boundary_hits': len(observations['active_boundary_hits'])}


def assess_group(rows):
    by = {row['case']['control']: row for row in rows}
    addresses = set().union(*(row['states'][0].cells for row in rows))
    matched = all(len({row['states'][0].at(a).r for row in rows}) == 1 for a in addresses)
    controls = all(not by[mask]['assessment']['outcome_B_word_pause_restart'] for mask in ('00', '10', '01'))
    joint = by['11']['assessment']
    null = by['00']['states']
    return {'geometry': {k: v for k, v in rows[0]['case'].items() if k != 'control'},
            'matched_initial_remainders': matched,
            'null_clock_complete_period4': all(null[t] == null[t+4] for t in range(len(null)-4)),
            'outcome_A_autonomous': joint['outcome_A_autonomous'],
            'outcome_B_driven_pause': matched and controls and joint['outcome_B_word_pause_restart'],
            'all_controls_fail_complete_bridge': controls,
            'case_verdicts': {mask: row['assessment'] for mask, row in by.items()},
            'final_state_hashes': {mask: state_sha256(row['states'][-1]) for mask, row in by.items()},
            'scope': 'Prearranged two-train driven waiting; not an independent approval computation.'}


def selected(case):
    return case['stage'] == 'encounter' and (case['side'], case['delay']) in ((129, 0), (161, 3))


def run(output):
    output = Path(output)
    raw_protocol = PROTOCOL.read_bytes()
    protocol = json.loads(raw_protocol)
    output.mkdir(parents=True, exist_ok=False)
    (output/'records').mkdir()
    (output/'protocol.json').write_bytes(raw_protocol)
    paths = [Path(__file__), PROTOCOL, HERE/'pulse_words.py', Path(base.__file__), base.PROTOCOL,
             *sorted((ROOT/'universe24').rglob('*.py')), *sorted((ROOT/'research/components').glob('*.py')),
             ROOT/'research/experiments/run.py', ROOT/'research/presenter/export.py']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    geometry = list(geometries(protocol))
    batches = [[{'id': f'bridge-pristine-L{side}-{label}', 'side': side, 'delay': 0, 'phase': 0,
                 'stage': 'pristine', 'guide_target_channel': 0, 'control': mask}]
               for side in protocol['family']['board_sides']
               for label, mask in (('lower', '10'), ('upper', '01'), ('combined', '11'))]
    batches += [[{**case, 'control': mask} for mask in protocol['family']['controls']] for case in geometry]
    registration = {'format': 'universe24-pause-bridge-registration-v1',
                    'protocol_sha256': hashlib.sha256(raw_protocol).hexdigest(), 'source_sha256': hashes,
                    'registered_cases': sum(map(len, batches)), 'cases': [c for batch in batches for c in batch],
                    'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                    'registered_before_capture': True, 'seed': None}
    base.write_json(output/'registration.json', registration)
    started_cpu, started_wall = time.process_time(), time.monotonic()
    ledger, groups, examples = [], [], []
    reason = None
    used_bytes = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    for batch in batches:
        if time.process_time()-started_cpu >= protocol['budget']['max_cpu_seconds']:
            reason = 'cpu_budget'
            break
        rows = []
        for case in batch:
            spec = case_spec(case, protocol)
            prepared = assemble(spec)
            recorded = run_experiment(spec)
            states = recorded_states(recorded['experiment'])
            observations = observe(case, prepared, states)
            rows.append({'case': case, 'spec': spec, 'assembly': recorded['assembly'],
                         'experiment': recorded['experiment'], 'states': states, 'observations': observations,
                         'assessment': assess_case(case, states, observations, protocol)})
        group = assess_group(rows) if len(rows) == 4 else None
        blobs = []
        for row in rows:
            wrapper = {'format': 'universe24-pause-bridge-record-v1', 'spec': row['spec'],
                       'assembly': row['assembly'], 'experiment': row['experiment'],
                       'observations': row['observations'], 'assessment': row['assessment'], 'group_assessment': group}
            raw = base.canonical(wrapper).encode()
            blobs.append((row, raw, gzip.compress(raw, mtime=0)))
        if used_bytes+sum(len(blob) for _, _, blob in blobs) > protocol['budget']['max_recorded_bytes']-6000000:
            reason = 'data_budget'
            break
        for row, raw, compressed in blobs:
            record = 'records/'+row['spec']['id']+'.json.gz'
            (output/record).write_bytes(compressed)
            used_bytes += len(compressed)
            ledger.append({'id': row['spec']['id'], 'case': row['case'], 'record': record,
                           'record_sha256': hashlib.sha256(raw).hexdigest(),
                           'record_gzip_sha256': hashlib.sha256(compressed).hexdigest(),
                           'initial_state_sha256': state_sha256(row['states'][0]),
                           'final_state_sha256': state_sha256(row['states'][-1]),
                           'frames': len(row['states']), 'transitions': len(row['states'])-1,
                           'full_state_inverse': row['experiment']['provenance']['full_rewind_equal'],
                           'assessment': row['assessment']})
            if selected(row['case']):
                examples.append(row['experiment'])
        if group is not None:
            groups.append(group)
        print(f"{len(ledger)}/38 {batch[0]['id']} "
              f"A={group['outcome_A_autonomous'] if group else '-'} "
              f"B={group['outcome_B_driven_pause'] if group else '-'}", flush=True)
    if any(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() != sha for p, sha in hashes.items()):
        raise RuntimeError('Execution source changed during bridge study')
    result = {'format': 'universe24-pause-bridge-result-v1', 'status': 'completed' if reason is None else 'budget_stopped',
              'stop_reason': reason, 'protocol_sha256': registration['protocol_sha256'],
              'registered_cases': 38, 'completed_cases': len(ledger), 'cases': ledger, 'groups': groups,
              'not_run_cases': registration['cases'][len(ledger):],
              'pristine_translation_passes': sum(c['assessment'].get('complete_translation', False) for c in ledger),
              'outcome_A_autonomous_groups': sum(g['outcome_A_autonomous'] for g in groups),
              'outcome_B_driven_pause_groups': sum(g['outcome_B_driven_pause'] for g in groups),
              'all_full_state_inverses': all(c['full_state_inverse'] for c in ledger),
              'all_no_active_boundary_contact': all(c['assessment']['active_boundary_hits'] == 0 for c in ledger),
              'total_states': sum(c['frames'] for c in ledger), 'total_transitions': sum(c['transitions'] for c in ledger),
              'displayed_experiments': len(examples), 'cpu_seconds': time.process_time()-started_cpu,
              'wall_seconds': time.monotonic()-started_wall, 'scope': protocol['interpretation']}
    base.write_json(output/'result.json', result)
    (output/'experiments.json').write_text(base.canonical(bundle(examples, title='The Presenter: two-lane driven pause'))+'\n')
    if sum(p.stat().st_size for p in output.rglob('*') if p.is_file()) > protocol['budget']['max_recorded_bytes']:
        raise RuntimeError('Bridge evidence exceeds its recorded data budget')
    print(base.canonical({k: result[k] for k in ('completed_cases', 'pristine_translation_passes',
                                               'outcome_A_autonomous_groups', 'outcome_B_driven_pause_groups',
                                               'cpu_seconds')}), flush=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    return run(parser.parse_args(argv).output)


if __name__ == '__main__':
    main()
