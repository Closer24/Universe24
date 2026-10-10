"""The momentum at the click, read on the board with the program's own functions: the run's world (run3d_fixed/one_piece_3d_fixed.json, with its mode file) is stepped through the run, and equation (5), the board's momentum along each axis, is summed over the whole board for the light's lines and for the atoms' lines at every tick (node.momentum_of, the one reading the click itself uses), as is the write's twist probe (meeting.Probe.gained) as the click runs: the piece's momentum per axis as the credit line reads it at the taker's two Nodes scaled to one count, the quarter turn, the largest count of the angle 1/q_0 two Nodes along the board can hold, the momentum that quarter turn gives the taker along the board, and what is left of the piece's; and the same world run again with no detector declared (the twin of the run's third check), for the light's drift without a click. Written to run_momentum.json beside the paper, the board sums at the ticks the paper prints. Deterministic; the run's own toss. Usage: python3 -I run_momentum.py [src directory, ../../src unless given]; the world names the repository's examples/ files; the twin's mode file is the run's with the twin's digest (the bodies' records and the packets are the same, only the detectors' declarations are dropped)."""
from __future__ import annotations
import json
import shutil

import numpy as np
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[2] / "src"
sys.path.insert(0, str(SRC))
from event_universe import meeting, node, resonance  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import input_digest, load_world  # noqa: E402

WORLD = HERE.parent / "run3d_fixed" / "one_piece_3d_fixed.json"
OUT = HERE.parent / "run_momentum.json"
PRINTED = (0, 96, 120, 172)  # the ticks whose sums the paper prints


def twin_world(folder: Path, keep_packet: int | None = None) -> Path:
    """The run's world with no detector declared (the bodies' node_detector, transitions and rates dropped, as run_e4.py's twin), the run's mode file beside it with the twin's digest; with `keep_packet`, one half of the light alone (that packet kept in the world and in the mode file, the other dropped)."""
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    mode = json.loads(WORLD.with_suffix(".mode.json").read_text(encoding="utf-8"))
    for body in document["bodies"]:
        for key in ("node_detector", "transitions", "rates"):
            body.pop(key, None)
    if keep_packet is not None:
        document["packets"] = [document["packets"][keep_packet]]
        mode["packets"] = [mode["packets"][keep_packet]]
    path = folder / f"one_piece_3d_fixed_twin{'' if keep_packet is None else keep_packet}.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    shutil.copy(WORLD.with_name("design.json"), folder / "design.json")
    mode["world_digest"] = input_digest(document)
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def sums(board: Lattice) -> dict[str, list[int]]:
    """Equation (5) over the whole board, per axis, for each family's lines, in the unit of equation (5) itself (the weight 1; the credit line's fan is in this unit)."""
    out = {}
    for family, state in zip(board.families, board.states, strict=True):
        out[family.name] = list(node.momentum_of(1, list(state.lines), board.wrap))
    return out


def lines_along(board: Lattice, name: str) -> list[int]:
    """Equation (5) along the board, line by line, for one family."""
    k = [f.name for f in board.families].index(name)
    family, state = board.families[k], board.states[k]
    return [node.momentum_of(1, [line], board.wrap)[0] for line in state.lines]


def p_along(now: np.ndarray, before: np.ndarray) -> float:
    """Equation (5) along the board for one line on arrays, the ends holding zero: the sum over Nodes of the flow in from the left less the flow in from the right."""
    f_left = np.zeros_like(now)
    f_right = np.zeros_like(now)
    f_left[1:] = now[1:] * before[:-1] - before[1:] * now[:-1]
    f_right[:-1] = now[:-1] * before[1:] - before[:-1] * now[1:]
    return float((f_left - f_right).sum())


def linear_run(board: Lattice, name: str, ticks: tuple[int, ...]) -> dict[str, float]:
    """The light's line stepped by the rule's linear form, the remainder's term dropped (each neighbour's weight a third of w, the own weight 0 on the empty board: next = the six neighbours' sum over three, less before), from the board's numbers at tick 0, in floating point; equation (5) along the board at the ticks named."""
    k = [f.name for f in board.families].index(name)
    line = board.states[k].lines[0]
    now, before = np.asarray(line.now, dtype=float), np.asarray(line.before, dtype=float)
    out = {}
    for t_ in range(max(ticks) + 1):
        if t_ in ticks:
            out[str(t_)] = round(p_along(now, before), 1)
        total = np.zeros_like(now)
        for axis in range(now.ndim):
            total += np.roll(now, 1, axis=axis) * (np.arange(now.shape[axis]) > 0).reshape([-1 if i == axis else 1 for i in range(now.ndim)])
            total += np.roll(now, -1, axis=axis) * (np.arange(now.shape[axis]) < now.shape[axis] - 1).reshape([-1 if i == axis else 1 for i in range(now.ndim)])
        now, before = total / 3 - before, now
    return out


