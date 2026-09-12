"""Bounded immutable neighbor geometry shared by carrier and field links."""

from .disturbance_state import (
    DEFAULT_TOPOLOGY,
    MAX_PORTS,
    MAX_SITE_MODULUS,
    MAX_SITE_RESIDUES,
    Address3,
    InitialState,
    PortTopology,
    bounded,
)


def _address(value: Address3, label: str) -> None:
    if not isinstance(value, tuple) or len(value) != 3:
        raise ValueError(f"{label} requires exactly three immutable coordinates")
    for component in value:
        bounded(component)


def site_allowed(position: Address3, topology: PortTopology = DEFAULT_TOPOLOGY) -> bool:
    """Test only the immutable site pattern, without reading another location."""
    _address(position, "position")
    if not 1 <= bounded(topology.site_modulus) <= MAX_SITE_MODULUS:
        raise ValueError("topology site_modulus exceeds its fixed bound")
    residue = tuple(value % topology.site_modulus for value in position)
    return residue in topology.site_residues


def validate_position(
    position: Address3, shape: Address3, topology: PortTopology = DEFAULT_TOPOLOGY
) -> None:
    _address(shape, "shape")
    _address(position, "position")
    if any(extent < 1 for extent in shape):
        raise ValueError("shape dimensions must be positive")
    if any(not 0 <= value < extent for value, extent in zip(position, shape, strict=True)):
        raise ValueError("position must lie within shape")
    if not site_allowed(position, topology):
        raise ValueError("position is not a site in the configured topology")


