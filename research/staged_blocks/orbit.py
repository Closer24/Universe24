"""Data-only shielded counter orbits and their prospectively specified audit.

The preparation is a clock candidate installed at time zero, not signal-written
memory. Only the unchanged reference Engine performs evolution.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.components import BoardSpec, Patch, TensorSpec, finalize, place, plain
from research.experiments.run import recorded_states, run_experiment
from research.presenter.build import build
from research.presenter.export import bundle, write_bundle
from universe24 import Channel, State
from universe24.core.group_2o import DIRECTIONS
from universe24.observation.clicks import classify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / 'orbit_protocol.json'
BACKGROUND = Channel(0, 0, 2)


def _integer(value, label):
    if type(value) is not int:
        raise ValueError(label + ' must be an exact integer')
    return value


def rotate_counters(a, b, phase):
    """Algebraic four-cycle, used only to construct/observe initial data."""
    return ((a, b), (b, -a), (-a, -b), (-b, a))[phase % 4]


def input_prefixes(a, b):
    return (0, b, b-a, -a, 0)


def halo_remainder(a, b, weight):
    """Choose the valid even remainder closest to background 2."""
    values = [weight * v for v in input_prefixes(a, b)]
    lower, upper = -2*min(values), 4-2*max(values)
    if lower > upper:
        raise ValueError('No passive zero-counter halo can shield these counters')
    return min(max(2, lower), upper)


def ShieldedOrbit(*, channel=0, a=1, b=0, r=2, tensor=None,
                  present=True, phase=0, halo_remainders=None):
    """Return an immutable Patch with a center and all 48 channels of its halo.

    Valid domain: |a|+|b| <= 2, channel 0..47, r 0..5, phase 0..3.
    ``phase`` advances the *entire* analytic preparation, including its retained
    remainder halo. ``present=False`` removes only its initial center counters.
    Arbitrary additional incoming influences are outside the isolated theorem.
    """
    for value, label in ((channel, 'channel'), (a, 'a'), (b, 'b'), (r, 'r'), (phase, 'phase')):
        _integer(value, label)
    if not 0 <= channel < 48 or not 0 <= r < 6 or not 0 <= phase < 4:
        raise ValueError('Channel, remainder or phase outside its declared domain')
    if abs(a) + abs(b) > 2:
        raise ValueError('The shielded orbit requires |a|+|b| <= 2')
    if type(present) is not bool:
        raise ValueError('present must be Boolean')
    tensor = TensorSpec() if tensor is None else tensor
    if not isinstance(tensor, TensorSpec):
        raise TypeError('tensor must be an exact TensorSpec')
    weights = [tensor.weights[d][channel] for d in range(6)]
    if halo_remainders is None:
        remainders = tuple(halo_remainder(a, b, w) for w in weights)
    else:
        remainders = tuple(halo_remainders)
        if len(remainders) != 6 or any(type(v) is not int or not 0 <= v < 6 for v in remainders):
            raise ValueError('halo_remainders needs six valid exact remainders')
    for remainder, weight in zip(remainders, weights):
        if any(not 0 <= remainder + 2*weight*p <= 5 for p in input_prefixes(a, b)):
            raise ValueError('A specified halo remainder crosses a quotient threshold')
    center = (0, 0, 0, channel)
    halo = tuple((*DIRECTIONS[d], tensor.ports[d][channel]) for d in range(6))
    positions = ((0, 0, 0), *DIRECTIONS)
    cells = {(*xyz, g): BACKGROUND for xyz in positions for g in range(48)}
    aa, bb = rotate_counters(a, b, phase) if present else (0, 0)
    cells[center] = (aa, bb, r)
    for address, remainder, weight in zip(halo, remainders, weights):
        cells[address] = (0, 0, remainder + 2*weight*input_prefixes(a, b)[phase])
    readouts = []
    for p in range(4):
        pa, pb = rotate_counters(a, b, p)
        clauses = [{'address': center, 'component': key, 'equals': str(value)}
                   for key, value in zip(('a', 'b', 'r'), (pa, pb, r))]
        for address, remainder, weight in zip(halo, remainders, weights):
            clauses.extend({'address': address, 'component': key, 'equals': str(value)}
                           for key, value in zip(('a', 'b', 'r'),
                               (0, 0, remainder + 2*weight*input_prefixes(a, b)[p])))
        readouts.append({'id': 'phase-' + str(p), 'label': 'Center and halo phase ' + str(p) + ' (projection)',
                         'kind': 'all_equal', 'clauses': clauses})
    resources = {'kind': 'shielded-orbit-contract-v1', 'model_role': 'prepared-clock-candidate',
                 'signal_written_memory_established': False, 'center': center,
                 'halo_recipients': halo, 'protected_nodes': positions,
                 'protected_channels': 336, 'base_counters': [a, b], 'center_remainder': r,
                 'initial_phase': phase, 'present': present, 'base_halo_remainders': remainders,
                 'period': 4 if present and (a or b) else 1,
                 'tensor_fingerprint': tensor.fingerprint,
                 'environment': 'No additional input to the center or any halo channel. '
                                'Shared halos require a new composition proof or complete-state validation.',
                 'scope': 'Every L>=3 and fixed body-sign triple, isolated preparation only.'}
    return Patch('shielded-orbit', cells, tensor=tensor,
                 ports={'center': (center,), 'center_node': tuple((0,0,0,g) for g in range(48)),
                        'halo': halo, 'region': tuple(cells)},
                 sources={'orbit': (center,)}, readouts=tuple(readouts),
                 evidence_domains=(resources,))


def prepare_orbit(*, side=5, location=None, body_signs=(1,1,1), **parameters):
    tensor = TensorSpec.from_signs(body_signs)
    location = (side//2,)*3 if location is None else tuple(location)
    patch = ShieldedOrbit(tensor=tensor, **parameters)
    return finalize(BoardSpec(side, tensor=tensor),
                    [place(patch, at=location, name='orbit', wrap=True)])


def raw_patch(patch):
    """Portable existing-composer contract; no new recipe dispatch is needed."""
    return {'kind': patch.kind, 'cells': [[*address, *value] for address, value in patch.cells],
            'ports': plain(patch.ports), 'sources': plain(patch.sources),
            'readouts': plain(patch.readouts), 'evidence_domains': plain(patch.evidence_domains)}


def canonical(value):
    return json.dumps(plain(value), sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def write_json(path, value):
    Path(path).write_text(canonical(value)+'\n')


def registered_cases(protocol):
    """Deterministic case enumeration frozen before any observation."""
    vectors = [list(v) for v in itertools.product(range(-2,3), repeat=2) if sum(map(abs,v)) <= 2]
    cases = []
    for index, (signs, channel) in enumerate(itertools.product(itertools.product((-1,1), repeat=3), range(48))):
        side = protocol['sides'][index % len(protocol['sides'])]
        a, b = vectors[index % len(vectors)]
        cases.append({'id': f'orbit-label-{index:03d}', 'family': 'labels', 'side': side,
                      'location': [0, side-1, channel % side], 'body_signs': list(signs),
                      'channel': channel, 'a': a, 'b': b, 'r': index % 6, 'phase': index % 4,
                      'present': True})
    for index, ((a,b), r, phase) in enumerate(itertools.product(vectors, range(6), range(4))):
        cases.append({'id': f'orbit-values-{index:03d}', 'family': 'values', 'side': 5,
                      'location': [2,2,2], 'body_signs': [1,-1,1] if index % 2 else [1,1,1],
                      'channel': index % 48, 'a': a, 'b': b, 'r': r, 'phase': phase, 'present': True})
    for phase, r in itertools.product(range(4), range(6)):
        matching_index = (vectors.index([1,0])*6+r)*4+phase
        cases.append({'id': f'orbit-off-p{phase}-r{r}', 'family': 'off', 'side': 5,
                      'location': [2,2,2], 'body_signs': [1,-1,1] if matching_index % 2 else [1,1,1],
                      'channel': matching_index % 48,
                      'a': 1, 'b': 0, 'r': r, 'phase': phase, 'present': False})
    for direction, field, delta in itertools.product(range(6), ('r','b'), (-1,1)):
        cases.append({'id': f'orbit-disturb-d{direction}-{field}{delta:+d}', 'family': 'disturbance',
                      'side': 9, 'location': [4,4,4], 'body_signs': [1,1,1], 'channel': 0,
                      'a': 1, 'b': 0, 'r': 2, 'phase': 0, 'present': True,
                      'disturbance': {'direction': direction, 'field': field,
                                      'delta': 2*delta if field == 'r' else delta}})
    return cases


def parameters(case):
    return {key: case[key] for key in ('channel','a','b','r','phase','present')}


def case_spec(case, steps):
    tensor = TensorSpec.from_signs(case['body_signs'])
    patch = ShieldedOrbit(tensor=tensor, **parameters(case))
    raw = raw_patch(patch)
    if 'disturbance' in case:
        disturbance = case['disturbance']
        address = tuple(patch.ports['halo'][disturbance['direction']])
        row = next(row for row in raw['cells'] if tuple(row[:4]) == address)
        offset = {'a':4, 'b':5, 'r':6}[disturbance['field']]
        row[offset] += disturbance['delta']
        if disturbance['field'] == 'r':
            row[offset] %= 6
    return {'format': 'universe24-assembly-experiment-v1', 'id': case['id'],
            'title': 'Prepared clock: ' + case['id'],
            'description': 'An initial counter orbit with its retained remainder halo. '
                           'Phase labels are center/halo projections; scientific acceptance compares the complete board. '
                           'The complete Rule3 board is recorded; this is not incoming-signal capture.',
            'board': {'side': case['side'], 'body_signs': case['body_signs'], 'background': [0,0,2]},
            'steps': steps, 'components': [{'name':'orbit', 'recipe':'Patch', 'params':raw,
                                          'at':case['location'], 'wrap':True}],
            'detectors': [], 'view': {'port':'orbit.center'}, 'controls':case,
            'budget': {'max_frames':steps+1, 'max_cells':500000, 'max_bytes':67108864, 'max_seconds':30}}


def assess(case, states):
    center = (*case['location'], case['channel'])
    tensor = TensorSpec.from_signs(case['body_signs'])
    local = ShieldedOrbit(tensor=tensor, **parameters(case))
    side = case['side']
    halo = [tuple((v+offset) % side for v, offset in zip(address[:3], case['location']))
            + (address[3],) for address in local.ports['halo']]
    expected_states = {}
    for phase in range(4) if case['present'] else (case['phase'],):
        expected_parameters = parameters(case)
        expected_parameters['phase'] = phase
        expected_states[phase] = prepare_orbit(side=side, location=case['location'],
                                 body_signs=case['body_signs'], **expected_parameters).initial
    events, samples, first_mismatch = [], [], None
    for step, state in enumerate(states):
        expected = expected_states[(case['phase']+step) % 4 if case['present'] else case['phase']]
        if state != expected and first_mismatch is None:
            first_mismatch = step
        samples.append({'step':step, 'center':list(state.at(center)),
                        'center_all48':[list(v) for v in state.node(case['location'])],
                        'halo':[list(state.at(address)) for address in halo],
                        'center_magnitude':state.at(center).a**2+state.at(center).b**2,
                        'noncenter_counter_addresses':[list(ad) for ad,v in sorted(state.cells.items())
                                                       if ad != center and (v.a or v.b)]})
        if step:
            old = states[step-1]
            for address in sorted(old.cells.keys() | state.cells.keys()):
                event = classify(old.at(address), state.at(address))
                if event is not None:
                    events.append({'step':step, 'address':list(address), 'kind':event[0], 'ell':event[1]})
    period = next((p for p in range(1, min(4,len(states)-1)+1) if states[p] == states[0]), None)
    expected_period = 4 if case['present'] and (case['a'] or case['b']) else 1
    return {'first_full_state_formula_mismatch':first_mismatch, 'minimal_return_at_most_four':period,
            'expected_period':expected_period, 'all_world_C':events, 'samples':samples,
            'isolated_contract_passed':first_mismatch is None and period == expected_period and not events,
            'complete_region_and_board_formula_passed':first_mismatch is None,
            'phase_projection_is_not_acceptance':True,
            'classification':'finite-disturbance-observation' if 'disturbance' in case else 'prepared-orbit-validation',
            'signal_written_memory_established':False}


def source_hashes():
    paths = [Path(__file__), PROTOCOL, *sorted((ROOT/'universe24').rglob('*.py')),
             *sorted((ROOT/'research/components').rglob('*.py')),
             ROOT/'research/experiments/run.py', ROOT/'research/presenter/export.py']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    protocol_raw = PROTOCOL.read_bytes()
    protocol, sources = json.loads(protocol_raw), source_hashes()
    cases = registered_cases(protocol)
    displayed_ids = [case['id'] for case in cases
                     if case['family'] in ('values','off') and (case['a'],case['b'],case['r']) == (1,0,2)]
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'records').mkdir()
    (args.output/'protocol.json').write_bytes(protocol_raw)
    registration = {'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                    'protocol_sha256':hashlib.sha256(protocol_raw).hexdigest(), 'source_sha256':sources,
                    'seed':None, 'case_count':len(cases), 'cases':cases,
                    'representative_presenter_ids':displayed_ids,
                    'representative_selection':'Four registered unit-clock phases and their matched absent controls; all cases remain in complete paged bundles.'}
    write_json(args.output/'registration.json', registration)
    started, cpu = time.monotonic(), time.process_time()
    rows, page, pages, display = [], [], [], []
    def flush():
        if not page:
            return
        filename = f'experiments-{len(pages)+1:03d}.json'
        write_bundle(args.output/filename, bundle(page, title='Prepared shielded clocks'))
        pages.append(filename)
        page.clear()
    for number, case in enumerate(cases, 1):
        if time.process_time()-cpu > protocol['budget']['cpu_seconds']:
            write_json(args.output/'failure.json', {'reason':'Registered CPU budget exhausted', 'completed':len(rows)})
            raise RuntimeError('Registered CPU budget exhausted')
        spec = case_spec(case, protocol['steps'])
        result = run_experiment(spec)
        assessment = assess(case, recorded_states(result['experiment']))
        record = {'case':case, 'spec':spec, 'assembly':result['assembly'],
                  'experiment':result['experiment'], 'assessment':assessment}
        path = args.output/'records'/(case['id']+'.json.gz')
        path.write_bytes(gzip.compress(canonical(record).encode(), mtime=0))
        rows.append({'id':case['id'], 'family':case['family'], 'case':case,
                     'record':str(path.relative_to(args.output)),
                     'record_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                     'isolated_contract_passed':assessment['isolated_contract_passed'],
                     'first_full_state_formula_mismatch':assessment['first_full_state_formula_mismatch'],
                     'C_events':len(assessment['all_world_C']),
                     'full_rewind_equal':result['experiment']['provenance']['full_rewind_equal']})
        page.append(result['experiment'])
        if case['id'] in displayed_ids:
            display.append(result['experiment'])
        if len(page) == 64:
            flush()
        if number % 64 == 0:
            print(f'{number}/{len(cases)} complete recorded orbit cases', flush=True)
    flush()
    assert source_hashes() == sources and PROTOCOL.read_bytes() == protocol_raw
    clean = [row for row in rows if row['family'] != 'disturbance']
    report = {'format':'universe24-staged-orbit-result-v1', 'registration':registration,
              'cases':rows, 'engine_runs':len(rows), 'frames':len(rows)*(protocol['steps']+1),
              'forward_inverse_transitions':len(rows)*protocol['steps'],
              'unperturbed_cases':len(clean), 'unperturbed_passed':sum(row['isolated_contract_passed'] for row in clean),
              'disturbance_cases':len(rows)-len(clean),
              'all_full_rewinds_equal':all(row['full_rewind_equal'] for row in rows),
              'portable_files':pages, 'cpu_seconds':time.process_time()-cpu,
              'wall_seconds':time.monotonic()-started, 'prepared_only':True,
              'signal_written_memory_established':False}
    write_json(args.output/'result.json', report)
    write_bundle(args.output/'experiments.json', bundle(display, title='Prepared clocks: four phases and matched absent controls'))
    build(args.output/'experiments.json', args.output/'The_Presenter.html')
    print(canonical({k:v for k,v in report.items() if k not in ('cases','registration')}))


if __name__ == '__main__':
    main()
