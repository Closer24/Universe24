"""Two pages with a moving picture for the model owner (2026-09-21,
visualisation requested): `click.html`, one record of the registered
two-slit world `slits_low` from its birth to its click, and `bell.html`,
the pair of the registered Bell worlds `bell_0_8`, `bell_0_24`,
`bell_16_8` and `bell_16_24` from its birth to its two clicks, with the
correlations and the CHSH sum S of the register.

Nothing of the law is touched: the worlds are the registered files beside
this folder, run once by the runner (`run.json`, `events.jsonl`,
`state.json` under `--runs`) and stepped again in-process through the same
engine to read, at every interval, the rows of one record on the
GameBoard (a GAMEBOARD picture: the host's view, never a measurement) and
the record's offers in the apparatus's layer (`Layer.records`, the
pointers per Node and label and the cells' weights by the layer's own
`cells` and `rungs`). The gathers of the in-process replay are checked
against the runner's `run.json` before a page is written. Every number on
a page is read from the runner's files or from `expectations.json`, the
register of the series, and the page names its source.

    PYTHONPATH=src python examples/events/amplitude/pages/build_pages.py --runs artifacts/pages

Writes `click.html` and `bell.html` beside this file: each page carries
its GIF and the frames of its player inside the HTML (base64), so the
page is one file.
"""

from __future__ import annotations

import argparse
import base64
import colorsys
import io
import json
import math
import sys
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
WORLDS = HERE.parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.phase import phase_cosines, phase_sines  # noqa: E402
from event_universe.events.amplitude import AMPLITUDE_SCALE, Layer, LiveRecord, rungs  # noqa: E402
from event_universe.events.engine import NatureBeamSimulation  # noqa: E402
from event_universe.runner import run_initialization  # noqa: E402
from event_universe.world_loading import load_world  # noqa: E402

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
# A folder for a few frames as PNG (`--samples`), for the eye; none by default.
SAMPLES: Path | None = None


def font(name: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = FONT_DIR / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT = font("DejaVuSans.ttf", 11)
SMALL = font("DejaVuSans.ttf", 9)
BOLD = font("DejaVuSans-Bold.ttf", 11)
MONO = font("DejaVuSansMono.ttf", 10)

BG = (12, 10, 8)
GRID = (40, 34, 30)
INK = (240, 236, 230)
MUTED = (160, 150, 140)
DIM = (90, 84, 78)
YELLOW = (255, 210, 60)
CYAN = (80, 220, 255)
DARK_CYAN = (30, 70, 84)
MAGENTA = (255, 110, 200)
ORANGE = (255, 140, 40)
GREEN = (110, 220, 130)
RED = (220, 80, 70)
PURPLE = (170, 120, 255)
WALL = (120, 112, 104)

Node = tuple[int, int, int]


# -- the run and the replay ---------------------------------------------------


@dataclass
class Snapshot:
    """The host's view of one record at one interval."""

    tick: int
    rows: list[tuple[int, int, int, int, int]]  # (x, y, phase, amount, branch)
    others: list[tuple[int, int]]  # the Nodes of the other records' rows
    pointers: dict[str, dict[tuple[Node, int], tuple[int, int]]]  # set -> (Node, label) -> (X, Y)
    weights: list[tuple[str, int, int]]  # per cell (its name, numerator, multiplicity)
    ladder: list[int]
    total: tuple[int, int]
    live: bool
    events: list[dict[str, Any]]
    gathered_now: dict[str, Any] | None = None


@dataclass
class Trace:
    """One world run by the runner and replayed in-process for one record."""

    name: str
    world_path: Path
    run_dir: Path
    run: dict[str, Any]
    events: list[dict[str, Any]]
    identity: int
    snapshots: list[Snapshot] = field(default_factory=list)
    gathers_by_tick: dict[int, list[dict[str, Any]]] = field(default_factory=dict)
    directions: list[tuple[int, int, int]] = field(default_factory=list)
    shape: tuple[int, int, int] = (0, 0, 0)
    steps: int = 64


def shown_path(path: Path) -> str:
    """A path as the page names it: relative to the checkout when inside it."""
    resolved = path.resolve()
    return resolved.relative_to(ROOT).as_posix() if resolved.is_relative_to(ROOT) else str(resolved)


def run_world(name: str, runs: Path) -> tuple[dict[str, Any], list[dict[str, Any]], Path]:
    """The runner's files of the world `name` under `runs/<name>` (made if absent)."""
    world_path = WORLDS / f"{name}.json"
    run_dir = runs / name
    if not (run_dir / "run.json").exists():
        run_initialization(world_path, run_dir)
    run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    if run["status"] != "completed" or not run["conserved_at_every_completed_tick"]:
        raise ValueError(f"{name}: the run is not completed and conserved")
    with (run_dir / "events.jsonl").open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    return run, events, run_dir


def cell_name(factors: list[list[object]]) -> str:
    return " ".join(
        f"{name}{'' if channel == '0' else ' ' + str(channel)}" for name, _, channel in factors
    )


def replay(trace: Trace, family_name: str, ticks: list[int]) -> None:
    """Step the world in-process to the last tick asked, taking a snapshot
    of the record at every tick listed; the gathers of the replay must
    equal the runner's `world`."""
    document = trace.world_path.read_bytes()
    world = load_world(document, base_dir=trace.world_path.parent).world
    family = [f.name for f in world.families].index(family_name)
    events: list[dict[str, Any]] = []
    simulation = NatureBeamSimulation(world, observer=events.append)
    layer: Layer = simulation.layer
    trace.directions = [(int(d[0]), int(d[1]), int(d[2])) for d in world.directions]
    trace.shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    trace.steps = world.phase_steps
    wanted = set(ticks)
    last = max(ticks)
    for gather in trace.run["world"]:
        trace.gathers_by_tick.setdefault(int(gather["tick"]), []).append(gather)
    for tick in range(1, last + 1):
        start = len(events)
        simulation.step()
        if not simulation.books()["balanced"]:
            raise ValueError(f"{trace.name}: the books do not close at tick {tick}")
        if tick not in wanted:
            continue
        store = simulation.stores[family]
        mine = store.record == trace.identity
        x, y, _ = store.coordinates(store.node)
        rows = [
            (int(x[i]), int(y[i]), int(store.phase[i]), int(store.amount[i]), int(store.branch[i]))
            for i in np.flatnonzero(mine)
        ]
        others = sorted({(int(x[i]), int(y[i])) for i in np.flatnonzero(~mine)})
        live: LiveRecord | None = layer.records.get(trace.identity)
        pointers: dict[str, dict[tuple[Node, int], tuple[int, int]]] = {}
        weights: list[tuple[str, int, int]] = []
        ladder: list[int] = []
        total = (0, 1)
        if live is not None:
            for (set_index, _), offer in sorted(live.offers.items()):
                # The layer keeps phase-count vectors (the click without
                # amplitudes, 2026-09-21, BEAM_LAW note 37 (xii)); the
                # pointer is their evaluation, a report.
                pointers[layer.names[set_index]] = {
                    key: layer.evaluate(counts) for key, counts in offer.counts.items()
                }
            cells = layer.cells(live)
            weights = [
                (
                    cell_name(
                        [[layer.names[o.set_index], o.arm, o.channel_name(c)] for o, c in factors]
                    ),
                    numerator,
                    multiplicity,
                )
                for factors, numerator, multiplicity, _ in cells
            ]
            # The rungs on the record's wheel (N under [1, N]; note 46).
            ladder, total = rungs([(n, m) for _, n, m in weights], live.wheel)
        gathered = [
            e for e in events[start:] if e["event"] == "gather" and e["record"] == trace.identity
        ]
        trace.snapshots.append(
            Snapshot(
                tick,
                rows,
                others,
                pointers,
                weights,
                ladder,
                total,
                live is not None,
                [e for e in events[start:] if concerns(e, trace.identity)],
                gathered[0] if gathered else None,
            )
        )
    replayed = [e for e in events if e["event"] == "gather"]
    expected = [g for g in trace.run["world"] if int(g["tick"]) <= last]
    if replayed != expected:
        raise ValueError(f"{trace.name}: the replay's gathers differ from run.json's world")


def offers_from_ends(
    ends: list[dict[str, Any]], upto: int, steps: int
) -> dict[str, dict[tuple[Node, int], tuple[int, int]]]:
    """A record's pointers per set from its `click` lines up to a tick, by the
    layer's formula: 32 x amount x (C[phase], S[phase]) per end Node and label,
    the tables C and S at the scale 256 (checked against the layer's own
    pointers while the record lives)."""
    cosines, sines = phase_cosines(steps), phase_sines(steps)
    found: dict[str, dict[tuple[Node, int], tuple[int, int]]] = {}
    for e in ends:
        if int(e["tick"]) > upto:
            continue
        set_name = str(e.get("detector") or e.get("face") or f"measured:{e['measured']}")
        node = (int(e["node"][0]), int(e["node"][1]), int(e["node"][2]))
        label = int(e["branch"]) & 0xFFFFFFFF
        X, Y = found.setdefault(set_name, {}).get((node, label), (0, 0))
        weight = AMPLITUDE_SCALE * int(e["amount"])
        # The phase the layer reads at an end: the exact phase at the row's
        # last Link where the click line carries it (note 45), else the walk's.
        phase = int(e.get("exact", e["phase"]))
        found[set_name][(node, label)] = (X + weight * cosines[phase], Y + weight * sines[phase])
    return found


def concerns(line: dict[str, Any], identity: int) -> bool:
    if line.get("record") == identity:
        return True
    return any(isinstance(r, list) and r and r[0] == identity for r in line.get("rows", []))


# -- drawing ----------------------------------------------------------------------


def hue(phase: int, steps: int, value: float) -> tuple[int, int, int]:
    r, g, b = colorsys.hsv_to_rgb(phase / steps, 0.9, value)
    return int(r * 255), int(g * 255), int(b * 255)


def arrow(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    dx: float,
    dy: float,
    colour: tuple[int, int, int],
    width: int = 2,
) -> None:
    ex, ey = cx + dx, cy - dy
    draw.line([(cx, cy), (ex, ey)], fill=colour, width=width)
    length = math.hypot(dx, dy)
    if length > 6:
        ux, uy = dx / length, -dy / length
        for sign in (1, -1):
            px = ex - 7 * ux + sign * 3.5 * uy
            py = ey - 7 * uy - sign * 3.5 * ux
            draw.line([(ex, ey), (px, py)], fill=colour, width=width)


def phase_plane(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    radius: int,
    vectors: list[tuple[float, float, tuple[int, int, int]]],
    scale: float,
) -> None:
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=DIM)
    draw.line([(cx - radius, cy), (cx + radius, cy)], fill=GRID)
    draw.line([(cx, cy - radius), (cx, cy + radius)], fill=GRID)
    for vx, vy, colour in vectors:
        arrow(draw, cx, cy, vx * scale * radius, vy * scale * radius, colour)


