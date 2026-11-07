"""Independent readback of every registered selection score and comparison.

All outlet observations are recomputed from full saved states. A bounded subset
also receives an independent exact-matrix forward/inverse replay. The study's
observer and decision functions are deliberately not imported.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import time

from .audit import (Snapshot, audit_checkpoints, coupling_fingerprint, digest_file,
                    from_checkpoint, transition_events)

PAIR_VALUES = {'O': (4, 0), 'N': (2, 2), 'R': (0, 4)}


def declared_initial(case):
    center = (case['side']//2,)*3
    cells = {}
    for side, pattern in zip((-1, 1), case['patterns']):
        if case.get('isolated_side') is not None and side != case['isolated_side']:
            continue
        for j in range(1, 7):
            values = PAIR_VALUES[pattern[j-2]] if j in (2, 3) else (4, 0)
            if j in case['perturb_sites']:
                r0 = (values[0]+2) % 6
                values = (r0, 4-r0)
            for channel, r in zip((0, 14), values):
                cells[(center[0]+side*j, center[1], center[2], channel)] = (0, 0, r)
    a, b = case['phase'] if case['source_present'] else (0, 0)
    cells[(*center, 0)] = (a, b, 2)
    cells[(*center, 14)] = (-a, -b, 2)
    return Snapshot(case['side'], (0, 0, 2), cells)


def observe(states, side, case):
    center = (case['side']//2,)*3
    position = (center[0]+6*side, center[1], center[2])
    addresses = [(*position, g) for g in range(48)]
    base = [states[0].at(a) for a in addresses]
    first_full = first_b = first_c = None
    events, banks, rtimes, vector = [], [], [], []
    transmitted, quiet = False, True
    for step, state in enumerate(states):
        values = [state.at(a) for a in addresses]
        changed = values != base
        active_b = any(v[1] != b[1] for v, b in zip(values, base))
        if step:
            if changed and first_full is None:
                first_full = step
            if active_b and first_b is None:
                first_b = step
            derived = transition_events(states[step-1], state, addresses)
            if derived['remainder']:
                rtimes.append(step)
            if derived['arithmetic']:
                banks.append(step)
                if first_c is None:
                    first_c = step
                for event in derived['arithmetic']:
                    address = event['address']
                    events.append({'step': step, 'address': list(address),
                        'kind': event['kind'], 'quotient': event['quotient'],
                        'before': list(states[step-1].at(address)),
                        'after': list(state.at(address))})
        if case['window'][0] <= step <= case['window'][1]:
            transmitted |= active_b
            quiet &= not changed
        if 6 <= step <= 15:
            vector.extend(v[1] for v in values)
    c_in_window = any(case['window'][0] <= t <= case['window'][1] for t in banks)
    return {'position': list(position), 'baseline': [list(v) for v in base],
            'first_full_change': first_full, 'first_b': first_b, 'first_C': first_c,
            'arrival_tuple': [first_full, first_b, first_c],
            'C_events': events, 'C_bank_times': banks, 'C_in_window': c_in_window,
            'b_transmission': transmitted, 'strong_quiet': quiet,
            'functional': transmitted and c_in_window,
            'calibration_vector': vector, 'remainder_change_times': rtimes}


def review(evidence, output):
    started = time.process_time()
    evidence, output = Path(evidence), Path(output)
    result = json.loads((evidence/'result.json').read_text())
    protocol = json.loads((evidence/'protocol.json').read_text())
    manifest = json.loads((evidence/'source_manifest.json').read_text())
    for path, value in manifest['sources'].items():
        assert digest_file(evidence/'source'/path) == value, path
    assert digest_file(evidence/'protocol.json') == result['protocol_sha256']
    scores_saved = json.loads((evidence/'calibration_scores.json').read_text())
    assert digest_file(evidence/'calibration_scores.json') == result['calibration_scores_sha256']
    patterns = protocol['family']['ordered_patterns']
    observations, cases, audit_paths = {}, {}, []
    eligible_ids = {row['id'] for row in result['comparisons'] if row['primary_eligible']}
    selected_ids = eligible_ids | {'joint-p0-OO-RR', 'joint-p0-RR-OO', 'null-OO-RR',
        'iso-p0-L-OO-base', 'iso-p0-R-RR-base', 'iso-p0-L-RR-base', 'iso-p0-R-OO-base',
        'iso-p0-L-OO-i', 'iso-p0-L-OO-j', 'iso-p0-L-OO-ij'}
    frames = 0
    for identifier, files in result['cases'].items():
        if time.process_time()-started > 120:
            raise TimeoutError('Independent selection readback CPU budget exceeded')
        folder = evidence/'cases'/identifier
        stored = json.loads((folder/'result.json').read_text())
        assert digest_file(folder/'result.json') == files['result_sha256']
        trace_path = folder/'states.jsonl.gz'
        assert digest_file(trace_path) == files['trace_sha256'] == stored['trace_sha256']
        lines = gzip.decompress(trace_path.read_bytes()).decode().splitlines()
        records = [json.loads(line) for line in lines]
        assert [hashlib.sha256(line.encode()).hexdigest() for line in lines] == stored['frame_sha256']
        states = [from_checkpoint(record) for record in records]
        case = stored['case']
        expected = declared_initial(case)
        assert states[0] == expected, identifier
        assert len(states) == case['steps']+1 == stored['frames']
        for index, record in enumerate(records):
            assert record['completed_steps'] == index
            assert tuple(record['experiment']['coupling_signs']) == (1, 1, 1)
            assert record['coupling_fingerprint'] == coupling_fingerprint((1, 1, 1))
        stationary = all(state == expected for state in states)
        assert stationary == stored['entire_board_stationary']
        derived = {str(side): observe(states, side, case) for side in (-1, 1)}
        assert derived == stored['outlets'], identifier
        observations[identifier] = {'outlets': derived, 'stationary': stationary}
        cases[identifier] = case
        frames += len(states)
        if identifier in selected_ids:
            audit_paths.append((trace_path, expected))
    scores = {}
    for side in (-1, 1):
        for pattern in patterns:
            vectors = {suffix: observations[f"iso-p0-{'L' if side < 0 else 'R'}-{pattern}-{suffix}"]['outlets'][str(side)]['calibration_vector']
                       for suffix in ('base', 'i', 'j', 'ij')}
            assert all(len(v) == 480 for v in vectors.values())
            mixed = [vij-vi-vj+v0 for v0, vi, vj, vij in zip(
                vectors['base'], vectors['i'], vectors['j'], vectors['ij'])]
            count = sum(v != 0 for v in mixed)
            score = Fraction(count, 480)
            key = f'{side},{pattern}'
            saved = scores_saved[key]
            assert saved == {'score': str(score), 'nonzero_coordinates': count,
                'vector_length': 480, 'binary_K_diagnostic': int(count != 0),
                'mixed_vector': mixed, 'calibration_vectors': vectors}
            scores[key] = score
    computed = []
    for registered in result['comparisons']:
        p = registered['phase_index']
        left, right = registered['patterns']
        joint = observations[registered['id']]['outlets']
        isolated = [observations[f'iso-p{p}-L-{left}-base']['outlets']['-1'],
                    observations[f'iso-p{p}-R-{right}-base']['outlets']['1']]
        values = [scores[f'-1,{left}'], scores[f'1,{right}']]
        functional = all(v['functional'] for v in isolated)
        matched = isolated[0]['arrival_tuple'] == isolated[1]['arrival_tuple']
        unequal = values[0] != values[1]
        high = -1 if values[0] > values[1] else 1
        sole = [side for side in (-1, 1)
                if joint[str(side)]['functional'] and joint[str(-side)]['strong_quiet']]
        unique = len(sole) == 1
        expected = {'scores': [str(v) for v in values], 'both_isolated_functional': functional,
            'matched_arrivals': matched, 'unequal_scores': unequal,
            'primary_eligible': functional and matched and unequal,
            'higher_side': high if unequal else None,
            'unique_outlet_side': sole[0] if unique else None,
            'higher_only': unequal and unique and sole[0] == high,
            'competitive_component': functional and unique,
            'null_stationary': observations[f'null-{left}-{right}']['stationary']}
        assert all(registered[k] == v for k, v in expected.items()), registered['id']
        computed.append({'id': registered['id'], **expected})
    by_id = {r['id']: r for r in computed}
    strong = competition = None
    for left, right in itertools.combinations(patterns, 2):
        ids = [f'joint-p{p}-{a}-{b}' for p in range(3) for a, b in ((left, right), (right, left))]
        if strong is None and all(by_id[i]['primary_eligible'] and by_id[i]['higher_only'] for i in ids):
            strong = {'patterns': [left, right], 'joint_ids': ids}
        if competition is None and all(by_id[i]['competitive_component'] for i in ids):
            competition = {'patterns': [left, right], 'joint_ids': ids}
    summary = result['summary']
    assert summary['strong_candidate'] == strong
    assert summary['competitive_candidate'] == competition
    assert summary['selected_for_holdout'] == (strong or competition)
    eligible = [row for row in computed if row['primary_eligible']]
    assert len(eligible) == summary['eligible_comparisons']
    assert sum(not row['higher_only'] for row in eligible) == summary['eligible_counterexamples']
    assert sum(row['competitive_component'] for row in computed) == summary['competitive_comparisons']
    full_replays = [audit_checkpoints(path, expected_initial=expected, expected_signs=(1, 1, 1))
                    for path, expected in audit_paths]
    report = {'format': 'universe24-independent-selection-review-v1', 'passed': True,
        'recorded_runs_observed_independently': len(observations), 'recorded_frames_observed': frames,
        'independent_calibration_scores': len(scores), 'independent_joint_classifications': len(computed),
        'eligible_comparisons': len(eligible),
        'eligible_counterexamples': sum(not r['higher_only'] for r in eligible),
        'competitive_comparisons': sum(r['competitive_component'] for r in computed),
        'selected_for_holdout': strong or competition,
        'full_oracle_replayed_runs': len(full_replays),
        'full_oracle_replayed_transitions': sum(r['transitions'] for r in full_replays),
        'source_snapshot_hashes_verified': True,
        'score_freeze_review': 'Saved calibration file/hash verified; retained source performs its write before joint cases. Files alone are not an external timestamp service.',
        'eligible_cases': eligible, 'full_replays': full_replays,
        'evidence_result_sha256': digest_file(evidence/'result.json'),
        'source_sha256': {str(p): digest_file(p) for p in (Path(__file__), Path(__file__).with_name('audit.py'))},
        'cpu_seconds': time.process_time()-started,
        'scope': 'All observations and243 classifications independently recomputed;20 selected full trajectories replayed. This refutes the registered finite-family C_pair prediction and certifies no robust selector or physical complexity law.'}
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
    print(json.dumps({k: v for k, v in report.items() if k not in ('eligible_cases', 'full_replays', 'source_sha256')}))
