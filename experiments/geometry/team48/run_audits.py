"""Reproduce Team48 constructions and their positive/negative controls.

Success means the declared results were reproduced, including failed physical
gates. It never means the nonlinear Einstein gate passed.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

MODULES = (
    'candidate', 'geometry_triangular_audit', 'geometry_charged_audit',
    'geometry_positive_audit', 'matter_audit', 'matter_charged_audit',
    'integer_audit', 'integer_pr39_audit', 'integer_staggered_audit',
    'constraints_audit', 'numerical_milne', 'numerical_sign_validation',
    'numerical_triangular_validation', 'numerical_milne_refinement',
    'numerical_sourced_refinement', 'numerical_positive_validation',
    'variational_null_rotation', 'variational_projective_milne',
    'variational_amplitude_modes',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    out = ROOT/'runs/team48'
    logs = out/'logs'
    logs.mkdir(parents=True, exist_ok=True)
    checks = []
    for module in MODULES:
        command = [sys.executable, '-m', 'experiments.geometry.team48.'+module]
        with (logs/(module+'.log')).open('w') as output:
            result = subprocess.run(command, cwd=ROOT, stdout=output,
                                    stderr=subprocess.STDOUT, timeout=300)
        checks.append({'module': module, 'exit_code': result.returncode,
                       'log': str((logs/(module+'.log')).relative_to(ROOT))})
        print(module+': '+('PASS' if result.returncode == 0 else 'FAIL'), flush=True)
        if result.returncode:
            raise RuntimeError('Audit failed; inspect '+checks[-1]['log'])
    from experiments.geometry.team48.candidate import build
    candidates = [build(model).manifest() for model in
                  ('scalar_dust', 'maxwell', 'charged', 'charged_positive')]
    sources = sorted((ROOT/'experiments/geometry/team48').glob('*.py'))
    sources += sorted((ROOT/'experiments/geometry/team48').glob('*.md'))
    sources += [ROOT/path for path in (
        'universe24/core/engine.py', 'universe24/core/tensor.py',
        'universe24/algebra/frame_equations.py', 'universe24/algebra/frame_matter.py',
        'universe24/layers/frame_matter.py', 'universe24/prepare/frame_matter.py',
        'universe24/tests/test_team48.py', 'docs/TEAM48_RESEARCH.md')]
    artifacts = sorted(path for path in out.rglob('*.json') if path.name != 'report.json')
    report = {
        'schema': 'Universe24-team48-research-v1',
        'baseline_main': '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
        'reviewed_PR39_head': '35344a1ba5c12c857404115e893911411ece7d35',
        'coordination_issue': 'https://github.com/Closer24/Universe24/issues/17',
        'checks': checks, 'candidates': candidates,
        'gates': {
            'fixed_six_degree_three_single_face_budget': True,
            'exact_PR39_70_to_36_physical_trajectories': True,
            'classical_charged_sources_and_backreaction_implemented': True,
            'signed_square_dust_nonnegative': True,
            'positive44_det_B_on_nonzero_wronskian_sector': True,
            'nonzero_wronskian_is_exact_continuum_time_pair': False,
            'generic_discrete_Einstein_constraint_preservation': False,
            'controlled_general_integer_refinement': False,
            'general_stable_full_Einstein_solution': False,
            'default_runtime_replaced': False,
        },
        'source_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sources},
        'artifact_sha256': {str(p.relative_to(ROOT)): digest(p) for p in artifacts},
    }
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    result = run()
    print(json.dumps({'audits': len(result['checks']), 'all_declared_checks_reproduced': True,
                      'general_Einstein_gate': False, 'report': 'runs/team48/report.json'}))