def ladder_bar(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    height: int,
    steps: int,
    cells: list[tuple[str, int, tuple[int, int, int]]],
    u: int,
    chosen: str | None,
) -> None:
    """The ladder 0 .. N top to bottom: per cell (its name, its rung, its
    colour), the mark of u and the chosen cell outlined."""
    draw.rectangle([x0, y0, x0 + 22, y0 + height], outline=MUTED)
    previous = 0
    for name, rung, colour in cells:
        if rung > previous:
            a = y0 + height * previous / steps
            b = y0 + height * rung / steps
            draw.rectangle([x0 + 1, a, x0 + 21, b], fill=colour)
            if chosen is not None and name == chosen:
                draw.rectangle([x0 - 2, a - 1, x0 + 24, b + 1], outline=ORANGE, width=2)
        previous = rung
    uy = y0 + height * (u + 0.5) / steps
    draw.polygon([(x0 - 4, uy), (x0 - 12, uy - 5), (x0 - 12, uy + 5)], fill=ORANGE)


def quantized(frames: list[Image.Image], colours: int) -> list[Image.Image]:
    palette = frames[len(frames) // 2].quantize(colors=colours, method=Image.Quantize.MEDIANCUT)
    return [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]


def gif_bytes(frames: list[Image.Image], durations: list[int]) -> bytes:
    small = quantized(frames, 128)
    buffer = io.BytesIO()
    small[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=small[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    return buffer.getvalue()


def sheet_bytes(frames: list[Image.Image], columns: int) -> bytes:
    w, h = frames[0].size
    rows = math.ceil(len(frames) / columns)
    sheet = Image.new("RGB", (columns * w, rows * h), BG)
    for k, frame in enumerate(frames):
        sheet.paste(frame, ((k % columns) * w, (k // columns) * h))
    buffer = io.BytesIO()
    sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(
        buffer, format="PNG", optimize=True
    )
    return buffer.getvalue()


def save_samples(name: str, frames: list[Image.Image], indices: list[int]) -> None:
    if SAMPLES is None:
        return
    SAMPLES.mkdir(parents=True, exist_ok=True)
    for k in indices:
        frames[k].save(SAMPLES / f"{name}_{k:03d}.png")


def data_uri(kind: str, payload: bytes) -> str:
    return f"data:{kind};base64,{base64.b64encode(payload).decode('ascii')}"


# -- page 1: the click ---------------------------------------------------------


def kind_of(name: str) -> str:
    if name.startswith("screen_"):
        return "screen"
    if name.startswith("face:"):
        return "face"
    return "wall"


KIND_COLOUR = {"screen": CYAN, "face": PURPLE, "wall": WALL}


def click_frame_ticks(events: list[dict[str, Any]], identity: int) -> list[int]:
    """Every interval from the birth through the split, every fourth
    across the fan's flight, every second from the first end at the screen
    to the gather, and two after it."""
    mine = [e for e in events if concerns(e, identity)]
    born = next(e["tick"] for e in mine if e["event"] == "birth")
    split = max(e["tick"] for e in mine if e["event"] == "split")
    first_screen = min(
        e["tick"]
        for e in mine
        if e["event"] == "click" and str(e.get("detector", "")).startswith("screen")
    )
    gather = next(e["tick"] for e in mine if e["event"] == "gather")
    ticks = list(range(born, split + 2))
    ticks += list(range(split + 2, first_screen - 1, 4))
    ticks += list(range(first_screen - 1, gather + 1, 2))
    ticks += [gather, gather + 1, gather + 2]
    return sorted(set(ticks))


def draw_click(trace: Trace, snap: Snapshot, context: dict[str, Any]) -> Image.Image:
    W, H = 600, 430
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    nx, ny, _ = trace.shape
    S, BX, BY = 3, 14, 36
    steps = trace.steps

    def px(x: int) -> int:
        return BX + x * S

    def py(y: int) -> int:
        return BY + (ny - 1 - y) * S

    # The GameBoard: the faces, the wall, the openings, the absorbers, the screen, the lamp.
    draw.rectangle([BX - 1, BY - 1, BX + nx * S, BY + ny * S], outline=GRID)
    for y in range(0, ny, 2):
        draw.point((BX - 3, py(y) + 1), fill=PURPLE)
        draw.point((BX + nx * S + 2, py(y) + 1), fill=DIM)
    for x, y, kind in context["things"]:
        colour = {"wall": WALL, "opening": GREEN, "absorber": INK, "screen": DARK_CYAN}[kind]
        draw.rectangle([px(x), py(y), px(x) + S - 1, py(y) + S - 1], fill=colour)
    lx, ly = context["lamp"]
    cx, cy = px(lx) + 1, py(ly) + 1
    draw.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=YELLOW)
    # The record's rows: per Node the coherent sum of its rows, the hue the phase, the
    # brightness the magnitude (a log scale from 1 unit to the largest seen).
    by_node: dict[tuple[int, int], tuple[float, float]] = {}
    for x, y, phase, amount, _ in snap.rows:
        angle = 2 * math.pi * phase / steps
        vx, vy = by_node.get((x, y), (0.0, 0.0))
        by_node[(x, y)] = (vx + amount * math.cos(angle), vy + amount * math.sin(angle))
    largest = context["largest"]
    for (x, y), (vx, vy) in by_node.items():
        magnitude = math.hypot(vx, vy)
        if magnitude < 1e-9:
            continue
        phase = int(round(math.atan2(vy, vx) / (2 * math.pi) * steps)) % steps
        value = 0.5 + 0.5 * math.log1p(magnitude) / math.log1p(largest)
        draw.rectangle([px(x) - 1, py(y) - 1, px(x) + S, py(y) + S], fill=hue(phase, steps, value))
    if snap.gathered_now is not None or (not snap.live and snap.tick > context["gather_tick"]):
        gx, gy = context["click_node"][0], context["click_node"][1]
        draw.ellipse([px(gx) - 8, py(gy) - 8, px(gx) + S + 8, py(gy) + S + 8], outline=ORANGE, width=2)
    # The screen's weights beside the screen (the Gram form per pixel, coherent within the Node).
    x0 = BX + nx * S + 12
    draw.text((x0, 22), "the screen's weights", fill=MUTED, font=SMALL)
    screen_weights = context["screen_weights"](snap)
    wmax = context["weight_max"]
    erased = not snap.live and snap.tick > context["gather_tick"]
    for y, w in screen_weights.items():
        length = int(64 * math.sqrt(w / wmax)) if wmax else 0
        clicked = (snap.gathered_now is not None or erased) and y == context["click_node"][1]
        colour = ORANGE if clicked else GRID if erased else CYAN
        draw.rectangle([x0, py(y), x0 + max(length, 1), py(y) + S - 1], fill=colour)
    if erased:
        draw.text((x0, BY + 4), "erased", fill=DIM, font=SMALL)
    # The pointer of the pixel that will click.
    cx, cy = 352, 100
    X, Y = context["pointer"](snap)
    pmax = context["pointer_max"]
    phase_plane(draw, cx, cy, 40, [(X / pmax, Y / pmax, ORANGE)] if pmax and (X or Y) else [], 1.0)
    draw.text((cx - 48, cy + 46), f"X {X}", fill=INK, font=MONO)
    draw.text((cx - 48, cy + 58), f"Y {Y}", fill=INK, font=MONO)
    draw.text((cx - 48, cy + 72), "the offer's pointer (X, Y)", fill=MUTED, font=SMALL)
    draw.text((cx - 48, cy + 84), f"at the pixel y = {context['click_node'][1]}", fill=MUTED, font=SMALL)
    # The ladder so far.
    lx0, ly0, lh = 452, 44, 250
    draw.text((lx0 - 24, 22), "the ladder so far, 0 .. 64", fill=MUTED, font=SMALL)
    cells = [
        (name, rung, KIND_COLOUR[kind_of(name.split()[0])])
        for (name, _, _), rung in zip(snap.weights, snap.ladder, strict=True)
    ]
    chosen = context["click_cell"] if not snap.live else None
    if not snap.live:
        cells = context["final_cells"]
    ladder_bar(draw, lx0, ly0, lh, steps, cells, context["u"], chosen)
    draw.text((lx0 + 30, ly0 - 4), "0", fill=MUTED, font=SMALL)
    draw.text((lx0 + 30, ly0 + lh - 6), "64", fill=MUTED, font=SMALL)
    draw.text(
        (lx0 + 30, ly0 + lh * (context["u"] + 0.5) / steps - 6),
        f"u = {context['u']}",
        fill=ORANGE,
        font=SMALL,
    )
    shares = Counter()
    previous = 0
    for name, rung, _ in cells:
        shares[kind_of(name.split()[0])] += max(rung - previous, 0)
        previous = rung
    for k, (kind, label) in enumerate((("wall", "wall"), ("screen", "screen"), ("face", "faces"))):
        draw.rectangle(
            [lx0 + 30, ly0 + 40 + 14 * k, lx0 + 38, ly0 + 48 + 14 * k], fill=KIND_COLOUR[kind]
        )
        draw.text(
            (lx0 + 42, ly0 + 38 + 14 * k), f"{label} {shares.get(kind, 0)}", fill=MUTED, font=SMALL
        )
    # The header and the notes.
    draw.text((12, 5), context["title"](snap), fill=INK, font=FONT)
    for k, line in enumerate(context["notes"](snap)[:7]):
        colour = ORANGE if line.startswith(("THE CLICK", "DELETED")) else MUTED
        draw.text((286, 300 + 15 * k), line, fill=colour, font=SMALL)
    # The legend.
    legend = [
        (YELLOW, "lamp"),
        (WALL, "wall"),
        (GREEN, "opening"),
        (INK, "absorber"),
        (DARK_CYAN, "screen"),
        (PURPLE, "open face y"),
    ]
    for k, (colour, label) in enumerate(legend):
        lx = 12 + k * 60
        draw.rectangle([lx, H - 16, lx + 8, H - 8], fill=colour)
        draw.text((lx + 12, H - 19), label, fill=MUTED, font=SMALL)
    return image


def build_click(runs: Path, out: Path) -> dict[str, Any]:
    name = "slits_low"
    run, events, run_dir = run_world(name, runs)
    document = json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))
    lamp = next(m for m in document["measured"] if "lamp" in m)
    lamp_xy = (lamp["position"][0], lamp["position"][1])
    # The record shown: among the first 64 births, the one whose click is the screen
    # pixel at the lamp's own y (the centre of the pattern).
    target = f"screen_{lamp_xy[1]}"
    gather = next(
        g
        for g in run["world"]
        if g["chosen"] and g["chosen"][0][0] == target and int(g["record"]) - (1 << 32) <= 64
    )
    identity = int(gather["record"])
    trace = Trace(name, WORLDS / f"{name}.json", run_dir, run, events, identity)
    ticks = click_frame_ticks(events, identity)
    replay(trace, "light", ticks)
    mine = [e for e in events if concerns(e, identity)]
    birth = next(e for e in mine if e["event"] == "birth")
    splits = [e for e in mine if e["event"] == "split"]
    ends = [e for e in mine if e["event"] == "click"]
    gather_tick = int(gather["tick"])
    click_node = tuple(gather["node"][0])
    click_cell = cell_name(gather["chosen"])
    u = int(gather["u"])
    # The things on the GameBoard, by the world file: the wall's x is the first wall
    # entry's, the screen's x the first detector's; an opening carries a table.
    screen_x = document["detectors"][0]["positions"][0][0]
    wall_x = next(m["position"][0] for m in document["measured"] if m["family"] == "wall")
    things: list[tuple[int, int, str]] = []
    for m in document["measured"]:
        if m["family"] != "wall":
            continue
        x, y = m["position"][0], m["position"][1]
        kind = (
            "opening"
            if "table" in m
            else "screen"
            if x == screen_x
            else "wall"
            if x == wall_x
            else "absorber"
        )
        things.append((x, y, kind))

    def offers_from_events(upto: int) -> dict[str, dict[tuple[Node, int], tuple[int, int]]]:
        return offers_from_ends(ends, upto, trace.steps)

    for snap in trace.snapshots:
        if snap.live:
            expected = offers_from_events(snap.tick)
            if any(snap.pointers.get(k) != v for k, v in expected.items() if not k.startswith("face")):
                raise ValueError(
                    f"{name}: the pointers read from the events differ from the layer's at tick {snap.tick}"
                )
    final_offers = offers_from_events(gather_tick)

    def pointers_at(snap: Snapshot) -> dict[str, dict[tuple[Node, int], tuple[int, int]]]:
        return snap.pointers if snap.live else final_offers

    def screen_weights(snap: Snapshot) -> dict[int, int]:
        found: dict[int, int] = {}
        for set_name, pointers in pointers_at(snap).items():
            if kind_of(set_name) != "screen":
                continue
            for (node, _), (X, Y) in pointers.items():
                found[node[1]] = found.get(node[1], 0) + X * X + Y * Y
        return found

    def pointer(snap: Snapshot) -> tuple[int, int]:
        X = Y = 0
        for (node, _), (px_, py_) in pointers_at(snap).get(target, {}).items():
            if node == click_node:
                X, Y = X + px_, Y + py_
        return X, Y

    final_weights = {y: w for y, w in screen_weights(trace.snapshots[-1]).items()}
    weight_max = max(final_weights.values()) if final_weights else 1
    pX, pY = pointer(trace.snapshots[-1])
    pointer_max = math.hypot(pX, pY) or 1.0
    largest = 1.0
    for s in trace.snapshots:
        by_node: dict[tuple[int, int], tuple[float, float]] = {}
        for x, y, phase, amount, _ in s.rows:
            angle = 2 * math.pi * phase / trace.steps
            vx, vy = by_node.get((x, y), (0.0, 0.0))
            by_node[(x, y)] = (vx + amount * math.cos(angle), vy + amount * math.sin(angle))
        largest = max([largest, *(math.hypot(*v) for v in by_node.values())])
    final_cells = [
        (cell_name(factors), rung, KIND_COLOUR[kind_of(factors[0][0])])
        for factors, rung in gather["cells"]
    ]
    end_ticks = Counter(int(e["tick"]) for e in ends)
    wall_ticks = sorted(
        {
            int(e["tick"])
            for e in ends
            if kind_of(str(e.get("detector") or f"measured:{e['measured']}")) == "wall"
        }
    )
    first_screen = min(int(e["tick"]) for e in ends if str(e.get("detector", "")).startswith("screen"))
    split_tick = max(int(e["tick"]) for e in splits)
    split_units = sum(int(e["born"]) for e in splits)
    offers_count = sum(len(p) for p in final_offers.values())
    total_units = sum(int(e["amount"]) for e in ends)
    rung_before = 0
    for factors, rung in gather["cells"]:
        if cell_name(factors) == click_cell:
            break
        rung_before = int(rung)

    def title(snap: Snapshot) -> str:
        return f"{name} - interval {snap.tick} of {document['ticks']} - the record born at tick {birth['tick']} with u = {u} (GAMEBOARD picture)"

    def notes(snap: Snapshot) -> list[str]:
        t = snap.tick
        lines: list[str] = []
        if t == birth["tick"]:
            lines.append(
                f"born at the lamp: {birth['units']} rows of amount 1, multiplicity {birth['multiplicity']}"
            )
        elif t < wall_ticks[0]:
            lines.append("the rows fly toward the wall; the hue is the phase")
        if t in wall_ticks:
            lines.append(f"{end_ticks[t]} row(s) end at the absorbers: offers at the wall")
        if t == split_tick:
            lines.append(f"the split at the two openings: {split_units} units born into the fan")
        if split_tick < t < first_screen:
            lines.append("the fan spreads behind the wall; every row keeps its phase")
        if first_screen <= t < gather_tick and t in end_ticks:
            lines.append(f"{end_ticks[t]} rows end at the screen or a face: the pointers grow")
        if snap.gathered_now is not None:
            lines.append(f"THE CLICK at tick {t}: the last row ended; the ladder is complete")
            lines.append(
                f"u = {u} falls in {click_cell}: the click at ({click_node[0]}, {click_node[1]})"
            )
            lines.append(f"the cell's weight / the total = {weight_share(gather)[0]}")
            lines.append(f"({weight_share(gather)[1]} in the unit 2^58)")
        if not snap.live and t > gather_tick:
            lines.append(f"DELETED: the {offers_count} offers of the record are gone")
            lines.append(f"({total_units} units ended at {len(final_offers)} sets);")
            lines.append(f"the world kept one bit: {click_cell}, content {gather['content']}")
        return lines

    context = {
        "things": things,
        "lamp": lamp_xy,
        "largest": max(largest, 1.0),
        "gather_tick": gather_tick,
        "click_node": click_node,
        "click_cell": click_cell,
        "screen_weights": screen_weights,
        "weight_max": weight_max,
        "pointer": pointer,
        "pointer_max": pointer_max,
        "u": u,
        "final_cells": final_cells,
        "title": title,
        "notes": notes,
    }
    frames = [draw_click(trace, snap, context) for snap in trace.snapshots]
    marks = [0, 9, 14, 24, 33, 36, 40, len(frames) - 3, len(frames) - 1]
    save_samples("click", frames, sorted({k for k in marks if 0 <= k < len(frames)}))
    durations = [
        900 if (s.gathered_now is not None or s.tick in (birth["tick"], split_tick)) else 260
        for s in trace.snapshots
    ]
    durations[-1] = 1600
    ticks_list = [s.tick for s in trace.snapshots]
    readings = {
        "world": name,
        "run_dir": shown_path(run_dir),
        "fingerprint": run["source_sha256"],
        "elapsed": run["elapsed_seconds"],
        "ticks": document["ticks"],
        "identity": identity,
        "u": u,
        "born": int(birth["tick"]),
        "units": int(birth["units"]),
        "multiplicity": int(birth["multiplicity"]),
        "wall_ticks": wall_ticks,
        "split_tick": split_tick,
        "split_units": split_units,
        "first_screen": first_screen,
        "gather_tick": gather_tick,
        "click_node": list(click_node),
        "click_cell": click_cell,
        "weight": gather["weight"],
        "total": gather["total"],
        "unit": gather["unit"],
        "cells": len(gather["cells"]),
        "rung_before": rung_before,
        "rung": next(c[1] for c in gather["cells"] if cell_name(c[0]) == click_cell),
        "content": gather["content"],
        "offers": offers_count,
        "sets": len(final_offers),
        "ended": total_units,
        "pointer": [pX, pY],
        "frames": len(frames),
        "rung_shares": rung_shares(gather),
    }
    write_click_page(out, frames, durations, ticks_list, readings, document)
    return readings


def weight_share(gather: dict[str, Any]) -> tuple[str, str]:
    w = Fraction(int(gather["weight"][0]), int(gather["weight"][1]))
    t = Fraction(int(gather["total"][0]), int(gather["total"][1]))
    return f"{float(w / t):.4f}", f"{float(w / gather['unit']):.4f} of {float(t / gather['unit']):.4f}"


def rung_shares(gather: dict[str, Any]) -> dict[str, int]:
    shares: Counter[str] = Counter()
    previous = 0
    for factors, rung in gather["cells"]:
        shares[kind_of(factors[0][0])] += max(int(rung) - previous, 0)
        previous = int(rung)
    return dict(shares)


# -- page 2: the pair ---------------------------------------------------------------


BELL = ("bell_0_8", "bell_0_24", "bell_16_8", "bell_16_24")


def draw_bell(traces: list[Trace], k: int, context: dict[str, Any]) -> Image.Image:
    W, H = 600, 470
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    tick = context["ticks"][k]
    draw.text(
        (12, 8),
        f"the pair on the bar of 21 - interval {tick} of 80 - the record born at tick 1 with u = 0 in orange, the later records grey",
        fill=INK,
        font=SMALL,
    )
    S, BX = 17, 16
    for j, trace in enumerate(traces):
        snap = trace.snapshots[k]
        y0 = 30 + j * 108
        settings = context["settings"][trace.name]
        draw.text(
            (BX, y0),
            f"{trace.name}: Alice's setting a = {settings[0]} at x = 7, Bob's b = {settings[1]} at x = 17",
            fill=INK,
            font=BOLD,
        )
        by = y0 + 28
        for x in range(trace.shape[0]):
            draw.rectangle([BX + x * S, by, BX + x * S + S - 2, by + S - 2], outline=GRID)
        for x, colour, label in context["things"]:
            draw.rectangle([BX + x * S + 3, by + 3, BX + x * S + S - 5, by + S - 5], fill=colour)
            draw.text((BX + x * S - 2, by + S + 1), label, fill=colour, font=SMALL)
        for x, _ in snap.others:
            draw.ellipse([BX + x * S + 6, by + 6, BX + x * S + 10, by + 10], fill=DIM)
        by_node = Counter((x, phase) for x, _, phase, _, _ in snap.rows)
        for (x, phase), count in by_node.items():
            cx, cy = BX + x * S + S // 2 - 1, by + S // 2 - 1
            draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=ORANGE)
            angle = 2 * math.pi * phase / trace.steps
            arrow(draw, cx, cy, 12 * math.cos(angle), 12 * math.sin(angle), INK, 1)
            draw.text((cx - 10, by - 13), f"{count} rows", fill=ORANGE, font=SMALL)
        # The offers: the pointer read at each side, one vector.
        final = context["final_pointers"][trace.name] if snap.gathered_now is not None else {}
        for side, (set_name, sx) in enumerate((("alice_plus", 396), ("bob_plus", 440))):
            pointers = snap.pointers.get(set_name, {}) or final.get(set_name, {})
            vectors = []
            for (_, _label), (X, Y) in pointers.items():
                norm = math.hypot(X, Y) or 1.0
                vectors.append((X / norm, Y / norm, ORANGE))
            phase_plane(draw, sx, y0 + 46, 14, vectors, 0.9)
            draw.text(
                (sx - 14, y0 + 62),
                "A" if side == 0 else "B",
                fill=CYAN if side == 0 else MAGENTA,
                font=SMALL,
            )
            if pointers:
                draw.text((sx - 14, y0 + 72), f"{len(pointers)} labels", fill=MUTED, font=SMALL)
        # The cells of the record: the four joint weights and the rungs, or the ladder of
        # the record gathered at this interval.
        gathered = [g for g in trace.gathers_by_tick.get(tick, []) if int(g["record"]) - (1 << 32) <= 64]
        shown = snap.gathered_now or (gathered[0] if gathered else None)
        x0 = 470
        if shown is not None:
            previous = 0
            for c, (factors, rung) in enumerate(shown["cells"]):
                label = "".join(str(f[2]) for f in factors)
                width = max(rung - previous, 0)
                colour = ORANGE if cell_name(factors) == cell_name(shown["chosen"]) else DIM
                draw.rectangle([x0, y0 + 22 + c * 15, x0 + 2 * width, y0 + 34 + c * 15], fill=colour)
                draw.text(
                    (x0 + 70, y0 + 21 + c * 15),
                    f"{label} {width}",
                    fill=colour if colour == ORANGE else MUTED,
                    font=SMALL,
                )
                previous = rung
            draw.text(
                (x0, y0 + 84),
                f"u = {shown['u']}: {''.join(str(f[2]) for f in shown['chosen'])}",
                fill=ORANGE,
                font=SMALL,
            )
        elif snap.weights:
            draw.text((x0, y0 + 30), "the cells wait for", fill=MUTED, font=SMALL)
            draw.text((x0, y0 + 42), "the second arm", fill=MUTED, font=SMALL)
        else:
            draw.text((x0, y0 + 30), "no offer yet", fill=MUTED, font=SMALL)
        counts = context["counts"](trace, tick)
        draw.text(
            (BX, by + S + 14),
            "clicks so far (DETECTOR, u = 0 .. 63): "
            + "  ".join(f"{key} {counts[key]}" for key in ("++", "+-", "-+", "--"))
            + f"   E x 64 = {counts['E']}",
            fill=MUTED,
            font=SMALL,
        )
        if snap.gathered_now is not None:
            draw.text(
                (BX, by + S + 26),
                "THE TWO CLICKS: one cell of the record, both Nodes, the same interval",
                fill=ORANGE,
                font=SMALL,
            )
    draw.text(
        (12, H - 14),
        "orange: the one record (its rows and its pointer at each side); the arrow on a row is its phase; A, B: the pointer (X, Y) read at Alice's and at Bob's counter",
        fill=MUTED,
        font=SMALL,
    )
    return image


def bell_counts(trace: Trace, upto: int) -> dict[str, int]:
    counts = {"++": 0, "+-": 0, "-+": 0, "--": 0}
    for g in trace.run["world"]:
        if int(g["tick"]) <= upto and int(g["record"]) - (1 << 32) <= 64 and g["chosen"]:
            counts["".join(str(f[2]) for f in g["chosen"])] += 1
    counts["E"] = counts["++"] + counts["--"] - counts["+-"] - counts["-+"]
    return counts


def build_bell(runs: Path, out: Path) -> dict[str, Any]:
    traces: list[Trace] = []
    identity = (1 << 32) + 1
    ticks: list[int] = []
    for name in BELL:
        run, events, run_dir = run_world(name, runs)
        trace = Trace(name, WORLDS / f"{name}.json", run_dir, run, events, identity)
        if not ticks:
            gather = next(g for g in run["world"] if int(g["record"]) == identity)
            last = max(int(g["tick"]) for g in run["world"] if int(g["record"]) - (1 << 32) <= 64)
            ticks = (
                list(range(1, int(gather["tick"]) + 4))
                + list(range(int(gather["tick"]) + 4, last, 4))
                + [last]
            )
        replay(trace, "light", ticks)
        traces.append(trace)
    document = json.loads((WORLDS / f"{BELL[0]}.json").read_text(encoding="utf-8"))
    settings = {}
    for name in BELL:
        d = json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))
        windows = {
            tuple(m["position"]): m["table"]["light"]["phase_window"]
            for m in d["measured"]
            if "table" in m and "light" in m["table"] and isinstance(m["table"]["light"], dict)
        }
        settings[name] = (windows[(7, 0, 0)], windows[(17, 0, 0)])
    things = [
        (10, YELLOW, "lamp"),
        (7, CYAN, "A+"),
        (4, DARK_CYAN, "A-"),
        (17, MAGENTA, "B+"),
        (18, (90, 40, 70), "B-"),
    ]
    final_pointers = {
        t.name: offers_from_ends(
            [e for e in t.events if e["event"] == "click" and e.get("record") == identity],
            10**9,
            t.steps,
        )
        for t in traces
    }
    context = {
        "ticks": ticks,
        "settings": settings,
        "things": things,
        "counts": bell_counts,
        "final_pointers": final_pointers,
    }
    frames = [draw_bell(traces, k, context) for k in range(len(ticks))]
    save_samples("bell", frames, [0, 5, 12, 14, len(frames) - 1])
    first = traces[0]
    gather_tick = int(next(g for g in first.run["world"] if int(g["record"]) == identity)["tick"])
    durations = [900 if t in (1, gather_tick) else 300 for t in ticks]
    durations[-1] = 1600
    # The register and the runs: the counts, E and S.
    expectations = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))["pair"]
    register = {key: dict(value["counts"], E=value["E"]) for key, value in expectations["chsh"].items()}
    measured = {
        name[len("bell_") :]: bell_counts(t, 10**9) for name, t in zip(BELL, traces, strict=True)
    }
    for key, counts in measured.items():
        expected = register[key]
        if (
            any(counts[c] != expected.get(c, 0) for c in ("++", "+-", "-+", "--"))
            or counts["E"] != expected["E"]
        ):
            raise ValueError(f"the run's counts of bell_{key} differ from the register")
    S64 = register["0_8"]["E"] - register["0_24"]["E"] + register["16_8"]["E"] + register["16_24"]["E"]
    if S64 != expectations["chsh_S"]:
        raise ValueError("the CHSH sum differs from the register's chsh_S")
    birth = next(e for e in first.events if e["event"] == "birth" and e["record"] == identity)
    ends = [e for e in first.events if e["event"] == "click" and e.get("record") == identity]
    gather = next(g for g in first.run["world"] if int(g["record"]) == identity)
    readings = {
        "worlds": list(BELL),
        "run_dirs": {t.name: shown_path(t.run_dir) for t in traces},
        "fingerprint": first.run["source_sha256"],
        "elapsed": {t.name: t.run["elapsed_seconds"] for t in traces},
        "identity": identity,
        "birth": birth,
        "ends": [
            (
                int(e["tick"]),
                e["detector"],
                list(e["node"]),
                int(e["branch"]) >> 32,
                int(e["branch"]) & 0xFFFFFFFF,
                int(e["age"]),
            )
            for e in ends
        ],
        "gather": gather,
        "settings": settings,
        "register": register,
        "measured": measured,
        "S64": S64,
        "S": Fraction(S64, 64),
        "n1024": expectations,
        "frames": len(frames),
        "shape": document["shape"],
        "branches": document["measured"][0]["lamp"]["branches"],
        "arms": document["measured"][0]["lamp"]["arms"],
    }
    write_bell_page(out, frames, durations, ticks, readings)
    return readings


