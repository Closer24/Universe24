"""The visual gallery: one HTML page per situation, the moving picture inside it.

The model owner asked on 2026-09-21 for pages that show, in beautiful HTML,
the situations the project talks about, in the terms of the law: beams and
clicks, nothing else. This host-only tool makes those pages under
`docs/pages/gallery/`. It changes no law and pins no number: a page shows a
registered world where one shows the story (its numbers read from the
run's files, `run.json` and `events.jsonl`, and from the register beside
the world) or a demonstration world of `examples/events/gallery/`, labelled
as a demonstration and never as a registered result.

Two kinds of readings appear on every page and are labelled as the register
labels them ([the experiments register](../docs/EXPERIMENTS.md), "Two kinds
of readings"): the moving picture is a GameBoard reading, the host's view of
the rows and the bodies at every interval, taken by replaying the world in
process through `NatureBeamSimulation` and reading its stores (nothing of
the law is replayed here: the engine steps, this tool draws); the clicks,
the pointers, the records and the pushes are detector readings, taken from
the record the runner wrote.

The page convention (the simulation runner skill, the model owner,
2026-09-19 and 2026-09-20): the GIF inside the HTML, a frame player with
play and pause and a slider over the intervals with the interval shown, the
GIF kept as a link, the frames downscaled and at most about 120 per
picture, every page a few megabytes at most.

    PYTHONPATH=src python tools/gallery_pages.py --page beam --out docs/pages/gallery
    PYTHONPATH=src python tools/gallery_pages.py --page all --runs artifacts/gallery_runs

`--runs DIR` keeps (and reuses) the runner's records under
`DIR/<world>/run/`; without it they are written to a temporary directory
and the page keeps their numbers.
"""

from __future__ import annotations

import argparse
import base64
import colorsys
import html
import io
import json
import math
import shutil
import tempfile
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from event_universe.events import NatureBeamSimulation
from event_universe.runner import run_initialization, source_fingerprint
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events"
GALLERY_WORLDS = WORLDS / "gallery"
FONT_PATHS = (
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
)
MAX_FRAMES = 120
SQRT3 = math.sqrt(3.0)
# Each family without a phase circle takes one of these colours, in the
# order the world declares its families; a family with a phase circle is
# drawn by its phase (the hue of the circle).
FAMILY_COLOURS = (
    (255, 99, 71),
    (80, 160, 255),
    (255, 200, 40),
    (120, 220, 120),
    (220, 120, 255),
    (255, 140, 200),
)
BODY_COLOURS = {
    "p": (255, 99, 71),
    "n": (80, 160, 255),
    "light": (255, 220, 90),
    "apparatus": (170, 170, 190),
    "wall": (170, 170, 190),
    "m": (200, 200, 220),
    "d": (120, 200, 160),
    "w": (220, 120, 255),
}


# ---------------------------------------------------------------------------
# The capture: the world replayed in process, its stores read every interval


@dataclass
class Rows:
    """One family's rows at one interval (a GameBoard reading): the columns
    of the store read as they are, the Node unpacked into x, y, z."""

    family: str
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    phase: np.ndarray
    amount: np.ndarray
    direction: np.ndarray
    age: np.ndarray
    record: np.ndarray
    number: np.ndarray
    multiplicity: np.ndarray
    birth: np.ndarray


@dataclass
class Body:
    """A measured event at one interval: its number, family, Node, content,
    momentum vector **p** and phase."""

    number: int
    family: str
    position: tuple[int, int, int]
    content: int
    momentum: tuple[int, int, int]
    phase: int


@dataclass
class SetState:
    """A detector set at one interval: its name, its Nodes, its cumulative
    record and its phase per family."""

    name: str
    nodes: list[tuple[int, int, int]]
    record: dict[str, int]
    phase: dict[str, int | None]


@dataclass
class Frame:
    tick: int
    rows: list[Rows]
    bodies: list[Body]
    sets: list[SetState]


class Replay:
    """A world stepped in process; `run` returns the frames at the requested
    intervals and `events` holds every record line the engine emitted, the
    same lines the runner writes to `events.jsonl`."""

    def __init__(self, path: Path, ticks: int | None = None) -> None:
        self.path = path
        self.source = path.read_bytes()
        self.loaded = load_world(self.source, base_dir=path.parent)
        self.world = self.loaded.world
        self.ticks = self.world.ticks if ticks is None else ticks
        self.events: list[dict[str, object]] = []
        self.simulation = NatureBeamSimulation(self.world, observer=self.events.append)
        self.families = [family.name for family in self.world.families]
        self.directions = [tuple(int(c) for c in v) for v in self.world.directions]

    def capture(self) -> Frame:
        simulation = self.simulation
        rows = []
        for name, store in zip(self.families, simulation.stores, strict=True):
            x, y, z = store.coordinates(store.node)
            rows.append(
                Rows(
                    name,
                    x.copy(),
                    y.copy(),
                    z.copy(),
                    store.phase.copy(),
                    store.amount.copy(),
                    store.direction.copy(),
                    store.age.copy(),
                    store.record.copy(),
                    store.number.copy(),
                    store.multiplicity.copy(),
                    store.birth.copy(),
                )
            )
        bodies = [
            Body(
                entry.number,
                self.families[entry.family],
                tuple(int(c) for c in entry.position),
                int(sum(entry.held)),
                tuple(int(c) for c in entry.momentum),
                int(entry.phase),
            )
            for entry in simulation.measured.values()
        ]
        sets = [
            SetState(
                str(detector.name) if detector.name is not None else f"measured:{detector.numbers[0]}",
                [tuple(int(c) for c in node) for node in detector.nodes],
                {name: int(detector.record[f]) for f, name in enumerate(self.families)},
                {name: detector.phase[f] for f, name in enumerate(self.families)},
            )
            for detector in simulation.detector_sets
        ]
        return Frame(simulation.tick, rows, bodies, sets)

    def run(self, ticks: Iterable[int]) -> list[Frame]:
        wanted = sorted(set(int(t) for t in ticks))
        frames: list[Frame] = []
        for tick in wanted:
            while self.simulation.tick < tick:
                self.simulation.step()
            frames.append(self.capture())
        return frames


def frame_ticks(last: int, count: int = MAX_FRAMES, first: int = 0) -> list[int]:
    """At most `count` intervals from `first` to `last`, evenly spaced, the
    ends kept."""
    if last - first + 1 <= count:
        return list(range(first, last + 1))
    return sorted({first + round(k * (last - first) / (count - 1)) for k in range(count)})


# ---------------------------------------------------------------------------
# The record: the runner's files, read for the detector readings


