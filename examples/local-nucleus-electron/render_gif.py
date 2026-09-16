"""Render a GIF from canonical recorded Node/Link states without running a world.

Only the optional display dependency Pillow is required. This read-only tool
can use the primary graphics runtime independently of the simulation interpreter.
All floating-point values below are display projections, never physical inputs.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path

COLORS = ("#ef9765", "#b8c5d4", "#75b7ff")


def read_recording(path):
    text = path.read_text(encoding="utf-8")
    start = text.find('{"frames"')
    if start < 0:
        raise ValueError("Expected canonical HTML containing recorded frames")
    recording, _ = json.JSONDecoder().raw_decode(text[start:])
    if not recording["frames"]:
        raise ValueError("A recorded frame is required")
    return recording


def record_owners(frame, names):
    """Each actual record owner occurs once; Link midpoint is a labeled glyph only."""
    owners = []
    for node in frame["nodes"]:
        for bank in ("disturbances", "held_outputs"):
            for record in node.get(bank, []):
                if record["type"] in names:
                    owners.append({**record, "position": node["position"], "owner": bank})
    for record in frame.get("transfers", []):
        if record["type"] in names:
            if record.get("target") is None:
                raise ValueError("Cannot display a transfer without a recorded neighboring target")
            owners.append(
                {
                    **record,
                    "position": [
                        (a + b) / 2 for a, b in zip(record["origin"], record["target"], strict=True)
                    ],
                    "owner": "link",
                }
            )
    return owners


def projection(position, center, scale):
    x, y, z = (a - b for a, b in zip(position, center, strict=True))
    return 475 + scale * (0.84 * x - 0.55 * y), 365 + scale * (0.32 * x + 0.48 * y - z)


def render_recording(html_path, output, *, electron, nucleons, stride=1, duration_ms=140):
    from PIL import Image, ImageDraw, ImageFont

    if stride < 1 or duration_ms < 1:
        raise ValueError("Frame stride and playback duration must be positive")
    recording = read_recording(html_path)
    frames = recording["frames"]
    metadata = recording["metadata"]
    names = (*nucleons, electron)
    owners = [record_owners(frame, names) for frame in frames]
    if not any(record["type"] == electron for rows in owners for record in rows):
        raise ValueError("Requested electron record is absent; no particle is invented")
    initial_nuclear = [r for r in owners[0] if r["type"] in nucleons]
    center = initial_nuclear[0]["position"] if initial_nuclear else owners[0][0]["position"]
    positions = [r["position"] for rows in owners for r in rows]
    extent = max(4, max(abs(p[i] - center[i]) for p in positions for i in range(3)) + 2)
    scale = min(43, 250 / extent)

    def project(position):
        return projection(position, center, scale)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 18)
        small = ImageFont.truetype("DejaVuSans.ttf", 14)
        title_font = ImageFont.truetype("DejaVuSans.ttf", 23)
    except OSError:
        font = small = title_font = ImageFont.load_default()
    selected = list(range(0, len(frames), stride))
    if selected[-1] != len(frames) - 1:
        selected.append(len(frames) - 1)
    images = []
    trail = []
    next_frame = 0
    for index in selected:
        while next_frame <= index:
            for record in owners[next_frame]:
                if record["type"] == electron and record["owner"] != "link":
                    position = tuple(record["position"])
                    if not trail or trail[-1] != position:
                        trail.append(position)
            next_frame += 1
        image = Image.new("RGB", (1040, 740), "#101a2a")
        draw = ImageDraw.Draw(image)
        draw.text(
            (28, 18),
            "Universe24 | recorded local nucleus / electron state",
            font=title_font,
            fill="#f4f6fa",
        )
        draw.text(
            (28, 55),
            str(metadata.get("model", "unnamed recorded model"))[:110],
            font=small,
            fill="#b9c7dc",
        )
        draw.text(
            (28, 81),
            f"Model tick {frames[index]['tick']} | saved frame {index + 1}/{len(frames)} | field hidden",
            font=font,
            fill="#e3edff",
        )
        # A grid slice and the three coordinate axes are read-only geometry.
        bound = math.ceil(extent)
        for coordinate in range(-bound, bound + 1):
            for axis in (0, 1):
                start, end = list(center), list(center)
                start[axis] += coordinate
                end[axis] += coordinate
                start[1 - axis] -= bound
                end[1 - axis] += bound
                draw.line((project(start), project(end)), fill="#233047", width=1)
        for axis, color in enumerate(("#ef9765", "#77d4aa", "#8faaff")):
            end = list(center)
            end[axis] += min(5, bound)
            draw.line((project(center), project(end)), fill=color, width=2)
            draw.text(project(end), "+" + "XYZ"[axis], font=font, fill=color)
        for previous, position in zip(trail, trail[1:], strict=False):
            if sum(abs(a - b) for a, b in zip(previous, position, strict=True)) == 1:
                draw.line((project(previous), project(position)), fill="#4b81b7", width=2)
        for position in trail:
            x, y = project(position)
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill="#6098ce")
        current = owners[index]
        nuclear = [r for r in current if r["type"] in nucleons]
        grouped = {}
        for record in nuclear:
            grouped.setdefault(tuple(record["position"]), []).append(record)
        for position, records in grouped.items():
            # Both glyphs appear inside the one actual occupied Node cube.
            corners = [
                [position[0] + dx, position[1] + dy, position[2] + dz]
                for dx in (-0.5, 0.5)
                for dy in (-0.5, 0.5)
                for dz in (-0.5, 0.5)
            ]
            for i, first in enumerate(corners):
                for second in corners[i + 1 :]:
                    if sum(a != b for a, b in zip(first, second, strict=True)) == 1:
                        draw.line((project(first), project(second)), fill="#debd87", width=2)
            for offset, record in enumerate(records):
                x, y = project(position)
                x += (offset - (len(records) - 1) / 2) * min(10, scale / 3)
                color = COLORS[nucleons.index(record["type"]) % 2]
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
                draw.text((x - 8, y - 26 - 17 * offset), record["type"], font=small, fill=color)
        electrons = [r for r in current if r["type"] == electron]
        if electrons:
            draw.text(
                (28, 112),
                "Recorded electron momentum: " + str(electrons[0]["values"].get("momentum")),
                font=small,
                fill=COLORS[2],
            )
        else:
            draw.text(
                (28, 112), "Electron absent from this saved world state", font=small, fill=COLORS[2]
            )
        for record in electrons:
            x, y = project(record["position"])
            draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=COLORS[2])
            draw.text(
                (x + 10, y - 18),
                "electron" + (" [Link]" if record["owner"] == "link" else ""),
                font=small,
                fill=COLORS[2],
            )
            momentum = record["values"].get("momentum")
            if momentum is not None and any(momentum):
                norm = math.sqrt(sum(value * value for value in momentum))
                end = [p + 1.5 * q / norm for p, q in zip(record["position"], momentum, strict=True)]
                ex, ey = project(end)
                draw.line(((x, y), (ex, ey)), fill="#e9f3ff", width=3)
                draw.ellipse((ex - 2, ey - 2, ex + 2, ey + 2), fill="#e9f3ff")
        if electrons and nuclear and electrons[0]["owner"] != "link":
            r2 = sum(
                (a - b) ** 2
                for a, b in zip(electrons[0]["position"], nuclear[0]["position"], strict=True)
            )
            detail = f"Distance to first nuclear record: sqrt({r2}) = {math.sqrt(r2):.3f} Nodes"
        else:
            detail = "Distance unavailable at this frame: electron in transit or record absent"
        draw.text((28, 611), detail, font=font, fill="#e4ecf8")
        draw.text(
            (28, 641),
            "Trail dots are recorded Node positions; lines only join observed neighboring Nodes.",
            font=small,
            fill="#b9c7dc",
        )
        draw.text(
            (28, 662),
            "Glyph offsets and Link midpoints are display only. Fixed-length arrow shows recorded momentum direction.",
            font=small,
            fill="#b9c7dc",
        )
        draw.text(
            (28, 684),
            "No interpolated motion. Playback loops are not physical recurrence; no orbital period is inferred.",
            font=small,
            fill="#b9c7dc",
        )
        images.append(image)
    output.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        output, save_all=True, append_images=images[1:], duration=duration_ms, loop=0, optimize=True
    )
    manifest = {
        "html": str(html_path.resolve()),
        "html_sha256": hashlib.sha256(html_path.read_bytes()).hexdigest(),
        "source_sha256": metadata.get("source_sha256"),
        "renderer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "model": metadata.get("model"),
        "gif": str(output.resolve()),
        "selected_ticks": [frames[i]["tick"] for i in selected],
        "interpolated": False,
        "electron": electron,
        "requested_nucleons": list(nucleons),
        "present_named_records": sorted({r["type"] for rows in owners for r in rows}),
        "period": "not inferred by renderer",
        "playback_frame_ms": duration_ms,
    }
    output.with_suffix(".json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--electron", required=True)
    parser.add_argument("--nucleons", nargs="*", default=[])
    parser.add_argument("--stride", type=int, default=1)
    args = parser.parse_args()
    print(
        json.dumps(
            render_recording(
                args.html,
                args.output,
                electron=args.electron,
                nucleons=args.nucleons,
                stride=args.stride,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
