"""Exact local Lorentzian geometry from ten signed squared intervals.

These are tangent-simplex data, not a claim that a curved cell is flat.
No diagonal lattice reads or changes to the Rule3 engine are introduced.
"""
from itertools import combinations
import sympy as sp

EDGES = tuple(combinations(range(5), 2))


def exact_matrix(values):
    matrix = sp.Matrix(values)
    if any(value.is_Rational is not True for value in matrix):
        raise ValueError('geometry requires exact rational entries')
    return matrix


def inertia(matrix):
    """Return (negative, positive, zero) by exact symmetric congruences.

    Two-by-two pivots also handle a null basis, where diagonal LDL fails.
    """
    work = exact_matrix(matrix)
    if work.rows != work.cols or work != work.T:
        raise ValueError('expected a symmetric matrix')
    negative = positive = zero = 0
    while work.rows:
        size = work.rows
        nonzero = next((i for i in range(size) if work[i, i] != 0), None)
        if nonzero is not None:
            order = [nonzero] + [i for i in range(size) if i != nonzero]
            work = work.extract(order, order)
            pivot = work[0, 0]
            negative += int(bool(pivot < 0))
            positive += int(bool(pivot > 0))
            work = work[1:, 1:] - work[1:, :1] * work[:1, 1:] / pivot
        else:
            pair = next(((i, j) for i in range(size) for j in range(i + 1, size)
                         if work[i, j] != 0), None)
            if pair is None:
                zero += size
                break
            order = list(pair) + [i for i in range(size) if i not in pair]
            work = work.extract(order, order)
            # [[0,c],[c,0]] has one eigenvalue of either sign.
            negative += 1
            positive += 1
            work = work[2:, 2:] - work[2:, :2] * work[:2, :2].inv() * work[:2, 2:]
    return negative, positive, zero


def signed_intervals(metric, basis=None):
    """All ten edges of {0,e0,e1,e2,e3}; basis columns are edge vectors."""
    metric = exact_matrix(metric)
    basis = sp.eye(4) if basis is None else exact_matrix(basis)
    if metric.shape != (4, 4) or basis.shape != (4, 4):
        raise ValueError('expected four dimensions')
    if metric != metric.T or inertia(metric) != (1, 3, 0) or basis.det() == 0:
        raise ValueError('expected a nondegenerate Lorentzian metric and basis')
    points = [sp.zeros(4, 1)] + [basis[:, i] for i in range(4)]
    return {(i, j): ((points[j] - points[i]).T * metric *
                     (points[j] - points[i]))[0] for i, j in EDGES}


def metric_from_intervals(intervals, basis=None):
    """Polarization identity, with exact signature and completeness checks."""
    if set(intervals) != set(EDGES):
        raise ValueError('all ten signed squared intervals are required')
    values = {edge: exact_matrix([[value]])[0] for edge, value in intervals.items()}
    gram = sp.zeros(4)
    for i in range(4):
        for j in range(4):
            cross = 0 if i == j else values[tuple(sorted((i + 1, j + 1)))]
            gram[i, j] = (values[0, i + 1] + values[0, j + 1] - cross) / 2
    if inertia(gram) != (1, 3, 0):
        raise ValueError('intervals do not define signature (-,+,+,+)')
    basis = sp.eye(4) if basis is None else exact_matrix(basis)
    if basis.shape != (4, 4) or basis.det() == 0:
        raise ValueError('expected an invertible four-dimensional basis')
    inverse = basis.inv()
    return inverse.T * gram * inverse


def straight_path_refinement(a0=sp.Rational(2), velocity=sp.Rational(1, 8)):
    """A finite curved cell is only approximately a tangent simplex.

    Integrate the length of each prescribed coordinate-straight path in
    a(eta)=a0+velocity*eta. These paths are generally NOT geodesics.
    Their signed length squared is eta(dx,dx)*mean(a_at_endpoints)**2.
    Refining recovers the local metric; this is not a Regge field solver.
    """
    a0, velocity = exact_matrix([[a0, velocity]])
    rows = []
    minkowski = sp.diag(-1, 1, 1, 1)
    for n in (1, 2, 4, 8, 16):
        h = sp.Rational(1, n)
        basis = sp.diag(h / 2, h, h, h)
        points = [sp.zeros(4, 1)] + [basis[:, i] for i in range(4)]
        lengths = {}
        for i, j in EDGES:
            dx = points[j] - points[i]
            mean_a = a0 + velocity * (points[i][0] + points[j][0]) / 2
            if mean_a <= 0 or a0 + velocity * h / 2 <= 0 or a0 <= 0:
                raise ValueError('cell crosses the a=0 singularity')
            lengths[i, j] = (dx.T * minkowski * dx)[0] * mean_a**2
        reconstructed = metric_from_intervals(lengths, basis)
        error = max(abs(value) for value in reconstructed - a0**2 * minkowski)
        rows.append({'n': n, 'max_metric_error': str(error)})
    return rows