def runner_record(path: Path, runs: Path | None, ticks: int | None = None) -> Path:
    """The runner's record of the world at `path`: `<runs>/<stem>/run/` when
    it exists (reused), made by `run_initialization` otherwise."""
    root = runs if runs is not None else Path(tempfile.mkdtemp(prefix="gallery_"))
    output = root / path.stem / "run"
    if not (output / "run.json").exists():
        if output.exists():
            shutil.rmtree(output)
        run_initialization(path, output, ticks=ticks)
    return output


def scan_events(path: Path, kinds: Sequence[str]) -> dict[str, list[dict[str, object]]]:
    """The lines of `events.jsonl` of the given kinds, by kind; a line is
    parsed only when its kind is wanted (the records of a bound nucleus hold
    a million border clicks)."""
    keys = {kind: f'"event": "{kind}"' for kind in kinds}
    found: dict[str, list[dict[str, object]]] = {kind: [] for kind in kinds}
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            for kind, key in keys.items():
                if key in line:
                    found[kind].append(json.loads(line))
                    break
    return found


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# The drawing


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_PATHS:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def phase_colour(phase: float, steps: int, value: float = 1.0) -> tuple[int, int, int]:
    """The hue of the circle Z_N at the phase, at the given brightness."""
    r, g, b = colorsys.hsv_to_rgb((phase % steps) / steps, 0.85, value)
    return int(255 * r), int(255 * g), int(255 * b)


def brightness(amount: np.ndarray, largest: float) -> np.ndarray:
    """A visible floor and a logarithmic rise: colour is not a linear
    measurement of the amount."""
    largest = max(float(largest), 1.0)
    return 0.35 + 0.65 * np.log2(1.0 + amount) / math.log2(1.0 + largest)


@dataclass
class Plane:
    """The x-y plane of a GameBoard drawn at `scale` pixels per Node, the
    rows' amounts summed over z (or taken at one z, `slice_z`), y upward;
    a family with a phase circle coloured by the amount-weighted mean of
    its phases at the Node, a family without one by its own colour."""

    shape: tuple[int, int, int]
    scale: int
    phase_steps: int
    phased: dict[str, bool]
    colours: dict[str, tuple[int, int, int]]
    slice_z: int | None = None
    margin: int = 6
    largest: dict[str, float] = field(default_factory=dict)
    detector_nodes: set[tuple[int, int, int]] = field(default_factory=set)
    detector_names: dict[tuple[int, int, int], str] = field(default_factory=dict)

    @property
    def size(self) -> tuple[int, int]:
        return (
            self.shape[0] * self.scale + 2 * self.margin,
            self.shape[1] * self.scale + 2 * self.margin,
        )

    def pixel(self, x: float, y: float) -> tuple[float, float]:
        """The centre of the Node (x, y) in image coordinates."""
        return (
            self.margin + (x + 0.5) * self.scale,
            self.margin + (self.shape[1] - 1 - y + 0.5) * self.scale,
        )

    def canvas(self) -> tuple[Image.Image, ImageDraw.ImageDraw]:
        image = Image.new("RGB", self.size, (14, 16, 24))
        draw = ImageDraw.Draw(image)
        w, h = self.size
        draw.rectangle(
            [self.margin - 1, self.margin - 1, w - self.margin, h - self.margin],
            outline=(70, 74, 92),
        )
        return image, draw

    def layer(self, rows: Rows) -> np.ndarray:
        """The RGB contribution of one family's rows as a float array of
        shape (X, Y, 3)."""
        nx, ny, _ = self.shape
        out = np.zeros((nx, ny, 3), dtype=np.float64)
        if rows.amount.size == 0:
            return out
        keep = np.ones(rows.amount.shape, dtype=bool)
        if self.slice_z is not None:
            keep = rows.z == self.slice_z
        x, y = rows.x[keep], rows.y[keep]
        amount = rows.amount[keep].astype(np.float64)
        if x.size == 0:
            return out
        total = np.zeros((nx, ny), dtype=np.float64)
        np.add.at(total, (x, y), amount)
        value = brightness(total, self.largest.get(rows.family, float(total.max())))
        lit = total > 0
        if self.phased.get(rows.family, False):
            angle = rows.phase[keep].astype(np.float64) * (2 * math.pi / self.phase_steps)
            cx = np.zeros((nx, ny))
            sy = np.zeros((nx, ny))
            np.add.at(cx, (x, y), amount * np.cos(angle))
            np.add.at(sy, (x, y), amount * np.sin(angle))
            hue = (np.arctan2(sy, cx) / (2 * math.pi)) % 1.0
            # The resultant's length against the amount: a Node whose rows
            # disagree in phase is drawn greyer.
            saturation = np.where(total > 0, np.hypot(cx, sy) / np.maximum(total, 1e-9), 0.0)
            saturation = 0.25 + 0.75 * saturation
            for i, j in zip(*np.nonzero(lit), strict=True):
                r, g, b = colorsys.hsv_to_rgb(hue[i, j], saturation[i, j], value[i, j])
                out[i, j] = (r, g, b)
        else:
            colour = np.array(self.colours[rows.family], dtype=np.float64) / 255.0
            out[lit] = value[lit][:, None] * colour[None, :]
        return out

    def image(
        self, frame: Frame, decorate: Callable[[ImageDraw.ImageDraw], None] | None = None
    ) -> Image.Image:
        image, draw = self.canvas()
        nx, ny, _ = self.shape
        rgb = np.zeros((nx, ny, 3), dtype=np.float64)
        for rows in frame.rows:
            rgb += self.layer(rows)
        rgb = np.clip(rgb, 0.0, 1.0)
        pixels = (rgb * 255).astype(np.uint8)
        # (x, y) -> image (column x, row from the top): flip y, transpose.
        board = Image.fromarray(np.transpose(pixels[:, ::-1, :], (1, 0, 2)), "RGB")
        if self.scale != 1:
            board = board.resize((nx * self.scale, ny * self.scale), Image.NEAREST)
        # Nodes without rows stay the background: paste through a mask of
        # the lit Nodes.
        lit = Image.fromarray(
            (np.transpose(rgb[:, ::-1, :].sum(axis=2) > 0) * 255).astype(np.uint8), "L"
        )
        if self.scale != 1:
            lit = lit.resize(board.size, Image.NEAREST)
        image.paste(board, (self.margin, self.margin), lit)
        for node in self.detector_nodes:
            if self.slice_z is not None and node[2] != self.slice_z:
                continue
            cx, cy = self.pixel(node[0], node[1])
            half = self.scale / 2
            draw.rectangle([cx - half, cy - half, cx + half - 1, cy + half - 1], outline=(120, 220, 160))
        radius = max(self.scale * 0.55, 3.0)
        for body in frame.bodies:
            if self.slice_z is not None and body.position[2] != self.slice_z and self.shape[2] > 1:
                pass
            cx, cy = self.pixel(body.position[0], body.position[1])
            colour = BODY_COLOURS.get(body.family, (230, 230, 230))
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                fill=colour,
                outline=(255, 255, 255),
            )
            if self.scale >= 12:
                label = body.family[:2]
                draw.text(
                    (cx, cy),
                    label,
                    fill=(0, 0, 0),
                    font=font(max(8, int(self.scale * 0.7))),
                    anchor="mm",
                )
        if decorate is not None:
            decorate(draw)
        return image


