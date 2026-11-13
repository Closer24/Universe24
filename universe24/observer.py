"""Passive arithmetic-click views and calibrated retained-memory inference.

These functions read click files, never complete traces or hidden Engine state.
Addresses and step indices are computational identifiers, not physical geometry
or proper-time measurements. Memory reconstruction requires the stated public
initial calibration and nonnegative detector sector; it is not a photon count.
"""
from __future__ import annotations

from collections import Counter
import gzip
import hashlib
from pathlib import Path

from .core import exact_json
from .detection import detector_tensor
from .system.bundle import canonical_bytes
from .system.decoder import verify_click_records

PROVENANCE_KEYS = frozenset(('run_id', 'event_id'))


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate click JSON field {key!r}')
        result[key] = value
    return result


def read_clicks(path):
    """No trace, seed, field, lattice metric or bundle read occurs here.

    Self-validation detects malformed records, not deletion of valid records.
    Complete-stream authenticity/completeness requires external replay evidence.
    """
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        records = [exact_json.loads(line, object_pairs_hook=_unique_pairs) for line in stream]
    verify_click_records(records, records)
    if len({event['run_id'] for event in records}) > 1:
        raise ValueError('a click file must contain exactly one run, not mixed provenance')
    if len({event['tensor_hash'] for event in records}) > 1:
        raise ValueError('a click file cannot mix tensor provenance')
    keys = [(event['step'], event['node'], event['channel']) for event in records]
    if any(left >= right for left, right in zip(keys, keys[1:])):
        raise ValueError('click events must be unique and in canonical chronological order')
    return records


def observed_payload(records):
    """Keep every recorded field except explicitly separated provenance IDs.

    In particular quotient, class, sign, channel, node and xyz are preserved.
    Addresses are identifiers, not calibrated physical distances or times.
    """
    return [{key: value for key, value in event.items() if key not in PROVENANCE_KEYS}
            for event in records]


def inspect_click_file(path):
    records = read_clicks(path)
    first_by_node = {}
    first_by_channel = {}
    for event in records:
        node, channel, step = str(event['node']), str(event['channel']), event['step']
        first_by_node[node] = min(first_by_node.get(node, step), step)
        first_by_channel[channel] = min(first_by_channel.get(channel, step), step)
    return {
        'source': 'canonical arithmetic clicks only',
        'events': len(records),
        'by_kind': dict(Counter(e['kind'] for e in records)),
        'observed_step_indices': sorted({e['step'] for e in records}),
        'first_recorded_step_by_node_address': first_by_node,
        'first_recorded_step_by_channel': first_by_channel,
        'signed_quotient_sum': exact_json.dumps(sum(e['quotient'] for e in records)),
        'complete_observational_payload_sha256': hashlib.sha256(canonical_bytes(observed_payload(records))).hexdigest(),
        'file_sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        'interpretation': 'first recorded arithmetic event, not photon arrival or a proper-time reading',
        'click_file_alone_proves_complete_horizon': False,
    }


def compare_click_files(left, right):
    a, b = read_clicks(left), read_clicks(right)
    x, y = observed_payload(a), observed_payload(b)
    return {
        'left_events': len(a), 'right_events': len(b),
        'entire_canonical_record_lists_equal': a == b,
        'complete_observational_payloads_equal': x == y,
        'excluded_cross_run_provenance_fields': sorted(PROVENANCE_KEYS),
        'quotient_retained_in_comparison': True,
        'left_payload_sha256': hashlib.sha256(canonical_bytes(x)).hexdigest(),
        'right_payload_sha256': hashlib.sha256(canonical_bytes(y)).hexdigest(),
    }


def reconstruct_memory_from_clicks(path, *, memory_channel, node_count, steps):
    """Infer calibrated nonnegative detector memory from clicks and quiet ticks.

    Public calibration: the declared detector law, zero initial (a,b) memory,
    node addresses 0..node_count-1, and a complete observation horizon. These
    are explicit assumptions, not quantities discovered in a hidden trace.

    A recorded quotient is m_next+m_old. If there is no event, either the
    complete triple is fixed, or this sum is zero. Nonnegative amplitudes and
    known old histories make these alternatives unambiguous. Constant carries
    follow from this detector tensor's coefficients being multiples of three.
    """
    if any(type(v) is not int for v in (memory_channel, node_count, steps)):
        raise ValueError('public calibration requires exact integers')
    if not 0 <= memory_channel < 48 or node_count < 1 or steps < 0:
        raise ValueError('invalid public calibration')
    records = read_clicks(path)
    fingerprint = detector_tensor().fingerprint
    events_by_key = {}
    for event in records:
        if event['tensor_hash'] != fingerprint:
            raise ValueError('clicks do not use the calibrated detector law')
        if event['step'] > steps or event['node'] >= node_count:
            raise ValueError('event is outside the declared observation window')
        if event['kind'] != 'C0' or event['sign'] != 1:
            raise ValueError('outside the declared nonnegative constant-carry sector')
        if event['channel'] == memory_channel:
            if (event['step'], event['node']) in events_by_key:
                raise ValueError('duplicate memory event key')
            events_by_key[event['step'], event['node']] = event
    old = [0] * node_count
    current = [0] * node_count
    changes, accounts = [], []
    for tick in range(1, steps + 1):
        next_values = []
        for node in range(node_count):
            event = events_by_key.get((tick, node))
            if event is not None:
                value = event['quotient'] - old[node]
                if old[node] == current[node] == value:
                    raise ValueError('a fixed memory triple unexpectedly emitted a click')
            else:
                value = current[node] if old[node] == current[node] else -old[node]
            if value < 0:
                raise ValueError('clicks/calibration imply negative retained memory')
            if value != current[node]:
                kind = ('capture' if current[node] == 0 else
                        'release' if value == 0 else 'exchange')
                changes.append({
                    'step': tick, 'node': node, 'kind': kind,
                    'memory_before': exact_json.dumps(current[node]), 'memory_after': exact_json.dumps(value),
                    'energy_to_memory': exact_json.dumps(value * value - current[node] * current[node]),
                    'arithmetic_event_id': event['event_id'] if event is not None else None,
                    'inference_uses_quiet_tick': event is None,
                    'photon_number': None,
                })
            next_values.append(value)
        old, current = current, next_values
        accounts.append({'step': tick, 'memory_account': exact_json.dumps(sum(v * v for v in current))})
    return {
        'schema': 'universe24/click-only-memory/1',
        'input': 'canonical click stream and explicit public calibration only',
        'calibration': {'tensor_hash': fingerprint, 'memory_channel': memory_channel,
                        'node_count': node_count, 'steps': steps,
                        'initial_a_memory': 'all zero', 'initial_b_memory': 'all zero',
                        'domain': 'nonnegative amplitudes; constant carries; complete click stream'},
        'memory_arithmetic_clicks': len(events_by_key),
        'outcomes': {kind: sum(e['kind'] == kind for e in changes)
                     for kind in ('capture', 'release', 'exchange')},
        'events': changes, 'accounts': accounts,
        'limitations': ['arithmetic transition count is not capture count',
                        'calibration is required; arbitrary latent state is not inferred',
                        'no incoming-light, arming, spacetime metric or proper-time readout',
                        'photon number and Born probabilities are not calibrated'],
    }