# -- the pages -----------------------------------------------------------------------


STYLE = """
  :root {
    --ground: #f6f2ec; --panel: #fbf9f5; --ink: #221b17; --muted: #6e635b; --line: #dcd3c9;
    --accent: #c4511c; --accent-ink: #ffffff;
    --display: "Fraunces", Georgia, "Times New Roman", serif;
    --body: "Source Sans 3", "Segoe UI", Helvetica, Arial, sans-serif;
    --mono: "JetBrains Mono", "SFMono-Regular", Menlo, Consolas, monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --ground: #17110e; --panel: #211a16; --ink: #f1e8df; --muted: #a89a8e; --line: #3a2f28;
      --accent: #f08a3c; --accent-ink: #1a110b;
    }
  }
  :root[data-theme="dark"] {
    --ground: #17110e; --panel: #211a16; --ink: #f1e8df; --muted: #a89a8e; --line: #3a2f28;
    --accent: #f08a3c; --accent-ink: #1a110b;
  }
  body { background: var(--ground); color: var(--ink); font-family: var(--body); font-size: 17px;
    line-height: 1.5; margin: 0; padding-inline: 16px; padding-block: 32px 64px; }
  main { max-width: 880px; margin: 0 auto; display: grid; gap: 36px; }
  header { display: grid; gap: 10px; }
  .eyebrow { font-family: var(--mono); font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); }
  h1 { font-family: var(--display); font-weight: 700; font-size: clamp(30px, 5vw, 44px); line-height: 1.1; margin: 0; text-wrap: balance; }
  h2 { font-family: var(--display); font-weight: 500; font-size: 24px; margin: 0 0 12px; text-wrap: balance; }
  p { margin: 0; max-width: 70ch; }
  .lede { font-size: 19px; color: var(--muted); }
  figure { margin: 0; display: grid; gap: 10px; }
  figcaption { font-size: 14px; color: var(--muted); max-width: 80ch; }
  .player canvas { width: 100%; max-width: 600px; height: auto; display: block; border: 1px solid var(--line); background: #000; image-rendering: pixelated; }
  .player .controls { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; font-family: var(--mono); font-size: 13px; }
  .player .controls button { font: inherit; padding: 4px 12px; border: 1px solid var(--line); background: var(--panel); color: var(--ink); border-radius: 4px; cursor: pointer; }
  .player .controls input[type="range"] { flex: 1 1 200px; accent-color: var(--accent); }
  .pair { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
  .reading { background: var(--panel); border: 1px solid var(--line); padding: 16px 18px; display: grid; gap: 6px; }
  .reading .label { font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
  .reading .value { font-family: var(--display); font-size: 28px; font-weight: 500; line-height: 1.1; color: var(--accent); }
  .reading .note { font-size: 15px; color: var(--muted); }
  .kind { font-family: var(--mono); font-size: 11px; border: 1px solid var(--line); padding: 1px 6px; border-radius: 3px; margin-left: 6px; }
  .tablewrap { overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; font-size: 15px; font-variant-numeric: tabular-nums; }
  th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
  td.num { font-family: var(--mono); white-space: nowrap; }
  section { display: grid; gap: 14px; }
  ul { margin: 0; padding-left: 22px; max-width: 70ch; }
  li { margin-bottom: 4px; }
  .fine { font-size: 14px; color: var(--muted); }
  code { font-family: var(--mono); font-size: 0.92em; }
  .moments { display: grid; gap: 8px; }
  .moment { display: grid; grid-template-columns: 110px 1fr; gap: 10px; }
  .moment b { font-family: var(--mono); font-size: 13px; color: var(--accent); letter-spacing: 0.06em; text-transform: uppercase; padding-top: 3px; }
"""


