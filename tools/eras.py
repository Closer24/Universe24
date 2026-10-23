"""The eras' log of a world under the volume form, a host tool (docs/ENGINE.md section 5's readers; DESIGN section 2 (i); ALGEBRA.md, The board's interval is no observable, The mean's velocity is the content's, The stress's trace is the time line's): the world is loaded as tools/run_inputs.py loads it and stepped by the engine's own step, and after every interval the board's own readings are appended as one JSON line to `<world>.eras.jsonl` (`--out`), the file complete at any refusal, so that the log itself is the checkpoint and a refusal's interval is the record (the state is not saved): per held row of the content the eras as the board reads them (`board_readings.eras`: the mean level and its velocity with the remainders, each sourcing family's write summed over the Nodes, the mix's exponent, the trace's own residual, the three tension lines' means and their velocities, the seed Node's level against the other Nodes') and the uniform mode (`board_readings.uniform_mode`), per family of quanta its largest level, its quanta over the board and, where the world lays a whole packet, its share within one Link of the seed Node by the engine's own `Lattice.quanta`, its rulers and its Links' factors at the seed Node and the far Node (the well's depth beside, the time line at the two Nodes); the floats are the host's from the integers (U the fine reading (1 / (d + 1)) ln(SUM X / (N Gamma)) from the volume's sums where the row carries its volume, with `U_level` the level reading's own beside it, and the level's U otherwise; the velocity in levels per interval from U's difference, H = v / Gamma, n_eff, the residual R_nat from that velocity, R_vol from the sums over three intervals, the seed's contrast U_seed - U_void and the clock ratio e^(-(U_seed - U_void))); a line every `--every` intervals on the standard output with the elapsed seconds, and at the end the spans' readings, the estimator of q on the integers' staircase (the symmetry hand's): over spans of `--span` intervals the slope of 1 / v gives n_eff = 2 Gamma d(1 / v) / dt, q_board = n_eff / 2 - 1 and q_p = q_board - 1, read where the velocity is above 0 at both ends of the span. With `--clicks <world>.clicks.jsonl` the NodeDetectors' lines of the same run are kept beside the eras log (the clicks, `reports.click`, the net current of a family into a declared region through its front Ports, the density readings, `reports.density`, and where an instrument body draws, its credit lines, the click written on the lattice, with the lay lines of that write), and after every interval one `detector` line per NodeDetector with the time line's level X at its Nodes and every family of quanta's share and quanta at its Nodes (the engine's own `Lattice.share_of` and `Lattice.quanta`, readings and no act): what the detector sees of what reaches it, history kept and never run back (ALGEBRA.md, The one Node: the click is the one act that makes a cycle new). With `--nodes <world>.nodes.jsonl` the Nodes' own readings are kept per interval for the torus view (tools/look/torus_page.py): X at every Node, the Link's length e^U from it, the Nodes the fifth act turned this interval and every Node's direction of time, and every family's quanta per Node (`node_lines`). The tool reads the board and sums over it (a reading, no act: the owner's locality decision of 2026-10-22) and computes nothing of the law; the page tools/look/eras_page.py draws the log.

Run with PYTHONPATH set to the checkout's src, at nice 15 for a long run:

    PYTHONPATH=src nice -n 15 python tools/eras.py <world>.json --every 100 --span 50 --out <world>.eras.jsonl [--clicks <world>.clicks.jsonl]
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import board_readings, node, records
from event_universe.bookings import sources_of
from event_universe.features import volume
from event_universe.features.read import link_tensions
from event_universe.lattice import Lattice
from event_universe.reports import ball
from event_universe.world_files import load_world

Node = tuple[int, int, int]


def kept_lines(board: Lattice) -> dict[records.Sourcing, list[records.Record]]:
    """Every record of quanta's lines copied before the step, the lines the forms are read against after it (`records.form` on the lines before and after, the bookings the write took, the symmetry hand's probe's way)."""
    return {
        source: [
            records.Record(r.now.copy(), r.before.copy(), r.remainder) for r in board.lines_of(*source)
        ]
        for source in sources_of(board.families, board.order)
    }


