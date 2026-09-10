"""Hierarchical 3D spatial focus for deferred quantum event selection.

Focus is a quantum-oracle computation, not a new physical lattice or a sequence
of measurements. A half-open integer region is recursively subdivided until one
canonical cell is reached. One integer ticket is narrowed through every level,
so refinement does not resample or alter the underlying categorical outcome.
"""

from dataclasses import dataclass
from typing import NamedTuple

from event_universe.core.state import Address, checked, checked_work

from .postulates import ORACLE_COST, OracleCost
from .state import checked_address


class Region3D(NamedTuple):
    """Half-open canonical-address box: [x0,x1) × [y0,y1) × [z0,z1)."""

    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int


class FocusCandidate(NamedTuple):
    """One distinguishable event outcome already represented by one quantum root."""

    root: int
    address: Address
    outcome: int


class WeightedFocusCandidate(NamedTuple):
    root: int
    address: Address
    outcome: int
    weight: int


class FocusStep(NamedTuple):
    region: Region3D
    child_count: int
    selected_child: int
    selected_weight: int
    total_event_weight: int


@dataclass(frozen=True, slots=True)
class FocusRequest:
    """One logical search for the next event within a canonical world region."""

    request_id: int
    region: Region3D
    candidates: tuple[FocusCandidate, ...]
    tick: int
    ticket: int
    no_event_weight: int = 0

    def __post_init__(self) -> None:
        checked(self.request_id)
        checked_region(self.region)
        checked(self.tick)
        checked(self.ticket)
        checked(self.no_event_weight)
        if min(self.request_id, self.tick, self.ticket, self.no_event_weight) < 0:
            raise ValueError("focus identifiers, tick, ticket and weights must be non-negative")
        if type(self.candidates) is not tuple:
            raise TypeError("focus candidates must be an immutable tuple")
        seen: set[tuple[Address, int]] = set()
        for candidate in self.candidates:
            if type(candidate) is not FocusCandidate:
                raise TypeError("focus candidates must be FocusCandidate records")
            checked(candidate.root)
            checked_address(candidate.address)
            checked(candidate.outcome)
            if candidate.root < 0 or candidate.outcome < 0:
                raise ValueError("focus roots and outcomes must be non-negative")
            if not contains(self.region, candidate.address):
                raise ValueError("focus candidate lies outside the root region")
            key = (candidate.address, candidate.outcome)
            if key in seen:
                raise ValueError("focus candidates must identify distinct cell outcomes")
            seen.add(key)


@dataclass(frozen=True, slots=True)
class FocusEvent:
    """Oracle-selected candidate event; not yet a native Engine commit."""

    request_id: int
    tick: int
    address: Address
    outcome: int
    root: int
    ticket: int


@dataclass(frozen=True, slots=True)
class FocusReply:
    event: FocusEvent | None
    path: tuple[FocusStep, ...]
    event_weight: int
    no_event_weight: int
    total_weight: int
    evaluation_nodes: int
    focus_steps: int
    repeated: int

    @property
    def cost(self) -> OracleCost:
        return ORACLE_COST


def checked_region(region: Region3D) -> Region3D:
    if type(region) is not Region3D:
        raise TypeError("focus region must be Region3D")
    values = tuple(checked(value) for value in region)
    x0, x1, y0, y1, z0, z1 = values
    if x0 < 0 or y0 < 0 or z0 < 0:
        raise ValueError("focus region origin must be non-negative")
    if x0 >= x1 or y0 >= y1 or z0 >= z1:
        raise ValueError("focus region must have positive extent on every axis")
    return Region3D(x0, x1, y0, y1, z0, z1)


def region_from_shape(nx: int, ny: int, nz: int) -> Region3D:
    for value in (nx, ny, nz):
        checked(value)
        if value <= 0:
            raise ValueError("focus shape must be positive")
    return Region3D(0, nx, 0, ny, 0, nz)


def contains(region: Region3D, address: Address) -> bool:
    x, y, z = checked_address(address)
    return region.x0 <= x < region.x1 and region.y0 <= y < region.y1 and region.z0 <= z < region.z1


def is_unit(region: Region3D) -> bool:
    checked_region(region)
    return region.x1 - region.x0 == 1 and region.y1 - region.y0 == 1 and region.z1 - region.z0 == 1


