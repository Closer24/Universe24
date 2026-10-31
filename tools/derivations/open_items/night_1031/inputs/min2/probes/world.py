"""Load a shipped world on an extracted tree by the runner's own steps (run.run's), whole numbers only."""
import json
import sys
from pathlib import Path


def tree_on(tree):
    sys.path.insert(0, str(Path(tree).joinpath("src")))


def loaded(tree, world):
    from tensor24 import main
    from tensor24.engine import state
    from tensor24.runner import files
    from tensor24.runner import load as L
    paths = [Path(world).joinpath(n + ".json") for n in ("universe", "piece", "setting")]
    found = files.departures(*paths)
    assert not found, found
    universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
    shape = piece["shape"]
    kinds, tables, square, lifted = main.ENGINE.made(files.star(len(shape)))
    found = files.held_departures(universe, setting, files.vocabulary(kinds, square, lifted))
    assert not found, found
    ld, found = L.load(universe, setting, files.sites_of(shape), kinds, tables, square, lifted)
    assert not found, found
    layout = main.ENGINE.layout(universe, shape, ld)
    start = state.State(*ld.state)
    return universe, setting, shape, kinds, ld, layout, start
