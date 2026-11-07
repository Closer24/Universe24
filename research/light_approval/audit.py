"""Independent, passive audit of light-approval records and selection controls.

The analytic controls are not Rule3 runs. The state audit uses the existing
exact matrix oracle, never the production updater or its coupling tables.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import gzip
from itertools import product
import json
from pathlib import Path
import time

from research.component_review.audit import (
    Snapshot, advance, rewind, coupling_fingerprint, net_inputs,
)

ROOT = Path(__file__).resolve().parents[2]


def fraction(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode('ascii')).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def exact_local_tables():
    """Finite exhaustive verification of the bounded-response CHSH lemma."""
    result = {}
    for name, alphabet in [('binary', (-1, 1)), ('ternary', (-1, 0, 1))]:
        scores = Counter()
        for a0, a1, b0, b1 in product(alphabet, repeat=4):
            scores[a0*b0 + a0*b1 + a1*b0 - a1*b1] += 1
        assert max(abs(v) for v in scores) == 2
        result[name] = {'tables': sum(scores.values()),
                        'score_histogram': dict(sorted(scores.items())),
                        'maximum_absolute_chsh': 2}
    return result


def table_statistics(rows):
    """Equal-weight finite ensemble; every row stays in all-trial statistics."""
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row['settings'])].append(tuple(row['outcomes']))
    assert set(grouped) == set(product(range(2), repeat=2))
    result = {}
    unconditioned, accepted = [], []
    for settings in product(range(2), repeat=2):
        values = grouped[settings]
        joint = [(a, b) for a, b in values if a != 0 and b != 0]
        e_all = Fraction(sum(a*b for a, b in values), len(values))
        e_joint = Fraction(sum(a*b for a, b in joint), len(joint)) if joint else None
        result[''.join(map(str, settings))] = {
            'trials': len(values), 'joint_clicks': len(joint),
            'A_clicks': sum(a != 0 for a, _ in values),
            'B_clicks': sum(b != 0 for _, b in values),
            'all_trial_correlation': fraction(e_all),
            'joint_click_conditioned_correlation': None if e_joint is None else fraction(e_joint),
            'A_mean': fraction(Fraction(sum(a for a, _ in values), len(values))),
            'B_mean': fraction(Fraction(sum(b for _, b in values), len(values))),
            'accepted_A_mean': None if not joint else fraction(Fraction(sum(a for a, _ in joint), len(joint))),
            'accepted_B_mean': None if not joint else fraction(Fraction(sum(b for _, b in joint), len(joint))),
        }
        unconditioned.append(e_all)
        accepted.append(e_joint)
    signs = (1, 1, 1, -1)
    signed = sum(s*e for s, e in zip(signs, unconditioned))
    conditional_signed = None if any(e is None for e in accepted) else sum(s*e for s, e in zip(signs, accepted))
    return {
        'settings': result,
        'signed_chsh_sum': fraction(signed),
        'all_trial_chsh': fraction(abs(signed)),
        'joint_click_conditioned_signed_sum': None if conditional_signed is None else fraction(conditional_signed),
        'joint_click_conditioned_chsh': None if conditional_signed is None else fraction(abs(conditional_signed)),
        'equal_weight_per_record': True,
    }


def postselection_control():
    rows = []
    for a, b in product(range(2), repeat=2):
        for u, v, sign in product(range(2), range(2), (-1, 1)):
            left = sign if a == u else 0
            right = sign*((-1)**(u*v)) if b == v else 0
            rows.append({'settings': [a, b], 'lambda': [u, v, sign],
                         'outcomes': [left, right]})
    result = table_statistics(rows)
    assert result['all_trial_chsh'] == '1'
    assert result['joint_click_conditioned_chsh'] == '4'
    assert all(row['joint_clicks'] == 2 and row['trials'] == 8
               for row in result['settings'].values())
    result.update({
        'model': 'Synthetic local response table; NOT a Rule3 run or a quantum model',
        'lambda_distribution': 'Uniform over (u,v,s) in {0,1}^2 x {-1,+1}, independent of settings',
        'A': 's when a=u, otherwise 0',
        'B': 's*(-1)^(u*v) when b=v, otherwise 0',
        'selection': 'Retain only A!=0 and B!=0; selected lambda has (u,v)=(a,b)',
        'locality': 'Each response uses only its own setting and the shared lambda',
        'interpretation': 'Setting-dependent retained ensembles invalidate inference from conditional CHSH to Bell nonlocality',
        'rows': rows,
    })
    return result


def recorded_snapshots(experiment):
    background = tuple(int(v) for v in experiment['background'])
    for index, frame in enumerate(experiment['frames']):
        assert frame['step'] == index
        cells = {}
        for row in frame['cells']:
            address = tuple(row[:4])
            assert address not in cells
            cells[address] = tuple(int(v) for v in row[4:])
        raw = {'side': experiment['side'], 'background': experiment['background'],
               'cells': frame['cells']}
        assert digest(raw) == frame['state_sha256'], ('state hash mismatch', index)
        yield Snapshot(experiment['side'], background, cells)


def audit_recording(experiment, receiver_positions, *, oracle=True, side=97, steps=16):
    signs = tuple(experiment['coupling']['body_signs'])
    assert signs == (1, 1, 1)
    assert experiment['coupling']['fingerprint'] == coupling_fingerprint(signs)
    snapshots = list(recorded_snapshots(experiment))
    assert len(snapshots) == steps+1 and all(s.side == side for s in snapshots)
    assert experiment['provenance']['full_rewind_equal'] is True
    assert experiment['provenance']['source_unchanged_during_capture'] is True
    traces, events, outcomes, inputs, memories = {}, {}, {}, {}, {}
    for label, position in receiver_positions.items():
        addresses = [(*position, g) for g in range(48)]
        traces[label] = [[list(s.at(a)) for a in addresses] for s in snapshots]
        inputs[label] = [net_inputs(s, addresses, signs) for s in snapshots]
        events[label] = []
        for t, (old, new) in enumerate(zip(snapshots, snapshots[1:]), 1):
            before, after = old.at((*position, 0)), new.at((*position, 0))
            quotient = before[0] + after[1]
            if quotient and before != after:
                events[label].append({'step': t, 'quotient': quotient,
                                      'sign': 1 if quotient > 0 else -1})
        outcomes[label] = events[label][0]['sign'] if events[label] else 0
        all_events = []
        for t, (old, new) in enumerate(zip(snapshots, snapshots[1:]), 1):
            for g, address in enumerate(addresses):
                before, after = old.at(address), new.at(address)
                q = before[0] + after[1]
                if q and before != after:
                    all_events.append({'step': t, 'channel': g, 'ell': q})
        magnitude = [s.at(addresses[0])[0]**2+s.at(addresses[0])[1]**2 for s in snapshots]
        rem_pair = [[s.at(addresses[0])[2], s.at(addresses[14])[2]] for s in snapshots]
        first = events[label][0]['step'] if events[label] else None
        memories[label] = {
            'I': magnitude, 'remainder_pairs': rem_pair, 'all48_clicks': all_events,
            'I_constant_after_first': first is not None and len(set(magnitude[first:])) == 1,
            'remainder_pair_constant_after_first': first is not None and len({tuple(v) for v in rem_pair[first:]}) == 1,
            'later_primary_clicks': max(0, len(events[label])-1),
        }
    if oracle:
        for index, (old, new) in enumerate(zip(snapshots, snapshots[1:]), 1):
            assert advance(old, signs) == new, ('matrix forward mismatch', index)
            assert rewind(new, signs) == old, ('matrix inverse mismatch', index)
    return {'states': len(snapshots), 'transitions': len(snapshots)-1,
            'oracle_forward_inverse': oracle, 'outcomes': outcomes,
            'events': events, 'local_trace_sha256': {k: digest(v) for k, v in traces.items()},
            'initial': snapshots[0], 'traces': traces, 'inputs': inputs, 'memories': memories,
            'whole_board_stationary': all(s == snapshots[0] for s in snapshots)}


def audit_evidence(folder, *, cpu_budget=120):
    started = time.process_time()
    protocol_path = folder/'protocol.json'
    protocol = json.loads(protocol_path.read_bytes())
    registration = json.loads((folder/'registration.json').read_bytes())
    expected_hash = '3c95321cce84de5bec0da1942f27a32d7d25250b68410c3da979203bad2c3e9d'
    assert file_digest(protocol_path) == registration['protocol_sha256'] == expected_hash
    assert file_digest(ROOT/'research/light_approval/protocol.json') == expected_hash
    assert protocol['steps'] == 16 and protocol['board'] == {
        'side': 97, 'background': [0, 0, 2], 'body_signs': [1, 1, 1]}
    assert registration['base_commit'] == '5894510ada12d22f17a70f93a41ec311aef13265'
    for path, expected in registration['source_sha256'].items():
        assert file_digest(ROOT/path) == expected, ('source changed', path)
    planned = registration['planned_cases']
    expected_cases = []
    for phase, a, b in product(range(4), range(2), range(2)):
        expected_cases.append({'ensemble': 'shared_phase', 'id': f'shared-{phase}-{a}{b}',
                               'phases': [phase, phase], 'present': True, 'settings': [a, b]})
    for pa, pb, a, b in product(range(4), range(4), range(2), range(2)):
        expected_cases.append({'ensemble': 'independent_phases', 'id': f'independent-{pa}-{pb}-{a}{b}',
                               'phases': [pa, pb], 'present': True, 'settings': [a, b]})
    for a, b in product(range(2), repeat=2):
        expected_cases.append({'ensemble': 'null', 'id': f'null-{a}{b}',
                               'phases': [0, 0], 'present': False, 'settings': [a, b]})
    assert planned == expected_cases
    paths = list((folder/'records').glob('*.json.gz'))
    assert {p.name for p in paths} == {c['id']+'.json.gz' for c in planned}
    positions = protocol['apparatus']['receivers']
    rows, run_reports, initial_groups, signatures = [], [], {}, defaultdict(set)
    total_states = total_transitions = 0
    clicked = later = memory_stable = remainder_stable = 0
    first_times = Counter()
    for case in planned:
        if time.process_time()-started > cpu_budget:
            raise TimeoutError('Independent audit CPU budget exceeded; partial audit not accepted')
        path = folder/'records'/(case['id']+'.json.gz')
        record = json.loads(gzip.decompress(path.read_bytes()))
        assert record['case'] == case and record['spec']['controls'] == case
        assert record['spec']['provenance']['protocol_sha256'] == expected_hash
        exp = record['experiment']
        assert exp['id'] == case['id']
        audit = audit_recording(exp, positions)
        expected_cells = {}
        for k, party in enumerate(('A', 'B')):
            x, y, z = positions[party]
            for offset in range(-7, 0):
                expected_cells[(x+offset, y, z, 0)] = (0, 0, 4)
                expected_cells[(x+offset, y, z, 14)] = (0, 0, 0)
            remainders = protocol['apparatus']['local_setting_receiver_remainders'][case['settings'][k]]
            for g, r in zip((0, 14), remainders):
                expected_cells[(x, y, z, g)] = (0, 0, r)
            a0, b0 = protocol['apparatus']['source_phases'][case['phases'][k]] if case['present'] else (0, 0)
            expected_cells[(x-8, y, z, 0)] = (a0, b0, 2)
            expected_cells[(x-8, y, z, 14)] = (-a0, -b0, 2)
        assert audit['initial'] == Snapshot(97, (0, 0, 2), expected_cells), ('initial preparation mismatch', case['id'])
        total_states += audit['states']
        total_transitions += audit['transitions']
        if not case['present']:
            assert audit['whole_board_stationary'], ('nonstationary null', case['id'])
        for party_index, party in enumerate(('A', 'B')):
            assert audit['traces'][party] == record['detector_traces'][party]
            assert audit['inputs'][party] == [[int(x) for x in row]
                for row in record['detector_input_traces'][party]]
            obs = record['observations'][party]
            assert audit['outcomes'][party] == obs['outcome']
            assert audit['memories'][party].items() <= obs.items()
            assert audit['local_trace_sha256'][party] == obs['detector_trace_sha256']
            expected_events = [{'step': e['step'], 'channel': 0, 'ell': e['quotient']}
                               for e in audit['events'][party]]
            assert expected_events == obs['primary_clicks']
            detection = case['present'] and case['phases'][party_index] in (0, 3)
            assert audit['outcomes'][party] == ((-1)**case['settings'][party_index] if detection else 0)
            if detection:
                first_time = (8 if case['phases'][party_index] == 0 else 9) + 2*case['settings'][party_index]
                assert [e['step'] for e in expected_events] == [first_time, first_time+2]
            if expected_events:
                assert expected_events[0]['step'] >= 8
                clicked += 1
                first_times[expected_events[0]['step']] += 1
                later += audit['memories'][party]['later_primary_clicks'] > 0
                memory_stable += audit['memories'][party]['I_constant_after_first']
                remainder_stable += audit['memories'][party]['remainder_pair_constant_after_first']
            key = (party, case['present'], case['phases'][party_index], case['settings'][party_index])
            signatures[key].add(audit['local_trace_sha256'][party])
            pos = positions[party]
            pair = protocol['apparatus']['local_setting_receiver_remainders'][case['settings'][party_index]]
            assert [audit['initial'].at((*pos, g)) for g in (0, 14)] == [(0, 0, r) for r in pair]
        phase_key = (case['present'], *case['phases'])
        if phase_key in initial_groups:
            initial, settings = initial_groups[phase_key]
            allowed = {(*positions[party], g) for k, party in enumerate(('A', 'B'))
                       if settings[k] != case['settings'][k] for g in (0, 14)}
            differences = {key for key in set(initial.cells)|set(audit['initial'].cells)
                           if initial.at(key) != audit['initial'].at(key)}
            assert differences == allowed
        else:
            initial_groups[phase_key] = (audit['initial'], case['settings'])
        for address in audit['initial'].cells:
            assert all(16 <= coordinate <= 80 for coordinate in address[:3]), 'initial support can wrap'
        rows.append({'ensemble': case['ensemble'], 'settings': case['settings'],
                     'lambda': case['phases'], 'outcomes': [audit['outcomes']['A'], audit['outcomes']['B']]})
        run_reports.append({'id': case['id'], 'record_sha256': file_digest(path),
                            'outcomes': audit['outcomes'], 'events': audit['events'],
                            'detector_sha256': audit['local_trace_sha256'],
                            'whole_board_stationary': audit['whole_board_stationary']})
    assert all(len(values) == 1 for values in signatures.values())
    stats = {group: table_statistics([r for r in rows if r['ensemble'] == group])
             for group in ('shared_phase', 'independent_phases', 'null')}
    for item in stats.values():
        assert abs(Fraction(item['all_trial_chsh'])) <= 2
    a, b = positions['A'], positions['B']
    distance = sum(min(abs(x-y), 97-abs(x-y)) for x, y in zip(a, b))
    assert distance == 48 and distance > 2*16
    return {
        'passed': True, 'runs': len(rows), 'states': total_states, 'transitions': total_transitions,
        'independent_matrix_forward_checks': total_transitions,
        'independent_matrix_inverse_checks': total_transitions,
        'protocol_sha256': expected_hash, 'registration_sha256': file_digest(folder/'registration.json'),
        'scope': 'Every complete retained state, both independent matrix transitions, every 48-channel detector and input trace',
        'sources_match_registration': True, 'fixed_tensor_matches_independent_matrix_oracle': True,
        'all_initial_states_match_independent_preparation': True,
        'all_planned_cases_present_once': True, 'no_trials_discarded': True,
        'settings_change_only_two_local_receiver_remainders': True,
        'all_local_traces_independent_of_remote_setting_and_phase': True,
        'local_trace_signature_groups': len(signatures), 'receiver_distance': distance,
        'backward_cones_disjoint_through_horizon': True, 'initial_support_cannot_wrap_by_horizon': True,
        'null_control_whole_boards_stationary': True,
        'clicked_receiver_instances': clicked, 'first_click_time_histogram': dict(sorted(first_times.items())),
        'clicked_instances_with_later_primary_click': later,
        'clicked_instances_with_stable_I_after_first': memory_stable,
        'clicked_instances_with_stable_remainder_pair_after_first': remainder_stable,
        'statistics': stats, 'records': run_reports,
        'derived_finite_response': {
            'formula': 'A(x,p)=(-1)^x*d(p), B(y,q)=(-1)^y*d(q), d=1 iff the source is present and its phase is0or3',
            'first_click_time': '8+2*setting for phase0;9+2*setting for phase3; no primary click by16 for phase1or2',
            'later_primary_click': 'Exactly one additional C two board updates after the first for every detected receiver',
            'scope': 'Exact explanatory lookup over the enumerated finite domain; not a prospective prediction for new preparations',
        },
        'cpu_seconds': time.process_time()-started,
        'source_files_sha256': {p: file_digest(ROOT/p) for p in
            ('research/light_approval/audit.py', 'research/component_review/audit.py', 'research/reference/algebra.py')},
        'preregistration_limit': 'Hashes and registration match the protocol observed by the audit before result inspection; this is not a third-party timestamp service',
    }


def longest_consecutive(indices):
    best = run = 0
    previous = None
    for index in indices:
        run = run+1 if previous is not None and index == previous+1 else 1
        best = max(best, run)
        previous = index
    return best


def audit_approval(folder):
    started = time.process_time()
    expected_hash = '395b6fd14ec252330234b2db4f1c843c9453c547b43e3cfa0a4b40a003229063'
    protocol_path = folder/'protocol.json'
    protocol = json.loads(protocol_path.read_bytes())
    registration = json.loads((folder/'registration.json').read_bytes())
    assert file_digest(protocol_path) == registration['protocol_sha256'] == expected_hash
    assert file_digest(ROOT/'research/light_approval/approval_protocol.json') == expected_hash
    assert protocol['board'] == {'side': 101, 'background': [0, 0, 2], 'body_signs': [1, 1, 1]}
    assert protocol['steps'] == 32 and protocol['receiver'] == [50, 50, 50]
    assert protocol['source_masks'] == [[False, False], [True, False], [False, True], [True, True]]
    for path, expected in registration['source_sha256'].items():
        assert file_digest(ROOT/path) == expected, ('secondary source changed', path)
    specs = registration['specs']
    assert len(specs) == 8
    assert {p.name for p in (folder/'records').glob('*.json.gz')} == {s['id']+'.json.gz' for s in specs}
    rows, by_control = [], {}
    for spec in specs:
        path = folder/'records'/(spec['id']+'.json.gz')
        record = json.loads(gzip.decompress(path.read_bytes()))
        assert record['spec'] == spec
        controls = spec['controls']
        phase, mask = controls['right_phase'], controls['source_mask']
        assert phase in (0, 1) and mask in protocol['source_masks']
        audit = audit_recording(record['experiment'], {'R': [50, 50, 50]}, side=101, steps=32)
        expected_cells = {(50+offset, 50, 50, g): (0, 0, r)
                          for offset in range(-8, 17) if offset not in (-8, 0, 16)
                          for g, r in ((0, 4), (14, 0))}
        expected_cells[(50, 50, 50, 0)] = (0, 0, 2)
        expected_cells[(50, 50, 50, 14)] = (0, 0, 4)
        for at, present, value in ((42, mask[0], 1), (66, mask[1], 1 if phase == 0 else -1)):
            for g, sign in ((0, 1), (14, -1)):
                expected_cells[(at, 50, 50, g)] = (0, sign*value if present else 0, 2)
        assert audit['initial'] == Snapshot(101, (0, 0, 2), expected_cells)
        trace, inputs = audit['traces']['R'], audit['inputs']['R']
        assert trace == record['detector_trace']
        assert inputs == [[int(x) for x in row] for row in record['detector_input_trace']]
        events = audit['memories']['R']['all48_clicks']
        times = sorted({e['step'] for e in events})
        pending = [t for t, local in enumerate(trace) if t > 0
                   and local[0] == [0, 0, 4] and local[14] == [0, 0, 2]]
        record_times = [t for t, local in enumerate(trace)
                        if local[0][2] == local[14][2] == 0
                        and local[0][0]**2+local[0][1]**2 == 1
                        and local[14][0]**2+local[14][1]**2 == 0]
        first_c = times[0] if times else None
        holds8 = first_c is not None and first_c+7 <= 32 and all(t in record_times for t in range(first_c, first_c+8))
        first_input = next(({'input_state_step': t, 'update_to_step': t+1, 'paired_input': [values[0], values[14]]}
                            for t, values in enumerate(inputs) if values[0] or values[14]), None)
        row = {'id': spec['id'], 'right_phase': phase, 'mask': mask,
               'node_C_times': times, 'all48_events': events, 'pending_times': pending,
               'maximum_pending_run': longest_consecutive(pending),
               'maximum_pending_before_first_C': longest_consecutive([t for t in pending if first_c is None or t < first_c]),
               'record_times': record_times, 'record_holds8_after_first_C': holds8,
               'whole_board_stationary': audit['whole_board_stationary'], 'first_paired_input': first_input,
               'record_sha256': file_digest(path), 'detector_sha256': audit['local_trace_sha256']['R']}
        reported = record['result']
        for key in ('node_C_times', 'pending_times', 'maximum_pending_run',
                    'maximum_pending_before_first_C', 'record_times', 'record_holds8_after_first_C'):
            assert row[key] == reported[key], ('secondary observation mismatch', key, spec['id'])
        assert events == reported['events']
        rows.append(row)
        key = (phase, tuple(mask))
        assert key not in by_control
        by_control[key] = row
    families = []
    for phase in (0, 1):
        null, left, right, joint = [by_control[(phase, tuple(mask))] for mask in protocol['source_masks']]
        predicates = {
            'null_stationary_and_quiet': null['whole_board_stationary'] and not null['node_C_times'],
            'both_isolated_controls_quiet': not left['node_C_times'] and not right['node_C_times'],
            'first_only_pending_at_least4': left['maximum_pending_run'] >= 4,
            'joint_pending_before_first_C_at_least4': joint['maximum_pending_before_first_C'] >= 4,
            'joint_exactly_one_C_time': len(joint['node_C_times']) == 1,
            'joint_first_C_within15to19': bool(joint['node_C_times']) and 15 <= joint['node_C_times'][0] <= 19,
            'joint_record_retained8_states': joint['record_holds8_after_first_C'],
        }
        families.append({'right_phase': phase, 'predicates': predicates, 'accepted': all(predicates.values())})
    return {'passed': True, 'runs': 8, 'states': 264, 'transitions': 256,
            'independent_matrix_forward_checks': 256, 'independent_matrix_inverse_checks': 256,
            'protocol_sha256': expected_hash, 'registration_sha256': file_digest(folder/'registration.json'),
            'all_initial_preparations_and_48channel_states_inputs_verified': True,
            'families': families, 'accepted_families': sum(f['accepted'] for f in families),
            'records': rows, 'cpu_seconds': time.process_time()-started,
            'scope': 'Prospective two-source preparation audit; does not refute all possible Rule3 approval preparations'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'research/light_approval/audit.json')
    parser.add_argument('--evidence', type=Path)
    parser.add_argument('--approval-evidence', type=Path)
    args = parser.parse_args()
    started = time.process_time()
    result = {'schema': 'universe24-light-approval-audit-v1',
              'status': 'analytic controls complete; Rule3 evidence audit pending',
              'local_tables': exact_local_tables(),
              'synthetic_postselection_control': postselection_control(),
              'source_sha256': file_digest(__file__),
              'cpu_seconds': time.process_time()-started}
    if args.evidence:
        result['rule3_audit'] = audit_evidence(args.evidence)
        result['status'] = 'passed: exact controls and complete independent Rule3 state audit'
        result['cpu_seconds'] = time.process_time()-started
    if args.approval_evidence:
        result['approval_audit'] = audit_approval(args.approval_evidence)
        result['status'] = 'passed: exact controls and complete independent Rule3 state audits'
        result['cpu_seconds'] = time.process_time()-started
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'output': str(args.output), 'status': result['status'],
                      'binary_tables': 16, 'ternary_tables': 81,
                      'synthetic_all_trial_S': '1', 'synthetic_postselected_S': '4'}))


if __name__ == '__main__':
    main()
