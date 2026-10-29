"""Tensor24's one joint: the engine's functions passed into the runner, the only module that imports both."""

from pathlib import Path
from typing import Any

from tensor24.engine import kinds, state, step
from tensor24.runner import load, run


def made(shape: tuple[int, ...]) -> tuple[kinds.Kinds, dict[Any, Any]]:
    """The 24's kinds on the board's axes and their tables, as the load reads them."""
    matrix, weight = kinds.turns(kinds.axes(len(shape)))
    held = kinds.kinds(matrix)
    return held, load.tables(held, kinds.kinds(kinds.inverse(matrix)), weight, kinds.projector)


def layout(universe: dict[str, Any], shape: list[int], loaded: load.Loaded) -> state.Layout:
    """The layout the load reads from the three files, in the engine's records."""
    nb, meshes, grip, gearing, plan, rate, gamma, clock = load.laid_out(universe, shape, loaded)
    return state.Layout(
        nb, meshes, grip, state.Gearing(*gearing), state.Plan(*plan), rate, gamma, state.Read(*clock)
    )


ENGINE = run.Engine(made, layout, step.tick, step.untick, state.State)


def ran(paths: list[Path], record: Path, bits: Any = None) -> list[str]:
    """The three files run to the record by the engine's own functions, every due beat firing or the caller's masks."""
    return run.run(ENGINE, paths, record, bits)
