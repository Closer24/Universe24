"""General nonlinear 4D Einstein readout and direct-compilation barriers.

This is an observer/reference audit, NOT an evolution engine. Exact rational
metric jets can be reconstructed from signed tangent-edge data. A small or
zero residual at one point does not establish a solution on a whole domain.
"""
from itertools import product
import sympy as sp
from universe24.core import Tensor
from universe24.core.tensor import LocalityError
from universe24.observe.simplex_metric import EDGES, exact_matrix, inertia

FOUR = range(4)


def einstein_from_jet(metric, first, second):
    """g, partial_c g, partial_c partial_d g -> full nonlinear curvature.

    All entries must be exact rationals; first[c] and second[c][d] are 4x4.
    No field equation, symmetry ansatz, or assumed matter source is used here.
    """
    g = exact_matrix(metric)
    if g.shape != (4, 4) or g != g.T or inertia(g) != (1, 3, 0):
        raise ValueError('expected a Lorentzian four-metric')
    if len(first) != 4 or len(second) != 4 or any(len(row) != 4 for row in second):
        raise ValueError('expected four first derivatives and 4x4 second derivatives')
    dg = [exact_matrix(item) for item in first]
    ddg = [[exact_matrix(item) for item in row] for row in second]
    if any(item.shape != (4, 4) or item != item.T for item in dg + [v for row in ddg for v in row]):
        raise ValueError('metric derivative matrices must be symmetric 4x4')
    if any(ddg[c][d] != ddg[d][c] for c, d in product(FOUR, repeat=2)):
        raise ValueError('second partial derivatives must commute')
    inv = g.inv()
    dinv = [-inv * item * inv for item in dg]
    connection = lambda s, i, j: dg[i][s, j] + dg[j][s, i] - dg[s][i, j]
    gamma = [[[sum(inv[r, s] * connection(s, i, j) for s in FOUR)/2
               for j in FOUR] for i in FOUR] for r in FOUR]
    dgamma = [[[[sum(dinv[c][r, s]*connection(s, i, j) + inv[r, s]*(
        ddg[c][i][s, j] + ddg[c][j][s, i] - ddg[c][s][i, j]) for s in FOUR)/2
        for j in FOUR] for i in FOUR] for r in FOUR] for c in FOUR]
    riemann = [[[[dgamma[i][r][j][s] - dgamma[j][r][i][s]
        + sum(gamma[r][i][q]*gamma[q][j][s] - gamma[r][j][q]*gamma[q][i][s] for q in FOUR)
        for j in FOUR] for i in FOUR] for s in FOUR] for r in FOUR]
    ricci = sp.Matrix(4, 4, lambda s, j: sum(riemann[r][s][r][j] for r in FOUR))
    scalar = sum(inv[i, j]*ricci[i, j] for i, j in product(FOUR, repeat=2))
    einstein = ricci - scalar*g/2
    assert ricci == ricci.T and einstein == einstein.T
    return {'metric': g, 'inverse': inv, 'Gamma': gamma, 'Riemann': riemann,
            'Ricci': ricci, 'R': scalar, 'G': einstein}


def symbolic_jet(metric, coords, point):
    """Sample analytic metric data for independent validation, never evolution."""
    evaluate = lambda matrix: matrix.subs(point).applyfunc(sp.simplify)
    first = [metric.diff(coord) for coord in coords]
    second = [[item.diff(coord) for coord in coords] for item in first]
    return evaluate(metric), [evaluate(v) for v in first], [[evaluate(v) for v in row] for row in second]


def polarization(values):
    """Linear Gram map, also valid on derivatives which are not metrics."""
    if set(values) != set(EDGES):
        raise ValueError('all ten signed squared edges or their derivatives are required')
    values = {key: exact_matrix([[value]])[0] for key, value in values.items()}
    return sp.Matrix(4, 4, lambda i, j: (values[0, i+1] + values[0, j+1]
        - (0 if i == j else values[tuple(sorted((i+1, j+1)))]))/2)


def einstein_from_link_jet(values, first, second):
    """Use all ten signed squared edges in a fixed coordinate tangent basis.

    Lengths at one time and point alone do not supply the required derivatives.
    """
    return einstein_from_jet(polarization(values), [polarization(v) for v in first],
                            [[polarization(v) for v in row] for row in second])


def compilation_barriers():
    """Concrete counterexamples to direct substitutions, not a universal no-go."""
    locality_rejected = False
    try:
        Tensor(['metric', 'matter'], [('metric', 1, (
            ('matter', (1, 0, 0), 'b'), ('matter', (0, 1, 0), 'b')))])
    except LocalityError:
        locality_rejected = True
    fminus, fzero, fplus = 1, 2, 4
    difference = sp.Rational(fplus*fplus-fminus*fminus, 2)
    leibniz = 2*fzero*sp.Rational(fplus-fminus, 2)
    assert difference-leibniz == sp.Rational(3, 2)
    x = sp.Symbol('x')
    inverse_component = 1/(1+x)
    fourth_derivative = sp.diff(inverse_component, x, 4)
    assert fourth_derivative != 0
    assert locality_rejected
    return {
        'direct_cross_axis_stress_monomial_rejected': locality_rejected,
        'ordinary_central_difference_Leibniz_defect': str(difference-leibniz),
        'inverse_metric_component': str(inverse_component),
        'inverse_component_fourth_derivative': str(fourth_derivative),
        'scope': 'These reject a direct one-step substitution in current fields. Auxiliary fields, different variables, staged computation, and consistent discrete actions are not ruled out.',
        'this_observer_compiles_dynamics': False,
        'staged_ADM_compiler_available': True,
        'staged_implementation': 'experiments/geometry/adm_equations.py',
    }


def audit():
    t, r, theta, phi = sp.symbols('t r theta phi', real=True)
    # Curved vacuum, including all non-linear connection products.
    f = 1-2/r
    schwarzschild = sp.diag(-f, 1/f, r*r, r*r*sp.sin(theta)**2)
    result = einstein_from_jet(*symbolic_jet(schwarzschild, (t, r, theta, phi),
                                            {t: 0, r: 10, theta: sp.pi/2, phi: 0}))
    nonzero = sum(v != 0 for a in result['Riemann'] for b in a for c in b for v in c)
    assert result['G'] == sp.zeros(4) and nonzero > 0
    # Off-diagonal and spatially dependent chart of an on-shell radiation metric.
    eta, x, y, z = sp.symbols('eta x y z', real=True)
    coordinates = sp.Matrix([eta+x/3, x, y, z])
    jacobian = coordinates.jacobian([eta, x, y, z])
    scale = 2 + coordinates[0]/8
    shifted = jacobian.T * sp.diag(-1, 1, 1, 1) * jacobian * scale**2
    result_shifted = einstein_from_jet(*symbolic_jet(shifted, (eta, x, y, z),
                                                   {eta: 0, x: 0, y: 0, z: 0}))
    # Source computed in the unshifted comoving frame, then tensor-transformed.
    source = jacobian.T * sp.diag(sp.Rational(3, 256), *[sp.Rational(1, 256)]*3) * jacobian
    assert result_shifted['G'] == source and source[0, 1] != 0
    return {'curved_Schwarzschild_vacuum_all_16_G_zero': True,
            'Schwarzschild_nonzero_Riemann_components': nonzero,
            'shifted_radiation_all_16_G_minus_T_zero': True,
            'shifted_radiation_G_01': str(source[0, 1]),
            'role': 'general nonlinear observer, not a dynamics implementation',
            'compilation_barriers': compilation_barriers()}
