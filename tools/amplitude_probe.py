"""A probe of the Inside: the rays in flight, the clicks, the records and the
gathers of a run checked against the engine's own forms (the model owner's
request of 2026-09-23, "see that the amplitudes propagate correctly on the
board; the amplitudes as a wave, the events as a ray"; the Boss's order to
ship it as a diagnostic). Every number it prints is GAMEBOARD by
definition: it verifies the engine against its own forms and compares
nothing with nature.

Three checks on a run folder (the runner's `initialization.json`,
`state.json`, `events.jsonl`; a partial `events.jsonl` of a running world
is accepted, complete lines only):

1. THE RAYS IN FLIGHT (`state.json`): every ray's Node is the one the
   flight table gives from its birth Node by the digital line of its
   direction at its age (m(tau) = (2 tau S_1 Q + T_D) // (2 T_D), the
   two-slit map's walk, `docs/designs/fraction_free/two_slits_map.py`);
   its phase is the pair form's from its birth phase (u plus the lamp's
   turn for a lamp row, u for a re-emitted row, plus the sum of by_clock
   over its age); its amount 1 and its multiplicity the lamp's ways times
   the split's norm. Counts the rays off each form.
2. THE CLICKS, RECORDS AND GATHERS (`events.jsonl`, the first N completed
   records): every screen click line's `exact` equals BEAM_LAW note 45's
   phi = phase - floor(age n / d) + floor(n made T_D / (d S_1 Q)) mod N
   from the row's age and its direction (recovered from the remainder's
   denominator d S_1 Q and the remainder itself, since the label at the
   scale Q does not tell a fine fan's directions apart); every `record`
   line's pointer is the sum of its clicks' unit vectors 32 x (C, S)[exact]
   per Node and its square the line's; every `gather`'s rungs are the
   engine's `rungs` on the sets' squares (the faces' from their click
   lines, per face Node) and its chosen cell is `cell_of` on the record's
   u. Counts the lines off each form.
3. THE WAVE AND THE RAY (`state.json`): the rows re-emitted at one Node,
   grouped by age: the distinct phases on the ring (the wave: one per
   age, floor(age n / d) mod N), the ring's radius against c x age = age /
   sqrt 3 (the front), and the distinct directions (the ray: one per
   direction).

The forms are the record form of a massless family with the pair form of
phase per interval, one lamp and plain `rerelease` re-emitters (the equal
split); a weighted split is read through its `weights`. A massive
family's turn by momentum, a rotation, a gate and a body's drive are
outside this probe.

    PYTHONPATH=src python tools/amplitude_probe.py <run folder> [--records 60] [--emitter NUMBER] [--no-clicks]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path
from typing import Any

from event_universe.core.integer import by_clock
from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events.amplitude import cell_of, rungs

Q = 64  # the label's scale, the flight table's
SCALE = 32  # AMPLITUDE_SCALE, the click's unit
Vector = tuple[int, int]


def resolution(vector: Vector) -> int:
    """T_D = isqrt(3 |D|^2 Q^2), the flight table's resolution."""
    return math.isqrt(3 * (vector[0] ** 2 + vector[1] ** 2) * Q * Q)


def bresenham(vector: Vector) -> list[Vector]:
    """One period of the digital line (the engine's line in two dimensions:
    the axis furthest behind, the lowest axis first)."""
    s1 = abs(vector[0]) + abs(vector[1])
    line: list[Vector] = []
    position = [0, 0]
    for j in range(s1):
        best = max(range(2), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1]))
    return line


def manhattan_steps(tau: int, s1: int, t: int) -> int:
    """m(tau) = (2 tau S_1 Q + T_D) // (2 T_D)."""
    return (2 * tau * s1 * Q + t) // (2 * t)


