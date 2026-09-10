"""The existing make_v7_run_html.py rendering pipeline, extracted and generalized.

Still uses imshow + FuncAnimation + PillowWriter and a GIF embedded in standalone
HTML. Rendering is diagnostic only; no rendered value is fed into the engine.
"""

import base64
import html
import json
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.artist import Artist
from matplotlib.figure import Figure

from .frames import AXES, Frame, Slice, VolumeFrame


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
    bounds = [(min(p[axis] for p in points) - 2, max(p[axis] for p in points) + 2) for axis in range(3)]
    vmax = max(1, max((value for frame in frames for value in frame.field.values()), default=1))
    fig = plt.figure(figsize=(9, 7.5), facecolor="#111827")
    ax = fig.add_subplot(111, projection="3d", facecolor="#111827")
    colors = ("#4cc9ff", "#74ffac", "#ffd166", "#fa8cff")

    def draw(index: int) -> tuple[Artist, ...]:
        ax.clear()
        frame = frames[index]
        if frame.field:
            xs, ys, zs = zip(*frame.field, strict=True)
            values = list(frame.field.values())
            ax.scatter(
                xs,
                ys,
                zs,
                c=values,
                cmap="autumn",
                vmin=0,
                vmax=vmax,
                s=[18 + 110 * value / vmax for value in values],
                alpha=0.35,
                edgecolors="none",
                depthshade=False,
            )
        for pid, x, y, z, px, py, pz in frame.particles:
            color = colors[pid % len(colors)]
            trail = [p[1:4] for past in frames[: index + 1] for p in past.particles if p[0] == pid]
            tx, ty, tz = zip(*trail, strict=True)
            ax.plot(tx, ty, tz, color=color, linewidth=2, alpha=0.9)
            ax.scatter([x], [y], [z], color=color, s=110, edgecolors="white", depthshade=False)
            scale = max(1, abs(px) + abs(py) + abs(pz))
            ax.quiver(
                x,
                y,
                z,
                2.5 * px / scale,
                2.5 * py / scale,
                2.5 * pz / scale,
                color=color,
                linewidth=2,
                arrow_length_ratio=0.3,
            )
            ax.text(x, y, z + 0.7, str(pid), color=color, fontsize=12)
        ax.set_xlim(*bounds[0])
        ax.set_ylim(*bounds[1])
        ax.set_zlim(*bounds[2])
        ax.set_box_aspect(tuple(hi - lo for lo, hi in bounds))
        ax.view_init(elev=26, azim=-65 + 35 * index / max(1, len(frames) - 1))
        for axis, label in ((ax.xaxis, "x"), (ax.yaxis, "y"), (ax.zaxis, "z")):
            axis.set_pane_color((0.10, 0.15, 0.23, 0.8))
            axis.label.set_color("white")
            axis.set_label_text(label)
        ax.tick_params(colors="#d1d5db")
        ax.set_title(
            f"Full 3D XYZ view | tick={frame.tick}\nPtotal={frame.total_momentum}", color="white", pad=18
        )
        return tuple(ax.get_children())

    return _save_animation_html(
        fig,
        draw,
        len(frames),
        (frames[0].tick, frames[-1].tick),
        "Full 3D XYZ view",
        html_path,
        title=title,
        metadata=metadata,
        note="Dots show all nonzero field cells; brightness and size indicate field value. "
        "Lines show sampled particle paths. The camera rotates; coordinates and physics do not.",
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
) -> Path:
    """One shared GIF/HTML output pipeline for plane and volume renderers."""
    html_path.parent.mkdir(parents=True, exist_ok=True)
    gif_path = html_path.with_suffix(".gif")
    try:
        animation = FuncAnimation(fig, draw, frames=frame_count, interval=120)
        animation.save(str(gif_path), writer=PillowWriter(fps=8), dpi=65 if compact else 100)
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
