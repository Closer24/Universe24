"""Clock: the one joint: the Node-clock's act handed to the runner that turns it.
Algebra: n/a: it computes nothing; it passes the engine's functions and the layout to the runner.
Board: the board's layout made from the loaded files, then the run.
Clicks: n/a.
"""

from pathlib import Path
from typing import Any

from tensor24.engine import contract, kinds, state, step
from tensor24.runner import load, run


def made(spokes: Any) -> tuple[kinds.Kinds, dict[Any, Any], Any]:
    """The 24's kinds and their tables, and the four-vector's square on the 24, derived once from the Node-clock's own star, its Spokes, as the load reads them: every candidate weighed by Rule3, 0 off the 24."""
    matrix, weight = kinds.turns(spokes)
    held = kinds.kinds(matrix)
    c = load.tables(kinds.stacked(held), kinds.stacked(kinds.kinds(kinds.inverse(matrix))), weight)
    turned = kinds.weighed(held, weight)
    return turned, c, kinds.square(turned)


def layout(universe: dict[str, Any], shape: list[int], loaded: load.Loaded) -> state.Layout:
    """The layout the load reads from the three files, in the engine's records."""
    return typed(load.laid_out(universe, shape, loaded))


def typed(parts: tuple[Any, ...]) -> state.Layout:
    """The load's eleven parts in the engine's records."""
    nb, spokes, meshes, grip, gearing, potential, clock, stretch, click, push, mesh = parts
    records = (
        state.Gearing(*gearing),
        contract.pushes(*potential),
        state.Plan(*clock),
        state.Read(*stretch),
        state.Click(*click),
        state.Plan(*push),
        state.Plan(*mesh),
    )
    return state.Layout(nb, spokes, meshes, grip, *records)


ENGINE = run.Engine(made, layout, step.act, step.untick, state.State, step.dials, step.grips)


def ran(paths: list[Path], record: Path) -> list[str]:
    """The three files run to the record and its ledger by the engine's own functions, every Node-clock in every round."""
    return run.run(ENGINE, paths, record)
