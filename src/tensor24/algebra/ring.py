"""The Gaussian ring: a hand as z = re + i im on two gears, a twin hand as two hands, products and sums alone."""

from tensor24.algebra.carry import Z

Hand = tuple[Z, Z]  # (re, im): the three-o'clock and the twelve-o'clock gears
Twin = tuple[Hand, Hand]  # (up, down): two hands read as one spinor


def mul(z: Hand, w: Hand) -> Hand:
    """The complex product of two hands, on their coefficients."""
    a, b = z
    c, d = w
    return a * c - b * d, a * d + b * c


def conj(z: Hand) -> Hand:
    """The conjugate, K: the hand's twelve-o'clock gear turned over, T on a hand."""
    a, b = z
    return a, -b


def norm(z: Hand) -> Z:
    """z conj(z), a whole number: the hand's size."""
    a, b = z
    return a * a + b * b


def pair(z: Hand, w: Hand) -> Hand:
    """conj(z) w: its real part the dot of two hands, its imaginary part their cross."""
    return mul(conj(z), w)


def add(z: Hand, w: Hand) -> Hand:
    """The sum of two hands."""
    a, b = z
    c, d = w
    return a + c, b + d


def overlap(phi: Twin, psi: Twin) -> Hand:
    """<phi, psi>, how far two twin hands agree: the sum of their hands' pairs, a Gaussian integer."""
    return add(pair(phi[0], psi[0]), pair(phi[1], psi[1]))


def reverse(psi: Twin) -> Twin:
    """T on a twin hand: (up, down) to (-conj down, conj up), so T T is -1 where on a hand it is +1."""
    up, down = psi
    a, b = conj(down)
    return (-a, -b), conj(up)


def axis(psi: Twin) -> tuple[Z, tuple[Z, Z, Z]]:
    """The twin hand's reading (rho, S): its size, and its spin from the pair of its two hands, S . S = rho rho."""
    up, down = psi
    x, y = pair(up, down)
    return norm(up) + norm(down), (x + x, y + y, norm(up) - norm(down))
