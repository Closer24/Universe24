"""Einstein--complex-scalar--dust frame equations, c=8*pi*G=1, Lambda=0.

Synchronous/Fermi gauge, V=m^2*(phi^2+chi^2)/2, normal-comoving dust.
Continuum identities require frame and scalar-gradient constraints.
No discrete conservation is assumed.
"""
from fractions import Fraction

import numpy as np

from universe24.algebra.frame_equations import (
    AXES, FIELDS as GEOMETRY_FIELDS, SYMMETRIC, equations as vacuum_equations)
from universe24.algebra.null_covector import integer_array

COMPONENTS = (('phi', 'Pi', 'Q'), ('chi', 'Pi_chi', 'W'))
FIELDS = GEOMETRY_FIELDS + ('phi', 'Pi', 'Q0', 'Q1', 'Q2',
                            'chi', 'Pi_chi', 'W0', 'W1', 'W2', 'dust_amplitude')


def exact_parameter(value, name, *, positive=False):
    if isinstance(value, (float, np.floating, bool, np.bool_)):
        raise TypeError(f'{name} must be exact, not floating or boolean')
    value = Fraction(value)
    if value < 0 or (positive and value == 0):
        raise ValueError(f'{name} must be {"positive" if positive else "nonnegative"}')
    return value


def stress_energy(fields, mass_squared=1):
    """Orthonormal rho, j_a=-T_0a and S_ab, plus the complex-field current."""
    m2 = exact_parameter(mass_squared, 'mass_squared')
    components = [(fields[f], fields[p], [fields[f'{q}{a}'] for a in AXES]) for f, p, q in COMPONENTS]
    pi2 = sum(pi*pi for _, pi, _ in components)
    q2 = sum(v*v for _, _, q in components for v in q)
    potential = Fraction(1, 2)*m2*sum(phi*phi for phi, _, _ in components)
    dust_density = fields['dust_amplitude']**2
    rho = Fraction(1, 2)*(pi2+q2)+potential+dust_density
    stress = [[sum(q[a]*q[b] for _, _, q in components)+(Fraction(1, 2)*(pi2-q2)-potential)*int(a == b)
               for b in AXES] for a in AXES]
    return {'rho': rho, 'j': [-sum(pi*q[a] for _, pi, q in components) for a in AXES],
            'S': stress, 'V': potential, 'rho_dark': dust_density,
            'charge': fields['phi']*fields['Pi_chi']-fields['chi']*fields['Pi'],
            'charge_flux': [fields['chi']*fields[f'Q{a}']-fields['phi']*fields[f'W{a}'] for a in AXES]}


def equations(fields, partial, mass_squared=1):
    """Return coupled RHS, constraints and stress; partial is a coordinate derivative."""
    m2 = exact_parameter(mass_squared, 'mass_squared')
    rhs, constraints, _ = vacuum_equations(fields, partial)
    matter = stress_energy(fields, m2)
    def derivative(name, a):
        return sum(fields[f'B{a}{i}']*partial(name, i) for i in AXES)
    def gamma(a, b, c):
        return (0 if a == b else (1 if a < b else -1)
                *fields[f'G{min(a,b)}{max(a,b)}{c}'])
    def k(a, b):
        return fields[f'K{min(a,b)}{max(a,b)}']
    trace = sum(k(a, a) for a in AXES)
    for a, b in SYMMETRIC:
        # Spatial trace reversal for the same matter as the default ADM.
        rhs[f'K{a}{b}'] -= (sum(fields[f'{q}{a}']*fields[f'{q}{b}'] for _, _, q in COMPONENTS)
                           +(matter['V']+Fraction(1, 2)*matter['rho_dark'])*int(a == b))
    for phi, pi, gradient in COMPONENTS:
        q = [fields[f'{gradient}{a}'] for a in AXES]
        rhs[phi] = fields[pi]
        rhs[pi] = (trace*fields[pi]-m2*fields[phi]
                   +sum(derivative(f'{gradient}{a}', a)-sum(gamma(b, a, a)*q[b] for b in AXES)
                        for a in AXES))
        for a in AXES:
            rhs[f'{gradient}{a}'] = derivative(pi, a)+sum(k(a, b)*q[b] for b in AXES)
            constraints[f'{gradient}_gradient{a}'] = q[a]-derivative(phi, a)
    # rho_dark=d^2: nonnegativity is algebraic, not a runtime projection.
    # Signed d is retained across zero; its sign is never discarded.
    rhs['dust_amplitude'] = Fraction(1, 2)*trace*fields['dust_amplitude']
    for a in AXES:
        constraints[f'M{a}'] -= matter['j'][a]
    constraints['H'] -= 2*matter['rho']
    return rhs, constraints, matter


def sampled(values, lat, dx=1, mass_squared=1):
    """Exact integer snapshots and centered differences; includes a flux defect.

    The local energy-balance defect uses differences of the actual composite
    flux, not a substituted continuum product rule. It is passive, never a veto.
    """
    dx = exact_parameter(dx, 'dx', positive=True)
    m2 = exact_parameter(mass_squared, 'mass_squared')
    values = integer_array(values)
    if values.shape != (35, lat.N):
        raise ValueError('Expected 35 fields on the supplied lattice')
    fields = dict(zip(FIELDS, values))
    def difference(row, axis):
        offset = tuple(int(i == axis) for i in AXES)
        return (row[lat.shift_index(offset)]-row[lat.shift_index(tuple(-v for v in offset))])/(2*dx)
    rhs, constraints, matter = equations(fields, lambda name, i: difference(fields[name], i), m2)
    def divergence(flux):
        result = sum(fields[f'B{a}{i}']*difference(flux[a], i) for a in AXES for i in AXES)
        for a in AXES:
            for b in AXES:
                if a != b:
                    gamma = (1 if b < a else -1)*fields[f'G{min(a,b)}{max(a,b)}{a}']
                    result -= gamma*flux[b]
        return result
    rho_dot = 2*fields['dust_amplitude']*rhs['dust_amplitude']+sum(fields[pi]*rhs[pi]+m2*fields[phi]*rhs[phi]
        +sum(fields[f'{q}{a}']*rhs[f'{q}{a}'] for a in AXES) for phi, pi, q in COMPONENTS)
    work = sum(fields[f'K{min(a,b)}{max(a,b)}']*matter['S'][a][b] for a in AXES for b in AXES)
    matter['energy_balance_defect'] = (rho_dot+divergence(matter['j'])
        -sum(fields[f'K{a}{a}'] for a in AXES)*matter['rho']-work)
    charge_dot = (rhs['phi']*fields['Pi_chi']+fields['phi']*rhs['Pi_chi']
                  -rhs['chi']*fields['Pi']-fields['chi']*rhs['Pi'])
    matter['charge_balance_defect'] = (charge_dot+divergence(matter['charge_flux'])
        -sum(fields[f'K{a}{a}'] for a in AXES)*matter['charge'])
    return rhs, constraints, matter