def walk(start: Vector, vector: Vector, age: int) -> tuple[Vector, int]:
    """The Node after `age` intervals from `start` on `vector`, and the Links made."""
    line = bresenham(vector)
    s1, t = len(line), resolution(vector)
    node = start
    made = 0
    for tau in range(1, age + 1):
        if manhattan_steps(tau, s1, t) > made:
            step = line[made % s1]
            node = (node[0] + step[0], node[1] + step[1])
            made += 1
    return node, made


def phase_whole(age: int, n: int, d: int) -> int:
    """The phase column after `age` intervals of the pair form."""
    return sum(by_clock(a, n, d) for a in range(age))


class World:
    """The declared world's pieces the probe needs."""

    def __init__(self, folder: Path) -> None:
        self.document = json.loads((folder / "initialization.json").read_text())
        self.modulus = int(self.document["N"])
        light = next(f for f in self.document["families"] if "phase_per_link" in f)
        self.n, self.d = (int(v) for v in light["phase_per_link"])
        measured = self.document["measured"]
        self.positions = {i + 1: (m["position"][0], m["position"][1]) for i, m in enumerate(measured)}
        lamps = [(i + 1, m) for i, m in enumerate(measured) if "lamp" in m]
        self.lamp_number, lamp = lamps[0]
        self.lamp_directions = [(v[0], v[1]) for v in lamp["lamp"]["directions"]]
        turns = lamp["lamp"].get("turns") or [0] * len(self.lamp_directions)
        self.lamp_turn = {v: int(t) for v, t in zip(self.lamp_directions, turns, strict=True)}
        self.ways = len(self.lamp_directions)
        self.norm: dict[int, int] = {}
        self.fan: dict[int, list[Vector]] = {}
        for i, m in enumerate(measured):
            table = m.get("table")
            if not isinstance(table, dict):
                continue
            rule = table.get(light["name"])
            if rule == "rerelease" or (isinstance(rule, dict) and rule.get("rule") == "rerelease"):
                directions = [(v[0], v[1]) for v in m["directions"]]
                weights = (
                    rule["weights"]
                    if isinstance(rule, dict) and "weights" in rule
                    else [1] * len(directions)
                )
                self.fan[i + 1] = directions
                self.norm[i + 1] = sum(int(a) * int(a) for a in weights)
        self.by_s1: dict[int, list[Vector]] = collections.defaultdict(list)
        for directions in self.fan.values():
            for v in directions:
                if v not in self.by_s1[abs(v[0]) + abs(v[1])]:
                    self.by_s1[abs(v[0]) + abs(v[1])].append(v)


def probe_rays(folder: Path, world: World) -> None:
    state = json.loads((folder / "state.json").read_text())
    n, d, modulus = world.n, world.d, world.modulus
    rays = bad_node = bad_phase = bad_amount = 0
    kinds: collections.Counter[str] = collections.Counter()
    per_record: collections.Counter[int] = collections.Counter()
    for entry in state["nodes"]:
        at = (entry["position"][0], entry["position"][1])
        for family in entry["families"]:
            for ray in family["rays"]:
                rays += 1
                vector = (ray["direction"][0], ray["direction"][1])
                number = int(ray["number"])
                start = world.positions[number]
                if number == world.lamp_number:
                    birth = (int(ray["u"]) + world.lamp_turn[vector]) % modulus
                    expected = world.ways
                    kinds["lamp rows"] += 1
                else:
                    birth = int(ray["u"]) % modulus
                    expected = world.ways * world.norm.get(number, 1)
                    kinds["re-emitted rows"] += 1
                node, _ = walk(start, vector, int(ray["age"]))
                if node != at:
                    bad_node += 1
                if (birth + phase_whole(int(ray["age"]), n, d)) % modulus != int(ray["phase"]):
                    bad_phase += 1
                if int(ray["amount"]) != 1 or int(ray["multiplicity"]) != expected:
                    bad_amount += 1
                per_record[int(ray["record"])] += 1
    rows_per_record = collections.Counter(per_record.values())
    print(
        f"1. THE RAYS IN FLIGHT at the tick {state['tick']} (GAMEBOARD): {rays} rays ({dict(kinds)});"
        f" Node off the flight table's walk from the birth Node: {bad_node}; phase off the pair form from the birth phase:"
        f" {bad_phase}; amount or multiplicity off: {bad_amount}; rows per record: {dict(sorted(rows_per_record.items()))}"
    )


