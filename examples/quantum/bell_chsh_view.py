"""Render saved two-wing Bell test runs as a three-dimensional animation.

The renderer reads recorded outputs of ``bell_chsh.py`` only: initialization
layers, ``events.jsonl`` receptions, ``run.json`` decision records and the
final ``state.json``. It never advances a world or interpolates a trajectory.
Every frame is one recorded tick. The arc drawn between the two members of the
pair marks that they belong to one joint state held by the quantum owner; it is
a display of a dependency, not a signal, a field or a Link.
"""

import argparse
import json
from fractions import Fraction
from io import BytesIO
from pathlib import Path
from typing import Any

from event_universe.retention import ArtifactLease, validate_output_path

BACKGROUND = "#0b1020"
INK = "#e8ecf4"
DIM = "#3a4562"
LATTICE = "#22304f"
REGISTER = "#2d7fb8"
PAIR = "#5ee6d0"
BOND = "#8fd3ff"
DETECTOR_A = "#ffb347"
DETECTOR_B = "#ff5fa2"
PLUS = "#7cf29a"
MINUS = "#ff7b7b"
SETTING_LABELS = {"a0": "Z", "a1": "X", "b0": "(3Z + 4X)/5", "b1": "(3Z - 4X)/5"}
HOLD_AT_MEASUREMENT = 3
SUMMARY_FRAMES = 8
FRAME_MS = 520
SUMMARY_MS = 900
ZOOM = 2.2
ELEVATION = 20


