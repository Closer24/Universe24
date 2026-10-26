"""H-Angular-Momentum-In-The-Clicks-1: the clicks' J read from the log alone equals the board's L2 change across every close (the hole to 12 intervals, exact to the integer), and a Link's current has one moment from either end (the arm along the axis drops out of the cross product). Under 15 s."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from moment_of_clicks import cross, moment_of_clicks  # noqa: E402
from board_across_close import L2P  # noqa: E402
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.interval import Interval
from event_universe.core.ports import AXES

WORLDS = Path(__file__).parents[4] / "tests" / "worlds"


def test_one_link_one_moment():
    """A current along axis a has the same moment about any centre from either end of its Link (and across the torus's seam)."""
    for a in range(AXES):
        p = [0, 0, 0]
        p[a] = 7
        for r in ([1, 2, 3], [0, 4, 4], [4, 0, 1]):
            for k in (1, -1, 4, -4):
                s = list(r)
                s[a] += k
                assert cross(r, p) == cross(s, p)


def test_clicks_J_is_the_boards_change_across_the_close():
    sys.set_int_max_str_digits(0)
    universe, world = load_world(str(WORLDS / "world_hole.json"))
    node = Node(universe, world)
    c = node.cube
    idx = np.indices(node.shape)
    X = [idx[a].astype(object) for a in range(AXES)]
    board = {}
    for _ in range(12):
        iv = Interval(node, 1)
        iv.readings(); iv.kick(); iv.division(); iv.swap()
        L3, _ = L2P(node.records(), X, c)
        iv.close()
        L4, _ = L2P(node.records(), X, c)
        board[node.interval] = [x - y for x, y in zip(L4, L3)]
    J = moment_of_clicks({"log": node.log, "cube": c})
    assert J["counts"]["births"] == 8 and J["closes with a click"] >= 3
    assert any(any(v) for v in board.values())
    for i, d in board.items():
        assert d == J["per close"].get(i, {"J": [0, 0, 0]})["J"], (i, d)
    assert J["senses summed over the births' children"] == 0
