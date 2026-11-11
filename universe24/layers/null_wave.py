"""Optional two-channel null-wave profile transport, independent of ADM."""
from universe24.core import GearType, Tensor

ZERO, PLUS_Z, MINUS_Z = (0, 0, 0), (0, 0, 1), (0, 0, -1)


def build():
    """u=3(R+R^-1)b, R(X,Y)=(Y,S_minus X), at fixed divisor six.

    This is a new compact model of the prepared pp-wave profile. It does not
    retain the old experiment's independent connection, signal or clock gears.
    """
    def f(bank, offset=ZERO):
        return (f'profile.{bank}', offset, 'b')
    return Tensor([GearType('profile.X', label='audit'),
                   GearType('profile.Y', label='audit')], [
        ('profile.X', 3, (f('Y'),)),
        ('profile.X', 3, (f('Y', PLUS_Z),)),
        ('profile.Y', 3, (f('X'),)),
        ('profile.Y', 3, (f('X', MINUS_Z),)),
    ], strict_support=True)
