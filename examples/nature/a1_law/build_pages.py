"""Build the two pages for the model owner from the records: e9_law.html and
a1_law.html, self-contained, the tables, an inline SVG bar chart of the counts
(and of what the screen returned), one GIF each embedded as a data URI."""

from __future__ import annotations

import base64
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(sys.argv[1])
E9 = json.loads((REPO / "examples/nature/e9_law/record.json").read_text())
A1 = json.loads((REPO / "examples/nature/a1_law/record.json").read_text())
GIFS = {"e9": Path(sys.argv[2]), "a1": Path(sys.argv[3])}

STYLE = """
:root { color-scheme: light; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e; --line: #d9d8d3;
  --series-1: #2a78d6; --series-2: #eb6834; --muted: #8a8984; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { color-scheme: dark; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7; --line: #3a3a38; --series-1: #3987e5; --series-2: #d95926; --muted: #8a8984; } }
:root[data-theme="dark"] { color-scheme: dark; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7; --line: #3a3a38; --series-1: #3987e5; --series-2: #d95926; --muted: #8a8984; }
body { margin: 0; padding: 16px; background: var(--surface); color: var(--ink); font: 15px/1.5 system-ui, sans-serif; max-width: 980px; margin-inline: auto; }
h1 { font-size: 1.5rem; margin: .2em 0; } h2 { font-size: 1.15rem; margin: 1.4em 0 .4em; border-bottom: 1px solid var(--line); }
p, li { color: var(--ink); } .muted { color: var(--ink-2); }
table { border-collapse: collapse; width: 100%; font-size: 14px; margin: .5em 0; display: block; overflow-x: auto; }
th, td { border-bottom: 1px solid var(--line); padding: 4px 8px; text-align: right; white-space: nowrap; } th:first-child, td:first-child { text-align: left; }
th { color: var(--ink-2); font-weight: 600; }
figure { margin: 1em 0; } figcaption { color: var(--ink-2); font-size: 13px; }
svg text { fill: var(--ink-2); font-size: 12px; } svg .bar { fill: var(--series-1); } svg .bar2 { fill: var(--series-2); } svg .axis { stroke: var(--line); }
img { max-width: 100%; height: auto; border-radius: 6px; }
code { font-size: 13px; }
"""


def bars(ys, values, title, unit, second=None, label2=None):
    """A single-series (or two-series) vertical bar chart as inline SVG."""
    w, h, left, bottom, top = 900, 260, 48, 28, 20
    n = len(values)
    real_max = max([abs(v) for v in values] + [abs(v) for v in (second or [])] + [0])
    vmax = max(real_max, 1)
    vmin = min([v for v in values] + [v for v in (second or [])] + [0])
    span = vmax - vmin if vmax > vmin else 1
    slot = (w - left - 12) / n
    bw = max(2, slot * (0.42 if second else 0.7))
    def y_of(v):
        return top + (vmax - v) / span * (h - top - bottom)
    y0 = y_of(0)
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}" style="width:100%;height:auto">']
    parts.append(f'<title>{html.escape(title)}</title>')
    parts.append(f'<line class="axis" x1="{left}" y1="{y0:.1f}" x2="{w-12}" y2="{y0:.1f}"/>')
    parts.append(f'<text x="{left}" y="14">{html.escape(unit)} (largest {real_max:,})</text>')
    for i, v in enumerate(values):
        x = left + i * slot + (slot - (bw * 2 + 2 if second else bw)) / 2
        y1, y2 = sorted((y_of(v), y0))
        parts.append(f'<rect class="bar" x="{x:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0.0, y2-y1):.1f}" rx="2"><title>y = {ys[i]}: {v:,}</title></rect>')
        if second is not None:
            v2 = second[i]
            y1b, y2b = sorted((y_of(v2), y0))
            parts.append(f'<rect class="bar2" x="{x+bw+2:.1f}" y="{y1b:.1f}" width="{bw:.1f}" height="{max(0.0, y2b-y1b):.1f}" rx="2"><title>y = {ys[i]}, {html.escape(label2 or "")}: {v2:,}</title></rect>')
        if n <= 16 or i % 4 == 0:
            parts.append(f'<text x="{left + i*slot + slot/2:.1f}" y="{h-8}" text-anchor="middle">{ys[i]}</text>')
    if second is not None:
        parts.append(f'<rect class="bar" x="{w-260}" y="6" width="10" height="10"/><text x="{w-246}" y="15">{html.escape(title.split(" against ")[0])}</text>')
        parts.append(f'<rect class="bar2" x="{w-130}" y="6" width="10" height="10"/><text x="{w-116}" y="15">{html.escape(label2 or "")}</text>')
    parts.append('</svg>')
    return "".join(parts)


