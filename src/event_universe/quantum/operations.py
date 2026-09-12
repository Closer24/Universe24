"""Finite host-side matrix builders; no particle names select these operations.

The builders express declared local candidate laws. They are not evidence that
such laws, material parameters or a classical limit emerged from the lattice.
"""

from .event_rules import LocalChannel, LocalInstrument, LocalUnitary, Matrix
from .state import checked_amp


def integer_matrix(rows: tuple[tuple[int, ...], ...]) -> Matrix:
    """Convert signed integer coefficients to the shared complex-pair schema."""
    return tuple(tuple(checked_amp(v, 0) for v in row) for row in rows)


def basis_measurement(dimension: int) -> LocalInstrument:
    """Distinguish each level; a certain level needs no sampling."""
    if type(dimension) is not int or not 2 <= dimension <= 4:
        raise ValueError("basis measurement dimension must be two to four")
    return LocalInstrument(
        tuple(
            integer_matrix(
                tuple(tuple(int(i == j == k) for j in range(dimension)) for i in range(dimension))
            )
            for k in range(dimension)
        )
    )


def dephasing(dimension: int) -> LocalChannel:
    """Discard a basis record without selecting, exposing or resampling it."""
    return LocalChannel(basis_measurement(dimension).branches)


def permutation(targets: tuple[int, ...], signs: tuple[int, ...] = ()) -> LocalUnitary:
    """Map each input column to one output row with an optional integer sign."""
    size = len(targets)
    if (
        type(targets) is not tuple
        or not 2 <= size <= 16
        or any(type(i) is not int for i in targets)
        or set(targets) != set(range(size))
    ):
        raise ValueError("targets must be a bounded basis permutation")
    if type(signs) is not tuple or (signs and len(signs) != size):
        raise ValueError("one sign per input column required")
    signs = signs or (1,) * size
    if any(type(sign) is not int or sign not in (-1, 1) for sign in signs):
        raise ValueError("permutation signs must be integer minus or plus one")
    return LocalUnitary(
        integer_matrix(
            tuple(tuple(signs[j] if targets[j] == i else 0 for j in range(size)) for i in range(size))
        )
    )


def transition_instrument(dimension: int, source: int, target: int) -> LocalInstrument:
    """One directed level transition and its no-transition outcome.

    This is a supplied amplitude-transfer instrument, not a bosonic ladder
    operator: number-dependent matrix elements and reservoir energy are separate.
    """
    if type(dimension) is not int or not 2 <= dimension <= 4:
        raise ValueError("transition dimension must be two to four")
    if any(type(i) is not int or not 0 <= i < dimension for i in (source, target)):
        raise ValueError("transition levels must lie in the register basis")
    return LocalInstrument(
        (
            integer_matrix(
                tuple(
                    tuple(int(i == j and i != source) for j in range(dimension))
                    for i in range(dimension)
                )
            ),
            integer_matrix(
                tuple(
                    tuple(int(i == target and j == source) for j in range(dimension))
                    for i in range(dimension)
                )
            ),
        )
    )
