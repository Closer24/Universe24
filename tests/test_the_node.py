"""The one-Node tests (the owner's word of 2026-10-25: every property tested on one Node fed through its six Links): the horizon (a Node whose x Links stand at the wall holds on that axis, is read by no Link close and births nothing; a body standing at it by a neighbour's shared half credits, PM-S1), the frozen content (a Node at the Link pace 0 is not read and never clicks), the turn (the turned Node ends the interval at its pre-state exchanged and complemented, the exchange an involution), the run back exact through all of it; the step's reach of one Link forward and none back; the files' refusals by name."""

from __future__ import annotations

import copy
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.rule3 import quotient
from event_universe.features import volume
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, zeros
from event_universe.take import frame_nodes
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


def clicks_at(node: Node, at: tuple[int, ...]) -> list[dict[str, Any]]:
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


def test_the_horizon_holds_the_links_at_the_wall_and_the_node_births_nothing() -> None:
    """The horizon: the fed Node's two x Links at the wall (the factor 0), its other four above; no Link close reads the Node (no birth at it, none with it as an end); under PM-S1 the near-massless plane's shared half from a child laid at a neighbour stands at the Node at its own unit, so the near-massless plane's credits are read there (five in 20 intervals under MS-S1's lay at T div 2, four at W = 0; named: the bodies' closing is not the Link close); the run back exact."""
    node = fed_horizon(node_of("world_node.json"), CENTRE)
    factors = node.link_factors()
    assert [int(f[CENTRE]) for f in factors[:2]] == [0, 0]
    assert all(int(f[CENTRE]) > 0 for f in factors[2:])
    fed = copy.deepcopy(node)
    for _ in range(INTERVALS):
        node.step()
    assert [e for e in clicks_at(node, CENTRE) if e["event"] == "birth"] == []
    credits = [(e["sense"], e["line"]) for e in clicks_at(node, CENTRE)]
    assert credits == [(0, 0), (0, 0), (0, 0), (0, 0), (-1, 0)]
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def test_the_frozen_node_is_not_read_and_never_clicks() -> None:
    node = node_of("world_node.json")
    frozen = paces.frozen_content(node.gamma)
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
    den = universe["integers"]["den"]
    refused("keys of no law: control", read_world, dict(world, control={"ride": "symmetric"}), universe)
    refused("keys of no law: detectors", read_world, dict(world, detectors=[[0, 0, 0]]), universe)
    refused(
        "a pair or a wall", read_world, world, dict(universe, rows=universe["rows"] + [{"shape": 1}])
    )
    ints = {**universe["integers"], "link_unit": 16}
    refused("keys of no law: link_unit", read_world, world, dict(universe, integers=ints))
    assert node_of("world_node.json").G == 16  # derived from Gamma 1,000 (K-S1), no key of the file
    rows = universe["rows"]
    for match, change in (
        ("the gap-0 row is the plane", dict(universe, rows=rows + [{"shape": 1, "pair": [1, 2]}])),
        ("one shape-10 row", dict(universe, rows=[r for r in rows if r["shape"] != 10])),
        (
            "the shape-4 row stands at",
            dict(universe, rows=[dict(r, pair=[1, den]) if r["shape"] == 4 else r for r in rows]),
        ),
    ):
        refused(match, Node, change, world)
    for match, change in (
        ("a cube", {"shape": [3, 3, 4]}),
        ("off the board", {"seed": [{"lay": "hole", "at": [3, 0, 0]}]}),
        ("no form of the law", {"seed": [{"lay": "wave", "row": 0}]}),
        ("the plane at the gap 0 alone", {"seed": [{"lay": "sea", "row": 1}]}),
        (
            "half-width 2 or 3",
            {"seed": [{"lay": "at", "row": 1, "centre": [1, 1, 1], "quanta": 1, "width": 4}]},
        ),
    ):
        refused(match, Node, universe, dict(world, **change))
    assert [r.shape for r in node_of("world_node.json").rows_] == [1, 2, 2, 2, 2, 4, 10]


def test_the_frozen_node_rests_and_its_links_stand_at_the_wall_bh_s1() -> None:
    """BH-S1 (the owner's word of 2026-10-25 through the Boss, 6398593790; BH_COMPARISON.md section 6): a Node whose Link pace reads 0 at the interval's start is frozen: no act changes any integer of its state and its proper count rests, no click reads it, every Link with a frozen end is at the wall from both ends; the frozen mask booked in the frame for the run back. The 3-cube centre fed to the frozen content 3,793 at Gamma 1,000 (X 4,268,834,097), 100 intervals: the centre's lines equal to the fed values at every interval, proper[centre] unchanged, the twelve factors 0, 0 clicks at it, the frozen count 1 at every interval, the transient within 128, the run back exact 100 of 100."""
    node = node_of("world_node.json")
    frozen = paces.frozen_content(node.gamma)
    carrier = node.row(CARRIER).lines[0]
    carrier.now[CENTRE] = level_at(node, frozen)
    carrier.before[CENTRE] = carrier.now[CENTRE]
    node.ride_walls()
    assert int(carrier.now[CENTRE]) == 4_268_834_097
    fed = [[int(a[CENTRE]) for a in (line.now, line.before, line.rem)] for line in node.all_lines()]
    proper = int(node.proper[CENTRE])
    kept = copy.deepcopy(node)
    for _ in range(100):
        node.step()
        lines = node.all_lines()
        assert [[int(a[CENTRE]) for a in (line.now, line.before, line.rem)] for line in lines] == fed
        assert int(node.proper[CENTRE]) == proper and not node.turned[CENTRE]
        frozen_now = np.asarray(paces.link_pace_of(node.gamma, node.content()), dtype=object) == 0
        assert int(frozen_now.sum()) == 1 and frozen_now[CENTRE]
        assert all(int(f[CENTRE]) == 0 for f in node.link_factors(None, frozen_now))
        assert all(
            int(node.link_factors(None, frozen_now)[port ^ 1][n]) == 0
            for port, n in enumerate(frame_nodes(node, CENTRE)[1:])
        )
    assert clicks_at(node, CENTRE) == [] and node.max_transient <= 128 and node.census()[1] <= 128
    assert run_back_exact(kept, 100) == 100


