"""The board: addresses, the six Port headings in Port order, and the cell bound.

The board is the cubic lattice of Highlights 3.1: a Node is addressed by three
integers, and its six Ports face the unit-axial headings in the fixed order
[+X, -X, +Y, -Y, +Z, -Z]. `MIXING_OPPOSITE[h]` is the Port an arrival with
travel heading h came in through, that is the opposite heading. `MAX_VALUE` is
the bound of one cell's amount (2^30 - 1): a value above it is refused, never
wrapped.
"""

Address3 = tuple[int, int, int]
Heading = tuple[int, int, int]

# The bound of a cell's whole amount: values are refused above it.
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
# The opposite of each heading, in Port order: the Port an arrival with that
# travel heading came in through.
MIXING_OPPOSITE = (1, 0, 3, 2, 5, 4)
