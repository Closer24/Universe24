"""The variants' pages from the law's real line (docs/ALGEBRA.md, The two slits' variants under the click's read; the derivations under papers/one_rule/variants/ with their README): three small animated pages, each a canvas player with a slider in the look pages' dark style (tools/look/page.py's tokens), the frames computed by the derivation's own scripts' functions and numbers (their outputs under papers/one_rule/variants/out/) and embedded as compact JSON, so that the pages are reproducible from the tree and every number on them is a script's or its output's; the page computes nothing but what it draws. examples/variants/e_time_slits.html (E): the two packets of light on the chain, the second the first's copy laid d Links behind, two slits in time, stepped by Rule3's line for light at the vacuum's paces, and at the probe Node the body's two quadratures accumulating P^2 = X^2 + Y^2 across the band, the fringes in frequency building under the single packet's envelope. examples/variants/d_mach_zehnder.html (D): the record's plane wave through the Mach-Zehnder's two arms at Delta L = 0 to 4 Links over a window of four periods, the arms adding at the second splitter and the exit side's weights accumulating as the side books them (the engine's meeting_back.side_weights on the arms' second moments, exact in the integers), the second splitter in or out at the viewer's word, the choice's interval any before the record reaches it. examples/variants/b_marker.html (B): the screen's row per region as the bolometer reads the marked two-part record, F[L] + F[U] + 2 cos theta F[L, U], beside the plain row over the marker's angle, the visibility cos theta and the distinguishability sin theta, and the eraser's two conditional rows F[L + U] and F[L - U] summing back to twice the incoherent row. No click on any of the three: the law's real line alone.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/look/line_page.py [--out examples/variants] [--only b|d|e]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "papers" / "one_rule" / "variants" / "scripts"
OUTPUTS = ROOT / "papers" / "one_rule" / "variants" / "out"
PAGES = ROOT / "examples" / "variants"
STRIDE = 5  # the time slits' frames, one per this many intervals
SPAN = (120, 620)  # the chain's Nodes drawn on the time slits' page
ARM = 24  # the first arm's Nodes drawn on the Mach-Zehnder page
EXIT = 12  # an exit's Nodes drawn
DEGREES = 90  # the marker's angle runs from 0 to this, one frame per degree
IDENTITY = ((1, 0), (0, 1))


def script(name: str) -> ModuleType:
    """One of the derivation's scripts loaded by its path (its own imports of the engine on the path)."""
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def output(name: str) -> dict[str, Any]:
    """A script's output under out/, the numbers the page carries."""
    found = json.loads((OUTPUTS / f"{name}.json").read_text(encoding="utf-8"))
    assert isinstance(found, dict)
    return found


def rounded(values: Any, digits: int) -> list[Any]:
    """A row as the page carries it, each number rounded (an integer where the digits are 0)."""
    return [
        int(round(float(v))) if digits == 0 else round(float(v), digits)
        for v in np.asarray(values).ravel()
    ]


def time_slits() -> dict[str, Any]:
    """E: the chain stepped with its profile kept (the script's lay and its line's coefficients, the probe's trace asserted equal to the script's own stepping), the two quadratures at the probe accumulated interval by interval over the band's grid, P^2 relative to the single packet's final peak (the final P^2 asserted equal to the script's quadratures), the frames every STRIDE intervals over the Nodes SPAN; the numbers the script's output."""
    e, out = script("e_time_slits"), output("e_time_slits")
    read, self_over_wall = e.line_light()
    k = 2 * math.pi / e.WAVELENGTH
    cos_omega = read * (math.cos(k) + 2) + self_over_wall / 2  # the band, as the script forms it
    omega = math.acos(cos_omega)
    assert abs(omega - float(out["band"]["omega"])) < 1e-12
    d, amplitude = e.SEPARATION, 1000.0
    first = e.lay(e.CHAIN, k, omega, e.COLUMN, e.EDGE, amplitude)
    second = e.lay(e.CHAIN, k, omega, e.COLUMN, e.EDGE, amplitude, shift=d)

    def profiles(now: np.ndarray, before: np.ndarray) -> np.ndarray:
        kept = np.zeros((e.INTERVALS + 1, e.CHAIN))
        for t in range(e.INTERVALS + 1):
            kept[t] = now
            if t == e.INTERVALS:
                break
            arrivals = 4 * now  # y and z folded: four of the six arrivals are the Node itself
            arrivals[1:] += now[:-1]
            arrivals[:-1] += now[1:]
            before, now = now, read * arrivals + self_over_wall * now - before
        return kept

    single = profiles(first[0].copy(), first[1].copy())
    double = profiles(first[0] + second[0], first[1] + second[1])
    trace_single = e.stepped(
        first[0].copy(), first[1].copy(), read, self_over_wall, e.INTERVALS, e.PROBE
    )
    assert np.allclose(single[:, e.PROBE], trace_single)  # the script's own stepping, bit for bit
    grid = np.linspace(omega - e.HALF_SPAN, omega + e.HALF_SPAN, e.POINTS)
    times = np.arange(e.INTERVALS + 1)
    cosines, sines = np.cos(np.outer(grid, times)), np.sin(np.outer(grid, times))

    def accumulated(trace: np.ndarray) -> np.ndarray:  # P^2 up to each interval, (intervals + 1, points)
        x = np.cumsum(cosines * trace, axis=1)
        y = np.cumsum(sines * trace, axis=1)
        return (x * x + y * y).T

    p_single, p_double = accumulated(single[:, e.PROBE]), accumulated(double[:, e.PROBE])
    assert np.allclose(p_double[-1], [e.quadratures(double[:, e.PROBE], w) for w in grid])
    peak = float(p_single[-1].max())
    kept = list(range(0, e.INTERVALS + 1, STRIDE))
    if kept[-1] != e.INTERVALS:
        kept.append(e.INTERVALS)
    frames = [
        {
            "interval": t,
            "levels": rounded(double[t, SPAN[0] : SPAN[1]], 0),
            "single": rounded(p_single[t] / peak, 4),
            "double": rounded(p_double[t] / peak, 4),
        }
        for t in kept
    ]
    band, packets = out["band"], out["packets"]
    return {
        "kind": "time_slits",
        "card": "time-slits",
        "title": "The time slits on the law's real line",
        "line": (
            "The law's real line on a chain of 1,200 Nodes: two packets of light of 17 Nodes at k = pi / 4, the second the first's copy laid 60 Links behind (two slits in time, tau = d / v_g = 109.7 intervals apart at the probe), stepped by Rule3's line for light at the vacuum's paces over 700 intervals; at the probe Node 400 a body's two quadratures X and Y accumulate over the window and P^2 = X^2 + Y^2 across the band builds the fringes in frequency, the envelope the single packet's and the beats 4 cos^2(k(omega_d) d / 2); no click."
        ),
        "span": list(SPAN),
        "probe": e.PROBE,
        "lays": [e.COLUMN, e.COLUMN - d],
        "amplitude": amplitude,
        "intervals": e.INTERVALS,
        "grid": rounded(grid, 5),
        "carrier": round(omega, 5),
        "zeros": out["beats_zeros_k(omega)d=(2m+1)pi"],
        "minima": out["double_P2_minima"],
        "frames": frames,
        "numbers": [
            [
                "the wave",
                f"k = pi / 4 (lambda 8 Links), cos omega {band['cos_omega']:.4f}, omega {band['omega']:.4f} per interval, the period {band['period_intervals']:.2f} intervals",
            ],
            [
                "the group pace",
                f"v_g = (R / w) sin k / sin omega = {band['v_g']:.4f} Links per interval",
            ],
            [
                "the two packets",
                f"{packets['length_nodes']} Nodes each, the second the first's copy laid d = {packets['separation_links']} Links behind: tau = d / v_g = {packets['tau_arrival_intervals']:.2f} intervals between the two arrivals at the probe",
            ],
            [
                "the fringes' spacing",
                f"2 pi / tau = {out['fringe_spacing_in_omega_2pi_over_tau']:.4f} in omega_d; the beats' zeros at k(omega_d) d = (2 m + 1) pi: {', '.join(f'{z:.4f}' for z in out['beats_zeros_k(omega)d=(2m+1)pi'])}",
            ],
            ["the double's minima read", ", ".join(f"{m:.4f}" for m in out["double_P2_minima"])],
            [
                "the ratio against the beats",
                f"P^2 of the two packets over the single's against 4 cos^2(k(omega_d) d / 2), the largest difference {out['max_abs_ratio_minus_beats_where_envelope_above_2pc']:.4f} where the envelope stands above 2 percent of its peak (the width {out['envelope_width_above_2pc_in_omega']:.2f} in omega_d)",
            ],
            [
                "the single packet's peak",
                f"P^2 largest at omega_d = {out['single_P2_peak_at']:.4f}, the carrier {band['omega']:.4f}",
            ],
            [
                "the verdict",
                "works (the README's section E): the beats exact to 0.002 under the single slit's envelope by the band's line and the body's two quadratures; the engine lacks a shutter and a spectrometer that draws at the toy integers",
            ],
        ],
        "sources": [
            [
                "the script",
                "papers/one_rule/variants/scripts/e_time_slits.py, its output out/e_time_slits.json",
            ],
            [
                "the frames",
                f"the script's lay stepped by its line's coefficients with the chain's profile kept, one frame per {STRIDE} intervals over the Nodes {SPAN[0]} to {SPAN[1] - 1}, P^2 accumulated at the probe per interval and divided by the single packet's final peak",
            ],
            ["this page", "written by tools/look/line_page.py"],
        ],
    }


