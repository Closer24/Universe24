"""Fixed six-port neighbor geometry shared by configured carrier and field links."""

from .disturbance_state import Address3, bounded


def neighbor_address(origin: Address3, port: int, shape: Address3, boundary: str) -> Address3 | None:
    """Return one neighbor, or no destination when an open link leaves the domain.

    Ports are +X, -X, +Y, -Y, +Z, -Z. Inputs are immutable, bounded lattice
    addresses and parameters; this helper neither transfers nor accounts stock.
    """
    if boundary not in ("periodic", "open"):
        raise ValueError("boundary must be periodic or open")
    if not isinstance(shape, tuple) or len(shape) != 3:
        raise ValueError("shape requires exactly three immutable dimensions")
    if not isinstance(origin, tuple) or len(origin) != 3:
        raise ValueError("origin requires exactly three immutable coordinates")
    for position, extent in zip(origin, shape, strict=True):
        if bounded(extent) < 1:
            raise ValueError("shape dimensions must be positive")
        if not 0 <= bounded(position) < extent:
            raise ValueError("origin must lie within shape")
    if not 0 <= bounded(port) < 6:
        raise ValueError("port must be a cardinal index from 0 through 5")
    axis = port // 2
    coordinate = bounded(origin[axis] + (1 if port % 2 == 0 else -1))
    if boundary == "periodic":
        coordinate %= shape[axis]
    elif not 0 <= coordinate < shape[axis]:
        return None
    return (
        coordinate if axis == 0 else origin[0],
        coordinate if axis == 1 else origin[1],
        coordinate if axis == 2 else origin[2],
    )
