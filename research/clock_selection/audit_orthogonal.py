"""Independent initial-state algebra for crossed guides; no evolution."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time
from research.clock_selection.audit import Snapshot, coupling, file_digest, load, native_digest
from research.reference.algebra import DIRECTIONS


def initial(case):
    L, phase, r, gap, mask = (case[k] for k in ('side', 'phase', 'r', 'gap', 'control'))
    c = L//2
    matrix = coupling((1, 1, 1))
    cells = {}
    def assign(address, triple):
        if address in cells:
            assert cells[address] == triple, ('Independent initial conflict', address)
        cells[address] = triple
    starts = (c-17, c-17-gap)
    sources = []
    for axis, gs, start, bit in ((0, (0, 14), starts[0], mask[0]), (1, (15, 39), starts[1], mask[1])):
        line = lambda i: (i, c-1, c) if axis == 0 else (c+1, i, c)
        assert all(matrix.ports[d][g] == g and matrix.weights[d][g] == 1 for d in (2*axis, 2*axis+1) for g in gs)
        for i in range(L):
            if i != c and i not in range(start, start+4):
                for g, rho in zip(gs, (0, 4)):
                    assign((*line(i), g), (0, 0, rho))
        source = []
        for i in range(4):
            a = (1 if i == 0 else -1 if i == 2 else 0) if bit == '1' else 0
            b = (1 if i == 1 else -1 if i == 3 else 0) if bit == '1' else 0
            for g, sign, rho in zip(gs, (1, -1), (4, 0)):
                address = (*line(start+i), g)
                assign(address, (sign*a, sign*b, rho))
                source.append(address)
        for i in (1, 2):
            xyz = line(start+i)
            for d, delta in enumerate(DIRECTIONS):
                if d//2 == axis:
                    continue
                recipient_xyz = tuple(xyz[j]+delta[j] for j in range(3))
                for sender, sign in zip(gs, (1, -1)):
                    recipients = [g for g in range(48) if matrix.ports[d ^ 1][g] == sender]
                    assert len(recipients) == 1
                    g = recipients[0]
                    assign((*recipient_xyz, g), (0, 0, 2-2*sign*matrix.weights[d ^ 1][g]))
        sources.append(source)
    center = (c, c, c)
    nodes = (center, *(tuple(c+d[j] for j in range(3)) for d in DIRECTIONS))
    local = {(*node, g): (0, 0, 2) for node in nodes for g in range(48)}
    local[(*center, 2)] = (*((0, 1), (1, 0), (0, -1), (-1, 0))[phase], r)
    for d, node in enumerate(nodes[1:]):
        recipients = [g for g in range(48) if matrix.ports[d ^ 1][g] == 2]
        assert len(recipients) == 1
        g = recipients[0]
        local[(*node, g)] = (0, 0, (0, 2, 2, 0, 2, 2)[d] +
            (2*matrix.weights[d ^ 1][g] if phase in (1, 2) else 0))
    for address in ((c, c-1, c, 14), (c+1, c, c, 39)):
        assert local[address] == (0, 0, 2)
        local[address] = (0, 0, 4)
    for a, v in local.items():
        assign(a, v)
    return Snapshot(L, (0, 0, 2), cells), sources


def audit(folder, output):
    folder, output = Path(folder), Path(output)
    assert not output.exists()
    start = time.process_time()
    result, registration = load(folder/'result.json'), load(folder/'registration.json')
    assert result['trajectories'] == 0 and len(result['cases']) == 64
    checks, states = [], {}
    for entry in result['cases']:
        path = folder/entry['record']
        assert file_digest(path) == entry['sha256']
        record = load(path)
        expected, sources = initial(record['case'])
        raw = record['initial']
        actual = Snapshot(raw['side'], tuple(map(int, raw['background'])),
            {tuple(v[:4]): tuple(map(int, v[4:])) for v in raw['cells']})
        assert actual == expected
        assert native_digest(expected) == record['state_sha256'] == entry['state_sha256']
        assert len(sources[0]) == len(sources[1]) == 8 and not(set(sources[0]) & set(sources[1]))
        case = record['case']
        states[(case['side'], case['r'], case['phase'], case['control'])] = expected
        checks.append({'id': entry['id'], 'full_initial_equal': True})
    for L, r, phase in itertools.product((129, 161), (0, 4), range(4)):
        group = [states[(L, r, phase, m)] for m in ('00', '10', '01', '11')]
        assert all(len({s.at(a)[2] for s in group}) == 1 for a in set().union(*(s.cells for s in group)))
    report = {'format': 'universe24-crossed-input-preflight-independent-v1', 'passed': True,
        'auditor_sha256': file_digest(__file__), 'producer_sha256': registration['source_sha256'],
        'protocol_sha256': file_digest(folder/'protocol.json'), 'complete_preparations': 64,
        'checks': checks, 'trajectories': 0, 'cpu_seconds': time.process_time()-start,
        'claim_limit': 'Independent complete initial-data equivalence and source masks only; no functional evolution tested.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.study, args.output)))
