"""Same-phase-tensor controls for optical darkness, localization and clicks.

These are candidate falsifiers, not a particle classifier. The click observer
reads only saved clicks; latent-state diagnostics are kept in a separate audit
and never feed evolution or the click observer.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine, State, exact_json
from universe24.core.symmetry import CONTRACT
from universe24.light import electromagnetic_fields, orientations
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol, summarize_clicks
from universe24.system.runtime import run_bundle, verify_run, _source_hashes as runtime_sources
from validation.light_link_resonance import PARTNER, build_tensor, force_oracle, prepare, read_states
from validation.system_smoke import scalar_step

ROOT = Path(__file__).resolve().parents[1]
PARAMETERS = dict(gradient=3, spring=3, optical=0, backreaction=False, phase_gate=True)


def source_hashes():
    paths = ('validation/matter_dark_audit.py', 'validation/light_link_resonance.py',
             'validation/system_smoke.py', 'universe24/light.py')
    return {**{'universe24/' + p: h for p, h in runtime_sources().items()},
            **{p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}}


def prepare_case(name):
    allowed = ('vacuum', 'clock', 'clock-light', 'local-contrast',
               'local-contrast-light', 'local-pulse')
    if name not in allowed:
        raise ValueError('unknown registered case')
    light = name in ('clock-light', 'local-contrast-light')
    seed, metadata = prepare(L=5, bias=32, amplitude=int(light), paused_history=True)
    g, h = metadata['carrier_pair']
    center = seed.lattice.index(2, 2, 2)
    if name == 'vacuum':
        seed = State(5, np.full((48, 125), 32, dtype=object),
                     np.full((48, 125), 32, dtype=object), np.ones((48, 125), dtype=int))
    if name.startswith('local-contrast'):
        # Change the central contrast, preserving the initial optical pair sum.
        seed.b[g, center] += 1
        seed.b[h, center] -= 1
    if name == 'local-pulse':
        # A point profile in both histories preserves the matched move/hold phase.
        for channel in (g, h):
            seed.a[channel, center] += 1
            seed.b[channel, center] += 1
    metadata.update(audit_case=name, perturbation_node=center,
                    readout='central contrasts and pair sums are latent audit variables, not particle labels')
    tensor = build_tensor(**PARAMETERS)
    return create_bundle(tensor, seed,
                         channels=[{'index': g, 'name': gear.name, 'label': gear.label,
                                    'owner': 'phase-matter-dark-controls',
                                    'purpose': 'complete regular node amplitude; no assigned particle species'}
                                   for g, gear in enumerate(tensor.gears)],
                         protocol=default_protocol(),
                         model={'id': 'phase-matter-dark-controls', 'version': '1',
                                'role': 'research', 'symmetry': CONTRACT,
                                'domain': 'finite same-tensor contrast and pulse controls',
                                'parameters': PARAMETERS, 'preparation': metadata,
                                'scope': 'no mass, dark-matter, detector or gravity acceptance'})


def click_observer(path):
    """Only clicks enter this function; no state, field or metric is available."""
    with gzip.open(Path(path) / 'clicks.jsonl.gz', 'rt') as stream:
        records = [exact_json.loads(line) for line in stream]
    result = summarize_clicks(records)
    counts = Counter(record['step'] for record in records)
    result['events_by_recorded_step'] = {str(t): n for t, n in sorted(counts.items())}
    result['active_channel_addresses'] = sorted({record['channel'] for record in records})
    result['physical_species'] = None
    result['source'] = 'canonical arithmetic clicks only; step and node are recorded addresses'
    return result


def central_contrasts(state):
    b = state.b.astype(object)
    return b - b[list(PARTNER)]


def centered_divergence(state, vector):
    """Unscaled centered difference; a nonzero value falsifies this constraint."""
    divergence = np.zeros(state.N, dtype=object)
    for axis in range(3):
        direction = tuple(int(i == axis) for i in range(3))
        plus = state.lattice.shift_index(direction)
        minus = state.lattice.shift_index(tuple(-v for v in direction))
        divergence += vector[axis, plus] - vector[axis, minus]
    return divergence


def latent_audit(path, bundle):
    verified = verify_run(path)
    engine = Engine(bundle.tensor)
    states = [state for _, state in read_states(path, bundle.seed)]
    name = bundle.model['preparation']['audit_case']
    fields = [electromagnetic_fields(state) for state in states]
    first_nonpositive = None
    samples = []
    for tick, state in enumerate(states):
        if tick:
            previous = states[tick - 1]
            if not state.same_as(force_oracle(previous, **PARAMETERS)):
                raise AssertionError('independent pair-force oracle mismatch')
            if tick <= 2 and not state.same_as(scalar_step(bundle.tensor, previous)):
                raise AssertionError('independent scalar oracle mismatch')
            if not engine.inverse_step(state).same_as(previous):
                raise AssertionError('inverse failed')
        for bank in ('a', 'b', 'r'):
            values = getattr(state, bank)
            bad = np.argwhere(values < 1)
            if first_nonpositive is None and len(bad):
                channel, node = map(int, bad[0])
                first_nonpositive = dict(tick=tick, bank=bank, channel=channel,
                                         node=node, value=str(values[channel, node]))
        electric, magnetic = fields[tick]
        norm = sum(int(v) ** 2 for vector in (electric, magnetic) for v in vector.flat)
        samples.append({'tick': tick, 'em_readout_squared_norm': str(norm),
                        'max_abs_central_contrast': str(max(abs(int(v)) for v in central_contrasts(state).flat)),
                        'nonzero_centered_div_e_nodes': int(np.count_nonzero(centered_divergence(state, electric))),
                        'nonzero_centered_div_b_nodes': int(np.count_nonzero(centered_divergence(state, magnetic)))})
    if not engine.rewind(states[-1], verified['steps']).same_as(bundle.seed):
        raise AssertionError('complete rewind failed')
    return {'case': name, 'run_id': verified['run_id'], 'tensor_hash': verified['tensor_hash'],
            'steps': verified['steps'], 'complete_replay_and_inverse': 'passed',
            'independent_force_oracle_all_steps': 'passed', 'scalar_oracle_first_two_steps': 'passed',
            'channels': 48, 'retained_integers_per_node': 144,
            'maximum_integer_bits': max(verified['maximum_integer_bits_by_step']),
            'strict_naturals': 'passed' if first_nonpositive is None else 'failed',
            'first_nonpositive': first_nonpositive, 'samples': samples}, states, fields


def collect(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    sources = source_hashes()
    cases, histories, field_histories = {}, {}, {}
    schedule = (('vacuum', 8), ('clock', 8), ('clock-light', 8),
                ('local-contrast', 4), ('local-contrast-light', 4), ('local-pulse', 8))
    for name, steps in schedule:
        bundle = prepare_case(name)
        destination = out / name
        run_bundle(bundle, destination, steps)
        audit, states, fields = latent_audit(destination, bundle)
        cases[name] = {'observer': click_observer(destination), 'latent_audit': audit}
        histories[name], field_histories[name] = states, fields
        print(f'{name}: {steps} steps; clicks={cases[name]["observer"]["events"]}; naturals={audit["strict_naturals"]}', flush=True)

    hashes = {case['latent_audit']['tensor_hash'] for case in cases.values()}
    if len(hashes) != 1:
        raise AssertionError('registered cases changed the tensor')
    for name in ('vacuum', 'clock', 'local-contrast'):
        if any(sample['em_readout_squared_norm'] != '0' for sample in cases[name]['latent_audit']['samples']):
            raise AssertionError('EM-dark control became optically visible')
    if cases['vacuum']['observer']['events'] or not cases['clock']['observer']['events']:
        raise AssertionError('clock/click negative control changed')

    no_optical_backreaction = all(
        np.array_equal(central_contrasts(dark), central_contrasts(light))
        for dark_name, light_name in (('clock', 'clock-light'), ('local-contrast', 'local-contrast-light'))
        for dark, light in zip(histories[dark_name], histories[light_name]))
    optical_effect = any(not all(np.array_equal(a, b) for a, b in zip(dark_fields, baseline_fields))
                         for dark_fields, baseline_fields in zip(field_histories['local-contrast-light'],
                                                                 field_histories['clock-light']))
    if not no_optical_backreaction or not optical_effect:
        raise AssertionError('registered one-way contrast coupling changed')

    pulse = field_histories['local-pulse']
    pulse_moves_exactly = all(all(np.array_equal(field, np.roll(initial.reshape(3, 5, 5, 5),
                                                               (tick + 1) // 2, axis=1).reshape(3, -1))
                                 for field, initial in zip(fields, pulse[0]))
                             for tick, fields in enumerate(pulse))
    pulse_stationary = all(all(np.array_equal(field, initial) for field, initial in zip(fields, pulse[0]))
                           for fields in pulse)
    if not pulse_moves_exactly or pulse_stationary:
        raise AssertionError('localized pulse transport control changed')

    tensor = prepare_case('clock').tensor
    pair_factorization = all(factor.gear in (term.target, PARTNER[term.target])
                             for term in tensor.monomials for factor in term.factors)
    axis_factorization = all(all(factor.offset[k] == 0 for k in range(3)
                                 if orientations()[term.target][0][k] == 0)
                             for term in tensor.monomials for factor in term.factors)
    if not pair_factorization or not axis_factorization:
        raise AssertionError('central-pair/axial factorization changed')
    if any(cases[name]['latent_audit']['first_nonpositive'] is None
           for name in ('local-contrast', 'local-contrast-light')):
        raise AssertionError('localized contrast instability control changed')

    result = {'schema': 'universe24/matter-dark-audit/1', 'source_hashes': sources,
              'cases': cases,
              'same_tensor': {'status': 'passed', 'hash': next(iter(hashes)),
                              'central_pair_blocks': 24, 'no_transverse_or_cross_pair_terms': True},
              'measured_comparisons': {'dark_contrast_changes_optical_evolution': optical_effect,
                                       'optical_pulse_changes_contrast_evolution': not no_optical_backreaction,
                                       'local_common_pulse_translates_exactly': pulse_moves_exactly,
                                       'local_common_pulse_is_stationary': pulse_stationary},
              'gates': {'em_dark_internal_activity': 'passed',
                        'em_dark_activity_produces_arithmetic_clicks': 'passed',
                        'light_to_contrast_backreaction': 'failed',
                        'tested_local_contrast_natural_domain': 'failed',
                        'tested_point_pulse_as_stationary_rest_object': 'failed',
                        'positive_rest_mass_and_dispersion': 'not_tested',
                        'cold_matter_equation_of_state': 'not_tested',
                        'gravitational_stress_source_and_clustering': 'not_tested',
                        'operational_particle_classifier_from_clicks': 'not_tested',
                        'ordinary_matter_acceptance': 'blocked', 'dark_matter_acceptance': 'blocked'},
              'interpretation': 'One tensor, separate prepared controls. EM cancellation and arithmetic activity are not dark-matter evidence. The installed light-memory tensor is a different law and cannot close these gates.'}
    if sources != source_hashes():
        raise AssertionError('an audit dependency changed during collection')
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    result = collect(parser.parse_args().out)
    print(json.dumps({'gates': result['gates'], 'cases': len(result['cases'])}, indent=2))
