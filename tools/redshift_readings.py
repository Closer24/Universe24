"""The readings of the redshift series E under the law of the ray, in
space, under the age reading.

Reads the run folders of the worlds of `examples/events/redshift/` (the
runner's `run.json` and `initialization.json`, the folders told apart by
the `model` of their record, `rays-redshift-<kind>-space-v1`, the kind
`scalar` or `age`) and prints, per shell radius r: the number of probes on
the shell, the mean owed count per self-creation over the whole run
(`waited / age` per probe, from the final states of `run.json`) and over
the window [T1, T2] of the stationary fan (the world replayed through the
API from the world file, the probes' (age, waited) taken at T1 and T2, the
difference's ratio: the same engine, the same integers), the fraction of
the shell's probes that counted anything, and the products k x r^2 (the
scalar world: expected constant, the fan diluting as the shell's Nodes)
and k x r (the age world: expected constant, the age of a ray at r being
about r x sqrt 3); then the single probes on the +x axis and the (1, 1, 0)
and (1, 1, 1) diagonals at the same radii (the granularity of the fan: a
probe on a line of the fan reads that line's beam, whose presence does not
fall with r); and the redshift ratios of the age clocks, the rate of a
clock being age / (age + waited) = 1 / (1 + k), rate(r) / rate(r_ref)
measured against (1 + k_a(r_ref)) / (1 + k_a(r)) with k_a(r) = C / r fitted
at r_ref, and against the first-order line 1 - C (1 / r - 1 / r_ref). The
record checks (completed, the books balanced at every tick) fail the tool;
the readings are registered inside or outside their expectation
(docs/EXPERIMENTS.md, "E, the clock's redshift in space under the age
reading (2026-09-20)") and never moved.

    PYTHONPATH=src python tools/redshift_readings.py artifacts/redshift
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

MODEL_PREFIX = "rays-redshift-"
MODEL_SUFFIX = "-space-v1"
WINDOW = (100, 300)
DIAGONALS = {
    "+x": (1, 0, 0),
    "(1,1,0)": (1, 1, 0),
    "(1,1,1)": (1, 1, 1),
}
# The expectation of the shell means: the product constant within this
# fraction of its mean over r >= 6 (the fan's granularity at r = 4, where
# many lines cross one Node, is reported and not held to it).
RIPPLE = 0.15


@dataclass
class Probe:
    position: tuple[int, int, int]
    radius: int
    age: int
    waited: int
    window_age: int = 0
    window_waited: int = 0

    def mean(self, window: bool) -> float:
        age = self.window_age if window else self.age
        waited = self.window_waited if window else self.waited
        return 0.0 if age == 0 else waited / age


@dataclass
class Shell:
    radius: int
    probes: list[Probe] = field(default_factory=list)

    def mean(self, window: bool) -> float:
        return sum(p.mean(window) for p in self.probes) / len(self.probes)

    def fraction_counting(self, window: bool) -> float:
        counting = sum(1 for p in self.probes if (p.window_waited if window else p.waited) > 0)
        return counting / len(self.probes)


@dataclass
class Reading:
    kind: str
    suspension: tuple[int, int]
    centre: tuple[int, int, int]
    directions: int
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    shells: dict[int, Shell] = field(default_factory=dict)
    by_position: dict[tuple[int, int, int], Probe] = field(default_factory=dict)

    @property
    def power(self) -> int:
        """The power of r whose product with k is expected constant: 2 for
        the presence (the shell's Nodes), 1 for the age reading."""
        return 1 if self.kind == "age" else 2

    def single(self, label: str, radius: int) -> Probe | None:
        """The probe of the shell nearest to the direction's line: the
        shell's Node of the largest cosine to the direction (the axis Node
        on the axis; on a diagonal the nearest GameBoard Node of the shell,
        which the diagonal's own line may miss)."""
        direction = DIAGONALS[label]
        shell = self.shells.get(radius)
        if shell is None:
            return None
        norm = math.sqrt(sum(c * c for c in direction))

        def cosine(probe: Probe) -> float:
            offset = [probe.position[i] - self.centre[i] for i in range(3)]
            length = math.sqrt(sum(c * c for c in offset)) or 1.0
            return sum(o * d for o, d in zip(offset, direction, strict=True)) / (length * norm)

        return max(shell.probes, key=cosine)


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    kind = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)]
    document = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    source = document["measured"][0]
    centre = (int(source["position"][0]), int(source["position"][1]), int(source["position"][2]))
    reading = Reading(
        kind=kind,
        suspension=(int(record["suspension"][0]), int(record["suspension"][1])),
        centre=centre,
        directions=len(source["directions"]),
        ticks=int(record["completed_ticks"]),
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
    )
    for entry in record["measured"][1:]:
        position = (int(entry["position"][0]), int(entry["position"][1]), int(entry["position"][2]))
        distance = math.sqrt(sum((position[i] - centre[i]) ** 2 for i in range(3)))
        radius = round(distance)
        probe = Probe(position, radius, int(entry["age"]), int(entry["waited"]))
        reading.shells.setdefault(radius, Shell(radius)).probes.append(probe)
        reading.by_position[position] = probe
    replay_window(document, reading)
    return reading