def _load_run(case_dir: Path) -> dict[str, Any]:
    """Collect the recorded facts of one run without reinterpreting them."""
    initialization = json.loads((case_dir / "initialization.json").read_text(encoding="utf-8"))
    report = json.loads((case_dir / "run.json").read_text(encoding="utf-8"))
    state = json.loads((case_dir / "state.json").read_text(encoding="utf-8"))
    program = initialization["event_program"]
    positions: dict[int, dict[str, list[int]]] = {}
    for line in (case_dir / "events.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["event"] == "received":
            positions.setdefault(event["tick"], {})[event["disturbance"]] = event["position"]
    positions[0] = {seed["type"]: seed["position"] for seed in initialization["seeds"]}
    records = {}
    for record in report["computation"]["resolver"]["records"]:
        decision = record["decision"]
        records[decision["register_index"]] = {
            "tick": decision["tick"],
            "weights": decision["weights"],
            "outcome": record["outcome"],
        }
    codes = {}
    for node in state["nodes"]:
        for record in node["disturbances"]:
            codes[record["type"]] = record["values"]["outcome"][0]
    return {
        "name": case_dir.name,
        "shape": initialization["shape"],
        "ticks": initialization["ticks"],
        "addresses": program["addresses"],
        "layers": program["layers"],
        "bindings": program["bindings"],
        "positions": positions,
        "records": records,
        "codes": codes,
    }


def _carriers_by_tick(run: dict[str, Any]) -> dict[int, tuple[set[int], str]]:
    """Which registers hold the pair after each recorded layer, and what the layer did."""
    layers = {layer["tick"]: layer["operations"] for layer in run["layers"]}
    carriers: set[int] = set()
    table: dict[int, tuple[set[int], str]] = {0: (set(), "Two detectors leave the boundaries")}
    for tick in range(1, run["ticks"] + 1):
        note = ""
        for operation in layers.get(tick, []):
            indices = operation["register_indices"]
            if "channel" in operation:
                note = "Dephasing channel: the basis record of one member is discarded"
            elif len(indices) == 1:
                carriers |= set(indices)
                note = f"Hadamard on the register at x = {run['addresses'][indices[0]][0]}"
            elif _is_swap(operation["matrix"]):
                carriers = (carriers - set(indices)) | (set(indices) - carriers)
                note = "SWAP gates carry each member one Link outward"
            else:
                carriers |= set(indices)
                note = (
                    f"Controlled-NOT on x = {run['addresses'][indices[0]][0]}, "
                    f"{run['addresses'][indices[1]][0]}: the Bell pair exists"
                )
        table[tick] = (set(carriers), note)
    return table


def _is_swap(matrix: list[list[Any]]) -> bool:
    """A recorded two-register matrix that exchanges the single-occupation keys 1 and 2."""
    return len(matrix) == 4 and matrix[1][2] != 0 and matrix[2][1] != 0 and matrix[1][1] == 0


def _measurement_note(run: dict[str, Any], tick: int) -> str:
    decisions = [r for r in run["records"].values() if r["tick"] == tick]
    if not decisions:
        return ""
    return "Detectors reach the wings; each wing decides locally at this tick"


def _outcome_text(record: dict[str, Any] | None) -> tuple[str, str]:
    if record is None:
        return "", INK
    return ("+1", PLUS) if record["outcome"] == 0 else ("-1", MINUS)


def _draw_lattice(ax: Any, shape: list[int], line: Any) -> None:
    xs, ys, zs = (range(n) for n in shape)
    points = [(x, y, z) for x in xs for y in ys for z in zs]
    ax.scatter(
        [p[0] for p in points],
        [p[1] for p in points],
        [p[2] for p in points],
        s=3,
        c=LATTICE,
        depthshade=False,
        linewidths=0,
    )
    segments = []
    for x, y, z in points:
        for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            if x + dx < shape[0] and y + dy < shape[1] and z + dz < shape[2]:
                segments.append([(x, y, z), (x + dx, y + dy, z + dz)])
    ax.add_collection3d(line(segments, colors=LATTICE, linewidths=0.4, alpha=0.6))


def _glow(ax: Any, x: float, y: float, z: float, color: str, base: float) -> None:
    for size, alpha in ((base * 9, 0.08), (base * 4, 0.18), (base * 1.8, 0.45), (base, 1.0)):
        ax.scatter([x], [y], [z], s=size, c=color, alpha=alpha, depthshade=False, linewidths=0)


def _draw_bond(ax: Any, a: list[int], b: list[int]) -> None:
    steps = 40
    xs, ys, zs = [], [], []
    for i in range(steps + 1):
        t = i / steps
        xs.append(a[0] + (b[0] - a[0]) * t)
        ys.append(a[1] + (b[1] - a[1]) * t)
        zs.append(a[2] + (b[2] - a[2]) * t + 1.6 * 4 * t * (1 - t))
    ax.plot(xs, ys, zs, color=BOND, linewidth=1.4, alpha=0.75, linestyle=(0, (4, 3)))


def _draw_frame(
    run: dict[str, Any], tick: int, setting: str, plt: Any, line: Any, azimuth: float
) -> Any:
    fig = plt.figure(figsize=(12, 5.6), dpi=100)
    fig.set_facecolor(BACKGROUND)
    ax = fig.add_axes([0.0, 0.02, 1.0, 0.86], projection="3d")
    ax.set_facecolor(BACKGROUND)
    ax.set_axis_off()
    shape = run["shape"]
    ax.set_box_aspect((shape[0], shape[1] * 1.4, shape[2] * 1.6), zoom=ZOOM)
    ax.set_xlim(-0.5, shape[0] - 0.5)
    ax.set_ylim(-0.6, shape[1] - 0.4)
    ax.set_zlim(-0.6, shape[2] + 0.6)
    ax.view_init(elev=ELEVATION, azim=azimuth)
    _draw_lattice(ax, shape, line)
    addresses = run["addresses"]
    ax.scatter(
        [a[0] for a in addresses],
        [a[1] for a in addresses],
        [a[2] for a in addresses],
        s=46,
        facecolors="none",
        edgecolors=REGISTER,
        linewidths=1.2,
        depthshade=False,
    )
    for index in (0, len(addresses) - 1):
        a = addresses[index]
        ax.text(
            a[0],
            a[1],
            a[2] - 1.5,
            "wing A" if index == 0 else "wing B",
            color=REGISTER,
            fontsize=9,
            ha="center",
        )
    carriers, note = _carriers_by_tick(run)[tick]
    members = sorted(addresses[i] for i in carriers)
    if len(members) == 2:
        _draw_bond(ax, members[0], members[1])
    for m in members:
        _glow(ax, m[0], m[1], m[2], PAIR, 60)
    positions = run["positions"].get(tick, {})
    decisions = run["records"]
    measured = tick >= min((r["tick"] for r in decisions.values()), default=10**9)
    for kind, color, register in (
        ("Detector A", DETECTOR_A, 0),
        ("Detector B", DETECTOR_B, len(addresses) - 1),
    ):
        p = positions.get(kind)
        if p is None:
            continue
        ax.scatter(
            [p[0]],
            [p[1]],
            [p[2]],
            s=110,
            c=color,
            marker="s",
            depthshade=False,
            edgecolors=INK,
            linewidths=0.6,
        )
        ax.text(
            p[0],
            p[1] + 0.3,
            p[2] - 1.2,
            kind[-1],
            color=color,
            fontsize=10,
            ha="center",
            fontweight="bold",
        )
        if measured:
            wing = addresses[register]
            text, tone = _outcome_text(decisions.get(register))
            _glow(ax, wing[0], wing[1], wing[2], tone, 40)
            ax.text(
                wing[0],
                wing[1],
                wing[2] + 1.9,
                text,
                color=tone,
                fontsize=15,
                ha="center",
                fontweight="bold",
            )
    for artist in (*ax.collections, *ax.lines, *ax.texts):
        artist.set_clip_on(False)
    label_a, label_b = setting[:2], setting[2:]
    fig.text(0.03, 0.93, "Bell test (CHSH) on the lattice", color=INK, fontsize=17, fontweight="bold")
    fig.text(
        0.03,
        0.875,
        f"Alice: {label_a} = {SETTING_LABELS[label_a]}     Bob: {label_b} = {SETTING_LABELS[label_b]}     tick {tick:02d}",
        color=INK,
        fontsize=11,
    )
    fig.text(
        0.03, 0.06, _measurement_note(run, tick) or note, color=PAIR if carriers else DIM, fontsize=11
    )
    if measured:
        a_code = run["codes"].get("Detector A")
        b_code = run["codes"].get("Detector B")
        fig.text(
            0.03,
            0.02,
            f"Classical outcome codes written into the detectors: A = {a_code}, B = {b_code}   (nine Links apart, same tick)",
            color=INK,
            fontsize=9.5,
            alpha=0.85,
        )
    fig.text(
        0.97,
        0.02,
        "dashed arc: one joint state held by the quantum owner, not a signal",
        color=DIM,
        fontsize=8.5,
        ha="right",
    )
    return fig


def _draw_summary(summary: dict[str, Any], plt: Any) -> Any:
    fig = plt.figure(figsize=(12, 5.6), dpi=100)
    fig.set_facecolor(BACKGROUND)
    exact = summary["exact"]
    control = summary["exact_control"]
    sampled = summary["sampled"]
    fig.text(0.05, 0.9, "Result", color=INK, fontsize=20, fontweight="bold")
    rows = [("setting", "correlation (exact)", "correlation (sampled)", "dephased control")]
    for key in ("a0b0", "a0b1", "a1b0", "a1b1"):
        rows.append(
            (
                f"{key[:2]} {key[2:]}",
                exact["correlations"][key],
                sampled["correlations"][key],
                control["correlations"][key],
            )
        )
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            fig.text(
                0.07 + c * 0.22,
                0.78 - r * 0.085,
                cell,
                color=INK if r else DIM,
                fontsize=12 if r else 10.5,
                fontweight="bold" if r == 0 else "normal",
            )
    fig.text(
        0.07,
        0.3,
        f"S = E(a0 b0) + E(a0 b1) + E(a1 b0) - E(a1 b1) = {exact['chsh']} = {float(Fraction(exact['chsh'])):.2f}",
        color=PAIR,
        fontsize=15,
        fontweight="bold",
    )
    fig.text(
        0.07,
        0.22,
        f"Local hidden-variable bound: 2.   Dephased control: {control['chsh']} = {float(Fraction(control['chsh'])):.2f}.   Sampled, {sampled['trials_per_setting']} trials per setting: {sampled['chsh']} = {sampled['chsh_decimal']:.2f}.",
        color=INK,
        fontsize=11,
    )
    fig.text(
        0.07,
        0.15,
        "Alice's weights are [4, 4] for every Bob setting; Bob's marginal is 1/2 for every Alice setting: no signalling.",
        color=INK,
        fontsize=11,
    )
    fig.text(
        0.07,
        0.07,
        "Exact integer model calculation with simulated tickets; settings are 3-4-5 rational stand-ins, so 2 sqrt(2) is not reachable.",
        color=DIM,
        fontsize=9.5,
    )
    return fig


def _image(fig: Any, plt: Any) -> Any:
    from PIL import Image

    buffer = BytesIO()
    fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def _select_runs(output: Path) -> list[tuple[str, Path]]:
    selected = []
    for key in ("a0b0", "a0b1", "a1b0", "a1b1"):
        candidates = sorted(output.glob(f"bell_{key}_trial_*")) or [output / f"bell_{key}_alice0"]
        if not candidates[0].is_dir():
            raise ValueError(f"no recorded run for setting {key} under {output}")
        selected.append((key, candidates[0]))
    return selected


def render_experiment(output: Path, target: Path | None = None) -> tuple[Path, ...]:
    """Write the animation and a few stills from the saved harness output."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Line3DCollection

    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    runs = _select_runs(output)
    target = output if target is None else target
    target.mkdir(parents=True, exist_ok=True)
    gif = target / "bell_chsh.gif"
    stills = [
        target / "bell_chsh_start.png",
        target / "bell_chsh_pair.png",
        target / "bell_chsh_measured.png",
        target / "bell_chsh_result.png",
    ]
    saved = [gif, *stills]
    for path in saved:
        path.touch()
    with ArtifactLease(target, saved):
        images = []
        durations = []
        for run_index, (key, case_dir) in enumerate(runs):
            run = _load_run(case_dir)
            measurement = min(r["tick"] for r in run["records"].values())
            for tick in range(run["ticks"] + 1):
                azimuth = -77 + 7 * (run_index * (run["ticks"] + 1) + tick) / (4 * (run["ticks"] + 1))
                fig = _draw_frame(run, tick, key, plt, Line3DCollection, azimuth)
                image = _image(fig, plt)
                hold = HOLD_AT_MEASUREMENT if tick == measurement else 1
                images.extend([image] * hold)
                durations.extend([FRAME_MS] * hold)
                if run_index == 0 and tick == 0:
                    image.save(stills[0])
                if run_index == 0 and tick == 2:
                    image.save(stills[1])
                if run_index == 0 and tick == measurement:
                    image.save(stills[2])
        result = _image(_draw_summary(summary, plt), plt)
        result.save(stills[3])
        images.extend([result] * SUMMARY_FRAMES)
        durations.extend([SUMMARY_MS] * SUMMARY_FRAMES)
        images[0].save(
            gif, save_all=True, append_images=images[1:], duration=durations, loop=0, optimize=False
        )
    return tuple(saved)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="directory written by bell_chsh.py")
    parser.add_argument(
        "--target", type=Path, help="where to write the animation; defaults to the output directory"
    )
    args = parser.parse_args()
    output = args.output.resolve()
    target = output if args.target is None else args.target.resolve()
    validate_output_path(target)
    for path in render_experiment(output, target):
        print(path)


if __name__ == "__main__":
    main()
