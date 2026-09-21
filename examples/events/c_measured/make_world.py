"""Write the one world of series Q, "c measured behind a detector", and its
register (the model owner's "go for it" of 2026-09-21, record 236: verify
c by a run behind a detector against the formula).

The world (README.md here; the entry "Q, c measured behind a detector
(2026-09-21)" in docs/EXPERIMENTS.md): an open cube of SIDE^3 Nodes, every
face a detector (an open face is a detector, an escape is a click), and at
its centre one lamp of the paid family `light` (quantum 1) whose content is
exactly one birth's cost, so that its first self-creation births one
record of one row of amount 1 on each of the FAN directions (every
primitive direction (a, b, c) with 0 < |a| + |b| + |c| <= FAN_MANHATTAN,
the fan series E, I and K declare) and its clock then reads a turn of 0
forever (E = h f: the birth spent the content). No other body, no field,
no collision (the six heading rows of one number never share a Node), no
merge (one row per direction). Every row flies its digital line at the
flight table's pace and leaves through a face: one click per direction,
each with its tick and the Node it left from.

The expectation, written before the run from the closed form of the flight
(docs/DERIVATIONS_BEAM.md section 11.1): the position of a row born at the
Node x_0 on the direction D (a vector of the world's table, S_1 its
Manhattan length, T_D = isqrt(3 |D|^2 Q^2) its resolution, Q = 64 the
label's scale) at the age tau is x_0 + line_D[m_D(tau)] with

    m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D)),

line_D the Bresenham line of D (at each step the axis whose progress is
furthest behind, the lowest axis first), so its k-th Link falls at the age
tau_k = ceil((2 k - 1) T_D / (2 S_1 Q)). The escape of the row is its
first Link k whose Node is off the GameBoard; its click carries the tick
birth + tau_k and the Node after k - 1 Links (the last Node on the
GameBoard), and the face of the k-th step. The Euclidean pace of the
escape is |x_k - x_0|_2 / tau_k Links per interval (x_k the position after
the k Links, one Link past the click's Node through the face), against
c = 1 / sqrt 3 and its finite-grain range over the fan Q |D| / T_D
(docs/designs/light_speed/FORM.md section 1: 0.5774 to 0.5818 over the
directions within 64 at Q = 64).

`expectations.json` beside the world is the register a test reads
(docs/TEST_EXPECTATIONS.md: one source per number), `derived.csv` the
per-direction table. Run from the repository root:

    PYTHONPATH=src python examples/events/c_measured/make_world.py
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.events.nature_beam import Q  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's family comes from (the model owner's
# decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

HALF_WIDTH = 32
SIDE = 2 * HALF_WIDTH + 1
CENTRE = (HALF_WIDTH, HALF_WIDTH, HALF_WIDTH)
FAN_MANHATTAN = 6
N = 64
# The lamp's first self-creation is at tick 1: every row is born at tick 1
# with the age 0 and the click of a row at the age tau is at tick 1 + tau.
BIRTH_TICK = 1
# The run's length: two intervals past the last derived escape, so that the
# record's gather (the one click of the record form) falls inside the run.
MARGIN = 2
FORMAT = "c-measured-expectations-v1"
DERIVATION = (
    "docs/DERIVATIONS_BEAM.md section 11.1 (the flight's closed form) and "
    "docs/designs/light_speed/FORM.md section 1 (c = 1 / sqrt 3 and its finite grain)"
)
Vector = tuple[int, int, int]
Json = dict[str, Any]
FACE_OF_AXIS = "xyz"


def fan(manhattan: int) -> list[Vector]:
    """Every primitive direction (a, b, c) with 0 < |a| + |b| + |c| <=
    manhattan, in a fixed order (the fan of series E)."""
    found: list[Vector] = []
    for a in range(-manhattan, manhattan + 1):
        for b in range(-manhattan, manhattan + 1):
            for c in range(-manhattan, manhattan + 1):
                if (a or b or c) and abs(a) + abs(b) + abs(c) <= manhattan:
                    if math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                        found.append((a, b, c))
    found.sort()
    return found


def bresenham(vector: Vector) -> list[Vector]:
    """The S_1 unit steps of one period of the digital line of the vector:
    at each step the axis whose progress is furthest behind, the lowest
    axis first (line_D of the derivation, the engine's `flight.lines`)."""
    s1 = sum(abs(c) for c in vector)
    line: list[Vector] = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


def resolution(vector: Vector) -> int:
    """T_D = isqrt(3 |D|^2 Q^2), the resolution of the direction."""
    return math.isqrt(3 * sum(c * c for c in vector) * Q * Q)


def manhattan_count(tau: int, s1: int, t: int) -> int:
    """m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D)): the Links made by
    the age tau (the derivation's closed form)."""
    return (2 * tau * s1 * Q + t) // (2 * t)


def link_age(k: int, s1: int, t: int) -> int:
    """tau_k = ceil((2 k - 1) T_D / (2 S_1 Q)): the age of the k-th Link."""
    return -(-(2 * k - 1) * t // (2 * s1 * Q))


def direction_class(vector: Vector) -> str:
    """The class of a direction of the fan: an axis (a heading), a face
    diagonal (two components of 1), a body diagonal (three), or the rest."""
    magnitudes = sorted(abs(c) for c in vector)
    if magnitudes == [0, 0, 1]:
        return "axes"
    if magnitudes == [0, 1, 1]:
        return "face_diagonals"
    if magnitudes == [1, 1, 1]:
        return "body_diagonals"
    return "rest"


def derive(vector: Vector) -> Json:
    """The escape of the row born at the centre on the direction, from the
    closed form: its Link count k, its age tau_k, the click's tick, Node
    and face, its displacement and its Euclidean pace."""
    s1 = sum(abs(c) for c in vector)
    t = resolution(vector)
    line = bresenham(vector)
    position = list(CENTRE)
    k = 0
    while True:
        step = line[k % s1]
        k += 1
        position = [p + s for p, s in zip(position, step, strict=True)]
        if any(p < 0 or p >= SIDE for p in position):
            break
    node = [p - s for p, s in zip(position, step, strict=True)]
    axis = next(a for a in range(3) if step[a])
    face = f"face:{'+' if step[axis] > 0 else '-'}{FACE_OF_AXIS[axis]}"
    tau = link_age(k, s1, t)
    assert manhattan_count(tau, s1, t) >= k > manhattan_count(tau - 1, s1, t)
    displacement = [p - c for p, c in zip(position, CENTRE, strict=True)]
    distance_squared = sum(d * d for d in displacement)
    return {
        "direction": list(vector),
        "class": direction_class(vector),
        "manhattan": s1,
        "resolution": t,
        "links": k,
        "age": tau,
        "tick": BIRTH_TICK + tau,
        "node": node,
        "face": face,
        "displacement": displacement,
        "distance_squared": distance_squared,
        "pace": round(math.sqrt(distance_squared) / tau, 6),
        "asymptotic_pace": round(Q * math.sqrt(sum(c * c for c in vector)) / t, 6),
    }


def summary(rows: list[Json], key: str) -> Json:
    values = [float(row[key]) for row in rows]
    return {
        "min": round(min(values), 6),
        "max": round(max(values), 6),
        "mean": round(sum(values) / len(values), 6),
    }


def expectations() -> Json:
    """The register: every direction's escape from the closed form and the
    totals over the fan and per class, written before the run."""
    directions = fan(FAN_MANHATTAN)
    rows = [derive(vector) for vector in directions]
    classes: Json = {}
    for name in ("axes", "face_diagonals", "body_diagonals", "rest"):
        members = [row for row in rows if row["class"] == name]
        classes[name] = {
            "count": len(members),
            "ages": sorted({int(row["age"]) for row in members}),
            "pace": summary(members, "pace"),
        }
    last = max(int(row["tick"]) for row in rows)
    return {
        "format": FORMAT,
        "derivation": DERIVATION,
        "world": "c_measured.json",
        "Q": Q,
        "half_width": HALF_WIDTH,
        "side": SIDE,
        "centre": list(CENTRE),
        "fan_manhattan": FAN_MANHATTAN,
        "fan": len(directions),
        "birth_tick": BIRTH_TICK,
        "births": 1,
        "clicks": len(directions),
        "last_tick": last,
        "ticks": last + MARGIN,
        "c": round(1 / math.sqrt(3), 6),
        "pace": summary(rows, "pace"),
        "asymptotic_pace": summary(rows, "asymptotic_pace"),
        "classes": classes,
        "directions": rows,
    }


def world(register: Json) -> Json:
    directions = fan(FAN_MANHATTAN)
    headings = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)}
    declared = [list(v) for v in directions if v not in headings]
    return {
        "law": "beam",
        "model_id": "beam-c-measured-v1",
        "shape": [SIDE, SIDE, SIDE],
        "boundary": "open",
        "ticks": register["ticks"],
        # The clock's rate: one turn per self-creation while the lamp holds
        # its declared content, one birth's cost; 0 turns after the birth.
        "K": len(directions),
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}],
        "directions": declared,
        "measured": [
            {
                "position": list(CENTRE),
                "family": "light",
                "amount": len(directions),
                "fixed": True,
                "lamp": {"rate": [1, 1], "wheel": [1, N], "directions": [list(v) for v in directions]},
            }
        ],
    }


