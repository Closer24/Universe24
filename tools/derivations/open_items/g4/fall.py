"""Hand g4, brief m, parts (c) and (d): one body of the heavy lift on the bare torus with the sea emptied, the volume
held by hand, measured on the branch's engine (no edit of src/). The lay: the universe {den, Gamma 1000, T 36000},
the cube, the point family whose g lies nearest --g; the light emptied (tests/laws_universe.light_emptied); the
volume holder's time line set by hand EVERY interval (tests/laws_universe.time_line_set) to (now, before) =
(X(c), X(c) + 1), the level before one unit above the level now, so that no Node is at a weak maximum and the swap
at the top never fires (ALGEBRA.md, The swap at the top: the trigger X0 <= X1 >= X2; on the flat empty gapped
board every Node turns every interval, W1), the content c(r) = depth div (1 + r) about the well's centre (r the
Manhattan distance on the torus; W2's profile), or flat (--depth 0 or --mode flat). The body: one quantum of the
family's record laid through the engine's one lay act (lay.laid) as a Gaussian packet at rest about its lay Node,
re_now = A e^(-r^2 / (4 sigma^2)) to the unit, the level before turned back by the local rest rotation
(re_before = (re_now K) div W, im_before = sense (re_now S) div W with K = den Gamma^2 - (den - num) p_0(c)^2,
W = den Gamma^2 and S = isqrt(W^2 - K^2)), A scaled so that the record's share reads one quantum of its unit;
sigma 0 lays the one-Node quarter-turn pixel as the click lays it. Modes: well (the fall), flat (the control),
pair (two bodies three Links apart on a flat board, the volume NOT set by hand but pumped: the sea's uniform write
stood in for by (4 X) div Gamma laid at every Node each interval, so the bodies' own wells stand and no Node tops),
clock (flat at --depth c everywhere, the beat read from the record's upward zero crossings at the peak Node).
Readings per interval, integers only: the peak Node, the share total S and the share within 1, 2, 3 Links of the
peak in thousandths of S, the centroid along z about the lay Node as (1000 M_z) div S, the rms radius about the
centroid in milli Links, the content c at the peak, the turned Nodes, the upward crossings at the lay Node and the
peak. The run back: the volume holder's post-step state snapshotted every interval and restored before each
inverse step, every array compared with the laid state at interval 0 (MATCH or the count of differing arrays).

    python tools/derivations/g4/fall.py --den 348893 --g 0.74 --cube 9 --mode well --depth 300 --offset 3 --sigma-tenths 15 --intervals 200 --run-back
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from math import isqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from event_universe import records, share, world_files  # noqa: E402
from event_universe.core.paces import clock_alone  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import light_emptied, node_arrays, time_line_set  # noqa: E402

GAMMA, ACTION = 1000, 36000


def offsets(shape: tuple[int, ...], origin: tuple[int, int, int]) -> np.ndarray:
    """The signed torus offset of every Node from `origin` per axis, the shorter way: shape (3, X, Y, Z)."""
    coords = np.indices(shape)
    found = np.zeros_like(coords)
    for a in range(3):
        n = shape[a]
        d = (coords[a] - origin[a]) % n
        found[a] = np.where(d > n // 2, d - n, d)
    return found


def manhattan(shape: tuple[int, ...], origin: tuple[int, int, int]) -> np.ndarray:
    return np.abs(offsets(shape, origin)).sum(axis=0)


def hand_volume(board: Lattice, levels: np.ndarray) -> None:
    """The volume holder's time line set by hand: now = X(c), before = X(c) + 1 at every Node (the falling triple: no weak maximum, the swap never fires)."""
    x = volume.volume_of(GAMMA, np.asarray(levels, dtype=object))
    time_line_set(board, x, x + 1)


def record_share_int(board: Lattice, k: int, r: int) -> np.ndarray:
    content, factors = board.read(k, 1, r)
    own = share.family_share(board.families[k], board.lines_of(k, r), GAMMA, content, factors, board.unit)
    return np.asarray(own, dtype=object)


