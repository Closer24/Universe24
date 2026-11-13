"""Inspect full canonical saved runs; never feed a diagnostic into evolution."""
from __future__ import annotations

from collections import Counter
import gzip
import json
from pathlib import Path

import numpy as np

from universe24.core import State, exact_json
from universe24.system.bundle import load_bundle
from universe24.system.runtime import run_bundle, verify_run
from .model import make_bundle, ideal, optical_matrix, curl, tensor


def _planes(state):
    result = []
    for bank in (state.a, state.b, state.r):
        full = bank.reshape(18, state.L, state.L * state.L)
        plane = full[:, :, 0]
        if not np.all(full == plane[:, :, None]):
            raise ValueError('Saved field is not plane symmetric')
        result.append(np.asarray(plane, dtype=object))
    return result


def _ledger(state):
    # Same exact invariant as the original experiment, evaluated on FULL arrays.
    p = np.asarray(state.b, dtype=object)
    C = optical_matrix(p)
    D, B = p[:3], p[3:6]
    CD = np.asarray([sum(C[i, j] * D[j] for j in range(3)) for i in range(3)])
    CB = np.asarray([sum(C[i, j] * B[j] for j in range(3)) for i in range(3)])
    rB = curl(C, B, state.L)
    CrB = np.asarray([sum(C[i, j] * rB[j] for j in range(3)) for i in range(3)])
    return int(sum((3 * (D * CD + B * CB) - D * CrB).flat))


def _energy(plane, preparation_scale):
    C = np.asarray(optical_matrix(plane), dtype=float)
    D, B = np.asarray(plane[:3], dtype=float) / preparation_scale, np.asarray(plane[3:6], dtype=float) / preparation_scale
    return .5 * sum(D[i] * sum(C[i, j] * D[j] for j in range(3)) +
                    B[i] * sum(C[i, j] * B[j] for j in range(3)) for i in range(3))