def _split_axis(low: int, high: int) -> tuple[tuple[int, int], ...]:
    extent = checked_work(high - low)
    if extent <= 0:
        raise ValueError("focus axis must have positive extent")
    if extent == 1:
        return ((low, high),)
    midpoint = checked(low + extent // 2)
    return ((low, midpoint), (midpoint, high))


def split_region(region: Region3D) -> tuple[Region3D, ...]:
    """Split each non-unit axis in two; 3D cubes therefore produce eight children.

    Odd extents are split into floor/ceiling halves. Half-open boundaries ensure
    exact coverage without overlap, including non-power-of-two world dimensions.
    """
    region = checked_region(region)
    xs = _split_axis(region.x0, region.x1)
    ys = _split_axis(region.y0, region.y1)
    zs = _split_axis(region.z0, region.z1)
    if len(xs) == len(ys) == len(zs) == 1:
        return (region,)
    return tuple(
        Region3D(x0, x1, y0, y1, z0, z1)
        for x0, x1 in xs
        for y0, y1 in ys
        for z0, z1 in zs
    )


def sum_candidate_weights(candidates: tuple[WeightedFocusCandidate, ...]) -> int:
    total = 0
    for candidate in candidates:
        checked(candidate.weight)
        if candidate.weight < 0:
            raise ValueError("focus candidate weight must be non-negative")
        total = checked_work(total + candidate.weight)
    return checked(total)


def select_focused_event(
    request: FocusRequest,
    weighted: tuple[WeightedFocusCandidate, ...],
    evaluation_nodes: int,
) -> FocusReply:
    """Select by one global ticket, then reveal only the spatial path to its leaf."""
    checked(evaluation_nodes)
    if type(weighted) is not tuple or len(weighted) != len(request.candidates):
        raise ValueError("weighted candidates must match the focus request")
    event_weight = sum_candidate_weights(weighted)
    total_weight = checked(checked_work(event_weight + request.no_event_weight))
    if total_weight == 0:
        raise ValueError("zero total focus weight cannot define an event decision")
    if request.ticket >= total_weight:
        raise ValueError("focus ticket must be smaller than total weight")
    if request.ticket < request.no_event_weight:
        return FocusReply(
            None,
            (),
            event_weight,
            request.no_event_weight,
            total_weight,
            evaluation_nodes,
            0,
            0,
        )

    local_ticket = request.ticket - request.no_event_weight
    active = tuple(candidate for candidate in weighted if candidate.weight > 0)
    region = request.region
    steps: list[FocusStep] = []

    while not is_unit(region):
        children = split_region(region)
        child_weights = tuple(
            sum_candidate_weights(tuple(candidate for candidate in active if contains(child, candidate.address)))
            for child in children
        )
        subtotal = sum(child_weights)
        if subtotal != sum_candidate_weights(active):
            raise RuntimeError("focus partition lost or duplicated candidate weight")
        selected = -1
        for index, child_weight in enumerate(child_weights):
            if local_ticket < child_weight:
                selected = index
                break
            local_ticket -= child_weight
        if selected < 0:
            raise RuntimeError("focus ticket did not map to a child region")
        chosen = children[selected]
        steps.append(FocusStep(region, len(children), selected, child_weights[selected], subtotal))
        active = tuple(candidate for candidate in active if contains(chosen, candidate.address))
        region = chosen

    ordered = tuple(sorted(active, key=lambda candidate: (candidate.outcome, candidate.root)))
    selected_candidate: WeightedFocusCandidate | None = None
    for candidate in ordered:
        if local_ticket < candidate.weight:
            selected_candidate = candidate
            break
        local_ticket -= candidate.weight
    if selected_candidate is None:
        raise RuntimeError("focus ticket did not map to a leaf outcome")

    event = FocusEvent(
        request.request_id,
        request.tick,
        selected_candidate.address,
        selected_candidate.outcome,
        selected_candidate.root,
        request.ticket,
    )
    return FocusReply(
        event,
        tuple(steps),
        event_weight,
        request.no_event_weight,
        total_weight,
        evaluation_nodes,
        len(steps),
        0,
    )
