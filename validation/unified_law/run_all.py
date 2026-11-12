"""Run seven-researcher proofs against one shared homogeneous candidate."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
AUDITS = (
    ('common', '00_common.json'),
    ('constrained_coordinates', '01_coordinates.json'),
    ('hamiltonian', '02_hamiltonian.json'),
    ('native_scheduler', '03_native_scheduler.json'),
    ('invariant_map', '04_invariant_map.json'),
    ('spatial_metric', '05_spatial_metric.json'),
    ('clock_acceptance', '06_clock_acceptance.json'),
    ('independent_review', '07_review.json'),
)


def main():
    output = ROOT/'runs/unified_law'
    output.mkdir(parents=True, exist_ok=True)
    rows, evidence = [], {}
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    for module, filename in AUDITS:
        start = time.monotonic()
        result = subprocess.run([sys.executable, '-m', 'validation.unified_law.'+module],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=900)
        (output/(module+'.stdout.log')).write_text(result.stdout)
        (output/(module+'.stderr.log')).write_text(result.stderr)
        path = output/filename
        row = {'module': module, 'returncode': result.returncode,
               'seconds': round(time.monotonic()-start, 3), 'evidence': str(path.relative_to(ROOT))}
        rows.append(row)
        print(json.dumps(row), flush=True)
        if result.returncode:
            print(result.stderr[-4000:], file=sys.stderr)
            raise SystemExit(result.returncode)
        evidence[module] = json.loads(path.read_text())
        row['evidence_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    paths = sorted((ROOT/'validation/unified_law').glob('*.py'))
    report = {'baseline_commit': '4c2abdda08c4212d08896bd2bd933a7c8dd42c1c',
        'researchers': 7, 'audits': rows, 'evidence': evidence,
        'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        'selected_candidate': 'six-channel homogeneous constrained spinor + beta',
        'native_scheduler_status': 'separate arithmetic bridge; not the selected spinor tensor',
        'general_spatial_Einstein_acceptance': 'not_established',
        'operational_detector': 'not_implemented', 'efficient_projective_bit_cost': 'failed'}
    (output/'audit_manifest.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'audit_count': len(rows), 'all_returncodes_zero': True,
        'selected_candidate': report['selected_candidate'],
        'general_spatial_Einstein_acceptance': 'not_established'}), flush=True)


if __name__ == '__main__':
    main()
