"""Eight-channel, prepared flat FLRW dust/radiation sector at fixed six.

This is an optional model, not the general ADM replacement. subdivision changes only
the fixed tensor coefficients and passive calibration, never the divisor.
"""
from universe24.core import Tensor

SOURCES = ('dust.matter', 'dust.antimatter', 'dust.dark')
NAMES = ('clock.q', 'geometry.s', 'clock.c6', 'light.l30', *SOURCES,
         'radiation.b')


def resolution(subdivision):
    if type(subdivision) is not int or subdivision < 1:
        raise ValueError('subdivision must be a positive Python integer')
    return subdivision


def build(subdivision=1):
    """Compile a fixed cubic tensor; channel count is independent of run length.

    With A=sum(dust), B=radiation.b, the prepared invariants are
    s=A*q^2+B*subdivision*q; c6=2*A*q^3+3*B*subdivision*q^2;
    l30=6*A^2*q^5+15*A*B*subdivision*q^4+10*B^2*subdivision^2*q^3.
    l30 is a null affine-parameter counter, NOT photon proper time or energy.
    """
    subdivision = resolution(subdivision)
    terms = [(name, 6, ((name, (0, 0, 0), 'b'),)) for name in NAMES]

    def add(target, coefficient, *names):
        terms.append((target, coefficient,
                      tuple((name, (0, 0, 0), 'b') for name in names),
                      {'designated_one_way': 'Prepared symmetry-reduced Friedmann recurrence; no generic reciprocal potential is asserted.'}))

    for source in SOURCES:
        add('geometry.s', 6, source)
        add('clock.c6', 36, source, 'clock.q')
        add('light.l30', 360, source, 'geometry.s', 'clock.q')
        add('light.l30', 90*subdivision, source, 'radiation.b')
        for other in SOURCES:
            add('light.l30', 180, source, other, 'clock.q')
    add('clock.c6', 18*subdivision, 'radiation.b')
    add('light.l30', 180*subdivision, 'radiation.b', 'geometry.s')
    return Tensor(NAMES, terms, strict_support=True)
