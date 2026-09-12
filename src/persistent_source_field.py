"""Compatibility entry point. Install event-universe, then keep existing imports.

The active implementation is event_universe; this file contains no copied physics.
Running this file delegates to the active CLI, which requires --init and is headless
by default. Use --visualize only when a recorded HTML display is requested.
"""

from event_universe.compat import IntegerO1Field, IntegerO1Field3D
from event_universe.core.state import (
    AXIS_PHASE,
    CELL_REGISTERS,
    DIRECTIONS,
    FIELD_PX,
    FIELD_PY,
    FIELD_PZ,
    FIELD_REM,
    FORCE_RX,
    FORCE_RY,
    FORCE_RZ,
    LAST_UPDATE_TICK,
    MAX_CORE_INT,
    MINUS_X,
    MINUS_Y,
    MINUS_Z,
    MOVE_BUDGET,
    PARTICLE_REGISTERS,
    PHI,
    PLUS_X,
    PLUS_Y,
    PLUS_Z,
    PX,
    PY,
    PZ,
    Config,
    X,
    Y,
    Z,
    checked,
    signed_divrem,
)
from event_universe.diagnostics.numeric_audit import static_integer_audit

__all__ = [
    "AXIS_PHASE",
    "CELL_REGISTERS",
    "Config",
    "DIRECTIONS",
    "FIELD_PX",
    "FIELD_PY",
    "FIELD_PZ",
    "FIELD_REM",
    "FORCE_RX",
    "FORCE_RY",
    "FORCE_RZ",
    "IntegerO1Field",
    "IntegerO1Field3D",
    "LAST_UPDATE_TICK",
    "MAX_CORE_INT",
    "MINUS_X",
    "MINUS_Y",
    "MINUS_Z",
    "MOVE_BUDGET",
    "PARTICLE_REGISTERS",
    "PHI",
    "PLUS_X",
    "PLUS_Y",
    "PLUS_Z",
    "PX",
    "PY",
    "PZ",
    "X",
    "Y",
    "Z",
    "checked",
    "signed_divrem",
    "static_integer_audit",
]

if __name__ == "__main__":
    from event_universe.runner import main

    main()