def probe_clicks(folder: Path, world: World, limit: int) -> None:
    n, d, modulus = world.n, world.d, world.modulus
    cos, sin = phase_cosines(modulus), phase_sines(modulus)

    def direction(label: list[int], remainder: list[int], age: int) -> Vector | None:
        s1 = remainder[1] // (d * Q)
        fits = []
        for v in world.by_s1.get(s1, []):
            t = resolution(v)
            made = manhattan_steps(age, s1, t)
            if (n * made * t) % (d * s1 * Q) == remainder[0]:
                fits.append(v)
        if not fits:
            return None
        angle = math.atan2(label[1], label[0])
        return min(fits, key=lambda v: abs(math.atan2(v[1], v[0]) - angle))

    clicks: dict[tuple[int, str], list[dict[str, Any]]] = collections.defaultdict(list)
    records: dict[tuple[int, str], dict[str, Any]] = {}
    gathers: dict[int, dict[str, Any]] = {}
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if not line.endswith("\n"):
                break
            if '"event": "click"' in line:
                event = json.loads(line)
                clicks[(int(event["record"]), str(event["detector"]))].append(event)
            elif '"event": "record"' in line:
                event = json.loads(line)
                records[(int(event["of"]), str(event["detector"]))] = event
            elif '"event": "gather"' in line:
                event = json.loads(line)
                gathers[int(event["record"])] = event
                if len(gathers) >= limit:
                    break
    checked = bad_exact = faces = no_direction = 0
    for rows in clicks.values():
        for event in rows:
            if "age" not in event:
                faces += 1
                continue
            vector = direction(list(event["push"]), list(event["remainder"]), int(event["age"]))
            if vector is None:
                no_direction += 1
                continue
            s1, t = abs(vector[0]) + abs(vector[1]), resolution(vector)
            made = manhattan_steps(int(event["age"]), s1, t)
            whole = (int(event["age"]) * n) // d
            expect = (int(event["phase"]) - whole + (n * made * t) // (d * s1 * Q)) % modulus
            checked += 1
            if expect != int(event["exact"]):
                bad_exact += 1

    def square(rows: list[dict[str, Any]]) -> tuple[int, int, int]:
        by_node: dict[tuple[int, ...], list[dict[str, Any]]] = collections.defaultdict(list)
        for event in rows:
            by_node[tuple(event["node"])].append(event)
        total = 0
        first = (0, 0)
        for index, group in enumerate(by_node.values()):
            x = sum(SCALE * int(e["amount"]) * cos[int(e["exact"]) % modulus] for e in group)
            y = sum(SCALE * int(e["amount"]) * sin[int(e["exact"]) % modulus] for e in group)
            total += x * x + y * y
            if index == 0:
                first = (x, y)
        return first[0], first[1], total

    checked_records = bad_pointer = bad_square = 0
    for key, record in records.items():
        if key not in clicks:
            continue
        x, y, total = square(clicks[key])
        checked_records += 1
        if [x, y] != record["pointer"]:
            bad_pointer += 1
        if total != record["record"]:
            bad_square += 1
    bad_rung = bad_cell = 0
    for identity, gather in gathers.items():
        cells = gather["cells"]
        names = [str(c[0][0][0]) for c in cells]
        printed = [int(c[1]) for c in cells]
        multiplicity = int(gather["weight"][1])
        weights = [
            (square(clicks[(identity, name)])[2] if (identity, name) in clicks else 0, multiplicity)
            for name in names
        ]
        found, _ = rungs(weights, _wheel(gather))
        if found != printed:
            bad_rung += 1
        k = cell_of(weights, _wheel(gather), int(gather["u"]))
        if k is None or names[k] != str(gather["chosen"][0][0]):
            bad_cell += 1
    print(
        f"2. THE CLICKS, RECORDS AND GATHERS of the first {len(gathers)} completed records (GAMEBOARD): {checked} screen click"
        f" lines, the exact phase off note 45's formula: {bad_exact} ({no_direction} whose remainder fits no direction);"
        f" {faces} face click lines (no age on the line, read through the gathers); {checked_records} record lines, the pointer"
        f" off the sum of its clicks' unit vectors: {bad_pointer}, the square off: {bad_square}; {len(gathers)} gathers, the"
        f" rungs off the engine's rungs on the sets' squares: {bad_rung}, the chosen cell off cell_of(u): {bad_cell}"
    )


def _wheel(gather: dict[str, Any]) -> int:
    """The record's wheel W: the last rung is W (b_K = W)."""
    return int(gather["cells"][-1][1])


def probe_front(folder: Path, world: World, emitter: int | None) -> None:
    state = json.loads((folder / "state.json").read_text())
    n, d, modulus = world.n, world.d, world.modulus
    if emitter is None:
        emitter = min(world.fan) if world.fan else world.lamp_number
    start = world.positions[emitter]
    by_age: dict[int, list[tuple[Vector, int, Vector]]] = collections.defaultdict(list)
    for entry in state["nodes"]:
        at = (entry["position"][0], entry["position"][1])
        for family in entry["families"]:
            for ray in family["rays"]:
                if int(ray["number"]) == emitter:
                    vector = (ray["direction"][0], ray["direction"][1])
                    turn = world.lamp_turn.get(vector, 0) if emitter == world.lamp_number else 0
                    by_age[int(ray["age"])].append(
                        (at, (int(ray["phase"]) - int(ray["u"]) - turn) % modulus, vector)
                    )
    c = 1 / math.sqrt(3)
    print(
        f"3. THE WAVE AND THE RAY: the rows emitted at {start} (measured {emitter}) at the tick {state['tick']}, by age"
        " (GAMEBOARD): age | rays | distinct phases less the birth phase (the wave: one) | that phase and floor(age n / d)"
        " mod N | the ring's radius min / mean / max in Links against c x age | distinct directions (the ray: one each)"
    )
    for age in sorted(by_age):
        group = by_age[age]
        phases = sorted({p for _, p, _ in group})
        radii = [math.hypot(at[0] - start[0], at[1] - start[1]) for at, _, _ in group]
        directions = {v for _, _, v in group}
        print(
            f"   {age:3d} | {len(group):5d} | {len(phases)} | {phases} and {((age * n) // d) % modulus} |"
            f" {min(radii):.2f} / {sum(radii) / len(radii):.2f} / {max(radii):.2f} against {c * age:.2f} | {len(directions)}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder", type=Path, help="a run folder of the shipped runner")
    parser.add_argument(
        "--records", type=int, default=60, help="the completed records to check (check 2)"
    )
    parser.add_argument(
        "--emitter", type=int, default=None, help="the measured event whose rows check 3 groups by age"
    )
    parser.add_argument("--no-clicks", action="store_true", help="skip check 2 (a large events.jsonl)")
    parser.add_argument(
        "--no-state", action="store_true", help="skip checks 1 and 3 (no state.json yet)"
    )
    args = parser.parse_args()
    world = World(args.folder)
    print(
        f"amplitude probe of {args.folder} (model {world.document.get('model_id')}): N = {world.modulus},"
        f" phase_per_link {world.n} / {world.d}, the lamp measured {world.lamp_number} on {world.ways} directions,"
        f" the re-emitters {sorted(world.fan)} with the norms {sorted(set(world.norm.values()))}"
    )
    if not args.no_state:
        probe_rays(args.folder, world)
    if not args.no_clicks:
        probe_clicks(args.folder, world, args.records)
    if not args.no_state:
        probe_front(args.folder, world, args.emitter)


if __name__ == "__main__":
    main()
