"""Render actual recorded ray positions, carried headings and phases.

This module never imports the simulator. All projected floats are display only.
It draws no orbit, interpolated path, hidden particle or inferred frequency.
"""

import argparse
import hashlib
import json
from pathlib import Path


def render_recording(source, output, *, duration_ms=300):
    from PIL import Image, ImageDraw, ImageFont

    recording = json.loads(source.read_text(encoding="utf-8"))
    frames = recording["frames"]
    if not frames or duration_ms < 1:
        raise ValueError("Recorded frames and a positive duration are required")
    ticks = [frame["tick"] for frame in frames]
    if ticks != sorted(set(ticks)):
        raise ValueError("Recorded ticks must be strictly increasing")
    positions = [
        ray["position"] if ray["owner"] == "node" else ray["origin"]
        for frame in frames
        for ray in frame["rays"]
    ]
    if not positions:
        raise ValueError("No actual rays are present in this recording")
    low = [min(p[i] for p in positions) - 1 for i in range(3)]
    high = [max(p[i] for p in positions) + 1 for i in range(3)]
    center = [(a + b) / 2 for a, b in zip(low, high, strict=True)]
    scale = min(54, 390 / max(b - a for a, b in zip(low, high, strict=True)))

    def project(position):
        x, y, z = (p - c for p, c in zip(position, center, strict=True))
        return 360 + scale * (x - 0.50 * y), 350 + scale * (0.25 * x + 0.42 * y - z)

    try:
        title = ImageFont.truetype("DejaVuSans.ttf", 24)
        normal = ImageFont.truetype("DejaVuSans.ttf", 17)
        small = ImageFont.truetype("DejaVuSans.ttf", 14)
    except OSError:
        title = normal = small = ImageFont.load_default()
    images = []
    for frame in frames:
        image = Image.new("RGB", (1120, 680), "#0c1626")
        draw = ImageDraw.Draw(image)
        draw.text((25, 20), "Universe24 | recorded ray coupling", font=title, fill="#f3f6ff")
        draw.text((25, 57), recording["model"], font=small, fill="#b7c7df")
        draw.text((25, 84), f"Actual world tick {frame['tick']}", font=normal, fill="#eff4ff")
        draw.text(
            (25, 113),
            "Finite residence and release; no stable nucleus claim",
            font=normal,
            fill="#f9bb76",
        )
        for x in range(low[0], high[0] + 1):
            for y in range(low[1], high[1] + 1):
                px, py = project((x, y, round(center[2])))
                draw.ellipse((px - 2, py - 2, px + 2, py + 2), fill="#33435d")
        for axis, color in enumerate(("#f79a78", "#77dab3", "#99b2ff")):
            end = list(center)
            end[axis] += 2
            draw.line((project(center), project(end)), fill=color, width=2)
            draw.text(project(end), "+" + "XYZ"[axis], font=normal, fill=color)
        rows = []
        for index, ray in enumerate(frame["rays"]):
            data = ray["ray"]
            phase = data["phase"]
            palette = (
                "#79bfff",
                "#a28fff",
                "#e998de",
                "#ffac82",
                "#ffd885",
                "#a8d994",
                "#71d8bc",
                "#79cce8",
            )
            color = palette[phase % len(palette)]
            position = ray.get("position")
            if ray["owner"] == "link":
                origin, target = ray["origin"], ray["target"]
                if target is None:
                    position = origin
                else:
                    draw.line((project(origin), project(target)), fill="#4c6487", width=3)
                    position = [(a + b) / 2 for a, b in zip(origin, target, strict=True)]
            px, py = project(position)
            # Concentric circles show colocated records without inventing locations.
            radius = 7 + 3 * (index % 3)
            draw.ellipse((px - radius, py - radius, px + radius, py + radius), outline=color, width=3)
            heading = ray["heading_vector"]
            divisor = max(abs(value) for value in heading)
            end = [p + h / divisor for p, h in zip(position, heading, strict=True)]
            draw.line(((px, py), project(end)), fill=color, width=2)
            rows.append(
                f"{ray['owner']} {ray['field']}: amount={data['amount']} "
                f"phase={phase} delay={data.get('interaction_delay', 0)}"
            )
            rows.append(f"  heading={heading} DDA={data['accumulators']}")
        draw.text((670, 176), "Actual owners and carried registers", font=normal, fill="#e3ecff")
        for i, row in enumerate(rows[:18]):
            draw.text((670, 212 + i * 20), row, font=small, fill="#bfd0e8")
        if not rows:
            draw.text((670, 212), "No rays remain in the world", font=normal, fill="#bfd0e8")
        draw.text(
            (25, 589),
            "Node centers are actual locations. Link midpoints are display markers only.",
            font=small,
            fill="#a5b7d2",
        )
        draw.text(
            (25, 612),
            "Arrow = carried heading. Ring color = recorded phase. No interpolated trajectory.",
            font=small,
            fill="#a5b7d2",
        )
        draw.text(
            (25, 635),
            "One playback only; the animation does not define a physical recurrence period.",
            font=small,
            fill="#a5b7d2",
        )
        images.append(image)
    output.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(output, save_all=True, append_images=images[1:], duration=duration_ms, optimize=False)
    manifest = {
        "model": recording["model"],
        "source_sha256": recording["source_sha256"],
        "recording_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "selected_ticks": ticks,
        "interpolated": False,
        "loop": False,
        "physical_frequency": "not inferred",
    }
    output.with_suffix(".json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recording", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(render_recording(args.recording, args.output), indent=2))


if __name__ == "__main__":
    main()
