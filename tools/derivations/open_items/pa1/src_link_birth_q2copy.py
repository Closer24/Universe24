"""The Link birth and the cube's 48 (hand q2, 2026-10-25; ALGEBRA.md, The Node: "the read of each Link once ..., a whole quantum from each end laying a child at each end at opposite senses and taking from the light at each end what the lay books, refused by name where the light cannot pay").

A measurement on the branch's engine with no edit of src/: the bare 3-cube torus at a den (1,021 by default) under the engine's own hole seed, every act of the interval the engine's (`Lattice.advanced_to_the_close`, `Lattice.closed_after` with the board's one-Node meetings emptied, as tests/laws_universe.node_toy empties them), and the close of the Link added test-side (`link_close`): every Link (i, j) read once from its +a end, a meeting where both ends hold a whole quantum of the light and no other Link of either end meets this close, the one child per end at opposite senses, the exact take of one child's wall at each end (`hole.take_of`, every take read before any write), the children laid through the engine's one click act (`act.click` over `take.Item`, the lays logged for the run back), refused by name 'stop' and 'lay' as the board's own close refuses, and the orientation (which end takes the + child) by the variant named on the command line:

  label     the + child at the end that owns the Link through its +a Port (the former hands' form: the axis a label);
  current   the + child at the end the light's Link current flows into at the interval's start, F_ij = num (now_i before_j - before_i now_j), the Link's own Wronskian, odd under the exchange of the ends; refused 'tie' where F_ij = 0;
  gradient  the + child at the end of the lower level now, now_i - now_j the odd quantity; refused 'tie' at equal levels.

Measured per interval: the meetings and their refusals by name, the current and the level difference on every meeting Link, the count of the cube's 48 under which the board carried equals the board bit for bit (tests/test_the_board_is_the_cube_48.carried, apart, turns_of), plain and with the senses exchanged (C: every plane's im line negated, the sign holder's rows negated, the remainders reflected about their lay as the test reflects an odd line's), the pair's charge over the board, and the run back from the end to the start (MATCH or MISS at the first interval that differs).

Run from the worktree root:

    PYTHONPATH=src python tools/derivations/q2/link_birth.py --orientation current --intervals 12 --out tools/derivations/q2/link_birth.current.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
for place in (str(ROOT), str(ROOT / "src")):
    if place not in sys.path:
        sys.path.insert(0, place)

import numpy as np  # noqa: E402

from event_universe import conversion, hole, meeting_back, meeting_board, records, registry, world_files  # noqa: E402
from event_universe.act import click  # noqa: E402
from event_universe.core.ports import AXES, arrival  # noqa: E402
from event_universe.core.rule3 import division_forward, wall_of  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.loader.derived import count_wall  # noqa: E402
from event_universe.take import Item, below_quantum  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import SMALL  # noqa: E402
from tests.test_the_board_is_the_cube_48 import IDENTITY, apart, carried, cube_48, turns_of  # noqa: E402

Node = tuple[int, int, int]


def bare_board(folder: Path, den: int, intervals: int, lines: list[dict[str, Any]]) -> Lattice:
    """The tests' small universe at `den` on the bare 3-cube torus, the engine's own hole seed, the one-Node meetings emptied (the Link close stands in their place), the output lines kept."""
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    (folder / "u.json").write_text(json.dumps({"integers": {**SMALL["integers"], "den": den}}), "utf-8")
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": intervals}
    (folder / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    meeting_board.meetings = lambda b, i, s, f: []  # the board's one-Node births emptied, test-side
    return Lattice(load_world(folder / "bare.json"), output=lines.append)


def neighbour(at: Node, axis: int, shape: tuple[int, ...]) -> Node:
    """The Node through the +a Port of `at` on the torus."""
    there = list(at)
    there[axis] = (there[axis] + 1) % shape[axis]
    return there[0], there[1], there[2]


def link_close(board: Lattice, begun: Any, orientation: str, child: int, log: list[dict[str, Any]]) -> None:
    """The Link close (the module's sentence): read on the interval's start, written on the state the step left."""
    index = board.world.seed
    light, unit = board.families[index], board.credit.units[index]
    span = records.record_slice(light, 0)
    num = light.pair[0]
    den = board.families[child].pair[1]
    wall_child = count_wall(board.families[child], board.world.quantum_action)
    stepped = [(s.lines, s.phases) for s in board.states]
    for s, lines, phases in zip(board.states, begun[0], begun[2], strict=True):
        s.lines, s.phases = lines, phases
    try:
        shares, frozen = board.share_of(index)
        line = board.states[index].lines[span.start]
        now, before = np.asarray(line.now, dtype=object), np.asarray(line.before, dtype=object)
    finally:
        for s, (lines, phases) in zip(board.states, stepped, strict=True):
            s.lines, s.phases = lines, phases
    whole = {at: int(division_forward(int(shares[at]), unit, 0)[0]) for at in np.ndindex(*board.shape)}
    meeting = []
    for axis in range(AXES):
        now_far, before_far = arrival(now, axis, 1), arrival(before, axis, 1)
        for at in np.ndindex(*board.shape):
            here = (int(at[0]), int(at[1]), int(at[2]))
            there = neighbour(here, axis, board.shape)
            if whole[here] < 1 or whole[there] < 1 or bool(frozen[here]) or bool(frozen[there]):
                continue
            current = num * (int(now[here]) * int(before_far[here]) - int(before[here]) * int(now_far[here]))
            gradient = int(now[here]) - int(now_far[here])
            meeting.append((here, there, axis, current, gradient))
    entries: list[dict[str, Any]] = []
    oriented = []  # (entry, plus, minus) for every meeting Link with an orientation
    for here, there, axis, current, gradient in meeting:
        entry: dict[str, Any] = {
            "interval": board.interval,
            "link": [list(here), list(there)],
            "axis": axis,
            "current": current,
            "gradient": gradient,
            "whole": [whole[here], whole[there]],
        }
        entries.append(entry)
        if orientation == "label":
            plus, minus = here, there
        elif orientation == "current":
            if current == 0:
                entry["refused"] = "tie"
                continue
            plus, minus = (here, there) if current > 0 else (there, here)
        elif orientation == "gradient":
            if gradient == 0:
                entry["refused"] = "tie"
                continue
            plus, minus = (there, here) if gradient > 0 else (here, there)
        else:
            raise ValueError(orientation)
        oriented.append((entry, plus, minus))
    # the law's form: a Node takes one child per meeting Link, up to six, paid from its own light in one take,
    # refused by name where the light cannot pay for all of them (no order among a Node's Links enters), a
    # refused Node refusing every Link of its own, the partners' demands then read again until nothing moves
    alive = {id(entry): True for entry, _p, _m in oriented}
    while True:
        demand: dict[Node, list[int]] = {}
        for entry, plus, minus in oriented:
            if alive[id(entry)]:
                demand.setdefault(plus, [0, 0])[0] += 1
                demand.setdefault(minus, [0, 0])[1] += 1
        takes = {}
        refused_nodes = set()
        for at, (n_plus, n_minus) in demand.items():
            found = hole.take_of(board, index, span, at, (n_plus + n_minus) * wall_child)
            takes[at] = found
            if found.taken < found.walls:
                refused_nodes.add(at)
            else:
                for sense, n in ((1, n_plus), (-1, n_minus)):
                    if n and at not in below_quantum(board, Item(child, n, (at,), (den, den), sense=sense, record=1 if sense > 0 else 0)):
                        refused_nodes.add(at)
        moved = False
        for entry, plus, minus in oriented:
            if alive[id(entry)] and (plus in refused_nodes or minus in refused_nodes):
                alive[id(entry)] = False
                entry["refused"] = "stop" if (takes[plus].taken < takes[plus].walls or takes[minus].taken < takes[minus].walls) else "lay"
                entry["take"] = [[takes[at].taken, takes[at].walls] for at in (plus, minus)]
                moved = True
        if not moved:
            break
    born_entries = [(entry, plus, minus) for entry, plus, minus in oriented if alive[id(entry)]]
    for entry, plus, minus in born_entries:
        entry["plus"], entry["minus"] = list(plus), list(minus)
        entry["take"] = [[takes[at].levels, takes[at].taken, takes[at].walls, takes[at].excess] for at in (plus, minus)]
    takes = {at: found for at, found in takes.items() if at in demand and at not in refused_nodes and any(alive[id(e)] for e, p, m in oriented if at in (p, m))}
    items = []
    for at, (n_plus, n_minus) in demand.items():
        if at not in takes:
            continue
        if n_plus:
            items.append(Item(child, n_plus, (at,), (den, den), sense=1, record=1))
        if n_minus:
            items.append(Item(child, n_minus, (at,), (den, den), sense=-1, record=0))
    lines = list(board.states[index].lines[span])
    targets = [(at, hole.moved(lines, at, found.levels)) for at, found in sorted(takes.items())]
    for at, target in targets:  # every hole read above, written here through the one lay act
        here = board.mask((at,))
        for number, line, after in zip(range(span.start, span.stop), lines, target, strict=True):
            change = (np.where(here, after.now - line.now, 0), np.where(here, 0, 0))
            laid(board, index, number, change, None, None, here)
        board.closes[at] += 1
    if items:
        click(board, items)
    log.extend(entries)
    counted = __import__("event_universe.credit", fromlist=["count_of"]).count_of(board, index)
    if counted is not None:
        board.credit.counts[index] = counted


def conjugated(board: Lattice, state: list[Any], turns: Any) -> list[Any]:
    """The senses exchanged on a carried state (C): every plane's im line negated with its remainder reflected about its lay (the test's gauge, (w - 2 odd - r) mod w, the turn parity of the plane's own row), the sign holder's every row negated alike with its write remainders reflected about their half wall, its phase counts and its phase row negated; the volume and the light untouched."""
    found = []
    gamma, unit = board.world.node_clock, board.unit
    sign = next(i for i, f in enumerate(board.families) if f.held and f.wronskian)
    swaps = {}  # the two records' labels exchanged under C: the + child stands on the record 1 by the lay's convention, so C moves it to the record 0 and the - child to the record 1, with their rows of the sign and their phase rows
    for index, family in enumerate(board.families):
        if family.plane and not family.held and registry.records_of(family, board.states[index].lines) == 2:
            swaps[index] = (registry.row_of(board.families, board.states, index, 0), registry.row_of(board.families, board.states, index, 1))
    for index, (lines, writes, phases) in enumerate(state):
        family = board.families[index]
        wall = wall_of(family.pair[1], gamma, unit)
        lines, writes, phases = list(lines), list(writes), [list(row) for row in phases]
        if index in swaps:
            w = family.width
            lines = lines[w : 2 * w] + lines[:w] + lines[2 * w :]
        if family.held and family.wronskian:
            for r0, r1 in swaps.values():
                w = family.width
                a, b = slice(r0 * w, (r0 + 1) * w), slice(r1 * w, (r1 + 1) * w)
                lines[a], lines[b] = lines[b], lines[a]
                writes[a], writes[b] = writes[b], writes[a]
                phases[r0], phases[r1] = phases[r1], phases[r0]
        if family.plane and not family.held:
            row = registry.row_of(board.families, board.states, index, 0)
            for k, line in enumerate(lines):
                if k % 2 == 1 and line is not None:
                    record = k // (family.width)
                    parity = turns[sign][row + record] if turns and row is not None else 0
                    now, before, remainder = line
                    r = np.asarray(remainder, dtype=object)
                    lines[k] = (-now, -before, np.mod(wall - 2 * np.asarray(parity, dtype=object) - r, wall))
        if family.held and family.wronskian:
            divided = records.divided_walls(family, board.fixed_walls[index], gamma)
            for k, line in enumerate(lines):
                if line is None:
                    continue
                row = k // family.width
                parity = turns[index][row] if turns else 0
                now, before, remainder = line
                r = np.asarray(remainder, dtype=object)
                lines[k] = (-now, -before, np.mod(wall - 2 * np.asarray(parity, dtype=object) - r, wall))
                w = np.asarray(divided[k], dtype=object)
                writes[k] = np.mod(w - 2 * np.asarray(parity, dtype=object) - np.asarray(writes[k], dtype=object), w)
            for row in phases:
                if not row:
                    continue
                for a in range(AXES):
                    now, before, remainder = row[2 * AXES + a]
                    row[2 * AXES + a] = (-np.asarray(now, dtype=object), -np.asarray(before, dtype=object), remainder)
                now, before, remainder = row[-1]
                row[-1] = (-np.asarray(now, dtype=object), -np.asarray(before, dtype=object), remainder)
        found.append((lines, writes, phases))
    return found


def charge_of(board: Lattice, child: int) -> list[int]:
    """The born pair's Wronskian summed over the board per record (the charge of each child), and the sign holder's rows' k = 0 sums."""
    found = []
    state = board.states[child]
    for record in range(registry.records_of(board.families[child], state.lines)):
        w = records.wronskian(board.lines_of(child, record), True)
        found.append(int(np.asarray(w, dtype=object).sum()))
    return found


def run(den: int, intervals: int, orientation: str, out: Any, folder: Path) -> dict[str, Any]:
    began = time.perf_counter()
    lines: list[dict[str, Any]] = []
    board = bare_board(folder, den, intervals, lines)
    seed = board.world.seed
    tables = conversion.birth_of(board.families, seed)
    child = min((t[0][0] for t in tables), key=lambda k: count_wall(board.families[k], board.world.quantum_action))
    group = [m for m in cube_48() if not np.array_equal(m, IDENTITY)]
    turns = turns_of(board, None)
    log: list[dict[str, Any]] = []
    snapshots = [meeting_back.snapshot(board)]
    held_plain, held_c = set(range(len(group))), set(range(len(group)))
    per_interval = []
    for _ in range(intervals):
        kept = board.advanced_to_the_close()
        board.closed_after(kept)
        link_close(board, kept, orientation, child, log)
        turns = turns_of(board, turns)
        state = carried(board, IDENTITY)
        plain, with_c = [], []
        for number, m in enumerate(group):
            image = carried(board, m, turns)
            if not apart(image, state):
                plain.append(number)
            elif not apart(conjugated(board, image, turns), state):
                with_c.append(number)
        held_plain &= set(plain)
        held_c &= set(plain) | set(with_c)
        births = [e for e in log if e["interval"] == board.interval and "plus" in e]
        refusals = {}
        for e in log:
            if e["interval"] == board.interval and "refused" in e:
                refusals[e["refused"]] = refusals.get(e["refused"], 0) + 1
        line = {
            "interval": board.interval,
            "births": len(births),
            "refused": refusals,
            "currents": [e["current"] for e in log if e["interval"] == board.interval],
            "gradients": [e["gradient"] for e in log if e["interval"] == board.interval],
            "held_plain": 1 + len(plain),
            "held_with_c": 1 + len(plain) + len(with_c),
            "charge": charge_of(board, child),
            "turned": int(np.asarray(board.turned).sum()),
        }
        per_interval.append(line)
        out.write(json.dumps(line) + "\n")
        snapshots.append(meeting_back.snapshot(board))
    verdict = "MATCH"
    for k in range(intervals, 0, -1):
        board.step_inverse()
        found = meeting_back.first_difference(snapshots[k - 1], meeting_back.snapshot(board))
        if found is not None:
            verdict = f"MISS at the interval {board.interval}: {found}"
            break
    births = [e for e in log if "plus" in e]
    summary = {
        "den": den,
        "orientation": orientation,
        "intervals": intervals,
        "child": board.families[child].name,
        "child_pair": list(board.families[child].pair),
        "births": len(births),
        "birth_intervals": sorted({e["interval"] for e in births}),
        "birth_axes": sorted({e["axis"] for e in births}),
        "refused": {k: sum(1 for e in log if e.get("refused") == k) for k in ("several", "tie", "stop", "lay")},
        "meeting_links": len(log),
        "zero_currents": sum(1 for e in log if e["current"] == 0),
        "zero_gradients": sum(1 for e in log if e["gradient"] == 0),
        "held_plain_through_run": 1 + len(held_plain),
        "held_with_c_through_run": 1 + len(held_c),
        "run_back": verdict,
        "milliseconds": int((time.perf_counter() - began) * 1000),
    }
    out.write(json.dumps({"links": log}) + "\n")
    out.write(json.dumps(summary) + "\n")
    return summary


def seeded_board(folder: Path, den: int, intervals: int, lines: list[dict[str, Any]], at: Node | None) -> Lattice:
    """The bare 3-cube with the hole seed (at None) or the sea plus one quantum at `at` (tests/laws_universe.sea_plus_one), the one-Node meetings emptied."""
    from event_universe import seed as seed_module
    from tests.laws_universe import sea_plus_one

    if at is not None:
        seed_module.uniform_seed = sea_plus_one(at)
    return bare_board(folder, den, intervals, lines)


def run_transformed(den: int, intervals: int, orientation: str, at: Node, out: Any, folder: Path) -> dict[str, Any]:
    """The 48 images of a run from a seed that is not symmetric (the sea plus one quantum at `at`, the hole at the origin): for every element g the run from the seed carried by g compared, interval by interval, with the run carried by g (tests/test_the_board_is_the_cube_48, check (b)); the count of elements under which the two agree bit for bit through every interval, plain and with the senses exchanged."""
    began = time.perf_counter()
    group = cube_48()
    held_plain, held_c, per_element = 0, 0, []
    births_seen: dict[int, int] = {}
    for number, m in enumerate(group):
        image = tuple(int(v) for v in np.mod(m @ np.array(at), 3))
        lines_a: list[dict[str, Any]] = []
        lines_b: list[dict[str, Any]] = []
        base = seeded_board(folder / "base", den, intervals, lines_a, at)
        other = seeded_board(folder / f"g{number}", den, intervals, lines_b, image)
        seed_index = base.world.seed
        tables = conversion.birth_of(base.families, seed_index)
        child = min((t[0][0] for t in tables), key=lambda k: count_wall(base.families[k], base.world.quantum_action))
        turns = turns_of(base, None)
        log_a: list[dict[str, Any]] = []
        log_b: list[dict[str, Any]] = []
        plain_ok, c_ok, first_miss = True, True, None
        for _ in range(intervals):
            for board, log in ((base, log_a), (other, log_b)):
                kept = board.advanced_to_the_close()
                board.closed_after(kept)
                link_close(board, kept, orientation, child, log)
            turns = turns_of(base, turns)
            carried_base, state_other = carried(base, m, turns), carried(other, IDENTITY)
            if apart(carried_base, state_other):
                plain_ok = False
                if apart(conjugated(other, carried_base, turns), state_other):
                    c_ok = False
                    first_miss = first_miss or base.interval
        births = sum(1 for e in log_a if "plus" in e)
        births_seen[number] = births
        held_plain += plain_ok
        held_c += plain_ok or c_ok
        per_element.append({"element": m.tolist(), "image": list(image), "plain": plain_ok, "with_c": plain_ok or c_ok, "first_miss": first_miss, "births": births, "births_image": sum(1 for e in log_b if "plus" in e)})
        out.write(json.dumps(per_element[-1]) + "\n")
    summary = {
        "den": den,
        "orientation": orientation,
        "seed": {"hole": [0, 0, 0], "plus_one_at": list(at)},
        "intervals": intervals,
        "births_of_the_base_run": births_seen[0],
        "held_plain": held_plain,
        "held_with_c": held_c,
        "of": len(group),
        "milliseconds": int((time.perf_counter() - began) * 1000),
    }
    out.write(json.dumps(summary) + "\n")
    return summary


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--den", type=int, default=SMALL["integers"]["den"])
    parser.add_argument("--intervals", type=int, default=12)
    parser.add_argument("--orientation", choices=("label", "current", "gradient"), default="current")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--folder", type=Path, default=Path("/dev/shm/tmp/q2_link_birth"))
    parser.add_argument("--transformed", type=str, default=None, help="x,y,z: the check (b), the sea plus one quantum at this Node, every element's image run")
    args = parser.parse_args(argv)
    folder = args.folder / f"{args.den}_{args.orientation}_{args.transformed or 'hole'}"
    if args.transformed is not None:
        at = tuple(int(v) for v in args.transformed.split(","))
        assert len(at) == 3
        with (args.out.open("w", encoding="utf-8") if args.out else sys.stdout) as out:
            summary = run_transformed(args.den, args.intervals, args.orientation, (at[0], at[1], at[2]), out, folder)
        print(json.dumps(summary))
        return
    if args.out is None:
        print(json.dumps(run(args.den, args.intervals, args.orientation, sys.stdout, folder)))
        return
    with args.out.open("w", encoding="utf-8") as out:
        summary = run(args.den, args.intervals, args.orientation, out, folder)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
