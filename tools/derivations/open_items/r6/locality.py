"""Hand R6 (2026-10-25): locality of the mended inverse (U24_RIDES=2 with the local trigger). On the open standing board
at interval t (the single-Node turn at the centre at 7), the post-state Z is stepped back twice: as it is, and with
one integer changed two Links away from the centre (the light's level now at (0, 0, 1) raised by one, and in a second
probe the volume's level now there). The centre's every array after the step back is compared bit for bit; the
Nodes where the two step-backs differ are listed (they lie within one Link of the changed Node). Usage: python
locality.py <t>; prints JSON. Integers only."""

import copy
import json
import os
import sys
from pathlib import Path

T_AT = int(sys.argv[1]) if len(sys.argv) > 1 else 7
os.environ["U24_RIDES"] = "2"
sys.argv[1:] = ["2"]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ride_local as rl  # noqa: E402

import numpy as np  # noqa: E402

from event_universe import flux, records  # noqa: E402
from tests.laws_universe import node_arrays  # noqa: E402

assert flux.RIDES and flux.MENDED
CHANGED, CENTRE = (0, 0, 1), (1, 1, 1)


def raised(board, index, line_number, at):
    state = board.states[index]
    line = state.lines[line_number]
    now = np.array(line.now, dtype=object, copy=True)
    now[at] = now[at] + 1
    lines = list(state.lines)
    lines[line_number] = records.Record(np.asarray(now, dtype=np.asarray(line.now).dtype), line.before, line.remainder)
    state.lines = lines


def differing_nodes(a, b):
    found = set()
    for key in a:
        for x, y in zip(a[key], b[key], strict=True):
            for n in np.argwhere(np.asarray(x, dtype=object) != np.asarray(y, dtype=object)):
                found.add(tuple(int(v) for v in n))
    return sorted(found)


def links_between(p, q):
    return sum(min((a - b) % 3, (b - a) % 3) for a, b in zip(p, q))


if __name__ == "__main__":
    board, _lines = rl.board_of(Path("/dev/shm/tmp/r6_locality"), T_AT + 5, rl.standing_seed)
    for _ in range(T_AT):
        board.advanced_to_the_close()
    turned = [tuple(int(v) for v in n) for n in np.argwhere(board.turned)]
    out = {"t": T_AT, "turned_at_t": turned, "changed_node": CHANGED, "links_from_centre": links_between(CHANGED, CENTRE), "probes": []}
    plain = copy.deepcopy(board)
    plain.step_inverse()
    plain_arrays = node_arrays(plain)
    for name, index, line_number in (("light level now", board.world.seed, 0), ("volume level now", rl.holder_of(board), 0)):
        probe = copy.deepcopy(board)
        raised(probe, index, line_number, CHANGED)
        probe.step_inverse()
        nodes = differing_nodes(node_arrays(probe), plain_arrays)
        centre_equal = CENTRE not in nodes
        out["probes"].append({"changed": name, "centre_bit_for_bit": centre_equal, "nodes_differing": nodes, "largest_links_from_changed": max((links_between(n, CHANGED) for n in nodes), default=0), "turned_back_plain": [tuple(int(v) for v in n) for n in np.argwhere(plain.turned)]})
    print(json.dumps(out, indent=1))