def main() -> None:
    register = expectations()
    (HERE / "expectations.json").write_text(json.dumps(register, indent=1) + "\n", encoding="utf-8")
    document = families_by_definition(world(register), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
    (HERE / "c_measured.json").write_text(
        json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    rows: list[Json] = register["directions"]
    with (HERE / "derived.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            [
                "a",
                "b",
                "c",
                "class",
                "manhattan",
                "resolution",
                "links",
                "age",
                "tick",
                "node_x",
                "node_y",
                "node_z",
                "face",
                "distance_squared",
                "pace",
                "asymptotic_pace",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    *row["direction"],
                    row["class"],
                    row["manhattan"],
                    row["resolution"],
                    row["links"],
                    row["age"],
                    row["tick"],
                    *row["node"],
                    row["face"],
                    row["distance_squared"],
                    row["pace"],
                    row["asymptotic_pace"],
                ]
            )
    print(
        f"fan {register['fan']} directions, half-width {HALF_WIDTH} (side {SIDE}), Q {Q}, "
        f"{register['ticks']} intervals; the last escape at tick {register['last_tick']}"
    )
    print(f"the derived pace over the fan: {register['pace']} (c = {register['c']})")
    print(f"the asymptotic pace Q |D| / T_D over the fan: {register['asymptotic_pace']}")
    classes: Json = register["classes"]
    for name, entry in classes.items():
        print(f"  {name}: {entry}")
    for name in ("expectations.json", "c_measured.json", "derived.csv"):
        print((HERE / name).relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
