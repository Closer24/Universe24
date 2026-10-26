"""The conservation check over the engine (src/event_universe), re-based from the hand co1's kit on the lean toy (tools/derivations/open_items/conservations): a world file is run for N intervals on the engine's own Node, and every law of the lattice that the record and the board carry is read in integers alone, each interval, from the engine's log and its lines; the engine's code is imported and never changed (the check subclasses the Node to snapshot the rows before the close).

Usage: python tools/derivations/conservations/conservation_check.py <world.json> <intervals>
Prints one line per law, "LAW: held N of N" or "LAW: broken at interval k, Node (x, y, z), the numbers", then the readings and the verdict; exit code 0 only when every law holds.

The laws, each by its clause of docs/ALGEBRA.md:
 1. ENERGY in the clicks (The ledger of exactness, the exact take; The conservation at the click): at every click the take re-read from the rows before the close equals the credit line's `taken`, the take is the least count of levels whose fall pays the walls, the fall pays the walls (taken >= booked) and taken == booked exactly; the taken line's level stands moved by the levels toward its before (or laid back, EQ-S1); the born pair carries two whole quanta (each child's share up by one unit of its own at its Node).
 2. MOMENTUM (The lattice momentum): the close's change of P_a per record row equals, exactly, what the credit and birth lines book (dP_take on the taken row, dP_lay on the children's row); P_a per row at the start and the end as a reading.
 3. CHARGE (The sign is the rotation sense; The charge written is the Wronskian): the board's W over the planes unchanged by the close, every birth's two children W of opposite sign summing to 0 (W_children), the senses [-1, 1].
 4. FLUX (The flux form of Rule3): F_ij = -F_ji on every Link of the gap-0 line's own current at the interval's start. Rule3's identity per Node and line and the write's book are the symmetric ride's (R5, the kick at the mean wall) and are not re-derived here: named for a hand.
 5. COUNT (the owner's standing rule; The click writes on the lattice; The direction): every change of the rows at the close is a logged take or lay and nothing else (the book exact, every level and remainder compared); the run back from the end to the seed, the state's hash at every interval bit for bit.
 6. THE 48 on the clicks (The cube's symmetry): the births, the credits and the refusals read through every signed permutation of the axes on the 3-cube image of the world for at most 30 intervals, each image's clicks read back through the inverse equal to the base's (an orientation, twist or sense refusal compared as its Link, the two ends unordered; the world's seed folded onto the 3-cube modulo 3).
"""

from __future__ import annotations

import copy
import itertools
import json
import os
import sys
from typing import Any

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "src"))
sys.set_int_max_str_digits(0)

from event_universe import gram, readings  # noqa: E402
from event_universe.core.ports import AXES, across, port_of  # noqa: E402
from event_universe.core.rule3 import quotient, share_weight  # noqa: E402
from event_universe.links import link_current, wronskian  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import PLANE  # noqa: E402

IMAGE_CUBE = AXES  # the 48 are read on the 3-cube image of the world
IMAGE_INTERVALS = 30


def tot(a: Any) -> int:
    return int(np.sum(np.asarray(a, dtype=object))) if np.ndim(a) else int(a)


def at_node(a: Any, at: tuple[int, ...]) -> int:
    return int(np.asarray(a, dtype=object)[at]) if np.ndim(a) else int(a)


def snap(node: Node) -> list[list[Any]]:
    return [[line.copy() for line in row] for row in node.rows()]


def record_rows(node: Node, rows: list[list[Any]]) -> list[list[Any]]:
    """The records' lines out of a rows snapshot, in the records' order."""
    where = {id(r): k for k, r in enumerate(node.rows_)}
    return [rows[where[id(r)]] for r in node.records()]


def determinant(m: Any) -> int:
    """The determinant of a signed permutation in integers: the permutation's sign times the product of the signs (a rotation 1, a reflection -1)."""
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(AXES)]
    sign = 1
    for a in range(AXES):
        for b in range(a + 1, AXES):
            if pi[a] > pi[b]:
                sign = -sign
    for a in range(AXES):
        sign *= int(m[pi[a], a])
    return sign


