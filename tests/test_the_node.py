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

CENTRE, INTERVALS = (1, 1, 1), 20  # the fed Node, the 3-cube's centre; the run's intervals


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
    """The horizon: the fed Node's two x Links at the wall (the factor 0), its other four above; no Link close reads the Node (no birth at it, none with it as an end); under PM-S1 the near-massless plane's shared half from a child laid at a neighbour stands at the Node at its own unit, so the near-massless plane's credits are read there (twelve in 20 intervals under PL-S1, five at W = 0; under the former write of 2 W after the step twelve with nine at W = 0, the first beat 4 and the rest 1, under MS-S1's lay at T div 2 and CK-S1's beat of the half period with the crossing read even; eleven with eight at W = 0 and every beat 1 under the crossing odd at a touch of zero; named: the bodies' closing is not the Link close); the run back exact."""
    node = fed_horizon(node_of("world_node.json"), CENTRE)
    factors = node.link_factors()
    assert [int(f[CENTRE]) for f in factors[:2]] == [0, 0]
    assert all(int(f[CENTRE]) > 0 for f in factors[2:])
    fed = copy.deepcopy(node)
    for _ in range(INTERVALS):
        node.step()
    assert [e for e in clicks_at(node, CENTRE) if e["event"] == "birth"] == []
    credits = [(e["sense"], e["line"]) for e in clicks_at(node, CENTRE)]
    assert credits == [(0, 0)] * 4 + [(1, 0), (0, 0), (-1, 0), (-1, 0)] + [(1, 0)] * 4
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
    return node_of(name, seed=[x for x in world_of(name)[1]["seed"] if x.get("lay") == "sea"])


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
            "off den's circle",
            dict(
                universe,
                rows=[
                    dict(r, pair=[r["pair"][0] - 1, den])
                    if r["shape"] == 2 and r["pair"][0] != den
                    else r
                    for r in rows
                ],
            ),
        ),
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
    """BH-S1 (the owner's word of 2026-10-25 through the Boss, 6398593790; The-Frozen-Node-Black-Hole_COMPARISON.md section 6): a Node whose Link pace reads 0 at the interval's start is frozen: no act changes any integer of its state and its proper count rests, no click reads it, every Link with a frozen end is at the wall from both ends; the frozen mask booked in the frame for the run back. The 3-cube centre fed to the frozen content 3,793 at Gamma 1,000 (X 4,268,834,097), 100 intervals: the centre's lines equal to the fed values at every interval, proper[centre] unchanged, the twelve factors 0, 0 clicks at it, the frozen count 1 at every interval, the transient within 128, the run back exact 100 of 100."""
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
    """PM-S1 (the owner's word of 2026-10-25, 15:18 UTC, through the Boss, 6399410929; The-Count-In-The-Carriers-Unit_COMPARISON.md section 5): the identity Gamma^2 div p_i^2 = X(c) div Gamma at c = 0 to 1,000 by 100 (pm1); on the 3-cube hole the carrier's share within one unit of the frame's at 27 of 27 Nodes at the interval 1 (X / Gamma below 2) and equal to the vacuum's there (X = Gamma); at 20 the vacuum's below the carrier's by X / Gamma (390 thousandths at X / Gamma between 2.36 and 2.94) and the frame's within four per mille; the chiral 5-cube at 40: births 17, body clicks 1,999 under PL-S1 (1,996 under the former write of 2 W after the step), the run back 10 of 10, 98 integers, 115 bits (at 60 under the crossing odd at a touch of zero and the standing light credited as a body: births 16 and 2,336 credits, pm2's 15 and 24 under the lay by the unit; the births and the credits re-cut by MS-S1's lay at T div 2; the credits 533 under the upward crossing alone, re-cut by CK-S1's beat of the half period; 40 intervals so the test stands under 10 s alone, the Boss's 6402497841)."""
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
    for _ in range(40):
        chiral.step()
    assert (chiral.counts["births"], chiral.counts["body_clicks"], chiral.census()) == (
        17,
        1999,
        (98, 115),
    )
    assert run_back_exact(kept, 10) == 10