def plane(amplitude: int, omega: float, k: float, t: float, offsets: np.ndarray) -> list[int]:
    """A plane wave's levels along a row of Nodes at the interval t: A cos(omega t - k x), x the Node's distance from the row's reference, rounded as the script rounds the arms' levels."""
    return [int(round(amplitude * math.cos(omega * t - k * x))) for x in offsets]


def mach_zehnder() -> dict[str, Any]:
    """D: per arm difference Delta L = 0 to 4, the two arms' plane waves over the window of four periods (the script's sigma rule: the first arm A cos(omega tau) at the exit side's Node, the second A cos(omega tau - k Delta L), the levels rounded to integers), the exits' waves with the second splitter in (the sum and the difference over root 2) and out (each arm straight on), and the exit side's weights accumulated interval by interval by the engine's meeting_back.side_weights on the partial second moments (the window's moments asserted equal to the script's arms_moments, the final shares to its output)."""
    d_script, out = script("d_mach_zehnder"), output("d_mach_zehnder")
    from event_universe import meeting_back
    from event_universe.loader.draw import ports_of

    k = 2 * math.pi / d_script.WAVELENGTH
    omega = math.acos((2 + math.cos(k)) / 3)  # the band for light along an axis, as the script forms it
    steps = int(round(d_script.PERIODS * 2 * math.pi / omega))
    amplitude = d_script.AMPLITUDE
    all_ones, identity = meeting_back.gram_of([], 2), meeting_back.gram_of([IDENTITY], 2)
    bs_in = [list(p) for p in ports_of((1, 1), IDENTITY)]
    bs_out = [list(p) for p in ports_of((1, 0), IDENTITY)]
    sets = []
    for delta in range(5):
        phase = k * delta
        moments = [[0, 0], [0, 0]]
        frames = []
        arm1 = np.arange(ARM) - (ARM - 1)  # the distance behind the first arm's end at the splitter
        arm2 = np.arange(ARM + delta) - (ARM - 1)  # the second arm ends Delta L Links further on
        exits = np.arange(EXIT) + 1
        for t in range(steps + 1):
            if t < steps:
                for member in (0, 1):  # now and before, as the side books them
                    tau = t - member
                    sigma = [
                        int(round(amplitude * math.cos(omega * tau))),
                        int(round(amplitude * math.cos(omega * tau - phase))),
                    ]
                    for a in range(2):
                        for b in range(2):
                            moments[a][b] += sigma[a] * sigma[b]
            hermitian = [[(moments[a][b], 0) for b in range(2)] for a in range(2)]
            w_in = meeting_back.side_weights(hermitian, bs_in, all_ones)
            w_out = meeting_back.side_weights(hermitian, bs_out, all_ones)
            w_first = meeting_back.side_weights(hermitian, bs_in, identity)
            first = plane(amplitude, omega, k, t, arm1)
            second = plane(amplitude, omega, k, t, arm2)
            through_1 = plane(amplitude, omega, k, t, exits)
            through_2 = plane(amplitude, omega, k, t, exits + delta)
            cross = [
                int(round((a + b) / math.sqrt(2))) for a, b in zip(through_1, through_2, strict=True)
            ]
            straight = [
                int(round((a - b) / math.sqrt(2))) for a, b in zip(through_1, through_2, strict=True)
            ]
            frames.append(
                {
                    "interval": t,
                    "arm1": first,
                    "arm2": second,
                    "cross": cross,
                    "straight": straight,
                    "through": [through_1, through_2],
                    "in": w_in,
                    "out": w_out,
                    "first": w_first,
                }
            )
        assert moments == [[m for m, _i in row] for row in d_script.arms_moments(delta)]  # the script's
        row = out["two_part_form"][f"Delta L = {delta}"]
        total_in, total_out = sum(frames[-1]["in"]), sum(frames[-1]["out"])
        shares_in = [w / total_in for w in frames[-1]["in"]]
        shares_out = [w / total_out for w in frames[-1]["out"]]
        assert all(
            abs(a - b) < 1e-4
            for a, b in zip(shares_in, row["BS2 in, (1, 1): P(cross), P(straight)"], strict=True)
        )
        assert all(
            abs(a - b) < 1e-4
            for a, b in zip(shares_out, row["BS2 out, (1, 0): P(arm 1), P(arm 2)"], strict=True)
        )
        one_line = out["one_line_form_s_half"][f"Delta L = {delta}"]
        sets.append(
            {
                "delta": delta,
                "frames": frames,
                "one_line": [one_line["cross"], one_line["straight"]],
                "two_part_in": row["BS2 in, (1, 1): P(cross), P(straight)"],
                "two_part_out": row["BS2 out, (1, 0): P(arm 1), P(arm 2)"],
                "totals": row["sum of the exit side's weights, in and out"],
                "first": row["the exit side with a side after it (Gram identity), either port"],
            }
        )
    one = out["one_line_form_s_half"]
    return {
        "kind": "mach_zehnder",
        "card": "delayed-choice",
        "title": "The delayed choice on the law's real line",
        "line": (
            "The law's real line on the Mach-Zehnder (the rows against nature, row (l)): the record's plane wave at k = pi / 4 through the two arms, the second longer by Delta L Links, over a window of four periods; at the second splitter the arms add with their phases and the exit side's weights accumulate as the side books them (the engine's meeting_back.side_weights on the arms' second moments, exact in the integers), the cross exit 4 s (1 - s) cos^2(Delta / 2) at s = 1 / 2; with the splitter out the exits read the arms, one half each; the choice may enter at any interval before the record reaches the second splitter, the exits reading the configuration the record meets; no click."
        ),
        "amplitude": amplitude,
        "arm": ARM,
        "exit": EXIT,
        "steps": steps,
        "sets": sets,
        "numbers": [
            [
                "the wave",
                f"k = pi / 4 (lambda 8 Links); omega {omega:.4f} per interval, the period {2 * math.pi / omega:.2f} intervals; the window {steps} intervals, four periods",
            ],
            [
                "the splitter",
                out["splitter"]["the one-Node splitter's content for s = 1/2 at k = pi/4 (row (l))"],
            ],
            [
                "the one-line form, the cross exit",
                ", ".join(f"Delta L = {d}: {one[f'Delta L = {d}']['cross']}" for d in range(5))
                + " (4 s (1 - s) cos^2(Delta / 2) at s = 1 / 2, Delta = 2 pi Delta L / 8)",
            ],
            [
                "the two-part form, the splitter in",
                ", ".join(
                    f"Delta L = {d}: {out['two_part_form'][f'Delta L = {d}']['BS2 in, (1, 1): P(cross), P(straight)'][0]}"
                    for d in range(5)
                )
                + " (P(cross) by the exit side's weights at the setting (1, 1), the all-ones Gram)",
            ],
            [
                "the two-part form, the splitter out",
                ", ".join(
                    f"Delta L = {d}: {out['two_part_form'][f'Delta L = {d}']['BS2 out, (1, 0): P(arm 1), P(arm 2)']}"
                    for d in range(5)
                )
                + " (the exits read the arms at the setting (1, 0))",
            ],
            [
                "a side after it",
                "the exit side's two weights with a side after it are M11 + M22 each at either port, the identity pattern's Gram the identity: the marginal carries no cross term, the Gram theorem's corollary",
            ],
            [
                "the verdict",
                "works with one act (the README's section D): the timed declaration of a face or a body, the splitter entering at a declared interval; the statistics those of the configuration the record meets, nothing retro-written but the realised orbit",
            ],
        ],
        "sources": [
            [
                "the script",
                "papers/one_rule/variants/scripts/d_mach_zehnder.py, its output out/d_mach_zehnder.json",
            ],
            [
                "the frames",
                "the script's arms' levels per interval (A cos(omega tau) and A cos(omega tau - k Delta L), rounded) drawn as plane waves along the arms, the exits' waves their sum and difference over root 2 with the splitter in and each arm straight on with it out, the exit side's weights per interval by the engine's meeting_back.side_weights on the moments booked so far",
            ],
            ["this page", "written by tools/look/line_page.py"],
        ],
    }


