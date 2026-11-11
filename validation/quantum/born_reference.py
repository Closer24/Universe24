"""Explicit Born-rule benchmark; never supplies outcomes to the Rule3 Engine.

Integer complex amplitudes and exact probabilities are retained. A joint
two-party draw uses BOTH settings and is NOT a local hidden-variable model.
Born's rule is assumed here, not derived from complexity or engine clicks.
"""
from fractions import Fraction
from itertools import product
from random import Random

import numpy as np

from universe24.core import Engine, State, compose
from universe24.core.tensor import Block, GearType
from universe24.layers.choice import build_fibre, build_gated_pair


def norm2(amplitude):
    real, imag = amplitude
    return real*real + imag*imag


def interference(arm_a, arm_b):
    return tuple(tuple(a + sign*b for a, b in zip(arm_a, arm_b)) for sign in (1, -1))


def probabilities(amplitudes):
    weights = tuple(norm2(a) for a in amplitudes)
    total = sum(weights)
    if not total:
        raise ValueError('zero state has no normalized Born probabilities')
    return weights, tuple(Fraction(w, total) for w in weights)


def measure(amplitudes, rng, *, ready):
    """A fresh draw ONLY on measurement; retain the amplitudes and random ticket.

    This is an external reference measurement, not an Engine event or inverse.
    Each ready call denotes a separate prepared trial.
    """
    if not ready:
        return None
    weights, _ = probabilities(amplitudes)
    ticket = rng.randrange(sum(weights))
    cumulative = 0
    for outcome, weight in enumerate(weights):
        cumulative += weight
        if ticket < cumulative:
            return {'outcome': outcome, 'ticket': ticket,
                    'amplitudes': tuple(tuple(a) for a in amplitudes)}
    raise AssertionError('unreachable integer sampling interval')


def singlet_amplitudes(x, y):
    """Unnormalized (A_x tensor B_y)|singlet>, as exact integer complex pairs.

    A0=I, A1=[[1,1],[-1,1]]/sqrt(2).
    B0=[[3,1],[-1,3]]/sqrt(10), B1=[[3,-1],[1,3]]/sqrt(10).
    Common normalization cancels in the Born ratios. No correlations are
    supplied as a lookup table: multiply the coherent signed amplitudes.
    """
    if x not in (0, 1) or y not in (0, 1):
        raise ValueError('binary settings required')
    a = ((1, 0), (0, 1)) if x == 0 else ((1, 1), (-1, 1))
    b = ((3, 1), (-1, 3)) if y == 0 else ((3, -1), (1, 3))
    psi = ((0, 1), (-1, 0))
    return tuple((sum(a[o_a][i]*psi[i][j]*b[o_b][j] for i, j in product((0, 1), repeat=2)), 0)
                 for o_a, o_b in product((0, 1), repeat=2))


def stochastic_local_bound():
    """Exact grid check, plus the continuous bound in BELL_BORN_CONE.md."""
    values = tuple(Fraction(k, 4) for k in range(5))
    maximum = Fraction(0)
    for probabilities_ in product(values, repeat=4):
        a0, a1, b0, b1 = (2*p-1 for p in probabilities_)
        maximum = max(maximum, abs(a0*(b0+b1)+a1*(b0-b1)))
    return {'local_probability_grid': list(map(str, values)), 'models_checked': len(values)**4,
            'maximum_expected_CHSH': str(maximum),
            'interpretation': 'Local stochastic outputs, including any local complexity-to-probability rule, still factor conditionally. Sampling only at measurement does not remove this bound.'}


def quantum_reference(arrival_ticks, samples_per_setting=20000, *, record_sink=None):
    if type(samples_per_setting) is not int or samples_per_setting < 1:
        raise ValueError('positive integer sample count required')
    if len(arrival_ticks) != 2 or any(type(t) is not int or t < 1 for t in arrival_ticks):
        raise ValueError('two actual positive arrival ticks required')
    rng = Random(20261111)
    cells = {}
    signs = (1, -1, -1, 1)
    for x, y in product((0, 1), repeat=2):
        amplitudes = singlet_amplitudes(x, y)
        weights, probs = probabilities(amplitudes)
        before = rng.getstate()
        for tick in range(max(arrival_ticks)):
            assert measure(amplitudes, rng, ready=all(tick >= arrival for arrival in arrival_ticks)) is None
        assert rng.getstate() == before
        counts = [0] * 4
        for _ in range(samples_per_setting):
            record = measure(amplitudes, rng, ready=True)
            assert record['amplitudes'] == amplitudes
            counts[record['outcome']] += 1
            if record_sink is not None:
                record_sink({'settings': [x, y], 'measurement_microtick': max(arrival_ticks),
                             'ticket': record['ticket'], 'outcome': record['outcome']})
        cells[f'{x}{y}'] = {'integer_complex_amplitudes': amplitudes, 'weights': weights,
            'probabilities': list(map(str, probs)), 'E': str(sum(s*p for s, p in zip(signs, probs))),
            'mean_A': str(probs[0]+probs[1]-probs[2]-probs[3]),
            'mean_B': str(probs[0]-probs[1]+probs[2]-probs[3]),
            'sample_counts': counts,
            'sample_E': str(Fraction(sum(s*n for s, n in zip(signs, counts)), samples_per_setting))}
    chsh = lambda key: abs(sum(sign * Fraction(cells[xy][key]) for xy, sign
        in (('00', 1), ('01', 1), ('10', 1), ('11', -1))))
    return {'assumption': 'Born rule imposed as a quantum reference, not derived from Rule3 or complexity.',
            'joint_sampler_uses_both_settings': True, 'feeds_Engine': False,
            'arrival_ticks_from_Engine_control': arrival_ticks,
            'randomness_before_measurement': False, 'rng_seed': 20261111,
            'samples_per_setting': samples_per_setting, 'cells': cells,
            'exact_CHSH': str(chsh('E')), 'sample_CHSH': str(chsh('sample_E')),
            'exact_marginals_nonsignalling': all(c['mean_A'] == c['mean_B'] == '0' for c in cells.values()),
            'all_emissions_included': True}


