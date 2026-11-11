"""Optional local wave / C2 memory / response field, under unchanged Rule3.

This is a declared probe model, not a new Einstein source or a quantum
collapse prescription. No clock, tick, observer or event label drives it.
"""
from universe24.core import Tensor
from universe24.core.tensor import FORMAT
from universe24.core.lattice import DIRECTIONS, ZERO

LANES = ('px', 'nx', 'py', 'ny', 'pz', 'nz')
NAMES = tuple('wave.' + lane for lane in LANES) + (
    'wave.detector', 'wave.memory', 'wave.response')


def with_causal_wave(base=None):
    """Append nine gears; preserve every existing gear and tensor term.

    u_lane = 3 (b_lane(x-d) + b_lane(x+d))
    u_detector = 6 b_detector
    u_memory = 2 b_detector sum_d b_lane(x-d)
    u_response = 3 b_memory + 3 sum_d b_response(x+d)

    The memory and response are actual retained state, not filtered clicks.
    The one-way coupling is chosen probe wiring, not reciprocal gravity.
    """
    if base is not None and any(name in base.names for name in NAMES):
        raise ValueError('causal wave is already present')
    data = base.to_dict() if base is not None else {
        'format': FORMAT, 'gears': [], 'monomials': [], 'designated_one_way': []}
    data['gears'].extend({'name': name, 'label': 'audit' if name == 'wave.detector'
                          else 'official'} for name in NAMES)
    terms = data['monomials']
    designations = data['designated_one_way']

    def add(target, coefficient, factors, one_way=False):
        terms.append([target, coefficient, factors])
        if one_way:
            designations.append([target, factors,
                'Optional causal probe: directed reception and memory response; no reciprocal gravitational force claimed.'])

    def b(name, offset=ZERO):
        return [name, list(offset), 'b']

    add('wave.detector', 6, [b('wave.detector')])
    for lane, direction in zip(LANES, DIRECTIONS):
        name = 'wave.' + lane
        upstream = tuple(-v for v in direction)
        for offset in (upstream, direction):
            add(name, 3, [b(name, offset)])
        add('wave.memory', 2, [b('wave.detector'), b(name, upstream)], True)
        add('wave.response', 3, [b('wave.response', direction)])
    add('wave.response', 3, [b('wave.memory')], True)
    return Tensor.from_dict(data, strict_support=True)
