"""The readings of the Heisenberg run A10 at a low rate, "the single-click
build-up": the registered A10 world at w = 27 under the `wave` reading run
at three source rates (docs/EXPERIMENTS.md, "A10 at a low rate, the
single-click build-up"; examples/events/buildup/make_worlds.py; the model
owner's go of 2026-09-20 on the law's own predictions, the physicist's
entry 5: "the wave is only in the detector: a screen that counts single
clicks shows no fringes").

Reads the run folders of the worlds (the runner's `run.json`,
`initialization.json` and `events.jsonl`, told apart by the `model` of the
record, `rays-buildup-w<w>-rate<n>-v1`) and prints, per rate, DETECTOR
readings only (the screen's 161 one-Node `wave` pixels, each a
`DetectorSet`), over the late window from `--window-start` (260 by
default, when every direction of the fan that lands on the screen has
arrived) to the end of the run:

- per pixel the plain count of clicks C and the coherent record R (the
  per-interval `record` lines summed: the square of the pointer of the
  rays the pixel clicked in one interval), and the incoherent sum I, what
  the record would be if every unit had been alone in its interval (the
  square of one unit's amplitude at the click's phase through the
  engine's `coherent_pointer`, times the amount); the cross term R - I
  and the ratio R / I, which is 1 exactly at a pixel that never clicked
  two units in one interval;
- the spread of the record and of the count over sin theta (the FWHM
  after the five-pixel moving mean and the weighted rms, the reading of
  A10 through `tools/heisenberg_readings.py`), the narrowing 1 - rms_R /
  rms_C, and w x FWHM;
- the coincidences: the number of (pixel, interval) cells in which the
  pixel's record summed two or more rays, their share of the cells with a
  click, and the share of the clicks that arrived in such cells; and the
  mean rays per pixel per interval, the rate the runs are ordered by.

The expectation, written before the runs (README.md): the law's cross
terms exist only in the cells with two or more rays, so at the lowest rate
R = I at every pixel, the record's spread is the count's (the narrowing 0)
and the lobe of A10 is not formed; at the highest rate the record narrows
as A10 read (the narrowing about 0.3). Nature builds the same fringes one
particle at a time, the narrowing the same at every rate. The record
checks (completed, the books balanced at every tick) fail the tool; the
readings are registered inside or outside their bracket and never moved.

    PYTHONPATH=src python tools/buildup_readings.py artifacts/buildup
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from event_universe.core.integer import by_clock
from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import parse_nature_beam_world
from event_universe.events.nature_beam import FIRST, coherent_pointer
from event_universe.world_loading import world_of_run

# The spread readings of A10 (the moving mean, the half width, the rms)
# are the sibling tool's, read from it and not copied.
_SPEC = importlib.util.spec_from_file_location(
    "heisenberg_readings_tool", Path(__file__).resolve().with_name("heisenberg_readings.py")
)
assert _SPEC is not None and _SPEC.loader is not None
HEISENBERG = importlib.util.module_from_spec(_SPEC)
sys.modules["heisenberg_readings_tool"] = HEISENBERG
_SPEC.loader.exec_module(HEISENBERG)

MODEL_PREFIX = "rays-buildup-"
MODEL_SUFFIX = "-v1"
SCREEN_PREFIX = "screen_"
DEFAULT_WINDOW_START = 260
# The brackets (README.md): at the lowest rate the narrowing within 0.02 of
# 0 and R / I within 0.02 of 1 at the peak; at the highest rate the
# narrowing above 0.2 (A10 read 0.31).
LOW_NARROWING = 0.02
LOW_RATIO = 0.02
HIGH_NARROWING = 0.2
# A pixel enters the ratio's range when it clicked at least this many rays.
MIN_COUNT = 20
DETECTOR = "DETECTOR"


@dataclass
class Pixel:
    y: int
    record: int = 0  # cumulative, run.json
    clicks: int = 0  # cumulative, run.json
    count: int = 0  # the window
    window_record: int = 0
    incoherent: int = 0
    cells: int = 0  # intervals with a click
    coincidences: int = 0  # intervals with two or more rays
    coincident_clicks: int = 0


@dataclass
class Reading:
    name: str
    width: int
    rate: int
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    wall_x: int
    screen_x: int
    centre: int
    wavelength: float
    window: tuple[int, int]
    pixels: dict[int, Pixel] = field(default_factory=dict)

    @property
    def distance(self) -> int:
        return self.screen_x - self.wall_x

    def sine(self, y: int) -> float:
        dy = y - self.centre
        return dy / math.hypot(self.distance, dy)


def read_run(folder: Path, *, window_start: int = DEFAULT_WINDOW_START) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    width_part, rate_part = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)].split("-")
    world = parse_nature_beam_world(world_of_run(folder))
    lamp = next(m for m in world.measured if m.lamp is not None)
    assert lamp.lamp is not None
    # The lamp's turn per self-creation off the engine's clock, and its rate
    # per self-creation on its one direction: the rate of the world.
    turn = world.turn(0, lamp.amount)
    rate = by_clock(0, lamp.lamp.rate[0], lamp.lamp.rate[1])
    wavelength = (world.phase_steps / turn) / HEISENBERG.SPEED_DIVISOR
    light = world.families[lamp.family].name
    wall_x = next(m.position[0] for m in world.measured if "rerelease" in m.table)
    screen = sorted(
        (int(d["name"].split("_")[1]), d)
        for d in record["detectors"]
        if d["name"].startswith(SCREEN_PREFIX)
    )
    screen_x = next(
        m.position[0]
        for m in world.measured
        if m.position[0] != wall_x and m.lamp is None and world.families[m.family].name != light
    )
    ticks = int(record["completed_ticks"])
    reading = Reading(
        name=f"w{width_part[1:]}_{rate_part}",
        width=int(width_part[1:]),
        rate=rate,
        ticks=ticks,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
        wall_x=wall_x,
        screen_x=screen_x,
        centre=len(screen) // 2,
        wavelength=wavelength,
        # The window is [window_start, ticks]: the run's last tick included.
        window=(window_start, ticks + 1),
    )
    for y, entry in screen:
        pixel = Pixel(y)
        pixel.record = int(entry["families"][light]["record"])
        pixel.clicks = int(entry["families"][light]["clicks"])
        reading.pixels[y] = pixel
    cosines = np.array(phase_cosines(world.phase_steps), dtype=np.int64)
    sines = np.array(phase_sines(world.phase_steps), dtype=np.int64)
    lo, hi = reading.window
    # The clicks of one interval at one pixel, gathered until the pixel's
    # `record` line of that interval (written after the set's last click).
    pending: dict[int, list[tuple[int, int]]] = {}
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"screen_' not in line:
                continue
            event = json.loads(line)
            if event["event"] not in ("click", "record") or event["family"] != light:
                # The layer's lines (a gather names the chosen set) are not
                # the crowd's clicks and records.
                continue
            tick = int(event["tick"])
            if not lo <= tick < hi:
                continue
            y = int(str(event["detector"]).split("_")[1])
            if event["event"] == "click":
                pending.setdefault(y, []).append((int(event["amount"]), int(event["phase"])))
            elif event["event"] == "record":
                rows = pending.pop(y, [])
                pixel = reading.pixels[y]
                total = sum(amount for amount, _ in rows)
                pixel.count += total
                pixel.window_record += int(event["record"])
                pixel.cells += 1
                if total >= 2:
                    pixel.coincidences += 1
                    pixel.coincident_clicks += total
                # Each unit alone: its own amplitude at its phase, squared
                # (a row of `amount` units is that many units).
                for amount, phase in rows:
                    x, yy = coherent_pointer(np.array([1]), np.array([phase]), FIRST, cosines, sines)
                    pixel.incoherent += amount * (x[0] * x[0] + yy[0] * yy[0])
    assert not pending, "a pixel's clicks without its record line"
    return reading


def find_runs(root: Path, *, window_start: int = DEFAULT_WINDOW_START) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent, window_start=window_start))
    return sorted(found, key=lambda r: -r.rate)


@dataclass
class Analysis:
    clicks: int
    cells: int
    coincidences: int
    coincident_clicks: int
    rays_per_pixel_interval: float
    record_width: float | None
    count_width: float | None
    record_rms: float
    count_rms: float
    narrowing: float
    ratio_peak: float
    ratio_centre: float
    ratio_min: float
    ratio_max: float
    peak: int
    cross: int


def analyse(reading: Reading) -> Analysis:
    ys = sorted(reading.pixels)
    sines = [reading.sine(y) for y in ys]
    record = [float(reading.pixels[y].window_record) for y in ys]
    count = [float(reading.pixels[y].count) for y in ys]
    rec_width, _, _ = HEISENBERG.half_width(HEISENBERG.smooth(record), sines)
    cnt_width, _, _ = HEISENBERG.half_width(HEISENBERG.smooth(count), sines)
    rec_rms = HEISENBERG.rms(record, sines)
    cnt_rms = HEISENBERG.rms(count, sines)
    peak = max(ys, key=lambda y: reading.pixels[y].window_record)
    ratios = {
        y: reading.pixels[y].window_record / reading.pixels[y].incoherent
        for y in ys
        if reading.pixels[y].count >= MIN_COUNT and reading.pixels[y].incoherent > 0
    }
    clicks = sum(p.count for p in reading.pixels.values())
    lo, hi = reading.window
    intervals = max(1, hi - lo)
    return Analysis(
        clicks=clicks,
        cells=sum(p.cells for p in reading.pixels.values()),
        coincidences=sum(p.coincidences for p in reading.pixels.values()),
        coincident_clicks=sum(p.coincident_clicks for p in reading.pixels.values()),
        rays_per_pixel_interval=clicks / intervals / len(ys),
        record_width=rec_width,
        count_width=cnt_width,
        record_rms=rec_rms,
        count_rms=cnt_rms,
        narrowing=1.0 - rec_rms / cnt_rms if cnt_rms else math.nan,
        ratio_peak=ratios.get(peak, math.nan),
        # The lobe's centre (reported after the runs, not pinned): at the
        # lowest rate the record's peak is a pixel of coincidences, not
        # the lobe.
        ratio_centre=ratios.get(reading.centre, math.nan),
        ratio_min=min(ratios.values()) if ratios else math.nan,
        ratio_max=max(ratios.values()) if ratios else math.nan,
        peak=peak,
        cross=sum(p.window_record - p.incoherent for p in reading.pixels.values()),
    )


def fmt(value: float | None, digits: int = 3) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    return f"{value:.{digits}f}"


def print_table(readings: list[Reading]) -> tuple[int, int]:
    first = readings[0]
    print(
        f"{DETECTOR} lambda = c x period = {first.wavelength:.3f} Links; L = {first.distance} Links; "
        f"w = {first.width}; the screen spans sin theta in [{first.sine(0):.3f}, "
        f"{first.sine(len(first.pixels) - 1):.3f}]; the window [{first.window[0]}, the last tick] per run"
    )
    print(
        f"{DETECTOR} (the per-interval columns count the pixels' own clock: fixed detectors in no crowd at "
        "suspension 0, whose tick is their age, record 569; the clock audit of 2026-09-22) "
        "| world | rate (units per lamp per interval) | window | clicks | rays per pixel per interval "
        "| cells with a click | cells with 2+ rays (share) | clicks in such cells (share) "
        "| record FWHM (count FWHM) | w x record FWHM | record rms (count rms) | narrowing 1 - rms_R / rms_C "
        "| R / I at the peak pixel (at the centre pixel, reported) | R / I least .. greatest | cross term R - I | verdict |"
    )
    inside = outside = 0
    highest = max(r.rate for r in readings)
    lowest = min(r.rate for r in readings)
    for r in readings:
        a = analyse(r)
        verdicts = []
        if r.rate == lowest:
            ok_n = abs(a.narrowing) <= LOW_NARROWING
            ok_r = abs(a.ratio_peak - 1.0) <= LOW_RATIO
            verdicts.append(
                f"narrowing {'inside' if ok_n else 'outside'} (expected 0 +- {LOW_NARROWING})"
            )
            verdicts.append(f"R / I {'inside' if ok_r else 'outside'} (expected 1 +- {LOW_RATIO})")
            inside += ok_n + ok_r
            outside += (not ok_n) + (not ok_r)
        elif r.rate == highest:
            ok_n = a.narrowing >= HIGH_NARROWING
            verdicts.append(
                f"narrowing {'inside' if ok_n else 'outside'} (expected >= {HIGH_NARROWING})"
            )
            inside += ok_n
            outside += not ok_n
        else:
            verdicts.append("between (reported)")
        rec = f"{fmt(a.record_width)} ({fmt(a.count_width)})"
        product = "-" if a.record_width is None else f"{r.width * a.record_width:.2f}"
        share_cells = a.coincidences / a.cells if a.cells else math.nan
        share_clicks = a.coincident_clicks / a.clicks if a.clicks else math.nan
        print(
            f"{DETECTOR} | `{r.name}` | {r.rate} | [{r.window[0]}, {r.window[1] - 1}] | {a.clicks} "
            f"| {fmt(a.rays_per_pixel_interval, 3)} | {a.cells} | {a.coincidences} ({fmt(share_cells, 3)}) "
            f"| {a.coincident_clicks} ({fmt(share_clicks, 3)}) | {rec} | {product} "
            f"| {fmt(a.record_rms)} ({fmt(a.count_rms)}) | {fmt(a.narrowing)} | {fmt(a.ratio_peak)} at y = {a.peak} ({fmt(a.ratio_centre)}) "
            f"| {fmt(a.ratio_min)} .. {fmt(a.ratio_max)} | {a.cross} | {'; '.join(verdicts)} |"
        )
    return inside, outside


def print_profiles(readings: list[Reading]) -> None:
    for r in readings:
        a = analyse(r)
        lo, hi = max(0, a.peak - 12), min(len(r.pixels), a.peak + 13)
        line = ", ".join(
            f"{y}:{r.pixels[y].count}/{r.pixels[y].window_record / max(1, r.pixels[y].incoherent):.2f}"
            for y in range(lo, hi)
        )
        print(
            f"{DETECTOR} {r.name}: the count / R over I per pixel about the peak at y = {a.peak}: {line}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    parser.add_argument("--window-start", type=int, default=DEFAULT_WINDOW_START)
    parser.add_argument(
        "--profiles", action="store_true", help="print the count and R / I about the peak"
    )
    args = parser.parse_args(argv)
    readings = find_runs(args.root, window_start=args.window_start)
    if not readings:
        print(f"no A10 low-rate run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.name}: {label} ({r.ticks} ticks, {r.elapsed:.1f} s)")
            failed += not ok
    print()
    inside, outside = print_table(readings)
    if args.profiles:
        print()
        print_profiles(readings)
    print()
    print(f"{failed} record check(s) failed; {inside} reading(s) inside, {outside} outside, none moved")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
