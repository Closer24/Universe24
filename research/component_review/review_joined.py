"""Independent full-state/readout review of the final 16 joined receiver trials."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time

from research.reference.algebra import DIRECTIONS, coupling as matrix_coupling
from .audit import (Snapshot, audit_checkpoints, digest_file, from_checkpoint,
                    net_inputs, transition_events)

PAIRS = {'O': (4, 0), 'N': (2, 2), 'R': (0, 4)}


def initial(case):
    cells = {}
    for side, pattern in zip((-1, 1), case['patterns']):
        if case.get('isolated_side') is not None and side != case['isolated_side']:
            continue
        for j in range(1, 8):
            pair = PAIRS[pattern[j-2]] if j in (2, 3) else (4, 0)
            for g, r in zip((0, 14), pair):
                cells[(64+side*j, 64, 64, g)] = (0, 0, r)
        for g, r in ((0, 4), (14, 2)):
            cells[(64+side*8, 64, 64, g)] = (0, 0, r)
    b = 1 if case['source_present'] else 0
    cells[(64, 64, 64, 0)] = (0, b, 2)
    cells[(64, 64, 64, 14)] = (0, -b, 2)
    return Snapshot(129, (0, 0, 2), cells)


def receiver_observation(states, addresses):
    reference = matrix_coupling((1, 1, 1))
    trace, events, rtimes = [], [], []
    for step, state in enumerate(states):
        values = [state.at(a) for a in addresses]
        arithmetic = []
        if step:
            derived = transition_events(states[step-1], state, addresses)
            if derived['remainder']:
                rtimes.append(step)
            arithmetic = [{'step': step, 'address': list(e['address']),
                           'kind': e['kind'], 'quotient': str(e['quotient'])}
                          for e in derived['arithmetic']]
            events.extend(arithmetic)
        terms = []
        for x, y, z, g in addresses:
            row = []
            for d, (dx, dy, dz) in enumerate(DIRECTIONS):
                sender = ((x+dx) % state.side, (y+dy) % state.side,
                          (z+dz) % state.side, reference.ports[d][g])
                row.append({'direction': d, 'address': list(sender),
                            'weight': reference.weights[d][g], 'b': str(state.at(sender)[1])})
            terms.append(row)
        trace.append({'step': step, 'detector': [[str(a), str(b), r] for a, b, r in values],
                      'memory': [v[2] for v in values],
                      'magnitude': [str(v[0]**2+v[1]**2) for v in values],
                      'next_input': [str(v) for v in net_inputs(state, addresses)],
                      'six_inputs': terms, 'arithmetic_events': arithmetic})
    return {'addresses': [list(a) for a in addresses], 'trace': trace,
            'record_event_times': rtimes, 'arithmetic_events': events}


def review(evidence, output):
    evidence, output = Path(evidence), Path(output)
    started = time.process_time()
    result = json.loads((evidence/'result.json').read_text())
    assert digest_file(evidence/'protocol.json') == result['protocol_sha256']
    batch = json.loads((evidence/'source_manifest.json').read_text())
    for path, value in batch.items():
        assert digest_file(evidence/'source'/path) == value
    candidates = {row['case']['id']: row for row in json.loads((evidence/'candidate_manifest.json').read_text())}
    assert set(candidates) == set(result['cases'])
    versions, reports = set(), []
    for identifier in sorted(result['cases']):
        if time.process_time()-started > 120:
            raise TimeoutError('Independent joined audit CPU budget exceeded')
        folder = evidence/'cases'/identifier
        analysis = json.loads((folder/'analysis.json').read_text())
        assert analysis == result['analyses'][identifier]
        runner = json.loads((folder/'result.json').read_text())
        case = analysis['case']
        assert case == candidates[identifier]['case']
        spec = json.loads((folder/'spec.json').read_text())
        assert spec == candidates[identifier]['spec']
        spec_hash = hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()
        assert spec_hash == runner['spec_sha256']
        hashes = runner['source_sha256']
        versions.add(json.dumps(hashes, sort_keys=True))
        assert all(batch.get(path) == value for path, value in hashes.items())
        path = folder/'states.jsonl.gz'
        assert digest_file(path) == analysis['trace_sha256']
        expected = initial(case)
        oracle = audit_checkpoints(path, expected_initial=expected, expected_signs=(1, 1, 1))
        states = [from_checkpoint(json.loads(line)) for line in gzip.decompress(path.read_bytes()).decode().splitlines()]
        assert len(states) == 49
        stationary = all(state == expected for state in states)
        assert stationary == analysis['entire_board_stationary']
        portable = json.loads((folder/'experiments.json').read_text())
        assert digest_file(folder/'experiments.json') == analysis['portable_bundle_sha256']
        experiment = portable['experiments'][0]
        assert experiment['provenance']['component_source_sha256'] == hashes
        assert len(experiment['frames']) == len(states)
        for frame, state in zip(experiment['frames'], states):
            cells = {tuple(row[:4]): (int(row[4]), int(row[5]), row[6]) for row in frame['cells']}
            assert len(cells) == len(frame['cells'])
            assert Snapshot(experiment['side'], tuple(int(v) for v in experiment['background']), cells) == state
        receivers = {}
        for side, label in ((-1, 'L'), (1, 'R')):
            if case.get('isolated_side') is not None and side != case['isolated_side']:
                continue
            addresses = [(64+8*side, 64, 64, g) for g in range(48)]
            observed = receiver_observation(states, addresses)
            assert observed == runner['observations'][label+'_receiver.node'], (identifier, side)
            bank = sorted({e['step'] for e in observed['arithmetic_events']})
            first = bank[0] if bank else None
            memories = [[state.at(addresses[g])[2] for g in (0, 14)] for state in states]
            one = len(bank) == 1
            first_in_window = first is not None and 12 <= first <= 15
            at_zero = first is not None and memories[first] == [0, 0]
            retained = first is not None and all(m == [0, 0] for m in memories[first:])
            actual_input = net_inputs(states[first-1], addresses) if first is not None else None
            driven = actual_input is not None and any(actual_input)
            quiet = all(all(state.at(a) == expected.at(a) for a in addresses) for state in states[1:])
            bad = next((t for t in range(first, 49) if memories[t] != [0, 0]), None) if first is not None else None
            stored = analysis['receivers'][str(side)]
            assert stored['C_bank_times'] == bank
            assert stored['C_event_count'] == len(observed['arithmetic_events'])
            assert stored['exactly_one_C_bank'] == one
            assert stored['event_in_declared_window'] == (one and first_in_window)
            assert stored['record_zero_zero_at_first_event'] == at_zero
            assert stored['record_retained_through_48'] == retained
            assert stored['nonzero_actual_input_at_first_event'] == bool(driven)
            assert stored['complete_node_quiet_all_1_to_48'] == quiet
            assert stored['first_record_failure_step'] == bad
            success = one and first_in_window and at_zero and retained and bool(driven)
            assert stored['single_click_retaining_success'] == success
            receivers[str(side)] = {'pattern': stored['pattern'], 'C_bank_times': bank,
                'first_C': first, 'first_C_in_window': first_in_window,
                'legacy_combined_one_C_and_window': stored['event_in_declared_window'],
                'first_old_input_pair': [actual_input[g] for g in (0, 14)] if actual_input else None,
                'first_record_failure_step': bad, 'full_48_channel_quiet': quiet,
                'single_click_retaining_success': success}
        if not case['source_present']:
            required, passed = True, stationary
        elif case['kind'] == 'isolated':
            required, passed = True, receivers[str(case['isolated_side'])]['single_click_retaining_success']
        elif case['patterns'][0] != case['patterns'][1]:
            winner = -1 if case['patterns'][0] == 'OR' else 1
            required = True
            passed = receivers[str(winner)]['single_click_retaining_success'] and receivers[str(-winner)]['full_48_channel_quiet']
            assert receivers[str(-winner)]['full_48_channel_quiet']
        else:
            required, passed = False, None
        assert analysis['required_case'] == required and analysis['required_case_passed'] == passed
        if required and case['source_present']:
            active = [r for r in receivers.values() if not r['full_48_channel_quiet']]
            assert len(active) == 1
            witness = active[0]
            assert witness['C_bank_times'] == list(range(12, 49, 2))
            assert witness['first_old_input_pair'] == [1, -1]
            assert witness['first_record_failure_step'] == 14
        reports.append({**oracle, 'case': case, 'required': required, 'passed': passed,
                        'stationary': stationary, 'receivers': receivers})
    assert len(versions) == 1 and len(reports) == 16
    failed = [r['case']['id'] for r in reports if r['required'] and not r['passed']]
    assert set(failed) == set(result['summary']['failed_required_ids'])
    assert len(failed) == 6
    report = {'format': 'universe24-independent-joined-receiver-review-v1', 'passed': True,
        'runs': len(reports), 'frames': sum(r['frames'] for r in reports),
        'independent_forward_inverse_transitions': sum(r['transitions'] for r in reports),
        'all_native_portable_states_equal': True, 'all_48_receiver_events_and_six_input_terms_recomputed': True,
        'source_versions': len(versions), 'all_sources_match_frozen_batch': True,
        'source_snapshot_files_verified': len(batch), 'null_cases_passed': 8,
        'required_source_cases_failed': 6, 'joined_component_passed': False,
        'failure_witness': {'first_C': 12, 'first_C_in_window': True,
            'old_step_11_input_pair': [1, -1], 'C_bearing_updates': 19,
            'C_times': list(range(12, 49, 2)), 'record_first_lost': 14},
        'loser_complete_48_channel_nodes_quiet_in_both_mixed_swaps': True,
        'diagnostic_caveat': 'Frozen event_in_declared_window also requires exactly one C. Its false value does not mean the first C was late. The actual failures are repeated clicks and record loss.',
        'source_sha256': {str(p): digest_file(p) for p in (Path(__file__), Path(__file__).with_name('audit.py'))},
        'evidence_result_sha256': digest_file(evidence/'result.json'),
        'cpu_seconds': time.process_time()-started, 'cases': reports,
        'scope': 'One initially supplied central source and an initially prepared waiting receiver; no autonomous prior waiting-state write or internally computed uniqueness approval was tested.'}
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
    print(json.dumps({k: v for k, v in report.items() if k not in ('cases', 'source_sha256')}))
