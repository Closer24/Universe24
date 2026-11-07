"""Independent review of fresh competition trials and batch source coherence."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import time

from .audit import (Snapshot, audit_checkpoints, coupling_fingerprint, digest_file,
                    from_checkpoint, transition_events)

PAIRS = {'O': (4, 0), 'N': (2, 2), 'R': (0, 4)}


def initial(case):
    center = (case['side']//2,)*3
    cells = {}
    for side, pattern in zip((-1, 1), case['patterns']):
        if case.get('isolated_side') is not None and side != case['isolated_side']:
            continue
        for j in range(1, case['arm_length']+1):
            pair = PAIRS[pattern[j-2]] if j in (2, 3) else (4, 0)
            for g, r in zip((0, 14), pair):
                cells[(center[0]+side*j, center[1], center[2], g)] = (0, 0, r)
    a, b = case['phase'] if case['source_present'] else (0, 0)
    cells[(*center, 0)] = (a, b, 2)
    cells[(*center, 14)] = (-a, -b, 2)
    return Snapshot(case['side'], (0, 0, 2), cells)


def observation(states, side, case):
    center = (case['side']//2,)*3
    pos = (center[0]+side*case['arm_length'], center[1], center[2])
    addresses = [(*pos, g) for g in range(48)]
    base = [states[0].at(a) for a in addresses]
    arrival = [None]*3
    active, quiet = False, True
    events, banks, rtimes = [], [], []
    for step, state in enumerate(states):
        vals = [state.at(a) for a in addresses]
        changed = vals != base
        b_changed = any(v[1] != b[1] for v, b in zip(vals, base))
        if step:
            if changed and arrival[0] is None:
                arrival[0] = step
            if b_changed and arrival[1] is None:
                arrival[1] = step
            derived = transition_events(states[step-1], state, addresses)
            if derived['remainder']:
                rtimes.append(step)
            if derived['arithmetic']:
                banks.append(step)
                if arrival[2] is None:
                    arrival[2] = step
                for e in derived['arithmetic']:
                    a = e['address']
                    events.append({'step': step, 'address': list(a), 'kind': e['kind'],
                                   'quotient': e['quotient'],
                                   'before': list(states[step-1].at(a)),
                                   'after': list(state.at(a))})
        if case['window'][0] <= step <= case['window'][1]:
            active |= b_changed
            quiet &= not changed
    has_c = any(case['window'][0] <= t <= case['window'][1] for t in banks)
    return {'arrival_tuple': arrival, 'b_transmission': active, 'strong_quiet': quiet,
            'C_events': events, 'C_bank_times': banks, 'remainder_change_times': rtimes,
            'position': list(pos), 'C_in_window': has_c, 'functional': active and has_c}


def review(evidence, output):
    evidence, output = Path(evidence), Path(output)
    start = time.process_time()
    result = json.loads((evidence/'result.json').read_text())
    protocol = json.loads((evidence/'protocol.json').read_text())
    assert digest_file(evidence/'protocol.json') == result['protocol_sha256']
    batch = json.loads((evidence/'source_manifest.json').read_text())
    for path, value in batch.items():
        assert digest_file(evidence/'source'/path) == value, path
    specs = {row['case']['id']: row for row in json.loads((evidence/'candidate_manifest.json').read_text())}
    assert set(result['cases']) == set(specs)
    observations, stationary, versions, oracle_replays = {}, {}, set(), []
    all_frames = 0
    primary_ids = set()
    for length in (8, 10):
        primary_ids.update(f'l{length}-joint-p0-{left}-{right}' for left, right in (('OR', 'NO'), ('NO', 'OR')))
        primary_ids.update(f'l{length}-null-{left}-{right}' for left, right in (('OR', 'NO'), ('NO', 'OR')))
        primary_ids.update(f'l{length}-iso-p0-{side}-{pattern}' for side in ('L', 'R') for pattern in ('OR', 'NO'))
    for identifier, files in result['cases'].items():
        if time.process_time()-start > 120:
            raise TimeoutError('Independent followup readback CPU budget exceeded')
        folder = evidence/'cases'/identifier
        analysis = json.loads((folder/'analysis.json').read_text())
        runner = json.loads((folder/'result.json').read_text())
        spec = json.loads((folder/'spec.json').read_text())
        case = analysis['case']
        assert case == specs[identifier]['case'] and spec == specs[identifier]['spec']
        spec_hash = hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()
        assert spec_hash == runner['spec_sha256'] == analysis['spec_sha256']
        hashes = runner['source_sha256']
        versions.add(json.dumps(hashes, sort_keys=True))
        assert all(batch.get(path) == value for path, value in hashes.items()), identifier
        trace = folder/'states.jsonl.gz'
        assert digest_file(trace) == files['trace_sha256'] == analysis['trace_sha256']
        native = [json.loads(line) for line in gzip.decompress(trace.read_bytes()).decode().splitlines()]
        states = [from_checkpoint(record) for record in native]
        expected = initial(case)
        assert states[0] == expected and len(states) == case['steps']+1
        for index, record in enumerate(native):
            assert record['completed_steps'] == index
            assert record['coupling_fingerprint'] == coupling_fingerprint((1, 1, 1))
            assert tuple(record['experiment']['coupling_signs']) == (1, 1, 1)
        margin = min(min(c, case['side']-1-c) for a in expected.cells for c in a[:3])
        assert margin == analysis['initial_boundary_margin'] and margin > case['steps']
        stationary[identifier] = all(state == expected for state in states)
        assert stationary[identifier] == analysis['entire_board_stationary']
        observations[identifier] = {str(s): observation(states, s, case) for s in (-1, 1)}
        assert observations[identifier] == analysis['outlets'], identifier
        bundle = json.loads((folder/'experiments.json').read_text())
        assert digest_file(folder/'experiments.json') == analysis['portable_bundle_sha256']
        experiment = bundle['experiments'][0]
        assert len(bundle['experiments']) == 1 and experiment['id'] == identifier
        assert experiment['provenance']['component_source_sha256'] == hashes
        assert experiment['provenance']['research_provenance']['protocol_sha256'] == result['protocol_sha256']
        assert len(experiment['frames']) == len(states)
        for frame, state in zip(experiment['frames'], states):
            cells = {}
            for row in frame['cells']:
                address = tuple(row[:4])
                assert address not in cells
                for value in row[4:6]:
                    assert type(value) is str and str(int(value)) == value
                cells[address] = (int(row[4]), int(row[5]), row[6])
            assert Snapshot(experiment['side'], tuple(int(v) for v in experiment['background']), cells) == state
        all_frames += len(states)
        if identifier in primary_ids:
            oracle_replays.append(audit_checkpoints(trace, expected_initial=expected, expected_signs=(1, 1, 1)))
    assert len(versions) == 1
    consistent = {}
    for row in result['verdict']['comparisons']:
        length, phase = row['arm_length'], row['phase_index']
        left, right = row['patterns']
        out = observations[row['id']]
        isolated = [observations[f'l{length}-iso-p{phase}-L-{left}']['-1'],
                    observations[f'l{length}-iso-p{phase}-R-{right}']['1']]
        both = all(v['functional'] for v in isolated)
        winners = [s for s in (-1, 1) if out[str(s)]['functional'] and out[str(-s)]['strong_quiet']]
        unique = winners[0] if len(winners) == 1 else None
        winning_pattern = (left if unique == -1 else right) if unique is not None else None
        assert row['both_isolated_functional'] == both
        assert row['isolated_arrival_tuples'] == [v['arrival_tuple'] for v in isolated]
        assert row['matched_arrivals'] == (isolated[0]['arrival_tuple'] == isolated[1]['arrival_tuple'])
        assert row['unique_side'] == unique and row['winning_pattern'] == winning_pattern
        assert row['competitive'] == (both and unique is not None)
        if left != right:
            consistent.setdefault((length, phase), []).append((both and unique is not None, winning_pattern))
    supported = {length: {} for length in (8, 10)}
    for (length, phase), values in consistent.items():
        if len(values) == 2 and all(v[0] for v in values) and len({v[1] for v in values}) == 1:
            supported[length][phase] = values[0][1]
    inputs = protocol['preparation']['ordered_inputs']
    cross = None
    for length in (8, 10):
        assert supported[length][0] == 'OR'
        assert all(stationary[f'l{length}-null-{a}-{b}'] for a, b in protocol['preparation']['all_joint_pairs'])
        declared = result['verdict']['input_response'][str(length)]
        assert declared['consistent_competitive_inputs'] == {str(k): v for k, v in supported[length].items()}
        flips = set()
        for i, j in itertools.combinations(sorted(supported[length]), 2):
            if supported[length][i] != supported[length][j]:
                same = sum(v*v for v in inputs[i]) == sum(v*v for v in inputs[j])
                flips.add(((i, j), (supported[length][i], supported[length][j]), same))
        assert len(flips) == len(declared['flips'])
        cross = flips if cross is None else cross & flips
    assert not cross and not result['summary']['input_controlled_flip_passed']
    assert not result['summary']['phase_controlled_flip_passed']
    assert result['summary']['primary_passed'] is True
    report = {'format': 'universe24-independent-selection-followup-review-v1', 'passed': True,
        'runs_observed_independently': len(observations), 'native_and_portable_frames_checked': all_frames,
        'joint_classifications_checked': len(result['verdict']['comparisons']),
        'distinct_runner_source_versions': len(versions), 'all_run_sources_match_frozen_batch': True,
        'source_snapshot_files_verified': len(batch), 'all_specs_match_pre_run_manifest': True,
        'primary_fresh_competition_passed': True, 'input_controlled_flip_found': False,
        'phase_controlled_flip_found': False, 'higher_cooperation_preference_claim': False,
        'full_oracle_replayed_runs': len(oracle_replays),
        'full_oracle_replayed_transitions': sum(r['transitions'] for r in oracle_replays),
        'supported_inputs_by_length': supported, 'full_replays': oracle_replays,
        'cpu_seconds': time.process_time()-start, 'evidence_result_sha256': digest_file(evidence/'result.json'),
        'source_sha256': {str(p): digest_file(p) for p in (Path(__file__), Path(__file__).with_name('audit.py'))},
        'scope': 'Finite OR/NO competition confirmed at the preregistered input(0,1), fresh lengths8/10, both spatial swaps and isolated/null controls. The failed higher-score prediction and original all-phase gate remain failed/closed; no autonomous waiting receiver is established.'}
    with output.open('x') as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write('\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = review(args.evidence, args.output)
    print(json.dumps({k: v for k, v in report.items() if k not in ('full_replays', 'source_sha256')}))
