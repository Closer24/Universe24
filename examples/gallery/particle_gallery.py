"""Named-particle experiments rendered as three-dimensional animations.

This is an experiment harness and a renderer of saved results, not another
evolution engine. Every configuration is derived from a checked-in file, runs
through the canonical runner, and is read back from its recorded output only:
receptions in ``events.jsonl``, the recorded frames of a ``--visualize`` run,
``run.json`` decision records and the final ``state.json``. Nothing is
interpolated between ticks and no trajectory is invented.

Two experiments:

1. ``backscatter``: the bounded rational elastic electron-positron contract
   from ``examples/particle-contracts``, with the two particles seeded six
   Nodes apart so that the approach, the contact and the recoil are recorded.
2. ``reactions``: the configured lepton reactions of ``lepton_reactions.json``,
   annihilation, a muon pair with its decays and beta decay, each rule a
   two-record conversion with conserved integer inventories.
"""

import argparse
import json
import shutil
from fractions import Fraction
from io import BytesIO
from pathlib import Path
from typing import Any

from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BACKSCATTER_TEMPLATE = ROOT / "examples/particle-contracts/electron-positron.json"
BACKSCATTER_SEEDS = [
    {"position": [5, 8, 8], "type": "electron"},
    {"position": [11, 8, 8], "type": "positron"},
]
BACKSCATTER_TICKS = 96
REACTIONS_TEMPLATE = HERE / "lepton_reactions.json"
REACTION_SCENARIOS = {
    "annihilation": {
        "title": "Electron-positron annihilation into two photons",
        "ticks": 12,
        "seeds": [
            {"position": [2, 7, 1], "type": "electron"},
            {"position": [12, 7, 1], "type": "positron"},
        ],
    },
    "muon_pair": {
        "title": "Electron-positron annihilation into a muon pair, then muon decays",
        "ticks": 12,
        "seeds": [
            {
                "position": [2, 7, 1],
                "type": "electron",
                "values": {"energy": 1100, "momentum": [1100, 0, 0]},
            },
            {
                "position": [12, 7, 1],
                "type": "positron",
                "values": {"energy": 1100, "momentum": [-1100, 0, 0]},
            },
            {"position": [7, 10, 1], "type": "vacuum_slot"},
            {"position": [7, 10, 1], "type": "vacuum_slot"},
            {"position": [7, 4, 1], "type": "vacuum_slot"},
            {"position": [7, 4, 1], "type": "vacuum_slot"},
        ],
    },
    "beta_decay": {
        "title": "Neutron beta decay through a one-tick W boson",
        "ticks": 11,
        "seeds": [
            {"position": [3, 7, 1], "type": "neutron"},
            {"position": [7, 7, 1], "type": "vacuum_slot"},
            {"position": [7, 7, 1], "type": "vacuum_slot"},
        ],
    },
}
SYMBOLS = {
    "electron": ("e\u207b", "#5ea8ff"),
    "positron": ("e\u207a", "#ff6b6b"),
    "photon": ("\u03b3", "#fff1a8"),
    "muon": ("\u03bc\u207b", "#b48cff"),
    "antimuon": ("\u03bc\u207a", "#ff8cf0"),
    "muon_neutrino": ("\u03bd\u03bc", "#9fe0c8"),
    "muon_antineutrino": ("\u03bd\u0305\u03bc", "#9fe0c8"),
    "electron_neutrino": ("\u03bd\u2091", "#9fe0c8"),
    "electron_antineutrino": ("\u03bd\u0305\u2091", "#9fe0c8"),
    "w_minus": ("W\u207b", "#ffa64d"),
    "w_plus": ("W\u207a", "#ffa64d"),
    "neutron": ("n", "#c9d3ea"),
    "proton": ("p", "#ff8a65"),
    "vacuum_slot": ("vacuum slot", "#3a4562"),
}
BACKGROUND = "#0b1020"
INK = "#e8ecf4"
DIM = "#8a95b3"
LATTICE = "#22304f"
NEGATIVE = "#5ea8ff"
POSITIVE = "#ff6b6b"
FLASH = "#ffffff"
LABELS = {
    "electron": ("electron  e⁻", NEGATIVE),
    "positron": ("positron  e⁺", POSITIVE),
}
FRAME_MS = 650
CONTACT_HOLD = 3