@dataclass
class Cube:
    """An open cube drawn in an oblique projection, the rows as discs with
    the heading as a short arrow: for a board of a few rows (the collision)."""

    shape: tuple[int, int, int]
    scale: int
    phase_steps: int
    directions: list[tuple[int, int, int]]
    margin: int = 24

    def project(self, x: float, y: float, z: float) -> tuple[float, float]:
        nx, ny, nz = self.shape
        u = (x + 0.5) + 0.5 * (z + 0.5)
        v = (ny - 1 - y + 0.5) + 0.5 * (nz - 1 - z + 0.5)
        return self.margin + u * self.scale, self.margin + v * self.scale

    @property
    def size(self) -> tuple[int, int]:
        nx, ny, nz = self.shape
        return (
            int((nx + 0.5 * nz) * self.scale + 2 * self.margin),
            int((ny + 0.5 * nz) * self.scale + 2 * self.margin),
        )

    def image(self, frame: Frame, highlight: tuple[int, int, int] | None = None) -> Image.Image:
        image = Image.new("RGB", self.size, (14, 16, 24))
        draw = ImageDraw.Draw(image)
        nx, ny, nz = self.shape
        corners = [
            (x, y, z) for x in (-0.5, nx - 0.5) for y in (-0.5, ny - 0.5) for z in (-0.5, nz - 0.5)
        ]
        for a in corners:
            for b in corners:
                if sum(1 for i in range(3) if a[i] != b[i]) == 1 and a < b:
                    draw.line([self.project(*a), self.project(*b)], fill=(70, 74, 92), width=1)
        # The floor's grid at z = 0 helps the eye place a Node.
        for x in range(nx):
            draw.line([self.project(x, -0.5, -0.5), self.project(x, ny - 0.5, -0.5)], fill=(34, 38, 52))
        if highlight is not None:
            cx, cy = self.project(*highlight)
            r = self.scale * 0.6
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 220, 160), width=2)
        radius = self.scale * 0.32
        for rows in frame.rows:
            order = np.argsort(rows.z, kind="stable")
            for k in order:
                x, y, z = int(rows.x[k]), int(rows.y[k]), int(rows.z[k])
                cx, cy = self.project(x, y, z)
                colour = phase_colour(int(rows.phase[k]), self.phase_steps)
                d = self.directions[int(rows.direction[k])]
                draw.ellipse(
                    [cx - radius, cy - radius, cx + radius, cy + radius],
                    fill=colour,
                    outline=(255, 255, 255),
                )
                if any(d):
                    ex, ey = self.project(x + 0.9 * d[0], y + 0.9 * d[1], z + 0.9 * d[2])
                    draw.line([(cx, cy), (ex, ey)], fill=(255, 255, 255), width=2)
        return image


# ---------------------------------------------------------------------------
# The GIF, the sprite sheet and the page


