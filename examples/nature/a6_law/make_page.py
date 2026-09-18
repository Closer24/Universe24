"""Write `a6_law.html`, the page of A6 repeated under the law of the bit: a
self-contained page (no script, no request) built from the analyzer's
`record.json`, the probe's tables and one GIF of `tools/ray_viewer` inlined as
a data URI; the tables of the four tests per reading and per w against
Einstein, Newton and the derivation, and an inline SVG of the bending against
1 / b with the GR and Newton lines. A Renderer of records (Highlights 3.29): it
computes nothing the analyzer did not, and reads no engine.

Run:  python examples/nature/a6_law/make_page.py --record record.json --gif bend.gif --probe probe_m256.json --out a6_law.html
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import math
from pathlib import Path

GR_W_NOTE = "3 x 1.861 sqrt(GM)"


def esc(value):
    return html.escape(str(value))


def fmt(value, digits=3):
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def table(headers, rows, caption=None):
    out = ["<table>"]
    if caption:
        out.append(f"<caption>{esc(caption)}</caption>")
    out.append("<thead><tr>" + "".join(f"<th>{esc(h)}</th>" for h in headers) + "</tr></thead><tbody>")
    for row in rows:
        out.append("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def world_label(result):
    w = result["w"]
    wname = "w = 1" if w == 1 else f"w = {w:.2f} (GR)"
    return f"{result['model'].replace('a6-law-', '')} [{result['wait_reads']}, {wname}]"


def clock_rows(results):
    """One row per cavity per clock world: r, rate, waits, quanta, left tick."""
    rows = []
    for result in results:
        if result["kind"] != "clock":
            continue
        for clock in result["clocks"]:
            rows.append(
                [
                    world_label(result),
                    "closed" if result["boundary"] == "periodic" else "open",
                    f"{clock['r']} ({clock['r_euclid']:.2f})",
                    "".join("+-"[c < 0] + "xyz"[i] for i, c in enumerate(clock["axis"]) if c),
                    fmt(clock["rate"], 4),
                    clock["waits_in_cavity"],
                    f"{clock['quanta_read_in_cavity']} in {clock['push_ticks_in_cavity']} ticks",
                    clock["stayed_ticks"],
                    clock["left_tick"] if clock["left_tick"] is not None else "stayed",
                ]
            )
    return rows


def clock_fit_rows(results):
    rows = []
    for result in results:
        if result["kind"] != "clock" or not result["star_on"]:
            continue
        gm = result["mass"]["GM"] if result["mass"] else None
        fits = result["fits"]
        a = fits["1/r"]["coefficient"]
        b = fits["1/r^2"]["coefficient"]
        w = result["w"]
        # The derivation's coefficients: amplitude (section 40) at the star as
        # one owner, 1 - (w/3) 0.5373 sqrt(GM) / r; count (section 35), 1 -
        # (sqrt(3) w / 2) GM / r^2 in the free field; the cavity reads every
        # other interval, so half of each.
        amp = (w / 3) * 0.5373 * math.sqrt(gm) / 2 if gm else None
        count = (math.sqrt(3) * w / 2) * gm / 2 if gm else None
        rows.append(
            [
                world_label(result),
                fmt(a, 4),
                fmt(fits["1/r"]["rss"], 5),
                fmt(b, 4),
                fmt(fits["1/r^2"]["rss"], 5),
                fmt(a / gm, 4) if (a is not None and gm) else "-",
                "1 (GR, at the GR w)",
                fmt(amp, 3),
                fmt(count, 3),
            ]
        )
    return rows


def fit_origin(points, power):
    """Least squares y = A / r^power through the origin (as analyze.py)."""
    xs = [(1.0 / r**power, y) for r, y in points]
    sxx = sum(x * x for x, _ in xs)
    if sxx == 0:
        return None, None
    a = sum(x * y for x, y in xs) / sxx
    return a, sum((y - a * x) ** 2 for x, y in xs)


def pooled_fit_rows(results):
    """The eight cavities of the two batches pooled per mass, reading and w."""
    groups = {}
    for result in results:
        if result["kind"] != "clock" or not result["star_on"] or result["boundary"] != "periodic":
            continue
        key = (result["mass"]["X"], result["wait_reads"], result["w"])
        groups.setdefault(key, []).extend(
            (c["r_euclid"], 1.0 - c["rate"]) for c in result["clocks"] if c["rate"] is not None
        )
    rows = []
    for (x, reading, w), points in sorted(groups.items()):
        gm = 6 * x / (2 * math.pi)
        a, rss_a = fit_origin(points, 1)
        b, rss_b = fit_origin(points, 2)
        rows.append(
            [
                f"X = {x} (GM = {gm:.1f})",
                reading,
                "1" if w == 1 else f"{w:.2f} (GR)",
                len(points),
                fmt(a, 3),
                fmt(rss_a, 3),
                fmt(b, 2),
                fmt(rss_b, 3),
                fmt(a / gm, 4) if a is not None else "-",
                fmt((w / 3) * 0.5373 * math.sqrt(gm) / 2, 3),
                fmt((math.sqrt(3) * w / 2) * gm / 2, 1),
            ]
        )
    return rows


def redshift_rows(results):
    rows = []
    for result in results:
        if result["kind"] != "clock" or not result["star_on"]:
            continue
        gm = result["mass"]["GM"] if result["mass"] else None
        w = result["w"]
        clocks = sorted(result["clocks"], key=lambda c: (c["r"], c["axis"]))
        for near, far in zip(clocks, clocks[1:], strict=False):
            if near["rate"] is None or far["rate"] is None or near["rate"] == 0 or near["r"] == far["r"]:
                continue
            z = far["rate"] / near["rate"] - 1
            r1, r2 = near["r_euclid"], far["r_euclid"]
            rows.append(
                [
                    world_label(result),
                    f"{near['r']} -> {far['r']} ({r1:.2f} -> {r2:.2f})",
                    fmt(z, 4),
                    fmt(gm * (1 / r1 - 1 / r2), 3) if gm else "-",
                    fmt((w / 3) * 0.5373 * math.sqrt(gm) * (1 / r1 - 1 / r2) / 2, 4) if gm else "-",
                    fmt((math.sqrt(3) * w / 2) * gm * (1 / r1**2 - 1 / r2**2) / 2, 4) if gm else "-",
                ]
            )
    return rows


def bend_rows(results):
    rows = []
    for result in results:
        if result["kind"] != "bend":
            continue
        gm = result["mass"]["GM"] if (result["mass"] and result["star_on"]) else 0.0
        for b, entry in sorted(result["per_b"].items(), key=lambda kv: int(kv[0])):
            bb = int(b)
            alpha = entry["fraction_turned"] * math.pi / 2
            rows.append(
                [
                    world_label(result),
                    "closed" if result["boundary"] == "periodic" else "open",
                    bb,
                    f"{entry['turned']}/{entry['lines']}",
                    f"{entry['frozen']} at r = {min(entry['stop_r'])} to {max(entry['stop_r'])}"
                    if entry["frozen"]
                    else "0",
                    fmt(entry["mean_quanta_read"], 2),
                    fmt(entry["mean_net_transverse_toward"], 2),
                    fmt(alpha, 3),
                    fmt(4 * gm / bb, 2),
                    fmt(2 * gm / bb, 2),
                    fmt(gm / bb, 2),
                    ", ".join(str(t) for t in entry["turn_ticks"]) or "-",
                ]
            )
    return rows


def shapiro_rows(results):
    rows = []
    for result in results:
        if result["kind"] != "bend":
            continue
        gm = result["mass"]["GM"] if (result["mass"] and result["star_on"]) else 0.0
        w = result["w"]
        for b, entry in sorted(result["per_b"].items(), key=lambda kv: int(kv[0])):
            bb = int(b)
            half = result.get("side", 33) // 2
            log = math.log(4 * half * half / bb**2)
            rows.append(
                [
                    world_label(result),
                    bb,
                    f"{entry['arrived']}/{entry['lines']}",
                    ", ".join(str(d) for d in entry["delays_of_arrived"]) or "-",
                    fmt(entry["mean_delay_of_arrived"], 2),
                    fmt(2 * gm * log, 1),
                    fmt((w / 3) * 0.5373 * math.sqrt(gm) * log, 2),
                    fmt(2.72 * w * gm / bb, 1),
                ]
            )
    return rows


def sep_rows(results):
    rows = []
    for result in results:
        if result["kind"] != "sep":
            continue
        rows.append(
            [
                result["model"].replace("a6-law-", ""),
                result["shadow_wait"] or "absent",
                "yes" if result["mass_on"] else "no",
                result["receiver_first_move_tick"]
                if result["receiver_first_move_tick"] is not None
                else "never",
                ", ".join(str(t) for t in result["receiver_first_waits"][:8]) or "-",
                result["receiver_moved"],
            ]
        )
    return rows


def bending_svg(results):
    """Deflection against 1 / b: the measured mean exit angle per b (one point
    per world and b) and the lines 4GM/b, 2GM/b and GM/b of the m256 mass."""
    width, height, left, bottom, top, right = 640, 360, 60, 40, 20, 20
    gms = [r["mass"]["GM"] for r in results if r["kind"] == "bend" and r["star_on"] and r["mass"]]
    gm = max(gms) if gms else 1.0
    xmax = 1 / 3 * 1.05
    ymax = max(math.pi / 2, 4 * gm / 3) * 1.05
    ymax = max(ymax, 4 * gm * xmax)

    def sx(x):
        return left + (width - left - right) * x / xmax

    def sy(y):
        return height - bottom - (height - bottom - top) * y / ymax

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="deflection against 1 over b">'
    ]
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="var(--panel)"/>')
    parts.append(
        f'<line x1="{left}" y1="{sy(0)}" x2="{width - right}" y2="{sy(0)}" stroke="var(--ink)"/>'
    )
    parts.append(f'<line x1="{left}" y1="{sy(0)}" x2="{left}" y2="{top}" stroke="var(--ink)"/>')
    for b in (3, 4, 6, 8):
        x = 1 / b
        parts.append(
            f'<line x1="{sx(x)}" y1="{sy(0)}" x2="{sx(x)}" y2="{sy(0) + 5}" stroke="var(--ink)"/>'
        )
        parts.append(
            f'<text x="{sx(x)}" y="{sy(0) + 18}" font-size="12" text-anchor="middle" fill="var(--ink)">1/{b}</text>'
        )
    for y in (0.5, 1.0, 1.5):
        parts.append(
            f'<text x="{left - 6}" y="{sy(y) + 4}" font-size="12" text-anchor="end" fill="var(--ink)">{y}</text>'
        )
    parts.append(
        f'<text x="{width / 2}" y="{height - 4}" font-size="12" text-anchor="middle" fill="var(--ink)">1 / b (Links)</text>'
    )
    parts.append(
        f'<text x="14" y="{height / 2}" font-size="12" text-anchor="middle" fill="var(--ink)" transform="rotate(-90 14 {height / 2})">deflection (rad)</text>'
    )
    for factor, colour in ((4, "#c0392b"), (2, "#2980b9"), (1, "#27ae60")):
        x_end = min(xmax, ymax / (factor * gm)) if gm else xmax
        parts.append(
            f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(x_end)}" y2="{sy(factor * gm * x_end)}" stroke="{colour}" stroke-width="2"/>'
        )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(math.pi / 2)}" x2="{sx(xmax)}" y2="{sy(math.pi / 2)}" stroke="var(--muted)" stroke-dasharray="4 4"/>'
    )
    parts.append(
        f'<text x="{sx(xmax) - 4}" y="{sy(math.pi / 2) - 4}" font-size="11" text-anchor="end" fill="var(--muted)">a whole turn of content 1: pi/2</text>'
    )
    markers = {}
    palette = ["#8e44ad", "#d35400", "#16a085", "#7f8c8d", "#2c3e50", "#f39c12"]
    for result in results:
        if result["kind"] != "bend" or not result["star_on"]:
            continue
        label = world_label(result)
        colour = markers.setdefault(label, palette[len(markers) % len(palette)])
        for b, entry in result["per_b"].items():
            x, y = 1 / int(b), entry["fraction_turned"] * math.pi / 2
            parts.append(
                f'<circle cx="{sx(x)}" cy="{sy(y)}" r="5" fill="{colour}" fill-opacity="0.8"><title>{esc(label)} b = {b}: {y:.3f} rad</title></circle>'
            )
    legend_y = top + 10
    for label, colour in (
        ("GR 4GM/b", "#c0392b"),
        ("Newton 2GM/b", "#2980b9"),
        ("derivation GM/b", "#27ae60"),
        *markers.items(),
    ):
        parts.append(
            f'<rect x="{left + 10}" y="{legend_y - 8}" width="10" height="10" fill="{colour}"/>'
        )
        parts.append(
            f'<text x="{left + 26}" y="{legend_y + 1}" font-size="11" fill="var(--ink)">{esc(label)}</text>'
        )
        legend_y += 15
    parts.append("</svg>")
    return "\n".join(parts)


def probe_table(probe):
    if not probe:
        return ""
    axis = probe["axis"]
    half = len(axis) // 2
    radii = list(range(1, len(axis[0]) + 1))
    late = [sum(row[i] for row in axis[half:]) / max(1, len(axis) - half) for i in range(len(radii))]
    rows = [[r, fmt(v, 2), fmt(r * r * v, 1)] for r, v in zip(radii, late, strict=True) if r <= 12]
    return table(
        ["r", "whole quanta per interval (ticks 20 to 40)", "r^2 n(r)"],
        rows,
        f"The probe: X = {probe['X']}, fill {probe['fill']}, on the +Y axis",
    )


def page(results, gif_uri, probe, fingerprint, notes):
    css = """