def router_calibration():
    """Existing quadratic inputs versus actual binary click frequencies.

    Complex packets travel two edges before the local detector reads them.
    Exhaust all 36 residue pairs; count events, never quotient magnitudes.
    """
    names = ('a_re', 'a_im', 'b_re', 'b_im')
    fibre = build_fibre(components=names, name='amp', label='audit')
    marker = Block((GearType('on', 'audit'),),
                   (('on', 6, (('on', (0, 0, 0), 'b'),)),), name='marker')
    router = build_gated_pair(kappa=1, arm1=['amp.a_re', 'amp.a_im'],
                             arm2=['amp.b_re', 'amp.b_im'], gate='marker.on', name='router')
    tensor = compose(fibre, marker, router, strict_support=True)
    engine = Engine(tensor)
    detector_gears = [tensor.gear_index('router.' + n) for n in ('dP', 'dM')]
    cases = []
    for label, a, b in [('same_phase', (1, 0), (1, 0)), ('quarter_turn', (1, 0), (0, 1)),
                        ('opposite_phase', (1, 0), (-1, 0)), ('unequal_arms', (2, 0), (1, 0))]:
        weights, probs = probabilities(interference(a, b))
        counts, c2_counts, double, silent = [0, 0], [0, 0], 0, 0
        amplitude_trace = []
        for r0, r1 in product(range(6), repeat=2):
            seed = State(9, *[np.zeros((tensor.G, 9**3), dtype=np.int64) for _ in range(3)])
            target = seed.lattice.index(4, 4, 4)
            marker_g = tensor.gear_index('marker.on')
            seed.a[marker_g, target] = seed.b[marker_g, target] = 1
            for components, amplitude, site, direction in (
                    (names[:2], a, (2, 4, 4), (1, 0, 0)),
                    (names[2:], b, (6, 4, 4), (-1, 0, 0))):
                for name, value in zip(components, amplitude):
                    g = tensor.gear_index('amp.' + name)
                    seed.b[g, seed.lattice.index(*site)] = value
                    seed.a[g] = seed.b[g, seed.lattice.shift_index(direction)]
            seed.r[detector_gears[0], target], seed.r[detector_gears[1], target] = r0, r1
            state = seed
            for tick in range(1, 4):
                if tick == 3:
                    assert tuple(int(engine.inputs(state)[g, target]) for g in detector_gears) == weights
                after = engine.step(state)
                events = engine.clicks(state, after, tick).select('official')
                if tick < 3:
                    assert len(events.node) == 0
                if (r0, r1) == (0, 0):
                    amplitude_trace.append({'microtick': tick,
                        'arm_a': [int(after.b[tensor.gear_index('amp.' + n), target]) for n in names[:2]],
                        'arm_b': [int(after.b[tensor.gear_index('amp.' + n), target]) for n in names[2:]]})
                state = after
            hits = [False, False]
            for g, n, kind in zip(events.gear, events.node, events.kind):
                if n == target and g in detector_gears:
                    side = detector_gears.index(g)
                    hits[side] = True
                    counts[side] += 1
                    c2_counts[side] += int(kind == 2)
            double += int(all(hits))
            silent += int(not any(hits))
            for _ in range(3):
                state = engine.inverse_step(state)
            assert state.same_as(seed)
        cases.append({'case': label, 'arm_a': a, 'arm_b': b, 'quadratic_inputs': weights,
            'Born_reference_probabilities': list(map(str, probs)), 'trials': 36,
            'actual_clicks': counts, 'actual_C2_clicks': c2_counts,
            'click_probability_per_emission': [str(Fraction(n, 36)) for n in counts],
            'share_of_all_clicks': [str(Fraction(n, sum(counts))) for n in counts],
            'double_click_trials': double, 'no_click_trials': silent, 'all_rewinds_exact': True,
            'no_early_detector_clicks': True, 'amplitude_trace': amplitude_trace})
    return {'tensor_fingerprint': tensor.fingerprint, 'G': tensor.G, 'cases': cases,
            'amplitude_arrival_microtick': 2, 'detector_readout_microtick': 3,
            'strict_support_violations': 0,
            'Born_click_law_derived': False,
            'meaning': 'The existing square polynomial yields interference intensities; actual binary Rule3 click counts are not generally normalized Born probabilities.'}
