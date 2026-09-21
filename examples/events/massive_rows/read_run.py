"""The reading of a `slits_matter` run against the pin (the design's section
4, `expectations.json` beside the worlds): every number a DETECTOR reading
(the screen's gathers, the first `click` lines) or a GAMEBOARD reading (the
faces' and the wall's completions, the books), labelled so.

    PYTHONPATH=src python examples/events/massive_rows/read_run.py <run dir> [--births W] [--write KEY]

`<run dir>` holds `run.json` and `events.jsonl` of the runner; `--births`
the records read (the wheel's W by default, read from the world); `--write`
puts the reading into `expectations.json` under `<KEY>.run` (the register's
line of the run, beside the pin). The two-source cosine is `1 + cos(2 pi
(l_2 - l_1) / lambda)` with lambda = h / p (de Broglie) and l_1, l_2 the
Euclidean distances from the openings to the pixel, the reading of
`slits_huygens`' register (the amplitude README, L2b); Pearson over the
121 pixels, the visibility between the cosine's bright pixels (y = 35 to
38, 59 to 61, 82 to 85) and its dark ones (13 to 20, 48 to 50, 70 to 72,
100 to 107), the bands' centres the count-weighted means of the three
bright bands; the group pace the first `click` line at `screen_60`,
`screen_37` and `screen_83`. The host's arithmetic on the counts (the
cosine, Pearson) is the reading tool's, not the engine's.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIGHT = [35, 36, 37, 38, 59, 60, 61, 82, 83, 84, 85]
DARK = list(range(13, 21)) + [48, 49, 50, 70, 71, 72] + list(range(100, 108))
BANDS = {"left": range(30, 44), "centre": range(53, 68), "right": range(77, 91)}
PACE_PIXELS = (60, 37, 83)


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return sxy / math.sqrt(sxx * syy) if sxx and syy else float("nan")


def read(run: Path, births: int | None = None) -> dict[str, object]:
    record = json.loads((run / "run.json").read_text(encoding="utf-8"))
    world = json.loads((run / "initialization.json").read_text(encoding="utf-8"))
    lamp = next(m for m in world["measured"] if "lamp" in m)
    wheel = int(lamp["lamp"]["wheel"][1])
    births = wheel if births is None else births
    family = next(f for f in world["families"] if f.get("massive"))
    h, p = int(world["action"]), int(lamp["lamp"]["momentum_magnitude"])
    wavelength = h / p
    openings = [tuple(m["position"][:2]) for m in world["measured"] if isinstance(m.get("table"), dict)]
    screen_x = max(m["position"][0] for m in world["measured"])
    pixels = world["shape"][1]
    base = (lamp_number := 1) << 32
    assert lamp_number == 1
    gathers = [
        g
        for g in record["world"]
        if g["family"] == family["name"] and base + 1 <= int(g["record"]) <= base + births
    ]
    counts = [0] * pixels
    wall = 0
    faces: dict[str, int] = {}
    missing = 0
    for g in gathers:
        chosen = g["chosen"]
        if chosen is None:
            missing += 1
            continue
        name = str(chosen[0][0])
        if name.startswith("screen_"):
            counts[int(name.split("_")[1])] += 1
        elif name.startswith("face:"):
            faces[name] = faces.get(name, 0) + 1
        else:
            wall += 1
    cosine = []
    for y in range(pixels):
        l1, l2 = (math.hypot(screen_x - o[0], y - o[1]) for o in openings)
        cosine.append(1 + math.cos(2 * math.pi * (l2 - l1) / wavelength))
    bright = [counts[y] for y in BRIGHT]
    dark = [counts[y] for y in DARK]
    mean_bright, mean_dark = sum(bright) / len(bright), sum(dark) / len(dark)
    visibility = (
        (mean_bright - mean_dark) / (mean_bright + mean_dark) if mean_bright + mean_dark else None
    )
    bands = {}
    for name, span in BANDS.items():
        weight = sum(counts[y] for y in span)
        bands[name] = round(sum(y * counts[y] for y in span) / weight, 2) if weight else None
    first_click: dict[str, int | None] = {f"screen_{y}": None for y in PACE_PIXELS}
    with (run / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"click"' not in line:
                continue
            event = json.loads(line)
            if event.get("event") != "click" or event.get("family") != family["name"]:
                continue
            detector = event.get("detector")
            if detector in first_click and first_click[detector] is None:
                first_click[detector] = int(event["tick"])
            if all(v is not None for v in first_click.values()):
                break
    books = record["audit"][-1]["families"][family["name"]]
    return {
        "date": "2026-09-21",
        "source_sha256": record["source_sha256"],
        "initialization_sha256": record["initialization_sha256"],
        "intervals": record["completed_ticks"],
        "elapsed_seconds": round(record["elapsed_seconds"], 1),
        "status": record["status"],
        "conserved": record["conserved_at_every_completed_tick"],
        "births_read": births,
        "born": record["layer"]["born"],
        "gathered": record["layer"]["gathered"],
        "open": record["layer"]["open"],
        "DETECTOR": {
            "screen_counts": counts,
            "screen_total": sum(counts),
            "gathers_without_a_choice": missing,
            "pearson_counts_cosine": round(pearson([float(c) for c in counts], cosine), 3),
            "visibility": None if visibility is None else round(visibility, 3),
            "bright_counts": bright,
            "dark_counts": dark,
            "dark_max": max(dark),
            "bands": bands,
            "first_click_tick": first_click,
        },
        "GAMEBOARD": {
            "wall_completions": wall,
            "face_completions": faces,
            "books_at_end": {
                "transit": books["transit"],
                "content": books["content"],
                "waiting": books["waiting"],
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("run", type=Path)
    parser.add_argument("--births", type=int)
    parser.add_argument("--write", type=str, help="the expectations key to write the reading under")
    args = parser.parse_args()
    reading = read(args.run, args.births)
    print(json.dumps(reading, indent=1))
    if args.write:
        path = HERE / "expectations.json"
        register = json.loads(path.read_text(encoding="utf-8"))
        register[args.write]["run"] = reading
        path.write_text(json.dumps(register, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