def test_the_charge_is_one_e_for_every_row_at_the_lay_ms_s1() -> None:
    """MS-S1 (the owner's word of 2026-10-25, 15:18 UTC, through the Boss, 6399410929; The-Masses-From-The-Clicks_COMPARISON.md section 5, ms2's exact form): the lay's two levels (A, B) with A B = T div 2 from T alone (125 and 144 at T 36,000), the same for every row; the chiral 5-cube at 12 intervals: every child's Wronskian is +-(T div 2) where its plane stood at nothing at its Node (the residue logged), every birth's children at opposite signs with the senses' sum 0, taken at or above booked on every birth, the run back exact."""
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


def test_the_born_pair_meets_at_the_next_close_with_no_current_and_is_refused_by_the_orientation_sl_s1() -> (
    None
):
    """SL-S1 (the Boss's 6399718139, The-Merger-As-The-Birth-Reversed_COMPARISON.md section 4: the generic close, every record's meeting by its own list): the chiral seed on the 3-cube at 30 intervals: every born pair's Link meets at the next close (the two ends holding a whole quantum of the children's record) and reads no current, F = 0 exactly, so the orientation refuses the undoing with no name (4 of 4 born Links under PL-S1; 5 of 5 under the former write of 2 W after the step); the meetings counted as `met`; the run back exact."""
    universe, world = world_of("world_chiral.json")
    lays = [lay for lay in world["seed"] if lay.get("lay") != "at" or all(x < 3 for x in lay["centre"])]
    node = Node(universe, dict(world, shape=[3, 3, 3], intervals=30, seed=lays))
    kept = copy.deepcopy(node)
    for _ in range(30):
        node.step()
    births = [e for e in node.log if e["event"] == "birth"]
    assert len(births) == 4 and node.counts["met"] > len(births)
    for b in births:
        link = {tuple(b["minus"]), tuple(b["plus"])}
        assert any(
            e["event"] == "refused"
            and e["i"] == b["i"] + 1
            and e["cause"] == "orientation"
            and e.get("row") == b["line_pair"]
            and {tuple(e["node"]), tuple(e["link"])} == link
            for e in node.log
        ), b
    assert run_back_exact(kept, 30) == 30


