"""Build one saved Universe24 run, its geodesic board and scoped evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .run import ROOT, run
from .board import render_board
from .constraint_audit import audit as constraint_audit
from .clock_audit import audit as clock_audit
from .quantum_audit import audit as quantum_audit
from .time_cost_audit import audit as time_cost_audit


def build(out):
    out = Path(out)
    data = run(out)
    reports = {
        'constraints': constraint_audit(),
        'clocks': clock_audit(data),
        'quantum': quantum_audit(),
        'time_cost': time_cost_audit(),
    }
    for name, report in reports.items():
        (out / (name + '.json')).write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    data['research_evidence'] = reports
    data['quantum'] = reports['quantum']
    sources = sorted((ROOT / 'validation/geodesic_board').glob('*.py'))
    sources += sorted((ROOT / 'validation/geodesic_board').glob('*.cjs'))
    sources += sorted((ROOT / 'docs/research/geodesic_board').glob('*.md'))
    data['provenance']['integration_source_sha256'] = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources
    }
    (out / 'board_data.json').write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')
    render_board(data, out / 'board.html')
    summary = {
        'schema': 'universe24/geodesic-board/evidence/1',
        'run_id': data['provenance']['run_id'],
        'bundle_id': data['provenance']['bundle_id'],
        'tensor_sha256': data['provenance']['tensor_sha256'],
        'metadata': data['metadata'],
        'acceptance_gates': data['acceptance_gates'],
        'first_step_control': data['independent_first_step_control'],
        'source_sha256': data['provenance']['integration_source_sha256'],
        'files_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(out.iterdir()) if p.is_file()},
        'scope': 'One Engine run and passive readouts; general Einstein and quantum acceptance remain open.',
    }
    (out / 'evidence.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'runs/geodesic-board')
    args = parser.parse_args()
    result = build(args.out)
    print(json.dumps({'board': str(args.out / 'board.html'),
                      'metadata': result['metadata'],
                      'acceptance_gates': result['acceptance_gates']}, indent=2))


if __name__ == '__main__':
    main()
