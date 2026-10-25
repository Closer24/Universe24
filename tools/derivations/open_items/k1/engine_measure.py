"""Hand k1, brief k, part (d): the engine's own run on the bare torus (the toy harness's universe: den, Gamma, T written as a universe file, the 3-cube, nothing declared) at a Link unit G, N intervals forward and N back by tools/back_in_time.verdict (MATCH / MISS / REFUSED), with the readings: the derived width, the amplitude bound A, the count of integers one Node holds and the largest bit length of the state, the largest bit length of every carried division's total (the one division act of the law, core/rule3.carried_division wrapped by this tool: Rule3's totals, the paces' roundings, the writes, the reads and the takes alike), the clicks (credit and birth lines, the senses' sum over the births), and the levels of every line at the end (a digest) so that two Link units can be compared. No file of src/ is edited: the Link unit is set on the loader's module global, the recorder wraps the act's function.

    PYTHONPATH=src python tools/derivations/k1/engine_measure.py <den> <Gamma> <T> <G> <intervals> [<cube>]
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from event_universe import world_files  # noqa: E402
from event_universe.core import rule3 as core_rule3  # noqa: E402
from event_universe.loader import world as loader_world  # noqa: E402

LARGEST = {"bits": 0, "wall_bits": 0, "calls": 0, "where": ""}


def bits_of(value) -> int:  # type: ignore[no-untyped-def]
    arr = np.asarray(value, dtype=object).reshape(-1)
    if arr.size == 0:
        return 0
    return max(abs(int(x)) for x in arr.tolist()).bit_length()


REAL_DIVISION = core_rule3.carried_division


def recorded_division(total, wall, remainder, direction=1):  # type: ignore[no-untyped-def]
    LARGEST["calls"] += 1
    whole = np.asarray(total, dtype=object) * direction + np.asarray(remainder, dtype=object)
    b = bits_of(whole)
    if b > LARGEST["bits"]:
        LARGEST["bits"] = b
    wb = bits_of(wall)
    if wb > LARGEST["wall_bits"]:
        LARGEST["wall_bits"] = wb
    return REAL_DIVISION(total, wall, remainder, direction)


def state_readings(board) -> dict:  # type: ignore[no-untyped-def]
    count, largest, digest = 0, 0, hashlib.sha256()
    for state in board.states:
        for line in state.lines:
            for a in (line.now, line.before, line.remainder):
                count += 1
                largest = max(largest, bits_of(a))
            for a in (line.now, line.before):
                digest.update(json.dumps([int(x) for x in np.asarray(a, dtype=object).reshape(-1).tolist()]).encode())
        for w in state.write_remainders:
            count += 1
            largest = max(largest, bits_of(w))
        for row in state.phases:
            for line in row:
                for a in (line.now, line.before, line.remainder):
                    count += 1
                    largest = max(largest, bits_of(a))
                for a in (line.now, line.before):
                    digest.update(json.dumps([int(x) for x in np.asarray(a, dtype=object).reshape(-1).tolist()]).encode())
    return {"integers_per_node": count, "largest_state_bits": largest, "levels_digest": digest.hexdigest()[:16]}


def main() -> None:
    den, gamma, action, unit, intervals = (int(a) for a in sys.argv[1:6])
    cube = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    folder = Path("/dev/shm/tmp") / f"k1_engine_{den}_{gamma}_{action}_{unit}_{cube}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(json.dumps({"integers": {"den": den, "node_clock": gamma, "quantum_action": action}}))
    (folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [cube] * 3, "intervals": intervals}))
    world_files.REPOSITORY_ROOT = folder
    loader_world.LINK_UNIT = unit  # the Link unit of this run, the loader's module global; src untouched
    core_rule3.carried_division = recorded_division  # the recorder on the one division act
    spec = importlib.util.spec_from_file_location("back_in_time", ROOT / "tools" / "back_in_time.py")
    back = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(back)
    from event_universe.lattice import Lattice
    from event_universe.world_files import load_world

    t0 = time.time()
    world = load_world(folder / "w.json")
    lines: list[dict] = []
    board = Lattice(world, output=lines.append)
    start = state_readings(board)
    verdict = back.verdict(board, intervals)
    # forward again to the end for the end's readings (the gate left the board at its first interval)
    for _ in range(intervals):
        board.step()
    end = state_readings(board)
    credits = [li for li in lines if li.get("event") == "credit"]
    births = [li for li in lines if li.get("event") == "birth"]
    senses = sum(sum(li.get("senses", [])) for li in births)
    children = sum(len(li.get("children", [])) for li in births)
    report = {
        "den": den, "den_bits": den.bit_length(), "Gamma": gamma, "T": action, "G": unit, "cube": cube, "intervals": intervals,
        "families": len(world.families), "width_bits": world.width.bit_length(), "A": world.amplitude_bound, "A_bits": world.amplitude_bound.bit_length(),
        "kind": str(world.kind), "run_back": verdict, "start": start, "end": end,
        "largest_division_total_bits": LARGEST["bits"], "largest_wall_bits": LARGEST["wall_bits"], "division_calls": LARGEST["calls"],
        "credits": len(credits), "births": len(births), "children": children, "senses_sum": senses,
        "born_at": {str(k): v for k, v in board.born_at.items()}, "seconds": round(time.time() - t0, 1),
    }
    print(json.dumps(report))


if __name__ == "__main__":
    main()
