"""Eight-channel, prepared flat FLRW dust/radiation sector at fixed six.

This is an optional model, not the general ADM replacement. Q changes only
the fixed tensor coefficients and passive calibration, never the divisor.
"""
from universe24.core import Tensor

SOURCES = ('dust.matter', 'dust.antimatter', 'dust.dark')
NAMES = ('clock.q', 'geometry.s', 'clock.c6', 'light.l30', *SOURCES,
         'radiation.b')


def resolution(Q):
    if type(Q) is not int or Q < 1:
        raise ValueError('Q must be a positive Python integer')
    return Q


def build(Q=1):
    """Compile a fixed cubic tensor; channel count is independent of run length.

    With A=sum(dust), B=radiation.b, the prepared invariants are
    s=A*q^2+B*Q*q; c6=2*A*q^3+3*B*Q*q^2;
    l30=6*A^2*q^5+15*A*B*Q*q^4+10*B^2*Q^2*q^3.
    l30 is a null affine-parameter counter, NOT photon proper time or energy.
    """
    Q = resolution(Q)
    terms = [(name, 6, ((name, (0, 0, 0), 'b'),)) for name in NAMES]

    def add(target, coefficient, *names):
        terms.append((target, coefficient,
                      tuple((name, (0, 0, 0), 'b') for name in names),
                      {'designated_one_way': 'Prepared symmetry-reduced Friedmann recurrence; no generic reciprocal potential is asserted.'}))

    for source in SOURCES:
        add('geometry.s', 6, source)
        add('clock.c6', 36, source, 'clock.q')
        add('light.l30', 360, source, 'geometry.s', 'clock.q')
        add('light.l30', 90*Q, source, 'radiation.b')
        for other in SOURCES:
            add('light.l30', 180, source, other, 'clock.q')
    add('clock.c6', 18*Q, 'radiation.b')
    add('light.l30', 180*Q, 'radiation.b', 'geometry.s')
    return Tensor(NAMES, terms, strict_support=True)
