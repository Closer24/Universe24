"""Vacuum frame equations in synchronous, Fermi-propagated time gauge.

Continuum identities on the torsion-free constraint surface, not a claim that
ordinary differences preserve it. This is not a transcription of WEBB's
constraint-added hyperbolic system. See docs/FRAME48_RESEARCH.md.
"""
from fractions import Fraction

import numpy as np

AXES = range(3)
SYMMETRIC = tuple((a, b) for a in AXES for b in AXES if a <= b)
ANTISYMMETRIC = tuple((a, b) for a in AXES for b in AXES if a < b)
FIELDS = tuple([f'B{a}{i}' for a in AXES for i in AXES]
               + [f'K{a}{b}' for a, b in SYMMETRIC]
               + [f'G{a}{b}{c}' for a, b in ANTISYMMETRIC for c in AXES])


def equations(fields, partial):
    """Return RHS and constraints for scalars, exact arrays or symbolic jets.

    e_a=B_a^i partial_i, K_ab=-<nabla_a n,e_b>,
    G^a_bc=<nabla_(e_c) e_b,e_a>. K is symmetric; G is antisymmetric
    in a,b. partial(name,i) is the coordinate spatial derivative.
    """
    B = [[fields[f'B{a}{i}'] for i in AXES] for a in AXES]
    K = [[fields[f'K{min(a,b)}{max(a,b)}'] for b in AXES] for a in AXES]
    def gamma(a, b, c):
        return (0 if a == b else (1 if a < b else -1)*fields[f'G{min(a,b)}{max(a,b)}{c}'])
    def dg(a, b, c, direction):
        return (0 if a == b else (1 if a < b else -1)*sum(
            B[direction][i]*partial(f'G{min(a,b)}{max(a,b)}{c}', i) for i in AXES))
    def dk(a, b, direction):
        return sum(B[direction][i]*partial(f'K{min(a,b)}{max(a,b)}', i) for i in AXES) - sum(
            gamma(d, a, direction)*K[d][b]+gamma(d, b, direction)*K[a][d] for d in AXES)
    def structure(a, b, c):
        return gamma(a, c, b)-gamma(a, b, c)
    def curvature(a, b, c, d):
        return dg(a, b, d, c)-dg(a, b, c, d)+sum(
            gamma(a, e, c)*gamma(e, b, d)-gamma(a, e, d)*gamma(e, b, c)
            - structure(e, c, d)*gamma(a, b, e) for e in AXES)
    ricci = [[sum(curvature(c, a, c, b) for c in AXES) for b in AXES] for a in AXES]
    trace = sum(K[a][a] for a in AXES)
    rhs = {f'B{a}{i}': sum(K[a][b]*B[b][i] for b in AXES) for a in AXES for i in AXES}
    # Upper-triangular closure off the constraint surface is explicit. The
    # antisymmetric Ricci defect is measured, never silently projected away.
    rhs.update({f'K{a}{b}': ricci[a][b]+trace*K[a][b] for a, b in SYMMETRIC})
    rhs.update({f'G{a}{b}{c}': dk(b, c, a)-dk(a, c, b)
                +sum(gamma(a, b, d)*K[d][c] for d in AXES)
                for a, b in ANTISYMMETRIC for c in AXES})
    constraints = {'H': sum(ricci[a][a] for a in AXES)+trace*trace
                   -sum(K[a][b]*K[a][b] for a in AXES for b in AXES)}
    constraints.update({f'M{a}': sum(dk(a, b, b)-dk(b, b, a) for b in AXES) for a in AXES})
    constraints.update({f'C{a}{b}{i}': sum(
        B[a][j]*partial(f'B{b}{i}', j)-B[b][j]*partial(f'B{a}{i}', j) for j in AXES)
        -sum(structure(c, a, b)*B[c][i] for c in AXES)
        for a, b in ANTISYMMETRIC for i in AXES})
    constraints.update({f'Ricci_antisym{a}{b}': ricci[a][b]-ricci[b][a] for a, b in ANTISYMMETRIC})
    return rhs, constraints, ricci


def sampled(values, lat, dx=Fraction(1)):
    """Passive/evaluation helper, with exact centered coordinate differences."""
    dx = Fraction(dx)
    if dx <= 0:
        raise ValueError('dx must be positive')
    values = np.asarray(values, dtype=object)
    if values.shape != (24, lat.N):
        raise ValueError('Expected 24 fields on the supplied lattice')
    fields = dict(zip(FIELDS, values))
    def partial(name, axis):
        plus = tuple(int(i == axis) for i in AXES)
        minus = tuple(-v for v in plus)
        return (fields[name][lat.shift_index(plus)]-fields[name][lat.shift_index(minus)])/(2*dx)
    return equations(fields, partial)
