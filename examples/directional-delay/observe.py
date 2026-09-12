"""Record and render a configured directional pulse and its timing control."""

import argparse
import io
import json
from copy import deepcopy
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease
from event_universe.runner import source_fingerprint


def record(raw, output):
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    expected = world.totals()
    frames = []
    for tick in range(raw["ticks"] + 1):
        if tick:
            world.step()
        totals, escaped = world.totals(), world.escaped_totals()
        assert all(
            tuple(a + b for a, b in zip(totals[k], escaped[k], strict=True)) == v
            for k, v in expected.items()
        )
        frames.append(world.snapshot())
    output.mkdir()
    (output / "initial.json").write_text(json.dumps(raw, indent=2))
    (output / "frames.jsonl").write_text("".join(json.dumps(f) + "\n" for f in frames))
    (output / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
    return frames, {
        "sent": sum(e["event"] == "sent" for e in events),
        "field_waits": sum(e["event"] == "spatial_departure_waiting" for e in events),
        "inventory_error": 0,
    }


def render(cases, display, output):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    images = []
    for index in range(len(cases[0])):
        fig = plt.figure(
            figsize=(display["width"] / 100, display["height"] / 100), dpi=100, facecolor="#091321"
        )
        for panel, frames in enumerate(cases):
            frame = frames[index]
            ax = fig.add_subplot(2, 1, panel + 1, projection="3d", facecolor="#091321")
            ax.view_init(25, -65 + display["camera_rotation_degrees"] * index / (len(frames) - 1))
            ax.set(xlim=display["view"], ylim=display["view"], zlim=display["view"])
            ax.set_box_aspect((1, 1, 0.65))
            ax.tick_params(colors="#c4daec", labelsize=8)
            for name in ("x", "y", "z"):
                getattr(ax, "set_" + name + "label")(name.upper(), color="white")
                getattr(ax, name + "axis").set_pane_color((0.035, 0.07, 0.12, 1))
            nodes = [(x, y, 32) for x in range(0, 65, 4) for y in range(0, 65, 4)]
            ax.scatter(*zip(*nodes, strict=True), s=2, color="#57718a", alpha=0.5)
            groups = {False: [], True: []}
            for cell in frame["spatial_fields"]:
                amount = sum(abs(v) for pop in cell["fields"]["pulse"]["populations"] for v in pop)
                if amount:
                    groups[False].append((cell["position"], 8 + amount))
            for packet in frame["spatial_transfers"]:
                amount = sum(abs(v) for pop in packet["fields"]["pulse"] for v in pop)
                if amount:
                    groups[packet.get("phase") == "waiting"].append((packet["origin"], 8 + amount))
            for waiting, points in groups.items():
                if points:
                    ax.scatter(
                        *zip(*(p for p, _ in points), strict=True),
                        s=[size for _, size in points],
                        color="#ffba54" if waiting else "#63d7e6",
                        marker="s" if waiting else ".",
                        alpha=0.7,
                    )
            records = [(c["position"], r) for c in frame["cells"] for r in c["disturbances"]]
            records += [(p["origin"], p) for p in frame["transfers"]]
            for position, record in records:
                color = "#ff73b9" if record["type"] == "right" else "#adf481"
                ax.scatter(*position, s=65, color=color, edgecolors="white")
                momentum = record["values"]["momentum"]
                ax.quiver(*position, *(3 * v for v in momentum), color=color, linewidth=2)
            ax.set_title(
                "DIRECTIONAL WAIT: load = (6, 0, 0)" if panel == 0 else "CONTROL: NO DIRECTIONAL WAIT",
                color="white",
                fontsize=13,
                pad=0,
            )
        fig.text(
            0.5,
            0.975,
            f"Particles AND field transfers | tick {index}",
            ha="center",
            color="white",
            fontsize=16,
        )
        fig.text(
            0.5,
            0.035,
            "Orange squares: field waiting at origin | Cyan: pulse stock / transit\n"
            "Pink: +X particle | Green: -X particle | Arrows: unchanged momentum\n"
            "64 x 64 x 64 nodes | Exact inventory balance | Saved integer-tick states",
            ha="center",
            color="#d1dfed",
            fontsize=10,
            linespacing=1.6,
        )
        fig.subplots_adjust(top=0.94, bottom=0.11, hspace=0.14)
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
        plt.close(fig)
        buffer.seek(0)
        images.append(Image.open(buffer).convert("RGB"))
    images[0].save(
        output / "directional-delay.gif",
        save_all=True,
        append_images=images[1:],
        duration=display["frame_duration_ms"],
        loop=0,
        optimize=False,
    )
    images[len(images) // 2].save(output / "preview.png")
    with Image.open(output / "directional-delay.gif") as movie:
        assert movie.n_frames == len(images)
        for index in range(movie.n_frames):
            movie.seek(index)
            movie.load()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).parent
    raw = json.loads((here / "initial.json").read_text())
    control = deepcopy(raw)
    control.pop("directional_delay")
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        frames, active = record(raw, args.output / "active")
        reference, baseline = record(control, args.output / "control")
        (args.output / "summary.json").write_text(
            json.dumps({"active": active, "control": baseline, "source": source_fingerprint()}, indent=2)
        )
        render((frames, reference), json.loads((here / "display.json").read_text()), args.output)
        print(json.dumps({"active": active, "control": baseline}))


if __name__ == "__main__":
    main()
