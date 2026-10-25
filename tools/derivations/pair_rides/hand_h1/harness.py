"""The hand h1's harness (2026-10-25, "the pair rides the quantum"): the measurement variant behind U24_PAIR_RIDES=1; scratch analysis, never src."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import digits, lay, meeting_board, node, records, seed, world_files
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.lattice import Lattice
from event_universe.loader.circle import circle_points, lift_points
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import bare_torus

PORT_SIDES = node.PORT_SIDES


def world_at(folder: Path, cube: int, den: int, intervals: int = 400) -> Path:
    import tests.laws_universe as lu

    saved = dict(lu.SMALL["integers"])
    lu.SMALL["integers"]["den"] = den
    try:
        path = bare_torus(folder, cube, intervals)
    finally:
        lu.SMALL["integers"].update(saved)
    return path


def lift_family(board: Lattice) -> tuple[int, int, int]:
    den = board.world.integers["den"] if hasattr(board.world, "integers") else board.families[0].pair[1]
    (vector, num, s), *_rest = lift_points(den)
    k = next(i for i, f in enumerate(board.families) if f.pair == (num, den))
    return k, num, s


def pythagorean_hits(number: int, unit: int, den: int) -> dict[str, Any]:
    """The draw of (num, s) from the read's one number: Q the quotient by the unit; rule A both from residues (num = Q mod den, s = (Q div den) mod den); rule B num from the residue and s the integer sine by the search, accepted where exact."""
    q = int(division_forward(number, unit, 0)[0])
    num_a = int(division_forward(q, den, 0)[1])
    s_a = int(division_forward(int(division_forward(q, den, 0)[0]), den, 0)[1])
    hit_a = num_a * num_a + s_a * s_a == den * den and num_a > 0 and s_a > 0
    num_b = num_a
    s_b = largest_below(den * den - num_b * num_b)
    hit_b = s_b * s_b == den * den - num_b * num_b and num_b > 0 and s_b > 0
    return {
        "q": q,
        "num_a": num_a,
        "s_a": s_a,
        "hit_a": hit_a,
        "num_b": num_b,
        "s_b": s_b,
        "hit_b": hit_b,
    }


def measure_births(folder: Path, cube: int, den: int, intervals: int) -> dict[str, Any]:
    """(i) main's path: every meeting read's number logged, the acceptance's hits counted against main's births; the Link-intervals with a whole quantum at each end counted from the shares."""
    world_files.REPOSITORY_ROOT = folder
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(world_at(folder, cube, den, intervals)), output=lines.append)
    seed_index = board.world.seed
    unit = board.credit.units[seed_index]
    reads: list[int] = []
    original = digits.read_of

    def logged(b: Lattice, rd: Any, label: str) -> int:
        found = original(b, rd, label)
        reads.append(int(found))
        return found

    meeting_board.read_of = logged
    link_meetings = 0
    began = time.perf_counter()
    for _ in range(intervals):
        board.step()
        shares = board.share_of(seed_index)[0]
        whole = np.asarray(shares, dtype=object) >= unit
        for axis in range(3):
            link_meetings += int(np.sum(whole & np.roll(whole, -1, axis=axis)))
    meeting_board.read_of = original
    hits = [pythagorean_hits(n, unit, den) for n in reads]
    births = [line for line in lines if line.get("event") == "birth"]
    refused = [line for line in lines if line.get("event") == "refused"]
    return {
        "cube": cube,
        "den": den,
        "intervals": intervals,
        "seconds": round(time.perf_counter() - began, 1),
        "reads": len(reads),
        "hits_rule_a": sum(h["hit_a"] for h in hits),
        "hits_rule_b": sum(h["hit_b"] for h in hits),
        "main_births": len(births),
        "refusals": len(refused),
        "link_intervals_both_whole": link_meetings,
        "circle_points": len(circle_points(den)),
        "p_rule_a": len(circle_points(den)) / (den * den),
        "p_rule_b": len(circle_points(den)) / den,
        "first_reads": [h["q"] for h in hits[:5]],
    }


# ---- (ii) to (iv): the pattern with a pair, the ride and the hole, the run back ----


