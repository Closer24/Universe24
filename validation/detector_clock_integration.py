"""Same-law negative control for phase-gated light plus retained detection.

The candidate is T_phase + T_detector - T_light, with one shared set of 48
channels. Component successes do not certify this sum or Einstein physics.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.algebra.group_2o import group
from universe24.core import Engine, State, Tensor, exact_json
from universe24.core.symmetry import CONTRACT, require_equivariant
from universe24.detection import (
    ARM_PORT, MEMORY_PORT, SELECTOR_PORT, detector_tensor, energy_account,
    make_detector_bundle, observe_detector_run, roles, sector_map,
)
from universe24.light import electromagnetic_fields, light_tensor, orientations
from universe24.node import NodeView
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.light_link_resonance import PAIRS, PARTNER, build_tensor, prepare
from validation.system_smoke import scalar_step

ROOT = Path(__file__).resolve().parents[1]


def phase_tensor():
    return build_tensor(phase_gate=True)


def combined_tensor():
    """Substitute phase transport for the detector's free transport terms."""
    phase = phase_tensor()
    terms = []
    for law, weight in ((phase, 1), (detector_tensor(), 1), (light_tensor(), -1)):
        for monomial in law.monomials:
            terms.append((monomial.target, weight * monomial.coeff,
                          [(f.gear, f.offset, f.field) for f in monomial.factors]))
    candidate = Tensor(phase.gears, terms, strict_support=True)
    require_equivariant(candidate)
    return candidate


def input_oracle(state, kind):
    """Direct independently grouped input, not a Tensor/Engine evaluator."""
    b = state.b.astype(object)
    free = np.zeros_like(b)
    phase = np.zeros_like(b)
    detection = np.zeros_like(b)
    multiplication = group().multiplication
    for g, (direction, _, _) in enumerate(orientations()):
        plus = state.lattice.shift_index(direction)
        minus = state.lattice.shift_index(tuple(-v for v in direction))
        contrast = b[g] - b[PARTNER[g]]
        free[g] = 3 * (b[g, minus] + b[g, plus])
        phase[g] = 3 * (b[PARTNER[g]] + b[g, plus]
                        + contrast**2 * (b[g, minus] - b[g, plus]))
        memory, arming, selector = (multiplication[g][p]
                                    for p in (MEMORY_PORT, ARM_PORT, SELECTOR_PORT))
        detection[g] += free[g] * (1 - b[selector]) + 6 * b[selector] * b[g]
        detection[g] += 3 * b[arming] * (b[memory] - b[g, minus])
        detection[memory] += 3 * b[arming] * (b[g, minus] - b[memory])
        detection[g] += 3 * b[arming] * (b[memory, plus] - b[g, plus])
        detection[memory] += 3 * b[arming, minus] * (b[g] - b[memory])
    return {'phase': phase, 'detector': detection,
            'combined': phase + detection - free}[kind]


