"""Render saved radial stock only; no simulation or physical interpolation."""

import argparse
import io
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    directory = args.evidence / "octant_base"
    frames = json.loads((directory / "frames.json").read_text())
    images = []
    for frame in frames:
        fig = plt.figure(figsize=(7, 8), facecolor="#101927")
        fig.suptitle("Local spreading: what actually emerges", color="white", fontsize=16)
        ax = fig.add_axes([0.06, 0.40, 0.88, 0.49], projection="3d", facecolor="#101927")
        data = np.array(frame["points"])
        points = ax.scatter(
            data[:, 0],
            data[:, 1],
            data[:, 2],
            c=data[:, 3],
            cmap="YlOrBr",
            norm=LogNorm(1, 30000),
            s=9,
            alpha=0.65,
        )
        ax.scatter([0], [0], [0], s=95, c="#55ddff", marker="*")
        for setter in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
            setter(-9, 9)
        ax.set_xlabel("X", color="white")
        ax.set_ylabel("Y", color="white")
        ax.set_zlabel("Z", color="white")
        ax.tick_params(colors="#ccd7e5", labelsize=8)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=24, azim=30 + frame["tick"] * 3)
        ax.set_title(
            f"Completed steps: {frame['tick']} | Manhattan radius <= 9", color="white", fontsize=11
        )
        bar = fig.colorbar(points, ax=ax, shrink=0.48, pad=0.01)
        bar.set_label("Scalar stock / Node (log scale)", color="white", fontsize=9)
        bar.ax.tick_params(colors="white", labelsize=8)
        chart = fig.add_axes([0.14, 0.13, 0.75, 0.21], facecolor="#101927")
        lookup = {tuple(row[:3]): row[3] for row in frame["points"]}
        values = [lookup.get((5, 0, 0), 0), lookup.get((3, 4, 0), 0)]
        chart.bar([0, 1], values, color=["#55ddff", "#ffb34f"], width=0.5)
        chart.set_xticks([0, 1], ["(5, 0, 0)", "(3, 4, 0)"])
        chart.set_ylim(0, 750)
        chart.set_title("Same Euclidean distance: 5 | Different local stock", color="white", fontsize=11)
        chart.tick_params(colors="white")
        chart.set_ylabel("Scalar stock", color="white")
        for index, value in enumerate(values):
            chart.text(index, value + 20, str(value), ha="center", color="white", fontsize=12)
        fig.text(
            0.5,
            0.04,
            "Recorded world audit. No force, gravity or observer image is inferred.",
            color="#ccd7e5",
            fontsize=9,
            ha="center",
        )
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=100, facecolor=fig.get_facecolor())
        buffer.seek(0)
        images.append(Image.open(buffer).convert("RGB"))
        plt.close(fig)
    target = args.evidence / "radial-emergence.gif"
    images[0].save(
        target,
        save_all=True,
        append_images=images[1:],
        duration=[220] * (len(images) - 1) + [1600],
        optimize=True,
    )
    images[0].save(args.evidence / "first-frame.png")
    images[-1].save(args.evidence / "last-frame.png")
    with Image.open(target) as decoded:
        for index in range(decoded.n_frames):
            decoded.seek(index)
            decoded.load()
        print(
            json.dumps(
                {
                    "file": str(target),
                    "frames": decoded.n_frames,
                    "size": decoded.size,
                    "bytes": target.stat().st_size,
                    "loops": decoded.info.get("loop", "none"),
                }
            )
        )


if __name__ == "__main__":
    main()
