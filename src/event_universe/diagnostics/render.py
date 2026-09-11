"""The existing make_v7_run_html.py rendering pipeline, extracted and generalized.

Still uses imshow + FuncAnimation + PillowWriter and a GIF embedded in standalone
HTML. Rendering is diagnostic only; no rendered value is fed into the engine.
"""

import base64
import html
import json
from collections.abc import Callable, Mapping, Sequence
from itertools import pairwise
from math import hypot
from pathlib import Path
from typing import cast

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.artist import Artist
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageSequence

from .frames import AXES, Frame, Slice, VolumeFrame

VOLUME_AXIS_COLORS = ("#ff8c91", "#81e6af", "#80bdff")
FULL_SPEED_ARROW_LENGTH = 10.8
FACE_LABELS = ("+X", "-X", "+Y", "-Y", "+Z", "-Z")


def _face_metadata(
    frames: Sequence[Frame] | Sequence[VolumeFrame], metadata: Mapping[str, object] | None
) -> Mapping[str, object] | None:
    """Keep exact signed face values separate from the cloud's aggregate quantity."""
    if not any(frame.faces_available for frame in frames):
        return metadata
    return {
        **dict(metadata or {}),
        "delivered_faces": {
            "order": FACE_LABELS,
            "meaning": "Local neighbor-facing surfaces from which input arrived; not velocity or phi",
            "inventory_meaning": (
                "Separate per-field, per-channel local state inventory, including retained remainders. "
                "Excludes in-flight packets. Face arrivals are not added to this inventory."
            ),
            "frames": [
                {
                    "tick": frame.tick,
                    "available": frame.faces_available,
                    "primary_field_name": frame.primary_field_name,
                    "fields": {
                        name: [
                            {"position": p, "values": values} for p, values in sorted(records.items())
                        ]
                        for name, records in frame.field_faces_by_name.items()
                    },
                    "local_inventory": {
                        name: [
                            {"position": p, "channels": values} for p, values in sorted(records.items())
                        ]
                        for name, records in frame.field_inventory_by_name.items()
                    },
                    "cells": [
                        {"position": position, "values": values}
                        for position, values in sorted(frame.field_faces.items())
                    ],
                }
                for frame in frames
            ],
        },
    }


def _speed_arrow(
    momentum: tuple[int, int, int], c_units: int | None, mass: int = 1, momentum_den: int = 1
) -> tuple[float, float, float]:
    """Display the model's capped hop-budget rate, with Euclidean arrow length proportional to it."""
    if c_units is None:
        return (0.0, 0.0, 0.0)
    if type(c_units) is not int or c_units <= 0:
        raise ValueError("display speed scale must be a positive integer")
    magnitude = hypot(*momentum)
    if magnitude == 0:
        return (0.0, 0.0, 0.0)
    if mass < 1 or momentum_den < 1:
        raise ValueError("positive mass and momentum denominator required")
    cap = c_units * mass * momentum_den
    fraction = min(sum(abs(value) for value in momentum), cap) / cap
    scale = FULL_SPEED_ARROW_LENGTH * fraction / magnitude
    return momentum[0] * scale, momentum[1] * scale, momentum[2] * scale


def _display_jump(
    previous: tuple[int, int, int],
    current: tuple[int, int, int],
    shape: tuple[int, int, int] | None = None,
) -> bool:
    """Flag two or more grid steps, using shortest periodic differences when known."""
    distances = [abs(after - before) for before, after in zip(previous, current, strict=True)]
    if shape is not None:
        distances = [
            min(distance, size - distance) for distance, size in zip(distances, shape, strict=True)
        ]
    return sum(distances) >= 2


def _periodic_crossing(
    previous: tuple[int, int, int],
    current: tuple[int, int, int],
    shape: tuple[int, int, int] | None,
) -> bool:
    """Recognize a boundary crossing by the shorter periodic coordinate displacement."""
    return shape is not None and any(
        abs(after - before) > size / 2
        for before, after, size in zip(previous, current, shape, strict=True)
    )