def inspect(path, *, replay=True):
    """Read every saved state and click; compare clicks to an independent predicate.

    Replay may be omitted only immediately after run_bundle already verified the
    immutable saved run. Public inspection and central receipts replay by default.
    """
    path = Path(path)
    execution = verify_run(path) if replay else json.loads((path / 'validation.json').read_text())
    bundle = load_bundle(path / 'bundle')
    if bundle.tensor.fingerprint != tensor().fingerprint:
        raise ValueError('Saved run does not use the declared light tensor')
    if bundle.model.get('id') != 'maxwell-light-packet-candidate':
        raise ValueError('Saved interpretation is not the light candidate')
    setup = bundle.model['preparation']
    if execution['steps'] != setup['steps']:
        raise ValueError('Saved horizon differs from the declared finite preparation')
    # Reconstruct and compare complete declared preparation; labels cannot certify a seed.
    expected = make_bundle(**{key: setup[key] for key in
                             ('L', 'steps', 'geometry', 'order', 'center', 'interface', 'amplitude')},
                           precision=int(setup['Q']) if setup['precision_control'] else None)
    if expected.bundle_id != bundle.bundle_id:
        raise ValueError('Declared preparation does not reproduce the complete bundle')
    L, preparation_scale = setup['L'], int(setup['Q'])
    seed = bundle.seed
    a0, p0, r0 = _planes(seed)
    initial_support = np.flatnonzero(np.any(a0[:12] != 0, axis=0) | np.any(p0[:12] != 0, axis=0))
    x = np.arange(L)
    dist = (np.min(np.minimum((x[:, None] - initial_support[None, :]) % L,
                            (initial_support[None, :] - x[:, None]) % L), axis=1)
            if len(initial_support) else np.full(L, L))
    times = [0.]
    energies = [_energy(p0, preparation_scale).tolist()]
    counts, weights, first = [], [], [None] * L
    classes = Counter({'C0': 0, 'C1': 0, 'C2': 0})
    exact_sector, fixed_carry, ledger_ok, cone_ok = True, True, True, True
    ledger0 = _ledger(seed)
    outside = []
    current = seed
    checked_clicks = 0
    with gzip.open(path / 'full_trace.jsonl.gz', 'rt', encoding='utf-8') as traces, \
            gzip.open(path / 'clicks.jsonl.gz', 'rt', encoding='utf-8') as events:
        pending = next(events, None)
        for tick, line in enumerate(traces, 1):
            record = exact_json.loads(line)
            before, after = State.from_dict(record['before']), State.from_dict(record['after'])
            if not before.same_as(current) or record['step'] != tick:
                raise ValueError('Broken saved transition chain')
            old, new = _planes(before), _planes(after)
            try:
                exact_sector &= np.array_equal(after.b, ideal(before.b, L))
            except ValueError:
                exact_sector = False
            fixed_carry &= np.array_equal(new[2], r0)
            expected_rows = []
            count, weight = np.zeros(L, dtype=int), np.zeros(L)
            for xx in range(L):
                for gear in range(18):
                    quotient = int(new[1][gear, xx] + old[0][gear, xx])
                    changed = any(old[i][gear, xx] != new[i][gear, xx] for i in range(3))
                    if quotient and changed:
                        delta = int((new[2][gear, xx] - old[2][gear, xx]) % 6)
                        kind = 'C0' if delta in (0, 3) else 'C1' if delta in (1, 2) else 'C2'
                        if gear >= 12:
                            raise ValueError('Frozen background emitted a click')
                        expected_rows.append((xx, gear, kind, quotient))
                        classes[kind] += L * L
                        count[xx] += 1
                        weight[xx] += abs(quotient) / preparation_scale
                        if first[xx] is None:
                            first[xx] = tick
            # Expand the independently computed plane rows in canonical node order.
            for xx in range(L):
                rows = [row for row in expected_rows if row[0] == xx]
                for yz in range(L * L):
                    for _, gear, kind, quotient in rows:
                        if pending is None:
                            raise ValueError('Missing canonical click')
                        event = exact_json.loads(pending)
                        actual = (event['step'], event['node'], event['channel'], event['kind'], event['quotient'])
                        if actual != (tick, xx * L * L + yz, gear, kind, quotient):
                            raise ValueError('Saved click differs from independent scalar predicate')
                        checked_clicks += 1
                        pending = next(events, None)
            counts.append(count.tolist()); weights.append(weight.tolist())
            cone_ok &= not any(count[dist > tick])
            if tick % 2 == 0:
                ledger_ok &= _ledger(after) == ledger0
                energy = _energy(new[1], preparation_scale)
                times.append(tick / 3); energies.append(energy.tolist())
                if setup['geometry'] == 'flat':
                    mask = dist > tick / 3
                    outside.append({'tick': tick, 'clicks': int(sum(count[mask])) * L * L,
                                    'energy_fraction': float(sum(energy[mask]) / sum(energy))
                                    if any(energy) else 0.})
            current = after
        if pending is not None or tick != execution['steps'] or checked_clicks != execution['click_count']:
            raise ValueError('Extra clicks, wrong horizon, or incomplete saved run')
    if not cone_ok:
        raise AssertionError('Computational face-neighbor cone violated')
    if not setup['precision_control'] and not (exact_sector and fixed_carry and ledger_ok):
        raise AssertionError('Finite prepared Maxwell-sector invariant failed')
    energy = np.asarray(energies)
    centers = (energy * x).sum(1) / energy.sum(1) if any(energy.flat) else np.zeros(len(times))
    result = {
        'run_id': execution['run_id'], 'bundle_id': execution['bundle_id'],
        'tensor_hash': execution['tensor_hash'], 'steps': execution['steps'], 'nodes': L ** 3,
        'algebra': {'divisor': 6, 'channels': 18, 'retained_integers_per_node': 54,
                    'monomials': len(bundle.tensor.monomials), 'maximum_degree': 2,
                    'strict_face_support': 'passed', 'old_a_reads': 0,
                    'maximum_integer_bits': max(execution['maximum_integer_bits_by_step'])},
        'click_count': checked_clicks, 'click_classes': dict(classes),
        'first_click_ticks': first, 'initial_complete_field_support': initial_support.tolist(),
        'coordinate_centroid_speed_fit': float(np.polyfit(times, centers, 1)[0]),
        'fixed_carry': bool(fixed_carry), 'exact_prepared_sector': bool(exact_sector),
        'exact_modified_energy_conservation': bool(ledger_ok),
        'computational_cone': 'passed', 'independent_click_check': 'passed',
        'target_cone': outside,
        'physical_gates': {
            'strict_target_null_cone': 'failed' if any(row['clicks'] for row in outside) else 'not_tested',
            'coupled_einstein_source': 'not_tested', 'operational_detector': 'not_tested',
            'photon_identification': 'blocked', 'general_physical_acceptance': 'blocked'},
        'times': times, 'energy': energies, 'centroids': centers.tolist(),
        'clicks_per_node_per_tick': counts, 'absolute_quotient_per_node_per_tick': weights,
        'scope': 'finite prepared static-background test field; arithmetic clicks are not detector events'}
    return result


