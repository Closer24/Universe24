"""Bounded current-main recurrence and growth/structure controls; no feedback."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import argparse
from collections import deque
import hashlib
import json

from experiments.cosmology.recurrent_bursts import (
    compact, feedback_interventions, run_case, score, structural_snapshot,
)
from universe24.core import Engine
from universe24.prepare.conformal_flrw import prepare
from universe24.observe.conformal_flrw import sample

BASELINE = '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2'


def run(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    configs = [
        ('baseline', dict(L=5, steps=600)),
        ('no_messages', dict(L=5, steps=80, amplitude=0)),
        ('disconnected', dict(L=5, steps=80, family='disconnected')),
        ('periodic_shell', dict(L=7, steps=70, family='periodic_control')),
    ] + [(family+'_plus1', dict(L=5, steps=160, family=family, coefficient=1))
         for family in ('linear', 'cubic', 'spring')]
    cases = []
    for name, params in configs:
        result = run_case(**params, out=out/name)
        row = compact(result)
        row['case'] = name
        maximum = row['maximum_site_pattern_types']
        row['first_maximum_site_patterns'] = next(
            r['update'] for r in result['samples'] if r['site_pattern_types'] == maximum)
        row['initial_score'] = score(result['samples'][0])
        row['final_score'] = score(result['samples'][-1])
        cases.append(row)
        print(json.dumps({k: row[k] for k in (
            'case', 'completed_updates', 'stop_reason', 'exact_rewind',
            'maximum_counter_bits', 'first_maximum_site_patterns', 'final_score')}), flush=True)

    # A separate tensor and physical interpretation: homogeneous metric growth
    # is not a recurrence of the reference-board concentration diagnostic.
    tensor, seed = prepare(L=3, q0=2, dust=(1, 1, 1), radiation=1)
    engine = Engine(tensor)
    state, history, rows = seed, deque(maxlen=2), []
    for tick in range(33):
        obs = sample(state)
        metrics, signatures = structural_snapshot(state, range(tensor.G), tuple(history))
        history.append(signatures)
        rows.append({'update': tick, 'q': int(state.b[0, 0]),
            'scale_factor': str(obs['scale_factor']), 'proper_time': str(obs['proper_time']),
            'score': score(metrics), 'max_bits': state.max_abs().bit_length(),
            'spatially_uniform': len(set(signatures)) == 1})
        if tick < 32:
            state = engine.step(state)
    assert engine.rewind(state, 32).same_as(seed)
    assert all(a['q'] < b['q'] for a, b in zip(rows, rows[1:]))
    assert all(a['score'] == b['score'] for a, b in zip(rows[2:], rows[3:]))
    flrw = {'scope': 'Optional prepared homogeneous FLRW only; not communication concentration.',
        'updates': 32, 'exact_rewind': True, 'all_samples_spatially_uniform': True,
        'tensor_fingerprint': tensor.fingerprint, 'initial_scale_factor': rows[0]['scale_factor'],
        'final_scale_factor': rows[-1]['scale_factor'], 'initial_bits': rows[0]['max_bits'],
        'final_bits': rows[-1]['max_bits'], 'settled_structure_score': rows[-1]['score'],
        'samples': rows}

    old = json.loads((ROOT/'docs/evidence/recurrent_bursts.json').read_text())
    keys = ('completed_updates', 'stop_reason', 'tensor_fingerprint', 'initial_hash',
        'final_hash', 'exact_rewind', 'full_state_returns', 'carrier_focus_updates',
        'reference_reassemblies', 'maximum_counter_bits')
    comparison = []
    for case in cases:
        matching = [r for r in old['cases'] if r['parameters'] == case['parameters']]
        differences = [key for key in keys if matching[0].get(key) != case.get(key)] if matching else None
        if matching:
            assert not differences
        comparison.append({'case': case['case'], 'matching_historical_parameters': bool(matching),
            'differences': differences,
            'note': 'Shorter declared control horizon' if not matching else 'Exact matched outputs'})
    sources = ('experiments/research/six_lens_complexity.py',
        'experiments/cosmology/recurrent_bursts.py', 'experiments/cosmology/PROTOCOL.md',
        'universe24/core/engine.py', 'universe24/layers/communication.py',
        'universe24/prepare/communication.py', 'universe24/layers/causal_wave.py',
        'universe24/layers/conformal_flrw.py', 'universe24/prepare/conformal_flrw.py',
        'universe24/observe/conformal_flrw.py', 'universe24/layers/frame48.py')
    result = {'baseline_main': BASELINE, 'cases': cases, 'flrw_growth_control': flrw,
        'historical_comparison': comparison, 'feedback_interventions': feedback_interventions(),
        'source_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}}
    (out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/six-lens/05-complexity-cycles'))
    run(parser.parse_args().out)