def replay_window(document: dict[str, object], reading: Reading) -> None:
    """The world replayed through the API: every probe's (age, waited) at
    the two ends of the window, the difference being its count over the
    stationary fan."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(document))
    start, end = WINDOW
    end = min(end, reading.ticks)
    at_start: dict[int, tuple[int, int]] = {}
    for tick in range(1, end + 1):
        simulation.step()
        if tick == start:
            at_start = {n: (m.age, m.waited) for n, m in simulation.measured.items()}
    for number, entry in simulation.measured.items():
        if number == 1:
            continue
        probe = reading.by_position[entry.position]
        age0, waited0 = at_start[number]
        probe.window_age = entry.age - age0
        probe.window_waited = entry.waited - waited0


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    return sorted(found, key=lambda r: r.kind, reverse=True)


def print_shells(readings: list[Reading]) -> list[tuple[str, bool]]:
    """The shell means per radius and the constancy of k x r^power over
    the window; returns the criteria."""
    criteria: list[tuple[str, bool]] = []
    for r in readings:
        n, d = r.suspension
        print(
            f"world `{r.kind}` (suspension [{n}, {d}], {r.directions} directions, {r.ticks} "
            f"intervals, {r.elapsed:.1f} s): the shell means of the owed count per self-creation"
        )
        print(
            f"| r | probes | counting (window) | k, whole run | k, window {WINDOW[0]}..{WINDOW[1]} | "
            f"k x r^{r.power} (window) | expected |"
        )
        print("| --- | --- | --- | --- | --- | --- | --- |")
        products = {}
        for radius in sorted(r.shells):
            shell = r.shells[radius]
            k = shell.mean(True)
            products[radius] = k * radius**r.power
        reference = [products[radius] for radius in sorted(products) if radius >= 6]
        centre = sum(reference) / len(reference)
        for radius in sorted(r.shells):
            shell = r.shells[radius]
            product = products[radius]
            inside = abs(product - centre) <= RIPPLE * centre if radius >= 6 else None
            verdict = "-" if inside is None else ("inside" if inside else "outside")
            print(
                f"| {radius} | {len(shell.probes)} | {shell.fraction_counting(True):.2f} | "
                f"{shell.mean(False):.3f} | {shell.mean(True):.3f} | {product:.2f} | "
                f"{centre:.2f} +- {RIPPLE * 100:.0f} %: {verdict} |"
            )
            if inside is not None:
                criteria.append((f"{r.kind}: k x r^{r.power} at r = {radius} within the ripple", inside))
        print()
    return criteria


def print_singles(readings: list[Reading]) -> None:
    print("the single probes (the window; the granularity of the fan: a probe on a line reads its beam)")
    print("| r | direction | Node | k scalar | k age | k scalar x r^2 | k age x r |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    by_kind = {r.kind: r for r in readings}
    scalar, age = by_kind.get("scalar"), by_kind.get("age")
    if scalar is None or age is None:
        print("(both worlds are needed)")
        return
    for radius in sorted(scalar.shells):
        for label in DIAGONALS:
            s, a = scalar.single(label, radius), age.single(label, radius)
            if s is None or a is None:
                print(f"| {radius} | {label} | - | - | - | - | - |")
                continue
            ks, ka = s.mean(True), a.mean(True)
            print(
                f"| {radius} | {label} | {list(s.position)} | {ks:.3f} | {ka:.3f} | "
                f"{ks * radius**2:.2f} | {ka * radius:.2f} |"
            )
    print()


def print_redshift(readings: list[Reading]) -> list[tuple[str, bool]]:
    """The ratio of the age clocks' rates against the 1 / r law fitted at
    the reference radius and its first-order line."""
    criteria: list[tuple[str, bool]] = []
    age = next((r for r in readings if r.kind == "age"), None)
    if age is None:
        return criteria
    radii = sorted(age.shells)
    reference = radii[-1]
    k_ref = age.shells[reference].mean(True)
    constant = k_ref * reference
    # The same law with C the mean of k x r over the shells from r = 6 (the
    # constant of the shell table), for the reader: the criterion is the
    # fit at the reference radius, pinned before the run.
    shell_constant = sum(age.shells[r].mean(True) * r for r in radii if r >= 6) / sum(
        1 for r in radii if r >= 6
    )
    print(
        f"the redshift of the age clocks (the window): rate = 1 / (1 + k), rate(r) / rate({reference}) "
        f"against (1 + k_ref) / (1 + C / r) with C = k_ref x {reference} = {constant:.2f} (and, for "
        f"the reader, with C the shell mean {shell_constant:.2f}), and the first-order line "
        f"1 - C (1 / r - 1 / {reference}), which holds for k << 1 only"
    )
    print(
        "| r | k age | rate | rate(r) / rate(ref) measured | 1 / r law | 1 / r law, shell C | "
        "first order | expected |"
    )
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for radius in radii:
        k = age.shells[radius].mean(True)
        measured = (1 + k_ref) / (1 + k)
        law = (1 + k_ref) / (1 + constant / radius)
        shell_law = (1 + shell_constant / reference) / (1 + shell_constant / radius)
        first = 1 - constant * (1 / radius - 1 / reference)
        inside = abs(measured - law) <= RIPPLE * abs(1 - law) + 1e-9 if radius >= 6 else None
        verdict = "-" if inside is None else ("inside" if inside else "outside")
        print(
            f"| {radius} | {k:.3f} | {1 / (1 + k):.4f} | {measured:.4f} | {law:.4f} | {shell_law:.4f} | "
            f"{first:.4f} | the 1 / r law within {RIPPLE * 100:.0f} % of its shift: {verdict} |"
        )
        if inside is not None and radius != reference:
            criteria.append((f"redshift ratio at r = {radius} against the 1 / r law", inside))
    print()
    return criteria


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    args = parser.parse_args(argv)
    readings = find_runs(args.root)
    if not readings:
        print(f"no redshift run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.kind}: {label}")
            failed += not ok
    print()
    readings_inside = print_shells(readings)
    print_singles(readings)
    readings_inside += print_redshift(readings)
    inside = sum(1 for _, ok in readings_inside if ok)
    print(
        f"{failed} record check(s) failed; {inside} reading(s) inside, {len(readings_inside) - inside} outside"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
