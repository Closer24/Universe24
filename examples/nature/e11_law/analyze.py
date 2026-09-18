"""Read the runs of E11 repeated under the law of the bit (docs/EXPERIMENTS.md).

Two readings, both Recorders in the sense of Highlights 3.29 (they read the
record a run left, or replay its world through the Simulation API and check
the replay against the record; they never change the engine):

1. From `run.json` of every world of the series (the runner's record): the
   books per bit at every completed tick (`audit`: the world line, the real
   line and the shadow line balanced, `real_conserved`), the shadows' total
   per tick, the escapes, the runner's standing-set report where the world
   declares `standing_field`, and for the probe worlds the test thing's
   momentum line per tick (the runner's `momentum`, thing id to vector; the
   test thing is type 2 and the body is thing 3), whose increments are the
   pushed amount per interval, and the body's momentum line, the recoil that
   came home through the field.

2. In-process (the dense layer holds every shadow and publishes no per-Node
   event, so the shells are read from the engine): a world is replayed for
   its ticks and after every tick the layer's arrays (arrivals per Node,
   owner, flow, sign, Port and phase layer; the parked ninths) and the
   engine's Nodes give, per Node, the body's shadows on their way (outgoing,
   returning), their signed radial flux J_r = sum over shadows of +-amount x
   (heading . r) / |r| (the sign of a returning share negative, what a thing
   reads) and the parked shares; from these, per L1 shell (|dx| + |dy| + |dz|
   = k) and per Euclidean shell (round |r| = k): the Nodes, the content, the
   content per Node, J_r per shell and per Node; the content on the axes, on
   the coordinate planes off the axes, and off the planes (all three
   coordinates nonzero), as fractions of the content on the board; and at the
   nine read Nodes of the probe worlds the content, J and the amplitude: the
   size of the coherent sum of the shadows that arrived at the Node in the
   interval, formed by the engine's own `arrival_amplitude` (wait-reads-v1:
   per travel heading the amount at the phase of its sum, its amplitude the
   integer square root in 32nds, the six summed on the phase circle of N
   steps, the size of the sum in the same units) from the arrivals the
   arrays and the engine's Node hold, once per group (owner, sign, flow) and
   summed over the groups, in quanta^(1/2), the |sum_p A_p| = 3 |u| of
   DERIVATIONS.md section 39 (|u| is that over three). The replay is checked
   against the record tick by tick (the shadows on the board, the escapes,
   the body's momentum line and the books; `identity_of`), so the reading
   belongs to the fingerprinted run; on a probe world the replay also reads,
   per tick, the momentum on the shadows (the arrays' momentum cells, the
   whole rays beside them, the engine's Nodes) and on the probe (its
   register), and checks that probe + shadows + body + escaped is zero at
   every tick (the runner's ledger line of the momentum field does not sum
   the momentum carried on rays, so the world's zero is read here).
   `pulse` and `standing` (open) and
   `standing_closed` are replayed for the shells; every closed probe world is
   replayed for the amplitude at the test thing's own Node (the engine's
   Node, the probe returning the shares it reads).

The front's arrival per direction (the pulse): at the read Nodes (r, 0, 0),
(m, m, 0), (m, m, m) for the three radii of each direction, the first tick at
which the Node's content reaches 1 % of its peak over the run, and the tick of
the peak; DERIVATIONS.md section 27 (iii) predicts the peak at sqrt 3 r.

The 1/r^2 fit (the probes): per direction, the pushed amount at the three
radii is the test thing's momentum along the radial direction, on the open
board cumulative at tick 40 (the momentum line less the thing's own amount x
heading; for a wave train that passes, the time-integrated push is the
content that crossed the shell over its area, Gauss for a pulse) and its mean
per interval over ticks 2 to 21 (the first twenty read intervals); on the
closed board the mean push per interval over the last twenty ticks (101 to
120, the settled push) and over every window of twenty, with the settling
tick (the first tick from which every later window of twenty stays within
10 % of the last); the log-log least-squares slope over the three radii; the
anisotropy is the axis fit's value over the (111) fit's value at r = 8 and
12, DERIVATIONS.md section 27 (v) predicting 1 - 1.25 omega^2 for a clocked
source and no far field at all for a clockless one. The 1/r fit (the
amplitude, closed board): the amplitude at the test thing's Node, mean over
the last twenty ticks, and at the same Node of the free field of
`standing_closed`, against r per direction, section 39 predicting 1/r with
half the count's anisotropy; and the wave fraction |sum A|^2 / (3 n), 1 for
a pure wave and 0 for flat-band standing content (section 39 (ii)).

Run:  PYTHONPATH=src python examples/nature/e11_law/analyze.py RUNS_DIR [RUNS_DIR ...] [--worlds DIR] [--record record.json] [--tables tables.md] [--no-replay] [--replay-jobs N]
      (each RUNS_DIR holds <name>/run/run.json for worlds written by make_worlds.py; the first
      directory that holds a world's record is read; a replay is cached as <name>/replay.json)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from make_worlds import CLOSED_TICKS, HALF, PROBES, cases  # noqa: E402

PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
PROBE_THING = 2
BODY_THING = 3
EARLY = (2, 21)
FRONT_THRESHOLD = 0.01
SETTLE_WINDOW = 20
SETTLE_TOLERANCE = 0.10
OPEN_WINDOWS = ((2, 11), (12, 21), (22, 31), (32, 40))
CLOSED_WINDOWS = tuple((a, a + 19) for a in range(1, CLOSED_TICKS, 20))


def load_record(runs, name):
    for directory in runs:
        path = Path(directory) / name / "run" / "run.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")), Path(directory)
    return None, None


def books(record):
    """The books per bit at every completed tick, from the record's audit."""
    rows = []
    for entry in record["audit"]:
        rows.append(
            {
                "tick": entry["tick"],
                "balanced": bool(entry["balanced"]),
                "real_balanced": all(line["balanced"] for line in entry["real"].values()),
                "shadow_balanced": all(line["balanced"] for line in entry["shadow"].values()),
                "real_conserved": bool(entry.get("real_conserved", False)),
                "momentum_current": list(entry["fields"]["momentum"]["current"]),
                "momentum_escaped": list(entry["fields"]["momentum"]["escaped"]),
                "bodies_momentum": list(entry["bodies"]["momentum"]),
            }
        )
    return rows


def unit(vector):
    norm = math.sqrt(sum(c * c for c in vector))
    return tuple(c / norm for c in vector)


