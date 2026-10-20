"""The Link's share of the force.

In the pair and the alone worlds at t = 0, the six Link tensions and factors Q_ij at every Node (features/read:
link_tensions, link_factors), and over body A (weighted by the share) the x-asymmetry of the effective hopping
rho_i Q_ij / G^2, set beside the clock's gradient 4 dU/dx (the hopping's N^4) and the mass term's 2 dU/dx. Reads the two
worlds run_fall2.py wrote under runs/two_bodies/ at the repository root and writes tension_check.json beside them; the
shipped copy stands beside this script.
"""

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from event_universe import node  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.features.read import link_factors, link_tensions  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402

RUNS = REPO / "runs" / "two_bodies"
GAMMA = 6000
PAIR, ALONE = "fall_pair_49x17.json", "fall_alone_49x17.json"


def loaded(name):
    """The world under runs/two_bodies/ at its start: the content every family reads and the share read at the paces."""
    world = load_world(RUNS / name)
    board = Lattice(world, (lambda s: None))
    mi = {f.name: i for i, f in enumerate(board.families)}["matter"]
    content, axes = node.read_lines(mi, board.families, board.states, 1, 0)
    return np.asarray(content), axes, np.asarray(board.quanta(mi)[0], dtype=float), board


G = 16


def analyse(name):
    content, axes, n, board = loaded(name)
    w = n.copy()
    w[24:] = 0
    W = w.sum()
    tens = link_tensions(axes, board.wrap)
    Q = [np.asarray(q, dtype=float) for q in link_factors(GAMMA, G, tens)]
    T = [np.asarray(t, dtype=float) for t in tens]
    p0, pi = paces.node_paces(GAMMA, content.astype(int))
    p0 = np.asarray(p0, dtype=float)
    pi = np.asarray(pi, dtype=float)
    U = content.astype(float) / GAMMA
    dU = np.zeros_like(U)
    dU[1:-1] = (U[2:] - U[:-2]) / 2
    g_clock = float((dU * w).sum() / W)
    # the effective hopping along +x and -x per Node, and its asymmetry relative to rho
    asym = (Q[0] - Q[1]) / G**2  # (Q_+x - Q_-x) / G^2 per Node
    g_link = float((asym * w).sum() / W)  # the Link's own gradient term, dimensionless per Link
    tmag = float(((np.abs(T[0]) + np.abs(T[1])) / 2 * w).sum() / W)
    print(
        f"{name}: tensions over A: mean |t_x| = {tmag:.2f} (of Gamma {GAMMA}); "
        f"Q range {min(q.min() for q in Q):.0f}..{max(q.max() for q in Q):.0f} (G^2 = {G * G})"
    )
    print(
        f"   clock: dU/dx = {g_clock:+.3e}  -> the hopping gradient 4 dU/dx = {4 * g_clock:+.3e}, "
        f"the mass gradient 2 dU/dx = {2 * g_clock:+.3e}"
    )
    print(
        f"   Link : (Q+x - Q-x)/G^2 over A = {g_link:+.3e}   (compare with the hopping gradient; same sign = adds)"
    )
    tx = [round(float(v), 2) for v in T[0][:, 8, 8]]
    print(f"   t_+x along the axis: {tx}")
    return {"g_clock": g_clock, "g_link": g_link, "tmag": tmag}


out = {n: analyse(n) for n in (PAIR, ALONE)}
(RUNS / "tension_check.json").write_text(json.dumps(out))
print("done")
