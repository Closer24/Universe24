"""Hand r4: where the mended inverse (U24_RIDES=2) parts from the forward run on the hole seed with the close: N intervals forward, one back, the unequal entries per array; N = 3 (before any birth), 5 (after the births at 4), 20 and 60."""

import json
import os
import sys
from pathlib import Path

os.environ["U24_RIDES"] = sys.argv[1] if len(sys.argv) > 1 else "2"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
import numpy as np  # noqa: E402

from event_universe import world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import bare_torus, node_arrays  # noqa: E402


def run(folder, forward, close=True):
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    board = Lattice(load_world(bare_torus(folder, 3, forward + 10)))
    snaps = [node_arrays(board)]
    for _ in range(forward):
        if close:
            board.step()
        else:
            board.advanced_to_the_close()
        snaps.append(node_arrays(board))
    board.step_inverse()
    after = node_arrays(board)
    bad = {}
    for key in snaps[forward - 1]:
        if key not in after:
            bad[str(key)] = "missing"
            continue
        n = sum(int((np.asarray(x, dtype=object) != np.asarray(y, dtype=object)).sum()) for x, y in zip(snaps[forward - 1][key], after[key], strict=True))
        if n:
            name = board.families[key[0]].name
            bad[f"{name} {key[1]} {key[2:]}"] = n
    return {"forward": forward, "close": close, "unequal": bad, "records": {board.families[i].name: len(board.states[i].lines) for i in range(len(board.families))}}


if __name__ == "__main__":
    base = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / "r4_diag"
    found = [run(base / "a", 3), run(base / "b", 5), run(base / "c", 20), run(base / "d", 20, close=False)]
    print(json.dumps(found, indent=1, default=str))