def window_mean(rows, key, a, b):
    values = [row[key] for row in rows if a <= row["tick"] <= b]
    return sum(values) / len(values) if values else None


def settling_tick(rows, key, window=SETTLE_WINDOW, tolerance=SETTLE_TOLERANCE):
    """The first tick t from which every mean of `key` over [s, s + window) with
    s >= t stays within `tolerance` of the mean over the last window; None
    when even the last two windows disagree."""
    values = [row[key] for row in rows]
    n = len(values)
    if n < 2 * window:
        return None
    final = sum(values[n - window :]) / window
    scale = abs(final) if final else 1.0
    ok = [abs(sum(values[s : s + window]) / window - final) <= tolerance * scale for s in range(0, n - window + 1)]
    t = n - window
    while t > 0 and ok[t - 1]:
        t -= 1
    # Settled only when at least the two last windows agree.
    return t + 1 if t <= n - 2 * window else None


def probe_reading(record, offset, heading, closed=False):
    """The test thing's momentum line per tick, its push per interval (the
    increments of the line less its own amount x heading), the cumulative push
    and its radial component."""
    radial = unit(offset)
    own = [c * 1 for c in heading]
    rows = []
    previous = [0, 0, 0]
    for tick, line in enumerate(record["momentum"], start=1):
        vector = list(line.get(str(PROBE_THING), [0, 0, 0]))
        body_vector = list(line.get(str(BODY_THING), [0, 0, 0]))
        carried = [vector[k] - own[k] for k in range(3)]
        push = [carried[k] - previous[k] for k in range(3)]
        previous = carried
        audit = record["audit"][tick - 1]
        line = audit["fields"]["momentum"]
        current, returned, escaped = list(line["current"]), list(line["returned"]), list(line["escaped"])
        rows.append(
            {
                "tick": tick,
                "momentum": vector,
                "carried": carried,
                "push": push,
                "push_radial": sum(push[k] * radial[k] for k in range(3)),
                "cumulative_radial": sum(carried[k] * radial[k] for k in range(3)),
                "body_momentum": body_vector,
                "ledger_momentum": {"current": current, "returned": returned, "escaped": escaped},
                "computation": record["computation_per_tick"][tick - 1],
            }
        )
    early = [row["push_radial"] for row in rows if EARLY[0] <= row["tick"] <= EARLY[1]]
    windows = CLOSED_WINDOWS if closed else OPEN_WINDOWS
    last = rows[-SETTLE_WINDOW:]
    before = rows[-2 * SETTLE_WINDOW : -SETTLE_WINDOW]
    return {
        "offset": list(offset),
        "heading": list(heading),
        "radius": math.sqrt(sum(c * c for c in offset)),
        "closed": closed,
        "ticks": rows,
        "cumulative_radial_at_end": rows[-1]["cumulative_radial"],
        "cumulative_radial_at_30": next((r["cumulative_radial"] for r in rows if r["tick"] == 30), None),
        "early_mean_radial": sum(early) / len(early) if early else 0.0,
        "window_means": {f"{a}-{b}": window_mean(rows, "push_radial", a, b) for a, b in windows},
        "settled_push": sum(r["push_radial"] for r in last) / len(last),
        "settled_push_error": standard_error([r["push_radial"] for r in last]),
        "settled_push_before": sum(r["push_radial"] for r in before) / len(before) if before else None,
        "settling_tick": settling_tick(rows, "push_radial") if closed else None,
        "sign_changes": sum(1 for x, y in zip(rows, rows[1:], strict=False) if x["push_radial"] * y["push_radial"] < 0),
        "body_momentum_at_end": rows[-1]["body_momentum"],
        # Filled from the replay (the momentum on the shadows and on the probe
        # read from the engine's arrays and Nodes): `in_flight_at_end` and
        # `world_momentum_zero_every_tick`.
        "in_flight_at_end": None,
        "world_momentum_zero_every_tick": None,
        "recoil_home_fraction": (
            -sum(rows[-1]["body_momentum"][k] * radial[k] for k in range(3)) / rows[-1]["cumulative_radial"]
            if rows[-1]["cumulative_radial"] else None
        ),
        "waited_intervals": sum(1 for r in rows if r["computation"] == 0 and r["tick"] >= 2),
    }


def standard_error(values):
    """The standard error of the mean of `values` (the sample deviation over root n)."""
    n = len(values)
    if n < 2:
        return None
    mean = sum(values) / n
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1) / n)


def fit_slope(points):
    """Log-log least squares of |y| against r over (r, y) with y != 0."""
    xs = [math.log(r) for r, y in points if y]
    ys = [math.log(abs(y)) for r, y in points if y]
    if len(xs) < 2:
        return None
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    slope = sxy / sxx
    intercept = my - slope * mx
    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys, strict=True))
    error = math.sqrt(residual / (n - 2) / sxx) if n > 2 else None
    return {"slope": slope, "intercept": intercept, "error": error, "points": n, "signs": [1 if y > 0 else -1 for r, y in points if y]}


def fit_value(fit, r):
    return math.exp(fit["intercept"] + fit["slope"] * math.log(r)) if fit else None


# ----------------------------------------------------------- the replay


def read_board(world, index, shape):
    """The body's shadows per Node and Port heading after a tick: outgoing and
    returning shares on their way, and the parked shares in whole quanta. The
    dense region's arrays (arrivals per Node, owner, flow, sign, Port and phase
    layer, and the departures in flight; the parked ninths per Node, owner,
    flow, sign and Port) hold every share the layer carries, and the engine's
    Nodes hold the rest (the body's own Node, a thing's Node); the reading is
    checked equal to the inventory view's on a small closed world before the
    run (moving content and parked ninths, tick by tick)."""
    spatial = world._spatial
    family = spatial.dense.families[index]
    definition = world.initial.spatial_fields[index]
    ports = [PORTS.index(tuple(h)) for h in definition.headings]
    arr = family.arr_amt.astype(np.int64) + family.fly_amt.astype(np.int64)
    # axes: x, y, z, owner, flow (0 outgoing, 1 returning), sign, port, layer
    out = np.ascontiguousarray(np.transpose(arr[:, :, :, :, 0].sum(axis=(3, 4, 6)), (3, 0, 1, 2)))
    ret = np.ascontiguousarray(np.transpose(arr[:, :, :, :, 1].sum(axis=(3, 4, 6)), (3, 0, 1, 2)))
    park_ninths = family.reg.astype(np.int64).sum(axis=(3, 4, 5, 6))
    for position, rays in family.overflow.items():
        for ray in rays:
            (out if ray.outbound else ret)[(ports[ray.heading], *position)] += ray.amount
    for position, node in spatial.nodes.items():
        if not node.rays:
            continue
        for ray in node.rays[index]:
            if ray.detector != 0:
                continue
            if ray.parked:
                park_ninths[position] += ray.amount
                continue
            (out if ray.outbound else ret)[(ports[ray.heading], *position)] += ray.amount
    return out, ret, park_ninths // family.total


