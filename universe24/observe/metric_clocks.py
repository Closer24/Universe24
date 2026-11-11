"""Instantaneous proper-clock rates in the existing ADM coordinate chart."""
from fractions import Fraction


def rate_squared(metric, velocity=(0, 0, 0)):
    """Return (d tau / d t)^2 for tangent (1,v), with signature -+++.

    Nonpositive values are null/spacelike tangents, not ticking observers.
    This local readout does not integrate a worldline or assert it is geodesic.
    """
    if len(metric) != 4 or any(len(row) != 4 for row in metric) or len(velocity) != 3:
        raise ValueError('expected a four-metric and three coordinate velocities')
    tangent = (Fraction(1), *map(Fraction, velocity))
    return -sum(Fraction(metric[i][j])*tangent[i]*tangent[j]
                for i in range(4) for j in range(4))


def clock_readout(metric, alpha, beta):
    normal_velocity = tuple(-Fraction(v) for v in beta)
    normal = rate_squared(metric, normal_velocity)
    if Fraction(alpha) <= 0 or normal != Fraction(alpha)**2:
        raise ValueError('clock tangent and lapse disagree with the ADM metric')
    grid = rate_squared(metric)
    return {'normal_rate': Fraction(alpha), 'normal_rate_squared': normal,
            'normal_coordinate_velocity': normal_velocity,
            'grid_rate_squared': grid,
            'grid_worldline': 'timelike' if grid > 0 else 'null' if grid == 0 else 'spacelike'}