def test_the_merger_takes_one_light_quantum_at_each_end_of_the_pair_and_lays_the_light_sl_s2() -> None:
    """SL-S2 (the Boss's ledger item 10, The-Merger-As-The-Birth-Reversed_COMPARISON.md section 3: the merger is the birth read at -1): the heaviest record's conjugate pair fed at two adjacent Nodes of the bare 5-cube (the + record at M and the - record at P at three times the lay's levels (A, B), one level pair on P's re line for a current across the Link and on two transverse neighbours for a twist) meets as the conjugate pair (the ends' charges opposite) and clicks into light: one birth whose taken row is the heaviest record and whose children are the gap-0 row, each child's wall one light quantum to the rounding paid by one exact take at its own end from the taken row's line, the gap-0 row standing at a whole quantum at each end where nothing stood, the children's charges -+(T div 2) summing to 0 and the gap-0 row's charge 0 over the board, taken at or above booked, the merger at the first close with no stop before it (CS4-S2: each end's take on the heavy row's second line, 3 B against 0 the farthest, logged per take as `taken_line` [1, 1]; under the former first line's take the stop refused both ends by name before the merger paid); the run back exact."""
    node = node_of("world_node.json", shape=[5, 5, 5], seed=[])
    a, b, k = node.A, node.B, 3
    heavy = max(range(len(node.records())), key=lambda r: node.records()[r].gap or 0)
    light = node.row(PLANE, gap=0)
    gap0, unit = node.records().index(light), node.unit_gap0
    m, p = (1, 1, 1), (2, 1, 1)
    feed = (
        (m, (k * a, 0, 0, k * b)),
        (p, (k * a, b, 0, -k * b)),
        ((1, 2, 1), (a, b, 0, 0)),
        ((2, 1, 2), (b, a, 0, 0)),
    )
    for at, levels in feed:
        node.lay(heavy, at, levels)
    kept = copy.deepcopy(node)
    for _ in range(INTERVALS):
        node.step()
    births = [e for e in node.log if e["event"] == "birth"]
    mergers = [e for e in births if e["taken_row"] == heavy]
    assert len(mergers) == 1 and mergers[0]["line_pair"] == gap0 and births[0] is mergers[0]
    (merger,) = mergers
    assert {tuple(merger["minus"]), tuple(merger["plus"])} == {m, p}
    assert [tuple(t["node"]) for t in merger["takes"]] == [tuple(merger["minus"]), tuple(merger["plus"])]
    assert all(unit <= t["booked"] <= t["taken"] and t["booked"] < 2 * unit for t in merger["takes"])
    assert merger["taken"] >= merger["booked"] == sum(t["booked"] for t in merger["takes"])
    assert merger["W_children"] == [-(node.T // 2), node.T // 2] and merger["stood"] == [[0] * 4] * 2
    refusals = [
        e
        for e in node.log
        if e["event"] == "refused" and e.get("row") == heavy and e["i"] <= merger["i"]
    ]
    assert merger["i"] == 1 and refusals == [] and merger["taken_line"] == [1, 1]
    probe = copy.deepcopy(kept)
    for _ in range(merger["i"]):
        probe.step()
    re, im = probe.row(PLANE, gap=0).lines
    assert int((re.now * im.before - im.now * re.before).sum()) == 0  # the light's charge at the merger
    assert run_back_exact(kept, INTERVALS) == INTERVALS


def test_the_swap_keeps_the_charge_of_every_plane_at_every_turned_node_ws() -> None:
    """WS (the Boss's 6400357538, The-Swap-Keeps-The-Charge_VERDICT.md section 4, ws1's exchange_read as a test under 15 s): the swap at the top is the conjugation composed with the exchange of the two levels, and W = re_now im_before - im_now re_before, odd under each, is even under the two: at every turned Node and every plane (the gap-0 plane with the gapped), W after the swap equals W of the held pre-state exactly (read by a Node whose click reads before it lays; the acts untouched), kept = sites, negated 0, changed 0; on the Boss's 3-cube (the sea and one quantum of row 1 at the centre, the first turn at 42 under EQ-S1, the centre's body laying back 12 of its 39 credits where nothing arrives; 35 with the take standing under CK-S1's crossing read even, 37 under the crossing odd at a touch of zero, 42 before CK-S1's credits) 296 of 296 sites by 60 (74 turned Nodes; 324 and 81 with the take standing), every W 0 there; on the chiral 5-cube at 20 intervals 2,156 of 2,156 sites (539 turned Nodes by the four planes), 625 of them with W not 0 (2,160 sites by 540 turned Nodes and 695 under the former write of 2 W after the step; 2,124 and 672 under the odd crossing; 2,120 and 668 under the upward crossing alone; at 60 the probe read 2,500 of 2,500, 908 not 0, against ws1's 1,863 on the former head)."""
    from event_universe.links import wronskian

    class Reading(Node):
        wronskians: dict[str, int] = {}

        def click(self, *args: Any, **keys: Any) -> Any:
            where = list(zip(*np.nonzero(self.turned), strict=True))
            for r, row, hrow in zip(self.rows_, self.rows(), args[1], strict=True):
                if r.shape == PLANE:
                    pre, after = wronskian(*hrow), wronskian(*row)
                    for at in where:
                        wp, wa = int(pre[at]), int(after[at])
                        key = "kept" if wa == wp else "negated" if wa == -wp else "changed"
                        for k in ("sites", key, "nonzero" if wp else "zero"):
                            self.wronskians[k] = self.wronskians.get(k, 0) + 1
            return super().click(*args, **keys)

    universe, world = world_of("world_node.json")
    one = {"lay": "at", "row": 1, "centre": [1, 1, 1], "quanta": 1, "width": 2, "sense": 1}
    found = []
    for node, n in (
        (Reading(universe, dict(world, seed=[world["seed"][0], one])), 60),
        (Reading(*world_of("world_chiral.json")), 20),
    ):
        node.wronskians = {}
        for _ in range(n):
            node.step()
        assert node.wronskians["kept"] == node.wronskians["sites"] > 0
        assert not {"negated", "changed"} & node.wronskians.keys()
        found.append(node.wronskians)
    assert [f["sites"] for f in found] == [296, 2156] and found[1]["nonzero"] == 625
    assert "nonzero" not in found[0]


def test_the_bodies_closing_clicks_on_the_zero_crossing_in_either_direction_ck_s1() -> None:
    """CK-S1 (the owner's word of 2026-10-25, 17:57 UTC, through the Boss, 6401141446; ck1's REPORT.md section 4): a record standing at a whole quantum of its own unit through one period of its re line's zero crossings, in either direction, clicks, the beat the half period, the crossing read even under the negation of the line (the two levels' product below 0 or exactly one of them 0, a touch of zero a crossing from either side alike; the Boss's 6402516165): at one Node a plane's re line fed at rest over the period 8 touching zero (2, 1, 0, -1, -2, -1, 0, 1) and over the period 6 (2, 1, -1, -2, -1, 1), each with its negation, gives the counters crossed and beats equal step for step, the period 6 the beat 3; on the chiral 5-cube at 20 intervals every plane credit's beat is the interval count between the two latest zero crossings of the record's re line at its Node in either direction, read by hand from the lines by the even form, 825 credits with 128 of them on a downward crossing under PL-S1 (819 and 177 under the former write of 2 W after the step; 536 and 50 under the form `b < 0 <= n or n < 0 <= b`, odd where exactly one level is 0; 115 credits under the upward crossing alone); the run back exact."""
    from event_universe.bodies import bodies

    node = node_of("world_node.json")
    rec, count = 1, len(node.records())
    re = node.records()[rec].lines[0]
    nothing, still = [zeros(node.shape) for _ in range(count)], np.zeros(node.shape, dtype=bool)
    rule = node.rule_of(node.row(PLANE, gap=0), node.content(), node.link_factors())
    for period in ((2, 1, 0, -1, -2, -1, 0, 1), (2, 1, -1, -2, -1, 1)):
        counters = []
        for sign in (1, -1):
            node.standing, node.crossed, node.beats = [
                [zeros(node.shape) for _ in range(count)] for _ in range(3)
            ]
            levels = [sign * v for v in period * 3]
            for before, now in zip(levels, levels[1:], strict=False):
                re.before[CENTRE], re.now[CENTRE] = before, now
                bodies(node, [r.lines for r in node.records()], nothing, set(), still, rule)
                counters.append((sign, int(node.crossed[rec][CENTRE]), int(node.beats[rec][CENTRE])))
        assert [c[1:] for c in counters if c[0] == 1] == [c[1:] for c in counters if c[0] == -1]
    assert counters[-1][2] == 3 and node.counts["body_clicks"] == 0
    node = node_of("world_chiral.json")
    kept = copy.deepcopy(node)
    crossings: dict[tuple[int, tuple[int, ...]], list[tuple[int, bool]]] = {}
    for t in range(1, INTERVALS + 1):
        node.step()
        for r, row in enumerate(node.records()):
            if row.shape == PLANE:
                before, now = row.lines[0].before, row.lines[0].now
                crossed = (before * now < 0) | ((before == 0) != (now == 0))
                for where in zip(*np.nonzero(crossed), strict=True):
                    at = tuple(int(x) for x in where)
                    crossings.setdefault((r, at), []).append((t, int(now[at]) >= 0))
    credits = [
        e for e in node.log if e["event"] == "credit" and node.records()[e["line"]].shape == PLANE
    ]
    upward = []
    for e in credits:
        seen = [c for c in crossings[(e["line"], tuple(e["node"]))] if c[0] <= e["i"]]
        assert e["beat"] == seen[-1][0] - seen[-2][0], e
        upward.append(seen[-1][1])
    assert (len(credits), sum(upward)) == (825, 697)
    assert run_back_exact(kept, INTERVALS) == INTERVALS


def test_the_take_moves_the_line_farthest_from_its_before_and_logs_it_per_take_cs4_s2() -> None:
    """CS4-S2 (the owner's word of 2026-10-25, 22:50 UTC, "all of them", through the Boss; cs4's REPORT.md sections 1.2, 1.5 and 4, The-Handed-Seed-And-Births_COMPARISON.md's finding (a) and cs5's mend, the line logged PER TAKE; the test under 15 s): the exact take moves the taken record's line whose level now stands farthest from its before (the largest now^2 - before^2, the first where equal), the line logged as `taken_line` on every birth, credit and merger take, unclick restoring that line. The pair's 3-cube at 20 intervals beside its image with the light turned a quarter at the seed ((re, im) -> (-im, re): the light on its second line, the first at 0): the two boards' X equal at every Node at 20 of 20 intervals and the 81 credits equal take for take in their numbers, every take on the first line on the board and on the second on the image, where the former act (the first line's take) is the stop by name (fall_of (None, 0) on a line at 0), the run back exact 20 of 20 through the takes on the second line; SL-S2's merger board (the heaviest record's conjugate pair at two adjacent Nodes of the bare 5-cube) at 20: the merger at the first close with no stop before it (the heavy row's second line, 3 B against 0, the farthest at both ends: its two takes on the second line; under the former act the first line's fall came short and the stop refused both ends before the merger paid), the ten light births after it taking the light's second line but one (at 19, where the first line's gap is the larger), 74 credits, each of the 87 takes' lines re-derived by hand from the Node's levels after the close (the other line untouched by the take, the taken line as the take found it), 66 of 87 on a line other than the first (0 under the former act; under the sign row's former write of 2 W after the step, before PL-S1, the board read 9 births every one on the second line, 318 takes with 219 on it and 308 credits), the run back exact."""
    pair, image = node_of("world_pair_3.json"), node_of("world_pair_3.json")
    re, im = image.row(PLANE, gap=0).lines
    im.now[...], im.before[...], re.now[...], re.before[...] = re.now.copy(), re.before.copy(), 0, 0
    kept = copy.deepcopy(image)
    for _ in range(INTERVALS):
        pair.step()
        image.step()
        assert (pair.row(CARRIER).lines[0].now == image.row(CARRIER).lines[0].now).all()
    credits = [
        [
            (e["i"], e["node"], e["taken"], e["levels"], e["taker"], e["taken_line"])
            for e in n.log
            if e["event"] == "credit"
        ]
        for n in (pair, image)
    ]
    assert len(credits[0]) == 81 and [c[:5] for c in credits[0]] == [c[:5] for c in credits[1]]
    assert {c[5] for c in credits[0]} == {0} and {c[5] for c in credits[1]} == {1}
    assert all(int(re.now[tuple(c[1])]) == int(re.before[tuple(c[1])]) for c in credits[1])
    assert run_back_exact(kept, INTERVALS) == INTERVALS
    node = node_of("world_node.json", shape=[5, 5, 5], seed=[])
    a, b, k = node.A, node.B, 3
    heavy = max(range(len(node.records())), key=lambda r: node.records()[r].gap or 0)
    for at, levels in (
        ((1, 1, 1), (k * a, 0, 0, k * b)),
        ((2, 1, 1), (k * a, b, 0, -k * b)),
        ((1, 2, 1), (a, b, 0, 0)),
        ((2, 1, 2), (b, a, 0, 0)),
    ):
        node.lay(heavy, at, levels)
    kept, lines_taken = copy.deepcopy(node), []
    for _ in range(INTERVALS):
        seen = len(node.log)
        node.step()
        for e in node.log[seen:]:
            if e["event"] not in ("birth", "credit"):
                continue
            lines = node.records()[
                e.get("taken_row", node.records().index(node.row(PLANE, gap=0)))
            ].lines
            for t in e.get("takes", [e]):
                at, k = tuple(t["node"]), t["taken_line"]
                gaps = [int(line.now[at]) ** 2 - int(line.before[at]) ** 2 for line in lines]
                gaps[k] = t["taken_now_was"] ** 2 - t["taker"][1] ** 2
                assert gaps.index(max(gaps)) == k and t["taker"][0] == t["taken_now_was"]
                lines_taken.append(k)
    births = [e for e in node.log if e["event"] == "birth"]
    assert births[0]["taken_row"] == heavy and births[0]["taken_line"] == [1, 1]
    on_first = [
        (e["i"], t["taken_line"]) for e in births for t in e.get("takes", [e]) if not t["taken_line"]
    ]
    assert on_first == [(19, 0)] and len(births) == 11
    assert (len(lines_taken), sum(lines_taken), node.counts["body_clicks"]) == (87, 66, 74)
    assert run_back_exact(kept, INTERVALS) == INTERVALS