:root { --bg: #fbfaf7; --panel: #ffffff; --ink: #1d1d1b; --muted: #6b6b66; --line: #d9d6cf; --accent: #8e3b46; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #15161a; --panel: #1e2026; --ink: #ecebe6; --muted: #a0a09a; --line: #3a3c44; --accent: #e08a96; } }
:root[data-theme="dark"] { --bg: #15161a; --panel: #1e2026; --ink: #ecebe6; --muted: #a0a09a; --line: #3a3c44; --accent: #e08a96; }
html { background: var(--bg); }
body { margin: 0 auto; max-width: 1100px; padding: 24px 16px; background: var(--bg); color: var(--ink); font: 15px/1.5 system-ui, sans-serif; }
h1 { font-size: 1.6em; margin: 0 0 .3em; } h2 { font-size: 1.25em; margin: 1.6em 0 .4em; border-bottom: 1px solid var(--line); }
table { border-collapse: collapse; width: 100%; margin: .6em 0 1em; font-size: 13px; display: block; overflow-x: auto; }
th, td { border: 1px solid var(--line); padding: 3px 7px; text-align: left; white-space: nowrap; } th { background: var(--panel); }
caption { text-align: left; color: var(--muted); font-size: 12px; padding: 2px 0; caption-side: top; }
p.note { color: var(--muted); } code { font-size: 90%; }
figure { margin: 1em 0; } figure img { max-width: 100%; height: auto; display: block; border: 1px solid var(--line); }
figcaption { color: var(--muted); font-size: 12px; }
"""
    body = ["<h1>A6 repeated under the law of the bit (2026-09-18)</h1>"]
    body.append(f"<p>{notes['intro']}</p>")
    body.append(
        f"<p class='note'>Source fingerprint (SHA-256 of the package files, recorded by every run): <code>{esc(fingerprint)}</code>. The records stay outside the tree; <code>record.json</code> beside this page is the analyzer's summary.</p>"
    )
    body.append("<h2>1. The clock of a thing at rest</h2>")
    body.append(f"<p>{notes['clock']}</p>")
    body.append(
        table(
            [
                "world",
                "board",
                "r (Euclidean)",
                "half-axis",
                "rate",
                "waits",
                "quanta read (net, per push tick)",
                "ticks stayed",
                "left at tick",
            ],
            clock_rows(results),
            "Per cavity: the rate (moving intervals over intervals) while the thing stayed between its mirrors.",
        )
    )
    body.append(
        table(
            [
                "world",
                "A (1/r fit)",
                "rss",
                "B (1/r^2 fit)",
                "rss",
                "A / GM (GR: 1 at the GR w)",
                "GR",
                "derivation, amplitude: (w/3) 0.537 sqrt(GM) / 2",
                "derivation, count: (sqrt3 w/2) GM / 2",
            ],
            clock_fit_rows(results),
            "The deficit 1 - rate fitted through the origin; the derivation's coefficients halved for a cavity that reads every other interval.",
        )
    )
    body.append(
        table(
            [
                "mass",
                "reading",
                "w",
                "cavities",
                "A (1/r)",
                "rss",
                "B (1/r^2)",
                "rss",
                "A / GM (GR: 1 at the GR w)",
                "derivation, amplitude (halved)",
                "derivation, count (halved)",
            ],
            pooled_fit_rows(results),
            "The two slopes: the cavities of both batches pooled per mass, reading and w.",
        )
    )
    body.append("<h2>2. The redshift between two radii</h2>")
    body.append(
        table(
            [
                "world",
                "r_near -> r_far",
                "z = rate(far)/rate(near) - 1",
                "GR: GM (1/r1 - 1/r2)",
                "derivation, amplitude",
                "derivation, count",
            ],
            redshift_rows(results),
        )
    )
    body.append("<h2>3. The bending of a light thing</h2>")
    body.append(f"<p>{notes['bend']}</p>")
    body.append(bending_svg(results))
    body.append(
        table(
            [
                "world",
                "board",
                "b",
                "lines pushed transversally",
                "lines frozen (where)",
                "quanta read per line",
                "net transverse toward the star",
                "mean exit angle (rad)",
                "GR 4GM/b",
                "Newton 2GM/b",
                "derivation GM/b",
                "turn ticks",
            ],
            bend_rows(results),
        )
    )
    body.append("<h2>4. The Shapiro delay</h2>")
    body.append(
        table(
            [
                "world",
                "b",
                "lines arrived",
                "delays (ticks past the straight arrival)",
                "mean delay",
                "GR 2GM ln(4 x_A x_B / b^2)",
                "derivation, amplitude: (w/3) 0.537 sqrt(GM) ln(...)",
                "derivation, count: 2.72 w GM / b",
            ],
            shapiro_rows(results),
        )
    )
    body.append("<h2>5. The shadow's wait: the separating run</h2>")
    body.append(f"<p>{notes['sep']}</p>")
    body.append(
        table(
            [
                "world",
                "shadow_wait",
                "mass",
                "receiver's first move (tick)",
                "receiver's first waits (ticks)",
                "receiver moved (intervals)",
            ],
            sep_rows(results),
        )
    )
    body.append("<h2>The field the runs read</h2>")
    body.append(f"<p>{notes['probe']}</p>")
    body.append(probe_table(probe))
    if gif_uri:
        body.append("<h2>One rendering</h2>")
        body.append(
            f"<figure><img src='{gif_uri}' alt='the bending world rendered by the ray viewer'><figcaption>{esc(notes['gif'])}</figcaption></figure>"
        )
    body.append("<h2>Fingerprints</h2>")
    rows = [
        [
            r["model"].replace("a6-law-", ""),
            r["status"],
            r["ticks"],
            fmt(r["elapsed_seconds"], 0),
            "yes" if r["all_balanced"] else "no",
            str(r["standing"].get("standing_field_iterations")),
            str(r["standing"].get("standing_field_residual")),
            r["source_sha256"][:16],
            r["initialization_sha256"][:16],
        ]
        for r in results
    ]
    body.append(
        table(
            [
                "world",
                "status",
                "ticks",
                "seconds",
                "ledger balanced",
                "standing set found after",
                "last residual",
                "source sha256",
                "world sha256",
            ],
            rows,
        )
    )
    return (
        f"<!DOCTYPE html>\n<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>A6 under the law</title><style>{css}</style></head><body>\n"
        + "\n".join(body)
        + "\n</body></html>\n"
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--gif", type=Path)
    parser.add_argument("--probe", type=Path)
    parser.add_argument(
        "--notes",
        type=Path,
        required=True,
        help="JSON with the page's paragraphs: intro, clock, bend, sep, probe, gif",
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    results = json.loads(args.record.read_text(encoding="utf-8"))
    gif_uri = ""
    if args.gif:
        gif_uri = "data:image/gif;base64," + base64.b64encode(args.gif.read_bytes()).decode("ascii")
    probe = json.loads(args.probe.read_text(encoding="utf-8")) if args.probe else None
    notes = json.loads(args.notes.read_text(encoding="utf-8"))
    fingerprints = sorted({r["source_sha256"] for r in results})
    text = page(results, gif_uri, probe, ", ".join(fingerprints), notes)
    args.out.write_text(text, encoding="utf-8")
    print(args.out, len(text.encode("utf-8")), "bytes")


if __name__ == "__main__":
    main()
