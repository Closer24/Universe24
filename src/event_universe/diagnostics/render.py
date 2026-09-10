"""The existing make_v7_run_html.py rendering pipeline, extracted and generalized.

Still uses imshow + FuncAnimation + PillowWriter and a GIF embedded in standalone
HTML. Rendering is diagnostic only; no rendered value is fed into the engine.
"""

import base64
import html
import json
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import cast

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.artist import Artist
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d import Axes3D

from .frames import AXES, Frame, Slice, VolumeFrame

VOLUME_AXIS_COLORS = ("#ff8c91", "#81e6af", "#80bdff")


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
        metadata=metadata,
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
        "Full 3D XYZ view  /  particles, field and trajectories  /  lattice coordinates",
        color="#91a4be",
        fontsize=10,
    )
    # Matplotlib draws this Hebrew-only label left-to-right; reverse its display order.
    fig.text(
        0.93,
        0.975,
        "תנע כולל במערכת"[::-1],
        ha="right",
        va="top",
        color="#edf5ff",
        fontsize=12,
        weight="bold",
    )
    status = fig.text(0.93, 0.94, "", ha="right", va="top", color="#c2d5ed", fontsize=11)
    for order, pid in enumerate(sorted({p[0] for frame in frames for p in frame.particles})):
        fig.text(
            0.28 + order * 0.16,
            0.095,
            f"●  Particle {pid}",
            color=colors[pid % len(colors)],
            fontsize=10,
        )
    fig.text(0.93, 0.055, "Warm glow: scalar field", color="#dcb485", ha="right", fontsize=10)
    fig.text(0.12, 0.18, "AXIS DIRECTIONS", color="#c2d5ed", ha="center", fontsize=8)
    # Smooth display geometry only: physical coordinates and integer state are untouched.
    longitude, latitude = np.meshgrid(np.linspace(0, 2 * np.pi, 21), np.linspace(0, np.pi, 13))
    sphere_x = 0.38 * np.cos(longitude) * np.sin(latitude)
    sphere_y = 0.38 * np.sin(longitude) * np.sin(latitude)
    sphere_z = 0.38 * np.cos(latitude)

    def draw(index: int) -> tuple[Artist, ...]:
        ax.clear()
        frame = frames[index]
        if frame.field:
            xs, ys, zs = zip(*frame.field, strict=True)
            values = list(frame.field.values())
            sizes = [28 + 130 * value / vmax for value in values]
            for spread, opacity in ((6, 0.035), (2.5, 0.07), (1, 0.16)):
                ax.scatter(
                    xs,
                    ys,
                    zs,
                    c=values,
                    cmap="YlOrBr_r",
                    vmin=0,
                    vmax=vmax,
                    s=[size * spread for size in sizes],
                    alpha=opacity,
                    edgecolors="none",
                    depthshade=False,
                )
        for pid, x, y, z, px, py, pz in frame.particles:
            color = colors[pid % len(colors)]
            trail = [p[1:4] for past in frames[: index + 1] for p in past.particles if p[0] == pid]
            tx, ty, tz = zip(*trail, strict=True)
            ax.plot(tx, ty, tz, color=color, linewidth=7, alpha=0.07)
            ax.plot(tx, ty, tz, color=color, linewidth=1.8, alpha=0.9)
            ax.scatter(
                [x], [y], [z], color=color, s=750, alpha=0.04, edgecolors="none", depthshade=False
            )
            ax.scatter(
                [x], [y], [z], color=color, s=320, alpha=0.10, edgecolors="none", depthshade=False
            )
            ax.plot_surface(
                x + sphere_x,
                y + sphere_y,
                z + sphere_z,
                color=color,
                linewidth=0,
                antialiased=True,
                shade=True,
            )
            scale = max(1, abs(px) + abs(py) + abs(pz))
            ax.quiver(
                x,
                y,
                z,
                1.8 * px / scale,
                1.8 * py / scale,
                1.8 * pz / scale,
                color=color,
                linewidth=1.4,
                arrow_length_ratio=0.3,
            )
            ax.text(x, y, z + 0.8, str(pid), color="#eff6ff", fontsize=10)
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
        for x in ax.get_xticks():
            if bounds[0][0] <= x <= bounds[0][1]:
                ax.plot([x, x], bounds[1], [bounds[2][0]] * 2, color="#38516d", linewidth=0.85)
        for y in ax.get_yticks():
            if bounds[1][0] <= y <= bounds[1][1]:
                ax.plot(bounds[0], [y, y], [bounds[2][0]] * 2, color="#38516d", linewidth=0.85)
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
        metadata=metadata,
        note="Soft markers show all nonzero field cells; brightness and size indicate field value. "
        "Particle spheres and glow are display symbols, not physical particle sizes. "
        "Lines show sampled paths. X is coral, Y is green and Z is blue. "
        "The corner arrows show positive axis directions, not a position or distance scale. "
        "System momentum is the combined momentum of particles and field. "
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
    encoded = base64.b64encode(gif_path.read_bytes()).decode("ascii")
    details = html.escape(json.dumps(dict(metadata or {}), indent=2, ensure_ascii=False))
    text = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>
body{{margin:0;background:#111827;color:#e5e7eb;font-family:system-ui}}
main{{max-width:1050px;margin:auto;padding:24px}}img{{max-width:100%;border-radius:12px}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#1f2937;padding:16px}}
</style></head><body><main><h1>{html.escape(title)}</h1>
<p>Full 3D physics · {plane_label} · ticks {ticks[0]}–{ticks[1]}</p>
<p>Frames may be sampled. Arrows show direction; their length is scaled for visibility.</p>
<p>{html.escape(note)}</p>
<img alt="Simulation: {plane_label}" src="data:image/gif;base64,{encoded}">
<details><summary>Run parameters and checks</summary><pre>{details}</pre></details>
</main></body></html>"""
    html_path.write_text(text, encoding="utf-8")
    return html_path
