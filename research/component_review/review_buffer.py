"""Representative independent full-state audit of the negative buffer study."""
import argparse
import json
from pathlib import Path

from .audit import Snapshot, audit_checkpoints, digest_file, from_checkpoint, transition_events


def review(evidence, output):
    evidence, output = Path(evidence), Path(output)
    summary = json.loads((evidence/'result.json').read_text())
    assert summary['cases_completed'] == 81 and summary['runs_completed'] == 324
    assert summary['passing_cases'] == [] and all(not row['passed'] for row in summary['results'])
    assert digest_file(evidence/'protocol.frozen.json') == summary['protocol_sha256']
    for path, value in summary['source_manifest'].items():
        assert digest_file(evidence/'source'/path) == value
    reports = []
    for mask in ('00', '10', '01', '11'):
        folder = evidence/'cases'/('confirmation-buffer-040-s'+mask)
        stored = json.loads((folder/'result.json').read_text())
        case = stored['preparation']
        origin = (case['side']//2,)*3
        cells = {(origin[0]+x, origin[1], origin[2], g): (0, 0, r)
                 for x in range(-8, 17) for g, r in ((0, 4), (14, 0))}
        for g, r in ((0, 2), (14, 4)):
            cells[(*origin, g)] = (0, 0, r)
        for offset in (-2, -1, 1, 2):
            for g in (0, 14):
                cells[(origin[0]+offset, origin[1], origin[2], g)] = (0, 0, 2)
        for offset, enabled in zip((-8, 16), mask):
            b = int(enabled)
            for g, value in ((0, b), (14, -b)):
                cells[(origin[0]+offset, origin[1], origin[2], g)] = (0, value, 2)
        expected = Snapshot(201, (0, 0, 2), cells)
        oracle = audit_checkpoints(folder/'states.jsonl', expected_initial=expected, expected_signs=(1, 1, 1))
        states = [from_checkpoint(json.loads(line)) for line in (folder/'states.jsonl').read_text().splitlines()]
        addresses = [(*origin, g) for g in range(48)]
        rtimes, events = [], []
        for step, (before, after) in enumerate(zip(states, states[1:]), 1):
            if any(before.at((*origin, g))[2] != after.at((*origin, g))[2] for g in (0, 14)):
                rtimes.append(step)
            for event in transition_events(before, after, addresses)['arithmetic']:
                address = event['address']
                events.append({'step': step, 'address': list(address), 'kind': event['kind'],
                               'quotient': event['quotient'], 'before': list(before.at(address)),
                               'after': list(after.at(address))})
        assert rtimes == stored['record_event_times']
        assert events == json.loads((folder/'receiver_events.json').read_text())
        reports.append({**oracle, 'source_mask': mask, 'R_times': rtimes,
                        'all_48_receiver_C_times': sorted({e['step'] for e in events})})
    report = {'format': 'universe24-independent-buffer-review-v1', 'passed': True,
              'reported_cases': 81, 'reported_runs': 324, 'reported_accepted_cases': 0,
              'independently_replayed_runs': 4, 'frames': 164, 'transitions': 160,
              'case_id': 'confirmation-buffer-040', 'source_snapshot_hashes_verified': True,
              'scope': 'Four complete controls independently prepared, replayed, inverted and observed. The324-run negative count is the inspected study result, not an independent full324-run replay.',
              'source_sha256': {str(p): digest_file(p) for p in (Path(__file__), Path(__file__).with_name('audit.py'))},
              'evidence_result_sha256': digest_file(evidence/'result.json'), 'cases': reports}
    with output.open('x') as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write('\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    report = review(args.evidence, args.output)
    print(json.dumps({k: v for k, v in report.items() if k not in ('cases', 'source_sha256')}))
