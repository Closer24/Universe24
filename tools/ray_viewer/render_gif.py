"""Render a GIF and a contact sheet from ``runs.json`` with the viewer page.

Playwright drives headless Chromium over a copy of ``viewer.html`` with the
runs document and the style (``--style``, default ``style.json`` beside this
script) inlined. The page loads Three.js r128 from cdnjs; here that request is
answered from a local copy of the same file through a route, so the capture
needs no network, and every other request is blocked. The camera azimuth
advances ``--step`` degrees per frame while the tick runs 0..ticks and then
holds the final state for ``--hold`` frames; the runs are stacked vertically
in each frame. Pillow assembles the GIF with one shared palette and, when the
preset asks for stills, writes a contact sheet of evenly spaced frames. Every
default below comes from the style's ``motion`` block and its GIF preset
(``--preset``: ``phone``, the default, a small GIF of at most 24 frames that
reads in about six seconds; ``full``, the large anti-aliased one with a
contact sheet), so a change of look is a file edit and a re-render. The
summary always prints the GIF's size in bytes.

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
        "scene_edge",
        "ink",
        "muted",
        "line",
        "accent",
        "lattice",
        "box",
        "trail",
        "momentum_arrow",
        "families",
        "markers",
        "source",
        "detector",
        "external_body",
    ),
    "sizes": (
        "ray_width_px",
        "head_radius_px",
        "head_links",
        "arrowhead_px",
        "momentum_arrow_px_per_quantum",
        "momentum_arrow_width_px",
        "trail_links",
        "trail_width_px",
        "trail_fade",
        "field_width_px",
        "field_trail_links",
        "field_arrowhead",
        "marker_radius",
        "marker_ring_thickness",
        "marker_alpha",
        "escape_dot_radius",
        "escape_alpha",
        "click_flash_ticks",
        "click_flash_px_per_quantum",
        "click_flash_min_px",
        "click_dot_px",
        "click_dot_alpha",
        "mark_alpha",
        "source_size",
        "detector_size",
        "body_size",
        "detector_alpha",
        "glow_scale",
        "glow_alpha",
        "sphere_roughness",
        "sphere_metalness",
        "sphere_emissive",
        "label_font_px",
        "label_min_distance_px",
        "node_dot_px",
        "node_dot_alpha",
        "lattice_alpha",
        "box_alpha",
    ),
    "draw": (
        "view",
        "markers",
        "marker_shapes",
        "marker_shape",
        "shape_overrides",
        "glow",
        "vignette",
        "field_additive",
        "labels",
        "label_text",
        "escapes",
        "sources",
        "detectors",
        "external_bodies",
        "apparatus",
        "trails",
        "momentum_arrow",
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
        "gif_supersample",
        "gif_preset",
        "gif_presets",
        "contact_stills",
        "elevation_deg",
        "start_angle_deg",
        "camera_fit",
        "camera_fit_margin_links",
    ),
}
# The keys a GIF preset (style motion.gif_presets.<name>) may override.
PRESET_KEYS = (
    "gif_width_px",
    "gif_panel_px",
    "gif_max_frames",
    "gif_hold_frames",
    "gif_hold_still",
    "gif_colors",
    "gif_supersample",
    "gif_seconds",
    "gif_frame_ms",
    "gif_target_bytes",
    "contact_stills",
)
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
    presets = style.get("motion", {}).get("gif_presets", {})
    if not isinstance(presets, dict) or not all(isinstance(p, dict) for p in presets.values()):
        raise ValueError("style.motion.gif_presets must map preset names to objects")
    for name, preset in presets.items():
        extra = set(preset) - set(PRESET_KEYS)
        if extra:
            raise ValueError(f"unknown keys in style.motion.gif_presets.{name}: {sorted(extra)}")
    chosen = style.get("motion", {}).get("gif_preset")
    if chosen is not None and chosen not in presets:
        raise ValueError(f"style.motion.gif_preset {chosen!r} is not one of {sorted(presets)}")
    return style


def preset_motion(motion: dict[str, Any], name: str | None) -> dict[str, Any]:
    """The motion block with the named GIF preset (default: ``gif_preset``) laid over it."""
    presets = motion.get("gif_presets", {})
    chosen = name if name is not None else motion.get("gif_preset")
    if chosen is None:
        return dict(motion)
    if chosen not in presets:
        raise ValueError(f"unknown GIF preset {chosen!r}; the style has {sorted(presets)}")
    return {**motion, **presets[chosen]}


def tick_schedule(ticks: int, hold: int, frames: int | None = None) -> list[int]:
    """The tick each frame shows: 0..ticks, then ``hold`` frames of the last tick.

    With a frame cap the moving frames are spread evenly over the run so it still
    reaches its end, and at most a quarter of the frames hold the last tick."""
    full = list(range(ticks + 1)) + [ticks] * hold
    if frames is None or len(full) == frames:
        return full
    if len(full) < frames:
        return full + [ticks] * (frames - len(full))
    if frames <= 2:
        return [0, ticks][:frames]
    holding = min(hold, max(1, frames // 4))
    moving = max(2, frames - holding)
    return [round(i * ticks / (moving - 1)) for i in range(moving)] + [ticks] * (frames - moving)


def frame_duration_ms(seconds: float | None, frames: int, fallback: int) -> int:
    """The frame duration that makes the GIF read in ``seconds``; at least 20 ms."""
    if seconds is None:
        return fallback
    return max(20, round(seconds * 1000 / max(1, frames)))


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


def side_by_side(parts: list[Image.Image]) -> Image.Image:
    """Panels left to right, tops aligned, the ground colour filling any gap."""
    width = sum(im.width for im in parts)
    height = max(im.height for im in parts)
    frame = Image.new("RGB", (width, height), parts[0].getpixel((0, 0)))
    x = 0
    for im in parts:
        frame.paste(im, (x, 0))
        x += im.width
    return frame


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
    schedule: list[int],
    angles: list[float],
    *,
    elevation: float,
    width: int,
    three: Path,
    work: Path,
    supersample: int = 1,
    views: tuple[str, ...] = ("board",),
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
            device_scale_factor=max(1, supersample),
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
        for i, (tick, angle) in enumerate(zip(schedule, angles, strict=True)):
            parts = []
            for j, key in enumerate(run_keys):
                panels = []
                for view in views:
                    page.evaluate("v => window.__setStyle({draw: {view: v}})", view)
                    page.evaluate(
                        "([t, a, r, m, e]) => { window.__capture(m); window.__render(t, a, r, e); }",
                        [tick, angle, key, "first" if j == 0 else "second", elevation],
                    )
                    png = capture.screenshot(type="png")
                    image = Image.open(io.BytesIO(png)).convert("RGB")
                    if supersample > 1:
                        # Rendered at supersample times the size and scaled down: gentle anti-aliasing.
                        image = image.resize(
                            (image.width // supersample, image.height // supersample),
                            Image.Resampling.LANCZOS,
                        )
                    panels.append(image)
                parts.append(side_by_side(panels) if len(panels) > 1 else panels[0])
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
    parser.add_argument(
        "--preset",
        help="GIF preset from the style's motion.gif_presets (default: motion.gif_preset)",
    )
    parser.add_argument(
        "--frames",
        type=int,
        help="frame count; the run is spread over them (default: the preset's gif_max_frames cap, "
        "else ticks + 1 + hold)",
    )
    parser.add_argument(
        "--hold", type=int, help="frames that hold the final tick (style gif_hold_frames)"
    )
    parser.add_argument("--step", type=float, help="camera azimuth per frame, degrees (style)")
    parser.add_argument("--start-angle", type=float, help="degrees (style start_angle_deg)")
    parser.add_argument("--elevation", type=float, help="degrees (style elevation_deg)")
    parser.add_argument("--width", type=int, help="pixels (style gif_width_px)")
    parser.add_argument("--colors", type=int, help="palette size (style gif_colors)")
    parser.add_argument("--frame-ms", type=int, help="frame duration (style gif_frame_ms)")
    parser.add_argument(
        "--contact-stills", type=int, help="stills on the contact sheet, 0 for none (preset)"
    )
    parser.add_argument(
        "--run", action="append", default=[], help="run key to draw; repeat; default all"
    )
    parser.add_argument("--three", type=Path, help="local copy of Three.js r128 (three.min.js)")
    parser.add_argument("--view", choices=["board", "eye"], help="override the style's draw.view")
    parser.add_argument(
        "--side-by-side",
        action="store_true",
        help="render the board view and the eye view as two panels, left and right",
    )
    parser.add_argument("--work", type=Path, help="directory for the inlined page and stills")
    args = parser.parse_args()

    style = load_style(args.style)
    if args.view:
        style["draw"]["view"] = args.view
    views: tuple[str, ...] = ("board", "eye") if args.side_by_side else (style["draw"]["view"],)
    try:
        motion = preset_motion(style["motion"], args.preset)
    except ValueError as error:
        parser.error(str(error))
    preset = args.preset if args.preset is not None else style["motion"].get("gif_preset")

    def pick(value: Any, key: str, fallback: Any) -> Any:
        return value if value is not None else motion.get(key, fallback)

    hold = int(pick(args.hold, "gif_hold_frames", 12))
    step = float(pick(args.step, "gif_degrees_per_frame", 5.0))
    start_angle = float(pick(args.start_angle, "start_angle_deg", -35.0))
    elevation = float(pick(args.elevation, "elevation_deg", 28.0))
    panel_key = "gif_panel_px" if len(views) > 1 else "gif_width_px"
    width = int(pick(args.width, panel_key, motion.get("gif_width_px", 640)))
    colors = int(pick(args.colors, "gif_colors", 128))
    stills = int(pick(args.contact_stills, "contact_stills", 16))
    supersample = int(motion.get("gif_supersample", 1) or 1)
    target_bytes = motion.get("gif_target_bytes")
    runs = json.loads(args.runs.read_text(encoding="utf-8"))
    keys = args.run or [run["key"] for run in runs["runs"]]
    known = {run["key"] for run in runs["runs"]}
    missing = [key for key in keys if key not in known]
    if missing:
        parser.error(f"unknown run keys {missing}; known: {sorted(known)}")
    ticks = max(int(run["ticks"]) for run in runs["runs"] if run["key"] in keys)
    cap = args.frames
    if cap is None:
        cap = motion.get("gif_frames")
    if cap is None:
        cap = motion.get("gif_max_frames")
    schedule = tick_schedule(ticks, hold, None if cap is None else int(cap))
    frames = len(schedule)
    frame_ms = int(
        args.frame_ms
        if args.frame_ms is not None
        else frame_duration_ms(motion.get("gif_seconds"), frames, int(motion.get("gif_frame_ms", 120)))
    )
    if frames < 1 or width < 320:
        parser.error("frames must be positive and width at least 320")
    # With a still hold the camera stops at the run's end, so the hold frames are
    # identical and the GIF stores them once with the whole hold's duration.
    hold_still = bool(motion.get("gif_hold_still", False))
    first_end = schedule.index(ticks) if ticks in schedule else frames - 1
    angles = [start_angle + step * (min(i, first_end) if hold_still else i) for i in range(frames)]
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
        schedule,
        angles,
        elevation=elevation,
        width=width,
        three=three,
        work=work,
        supersample=supersample,
        views=views,
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
    sheet_path: Path | None = None
    still_paths: dict[int, str] = {}
    if stills > 0:
        # Stills belong to the full preset; the phone preset writes the GIF alone.
        sheet_path = args.contact_sheet or args.output.with_name(args.output.stem + "-contact.png")
        contact_sheet(images, count=stills, width=320 * len(views)).save(sheet_path)
        for index in sorted({0, frames // 2, frames - 1}):
            path = work / f"frame-{index:03d}.png"
            images[index].save(path)
            still_paths[index] = str(path)
    with Image.open(args.output) as check:
        n_frames, size = getattr(check, "n_frames", 1), check.size
    gif_bytes = args.output.stat().st_size
    above_target = target_bytes is not None and gif_bytes > int(target_bytes)
    summary = {
        "gif": str(args.output),
        "gif_bytes": gif_bytes,
        "gif_target_bytes": target_bytes,
        "above_target": above_target,
        "preset": preset,
        "frames": frames,
        "hold_still": hold_still,
        "n_frames": n_frames,
        "size_px": list(size),
        "frame_ms": frame_ms,
        "seconds": round(frames * frame_ms / 1000, 2),
        "step_deg": step,
        "start_angle_deg": start_angle,
        "elevation_deg": elevation,
        "colors": colors,
        "style": str(args.style or STYLE_FILE),
        "contact_stills": stills,
        "supersample": supersample,
        "views": list(views),
        "runs": keys,
        "tick_schedule": schedule,
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
        "contact_sheet": None if sheet_path is None else str(sheet_path),
        "stills": still_paths,
        "elapsed_seconds": round(time.time() - started, 1),
    }
    (work / "render-summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))
    note = f", above the preset's target of {target_bytes}" if above_target else ""
    print(
        f"GIF {args.output}: {gif_bytes} bytes, {n_frames} frames stored of {frames}, "
        f"{size[0]}x{size[1]} px, {summary['seconds']} s{note}"
    )


if __name__ == "__main__":
    main()
