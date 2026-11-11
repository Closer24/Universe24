"""Fixed-six amplitude audit: phase, scale, norm and actual detector events.

No new evolution law. All detector runs use the existing fibre/gated pair.
Reference probabilities are comparisons, never supplied to Engine.step.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np

from experiments.quantum.born_reference import interference, probabilities, router_calibration
from universe24.core import Engine, State, compose
from universe24.core.tensor import Block, GearType
from universe24.layers.choice import build_fibre, build_gated_pair
from universe24.layers.matter import check_algebra

BASELINE = '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2'
COMPONENTS = ('a_re', 'a_im', 'b_re', 'b_im')


def apparatus():
    fibre = build_fibre(components=COMPONENTS, name='amp', label='audit')
    marker = Block((GearType('on', 'audit'),),
                   (('on', 6, (('on', (0, 0, 0), 'b'),)),), name='marker')
    detector = build_gated_pair(kappa=1, arm1=['amp.a_re', 'amp.a_im'],
        arm2=['amp.b_re', 'amp.b_im'], gate='marker.on', name='router')
    return compose(fibre, marker, detector, strict_support=True)


def calibrated_case(engine, label, a, b):
    tensor = engine.tensor
    amp_gears = [tensor.gear_index('amp.' + name) for name in COMPONENTS]
    ds = [tensor.gear_index('router.' + name) for name in ('dP', 'dM')]
    weights, born = probabilities(interference(a, b))
    counts, c2 = [0, 0], [0, 0]
    double = quiet = 0
    first_trace = []
    for residues in product(range(6), repeat=2):
        seed = State(9, *[np.zeros((tensor.G, 9**3), dtype=np.int64) for _ in range(3)])
        target = seed.lattice.index(4, 4, 4)
        g = tensor.gear_index('marker.on')
        seed.a[g, target] = seed.b[g, target] = 1
        for names, amplitude, site, direction in (
                (COMPONENTS[:2], a, (2, 4, 4), (1, 0, 0)),
                (COMPONENTS[2:], b, (6, 4, 4), (-1, 0, 0))):
            for name, value in zip(names, amplitude):
                g = tensor.gear_index('amp.' + name)
                seed.b[g, seed.lattice.index(*site)] = value
                seed.a[g] = seed.b[g, seed.lattice.shift_index(direction)]
        for g, r in zip(ds, residues):
            seed.r[g, target] = r
        state = seed
        amp_norm = lambda s: sum(int(v)**2 for v in s.b[amp_gears].flat)
        norm0 = amp_norm(seed)
        for tick in range(1, 4):
            if tick == 3:
                assert tuple(int(engine.inputs(state)[g, target]) for g in ds) == weights
            after = engine.step(state)
            clicks = engine.clicks(state, after, tick).select('official')
            assert amp_norm(after) == norm0
            if tick < 3:
                assert len(clicks) == 0
            if residues == (0, 0):
                first_trace.append({'tick': tick, 'transport_b_norm2': amp_norm(after),
                    'detector_a_b_r': [list(after.gear(g, target)) for g in ds]})
            state = after
        hit = [False, False]
        for g, node, kind in zip(clicks.gear, clicks.node, clicks.kind):
            assert int(node) == target and int(g) in ds
            side = ds.index(int(g))
            hit[side] = True
            counts[side] += 1
            c2[side] += int(kind == 2)
        # Independent arithmetic oracle; do not call Engine to set expectations.
        expected = [((2*int(w)+r)//6 != 0) for w, r in zip(weights, residues)]
        assert hit == expected
        double += int(all(hit))
        quiet += int(not any(hit))
        assert engine.rewind(state, 3).same_as(seed)
    expected_prob = [min(Fraction(1), Fraction(w, 3)) for w in weights]
    actual_prob = [Fraction(n, 36) for n in counts]
    assert actual_prob == expected_prob
    return {'case': label, 'arm_a': a, 'arm_b': b, 'input_weights': weights,
        'born_reference_probabilities': list(map(str, born)), 'emissions': 36,
        'actual_click_counts': counts, 'actual_C2_counts': c2,
        'actual_click_probability_per_emission': list(map(str, actual_prob)),
        'click_shares': [str(Fraction(n, sum(counts))) for n in counts],
        'double_clicks': double, 'no_clicks': quiet, 'trace_r00': first_trace,
        'transport_norm_preserved': True, 'rewind_exact': True, 'no_early_click': True}


def generic_norm_control():
    tensor = compose(build_fibre(components=('re', 'im'), name='amp', label='audit'))
    engine = Engine(tensor)
    state = State(9, *[np.zeros((tensor.G, 9**3), dtype=np.int64) for _ in range(3)])
    state.b[0, state.lattice.index(4, 4, 4)] = 1
    seed = state.copy()
    trace = []
    for tick in range(4):
        norms = {field: sum(int(v)**2 for v in getattr(state, field).flat) for field in ('a', 'b')}
        trace.append({'tick': tick, 'a_norm2': norms['a'], 'b_norm2': norms['b'],
                      'a_b_norm2': sum(norms.values())})
        if tick < 3:
            state = engine.step(state)
    assert [row['b_norm2'] for row in trace] == [1, 2, 3, 4]
    assert engine.rewind(state, 3).same_as(seed)
    return {'prepared_directed_transport_relation': False, 'trace': trace,
        'rewind_exact': True,
        'interpretation': 'The ordinary squared register norm is not preserved on arbitrary complete states. This does not rule out a different invariant or a restricted emergent quantum encoding.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/six-lens/03-born-algebra'))
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    current = router_calibration()
    engine = Engine(apparatus())
    cases = [calibrated_case(engine, f'scale_{s}', (2*s, 0), (s, 0)) for s in (1, 2, 3, 5)]
    cases += [calibrated_case(engine, 'global_i', (0, 2), (0, 1))]
    cases += [calibrated_case(engine, f'phase_{x}_{y}', (5, 0), (x, y))
              for x, y in ((5, 0), (3, 4), (0, 5), (-3, 4), (-5, 0))]
    rotated = calibrated_case(engine, 'common_rational_phase', (6, 8), (3, 4))
    cases.append(rotated)
    assert all(c['born_reference_probabilities'] == ['9/10', '1/10'] for c in cases[:4])
    assert cases[0]['actual_click_counts'] == cases[4]['actual_click_counts']
    assert cases[3]['input_weights'] == rotated['input_weights']
    assert cases[3]['actual_click_counts'] == rotated['actual_click_counts']
    algebra = check_algebra()
    assert all(algebra.values())
    root = Path(__file__).resolve().parents[2]
    names = ['experiments/research/six_lens_born.py', 'experiments/quantum/born_reference.py',
        'universe24/core/engine.py', 'universe24/core/tensor.py', 'universe24/layers/choice.py',
        'universe24/layers/matter.py']
    report = {'main_baseline': BASELINE, 'tensor_fingerprint': engine.tensor.fingerprint,
        'scope': 'Existing laws, declared initial-data controls; no production edits or Born feedback.',
        'scaling_interpretation': 'Common rescaling represents the same quantum ray only under a normalized single-particle amplitude encoding. If registers encode classical field strength or occupation, rescaling can change the physical preparation. These runs diagnose the missing encoding/calibration, not all possible quantum interpretations.',
        'current_calibration': current, 'extended_calibrations': cases,
        'extended_emissions': 36*len(cases),
        'binary_detector_law_for_this_preparation': 'P(click | nonnegative integer I, uniform r in 0..5, a=b=0)=min(1,I/3)',
        'generic_norm_control': generic_norm_control(), 'matter_algebra_checks': algebra,
        'born_rule_derived': False, 'source_sha256': {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}}
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'baseline': BASELINE, 'extended_emissions': report['extended_emissions'],
        'algebra_checks_passed': len(algebra), 'scaling': [{k: c[k] for k in ('case','input_weights','born_reference_probabilities','click_shares','double_clicks')} for c in cases[:4]],
        'norm_control': report['generic_norm_control']['trace']}, indent=2))


if __name__ == '__main__':
    main()
