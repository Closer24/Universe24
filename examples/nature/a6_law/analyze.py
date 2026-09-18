"""Read the records of A6 repeated under the law of the bit (docs/EXPERIMENTS.md)
and compute the tests' numbers per world, a Renderer of records in the sense of
Highlights 3.29: it reads only what the runner wrote (``run.json``,
``events.jsonl``, ``initialization.json``) and never the engine.

Per light thing (one per lamp, its own thing id) the path is read from the
``spatial_received`` events that carry a whole quantum of ``light`` (the Node
and tick of every arrival; a tick without an arrival is an interval the thing
waited, since every ray moves one Link per interval, point 21, the wait the only
exception), the clicks from ``detector_click`` (the arrival tick at the mark),
the pushes from the per-tick ``momentum`` line of ``run.json`` (the thing's
momentum: amount x heading plus the pushes it carries; a change of it is a
push read, or a step), and the rate of a clock as the intervals it moved over
the intervals elapsed (K 1, content 1: one phase step per moving interval).

The tests: (1) the clock, per cavity the rate while the thing stayed between
its mirrors (its centre and the two mirror Nodes), the tick it left, the
quanta it read (momentum changes), the deficit 1 - rate against r fitted to
A / r and B / r^2 (least squares through the origin, both with their residual
sum of squares); the derivation's coefficients beside them (section 40: GR is
1 - GM/r at the GR w; section 35: the count gives 1 - (sqrt(3) w / 2) GM / r^2
in the free field); (2) the redshift between two radii, z = rate(r_far) /
rate(r_near) - 1, against GM (1/r_near - 1/r_far) (GR) and the count's
(sqrt(3) w / 2) GM (1/r_near^2 - 1/r_far^2); (3) the bending: per line the
pushes read (with their headings), the tick of the first transverse push (the
turn, a whole step for a thing of content 1), the heading it left on and its
offset from the launch line, the click at the mark, the capture; per b the
fraction of lines turned and the mean transverse quanta toward the star,
against GR's 4GM/b, Newton's 2GM/b and the derivation's GM/b in radians (a
turn of content 1 is a right angle, 1.571 rad); (4) the Shapiro delay of the
lines that arrived, click tick - 40, against GR's 2GM ln(4 x_A x_B / b^2) and
the derivation's GM ln(...) (amplitude at the GR w) or 2.72 w GM / b (count);
(5) the separating run: the receiver's momentum first-move tick and the ticks
of its first waits.

Run:  python examples/nature/a6_law/analyze.py RUN [RUN ...] [--out summary.json] [--record record.json]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

SIDE = 33  # set per world from its shape by `analyze`
STAR = (SIDE // 2, SIDE // 2, SIDE // 2)
STRAIGHT_TICK = SIDE - 1


def set_board(shape):
    """The board's side, its centre (the star) and the straight arrival tick."""
    global SIDE, STAR, STRAIGHT_TICK
    SIDE = shape[0]
    STAR = (shape[0] // 2, shape[1] // 2, shape[2] // 2)
    STRAIGHT_TICK = SIDE - 1


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
    arrivals = {}  # tick -> list of (position, amount) where a whole light quantum arrived
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
            elif kind == "spatial_escaped" and event.get("escaped", {}).get("light", [0])[0]:
                escapes.append(event)
    return arrivals, clicks, captures, escapes


def neighbours(here, there, shape):
    """One Link apart on the board, the wrap-around counted."""
    distance = 0
    for i in range(3):
        d = abs(here[i] - there[i])
        distance += min(d, shape[i] - d)
    return distance == 1


def track(things, arrivals, ticks, shape):
    """Assign every light arrival to a thing by continuity: at tick t a thing that
    moved is at a Node one Link from its last Node; a thing with no arrival
    waited. Things start at their seed Node at tick 0 and leave at tick 0 (the
    lamp's emission), arriving one Link on at tick 1."""
    at = {thing: seed for thing, (_, seed, _) in things.items()}
    paths = {thing: [(0, seed)] for thing, (_, seed, _) in things.items()}
    moved = {thing: [] for thing in things}
    for tick in range(1, ticks + 1):
        events = list(arrivals.get(tick, []))
        used = set()
        for thing in sorted(things):
            here = at[thing]
            best = None
            for index, (position, _amount) in enumerate(events):
                if index in used:
                    continue
                if neighbours(position, here, shape):
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


def pushes_of(momentum_line, thing, paths=None, bodies=(), absorbed_tick=None):
    """The changes of a thing's momentum vector per tick (the momentum line is
    amount x heading plus the pushes carried), each classified: a change of
    one quantum on one axis is a push; a reversal at a mirror body's Node
    (-2 x the heading, the thing there) is the reflection and no push; every
    other change (a turn, a reversal away from a mirror) is a push that stepped
    the thing in the same tick, its direction the new heading. Returns the
    series and the pushes as (tick, push vector)."""
    key = str(thing)
    series = [tuple(row.get(key, (0, 0, 0))) for row in momentum_line]
    where = {tick: node for tick, node in (paths or [])}
    pushes = []
    for tick in range(1, len(series)):
        delta = tuple(series[tick][i] - series[tick - 1][i] for i in range(3))
        if not any(delta):
            continue
        size = sum(abs(d) for d in delta)
        node = where.get(tick)
        previous = series[tick - 1]
        if absorbed_tick is not None and tick >= absorbed_tick - 1 and not any(series[tick]):
            # The thing absorbed at a mark leaves the momentum line: no push.
            continue
        if size == 1 or node is None:
            # One quantum, or several read in a tick the thing did not move.
            pushes.append((tick, delta))
            continue
        reversal = all(delta[i] == -2 * previous[i] for i in range(3))
        if reversal and tuple(node) in bodies:
            continue
        after = series[tick]
        direction = tuple(
            (1 if after[i] > 0 else -1 if after[i] < 0 else 0)
            if abs(after[i]) == max(abs(a) for a in after)
            else 0
            for i in range(3)
        )
        pushes.append((tick, direction))
    return series, pushes


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


def wait_value(wait):
    return wait[0] / wait[1] if isinstance(wait, list) else float(wait)


def mass_of(metadata, world):
    """S = 6X of the prefill and GM = S / (2 pi); X from the star's release."""
    for entry in world.get("spatial_fields", []):
        if entry["field"] == "star" and "release" in entry:
            numerator, denominator = entry["release"]
            amounts = [b["amount"] for b in world["external_bodies"] if b["family"] == "star"]
            if not amounts:
                return None  # a control without the star
            x = amounts[0] * numerator // denominator
            flux = 6 * x
            return {"X": x, "S": flux, "GM": flux / (2 * math.pi)}
    return None


def analyze_clock(directory, metadata, world):
    shape = tuple(world["shape"])
    things = things_of(world)
    arrivals, clicks, captures, escapes = read_events(directory)
    ticks = metadata["completed_ticks"]
    paths, moved = track(things, arrivals, ticks, shape)
    star_on = any(body["family"] == "star" for body in world["external_bodies"])
    rows = []
    for thing, (_name, seed, heading) in sorted(things.items()):
        # The cavity's axis is the launch heading; its r the offset along it
        # (the nominal r of the batch), its Euclidean r with the one-Link
        # offset aside of the axis.
        axis = heading
        r = sum((seed[i] - STAR[i]) * axis[i] for i in range(3))
        r_euclid = math.sqrt(sum((seed[i] - STAR[i]) ** 2 for i in range(3)))
        mirrors = {
            tuple(seed[i] + heading[i] for i in range(3)),
            tuple(seed[i] - heading[i] for i in range(3)),
        }
        cavity = {seed, *mirrors}
        series, changes = pushes_of(metadata["momentum"], thing, paths[thing], mirrors)
        left_tick = None
        for tick, node in paths[thing]:
            if node not in cavity:
                left_tick = tick
                break
        stayed = ticks if left_tick is None else left_tick - 1
        moved_in = sum(moved[thing][:stayed])
        reads = [(t, d) for t, d in changes if left_tick is None or t <= left_tick]
        rows.append(
            {
                "thing": thing,
                "r": r,
                "r_euclid": r_euclid,
                "axis": list(axis),
                "ticks": ticks,
                "stayed_ticks": stayed,
                "left_tick": left_tick,
                "moved_in_cavity": moved_in,
                "rate": moved_in / stayed if stayed else None,
                "waits_in_cavity": stayed - moved_in,
                "push_ticks_in_cavity": len(reads),
                "quanta_read_in_cavity": sum(sum(abs(c) for c in d) for _, d in reads),
                "reads": [[t, list(d)] for t, d in reads],
                "pushes_total": len(changes),
                "first_push_tick": changes[0][0] if changes else None,
                "momentum_series_head": [list(m) for m in series[:12]],
                "last_node": list(paths[thing][-1][1]),
            }
        )
    deficit = [(row["r_euclid"], 1.0 - row["rate"]) for row in rows if row["rate"] is not None]
    fits = {"1/r": fit_origin(deficit, 1), "1/r^2": fit_origin(deficit, 2)}
    return {
        "kind": "clock",
        "star_on": star_on,
        "clocks": rows,
        "deficit": deficit,
        "fits": fits,
        "captures": len(captures),
        "escapes": len(escapes),
    }


def analyze_bend(directory, metadata, world):
    shape = tuple(world["shape"])
    things = things_of(world)
    arrivals, clicks, captures, escapes = read_events(directory)
    ticks = metadata["completed_ticks"]
    paths, moved = track(things, arrivals, ticks, shape)
    click_at = {tuple(click["position"]): click["tick"] for click in clicks}
    star_on = any(body["family"] == "star" for body in world["external_bodies"])
    rows = []
    for thing, (_name, seed, _heading) in sorted(things.items()):
        line = seed
        b = math.hypot(line[1] - STAR[1], line[2] - STAR[2])
        b_nominal = abs(line[1] - STAR[1])
        side = 1 if line[1] > STAR[1] else -1
        dz = line[2] - STAR[2]
        mark = (SIDE - 1, line[1], line[2])
        click = click_at.get(mark)
        series, changes = pushes_of(metadata["momentum"], thing, paths[thing], absorbed_tick=click)
        toward = away = along_back = along_forward = 0
        turn_tick = None
        for tick, delta in changes:
            # A push toward the star: -side on y, -sign(dz) on z; along: x.
            t = -side * delta[1] - (1 if dz > 0 else -1 if dz < 0 else 0) * delta[2]
            if dz == 0:
                t = -side * delta[1]
            if abs(delta[1]) + abs(delta[2]) and turn_tick is None:
                turn_tick = tick
            toward += max(t, 0)
            away += max(-t, 0)
            along_back += max(-delta[0], 0)
            along_forward += max(delta[0], 0)
        last_tick, last_node = paths[thing][-1]
        # Where the thing stopped: its last Node, the distance from the star and
        # the tick of its last move; a thing that never moved again from a
        # Node inside the field is frozen there (it owes more than it pays).
        stop_r = math.sqrt(sum((last_node[i] - STAR[i]) ** 2 for i in range(3)))
        waits_after_stop = ticks - last_tick
        previous = paths[thing][-2][1] if len(paths[thing]) > 1 else None
        exit_heading = None
        if previous is not None:
            exit_heading = [
                ((last_node[i] - previous[i] + shape[i] // 2) % shape[i]) - shape[i] // 2
                for i in range(3)
            ]
        rows.append(
            {
                "thing": thing,
                "line": list(line),
                "b": b,
                "b_nominal": b_nominal,
                "side": side,
                "click_tick": click,
                "delay": None if click is None else click - STRAIGHT_TICK,
                "quanta_read": len(changes),
                "turn_tick": turn_tick,
                "pushes": [[t, list(d)] for t, d in changes],
                "transverse_toward": toward,
                "transverse_away": away,
                "along_back": along_back,
                "along_forward": along_forward,
                # The waits before the click: the click tick is the arrival at
                # the mark (no arrival event is written for it).
                "waits": (ticks - sum(moved[thing]))
                if click is None
                else (click - (sum(moved[thing][: click - 1]) + 1)),
                "last_tick": last_tick,
                "last_node": list(last_node),
                "stop_r": stop_r,
                "waits_after_stop": waits_after_stop,
                "exit_heading": exit_heading,
                "exit_offset": [last_node[1] - line[1], last_node[2] - line[2]],
                "captured": last_node == STAR or any(abs(last_node[i] - STAR[i]) for i in range(3)) == 0,
            }
        )
    per_b = {}
    for b_nominal in sorted({row["b_nominal"] for row in rows}):
        lines = [row for row in rows if row["b_nominal"] == b_nominal]
        arrived = [row for row in lines if row["click_tick"] is not None]
        turned = [row for row in lines if row["turn_tick"] is not None]
        net = [row["transverse_toward"] - row["transverse_away"] for row in lines]
        frozen = [row for row in lines if row["click_tick"] is None and row["waits_after_stop"] >= 10]
        per_b[str(b_nominal)] = {
            "lines": len(lines),
            "arrived": len(arrived),
            "turned": len(turned),
            "frozen": len(frozen),
            "stop_x": [row["last_node"][0] for row in frozen],
            "stop_r": [round(row["stop_r"], 2) for row in frozen],
            "stop_ticks": [row["last_tick"] for row in frozen],
            "fraction_turned": len(turned) / len(lines),
            "mean_net_transverse_toward": sum(net) / len(net),
            "mean_quanta_read": sum(row["quanta_read"] for row in lines) / len(lines),
            "delays_of_arrived": [row["delay"] for row in arrived],
            "mean_delay_of_arrived": (sum(row["delay"] for row in arrived) / len(arrived))
            if arrived
            else None,
            "turn_ticks": [row["turn_tick"] for row in turned],
        }
    return {
        "kind": "bend",
        "star_on": star_on,
        "b_nominal": sorted({row["b_nominal"] for row in rows}),
        "passes": rows,
        "per_b": per_b,
        "arrived": sum(1 for row in rows if row["click_tick"] is not None),
        "captures": len(captures),
        "escapes": len(escapes),
    }


def analyze_sep(directory, metadata, world):
    shape = tuple(world["shape"])
    things = things_of(world)
    arrivals, clicks, captures, escapes = read_events(directory)
    ticks = metadata["completed_ticks"]
    paths, moved = track(things, arrivals, ticks, shape)
    thing = 1
    _, seed, heading = things[thing]
    mirrors = {
        tuple(seed[i] + heading[i] for i in range(3)),
        tuple(seed[i] - heading[i] for i in range(3)),
    }
    series, changes = pushes_of(metadata["momentum"], thing, paths[thing], mirrors)
    waits = [tick + 1 for tick, m in enumerate(moved[thing]) if not m]
    return {
        "kind": "sep",
        "mass_on": any(body["family"] == "star" for body in world["external_bodies"]),
        "receiver_first_move_tick": changes[0][0] if changes else None,
        "receiver_changes": [[t, list(d)] for t, d in changes[:20]],
        "receiver_first_waits": waits[:20],
        "receiver_moved": sum(moved[thing]),
        "receiver_last_node": list(paths[thing][-1][1]),
    }


def analyze(run):
    directory, metadata, world = load(run)
    set_board(world["shape"])
    model = metadata["model"]
    if "clock" in model:
        result = analyze_clock(directory, metadata, world)
    elif "bend" in model:
        result = analyze_bend(directory, metadata, world)
    else:
        result = analyze_sep(directory, metadata, world)
    audit = metadata["audit"]
    result.update(
        {
            "run": str(directory),
            "model": model,
            "status": metadata["status"],
            "error": metadata.get("error"),
            "ticks": metadata["completed_ticks"],
            "elapsed_seconds": metadata["elapsed_seconds"],
            "source_sha256": metadata["source_sha256"],
            "initialization_sha256": metadata["initialization_sha256"],
            "all_balanced": all(entry["balanced"] for entry in audit),
            "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
            "boundary": metadata.get("boundary"),
            "side": SIDE,
            "K": metadata["K"],
            "N": metadata.get("N"),
            "wait_per_quantum": metadata["wait_per_quantum"],
            "w": wait_value(metadata["wait_per_quantum"]),
            "wait_reads": metadata.get("wait_reads_option", "amount"),
            "shadow_wait": metadata.get("shadow_wait_option"),
            "initial_field": metadata.get("initial_field"),
            "mass": mass_of(metadata, world),
            "standing": {k: metadata[k] for k in metadata if k.startswith("standing_field")},
            "shadow_content_first_last": [metadata["shadow_content"][0], metadata["shadow_content"][-1]]
            if metadata.get("shadow_content")
            else None,
        }
    )
    return result


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("runs", nargs="+")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    results = [analyze(run) for run in args.runs]
    for result in results:
        head = (
            f"{result['model']}: {result['status']} ticks {result['ticks']} balanced {result['all_balanced']} "
            f"w {result['w']:.3f} reads {result['wait_reads']} standing {result['standing']}"
        )
        if result["kind"] == "clock":
            rates = " ".join(
                f"r={c['r']}:{c['rate']:.3f}(w{c['waits_in_cavity']},q{c['quanta_read_in_cavity']},p{c['push_ticks_in_cavity']},left {c['left_tick']})"
                for c in result["clocks"]
            )
            fits = result["fits"]
            print(
                f"{head} | {rates} | A/r {fits['1/r']['coefficient']} rss {fits['1/r']['rss']} | B/r^2 {fits['1/r^2']['coefficient']} rss {fits['1/r^2']['rss']}"
            )
        elif result["kind"] == "bend":
            print(head)
            for b, entry in result["per_b"].items():
                print(
                    f"  b={b}: arrived {entry['arrived']}/{entry['lines']} turned {entry['turned']} frozen {entry['frozen']} at x {entry['stop_x']} r {entry['stop_r']} since ticks {entry['stop_ticks']} "
                    f"net toward {entry['mean_net_transverse_toward']:.2f} quanta {entry['mean_quanta_read']:.2f} "
                    f"delays {entry['delays_of_arrived']} turn ticks {entry['turn_ticks']}"
                )
        else:
            print(
                f"{head} | first move {result['receiver_first_move_tick']} waits {result['receiver_first_waits']}"
            )
    if args.out:
        args.out.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    if args.record:
        record = []
        for result in results:
            small = {k: v for k, v in result.items() if k not in ("passes", "clocks")}
            if result["kind"] == "clock":
                small["clocks"] = [
                    {
                        k: c[k]
                        for k in (
                            "r",
                            "r_euclid",
                            "axis",
                            "rate",
                            "stayed_ticks",
                            "left_tick",
                            "waits_in_cavity",
                            "quanta_read_in_cavity",
                            "push_ticks_in_cavity",
                        )
                    }
                    for c in result["clocks"]
                ]
            elif result["kind"] == "bend":
                small["passes"] = [
                    {
                        k: p[k]
                        for k in (
                            "line",
                            "b",
                            "click_tick",
                            "delay",
                            "quanta_read",
                            "turn_tick",
                            "transverse_toward",
                            "transverse_away",
                            "along_back",
                            "along_forward",
                            "exit_heading",
                            "exit_offset",
                            "last_node",
                            "last_tick",
                            "stop_r",
                            "waits_after_stop",
                            "waits",
                        )
                    }
                    for p in result["passes"]
                ]
            record.append(small)
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