def seed_nodes(board: Lattice) -> tuple[Node, Node] | None:
    """The seed Node, the first whole packet's at the file's coordinates, and the far Node, half the board away on every axis through the wrap; None where the world lays no whole packet."""
    if not board.world.wholes:
        return None
    at = tuple(a + o for a, o in zip(board.world.wholes[0].at, board.offset, strict=True))
    far = tuple(int((a + extent // 2) % extent) for a, extent in zip(at, board.shape, strict=True))
    return (at[0], at[1], at[2]), (far[0], far[1], far[2])


def at_node(array: Any, where: Node, shape: tuple[int, int, int]) -> int:
    """One integer of a reading at a Node, a scalar reading spread over the board first."""
    return int((np.asarray(array, dtype=object) + np.zeros(shape, dtype=object))[where])


def row_line(board: Lattice, index: int, read: board_readings.Eras) -> dict[str, Any]:
    """One held row of the content's readings this interval as the log writes them: the integers of `Eras` and the host's floats from them; where the row carries its volume, U is the fine reading (1 / (d + 1)) ln(SUM X / (N Gamma)) from the record's sums (the reader's line on the first full run: the level reading is a staircase below one level per interval), the velocity Gamma times its difference over the interval, H and the trace's residual from that velocity, and `U_level` the level reading's own U, the clock's column; where the row is at its level, U is the level reading's and the velocity the level's difference with the remainders."""
    gamma = board.world.node_clock
    nodes = read.nodes
    velocity = (read.level - read.before) + (read.level_remainder - read.before_remainder) / nodes
    level = read.level + read.level_remainder / nodes
    fine = level / gamma  # the fine U where the row carries its volume, the level reading's U otherwise
    if read.volume != (0, 0):  # (1 / (d + 1)) ln(SUM X / (N Gamma)) and its difference, no staircase
        fine, earlier = (float(np.log(x / (nodes * gamma))) / volume.EXPONENT for x in read.volume)
        velocity = gamma * (fine - earlier)
    mix = read.mix[0] / read.mix[1] if read.mix[1] else None
    nature = read.nature[0] / read.nature[1] - 1 if read.nature[1] else None
    if read.volume != (0, 0) and read.nature[1]:  # the trace's residual from the fine velocity
        nature = 3 * board.writes[index].walls[0] * (nodes * velocity) ** 2 / read.nature[1] - 1
    line: dict[str, Any] = {
        "family": board.families[index].name,
        "level": read.level,
        "level_remainder": read.level_remainder,
        "before": read.before,
        "before_remainder": read.before_remainder,
        "nodes": nodes,
        "U": fine,
        "U_level": level / gamma,
        "velocity": velocity,
        "H": velocity / gamma,
        "writes": dict(read.writes),
        "n_eff": mix,
        "nature_residual": nature,
        "tension_means": [t / nodes for t in read.tensions],
        "tension_velocities": [
            (t - b) / nodes for t, b in zip(read.tensions, read.tensions_before, strict=True)
        ],
    }
    if read.volume != (
        0,
        0,
    ):  # the volume's record summed over the Nodes, the host's constraint from three
        line.update(volume=read.volume[0], volume_before=read.volume[1])
    if read.seed[2]:
        seed_level, void_sum, void_nodes = read.seed
        contrast = (seed_level - void_sum / void_nodes) / gamma
        line.update(seed_level=seed_level, void_level=void_sum / void_nodes, contrast=contrast)
        line["clock_ratio"] = float(
            np.exp(-contrast)
        )  # N_seed / N_void, the wall observer's clock against the void's
    return line


def quanta_line(board: Lattice, index: int, seed: tuple[Node, Node] | None) -> dict[str, Any]:
    """One family of quanta's readings this interval: its largest level (against the amplitude bound), its quanta over the board (the engine's own `Lattice.quanta`, None over a board holding a frozen Node) and, where a seed Node stands, its share within one Link of the seed over its share on the board, its rulers at the far Node (the clock and the three axis paces of its read, the page's h_a = p_0 / p_a) and its Links' factors (q_+ + q_-) / (2 Gamma) per axis at the seed Node and the far Node (the tension's reach into the write's paces, the second smoke's finding); where the read refuses by name (a Link's tension beyond Gamma after this interval's write, features/read.link_tensions), the reading carries the refusal's words under `refused_reading` and the next step refuses the run by name, so that the log is complete at the refusal."""
    lines, gamma, shape = board.record(index), board.world.node_clock, board.shape
    found: dict[str, Any] = {
        "largest": max(int(np.abs(np.asarray(line.now, dtype=object)).max()) for line in lines)
    }
    try:
        quanta, frozen = board.quanta(index)
    except ValueError as refusal:  # a reading never refuses the run: the next step does, by name
        found["refused_reading"] = str(refusal)
        return found
    total = int(quanta.sum(dtype=object))
    found.update(quanta=total, frozen=int(frozen.sum()))
    if seed is not None:
        near = ball(board.shape, seed[0], 1, board.wrap)
        within = int(quanta[near].sum(dtype=object))
        found.update(within_one_link=within)
        found["share_within_one_link"] = within / total if total else None
        clock, paces = node.rulers(index, board.families, board.states, -1, board.wrap, gamma, 0)
        found["rulers_far"] = [
            at_node(clock, seed[1], shape),
            [at_node(p, seed[1], shape) for p in paces],
        ]
        _content, axes = node.read_lines(index, board.families, board.states, -1, gamma, 0)
        tensions = link_tensions(axes, board.wrap, gamma)
        for name, where in (("links_seed", seed[0]), ("links_far", seed[1])):
            found[name] = [
                (
                    2 * gamma
                    - at_node(tensions[2 * a], where, shape)
                    - at_node(tensions[2 * a + 1], where, shape)
                )
                / (2 * gamma)
                for a in range(3)
            ]
    return found


def interval_line(
    board: Lattice,
    kept: dict[records.Sourcing, list[records.Record]],
    seconds: float,
) -> dict[str, Any]:
    """The log's line after one interval: the eras per held row of the content the uniform mode, the families of quanta's readings, the time line at the seed Node and the far Node where a seed stands, the Nodes the fifth act turned this interval (`fires`, the swap at the top's own reading, `Lattice.swaps`), the elapsed seconds."""
    forms = {source: records.form(lines, board.lines_of(*source)) for source, lines in kept.items()}
    rulers = board.rulers(
        -1
    )  # the write's rulers at the interval's start, read from the held rows' before
    seed = seed_nodes(board)
    fires = sum(nodes for at, direction, nodes in board.swaps if at == board.interval and direction == 1)
    line: dict[str, Any] = {
        "interval": board.interval,
        "seconds": seconds,
        "fires": fires,
        "horizon": len(horizon_links(board)),  # the Links at the wall (ALGEBRA.md, The horizon)
        "rows": {},
        "quanta": {},
    }
    for index in board.held:
        family = board.families[index]
        if family.wronskian:
            continue
        read = board_readings.eras(board, index, forms, rulers)
        line["rows"][family.name] = row_line(board, index, read)
        if seed is not None:
            time_line = board.states[index].lines[0].now
            at, far = at_node(time_line, seed[0], board.shape), at_node(time_line, seed[1], board.shape)
            line["rows"][family.name].update(at_seed=at, at_far=far, well=at - far)
    for index in board.order:
        line["quanta"][board.families[index].name] = quanta_line(board, index, seed)
    return line


def volume_residuals(previous: dict[str, Any] | None, line: dict[str, Any]) -> None:
    """The volume form's own constraint read on each held row that carries its volume, from the board's sums of X over three intervals (the derivation M12a: the Lagrangian's energy E = 0 reached from rest as -X_0 / X, the test of the law's course): R_vol = X'^2 / (2 X X'') - 1 with X' = X(t) - X(t - 1) this interval's and X'' = X' less the previous interval's X', written on this interval's row where both stand and X'' is not 0; None otherwise."""
    for name, row in line["rows"].items():
        if "volume" not in row:
            continue
        speed = row["volume"] - row["volume_before"]
        before = previous["rows"].get(name) if previous else None
        if before is None or "volume" not in before:
            row["volume_residual"] = None
            continue
        force = speed - (before["volume"] - before["volume_before"])
        row["volume_residual"] = speed * speed / (2 * row["volume"] * force) - 1 if force else None


def spans(lines: list[dict[str, Any]], family: str, span: int, gamma: int) -> list[dict[str, Any]]:
    """The estimator on the integers' staircase over spans of `span` intervals (the symmetry hand's section 10; DESIGN section 2 (h)): from the mean velocity v at the span's two ends, both above 0, the slope of 1 / v over the span, n_eff = 2 Gamma d(1 / v) / dt, q_board = n_eff / 2 - 1 and q_p = q_board - 1; one row per span with its U at the start."""
    found = []
    rows = [line["rows"][family] for line in lines if family in line.get("rows", {})]
    for start in range(0, len(rows) - span, span):
        first, last = rows[start], rows[start + span]
        if first["velocity"] <= 0 or last["velocity"] <= 0:
            continue
        slope = (1 / last["velocity"] - 1 / first["velocity"]) / span
        n_eff = 2 * gamma * slope
        found.append(
            {
                "interval": lines[start]["interval"],
                "U": first["U"],
                "velocity": first["velocity"],
                "n_eff": n_eff,
                "q_board": n_eff / 2 - 1,
                "q_p": n_eff / 2 - 2,
            }
        )
    return found


def header_of(path: Path, board: Lattice, intervals: int | None) -> dict[str, Any]:
    """The log's first line: the world's own numbers and the held rows by name (the page's legend names the hypotheses under their keys)."""
    world = board.world
    held = [family.name for family in world.families if family.held and not family.wronskian]
    return {
        "world": path.name,
        "node_clock": world.node_clock,
        "quantum_action": world.quantum_action,
        "width": world.width.bit_length(),
        "shape": list(world.shape),
        "families": [family.name for family in world.families],
        "held": held,
        "amplitude_bound": world.amplitude_bound,
        "intervals": world.intervals if intervals is None else intervals,
    }


def detector_lines(board: Lattice) -> list[dict[str, Any]]:
    """One `detector` line per NodeDetector after the interval: the time line's level X of the first held row at its Nodes (in the file's order of its positions) and, per family of quanta, the record's share and its quanta at those Nodes (`Lattice.share_of`, `Lattice.quanta`; None where a reading refuses by name), the readings a one-way clock at the detector keeps beside its clicks."""
    found: list[dict[str, Any]] = []
    time_line = board.states[board.held[0]].lines[0].now if board.held else None
    for detector in board.node_detectors:
        if detector.nodes is None:
            continue
        where = tuple(np.argwhere(detector.nodes).T)
        line: dict[str, Any] = {
            "event": "detector",
            "interval": board.interval,
            "node_detector": detector.name,
            "share": {},
            "quanta": {},
        }
        if time_line is not None:
            line["X"] = [int(x) for x in np.asarray(time_line, dtype=object)[where]]
        for index in board.order:
            name = board.families[index].name
            try:
                share = board.share_of(index)[0]
                quanta = board.quanta(index)[0]
            except ValueError:  # a reading refuses by name and the run's next step refuses the run
                line["share"][name] = line["quanta"][name] = None
                continue
            line["share"][name] = [int(x) for x in np.asarray(share, dtype=object)[where]]
            line["quanta"][name] = [int(x) for x in np.asarray(quanta, dtype=object)[where]]
        found.append(line)
    return found


def node_lines(board: Lattice, before: Any, directions: list[int]) -> dict[str, Any]:
    """The Nodes' own readings after the interval, one line per interval for the torus view (tools/look/torus_page.py): the first held row's level X at every Node in x-major order, the Link's length at every Node e^U = (X / Gamma)^(1 / (d + 1)) from that level (the volume form's reading, `volume.EXPONENT`), the Nodes turned by the fifth act this interval (the Node's level before after the interval equal to its level now before it and its level now equal to its level before: the swap at the top's own footprint, a reading of the two time lines kept across the step) and every Node's direction of time, +1 forward and -1 turned, flipped at each of its turns since the start (`directions`, carried by the caller), and every family of quanta's quanta at every Node."""
    index = board.held[0]
    line = board.states[index].lines[0]
    now = [int(x) for x in np.asarray(line.now, dtype=object).reshape(-1)]
    before_now, before_before = before
    turned = [
        i
        for i, (n, b) in enumerate(
            zip(now, [int(x) for x in np.asarray(line.before, dtype=object).reshape(-1)], strict=True)
        )
        if b == before_now[i] and n == before_before[i] and before_before[i] <= before_now[i] and n != b
    ]
    for i in turned:
        directions[i] = -directions[i]
    gamma = board.world.node_clock
    found: dict[str, Any] = {
        "interval": board.interval,
        "X": now,
        "length": [round(float((x / gamma) ** (1 / volume.EXPONENT)), 6) if x > 0 else 0.0 for x in now],
        "turned": turned,
        "direction": list(directions),
        "quanta": {},
    }
    for i in board.order:
        try:
            quanta = board.quanta(i)[0]
        except ValueError:
            continue
        found["quanta"][board.families[i].name] = [
            int(q) for q in np.asarray(quanta, dtype=object).reshape(-1)
        ]
    found["horizon"] = horizon_links(board)
    return found


def horizon_links(board: Lattice) -> list[list[int]]:
    """The Links at the wall after the interval, the horizon (ALGEBRA.md, The horizon, 2026-10-23): every Link whose factor the read gives at 0 and the world does not cut (board_readings.horizon_ports on the first family of quanta, the tension being the Link's and no family's), as pairs of the two Nodes' x-major indexes through the +a Ports; a reading for the torus view, no act."""
    if not board.order:
        return []
    ports = board_readings.horizon_ports(board, board.order[0])
    if ports is None:
        return []
    shape, found = board.shape, []
    for axis in range(3):
        for at in np.argwhere(np.asarray(ports[2 * axis], dtype=bool)):
            far = list(at)
            far[axis] = (far[axis] + 1) % shape[axis]
            found.append(
                [
                    int(np.ravel_multi_index(tuple(at), shape)),
                    int(np.ravel_multi_index(tuple(far), shape)),
                ]
            )
    return found


def run(
    path: Path,
    out: Path,
    every: int,
    intervals: int | None,
    clicks: Path | None = None,
    nodes: Path | None = None,
) -> list[dict[str, Any]]:
    """The world stepped and logged: one JSON line per interval appended to `out` as it goes (the file begun with the world's own numbers), a refusal written as the last line with its reason and the interval; the lines returned; with `clicks`, the NodeDetectors' click and density lines and the `detector` readings appended to that file as they come, history kept."""
    world = load_world(path)
    kept_clicks = clicks.open("w", encoding="utf-8") if clicks is not None else None

    def keep(line: dict[str, object]) -> None:
        if kept_clicks is not None and line.get("event") in (
            "click",
            "density",
            "credit",
            "lay",
            "birth",
        ):
            kept_clicks.write(json.dumps(line) + "\n")

    board = Lattice(world, output=keep)
    kept_nodes = nodes.open("w", encoding="utf-8") if nodes is not None else None
    directions = [1] * int(np.prod(board.shape))
    lines: list[dict[str, Any]] = []
    began = time.perf_counter()
    with out.open("w", encoding="utf-8") as log:
        log.write(json.dumps(header_of(path, board, intervals)) + "\n")
        for _ in range(world.intervals if intervals is None else intervals):
            kept = kept_lines(board)
            time_line = board.states[board.held[0]].lines[0] if board.held else None
            before = (
                (
                    [int(x) for x in np.asarray(time_line.now, dtype=object).reshape(-1)],
                    [int(x) for x in np.asarray(time_line.before, dtype=object).reshape(-1)],
                )
                if time_line is not None
                else None
            )
            try:
                board.step()
            except (ValueError, RuntimeError) as refusal:
                line = {
                    "interval": board.interval,
                    "refused": str(refusal),
                    "seconds": time.perf_counter() - began,
                }
                log.write(json.dumps(line) + "\n")
                print(json.dumps(line))
                break
            line = interval_line(board, kept, time.perf_counter() - began)
            volume_residuals(lines[-1] if lines else None, line)
            lines.append(line)
            log.write(json.dumps(line) + "\n")
            log.flush()
            if kept_clicks is not None:
                for seen in detector_lines(board):
                    kept_clicks.write(json.dumps(seen) + "\n")
                kept_clicks.flush()
            if kept_nodes is not None and before is not None:
                kept_nodes.write(json.dumps(node_lines(board, before, directions)) + "\n")
                kept_nodes.flush()
            if board.interval % every == 0:
                rows = {
                    name: (round(row["U"], 3), round(row["velocity"], 2))
                    for name, row in line["rows"].items()
                }
                print(
                    json.dumps(
                        {"interval": board.interval, "seconds": round(line["seconds"], 1), "U_v": rows}
                    )
                )
            if board.ended is not None:
                break
    if kept_clicks is not None:
        kept_clicks.close()
    if kept_nodes is not None:
        kept_nodes.close()
    return lines


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the world file, its mode file beside it")
    parser.add_argument(
        "--every", type=int, required=True, help="a line on the standard output every so many intervals"
    )
    parser.add_argument(
        "--span",
        type=int,
        default=None,
        help="the spans of the estimator at the end (--every where omitted)",
    )
    parser.add_argument(
        "--intervals", type=int, default=None, help="the intervals to run (the world's own)"
    )
    parser.add_argument("--out", type=Path, default=None, help="the log (<world>.eras.jsonl)")
    parser.add_argument(
        "--nodes",
        type=Path,
        default=None,
        help="the Nodes' own readings per interval for the torus view (<world>.nodes.jsonl)",
    )
    parser.add_argument(
        "--clicks",
        type=Path,
        default=None,
        help="the NodeDetectors' lines of the same run kept beside the log (<world>.clicks.jsonl)",
    )
    args = parser.parse_args(argv)
    if args.every < 1:
        raise ValueError(f"--every takes an integer from 1, got {args.every}")
    out = args.out if args.out is not None else args.world.with_suffix(".eras.jsonl")
    lines = run(args.world, out, args.every, args.intervals, args.clicks, args.nodes)
    gamma = load_world(args.world).node_clock
    span = args.span if args.span is not None else args.every
    for family in sorted({name for line in lines for name in line.get("rows", {})}):
        for row in spans(lines, family, span, gamma):
            print(
                json.dumps(
                    {
                        "family": family,
                        "span": span,
                        **{k: round(v, 3) if isinstance(v, float) else v for k, v in row.items()},
                    }
                )
            )
    print(json.dumps({"log": str(out), "intervals": len(lines)}))


if __name__ == "__main__":
    main()