def gif_bytes(images: Sequence[Image.Image], duration_ms: int) -> bytes:
    palettes = [image.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for image in images]
    buffer = io.BytesIO()
    palettes[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=palettes[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
    )
    return buffer.getvalue()


def sprite_sheet(images: Sequence[Image.Image]) -> tuple[bytes, int, int, int]:
    """One PNG holding every frame in a grid; (png, columns, width, height)."""
    w, h = images[0].size
    columns = max(1, min(len(images), int(math.ceil(math.sqrt(len(images) * h / max(w, 1))))))
    rows = int(math.ceil(len(images) / columns))
    sheet = Image.new("RGB", (columns * w, rows * h), (14, 16, 24))
    for k, image in enumerate(images):
        sheet.paste(image, ((k % columns) * w, (k // columns) * h))
    buffer = io.BytesIO()
    sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(buffer, format="PNG", optimize=True)
    return buffer.getvalue(), columns, w, h


def data_url(payload: bytes, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(payload).decode('ascii')}"


@dataclass
class Player:
    """A frame player: the frames, their intervals, and per frame the lines
    of readings shown beside the picture (label, value)."""

    key: str
    images: Sequence[Image.Image]
    ticks: Sequence[int]
    readings: Sequence[dict[str, str]]
    caption: str
    duration_ms: int = 120

    def html(self) -> str:
        png, columns, w, h = sprite_sheet(self.images)
        gif = gif_bytes(self.images, self.duration_ms)
        data = {
            "columns": columns,
            "width": w,
            "height": h,
            "count": len(self.images),
            "ticks": list(self.ticks),
            "readings": list(self.readings),
            "duration": self.duration_ms,
        }
        return f"""
<figure class="player" id="{self.key}">
  <canvas width="{w}" height="{h}" aria-label="the moving picture"></canvas>
  <div class="controls">
    <button class="play" type="button">Play</button>
    <input class="slider" type="range" min="0" max="{len(self.images) - 1}" value="0">
    <span class="tick">interval 0</span>
  </div>
  <dl class="readings"></dl>
  <figcaption>{self.caption} <a class="gif" download="{self.key}.gif">The GIF</a> (the frames at
  {self.duration_ms} ms; {len(self.images)} frames).</figcaption>
  <script type="application/json" class="frames">{json.dumps(data)}</script>
  <img class="sheet" alt="" src="{data_url(png, "image/png")}" hidden>
  <a hidden class="gifdata" href="{data_url(gif, "image/gif")}"></a>
</figure>
"""


PLAYER_SCRIPT = """
document.querySelectorAll('figure.player').forEach(function (figure) {
  var data = JSON.parse(figure.querySelector('script.frames').textContent);
  var canvas = figure.querySelector('canvas');
  var context = canvas.getContext('2d');
  var sheet = figure.querySelector('img.sheet');
  var slider = figure.querySelector('input.slider');
  var button = figure.querySelector('button.play');
  var tick = figure.querySelector('span.tick');
  var readings = figure.querySelector('dl.readings');
  figure.querySelector('a.gif').href = figure.querySelector('a.gifdata').href;
  var frame = 0, timer = null;
  function show(k) {
    frame = k;
    var sx = (k % data.columns) * data.width, sy = Math.floor(k / data.columns) * data.height;
    context.drawImage(sheet, sx, sy, data.width, data.height, 0, 0, data.width, data.height);
    slider.value = k;
    tick.textContent = 'interval ' + data.ticks[k];
    var lines = data.readings[k] || {};
    readings.innerHTML = Object.keys(lines).map(function (key) {
      return '<div><dt>' + key + '</dt><dd>' + lines[key] + '</dd></div>';
    }).join('');
    figure.dispatchEvent(new CustomEvent('frame', {detail: k}));
  }
  function play() {
    if (timer) { clearInterval(timer); timer = null; button.textContent = 'Play'; return; }
    button.textContent = 'Pause';
    timer = setInterval(function () { show((frame + 1) % data.count); }, data.duration);
  }
  button.addEventListener('click', play);
  slider.addEventListener('input', function () {
    if (timer) { clearInterval(timer); timer = null; button.textContent = 'Play'; }
    show(parseInt(slider.value, 10));
  });
  if (sheet.complete) { show(0); } else { sheet.addEventListener('load', function () { show(0); }); }
});
"""

STYLE = """
:root {
  --bg: #f6f4ee; --ink: #1c1b18; --muted: #5f5b52; --line: #d9d4c7; --card: #ffffff;
  --accent: #b5541b; --accent-ink: #ffffff; --board: #0e1018; --good: #2f7a4f;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #121317; --ink: #ebe7dd; --muted: #a39d90; --line: #2c2f38; --card: #1a1c23;
    --accent: #e8935a; --accent-ink: #14110d; --board: #0e1018; --good: #7fcf9a;
  }
}
:root[data-theme="dark"] {
  --bg: #121317; --ink: #ebe7dd; --muted: #a39d90; --line: #2c2f38; --card: #1a1c23;
  --accent: #e8935a; --accent-ink: #14110d; --board: #0e1018; --good: #7fcf9a;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.5 Georgia, "Times New Roman", serif; }
main { max-width: 900px; margin: 0 auto; padding: 24px 16px 64px; }
h1 { font-size: 2rem; line-height: 1.15; margin: 0 0 4px; }
h2 { font-size: 1.3rem; margin: 40px 0 8px; border-top: 1px solid var(--line); padding-top: 16px; }
p.lead { color: var(--muted); margin-top: 0; }
p, li, dd, dt, td, th { font-size: 1rem; }
a { color: var(--accent); }
nav.crumbs { font-size: 0.9rem; color: var(--muted); margin-bottom: 16px; }
figure.player { margin: 16px 0; background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 12px; }
figure.player canvas { display: block; max-width: 100%; height: auto; margin: 0 auto; background: var(--board); border-radius: 4px; image-rendering: pixelated; }
figure.player .controls { display: flex; gap: 12px; align-items: center; margin: 10px 0 4px; }
figure.player input.slider { flex: 1; }
figure.player button { background: var(--accent); color: var(--accent-ink); border: 0; border-radius: 6px; padding: 6px 14px; font: inherit; cursor: pointer; }
figure.player span.tick { font-variant-numeric: tabular-nums; min-width: 8em; }
figure.player dl.readings { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 4px 16px; margin: 8px 0 0; }
figure.player dl.readings div { display: flex; gap: 8px; }
figure.player dl.readings dt { color: var(--muted); margin: 0; }
figure.player dl.readings dd { margin: 0; font-variant-numeric: tabular-nums; }
figcaption { color: var(--muted); font-size: 0.92rem; margin-top: 8px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--muted); font-weight: normal; }
td.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
code { font-family: "DejaVu Sans Mono", Menlo, Consolas, monospace; font-size: 0.9em; }
.legend { display: flex; flex-wrap: wrap; gap: 10px 20px; margin: 8px 0; }
.legend span { display: inline-flex; align-items: center; gap: 8px; }
.swatch { width: 14px; height: 14px; border-radius: 50%; display: inline-block; border: 1px solid #fff8; }
.wheel { width: 14px; height: 14px; border-radius: 50%; display: inline-block; background: conic-gradient(hsl(0 85% 50%), hsl(60 85% 50%), hsl(120 85% 50%), hsl(180 85% 50%), hsl(240 85% 50%), hsl(300 85% 50%), hsl(360 85% 50%)); }
.kind { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
.demo { background: var(--card); border-left: 4px solid var(--accent); padding: 8px 12px; margin: 12px 0; }
.three { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }
.three section { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; min-height: 120px; }
.three h3 { margin: 0 0 6px; font-size: 1.05rem; }
.three pre { font-size: 0.8rem; white-space: pre-wrap; margin: 0; font-family: "DejaVu Sans Mono", Menlo, Consolas, monospace; }
ul.pages li { margin: 8px 0; }
"""


def page(title: str, lead: str, body: str, *, index_link: bool = True) -> str:
    crumbs = (
        '<nav class="crumbs"><a href="index.html">The gallery</a> · <a href="../../README.md">The documentation</a></nav>'
        if index_link
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{STYLE}</style>
</head>
<body>
<main>
{crumbs}
<h1>{html.escape(title)}</h1>
<p class="lead">{lead}</p>
{body}
</main>
<script>{PLAYER_SCRIPT}</script>
</body>
</html>
"""


def sources(lines: Sequence[tuple[str, str]]) -> str:
    rows = "".join(f"<tr><th>{html.escape(k)}</th><td>{v}</td></tr>" for k, v in lines)
    return f'<h2>Where every number comes from</h2><table class="sources">{rows}</table>'


def legend(items: Sequence[tuple[str, str]]) -> str:
    return (
        '<div class="legend">'
        + "".join(f"<span>{swatch}{html.escape(text)}</span>" for text, swatch in items)
        + "</div>"
    )


def swatch(colour: tuple[int, int, int]) -> str:
    return f'<i class="swatch" style="background: rgb({colour[0]},{colour[1]},{colour[2]})"></i>'


def num(value: object) -> str:
    """An integer with thin spaces by thousands, as the register prints them."""
    if isinstance(value, int):
        sign = "-" if value < 0 else ""
        digits = f"{abs(value):,}".replace(",", " ")
        return sign + digits
    return html.escape(str(value))


def write_page(out: Path, name: str, document: str) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.html"
    path.write_text(document, encoding="utf-8")
    return path


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def plane_for(replay: Replay, scale: int, slice_z: int | None = None) -> Plane:
    world = replay.world
    plane = Plane(
        tuple(world.shape),
        scale,
        world.phase_steps,
        {family.name: bool(family.phase) for family in world.families},
        {
            family.name: FAMILY_COLOURS[i % len(FAMILY_COLOURS)]
            for i, family in enumerate(world.families)
        },
        slice_z=slice_z,
    )
    for detector in world.detectors:
        for position in detector.positions:
            plane.detector_nodes.add(tuple(int(c) for c in position))
            plane.detector_names[tuple(int(c) for c in position)] = str(detector.name)
    return plane


def largest_amounts(frames: Sequence[Frame]) -> dict[str, float]:
    """Per family the largest amount at one Node over the frames, so that
    the brightness scale is one for the whole picture."""
    largest: dict[str, float] = {}
    for frame in frames:
        for rows in frame.rows:
            if rows.amount.size == 0:
                continue
            nodes = rows.x * 1_000_000 + rows.y * 1000 + rows.z
            unique, inverse = np.unique(nodes, return_inverse=True)
            totals = np.zeros(unique.size)
            np.add.at(totals, inverse, rows.amount.astype(np.float64))
            largest[rows.family] = max(largest.get(rows.family, 0.0), float(totals.max()))
    return largest


# ---------------------------------------------------------------------------
# The pages


PAGES: dict[str, Callable[[Path, Path | None], Path]] = {}


def register(
    name: str,
) -> Callable[[Callable[[Path, Path | None], Path]], Callable[[Path, Path | None], Path]]:
    def wrap(function: Callable[[Path, Path | None], Path]) -> Callable[[Path, Path | None], Path]:
        PAGES[name] = function
        return function

    return wrap


def demonstration_note(world: Path) -> str:
    return (
        f'<p class="demo"><b>A demonstration world</b>, <code>{relative(world)}</code>, written for this '
        "page by <code>examples/events/gallery/make_worlds.py</code>: it is not a registered experiment, "
        "no number on this page is a registered result, and nothing here enters the register. "
        "The law it runs under is the one engine, unchanged.</p>"
    )


def registered_note(world: Path, entry: str, entry_url: str) -> str:
    return (
        f'<p class="demo"><b>A registered world</b>, <code>{relative(world)}</code>, run as it is '
        f'declared; its register entry is <a href="{entry_url}">{html.escape(entry)}</a>. Nothing was '
        "changed in the world and nothing is pinned by this page.</p>"
    )


def fingerprint_line(record: dict[str, object]) -> str:
    return f"<code>{html.escape(str(record.get('source_sha256', '')))}</code> (the runner's <code>source_sha256</code>; today's package {html.escape(source_fingerprint()[:16])}...)"


@register("beam")
def page_beam(out: Path, runs: Path | None) -> Path:
    """(1) The beam: a lamp's rows spreading over the plane on the digital
    lines of its fan, the phase as colour, the front against the circle of
    the pace c and the L1 bound."""
    world = GALLERY_WORLDS / "beam_fan.json"
    record_dir = runner_record(world, runs)
    record = read_json(record_dir / "run.json")
    replay = Replay(world)
    lamp = replay.world.measured[0]
    centre = tuple(int(c) for c in lamp.position)
    ticks = frame_ticks(replay.ticks)
    frames = replay.run(ticks)
    plane = plane_for(replay, scale=8)
    plane.largest = largest_amounts(frames)
    world_document = json.loads(world.read_text(encoding="utf-8"))
    fan_directions = world_document["measured"][0]["lamp"]["directions"]
    fan = len(fan_directions)
    fan_bound = max(abs(a) + abs(b) for a, b, _ in fan_directions)
    audit = record["audit"]
    escaped_by_tick = [int(a["families"]["light"]["transit"]["escaped"]) for a in audit]
    births_by_tick = [int(a["families"]["light"]["transit"]["released"]) for a in audit]

    def decorate_at(tick: int) -> Callable[[ImageDraw.ImageDraw], None]:
        def decorate(draw: ImageDraw.ImageDraw) -> None:
            cx, cy = plane.pixel(centre[0], centre[1])
            r = tick / SQRT3 * plane.scale
            if r > 0:
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255))
                d = tick * plane.scale
                draw.polygon(
                    [(cx + d, cy), (cx, cy - d), (cx - d, cy), (cx, cy + d)], outline=(140, 140, 160)
                )

        return decorate

    images = [plane.image(frame, decorate_at(frame.tick)) for frame in frames]
    readings = []
    for frame in frames:
        t = frame.tick
        rows = frame.rows[0]
        on_board = int(rows.amount.sum())
        radius = 0.0
        if rows.amount.size:
            radius = float(np.max(np.abs(rows.x - centre[0]) + np.abs(rows.y - centre[1])))
        readings.append(
            {
                "rows on the GameBoard (GameBoard reading)": num(on_board),
                "units born so far (run.json, audit)": num(births_by_tick[t - 1] if t >= 1 else 0),
                "units escaped through the faces (run.json, audit)": num(
                    escaped_by_tick[t - 1] if t >= 1 else 0
                ),
                "farthest row, in Links of the L1 distance": num(int(radius)),
                "the circle drawn, t / sqrt 3 Links": f"{t / SQRT3:.1f}",
            }
        )
    player = Player(
        "beam",
        images,
        ticks,
        readings,
        "The x-y plane of the GameBoard, y upward, 8 pixels per Node; every Node with rows "
        "coloured by the phase of its rows (the hue of the circle: the record's birth phase u) and their "
        "amount (the brightness, logarithmic); the white circle is t / sqrt 3 Links from the lamp, the pace "
        "c of the flight table, the grey diamond is t Links, the L1 bound no row can pass.",
    )
    N = replay.world.phase_steps
    K = replay.world.K
    turn = world_document["measured"][0]["amount"] // K
    body = f"""
{demonstration_note(world)}
<h2>The GameBoard</h2>
<p>An open plane of {replay.world.shape[0]} x {
        replay.world.shape[1]
    } Nodes (z periodic with an extent of 1:
a plane). At its centre, Node {centre[:2]}, a <b>lamp</b> of the paid family <code>light</code>
(<code>quantum</code> 1: a paid family, its rows cost content), the measured event number 1 of the world
file, content {num(world_document["measured"][0]["amount"])} at the clock's rate K = {num(K)}, so its
turn is {turn} phase steps of the circle N = {N} per self-creation and every unit it releases costs
{turn} content (E = h f). Its <code>lamp</code> releases one unit per self-creation on each of {fan}
directions, the primitive in-plane vectors (a, b, 0) with |a| + |b| at most
{fan_bound}: the fan. The faces of the plane are open: a row that leaves
clicks on the face detector and is booked as escaped.</p>
{
        legend(
            [
                ("a row, coloured by its phase on the circle Z_N", '<i class="wheel"></i>'),
                ("the lamp (a measured event)", swatch(BODY_COLOURS["light"])),
            ]
        )
    }
<h2>Why this page</h2>
<p>The owner asked to see how the beam spreads on the GameBoard: "in our system there is something that
spreads, the beam, and there are clicks, nothing else". This page shows the spreading alone. Every row
(a message in flight: one point of Node x direction x phase x age x amount x number) follows the digital
line of its direction by the flight table, at most one Link per interval; on a heading it crosses 32
Links in 55 intervals, and every direction of the fan keeps the same Euclidean pace, c = 1 / sqrt 3
Links per interval, the norm of the flight operator. The phase a row carries is the record's birth phase u, the
wheel value: the lamp's count of births less one, modulo N, the same on every row of the record whatever
the lamp's turn (the K finding of 2026-09-20, BEAM_LAW note 37), and no phase per Link is declared. One
record is born per interval here, so the hue turns once round the circle over {
        N
    } intervals from the front
inward: the front, born at u = 0, is red, and the rows born later are yellow, green, blue in turn. The
clock's turn, {
        turn
    } steps per self-creation, is what each unit costs the lamp (E = h f), read in the books.</p>
<h2>The moving picture</h2>
{player.html()}
<p>What to see: the front is round, not an octahedron. The six neighbours of a Node are the vertices of
the L1 unit ball (the grey diamond in the plane) and the pace c is the radius of its inscribed sphere
(the white circle); a row on a heading and a row on a diagonal reach the circle together, since each
direction's line is cut so that no direction outruns c. From the front inward the colour turns once around
the circle: the phase, an element of Z_{
        N
    }, drawn as a hue, one value per record. Where the fan's lines are sparse (far out,
between neighbouring directions) the Nodes are dark: the rows are on the digital lines and nowhere
else; nothing spreads sideways, and no Node holds anything between intervals.</p>
<h2>The readings</h2>
<table>
<tr><th>Reading</th><th>Kind</th><th>Value</th><th>Source</th></tr>
<tr><td>units released over the run</td><td>GameBoard (the books)</td><td class="num">{
        num(births_by_tick[-1])
    }</td><td><code>run.json</code>, <code>audit[-1].families.light.transit.released</code></td></tr>
<tr><td>units escaped through the faces</td><td>detector (the faces)</td><td class="num">{
        num(escaped_by_tick[-1])
    }</td><td><code>run.json</code>, <code>audit[-1].families.light.transit.escaped</code></td></tr>
<tr><td>units still in flight at the end</td><td>GameBoard (the books)</td><td class="num">{
        num(int(audit[-1]["families"]["light"]["transit"]["current"]))
    }</td><td><code>run.json</code>, <code>audit[-1].families.light.transit.current</code></td></tr>
<tr><td>the books balanced at every interval</td><td>GameBoard</td><td class="num">{
        record["conserved_at_every_completed_tick"]
    }</td><td><code>run.json</code>, <code>conserved_at_every_completed_tick</code></td></tr>
</table>
{
        sources(
            [
                ("the world", f"<code>{relative(world)}</code> (a demonstration world)"),
                (
                    "the run",
                    f"<code>run.json</code> and <code>events.jsonl</code> made by <code>python -m event_universe --init {relative(world)}</code>, {record['completed_ticks']} intervals",
                ),
                ("the source fingerprint", fingerprint_line(record)),
                (
                    "the frames",
                    "the world replayed in process through <code>NatureBeamSimulation</code>, the stores read at every drawn interval (a GameBoard reading, the host's view)",
                ),
                (
                    "the law",
                    '<a href="../../BEAM_LAW.md">the Beam Law</a>, section 3 (the flight table); <a href="../../THREE_WORLDS.md">the three worlds</a>',
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "beam",
        page(
            "The beam",
            "A lamp's rows spreading over the GameBoard on the digital lines of its fan, the phase as colour.",
            body,
        ),
    )


def ladder_html(gather: dict[str, object]) -> str:
    """The ladder of one record's click as a bar: the cells in order with
    their rungs (cumulative, out of N), and the wheel value u marked."""
    cells = gather["cells"]
    assert isinstance(cells, list)
    total = int(cells[-1][1])
    parts = []
    previous = 0
    for cell, rung in cells:
        name = html.escape(str(cell[0][0]))
        width = 100.0 * (int(rung) - previous) / total
        parts.append(
            f'<div style="flex: 0 0 {width:.2f}%; border-right: 1px solid var(--line); padding: 2px 4px; '
            f'overflow: hidden; white-space: nowrap; font-size: 0.8rem">{name}<br>&lt; {int(rung)}</div>'
        )
        previous = int(rung)
    u = int(gather["u"])  # type: ignore[arg-type]
    marker = 100.0 * (u + 0.5) / total
    chosen = html.escape(str(gather["chosen"][0][0]))  # type: ignore[index]
    return (
        f'<div style="position: relative; display: flex; border: 1px solid var(--line); border-radius: 6px; '
        f'background: var(--card)">{"".join(parts)}'
        f'<div style="position: absolute; left: {marker:.2f}%; top: -6px; bottom: -6px; width: 2px; '
        f'background: var(--accent)"></div></div>'
        f'<p class="kind">the record {gather["record"]} completed at the interval {gather["tick"]}: '
        f"u = {u}, the cell whose rung u falls under is {chosen}, the click lands there; the rungs are "
        f"b_k = (2 N C_k + T) // (2 T) over the cells' cumulative weights C_k, N = {total}</p>"
    )


@register("clicks")
def page_clicks(out: Path, runs: Path | None) -> Path:
    """(2) The clicks: a plate of pixels on the far side of a narrow beam,
    every record's one click landing on one pixel by the ladder and the
    wheel value u; the click list growing."""
    world = GALLERY_WORLDS / "clicks_plate.json"
    record_dir = runner_record(world, runs)
    record = read_json(record_dir / "run.json")
    events = scan_events(record_dir / "events.jsonl", ["gather", "birth", "record"])
    gathers = events["gather"]
    births = events["birth"]
    replay = Replay(world)
    ticks = frame_ticks(replay.ticks)
    frames = replay.run(ticks)
    plane = plane_for(replay, scale=10)
    plane.largest = largest_amounts(frames)
    pixels = [str(d.name) for d in replay.world.detectors]
    pixel_node = {str(d.name): tuple(int(c) for c in d.positions[0]) for d in replay.world.detectors}
    clicks_by_pixel_total = {name: 0 for name in pixels}
    for gather in gathers:
        clicks_by_pixel_total[str(gather["chosen"][0][0])] += 1  # type: ignore[index]
    largest_clicks = max(1, max(clicks_by_pixel_total.values()))
    pointer_by_tick: dict[tuple[int, str], tuple[int, int]] = {}
    for line in events["record"]:
        name = line.get("detector")
        if name is not None and "pointer" in line:
            pointer_by_tick[(int(line["tick"]), str(name))] = tuple(line["pointer"])  # type: ignore[arg-type]

    def decorate_for(tick: int) -> Callable[[ImageDraw.ImageDraw], None]:
        counts = {name: 0 for name in pixels}
        for gather in gathers:
            if int(gather["tick"]) <= tick:  # type: ignore[arg-type]
                counts[str(gather["chosen"][0][0])] += 1  # type: ignore[index]

        def decorate(draw: ImageDraw.ImageDraw) -> None:
            half = plane.scale / 2
            for name, node in pixel_node.items():
                cx, cy = plane.pixel(node[0], node[1])
                level = counts[name] / largest_clicks
                fill = (int(40 + 200 * level), int(120 + 120 * level), int(90 + 60 * level))
                if counts[name]:
                    draw.rectangle(
                        [cx - half + 1, cy - half + 1, cx + half - 2, cy + half - 2], fill=fill
                    )
                    draw.text(
                        (cx + half + 3, cy),
                        str(counts[name]),
                        fill=(230, 230, 230),
                        font=font(9),
                        anchor="lm",
                    )

        return decorate

    images = [plane.image(frame, decorate_for(frame.tick)) for frame in frames]
    readings = []
    for frame in frames:
        t = frame.tick
        done = [g for g in gathers if int(g["tick"]) <= t]  # type: ignore[arg-type]
        born = sum(1 for b in births if int(b["tick"]) <= t)  # type: ignore[arg-type]
        lines = {
            "records born (events.jsonl, birth lines)": num(born),
            "records completed, the clicks (events.jsonl, gather lines)": num(len(done)),
            "rows in flight (GameBoard reading)": num(int(frame.rows[0].amount.sum())),
        }
        if done:
            last = done[-1]
            lines["the last click"] = (
                f"record {last['record']}, u = {last['u']}, at {html.escape(str(last['chosen'][0][0]))} "  # type: ignore[index]
                f"(interval {last['tick']})"
            )
            counts = {}
            for g in done:
                name = str(g["chosen"][0][0])  # type: ignore[index]
                counts[name] = counts.get(name, 0) + 1
            lines["clicks per pixel so far"] = ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
        pointers = [
            (name, pointer_by_tick[(t, name)]) for name in pixels if (t, name) in pointer_by_tick
        ]
        if pointers:
            lines["the pointer (X, Y) per pixel this interval (record lines)"] = "; ".join(
                f"{name} ({x}, {y})" for name, (x, y) in pointers
            )
        readings.append(lines)
    player = Player(
        "clicks",
        images,
        ticks,
        readings,
        "The x-y plane, y upward, 10 pixels per Node; the rows of the beam coloured by their phase (the "
        "record's birth phase u) and their amount; the plate's pixels outlined in green, each filled and "
        "numbered by the clicks that landed on it so far (a detector reading, the gather lines).",
        duration_ms=100,
    )
    clicks_rows = "".join(
        f"<tr><td><code>{html.escape(name)}</code> at {pixel_node[name][:2]}</td>"
        f'<td class="num">{num(clicks_by_pixel_total[name])}</td>'
        f'<td class="num">{num(int(next(d for d in record["detectors"] if d["name"] == name)["families"]["light"]["clicks"]))}</td>'
        f'<td class="num">{num(int(next(d for d in record["detectors"] if d["name"] == name)["families"]["light"]["record"]))}</td></tr>'
        for name in pixels
        if clicks_by_pixel_total[name]
        or next(d for d in record["detectors"] if d["name"] == name)["families"]["light"]["clicks"]
    )
    click_list = "".join(
        f'<tr><td class="num">{g["tick"]}</td><td class="num">{g["record"]}</td><td class="num">{g["u"]}</td>'
        f"<td>{html.escape(str(g['chosen'][0][0]))} at {tuple(g['node'][0][:2])}</td>"  # type: ignore[index]
        f'<td class="num">{g["content"]}</td><td class="num">{tuple(g["momentum"])}</td></tr>'  # type: ignore[arg-type]
        for g in gathers
    )
    N = replay.world.phase_steps
    body = f"""
{demonstration_note(world)}
<h2>The GameBoard</h2>
<p>An open plane of {replay.world.shape[0]} x {
        replay.world.shape[1]
    } Nodes. A <b>lamp</b> of the paid family
<code>light</code> at Node (1, 5), the measured event number 1, content {num(1 << 25)} at K = {
        num(replay.world.K)
    }
(the turn 8 steps of N = {
        N
    } per self-creation; every unit costs 8 content, E = h f), releasing one unit per
self-creation on five directions within 5 degrees of +x: the heading (1, 0, 0) and (24, +-1, 0), (12, +-1, 0),
series K's narrow beam. Each self-creation births <b>one record</b> of five rows (one per direction, the
multiplicity 5), the record's birth phase u the lamp's count of births less one, modulo N. A <b>plate</b> of
eleven measured events of the paid family <code>apparatus</code> at x = 29, y = 0 .. 10, each declared as the
one-Node detector <code>plate_&lt;y&gt;</code> reading <code>wave</code> with the threshold 1: the pixels. A
paid arrival at a pixel is measured (the table the keys give): the row ends there and the record offers
that cell. The faces are open and take nothing here: every row of the beam ends on the plate.</p>
{
        legend(
            [
                ("a row of the beam, coloured by its record's birth phase u", '<i class="wheel"></i>'),
                ("the lamp (measured event 1)", swatch(BODY_COLOURS["light"])),
                (
                    "a pixel of the plate (a measured event of apparatus, a one-Node wave detector)",
                    swatch(BODY_COLOURS["apparatus"]),
                ),
            ]
        )
    }
<h2>Why this page</h2>
<p>"In our system there is something that spreads, the beam, and there are clicks, nothing else." The first page
showed the beam; this one shows the clicks: what a detector on the far side reads as records arrive, one click
per record, the list growing interval by interval and never shrinking. The arrow of time on the GameBoard is
this list: the flight and the collision are a bijection (the inverse interval exists), the click is the one
one-way step, a record that clicked is gone from everywhere and the list has one more line.</p>
<h2>The moving picture</h2>
{player.html()}
<p>What to see: the five rows of every record fly on their digital lines and reach the plate 28 Links away
after 48 intervals (the flight table: 32 Links in 55 intervals on the heading), ending on five neighbouring
pixels. The record is then complete and its one click is decided: the cells' weights are the squares of the
pointers of what ended at each pixel (equal here, one row per cell), the rungs are the cumulative weights
scaled to N = {
        N
    }, and the wheel value u, written on the record at its birth, selects the cell whose rung it
falls under. Since u advances by one per birth, the clicks walk over the five pixels in turn, and the counts
grow together: the Born weights, one click at a time.</p>
<h2>The threshold and the ladder of the first record</h2>
{ladder_html(gathers[0]) if gathers else "<p>No record completed.</p>"}
<p>The threshold of every pixel is T = 1 (the world file's <code>threshold</code>): the smallest amount arriving
over the set in one interval that the set responds to. The ladder above is the click's own threshold, the
one read-out of the law: the record's weight per cell, the rungs and u, from the <code>gather</code> line of
<code>events.jsonl</code>.</p>
<h2>The readings</h2>
<table>
<tr><th>Pixel</th><th>Clicks that landed here (gather lines)</th><th>Rows that ended here (<code>clicks</code> on the detector, run.json)</th><th>The cumulative record (X^2 + Y^2, run.json)</th></tr>
{clicks_rows}
</table>
<p>Every number in the table is a detector reading. The middle column counts the rows that ended at the pixel
(each record offers all five pixels); the first column counts the records whose one click landed there. The
records born over the run: {num(len(births))} (<code>birth</code> lines); completed: {
        num(len(gathers))
    }; the rest
are in flight at the end. The books balanced at every interval: {
        record["conserved_at_every_completed_tick"]
    }.</p>
<h2>The click list, the arrow of time</h2>
<table>
<tr><th>Interval</th><th>Record</th><th>u</th><th>Where the click landed</th><th>Content taken</th><th>Momentum **p** given (label units)</th></tr>
{click_list}
</table>
<p>For comparison, the catalog's placement world <code>examples/events/catalog/lamp_mirror_screen.json</code>
(a laser, a mirror, a wall with a slit, a screen of nineteen pixels; not an experiment) run as declared for 50
intervals completes 52 records, of which 25 click at the wall Node (10, 13) beside the slit, 25 at (12, 13)
and 2 at the screen pixel <code>screen_9</code>: the slit's fan offers the wall's neighbours first and with the
largest weight, so the far screen is rarely chosen there (its run's <code>gather</code> lines).</p>
{
        sources(
            [
                ("the world", f"<code>{relative(world)}</code> (a demonstration world)"),
                (
                    "the run",
                    f"<code>run.json</code> and <code>events.jsonl</code> made by <code>python -m event_universe --init {relative(world)}</code>, {record['completed_ticks']} intervals",
                ),
                ("the source fingerprint", fingerprint_line(record)),
                (
                    "the frames",
                    "the world replayed in process through <code>NatureBeamSimulation</code>, the stores read at every interval (a GameBoard reading)",
                ),
                (
                    "the law",
                    '<a href="../../BEAM_LAW.md">the Beam Law</a>, section 5 (the detector record) and note 37 (the one click); <a href="../../HIGHLIGHTS.md">Highlights</a> 5.7 (from a reading to a bit)',
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "clicks",
        page(
            "The clicks",
            "A plate on the far side of a beam clicking as records arrive: one click per record, the list growing.",
            body,
        ),
    )


@register("index")
def page_index(out: Path, runs: Path | None) -> Path:
    entries = [
        (
            "beam.html",
            "The beam",
            "a lamp's rows spreading on the digital lines of the fan, the phase as colour; the front against the circle of c and the L1 bound (a demonstration world)",
        ),
        (
            "clicks.html",
            "The clicks",
            "the catalog's optical bench: a laser, a mirror, a slit and a screen of pixels clicking as records arrive; the pointer per pixel and the click list growing (a registered placement world)",
        ),
        (
            "nucleus.html",
            "The nucleus",
            "series I: the deuteron bound at one Link, free at three, and the alpha square sheared apart; the strong rows' escape clicks at the lifetime (registered worlds)",
        ),
        (
            "decay.html",
            "The decay",
            "series J: a neutron family becoming another (the transformation become), the products' flight to the shell, the W exchange at one Link; the trigger ticks and counts from the register",
        ),
        (
            "collision.html",
            "The collision",
            "rows meeting at a Node permuted by the collision table: the head-on pair parks, turns and leaves; the classes of the group action (a demonstration world)",
        ),
        (
            "energy.html",
            "High-energy rows",
            "series K under the meeting: a beam of light passing a mass, bent toward it; the mass measuring the most turned rows (registered worlds)",
        ),
        (
            "worlds.html",
            "Our world",
            "the vector world, the software world and our world side by side for one record from its birth to its click, in the Mach-Zehnder world of the amplitude series (a registered world)",
        ),
    ]
    present = {path.name for path in out.glob("*.html")}
    items = "".join(
        f'<li><a href="{name}">{html.escape(title)}</a>: {html.escape(text)}</li>'
        if name in present or name == "index.html"
        else f"<li><b>{html.escape(title)}</b> (in preparation): {html.escape(text)}</li>"
        for name, title, text in entries
    )
    body = f"""
<p>The model owner, 2026-09-21 (translated): "a visualisation agent on a separate, strong machine, so
that one can see in beautiful HTML pages all the different situations we talk about: quarks, nucleons,
how something hits something and comes apart; the visualisation gives our world in simulations, in HTML
pages; it composes all the families, high-energy photons, all kinds of things that break them apart;
and it shows how it looks in our system, because in our system there is something that spreads, the
beam, and there are clicks, nothing else: beams and clicks, that is what we have; make it beautiful."</p>
<p>Every page plays the run inside the page (play, pause, a slider over the intervals, the interval
shown, the GIF as a link), draws the GameBoard with the world file's name of every thing on it, and
takes every number from the run's files or from the register, naming the path. The moving picture is a
GameBoard reading, the host's view; the clicks, the pointers and the pushes are detector readings, the
only kind reality has (<a href="../../EXPERIMENTS.md">the register</a>, "Two kinds of readings"). A
page made from a registered world says so and changes nothing in it; a page made from a demonstration
world says so and registers nothing. The quarks are not modelled today (the nucleon is a family,
<a href="../../ENTITY_CATALOG.md">the entity catalog</a>); a design is in preparation.</p>
<ul class="pages">{items}</ul>
<p>Two more pages are made on the Boss's machine and will be linked here when they are on main: how a
click looks (one record spreading, the click, the deletion) and Bell on the board.</p>
<p>The pages are written by <code>tools/gallery_pages.py</code> (<code>--page all</code> rewrites them
from the worlds and the runs); the demonstration worlds are in
<code>examples/events/gallery/</code>.</p>
"""
    return write_page(
        out,
        "index",
        page(
            "The visual gallery",
            "Beams and clicks, nothing else: the situations of the law, one page each, with the run playing inside the page.",
            body,
            index_link=False,
        ),
    )


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Write the pages of the visual gallery.")
    parser.add_argument("--page", default="all", help="one of " + ", ".join(PAGES) + ", or all")
    parser.add_argument("--out", type=Path, default=ROOT / "docs" / "pages" / "gallery")
    parser.add_argument(
        "--runs", type=Path, default=None, help="keep and reuse the runner's records here"
    )
    args = parser.parse_args(argv)
    names = (
        [name for name in PAGES if name != "index"] + ["index"] if args.page == "all" else [args.page]
    )
    for name in names:
        if name not in PAGES:
            parser.error(f"unknown page {name!r}; one of {', '.join(PAGES)}")
        path = PAGES[name](args.out, args.runs)
        print(f"{path} ({path.stat().st_size / 1e6:.2f} MB)")
    if args.page != "all" and args.page != "index":
        path = PAGES["index"](args.out, args.runs)
        print(f"{path} ({path.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
