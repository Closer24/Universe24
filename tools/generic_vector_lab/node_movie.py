"""Record a real node transaction; render its momentum states, not invented paths."""

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .run_demo import encode, ledger
from .runtime import Lab

ROOT = Path(__file__).parent


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/generic-vector-lab"))
    output = parser.parse_args().output
    output.mkdir(parents=True, exist_ok=True)
    definitions = json.loads((ROOT / "definitions.json").read_text(encoding="utf-8"))
    engine = Lab(definitions)
    demo = definitions["node_demo"]
    ids = [engine.insert(0, engine.record(p["type"], p["fields"])) for p in demo["participants"]]

    def snapshot(tick):
        return {
            "tick": tick,
            "ledger": ledger(engine),
            "records": [
                {
                    "id": identifier,
                    "type": record.kind,
                    "p": encode(engine.context(record)["p"]),
                }
                for identifier, record in engine.cells[0]
            ],
        }

    states = [snapshot(0)]
    engine.react(0, demo["rule"], ids)
    states.append(snapshot(1))
    assert states[0]["ledger"] == states[1]["ledger"]
    (output / "node-states.json").write_text(json.dumps(states, indent=2) + "\n", encoding="utf-8")
    render(demo["view"], output)


def render(view, output):
    # Rendering reads the saved physical snapshots; no reaction formulas here.
    states = json.loads((output / "node-states.json").read_text(encoding="utf-8"))
    size, count = view["size"], view["frames_per_state"]
    colors = view["colors"]
    kinds = list(dict.fromkeys(r["type"] for r in states[0]["records"]))
    font_path = Path("C:/Windows/Fonts/arial.ttf")

    def font(n):
        return (
            ImageFont.truetype(str(font_path), n)
            if font_path.exists()
            else ImageFont.load_default(size=n)
        )

    title, normal, small = font(27), font(20), font(17)
    images = []
    for frame in range(count * len(states)):
        state = states[frame // count]
        angle = 0.48 + 0.22 * math.sin(2 * math.pi * frame / (count * len(states)))

        def project(point, angle=angle):
            x, y, z = point
            a = math.cos(angle) * x - math.sin(angle) * y
            b = math.sin(angle) * x + math.cos(angle) * y
            return (size / 2 + 135 * a, 340 + 65 * b - 125 * z)

        im = Image.new("RGB", (size, size), "#101827")
        draw = ImageDraw.Draw(im)
        draw.text((24, 20), "6 disturbances / one node", font=title, fill="white")
        draw.text(
            (24, 62),
            "BEFORE" if state["tick"] == 0 else "AFTER: one atomic reaction",
            font=normal,
            fill="#73e3bb",
        )
        draw.text((24, 93), "Momentum vectors | no contact normal", font=small, fill="#b9c6dc")
        for k in range(-2, 3):
            draw.line([project((k, -2, 0)), project((k, 2, 0))], fill="#2c384f", width=1)
            draw.line([project((-2, k, 0)), project((2, k, 0))], fill="#2c384f", width=1)
        center = project((0, 0, 0))
        for axis, label in [
            ((1.65, 0, 0), "X"),
            ((0, 1.65, 0), "Y"),
            ((0, 0, 1.6), "Z"),
        ]:
            end = project(axis)
            draw.line([center, end], fill="#536078", width=1)
            draw.text(end, label, font=small, fill="#7888a2")
        for record in state["records"]:
            momentum = []
            for payload in record["p"]["payload"]:
                code = payload["code"]
                numerator = code // 2 if code % 2 else -(code // 2)
                momentum.append(numerator / payload["denominator"])
            end = project(momentum)
            color = colors[kinds.index(record["type"])]
            draw.line([center, end], fill=color, width=5)
            dx, dy = end[0] - center[0], end[1] - center[1]
            length = math.hypot(dx, dy)
            ux, uy = dx / length, dy / length
            draw.polygon(
                [
                    end,
                    (end[0] - 14 * ux + 6 * uy, end[1] - 14 * uy - 6 * ux),
                    (end[0] - 14 * ux - 6 * uy, end[1] - 14 * uy + 6 * ux),
                ],
                fill=color,
            )
            draw.text((end[0] + 8, end[1] - 10), record["type"][-1], font=normal, fill=color)
        draw.ellipse((center[0] - 7, center[1] - 7, center[0] + 7, center[1] + 7), fill="white")
        draw.text((24, 522), "A: 2      B: 2      C: 2", font=normal, fill="white")
        totals = state["ledger"]
        draw.text(
            (24, 555),
            "Energy "
            + totals["E"]["values"][0]
            + "    Momentum ("
            + ", ".join(totals["p"]["values"])
            + ")",
            font=normal,
            fill="#73e3bb",
        )
        draw.text(
            (24, 589),
            f"Recorded state {state['tick']} | exact balance preserved",
            font=small,
            fill="#b9c6dc",
        )
        images.append(im)
    path = output / "six-node.gif"
    images[0].save(
        path,
        save_all=True,
        append_images=images[1:],
        duration=view["duration_ms"],
        loop=0,
        disposal=2,
    )
    with Image.open(path) as decoded:
        assert decoded.n_frames == len(images)
        for i in [0, count, len(images) - 1]:
            decoded.seek(i)
            decoded.convert("RGB").save(output / f"node-preview-{i}.png")
    provenance = {
        "frames": len(images),
        "duration_ms": len(images) * view["duration_ms"],
        "rendering": "Two recorded node states; only the viewing angle moves between state changes. No interpolated physical trajectories.",
        "definitions_sha256": hashlib.sha256((ROOT / "definitions.json").read_bytes()).hexdigest(),
        "states_sha256": hashlib.sha256((output / "node-states.json").read_bytes()).hexdigest(),
        "gif_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
    }
    (output / "node-provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    run()
