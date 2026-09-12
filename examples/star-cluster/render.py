"""Render recorded star trajectories and an actual field slice without physics updates."""

import argparse
import io
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

from event_universe.retention import ArtifactLease


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--display", type=Path, default=Path(__file__).with_name("display.json"))
    args = parser.parse_args()
    display = json.loads(args.display.read_text())
    args.cases = display["cases"]
    series = [json.loads((args.input / name / "trajectory.json").read_text()) for name in args.cases]
    results = [json.loads((args.input / name / "result.json").read_text()) for name in args.cases]
    horizon = max(len(s) for s in series) - 1
    count = display["maximum_frames"]
    if count < 2 or display["frame_duration_ms"] < 10:
        raise ValueError("Display needs at least two frames and ten milliseconds per frame")
    sample_ticks = sorted(set(round(i * horizon / (count - 1)) for i in range(count)))
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        frames = []
        for tick in sample_ticks:
            fig = plt.figure(
                figsize=(display["width_inches"], display["panel_height_inches"] * len(series)),
                dpi=display["dpi"],
                facecolor="#091321",
            )
            for panel, (name, states, result) in enumerate(
                zip(args.cases, series, results, strict=True), 1
            ):
                index = min(tick, len(states) - 1)
                state = states[index]
                ax = fig.add_subplot(len(series), 1, panel, projection="3d", facecolor="#091321")
                ax.view_init(
                    elev=24, azim=-55 + display["camera_rotation_degrees"] * tick / max(horizon, 1)
                )
                ax.set(xlim=(0, 10), ylim=(0, 10), zlim=(0, 10))
                ax.set_box_aspect((1, 1, 0.8))
                for label in ("x", "y", "z"):
                    getattr(ax, "set_" + label + "label")(label.upper(), color="white")
                    axis = getattr(ax, label + "axis")
                    axis.set_pane_color((0.05, 0.09, 0.14, 1))
                ax.tick_params(colors="#a8bed0", labelsize=8)
                nodes = [
                    (x, y, z) for x in range(0, 11, 2) for y in range(0, 11, 2) for z in range(0, 11, 2)
                ]
                ax.scatter(*zip(*nodes, strict=True), s=6, c="#668298", alpha=0.45)
                sources = state["sources"]
                if sources:
                    ax.scatter(
                        *zip(*(s["position"] for s in sources), strict=True),
                        s=[max(12, math.sqrt(s["values"]["mass"][0]) * 2) for s in sources],
                        c="#ffbd61",
                        alpha=0.9,
                    )
                path = [f["probe"]["position"] for f in states[: index + 1] if f["probe"]]
                if path:
                    ax.plot(*zip(*path, strict=True), color="#69e6ff", linewidth=2)
                probe = state["probe"]
                if probe:
                    ax.scatter(*probe["position"], s=80, c="#75efff", edgecolors="white")
                    velocity = [3 * p / probe["values"]["mass"][0] for p in probe["values"]["momentum"]]
                    ax.quiver(*probe["position"], *velocity, color="#ff7bc4", linewidth=2)
                sample = next(
                    (f["signal_slice"] for f in reversed(states[: index + 1]) if f["signal_slice"]), []
                )
                for x, y, z, _stock, fx, fy, fz in sample:
                    if (x == 5 or y == 5 or (x % 2 == 0 and y % 2 == 0)) and fx * fx + fy * fy + fz * fz:
                        # One fixed arrow scale for all nodes, ticks and cases.
                        ax.quiver(
                            x,
                            y,
                            z,
                            fx / 80,
                            fy / 80,
                            fz / 80,
                            color="#779cf5",
                            alpha=0.8,
                            linewidth=0.9,
                        )
                status = result["classification"] if tick >= len(states) - 1 else "running"
                ax.set_title(
                    name.replace("_", " ") + f"  |  tick {state['tick']}  |  {status}",
                    color="white",
                    fontsize=11,
                    pad=2,
                )
                ax.text2D(
                    0.02,
                    0.92,
                    f"In-domain K proxy: {state['kinetic_proxy']:.2f}  |  total energy undefined",
                    transform=ax.transAxes,
                    color="#bfccd9",
                    fontsize=9,
                )
            fig.suptitle(
                "Recorded lattice encounters\nOrange: masses   Cyan: path   Pink: p/m\nBlue: signal at Z=5, sampled every 4 ticks; nodes shown every 2 cells",
                color="white",
                fontsize=11,
                y=0.98,
            )
            fig.subplots_adjust(top=0.91, bottom=0.025, hspace=0.14)
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
            plt.close(fig)
            buffer.seek(0)
            frames.append(Image.open(buffer).convert("RGB").copy())
        path = args.output / "star-encounters.gif"
        frames[0].save(
            path,
            save_all=True,
            append_images=frames[1:],
            duration=display["frame_duration_ms"],
            loop=0,
            optimize=True,
        )
        with Image.open(path) as gif:
            for frame in range(gif.n_frames):
                gif.seek(frame)
                gif.load()
            proof = {
                "frames": gif.n_frames,
                "size": list(gif.size),
                "bytes": path.stat().st_size,
                "cases": args.cases,
                "ticks": sample_ticks,
                "decoded_all_frames": True,
            }
        frames[len(frames) // 2].save(args.output / "preview.png")
        (args.output / "render.json").write_text(json.dumps(proof, indent=2))
        print(json.dumps(proof))


if __name__ == "__main__":
    main()
