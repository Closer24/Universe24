"""Probe: the adopted gate (54b9e6a63, scribe-5 a0dd6b376) on runner/board.py, against wraps it may not name.

Each plant replaces board.py's wrap body (the carry's remainder) with another spelling of x mod side, for x in [-1, side],
and is scanned as tensor24/runner/board.py by scribe_scan.scan; CAUGHT where a BLOCK rule's count rises over the board
as it stands. Each plant is also run, to show it is a wrap: wrap(x, side) == x mod side for x in -1 .. side.
usage: python -I gate_board_dodges.py <worktree>"""

import importlib.util
import sys
from collections import Counter
from pathlib import Path

WT = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("scribe_scan", WT / "tools/derivations/open_items/scribe_scan.py")
gate = importlib.util.module_from_spec(spec)
sys.modules["scribe_scan"] = gate
spec.loader.exec_module(gate)
REL = "tensor24/runner/board.py"
SOURCE = (WT / "src" / REL).read_text()
BODY = "    _, kept = carry(x, side, 0)\n    return kept\n"
PLANTS = {
    "control: x % side": "    return x % side\n",
    "control: np.mod": "    return np.mod(x, side)\n",
    "control: np.take with mode=": "    return np.take(np.arange(side), x, mode=\"wrap\")\n",
    "a doubled range indexed": "    return np.concatenate((np.arange(side), np.arange(side), np.arange(side)))[x + side]\n",
    "np.tile indexed": "    return np.tile(np.arange(side), 1 + 1 + 1)[x + side]\n",
    "np.resize indexed": "    return np.resize(np.arange(side), (1 + 1 + 1) * side)[x + side]\n",
    "np.unravel_index's second part": "    return np.unravel_index(x + side, (1 + 1 + 1, side))[1]\n",
    "== as the whether (no ordering)": "    return x + side * (x == 0 - 1) - side * (x == side)\n",
    "np.equal as the whether": "    return x + side * np.equal(x, 0 - 1) - side * np.equal(x, side)\n",
    "np.greater_equal as the whether": "    return x + side * np.less(x, 0) - side * np.greater_equal(x, side)\n",
    "np.digitize as the whether": "    return x + side - side * np.digitize(x, [0, side])\n",
    "a getattr of a built name": "    return getattr(np, \"re\" + \"mainder\")(x, side)\n",
    "vars(np) by key": "    return vars(np)[\"remainder\"](x, side)\n",
}
base = Counter(h.rule for h in gate.scan(REL, SOURCE) if h.tier == "BLOCK")
assert BODY in SOURCE
missed = 0
for name, body in PLANTS.items():
    source = SOURCE.replace(BODY, body)
    hits = Counter(h.rule for h in gate.scan(REL, source) if h.tier == "BLOCK")
    rose = {rule: hits[rule] - base[rule] for rule in hits if hits[rule] > base[rule]}
    space = {"np": __import__("numpy")}
    exec(compile("def wrap(x, side):\n" + body, "plant", "exec"), space)
    side = 5
    is_wrap = all(int(space["wrap"](__import__("numpy").array(x), side)) == x % side for x in range(-1, side + 1))
    missed += not rose and is_wrap
    print(f"{'CAUGHT' if rose else 'MISSED'} {str(rose or ''):<40} a wrap: {is_wrap!s:<5} {name}")
print("wraps the gate misses:", missed)
