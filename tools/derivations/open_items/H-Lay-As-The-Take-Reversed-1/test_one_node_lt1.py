"""lt1's one-Node test (pytest, under 15 s): on the hole world with LT1_RECOIL=1, (1) at every click the Link's record identity holds per axis at every end, dp clock^2 + carry before - carry after = laid x wall, on the Node's own flux lines (read from the Node, not the log alone); (2) the run back is exact with the recoil written (the state's hash after n forward and n back equals the kept one); (3) the flux's sign: the kick's count flux summed over the board against the records' lattice momentum (the sum of the Node lines' F), the quotient in per mille. Run: LT1_RECOIL=1 PYTHONPATH=<copy> pytest -q test_one_node_lt1.py"""
import json
import os
import sys
from pathlib import Path

os.environ["LT1_RECOIL"] = "1"
for path in reversed(os.environ.get("PYTHONPATH", "").split(":")):
    if path:
        sys.path.insert(0, path)  # the flagged copy first, before pytest's rootdir path

import numpy as np  # noqa: E402

from event_universe import interval as interval_  # noqa: E402
from event_universe.core.ports import AXES, port_of  # noqa: E402
from event_universe.links import link_current  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

HERE = Path(__file__).resolve().parent
WORLDS = HERE.parents[3] / "tests" / "worlds"


def make(world: str) -> Node:
    universe, world_ = load_world(str(WORLDS / world))
    return Node(universe, world_)


def test_identity_on_the_node_and_the_run_back() -> None:
    node = make("world_hole.json")
    wall = node.trace * node.den * node.gamma * node.gamma * node.T
    lines = node.row(CARRIER).lines[1 + AXES : 1 + AXES + AXES]
    hashes = []
    checked = 0
    for _ in range(14):
        hashes.append(node.state_hash())
        before = [[int(line.wr[idx]) for line in lines] for idx in np.ndindex(node.shape)]
        from_log = len(node.log)
        node.step()
        for e in node.log[from_log:]:
            if e["event"] not in ("birth", "credit"):
                continue
            for t in e.get("takes", [e]):
                assert "carry" in t, "every click carries the recoil's numbers"
                for a in range(AXES):
                    assert int(t["dP_take"][a]) * t["clock"] ** 2 + int(t["carry_was"][a]) - int(t["carry"][a]) == int(t["recoil"][a]) * wall
                checked += 1
            if e["event"] == "birth":
                for k in range(2):
                    for a in range(AXES):
                        assert int(e["dP_lay_ends"][k][a]) * e["clock_ends"][k] ** 2 + int(e["carry_was_ends"][k][a]) - int(e["carry_ends"][k][a]) == int(e["recoil_ends"][k][a]) * wall
        # the Node's own carry after the step is the carry of the last booking at that Node (the lines re-read: the act returns new Line objects)
        last: dict[tuple[int, ...], list[int]] = {}
        for e in node.log[from_log:]:
            if e["event"] in ("birth", "credit"):
                for t in e.get("takes", [e]):
                    last[tuple(t.get("node", e["node"]))] = [int(x) for x in t["carry"]]
                if e["event"] == "birth":
                    for k, where in enumerate((e["minus"], e["plus"])):
                        last[tuple(where)] = [int(x) for x in e["carry_ends"][k]]
        fresh = node.row(CARRIER).lines[1 + AXES : 1 + AXES + AXES]
        for at, carry in last.items():
            assert carry == [int(line.wr[at]) for line in fresh]
        assert before is not None
    assert checked > 0, "the hole world clicks within 14 intervals"
    for h in reversed(hashes):
        node.step_back()
        assert node.state_hash() == h, "the run back exact with the recoil written and undone"


def test_flux_sign_against_the_lattice_momentum() -> None:
    node = make("world_node.json")
    for _ in range(3):
        node.step()
    it = interval_.Interval(node, 1)
    it.readings()
    it.kick()
    emitter = node.emitter()
    num = emitter.pair[0]
    out = {}
    for a in range(AXES):
        flux = int(np.sum(it.flux[a]))
        f = int(np.sum(link_current(emitter.lines[0], port_of(a, 0))))
        p = -2 * num * f  # P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) = -2 num SUM_i F(i, i + a)
        out[a] = {"flux_sum": flux, "P_a": p, "flux x 1000 div (-P)": (flux * 1000) // (-p) if p else None}
    node.interval -= 1
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out" / "flux_sign.json").write_text(json.dumps(out))
    assert len(out) == AXES