class Law:
    """One law's tally: the held count and the first breaks with their numbers."""

    def __init__(self, name: str) -> None:
        self.name, self.held, self.of, self.breaks = name, 0, 0, []

    def count(self, ok: bool, interval: Any = None, node: Any = None, numbers: str = "") -> None:
        self.of += 1
        if ok:
            self.held += 1
        elif len(self.breaks) < 4:
            self.breaks.append((interval, node, numbers))

    def line(self) -> str:
        if not self.breaks:
            return f"{self.name}: held {self.held} of {self.of}"
        k, node, numbers = self.breaks[0]
        return f"{self.name}: broken at interval {k}, Node {node}, {numbers} (held {self.held} of {self.of})"

    def ok(self) -> bool:
        return not self.breaks


class Checked(Node):
    """The engine's Node with the rows snapshotted before its click (the state after the step and the swap), nothing else."""

    def click(self, plane_starts: Any, held: Any, direction: int = 1, frame: Any = None) -> None:
        if direction == 1:
            self.pre_close = snap(self)
        super().click(plane_starts, held, direction, frame)


def momentum(lines: list[Any], num: int) -> list[int]:
    """P_a = 2 num SUM over the lines and the Nodes of (now_(i+a) before_i - now_i before_(i+a))."""
    found = []
    for a in range(AXES):
        p = 0
        for line in lines:
            port = port_of(a, 0)
            p += tot(across(line.now, port) * line.before - line.now * across(line.before, port))
        found.append((num + num) * p)
    return found


def neighbour(at: tuple[int, ...], axis: int, side: int, cube: int) -> tuple[int, ...]:
    return tuple((x + (side if k == axis else 0)) % cube for k, x in enumerate(at))


def take_fall(node: Node, rule: Any, at: tuple[int, ...], now: int, before: int, cube: int) -> Any:
    """The take's fall at the Node as take.fall_of reads it, a function of the count s of levels moved toward the before."""
    own, w = at_node(rule.self_coefficient, at), int(rule.wall)
    reached = 0
    for port, reach in enumerate(rule.reaches):
        axis, side = port // 2, port % 2
        reached += at_node(reach, at) * before_at(node, rule, at, axis, side, cube)
    pull = own * before + reached
    x, weight = int(node.start_x[at]), share_weight(node.gamma, node.G)
    t = 1 if before > now else -1

    def fall(s: int) -> int:
        moved = now + t * s
        return int(quotient(x * (w * (now * now - moved * moved) - t * s * pull), weight))

    return fall, t


BEFORE_LINE: dict[str, Any] = {}


