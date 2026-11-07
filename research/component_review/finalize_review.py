"""Aggregate completed independent audits and pin the exact reviewed sources."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

from .audit import digest_file

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def main():
    previous = json.loads((HERE/'preservation_before.json').read_text())['files']
    current = {path: digest_file(ROOT/path) for path in previous}
    changed = [path for path in previous if current[path] != previous[path]]
    preservation = {'format': 'universe24-component-review-preservation-v1',
        'passed': not changed, 'files_checked': len(previous), 'core_files': 13,
        'historical_trajectories': 44, 'historical_html_files': 3,
        'changed_files': changed, 'before_sha256': previous, 'after_sha256': current}
    save(HERE/'preservation_after.json', preservation)
    assert not changed, changed
    audits = {}
    for filename in ('baseline_trace_audit.json', 'confirmation_discovery_review.json',
                     'buffer_review.json', 'packet_review.json', 'selection_review.json',
                     'selection_followup_review.json', 'joined_receiver_review.json'):
        report = json.loads((HERE/filename).read_text())
        assert report['passed'], filename
        audits[filename] = {'sha256': digest_file(HERE/filename), 'format': report['format'], 'passed': True}
    baseline = json.loads((HERE/'baseline_trace_audit.json').read_text())
    baseline_source = HERE/'baseline_source/research/component_review/audit.py'
    assert digest_file(baseline_source) == baseline['source_sha256']['research/component_review/audit.py']
    full_suite_path = ROOT/'research/experiments/evidence/assembly_v1/final_checks/unittest_complete.json'
    full_suite = json.loads(full_suite_path.read_text())
    assert full_suite['tests_run'] == full_suite['expected'] == 120
    assert full_suite['successful'] and not any(full_suite[k] for k in ('failures', 'errors', 'skips'))
    test_log = full_suite_path.with_suffix('.log')
    text = test_log.read_text()
    reviewer_tests = sum('test_component_research_review.' in line and ' ... ok' in line
                         for line in text.splitlines())
    assert reviewer_tests == 20
    ui_path = ROOT/'research/experiments/evidence/assembly_v1/presenter_render/report.json'
    ui = json.loads(ui_path.read_text())
    assert ui['passed'] and not ui['errors'] and len(ui['checks']) == 24
    paths = set(ROOT.glob('universe24/**/*.py'))
    for folder in ('research/components', 'research/experiments', 'research/component_review', 'research/reference'):
        paths.update((ROOT/folder).glob('*.py'))
    paths.update(ROOT/p for p in ('AGENTS.md', 'docs/MODEL.md', 'docs/COMPONENT_REVIEW.md',
        'research/presenter/export.py', 'tests/test_component_research_review.py',
        'research/component_review/packet_proof_review.md'))
    hashes = {}
    for path in sorted(paths):
        relative = path.relative_to(ROOT)
        target = HERE/'source'/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        hashes[str(relative)] = digest_file(path)
        assert digest_file(target) == hashes[str(relative)]
    source_manifest = {'format': 'universe24-independent-review-source-v1',
        'checkout_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'reviewed_worktree_sources': hashes, 'new_sources_committed': False,
        'baseline_oracle_snapshot': str(baseline_source.relative_to(ROOT)),
        'baseline_oracle_sha256': digest_file(baseline_source)}
    save(HERE/'source_manifest.json', source_manifest)
    report = {'format': 'universe24-independent-component-review-v1',
        'status': 'scoped_software_and_scientific_evidence_review_complete',
        'review_passed': True, 'all_scientific_targets_passed': False,
        'preservation': {'passed': True, 'files_checked': len(previous), 'core_files_unchanged': 13,
                         'report': 'preservation_after.json', 'sha256': digest_file(HERE/'preservation_after.json')},
        'source_manifest': {'path': 'source_manifest.json', 'sha256': digest_file(HERE/'source_manifest.json'),
                            'archived_source_files': len(hashes)},
        'full_test_suite': {**full_suite, 'report': str(full_suite_path.relative_to(ROOT)),
                            'sha256': digest_file(full_suite_path), 'log_sha256': digest_file(test_log),
                            'independent_review_tests_included': reviewer_tests,
                            'execution_owner': 'code_writer', 'independent_review': 'Explicit result and complete log inspected'},
        'historical_migration': {'experiments': 44, 'complete_states_equal': 1868,
                                'independent_forward_inverse_transitions': 1824},
        'oracle': {'routing': 'Separate exact 4x4-matrix construction',
                   'evolution': 'Independent sparse gather from one old complete state',
                   'uses_production_scalar_or_routing_tables': False},
        'scientific_results': {
            'waiting_confirmation': {'reported_cases': 145, 'reported_runs': 580, 'accepted_cases': 0,
                                     'independent_replayed_runs': 8, 'claim_established': False},
            'guided_packet': {'full_replayed_runs': 6, 'transitions': 106,
                              'finite_sides': [5, 17, 31], 'proof_scope': 'Fixed+++ declared periodic guide and halo, every L>=5',
                              'physical_light_established': False},
            'higher_score_prediction': {'recordings_reobserved': 432, 'scores_recomputed': 18,
                                       'comparisons_recomputed': 243, 'eligible': 10, 'counterexamples': 10,
                                       'oracle_replayed_runs': 20, 'prediction_refuted_in_registered_family': True},
            'fresh_competition': {'recordings_reobserved': 200, 'native_portable_frames': 10600,
                                 'comparisons_recomputed': 96, 'oracle_replayed_runs': 16,
                                 'registered_phase_conditioned_prediction_passed': True,
                                 'input_or_phase_controlled_winner_flip_found': False,
                                 'one_frozen_source_version_per_batch': True},
            'joined_receiver': {'recordings_reobserved_and_replayed': 16, 'frames': 784,
                                'transitions': 768, 'null_controls_passed': 8,
                                'required_active_cases_failed': 6, 'first_C': 12,
                                'C_bearing_updates': 19, 'first_record_loss': 14,
                                'loser_full_node_quiet_both_swaps': True,
                                'single_click_retaining_component_established': False,
                                'one_frozen_source_version_per_batch': True}},
        'audit_reports': audits,
        'rendering_report_review': {'report': str(ui_path.relative_to(ROOT)), 'sha256': digest_file(ui_path),
                                   'selected_experiments': 24, 'passed': True,
                                   'scope': ui['scope'], 'actual_browser_or_ipad_verified': False},
        'limits': ['Valid assembly is not a general functional-composition theorem.',
                   'The580 waiting-search production trajectories were not all replayed independently.',
                   'All selection/followup observations were independently recomputed, but only the declared subsets received a separate dynamics replay.',
                   'No physical-light, physical-time, collapse, energy, autonomous uniqueness-approval or general complexity-law claim.',
                   'No commit, push or remote deployment was performed by this reviewer.'],
        'documentation': 'docs/COMPONENT_REVIEW.md'}
    save(HERE/'report.json', report)
    print(json.dumps({'review_passed': True, 'all_scientific_targets_passed': False,
                      'preserved_files': len(previous), 'full_tests': full_suite['tests_run'],
                      'review_tests': reviewer_tests, 'archived_sources': len(hashes),
                      'report': str((HERE/'report.json').relative_to(ROOT))}))


if __name__ == '__main__':
    main()
