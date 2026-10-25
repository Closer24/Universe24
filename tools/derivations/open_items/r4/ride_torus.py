"""Hand r4 (2026-10-25): the self-consistent run of the uniform sea on the bare 3-cube with the write on, the flag off
(argv 0, the branch's path) and on (argv 1, U24_RIDES: the quanta's lines ride the volume, flux.ride_line), the tests'
small universe (den 1,021, Gamma 1,000, T 36,000). Part A: the uniform sea laid on every Node (the origin too, no hole,
tests/laws_universe.uniform_sea in the seed's place), every act but the close for 320 intervals: per interval X at one
Node, the light's velocity at one Node, the count per Node (Lattice.quanta) and the share total; the top (the largest X,
its interval), the return (the first interval after the top at which X reads 1,000 again), the Nodes turned at the top.
Part B: the law's hole seed (seed.uniform_seed, the origin empty) with every act and the board's own close, 120
intervals: the births per interval from the output lines, the light's count and the born families' counts. Part C (the
flag on): one step back attempted, the refusal by name recorded; the flag off: the step back and the match of the arrays
with the start. Outputs ride_torus_<flag>.json. Integers only."""

import json
import os
import sys
from pathlib import Path

FLAG = sys.argv[1] if len(sys.argv) > 1 else "0"
os.environ["U24_RIDES"] = FLAG
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, os.environ.get("U24_SRC", str(ROOT / "src")))  # U24_SRC: the branch's pristine src, for the bit-for-bit check of the flag off

import numpy as np  # noqa: E402

from event_universe import flux, seed, world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import bare_torus, node_arrays, uniform_sea  # noqa: E402

AT = (0, 0, 0)


def board_of(folder, intervals, sea):
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    lines = []
    kept = seed.uniform_seed
    if sea:
        seed.uniform_seed = uniform_sea
    try:
        board = Lattice(load_world(bare_torus(folder, 3, intervals)), output=lines.append)
    finally:
        seed.uniform_seed = kept
    return board, lines


def readings(board):
    light, holder = board.world.seed, board.held[0]
    time = board.states[holder].lines[0]
    line = board.states[light].lines[0]
    quanta, _frozen = board.quanta(light)
    share, _frozen = board.share_of(light)
    return {
        "X": int(time.now[AT]),
        "X_before": int(time.before[AT]),
        "velocity": int(line.now[AT]) - int(line.before[AT]),
        "velocities_distinct": len(set(int(v) for v in (np.asarray(line.now, dtype=object) - np.asarray(line.before, dtype=object)).reshape(-1))),
        "count_per_node": int(quanta[AT]),
        "count_total": int(np.asarray(quanta, dtype=object).sum()),
        "share_total": int(np.asarray(share, dtype=object).sum()),
        "largest_level": int(max(abs(int(v)) for v in np.asarray(line.now, dtype=object).reshape(-1))),
    }


def part_a(folder):
    board, _lines = board_of(folder / "a", 400, True)
    rows = {0: readings(board)}
    top, top_at, returned_at = rows[0]["X"], 0, None
    turned_at = []
    for t in range(1, 321):
        board.advanced_to_the_close()
        row = readings(board)
        if board.turned.any():
            turned_at.append((t, int(board.turned.sum())))
        if row["X"] > top:
            top, top_at = row["X"], t
        if returned_at is None and top_at and t > top_at and row["X"] <= 1000:
            returned_at = t
        if t % 20 == 0 or t in (23, 140, 141, 280):
            rows[t] = row
    import hashlib

    digest = hashlib.sha256(repr(sorted((k, tuple(a.tolist() for a in v)) for k, v in node_arrays(board).items())).encode()).hexdigest()
    return {"rows": rows, "top": top, "top_at": top_at, "returned_at": returned_at, "turned_at": turned_at[:5], "turns": len(turned_at), "arrays_sha256_at_320": digest}


def part_b(folder, intervals=120):
    board, lines = board_of(folder / "b", intervals + 10, False)
    births, refusals = {}, {}
    for t in range(1, intervals + 1):
        before = len(lines)
        board.step()
        for line in lines[before:]:
            kind = str(line.get("kind", line.get("line", "")))
            if "birth" in kind:
                births[t] = births.get(t, 0) + 1
            if "refus" in json.dumps(line, default=str):
                refusals[t] = refusals.get(t, 0) + 1
    light = board.world.seed
    counts = {board.families[i].name: int(board.quanta(i)[0].sum()) for i in board.order}
    return {
        "births_by_interval": births,
        "births_total": sum(births.values()),
        "last_birth_interval": max(births) if births else None,
        "refusal_lines_by_interval": {k: v for k, v in list(refusals.items())[:40]},
        "counts_at_end": counts,
        "X_at_end": int(board.states[board.held[0]].lines[0].now[AT]),
        "light_velocity_at_end": int(board.states[light].lines[0].now[AT]) - int(board.states[light].lines[0].before[AT]),
        "kinds_seen": sorted(set(str(line.get("kind", line.get("line", ""))) for line in lines))[:12],
    }


def part_c(folder):
    board, _lines = board_of(folder / "c", 40, True)
    start = node_arrays(board)
    for _ in range(5):
        board.advanced_to_the_close()
    try:
        for _ in range(5):
            board.step_inverse()
    except NotImplementedError as refusal:
        return {"step_back": "refused", "reason": str(refusal)}
    after = node_arrays(board)
    unequal = sum(
        int((np.asarray(a, dtype=object) != np.asarray(b, dtype=object)).sum())
        for key in start
        for a, b in zip(start[key], after[key], strict=True)
    )
    return {"step_back": "run", "unequal_entries_after_5_back": unequal, "MATCH": unequal == 0}


if __name__ == "__main__":
    folder = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r4_torus_{FLAG}"
    found = {"flag": FLAG, "rides": getattr(flux, "RIDES", None), "A": part_a(folder), "B": part_b(folder), "C": part_c(folder)}
    tag = FLAG + ("_pristine" if "U24_SRC" in os.environ else "")
    (HERE / f"ride_torus_{tag}.json").write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
    print(json.dumps(found, indent=1, default=str))
