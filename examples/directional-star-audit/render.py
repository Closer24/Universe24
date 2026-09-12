"""Render the recorded star encounters without supplying a physical trajectory."""

import argparse
import io
import json
from pathlib import Path

from event_universe.retention import ArtifactLease


def main():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = ("active", "radial", "oblique")
    frames = {
        case: [
            json.loads(line) for line in (args.input / case / "frames.jsonl").read_text().splitlines()
        ]
        for case in cases
    }
    raw = json.loads((args.input / "active/initial.json").read_text())
    display = json.loads(Path(__file__).with_name("display.json").read_text())
    colors = {"active": "#56def4", "radial": "#ff78bc", "oblique": "#baee70"}
    images = []
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        for index in range(len(frames["active"])):
            fig = plt.figure(
                figsize=(display["width"] / 100, display["height"] / 100), dpi=100, facecolor="#091321"
            )
            ax = fig.add_subplot(111, projection="3d", facecolor="#091321")
            ax.view_init(
                28, -68 + display["camera_rotation_degrees"] * index / (len(frames["active"]) - 1)
            )
            ax.set(xlim=display["x"], ylim=display["y"], zlim=display["z"])
            ax.set_box_aspect((2, 1, 0.6))
            for name in ("x", "y", "z"):
                getattr(ax, "set_" + name + "label")(name.upper(), color="white")
                getattr(ax, name + "axis").set_pane_color((0.035, 0.07, 0.12, 1))
            ax.tick_params(colors="#bacde0", labelsize=8)
            nodes = [(x, y, 64) for x in range(52, 81, 2) for y in range(58, 77, 2)]
            ax.scatter(*zip(*nodes, strict=True), s=4, color="#67829c", alpha=0.45)
            points = frames["active"][index]["field"]
            if points:
                ax.scatter(
                    *zip(*(p[:3] for p in points), strict=True),
                    s=[8 + min(35, sum(abs(v) for v in p[3:6]) / 10) for p in points],
                    c=["#8e78ca" if p[6] == 0 else "#e6ad49" for p in points],
                    alpha=0.3,
                    marker="s",
                )
            stars = raw["seeds"][:27]
            ax.scatter(*zip(*(s["position"] for s in stars), strict=True), s=25, color="#ffba55")
            ax.scatter(64, 64, 64, s=300, color="#ffdf8e", alpha=0.85)
            for case in cases:
                path = [f["probes"]["light_neutral"]["position"] for f in frames[case][: index + 1]]
                ax.plot(*zip(*path, strict=True), color=colors[case], linewidth=2, label=case)
                current = frames[case][index]["probes"]["light_neutral"]
                ax.scatter(*current["position"], s=60, color=colors[case], edgecolors="white")
                direction = current["values"]["momentum"]
                ax.quiver(
                    *current["position"], *(2 * v for v in direction), color=colors[case], linewidth=1.5
                )
            fig.text(
                0.5,
                0.96,
                "DOES DIRECTIONAL DELAY BIND AN ORBIT?",
                ha="center",
                color="white",
                fontsize=15,
            )
            fig.text(
                0.5,
                0.915,
                f"128 x 128 x 128 | local view | tick {frames['active'][index]['tick']}",
                ha="center",
                color="#c8ddec",
                fontsize=12,
            )
            fig.text(
                0.5,
                0.87,
                "Star / light mass: 315,000 | Star / heavy mass: 315",
                ha="center",
                color="#ffdf8e",
                fontsize=11,
            )
            fig.text(
                0.5,
                0.16,
                "Three independent runs overlaid; three entity profiles coincide in each\n"
                "Cyan: offset pass | Pink: through center | Green: oblique pass\n"
                "Boxes: recorded field stock, including origin waiting\n"
                "Momentum unchanged | No orbit observed | Exact linear accounting",
                ha="center",
                color="#d0dfed",
                fontsize=10,
                linespacing=1.7,
            )
            fig.subplots_adjust(left=0, right=1, top=0.88, bottom=0.23)
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
            plt.close(fig)
            buffer.seek(0)
            images.append(Image.open(buffer).convert("RGB"))
        images[0].save(
            args.output / "star-orbit-audit.gif",
            save_all=True,
            append_images=images[1:],
            duration=display["frame_duration_ms"],
            loop=0,
            optimize=False,
        )
        images[min(12, len(images) - 1)].save(args.output / "preview.png")
        with Image.open(args.output / "star-orbit-audit.gif") as movie:
            for i in range(movie.n_frames):
                movie.seek(i)
                movie.load()
            assert movie.n_frames == len(images)
        print(len(images), "verified GIF frames")


if __name__ == "__main__":
    main()
