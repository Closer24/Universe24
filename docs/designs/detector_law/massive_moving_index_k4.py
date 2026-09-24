"""The receding index row at k = 4 (one Link every FOUR intervals, beta = 1 / (4 c) = 0.433 c,
the motion pair [K^2, K^2 - 3] = [16, 13], gamma_m^2 = 16 / 13): the script's number on the
declared geometry of DECLARATIONS.md section 11 (the chain of 4000, the source at 800, the probe
at 2400, the block of side 24 from 1500 stepping away from interval 3000, the window [3800, 5400]),
by `massive_moving_index.py`'s `receding_declared` (imported, nothing re-derived) with its motion
integers set to K = 4 and the same-Node scheme of the declared row. The PIN of the k = 4 worlds
(`index_moving_long_k4_away.json` with its rest and reference worlds; the rest world's light clock
[2243, 10000] on N = 64 is the block-frame frequency gamma_m omega (1 - beta) = 0.02202 per
interval, the same convention), a COMPUTATION written BLIND on 2026-09-24 before any reading of
those worlds (the Preliminary Runner holds its k = 4 readings unrelayed until this number is on
main; the Boss's order of 12:45Z). The reader of record is section 11's: the probe's phase over
the window against the reference and its drift between the window's halves, GAMEBOARD.

    PYTHONPATH=src python docs/designs/detector_law/massive_moving_index_k4.py > docs/designs/detector_law/massive_moving_index_k4.out
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import massive_moving_index as mmi  # noqa: E402

K = 4


def main() -> None:
    mmi.K = K
    mmi.BETA = 1 / (K * mmi.C)
    mmi.GAMMA2 = K * K / (K * K - 3)
    mmi.GAMMA = np.sqrt(mmi.GAMMA2)
    mmi.COUPLING = "same_node"
    print(
        f"THE RECEDING INDEX AT K = {K}: beta = {mmi.BETA:.4f} c, the motion pair [{K * K}, {K * K - 3}],"
        f" gamma_m^2 = {mmi.GAMMA2:.4f}, gamma_m = {mmi.GAMMA:.4f}; the block-frame frequency away"
        f" {mmi.GAMMA * 0.035 * (1 - mmi.BETA):.5f} per interval (the rest world's clock [2243, 10000] on N = 64"
        f" = {0.2243 * 2 * np.pi / 64:.5f}); the same-Node scheme, the declared geometry of section 11"
    )
    mmi.receding_declared()


if __name__ == "__main__":
    main()
