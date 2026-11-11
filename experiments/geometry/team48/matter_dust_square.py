"""PR39's signed square-density dust, as an optional research adapter.

This changes the discrete dust trajectory. It is not a projection of the raw
rho_dust trajectory and does not enlarge the field/channel count.
"""
from fractions import Fraction

from . import matter_equations as neutral
from . import matter_charged as charged


def fields_for(fields):
    return tuple('dust_amplitude' if name == 'rho_dust' else name for name in fields)


FIELDS = fields_for(neutral.FIELDS)
FIELDS_WITH_MAXWELL = fields_for(neutral.FIELDS_WITH_MAXWELL)
FIELDS_CHARGED = fields_for(charged.FIELDS)


def equations(fields, partial, *, base_equations=neutral.equations, **kwargs):
    """Evaluate a coupled frame system with rho_d=d^2 and d_dot=K*d/2.

    dust_amplitude is signed and retained through zero; there is no clipping,
    square-root calculation or discarded sign. Integer d restricts represented
    densities to squares in the declared units. Conservation is a separate gate.
    """
    expanded = dict(fields)
    amplitude = fields['dust_amplitude']
    expanded['rho_dust'] = amplitude*amplitude

    def expanded_partial(name, axis):
        if name == 'rho_dust':
            raise ValueError('The supported normal-dust systems do not differentiate rho_dust; no discrete product rule is inserted')
        return partial(name,axis)

    rhs,constraints,diagnostic = base_equations(expanded,expanded_partial,**kwargs)
    rhs = dict(rhs)
    del rhs['rho_dust']
    trace = sum(fields[f'K{a}{a}'] for a in range(3))
    rhs['dust_amplitude'] = Fraction(1,2)*trace*amplitude
    diagnostic = dict(diagnostic)
    diagnostic.update(dust_density=amplitude*amplitude,dust_encoding='signed_square')
    return rhs,constraints,diagnostic