def shares_of(node: Node) -> tuple[Any, Any, Any]:
    """The gap-0 line's share in the carrier's unit, and by hand at the frame's weight (X set to Gamma^3 div p_i^2) and at the vacuum's (X set to Gamma)."""
    gap0 = node.row(PLANE, gap=0)
    rule = node.rule(gap0.pair, node.start_content, node.link_factors())
    pace = np.asarray(paces.link_pace_of(node.gamma, node.start_content), dtype=object)
    x, carrier = node.start_x, node.share(gap0.lines, rule)
    node.start_x = np.vectorize(lambda p: quotient(node.gamma**3, p * p), otypes=[object])(pace)
    frame = node.share(gap0.lines, rule)
    node.start_x = zeros(node.shape) + node.gamma
    vacuum, node.start_x = node.share(gap0.lines, rule), x
    return carrier, frame, vacuum


def test_every_count_is_read_in_the_carriers_unit_pm_s1() -> None:
    """PM-S1 (the owner's word of 2026-10-25, 15:18 UTC, through the Boss, 6399410929; PM_COMPARISON.md section 5): the identity Gamma^2 div p_i^2 = X(c) div Gamma at c = 0 to 1,000 by 100 (pm1); on the 3-cube hole the carrier's share within one unit of the frame's at 27 of 27 Nodes at the interval 1 (X / Gamma below 2) and equal to the vacuum's there (X = Gamma); at 20 the vacuum's below the carrier's by X / Gamma (390 thousandths at X / Gamma between 2.36 and 2.94) and the frame's within four per mille; the chiral 5-cube at 60: births 16, body clicks 533, the run back 10 of 10, 98 integers, 115 bits (pm2's 15 and 24 under the lay by the unit; the births and the credits re-cut by MS-S1's lay at T div 2)."""
    node = node_of("world_node.json")
    for c in range(0, 1_001, 100):
        pace = paces.link_pace(node.gamma, c)
        assert quotient(node.gamma * node.gamma, pace * pace) == quotient(level_at(node, c), node.gamma)
    node.step()
    node.step_back()
    carrier, frame, vacuum = shares_of(node)
    assert bool((node.start_x < 2 * node.gamma).all()) and int((abs(carrier - frame) <= 1).sum()) == 27
    assert carrier.tolist() == vacuum.tolist()
    for _ in range(20):
        node.step()
    node.start_content, node.start_x = node.content(), node.row(CARRIER).lines[0].now
    carrier, frame, vacuum = shares_of(node)
    totals = [sum(int(v) for v in a.reshape(-1)) for a in (carrier, frame, vacuum)]
    assert totals[2] * 1000 // totals[0] == 390 and abs(totals[1] - totals[0]) * 1000 <= 4 * totals[0]
    assert (
        2_356
        <= int(node.start_x.min()) * 1000 // node.gamma
        <= int(node.start_x.max()) * 1000 // node.gamma
        <= 2_938
    )
    chiral = node_of("world_chiral.json")
    kept = copy.deepcopy(chiral)
    for _ in range(60):
        chiral.step()
    assert (chiral.counts["births"], chiral.counts["body_clicks"], chiral.census()) == (
        16,
        533,
        (98, 115),
    )
    assert run_back_exact(kept, 10) == 10


def test_the_charge_is_one_e_for_every_row_at_the_lay_ms_s1() -> None:
    """MS-S1 (the owner's word of 2026-10-25, 15:18 UTC, through the Boss, 6399410929; MS_COMPARISON.md section 5, ms2's exact form): the lay's two levels (A, B) with A B = T div 2 from T alone (125 and 144 at T 36,000), the same for every row; the chiral 5-cube at 12 intervals: every child's Wronskian is +-(T div 2) where its plane stood at nothing at its Node (the residue logged), every birth's children at opposite signs with the senses' sum 0, taken at or above booked on every birth, the run back exact."""
    node = node_of("world_chiral.json")
    assert (node.A, node.B, node.A * node.B) == (125, 144, node.T // 2)
    kept = copy.deepcopy(node)
    for _ in range(12):
        node.step()
    births = [e for e in node.log if e["event"] == "birth"]
    assert len(births) >= 8 and all(b["amplitude"] == [125, 144] for b in births)
    for b in births:
        for w, stood in zip(b["W_children"], b["stood"], strict=True):
            assert abs(w) == node.T // 2 or any(stood), (w, stood)
        assert (b["W_children"][0] > 0) != (b["W_children"][1] > 0) and 0 not in b["W_children"]
        assert b["taken"] >= b["booked"] > 0
    assert sum((w > 0) - (w < 0) for b in births for w in b["W_children"]) == 0
    assert sum(1 for b in births for w in b["W_children"] if abs(w) == node.T // 2) >= len(births)
    assert run_back_exact(kept, 12) == 12
