"""Encode native Presenter state images as a GIF; never synthesize board states.

python -m research.staged_blocks.animation --report SMOKE/report.json --output NEW_DIR
Pillow is an optional presentation dependency, separate from the engine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from research.experiments.run import write_json


def encode(report_path, output, *, milliseconds=250):
    from PIL import Image
    import PIL

    report_path, output = Path(report_path), Path(output)
    if type(milliseconds) is not int or milliseconds < 20 or milliseconds % 10:
        raise ValueError("GIF frame duration must be a multiple of 10 milliseconds, at least 20")
    if output.exists():
        raise FileExistsError("Refusing to overwrite " + str(output))
    report = json.loads(report_path.read_text())
    if report.get("passed") is not True:
        raise ValueError("The complete recording/Presenter smoke must pass first")
    animations = [a for bundle in report["bundles"] for a in bundle.get("animations", [])]
    if not animations:
        raise ValueError("The smoke report contains no recorded animation frames")
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for animation in animations:
        images = []
        for index, frame in enumerate(animation["frames"]):
            if frame["frame"] != index:
                raise ValueError("Animation must retain every consecutive recorded frame")
            path = report_path.parent / frame["file"]
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != frame["png_sha256"]:
                raise ValueError("A rendered native frame changed after smoke verification")
            with Image.open(path) as image:
                images.append(image.convert("RGB"))
        destination = output / (animation["name"] + ".gif")
        images[0].save(destination, save_all=True, append_images=images[1:],
                       duration=milliseconds, loop=0, disposal=2, optimize=False)
        with Image.open(destination) as decoded:
            count = decoded.n_frames
            durations = []
            for index in range(count):
                decoded.seek(index)
                durations.append(decoded.info.get("duration"))
        if count != len(images) or durations != [milliseconds] * count:
            raise ValueError("GIF encoding did not retain every recorded frame and duration")
        results.append({"experiment": animation["experiment"], "file": destination.name,
                        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                        "frames": animation["frames"], "milliseconds_per_frame": milliseconds,
                        "replay_loop": True, "interpolated_states": False,
                        "scope": animation["scope"]})
    result = {"format": "universe24-staged-recorded-animation-v1",
              "smoke_report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
              "encoder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "pillow_version": PIL.__version__, "animations": results}
    write_json(output / "manifest.json", result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--milliseconds", type=int, default=250)
    args = parser.parse_args(argv)
    result = encode(args.report, args.output, milliseconds=args.milliseconds)
    print(json.dumps({"animations": [{"file": a["file"], "frames": len(a["frames"])}
                                     for a in result["animations"]]}, indent=2))


if __name__ == "__main__":
    main()
