"""Render saved many-contact results without advancing or altering a world.

Panels use an oblique projection of actual three-dimensional Node coordinates.
Lines identify configured Links, not particle trajectories. The ordinary field
is the combined saved local value; it is never attributed to a particular source.
"""

import json
from io import BytesIO
from pathlib import Path
from typing import Any

BACKGROUND = "#f4f6f8"
INK = "#233344"
QUANTUM = "#007fa8"
LOCALIZED = "#972fc5"
INCOMING = "#bc4848"


def _project(position: list[int], center: list[int]) -> tuple[float, float]:
    """Project recorded coordinates for display only, without motion interpolation."""
    x, y, z = (p - c for p, c in zip(position, center, strict=True))
    return x - 0.48 * z, y + 0.52 * z


def _value(node: dict[str, Any]) -> int:
    return int(node["fields"]["electric_signal"]["value"][0])


def _captures(frame: dict[str, Any]) -> list[dict[str, Any]]:
    return [t for t in frame["contact_transfers"] if t["direction"] == "to_localized"]


def _draw_frame(
    frame: dict[str, Any],
    domains: list[dict[str, Any]],
    maximum: int,
    plt: Any,
    colors: Any,
    line: Any,
) -> Any:
    fig, axes = plt.subplots(2, 3, figsize=(14, 9), dpi=120)
    fig.set_facecolor(BACKGROUND)
    field_norm = colors.Normalize(vmin=0, vmax=max(1, maximum))
    captures = _captures(frame)
    fig.suptitle(
        f"Local quantum sources and ordinary fields  |  tick {frame['tick']:02d}",
        x=0.05,
        y=0.985,
        ha="left",
        color=INK,
        fontsize=19,
        fontweight="bold",
    )
    fig.text(
        0.05,
        0.94,
        "Six independent origins; three physical targets each. Every frame is a saved tick.",
        fontsize=11,
        color=INK,
    )
    for axis, domain in zip(axes.flat, domains, strict=True):
        center = domain["hub"]
        axis.set_facecolor("white")
        axis.set_aspect("equal")
        axis.set_xlim(-2.2, 2.2)
        axis.set_ylim(-1.5, 1.95)
        axis.set_xticks([])
        axis.set_yticks([])
        for spine in axis.spines.values():
            spine.set_color("#d7dfe6")
        points = {"S": domain["source"], "H": center, **domain["targets"]}
        for label, position in points.items():
            x, y = _project(position, center)
            if label != "H":
                axis.plot([0, x], [0, y], color="#cbd3dd", linewidth=1.8, zorder=2)
            axis.scatter([x], [y], marker="s", s=105, c="#566576", zorder=4)
            axis.text(x + 0.11, y + 0.12, label, fontsize=11, color=INK, zorder=9)

        local_field = [
            node
            for node in frame.get("spatial_fields", [])
            if _value(node)
            and all(abs(p - c) <= 2 for p, c in zip(node["position"], center, strict=True))
        ]
        if local_field:
            projected = [_project(node["position"], center) for node in local_field]
            axis.scatter(
                [p[0] for p in projected],
                [p[1] for p in projected],
                c=[abs(_value(node)) for node in local_field],
                norm=field_norm,
                cmap="YlOrBr",
                marker="o",
                s=450,
                alpha=0.85,
                linewidths=0,
                zorder=1,
            )
        for envelope in frame["source_envelopes"]:
            if envelope["position"] not in points.values():
                continue
            real, imaginary, denominator = envelope["amplitude"]
            weight = (real * real + imaginary * imaginary) / (denominator * denominator)
            if envelope["retired"] or not weight:
                continue
            x, y = _project(envelope["position"], center)
            axis.scatter(
                [x],
                [y],
                s=1500 * weight,
                facecolors="none",
                edgecolors=QUANTUM,
                linewidths=2.5,
                zorder=6,
            )
            axis.text(
                x,
                y - 0.26,
                f"w={weight:.3g}",
                ha="center",
                color=QUANTUM,
                fontsize=10,
                zorder=9,
                bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "none", "pad": 1},
            )
        for node in frame["nodes"]:
            if node["position"] not in points.values():
                continue
            for disturbance in node["disturbances"]:
                if disturbance["type"] not in ("incoming_charge", "localized_charge"):
                    continue
                x, y = _project(node["position"], center)
                localized = disturbance["type"] == "localized_charge"
                axis.scatter(
                    [x],
                    [y],
                    marker="*" if localized else "D",
                    s=400 if localized else 140,
                    c=LOCALIZED if localized else INCOMING,
                    edgecolors="white",
                    linewidths=1,
                    zorder=10,
                )
                if localized:
                    axis.text(x, y - 0.38, "localized", ha="center", color=LOCALIZED, fontsize=10)
        captured = next((c for c in captures if c["domain"] == domain["name"]), None)
        status = "No localized capture yet"
        if captured is not None:
            target = next(k for k, p in domain["targets"].items() if p == captured["address"])
            status = f"Captured at {target}, tick {captured['tick']}"
        axis.set_title(f"{domain['name']}  |  {status}", fontsize=11, color=INK, pad=10)
        axis.text(
            0.025,
            0.03,
            f"Hub {tuple(center)}\nOblique XYZ view; no interpolated path",
            transform=axis.transAxes,
            fontsize=8,
            color="#647384",
        )
        for label, end, color in (
            ("X", (0.33, 0), "#c05245"),
            ("Y", (0, 0.33), "#32845a"),
            ("Z", (-0.16, 0.17), "#3b65ab"),
        ):
            ox, oy = 1.6, -1.05
            axis.annotate(
                "",
                xy=(ox + end[0], oy + end[1]),
                xytext=(ox, oy),
                arrowprops={"arrowstyle": "->", "color": color, "lw": 1.2},
            )
            axis.text(ox + end[0], oy + end[1] + 0.07, label, fontsize=8, color=color)

    handles = [
        line(
            [],
            [],
            marker="o",
            color=QUANTUM,
            markerfacecolor="none",
            linestyle="none",
            markersize=12,
            label="Local source weight w (ring area)",
        ),
        line(
            [],
            [],
            marker="o",
            color="#c18120",
            linestyle="none",
            markersize=8,
            label=f"Combined |electric_signal| (fixed scale 0–{maximum})",
        ),
        line(
            [],
            [],
            marker="*",
            color=LOCALIZED,
            linestyle="none",
            markersize=14,
            label="Actual localized output",
        ),
        line(
            [],
            [],
            marker="D",
            color=INCOMING,
            linestyle="none",
            markersize=7,
            label="Initial charged input",
        ),
        line(
            [],
            [],
            marker="s",
            color="#566576",
            linestyle="none",
            markersize=8,
            label="Configured Node: S source, H transit, A/B/C targets",
        ),
    ]
    fig.legend(
        handles=handles,
        loc="lower left",
        bbox_to_anchor=(0.04, 0.065),
        ncol=2,
        frameon=False,
        fontsize=10,
    )
    retired = sum(bool(node["retired"]) for node in frame["source_envelopes"])
    stock = sum(_value(node) for node in frame.get("spatial_fields", []))
    fig.text(
        0.05,
        0.049,
        f"Captures: {len(captures)}/6   |   Retired envelopes: {retired}/30   |   "
        f"Recorded ordinary field at Nodes: {stock}",
        fontsize=10,
        color=INK,
    )
    fig.text(
        0.05,
        0.022,
        "w is the local retarded source envelope, not the exact conditional probability "
        "after measurement. Orange samples include all sources.",
        fontsize=9,
        color="#647384",
    )
    fig.subplots_adjust(left=0.04, right=0.975, top=0.875, bottom=0.19, hspace=0.31, wspace=0.14)
    return fig


