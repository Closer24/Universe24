"""Execute declared controls through one runtime without pooling physical claims.

The massless native solution, massive spinor candidate and finite selector are
different immutable laws. This fixed validation sequence reports their exact
identities, scoped successes and failed/missing joint acceptance conditions.
It is excluded from the installed package and supplies no default universe.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import gzip
import hashlib
import json
from pathlib import Path

from universe24.core import State, exact_json
from universe24.system.bundle import canonical_bytes, load_bundle
from universe24.system.runtime import run_bundle, verify_run

ROOT = Path(__file__).resolve().parents[2]


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def source_hashes():
    # Include indirect prepared-tensor, locality and scalar-oracle dependencies,
    # not just the packages whose public entrypoints happen to be invoked here.
    # This is the repository-owned Python closure; external libraries are not
    # authenticated by these hashes and receipt equality is not a proof token.
    paths = sorted(path for package in ('universe24', 'validation')
                   for path in (ROOT / package).rglob('*.py')
                   if 'tests' not in path.relative_to(ROOT).parts)
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths}


@dataclass(frozen=True)
class RunReceipt:
    """Compatibility receipt from replayed bytes, not an authentication token."""
    run_id: str
    bundle_id: str
    tensor_sha256: str
    seed_sha256: str
    model_sha256: str
    protocol_sha256: str
    channels_sha256: str
    trace_sha256: str
    clicks_sha256: str
    current_source_sha256: str
    steps: int
    channels: int
    nodes: int


def inspect_saved_run(path):
    """Recompute complete evolution/clicks before issuing a scoped receipt."""
    path = Path(path)
    report = verify_run(path)
    bundle = load_bundle(path / 'bundle')
    if any(report['acceptance_gates'][key]['status'] != 'not_tested' for key in 'CDEF'):
        raise ValueError('Generic runtime must not promote physical acceptance')
    receipt = RunReceipt(
        report['run_id'], bundle.bundle_id, bundle.tensor.fingerprint,
        digest(bundle.seed.to_dict()), digest(bundle.model), digest(bundle.protocol),
        digest(list(bundle.channels)), report['files']['full_trace.jsonl.gz'],
        report['files']['clicks.jsonl.gz'], digest(source_hashes()),
        report['steps'], bundle.tensor.G, bundle.seed.N)
    return receipt, report


def require_same_run(left, right):
    """No cross-law, cross-seed, cross-readout or cross-horizon evidence joins."""
    if type(left) is not RunReceipt or type(right) is not RunReceipt:
        raise TypeError('RunReceipt objects required; equality checks compatibility, not authentication')
    if left != right:
        raise ValueError('Different complete runs or interpretations cannot supply one physical certificate')
    return True


def _massive_run(out):
    from validation.unified_law import common, constrained_coordinates, independent_review
    from validation.unified_law.clock_acceptance import same_candidate_audit

    data = common.trace()
    bundle = common.make_bundle(data['program'], data['seed'])
    path = Path(out) / 'run'
    run_bundle(bundle, path, 3)
    receipt, execution = inspect_saved_run(path)
    with gzip.open(path / 'full_trace.jsonl.gz', 'rt', encoding='utf-8') as stream:
        rows = [exact_json.loads(line) for line in stream]
    if len(rows) != 3:
        raise AssertionError('Missing declared massive-candidate transitions')
    for index, row in enumerate(rows):
        before, after = (State.from_dict(row[key]) for key in ('before', 'after'))
        if not before.same_as(data['states'][index]) or not after.same_as(data['states'][index + 1]):
            raise AssertionError('Runtime differs from independent complete-state trajectory')
        oracle = independent_review.scalar_step_oracle(data['program'], before)
        if not after.same_as(oracle):
            raise AssertionError('Independent massive scalar oracle failed')
    source = constrained_coordinates.symbolic_audit()
    source_match = constrained_coordinates.source_builder_audit()
    wrong = independent_review.wrong_dynamics_audit()
    refinement = same_candidate_audit()
    if (refinement['shared_default_tensor_sha256'] != receipt.tensor_sha256
            or refinement['shared_default_seed_sha256'] != receipt.seed_sha256):
        raise AssertionError('Default runtime and clock/source audit identities differ')
    if not all(row['wrong_dynamics_rejected'] for row in wrong):
        raise AssertionError('Constraint-only false acceptance control was lost')
    return {'receipt': asdict(receipt), 'execution': execution,
            'same_saved_state_constraint': 'exactly_zero', 'source_pushforward': source,
            'full44_source_match': source_match, 'wrong_dynamics_controls': wrong,
            'clock_and_refinement': refinement,
            'scope': 'Homogeneous expanding massive scalar plus dust; finite-time approximation.'}, receipt


def _ledger(native, massive, bursts):
    """Decisions attach to specific constructions; they are not runtime modes."""
    return [
        {'idea': 'fixed_rule3_complete_state_runtime', 'decision': 'accepted_runtime',
         'evidence': 'Every declared saved run is replayed, inverted and canonically decoded by universe24.system.runtime.'},
        {'idea': 'native_massless_scalar_dust_flrw', 'decision': 'accepted_scoped',
         'tensor_sha256': native['runs'][0]['tensor_sha256'],
         'evidence': 'Five fresh saved runs, source/domain guards and exact physical endpoint comparison.',
         'scope': 'Expanding homogeneous massless chart; no material detector or singularity crossing.'},
        {'idea': 'massive_spinor_constraint_and_source', 'decision': 'accepted_scoped',
         'tensor_sha256': massive['receipt']['tensor_sha256'],
         'evidence': 'Exact decoder constraint, physical pushforward, saved trajectory and independent source/clock refinement.',
         'scope': 'Homogeneous massive approximation with bounded stated finite-time proof domain.'},
        {'idea': 'constraint_identity_alone_certifies_dynamics', 'decision': 'rejected',
         'evidence': 'Wrong scalar and metric drifts retain zero constraint but fail physical equations.'},
        {'idea': 'exact_massive_dust_mass_at_finite_step', 'decision': 'rejected',
         'evidence': massive['clock_and_refinement']['exact_discrete_dust_mass_conservation']},
        {'idea': 'scalar_phase_is_universal_proper_time', 'decision': 'rejected',
         'evidence': massive['clock_and_refinement']['universal_scalar_phase_over_mass_as_proper_time']},
        {'idea': 'efficient_massive_long_time_encoding', 'decision': 'blocked',
         'evidence': massive['clock_and_refinement']['efficient_refinement_bit_cost']},
        {'idea': 'native_selector_recurrent_memory_activity', 'decision': 'accepted_scoped',
         'run_id': bursts['recurrent_witness']['run_id'],
         'evidence': bursts['gates']['recurrent_memory_event_peaks'],
         'scope': 'The separately replayed recurrent witness; not cosmological bursts or growing complexity.'},
        {'idea': 'native_selector_sustained_structural_growth', 'decision': 'rejected',
         'evidence': bursts['gates']['predeclared_structural_growth'],
         'scope': 'Exhaustive declared finite Boolean preparation domain, not a universal no-growth theorem.'},
        {'idea': 'combine_positive_results_from_different_tensors', 'decision': 'rejected',
         'evidence': 'Actual saved receipts reject cross-law joins and different complete preparations.'},
        {'idea': 'one_spatial_einstein_detector_burst_growth_law', 'decision': 'blocked',
         'evidence': 'No supplied immutable tensor jointly certifies spatial geometry, operational apparatus and sustained burst-to-burst growth.'},
        {'idea': 'born_measure_and_physical_bell_from_arithmetic_clicks', 'decision': 'blocked',
         'evidence': 'Canonical clicks remain passive arithmetic records; no new outcome-measure derivation is supplied.'},
    ]


def run(out):
    """Fixed source acceptance pipeline, with no model-selection argument."""
    out = Path(out)
    if out.exists():
        raise ValueError('Acceptance output must be a new directory')
    initial_sources = source_hashes()
    out.mkdir(parents=True)
    from validation.sourced_map.runtime import run_audit
    from . import burst_growth

    native = run_audit(out / 'massless')
    massive, massive_receipt = _massive_run(out / 'massive')
    bursts = burst_growth.audit(out / 'bursts')
    native_receipt, _ = inspect_saved_run(out / 'massless/N24')
    repeated_receipt, _ = inspect_saved_run(out / 'massless/N24')
    require_same_run(native_receipt, repeated_receipt)
    changed_receipt, _ = inspect_saved_run(out / 'massless/changed-carry')
    burst_receipt, _ = inspect_saved_run(out / 'bursts/representative-run')
    recurrent_receipt, _ = inspect_saved_run(out / 'bursts/recurrent-witness-run')
    if (bursts['run_id'] != burst_receipt.run_id
            or bursts['bundle_id'] != burst_receipt.bundle_id
            or bursts['seed_hash'] != burst_receipt.seed_sha256
            or bursts['tensor_hash'] != burst_receipt.tensor_sha256
            or bursts['recurrent_witness']['run_id'] != recurrent_receipt.run_id
            or bursts['recurrent_witness']['bundle_id'] != recurrent_receipt.bundle_id):
        raise ValueError('Burst claims do not identify their actual saved runs')
    if (bursts['gates']['recurrent_memory_event_peaks'] != 'passed'
            or bursts['gates']['predeclared_structural_growth'] != 'failed'):
        raise ValueError('Declared burst/growth acceptance contract changed')
    negative = {}
    for name, other in (('massless_vs_massive', massive_receipt),
                        ('massless_vs_native_selector', burst_receipt),
                        ('same_fields_changed_retained_carry', changed_receipt)):
        try:
            require_same_run(native_receipt, other)
        except ValueError as error:
            negative[name] = {'status': 'rejected', 'reason': str(error)}
        else:
            raise AssertionError('Invalid physical evidence join accepted: ' + name)
    try:
        require_same_run(burst_receipt, recurrent_receipt)
    except ValueError as error:
        negative['same_selector_different_preparation'] = {'status': 'rejected', 'reason': str(error)}
    else:
        raise AssertionError('Distinct pulse and recurrent preparations were conflated')
    final_sources = source_hashes()
    if initial_sources != final_sources:
        raise ValueError('Sources changed during the acceptance run')
    evidence = {'massless': native, 'massive': massive, 'bursts': bursts}
    files = {}
    for name, report in evidence.items():
        path = out / (name + '.json')
        path.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n', encoding='utf-8')
        files[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    result = {
        'schema': 'universe24/system-acceptance/1',
        'execution_interface': 'universe24.system.runtime.run_bundle / verify_run',
        'software_execution': 'passed',
        'research_constructions_are_one_physical_law': False,
        'general_physical_acceptance': 'blocked',
        'same_law_recurrent_bursts_and_growth': 'not_established',
        'default_physical_model': 'none',
        'source_sha256': final_sources, 'evidence_sha256': files,
        'representative_receipts': {'massless': asdict(native_receipt),
                                    'massive': asdict(massive_receipt),
                                    'native_selector': asdict(burst_receipt),
                                    'native_selector_recurrent_witness': asdict(recurrent_receipt)},
        'same_run_join': 'passed for independent replay of the same saved bytes',
        'rejected_cross_run_joins': negative,
        'idea_ledger': _ledger(native, massive, bursts),
        'scope': 'One implementation and validation entry point, several explicitly separate research laws. Success is evidence reproduction, including failed and blocked physical gates.'}
    (out / 'acceptance.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    return result