def visibility(row: list[float], central: int = 6, minima: tuple[int, int] = (4, 8)) -> float:
    """The visibility at the blind central maximum against the blind first minima, the script's rule."""
    most, low = row[central] * len(minima), sum(row[m] for m in minima)
    return (most - low) / (most + low)


def marker() -> dict[str, Any]:
    """B: the screen's rows per region over the marker's angle, F[L] + F[U] + 2 cos theta F[L, U] from the script's three rows (the lower gap alone, the upper gap alone, the cross current), one frame per degree from 0 to 90 with the visibility and the distinguishability; the script's three marked rows asserted equal to the frames at their angles; the eraser's rows the script's output."""
    out = output("b_marker")
    lower, upper, cross = (np.array(out[key]) for key in ("lower_alone", "upper_alone", "cross_F[L,U]"))
    frames = []
    for degree in range(DEGREES + 1):
        theta = math.radians(degree)
        row = lower + upper + 2 * math.cos(theta) * cross
        frames.append(
            {
                "degrees": degree,
                "row": rounded(row, 2),
                "N": round(float(row.sum()), 2),
                "V": round(math.cos(theta), 4),
                "D": round(math.sin(theta), 4),
                "visibility": round(visibility(list(row)), 4),
            }
        )
    marked = out["marked_rows_bolometer"]
    for label, degree in (("unmarked (theta 0)", 0), ("fully marked (theta 90): cos theta 0", 90)):
        assert all(
            abs(a - b) <= 0.011 for a, b in zip(frames[degree]["row"], marked[label]["row"], strict=True)
        ), label
    half = lower + upper + 2 * 0.6 * cross  # the Pythagorean half angle (2, 1), cos theta 3 / 5
    half_row = marked["half marked, half angle (2, 1): cos theta 3/5"]["row"]
    assert all(abs(a - b) <= 0.011 for a, b in zip(half, half_row, strict=True))
    eraser, englert = out["eraser_conditional_rows"], out["englert_exact"]
    return {
        "kind": "marker",
        "card": "marker-eraser",
        "title": "The marker and the eraser on the law's real line",
        "line": (
            "The law's real line on the shipped two slits' board: the screen's row per region as the bolometer reads a two-part record whose parts are rotated at the two gaps by the marker's half angle, F[L] + F[U] + 2 cos theta F[L, U], beside the plain row (theta 0), the visibility cos theta and the distinguishability sin theta (Englert, V^2 + D^2 = 1 exact); below, the eraser's two conditional rows F[L + U] and F[L - U], fringes and anti-fringes, summing back to twice the incoherent row; no click."
        ),
        "regions": [f"screen_{index}" for index in range(len(lower))],
        "plain": rounded(lower + upper + 2 * cross, 2),
        "incoherent": rounded(lower + upper, 2),
        "frames": frames,
        "half_angle_degrees": round(math.degrees(math.acos(0.6)), 2),
        "eraser": {
            "plus": eraser["port_plus_F[L+U]"],
            "minus": eraser["port_minus_F[L-U]"],
            "sum": eraser["sum_over_ports"],
            "twice": eraser["twice_incoherent"],
            "visibilities": [
                eraser["visibility_plus"],
                eraser["visibility_minus"],
                eraser["visibility_sum"],
            ],
        },
        "numbers": [
            [
                "the rows",
                f"the two gaps' real line {out['N_two_gaps']} W_c over the window; the coherent sum of the paths F[L + U] {out['N_coherent_sum']}, the incoherent F[L] + F[U] {out['N_incoherent_sum']}",
            ],
            [
                "the marker's rows",
                "; ".join(
                    f"{label}: N {row['N']}, the visibility at 6 against 4 and 8 {row['visibility_6_vs_4_8']}"
                    for label, row in marked.items()
                ),
            ],
            [
                "Englert, exact",
                f"the half angle ({englert['half_angle_pair'][0]}, {englert['half_angle_pair'][1]}): P(+ | L) = {englert['P(+|L)']}, P(+ | U) = {englert['P(+|U)']}, D = {englert['D']}, V = {englert['V']}, V^2 + D^2 = {englert['V^2+D^2']}",
            ],
            [
                "the eraser",
                f"F[L + U] the fringes (the visibility {eraser['visibility_plus']}), F[L - U] the anti-fringes ({eraser['visibility_minus']}), their sum twice the incoherent row ({eraser['visibility_sum']})",
            ],
            [
                "the Gram theorem",
                "the last side's two ports sum to twice a first side's one port in exact integers at the central region (the script's gram_theorem_integers_central_region)",
            ],
            [
                "the verdict",
                "works with one act (the README's section B): the marking rotation of the parts on the gap's Links; Englert exact (V = 3/5, D = 4/5); the eraser by the one form and the write at the birth in the eraser-first order, the position-first order out of the engine's reach as built, named",
            ],
        ],
        "sources": [
            ["the script", "papers/one_rule/variants/scripts/b_marker.py, its output out/b_marker.json"],
            [
                "the frames",
                "the script's three rows (the lower gap alone, the upper gap alone, the symmetrised cross current) combined as the bolometer's F[L] + F[U] + 2 cos theta F[L, U], one frame per degree; the eraser's rows the output's",
            ],
            ["this page", "written by tools/look/line_page.py"],
        ],
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{LINE}}">
<style>
/* The page's own layout: the look pages' tokens (tools/look/page.py), every colour and size in this one block. */
:root {
  --bg: #0f1114; --panel: #171a20; --fg: #e9e7df; --muted: #9a9ea8; --line: #2e323a; --board: #07080a;
  --light: #4ade80; --matter: #6ea1f0; --blind: #b4b8c0; --flash: #ff5a1f; --focus: #5f97ea; --window: rgba(95, 151, 234, 0.2);
  --font-body: "IBM Plex Sans", system-ui, sans-serif; --font-mono: "IBM Plex Mono", ui-monospace, monospace;
  --text: 14px; --small: 12px; --title: 20px; --gap: 12px; --pad: 14px; --radius: 6px; --gutter: 16px;
  --stage-height: min(64vh, 620px); --frames-per-second: 12;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body { margin: 0; padding-inline: var(--gutter); padding-block: var(--pad); background: var(--bg); color: var(--fg); font: var(--text)/1.45 var(--font-body); }
h1 { font-size: var(--title); margin: 0; font-weight: 600; text-wrap: balance; }
h2 { font-size: var(--text); margin: 0 0 6px; font-weight: 600; }
header { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--gap); margin-bottom: 6px; }
header .verdict { font-family: var(--font-mono); color: var(--muted); }
p.line { margin: 0 0 var(--gap); color: var(--muted); max-width: 110ch; }
a { color: var(--focus); }
.page { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: var(--gap); align-items: start; }
.wide { grid-column: 1 / -1; }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: var(--pad); min-width: 0; }
.stage { position: relative; height: var(--stage-height); border-radius: var(--radius); overflow: hidden; background: var(--board); border: 1px solid var(--line); }
.stage canvas { display: block; width: 100%; height: 100%; }
.corner { position: absolute; top: var(--gap); left: var(--gap); font: 500 var(--small)/1.2 var(--font-mono); color: var(--muted); pointer-events: none; }
.controls { display: flex; flex-wrap: wrap; gap: 6px var(--gap); align-items: center; margin-top: var(--gap); font-size: var(--small); }
.controls:empty { display: none; }
.time { display: grid; grid-template-columns: auto minmax(12rem, 1fr) auto; align-items: center; gap: var(--gap); margin-top: var(--gap); }
.track input { width: 100%; margin: 0; }
.frame { font-family: var(--font-mono); font-variant-numeric: tabular-nums; min-width: 9ch; max-width: 60ch; text-align: right; font-size: var(--small); }
.lines { font: var(--small)/1.4 var(--font-mono); color: var(--muted); margin-top: 6px; min-height: 1.4em; }
button, select { font: inherit; color: var(--fg); background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 4px 10px; }
button:focus-visible, select:focus-visible, input:focus-visible { outline: 2px solid var(--focus); outline-offset: 1px; }
dl { display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: 4px var(--gap); margin: 0; font-size: var(--small); }
dt { color: var(--muted); } dd { margin: 0; font-family: var(--font-mono); overflow-wrap: anywhere; }
footer { margin-top: var(--gap); font-size: var(--small); color: var(--muted); }
@media (max-width: 640px) { dl { grid-template-columns: 1fr; } .time { grid-template-columns: auto 1fr; } .frame { grid-column: 1 / -1; text-align: left; } }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
</head>
<body>
<header><h1>{{TITLE}}</h1><span class="verdict">the law's real line, no click</span></header>
<p class="line">{{LINE}} <a href="../variants.html#{{CARD}}">The variants page's card</a>, with nature's experiment, the law's statement and the verdict.</p>
<div class="page">
  <section class="panel wide">
    <div class="stage"><canvas id="stage"></canvas><div class="corner">the law's real line</div></div>
    <div class="controls" id="controls"></div>
    <div class="time">
      <button type="button" id="play">Play</button>
      <div class="track"><input type="range" id="slider" min="0" value="0" step="1" aria-label="the frame"></div>
      <div class="frame" id="frame"></div>
    </div>
    <div class="lines" id="lines"></div>
  </section>
  <section class="panel"><h2>The numbers, the script's</h2><dl id="numbers"></dl></section>
  <section class="panel"><h2>The sources</h2><dl id="sources"></dl></section>
