"""Run the eight-researcher continuation and shared runtime handoff.

All tests are source-only. A passing counterexample audit preserves its failed
physical gate; it never promotes that gate to a passed Einstein model.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
AUDITS = (
    ('common45', '00_common45.json'),
    ('formulation', '01_formulation.json'),
    ('native_compiler', 'native_compiler.json'),
    ('metric_domain', '03_metric_domain.json'),
    ('matter_clock', '04_matter_clock.json'),
    ('geodesic_signals', '05_geodesic_signals.json'),
    ('time_stability', 'time_stability.json'),
    ('constraint_closure', '07_constraint_closure.json'),
    ('integration_review', '08_integration_review.json'),
)


def main():
    output = ROOT/'runs/completion'
    output.mkdir(parents=True, exist_ok=True)
    rows, evidence = [], {}
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    for module, filename in AUDITS:
        start = time.monotonic()
        completed = subprocess.run([sys.executable, '-m', 'validation.completion.'+module],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=900)
        (output/(module+'.stdout.log')).write_text(completed.stdout)
        (output/(module+'.stderr.log')).write_text(completed.stderr)
        path = output/filename
        row = {'module': module, 'returncode': completed.returncode,
               'seconds': round(time.monotonic()-start, 3),
               'evidence': str(path.relative_to(ROOT))}
        rows.append(row)
        print(json.dumps(row), flush=True)
        if completed.returncode:
            print(completed.stderr[-4000:], file=sys.stderr)
            raise SystemExit(completed.returncode)
        evidence[module] = json.loads(path.read_text())
        row['evidence_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    paths = sorted((ROOT/'validation/completion').glob('*.py'))
    result = {'baseline_commit': '62202fdccdd9a40d5dbbec104de6f97d9587a999',
              'researchers': 8, 'audits': rows,
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              'evidence': evidence,
              'general_coupled_Einstein_acceptance': 'blocked',
              'scope': 'Distinct laws have distinct evidence; successful software audits do not combine physical gates.'}
    (output/'audit_manifest.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'audit_count': len(rows), 'all_returncodes_zero': True,
                      'general_coupled_Einstein_acceptance': 'blocked'}), flush=True)


if __name__ == '__main__':
    main()