def table(headers, rows):
    out = ["<table><thead><tr>" + "".join(f"<th>{html.escape(str(h))}</th>" for h in headers) + "</tr></thead><tbody>"]
    for row in rows:
        out.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def gif_tag(path, caption):
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'<figure><img alt="{html.escape(caption)}" src="data:image/gif;base64,{data}"><figcaption>{html.escape(caption)} ({path.stat().st_size/1e6:.2f} MB, rendered with tools/ray_viewer, phone preset, board and eye view side by side)</figcaption></figure>'


def page(title, body):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{STYLE}</style></head><body>{body}</body></html>'


def e9_page():
    worlds = E9["worlds"]
    scan = E9["scan"]["rows"]
    fill1 = worlds["ring_screen_clock_fill1"]
    marks = [m["position"][1] for m in fill1["marks"]]
    counts = [0 for _ in marks]
    body = ["<h1>E9 repeated under the law of the bit (2026-09-18)</h1>",
            "<p class='muted'>The ring of E5 with its prefilled shadow set on E6's screen of seven marks, on the engine of origin/main at ffa4a56. The engine refused the worlds: a corner Node's ray slot budget is exceeded by the shadows of the ring's eight owners in the two phases the mixing makes of a phase-0 set. Nothing here is a law; the tables are what the engine gave.</p>",
            "<h2>What was asked, what the engine gave</h2>",
            "<ul><li>Counts of things per mark: <b>0 at every mark</b> in every world (no thing leaves the ring; no run completed more than four ticks).</li>"
            "<li>Shadows returned per mark: read for the fill-1 world only, 8 quanta at (7, 5, 5) at tick 4 (phase 0), none elsewhere before the failure at tick 5.</li>"
            "<li>The pushed amount at each mark's Node: (8, 0, 0) at (7, 5, 5) at tick 4; nothing else read.</li>"
            "<li>The clocked ring: declared (K = 4096, 8 steps of 64 per interval), but the prefill releases at phase 0 and a re-release keeps a shadow's phase, so the clock enters no shadow; the runs with and without the clock fail alike.</li>"
            "<li>Fringes in counts or in the push: <b>not read</b>, no run went past tick 4.</li></ul>",
            "<h2>The runs</h2>",
            table(["World", "Fill", "Clock", "Status", "Completed ticks", "Shadows at the start", "Things", "Clicks", "Elapsed s"],
                  [[n, w["fill"], "yes" if w["clock"] else "no", f"{w['status']}: {w['error']}", w["completed_ticks"], f"{w['initial_totals']['electron'][0]:,}", f"{w['real_content'][0] if w['real_content'] else 262144:,}", w["clicks"], w["elapsed_seconds"]] for n, w in worlds.items()]),
            "<h2>The refusals, reproduced (scan_fill.py)</h2>",
            table(["Ray slots", "Fill", "Admitted", "Failed at tick", "Error"], [[r["ray_slots"], r["fill"], "yes" if r["admitted"] else "no", r["failed_tick"] if r["failed_tick"] else "(the prefill)", r["error"]] for r in scan]),
            "<h2>Counts per mark (things absorbed)</h2>",
            f"<figure>{bars(marks, counts, 'Counts per mark', 'things')}<figcaption>The seven marks at x = 7, y = 2 to 8: zero things absorbed in every world.</figcaption></figure>",
            "<h2>The fill-1 record, four ticks</h2>",
            f"<p>Real electron line {fill1['ledger_last']['real']['electron']['current'][0]:,} at every tick (no source, escape, absorption or conversion); shadows {fill1['ledger_last']['shadow']['electron']['initial'][0]:,} at the start, {fill1['ledger_last']['shadow']['electron']['current'][0]:,} at tick 4, {fill1['ledger_last']['shadow']['electron']['escaped'][0]:,} escaped; every ledger line balanced, conserved at every completed tick: {fill1['conserved_at_every_completed_tick']}. Events: {html.escape(json.dumps(fill1['events']))}.</p>",
            gif_tag(GIFS["e9"], "E9 under the law: the ring with its one-interval shell, the four ticks the engine completed"),
            "<h2>Fingerprint</h2>",
            f"<p><code>source_sha256 {fill1['source_sha256']}</code>, engine commit ffa4a56; initialization digests in docs/EXPERIMENTS.md; worlds and readers under examples/nature/e9_law/.</p>"]
    return page("E9 under the law", "".join(body))


