"""Exhaustive recurrence/growth check of the existing native selection law.

This is a source-only acceptance audit, not a new runtime or physical model.
The fixed three-channel Boolean selector is unchanged. Every possible current
configuration of one three-site x ring is checked, including all ready-memory
and nonready-memory preparations. No retained state is reset during evolution.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from math import lcm
from pathlib import Path

import numpy as np

from universe24.core import Engine
from universe24.system.bundle import canonical_bytes, create_bundle
from universe24.system.decoder import default_protocol, decode_transition, make_transition
from universe24.system.runtime import run_bundle, verify_run
from validation.selection.clocks import build_native_gate, prepare_gate, validate_prepared_state
from validation.selection.complexity import SORT_GATE, episode_gate, structure_trace

ROOT = Path(__file__).resolve().parents[2]
SIDE = 3
DIRECTION = (1, 0, 0)
REPRESENTATIVE = 64  # One y-lane carrier at x=0, ready memory; fixed before search.
PROTOCOL = {
    'law': 'existing selection.SORT_GATE; same tensor for every preparation',
    'population': 'all 512 three-site Boolean ring configurations; all 64 ready-memory cases included',
    'embedding': 'repeat the x ring over all nine y/z lines of a 3x3x3 cube',
    'histories': 'prepare a=F^-1(b); freeze no additional history; retain every carry',
    'carries': '(channel+node) modulo 6',
    'original_window': 24,
    'cycle_window': 'max(24, 4 * exact full-state cycle period)',
    'episodes': 'unchanged selection.complexity strict interior peaks of memory arithmetic events',
    'score': 'unchanged repeated nonuniform axial carrier motifs persistent over adjacent checkpoints',
    'growth': 'unchanged at least four episodes and strict score increase at every successive episode',
    'representative_code': REPRESENTATIVE,
    'selection_after_outcome': False,
    'physical_big_bang_interpretation': 'not_supplied',
}


def ring_bits(code):
    if type(code) is not int or not 0 <= code < 512:
        raise ValueError('one exact nine-bit ring code is required')
    return tuple(tuple((code >> (3*g+x)) & 1 for x in range(3)) for g in range(3))


def ring_step(code):
    """Independent Boolean algebra and explicit periodic shift, no compiler calls."""
    before = ring_bits(code)
    after = [[0]*3 for _ in range(3)]
    for x in range(3):
        memory, moving, local = (before[g][x] for g in range(3))
        following_memory = memory ^ (local * (1-moving))
        after[0][x] = following_memory
        after[1][(x+1) % 3] = moving + following_memory*(local-moving)
        after[2][x] = local + following_memory*(moving-local)
    return sum(after[g][x] << (3*g+x) for g in range(3) for x in range(3))


def embed_ring(code):
    bits = ring_bits(code)
    return np.array([[bits[g][node//9] for node in range(27)]
                     for g in range(3)], dtype=object)


def cycle_decomposition(forward):
    if len(forward) != 512 or set(forward) != set(range(512)):
        raise ValueError('the complete 512-state map must be a permutation')
    visited, cycles = set(), []
    for initial in range(512):
        if initial in visited:
            continue
        cycle, current = [], initial
        while current not in visited:
            cycle.append(current)
            visited.add(current)
            current = forward[current]
        if current != initial:
            raise ValueError('a reversible permutation cannot have a transient basin')
        cycles.append(cycle)
    return cycles


def _trace(initial, steps, forward, scores, counts):
    current = initial
    structure, events = [{'score': 0}], []
    for _ in range(steps):
        events.append(counts[current])
        current = forward[current]
        structure.append({'score': scores[current]})
    return episode_gate(structure, events), events


def audit(out=None):
    law = build_native_gate(SORT_GATE, direction=DIRECTION, name='selection')
    assert law.G == 3 and max(term.degree for term in law.monomials) <= 3
    assert not law.support_violations()
    assert all(factor.offset[1:] == (0, 0)
               for term in law.monomials for factor in term.factors)
    engine = Engine(law)
    forward = [ring_step(code) for code in range(512)]
    cycles = cycle_decomposition(forward)
    inverse = {following: before for before, following in enumerate(forward)}
    period = {code: len(cycle) for cycle in cycles for code in cycle}
    values = [embed_ring(code) for code in range(512)]
    carries = np.array([[(channel+node) % 6 for node in range(27)]
                        for channel in range(3)], dtype=object)
    scores, counts = {}, {}
    representative_seed = None
    for code in range(512):
        seed = prepare_gate(SORT_GATE, values[code], SIDE, DIRECTION, remainders=carries)
        assert np.array_equal(seed.a, values[inverse[code]])
        validate_prepared_state(seed, SORT_GATE, DIRECTION)
        after = engine.step(seed)
        assert np.array_equal(after.a, values[code])
        assert np.array_equal(after.b, values[forward[code]])
        assert np.array_equal(after.r, carries)
        assert engine.inverse_step(after).same_as(seed)
        assert sum(int(x) for x in seed.b[1:].flat) == sum(int(x) for x in after.b[1:].flat)
        records = decode_transition(make_transition(law, seed, after,
                                    run_id='native-cycle-audit', step=1), law)
        counts[code] = sum(record['channel'] == 0 for record in records)
        # Independent definition of canonical memory activity: nonzero ell and
        # changed complete triple. r is unchanged, but not discarded.
        old, now, nxt = ring_bits(inverse[code]), ring_bits(code), ring_bits(forward[code])
        expected_count = 9*sum(old[0][x]+nxt[0][x] != 0 and
                              (old[0][x] != now[0][x] or now[0][x] != nxt[0][x])
                              for x in range(3))
        assert counts[code] == expected_count
        scores[code] = structure_trace([values[inverse[code]], values[code]],
                                      SIDE, DIRECTION)[1]['score']
        if code == REPRESENTATIVE:
            representative_seed = seed

    rows = []
    for code in range(512):
        original, _ = _trace(code, 24, forward, scores, counts)
        recurrent, _ = _trace(code, max(24, 4*period[code]), forward, scores, counts)
        rows.append({'code': code, 'ready_memory': code & 7 == 0,
                     'exact_period': period[code], 'original_window': original,
                     'complete_cycle_window': recurrent})
    recurrent_rows = [row for row in rows if row['complete_cycle_window']['at_least_four']]
    # This is an explanatory witness extracted from the COMPLETE population,
    # not a replacement for its verdict or a tuned new growth experiment.
    witness = recurrent_rows[0] if recurrent_rows else None
    # A complete-period score repeats. Periodic state recurrence is not
    # sustained monotone growth, even if genuine event peaks keep recurring.
    for cycle in cycles:
        twice = [scores[c] for c in cycle]*2
        assert twice[:len(cycle)] == twice[len(cycle):]
    representative_steps = max(24, 4*period[REPRESENTATIVE])
    representative_gate, representative_counts = _trace(
        REPRESENTATIVE, representative_steps, forward, scores, counts)
    current = representative_seed
    recurrence_ticks = []
    for tick in range(1, representative_steps+1):
        previous = current
        current = engine.step(current)
        assert engine.inverse_step(current).same_as(previous)
        if tick % period[REPRESENTATIVE] == 0:
            assert current.same_as(representative_seed)
            recurrence_ticks.append(tick)
    assert engine.rewind(current, representative_steps).same_as(representative_seed)

    changed_history = representative_seed.copy()
    changed_history.a[0, 0] += 1
    try:
        validate_prepared_state(changed_history, SORT_GATE, DIRECTION)
    except ValueError:
        wrong_history_rejected = True
    else:
        raise AssertionError('equal current readings silently admitted a different history')
    # Wrong-history runs are still reversible. Reversibility is not this
    # prepared-domain theorem and must not be used to override its rejection.
    assert engine.inverse_step(engine.step(changed_history)).same_as(changed_history)

    channels = [{'index': i, 'name': gear.name, 'label': gear.label,
                 'owner': 'native_selection_control',
                 'purpose': 'retained Boolean carrier/memory; no Einstein source identification'}
                for i, gear in enumerate(law.gears)]
    bundle = create_bundle(law, representative_seed, channels=channels,
                           protocol=default_protocol(),
                           model={'id': 'native-selection-cycle-control', 'version': '1',
                                  'domain': 'prepared Boolean selector, periodic three-site x ring'})
    saved = None
    witness_saved = None
    witness_bundle = None
    if witness is not None:
        witness_seed = prepare_gate(SORT_GATE, values[witness['code']], SIDE,
                                    DIRECTION, remainders=carries)
        witness_bundle = create_bundle(law, witness_seed, channels=channels,
                                       protocol=default_protocol(),
                                       model={'id': 'native-selection-recurrent-witness', 'version': '1',
                                              'domain': 'explanatory witness from exhaustive Boolean population'})
    if out is not None:
        out = Path(out)
        if out.exists() and any(out.iterdir()):
            raise ValueError('fresh burst-growth output directory required')
        out.mkdir(parents=True, exist_ok=True)
        saved = run_bundle(bundle, out/'representative-run', steps=representative_steps)
        verify_run(out/'representative-run')
        if witness is not None:
            witness_saved = run_bundle(witness_bundle, out/'recurrent-witness-run',
                                       steps=max(24, 4*period[witness['code']]))
            verify_run(out/'recurrent-witness-run')

    histogram = Counter(len(cycle) for cycle in cycles)
    population = {}
    for name, sample in (('all_prepared_memory', rows),
                         ('ready_memory', [row for row in rows if row['ready_memory']])):
        population[name] = {'count': len(sample)}
        for window in ('original_window', 'complete_cycle_window'):
            statuses = Counter(row[window]['status'] for row in sample)
            population[name][window] = {status: statuses[status]
                                       for status in ('passed', 'failed', 'blocked')}
    files = ('validation/system_acceptance/burst_growth.py',
             'validation/selection/clocks.py', 'validation/selection/complexity.py')
    report = {
        'schema': 'universe24/system-acceptance/burst-growth/1', 'protocol': PROTOCOL,
        'tensor_hash': law.fingerprint, 'bundle_id': bundle.bundle_id,
        'seed_hash': hashlib.sha256(canonical_bytes(representative_seed.to_dict())).hexdigest(),
        'run_id': saved['run_id'] if saved is not None else None,
        'channels': 3, 'retained_integers_per_node': 9, 'actual_nodes': 27,
        'maximum_retained_integer_bits': 3, 'all_six_carry_classes': True,
        'exhaustive_ring_states': 512, 'independent_complete_register_comparisons': 512*3*3*27,
        'cycle_count': len(cycles), 'cycle_length_histogram': dict(sorted(histogram.items())),
        'maximum_ring_period': max(histogram),
        'whole_3_cube_period_divides': lcm(*histogram),
        'whole_cube_argument': 'Nine independent x rings; each ring follows this exhaustive permutation.',
        'population_results': population, 'rows': rows,
        'recurrent_peak_preparation_count': len(recurrent_rows),
        'recurrent_witness': None if witness is None else {
            **witness, 'selection': 'lowest numeric qualifying code; explanatory exhaustive-population witness',
            'bundle_id': witness_bundle.bundle_id,
            'run_id': witness_saved['run_id'] if witness_saved is not None else None,
            'saved_run': witness_saved},
        'representative': {'code': REPRESENTATIVE, 'period': period[REPRESENTATIVE],
                           'steps': representative_steps, 'complete_recurrence_ticks': recurrence_ticks,
                           'memory_event_counts': representative_counts, 'growth': representative_gate,
                           'full_rewind': True},
        'negative_controls': {'wrong_old_history_rejected_despite_same_current': wrong_history_rejected,
                              'wrong_history_still_reversible': True,
                              'periodic_scores_not_accumulated': True},
        'gates': {
            'exact_native_state_oracle_inverse_and_replay': 'passed',
            'recurrent_memory_event_peaks': 'passed' if recurrent_rows else 'blocked',
            'preselected_single_pulse_strict_peaks': 'passed' if representative_gate['at_least_four'] else 'blocked',
            'predeclared_structural_growth': 'passed' if any(row['complete_cycle_window']['strict_growth']
                                                          for row in rows) else 'failed',
            'indefinite_strict_growth_on_this_finite_boolean_domain': 'impossible_by_recurrence',
            'physical_cosmological_bursts': 'not_identified',
            'one_tensor_join_to_einstein_matter_metric': 'not_supplied'},
        'physical_acceptance': 'not_established',
        'scope': 'Exhaustive replicated three-site-ring preparations only. The periodicity theorem extends to the whole Boolean cube; the finite-window search does not exhaust all nonuniform cube preparations. No no-growth claim for other unbounded-integer laws.',
        'source_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
        'saved_run': saved,
    }
    if out is not None:
        (out/'burst-growth.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    result = audit(args.out)
    print(json.dumps({key: result[key] for key in
                     ('tensor_hash', 'cycle_length_histogram', 'population_results', 'gates')}, indent=2))


if __name__ == '__main__':
    main()
