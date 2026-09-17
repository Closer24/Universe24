"""Render a GIF and a contact sheet from ``runs.json`` with the viewer page.

Playwright drives headless Chromium over a copy of ``viewer.html`` with the
runs document and the style (``--style``, default ``style.json`` beside this
script) inlined. The page loads Three.js r128 from cdnjs; here that request is
answered from a local copy of the same file through a route, so the capture
needs no network, and every other request is blocked. The camera azimuth
advances ``--step`` degrees per frame while the tick runs 0..ticks and then
holds the final state for ``--hold`` frames; the runs are stacked vertically
in each frame. Pillow assembles the GIF with one shared palette and writes a
contact sheet of evenly spaced frames. Every default below comes from the
style's ``motion`` block, so a change of look is a file edit and a re-render.

The result is a rendering of a fingerprinted record, not evidence by itself.

Run:  python tools/ray_viewer/render_gif.py runs.json --output electron.gif
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any

from PIL import Image
from playwright.sync_api import Route, sync_playwright

HERE = Path(__file__).resolve().parent
THREE_URL = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
# SHA-256 of the r128 UMD build served on 2026-09-17; a differing copy is refused.
THREE_SHA256 = "9274bbcec8d96168626c732b5d31c775aa8cfb7eaa0599bec0c175908a2c1ce2"
GUTTER = 16  # the page's side padding, so the capture element is viewport - 2 * GUTTER wide
DATA_TAG = '<script type="application/json" id="runs-data"></script>'
STYLE_TAG = '<script type="application/json" id="style"></script>'
STYLE_FILE = HERE / "style.json"
STYLE_KEYS = {
    "colors": (
        "background",
        "surface",
        "scene",
        "ink",
        "muted",
        "line",
        "accent",
        "lattice",
        "box",
        "families",
        "markers",
        "source",
        "detector",
        "external_body",
    ),
    "sizes": (
        "ray_width_px",
        "arrowhead_px",
        "trail_links",
        "trail_width_px",
        "trail_fade",
        "field_width_px",
        "field_trail_links",
        "field_arrowhead",
        "marker_radius",
        "escape_dot_radius",
        "source_size",
        "detector_size",
        "body_size",
        "label_font_px",
        "label_min_distance_px",
        "node_dot_px",
        "lattice_alpha",
        "box_alpha",
    ),
    "draw": (
        "markers",
        "marker_shapes",
        "labels",
        "label_text",
        "escapes",
        "sources",
        "detectors",
        "external_bodies",
        "apparatus",
        "trails",
        "hue_by_phase",
        "silent_field_events",
        "page_text",
    ),
    "caption": (
        "kinds",
        "max_per_tick",
        "more",
        "emissions",
        "escapes",
        "field_escapes",
        "empty",
        "totals",
        "conservation",
    ),
    "motion": (
        "rotation_seconds_per_turn",
        "autoplay",
        "loop",
        "page_ticks_per_second",
        "gif_degrees_per_frame",
        "gif_frames",
        "gif_hold_frames",
        "gif_width_px",
        "gif_frame_ms",
        "gif_colors",
        "contact_stills",
        "elevation_deg",
        "start_angle_deg",
    ),
}
CHROMIUM_ARGS = [
    "--use-angle=swiftshader",
    "--enable-unsafe-swiftshader",
    "--ignore-gpu-blocklist",
    "--hide-scrollbars",
]


def three_js(explicit: Path | None) -> Path:
    """The local Three.js copy: an explicit path, a cached file, or one download."""
    candidates = [explicit] if explicit else []
    cache = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "ray_viewer"
    candidates += [HERE / "three.r128.min.js", cache / "three.r128.min.js"]
    for path in candidates:
        if path is not None and path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != THREE_SHA256:
                raise ValueError(f"{path} is not the pinned Three.js r128 build (sha256 {digest})")
            return path
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / "three.r128.min.js"
    try:
        with urllib.request.urlopen(THREE_URL, timeout=30) as response:  # noqa: S310
            content = response.read()
    except OSError as error:
        raise ValueError(
            f"no local Three.js r128 copy and the download failed ({error}); pass --three PATH"
        ) from error
    digest = hashlib.sha256(content).hexdigest()
    if digest != THREE_SHA256:
        raise ValueError(f"downloaded Three.js has sha256 {digest}, not the pinned build")
    target.write_bytes(content)
    return target


def load_style(path: Path | None) -> dict[str, Any]:
    """The style file, checked against the documented keys (``ray-viewer-style-v1``)."""
    style = json.loads((path or STYLE_FILE).read_text(encoding="utf-8"))
    return validate_style(style)


def validate_style(style: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(style, dict) or style.get("schema") != "ray-viewer-style-v1":
        raise ValueError("a style must be a ray-viewer-style-v1 object")
    unknown = set(style) - set(STYLE_KEYS) - {"schema"}
    if unknown:
        raise ValueError(f"unknown style sections {sorted(unknown)}")
    for section, keys in STYLE_KEYS.items():
        block = style.get(section, {})
        if not isinstance(block, dict):
            raise ValueError(f"style section {section} must be an object")
        extra = set(block) - set(keys)
        if extra:
            raise ValueError(f"unknown keys in style.{section}: {sorted(extra)}")
    return style


def inline_json(page: str, tag: str, document: dict[str, Any]) -> str:
    if page.count(tag) != 1:
        raise ValueError(f"viewer.html must hold {tag} exactly once")
    payload = json.dumps(document, separators=(",", ":")).replace("</", "<\\/")
    return page.replace(tag, tag.replace("></script>", ">" + payload + "</script>"))


def inline_page(runs: dict[str, Any], style: dict[str, Any] | None = None) -> str:
    """The viewer page with the runs document and the style inlined; self-contained."""
    page = (HERE / "viewer.html").read_text(encoding="utf-8")
    page = inline_json(page, DATA_TAG, runs)
    if style is not None:
        page = inline_json(page, STYLE_TAG, style)
    return page


def stack(parts: list[Image.Image]) -> Image.Image:
    width = max(im.width for im in parts)
    height = sum(im.height for im in parts)
    frame = Image.new("RGB", (width, height), parts[0].getpixel((0, 0)))
    y = 0
    for im in parts:
        frame.paste(im, (0, y))
        y += im.height
    return frame


def pad_to_one_size(frames: list[Image.Image]) -> list[Image.Image]:
    """Every GIF frame shares one size; a shorter frame is padded with its ground color."""
    width, height = max(f.width for f in frames), max(f.height for f in frames)
    if all(f.size == (width, height) for f in frames):
        return frames
    padded = []
    for f in frames:
        canvas = Image.new("RGB", (width, height), f.getpixel((0, f.height - 1)))
        canvas.paste(f, (0, 0))
        padded.append(canvas)
    return padded


def quantize(frames: list[Image.Image], colors: int) -> list[Image.Image]:
    """One adaptive palette from a montage of sample frames, no dithering."""
    sample_ids = sorted({0, len(frames) // 4, len(frames) // 2, 3 * len(frames) // 4, len(frames) - 1})
    sample = frames[sample_ids[0]]
    montage = Image.new("RGB", (sample.width, sample.height * len(sample_ids)))
    for k, index in enumerate(sample_ids):
        montage.paste(frames[index], (0, k * sample.height))
    palette = montage.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]


def contact_sheet(
    frames: list[Image.Image], columns: int = 4, count: int = 16, width: int = 320
) -> Image.Image:
    ids = [round(i * (len(frames) - 1) / max(1, count - 1)) for i in range(min(count, len(frames)))]
    thumbs = [frames[i].resize((width, round(frames[i].height * width / frames[i].width))) for i in ids]
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * width, rows * thumbs[0].height), (0, 0, 0))
    for k, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((k % columns) * width, (k // columns) * thumb.height))
    return sheet


def capture_frames(
    page_html: str,
    run_keys: list[str],
    ticks: int,
    *,
    frames: int,
    step: float,
    start_angle: float,
    elevation: float,
    width: int,
    three: Path,
    work: Path,
) -> tuple[list[Image.Image], list[str], list[str]]:
    wrapped = (work / "viewer-inlined.html").resolve()
    wrapped.write_text(page_html, encoding="utf-8")
    blocked: set[str] = set()
    errors: list[str] = []

    def route(route: Route, request: Any) -> None:
        url = str(request.url)
        if url == THREE_URL:
            route.fulfill(path=str(three), content_type="application/javascript")
        elif url.startswith("file://"):
            route.continue_()
        else:
            blocked.add(url.split("?")[0])
            route.abort()

    images: list[Image.Image] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=CHROMIUM_ARGS)
        context = browser.new_context(
            viewport={"width": width + 2 * GUTTER, "height": 1400},
            device_scale_factor=1,
            color_scheme="dark",
            reduced_motion="no-preference",
        )
        page = context.new_page()
        page.route("**/*", route)
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(wrapped.as_uri())
        page.wait_for_function("window.__ready === true", timeout=30000)
        info = page.evaluate("() => window.__render(0, 0, null)")
        if not info.get("webgl"):
            raise RuntimeError("the page reports no WebGL renderer")
        capture = page.locator("#capture")
        for i in range(frames):
            tick = min(i, ticks)
            angle = start_angle + step * i
            parts = []
            for j, key in enumerate(run_keys):
                page.evaluate(
                    "([t, a, r, m, e]) => { window.__capture(m); window.__render(t, a, r, e); }",
                    [tick, angle, key, "first" if j == 0 else "second", elevation],
                )
                png = capture.screenshot(type="png")
                parts.append(Image.open(io.BytesIO(png)).convert("RGB"))
            images.append(stack(parts))
            print(f"frame {i:03d} tick {tick:03d} angle {angle:7.1f} size {images[-1].size}", flush=True)
        browser.close()
    return images, errors, sorted(blocked)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path, help="runs.json from extract.py")
    parser.add_argument("--output", type=Path, default=Path("ray-viewer.gif"))
    parser.add_argument("--contact-sheet", type=Path, help="default: the output name with -contact.png")
    parser.add_argument("--html", type=Path, help="also write the viewer page with the runs inlined")
    parser.add_argument("--style", type=Path, help="style file (default: style.json beside this script)")
    parser.add_argument("--frames", type=int, help="default: style gif_frames, else ticks + 1 + hold")
    parser.add_argument(
        "--hold", type=int, help="frames that hold the final tick (style gif_hold_frames)"
    )
    parser.add_argument("--step", type=float, help="camera azimuth per frame, degrees (style)")
    parser.add_argument("--start-angle", type=float, help="degrees (style start_angle_deg)")
    parser.add_argument("--elevation", type=float, help="degrees (style elevation_deg)")
    parser.add_argument("--width", type=int, help="pixels (style gif_width_px)")
    parser.add_argument("--colors", type=int, help="palette size (style gif_colors)")
    parser.add_argument("--frame-ms", type=int, help="frame duration (style gif_frame_ms)")
    parser.add_argument("--contact-stills", type=int, help="stills on the contact sheet (style)")
    parser.add_argument(
        "--run", action="append", default=[], help="run key to draw; repeat; default all"
    )
    parser.add_argument("--three", type=Path, help="local copy of Three.js r128 (three.min.js)")
    parser.add_argument("--work", type=Path, help="directory for the inlined page and stills")
    args = parser.parse_args()

    style = load_style(args.style)
    motion = style["motion"]

    def pick(value: Any, key: str, fallback: Any) -> Any:
        return value if value is not None else motion.get(key, fallback)

    hold = int(pick(args.hold, "gif_hold_frames", 12))
    step = float(pick(args.step, "gif_degrees_per_frame", 5.0))
    start_angle = float(pick(args.start_angle, "start_angle_deg", -35.0))
    elevation = float(pick(args.elevation, "elevation_deg", 28.0))
    width = int(pick(args.width, "gif_width_px", 640))
    colors = int(pick(args.colors, "gif_colors", 128))
    frame_ms = int(pick(args.frame_ms, "gif_frame_ms", 120))
    stills = int(pick(args.contact_stills, "contact_stills", 16))
    runs = json.loads(args.runs.read_text(encoding="utf-8"))
    keys = args.run or [run["key"] for run in runs["runs"]]
    known = {run["key"] for run in runs["runs"]}
    missing = [key for key in keys if key not in known]
    if missing:
        parser.error(f"unknown run keys {missing}; known: {sorted(known)}")
    ticks = max(int(run["ticks"]) for run in runs["runs"] if run["key"] in keys)
    styled_frames = motion.get("gif_frames")
    frames = int(
        args.frames
        if args.frames is not None
        else styled_frames
        if styled_frames is not None
        else ticks + 1 + hold
    )
    if frames < 1 or width < 320:
        parser.error("frames must be positive and width at least 320")
    work = args.work or args.output.with_suffix("").with_name(args.output.stem + "-render")
    work.mkdir(parents=True, exist_ok=True)
    three = three_js(args.three)
    page_html = inline_page(runs, style)
    if args.html:
        args.html.write_text(page_html, encoding="utf-8")
    started = time.time()
    images, errors, blocked = capture_frames(
        page_html,
        keys,
        ticks,
        frames=frames,
        step=step,
        start_angle=start_angle,
        elevation=elevation,
        width=width,
        three=three,
        work=work,
    )
    if errors:
        raise RuntimeError("page errors: " + "; ".join(errors))
    images = pad_to_one_size(images)
    quantized = quantize(images, colors)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    quantized[0].save(
        args.output,
        save_all=True,
        append_images=quantized[1:],
        duration=frame_ms,
        loop=0,
        optimize=False,
        disposal=1,
    )
    sheet_path = args.contact_sheet or args.output.with_name(args.output.stem + "-contact.png")
    contact_sheet(images, count=stills).save(sheet_path)
    still_paths = {}
    for index in sorted({0, min(ticks // 2, frames - 1), min(ticks, frames - 1), frames - 1}):
        path = work / f"frame-{index:03d}.png"
        images[index].save(path)
        still_paths[index] = str(path)
    with Image.open(args.output) as check:
        n_frames, size = getattr(check, "n_frames", 1), check.size
    summary = {
        "gif": str(args.output),
        "gif_bytes": args.output.stat().st_size,
        "n_frames": n_frames,
        "size_px": list(size),
        "frame_ms": frame_ms,
        "step_deg": step,
        "start_angle_deg": start_angle,
        "elevation_deg": elevation,
        "colors": colors,
        "style": str(args.style or STYLE_FILE),
        "contact_stills": stills,
        "runs": keys,
        "tick_schedule": f"tick = min(frame, {ticks}); frames {ticks + 1}..{frames - 1} hold tick {ticks}",
        "records": [
            {
                "key": run["key"],
                "model": run.get("model"),
                "source_sha256": (run.get("record") or {}).get("source_sha256"),
                "initialization_sha256": (run.get("record") or {}).get("initialization_sha256"),
            }
            for run in runs["runs"]
            if run["key"] in keys
        ],
        "three_js": THREE_URL,
        "three_served_from": str(three),
        "blocked_requests": blocked,
        "contact_sheet": str(sheet_path),
        "stills": still_paths,
        "elapsed_seconds": round(time.time() - started, 1),
    }
    (work / "render-summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
