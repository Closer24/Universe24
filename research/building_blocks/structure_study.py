"""Bounded prepared-structure study using unchanged Rule3 and passive readouts.

Run from repository root:
  python -m research.building_blocks.structure_study --output runs/structures.json
An existing result is never overwritten. The registered protocol is immutable
input. All physical terminology is kept separate from computational acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import subprocess
import time

from universe24.core import Coupling, Cube, Engine, State
from universe24.experiments.config import checkpoint_data

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = Path(__file__).with_name('structure_protocol.json')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest_state(state):
    return hashlib.sha256(canonical({
        'side': state.cube.side, 'background': state.background,
        'cells': [[*address, *triple] for address, triple in sorted(state.cells.items())]
    })).hexdigest()


def put_pair(cells, position, pair):
    for channel, triple in zip((0, 14), pair):
        cells[(*position, channel)] = tuple(triple)


def project(state, positions):
    return [[list(state.at((*position, channel))) for channel in (0, 14)]
            for position in positions]


def check_budget(start, state, protocol):
    if time.process_time() - start > protocol['budget']['cpu_seconds']:
        raise TimeoutError('Registered CPU budget exhausted; result is inconclusive')
    if len(state.cells) > protocol['budget']['max_sparse_channels']:
        raise TimeoutError('Registered sparse-support budget exhausted; result is inconclusive')


def run_case(name, state, signs, positions, protocol, start):
    engine = Engine(Coupling(tuple(signs)))
    initial = state
    snapshots = [state]
    trace = []
    all_inverse = True
    for t in range(protocol['steps'] + 1):
        check_budget(start, state, protocol)
        coordinates = [v for addr in state.cells for v in addr[:3]]
        trace.append({
            't': t, 'state_sha256': digest_state(state),
            'sparse_channels': len(state.cells), 'target_pairs': project(state, positions),
            'minimum_active_boundary_distance': min(
                (min(v, state.cube.side - 1 - v) for v in coordinates), default=state.cube.side),
        })
        if t == protocol['steps']:
            break
        next_state = engine.advance(state)
        all_inverse = all_inverse and engine.rewind(next_state) == state
        state = next_state
        snapshots.append(state)
    restored = state
    for _ in range(protocol['steps']):
        restored = engine.rewind(restored)
    targets = set(positions)
    first_return = next((t for t in range(1, 13) if snapshots[t] == initial), None)
    localized = all(addr[:3] in targets for s in snapshots for addr in s.cells)
    first_activity = []
    memory_clicks = []
    for position in positions:
        first_activity.append(next((t for t, s in enumerate(snapshots)
                                    if any(s.at((*position, g)).a or s.at((*position, g)).b
                                           for g in (0, 14))), None))
        memory = [s.at((*position, 0)).r == 0 and s.at((*position, 14)).r == 4
                  for s in snapshots]
        memory_clicks.append([t for t in range(1, len(memory)) if memory[t] and not memory[t - 1]])
    result = {
        'case': name, 'signs': list(signs), 'coupling_fingerprint': engine.coupling.fingerprint,
        'initial': checkpoint_data(initial, engine, 0),
        'final': checkpoint_data(state, engine, protocol['steps']),
        'target_positions': [list(p) for p in positions],
        'first_full_state_return_through_12': first_return,
        'localized_to_target_sites_all_40_steps': localized,
        'first_target_counter_activity': first_activity,
        'memory_rising_edges': memory_clicks,
        'exact_one_step_inverses': all_inverse,
        'exact_full_rewind': restored == initial,
        'trace': trace,
    }
    assert all_inverse and restored == initial, name
    return result, snapshots


def run(protocol):
    start = time.process_time()
    side = protocol['side']
    origin = tuple(protocol['motif_origin'])
    pair = [protocol['clock_pair']['channel_0'], protocol['clock_pair']['channel_14']]
    all_results = []
    baseline_trajectories = {}
    for signs in product((-1, 1), repeat=3):
        cells = {}
        put_pair(cells, origin, pair)
        isolated, isolated_states = run_case(
            'isolated_' + ''.join('p' if x > 0 else 'm' for x in signs),
            State(Cube(side), cells=cells), signs, [origin], protocol, start)
        baseline_trajectories[signs] = isolated_states
        # Retain all baselines: source-independent clock evidence is explicit.
        all_results.append(isolated)
    for signs in product((-1, 1), repeat=3):
        separations = protocol['separations'] if signs == (1, 1, 1) else [1]
        for separation in separations:
            positions = [origin, (origin[0] + separation, origin[1], origin[2])]
            cells = {}
            for position in positions:
                put_pair(cells, position, pair)
            result, states = run_case(
                f'pair_{"".join("p" if x > 0 else "m" for x in signs)}_d{separation}',
                State(Cube(side), cells=cells), signs, positions, protocol, start)
            isolated = baseline_trajectories[signs]
            interaction_times = [t for t in range(len(states))
                                 if any(states[t].at((*position, g)) != isolated[t].at((*origin, g))
                                        for position in positions for g in (0, 14))]
            result['first_local_difference_from_isolated_copy'] = next(iter(interaction_times), None)
            result['operational_bound_motif'] = bool(
                result['first_full_state_return_through_12'] is not None
                and result['localized_to_target_sites_all_40_steps'] and interaction_times)
            all_results.append(result)
    signal = protocol['signal_preparation']
    source = tuple(signal['source'])
    targets = [(source[0] + j, source[1], source[2]) for j in signal['target_x_offsets']]
    comparisons = []
    for variant in signal['target_variants']:
        trajectories = {}
        case_results = {}
        for source_present in signal['source_controls']:
            cells = {}
            for j in signal['guide_x_offsets']:
                put_pair(cells, (source[0] + j, source[1], source[2]), signal['guide_pair'])
            for position in targets:
                put_pair(cells, position, pair if variant == 'preloaded_clock_pair' else signal['guide_pair'])
            if source_present:
                put_pair(cells, source, signal['source_pair'])
            result, states = run_case(
                f'signal_{variant}_{"on" if source_present else "off"}',
                State(Cube(side), cells=cells), (1, 1, 1), targets, protocol, start)
            result['target_period5_t16_through_t35'] = all(
                project(states[t], targets) == project(states[t + 5], targets) for t in range(16, 31))
            result['target_counters_inactive_all_steps'] = all(
                all(s.at((*position, g)).a == 0 and s.at((*position, g)).b == 0
                    for position in targets for g in (0, 14)) for s in states)
            trajectories[source_present] = states
            case_results[source_present] = result
            all_results.append(result)
        on, off = trajectories[True], trajectories[False]
        difference = next((t for t in range(len(on)) if project(on[t], targets) != project(off[t], targets)), None)
        comparisons.append({
            'target_variant': variant,
            'first_source_caused_target_difference': difference,
            'source_absent_inactive': case_results[False]['target_counters_inactive_all_steps'],
            'source_present_postarrival_period5': case_results[True]['target_period5_t16_through_t35'],
            'created_source_driven_localized_period5_structure': bool(
                case_results[False]['target_counters_inactive_all_steps']
                and difference is not None
                and case_results[True]['target_period5_t16_through_t35']
                and case_results[True]['localized_to_target_sites_all_40_steps']),
            'attachment_or_breakup_certified': False,
        })
    return {'execution_status': 'completed', 'case_count': len(all_results),
            'cases': all_results, 'source_comparisons': comparisons,
            'all_full_inverses_pass': all(r['exact_one_step_inverses'] and r['exact_full_rewind'] for r in all_results),
            'cpu_seconds': time.process_time() - start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f'Refusing to overwrite evidence: {args.output}')
    protocol = json.loads(PROTOCOL.read_text())
    source_paths = sorted((ROOT / 'universe24').rglob('*.py')) + [Path(__file__).resolve(), PROTOCOL]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    metadata = {
        'protocol_id': protocol['protocol_id'], 'engine_baseline': protocol['engine_baseline'],
        'source_sha256': hashes, 'python': platform.python_version(),
        'checkout_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'working_tree_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT)),
        'protocol': protocol,
    }
    try:
        result = run(protocol)
    except TimeoutError as error:
        result = {'execution_status': 'inconclusive', 'reason': str(error)}
    result.update(metadata)
    assert hashes == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'output': str(args.output), 'execution_status': result['execution_status'],
                      'case_count': result.get('case_count'), 'source_comparisons': result.get('source_comparisons')}, indent=2))
    if result['execution_status'] != 'completed':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
