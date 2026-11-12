"""Reproduce scoped positive and negative refinement evidence through one Engine."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
MODULES = ('refinement_integer_audit', 'temporal_repair_projective',
           'validation_repair_projective', 'constraint_repair_spatial',
           'constraint_repair_ppwave', 'matter_repair_flux',
           'variational_repair_dust', 'refinement_runtime_adapter')
ARTIFACTS = ('refinement_integer/audit.json', 'temporal_repair/projective44.json',
             'validation_repair/projective_validation.json',
             'constraint_repair/spatial.json', 'constraint_repair/ppwave.json',
             'matter/repair_flux.json', 'variational/repair_plane_dust.json',
             'refinement_runtime/latest_report.json')


def run():
    output = ROOT/'runs/team48/refinement'
    output.mkdir(parents=True, exist_ok=True)
    checks = []
    for module in MODULES:
        command = [sys.executable, '-m', 'validation.geometry.team48.'+module]
        if module == 'refinement_runtime_adapter':
            command += ['--runtime-source', str(ROOT)]
        log = output/(module+'.log')
        with log.open('w') as stream:
            result = subprocess.run(command, cwd=ROOT, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=300)
        checks.append({'module': module, 'exit_code': result.returncode,
                       'command': command, 'log': str(log.relative_to(ROOT))})
        print(module+': '+('PASS' if result.returncode == 0 else 'FAIL'), flush=True)
        if result.returncode:
            raise RuntimeError('Audit failed; inspect '+str(log))
    products = {name: json.loads((ROOT/'runs/team48'/name).read_text()) for name in ARTIFACTS}
    spatial = products['validation_repair/projective_validation.json']
    source_files = sorted(Path(__file__).parent.glob('*.py'))
    source_files += sorted(Path(__file__).parent.glob('*.md'))
    source_files += [ROOT/'universe24/tests/test_team48_refinement.py',
                     ROOT/'docs/TEAM48_REFINEMENT.md']
    source_files += sorted((ROOT/'universe24/core').glob('*.py'))
    source_files += sorted((ROOT/'universe24/system').glob('*.py'))
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    report = {
        'schema': 'universe24/team48-projective-refinement/1',
        'baseline_main': 'c2d6b05a7b8e32cfad40162df0377335c8dc4577',
        'historical_proposal': '49b896c795203914a939e465d6d39e5b99343259',
        'coordination_issue': 'https://github.com/Closer24/Universe24/issues/40',
        'checks': checks,
        'interpretation': 'Passing audit programs reproduce their declared successes AND failures; they do not certify general Einstein physics.',
        'gates': {
            'integer_rational_step_encoding': 'passed',
            'protected44_metric_domain': 'passed_on_declared_preparation',
            'homogeneous_sourced_temporal_refinement': 'passed_on_tested_family',
            'inhomogeneous_refinement_groups': spatial['gates'],
            'generic_Einstein_constraints_and_spatial_convergence': 'open',
            'bounded_bit_growth_or_practical_long_horizon': 'failed_for_this_encoding',
            'operational_clock_detector_and_Born_Bell': 'not_tested',
            'one_runtime_complete_state_handoff': 'passed',
        },
        'source_sha256': {str(p.relative_to(ROOT)): digest(p) for p in source_files},
        'artifact_sha256': {str((ROOT/'runs/team48'/name).relative_to(ROOT)):
                            digest(ROOT/'runs/team48'/name) for name in ARTIFACTS},
        'evidence': products,
    }
    (output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    result = run()
    print(json.dumps({'audit_programs':len(result['checks']),
                      'general_Einstein_gate':'open',
                      'report':'runs/team48/refinement/report.json'}))
