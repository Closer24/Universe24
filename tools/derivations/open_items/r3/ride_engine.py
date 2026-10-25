"""Hand R3 (2026-10-25), item (d): the self-consistent run of the engine with the riding lines behind the flag U24_RIDES
(src/event_universe/flux.py `ride_division`, `ride_volumes`; swap.py the complement wall; lattice.py the half-wall origin
and the fixed-point inverse), the tests' small universe (den 1,021, Gamma 1,000, T 36,000) on the 3-cube torus.

Parts (the command's first word; the flag read from the environment at the import, so the script runs twice, with
U24_RIDES unset and with U24_RIDES=1, and writes ride_engine_<part>_<off|on>.json beside itself):
  sea   the uniform sea (the origin holding a quantum too, tests.laws_universe.uniform_sea) with the volume's write on and
        the interval's acts without the close, 320 intervals: X at every interval, the first turn (the top), the least X
        after it (the return through the seed), the sea's drift and its count per Node, the mean level.
  hole  the law's hole seed, every act and the close, 120 intervals: the births per interval, the refusals by name, the
        light's count, the content's level.
  back  the hole seed, 32 intervals forward through the births and 32 back by the lattice's own inverse, every array
        compared bit for bit (tests.laws.board_state, same_state): the count returned and the fixed-point trials per step.
Command: [U24_RIDES=1] PYTHONPATH=src:. TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/r3/ride_engine.py <part>
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
for path in (ROOT / "src", ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from event_universe import flux, readings, registry, seed, share, world_files  # noqa: E402
from event_universe.core.rule3 import division_forward  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.frames import frames_of  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws import board_state, same_state  # noqa: E402
from tests.laws_universe import GAMMA, bare_torus, uniform_sea  # noqa: E402

FLAG = "on" if flux.RIDES else "off"
SCALE = 10**6


def board_of(folder: Path, sea: bool, lines: list | None = None) -> Lattice:
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    if sea:
        seed.uniform_seed = uniform_sea
    return Lattice(load_world(bare_torus(folder, 3, 400)), output=None if lines is None else lines.append)


def reading(board: Lattice) -> dict:
    light, held = board.world.seed, board.held[0]
    line = board.states[light].lines[0]
    now = np.asarray(line.now, dtype=object)
    drift = now - np.asarray(line.before, dtype=object)
    time = board.states[held].lines[0]
    x = np.asarray(time.now, dtype=object)
    level = np.asarray(volume.level_of(GAMMA, x), dtype=object)
    quanta, _ = board.quanta(light)
    return {
        "interval": board.interval,
        "X_min": int(x.min()),
        "X_max": int(x.max()),
        "level_min": int(level.min()),
        "level_max": int(level.max()),
        "drift_min": int(drift.min()),
        "drift_max": int(drift.max()),
        "mean_level": int(division_forward(int(now.sum()), now.size, 0)[0]),
        "quanta_min": int(np.asarray(quanta).min()),
        "quanta_max": int(np.asarray(quanta).max()),
        "quanta_total": int(np.asarray(quanta, dtype=object).sum()),
        "turned": int(board.turned.sum()),
    }


def sea(folder: Path) -> dict:
    board = board_of(folder, True)
    rows = [reading(board)]
    for interval in range(320):
        board.advanced_to_the_close()
        rows.append(reading(board))
        row = rows[-1]
        if interval % 20 == 19 or row["turned"]:
            print(
                f"sea {FLAG} interval {row['interval']:4d} X {row['X_min']}..{row['X_max']} level {row['level_min']}..{row['level_max']} "
                f"drift {row['drift_min']}..{row['drift_max']} mean level {row['mean_level']} quanta {row['quanta_min']}..{row['quanta_max']} turned {row['turned']}",
                flush=True,
            )
    tops = [r["interval"] for r in rows if r["turned"]]
    top = max(rows, key=lambda r: r["X_max"])
    after = [r for r in rows if tops and r["interval"] > tops[0]]
    least = min(after, key=lambda r: r["X_min"]) if after else None
    summary = {
        "first_turn": tops[0] if tops else None,
        "turn_intervals": len(tops),
        "X_top": top["X_max"],
        "interval_top": top["interval"],
        "level_top": top["level_max"],
        "X_least_after_top": least["X_min"] if least else None,
        "interval_least_after_top": least["interval"] if least else None,
        "drift_at_top": [top["drift_min"], top["drift_max"]],
        "drift_at_least": [least["drift_min"], least["drift_max"]] if least else None,
        "quanta_per_node_at_top": [top["quanta_min"], top["quanta_max"]],
        "quanta_per_node_rows_at_1_2_3": [r["interval"] for r in rows if r["quanta_min"] >= 2][:1],
        "first_interval_at_two_quanta": next((r["interval"] for r in rows if r["quanta_min"] >= 2), None),
    }
    print(f"sea {FLAG} summary {summary}")
    return {"flag": FLAG, "rows": rows, "summary": summary}


def hole(folder: Path) -> dict:
    lines: list[dict] = []
    board = board_of(folder, False, lines)
    rows = []
    for _ in range(120):
        board.step()
        births = [line for line in lines if line.get("event") == "birth" and line.get("interval") == board.interval]
        refused = [line for line in lines if line.get("event") == "refused" and line.get("interval") == board.interval]
        causes: dict[str, int] = {}
        for line in refused:
            cause = str(line.get("cause", line.get("label", "?")))
            causes[cause] = causes.get(cause, 0) + 1
        read = reading(board)
        read["births"] = len(births)
        read["refused"] = causes
        rows.append(read)
        if births or read["interval"] % 20 == 0 or read["turned"]:
            print(
                f"hole {FLAG} interval {read['interval']:4d} births {len(births)} refused {causes} X {read['X_min']}..{read['X_max']} "
                f"level {read['level_min']}..{read['level_max']} light quanta {read['quanta_total']} drift {read['drift_min']}..{read['drift_max']} turned {read['turned']}",
                flush=True,
            )
    births_total = sum(r["births"] for r in rows)
    first_bang = next((r["interval"] for r in rows if r["births"]), None)
    later = [r["interval"] for r in rows if r["births"] and first_bang is not None and r["interval"] > first_bang + 10]
    summary = {
        "births_total": births_total,
        "birth_intervals": [r["interval"] for r in rows if r["births"]],
        "first_bang": first_bang,
        "births_after_the_first_bang_plus_10": later,
        "turn_intervals": [r["interval"] for r in rows if r["turned"]],
        "credits": sum(1 for line in lines if line.get("event") == "credit"),
    }
    print(f"hole {FLAG} summary {summary}")
    return {"flag": FLAG, "rows": rows, "summary": summary}


def back(folder: Path) -> dict:
    lines: list[dict] = []
    board = board_of(folder, False, lines)
    states = [board_state(board)]
    intervals = 32
    for _ in range(intervals):
        board.step()
        states.append(board_state(board))
    during: list[dict] = []
    board.output = during.append
    returned, trials, misses = 0, [], []
    for k in range(intervals):
        try:
            board.step_inverse()
        except RuntimeError as refusal:
            misses.append({"interval": board.interval, "refused": str(refusal)})
            break
        trials.append(getattr(board, "ride_trials", 0))
        if same_state(board_state(board), states[intervals - 1 - k]):
            returned += 1
        else:
            misses.append({"interval": board.interval})
    summary = {
        "intervals": intervals,
        "returned_bit_for_bit": returned,
        "interval_at_end": board.interval,
        "fixed_point_trials_per_step": trials,
        "misses": misses[:5],
        "births_forward": sum(1 for line in lines if line.get("event") == "birth"),
        "verdict": "MATCH" if returned == intervals and board.interval == 0 and not during else "MISS",
    }
    print(f"back {FLAG} summary {summary}")
    return {"flag": FLAG, "summary": summary}


def top(folder: Path) -> dict:
    """The Boss's follow-up (3): the uniform sea with the write on, the acts without the close, run forward through its first top and 40 intervals beyond, every state kept; then (i) the retrace, the state at the interval top + k against the state at top + 1 - k with the levels exchanged (the swap's own mirror: the forward run from the swapped state is the run back of the rise where the retrace is exact), counted per array; (ii) the run back from the end to the start by the lattice's inverse, every state bit for bit (the involution of the swap and the inverse through the top)."""
    board = board_of(folder, True)
    states = [board_state(board)]
    rows = [reading(board)]
    first_turn = None
    while True:
        board.advanced_to_the_close()
        states.append(board_state(board))
        rows.append(reading(board))
        if rows[-1]["turned"] and first_turn is None:
            first_turn = board.interval
            print(f"top {FLAG}: the first turn at {first_turn}, X {rows[-1]['X_min']}..{rows[-1]['X_max']}", flush=True)
        if (first_turn is not None and board.interval >= first_turn + 40) or board.interval >= 400:
            break
    run = board.interval
    retrace = []
    if first_turn is not None:
        light, held = board.world.seed, board.held[0]
        for k in range(1, min(first_turn, 41)):
            after, before = states[first_turn + k], states[first_turn + 1 - k]
            # the mirror: the light's level now after the top against the level before at the mirror interval, the volume's X alike (board_state: per family (lines, writes), a line (now, before, remainder))
            a_now = np.asarray(after[light][0][0][0], dtype=object)
            b_before = np.asarray(before[light][0][0][1], dtype=object)
            x_after = np.asarray(after[held][0][0][0], dtype=object)
            x_before = np.asarray(before[held][0][0][1], dtype=object)
            retrace.append(
                {
                    "k": k,
                    "light_now_equal_nodes": int(np.sum(a_now == b_before)),
                    "X_equal_nodes": int(np.sum(x_after == x_before)),
                    "X_after": int(x_after.reshape(-1)[0]),
                    "X_mirror": int(x_before.reshape(-1)[0]),
                    "light_now_after": int(a_now.reshape(-1)[0]),
                    "light_before_mirror": int(b_before.reshape(-1)[0]),
                }
            )
    returned, trials, misses = 0, [], []
    for k in range(run):
        try:
            board.step_inverse()
        except RuntimeError as refusal:
            misses.append({"interval": board.interval, "refused": str(refusal)})
            break
        trials.append(getattr(board, "ride_trials", 0))
        if same_state(board_state(board), states[run - 1 - k]):
            returned += 1
        else:
            misses.append({"interval": board.interval})
            if len(misses) > 3:
                break
    nodes = int(np.prod(board.shape))
    summary = {
        "first_turn": first_turn,
        "intervals_run": run,
        "returned_bit_for_bit": returned,
        "verdict": "MATCH" if returned == run and board.interval == 0 else "MISS",
        "misses": misses[:4],
        "fixed_point_trials_max": max(trials) if trials else None,
        "fixed_point_trials_histogram": {str(t): trials.count(t) for t in sorted(set(trials))},
        "retrace_exact_k": [r["k"] for r in retrace if r["light_now_equal_nodes"] == nodes and r["X_equal_nodes"] == nodes],
        "retrace_first_inexact_k": next((r["k"] for r in retrace if r["light_now_equal_nodes"] < nodes or r["X_equal_nodes"] < nodes), None),
        "retrace_rows": retrace[:6] + retrace[-3:] if len(retrace) > 9 else retrace,
        "X_top": max(r["X_max"] for r in rows),
        "X_at_end": rows[-1]["X_min"],
    }
    print(f"top {FLAG} summary {summary}")
    return {"flag": FLAG, "rows": rows, "summary": summary}


