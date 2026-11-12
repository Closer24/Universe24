"""Research geometry with positive diagonal triads from amplitude pairs.

For each diagonal B_aa=p_a^2+q_a^2, evolve both amplitudes with K_aa/2.
Continuum equations are the triangular frame equations in these variables.
Their common-phase sign lift is NOT degree-three; a successfully checked
staggered phase compiler is needed before claiming an Engine realization.
"""
from fractions import Fraction as F

from universe24.algebra.frame_equations import equations as vacuum_equations
from . import geometry_triangular as triangular

AXES = range(3)
DIAGONALS = tuple(f'B{a}{a}' for a in AXES)
AMPLITUDES = tuple(f'diag_{label}{a}' for a in AXES for label in ('p','q'))
FIELDS = tuple(name for name in triangular.FIELDS if name not in DIAGONALS)+AMPLITUDES


def replace_fields(names):
    """Remove both gauge-redundant and diagonal metric registers; add pairs."""
    return tuple(name for name in names if name not in triangular.ZERO_FIELDS
                 and name not in triangular.ALIASES and name not in DIAGONALS)+AMPLITUDES


def phase_offsets(names):
    """Candidate parity assignment for the separately audited staggered lift."""
    return {name:int(name.startswith(('G','Psi_','Xi_','M'))
                     or (name.startswith('B') and name not in DIAGONALS)) for name in names}


def expand(fields, partial):
    """Expand continuum field jets using the analytic chain rule.

    For a finite-difference partial, the returned derivative of B_aa is NOT
    the literal finite difference of p_a^2+q_a^2. The evolution RHS contains
    no spatial derivative of B and is unaffected. Constraint diagnostics
    must instead call sampled_constraints on complete reconstructed fields.
    """
    result = dict(fields)
    for a in AXES:
        result[f'B{a}{a}'] = fields[f'diag_p{a}']**2+fields[f'diag_q{a}']**2

    def expanded_partial(name, axis):
        if name in DIAGONALS:
            a = int(name[-1])
            return 2*sum(fields[f'diag_{label}{a}']*partial(f'diag_{label}{a}',axis)
                         for label in ('p','q'))
        return partial(name,axis)

    return result, expanded_partial


def equations(fields, partial, *, fermi_equations=vacuum_equations, **kwargs):
    """Return polynomial RHS plus CONTINUUM-JET constraints and diagnostics.

    A centered-difference callback does not turn these returned torsion
    constraints into literal sampled composite-field constraints; use the
    passive sampled_constraints helper for that purpose.
    """
    full, full_partial = expand(fields,partial)
    rhs,constraints,diagnostic = triangular.equations(
        full,full_partial,fermi_equations=fermi_equations,**kwargs)
    for a in AXES:
        del rhs[f'B{a}{a}']
        for label in ('p','q'):
            name = f'diag_{label}{a}'
            rhs[name] = F(1,2)*fields[f'K{a}{a}']*fields[name]
    return rhs,constraints,diagnostic


def sampled_constraints(fields, lat, dx=1, *, fermi_equations=vacuum_equations, **kwargs):
    """Passively compute literal centered constraints after reconstructing B.

    fields maps retained names to arrays on lat. There is no field update,
    projection, or multiplication-rule substitution in these diagnostics.
    """
    dx = F(dx)
    if dx <= 0:
        raise ValueError('dx must be positive')
    full = dict(fields)
    for a in AXES:
        full[f'B{a}{a}'] = fields[f'diag_p{a}']**2+fields[f'diag_q{a}']**2

    def partial(name, axis):
        plus = tuple(int(i == axis) for i in AXES)
        minus = tuple(-v for v in plus)
        return (full[name][lat.shift_index(plus)]-full[name][lat.shift_index(minus)])/(2*dx)

    _,constraints,diagnostic = triangular.equations(
        full,partial,fermi_equations=fermi_equations,**kwargs)
    return constraints,diagnostic


def wronskians(previous,current):
    """Read the three exact two-slice area invariants; no enforcement/reset."""
    return tuple(current[f'diag_p{a}']*previous[f'diag_q{a}']
                 -current[f'diag_q{a}']*previous[f'diag_p{a}'] for a in AXES)
