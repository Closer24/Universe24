"""Continuum/parasitic-mode audit of a squared-diagonal representation.

This checks the proposed physical leapfrog recurrence independently of its
integer compiler. Exact Fraction trajectories below are not Engine runs.
"""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]


def audit(out):
    p, q, old_p, old_q, coefficient = sp.symbols('p q old_p old_q coefficient', real=True)
    next_p, next_q = old_p+coefficient*p, old_q+coefficient*q
    wronskian = p*old_q-q*old_p
    assert sp.expand(next_p*q-next_q*p+wronskian) == 0
    norm, old_norm = p*p+q*q, old_p*old_p+old_q*old_q
    dot = p*old_p+q*old_q
    assert sp.expand(norm*old_norm-dot*dot-wronskian*wronskian) == 0
    # c=h*K=-3/2 has exact roots 1/2,-2. The second-root component
    # preserves strict positivity but eventually dominates the decaying mode.
    c, epsilon = F(-3, 2), F(1, 1024)
    previous, current = (F(2), -epsilon/2), (F(1), epsilon)
    initial_wronskian = current[0]*previous[1]-current[1]*previous[0]
    exact_rows = []
    for tick in range(16):
        a, b = current
        observed = a*a+b*b
        physical_branch = F(1, 4)**tick
        parasite_branch = epsilon*epsilon*F(4)**tick
        assert observed == physical_branch+parasite_branch
        assert observed > 0
        current_wronskian = a*previous[1]-b*previous[0]
        assert current_wronskian == (-1)**tick*initial_wronskian
        if tick in (0, 5, 10, 15):
            exact_rows.append({'tick': tick, 'B': str(observed),
                               'physical_root_contribution': str(physical_branch),
                               'parasitic_root_contribution': str(parasite_branch),
                               'wronskian': str(current_wronskian)})
        previous, current = current, (previous[0]+c*a, previous[1]+c*b)
    assert F(exact_rows[-1]['parasitic_root_contribution']) > 1000
    # A positive control against an overbroad no-go: shrinking the parasitic
    # seed with h gives ordinary fixed-time convergence in floating analysis.
    # This is not a fixed-tensor integer refinement construction.
    refinement = []
    duration, curvature = 4, -1
    target = math.exp(curvature*duration)
    for subdivision in (4, 8, 16, 32, 64, 128):
        step = 1/subdivision
        z = step*curvature/2
        plus, minus = z+math.sqrt(1+z*z), z-math.sqrt(1+z*z)
        count, amplitude = duration*subdivision, step*step
        observed = plus**(2*count)+amplitude*amplitude*minus**(2*count)
        error = abs(observed-target)
        refinement.append({'subdivision': subdivision, 'h': step,
                           'parasitic_seed_amplitude': amplitude,
                           'B_at_time_4': observed, 'target_exp_minus_4': target,
                           'absolute_error': error})
    assert all(b['absolute_error'] < a['absolute_error'] for a, b in zip(refinement, refinement[1:]))
    report = {'scope': 'independent amplitude recurrence and mode analysis; not an Engine compilation',
              'exact_wronskian_sign_flip': True, 'exact_Gram_identity': True,
              'positivity_if_nonzero_wronskian': True,
              'nonzero_wronskian_requires_second_root_for_constant_K': True,
              'exact_decaying_branch_counterexample': exact_rows,
              'floating_fixed_time_refinement_positive_control': refinement,
              'limitations': ['Constant prescribed K is a mode test, not a self-consistent Einstein solution.',
                  'Exact rational recurrence is not an integer Engine run or channel-count result.',
                  'Positivity does not establish H/M, matter conservation, or continuum convergence.',
                  'Shrinking a physical Wronskian with precision is possible in principle; its integer compiler and preparation remain separate obligations.'],
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    print(json.dumps(audit(ROOT/'runs/team48/variational/amplitude_modes.json'), indent=2))
