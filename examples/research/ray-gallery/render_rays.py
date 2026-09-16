"""Compose one animated GIF: eight panels, one ray kind each, advancing tick by tick.

Input: the per-tick JSON that record_ticks.py read back from the recorded runs
(verified against the runner's own frames). One GIF frame per recorded tick;
panels whose run is shorter hold their final recorded state (marked "held").
Nothing is interpolated, no trajectory is invented. Arrows are rays resident at
a Node (the recorded state after each tick has every ray at a Node; nothing is
in flight at frame time), squares are records, shaded cells are octant field
stock or claims. The picture is a faithful drawing of recorded state; it is not
evidence of physics.

Run:  PYTHONPATH=src python examples/research/ray-gallery/render_rays.py --output DIR
      (after record_ticks.py has written DIR/ticks/; needs the render extra: matplotlib, Pillow)
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import worlds  # noqa: E402
from matplotlib import cm  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BACKGROUND = "#0b1020"
PANEL_BG = "#101830"
INK = "#e8ecf4"
DIM = "#8a95b3"
LATTICE = "#2a3a5f"
RAY = "#ffd166"  # unphased ray
HOMING = "#ffffff"  # homing ray (claim and gather): white, a hue the phase wheel never produces
LOAD = (0.35, 0.55, 1.0)  # computation field halo (panel 7), drawn translucent under the rays
EMITTER = "#ff8a3d"  # records that emit (lamps, sources, charge, particle)
ABSORBER = "#4c5c80"  # records that absorb or detect, filled toward white by stock
MIRROR = "#d8dfec"
MASS = "#d05cff"
CLAIM = "#a06cff"
WAIT = "#ff5c5c"
BOND = "#ff6bd6"
FRAME_MS = 450
FINAL_MS = 4000
STILL_TICKS = ("first", 8, 20, "final")

EMITTER_TYPES = {
    "lamp",
    "lamp_x",
    "lamp_y",
    "lamp_diag",
    "lamp_a",
    "lamp_b",
    "source_alice",
    "source_bob",
    "reference_alice",
    "reference_bob",
    "charge",
    "particle",
}
LABELS = {
    "lamp": "lamp",
    "lamp_x": "lamp",
    "lamp_y": "lamp",
    "lamp_diag": "lamp",
    "lamp_a": "lamp A",
    "lamp_b": "lamp B",
    "source_alice": "source A+B",
    "source_bob": None,
    "reference_alice": "ref lamp",
    "reference_bob": "ref lamp",
    "charge": "charge",
    "particle": "particle",
    "screen": "screen",
    "plus_alice": "+A",
    "minus_alice": "−A",
    "plus_bob": "+B",
    "minus_bob": "−B",
    "mirror": "mirror",
    "mass body": "mass",
}
LEGENDS = {
    "1-outward-halo": "held charge injects 216/tick; cells = octant stock, white arrow = net octant direction. "
    "Records (not rays): charge.",
    "2-straight-rays": "three funded lamps, headings [1,0,0] [0,1,0] [2,1,0]; rays cross at a Node without responding. "
    "Records (not rays): lamps.",
    "3-double-slit": "lamps A and B in phase, 8 phase steps, +2 per link; the fringe builds in the screen stock. "
    "Records (not rays): lamps, 9 screen absorbers.",
    "4-bonded-pair": "one Node births a pair per tick (dashed = equal bond code); +A/+B ask the registry, "
    "−A/−B take what walks on. Records (not rays): sources, detectors.",
    "5-claim-gather": "particle dissolves at pace 1/4; the screen's click opens a claim (violet cells, small arrow = "
    "way home); white = homing ray. Records (not rays): particle, screen.",
    "6-mirror-cavity": "lamp fires 8 quanta each way, once; a mirror absorbs a ray for one tick and re-emits it "
    "along the mirrored heading at the carried phase. Records (not rays): lamp, mirrors.",
    "7-ray-delay": "blue shade = the mass's outward computation field; red ring k = ray_wait, rays held k cycles. "
    "Records (not rays): lamp, screen, mass body.",
    "8-lottery-detector": "a reference lamp lands a quantum per tick at +A/+B at the setting phase; the lottery takes or "
    "passes each arriving ray. Records (not rays): sources, reference lamps, detectors.",
}


def load(out: Path) -> list[dict]:
    return [
        json.loads((out / "ticks" / f"{p['key']}.json").read_text(encoding="utf-8"))
        for p in worlds.PANELS
    ]


def phase_color(phase: int, steps: int):
    return cm.hsv(phase / steps)


def draw_panel(ax, panel: dict, frame: dict, held: bool, scales: dict) -> None:
    shape = panel["shape"]
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(-0.75, shape[0] - 0.25)
    ax.set_ylim(-0.75, shape[1] - 0.25)
    ax.set_aspect("equal")
    ax.set_axis_off()
    xs = [x for x in range(shape[0]) for _ in range(shape[1])]
    ys = [y for _ in range(shape[0]) for y in range(shape[1])]
    ax.scatter(xs, ys, s=2.5, c=LATTICE, linewidths=0, zorder=1)
    cell_pt = scales["cell_pt"]
    # Octant field stock (panel 1 and the computation field of panel 7).
    vmax = scales["cell_vmax"]
    for x, y, _name, total, dx, dy in frame["cells"]:
        level = math.sqrt(total / vmax) if vmax else 0.0
        if panel["kind"] == "octants":
            color = cm.magma(0.15 + 0.8 * level)
            ax.scatter(
                [x],
                [y],
                s=(cell_pt * 0.95) ** 2,
                marker="s",
                c=[color],
                linewidths=0,
                alpha=0.9,
                zorder=2,
            )
        else:
            # A computation field under rays: one translucent hue, so the rays stay on top.
            ax.scatter(
                [x],
                [y],
                s=(cell_pt * 0.95) ** 2,
                marker="s",
                c=[(*LOAD, 0.08 + 0.5 * level)],
                linewidths=0,
                zorder=2,
            )
        if panel["kind"] == "octants":
            norm = math.hypot(dx, dy)
            if norm:
                length = 0.18 + 0.24 * level
                ax.arrow(
                    x - dx / norm * length / 2,
                    y - dy / norm * length / 2,
                    dx / norm * length,
                    dy / norm * length,
                    head_width=0.13,
                    head_length=0.12,
                    length_includes_head=True,
                    color="white",
                    alpha=0.75,
                    lw=0.6,
                    zorder=3,
                )
    # Claims: every Node that knows a train was captured, with the way home.
    for x, y, parent, root, _train, _since in frame["claims"]:
        ax.scatter(
            [x], [y], s=(cell_pt * 0.95) ** 2, marker="s", c=[CLAIM], alpha=0.22, linewidths=0, zorder=2
        )
        if root:
            ax.scatter(
                [x],
                [y],
                s=(cell_pt * 1.1) ** 2,
                marker="s",
                facecolors="none",
                edgecolors=CLAIM,
                linewidths=1.2,
                zorder=6,
            )
        else:
            px, py = worlds_port(parent)
            ax.arrow(
                x,
                y,
                px * 0.28,
                py * 0.28,
                head_width=0.1,
                head_length=0.09,
                length_includes_head=True,
                color=CLAIM,
                alpha=0.55,
                lw=0.5,
                zorder=3,
            )
    # Records: squares, labelled; absorbers fill toward white with stock.
    absorber_max = scales["absorber_max"]
    labelled = set()
    for x, y, kind, values, _extra in frame["records"]:
        stock = values.get(panel["field"], [0])[0] if panel["field"] in values else None
        if kind == "mirror":
            face = MIRROR if stock else "#5a6478"
            ax.scatter(
                [x],
                [y],
                s=(cell_pt * 1.05) ** 2,
                marker="s",
                c=[face],
                edgecolors="white",
                linewidths=1.0,
                zorder=5,
            )
            if stock:
                ax.text(
                    x,
                    y,
                    str(stock),
                    ha="center",
                    va="center",
                    fontsize=5.5,
                    color="black",
                    zorder=7,
                    fontweight="bold",
                )
        elif kind == "mass body":
            ax.scatter(
                [x],
                [y],
                s=(cell_pt * 1.05) ** 2,
                marker="s",
                c=[MASS],
                edgecolors="white",
                linewidths=0.8,
                zorder=5,
            )
        elif kind in EMITTER_TYPES:
            ax.scatter(
                [x],
                [y],
                s=(cell_pt * 1.0) ** 2,
                marker="s",
                c=[EMITTER],
                edgecolors="white",
                linewidths=0.8,
                zorder=5,
            )
        else:
            level = min(1.0, stock / absorber_max) if absorber_max and stock else 0.0
            base = matplotlib.colors.to_rgb(ABSORBER)
            face = tuple(b + (1.0 - b) * level for b in base)
            ax.scatter(
                [x],
                [y],
                s=(cell_pt * 1.0) ** 2,
                marker="s",
                c=[face],
                edgecolors="white",
                linewidths=0.8,
                zorder=5,
            )
            if stock:
                ax.text(
                    x,
                    y,
                    str(stock),
                    ha="center",
                    va="center",
                    fontsize=5.2,
                    color="black" if level > 0.45 else "white",
                    zorder=7,
                )
        label = LABELS.get(kind, kind)
        if kind == "screen" and panel["key"] == "3-double-slit":
            label = "screen ×9" if y == shape[1] // 2 else None
        if label and (x, y) not in labelled:
            labelled.add((x, y))
            if kind == "screen" and panel["key"] == "3-double-slit":
                ax.text(
                    x + 0.7,
                    y,
                    label,
                    ha="left",
                    va="center",
                    fontsize=5.6,
                    color=INK,
                    zorder=8,
                    bbox=dict(boxstyle="round,pad=0.12", fc=BACKGROUND, ec="none", alpha=0.6),
                )
            else:
                ax.text(
                    x,
                    y + 0.62,
                    label,
                    ha="center",
                    va="bottom",
                    fontsize=5.6,
                    color=INK,
                    zorder=8,
                    bbox=dict(boxstyle="round,pad=0.12", fc=BACKGROUND, ec="none", alpha=0.6),
                )
    # Ray wait registers.
    for x, y, k in frame["waits"]:
        ax.scatter(
            [x],
            [y],
            s=(cell_pt * 1.25) ** 2,
            marker="o",
            facecolors="none",
            edgecolors=WAIT,
            linewidths=1.1,
            zorder=6,
        )
        ax.text(
            x,
            y + 0.58,
            f"k={k}",
            ha="center",
            va="bottom",
            fontsize=5.6,
            color=WAIT,
            zorder=8,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.1", fc=BACKGROUND, ec="none", alpha=0.7),
        )
    # Rays: one arrow each, tail at the Node, length by amount, hue by phase.
    amax = scales["ray_amax"]
    steps = panel["phase_steps"]
    groups: dict[tuple, list] = {}
    for ray in frame["rays"]:
        groups.setdefault((ray[0], ray[1], ray[2], ray[3], ray[6]), []).append(ray)
    bonds: dict[int, list] = {}
    for rays in groups.values():
        n = len(rays)
        for i, (x, y, hx, hy, amount, phase, homing, wait, bond, _train, parent_vec) in enumerate(rays):
            if homing and parent_vec is not None and any(parent_vec):
                dx, dy = parent_vec
            elif homing:
                dx, dy = 0, 0
            else:
                dx, dy = hx, hy
            norm = math.hypot(dx, dy)
            length = min(0.78, 0.26 + 0.46 * math.sqrt(amount / amax)) if amax else 0.3
            lw = 0.7 + 1.6 * math.sqrt(amount / amax) if amax else 0.8
            color = (
                HOMING if homing else (phase_color(phase, steps) if steps and phase is not None else RAY)
            )
            jitter = 0.09 * (i - (n - 1) / 2)
            if norm:
                ox, oy = -dy / norm * jitter, dx / norm * jitter
                ax.arrow(
                    x + ox,
                    y + oy,
                    dx / norm * length,
                    dy / norm * length,
                    head_width=0.17,
                    head_length=0.15,
                    length_includes_head=True,
                    color=color,
                    lw=lw,
                    alpha=0.95,
                    zorder=9,
                )
            else:
                ax.scatter(
                    [x + jitter],
                    [y],
                    s=(cell_pt * 0.5) ** 2,
                    marker="o",
                    facecolors="none",
                    edgecolors=color,
                    linewidths=lw,
                    zorder=9,
                )
            if homing:
                ax.scatter(
                    [x + (ox if norm else jitter)],
                    [y + (oy if norm else 0)],
                    s=(cell_pt * 0.42) ** 2,
                    marker="o",
                    facecolors="none",
                    edgecolors=HOMING,
                    linewidths=0.8,
                    zorder=9,
                )
            if wait and panel["key"] == "5-claim-gather" and not homing:
                pass
            if bond:
                bonds.setdefault(bond, []).append(
                    (x + (ox if norm else jitter), y + (oy if norm else 0))
                )
    for code, points in bonds.items():
        if len(points) == 2:
            (x1, y1), (x2, y2) = points
            ax.plot([x1, x2], [y1, y2], ls=(0, (3, 2)), lw=0.8, color=BOND, alpha=0.8, zorder=4)
            ax.text(
                (x1 + x2) / 2,
                (y1 + y2) / 2 + 0.22,
                f"bond …{str(code)[-2:]}",
                ha="center",
                va="bottom",
                fontsize=5.2,
                color=BOND,
                zorder=8,
            )
    if held:
        ax.text(
            -0.45,
            shape[1] - 0.45,
            "held: run ended",
            ha="left",
            va="top",
            fontsize=6,
            color=DIM,
            zorder=10,
            bbox=dict(boxstyle="round,pad=0.15", fc=BACKGROUND, ec=DIM, lw=0.4),
        )


def worlds_port(port: int) -> tuple[int, int]:
    return [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0), (0, 0)][port]


def footer(panel: dict, frame: dict, held: bool) -> tuple[str, str]:
    t = frame["totals"]
    field = panel["field"]
    tick = f"tick {frame['tick']}/{panel['ticks']}" + (" (held)" if held else "")
    flag = "balanced ✓" if frame["balanced"] else "NOT balanced"
    if panel["key"] == "1-outward-halo":
        line1 = f"{tick} · {flag} · {field}: {t['in_world']} in field + {t['escaped']} escaped = {t['injected']} injected"
    else:
        line1 = (
            f"{tick} · {flag} · {field}: {t['rays']} in rays + {t['records']} in records + {t['escaped']} escaped = "
            f"{t['rays'] + t['records'] + t['escaped']} (initial {t['initial']})"
        )
    d = panel["derived"]
    key = panel["key"]
    line2 = ""
    if key in ("4-bonded-pair", "8-lottery-detector"):
        row = next((r for r in d["per_tick"] if r["tick"] == frame["tick"]), None)
        if row is None and frame["tick"] == 0:
            row = {"taken": {"alice": 0, "bob": 0}, "passed": {"alice": 0, "bob": 0}}
        if row:
            line2 = (
                f"Alice: taken at +A {row['taken']['alice']}, passed to −A {row['passed']['alice']} · "
                f"Bob: taken at +B {row['taken']['bob']}, passed to −B {row['passed']['bob']}"
            )
        if key == "4-bonded-pair":
            outcomes = d["pair_outcomes"]
            resolved = []
            for code, sides in outcomes.items():
                resolved.append(f"…{code[-2:]}: A{sides.get('alice', '?')} B{sides.get('bob', '?')}")
            line2 = "pairs (registry answers, final): " + "  ".join(resolved) + " | " + line2
    elif key == "5-claim-gather":
        row = next(r for r in d["per_tick"] if r["tick"] == frame["tick"])
        screen = next((r[3]["matter"][0] for r in frame["records"] if r[2] == "screen"), 0)
        line2 = (
            f"claimed Nodes {row['claims']}/405 · free rays {row['free']} · homing {row['homing']} · "
            f"screen holds {screen}/64 · first claim tick {d['first_claim_tick']}, gathered tick {d['gathered_tick']}"
        )
    elif key == "7-ray-delay":
        screen = next((r[3]["quanta"][0] for r in frame["records"] if r[2] == "screen"), 0)
        waits = ", ".join(f"x={x}:k={k}" for x, y, k in frame["waits"]) or "none"
        line2 = f"first screen click tick {d['first_click_tick']} (same world without load: 11) · screen {screen}/128 · waits {waits}"
    elif key == "6-mirror-cavity":
        holds = [f"t{t}@x{x}" for t, x in d["mirror_hold_ticks"] if t <= frame["tick"]][-4:]
        line2 = (
            "mirror held stock at: "
            + (" ".join(holds) if holds else "—")
            + " · phase +4/link (64 steps)"
        )
    elif key == "3-double-slit":
        prof = {r[1]: r[3]["quanta"][0] for r in frame["records"] if r[2] == "screen"}
        line2 = (
            "screen y=0..8: "
            + " ".join(str(prof.get(y, 0)) for y in range(9))
            + " · y=3,5 = half-turn path difference"
        )
    elif key == "2-straight-rays":
        line2 = f"one link per tick along each integer line (DDA) · escaped {t['escaped']} through the open boundary"
    elif key == "1-outward-halo":
        line2 = f"{len(frame['cells'])} Nodes hold stock · axis weights [1,1,0]: the halo stays in z=1 · straight carried phases"
    return line1, line2


FIG_W, FIG_H = 16.4, 8.2
COLS = 4
LEFT, GAP = 0.008, 0.012
PANEL_W = (1 - 2 * LEFT - (COLS - 1) * GAP) / COLS
PANEL_H = 0.310
TOPS = (0.868, 0.435)
TITLE_BLOCK = 0.046  # title + contract + two legend lines above the axes
LINE = 0.0135  # one small text line, figure fraction


def wrap(text: str, width: int) -> list[str]:
    import textwrap

    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)


def compose(panels: list[dict], tick: int, meta: dict, plt_module) -> Image.Image:
    fig = plt_module.figure(figsize=(FIG_W, FIG_H), dpi=100)
    fig.set_facecolor(BACKGROUND)
    fig.text(
        0.008,
        0.982,
        "Universe24 — every ray kind the current engine propagates, one recorded run per panel",
        fontsize=11,
        color=INK,
        fontweight="bold",
        va="top",
    )
    fig.text(
        0.008,
        0.955,
        f"commit {meta['commit']} · source sha256 {meta['fingerprint'][:16]}… · {meta['python']} · "
        f"one frame per recorded tick, nothing interpolated · replay verified against run.html frames at every tick "
        f"({meta['mismatches']} mismatches) · tick {tick}",
        fontsize=7.6,
        color=DIM,
        va="top",
    )
    fig.text(
        0.008,
        0.932,
        "arrow = ray resident at its Node (length by amount; hue = Kerengonen phase, see strip; amber = no phase) · "
        "white arrow with ring = homing ray, drawn along the claim's parent port · ■ = record (emits, absorbs, "
        "reflects or detects; a record is not a ray)",
        fontsize=7.2,
        color=DIM,
        va="top",
    )
    fig.text(
        0.008,
        0.913,
        "shaded cell = octant field stock (panels 1, 7) or claim (panel 5) · nothing is in flight at frame time: after "
        "each tick every ray is at a Node · the picture is recorded state, not evidence of physics",
        fontsize=7.2,
        color=DIM,
        va="top",
    )
    strip = fig.add_axes([0.868, 0.960, 0.10, 0.015])
    strip.imshow([[i / 63 for i in range(64)]], cmap="hsv", aspect="auto")
    strip.set_axis_off()
    fig.text(0.866, 0.9675, "phase 0", fontsize=6.5, color=DIM, ha="right", va="center")
    fig.text(0.970, 0.9675, "P", fontsize=6.5, color=DIM, ha="left", va="center")
    cell_pt = (PANEL_W * FIG_W * 72) / 15.5
    for index, panel in enumerate(panels):
        r, c = divmod(index, COLS)
        x0 = LEFT + c * (PANEL_W + GAP)
        y0 = TOPS[r] - TITLE_BLOCK - PANEL_H
        ax = fig.add_axes([x0, y0, PANEL_W, PANEL_H])
        n = min(tick, panel["ticks"])
        held = tick > panel["ticks"]
        frame = panel["frames"][n]
        draw_panel(ax, panel, frame, held, {**panel["_scales"], "cell_pt": cell_pt})
        fig.text(x0, TOPS[r], panel["title"], fontsize=8.6, color=INK, fontweight="bold", va="top")
        fig.text(
            x0,
            TOPS[r] - 0.016,
            panel["contract"],
            fontsize=6.4,
            color="#9fd0ff",
            va="top",
            family="monospace",
        )
        for i, line in enumerate(wrap(LEGENDS[panel["key"]], 92)[:2]):
            fig.text(x0, TOPS[r] - 0.028 - i * 0.0115, line, fontsize=5.8, color=DIM, va="top")
        line1, line2 = footer(panel, frame, held)
        y = y0 - 0.003
        for line in wrap(line1, 74)[:2]:
            fig.text(x0, y, line, fontsize=6.1, color=INK, va="top")
            y -= LINE
        for line in wrap(line2, 88)[:2]:
            fig.text(x0, y, line, fontsize=5.8, color=DIM, va="top")
            y -= LINE * 0.9
    buffer = BytesIO()
    fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    plt_module.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def scales_for(panel: dict) -> dict:
    ray_amax = max([1] + [r[4] for f in panel["frames"] for r in f["rays"]])
    cell_vmax = max([0] + [c[3] for f in panel["frames"] for c in f["cells"]])
    absorber_max = max(
        [0]
        + [
            r[3].get(panel["field"], [0])[0]
            for f in panel["frames"]
            for r in f["records"]
            if r[2] not in EMITTER_TYPES
            and r[2] not in ("mirror", "mass body")
            and panel["field"] in r[3]
        ]
    )
    return {"ray_amax": ray_amax, "cell_vmax": cell_vmax, "absorber_max": absorber_max}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--repository", type=Path, default=ROOT, help="Git checkout whose short HEAD labels the frames"
    )
    args = parser.parse_args()
    out = args.output
    panels = load(out)
    for panel in panels:
        panel["_scales"] = scales_for(panel)
    index = json.loads((out / "ticks" / "index.json").read_text(encoding="utf-8"))
    commit = subprocess.run(
        ["git", "-C", str(args.repository), "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    meta = {
        "commit": commit,
        "fingerprint": index["source_sha256"],
        "python": "Python " + sys.version.split()[0],
        "mismatches": sum(p["mismatches"] for p in index["panels"]),
    }
    max_tick = max(p["ticks"] for p in panels)
    images = []
    durations = []
    stills = {}
    still_ticks = {0: "first", 8: "early", 20: "mid", max_tick: "final"}
    for tick in range(max_tick + 1):
        image = compose(panels, tick, meta, plt)
        images.append(image)
        durations.append(FINAL_MS if tick == max_tick else FRAME_MS)
        if tick in still_ticks:
            path = out / f"still-{still_ticks[tick]}-tick{tick:02d}.png"
            image.save(path)
            stills[still_ticks[tick]] = str(path)
        print("frame", tick, flush=True)
    gif = out / "rays.gif"
    # No loop extension: the GIF plays once and stops on the final frame.
    images[0].save(gif, save_all=True, append_images=images[1:], duration=durations, optimize=False)
    summary = {
        "gif": str(gif),
        "stills": stills,
        "frames": len(images),
        "frame_ms": FRAME_MS,
        "final_frame_ms": FINAL_MS,
        "loop": "none (plays once, stops on final frame)",
        "commit": commit,
        "source_sha256": index["source_sha256"],
        "python": sys.version,
        "matplotlib": matplotlib.__version__,
        "one_frame_per_recorded_tick": True,
        "interpolation": "none",
        "held_panels": "a panel whose run is shorter than the longest holds its final recorded frame, marked 'held'",
        "replay_note": (
            "run.html frames record per-Node value/populations/ray_count but not per-ray heading, amount or phase; "
            "record_ticks.py replays the identical initialization.json in-process and verifies it against the "
            "recorded frames at every tick (records, field readouts, escaped totals) before anything is drawn"
        ),
        "commands_log": str(out / "commands.log"),
        "scripts": [str(HERE / name) for name in ("worlds.py", "record_ticks.py", "render_rays.py")],
        "validator": "python -m event_universe.configuration_validation --kind initialization <config> reported VALID for all eight",
        "notes": [
            "panel 7 was first run with normal_budget 100 and emission 2400 and failed at tick 7 with 'funded ray emission or "
            "absorption does not support a delayed carrier cycle' (the load reaching the held lamp/screen plus their cycle cost "
            "exceeded the budget); the recorded panel uses budget 1000 and emission 28000 as tests/test_ray_delay.py's scale does",
            "conserved_at_every_completed_tick is False wherever quanta escape or are injected by design (open boundary, source: true); "
            "accounting_balanced_at_every_completed_tick (final = initial + sources - escaped) is True for every panel",
            "the bond registry (panel 4) and the lottery ticket (panel 8) have no drawing: only their recorded consequences on the board are shown",
        ],
        "panels": [
            {
                "key": p["key"],
                "title": p["title"],
                "contract_label": p["contract"],
                "config": p["config"],
                "run_dir": p["run_dir"],
                "ticks": p["ticks"],
                "run": p["run"],
                "verify": {k: v for k, v in p["verify"].items() if k != "first_mismatches"},
                "derived": {k: v for k, v in p["derived"].items() if k != "per_tick"},
                "shows": SHOWS[p["key"]][0],
                "does_not_show": SHOWS[p["key"]][1],
                "records_in_panel": sorted({r[2] for f in p["frames"] for r in f["records"]}),
            }
            for p in panels
        ],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print("wrote", gif, "and", out / "summary.json")


SHOWS = {
    "1-outward-halo": (
        "octant stock of a conservative outward field injected by a held charge record, spreading one link per tick with net octant direction per Node",
        "no rays exist in this panel: octant populations are the ray form of this contract; single-unit paths are not tracked; injection is external (source: true), not funded",
    ),
    "2-straight-rays": (
        "funded directed rays on three integer headings, one link per tick along a DDA line, crossing at a Node without responding, escaping through the open boundary",
        "no phase, no absorber; nothing shows a physical light speed, only the configured link clock",
    ),
    "3-double-slit": (
        "phased rays from two lamps in phase meeting at screen records; the fringe in Manhattan path difference builds in the screen stock",
        "the coherence gate itself is not drawn (only its result in absorbed stock); quanta that cancel continue and escape; no wavelength unit",
    ),
    "4-bonded-pair": (
        "pairs born at one Node on one tick carrying the same bond code (dashed link), plus detectors with settings, the registry's answers as captures",
        "the registry is not on the board and has no drawing: the dashed link marks equal bond codes, it is not a ray or a signal; four pairs are not a statistic",
    ),
    "5-claim-gather": (
        "a slow wave (pace 1/4), a screen click opening a claim, the claim flooding every Node with its parent port, free rays turning homing and walking home, gathered whole",
        "no lottery here (share capture of a single train); the flood is knowledge at Nodes, not stock",
    ),
    "6-mirror-cavity": (
        "one parcel each way, absorbed by a mirror record for one tick and re-emitted along the mirrored heading at the carried phase; the phase hue advances per link",
        "no standing wave (the lamp fires once); reflection passes through a record, there is no ray-to-ray reflection rule",
    ),
    "7-ray-delay": (
        "a lamp's ray train crossing Nodes loaded by a mass record's outward computation field; ray_wait registers holding rays k cycles; rays merging while they wait; the delayed first click",
        "no gravitational law: the wait is the configured local delay law applied to rays; the whole row is loaded because the field spreads",
    ),
    "8-lottery-detector": (
        "single quanta meeting a reference lamp's quantum at a plus detector with coherence one half; the lottery taking or passing each whole ray; the minus detector taking what passed",
        "plus detector stock includes the reference quanta it absorbs; reference quanta not taken walk on along -y and escape; eight quanta per side are not a rate measurement",
    ),
}


if __name__ == "__main__":
    main()