def momenta(world, index):
    """The momentum on rays after a tick: on the shadows (the layer's arrays of
    arrivals, departures and parked ninths, the whole rays beside them and the
    engine's Nodes' shadows; checked equal to the inventory view's sum on a
    small closed world) and on the real rays (a thing's register, the pushes
    it has taken); the bodies' is `external_bodies()`."""
    spatial = world._spatial
    family = spatial.dense.families[index]
    axes = tuple(range(family.arr_mom.ndim - 1))
    shadows = (
        family.arr_mom.astype(np.int64).sum(axis=axes)
        + family.fly_mom.astype(np.int64).sum(axis=axes)
        + family.reg_mom.astype(np.int64).sum(axis=tuple(range(family.reg_mom.ndim - 1)))
    )
    shadows = [int(c) for c in shadows]
    real = [0, 0, 0]
    for rays in family.overflow.values():
        for ray in rays:
            if ray.momentum is not None:
                for k in range(3):
                    shadows[k] += ray.momentum[k]
    for node in spatial.nodes.values():
        if not node.rays:
            continue
        for family_rays in node.rays:
            for ray in family_rays:
                if ray.momentum is None:
                    continue
                target = shadows if ray.detector == 0 else real
                for k in range(3):
                    target[k] += ray.momentum[k]
    return shadows, real


def arrivals_at(world, index, position):
    """The shadows that arrived at a Node in the interval just completed, as
    rays: from the layer's arrival arrays (one ray per owner, flow, sign, Port
    and phase layer) and from the engine's Node when it holds the Node."""
    spatial = world._spatial
    family = spatial.dense.families[index]
    rays = []
    amounts, phases, momenta = family.arr_amt[position], family.arr_ph[position], family.arr_mom[position]
    for cell in zip(*np.nonzero(amounts), strict=True):
        rank, flow, sign, port, layer = (int(c) for c in cell)
        rays.append(family.ray(rank, flow, sign, port, int(amounts[cell]), int(phases[cell]), momenta[cell]))
    rays.extend(family.overflow.get(position, ()))
    node = spatial.nodes.get(position)
    if node is not None and node.rays:
        rays.extend(ray for ray in node.rays[index] if ray.detector == 0 and not ray.parked and ray.steps >= 1)
    return rays


def amplitude_at(world, index, position):
    """The amplitude a thing at the Node would read (wait-reads-v1): the size of
    the coherent sum per group (owner, sign, flow) by the engine's
    `arrival_amplitude`, in quanta^(1/2), and their sum; beside it the amount
    that arrived, per flow."""
    from event_universe.core.spatial_state import MIXING_AMPLITUDE_SCALE, arrival_amplitude

    definition = world.initial.spatial_fields[index]
    groups = {}
    for ray in arrivals_at(world, index, position):
        groups.setdefault((ray.owner, ray.source_sign, ray.outbound), []).append(ray)
    sizes = {}
    amounts = {"outgoing": 0, "returning": 0}
    for (owner, sign, outbound), members in groups.items():
        size = arrival_amplitude(tuple(members), definition) / MIXING_AMPLITUDE_SCALE
        sizes[f"{owner}:{sign}:{'out' if outbound else 'ret'}"] = size
        amounts["outgoing" if outbound else "returning"] += sum(ray.amount for ray in members)
    return {"sum": sum(sizes.values()), "groups": sizes, "arrived": amounts}


