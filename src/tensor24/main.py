"""Tensor24's one joint: the engine's functions passed into the runner, the only module that imports both."""

from pathlib import Path
from typing import Any

from tensor24.engine import kinds, state, step
from tensor24.runner import load, run


def made(spokes: Any) -> tuple[kinds.Kinds, dict[Any, Any], Any]:
    """The 24's kinds and their tables, and the four-vector's square on the 24, derived once from the Node-clock's own star, its Spokes, as the load reads them."""
    matrix, weight = kinds.turns(spokes)
    held = kinds.kinds(matrix)
    c = load.tables(held, kinds.kinds(kinds.inverse(matrix)), weight, kinds.projector)
    turned = kinds.kinds(
        matrix[weight == 1]
    )  # the five kinds on the 24 alone, the candidates Rule3 weighs 1
    return turned, c, kinds.square(turned)


def layout(universe: dict[str, Any], shape: list[int], loaded: load.Loaded) -> state.Layout:
    """The layout the load reads from the three files, in the engine's records."""
    nb, spokes, meshes, grip, gearing, plan, clock = load.laid_out(universe, shape, loaded)
    typed = state.Gearing(*gearing), state.Plan(*plan), state.Read(*clock)
    return state.Layout(nb, spokes, meshes, grip, *typed)


ENGINE = run.Engine(made, layout, step.tick, step.untick, state.State)


def ran(paths: list[Path], record: Path) -> list[str]:
    """The three files run to the record and its ledger by the engine's own functions, every Node-clock in every round."""
    return run.run(ENGINE, paths, record)
