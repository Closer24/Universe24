"""The one-Node tests (the owner's word of 2026-10-25: every property tested on one Node fed through its six Links): the horizon (a Node whose x Links stand at the wall holds on that axis, is read by no Link close and births nothing), the frozen content (a Node at the Link pace 0 is not read and never clicks), the turn (the turned Node ends the interval at its pre-state exchanged and complemented, the exchange an involution), the run back exact through all of it; the step's reach of one Link forward and none back; the files' refusals by name."""

from __future__ import annotations

import copy
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import PORT_SIDES
from event_universe.features import volume
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE
from tests.laws import node_of, refused, run_back_exact, state_of, world_of

CENTRE = (1, 1, 1)  # the fed Node, the 3-cube's centre
INTERVALS = 20


def level_at(node: Node, content: int) -> int:
    """The carrier's level at a content."""
    return int(
        np.asarray(
            volume.volume_of(node.gamma, np.array([content], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )


def pace_at(node: Node, content: int) -> int:
    return int(
        np.asarray(
            paces.link_pace_of(node.gamma, np.array([content], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )


def clicks_at(node: Node, at: tuple[int, ...]) -> list[dict[str, Any]]:
    """The births and credits logged at the Node, and the births whose children land there."""
    own = [e for e in node.log if tuple(e["node"]) == at and e["event"] in ("birth", "credit")]
    ends = [e for e in node.log if e["event"] == "birth" and at in (tuple(e["minus"]), tuple(e["plus"]))]
    return own + ends


def fed_horizon(node: Node, at: tuple[int, ...]) -> Node:
    """The Node's x axis line of the carrier fed to 2 Gamma, so the tension of its two x Links stands at Gamma and their factor is 0; its light far above two quanta, so a meeting would be read were the Node read."""
    axis = node.row(CARRIER).lines[1]
    axis.now[at] = 2 * node.gamma
    axis.before[at] = 2 * node.gamma
    light = node.row(PLANE, gap=0).lines[0]
    light.now[at] = 4 * int(light.now[at])
    node.ride_walls()
    return node


def test_the_horizon_holds_the_links_at_the_wall_and_the_node_never_clicks() -> None:
    node = fed_horizon(node_of("world_node.json"), CENTRE)
    factors = node.link_factors()
    assert [int(f[CENTRE]) for f in factors[:2]] == [0, 0]
    assert all(int(f[CENTRE]) > 0 for f in factors[2:])
    fed = copy.deepcopy(node)
    for _ in range(INTERVALS):
        node.step()
    assert clicks_at(node, CENTRE) == []
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def test_the_frozen_node_is_not_read_and_never_clicks() -> None:
    node = node_of("world_node.json")
    frozen = next(c for c in range(1, 100000) if pace_at(node, c) == 0)
    assert frozen == paces.frozen_content(node.gamma)
    carrier = node.row(CARRIER).lines[0]
    carrier.now[CENTRE] = level_at(node, frozen)
    carrier.before[CENTRE] = carrier.now[CENTRE]
    node.ride_walls()
    light = node.row(PLANE, gap=0).lines[0]
    light.now[CENTRE] = 4 * int(light.now[CENTRE])
    fed = copy.deepcopy(node)
    for _ in range(INTERVALS):
        node.step()
    assert clicks_at(node, CENTRE) == []
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def exchanged(node: Node, held: list[list[Any]], at: tuple[int, ...]) -> bool:
    """Every line at the Node is the held line exchanged and complemented: the levels exchanged (an im line conjugated), the rotation remainder complemented at its wall (an im line's kept), the write remainder complemented at the write wall."""
    flat = [line for row in held for line in row]
    for line, h, im in zip(node.all_lines(), flat, node.is_im(), strict=True):
        sign = -1 if im else 1
        wall = int(np.asarray(line.wall)[at]) if np.ndim(line.wall) else int(line.wall)
        if int(line.now[at]) != sign * int(h.before[at]) or int(line.before[at]) != sign * int(
            h.now[at]
        ):
            return False
        if int(line.rem[at]) != (int(h.rem[at]) if im else wall - 1 - int(h.rem[at])):
            return False
        if line.wr is not None and int(line.wr[at]) != line.wwall - 1 - int(h.wr[at]):
            return False
    return True


def bumped(node: Node) -> Node:
    """The carrier's time line at the centre fed a bump with before = now above its neighbours, so the Node turns alone at the first interval."""
    bump = level_at(node, 40)
    carrier = node.row(CARRIER).lines[0]
    carrier.now[CENTRE] = bump
    carrier.before[CENTRE] = bump
    node.ride_walls()
    return node


def sea_only(name: str) -> Node:
    universe, world = world_of(name)
    return Node(universe, dict(world, seed=[lay for lay in world["seed"] if lay.get("lay") == "sea"]))


def test_the_turn_is_the_pre_state_exchanged_and_complemented_and_runs_back_exact() -> None:
    node = bumped(sea_only("world_node.json"))
    fed = copy.deepcopy(node)
    held = [[line.copy() for line in row] for row in node.rows()]
    node.step()
    turned = [tuple(int(x) for x in q) for q in zip(*np.nonzero(node.turned), strict=True)]
    assert turned == [CENTRE]
    assert exchanged(node, held, CENTRE)
    twice = copy.deepcopy(node)
    before = state_of(twice)
    for _ in range(2):
        twice.exchange(node.turned, [[line.copy() for line in row] for row in twice.rows()])
    assert state_of(twice) == before
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def test_the_turn_at_the_horizon_runs_back_exact() -> None:
    node = fed_horizon(bumped(sea_only("world_node.json")), CENTRE)
    fed = copy.deepcopy(node)
    node.step()
    assert [tuple(int(x) for x in q) for q in zip(*np.nonzero(node.turned), strict=True)] == [CENTRE]
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def differences(a: Node, b: Node, origin: tuple[int, ...]) -> set[int]:
    """The torus distances from the origin of every Node where the two boards' lines differ."""
    found = set()
    for ra, rb in zip(a.rows(), b.rows(), strict=True):
        for la, lb in zip(ra, rb, strict=True):
            for slot in ("now", "before", "rem", "wr"):
                xa, xb = getattr(la, slot), getattr(lb, slot)
                if xa is None:
                    continue
                for where in zip(*np.nonzero(np.asarray(xa != xb)), strict=True):
                    node = tuple(int(x) for x in where)
                    found.add(
                        sum(
                            min(abs(node[k] - origin[k]), a.cube - abs(node[k] - origin[k]))
                            for k in range(3)
                        )
                    )
    return found


def test_the_step_reaches_one_link_forward_and_none_back() -> None:
    at = (2, 2, 2)
    a = sea_only("world_hole.json")
    for _ in range(2):
        a.step()
    b = copy.deepcopy(a)
    light = b.row(PLANE, gap=0).lines[0]
    light.now[at] = light.now[at] + 1
    assert differences(a, b, at) == {0}
    a.step()
    b.step()
    assert a.counts["births"] == b.counts["births"] == 0
    assert differences(a, b, at) <= {0, 1}
    a2, b2 = copy.deepcopy(a), copy.deepcopy(a)
    light = b2.row(PLANE, gap=0).lines[0]
    light.now[at] = light.now[at] + 1
    a2.step_back()
    b2.step_back()
    assert differences(a2, b2, at) <= {0}


def test_the_files_are_refused_by_name() -> None:
    universe, world = world_of("world_node.json")
    refused("keys of no law: control", read_world, dict(world, control={"ride": "symmetric"}), universe)
    refused("keys of no law: detectors", read_world, dict(world, detectors=[[0, 0, 0]]), universe)
    refused(
        "a pair or a wall", read_world, world, dict(universe, rows=universe["rows"] + [{"shape": 1}])
    )
    refused(
        "light is the plane",
        Node,
        dict(universe, rows=universe["rows"] + [{"shape": 1, "pair": [1, 2]}]),
        world,
    )
    refused(
        "one shape-10 row",
        Node,
        dict(universe, rows=[r for r in universe["rows"] if r["shape"] != 10]),
        world,
    )
    refused(
        "the shape-4 row stands at",
        Node,
        dict(
            universe,
            rows=[
                dict(r, pair=[1, universe["integers"]["den"]]) if r["shape"] == 4 else r
                for r in universe["rows"]
            ],
        ),
        world,
    )
    refused("a cube", Node, universe, dict(world, shape=[3, 3, 4]))
    refused("off the board", Node, universe, dict(world, seed=[{"lay": "hole", "at": [3, 0, 0]}]))
    refused("no form of the law", Node, universe, dict(world, seed=[{"lay": "wave", "row": 0}]))
    refused("the massless plane's alone", Node, universe, dict(world, seed=[{"lay": "sea", "row": 1}]))
    refused(
        "half-width 2 or 3",
        Node,
        universe,
        dict(world, seed=[{"lay": "at", "row": 1, "centre": [1, 1, 1], "quanta": 1, "width": 4}]),
    )
    assert [r.shape for r in node_of("world_node.json").rows_] == [1, 2, 2, 2, 2, 4, 10]
    assert [(axis, side) for axis, side in PORT_SIDES][:2] == [(0, 1), (0, -1)]
