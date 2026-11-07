"""Prospective same-board phase-memory validation; no runtime intervention."""
from __future__ import annotations

import argparse
from copy import deepcopy
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from universe24 import Channel
from universe24.core.group_2o import DIRECTIONS
from . import interactions as base

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE/'phase_protocol.json'
ALPHABET = ((1, 0), (0, 1), (-1, 0), (0, -1))
COUNTER_CYCLE = ((0, 1), (1, 0), (0, -1), (-1, 0))


def geometries(protocol):
    family = protocol['family']
    for side, r, phase, delay in itertools.product(family['board_sides'], family['clock_remainders'],
                                                 family['clock_phases'], family['packet_delays']):
        yield {'id': f'phase-L{side}-r{r}-p{phase}-d{delay}', 'side': side,
               'clock_remainder': r, 'phase': phase, 'delay': delay,
               'stage': 'phase', 'guide_target_channel': 0, 'compensation_direction': None}


def base_protocol(case):
    protocol = json.loads(base.PROTOCOL.read_text())
    c = case['side']//2
    protocol['board']['side'] = case['side']
    protocol['geometry'] = {'row_y': c, 'row_z': c, 'packet_x': c-16-case['delay'],
                            'clock_x': c, 'clock_y': c+1, 'clock_z': c,
                            'forward_outlet_x': c+8, 'backward_outlet_x': c-8}
    return protocol


