"""Hand K2: the engine's own width (loader/rooms.width_of, the least width at which the amplitude bound holds the volume's deepest level) probed along Gamma at den 348,893 (T 36,000) and along T at den 1,021 (Gamma 1,021), G the engine's 16; the 128-bit edge of the principle "the constants are the largest the 128 bits allow", read bit for bit from the engine. Integers only.

Run: PYTHONPATH=<worktree>/src python tools/derivations/open_items/H-Constants-Of-The-Universe-2/k2_width_probe.py > tools/derivations/open_items/H-Constants-Of-The-Universe-2/k2_width_probe.txt
"""

from __future__ import annotations

import json
import sys
import time

from event_universe.core.ports import LINK_UNIT
from event_universe.loader import derived
from event_universe.loader.rooms import width_of
from event_universe.loader.universe import universe_of


def width_at(den: int, gamma: int, action: int) -> dict[str, int | str]:
    t0 = time.time()
    try:
        fams = universe_of({"integers": {"den": den, "node_clock": gamma, "quantum_action": action}})[1]
        width = width_of(fams, gamma, action, LINK_UNIT)
        bound = derived.amplitude_bound(fams, gamma, action, width, LINK_UNIT)
        return {"width": width, "A_bits": bound.bit_length(), "seconds": int(time.time() - t0)}
    except ValueError as e:
        return {"refused": str(e)[:120], "seconds": int(time.time() - t0)}


def main() -> None:
    out: dict[str, object] = {}
    for gamma in (7000, 8000, 9000, 10000, 11000, 12000, 14000):
        out[f"den_348893_Gamma_{gamma}_T_36000"] = width_at(348893, gamma, 36000)
        print(json.dumps({gamma: out[f"den_348893_Gamma_{gamma}_T_36000"]}), file=sys.stderr, flush=True)
    for action in (36000, 1 << 20, 1 << 24, 1 << 28, 1 << 32, 1 << 40, 1 << 48, 1 << 56):
        out[f"den_1021_Gamma_1021_T_{action}"] = width_at(1021, 1021, action)
        print(json.dumps({action: out[f"den_1021_Gamma_1021_T_{action}"]}), file=sys.stderr, flush=True)
    for action in (1 << 20, 1 << 28, 1 << 36):
        out[f"den_348893_Gamma_6000_T_{action}"] = width_at(348893, 6000, action)
        print(json.dumps({action: out[f"den_348893_Gamma_6000_T_{action}"]}), file=sys.stderr, flush=True)
    for den in (1655909141, 4471099877, 15162856759112389):
        out[f"den_{den}_Gamma_1000_T_36000"] = width_at(den, 1000, 36000)
        print(json.dumps({den: out[f"den_{den}_Gamma_1000_T_36000"]}), file=sys.stderr, flush=True)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
