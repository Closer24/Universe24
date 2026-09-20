"""The readings of the Heisenberg run A10 under the law of the ray: the
width of an opening and the spread behind it.

Reads the run folders of the worlds of `examples/events/heisenberg/` (the
runner's `run.json`, the folders told apart by the `model` of their record,
`rays-heisenberg-w<w>-<reading>-v1`) and prints, per run, the screen's
record per pixel (the 161 one-Node detectors `screen_<y>`, their cumulative
`record`: under `wave` the square of the coherent pointer, under `beam` the
count of the clicks that survived the pairing) and per pixel its plain
count of clicks; the angle of a pixel, theta = atan((y - centre) / L) with
L the screen's distance behind the wall; and the spread of what reached
the screen: the full width at half maximum of the record over sin theta
(the record smoothed by a moving mean over five pixels, the half maximum
found by linear interpolation on each side of the peak; "beyond the screen"
when the record does not fall to half within the screen), the same width
of the count (the control: the fan itself, which the width w does not
narrow), the record-weighted and count-weighted root mean squares of sin
theta, and the product w x the record's width in sin theta against the
expectation of the coherent record of w emitters one Link apart at the
wavelength lambda = c x period (0.886 lambda for w >= lambda, the width of
sinc^2; README.md there). The record checks (completed, the books balanced
at every tick) fail the tool; the readings are registered inside or
outside their expectation (docs/EXPERIMENTS.md, "A10, the width of an
opening and the spread behind it, under the law of the ray") and never
moved.

    PYTHONPATH=src python tools/heisenberg_readings.py artifacts/heisenberg
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

from event_universe.core.integer import by_clock
from event_universe.events import parse_nature_beam_world
from event_universe.json_documents import parse_json_document

# Every rule of the engine this tool needs is read off the engine's own
# functions (the architecture review of 2026-09-20, Highlights 5.4: a tool
# is a reader of the record, never a second owner of a rule): the lamp's
# turn off the clock `core.integer.by_clock` (the primitive the engine's
# frame calls), the world's keys through
# `parse_nature_beam_world`; the records are the run's (`run.json`, the
# `DetectorSet` record per screen pixel).
MODEL_PREFIX = "rays-heisenberg-"
MODEL_SUFFIX = "-v1"
SMOOTH = 5
SINC_HALF = 1.39156  # the x at which (sin x / x)^2 = 1/2
# The speed of the law's design, 1 / sqrt 3 Links per interval (RAY_LAW
# section 3): the wavelength of the derivation, lambda = c x period, is at
# this nominal c; the flight table rounds T_d = isqrt(3 |v|^2 Q^2) to an
# integer per direction, differently on each direction of the fan.
SPEED_DIVISOR = math.sqrt(3)


@dataclass
class Reading:
    name: str
    width: int
    reading: str
    wall_x: int
    screen_x: int
    centre: int
    wavelength: float
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    record: list[int] = field(default_factory=list)
    count: list[int] = field(default_factory=list)
    opening_clicks: int = 0
    escaped: int = 0

    @property
    def distance(self) -> int:
        return self.screen_x - self.wall_x

    def sine(self, y: int) -> float:
        dy = y - self.centre
        return dy / math.hypot(self.distance, dy)

    def expected_width(self) -> float | None:
        """The full width at half maximum in sin theta of the coherent
        record of w emitters one Link apart, [sin(pi w s / lambda) /
        (w sin(pi s / lambda))]^2, solved numerically; None when it lies
        beyond sin theta = 1 (no half maximum: a fan)."""
        w, lam = self.width, self.wavelength
        if w == 1:
            return None
        lo, hi = 0.0, 1.0

        def factor(s: float) -> float:
            x = math.pi * s / lam
            d = w * math.sin(x)
            return 1.0 if d == 0 else (math.sin(w * x) / d) ** 2

        if factor(1.0) > 0.5:
            return None
        for _ in range(60):
            mid = (lo + hi) / 2
            if factor(mid) > 0.5:
                lo = mid
            else:
                hi = mid
        return 2 * (lo + hi) / 2


def smooth(values: list[float]) -> list[float]:
    half = SMOOTH // 2
    out = []
    for i in range(len(values)):
        window = values[max(0, i - half) : i + half + 1]
        out.append(sum(window) / len(window))
    return out


def half_width(profile: list[float], sines: list[float]) -> tuple[float | None, float, float]:
    """The full width at half maximum of `profile` over `sines`: (the
    width or None when the profile does not fall to half on both sides
    within the screen, the peak's sine, the width's lower bound within
    the screen)."""
    peak = max(range(len(profile)), key=lambda i: profile[i])
    top = profile[peak]
    if top <= 0:
        return None, 0.0, 0.0
    half = top / 2

    def cross(direction: int) -> float | None:
        i = peak
        while 0 <= i + direction < len(profile):
            j = i + direction
            if profile[j] <= half:
                # Linear interpolation between i and j.
                fraction = (profile[i] - half) / (profile[i] - profile[j])
                return sines[i] + fraction * (sines[j] - sines[i])
            i = j
        return None

    left, right = cross(-1), cross(1)
    bound = (right if right is not None else sines[-1]) - (left if left is not None else sines[0])
    if left is None or right is None:
        return None, sines[peak], bound
    return right - left, sines[peak], bound


def rms(weights: list[float], sines: list[float]) -> float:
    total = sum(weights)
    if total <= 0:
        return 0.0
    mean = sum(w * s for w, s in zip(weights, sines, strict=True)) / total
    return math.sqrt(sum(w * (s - mean) ** 2 for w, s in zip(weights, sines, strict=True)) / total)


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    name = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)]
    width_part, reading = name.split("-")
    # The world as the engine parses it (the keys with their defaults).
    world = parse_nature_beam_world(parse_json_document((folder / "initialization.json").read_bytes()))
    lamp = next(m for m in world.measured if m.lamp is not None)
    # The lamp's turn per self-creation off the engine's clock, `by_clock(age,
    # content, K)` (the frame, ENGINE.md), at its first self-creation: the
    # lamps' content is 8 K + 1 400 000 and what a run spends never reaches
    # the next step of the clock, so the turn is the same at every age.
    turn = by_clock(0, lamp.amount, world.clock)
    wavelength = (world.phase_steps / turn) / SPEED_DIVISOR
    # The wall is the row of measured events that re-emit (the opening), the
    # screen the other row of the family `wall`.
    wall_x = next(m.position[0] for m in world.measured if "rerelease" in m.table)
    screen = sorted(
        (int(d["name"].split("_")[1]), d) for d in record["detectors"] if d["name"].startswith("screen_")
    )
    screen_x = next(
        m.position[0]
        for m in world.measured
        if m.position[0] != wall_x and world.families[m.family].name == "wall"
    )
    height = len(screen)
    reading_ = Reading(
        name=name.replace("-", "_"),
        width=int(width_part[1:]),
        reading=reading,
        wall_x=wall_x,
        screen_x=screen_x,
        centre=height // 2,
        wavelength=wavelength,
        ticks=int(record["completed_ticks"]),
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
    )
    reading_.record = [int(d["families"]["light"]["record"]) for _, d in screen]
    reading_.count = [int(d["families"]["light"]["clicks"]) for _, d in screen]
    reading_.opening_clicks = sum(
        int(m["measured"][0]["rerelease"]) for m in record["measured"] if m["detector"] == 0
    )
    reading_.escaped = int(record["escaped"][0]["amount"])
    return reading_


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    return sorted(found, key=lambda r: (r.reading, r.width))


def analyse(r: Reading) -> dict[str, object]:
    sines = [r.sine(y) for y in range(len(r.record))]
    rec = smooth([float(v) for v in r.record])
    cnt = smooth([float(v) for v in r.count])
    rec_width, rec_peak, rec_bound = half_width(rec, sines)
    cnt_width, _, cnt_bound = half_width(cnt, sines)
    expected = r.expected_width()
    return {
        "record_width": rec_width,
        "record_bound": rec_bound,
        "record_peak": rec_peak,
        "count_width": cnt_width,
        "count_bound": cnt_bound,
        "record_rms": rms([float(v) for v in r.record], sines),
        "count_rms": rms([float(v) for v in r.count], sines),
        "expected_width": expected,
        "product": None if rec_width is None else r.width * rec_width,
        "expected_product": None if expected is None else r.width * expected,
        "screen_sine": sines[-1] - sines[0],
    }


def fmt(value: float | None, digits: int = 3) -> str:
    return "-" if value is None else f"{value:.{digits}f}"


def print_table(readings: list[Reading]) -> None:
    print(
        "| World | reading | w | record FWHM in sin theta (expected) | count FWHM (the fan) | "
        "record rms | count rms | w x record FWHM (expected 0.886 lambda = "
        f"{0.886 * readings[0].wavelength:.2f} for w >= lambda) | clicks on the screen | escaped |"
    )
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in readings:
        a = analyse(r)
        rec = (
            f"{fmt(a['record_width'])} ({fmt(a['expected_width'])})"
            if a["record_width"] is not None
            else f"beyond the screen, > {fmt(a['record_bound'])} ({fmt(a['expected_width']) if a['expected_width'] is not None else 'the fan'})"
        )
        cnt = (
            fmt(a["count_width"])
            if a["count_width"] is not None
            else f"beyond the screen, > {fmt(a['count_bound'])}"
        )
        product = (
            f"{fmt(a['product'], 2)} ({fmt(a['expected_product'], 2)})"
            if a["product"] is not None
            else f"> {fmt(r.width * a['record_bound'], 2)} ({fmt(a['expected_product'], 2) if a['expected_product'] is not None else 'the fan'})"
        )
        print(
            f"| `{r.name}` | {r.reading} | {r.width} | {rec} | {cnt} | {fmt(a['record_rms'])} | "
            f"{fmt(a['count_rms'])} | {product} | {sum(r.count)} | {r.escaped} |"
        )


def print_profiles(readings: list[Reading]) -> None:
    for r in readings:
        peak = max(range(len(r.record)), key=lambda i: r.record[i])
        lo, hi = max(0, peak - 20), min(len(r.record), peak + 21)
        line = ", ".join(f"{y}:{r.record[y]}" for y in range(lo, hi))
        print(f"{r.name}: the record about its peak at y = {peak}: {line}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    parser.add_argument("--profiles", action="store_true", help="print the record about its peak")
    args = parser.parse_args(argv)
    readings = find_runs(args.root)
    if not readings:
        print(f"no Heisenberg run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.name}: {label} ({r.ticks} ticks, {r.elapsed:.1f} s)")
            failed += not ok
    print()
    print(
        f"lambda = c x period = {readings[0].wavelength:.3f} Links; L = {readings[0].distance} Links; "
        f"the screen spans sin theta in [{readings[0].sine(0):.3f}, "
        f"{readings[0].sine(len(readings[0].record) - 1):.3f}]"
    )
    print_table(readings)
    if args.profiles:
        print()
        print_profiles(readings)
    print()
    print(f"{failed} record check(s) failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
