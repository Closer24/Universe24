"""Experimental 48-channel reversible lift of a quadratic frame leapfrog.

This preserves its encoded map exactly, NOT the Einstein constraint surface.
No matter, physical clock apparatus, or arbitrary precision refinement is
claimed. Noninteger increment coefficients fail instead of being rounded.
"""
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

import sympy as sp

from universe24.algebra.frame_equations import FIELDS, equations
from universe24.core import GearType, Tensor
from universe24.core.lattice import ZERO, OFFSETS


@dataclass(frozen=True)
class FrameProgram:
    tensor: Tensor
    dt: Fraction
    dx: Fraction


def compile_frame48(*, dt=1, dx=1):
    """Construct one horizon-independent tensor for R(x,y)=(y,x+2dt*f(y))."""
    for value in (dt, dx):
        if isinstance(value, (float, bool)):
            raise TypeError('Use exact positive rational dt and dx')
    dt, dx = Fraction(dt), Fraction(dx)
    if dt <= 0 or dx <= 0:
        raise ValueError('dt and dx must be positive')
    return _compile(dt, dx)


@lru_cache(maxsize=8)
def _compile(dt, dx):
    symbols = {(name, offset): sp.Symbol(f'z{index}_{j}')
               for index, name in enumerate(FIELDS) for j, offset in enumerate(OFFSETS)}
    locations = {v: k for k, v in symbols.items()}
    fields = {name: symbols[name, ZERO] for name in FIELDS}
    def partial(name, axis):
        plus = tuple(int(i == axis) for i in range(3))
        return (symbols[name, plus]-symbols[name, tuple(-v for v in plus)])/(2*sp.Rational(dx))
    rhs, _, _ = equations(fields, partial)
    terms = []
    for name in FIELDS:
        # R+R^-1=(2y-F(x),2x+F(y)), F=2dt*f.
        terms += [(f'X.{name}', 6, ((f'Y.{name}', ZERO, 'b'),)),
                  (f'Y.{name}', 6, ((f'X.{name}', ZERO, 'b'),))]
        for term in sp.Add.make_args(sp.expand(2*sp.Rational(dt)*rhs[name])):
            coefficient, product = term.as_coeff_Mul()
            if not coefficient.is_Integer:
                raise ValueError(f'Increment of {name} has noninteger coefficient {coefficient}; '
                                 '48-channel integer refinement is not established')
            factors = []
            for symbol, power in product.as_powers_dict().items():
                if symbol == 1:
                    continue
                factors.extend([locations[symbol]]*int(power))
            for bank, sign in (('X', -1), ('Y', 1)):
                terms.append((f'{bank}.{name}', sign*3*int(coefficient),
                              tuple((f'{bank}.{source}', offset, 'b') for source, offset in factors)))
    gears = [GearType(f'{bank}.{name}', label='audit') for bank in ('X', 'Y') for name in FIELDS]
    return FrameProgram(Tensor(gears, terms, strict_support=True), dt, dx)
