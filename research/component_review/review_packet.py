"""Independent full-state translation audit for the prepared guided packet."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import time

from research.reference.algebra import DIRECTIONS, coupling as matrix_coupling
from .audit import (Snapshot, audit_checkpoints, digest_file, from_checkpoint,
                    transition_events)


def declared_packet(side, present):
    """Reconstruct the protocol using the independent receiver routing relation."""
    if side < 5:
        raise ValueError('This packet declaration is scoped to L>=5')
    center = side//2
    cells = {(x, center, center, g): (0, 0, r)
             for x in range(side) for g, r in ((0, 0), (14, 4))}
    for x in range(4):
        a = {0: 1, 2: -1}.get(x, 0) if present else 0
        b = {1: 1, 3: -1}.get(x, 0) if present else 0
        cells[(x, center, center, 0)] = (a, b, 4)
        cells[(x, center, center, 14)] = (-a, -b, 0)
    reference = matrix_coupling((1, 1, 1))
    for x in (1, 2):
        for direction in range(2, 6):
            dx, dy, dz = DIRECTIONS[direction]
            # A receiver at source+direction sees its source in -direction.
            for source, sign in ((0, 1), (14, -1)):
                receivers = [g for g in range(48)
                             if reference.ports[direction ^ 1][g] == source]
                assert len(receivers) == 1
                receiver = receivers[0]
                weight = reference.weights[direction ^ 1][receiver]
                cells[(x+dx, center+dy, center+dz, receiver)] = (0, 0, 2-2*sign*weight)
    return Snapshot(side, (0, 0, 2), cells)


def translated(state):
    return Snapshot(state.side, state.background,
        {((x+1) % state.side, y, z, g): value
         for (x, y, z, g), value in state.cells.items()})


def review(evidence, output):
    evidence, output = Path(evidence), Path(output)
    summary = json.loads((evidence/'result.json').read_text())
    assert digest_file(evidence/'protocol.frozen.json') == summary['protocol_sha256']
    for path, expected in summary['source_manifest'].items():
        assert digest_file(evidence/'source'/path) == expected
    started = time.process_time()
    reports = []
    for run in summary['results']:
        folder = evidence/'cases'/run['id']
        initial = declared_packet(run['side'], run['present'])
        oracle = audit_checkpoints(folder/'states.jsonl', expected_initial=initial,
                                   expected_signs=(1, 1, 1))
        assert oracle['trace_sha256'] == run['trace_sha256']
        records = [json.loads(line) for line in (folder/'states.jsonl').read_text().splitlines()]
        states = [from_checkpoint(record) for record in records]
        assert len(states) == run['side']+1
        assert json.loads((folder/'initial.json').read_text()) == records[0]
        assert json.loads((folder/'final.json').read_text()) == records[-1]
        events = []
        for step, (before, after) in enumerate(zip(states, states[1:]), 1):
            if run['present']:
                assert after == translated(before), (run['id'], step)
            else:
                assert after == initial, (run['id'], step)
            addresses = sorted(set(before.cells) | set(after.cells))
            for event in transition_events(before, after, addresses)['arithmetic']:
                address = event['address']
                events.append({'step': step, 'address': list(address),
                    'kind': event['kind'], 'quotient': event['quotient'],
                    'before': list(before.at(address)), 'after': list(after.at(address))})
        assert events == json.loads((folder/'events.json').read_text())
        expected_events = 4*run['side'] if run['present'] else 0
        assert len(events) == run['guarded_events'] == expected_events
        first_return = next(step for step, state in enumerate(states[1:], 1) if state == initial)
        assert first_return == run['first_return'] == (run['side'] if run['present'] else 1)
        reports.append({**oracle, 'present': run['present'], 'side': run['side'],
            'exact_full_state_translation': bool(run['present']),
            'stationary_null': not run['present'], 'first_return': first_return,
            'all_board_guarded_events': len(events),
            'initial_halo_derived_from_independent_receiver_relation': True})
    assert len(reports) == 6
    report = {'format': 'universe24-independent-guided-packet-review-v1', 'passed': True,
        'runs': len(reports), 'frames': sum(r['frames'] for r in reports),
        'forward_and_inverse_transitions': sum(r['transitions'] for r in reports),
        'finite_checked_sides': [5, 17, 31], 'all_complete_states_and_events_checked': True,
        'proof_review': 'The fixed+++ prepared guide and halo obey exact translation for all L>=5; see packet_proof_review.md for the direct local algebra and induction. The six trace checks alone are not that theorem.',
        'physical_light_claim': False, 'silent_waiting_memory_claim': False,
        'boundary_scope': 'Intentionally periodic whole-row guide; wrap and periodL are part of the construction.',
        'source_snapshot_hashes_verified': True, 'cpu_seconds': time.process_time()-started,
        'source_sha256': {str(p): digest_file(p) for p in (Path(__file__), Path(__file__).with_name('audit.py'))},
        'evidence_result_sha256': digest_file(evidence/'result.json'), 'cases': reports}
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
