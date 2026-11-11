"""Bounded organization across periodic carrier cycles; not cosmology.

Frozen grid: L=3,5,7, six L-step cycles, coherent/no-write/no-read/scaled/
scrambled/noisy-memory controls. This delayed memory has finite structural
capacity: recurrent positive writes can subsequently grow amplitudes only.
"""
import argparse
from fractions import Fraction
from functools import reduce
import gzip
import hashlib
import json
from math import gcd
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import DIRECTIONS

LANES = ('px', 'nx', 'py', 'ny', 'pz', 'nz')
MEM = ('memory.X', 'memory.Y', 'memory.Z')
ZERO = (0, 0, 0)
PLUS, MINUS = (1, 0, 0), (-1, 0, 0)
VARIANTS = ('coherent', 'no_write', 'no_read', 'scaled', 'scrambled', 'noisy_memory')


def build(write=True, read=True):
    names = ['carrier.'+lane for lane in LANES] + list(MEM) + ['response']
    terms = []
    def add(target, c, *factors):
        terms.append((target, c, factors))
    def f(name, offset=ZERO, field='b'):
        return (name, offset, field)
    for lane, direction in zip(LANES, DIRECTIONS):
        g = 'carrier.'+lane
        add(g, 3, f(g, direction))
        add(g, 3, f(g, tuple(-v for v in direction)))
    for target, source, offset in (
        (MEM[0], MEM[1], ZERO), (MEM[0], MEM[2], PLUS),
        (MEM[1], MEM[2], ZERO), (MEM[1], MEM[0], ZERO),
        (MEM[2], MEM[0], MINUS), (MEM[2], MEM[1], ZERO)):
        add(target, 3, f(source, offset))
    if write:
        for i in range(0, 6, 2):
            a, b = ('carrier.'+LANES[j] for j in (i, i+1))
            add(MEM[0], 3, f(a), f(b))
            add(MEM[1], -3, f(a, field='a'), f(b, field='a'))
    if read:
        for lane in LANES:
            add('response', 3, f(MEM[0]), f('carrier.'+lane))
    return Tensor(names, terms, strict_support=True)


def collision(state, field):
    values = getattr(state, field)
    return sum(values[i]*values[i+1] for i in (0, 2, 4))


