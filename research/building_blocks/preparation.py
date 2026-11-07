"""Initial-state construction and passive readout; no runtime interventions."""
from universe24.core import Coupling, Cube, Engine, State
from universe24.core.state import Channel


def prepare(case):
    side, n = case['side'], case['N']
    origin = (side // 2 - n // 2, side // 2, side // 2)
    if origin[0] < 1 or origin[0] + n >= side - 1:
        raise ValueError('Preparation must not wrap')
    mode = case.get('mode', 'guide')
    if mode not in {'guide', 'no_source', 'source_only', 'gap', 'odd_remainder'}:
        raise ValueError('Unknown preparation mode')
    cells = {}
    x, y, z = origin
    if mode != 'source_only':
        for j in range(1, n + 1):
            if mode == 'gap' and j == case['gap']:
                continue
            cells[(x+j,y,z,0)] = Channel(0,0,4)
            cells[(x+j,y,z,14)] = Channel(0,0,0)
    if mode != 'no_source':
        cells[(x,y,z,0)] = Channel(0,1,2)
        cells[(x,y,z,14)] = Channel(0,-1,2)
    if mode == 'odd_remainder':
        cells[(x+case['perturb_at'],y,z,0)] = Channel(0,0,5)
    engine = Engine(Coupling((1,1,1)))
    return engine, State(Cube(side), Channel(0,0,2), cells), origin


def pair(state, origin, j):
    x,y,z = origin
    return state.at((x+j,y,z,0)), state.at((x+j,y,z,14))


def memory(values):
    """Fixed internal remainder predicate, independent of all prior samples."""
    return int(values[0].r == 0 and values[1].r == 4)
