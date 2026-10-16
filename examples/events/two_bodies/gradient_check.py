"""The content gradient at body A from body B at t = 0 against the measured mutual acceleration.

Reads the pair and the alone worlds run_fall2.py wrote (49 x 17 x 17, under runs/two_bodies/ at the repository root),
the content every family reads (node.read_lines) and A's share; B's field is pair - alone; a_pred = 2 (1 - nu) N^2
(R / w) / sin^2(omega_0) x dU/dx, weighted by the share over A, with U = content / Gamma. The band's 2 cos omega_0 =
1646 / 1202 is the pixel's own (examples/events/matter_alone/pixel.mode.json) and stands here as a literal, as do the
accelerations measured on fall_results_49x17.json (quadratic fits over 0..300). Writes gradient_check.json beside the
worlds; the shipped copy stands beside this script.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from event_universe import node  # noqa: E402
from event_universe.core import paces  # noqa: E402
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


c_pair, _axes, n_pair, _bp = loaded(PAIR)
c_alone, _axes, n_alone, _ba = loaded(ALONE)
c_pair = c_pair.astype(float)
c_alone = c_alone.astype(float)
field_B = c_pair - c_alone  # B's content at A's region (the wall is in both)
mid = (slice(None), 8, 8)
print("content along the axis at t=0 (pair):", [int(v) for v in c_pair[mid]])
print("B field along the axis (pair - alone):", [round(float(v), 1) for v in field_B[mid]])
# the gradient of U = content / Gamma along x, central differences, weighted by the share over body A (x < 24)
dU = np.zeros_like(field_B)
dU[1:-1] = (field_B[2:] - field_B[:-2]) / 2 / GAMMA
wA = n_alone.copy()
wA[24:] = 0
grad = float((dU * wA).sum() / wA.sum())
# the body's own N^2 and R/w, weighted by the share, from the pair's content
p0, pi = paces.node_paces(GAMMA, c_pair.astype(int))
p0 = np.asarray(p0, dtype=float)
pi = np.asarray(pi, dtype=float)
N2 = float(((p0 / GAMMA) ** 2 * wA).sum() / wA.sum())
Rw = float((NUM * pi**2 / (3 * DEN * GAMMA**2) * wA).sum() / wA.sum())
two_cos0 = 1646 / 1202
om0 = math.acos(two_cos0 / 2)
nu = NUM / DEN
coef = 2 * (1 - nu) * N2 * Rw / math.sin(om0) ** 2
a_pred = coef * grad
print(
    f"share-weighted dU/dx at A from B: {grad:.3e} per Link  (content slope {grad * GAMMA:.3f} units/Link)"
)
print(f"N^2 {N2:.4f}  R/w {Rw:.4f}  coefficient 2(1-nu)N^2(R/w)/sin^2(omega0) = {coef:.4f}")
print(
    f"a_pred = {a_pred:.3e} Links/interval^2   measured mutual (A - alone) = +2.57e-05, "
    "A alone-in-pair +3.72e-05, wall +1.14e-05"
)
found = {
    "grad": grad,
    "N2": N2,
    "Rw": Rw,
    "coef": coef,
    "a_pred": a_pred,
    "axis_content_pair": [int(v) for v in c_pair[mid]],
    "axis_field_B": [float(v) for v in field_B[mid]],
}
(RUNS / "gradient_check.json").write_text(json.dumps(found))