# ---------------------------------------------------------------- configurations


def backscatter_configuration() -> dict[str, Any]:
    """The checked-in contract with the pair seeded apart, so the approach is recorded."""
    raw = json.loads(BACKSCATTER_TEMPLATE.read_text(encoding="utf-8"))
    raw["seeds"] = json.loads(json.dumps(BACKSCATTER_SEEDS))
    raw["ticks"] = BACKSCATTER_TICKS
    return raw


def reaction_configuration(name: str) -> dict[str, Any]:
    """The checked-in reaction laws with one scenario's seeds and run length."""
    raw = json.loads(REACTIONS_TEMPLATE.read_text(encoding="utf-8"))
    scenario = REACTION_SCENARIOS[name]
    raw["seeds"] = json.loads(json.dumps(scenario["seeds"]))
    raw["ticks"] = scenario["ticks"]
    return raw


# ---------------------------------------------------------------- recorded facts


def _run(raw: dict[str, Any], output: Path, name: str, *, visualize: bool) -> Path:
    case_dir = output / name
    if case_dir.exists():
        shutil.rmtree(case_dir)
    output.mkdir(parents=True, exist_ok=True)
    initialization = output / (name + ".json")
    initialization.write_text(json.dumps(raw, indent=1) + "\n", encoding="utf-8")
    run_initialization(initialization, case_dir, visualize=visualize)
    report = json.loads((case_dir / "run.json").read_text(encoding="utf-8"))
    assert report["status"] == "completed", report["error"]
    return case_dir


def momentum(values: dict[str, list[int]]) -> tuple[Fraction, Fraction, Fraction]:
    """Decode the contract's whole + remainder / denominator momentum, host side only."""
    whole, remainder, denominator = values["whole"], values["remainder"], values["denominator"][0]
    return tuple(Fraction(w) + Fraction(r, denominator) for w, r in zip(whole, remainder, strict=True))


