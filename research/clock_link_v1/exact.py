"""Closed full-state trajectory, not an alternative evolution engine."""
from research.component_families.oracle import routing
from research.reference.algebra import DIRECTIONS

BACKGROUND = (0, 0, 2)


def s(q):
    return (1, 0, -1, 0)[q % 4] if q >= 0 else 0


def H(q):
    return (0, 1, 1, 0)[q % 4] if q > 0 else 0


def row_b(i, t, D):
    M = D + 1
    if i == 0:
        return s(t)
    return s(t-i)-s(t+i-2*M)+s(t-i-2*M)-s(t+i-4*M)


def row_F(i, t, D):
    M = D + 1
    if i == 0:
        return H(t)
    return H(t-i)-H(t+i-2*M)+H(t-i-2*M)-H(t+i-4*M)


def closed_state(D, t, side, origin=(4, 4, 4)):
    """Complete sparse canonical state at arbitrary nonnegative t, even D>=2.

    Omitted triples are the exact stationary background. The independent
    reference routing identifies all transverse/axial halo addresses.
    """
    if type(D) is not int or D < 2 or D % 2 or side < D+3 or t < 0:
        raise ValueError('Outside the exact even-guide nonaliased domain')
    t %= 4*(D+1)
    M = D+1
    def addr(i):
        return ((origin[0]+i) % side, origin[1] % side, origin[2] % side, 0)
    row = {addr(i): i for i in range(D+1)}
    result = {}
    def put(address, value):
        if value != BACKGROUND:
            if address in result and result[address] != value:
                raise AssertionError('Aliased closed-state assignments')
            result[address] = value
    put(addr(0), (s(t-1) if t else 0, s(t), 2+2*row_F(1,t,D)))
    for i in range(1,D+1):
        theta = int(t>=i)-int(t>=2*M-i)+int(t>=2*M+i)-int(t>=4*M-i)
        put(addr(i), (row_b(i,t-1,D), row_b(i,t,D), 4-4*theta))
    _, inverse = routing((1,1,1))
    for address, i in row.items():
        x,y,z,g = address
        for d,(dx,dy,dz) in enumerate(DIRECTIONS):
            recipient = ((x-dx)%side,(y-dy)%side,(z-dz)%side,inverse[d][g])
            if recipient not in row:
                put(recipient,(0,0,2+2*row_F(i,t,D)))
    return result