def site_count(shape: Address3, topology: PortTopology = DEFAULT_TOPOLOGY) -> int:
    """Count permitted sites for read-only totals with at most eight products.

    The topology has already been validated by its owner. This diagnostic uses
    the immutable residue pattern, never a scan or feedback into physical state.
    """
    _address(shape, "shape")
    if any(extent < 1 for extent in shape):
        raise ValueError("shape dimensions must be positive")
    if not 1 <= bounded(topology.site_modulus) <= MAX_SITE_MODULUS:
        raise ValueError("topology site_modulus exceeds its fixed bound")
    if not 1 <= len(topology.site_residues) <= MAX_SITE_RESIDUES:
        raise ValueError("topology site residue count exceeds its fixed bound")
    total = 0
    for residue in topology.site_residues:
        _address(residue, "site residue")
        amount = 1
        for extent, value in zip(shape, residue, strict=True):
            if not 0 <= value < topology.site_modulus:
                raise ValueError("site residues must lie below site_modulus")
            amount *= max(0, (extent - 1 - value) // topology.site_modulus + 1)
        total += amount
    return total


def validate_topology(topology: PortTopology, shape: Address3, boundary: str) -> None:
    """Validate bounded configuration, never enumerate the domain's nodes.

    The residue closure test costs at most 8 times 26 local offset checks.
    Explicit topologies forbid self-links and duplicate periodic destinations;
    the default cardinal model retains its historical thin-domain behavior.
    """
    if boundary not in ("periodic", "open"):
        raise ValueError("boundary must be periodic or open")
    _address(shape, "shape")
    if any(extent < 1 for extent in shape):
        raise ValueError("shape dimensions must be positive")
    if not isinstance(topology, PortTopology):
        raise ValueError("immutable port topology required")
    if topology.model_id not in ("cardinal-six-v1", "configured-ports-v1"):
        raise ValueError("unknown topology model_id")
    if topology.model_id == "cardinal-six-v1" and topology != DEFAULT_TOPOLOGY:
        raise ValueError("cardinal-six-v1 requires the unchanged default topology")
    if not isinstance(topology.offsets, tuple) or not 2 <= topology.degree <= MAX_PORTS:
        raise ValueError("topology requires 2 through 26 immutable ports")
    for offset in topology.offsets:
        _address(offset, "port offset")
        if not any(offset) or any(value not in (-1, 0, 1) for value in offset):
            raise ValueError("port offsets must be nonzero and use components -1, 0 or 1")
    if len(set(topology.offsets)) != topology.degree:
        raise ValueError("topology offsets must be unique")
    if any(tuple(-value for value in offset) not in topology.offsets for offset in topology.offsets):
        raise ValueError("every port requires its reciprocal offset")
    if not 1 <= bounded(topology.site_modulus) <= MAX_SITE_MODULUS:
        raise ValueError("topology site_modulus exceeds its fixed bound")
    if (
        not isinstance(topology.site_residues, tuple)
        or not 1 <= len(topology.site_residues) <= MAX_SITE_RESIDUES
    ):
        raise ValueError("topology requires a bounded immutable site residue list")
    for residue in topology.site_residues:
        _address(residue, "site residue")
        if any(not 0 <= value < topology.site_modulus for value in residue):
            raise ValueError("site residues must lie below site_modulus")
        if any(value >= extent for value, extent in zip(residue, shape, strict=True)):
            raise ValueError("each declared site residue must occur inside the domain")
    if len(set(topology.site_residues)) != len(topology.site_residues):
        raise ValueError("topology site residues must be unique")
    for residue in topology.site_residues:
        for offset in topology.offsets:
            target = tuple(
                (value + delta) % topology.site_modulus
                for value, delta in zip(residue, offset, strict=True)
            )
            if target not in topology.site_residues:
                raise ValueError("topology site pattern is not closed under its port offsets")
    if topology.model_id == "cardinal-six-v1" or boundary == "open":
        return
    if any(extent % topology.site_modulus for extent in shape):
        raise ValueError("periodic shape must be divisible by topology site_modulus")
    destinations = tuple(
        tuple(delta % extent for delta, extent in zip(offset, shape, strict=True))
        for offset in topology.offsets
    )
    if (0, 0, 0) in destinations:
        raise ValueError("explicit periodic topology cannot contain self-links")
    if len(set(destinations)) != len(destinations):
        raise ValueError("explicit periodic topology cannot alias different ports")


def inverse_port(port: int, topology: PortTopology = DEFAULT_TOPOLOGY) -> int:
    if not 0 <= bounded(port) < topology.degree:
        raise ValueError("port index exceeds the configured topology")
    offset = topology.offsets[port]
    opposite = (-offset[0], -offset[1], -offset[2])
    try:
        return topology.offsets.index(opposite)
    except ValueError as error:
        raise ValueError("port has no reciprocal offset") from error


def validate_topology_configuration(initial: InitialState) -> None:
    """Check topology capabilities at both JSON and typed public boundaries."""
    validate_topology(initial.topology, initial.shape, initial.boundary)
    for seed in initial.seeds:
        validate_position(seed.position, initial.shape, initial.topology)
    for spatial_seed in initial.spatial_seeds:
        validate_position(spatial_seed.position, initial.shape, initial.topology)
    if initial.topology == DEFAULT_TOPOLOGY:
        return
    if any(definition.transport != "local" for definition in initial.spatial_fields):
        raise ValueError("configured topology requires local spatial field transport")
    if initial.spatial_couplings:
        raise ValueError(
            "configured topology requires generic spatial_interactions instead of spatial_couplings"
        )
    if initial.event_program is not None:
        raise ValueError("native event_program currently requires cardinal-six-v1 topology")
    for definition in initial.disturbances:
        transport = definition.transport
        has_direction = transport.direction_field is not None or transport.direction is not None
        if has_direction and transport.direction_policy != "positive-dot":
            raise ValueError("configured topology direction providers require positive-dot policy")


def neighbor_address(
    origin: Address3,
    port: int,
    shape: Address3,
    boundary: str,
    topology: PortTopology = DEFAULT_TOPOLOGY,
) -> Address3 | None:
    """Return one configured neighbor, or an actual open terminal destination.

    Each transfer crosses exactly one declared link. The default port order is
    +X, -X, +Y, -Y, +Z, -Z. No stock is read or changed by this helper.
    """
    if boundary not in ("periodic", "open"):
        raise ValueError("boundary must be periodic or open")
    validate_position(origin, shape, topology)
    if not 0 <= bounded(port) < topology.degree:
        raise ValueError("port index exceeds the configured topology")
    offset = topology.offsets[port]
    coordinates = tuple(bounded(value + delta) for value, delta in zip(origin, offset, strict=True))
    if boundary == "periodic":
        coordinates = tuple(value % extent for value, extent in zip(coordinates, shape, strict=True))
    elif any(not 0 <= value < extent for value, extent in zip(coordinates, shape, strict=True)):
        return None
    target = (coordinates[0], coordinates[1], coordinates[2])
    if not site_allowed(target, topology):
        raise ValueError("neighbor does not belong to the configured site pattern")
    return target
