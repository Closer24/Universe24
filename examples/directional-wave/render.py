"""Render requested GIFs from canonical recordings; never execute field updates."""

import argparse
import copy
import json
import math
from pathlib import Path

from observe import measure
from PIL import Image, ImageDraw, ImageFont
from verify import checked_proof, load_recording

from event_universe.retention import ArtifactLease, validate_output_path

HERE = Path(__file__).resolve().parent


def font(size, bold=False):
    for name in ["DejaVuSans-Bold.ttf", "arialbd.ttf"] if bold else ["DejaVuSans.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def render(paths, target, display_path=HERE / "display.json"):
    validate_output_path(target)
    if target.exists():
        raise ValueError("use a new render output directory")
    target.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(target.parent, [target.resolve()]):
        return _render(paths, target, display_path)


def _render(paths, target, display_path):
    options = json.loads(display_path.read_text(encoding="utf-8"))
    definition = json.loads((HERE / "definition.json").read_text(encoding="utf-8"))
    data = [load_recording(path) for path in paths]
    if len(data) != 2:
        raise ValueError("supply a free reference followed by an interacting recording")
    proofs = [checked_proof(path) for path in paths]
    inputs = [
        json.loads((path.parent / "initialization.json").read_text(encoding="utf-8")) for path in paths
    ]
    law = json.loads((HERE / "law.json").read_text(encoding="utf-8"))
    if inputs[1]["model_id"] != definition["model_id"] or any(
        inputs[1][key] != law[key] for key in ("fields", "spatial_fields", "field_rules")
    ):
        raise ValueError("interacting input does not match the saved candidate law")
    expected_reference = copy.deepcopy(inputs[1])
    expected_reference["model_id"] += "-free"
    expected_reference["field_rules"] = [
        r for r in expected_reference["field_rules"] if r["name"] not in definition["collision_rules"]
    ]
    if inputs[0] != expected_reference:
        raise ValueError("reference input must differ only by disabling the configured encounters")
    ticks = [frame["tick"] for frame in data[0]["frames"]]
    if any([f["tick"] for f in item["frames"]] != ticks for item in data):
        raise ValueError("comparison recordings must use the same sampled ticks")
    if data[0]["metadata"]["source_sha256"] != data[1]["metadata"]["source_sha256"]:
        raise ValueError("comparison recordings must use the same simulator source")
    if data[0]["frames"][0] != data[1]["frames"][0]:
        raise ValueError("comparison recordings must have identical initial state")
    measured = [[measure(frame, definition["channels"]) for frame in item["frames"]] for item in data]
    for series in measured:
        expected = (series[0]["energy"], series[0]["momentum"])
        if any((f["energy"], f["momentum"]) != expected for f in series):
            raise ValueError("recorded candidate energy or momentum changed")
    width, height = options["width"], options["height"]
    images, durations = [], []
    text, small, title = font(19), font(16), font(25, True)
    panel_height = (height - 166) // 2
    for frame_index, tick in enumerate(ticks):
        canvas = Image.new("RGB", (width, height), "#091425")
        draw = ImageDraw.Draw(canvas)
        draw.text((22, 18), "A CONSERVATIVE FIELD ENCOUNTER", font=title, fill="#f4f7fe")
        draw.text(
            (22, 57),
            f"Recorded tick {tick} / {ticks[-1]}  |  same initial state",
            font=text,
            fill="#b8cde6",
        )
        collision_nearby = False
        for panel, item in enumerate(data):
            y0 = 96 + panel * (panel_height + 12)
            bottom = y0 + panel_height
            draw.rounded_rectangle((14, y0, width - 14, bottom), radius=15, fill="#14253c")
            label = "FREE PROPAGATION" if panel == 0 else "POLARIZATION INTERACTION"
            draw.text((30, y0 + 13), label, font=font(21, True), fill="#e5efff")
            n = item["metadata"]["shape"][0]
            if item["metadata"]["shape"] != [n, n, n]:
                raise ValueError("the example camera requires a cubic domain")
            angle = options["camera_yaw"] + options["camera_wobble"] * math.sin(tick * 0.17)
            ca, sa = math.cos(angle), math.sin(angle)
            scale = min((width - 190) / (1.55 * (n - 1)), (panel_height - 104) / (1.32 * (n - 1)))

            def project(position, n=n, scale=scale, ca=ca, sa=sa, y0=y0):
                x, y, z = [v - (n - 1) / 2 for v in position]
                return (
                    width / 2 + scale * (ca * x - sa * y),
                    y0 + (panel_height - 14) / 2 + scale * (0.45 * (sa * x + ca * y) - 0.6 * z),
                )

            def arrow(position, vector, color, factor=1, thickness=3, project=project, draw=draw):
                if not any(vector):
                    return
                start = project(position)
                end = project([position[i] + factor * vector[i] for i in range(3)])
                dx, dy = end[0] - start[0], end[1] - start[1]
                length = math.hypot(dx, dy)
                if length < 1:
                    return
                ux, uy = dx / length, dy / length
                draw.line((start, end), fill=color, width=thickness)
                head = min(7, length * 0.4)
                draw.polygon(
                    (
                        end,
                        (end[0] - head * ux + 3 * uy, end[1] - head * uy - 3 * ux),
                        (end[0] - head * ux - 3 * uy, end[1] - head * uy + 3 * ux),
                    ),
                    fill=color,
                )

            if options["show_nodes"]:
                for x in range(n):
                    for y in range(n):
                        for z in range(n):
                            u, v = project((x, y, z))
                            draw.ellipse((u - 1, v - 1, u + 1, v + 1), fill="#506681")
            for axis in range(3):
                others = [i for i in range(3) if i != axis]
                for a in (0, n - 1):
                    for b in (0, n - 1):
                        p = [0, 0, 0]
                        p[others[0]], p[others[1]] = a, b
                        q = p.copy()
                        q[axis] = n - 1
                        draw.line((project(p), project(q)), fill="#35516c", width=1)
            if options["show_axes"]:
                for axis, color in enumerate(("#fb9291", "#89d9a2", "#84b7fb")):
                    vector = [0, 0, 0]
                    vector[axis] = n - 1
                    arrow((0, 0, 0), vector, color, thickness=2)
                    x, y = project(vector)
                    draw.text((x + 4, y - 9), "XYZ"[axis], font=small, fill=color)
            state = measured[panel][frame_index]
            glyphs = list(state["nodes"])
            for packet in state["transfers"]:
                link_ticks = item["metadata"]["link_ticks"]
                progress = (tick - packet["arrival_tick"] + link_ticks) / link_ticks
                direction = packet["modes"][0]["direction"]
                position = [(packet["origin"][i] + progress * direction[i]) % n for i in range(3)]
                glyphs.append(dict(packet, position=position, in_transit=True))
            for node in glyphs:
                position = node["position"]
                x, y = project(position)
                draw.ellipse(
                    (x - 5, y - 5, x + 5, y + 5),
                    fill=None if node.get("in_transit") else "#ffd18d",
                    outline="#ffd18d",
                    width=2,
                )
                if options["show_modes"]:
                    for mode in node["modes"]:
                        arrow(position, mode["amplitude"], "#e0b365", options["vector_scale"], 1)
                if options["show_electric"]:
                    arrow(position, node["electric"], "#59e6ed", options["vector_scale"], 4)
                if options["show_magnetic"]:
                    arrow(position, node["magnetic"], "#c493ff", options["vector_scale"], 4)
                if options["show_travel"]:
                    for mode in node["modes"]:
                        arrow(position, mode["direction"], "#eff4fa", 0.85, 2)
                multiple = len(node["modes"]) > 1
                collision_nearby |= multiple
                draw.text(
                    (x + 10, y + 6),
                    "in transit"
                    if node.get("in_transit")
                    else "overlap"
                    if multiple
                    else str(node["energy"]),
                    font=small,
                    fill="#ffdaa1",
                )
            momentum = ",".join(f"{v:+d}" for v in state["momentum"])
            draw.text(
                (30, bottom - 47),
                f"Energy {state['energy']}    Momentum ({momentum})",
                font=text,
                fill="#97dfbd",
            )
            draw.text(
                (30, bottom - 24),
                "Conservation errors: 0   |   opposite faces connect",
                font=small,
                fill="#b9cde1",
            )
        draw.text(
            (22, height - 43),
            "E cyan | B violet | travel white | modes amber",
            font=small,
            fill="#c6d6e9",
        )
        draw.text(
            (22, height - 23),
            "Normalized directional-wave candidate; Maxwell dynamics not established.",
            font=font(14),
            fill="#9cacc3",
        )
        images.append(canvas)
        durations.append(
            options["encounter_ms"]
            if collision_nearby or frame_index in (0, len(ticks) - 1)
            else options["frame_ms"]
        )
    gif_path = target / "directional-wave.gif"
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=True,
    )
    with Image.open(gif_path) as gif:
        if gif.n_frames != len(ticks):
            raise ValueError("GIF frame count changed")
        decoded_duration = 0
        for i in range(gif.n_frames):
            gif.seek(i)
            gif.load()
            decoded_duration += gif.info.get("duration", 0)
            if i in (0, 1, 2, len(ticks) - 1):
                gif.convert("RGB").save(target / f"frame-{i:02d}.png")
        if decoded_duration != sum(durations):
            raise ValueError("GIF timing changed")
    proof = {
        "source_sha256": data[0]["metadata"]["source_sha256"],
        "frames": len(ticks),
        "duration_ms": sum(durations),
        "size_bytes": gif_path.stat().st_size,
        "energy_error_max": 0,
        "momentum_error_max": 0,
        "recorded_readouts": measured,
        "recording_proofs": proofs,
    }
    (target / "verification.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    return gif_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--recording", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--display", type=Path, default=HERE / "display.json")
    args = parser.parse_args()
    print(render([args.reference, args.recording], args.output, args.display))


if __name__ == "__main__":
    main()
