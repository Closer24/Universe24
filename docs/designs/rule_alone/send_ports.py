"""THE DIAGNOSTIC OF RECORD 2197 (the Boss, 2026-09-26; the model owner: "an event replicates
itself in all directions; it is not logical that it does not replicate in a certain direction;
there is no such thing as motion, motion is the replication of events at the Nodes"): a free
packet under the rule 9.57 (1) with THE SEND DECLARED ON FEWER THAN SIX PORTS (the step's send,
the ledger's primitive 13), to show what a broken symmetry does to motion. HOST checking code
(record 2135), the rule's transcription of rule_alone.py with one change: the arrival at a Node
through its Port -a is the neighbour's send through its Port +a, and a neighbour that does not
send on +a delivers nothing there; the own term S and the wall w are the six-Port rule's,
unchanged, so the declaration changes only what arrives.

The sends tried: all six (the law's own, the control); five (no send toward +x); four (no send
along x); three (+x, +y, +z only). The packet: a Gaussian of rms 4.2 of the kind [800, 850] at
amplitude 2^11, at rest and moving at the group pace 0.1 along +x (K by item9_pair.wave_number),
on [160, 48, 48] periodic, 200 intervals, the readings every 25 (GAMEBOARD of the runner; a first run
of 600 intervals every 100 showed the free packet filling the periodic board by 200, so the
readings are taken before that): the
envelope's centroid, its rms, the total norm now^2 + before^2 over its start, and the level's
maximum; a level beyond 2^40 ends the run as unstable.

    PYTHONPATH=src python docs/designs/rule_alone/send_ports.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import item9_pair as Pm  # noqa: E402
import rule_alone as R  # noqa: E402

SHAPE = (160, 48, 48)
WRAP = (True, True, True)
SIGMA = 4.2
AMPLITUDE = 1 << 11
INTERVALS = 200
EVERY = 25
UNSTABLE = 1 << 40
SENDS = {
    "six": ("+x", "-x", "+y", "-y", "+z", "-z"),
    "five_no_plus_x": ("-x", "+y", "-y", "+z", "-z"),
    "four_no_x": ("+y", "-y", "+z", "-z"),
    "three_plus": ("+x", "+y", "+z"),
}
AXIS = {"x": 0, "y": 1, "z": 2}


def arrivals(a: np.ndarray, sends: tuple[str, ...]) -> np.ndarray:
    """What a Node receives: for each Port +a in the sender's declaration, the neighbour at -a
    delivers its level here (np.roll by +1 along the axis brings a[i - 1] to i); for -a the
    neighbour at +a (a roll by -1). A Port not declared delivers nothing."""
    total = np.zeros_like(a)
    for port in sends:
        sign, axis = port[0], AXIS[port[1]]
        total += np.roll(a, 1 if sign == "+" else -1, axis=axis)
    return total


def run(sends: tuple[str, ...], moving: bool) -> dict:
    num = np.full(SHAPE, 800, dtype=R.INT)
    den = np.full(SHAPE, 850, dtype=R.INT)
    read, own, wall = R.coefficients(num, den, np.zeros(SHAPE, dtype=R.INT))
    cos0 = float(R.rest_rotation(read, own, wall)[0, 0, 0])
    grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in SHAPE], indexing="ij")
    centre = (40.0, 24.0, 24.0)
    r2 = sum((g - c) ** 2 for g, c in zip(grids, centre, strict=True))
    envelope = AMPLITUDE * np.exp(-r2 / (2 * SIGMA * SIGMA))
    if moving:
        k, wk = Pm.wave_number(0.1, 800, 850)
        dx = grids[0] - centre[0]
        now = np.rint(envelope * np.cos(k * dx - wk / 2)).astype(R.INT)
        before = np.rint(envelope * np.cos(k * dx + wk / 2)).astype(R.INT)
    else:
        k, wk = 0.0, 0.0
        now = np.rint(envelope).astype(R.INT)
        before = np.rint(envelope * cos0).astype(R.INT)
    remainder = np.zeros(SHAPE, dtype=R.INT)
    norm0 = float((now.astype(np.float64) ** 2 + before.astype(np.float64) ** 2).sum())
    rows: list[dict] = []
    unstable_at = None
    for t in range(INTERVALS + 1):
        if t % EVERY == 0:
            n = now.astype(np.float64)
            b = before.astype(np.float64)
            weight = n * n + b * b
            cx, cy, cz = R.centroid(weight)
            total = float(weight.sum())
            rms = math.sqrt(
                float(
                    (weight * ((grids[0] - cx) ** 2 + (grids[1] - cy) ** 2 + (grids[2] - cz) ** 2)).sum()
                )
                / total
                / 3.0
            )
            rows.append(
                {
                    "t": t,
                    "centroid": [cx, cy, cz],
                    "rms": rms,
                    "norm_over_start": total / norm0,
                    "level_max": int(np.abs(now).max()),
                }
            )
        if t == INTERVALS:
            break
        total_int = read * arrivals(now, sends) + own * now - wall * before + remainder
        nxt = np.floor_divide(total_int, wall)
        now, before, remainder = nxt, now, total_int - wall * nxt
        if int(np.abs(now).max()) > UNSTABLE:
            unstable_at = t + 1
            break
    return {
        "sends": list(sends),
        "moving": moving,
        "k": k,
        "omega_k": wk,
        "cos_omega_vacuum_six_ports": cos0,
        "unstable_at": unstable_at,
        "readings": rows,
    }


def main() -> None:
    out: dict = {"shape": SHAPE, "sigma": SIGMA, "amplitude": AMPLITUDE, "runs": []}
    for name, sends in SENDS.items():
        for moving in (False, True):
            result = run(sends, moving)
            result["name"] = name
            out["runs"].append(result)
            first, last = result["readings"][0], result["readings"][-1]
            speed = (last["centroid"][0] - first["centroid"][0]) / max(1, last["t"])
            print(
                f"{name:16s} {'moving' if moving else 'at rest'}: centroid x {[round(r['centroid'][0], 1) for r in result['readings']]}; "
                f"speed {speed:+.4f} (expected {0.1 if moving else 0.0}); rms {[round(r['rms'], 1) for r in result['readings']]}; "
                f"norm/start {[round(r['norm_over_start'], 3) for r in result['readings']]}; "
                f"level max {last['level_max']}; unstable at {result['unstable_at']}"
            )
    (Path(__file__).resolve().parent / "send_ports.json").write_text(
        json.dumps(out, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
