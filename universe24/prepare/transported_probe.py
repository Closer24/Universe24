"""Complete stationary pp-wave seeds and localized transported clock states."""
import numpy as np

from universe24.core import State
from universe24.core.lattice import lattice
from universe24.layers.transported_probe import CLOCKS


def prepare(tensor, curvature=1, x=0, y=0, L=5, amplitude=1):
    """P=1, F=c(x²-y²); all arithmetic is integer. No runtime preparation.

    x,y must lie inside the centered chart, leaving a derivative stencil.
    The geometry is stationary only on a=b. Arbitrary histories may drift.
    """
    if type(L) is not int or L < 5 or L % 2 != 1:
        raise ValueError("Use odd L>=5")
    if type(curvature) is not int or curvature not in (0, 1):
        raise ValueError("Use flat (0) or the declared pp-wave (1)")
    if any(type(v) is not int or abs(v) >= L//2 for v in (x, y)):
        raise ValueError("Probe must leave a transverse interior stencil")
    if type(amplitude) is not int or amplitude < 1:
        raise ValueError("Positive integer packet amplitude required")
    lat = lattice(L)
    xyz = lat.all_coords().astype(object)
    xx, yy = xyz[:, 0]-L//2, xyz[:, 1]-L//2
    profile = curvature*(xx*xx-yy*yy)
    eta, ell = (-1, 1, 1, 1), (1, 0, 0, -1)
    b = np.zeros((tensor.G, lat.N), dtype=object)
    for alpha in range(4):
        for mu in range(4):
            b[tensor.gear_index(f"E{alpha}{mu}")] = (
                int(alpha == mu)+eta[alpha]*ell[alpha]*ell[mu]*profile)
    a, r = b.copy(), np.zeros_like(b)
    node = lat.index(L//2+x, L//2+y, 0)
    b[tensor.gear_index("probe.X"), node] = amplitude
    a[tensor.gear_index("probe.Y"), node] = amplitude
    k = 1-2*curvature*(x*x-y*y)
    for clock in CLOCKS:
        # Initial X=(amplitude,0), Y=0; a=R^-1 b has Y=Q^-1 X.
        b[tensor.gear_index(f"{clock}.X0"), node] = amplitude
        a[tensor.gear_index(f"{clock}.Y0"), node] = (k if clock == "candidate" else 0)*amplitude
        a[tensor.gear_index(f"{clock}.Y1"), node] = -amplitude
    return State(L, a, b, r)
