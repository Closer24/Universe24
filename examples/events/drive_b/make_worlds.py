"""Write the deciding worlds of `drive-b-v1`, the directional drive of a body
(form B in the integer form (c) of docs/designs/light_speed/FORM.md section
3.1; docs/designs/drive_b/DESIGN.md sections 2 and 4; the model owner's
approval of form B, 2026-09-22, record 652 of the log of 2026-09-20), and
their expectations before the runs (`expectations.json`).

The rule is a world key, `drive_b`, absent by default: under it a body's
three drive accumulators gain p_a Q each against ONE wall W = Q^2 S M +
|p|_1 T_h (T_h = isqrt(3 Q^2) = 110, the flight table's heading resolution,
formed at load), and the axis furthest over the wall makes the Link, the
others keeping their overflow (`core.integer.by_line`): the Bresenham line of
the momentum, one Link per interval at most, no coincident fire lost, no
root at run time. With the key absent every registered world reads as it
did, byte for byte.

Six worlds, each an open box of 41 x 41 x 41 (`"law": "beam"`, K 2^20, N
64, `release` [1, 2^20] so no row is born within the run, `suspension` 0,
`width` 1, 200 intervals), one free body of the shipped family `probe` (content 64,
Q S M = 4096, Q^2 S M = 262144) at the centre (20, 20, 20), the six open
faces the detectors. The momentum has |p|_1 = 6000 on all three, so the
wall under the key is one number, W = 262144 + 660000 = 922144:

- `axis_b`, `plane_b`, `cube_b`: p = (6000, 0, 0), (3000, 3000, 0) and
  (2000, 2000, 2000) under the key;
- `axis_main`, `plane_main`, `cube_main`: the same bodies without the key,
  the controls on the per-axis drive of BEAM_LAW note 17 (the refuting
  readings, registered so that the difference is a detector's).

The pins, written here before any run, each with its kind, derived by the
host's replay of the count rule (the same integers as
docs/designs/drive_b/drive_b_map.py (A)):

- the DETECTOR reading: the body's click on a face (`click` with
  `detector` `face:+x`, its `tick`, its `node` the last Node inside). Under
  the key: tick 51 from (40, 20, 20), tick 101 from (40, 40, 20), tick 152
  from (40, 40, 40), the k-th x Link at the first n with n |p_x| Q >= k W
  (the 21st, the escape, at ceil(21 W / (|p_x| Q))), x never deferred (the
  lowest axis wins every tie) and y, z trailing by one Link; the tolerance
  one interval on the tick (the engine's numbering of its first advance),
  none on the face and the Node. The controls: tick 36, 50 and 65 from
  (40, 20, 20), y and z never moved (every coincident fire lost);
- the GAMEBOARD readings: every `step` line's Node within one Link of the
  line of p through the centre (the distance 0, at most 0.707, at most
  0.816); the `drive` accumulators on every `step` line below 3 W (the
  bound proved in the design's section 4) and the largest observed below W
  + 2 max |p_a| Q; `fast_steps` 0 on the axis world.

Nothing here is a test: the runs are made once and registered (`README.md`,
docs/EXPERIMENTS.md, docs/VALIDATION.md); a reading outside its pin is
reported with its numbers, never moved.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events.world import LABEL_SCALE, T_HEADING  # noqa: E402

Json = dict[str, object]

# The line drive is the law's drive since 2026-09-22 (record 972; DEFAULT.md):
# the `_b` worlds declare nothing, the `_main` controls the drive of history.
HISTORY_IDENTITY = "per-axis-drive-v1"
Q = LABEL_SCALE
T_H = T_HEADING
BOX = 41
CENTRE = BOX // 2
CONTENT = 64
WIDTH = 1
TICKS = 200
P1 = 6000
MOMENTA = {
    "axis": [P1, 0, 0],
    "plane": [P1 // 2, P1 // 2, 0],
    "cube": [P1 // 3, P1 // 3, P1 // 3],
}
TICK_TOLERANCE = 1


def world(name: str, momentum: list[int], key: bool) -> Json:
    document: Json = {
        "law": "beam",
        "model_id": f"beam-drive-b-{name}-v1",
        "shape": [BOX, BOX, BOX],
        "boundary": "open",
        "ticks": TICKS,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1 << 20],
        "suspension": 0,
        "width": WIDTH,
        "families": [{"name": "probe", "quantum": 0, "charge": 0, "phase": False}],
        "measured": [
            {
                "position": [CENTRE, CENTRE, CENTRE],
                "family": "probe",
                "amount": CONTENT,
                "momentum": list(momentum),
            }
        ],
    }
    if not key:
        document["per_axis_drive"] = True
    return document


def worlds() -> dict[str, Json]:
    found: dict[str, Json] = {}
    for stem, momentum in MOMENTA.items():
        found[f"{stem}_b"] = world(f"{stem}_b", momentum, True)
        found[f"{stem}_main"] = world(f"{stem}_main", momentum, False)
    return found


# -- the host's replay of the two rules, the pins' derivation -----------------------


def wall(momentum: list[int]) -> int:
    return Q * Q * WIDTH * CONTENT + sum(abs(c) for c in momentum) * T_H


def replay_key(momentum: list[int]) -> Json:
    """`drive-b-v1` on the body from the centre: the escape's tick, face and
    Node, the Links per axis before it, the largest distance of a Node from
    the line of p and the largest |drive_a| (docs/designs/drive_b/DESIGN.md
    section 4; the same integers as `core.integer.by_line`)."""
    w = wall(momentum)
    drives = [0, 0, 0]
    position = [CENTRE] * 3
    links = [0, 0, 0]
    farthest = 0.0
    largest = 0
    norm = math.sqrt(sum(c * c for c in momentum))
    for tick in range(1, TICKS + 1):
        for axis in range(3):
            if momentum[axis]:
                drives[axis] += momentum[axis] * Q
        over = [a for a in range(3) if momentum[a] and abs(drives[a]) >= w]
        if not over:
            continue
        chosen = max(over, key=lambda a: (abs(drives[a]), -a))
        sign = 1 if drives[chosen] > 0 else -1
        drives[chosen] -= sign * w
        largest = max(largest, max(abs(d) for d in drives))
        if not 0 <= position[chosen] + sign < BOX:
            return {
                "tick": tick,
                "face": ("face:+" if sign > 0 else "face:-") + "xyz"[chosen],
                "node": list(position),
                "links": links,
                "off_line": round(farthest, 3),
                "largest_drive": largest,
            }
        position[chosen] += sign
        links[chosen] += sign
        r = [position[a] - CENTRE for a in range(3)]
        along = sum(r[a] * momentum[a] for a in range(3)) / norm
        farthest = max(farthest, math.sqrt(max(0.0, sum(c * c for c in r) - along * along)))
    raise ValueError("the body did not escape within the run")


def replay_main(momentum: list[int]) -> Json:
    """The per-axis drive of BEAM_LAW note 17 (`engine.step_axis`, the first
    axis to fire steps, a later coincident fire lost): the control's escape."""
    drives = [0, 0, 0]
    position = [CENTRE] * 3
    links = [0, 0, 0]
    lost = 0
    for tick in range(1, TICKS + 1):
        fired = None
        for axis in range(3):
            p = momentum[axis]
            if p == 0:
                continue
            divisor = Q * WIDTH * CONTENT + abs(p)
            drives[axis] += p
            count = min(abs(drives[axis]) // divisor, 1)
            if drives[axis] < 0:
                count = -count
            drives[axis] -= count * divisor
            if count and fired is None:
                fired = (axis, count)
            elif count:
                lost += 1
        if fired is None:
            continue
        chosen, sign = fired
        if not 0 <= position[chosen] + sign < BOX:
            return {
                "tick": tick,
                "face": ("face:+" if sign > 0 else "face:-") + "xyz"[chosen],
                "node": list(position),
                "links": links,
                "fires_lost": lost,
            }
        position[chosen] += sign
        links[chosen] += sign
    raise ValueError("the control did not escape within the run")


def expectation(stem: str, momentum: list[int], key: bool) -> Json:
    w = wall(momentum)
    manhattan = sum(abs(c) for c in momentum)
    euclid = math.sqrt(sum(c * c for c in momentum))
    if key:
        escape = replay_key(momentum)
        return {
            "momentum": list(momentum),
            "wall": w,
            "pace_per_axis": [abs(c) * Q / w for c in momentum],
            "pace_manhattan": manhattan * Q / w,
            "pace_euclidean": euclid * Q / w,
            "click": {
                "kind": "DETECTOR",
                "line": "click on a face, the body's escape",
                "tick": escape["tick"],
                "tolerance": TICK_TOLERANCE,
                "face": escape["face"],
                "node": escape["node"],
                "links_before": escape["links"],
                "derivation": (
                    "the k-th x Link at the first n with n |p_x| Q >= k W, the 21st (the escape from "
                    f"x = 40) at ceil(21 x {w} / ({abs(momentum[0])} x {Q})) = "
                    f"{math.ceil(21 * w / (abs(momentum[0]) * Q))}; x wins every tie, y and z trail by one Link"
                ),
            },
            "line": {
                "kind": "GAMEBOARD",
                "line": "step (every Node within one Link of the line of p)",
                "farthest": escape["off_line"],
                "bound": 1.0,
            },
            "accumulators": {
                "kind": "GAMEBOARD",
                "line": "step (the drive fields)",
                "largest_replayed": escape["largest_drive"],
                "bound_proved": 3 * w,
                "bound_observed": w + 2 * max(abs(c) for c in momentum) * Q,
            },
            "fast_steps": {
                "kind": "GAMEBOARD",
                "line": "run.json",
                "value": 0 if stem == "axis" else None,
            },
        }
    escape = replay_main(momentum)
    return {
        "momentum": list(momentum),
        "divisors": [Q * WIDTH * CONTENT + abs(c) for c in momentum],
        "pace_per_axis": [abs(c) / (Q * WIDTH * CONTENT + abs(c)) if c else 0.0 for c in momentum],
        "click": {
            "kind": "DETECTOR",
            "line": "click on a face, the body's escape (the per-axis drive of BEAM_LAW note 17)",
            "tick": escape["tick"],
            "tolerance": TICK_TOLERANCE,
            "face": escape["face"],
            "node": escape["node"],
            "links_before": escape["links"],
            "fires_lost": escape["fires_lost"],
            "derivation": (
                "by_drive per axis against Q S M + |p_a| with the first axis to fire stepping and a "
                "later coincident fire lost: y and z never move on the diagonals"
            ),
        },
    }


def expectations() -> Json:
    found: Json = {
        "format": "drive-b-expectations-v1",
        "drive": "line (the law's, nothing declared) on the `_b` worlds; per_axis (the drive of history, "
        f"the key per_axis_drive, {HISTORY_IDENTITY}) on the `_main` controls",
        "constants": {"Q": Q, "T_h": T_H, "content": CONTENT, "width": WIDTH, "box": BOX},
        "worlds": {},
        "derivations": {
            "wall": "W = Q^2 S M + |p|_1 T_h, T_h = isqrt(3 Q^2) = 110 (DESIGN.md section 2; FORM.md 3.1 (c))",
            "pace": (
                "per axis |p_a| Q / W Links per interval; Manhattan |p|_1 Q / W; Euclidean |p|_2 Q / W; "
                "on a heading form B's |p| x 64 / (Q S M x 64 + 110 |p|); the cap 64 / 110"
            ),
            "click": (
                "the host's replay of by_line from the centre of the open box (drive_b_map.py (A)): "
                "the escape's tick exact up to the engine's numbering of its first advance (one "
                "interval), the face and the Node exact"
            ),
            "controls": "the host's replay of the per-axis drive (engine.step_axis) with the lost fire",
            "line": "every step's Node within one Link of the line of p (DESIGN.md section 4, GAMEBOARD)",
            "accumulators": "|drive_a| < 3 W proved (DESIGN.md section 4, S2); observed below W + 2 max |p_a| Q",
        },
    }
    for stem, momentum in MOMENTA.items():
        found["worlds"][f"{stem}_b"] = expectation(stem, momentum, True)  # type: ignore[index]
        found["worlds"][f"{stem}_main"] = expectation(stem, momentum, False)  # type: ignore[index]
    return found


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    expected = expectations()
    existing = HERE / "expectations.json"
    if existing.exists():
        # The run blocks (the source sha, the digests, the readings) are
        # written after the runs and kept.
        previous = json.loads(existing.read_text(encoding="utf-8"))
        if "runs" in previous:
            expected["runs"] = previous["runs"]
    existing.write_text(json.dumps(expected, indent=1) + "\n", encoding="utf-8")
    print(existing.relative_to(ROOT))
    for name, entry in expected["worlds"].items():  # type: ignore[union-attr]
        print(name, json.dumps(entry["click"]))


if __name__ == "__main__":
    main()