def a1_world_section(two, one, ctl, counts_key, title):
    ys = two["screen_y"]
    clicks_by_y = {}
    for key, value in two["screen_clicks"].items():
        clicks_by_y[json.loads(key)[1]] = clicks_by_y.get(json.loads(key)[1], 0) + value
    counts = [clicks_by_y.get(y, 0) for y in ys]
    marks = f"The {len(ys)} marks of the screen at x = 40, y = {min(ys)} to {max(ys)}"
    def fmt_depth(d):
        return "none (nothing arrived)" if d["depth"] is None else f"{d['depth']:.3f} (central {d['central']:,}, nearest minimum {d['nearest_minimum']})"
    out = [f"<h2>{html.escape(title)}</h2>",
           f"<ul><li>Shadows at the start {two['initial_totals']['light'][0]:,}; the lamp's stock {two['lamp_stock']:,}; emissions {two['emissions']} photons of amount {two['photon_amount']} ({two['photons_in_flight_at_end']} in flight at the end); run {two['completed_ticks']} ticks in {two['elapsed_seconds']} s (two slits), {one['elapsed_seconds']} s (one slit).</li>"
           f"<li>Counts at the screen: <b>{sum(two['screen_clicks'].values())}</b> (two slits), <b>{sum(one['screen_clicks'].values())}</b> (one slit). Counts at the wall: {sum(two['wall_clicks'].values())} at {list(two['wall_clicks'])} from tick {two['wall_first_click']}, {sum(one['wall_clicks'].values())} in the control.</li>"
           f"<li>Shadows returned by the screen over the run: {sum(two['returned']):,} quanta (two slits), {sum(one['returned']):,} (one slit); by the wall {two['wall_returned_total']:,} and {one['wall_returned_total']:,}, peaking at {two['wall_returned_peak']:,} per tick.</li>"
           f"<li>Behind the slits, the peak amount per tick at a Node: {html.escape(json.dumps({k: (v['peak'], v['peak_tick']) for k, v in two['probes'].items()}))} (amount, tick); in the region beyond the wall at most {two['beyond_wall_peak']:,} quanta at tick {two['beyond_wall_peak_tick']}, {two['beyond_wall_last']:,} at the end.</li>"
           f"<li>Phases at the screen: {html.escape(json.dumps(two['phases']))}; owners: {html.escape(json.dumps(two['owners']))}.</li>"
           f"<li>The push J_x summed over the run, two slits: maxima at y = {[m[0] for m in two['extrema_push']['maxima']]}, minima at y = {[m[0] for m in two['extrema_push']['minima']]}, mean spacing of the maxima {two['extrema_push']['mean_spacing']} against the optical {two['optical_spacing_links']:.1f} Links; depth about the axis {fmt_depth(two['depth_push'])}.</li>"
           f"<li>The returned amount summed over the run, two slits: maxima at y = {[m[0] for m in two['extrema_returned']['maxima']]}, minima at y = {[m[0] for m in two['extrema_returned']['minima']]}, mean spacing {two['extrema_returned']['mean_spacing']}; depth {fmt_depth(two['depth_returned'])}.</li>"
           f"<li>Control: the two-slit profile against the incoherent sum of the one-slit profile and its mirror image: the cross term of the returned amount from {ctl.get('cross_min')} to {ctl.get('cross_max')} ({ctl.get('cross_sign_changes')} sign changes along y), of the push from {ctl.get('cross_push_min')} to {ctl.get('cross_push_max')} ({ctl.get('cross_push_sign_changes')} sign changes); totals {ctl.get('two_total'):,} against {ctl.get('incoherent_total'):,}.</li></ul>",
           f"<figure>{bars(ys, counts, 'Counts per mark', 'things')}<figcaption>{marks}: things absorbed over the run, two slits.</figcaption></figure>",
           f"<figure>{bars(ys, two['returned'], 'Two slits against one slit', 'quanta', one['returned'], 'one slit')}<figcaption>The amount of shadows each mark turned back over the run: two slits (blue) and the control with one slit (orange).</figcaption></figure>",
           f"<figure>{bars(ys, two['push_x'], 'Two slits against one slit', 'quanta x Link', one['push_x'], 'one slit')}<figcaption>J_x, the sum of amount x arrival heading (x component) over the shadows each mark turned back, summed over the run; positive toward +X.</figcaption></figure>",
           table(["y", "clicks (2)", "returned (2)", "peak (tick)", "first", "push_x (2)", "peak push_x (2)", "returned (1)", "push_x (1)", "cross term", "cross push"],
                 [[y, counts[k], two["returned"][k], f"{two['peak'][k]} ({two['peak_tick'][k]})", two["first_arrival"][k], two["push_x"][k], two["peak_push_x"][k], one["returned"][k], one["push_x"][k], ctl["rows"][k]["cross"] if ctl else "", ctl["rows"][k]["cross_push"] if ctl else ""] for k, y in enumerate(ys)])]
    return "".join(out)


