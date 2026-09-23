"""The readings of series I, "the nucleus": nucleons that are free bodies
holding one unit of a strong family with a lifetime, bound or not by the
one coupling over the columns and the contact through the table
(docs/EXPERIMENTS.md, "I, the nucleus"; examples/events/nucleus/make_worlds.py;
the model owner's decisions of 2026-09-20: "one mechanism for all the laws on
the GameBoard", "the strong force's range is a lifetime, L", the contact).

Reads the run folders of the worlds (the runner's `run.json`,
`initialization.json` and `events.jsonl`, told apart by the `model` of the
record, `beam-nucleus-<name>-space-v1`) and prints, per world, two kinds of
number, each line labelled (the model owner, 2026-09-20: "in reality there
is no such thing" about the host's readings of the GameBoard):

- DETECTOR readings, the only kind reality has, the bodies' own records:
  the push per interval each body reads at the reference tick (its `read`
  records, summed over the families and per family, in label units), the
  hand-overs at its refused steps (its `contact` records: the count, the
  first tick, the largest component, whether its label is 0 after each),
  the tick by which the pushes it read outweigh a declared kick, the sum of
  the pushes over a row of the square (the shear, the bodies' own reads)
  and the clicks on the border `lifetime` per interval;
- GAMEBOARD readings, the host's view of the mechanism, which exist for us
  and not in reality: the bodies' steps (the count, the first step and its
  direction, the final position, the escape through a face) and the
  separation of a pair over the run (its start, its largest value, whether
  it ever shrank after growing).

The expectation, written before the runs (README.md, docs/EXPERIMENTS.md):
the deuteron at one Link reads 310 967 280 640 per interval on each body
toward the other and never steps, its labels handed over and bounded; at
three Links no strong ray is read, gravity alone (1 067 524 788) and the
kicked pair separates; two protons at one Link attract by 148 716 220 864
and hold, at G = 7000 they repel by 4 691 779 136 and separate, at three
Links they repel by 15 977 466 864 and separate; the square p n / n p is
sheared by 49 090 283 970 per row per interval and a proton leaves within
the first hundred intervals; the line p n n p holds. The record checks
(completed, the books balanced at every tick) fail the tool; the readings
are registered inside or outside their expectation and never moved.

    PYTHONPATH=src python tools/click_readings/nucleus.py artifacts/nucleus

The rule of records 562 and 564 (the model owner, 2026-09-22; the audit of
record 567): only a detector's reading or a measured event's own record
(DETECTOR) is compared with an expectation; a number of the GameBoard (the
step records' positions, a replay, the books) is a diagnostic, printed
with its expectation as "agrees" or "differs", never counted inside or
outside, and names the detector reading behind it, not yet read.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.world_loading import world_of_run  # noqa: E402

MODEL_PREFIX = "beam-nucleus-"
MODEL_SUFFIX = "-space-v1"
# The tick at which the push per interval is read: every line of the fan
# within the reach has arrived by then and no body of the register's
# worlds has stepped.
REFERENCE_TICK = 20
LIFETIME_BORDER = "lifetime"
Vector = tuple[int, int, int]
Kind = str
GAMEBOARD: Kind = "GAMEBOARD"
DETECTOR: Kind = "DETECTOR"
# The order of the worlds in the register.
ORDER = (
    "deuteron_1",
    "deuteron_3",
    "deuteron_1_kick",
    "pp_1",
    "pp_1_weak",
    "pp_3",
    "alpha_square",
    "alpha_line",
)


@dataclass
class Body:
    number: int
    family: str
    start: Vector
    kick: Vector
    # The push per interval at the reference tick, in all and per family.
    push: Vector = (0, 0, 0)
    push_by_family: dict[str, Vector] = field(default_factory=dict)
    # The cumulative push over the ticks 1 .. t (DETECTOR: the read records).
    cumulative: list[Vector] = field(default_factory=list)
    steps: int = 0
    first_step: tuple[int, Vector] | None = None
    positions: dict[int, Vector] = field(default_factory=dict)
    final: Vector = (0, 0, 0)
    escaped: tuple[int, str] | None = None
    contacts: int = 0
    first_contact: int | None = None
    largest_handed: int = 0
    handed_to_zero: bool = True
    strong_reads: int = 0

    @property
    def kicked_back_at(self) -> int | None:
        """The first tick by which the pushes read outweigh the declared
        kick on its axis (None without a kick or never)."""
        axis = next((k for k in range(3) if self.kick[k]), None)
        if axis is None:
            return None
        against = -self.kick[axis]
        for tick, total in enumerate(self.cumulative, start=1):
            if (total[axis] > 0) == (against > 0) and abs(total[axis]) > abs(against):
                return tick
        return None


@dataclass
class Reading:
    name: str
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    strong: int
    lifetime: int
    width: int
    bodies: list[Body] = field(default_factory=list)
    lifetime_clicks: dict[int, int] = field(default_factory=dict)
    escaped_amount: dict[str, int] = field(default_factory=dict)

    def separation(self, a: int, b: int) -> list[tuple[int, float]]:
        """The Euclidean distance of the bodies `a` and `b` per tick from
        their step records, while both are on the GameBoard (GAMEBOARD)."""
        first, second = self.bodies[a - 1], self.bodies[b - 1]
        found = []
        here = [first.start, second.start]
        for tick in range(0, self.ticks + 1):
            if tick in first.positions:
                here[0] = first.positions[tick]
            if tick in second.positions:
                here[1] = second.positions[tick]
            if (first.escaped and tick >= first.escaped[0]) or (
                second.escaped and tick >= second.escaped[0]
            ):
                break
            found.append((tick, math.dist(here[0], here[1])))
        return found


def add(a: Vector, b: list[int] | Vector) -> Vector:
    return (a[0] + int(b[0]), a[1] + int(b[1]), a[2] + int(b[2]))


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    world = world_of_run(folder)
    families = {str(f["name"]): f for f in world["families"]}
    strong_family = next(
        (name for name, f in families.items() if "columns" in f and "strong" in f["columns"]), ""
    )
    strong = families[strong_family]["columns"]["strong"]["value"] if strong_family else 0
    reading = Reading(
        name=model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)],
        ticks=int(record["completed_ticks"]),
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
        strong=int(strong) if isinstance(strong, int) else int(strong[0]),
        lifetime=int(families[strong_family].get("lifetime", 0)) if strong_family else 0,
        width=int(world.get("width", 1)),
    )
    for index, declared in enumerate(world["measured"]):
        position = tuple(int(v) for v in declared["position"])
        kick = tuple(int(v) for v in declared.get("momentum", [0, 0, 0]))
        reading.bodies.append(
            Body(
                index + 1,
                str(declared["family"]),
                (position[0], position[1], position[2]),
                (kick[0], kick[1], kick[2]),
                final=(position[0], position[1], position[2]),
            )
        )
    for line in record["escaped"]:
        reading.escaped_amount[str(line["family"])] = int(line["amount"])
    by_number = {body.number: body for body in reading.bodies}
    running = {body.number: (0, 0, 0) for body in reading.bodies}
    last_tick = 0
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            if (
                '"read"' not in text
                and '"step"' not in text
                and '"contact"' not in text
                and '"click"' not in text
            ):
                continue
            event = json.loads(text)
            kind = event["event"]
            tick = int(event["tick"])
            if tick != last_tick:
                for number, body in by_number.items():
                    while len(body.cumulative) < tick - 1:
                        body.cumulative.append(running[number])
                last_tick = tick
            if kind == "read":
                body = by_number.get(int(event["measured"]))
                if body is None:
                    continue
                push = event["push"]
                running[body.number] = add(running[body.number], push)
                if str(event["family"]) == strong_family:
                    body.strong_reads += 1
                if tick == REFERENCE_TICK:
                    body.push = add(body.push, push)
                    family = str(event["family"])
                    body.push_by_family[family] = add(body.push_by_family.get(family, (0, 0, 0)), push)
            elif kind == "step":
                body = by_number[int(event["number"])]
                to = tuple(int(v) for v in event["to"])
                body.steps += 1
                if body.first_step is None:
                    body.first_step = (tick, (to[0], to[1], to[2]))
                body.positions[tick] = (to[0], to[1], to[2])
                body.final = (to[0], to[1], to[2])
            elif kind == "contact":
                body = by_number[int(event["number"])]
                body.contacts += 1
                if body.first_contact is None:
                    body.first_contact = tick
                component = abs(int(event["component"]))
                body.largest_handed = max(body.largest_handed, component)
                if int(event["momentum"][int(event["axis"])]) != 0:
                    body.handed_to_zero = False
            elif kind == "click":
                if event.get("detector") == LIFETIME_BORDER:
                    reading.lifetime_clicks[tick] = reading.lifetime_clicks.get(tick, 0) + 1
                elif event.get("measured") is not None:
                    body = by_number[int(event["measured"])]
                    body.escaped = (tick, str(event["detector"]))
    for number, body in by_number.items():
        while len(body.cumulative) < reading.ticks:
            body.cumulative.append(running[number])
    return reading


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    return sorted(found, key=lambda r: (ORDER.index(r.name) if r.name in ORDER else len(ORDER), r.name))


def vector(v: Vector) -> str:
    return "(" + ", ".join(f"{c:,}" for c in v) + ")"


def separation_summary(reading: Reading, a: int, b: int) -> tuple[float, float, float, bool]:
    """The start, the largest and the final separation of a pair and
    whether it ever shrank after growing (a return)."""
    trace = reading.separation(a, b)
    start = trace[0][1]
    largest = max(d for _, d in trace)
    final = trace[-1][1]
    returned = False
    peak = start
    for _, d in trace:
        if d > peak:
            peak = d
        elif d < peak - 0.5 and peak > start + 0.5:
            returned = True
    return start, largest, final, returned


def print_world(reading: Reading) -> list[tuple[str, bool]]:
    """Print the readings of one world and return its criteria (label,
    inside)."""
    criteria: list[tuple[str, bool]] = []
    print(
        f"[{GAMEBOARD}] world `{reading.name}`: {len(reading.bodies)} bodies, G = {reading.strong}, "
        f"lifetime {reading.lifetime}, width {reading.width}; {reading.ticks} intervals in {reading.elapsed:.1f} s"
    )
    for body in reading.bodies:
        parts = ", ".join(f"{name} {vector(v)}" for name, v in sorted(body.push_by_family.items()))
        print(
            f"[{DETECTOR}]   body {body.number} ({body.family} at {body.start}): the push per interval at tick "
            f"{REFERENCE_TICK} {vector(body.push)} [{parts}]; strong reads over the run {body.strong_reads}"
        )
        handed = (
            f"{body.contacts} hand-overs from tick {body.first_contact}, the largest {body.largest_handed:,}, "
            f"the label 0 after each: {'yes' if body.handed_to_zero else 'no'}"
            if body.contacts
            else "no hand-over"
        )
        print(f"[{DETECTOR}]   body {body.number}: {handed}")
        if any(body.kick):
            print(
                f"[{DETECTOR}]   body {body.number}: the kick {vector(body.kick)} outweighed by the pushes read; "
                f"[{GAMEBOARD}] by tick {body.kicked_back_at} (the record's ordering)"
            )
        steps = (
            f"{body.steps} steps, the first at tick {body.first_step[0]} to {body.first_step[1]}, "
            f"the final position {body.final}"
            if body.first_step
            else "no step"
        )
        escaped = f", out through {body.escaped[1]} at tick {body.escaped[0]}" if body.escaped else ""
        print(f"[{GAMEBOARD}]   body {body.number}: {steps}{escaped}")
    clicks = reading.lifetime_clicks
    if clicks:
        at = min(clicks)
        steady = clicks.get(REFERENCE_TICK, 0)
        print(
            f"[{DETECTOR}]   the border `lifetime`: {steady} per interval at tick {REFERENCE_TICK} "
            f"({steady // max(1, len(reading.bodies))} per body; a fixed detector at k = 0, its tick its own "
            f"clock); [{GAMEBOARD}] the first clicks at tick {at} (the onset, the record's ordering)"
        )
    if len(reading.bodies) == 2:
        start, largest, final, returned = separation_summary(reading, 1, 2)
        print(
            f"[{GAMEBOARD}]   the pair's separation: {start:.2f} at the start, the largest {largest:.2f}, "
            f"{final:.2f} at the end{' (both on the GameBoard)' if not any(b.escaped for b in reading.bodies) else ''}, "
            f"{'shrank after growing' if returned else 'never shrank after growing'}"
        )
    if len(reading.bodies) == 4 and reading.name == "alpha_square":
        rows = ((1, 2), (3, 4))
        for row in rows:
            shear = sum(reading.bodies[k - 1].push[0] for k in row)
            print(
                f"[{GAMEBOARD}]   the row {{{row[0]}, {row[1]}}}: the sum of its x pushes {shear:,} per interval (the shear)"
            )
        largest = max(
            math.dist(a.final, b.final)
            for a in reading.bodies
            for b in reading.bodies
            if a.number < b.number
        )
        print(f"[{GAMEBOARD}]   the largest separation of two bodies at the end {largest:.2f}")
    criteria += expectations(reading)
    for label, ok in criteria:
        if deciding(label):
            print(f"[{DETECTOR}]   {label}: {'inside' if ok else 'outside'}")
        else:
            print(
                f"[{GAMEBOARD}] (a diagnostic, not counted: the step records or an onset tick)   {label}: "
                f"{'agrees' if ok else 'differs'}; the detector reading behind it, the faces' and the "
                "border's clicks of the bodies, not yet read"
            )
    print()
    return [c for c in criteria if deciding(c[0])]


# The onset of a reading in host ticks (the border's first click, the tick
# by which the pushes outweigh the kick): the record's ordering, a GameBoard
# number (the clock audit of 2026-09-22, record 678), a diagnostic beside
# the rate or the push it belongs to.
ONSET = "the onset tick (the record's ordering)"


def deciding(label: str) -> bool:
    """A criterion counts inside or outside when it reads a body's own
    records (its pushes and their row sums, the shear; its reads, hand-overs,
    kicks and clicks; the border's clicks); a step, a position or a
    separation is a diagnostic (record 567, F12), and so is an onset in host
    ticks (the clock audit of 2026-09-22)."""
    if ONSET in label:
        return False
    return any(word in label for word in ("push", "shear", "read", "hand", "kick", "click", "leave"))


DEUTERON_PUSH = 310_967_280_640
DEUTERON_GRAVITY = 1_067_524_788
PP_PUSH = 148_716_220_864
PP_WEAK_PUSH = -4_691_779_136
PP_3_PUSH = -15_977_466_864
SQUARE_PUSH = {
    1: (355_957_892_670, 320_048_730_393, 0),
    2: (-405_048_176_640, 376_205_857_440, 0),
    3: (405_048_176_640, -376_205_857_440, 0),
    4: (-355_957_892_670, -320_048_730_393, 0),
}
SHEAR = 49_090_283_970
LINE_P1_PUSH = 403_332_137_616


def expectations(reading: Reading) -> list[tuple[str, bool]]:
    """The criteria of each world against its expectation, written before
    the runs (README.md)."""
    bodies = reading.bodies
    found: list[tuple[str, bool]] = []
    name = reading.name
    if name == "deuteron_1":
        found.append(
            (
                f"the push on the proton {DEUTERON_PUSH:,} toward the neutron",
                bodies[0].push == (DEUTERON_PUSH, 0, 0),
            )
        )
        found.append(("the neutron's push the mirror", bodies[1].push == (-DEUTERON_PUSH, 0, 0)))
        found.append(("no step in the run", all(b.steps == 0 for b in bodies)))
        found.append(
            (
                "the label 0 after every hand-over",
                all(b.handed_to_zero for b in bodies) and any(b.contacts for b in bodies),
            )
        )
        found.append(
            (
                "the largest hand-over within 10^12 .. 10^13",
                all(10**12 <= b.largest_handed <= 10**13 for b in bodies if b.contacts),
            )
        )
        # The rate is read at the border, a fixed detector at k = 0 whose
        # tick is its own clock (record 569): counted. The onset "from tick
        # 4" is the record's ordering: a diagnostic (the clock audit of
        # 2026-09-22).
        found.append(
            (
                f"290 lifetime clicks per body per interval at tick {REFERENCE_TICK} (the border, a fixed "
                "detector at k = 0: its tick its own clock)",
                reading.lifetime_clicks.get(REFERENCE_TICK) == 290 * len(bodies),
            )
        )
        found.append(
            (
                f"the border's first clicks at tick 4, {ONSET}",
                min(reading.lifetime_clicks, default=0) == 4,
            )
        )
    elif name == "deuteron_3":
        found.append(("no strong read at either body", all(b.strong_reads == 0 for b in bodies)))
        found.append(
            (
                f"the gravity push {DEUTERON_GRAVITY:,} on the proton at tick {REFERENCE_TICK}",
                bodies[0].push == (DEUTERON_GRAVITY, 0, 0),
            )
        )
        start, largest, final, returned = separation_summary(reading, 1, 2)
        found.append(
            ("the pair separates beyond 10 Links and never returns", largest > 10 and not returned)
        )
        found.append(("both bodies leave through the faces", all(b.escaped is not None for b in bodies)))
    elif name == "deuteron_1_kick":
        # The pushes read are the bodies' own records: counted. "By tick 5"
        # is the record's ordering: a diagnostic (the clock audit of 2026-09-22).
        found.append(
            (
                "the kick outweighed by the pushes read",
                all(b.kicked_back_at is not None for b in bodies),
            )
        )
        found.append(
            (
                f"the kick outweighed by tick 5, {ONSET}",
                all(b.kicked_back_at is not None and b.kicked_back_at <= 5 for b in bodies),
            )
        )
        found.append(("no step in the run", all(b.steps == 0 for b in bodies)))
        found.append(
            (
                "the first refused step of each body is toward the other",
                all(b.contacts > 0 for b in bodies),
            )
        )
    elif name == "pp_1":
        found.append(
            (
                f"the push on each proton {PP_PUSH:,} toward the other",
                bodies[0].push == (PP_PUSH, 0, 0) and bodies[1].push == (-PP_PUSH, 0, 0),
            )
        )
        found.append(("no step in the run", all(b.steps == 0 for b in bodies)))
        found.append(
            (
                "the label 0 after every hand-over",
                all(b.handed_to_zero for b in bodies) and any(b.contacts for b in bodies),
            )
        )
    elif name == "pp_1_weak":
        found.append(
            (
                f"the push on each proton {PP_WEAK_PUSH:,} (repulsion)",
                bodies[0].push == (PP_WEAK_PUSH, 0, 0) and bodies[1].push == (-PP_WEAK_PUSH, 0, 0),
            )
        )
        start, largest, final, returned = separation_summary(reading, 1, 2)
        found.append(("the pair separates and never returns", largest > start + 1 and not returned))
        found.append(
            (
                "the first step within 200 intervals",
                all(b.first_step is not None and b.first_step[0] <= 200 for b in bodies),
            )
        )
    elif name == "pp_3":
        found.append(
            (
                f"the push on each proton {PP_3_PUSH:,} (repulsion)",
                bodies[0].push == (PP_3_PUSH, 0, 0) and bodies[1].push == (-PP_3_PUSH, 0, 0),
            )
        )
        found.append(("no strong read at either body", all(b.strong_reads == 0 for b in bodies)))
        found.append(
            (
                "the first step at tick 30 .. 60",
                all(b.first_step is not None and 30 <= b.first_step[0] <= 60 for b in bodies),
            )
        )
        start, largest, final, returned = separation_summary(reading, 1, 2)
        found.append(("the pair separates and never returns", largest > start + 1 and not returned))
    elif name == "alpha_square":
        found.append(
            ("the push per body the design's", all(b.push == SQUARE_PUSH[b.number] for b in bodies))
        )
        shear = [sum(bodies[k - 1].push[0] for k in row) for row in ((1, 2), (3, 4))]
        found.append((f"the shear {SHEAR:,} per row per interval", shear == [-SHEAR, SHEAR]))
        protons = [b for b in bodies if b.family == "p"]
        found.append(
            (
                "a proton's step within the first hundred intervals",
                any(b.first_step is not None and b.first_step[0] <= 100 for b in protons),
            )
        )
        largest = max(math.dist(a.final, b.final) for a in bodies for b in bodies if a.number < b.number)
        found.append(("the cluster disperses (the largest separation beyond 3 Links)", largest > 3))
    elif name == "alpha_line":
        found.append(
            (
                f"the push on the first proton {LINE_P1_PUSH:,} on x",
                bodies[0].push == (LINE_P1_PUSH, 0, 0),
            )
        )
        found.append(("no step in the run", all(b.steps == 0 for b in bodies)))
        found.append(
            (
                "the label 0 after every hand-over",
                all(b.handed_to_zero for b in bodies) and any(b.contacts for b in bodies),
            )
        )
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    args = parser.parse_args(argv)
    readings = find_runs(args.root)
    if not readings:
        print(f"no nucleus run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.name}: {label} ({r.elapsed:.1f} s, {r.ticks} ticks)")
            failed += not ok
    print()
    print(
        f"every line below is labelled [{GAMEBOARD}] (the host's view of the GameBoard: the steps, the "
        f"separations; exists for us, not in reality; a criterion of this kind is a diagnostic, printed "
        f"and not counted) or [{DETECTOR}] (a measured event's own records: the only kind reality has)"
    )
    print()
    criteria: list[tuple[str, bool]] = []
    for r in readings:
        criteria += print_world(r)
    inside = sum(1 for _, ok in criteria if ok)
    print(
        f"{failed} record check(s) failed; {inside} reading(s) inside, {len(criteria) - inside} outside "
        "(the GameBoard diagnostics printed above are not counted)"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