def case_spec(case, protocol=None):
    protocol = json.loads(PROTOCOL.read_text()) if protocol is None else protocol
    spec = base.case_spec(case, base_protocol(case))
    c = case['side']//2
    reference = (c, c+24, c+24)
    nodes = ((0, 0, 0), *DIRECTIONS)
    cells = {(*xyz, g): (0, 0, 2) for xyz in nodes for g in range(48)}
    cells[(0, 0, 0, 0)] = (0, 1, 2)
    spec['components'].append({'name': 'reference', 'recipe': 'Patch', 'at': list(reference),
                              'params': {'kind': 'reference-orbit',
                                         'cells': [[*a, *v] for a, v in sorted(cells.items())],
                                         'ports': {'center': [(0, 0, 0, 0)], 'region': list(cells)},
                                         'sources': {'reference': [(0, 0, 0, 0)]}}})
    spec['title'] = 'Same-board phase memory: ' + spec['id']
    spec['question'] = protocol['question']
    spec['description'] = ('Prospective synchronization test with an untouched Rule3 reference clock. '
                           'D/X is a passive relative-phase observer, not an implemented comparator or release gate.')
    spec['provenance'] = {'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                          'initial_only': True, 'discovery_source': 'interactions/main'}
    return spec


def distance(a, b, side):
    return sum(min(abs(a[j]-b[j]), side-abs(a[j]-b[j])) for j in range(3))


def reference_readout(states, coupling, center):
    nodes = (center, *(tuple(center[j]+d[j] for j in range(3)) for d in DIRECTIONS))
    node_set = set(nodes)
    addresses = [(*xyz, g) for xyz in nodes for g in range(48)]
    region_trace = [[list(s.at(a)) for a in addresses] for s in states]
    center_trace = [list(s.at((*center, 0))) for s in states]
    expected = []
    for t in range(len(states)):
        cells = {(*center, 0): Channel(*COUNTER_CYCLE[t % 4], 2)}
        for d, xyz in enumerate(nodes[1:]):
            cells[(*xyz, coupling.ports[d][0])] = Channel(0, 0, 4 if t % 4 in (1, 2) else 2)
        expected.append([list(cells.get(a, Channel(0, 0, 2))) for a in addresses])
    inputs, boundary = [], []
    for t, (old, new) in enumerate(zip(states, states[1:]), 1):
        terms = []
        for d in range(6):
            sender = old.cube.adjacent((*center, 0), d, coupling.ports[d][0])
            terms.append({'source': list(sender), 'term': coupling.weights[d][0]*old.at(sender).b})
        inputs.append({'update': t, 'terms': terms, 'u': sum(term['term'] for term in terms),
                       'ell': new.at((*center, 0)).b+old.at((*center, 0)).a})
        external = []
        for address, value in old.cells.items():
            if not value.b or address[:3] in node_set:
                continue
            for d in range(6):
                target = old.cube.adjacent(address, d, coupling.ports[d][address[3]])
                if target[:3] in node_set:
                    external.append({'source': list(address), 'target': list(target),
                                     'term': coupling.weights[d][address[3]]*value.b})
        boundary.append({'update': t, 'nonzero_external_terms': external})
    return {'center': list(center), 'region_nodes': [list(n) for n in nodes],
            'region_addresses': [list(a) for a in addresses], 'region_trace': region_trace,
            'center_trace': center_trace, 'inputs': inputs, 'boundary_inputs': boundary,
            'complete_region_matches_isolated_formula': region_trace == expected,
            'all_external_terms_zero': all(not row['nonzero_external_terms'] for row in boundary)}


def observe(case, prepared, states):
    target = base.observe(base_protocol(case), case, prepared, states)
    c = case['side']//2
    center = (c, c+24, c+24)
    reference = reference_readout(states, prepared.engine.coupling, center)
    active = [a for a, v in states[0].cells.items() if v.a or v.b]
    non_reference = [a for a in active if a[:3] != center]
    ref_nodes = reference['region_nodes']
    target_nodes = target['region_nodes']
    to_reference = min((distance(a, n, case['side']) for a in non_reference for n in ref_nodes), default=None)
    to_target = min(distance(center, n, case['side']) for n in target_nodes)
    phase_trace = []
    for t, (v, z) in enumerate(zip(target['center_trace'], reference['center_trace'])):
        D = v[0]*z[0]+v[1]*z[1]
        X = v[0]*z[1]-v[1]*z[0]
        I, I_ref = v[0]*v[0]+v[1]*v[1], z[0]*z[0]+z[1]*z[1]
        phase_trace.append({'step': t, 'D': D, 'X': X, 'I_target': I, 'I_reference': I_ref,
                            'identity_equal': D*D+X*X == I*I_ref})
    target_inputs = []
    for t, row in enumerate(target['center_inputs']):
        old, new = target['center_trace'][t], target['center_trace'][t+1]
        target_inputs.append({**row, 'ell': new[1]+old[0]})
    target['center_inputs'] = target_inputs
    target['reference'] = reference
    target['phase_trace'] = phase_trace
    target['causal_separation'] = {'non_reference_to_reference_region': to_reference,
                                  'reference_to_target_region': to_target,
                                  'valid': (to_reference is None or to_reference > 40) and to_target > 40}
    return target


def case_assessment(case, observations):
    mask = case['control']
    expected = ALPHABET[(-case['delay']) % 4] if mask == '11' else ALPHABET[case['phase']] if mask == '01' else (0, 0)
    trace = observations['phase_trace'][32:41]
    predicted = all((r['D'], r['X']) == expected for r in trace)
    isolation = all(not observations['boundary_inputs'][t]['nonzero_external_terms'] for t in range(32, 40))
    if mask[1] == '1':
        local_hold = any(c['kind'] == 'retained_orbit' and c['start'] == 32
                         and c['R'] == [1, case['clock_remainder']]
                         for c in observations['candidate_holds'])
    else:
        region = observations['region_trace'][32:41]
        local_hold = all(frame == region[0] for frame in region) and all(not(v[0] or v[1]) for frame in region for v in frame)
    quotients_zero = all(observations['center_inputs'][t]['u'] == observations['center_inputs'][t]['ell'] == 0
                         for t in range(32, 40))
    ref = observations['reference']
    reference_valid = (ref['complete_region_matches_isolated_formula'] and ref['all_external_terms_zero']
                       and all(row['u'] == row['ell'] == 0 for row in ref['inputs']))
    return {'expected_DX': list(expected), 'prediction_matches': predicted,
            'target_complete_hold': local_hold, 'target_external_terms_zero': isolation,
            'target_hold_input_and_quotient_zero': quotients_zero,
            'reference_valid': reference_valid,
            'causal_separation_valid': observations['causal_separation']['valid'],
            'phase_identity_all_states': all(r['identity_equal'] for r in observations['phase_trace']),
            'passed': all((predicted, local_hold, isolation, quotients_zero, reference_valid,
                           observations['causal_separation']['valid']))}


def group_assessment(rows):
    by = {r['case']['control']: r for r in rows}
    addresses = set().union(*(r['states'][0].cells for r in rows))
    matched = all(len({r['states'][0].at(a).r for r in rows}) == 1 for a in addresses)
    success = matched and all(r['case_assessment']['passed'] for r in rows)
    case = rows[0]['case']
    changed = case['phase'] != (-case['delay']) % 4
    hashes = {mask: state_sha256(row['states'][-1]) for mask, row in by.items()}
    return {'geometry': {k: v for k, v in case.items() if k != 'control'},
            'matched_initial_remainders': matched, 'synchronization_passed': success,
            'expected_changed_phase': changed, 'retained_changed_phase': bool(success and changed),
            'already_aligned': bool(success and not changed),
            'case_verdicts': {mask: r['case_assessment'] for mask, r in by.items()},
            'full_state_final_hashes': hashes, 'four_final_states_distinct': len(set(hashes.values())) == 4,
            'scope': 'Passive relative-phase storage; not a physical comparator or unconditional presence latch.'}


def selected(case):
    return ((case['side'], case['clock_remainder'], case['phase'], case['delay'])
            in ((129, 0, 0, 1), (161, 4, 3, 5)))


def run(output):
    output = Path(output)
    raw_protocol = PROTOCOL.read_bytes()
    protocol = json.loads(raw_protocol)
    output.mkdir(parents=True, exist_ok=False)
    (output/'records').mkdir()
    (output/'protocol.json').write_bytes(raw_protocol)
    sources = [Path(__file__), PROTOCOL, Path(base.__file__), base.PROTOCOL,
               *sorted((ROOT/'universe24').rglob('*.py')), *sorted((ROOT/'research/components').glob('*.py')),
               ROOT/'research/experiments/run.py', ROOT/'research/presenter/export.py']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    cases = list(geometries(protocol))
    registration = {'format': 'universe24-staged-phase-registration-v1',
                    'protocol_sha256': hashlib.sha256(raw_protocol).hexdigest(),
                    'source_sha256': hashes, 'registered_cases': 4*len(cases), 'geometries': cases,
                    'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                    'registered_before_capture': True, 'seed': None}
    base.write_json(output/'registration.json', registration)
    started_cpu, started_wall = time.process_time(), time.monotonic()
    groups, ledger, examples = [], [], []
    used_bytes = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    reason = None
    for geometry in cases:
        if time.process_time()-started_cpu >= protocol['budget']['max_cpu_seconds']:
            reason = 'cpu_budget'
            break
        rows = []
        for mask in ('00', '10', '01', '11'):
            case = {**geometry, 'control': mask}
            spec = case_spec(case, protocol)
            prepared = assemble(spec)
            recorded = run_experiment(spec)
            states = recorded_states(recorded['experiment'])
            observations = observe(case, prepared, states)
            if observations['active_boundary_hits']:
                raise AssertionError('Unexpected active boundary contact')
            rows.append({'case': case, 'spec': spec, 'assembly': recorded['assembly'],
                         'experiment': recorded['experiment'], 'states': states,
                         'observations': observations, 'case_assessment': case_assessment(case, observations)})
        assessment = group_assessment(rows)
        blobs = []
        for row in rows:
            wrapper = {'format': 'universe24-staged-phase-record-v1', 'spec': row['spec'],
                       'assembly': row['assembly'], 'experiment': row['experiment'],
                       'observations': row['observations'], 'assessment': assessment}
            raw = base.canonical(wrapper).encode()
            blobs.append((row, raw, gzip.compress(raw, mtime=0)))
        if used_bytes+sum(len(blob) for _, _, blob in blobs) > protocol['budget']['max_recorded_bytes']-5000000:
            reason = 'data_budget'
            break
        for row, raw, compressed in blobs:
            identity = row['spec']['id']
            record = 'records/'+identity+'.json.gz'
            (output/record).write_bytes(compressed)
            used_bytes += len(compressed)
            ledger.append({'id': identity, 'case': row['case'], 'record': record,
                           'record_sha256': hashlib.sha256(raw).hexdigest(),
                           'record_gzip_sha256': hashlib.sha256(compressed).hexdigest(),
                           'initial_state_sha256': state_sha256(row['states'][0]),
                           'final_state_sha256': state_sha256(row['states'][-1]),
                           'assessment': row['case_assessment'], 'frames': 41, 'transitions': 40,
                           'full_state_inverse': row['experiment']['provenance']['full_rewind_equal']})
            if selected(row['case']):
                examples.append(row['experiment'])
        groups.append(assessment)
        print(f"{len(ledger)}/256 {geometry['id']} sync={assessment['synchronization_passed']} changed={assessment['retained_changed_phase']}", flush=True)
    if any(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() != sha for p, sha in hashes.items()):
        raise RuntimeError('Execution source changed during phase study')
    result = {'format': 'universe24-staged-phase-result-v1', 'status': 'completed' if reason is None else 'budget_stopped',
              'stop_reason': reason, 'protocol_sha256': registration['protocol_sha256'],
              'registered_cases': 256, 'completed_cases': len(ledger), 'groups': groups, 'cases': ledger,
              'not_run_geometries': cases[len(groups):],
              'synchronization_groups': sum(g['synchronization_passed'] for g in groups),
              'retained_changed_phase_groups': sum(g['retained_changed_phase'] for g in groups),
              'already_aligned_groups': sum(g['already_aligned'] for g in groups),
              'all_references_valid': all(c['assessment']['reference_valid'] for c in ledger),
              'all_full_state_inverses': all(c['full_state_inverse'] for c in ledger),
              'displayed_experiments': len(examples), 'cpu_seconds': time.process_time()-started_cpu,
              'wall_seconds': time.monotonic()-started_wall,
              'scope': protocol['claim']}
    base.write_json(output/'result.json', result)
    (output/'experiments.json').write_text(base.canonical(bundle(examples, title='The Presenter: same-board phase memory'))+'\n')
    if sum(p.stat().st_size for p in output.rglob('*') if p.is_file()) > protocol['budget']['max_recorded_bytes']:
        raise RuntimeError('Phase evidence exceeds recorded data budget')
    print(base.canonical({k: result[k] for k in ('completed_cases', 'synchronization_groups',
                                               'retained_changed_phase_groups', 'already_aligned_groups', 'cpu_seconds')}), flush=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    return run(parser.parse_args(argv).output)


if __name__ == '__main__':
    main()
