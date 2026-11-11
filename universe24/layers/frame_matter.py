"""One 70-channel candidate: frame, complex scalar and normal-comoving dust.

The exact pair map is established; general Einstein constraints, physical
clocks and integer refinement are not. The vacuum Frame48 stays unchanged.
"""
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

import sympy as sp

from universe24.algebra.frame_matter import FIELDS, equations, exact_parameter
from universe24.core import GearType, Tensor
from universe24.core.lattice import ZERO, OFFSETS


@dataclass(frozen=True)
class MatterFrameProgram:
    tensor: Tensor
    dt: Fraction
    dx: Fraction
    mass_squared: Fraction


def compile_matter_frame(*, dt=1, dx=1, mass_squared=1):
    """Compile R(x,y)=(y,x+2dt*f(y)) without a runtime solver or denominator."""
    return _compile(exact_parameter(dt, 'dt', positive=True),
                    exact_parameter(dx, 'dx', positive=True),
                    exact_parameter(mass_squared, 'mass_squared'))


@lru_cache(maxsize=8)
def _compile(dt, dx, mass_squared):
    symbols = {(name, offset): sp.Symbol(f'z{index}_{j}')
               for index, name in enumerate(FIELDS) for j, offset in enumerate(OFFSETS)}
    locations = {v: k for k, v in symbols.items()}
    fields = {name: symbols[name, ZERO] for name in FIELDS}
    def partial(name, axis):
        plus = tuple(int(i == axis) for i in range(3))
        return (symbols[name, plus]-symbols[name, tuple(-v for v in plus)])/(2*sp.Rational(dx))
    rhs, _, _ = equations(fields, partial, mass_squared)
    terms = []
    for name in FIELDS:
        terms += [(f'X.{name}', 6, ((f'Y.{name}', ZERO, 'b'),)),
                  (f'Y.{name}', 6, ((f'X.{name}', ZERO, 'b'),))]
        for term in sp.Add.make_args(sp.expand(2*sp.Rational(dt)*rhs[name])):
            coefficient, product = term.as_coeff_Mul()
            if not coefficient.is_Integer:
                raise ValueError(f'Increment of {name} has noninteger coefficient {coefficient}; '
                                 '70-channel integer refinement is not established')
            factors = []
            for symbol, power in product.as_powers_dict().items():
                if symbol != 1:
                    factors.extend([locations[symbol]]*int(power))
            for bank, sign in (('X', -1), ('Y', 1)):
                terms.append((f'{bank}.{name}', sign*3*int(coefficient),
                              tuple((f'{bank}.{source}', offset, 'b') for source, offset in factors)))
    gears = [GearType(f'{bank}.{name}', label='audit') for bank in ('X', 'Y') for name in FIELDS]
    return MatterFrameProgram(Tensor(gears, terms, strict_support=True), dt, dx, mass_squared)
