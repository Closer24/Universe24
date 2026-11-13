"""Passive arithmetic-click views and explicitly calibrated channel inference.

These functions read click files, never complete traces or hidden Engine state.
Addresses and step indices are computational identifiers, not physical geometry
or proper-time measurements. Channel reconstruction requires public initial calibration and the positive
constant-carry sector; it is not a photon count.
"""
from __future__ import annotations

from collections import Counter
import gzip
import hashlib
from pathlib import Path

from .core import exact_json
from .model import coupling_tensor
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


def reconstruct_channel_from_clicks(path, *, channel, node_count, steps,
                                    initial_a, initial_b):
    """Reconstruct one positive channel from clicks and explicit public history.

    Rule3 gives b_next = quotient - a. In this constant-carry sector a fixed
    triple emits no click. Positive histories exclude a zero quotient, so a
    quiet update requires a=b=b_next. Missing records cannot in general be
    authenticated by this observer; complete-stream replay is a separate audit.
    """
    if any(type(v) is not int for v in (channel, node_count, steps)):
        raise ValueError('public calibration requires exact integers')
    if not 0 <= channel < 48 or node_count < 1 or steps < 0:
        raise ValueError('invalid public calibration')

    def history(value):
        if type(value) is int:
            values = [value] * node_count
        else:
            try:
                values = list(value)
            except TypeError as exc:
                raise ValueError('calibration requires positive integer histories') from exc
        if len(values) != node_count or any(type(v) is not int or v < 1 for v in values):
            raise ValueError('calibration requires complete positive integer histories')
        return values

    old, current = history(initial_a), history(initial_b)
    initial_old, initial_current = old[:], current[:]
    records = read_clicks(path)
    fingerprint = coupling_tensor().fingerprint
    events_by_key = {}
    for event in records:
        if event['tensor_hash'] != fingerprint:
            raise ValueError('clicks do not use the calibrated coupling law')
        if event['step'] > steps or event['node'] >= node_count:
            raise ValueError('event is outside the declared observation window')
        if event['kind'] != 'C0' or event['sign'] != 1:
            raise ValueError('outside the declared positive constant-carry sector')
        if event['channel'] == channel:
            events_by_key[event['step'], event['node']] = event
    changes, values_by_step = [], []
    for tick in range(1, steps + 1):
        next_values = []
        for node in range(node_count):
            event = events_by_key.get((tick, node))
            if event is not None:
                value = event['quotient'] - old[node]
                if old[node] == current[node] == value:
                    raise ValueError('a fixed channel triple unexpectedly emitted a click')
            else:
                if old[node] != current[node]:
                    raise ValueError('missing required nonquiet channel record')
                value = current[node]
            if value < 1:
                raise ValueError('clicks/calibration imply a nonpositive channel value')
            if value != current[node]:
                changes.append({'step':tick, 'node':node,
                                'before':exact_json.dumps(current[node]),
                                'after':exact_json.dumps(value),
                                'arithmetic_event_id':event['event_id']})
            next_values.append(value)
        old, current = current, next_values
        values_by_step.append([exact_json.dumps(value) for value in current])
    return {
        'schema':'universe24/click-only-channel/1',
        'input':'canonical click stream and explicit public calibration only',
        'calibration':{'tensor_hash':fingerprint, 'channel':channel,
                       'node_count':node_count, 'steps':steps,
                       'initial_a':[exact_json.dumps(v) for v in initial_old],
                       'initial_b':[exact_json.dumps(v) for v in initial_current],
                       'domain':'positive histories; constant carries; complete click stream'},
        'channel_arithmetic_clicks':len(events_by_key),
        'changes':changes, 'values_by_step':values_by_step,
        'limitations':['the initial calibration is supplied, not inferred',
                       'no metric, proper time, photon count or quantum probabilities are inferred',
                       'a standalone click file does not prove stream completeness'],
    }