def step_oracle(state, kind):
    numerator = 2 * input_oracle(state, kind) + state.r
    return State(state.L, state.b, numerator // 6 - state.a, numerator % 6)


def research_bundle(tensor, seed, case):
    return create_bundle(
        tensor, seed,
        channels=[{'index': g, 'name': gear.name, 'label': gear.label,
                   'owner': 'detector-clock-composition-audit',
                   'purpose': 'complete node amplitude with a,b,r; no extra clock or memory bank'}
                  for g, gear in enumerate(tensor.gears)],
        protocol=default_protocol(),
        model={'id': 'universe24/detector-clock-composition-audit', 'version': '1',
               'role': 'research', 'symmetry': CONTRACT, 'case': case,
               'domain': 'registered component preparations and their explicit naive-composition countercontrols',
               'scope': 'not an accepted combined detector/geometry/matter law'})


def states_from_run(path, seed):
    yield 0, seed
    with gzip.open(Path(path) / 'full_trace.jsonl.gz', 'rt') as stream:
        for tick, line in enumerate(stream, 1):
            yield tick, State.from_dict(exact_json.loads(line)['after'])


def detector_sector(state):
    """Declared installed detector invariant, used only as validation."""
    try:
        expected_previous = sector_map(state.b, state.L, 0, inverse=True)
    except ValueError:
        return False
    return np.array_equal(state.a, expected_previous)


def phase_clock_sector(state, tick):
    q = (1, 0, -1, 0)[tick % 4]
    qa = (0, 1, 0, -1)[tick % 4]
    return all(np.all(state.b[g].astype(object) - state.b[h].astype(object) == q)
               and np.all(state.a[g].astype(object) - state.a[h].astype(object) == qa)
               for g, h in PAIRS)


def inspect(path, bundle, kind, preparation):
    replay = verify_run(path)
    engine = Engine(bundle.tensor)
    initial_e, initial_b = electromagnetic_fields(bundle.seed)
    initial_account = energy_account(bundle.seed, 0)['light_plus_memory']
    previous = None
    first_negative = None
    first_detector_failure = None
    first_phase_failure = None
    first_delay_failure = None
    samples = []
    for tick, state in states_from_run(path, bundle.seed):
        if previous is not None:
            if not state.same_as(step_oracle(previous, kind)):
                raise AssertionError('independent grouped-input mismatch')
            if not state.same_as(scalar_step(bundle.tensor, previous)):
                raise AssertionError('independent scalar-monomial mismatch')
            if not engine.inverse_step(state).same_as(previous):
                raise AssertionError('complete inverse mismatch')
        # This view is topology/validation only, not an operational clock.
        node = NodeView(state, 0)
        if len(node.faces) != 6 or sum(len(port.channels) for port in node.faces) != 48:
            raise AssertionError('six internal faces do not cover the node')
        if any(port.opposite.edge != port.edge for port in node.faces):
            raise AssertionError('neighbor endpoints disagree on adjacency')
        for bank in ('a', 'b', 'r'):
            bad = np.argwhere(getattr(state, bank) < 0)
            if len(bad) and first_negative is None:
                channel, site = map(int, bad[0])
                first_negative = {'tick': tick, 'bank': bank, 'channel': channel,
                                  'node': site, 'value': str(getattr(state, bank)[channel, site])}
        detector_ok = detector_sector(state)
        phase_ok = phase_clock_sector(state, tick)
        if not detector_ok and first_detector_failure is None:
            first_detector_failure = tick
        if not phase_ok and first_phase_failure is None:
            first_phase_failure = tick
        e, b = electromagnetic_fields(state)
        delayed = all(np.array_equal(actual,
            np.roll(initial.reshape(3, state.L, state.L, state.L),
                    (tick + 1) // 2, axis=1).reshape(3, -1))
            for actual, initial in ((e, initial_e), (b, initial_b)))
        if not delayed and first_delay_failure is None:
            first_delay_failure = tick
        account = energy_account(state, 0)
        samples.append({'tick': tick, 'detector_sector': detector_ok,
                        'phase_clock_sector': phase_ok,
                        'delayed_field_translation': delayed,
                        'role_quadratic_account': str(account['light_plus_memory']),
                        'role_account_matches_initial': account['light_plus_memory'] == initial_account,
                        'memory_amplitude_sum': str(sum(int(v) for v in state.b[roles(0)['memory']]))})
        previous = state
    if not engine.rewind(previous, replay['steps']).same_as(bundle.seed):
        raise AssertionError('complete rewind mismatch')
    return {'run_id': replay['run_id'], 'tensor_hash': bundle.tensor.fingerprint,
            'kind': kind, 'preparation': preparation, 'steps': replay['steps'],
            'channels': 48, 'retained_integers_per_node': 144,
            'monomials': len(bundle.tensor.monomials), 'degree': bundle.tensor.rank - 1,
            'model_contract': replay['model_contract'],
            'maximum_integer_bits': max(replay['maximum_integer_bits_by_step']),
            'independent_grouped_and_scalar_oracles_all_steps': 'passed',
            'complete_replay_inverse_rewind': 'passed', 'six_internal_face_views': 'passed',
            'retained_nonnegative': 'passed' if first_negative is None else 'failed',
            'first_negative': first_negative,
            'first_detector_sector_failure': first_detector_failure,
            'first_phase_clock_sector_failure': first_phase_failure,
            'first_delayed_field_failure': first_delay_failure,
            'samples': samples}


def relevant_source_hashes():
    paths = ['validation/detector_clock_integration.py', 'validation/light_link_resonance.py',
             'validation/system_smoke.py', 'universe24/detection.py', 'universe24/light.py',
             'universe24/node.py']
    paths += [str(p.relative_to(ROOT)) for folder in ('core', 'system', 'algebra')
              for p in sorted((ROOT / 'universe24' / folder).glob('*.py'))]
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}


def run(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    source_hashes = relevant_source_hashes()
    installed_detector = make_detector_bundle(L=5, root=0, light_position=0, arm_position=3)
    phase_seed, _ = prepare(L=5, bias=1, paused_history=True)
    phase = phase_tensor()
    combined = combined_tensor()
    panel = [
        ('detector-control', installed_detector, 'detector', 'installed_detector', 8),
        ('phase-control', research_bundle(phase, phase_seed, 'phase-control'), 'phase', 'matched_phase', 8),
        ('combined-detector-preparation', research_bundle(combined, installed_detector.seed,
             'combined-detector-preparation'), 'combined', 'installed_detector', 4),
        ('combined-phase-preparation', research_bundle(combined, phase_seed,
             'combined-phase-preparation'), 'combined', 'matched_phase', 3),
    ]
    cases = {}
    for name, bundle, kind, preparation, horizon in panel:
        run_bundle(bundle, out / name, horizon)
        cases[name] = inspect(out / name, bundle, kind, preparation)
    detector_observation = observe_detector_run(out / 'detector-control')
    if detector_observation['outcomes']['capture'] < 1 or detector_observation['outcomes']['release'] < 1:
        raise AssertionError('registered detector control lacks capture and release')
    if cases['detector-control']['first_detector_sector_failure'] is not None:
        raise AssertionError('native detector control left its own sector')
    if (cases['phase-control']['first_delayed_field_failure'] is not None
            or cases['phase-control']['retained_nonnegative'] != 'passed'):
        raise AssertionError('matched-phase component control failed')
    if any(cases[name]['first_negative'] is None for name in
           ('combined-detector-preparation', 'combined-phase-preparation')):
        raise AssertionError('registered composition negative changed')
    if source_hashes != relevant_source_hashes():
        raise AssertionError('relevant sources changed during integration audit')
    result = {'schema': 'universe24/detector-clock-integration/1',
              'candidate_definition': 'T_phase + T_detector - T_light; no copied second bank',
              'cases': cases, 'source_hashes': source_hashes,
              'detector_control_outcomes': detector_observation['outcomes'],
              'preparation_intersection': {
                  'status': 'empty_for_declared_sectors',
                  'reason': 'Phase q=+/-1 in all24 central pairs requires at least24 occupied channel rows; installed detector admits only4 role rows.'},
              'gates': {'mechanical_admission_oracles_and_rewind': 'passed',
                        'component_controls': 'passed',
                        'naive_same_law_natural_domain': 'failed',
                        'naive_same_law_delayed_detection': 'failed',
                        'accepted_common_clock_detector_coupling': 'blocked',
                        'material_proper_clock': 'not_tested',
                        'matter_dark_matter_and_einstein_source': 'not_tested'},
              'scope': 'Four runs using one Engine; distinct component controls do not repair the failed common candidate. Hidden states are used only for independent validation, not for the click-only observer.'}
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    result = run(parser.parse_args().out)
    print(json.dumps({'gates': result['gates'], 'cases': {
        name: {'steps': case['steps'], 'first_negative': case['first_negative'],
               'bits': case['maximum_integer_bits']} for name, case in result['cases'].items()}}, indent=2))
