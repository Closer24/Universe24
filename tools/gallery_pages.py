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
import itertools
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
# The helpers (the bodies, their copies, the arrows, the outlines) are drawn
# at this factor of the size and downsampled: sharp over the blocky board.
SUPERSAMPLE = 4
# The three-dimensional players turn the cube once over this many frames.
TURN_FRAMES = 150
# The accent of the pages: green, in dark mode (the model owner, 2026-09-21).
# A body's copies fade with their age over this many intervals: the rows
# just released into the Nodes beside the body are the bright ones.
AGE_FADE = 40
ACCENT = (74, 222, 128)
# Appended to the caption of every picture with bodies (the model owner,
# 2026-09-21: a body's copies spreading, transparent, and its arrow).
COPIES_NOTE = (
    "Every body is drawn with the copies, in the owner's word: the body's own rows, the rows carrying its "
    "number that its self-creations release on its directions, drawn as translucent discs in its colour at "
    "their Nodes on the GameBoard; and with the white arrow of its momentum label, the vector p of its record "
    "(no arrow at p = 0); a product row carries a short arrow along its direction of the fan. The copies "
    "fade with their age: the bright ones are the rows just released into the Nodes beside the body, the "
    "faint ones far along their lines; every particle is a beam, releasing itself at every self-creation. A "
    "copy looks like its body: a disc with a rim, coloured as the body is (by the row's phase for a family "
    "with a phase circle): the body radiates itself."
)
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
    "u": (255, 150, 60),
    "e": (110, 225, 255),
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