def a1_page():
    worlds = A1["worlds"]
    two, one = worlds["two_slits"], worlds["one_slit"]
    big = "two_slits_big" in worlds and "one_slit_big" in worlds
    periodic = "two_slits_periodic" in worlds and "one_slit_periodic" in worlds
    pw = worlds.get("two_slits_periodic")
    po = worlds.get("one_slit_periodic")
    body = ["<h1>A1 repeated under the law of the bit (2026-09-18)</h1>",
            f"<p class='muted'>One lamp of light (amount 4 per interval, a clock of 4 steps of 64 per interval, lambda_w = {two['lambda_w_links']:.2f} Links) behind a wall of marks at x = 16 with two slit columns d = {two['d']} apart, a screen of marks at x = 40 (L = {two['L']}); the lamp's shadow set a shell of eight intervals of release, the longest fill the engine's prefill admits, at phase 0 (a record has no phase; the clock enters no shadow). Optical spacing lambda_w L / d = {two['optical_spacing_links']:.1f} Links. Three pairs: the open board 45 x 65 x 17 with the lamp's stock 2^22 and 2^26 (the lamp at (4, 32, 8), the slits at y = 24 and 40, the screen y = 1 to 63 at z = 8), and the closed board, periodic 45 x 49 x 9 with the stock 2^26 (the lamp at (4, 24, 4), the slits at y = 16 and 32, the screen over every y at z = 4, a second wall of marks at x = 44 closing the wrap in x: the model owner's decision of 2026-09-18, the confrontation runs are made on a closed board). Engine of origin/main at ffa4a56. Nothing here is a law; the tables are what the engine gave.</p>",
            "<h2>Headline</h2>",
            "<ul><li>Fringes in the counts of things: <b>none</b>. No thing reached the screen in any of the six worlds: every photon goes straight along its line to the wall's mark on the axis (a thing has one path; the lamp's shadows are home to its own photons and push nothing).</li>",
            (f"<li>Fringes in the push, the closed board (the run the decision asks for): the returned amount along the screen is modulated at <b>depth {pw['depth_returned']['depth']:.2f}</b> about the axis, its maxima at y = {[m[0] for m in pw['extrema_returned']['maxima']]} (the three about the axis <b>{pw['extrema_returned']['maxima'][2][0] - pw['extrema_returned']['maxima'][1][0]} Links apart</b> against the optical {pw['optical_spacing_links']:.1f}) and its minima at y = {[m[0] for m in pw['extrema_returned']['minima']]}; the push J_x at depth {pw['depth_push']['depth']:.2f} with maxima {pw['extrema_push']['mean_spacing']:.1f} Links apart on the mean; the one-slit control at depth {po['depth_returned']['depth']:.2f} (returned) and {po['depth_push']['depth']:.2f} (push). The cross term against the incoherent sum changes sign {A1['control_periodic']['cross_sign_changes']} times along the screen. What arrived is at phases {list(pw['phases'])} of 64 only: a phase-0 shell, not a wave of lambda_w. Nothing escaped ({pw['escaped_totals']['light'][0]} quanta).</li>" if periodic else "<li>Fringes in the push, the closed board: not run.</li>"),
            "<li>Fringes in the push, the open board: with the shell of 2^22 per heading nothing whole reached the screen; with 2^26 the returned amount was modulated at depth 0.73 at a mean spacing of 5.1 Links (97 % of the shell escaped through the open faces).</li></ul>"]
    if periodic:
        body.append(a1_world_section(worlds["two_slits_periodic"], worlds["one_slit_periodic"], A1.get("control_periodic", {}), "periodic", "The third pair: the closed board (periodic 45 x 49 x 9, the lamp's stock 2^26, nothing escapes)"))
    if big:
        body.append(a1_world_section(worlds["two_slits_big"], worlds["one_slit_big"], A1.get("control_big", {}), "big", "The second pair: the lamp's stock 2^26, a shell sixteen times larger"))
    body.append(a1_world_section(two, one, A1.get("control", {}), "", "The first pair: the lamp's stock 2^22"))
    body += ["<h2>The ledger at the end</h2>",
             table(["World", "Ticks", "s", "Light real: initial / current / absorbed", "Light shadow: initial / current / escaped / home", "Marks: absorbed real", "Conserved", "Real conserved"],
                   [[n, w["completed_ticks"], w["elapsed_seconds"], f"{w['ledger_last']['real']['light']['initial'][0]:,} / {w['ledger_last']['real']['light']['current'][0]:,} / {w['ledger_last']['real']['light']['absorbed'][0]:,}", f"{w['ledger_last']['shadow']['light']['initial'][0]:,} / {w['ledger_last']['shadow']['light']['current'][0]:,} / {w['ledger_last']['shadow']['light']['escaped'][0]:,} / {w['ledger_last']['shadow']['light']['absorbed_at_home'][0]:,}", f"{w['ledger_last']['light']['absorbed_by_marks'][0]:,}", w["conserved_at_every_completed_tick"], w["real_conserved"]] for n, w in worlds.items()]),
             gif_tag(GIFS["a1"], "A1 under the law: the lamp, the wall of marks with two slits, the screen; the photons on their one path to the wall (two_slits)"),
             "<h2>Fingerprint</h2>",
             f"<p><code>source_sha256 {two['source_sha256']}</code>, engine commit ffa4a56; initialization " + ", ".join(f"{n} <code>{w['initialization_sha256']}</code>" for n, w in worlds.items()) + "; worlds, Recorder and reader under examples/nature/a1_law/.</p>"]
    return page("A1 under the law", "".join(body))


PAGES = {"e9_law.html": REPO / "examples/nature/e9_law", "a1_law.html": HERE}
(PAGES["e9_law.html"] / "e9_law.html").write_text(e9_page(), encoding="utf-8")
(PAGES["a1_law.html"] / "a1_law.html").write_text(a1_page(), encoding="utf-8")
for name, folder in PAGES.items():
    print(folder / name, (folder / name).stat().st_size)