def before_at(node: Node, rule: Any, at: tuple[int, ...], axis: int, side: int, cube: int) -> int:
    """The taken line's before at the neighbour across the Port (the side 0 the + neighbour, 1 the - neighbour as core/ports lays them)."""
    line = BEFORE_LINE["line"]
    there = neighbour(at, axis, 1 if side == 0 else -1, cube)
    return int(line.before[there])


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.split("\n")[2])
        return 2
    world_path, n = argv[1], int(argv[2])
    universe, world = load_world(world_path)
    node = Checked(universe, world)
    cube = node.cube
    recs = node.records()
    rec0 = recs.index(node.emitter())
    nums = [r.pair[0] for r in recs if r.pair]
    print(
        json.dumps(
            {
                "world": os.path.basename(world_path),
                "cube": cube,
                "intervals": n,
                "den": node.den,
                "Gamma": node.gamma,
                "T": node.T,
                "G": node.G,
                "records": len(recs),
                "units": node.units,
            }
        )
    )
    names = [
        "ENERGY the take read from the rows equals the credit line",
        "ENERGY the take is the least count paying the walls",
        "ENERGY taken pays booked (taken >= booked)",
        "ENERGY the exact take (taken == booked)",
        "ENERGY the taken line stands moved by the levels (or laid back)",
        "ENERGY the born pair carries two whole quanta (one per child, the book)",
        "MOMENTUM the close wrote what the credit and birth lines book (dP_a exact per row)",
        "CHARGE the board W over the planes unchanged at the close",
        "CHARGE every birth W(-) + W(+) = 0 and the senses [-1, 1]",
        "FLUX F_ij = -F_ji on every Link of the gap-0 current",
        "COUNT the close book exact (every change a logged take or lay)",
        "COUNT the run back exact (the state bit for bit)",
    ]
    L = {k: Law(k) for k in names}
    reading: dict[str, Any] = {
        "clicks": {"births": 0, "credits": 0, "refused": 0, "turns": 0, "laid back": 0},
        "excess taken - booked (share units)": 0,
        "children laid at 1 / 2 / more quanta of their unit": [0, 0, 0],
        "momentum P_a per record row start/end": {},
        "W over the planes start/end": [None, None],
    }
    with_clicks = []
    hashes = [node.state_hash()]
    for t in range(n):
        pre = snap(node)
        node.step()
        post, mid = snap(node), node.pre_close
        turned = np.asarray(node.turned, dtype=bool)
        log_new = node.log[node.stack[-1]["log_from"] :]
        births = [e for e in log_new if e["event"] == "birth"]
        credits = [e for e in log_new if e["event"] == "credit"]
        refused = [e for e in log_new if e["event"] == "refused"]
        reading["clicks"]["births"] += len(births)
        reading["clicks"]["credits"] += len(credits)
        reading["clicks"]["refused"] += len(refused)
        reading["clicks"]["turns"] += int(turned.sum())
        reading["clicks"]["laid back"] += sum(1 for e in credits if "laid_back" in e)
        k = node.interval
        c = node.start_content
        pre_r, mid_r, post_r = record_rows(node, pre), record_rows(node, mid), record_rows(node, post)
        factors = node.link_factors(None, readings.frozen_of(node, c))
        # ---- 4. FLUX: the gap-0 line's own current antisymmetric on every Link at the start
        line0 = pre_r[rec0][0]
        anti = True
        for a in range(AXES):
            f_plus, f_minus = link_current(line0, port_of(a, 0)), link_current(line0, port_of(a, 1))
            if not bool(np.asarray(f_plus + across(f_minus, port_of(a, 0)) == 0).all()):
                anti = False
        L["FLUX F_ij = -F_ji on every Link of the gap-0 current"].count(
            anti, k, None, "the gap-0 current not antisymmetric on a Link"
        )
        # ---- 1. ENERGY in the clicks
        clicks_at: dict[tuple[tuple[int, ...], int, int], list[Any]] = {}
        for e in births + credits:
            takes = e["takes"] if "takes" in e else [e]
            rec = e["taken_row"] if e["event"] == "birth" else rec0
            booked = e["booked"] if e["event"] == "birth" else node.units[e["line"]]
            for tk in takes:
                at = tuple(tk["node"])
                walls = booked if len(takes) == 1 else tk["booked"]
                if "taken_levels" in tk:
                    L[names[2]].count(
                        tk["taken"] >= walls, k, at, f"taken {tk['taken']}, booked {walls}"
                    )
                    L[names[3]].count(
                        tk["taken"] == walls,
                        k,
                        at,
                        f"taken {tk['taken']}, booked {walls}, excess {tk['taken'] - walls}",
                    )
                    reading["excess taken - booked (share units)"] += tk["taken"] - walls
                    continue
                now_was, before, levels = tk["taker"]
                line_k = tk["taken_line"]
                clicks_at.setdefault((at, rec, line_k), []).append((tk, e))
                rule = node.rule_of(recs[rec], c, factors)
                BEFORE_LINE["line"] = mid_r[rec][line_k]
                fall, t_ = take_fall(node, rule, at, now_was, before, cube)
                read, taken = fall(levels), tk["taken"]
                L[names[0]].count(
                    read == taken, k, at, f"fall read {read}, credit line taken {taken}, levels {levels}"
                )
                least = levels >= 1 and (levels == 1 or fall(levels - 1) < walls) and read >= walls
                L[names[1]].count(
                    least,
                    k,
                    at,
                    f"levels {levels}, fall at levels - 1 {fall(levels - 1) if levels > 1 else 0}, walls {walls}",
                )
                L[names[2]].count(taken >= walls, k, at, f"taken {taken}, booked {walls}")
                L[names[3]].count(
                    taken == walls, k, at, f"taken {taken}, booked {walls}, excess {taken - walls}"
                )
                reading["excess taken - booked (share units)"] += taken - walls
        for (at, rec, line_k), found in clicks_at.items():
            tk, e = found[-1]
            now_was, before, levels = tk["taker"]
            t_ = 1 if before > now_was else -1
            stands = int(post_r[rec][line_k].now[at])
            want = now_was if "laid_back" in e else now_was + t_ * levels
            L[names[4]].count(
                len(found) > 1 or stands == want,
                k,
                at,
                f"the taken line now {stands}, the credit line's {want} ({'laid back' if 'laid_back' in e else 'taken'})",
            )
        for e in births:
            if "exact_lay" in e:
                continue
            s = e["line_pair"]
            row = recs[s]
            r = node.rule(row.pair, c, factors)
            quanta = []
            for where in (tuple(e["minus"]), tuple(e["plus"])):
                s1 = int(gram.share(node, post_r[s], r)[where])
                s0 = int(gram.share(node, mid_r[s], r)[where])
                q = (s1 - s0) // node.units[s]
                quanta.append(q)
                reading["children laid at 1 / 2 / more quanta of their unit"][
                    0 if q == 1 else 1 if q == 2 else 2
                ] += 1
            L[names[5]].count(
                all(q == 1 for q in quanta),
                k,
                e["node"],
                f"the two children laid {quanta} whole quanta of the unit {node.units[s]} where the book is 1 and 1 (amplitude {e['amplitude']})",
            )
        # ---- 2. MOMENTUM at the close, per record row, against the lines' dP_take and dP_lay
        if births or credits:
            expected = {rec: [0] * AXES for rec in range(len(recs))}
            for e in births + credits:
                rec = e["taken_row"] if e["event"] == "birth" else rec0
                for a in range(AXES):
                    expected[rec][a] += e["dP_take"][a]
                if e["event"] == "birth":
                    for a in range(AXES):
                        expected[e["line_pair"]][a] += e["dP_lay"][a]
            exact, bad = True, None
            for rec in range(len(recs)):
                p_mid, p_post = momentum(mid_r[rec], nums[rec]), momentum(post_r[rec], nums[rec])
                got = [p_post[a] - p_mid[a] for a in range(AXES)]
                if got != expected[rec]:
                    exact, bad = False, (rec, got, expected[rec])
                    break
            L[names[6]].count(
                exact,
                k,
                None,
                f"record {bad[0]}: the rows' dP {bad[1]} against the lines' {bad[2]}" if bad else "",
            )
        for rec in range(len(recs)):
            if t == 0:
                reading["momentum P_a per record row start/end"][rec] = [
                    momentum(pre_r[rec], nums[rec]),
                    None,
                ]
            reading["momentum P_a per record row start/end"][rec][1] = momentum(post_r[rec], nums[rec])
        # ---- 3. CHARGE at the close
        planes = [rec for rec, r in enumerate(recs) if r.shape == PLANE]
        w_mid = sum(tot(wronskian(*mid_r[rec])) for rec in planes)
        w_post = sum(tot(wronskian(*post_r[rec])) for rec in planes)
        if t == 0:
            reading["W over the planes start/end"][0] = sum(
                tot(wronskian(*pre_r[rec])) for rec in planes
            )
        reading["W over the planes start/end"][1] = w_post
        L[names[7]].count(
            w_post == w_mid,
            k,
            None,
            f"W after the step {w_mid}, after the close {w_post}, births {len(births)}",
        )
        for e in births:
            L[names[8]].count(
                sum(e["W_children"]) == 0 and sorted(e["senses"]) == [-1, 1],
                k,
                e["node"],
                f"the two children W {e['W_children']}, senses {e['senses']}",
            )
        # ---- 5. COUNT: the close's book exact
        expected_rows = [[line.copy() for line in row] for row in mid]
        exp_r = record_rows(node, expected_rows)
        for e in births + credits:
            takes = e["takes"] if "takes" in e else [e]
            rec = e["taken_row"] if e["event"] == "birth" else rec0
            for tk in takes:
                at = tuple(tk["node"])
                if "taken_levels" in tk:
                    taken_levels = tk["taken_levels"]
                    for line, n_, b_ in zip(
                        exp_r[rec], taken_levels[0::2], taken_levels[1::2], strict=True
                    ):
                        line.now[at], line.before[at] = line.now[at] - n_, line.before[at] - b_
                    continue
                now_was, before, levels = tk["taker"]
                t_ = 1 if before > now_was else -1
                if "laid_back" not in e:
                    exp_r[rec][tk["taken_line"]].now[at] = (
                        exp_r[rec][tk["taken_line"]].now[at] + t_ * levels
                    )
        for e in births:
            s = e["line_pair"]
            amp_a, amp_b = e["amplitude"]
            re, im = exp_r[s]
            ends = ((-1, tuple(e["minus"])), (1, tuple(e["plus"])))
            for (sense, where), laid in zip(ends, e.get("exact_lay", [None, None]), strict=True):
                if laid is None:  # GP-S1: the charge's sign on the re line
                    re.now[where] = re.now[where] + sense * amp_a
                    im.before[where] = im.before[where] + amp_b
                else:
                    exp_r[s][laid[0]].now[where] = exp_r[s][laid[0]].now[where] + laid[1]
        book_ok, book_bad = True, None
        for ridx, (row_e, row_p) in enumerate(zip(expected_rows, post, strict=True)):
            for j, (le, lp) in enumerate(zip(row_e, row_p, strict=True)):
                for slot in ("now", "before", "rem", "wr"):
                    xe, xp = getattr(le, slot), getattr(lp, slot)
                    if xe is None:
                        continue
                    off = np.asarray(xe != xp)
                    if bool(off.any()):
                        book_ok = False
                        book_bad = (
                            ridx,
                            j,
                            slot,
                            tuple(int(x) for x in next(zip(*np.nonzero(off), strict=True))),
                        )
                        break
                if not book_ok:
                    break
            if not book_ok:
                break
        L[names[10]].count(
            book_ok,
            k,
            None if book_bad is None else book_bad[3],
            f"a change not in the log: row {book_bad[0]} line {book_bad[1]} {book_bad[2]}"
            if book_bad
            else "",
        )
        if births or credits:
            with_clicks.append(
                {
                    "i": k,
                    "births": len(births),
                    "credits": len(credits),
                    "laid back": sum(1 for e in credits if "laid_back" in e),
                    "refused": len(refused),
                    "turned": int(turned.sum()),
                }
            )
        hashes.append(node.state_hash())
    # ---- 5. the run back
    exact, first_bad = 0, None
    for kk in range(n):
        node.step_back()
        if node.state_hash() == hashes[n - 1 - kk]:
            exact += 1
        elif first_bad is None:
            first_bad = n - 1 - kk
    L[names[11]].count(
        exact == n, first_bad, None, f"exact {exact} of {n}, first mismatch at interval {first_bad}"
    )
    L[names[11]].held, L[names[11]].of = exact, n
    # ---- 6. THE 48 on the clicks
    n48 = min(n, IMAGE_INTERVALS)
    law48 = Law(
        f"THE 48 on the clicks (births, credits, refusals through the image; the {IMAGE_CUBE}-cube image of the world, {n48} intervals)"
    )

    def image(m: Any, at: Any) -> tuple[int, ...]:
        return tuple(int(x) % IMAGE_CUBE for x in m @ np.array(at, dtype=int))

    def world_image(m: Any) -> dict[str, Any]:
        w2 = copy.deepcopy(world)
        w2["shape"] = [IMAGE_CUBE] * AXES
        for lay in w2.get("seed", []):
            for key in ("at", "centre"):
                if key in lay:
                    lay[key] = list(image(m, tuple(int(x) % IMAGE_CUBE for x in lay[key])))
        return w2

    def clicks_of(bb: Node, m: Any) -> tuple[list[Any], list[Any], list[Any]]:
        births_ = sorted(
            (
                e["i"],
                image(m, e["node"]),
                e["line_pair"],
                image(m, e["minus"]),
                image(m, e["plus"]),
                e["taken"],
                e["booked"],
                e["levels"],
            )
            for e in bb.log
            if e["event"] == "birth"
        )
        credits_ = sorted(
            (
                e["i"],
                image(m, e["node"]),
                e["line"],
                e["taken"],
                e["levels"],
                e["beat"],
                e["proper"],
                e["sense"],
            )
            for e in bb.log
            if e["event"] == "credit"
        )
        refused_ = sorted(
            (
                e["i"],
                tuple(sorted((image(m, e["node"]), image(m, e["link"]))))
                if "link" in e
                else (image(m, e["node"]),),
                e["cause"],
            )
            for e in bb.log
            if e["event"] == "refused"
        )
        return births_, credits_, refused_

    def signed_permutations() -> list[Any]:
        axes = range(AXES)
        return [
            np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes])
            for pi in itertools.permutations(axes)
            for s in itertools.product((1, -1), repeat=AXES)
        ]

    try:
        eye = np.eye(AXES, dtype=int)
        base = Node(json.loads(json.dumps(universe)), world_image(eye))
        for _ in range(n48):
            base.step()
        base_clicks = clicks_of(base, eye)
        counts48 = {
            "births": len(base_clicks[0]),
            "credits": len(base_clicks[1]),
            "refused": len(base_clicks[2]),
            "images holding births/credits/refusals": [0, 0, 0],
            "rotations/reflections apart": [0, 0],
        }
        for m in signed_permutations():
            other = Node(json.loads(json.dumps(universe)), world_image(m))
            for _ in range(n48):
                other.step()
            found = clicks_of(other, np.array(m.T, dtype=int))
            same = [found[q] == base_clicks[q] for q in range(3)]
            for q in range(3):
                counts48["images holding births/credits/refusals"][q] += int(same[q])
            det = determinant(m)
            if not all(same):
                counts48["rotations/reflections apart"][0 if det == 1 else 1] += 1
            law48.count(
                all(same),
                None,
                None,
                f"image {m.tolist()} apart in {[nm for nm, s_ in zip(('births', 'credits', 'refused'), same, strict=True) if not s_]}",
            )
        print(json.dumps({"the 48": counts48}))
    except ValueError as err:
        law48.count(False, None, None, f"the {IMAGE_CUBE}-cube image refused: {err}")
    all_ok = True
    for name in names:
        print(L[name].line())
        all_ok = all_ok and L[name].ok()
        for brk in L[name].breaks[1:]:
            print(f"  also at interval {brk[0]}, Node {brk[1]}: {brk[2]}")
    print(law48.line())
    all_ok = all_ok and law48.ok()
    print(json.dumps({"readings": reading}))
    for row in with_clicks[:12]:
        print(json.dumps({"interval with clicks": row}))
    if len(with_clicks) > 12:
        print(json.dumps({"intervals with clicks": len(with_clicks), "shown": 12}))
    print("VERDICT: " + ("every law holds" if all_ok else "a law is broken (named above)"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