def back60(folder: Path) -> dict:
    """The Boss's follow-up (1): the hole seed with births and every act, 60 intervals forward and 60 back, bit for bit, the fixed-point trials per step."""
    lines: list[dict] = []
    board = board_of(folder, False, lines)
    states = [board_state(board)]
    intervals = 60
    turned = []
    for _ in range(intervals):
        board.step()
        states.append(board_state(board))
        if board.turned.any():
            turned.append(board.interval)
    returned, trials, misses = 0, [], []
    for k in range(intervals):
        try:
            board.step_inverse()
        except RuntimeError as refusal:
            misses.append({"interval": board.interval, "refused": str(refusal)})
            break
        trials.append(getattr(board, "ride_trials", 0))
        if same_state(board_state(board), states[intervals - 1 - k]):
            returned += 1
        else:
            misses.append({"interval": board.interval})
            if len(misses) > 3:
                break
    summary = {
        "intervals": intervals,
        "returned_bit_for_bit": returned,
        "interval_at_end": board.interval,
        "verdict": "MATCH" if returned == intervals and board.interval == 0 else "MISS",
        "misses": misses[:4],
        "fixed_point_trials_max": max(trials) if trials else None,
        "fixed_point_trials_histogram": {str(t): trials.count(t) for t in sorted(set(trials))},
        "births_forward": sum(1 for line in lines if line.get("event") == "birth"),
        "birth_intervals": sorted({int(line["interval"]) for line in lines if line.get("event") == "birth"}),
        "turn_intervals": turned,
    }
    print(f"back60 {FLAG} summary {summary}")
    return {"flag": FLAG, "summary": summary}


