"""Bounded prepared-front family and complete-state translation search.

Only initial states and the eight existing fixed tensors vary. Observers are
passive. All scientific criteria are registered in signal_protocol.json.
"""
from __future__ import annotations
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import sys
import time

from universe24.core import Coupling, Cube, Engine, State

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = Path(__file__).with_name('signal_protocol.json')
SIGNS = tuple(product((-1, 1), repeat=3))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def state_data(state):
    return {'side': state.cube.side, 'background': list(state.background),
            'cells': [[*address, *triple] for address, triple in sorted(state.cells.items())]}


def state_digest(state):
    return hashlib.sha256(canonical(state_data(state))).hexdigest()


def guide(n, signs=(1, 1, 1), source_ab=(0, 1), mode='guide', side=151,
          origin=(60, 75, 75)):
    """Complete deterministic initial-state generator; no later injection."""
    x, y, z = origin
    cells = {}
    if mode != 'no_guide':
        for j in range(1, n + 1):
            if mode == 'gap' and j == 3:
                continue
            cells[(x+j, y, z, 0)] = (0, 0, 4)
            cells[(x+j, y, z, 14)] = (0, 0, 0)
    if mode != 'no_source':
        a, b = source_ab
        cells[(x, y, z, 0)] = (a, b, 2)
        cells[(x, y, z, 14)] = (-a, -b, 2)
    return Engine(Coupling(tuple(signs))), State(Cube(side), cells=cells)


def compact_seed(motif, signs):
    addr = (30, 30, 30)
    if motif.startswith('single_b'):
        cells = {(*addr, 0): (0, int(motif[-1]), 2)}
    elif motif.startswith('opposite_b'):
        b = int(motif[-1])
        cells = {(*addr, 0): (0, b, 2), (*addr, 14): (0, -b, 2)}
    elif motif == 'clock_pair':
        cells = {(*addr, 0): (-1, -1, 0), (*addr, 14): (1, 1, 4)}
    else:
        raise ValueError(motif)
    return Engine(Coupling(tuple(signs))), State(Cube(61), cells=cells)


def translated(state, shift):
    L = state.cube.side
    return State(state.cube, state.background,
                 {((x+shift[0]) % L, (y+shift[1]) % L, (z+shift[2]) % L, g): v
                  for (x, y, z, g), v in state.cells.items()})


class BudgetExceeded(RuntimeError):
    pass


def check_budget(start, state):
    if time.process_time()-start > 120:
        raise BudgetExceeded('120 CPU seconds exceeded')
    if len(state.cells) > 20000:
        raise BudgetExceeded('20000 sparse stored channels exceeded')


def run_guide(n, signs, ab, mode, start):
    engine, initial = guide(n, signs, ab, mode)
    state = initial
    x, y, z = (60, 75, 75)
    steps = n + 12
    arrivals = [None]*n
    records = {str(j): [] for j in (6, 12)}
    clicks = {str(j): [] for j in (6, 12)}
    peak = len(state.cells)
    hashes = []
    for t in range(steps+1):
        check_budget(start, state)
        hashes.append(state_digest(state))
        for j in range(1, n+1):
            if arrivals[j-1] is None and state.at((x+j, y, z, 0)).b != 0:
                arrivals[j-1] = t
        for j in (6, 12):
            values = state.at((x+j, y, z, 0)), state.at((x+j, y, z, 14))
            bit = int((values[0].r, values[1].r) == (0, 4))
            record = records[str(j)]
            if record and bit and not record[-1]:
                clicks[str(j)].append(t)
            record.append(bit)
        if t < steps:
            next_state = engine.advance(state)
            check_budget(start, next_state)
            if engine.rewind(next_state) != state:
                raise AssertionError(('step inverse', signs, n, ab, mode, t))
            state = next_state
            peak = max(peak, len(state.cells))
    final_digest = state_digest(state)
    for _ in range(steps):
        check_budget(start, state)
        state = engine.rewind(state)
    if state != initial:
        raise AssertionError(('full inverse', signs, n, ab, mode))
    delay = next((d for d in (0, 1) if arrivals == [j+d for j in range(1, n+1)]), None)
    return {'id': f'{mode}_N{n}_{"".join("p" if s == 1 else "m" for s in signs)}_a{ab[0]}b{ab[1]}',
            'generator': {'function': 'guide', 'n': n, 'signs': list(signs),
                          'source_ab': list(ab), 'mode': mode, 'side': 151,
                          'origin': [60, 75, 75]},
            'steps': steps, 'coupling_fingerprint': engine.coupling.fingerprint,
            'first_arrivals': arrivals, 'unit_speed_delay': delay,
            'unit_speed_all_receivers': delay is not None,
            'memory_bits': records, 'click_times': clicks,
            'initial_sha256': state_digest(initial), 'final_sha256': final_digest,
            'trace_sha256': hashlib.sha256(canonical(hashes)).hexdigest(),
            'peak_stored_channels': peak, 'step_inverse_all': True, 'full_rewind': True}


