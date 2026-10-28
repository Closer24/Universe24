"""Tensor24's one joint: the engine's functions passed into the runner, the only module that imports both."""

from typing import Any

from tensor24.engine import kinds
from tensor24.runner import load


def made(shape: tuple[int, ...]) -> tuple[kinds.Kinds, dict[Any, Any]]:
    """The 24's kinds on the board's axes and their tables, as the load reads them."""
    axes = kinds.axes(len(shape))
    matrix, weight = kinds.turns(axes)
    held = kinds.kinds(matrix, axes)
    return held, load.tables(held, kinds.kinds(kinds.inverse(matrix), axes), weight, kinds.projector)
