"""Passive audit of PR47 denominator growth and unsafe scale cancellation.

No normalization enters Engine. Small algebra counterexamples are reference
calculations; the protected-frame runs use the existing 44-channel tensor.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import reduce
import hashlib
import json
from math import gcd
from pathlib import Path

import numpy as np

from universe24.core import Engine, State
from validation.geometry.team48 import refinement_integer_projective as projective
from validation.geometry.team48 import temporal_repair_projective as temporal


def algebra_checks():
    """Exhaust signed numerators and six carries independently of Engine."""
    count = 0
    for degree in (2, 3):
        for old_d in range(3):
            for d in range(2, 6):
                for old_p in range(-3, 4):
                    for p in range(-3, 4):
                        for carry in range(6):
                            # Scalar reference f(y)=y^2, dt=1/2, C=2.
                            raw = 2*d**(degree-1)*p+d**(degree-2)*p*p
                            quotient, remainder = divmod(6*raw+carry, 6)
                            next_p = quotient-old_p
                            next_d = 2*d**degree-old_d
                            assert remainder == carry and quotient == raw
                            assert raw-next_p == old_p
                            euler = F(p, d)+F(1, 2)*F(p, d)**2
                            # The equivalent identity also covers old_d=0.
                            exact = euler+(old_d*euler-old_p)/next_d
                            assert F(next_p, next_d) == exact
                            count += 1
    return {'signed_all_carry_scalar_cases': count, 'exact_ratio_identity': True}


def engine_scale_counterexample():
    program = projective.compile_projective(
        ('x',), lambda fields, partial: {'x': 0}, degree=2)
    engine = Engine(program.tensor)
    rows = []
    for carry in range(6):
        outputs = []
        for scale in (1, 2):
            old = np.repeat(np.array([[scale], [scale]], dtype=object), 27, axis=1)
            now = np.repeat(np.array([[3*scale], [2*scale]], dtype=object), 27, axis=1)
            seed = State(3, old, now, np.full((2, 27), carry, dtype=object))
            after = engine.step(seed)
            assert engine.inverse_step(after).same_as(seed)
            assert np.array_equal(after.r, seed.r)
            outputs.append(str(projective.readout(program, after)[0, 0]))
        assert outputs == ['11/17', '23/35']
        rows.append({'carry': carry, 'unscaled_next_ratio': outputs[0],
                     'scaled_next_ratio': outputs[1]})
    return {'same_current_ratio': '2/3', 'same_old_ratio': '1',
            'same_next_ratio': False, 'all_carry_engine_results': rows,
            'conclusion': 'Raw retained scale changes the physical history term.'}


def protected_runs():
    program = projective.compile_projective(temporal.NAMES, temporal.BUILDER,
                                            dt=F(1, 16), dx=1, degree=3)
    assert program.tensor.G == 44 and not program.tensor.support_violations()
    engine = Engine(program.tensor)
    runs = []
    for initial_d in (2, 16, 256):
        seed = temporal.prepared(program, initial_d)
        state = seed
        samples = []
        oracle_old, oracle_now = seed.a[:, 0].copy(), seed.b[:, 0].copy()
        for tick in range(7):
            d = int(state.b[0, 0])
            common = reduce(gcd, (abs(int(v)) for v in state.b[:, 0]), 0)
            paired_common = reduce(gcd, (abs(int(v)) for bank in (state.a, state.b)
                                         for v in bank[:, 0]), 0)
            wronskians = []
            for axis in range(3):
                p = 1+temporal.NAMES.index(f'diag_p{axis}')
                q = 1+temporal.NAMES.index(f'diag_q{axis}')
                w = int(state.b[p, 0])*int(state.a[q, 0])-int(state.b[q, 0])*int(state.a[p, 0])
                assert w == initial_d and w % common == 0
                wronskians.append(w)
            # Exact lower bound, not a floating logarithm or asymptotic fit.
            assert d >= initial_d**(3**tick)
            assert paired_common == 1
            samples.append({'tick': tick, 'denominator_bits': d.bit_length(),
                            'rigorous_bit_lower_bound': (initial_d.bit_length()-1)*3**tick+1,
                            'current_bank_gcd': common, 'paired_bank_gcd': paired_common,
                            'bits_after_passive_current_gcd': (d//common).bit_length(),
                            'Wronskians': wronskians})
            if tick == 6:
                break
            expected = temporal.integer_oracle(program, oracle_old, oracle_now)
            before = state
            state = engine.step(state)
            assert np.array_equal(state.a, np.repeat(oracle_now[:, None], 27, axis=1))
            assert np.array_equal(state.b, np.repeat(expected[:, None], 27, axis=1))
            assert np.array_equal(state.r, seed.r)
            assert engine.inverse_step(state).same_as(before)
            oracle_old, oracle_now = oracle_now, expected
        assert engine.rewind(state, 6).same_as(seed)
        final = temporal.diagnostics(state)
        runs.append({'initial_denominator': initial_d, 'steps': 6,
                     'fixed_final_time': '3/8', 'samples': samples,
                     'final_abs_H': final['abs_H'], 'final_B': final['B'],
                     'complete_scalar_oracle_and_rewind': True})
    return {'channels': 44, 'nodes': 27, 'degree': 3,
            'dt': '1/16', 'multiplier': program.multiplier,
            'tensor_fingerprint': program.tensor.fingerprint,
            'runs': runs}


def audit(out):
    root = Path(__file__).resolve().parents[2]
    source_paths = [Path(__file__),
                    root/'validation/geometry/team48/refinement_integer_projective.py',
                    root/'validation/geometry/team48/temporal_repair_projective.py']
    report = {'schema': 'universe24/projective-bitgrowth-audit/1',
              'baseline': '621fc1f55800e50e1db5f6a30ce24bb83716a49a',
              'command': f'python -m validation.synthesis.bitgrowth_algebra --out {out}',
              'status': {'exact_algebra_and_replay': 'passed',
                         'raw_scale_is_a_dynamical_gauge': 'failed',
                         'current_gcd_can_remove_exponential_growth': 'failed',
                         'efficient_generic_replacement': 'not_tested',
                         'physical_acceptance': 'not_tested'},
              'scope': 'Representation cost and algebraic obstruction; no physical acceptance.',
              'sources': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in source_paths},
              'algebra': algebra_checks(),
              'scale_counterexample': engine_scale_counterexample(),
              'protected44': protected_runs(),
              'normalization_implemented': False,
              'limits': ['Short homogeneous scalar/dust geometry runs, not a generic sourced convergence test.',
                         'The lower bound is for this prepared projective recurrence only, not all Universe24 tensors.',
                         'All gcd calculations are passive diagnostics and never change Engine state.',
                         'No claim equates bit growth or algebraic entropy with physical complexity.'],
              'mitigation': 'Smaller prepared denominator reduces the bit-growth prefactor but changes retained-history error; exponential growth remains.'}
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'report': str(out), 'cases': report['algebra']['signed_all_carry_scalar_cases'],
                      'final_bits': [r['samples'][-1]['denominator_bits']
                                     for r in report['protected44']['runs']]}))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='runs/synthesis/bitgrowth_algebra.json')
    audit(parser.parse_args().out)
