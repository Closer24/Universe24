"""Finite exact certificates for the clock/gear readout; no evolution additions.

Run from the repository root:
    python -m research.building_blocks.algebra_checks --output NEW_RESULT.json
The sole state-changing forward call is Engine.advance. Default output is stdout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.experiments.config import checkpoint_data

ROOT = Path(__file__).resolve().parents[2]
BASELINE = 'ed1556e202eb0f3cc60342c75d44012c2eeb71c3'
BUDGET_CPU_SECONDS = 60


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def state_data(state):
    return {'side': state.cube.side, 'background': list(state.background),
            'cells': [[*address, *triple] for address, triple in sorted(state.cells.items())]}


def snapshot(state, addresses):
    return {','.join(map(str, address)): list(state.at(address)) for address in addresses}


def checked_step(engine, old, observed, start):
    if time.process_time() - start > BUDGET_CPU_SECONDS:
        raise TimeoutError('Algebra certificate CPU budget exhausted; result is inconclusive')
    inputs = engine.input_sums(old)
    new = engine.advance(old)
    arithmetic = []
    for address in observed:
        prior, nxt = old.at(address), new.at(address)
        u = inputs.get(address, 0)
        ell = nxt.b + prior.a
        theta, epsilon = divmod(prior.r, 2)
        next_theta, next_epsilon = divmod(nxt.r, 2)
        assert 2 * u + prior.r == 6 * ell + nxt.r
        assert u + theta == 3 * ell + next_theta
        assert next_epsilon == epsilon
        assert nxt.a == prior.b and nxt.b == ell - prior.a
        arithmetic.append({'address': list(address), 'old': list(prior), 'u': u,
                           'ell': ell, 'new': list(nxt), 'theta': theta,
                           'theta_next': next_theta, 'epsilon': epsilon})
    assert engine.rewind(new) == old
    return new, arithmetic


def clock_case(side, signs, pairs, start):
    origin = (side // 2, side // 2, side // 2)
    cells = {}
    for j in range(pairs):
        position = (origin[0] + j, *origin[1:])
        cells[(*position, 0)] = Channel(-1, -1, 0)
        cells[(*position, 14)] = Channel(1, 1, 4)
    initial = State(Cube(side), cells=cells)
    engine = Engine(Coupling(signs))
    state = initial
    steps = 20
    trace = []
    addresses = sorted(cells)
    first_return = None
    for t in range(steps + 1):
        row = {'t': t, 'state_sha256': digest(state_data(state)),
               'explicit_cells': len(state.cells), 'observed': snapshot(state, addresses)}
        if t and state == initial and first_return is None:
            first_return = t
        if t < steps:
            state, row['outgoing_update'] = checked_step(engine, state, addresses, start)
        trace.append(row)
    final = state
    for _ in range(steps):
        state = engine.rewind(state)
    assert state == initial
    expected = 4 if pairs == 1 else 5
    assert first_return == expected
    return {'id': f'preloaded_pairs{pairs}_L{side}_signs' + ''.join('p' if s > 0 else 'm' for s in signs),
            'kind': 'preloaded_clock', 'steps': steps, 'expected_first_full_return': expected,
            'observed_first_full_return': first_return, 'acceptance': True,
            'initial': checkpoint_data(initial, engine, 0),
            'final': checkpoint_data(final, engine, steps),
            'one_step_inverses': steps, 'full_rewind_exact': True, 'trace': trace}


def guide_case(source, start):
    side, length, receiver, steps = 151, 24, 6, 60
    origin = (side // 2 - length // 2, side // 2, side // 2)
    cells = {}
    for j in range(1, length + 1):
        cells[(origin[0] + j, *origin[1:], 0)] = Channel(0, 0, 4)
        cells[(origin[0] + j, *origin[1:], 14)] = Channel(0, 0, 0)
    if source:
        cells[(*origin, 0)] = Channel(0, 1, 2)
        cells[(*origin, 14)] = Channel(0, -1, 2)
    initial = State(Cube(side), cells=cells)
    engine = Engine(Coupling((1, 1, 1)))
    addresses = [(origin[0] + receiver, *origin[1:], g) for g in (0, 14)]
    state = initial
    trace = []
    all_stationary = True
    for t in range(steps + 1):
        all_stationary &= state == initial
        row = {'t': t, 'state_sha256': digest(state_data(state)),
               'observed': snapshot(state, addresses)}
        if t < steps:
            state, row['outgoing_update'] = checked_step(engine, state, addresses, start)
        trace.append(row)
    final = state
    for _ in range(steps):
        state = engine.rewind(state)
    assert state == initial
    cycle = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    key0 = ','.join(map(str, addresses[0]))
    end = 2 * (length + 1) - receiver
    if source:
        assert all(tuple(row['observed'][key0][:2]) == cycle[(row['t'] - receiver) % 4]
                   for row in trace if receiver <= row['t'] < end)
        assert trace[receiver - 1]['outgoing_update'][0]['u'] == 1
        assert trace[receiver - 1]['outgoing_update'][0]['ell'] == 1
        assert all(row['outgoing_update'][0]['u'] == 0
                   for row in trace if receiver <= row['t'] < end - 1)
    else:
        assert all_stationary
    return {'id': 'guide_source' if source else 'guide_no_source',
            'kind': 'signal_started_clock_control', 'N': length, 'receiver_j': receiver,
            'origin': list(origin), 'steps': steps, 'source_present': source,
            'whole_state_stationary_for_all_samples': all_stationary,
            'source_case_first_clock_window': [receiver, end] if source else None,
            'window_convention': 'start inclusive, end exclusive',
            'initial': checkpoint_data(initial, engine, 0),
            'final': checkpoint_data(final, engine, steps),
            'one_step_inverses': steps, 'full_rewind_exact': True, 'acceptance': True,
            'trace': trace}


def run():
    start = time.process_time()
    pin_path = ROOT / 'research/reproducibility/base_engine.json'
    pin = json.loads(pin_path.read_text())
    files = sorted((ROOT / 'universe24').rglob('*.py')) + [Path(__file__).resolve(), pin_path]
    source_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    assert pin['engine_commit'] == BASELINE
    assert all(source_hashes[path] == sha for path, sha in pin['source_sha256'].items())
    results = [clock_case(side, signs, pairs, start)
               for side in (5, 7, 11) for signs in ((1, 1, 1), (1, -1, 1)) for pairs in (1, 2)]
    results.extend(guide_case(source, start) for source in (False, True))
    assert time.process_time() - start <= BUDGET_CPU_SECONDS
    return {'protocol': 'U24-CLOCKWORK-ALGEBRA-v1', 'engine_baseline_commit': BASELINE,
            'checkout_commit_at_execution': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'python': platform.python_version(), 'source_sha256': source_hashes,
            'core_hashes_match_pinned_baseline': True,
            'random_seed': None, 'budget_cpu_seconds': BUDGET_CPU_SECONDS,
            'cases': results, 'case_count': len(results),
            'forward_steps': sum(case['steps'] for case in results),
            'all_acceptance': all(case['acceptance'] for case in results),
            'scope': 'Finite exact engine certificates plus separately documented algebraic proofs; no physical identification of light or energy.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, separators=(',', ':')) + '\n'
    if args.output:
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(text)
        print(json.dumps({'cases': result['case_count'], 'forward_steps': result['forward_steps'],
                          'all_acceptance': result['all_acceptance'], 'output': str(args.output)}))
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
