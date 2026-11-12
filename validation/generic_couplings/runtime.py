"""Run the full and restricted audit bundles through the one system runtime."""
from __future__ import annotations

import gzip
from pathlib import Path

from universe24.core import State, exact_json
from universe24.system.bundle import create_bundle
from universe24.system.decoder import decode_transition, default_protocol, make_transition
from universe24.system.runtime import run_bundle, verify_run
from .sector import build_reduction, embed_state, prepare_seed

FULL_HASH = '6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0'
REDUCED_HASH = '6e00a1bb2dd7f7f9ddf5c1bd66b31e5bafc450fff12d98515367368e1e0d2c3a'


def _bundle(tensor, seed, role):
    return create_bundle(
        tensor, seed,
        channels=[{'index': i, 'name': gear.name, 'label': gear.label,
                   'owner': 'validation.homogeneous_sector',
                   'purpose': role + '; complete history and carry retained'}
                  for i, gear in enumerate(tensor.gears)],
        protocol=default_protocol(),
        model={'id': 'generic-couplings-' + role, 'version': '1',
               'domain': 'homogeneous isotropic neutral scalar/dust invariant-sector audit; '
                         'constraint and stability defects remain; no physical acceptance'})


def _read(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        return [exact_json.loads(line) for line in stream]


def run_runtime_pair(out: Path, steps: int = 4) -> dict:
    """Save both bundles, verify every reconstructed transition and full click.

    Raw six-channel clicks have different owners/identities and are not the
    full45 stream. Reconstruct full transitions before applying its decoder.
    """
    if type(steps) is not int or not 1 <= steps <= 8:
        raise ValueError('audit steps must be an integer in 1..8')
    out = Path(out)
    if out.exists():
        raise ValueError('audit output must be a new directory')
    reduction = build_reduction()
    if reduction.full_tensor.fingerprint != FULL_HASH or reduction.tensor.fingerprint != REDUCED_HASH:
        raise ValueError('default sector law fingerprint changed; rederive the reference contract')
    reduced_seed = prepare_seed()
    full_seed = embed_state(reduction, reduced_seed)
    full_bundle = _bundle(reduction.full_tensor, full_seed, 'full45-reference')
    reduced_bundle = _bundle(reduction.tensor, reduced_seed, 'restricted6')
    full = run_bundle(full_bundle, out / 'full', steps)
    reduced = run_bundle(reduced_bundle, out / 'reduced', steps)
    if verify_run(out / 'full') != full or verify_run(out / 'reduced') != reduced:
        raise AssertionError('saved runtime replay mismatch')
    full_trace = _read(out / 'full' / 'full_trace.jsonl.gz')
    reduced_trace = _read(out / 'reduced' / 'full_trace.jsonl.gz')
    if len(full_trace) != steps or len(reduced_trace) != steps:
        raise AssertionError('incomplete saved sector trace')
    reconstructed_clicks = []
    for source, small in zip(full_trace, reduced_trace):
        if source['step'] != small['step']:
            raise AssertionError('sector trace step mismatch')
        before, after = [embed_state(reduction, State.from_dict(small[key]))
                         for key in ('before', 'after')]
        for key, state in (('before', before), ('after', after)):
            if not state.same_as(State.from_dict(source[key])):
                raise AssertionError('saved complete-state reconstruction mismatch')
        reconstructed = make_transition(reduction.full_tensor, before, after,
                                        run_id=full['run_id'], step=source['step'])
        reconstructed_clicks.extend(decode_transition(reconstructed, reduction.full_tensor))
    full_clicks = _read(out / 'full' / 'clicks.jsonl.gz')
    if reconstructed_clicks != full_clicks:
        raise AssertionError('reconstructed canonical source clicks differ')
    for report in (full, reduced):
        if any(report['acceptance_gates'][key]['status'] != 'not_tested' for key in 'CDEF'):
            raise AssertionError('mechanical reduction must not promote physical acceptance')
    return {'status': 'passed', 'steps': steps, 'full_channels': full_bundle.tensor.G,
            'reduced_channels': reduced_bundle.tensor.G,
            'full_tensor_hash': FULL_HASH, 'reduced_tensor_hash': REDUCED_HASH,
            'full_bundle_id': full_bundle.bundle_id, 'reduced_bundle_id': reduced_bundle.bundle_id,
            'full_run_id': full['run_id'], 'reduced_run_id': reduced['run_id'],
            'reconstructed_transitions': len(full_trace),
            'reconstructed_source_clicks': len(reconstructed_clicks),
            'full_trace_and_click_reconstruction': 'passed', 'saved_replay': 'passed',
            'maximum_integer_bits_by_step': full['maximum_integer_bits_by_step'],
            'physics_acceptance': 'not_established'}
