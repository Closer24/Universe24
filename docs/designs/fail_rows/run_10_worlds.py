"""Write the two worlds of row 10 under the one click (`opening_w27.json`,
`opening_w9.json`): a single opening of w Nodes in a wall, lit by one lamp
whose rows reach the opening in phase, re-emitting on a fan uniform in
angle, read by a screen of one-Node `sum` detectors L Links behind
(docs/designs/fail_rows/RUN_10.md, STEP 1: the worlds validated at load,
never run here). Existing keys only.

The geometry is the register's (examples/events/heisenberg/, A10): the
plane 120 x 161 x 1 (z periodic), the wall at x = 8, the opening centred
on y = 80, the screen at x = 116 (L = 108 Links), N = 64, K = 2^30; the
record form of `examples/events/amplitude/slits_huygens.json`: the family
`light` with the pair form of `phase_per_link` (8591334592 / 2^30 steps
per interval of age, the registered frequency), one lamp with the golden
wheel [2531, 4096], the opening's Nodes re-emitting (`rerelease`, the
equal split over the declared directions), the screen's pixels `sum`
detectors. The two families are declared inline (`light` as
`entities/families.json` declares it, key by key; `wall` the same): the
entity file is outside this folder's reach at load, as `j2_massive.json`
beside this file declares its families.

Two things differ from the two-slit world, both declarations:

- the lamp lights the whole opening with ONE record: one direction per
  opening Node, the primitive direction (a, b, 0) of the smallest a + |b|
  (then the earliest arrival) whose walk from the lamp at (2, 80) on the
  engine's own digital line and flight table first reaches x = 8 at the
  Node (8, 80 + j) (the Euclidean vector (6, j) reduced does not do: on
  the digital line (1, -1) and (6, -5) both land on (8, 75), and (8, 67)
  is reached by no vector of the form (6, j)), and the lamp's `turns`
  (the amplitude law's phase step per direction at birth) cancel the
  flight's whole phase of each leg, so the record's rows reach the
  opening Nodes in phase (a plane front across the opening from a point
  lamp; the legs and the turns are computed here from the two-slit map's
  `walk` on the engine's Bresenham line and `by_clock`);
- the opening's fan is uniform in angle by SELECTION and unweighted: one
  direction per 0.15 degree from -45 to +45 degrees (601 directions; the
  spacing of DERIVATIONS_BEAM 22.2's premise, record 155's 0.0026 in s),
  each the primitive direction (a, b, 0) with a + |b| <= 330 nearest the
  target angle (the world key `direction_bound` 330: a fan of width 48 has
  no direction between 0 and atan(1 / 47) = 1.22 degrees, a hole of 2.3
  pixels at L = 108 around every emitter's axis, which the pins script
  shows as a dip on the axis at w = 9), the plain equal split (a weighted
  split's norm enters the load-time ceiling as a product over every
  re-emitter, world.py `_record_load_checks`: 27 weighted openings
  would refuse at load; the plain split is not in the product and the
  run-time bound at the split, 27 x 601 per record, is far inside).

    PYTHONPATH=src python docs/designs/fail_rows/run_10_worlds.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "docs" / "designs" / "fraction_free"))

from two_slits_map import bresenham, manhattan_steps, phase_by_clock, resolution  # noqa: E402

N = 64
K = 1 << 30
FREQUENCY = [8591334592, 1 << 30]
WHEEL = [2531, 4096]
WIDTH_X, HEIGHT = 120, 161
LAMP = (2, 80)
WALL_X = 8
SCREEN_X = 116
CENTRE_Y = 80
FAN_WIDTH = 330  # the world key `direction_bound`: a + |b| <= 330
FAN_HALF_ANGLE = 45.0
FAN_GRAIN_DEGREES = 0.15  # 22.2's premise: record 155's spacing 0.0026 in s
WORLDS: dict[str, dict[str, object]] = {
    "opening_w27": {"w": 27, "rate": [1, 2], "ticks": 8500},
    "opening_w9": {"w": 9, "rate": [1, 1], "ticks": 4400},
}
Vector = tuple[int, int]


def fan_by_angle() -> list[Vector]:
    """One primitive direction per grain of angle within the half-angle,
    the nearest of the full fan a + |b| <= FAN_WIDTH; no weights."""
    full = sorted(
        {
            (a, b)
            for a in range(1, FAN_WIDTH + 1)
            for b in range(-FAN_WIDTH, FAN_WIDTH + 1)
            if a + abs(b) <= FAN_WIDTH and math.gcd(a, b) == 1
        },
        key=lambda v: math.atan2(v[1], v[0]),
    )
    angles = [math.degrees(math.atan2(b, a)) for a, b in full]
    steps = int(round(2 * FAN_HALF_ANGLE / FAN_GRAIN_DEGREES))
    chosen: list[Vector] = []
    for k in range(steps + 1):
        target = -FAN_HALF_ANGLE + k * FAN_GRAIN_DEGREES
        nearest = min(range(len(full)), key=lambda i: (abs(angles[i] - target), i))
        if full[nearest] not in chosen:
            chosen.append(full[nearest])
    return chosen


def leg_to_wall(vector: Vector) -> tuple[Vector, int]:
    """The lamp's row on `vector`: the first Node it reaches at the wall's
    x and the age of that arrival (the two-slit map's walk on the engine's
    Bresenham line and flight table)."""
    line = bresenham(vector)
    s1, t = len(line), resolution(vector)
    node = LAMP
    made = 0
    tau = 0
    while True:
        tau += 1
        if manhattan_steps(tau, s1, t) > made:
            step = line[made % s1]
            node = (node[0] + step[0], node[1] + step[1])
            made += 1
            if node[0] == WALL_X:
                return node, tau
        if tau > 10_000:
            raise RuntimeError("no arrival")


LEG_SEARCH = 12  # the largest a of a lamp direction searched


def lamp_legs(w: int) -> list[tuple[Vector, Vector, int, int]]:
    """Per opening Node (8, 80 + j), j = -w // 2 .. w // 2, the lamp's
    direction (the primitive (a, b) with the smallest a + |b|, then the
    earliest arrival, whose walk first reaches x = 8 at that Node), the
    Node reached, the age and the turn that cancels the leg's whole
    phase; one direction per Node, a bijection."""
    half = w // 2
    arrivals: dict[Vector, list[tuple[tuple[int, int], Vector, int]]] = {}
    for a in range(1, LEG_SEARCH + 1):
        for b in range(-3 * a - 1, 3 * a + 2):
            if math.gcd(a, b) != 1:
                continue
            node, age = leg_to_wall((a, b))
            arrivals.setdefault(node, []).append(((a + abs(b), age), (a, b), age))
    legs = []
    for j in range(-half, half + 1):
        node = (WALL_X, CENTRE_Y + j)
        _, vector, age = min(arrivals[node])
        turn = (-phase_by_clock(age, FREQUENCY[0], FREQUENCY[1])) % N
        legs.append((vector, node, age, turn))
    return legs


def world(name: str) -> dict[str, object]:
    keys = WORLDS[name]
    w = int(keys["w"])
    half = w // 2
    fan = fan_by_angle()
    legs = lamp_legs(w)
    reached = [node for _, node, _, _ in legs]
    opening = {(WALL_X, CENTRE_Y + j) for j in range(-half, half + 1)}
    assert set(reached) == opening and len(set(reached)) == w, (sorted(reached), sorted(opening))
    lamp_vectors = [vector for vector, _, _, _ in legs]
    table_vectors: list[Vector] = []
    for vector in [*lamp_vectors, *fan]:
        if vector != (1, 0) and vector not in table_vectors:
            table_vectors.append(vector)
    measured: list[dict[str, object]] = [
        {
            "position": [LAMP[0], LAMP[1], 0],
            "family": "light",
            "amount": K,
            "phase": 0,
            "fixed": True,
            "lamp": {
                "rate": list(keys["rate"]),
                "wheel": list(WHEEL),
                "directions": [[a, b, 0] for a, b in lamp_vectors],
                "turns": [turn for _, _, _, turn in legs],
            },
        }
    ]
    for y in range(HEIGHT):
        entry: dict[str, object] = {
            "position": [WALL_X, y, 0],
            "family": "wall",
            "amount": 1,
            "fixed": True,
        }
        if (WALL_X, y) in opening:
            entry["table"] = {"light": "rerelease"}
            entry["directions"] = [[a, b, 0] for a, b in fan]
        measured.append(entry)
    for y in range(HEIGHT):
        measured.append({"position": [SCREEN_X, y, 0], "family": "wall", "amount": 1, "fixed": True})
    detectors = [
        {"name": f"screen_{y}", "positions": [[SCREEN_X, y, 0]], "threshold": 1, "reading": "sum"}
        for y in range(HEIGHT)
    ]
    document: dict[str, object] = {
        "law": "beam",
        "model_id": f"beam-row10-{name.replace('_', '-')}-v1",
        "shape": [WIDTH_X, HEIGHT, 1],
        "boundary": {"z": "periodic"},
        "ticks": int(keys["ticks"]),
        "K": K,
        "N": N,
        "release": [1, 128],
        "suspension": 0,
        "direction_bound": FAN_WIDTH,
        "directions": [[a, b, 0] for a, b in table_vectors],
        "families": [
            {"name": "light", "quantum": 1, "phase_per_link": list(FREQUENCY)},
            {"name": "wall", "quantum": 1},
        ],
        "measured": measured,
        "detectors": detectors,
    }
    return document


def main() -> None:
    fan = fan_by_angle()
    print(
        f"the fan by angle: {len(fan)} directions, one per {FAN_GRAIN_DEGREES} degree within "
        f"+-{FAN_HALF_ANGLE:.0f} degrees of the full fan a + |b| <= {FAN_WIDTH} (unweighted)"
    )
    for name, keys in WORLDS.items():
        legs = lamp_legs(int(keys["w"]))
        print(f"{name}: w = {keys['w']}, the lamp's rate {keys['rate']}, {keys['ticks']} intervals")
        for vector, node, age, turn in legs:
            print(f"  the lamp's row on {vector} reaches {node} at the age {age}, the turn {turn}")
        document = world(name)
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"  written {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