</div>
<footer>Universe24: the law's derivations under papers/one_rule/variants/, every number on this page the script's or its output's; the page draws them and computes nothing else.</footer>
<script id="data" type="application/json">{{DATA}}</script>
<script>
'use strict';
const DATA = JSON.parse(document.getElementById('data').textContent);
const byId = id => document.getElementById(id);
const token = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
const size = name => parseFloat(token(name));
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'})[c]);
const format = v => typeof v === 'number' ? (Number.isInteger(v) ? v.toLocaleString('en-US') : String(v)) : String(v);
const canvas = byId('stage'), ctx = canvas.getContext('2d');
let t = 0, playing = null, choice = {delta: 0, splitter: true};
let narrow = false, fontSize = 12, head = 46;  /* set per draw from the canvas's width: the layout and the type scale with it; the drawing starts under the corner caption */

/* The lists: the numbers and the sources, each a row. */
for (const [id, rows] of [['numbers', DATA.numbers], ['sources', DATA.sources]]) {
  byId(id).innerHTML = rows.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('');
}

/* The frames of the page shown: the time slits' and the marker's one list, the Mach-Zehnder's per arm difference. */
function frames() { return DATA.kind === 'mach_zehnder' ? DATA.sets[choice.delta].frames : DATA.frames; }
function last() { return frames().length - 1; }

