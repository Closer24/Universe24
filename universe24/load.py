"""Passive exact load diagnostics; never an input to the evolution rule.

Three different quantities are deliberately reported separately: a fixed
scalar evaluation schedule, representation-dependent integer magnitudes, and
the model's dynamical occupation/traffic. None is calibrated stress-energy,
proper time, a CPU benchmark or a physical particle classification.
"""
from __future__ import annotations

from math import gcd

import numpy as np

from .core import State, Tensor


def _exact_values(values, *, shape=None, nonnegative=False):
    array = np.asarray(values, dtype=object)
    if shape is not None and array.shape != shape:
        raise ValueError(f'expected complete array of shape {shape}')
    if any(isinstance(value, (bool, np.bool_)) or
           not isinstance(value, (int, np.integer)) for value in array.flat):
        raise ValueError('load diagnostics require exact integers')
    array = np.asarray([int(value) for value in array.flat], dtype=object).reshape(array.shape)
    if nonnegative and any(value < 0 for value in array.flat):
        raise ValueError('distribution weights must be nonnegative')
    return array


def _ratio(numerator, denominator):
    common = gcd(numerator, denominator)
    return {'num': numerator // common, 'den': denominator // common}


def distribution_profile(values):
    """Exact concentration of a complete nonnegative node-load vector.

    Participation is (sum q)^2/sum(q^2), equal to the number of occupied
    nodes for equal nonzero weights. Normalized concentration is its reciprocal
    times the lattice node count: one for a nonempty uniform distribution and
    N for one occupied node. For the empty vector of weights both ratios use
    the explicit reporting convention zero; ``empty`` distinguishes it.

    The profile is invariant under node permutations and positive integer
    rescaling, apart from the dimensional totals, mean and variance. A packet
    merely translating cannot be misreported as becoming more evenly spread.
    """
    weights = _exact_values(values, nonnegative=True)
    if weights.ndim != 1 or weights.size == 0:
        raise ValueError('supply at least one complete node weight')
    rows = list(weights)
    nodes = len(rows)
    total = sum(rows)
    squares = sum(value * value for value in rows)
    return {
        'nodes': nodes,
        'total': total,
        'sum_squares': squares,
        'maximum': max(rows),
        'support_nodes': sum(value != 0 for value in rows),
        'empty': total == 0,
        'mean': _ratio(total, nodes),
        'variance': _ratio(nodes * squares - total * total, nodes * nodes),
        'participation': _ratio(total * total, squares) if squares else _ratio(0, 1),
        'normalized_concentration': _ratio(nodes * squares, total * total) if total else _ratio(0, 1),
    }


def compare_distributions(before, after):
    """Compare conserved-load spreading, retaining the null and failure cases.

    Greater participation/lower concentration supports a finite-time spreading
    statement only when the same total load is retained. It proves neither
    mixing nor monotonic balancing of every trajectory of a reversible system.
    """
    left = _exact_values(before, nonnegative=True)
    right = _exact_values(after, shape=left.shape, nonnegative=True)
    a, b = distribution_profile(left), distribution_profile(right)
    conserved = a['total'] == b['total']
    reduction = a['sum_squares'] - b['sum_squares'] if conserved else None
    return {
        'before': a,
        'after': b,
        'total_conserved': conserved,
        'node_load_l1_change': sum(abs(x - y) for x, y in zip(left, right)),
        'sum_squares_reduction': reduction,
        'more_even_at_equal_total': conserved and reduction > 0,
        'unchanged_concentration_at_equal_total': conserved and reduction == 0,
        'support_change': b['support_nodes'] - a['support_nodes'],
        'interpretation': 'finite-time occupation distribution; no monotonic or thermodynamic claim',
    }


def integer_work_profile(state, tensor):
    """A fixed canonical scalar schedule and exact retained bit lengths.

    This counts one coefficient-first multiplication for every monomial
    factor and one accumulation per monomial, independently of zero values.
    Vectorization, common reads and hardware can execute a different number
    of machine instructions. Magnitude bits use max(1,abs(value).bit_length()),
    excluding sign and object overhead. Int64 arrays still allocate fixed-width
    words for small values: these counts are not allocated memory. They are not a measured CPU duration,
    minimal information content, physical energy or a permitted load controller.
    """
    if not isinstance(state, State) or not isinstance(tensor, Tensor):
        raise TypeError('a complete State and Tensor are required')
    if state.G != tensor.G:
        raise ValueError('state and tensor channel counts disagree')
    schedule = {
        'monomial_evaluations': len(tensor.monomials),
        'factor_reads': sum(len(term.factors) for term in tensor.monomials),
        'integer_multiplications': sum(len(term.factors) for term in tensor.monomials),
        'term_accumulations': len(tensor.monomials),
        'rule3_divmod_calls': tensor.G,
        'rule3_doublings': tensor.G,
        'rule3_additions': tensor.G,
        'rule3_history_subtractions': tensor.G,
    }
    bit_sum = [0] * state.N
    bit_max = [0] * state.N
    negative_entries = [0] * state.N
    for bank in (state.a, state.b, state.r):
        for channel in bank:
            for node, raw in enumerate(channel):
                value = int(raw)
                bits = max(1, abs(value).bit_length())
                bit_sum[node] += bits
                bit_max[node] = max(bit_max[node], bits)
                negative_entries[node] += value < 0
    return {
        'schema': 'universe24/integer-work-profile/1',
        'nodes': state.N,
        'channels_per_node': state.G,
        'retained_integers_per_node': 3 * state.G,
        'canonical_scalar_schedule_per_node': schedule,
        'canonical_scalar_schedule_total': {key: value * state.N for key, value in schedule.items()},
        'magnitude_bits_sum_by_node': bit_sum,
        'magnitude_bits_max_by_node': bit_max,
        'negative_entries_by_node': negative_entries,
        'representation_dependent': True,
        'feeds_engine': False,
        'interpretation': 'fixed symbolic work and minimal magnitude bits, not allocated memory, CPU timing or stress-energy',
    }


def face_load_profile(values, L):
    """Read anonymous occupation and current edge capacity without evolving it.

    Each of the 48 channels has unit Boolean capacity, grouped into six faces.
    A quartet with three occupied slots is blocked by the collision gate. A
    full quartet is separately marked saturated; its unchanged word cannot
    identify individual carriers. ``held_occupation`` includes both cases.
    ``moving_occupation`` counts occupied slots in the open edge stage, before
    the subsequent onsite face permutation. These are readouts of one snapshot,
    not newly retained state or a physical particle classification.
    """
    from .core.lattice import DIRECTIONS
    from .model import decode_occupation, edge_quartets, frames

    bits = decode_occupation(values, L)
    directions = frames()
    face_index = [DIRECTIONS.index(direction) for direction in directions]
    names = ('occupation', 'available_capacity', 'held_occupation', 'moving_occupation')
    faces = [{'face': face, 'direction': list(direction), 'capacity_per_node': 8,
              **{name: [0] * (L**3) for name in names}}
             for face, direction in enumerate(DIRECTIONS)]
    for channel in range(48):
        face = faces[face_index[channel]]
        for node, raw in enumerate(bits[channel]):
            value = int(raw)
            face['occupation'][node] += value
            face['available_capacity'][node] += 1 - value
    histogram = [0] * 5
    for quartet in edge_quartets(L):
        load = sum(int(bits[channel, node]) for channel, node in quartet)
        histogram[load] += 1
        destination = 'held_occupation' if load >= 3 else 'moving_occupation'
        for channel, node in quartet:
            faces[face_index[channel]][destination][node] += int(bits[channel, node])
    per_node = {name: [sum(face[name][node] for face in faces) for node in range(L**3)]
                for name in names}
    return {
        'schema': 'universe24/face-load-profile/2',
        'nodes': L**3,
        'capacity_per_node': 48,
        'per_node': per_node,
        'per_face': faces,
        'totals': {name: sum(column) for name, column in per_node.items()},
        'edge_load_histogram': histogram,
        'blocked_quartets': histogram[3],
        'saturated_quartets': histogram[4],
        'distribution': distribution_profile(per_node['occupation']),
        'interpretation': 'anonymous occupied slots and edge capacity, not CPU cost, mass or dark matter',
        'feeds_engine': False,
    }


def transition_load_profile(before, after):
    """Audit exact node continuity against the capacity gate's edge current.

    Each edge quartet has two slots at each endpoint. If its total occupation
    is below three, every occupied slot crosses the edge; otherwise its word
    is unchanged. Thus the left-to-right net current is q_left-q_right for an
    open quartet and zero for a blocked/saturated one. The onsite permutation
    redistributes directions but preserves the node's total occupation.

    This is a passive current calculation, not an Engine update or a claim
    that each identifiable particle has a measured trajectory. Complete-state
    replay is the separate authority for the supplied transition.
    """
    from .model import decode_occupation, edge_quartets

    if not isinstance(before, State) or not isinstance(after, State):
        raise TypeError('complete before and after State objects are required')
    if before.L != after.L or before.G != after.G:
        raise ValueError('states have different lattice/channel dimensions')
    bits = decode_occupation(before.b, before.L)
    a = face_load_profile(before.b, before.L)
    b = face_load_profile(after.b, after.L)
    incoming = [0] * before.N
    outgoing = [0] * before.N
    for quartet in edge_quartets(before.L):
        word = [int(bits[channel, node]) for channel, node in quartet]
        if sum(word) >= 3:
            continue
        left, right = quartet[0][1], quartet[1][1]
        if quartet[2][1] != left or quartet[3][1] != right or left == right:
            raise ValueError('edge quartet does not alternate two neighboring endpoints')
        q_left, q_right = word[0] + word[2], word[1] + word[3]
        outgoing[left] += q_left
        incoming[right] += q_left
        outgoing[right] += q_right
        incoming[left] += q_right
    residual = [b['per_node']['occupation'][node] - a['per_node']['occupation'][node]
                - incoming[node] + outgoing[node] for node in range(before.N)]
    changed = ((before.a != after.a) | (before.b != after.b) | (before.r != after.r))
    return {
        'schema': 'universe24/transition-load-profile/2',
        'incoming_occupied_slots_by_node': incoming,
        'outgoing_occupied_slots_by_node': outgoing,
        'held_occupation_by_node': a['per_node']['held_occupation'],
        'changed_channel_triples_by_node': [int(value) for value in changed.sum(axis=0)],
        'node_continuity_residuals': residual,
        'node_continuity_passed': not any(residual),
        'distribution_change': compare_distributions(a['per_node']['occupation'], b['per_node']['occupation']),
        'interpretation': 'edge current and changed retained triples, not particle identities or CPU timing',
        'feeds_engine': False,
    }
