"""Research-only 20-field triangular spatial frame, without projections.

This is a continuum gauge reduction of frame_equations, not a new Engine or
a constraint-preserving discretization. Spatial derivatives stay first order,
and every RHS stays polynomial of degree at most two. Coordinate dependence
is unrestricted within a nondegenerate local synchronous-gauge chart.
"""
from universe24.algebra.frame_equations import FIELDS as FULL_FIELDS
from universe24.algebra.frame_equations import equations as vacuum_equations

AXES = range(3)
ZERO_FIELDS = ('B10', 'B20', 'B21')
ALIASES = {'G021': 'G012'}
FIELDS = tuple(name for name in FULL_FIELDS
               if name not in ZERO_FIELDS and name not in ALIASES)


def expand(fields, partial):
    """Expand a reduced state and its spatial jet by algebraic identities."""
    full = dict(fields)
    full.update({name: 0 for name in ZERO_FIELDS})
    full.update({name: fields[alias] for name, alias in ALIASES.items()})

    def full_partial(name, axis):
        return 0 if name in ZERO_FIELDS else partial(ALIASES.get(name, name), axis)

    return full, full_partial


def rotate_rhs(fields, partial, rhs):
    """Add the angular velocity Omega_ab=sign(b-a)K_ab to frame equations.

    The scalar and dust equations are invariant; spatial vector components
    (scalar gradients and optional Maxwell fields) acquire Omega times vector.
    This function accepts the full Fermi-frame vacuum or sourced RHS.
    """
    result = dict(rhs)
    K = [[fields[f'K{min(a,b)}{max(a,b)}'] for b in AXES] for a in AXES]
    omega = [[(0 if a == b else (1 if a < b else -1))*K[a][b]
              for b in AXES] for a in AXES]

    def gamma(a, b, c):
        return 0 if a == b else (1 if a < b else -1)*fields[f'G{min(a,b)}{max(a,b)}{c}']

    for a in AXES:
        for i in AXES:
            result[f'B{a}{i}'] += sum(omega[a][b]*fields[f'B{b}{i}'] for b in AXES)
        for b in range(a, 3):
            result[f'K{a}{b}'] += sum(omega[a][d]*K[d][b]+omega[b][d]*K[a][d] for d in AXES)
        for b in range(a+1, 3):
            for c in AXES:
                result[f'G{a}{b}{c}'] += sum(
                    omega[a][d]*gamma(d,b,c)+omega[b][d]*gamma(a,d,c)
                    +omega[c][d]*gamma(a,b,d) for d in AXES)
                result[f'G{a}{b}{c}'] -= sum(fields[f'B{c}{i}']*partial(f'K{a}{b}',i) for i in AXES)
    vector_prefixes = ('Psi_phi', 'Psi_chi', 'Xi_phi', 'Xi_chi', 'A', 'E', 'M')
    for prefix in vector_prefixes:
        if all(f'{prefix}{a}' in result for a in AXES):
            for a in AXES:
                result[f'{prefix}{a}'] += sum(omega[a][b]*fields[f'{prefix}{b}'] for b in AXES)
    return result


def equations(fields, partial, *, fermi_equations=vacuum_equations, **kwargs):
    """Return reduced RHS, unchanged constraints, and Fermi diagnostics.

    Supply fermi_equations=matter_equations.equations to attach its matter
    fields, with their original keyword arguments. No field is reset after
    initialization: the eliminated values are exact parametrization identities.
    """
    full, full_partial = expand(fields, partial)
    rhs, constraints, diagnostic = fermi_equations(full, full_partial, **kwargs)
    rhs = rotate_rhs(full, full_partial, rhs)
    return {name: value for name, value in rhs.items()
            if name not in ZERO_FIELDS and name not in ALIASES}, constraints, diagnostic
