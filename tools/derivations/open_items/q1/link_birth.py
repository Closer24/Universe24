"""Hand q1 (2026-10-25): the birth on the Link as one act of the Node, measured on the branch's engine with no change to src/ (the board's own close `meeting_board.closed` replaced from this script by a Link close built from the engine's own acts: `hole.take_of`, `lay.laid`, `act.born_items`, `act.click`).

The Link close (ALGEBRA.md, The Node: "the read of each Link once ..., a whole quantum from each end laying a child at each end at opposite senses and taking from the light at each end what the lay books, refused by name where the light cannot pay"): at the end of the interval, on the state the interval started from, every +a Link whose two ends each hold a whole quantum of light (the floor of the share over W_c at or above 1 at both ends) and whose lift's walls fit is a meeting; the orientation, which end lays the + child, by one of two rules: `label`, the + child at the +a end (the owner's "the orientation a label"), or `current`, the + child at the end the light's current F_ij = num (now_i before_j - before_i now_j) flows into at the interval's start (the Link's own odd reading, antisymmetric in its two ends; a meeting with F_ij = 0 is refused by name, no end distinguished); each end takes one child's wall 3 T s from its own light by the exact take (`take_of`, summed where a Node meets on several Links, the Node's Links all refused where the full stop cannot pay), then the holes through the one lay act and the children through the one click act, the + children on the lift's record 0 and the - children on its record 1 (so that the engine's one row per record gives the + row and the - row, and their sum is the one shared row). The whether is not drawn here (every meeting Link meets), a deviation from the law's letter named in the report.

Measured: (A) the hole seed on the bare 3-cube at den 1,021, invariant under the 48 about the origin, run under each rule: the count of the 48 under which the board's image equals the image's board bit for bit at every interval (`carried`, `apart` of tests/test_the_board_is_the_cube_48.py), with the sense-exchanged comparison beside it, the births, the refusals and the current at every meeting Link; (B) an asymmetric seed (the hole seed plus one quantum of light at (1, 0, 0)) and the same seed carried by each of the 47 non-trivial elements before the run: the count of elements under which the carried seed's run is the carried run bit for bit; (C) the run back over the run's length; (D) the charge, SUM W over the board; (E) the one row at the birth Link's two ends over the intervals: the + record's row, the - record's row, their sum, the free row, in units of the write's wall; (F) the self-read at the + child's Node: the sum of every row but its own against the sum of all rows.

Usage: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/q1/link_birth.py [intervals] ; writes link_birth.json beside it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from event_universe import meeting_board, records, registry, seed, world_files  # noqa: E402
from event_universe.act import affordable, born_items, click  # noqa: E402
from event_universe.core.ports import AXES, arrival  # noqa: E402
from event_universe.core.rule3 import wall_of  # noqa: E402
from event_universe.hole import moved, take_of  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.loader.derived import count_wall  # noqa: E402
from event_universe.loader.universe import SIGN  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws import board_state, same_state  # noqa: E402
from tests.laws_universe import bare_torus  # noqa: E402
from tests.test_the_board_is_the_cube_48 import (  # noqa: E402
    IDENTITY,
    apart,
    axis_map,
    carried,
    cube_48,
    turns_of,
)

OUT = Path(__file__).resolve().parent
TMP = Path("/dev/shm/tmp/q1_link_birth")
Node = tuple[int, int, int]

ENGINE_CLOSE = meeting_board.closed
ENGINE_SEED = seed.uniform_seed  # bound once: the seeders below call the engine's own, never the one installed in its place
DEN = 1021


def currents_of(board: Lattice, index: int, lines: list[records.Record]) -> list[np.ndarray]:
    """F on every +a Link of every Node from the given lines of the light's record: num (now_i before_j - before_i now_j), the inflow into i from j (reports' F_ij); antisymmetric: F_ji = -F_ij."""
    num = board.families[index].pair[0]
    now = np.asarray(lines[0].now, dtype=object)
    before = np.asarray(lines[0].before, dtype=object)
    found = []
    for a in range(AXES):
        found.append(num * (now * arrival(before, a, 1) - before * arrival(now, a, 1)))
    return found


def neighbour(at: Node, axis: int, side: int, shape: tuple[int, ...]) -> Node:
    found = list(at)
    found[axis] = (found[axis] + side) % shape[axis]
    return (found[0], found[1], found[2])


def link_close(board: Lattice, begun: Any, rule: str, log: list[dict[str, Any]]) -> None:
    """The Link close in place of the Node close (the module's sentence)."""
    index = board.world.seed
    if index is None:
        return
    family = board.families[index]
    unit = board.credit.units[index]
    span = records.record_slice(family, 0)
    stepped = [(state.lines, state.phases) for state in board.states]
    for state, lines, phases in zip(board.states, begun[0], begun[2], strict=True):
        state.lines, state.phases = lines, phases  # the read on the interval's start
    try:
        shares, frozen = board.share_of(index)
        start_lines = list(board.states[index].lines[span])
        currents = currents_of(board, index, start_lines)
        meetings: list[tuple[Node, Node, int, Any, int]] = []  # (plus end, minus end, axis, table, F)
        refusals: list[dict[str, Any]] = []
        for at in np.ndindex(*board.shape):
            here = (int(at[0]), int(at[1]), int(at[2]))
            if bool(frozen[here]) or int(shares[here]) < unit:
                continue
            for a in range(AXES):
                there = neighbour(here, a, 1, board.shape)
                if bool(frozen[there]) or int(shares[there]) < unit:
                    continue
                whole = min(int(shares[here]) // unit, int(shares[there]) // unit)
                tables = affordable(
                    board.families,
                    index,
                    board.world.quantum_action,
                    int(shares[here]) + int(shares[there]),
                    2 * max(whole, 1),
                )  # the two children's walls within the two ends' energy, one quantum from each end
                if not tables:
                    continue
                table = tables[0]  # den 1,021: the one lift, certain; the quotient's pick not drawn here
                f = int(currents[a][here])  # the inflow into `here` from `there`
                if rule == "label":
                    plus, minus = there, here  # the + child at the +a end
                elif rule == "current":
                    if f == 0:
                        refusals.append(
                            {"interval": board.interval, "link": [list(here), list(there)], "cause": "orientation", "F": 0}
                        )
                        continue
                    plus, minus = (here, there) if f > 0 else (there, here)  # the + child where the light flows in
                else:
                    raise ValueError(rule)
                meetings.append((plus, minus, a, table, f))
    finally:
        for state, (lines, phases) in zip(board.states, stepped, strict=True):
            state.lines, state.phases = lines, phases  # the write on the state the step left
    # the takes: per Node the walls of its meeting Links summed; a Node that cannot pay refuses all its Links; until stable
    child_wall = {}
    alive = list(meetings)
    while True:
        owed: dict[Node, int] = {}
        for plus, minus, _a, table, _f in alive:
            for end, (out, _sense) in zip((plus, minus), table, strict=True):
                owed[end] = owed.get(end, 0) + count_wall(board.families[out], board.world.quantum_action)
        takes = {at: take_of(board, index, span, at, walls) for at, walls in owed.items()}
        broke = {at for at, found in takes.items() if found.taken < found.walls}
        if not broke:
            break
        for at in broke:
            refusals.append({"interval": board.interval, "node": list(at), "cause": "stop", "taken": takes[at].taken, "walls": takes[at].walls})
        alive = [m for m in alive if m[0] not in broke and m[1] not in broke]
    lines = list(board.states[index].lines[span])
    targets = {at: moved(lines, at, found.levels) for at, found in takes.items()} if alive else {}
    items = []
    for at, target in targets.items():
        here = board.mask((at,))
        for number, line, after in zip(range(span.start, span.stop), lines, target, strict=True):
            change = (np.where(here, after.now - line.now, 0), np.where(here, 0, 0))
            laid(board, index, number, change, None, None, here)
    for plus, minus, a, table, f in alive:
        children = born_items(board.families, table, (plus,))
        # the table is ((k, -1), (k, 1)): record 0 the sense -1, record 1 the sense 1 as the engine lays it;
        # here the + child on record 1 at `plus` and the - child on record 0 at `minus`
        for child in children:
            end = plus if child.sense > 0 else minus
            items.append(type(child)(child.family, 1, (end,), child.pair, sense=child.sense, record=child.record))
        board.closes[plus] += 1
        board.closes[minus] += 1
        log.append(
            {
                "event": "link_birth",
                "interval": board.interval,
                "axis": a,
                "plus": list(plus),
                "minus": list(minus),
                "F_into_plus_from_minus": f if plus == minus_end_here(plus, minus, a, board.shape) else -f,
                "children": [board.families[out].name for out, _s in table],
                "taken": [takes[plus].taken, takes[minus].taken],
                "walls": [takes[plus].walls, takes[minus].walls],
            }
        )
    for r in refusals:
        log.append({"event": "refused", **r})
    if items:
        click(board, items)


def minus_end_here(plus: Node, minus: Node, a: int, shape: tuple[int, ...]) -> Node:
    """The -a end of the Link (the Node `here` the current F was read at): `minus` where the + child stands at the +a end, else `plus`."""
    return plus if neighbour(plus, a, 1, shape) == minus else minus


def install(rule: str, log: list[dict[str, Any]]) -> None:
    meeting_board.closed = lambda board, begun: link_close(board, begun, rule, log)


def hole_plus_one(at: Node) -> Any:
    """The hole seed (the sea at the drift on every Node but the origin, `seed.uniform_seed`) plus one quantum more at `at`: an asymmetric seed."""

    def laid_seed(board: Lattice, index: int) -> None:
        from event_universe.emission import emitted_lines

        ENGINE_SEED(board, index)
        family, drift = board.families[index], seed.drift_of(board.world.quantum_action)
        first, zeros = records.record_slice(family, 0).start, records.zeros(board.shape, board.kind)
        mask = board.mask((at,))
        for line in emitted_lines(family):
            laid(board, index, first + line, (np.where(mask, drift, 0), zeros), None, None, mask)

    return laid_seed


def board_of(folder: Path, seeder: Any, intervals: int) -> tuple[Lattice, list[dict[str, Any]]]:
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    if seeder is not None:
        seed_was = seed.uniform_seed
        seed.uniform_seed = seeder
    lines: list[dict[str, Any]] = []
    try:
        path = bare_torus(folder, 3, intervals)
        if DEN != 1021:
            from tests.laws_universe import SMALL

            (folder / "u.json").write_text(json.dumps({"integers": {**SMALL["integers"], "den": DEN}}), "utf-8")
        board = Lattice(load_world(path), output=lines.append)
    finally:
        if seeder is not None:
            seed.uniform_seed = seed_was
    return board, lines


def conjugated(board: Lattice, state: list[Any]) -> list[Any]:
    """The sense exchange C on a carried state (the module's sentence): every plane's im line negated with its remainder reflected about the half wall, (w - r) mod w, and the lift's two records exchanged (record 0 the - children, record 1 the + children); the holder of the sign's rows beyond the free row negated (levels, the remainders and the write remainders reflected) and exchanged; the phase rows exchanged with their counts and Phi negated; the free row and the light untouched."""
    found = []
    for index, (lines, writes, phases) in enumerate(state):
        family = board.families[index]
        lines, writes, phases = list(lines), list(writes), list(phases)
        if family.plane and not family.held and lines and lines[0] is not None:
            wall = wall_of(family.pair[1], board.world.node_clock, board.unit)
            per = family.parts * family.width
            rows = len(lines) // per
            out = list(lines)
            for r in range(rows):
                src = (1 - r) if rows == 2 else r
                for k in range(per):
                    now, before, rem = lines[src * per + k]
                    if k % 2 == 1:
                        now, before = -np.asarray(now, dtype=object), -np.asarray(before, dtype=object)
                        rem = np.mod(wall - np.asarray(rem, dtype=object), wall)
                    out[r * per + k] = (now, before, rem)
            lines = out
        elif family.held and family.wronskian:
            width = family.width
            rows = len(lines) // width
            wall = wall_of(family.pair[1], board.world.node_clock, board.unit)
            divided = records.divided_walls(family, board.fixed_walls[index], board.world.node_clock)
            out_l, out_w = list(lines), list(writes)
            for r in range(1, rows):
                src = r if rows != 3 else (3 - r)
                for k in range(width):
                    now, before, rem = lines[src * width + k]
                    out_l[r * width + k] = (
                        -np.asarray(now, dtype=object),
                        -np.asarray(before, dtype=object),
                        np.mod(wall - np.asarray(rem, dtype=object), wall),
                    )
                    dw = np.asarray(divided[src * width + k], dtype=object)
                    out_w[r * width + k] = np.mod(dw - np.asarray(writes[src * width + k], dtype=object), dw)
            lines, writes = out_l, out_w
            out_p = list(phases)
            for r in range(1, rows):
                src = r if rows != 3 else (3 - r)
                row = phases[src]
                if not row:
                    out_p[r] = row
                    continue
                new = list(row)
                for a in range(AXES):
                    now, before, rem = row[2 * AXES + a]
                    new[2 * AXES + a] = (-np.asarray(now, dtype=object), -np.asarray(before, dtype=object), rem)
                now, before, rem = row[-1]
                new[-1] = (-np.asarray(now, dtype=object), -np.asarray(before, dtype=object), rem)
                out_p[r] = new
            phases = out_p
        found.append((lines, writes, phases))
    return found


def charge_of(board: Lattice) -> int:
    total = 0
    for k, family in enumerate(board.families):
        if family.plane and not family.held:
            for r in range(registry.records_of(family, board.states[k].lines)):
                total += int(np.asarray(records.wronskian(board.lines_of(k, r), True), dtype=object).sum())
    return total


def row_reading(board: Lattice, at: Node) -> dict[str, Any]:
    """The holder of the sign's rows at `at`: per row its time level and write remainder over the wall, in units of the wall (level + remainder / wall - origin), and the sums."""
    sign = next(k for k, f in enumerate(board.families) if f.held and f.wronskian)
    family, state = board.families[sign], board.states[sign]
    width = family.width
    rows = registry.records_of(family, state.lines)
    found = {}
    values = []
    divided = records.divided_walls(family, board.fixed_walls[sign], board.world.node_clock)
    for r in range(rows):
        level = int(state.lines[r * width].now[at])
        rem = int(np.asarray(state.write_remainders[r * width], dtype=object)[at])
        wall_arr = np.asarray(divided[r * width], dtype=object)
        wall = int(wall_arr[at]) if wall_arr.ndim else int(wall_arr)
        origin = wall // 2
        fine = level * wall + (rem - origin)  # the row in units of 1 / wall, an integer
        values.append(fine)
        found[f"row{r}"] = {"level": level, "remainder_less_origin": rem - origin, "wall": wall, "float_check": round(fine / wall, 6)}
    found["one_row_over_wall"] = (sum(values), wall)
    found["rows_but_own_for_each_over_wall"] = {f"record{r - 1}": (sum(values) - values[r], wall) for r in range(1, rows)}
    found["own_share_of_one_row_for_each"] = {
        f"record{r - 1}": (values[r], sum(values)) for r in range(1, rows)
    }  # the record's own write over the one row's reading at the Node, two integers
    return found


def run_a(rule: str, intervals: int) -> dict[str, Any]:
    """(A) the hole seed, invariant under the 48 about the origin, under the Link close with `rule`: the 48 count per interval, plain and sense-exchanged, the births and the charge; (C) the run back; (E) the row at the first birth Link's ends."""
    log: list[dict[str, Any]] = []
    install(rule, log)
    board, lines = board_of(TMP / f"a_{rule}", None, intervals)
    group = cube_48()
    turns = turns_of(board, None)
    states = [board_state(board)]
    per_interval = []
    first_link = None
    rows_course = []
    for _ in range(intervals):
        board.step()
        turns = turns_of(board, turns)
        own = carried(board, IDENTITY)
        held = [m for m in group if not apart(carried(board, m, turns), own)]
        conj = conjugated(board, own)
        held_c = [m for m in group if not apart(carried(board, m, turns), conj)]
        births = [x for x in log if x["event"] == "link_birth" and x["interval"] == board.interval]
        refused = [x for x in log if x["event"] == "refused" and x["interval"] == board.interval]
        if births and first_link is None:
            first_link = (tuple(births[0]["plus"]), tuple(births[0]["minus"]))
        if first_link is not None:
            rows_course.append(
                {"interval": board.interval, "plus": row_reading(board, first_link[0]), "minus": row_reading(board, first_link[1])}
            )
        per_interval.append(
            {
                "interval": board.interval,
                "held_of_48": len(held),
                "held_with_sense_exchange_of_48": len(held_c),
                "held_elements_signs": sorted({tuple(axis_map(m)[1]) for m in held}),
                "births": len(births),
                "birth_axes": sorted({b["axis"] for b in births}),
                "F_at_births": [b["F_into_plus_from_minus"] for b in births],
                "refused": [(r.get("cause"), r.get("F", r.get("taken"))) for r in refused][:8],
                "charge_sum_W": charge_of(board),
            }
        )
        states.append(board_state(board))
    back = 0
    for k in range(intervals):
        board.step_inverse()
        back += same_state(board_state(board), states[intervals - 1 - k])
    meeting_board.closed = ENGINE_CLOSE
    return {
        "rule": rule,
        "per_interval": per_interval,
        "run_back_match": f"{back} of {intervals}",
        "interval_after_back": board.interval,
        "total_link_births": sum(1 for x in log if x["event"] == "link_birth"),
        "first_link": first_link,
        "rows_at_first_link": rows_course,
        "engine_lines_events": sorted({str(x.get("event")) for x in lines}),
    }


def run_b(rule: str, intervals: int, at: Node = (1, 0, 0)) -> dict[str, Any]:
    """(B) the hole seed plus one quantum at `at`, run under `rule`, against the same seed carried by each of the 47 non-trivial elements before its run: the count of elements under which the carried seed's run is the carried run bit for bit at every interval."""
    group = [m for m in cube_48() if not np.array_equal(m, IDENTITY)]
    log: list[dict[str, Any]] = []
    install(rule, log)
    board, _ = board_of(TMP / f"b_{rule}_base", hole_plus_one(at), intervals)
    for _ in range(intervals):
        board.step()
    held, broken_at = [], {}
    births_base = [x for x in log if x["event"] == "link_birth"]
    for number, m in enumerate(group):
        image = tuple(int(v) for v in np.mod(m @ np.array(at), 3))
        log_m: list[dict[str, Any]] = []
        install(rule, log_m)
        other, _ = board_of(TMP / f"b_{rule}_{number}", hole_plus_one(image), intervals)
        log_base: list[dict[str, Any]] = []
        install(rule, log_base)
        base, _ = board_of(TMP / f"b_{rule}_base2", hole_plus_one(at), intervals)
        turns = turns_of(base, None)
        ok = True
        for _ in range(intervals):
            base.step()
            other.step()
            turns = turns_of(base, turns)
            found = apart(carried(base, m, turns), carried(other, IDENTITY))
            if found:
                ok = False
                broken_at[str(m.tolist())] = base.interval
                break
        if ok:
            held.append(m)
    meeting_board.closed = ENGINE_CLOSE
    return {
        "rule": rule,
        "seed": f"hole seed plus one quantum at {list(at)}",
        "held_of_47": len(held),
        "held_of_48_with_identity": len(held) + 1,
        "held_signs_and_permutations": sorted(str(axis_map(m)) for m in held),
        "broken_first_interval": broken_at,
        "base_run_link_births": [(b["interval"], b["axis"], b["plus"], b["minus"], b["F_into_plus_from_minus"]) for b in births_base],
        "base_run_refusals": [(r["interval"], r.get("cause"), r.get("F", r.get("taken"))) for r in log if r["event"] == "refused"][:12],
    }


def main() -> None:
    global DEN
    intervals = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    modes = sys.argv[2] if len(sys.argv) > 2 else "AB"
    DEN = int(sys.argv[3]) if len(sys.argv) > 3 else 1021
    TMP.mkdir(parents=True, exist_ok=True)
    found: dict[str, Any] = {"den": DEN, "cube": 3, "intervals": intervals}
    for rule in ("label", "current") if "A" in modes else ():
        found[f"A_{rule}"] = run_a(rule, intervals)
        print(rule, "A: held of 48 per interval", [x["held_of_48"] for x in found[f"A_{rule}"]["per_interval"]])
        print(rule, "A: with sense exchange", [x["held_with_sense_exchange_of_48"] for x in found[f"A_{rule}"]["per_interval"]])
        print(rule, "A: births per interval", [x["births"] for x in found[f"A_{rule}"]["per_interval"]], "run back", found[f"A_{rule}"]["run_back_match"])
        print(rule, "A: charge", [x["charge_sum_W"] for x in found[f"A_{rule}"]["per_interval"]])
        print(rule, "A: F at births", [x["F_at_births"] for x in found[f"A_{rule}"]["per_interval"] if x["births"]][:3])
    for rule in ("label", "current") if "B" in modes else ():
        found[f"B_{rule}"] = run_b(rule, intervals)
        print(rule, "B: held of 47", found[f"B_{rule}"]["held_of_47"], "births", found[f"B_{rule}"]["base_run_link_births"][:6])
    (OUT / f"link_birth_{modes}_{DEN}.json").write_text(json.dumps(found, indent=1, default=str))


if __name__ == "__main__":
    main()
