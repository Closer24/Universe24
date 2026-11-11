"""Passive exact geometry, sources and clocks; no update or projection."""
from fractions import Fraction as F
import numpy as np
from universe24.layers.conformal_flrw import NAMES, SOURCES, resolution


def sample(state, *, Q=1):
    Q = resolution(Q)
    if state.G != len(NAMES):
        raise ValueError('expected the standalone eight-channel state')
    if any(not np.all(v == v[:, :1]) for v in (state.a, state.b)):
        raise ValueError('this FLRW decoder requires spatial homogeneity')
    q, s, c, ell, *sources, B = map(int, state.b[:, 0])
    A = sum(sources)
    if q < 2 or min(*sources, B) < 0 or A == B == 0:
        raise ValueError('outside the positive expanding sector')
    # Check both histories, including the velocities. Off-sector states still
    # evolve reversibly, but must not be silently interpreted as this metric.
    for array, t in ((state.a, q-1), (state.b, q)):
        expected = [t, A*t*t+B*Q*t, 2*A*t**3+3*B*Q*t*t,
                    6*A*A*t**5+15*A*B*Q*t**4+10*B*B*Q*Q*t**3,
                    *sources, B]
        if list(map(int, array[:, 0])) != expected:
            raise ValueError('prepared FLRW history invariant failed')
    eta, a = F(q, Q), F(s, Q*Q)
    ap, app = 2*A*eta+B, F(2*A)
    densities = {name: F(12*value)/a**3 for name, value in zip(SOURCES, sources)}
    densities['radiation'] = F(3*B*B)/a**4
    rho, pressure = sum(densities.values()), densities['radiation']/3
    metric = [[(-1 if i == 0 else 1)*a*a if i == j else F(0)
               for j in range(4)] for i in range(4)]
    einstein_diag = [3*(ap/a)**2] + [(ap/a)**2-2*app/a]*3
    stress_diag = [rho*a*a] + [pressure*a*a]*3
    # The four-metric is determined by one scale only because of homogeneity
    # and isotropy. These conditions must not be used in the default ADM run.
    return {'eta': eta, 'scale_factor': a, 'proper_time': F(c, 6*Q**3),
            'null_affine_parameter': F(ell, 30*Q**5),
            'proper_rate_per_conformal_time': a,
            'densities': densities, 'rho': rho, 'pressure': pressure,
            'metric': metric, 'einstein_diagonal': einstein_diag,
            'stress_diagonal': stress_diag,
            'einstein_residual': [g-t for g, t in zip(einstein_diag, stress_diag)],
            'friedmann_residual': ap*ap-4*A*a-B*B}
