"""Declare the complete causal-wave seed before the first update."""
from universe24.core import State
from universe24.core.lattice import DIRECTIONS
from universe24.layers.causal_wave import LANES, NAMES


def prepare_causal_wave(state, tensor, *, packets, detectors):
    """Replace only the nine wave gears; all other (a,b,r) stay exact.

    Packets are (lane, canonical xyz, Python integer). Duplicate packets add.
    Prepared a_lane(x)=b_lane(x+d) is necessary for exact directed transport.
    Detector addresses are a static local seed, not runtime activation times.
    """
    if state.G != tensor.G:
        raise ValueError('state and tensor gear counts differ')
    indices = [tensor.gear_index(name) for name in NAMES]
    a, b, r = (v.astype(object).copy() for v in (state.a, state.b, state.r))
    for array in (a, b, r):
        array[indices] = 0
    r[tensor.gear_index('wave.memory')] = 2

    def address(xyz):
        xyz = tuple(xyz)
        if len(xyz) != 3 or any(type(v) is not int or not 0 <= v < state.L for v in xyz):
            raise ValueError('coordinates must be three canonical lattice integers')
        return state.lattice.index(*xyz)

    for lane, xyz, payload in packets:
        if lane not in LANES:
            raise ValueError('unknown wave lane')
        if type(payload) is not int:
            raise TypeError('packet payload must be an exact Python int')
        b[tensor.gear_index('wave.' + lane), address(xyz)] += payload
    for lane, direction in zip(LANES, DIRECTIONS):
        gear = tensor.gear_index('wave.' + lane)
        a[gear] = b[gear, state.lattice.shift_index(direction)]
    detector = tensor.gear_index('wave.detector')
    for xyz in detectors:
        a[detector, address(xyz)] = b[detector, address(xyz)] = 1
    return State(state.L, a, b, r)


def default_causal_wave(state, tensor):
    info = default_wave_info(state.L)
    source, target = tuple(info['source']), tuple(info['detector'])
    seed = prepare_causal_wave(state, tensor, packets=[('px', source, 1)], detectors=[target])
    return seed, info


def default_wave_info(L):
    if type(L) is not int or L < 3:
        raise ValueError('causal-wave demonstration requires L >= 3')
    source = [0, L // 2, L // 2]
    target = [L // 2, source[1], source[2]]
    previous = [L - 1, source[1], source[2]]
    return {'source': source, 'detector': target, 'lane': 'px',
            'payload': 1, 'initial_support': [source, previous],
            'first_arrival_microtick': L // 2}
