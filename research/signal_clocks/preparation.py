"""Data-only preparation of two initially supplied guide disturbances.

The source mask changes only counter values at t=0. No function in this module
advances, injects into, or modifies an already-running state.
"""
from universe24 import Channel, Coupling, Cube, Engine, State


def prepare(case, source_mask=(True, True)):
    side = case['side']
    origin = (side // 2, side // 2, side // 2)
    extent = case['extent']
    if side < 2 * extent + 3:
        raise ValueError('Guide must fit strictly inside the periodic cube')
    if len(source_mask) != 2 or any(type(v) is not bool for v in source_mask):
        raise ValueError('Two Boolean initial-source flags are required')
    cells = {}
    x, y, z = origin
    mode=case.get('guide_mode','full_segment')
    if mode not in ('full_segment','between_sources'):
        raise ValueError('Unknown initial guide preparation')
    span=(range(min(case['source_offsets']),max(case['source_offsets'])+1)
          if mode=='between_sources' else range(-extent,extent+1))
    for j in span:
        cells[(x+j,y,z,0)] = Channel(0,0,4)
        cells[(x+j,y,z,14)] = Channel(0,0,0)
    target_r = case['target_remainders']
    for g,r in zip((0,14), target_r):
        cells[(x,y,z,g)] = Channel(0,0,r)
    sources = []
    for present, offset, ab in zip(source_mask, case['source_offsets'], case['source_ab']):
        if not -extent < offset < extent or offset == 0:
            raise ValueError('Source must be a non-target interior guide site')
        position = (x+offset,y,z)
        sources.append(position)
        a,b = ab if present else (0,0)
        cells[(*position,0)] = Channel(a,b,2)
        cells[(*position,14)] = Channel(-a,-b,2)
    if sources[0] == sources[1]:
        raise ValueError('Independent source sites must be distinct')
    engine = Engine(Coupling(tuple(case.get('body_signs', [1,1,1]))))
    state = State(Cube(side), Channel(0,0,2), cells)
    return engine, state, {'origin':origin, 'detector':[(x,y,z,0),(x,y,z,14)],
                           'sources':sources}


def candidate_cases(family):
    """Deterministic frozen-family enumeration, without trajectory selection."""
    index = 0
    for remainders in family['target_remainder_pairs']:
        for geometry in family['geometries']:
            for d1,d2 in family['distance_pairs']:
                offsets = [-d1, d2 if geometry == 'opposed' else -d2]
                for phase1 in family['source_phases']:
                    for phase2 in family['source_phases']:
                        yield {'id':f'{family.get("id_prefix","candidate")}-{index:03d}', 'geometry':geometry,
                               'side':family['side'], 'extent':family['extent'],
                               'steps':family['steps'], 'body_signs':family['body_signs'],
                               'source_offsets':offsets, 'source_ab':[phase1,phase2],
                               'target_remainders':remainders,
                               'arrival_windows':[[d1,d1+1],[d2,d2+1]],
                               **({'guide_mode':family['guide_mode']} if 'guide_mode' in family else {})}
                        index += 1
