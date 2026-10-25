"""cs2's runner: ma2's Node (the engine's own, src untouched; ma2's diag line per interval) with the screw lay on the plane at the gap 0: a Z_4 phase t(k) at every Node from a 2x2x2 cell extended per axis (periodic or antiperiodic by two Links), the pair (now, before) turned by quarters, the amplitude A over the sea's drift: re += (A cos t, A sin t), and where `complex` is given im += (A sin t, -A cos t) (the quadratic forms uniform at every Node). The diag at i = 0 (the lay's F, twist, share) is written first.

Usage: python cs_run.py <world.json> <out.json> back N screw <cell 8 digits> <eta 3 digits> <A> [complex] [lays <lays.json>]
Integers only."""

from __future__ import annotations

import json
import sys
from typing import Any

sys.path.insert(0, "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs2/tools/derivations/open_items/ma2")

import numpy as np  # noqa: E402

import ma_run  # noqa: E402
from event_universe import run, seed  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.rows import PLANE, zeros  # noqa: E402

COS = (1, 0, -1, 0)
SIN = (0, 1, 0, -1)


def phases(shape: tuple[int, ...], cell: list[int], eta: list[int]) -> Any:
    t = zeros(shape)
    for at in np.ndindex(*shape):
        x, y, z = at
        base = cell[((x % 2) * 2 + (y % 2)) * 2 + (z % 2)]
        shift = 2 * (eta[0] * (x // 2) + eta[1] * (y // 2) + eta[2] * (z // 2))
        t[at] = (base + shift) % 4
    return t


class CsNode(ma_run.MaNode):
    """ma2's Node with the screw lay on the gap-0 plane after the world's lays and the fourth form."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any], lays: list[dict[str, Any]], screw: dict[str, Any] | None) -> None:
        super().__init__(universe, world, lays)
        self.screw = screw
        if screw is not None:
            gap0 = self.row(PLANE, gap=0)
            rec0 = self.records().index(gap0)
            t = phases(self.shape, screw["cell"], screw["eta"])
            amp = int(screw["A"])
            c = np.vectorize(lambda p: COS[int(p)], otypes=[object])(t)
            s = np.vectorize(lambda p: SIN[int(p)], otypes=[object])(t)
            re_now, re_before = amp * c, amp * s
            if screw.get("complex"):
                im_now, im_before = amp * s, -amp * c
            else:
                im_now, im_before = zeros(self.shape), zeros(self.shape)
            self.lay(rec0, Ellipsis, (re_now, re_before, im_now, im_before))
            self.start_content = self.content()
            self.log.append({"event": "lay_screw", "i": 0, "cell": screw["cell"], "eta": screw["eta"], "A": amp, "complex": bool(screw.get("complex")), "phases": [int(v) for v in t.reshape(-1)]})
        self.diag.append(self.read_diag())


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    lays = []
    if "lays" in argv:
        with open(argv[argv.index("lays") + 1], encoding="utf-8") as f:
            lays = json.load(f)
    screw = None
    if "screw" in argv:
        k = argv.index("screw")
        screw = {"cell": [int(ch) for ch in argv[k + 1]], "eta": [int(ch) for ch in argv[k + 2]], "A": int(argv[k + 3]), "complex": "complex" in argv}
    node = CsNode(universe, world, lays, screw)
    intervals = int(world["intervals"])
    out = lambda line: print(line, flush=True)
    d0 = node.diag[0]
    out(json.dumps({"seed_diag": {k: d0[k] for k in ("F_links_zero", "twist_links_nonzero", "F_abs_max", "light_share_min_max_hundredths", "X_min", "X_max", "bits")}}))
    rows, nodes, hashes = run.forward(node, intervals, back, out)
    kept_log = list(node.log)
    returned = run.run_back(node, hashes) if back else None
    if returned:
        out(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in node.counts.items()}
    out(json.dumps({"counts": counts}))
    found = {
        "world": world,
        "universe": universe,
        "lays_fourth": lays,
        "screw": screw,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(seed.sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T,
        "gamma": node.gamma,
        "G": node.G,
        "counts": counts,
        "turns": node.turns,
        "rows": rows,
        "nodes": nodes,
        "run_back": returned,
        "log": kept_log,
        "diag": node.diag,
    }
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(found, f)


if __name__ == "__main__":
    main(sys.argv)
