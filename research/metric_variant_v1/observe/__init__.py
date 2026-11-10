"""observe/: READ-ONLY observables of already determined states (AGENTS item 10). Nothing here changes a state or
feeds anything back into the dynamics."""
from __future__ import annotations

import numpy as np

from ..core.engine import ClickLog, State, extract_clicks, handedness_kind
from ..core.tensor import Tensor


def gear_field(state: State, tensor: Tensor, name: str, field: str = "b") -> np.ndarray:
    """Copy of one gear type's field as an (L, L, L) array indexed [x, y, z]."""
    if field not in ("a", "b", "r"):
        raise ValueError("field must be a, b or r")
    g = tensor.gear_index(name)
    L = state.L
    return getattr(state, field)[g].copy().reshape(L, L, L)


__all__ = ["ClickLog", "extract_clicks", "handedness_kind", "gear_field"]