class Rides:
    """The variant's third-rule act on the one matter plane: the ride, the hole and the birth's pair, logged per interval for the run back."""

    def __init__(self, board: Lattice, k: int, num: int, den: int) -> None:
        self.board, self.k, self.num, self.den = board, k, num, den
        self.nums = np.full(board.shape, den, dtype=object)
        node.NUMS[board.families[k].pair] = self.nums
        self.unit = count_wall(board.families[k], board.world.quantum_action)
        self.floors = np.zeros(board.shape, dtype=object)
        self.log: dict[int, list[tuple[tuple[int, int, int], int, int]]] = {}
        self.counts = {"rides": 0, "holes": 0, "births": 0, "ties": 0}

    def floors_now(self) -> np.ndarray:
        if not self.board.states[self.k].lines:
            return np.zeros(self.board.shape, dtype=object)
        shares = np.asarray(self.board.share_of(self.k)[0], dtype=object)
        return np.asarray(division_forward(shares, self.unit, 0)[0], dtype=object)

    def act(self) -> None:
        """After the close: a Node at (den, 0) whose floor rose with a neighbour's pair through a Port takes it (the ride); a Node with a pair whose floor fell to 0 returns to (den, 0) (the hole); a Node with a floor from 0 and no neighbour's pair was born: the birth's pair."""
        after = self.floors_now()
        changes = []
        nums = self.nums
        neighbours = [node.arrival(nums, axis, side) for axis, side in PORT_SIDES]
        for at in np.ndindex(*self.board.shape):
            here = int(nums[at])
            if here == self.den:
                if int(after[at]) >= 1 and int(after[at]) > int(self.floors[at]):
                    pairs = {int(n[at]) for n in neighbours if int(n[at]) != self.den}
                    if len(pairs) > 1:
                        self.counts["ties"] += 1
                        continue
                    if pairs:
                        changes.append((at, here, pairs.pop()))
                        self.counts["rides"] += 1
                    else:
                        changes.append((at, here, self.num))
                        self.counts["births"] += 1
            elif int(after[at]) == 0:
                changes.append((at, here, self.den))
                self.counts["holes"] += 1
        for at, _was, now in changes:
            nums[at] = now
        if changes:
            self.log[self.board.interval] = [
                (tuple(int(i) for i in at), was, now) for at, was, now in changes
            ]
        self.floors = after

    def undo(self) -> None:
        """Before the step back of the board's interval: the act's pairs of that close restored (the lay's inverse from the books)."""
        for at, was, _now in reversed(self.log.get(self.board.interval, [])):
            self.nums[at] = was
        self.floors = self.floors_now()  # re-read after the inverse by the caller


def lay_pattern(
    board: Lattice, k: int, num: int, s: int, den: int, nodes: list[tuple[int, int, int]], amplitude: int
) -> None:
    """The pattern at rest at its pair on the Nodes: z_now = A, z_before = A e^(-i omega_0) with cos omega_0 = num / den, laid through the one lay act at the lay's origin (sense +1)."""
    board.born_point(k)
    mask = board.mask(tuple(nodes))
    re_before = int(division_forward(amplitude * num, den, 0)[0])
    im_before = int(division_forward(amplitude * s, den, 0)[0])
    first = records.record_slice(board.families[k], 0).start
    zeros = np.zeros(board.shape, dtype=object)
    origin = board.half_wall(k)
    lay.laid(
        board, k, first, (np.where(mask, amplitude, 0), np.where(mask, re_before, 0)), None, origin, mask
    )
    lay.laid(board, k, first + 1, (zeros, np.where(mask, im_before, 0)), None, origin, mask)
    board.credit.counts[k] += len(nodes)


