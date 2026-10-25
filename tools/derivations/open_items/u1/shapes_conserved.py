"""U1 (Addition 4; THE_WAY steps 3 and 4): what the lattice conserves, on the board and in the clicks, on the bare 3-cube at den 1,021 run through its births: the run back MATCH (tools/back_in_time.verdict over 36 intervals), the linear sum L of light (the massless invariant, remainders included, tests/laws.linear_sum) interval by interval until the births, the lattice momentum P_a of every record of quanta per interval (readings.momentum_of) with the per-step move against the hands' bound, the charge on the board (every plane record's Wronskian summed over the board, per record and in all) against the charge in the clicks (the births' senses summed), the count at the births (the take's integers on the birth lines: taken, the children's walls, the excess, the step), the fixed count and the largest bit length (tools/node_integers.py). Integer readings only; the output beside the script as shapes_conserved.json.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/u1/shapes_conserved.py"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from event_universe import readings, records, registry, world_files  # noqa: E402
from event_universe.core.rule3 import wall_of  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws import linear_sum  # noqa: E402
from tests.laws_universe import GAMMA, SMALL, bare_torus  # noqa: E402


def load_tool(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BACK = load_tool("back_in_time", ROOT / "tools" / "back_in_time.py")
COUNT = load_tool("node_integers", ROOT / "tools" / "node_integers.py")
INTERVALS = 36


def main() -> None:
    folder = Path("/dev/shm/tmp/u1_conserved")
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    path = bare_torus(folder, 3, INTERVALS)
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(path), output=lines.append)
    light = board.world.seed
    den, unit = SMALL["integers"]["den"], board.unit
    wall = wall_of(den, GAMMA, unit)
    out: dict = {"intervals": INTERVALS}  # type: ignore[type-arg]
    linear, momentum, charge, counts = [], [], [], []
    for _ in range(INTERVALS):
        board.step()
        line = board.states[light].lines[0]
        linear.append(int(linear_sum(wall, line)))
        p = {"interval": board.interval}
        num = board.families[light].pair[0]
        p["light"] = list(readings.momentum_of(num, [line]))
        bound = [2 * num * int(np.abs(np.roll(np.asarray(line.now, dtype=object), -1, a) - np.roll(np.asarray(line.now, dtype=object), 1, a)).sum()) for a in range(3)]
        p["light_bound"] = bound
        for index in board.turning:
            family = board.families[index]
            total = [0, 0, 0]
            for record in range(registry.records_of(family, board.states[index].lines)):
                span = records.record_slice(family, record)
                found = readings.momentum_of(family.pair[0], board.states[index].lines[span])
                total = [t + f for t, f in zip(total, found, strict=True)]
            p[family.name] = total
        momentum.append(p)
        c = {"interval": board.interval}
        board_total = 0
        for index in board.turning:
            family = board.families[index]
            per_record = []
            for record in range(registry.records_of(family, board.states[index].lines)):
                span = records.record_slice(family, record)
                w = int(np.asarray(records.wronskian(board.states[index].lines[span], True), dtype=object).sum())
                per_record.append(w)
                board_total += w
            c[family.name] = per_record
        c["board_total"] = board_total
        senses = sum(s for x in lines if x.get("event") == "birth" for s in x["senses"])
        c["clicks_senses_sum"] = int(senses)
        c["births_so_far"] = sum(1 for x in lines if x.get("event") == "birth")
        charge.append(c)
        reading = COUNT.line_of(board)
        counts.append({"interval": board.interval, "integers": reading["integers"], "same": reading["same_at_every_node"], "bits": reading["largest_bit_length"]})
    out["linear_sum_of_light"] = {"values_first_12": linear[:12], "distinct_until_first_birth": None, "all": linear}
    first_birth = next((x["interval"] for x in lines if x.get("event") == "birth"), None)
    out["first_birth"] = first_birth
    if first_birth is not None:
        before = linear[: first_birth - 1]
        out["linear_sum_of_light"]["distinct_until_first_birth"] = len(set(before))
        out["linear_sum_of_light"]["at_birth_change"] = linear[first_birth - 1] - linear[first_birth - 2] if first_birth >= 2 else None
    moves = [abs(momentum[k]["light"][a] - momentum[k - 1]["light"][a]) for k in range(1, len(momentum)) for a in range(3)]
    bounds = [momentum[k]["light_bound"][a] for k in range(1, len(momentum)) for a in range(3)]
    out["momentum"] = {
        "light_first_8": [m["light"] for m in momentum[:8]],
        "light_max_step_move": max(moves) if moves else 0,
        "light_min_bound": min(bounds) if bounds else 0,
        "moves_within_bound": all(mv <= b for mv, b in zip(moves, bounds, strict=True)),
        "planes_at_the_end": {k: v for k, v in momentum[-1].items() if k not in ("interval", "light", "light_bound")},
    }
    out["charge"] = {"at_the_end": charge[-1], "after_the_first_birth": charge[first_birth - 1] if first_birth else None, "board_total_nonzero_intervals": sum(1 for c in charge if c["board_total"] != 0), "clicks_sum_nonzero_intervals": sum(1 for c in charge if c["clicks_senses_sum"] != 0)}
    out["births"] = [{k: x.get(k) for k in ("interval", "family", "children", "senses", "nodes", "taken", "walls", "excess", "step")} for x in lines if x.get("event") == "birth"]
    out["refused"] = [{k: x.get(k) for k in ("interval", "cause", "nodes", "reason")} for x in lines if x.get("event") == "refused"][:6]
    out["take_identity"] = [
        {"interval": b["interval"], "taken_equals_walls_plus_excess": (b["taken"] == b["walls"] + b["excess"]) if b.get("taken") is not None else None}
        for b in out["births"]
    ]
    out["counts"] = {"distinct": sorted({c["integers"] for c in counts}), "same_at_every_node_all": all(c["same"] for c in counts), "largest_bits": max(c["bits"] for c in counts)}
    out["run_back"] = BACK.verdict(Lattice(load_world(path)), INTERVALS)
    (HERE / "shapes_conserved.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("first_birth", "linear_sum_of_light", "momentum", "charge", "take_identity", "counts", "run_back")}, default=str))
    print(json.dumps(out["births"][:3], default=str))


if __name__ == "__main__":
    main()