def collect(out, *, L=13, steps=6, order=2, center=3, interface=5):
    """A fixed, bounded central regression collection, not a production selector."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    options = dict(L=L, steps=steps, order=order, center=center, interface=interface)
    report = {'schema': 'universe24/light-packet-audit/1', 'cases': {}, 'controls': {}}
    preparations = [(name, dict(options, geometry=name)) for name in ('flat', 'fast', 'step')]
    control = dict(L=9, steps=6, order=4, center=4, interface=6)
    preparations += [('amplitude_1', dict(control, amplitude=1)),
                     ('amplitude_2', dict(control, amplitude=2)),
                     ('vacuum', dict(control, amplitude=0)),
                     ('low_precision', dict(control, precision=3))]
    for name, kwargs in preparations:
        bundle = make_bundle(**kwargs)
        run_bundle(bundle, out / name, kwargs['steps'])
        observation = inspect(out / name, replay=False)
        (out / f'{name}.json').write_text(json.dumps(observation, indent=2, allow_nan=False) + '\n')
        report['cases' if name in ('flat', 'fast', 'step') else 'controls'][name] = observation
    main = list(report['cases'].values()); controls = report['controls']
    a, b = controls['amplitude_1'], controls['amplitude_2']
    amplitude_ok = (a['clicks_per_node_per_tick'] == b['clicks_per_node_per_tick'] and
                    a['click_classes'] == b['click_classes'] and
                    np.allclose(np.asarray(b['energy']), 4 * np.asarray(a['energy']), rtol=1e-14, atol=0) and
                    np.allclose(np.asarray(b['absolute_quotient_per_node_per_tick']),
                                2 * np.asarray(a['absolute_quotient_per_node_per_tick']), rtol=1e-14, atol=0))
    if not amplitude_ok or controls['vacuum']['click_count'] != 0:
        raise AssertionError('Amplitude or empty-field negative control changed')
    if controls['low_precision']['exact_prepared_sector']:
        raise AssertionError('Low precision falsely accepted as the exact prepared sector')
    report['comparisons'] = {
        'same_tensor': len({row['tensor_hash'] for row in main + list(controls.values())}) == 1,
        'main_count_maps_identical': all(row['clicks_per_node_per_tick'] == main[0]['clicks_per_node_per_tick'] for row in main),
        'amplitude_x2_energy_x4_same_click_counts': 'passed',
        'empty_field_zero_clicks': 'passed', 'low_precision_sector_failure_retained': 'passed'}
    report['physical_gates'] = {'strict_target_null_cone': main[0]['physical_gates']['strict_target_null_cone'],
                                'photon_identification': 'blocked', 'general_physical_acceptance': 'blocked'}
    report['profile'] = {'L': L, 'steps': steps, 'order': order, 'center': center, 'interface': interface,
                         'role': 'bounded regression; not a replacement for the archived 41^3 experiment'}
    (out / 'light_packet.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    return report
