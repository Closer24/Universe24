"""Hand K2: the 128-bit edge of the engine's own width (loader/rooms.width_of) by bisection on Gamma at each den of the window (T 36,000, G 16), the volume holder's pair at Gamma above den, and T's bound from the one-quantum lay: the loader at den 1,021, Gamma 1,021 and T from 2^60 to 2^70 (the drift isqrt(T) and the lay isqrt(T div 2) against the amplitude bound A). Integers only.

Run: PYTHONPATH=<worktree>/src python tools/derivations/open_items/H-Constants-Of-The-Universe-2/k2_width_edge.py > tools/derivations/open_items/H-Constants-Of-The-Universe-2/k2_width_edge.txt
"""

from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path

from event_universe import world_files
from event_universe.core.ports import LINK_UNIT
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.lattice import Lattice
from event_universe.loader.rooms import width_of
from event_universe.loader.universe import universe_of, volume_pair
from event_universe.world_files import load_world

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from tests import laws_universe  # noqa: E402

BITS = 128


def width_at(den: int, gamma: int, action: int) -> int | None:
    try:
        fams = universe_of({"integers": {"den": den, "node_clock": gamma, "quantum_action": action}})[1]
        return width_of(fams, gamma, action, LINK_UNIT)
    except ValueError:
        return None


def edge(den: int, lo: int, hi: int, action: int) -> tuple[int, int | None, int | None]:
    """The largest Gamma in [lo, hi] with the width <= 128 (the width grows with Gamma), with the widths at it and one above."""
    while hi - lo > 1:
        mid = int(division_forward(lo + hi, 2, 0)[0])
        w = width_at(den, mid, action)
        if w is not None and w <= BITS:
            lo = mid
        else:
            hi = mid
    return lo, width_at(den, lo, action), width_at(den, lo + 1, action)


def main() -> None:
    out: dict[str, object] = {}
    for den, lo, hi in ((348893, 9000, 10000), (15162856759112389, 1000, 2500), (1655909141, 1000, 10000), (4471099877, 1000, 10000)):
        t0 = time.time()
        g, w, w1 = edge(den, lo, hi, 36000)
        out[f"den_{den}"] = {"Gamma_max_width_le_128": g, "width_at_Gamma_max": w, "width_at_Gamma_max_plus_1": w1, "seconds": int(time.time() - t0)}
        print(json.dumps(out[f"den_{den}"]), file=sys.stderr, flush=True)
    out["den_1021"] = {
        "width_at_Gamma_1021": width_at(1021, 1021, 36000),
        "width_at_Gamma_1022": width_at(1021, 1022, 36000),
        "volume_pair_at_1022": list(volume_pair(1021, 1022)),
        "width_at_Gamma_4096_if_loads": width_at(1021, 4096, 36000),
    }
    print(json.dumps(out["den_1021"]), file=sys.stderr, flush=True)
    folder = Path(tempfile.mkdtemp(prefix="k2edge_"))
    world_files.REPOSITORY_ROOT = folder
    lays = {}
    for e in (60, 64, 66, 67, 68, 70):
        action = 1 << e
        laws_universe.SMALL["integers"] = {"den": 1021, "node_clock": 1021, "quantum_action": action}
        try:
            world = load_world(laws_universe.bare_torus(folder, 3, 4))
            board = Lattice(world, output=None)
            board.step()
            lays[f"T_2^{e}"] = {
                "loaded": True,
                "A": world.amplitude_bound,
                "A_bits": world.amplitude_bound.bit_length(),
                "drift_isqrt_T_bits": largest_below(action).bit_length(),
                "lay_isqrt_T_div_2_bits": largest_below(action >> 1).bit_length(),
                "stepped": True,
            }
        except (ValueError, RuntimeError) as err:
            lays[f"T_2^{e}"] = {"loaded": False, "refusal": str(err)[:160]}
        print(json.dumps({e: lays[f"T_2^{e}"]}), file=sys.stderr, flush=True)
    out["T_bound_den_1021_Gamma_1021"] = lays
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
