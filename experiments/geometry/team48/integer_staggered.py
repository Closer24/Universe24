"""Per-field sign offsets for a restricted cubic integer leapfrog.

This is separate from the validated quadratic compiler. Every monomial is
checked after sign cancellation; unsupported cubic phase assignments fail.
It does not improve physical constraints, stability, or integer refinement.
"""
from dataclasses import dataclass
from fractions import Fraction

import numpy as np
import sympy as sp

from universe24.algebra.null_covector import integer_array
from universe24.core import GearType, State, Tensor
from universe24.core.lattice import OFFSETS, ZERO, lattice


@dataclass(frozen=True)
class StaggeredProgram:
    tensor: Tensor
    fields: tuple[str, ...]
    dt: Fraction
    dx: Fraction
    phase_offsets: tuple[int, ...]


def compile_staggered(fields, equation_builder, *, phase_offsets, dt=1, dx=1):
    """Compile y_next=y_previous+2dt*f(y) with per-field phase offsets.

    Offset0 uses s_n=clock.a; offset1 uses s_(n+1)=clock.b. Their
    next signs are clock.b and -clock.a, respectively. On a RHS monomial
    the compiled sign is its target's next sign times every input's current
    sign. Powers of either clock sign reduce modulo two. A cubic term is
    allowed exactly when delta_target+sum(delta_inputs)=1 modulo two.
    All coefficients of 2dt*f must be integers; no rounding is introduced.
    """
    for value in (dt, dx):
        if isinstance(value, (float, bool, np.floating, np.bool_)):
            raise TypeError('Use exact positive dt and dx')
    dt, dx = Fraction(dt), Fraction(dx)
    if dt <= 0 or dx <= 0:
        raise ValueError('dt and dx must be positive')
    fields = tuple(fields)
    if not fields or len(set(fields)) != len(fields):
        raise ValueError('Expected nonempty unique physical field names')
    if set(phase_offsets) != set(fields):
        raise ValueError('Provide one explicit phase offset for every physical field')
    if any(type(phase_offsets[name]) is not int or phase_offsets[name] not in (0, 1) for name in fields):
        raise ValueError('Each phase offset must be the integer0 or1')
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
    phase = 'phase.staggered'
    terms = []
    for name in fields:
        for term in sp.Add.make_args(sp.expand(2*sp.Rational(dt)*rhs[name])):
            if not term:
                continue
            coefficient, product = term.as_coeff_Mul()
            if not coefficient.is_Integer:
                raise ValueError(f'Increment of {name} has noninteger coefficient {coefficient}; '
                                 'staggering does not remove the integer refinement limitation')
            factors = []
            sign_powers = [int(phase_offsets[name] == 1), int(phase_offsets[name] == 0)]
            for symbol, power in product.as_powers_dict().items():
                if symbol == 1:
                    continue
                if symbol not in locations or not power.is_Integer or power < 0:
                    raise ValueError('RHS must be polynomial in the declared stencil')
                source, offset = locations[symbol]
                factors.extend([(f'field.{source}', offset, 'b')]*int(power))
                sign_powers[phase_offsets[source]] += int(power)
            degree = len(factors)
            if degree > 3:
                raise ValueError('Staggered compiler only accepts RHS degree at most3')
            clock_factors = [(phase, ZERO, ('a', 'b')[j]) for j in range(2) if sign_powers[j] % 2]
            if degree+len(clock_factors) > 3:
                raise ValueError(f'Phase assignment for cubic term in {name} violates '
                                 'delta_target+sum(delta_inputs)=1 modulo2')
            sign = -1 if phase_offsets[name] else 1
            terms.append((f'field.{name}', sign*3*int(coefficient), tuple(clock_factors+factors),
                          {'designated_one_way': 'Computational sign encoding; not a physical clock or reciprocal interaction.'}))
    tensor = Tensor([GearType(phase, label='audit')]
                    +[GearType(f'field.{name}', label='audit') for name in fields],
                    terms, strict_support=True)
    return StaggeredProgram(tensor, fields, dt, dx, tuple(phase_offsets[name] for name in fields))


def _signs(program, sa, sb):
    if sa not in (-1, 1) or sb not in (-1, 1):
        raise ValueError('Expected two clock signs')
    old = np.array([-sb if delta == 0 else sa for delta in program.phase_offsets], dtype=object).reshape(-1, 1)
    now = np.array([sa if delta == 0 else sb for delta in program.phase_offsets], dtype=object).reshape(-1, 1)
    return old, now


def prepare(program, previous, current, *, L, phase=(1, 1), remainders=None):
    """Encode both physical slices and every retained carry, with no repair."""
    phase = tuple(phase)
    if len(phase) != 2 or any(type(v) is not int or v not in (-1, 1) for v in phase):
        raise ValueError('phase must contain two integer signs')
    lat = lattice(L)
    old, now = integer_array(previous), integer_array(current)
    shape = (len(program.fields), lat.N)
    if old.shape != shape or now.shape != shape:
        raise ValueError(f'Expected two physical arrays with shape {shape}')
    sign_old, sign_now = _signs(program, *phase)
    a = np.concatenate((np.full((1, lat.N), phase[0], dtype=object), sign_old*old))
    b = np.concatenate((np.full((1, lat.N), phase[1], dtype=object), sign_now*now))
    r = np.zeros_like(b) if remainders is None else integer_array(remainders)
    if r.shape != b.shape or np.any(r < 0) or np.any(r > 5):
        raise ValueError('Expected one legal carry per channel and node')
    return State(L, a, b, r)


def physical_slices(program, state):
    """Decode the proved sign sector; do not assert Einstein constraints."""
    if state.G != len(program.fields)+1:
        raise ValueError('Expected the standalone staggered program state')
    sa, sb = int(state.a[0, 0]), int(state.b[0, 0])
    if not np.all(state.a[0] == sa) or not np.all(state.b[0] == sb):
        raise ValueError('Clock signs must be uniform across the lattice')
    sign_old, sign_now = _signs(program, sa, sb)
    return sign_old*state.a[1:].astype(object), sign_now*state.b[1:].astype(object)


def invariant_summary(program):
    return {'physical_fields': len(program.fields), 'channels': program.tensor.G,
            'integer_entries_per_node': 3*program.tensor.G,
            'unallocated_channels_within_48': max(0, 48-program.tensor.G),
            'phase_offsets': dict(zip(program.fields, program.phase_offsets)),
            'phase_channels': 1, 'scratch_channels': 0, 'hidden_registers': 0,
            'computational_phase_not_proper_clock': True,
            'input_degree': program.tensor.rank-1,
            'single_edge_violations': len(program.tensor.support_violations()),
            'old_a_reads': sorted({program.tensor.names[f.gear]
                                  for m in program.tensor.monomials for f in m.factors if f.field == 'a'}),
            'physical_map': 'y_next=y_previous+2dt*f(y_current)',
            'constraints_improved_by_encoding': False,
            'full_sourced_einstein_convergence_established': False,
            'generic_fractional_coefficient_refinement': False}
