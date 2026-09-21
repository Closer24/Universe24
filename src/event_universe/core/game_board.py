"""The GameBoard: addresses, the six Port headings in Port order, the cube's
group of 48 symmetries, and the bound of a declared charge and quantum.

The GameBoard is the cubic lattice of Nodes of Highlights 3.1 (the canonical
name, docs/TERMINOLOGY.md): a Node is addressed by three integers, and its
six Ports face the unit-axial headings in the fixed order
[+X, -X, +Y, -Y, +Z, -Z]. `MAX_VALUE` is the bound of a family's charge and
quantum and of a measured event's charge as the world file declares them
(2^30 - 1): a value above it is refused, never wrapped.
"""

from functools import lru_cache
from itertools import permutations, product

from event_universe.core.integer import checked_work

Address3 = tuple[int, int, int]
Heading = tuple[int, int, int]
# A symmetry of the cube as the image of the six Ports in Port order: the
# Port that Port k faces after the symmetry.
CubeSymmetry = tuple[int, int, int, int, int, int]

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


@lru_cache(maxsize=1)
def cube_symmetries() -> tuple[CubeSymmetry, ...]:
    """The cube's group of 48 (the signed axis permutations, the symmetries
    of the lattice about a Node: an axis permutation and a sign per axis),
    each as its image of the six Ports; closed under `compose_symmetries`,
    the identity `IDENTITY_SYMMETRY` among them and every inverse
    (`inverse_symmetry`). The 24 of hand +1 are the rotations, the 24 of
    hand -1 the reflections (`symmetry_hand`, the pseudoscalar of the
    group: the sign of the axis permutation times the product of the
    signs). Named on 2026-09-21 (the vector program, record 191: "the hand
    a pseudoscalar of the cube's group of 48"); the same 48 maps the
    collision test enumerated before."""
    found = []
    for axes in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            image = []
            for port in range(6):
                axis, forward = port >> 1, (port & 1) == 0
                sign = (1 if forward else -1) * signs[axis]
                image.append(2 * axes[axis] + (0 if sign > 0 else 1))
            found.append((image[0], image[1], image[2], image[3], image[4], image[5]))
    return tuple(found)


IDENTITY_SYMMETRY: CubeSymmetry = (0, 1, 2, 3, 4, 5)


def compose_symmetries(first: CubeSymmetry, second: CubeSymmetry) -> CubeSymmetry:
    """The symmetry that applies `first` and then `second`."""
    image = tuple(second[first[port]] for port in range(6))
    return image[0], image[1], image[2], image[3], image[4], image[5]


def inverse_symmetry(symmetry: CubeSymmetry) -> CubeSymmetry:
    """The symmetry that undoes `symmetry`."""
    image = [0] * 6
    for port in range(6):
        image[symmetry[port]] = port
    return image[0], image[1], image[2], image[3], image[4], image[5]


def symmetry_hand(symmetry: CubeSymmetry) -> int:
    """+1 for a rotation, -1 for a reflection: the sign of the axis
    permutation times the product of the axis signs (the determinant of
    the signed permutation matrix)."""
    axes = [symmetry[2 * axis] >> 1 for axis in range(3)]
    signs = [1 if symmetry[2 * axis] & 1 == 0 else -1 for axis in range(3)]
    inversions = sum(1 for i in range(3) for j in range(i + 1, 3) if axes[i] > axes[j])
    return (-1 if inversions % 2 else 1) * signs[0] * signs[1] * signs[2]


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
            raise ValueError("adjacency requires an integer position on the GameBoard")
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