/* The canvas at the device's pixels. */
function fit() {
  const r = canvas.parentElement.getBoundingClientRect(), s = window.devicePixelRatio || 1;
  canvas.width = Math.round(r.width * s); canvas.height = Math.round(r.height * s);
  ctx.setTransform(s, 0, 0, s, 0, 0);
  draw();
}

/* Drawing helpers: every text is cut to the width it is given, so nothing runs off the canvas at any width, and the long labels have a short form for a narrow canvas. */
function font(mono) { ctx.font = (mono ? '500 ' : '') + fontSize + 'px ' + (mono ? token('--font-mono') : token('--font-body')); }
function cut(s, max) {
  if (!(max > 0)) return '';
  if (ctx.measureText(s).width <= max) return s;
  let kept = s;
  while (kept.length > 1 && ctx.measureText(kept + '...').width > max) kept = kept.slice(0, -1);
  return kept + '...';
}
function text(s, x, y, colour, align, mono, max) {
  font(mono); ctx.fillStyle = colour || token('--muted'); ctx.textAlign = align || 'left'; ctx.textBaseline = 'alphabetic';
  ctx.fillText(max === undefined ? s : cut(s, max), x, y);
}
const pick = (long, short) => narrow ? short : long;
function box(x, y, w, h) { ctx.strokeStyle = token('--line'); ctx.lineWidth = 1; ctx.strokeRect(x + 0.5, y + 0.5, w, h); }
function polyline(points, colour, width, dashed) {
  if (!points.length) return;
  ctx.save(); ctx.strokeStyle = colour; ctx.lineWidth = width || 1.6; ctx.setLineDash(dashed ? [5, 4] : []);
  ctx.beginPath(); points.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.stroke(); ctx.restore();
}
function dashedLine(x0, y0, x1, y1, colour) { polyline([[x0, y0], [x1, y1]], colour, 1, true); }
function bars(x, y, w, h, values, high, colour, outline) {
  const n = values.length, slot = w / n, bw = slot * 0.62;
  values.forEach((v, k) => {
    const bh = Math.max(0, v) / high * h, bx = x + slot * (k + 0.5) - bw / 2, by = y + h - bh;
    if (outline) { ctx.save(); ctx.strokeStyle = colour; ctx.lineWidth = 1.2; ctx.setLineDash([4, 3]); ctx.strokeRect(bx + 0.5, by + 0.5, bw, bh); ctx.restore(); }
    else { ctx.fillStyle = colour; ctx.fillRect(bx, by, bw, bh); }
  });
}
function glowNodes(x, y, cell, levels, amplitude, colour) {
  /* a row of Nodes as squares, each glowing by its level squared against the amplitude squared (the look pages' glow by the wave's intensity) */
  levels.forEach((v, k) => {
    const a = Math.min(1, (v / amplitude) ** 2);
    ctx.fillStyle = token('--panel'); ctx.fillRect(x + k * cell, y, cell - 1, cell - 1);
    ctx.globalAlpha = 0.15 + 0.85 * a; ctx.fillStyle = colour; ctx.fillRect(x + k * cell + 1, y + 1, cell - 3, cell - 3); ctx.globalAlpha = 1;
  });
}

