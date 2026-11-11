"""Passive snapshots of the optional wave, including complete memory triples."""
import numpy as np
from universe24.layers.causal_wave import LANES


def wave_frame(state, tensor, tick, clicks=None, *, namespace='wave'):
    lanes = [tensor.gear_index(namespace + '.' + lane) for lane in LANES]
    memory = tensor.gear_index(namespace + '.memory')
    response = tensor.gear_index(namespace + '.response')
    detector = tensor.gear_index(namespace + '.detector')
    events = [] if clicks is None else [
        [int(g), int(n), int(k)] for g, n, k in zip(clicks.gear, clicks.node, clicks.kind)
        if int(g) in lanes + [memory, response]]
    return {'microtick': tick, 'clicks': events, 'nodes': [
        {'grid': list(state.lattice.coords(n)),
         'packets_hex': [format(int(state.b[g, n]), 'x') for g in lanes],
         'memory_hex': [format(int(v[memory, n]), 'x') for v in (state.a, state.b, state.r)],
         'response_hex': format(int(state.b[response, n]), 'x'),
         'detector': bool(state.b[detector, n])} for n in range(state.N)]}


def changed_sites(before, after):
    """Support of a full-state difference, including old history and residue."""
    return set(map(int, np.flatnonzero(np.any(
        (before.a != after.a) | (before.b != after.b) | (before.r != after.r), axis=0))))


def inside_cone(lattice, node, initial_support, elapsed):
    """Conservative periodic face-edge cone, not a metric-null geodesic."""
    xyz = lattice.coords(node)
    return any(sum(min(abs(a-b), lattice.L-abs(a-b)) for a, b in zip(xyz, origin)) <= elapsed
               for origin in initial_support)
