"""The one board test: the 48 (the board run from a seed and from each of its 48 images, the signed permutations of the axes about the origin; the births and the carrier's and the gap-0 line's levels compared through the image, the 24 rotations alike under the bodies' closing with its crossing read even, the 24 reflections apart under the default: A2's standing item, named), the run back exact through births and turns, the chiral seed's births with both hands and the charge summed to 0."""

from __future__ import annotations

import copy
import itertools
import json
from typing import Any

import numpy as np

from event_universe import gates as table
from event_universe import run as writer
from event_universe.core.ports import PORTS
from event_universe.links import row_current
from event_universe.node import Node
from event_universe.rows import CARRIER
from tests.laws import node_of, refused, run_back_exact, state_of, world_of

CUBE, INTERVALS, GROUPS, ALIKE = 5, 20, 4, (6, 6, 6, 6)  # rotations alike per part (CK-S1 even)
COUNTED = ("births", "laid_back", "refused_stop")  # the counts the EQ-S1 test reads per world
IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]


def image(m: Any, node: tuple[int, ...], cube: int) -> tuple[int, ...]:
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def births_of(node: Node) -> list[tuple[Any, ...]]:
    return sorted(
        (e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"]))
        for e in node.log
        if e["event"] == "birth"
    )


def mapped(births: list[tuple[Any, ...]], m: Any, cube: int, exchanged: bool) -> list[tuple[Any, ...]]:
    found = [
        (i, image(m, at, cube), s, image(m, mi, cube), image(m, pl, cube)) for i, at, s, mi, pl in births
    ]
    return sorted((i, at, s, pl, mi) if exchanged else (i, at, s, mi, pl) for i, at, s, mi, pl in found)


def world_image(world: dict[str, Any], m: Any, cube: int) -> dict[str, Any]:
    found = dict(world, shape=[cube] * 3, seed=[dict(lay) for lay in world["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, tuple(lay[key]), cube))
    return found


def run(universe: dict[str, Any], world: dict[str, Any]) -> Node:
    node = Node(universe, world)
    for _ in range(INTERVALS):
        node.step()
    return node


def same_rows(base: Node, other: Node, m: Any) -> bool:
    for line_b, line_o in (
        (base.row(CARRIER).lines[0], other.row(CARRIER).lines[0]),
        (base.emitter().lines[0], other.emitter().lines[0]),
    ):
        for at in np.ndindex(CUBE, CUBE, CUBE):
            there = image(m, at, CUBE)
            if int(line_b.now[at]) != int(line_o.now[there]) or int(line_b.before[at]) != int(
                line_o.before[there]
            ):
                return False
    return True


def images_hold(group: int) -> None:
    """The images of one part of the 48 (every fourth from the group's first): a rotation that negates no axis runs alike the seed through the image (the rows and the births), a rotation negating the y or the z axis runs alike too once the bodies' closing reads the crossing even (24 of 24 at 20 intervals on the hole seed, 56 credits and 16 births under PL-S1, 209 credits and 20 births under A48-S1 (05cca50, the read of the remainder in the laid frame, reverted for the tie of the sign row's write remainder and the births' seed), 12 births under the former write of 2 W after the step; 6 of 24 under the crossing odd at a touch of zero, the form `b < 0 <= n or n < 0 <= b`, which parted a negated line at its touch of zero: A2's standing item, 6 of 24 under MS-S1 against 24 before it, read now to the odd crossing), every reflection apart; the counts held by name so that an image coming alike or parting is read."""
    universe, world = world_of("world_hole.json")
    base = run(universe, world_image(world, np.eye(3, dtype=int), CUBE))
    births = births_of(base)
    assert len(births) > 0
    alike = {True: 0, False: 0}
    for m in IMAGES[group::GROUPS]:
        other = run(universe, world_image(world, m, CUBE))
        reflection = int(round(np.linalg.det(m))) == -1
        same = same_rows(base, other, m) and births_of(other) == mapped(births, m, CUBE, reflection)
        alike[reflection] += same
    assert alike[True] == 0 and alike[False] == ALIKE[group]


def test_the_run_back_is_exact_through_births_and_turns() -> None:
    node = node_of("world_hole.json")
    assert run_back_exact(node, 40) == 40
    for _ in range(40):
        node.step()
    assert node.counts["births"] > 0 and node.counts["turns"] > 0


def test_the_chiral_seed_births_both_hands_and_the_charge_sums_to_zero() -> None:
    node = node_of("world_chiral.json")
    for _ in range(60):
        node.step()
    births = [e for e in node.log if e["event"] == "birth"]
    assert len(births) >= 8
    signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    assert sum(signs) == 0 and 0 not in signs
    assert all(b["taken"] >= b["booked"] for b in births)
    hands = {1 if tuple(b["plus"]) > tuple(b["minus"]) else -1 for b in births}
    assert hands == {1, -1}


def test_the_first_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged() -> None:
    images_hold(0)


def test_the_second_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged() -> None:
    images_hold(1)


def test_the_third_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged() -> None:
    images_hold(2)


def test_the_fourth_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged() -> None:
    images_hold(3)


def test_the_uniform_pair_at_every_node_returns_with_the_whole_board_turning_at_once_ma() -> None:
    """MA-S1 by the fourth form of the file (the owner's word of 17:57 through the Boss, 6401141446; ma2's spelling, the Boss's 6401095909) with EQ-S1 in cs7's letter (6403341352): the pair of the heavy row laid at every Node of the 3-cube at one quantum (tests/worlds/world_pair_3.json, {"lay": "sea", "row": 2, "quanta": 1, "sense": 0}: the amplitude 96, ma1's, re_now 192 the two senses summed, W 0) keeps every Node alike to the integer (400 of 400), turns every Node at once at both tops (27 at 85, ma1's, and at 252), births nothing, and returns to Gamma EXACTLY at 169 and 334 (ma1's 168 / 169 and 333 / 334) with a body credited at every Node in every cycle: 297 credits, 27 at each of 4, 6 and 8 and after each return, every one laid back (nothing arrives at a Node of the board alike); before EQ-S1 the take stood and the bottoms read 953 at 171 and 888 at 342 with 351 credits and the second top at 255 (992 and 966 with 162 credits under the upward crossing alone); the run back exact 10 of 10."""
    node = node_of("world_pair_3.json")
    assert int(node.by_index[2].lines[0].now.min()) == int(node.by_index[2].lines[0].now.max()) == 192
    kept = copy.deepcopy(node)
    alike, tops, means = 0, 0, []
    for _ in range(400):
        node.step()
        x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
        alike += min(x) == max(x)
        means.append(sum(x) // len(x))
        if node.turned.any():
            tops += 1
            assert (node.interval, int(node.turned.sum())) in ((85, 27), (252, 27))
    bottoms = [
        (k + 1, means[k]) for k in range(1, 399) if means[k] <= means[k - 1] and means[k] < means[k + 1]
    ]
    credits = [e for e in node.log if e["event"] == "credit"]
    assert (alike, tops, node.counts["births"], len(credits)) == (400, 2, 0, 297)
    assert bottoms == [(169, 1000), (334, 1000)] and sum(1 for c in credits if c["i"] == 4) == 27
    assert node.counts["laid_back"] == 297
    assert run_back_exact(kept, 10) == 10


def test_the_plasma_retraces_bit_for_bit_and_returns_to_gamma_exactly_pl_s1() -> None:
    """PL-S1 (the owner's word of 2026-10-25, 22:50 UTC, through the Boss, 6404425423; pl1's test_pl1.py and pl2's test_pl2.py brought to the engine's own path): nature's plasma on the 3-cube (tests/worlds/world_plasma_3.json, the heavy row at +1 and the light row at -1 at every Node) to 170 tops at 84 with 27 turning, the fall's state at top + k the exchange of the rise's at top - 1 - k in every level and remainder at 83 of 83 k (before PL-S1 the sign row's time line's write remainder parted at k = 1 by 2 (W(83) - W(82)) = 32, its level at k = 8 and X at k = 9), X = Gamma at every Node at 166 and 167 and nowhere else (the bottom 1,000 at 167; 939 before), 162 credits with 135 in the rise, every one laid back (135 before), births 0, the emission laid 0, the run back exact 10 of 10 through the top (170 back to 80), 98 integers, the bits within 128."""
    node = node_of("world_plasma_3.json")
    states, kept, exact, tops = [], [], [], []
    for _ in range(170):
        states.append([[line.copy() for line in row] for row in node.rows()])
        if 80 <= node.interval < 90:
            kept.append(state_of(node))
        node.step()
        x = node.row(CARRIER).lines[0].now
        exact.append(int(x.min()) == int(x.max()) == node.gamma)
        if node.turned.any():
            tops.append((node.interval, int(node.turned.sum())))
    states.append([[line.copy() for line in row] for row in node.rows()])
    credits = [e for e in node.log if e["event"] == "credit"]
    top = tops[0][0]
    assert tops[0] == (84, 27) and [i + 1 for i, e in enumerate(exact) if e] == [166, 167]
    laid_back = sum(1 for c in credits if "laid_back" in c)
    assert (len(credits), laid_back, sum(1 for c in credits if c["i"] < top)) == (162, 162, 135)
    assert node.counts["births"] == node.counts["laid"] == 0
    assert node.census()[0] == 98 and node.census()[1] <= 128
    for _ in range(80):
        node.step_back()
    assert sum(state_of(node) == kept[9 - k] for k in range(10) if not node.step_back()) == 10
    everywhere = np.ones(node.shape, dtype=bool)

    def text(rows: list[list[Any]], exchanged: bool) -> bytes:
        node.set_rows([[line.copy() for line in row] for row in rows])
        if exchanged:
            node.exchange(everywhere, rows)
        return node.state_bytes()

    assert (
        sum(text(states[top + k], False) == text(states[top - 1 - k], True) for k in range(1, top)) == 83
    )


def test_the_body_at_rest_lays_back_what_it_takes_and_the_light_stays_whole_eq_s1() -> None:
    """EQ-S1 in cs7's letter (CS7-S1; the owner's word of 2026-10-25, 17:57 UTC, through the Boss's recommendation, 6402908585 and 6403341352; eq1's test_eq1_equilibrium.py and eq2's test_eq2.py re-read on the engine's own path): on the uniform pair of the 3-cube the gap-0 row's current across the six Links sums to 0 at every Node at every interval's start (nothing arrives), every credit carries laid_back equal to its levels with its momentum booked 0 and leaves the gap-0 line's level at its Node as the take found it (the light whole), the credits 27 at each of 4, 6 and 8 (81 in 20 intervals; before EQ-S1 the board, its light taken, credited at 10 and 13 too), no refusal of the stop, the run back exact 10 of 10; on the hole seed of the 5-cube at 20 every credit stands at a Node whose net current is not 0 (something arrives), none laid back, 56 credits and 16 births under PL-S1 (209 credits and 20 births under A48-S1 (05cca50, the read of the remainder in the laid frame, reverted for the tie of the sign row's write remainder and the births' seed); 12 births with the same 56 credits under the former write of 2 W after the step, as before EQ-S1: the records where light flows bit for bit under it), the run back exact."""
    found = {}
    for world, quiet in (("world_pair_3.json", True), ("world_hole.json", False)):
        node, kept = node_of(world), node_of(world)
        by_interval: dict[int, int] = {}
        for _ in range(INTERVALS):
            lines = node.emitter().lines
            net = sum((row_current(lines, port) for port in range(PORTS)), start=0)
            seen = len(node.log)
            node.step()
            credits = [e for e in node.log[seen:] if e["event"] == "credit"]
            for c in credits:
                at = tuple(c["node"])
                assert (int(net[at]) == 0) == ("laid_back" in c) == quiet
                if quiet:
                    assert c["laid_back"] == c["levels"] > 0 and c["dP_take"] == [0, 0, 0]
                    assert int(node.emitter().lines[0].now[at]) == c["taken_now_was"]
            by_interval[node.interval] = len(credits)
        counts = node.counts
        found[world] = ({i: n for i, n in by_interval.items() if n}, *(counts[k] for k in COUNTED))
        assert run_back_exact(kept, 10) == 10
    assert found["world_pair_3.json"] == ({4: 27, 6: 27, 8: 27}, 0, 81, 0)
    assert found["world_hole.json"][1:3] == (16, 0) and sum(found["world_hole.json"][0].values()) == 56


def test_the_bare_sea_returns_exactly_with_the_whole_board_turning_at_once_bb() -> None:
    """BB-S1 and MA-S1 read by gate 1 from the Node lines (the Boss's 6400540638 and 6400767119 (2); The-Uniform-Board-Returns_COMPARISON.md section 4): the sea alone on the 3-cube to 240 (tests/worlds/world_sea_3.json, the Universe seed that returns) tops at 58 and 173 with all 27 Nodes turning at once, returns to X = Gamma at every Node exactly at 115 and 230 (the bottoms), the bangs numbered 1, 116 and 231 with no birth and no credit between them; the record read through the table, gate 1 SHOWN, gate 46 NOT SHOWN (no body in the later cycle), the run back exact 10 of 10."""
    universe, world = world_of("world_sea_3.json")
    found = json.loads(json.dumps(writer.record(universe, world, 10, lambda line: None)))
    out = table.gates(found)
    bang = json.loads(json.dumps(out["1 recurring bangs"]))
    assert bang["tops with every Node turning at once (interval)"] == [58, 173]
    assert bang["bottoms (interval, mean X, at Gamma at every Node)"] == [
        [115, 1000, True],
        [230, 1000, True],
    ]
    assert bang["bangs numbered (the interval each begins)"] == [1, 116, 231]
    assert bang["births and body credits between the bangs"] == [[0, 0], [0, 0], [0, 0]]
    assert bang["verdict"].startswith("SHOWN: 2 exact returns")
    assert out["46 the bangs recurring with the same gates"]["verdict"].startswith("NOT SHOWN")
    assert found["run_back"] == {"intervals": 10, "exact": 10} and found["counts"]["births"] == "0"
    universe, world = world_of("world_pair_3.json")
    tied = table.gates(
        json.loads(json.dumps(writer.record(universe, dict(world, intervals=12), 0, lambda line: None)))
    )
    assert len(tied["2 the Links lengthening in the clicks"]["at"]) == 3  # every Node's spacing ties


def test_the_moving_lay_runs_at_its_momentum_over_twice_its_share_mv() -> None:
    """MV-S1 to MV-S3 (the Boss's ledger item 7, The-Moving-Lay-With-A-Wave-Number_COMPARISON.md's section for David): the heavy row's pair of 3 quanta laid under the sea at the centre of the 9-cube with the wave number h = den div 2 along x (k = pi / 3 exactly): W 0 at every Node of every lay, the share centroid's step at each of the first four closes (the paces still the vacuum's, before the sea deepens the board) within 40 milli-Links per interval of (1000 P) div (2 E) by cross multiplication (P_x = 2 num SUM_i (now_(i+x) before_i - now_i before_(i+x)) over the two lines, E the share summed), a top of 3 Nodes above the width-2 value, wave 0 hash-equal to no wave, the refusals by name, the run back exact through 10."""
    universe, world = world_of("world_packet.json")
    den, milli = int(universe["integers"]["den"]), 1000
    packet = {"lay": "at", "row": 2, "centre": [4, 4, 4], "width": 2, "quanta": 3}
    moving = dict(packet, wave=[den // 2, 0, 0])

    def ints(a: Any) -> list[int]:
        return [int(x) for x in a.reshape(-1)]

    def laid(lay: dict[str, Any]) -> tuple[Node, int]:
        node = Node(universe, dict(world, seed=[{"lay": "sea", "row": 0}, lay]))
        row = node.by_index[2]
        re, im = row.lines
        assert row.pair is not None and not any(ints(re.now * im.before - im.now * re.before))
        energy = sum(
            ints(node.share(row.lines, node.rule(row.pair, node.content(), node.link_factors())))
        )
        momentum = sum(
            sum(
                ints(
                    np.roll(line.now, -1, axis=0) * line.before
                    - line.now * np.roll(line.before, -1, axis=0)
                )
            )
            for line in row.lines
        )
        return node, milli * 2 * row.pair[0] * momentum // (2 * energy)

    def centroid(node: Node) -> tuple[int, int]:
        row = node.by_index[2]
        assert row.pair is not None
        share = node.share(row.lines, node.rule(row.pair, node.content(), node.link_factors()))
        return sum(ints(share * np.indices(node.shape)[0])), sum(ints(share))

    node, law = laid(moving)
    assert laid(dict(moving, top=3))[1] > law > 0
    kept = copy.deepcopy(node)
    before = centroid(node)
    for _ in range(4):
        node.step()
        after = centroid(node)
        step, scale = milli * (after[0] * before[1] - before[0] * after[1]), after[1] * before[1]
        assert abs(step - law * scale) <= 40 * scale, (law, step // scale)
        before = after
    assert node.counts["births"] == 0 and run_back_exact(kept, 10) == 10
    rest, zero = laid(packet)[0], laid(dict(packet, wave=[0, 0, 0]))[0]
    for _ in range(2):
        assert rest.state_hash() == zero.state_hash()
        rest.step()
        zero.step()
    for bad, match in (
        (dict(moving, wave=[den + 1, 0, 0]), "beyond the band's edge"),
        (dict(moving, row=0, wave=[0, 0, 0]), "the gap-0 row at the wave 0"),
        (dict(moving, top=9), "a top is an odd count"),
        (dict(moving, interval=3), "a field of no form"),
    ):
        refused(match, Node, universe, dict(world, seed=[bad]))


def test_the_moving_lay_is_carried_by_the_48_with_its_centre_and_wave_mv() -> None:
    """MV-S1's 48 (vf5's item (a), the Boss's 6401916517; The-Moving-Lay-With-A-Wave-Number_COMPARISON.md's spec: the 48 with the centre and the wave transformed): the heavy row's pair of 3 quanta laid under the sea on the 5-cube at the wave [den div 2, den div 3, 0] and run two intervals, against the 48 worlds whose centre and wave are the image's: carried back by the image's inverse, the carrier's X and the row's re lines equal bit for bit, the im lines equal under a rotation and negated under a reflection (the senses exchanged), 24 and 24, 0 apart."""
    universe, world = world_of("world_packet.json")
    den, cube, centre = int(universe["integers"]["den"]), 5, [2, 2, 1]
    wave = [den // 2, den // 3, 0]

    def moved(g: tuple[tuple[int, ...], tuple[int, ...]], x: list[int], wrap: int) -> list[int]:
        pi, s = g
        y = [0, 0, 0]
        for a in range(3):
            y[pi[a]] = (s[a] * x[a]) % wrap if wrap else s[a] * x[a]
        return y

    def run(g: tuple[tuple[int, ...], tuple[int, ...]]) -> Node:
        lay = {
            "lay": "at",
            "row": 2,
            "centre": moved(g, centre, cube),
            "width": 2,
            "quanta": 3,
            "wave": moved(g, wave, 0),
        }
        node = Node(
            universe, dict(world, shape=[cube] * 3, intervals=2, seed=[{"lay": "sea", "row": 0}, lay])
        )
        node.step()
        node.step()
        return node

    def back(a: Any, g: tuple[tuple[int, ...], tuple[int, ...]]) -> Any:
        out = np.empty_like(a)
        for idx in np.ndindex(*a.shape):
            out[idx] = a[tuple(moved(g, list(idx), cube))]
        return out

    base = run(((0, 1, 2), (1, 1, 1)))
    alike = {1: 0, -1: 0}
    for pi in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            g = (pi, s)
            det = (
                (-1) ** sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
                * s[0]
                * s[1]
                * s[2]
            )
            img = run(g)
            same = bool((back(img.row(CARRIER).lines[0].now, g) == base.row(CARRIER).lines[0].now).all())
            for (lb, li), sign in zip(
                zip(base.by_index[2].lines, img.by_index[2].lines, strict=True), (1, det), strict=True
            ):
                same = same and bool(
                    (back(li.now, g) == sign * lb.now).all()
                    and (back(li.before, g) == sign * lb.before).all()
                )
            alike[det] += same
    assert alike == {1: 24, -1: 24}


def test_one_pair_in_several_rows_births_the_conjugate_pair_at_every_node_cs5_s2() -> None:
    """CS5-S2 (the owner's word of 2026-10-25, 22:50 UTC, "all of them", through the Boss, 6404425423; cs5's REPORT.md section 4 and cs7's section 3.3: the file universe_ga2 and the `wave` lay of cs3's cycle form in cs5's and cs7's spelling): the universe file names one pair in two rows (tests/worlds/universe_ga2.json, 115,762,739,551,980 twice) and the loader admits it as written, two records with the same numbers and one unit, the decoder one name for both; the 4-cube with no sea under the cycle lay at 5 quanta (tests/worlds/world_ga2.json: the amplitude 300 at every Node, logged with its digits and the sense 1) births 0 at i 1 (64 lay refusals, the light's own row drawn where it stands; cs5's hh3 read 64 crowd refusals there) and 64 at i 2 at 64 of 64 Nodes, every Node one child of the row 0 and one of the row 1 at W -18,000 / +18,000 (the conjugate pair of the plane at the Node, the crowd refusing nothing: two records, not one), taken at or above booked on 64 of 64, X 1,050 at 64 of 64 at i 2 and 1,880 at i 10 (cs5's and cs7's numbers to the integer), 256 credits by 20 (128 at i 8 and 128 at i 10, every one laid back under EQ-S1; cs7 read 128 at i 10 alone on its head before CK-S1's crossing in either direction) every one decoded from the clicks to the one species gapped 0 whichever row it stands on (256 of 256 right, 128 tracks right), the run back exact 20 of 20, 89 integers, 115 bits; the lay refused by name off the plane at the gap 0, with a field of no form, off Z_4, off the mirror 0 and 1, on a cube not a multiple of 4; the mirror 1 mirrors the remainder on the 32 negated Nodes of each line and leaves the levels; under A48-S1 (05cca50, the read of the remainder in the laid frame, reverted for the tie of the sign row's write remainder and the births' seed) the cycle board birthed NOTHING: the draw at the first close refused as the origin at 64 reads (every folded remainder at the lay's half on the board alike), 1,216 lays refused after it, no credit, no turn by 20, Gamma exactly at 198 and 199 to 230: the pattern's digits were fitted to this read, named for the Boss and the hand on the births' seed."""
    universe, world = world_of("world_ga2.json")
    seed = world["seed"][0]
    found = json.loads(
        json.dumps(writer.record(universe, dict(world, intervals=20), 20, lambda line: None))
    )
    assert found["planes"][0] == found["planes"][1] != found["planes"][2]
    lay = [e for e in found["log"] if e["event"] == "lay"]
    assert len(lay) == 1 and (lay[0]["amplitude"], lay[0]["p1"], lay[0]["sense"]) == (300, seed["p1"], 1)
    births = [e for e in found["log"] if e["event"] == "birth"]
    children: dict[tuple[int, ...], list[int]] = {}
    for b in births:
        for end in ("minus", "plus"):
            children.setdefault(tuple(b[end]), []).append(b["line_pair"])
    assert len(births) == 64 and {b["i"] for b in births} == {2} and len(children) == 64
    assert all(sorted(rows) == [0, 1] for rows in children.values())
    assert {tuple(b["W_children"]) for b in births} == {(-18000, 18000)}
    assert all(b["taken"] >= b["booked"] for b in births)
    first = [e for e in found["log"] if e["event"] == "refused" and e["i"] == 1 and e["cause"] == "lay"]
    assert len(first) == 64 and all("standing" in e for e in first)
    assert (set(found["nodes"][1]["X"]), set(found["nodes"][9]["X"])) == ({1050}, {1880})
    credits = [e for e in found["log"] if e["event"] == "credit"]
    assert {c["i"] for c in credits} == {8, 10} and len(credits) == 256 == int(
        found["counts"]["laid_back"]
    )
    out = table.gates(found)
    whole = out["8 families forming (whole view)"]
    assert (whole["species readable"], whole["decoded right per credit"]) == (256, 256)
    assert whole["tracks right"] == [128, 128] and whole["births by species (decoder)"] == {
        "gapped 0": 64
    }
    assert found["run_back"] == {"intervals": 20, "exact": 20}
    assert ({r["integers"] for r in found["rows"]}, max(r["max bits"] for r in found["rows"])) == (
        {89},
        115,
    )
    for match, change in (
        ("the plane at the gap 0", {"row": 1}),
        ("a field of no form", {"sense": 1}),
        ("each of Z_4", {"p1": seed["p1"][:15] + [4]}),
        ("each of Z_4", {"cz": 4}),
        ("mirror is 0 or 1", {"mirror": 2}),
    ):
        refused(match, Node, universe, dict(world, seed=[{**seed, **change}]))
    refused("a multiple of 4", Node, universe, dict(world, shape=[3, 3, 3]))
    plain, mirrored = (Node(universe, dict(world, seed=[{**seed, "mirror": m}])) for m in (0, 1))
    for a, b in zip(plain.emitter().lines, mirrored.emitter().lines, strict=True):
        assert (
            (a.now == b.now).all() and (a.before == b.before).all() and int((a.rem != b.rem).sum()) == 32
        )
