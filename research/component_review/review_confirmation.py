"""Bounded independent review of retained confirmation-search evidence."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import time

from .audit import (audit_checkpoints, digest_file, from_checkpoint, net_inputs,
                    transition_events)


def review(evidence, output, case_id='confirmation-000'):
    evidence, output = Path(evidence), Path(output)
    summary = json.loads((evidence/'result.json').read_text())
    protocol = json.loads((evidence/'protocol.frozen.json').read_text())
    source_manifest = json.loads((evidence/'source_manifest.json').read_text())
    for path, expected in source_manifest.items():
        assert digest_file(evidence/'source'/path) == expected, path
    assert digest_file(evidence/'protocol.frozen.json') == summary['protocol_sha256']
    started = time.process_time()
    results = []
    for mask in ('00', '10', '01', '11'):
        folder = evidence/'cases'/(case_id+'-s'+mask)
        audit = audit_checkpoints(folder/'states.jsonl', expected_signs=(1, 1, 1))
        stored = json.loads((folder/'result.json').read_text())
        states = [from_checkpoint(json.loads(line)) for line in
                  (folder/'states.jsonl').read_text().splitlines()]
        center = (states[0].side//2,)*3
        all_channels = [(*center, g) for g in range(48)]
        detector = [(*center, g) for g in (0, 14)]
        records, events = [], []
        for step in range(1, len(states)):
            before, after = states[step-1:step+1]
            if any(before.at(a)[2] != after.at(a)[2] for a in detector):
                records.append(step)
            for event in transition_events(before, after, all_channels)['arithmetic']:
                address = event['address']
                events.append({'step': step, 'address': list(address),
                               'kind': event['kind'], 'quotient': event['quotient'],
                               'before': list(before.at(address)),
                               'after': list(after.at(address))})
        assert records == stored['record_event_times']
        assert events == json.loads((folder/'receiver_events.json').read_text())
        results.append({**audit, 'mask': mask, 'R_times': records,
                        'all_48_receiver_C_times': sorted({e['step'] for e in events}),
                        'all_receiver_events': events,
                        'whole_board_stationary': all(s == states[0] for s in states),
                        'early_detector': [{'step': step,
                                            'triples': [list(states[step].at(a)) for a in detector],
                                            'next_inputs': net_inputs(states[step], detector)}
                                           for step in range(6, min(13, len(states)))]})
    checked = json.loads((evidence/(case_id+'.json')).read_text())
    assert not checked['passed']
    mask10 = next(r for r in results if r['mask'] == '10')
    old9 = next(r for r in mask10['early_detector'] if r['step'] == 9)
    assert old9['next_inputs'] == [-2, 2]
    assert any(event['step'] == 10 and event['address'][-1] == 14
               for event in mask10['all_receiver_events'])
    minimum_gap = min(d2-d1 for d1, d2 in protocol['family']['distance_pairs'])
    report = {'format': 'universe24-independent-confirmation-review-v1',
              'passed': True, 'studied_case': case_id,
              'reported_search_cases': summary['cases_completed'],
              'reported_search_runs': summary['runs_completed'],
              'reported_passing_cases': summary['passing_cases'],
              'independently_replayed_runs': len(results),
              'frames': sum(r['frames'] for r in results),
              'transitions': sum(r['transitions'] for r in results),
              'finding': 'Source1-only writes a transient remainder record at step8; old-step9 input(-2,+2) produces an unwanted receiver C at10. This fails the frozen silent waiting interface.',
              'waiting_bound_review': {'standalone_count_is_off_by_one': True,
                  'combined_windows_minimum_quiet_transitions': minimum_gap-2,
                  'registered_required_quiet_transitions': 4,
                  'can_change_overall_acceptance_in_registered_family': minimum_gap-2 < 4},
              'source_snapshot_hashes_verified': True,
              'cpu_seconds': time.process_time()-started,
              'source_sha256': {str(p): digest_file(p) for p in (
                  Path(__file__), Path(__file__).with_name('audit.py'))},
              'evidence_result_sha256': digest_file(evidence/'result.json'),
              'runs': results,
              'scope': 'Four representative traces independently replayed and observed. No full256-run independent replay and no positive confirmation claim.'}
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
    print(json.dumps({k: report[k] for k in ('passed', 'independently_replayed_runs',
                                            'frames', 'transitions', 'finding')}))
