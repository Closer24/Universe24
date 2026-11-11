"""Research audit: exact 48-channel frame map and explicit failed GR gates."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from universe24.algebra.frame_equations import FIELDS, equations
from universe24.core import Engine
from universe24.core.channels import ChannelAssembly, Component
from universe24.layers.frame48 import compile_frame48
from universe24.prepare.frame48 import flat_values, prepare, increment
from universe24.observe.frame48 import bank_values, diagnostics


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def kasner_reference():
    """Float-only homogeneous consistency control, NEVER an Engine trajectory.

    Exact sampled initial pair; compare leapfrog at t=2 to curved vacuum
    Kasner p=(2/3,2/3,-1/3). Small dt does not compile in the integer sector.
    """
    powers = (2/3, 2/3, -1/3)
    def analytic(t):
        values = np.zeros(24)
        for i, p in enumerate(powers):
            values[FIELDS.index(f'B{i}{i}')] = t**(-p)
            values[FIELDS.index(f'K{i}{i}')] = -p/t
        return values
    rows = []
    for steps in (16, 32, 64):
        dt = 1/steps
        previous, current = analytic(1-dt), analytic(1)
        for _ in range(steps):
            rhs, _, _ = equations(dict(zip(FIELDS, current)), lambda name, i: 0)
            following = previous+2*dt*np.array([rhs[name] for name in FIELDS])
            previous, current = current, following
        rows.append({'steps': steps, 'dt': f'1/{steps}',
                     'max_abs_error_at_t2': float(np.max(np.abs(current-analytic(2))))})
    return {'role': 'floating homogeneous reference only; not compiled Rule3 or general convergence evidence',
            'runs': rows,
            'errors_decrease': all(b['max_abs_error_at_t2'] < a['max_abs_error_at_t2']
                                   for a, b in zip(rows, rows[1:]))}


def audit(out=None):
    program = compile_frame48()
    assembly = ChannelAssembly([Component('frame48_experiment', program.tensor,
        'paired 24-field vacuum-frame candidate; general physical gates remain false', 'audit')])
    manifest = assembly.manifest()
    manifest['cross_component_dynamics'] = 'none; standalone research candidate'
    manifest['bank_semantics'] = {'X': 'previous physical field slice', 'Y': 'current physical field slice'}
    engine = Engine(assembly.tensor)
    L = 3
    cases = {}
    flat = flat_values(L)
    cases['flat'] = (flat, flat.copy(), 120)
    anisotropic = flat.copy()
    for i, k in enumerate((2, 2, -1)):
        anisotropic[FIELDS.index(f'K{i}{i}')] = k
    cases['nonlinear_anisotropic'] = (anisotropic, anisotropic.copy(), 6)
    rng = np.random.default_rng(48)
    cases['off_constraint_spatial'] = tuple(rng.integers(-1, 2, size=(24, L**3)).astype(object)
                                           for _ in range(2))+(3,)
    x, y = flat.copy(), flat.copy()
    x[FIELDS.index('K00')], y[FIELDS.index('K11')] = 1, 1
    cases['constraint_pair_counterexample'] = (x, y, 1)
    x, y = flat.copy(), flat.copy()
    x[FIELDS.index('B00')], y[FIELDS.index('K00')] = 2, -1
    cases['degeneracy_counterexample'] = (x, y, 1)
    results = {}
    for name, (old, current, steps) in cases.items():
        remainder = np.arange(48*L**3).reshape(48, L**3) % 6
        seed = assembly.pack({'frame48_experiment': prepare(program, old, current, L=L, remainders=remainder)})
        state = seed
        trace = [encoded({'format': 'Universe24-frame48-trace-v1', 'case': name,
                          'tensor': assembly.tensor.to_dict(), 'channels': manifest,
                          'dt': str(program.dt), 'dx': str(program.dx)})]
        observed, classes = [], {str(i): 0 for i in range(3)}
        largest_bits = 0
        for tick in range(steps+1):
            local = assembly.extract(state, 'frame48_experiment')
            trace.append(encoded({'tick': tick, 'state': state.to_dict()}))
            observed.append(diagnostics(bank_values(local), L=L, dx=program.dx))
            largest_bits = max(largest_bits, state.max_abs().bit_length())
            if tick == steps:
                break
            expected = old+increment(program, current, local.lattice)
            after = engine.step(state)
            decoded = assembly.extract(after, 'frame48_experiment')
            assert np.array_equal(bank_values(decoded, 'X'), current)
            assert np.array_equal(bank_values(decoded, 'Y'), expected)
            assert np.array_equal(after.r, seed.r)
            assert engine.inverse_step(after).same_as(state)
            clicks = engine.clicks(state, after, tick+1).select('audit')
            for kind in range(3):
                classes[str(kind)] += int(np.count_nonzero(clicks.kind == kind))
            old, current, state = current, expected, after
        assert engine.rewind(state, steps).same_as(seed)
        payload = b''.join(trace)
        if out is not None:
            Path(out).mkdir(parents=True, exist_ok=True)
            (Path(out)/f'{name}.jsonl').write_bytes(payload)
        results[name] = {'steps': steps, 'complete_snapshots': steps+1,
                         'exact_lift_every_step': True, 'exact_rewind': True,
                         'remainders_frozen': True, 'maximum_integer_bits': largest_bits,
                         'audit_click_classes': classes,
                         'initial_previous': diagnostics(cases[name][0], L=L),
                         'observations': observed if steps <= 6 else [observed[0], observed[-1]],
                         'trace_sha256': hashlib.sha256(payload).hexdigest()}
    rejected = {}
    for dt in (Fraction(1, 2), Fraction(1, 16)):
        try:
            compile_frame48(dt=dt)
        except ValueError as exc:
            rejected[str(dt)] = str(exc)
        else:
            raise AssertionError('Refinement barrier unexpectedly changed')
    source_paths = [Path(__file__).relative_to(ROOT)] + [Path(f'universe24/{p}.py') for p in (
        'algebra/frame_equations', 'layers/frame48', 'prepare/frame48', 'observe/frame48',
        'core/engine', 'core/tensor', 'core/lattice', 'core/channels')]
    return {'schema': 'Universe24-frame48-research-v1',
            'base_commit': 'df327c1a4d807df48500b3afeb51a4c4264b8b72', 'tensor_fingerprint': assembly.tensor.fingerprint,
            'channels': 48, 'monomials': len(assembly.tensor), 'input_degree': 2,
            'manifest': manifest, 'cases': results,
            'joint_half_grid_compiles': compile_frame48(dt=Fraction(1, 2), dx=Fraction(1, 2)).tensor.G == 48,
            'refinement_rejections': rejected, 'kasner_reference': kasner_reference(),
            'gates': {'exact_48_channel_reversible_map': True,
                      'strict_single_edge_support': not assembly.tensor.support_violations(),
                      'general_constraint_preservation': False,
                      'nondegeneracy_preservation': False,
                      'arbitrary_integer_precision_refinement': False,
                      'retained_physical_clock': False,
                      'general_einstein_solver_validated': False,
                      'matter_coupled': False},
            'source_sha256': {str(p): hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_paths}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'runs/frame48')
    args = parser.parse_args()
    report = audit(args.out)
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('channels', 'monomials', 'gates', 'kasner_reference')}, indent=2))
