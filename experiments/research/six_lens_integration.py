"""Read-only cross-owner audit on the current compiled ADM assembly.

This audits an intentional direct sum; it does not introduce physical coupling.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from universe24.core import Engine
from universe24.layers.adm import compile_adm, flat_data
from universe24.layers.universe import UniverseProgram


def audit(out):
    out.mkdir(parents=True, exist_ok=True)
    base, parameters = compile_adm(complex_matter=True, dark_matter=True)
    inventory = UniverseProgram(base, parameters, communication=True,
        probe_experiment=True, causal_wave=True)
    assembly = inventory.assembly
    edges = Counter()
    for monomial in assembly.tensor.monomials:
        for factor in monomial.factors:
            edges[assembly.owners[factor.gear], assembly.owners[monomial.target]] += 1
    cross = {f'{a}->{b}': n for (a, b), n in edges.items() if a != b}
    assert not cross

    program = UniverseProgram(base, parameters, communication=True, causal_wave=True)
    data = flat_data(3)
    for name in ('chi', 'Pi_chi', 'rho_dark'):
        data[name] = np.zeros((3, 3, 3), dtype=object)
    reference = program.prepare(3, data)
    # An initial-data intervention, never a runtime injection.
    wave_changed = reference.copy()
    g = program.tensor.gear_index('causal_wave.wave.px')
    wave_changed.a[g] *= 2
    wave_changed.b[g] *= 2
    assert not wave_changed.same_as(reference)
    metric_data = {key: value.copy() for key, value in data.items()}
    metric_data['g00'] *= 4
    metric_changed = program.prepare(3, metric_data)
    states = {'reference': reference, 'wave_changed': wave_changed,
              'metric_changed': metric_changed}
    seeds = {key: state.copy() for key, state in states.items()}
    engine = Engine(program.tensor)
    equalities = []
    with gzip.open(out/'counterfactuals.jsonl.gz', 'wt') as trace:
        trace.write(json.dumps({'tensor': program.tensor.to_dict(),
            'manifest': program.assembly.manifest(), 'updates': 6})+'\n')
        for tick in range(7):
            for name, state in states.items():
                trace.write(json.dumps({'trial': name, 'tick': tick, 'state': state.to_dict()})+'\n')
            same_einstein = program.assembly.extract(states['reference'], 'einstein').same_as(
                program.assembly.extract(states['wave_changed'], 'einstein'))
            same_wave = program.assembly.extract(states['reference'], 'causal_wave').same_as(
                program.assembly.extract(states['metric_changed'], 'causal_wave'))
            assert same_einstein and same_wave
            equalities.append({'microtick': tick, 'Einstein_independent_of_wave': same_einstein,
                               'wave_independent_of_metric': same_wave})
            if tick < 6:
                states = {key: engine.step(state) for key, state in states.items()}
    assert all(engine.rewind(states[key], 6).same_as(seeds[key]) for key in states)
    paths = ('universe24/core/channels.py', 'universe24/layers/universe.py',
             'universe24/layers/adm.py', 'universe24/layers/causal_wave.py',
             'experiments/research/six_lens_integration.py')
    return {'baseline': '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
        'scope': 'Component isolation, not shared physical dynamics or empirical validation.',
        'inventory': assembly.manifest(include_channels=False),
        'factor_edges': {f'{a}->{b}': n for (a, b), n in edges.items()},
        'cross_owner_factor_edges': cross, 'source_and_metric_counterfactuals': equalities,
        'all_full_state_rewinds_exact': True,
        'prepared_arms_and_metric_different': True,
        'trace_sha256': hashlib.sha256((out/'counterfactuals.jsonl.gz').read_bytes()).hexdigest(),
        'source_sha256': {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in paths}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'runs/six-lens/06-integration/wiring')
    args = parser.parse_args()
    result = audit(args.out)
    (args.out/'report.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in ('factor_edges', 'cross_owner_factor_edges',
        'source_and_metric_counterfactuals', 'all_full_state_rewinds_exact')}, indent=2))