def replay(document, ticks, read_nodes, log=print, shells=True):
    """The world through the Simulation API: per tick the shells and the
    fractions, the content, J and the amplitude at the read Nodes, and the
    ledger."""
    from event_universe import Simulation
    from event_universe.initialization import parse_initial_state

    shape = tuple(int(n) for n in document["shape"])
    centre = tuple(int(c) for c in document["external_bodies"][0]["position"])
    grid = np.indices(shape, dtype=np.int64) - np.array(centre, dtype=np.int64)[:, None, None, None]
    if document.get("boundary") == "periodic":
        # The nearest image of every Node on the closed board.
        for k in range(3):
            grid[k] = (grid[k] + shape[k] // 2) % shape[k] - shape[k] // 2
    l1 = np.abs(grid).sum(axis=0)
    radius = np.sqrt((grid * grid).sum(axis=0).astype(float))
    euclid = np.rint(radius).astype(np.int64)
    nonzero = (grid != 0).sum(axis=0)
    unit_r = np.where(radius > 0, grid / np.maximum(radius, 1e-9), 0.0)
    kmax = max(shape) // 2
    headings = np.array(PORTS, dtype=np.int64)
    per_tick = []
    ledgers = []
    with Simulation(parse_initial_state(document)) as world:
        index = 0
        for tick in range(1, ticks + 1):
            started = time.perf_counter()
            world.step()
            stepped = time.perf_counter() - started
            out, ret, park = read_board(world, index, shape)
            signed = out - ret
            jvec = np.einsum("pxyz,pk->kxyz", signed, headings)
            jr = (jvec * unit_r).sum(axis=0)
            out_total, ret_total, park_total = out.sum(axis=0), ret.sum(axis=0), park
            total = int(out_total.sum() + ret_total.sum() + park_total.sum())
            row = {"tick": tick, "seconds": round(stepped, 3), "on_board": total}
            if shells:
                for kind, level in (("l1", l1), ("euclid", euclid)):
                    rows = []
                    for k in range(0, kmax + 1):
                        mask = level == k
                        n = int(mask.sum())
                        if n == 0:
                            continue
                        content = int(out_total[mask].sum() + ret_total[mask].sum() + park_total[mask].sum())
                        rows.append(
                            {
                                "k": k,
                                "nodes": n,
                                "out": int(out_total[mask].sum()),
                                "ret": int(ret_total[mask].sum()),
                                "parked": int(park_total[mask].sum()),
                                "content": content,
                                "per_node": content / n,
                                "jr": float(jr[mask].sum()),
                                "jr_per_node": float(jr[mask].sum()) / n,
                            }
                        )
                    row[kind] = rows
            moving = out_total + ret_total
            row["fractions"] = {
                "axes": float(moving[nonzero <= 1].sum()) / total if total else 0.0,
                "planes_off_axes": float(moving[nonzero == 2].sum()) / total if total else 0.0,
                "off_planes": float(moving[nonzero == 3].sum()) / total if total else 0.0,
                "parked": float(park_total.sum()) / total if total else 0.0,
            }
            row["read_nodes"] = {}
            for label, offset in read_nodes.items():
                position = tuple(centre[k] + offset[k] for k in range(3))
                radial = unit(offset)
                j = [int(jvec[k][position]) for k in range(3)]
                amplitude = amplitude_at(world, index, position)
                content = int(out_total[position] + ret_total[position] + park_total[position])
                arrived = amplitude["arrived"]["outgoing"] + amplitude["arrived"]["returning"]
                row["read_nodes"][label] = {
                    "content": content,
                    "out": int(out_total[position]),
                    "ret": int(ret_total[position]),
                    "parked": int(park_total[position]),
                    "j": j,
                    "j_radial": sum(j[k] * radial[k] for k in range(3)),
                    "amplitude": amplitude["sum"],
                    "amplitude_groups": amplitude["groups"],
                    "arrived": arrived,
                    "wave_fraction": amplitude["sum"] ** 2 / (3 * arrived) if arrived else None,
                }
            row["escaped"] = int(world.escaped_totals()["proton"][0])
            ledger = world.audit()
            ledgers.append(ledger)
            row["balanced"] = bool(ledger["balanced"]) and bool(ledger.get("real_conserved", True))
            row["body_momentum"] = [list(b["momentum"]) for b in world.external_bodies()]
            row["shadow_momentum"], row["real_momentum"] = momenta(world, index)
            row["world_zero"] = all(
                row["shadow_momentum"][k] + row["real_momentum"][k] + sum(b[k] for b in row["body_momentum"]) + int(world.audit()["fields"]["momentum"]["escaped"][k]) == 0
                for k in range(3)
            )
            per_tick.append(row)
            log(
                f"  tick {tick} {stepped:.2f}s on board {total} escaped {row['escaped']} "
                f"off planes {row['fractions']['off_planes']:.3f} balanced {row['balanced']}"
            )
    return per_tick, ledgers


def identity_of(per_tick, run):
    """The replay against the record, tick by tick: the shadows on the board
    (the record's `shadow_content`), the escapes (the audit's shadow line), the
    bodies' momentum (the runner's `momentum` line of thing 3) and, on a probe
    world, the probe's momentum line (thing 2, read from the replay's ledger
    as the world's momentum less the body's and the shadows' is not available
    here, so the bodies' line stands for it); all four True is the identity."""
    audit = run["audit"]
    checks = {
        "shadows_on_board": [row["on_board"] for row in per_tick] == list(run["shadow_content"][: len(per_tick)]),
        "escaped": all(row["escaped"] == audit[i]["shadow"]["proton"]["escaped"][0] for i, row in enumerate(per_tick)),
        "body_momentum": all(
            row["body_momentum"][0] == list(run["momentum"][i].get(str(BODY_THING), [0, 0, 0])) for i, row in enumerate(per_tick)
        ),
        "balanced": all(row["balanced"] == (bool(audit[i]["balanced"]) and bool(audit[i].get("real_conserved", True))) for i, row in enumerate(per_tick)),
    }
    if all("real_momentum" in row for row in per_tick) and str(PROBE_THING) in run["momentum"][-1]:
        # The probe's momentum line of the record is its own amount x heading
        # plus the register the replay reads.
        heading = None
        for row, line in zip(per_tick, run["momentum"], strict=True):
            probe = line.get(str(PROBE_THING))
            if probe is None:
                continue
            if heading is None:
                heading = [probe[k] - row["real_momentum"][k] for k in range(3)]
            if [probe[k] - heading[k] for k in range(3)] != row["real_momentum"]:
                checks["probe_momentum"] = False
                break
        else:
            checks["probe_momentum"] = True
        checks["world_zero_every_tick"] = all(row["world_zero"] for row in per_tick)
    checks["identical"] = all(checks.values())
    return checks


def replay_world(job):
    """One replay (a worker of the pool): the world's document, its record and
    the cache to write; the replay's identity to the record is checked
    (`identity_of`), and the replay's ledger shadow line is kept beside it."""
    name, world_path, run_path, cache_path, labels, shells = job
    document = json.loads(Path(world_path).read_text(encoding="utf-8"))
    run = json.loads(Path(run_path).read_text(encoding="utf-8"))
    started = time.perf_counter()
    per_tick, ledgers = replay(document, run["completed_ticks"], labels, log=lambda _: None, shells=shells)
    identity = identity_of(per_tick, run)
    shadow_lines = json.loads(json.dumps([entry["shadow"] for entry in ledgers]))
    identity["ledger_shadow_line"] = shadow_lines == [entry["shadow"] for entry in run["audit"]]
    Path(cache_path).write_text(
        json.dumps({"per_tick": per_tick, "identity": identity, "seconds": round(time.perf_counter() - started, 1)}),
        encoding="utf-8",
    )
    return name, identity["identical"], round(time.perf_counter() - started, 1)


def front(per_tick, label):
    """The first tick at which the read Node's content reaches 1 % of its peak, and the peak's tick."""
    series = [row["read_nodes"][label]["content"] for row in per_tick]
    peak = max(series)
    if peak <= 0:
        return {"first": None, "peak_tick": None, "peak": 0}
    first = next(t for t, c in enumerate(series, start=1) if c >= FRONT_THRESHOLD * peak)
    return {"first": first, "peak_tick": series.index(peak) + 1, "peak": peak}


def read_node_labels():
    labels = {}
    for direction, (offsets, _, letter) in PROBES.items():
        for offset in offsets:
            labels[f"{direction}_{letter}{offset[0]}"] = offset
    return labels


def mean_over(rows, read):
    values = [read(row) for row in rows]
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def settled_reading(per_tick, labels, window=SETTLE_WINDOW):
    """The mean over the last window and over the one before it, per L1 shell and per read Node."""
    last = per_tick[-window:]
    before = per_tick[-2 * window : -window]
    settled = {}
    for k in range(0, HALF + 1):
        def shell(row, key, k=k):
            return next((x[key] for x in row.get("l1", ()) if x["k"] == k), None)

        settled[k] = {
            "per_node": mean_over(last, lambda r: shell(r, "per_node")),
            "per_node_before": mean_over(before, lambda r: shell(r, "per_node")),
            "jr_per_node": mean_over(last, lambda r: shell(r, "jr_per_node")),
            "jr_per_node_before": mean_over(before, lambda r: shell(r, "jr_per_node")),
        }
    nodes = {}
    for label in labels:
        nodes[label] = {
            key: mean_over(rows, lambda r, key=key, label=label: r["read_nodes"][label][key.removesuffix("_before")])
            for key in ("content", "content_before", "j_radial", "j_radial_before", "amplitude", "amplitude_before", "arrived", "wave_fraction")
            for rows in ((before if key.endswith("_before") else last),)
        }
        nodes[label]["settling_tick_content"] = settling_tick([{"tick": r["tick"], "v": r["read_nodes"][label]["content"]} for r in per_tick], "v")
        nodes[label]["settling_tick_amplitude"] = settling_tick([{"tick": r["tick"], "v": r["read_nodes"][label]["amplitude"]} for r in per_tick], "v")
    return settled, nodes


# ------------------------------------------------------------- the tables


def fmt(value, digits=1):
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def standing_line(w):
    sf = w.get("standing_field") or {}
    if not sf:
        return "no standing-set search"
    res = sf.get("standing_field_residual") or {}
    return (
        f"fixed point or cycle found {sf.get('standing_field')}, iterations to the repeat {sf.get('standing_field_iterations')}, "
        f"period {sf.get('standing_field_period')}, residual at the last comparison {res.get('cells', '-')} cells and {res.get('amount', '-')} quanta, "
        f"ticks kept fixed {sf.get('standing_field_ticks')}, fallback {sf.get('standing_field_fallback')}"
    )


def tables(record):
    lines = []
    lines.append("### The books per bit\n")
    lines.append("| World | Board | Ticks | World line balanced | Real line | Shadow line | `real_conserved` | Shadows at start | At the end | Escaped | Runner s | Source |")
    lines.append("| --- | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |")
    for name, row in record["worlds"].items():
        b = row["books"]
        lines.append(
            f"| `{name}` | {row['boundary']} | {row['completed_ticks']} | {'every tick' if all(x['balanced'] for x in b) else 'NO'} | "
            f"{'every tick' if all(x['real_balanced'] for x in b) else 'NO'} | {'every tick' if all(x['shadow_balanced'] for x in b) else 'NO'} | "
            f"{'every tick' if all(x['real_conserved'] for x in b) else 'NO'} | {row['shadows_initial']} | {row['shadows_final']} | {row['escaped']} | {fmt(row['elapsed_seconds'])} | `{row['source_sha256'][:8]}` |"
        )
    if record.get("identity_check"):
        ic = record["identity_check"]
        lines.append(
            f"\nThe world `{ic['world']}` recorded on the source `{ic['earlier_source'][:8]}` and run again on `{ic['later_source'][:8]}`: "
            f"the audit per tick identical {ic['audit_identical']}, the shadows per tick identical {ic['shadow_content_identical']}, the momentum lines identical {ic['momentum_identical']}.\n"
        )
    if "standing_closed" in record["replays"]:
        c = record["replays"]["standing_closed"]
        w = record["worlds"]["standing_closed"]
        lines.append("\n### The standing world (`standing_closed`): the field of the thing at rest on the closed board, `boundary` periodic, 120 ticks, `standing_field` on\n")
        lines.append(f"The runner's standing-set search: {standing_line(w)}. Shadows on the board at every tick: {w['shadows_initial']} (escaped {w['escaped']}). Off the planes, mean of the last twenty ticks: {c['off_planes_last_20']:.3f}. The replay identical to the record tick by tick (shadows on the board, escapes, the body's momentum, the books): {c['ledger_identical_to_record']}.\n")
        lines.append("| k (L1) | Nodes | Content per Node, ticks 81-100 | 101-120 | J_r per Node, 81-100 | 101-120 |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: |")
        nodes_of = {x["k"]: x["nodes"] for x in c["per_tick"][-1]["l1"]}
        for k, v in c["settled"].items():
            if v["per_node"] is None:
                continue
            lines.append(f"| {k} | {nodes_of.get(int(k), '-')} | {v['per_node_before']:.0f} | {v['per_node']:.0f} | {v['jr_per_node_before']:.0f} | {v['jr_per_node']:.0f} |")
        lines.append("\n| Read Node (free field) | r | Content, ticks 81-100 | 101-120 | Settled from tick | J_r, 81-100 | 101-120 | Amplitude, 81-100 | 101-120 | Settled from tick | Wave fraction |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for label, v in c["settled_read_nodes"].items():
            r = record["read_nodes"][label]["radius"]
            lines.append(f"| {label} | {r:.2f} | {v['content_before']:.0f} | {v['content']:.0f} | {fmt(v['settling_tick_content'])} | {v['j_radial_before']:.1f} | {v['j_radial']:.1f} | {v['amplitude_before']:.1f} | {v['amplitude']:.1f} | {fmt(v['settling_tick_amplitude'])} | {fmt(v['wave_fraction'], 3)} |")
        lines.append("\n| t | On the board | Content per Node at k = 4 | 8 | 12 | J_r per Node at k = 4 | 8 | 12 | Off the planes | Parked | Step s |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in c["per_tick"]:
            if row["tick"] in (1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120):
                j = {x["k"]: x["jr_per_node"] for x in row["l1"]}
                n = {x["k"]: x["per_node"] for x in row["l1"]}
                lines.append(f"| {row['tick']} | {row['on_board']} | {n.get(4, 0):.0f} | {n.get(8, 0):.0f} | {n.get(12, 0):.0f} | {j.get(4, 0):.0f} | {j.get(8, 0):.0f} | {j.get(12, 0):.0f} | {row['fractions']['off_planes']:.3f} | {row['fractions']['parked']:.3f} | {row['seconds']} |")
    open_probes = {k: v for k, v in record["probes"].items() if not v["closed"]}
    closed_probes = {k: v for k, v in record["probes"].items() if v["closed"]}
    if closed_probes:
        lines.append("\n### The test things (the nine closed probe worlds): the push per interval per window of twenty, the settled push and the amplitude at the thing's Node\n")
        lines.append("| Probe | r | Ticks 1-20 | 21-40 | 41-60 | 61-80 | 81-100 | 101-120 (+- its standard error) | Settled from tick | Sign changes | Amplitude at the Node, 81-100 | 101-120 | Arrived per interval, 101-120 | Wave fraction | Free-field amplitude (`standing_closed`), 101-120 | Intervals waited | Cumulative push at 120 | Body's momentum at 120 | Recoil home | In flight on the shadows at 120 (replay) | Probe + shadows + body = 0 every tick (replay) | Standing-set search |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | --- | --- |")
        for label, probe in closed_probes.items():
            w = probe["window_means"]
            amp = record["amplitude_at_probes"].get(label, {})
            free = record["replays"].get("standing_closed", {}).get("settled_read_nodes", {}).get(label, {})
            sf = (record["worlds"][f"probe_{label}"].get("standing_field") or {})
            search = f"{sf.get('standing_field')}, iterations {sf.get('standing_field_iterations')}, residual {(sf.get('standing_field_residual') or {}).get('amount', '-')}"
            lines.append(
                f"| `{label}` | {probe['radius']:.2f} | " + " | ".join(f"{w[k]:.1f}" for k in ("1-20", "21-40", "41-60", "61-80", "81-100", "101-120")) +
                f" +- {probe['settled_push_error']:.0f} | {fmt(probe['settling_tick'])} | {probe['sign_changes']} | {fmt(amp.get('amplitude_before'))} | {fmt(amp.get('amplitude'))} | {fmt(amp.get('arrived'), 0)} | {fmt(amp.get('wave_fraction'), 3)} | {fmt(free.get('amplitude'))} | {probe['waited_intervals']} | {probe['cumulative_radial_at_end']:.0f} | {probe['body_momentum_at_end']} | {fmt(100 * probe['recoil_home_fraction'], 1) if probe['recoil_home_fraction'] is not None else '-'} % | {probe['in_flight_at_end'] if probe['in_flight_at_end'] is not None else 'not read'} | {probe['world_momentum_zero_every_tick'] if probe['world_momentum_zero_every_tick'] is not None else 'not read'} | {search} |"
            )
    fit_tables(lines, record, "closed")
    open_probes_block(lines, record, open_probes)
    if "pulse" in record["replays"]:
        p = record["replays"]["pulse"]
        lines.append("\n### The pulse (open board, measured earlier): the front per direction and the release off the planes\n")
        lines.append("| Read Node | r | sqrt 3 r | First arrival (tick) | Peak (tick) | Peak content |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
        for label, f in p["fronts"].items():
            r = record["read_nodes"][label]["radius"]
            lines.append(f"| {label} | {r:.2f} | {math.sqrt(3) * r:.1f} | {fmt(f['first'])} | {fmt(f['peak_tick'])} | {f['peak']} |")
        lines.append("\n| t | On the board | Escaped | On the axes | On the planes off the axes | Off the planes | Parked |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in p["per_tick"]:
            if row["tick"] in (1, 2, 3, 5, 10, 20, 30, 40):
                f = row["fractions"]
                lines.append(f"| {row['tick']} | {row['on_board']} | {row['escaped']} | {f['axes']:.3f} | {f['planes_off_axes']:.3f} | {f['off_planes']:.3f} | {f['parked']:.3f} |")
    if "standing" in record["replays"]:
        s = record["replays"]["standing"]
        lines.append("\n### The field of the thing at rest on the open board (measured earlier), shell by shell (L1 shells; content per Node / J_r per Node)\n")
        ticks_shown = (1, 5, 10, 20, 30, 40)
        lines.append("| k | Nodes | " + " | ".join(f"t = {t}" for t in ticks_shown) + " |")
        lines.append("| ---: | ---: | " + " | ".join("---:" for _ in ticks_shown) + " |")
        by_tick = {row["tick"]: row for row in s["per_tick"]}
        for k in range(0, HALF + 1):
            cells, nodes = [], None
            for t in ticks_shown:
                shell = next((x for x in by_tick[t]["l1"] if x["k"] == k), None)
                if shell is None:
                    cells.append("-")
                    continue
                nodes = shell["nodes"]
                cells.append(f"{shell['per_node']:.0f} / {shell['jr_per_node']:.0f}")
            lines.append(f"| {k} | {nodes} | " + " | ".join(cells) + " |")
        lines.append("\n| t | On the board | Escaped | J_r per Node at k = 4 | 8 | 12 | Off the planes |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in s["per_tick"]:
            if row["tick"] in (1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40):
                j = {x["k"]: x["jr_per_node"] for x in row["l1"]}
                lines.append(f"| {row['tick']} | {row['on_board']} | {row['escaped']} | {j.get(4, 0):.0f} | {j.get(8, 0):.0f} | {j.get(12, 0):.0f} | {row['fractions']['off_planes']:.3f} |")
    fit_tables(lines, record, "open")
    return "\n".join(lines) + "\n"


def fit_tables(lines, record, board):
    lines.append(f"\n### The 1/r^2 fit per direction and the anisotropy ({board} board)\n")
    lines.append("| Direction | Quantity | Slope (log-log over three radii) | Standard error | Value at r = 8 | At r = 12 | Signs |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | --- |")
    for direction, fits in record["fits"].get(board, {}).items():
        for quantity, fit in fits.items():
            if fit:
                lines.append(f"| {direction} | {quantity} | {fit['slope']:.2f} | {fmt(fit['error'], 2)} | {fit_value(fit, 8):.1f} | {fit_value(fit, 12):.1f} | {fit['signs']} |")
    lines.append("\n| Quantity | Axis / (111) at r = 8 | At r = 12 | Axis / (110) at r = 8 | At r = 12 |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for quantity, a in record["anisotropy"].get(board, {}).items():
        lines.append(f"| {quantity} | {fmt(a.get('axis_over_111_at_8'), 3)} | {fmt(a.get('axis_over_111_at_12'), 3)} | {fmt(a.get('axis_over_110_at_8'), 3)} | {fmt(a.get('axis_over_110_at_12'), 3)} |")


def open_probes_block(lines, record, open_probes):
    if open_probes:
        lines.append("\n## The open board, measured earlier (recorded; not the series)\n\nThe eight open-board records below were made before the model owner's decision that only closed worlds are tested (Highlights 5.4, \"The board of a run is closed\"); they are kept as recorded and stand outside the series' reading.\n")
        lines.append("\n### The test things on the open board: the pushed amount per interval and the inventory's J at the same Node\n")
        lines.append("| Probe | r | Cumulative radial push at 40 | At 30 | Mean per interval, ticks 2-21 | 2-11 | 12-21 | 22-31 | 32-40 | Sign changes | Inventory J_r, mean 2-21 (`standing`) | Content per Node at 2 / 21 / 40 | Intervals waited | Body's momentum at 40 | Recoil home | Ledger momentum lines at 40 (current, returned, escaped) |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | --- | --- |")
        for label, probe in open_probes.items():
            inv = record["inventory_at_read_nodes"].get(label, {})
            w = probe["window_means"]
            lines.append(
                f"| `{label}` | {probe['radius']:.2f} | {probe['cumulative_radial_at_end']:.0f} | {fmt(probe['cumulative_radial_at_30'], 0)} | "
                f"{probe['early_mean_radial']:.1f} | {w['2-11']:.1f} | {w['12-21']:.1f} | {w['22-31']:.1f} | {w['32-40']:.1f} | {probe['sign_changes']} | "
                f"{fmt(inv.get('j_radial_mean_2_21'))} | {inv.get('content_2', '-')} / {inv.get('content_21', '-')} / {inv.get('content_40', '-')} | {probe['waited_intervals']} | {probe['body_momentum_at_end']} | {fmt(100 * probe['recoil_home_fraction'], 1) if probe['recoil_home_fraction'] is not None else '-'} % | {probe['ticks'][-1]['ledger_momentum']} |"
            )


QUANTITIES = {
    "open": {
        "cumulative_push_at_40": lambda p: p["cumulative_radial_at_end"],
        "mean_push_2_21": lambda p: p["early_mean_radial"],
    },
    "closed": {
        "settled_push_101_120": lambda p: p["settled_push"],
        "push_81_100": lambda p: p["settled_push_before"],
    },
}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("runs", type=Path, nargs="+")
    parser.add_argument("--worlds", type=Path, default=HERE)
    parser.add_argument("--record", type=Path, default=HERE / "record.json")
    parser.add_argument("--tables", type=Path, default=HERE / "tables.md")
    parser.add_argument("--no-replay", action="store_true")
    parser.add_argument("--replay-jobs", type=int, default=1, help="replays at once (processes)")
    parser.add_argument("--identity", type=Path, default=None, help="a second run.json of `standing` (another source) to compare with the record read")
    parser.add_argument("--prior-record", type=Path, default=None, help="an earlier record.json whose replay rows stand in for a world whose replay cache is absent (no new replay is made for it)")
    args = parser.parse_args(argv)
    labels = read_node_labels()
    record = {
        "experiment": "E11 repeated under the law of the bit (2026-09-18)",
        "read_nodes": {label: {"offset": list(o), "radius": math.sqrt(sum(c * c for c in o))} for label, o in labels.items()},
        "worlds": {},
        "probes": {},
        "replays": {},
        "inventory_at_read_nodes": {},
        "amplitude_at_probes": {},
        "fits": {"open": {}, "closed": {}},
        "anisotropy": {"open": {}, "closed": {}},
        "identity_check": None,
    }
    documents = dict(cases())
    found = {}
    for name in documents:
        run, directory = load_record(args.runs, name)
        if run is None:
            print(f"{name}: no record")
            continue
        found[name] = directory
        b = books(run)
        record["worlds"][name] = {
            "status": run["status"],
            "completed_ticks": run["completed_ticks"],
            "source_sha256": run["source_sha256"],
            "initialization_sha256": run["initialization_sha256"],
            "elapsed_seconds": run["elapsed_seconds"],
            "books": b,
            "shadows_initial": run["shadow_content"][0] if run["shadow_content"] else None,
            "shadows_final": run["shadow_content"][-1] if run["shadow_content"] else None,
            "escaped": run["escaped_totals"]["proton"][0],
            "body_positions_fixed": all(p[1:] == run["external_bodies"][0]["positions"][0][1:] for p in run["external_bodies"][0]["positions"]),
            "boundary": documents[name]["boundary"],
            "standing_field": {k: run.get(k) for k in ("standing_field", "standing_field_iterations", "standing_field_period", "standing_field_residual", "standing_field_ticks", "standing_field_fallback", "standing_field_max_iterations")} if "standing_field" in run else None,
        }
        if name.startswith("probe_"):
            parts = name.split("_")
            direction, tag, closed = parts[1], parts[2], name.endswith("_closed")
            offsets, heading, letter = PROBES[direction]
            offset = next(o for o in offsets if f"{letter}{o[0]}" == tag)
            record["probes"][f"{direction}_{tag}" + ("_closed" if closed else "")] = probe_reading(run, offset, heading, closed=closed)
        print(f"{name}: {run['status']} {run['completed_ticks']} ticks, books balanced at every tick: {all(x['balanced'] for x in b)}")
    if args.identity and "standing" in record["worlds"]:
        earlier, _ = load_record(args.runs, "standing")
        later = json.loads(args.identity.read_text(encoding="utf-8"))
        record["identity_check"] = {
            "world": "standing",
            "earlier_source": earlier["source_sha256"],
            "later_source": later["source_sha256"],
            "audit_identical": [e["fields"] for e in earlier["audit"]] == [e["fields"] for e in later["audit"]],
            "shadow_content_identical": earlier["shadow_content"] == later["shadow_content"],
            "momentum_identical": earlier["momentum"] == later["momentum"],
            "elapsed_seconds": {"earlier": earlier["elapsed_seconds"], "later": later["elapsed_seconds"]},
        }
    if not args.no_replay:
        to_replay = [n for n in ("pulse", "standing", "standing_closed") if n in record["worlds"]]
        to_replay += [n for n in record["worlds"] if n.startswith("probe_") and n.endswith("_closed")]
        prior = json.loads(args.prior_record.read_text(encoding="utf-8")) if args.prior_record else {}
        from_prior = set()
        jobs = []
        for name in to_replay:
            cache = found[name] / name / "replay.json"
            if cache.exists():
                continue
            if name in prior.get("replays", {}):
                from_prior.add(name)
                continue
            shells = not name.startswith("probe_")
            jobs.append((name, str(args.worlds / f"{name}.json"), str(found[name] / name / "run" / "run.json"), str(cache), labels, shells))
        if jobs:
            print(f"replaying {[j[0] for j in jobs]} in-process, {args.replay_jobs} at once")
            if args.replay_jobs > 1:
                import multiprocessing

                with multiprocessing.get_context("spawn").Pool(args.replay_jobs) as pool:
                    for name, identical, seconds in pool.imap_unordered(replay_world, jobs):
                        print(f"  {name}: ledger identical to the record {identical}, {seconds} s")
            else:
                for job in jobs:
                    name, identical, seconds = replay_world(job)
                    print(f"  {name}: ledger identical to the record {identical}, {seconds} s")
        for name in to_replay:
            if name in from_prior:
                # The earlier record's reading of this world (its replay cache
                # is absent and no new replay is made): the read-Node rows and
                # the identity as recorded there, no momentum reading.
                label = name.removeprefix("probe_").removesuffix("_closed")
                entry = dict(prior["replays"][name])
                entry["from_prior_record"] = str(args.prior_record)
                record["replays"][name] = entry
                record["amplitude_at_probes"][label + "_closed"] = prior["amplitude_at_probes"][label + "_closed"]
                print(f"  {name}: the earlier record's replay rows (identity there: {entry.get('identity', {}).get('identical')})")
                continue
            cache = found[name] / name / "replay.json"
            cached = json.loads(cache.read_text(encoding="utf-8"))
            per_tick = cached["per_tick"]
            run, _ = load_record(args.runs, name)
            identity = identity_of(per_tick, run)
            if "identity" in cached:
                identity["ledger_shadow_line"] = cached["identity"].get("ledger_shadow_line")
            identical = identity["identical"]
            entry = {"per_tick": per_tick, "identity": identity, "ledger_identical_to_record": identical, "replay_seconds": cached.get("seconds")}
            document = documents[name]
            if name == "pulse":
                entry["fronts"] = {label: front(per_tick, label) for label in labels}
                entry["release"] = 6 * (document["external_bodies"][0]["amount"] // document["spatial_fields"][0]["release"][1])
            if name == "standing_closed":
                entry["settled"], entry["settled_read_nodes"] = settled_reading(per_tick, labels)
                entry["off_planes_last_20"] = mean_over(per_tick[-SETTLE_WINDOW:], lambda r: r["fractions"]["off_planes"])
            if name == "standing":
                for label in labels:
                    series = [row["read_nodes"][label] for row in per_tick]
                    early = [s["j_radial"] for s, row in zip(series, per_tick, strict=True) if EARLY[0] <= row["tick"] <= EARLY[1]]
                    record["inventory_at_read_nodes"][label] = {
                        "j_radial_mean_2_21": sum(early) / len(early) if early else None,
                        "j_radial_cumulative_2_40": sum(s["j_radial"] for s, row in zip(series, per_tick, strict=True) if row["tick"] >= 2),
                        "content_2": series[1]["content"],
                        "content_21": series[20]["content"],
                        "content_40": series[-1]["content"],
                        "min_content_2_40": min(s["content"] for s in series[1:]),
                        "amplitude_mean_2_21": mean_over([r for r in per_tick if EARLY[0] <= r["tick"] <= EARLY[1]], lambda r, label=label: r["read_nodes"][label]["amplitude"]),
                    }
            if name.startswith("probe_"):
                label = name.removeprefix("probe_").removesuffix("_closed")
                _, nodes = settled_reading(per_tick, {label: labels[label]})
                node = nodes[label]
                record["amplitude_at_probes"][label + "_closed"] = {
                    "amplitude": node["amplitude"],
                    "amplitude_before": node["amplitude_before"],
                    "arrived": node["arrived"],
                    "wave_fraction": node["wave_fraction"],
                    "settling_tick_amplitude": node["settling_tick_amplitude"],
                    "content": node["content"],
                    "j_radial": node["j_radial"],
                    "groups_at_end": per_tick[-1]["read_nodes"][label]["amplitude_groups"],
                    "per_tick": [row["read_nodes"][label]["amplitude"] for row in per_tick],
                }
                # The shells are not read for a probe world; keep the per-tick
                # read-Node rows only.
                probe = record["probes"][label + "_closed"]
                probe["in_flight_at_end"] = per_tick[-1].get("shadow_momentum")
                probe["world_momentum_zero_every_tick"] = identity.get("world_zero_every_tick")
                probe["in_flight_per_tick"] = [row.get("shadow_momentum") for row in per_tick]
                entry = {"identity": identity, "ledger_identical_to_record": identical, "replay_seconds": cached.get("seconds"), "read_node": [row["read_nodes"][label] for row in per_tick], "momenta": [(row.get("real_momentum"), row.get("shadow_momentum"), row["body_momentum"]) for row in per_tick]}
            record["replays"][name] = entry
            print(f"  {name}: ledger identical to the record: {identical}")
    for board in ("open", "closed"):
        suffix = "_closed" if board == "closed" else ""
        for direction in PROBES:
            probes = [(p["radius"], p) for label, p in record["probes"].items() if label.startswith(direction + "_") and label.endswith(suffix) and (board == "closed" or not p["closed"])]
            record["fits"][board][direction] = {q: fit_slope([(r, read(p)) for r, p in probes]) for q, read in QUANTITIES[board].items()}
            if board == "open":
                points_inv = [
                    (record["read_nodes"][label]["radius"], inv["j_radial_mean_2_21"])
                    for label, inv in record["inventory_at_read_nodes"].items()
                    if label.startswith(direction + "_") and inv["j_radial_mean_2_21"]
                ]
                record["fits"][board][direction]["inventory_j_2_21"] = fit_slope(points_inv)
            else:
                amps = [(record["read_nodes"][label.removesuffix("_closed")]["radius"], a["amplitude"]) for label, a in record["amplitude_at_probes"].items() if label.startswith(direction + "_")]
                record["fits"][board][direction]["amplitude_at_probe_101_120"] = fit_slope(amps)
                free = record["replays"].get("standing_closed", {}).get("settled_read_nodes", {})
                record["fits"][board][direction]["free_amplitude_101_120"] = fit_slope([(record["read_nodes"][label]["radius"], v["amplitude"]) for label, v in free.items() if label.startswith(direction + "_")])
                record["fits"][board][direction]["free_j_101_120"] = fit_slope([(record["read_nodes"][label]["radius"], v["j_radial"]) for label, v in free.items() if label.startswith(direction + "_")])
                record["fits"][board][direction]["free_content_101_120"] = fit_slope([(record["read_nodes"][label]["radius"], v["content"]) for label, v in free.items() if label.startswith(direction + "_")])
        quantities = set()
        for fits in record["fits"][board].values():
            quantities.update(fits)
        for quantity in sorted(quantities):
            a = {}
            for other in ("111", "110"):
                for r in (8, 12):
                    fa, fo = record["fits"][board].get("axis", {}).get(quantity), record["fits"][board].get(other, {}).get(quantity)
                    va, vo = fit_value(fa, r), fit_value(fo, r)
                    a[f"axis_over_{other}_at_{r}"] = va / vo if va and vo else None
            record["anisotropy"][board][quantity] = a
    args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    text = tables(record)
    args.tables.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
