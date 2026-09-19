"""The board: addresses, the six Port headings in Port order, and the bound of
a declared charge and quantum.

The board is the cubic lattice of Highlights 3.1: a Node is addressed by three
integers, and its six Ports face the unit-axial headings in the fixed order
[+X, -X, +Y, -Y, +Z, -Z]. `MAX_VALUE` is the bound of a family's charge and
quantum and of a measured event's charge as the world file declares them
(2^30 - 1): a value above it is refused, never wrapped.
"""

from event_universe.core.integer import checked_work

Address3 = tuple[int, int, int]
Heading = tuple[int, int, int]

# The bound of a declared charge or quantum: values are refused above it.
MAX_VALUE = 1_073_741_823
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
PORT_HEADINGS: tuple[Heading, ...] = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


def adjacent_node(
    position: Address3,
    port: int,
    shape: Address3,
    periodic: tuple[bool, bool, bool] = (False, False, False),
) -> Address3 | None:
    """Return one declared neighbor, or None through an open outer face.

    An extent-one periodic axis is a self-Link. This function supplies its
    address only; transport still takes the ordinary interval.
    """
    if (
        type(position) is not tuple
        or len(position) != 3
        or type(shape) is not tuple
        or len(shape) != 3
        or type(periodic) is not tuple
        or len(periodic) != 3
    ):
        raise ValueError("adjacency requires three-tuples for position, shape and periodic")
    if type(port) is not int or not 0 <= port < 6:
        raise ValueError("adjacency requires an integer Port in 0 through 5")
    for coordinate, extent, wraps in zip(position, shape, periodic, strict=True):
        if type(extent) is not int or not 1 <= extent <= 4096:
            raise ValueError("adjacency requires integer extents in 1 through 4096")
        if type(coordinate) is not int or not 0 <= coordinate < extent:
            raise ValueError("adjacency requires an in-board integer position")
        if type(wraps) is not bool:
            raise ValueError("adjacency requires one boolean periodic flag per axis")
    axis = port // 2
    target = checked_work(position[axis] + PORT_HEADINGS[port][axis])
    if not 0 <= target < shape[axis]:
        if not periodic[axis]:
            return None
        target = 0 if target == shape[axis] else checked_work(shape[axis] - 1)
    result = list(position)
    result[axis] = target
    return result[0], result[1], result[2]
