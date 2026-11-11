"""Collect executed evidence and verify source hashes; does not run dynamics."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = {
    'sensor': ('01-stagnation/report.json', 'local_stagnation.py'),
    'memory': ('02-memory/report.json', 'structural_memory.py'),
    'rotor': ('03-reassembly/verified/summary.json', 'reassembly_feedback.py'),
    'organization': ('04-organization/report.json', 'cycle_organization.py'),
    'phase': ('05-born/report.json', 'complexity_born.py'),
    'joint': ('07-sensor-rotor/report.json', 'sensor_rotor.py'),
    'independent_controls': ('06-acceptance/report.json', 'acceptance_audit.py'),
    'independent_sensor': ('06-acceptance/stagnation-independent/report.json', None),
    'independent_phase': ('06-acceptance/born-independent/report.json', None),
    'independent_peers': ('06-acceptance/peers-independent/report.json', None),
    'independent_joint': ('06-acceptance/joint-independent/report.json', None),
}
# Full traces and per-update observations remain in the reproducible run
# artifact. Preserve all case entries, interventions, failures and gate results.
OMIT = {'frames', 'samples', 'records', 'rows', 'branches', 'state_hashes',
        'message_hashes', 'memory_subsystem_return_updates'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(value):
    if isinstance(value, dict):
        return {k: compact(v) for k, v in value.items() if k not in OMIT}
    if isinstance(value, list):
        return [compact(v) for v in value]
    return value


def collect(run_root):
    evidence, verified = {}, {}
    for name, (relative, owner) in REPORTS.items():
        path = run_root / relative
        report = json.loads(path.read_text())
        hashes = report.get('source_sha256', {})
        if isinstance(hashes, str):
            if owner is None:
                raise ValueError(f'Cannot identify source of {relative}')
            hashes = {f'experiments/complexity/{owner}': hashes}
        hashes = {**hashes, **report.get('dependency_sha256', {})}
        for source, expected in hashes.items():
            actual = sha(ROOT / source)
            if actual != expected:
                raise ValueError(f'Stale evidence {relative}: {source}')
            verified[source] = actual
        evidence[name] = {'report': relative, 'report_sha256': sha(path),
                          'result': compact(report)}
    return {
        'production_baseline': '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
        'audit_parent': 'e0539cc60057b4616bce95cfa0926f4a7705b58f',
        'scope': 'Optional research tensors; production law unchanged.',
        'method': 'Report collection with source verification, not independent replay. See the included independent audit outputs and reproduction commands.',
        'original_goal_demonstrated': False,
        'Born_selection_derived': False,
        'Bell_violation_claimed': False,
        'verified_report_source_sha256': verified,
        'research_source_sha256': {
            str(p.relative_to(ROOT)): sha(p)
            for p in sorted((ROOT / 'experiments/complexity').glob('*.py'))},
        'protocol_sha256': {
            p: sha(ROOT / p) for p in ('experiments/complexity/PROTOCOL.md',
                                      'experiments/cosmology/PROTOCOL.md')},
        'reports': evidence,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, default=Path('runs/complexity-research'))
    parser.add_argument('--out', type=Path, default=Path('runs/complexity-research/summary.json'))
    args = parser.parse_args()
    report = collect(args.runs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'reports': len(report['reports']),
                      'verified_sources': len(report['verified_report_source_sha256']),
                      'original_goal_demonstrated': False}))


if __name__ == '__main__':
    main()
