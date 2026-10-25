"""Hand h2's measurement variant of the proposal "the pair rides the quantum" (2026-10-25): a per-Node pair (num_i, s_i) on one matter plane, read by Rule3's coefficients at the Node and never written by the step, behind the environment flag U24_H2_MODE (off: main's path untouched, bit for bit; own: each end's reach from its own num_i; link: the Link's reach from the one number both ends read, min(num_i, num_j)); the ride (a whole quantum crossing one Link sets the receiver's pair), the hole (the share below one quantum returns the pair to (den, 0)) and the exclusion (a pair not the sender's refuses the ride) as acts after the step, logged for the run back; the birth-rate count of the acceptance num^2 + s^2 = den^2 on the read's quotient; the bound-or-spread reading of a hand-laid pair; the clicks and the decoder's solve x = 3 cos omega / SUM cos k_a; the run back MATCH. A scratch tool of the worktree hand-h2, never pushed; floats in the readings only, never in the engine's integers.

U24_H2_MODE=link PYTHONPATH=src:. python tools/hand_h2_pair_rides.py <part> [cube] [intervals]
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import bound_body, digits, emission, flux, meeting_board, node, share, world_files
from event_universe.core import paces
from event_universe.core.ports import AXES, PORT_SIDES, arrival
from event_universe.core.rule3 import Rule, division_forward, form_term, largest_below, wall_of
from event_universe.core.rule3 import mass as mass_of
from event_universe.features.phase import fold, signed_rounded
from event_universe.features.read import READS, read_again
from event_universe.lattice import Lattice
from event_universe.loader.circle import circle_points
from event_universe.plane import link_levels, link_wall, phase_links
from event_universe.readings import ports
from event_universe.take import Item
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import bare_torus

MODE = os.environ.get("U24_H2_MODE", "off")
DELTA = int(os.environ.get("U24_H2_DELTA", "1"))  # the whole quanta of the hand lay at the one Node
H2: dict[str, Any] = {"active": False, "name": None, "num": None, "s": None, "den": None, "mode": MODE}
LOG: list[dict[str, Any]] = []  # the ride's, the hole's and the exclusion's lines


def port_num(num: Any, port: int) -> Any:
    """The num the reach through `port` is read with: the Node's own (mode own) or the Link's one number min(num_i, num_j) read the same from both ends (mode link)."""
    if H2["mode"] != "link":
        return num
    axis, side = PORT_SIDES[port]
    other = arrival(num, axis, side)
    return np.where(other < num, other, num)


def h2_rule_of(family: Any, gamma: int, content: Any, factors: Any = None, unit: int = 1) -> Rule:
    """Rule3's integers with the per-Node pair: D_i = 12 (den - num_i) p_0^2 G^2, R_ij = 2 p_i^2 Q_ij num (the num of `port_num`), w unchanged, S = 2 w - D - SUM R."""
    if not H2["active"] or family.name != H2["name"]:
        return REAL_RULE_OF(family, gamma, content, factors, unit)
    num, den = H2["num"], family.pair[1]
    clock, pace = paces.node_paces(gamma, content)
    square = unit * unit
    node_squared = np.asarray(pace, dtype=object) * np.asarray(pace, dtype=object)
    links = (square,) * 6 if factors is None else factors
    reaches = tuple(2 * node_squared * factor * port_num(num, port) for port, factor in enumerate(links))
    wall, own = wall_of(den, gamma, unit), mass_of(num, den, np.asarray(clock, dtype=object), unit)
    return Rule(reaches, wall + wall - own - sum(reaches), wall, own)


