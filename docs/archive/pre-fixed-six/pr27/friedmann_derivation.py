"""Symbolically derive the optional radiation sector from Einstein's action.

Units c=kappa=1, k=Lambda=0. Matter is a homogeneous perfect radiation
fluid with fixed comoving energy E=rho*a**4. It is not microscopic photons.
The lapse is varied BEFORE choosing conformal-time gauge n=1.
"""
from functools import lru_cache
import sympy as sp


def curvature(metric, coords):
    """Compute connection, mixed Riemann, Ricci and Einstein from a metric."""
    inv = metric.inv()
    gamma = [[[sp.simplify(sum(inv[r, s] * (
        sp.diff(metric[s, j], coords[i]) + sp.diff(metric[s, i], coords[j])
        - sp.diff(metric[i, j], coords[s])) for s in range(4)) / 2)
        for j in range(4)] for i in range(4)] for r in range(4)]
    riemann = [[[[sp.simplify(
        sp.diff(gamma[r][j][s], coords[i]) - sp.diff(gamma[r][i][s], coords[j])
        + sum(gamma[r][i][q] * gamma[q][j][s] - gamma[r][j][q] * gamma[q][i][s]
              for q in range(4)))
        for j in range(4)] for i in range(4)] for s in range(4)] for r in range(4)]
    ricci = sp.Matrix(4, 4, lambda s, j: sum(riemann[r][s][r][j] for r in range(4)))
    scalar = sp.simplify(sum(inv[i, j] * ricci[i, j] for i in range(4) for j in range(4)))
    einstein = (ricci - metric * scalar / 2).applyfunc(sp.simplify)
    return gamma, riemann, ricci, scalar, einstein


@lru_cache(maxsize=1)
def audit():
    eta, x, y, z = sp.symbols('eta x y z', real=True)
    a = sp.Function('a', positive=True)(eta)
    n = sp.Function('n', positive=True)(eta)
    energy = sp.Symbol('E', nonnegative=True)
    coords = (eta, x, y, z)
    ap, app = sp.diff(a, eta), sp.diff(a, eta, 2)
    metric = sp.diag(-a**2 * n**2, a**2, a**2, a**2)
    gamma, riemann, ricci, scalar, einstein = curvature(metric, coords)
    # EH density = reduced gravity density + an explicit boundary derivative.
    gravity = -3 * ap**2 / n
    boundary = sp.diff(3 * a * ap / n, eta)
    eh_identity = sp.simplify(n * a**4 * scalar / 2 - gravity - boundary) == 0
    # Fixed-comoving-energy fluid Routhian: -N*rho*a^3, with N=a*n.
    lagrangian = gravity - n * energy
    lapse_equation = sp.diff(lagrangian, n)
    evolution = sp.simplify(sp.diff(sp.diff(lagrangian, ap), eta) - sp.diff(lagrangian, a))
    assert sp.simplify(lapse_equation - (3 * ap**2 / n**2 - energy)) == 0
    assert sp.simplify(evolution + 6 * sp.diff(ap / n, eta)) == 0

    # Independently calculate perfect-fluid T, not by setting T=G.
    rho = energy / a**4
    pressure = rho / 3
    four_velocity = sp.Matrix([1 / (a * n), 0, 0, 0])
    cov_velocity = metric * four_velocity
    stress = (rho + pressure) * cov_velocity * cov_velocity.T + pressure * metric
    gauge = {n: 1, sp.diff(n, eta): 0, sp.diff(n, eta, 2): 0}
    on_shell = {energy: 3 * ap**2, app: 0}
    gauge_g = einstein.subs(gauge).applyfunc(sp.simplify)
    gauge_t = stress.subs(gauge).applyfunc(sp.simplify)
    residual = (gauge_g - gauge_t).applyfunc(lambda v: sp.simplify(v.subs(on_shell)))
    expected_g = sp.diag(3 * ap**2 / a**2,
                        *[(ap**2 - 2 * a * app) / a**2] * 3)
    assert (gauge_g - expected_g).applyfunc(sp.simplify) == sp.zeros(4)
    # All four covariant conservation equations, including the lapse.
    mixed_stress = metric.inv() * stress
    divergences = [sp.simplify(sum(sp.diff(mixed_stress[mu, nu], coords[mu])
        + sum(gamma[mu][mu][q] * mixed_stress[q, nu]
              - gamma[q][mu][nu] * mixed_stress[mu, q] for q in range(4))
        for mu in range(4))) for nu in range(4)]

    # Independent curvature invariant: radiation has R=0 but is not flat.
    diagonal = [metric[i, i] for i in range(4)]
    kretschmann = sp.simplify(sum(
        diagonal[r] / (diagonal[s] * diagonal[i] * diagonal[j]) * riemann[r][s][i][j]**2
        for r in range(4) for s in range(4) for i in range(4) for j in range(4)))
    radiation_k = sp.simplify(kretschmann.subs(gauge).subs(app, 0))
    assert sp.simplify(radiation_k - 24 * ap**4 / a**8) == 0

    previous, current, following, h = sp.symbols('a_previous a_current a_next h', real=True)
    lapse_left, lapse_right = sp.symbols('n_left n_right', positive=True)
    discrete = lambda left, right, lapse: -3 * (right - left)**2 / (h * lapse) - h * lapse * energy
    discrete_el = sp.diff(discrete(previous, current, lapse_left)
                         + discrete(current, following, lapse_right), current)
    discrete_gauge_el = sp.simplify(discrete_el.subs({lapse_left: 1, lapse_right: 1}))
    discrete_constraint = sp.simplify(sp.diff(discrete(current, following, lapse_right), lapse_right)
                                      .subs(lapse_right, 1) / h)
    assert sp.simplify(discrete_gauge_el - 6 * (following - 2 * current + previous) / h) == 0
    assert sp.simplify(discrete_constraint - (3 * ((following - current) / h)**2 - energy)) == 0
    checks = {
        'EH_density_equals_reduced_action_plus_boundary': eh_identity,
        'lapse_varied_before_gauge_fixing': True,
        'all_16_Einstein_residuals_zero_on_shell': residual == sp.zeros(4),
        'all_4_stress_divergences_zero': all(v == 0 for v in divergences),
        'scalar_curvature_zero_on_shell': sp.simplify(scalar.subs(gauge).subs(app, 0)) == 0,
        'nonzero_radiation_Kretschmann_verified': True,
        'discrete_evolution_derived': True,
        'discrete_lapse_constraint_derived': True,
    }
    assert all(checks.values())
    return {'checks': checks, 'units': 'c=kappa=1; k=Lambda=0',
            'matter_assumption': 'homogeneous perfect fluid, p=rho/3, E=rho*a^4 fixed',
            'reduced_lagrangian': str(lagrangian), 'lapse_equation': str(lapse_equation),
            'evolution_equation': str(evolution), 'discrete_evolution': str(discrete_gauge_el),
            'discrete_constraint': str(discrete_constraint),
            'G_conformal': [[str(v) for v in gauge_g.row(i)] for i in range(4)],
            'T_conformal': [[str(v) for v in gauge_t.row(i)] for i in range(4)],
            'Kretschmann_on_shell': str(radiation_k)}