def total(value) -> int:  # type: ignore[no-untyped-def]
    """An integer or a nested list of integers summed; None counts 0."""
    if value is None:
        return 0
    if isinstance(value, list | tuple):
        return sum(total(v) for v in value)
    return int(value)


def clicks(folder: Path) -> dict:
    """The owner's Addition 5, the conservations read on the board and in the clicks with the ride on or off: the hole seed, every act and the close, 120 intervals. On the board per interval: the light's share summed over the torus (the conserved form's reading, the frame's weight in it) and in quanta, every record's six Port currents summed over the torus (the current's antisymmetry: 0 exactly where every Link's current is read opposite from its two ends), every plane family's charge (the Wronskian over T div 2), the volume's X range. In the clicks (the lines alone): per birth line the senses' sum (the charge), taken against walls plus excess (the exact take's identity), per credit line the kind, the count, the beat and the proper (the energy as the beat per proper interval, (beat x Gamma) div proper where both stand)."""
    lines: list[dict] = []
    board = board_of(folder, False, lines)
    rows = []
    for _ in range(120):
        board.step()
        light = board.world.seed
        shares, cold = board.share_of(light)
        quanta, _ = board.quanta(light)
        currents = {}
        for index in board.order:
            if not registry.records_of(board.families[index], board.states[index].lines):
                continue
            found = 0
            for record in range(registry.records_of(board.families[index], board.states[index].lines)):
                own = board.lines_of(index, record)
                ports_sum = readings.currents_of(
                    board.families[index].pair[0], own, frames_of(index, board.families, board.states, record)
                )
                found += int(sum(int(np.asarray(p, dtype=object).sum()) for p in ports_sum))
            currents[board.families[index].name] = found
        charges = {
            board.families[index].name: share.charge_of(board, index)
            for index in board.order
            if board.families[index].plane and registry.records_of(board.families[index], board.states[index].lines)
        }
        x = np.asarray(board.states[board.held[0]].lines[0].now, dtype=object)
        rows.append(
            {
                "interval": board.interval,
                "light_share_total": int(np.asarray(shares, dtype=object).sum()),
                "light_quanta_total": int(np.asarray(quanta, dtype=object).sum()),
                "frozen": int(np.asarray(cold).sum()),
                "currents_sum_over_torus": currents,
                "charges": charges,
                "X_min": int(x.min()),
                "X_max": int(x.max()),
            }
        )
    births = [line for line in lines if line.get("event") == "birth"]
    credits = [line for line in lines if line.get("event") == "credit"]
    sense_sums = [total(line.get("senses")) for line in births]
    take_identity = [
        {"interval": line.get("interval"), "taken": total(line.get("taken")), "walls_plus_excess": total(line.get("walls")) + total(line.get("excess"))}
        for line in births
    ]
    beats = []
    for line in credits:
        beat, proper = line.get("beat"), line.get("proper")
        beats.append(
            {
                "interval": line.get("interval"),
                "family": line.get("family"),
                "kind": line.get("kind"),
                "count": line.get("count"),
                "beat": beat,
                "proper": proper,
                "beat_gamma_over_proper": int(division_forward(int(beat) * GAMMA, int(proper), 0)[0]) if isinstance(beat, int) and isinstance(proper, int) and proper else None,
                "momentum": line.get("momentum"),
                "sense": line.get("sense"),
            }
        )
    summary = {
        "births": len(births),
        "birth_intervals": sorted({int(b["interval"]) for b in births}),
        "senses_sum_per_birth": sense_sums,
        "charge_conserved_at_every_birth": all(s == 0 for s in sense_sums),
        "take_identity_holds_on_every_birth": all(t["taken"] == t["walls_plus_excess"] for t in take_identity),
        "take_rows": take_identity[:6],
        "credits": len(credits),
        "credits_by_kind": {str(k): sum(1 for c in credits if c.get("kind") == k) for k in {c.get("kind") for c in credits}},
        "credits_with_beat": sum(1 for c in credits if isinstance(c.get("beat"), int) and c.get("beat")),
        "beat_rows": [b for b in beats if b["beat"]][:12],
        "currents_sum_nonzero_intervals": sum(1 for r in rows if any(v != 0 for v in r["currents_sum_over_torus"].values())),
        "charges_first_last": [rows[0]["charges"], rows[-1]["charges"]],
        "light_share_first_last": [rows[0]["light_share_total"], rows[-1]["light_share_total"]],
        "light_quanta_first_last": [rows[0]["light_quanta_total"], rows[-1]["light_quanta_total"]],
    }
    print(f"clicks {FLAG} summary {json.dumps(summary, default=str)}")
    return {"flag": FLAG, "rows": rows, "summary": summary, "births": births, "credits": credits}