def h2_sign_pairs(
    nums: tuple[Any, ...], gamma: int, factors: tuple[Any, ...], links: tuple[Any, ...]
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """plane.sign_pairs with the num per Port (`port_num`), X_ij = 2 num Q_ij."""
    wall = link_wall(gamma)
    even, odd = [], []
    for num, factor, link in zip(nums, factors, links, strict=True):
        x, circle = 2 * num * factor, wall * wall + link * link
        even.append(paces.rounded(x * (wall * wall - link * link), circle))
        odd.append(signed_rounded(x * 2 * wall * link, circle))
    return tuple(even), tuple(odd)


def h2_pairs_of(
    index: int,
    families: Any,
    states: Any,
    direction: int,
    gamma: int,
    content: Any,
    factors: Any,
    record: int,
    amplitude: int,
) -> Any:
    """flux.pairs_of with the per-Node pair on the matter plane: the sign's pair per Port at the Port's num, folded with the phase pair, times p_i^2."""
    if not H2["active"] or families[index].name != H2["name"]:
        return REAL_PAIRS_OF(
            index, families, states, direction, gamma, content, factors, record, amplitude
        )
    key = (h2_pairs_of, index, record, direction, gamma, amplitude)
    taken = (
        *states[index].lines,
        *(line for held, family in enumerate(families) if family.held for line in states[held].lines),
        *(
            line
            for held, family in enumerate(families)
            if family.held
            for row in states[held].phases
            for line in row
        ),
        content,
        *(() if factors is None else tuple(factors)),
        H2["num"],
    )
    if (kept := read_again(key, taken)) is not None:
        return kept[0]
    angles = node.turning(index, families, states, direction, record)
    if angles is None:
        READS[key] = (taken, (None, []))
        return None
    sign = link_levels(angles[1], families[node.sign_holder(index, families)].link_read)
    row = node.registry.row_of(families, states, index, record)
    phases = phase_links(states[node.sign_holder(index, families)].phases[row])
    nums = tuple(port_num(H2["num"], port) for port in range(6))
    evens, odds = h2_sign_pairs(nums, gamma, factors, sign)
    phased = [
        fold(c, s, hop[0], hop[1], amplitude) for c, s, hop in zip(evens, odds, phases, strict=True)
    ]
    evens, odds = tuple(f[0] for f in phased), tuple(f[1] for f in phased)
    pace = np.asarray(paces.link_pace_of(gamma, content), dtype=object)
    square = pace * pace
    found = tuple(square * x for x in evens), tuple(square * x for x in odds)
    READS[key] = (taken, (found, []))
    return found


def h2_share(
    pair: Any,
    record: Any,
    gamma: int,
    content: Any = 0,
    factors: Any = None,
    unit: int = 1,
    nodes: Any = None,
    as_read: Any = None,
) -> np.ndarray:
    """share.share with the per-Node pair where the pair is the matter plane's: the conserved form's term with the Node's own D_i and the Ports' reaches at `port_num`."""
    if not H2["active"] or tuple(pair) != tuple(H2["pair"]):
        return REAL_SHARE(pair, record, gamma, content, factors, unit, nodes, as_read)
    den = pair[1]
    at = (record.now != 0) | (record.before != 0) if nodes is None else nodes
    if nodes is None and as_read is None:
        beside = ports(np.asarray(at, dtype=np.int64))
        at = at | np.logical_or.reduce([np.asarray(value) != 0 for value in beside])
    read = record if as_read is None else as_read
    now, before = record.now[at].astype(object), record.before[at].astype(object)
    clock, pace = paces.node_paces(gamma, paces.at_nodes(content, at))
    links = (
        (unit * unit,) * 6
        if factors is None
        else tuple(paces.at_nodes(factor, at) for factor in factors)
    )
    nums = tuple(np.asarray(port_num(H2["num"], port), dtype=object)[at] for port in range(6))
    pace_o = np.asarray(pace, dtype=object)
    reads = tuple(2 * pace_o * pace_o * link * num for link, num in zip(links, nums, strict=True))
    wall = wall_of(den, gamma, unit)
    own = mass_of(np.asarray(H2["num"], dtype=object)[at], den, np.asarray(clock, dtype=object), unit)
    self_coefficient = wall + wall - own - sum(reads)
    arrived = tuple(value[at].astype(object) for value in ports(read.before))
    link = sum(r * a for r, a in zip(reads, arrived, strict=True))
    turn = self_coefficient * (read.before[at].astype(object) - before)
    found = form_term(self_coefficient, wall, now, before) - now * (link + turn)
    halves = 1
    if as_read is None:
        arrived_now = tuple(value[at].astype(object) for value in ports(record.now))
        present = tuple(value[at] for value in ports(np.ones(record.now.shape, dtype=object)))
        shared = sum(
            r * (before - b_j) * (now + n_j) * on
            for r, b_j, n_j, on in zip(reads, arrived, arrived_now, present, strict=True)
        )
        found, halves = found + found - shared, 2
    everywhere = np.zeros(record.now.shape, dtype=object)
    everywhere[at] = share.over_pace(found, gamma, paces.at_nodes(content, at), unit, halves)
    return everywhere


REAL_RULE_OF, REAL_PAIRS_OF, REAL_SHARE = node.rule_of, flux.pairs_of, share.share
if MODE != "off":
    node.rule_of = h2_rule_of
    flux.pairs_of = h2_pairs_of
    share.share = h2_share


def activate(board: Lattice, index: int) -> None:
    """The per-Node pair arrays on the matter plane `index`: (den, 0) at every Node."""
    den = board.families[index].pair[1]
    H2.update(
        active=MODE != "off", name=board.families[index].name, pair=board.families[index].pair, den=den
    )
    H2["num"] = np.full(board.shape, den, dtype=object)
    H2["s"] = np.full(board.shape, 0, dtype=object)


def set_pair(at: tuple[int, int, int], num: int, s: int) -> None:
    H2["num"][at], H2["s"][at] = num, s


def point_family(board: Lattice) -> tuple[int, int, int]:
    """The point (779, 1021)'s family index at den 1,021, with num and the leg s."""
    den = board.families[board.world.seed].pair[1]
    found = max(
        (k for k in board.order if share.charged(board.families[k])),
        key=lambda k: board.families[k].pair[0],
    )
    num = board.families[found].pair[0]
    return found, num, largest_below(den * den - num * num)


def lay_pair(board: Lattice, index: int, at: tuple[int, int, int], sense: int) -> None:
    """One whole quantum of the point laid by hand at one Node on record 0 (emission.laid_by_count, the engine's own lay) and the Node's pair set to the point's."""
    den = board.families[index].pair[1]
    emission.laid_by_count(board, Item(index, DELTA, (at,), (den, den), sense=sense, record=0))
    _k, num, s = point_family(board)
    set_pair(at, num, sense * s)


def floors_of(board: Lattice, index: int, unit: int) -> np.ndarray:
    shares = board.share_of(index)[0]
    return np.asarray(division_forward(np.asarray(shares, dtype=object), unit, 0)[0], dtype=object)


def ride(board: Lattice, before: np.ndarray, after: np.ndarray) -> None:
    """The third rule's acts (2) after the step, one Link each: the ride where the floor of the share over the unit rose by one at a Node at (den, 0) while it fell at a neighbour with a pair across one Link; the exclusion where the receiver's pair is another's; the hole where a Node's share fell below one quantum."""
    num, s, den = H2["num"], H2["s"], H2["den"]
    rises, falls = after - before, before - after
    new_num, new_s = num.copy(), s.copy()
    for axis in range(AXES):
        for side in (1, -1):
            far_num, far_s = arrival(num, axis, side), arrival(s, axis, side)
            far_fall = arrival(falls, axis, side)
            crossing = (rises >= 1) & (far_fall >= 1) & (far_num < den)
            for at in zip(*np.nonzero(crossing), strict=True):
                here = (int(at[0]), int(at[1]), int(at[2]))
                if num[here] == den:
                    new_num[here], new_s[here] = far_num[here], far_s[here]
                    LOG.append(
                        {
                            "interval": board.interval,
                            "act": "ride",
                            "at": list(here),
                            "axis": axis,
                            "side": side,
                            "num": int(far_num[here]),
                        }
                    )
                elif num[here] != far_num[here] or s[here] != far_s[here]:
                    LOG.append(
                        {
                            "interval": board.interval,
                            "act": "refused",
                            "at": list(here),
                            "own": [int(num[here]), int(s[here])],
                            "incoming": [int(far_num[here]), int(far_s[here])],
                        }
                    )
    holes = (new_num < den) & (after < 1)
    for at in zip(*np.nonzero(holes), strict=True):
        here = (int(at[0]), int(at[1]), int(at[2]))
        new_num[here], new_s[here] = den, 0
        LOG.append({"interval": board.interval, "act": "hole", "at": list(here)})
    H2["num"], H2["s"] = new_num, new_s


def fresh(
    tmp: Path, cube: int, intervals: int, births: bool, clicks: bool, lines: list[dict[str, Any]] | None
) -> Lattice:
    world_files.REPOSITORY_ROOT = tmp
    board = Lattice(
        load_world(bare_torus(tmp, cube, intervals)), output=None if lines is None else lines.append
    )
    if not births:
        meeting_board.child_of = lambda *a: ()  # no list affordable: no birth, the bodies' clicks alone
    else:
        meeting_board.child_of = REAL_CHILD_OF
    if not clicks:
        board.closed_after = lambda kept: setattr(board, "tick", board.tick + 1)  # type: ignore[method-assign]
    return board


REAL_CHILD_OF = meeting_board.child_of


def within_one_link(
    shares: np.ndarray, at: tuple[int, int, int], shape: tuple[int, ...]
) -> tuple[int, int, int]:
    """(the share at the Node, within one Link (7 Nodes), over the board), Python's integers."""
    total = int(np.asarray(shares, dtype=object).sum())
    here = int(shares[at])
    near = here
    for axis in range(AXES):
        for side in (1, -1):
            there = list(at)
            there[axis] = (there[axis] + side) % shape[axis]
            near += int(shares[tuple(there)])
    return here, near, total


def spread(cube: int, intervals: int, ride_on: bool, clicks: bool, out: Any) -> dict[str, Any]:
    """(ii) and (iii): the pair laid by hand at the cube's centre, the share at the Node, within one Link and over the board per interval; the rides and the holes; the clicks' credits with the decoder's solve."""
    tmp = Path(os.environ["TMPDIR"]) / f"h2_{MODE}_{cube}_{int(ride_on)}_{int(clicks)}_{DELTA}"
    tmp.mkdir(parents=True, exist_ok=True)
    lines: list[dict[str, Any]] = []
    board = fresh(tmp, cube, intervals, False, clicks, lines)
    index, num, s = point_family(board)
    activate(board, index)
    centre = (cube // 2, cube // 2, cube // 2)
    lay_pair(board, index, centre, 1)
    unit = 3 * board.world.quantum_action * s
    LOG.clear()
    rows = []
    before = floors_of(board, index, unit)
    began = time.perf_counter()
    for _ in range(intervals):
        board.step()
        after = floors_of(board, index, unit)
        if ride_on:
            ride(board, before, after)
            after = floors_of(board, index, unit)
        before = after
        shares = board.share_of(index)[0]
        here, near, total = within_one_link(shares, centre, board.shape)
        paired = int((H2["num"] < H2["den"]).sum()) if H2["active"] else 0
        rows.append(
            {
                "interval": board.interval,
                "at": here / unit,
                "one_link": near / unit,
                "board": total / unit,
                "paired_nodes": paired,
                "support": int((np.asarray(shares, dtype=object) != 0).sum()),
            }
        )
    seconds = time.perf_counter() - began
    credits = [row for row in lines if row["event"] == "credit"]
    decoded = [decode(row, num, board.families[index].pair[1], centre, board.shape) for row in credits]
    found = {
        "mode": MODE,
        "cube": cube,
        "intervals": intervals,
        "ride": ride_on,
        "clicks": clicks,
        "delta": DELTA,
        "pair": [num, s],
        "unit": unit,
        "rows": rows,
        "log": list(LOG),
        "credits": decoded,
        "refusals": sum(1 for row in lines if row["event"] == "refused"),
        "seconds": round(seconds, 1),
    }
    out.write(json.dumps(found) + "\n")
    return found


def decode(
    row: dict[str, Any], num: int, den: int, centre: tuple[int, int, int], shape: tuple[int, ...]
) -> dict[str, Any]:
    """The decoder's solve on one credit: x = 3 cos omega / SUM_a cos k_a from the point and the three momentum pairs, against num / den."""
    place = int(row["node_detector"]) if isinstance(row["node_detector"], int) else None
    at = [int(v) for v in np.unravel_index(place, shape)] if place is not None else None
    distance = None
    if at is not None:
        distance = sum(
            min(abs(a - c), s - abs(a - c)) for a, c, s in zip(at, centre, shape, strict=True)
        )
    readings = row.get("readings", {}) if isinstance(row.get("readings"), dict) else {}
    point = row.get("point", readings.get("point"))
    momentum = row.get("momentum")
    identity, beat = row.get("identity", readings.get("identity")), row.get("beat", readings.get("beat"))

    def as_pairs(value: Any) -> list[tuple[int, int] | None]:
        if value is None:
            return [None]
        if isinstance(value, list) and len(value) == 2 and all(isinstance(v, int) for v in value):
            return [(value[0], value[1])]
        return [None if v is None else (v[0], v[1]) for v in value]

    xs: list[float | None] = []
    if point is not None and isinstance(momentum, list) and len(momentum) == 3:
        points = as_pairs(point)
        axes = []
        for entry in momentum:
            if entry is None:
                axes.append(None)
            elif len(entry) == 3 and all(isinstance(v, int) for v in entry):
                axes.append([(entry[1], entry[2])])
            else:
                axes.append(
                    as_pairs(entry[1:])
                    if all(isinstance(v, int) for v in entry[1:])
                    else [None if v is None else (v[0], v[1]) for v in entry[1:]]
                )
        for line, cosine in enumerate(points):
            if cosine is None or any(a is None for a in axes):
                xs.append(None)
                continue
            total = 0.0
            ok = True
            for a in axes:
                pair = a[line] if len(a) > line else a[0]
                if pair is None or pair[1] == 0:
                    ok = False
                    break
                total += pair[0] / pair[1]
            xs.append(3 * (cosine[0] / cosine[1]) / total if ok and total else None)
    found_x = [v for v in xs if v is not None]
    x = sum(found_x) / len(found_x) if found_x else None
    return {
        "interval": row["interval"],
        "at": at,
        "distance": distance,
        "identity": identity,
        "point": point,
        "momentum": momentum,
        "beat": beat,
        "x": x,
        "x_lines": xs,
        "target": num / den,
        "proper": row.get("proper"),
        "windows": row.get("windows"),
    }


def run_back(cube: int, intervals: int, births: bool, out: Any) -> dict[str, Any]:
    """(iv): forward through rides, holes and clicks (and main's one-Node births where `births`, the pair set at the birth Node), then back with the pair arrays restored from the log, the states compared bit for bit."""
    tmp = Path(os.environ["TMPDIR"]) / f"h2_back_{MODE}_{cube}_{int(births)}"
    tmp.mkdir(parents=True, exist_ok=True)
    lines: list[dict[str, Any]] = []
    board = fresh(tmp, cube, intervals, births, True, lines)
    index, num, s = point_family(board)
    activate(board, index)
    centre = (cube // 2, cube // 2, cube // 2)
    if not births:
        lay_pair(board, index, centre, 1)
    unit = 3 * board.world.quantum_action * s
    LOG.clear()
    states, history = [board_state(board)], {}
    before = floors_of(board, index, unit)
    for _ in range(intervals):
        history[board.interval + 1] = (
            H2["num"].copy(),
            H2["s"].copy(),
        )  # the pair the step of this interval reads
        board.step()
        for row in lines:
            if row["event"] == "birth" and row["interval"] == board.interval:
                for node_at in row["nodes"]:
                    here = tuple(int(v) for v in node_at)
                    if H2["num"][here] == H2["den"]:
                        set_pair(here, num, s)
                        LOG.append({"interval": board.interval, "act": "birth", "at": list(here)})
        after = floors_of(board, index, unit)
        ride(board, before, after)
        before = floors_of(board, index, unit)
        states.append(board_state(board))
    pairs_end = (H2["num"].copy(), H2["s"].copy())
    board.output = None
    matched = 0
    for k in range(intervals):
        H2["num"], H2["s"] = history[board.interval]
        board.step_inverse()
        matched += same_state(board_state(board), states[intervals - 1 - k])
    found = {
        "mode": MODE,
        "cube": cube,
        "intervals": intervals,
        "births": births,
        "match": matched,
        "interval_after": board.interval,
        "credits": sum(1 for r in lines if r["event"] == "credit"),
        "births_count": sum(1 for r in lines if r["event"] == "birth"),
        "rides": sum(1 for r in LOG if r["act"] == "ride"),
        "holes": sum(1 for r in LOG if r["act"] == "hole"),
        "refused_rides": sum(1 for r in LOG if r["act"] == "refused"),
        "paired_at_end": int((pairs_end[0] < H2["den"]).sum()),
        "log": list(LOG)[:200],
    }
    out.write(json.dumps(found) + "\n")
    return found


def birth_rate(cube: int, intervals: int, out: Any) -> dict[str, Any]:
    """(i): main's path with every read's number logged; the acceptance's hits under the modular draw (num = q mod den, s = (q div den) mod den) and under the floor draw (num = q mod den, s the largest leg below, accepted where exact)."""
    tmp = Path(os.environ["TMPDIR"]) / f"h2_rate_{cube}"
    tmp.mkdir(parents=True, exist_ok=True)
    lines: list[dict[str, Any]] = []
    numbers: list[int] = []
    real_read = digits.read_of

    def logged_read(board: Lattice, reads: Any, label: str) -> int:
        found = real_read(board, reads, label)
        numbers.append(found)
        return found

    digits.read_of = logged_read
    meeting_board.read_of = logged_read  # the close imports the name
    bound_body.read_of = logged_read
    board = fresh(tmp, cube, intervals, True, True, lines)
    unit, den = board.credit.units[board.world.seed], board.families[board.world.seed].pair[1]
    for _ in range(intervals):
        board.step()
    digits.read_of = meeting_board.read_of = bound_body.read_of = real_read
    points = {(p[1], p[2]) for p in circle_points(den)}
    hits_mod = hits_floor = hits_floor_axis = 0
    bits = []
    for n in numbers:
        q = n // unit
        bits.append(q.bit_length())
        a, b = q % den, (q // den) % den
        if a * a + b * b == den * den and a > 0 and b > 0:
            hits_mod += 1
        leg = largest_below(den * den - a * a)
        if leg * leg == den * den - a * a:
            if a > 0 and leg > 0:
                hits_floor += 1
            else:
                hits_floor_axis += 1
    found = {
        "cube": cube,
        "intervals": intervals,
        "den": den,
        "unit": unit,
        "reads": len(numbers),
        "quotient_bits_min_max": [min(bits, default=0), max(bits, default=0)],
        "births_main": sum(1 for r in lines if r["event"] == "birth"),
        "credits_main": sum(1 for r in lines if r["event"] == "credit"),
        "hits_modular": hits_mod,
        "hits_floor": hits_floor,
        "hits_floor_axis": hits_floor_axis,
        "circle_points": len(points),
        "p_modular": len(points) / den**2,
        "p_floor": len(points) / den,
    }
    out.write(json.dumps(found) + "\n")
    return found


def main(argv: list[str]) -> None:
    part, cube, intervals = (
        argv[0],
        int(argv[1]) if len(argv) > 1 else 3,
        int(argv[2]) if len(argv) > 2 else 120,
    )
    out = sys.stdout
    if part == "rate":
        birth_rate(cube, intervals, out)
    elif part == "spread":
        spread(cube, intervals, False, False, out)
    elif part == "ride":
        spread(cube, intervals, True, False, out)
    elif part == "clicks":
        spread(cube, intervals, True, True, out)
    elif part == "back":
        run_back(cube, intervals, False, out)
    elif part == "back_births":
        run_back(cube, intervals, True, out)
    else:
        raise SystemExit(f"unknown part {part!r}")


if __name__ == "__main__":
    main(sys.argv[1:])
