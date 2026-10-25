"""W2's toy (2026-10-25): two bodies of one gapped family on a bare torus, laid by the birth's own lay act,
the births of the light sea refused by name (a toy-side filter on meeting_board.child_of), every other act the
engine's. Per interval the script reads each body record's share (share.family_share on its own lines), its peak
and its centroid about the lay Node, the volume's content level c = level_of(X) at named Nodes, the sign holder's
free row and the seed light's share there, and keeps every credit and refusal line the board writes; at the end
the run back (step_inverse over every interval) is compared with the state after the lay, array by array.

Run (PYTHONPATH=<worktree>/src, TMPDIR=/dev/shm/tmp):
    python tools/derivations/open_items/H-Two-Bodies-Free-Fall-2/two_bodies.py --config pair3 --den 15162856759112389 --cube 7 --intervals 300
Configs: alone (A at (3,3,3)); pair3 (A and B three Links apart on z); pair2 (two Links); fall (A alone with a
well laid by hand, time_line_set, centred three Links away on z, --well-depth levels at its centre, falling as
c0 div (1 + r)); heavy (A of --delta quanta and B of one quantum three Links apart).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # the worktree root: tests.laws_universe

from event_universe import emission, meeting_board, share, world_files  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.take import Item  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import node_arrays, time_line_set  # noqa: E402

GAMMA, ACTION = 1000, 36000
A_NODE = (3, 3, 3)


def configs(cube: int, delta: int) -> dict[str, dict]:
    far = (3, 3, (3 + 3) % cube)
    near = (3, 3, (3 + 2) % cube)
    return {
        "alone": {"bodies": [(A_NODE, 1, 0, 1)]},
        "pair3": {"bodies": [(A_NODE, 1, 0, 1), (far, 1, 1, 1)]},
        "pair2": {"bodies": [(A_NODE, 1, 0, 1), (near, 1, 1, 1)]},
        "pair3opp": {"bodies": [(A_NODE, 1, 0, 1), (far, -1, 1, 1)]},
        "fall": {"bodies": [(A_NODE, 1, 0, 1)], "well": far},
        "heavy": {"bodies": [(A_NODE, 1, 0, delta), (far, 1, 1, 1)]},
        "empty": {"bodies": []},
    }


def torus_offset(at: tuple[int, int, int], origin: tuple[int, int, int], cube: int) -> tuple[int, int, int]:
    found = []
    for a, o in zip(at, origin, strict=True):
        d = (a - o) % cube
        if d > cube // 2:
            d -= cube
        found.append(d)
    return tuple(found)


def distance(a: tuple[int, int, int], b: tuple[int, int, int], cube: int) -> int:
    return sum(abs(d) for d in torus_offset(a, b, cube))


def body_share(board: Lattice, k: int, r: int) -> np.ndarray:
    content, factors = board.read(k, 1, r)
    found = share.family_share(
        board.families[k], board.lines_of(k, r), board.world.node_clock, content, factors, board.unit
    )
    return np.asarray(found, dtype=object)


def centroid(shares: np.ndarray, origin: tuple[int, int, int], cube: int) -> tuple[list[float], float]:
    total = int(shares.sum())
    if total <= 0:
        return [0.0, 0.0, 0.0], 0.0
    moments = [0, 0, 0]
    for at in np.ndindex(*shares.shape):
        s = int(shares[at])
        if s:
            off = torus_offset(at, origin, cube)
            for a in range(3):
                moments[a] += s * off[a]
    found = [m / total for m in moments]
    return found, float(np.sqrt(sum(x * x for x in found)))


def well_levels(shape: tuple[int, ...], centre: tuple[int, int, int], depth: int, cube: int) -> np.ndarray:
    found = np.zeros(shape, dtype=object)
    for at in np.ndindex(*shape):
        r = distance(at, centre, cube)
        found[at] = depth // (1 + r)
    return found


def snapshot(board: Lattice) -> dict:
    return {k: tuple(np.asarray(a, dtype=object).copy() for a in v) for k, v in node_arrays(board).items()}


def differing(a: dict, b: dict) -> int:
    count = 0
    for key in set(a) | set(b):
        if key not in a or key not in b:
            count += 1
            continue
        for x, y in zip(a[key], b[key], strict=False):
            if np.shape(x) != np.shape(y) or not np.array_equal(
                np.asarray(x, dtype=object), np.asarray(y, dtype=object)
            ):
                count += 1
                break
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--den", type=int, default=15162856759112389)
    parser.add_argument("--cube", type=int, default=7)
    parser.add_argument("--intervals", type=int, default=300)
    parser.add_argument("--family", default="point 0 2 0")
    parser.add_argument("--delta", type=int, default=3)
    parser.add_argument("--well-depth", type=int, default=200)
    parser.add_argument("--no-births", action="store_true", default=True)
    parser.add_argument("--run-back", action="store_true", default=False)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    out = Path(args.out) if args.out else here / f"two_bodies_{args.config}_den{args.den.bit_length()}b_c{args.cube}_n{args.intervals}.jsonl"
    folder = Path(f"/dev/shm/tmp/w2_{args.config}_{args.cube}_{args.intervals}")
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    (folder / "u.json").write_text(
        json.dumps({"integers": {"den": args.den, "node_clock": GAMMA, "quantum_action": ACTION}})
    )
    (folder / "w.json").write_text(
        json.dumps({"universe": "u.json", "shape": [args.cube] * 3, "intervals": args.intervals})
    )
    lines: list[dict] = []
    board = Lattice(load_world(folder / "w.json"), output=lines.append)
    meeting_board.child_of = lambda b, i, v, w: ()  # the toy's deviation: the sea's births refused by name
    names = [f.name for f in board.families]
    k = names.index(args.family)
    family = board.families[k]
    num, den = family.pair
    config = configs(args.cube, args.delta)[args.config]
    seed, vol, sign = board.world.seed, board.held[0], board.held[1]
    if "well" in config:
        levels = well_levels(board.shape, config["well"], args.well_depth, args.cube)
        x = volume.volume_of(GAMMA, levels)
        time_line_set(board, x, x.copy())
    bodies = []
    for at, sense, record, delta in config["bodies"]:
        emission.laid_by_count(board, Item(k, delta, (at,), (den, den), sense=sense, record=record))
        bodies.append((k, record, at))
    probes = {"A": A_NODE, "B": (3, 3, (3 + 3) % args.cube), "mid": (3, 3, (3 + 1) % args.cube) if args.config != "pair3" and args.config != "heavy" and args.config != "fall" else (3, 3, (3 + 1) % args.cube), "mid2": (3, 3, (3 + 2) % args.cube), "far": (0, 0, 0 if args.cube < 6 else (3 + args.cube // 2) % args.cube)}
    header = {
        "event": "header", "config": args.config, "den": args.den, "den_bits": args.den.bit_length(),
        "cube": args.cube, "intervals": args.intervals, "family": args.family, "pair": [num, den],
        "g": (den - num) / den, "cos_omega0": num / den, "omega0": float(np.arccos(num / den)),
        "period0": float(2 * np.pi / np.arccos(num / den)), "unit_k": board.credit.units[k],
        "unit_light": board.credit.units[seed], "bodies": [[list(at), s, r, d] for at, s, r, d in config["bodies"]],
        "well": list(config["well"]) if "well" in config else None, "well_depth": args.well_depth if "well" in config else None,
        "width_bits": board.world.width.bit_length(), "amplitude_bound": board.world.amplitude_bound,
        "volume_pair": list(board.families[vol].pair), "probes": {n: list(p) for n, p in probes.items()},
    }
    with out.open("w") as f:
        f.write(json.dumps(header) + "\n")
        start = snapshot(board)
        t0 = time.time()
        for step in range(args.intervals + 1):
            # the readings at the interval's start (interval 0 the lay)
            x = np.asarray(board.states[vol].lines[0].now, dtype=object)
            c = volume.level_of(GAMMA, x)
            free_row = np.asarray(board.states[sign].lines[0].now, dtype=object)
            light = np.asarray(board.share_of(seed)[0], dtype=object)
            row: dict = {"event": "reading", "interval": board.interval, "bodies": []}
            for kk, r, at in bodies:
                s = body_share(board, kk, r)
                peak = tuple(int(i) for i in np.unravel_index(int(np.argmax(np.asarray(s, dtype=float))), s.shape))
                cen, radius = centroid(s, at, args.cube)
                total = int(s.sum())
                moments = [0, 0, 0]  # the integer first moments of the share about the lay Node, SUM s_i x_i per axis
                for where in np.ndindex(*s.shape):
                    si = int(s[where])
                    if si:
                        off = torus_offset(where, at, args.cube)
                        for a in range(3):
                            moments[a] += si * off[a]
                row["bodies"].append({
                    "record": r, "lay": list(at), "peak": list(peak), "peak_offset": list(torus_offset(peak, at, args.cube)),
                    "moment": moments,
                    "share_peak": int(s[peak]), "share_lay": int(s[at]), "share_total": total,
                    "frac_lay": (int(s[at]) / total if total else None), "centroid": cen, "radius": radius,
                    "beat": int(board.beats.get((kk, r), np.zeros(board.shape, dtype=np.int64))[at]),
                    "standing": int(board.standing.get((kk, r), np.zeros(board.shape, dtype=np.int64))[at]),
                    "c_lay": int(c[at]), "proper_lay": int(board.proper_count[at]),
                })
            row["c"] = {n: int(c[p]) for n, p in probes.items()}
            row["c_max"] = int(c.max()); row["c_min"] = int(c.min()); row["c_mean"] = float(np.asarray(c, dtype=float).mean())
            row["free_row"] = {n: int(free_row[p]) for n, p in probes.items()}
            row["light"] = {n: int(light[p]) for n, p in probes.items()}
            row["light_total"] = int(light.sum())
            row["light_quanta_total"] = int(light.sum()) / board.credit.units[seed]
            if len(bodies) == 2:
                pa = row["bodies"][0]["peak"]; pb = row["bodies"][1]["peak"]
                row["peak_distance"] = distance(tuple(pa), tuple(pb), args.cube)
                ca = np.array(row["bodies"][0]["centroid"]) + np.array(bodies[0][2]); cb = np.array(row["bodies"][1]["centroid"]) + np.array(bodies[1][2])
                d = cb - ca
                d = np.where(d > args.cube / 2, d - args.cube, np.where(d < -args.cube / 2, d + args.cube, d))
                row["centroid_distance"] = float(np.sqrt((d * d).sum()))
            row["seconds"] = round(time.time() - t0, 2)
            f.write(json.dumps(row) + "\n")
            if step == args.intervals:
                break
            n_before = len(lines)
            board.step()
            for li in lines[n_before:]:
                if li.get("event") in ("credit", "refused", "birth"):
                    f.write(json.dumps(li) + "\n")
        summary = {"event": "summary", "seconds": round(time.time() - t0, 2), "interval": board.interval,
                   "credits": sum(1 for li in lines if li.get("event") == "credit"),
                   "refused": sum(1 for li in lines if li.get("event") == "refused"),
                   "births": sum(1 for li in lines if li.get("event") == "birth"),
                   "swaps": len(board.swaps), "counts": {names[i]: int(v) for i, v in board.credit.counts.items() if v},
                   "deficits": {names[i]: int(v) for i, v in board.credit.deficits.items()}}
        if args.run_back:
            t1 = time.time()
            for _ in range(args.intervals):
                board.step_inverse()
            end = snapshot(board)
            summary["run_back"] = {"interval": board.interval, "arrays_differing": differing(start, end),
                                   "arrays": len(start), "seconds": round(time.time() - t1, 2),
                                   "verdict": "MATCH" if differing(start, end) == 0 and board.interval == 0 else "MISMATCH"}
        f.write(json.dumps(summary) + "\n")
    print(json.dumps(header)); print(json.dumps(summary)); print("out", out)


if __name__ == "__main__":
    main()