def player(
    frames: list[Image.Image],
    durations: list[int],
    ticks: list[int],
    name: str,
    caption: str,
    gif: bytes,
) -> str:
    columns = 8
    w, h = frames[0].size
    sheet = data_uri("image/png", sheet_bytes(frames, columns))
    gif_uri = data_uri("image/gif", gif)
    return f"""<figure class="player" id="player-{name}">
    <canvas width="{w}" height="{h}" aria-label="the moving picture, played frame by frame"></canvas>
    <div class="controls">
      <button type="button" class="play" aria-label="play or pause">Pause</button>
      <input type="range" class="scrub" min="0" max="{len(frames) - 1}" value="0" step="1" aria-label="the interval">
      <span class="tick">interval {ticks[0]}</span>
    </div>
    <figcaption>{caption} Pause and drag the slider to any interval; the intervals per frame vary as the caption says. The same frames as one GIF, inside this page: <a href="{gif_uri}" download="{name}.gif">{name}.gif</a>.</figcaption>
  </figure>
  <script>
  (function () {{
    var fig = document.getElementById("player-{name}");
    var canvas = fig.querySelector("canvas"), ctx = canvas.getContext("2d");
    var button = fig.querySelector(".play"), slider = fig.querySelector(".scrub"), label = fig.querySelector(".tick");
    var sheet = new Image(); sheet.src = "{sheet}";
    var frames = {len(frames)}, cols = {columns}, fw = {w}, fh = {h};
    var ticks = {json.dumps(ticks)}, durations = {json.dumps(durations)};
    var frame = 0, playing = true, timer = null;
    function draw() {{
      ctx.drawImage(sheet, (frame % cols) * fw, Math.floor(frame / cols) * fh, fw, fh, 0, 0, fw, fh);
      slider.value = frame; label.textContent = "interval " + ticks[frame] + " of " + ticks[frames - 1];
    }}
    function schedule() {{ timer = setTimeout(function () {{ frame = (frame + 1) % frames; draw(); if (playing) {{ schedule(); }} }}, durations[frame]); }}
    function play() {{ playing = true; button.textContent = "Pause"; if (timer === null) {{ schedule(); }} }}
    function pause() {{ playing = false; button.textContent = "Play"; if (timer !== null) {{ clearTimeout(timer); timer = null; }} }}
    button.addEventListener("click", function () {{ if (playing) {{ pause(); }} else {{ play(); }} }});
    slider.addEventListener("input", function () {{ pause(); frame = parseInt(slider.value, 10); draw(); }});
    sheet.addEventListener("load", function () {{ draw(); play(); }});
    sheet.addEventListener("error", function () {{ label.textContent = "the frames did not load; open the GIF"; }});
  }})();
  </script>"""


