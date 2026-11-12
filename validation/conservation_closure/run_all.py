"""Execute six connected audits; retain their positive and negative evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
AUDITS = ('native', 'tensor_metric', 'covector_geodesics', 'clocks',
          'noether_spatial', 'review')


def main():
    output = ROOT/'runs/conservation_closure'
    output.mkdir(parents=True, exist_ok=True)
    rows, evidence = [], {}
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    for module in AUDITS:
        start = time.monotonic()
        result = subprocess.run(
            [sys.executable, '-m', 'validation.conservation_closure.'+module],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=900)
        (output/(module+'.stdout.log')).write_text(result.stdout)
        (output/(module+'.stderr.log')).write_text(result.stderr)
        path = output/(module+'.json')
        row = {'module': module, 'returncode': result.returncode,
               'seconds': round(time.monotonic()-start, 3),
               'evidence': str(path.relative_to(ROOT))}
        rows.append(row)
        print(json.dumps(row), flush=True)
        if result.returncode:
            print(result.stderr[-5000:], file=sys.stderr)
            raise SystemExit(result.returncode)
        evidence[module] = json.loads(path.read_text())
        row['evidence_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    paths = sorted((ROOT/'validation/conservation_closure').glob('*.py'))
    report = {
        'researchers': 6,
        'massless_predecessor': '228f581d02971435c0cd70548ff56267378ffc31',
        'massive_predecessor': '6b82369830bf763cbaddcc37bd972c555faea782',
        'selected_candidate': 'eight-channel exact native diagonal Bianchi I, massless scalar and dust',
        'audits': rows, 'evidence': evidence,
        'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in paths},
        'spatial_transport_control': 'separate arithmetic tensor; no coupled Einstein claim',
        'operational_detector': 'not_implemented',
        'general_spatial_Einstein_acceptance': 'not_established',
        'massive_source_native_encoding': 'not_established',
        'uniqueness_from_conservation': 'false',
    }
    (output/'audit_manifest.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'audit_count': len(rows), 'all_returncodes_zero': True,
                      'general_spatial_Einstein_acceptance': 'not_established'}), flush=True)


if __name__ == '__main__':
    main()