/* E: the chain's levels over the Nodes drawn and, below, P^2 across the band up to the frame's interval. */
function drawTimeSlits(W, H) {
  const f = frames()[t], pad = 10, left = narrow ? 40 : 52, top = head, split = Math.round(H * 0.52), fg = token('--fg'), muted = token('--muted'), blind = token('--blind');
  const gw = W - left - pad, gh = split - top - 30, A = DATA.amplitude, n = f.levels.length, d = DATA.lays[0] - DATA.lays[1];
  const px = i => left + i / (n - 1) * gw, py = v => top + (1 - v / A) / 2 * gh;
  box(left, top, gw, gh);
  text(pick("the chain: the record's level per Node, the two packets (the second the first's copy laid " + d + " Links behind)", "the chain: the level per Node, the two packets"), left, top - 8, fg, 'left', false, gw);
  text(format(A), left - 4, top + 10, muted, 'right', true, left - 6); text('-' + format(A), left - 4, top + gh, muted, 'right', true, left - 6);
  text('Node ' + DATA.span[0], left, split - 12, muted, 'left', true, gw / 2 - 4); text('Node ' + (DATA.span[1] - 1), left + gw, split - 12, muted, 'right', true, gw / 2 - 4);
  dashedLine(px(0), py(0), px(n - 1), py(0), token('--line'));
  const probe = px(DATA.probe - DATA.span[0]);
  dashedLine(probe, top, probe, top + gh, blind);
  text(pick('the probe, the Node ' + DATA.probe, 'probe ' + DATA.probe), probe + 4, top + 12, blind, 'left', true, left + gw - probe - 6);
  for (const lay of DATA.lays) { const lx = px(lay - DATA.span[0]); dashedLine(lx, top + gh - 10, lx, top + gh, token('--window')); }
  const lx = px(DATA.lays[1] - DATA.span[0]);
  text(pick('the two slits in time: the lays at the Nodes ' + DATA.lays[1] + ' and ' + DATA.lays[0], 'the lays at ' + DATA.lays[1] + ' and ' + DATA.lays[0]), lx, top + gh - 14, muted, 'left', true, probe - lx - 8);
  polyline(f.levels.map((v, i) => [px(i), py(v)]), token('--light'), 1.4);
  /* the spectrum */
  const stop = split + 26, sh = H - stop - 30, grid = DATA.grid, m = grid.length, high = 4.2, span = grid[m - 1] - grid[0];
  const qx = i => left + i / (m - 1) * gw, qy = v => stop + (1 - Math.min(v, high) / high) * sh;
  box(left, stop, gw, sh);
  text(pick("P^2 = X^2 + Y^2 at the probe up to this interval, over the body's resonance omega_d (the single packet dashed, its final peak 1; the two packets solid)", 'P^2 at the probe up to this interval (single dashed, two packets solid)'), left, stop - 8, fg, 'left', false, gw);
  text('4', left - 4, stop + 10, muted, 'right', true, left - 6); text('0', left - 4, stop + sh, muted, 'right', true, left - 6);
  text('omega_d ' + grid[0].toFixed(3), left, H - 12, muted, 'left', true, gw / 2 - 4); text(grid[m - 1].toFixed(3), left + gw, H - 12, muted, 'right', true, gw / 2 - 4);
  const cx = qx((DATA.carrier - grid[0]) / span * (m - 1));
  dashedLine(cx, stop, cx, stop + sh, token('--window'));
  text(pick('the carrier ' + DATA.carrier.toFixed(4), 'carrier'), cx + 4, stop + sh - 6, muted, 'left', true, left + gw - cx - 6);
  for (const z of DATA.zeros) { const zx = qx((z - grid[0]) / span * (m - 1)); dashedLine(zx, stop + sh - 12, zx, stop + sh, blind); }
  text(pick("the beats' zeros, k(omega_d) d = (2 m + 1) pi", "the beats' zeros"), left + gw - 4, stop + sh - 18, blind, 'right', true, gw * 0.5);
  polyline(f.single.map((v, i) => [qx(i), qy(v)]), blind, 1.2, true);
  polyline(f.double.map((v, i) => [qx(i), qy(v)]), token('--light'), 1.6);
  byId('frame').textContent = 'interval ' + f.interval + ' of ' + DATA.intervals;
  const mid = Math.round((m - 1) / 2);
  byId('lines').textContent = 'P^2 at the carrier: the single packet ' + f.single[mid].toFixed(3) + ', the two packets ' + f.double[mid].toFixed(3) + " of the single's final peak; the second packet arrives at the probe about " + d + ' / v_g intervals after the first';
}