def main() -> int:
    readings: list[tuple[int, int, int]] = []  # (axis, count of acts, the momentum gained)
    original = meeting.Probe.gained

    def logged(self: meeting.Probe, count: int) -> int:
        value = original(self, count)
        readings.append((self.axis, count, value))
        return value

    meeting.Probe.gained = logged  # the probe read as the click runs
    lines: list[dict] = []
    board = Lattice(load_world(WORLD), lines.append)
    by_tick = {0: sums(board)}
    light_name = [f.name for f in board.families if f.pair[0] == f.pair[1]][0]
    linear = {"both": linear_run(board, light_name, (0, 48, 96))}
    credit = None
    before_click = None
    while board.interval < board.world.intervals:
        board.step()
        if credit is None:
            found = next((l for l in lines if l.get("event") == "credit" and l.get("count") == 1 and l.get("momentum")), None)
            if found is not None:
                credit = found
                before_click = by_tick[board.interval - 1]
                taker_lines = lines_along(board, credit["family"])
        by_tick[board.interval] = sums(board)
    meeting.Probe.gained = original
    if credit is None:
        print("run_momentum: no click with a momentum in this world")
        return 1
    tick = int(credit["interval"])
    with tempfile.TemporaryDirectory() as tmp:
        twin = Lattice(load_world(twin_world(Path(tmp))))
        twin_by_tick = {0: sums(twin)}
        while twin.interval < twin.world.intervals:
            twin.step()
            twin_by_tick[twin.interval] = sums(twin)
        halves = {}
        for k in range(len(board.world.packets)):
            half = Lattice(load_world(twin_world(Path(tmp), k)))
            kind = [f.name for f in half.families].index(credit["absorbed"])
            linear[f"half {k}"] = linear_run(half, credit["absorbed"], (0, 48, 96))
            along = {0: node.momentum_of(1, list(half.states[kind].lines), half.wrap)[0]}
            while half.interval < tick:
                half.step()
            along[tick] = node.momentum_of(1, list(half.states[kind].lines), half.wrap)[0]
            halves[str(k)] = {str(t_): v for t_, v in along.items()}
    taker_nodes = board.credit.bodies[int(credit["node_detector"].split()[-1])].nodes
    taken = max(halves, key=lambda k: halves[k][str(tick)] * (1 if taker_nodes[0][0] >= board.world.packets[int(k)].top[0][0] else -1))
    quarter = max(abs(c) for _, c, _ in readings)
    gained = max(abs(v) for a, c, v in readings if a == 0 and abs(c) == quarter)
    piece = [int(p) for p in credit["momentum"]]
    light, atom = credit["absorbed"], credit["family"]
    last = int(board.world.intervals)
    out = {
        "click_tick": tick,
        "taker": credit["node_detector"],
        "q_0": int(board.world.node_clock),
        "piece_momentum_read_at_the_taker": piece,
        "fan": [int(x) for x in credit["fan"]],
        "twist": [int(t) for t in credit["twist"]],
        "quarter_turn_acts": int(quarter),
        "gained_along_board": int(gained),
        "short_of_the_piece": int(abs(piece[0]) - gained),
        "taker_lines_along_board": [int(x) for x in taker_lines],
        "taker_along_board": int(sum(taker_lines)),
        "light_along_board": {str(t): by_tick[t][light][0] for t in PRINTED if t in by_tick},
        "light_along_board_before_click": before_click[light][0],
        "atoms_along_board": {str(t): by_tick[t][atom][0] for t in PRINTED if t in by_tick},
        "light_and_atoms_along_board_at_end": by_tick[last][light][0] + by_tick[last][atom][0],
        "light_at_end_plus_taker_as_written": by_tick[last][light][0] + int(sum(taker_lines)),
        "twin_light_along_board": {str(t): twin_by_tick[t][light][0] for t in PRINTED if t in twin_by_tick},
        "light_and_taker_at_120": by_tick[120][light][0] + int(sum(taker_lines)),
        "halves_alone_along_board": halves,
        "linear_form_along_board": linear,
        "cross_terms_at_start": by_tick[0][light][0] - sum(h["0"] for h in halves.values()),
        "gap_at_click_tick": by_tick[tick][light][0] - sum(h[str(tick)] for h in halves.values()),
        "taken_half": taken,
        "taker_over_taken_half": round(int(sum(taker_lines)) / halves[taken][str(tick)], 3),
        "reference_scale": int(resonance.scale_of(board.world.width, board.world.amplitude_bound, max(b["node_detector"]["window"] for b in json.loads(WORLD.read_text(encoding="utf-8"))["bodies"] if "node_detector" in b))),
        "lost": credit.get("lost"),
    }
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(f"run_momentum: the click at tick {tick} by {out['taker']}: the piece's momentum read at the taker {piece}; the quarter turn {quarter} of the angle 1/q_0 (q_0 = {out['q_0']}), the twist {out['twist']}; the taker gained {gained} of {abs(piece[0])} along the board, {out['short_of_the_piece']} short; its lines {out['taker_lines_along_board']}")
    print(f"run_momentum: each half of the light alone, without detectors, along the board at ticks 0 and {tick}: {halves} (the taken half is packet {taken}; the taker holds {out['taker_over_taken_half']} of it); light and taker at tick 120: {out['light_and_taker_at_120']} against {twin_by_tick[120][light][0]} without a click; the references' scale {out['reference_scale']}")
    print(f"run_momentum: the linear form keeps equation (5) along the board: {linear}; the halves' cross terms at the start {out['cross_terms_at_start']}, the gap at tick {tick} {out['gap_at_click_tick']} (the rest the remainder's drift)")
    print(f"run_momentum: equation (5) along the board, the light: {out['light_along_board']} with the click (before it at tick {tick}: {out['light_along_board_before_click']}; the credit line's fan {out['fan']}); without a click: {out['twin_light_along_board']}; the atoms: {out['atoms_along_board']}; light and atoms at the end: {out['light_and_atoms_along_board_at_end']}")
    print(f"written to {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