def _overview(summary: dict[str, Any], frame: dict[str, Any], output: Path, plt: Any) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.7), dpi=150, gridspec_kw={"width_ratios": [1, 1.1]})
    fig.set_facecolor(BACKGROUND)
    total = summary["total_captures"]
    fig.suptitle(
        f"{total:,} localized captures across {summary['trial_count']} runs",
        x=0.06,
        y=0.97,
        ha="left",
        fontsize=20,
        color=INK,
        fontweight="bold",
    )
    fig.text(
        0.06,
        0.9,
        "6 independent charged excitations + 18 massive targets per run",
        color=INK,
        fontsize=11,
    )
    labels = list(summary["expected_probabilities"])
    observed = [100 * summary["counts"][label] / total for label in labels]
    expected = [100 * summary["expected_probabilities"][label] for label in labels]
    axis = axes[0]
    axis.set_facecolor("white")
    bars = axis.bar(
        labels, observed, color=[QUANTUM, "#55a0b9", "#8cbaca"], width=0.55, label="Measured captures"
    )
    axis.scatter(
        labels,
        expected,
        marker="_",
        s=700,
        linewidths=3,
        color=INK,
        zorder=4,
        label="Configured Born target",
    )
    for bar, value, label in zip(bars, observed, labels, strict=True):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value + 4,
            f"{summary['counts'][label]}\n{value:.2f}%",
            ha="center",
            color=INK,
            fontsize=11,
        )
    axis.set_ylim(0, 84)
    axis.set_ylabel("Captures (%)", color=INK)
    axis.set_title("Observed distribution", loc="left", color=INK, fontsize=13)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, loc="upper right", fontsize=9)
    axis.grid(axis="y", alpha=0.15)
    axis.set_axisbelow(True)
    axes[1].axis("off")
    axes[1].set_title(
        f"Recorded example: seed {summary['seed_start']}", loc="left", fontsize=13, color=INK
    )
    captures = _captures(frame)
    rows = []
    for domain in summary["domains"]:
        capture = next((c for c in captures if c["domain"] == domain["name"]), None)
        if capture is None:
            rows.append([domain["name"], "None", "—", "—"])
        else:
            target = next(k for k, p in domain["targets"].items() if p == capture["address"])
            rows.append([domain["name"], target, str(capture["tick"]), str(tuple(capture["address"]))])
    table = axes[1].table(
        cellText=rows,
        colLabels=["Origin", "Target", "Tick", "XYZ"],
        loc="upper left",
        cellLoc="left",
        colLoc="left",
        colWidths=[0.26, 0.16, 0.12, 0.36],
        bbox=[0, 0.29, 1, 0.67],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#d7dfe6")
        cell.set_facecolor("#e7edf2" if row == 0 else "white")
        cell.set_text_props(color=INK, weight="bold" if row == 0 else "normal")
    axes[1].text(
        0,
        0.24,
        "A, B and C are each two physical Links from S.\n"
        "Detection appears at a discrete local event;\n"
        "the animation shows every recorded tick, without a path guess.",
        transform=axes[1].transAxes,
        fontsize=10,
        color=INK,
        linespacing=1.6,
        va="top",
    )
    fig.text(
        0.06,
        0.06,
        "These are finite configured quantum-contact trials, not repeated hopping of the "
        "same particle or a claim of full electromagnetic dynamics.",
        color="#647384",
        fontsize=9,
    )
    fig.subplots_adjust(left=0.075, right=0.97, bottom=0.2, top=0.79, wspace=0.27)
    target = output / "overview.png"
    fig.savefig(target, facecolor=fig.get_facecolor())
    plt.close(fig)
    return target


def render_experiment(output: Path) -> tuple[Path, ...]:
    """Save an overview, faithful tick replay and selected actual-frame PNGs."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.colors as colors
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from PIL import Image

    from event_universe.retention import ArtifactLease

    output = output.resolve()
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    frames = json.loads((output / "representative/frames.json").read_text(encoding="utf-8"))
    if not frames or len(summary["domains"]) != 6:
        raise ValueError("many-contact view requires recorded frames and six configured domains")
    ticks = [frame["tick"] for frame in frames]
    if ticks != list(range(ticks[0], ticks[-1] + 1)):
        raise ValueError("many-contact view requires consecutive saved ticks")
    maximum = max(
        (abs(_value(node)) for frame in frames for node in frame.get("spatial_fields", [])), default=0
    )
    images = []
    selected = {0, len(frames) - 1}
    selected.add(
        max(range(len(frames)), key=lambda i: sum(abs(_value(n)) for n in frames[i]["spatial_fields"]))
    )
    first_capture = next((i for i, frame in enumerate(frames) if _captures(frame)), None)
    if first_capture is not None:
        selected.add(first_capture)
    saved = [output / "overview.png"]
    saved.extend(output / f"tick-{frames[index]['tick']:02d}.png" for index in sorted(selected))
    saved.append(output / "replay.gif")
    for target in saved:
        target.touch(exist_ok=True)
    with ArtifactLease(output, saved):
        _overview(summary, frames[-1], output, plt)
        for index, frame in enumerate(frames):
            fig = _draw_frame(frame, summary["domains"], maximum, plt, colors, Line2D)
            data = BytesIO()
            fig.savefig(data, format="png", facecolor=fig.get_facecolor())
            plt.close(fig)
            data.seek(0)
            with Image.open(data) as rendered:
                images.append(rendered.convert("RGB"))
            if index in selected:
                images[-1].save(output / f"tick-{frame['tick']:02d}.png")
        images[0].save(
            output / "replay.gif",
            save_all=True,
            append_images=images[1:],
            duration=[900 if frame["tick"] < 9 else 450 for frame in frames[:-1]] + [3000],
            disposal=2,
            optimize=False,
        )
    for rendered in images:
        rendered.close()
    return tuple(saved)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Completed many-contact experiment output directory")
    for artifact in render_experiment(parser.parse_args().output):
        print(artifact)
