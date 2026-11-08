"""Independent sparse gather oracle derived from exact reference matrices.

No production State, Engine, Coupling, Rule3 or classifier is imported here.
The stationary background completes every omitted address. The support closure
includes every possible recipient of a nonzero old counter before gathering all
six donors. Every other address stays at its stationary background exactly.
"""
from functools import lru_cache
from research.reference.algebra import coupling, DIRECTIONS


@lru_cache(maxsize=8)
def routing(signs):
    graph = coupling(signs)
    inverse = tuple(tuple(row.index(g) for g in range(48)) for row in graph.ports)
    return graph, inverse


def input_at(old, address, side, signs=(1, 1, 1), component=1):
    graph, _ = routing(tuple(signs))
    x, y, z, g = address
    return sum(graph.weights[d][g] * old.get(
        ((x + dx) % side, (y + dy) % side, (z + dz) % side, graph.ports[d][g]),
        (0, 0, 2))[component] for d, (dx, dy, dz) in enumerate(DIRECTIONS))


def step(old, side, background=(0, 0, 2), signs=(1, 1, 1), reverse=False):
    if background[:2] != (0, 0):
        raise ValueError('The sparse oracle requires a stationary background')
    graph, inverse = routing(tuple(signs))
    component = 0 if reverse else 1
    candidates = set(old)
    for (x, y, z, g), v in old.items():
        if v[component]:
            candidates.update(((x - dx) % side, (y - dy) % side, (z - dz) % side,
                               inverse[d][g]) for d, (dx, dy, dz) in enumerate(DIRECTIONS))
    result = {}
    for address in candidates:
        a, b, r = old.get(address, background)
        u = input_at(old, address, side, signs, component)
        if reverse:
            old_r = (r - 2 * u) % 6
            new = ((2 * u + old_r - r) // 6 - b, a, old_r)
        else:
            numerator = 2 * u + r
            ell = numerator // 6
            new = (b, ell - a, numerator - 6 * ell)
        if new != background:
            result[address] = new
    return result


def click(before, after):
    """Independent read-only arithmetic C classification, not path selection."""
    ell = after[1] + before[0]
    if before[2] % 2 != after[2] % 2:
        raise ValueError('Remainder parity changed')
    return None if not ell or before == after else ((after[2] - before[2]) // 2) % 3