def prepare(tensor, L, variant):
    b = np.zeros((tensor.G, L**3), dtype=object)
    a = b.copy()
    seed = State(L, a, b, np.full(b.shape, 2, dtype=object))
    rng = np.random.default_rng(20261111+L)
    center = (L//2,)*3
    amplitude = 2 if variant == 'scaled' else 1
    for i, direction in enumerate(DIRECTIONS):
        site = tuple(map(int, rng.integers(0, L, size=3))) if variant == 'scrambled' else center
        seed.b[i, seed.lattice.index(*site)] = amplitude
        seed.a[i] = seed.b[i, seed.lattice.shift_index(direction)]
    if variant == 'noisy_memory':
        # Declared reproducible unstructured initial memory, no encoded word.
        for g in (6, 7, 8):
            draw = rng.integers(0, 20, size=L**3)
            seed.b[g] = np.where(draw == 0, -1, np.where(draw == 1, 1, 0))
    seed.a[6] = seed.b[8, seed.lattice.shift_index(PLUS)]
    seed.a[7] = seed.b[6] - (collision(seed, 'a') if variant != 'no_write' else 0)
    seed.a[8] = seed.b[7]
    return seed


def digest(state):
    return hashlib.sha256(json.dumps(state.to_dict(), sort_keys=True).encode()).hexdigest()


def primitive(values):
    flat = list(map(int, np.asarray(values).flat))
    scale = reduce(gcd, map(abs, flat), 0) or 1
    return hashlib.sha256(json.dumps([v//scale for v in flat]).encode()).hexdigest()


def structure(state):
    signs = np.sign(state.b[6:9]).astype(np.int8)
    patterns = [tuple(map(int, v)) for v in signs.T]
    sites = {p for p in patterns if any(p)}
    edges = set()
    for direction in DIRECTIONS[::2]:
        for n, neighbor in enumerate(state.lattice.shift_index(direction)):
            p, q = patterns[n], patterns[int(neighbor)]
            if any(p) or any(q):
                edges.add(p+q)
    weight = np.sum(np.abs(state.b[:6]), axis=0)
    mass = int(sum(weight))
    ball = weight.copy()
    for direction in DIRECTIONS:
        ball += weight[state.lattice.shift_index(direction)]
    return {'carrier_focus': str(Fraction(int(max(ball)), mass)) if mass else '0',
        'memory_occupied_cells': int(np.count_nonzero(state.b[6:9])),
        'memory_occupied_sites': int(np.count_nonzero(np.any(signs, axis=0))),
        'memory_site_types': len(sites), 'memory_edge_types': len(edges),
        'memory_primitive_fingerprint': primitive(state.b[6:9]),
        'memory_mass': int(np.sum(np.abs(state.b[6:9]))),
        'response_occupied_sites': int(np.count_nonzero(state.b[9])),
        'response_primitive_fingerprint': primitive(state.b[9]),
        'maximum_bits': state.max_abs().bit_length()}


def run_case(out, L, variant):
    tensor = build(write=variant != 'no_write', read=variant != 'no_read')
    seed = prepare(tensor, L, variant)
    state = seed
    engine = Engine(tensor)
    case_dir = out/f'L{L}-{variant}'
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir/'tensor.json').write_text(json.dumps(tensor.to_dict(), indent=2)+'\n')
    (case_dir/'seed.json').write_text(json.dumps(seed.to_dict())+'\n')
    rows, snapshots = [], {}
    seen = {digest(seed): 0}
    recurrence = None
    previous_signs = []
    retained_between_writes = True
    click_classes = {str(kind): 0 for kind in range(3)}
    with gzip.open(case_dir/'trace.jsonl.gz', 'wt') as trace:
        for tick in range(6*L+1):
            trace.write(json.dumps({'tick': tick, 'state': state.to_dict()})+'\n')
            row = structure(state)
            signs = np.sign(state.b[6:9]).astype(np.int8)
            previous_signs.append(signs.copy())
            persistent = np.zeros(state.N, dtype=bool)
            if len(previous_signs) >= 3:
                persistent = np.any(signs != 0, axis=0)
                for prev in previous_signs[-3:-1]:
                    persistent &= np.all(prev == signs, axis=0)
            row.update(microtick=tick, macrocycle=tick//L if tick % L == 0 else None,
                persistent_site_types=len({tuple(map(int, p)) for p in signs[:, persistent].T}))
            rows.append(row)
            if tick % L == 0:
                snapshots[tick//L] = state.copy()
            if tick == 6*L or row['maximum_bits'] > 128:
                break
            before = state
            state = engine.step(before)
            assert np.array_equal(state.r, before.r)
            events = engine.clicks(before, state, tick+1)
            for kind in range(3):
                click_classes[str(kind)] += int(np.count_nonzero(events.kind == kind))
            # Independent prepared-sector oracle for the three-bank memory.
            expected = np.stack([before.b[7], before.b[8],
                before.b[6, before.lattice.shift_index(MINUS)]]).astype(object)
            j = collision(before, 'b') if variant != 'no_write' else np.zeros(before.N, dtype=object)
            expected[0] += j
            assert np.array_equal(state.b[6:9], expected)
            if not np.any(j):
                retained_between_writes &= sorted(map(int, state.b[6:9].flat)) == sorted(map(int, before.b[6:9].flat))
            assert engine.inverse_step(state).same_as(before)
            h = digest(state)
            if h in seen and recurrence is None:
                recurrence = {'first': seen[h], 'return': tick+1}
            seen[h] = tick+1
    assert engine.rewind(state, rows[-1]['microtick']).same_as(seed)
    (case_dir/'final.json').write_text(json.dumps(state.to_dict())+'\n')
    report = {'L': L, 'variant': variant, 'updates': rows[-1]['microtick'],
        'tensor_fingerprint': tensor.fingerprint, 'gears': tensor.G, 'terms': len(tensor),
        'support_violations': len(tensor.support_violations()), 'full_state_recurrence': recurrence,
        'exact_rewind': True, 'memory_transport_oracle_matches': True,
        'click_classes': click_classes, 'remainders_unchanged': True,
        'memory_values_permuted_between_writes': retained_between_writes,
        'rows': rows, 'seed_sha256': digest(seed), 'final_sha256': digest(state),
        'tensor_sha256': hashlib.sha256((case_dir/'tensor.json').read_bytes()).hexdigest(),
        'trace_sha256': hashlib.sha256((case_dir/'trace.jsonl.gz').read_bytes()).hexdigest()}
    (case_dir/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report, snapshots


def memory_counterfactual(out, L, snapshots):
    """Two complete new preparations, same law/carriers/response, different memory.

    Declared follow-up: compare memory at macrocycles 1 and 2, for every L.
    No field is edited once either new trajectory begins.
    """
    tensor = build()
    engine = Engine(tensor)
    early = snapshots[1].copy()
    later_memory = early.copy()
    for field in ('a', 'b', 'r'):
        getattr(later_memory, field)[6:9] = getattr(snapshots[2], field)[6:9]
    seeds = [early, later_memory]
    states = [s.copy() for s in seeds]
    path = out/f'L{L}-memory-intervention'
    path.mkdir(parents=True, exist_ok=True)
    (path/'tensor.json').write_text(json.dumps(tensor.to_dict())+'\n')
    (path/'seeds.json').write_text(json.dumps([s.to_dict() for s in seeds])+'\n')
    differing_ticks = []
    with gzip.open(path/'trace.jsonl.gz', 'wt') as trace:
        for tick in range(L+1):
            trace.write(json.dumps({'tick': tick, 'states': [s.to_dict() for s in states]})+'\n')
            assert all(np.array_equal(getattr(states[0], f)[:6], getattr(states[1], f)[:6]) for f in ('a','b','r'))
            if any(not np.array_equal(getattr(states[0], f)[9], getattr(states[1], f)[9]) for f in ('a','b','r')):
                differing_ticks.append(tick)
            if tick < L:
                states = [engine.step(s) for s in states]
    assert all(engine.rewind(s, L).same_as(seed) for s, seed in zip(states, seeds))
    (path/'finals.json').write_text(json.dumps([s.to_dict() for s in states])+'\n')
    return {'L': L, 'only_memory_differs_initially': True,
        'same_tensor': tensor.fingerprint, 'response_difference_microticks': differing_ticks,
        'carrier_histories_still_identical': True, 'exact_rewinds': True,
        'seed_sha256': [digest(s) for s in seeds], 'final_sha256': [digest(s) for s in states],
        'trace_sha256': hashlib.sha256((path/'trace.jsonl.gz').read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'runs/complexity-research/04-organization')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    reports, controls, interventions = [], [], []
    for L in (3, 5, 7):
        cases = {}
        for variant in VARIANTS:
            report, snapshots = run_case(args.out, L, variant)
            reports.append(report)
            cases[variant] = snapshots
        coherent = cases['coherent']
        interventions.append(memory_counterfactual(args.out, L, coherent))
        for cycle, state in coherent.items():
            if cycle == 0:
                continue
            no_write, no_read, scaled = (cases[key][cycle] for key in ('no_write', 'no_read', 'scaled'))
            assert np.array_equal(state.b[:6], no_write.b[:6])
            assert np.array_equal(state.b[:9], no_read.b[:9])
            assert np.array_equal(scaled.b[6:9], 4*state.b[6:9])
            assert np.array_equal(scaled.b[9], 8*state.b[9])
            controls.append({'L': L, 'macrocycle': cycle,
                'carrier_return_exact': all(np.array_equal(getattr(state, f)[:6], getattr(coherent[0], f)[:6]) for f in ('a','b','r')),
                'memory_affects_response': not np.array_equal(state.b[9], no_read.b[9]),
                'source_write_affects_memory': not np.array_equal(state.b[6:9], no_write.b[6:9]),
                'memory_changes_later_carrier_cycles': False,
                'scaled_memory_factor': 4, 'scaled_response_factor': 8})
    result = {'baseline': '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
        'hypothesis': 'Slow retained transport can preserve spatial traces across fast macrocycles; finite three-phase capacity is not open-ended organization.',
        'frozen_grid': {'L':[3,5,7], 'cycles':6, 'variants':VARIANTS, 'bit_stop':128},
        'all_original_protocol_gates_pass': False,
        'failures': ['No memory-to-carrier feedback; carrier cycles are prescribed periodic control.',
                     'Three-phase memory saturates; later integer growth alone is not organization.',
                     'No local stagnation sensor, Born law or physical cosmological claim.'],
        'cases': reports, 'paired_controls': controls, 'same_law_memory_interventions': interventions,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.out/'report.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'cases':len(reports), 'rewinds':sum(r['exact_rewind'] for r in reports),
        'macrocycle_controls':len(controls), 'original_protocol_success':False}, indent=2))


if __name__ == '__main__':
    main()
