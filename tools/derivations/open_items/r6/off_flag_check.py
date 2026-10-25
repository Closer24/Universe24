"""Hand R6 (2026-10-25): the branch's path bit for bit with the flag off. The uniform sea (every act but the close, 30
intervals) and the hole seed (every act and the close, 20 intervals) run with U24_RIDES unset; the sha256 of every
array of the board at the end and the clicks lines' count printed. Run once with PYTHONPATH on the pristine src
(git archive of 7dc781bc2) and once on the worktree's src; the digests must be equal. Usage: python off_flag_check.py
<label>; output off_flag_check_<label>.json beside the script."""

import hashlib
import json
import os
import sys
from pathlib import Path

LABEL = sys.argv[1] if len(sys.argv) > 1 else "worktree"
os.environ.pop("U24_RIDES", None)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

import event_universe  # noqa: E402
from event_universe import seed, world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import bare_torus, node_arrays, uniform_sea  # noqa: E402


def board_of(folder, intervals, lay):
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    lines = []
    kept = seed.uniform_seed
    if lay is not None:
        seed.uniform_seed = lay
    try:
        board = Lattice(load_world(bare_torus(folder, 3, intervals)), output=lines.append)
    finally:
        seed.uniform_seed = kept
    return board, lines


def digest_of(board):
    found = hashlib.sha256()
    for key in sorted(node_arrays(board), key=str):
        for array in node_arrays(board)[key]:
            found.update(str(key).encode())
            found.update(json.dumps([int(v) for v in np.asarray(array, dtype=object).reshape(-1)]).encode())
    return found.hexdigest()


if __name__ == "__main__":
    base = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r6_off_{LABEL}"
    out = {"label": LABEL, "src": str(Path(event_universe.__file__).resolve().parent)}
    board, lines = board_of(base / "sea", 40, uniform_sea)
    for _ in range(30):
        board.advanced_to_the_close()
    out["sea_30_digest"] = digest_of(board)
    out["sea_30_X_centre"] = int(board.states[board.held[0]].lines[0].now[1, 1, 1])
    board, lines = board_of(base / "hole", 30, None)
    for _ in range(20):
        board.step()
    out["hole_20_digest"] = digest_of(board)
    out["hole_20_lines"] = len(lines)
    out["hole_20_births"] = sum(1 for line in lines if "senses" in line)
    (HERE / f"off_flag_check_{LABEL}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))