def cube48(folder: Path) -> dict:
    """The cube's 48 on the levels (the owner's law The cube's symmetry): the hole seed, every act and the close, 30 intervals through the births at 4 and the turns; at every interval every line's two levels of every family carried by each of the 48 signed permutations about the origin (a scalar line permuted over the Nodes; a holder's axis lines permuted over the axes, the sign holder's odd lines negated where their axis flips) compared with the board's own, the unequal entries counted; the remainders and the phase lines are not compared here (their mirror under the moving wall is the wall-dependent reflection the branch's harness does not model, section 7.4)."""
    from tests.test_the_board_is_the_cube_48 import axis_map, cube_48

    lines: list[dict] = []
    board = board_of(folder, False, lines)
    group = cube_48()
    shape, side = board.shape, board.shape[0]
    nodes = np.array(list(np.ndindex(*shape)))

    def moved(array, m):  # type: ignore[no-untyped-def]
        a = np.asarray(array, dtype=object)
        images = np.mod(nodes @ m.T, side)
        out = np.empty_like(a)
        out[tuple(images.T)] = a[tuple(nodes.T)]
        return out

    def unequal(m) -> int:  # type: ignore[no-untyped-def]
        pi, s = axis_map(m)
        count = 0
        for index, state in enumerate(board.states):
            family = board.families[index]
            if not family.held:
                for line in state.lines:
                    for level in (line.now, line.before):
                        count += int(np.sum(moved(level, m) != np.asarray(level, dtype=object)))
                continue
            rows, per_row = registry.records_of(family, state.lines), family.width
            for row in range(rows):
                base = row * per_row
                for level in (state.lines[base].now, state.lines[base].before):
                    count += int(np.sum(moved(level, m) != np.asarray(level, dtype=object)))
                for triple in range((per_row - 1) // 3):
                    for a in range(3):
                        k, target = base + 1 + triple * 3 + a, base + 1 + triple * 3 + pi[a]
                        sign = -1 if (family.wronskian and s[a] < 0) else 1
                        for part in (0, 1):
                            source = (state.lines[k].now, state.lines[k].before)[part]
                            image = (state.lines[target].now, state.lines[target].before)[part]
                            count += int(np.sum(moved(np.asarray(source, dtype=object) * sign, m) != np.asarray(image, dtype=object)))
        return count

    rows = []
    for _ in range(30):
        board.step()
        broken = [unequal(m) for m in group]
        rows.append(
            {
                "interval": board.interval,
                "elements_with_unequal_levels": sum(1 for b in broken if b),
                "unequal_entries_total": sum(broken),
                "turned": int(board.turned.sum()),
                "births": sum(1 for line in lines if line.get("event") == "birth" and line.get("interval") == board.interval),
            }
        )
        print(f"cube48 {FLAG} interval {board.interval:3d} elements broken {rows[-1]['elements_with_unequal_levels']:2d} of 48, unequal entries {rows[-1]['unequal_entries_total']}, turned {rows[-1]['turned']}, births {rows[-1]['births']}", flush=True)
    summary = {
        "intervals": 30,
        "intervals_with_every_element_equal": sum(1 for r in rows if r["elements_with_unequal_levels"] == 0),
        "first_broken_interval": next((r["interval"] for r in rows if r["elements_with_unequal_levels"]), None),
        "births": sum(r["births"] for r in rows),
        "turn_intervals": [r["interval"] for r in rows if r["turned"]],
    }
    print(f"cube48 {FLAG} summary {summary}")
    return {"flag": FLAG, "rows": rows, "summary": summary}


def main() -> None:
    part = sys.argv[1]
    folder = Path(tempfile.mkdtemp(prefix=f"r3_{part}_{FLAG}_", dir=os.environ.get("TMPDIR", "/dev/shm/tmp")))
    found = {"sea": sea, "hole": hole, "back": back, "top": top, "back60": back60, "clicks": clicks, "cube48": cube48}[part](folder)
    out = HERE.parent / f"ride_engine_{part}_{FLAG}.json"
    out.write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
    print("written", out)


if __name__ == "__main__":
    main()
