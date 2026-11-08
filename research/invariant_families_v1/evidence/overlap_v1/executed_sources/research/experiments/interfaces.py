"""Data adapters for retained studies; all execution uses the generic runner."""
from copy import deepcopy

from .run import FORMAT


def signal_case_spec(case, source_mask=(True, True), *, identifier=None):
    """Express a legacy guide/receiver preparation as four independent recipes."""
    side = case['side']
    origin = [side//2]*3
    offsets = case['source_offsets']
    start, stop = (min(offsets), max(offsets)) if case.get('guide_mode') == 'between_sources' else (-case['extent'], case['extent'])
    slots = [x for x in [*offsets, 0] if start <= x <= stop]
    components = [
        {'name': 'guide', 'recipe': 'GuideSegment', 'at': origin,
         'params': {'start': start, 'stop': stop, 'sockets': slots}},
        {'name': 'receiver', 'recipe': 'Receiver', 'at': origin,
         'params': {'remainders': case['target_remainders']}},
    ]
    if len(source_mask) != 2 or any(type(v) is not bool for v in source_mask):
        raise ValueError('Two independent initial-source flags required')
    for i, (offset, ab, present) in enumerate(zip(offsets, case['source_ab'], source_mask)):
        components.append({'name': f'source-{i+1}', 'recipe': 'SignalSource',
                           'at': [origin[0]+offset, origin[1], origin[2]],
                           'params': {'a': ab[0], 'b': ab[1], 'present': present}})
    return {'format': FORMAT, 'id': identifier or case['id'],
            'title': identifier or case['id'],
            'description': 'Initial signal sources, an armed guide and a local clock/memory receiver, assembled from generic data recipes. Full states are replayed; these signals are not established physical light.',
            'board': {'side': side, 'body_signs': case.get('body_signs', [1,1,1]), 'background': [0,0,2]},
            'components': components, 'steps': case['steps'], 'detectors': ['receiver.memory'],
            'view': {'port': 'receiver.memory'},
            'controls': {'initial_source_mask': list(source_mask)},
            'provenance': {'data_adapter': 'signal_case_spec', 'legacy_case': deepcopy(case)}}


def paired_case_spec(case, *, identifier=None):
    """Shared source plus independently prepared arms; no special runtime routing."""
    origin = [case['side']//2]*3
    components = [{'name': 'source', 'recipe': 'SignalSource', 'at': origin,
                   'params': {'present': case.get('source_present', True)}}]
    detectors = ['source.signal']
    for index, (sign, variant) in enumerate(zip((-1,1), case['variants'])):
        if case.get('isolated_side') is not None and case['isolated_side'] != sign:
            continue
        name = 'left' if sign < 0 else 'right'
        params = {'variant': variant, 'direction': sign}
        if 'length' in case:
            params['length'] = case['length']
        if 'gate_pairs' in case:
            params['gate_pairs'] = case['gate_pairs'][index]
        components.append({'name': name, 'recipe': 'PairedArm', 'params': params, 'at': origin})
        detectors.append(name+'.outlet')
    return {'format': FORMAT, 'id': identifier or case['id'], 'title': identifier or case['id'],
            'description': 'A preloaded paired signal source and independently prepared transfer arms. One shared tensor; path labels do not change evolution. Blocking is a finite complete-state outlet comparison.',
            'board': {'side': case['side'], 'body_signs': case.get('body_signs', [1,1,1]), 'background': [0,0,2]},
            'components': components, 'steps': case['steps'], 'detectors': detectors,
            'view': {'port': 'source.signal'},
            'controls': {'initial_source_present': case.get('source_present', True),
                         'isolated_side': case.get('isolated_side')},
            'provenance': {'data_adapter': 'paired_case_spec', 'legacy_case': deepcopy(case)}}