def backscatter_timeline(case_dir: Path) -> dict[str, Any]:
    """Recorded positions and momenta per reception tick; the contact is where both share a Node."""
    initialization = json.loads((case_dir / "initialization.json").read_text(encoding="utf-8"))
    positions: dict[int, dict[str, dict[str, Any]]] = {
        0: {
            seed["type"]: {"position": seed["position"], "values": None}
            for seed in initialization["seeds"]
        }
    }
    defaults = {t["name"]: t["defaults"] for t in initialization["disturbance_types"]}
    for kind, entry in positions[0].items():
        entry["values"] = {
            k: (list(v) if isinstance(v, list) else [v]) for k, v in defaults[kind].items()
        }
    for line in (case_dir / "events.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["event"] == "received":
            positions.setdefault(event["tick"], {})[event["disturbance"]] = {
                "position": event["position"],
                "values": event["values"],
            }
    ticks = sorted(positions)
    for tick in ticks:
        for kind in ("electron", "positron"):
            if kind not in positions[tick]:
                previous = max(t for t in ticks if t < tick and kind in positions[t])
                positions[tick][kind] = positions[previous][kind]
    contact = [
        t for t in ticks if positions[t]["electron"]["position"] == positions[t]["positron"]["position"]
    ]
    report = json.loads((case_dir / "run.json").read_text(encoding="utf-8"))
    return {
        "shape": initialization["shape"],
        "ticks": ticks,
        "records": positions,
        "contact_ticks": contact,
        "final_totals": report["final_totals"],
        "conserved": report["conserved_at_every_completed_tick"],
    }


def recorded_frames(case_dir: Path) -> list[dict[str, Any]]:
    """The frames the canonical runner embedded in its HTML player, read back verbatim."""
    document = (case_dir / "run.html").read_text(encoding="utf-8")
    start = document.find('{"frames"')
    if start < 0:
        raise ValueError("run.html carries no recorded frames; run with visualize")
    recording, _ = json.JSONDecoder().raw_decode(document[start:])
    return recording["frames"]


def _records_by_node(frame: dict[str, Any]) -> dict[tuple[int, ...], list[dict[str, Any]]]:
    return {
        tuple(node["position"]): [d for d in node["disturbances"] if d["type"] != "vacuum_slot"]
        for node in frame["nodes"]
        if any(d["type"] != "vacuum_slot" for d in node["disturbances"])
    }


def sent_types(case_dir: Path) -> dict[tuple[int, tuple[int, ...]], list[str]]:
    """Record types sent from each Node at each tick, from the event trace."""
    table: dict[tuple[int, tuple[int, ...]], list[str]] = {}
    for line in (case_dir / "events.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["event"] == "sent":
            table.setdefault((event["tick"], tuple(event["position"])), []).append(event["disturbance"])
    return table


def reaction_events(
    frames: list[dict[str, Any]],
    sent: dict[tuple[int, tuple[int, ...]], list[str]],
    rules: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """A rule fired at (tick, Node) when its inputs are recorded there and its outputs leave or stay."""
    events = []
    for index, frame in enumerate(frames):
        following = frames[index + 1] if index + 1 < len(frames) else None
        present = {
            tuple(node["position"]): [d["type"] for d in node["disturbances"]] for node in frame["nodes"]
        }
        held = (
            {}
            if following is None
            else {
                tuple(node["position"]): [d["type"] for d in node["disturbances"]]
                for node in following["nodes"]
            }
        )
        for position, kinds in present.items():
            produced = sent.get((frame["tick"], position), []) + held.get(position, [])
            for rule in rules:
                left, right = rule["left_type"], rule["right_type"]
                if left not in kinds or right not in kinds:
                    continue
                outputs = [rule["output_types"]["left"], rule["output_types"]["right"]]
                remaining = list(produced)
                if all(o in remaining and (remaining.remove(o) or True) for o in outputs):
                    events.append(
                        {"tick": frame["tick"], "position": list(position), "rule": rule["name"]}
                    )
    return events


def reaction_summary(case_dir: Path, frames: list[dict[str, Any]]) -> dict[str, Any]:
    initialization = json.loads((case_dir / "initialization.json").read_text(encoding="utf-8"))
    report = json.loads((case_dir / "run.json").read_text(encoding="utf-8"))
    final = _records_by_node(frames[-1])
    return {
        "events": reaction_events(frames, sent_types(case_dir), initialization["interactions"]),
        "final_records": sorted(
            (list(p), d["type"], d["values"]["energy"][0], d["values"]["momentum"])
            for p, records in final.items()
            for d in records
        ),
        "initial_totals": report["initial_totals"],
        "final_totals": report["final_totals"],
        "escaped_totals": report["escaped_totals"],
        "accounting_balanced": report["accounting_balanced_at_every_completed_tick"],
    }


# ---------------------------------------------------------------- drawing


def _grid_plane(ax: Any, shape: list[int], z: int, line: Any) -> None:
    segments = []
    for x in range(shape[0]):
        segments.append([(x, 0, z), (x, shape[1] - 1, z)])
    for y in range(shape[1]):
        segments.append([(0, y, z), (shape[0] - 1, y, z)])
    ax.add_collection3d(line(segments, colors=LATTICE, linewidths=0.5, alpha=0.9))
    points = [(x, y, z) for x in range(shape[0]) for y in range(shape[1])]
    ax.scatter(
        [p[0] for p in points],
        [p[1] for p in points],
        [p[2] for p in points],
        s=4,
        c=LATTICE,
        depthshade=False,
        linewidths=0,
    )


def _glow(ax: Any, p: list[int], color: str, base: float) -> None:
    for size, alpha in ((base * 9, 0.07), (base * 4, 0.16), (base * 1.8, 0.4), (base, 1.0)):
        ax.scatter([p[0]], [p[1]], [p[2]], s=size, c=color, alpha=alpha, depthshade=False, linewidths=0)


def _unclip(ax: Any) -> None:
    for artist in (*ax.collections, *ax.lines, *ax.texts):
        artist.set_clip_on(False)


def _figure(plt: Any):
    fig = plt.figure(figsize=(12, 6), dpi=100)
    fig.set_facecolor(BACKGROUND)
    ax = fig.add_axes([0.0, 0.0, 1.0, 0.86], projection="3d")
    ax.set_facecolor(BACKGROUND)
    ax.set_axis_off()
    return fig, ax


def draw_backscatter_frame(timeline: dict[str, Any], tick: int, plt: Any, line: Any) -> Any:
    fig, ax = _figure(plt)
    shape = timeline["shape"]
    ax.set_box_aspect((shape[0], shape[1] * 0.7, 4), zoom=2.3)
    ax.set_xlim(-0.5, shape[0] - 0.5)
    ax.set_ylim(2.5, shape[1] - 3.5)
    ax.set_zlim(shape[2] // 2 - 2, shape[2] // 2 + 2)
    ax.view_init(elev=26, azim=-72)
    z = shape[2] // 2
    _grid_plane(ax, shape, z, line)
    records = timeline["records"][tick]
    contact = tick in timeline["contact_ticks"]
    if contact:
        p = records["electron"]["position"]
        _glow(ax, p, FLASH, 260)
        ax.text(
            p[0],
            p[1],
            p[2] + 2.4,
            "contact: elastic backscatter, momenta exchanged",
            color=INK,
            fontsize=12,
            ha="center",
            fontweight="bold",
        )
    momenta = {}
    for kind in ("electron", "positron"):
        entry = records[kind]
        p = entry["position"]
        label, color = LABELS[kind]
        _glow(ax, p, color, 130)
        px, py, pz = momentum(entry["values"])
        momenta[kind] = (px, py, pz)
        if not contact:
            ax.quiver(
                p[0],
                p[1],
                p[2],
                float(px) / 650,
                float(py) / 650,
                float(pz) / 650,
                color=color,
                linewidth=2,
                arrow_length_ratio=0.3,
            )
        above = kind == "electron"
        height = 1.35 if above else -1.05
        ax.text(
            p[0], p[1], p[2] + height, label, color=color, fontsize=11, ha="center", fontweight="bold"
        )
        ax.text(
            p[0],
            p[1],
            p[2] + height - 0.5,
            f"p = ({px}, {py}, {pz})   m = {entry['values']['mass'][0]}   q = {entry['values']['charge'][0]:+d}",
            color=color,
            fontsize=8.5,
            ha="center",
        )
    _unclip(ax)
    total = tuple(sum(m[i] for m in momenta.values()) for i in range(3))
    fig.text(
        0.03,
        0.93,
        "Electron and positron: bounded rational elastic contact",
        color=INK,
        fontsize=17,
        fontweight="bold",
    )
    fig.text(
        0.03,
        0.88,
        f"tick {tick:03d}   periodic 17³ lattice, plane z = {z}   one Node per 12 ticks at |p| = 1000, m = 1000",
        color=DIM,
        fontsize=10.5,
    )
    fig.text(
        0.03,
        0.04,
        f"total momentum {tuple(str(v) for v in total)}   total charge 0   total mass 2000   conserved at every completed tick: {timeline['conserved']}",
        color=INK,
        fontsize=10,
    )
    fig.text(
        0.97, 0.04, "recorded receptions only; nothing interpolated", color=DIM, fontsize=8.5, ha="right"
    )
    return fig


def _reaction_caption(events: list[dict[str, Any]], tick: int, rules: dict[str, dict[str, Any]]) -> str:
    parts = []
    for event in events:
        if event["tick"] != tick:
            continue
        rule = rules[event["rule"]]
        left, right = rule["left_type"], rule["right_type"]
        inputs = [SYMBOLS[left][0]] + ([] if right == "vacuum_slot" else [SYMBOLS[right][0]])
        outputs = [SYMBOLS[rule["output_types"][s]][0] for s in ("left", "right")]
        parts.append(" + ".join(inputs) + "  \u2192  " + " + ".join(outputs) + f"   ({rule['name']})")
    return "     ".join(parts)


def draw_reaction_frame(
    frame: dict[str, Any],
    scenario: str,
    shape: list[int],
    events: list[dict[str, Any]],
    rules: dict[str, dict[str, Any]],
    plt: Any,
    line: Any,
) -> Any:
    fig, ax = _figure(plt)
    ax.set_box_aspect((shape[0], shape[1], 3), zoom=2.2)
    ax.set_xlim(-0.5, shape[0] - 0.5)
    ax.set_ylim(-0.5, shape[1] - 0.5)
    ax.set_zlim(0, 2)
    ax.view_init(elev=38, azim=-90)
    _grid_plane(ax, shape, 1, line)
    tick = frame["tick"]
    fired = {tuple(e["position"]) for e in events if e["tick"] == tick}
    for position in fired:
        _glow(ax, list(position), FLASH, 320)
    for node in frame["nodes"]:
        p = node["position"]
        stack = 0
        for record in node["disturbances"]:
            kind = record["type"]
            symbol, color = SYMBOLS.get(kind, (kind, INK))
            if kind == "vacuum_slot":
                ax.scatter(
                    [p[0]],
                    [p[1]],
                    [p[2]],
                    s=60,
                    facecolors="none",
                    edgecolors=color,
                    linewidths=0.9,
                    depthshade=False,
                )
                continue
            values = record["values"]
            energy, momentum_vector = values["energy"][0], values["momentum"]
            _glow(ax, p, color, 150 if kind not in ("photon",) else 110)
            if any(momentum_vector):
                norm = sum(abs(c) for c in momentum_vector)
                ax.quiver(
                    p[0],
                    p[1],
                    p[2],
                    1.3 * momentum_vector[0] / norm,
                    1.3 * momentum_vector[1] / norm,
                    0,
                    color=color,
                    linewidth=1.8,
                    arrow_length_ratio=0.35,
                )
            label = f"{kind.replace('_', ' ')}  {symbol}"
            detail = f"E = {energy / 10:g} MeV   p = ({momentum_vector[0] / 10:g}, {momentum_vector[1] / 10:g}, 0)   q = {values['charge'][0]:+d}"
            dy = 0.9 + 1.15 * stack
            ax.text(
                p[0],
                p[1] + dy,
                p[2] + 0.4,
                label,
                color=color,
                fontsize=9.5,
                ha="center",
                fontweight="bold",
            )
            ax.text(p[0], p[1] + dy - 0.38, p[2] + 0.4, detail, color=color, fontsize=7.2, ha="center")
            stack += 1
    _unclip(ax)
    caption = _reaction_caption(events, tick, rules)
    fig.text(
        0.03, 0.93, REACTION_SCENARIOS[scenario]["title"], color=INK, fontsize=16, fontweight="bold"
    )
    fig.text(
        0.03,
        0.88,
        f"tick {tick:02d}   open 15 x 15 x 3 lattice, plane z = 1   configured two-record conversions; energy, momentum, charge, lepton and baryon numbers are conserved inventories",
        color=DIM,
        fontsize=9.5,
    )
    fig.text(
        0.03,
        0.04,
        caption
        if caption
        else "records move one Node per tick along their unit direction; vacuum slots are the configured decay locations",
        color=INK if caption else DIM,
        fontsize=11 if caption else 9.5,
    )
    fig.text(
        0.97,
        0.005,
        "energies and momenta in MeV from recorded values (units of 0.1 MeV); rest masses are not enforced on the shell",
        color=DIM,
        fontsize=8,
        ha="right",
    )
    return fig


def _image(fig: Any, plt: Any) -> Any:
    from PIL import Image

    buffer = BytesIO()
    fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def _save_gif(images: list[Any], durations: list[int], target: Path) -> None:
    images[0].save(
        target, save_all=True, append_images=images[1:], duration=durations, loop=0, optimize=False
    )


# ---------------------------------------------------------------- experiments


def run_backscatter(output: Path) -> dict[str, Any]:
    case_dir = _run(
        backscatter_configuration(), output, "electron_positron_backscatter", visualize=False
    )
    timeline = backscatter_timeline(case_dir)
    before = timeline["records"][timeline["contact_ticks"][0] - 12]
    after = timeline["records"][timeline["contact_ticks"][0] + 12]
    return {
        "case": case_dir.name,
        "contact_ticks": timeline["contact_ticks"],
        "momenta_before": {k: [str(v) for v in momentum(before[k]["values"])] for k in before},
        "momenta_after": {k: [str(v) for v in momentum(after[k]["values"])] for k in after},
        "final_totals": timeline["final_totals"],
        "conserved": timeline["conserved"],
        "timeline": timeline,
    }


def run_reactions(output: Path) -> dict[str, Any]:
    results = {}
    for name in REACTION_SCENARIOS:
        case_dir = _run(reaction_configuration(name), output, "reaction_" + name, visualize=True)
        frames = recorded_frames(case_dir)
        summary = reaction_summary(case_dir, frames)
        assert summary["accounting_balanced"], name
        results[name] = {"case": case_dir.name, "frames": frames, "summary": summary}
    return results


def render_reactions(output: Path, reactions: dict[str, Any]) -> tuple[Path, ...]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Line3DCollection

    saved = []
    for name in reactions:
        saved.append(output / f"reaction_{name}.gif")
        saved.append(output / f"reaction_{name}_event.png")
    for path in saved:
        path.touch()
    with ArtifactLease(output, saved):
        for index, (name, result) in enumerate(reactions.items()):
            initialization = json.loads(
                (output / result["case"] / "initialization.json").read_text(encoding="utf-8")
            )
            rules = {r["name"]: r for r in initialization["interactions"]}
            events = result["summary"]["events"]
            event_ticks = {e["tick"] for e in events}
            images, durations = [], []
            for frame in result["frames"]:
                image = _image(
                    draw_reaction_frame(
                        frame, name, initialization["shape"], events, rules, plt, Line3DCollection
                    ),
                    plt,
                )
                hold = CONTACT_HOLD if frame["tick"] in event_ticks else 1
                images.extend([image] * hold)
                durations.extend([FRAME_MS] * hold)
                if frame["tick"] == min(event_ticks, default=-1):
                    image.save(saved[2 * index + 1])
            _save_gif(images, durations, saved[2 * index])
    return tuple(saved)


def render(output: Path, backscatter: dict[str, Any]) -> tuple[Path, ...]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Line3DCollection

    saved = [
        output / "electron_positron_backscatter.gif",
        output / "electron_positron_backscatter_contact.png",
    ]
    for path in saved:
        path.touch()
    with ArtifactLease(output, saved):
        timeline = backscatter["timeline"]
        images, durations = [], []
        for tick in timeline["ticks"]:
            image = _image(draw_backscatter_frame(timeline, tick, plt, Line3DCollection), plt)
            hold = CONTACT_HOLD if tick in timeline["contact_ticks"] else 1
            images.extend([image] * hold)
            durations.extend([FRAME_MS] * hold)
            if tick in timeline["contact_ticks"]:
                image.save(saved[1])
        _save_gif(images, durations, saved[0])
    return tuple(saved)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--no-render", action="store_true", help="run and summarize without matplotlib")
    args = parser.parse_args()
    out = args.output.resolve()
    validate_output_path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("use a new or empty output directory")
    out.mkdir(parents=True, exist_ok=True)
    backscatter = run_backscatter(out)
    reactions = run_reactions(out)
    summary = {
        "backscatter": {k: v for k, v in backscatter.items() if k != "timeline"},
        "reactions": {name: r["summary"] for name, r in reactions.items()},
    }
    if not args.no_render:
        summary["rendered"] = [str(p) for p in render(out, backscatter)]
        summary["rendered"] += [str(p) for p in render_reactions(out, reactions)]
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "rendered"}, indent=None)[:600])


if __name__ == "__main__":
    main()