def run_compact(motif, signs, start):
    engine, initial = compact_seed(motif, signs)
    state = initial
    shifts = tuple(tuple(amount if axis == index else 0 for index in range(3))
                   for axis in range(3) for amount in (-2, -1, 1, 2))
    goals = [(shift, translated(initial, shift)) for shift in shifts]
    hits = []
    returns = []
    hashes = [state_digest(initial)]
    peak = len(state.cells)
    for t in range(1, 13):
        check_budget(start, state)
        new = engine.advance(state)
        check_budget(start, new)
        if engine.rewind(new) != state:
            raise AssertionError(('compact inverse', motif, signs, t))
        state = new
        peak = max(peak, len(state.cells))
        hashes.append(state_digest(state))
        if state == initial:
            returns.append(t)
        if len(state.cells) == len(initial.cells):
            for shift, goal in goals:
                if state == goal:
                    hits.append({'step': t, 'shift': list(shift)})
    final_digest = state_digest(state)
    for _ in range(12):
        check_budget(start, state)
        state = engine.rewind(state)
    if state != initial:
        raise AssertionError(('compact full inverse', motif, signs))
    return {'motif': motif, 'signs': list(signs), 'side': 61, 'origin': [30, 30, 30],
            'steps': 12, 'coupling_fingerprint': engine.coupling.fingerprint,
            'initial_state': state_data(initial), 'initial_sha256': state_digest(initial),
            'final_sha256': final_digest,
            'trace_sha256': hashlib.sha256(canonical(hashes)).hexdigest(),
            'translation_certificates': hits, 'return_times': returns,
            'peak_stored_channels': peak, 'step_inverse_all': True, 'full_rewind': True}


def study():
    protocol = json.loads(PROTOCOL_PATH.read_text())
    started = time.process_time()
    result = {'protocol_id': protocol['protocol_id'],
              'protocol_sha256': hashlib.sha256(PROTOCOL_PATH.read_bytes()).hexdigest(),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'engine_baseline': protocol['engine_baseline'],
              'engine_source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in sorted((ROOT/'universe24').rglob('*.py'))},
              'python': platform.python_version(), 'random_seed': None,
              'guide_cases': [], 'compact_cases': [], 'execution_status': 'completed',
              'budget_exceeded_at': None}
    case = None
    try:
        for n, signs, ab in product(protocol['guide']['lengths'], SIGNS,
                                   protocol['guide']['source_ab']):
            case = ['guide', n, list(signs), ab]
            result['guide_cases'].append(run_guide(n, signs, tuple(ab), 'guide', started))
        for signs, mode in product(SIGNS, ('no_source', 'no_guide', 'gap')):
            case = [mode, 24, list(signs), [0, 1]]
            result['guide_cases'].append(run_guide(24, signs, (0, 1), mode, started))
        for signs, motif in product(SIGNS, protocol['compact_search']['motifs']):
            case = ['compact', motif, list(signs)]
            result['compact_cases'].append(run_compact(motif, signs, started))
    except BudgetExceeded as exc:
        result['execution_status'] = 'inconclusive_budget'
        result['budget_exceeded_at'] = {'case': case, 'reason': str(exc)}
    result['summary'] = {
        'completed_guide_cases': len(result['guide_cases']),
        'unit_speed_guide_cases': sum(c['unit_speed_all_receivers'] for c in result['guide_cases']
                                     if c['generator']['mode'] == 'guide'),
        'completed_compact_cases': len(result['compact_cases']),
        'nonzero_shift_certificates': sum(len(c['translation_certificates']) for c in result['compact_cases']),
        'all_completed_full_rewinds': all(c['full_rewind'] for c in result['guide_cases']+result['compact_cases']),
        'physical_light_established': False,
    }
    result['runtime_cpu_seconds'] = time.process_time()-started
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path,
                        help='New JSON output path; existing evidence is never overwritten.')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output exists; choose a new path')
    result = study()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'status': result['execution_status'], 'summary': result['summary'],
                      'cpu_seconds': result['runtime_cpu_seconds']}, indent=2))
    return 0 if result['execution_status'] == 'completed' else 2


if __name__ == '__main__':
    sys.exit(main())