def amplitude_for(
    board: Lattice, k: int, num: int, s: int, den: int, nodes: list, target_tenths: int = 15
) -> int:
    """The amplitude whose share at the first Node is about target_tenths / 10 of the unit (a scan on copies of the state)."""
    unit = count_wall(board.families[k], board.world.quantum_action)
    import copy

    best = None
    for amplitude in range(50, 3000, 10):
        saved = (
            copy.deepcopy(board.states),
            dict(board.credit.counts),
            copy.deepcopy(board.born_at),
            copy.deepcopy(board.fixed_walls),
        )
        lay_pattern(board, k, num, s, den, nodes, amplitude)
        share = int(np.asarray(board.share_of(k)[0], dtype=object)[nodes[0]])
        board.states, board.credit.counts, board.born_at, board.fixed_walls = saved
        from event_universe.features.read import READS

        READS.clear()
        if 10 * share >= target_tenths * unit:
            best = amplitude
            break
    assert best is not None
    return best


def distance(a: tuple[int, int, int], b: tuple[int, int, int], shape: tuple[int, int, int]) -> int:
    return sum(min(abs(x - y), n - abs(x - y)) for x, y, n in zip(a, b, shape, strict=False))


def exact_solve(lines, remainders_after, rule_wall, den, gamma, unit, at) -> list[float]:
    """The decoder's solve of Rule3's line for x = num / den at the vacuum paces with no tension: x = [w (a_next - 2 a_now + a_before) + r' - r + 12 den Gamma^2 G^2 a_now] / [2 den Gamma^2 G^2 SUM_j (m_j - a_now) + 12 den Gamma^2 G^2 a_now], per line."""
    found = []
    g2 = unit * unit
    for (start, after), (r_before, r_after) in zip(lines, remainders_after, strict=False):
        a_before, a_now, a_next = int(start.before[at]), int(start.now[at]), int(after.now[at])
        m = sum(int(node.arrival(start.now, axis, side)[at]) for axis, side in PORT_SIDES)
        top = (
            rule_wall * (a_next - 2 * a_now + a_before)
            + (r_after - r_before)
            + 12 * den * gamma * gamma * g2 * a_now
        )
        bottom = 2 * den * gamma * gamma * g2 * (m - 6 * a_now) + 12 * den * gamma * gamma * g2 * a_now
        found.append(None if bottom == 0 else top / bottom)
    return found


