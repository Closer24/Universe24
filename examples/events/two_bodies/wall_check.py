"""The same force formula on the wall's own field.

In the alone world the share-weighted dU/dx over the body (the wall's asymmetry) against the measured wall push
+1.14e-05, and in the pair world the total over A against +3.72e-05; the coefficient 0.2204 is gradient_check.py's and
the accelerations are those measured on fall_results_49x17.json, both standing here as literals. Reads the two worlds
run_fall2.py wrote under runs/two_bodies/ at the repository root and writes wall_check.json beside them; the shipped
copy stands beside this script.
"""

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from event_universe import node  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402

RUNS = REPO / "runs" / "two_bodies"
GAMMA, NUM, DEN = 6000, 4000, 6000
PAIR, ALONE = "fall_pair_49x17.json", "fall_alone_49x17.json"


def loaded(name):
    """The world under runs/two_bodies/ at its start: the content every family reads and the share read at the paces."""
    world = load_world(RUNS / name)
    board = Lattice(world, (lambda s: None))
    mi = {f.name: i for i, f in enumerate(board.families)}["matter"]
    content, axes = node.read_lines(mi, board.families, board.states, 1, 0)
    return np.asarray(content), axes, np.asarray(board.quanta(mi)[0], dtype=float), board


coef = 0.2204
out = {}
for name, label, measured in (
    (ALONE, "alone (wall only)", 1.14e-5),
    (PAIR, "pair, body A (wall + B)", 3.72e-5),
):
    c, _axes, n, _board = loaded(name)
    c = c.astype(float)
    dU = np.zeros_like(c)
    dU[1:-1] = (c[2:] - c[:-2]) / 2 / GAMMA
    w = n.copy()
    w[24:] = 0
    g = float((dU * w).sum() / w.sum())
    ratio = measured / (coef * g) if g else float("nan")
    print(
        f"{label}: share-weighted dU/dx over A = {g:+.3e} per Link -> a_pred = {coef * g:+.3e}; "
        f"measured {measured:+.2e}; ratio measured/pred = {ratio:.2f}"
    )
    out[label] = {"grad": g, "a_pred": coef * g, "measured": measured}
(RUNS / "wall_check.json").write_text(json.dumps(out))
