"""Hand r5 (2026-10-25): the inverse under the local trigger reads the Node and its six Links alone (U24_RIDES=3).

On the open standing board (80 forward), at every interval t: the true post-state Z_t one step back (the reference), and
again with Z_t changed at one Node by +1 on the light's two levels and the volume's two levels: at a Node two Links from
the centre (0, 0, 1), and, the control, at a Node one Link from it (1, 1, 0). Read: the intervals at which the centre's
inverse (every array at the centre) differs from the reference. Output locality.json."""

import copy
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.argv = [sys.argv[0], "3", "open"]
import top_local as tl  # noqa: E402

import numpy as np  # noqa: E402

from event_universe import records  # noqa: E402
from tests.laws_universe import CENTRE, node_arrays  # noqa: E402


def changed(board, at):
    b = copy.deepcopy(board)
    for index in (b.world.seed, b.held[0]):
        line = b.states[index].lines[0]
        now, before = (np.asarray(a, dtype=object).copy() for a in (line.now, line.before))
        now[at] += 1
        before[at] += 1
        b.states[index].lines[0] = records.Record(np.asarray(now, dtype=line.now.dtype), np.asarray(before, dtype=line.before.dtype), line.remainder)
    return b


def at_centre(arrays):
    return {k: tuple(int(np.asarray(a, dtype=object)[CENTRE]) for a in v) for k, v in arrays.items()}


def main():
    base = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / "r5_locality"
    board, _ = tl.board_of(base, 90, tl.standing_seed)
    boards = []
    for _ in range(80):
        board.advanced_to_the_close()
        boards.append(copy.deepcopy(board))
    found = {"two_links": [], "one_link": [], "intervals": 80, "turned_back_centre_reference": 0}
    for t, z in enumerate(boards, 1):
        ref = copy.deepcopy(z)
        ref.step_inverse()
        found["turned_back_centre_reference"] += int(np.asarray(ref.turned, dtype=bool)[CENTRE])
        reference = at_centre(node_arrays(ref))
        for name, at in (("two_links", (0, 0, 1)), ("one_link", (1, 1, 0))):
            b = changed(z, at)
            b.step_inverse()
            if at_centre(node_arrays(b)) != reference:
                found[name].append(t)
    found["two_links_intervals_changed"] = len(found["two_links"])
    found["one_link_intervals_changed"] = len(found["one_link"])
    (HERE / "locality.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
    print(json.dumps({k: (v if not isinstance(v, list) else v[:20]) for k, v in found.items()}))


if __name__ == "__main__":
    main()
