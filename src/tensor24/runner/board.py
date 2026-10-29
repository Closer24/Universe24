"""The board from its shape: each site's six neighbours, the wrap by Rule3 on each coordinate."""

import numpy as np

from tensor24.algebra.carry import Z, carry


def site(x: Z, y: Z, z: Z, sy: Z, sz: Z) -> Z:
    """The site at three coordinates, z the fastest: (x sy + y) sz + z."""
    return (x * sy + y) * sz + z


def wrap(x: Z, side: Z) -> Z:
    """A coordinate brought onto the board's side by Rule3: the carry's remainder."""
    _, kept = carry(x, side, 0)
    return kept


def board(shape: tuple[int, int, int]) -> Z:
    """The six neighbours of every site, +x, -x, +y, -y, +z, -z, as one index array."""
    sx, sy, sz = shape
    n = sx * sy * sz
    sites = np.arange(n, dtype=np.intp)  # an index array: the sites counted, each a whole number below n
    rest, z = carry(sites, sz, 0)
    x, y = carry(rest, sy, 0)
    return np.stack(
        [
            site(wrap(x + 1, sx), y, z, sy, sz),
            site(wrap(x - 1, sx), y, z, sy, sz),
            site(x, wrap(y + 1, sy), z, sy, sz),
            site(x, wrap(y - 1, sy), z, sy, sz),
            site(x, y, wrap(z + 1, sz), sy, sz),
            site(x, y, wrap(z - 1, sz), sy, sz),
        ]
    )
