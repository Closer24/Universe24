"""Hand z1, parts (b), (c), (d): a seed world run N intervals on the branch's engine, the three logs written as
tools/eras.py writes them (the header, the eras, the nodes, the clicks) into an output folder for tools/record_gates.py,
and beside them this hand's integer readings per interval (`<tag>.readings.jsonl`): the light's quanta at the vacuum's
weight, the births and the refusals by cause, the turned Nodes, the level of the volume at the origin and the board's
least and largest content, the records standing, the largest record's quanta over the board and the count of records
within one Link of each other (part c), and for a bodies' seed each body's peak, centroid along z, share within one
Link, content at its centre against the board's and the proper count at its centre against the far Node (part d). With
`--run-back K N` the run back's verdict instead: tools/back_in_time.verdict over the window [K, K + N] (MATCH or MISS).

    PYTHONPATH=src python tools/derivations/open_items/H-Minimal-Seed-1/z1_run.py tools/derivations/open_items/H-Minimal-Seed-1/worlds/emergence_hole.json --intervals 300 --tag hole
    PYTHONPATH=src python tools/derivations/open_items/H-Minimal-Seed-1/z1_run.py tools/derivations/open_items/H-Minimal-Seed-1/worlds/emergence_hole.json --run-back 0 60
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from z1lib import ROOT, board_of, light_quanta, record_share  # noqa: E402

from event_universe import registry, share  # noqa: E402
from event_universe.features import volume  # noqa: E402


def loaded(name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def offsets(shape: tuple[int, ...], origin: tuple[int, int, int]) -> np.ndarray:
    coords = np.indices(shape)
    found = np.zeros_like(coords)
    for a in range(3):
        n = shape[a]
        d = (coords[a] - origin[a]) % n
        found[a] = np.where(d > n // 2, d - n, d)
    return found


def manhattan(shape: tuple[int, ...], origin: tuple[int, int, int]) -> np.ndarray:
    return np.abs(offsets(shape, origin)).sum(axis=0)


def body_reading(board, k: int, r: int, centre: tuple[int, int, int], far: tuple[int, int, int]) -> dict:  # type: ignore[no-untyped-def]
    """One record's integer readings: the total share, the peak Node, the centroid about `centre` in milli Links per axis, the share within one Link of the centre and of the peak in milli, the content at the centre and at the peak against the far Node's, the proper count at the centre and at the far Node."""
    s = record_share(board, k, r)
    s = np.where(np.asarray(s, dtype=object) > 0, s, 0)
    flat = [int(v) for v in s.reshape(-1)]
    total = sum(flat)
    gamma = board.world.node_clock
    held = board.held[0]
    c = volume.level_of(gamma, np.asarray(board.states[held].lines[0].now, dtype=object))
    found = {"record": r, "total": total, "c_centre": int(c[centre]), "c_far": int(c[far]), "proper_centre": int(board.proper_count[centre]), "proper_far": int(board.proper_count[far])}
    if total == 0:
        return found
    peak_flat = max(range(len(flat)), key=flat.__getitem__)
    peak = tuple(int(x) for x in np.unravel_index(peak_flat, s.shape))
    off = offsets(s.shape, centre)
    moments = [int(sum(int(v) * int(o) for v, o in zip(flat, off[a].reshape(-1), strict=True))) for a in range(3)]
    d_centre, d_peak = manhattan(s.shape, centre), manhattan(s.shape, peak)
    within_centre = sum(v for v, d in zip(flat, d_centre.reshape(-1), strict=True) if int(d) <= 1)
    within_peak = sum(v for v, d in zip(flat, d_peak.reshape(-1), strict=True) if int(d) <= 1)
    found.update(peak=list(peak), peak_offset=[int(off[a][peak]) for a in range(3)], centroid_milli=[(1000 * m) // total for m in moments], within_one_of_centre_milli=(1000 * within_centre) // total, within_one_of_peak_milli=(1000 * within_peak) // total, c_peak=int(c[peak]), quanta_milli=(1000 * total) // board.credit.units[k])
    return found


def records_reading(board) -> dict:  # type: ignore[no-untyped-def]
    """Part (c): every charged record standing, its quanta over the board (the share div its unit) and its peak Node; the largest record's quanta; the count of record pairs whose peaks stand within one Link of each other, and at the same Node."""
    rows = []
    for k in board.order:
        if not share.charged(board.families[k]):
            continue
        for r in registry.quanta_records(board.families, board.states, k):
            s = record_share(board, k, r)
            flat = [max(int(v), 0) for v in s.reshape(-1)]
            total = sum(flat)
            if total <= 0:
                continue
            peak_flat = max(range(len(flat)), key=flat.__getitem__)
            peak = tuple(int(x) for x in np.unravel_index(peak_flat, s.shape))
            unit = board.credit.units[k]
            above = sum(1 for v in flat if v >= unit)
            rows.append({"family": board.families[k].name, "pair": list(board.families[k].pair), "record": r, "quanta_milli": (1000 * total) // unit, "peak": list(peak), "peak_quanta_milli": (1000 * flat[peak_flat]) // unit, "nodes_above_one_quantum": above})
    shape = board.shape
    adjacent, same = 0, 0
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            d = int(manhattan(shape, tuple(rows[i]["peak"]))[tuple(rows[j]["peak"])])
            adjacent += d == 1
            same += d == 0
    largest = max((row["quanta_milli"] for row in rows), default=0)
    return {"records": len(rows), "largest_quanta_milli": largest, "peak_pairs_adjacent": adjacent, "peak_pairs_same_node": same, "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("world", type=Path)
    parser.add_argument("--intervals", type=int, default=300)
    parser.add_argument("--tag", default=None)
    parser.add_argument("--every", type=int, default=25)
    parser.add_argument("--run-back", nargs=2, type=int, default=None, metavar=("K", "N"))
    args = parser.parse_args()
    tag = args.tag or args.world.stem
    out = HERE / "out" / tag
    out.mkdir(parents=True, exist_ok=True)
    folder = Path("/dev/shm/tmp") / f"z1_run_{tag}" / ("back" if args.run_back else "fwd")
    if args.run_back:
        back_in_time = loaded("back_in_time")
        board, laid, _bad = board_of(args.world, folder)
        began = time.perf_counter()
        start, n = args.run_back
        verdict = back_in_time.verdict(board, n, None if start == 0 else start)
        verdict.update(window=[start, start + n], seconds=round(time.perf_counter() - began, 1), world=args.world.name)
        print(json.dumps(verdict, default=str))
        with (out / f"{tag}.runback.jsonl").open("a") as f:
            f.write(json.dumps(verdict, default=str) + "\n")
        return
    eras = loaded("eras")
    clicks_file = (out / f"{tag}.clicks.jsonl").open("w")
    eras_file = (out / f"{tag}.eras.jsonl").open("w")
    nodes_file = (out / f"{tag}.nodes.jsonl").open("w")
    readings_file = (out / f"{tag}.readings.jsonl").open("w")
    refusals: list[dict] = []

    def keep(line: dict) -> None:
        if line.get("event") in ("click", "density", "credit", "lay", "birth"):
            clicks_file.write(json.dumps(line) + "\n")
        elif line.get("event") == "refused":
            refusals.append(line)

    board, laid, _bad = board_of(args.world, folder, output=keep)
    _engine, seeds = json.loads(args.world.read_text()), json.loads(args.world.read_text()).get("seed", [])
    bodies = [(tuple(e["centre"]), e["row"]) for e in seeds if e["lay"] == "at" and e["row"][0] != e["row"][1]]
    pairs = {tuple(f.pair): i for i, f in enumerate(board.families)}
    shape = board.shape
    far = (0, 0, 0)  # the far Node: the origin, two Links from each body's centre on the bodies' board, the hole on the emergence board
    header = eras.header_of(args.world, board, args.intervals)
    header["z1_seed"] = seeds
    header["z1_lays"] = laid
    eras_file.write(json.dumps(header, default=str) + "\n")
    directions = [1] * int(np.prod(shape))
    began = time.perf_counter()
    gamma = board.world.node_clock
    held = board.held[0]
    births_total = 0
    refusals_before = 0
    lines_eras: list[dict] = []
    for step in range(args.intervals + 1):
        if step > 0:
            kept = eras.kept_lines(board)
            time_line = board.states[held].lines[0]
            before = (eras.whole(time_line.now), eras.whole(time_line.before))
            try:
                board.step()
            except (ValueError, RuntimeError) as refusal:
                line = {"interval": board.interval, "refused": str(refusal), "seconds": round(time.perf_counter() - began, 1)}
                eras_file.write(json.dumps(line) + "\n")
                readings_file.write(json.dumps({"event": "refused_run", **line}) + "\n")
                print(json.dumps(line))
                break
            line = eras.interval_line(board, kept, time.perf_counter() - began)
            eras.volume_residuals(lines_eras[-1] if lines_eras else None, line)
            lines_eras.append(line)
            eras_file.write(json.dumps(line, default=str) + "\n")
            nodes_file.write(json.dumps(eras.node_lines(board, before, directions), default=str) + "\n")
            clicks_file.flush()
        total, by_div, by_node = light_quanta(board)
        c = volume.level_of(gamma, np.asarray(board.states[held].lines[0].now, dtype=object))
        births_now = sum(1 for _ in board.born_at.get(board.interval, [])) if False else None
        birth_lines = sum(len(v) for t, v in board.credit.births.items()) if False else None
        reading = {
            "interval": board.interval,
            "seconds": round(time.perf_counter() - began, 1),
            "light": {"share": total, "quanta_div": by_div, "quanta_per_node_sum": by_node, "max_level": int(np.abs(np.asarray(board.states[board.world.seed].lines[0].now, dtype=object)).max())},
            "content": {"origin": int(c[0, 0, 0]), "least": int(c.min()), "largest": int(c.max()), "X_origin": int(board.states[held].lines[0].now[0, 0, 0])},
            "turned": int(board.turned.sum()),
            "swaps_total": sum(n for _t, d, n in board.swaps if d == 1),
            "refusals_this_interval": {cause: sum(1 for r in refusals[refusals_before:] if r["cause"] == cause) for cause in sorted({r["cause"] for r in refusals[refusals_before:]})},
            "records": records_reading(board),
            "proper": {"origin": int(board.proper_count[0, 0, 0]), "far": int(board.proper_count[far]), "least": int(np.asarray(board.proper_count, dtype=object).min()), "largest": int(np.asarray(board.proper_count, dtype=object).max())},
        }
        refusals_before = len(refusals)
        if bodies:
            reading["bodies"] = []
            for centre, row in bodies:
                k = pairs[tuple(row)]
                for r in registry.quanta_records(board.families, board.states, k):
                    reading["bodies"].append({"centre": list(centre), **body_reading(board, k, r, centre, far)})
            if len(bodies) == 2:
                a, b = bodies[0][0], bodies[1][0]
                gap = (b[2] - a[2]) % shape[2]
                gap = gap - shape[2] if gap > shape[2] // 2 else gap
                rows = reading["bodies"]
                # the separation along z of the two bodies' centroids (record 0 at each centre), in milli Links
                ca = [row for row in rows if row["centre"] == list(a) and "centroid_milli" in row]
                cb = [row for row in rows if row["centre"] == list(b) and "centroid_milli" in row]
                if ca and cb:
                    reading["separation_milli"] = 1000 * gap + cb[0]["centroid_milli"][2] - ca[0]["centroid_milli"][2]
                    reading["peak_distance"] = int(manhattan(shape, tuple(ca[0]["peak"]))[tuple(cb[0]["peak"])])
        readings_file.write(json.dumps(reading, default=str) + "\n")
        readings_file.flush()
        if board.interval % args.every == 0:
            print(json.dumps({k: reading[k] for k in ("interval", "seconds", "light", "content", "turned", "swaps_total")}, default=str), flush=True)
    summary = {"event": "summary", "world": args.world.name, "intervals": board.interval, "seconds": round(time.perf_counter() - began, 1), "refusals_by_cause": {cause: sum(1 for r in refusals if r["cause"] == cause) for cause in sorted({r["cause"] for r in refusals})}, "swaps_total": sum(n for _t, d, n in board.swaps if d == 1), "integers_per_node": None}
    node_integers = loaded("node_integers")
    bits, label = node_integers.largest_bits(board)
    summary["integers_per_node"] = {"count": node_integers.total_of(board), "same_at_every_node": node_integers.same_shape(board), "largest_bits": bits, "largest_at": label}
    readings_file.write(json.dumps(summary, default=str) + "\n")
    print(json.dumps(summary, default=str))
    for f in (clicks_file, eras_file, nodes_file, readings_file):
        f.close()
    with (out / f"{tag}.refused.jsonl").open("w") as f:
        for r in refusals:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main()
