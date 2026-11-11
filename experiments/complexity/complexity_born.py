"""Predeclared phase-clock correlation and complexity-to-Born experiment.

See docs/research/complexity/05-born.md. Experimental tensor only: never
modifies production evolution or feeds external probabilities into Engine.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine, State, compose
from universe24.core.tensor import Block, GearType

BASELINE = '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2'
PHASES = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
KERNEL = (2, 1, -1, -2, -1, 1)
METRICS = ('histories', 'distinct_histories', 'persistent_pairs')
O = (0, 0, 0)


def amplitude(phases):
    return tuple(sum(PHASES[p % 6][i] for p in phases) for i in (0, 1))


def norm2(z):
    x, y = z
    return x*x+x*y+y*y


def contrast(phases):
    doubled = sum(KERNEL[(a-b) % 6] for a, b in product(phases, repeat=2))
    assert doubled >= 0 and doubled % 2 == 0
    return doubled//2


def branch(phases):
    return {'phases': list(phases), 'amplitude': amplitude(phases),
        'q': norm2(amplitude(phases)), 'pair_contrast': contrast(phases),
        'histories': len(phases), 'distinct_histories': len(set(phases)),
        'persistent_pairs': len(phases)**2}


def normalized(weights):
    total = sum(weights)
    if total <= 0:
        raise ValueError('positive total required')
    return tuple(Fraction(w, total) for w in weights)


def tv(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))/2


def summarize_grid(branches):
    summaries = {}
    modes = [('direct', metric, None) for metric in (*METRICS, 'pair_contrast')]
    modes += [('postweight', metric, lam) for metric in METRICS
              for lam in (Fraction(0), Fraction(1, 4), Fraction(1))]
    for mode, metric, lam in modes:
        checked = mismatches = 0
        maximum = Fraction(0)
        witness = None
        for left, right in product(branches, repeat=2):
            q = (left['q'], right['q'])
            if not sum(q):
                continue
            reference = normalized(q)
            weights = tuple(c[metric] for c in (left, right)) if mode == 'direct' else tuple(
                c['q']*(1+lam*c[metric]) for c in (left, right))
            actual = normalized(weights)
            error = tv(reference, actual)
            checked += 1
            mismatches += int(error != 0)
            if error > maximum:
                maximum = error
                witness = {'branches': [left, right], 'reference': list(map(str, reference)),
                           'candidate': list(map(str, actual)), 'TV': str(error)}
        key = f'{mode}:{metric}' + (f':lambda={lam}' if lam is not None else '')
        summaries[key] = {'pairs_checked': checked, 'mismatches': mismatches,
            'maximum_TV': str(maximum), 'witness': witness}
    return summaries


def phase_clock_tensor(number):
    names = [(f'x{h}', f'y{h}') for h in range(number)]
    gears = [GearType(name, 'audit') for pair in names for name in pair]
    gears.append(GearType('detector', 'official'))
    terms = [(name, 3, ((name, O, 'b'),)) for pair in names for name in pair]
    why = {'designated_one_way': 'experimental local phase-pair observer; no feedback or external probability'}
    def pair_term(coefficient, a, b):
        terms.append(('detector', coefficient, ((a, O, 'b'), (b, O, 'b')), why))
    for h, (x, y) in enumerate(names):
        pair_term(1, x, x)
        pair_term(1, x, y)
        pair_term(1, y, y)
        for X, Y in names[h+1:]:
            pair_term(2, x, X)
            pair_term(1, x, Y)
            pair_term(1, y, X)
            pair_term(2, y, Y)
    return compose(Block(tuple(gears), tuple(terms), name='phase'), strict_support=True)


def engine_check(branches):
    engines = {n: Engine(phase_clock_tensor(n)) for n in (1, 2, 3)}
    rows = []
    for branch_ in branches:
        phases = branch_['phases']
        engine = engines[len(phases)]
        tensor = engine.tensor
        detector = tensor.gear_index('phase.detector')
        hits = 0
        quotients = []
        for r in range(6):
            seed = State(3, *[np.zeros((tensor.G, 27), dtype=np.int64) for _ in range(3)])
            for h, phase in enumerate(phases):
                x, y = PHASES[phase]
                gx, gy = [tensor.gear_index(f'phase.{c}{h}') for c in ('x', 'y')]
                seed.b[gx, 0], seed.b[gy, 0] = x, y
                seed.a[gx, 0], seed.a[gy, 0] = x+y, -x
            seed.r[detector, 0] = r
            assert int(engine.inputs(seed)[detector, 0]) == branch_['q'] == branch_['pair_contrast']
            after = engine.step(seed)
            events = engine.clicks(seed, after).select('official')
            observed = any(int(g) == detector and int(n) == 0 for g, n in zip(events.gear, events.node))
            q = (2*branch_['q']+r)//6
            assert observed == (q != 0)
            hits += int(observed)
            quotients.append(q)
            assert engine.inverse_step(after).same_as(seed)
            state = seed
            for tick in range(1, 7):
                state = engine.step(state)
                for h, phase in enumerate(phases):
                    expected = PHASES[(phase+tick) % 6]
                    for c, value in zip(('x', 'y'), expected):
                        assert int(state.b[tensor.gear_index(f'phase.{c}{h}'), 0]) == value
            assert engine.rewind(state, 6).same_as(seed)
        assert Fraction(hits, 6) == min(Fraction(1), Fraction(branch_['q'], 3))
        rows.append({'phases': phases, 'input_q': branch_['q'], 'events_per_6_remainders': hits,
                     'quotients': quotients})
    return {'preparations': len(branches)*6, 'first_step_input_identity': True,
        'every_clock_six_step_orbit_verified': True, 'all_first_and_six_step_rewinds_exact': True,
        'tensor_fingerprints': {n: e.tensor.fingerprint for n, e in engines.items()},
        'actual_detector_law': 'min(1,q/3) over six equally weighted initial detector remainders',
        'Born_sampling_derived': False, 'rows': rows}


def history_controls():
    rows = []
    for phases, velocities, label in [((0, 0), (1, 1), 'locked_equal'),
            ((0, 3), (1, 1), 'locked_antiphase'), ((0, 0), (0, 1), 'relative_drift'),
            ((0, 2, 4), (1, 1, 1), 'locked_canceling_triad')]:
        histories = [tuple((p+v*t) % 6 for t in range(6)) for p, v in zip(phases, velocities)]
        contrasts = [contrast([history[t] for history in histories]) for t in range(6)]
        q = [norm2(amplitude([history[t] for history in histories])) for t in range(6)]
        assert contrasts == q
        persistent = sum(len({(h[t]-k[t]) % 6 for t in range(6)}) == 1
                         for h, k in product(histories, repeat=2))
        rows.append({'case': label, 'histories': histories, 'persistent_unsigned_pairs': persistent,
            'instantaneous_q': q, 'time_averaged_pair_contrast': str(Fraction(sum(contrasts), 6))})
    base, expanded = branch((0,)), branch((0, 1, 4))
    assert base['q'] == expanded['q'] == 1
    reference = normalized((base['q'], base['q']))
    weights = [c['q']*(1+c['histories']) for c in (expanded, base)]
    post = normalized(weights)
    return {'time_histories': rows, 'canceling_pair_addition': {'before': base, 'after': expanded,
        'encoding_condition': 'Same coarse amplitude state only if extra clock histories are representational rather than an independently measurable change in source/apparatus.',
        'fixed_q_reference': list(map(str, reference)), 'postweighted_history_probability': list(map(str, post)),
        'TV': str(tv(reference, post))}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/complexity-research/05-born'))
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    branches = [branch(p) for n in (1, 2, 3) for p in combinations_with_replacement(range(6), n)]
    assert len(branches) == 83 and all(b['q'] == b['pair_contrast'] for b in branches)
    rotated = scaled = 0
    for b in branches:
        for shift in range(6):
            assert contrast([(p+shift) % 6 for p in b['phases']]) == b['q']
            rotated += 1
        for multiple in (2, 3):
            assert contrast(b['phases']*multiple) == multiple**2*b['q']
            scaled += 1
    root = Path(__file__).resolve().parents[2]
    source_paths = ['experiments/complexity/complexity_born.py', 'docs/research/complexity/05-born.md',
                    'universe24/core/engine.py', 'universe24/core/tensor.py']
    report = {'main_baseline': BASELINE, 'scope': 'Experimental local clock intensity plus analytical probability comparisons; no feedback into production Engine.',
        'kernel_predeclared': KERNEL, 'branch_count': len(branches),
        'branch_pairs_total': len(branches)**2,
        'excluded_zero_total_intensity_pairs': sum(a['q']+b['q'] == 0 for a, b in product(branches, repeat=2)),
        'global_phase_controls': rotated, 'uniform_history_duplication_controls': scaled,
        'branches': branches, 'grid': summarize_grid(branches), 'controls': history_controls(),
        'engine': engine_check(branches), 'signed_pair_identity_derived': True,
        'Born_probability_rule_derived': False, 'Bell_violation_claimed': False,
        'source_sha256': {p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in source_paths}}
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'branches': len(branches), 'grid': {k: {x:v[x] for x in ('pairs_checked','mismatches','maximum_TV')} for k,v in report['grid'].items()},
        'engine_preparations': report['engine']['preparations'], 'controls': report['controls']}, indent=2))


if __name__ == '__main__':
    main()