def html_page(title: str, eyebrow: str, lede: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{STYLE}</style>
</head>
<body>
<main>
  <header>
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </header>
{body}
</main>
</body>
</html>
"""


def write_click_page(
    out: Path,
    frames: list[Image.Image],
    durations: list[int],
    ticks: list[int],
    r: dict[str, Any],
    document: dict[str, Any],
) -> None:
    gif = gif_bytes(frames, durations)
    w = Fraction(int(r["weight"][0]), int(r["weight"][1]))
    t = Fraction(int(r["total"][0]), int(r["total"][1]))
    share = float(w / t)
    run_json = f"{r['run_dir']}/run.json"
    events_jsonl = f"{r['run_dir']}/events.jsonl"
    caption = (
        f"The plane of {document['shape'][0]} x {document['shape'][1]} Nodes seen from +z (x to the right, y up, 3 pixels per Node), "
        f"the world <code>slits_low</code>: the lamp at ({document['measured'][0]['position'][0]}, {document['measured'][0]['position'][1]}), "
        "the wall at x = 8 with its two openings (green) that re-emit a row into the fan of 91 directions, the three absorbers at x = 7 (white), "
        "the screen of 121 pixels at x = 52 (dark cyan) and the open faces in y (purple dots). The record's rows are drawn at their Nodes: "
        "the hue is the phase on the circle of N = 64, the brightness the magnitude of the phase-count vector at the Node. "
        f"One frame per interval from the birth through the split, one per four intervals across the fan's flight, one per two from the first end at the screen to the click; {len(frames)} frames."
    )
    body = f"""
  <section>
    <h2>1. The GameBoard and what is on it</h2>
    <p>The registered world <code>examples/events/amplitude/slits_low.json</code> of series L2 (the two slits at a low rate), a plane of {document["shape"][0]} x {document["shape"][1]} x 1 with z periodic and x, y open, K = 2^30, N = 64, {document["ticks"]} intervals. On it, by the world file:</p>
    <ul>
      <li><b>the lamp</b> (yellow), a measured event of the family <code>light</code> at ({document["measured"][0]["position"][0]}, {document["measured"][0]["position"][1]}), rate [1, 1]: one record per interval, each of {r["units"]} rows of amount 1 on its five directions (multiplicity {r["multiplicity"]});</li>
      <li><b>the wall</b> (grey), wall Nodes at x = 8, freed within 6 Links of each opening; <b>the two openings</b> (green) at (8, 55) and (8, 65), wall Nodes with a <code>rerelease</code> table that re-emits an arriving row into the fan of 91 directions by integer weights;</li>
      <li><b>the three absorbers</b> (white) at (7, 58), (7, 60), (7, 62), wall Nodes that end the lamp's three rows that miss the openings;</li>
      <li><b>the screen</b> (dark cyan), 121 pixels at x = 52, each a detector of one Node reading <code>sum</code> (<code>screen_0</code> .. <code>screen_120</code>);</li>
      <li><b>the open faces</b> in y (purple), detectors too: a row leaving the board clicks there.</li>
    </ul>
    <p class="fine">The lamp births one record per interval; this page follows one of them and draws only its rows. The other records are their own: the merge adds rows of one record only, and no rule of the GameBoard reads another record, so the picture of this record is the same with or without them.</p>
  </section>

  <section>
    <h2>2. Why it was shown</h2>
    <p>The model owner, 2026-09-21 (translated): "show me an HTML with a GIF of how a click looks: I want to see the amplitudes spreading, and a click on the other side, and how the amplitudes in it spread". This is a demonstration of the registered world, not a new reading: every number below is the run's, as the register L2 has it.</p>
  </section>

  <section>
    <h2>3. The moving picture: one record from its birth to its click</h2>
{player(frames, durations, ticks, "click", caption, gif)}
    <div class="moments">
      <div class="moment"><b>spreading</b><p>Born at tick {r["born"]} with the birth phase u = {r["u"]}, the record's {r["units"]} rows fly toward the wall; three end at the absorbers (ticks {", ".join(str(x) for x in r["wall_ticks"])}) and two pass the openings, where at tick {r["split_tick"]} the split re-creates them as {r["split_units"]} units over the fan, which spreads behind the wall with its phases and ends, row by row, at the screen's pixels (from tick {r["first_screen"]}) and at the faces, each end adding its pointer to the record's offer at that set.</p></div>
      <div class="moment"><b>the click</b><p>At tick {r["gather_tick"]} the last row ends and the record is complete: the layer builds the ladder over its {r["cells"]} cells (the Gram weight of each set, coherent within a Node and incoherent across Nodes, normalised by the total), and u = {r["u"]} falls in the cell {r["click_cell"]} (its rungs {r["rung_before"]} to {r["rung"]} of 64): the click is at the pixel ({r["click_node"][0]}, {r["click_node"][1]}), with the content {r["content"]}.</p></div>
      <div class="moment"><b>the deletion</b><p>In the same interval the record leaves the layer's table: its {r["offers"]} offers (the pointers of {r["ended"]} units that ended at {r["sets"]} sets) are erased, and nothing of the record remains anywhere; the world kept one bit, the cell that clicked.</p></div>
    </div>
  </section>

  <section>
    <h2>4. The numbers, read from the run</h2>
    <div class="pair">
      <div class="reading"><div class="label">the click's interval <span class="kind">detector</span></div><div class="value">tick {r["gather_tick"]}</div><div class="note">The gather line of the record {r["identity"]} (u = {r["u"]}, born at tick {r["born"]}) in <code>run.json</code>'s <code>world</code>: <code>tick</code> {r["gather_tick"]}, <code>arrived</code> {r["gather_tick"]}, <code>chosen</code> {r["click_cell"]}, <code>node</code> ({r["click_node"][0]}, {r["click_node"][1]}, {r["click_node"][2]}), <code>content</code> {r["content"]}.</div></div>
      <div class="reading"><div class="label">the weight against the threshold <span class="kind">gameboard</span></div><div class="value">{share:.4f} of the total</div><div class="note">The chosen cell's <code>weight</code> {r["weight"][0]} / {r["weight"][1]} against the record's <code>total</code> {r["total"][0]} / {r["total"][1]}, both in the unit 2^58 (one row of amount 1): the cell {float(w / r["unit"]):.4f} of the birth norm, the total {float(t / r["unit"]):.4f}. The threshold of the click is the rung: b_k = (2 N C_k + T) // (2 T) with C_k the cumulative weight and T the total gives the rungs {r["rung_before"]} and {r["rung"]} around u = {r["u"]}; the click is the one comparison u &lt; b_k (<code>cell_of</code>, the fraction-free form). The detectors' declared <code>threshold</code> is 1 on every pixel.</div></div>
      <div class="reading"><div class="label">the rows deleted <span class="kind">gameboard</span></div><div class="value">{r["offers"]} offers, 0 rows</div><div class="note">At the completion every row of the record had already ended ({r["ended"]} units at {r["sets"]} sets, the <code>click</code> lines of <code>events.jsonl</code> carrying <code>record</code> {r["identity"]}); what the click deletes is the record's vector in the layer, {r["offers"]} pointers (one per end Node and label), and the record's entry in the table. No row of it was on the GameBoard to delete.</div></div>
      <div class="reading"><div class="label">the pointer at the clicked pixel <span class="kind">gameboard</span></div><div class="value">({r["pointer"][0]}, {r["pointer"][1]})</div><div class="note">The accumulated pointer (X, Y) of the offer at <code>{r["click_cell"]}</code>, 32 x amount x (C[phase], S[phase]) summed over the rows that ended there, the tables C and S at the scale 256; its square X^2 + Y^2 is the cell's Gram weight up to the multiplicity {r["weight"][1]}.</div></div>
    </div>
    <div class="tablewrap"><table>
      <thead><tr><th>reading</th><th>value</th><th>kind</th><th>source</th></tr></thead>
      <tbody>
        <tr><td>the birth</td><td class="num">tick {r["born"]}, u = {r["u"]}, {r["units"]} rows of amount 1, multiplicity {r["multiplicity"]}</td><td>gameboard</td><td>the <code>birth</code> line of <code>events.jsonl</code></td></tr>
        <tr><td>the absorbers</td><td class="num">3 rows ended at ticks {", ".join(str(x) for x in r["wall_ticks"])}</td><td>gameboard</td><td>the <code>click</code> lines at <code>measured:223 .. 225</code></td></tr>
        <tr><td>the split</td><td class="num">tick {r["split_tick"]}: 2 rows in, {r["split_units"]} units out</td><td>gameboard</td><td>the two <code>split</code> lines</td></tr>
        <tr><td>the ends at the screen and the faces</td><td class="num">ticks {r["first_screen"]} to {r["gather_tick"]}, {r["ended"]} units at {r["sets"]} sets in all</td><td>gameboard</td><td>the <code>click</code> lines</td></tr>
        <tr><td>the ladder</td><td class="num">{r["cells"]} cells; the rungs give wall {r["rung_shares"].get("wall", 0)}, screen {r["rung_shares"].get("screen", 0)}, faces {r["rung_shares"].get("face", 0)} of 64</td><td>gameboard</td><td>the gather's <code>cells</code></td></tr>
        <tr><td>the click</td><td class="num">tick {r["gather_tick"]}, {r["click_cell"]} at ({r["click_node"][0]}, {r["click_node"][1]}), content {r["content"]}</td><td>detector</td><td><code>run.json</code>, <code>world</code></td></tr>
        <tr><td>the register</td><td class="num">over the 64 births: wall 34, screen 15 (one at y = 60), faces 15</td><td>detector</td><td><code>expectations.json</code>, <code>two_slits.clicks</code>; EXPERIMENTS L2</td></tr>
      </tbody>
    </table></div>
    <p class="fine">The run: <code>{run_json}</code> and <code>{events_jsonl}</code>, the runner on the checkout's source fingerprint <code>{r["fingerprint"][:12]}</code>, {r["ticks"]} intervals in {r["elapsed"]:.1f} s, completed and conserved at every tick. The frames are the same engine stepped in-process; its gathers equal the run's <code>world</code> (checked before this page was written). GAMEBOARD readings are the host's view of the deterministic board, the picture; the DETECTOR reading is the click, the world's row.</p>
  </section>

  <section>
    <h2>5. What the picture shows</h2>
    <p>The amplitudes that spread are the rows of one record with their phases: the GameBoard carries them locally, one Link per interval at most, and never reads the layer. The click happens once, at the completion, when the whole record has ended: the ladder of the Gram weights and the one birth phase u decide the cell, the content goes to that Node, and the record's vector <b>f</b> (its offers) is erased everywhere in the same interval. This is the reading of DERIVATIONS_BEAM section 14: the click reads a few bits of u and erases the rest; the rows on the GameBoard were never deleted at the click because none remained.</p>
  </section>
"""
    page = html_page(
        "The Click of One Record",
        "beam-v1 · amplitude-v1 · 2026-09-21 · visualisation requested",
        "One record of the registered two-slit world, from the lamp to the screen: the rows spreading with their phases, the offers and the ladder growing at the detectors, the click at one pixel and the deletion of the record.",
        body,
    )
    (out / "click.html").write_text(page, encoding="utf-8")


def write_bell_page(
    out: Path, frames: list[Image.Image], durations: list[int], ticks: list[int], r: dict[str, Any]
) -> None:
    gif = gif_bytes(frames, durations)
    reg = r["register"]
    meas = r["measured"]
    S = r["S"]
    caption = (
        f"The four registered worlds stacked, one bar of {r['shape'][0]} Nodes each (x to the right), from the birth of the first record at tick 1 to the gather of the 64th birth; "
        "one frame per interval through the first record's two clicks, then one per four intervals. On each bar: the lamp at x = 10, Alice's counters at x = 7 (A+) and 4 (A-), Bob's at x = 17 (B+) and 18 (B-); "
        "the first record's rows in orange (two per arm, the labels 00 and 11), the later records' rows grey; at the right the pointer read at each side, the four cells of the record gathered at this interval with their rungs and the clicks counted so far."
    )
    rows = ""
    for key, label in (
        ("0_8", "(0, 8)"),
        ("0_24", "(0, 24)"),
        ("16_8", "(16, 8)"),
        ("16_24", "(16, 24)"),
    ):
        e = reg[key]
        m = meas[key]
        rows += f'<tr><td><code>bell_{key}</code> {label}</td><td class="num">{e["++"]} / {e["+-"]} / {e["-+"]} / {e["--"]}</td><td class="num">{e["E"]} / 64 = {e["E"] / 64:+.4f}</td><td class="num">{m["++"]} / {m["+-"]} / {m["-+"]} / {m["--"]}, E x 64 = {m["E"]}</td><td>{"equal" if m["E"] == e["E"] else "differs"}</td></tr>\n'
    ends = r["ends"]
    alice = [e for e in ends if e[1] == "alice_plus"]
    bob = [e for e in ends if e[1] == "bob_plus"]
    g = r["gather"]
    cells = ", ".join(
        f"{''.join(str(f[2]) for f in factors)} up to {rung}" for factors, rung in g["cells"]
    )
    body = f"""
  <section>
    <h2>1. The GameBoard and what is on it</h2>
    <p>The registered Bell worlds of series L3, <code>examples/events/amplitude/bell_0_8.json</code>, <code>bell_0_24.json</code>, <code>bell_16_8.json</code>, <code>bell_16_24.json</code>: a bar of {r["shape"][0]} Nodes, open, K = 15 x 2^20, N = 64, 80 intervals. On it, by the world files:</p>
    <ul>
      <li><b>the lamp</b> (yellow) at x = 10, a measured event of the family <code>light</code> with <code>arms</code> {r["arms"]} on the directions -x and +x and <code>branches</code> {json.dumps(r["branches"])}: every birth is ONE record with two arms, four rows of amount 1 (per arm one row per joint label, the labels 0 = 00 and 3 = 11 with the weights 1 and 1), the record's identity the lamp's number x 2^32 + the birth's ordinal, its birth phase u the ordinal less one, mod 64, written on all four rows (<code>events.jsonl</code>, the <code>birth</code> line: <code>arms</code> 2, <code>units</code> 4, <code>multiplicity</code> 2);</li>
      <li><b>Alice's counters</b> (cyan) at x = 7 and x = 4, measured events of the family <code>counter</code> reading <code>light</code> with a <code>phase_window</code>, her setting a; <b>Bob's counters</b> (magenta) at x = 17 and 18 with his setting b. Each is a detector of one Node reading <code>sum</code> (<code>alice_plus</code>, <code>alice_minus</code>, <code>bob_plus</code>, <code>bob_minus</code>).</li>
    </ul>
    <p class="fine">Under the amplitude law the rows of an arm end at the first counter they reach (x = 7, x = 17), where the setting rotates the arm's label bit by the half-angle tables of 2N and offers the channels + and -; the counters at x = 4 and 18 receive no row in these runs. The four registered settings (a, b) are the names of the worlds: (0, 8), (0, 24), (16, 8), (16, 24), the CHSH quadruple.</p>
  </section>

  <section>
    <h2>2. Why it was shown</h2>
    <p>The model owner, 2026-09-21 (translated): "the famous experiment with two detectors entangled through the middle that asks for 2.83, how it fits with the amplitudes, since the detectors are in fact already entangled; show something one really sees on the board, how things are entangled in their amplitudes". This is a demonstration of the registered worlds; the correlations and S are the register's, nothing is tuned.</p>
  </section>

  <section>
    <h2>3. The moving picture: one record, two arms, two clicks</h2>
{player(frames, durations, ticks, "bell", caption, gif)}
    <div class="moments">
      <div class="moment"><b>one record</b><p>Born at tick {r["birth"]["tick"]} at the lamp with u = {r["birth"]["u"]}, the record's four rows leave on the two arms, two toward Alice and two toward Bob, all four carrying the one phase u: one vector, drawn in one colour on both sides.</p></div>
      <div class="moment"><b>two pointers</b><p>Alice's rows end at <code>alice_plus</code> (x = 7) at tick {alice[0][0]} (age {alice[0][5]}), Bob's at <code>bob_plus</code> (x = 17) at tick {bob[0][0]} (age {bob[0][5]}); each end adds its pointer (X, Y) to the record's offer at that set, where the setting rotates the label bit into the channels + and -. Until both arms have ended there is no cell: the joint amplitude needs both readings.</p></div>
      <div class="moment"><b>two clicks</b><p>At tick {g["tick"]} the record is complete; the four cells ++, +-, -+, -- get the Gram weights of the joint amplitude (the sum over the labels of the product of the two arms' residuals), the ladder's rungs are {cells}, and u = {g["u"]} falls in {"".join(str(f[2]) for f in g["chosen"])}: the two clicks, at ({g["node"][0][0]}, 0, 0) and ({g["node"][1][0]}, 0, 0), in the same interval, from one cell.</p></div>
    </div>
  </section>

  <section>
    <h2>4. The correlations of the register and S</h2>
    <div class="tablewrap"><table>
      <thead><tr><th>world (a, b)</th><th>register: ++ / +- / -+ / -- over 64 births</th><th>register: E</th><th>this run's gathers, u = 0 .. 63</th><th>verdict</th></tr></thead>
      <tbody>
{rows}      </tbody>
    </table></div>
    <div class="pair">
      <div class="reading"><div class="label">S of the register <span class="kind">detector</span></div><div class="value">S = {r["S64"]} / 64 = {float(S):.4f}</div><div class="note">S = E(0, 8) - E(0, 24) + E(16, 8) + E(16, 24) with E = (++ + -- - +- - -+) / 64, exactly as <code>expectations.json</code> under <code>pair.chsh</code> and <code>pair.chsh_S</code> = {r["S64"]} define it (the design's <code>bell.py</code>; EXPERIMENTS L3). Each E is a DETECTOR reading of the gathers.</div></div>
      <div class="reading"><div class="label">the two bounds</div><div class="value">2 and 2 sqrt 2 = 2.8284</div><div class="note">The classical bound of a local deterministic window is 2; the quantum bound (Tsirelson) is 2 sqrt 2 = 2.8284. The registered S = {float(S):.4f} passes 2 and does not reach 2.83: the register says S = 2 sqrt 2 - epsilon(N), the discreteness of the 64 birth phases and of the tables (the design's epsilon at most 4 / N, not met at N = 64: 0.078 against 0.0625). At N = 1024 and 4096 (series L6, the same board) the register reads S = 2896 / 1024 = 2.828125 and 11584 / 4096 = 2.828125, below 2 sqrt 2 at every N.</div></div>
    </div>
    <p class="fine">The runs: <code>{r["run_dirs"]["bell_0_8"]}</code> and its three siblings (<code>run.json</code>, <code>events.jsonl</code>), the runner on the checkout's source fingerprint <code>{r["fingerprint"][:12]}</code>, 80 intervals in {max(r["elapsed"].values()):.2f} s each, completed and conserved at every tick; the counts of the table are the gathers of <code>run.json</code>'s <code>world</code> for the records of ordinals 1 .. 64 (the lamp's clock stalls once, so the 64th birth is at tick 65), equal to the register on every world. The frames are the same engine stepped in-process; its gathers equal the run's.</p>
  </section>

  <section>
    <h2>5. Why the two clicks are correlated on this board</h2>
    <p>There is one record, born once at the lamp, and its four rows carry one phase-count vector <b>f</b> with the joint labels 00 and 11: the label of Alice's row and the label of Bob's row are the same bit, written together at the birth, and the rows fly apart carrying it. Each counter reads its own arm through the Gram form <b>G</b> of the layer at its setting (the rotation of the label bit by the half-angle tables), and the weight of a joint cell is the square of the sum over the labels of the product of the two readings: the cross terms of 00 and 11 are what make the weights of ++ and -- 27 of 64 and those of +- and -+ 5 of 64 at (0, 8), and the same numbers with the signs exchanged at (0, 24). At the completion one birth phase u, the record's own scalar, falls in one cell, and both clicks are that cell's: nothing is sent between the counters at the click, no row crosses from x = 7 to x = 17, the counters never read each other; the correlation was in the one vector from the birth, and the click reads it at two places. Over the 64 births u runs the circle once, so the counts are the rungs, and S is their sum.</p>
  </section>
"""
    page = html_page(
        "The Pair and Its Two Clicks",
        "beam-v1 · amplitude-v1 · 2026-09-21 · visualisation requested",
        "The registered Bell worlds: one record with two arms, read at Alice's and Bob's counters, its two clicks from one cell, and the correlations that give S = 176 / 64 = 2.75 against the bounds 2 and 2.83.",
        body,
    )
    (out / "bell.html").write_text(page, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, required=True, help="the folder of the runner's outputs")
    parser.add_argument("--out", type=Path, default=HERE, help="where the pages are written")
    parser.add_argument("--samples", type=Path, help="a folder for a few frames as PNG, for the eye")
    args = parser.parse_args()
    global SAMPLES
    SAMPLES = args.samples
    args.out.mkdir(parents=True, exist_ok=True)
    click = build_click(args.runs, args.out)
    print(json.dumps(click, default=str))
    bell = build_bell(args.runs, args.out)
    print(
        json.dumps(
            {k: bell[k] for k in ("S64", "S", "frames", "register", "measured", "ends")}, default=str
        )
    )
    for name in ("click.html", "bell.html"):
        print(name, (args.out / name).stat().st_size, "bytes")


if __name__ == "__main__":
    main()