/* D: the two arms and the exits as rows of glowing Nodes, the exit side's weights booked so far as bars over the window's total. */
function drawMachZehnder(W, H) {
  const set = DATA.sets[choice.delta], f = set.frames[t], final = set.frames[set.frames.length - 1], A = DATA.amplitude, pad = 12;
  const fg = token('--fg'), muted = token('--muted'), colour = token('--light'), stacked = W < 760;
  const panel = stacked ? 0 : 200, cells = DATA.arm + 4 + DATA.exit + 3;
  const cell = Math.max(5, Math.min(18, Math.floor((W - 2 * pad - panel - (stacked ? 0 : pad)) / cells)));
  const x0 = pad + 2 * cell, rowGap = Math.max(3 * cell, 40), yTop = head + 14, yBottom = yTop + rowGap + cell, below = yBottom + cell + 14;
  const inOut = choice.splitter ? 'in' : 'out', links = set.delta + (set.delta === 1 ? ' Link' : ' Links');
  text(pick("the record's plane wave through the two arms, Delta L = " + links + '; the second splitter ' + inOut, 'Delta L = ' + links + '; the splitter ' + inOut), pad, head - 8, fg, 'left', false, W - 2 * pad);
  /* the first splitter, the two arms, the second splitter at the first arm's end */
  ctx.fillStyle = token('--blind'); ctx.fillRect(x0 - 1.5 * cell, yTop, cell * 0.5, yBottom - yTop + cell);
  text('BS1', x0 - 1.25 * cell, below, muted, 'center', true, 3 * cell + 12);
  const xs = x0 + DATA.arm * cell + cell * 0.5;
  glowNodes(x0, yTop, cell, f.arm2, A, colour); glowNodes(x0, yBottom, cell, f.arm1, A, colour);
  text('arm 2, ' + (DATA.arm + set.delta) + ' Nodes', x0 + 2 * cell, yTop - 6, muted, 'left', true, xs - x0 - 2 * cell - 4);
  text('arm 1, ' + DATA.arm + ' Nodes', x0 + 2 * cell, below, muted, 'left', true, xs - x0 - 2.5 * cell - 4);
  if (choice.splitter) { ctx.fillStyle = token('--blind'); ctx.fillRect(xs, yTop - cell * 0.5, cell * 0.5, yBottom - yTop + 2 * cell); }
  else { ctx.save(); ctx.strokeStyle = token('--blind'); ctx.setLineDash([3, 3]); ctx.strokeRect(xs + 0.5, yTop - cell * 0.5 + 0.5, cell * 0.5, yBottom - yTop + 2 * cell); ctx.restore(); }
  /* the exits to the right of the second splitter, the second arm's extra Nodes reaching past it */
  const xe = xs + cell * 1.5 + set.delta * cell, right = (stacked ? W : W - panel) - pad;
  const upper = choice.splitter ? f.cross : f.through[1], lower = choice.splitter ? f.straight : f.through[0];
  glowNodes(xe, yTop, cell, upper, A, colour); glowNodes(xe, yBottom, cell, lower, A, colour);
  text('BS2 ' + inOut, xs + cell, (yTop + yBottom) / 2 + cell, muted, 'left', true, right - xs - cell);
  text(choice.splitter ? pick('the cross exit, (arm 1 + arm 2) / root 2', 'cross: (1 + 2) / root 2') : pick('exit 2: arm 2 straight on', 'exit 2: arm 2'), xe, yTop - 6, muted, 'left', true, right - xe);
  text(choice.splitter ? pick('the straight exit, (arm 1 - arm 2) / root 2', 'straight: (1 - 2) / root 2') : pick('exit 1: arm 1 straight on', 'exit 1: arm 1'), xe, below, muted, 'left', true, right - xe);
  /* the weights booked so far over the window's total, the two bars growing to the script's final shares (dashed) */
  const w = choice.splitter ? f.in : f.out, total = (choice.splitter ? final.in : final.out).reduce((a, b) => a + b, 0) || 1, shares = [w[0] / total, w[1] / total];
  const blind = choice.splitter ? set.two_part_in : set.two_part_out;
  const bx = stacked ? pad + 36 : W - pad - panel + 20, by = stacked ? below + 30 : head + 14, bw = stacked ? W - 2 * pad - 36 : panel - 20, bh = Math.max(40, H - by - 44);
  box(bx, by, bw, bh);
  text('the weights booked so far', bx, by - 8, fg, 'left', false, bw);
  text('1', bx - 4, by + 10, muted, 'right', true, 30); text('0', bx - 4, by + bh, muted, 'right', true, 30);
  bars(bx, by, bw, bh, shares, 1, colour, false); bars(bx, by, bw, bh, blind, 1, token('--blind'), true);
  text(choice.splitter ? 'cross' : 'arm 1', bx + bw * 0.25, by + bh + 14, muted, 'center', true, bw / 2 - 4);
  text(choice.splitter ? 'straight' : 'arm 2', bx + bw * 0.75, by + bh + 14, muted, 'center', true, bw / 2 - 4);
  shares.forEach((s, k) => text(s.toFixed(3), bx + bw * (0.25 + 0.5 * k), Math.max(by + 12, by + bh * (1 - s) - 4), fg, 'center', true, bw / 2 - 4));
  byId('frame').textContent = 'interval ' + f.interval + ' of ' + DATA.steps;
  byId('lines').textContent = (choice.splitter
    ? 'the splitter in: the weights booked so far ' + format(w[0]) + ' and ' + format(w[1]) + " of the window's " + format(total) + ' (the shares so far ' + shares.map(s => s.toFixed(3)).join(', ') + '); P(cross) by the one-line form 4 s (1 - s) cos^2(Delta / 2) at s = 1 / 2 is ' + set.one_line[0] + ', by the two-part form ' + set.two_part_in[0] + ' (dashed)'
    : 'the splitter out: the exits read the arms; the weights booked so far ' + format(w[0]) + ' and ' + format(w[1]) + " of the window's " + format(total) + ' (the shares so far ' + shares.map(s => s.toFixed(3)).join(', ') + '); P(arm 1), P(arm 2) = ' + set.two_part_out.join(', ') + ' by the two-part form (dashed)')
    + '; with a side after this one its two weights are ' + format(f.first[0]) + ' each so far (the Gram identity)';
}

