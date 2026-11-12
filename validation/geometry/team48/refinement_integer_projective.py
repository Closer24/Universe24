"""Exact integer reversible homogenization of an explicit polynomial Euler step.

This changes the sign-leapfrog integrator. One retained common denominator
replaces its computational phase. The passive ratio identity is proved in
refinement_integer_report.md; denominator bit length grows exponentially in
the step count. This is a research encoding, not an accepted GR solver.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import reduce
from math import lcm

import numpy as np
import sympy as sp

from universe24.core import GearType, State, Tensor
from universe24.core.lattice import OFFSETS, ZERO, lattice


@dataclass(frozen=True)
class ProjectiveProgram:
    tensor: Tensor
    fields: tuple[str, ...]
    dt: F
    dx: F
    degree: int
    multiplier: int


def compile_projective(fields, equation_builder, *, dt=1, dx=1, degree=2):
    """Compile P'=C[D^(d-1)P+h F_hom(P,D)]-P_old, D'=C D^d-D_old.

    C clears the *static* rational coefficients and is at least two. It is
    an integer tensor multiplier, never an Engine denominator. Homogenizing
    onsite and single-edge polynomials preserves their support. D is an
    actual channel, not an observer-generated number or runtime injection.
    """
    if degree not in (2, 3):
        raise ValueError('Supported homogenization degree is 2 or 3')
    if any(isinstance(v, (float, bool, np.floating, np.bool_)) for v in (dt, dx)):
        raise TypeError('Use exact rational dt and dx')
    dt, dx = F(dt), F(dx)
    if dt <= 0 or dx <= 0:
        raise ValueError('dt and dx must be positive')
    fields = tuple(fields)
    if not fields or len(set(fields)) != len(fields) or len(fields)+1 > 48:
        raise ValueError('Unique nonempty fields plus denominator must fit 48 channels')
    symbols = {(name, offset): sp.Symbol(f'p{i}_{j}')
               for i, name in enumerate(fields) for j, offset in enumerate(OFFSETS)}
    locations = {symbol: address for address, symbol in symbols.items()}
    here = {name: symbols[name, ZERO] for name in fields}

    def partial(name, axis):
        plus = tuple(int(i == axis) for i in range(3))
        minus = tuple(-v for v in plus)
        return (symbols[name, plus]-symbols[name, minus])/(2*sp.Rational(dx))

    result = equation_builder(here, partial)
    rhs = result[0] if isinstance(result, tuple) else result
    denominator = 'projective.denominator'
    parsed = []
    for name in fields:
        for term in sp.Add.make_args(sp.expand(sp.Rational(dt)*rhs[name])):
            if not term:
                continue
            coefficient, product = term.as_coeff_Mul()
            if not coefficient.is_Rational:
                raise ValueError('Only exact rational polynomial coefficients are supported')
            factors = []
            for symbol, power in product.as_powers_dict().items():
                if symbol == 1:
                    continue
                if symbol not in locations or not power.is_Integer or power < 0:
                    raise ValueError('RHS must be a polynomial in the declared stencil')
                source, offset = locations[symbol]
                factors.extend([(f'projective.{source}', offset, 'b')]*int(power))
            if len(factors) > degree:
                raise ValueError('RHS exceeds the declared homogenization degree')
            factors.extend([(denominator, ZERO, 'b')]*(degree-len(factors)))
            parsed.append((name, F(coefficient), tuple(factors)))
    multiplier = max(2, reduce(lcm, (c.denominator for _, c, _ in parsed), 1))
    # Every u is divisible by three: all six valid core carries are retained
    # unchanged and ell is exactly the indicated integer polynomial.
    terms = [(denominator, 3*multiplier, ((denominator, ZERO, 'b'),)*degree)]
    for name in fields:
        terms.append((f'projective.{name}', 3*multiplier,
                      ((f'projective.{name}', ZERO, 'b'),)
                      +((denominator, ZERO, 'b'),)*(degree-1)))
    for name, coefficient, factors in parsed:
        terms.append((f'projective.{name}', 3*int(multiplier*coefficient), factors))
    tensor = Tensor([GearType(denominator, label='audit')]
                    +[GearType(f'projective.{name}', label='audit') for name in fields],
                    terms, strict_support=True)
    return ProjectiveProgram(tensor, fields, dt, dx, degree, multiplier)


def prepare(program, current, *, L, denominator=None, remainders=None):
    """Prepare rational initial physical data; previous retained registers are zero.

    Preparation uses no future solution and no evolution callback. D_old=0
    is a memory boundary, not a second physical time slice. Only current
    P/D is the physical readout; the first Engine step is exactly Euler.
    """
    current = np.asarray(current, dtype=object)
    shape = (len(program.fields), lattice(L).N)
    if current.shape != shape:
        raise ValueError(f'Expected current physical data shape {shape}')
    values = []
    for value in current.flat:
        if isinstance(value, (float, bool, np.floating, np.bool_)):
            raise TypeError('Initial physical data must be exact rational')
        values.append(F(value))
    needed = reduce(lcm, (v.denominator for v in values), 1)
    if denominator is None:
        denominator = max(2, needed)
    if type(denominator) is not int or denominator < 2 or denominator % needed:
        raise ValueError('Denominator must be an integer >=2 divisible by every seed denominator')
    b = np.vstack((np.full((1, shape[1]), denominator, dtype=object),
                   np.array([int(v*denominator) for v in values], dtype=object).reshape(shape)))
    a = np.zeros_like(b)
    r = np.zeros_like(b) if remainders is None else np.asarray(remainders, dtype=object)
    if r.shape != b.shape or any(type(v) is not int or not 0 <= v < 6 for v in r.flat):
        raise ValueError('Provide one exact legal core carry per retained channel/node')
    return State(L, a, b, r)


def readout(program, state):
    """Read current P/D only on the proved uniform positive-denominator domain."""
    if state.G != len(program.fields)+1:
        raise ValueError('Wrong state allocation')
    d = int(state.b[0, 0])
    if d <= 0 or not np.all(state.b[0] == d) or not np.all(state.a[0] == state.a[0, 0]):
        raise ValueError('Denominator must be positive and both retained slices uniform')
    return np.array([F(int(v), d) for v in state.b[1:].flat], dtype=object).reshape(state.b[1:].shape)


def build_charged(*, dt=1, dx=1, mass_squared=0, cosmological=0, coupling=1):
    """The actual 40-field triangular Einstein/scalar/dust/Maxwell proposal."""
    from . import geometry_triangular as geometry
    from . import matter_charged as charged
    from . import matter_dust_square as square
    from . import matter_equations as matter
    fields = (geometry.FIELDS + tuple(charged.rename(name) for name in matter.SCALAR_FIELDS)
              + ('dust_amplitude',) + matter.MAXWELL_FIELDS + tuple(f'A{a}' for a in range(3)))

    def equations(fields, partial):
        return geometry.equations(fields, partial, fermi_equations=square.equations,
                                  base_equations=charged.equations,
                                  mass_squared=mass_squared, cosmological=cosmological,
                                  coupling=coupling)

    return compile_projective(fields, equations, dt=dt, dx=dx)