def lay_packet(board: Lattice, k: int, r: int, at: tuple[int, int, int], sigma_tenths: int, sense: int, kind: object, quanta: int = 1) -> dict:
    """One quantum of the record `r` of the family `k` laid about `at` as a Gaussian packet at rest (sigma in tenths of a Link; 0 the one-Node quarter-turn lay), through the engine's lay act; returns the lay's integers."""
    family = board.families[k]
    num, den = family.pair
    first = records.record_slice(family, r).start
    shape = board.shape
    held = board.held[0]
    c_lay = int(volume.level_of(GAMMA, np.asarray(board.states[held].lines[0].now, dtype=object))[at])
    p0 = clock_alone(GAMMA, c_lay)
    w_rot = den * GAMMA * GAMMA
    k_rot = w_rot - (den - num) * p0 * p0  # cos omega at the content: K / W
    s_rot = isqrt(w_rot * w_rot - k_rot * k_rot)  # sin omega at the content, to the unit
    unit_k = board.credit.units[k]

    def levels(amplitude: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        re_now = np.zeros(shape, dtype=object)
        if sigma_tenths == 0:
            re_now[at] = amplitude
            re_before = np.zeros(shape, dtype=object)
            im_now = np.zeros(shape, dtype=object)
            im_before = np.zeros(shape, dtype=object)
            im_before[at] = sense * amplitude  # the click's quarter-turn lay: re (A, 0), im (0, sense A)
            return re_now, re_before, im_now, im_before
        off = offsets(shape, at)
        r2 = (off * off).sum(axis=0)
        sigma = sigma_tenths / 10
        for where in np.ndindex(*shape):
            re_now[where] = int(round(amplitude * math.exp(-float(r2[where]) / (4 * sigma * sigma))))
        re_before = np.vectorize(lambda v: (int(v) * k_rot) // w_rot, otypes=[object])(re_now)
        im_before = np.vectorize(lambda v: sense * ((int(v) * s_rot) // w_rot), otypes=[object])(re_now)
        im_now = np.zeros(shape, dtype=object)
        return re_now, re_before, im_now, im_before

    content, factors = board.read(k, 1, r)

    def share_of(amplitude: int) -> int:
        re_now, re_before, im_now, im_before = levels(amplitude)
        remainder = board.states[k].lines[first].remainder
        lines = [records.Record(re_now, re_before, remainder), records.Record(im_now, im_before, remainder)]
        found = share.family_share(family, lines, GAMMA, content, factors, board.unit)
        return int(np.asarray(found, dtype=object).sum())

    a0 = 2000
    s0 = share_of(a0)
    amplitude = isqrt(a0 * a0 * quanta * unit_k // s0)  # the share grows as A^2: `quanta` quanta of the record's unit
    for _ in range(3):  # the roundings of the levels: corrections toward the count
        s1 = share_of(amplitude)
        amplitude = isqrt(amplitude * amplitude * quanta * unit_k // s1)
    re_now, re_before, im_now, im_before = levels(amplitude)
    laid(board, k, first, (re_now.astype(kind), re_before.astype(kind)), None, None)
    laid(board, k, first + 1, (im_now.astype(kind), im_before.astype(kind)), None, None)
    total = int(record_share_int(board, k, r).sum())
    return {"amplitude": amplitude, "c_lay": c_lay, "p0_lay": p0, "cos_milli": (1000 * k_rot) // w_rot, "sin_milli": (1000 * s_rot) // w_rot, "share_total": total, "unit": unit_k, "quanta_milli": (1000 * total) // unit_k}


def readings(board: Lattice, k: int, r: int, at: tuple[int, int, int], axis: int = 2) -> dict:
    """The integer readings of one record."""
    s = record_share_int(board, k, r)
    s = np.where(np.asarray(s, dtype=object) > 0, s, 0)
    total = int(sum(int(v) for v in s.reshape(-1)))
    if total == 0:
        return {"total": 0}
    flat = [int(v) for v in s.reshape(-1)]
    peak_flat = max(range(len(flat)), key=flat.__getitem__)
    peak = tuple(int(x) for x in np.unravel_index(peak_flat, s.shape))
    off = offsets(s.shape, at)
    moments = [int(sum(int(v) * int(o) for v, o in zip(s.reshape(-1), off[a].reshape(-1)))) for a in range(3)]
    r2 = sum(int(v) * int(o2) for v, o2 in zip(s.reshape(-1), (off * off).sum(axis=0).reshape(-1)))
    var_micro = (10**6 * r2 * total - 10**6 * sum(m * m for m in moments)) // (total * total)
    d_peak = manhattan(s.shape, peak)
    within = [int(sum(int(v) for v, d in zip(s.reshape(-1), d_peak.reshape(-1)) if int(d) <= n)) for n in (0, 1, 2, 3)]
    held = board.held[0]
    c = volume.level_of(GAMMA, np.asarray(board.states[held].lines[0].now, dtype=object))
    return {
        "total": total,
        "peak": list(peak),
        "peak_offset": [int(off[a][peak]) for a in range(3)],
        "centroid_milli": [(1000 * m) // total for m in moments],
        "rms_milli": isqrt(max(var_micro, 0)),
        "within_milli": [(1000 * w) // total for w in within],
        "c_peak": int(c[peak]),
        "c_lay": int(c[at]),
        "share_lay_milli": (1000 * int(s[at])) // total,
    }


def snapshot_volume(board: Lattice) -> tuple:
    state = board.states[board.held[0]]
    return (
        [records.Record(np.array(l.now, copy=True), np.array(l.before, copy=True), np.array(l.remainder, copy=True)) for l in state.lines],
        [np.array(w, copy=True) for w in state.write_remainders],
    )


def restore_volume(board: Lattice, kept: tuple) -> None:
    state = board.states[board.held[0]]
    state.lines = [records.Record(np.array(l.now, copy=True), np.array(l.before, copy=True), np.array(l.remainder, copy=True)) for l in kept[0]]
    state.write_remainders = [np.array(w, copy=True) for w in kept[1]]


def snapshot_all(board: Lattice) -> dict:
    return {key: tuple(np.array(a, dtype=object, copy=True) for a in value) for key, value in node_arrays(board).items()}


def differing(a: dict, b: dict) -> list:
    found = []
    for key in sorted(set(a) | set(b), key=str):
        if key not in a or key not in b:
            found.append(key)
            continue
        for x, y in zip(a[key], b[key], strict=False):
            if np.shape(x) != np.shape(y) or not np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)):
                found.append(key)
                break
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--den", type=int, default=348893)
    parser.add_argument("--g", type=float, default=0.74)
    parser.add_argument("--cube", type=int, default=9)
    parser.add_argument("--mode", default="well", choices=("well", "flat", "pair", "clock"))
    parser.add_argument("--depth", type=int, default=300)
    parser.add_argument("--offset", type=int, default=3)
    parser.add_argument("--sigma-tenths", type=int, default=15)
    parser.add_argument("--senses", default="1,1")
    parser.add_argument("--separation", type=int, default=3)
    parser.add_argument("--pump", type=int, default=2, help="the uniform write per interval in units of X div Gamma (pair mode): the gapped line's own fall 2 X / Gamma made good, the start's margin kept")
    parser.add_argument("--margin", type=int, default=10, help="pair mode: the level now above the level before at the start, above the gapped line's fall 2 X / Gamma, so that no Node is at a weak maximum")
    parser.add_argument("--quanta", type=int, default=1, help="the quanta laid per body (1 the brief's one-quantum body; more for the integer budget's resolution, the dynamics linear)")
    parser.add_argument("--intervals", type=int, default=200)
    parser.add_argument("--run-back", action="store_true")
    parser.add_argument("--tag", default="")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    tag = args.tag or f"{args.mode}_den{args.den}_c{args.cube}_d{args.depth}_s{args.sigma_tenths}_o{args.offset}_q{args.quanta}_n{args.intervals}"
    out = here / f"fall_{tag}.jsonl"
    folder = Path(f"/dev/shm/tmp/g4_{tag}")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(json.dumps({"integers": {"den": args.den, "node_clock": GAMMA, "quantum_action": ACTION}}))
    (folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [args.cube] * 3, "intervals": args.intervals}))
    world_files.REPOSITORY_ROOT = folder
    lines_out: list[dict] = []
    board = Lattice(load_world(folder / "w.json"), output=lines_out.append)
    kind = board.kind
    light_emptied(board)
    point_families = [(i, f) for i, f in enumerate(board.families) if f.plane and f.quanta]
    k, family = min(point_families, key=lambda row: abs((row[1].pair[1] - row[1].pair[0]) / row[1].pair[1] - args.g))
    num, den = family.pair
    board.born_point(k)
    centre = (args.cube // 2,) * 3
    shape = board.shape
    # the volume by hand
    if args.mode == "well":
        levels = (args.depth // (1 + manhattan(shape, centre))).astype(object)
    else:
        levels = np.full(shape, args.depth, dtype=object)
    if args.mode == "pair":
        x0 = volume.volume_of(GAMMA, np.asarray(levels, dtype=object))
        time_line_set(board, x0, x0 - args.margin)  # the rising triple, the margin above the gapped line's fall; the pump keeps it
    else:
        hand_volume(board, levels)
    senses = [int(s) for s in args.senses.split(",")]
    bodies: list[tuple[int, int, tuple[int, int, int], int]] = []
    if args.mode == "pair":
        z0 = centre[2] - args.separation // 2
        bodies.append((k, 0, (centre[0], centre[1], z0 % args.cube), senses[0]))
        bodies.append((k, 1, (centre[0], centre[1], (z0 + args.separation) % args.cube), senses[1]))
    else:
        bodies.append((k, 0, (centre[0], centre[1], (centre[2] - args.offset) % args.cube), senses[0]))
    lays = [lay_packet(board, kk, rr, at, args.sigma_tenths, sense, kind, args.quanta) for kk, rr, at, sense in bodies]
    header = {
        "event": "header", "mode": args.mode, "den": args.den, "den_bits": args.den.bit_length(), "cube": args.cube,
        "family": family.name, "pair": [num, den], "g_milli": (1000 * (den - num)) // den, "sin_milli": isqrt(10**6 * (den * den - num * num) // (den * den)),
        "unit": board.credit.units[k], "width_bits": board.world.width.bit_length() if hasattr(board.world.width, "bit_length") else int(board.world.width), "kind": str(kind),
        "amplitude_bound": board.world.amplitude_bound, "depth": args.depth, "offset": args.offset, "sigma_tenths": args.sigma_tenths,
        "bodies": [[list(at), sense, rr] for kk, rr, at, sense in bodies], "lays": lays, "intervals": args.intervals, "pump": args.pump if args.mode == "pair" else None, "margin": args.margin if args.mode == "pair" else None, "quanta": args.quanta,
    }
    print(json.dumps(header), flush=True)
    rows: list[dict] = [header]
    start_state = snapshot_all(board)
    snapshots: list[tuple] = []
    crossings = {(kk, rr): 0 for kk, rr, _at, _s in bodies}
    last_sign = {}
    t0 = time.time()
    marks = {0, 1, 2, 5, 10, 20, 30, 50, 75, 100, 150, 200, 250, 300, args.intervals}

    def read_all(interval: int) -> dict:
        row = {"event": "reading", "interval": interval, "bodies": [], "turned": int(board.turned.sum()), "seconds": round(time.time() - t0, 1)}
        for kk, rr, at, _sense in bodies:
            found = readings(board, kk, rr, at)
            line = board.lines_of(kk, rr)[0]
            found["re_now_lay"], found["re_before_lay"] = int(line.now[at]), int(line.before[at])
            found["crossings_lay"] = crossings[(kk, rr)]
            found["beat_engine_lay"] = int(board.beats.get((kk, rr), np.zeros(shape, dtype=np.int64))[at])
            found["proper_lay"] = int(board.proper_count[at])
            row["bodies"].append(found)
        if len(bodies) == 2 and row["bodies"][0].get("total") and row["bodies"][1].get("total"):
            a, b = row["bodies"]
            lay_gap = (bodies[1][2][2] - bodies[0][2][2]) % args.cube
            if lay_gap > args.cube // 2:
                lay_gap -= args.cube
            row["separation_milli"] = 1000 * lay_gap + b["centroid_milli"][2] - a["centroid_milli"][2]
            row["peak_distance"] = int(manhattan(shape, tuple(a["peak"]))[tuple(b["peak"])])
        return row

    rows.append(read_all(0))
    print(json.dumps(rows[-1]), flush=True)
    for step in range(1, args.intervals + 1):
        before_lines = {key: np.array(board.lines_of(kk, rr)[0].now, copy=True) for key in crossings for kk, rr in [key]}
        board.step()
        for key in crossings:  # the upward zero crossings of the re line at the lay Node, counted on the step
            kk, rr = key
            at = next(b[2] for b in bodies if (b[0], b[1]) == key)
            now = int(board.lines_of(kk, rr)[0].now[at])
            if int(before_lines[key][at]) < 0 <= now:
                crossings[key] += 1
        snapshots.append(snapshot_volume(board))
        if args.mode == "pair":
            state = board.states[board.held[0]]
            line = state.lines[0]
            pumped = np.asarray(line.now, dtype=object) + (args.pump * np.asarray(line.now, dtype=object)) // GAMMA
            state.lines[0] = records.Record(pumped.astype(kind), line.before, line.remainder)
        else:
            hand_volume(board, levels)
        row = read_all(board.interval)
        rows.append(row)
        if board.interval in marks:
            print(json.dumps(row), flush=True)
    credits = [l for l in lines_out if isinstance(l, dict)]
    summary = {"event": "summary", "intervals": args.intervals, "seconds": round(time.time() - t0, 1), "output_lines": len(lines_out), "credit_lines": sum(1 for l in credits if l.get("event") == "credit"), "refused_lines": sum(1 for l in credits if l.get("event") == "refused")}
    if args.run_back:
        t1 = time.time()
        for step in range(args.intervals, 0, -1):
            restore_volume(board, snapshots[step - 1])
            board.step_inverse()
        diff = differing(start_state, snapshot_all(board))
        summary["run_back"] = "MATCH" if not diff else f"MISMATCH in {len(diff)} arrays: {[str(d) for d in diff[:6]]}"
        summary["run_back_seconds"] = round(time.time() - t1, 1)
    rows.append(summary)
    print(json.dumps(summary), flush=True)
    with out.open("w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    main()