def _draw_orientation(ax: Axes3D, *, elevation: float, azimuth: float) -> None:
    """Show positive world-axis directions with the same camera as the main view."""
    ax.clear()
    ax.set_axis_off()
    ax.set_xlim(-0.25, 1.45)
    ax.set_ylim(-0.25, 1.45)
    ax.set_zlim(-0.25, 1.45)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elevation, azim=azimuth)
    for index, (label, color) in enumerate(zip("XYZ", VOLUME_AXIS_COLORS, strict=True)):
        direction = [int(axis == index) for axis in range(3)]
        ax.quiver(0, 0, 0, *direction, color=color, linewidth=2.5, arrow_length_ratio=0.22)
        ax.text(
            *(1.25 * component for component in direction),
            f"+{label}",
            color=color,
            fontsize=12,
            weight="bold",
            ha="center",
            va="center",
        )


def _bounds(frames: Sequence[Frame]) -> tuple[int, int, int, int]:
    points = [(p[1], p[2]) for frame in frames for p in frame.particles]
    if not points:
        points = [point for frame in frames for point in frame.field]
    if not points:
        return 0, 8, 0, 8
    xs, ys = zip(*points, strict=True)
    return min(xs) - 5, max(xs) + 5, min(ys) - 5, max(ys) + 5


def render_run(
    frames: Sequence[Frame],
    view: Slice,
    html_path: Path,
    *,
    title: str,
    metadata: Mapping[str, object] | None = None,
    compact: bool = False,
) -> Path:
    """Render sampled frames with fixed color scale and a true, explicitly named plane."""
    if not frames:
        raise ValueError("at least one diagnostic frame is required")
    xmin, xmax, ymin, ymax = _bounds(frames)
    h_axis, v_axis, fixed_axis = AXES[view.plane]
    labels = ("x", "y", "z")
    plane_label = f"{view.plane} slice {labels[fixed_axis]}={view.coordinate}"
    if any(frame.field_kind != frames[0].field_kind for frame in frames):
        raise ValueError("one animation must use one field quantity")
    if frames[0].field_kind == "stream-magnitude":
        plane_label += " | Stream magnitude = sum populations (not scalar phi)"
    if frames[0].field_kind == "face-magnitude":
        plane_label += f" | {frames[0].primary_field_name}: last delivered face flux: sum magnitudes (not inventory)"
    vmax = max(1, max((v for frame in frames for v in frame.field.values()), default=1))
    fig, ax = plt.subplots(figsize=(4, 2.8) if compact else (9, 5.5))

    def draw(index: int) -> tuple[Artist, ...]:
        ax.clear()
        frame = frames[index]
        grid = [[0] * (xmax - xmin + 1) for _ in range(ymax - ymin + 1)]
        for (x, y), value in frame.field.items():
            if xmin <= x <= xmax and ymin <= y <= ymax:
                grid[y - ymin][x - xmin] = value
        ax.imshow(
            grid,
            origin="lower",
            extent=(xmin - 0.5, xmax + 0.5, ymin - 0.5, ymax + 0.5),
            interpolation="nearest",
            aspect="equal",
            vmin=0,
            vmax=vmax,
            cmap="magma",
        )
        for pid, x, y, px, py, _ in frame.particles:
            color = ("#4cc9ff", "#74ffac", "#ffd166", "#fa8cff")[pid % 4]
            ax.scatter([x], [y], s=45 if compact else 90, color=color, edgecolors="white")
            magnitude = max(1, abs(px) + abs(py))
            ax.arrow(
                x,
                y,
                1.8 * px / magnitude,
                1.8 * py / magnitude,
                width=0.06,
                color=color,
                length_includes_head=True,
            )
            if not compact:
                ax.text(x + 0.4, y + 0.3, str(pid), color="white")
        ax.set_xlim(xmin - 0.5, xmax + 0.5)
        ax.set_ylim(ymin - 0.5, ymax + 0.5)
        ax.set_title(
            f"3D | {plane_label} | tick={frame.tick}\nPtotal={frame.total_momentum}",
            fontsize=8 if compact else 11,
        )
        ax.set_xlabel(labels[h_axis])
        ax.set_ylabel(labels[v_axis])
        ax.grid(True, alpha=0.15)
        return tuple(ax.get_children())

    return _save_animation_html(
        fig,
        draw,
        len(frames),
        (frames[0].tick, frames[-1].tick),
        plane_label,
        html_path,
        title=title,
        metadata=_face_metadata(frames, metadata),
        compact=compact,
    )


