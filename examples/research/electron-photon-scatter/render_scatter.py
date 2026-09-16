"""Renderer (exploration lane): GIF of the recorded electron-ray / photon-ray run.

Follows examples/gallery/particle_gallery.py: the frames the canonical runner embedded
in run.html are read back verbatim, one drawn frame per recorded tick, nothing
interpolated, no trajectory invented. Every displayed number is a recorded value
(frame node fields, carrier position and momentum) or a cumulative sum of recorded
events (escaped quanta). Cross-checks against events.jsonl and run.json are
asserted before anything is drawn.

    PYTHONPATH=src python examples/research/electron-photon-scatter/render_scatter.py --run <run dir> --output <out dir>
"""

from __future__ import annotations

import argparse
import json
import math
from io import BytesIO
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from PIL import Image

BACKGROUND = "#0b1020"
INK = "#e8ecf4"
DIM = "#8a95b3"
LATTICE = "#22304f"
ELECTRON = "#5ea8ff"
HALO = "#3d7bff"
FORWARD = "#ffd166"  # rad_px quanta travelling +X
BACK = "#ff8c5a"  # rad_mx quanta travelling -X
HELD = "#ffffff"
FLASH = "#ffffff"
RULE = "#ffd166"
FRAME_MS = 650
HOLD = 3
FINAL_HOLD = 4
DIRS = ("px", "mx", "py", "my", "pz", "mz")
UNIT = {
    "px": (1, 0, 0),
    "mx": (-1, 0, 0),
    "py": (0, 1, 0),
    "my": (0, -1, 0),
    "pz": (0, 0, 1),
    "mz": (0, 0, -1),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def recorded_frames(case_dir: Path) -> list[dict[str, Any]]:
    document = (case_dir / "run.html").read_text(encoding="utf-8")
    start = document.find('{"frames"')
    if start < 0:
        raise ValueError("run.html carries no recorded frames; run with --visualize")
    recording, _ = json.JSONDecoder().raw_decode(document[start:])
    return recording["frames"]


def events(case_dir: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line) for line in (case_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]


# ---------------------------------------------------------------- recorded facts per tick


def timeline(case_dir: Path) -> dict[str, Any]:
    frames = recorded_frames(case_dir)
    trace = events(case_dir)
    report = load(case_dir / "run.json")
    init = load(case_dir / "initialization.json")
    carrier_type = init["disturbance_types"][0]["name"]
    rate_den = init["disturbance_types"][0]["transport"].get("rate_denominator")
    scatter = {
        e["tick"]: (-e["reaction"]["held_px"][0], e["position"])
        for e in trace
        if e["event"] == "spatial_coupled" and e.get("reaction")
    }
    hold_ticks = sorted(
        e["tick"]
        for e in trace
        if e["event"] == "spatial_cycle" and e.get("rule_delta", {}).get("held_px", [0])[0] > 0
    )
    sent_ticks = {e["tick"]: e["arrival_tick"] for e in trace if e["event"] == "sent"}
    escaped_cumulative: dict[int, tuple[int, int]] = {}
    px = mx = 0
    for e in trace:
        if e["event"] == "spatial_escaped":
            px += e["escaped"].get("rad_px", [0])[0]
            mx += e["escaped"].get("rad_mx", [0])[0]
            escaped_cumulative[e["tick"]] = (px, mx)
    rows = []
    for frame in frames:
        tick = frame["tick"]
        cumulative = max(
            ((t, v) for t, v in escaped_cumulative.items() if t <= tick), default=(-1, (0, 0))
        )[1]
        carrier = None
        for node in frame["nodes"]:
            for d in node["disturbances"]:
                if d["type"] == carrier_type:
                    carrier = {"position": node["position"], "values": d["values"]}
        assert carrier is not None, f"carrier not resident at tick {tick}"
        quanta: dict[str, dict[tuple[int, int, int], int]] = {f"rad_{d}": {} for d in DIRS}
        quanta["held_px"] = {}
        halo: dict[tuple[int, int, int], int] = {}
        for node in frame.get("spatial_fields", []):
            p = tuple(node["position"])
            for name in quanta:
                v = node["fields"][name]["value"][0]
                if v:
                    quanta[name][p] = v
            v = node["fields"]["electric_signal"]["value"][0]
            if v:
                halo[p] = v
        resident = sum(sum(m.values()) for m in quanta.values())
        wave_p = [0, 0, 0]
        for d in DIRS:
            n = sum(quanta[f"rad_{d}"].values())
            for i in range(3):
                wave_p[i] += n * UNIT[d][i]
        wave_p[0] += sum(quanta["held_px"].values())
        pe = carrier["values"]["momentum"]
        total_in_world = [pe[i] + wave_p[i] for i in range(3)]
        escaped_p = cumulative[0] - cumulative[1]
        rows.append(
            {
                "tick": tick,
                "carrier": carrier,
                "quanta": quanta,
                "halo": halo,
                "resident_quanta": resident,
                "escaped_quanta": cumulative[0] + cumulative[1],
                "escaped_px": cumulative[0],
                "escaped_mx": cumulative[1],
                "wave_momentum": wave_p,
                "total_in_world": total_in_world,
                "total_with_escaped": [
                    total_in_world[0] + escaped_p,
                    total_in_world[1],
                    total_in_world[2],
                ],
                "halo_total": sum(halo.values()),
                "scatter": tick in scatter,
                "scatter_amount": scatter.get(tick, (0, None))[0],
                "scatter_position": scatter.get(tick, (0, None))[1],
                "held_now": sum(quanta["held_px"].values()),
                "hop": sent_ticks.get(tick),
            }
        )
    initial_quanta = sum(s["populations"][0] for s in init["spatial_seeds"])
    # Cross-checks: recorded frames versus event trace and run.json
    for row in rows:
        assert row["resident_quanta"] + row["escaped_quanta"] == initial_quanta, row["tick"]
        assert row["total_with_escaped"] == [initial_quanta, 0, 0], (
            row["tick"],
            row["total_with_escaped"],
        )
        for d in ("py", "my", "pz", "mz"):
            assert not row["quanta"][f"rad_{d}"]
    assert rows[-1]["carrier"]["values"]["momentum"] == [2 * sum(a for a, _ in scatter.values()), 0, 0]
    assert report["status"] == "completed" and report["accounting_balanced_at_every_completed_tick"]
    assert report["spatial_accounting"]["rad_px"]["escaped"][0] == rows[-1]["escaped_px"]
    assert report["spatial_accounting"]["rad_mx"]["escaped"][0] == rows[-1]["escaped_mx"]
    assert report["spatial_accounting"]["held_px"]["current"][0] == rows[-1]["held_now"]
    assert report["final_totals"]["electric_signal"][0] == rows[-1]["halo_total"]
    return {
        "shape": init["shape"],
        "rows": rows,
        "scatter": scatter,
        "scatter_ticks": sorted(scatter),
        "hold_ticks": hold_ticks,
        "hop_ticks": sorted(sent_ticks),
        "first_contact": hold_ticks[0] if hold_ticks else None,
        "initial_quanta": initial_quanta,
        "rate_denominator": rate_den,
        "report": report,
        "init": init,
        "max_halo": max((abs(v) for r in rows for v in r["halo"].values()), default=1),
    }


# ---------------------------------------------------------------- drawing


def _figure():
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.set_facecolor(BACKGROUND)
    ax = fig.add_axes([0.0, 0.11, 1.0, 0.77], projection="3d")
    ax.set_facecolor(BACKGROUND)
    ax.set_axis_off()
    return fig, ax


def _grid(ax, shape):
    segs = []
    nx, ny, nz = shape
    for x in range(nx):
        segs.append([(x, 0, 0), (x, ny - 1, 0)])
    for y in range(ny):
        segs.append([(0, y, 0), (nx - 1, y, 0)])
    for x, y in ((0, 0), (nx - 1, 0), (0, ny - 1), (nx - 1, ny - 1)):
        segs.append([(x, y, 0), (x, y, nz - 1)])
    for a, b in (
        ((0, 0), (nx - 1, 0)),
        ((0, ny - 1), (nx - 1, ny - 1)),
        ((0, 0), (0, ny - 1)),
        ((nx - 1, 0), (nx - 1, ny - 1)),
    ):
        segs.append([(a[0], a[1], nz - 1), (b[0], b[1], nz - 1)])
    ax.add_collection3d(Line3DCollection(segs, colors=LATTICE, linewidths=0.6, alpha=0.9))
    cy, cz = ny // 2, nz // 2
    ax.scatter(list(range(nx)), [cy] * nx, [cz] * nx, s=6, c=LATTICE, depthshade=False, linewidths=0)
    for x in range(0, nx - 1, 4):
        ax.text(x, -0.9, 0, f"x={x}", color=DIM, fontsize=7, ha="center")


def _glow(ax, p, color, base):
    for size, alpha in ((base * 9, 0.07), (base * 4, 0.16), (base * 1.8, 0.4), (base, 1.0)):
        ax.scatter([p[0]], [p[1]], [p[2]], s=size, c=color, alpha=alpha, depthshade=False, linewidths=0)


def _unclip(ax):
    for artist in (*ax.collections, *ax.lines, *ax.texts):
        artist.set_clip_on(False)


def draw_frame(tl: dict[str, Any], index: int, provenance: str):
    row = tl["rows"][index]
    tick = row["tick"]
    shape = tl["shape"]
    rate_den = tl["rate_denominator"]
    fig, ax = _figure()
    ax.set_box_aspect((shape[0], shape[1], shape[2]), zoom=1.5)
    ax.set_xlim(-0.5, shape[0] - 0.5)
    ax.set_ylim(-0.5, shape[1] - 0.5)
    ax.set_zlim(-0.5, shape[2] - 0.5)
    ax.view_init(elev=22, azim=-58)
    _grid(ax, shape)

    # electric_signal halo: square-root display mapping (display contract), one colour = negative sign
    for p, v in row["halo"].items():
        strength = math.sqrt(abs(v) / tl["max_halo"])
        ax.scatter(
            [p[0]],
            [p[1]],
            [p[2]],
            s=20 + 600 * strength,
            c=HALO,
            alpha=0.05 + 0.40 * strength,
            depthshade=False,
            linewidths=0,
        )

    # photon rays: forward stream rad_px (+X) and back stream rad_mx (-X)
    for p, n in row["quanta"]["rad_px"].items():
        ax.scatter(
            [p[0]], [p[1]], [p[2]], s=40 + 22 * n, c=FORWARD, alpha=0.95, depthshade=False, linewidths=0
        )
        ax.quiver(
            p[0], p[1], p[2], 0.12 * n, 0, 0, color=FORWARD, linewidth=1.6, arrow_length_ratio=0.35
        )
        ax.text(p[0], p[1], p[2] - 0.75, f"{n}", color=FORWARD, fontsize=8, ha="center")
    for p, n in row["quanta"]["rad_mx"].items():
        ax.scatter(
            [p[0]],
            [p[1] - 0.35],
            [p[2] + 0.35],
            s=40 + 22 * n,
            c=BACK,
            alpha=0.95,
            depthshade=False,
            linewidths=0,
        )
        ax.quiver(
            p[0],
            p[1] - 0.35,
            p[2] + 0.35,
            -0.12 * n,
            0,
            0,
            color=BACK,
            linewidth=1.6,
            arrow_length_ratio=0.35,
        )
        ax.text(p[0], p[1] - 0.35, p[2] + 0.9, f"{n}", color=BACK, fontsize=8, ha="center")

    # electron ray
    c = row["carrier"]
    p = c["position"]
    pe = c["values"]["momentum"]
    q3 = c["values"]["charge"][0]
    m = c["values"]["mass"][0]
    scatter_visible = (tick - 1) in tl["scatter_ticks"]
    if scatter_visible:
        _glow(ax, p, FLASH, 330)
    _glow(ax, p, ELECTRON, 170)
    for hp, n in row["quanta"]["held_px"].items():
        ax.scatter(
            [hp[0]],
            [hp[1]],
            [hp[2]],
            s=260,
            facecolors="none",
            edgecolors=HELD,
            linewidths=1.4,
            depthshade=False,
        )
        stranded = list(hp) != list(p)
        ax.text(
            hp[0],
            hp[1] + 0.9,
            hp[2] + (-1.0 if stranded else 0.55),
            f"held_px = {n}" + ("  (stranded: electron moved on)" if stranded else ""),
            color=HELD,
            fontsize=8.5,
            ha="center",
        )
    if any(pe):
        ax.quiver(
            p[0],
            p[1],
            p[2],
            0.125 * pe[0],
            0.125 * pe[1],
            0.125 * pe[2],
            color=ELECTRON,
            linewidth=2.4,
            arrow_length_ratio=0.25,
        )
    if row["hop"] is not None:
        ax.text(
            p[0] + 0.4,
            p[1],
            p[2] - 1.15,
            f"→ hop +X, arrives tick {row['hop']}",
            color=ELECTRON,
            fontsize=8,
            ha="left",
        )
    ax.text(
        p[0],
        p[1],
        p[2] + 2.3,
        "electron ray  e⁻",
        color=ELECTRON,
        fontsize=12,
        ha="center",
        fontweight="bold",
    )
    ax.text(
        p[0],
        p[1],
        p[2] + 1.8,
        f"q = {q3 / 3:+.0f} e (catalog: {q3:+d} thirds)   m = {m} keV/c² (catalog)",
        color=ELECTRON,
        fontsize=8.5,
        ha="center",
    )
    ax.text(
        p[0],
        p[1],
        p[2] + 1.35,
        f"p = ({pe[0]}, {pe[1]}, {pe[2]}) quantum momentum units",
        color=ELECTRON,
        fontsize=8.5,
        ha="center",
    )
    _unclip(ax)

    # header
    fig.text(
        0.03,
        0.960,
        "Electron ray meets photon rays  (declared family coupling, recorded run of the Universe24 engine)",
        color=INK,
        fontsize=15,
        fontweight="bold",
    )
    fig.text(
        0.03,
        0.927,
        f"tick {tick:02d} / {tl['rows'][-1]['tick']}    open {shape[0]} × {shape[1]} × {shape[2]} lattice, link_ticks 1    "
        f"photon rays: six pulses of 10 quanta (+X, 1 momentum unit each) seeded at x = 1..6; electron ray seeded at rest at x = 8",
        color=DIM,
        fontsize=9.3,
    )
    fig.text(0.03, 0.900, provenance, color=DIM, fontsize=7.3)
    fig.text(
        0.97,
        0.900,
        "one frame per recorded tick; nothing interpolated; playback stops at the final frame",
        color=DIM,
        fontsize=7.3,
        ha="right",
    )

    # legend (2D, fixed)
    fig.text(
        0.015,
        0.80,
        "electron ray: electron family (charge, mass, momentum), moves along p",
        color=ELECTRON,
        fontsize=8,
    )
    fig.text(
        0.015,
        0.78,
        f"    at |p|/{rate_den} hops per tick (supplied transport rule)",
        color=ELECTRON,
        fontsize=8,
    )
    fig.text(
        0.015,
        0.75,
        "photon rays γ: catalog q = 0, m = 0 (theoretical), spin 1 → here the",
        color=FORWARD,
        fontsize=8,
    )
    fig.text(
        0.015,
        0.73,
        "    radiation-quantum family: fields rad_px (+X, yellow) / rad_mx (−X, orange),",
        color=FORWARD,
        fontsize=8,
    )
    fig.text(
        0.015,
        0.71,
        "    1 momentum unit per quantum, no energy register; number = quanta at Node",
        color=FORWARD,
        fontsize=8,
    )
    fig.text(
        0.015,
        0.68,
        "halo: electric_signal, configured outward field emitted by any",
        color=HALO,
        fontsize=8,
    )
    fig.text(
        0.015,
        0.66,
        "    charge-carrying family (charge×72 per interval); size ∝ √|value|",
        color=HALO,
        fontsize=8,
    )
    fig.text(
        0.015,
        0.63,
        "white ring: held_px quanta waiting at a Node for the coupling",
        color=HELD,
        fontsize=8,
    )

    # event note: the frame for tick t shows the commits recorded at tick t-1 in events.jsonl
    prev = tick - 1
    if scatter_visible:
        amount, sp = next((a, s_) for t_, (a, s_) in tl["scatter"].items() if t_ == prev)
        note = (
            f"visible now (committed at tick {prev}): coupling scatter_held_quanta at Node ({sp[0]},{sp[1]},{sp[2]}): "
            f"{amount} held quanta → rad_mx (−X), electron p += {2 * amount} (+X); invariants quanta / total_momentum exact"
        )
        color = INK
    elif prev == tl["first_contact"]:
        note = (
            f"visible now (field rule at tick {prev}): first contact; hold_scattered_quanta keeps min(rad_px, presence×2) = "
            f"{row['held_now']} quanta at the electron's Node, 8 stream on"
        )
        color = INK
    elif tick == 0:
        note = "tick 0: initial state; any charge-carrying family emits presence (a supplied marker) and the electric_signal halo each interval"
        color = DIM
    elif prev in tl["hop_ticks"]:
        note = (
            f"visible now: the electron ray hopped one link along its momentum (sent at tick {prev}, received at tick {tick}); "
            f"supplied hop rate |p|/{rate_den} per tick, integer remainder carried"
        )
        color = DIM
    else:
        note = "streams move one link per tick; forward stream continues with 8 per pulse, back stream carries 2 per pulse; open faces record escapes"
        color = DIM
    fig.text(0.03, 0.128, note, color=color, fontsize=9.2)

    # readout
    tw = row["total_with_escaped"]
    ti = row["total_in_world"]
    fig.text(
        0.03,
        0.103,
        f"electron p = ({pe[0]}, {pe[1]}, {pe[2]})    quanta in world {row['resident_quanta']} + escaped {row['escaped_quanta']} = {tl['initial_quanta']}    "
        f"total momentum electron + quanta in world = ({ti[0]}, {ti[1]}, {ti[2]}), incl. escaped quanta ({tw[0]}, {tw[1]}, {tw[2]})    "
        f"halo stock {row['halo_total']}    accounting balanced: {tl['report']['accounting_balanced_at_every_completed_tick']}",
        color=INK,
        fontsize=8.6,
    )
    fig.text(
        0.03,
        0.080,
        "meeting rule = declared coupling between the two families: spatial_interactions scatter_held_quanta, selector requires [charge, momentum]",
        color=INK,
        fontsize=7.8,
    )
    fig.text(
        0.03,
        0.061,
        "(any family carrying both) with the radiation-quantum fields: held_px → 0, rad_mx += held, p += 2·held·(+X). "
        "Hold: field rule min(rad_px, presence×2); presence = (q/3)² emitted by requires [charge].",
        color=INK,
        fontsize=7.8,
    )
    fig.text(
        0.03,
        0.042,
        "scattering fraction is a supplied rule (presence×2), not a derived cross section;  energy-family law: ABSENT "
        "(no declared relation between photon energy/momentum and the electron family's response)",
        color=RULE,
        fontsize=7.8,
    )
    fig.text(
        0.03,
        0.023,
        "electric_signal is a configured outward field (no Coulomb law, no attenuation; dilution by redistribution only).  "
        "Not reproduced: photon energy/frequency shift (Compton formula), Klein–Nishina cross section,",
        color=DIM,
        fontsize=7.6,
    )
    fig.text(
        0.03,
        0.005,
        f"relativistic kinematics; the 511 keV/c² mass is inert inventory; hop rate |p|/{rate_den} is supplied.  "
        "Arrow lengths ∝ recorded momentum.  Frame t shows commits recorded at tick t−1 (arrivals at tick t).",
        color=DIM,
        fontsize=7.6,
    )
    return fig


def _image(fig) -> Image.Image:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stills", default="0,3,4,6,10,16", help="ticks saved as PNG")
    parser.add_argument(
        "--commit", default="e5b5911", help="commit label printed in the provenance line"
    )
    args = parser.parse_args()
    tl = timeline(args.run)
    report = tl["report"]
    provenance = (
        f"model {report['model']}   source sha256 {report['source_sha256'][:12]}…   "
        f"init sha256 {report['initialization_sha256'][:12]}…   commit {args.commit}"
    )
    args.output.mkdir(parents=True, exist_ok=True)
    stills = {int(s) for s in args.stills.split(",")}
    images: list[Image.Image] = []
    durations: list[int] = []
    saved = []
    for index, row in enumerate(tl["rows"]):
        image = _image(draw_frame(tl, index, provenance))
        visible_scatter = (row["tick"] - 1) in tl["scatter"]
        hold = HOLD if (visible_scatter or row["tick"] - 1 == tl["first_contact"]) else 1
        if index == len(tl["rows"]) - 1:
            hold = FINAL_HOLD
        images.extend([image] * hold)
        durations.extend([FRAME_MS] * hold)
        if row["tick"] in stills:
            path = args.output / f"electron_photon_scatter_tick{row['tick']:02d}.png"
            image.save(path)
            saved.append(str(path))
    gif = args.output / "electron_photon_scatter.gif"
    # No `loop` argument: the GIF plays once and stops at the final frame (display contract).
    images[0].save(gif, save_all=True, append_images=images[1:], duration=durations, optimize=False)
    summary = {
        "gif": str(gif),
        "stills": saved,
        "frames_drawn": len(tl["rows"]),
        "gif_logical_frames": len(images),
        "frame_ms": FRAME_MS,
        "scatter_ticks": tl["scatter_ticks"],
        "hold_ticks": tl["hold_ticks"],
        "hop_ticks": tl["hop_ticks"],
        "first_contact": tl["first_contact"],
        "frame_offset_note": "the recorded frame for tick t shows field-rule and joint-transaction commits recorded at tick t-1 in events.jsonl; hops sent at t-1 are received at t",
        "per_tick": [
            {k: v for k, v in r.items() if k not in ("quanta", "halo")}
            | {
                "quanta_nodes": {
                    n: {str(list(p)): c for p, c in m.items()} for n, m in r["quanta"].items() if m
                },
                "halo_nodes": len(r["halo"]),
                "halo_min": min(r["halo"].values(), default=0),
            }
            for r in tl["rows"]
        ],
        "run_flags": {
            k: report[k]
            for k in (
                "status",
                "completed_ticks",
                "conserved_at_every_completed_tick",
                "accounting_balanced_at_every_completed_tick",
                "initial_totals",
                "final_totals",
                "source_totals",
                "escaped_totals",
                "source_sha256",
                "initialization_sha256",
                "model",
            )
        },
    }
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("per_tick", "run_flags")}, indent=1))


if __name__ == "__main__":
    main()
