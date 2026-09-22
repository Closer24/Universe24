"""The readings of the atom's baseline run (docs/designs/atom_baseline/RUN.md):
hydrogen at r = 12 as the law stands, the world `examples/events/atoms/
hydrogen_r12.json` run once, headless, by the register's runner; this host
script reads the run's records (`run.json`, `events.jsonl`, the world through
`world_of_run`) and prints every number labelled by its kind (the model
owner, records 281 and 754): DETECTOR, a detector's record or a measured
event's own record (the faces' `click` lines, the proton's `read` lines,
the clicks per detector of `run.json`); GAMEBOARD, the host's view of the
board (the electron's `step` lines: its position, radius, phase), printed
beside as a diagnostic, never pinned.

The method, fixed before the run (RUN.md section 3):

- Every release of the electron (one unit per in-plane heading every 10 of
  its self-creations, from one Node of its set) ends at one of the four
  side faces, and the click's Node on the face carries the electron's
  coordinate across the flight: `face:+x` and `face:-x` its y, `face:+y`
  and `face:-y` its x. The clicks of one release are paired by the flight
  table's own delays (`Flight.manhattan_steps`, the engine's): a `face:+x`
  click at t1 with Node y and a `face:+y` click at t2 with Node x belong to
  one release when t1 - f(52 - x) = t2 - f(52 - y) within the pairing
  tolerance; the release count is that common value. The electron's
  position per release is then (x, y), read at two detector Nodes.
- The crossings: a pass of y through the proton's y = 26 with x > 26 is a
  crossing of the +x axis (the start's), with x < 26 of the -x axis; a
  pass of x through 26 with y > 26 of the +y axis, y < 26 of the -y axis.
  The period is the count between two successive crossings of one axis;
  the returns are the crossings of the +x axis after the start.
- The dwell: on the face that carries the coordinate of motion at a
  crossing, the count from the first click at one Node to the first click
  at the next, for the hops within two Nodes of the crossing.
- The closure: the phase stamped on the rows of successive releases,
  unwrapped (an increment below N / 2 per release), summed over one return
  and divided by N: the circles per return j; the residue in steps of N.
- The proton's reads: the `read` lines of the proton (measured event 1)
  for the electron's family, counted per crossing.

    PYTHONPATH=src python docs/designs/atom_baseline/baseline_readings.py artifacts/atom_baseline/hydrogen_r12/run
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from event_universe.events.nature_beam import direction_flight
from event_universe.world_loading import world_of_run

GAMEBOARD = "GAMEBOARD"
DETECTOR = "DETECTOR"
PROTON = 1
ELECTRON = 2
FACE_HEADINGS = {
    "face:+x": (1, 0, 0),
    "face:-x": (-1, 0, 0),
    "face:+y": (0, 1, 0),
    "face:-y": (0, -1, 0),
}
PAIRING_TOLERANCE = 3
RELEASE_PERIOD = 10
HOPS_ABOUT_CROSSING = 2

# The pins of RUN.md section 2 (GAMEBOARD by formula until a detector clicks).
PIN_DWELL = (19.0, 20.5)
PIN_DWELL_TOLERANCE = 2.0
PIN_PERIOD = 1552
PIN_PERIOD_SHARE = 0.15
PIN_RETURNS = (4, 5)
PIN_RETURN_LINKS = 3
PIN_CIRCLES = 4.0
PIN_CIRCLES_TOLERANCE = 0.05
PIN_RESIDUE_STEPS = 3
PIN_READS_PER_CROSSING = (0, 2)
PIN_FACE_CLICKS = 750


@dataclass
class Release:
    count: int
    x: int
    y: int
    phase: int
    faces: dict[str, tuple[int, tuple[int, int, int], int]] = field(default_factory=dict)


@dataclass
class Crossing:
    axis: str
    count: int
    x: int
    y: int
    index: int


def flight_delay(heading: tuple[int, int, int], links: int) -> int:
    """The least age at which a row on `heading` has made `links` Manhattan
    steps (the engine's flight table)."""
    table = direction_flight((heading,))
    age = 0
    while int(table.manhattan_steps(np.array([0]), np.array([age]))[0]) < links:
        age += 1
    return age


def unwrap(previous: int, current: int, modulus: int) -> int:
    delta = (current - previous) % modulus
    return delta - modulus if delta > modulus // 2 else delta


def read_events(folder: Path, electron_family: str, proton_family: str):
    clicks: dict[str, list[tuple[int, tuple[int, int, int], int]]] = {name: [] for name in FACE_HEADINGS}
    proton_reads: list[int] = []
    electron_reads = 0
    steps: dict[int, tuple[tuple[int, int, int], list[int], int]] = {}
    escaped = ""
    electron_key = f'"family": "{electron_family}"'
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"step"' not in line and electron_key not in line and '"read"' not in line:
                continue
            event = json.loads(line)
            kind = event["event"]
            if kind == "step" and event["number"] == ELECTRON:
                to = event["to"]
                steps[int(event["tick"])] = (
                    (int(to[0]), int(to[1]), int(to[2])),
                    [int(v) for v in event["momentum"]],
                    int(event["phase"]),
                )
            elif kind == "click" and event["family"] == electron_family and event["measured"] is None:
                name = str(event["detector"])
                if name in clicks:
                    node = event["node"]
                    clicks[name].append(
                        (
                            int(event["tick"]),
                            (int(node[0]), int(node[1]), int(node[2])),
                            int(event["phase"]),
                        )
                    )
            elif kind == "click" and event.get("measured") == ELECTRON:
                escaped = f"the electron left through {event['detector']} at tick {event['tick']}"
            elif kind == "read" and event["measured"] == PROTON and event["family"] == electron_family:
                proton_reads.append(int(event["tick"]))
            elif kind == "read" and event["measured"] == ELECTRON and event["family"] == proton_family:
                electron_reads += 1
    return clicks, proton_reads, electron_reads, steps, escaped


def pair_releases(clicks, side: int) -> tuple[list[Release], int]:
    """The releases from the faces' clicks: each `face:+x` click paired with
    the `face:+y` click of the same release by the flight delays; then the
    two other faces attached the same way. Returns the releases and the
    count of clicks left unpaired."""
    delays: dict[tuple[str, int], int] = {}

    def delay(face: str, links: int) -> int:
        key = (face, links)
        if key not in delays:
            delays[key] = flight_delay(FACE_HEADINGS[face], links)
        return delays[key]

    far = side - 1
    plus_y = list(clicks["face:+y"])
    used_y = [False] * len(plus_y)
    releases: list[Release] = []
    unpaired = 0
    for t1, node1, phase1 in clicks["face:+x"]:
        y = node1[1]
        found = None
        for k, (t2, node2, phase2) in enumerate(plus_y):
            if used_y[k]:
                continue
            x = node2[0]
            c1 = t1 - delay("face:+x", far - x)
            c2 = t2 - delay("face:+y", far - y)
            # The four units of one release land on the set's Nodes by the
            # Nodes' claims (BEAM_LAW note 41 (viii)), so their z differ.
            if abs(c1 - c2) <= PAIRING_TOLERANCE and phase1 == phase2:
                found = (k, x, c1)
                break
            if t2 - t1 > 70:
                break
        if found is None:
            unpaired += 1
            continue
        k, x, count = found
        used_y[k] = True
        release = Release(count, x, y, phase1)
        release.faces["face:+x"] = (t1, node1, phase1)
        release.faces["face:+y"] = plus_y[k]
        releases.append(release)
    unpaired += used_y.count(False)
    # The two other faces, attached to the release whose count and Node match.
    by_count: dict[int, Release] = {}
    for release in releases:
        by_count[release.count] = release
    for face, axis in (("face:-x", 1), ("face:-y", 0)):
        for t, node, phase in clicks[face]:
            coordinate = node[axis]
            attached = False
            for offset in range(-PAIRING_TOLERANCE, PAIRING_TOLERANCE + 1):
                # The flight from the electron to the near face is its own
                # coordinate on the flight axis.
                for candidate in by_count.values():
                    own = candidate.x if face == "face:-x" else candidate.y
                    across = candidate.y if face == "face:-x" else candidate.x
                    if across != coordinate or candidate.phase != phase:
                        continue
                    if t - delay(face, own) == candidate.count + offset and face not in candidate.faces:
                        candidate.faces[face] = (t, node, phase)
                        attached = True
                        break
                if attached:
                    break
            if not attached:
                unpaired += 1
    releases.sort(key=lambda r: r.count)
    return releases, unpaired


def crossings_of(releases: list[Release], centre: tuple[int, int]) -> list[Crossing]:
    """The axis crossings read from the releases' positions: the first
    release of each pass at the axis's coordinate on the axis's side."""
    found: list[Crossing] = []
    cx, cy = centre
    previous: Release | None = None
    for index, release in enumerate(releases):
        if previous is not None:
            # A pass of y through cy on the +x side (x > cx) or the -x side.
            if (previous.y - cy) * (release.y - cy) <= 0 and previous.y != release.y:
                if release.y == cy or previous.y != cy:
                    side = "+x" if release.x > cx else "-x"
                    found.append(Crossing(side, release.count, release.x, release.y, index))
            if (previous.x - cx) * (release.x - cx) <= 0 and previous.x != release.x:
                if release.x == cx or previous.x != cx:
                    side = "+y" if release.y > cy else "-y"
                    found.append(Crossing(side, release.count, release.x, release.y, index))
        previous = release
    # One crossing per pass: drop a repeat of the same axis within 100 counts.
    kept: list[Crossing] = []
    for crossing in found:
        if kept and kept[-1].axis == crossing.axis and crossing.count - kept[-1].count < 100:
            continue
        kept.append(crossing)
    return kept


def dwell_gaps(releases: list[Release], crossings: list[Crossing], centre: tuple[int, int]) -> list[int]:
    """The count from the first release at one Node to the first release at
    the next along the axis of motion, for the hops within
    HOPS_ABOUT_CROSSING Nodes of each crossing (DETECTOR: the faces' arrival
    Nodes and counts)."""
    gaps: list[int] = []
    cx, cy = centre
    for crossing in crossings:
        moving = "y" if crossing.axis in ("+x", "-x") else "x"
        centre_value = cy if moving == "y" else cx
        window = [
            r
            for r in releases
            if abs(r.count - crossing.count) <= 400
            and abs((r.y if moving == "y" else r.x) - centre_value) <= HOPS_ABOUT_CROSSING
            and (
                (r.x > cx)
                if crossing.axis == "+x"
                else (r.x < cx)
                if crossing.axis == "-x"
                else (r.y > cy)
                if crossing.axis == "+y"
                else (r.y < cy)
            )
        ]
        first_at: dict[int, int] = {}
        for r in window:
            coordinate = r.y if moving == "y" else r.x
            first_at.setdefault(coordinate, r.count)
        ordered = sorted(first_at.items(), key=lambda kv: kv[1])
        for (c0, t0), (c1, t1) in zip(ordered, ordered[1:], strict=False):
            if abs(c1 - c0) == 1:
                gaps.append(t1 - t0)
    return gaps


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder", type=Path, help="the run folder (run.json, events.jsonl)")
    args = parser.parse_args(argv)
    folder = args.folder
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    world = world_of_run(folder)
    proton, electron = world["measured"]
    centre3 = tuple(int(v) for v in proton["position"])
    centre = (centre3[0], centre3[1])
    side = int(world["shape"][0])
    modulus = int(world["N"])
    action = int(world["action"])
    momentum = [int(v) for v in electron["momentum"]]
    start = tuple(int(v) for v in electron["position"])
    electron_family, proton_family = str(electron["family"]), str(proton["family"])
    verdicts: list[tuple[str, bool]] = []

    completed = record["status"] == "completed"
    balanced = bool(record["conserved_at_every_completed_tick"])
    ticks = int(record["completed_ticks"])
    print(
        f"{'PASS' if completed else 'FAIL'} record check: completed ({record['elapsed_seconds']:.1f} s, {ticks} ticks)"
    )
    print(f"{'PASS' if balanced else 'FAIL'} record check: the books balanced at every completed tick")
    print(
        f"[{GAMEBOARD}] world `{record['model']}`: h = {action}, N = {modulus}, the electron's declared momentum {momentum}, start {start}, the proton at {centre3}"
    )
    print()

    # The clicks per detector (DETECTOR, run.json).
    print(f"[{DETECTOR}] the clicks per detector over the run (run.json `detectors`, per family):")
    face_clicks_e: dict[str, int] = {}
    for detector in record["detectors"]:
        name = str(detector["name"])
        families = detector["families"]
        parts = []
        for family, values in families.items():
            parts.append(
                f"{family}: clicks {values.get('clicks', 0)}, measured {values.get('measured', 0)}, record {values.get('record', 0)}"
            )
        print(
            f"[{DETECTOR}]   {name} ({detector.get('nodes', '?')} Nodes, {detector.get('reading', '?')}): "
            + "; ".join(parts)
        )
        if name in FACE_HEADINGS:
            face_clicks_e[name] = int(families.get(electron_family, {}).get("clicks", 0))
    escaped_record = record.get("escaped", [])
    entries = escaped_record.items() if isinstance(escaped_record, dict) else enumerate(escaped_record)
    for family, values in entries:
        print(f"[{DETECTOR}]   escaped {family}: {values}")
    clicks, proton_reads, electron_reads, steps, escaped = read_events(
        folder, electron_family, proton_family
    )
    print(
        f"[{DETECTOR}] the electron's rows clicked on the side faces (events.jsonl): "
        + ", ".join(f"{name} {len(rows)}" for name, rows in clicks.items())
    )
    inside = all(face_clicks_e.get(name, 0) == PIN_FACE_CLICKS for name in FACE_HEADINGS) and not escaped
    verdicts.append(
        (
            f"P6 the electron's rows on each side face: {PIN_FACE_CLICKS} each (read {sorted(face_clicks_e.values())})",
            inside,
        )
    )
    print(
        f"[{DETECTOR}] the proton's reads of the electron's rows: {len(proton_reads)} `read` lines; the electron's own reads of the proton's rows: {electron_reads}"
    )
    print(f"[{DETECTOR}] {escaped or 'no escape of the electron recorded on a face'}")
    print()

    # The releases from the faces' clicks (DETECTOR).
    releases, unpaired = pair_releases(clicks, side)
    counts = [r.count for r in releases]
    residuals = sorted({c % RELEASE_PERIOD for c in counts})
    print(
        f"[{DETECTOR}] releases read from the faces' clicks: {len(releases)} paired (+x with +y), {unpaired} clicks unpaired; the release counts modulo {RELEASE_PERIOD}: {residuals}; the first at {counts[0] if counts else '-'}, the last at {counts[-1] if counts else '-'}"
    )
    if len(releases) < 4:
        print("too few releases to read a loop")
        return 1
    distances = [math.dist((r.x, r.y), centre) for r in releases]
    print(
        f"[{DETECTOR}] the electron's position per release from the arrival Nodes: the distance from the proton's Node "
        f"least {min(distances):.2f}, greatest {max(distances):.2f} Links; the last release read at ({releases[-1].x}, {releases[-1].y}) at count {releases[-1].count}"
    )
    crossings = crossings_of(releases, centre)
    print(f"[{DETECTOR}] the axis crossings read from the arrival Nodes: {len(crossings)}")
    for crossing in crossings:
        print(
            f"[{DETECTOR}]   {crossing.axis} at count {crossing.count}: the electron at ({crossing.x}, {crossing.y}), {math.dist((crossing.x, crossing.y), centre):.2f} Links from the proton"
        )
    plus_x = [c for c in crossings if c.axis == "+x"]
    periods = [b.count - a.count for a, b in zip(plus_x, plus_x[1:], strict=False)]
    returns = len(plus_x)
    bracket = (round(PIN_PERIOD * (1 - PIN_PERIOD_SHARE)), round(PIN_PERIOD * (1 + PIN_PERIOD_SHARE)))
    return_links = [abs(c.x - start[0]) + abs(c.y - start[1]) for c in plus_x]
    print(
        f"[{DETECTOR}] the returns to the +x axis: {returns}, the counts between them {periods}; the return's distance from the start in Links {return_links}"
    )
    inside = (
        returns in PIN_RETURNS and all(bracket[0] <= T <= bracket[1] for T in periods) and bool(periods)
    )
    verdicts.append(
        (
            f"P2 returns to the +x axis {PIN_RETURNS[0]} to {PIN_RETURNS[1]} with every period within {bracket} (read {returns}, {periods})",
            inside,
        )
    )
    verdicts.append(
        (
            f"P2b every return within {PIN_RETURN_LINKS} Links of the start (read {return_links})",
            bool(return_links) and all(d <= PIN_RETURN_LINKS for d in return_links),
        )
    )
    for axis in ("+y", "-x", "-y"):
        same = [c for c in crossings if c.axis == axis]
        print(
            f"[{DETECTOR}]   the {axis} crossings: {len(same)}, the counts between them {[b.count - a.count for a, b in zip(same, same[1:], strict=False)]}"
        )
    print()

    # The dwell (DETECTOR).
    gaps = dwell_gaps(releases, crossings, centre)
    mean_gap = sum(gaps) / len(gaps) if gaps else float("nan")
    print(
        f"[{DETECTOR}] the dwell about the crossings, first click to first click at the next Node along the motion: {len(gaps)} hops, the gaps {gaps}"
    )
    print(
        f"[{DETECTOR}] the mean dwell over those hops: {mean_gap:.2f} counts per Link (the release grain {RELEASE_PERIOD})"
    )
    inside = bool(gaps) and (PIN_DWELL[0] - PIN_DWELL_TOLERANCE) <= mean_gap <= (
        PIN_DWELL[1] + PIN_DWELL_TOLERANCE
    )
    verdicts.append(
        (
            f"P1 the mean dwell per Node about the crossings within {PIN_DWELL[0] - PIN_DWELL_TOLERANCE:.0f} to {PIN_DWELL[1] + PIN_DWELL_TOLERANCE:.1f} counts (read {mean_gap:.2f} over {len(gaps)} hops)",
            inside,
        )
    )
    print()

    # The closure from the rows' phases (DETECTOR).
    increments = [
        unwrap(a.phase, b.phase, modulus) for a, b in zip(releases, releases[1:], strict=False)
    ]
    cumulative = [0]
    for d in increments:
        cumulative.append(cumulative[-1] + d)
    print(
        f"[{DETECTOR}] the phase per release: the increments' range {min(increments) if increments else '-'} to {max(increments) if increments else '-'} steps (unwrapped below N / 2 = {modulus // 2}); the mean {sum(increments) / len(increments):.3f} steps per release"
    )
    circles: list[float] = []
    residues: list[int] = []
    for a, b in zip(plus_x, plus_x[1:], strict=False):
        turned = cumulative[b.index] - cumulative[a.index]
        circles.append(turned / modulus)
        residue = turned % modulus
        residues.append(residue - modulus if residue > modulus // 2 else residue)
    print(
        f"[{DETECTOR}] the circles per return j (the sum of the increments over a return over N): {[f'{j:.3f}' for j in circles]}; the residue in steps of {modulus}: {residues}"
    )
    inside = bool(circles) and all(abs(j - PIN_CIRCLES) <= PIN_CIRCLES_TOLERANCE for j in circles)
    verdicts.append(
        (
            f"P3 the circles per return j = {PIN_CIRCLES:.2f} within {PIN_CIRCLES_TOLERANCE} (read {[f'{j:.3f}' for j in circles]})",
            inside,
        )
    )
    inside = bool(residues) and all(abs(s) <= PIN_RESIDUE_STEPS for s in residues)
    verdicts.append(
        (
            f"P3b the residue per return within {PIN_RESIDUE_STEPS} steps of {modulus} (read {residues})",
            inside,
        )
    )
    # The phase at the same axis, return by return.
    print(
        f"[{DETECTOR}] the phase stamped at the +x crossings: {[releases[c.index].phase for c in plus_x]} (the same step every return on a closed loop, within the release grain)"
    )
    print()

    # The proton's reads per crossing (DETECTOR).
    per_crossing: list[int] = []
    for crossing in crossings:
        per_crossing.append(sum(1 for t in proton_reads if abs(t - crossing.count - 20) <= 60))
    print(
        f"[{DETECTOR}] the proton's reads of the electron's rows per crossing (within 60 counts of the crossing plus the flight): {per_crossing}; total {len(proton_reads)}"
    )
    inside = bool(per_crossing) and all(
        PIN_READS_PER_CROSSING[0] <= n <= PIN_READS_PER_CROSSING[1] for n in per_crossing
    )
    verdicts.append(
        (
            f"P5 the proton's reads per crossing within {PIN_READS_PER_CROSSING} (read {per_crossing})",
            inside,
        )
    )
    print()

    # The GameBoard diagnostics (the step lines).
    position = start
    phase = int(electron.get("phase", 0))
    positions = [position]
    phases = [phase]
    for tick in range(1, ticks + 1):
        if tick in steps:
            position, _, phase = steps[tick]
        positions.append(position)
        phases.append(phase)
    radii = [math.dist(p, centre3) for p in positions]
    unwrapped = 0.0
    previous = math.atan2(start[1] - centre3[1], start[0] - centre3[0])
    closings: list[int] = []
    for tick, (x, y, _) in enumerate(positions):
        angle = math.atan2(y - centre3[1], x - centre3[0])
        delta = angle - previous
        if delta > math.pi:
            delta -= 2 * math.pi
        elif delta < -math.pi:
            delta += 2 * math.pi
        unwrapped += delta
        previous = angle
        if unwrapped >= 2 * math.pi * (len(closings) + 1):
            closings.append(tick)
    print(
        f"[{GAMEBOARD}] (a diagnostic, not pinned) the electron's radius over the run from its step lines: least {min(radii):.2f}, greatest {max(radii):.2f}, at the end {radii[-1]:.2f} at {positions[-1]}; {unwrapped / (2 * math.pi):.2f} turns of the angle; the closings of the angle at ticks {closings}, T {[b - a for a, b in zip([0] + closings, closings, strict=False)]}"
    )
    print(
        f"[{GAMEBOARD}] (a diagnostic) the loop {'stays on the GameBoard' if not escaped and 6 <= radii[-1] <= 20 else 'does not stay'}: the electron {'on the GameBoard at the end' if not escaped else escaped}"
    )
    # The per-axis action sums over the crossed Links between closings.
    step_ticks = sorted(steps)
    print(
        f"[{GAMEBOARD}] (a diagnostic) the per-axis action gained over the crossed Links between closings, |p_a| N summed on the axis stepped, as quotients of h with the fraction:"
    )
    bounds = [0] + closings
    for a, b in zip(bounds, bounds[1:], strict=False):
        sums = [0, 0, 0]
        for tick in step_ticks:
            if a < tick <= b:
                to, p, _ = steps[tick]
                came = positions[tick - 1]
                axis = next(k for k in range(3) if to[k] != came[k])
                sums[axis] += abs(p[axis]) * modulus
        quotients = [s / action for s in sums]
        print(
            f"[{GAMEBOARD}]   closing at {b}: x {quotients[0]:.3f}, y {quotients[1]:.3f}, z {quotients[2]:.3f}; the sum {sum(quotients):.3f} = {sum(quotients) / modulus:.4f} circles; the body's phase at the closing {phases[b]}"
        )
    dwell_exact: list[int] = []
    for crossing in crossings:
        moving = 1 if crossing.axis in ("+x", "-x") else 0
        hop_ticks = [
            t
            for t in step_ticks
            if abs(t - crossing.count) <= 400
            and steps[t][0][moving] != positions[t - 1][moving]
            and abs(steps[t][0][moving] - centre3[moving]) <= HOPS_ABOUT_CROSSING + 1
        ]
        dwell_exact += [b - a for a, b in zip(hop_ticks, hop_ticks[1:], strict=False)]
    if dwell_exact:
        print(
            f"[{GAMEBOARD}] (a diagnostic) the dwell from the step lines at the same hops: {len(dwell_exact)} gaps, the mean {sum(dwell_exact) / len(dwell_exact):.2f}, the least {min(dwell_exact)}, the greatest {max(dwell_exact)} (the formula's 19.05 at the start's crossing)"
        )
    print()
    for label, ok in verdicts:
        print(f"{'PASS' if ok else 'FAIL'} {label}")
    print(
        f"{sum(1 for _, ok in verdicts if ok)} PASS, {sum(1 for _, ok in verdicts if not ok)} FAIL of {len(verdicts)} pins (DETECTOR); the GameBoard lines above are diagnostics, not counted"
    )
    return 0 if completed and balanced else 1


if __name__ == "__main__":
    sys.exit(main())