def brightness(amount: np.ndarray, largest: float, floor: float = 0.35) -> np.ndarray:
    """A visible floor and a logarithmic rise: colour is not a linear
    measurement of the amount."""
    largest = max(float(largest), 1.0)
    return floor + (1.0 - floor) * np.log2(1.0 + amount) / math.log2(1.0 + largest)


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
    body_radius: float = 0.55
    body_labels: bool = True
    # The brightness floor of a lit Node, and per family a weight on its
    # layer; a family named `on_top` is drawn opaque over the others where
    # it has rows (the strong rows under a dense fan).
    floor: float = 0.35
    weights: dict[str, float] = field(default_factory=dict)
    on_top: str | None = None
    # Draw only the bodies at this z (a shell of readers projected would
    # cover the plane); None draws every body.
    body_slice_z: int | None = None
    # The world's direction table, for the arrows on the rows of the
    # families in `arrow_families` (a few rows: the products, the beam).
    directions: list[tuple[int, int, int]] = field(default_factory=list)
    arrow_families: set[str] = field(default_factory=set)
    # A body's copies: its own rows (the rows carrying its number) drawn as
    # translucent discs in its colour, spreading in every direction; and
    # the arrow of its momentum vector p.
    copies: bool = True
    # The families whose bodies are coloured by their phase (the electron
    # turning its phase by its momentum).
    phase_bodies: set[str] = field(default_factory=set)

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
        value = brightness(total, self.largest.get(rows.family, float(total.max())), self.floor)
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
        """The board at its Node resolution (blocky: one cell per Node), and
        over it the helpers, sharp: the detector outlines, the bodies'
        copies, the bodies, the arrows, drawn at SUPERSAMPLE times the size
        and downsampled (the model owner, 2026-09-21: the board may be
        pixelated, the helpers sharp and beautiful)."""
        image, draw = self.canvas()
        nx, ny, _ = self.shape
        rgb = np.zeros((nx, ny, 3), dtype=np.float64)
        top: np.ndarray | None = None
        for rows in frame.rows:
            layer = self.layer(rows)
            if rows.family == self.on_top:
                top = layer
                continue
            rgb += layer * self.weights.get(rows.family, 1.0)
        rgb = np.clip(rgb, 0.0, 1.0)
        if top is not None:
            lit_top = top.sum(axis=2) > 0
            rgb[lit_top] = top[lit_top]
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
        k = SUPERSAMPLE
        overlay = Image.new("RGBA", (image.width * k, image.height * k), (0, 0, 0, 0))
        over = ImageDraw.Draw(overlay)
        for node in self.detector_nodes:
            if self.slice_z is not None and node[2] != self.slice_z:
                continue
            if self.body_slice_z is not None and node[2] != self.body_slice_z:
                continue
            cx, cy = self.pixel(node[0], node[1])
            half = self.scale / 2
            over.rectangle(
                [(cx - half) * k, (cy - half) * k, (cx + half - 1) * k, (cy + half - 1) * k],
                outline=(*ACCENT, 220),
                width=max(1, k // 2),
            )
        if self.copies:
            self.draw_copies(over, frame, k)
        radius = max(self.scale * self.body_radius, 3.0)
        for body in frame.bodies:
            if self.body_slice_z is not None and body.position[2] != self.body_slice_z:
                continue
            cx, cy = self.pixel(body.position[0], body.position[1])
            colour = BODY_COLOURS.get(body.family, (230, 230, 230))
            if body.family in self.phase_bodies:
                colour = phase_colour(body.phase, self.phase_steps)
            # A soft glow, then the disc with a thin light rim.
            glow = radius * 1.9
            over.ellipse(
                [(cx - glow) * k, (cy - glow) * k, (cx + glow) * k, (cy + glow) * k],
                fill=(*colour, 55),
            )
            over.ellipse(
                [(cx - radius) * k, (cy - radius) * k, (cx + radius) * k, (cy + radius) * k],
                fill=(*colour, 255),
                outline=(245, 245, 245, 255),
                width=max(1, k // 2),
            )
            if self.body_labels and self.scale >= 12:
                over.text(
                    (cx * k, cy * k),
                    body.family[:2],
                    fill=(0, 0, 0, 255),
                    font=font(max(8, int(self.scale * 0.7)) * k),
                    anchor="mm",
                )
            self.draw_momentum(over, body, cx, cy, radius, k)
        for rows in frame.rows:
            if rows.family in self.arrow_families:
                self.draw_row_arrows(over, rows, k)
        overlay = overlay.resize(image.size, Image.LANCZOS)
        image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
        if decorate is not None:
            decorate(ImageDraw.Draw(image))
        return image

    def draw_copies(self, over: ImageDraw.ImageDraw, frame: Frame, k: int) -> None:
        """The copies of every body (the owner's word): the body's own rows,
        the rows carrying its number that its self-creations release on its
        directions, drawn as translucent discs in the body's colour at their
        Nodes; what spreads is the body's own record, many times over."""
        nx, ny, _ = self.shape
        base = max(self.scale * 0.46, 2.0)
        for body in frame.bodies:
            colour = BODY_COLOURS.get(body.family, (230, 230, 230))
            total = np.zeros((nx, ny), dtype=np.float64)
            youngest = np.full((nx, ny), AGE_FADE * 4, dtype=np.float64)
            for rows in frame.rows:
                mine = rows.number == body.number
                if self.slice_z is not None:
                    mine &= rows.z == self.slice_z
                if not mine.any():
                    continue
                np.add.at(total, (rows.x[mine], rows.y[mine]), rows.amount[mine].astype(np.float64))
                np.minimum.at(youngest, (rows.x[mine], rows.y[mine]), rows.age[mine].astype(np.float64))
            if not total.any():
                continue
            largest = float(total.max())
            # A copy looks like the body itself: for a family with a phase
            # circle, the youngest row's phase at the Node gives the copy's
            # hue, as the body's own disc is coloured by its phase.
            phase_at: dict[tuple[int, int], int] = {}
            if self.phased.get(body.family, False):
                for rows in frame.rows:
                    mine = rows.number == body.number
                    if self.slice_z is not None:
                        mine &= rows.z == self.slice_z
                    order = np.argsort(rows.age[mine], kind="stable")
                    xs, ys, phases = rows.x[mine][order], rows.y[mine][order], rows.phase[mine][order]
                    for x, y, phase in zip(xs.tolist(), ys.tolist(), phases.tolist(), strict=True):
                        phase_at.setdefault((x, y), phase)
            for i, j in zip(*np.nonzero(total), strict=True):
                if (int(i), int(j)) == (body.position[0], body.position[1]):
                    continue
                # The rows just released, in the Nodes beside the body, are
                # bright and large; the rows far along their lines faint.
                fade = 0.3 + 0.7 * max(0.0, 1.0 - youngest[i, j] / AGE_FADE)
                alpha = int((30 + 100 * math.log2(1.0 + total[i, j]) / math.log2(1.0 + largest)) * fade)
                radius = base * (0.72 + 0.38 * fade)
                cx, cy = self.pixel(int(i), int(j))
                tint = colour
                if (int(i), int(j)) in phase_at:
                    tint = phase_colour(phase_at[(int(i), int(j))], self.phase_steps)
                over.ellipse(
                    [(cx - radius) * k, (cy - radius) * k, (cx + radius) * k, (cy + radius) * k],
                    fill=(*tint, alpha),
                    outline=(235, 240, 245, min(255, alpha + 70)),
                    width=max(1, k // 4),
                )

    def draw_momentum(
        self, over: ImageDraw.ImageDraw, body: Body, cx: float, cy: float, radius: float, k: int
    ) -> None:
        """The arrow of the body's momentum label, the vector p of its
        record, in the plane: where the body travels; no arrow at p = 0."""
        px, py = body.momentum[0], body.momentum[1]
        if px == 0 and py == 0:
            return
        length = max(1.8 * self.scale, 14.0)
        norm = math.hypot(px, py)
        ux, uy = px / norm, -py / norm
        arrow(over, (cx + ux * radius, cy + uy * radius), (ux, uy), length, max(2.0, self.scale / 5), k)

    def draw_row_arrows(self, over: ImageDraw.ImageDraw, rows: Rows, k: int) -> None:
        """A short arrow per row along its direction of the fan, for a family
        of a few rows (a product, a beam)."""
        for j in range(rows.amount.size):
            if self.slice_z is not None and int(rows.z[j]) != self.slice_z:
                continue
            d = self.directions[int(rows.direction[j])] if self.directions else (0, 0, 0)
            if d[0] == 0 and d[1] == 0:
                continue
            norm = math.hypot(d[0], d[1])
            ux, uy = d[0] / norm, -d[1] / norm
            cx, cy = self.pixel(int(rows.x[j]), int(rows.y[j]))
            arrow(over, (cx, cy), (ux, uy), max(self.scale * 1.3, 9.0), max(1.5, self.scale / 6), k)


def arrow(
    over: ImageDraw.ImageDraw,
    start: tuple[float, float],
    unit: tuple[float, float],
    length: float,
    width: float,
    k: int,
) -> None:
    """An arrow in the accent colour with a dark halo, drawn at k times the
    size on the overlay: the shaft and a filled head."""
    ux, uy = unit
    tip = (start[0] + ux * length, start[1] + uy * length)
    head = max(4.0, width * 2.6)
    base = (tip[0] - ux * head, tip[1] - uy * head)
    left = (base[0] - uy * head * 0.55, base[1] + ux * head * 0.55)
    right = (base[0] + uy * head * 0.55, base[1] - ux * head * 0.55)
    for colour, extra in (((10, 12, 18, 200), width * 1.2), ((*ACCENT, 255), 0.0)):
        over.line(
            [(start[0] * k, start[1] * k), (base[0] * k, base[1] * k)],
            fill=colour,
            width=int((width + extra) * k),
        )
        over.polygon(
            [(tip[0] * k, tip[1] * k), (left[0] * k, left[1] * k), (right[0] * k, right[1] * k)],
            fill=colour,
            outline=colour,
            width=int(extra * k),
        )


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
        """Drawn at SUPERSAMPLE times the size and downsampled: sharp."""
        k = SUPERSAMPLE
        scale, margin = self.scale, self.margin
        self.scale, self.margin = scale * k, margin * k
        try:
            large = self.draw_scene(frame, highlight)
        finally:
            self.scale, self.margin = scale, margin
        return large.resize(self.size, Image.LANCZOS)

    def draw_scene(self, frame: Frame, highlight: tuple[int, int, int] | None = None) -> Image.Image:
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
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ACCENT, width=max(2, self.scale // 8))
        radius = self.scale * 0.32
        for rows in frame.rows:
            order = np.argsort(rows.z, kind="stable")
            for k in order:
                x, y, z = int(rows.x[k]), int(rows.y[k]), int(rows.z[k])
                colour = phase_colour(int(rows.phase[k]), self.phase_steps)
                d = self.directions[int(rows.direction[k])]
                # The disc displaced a third of a Link toward its heading (a
                # rest slot sideways by its index) so that the rows of one
                # Node stay apart.
                shift = (
                    (0.3 * d[0], 0.3 * d[1], 0.3 * d[2])
                    if any(d)
                    else ((-0.2, 0.0, 0.0) if int(rows.direction[k]) == 0 else (0.2, 0.0, 0.0))
                )
                cx, cy = self.project(x + shift[0], y + shift[1], z + shift[2])
                draw.ellipse(
                    [cx - radius, cy - radius, cx + radius, cy + radius],
                    fill=colour,
                    outline=(255, 255, 255),
                )
                if any(d):
                    ex, ey = self.project(x + 0.9 * d[0], y + 0.9 * d[1], z + 0.9 * d[2])
                    draw.line([(cx, cy), (ex, ey)], fill=ACCENT, width=max(2, self.scale // 8))
        return image


# ---------------------------------------------------------------------------
# The GIF, the sprite sheet and the page


def gif_bytes(images: Sequence[Image.Image], duration_ms: int, colours: int = 96) -> bytes:
    palettes = [image.quantize(colors=colours, method=Image.Quantize.MEDIANCUT) for image in images]
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


def sprite_sheet(images: Sequence[Image.Image], colours: int = 128) -> tuple[bytes, int, int, int]:
    """One PNG holding every frame in a grid; (png, columns, width, height)."""
    w, h = images[0].size
    columns = max(1, min(len(images), int(math.ceil(math.sqrt(len(images) * h / max(w, 1))))))
    rows = int(math.ceil(len(images) / columns))
    sheet = Image.new("RGB", (columns * w, rows * h), (14, 16, 24))
    for k, image in enumerate(images):
        sheet.paste(image, ((k % columns) * w, (k // columns) * h))
    buffer = io.BytesIO()
    sheet.quantize(colors=colours, method=Image.Quantize.MEDIANCUT).save(
        buffer, format="PNG", optimize=True
    )
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
    # Optional: per frame a list of (title, html) panels drawn side by side
    # under the readings (the three worlds page).
    panels: Sequence[Sequence[tuple[str, str]]] | None = None
    # The palette of the sprite sheet and the GIF (fewer colours: a smaller page).
    colours: int = 128

    def html(self) -> str:
        png, columns, w, h = sprite_sheet(self.images, self.colours)
        gif = gif_bytes(self.images, self.duration_ms, min(self.colours, 96))
        data = {
            "columns": columns,
            "width": w,
            "height": h,
            "count": len(self.images),
            "ticks": list(self.ticks),
            "readings": list(self.readings),
            "duration": self.duration_ms,
            "panels": [list(map(list, frame)) for frame in self.panels] if self.panels else None,
        }
        return f"""
<figure class="player" id="{self.key}">
  <img class="gif" alt="the moving picture" src="{data_url(gif, "image/gif")}">
  <canvas width="{w}" height="{h}" aria-label="the moving picture" hidden></canvas>
  <div class="controls" hidden>
    <button class="play" type="button">Play</button>
    <input class="slider" type="range" min="0" max="{len(self.images) - 1}" value="0">
    <span class="tick">interval 0</span>
  </div>
  <dl class="readings"></dl>
  <div class="three"></div>
  <figcaption>{self.caption} <a class="gif" download="{self.key}.gif">The GIF</a> (the frames at
  {self.duration_ms} ms; {len(self.images)} frames; the GIF plays by itself, the player with its slider needs
  scripts enabled).</figcaption>
  <script type="application/json" class="frames">{json.dumps(data)}</script>
  <img class="sheet" alt="" src="{data_url(png, "image/png")}" hidden>
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
  var panels = figure.querySelector('div.three');
  var gif = figure.querySelector('img.gif');
  figure.querySelector('a.gif').href = gif.src;
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
    if (data.panels) {
      panels.innerHTML = (data.panels[k] || []).map(function (panel) {
        return '<section><h3>' + panel[0] + '</h3>' + panel[1] + '</section>';
      }).join('');
    }
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
  function start() {
    gif.hidden = true;
    canvas.hidden = false;
    figure.querySelector('div.controls').hidden = false;
    show(0);
  }
  if (sheet.complete) { start(); } else { sheet.addEventListener('load', start); }
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
    --accent: #4ade80; --accent-ink: #0b1a10; --board: #0e1018; --good: #7fcf9a;
  }
}
:root[data-theme="dark"] {
  --bg: #0f1114; --ink: #e8ecef; --muted: #9aa5ad; --line: #262b33; --card: #171a1f;
  --accent: #4ade80; --accent-ink: #0b1a10; --board: #0e1018; --good: #7fcf9a;
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
figure.player img.gif { display: block; max-width: 100%; height: auto; margin: 0 auto; border-radius: 4px; }
figure.player img.gif[hidden], figure.player canvas[hidden], figure.player div.controls[hidden] { display: none; }
figure.player canvas { display: block; max-width: 100%; height: auto; margin: 0 auto; background: var(--board); border-radius: 4px; }
figure.player .controls { display: flex; gap: 12px; align-items: center; margin: 10px 0 4px; }
figure.player input.slider { flex: 1; accent-color: var(--accent); }
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
.note { font-size: 0.85rem; color: var(--muted); margin: 6px 0 0; }
.demo { background: var(--card); border-left: 4px solid var(--accent); padding: 8px 12px; margin: 12px 0; }
figure.player div.three:empty { display: none; }
.three { display: grid; margin-top: 10px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }
.three section { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; min-height: 120px; }
.three h3 { margin: 0 0 6px; font-size: 1.05rem; }
.three pre { font-size: 0.8rem; white-space: pre-wrap; margin: 0; font-family: "DejaVu Sans Mono", Menlo, Consolas, monospace; }
ul.pages li { margin: 8px 0; }
.formula section ol { padding-left: 1.2em; margin: 4px 0; }
.formula section li { margin: 2px 0; font-size: 0.95rem; }
.formula section div { font-size: 0.95rem; }
.formula section pre { font-size: 0.85rem; white-space: pre-wrap; margin: 6px 0; font-family: "DejaVu Sans Mono", Menlo, Consolas, monospace; color: var(--accent); }
table.map td, table.map th { font-size: 0.85rem; }
section.big { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 20px 16px; margin: 16px 0 24px; text-align: center; }
section.big pre.formula { font-size: 2.2rem; line-height: 1.3; }
section.big pre.formula.small-caps { font-size: 1.35rem; }
pre.formula { font-family: "DejaVu Sans Mono", Menlo, Consolas, monospace; color: var(--accent); white-space: pre-wrap; margin: 8px 0; }
.smalls { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.smalls section { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; }
.smalls h3 { margin: 0 0 4px; font-size: 1.05rem; }
.smalls pre.formula { font-size: 1.1rem; }
.smalls p { font-size: 0.92rem; margin: 4px 0; }
table.compare td.ours { color: var(--good); }
math { font-family: "Latin Modern Math", "STIX Two Math", "Cambria Math", "Noto Sans Math", "DejaVu Serif", serif; color: var(--accent); }
math[display="block"] { padding: 4px 10px; box-sizing: border-box; }
section.big math { font-size: 2.4rem; margin: 10px 0; }
section.big .conditions math { font-size: 1.4rem; margin: 4px 0; }
math[display="block"] { max-width: 100%; overflow-x: auto; }
.scroll { overflow-x: auto; }
.who { display: inline-block; font: 0.72rem/1.4 Georgia, serif; letter-spacing: 0.06em; text-transform: uppercase; padding: 1px 8px; border-radius: 999px; border: 1px solid; margin: 0 0 4px; }
.who.law { color: var(--accent); border-color: var(--accent); }
.who.newton { color: #f0a050; border-color: #f0a050; }
.who.lorentz { color: #c79cff; border-color: #c79cff; }
.who.einstein { color: #6cb4ff; border-color: #6cb4ff; }
.who.planck, .who.doppler { color: #b8b8c8; border-color: #b8b8c8; }
section.big.theirs-box math { color: #6cb4ff; font-size: 1.8rem; }
.owners { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; }
.owners section { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; }
.owners h3 { margin: 0 0 6px; font-size: 1rem; }
.owners ul { padding-left: 1.1em; margin: 4px 0; }
.owners li { font-size: 0.9rem; margin: 3px 0; }
.story { display: grid; gap: 12px; }
.story .step { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 10px 14px; }
.story h3 { margin: 0 0 6px; font-size: 1.05rem; }
.story .pair { display: grid; grid-template-columns: 1fr auto 1fr; gap: 12px; align-items: center; }
.story .pair > div, .story .step, .owners section, .smalls section { min-width: 0; }
.story .arrow { font-size: 1.6rem; color: var(--muted); transform: rotate(-90deg); }
.story .theirs math { color: #6cb4ff; }
.story math { font-size: 1.3rem; margin: 6px 0; }
.story p { font-size: 0.9rem; margin: 4px 0; }
.story p.status { border-top: 1px solid var(--line); padding-top: 6px; margin-top: 8px; }
@media (max-width: 640px) { .story .pair { grid-template-columns: 1fr; } .story .arrow { transform: none; text-align: center; } }
.deriveds { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
.deriveds section { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; }
.deriveds h3 { margin: 0 0 4px; font-size: 1.05rem; }
.deriveds math { font-size: 1.45rem; margin: 8px 0; }
.deriveds p { font-size: 0.92rem; margin: 4px 0; }
@media (max-width: 600px) { section.big math { font-size: 1.7rem; } section.big .conditions math { font-size: 1.15rem; } section.big.theirs-box math { font-size: 1.35rem; } }
details summary { cursor: pointer; color: var(--accent); margin: 12px 0; }
@media (max-width: 600px) { section.big pre.formula { font-size: 1.5rem; } section.big pre.formula.small-caps { font-size: 1rem; } }
td.reached { color: var(--good); white-space: nowrap; }
td.different { color: #e0b44a; }
td.missing { color: #f08080; }
"""


def page(title: str, lead: str, body: str, *, index_link: bool = True, head: str = "") -> str:
    crumbs = (
        '<nav class="crumbs"><a href="index.html">The gallery</a> · <a href="../../README.md">The documentation</a></nav>'
        if index_link
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{head}<style>{STYLE}</style>
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


def family_legend(replay: Replay) -> list[tuple[str, str]]:
    """One legend entry per family of the world: the wheel for a family with
    a phase circle (drawn by its phase), its colour otherwise."""
    entries = []
    for i, family in enumerate(replay.world.families):
        if family.phase:
            entries.append((f"the {family.name} rows, coloured by their phase", '<i class="wheel"></i>'))
        else:
            entries.append((f"the {family.name} rows", swatch(FAMILY_COLOURS[i % len(FAMILY_COLOURS)])))
    return entries


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
        directions=list(replay.directions),
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


def followed_record(frame: Frame, first: int, first_gather: int) -> int | None:
    """The record the three-worlds page follows at a frame: the first
    record until its click, then the youngest record alive."""
    if frame.tick <= first_gather:
        return first
    alive = [int(r) for rows in frame.rows for r in rows.record if int(r) != 0]
    return max(alive) if alive else None


@register("worlds")
def page_worlds(out: Path, runs: Path | None) -> Path:
    """(7) Our world: the vector world, the software world and our world
    side by side for one record from its birth to its click, on the
    registered Mach-Zehnder world with equal arms."""
    world = WORLDS / "amplitude" / "mz_equal.json"
    record_dir = runner_record(world, runs)
    record = read_json(record_dir / "run.json")
    events = scan_events(
        record_dir / "events.jsonl", ["birth", "split", "cancel", "click", "record", "gather"]
    )
    replay = Replay(world)
    N = replay.world.phase_steps
    ticks = frame_ticks(replay.ticks)
    frames = replay.run(ticks)
    plane = plane_for(replay, scale=44)
    plane.largest = largest_amounts(frames)
    plane.body_radius = 0.26
    plane.body_labels = False
    plane.margin = 18
    directions = replay.directions
    first = int(events["birth"][0]["record"])  # type: ignore[arg-type]
    first_gather = next(int(g["tick"]) for g in events["gather"] if int(g["record"]) == first)  # type: ignore[arg-type]
    by_record: dict[int, dict[str, list[dict[str, object]]]] = {}
    for kind in ("birth", "split", "cancel", "click", "gather"):
        for line in events[kind]:
            key = "of" if kind == "record" else "record"
            by_record.setdefault(int(line[key]), {}).setdefault(kind, []).append(line)  # type: ignore[arg-type]
    for line in events["record"]:
        by_record.setdefault(int(line["of"]), {}).setdefault("record", []).append(line)  # type: ignore[arg-type]
    names = {int(m.number): m for m in replay.simulation.measured.values()}
    labels = {1: "the lamp", 2: "mirror 1", 3: "mirror 2", 4: "the splitter", 5: "D1", 6: "D2"}

    def ring_for(followed: int | None) -> Callable[[ImageDraw.ImageDraw], None]:
        def decorate(draw: ImageDraw.ImageDraw) -> None:
            for number, label in labels.items():
                body = names[number]
                cx, cy = plane.pixel(body.position[0], body.position[1])
                draw.text(
                    (cx, cy + plane.scale * 0.62),
                    label,
                    fill=(235, 235, 235),
                    font=font(11),
                    anchor="mm",
                )
            if followed is None:
                return
            for rows in current_frame.rows:
                for k in range(rows.amount.size):
                    if int(rows.record[k]) == followed:
                        cx, cy = plane.pixel(int(rows.x[k]), int(rows.y[k]))
                        r = plane.scale * 0.5 - 2
                        draw.rectangle(
                            [cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2
                        )

        return decorate

    images = []
    panels = []
    readings = []
    for current_frame in frames:
        t = current_frame.tick
        followed = followed_record(current_frame, first, first_gather)
        images.append(plane.image(current_frame, ring_for(followed)))
        rows_of: list[tuple[int, ...]] = []
        for rows in current_frame.rows:
            for k in range(rows.amount.size):
                if followed is not None and int(rows.record[k]) == followed:
                    rows_of.append(
                        (
                            int(rows.x[k]),
                            int(rows.y[k]),
                            int(rows.z[k]),
                            int(rows.direction[k]),
                            int(rows.age[k]),
                            int(rows.phase[k]),
                            int(rows.amount[k]),
                            int(rows.number[k]),
                            int(rows.multiplicity[k]),
                            int(rows.birth[k]),
                        )
                    )
        lines = by_record.get(followed, {}) if followed is not None else {}
        gathered = [g for g in lines.get("gather", []) if int(g["tick"]) <= t]  # type: ignore[arg-type]
        clicks_so_far = {"D1": 0, "D2": 0}
        for g in events["gather"]:
            if int(g["tick"]) <= t:  # type: ignore[arg-type]
                clicks_so_far[str(g["chosen"][0][0])] += 1  # type: ignore[index]
        # The vector world: the rows as points of the product of circles and
        # lines, the record as the vector f at the ports.
        if followed is None:
            vector = "<p>No record alive.</p>"
        elif rows_of:
            vector = (
                "<pre>"
                + "\n".join(
                    f"row: Node ({x}, {y}), direction {directions[d]}, phase {ph} of Z_{N}, age {a}, amount {m}, number {n}"
                    for x, y, _, d, a, ph, m, n, _, _ in rows_of
                )
                + "</pre>"
            )
            vector += (
                f'<p class="note">the record\'s identity {followed}, its birth phase u = {rows_of[0][9]}, '
                f"its multiplicity m = {rows_of[0][8]} (the paths so far); the record is one element of "
                f"Z[Z_{N}] per end Node: the amounts that ended at each phase</p>"
            )
        elif gathered:
            g = gathered[-1]
            ports = [r for r in lines.get("record", []) if int(r["tick"]) == int(g["tick"])]  # type: ignore[arg-type]
            vector = (
                "<pre>"
                + "\n".join(
                    f"f at {r['detector']}: pointer (X, Y) = {tuple(r['pointer'])}, the square X^2 + Y^2 = {r['record']}"  # type: ignore[arg-type]
                    for r in ports
                )
                + "</pre>"
            )
            vector += (
                f'<p class="note">the weight of each cell is the bilinear form f^T G f (the square of the pointer); '
                f"the rungs over the cells' cumulative weights: {', '.join(str(c[0][0][0]) + ' < ' + str(c[1]) for c in g['cells'])}; "  # type: ignore[index]
                f"u = {g['u']} selects {g['chosen'][0][0]}; the record is then translated to nothing: deleted everywhere</p>"
            )  # type: ignore[index]
        else:
            vector = "<p>The record has clicked and is gone: the state vector no longer holds it.</p>"
        # The software world: the store's columns, the int64 fields as they are.
        if rows_of:
            body_rows = "\n".join(
                f"node {x * 5 + y} (x {x}, y {y}) | direction {d} | age {a} | phase {ph} | number {n} | "
                f"amount {m} | content {m} | record {followed} | branch 0 | multiplicity {mu} | birth {u}"
                for x, y, _, d, a, ph, m, n, mu, u in rows_of
            )
            software = (
                f'<pre>{body_rows}</pre><p class="note">NatureBeamStore.light, one int64 row per row: '
                f"node the packed index x * 5 + y, direction an index into the world's direction table, "
                f"content per unit the family's quantum 1, birth the wheel value u</p>"
            )
        elif gathered:
            g = gathered[-1]
            software = (
                f"<pre>gather line, events.jsonl, tick {g['tick']}:\n  record {g['record']}, u {g['u']}, chosen {g['chosen'][0][0]},\n"  # type: ignore[index]
                f"  weight {g['weight']}, total {g['total']} (the unit 2^58),\n  cells {json.dumps(g['cells'])}\n"
                f"click line: D1 amount 41, phase 16, content 41, push [2624, 0, 0]</pre>"
                f"<p class=\"note\">Layer.complete (amplitude.py) removed the record from the layer's table and NatureBeamStore.merge dropped its rows; DetectorSet.record of D1 grew by the square; the books moved by the click's content and momentum</p>"
            )
        else:
            software = "<p>No row of this record in the store.</p>"
        # Our world: what the two detectors read.
        if gathered and followed == first:
            ours = (
                f"<p><b>D1 clicked</b> at the interval {gathered[-1]['tick']}: one photon arrived at (4, 3). D2 did not click. "
                f"Nothing else of this photon was ever seen: not its two arms, not its phases, not the 41 rows that merged.</p>"
            )
        elif followed == first:
            ours = (
                "<p>Nothing yet. The photon is on its way, unseen: a detector reads only the click.</p>"
            )
        else:
            ours = "<p>The later photons repeat the story: each is seen once, at D1.</p>"
        ours += (
            f"<p>The click list so far: D1 {clicks_so_far['D1']}, D2 {clicks_so_far['D2']} (the gather lines up to this interval). "
            f"The register's pinned reading over the first 64 births: D1 64, D2 0 (<code>examples/events/amplitude/expectations.json</code>, <code>mach_zehnder.mz_equal.clicks</code>).</p>"
        )
        panels.append(
            [("The vector world", vector), ("The software world", software), ("Our world", ours)]
        )
        readings.append(
            {
                "the record followed": str(followed) if followed is not None else "none",
                "records completed so far (gather lines)": num(
                    len([g for g in events["gather"] if int(g["tick"]) <= t])
                ),  # type: ignore[arg-type]
                "rows in the store (GameBoard reading)": num(
                    int(sum(int(r.amount.size) for r in current_frame.rows))
                ),
            }
        )
    player = Player(
        "worlds",
        images,
        ticks,
        readings,
        "The 5 x 5 plane, 44 pixels per Node; every Node with rows coloured by their phase and amount; the "
        "rows of the followed record ringed in white; the lamp, the mirrors, the splitter and the ports labelled "
        "by the world file's numbers.",
        duration_ms=350,
        panels=panels,
    )
    entry = "L, the amplitude law (2026-09-20)"
    body = f"""
{registered_note(world, entry, "../../EXPERIMENTS.md#l-the-amplitude-law-2026-09-20")}
<h2>The GameBoard</h2>
<p>The Mach-Zehnder world with equal arms of the amplitude series (L1): a plane of 5 x 5 with z periodic, K =
{num(replay.world.K)}, N = {
        N
    }. <b>The lamp</b> at (0, 0), measured event 1, content 2^20 at K 2^20 (the turn one
step per self-creation, each birth paying 2 content), births one record per self-creation of two rows of
amount 1, +x (arm 1) and +y (arm 2, the reflection's quarter turn 16 on the row), the multiplicity 2.
<b>Mirror 1</b> at (3, 0), measured event 2, re-emits +x arrivals on +y; <b>mirror 2</b> at (0, 3), event
3, re-emits +y arrivals on +x. <b>The splitter</b> at (3, 3), event 4, a <code>rerelease</code> whose
weights (20, 21) and turns are selected by the arrival's direction. <b>D1</b> at (4, 3), event 5, and
<b>D2</b> at (3, 4), event 6, are one-Node detectors reading <code>sum</code>: the record's own pointer over
its lifetime, the one click at its completion.</p>
{
        legend(
            [
                ("a row, coloured by its phase on the circle", '<i class="wheel"></i>'),
                (
                    "the lamp, the mirrors, the splitter, the ports: measured events of light",
                    swatch(BODY_COLOURS["light"]),
                ),
                (
                    "the rows of the followed record",
                    '<i class="swatch" style="background: none; border: 2px solid #fff"></i>',
                ),
            ]
        )
    }
<h2>Why this page</h2>
<p>The owner asked (<a href="../../THREE_WORLDS.md">the three worlds</a>): "let there be precise definitions
between what a thing is in the vector world, what it is in the software world and what it is in our world; a
click, for us, is a sampling of the game engine that yields a number, and it does an operation in the engine,
a vector operation, and an operation in our world". This page follows one record, the first the lamp births,
from its birth to its click, and shows at every interval the same thing three times: as integer vectors on
tori and the operations of the map <b>F</b>; as the int64 columns of the store and the lines of the record;
and as what a detector reads, which is a click and nothing else. Beams and clicks: in the vector world the
beam is a set of points moving by translation, split by an integer matrix, added in the group ring; in the
software world it is rows of a store; in our world it is nothing until the click.</p>
<h2>The moving picture, the three worlds beside it</h2>
{player.html()}
<p>What to see, interval by interval. At 1 the record is born: two rows, one per arm, the phases 0 and 16.
At 6 each row reaches its mirror and is re-emitted on the other axis (the split with one weight: the phase
and the content kept, the age started again). At 11 both reach the splitter in the same interval and each is
split by the matrix (20, 21) with the quarter turn on the reflected row: toward D1 the two rows of amount 20
and 21 are in phase and merge to 41 (the group-ring addition), toward D2 they are in antiphase and cancel to
1 (the <code>cancel</code> line: 40 units removed on the GameBoard). At 12 the rows end at the ports and
offer their cells; the weights are the squares of the pointers, 1681 against 1 out of 1682; the wheel value
u = 0 falls under D1's rung; the click lands at D1 and the record is deleted everywhere. Our world saw one
thing: D1 clicked.</p>
<h2>The readings</h2>
<table>
<tr><th>Reading</th><th>Kind</th><th>Value</th><th>Source</th></tr>
<tr><td>the clicks at D1 and D2 over the run's {record["completed_ticks"]} intervals ({
        num(len(events["gather"]))
    } records completed)</td><td>detector</td><td class="num">D1 {
        num(sum(1 for g in events["gather"] if g["chosen"][0][0] == "D1"))
    }, D2 {
        num(sum(1 for g in events["gather"] if g["chosen"][0][0] == "D2"))
    }</td><td><code>events.jsonl</code>, the <code>gather</code> lines' <code>chosen</code></td></tr>
<tr><td>the register's pin over the first 64 births</td><td>detector</td><td class="num">D1 64, D2 0</td><td><code>examples/events/amplitude/expectations.json</code>, <code>mach_zehnder.mz_equal.clicks</code>; the offers 1681/1682 and 1/1682</td></tr>
<tr><td>the first record's offers</td><td>detector</td><td class="num">D1: 41 units at the phase 16, the square {
        num(
            int(
                next(
                    r["record"]
                    for r in events["record"]
                    if int(r["of"]) == first and r["detector"] == "D1"
                )
            )
        )
    }; D2: 1 unit at the phase 32, the square {
        num(
            int(
                next(
                    r["record"]
                    for r in events["record"]
                    if int(r["of"]) == first and r["detector"] == "D2"
                )
            )
        )
    }</td><td><code>events.jsonl</code>, the <code>click</code> and <code>record</code> lines of the record {
        first
    }</td></tr>
<tr><td>the rows cancelled toward D2 per record</td><td>GameBoard (the books)</td><td class="num">40</td><td><code>events.jsonl</code>, the <code>cancel</code> line at the interval 11</td></tr>
<tr><td>the books balanced at every interval</td><td>GameBoard</td><td class="num">{
        record["conserved_at_every_completed_tick"]
    }</td><td><code>run.json</code></td></tr>
</table>
{
        sources(
            [
                (
                    "the world",
                    f"<code>{relative(world)}</code>, registered in series L (the amplitude law), run as declared for {record['completed_ticks']} intervals",
                ),
                (
                    "the run",
                    f"<code>run.json</code> and <code>events.jsonl</code> made by <code>python -m event_universe --init {relative(world)}</code>",
                ),
                ("the source fingerprint", fingerprint_line(record)),
                (
                    "the frames and the store's columns",
                    "the world replayed in process through <code>NatureBeamSimulation</code>, the stores read at every interval (a GameBoard reading); the software column prints the store's int64 fields as they are",
                ),
                (
                    "the words",
                    '<a href="../../THREE_WORLDS.md">THREE_WORLDS.md</a>, the six transformations; <a href="../../HIGHLIGHTS.md">Highlights</a> 5.7, the three conversions',
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "worlds",
        page(
            "Our world",
            "One record from its birth to its click, seen three times: the vector world, the software world and our world.",
            body,
        ),
    )


def by_tick(lines: Sequence[dict[str, object]]) -> dict[int, list[dict[str, object]]]:
    out: dict[int, list[dict[str, object]]] = {}
    for line in lines:
        out.setdefault(int(line["tick"]), []).append(line)  # type: ignore[arg-type]
    return out


def escaped_per_tick(record: dict[str, object], family: str) -> list[int]:
    """Per completed interval what the family's transit line escaped in it
    (the faces and the border together), from the books."""
    audit = record["audit"]
    assert isinstance(audit, list)
    totals = [int(a["families"][family]["transit"]["escaped"]) for a in audit]
    return [b - a for a, b in zip([0] + totals[:-1], totals, strict=True)]


def nucleus_player(
    key: str,
    world: Path,
    runs: Path | None,
    ticks: Sequence[int],
    caption: str,
    duration_ms: int,
    weights: dict[str, float] | None = None,
    on_top: str = "nuclear",
    border_family: str = "nuclear",
    push_body: int = 1,
    colours: int = 128,
    scale: int = 10,
) -> tuple[Player, dict[str, object], dict[str, list[dict[str, object]]]]:
    """One series I world (or series R's, the quarks) replayed and drawn as
    the x-y projection (the amounts summed over z), the bodies as discs;
    per frame the bodies' Nodes, the steps and hand-overs so far, the
    border's clicks of the strong family in the interval and the push read
    by one body."""
    record_dir = runner_record(world, runs)
    record = read_json(record_dir / "run.json")
    events = scan_events(record_dir / "events.jsonl", ["step", "contact", "read", "become"])
    face_exits = [
        line
        for line in scan_events(record_dir / "events.jsonl", ["click"])["click"]
        if line.get("measured") is not None and str(line.get("detector", "")).startswith("face")
    ]
    events["exit"] = face_exits
    replay = Replay(world)
    frames = replay.run(ticks)
    # The plane of the bodies (z = 10 in every series I world): the rows in
    # that plane alone, so that the strong rows' halo is visible under the
    # fan's crowd.
    plane = plane_for(replay, scale=scale, slice_z=int(replay.world.measured[0].position[2]))
    plane.largest = largest_amounts(frames)
    plane.floor = 0.12
    plane.weights = weights if weights is not None else {"p": 0.5, "n": 0.5}
    plane.on_top = on_top
    steps = by_tick(events["step"])
    contacts = by_tick(events["contact"])
    exits = by_tick(face_exits)
    pushes: dict[int, int] = {}
    for line in events["read"]:
        if int(line["measured"]) == push_body:  # type: ignore[arg-type]
            pushes[int(line["tick"])] = pushes.get(int(line["tick"]), 0) + int(line["push"][0])  # type: ignore[arg-type, index]
    border = escaped_per_tick(record, border_family)
    images = [plane.image(frame) for frame in frames]
    readings = []
    for frame in frames:
        t = frame.tick
        lines = {
            "the bodies (number: family at Node)": "; ".join(
                f"{b.number}: {b.family} at {b.position}" for b in frame.bodies
            )
            or "none on the GameBoard (all left through the faces)",
            "steps so far (step lines)": num(sum(len(v) for k, v in steps.items() if k <= t)),
            "hand-overs so far (contact lines)": num(sum(len(v) for k, v in contacts.items() if k <= t)),
            f"the border's clicks of {border_family} this interval (run.json, audit)": num(
                border[t - 1] if 1 <= t <= len(border) else 0
            ),
            f"the push read by body {push_body} on x this interval (read lines)": num(pushes.get(t, 0)),
        }
        left = [
            f"{e['measured']} through {e['detector']} at {e['tick']}"
            for k, v in exits.items()
            if k <= t
            for e in v
        ]
        if left:
            lines["bodies that left (face click lines)"] = "; ".join(left)
        readings.append(lines)
    player = Player(
        key, images, list(ticks), readings, caption + " " + COPIES_NOTE, duration_ms, colours=colours
    )
    return player, record, events


@register("nucleus")
def page_nucleus(out: Path, runs: Path | None) -> Path:
    """(3) The nucleus, series I: the deuteron bound at one Link and free at
    three, the alpha square sheared apart; the strong rows' escape clicks
    at the lifetime."""
    folder = WORLDS / "nucleus"
    bound, bound_record, bound_events = nucleus_player(
        "deuteron_1",
        folder / "deuteron_1.json",
        runs,
        list(range(0, 49)),
        "The deuteron at one Link, `deuteron_1`: the plane z = 10 of the 21^3 cube (the bodies' plane, the rows "
        "in it alone), 10 pixels per Node; the proton p (red) at (10, 10, 10) and the neutron n (blue) at (11, 10, 10); "
        "the `nuclear` rows (gold) reach three Links and click on the border `lifetime`, the `p` and `n` rows "
        "fly to the faces. One frame per interval: each body releasing its rows into the Nodes beside it at "
        "every self-creation, the rows walking outward at the pace of the flight table.",
        120,
    )
    free, free_record, free_events = nucleus_player(
        "deuteron_3",
        folder / "deuteron_3.json",
        runs,
        frame_ticks(360, 45),
        "The deuteron at three Links, kicked outward, `deuteron_3`: the pair separates and leaves through the "
        "faces (one frame per three intervals).",
        100,
    )
    square, square_record, square_events = nucleus_player(
        "alpha_square",
        folder / "alpha_square.json",
        runs,
        frame_ticks(345, 45),
        "The square p n / n p, `alpha_square`: sheared apart, a proton steps first, the four disperse and leave "
        "(one frame per three intervals).",
        100,
    )
    world = folder / "deuteron_1.json"

    def first_steps(events: dict[str, list[dict[str, object]]]) -> str:
        seen: dict[int, dict[str, object]] = {}
        for line in events["step"]:
            seen.setdefault(int(line["number"]), line)  # type: ignore[arg-type]
        return (
            "; ".join(
                f"body {n} at the interval {line['tick']} from {tuple(line['node'])} to {tuple(line['to'])}"  # type: ignore[arg-type]
                for n, line in sorted(seen.items())
            )
            or "none"
        )

    def exits(events: dict[str, list[dict[str, object]]]) -> str:
        return (
            "; ".join(
                f"body {e['measured']} through {e['detector']} at {e['tick']}" for e in events["exit"]
            )
            or "none"
        )

    lifetime_clicks = int(
        next(d for d in bound_record["detectors"] if d["name"] == "lifetime")["families"]["nuclear"][
            "clicks"
        ]
    )  # type: ignore[index]
    bound_push = int(bound_record["measured"][0]["momentum"][0])  # type: ignore[index]
    entry_url = "../../EXPERIMENTS.md#i-the-nucleus-2026-09-20"
    body = f"""
{registered_note(world, "I, the nucleus (2026-09-20)", entry_url)}
<p class="demo">Also registered here: <code>examples/events/nucleus/deuteron_3.json</code> and
<code>examples/events/nucleus/alpha_square.json</code>, the same series, run as declared. He-5 (the register's
I9, the core family) was cut from series I for the budget and never run; it is not drawn.</p>
<h2>The GameBoard</h2>
<p>An open cube of 21 x 21 x 21 Nodes, K = {
        num(1 << 20)
    }, N = 64, the width of the push 2^28, the contact
through the table. Three free families without a phase circle: <code>p</code> (<code>charge</code> 4),
<code>n</code>, and <code>nuclear</code> with the column <code>strong</code> of value G = 10 000 and the sign
minus and the <code>lifetime</code> 3. A <b>proton</b> is a free body of 1836 units of <code>p</code> holding one
unit of <code>nuclear</code> (M 1837, Q 7344, G 10 000); a <b>neutron</b> 1839 of <code>n</code> holding one
(1840, 0, 10 000); every body releases one row of its held content per direction of the 290 primitive
directions with |a| + |b| + |c| at most 6 per interval. No detector is declared: the bodies are the external
things whose <code>read</code> and <code>contact</code> records are the readings, the six faces and the border
<code>lifetime</code> the detectors of what leaves. In <code>deuteron_1</code> p is at (10, 10, 10) and n at
(11, 10, 10); in <code>deuteron_3</code> at (9, 10, 10) and (12, 10, 10), each kicked outward by 10^12; in
<code>alpha_square</code> p1 (10, 10, 10), n2 (11, 10, 10), n3 (10, 11, 10), p4 (11, 11, 10).</p>
{
        legend(
            [
                ("the p rows", swatch(FAMILY_COLOURS[0])),
                ("the n rows", swatch(FAMILY_COLOURS[1])),
                ("the nuclear rows (the strong column, lifetime 3)", swatch(FAMILY_COLOURS[2])),
                ("a proton (a body of p)", swatch(BODY_COLOURS["p"])),
                ("a neutron (a body of n)", swatch(BODY_COLOURS["n"])),
            ]
        )
    }
<h2>Why this page</h2>
<p>The owner asked to see the nucleons: bound, and coming apart. In this law a nucleus is bodies at adjacent
Nodes reading each other's rows through the one coupling, a signed inner product over the columns the
families declare (gravity, the charge, the strong column), and the strong column has a range that is a
lifetime: a <code>nuclear</code> row clicks on the border at the age 3, so a body three Links away reads no
strong row at all. A body that would step onto the other's Node is refused and hands its momentum component
over through the occupant's table (the contact): the bound pair's labels are handed back and forth and
return to 0, and nothing steps.</p>
<h2>Bound: the deuteron at one Link</h2>
{bound.html()}
<p>What to see: from the second interval each body reads the other's rows and is pushed toward it by
{num(bound_push)} label units per interval (the register's designed integer, the <code>n</code> rows
10 161 754 944 and the <code>nuclear</code> rows 300 805 525 696); the gold halo is the strong rows within
three Links, clicking on the border <code>lifetime</code> at 580 per interval from the fourth interval
({
        num(lifetime_clicks)
    } over the run's 3000: <code>run.json</code>, the border's <code>clicks</code>); the pair
never steps in 3000 intervals; its hand-overs: {num(len(bound_events["contact"]))} (<code>contact</code>
lines), the label 0 after each. The escape click at the lifetime is the strong force's range, seen at the
border.</p>
<h2>Free: the deuteron at three Links, kicked</h2>
{free.html()}
<p>What to see: no strong row reaches three Links (the reads of <code>nuclear</code>: 0), gravity alone pulls
by 1 067 524 788 per interval on p (the register), far below the kick of 10^12; the first steps are at the
intervals {first_steps(free_events)}; the bodies leave: {exits(free_events)}.</p>
<h2>Coming apart: the square p n / n p</h2>
{square.html()}
<p>What to see: the square's bonds are central pushes and the contacts frictionless, and the p-p diagonal bond
is weaker than the n-n one by exactly Q^2 x U_d, so the rows are sheared apart (the register: 49 090 283 970 per
row per interval); the first steps: {first_steps(square_events)}; the bodies leave: {
        exits(square_events)
    }. The
register's alpha is the line p n n p (<code>alpha_line</code>), which holds for 3000 intervals; the square
does not.</p>
<h2>The readings</h2>
<table>
<tr><th>World</th><th>Reading</th><th>Kind</th><th>This run</th><th>The register (the signed-drive re-read)</th></tr>
<tr><td><code>deuteron_1</code></td><td>the push on p toward n per interval; steps; hand-overs; the border's clicks per interval</td><td>detector; GameBoard; detector; detector</td><td class="num">{
        num(bound_push)
    }; {num(len(bound_events["step"]))}; {num(len(bound_events["contact"]))}; {
        num(lifetime_clicks)
    } / 3000</td><td class="num">310 967 280 640; 0; 169 on p and 158 on n; 580 per interval from tick 4</td></tr>
<tr><td><code>deuteron_3</code></td><td>the first steps; the exits</td><td>GameBoard; detector (the faces)</td><td>{
        first_steps(free_events)
    }; {exits(free_events)}</td><td>ticks 33 and 34; face:+x at 311 and face:-x at 346</td></tr>
<tr><td><code>alpha_square</code></td><td>the first steps; the exits</td><td>GameBoard; detector (the faces)</td><td>{
        first_steps(square_events)
    }; {
        exits(square_events)
    }</td><td>p4 +y at 81, n2 at 89, p1 at 95, n3 at 110; out at 275, 285, 336, 339</td></tr>
<tr><td>all three</td><td>the books balanced at every interval</td><td>GameBoard</td><td class="num">{
        bound_record["conserved_at_every_completed_tick"]
    }, {free_record["conserved_at_every_completed_tick"]}, {
        square_record["conserved_at_every_completed_tick"]
    }</td><td>yes</td></tr>
</table>
{
        sources(
            [
                (
                    "the worlds",
                    "<code>examples/events/nucleus/deuteron_1.json</code>, <code>deuteron_3.json</code>, <code>alpha_square.json</code> (series I, registered), run as declared for 3000 intervals",
                ),
                (
                    "the runs",
                    "<code>run.json</code> and <code>events.jsonl</code> of each, made by <code>tools/run_series.py</code> (the runner, one process per world)",
                ),
                ("the source fingerprint", fingerprint_line(bound_record)),
                (
                    "the register",
                    f'<a href="{entry_url}">I, the nucleus (2026-09-20)</a> and <a href="../../../examples/events/nucleus/README.md">the series README</a> (the expectations pinned before the runs, the re-reads under the step drive and the signed drive)',
                ),
                (
                    "the frames",
                    "each world replayed in process through <code>NatureBeamSimulation</code>, the stores read at the drawn intervals (a GameBoard reading)",
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "nucleus",
        page(
            "The nucleus",
            "Series I: the deuteron bound at one Link and free at three, the alpha square sheared apart; the strong rows' escape clicks at the lifetime.",
            body,
        ),
    )


def decay_player(
    key: str,
    world: Path,
    runs: Path | None,
    ticks: Sequence[int],
    caption: str,
    duration_ms: int,
    scale: int = 12,
) -> tuple[Player, dict[str, object], dict[str, list[dict[str, object]]]]:
    """One series J world replayed in the neutron's plane, the products'
    rows drawn on top of the crowd; per frame the transformation, the
    products in flight and the shell's clicks."""
    record_dir = runner_record(world, runs)
    record = read_json(record_dir / "run.json")
    events = scan_events(record_dir / "events.jsonl", ["become", "step", "contact"])
    shell = [
        line
        for line in scan_events(record_dir / "events.jsonl", ["click"])["click"]
        if line.get("detector") not in (None,)
        and not str(line.get("detector")).startswith("face")
        and str(line.get("detector")) != "lifetime"
        or (
            str(line.get("detector", "")).startswith("face")
            and line.get("family") in ("beta", "nu", "w")
        )
    ]
    events["product_click"] = shell
    replay = Replay(world)
    frames = replay.run(ticks)
    plane = plane_for(replay, scale=scale)
    plane.largest = largest_amounts(frames)
    plane.floor = 0.12
    plane.body_slice_z = int(replay.world.measured[0].position[2])
    plane.weights = {name: 0.35 for name in replay.families if name not in ("beta", "nu", "w")}
    for name in ("beta", "nu", "w"):
        if name in replay.families:
            plane.largest[name] = 1.0
    plane.on_top = "beta" if "beta" in replay.families else ("w" if "w" in replay.families else None)
    plane.arrow_families = {name for name in ("beta", "nu", "w") if name in replay.families}
    becomes = by_tick(events["become"])
    clicks = by_tick(shell)
    images = [plane.image(frame) for frame in frames]
    readings = []
    for frame in frames:
        t = frame.tick
        lines: dict[str, str] = {}
        fired = [b for k, v in becomes.items() if k <= t for b in v]
        lines["transformations fired so far (become lines)"] = num(len(fired))
        if fired:
            last = fired[-1]
            lines["the last become"] = (
                f"body {last['measured']} at {tuple(last['node'])}, interval {last['tick']}: {last['from']} into {last['into']}, "  # type: ignore[arg-type]
                f"the products {', '.join(f'{p[0]} ({p[1]} unit of content {p[2]} on {tuple(p[3])})' for p in last['products'])}, "  # type: ignore[union-attr]
                f"the recoil {tuple(last['recoil'])}, the count the clock read {num(int(last['counted']))}"  # type: ignore[arg-type]
            )
        products = {
            name: int(r.amount.sum())
            for r in frame.rows
            for name in [r.family]
            if name in ("beta", "nu", "w")
        }
        lines["product rows in flight (GameBoard reading)"] = (
            ", ".join(f"{k} {v}" for k, v in products.items()) or "none"
        )
        seen = [c for k, v in clicks.items() if k <= t for c in v]
        lines["product clicks so far (click lines)"] = (
            "; ".join(
                f"{c['family']} at {c['detector']} {tuple(c['node'])} at {c['tick']} (content {c['content']})"
                for c in seen
            )
            or "none"
        )
        readings.append(lines)
    player = Player(key, images, list(ticks), readings, caption + " " + COPIES_NOTE, duration_ms)
    return player, record, events


@register("decay")
def page_decay(out: Path, runs: Path | None) -> Path:
    """(4) The decay, series J: a neutron family becoming another by the
    transformation `become`, the products' flight to the shell, the W
    exchange at one Link; the trigger ticks and counts from the register."""
    folder = WORLDS / "weak"
    release, _, _ = decay_player(
        "j3_release",
        folder / "j3_neutron_free.json",
        runs,
        list(range(0, 49)),
        "The release, `j3_neutron_free` at its first 48 intervals, one frame per interval: the neutron is a "
        "beam, releasing one row per direction of the 290 into the Nodes beside it at every self-creation, "
        "the rows walking outward; the shell's ring at r = 8.",
        120,
    )
    free_ticks = list(range(0, 501, 50)) + list(range(501, 561, 2))
    free, free_record, free_events = decay_player(
        "j3_neutron_free",
        folder / "j3_neutron_free.json",
        runs,
        free_ticks,
        "The free neutron, `j3_neutron_free`: the x-y projection of the 21^3 cube (the rows' amounts summed over z), "
        "12 pixels per Node; the neutron n at (10, 10, 10); the shell of readers at r = 8 (its ring in the plane "
        "z = 10 drawn, the rest of the shell not) is one `beam` "
        "detector of 762 Nodes measuring beta; the beta row drawn on top (its colour in the legend); one frame per 50 intervals "
        "until 500, then every second interval.",
        150,
    )
    bound_ticks = list(range(0, 551, 50)) + list(range(551, 611, 2))
    bound, bound_record, bound_events = decay_player(
        "j3_deuteron",
        folder / "j3_deuteron.json",
        runs,
        bound_ticks,
        "The bound neutron, `j3_deuteron`: the deuteron of series I with `become` at 512 on the neutron; the "
        "same shell; the proton p and the neutron n at one Link; one frame per 50 intervals until "
        "550, then every second interval.",
        150,
    )
    exchange, exchange_record, exchange_events = decay_player(
        "w_exchange",
        folder / "w_exchange.json",
        runs,
        list(range(0, 17)),
        "The W exchange, `w_exchange`: a bar of 7 x 1 x 1, 40 pixels per Node; the neutron n at x = 2 and the "
        "proton p at x = 3; the W row (its colour in the legend) born at the interval 8 on +x and measured by the proton at 9.",
        500,
        scale=40,
    )
    world = folder / "j3_neutron_free.json"
    entry_url = "../../EXPERIMENTS.md#j-the-weak-force-2026-09-20"

    def become_line(events: dict[str, list[dict[str, object]]]) -> dict[str, object] | None:
        return events["become"][0] if events["become"] else None

    fb = become_line(free_events)
    bb = become_line(bound_events)
    eb = become_line(exchange_events)
    fc = free_events["product_click"]
    bc = bound_events["product_click"]
    ec = exchange_events["product_click"]
    proton_after = exchange_record["measured"][1]  # type: ignore[index]
    body = f"""
{registered_note(world, "J, the weak force (2026-09-20)", entry_url)}
<p class="demo">Also registered here and run as declared: <code>examples/events/weak/j3_deuteron.json</code> and
<code>examples/events/weak/w_exchange.json</code>. The counts and the trigger ticks are the register's
(<a href="../../../examples/events/weak/README.md">the series README</a>, <code>weak/expectations.json</code>).</p>
<h2>The GameBoard</h2>
<p><b>J3, the neutron's decay against its clock.</b> An open cube of 21 x 21 x 21, K = {
        num(1 << 20)
    }, N = 64,
<code>release</code> [1, 1], <code>suspension</code> [1, 2^20]. The neutron is a free body of 1839 units of
<code>n</code> at (10, 10, 10) with the transformation <code>become</code> at 512 into <code>p</code> with the
products <code>beta</code> (1 unit of content 3, the charge -7344 per unit of amount) and <code>nu</code> (1 unit
of content 0): at the self-creation whose clock reaches 512 the event becomes a proton and the products are
born as a re-release is, with the recoil over both. A shell of 762 measured events of the paid family
<code>d</code> at r = 8 is one <code>beam</code> detector <code>shell</code> measuring <code>beta</code> with
<code>reads</code> <code>age</code> (the flight time on the click) and passing everything else. In
<code>j3_deuteron</code> the neutron is bound to a proton at one Link (series I's deuteron, the strong column
G = 10 000, lifetime 3, the width 2^28) and its clock is slowed by the count it reads, the crowd of the
proton's rows. <b>The W exchange.</b> A bar of 7 x 1 x 1: the neutron fixed at x = 2 with <code>become</code>
at 8 into <code>p</code> with the one product <code>w</code> (1 unit of content 3, the paid family with the whole
charge -7344 per unit of amount and the <code>lifetime</code> 1) on the direction +x, the proton of 1836 fixed
at x = 3.</p>
{
        legend(
            family_legend(Replay(world))
            + [
                ("the neutron, the proton (bodies)", swatch(BODY_COLOURS["n"])),
                ("a reader of the shell (a body of d)", swatch(BODY_COLOURS["d"])),
            ]
        )
    }
<h2>Why this page</h2>
<p>The owner asked to see a family becoming another. In this law the weak force is not a coupling but a rule
on the one-way side of the border: a measured event of one family becomes an event of another at the
self-creation whose clock reaches a declared key, the rest released as products with the recoil, the
charges balancing at load; the clock is slowed by the count it reads as every clock is, so a neutron in a
crowd fires later and a neutron alone at the key exactly. The hand of the products (series P, the parity
test) and the neutrino's phase window (series J2, the filter) are cited below from the register; this page
shows the transformation itself.</p>
<h2>The release: a body is a beam</h2>
{release.html()}
<h2>The free neutron</h2>
{free.html()}
<p>What to see: nothing for 511 intervals but the neutron's own rows; at {fb["tick"] if fb else "?"} the
<code>become</code> line: the neutron becomes a proton, the beta (content 3) leaves on
{tuple(fb["products"][0][3]) if fb else "?"} and the neutrino on {
        tuple(fb["products"][1][3]) if fb else "?"
    }, the
recoil {tuple(fb["recoil"]) if fb else "?"} on the new proton; the beta clicks the shell at the interval
{fc[0]["tick"] if fc else "?"} at {
        tuple(fc[0]["node"]) if fc else "?"
    } with the content 3 (the register: one
click, the content 3); the neutrino, a free row of content 0, passes every reader and leaves through a face
({
        "; ".join(
            f"{c['family']} through {c['detector']} at {c['tick']}" for c in fc if c["family"] == "nu"
        )
        or "no face click of nu in the run"
    }).</p>
<h2>The bound neutron</h2>
{bound.html()}
<p>What to see: the same key, later. The neutron's clock counts the proton's crowd at one Link (the count read
at the trigger {num(int(bb["counted"])) if bb else "?"}), so the transformation fires at
{
        bb["tick"] if bb else "?"
    } (the register under the fraction-free law: 568; the free neutron's 512); the beta
clicks the shell at {
        bc[0]["tick"] if bc else "?"
    } with the content 3; the pair is then two protons at one
Link and holds ({num(len(bound_events["step"]))} steps of {
        num(len(bound_events["contact"]))
    } attempted, every
attempt a hand-over). Against nature the register states the law's own prediction: a bound neutron that
decays later where nature's is stable by its binding energy.</p>
<h2>The W exchange at one Link</h2>
{exchange.html()}
<p>What to see: at the interval {
        eb["tick"] if eb else "?"
    } the neutron becomes a proton and throws the W on +x
with the recoil {tuple(eb["recoil"]) if eb else "?"}; at {
        ec[0]["tick"] if ec else "?"
    } the proton one Link away
measures it (the click, the push {tuple(ec[0]["push"]) if ec else "?"}) and has afterwards the charge
{proton_after["charge"]} and the content {
        num(int(proton_after["content"]))
    }: a neutron's, in the detector's
terms. No W reaches the border <code>lifetime</code>. The exchange is complete at the click; the momenta
{tuple(exchange_record["measured"][0]["momentum"])} and {tuple(proton_after["momentum"])}.</p>
<h2>The readings</h2>
<table>
<tr><th>World</th><th>Reading</th><th>Kind</th><th>This run</th><th>The register</th></tr>
<tr><td><code>j3_neutron_free</code></td><td>the trigger tick; the shell's clicks and their content</td><td>GameBoard; detector</td><td class="num">{
        fb["tick"] if fb else "?"
    }; {num(len([c for c in fc if c["family"] == "beta"]))} click, content {
        fc[0]["content"] if fc else "?"
    } at {fc[0]["tick"] if fc else "?"}</td><td class="num">512 exactly; one click, content 3</td></tr>
<tr><td><code>j3_deuteron</code></td><td>the trigger tick and the count read; the shell's click; steps of attempts</td><td>GameBoard; detector; GameBoard</td><td class="num">{
        bb["tick"] if bb else "?"
    }, {num(int(bb["counted"])) if bb else "?"}; {bc[0]["tick"] if bc else "?"}; {
        num(len(bound_events["step"]))
    } of {
        num(len(bound_events["contact"]))
    }</td><td class="num">568 (the fraction-free re-read; pinned 574 or up to 3 before), the warm count 128 590; 581; 0 of 33 and 31</td></tr>
<tr><td><code>w_exchange</code></td><td>the become tick and the recoil; the proton's click; the proton's charge and content after</td><td>GameBoard; detector; detector</td><td class="num">{
        eb["tick"] if eb else "?"
    }, {tuple(eb["recoil"]) if eb else "?"}; {ec[0]["tick"] if ec else "?"}; {proton_after["charge"]}, {
        num(int(proton_after["content"]))
    }</td><td class="num">8, [-192, 0, 0]; 9; [0, 1], 1839</td></tr>
<tr><td>J1 (not replayed here)</td><td>64 free neutrons on a lattice: the trigger ticks and the shell's 64 clicks</td><td>GameBoard; detector</td><td>not run for this page (about 4 minutes each)</td><td>522 .. 524 (the lattice) and 523 .. 528 (with a source); the 64 clicks a step from 541 to 563, every click the content 3</td></tr>
<tr><td>J2 (the neutrino's window)</td><td>the first reader's share of a stride-1 source's arrivals; the 127 readers behind it</td><td>detector</td><td>not replayed here</td><td>exactly 1 / 64; nothing (a filter, not an attenuation); the ladder exhausts the beam after 64 readers</td></tr>
<tr><td>P (the hand)</td><td>the parity test of the W's hand against the axis; J2's bar with two readers admitting one hand each</td><td>detector</td><td>not replayed here</td><td>the mirror image sends the W to the other side (<code>tests/test_hand.py</code> (d)); 0 and 1022 clicks</td></tr>
<tr><td>all three</td><td>the books balanced at every interval</td><td>GameBoard</td><td class="num">{
        free_record["conserved_at_every_completed_tick"]
    }, {bound_record["conserved_at_every_completed_tick"]}, {
        exchange_record["conserved_at_every_completed_tick"]
    }</td><td>yes</td></tr>
</table>
{
        sources(
            [
                (
                    "the worlds",
                    "<code>examples/events/weak/j3_neutron_free.json</code>, <code>j3_deuteron.json</code>, <code>w_exchange.json</code> (series J, registered), run as declared",
                ),
                (
                    "the runs",
                    "<code>run.json</code> and <code>events.jsonl</code> of each, made by <code>tools/run_series.py</code>",
                ),
                ("the source fingerprint", fingerprint_line(free_record)),
                (
                    "the register",
                    f'<a href="{entry_url}">J, the weak force (2026-09-20)</a>, <a href="../../EXPERIMENTS.md#p-the-hand-2026-09-20">P, the hand (2026-09-20)</a>, <a href="../../../examples/events/weak/README.md">the series README</a> and <code>examples/events/weak/expectations.json</code>',
                ),
                (
                    "the frames",
                    "each world replayed in process through <code>NatureBeamSimulation</code>, the stores read at the drawn intervals (a GameBoard reading); the beta and W rows drawn on top of the crowd",
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "decay",
        page(
            "The decay",
            "Series J: a neutron family becoming another by the transformation become, the products' flight to the shell, the W exchange at one Link.",
            body,
        ),
    )


def slot_name(direction: tuple[int, int, int], index: int) -> str:
    names = {
        (1, 0, 0): "+x",
        (-1, 0, 0): "-x",
        (0, 1, 0): "+y",
        (0, -1, 0): "-y",
        (0, 0, 1): "+z",
        (0, 0, -1): "-z",
    }
    if direction == (0, 0, 0):
        return "rest a" if index == 0 else "rest b"
    return names.get(direction, f"spectator {direction}")


@register("collision")
def page_collision(out: Path, runs: Path | None) -> Path:
    """(5) The collision: rows meeting at a Node of free space permuted by
    the collision table, on a small cube; the slot states per interval."""
    world = GALLERY_WORLDS / "collision.json"
    record_dir = runner_record(world, runs)
    record = read_json(record_dir / "run.json")
    replay = Replay(world)
    ticks = list(range(0, replay.ticks + 1))
    frames = replay.run(ticks)
    cube = Cube(tuple(replay.world.shape), 22, replay.world.phase_steps, replay.directions)
    meetings = [(4, 4, 4), (4, 4, 1)]
    images = [cube.image(frame) for frame in frames]
    readings = []
    for frame in frames:
        rows = frame.rows[0]
        lines: dict[str, str] = {
            "rows on the GameBoard (GameBoard reading)": num(int(rows.amount.size)),
        }
        for node in meetings:
            here = [
                slot_name(replay.directions[int(rows.direction[k])], int(rows.direction[k]))
                for k in range(rows.amount.size)
                if (int(rows.x[k]), int(rows.y[k]), int(rows.z[k])) == node
            ]
            lines[f"the slots occupied at {node}"] = ", ".join(sorted(here)) or "none"
        lines["every row (Node, direction, age)"] = (
            "; ".join(
                f"({int(rows.x[k])}, {int(rows.y[k])}, {int(rows.z[k])}) {slot_name(replay.directions[int(rows.direction[k])], int(rows.direction[k]))} age {int(rows.age[k])}"
                for k in range(rows.amount.size)
            )
            or "none: every row has left through a face"
        )
        readings.append(lines)
    player = Player(
        "collision",
        images,
        ticks,
        readings,
        "The open cube of 9 x 9 x 9 in an oblique projection, 22 pixels per Link (x to the right, y upward, z "
        "receding); every row a disc coloured by its phase with a bar toward its heading (no bar: a rest "
        "slot); one frame per interval.",
        duration_ms=400,
    )
    faces = {
        d["name"]: int(d["families"]["light"]["clicks"])
        for d in record["detectors"]
        if str(d["name"]).startswith("face")
    }  # type: ignore[index]
    body = f"""
{demonstration_note(world)}
<h2>The GameBoard</h2>
<p>An open cube of 9 x 9 x 9 Nodes with no measured event on it: free space only, so the collision table acts
at every Node. Six rows of the paid family <code>light</code> are declared in transit, all of the number 1, the
amount 1 and the content 1, at the age 0: a <b>head-on pair</b> on the x axis, from (1, 4, 4) on +x and from
(7, 4, 4) on -x, meeting at (4, 4, 4); a <b>triple</b> on the plane z = 1, from (1, 4, 1) on +x, (7, 4, 1) on
-x and (4, 1, 1) on +y, meeting at (4, 4, 1); and a <b>lone unit</b> from (0, 0, 7) on the diagonal (1, 1, 0),
a declared direction beyond the six headings. The faces are open: a row that leaves clicks on its face.</p>
{legend([("a row, coloured by its phase (all born at the phase 0)", '<i class="wheel"></i>')])}
<h2>Why this page</h2>
<p>The owner asked to see "how something hits something". On the GameBoard two rows never touch: a Node holds
eight single-occupancy slots, the six headings and two rest slots, and when single units of one number and
content occupy several slots at a Node of free space in one interval, the collision table permutes them: the
slot state's class (the crowd mask, the number of singles and their vector sum) is kept, and inside a class
the forward map is the cyclic shift by one, so the table is a bijection with an inverse (BEAM_LAW section 4).
Amount and momentum are conserved by construction; a row on a fan direction is a spectator and passes
untouched.</p>
<h2>The moving picture</h2>
{player.html()}
<p>What to see. The head-on pair (the class of "+x -x", four members: +x -x, +y -y, +z -z and the rest pair,
the shift +x -x to rest a rest b to +z -z to +y -y to +x -x) reaches (4, 4, 4) at the interval 5 and parks:
both rows on the rest slots, no momentum to trade; at 6 the rest pair becomes +z -z; the flight table does
not step them in that interval, so at 7 the table acts again and +z -z becomes +y -y; from 8 the pair walks
apart along y and leaves through the faces at 13 and 14. The triple at (4, 4, 1) is the class "+x -x +y"
(three members, the shift to "+y rest a rest b"): the head-on pair parks and the odd unit keeps its heading,
then the parked pair turns and goes. The lone diagonal unit is a spectator of the table, straight and
unchanged, and leaves through a face. Every class is an orbit of the permutation, the invariants written on
it: the same n and the same vector sum before and after.</p>
<h2>The readings</h2>
<table>
<tr><th>Reading</th><th>Kind</th><th>Value</th><th>Source</th></tr>
<tr><td>rows declared; rows on the GameBoard at the end</td><td>GameBoard (the books)</td><td class="num">{
        num(int(record["audit"][0]["families"]["light"]["transit"]["initial"]))
    }; {
        num(int(record["audit"][-1]["families"]["light"]["transit"]["current"]))
    }</td><td><code>run.json</code>, <code>audit</code>, the transit line of <code>light</code></td></tr>
<tr><td>the clicks per face</td><td>detector (the faces)</td><td>{
        ", ".join(f"{k} {v}" for k, v in faces.items())
    }</td><td><code>run.json</code>, <code>detectors</code></td></tr>
<tr><td>the books balanced at every interval</td><td>GameBoard</td><td class="num">{
        record["conserved_at_every_completed_tick"]
    }</td><td><code>run.json</code></td></tr>
</table>
<p>The table's classes and the 20 orbits of the six-heading patterns under the cube's 48 signed axis
permutations are pinned in <code>tests/test_nature_beam_collision.py</code>
(<a href="../../TEST_EXPECTATIONS.md#the-collision-table">the test expectations</a>); this page draws the
table's action on two of them.</p>
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
                    "the world replayed in process through <code>NatureBeamSimulation</code>, the stores read at every interval (a GameBoard reading: the rows' Nodes, directions and ages)",
                ),
                (
                    "the law",
                    '<a href="../../BEAM_LAW.md">the Beam Law</a>, section 4 (the collision table)',
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "collision",
        page(
            "The collision",
            "Rows meeting at a Node of free space, permuted by the collision table: the head-on pair parks, turns and leaves.",
            body,
        ),
    )


def lensing_player(
    key: str,
    world: Path,
    runs: Path | None,
    caption: str,
    ticks: Sequence[int] | None = None,
) -> tuple[Player, dict[str, object], dict[str, list[dict[str, object]]]]:
    """A series K world replayed as the x-y projection, the beam's rows on
    top of the mass's dimmed crowd; per frame the beam in flight, the
    screen's and the mass's clicks of light and the books' turned line."""
    record_dir = runner_record(world, runs)
    record = read_json(record_dir / "run.json")
    clicks = [
        line
        for line in scan_events(record_dir / "events.jsonl", ["click"])["click"]
        if line.get("family") == "light"
    ]
    screen = by_tick([c for c in clicks if str(c.get("detector", "")).startswith("screen")])
    taken = by_tick([c for c in clicks if c.get("detector") is None])
    faces = by_tick([c for c in clicks if str(c.get("detector", "")).startswith("face")])
    replay = Replay(world)
    ticks = list(ticks) if ticks is not None else frame_ticks(replay.ticks, 72)
    frames = replay.run(ticks)
    plane = plane_for(replay, scale=6)
    plane.largest = largest_amounts(frames)
    plane.floor = 0.12
    plane.weights = {"m": 0.3}
    plane.on_top = "light"
    plane.body_slice_z = int(replay.world.measured[0].position[2])
    plane.body_radius = 0.9
    plane.body_labels = False
    audit = record["audit"]
    assert isinstance(audit, list)
    images = [plane.image(frame) for frame in frames]
    readings = []
    for frame in frames:
        t = frame.tick
        light = next(r for r in frame.rows if r.family == "light")
        lines = {
            "rows of the beam in flight (GameBoard reading)": num(int(light.amount.sum())),
            "the screen's clicks so far (click lines)": num(
                sum(int(c["amount"]) for k, v in screen.items() if k <= t for c in v)
            ),  # type: ignore[arg-type]
            "rows of light the mass took so far (click lines)": num(
                sum(int(c["amount"]) for k, v in taken.items() if k <= t for c in v)
            ),  # type: ignore[arg-type]
            "rows of light on the faces so far": num(
                sum(int(c["amount"]) for k, v in faces.items() if k <= t for c in v)
            ),  # type: ignore[arg-type]
        }
        if 1 <= t <= len(audit):
            lines["the books' turned line of light (run.json, audit)"] = str(
                tuple(audit[t - 1]["families"]["light"].get("turned", (0, 0, 0)))
            )
        readings.append(lines)
    player = Player(key, images, ticks, readings, caption + " " + COPIES_NOTE, 100)
    events = {
        "screen": [c for v in screen.values() for c in v],
        "taken": [c for v in taken.values() for c in v],
        "faces": [c for v in faces.values() for c in v],
    }
    return player, record, events


def centroid_y(clicks: Sequence[dict[str, object]], first: int) -> tuple[float, int]:
    """The amount-weighted mean y of the screen's clicks from the interval
    `first` on, and their count (the register's window)."""
    total = 0
    weighted = 0.0
    for c in clicks:
        if int(c["tick"]) >= first:  # type: ignore[arg-type]
            amount = int(c["amount"])  # type: ignore[arg-type]
            total += amount
            weighted += amount * float(c["node"][1])  # type: ignore[index]
    return (weighted / total if total else float("nan")), total


@register("energy")
def page_energy(out: Path, runs: Path | None) -> Path:
    """(6) High-energy rows: series K under the meeting, a beam of light
    passing a mass and bent toward it, the mass measuring the most turned
    rows; the control beside it."""
    folder = WORLDS / "lensing"
    release, _, _ = lensing_player(
        "mass_release",
        folder / "mass_meeting.json",
        runs,
        "The release, `mass_meeting` at its first 48 intervals, one frame per interval: the mass is a beam, "
        "releasing one row per direction of the 290 into the Nodes beside it at every self-creation, its "
        "crowd walking outward; the lamp's first records on their five lines.",
        list(range(0, 49)),
    )
    mass, mass_record, mass_events = lensing_player(
        "mass_meeting",
        folder / "mass_meeting.json",
        runs,
        "`mass_meeting`: the x-y projection of the 57 x 41 x 41 box, 6 pixels per Node; the lamp at (2, 26, 20), "
        "the mass m at the centre (28, 20, 20) with its crowd of 290 directions dimmed, the beam's rows on top "
        "coloured by their phase, the screen at x = 54 (the green column); one frame per 5.6 intervals.",
    )
    control, control_record, control_events = lensing_player(
        "control",
        folder / "control.json",
        runs,
        "`control`: the same box without the mass; the beam goes straight.",
    )
    world = folder / "mass_meeting.json"
    entry_url = "../../EXPERIMENTS.md#k-under-the-meeting-2026-09-20"
    m_y, m_n = centroid_y(mass_events["screen"], 110)
    c_y, c_n = centroid_y(control_events["screen"], 110)
    body = f"""
{registered_note(world, "K under the meeting (2026-09-20)", entry_url)}
<p class="demo">Also registered here and run as declared: <code>examples/events/lensing/control.json</code> (series K's
control without the mass).</p>
<h2>The GameBoard</h2>
<p>An open box of 57 x 41 x 41 Nodes, the centre c = (28, 20, 20), K = 2^30, N = 64, the world key
<code>meeting</code> true (the identity <code>meeting-v1</code>). <b>The lamp</b> at (2, 26, 20), a fixed measured
event of the paid family <code>light</code> (the turn 8 steps per self-creation), releases one unit per
self-creation on five directions within 5 degrees of +x: a narrow beam at the impact distance b = 6 above
the mass's line. <b>The mass</b> at c, a fixed measured event of the free, phase-less family <code>m</code> of
content M = 2^12, releases one row per direction of the 290 primitive directions with |a| + |b| + |c| at
most 6 per interval: its crowd. <b>The screen</b> at x = 54 is 1681 fixed events of <code>wall</code>, each a
one-Node <code>wave</code> detector <code>screen_&lt;y&gt;_&lt;z&gt;</code> with the age moment on the click
record. Under the meeting every paid unit of the beam reads the mass's free crowd at each free-space Node
it shares with it and turns toward the mass by one grain step of the direction table per N = 64 crowd units
met, the count kept on its phase register, the crowd untouched.</p>
{
        legend(
            family_legend(Replay(world))
            + [
                ("the lamp and the mass (bodies)", swatch(BODY_COLOURS["light"])),
                ("a pixel of the screen (a wall event)", swatch(BODY_COLOURS["wall"])),
            ]
        )
    }
<h2>Why this page</h2>
<p>The owner asked for "high-energy photons, all kinds of things that break them apart". In this law a row's
energy is its phase rate and its momentum label (E = h f; the label amount x content x <b>u</b>_d), and a row
in flight is moved by the flight table alone: the physicist's entry 2 predicted that light is neither bent
nor delayed by a mass, and series K measured exactly that (0.000 pixel, 0.00 interval). Under the meeting, the
owner's decision of 2026-09-20 ("an event in transit reads the crowd as a body does, a report, not a
balance"), the beam is bent toward the mass with the sign of gravity and the M / b form, at the grain of the
fan: this page shows that run beside its control. What the mass does to the rows that reach it is the
other half of the story: it measures them (the click), and the most turned rows end there.</p>
<h2>The release: a body is a beam</h2>
{release.html()}
<h2>The beam beside the mass, under the meeting</h2>
{mass.html()}
<h2>The control: no mass</h2>
{control.html()}
<p>What to see: in the control the five rows of every record fly straight to the screen at y = 26 (the
centroid {c_y:.3f} over {num(c_n)} clicks from the interval 110); under the meeting the beam bends toward
the mass as it passes (the phase register counting the crowd met, the direction turned one grain step per
64 units), the arrivals land lower (the centroid {m_y:.3f}, a shift of {m_y - c_y:+.3f} pixels over
{num(m_n)} clicks), and {
        num(sum(int(c["amount"]) for c in mass_events["taken"]))
    } rows of the beam, the most
turned, reach the mass's own Node and click there: the mass measures the light that reaches it. The books'
<code>turned</code> line of light reports what the meetings moved the transit momentum by: the y component
toward the mass.</p>
<h2>The readings</h2>
<table>
<tr><th>Reading</th><th>Kind</th><th>This run</th><th>The register (2026-09-20)</th></tr>
<tr><td>the screen's centroid in y from the interval 110, the mass world (the control)</td><td>detector</td><td class="num">{
        m_y:.3f} ({c_y:.3f}); the shift {
        m_y
        - c_y:+.3f}</td><td class="num">-1.790 (26.000): the sign toward the mass, expected -3.0</td></tr>
<tr><td>the screen's clicks from the interval 110, the mass world (the control)</td><td>detector</td><td class="num">{
        num(m_n)
    } ({num(c_n)})</td><td class="num">1350 (1455)</td></tr>
<tr><td>rows of light the mass took over the run</td><td>detector</td><td class="num">{
        num(sum(int(c["amount"]) for c in mass_events["taken"]))
    }</td><td class="num">122</td></tr>
<tr><td>rows of light on the faces over the run</td><td>detector</td><td class="num">{
        num(sum(int(c["amount"]) for c in mass_events["faces"]))
    }</td><td class="num">0</td></tr>
<tr><td>the books' turned line of light at the end</td><td>GameBoard (the books)</td><td class="num">{
        tuple(mass_record["audit"][-1]["families"]["light"]["turned"])
    }</td><td class="num">(-8016, -85088, 0)</td></tr>
<tr><td>the books balanced at every interval (the mass world, the control)</td><td>GameBoard</td><td class="num">{
        mass_record["conserved_at_every_completed_tick"]
    }, {control_record["conserved_at_every_completed_tick"]}</td><td>yes</td></tr>
</table>
<p>The register's run was made on 2026-09-20 at the fingerprint of that day; the law's counts changed since
(the fraction-free law, the step drive), so a number of this run that differs from the register's is the
present engine's reading, not a re-registration: nothing is moved here. The register also holds the
<code>heavy</code> (M = 2^13), <code>near</code> (b = 3) and <code>lens</code> (two beams) worlds; the delay in
time is none in every world (the mean ages the bent path's), and the grain of the fan, 2.4 degrees, is 10^4
times nature's angle at the Sun's limb, so the value is not claimed.</p>
{
        sources(
            [
                (
                    "the worlds",
                    "<code>examples/events/lensing/mass_meeting.json</code> and <code>control.json</code> (series K under the meeting, registered), run as declared for 400 intervals",
                ),
                (
                    "the runs",
                    "<code>run.json</code> and <code>events.jsonl</code> of each, made by <code>tools/run_series.py</code>",
                ),
                ("the source fingerprint", fingerprint_line(mass_record)),
                (
                    "the register",
                    f'<a href="{entry_url}">K under the meeting (2026-09-20)</a> and <a href="../../EXPERIMENTS.md#k-light-beside-a-mass-2026-09-20">K, light beside a mass (2026-09-20)</a>; <a href="../../../examples/events/lensing/README.md">the series README</a>',
                ),
                (
                    "the frames",
                    "each world replayed in process through <code>NatureBeamSimulation</code>, the stores read at the drawn intervals (a GameBoard reading); the beam's rows drawn on top of the crowd",
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "energy",
        page(
            "High-energy rows",
            "Series K under the meeting: a beam of light passing a mass, bent toward it; the mass measuring the most turned rows.",
            body,
        ),
    )


@register("atom")
def page_atom(out: Path, runs: Path | None) -> Path:
    """(8) The atom, series H: the electron orbiting the proton with its
    momentum arrow and its copies, its phase turning by its momentum, the
    proton's shell of copies; the faces reading what comes out."""
    world = WORLDS / "bohr" / "r8.json"
    record_dir = runner_record(world, runs)
    record = read_json(record_dir / "run.json")
    events = scan_events(record_dir / "events.jsonl", ["step"])
    exits = [
        line
        for line in scan_events(record_dir / "events.jsonl", ["click"])["click"]
        if line.get("measured") is not None and str(line.get("detector", "")).startswith("face")
    ]
    replay = Replay(world)
    ticks = frame_ticks(min(replay.ticks, (int(exits[0]["tick"]) + 30) if exits else replay.ticks), 90)  # type: ignore[arg-type]
    frames = replay.run(ticks)
    proton = tuple(int(c) for c in replay.world.measured[0].position)
    plane = plane_for(replay, scale=8, slice_z=proton[2])
    plane.largest = largest_amounts(frames)
    plane.floor = 0.1
    plane.weights = {"p": 0.35, "e": 0.0}
    plane.phase_bodies = {"e"}
    plane.body_radius = 0.9
    plane.body_labels = False
    steps = by_tick(events["step"])
    early = Replay(world).run(list(range(0, 49)))
    release = Player(
        "atom_release",
        [plane.image(frame) for frame in early],
        list(range(0, 49)),
        [
            {
                "rows of the proton on the GameBoard (GameBoard reading)": num(
                    int(sum(int(r.amount.sum()) for r in frame.rows if r.family == "p"))
                ),
                "rows of the electron on the GameBoard": num(
                    int(sum(int(r.amount.sum()) for r in frame.rows if r.family == "e"))
                ),
            }
            for frame in early
        ],
        "The release, `r8` at its first 48 intervals, one frame per interval: the proton is a beam, releasing "
        "one row per direction of its shell of 2616 into the Nodes beside it every 10 intervals (the rows in "
        "the plane z = 22 drawn), the shells walking outward; the electron releasing its rows on its four "
        "directions at every self-creation. " + COPIES_NOTE,
        120,
    )
    images = [plane.image(frame) for frame in frames]
    readings = []
    previous_angle = None
    turned = 0.0
    for frame in frames:
        t = frame.tick
        electron = next((b for b in frame.bodies if b.family == "e"), None)
        lines: dict[str, str] = {}
        if electron is not None:
            dx, dy = electron.position[0] - proton[0], electron.position[1] - proton[1]
            angle = math.atan2(dy, dx)
            if previous_angle is not None:
                delta = angle - previous_angle
                while delta > math.pi:
                    delta -= 2 * math.pi
                while delta < -math.pi:
                    delta += 2 * math.pi
                turned += delta
            previous_angle = angle
            lines["the electron's Node (GameBoard reading)"] = str(electron.position)
            lines["its distance from the proton, Links"] = f"{math.hypot(dx, dy):.2f}"
            lines["its momentum vector p (label units)"] = str(electron.momentum)
            lines["its phase on the circle Z_64 (turned by its momentum)"] = num(electron.phase)
            lines["the angle turned since the start, in orbits"] = f"{turned / (2 * math.pi):.2f}"
        else:
            lines["the electron"] = "gone: it left through a face"
        lines["steps so far (step lines)"] = num(sum(len(v) for k, v in steps.items() if k <= t))
        readings.append(lines)
    player = Player(
        "atom",
        images,
        ticks,
        readings,
        "`r8`: the plane z = 22 of the 45^3 cube (the orbit's plane), 8 pixels per Node; the proton p at the "
        "centre with its shell of copies (one row per direction of 2616 every 10 intervals, the in-plane ones "
        "drawn), the electron e as a disc coloured by its phase, with its momentum arrow and its own copies; the "
        "proton is fixed and does not step, its arrow the momentum it was handed; one frame per 43 intervals. "
        + COPIES_NOTE,
        100,
    )
    entry_url = "../../EXPERIMENTS.md#h-bohrs-lines-behind-the-detector-2026-09-20"
    exit_text = (
        f"the electron left through {exits[0]['detector']} at the interval {exits[0]['tick']}"
        if exits
        else "the electron is on the GameBoard at the end"
    )
    body = f"""
{registered_note(world, "H, Bohr's lines behind the detector (2026-09-20)", entry_url)}
<h2>The GameBoard</h2>
<p>An open cube of 45 x 45 x 45 Nodes, K = {num(replay.world.K)}, N = 64, the world's <code>action</code>
h = {
        num(int(record["action"]))
    } (the identity <code>bohr-v1</code>). <b>The proton</b> at (22, 22, 22), measured
event 1: a fixed body of 1836 units of <code>p</code> (<code>charge</code> [1, 1]) releasing one row per
direction of a shell of 2616 primitive directions every 10 intervals, its field. <b>The electron</b>, measured
event 2: a free body of 1836 units of <code>e</code> (<code>charge</code> -15, a phase circle) on a set of three
Nodes (<code>span</code> [1, 1, 3]) at r = 8 on the +x axis, with the tangential momentum
<b>p</b> = {
        tuple(int(c) for c in replay.world.measured[1].momentum)
    } the series README derives from the engine's
own flight lines for a circular orbit, turning its phase by its momentum at every Link it steps
(<code>phase_by_momentum</code> under h) and releasing rows on four directions that carry that phase to the
open faces, the <code>wave</code> detectors of what comes out of the atom.</p>
{
        legend(
            family_legend(Replay(world))
            + [
                ("the proton (a body of p)", swatch(BODY_COLOURS["p"])),
                ("the electron (a body of e), coloured by its phase", '<i class="wheel"></i>'),
            ]
        )
    }
<h2>Why this page</h2>
<p>The owner asked that a body be shown with its spreading: "if one sees an electron, one should also see its
spreading, its copies in space, transparent, and the arrow of its vector, where it travels". Here the electron
is that body: at every self-creation it releases rows on its directions (its copies, the translucent discs
that spread from it at the pace of the flight table), it reads the proton's rows and is pushed by the one
coupling (the charge column), its momentum vector <b>p</b> is the white arrow, and its phase, an element of
Z_64, turns by |<b>p</b>| N over h at every Link it steps, so the disc's colour goes round the circle as it
orbits. What a detector reads of the atom is on the faces: the coherent record of the electron's rows.</p>
<h2>The release: a body is a beam</h2>
{release.html()}
<h2>The orbit</h2>
{player.html()}
<p>What to see: the electron circles the proton, its arrow turning with it and its copies streaming outward;
the proton's shell of copies pulses every 10 intervals through the plane; the phase colour of the electron
turns as it moves. The register (the signed-drive re-read of series H, then the turn by momentum as a row of
the counts table): the orbit at r = 8 closes the angle twice (T 1292, 2016), the phase's turn per orbit 0.969
against the expected 0, the faces' coherence C(2) = 1.24, and the electron leaves at 3869; Bohr's lines are not
read and the register keeps that verdict, nothing tuned. In this run {exit_text}.</p>
<h2>The readings</h2>
<table>
<tr><th>Reading</th><th>Kind</th><th>This run</th><th>The register</th></tr>
<tr><td>the electron's steps; its exit</td><td>GameBoard; detector (the faces)</td><td class="num">{
        num(len(events["step"]))
    }; {html.escape(exit_text)}</td><td>closes the angle twice (T 1292, 2016); leaves at 3869</td></tr>
<tr><td>the electron's rows clicked on the faces (x, y)</td><td>detector</td><td class="num">{
        ", ".join(
            f"{d['name']} {d['families']['e']['clicks']}"
            for d in record["detectors"]
            if d["families"]["e"]["clicks"]
        )
    }</td><td>the faces' coherence at the closing C(2) = 1.24 (the criterion 1.0)</td></tr>
<tr><td>the books balanced at every interval</td><td>GameBoard</td><td class="num">{
        record["conserved_at_every_completed_tick"]
    }</td><td>yes</td></tr>
</table>
{
        sources(
            [
                (
                    "the world",
                    "<code>examples/events/bohr/r8.json</code> (series H, registered), run as declared for 4200 intervals",
                ),
                (
                    "the run",
                    "<code>run.json</code> and <code>events.jsonl</code> made by <code>python -m event_universe --init examples/events/bohr/r8.json</code>",
                ),
                ("the source fingerprint", fingerprint_line(record)),
                (
                    "the register",
                    f'<a href="{entry_url}">H, Bohr lines behind the detector (2026-09-20)</a> and <a href="../../../examples/events/bohr/README.md">the series README</a> (the re-reads under the step drive, the signed drive and the counts table)',
                ),
                (
                    "the frames",
                    "the world replayed in process through <code>NatureBeamSimulation</code>, the stores read at the drawn intervals (a GameBoard reading)",
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "atom",
        page(
            "The atom",
            "Series H: the electron circling the proton with its momentum arrow and its copies spreading, its phase turning by its momentum.",
            body,
        ),
    )


@dataclass
class Volume:
    """The whole GameBoard in three dimensions, an isometric projection (x
    to the right and down, z to the left and down, y up), the rows
    aggregated per Node and drawn as translucent discs back to front, the
    bodies with their copies and the arrows of their momentum labels as
    on the plane; drawn at SUPERSAMPLE times the size and downsampled
    (the model owner, 2026-09-21: "now show all of these in three
    dimensions")."""

    shape: tuple[int, int, int]
    scale: int
    phase_steps: int
    phased: dict[str, bool]
    colours: dict[str, tuple[int, int, int]]
    directions: list[tuple[int, int, int]]
    margin: int = 24
    weights: dict[str, float] = field(default_factory=dict)
    largest: dict[str, float] = field(default_factory=dict)
    phase_bodies: set[str] = field(default_factory=set)
    arrow_families: set[str] = field(default_factory=set)
    body_radius: float = 0.9
    copies: bool = True
    # The families whose bodies are drawn as small dots (a shell of readers,
    # a screen of pixels): the apparatus, not the story.
    dot_bodies: set[str] = field(default_factory=set)
    # The cube turned about its vertical axis by this angle (radians): the
    # player turns it slowly, frame by frame (the model owner, 2026-09-21:
    # "let the cube turn slowly").
    angle: float = 0.0

    COS30 = math.cos(math.pi / 6)
    SIN30 = math.sin(math.pi / 6)

    @property
    def diagonal(self) -> float:
        nx, _, nz = self.shape
        return math.hypot(nx, nz)

    @property
    def size(self) -> tuple[int, int]:
        _, ny, _ = self.shape
        d = self.diagonal
        return (
            int(2 * d * self.COS30 * self.scale) + 2 * self.margin,
            int((ny + 2 * d * self.SIN30) * self.scale) + 2 * self.margin,
        )

    def turned(self, x: float, z: float) -> tuple[float, float]:
        """The horizontal coordinates about the cube's centre, turned by the
        angle."""
        nx, _, nz = self.shape
        cx, cz = (nx - 1) / 2, (nz - 1) / 2
        dx, dz = x - cx, z - cz
        c, s_ = math.cos(self.angle), math.sin(self.angle)
        return dx * c - dz * s_, dx * s_ + dz * c

    def project(self, x: float, y: float, z: float) -> tuple[float, float]:
        _, ny, _ = self.shape
        d = self.diagonal
        xr, zr = self.turned(x, z)
        u = self.margin + (d * self.COS30 + (xr - zr) * self.COS30) * self.scale
        v = self.margin + (ny - y + d * self.SIN30 + (xr + zr) * self.SIN30) * self.scale
        return u, v

    def depth(self, x: float, y: float, z: float) -> float:
        """Larger is nearer the viewer: drawn later."""
        xr, zr = self.turned(x, z)
        return xr + zr + y * 0.5

    def edges(self, draw: ImageDraw.ImageDraw, k: int) -> None:
        nx, ny, nz = self.shape
        c = [(x, y, z) for x in (-0.5, nx - 0.5) for y in (-0.5, ny - 0.5) for z in (-0.5, nz - 0.5)]
        for a in c:
            for b in c:
                if sum(1 for i in range(3) if a[i] != b[i]) == 1 and a < b:
                    near = (a[0] + a[1] + a[2] + b[0] + b[1] + b[2]) > (nx + ny + nz - 3)
                    pa, pb = self.project(*a), self.project(*b)
                    draw.line(
                        [(pa[0] * k, pa[1] * k), (pb[0] * k, pb[1] * k)],
                        fill=(96, 102, 124, 255) if near else (52, 56, 72, 255),
                        width=max(1, k // 2),
                    )

    def nodes(self, frame: Frame) -> list[tuple[int, int, int, tuple[int, int, int], int, float]]:
        """Per lit Node and family: (x, y, z, colour, alpha, radius factor),
        the copies of a body in its colour (its phase hue for a phased
        family), the other rows in their family's colour, dimmed by the
        family's weight; the amount sets the alpha."""
        out: list[tuple[int, int, int, tuple[int, int, int], int, float]] = []
        numbers = {body.number: body for body in frame.bodies}
        for rows in frame.rows:
            if rows.amount.size == 0:
                continue
            weight = self.weights.get(rows.family, 1.0)
            if weight <= 0:
                continue
            packed = rows.x * 1_000_000 + rows.y * 1000 + rows.z
            unique, inverse = np.unique(packed, return_inverse=True)
            total = np.zeros(unique.size)
            np.add.at(total, inverse, rows.amount.astype(np.float64))
            largest = max(self.largest.get(rows.family, float(total.max())), 1.0)
            angle = rows.phase.astype(np.float64) * (2 * math.pi / self.phase_steps)
            cx = np.zeros(unique.size)
            sy = np.zeros(unique.size)
            np.add.at(cx, inverse, rows.amount * np.cos(angle))
            np.add.at(sy, inverse, rows.amount * np.sin(angle))
            youngest = np.full(unique.size, AGE_FADE * 4, dtype=np.float64)
            np.minimum.at(youngest, inverse, rows.age.astype(np.float64))
            owner = np.full(unique.size, -1, dtype=np.int64)
            for n in numbers:
                mine = rows.number == n
                if mine.any():
                    owner[np.unique(inverse[mine])] = n
            for idx in range(unique.size):
                node = int(unique[idx])
                x, y, z = node // 1_000_000, (node // 1000) % 1000, node % 1000
                level = math.log2(1.0 + total[idx]) / math.log2(1.0 + largest)
                fade = 0.3 + 0.7 * max(0.0, 1.0 - youngest[idx] / AGE_FADE)
                body = numbers.get(int(owner[idx]))
                if self.copies and body is not None and (x, y, z) != body.position:
                    colour = BODY_COLOURS.get(body.family, (230, 230, 230))
                    if self.phased.get(rows.family, False):
                        colour = phase_colour(
                            math.atan2(sy[idx], cx[idx]) / (2 * math.pi) * self.phase_steps,
                            self.phase_steps,
                        )
                    out.append((x, y, z, colour, int((22 + 90 * level) * fade), 0.34 + 0.14 * fade))
                else:
                    if self.phased.get(rows.family, False):
                        colour = phase_colour(
                            math.atan2(sy[idx], cx[idx]) / (2 * math.pi) * self.phase_steps,
                            self.phase_steps,
                        )
                    else:
                        colour = self.colours[rows.family]
                    out.append((x, y, z, colour, int((26 + 100 * level) * weight), 0.34))
        return out

    def image(self, frame: Frame) -> Image.Image:
        k = SUPERSAMPLE // 2 or 1
        w, h = self.size
        over = Image.new("RGBA", (w * k, h * k), (14, 16, 24, 255))
        draw = ImageDraw.Draw(over)
        self.edges(draw, k)
        items = self.nodes(frame)
        items.sort(key=lambda t: self.depth(t[0], t[1], t[2]))
        base = max(self.scale * 0.5, 1.5)
        for x, y, z, colour, alpha, factor in items:
            r = base * factor / 0.5
            u, v = self.project(x, y, z)
            draw.ellipse([(u - r) * k, (v - r) * k, (u + r) * k, (v + r) * k], fill=(*colour, alpha))
        radius = max(self.scale * self.body_radius, 3.0)
        for body in sorted(frame.bodies, key=lambda b: self.depth(*b.position)):
            u, v = self.project(*body.position)
            colour = BODY_COLOURS.get(body.family, (230, 230, 230))
            if body.family in self.dot_bodies:
                dot = max(self.scale * 0.22, 1.5)
                draw.ellipse(
                    [(u - dot) * k, (v - dot) * k, (u + dot) * k, (v + dot) * k], fill=(*colour, 110)
                )
                continue
            if body.family in self.phase_bodies:
                colour = phase_colour(body.phase, self.phase_steps)
            glow = radius * 1.9
            draw.ellipse(
                [(u - glow) * k, (v - glow) * k, (u + glow) * k, (v + glow) * k], fill=(*colour, 55)
            )
            draw.ellipse(
                [(u - radius) * k, (v - radius) * k, (u + radius) * k, (v + radius) * k],
                fill=(*colour, 255),
                outline=(245, 245, 245, 255),
                width=max(1, k // 2),
            )
            px, py, pz = body.momentum
            if px or py or pz:
                du, dv = self.project(px, py, pz)
                ou, ov = self.project(0, 0, 0)
                ux, uy = du - ou, dv - ov
                norm = math.hypot(ux, uy)
                if norm > 0:
                    ux, uy = ux / norm, uy / norm
                    arrow(
                        draw,
                        (u + ux * radius, v + uy * radius),
                        (ux, uy),
                        max(1.8 * self.scale, 14.0),
                        max(2.0, self.scale / 5),
                        k,
                    )
        for rows in frame.rows:
            if rows.family not in self.arrow_families:
                continue
            for j in range(rows.amount.size):
                d = self.directions[int(rows.direction[j])]
                if not any(d):
                    continue
                du, dv = self.project(*d)
                ou, ov = self.project(0, 0, 0)
                ux, uy = du - ou, dv - ov
                norm = math.hypot(ux, uy)
                if norm == 0:
                    continue
                u, v = self.project(int(rows.x[j]), int(rows.y[j]), int(rows.z[j]))
                arrow(
                    draw,
                    (u, v),
                    (ux / norm, uy / norm),
                    max(self.scale * 1.3, 9.0),
                    max(1.5, self.scale / 6),
                    k,
                )
        return over.resize((w, h), Image.LANCZOS).convert("RGB")


def volume_for(replay: Replay, scale: int) -> Volume:
    world = replay.world
    return Volume(
        tuple(world.shape),
        scale,
        world.phase_steps,
        {family.name: bool(family.phase) for family in world.families},
        {
            family.name: FAMILY_COLOURS[i % len(FAMILY_COLOURS)]
            for i, family in enumerate(world.families)
        },
        list(replay.directions),
    )


def volume_player(
    key: str,
    world: Path,
    ticks: Sequence[int],
    scale: int,
    caption: str,
    duration_ms: int,
    weights: dict[str, float] | None = None,
    phase_bodies: set[str] | None = None,
    arrow_families: set[str] | None = None,
    dot_bodies: set[str] | None = None,
    copies: bool = True,
) -> Player:
    replay = Replay(world)
    frames = replay.run(ticks)
    volume = volume_for(replay, scale)
    volume.largest = largest_amounts(frames)
    volume.dot_bodies = dot_bodies or set()
    volume.copies = copies
    volume.weights = weights or {}
    volume.phase_bodies = phase_bodies or set()
    volume.arrow_families = arrow_families or set()
    images = []
    for index, frame in enumerate(frames):
        # The cube turns slowly: a full turn over TURN_FRAMES frames.
        volume.angle = 2 * math.pi * index / TURN_FRAMES
        images.append(volume.image(frame))
    readings = [
        {
            "rows on the GameBoard (GameBoard reading)": num(
                int(sum(int(r.amount.sum()) for r in frame.rows))
            ),
            "the bodies (number: family at Node)": "; ".join(
                f"{b.number}: {b.family} at {b.position}" for b in frame.bodies
            )
            or "none",
        }
        for frame in frames
    ]
    return Player(
        key,
        images,
        list(ticks),
        readings,
        caption + " " + COPIES_NOTE if copies else caption,
        duration_ms,
        colours=64,
    )


@register("volume")
def page_volume(out: Path, runs: Path | None) -> Path:
    """(9) In three dimensions: the deuteron, the free neutron's decay, the
    atom and the beam beside the mass, the whole GameBoard drawn in an
    isometric projection."""
    deuteron = volume_player(
        "volume_deuteron",
        WORLDS / "nucleus" / "deuteron_1.json",
        list(range(0, 49, 2)),
        6,
        "The deuteron at one Link, `deuteron_1` (series I), the whole 21^3 cube, one frame per two intervals: the proton "
        "and the neutron releasing their rows on the 290 directions into the Nodes beside them, the strong rows "
        "(gold) clicking on the border at three Links, the p and n rows flying to the faces.",
        120,
        weights={"p": 0.45, "n": 0.45, "nuclear": 1.0},
    )
    decay = volume_player(
        "volume_decay",
        WORLDS / "weak" / "j3_neutron_free.json",
        list(range(504, 546)),
        6,
        "The free neutron's decay, `j3_neutron_free` (series J), the whole 21^3 cube from the interval 504, one "
        "frame per interval: the transformation at 512, the beta and the neutrino leaving on their directions "
        "(the arrows), the beta's click on the shell of readers at r = 8, the neutrino out through a face.",
        150,
        weights={"n": 0.3, "p": 0.3, "nuclear": 0.6, "beta": 1.0, "nu": 1.0, "d": 0.0},
        arrow_families={"beta", "nu"},
        dot_bodies={"d"},
    )
    atom_release = volume_player(
        "volume_atom_release",
        WORLDS / "bohr" / "r8.json",
        list(range(0, 49, 2)),
        3,
        "The atom, `r8` (series H), the whole 45^3 cube at its first 48 intervals, one frame per two intervals: the "
        "proton's shells of 2616 rows leaving every 10 intervals, the electron (coloured by its phase) with its "
        "momentum arrow releasing its rows on its four directions.",
        120,
        weights={"p": 0.4, "e": 0.0},
        phase_bodies={"e"},
    )
    atom_orbit = volume_player(
        "volume_atom_orbit",
        WORLDS / "bohr" / "r8.json",
        frame_ticks(3900, 40),
        3,
        "The atom, `r8`, the orbit over 3900 intervals, one frame per 100: the electron circling the proton in the "
        "plane z = 22 of the cube, its copies and its arrow turning with it.",
        120,
        weights={"p": 0.4, "e": 0.0},
        phase_bodies={"e"},
    )
    lens = volume_player(
        "volume_lens",
        WORLDS / "lensing" / "mass_meeting.json",
        frame_ticks(400, 40),
        3,
        "The beam beside the mass, `mass_meeting` (series K under the meeting), the whole 57 x 41 x 41 box, one "
        "frame per 10 intervals: the lamp's rows (coloured by their phase) passing the mass and bent toward "
        "it, the mass's crowd of 290 directions dimmed, the screen at x = 54.",
        100,
        weights={"m": 0.25, "light": 1.0, "wall": 0.0},
        dot_bodies={"wall"},
    )
    body = f"""
<p class="demo"><b>Registered worlds</b>, run as declared and replayed in process; the same runs as the pages
of the plane (the nucleus, the decay, the atom, high-energy rows), now the whole GameBoard drawn in three
dimensions. Nothing changed in any world, nothing pinned.</p>
<h2>The GameBoard in three dimensions</h2>
<p>An isometric projection of the cube, turning slowly about its vertical axis as the frames play (a full
turn over 150 frames): at the start x is to the right and down, z to the left and down, y up; the near
edges brighter. Every Node with rows is a translucent disc, the rows of one Node and family added (their
amount the alpha), drawn from the far corner to the near one; a body's own rows are its copies, discs in
its colour (the phase hue for a family with a phase circle) with a rim; the body a disc with a glow and its
momentum arrow projected. The model owner, 2026-09-21: "now show all of these in three dimensions".</p>
{
        legend(
            [
                ("the p rows", swatch(FAMILY_COLOURS[0])),
                ("the n rows", swatch(FAMILY_COLOURS[1])),
                ("the nuclear rows (the strong column)", swatch(FAMILY_COLOURS[2])),
                ("a row of a family with a phase circle, by its phase", '<i class="wheel"></i>'),
                ("a proton", swatch(BODY_COLOURS["p"])),
                ("a neutron", swatch(BODY_COLOURS["n"])),
                ("the mass", swatch(BODY_COLOURS["m"])),
                ("the lamp", swatch(BODY_COLOURS["light"])),
            ]
        )
    }
<h2>The nucleus: the deuteron releasing itself</h2>
{deuteron.html()}
<h2>The decay: the free neutron becoming a proton</h2>
{decay.html()}
<h2>The atom: the release</h2>
{atom_release.html()}
<h2>The atom: the orbit</h2>
{atom_orbit.html()}
<h2>High-energy rows: the beam beside the mass</h2>
{lens.html()}
<h2>The readings</h2>
<p>The numbers of these runs are on their pages of the plane, with their sources: <a href="nucleus.html">the
nucleus</a>, <a href="decay.html">the decay</a>, <a href="atom.html">the atom</a>,
<a href="energy.html">high-energy rows</a>; the collision page is already drawn in three dimensions. The
moving pictures here are GameBoard readings, the host's view of the replay's stores.</p>
{
        sources(
            [
                (
                    "the worlds",
                    "<code>examples/events/nucleus/deuteron_1.json</code>, <code>weak/j3_neutron_free.json</code>, <code>bohr/r8.json</code>, <code>lensing/mass_meeting.json</code> (registered), replayed in process as declared",
                ),
                (
                    "the frames",
                    "each world replayed through <code>NatureBeamSimulation</code>, the stores read at the drawn intervals and projected (a GameBoard reading)",
                ),
                ("the builder", "<code>tools/gallery_pages.py</code>, the volume renderer"),
            ]
        )
    }
"""
    return write_page(
        out,
        "volume",
        page(
            "In three dimensions",
            "The nucleus, the decay, the atom and the beam beside the mass, the whole GameBoard drawn in an isometric projection.",
            body,
        ),
    )


# ---------------------------------------------------------------------------
# Page 10: the octahedron, the 48 and the general formula (the model owner,
# 2026-09-21: "what follows exactly from our formula is an octahedron ...
# 48 in the matrix, 24 rotations and 24 transformations; yes, build it").
# ---------------------------------------------------------------------------

PORT_LABELS = ("+x", "-x", "+y", "-y", "+z", "-z")
PORT_VECTORS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
PORT_COLOURS = (
    (255, 96, 96),
    (255, 168, 72),
    (88, 168, 255),
    (176, 128, 255),
    (255, 224, 72),
    (88, 220, 210),
)
# The inradius of the octahedron whose vertices are the six Ports at one
# Link: the face x + y + z = 1 lies at 1 / sqrt 3 from the centre. It is the
# law's c (HIGHLIGHTS 5.7, "Straightness and one pace": the largest
# isotropic pace at which no direction crosses two Links in one interval,
# equality on the cube diagonals).
INRADIUS = 1.0 / math.sqrt(3.0)
OCTAHEDRON_EDGES = tuple(
    (i, j)
    for i in range(6)
    for j in range(i + 1, 6)
    if PORT_VECTORS[i] != tuple(-c for c in PORT_VECTORS[j])
)
CUBE_CORNERS = tuple((x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1))
CUBE_EDGES = tuple(
    (a, b)
    for a in range(8)
    for b in range(a + 1, 8)
    if sum(1 for i in range(3) if CUBE_CORNERS[a][i] != CUBE_CORNERS[b][i]) == 1
)


def permutation_sign(perm: Sequence[int]) -> int:
    sign = 1
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                sign = -sign
    return sign


def signed_permutations() -> list[np.ndarray]:
    """The 48 signed axis permutations, the maps of the six Ports onto
    themselves that send opposite Ports to opposite Ports: 3! orderings of
    the axes times 2^3 choices of sign. The 24 of determinant +1 (the
    rotations) come first, then the 24 of determinant -1 (the reflections,
    the inversion among them); the determinant is the sign of the
    permutation times the product of the signs, in integers (record 226 of
    docs/LOG_2026-09-20.md; docs/designs/hand/FORM.md section 2). Column i
    of g is the image of the axis i."""
    proper: list[np.ndarray] = []
    improper: list[np.ndarray] = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            g = np.zeros((3, 3), dtype=np.int64)
            for i in range(3):
                g[perm[i], i] = signs[i]
            det = permutation_sign(perm) * signs[0] * signs[1] * signs[2]
            (proper if det == 1 else improper).append(g)
    return proper + improper


def determinant(g: np.ndarray) -> int:
    """The determinant of a signed permutation matrix, in integers."""
    perm = [int(np.nonzero(g[:, i])[0][0]) for i in range(3)]
    signs = [int(g[perm[i], i]) for i in range(3)]
    return permutation_sign(perm) * signs[0] * signs[1] * signs[2]


def fixed_vector(g: np.ndarray) -> tuple[int, int, int]:
    """The first nonzero v in {-1, 0, 1}^3 with g v = v (the axis of a
    rotation, the normal of a reflection of -g)."""
    for v in itertools.product((1, 0, -1), repeat=3):
        if any(v) and (g @ np.array(v) == np.array(v)).all():
            return v
    raise ValueError("no fixed vector")


def vector_text(v: Sequence[int]) -> str:
    return "(" + ", ".join(str(int(c)) for c in v) + ")"


def symmetry_name(g: np.ndarray) -> str:
    """What one of the 48 does, read from its determinant and its trace: a
    rotation (det +1) is the identity (trace 3), a half turn (trace -1), a
    quarter turn (trace 1) or a third turn (trace 0) about its fixed axis;
    an improper one (det -1) is the inversion (trace -3), a reflection in a
    plane (trace 1), or a quarter turn (trace -1) or a sixth turn (trace 0)
    followed by the reflection across its axis."""
    det = determinant(g)
    trace = int(np.trace(g))
    if det == 1:
        if trace == 3:
            return "the identity"
        angle = {-1: 180, 1: 90, 0: 120}[trace]
        return f"a rotation by {angle} degrees about {axis_text(fixed_vector(g))}"
    if trace == -3:
        return "the inversion, every Port to its opposite"
    if trace == 1:
        return f"a reflection in the plane across {axis_text(fixed_vector(-g))}"
    angle = {-1: 90, 0: 60}[trace]
    return (
        f"a rotation by {angle} degrees about {axis_text(fixed_vector(-g))} with the "
        "reflection across it"
    )


def axis_text(v: Sequence[int]) -> str:
    """An axis by its kind: through a Port, through an edge's midpoint, or
    a diagonal of the cube (through a face's centre)."""
    kind = {1: "the Port axis", 2: "the edge axis", 3: "the diagonal"}[sum(1 for c in v if c)]
    return f"{kind} {vector_text(v)}"


def port_image(g: np.ndarray) -> list[int]:
    """The polar image of the six Ports in Port order: the index of the
    Port that g sends each Port to (the table of hand/FORM.md section 2)."""
    images = []
    for v in PORT_VECTORS:
        w = tuple(int(c) for c in g @ np.array(v))
        images.append(PORT_VECTORS.index(w))
    return images


def symmetry_classes(matrices: Sequence[np.ndarray]) -> list[tuple[str, int]]:
    """The kinds among the 48 with their counts, in the order first met."""
    counts: dict[str, int] = {}
    for g in matrices:
        name = symmetry_name(g)
        kind = name
        for axis_kind in ("the Port axis", "the edge axis", "the diagonal"):
            if axis_kind in name:
                kind = name.split(axis_kind)[0] + axis_kind
                if "with the reflection" in name:
                    kind += " with the reflection across it"
        counts[kind] = counts.get(kind, 0) + 1
    return list(counts.items())


@dataclass
class Solid:
    """The octahedron of the six Ports (the vertices at one Link on the
    axes: the L1 ball, one Link per interval along an axis), the sphere
    inscribed in it (its radius 1 / sqrt 3, the law's c) and the cube whose
    face centres are the six Ports (the 48 are the cube's symmetries too),
    drawn in the isometric projection of the three-dimensional pages,
    turned about the vertical axis by an angle; drawn at SUPERSAMPLE times
    the size and downsampled. The projection is an orthographic one scaled
    by sqrt 1.5, so the sphere projects to a circle."""

    scale: int
    angle: float = 0.0
    margin: int = 28
    labels: bool = True

    COS30 = math.cos(math.pi / 6)
    SIN30 = math.sin(math.pi / 6)
    PROJECTION_GAIN = math.sqrt(1.5)

    @property
    def size(self) -> tuple[int, int]:
        return (
            int(2 * 1.9 * self.scale) + 2 * self.margin,
            int(2 * 2.1 * self.scale) + 2 * self.margin,
        )

    @property
    def centre(self) -> tuple[float, float]:
        w, h = self.size
        return w / 2, h / 2

    def turned(self, x: float, z: float) -> tuple[float, float]:
        c, s_ = math.cos(self.angle), math.sin(self.angle)
        return x * c - z * s_, x * s_ + z * c

    def project(self, x: float, y: float, z: float) -> tuple[float, float]:
        cx, cy = self.centre
        xr, zr = self.turned(x, z)
        return (
            cx + (xr - zr) * self.COS30 * self.scale,
            cy + (-y + (xr + zr) * self.SIN30) * self.scale,
        )

    def depth(self, x: float, y: float, z: float) -> float:
        """Larger is nearer the viewer: the projection looks along (1, 1, 1)
        of the turned solid."""
        xr, zr = self.turned(x, z)
        return xr + zr + y

    def image(
        self,
        mapping: np.ndarray | None = None,
        axis: Sequence[int] | None = None,
        sphere: bool = True,
        cube: bool = True,
        radius_line: bool = True,
    ) -> Image.Image:
        """The solid; with a mapping g, the octahedron after g: every Port's
        disc drawn at g's image of it, in the Port's own colour."""
        k = SUPERSAMPLE
        w, h = self.size
        over = Image.new("RGBA", (w * k, h * k), (14, 16, 24, 255))
        draw = ImageDraw.Draw(over)
        g = np.eye(3, dtype=np.int64) if mapping is None else mapping
        positions = [tuple(int(c) for c in g @ np.array(v)) for v in PORT_VECTORS]

        def line(a: Sequence[float], b: Sequence[float], colour: tuple[int, ...], width: float) -> None:
            pa, pb = self.project(*a), self.project(*b)
            draw.line(
                [(pa[0] * k, pa[1] * k), (pb[0] * k, pb[1] * k)],
                fill=colour,
                width=max(1, int(width * k)),
            )

        def composite(layer: Image.Image) -> None:
            nonlocal over, draw
            over = Image.alpha_composite(over, layer)
            draw = ImageDraw.Draw(over)

        if cube:
            for a, b in CUBE_EDGES:
                line(CUBE_CORNERS[a], CUBE_CORNERS[b], (58, 62, 80, 255), 0.6)
        for v in PORT_VECTORS[::2]:
            line(tuple(-c for c in v), v, (46, 50, 64, 255), 0.5)
        if axis is not None:
            n = math.sqrt(sum(c * c for c in axis))
            far = tuple(1.6 * c / n for c in axis)
            layer = Image.new("RGBA", over.size, (0, 0, 0, 0))
            pa, pb = self.project(*[-c for c in far]), self.project(*far)
            ImageDraw.Draw(layer).line(
                [(pa[0] * k, pa[1] * k), (pb[0] * k, pb[1] * k)],
                fill=(*ACCENT, 170),
                width=max(1, int(1.2 * k)),
            )
            composite(layer)
        # The back edges, then the sphere, then the front edges and vertices.
        edges = sorted(
            OCTAHEDRON_EDGES,
            key=lambda e: self.depth(
                *[(p + q) / 2 for p, q in zip(positions[e[0]], positions[e[1]], strict=True)]
            ),
        )
        back = [
            e
            for e in edges
            if self.depth(*[(p + q) / 2 for p, q in zip(positions[e[0]], positions[e[1]], strict=True)])
            < 0
        ]
        front = [e for e in edges if e not in back]
        for i, j in back:
            line(positions[i], positions[j], (120, 126, 150, 255), 0.9)
        if sphere:
            cx, cy = self.project(0, 0, 0)
            r = INRADIUS * self.PROJECTION_GAIN * self.scale
            # The eight points where the sphere touches the faces, on the
            # cube's diagonals: the ones behind the sphere first, dim.
            touches = [tuple(INRADIUS / math.sqrt(3.0) * c for c in corner) for corner in CUBE_CORNERS]
            dot = self.scale * 0.035

            def touch_dots(front: bool) -> None:
                for t in touches:
                    if (self.depth(*t) >= 0) != front:
                        continue
                    tx, ty = self.project(*t)
                    draw.ellipse(
                        [(tx - dot) * k, (ty - dot) * k, (tx + dot) * k, (ty + dot) * k],
                        fill=(*ACCENT, 255) if front else (40, 110, 70, 255),
                    )

            touch_dots(False)
            layer = Image.new("RGBA", over.size, (0, 0, 0, 0))
            ImageDraw.Draw(layer).ellipse(
                [(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k],
                fill=(*ACCENT, 60),
                outline=(*ACCENT, 210),
                width=max(1, int(0.8 * k)),
            )
            composite(layer)
            if radius_line:
                # The radius to the nearest of the four lower touching points.
                touch = max((t for t in touches if t[1] < 0), key=lambda t: self.depth(*t))
                line((0, 0, 0), touch, (*ACCENT, 255), 1.0)
            touch_dots(True)
        for i, j in front:
            line(positions[i], positions[j], (222, 228, 240, 255), 1.3)
        order = sorted(range(6), key=lambda i: self.depth(*positions[i]))
        f = font(max(10, int(self.scale * 0.22)))
        for i in order:
            px, py = self.project(*positions[i])
            near = self.depth(*positions[i]) >= 0
            colour = PORT_COLOURS[i] if near else tuple(int(c * 0.6) for c in PORT_COLOURS[i])
            r = self.scale * (0.11 if near else 0.085)
            draw.ellipse(
                [(px - r) * k, (py - r) * k, (px + r) * k, (py + r) * k],
                fill=(*colour, 255),
                outline=(14, 16, 24, 255),
                width=max(1, int(0.5 * k)),
            )
        out = over.resize((w, h), Image.Resampling.LANCZOS).convert("RGB")
        if self.labels:
            text = ImageDraw.Draw(out)
            for i in order:
                px, py = self.project(*positions[i])
                dx = 1 if positions[i][0] + positions[i][2] >= 0 else -1
                label = PORT_LABELS[i]
                text.text(
                    (
                        px + dx * self.scale * 0.16 - (0 if dx > 0 else f.getlength(label)),
                        py - self.scale * 0.16,
                    ),
                    label,
                    fill=PORT_COLOURS[i],
                    font=f,
                )
            if sphere and radius_line:
                touch = max(
                    (
                        tuple(INRADIUS / math.sqrt(3.0) * c for c in corner)
                        for corner in CUBE_CORNERS
                        if corner[1] < 0
                    ),
                    key=lambda t: self.depth(*t),
                )
                tx, ty = self.project(*[0.5 * c for c in touch])
                text.text((tx + 4, ty - self.scale * 0.26), "c", fill=ACCENT, font=f)
        return out


def octahedron_player(frames: int, scale: int) -> Player:
    solid = Solid(scale)
    images = []
    for index in range(frames):
        solid.angle = 2 * math.pi * index / frames
        images.append(solid.image())
    readings = [
        {
            "the vertices": "the six Ports, one Link from the Node on its three axes",
            "the sphere": f"radius 1 / sqrt 3 = {INRADIUS:.5f} Links per interval, the law's c",
            "the sphere touches the faces at": "(+-1, +-1, +-1) / 3, the cube's diagonals",
            "the turn": f"{index + 1} of {frames}",
        }
        for index in range(frames)
    ]
    return Player(
        "octahedron",
        images,
        list(range(frames)),
        readings,
        "The octahedron of the six Ports (its vertices the Ports +x, -x, +y, -y, +z, -z at one Link, its "
        "faces the L1 bound |x| + |y| + |z| = 1: one Link per interval), the sphere inscribed in it, of "
        "radius 1 / sqrt 3 = c (green), touching the eight faces on the cube's diagonals, and the cube "
        "whose face centres are the six Ports (faint). The solid turns slowly about the vertical axis; the "
        "frame counter is the turn, not an interval of any run.",
        duration_ms=80,
        colours=64,
    )


def matrix_lines(g: np.ndarray) -> list[str]:
    return ["  ".join(f"{int(c):>2d}" for c in row) for row in g]


def the_48_player(scale: int) -> Player:
    """One frame per signed axis permutation: the octahedron before and
    after it, its matrix, its determinant, its kind and the hand's bit."""
    matrices = signed_permutations()
    before = Solid(scale, angle=0.55, labels=True)
    after = Solid(scale, angle=0.55, labels=True)
    w, h = before.size
    gap = int(scale * 2.4)
    width = 2 * w + gap
    height = h + int(scale * 1.1)
    title_font = font(max(12, int(scale * 0.24)))
    mono = font(max(12, int(scale * 0.28)))
    images = []
    readings = []
    for index, g in enumerate(matrices):
        det = determinant(g)
        name = symmetry_name(g)
        axis: Sequence[int] | None = None
        if " about " in name:
            axis = fixed_vector(g if det == 1 else -g)
        elif "in the plane across" in name:
            axis = fixed_vector(-g)
        left = before.image(sphere=False, cube=True, radius_line=False)
        right = after.image(mapping=g, axis=axis, sphere=False, cube=True, radius_line=False)
        canvas = Image.new("RGB", (width, height), (14, 16, 24))
        top = int(scale * 1.1)
        canvas.paste(left, (0, top))
        canvas.paste(right, (w + gap, top))
        draw = ImageDraw.Draw(canvas)
        half = "of the 24 rotations" if det == 1 else "of the 24 improper ones"
        ordinal = index + 1 if det == 1 else index + 1 - 24
        head = f"g {index + 1} of 48: {ordinal} {half}; det {det:+d}"
        draw.text((12, 8), head, fill=(232, 236, 239), font=title_font)
        draw.text((12, 8 + int(scale * 0.34)), name, fill=(154, 165, 173), font=title_font)
        draw.text(
            (12, 8 + int(scale * 0.68)),
            f"the hand: h -> {'+' if det == 1 else '-'}h",
            fill=ACCENT,
            font=title_font,
        )
        x0 = w + gap // 2
        y0 = top + h // 2 - int(scale * 0.5)
        for row, line in enumerate(matrix_lines(g)):
            draw.text(
                (x0 - mono.getlength(line) / 2, y0 + row * int(scale * 0.36)),
                line,
                fill=(232, 236, 239),
                font=mono,
            )
        draw.text(
            (x0 - mono.getlength("g") / 2, y0 - int(scale * 0.42)), "g", fill=(154, 165, 173), font=mono
        )
        draw.text((12, top + h - int(scale * 0.3)), "before", fill=(154, 165, 173), font=title_font)
        draw.text(
            (w + gap + 12, top + h - int(scale * 0.3)), "after g", fill=(154, 165, 173), font=title_font
        )
        images.append(canvas)
        readings.append(
            {
                "g": f"{index + 1} of 48 ({ordinal} {half})",
                "what it is": name,
                "det g": f"{det:+d}",
                "the polar image of (+x -x +y -y +z -z)": " ".join(str(i) for i in port_image(g)),
                "the hand h -> det(g) h": f"h -> {'+' if det == 1 else '-'}h",
            }
        )
    return Player(
        "the_48",
        images,
        list(range(48)),
        readings,
        "The 48 signed axis permutations, one per frame: the octahedron of the six Ports before (left) "
        "and after g (right, every Port's disc carried to its image in the Port's own colour; the green "
        "line the axis of a rotation or the normal of a reflection), the matrix g between them, its "
        "determinant, and the hand's bit, kept by the 24 rotations and flipped by the 24 improper ones. "
        "The frame counter is the index of g, not an interval of any run.",
        duration_ms=700,
        colours=64,
    )


def formula_html() -> str:
    """The general formula, drawn as cards: the state vectors, the map F of
    six verbs, the reading, the click, in the words of HIGHLIGHTS 5.7 with
    no claim added."""
    cards = [
        (
            "The state: three vectors",
            "<b>A row</b> (a message in flight) is a point of a product of circles and lines: its Node in "
            "Z<sub>X</sub> x Z<sub>Y</sub> x Z<sub>Z</sub>, its direction (an index of the fan F<sub>P</sub>), its "
            "phase on the circle Z<sub>N</sub>, its age, its amount and its number. <b>A record</b> is the vector "
            "<b>f</b> of Z<sup>N</sup> of the amounts that ended at each phase, an element of the group ring "
            "Z[Z<sub>N</sub>]. <b>A body</b> (a measured event) is its held contents, its momentum vector "
            "<b>p</b> and its counts table, one accumulator (s, r, d) per count. A Node is an index and holds "
            "nothing.",
        ),
        (
            "The map F: six verbs, no seventh",
            "<ol>"
            "<li><b>the translation</b> of an accumulator by its rate, s &lt;- s + r: the flight, the phase, "
            "the age, every count;</li>"
            "<li><b>the bilinear form</b> with a declared matrix: the coupling <b>C a</b>, the click's "
            "<b>G</b>, the moments;</li>"
            "<li><b>the group-ring addition</b> in Z[Z<sub>N</sub>]: the merge, an antiphase pair "
            "cancelling;</li>"
            "<li><b>the permutation</b>: the collision table, the gate;</li>"
            "<li><b>the evaluation</b> of the tables at zeta<sub>N</sub>, the primitive N-th root of unity;</li>"
            "<li><b>the Euclidean division</b> with the remainder kept: the carry that is the event, and the "
            "threshold.</li>"
            "</ol>"
            "Two places are not linear and there is no third: the carry (a bijection) and the click's "
            "threshold (the one read-out). A root at run time is outside the six.",
        ),
        (
            "The reading R: nobody sees the state",
            "A detector reads its Node's neighbourhood by one linear reading <b>R</b>: the moments of the "
            "arriving rows, order 0 a scalar (the presence), order 1 a vector (the flow, the pointer), order 2 "
            "a tensor (the spread) and the age moment: the content of the stress-energy tensor <b>T</b>. Every "
            "value compared with nature is such a reading; a GameBoard reading is a diagnostic.",
        ),
        (
            "The click: one threshold",
            "The click is one bilinear form on the record, the weight <b>f</b><sup>T</sup> <b>G f</b> with "
            "<b>G</b> = <b>E</b><sup>T</sup> <b>E</b> the Gram matrix of the rounded cosine and sine tables, "
            "then one threshold [u &lt; b<sub>k</sub>] against the rungs of the cells' cumulative weights, u "
            "the lamp's wheel written on the record at its birth. The click discards information by design, "
            "the law's one cost.",
        ),
        (
            "The symmetry: 48 = 3! x 2<sup>3</sup> = 24 + 24",
            "The maps of the six Ports onto themselves that send opposite Ports to opposite Ports are the "
            "signed permutations of the three axes: 3! orderings times 2<sup>3</sup> signs, 48 in all, the "
            "symmetry group of the octahedron and of the cube. The determinant splits them: 24 of determinant "
            "+1, the rotations, and 24 of determinant -1, the reflections with the inversion among them. The "
            "hand of a row is a pseudoscalar: h -&gt; det(g) h, kept by the 24 rotations, flipped by the 24 "
            "improper ones. A Lorentz boost mixes a space step with a time step and is not among the 48: "
            "Lorentz's symmetry belongs to the limit, not to the group.",
        ),
        (
            "c from the octahedron",
            "The octahedron's faces are |x| + |y| + |z| = 1, one Link per interval: the L1 bound of a step. "
            "The sphere inscribed in it has radius 1 / sqrt 3, the distance from the centre to the face "
            "x + y + z = 1, and touches the faces where the cube's diagonals cross them. That is c: the "
            "largest isotropic pace at which no direction crosses two Links in one interval, with equality "
            "on the cube diagonals; derived, not declared. The flight table realises it in integers, 32 "
            "Links in 55 intervals on an axis.",
        ),
    ]
    items = "".join(f"<section><h3>{title}</h3><div>{body}</div></section>" for title, body in cards)
    return f'<div class="three formula">{items}</div>'


def formula_figures(out: Path, scale: int = 160) -> list[Path]:
    """Still pictures of the formula page for the paper (the model owner,
    2026-09-21: "send the paper writer to attach this shape"): the
    octahedron of the six Ports with the sphere of c, and a contact sheet
    of the 48 (the 24 rotations in the upper half, the 24 improper ones in
    the lower, six per row, each the octahedron after g with its matrix).
    Written as PNG at the given scale; nothing is read from a run."""
    out.mkdir(parents=True, exist_ok=True)
    solid = Solid(scale, angle=0.55)
    octahedron = out / "octahedron.png"
    solid.image().save(octahedron, optimize=True)
    small = Solid(scale // 3, angle=0.55, labels=True)
    w, h = small.size
    mono = font(max(10, int(small.scale * 0.3)))
    head = int(small.scale * 1.4)
    cell_h = h + head
    sheet = Image.new("RGB", (6 * w, 8 * cell_h + int(small.scale * 0.5)), (14, 16, 24))
    draw = ImageDraw.Draw(sheet)
    for index, g in enumerate(signed_permutations()):
        det = determinant(g)
        axis: Sequence[int] | None = None
        if " about " in symmetry_name(g):
            axis = fixed_vector(g if det == 1 else -g)
        elif "in the plane across" in symmetry_name(g):
            axis = fixed_vector(-g)
        column, row = index % 6, index // 6
        x0 = column * w
        y0 = row * cell_h + (int(small.scale * 0.5) if row >= 4 else 0)
        sheet.paste(small.image(mapping=g, axis=axis, sphere=False, radius_line=False), (x0, y0 + head))
        draw.text((x0 + 6, y0 + 2), f"g {index + 1}, det {det:+d}", fill=(232, 236, 239), font=mono)
        for line_index, line in enumerate(matrix_lines(g)):
            draw.text(
                (x0 + 6, y0 + int(small.scale * 0.34) * (line_index + 1)),
                line,
                fill=(154, 165, 173),
                font=mono,
            )
    contact = out / "the_48.png"
    sheet.save(contact, optimize=True)
    return [octahedron, contact]


@register("formula")
def page_formula(out: Path, runs: Path | None) -> Path:
    del runs  # no run: the page draws the law's geometry and its group
    matrices = signed_permutations()
    proper = [g for g in matrices if determinant(g) == 1]
    improper = [g for g in matrices if determinant(g) == -1]
    classes_proper = symmetry_classes(proper)
    classes_improper = symmetry_classes(improper)
    kinds = "".join(
        f'<tr><th>{html.escape(kind)}</th><td class="num">{count}</td></tr>'
        for kind, count in classes_proper + classes_improper
    )
    log = "../../LOG_2026-09-20.md"
    body = f"""
<p class="demo"><b>No run and no world</b>: this page draws the geometry of one Node and the group of its
six Ports, and states the general formula in the words of
<a href="../../HIGHLIGHTS.md">HIGHLIGHTS section 5.7</a>. Every count on it is enumerated by the page's
builder from the three axes; nothing is pinned and nothing enters the register.</p>
<p>The model owner, 2026-09-21 (translated): "what follows exactly from our formula is an octahedron;
that is what follows from our formula. And we have in the matrix 48, with 24 rotations and 24
transformations." The six Ports of a Node are the six vertices of an octahedron; the sphere inscribed in it
has the radius c; the symmetries of that octahedron are the 48 signed axis permutations, 24 rotations and
24 improper ones, and the hand tells the halves apart.</p>
<h2>The octahedron of the six Ports and the sphere of c</h2>
{
        legend(
            [
                (f"the Port {label}", swatch(colour))
                for label, colour in zip(PORT_LABELS, PORT_COLOURS, strict=True)
            ]
            + [("the sphere of radius c and its radius to a face", swatch(ACCENT))]
        )
    }
{octahedron_player(60, 70).html()}
<h2>The 48: 24 rotations and 24 improper ones</h2>
<p>The frames are the 48 matrices in the order the builder enumerates them, the 24 of determinant +1
first. Among the rotations: the identity, the quarter turns and the half turns about the axes of the
Ports, the half turns about the axes through the edges' midpoints, and the third turns about the cube's
diagonals; among the improper ones: the inversion, the reflections in the three planes of the Ports and
in the six diagonal planes, and the turns followed by a reflection. The counts, enumerated by the builder:</p>
<table><tr><th>The kind</th><th>Count</th></tr>{
        kinds
    }<tr><th>the rotations (det +1)</th><td class="num">{
        len(proper)
    }</td></tr><tr><th>the improper ones (det -1)</th><td class="num">{
        len(improper)
    }</td></tr><tr><th>all</th><td class="num">{len(matrices)}</td></tr></table>
{the_48_player(64).html()}
<h2>The general formula</h2>
<p><b>The statement</b> (the owner, record 181, in HIGHLIGHTS 5.7): the state is integer vectors on tori
and one tensor; the law is one map <b>F</b> (the interval's map) at every Node, made of six operations; the
GameBoard computes exactly where the formula has only a limit; the measurement is the one threshold read
out.</p>
{formula_html()}
<p>The three tests of every rule (record 202): generic (one primitive with declared integers, no family
name), vector (one of the six verbs, no root, no float), local (its own record and the six neighbours,
nothing kept at a Node). What is derived from the six verbs alone, what is not, and what is input are
listed in <a href="../../HIGHLIGHTS.md">HIGHLIGHTS 5.7</a> and derived in
<a href="../../DERIVATIONS_BEAM.md">DERIVATIONS_BEAM.md</a>; this page adds no claim.</p>
{
        sources(
            [
                (
                    "48 = 3! x 2^3, 24 + 24 by the determinant; not a constant of the law",
                    f'<a href="{log}">record 226</a> of the log of 2026-09-20; the matrices enumerated by <code>signed_permutations()</code> in <code>tools/gallery_pages.py</code>',
                ),
                (
                    "24 is the octahedron's 24 rotations; the boost is not among the 48",
                    f'<a href="{log}">record 231</a>',
                ),
                (
                    "the hand h -> det(g) h; the polar image of the six Ports per g",
                    '<a href="../../designs/hand/FORM.md">hand/FORM.md</a> section 2 (its first rows: the identity 0 1 2 3 4 5; z -> -z 0 1 2 3 5 4; y -> -y 0 1 3 2 4 5, reproduced by the player), <a href="'
                    + log
                    + '">record 142</a>',
                ),
                (
                    "the kinds and their counts",
                    "enumerated by <code>symmetry_name()</code> from the determinant and the trace of each g; the sum of the kinds is 24 and 24",
                ),
                (
                    "c = 1 / sqrt 3 derived (straightness and one pace)",
                    '<a href="../../HIGHLIGHTS.md">HIGHLIGHTS 5.7</a>, "The principles" (records 186, 191); the inradius of the octahedron with its vertices at one Link, computed as 1 / sqrt 3 = '
                    + f"{INRADIUS:.6f}"
                    + " by the builder",
                ),
                (
                    "32 Links in 55 intervals on an axis",
                    '<a href="../../BEAM_LAW.md">BEAM_LAW.md</a>, the flight table (32 / 55 = '
                    + f"{32 / 55:.5f}"
                    + " Links per interval against c = "
                    + f"{INRADIUS:.5f}"
                    + ")",
                ),
                (
                    "the 20 orbits of the collision table under the 48",
                    '<a href="../../BEAM_LAW.md">BEAM_LAW.md</a>, "The 20 orbits" (10 x 2; the group includes the reflections)',
                ),
                (
                    "the statement, the three conversions, the six verbs, the click",
                    '<a href="../../HIGHLIGHTS.md">HIGHLIGHTS 5.7</a> (records 173 to 198, 202); <a href="../../THREE_WORLDS.md">THREE_WORLDS.md</a>',
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "formula",
        page(
            "The octahedron and the 48",
            "One Node's six Ports are an octahedron; the sphere inside it has the radius c; its 48 "
            "symmetries are 24 rotations and 24 improper ones; the law is one map of six verbs.",
            body,
        ),
    )


# ---------------------------------------------------------------------------
# Page 11: the quarks (the model owner, 2026-09-21: "prepare one on the
# quarks too, one that can be broken apart by an electron moving fast at
# them: breaking a proton").
# ---------------------------------------------------------------------------


def quark_bodies_text(frame: Frame) -> str:
    return (
        "; ".join(f"{b.number}: {b.family} at {b.position}" for b in frame.bodies)
        or "none on the GameBoard (all left through the faces)"
    )


@register("quarks")
def page_quarks(out: Path, runs: Path | None) -> Path:
    """(11) The quarks, series R: the proton line u d u holding, the kicked
    quark walking off (the law binds and does not confine), and a
    demonstration: a fast electron thrown at the line."""
    folder = WORLDS / "quarks"
    demo_world = GALLERY_WORLDS / "proton_electron.json"
    weights = {"u": 0.35, "d": 0.35, "e": 0.25}
    line, line_record, line_events = nucleus_player(
        "proton_line",
        folder / "q1_proton_line.json",
        runs,
        list(range(0, 49)),
        "The proton line u d u, `q1_proton_line`: the plane z = 10 of the 21^3 cube (the bodies' plane, the "
        "rows in it alone), 14 pixels per Node; u at (9, 10, 10), d at (10, 10, 10), u at (11, 10, 10), each "
        "holding one unit of `glue` (gold rows, reaching three Links and clicking on the border `lifetime`). "
        "One frame per interval: the three bodies releasing their rows into the Nodes beside them; the line "
        "holds 3000 intervals with no step (the register's R).",
        120,
        weights=weights,
        on_top="glue",
        border_family="glue",
        scale=14,
    )
    kick, kick_record, kick_events = nucleus_player(
        "proton_kick",
        folder / "q6_proton_kick.json",
        runs,
        list(range(0, 91, 2)),
        "The kicked quark, `q6_proton_kick`: the left u thrown -x by 10^13 label units; it steps every seven "
        "intervals, its push falling to the electric residual beyond the reach, and leaves through the face "
        "-x (one frame per two intervals): the law binds and does not confine.",
        160,
        weights=weights,
        on_top="glue",
        border_family="glue",
        colours=64,
        scale=14,
    )
    hit, hit_record, hit_events = nucleus_player(
        "proton_electron",
        demo_world,
        runs,
        list(range(0, 121, 3)),
        "The fast electron, `proton_electron` (a demonstration world): the electron e (cyan) at (3, 10, 10) "
        "thrown +x at the line with 2 x 10^13 label units, about one Link per 1.4 intervals; what the law does "
        "when it reaches the first quark is what the frames show (one frame per three intervals): the contact through "
        "the table hands the momentum to the occupant, and a quark that walks off is not held back.",
        160,
        weights=weights,
        on_top="glue",
        border_family="glue",
        push_body=4,
        colours=64,
        scale=14,
    )
    volume = volume_player(
        "volume_proton_electron",
        demo_world,
        list(range(0, 121, 3)),
        6,
        "The same demonstration in three dimensions, one frame per three intervals, the cube turning slowly: "
        "the line of three quarks with their glue (the gold halo), the electron arriving on +x, the knocked "
        "quark leaving, with the arrows of their momentum labels. Here only the glue rows are drawn (their "
        "reach three Links, the strong column's range) and the bodies' copies are not: four bodies releasing "
        "on 290 directions fill the cube; the plane above shows the u, d and e rows and the copies.",
        100,
        weights={"u": 0.0, "d": 0.0, "glue": 0.4, "e": 0.0},
        copies=False,
    )

    def first_steps(events: dict[str, list[dict[str, object]]]) -> str:
        seen: dict[int, dict[str, object]] = {}
        for entry in events["step"]:
            seen.setdefault(int(entry["number"]), entry)  # type: ignore[arg-type]
        return (
            "; ".join(
                f"body {n} at the interval {entry['tick']} from {tuple(entry['node'])} to {tuple(entry['to'])}"  # type: ignore[arg-type]
                for n, entry in sorted(seen.items())
            )
            or "none"
        )

    def step_ticks(events: dict[str, list[dict[str, object]]], number: int, limit: int = 12) -> str:
        ticks = [int(e["tick"]) for e in events["step"] if int(e["number"]) == number]  # type: ignore[arg-type]
        text = ", ".join(str(t) for t in ticks[:limit])
        return (
            f"{text}{', ...' if len(ticks) > limit else ''} ({len(ticks)} steps in all)"
            if ticks
            else "none"
        )

    def exits(events: dict[str, list[dict[str, object]]]) -> str:
        return (
            "; ".join(
                f"body {e['measured']} through {e['detector']} at {e['tick']}" for e in events["exit"]
            )
            or "none"
        )

    def read_mass(world: Path) -> str:
        """The contents declared (the family's units and the held units),
        their sum what a detector reads as the set's mass."""
        declared = read_json(world)["measured"]
        assert isinstance(declared, list)
        parts = [int(m["amount"]) + sum(int(v) for v in m.get("held", {}).values()) for m in declared]
        return " + ".join(str(c) for c in parts) + " = " + str(sum(parts))

    hit_first_contact = min(
        (int(e["tick"]) for e in hit_events["contact"]),
        default=None,  # type: ignore[arg-type]
    )
    entry_url = "../../EXPERIMENTS.md#r-the-quarks-2026-09-21"
    body = f"""
{registered_note(folder / "q1_proton_line.json", "R, the quarks (2026-09-21)", entry_url)}
<p class="demo">Also registered there: <code>examples/events/quarks/q6_proton_kick.json</code>, run as declared.
Series R is a research run of a read-only design (<a href="../../designs/quarks/QUARKS.md">the quarks as
families of the family table</a>): the quarks are not rows of the law's family table today, and nothing on this
page changes that. The third world is a demonstration written for this page.</p>
{demonstration_note(demo_world)}
<h2>The GameBoard</h2>
<p>Series I's cube: 21 x 21 x 21 open Nodes, K = {num(1 << 20)}, N = 64, the width of the push 2^37, the
contact through the table, the fan of the 290 primitive directions with |a| + |b| + |c| at most 6. Three free
families without a phase circle: <code>u</code> (4 units of content, the charge 1224 per unit: the whole
charge 4896, 2/3 of the register's proton 7344), <code>d</code> (9 units at -272: -2448, -1/3) and
<code>glue</code> (the column <code>strong</code> of value 10 000 with the sign minus, the <code>lifetime</code>
3: series I's <code>nuclear</code> at the quark level). A <b>quark</b> is a body of <code>u</code> or
<code>d</code> holding one unit of <code>glue</code>; every body releases one row of its held content per
direction per interval; the push per interval between two bodies within the reach is
(Q<sub>A</sub> Q<sub>B</sub> - G<sub>A</sub> G<sub>B</sub> - M<sub>A</sub> M<sub>B</sub>) x U(r) per unit per
direction. In the demonstration a fourth family <code>e</code> (one unit of content, the charge -7344 per
unit, minus the proton's; no strong column) has one body at (3, 10, 10) with the momentum 2 x 10^13 label
units on +x: at the width 2^37 it steps one Link per (64 x 2^37 + p) / p = 1.44 self-creations. No detector
is declared: the bodies' <code>read</code> and <code>contact</code> records are the readings, the six faces and
the border <code>lifetime</code> the detectors of what leaves.</p>
{
        legend(
            [
                ("the u rows", swatch(FAMILY_COLOURS[0])),
                ("the d rows", swatch(FAMILY_COLOURS[1])),
                ("the glue rows (the strong column, lifetime 3)", swatch(FAMILY_COLOURS[2])),
                ("the e rows", swatch(FAMILY_COLOURS[3])),
                ("a u quark (a body of u)", swatch(BODY_COLOURS["u"])),
                ("a d quark (a body of d)", swatch(BODY_COLOURS["d"])),
                ("the electron (a body of e)", swatch(BODY_COLOURS["e"])),
            ]
        )
    }
<h2>Why this page</h2>
<p>The owner asked for the quarks: a proton that a fast electron can break apart. In series R the proton is
three quark bodies in a line, bound by the one coupling over the columns through the strong column of the
glue each holds, with the contact through the table: a body refused a step onto its neighbour's Node hands
its momentum component to the occupant. The register's verdict: the line holds, and a kicked quark walks
off, because the law binds and does not confine (nothing in it grows with distance). The demonstration throws
an electron at the line: the electron's charge pulls the u and pushes the d as it comes, and when it reaches
the first quark its momentum is handed over through the table. Whether the line breaks, which quark leaves
and what the electron does afterwards are read off the run below, not assumed.</p>
<h2>1. The proton line holds</h2>
{line.html()}
<h2>2. A kicked quark walks off</h2>
{kick.html()}
<h2>3. A fast electron thrown at the proton (a demonstration)</h2>
{hit.html()}
{volume.html()}
<h2>What the runs read</h2>
<table>
<tr><th>Reading (kind)</th><th>q1_proton_line</th><th>q6_proton_kick</th><th>proton_electron (demonstration)</th></tr>
<tr><th>the first step of each body (GAMEBOARD, step lines)</th><td>{
        html.escape(first_steps(line_events))
    }</td><td>{html.escape(first_steps(kick_events))}</td><td>{
        html.escape(first_steps(hit_events))
    }</td></tr>
<tr><th>the steps of the kicked or hit body (GAMEBOARD)</th><td>none</td><td>body 1: {
        html.escape(step_ticks(kick_events, 1))
    }</td><td>body 4, the electron: {html.escape(step_ticks(hit_events, 4))}</td></tr>
<tr><th>hand-overs over the run (contact lines)</th><td class="num">{
        num(len(line_events["contact"]))
    }</td><td class="num">{num(len(kick_events["contact"]))}</td><td class="num">{
        num(len(hit_events["contact"]))
    }</td></tr>
<tr><th>the first hand-over (contact lines)</th><td>{
        html.escape(str(min((int(e["tick"]) for e in line_events["contact"]), default="none")))
    }</td><td>{
        html.escape(str(min((int(e["tick"]) for e in kick_events["contact"]), default="none")))
    }</td><td>{
        html.escape(str(hit_first_contact) if hit_first_contact is not None else "none")
    }</td></tr>
<tr><th>what left through the faces (DETECTOR, face click lines)</th><td>{
        html.escape(exits(line_events))
    }</td><td>{html.escape(exits(kick_events))}</td><td>{html.escape(exits(hit_events))}</td></tr>
<tr><th>the contents declared, their sum the read mass (DETECTOR)</th><td>{
        html.escape(read_mass(folder / "q1_proton_line.json"))
    }</td><td>{html.escape(read_mass(folder / "q6_proton_kick.json"))}</td><td>{
        html.escape(read_mass(demo_world))
    }</td></tr>
<tr><th>the run's intervals (completed)</th><td class="num">{
        num(int(line_record["completed_ticks"]))
    }</td><td class="num">{num(int(kick_record["completed_ticks"]))}</td><td class="num">{
        num(int(hit_record["completed_ticks"]))
    }</td></tr>
</table>
<p>The register's pins for the two registered worlds (series R, read and compared there): the push at the
interval 20 on the ends of the line +-416 530 868 696 on x and 0 on the middle, exactly; no step in 3000
intervals; the read mass 20 units (the exact sum of the declared contents: nothing raises a bound set's mass
above its parts, the proton's 99 percent binding is not in the law); the kicked u steps -x at the intervals
6, 13, 20, ... every seven and leaves through <code>face:-x</code> at 63 with its charge 2/3 e, outside the
page's pin of 70 to 90 by seven intervals, reported and not moved. The demonstration has no pin: its
readings above are what its run did.</p>
{
        sources(
            [
                (
                    "the worlds q1_proton_line and q6_proton_kick, their families, fan, width and pins",
                    '<a href="../../../examples/events/quarks/README.md">examples/events/quarks/README.md</a>, <code>expectations.json</code>; the register, <a href="'
                    + entry_url
                    + '">R, the quarks (2026-09-21)</a>',
                ),
                (
                    "the design (read-only): the six quark rows, what the law lacks for confinement",
                    '<a href="../../designs/quarks/QUARKS.md">docs/designs/quarks/QUARKS.md</a> (sections 1, 2, 5); the owner\'s direction, records 249, 251 and 256 of the log of 2026-09-20',
                ),
                (
                    "the demonstration world",
                    f"<code>{relative(demo_world)}</code>, written by <code>examples/events/gallery/make_worlds.py</code> from <code>q1_proton_line.json</code> with the family <code>e</code> and its body added; the electron's charge -7344 is minus the register's proton (4 per unit on 1836 units); the throw 2 x 10^13 label units",
                ),
                (
                    "the steps, hand-overs, pushes and exits per frame",
                    "the runs' <code>events.jsonl</code> (the kinds step, contact, read, click) and <code>run.json</code> (the audit's transit lines), replayed in process for the pictures",
                ),
                (
                    "the runs' fingerprints",
                    f"q1 {fingerprint_line(line_record)}; q6 {fingerprint_line(kick_record)}; the demonstration {fingerprint_line(hit_record)}",
                ),
                (
                    "the step rule (one Link per (Q S M + p) / p self-creations) and the contact through the table",
                    '<a href="../../BEAM_LAW.md">BEAM_LAW.md</a>, note 31; <code>src/event_universe/events/engine.py</code>, <code>step_axis</code>',
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "quarks",
        page(
            "The quarks",
            "Series R: the proton of three quarks holding in a line, a kicked quark walking off, and a fast "
            "electron thrown at the proton; the law binds and does not confine.",
            body,
        ),
    )


# ---------------------------------------------------------------------------
# Page 12: Universe24, the formula and its derivations (the model owner, 2026-09-21: "my
# formula at the top, big; below it the small formulas with their
# explanation; then the comparison between me and Einstein, Lorentz and
# Newton, to see the derivations").
# ---------------------------------------------------------------------------

# The Einstein map of DERIVATIONS_BEAM.md section 21.4, one row per result:
# (number, Einstein's result, the status today, what the six verbs give,
# what must be added and under which identity, the pin a run would meet).
# R: reached; D: a different law as declared; N: not reached.
EINSTEIN_MAP = (
    (
        "E1",
        "Lorentz's symmetry of light, omega = c k, the light cone",
        "R",
        "the rows' limit is the wave equation at c (4.1, 5.1)",
        "nothing",
        "series K's ages, 89.40 in every world (registered)",
    ),
    (
        "E2",
        "gamma (the Lorentz factor), the time dilation of a moving clock",
        "D (the rate 1, 4.3; NATURE 4a)",
        "no operation carries a body's speed into its clock",
        "the self-creation gated by the proper-time owed count (17.6 M1), covariant-readings-v1",
        "J4's world of 17.6 M9: the products' face clicks at 367 and 345 (the decay at 70.9 and 125.2 derived), 391 at rest",
    ),
    (
        "E3",
        "the contraction 1 / gamma",
        "D (12b.2: 0.87 to 0.96 by the dispersion, unstable)",
        "the retarded flux push (12.1); -grad(A) alone gives the rest force along and gamma across (17.6 M4)",
        "the magnetic part of the push, which needs the source's velocity: source-velocity-v1, named, not designed",
        "none until then; the geometry when it comes: the thrown orbit at beta 0.43 or above, the extents' ratio 0.903",
    ),
    (
        "E4",
        "Doppler with gamma, 1 + z = gamma (1 + beta)",
        "D (the count 1 + beta, 2.2; NATURE 4b)",
        "the crossing count per interval, exact",
        "the count charged per self-creation, the cadence of 17.6 M1, covariant-readings-v1",
        "coasting_none's s_mz2 at its declared momentum: z = 0.369 +- 0.003",
    ),
    (
        "E5",
        "E = m c^2, the inertia of energy",
        "N (4.5, 12.4)",
        "E = h f for a row; the content and the momentum of a body untied",
        "E'_0 = Q S M forced by the Newtonian limit, W gaining on a change of content, the load-time identity 3 h n = Q S d (17.6 M3, M7), covariant-readings-v1",
        "a lamp emitting two opposite units keeps its pace, its W falling by the content identity per unit paid",
    ),
    (
        "E6",
        "the invariant E^2 - p^2 c^2 = E_0^2, v = p c^2 / E, the velocity addition",
        "D (v = p / (m + p / c), 4.4)",
        "the drive's rational form, first order off Newton",
        "W = E'_0^2 + 3 p . p exact and E' by comparisons (17.6 M3); the pace p / E'; form B's directional accumulator without the cap term (M8)",
        "E'^2 <= W < (E' + 1)^2 at every interval of a pinned run",
    ),
    (
        "E7",
        "the field of a moving charge (Heaviside), the magnetic term",
        "D (12.1, 12b.1)",
        "the age moment is the Lienard-Wiechert potential exactly (12.1); its gradient across the six Ports gives -grad(A) only (17.6 M4)",
        "the magnetic part: source-velocity-v1, named, not designed",
        "none until then; under -grad(A) alone the co-moving pair's pushes are the rest force along and gamma times the rest across",
    ),
    (
        "E8",
        "Poisson's equation, the field of a source",
        "R (5.1)",
        "the age moment, sourced by the release",
        "nothing",
        "series E: k_a r = 36.1, k_s r^2 = 41.5",
    ),
    (
        "E9",
        "the gravitational redshift at first order",
        "R (5.2)",
        "the owed count on the age moment, 1 / (1 + k_a)",
        "nothing",
        "series E's shells",
    ),
    (
        "E10",
        "Newton's geodesics (the retarded inverse square, the orbit)",
        "R (3.3, 5.3)",
        "the push and the drive",
        "nothing",
        "series D's orbit; push_m = m push_1",
    ),
    (
        "E11",
        "the second-order redshift, sqrt(1 - 2 G M / (r c^2))",
        "D (5.2: 1 / (1 + k) at second order, no horizon)",
        "a clock slowed by what it reads, linear in the crowd",
        "the field's self-source: the rows in flight as sources of rows, field-source-v1, not decided",
        "the strong-field probes k = 2 to 9 of series E re-read",
    ),
    (
        "E12",
        "the perihelion advance, 6 pi G M / (c^2 a (1 - e^2))",
        "N (5.6: post-Newtonian terms)",
        "the retarded push gives the drift and the decay of 12b.2, not a precession",
        "one sixth from the velocity terms of covariant-readings-v1, five sixths from the field's nonlinearity, field-source-v1",
        "the thrown orbit's apsidal drift per turn, pi beta_orbit^2 from the readings alone (one sixth of Einstein's)",
    ),
    (
        "E13",
        "the bending of light, 4 G M / (c^2 b)",
        "D (5.4; series K's 0.000; the meeting key about M / b)",
        "the flight blind to the crowd",
        "a rule on the linear block: the row's wall reading the age moment (optical-v1), giving the delay's half; the space half needs the second-order field",
        "series K's beam at b = 6: 2 G M / (c^2 b) under the wall alone, 4 G M / (c^2 b) with the field's second order",
    ),
    (
        "E14",
        "the Shapiro delay",
        "D (5.4)",
        "no delay in time on main",
        "the same optical-v1",
        "the lensing world's round trip lengthened by (2 G M / c^3) ln(4 r_1 r_2 / b^2)",
    ),
    (
        "E15",
        "the equivalence principle for a bound body",
        "D (19.5)",
        "the source's rows from the held content, M_A cancelling for a free body (3.3, exact)",
        "the release reading the body's own E' / (Q S) (17.6 M6), inside covariant-readings-v1; the energy in flight, field-source-v1",
        "a thrown body beside a probe of content 1: the probe's push against the body's drive, 1 at rest and gamma in motion",
    ),
    (
        "E16",
        "the self-gravitation of the field's content",
        "N",
        "the rows carry no source",
        "field-source-v1 (rows in flight releasing, or the wall reading the presence)",
        "E11's and E12's numbers",
    ),
    (
        "E17",
        "the tensor source (the stress as a source)",
        "D (record 196)",
        "the reading R returns the traceless second moment",
        "the push reading the order-2 moment as well, a column of the coupling (tensor-source-v1)",
        "a moving crowd's push on a probe differing from a static crowd's by the stress term",
    ),
    (
        "E18",
        "the cosmological term, q_0 = -0.53",
        "D (15.4: Milne's 0)",
        "the growing wall at a constant H",
        "a rising H, a second declared rate under expansion-v1",
        "the 24 stars' z(tau) with q < 0 against the register's bracket",
    ),
    (
        "E19",
        "the relativistic dispersion of a massive quantum, E^2 = m^2 c^4 + p^2 c^2 as a wave (Klein-Gordon)",
        "N (every row flies at c)",
        "the rows' massless wave equation (4.1, 5.1)",
        "massive-rows-v1 (section 23): the row's wall E' = isqrt(E'_0^2 + 3 p . p)",
        "slits_matter's bands at 36.5, 60, 83.5 and the centre's first click at 1 + 828 (23.3)",
    ),
)


def status_class(status: str) -> str:
    return {"R": "reached", "D": "different", "N": "missing"}[status[0]]


# The small formulas: (name, the formula, what it is, what it derives to,
# where in DERIVATIONS_BEAM.md), the components of the one map.
SMALL_FORMULAS = (
    (
        "The flight",
        "m(tau) = floor((2 tau S<sub>1</sub> Q + T<sub>d</sub>) / (2 T<sub>d</sub>))",
        "a row's Manhattan count at the age tau on its direction d (S<sub>1</sub> the direction's L1 length, "
        "Q the pace's grain, T<sub>d</sub> the direction's wall by isqrt): the accumulator's whole part at a constant rate",
        "the digital line at Q / T<sub>d</sub> -&gt; 1 / sqrt 3 Links per interval, the same on every direction: "
        "c, derived as the largest isotropic pace at which no direction crosses two Links in one interval",
        "1.4, 2.1, 4.1",
    ),
    (
        "The phase",
        "phi(tau) = floor((n / d) tau) mod N",
        "a row's phase on the circle Z<sub>N</sub>, n / d the family's rate",
        "omega = c k along the line, dispersionless: "
        "the massless wave equation at c in the limit, whose symmetry is Lorentz's",
        "4.1, 7.1",
    ),
    (
        "The merge",
        "[p] + [p + N / 2] = 0 in Z[Z<sub>N</sub>]",
        "two rows of one record at one Node add in the group ring; an antiphase pair cancels",
        "the coherent sum within one Node; Young's fringes at L<sub>1</sub> - L<sub>2</sub> = +- j lambda",
        "6.3, 7.1",
    ),
    (
        "The click",
        "w = <b>f</b><sup>T</sup> <b>G f</b>,  <b>G</b> = <b>E</b><sup>T</sup> <b>E</b>;  click k where 2 T u + T &lt;= 2 N C<sub>k</sub>",
        "one bilinear form on the record's phase-count vector <b>f</b>, then one threshold against the rungs of the "
        "cells' cumulative weights, u the wheel written at the birth",
        "Born's rule as the unique reading (the lattice "
        "Gleason), S = 176 / 64 = 2.75 on the pair; the one read-out, the law's one cost",
        "6.1 to 6.7",
    ),
    (
        "The push",
        "<b>p</b><sub>t+1</sub> = <b>p</b><sub>t</sub> + <b>C a</b><sub>t</sub>",
        "a body's momentum changed by the coupling matrix <b>C</b> (its charges per column: gravity, the charge, the "
        "strong column) applied to the arriving label flow <b>a</b>: bilinear in the state",
        "d<b>p</b> / dt = -M grad(A): Newton's and Coulomb's 1 / r<sup>2</sup> in the shell mean, retarded at c; "
        "Gauss's law exact; G = K (n / d) / (4 pi S)",
        "3.1 to 3.4",
    ),
    (
        "The drive",
        "x<sub>t+1</sub> = x<sub>t</sub> + [drive &gt;= Q S M + |p|],  v = p / (Q S M + p)",
        "a body steps one Link when its drive crosses the wall; M its content, S the width",
        "Newton's F = m a with "
        "m = Q S M at p &lt;&lt; Q S M c; the pace saturating at c: p = m v / (1 - v / c), first order off Newton's m v",
        "4.4, 17.2",
    ),
    (
        "The clock",
        "owed = by_clock(age, k n, d):  rate 1 / (1 + k n / d)",
        "a body's own counter, slowed by the crowd k it reads (the presence, or the age moment), never by its speed",
        "the gravitational redshift at first order, 1 / (1 + k<sub>a</sub>); the moving clock's rate 1 (a different law "
        "from Einstein's gamma, registered in G2)",
        "4.3, 5.2",
    ),
    (
        "The field",
        "A(x, t) = the age moment of the arriving rows",
        "what a detector reads of a source's rows, sourced by the release",
        "Poisson's equation and the retarded wave equation; the Lienard-Wiechert potential exactly",
        "5.1, 12.1",
    ),
    (
        "The turn",
        "phi += floor(k<sub>1</sub> |p| N / h) - floor(k<sub>0</sub> |p| N / h)",
        "a body's phase turned by its momentum under action",
        "Bohr's levels, 2 pi p r = j h (r = 8 and 12 closing)",
        "7.2",
    ),
    (
        "The cost",
        "E = h f",
        "the content a lamp pays per phase step at the release, h the family's cost, f the rate",
        "Planck's relation as the release's accounting; E = p c for a row",
        "6.4, 16.1",
    ),
)

# The comparison: (the quantity, Newton, Lorentz, Einstein, the law today
# with its derivation and status).
COMPARISON = (
    (
        "The speed of light",
        "no limit: gravity acts at once",
        "the ether's wave speed c; matter contracts and clocks slow under the ether so that the ether wind is not measured",
        "a postulate: one c for every observer",
        "DERIVED: c = 1 / sqrt 3 Links per interval from the flight's straightness and one pace; the rows' limit is the wave equation at c, the light cone (reached, series K's 89.40 in every world)",
    ),
    (
        "Inertia and F = m a",
        "the first and the second law, p = m v",
        "Newton's, with the electron's mass growing with speed by the ether",
        "p = gamma m v; F = dp / dt",
        "the drive: p an accumulator kept between pushes (inertia 1.0000, G2's stars); F = m a with m = Q S M at low speed (series 7's push_m = m push_1); the law's own p = m v / (1 - v / c) departs at FIRST order where nature's gamma departs at second: a different law, the covariant drive p c^2 / E has the right order (17.2)",
    ),
    (
        "The third law and momentum",
        "action and reaction equal and opposite",
        "as Newton's",
        "the conservation of energy-momentum",
        "the apportioning at the release: the two sources' momenta equal and opposite to the grain (9 612 145 197 056 against -9 612 088 573 952; reached)",
    ),
    (
        "Gravitation",
        "G M / r^2, absolute space and time",
        "not addressed",
        "the geodesics of a curved metric; the field equation with the stress-energy tensor as its source",
        "the push's shell mean: the inverse square retarded at c, the equivalence principle exact (M_A cancels), G = K (n / d) / (4 pi S); Poisson's equation from the age moment (reached: series E's k_s r^2 = 41.5, series D's orbit); the tensor source and the field's self-source not reached (E16, E17)",
    ),
    (
        "Doppler",
        "1 +- v / c, the classical count",
        "1 +- v / c with the ether's correction",
        "gamma (1 +- beta), the transverse gamma",
        "the crossing count per interval: 1 +- v / c exactly, 1 across (reached: record 158's 45, 58, 19, 38); the gamma needs the count charged per self-creation, covariant-readings-v1 (E4)",
    ),
    (
        "A moving clock",
        "absolute time: no slowing",
        "clocks slow by sqrt(1 - beta^2), a mechanism in the ether",
        "the same factor gamma, a property of space and time",
        "a DIFFERENT law as declared: the rate is 1 at every speed; a clock slows only by what it reads, 1 / (1 + k n / d) (registered: G2's coasting star reads z = 0.2636 against the relativistic 0.315); under covariant-readings-v1 the turn per proper time gives the muon at 70.9 and 125.2 (E2)",
    ),
    (
        "The contraction",
        "none",
        "1 / gamma by the ether's push on the bond (1892 to 1904)",
        "1 / gamma, kinematics",
        "0.87 to 0.96 by the drive's dispersion, unstable (12b.2): a different law; under covariant readings reached by Lorentz's own 1904 argument on Heaviside's field, once the magnetic term is carried (source-velocity-v1, named; E3)",
    ),
    (
        "E = m c^2",
        "none: mass and energy separate",
        "the electron's electromagnetic mass",
        "the inertia of energy, the mass defect",
        "not reached as declared (the content and the momentum untied); E = h f for a row reached; under covariant-readings-v1 E'_0 = Q S M is forced by the Newtonian limit and the invariant E'^2 - 3 p . p is kept by the accumulator without a root (E5, E6)",
    ),
    (
        "The field of a moving charge",
        "none",
        "Heaviside's field, the magnetic term from the ether",
        "the same, from the transformation",
        "the age moment is the Lienard-Wiechert potential exactly; its gradient across the six Ports gives -grad(A) only, the magnetic part missing (E7, source-velocity-v1)",
    ),
    (
        "Gravity on clocks and light",
        "none (Soldner's half bending from a corpuscle)",
        "none",
        "the redshift sqrt(1 - 2 G M / (r c^2)), the bending 4 G M / (c^2 b), the Shapiro delay, the perihelion 6 pi G M / (c^2 a (1 - e^2))",
        "the redshift at first order reached (series E); its second order, the bending, the delay and the perihelion not reached on main: the flight is blind to the crowd (series K's 0.000) and the rows carry no source; named as optical-v1 and field-source-v1, not decided (E11 to E14)",
    ),
    (
        "The quantum",
        "none",
        "none",
        "E = h f (1905), the light quantum",
        "E = h f as the release's accounting; the click as the one threshold gives Born's rule uniquely, Young's spacing, Bohr's levels; the uncertainty relation from the six verbs (section 22)",
    ),
)


def small_formula_html(entry: tuple[str, str, str, str, str]) -> str:
    name, formula, what, derives, where = entry
    return (
        f'<section class="small"><h3>{html.escape(name)}</h3><pre class="formula">{formula}</pre>'
        f"<p><b>What it is:</b> {what}.</p><p><b>What it derives to:</b> {derives}.</p>"
        f'<p class="note">DERIVATIONS_BEAM.md {html.escape(where)}</p></section>'
    )


def m(*items: str) -> str:
    """A MathML formula (block): the items are MathML elements."""
    return '<math display="block">' + "".join(items) + "</math>"


def mi(x: str, bold: bool = False) -> str:
    return f'<mi mathvariant="bold">{x}</mi>' if bold else f"<mi>{x}</mi>"


def mn(x: str) -> str:
    return f"<mn>{x}</mn>"


def mo(x: str) -> str:
    return f"<mo>{x}</mo>"


def msub(base: str, sub: str) -> str:
    return f"<msub>{base}{sub}</msub>"


def msup(base: str, sup: str) -> str:
    return f"<msup>{base}{sup}</msup>"


def mfrac(a: str, b: str) -> str:
    return f"<mfrac>{a}{b}</mfrac>"


def msqrt(a: str) -> str:
    return f"<msqrt>{a}</msqrt>"


def mrow(*items: str) -> str:
    return "<mrow>" + "".join(items) + "</mrow>"


E0 = msub(mi("E"), mn("0"))
P = mi("p", bold=True)
C2 = msup(mi("c"), mn("2"))

# The main formula: the exact square of the energy, the invariant of
# covariant-readings-v1 (DERIVATIONS_BEAM 17.6 M3): W = E_0^2 + 3 p . p in
# the law's whole units (c^2 declared as the pair [1, 3]), E kept as the
# largest integer with E^2 <= W by comparisons, E_0 = Q S M.
mspace = '<mspace width="1.5em"/>'
MAIN_FORMULA = m(mi("W"), mo("="), msup(E0, mn("2")), mo("+"), mn("3"), mrow(P, mo("&sdot;"), P))
MAIN_CONDITIONS = m(
    msup(mi("E"), mn("2")),
    mo("&le;"),
    mi("W"),
    mo("&lt;"),
    msup(mrow(mo("("), mi("E"), mo("+"), mn("1"), mo(")")), mn("2")),
) + m(E0, mo("="), mi("Q"), mi("S"), mi("M"))
NATURE_FORMULA = m(
    msup(mi("E"), mn("2")), mo("="), msup(E0, mn("2")), mo("+"), msup(mi("p"), mn("2")), C2
) + m(C2, mo("="), mfrac(mn("1"), mn("3")))

# A mathematical font for the formulas where the reader's device has none
# (a stylesheet from Google Fonts, the one external source the page
# contract allows; the page reads the same without it).
MATH_FONT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Math&display=swap">\n'
)

# Who owns what: the badge classes and their names.
WHO = {
    "law": "the law (yours)",
    "newton": "Newton",
    "lorentz": "Lorentz",
    "einstein": "Einstein",
    "planck": "Planck",
    "doppler": "Doppler",
}


def who(key: str) -> str:
    return f'<span class="who {key}">{WHO[key]}</span>'


# The story: from the formula at the top, step by step, to the formulas of
# the others. Per step: (title, the law's step as MathML, its explanation,
# the formula it converges to as MathML, whose it is, the explanation, the
# status today, where in DERIVATIONS_BEAM.md).
GAMMA = mfrac(mn("1"), msqrt(mrow(mn("1"), mo("&minus;"), mfrac(msup(mi("v"), mn("2")), C2))))
STORY = (
    (
        "The rest energy",
        m(msub(mi("E"), mn("0")), mo("="), mi("Q"), mi("S"), mi("M")),
        "the energy at rest is the width times the content, whole; forced by the Newtonian limit of the "
        "drive (17.3 (iii))",
        m(E0, mo("="), mi("m"), C2),
        "einstein",
        "the inertia of energy, 1905; in the law c^2 = 1 / 3 and m = Q S M, so the two are one line",
        "under covariant-readings-v1 (decided, not built); as declared the content and the momentum are untied",
        "17.3, 17.6 M3",
    ),
    (
        "The invariant",
        m(
            msup(mi("E"), mn("2")),
            mo("&le;"),
            mi("W"),
            mo("&lt;"),
            msup(mrow(mo("("), mi("E"), mo("+"), mn("1"), mo(")")), mn("2")),
        ),
        "E is the largest integer whose square is at most W, kept by comparisons alone, at most three per "
        "interval: no root, no float, the sixth verb; W is bilinear in p and never drifts",
        m(msup(mi("E"), mn("2")), mo("&minus;"), msup(mi("p"), mn("2")), C2, mo("="), msup(E0, mn("2"))),
        "einstein",
        "the energy-momentum relation, 1905 to 1907 (Minkowski's form, 1908); the same relation, but for "
        "continuous quantities and from two postulates",
        "under covariant-readings-v1; the script's 40 000 pushes keep it at every step",
        "17.6 M3",
    ),
    (
        "The pace",
        m(mi("v"), mo("="), mfrac(mi("p"), msup(mi("E"), mo("&prime;")))),
        "Links per interval: the drive's Newtonian rate per self-creation, p / (Q S M), times the "
        "self-creation's cadence E_0 / E; capped at c = 1 / sqrt 3 as p grows",
        m(mi("v"), mo("="), mfrac(mrow(mi("p"), C2), mi("E"))),
        "einstein",
        "the velocity of a body from its energy and momentum, 1905; the velocity addition follows",
        "under covariant-readings-v1; as declared v = p / (m + p / c), first order off Newton",
        "17.6 M1, 4.4",
    ),
    (
        "Proper time",
        m(
            "<mtext>one self-creation per&nbsp;</mtext>",
            mfrac(mi("E"), E0),
            "<mtext>&nbsp;intervals</mtext>",
        ),
        "the body owes by_drive(acc_tau, E - E_0, E_0) intervals after every self-creation: its age, its "
        "turn, its decay and its count all follow that cadence, a counted mechanism",
        m(mi("&gamma;"), mo("="), mfrac(mi("E"), E0), mo("="), GAMMA),
        "lorentz",
        "the Lorentz factor: Lorentz's local time (1895, 1904) as a mechanism, Einstein's time dilation "
        "(1905) as kinematics; the muon of J4 fires at 70.9 and 125.2 intervals against 64 at rest",
        "under covariant-readings-v1; as declared the rate is 1 at every speed (a different law, registered)",
        "17.6 M1, M2; 4.3",
    ),
    (
        "The momentum",
        m(P, mo("="), msup(mi("E"), mo("&prime;")), mi("v", bold=True)),
        "from the pace: the momentum vector is the energy times the velocity",
        m(
            P,
            mo("="),
            mi("&gamma;"),
            mi("m"),
            mi("v", bold=True),
            mspace,
            mo("&rarr;"),
            mspace,
            P,
            mo("="),
            mi("m"),
            mi("v", bold=True),
        ),
        "newton",
        "at low speed Newton's momentum (1687); at every speed Lorentz's and Einstein's gamma m v",
        "under covariant-readings-v1 the right order; as declared p = m v / (1 - v / c), a first-order departure",
        "17.2, 17.6 M1",
    ),
    (
        "Doppler",
        m("<mtext>the crossing count per self-creation</mtext>"),
        "a moving reader meets the rows of a stream at 1 - n . beta per interval and is charged per "
        "self-creation, gamma intervals apart",
        m(
            mn("1"),
            mo("+"),
            mi("z"),
            mo("="),
            mi("&gamma;"),
            mrow(
                mo("("),
                mn("1"),
                mo("&minus;"),
                mi("n", bold=True),
                mo("&sdot;"),
                mi("&beta;", bold=True),
                mo(")"),
            ),
        ),
        "einstein",
        "the relativistic Doppler with the transverse gamma, 1905; at low speed Doppler's 1 +- v / c "
        "(1842), which the law reaches as declared and registered (record 158)",
        "the gamma under covariant-readings-v1 (the pin z = 0.369); the classical count reached today",
        "2.2, 17.6 M2",
    ),
    (
        "Newton's laws",
        m(
            P,
            mo("&larr;"),
            P,
            mo("+"),
            mi("C", bold=True),
            mi("a", bold=True),
            mspace,
            mo(","),
            mspace,
            mi("x"),
            mo("&larr;"),
            mi("x"),
            mo("+"),
            mo("["),
            "<mtext>drive</mtext>",
            mo("&ge;"),
            mi("D"),
            mo("]"),
        ),
        "the push, bilinear in the state (the reader's charges times the arriving flow), and the drive; the "
        "shell mean of the flux is the inverse square, retarded at c",
        m(
            mi("F"),
            mo("="),
            mi("m"),
            mi("a"),
            mspace,
            mo(","),
            mspace,
            mi("F"),
            mo("="),
            mfrac(mrow(mi("G"), mi("M"), mi("m")), msup(mi("r"), mn("2"))),
        ),
        "newton",
        "the three laws and gravitation (1687), with G = K (n / d) / (4 pi S); the equivalence principle "
        "exact because M cancels",
        "reached as declared and registered (inertia 1.0000, push_m = m push_1, series E's inverse square, series D's orbit)",
        "3.1 to 3.4, 17.2",
    ),
    (
        "The speed of light",
        m(
            mi("m"),
            mo("("),
            mi("&tau;"),
            mo(")"),
            mo("="),
            "<mtext>floor</mtext>",
            mo("("),
            mfrac(
                mrow(
                    mn("2"),
                    mi("&tau;"),
                    msub(mi("S"), mn("1")),
                    mi("Q"),
                    mo("+"),
                    msub(mi("T"), mi("d")),
                ),
                mrow(mn("2"), msub(mi("T"), mi("d"))),
            ),
            mo(")"),
        ),
        "the flight table: a row walks its digital line at Q / T_d Links per interval, the same on every "
        "direction, 32 Links in 55 intervals on an axis",
        m(
            mi("c"),
            mo("="),
            mfrac(mn("1"), msqrt(mn("3"))),
            mspace,
            mo(","),
            mspace,
            mi("&omega;"),
            mo("="),
            mi("c"),
            mi("k"),
        ),
        "einstein",
        "one c for every observer is Einstein's second postulate (1905) and the ether's wave speed for "
        "Lorentz; here it is DERIVED: the largest isotropic pace at which no direction crosses two Links in "
        "one interval, and the rows' limit is the wave equation whose symmetry is Lorentz's",
        "reached as declared and registered (record 144's cone, series K's 89.40)",
        "1.4, 2.1, 4.1",
    ),
    (
        "The quantum of energy",
        m(mn("3"), mi("h"), mi("n"), mo("="), mi("Q"), mi("S"), mi("d")),
        "the release pays h content per phase step; the exchange's books balance only under this identity "
        "of the cost, the rate and the width, checked at load",
        m(mi("E"), mo("="), mi("h"), mi("f")),
        "planck",
        "Planck's relation (1900) and Einstein's light quantum (1905): here the release's accounting, and "
        "the mass defect of a bound set is the escaped rows' energy",
        "E = h f reached as declared (6.4); the identity under covariant-readings-v1",
        "6.4, 17.6 M7",
    ),
    (
        "Gravity on a clock",
        m(
            "<mtext>rate</mtext>",
            mspace,
            mfrac(mn("1"), mrow(mn("1"), mo("+"), mi("k"), mi("n"), mo("/"), mi("d"))),
        ),
        "a clock slows by the crowd it reads (the age moment), never by its speed; the age moment obeys "
        "Poisson's equation",
        m(
            mfrac(mrow(mi("&Delta;"), mi("f")), mi("f")),
            mo("="),
            mo("&minus;"),
            mfrac(mrow(mi("G"), mi("M")), mrow(mi("r"), C2)),
        ),
        "einstein",
        "the gravitational redshift at first order (1911) and Newton's potential; the second order, the "
        "bending 4 G M / (c^2 b), the delay and the perihelion (1915) are not reached",
        "the first order reached and registered (series E); the second order needs field-source-v1 and optical-v1",
        "5.1, 5.2, 21.4",
    ),
)


def story_html(entry: tuple[str, str, str, str, str, str, str, str]) -> str:
    title, law_formula, law_text, target, owner, target_text, status, where = entry
    return (
        f'<section class="step"><h3>{html.escape(title)}</h3>'
        f'<div class="pair"><div class="mine">{who("law")}{law_formula}<p>{law_text}.</p></div>'
        f'<div class="arrow">&darr;</div>'
        f'<div class="theirs">{who(owner)}{target}<p>{target_text}.</p></div></div>'
        f'<p class="status"><b>Today:</b> {status}. <span class="note">DERIVATIONS_BEAM.md {html.escape(where)}</span></p>'
        "</section>"
    )


@register("universe24")
def page_einstein(out: Path, runs: Path | None) -> Path:
    """(12) Universe24, the formula: the owner's formula at the top, whose
    each formula is, and the story of the derivations from it to Newton's,
    Lorentz's and Einstein's; no run, no claim added."""
    del runs
    steps = "".join(story_html(entry) for entry in STORY)
    smalls = "".join(small_formula_html(entry) for entry in SMALL_FORMULAS)
    comparison = "".join(
        f"<tr><th>{html.escape(q)}</th><td>{html.escape(n)}</td><td>{html.escape(lo)}</td>"
        f'<td>{html.escape(e)}</td><td class="ours">{html.escape(us)}</td></tr>'
        for q, n, lo, e, us in COMPARISON
    )
    einstein_rows = "".join(
        f'<tr><td class="num">{n}</td><td>{html.escape(result)}</td>'
        f'<td class="{status_class(status)}">{html.escape(status)}</td><td>{html.escape(gives)}</td>'
        f"<td>{html.escape(add)}</td><td>{html.escape(pin)}</td></tr>"
        for n, result, status, gives, add, pin in EINSTEIN_MAP
    )
    body = f"""
<section class="big">
<p class="kind">{who("law")} the exact square of a body's energy, in whole numbers</p>
{MAIN_FORMULA}
<div class="conditions">{MAIN_CONDITIONS}</div>
<p class="kind">W the state carried, bilinear in the momentum vector p; E the largest integer whose square is at most W, kept by comparisons; E<sub>0</sub> the rest value, the width Q S times the content M; c<sup>2</sup> = 1 / 3 derived from the flight</p>
</section>
<section class="big theirs-box">
<p class="kind">{who("einstein")} the same relation in nature's units, 1905 to 1907</p>
{NATURE_FORMULA}
</section>
<h2>What is yours and what is theirs</h2>
<p>The formula at the top is the law's: its numbers are whole, E is kept by comparisons and never by a root,
E<sub>0</sub> = Q S M ties the rest energy to the content, and c<sup>2</sup> = 1 / 3 is derived from the
flight table, not declared. Written in nature's units it reads E<sup>2</sup> = E<sub>0</sub><sup>2</sup> +
p<sup>2</sup> c<sup>2</sup>, which is Einstein's relation of 1905 to 1907: the relation is his, the integer
form and the mechanism that reaches it are the law's. Everything below is derived from the top: each step
shows the law's line on the left and, on the right, whose formula it becomes and when it was found.</p>
<div class="owners">
<section><h3>{who("law")}</h3><ul>
<li>W = E<sub>0</sub><sup>2</sup> + 3 p . p, E by comparisons, E<sub>0</sub> = Q S M</li>
<li>c = 1 / sqrt 3 derived from the flight table (32 Links in 55 intervals)</li>
<li>proper time as an owed count: one self-creation per E / E<sub>0</sub> intervals</li>
<li>the crossing count (Doppler as a count of rows met)</li>
<li>the push p &lt;- p + <b>C a</b> and the drive: one coupling over the columns, bilinear, local</li>
<li>the click as the one threshold; the identity 3 h n = Q S d</li>
</ul><p class="note">the six verbs on integers, one map at every Node (HIGHLIGHTS 5.7)</p></section>
<section><h3>{who("newton")}</h3><ul>
<li>the three laws: inertia, F = m a, action and reaction (1687)</li>
<li>gravitation G M m / r<sup>2</sup>, absolute space and time</li>
<li>p = m v, the Galilean composition</li>
</ul><p class="note">the law's low-speed regime, every row registered</p></section>
<section><h3>{who("lorentz")}</h3><ul>
<li>the transformations and the local time (1895, 1904)</li>
<li>the contraction 1 / gamma and the slowing sqrt(1 - beta<sup>2</sup>) as a mechanism in the ether</li>
<li>the electron's mass growing with speed</li>
</ul><p class="note">the law stands nearer to Lorentz: a mechanism, not a postulate (record 231)</p></section>
<section><h3>{who("einstein")}</h3><ul>
<li>the two postulates and the kinematics: gamma, the Doppler with gamma (1905)</li>
<li>E<sub>0</sub> = m c<sup>2</sup> (1905), E<sup>2</sup> = E<sub>0</sub><sup>2</sup> + p<sup>2</sup> c<sup>2</sup> (1907), v = p c<sup>2</sup> / E</li>
<li>the light quantum E = h f (1905, after Planck 1900)</li>
<li>the general theory: the redshift, the bending, the delay, the perihelion (1911 to 1915)</li>
</ul><p class="note">the special theory one hypothesis away; the general theory's first order reached</p></section>
</div>
<h2>The story: from the top, step by step, to theirs</h2>
<div class="story">{steps}</div>
<p><b>Where it stands</b>: the top formula and the steps marked "under covariant-readings-v1" are the four
covariant readings of a body named in DERIVATIONS_BEAM section 17, reviewed (record 297) and decided by the
owner (record 270) to be built beside the law; not built today, and the law as declared keeps the drive
v = p / (m + p / c) and a clock's rate 1 at every speed. The steps marked "reached as declared" are the
law on main, registered. Nothing is added here.</p>
<h2>The comparison in one table</h2>
<div class="scroll"><table class="map compare"><tr><th>The quantity</th><th>Newton</th><th>Lorentz</th><th>Einstein</th><th>The law (its status today)</th></tr>{
        comparison
    }</table></div>
<details><summary>The one map of six verbs and its small formulas (the law as declared)</summary>
<section class="big">
<p class="kind">The one map F at every Node, every interval</p>
<pre class="formula">
s &lt;- s + r
e &lt;- [s &gt;= d]
s &lt;- s - e d
</pre>
<p class="kind">the state s an integer vector on the torus, r its rates, d its walls; every wall crossing an event</p>
<pre class="formula small-caps">click k where  2 T u + T &lt;= 2 N C<sub>k</sub>,   C<sub>k</sub> = <b>f</b><sup>T</sup> <b>G f</b></pre>
</section>
<div class="smalls">{smalls}</div>
</details>
<details><summary>The full Einstein map, E1 to E19 (DERIVATIONS_BEAM 21.4): {
        sum(1 for r in EINSTEIN_MAP if r[2].startswith("R"))
    } reached as declared, {sum(1 for r in EINSTEIN_MAP if r[2].startswith("D"))} a different law, {
        sum(1 for r in EINSTEIN_MAP if r[2].startswith("N"))
    } not reached</summary>
<div class="scroll"><table class="map"><tr><th>#</th><th>Einstein's result</th><th>status</th><th>what the six verbs give</th><th>what must be added, under which identity</th><th>the pin a run would meet</th></tr>{
        einstein_rows
    }</table></div>
</details>
{
        sources(
            [
                (
                    "the main formula W = E_0^2 + 3 p . p, E by comparisons, the pace p / E, the proper-time cadence, the identity 3 h n = Q S d, the muon's 70.9 and 125.2, the star's z = 0.369",
                    '<a href="../../DERIVATIONS_BEAM.md">DERIVATIONS_BEAM.md</a> section 17.6 (M1 to M9, record 297)',
                ),
                (
                    "the theorem of covariant readings, built on Newton, tried on Lorentz",
                    '<a href="../../DERIVATIONS_BEAM.md">DERIVATIONS_BEAM.md</a> sections 17.1 to 17.5; the owner\'s decision, record 270',
                ),
                (
                    "c, Doppler, Newton and Coulomb, the symmetry of the limit, the delay field, the click, Young and Bohr",
                    '<a href="../../DERIVATIONS_BEAM.md">DERIVATIONS_BEAM.md</a> sections 0 and 2 to 7',
                ),
                (
                    "the statement, the six verbs, what is derived and what is input",
                    '<a href="../../HIGHLIGHTS.md">HIGHLIGHTS 5.7</a>',
                ),
                (
                    "Newton, Lorentz and Einstein in the owner's question",
                    '<a href="../../LOG_2026-09-20.md">record 231</a> of the log of 2026-09-20',
                ),
                (
                    "the Einstein map, E1 to E19",
                    '<a href="../../DERIVATIONS_BEAM.md">DERIVATIONS_BEAM.md</a> section 21.4 (record 291)',
                ),
                (
                    "the dates of the others' formulas",
                    "the standard history: Newton 1687; Doppler 1842; Lorentz 1892 to 1904; Planck 1900; Einstein 1905, 1907, 1911, 1915; Minkowski 1908",
                ),
            ]
        )
    }
"""
    return write_page(
        out,
        "universe24",
        page(
            "Universe24",
            "Your formula at the top; whose each formula is; and the story of the derivations from it to "
            "Newton's, Lorentz's and Einstein's, step by step.",
            body,
            head=MATH_FONT,
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
            "a plate of pixels on the far side of a narrow beam clicking as records arrive, one click per "
            "record by the ladder and the wheel value u, the click list growing (a demonstration world; the "
            "catalog's optical bench cited beside it)",
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
            "atom.html",
            "The atom",
            "series H: the electron circling the proton with its momentum arrow and its copies spreading, "
            "its phase turning by its momentum; the faces reading what comes out (a registered world)",
        ),
        (
            "volume.html",
            "In three dimensions",
            "the nucleus, the decay, the atom and the beam beside the mass, the whole GameBoard drawn in an "
            "isometric projection, the bodies releasing themselves into the Nodes beside them (registered worlds)",
        ),
        (
            "quarks.html",
            "The quarks",
            "series R: the proton of three quarks holding in a line, a kicked quark walking off, and a fast "
            "electron thrown at the proton, handing its momentum through the table (two registered worlds and "
            "a demonstration world)",
        ),
        (
            "universe24.html",
            "Universe24",
            "the owner's formula at the top (the exact square of a body's energy, W = E_0^2 + 3 p . p), whose "
            "each formula is, and the story of the derivations from it to Newton's, Lorentz's and Einstein's; "
            "the comparison table, the one map and the Einstein map beneath (no run)",
        ),
        (
            "formula.html",
            "The octahedron and the 48",
            "one Node's six Ports as an octahedron with the sphere of c inside it, turning; the 48 signed "
            "axis permutations one per frame, 24 rotations and 24 improper ones, the hand's bit kept or "
            "flipped; the general formula in the words of HIGHLIGHTS 5.7 (no run)",
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
<p>Two pages of the same request, made beside the amplitude series and on main (the register's E15 and
E16): <a href="../../../examples/events/amplitude/pages/click.html">the click of one record</a> (one record
spreading, its ladder growing, the click, the deletion of its offers) and
<a href="../../../examples/events/amplitude/pages/bell.html">the pair's two clicks</a> (Bell on the board,
S = 176 / 64 = 2.75 against the bounds 2 and 2.83).</p>
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
    parser.add_argument(
        "--figures",
        type=Path,
        default=None,
        help="write the still pictures of the formula page (the octahedron, the 48) here and stop",
    )
    args = parser.parse_args(argv)
    if args.figures is not None:
        for path in formula_figures(args.figures):
            print(f"{path} ({path.stat().st_size / 1e6:.2f} MB)")
        return
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