def render_volume(
    frames: Sequence[VolumeFrame],
    html_path: Path,
    *,
    title: str,
    metadata: Mapping[str, object] | None = None,
) -> Path:
    """Render all nonzero field cells, particle trails and momenta in a rotating XYZ view."""
    if not frames:
        raise ValueError("at least one diagnostic frame is required")
    if any(frame.field_kind != frames[0].field_kind for frame in frames):
        raise ValueError("one animation must use one field quantity")
    streaming = frames[0].field_kind == "stream-magnitude"
    face_magnitude = frames[0].field_kind == "face-magnitude"
    primary_name = frames[0].primary_field_name
    show_faces = any(frame.faces_available for frame in frames)
    selected_pid = min((p[0] for frame in frames for p in frame.particles), default=None)
    points = [position for frame in frames for position in frame.field]
    points.extend((p[1], p[2], p[3]) for frame in frames for p in frame.particles)
    if not points:
        points = [(0, 0, 0), (8, 8, 8)]
    bounds: list[tuple[float, float]] = [
        (min(p[axis] for p in points) - 2, max(p[axis] for p in points) + 2) for axis in range(3)
    ]
    # Leave room for tick labels in flat/narrow runs while retaining equal XYZ unit scales.
    minimum_span = max(hi - lo for lo, hi in bounds) * 0.4
    bounds = [
        (lo - max(0, minimum_span - (hi - lo)) / 2, hi + max(0, minimum_span - (hi - lo)) / 2)
        for lo, hi in bounds
    ]
    vmax = max(1, max((value for frame in frames for value in frame.field.values()), default=1))
    fig = plt.figure(figsize=(10, 8.5), facecolor="#080f1c")
    ax = cast(Axes3D, fig.add_axes((0.03, 0.17, 0.88, 0.71), projection="3d", facecolor="#080f1c"))
    compass = cast(
        Axes3D, fig.add_axes((0.025, 0.015, 0.19, 0.19), projection="3d", facecolor="#080f1c")
    )
    colors = ("#4cc9ff", "#74ffac", "#ffd166", "#fa8cff")
    fig.text(0.07, 0.94, "PARTICLE FIELD", color="#edf5ff", fontsize=20, weight="bold")
    fig.text(
        0.07,
        0.905,
        f"{primary_name}: last delivered face flux: sum magnitudes (not inventory)"
        if face_magnitude
        else "Full 3D XYZ / Stream magnitude = sum populations (not scalar phi)"
        if streaming
        else "Full 3D XYZ view  /  particles, field and trajectories  /  lattice coordinates",
        color="#91a4be",
        fontsize=10,
    )
    fig.text(
        0.93,
        0.975,
        "TOTAL SYSTEM MOMENTUM",
        ha="right",
        va="top",
        color="#edf5ff",
        fontsize=12,
        weight="bold",
    )
    status = fig.text(0.93, 0.94, "", ha="right", va="top", color="#c2d5ed", fontsize=11)
    face_heading = None
    face_values = []
    if show_faces:
        ax.set_position((0.03, 0.17, 0.88, 0.64))
        face_heading = fig.text(0.07, 0.865, "", color="#c2d5ed", fontsize=10)
        for index in range(6):
            face_values.append(
                fig.text(
                    0.07 + index * 0.145,
                    0.837,
                    "",
                    color=VOLUME_AXIS_COLORS[index // 2],
                    fontsize=11,
                    weight="bold",
                )
            )
    for order, pid in enumerate(sorted({p[0] for frame in frames for p in frame.particles})):
        fig.text(
            0.28 + order * 0.16,
            0.095,
            f"●  Particle {pid}",
            color=colors[pid % len(colors)],
            fontsize=10,
        )
    fig.text(
        0.93,
        0.055,
        "Face arrivals: faint → strong"
        if face_magnitude
        else "Streams: faint → strong"
        if streaming
        else "Field: faint → strong",
        color="#dcb485",
        ha="right",
        fontsize=10,
    )
    fig.text(0.28, 0.055, "Arrow length: speed / c", color="#c2d5ed", fontsize=10)
    fig.text(0.28, 0.025, "↻ Periodic boundary", color="#65e8ff", fontsize=10)
    fig.text(0.60, 0.025, "X Jump of 2+ cells", color="#ff5252", fontsize=10)
    fig.text(0.12, 0.18, "AXIS DIRECTIONS", color="#c2d5ed", ha="center", fontsize=8)
    # Overlay particle identity and velocity above the translucent field.
    ax.computed_zorder = False

    def draw(index: int) -> tuple[Artist, ...]:
        ax.clear()
        frame = frames[index]
        if face_heading is not None:
            selected = next((p for p in frame.particles if p[0] == selected_pid), None)
            if not frame.faces_available or selected is None:
                face_heading.set_text("Local delivered faces: no selected occupied cell")
                for text in face_values:
                    text.set_text("")
            else:
                position = (selected[1], selected[2], selected[3])
                delivered_values = frame.field_faces.get(position, (0, 0, 0, 0, 0, 0))
                face_heading.set_text(
                    f"Local delivered faces / particle {selected_pid} at {position} / not velocity or phi"
                    + (f" / {frame.primary_field_name}" if frame.primary_field_name else "")
                )
                for text, label, value in zip(face_values, FACE_LABELS, delivered_values, strict=True):
                    text.set_text(f"{label}: {value}")
        previous_positions = (
            {p[0]: (p[1], p[2], p[3]) for p in frames[index - 1].particles} if index else {}
        )
        if frame.field:
            xs, ys, zs = zip(*frame.field, strict=True)
            values = list(frame.field.values())
            # Display-only gamma lift keeps weak field cells visible on the dark background.
            strengths = [(value / vmax) ** 0.5 for value in values]
            # One shared scalar field: do not invent a per-particle source attribution.
            for spread, base_alpha, gain in (
                (45, 0.025, 0.05),
                (20, 0.04, 0.08),
                (8, 0.06, 0.12),
                (2, 0.12, 0.30),
            ):
                ax.scatter(
                    xs,
                    ys,
                    zs,
                    c=[(1.0, 0.35 + 0.5 * u, 0.12 + 0.35 * u, base_alpha + gain * u) for u in strengths],
                    s=[(18 + 70 * u) * spread for u in strengths],
                    marker="o",
                    edgecolors="none",
                    depthshade=False,
                    zorder=3,
                )
        for pid, x, y, z, px, py, pz in frame.particles:
            color = colors[pid % len(colors)]
            trail = [p[1:4] for past in frames[: index + 1] for p in past.particles if p[0] == pid]
            # Break visual discontinuities instead of drawing a fictitious line across the box.
            path: list[tuple[float, float, float]] = []
            for step, point in enumerate(trail):
                if step and (
                    _display_jump(trail[step - 1], point)
                    or _periodic_crossing(trail[step - 1], point, frame.shape)
                ):
                    path.append((float("nan"),) * 3)
                path.append(point)
            tx, ty, tz = zip(*path, strict=True)
            ax.plot(tx, ty, tz, color=color, linewidth=7, alpha=0.07)
            ax.plot(tx, ty, tz, color=color, linewidth=1.8, alpha=0.9)
            ax.scatter(
                [x], [y], [z], color=color, s=750, alpha=0.04, edgecolors="none", depthshade=False
            )
            ax.scatter(
                [x], [y], [z], color=color, s=320, alpha=0.10, edgecolors="none", depthshade=False
            )
            ax.scatter(
                [x],
                [y],
                [z],
                color=color,
                s=150,
                alpha=1,
                edgecolors="#ffffff",
                linewidths=1.4,
                depthshade=False,
                zorder=20,
            )
            arrow_x, arrow_y, arrow_z = _speed_arrow(
                (px, py, pz), frame.c_units, *frame.particle_scales.get(pid, (1, 1))
            )
            velocity_arrow = ax.quiver(
                x,
                y,
                z,
                arrow_x,
                arrow_y,
                arrow_z,
                color=color,
                linewidth=3.2,
                arrow_length_ratio=0.35,
                zorder=19,
            )
            velocity_arrow.set_path_effects(
                [
                    path_effects.Stroke(linewidth=5.5, foreground="#080f1c"),
                    path_effects.Normal(),
                ]
            )
            ax.text(
                x,
                y,
                z + 1.4,
                f"{pid}  m={frame.particle_scales.get(pid, (1, 1))[0]}",
                color=color,
                fontsize=13,
                weight="bold",
                zorder=21,
                bbox={"facecolor": "#080f1c", "edgecolor": "none", "alpha": 0.85, "pad": 1},
            )
            previous = previous_positions.get(pid)
            if previous is not None and _periodic_crossing(previous, (x, y, z), frame.shape):
                ax.text(
                    x,
                    y,
                    z + 3.2,
                    "↻",
                    color="#65e8ff",
                    fontsize=30,
                    ha="center",
                    va="center",
                    weight="bold",
                    zorder=100,
                )
            if previous is not None and _display_jump(previous, (x, y, z), frame.shape):
                ax.scatter(
                    [x],
                    [y],
                    [z],
                    marker="x",
                    s=350,
                    color="#ff3030",
                    linewidths=3.5,
                    depthshade=False,
                    zorder=100,
                )
        ax.set_xlim(*bounds[0])
        ax.set_ylim(*bounds[1])
        ax.set_zlim(*bounds[2])
        ax.set_box_aspect(tuple(hi - lo for lo, hi in bounds))
        azimuth = -65 + 35 * index / max(1, len(frames) - 1)
        ax.view_init(elev=26, azim=azimuth)
        _draw_orientation(compass, elevation=26, azimuth=azimuth)
        ax.grid(False)
        for axis, label, color in zip(
            (ax.xaxis, ax.yaxis, ax.zaxis), "XYZ", VOLUME_AXIS_COLORS, strict=True
        ):
            axis.set_pane_color((0.055, 0.085, 0.14, 0.40))
            axis.pane.set_edgecolor("#435a75")
            axis.line.set_color(color)
            axis.line.set_linewidth(2.2)
            axis.set_major_locator(MaxNLocator(4, integer=True))
            axis.set_rotate_label(False)
            axis.set_label_text(label, color=color, fontsize=17, weight="bold")
            axis.labelpad = 12
            axis.set_tick_params(colors=color, labelsize=11, pad=3)
        # Double the visible grid density without changing physical cells or tick labels.
        grid_ticks = []
        for ticks, (lo, hi) in zip(
            (ax.get_xticks(), ax.get_yticks(), ax.get_zticks()), bounds, strict=True
        ):
            dense_ticks = sorted([*ticks, *((a + b) / 2 for a, b in pairwise(ticks))])
            grid_ticks.append([value for value in dense_ticks if lo <= value <= hi])
        for grid_x in grid_ticks[0]:
            ax.plot([grid_x, grid_x], bounds[1], [bounds[2][0]] * 2, color="#38516d", linewidth=0.7)
            ax.plot([grid_x, grid_x], [bounds[1][1]] * 2, bounds[2], color="#283c53", linewidth=0.55)
        for grid_y in grid_ticks[1]:
            ax.plot(bounds[0], [grid_y, grid_y], [bounds[2][0]] * 2, color="#38516d", linewidth=0.7)
            ax.plot([bounds[0][0]] * 2, [grid_y, grid_y], bounds[2], color="#283c53", linewidth=0.55)
        for grid_z in grid_ticks[2]:
            ax.plot(bounds[0], [bounds[1][1]] * 2, [grid_z, grid_z], color="#283c53", linewidth=0.55)
            ax.plot([bounds[0][0]] * 2, bounds[1], [grid_z, grid_z], color="#283c53", linewidth=0.55)
        status.set_text(
            f"(Px, Py, Pz) = {frame.total_momentum}\nTICK  {frame.tick:03d} / {frames[-1].tick:03d}"
        )
        return (*ax.get_children(), *compass.get_children())

    return _save_animation_html(
        fig,
        draw,
        len(frames),
        (frames[0].tick, frames[-1].tick),
        "Full 3D XYZ view",
        html_path,
        title=title,
        metadata=_face_metadata(frames, metadata),
        note=(
            f"Transparent amber markers show {primary_name}: the sum of absolute values of its "
            "six decoded last-delivered face fluxes, not scalar phi or conserved inventory. "
            "Retained remainders can remain while face brightness is zero; brightness is not decay. "
            "Other fields are not added to this magnitude. "
            "Exact signed faces for every named field are recorded below. Stronger values have "
            if face_magnitude
            else "Transparent amber markers show stream magnitude: the sum of eight populations, "
            "not scalar phi. Stronger values have "
            if streaming
            else "Transparent amber markers show the combined scalar field. Stronger values have "
        )
        + "brighter color and greater opacity, using one fixed scale throughout the animation. "
        "Broad soft halos enlarge field markers for visibility, not the physical field range. "
        "A square-root display transfer lifts weak values; colors are not a linear field scale. "
        "The display grid has twice as many subdivisions per axis; physical cells are unchanged. "
        "Particle markers and glow are display symbols, not physical particle sizes. "
        "Lines show sampled paths. X is coral, Y is green and Z is blue. "
        "The corner arrows show positive axis directions, not a position or distance scale. "
        "System momentum is the combined momentum of particles and field. "
        "Arrow length is proportional to the capped movement-budget speed: c = 10.8 display cells. "
        "Frames without a recorded speed scale omit velocity arrows. "
        "A cyan ↻ marks a periodic boundary crossing (the shorter displacement uses the boundary). "
        "A red X marks a shortest displacement of at least two cardinal grid steps, "
        "including multi-cell jumps across a periodic boundary. Both markers may appear. "
        "Trails break at both markers. Use consecutive ticks to avoid sampled-frame ambiguity; "
        "a marker alone does not indicate motion faster than c. "
        "The camera rotates; coordinates and physics do not.",
        dpi=150,
    )


def _save_animation_html(
    fig: Figure,
    draw: Callable[[int], tuple[Artist, ...]],
    frame_count: int,
    ticks: tuple[int, int],
    plane_label: str,
    html_path: Path,
    *,
    title: str,
    metadata: Mapping[str, object] | None = None,
    compact: bool = False,
    note: str = "",
    dpi: int = 100,
) -> Path:
    """One shared GIF/HTML output pipeline for plane and volume renderers."""
    html_path.parent.mkdir(parents=True, exist_ok=True)
    gif_path = html_path.with_suffix(".gif")
    try:
        animation = FuncAnimation(fig, draw, frames=frame_count, interval=120)
        animation.save(str(gif_path), writer=PillowWriter(fps=8), dpi=65 if compact else dpi)
    finally:
        plt.close(fig)
    # PillowWriter exports an infinite loop. Remove that playback instruction
    # through Pillow's public API so the final tick never looks like a teleport.
    with Image.open(gif_path) as animation_file:
        images = [frame.copy() for frame in ImageSequence.Iterator(animation_file)]
    durations = [frame.info.get("duration", 120) for frame in images]
    for frame in images:
        frame.info.pop("loop", None)
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=durations)
    encoded = base64.b64encode(gif_path.read_bytes()).decode("ascii")
    details = html.escape(json.dumps(dict(metadata or {}), indent=2, ensure_ascii=False, default=str))
    text = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>
body{{margin:0;background:#111827;color:#e5e7eb;font-family:system-ui}}
main{{max-width:1050px;margin:auto;padding:24px}}img{{max-width:100%;border-radius:12px}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#1f2937;padding:16px}}
</style></head><body><main><h1>{html.escape(title)}</h1>
<p>Full 3D physics · {plane_label} · ticks {ticks[0]}–{ticks[1]}</p>
<p>Frames may be sampled. Arrows show direction; their length is scaled for visibility.</p>
<p>Playback stops at the final frame. Reload the page to replay from the beginning.</p>
<p>{html.escape(note)}</p>
<img alt="Simulation: {plane_label}" src="data:image/gif;base64,{encoded}">
<details><summary>Run parameters and checks</summary><pre>{details}</pre></details>
</main></body></html>"""
    html_path.write_text(text, encoding="utf-8")
    return html_path
