"""Read the records of A6 repeated under the law of the bit (docs/EXPERIMENTS.md)
and compute the four tests' numbers per world, a Renderer of records in the
sense of Highlights 3.29: it reads only what the runner wrote (``run.json``,
``events.jsonl``, ``initialization.json``) and never the engine.

Per light thing (one per lamp, its own thing id) the path is read from the
``spatial_received`` events that carry a whole quantum of ``light`` (the Node
and tick of every arrival; a tick without an arrival is an interval the thing
waited, since every ray moves one Link per interval, point 21, the wait the only
exception), the clicks from ``detector_click`` (the arrival tick at the mark),
the captures from ``external_body_absorbed``, the pushes from the per-tick
``momentum`` line of ``run.json`` (the thing's momentum: amount x heading plus
the pushes it carries), and the rate of a clock as the intervals it moved over
the intervals elapsed (K 1, content 1: one phase step per moving interval).

The tests: (1) the clock, the rate deficit 1 - rate per cavity against its
radius r, fitted to A / r and B / r^2 (least squares through the origin, both
reported with their residuals), and the whole-quanta waits counted; (2) the
redshift between two radii, z = rate(r_far) / rate(r_near) - 1; (3) the
bending: per pass the net transverse push toward the star (quanta), the exit
Node against the launch line and the exit heading, the mean over the six lines
of one b as the image's alpha = <transverse quanta read> / p with p = 1 (the
small-angle register reading of DERIVATIONS.md section 35: alpha_image = GM/b
in every option), against GR's 4GM/b, Newton's 2GM/b and the law's GM/b with
GM read from the clocks (GM = (2/sqrt(3)) r^2 n(r), section 34) and from the
pushes themselves; (4) the Shapiro delay, the click tick less the control's
(24), against 2GM ln(4 x_A x_B / b^2) and round 5's 2.72 w GM / b.

Run:  python examples/nature/a6_law/analyze.py RUN [RUN ...] [--out summary.json] [--record record.json]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

STAR = (12, 12, 12)
STRAIGHT_TICK = 24


def load(run):
    directory = Path(run)
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    return directory, metadata, world


def things_of(world):
    """thing id -> (type name, seed position, emission heading)."""
    kinds = [kind["name"] for kind in world["disturbance_types"]]
    seeds = {seed["type"]: tuple(seed["position"]) for seed in world["seeds"]}
    headings = {e["type"]: tuple(e["heading"]) for e in world["emissions"]}
    return {index + 1: (name, seeds[name], headings[name]) for index, name in enumerate(kinds)}


def read_events(directory):
    arrivals = {}  # tick -> list of positions where a whole light quantum arrived
    clicks = []
    captures = []
    escapes = []
    with (directory / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            event = json.loads(text)
            kind = event["event"]
            if kind == "spatial_received":
                amount = sum(fields.get("light", [0])[0] for fields in event["received_fields"])
                if amount:
                    arrivals.setdefault(event["tick"], []).append((tuple(event["position"]), amount))
            elif kind == "detector_click" and event.get("family") == "light":
                clicks.append(event)
            elif kind == "external_body_absorbed" and event.get("family") == "light":
                captures.append(event)
            elif kind == "spatial_escaped" and event["escaped"].get("light", [0])[0]:
                escapes.append(event)
    return arrivals, clicks, captures, escapes


def track(things, arrivals, ticks):
    """Assign every light arrival to a thing by continuity: at tick t a thing that
    moved is at a Node one Link from its last Node; a thing with no arrival
    waited. Things start at their seed Node at tick 0 and leave at tick 0 (the
    lamp's emission), arriving one Link on at tick 1."""
    at = {thing: seed for thing, (_, seed, _) in things.items()}
    alive = set(things)
    paths = {thing: [(0, seed)] for thing, (_, seed, _) in things.items()}
    moved = {thing: [] for thing in things}
    for tick in range(1, ticks + 1):
        events = list(arrivals.get(tick, []))
        used = set()
        for thing in sorted(alive):
            here = at[thing]
            best = None
            for index, (position, amount) in enumerate(events):
                if index in used:
                    continue
                if sum(abs(position[i] - here[i]) for i in range(3)) == 1:
                    best = index
                    break
            if best is None:
                moved[thing].append(0)
                continue
            used.add(best)
            at[thing] = events[best][0]
            paths[thing].append((tick, events[best][0]))
            moved[thing].append(1)
    return paths, moved


def pushes_of(momentum_line, thing):
    """The changes of a thing's momentum vector per tick (pushes and steps)."""
    key = str(thing)
    series = [tuple(row.get(key, (0, 0, 0))) for row in momentum_line]
    changes = []
    for tick in range(1, len(series)):
        delta = tuple(series[tick][i] - series[tick - 1][i] for i in range(3))
        if any(delta):
            changes.append((tick, delta))
    return series, changes


def fit_origin(points, power):
    """Least squares y = A / r^power through the origin; the coefficient, the
    residual sum of squares and the number of points."""
    xs = [(1.0 / r**power, y) for r, y in points]
    sxx = sum(x * x for x, _ in xs)
    if sxx == 0:
        return {"coefficient": None, "rss": None, "points": len(points)}
    a = sum(x * y for x, y in xs) / sxx
    rss = sum((y - a * x) ** 2 for x, y in xs)
    return {"coefficient": a, "rss": rss, "points": len(points)}


def analyze_clock(directory, metadata, world):
    things = things_of(world)
    arrivals, clicks, captures, escapes = read_events(directory)
    ticks = metadata["completed_ticks"]
    paths, moved = track(things, arrivals, ticks)
    star_on = any(body["family"] == "star" for body in world["external_bodies"])
    rows = []
    for thing, (name, seed, heading) in sorted(things.items()):
        r = sum(abs(seed[i] - STAR[i]) for i in range(3))
        axis = tuple((seed[i] - STAR[i]) // max(1, r) for i in range(3))
        series, changes = pushes_of(metadata["momentum"], thing)
        halves = [moved[thing][: ticks // 2], moved[thing][ticks // 2 :]]
        left = paths[thing][-1][1] if paths[thing] else seed
        inside = sum(abs(left[i] - seed[i]) for i in range(3)) <= 1
        rows.append(
            {
                "thing": thing,
                "r": r,
                "axis": list(axis),
                "moved": sum(moved[thing]),
                "ticks": ticks,
                "rate": sum(moved[thing]) / ticks,
                "rate_first_half": sum(halves[0]) / max(1, len(halves[0])),
                "rate_second_half": sum(halves[1]) / max(1, len(halves[1])),
                "waits": ticks - sum(moved[thing]),
                "momentum_changes": len(changes),
                "first_change_tick": changes[0][0] if changes else None,
                "in_cavity_at_end": inside,
                "last_node": list(left),
            }
        )
    deficit = [(row["r"], 1.0 - row["rate"]) for row in rows]
    fits = {"1/r": fit_origin(deficit, 1), "1/r^2": fit_origin(deficit, 2)}
    nonzero = [(r, d) for r, d in deficit if d > 0]
    fits_nonzero = {"1/r": fit_origin(nonzero, 1), "1/r^2": fit_origin(nonzero, 2)}
    return {
        "kind": "clock",
        "star_on": star_on,
        "clocks": rows,
        "deficit": deficit,
        "fits": fits,
        "fits_nonzero_only": fits_nonzero,
        "captures": len(captures),
        "escapes": len(escapes),
    }


def analyze_bend(directory, metadata, world):
    things = things_of(world)
    arrivals, clicks, captures, escapes = read_events(directory)
    ticks = metadata["completed_ticks"]
    paths, moved = track(things, arrivals, ticks)
    marks = {tuple(mark["position"]): mark for mark in world.get("detectors", [])}
    click_at = {tuple(click["position"]): click["tick"] for click in clicks}
    star_on = any(body["family"] == "star" for body in world["external_bodies"])
    rows = []
    for thing, (name, seed, heading) in sorted(things.items()):
        line = seed
        b_vec = (line[1] - STAR[1], line[2] - STAR[2])
        b = math.hypot(*b_vec)
        side = 1 if line[1] > STAR[1] else -1
        series, changes = pushes_of(metadata["momentum"], thing)
        # The transverse push toward the star: the sum over the pushes of the
        # y component times -side (toward the star is -side on y) and the z
        # component toward z = 12.
        toward = 0
        away = 0
        along = 0
        for _, delta in changes:
            dy, dz = delta[1], delta[2]
            t = -side * dy + (-(1 if line[2] > STAR[2] else -1 if line[2] < STAR[2] else 0)) * dz
            if line[2] == STAR[2]:
                t = -side * dy
            toward += max(t, 0)
            away += max(-t, 0)
            along += abs(delta[0])
        mark = (24, line[1], line[2])
        click = click_at.get(mark)
        last = paths[thing][-1]
        exit_offset = [last[1][1] - line[1], last[1][2] - line[2]]
        final_momentum = list(series[-1]) if series else None
        captured = any(c.get("owner") == thing for c in captures) if captures and "owner" in captures[0] else None
        rows.append(
            {
                "thing": thing,
                "line": list(line),
                "b": b,
                "side": side,
                "click_tick": click,
                "delay": None if click is None else click - STRAIGHT_TICK,
                "moved": sum(moved[thing]),
                "waits_before_click": None
                if click is None
                else click - STRAIGHT_TICK,
                "momentum_changes": [[t, list(d)] for t, d in changes],
                "transverse_toward": toward,
                "transverse_away": away,
                "along_changes": along,
                "last_tick": last[0],
                "last_node": list(last[1]),
                "exit_offset": exit_offset,
                "final_momentum": final_momentum,
                "captured": captured,
            }
        )
    passes = [row for row in rows]
    arrived = [row for row in passes if row["click_tick"] is not None]
    net = [row["transverse_toward"] - row["transverse_away"] for row in passes]
    delays = [row["delay"] for row in arrived]
    b_nominal = sorted({round(math.hypot(seed[1] - STAR[1], 0)) for _, (_, seed, _) in things.items()})
    return {
        "kind": "bend",
        "star_on": star_on,
        "b_nominal": b_nominal,
        "passes": rows,
        "arrived": len(arrived),
        "not_arrived": len(passes) - len(arrived),
        "captures": len(captures),
        "escapes_elsewhere": len(escapes),
        "mean_transverse_net": sum(net) / len(net) if net else None,
        "mean_delay_of_arrived": sum(delays) / len(delays) if delays else None,
        "delays": delays,
        "net_transverse_per_pass": net,
    }


def analyze(run):
    directory, metadata, world = load(run)
    kind = "clock" if "clock" in metadata["model"] else "bend"
    result = analyze_clock(directory, metadata, world) if kind == "clock" else analyze_bend(directory, metadata, world)
    audit = metadata["audit"]
    result.update(
        {
            "run": str(directory),
            "model": metadata["model"],
            "status": metadata["status"],
            "error": metadata.get("error"),
            "ticks": metadata["completed_ticks"],
            "elapsed_seconds": metadata["elapsed_seconds"],
            "source_sha256": metadata["source_sha256"],
            "initialization_sha256": metadata["initialization_sha256"],
            "all_balanced": all(entry["balanced"] for entry in audit),
            "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
            "K": metadata["K"],
            "N": metadata.get("N"),
            "wait_per_quantum": metadata["wait_per_quantum"],
            "wait_reads": metadata.get("wait_reads_option"),
            "shadow_wait": metadata.get("shadow_wait_option"),
            "initial_field": metadata.get("initial_field"),
            "shadow_content_first_last": [metadata["shadow_content"][0], metadata["shadow_content"][-1]]
            if metadata.get("shadow_content")
            else None,
            "computation_per_tick_sum": sum(metadata["computation_per_tick"]),
        }
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    results = [analyze(run) for run in args.runs]
    for result in results:
        if result["kind"] == "clock":
            rates = " ".join(f"r={c['r']}:{c['rate']:.3f}({c['waits']})" for c in result["clocks"])
            fits = result["fits"]
            print(
                f"{result['model']}: {result['status']} ticks {result['ticks']} balanced {result['all_balanced']} "
                f"| {rates} | A/r {fits['1/r']['coefficient']} rss {fits['1/r']['rss']} | B/r^2 {fits['1/r^2']['coefficient']} rss {fits['1/r^2']['rss']}"
            )
        else:
            print(
                f"{result['model']}: {result['status']} ticks {result['ticks']} balanced {result['all_balanced']} "
                f"| b {result['b_nominal']} arrived {result['arrived']}/{result['arrived'] + result['not_arrived']} "
                f"captures {result['captures']} | net transverse per pass {result['net_transverse_per_pass']} "
                f"| delays {result['delays']}"
            )
    if args.out:
        args.out.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    if args.record:
        record = []
        for result in results:
            small = {k: v for k, v in result.items() if k not in ("passes", "clocks")}
            if result["kind"] == "clock":
                small["clocks"] = [
                    {k: c[k] for k in ("r", "axis", "rate", "waits", "rate_first_half", "rate_second_half", "in_cavity_at_end")}
                    for c in result["clocks"]
                ]
            else:
                small["passes"] = [
                    {k: p[k] for k in ("line", "b", "click_tick", "delay", "transverse_toward", "transverse_away", "exit_offset", "last_node", "last_tick")}
                    for p in result["passes"]
                ]
            record.append(small)
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
