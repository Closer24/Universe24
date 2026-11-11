"""Exact rank-one null coframes; algebra only, not Einstein evolution."""
from dataclasses import dataclass
from numbers import Integral

import numpy as np


ETA = (-1, 1, 1, 1)


def integer_array(values):
    """Copy as Python integers without rounding or fixed-width products."""
    values = np.asarray(values, dtype=object)
    if any(isinstance(v, (bool, np.bool_)) or not isinstance(v, Integral)
           for v in values.flat):
        raise TypeError("Expected exact integers, not floats or booleans")
    return np.array([int(v) for v in values.flat], dtype=object).reshape(values.shape)


@dataclass(frozen=True)
class NullCoframe:
    """Fixed P and nonzero integer null covector in Minkowski coordinates.

    E = P I + F L, L = ell^sharp outer ell, L^2 = 0.
    No normalization is performed: rescaling ell changes the geometry at fixed F.
    The generic algebra does not prescribe a propagation or connection law.
    """

    P: int = 256
    covector: tuple[int, int, int, int] = (1, 0, 0, -1)

    def __post_init__(self):
        p = integer_array(self.P)
        ell = integer_array(self.covector)
        if p.shape != () or p.item() <= 0:
            raise ValueError("P must be a positive integer")
        if ell.shape != (4,) or not any(ell):
            raise ValueError("Expected four components of a nonzero covector")
        if sum(s*v*v for s, v in zip(ETA, ell)) != 0:
            raise ValueError("Covector must be null for eta=diag(-1,1,1,1)")
        object.__setattr__(self, 'P', p.item())
        object.__setattr__(self, 'covector', tuple(ell))

    def decode(self, profile):
        """Passive exact matrices, with the profile's shape as batch axes.

        E^-1 = inverse_coframe_numerator / P^2;
        g^-1 = inverse_metric_numerator / P^3.
        The denominators are geometric readout constants, never Engine divisors.
        """
        f = integer_array(profile)[..., None, None]
        ell = np.array(self.covector, dtype=object)
        raised = np.array(ETA, dtype=object)*ell
        identity = np.eye(4, dtype=object)
        eta = np.diag(np.array(ETA, dtype=object))
        deformation = f*np.outer(raised, ell)
        return {
            'coframe': self.P*identity + deformation,
            'inverse_coframe_numerator': self.P*identity - deformation,
            'inverse_coframe_denominator': self.P**2,
            'metric': self.P**2*eta + 2*self.P*f*np.outer(ell, ell),
            'inverse_metric_numerator': self.P*eta - 2*f*np.outer(raised, raised),
            'inverse_metric_denominator': self.P**3,
        }
