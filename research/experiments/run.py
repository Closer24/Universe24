"""Record a generic assembled experiment; observations cannot affect evolution.

python -m research.experiments.run --spec SPEC.json --output NEW_DIRECTORY
The input can be one experiment or a study containing an experiments list.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import time

from research.components import (BoardSpec, TensorSpec, Patch, Socket, SignalSource,
                                 GuideSegment, Receiver, PairedArm, GuidedPacketSource, place, finalize, plain,
                                 LocalizedSixClock, CompactFiveClock, CooperativeClockPair,
                                 EvenPacketSource, RemainderTarget, RegisterWriter, SourceOverlapRegister)
from research.presenter.export import (capture, bundle, write_bundle, decimal_string,
                                       parse_decimal, _portable_state)
from research.presenter.build import build, _new_file
from universe24 import Channel
from universe24.observation.clicks import classify

ROOT = Path(__file__).resolve().parents[2]
FORMAT = 'universe24-assembly-experiment-v1'
STUDY = 'universe24-component-study-v1'
RECIPES = {'SignalSource': SignalSource, 'GuideSegment': GuideSegment,
           'Receiver': Receiver, 'PairedArm': PairedArm, 'GuidedPacketSource': GuidedPacketSource,
           'LocalizedSixClock': LocalizedSixClock, 'CompactFiveClock': CompactFiveClock,
           'CooperativeClockPair': CooperativeClockPair, 'EvenPacketSource': EvenPacketSource,
           'RemainderTarget': RemainderTarget, 'RegisterWriter': RegisterWriter,
           'SourceOverlapRegister': SourceOverlapRegister}


def portable(value):
    value = plain(value)
    if isinstance(value, dict):
        return {key: portable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [portable(item) for item in value]
    if type(value) is int and abs(value) > 2**53-1:
        return decimal_string(value)
    return value


def canonical(value):
    return json.dumps(portable(value), sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode('ascii')).hexdigest()


def write_json(path, value):
    _new_file(Path(path), (canonical(value)+'\n').encode('ascii'))


def _keys(value, allowed, required, label):
    if not isinstance(value, dict) or set(value)-set(allowed) or set(required)-set(value):
        raise ValueError('Unsupported or missing ' + label + ' fields')


def _counter(value):
    if type(value) is int:
        return value
    return parse_decimal(value)


def _raw_patch(params, tensor):
    _keys(params, ('kind','cells','ports','sources','sockets','readouts','background','evidence_domains'),
          ('kind','cells'), 'raw patch')
    rows = []
    for row in params['cells']:
        if not isinstance(row, (list, tuple)) or len(row) != 7:
            raise ValueError('Raw cells require [x,y,z,g,a,b,r]')
        rows.append((tuple(row[:4]), (_counter(row[4]), _counter(row[5]), row[6])))
    sockets = tuple(Socket(**item) for item in params.get('sockets', []))
    return Patch(kind=params['kind'], cells=rows, tensor=tensor,
                 background=tuple(params.get('background', (0,0,2))),
                 ports=params.get('ports', {}), sources=params.get('sources', {}),
                 sockets=sockets, readouts=params.get('readouts', ()),
                 evidence_domains=params.get('evidence_domains', ()))


def assemble(spec):
    """Build exactly one immutable board from a data-only experiment definition."""
    _keys(spec, ('format','id','title','description','question','board','components','steps',
                'readouts','detectors','view','controls','budget','provenance','seed'),
          ('format','id','board','components','steps'), 'experiment')
    if spec['format'] != FORMAT:
        raise ValueError('Unsupported experiment format')
    if not isinstance(spec['id'], str) or not spec['id']:
        raise ValueError('An experiment requires a nonempty ID')
    if type(spec['steps']) is not int or spec['steps'] < 0:
        raise ValueError('Steps must be a nonnegative integer')
    item = spec['board']
    _keys(item, ('side','background','body_signs','tensor'), ('side',), 'board')
    if 'tensor' in item and 'body_signs' in item:
        raise ValueError('Specify the complete tensor or signs, not two tensor definitions')
    tensor = TensorSpec(**item['tensor']) if 'tensor' in item else TensorSpec.from_signs(item.get('body_signs', (1,1,1)))
    board = BoardSpec(item['side'], tuple(item.get('background', (0,0,2))), tensor)
    placements = []
    if not isinstance(spec['components'], list):
        raise ValueError('Components must be a list')
    for item in spec['components']:
        _keys(item, ('name','recipe','params','at','orientation','wrap'),
              ('name','recipe','at'), 'component')
        params = copy.deepcopy(item.get('params', {}))
        if not isinstance(params, dict) or 'tensor' in params:
            raise ValueError('Component parameters cannot install a separate tensor')
        if item['recipe'] == 'Patch':
            patch = _raw_patch(params, tensor)
        else:
            if item['recipe'] not in RECIPES:
                raise ValueError('Unknown data-only component recipe')
            if item['recipe'] == 'SignalSource':
                for field in ('a','b'):
                    if field in params:
                        params[field] = _counter(params[field])
            if item['recipe'] == 'Receiver' and 'counters' in params:
                params['counters'] = [[_counter(v) for v in pair] for pair in params['counters']]
            patch = RECIPES[item['recipe']](**params, tensor=tensor)
        placements.append(place(patch, name=item['name'], at=item['at'],
                                orientation=item.get('orientation', 0), wrap=item.get('wrap', False)))
    return finalize(board, placements)


def _address(clause, prepared):
    if 'port' in clause:
        if 'address' in clause or clause['port'] not in prepared.ports:
            raise ValueError('Unknown or ambiguous readout port')
        index = clause.get('index', 0)
        if type(index) is not int or not 0 <= index < len(prepared.ports[clause['port']]):
            raise ValueError('Readout port index is out of range')
        return list(prepared.ports[clause['port']][index])
    if 'index' in clause or 'address' not in clause:
        raise ValueError('A readout needs one address or a named port')
    return list(prepared.initial.cube.validate_address(clause['address']))


def resolve_readouts(spec, prepared):
    if 'readouts' not in spec:
        return plain(prepared.readouts)
    result = []
    for readout in spec['readouts']:
        _keys(readout, ('id','label','kind','clauses'), ('id','label','kind','clauses'), 'readout')
        clauses = []
        for clause in readout['clauses']:
            _keys(clause, ('port','index','address','component','equals'), ('component','equals'), 'readout clause')
            clauses.append({'address': _address(clause, prepared), 'component': clause['component'], 'equals': clause['equals']})
        result.append({**readout, 'clauses': clauses})
    return result


def recorded_states(experiment):
    """Read complete saved states; no extra evolution is performed."""
    bg = Channel(0,0,experiment['background'][2])
    return [_portable_state(frame, experiment['side'], bg) for frame in experiment['frames']]


def observe(experiment, prepared, detectors, *, deadline):
    """Fixed passive C/R and magnitude reports on named addresses, after capture."""
    states = recorded_states(experiment)
    reports = {key: {'addresses': plain(prepared.ports[key]), 'trace': [],
                     'record_event_times': [], 'arithmetic_events': []} for key in detectors}
    for t, state in enumerate(states):
        if time.monotonic() > deadline:
            raise TimeoutError('Experiment observation budget exhausted')
        sums = prepared.engine.input_sums(state)
        for key, report in reports.items():
            addresses = prepared.ports[key]
            values = [state.at(a) for a in addresses]
            symbol = [v.r for v in values]
            arithmetic = []
            if t:
                old = [states[t-1].at(a) for a in addresses]
                if symbol != [v.r for v in old]:
                    report['record_event_times'].append(t)
                for address, before, after in zip(addresses, old, values):
                    event = classify(before, after)
                    if event is not None:
                        kind, quotient = event
                        arithmetic.append({'step': t, 'address': list(address), 'kind': kind,
                                           'quotient': decimal_string(quotient)})
            terms = []
            for address in addresses:
                row = []
                for d in range(6):
                    sender = state.cube.adjacent(address, d, prepared.engine.coupling.ports[d][address[3]])
                    row.append({'direction': d, 'address': list(sender),
                                'weight': prepared.engine.coupling.weights[d][address[3]],
                                'b': decimal_string(state.at(sender).b)})
                terms.append(row)
            report['trace'].append({'step': t, 'detector': [[decimal_string(v.a), decimal_string(v.b), v.r] for v in values],
                                    'memory': symbol, 'magnitude': [decimal_string(v.a*v.a+v.b*v.b) for v in values],
                                    'next_input': [decimal_string(sums.get(a, 0)) for a in addresses],
                                    'six_inputs': terms, 'arithmetic_events': arithmetic})
            report['arithmetic_events'].extend(arithmetic)
    return reports


def source_hashes():
    files = [*sorted((ROOT/'research/components').glob('*.py')), Path(__file__),
             ROOT/'research/presenter/export.py', *sorted((ROOT/'universe24').rglob('*.py'))]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def run_experiment(spec, output=None):
    """Finalize once; capture with the existing engine; then read fixed observers.

    Returns experiment (complete Presenter recording), observations and assembly.
    Counter-valued observations use exact decimal strings, including quotients.
    """
    spec = json.loads(canonical(spec))
    prepared = assemble(spec)
    readouts = resolve_readouts(spec, prepared)
    detectors = spec.get('detectors', [])
    if not isinstance(detectors, list) or len(set(detectors)) != len(detectors) or any(d not in prepared.ports for d in detectors):
        raise ValueError('Detectors must be distinct named ports fixed before capture')
    budget = spec.get('budget', {})
    _keys(budget, ('max_frames','max_cells','max_bytes','max_seconds'), (), 'budget')
    limits = {'max_frames': 10000, 'max_cells': 500000, 'max_bytes': 67108864, 'max_seconds': 120}
    limits.update(budget)
    seconds = limits['max_seconds']
    if type(seconds) not in (int,float) or not 0 < seconds <= 3600:
        raise ValueError('Experiment budget must be 0 < max_seconds <= 3600')
    view = spec.get('view')
    if view is not None and 'port' in view:
        _keys(view, ('port','index'), ('port',), 'view')
        addr = _address(view, prepared)
        view = {'position': addr[:3], 'channel': addr[3]}
    sources = source_hashes()
    destination = Path(output) if output is not None else None
    if destination:
        destination.mkdir(parents=True, exist_ok=False)
        write_json(destination/'spec.json', spec)
        write_json(destination/'assembly.json', prepared.manifest)
    start = time.monotonic()
    try:
        experiment = capture(prepared.engine, prepared.initial, spec['steps'],
                             id=spec['id'], title=spec.get('title', spec['id']),
                             description=spec.get('description', ''), readouts=readouts, view=view, **limits)
        observations = observe(experiment, prepared, detectors, deadline=start+seconds) if detectors else {}
        if source_hashes() != sources:
            raise RuntimeError('Assembly or recording sources changed during the experiment')
        experiment['provenance'].update({'assembly_spec_sha256': digest(spec),
                                         'assembly_manifest_sha256': digest(prepared.manifest),
                                         'component_source_sha256': sources,
                                         'predeclared_controls': spec.get('controls', []),
                                         'research_provenance': spec.get('provenance', {}),
                                         'assembly_validity_is_not_behavioral_acceptance': True})
        result = {'format': 'universe24-component-result-v1', 'status': 'completed',
                  'id': spec['id'], 'experiment': experiment, 'observations': observations,
                  'assembly': portable(prepared.manifest), 'spec_sha256': digest(spec),
                  'source_sha256': sources, 'elapsed_seconds': time.monotonic()-start,
                  'behavioral_acceptance': 'Defined and assessed by the separate research protocol',
                  'physical_light_established': False}
        if destination:
            write_bundle(destination/'experiments.json', bundle([experiment]))
            write_json(destination/'result.json', {k: v for k, v in result.items() if k not in ('experiment','assembly')})
        return result
    except Exception as exc:
        if destination:
            write_json(destination/'failure.json', {'status': 'inconclusive', 'type': type(exc).__name__,
                       'reason': str(exc), 'spec_sha256': digest(spec), 'source_sha256': sources})
        raise


def run_study(spec, output, *, presenter=True):
    _keys(spec, ('format','title','experiments','protocol'), ('format','experiments'), 'study')
    if spec['format'] != STUDY or not isinstance(spec['experiments'], list) or not 1 <= len(spec['experiments']) <= 64:
        raise ValueError('A study must contain 1..64 complete experiments')
    if len({item['id'] for item in spec['experiments']}) != len(spec['experiments']):
        raise ValueError('Study experiment IDs must be unique')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    write_json(output/'study.json', spec)
    recordings = []
    results = []
    for index, item in enumerate(spec['experiments']):
        result = run_experiment(item, output/'cases'/f'{index:03d}')
        recordings.append(result['experiment'])
        results.append({'id': item['id'], 'case': f'cases/{index:03d}', 'spec_sha256': result['spec_sha256']})
    data = bundle(recordings, title=spec.get('title', 'Assembled experiments'))
    write_bundle(output/'experiments.json', data)
    html = None
    if presenter:
        html, _ = build(output/'experiments.json', output/'The_Presenter.html')
    write_json(output/'manifest.json', {'format': STUDY, 'cases': results,
               'experiments': len(recordings), 'frames': sum(len(e['frames']) for e in recordings),
               'html': html.name if html else None, 'generic_presenter_sources_unchanged_by_runner': True})
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    def reject(value):
        raise ValueError('Nonfinite JSON value: ' + value)
    spec = json.loads(args.spec.read_text(), parse_constant=reject)
    if spec.get('format') == FORMAT:
        spec = {'format': STUDY, 'experiments': [spec]}
    print(json.dumps(run_study(spec, args.output), indent=2))


if __name__ == '__main__':
    main()
