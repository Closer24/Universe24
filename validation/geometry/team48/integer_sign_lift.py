"""One field bank plus one period-four sign channel for a quadratic leapfrog.

This is an exact encoding improvement, not a new Einstein integrator. It
retains the physical leapfrog's constraint, stability and refinement limits.
No production layer or Engine code is changed.
"""
from dataclasses import dataclass
from fractions import Fraction

import numpy as np
import sympy as sp

from universe24.core import GearType, State, Tensor
from universe24.core.lattice import OFFSETS, ZERO, lattice
from universe24.algebra.null_covector import integer_array


@dataclass(frozen=True)
class SignProgram:
    tensor: Tensor
    fields: tuple[str, ...]
    dt: Fraction
    dx: Fraction


def compile_quadratic(fields, equation_builder, *, dt=1, dx=1):
    """Compile y_next=y_previous+2dt*f(y), for fixed degree<=2 local f.

    The builder has the existing (fields, partial) interface and may return
    rhs or a tuple whose first item is rhs. It executes only at construction.
    Constants/linear/quadratic terms may coexist. Every coefficient of 2dt*f
    must be integral; this function never rounds or changes the divisor.
    """
    for value in (dt, dx):
        if isinstance(value, (float, bool)):
            raise TypeError('Use exact positive dt and dx')
    dt, dx = Fraction(dt), Fraction(dx)
    if dt <= 0 or dx <= 0:
        raise ValueError('dt and dx must be positive')
    fields = tuple(fields)
    if len(set(fields)) != len(fields) or not fields:
        raise ValueError('Expected nonempty unique physical field names')
    symbols = {(name, offset): sp.Symbol(f'z{i}_{j}')
               for i, name in enumerate(fields) for j, offset in enumerate(OFFSETS)}
    locations = {value: key for key, value in symbols.items()}
    here = {name: symbols[name, ZERO] for name in fields}

    def partial(name, axis):
        plus = tuple(int(i == axis) for i in range(3))
        minus = tuple(-v for v in plus)
        return (symbols[name, plus]-symbols[name, minus])/(2*sp.Rational(dx))

    result = equation_builder(here, partial)
    rhs = result[0] if isinstance(result, tuple) else result
    phase = 'phase.sign'
    terms = []  # u_phase=0, hence phase.b_next=-phase.a, at fixed six.
    for name in fields:
        for term in sp.Add.make_args(sp.expand(2*sp.Rational(dt)*rhs[name])):
            if not term:
                continue
            coefficient, product = term.as_coeff_Mul()
            if not coefficient.is_Integer:
                raise ValueError(f'Increment of {name} has noninteger coefficient {coefficient}; '
                                 'sign encoding does not remove integer refinement limits')
            factors = []
            for symbol, power in product.as_powers_dict().items():
                if symbol == 1:
                    continue
                if symbol not in locations or not power.is_Integer or power < 0:
                    raise ValueError('RHS must be a polynomial in the declared stencil')
                source, offset = locations[symbol]
                factors.extend([(f'field.{source}', offset, 'b')]*int(power))
            degree = len(factors)
            if degree > 2:
                raise ValueError('One-sign-channel lift requires degree <= 2')
            factors.insert(0, (phase, ZERO, 'b'))
            if degree == 1:
                factors.insert(1, (phase, ZERO, 'a'))
            terms.append((f'field.{name}', 3*int(coefficient), tuple(factors),
                          {'designated_one_way': 'Computational phase channel for an exact quadratic leapfrog encoding; not a reciprocal matter/clock interaction.'}))
    tensor = Tensor([GearType(phase, label='audit')]
                    + [GearType(f'field.{name}', label='audit') for name in fields],
                    terms, strict_support=True)
    return SignProgram(tensor, fields, dt, dx)


def prepare(program, previous, current, *, L, phase=(1, 1), remainders=None):
    """Encode previous/current physical slices into a and b, not extra gears.

    phase=(s_n,s_(n+1)); s_(n-1)=-s_(n+1). All nodes share this
    phase, because neighbor products assume the same sign convention.
    """
    lat = lattice(L)
    phase = tuple(phase)
    if len(phase) != 2 or any(type(s) is not int or s not in (-1, 1) for s in phase):
        raise ValueError('phase must contain two signs')
    old, now = integer_array(previous), integer_array(current)
    shape = (len(program.fields), lat.N)
    if old.shape != shape or now.shape != shape:
        raise ValueError(f'Expected physical arrays of shape {shape}')
    a = np.concatenate((np.full((1, lat.N), phase[0], dtype=object), -phase[1]*old))
    b = np.concatenate((np.full((1, lat.N), phase[1], dtype=object), phase[0]*now))
    r = np.zeros_like(b) if remainders is None else integer_array(remainders)
    if r.shape != b.shape or np.any(r < 0) or np.any(r >= 6):
        raise ValueError('Expected one legal remainder per channel/node')
    return State(L, a, b, r)


def physical_slices(program, state):
    """Decode only the sign invariant, without asserting Einstein constraints."""
    if state.G != len(program.fields)+1:
        raise ValueError('Expected the standalone sign-lift state')
    sa, sb = int(state.a[0, 0]), int(state.b[0, 0])
    if sa not in (-1, 1) or sb not in (-1, 1):
        raise ValueError('Phase is not in its sign sector')
    if not np.all(state.a[0] == sa) or not np.all(state.b[0] == sb):
        raise ValueError('A shared sign phase is required across neighbor stencils')
    return -sb*state.a[1:].astype(object), sa*state.b[1:].astype(object)


def invariant_summary(program):
    return {'physical_fields': len(program.fields), 'channels': program.tensor.G,
            'integer_entries_per_node': 3*program.tensor.G,
            'unallocated_channels_within_48': max(0, 48-program.tensor.G),
            'scratch_channels': 0, 'hidden_registers': 0,
            'phase_channels': 1, 'computational_phase_not_proper_clock': True,
            'input_degree': program.tensor.rank-1,
            'single_edge_violations': len(program.tensor.support_violations()),
            'old_a_reads': sorted({program.tensor.names[f.gear]
                                  for m in program.tensor.monomials for f in m.factors if f.field == 'a'}),
            'physical_map': 'y_next=y_previous+2dt*f(y_current)',
            'constraints_improved_by_encoding': False,
            'full_sourced_einstein_convergence_established': False,
            'generic_fractional_coefficient_refinement': False}
