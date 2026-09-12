"""Render the saved delay-only run beside its zero-emission reference."""

import argparse
import io
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

from event_universe.retention import ArtifactLease


def read_frames(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--display", type=Path, default=Path(__file__).with_name("display.json"))
    args = parser.parse_args()
    display = json.loads(args.display.read_text())
    active = read_frames(args.input / "active/frames.jsonl")
    reference = read_frames(args.input / "no_field/frames.jsonl")
    raw = json.loads((args.input / "active/initial.json").read_text())
    stars = [s for s in raw["seeds"] if s["type"] == "star_constituent"]
    colors = {"inner": "#64eaff", "middle": "#b5ed6a", "outer": "#ff88c4"}
    images = []
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        for index in range(0, len(active), display["frame_stride"]):
            current = active[index]
            fig = plt.figure(
                figsize=(display["width"] / 100, display["height"] / 100), dpi=100, facecolor="#091321"
            )
            ax = fig.add_subplot(111, projection="3d", facecolor="#091321")
            ax.view_init(
                elev=31, azim=-68 + display["camera_rotation_degrees"] * index / (len(active) - 1)
            )
            ax.set(xlim=display["view"]["x"], ylim=display["view"]["y"], zlim=display["view"]["z"])
            ax.set_box_aspect((2, 1, 0.65))
            for axis_name in ("x", "y", "z"):
                getattr(ax, "set_" + axis_name + "label")(axis_name.upper(), color="white")
                getattr(ax, axis_name + "axis").set_pane_color((0.035, 0.07, 0.12, 1))
            ax.tick_params(colors="#a4bad0", labelsize=9)
            nodes = [(x, y, 32) for x in range(20, 61, 2) for y in range(26, 46, 2)]
            ax.scatter(*zip(*nodes, strict=True), s=3, color="#55718a", alpha=0.5)
            if current["field_slice"]:
                points = current["field_slice"]
                magnitudes = [sum(abs(v) for v in p[3:]) for p in points]
                ax.scatter(
                    *zip(*(p[:3] for p in points), strict=True),
                    c=magnitudes,
                    cmap="Purples",
                    vmin=0,
                    vmax=600,
                    s=12,
                    alpha=0.7,
                    marker="s",
                )
            for star in stars:
                center = star["position"] == [32, 32, 32]
                ax.scatter(
                    *star["position"],
                    s=750 if center else 18,
                    color="#ffbd54" if center else "#d79743",
                    alpha=0.9,
                    edgecolors="none",
                )
            for name, color in colors.items():
                path = [
                    f["probes"][name]["position"] for f in active[: index + 1] if name in f["probes"]
                ]
                if path:
                    ax.plot(*zip(*path, strict=True), color=color, linewidth=2)
                probe = current["probes"].get(name)
                if probe:
                    ax.scatter(*probe["position"], s=55, color=color, edgecolors="white")
                    ax.quiver(*probe["position"], 2, 0, 0, color=color, linewidth=1.5)
                control = reference[index]["probes"].get(name)
                if control:
                    ax.scatter(
                        *control["position"], s=70, facecolors="none", edgecolors=color, alpha=0.6
                    )
            fig.text(0.5, 0.96, "COMPUTATIONAL LOAD ONLY", ha="center", color="white", fontsize=17)
            fig.text(
                0.5,
                0.925,
                f"64 x 64 x 64 space  |  star / probe mass = 315,000  |  tick {current['tick']}",
                ha="center",
                color="#d0dfed",
                fontsize=10,
            )
            fig.text(
                0.5,
                0.89,
                "No force coupling. Momentum arrows remain unchanged.",
                ha="center",
                color="#a6bfd8",
                fontsize=10,
            )
            positions = [current["probes"].get(n, {}).get("position", [None])[0] for n in colors]
            labels = "   ".join(f"{n}: x={x}" for n, x in zip(colors, positions, strict=True))
            fig.text(0.5, 0.14, labels, ha="center", color="white", fontsize=11)
            fig.text(
                0.5,
                0.105,
                "Hollow markers: no-field control   |   Purple: vector-load magnitude",
                ha="center",
                color="#becddd",
                fontsize=9,
            )
            fig.text(
                0.5,
                0.072,
                "Recorded global view, zoomed region. Marker size is illustrative.",
                ha="center",
                color="#8fa8be",
                fontsize=9,
            )
            fig.text(
                0.5,
                0.042,
                "The three tracks are independent probes, not one bound particle.",
                ha="center",
                color="#8fa8be",
                fontsize=9,
            )
            fig.subplots_adjust(top=0.87, bottom=0.18, left=0.02, right=0.98)
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
            plt.close(fig)
            buffer.seek(0)
            images.append(Image.open(buffer).convert("RGB").copy())
        gif_path = args.output / "computational-star.gif"
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=display["duration_ms"],
            loop=0,
            optimize=True,
        )
        with Image.open(gif_path) as gif:
            for frame in range(gif.n_frames):
                gif.seek(frame)
                gif.load()
            report = {
                "decoded_frames": gif.n_frames,
                "dimensions": list(gif.size),
                "bytes": gif_path.stat().st_size,
            }
        images[len(images) // 2].save(args.output / "preview.png")
        images[-1].save(args.output / "final.png")
        (args.output / "render.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report))


if __name__ == "__main__":
    main()