def measure_pattern(
    folder: Path,
    cube: int,
    den: int,
    intervals: int,
    block: int,
    light: bool,
    variant: bool,
    run_back: int = 0,
) -> dict[str, Any]:
    world_files.REPOSITORY_ROOT = folder
    node.NUMS.clear()
    node.PAIR_RIDES = variant
    if not light:
        seed.uniform_seed = lambda board, index: None  # no light: the pattern alone
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(world_at(folder, cube, den, intervals + 10)), output=lines.append)
    k, num, s = lift_family(board)
    centre = tuple([cube // 2] * 3)
    half = block // 2
    nodes = [
        tuple((c + d) % cube for c, d in zip(centre, (dx, dy, dz), strict=False))
        for dx in range(-half, half + 1)
        for dy in range(-half, half + 1)
        for dz in range(-half, half + 1)
    ]
    amplitude = amplitude_for(board, k, num, s, den, [centre])
    lay_pattern(board, k, num, s, den, nodes, amplitude)
    rides = Rides(board, k, num, den)
    if variant:
        for at in nodes:
            rides.nums[at] = num
        rides.floors = rides.floors_now()
    unit = rides.unit
    gamma, g = board.world.node_clock, board.unit
    wall = 6 * den * gamma * gamma * g * g

    def metrics() -> dict[str, Any]:
        from event_universe import share as _share

        content, factors = board.read(k, 1, 0)
        shares = np.asarray(
            _share.family_share(board.families[k], board.lines_of(k, 0), gamma, content, factors, g),
            dtype=object,
        )  # the laid record alone (record 0), the born children apart
        total = int(shares.sum())
        within = sum(
            int(shares[at]) for at in np.ndindex(*board.shape) if distance(at, centre, board.shape) <= 1
        )
        floors = np.asarray(division_forward(shares, unit, 0)[0], dtype=object)
        paired = [at for at in np.ndindex(*board.shape) if int(rides.nums[at]) != den]
        return {
            "total_over_unit": round(total / unit, 3),
            "within_one_link": round(within / unit, 3),
            "fraction_within": round(within / total, 3) if total else None,
            "nodes_whole": int(np.sum(floors >= 1)),
            "nodes_with_level": int(np.sum(shares != 0)),
            "paired_nodes": len(paired),
            "pair_reach": max((distance(at, centre, board.shape) for at in paired), default=0),
        }

    history = [{"interval": 0, **metrics()}]
    states = [board_state(board)] if run_back else []
    credits = []
    began = time.perf_counter()
    for t in range(intervals):
        start_lines = (
            [
                (line.now.copy(), line.before.copy(), line.remainder.copy())
                for line in board.states[k].lines[:2]
            ]
            if board.states[k].lines
            else []
        )
        kept = board.advanced_to_the_close()
        stepped = (
            [
                (line.now.copy(), line.before.copy(), line.remainder.copy())
                for line in board.states[k].lines[:2]
            ]
            if board.states[k].lines
            else []
        )
        n_before = len(lines)
        board.closed_after(kept)
        board.passes, board.heading = board.passes + (board.heading < 0), 1
        for line in lines[n_before:]:
            if line.get("event") == "credit" and line.get("readings", {}).get("identity") == [k, 0]:
                at = tuple(line["readings"]["support"])
                sol = None
                if start_lines:
                    pairs = [
                        (records.Record(*start_lines[i]), records.Record(*stepped[i])) for i in range(2)
                    ]
                    rem = [(int(start_lines[i][2][at]), int(stepped[i][2][at])) for i in range(2)]
                    sol = exact_solve(pairs, rem, wall, den, gamma, g, at)
                credits.append(
                    {
                        "interval": t + 1,
                        "node": list(at),
                        "distance": distance(at, centre, board.shape),
                        "point": line["readings"].get("point"),
                        "beat": line["readings"].get("beat"),
                        "unit": unit,
                        "solve": sol,
                        "momentum": line.get("momentum"),
                    }
                )
        if variant:
            rides.act()
        if run_back:
            states.append(board_state(board))
        if t + 1 in (1, 2, 5, 10, 20, 40, 60, 100, 150, 200, 250, 300) or t + 1 == intervals:
            history.append({"interval": t + 1, **metrics()})
    seconds = round(time.perf_counter() - began, 1)
    back = None
    if run_back:
        matched = 0
        for j in range(run_back):
            if variant:
                rides.undo()
            board.step_inverse()
            matched += same_state(board_state(board), states[intervals - 1 - j])
        back = {"steps": run_back, "matched": matched, "interval_after": board.interval}
    births = [line for line in lines if line.get("event") == "birth"]
    all_credits = [line for line in lines if line.get("event") == "credit"]
    return {
        "cube": cube,
        "den": den,
        "block": block,
        "light": light,
        "variant": variant,
        "amplitude": amplitude,
        "unit": unit,
        "pair": [num, s],
        "intervals": intervals,
        "seconds": seconds,
        "history": history,
        "credits_of_pattern": credits,
        "credits_all": len(all_credits),
        "births": len(births),
        "ride_counts": rides.counts,
        "run_back": back,
        "integers_at_start_plus_pair": None,
    }


if __name__ == "__main__":
    what = sys.argv[1]
    folder = Path(sys.argv[2])
    folder.mkdir(parents=True, exist_ok=True)
    out = Path(sys.argv[3])
    results = []
    if what == "births":
        for cube, den, intervals in ((3, 1021, 120), (5, 1021, 120), (3, 1105, 120), (3, 65, 120)):
            try:
                results.append(measure_births(folder, cube, den, intervals))
            except Exception as refusal:
                results.append({"cube": cube, "den": den, "error": repr(refusal)[:400]})
            out.write_text(json.dumps(results, indent=1, default=str))
    elif what == "pattern":
        cube, intervals, block, light, variant, run_back = (
            int(sys.argv[4]),
            int(sys.argv[5]),
            int(sys.argv[6]),
            sys.argv[7] == "1",
            sys.argv[8] == "1",
            int(sys.argv[9]),
        )
        results.append(measure_pattern(folder, cube, 1021, intervals, block, light, variant, run_back))
        out.write_text(json.dumps(results, indent=1, default=str))
    print(json.dumps(results, default=str)[:3000])
