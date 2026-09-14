"""Exact finite spatial-momentum diagnostics, never ordinary movement inputs.

For an oriented edge (a, b), P[a, b] = -i and P[b, a] = +i. Thus P is
-i(T - T.adjoint) with T[a, b] = 1; T reads the forward neighbor rather than
moving a basis state forward. This supplied finite derivative observable is
dimensionless, not a derived canonical momentum or a kinetic Hamiltonian.

The quantum diagnostic reads the actual reduced density, including coherence.
Only local_position_moments accepts physical preparation data: an immutable
local operator row with at most six signed unit entries, without any state.
"""

from fractions import Fraction

from event_universe.core.state import checked
from event_universe.core.topology import neighbor_address
from event_universe.quantum.event_network import EventNetwork


def local_position_moments(local_row: tuple[int, ...]) -> dict[str, int]:
    """Moments of a rank-one position reencoding from its local operator row.

    Entries are the nonzero imaginary coefficients of the zero-diagonal P row.
    Graph authoring must supply one entry per distinct incident Link. No quantum
    state, event outcome, network or global estimator enters this calculation.
    Absorbing a wave leaves vacuum; this describes a separately declared
    reencoding of the localized ordinary output as a position state.
    """
    if (
        type(local_row) is not tuple
        or len(local_row) > 6
        or any(type(value) is not int or value not in (-1, 1) for value in local_row)
    ):
        raise ValueError("a fixed local row requires at most six signed unit integer entries")
    second = checked(sum(value * value for value in local_row))
    return {"mean_momentum": 0, "second_moment": second, "variance": second}


def _operator(network, mode_registers, oriented_edges):
    """Build the imaginary coefficient matrix of a finite simple local graph."""
    if (
        type(mode_registers) is not tuple
        or not 1 <= len(mode_registers) <= 30
        or any(
            type(index) is not int or not 0 <= index < len(network.config.addresses)
            for index in mode_registers
        )
        or len(set(mode_registers)) != len(mode_registers)
    ):
        raise ValueError("distinct bounded spatial mode register IDs are required")
    if any(network.config.local_dimensions[index] != 2 for index in mode_registers):
        raise ValueError("spatial occupation modes must be binary")
    addresses = tuple(network.config.addresses[index] for index in mode_registers)
    if len(set(addresses)) != len(addresses):
        raise ValueError("spatial mode locations must be distinct")
    if type(oriented_edges) is not tuple or len(oriented_edges) > 90:
        raise ValueError("a bounded immutable oriented edge tuple is required")
    indices = {register: index for index, register in enumerate(mode_registers)}
    matrix = [[0] * len(indices) for _ in indices]
    seen = set()
    for edge in oriented_edges:
        if (
            type(edge) is not tuple
            or len(edge) != 2
            or any(type(index) is not int or index not in indices for index in edge)
            or edge[0] == edge[1]
        ):
            raise ValueError("an edge must join two distinct selected spatial modes")
        pair = frozenset(edge)
        if pair in seen:
            raise ValueError("duplicate or oppositely repeated edges are not supported")
        seen.add(pair)
        left, right = (network.config.addresses[index] for index in edge)
        space = network.event_space
        adjacent = (
            sum(abs(a - b) for a, b in zip(left, right, strict=True)) == 1
            if space.shape is None
            else any(
                neighbor_address(left, port, space.shape, space.boundary) == right for port in range(6)
            )
        )
        if not adjacent:
            raise ValueError("spatial momentum edges must follow neighboring Links")
        a, b = (indices[index] for index in edge)
        matrix[a][b], matrix[b][a] = -1, 1
    if any(sum(value != 0 for value in row) > 6 for row in matrix):
        raise ValueError("a spatial momentum row cannot exceed six neighbors")
    return matrix


def spatial_moments(
    network: EventNetwork,
    mode_registers: tuple[int, ...],
    oriented_edges: tuple[tuple[int, int], ...],
) -> dict[str, Fraction | str | None]:
    """Read exact conditional single-excitation moments from pure or mixed state.

    Edges contain register IDs, not offsets into mode_registers. Other registers
    are traced out by the existing quantum owner. Vacuum has no particle moments;
    a partial vacuum sector is reported separately from the conditional moments.
    Multi-excitation support is rejected, never silently discarded or normalized
    into a one-particle state. Fractions belong only to this external diagnostic.
    """
    imaginary = _operator(network, mode_registers, oriented_edges)
    density = network.joint_density(mode_registers)
    levels = {1 << index: index for index in range(len(mode_registers))}
    total = occupied = 0
    entries = []
    for row, column, amplitude in density.entries:
        if (row != 0 and row not in levels) or (column != 0 and column not in levels):
            raise ValueError("spatial momentum requires at most one excitation in the selected modes")
        if row == column:
            total += amplitude.real
            if row:
                occupied += amplitude.real
        if row and column:
            entries.append((levels[row], levels[column], amplitude))
    if total <= 0 or not 0 <= occupied <= total:
        raise ValueError("invalid occupation density normalization")
    if not occupied:
        return {
            "status": "vacuum",
            "occupation_probability": Fraction(0),
            "mean_momentum": None,
            "second_moment": None,
            "variance": None,
        }
    # Tr(rho P) and Tr(rho P^2): P is purely imaginary and antisymmetric.
    mean_real = mean_imag = second_real = second_imag = 0
    for row, column, amplitude in entries:
        coefficient = imaginary[column][row]
        mean_real -= amplitude.imag * coefficient
        mean_imag += amplitude.real * coefficient
        second = -sum(
            imaginary[column][middle] * imaginary[middle][row] for middle in range(len(mode_registers))
        )
        second_real += amplitude.real * second
        second_imag += amplitude.imag * second
    if mean_imag or second_imag:
        raise ArithmeticError("a Hermitian spatial observable must have real moments")
    mean, second = Fraction(mean_real, occupied), Fraction(second_real, occupied)
    variance = second - mean * mean
    if variance < 0:
        raise ArithmeticError("spatial momentum variance cannot be negative")
    return {
        "status": "single_excitation" if occupied == total else "partial_occupation",
        "occupation_probability": Fraction(occupied, total),
        "mean_momentum": mean,
        "second_moment": second,
        "variance": variance,
    }