/* B: the plain row beside the marked row at the angle, and the eraser's two rows summing back. */
function drawMarker(W, H) {
  const f = frames()[t], pad = 10, left = narrow ? 34 : 40, n = DATA.regions.length, top = head, gap = narrow ? 14 : 24, fg = token('--fg'), muted = token('--muted');
  const half = (W - left - pad - gap) / 2, gh = Math.round(H * 0.34), high = Math.max(...DATA.plain, ...DATA.eraser.sum) * 1.05, every = narrow ? 2 : 1;
  box(left, top, half, gh); box(left + half + gap, top, half, gh);
  text(pick('the plain row, theta 0: F[L] + F[U] + 2 F[L, U] per region (W_c over the window)', 'plain, theta 0'), left, top - 8, fg, 'left', false, half);
  text(pick('the marked row at theta = ' + f.degrees + ' degrees: F[L] + F[U] + 2 cos theta F[L, U] (the plain row dashed)', 'marked, theta ' + f.degrees + ' deg'), left + half + gap, top - 8, fg, 'left', false, half);
  text(format(Math.round(high)), left - 4, top + 10, muted, 'right', true, left - 6); text('0', left - 4, top + gh, muted, 'right', true, left - 6);
  bars(left, top, half, gh, DATA.plain, high, token('--blind'), false);
  bars(left + half + gap, top, half, gh, f.row, high, token('--light'), false);
  bars(left + half + gap, top, half, gh, DATA.plain, high, token('--blind'), true);
  const slot = half / n;
  DATA.regions.forEach((name, k) => { if (k % every) return; text(String(k), left + slot * (k + 0.5), top + gh + 12, muted, 'center', true, slot * every); text(String(k), left + half + gap + slot * (k + 0.5), top + gh + 12, muted, 'center', true, slot * every); });
  /* the eraser */
  const etop = top + gh + 44, eh = H - etop - 30, ew = W - left - pad, eslot = ew / n, bw = eslot * 0.62;
  box(left, etop, ew, eh);
  text(pick("the eraser's two conditional rows: F[L + U] the fringes (green) and F[L - U] the anti-fringes (orange), stacked; their sum twice the incoherent row F[L] + F[U] (dashed)", 'the eraser: F[L + U] (green) + F[L - U] (orange) = 2 (F[L] + F[U]) (dashed)'), left, etop - 8, fg, 'left', false, ew);
  text(format(Math.round(high)), left - 4, etop + 10, muted, 'right', true, left - 6); text('0', left - 4, etop + eh, muted, 'right', true, left - 6);
  DATA.eraser.plus.forEach((v, k) => {
    const x = left + eslot * (k + 0.5) - bw / 2, hp = v / high * eh, hm = DATA.eraser.minus[k] / high * eh;
    ctx.fillStyle = token('--light'); ctx.fillRect(x, etop + eh - hp, bw, hp);
    ctx.fillStyle = token('--flash'); ctx.fillRect(x, etop + eh - hp - hm, bw, hm);
    if (k % every === 0) text(String(k), left + eslot * (k + 0.5), etop + eh + 12, muted, 'center', true, eslot * every);
  });
  bars(left, etop, ew, eh, DATA.eraser.twice, high, token('--blind'), true);
  byId('frame').textContent = 'theta ' + f.degrees + ' degrees';
  byId('lines').textContent = 'V = cos theta = ' + f.V.toFixed(4) + ', D = sin theta = ' + f.D.toFixed(4) + ', V^2 + D^2 = ' + (f.V * f.V + f.D * f.D).toFixed(4) + "; the row's N " + f.N + ', the visibility at the region 6 against 4 and 8 ' + f.visibility.toFixed(3) + ' (the Pythagorean half angle (2, 1) at ' + DATA.half_angle_degrees + " degrees, cos theta 3 / 5; the eraser's visibilities " + DATA.eraser.visibilities.join(', ') + ')';
}

function draw() {
  const W = canvas.width / (window.devicePixelRatio || 1), H = canvas.height / (window.devicePixelRatio || 1);
  narrow = W < 600; fontSize = narrow ? 10 : 12;
  ctx.fillStyle = token('--board'); ctx.fillRect(0, 0, W, H);
  if (DATA.kind === 'time_slits') drawTimeSlits(W, H);
  else if (DATA.kind === 'mach_zehnder') drawMachZehnder(W, H);
  else drawMarker(W, H);
  byId('slider').value = t;
}

/* The controls: the Mach-Zehnder's arm difference and its second splitter, in or out at any frame. */
if (DATA.kind === 'mach_zehnder') {
  const controls = byId('controls');
  const label = document.createElement('label'); label.textContent = 'the arm difference Delta L ';
  const select = document.createElement('select');
  DATA.sets.forEach(set => { const o = document.createElement('option'); o.value = set.delta; o.textContent = set.delta + (set.delta === 1 ? ' Link' : ' Links') + ' (the cross exit ' + set.one_line[0] + ')'; select.append(o); });
  select.addEventListener('change', () => { choice.delta = Number(select.value); draw(); });
  label.append(select); controls.append(label);
  const toggle = document.createElement('button'); toggle.type = 'button'; toggle.textContent = 'the second splitter: in (take it out)';
  toggle.addEventListener('click', () => { choice.splitter = !choice.splitter; toggle.textContent = choice.splitter ? 'the second splitter: in (take it out)' : 'the second splitter: out (put it in)'; draw(); });
  controls.append(toggle);
  const note = document.createElement('span'); note.textContent = "the choice may be made at any frame: the exits read the configuration the record meets at the second splitter's place";
  controls.append(note);
}

/* The time: one frame per slider step, play at the frames per second, the arrow keys stepping. */
const slider = byId('slider'); slider.max = last();
slider.addEventListener('input', () => { t = Number(slider.value); draw(); });
byId('play').addEventListener('click', () => {
  if (playing) { clearInterval(playing); playing = null; byId('play').textContent = 'Play'; return; }
  if (t >= last()) t = 0;
  byId('play').textContent = 'Pause';
  playing = setInterval(() => { if (t >= last()) { clearInterval(playing); playing = null; byId('play').textContent = 'Play'; return; } t++; draw(); }, 1000 / size('--frames-per-second'));
});
document.addEventListener('keydown', e => { if (e.target.tagName === 'INPUT' && e.target.type !== 'range') return; if (e.key === 'ArrowRight' && t < last()) { t++; draw(); } if (e.key === 'ArrowLeft' && t > 0) { t--; draw(); } });
window.addEventListener('resize', fit);
fit();
</script>
</body>
</html>
"""


def embedded(value: object) -> str:
    """A value as compact JSON safe inside a script element."""
    return json.dumps(value, separators=(",", ":")).replace("</", "<\\/")


def page(data: dict[str, Any]) -> str:
    """The page's HTML from one page's data, the template's four marks filled."""
    return (
        TEMPLATE.replace("{{TITLE}}", data["title"])
        .replace("{{LINE}}", data["line"].replace('"', "&quot;"))
        .replace("{{CARD}}", data["card"])
        .replace("{{DATA}}", embedded(data))
    )


BUILDERS = {
    "b": ("b_marker", marker),
    "d": ("d_mach_zehnder", mach_zehnder),
    "e": ("e_time_slits", time_slits),
}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=PAGES, help="the folder of the pages written")
    parser.add_argument("--only", choices=sorted(BUILDERS), default=None, help="one page alone")
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    for key, (name, builder) in BUILDERS.items():
        if args.only and key != args.only:
            continue
        data = builder()
        target = args.out / f"{name}.html"
        html = page(data)
        assert "{{" not in html and html.isascii(), name
        target.write_text(html, encoding="utf-8")
        frames = sum(len(s["frames"]) for s in data["sets"]) if "sets" in data else len(data["frames"])
        print(json.dumps({"page": str(target), "frames": frames, "bytes": len(html)}))


if __name__ == "__main__":
    main()
