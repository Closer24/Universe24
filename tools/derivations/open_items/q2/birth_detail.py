"""The base run of the transformed check read in detail (hand q2): the sea plus one quantum at (1, 0, 0) on the bare 3-cube at den 1,021, the Link close with the current's orientation over 8 intervals; per birth the Link, the current and the children's Nodes; the Node's count of integers and the largest bit length before and after the births (tools/node_integers.py, loaded by its path); the children's charge per record over the board.

    PYTHONPATH=src python tools/derivations/q2/birth_detail.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
for place in (str(ROOT), str(ROOT / "src")):
    if place not in sys.path:
        sys.path.insert(0, place)

from event_universe import conversion  # noqa: E402
from event_universe.loader.derived import count_wall  # noqa: E402
from tests.laws import load_file  # noqa: E402

link_birth = load_file("link_birth", HERE.parent / "link_birth.py")
TOOL = load_file("node_integers", ROOT / "tools" / "node_integers.py")

lines: list = []
board = link_birth.seeded_board(Path("/dev/shm/tmp/q2_detail"), 1021, 8, lines, (1, 0, 0))
seed = board.world.seed
child = min((t[0][0] for t in conversion.birth_of(board.families, seed)), key=lambda k: count_wall(board.families[k], board.world.quantum_action))
log: list = []
out = []
before = TOOL.line_of(board)
for _ in range(8):
    kept = board.advanced_to_the_close()
    board.closed_after(kept)
    link_birth.link_close(board, kept, "current", child, log)
    out.append({"interval": board.interval, "births": [{"link": e["link"], "axis": e["axis"], "current": e["current"], "plus": e["plus"], "minus": e["minus"], "take": e["take"]} for e in log if e["interval"] == board.interval and "plus" in e], "refused": {k: sum(1 for e in log if e["interval"] == board.interval and e.get("refused") == k) for k in ("tie", "stop", "lay")}, "charge": link_birth.charge_of(board, child), "integers": TOOL.total_of(board), "largest_bits": TOOL.largest_bits(board)[0]})
after = TOOL.line_of(board)
print(json.dumps({"before": {k: before[k] for k in ("integers", "largest_bit_length", "same_at_every_node")}, "after": {k: after[k] for k in ("integers", "largest_bit_length", "same_at_every_node")}, "child_wall": count_wall(board.families[child], board.world.quantum_action), "light_unit": board.credit.units[seed], "intervals": out}, indent=None))
