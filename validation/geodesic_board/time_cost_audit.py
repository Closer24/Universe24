"""Independent fixed-time FLRW reference and integer cost audit.

Decimal RK4 is an external continuum oracle only. It never supplies a tensor,
seed value or Engine transition. The actual integer runs use the shared builder.
"""
from __future__ import annotations

from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
from pathlib import Path

from universe24.core import Engine
from .run import build_program, prepare_seed, fields_readout
from .constraint_audit import reduced_values, hamiltonian


def continuum_reference(steps=1024):
    """Raychaudhuri + scalar/dust conservation in (a,H,phi,pi,rho_d).

    This is a different variable set and on-constraint equation from the
    production off-constraint K equation. Units c=8*pi*G=m=1, lapse=1.
    Initial Friedmann constraint 3H^2=rho_d+(pi^2+phi^2)/2 is exactly satisfied.
    """
    if type(steps) is not int or steps < 1:
        raise ValueError('Positive reference step count required')
    with localcontext() as ctx:
        ctx.prec = 60
        dt = D(1)/(D(8)*steps)
        values = tuple(map(D, (1, 1, 2, 0, 1)))

        def rhs(v):
            a, H, phi, pi, rho = v
            return (H*a, -(pi*pi+rho)/2, pi, -3*H*pi-phi, -3*H*rho)

        for _ in range(steps):
            k1 = rhs(values)
            k2 = rhs(tuple(x+dt*k/2 for x, k in zip(values, k1)))
            k3 = rhs(tuple(x+dt*k/2 for x, k in zip(values, k2)))
            k4 = rhs(tuple(x+dt*k for x, k in zip(values, k3)))
            values = tuple(x+dt*(a+2*b+2*c+d)/6 for x, a, b, c, d in
                           zip(values, k1, k2, k3, k4))
        a, H, phi, pi, rho = values
        physical = (1/a, -H, phi, pi, rho.sqrt())
        friedmann = 3*H*H-rho-(pi*pi+phi*phi)/2
        return physical, abs(friedmann)


def integer_case(steps, reference):
    if steps not in (2, 4, 8):
        raise ValueError('Declared bounded refinement uses 2, 4 or 8 updates')
    program = build_program(dt=F(1, 8*steps), dx=F(1, 4), mass_squared=1)
    seed = prepare_seed(program, L=3, denominator=32)
    engine, state = Engine(program.tensor), seed
    bits = [seed.max_abs().bit_length()]
    for n in range(1, steps+1):
        after = engine.step(state)
        assert engine.inverse_step(after).same_as(state)
        # D_n >= D_0^(2^n), since C>=2 and 0<=D_previous<=D_current^2.
        assert int(after.b[0, 0]) >= 32**(2**n)
        state = after
        bits.append(state.max_abs().bit_length())
    assert engine.rewind(state, steps).same_as(seed)
    values = reduced_values(dict(zip(program.fields, fields_readout(program, state))))
    with localcontext() as ctx:
        ctx.prec = 60
        errors = [abs(D(v.numerator)/D(v.denominator)-r) for v, r in zip(values, reference)]
    return {'steps': steps, 'dt': str(program.dt), 'final_time': '1/8',
            'channels': program.tensor.G, 'tensor_sha256': program.tensor.fingerprint,
            'fields': ['inverse_scale_B', 'extrinsic_k', 'phi', 'Pi_phi', 'dust_amplitude'],
            'absolute_field_errors': [float(v) for v in errors],
            'maximum_field_error': float(max(errors)),
            'hamiltonian_abs': float(abs(hamiltonian(values))),
            'maximum_retained_bits_by_step': bits,
            'denominator_minimum_bits_proved': 5*(2**steps)+1,
            'measured_denominator_bits': int(state.b[0, 0]).bit_length(),
            'complete_rewind': True, 'positive_metric_on_final_slice': values[0] != 0}


def audit():
    coarse, residual_coarse = continuum_reference(1024)
    fine, residual_fine = continuum_reference(2048)
    discrepancy = max(abs(a-b) for a, b in zip(coarse, fine))
    assert discrepancy < D('1e-16') and residual_fine < D('1e-16')
    rows = [integer_case(n, fine) for n in (2, 4, 8)]
    errors = [row['maximum_field_error'] for row in rows]
    orders = [math.log2(a/b) for a, b in zip(errors, errors[1:])]
    assert all(a>b for a, b in zip(errors, errors[1:]))
    return {'schema': 'universe24/geodesic-board/time-cost/1',
            'scope': 'Finite homogeneous time refinement only; no spatial, general stability or constraint-preserving proof',
            'reference': {'method': '60-digit Decimal RK4 of independent on-constraint FLRW variables',
                          'steps_compared': [1024, 2048],
                          'maximum_reference_difference': str(discrepancy),
                          'friedmann_residual_coarse': str(residual_coarse),
                          'friedmann_residual_fine': str(residual_fine),
                          'feeds_engine_or_seed': False},
            'integer_refinement': rows, 'observed_max_norm_orders': orders,
            'all_field_errors_decrease': all(all(a>b for a, b in zip(
                [row['absolute_field_errors'][i] for row in rows],
                [row['absolute_field_errors'][i] for row in rows][1:])) for i in range(5)),
            'projective_cost': {'lower_bound': 'D_n >= 32^(2^n)',
                                'proof_domain': 'D_-1=0, D_0=32, C>=2, D_next=C D^2-D_previous',
                                'efficient_long_time_gate': 'failed'},
            'general_Einstein_convergence': 'not_established',
            'exact_discrete_constraints': 'failed',
            'next_compiler_obligation': 'Counted reversible temporal composition with no runtime projection or denominator normalization'}


def main():
    result = audit()
    output = Path('runs/geodesic-board/time-cost-audit.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
