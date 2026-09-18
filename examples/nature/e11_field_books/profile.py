"""The profile of a point source shell by shell: part (b) of experiment E11
(docs/EXPERIMENTS.md), the field's books.

Runs `point_source.json` (one external body radiating its spreading light on the
49^3 open board under the dense mode) in-process and reads, per completed tick,
the world ledger (the light's sourced, current, escaped and absorbed lines, the
current split into content in flight and content in the remainder registers, the
momentum line, the body's momentum) and the total content of every L1 shell; at
the end, per L1 shell (|dx| + |dy| + |dz| = k) and per Euclidean shell (the
rounded distance k) for k = 1 to 22: the number of Nodes, the content in flight
and in the registers, the content per Node, the radial momentum (the sum over
rays of amount x (heading . r) as an integer and amount x (heading . r) / |r| as
a real), the outward flux through the shell and the net momentum at the axis Node
and at a diagonal Node of the shell; then the local log-log slopes between
consecutive shells of the content per Node, the radial momentum per Node and the
flux, no power law assumed; and beside every column the mean field of the split
table (`examples/nature/a5_static/mean_field_gauss.py`, the expectation of the
engine's integers) at the same tick in the same box and at the box's steady state.

How the columns are read. At the end of an interval every ray has walked its
Link and is resident at the Node it reached, so a Node's content in flight is
what arrived there in the last interval, per heading (the mean field's f[j] at
the same instant); the registers hold the shares below one quantum, whole quanta
in total per Node and no momentum. The flux through the surface between the
shells k and k + 1 is read from the same per-heading content as what crossed it
in the last interval: the content that arrived at a Node of shell k + 1 from a
Node of shell k (outward) less the content that arrived at a Node of shell k from
a Node of shell k + 1 (inward); a Link changes the L1 distance by exactly one and
the rounded distance by at most one, so every crossing is between neighbouring
shells. The flux through the surface between the body and shell 1 is the release
less what the sink took in the last interval, read from the ledger. The runner's
`state.json` holds per Node a family's total and its ray count, not the amount
per heading, so this script is a Recorder in the sense of Highlights 3.29: it
reads the engine in-process, the region's Nodes read back as Node state through
the inventory view (the reading the snapshot itself uses), and every per-tick
shell total from the region's arrays, checked against the inventory at the end.

Run:  PYTHONPATH=src python examples/nature/e11_field_books/profile.py [--world point_source.json] [--ticks N] [--record record.json]
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.json_documents import parse_json_document
from event_universe.runner import source_fingerprint

HERE = Path(__file__).resolve().parent
MEAN_FIELD = HERE.parent / "a5_static" / "mean_field_gauss.py"
PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
HEADINGS = np.array(PORTS, dtype=np.int64)
KMAX = 22
WINDOW = 32
STEADY_TOLERANCE = 0.01
FAMILY = "light"


def load_mean_field():
    spec = importlib.util.spec_from_file_location("a5_static_mean_field_gauss", MEAN_FIELD)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# ----------------------------------------------------------------- geometry


def offsets(shape, centre):
    """d[axis, x, y, z] = the coordinate less the centre's, three integer arrays."""
    grid = np.indices(tuple(int(n) for n in shape), dtype=np.int64)
    return grid - np.array(centre, dtype=np.int64)[:, None, None, None]


def l1_level(d):
    return np.abs(d).sum(axis=0)


def euclid_level(d):
    return np.rint(np.sqrt((d * d).sum(axis=0))).astype(np.int64)


def radius_of(d):
    return np.sqrt((d * d).sum(axis=0).astype(float))


def shell_counts(level, kmax=KMAX):
    """The number of Nodes of every shell k = 0 .. kmax under a level function."""
    return [int((level == k).sum()) for k in range(kmax + 1)]


def shell_index(level, kmax=KMAX):
    """The level clipped to kmax + 1 for a bincount over kmax + 2 bins."""
    return np.minimum(level, kmax + 1).ravel()


def diagonal_node(kind, k):
    """A Node of shell k off the axes: on the (1, 1, 0) diagonal, (ceil(k/2),
    floor(k/2), 0) for the L1 shell and (m, m, 0) with round(m sqrt 2) = k for the
    Euclidean shell, or (m, m, m) with round(m sqrt 3) = k when no (m, m, 0) Node
    lies on that shell (k = 2: (1, 1, 1)); (k, 0, 0) when neither does."""
    if kind == "l1":
        return ((k + 1) // 2, k // 2, 0)
    for stretch, node in ((math.sqrt(2), lambda m: (m, m, 0)), (math.sqrt(3), lambda m: (m, m, m))):
        for m in (int(k / stretch), int(k / stretch) + 1):
            if m > 0 and round(m * stretch) == k:
                return node(m)
    return (k, 0, 0)


# ------------------------------------------------------------- the reading


def family_index(initial, name=FAMILY):
    names = [field.name for field in initial.fields]
    return [field.field for field in initial.spatial_fields].index(names.index(name))


def port_of_heading_index(definition):
    return [PORTS.index(tuple(heading)) for heading in definition.headings]


def read_inventory(world, name=FAMILY):
    """The family's content per Node and heading (amounts[port, x, y, z], the
    outbound rays resident at every Node, the dense region's read back as Node
    state) and the whole quanta its remainder registers hold per Node, from the
    inventory view; content still on a Link is placed at the Node it walks to."""
    initial = world.initial
    index = family_index(initial, name)
    definition = initial.spatial_fields[index]
    ports = port_of_heading_index(definition)
    total = sum(definition.spread) if definition.spread else 1
    shape = tuple(int(n) for n in initial.shape)
    amounts = np.zeros((6, *shape), dtype=np.int64)
    registers = np.zeros(shape, dtype=np.int64)
    view = world.inventory_view()
    for node in view.nodes:
        if node.rays:
            for ray in node.rays[index]:
                if ray.outbound:
                    amounts[(ports[ray.heading], *node.position)] += ray.amount
        if node.remainders and node.remainders[index]:
            registers[node.position] += sum(node.remainders[index]) // total
    for packet in view.packets:
        if not packet.rays:
            continue
        heading = PORTS[packet.port]
        target = tuple(int(c + h) for c, h in zip(packet.origin, heading, strict=True))
        if all(0 <= t < n for t, n in zip(target, shape, strict=True)):
            for ray in packet.rays[index]:
                if ray.outbound:
                    amounts[(ports[ray.heading], *target)] += ray.amount
    return amounts, registers


def read_arrays(world, name=FAMILY):
    """The same reading from the dense region's arrays and the engine's own
    Nodes, cheap enough for every tick; None when the world has no region."""
    spatial = world._spatial
    if spatial is None or spatial.dense is None:
        return None
    initial = world.initial
    index = family_index(initial, name)
    definition = initial.spatial_fields[index]
    ports = port_of_heading_index(definition)
    family = spatial.dense.families[index]
    amounts = np.transpose(
        family.arr_amt.sum(axis=(3, 5)) + family.fly_amt.sum(axis=(3, 5)), (3, 0, 1, 2)
    )
    amounts = np.ascontiguousarray(amounts)
    registers = family.reg.sum(axis=(3, 4)) // family.total
    for position, rays in family.overflow.items():
        for ray in rays:
            amounts[(ports[ray.heading], *position)] += ray.amount
    for position, node in spatial.nodes.items():
        if node.rays:
            for ray in node.rays[index]:
                if ray.outbound:
                    amounts[(ports[ray.heading], *position)] += ray.amount
        if node.remainders and node.remainders[index]:
            registers[position] += sum(node.remainders[index]) // family.total
    return amounts, registers


# ------------------------------------------------------------- the profile


def shell_profile(amounts, registers, d, kind, kmax=KMAX):
    """Per shell k = 1 .. kmax under the level function `kind` ("l1" or
    "euclid"): the rows described in the module docstring. `amounts` is
    (6, X, Y, Z), integer for the engine and float for the mean field."""
    level = l1_level(d) if kind == "l1" else euclid_level(d)
    radius = radius_of(d)
    density = amounts.sum(axis=0)
    dots = HEADINGS @ d.reshape(3, -1)  # (6, N): heading . r_vec at every Node
    dots = dots.reshape(6, *d.shape[1:])
    radial_int = (amounts * dots).sum(axis=0)
    safe = np.where(radius > 0, radius, 1.0)
    radial_real = np.where(radius > 0, radial_int / safe, 0.0)
    # The level of the Node a ray came from, P - h_j, per heading.
    origin = []
    for j in range(6):
        back = d - HEADINGS[j][:, None, None, None]
        origin.append(l1_level(back) if kind == "l1" else euclid_level(back))
    bins = kmax + 2
    idx = shell_index(level, kmax)
    counts = np.bincount(idx, minlength=bins)
    flight = np.bincount(idx, weights=density.ravel().astype(float), minlength=bins)
    held = np.bincount(idx, weights=registers.ravel().astype(float), minlength=bins)
    dot_sum = np.bincount(idx, weights=radial_int.ravel().astype(float), minlength=bins)
    real_sum = np.bincount(idx, weights=radial_real.ravel(), minlength=bins)
    radius_sum = np.bincount(idx, weights=radius.ravel(), minlength=bins)
    outward = np.zeros(bins)
    inward = np.zeros(bins)
    for j in range(6):
        weights = amounts[j].ravel().astype(float)
        origin_idx = shell_index(origin[j], kmax)
        # Outward across level k: from k to k + 1; inward: from k + 1 to k.
        out_mask = idx == origin_idx + 1
        in_mask = idx + 1 == origin_idx
        outward += np.bincount(origin_idx[out_mask], weights=weights[out_mask], minlength=bins)
        inward += np.bincount(idx[in_mask], weights=weights[in_mask], minlength=bins)
    centre = tuple(int(-d[axis].min()) for axis in range(3))
    rows = []
    integer = np.issubdtype(amounts.dtype, np.integer)
    for k in range(1, kmax + 1):
        n = int(counts[k])
        axis_node = (k, 0, 0)
        diag = diagonal_node(kind, k)
        row = {
            "k": k,
            "nodes": n,
            "mean_radius": float(radius_sum[k] / n) if n else None,
            "flight": int(flight[k]) if integer else float(flight[k]),
            "registers": int(held[k]) if integer else float(held[k]),
            "total": (int(flight[k]) + int(held[k])) if integer else float(flight[k] + held[k]),
            "per_node": float((flight[k] + held[k]) / n) if n else None,
            "flight_per_node": float(flight[k] / n) if n else None,
            "radial_dot": int(dot_sum[k]) if integer else float(dot_sum[k]),
            "radial": float(real_sum[k]),
            "radial_per_node": float(real_sum[k] / n) if n else None,
            "flux_out": int(outward[k]) if integer else float(outward[k]),
            "flux_in": int(inward[k]) if integer else float(inward[k]),
            "flux": (int(outward[k]) - int(inward[k])) if integer else float(outward[k] - inward[k]),
        }
        for label, node in (("axis", axis_node), ("diagonal", diag)):
            position = tuple(c + o for c, o in zip(centre, node, strict=True))
            inside = all(0 <= p < s for p, s in zip(position, d.shape[1:], strict=True))
            if inside and int(level[position]) == k:
                vector = [
                    (int(v) if integer else float(v))
                    for v in (amounts[(slice(None), *position)][:, None] * HEADINGS).sum(axis=0)
                ]
                row[label] = {
                    "node": list(node),
                    "momentum": vector,
                    "radial": float(radial_real[position]),
                    "content": (int(density[position]) if integer else float(density[position])),
                    "registers": int(registers[position]),
                }
            else:
                row[label] = {"node": list(node), "momentum": None, "radial": None, "content": None}
        rows.append(row)
    return rows


def local_slopes(rows, key, sub=None):
    """The log-log slope between consecutive shells of a positive column:
    ln(v(k+1) / v(k)) / ln((k+1) / k); None where either value is not positive."""
    out = []
    for a, b in zip(rows, rows[1:], strict=False):
        va = a[key] if sub is None else (a[key] or {}).get(sub)
        vb = b[key] if sub is None else (b[key] or {}).get(sub)
        if va is None or vb is None or va <= 0 or vb <= 0:
            out.append({"from": a["k"], "to": b["k"], "slope": None})
        else:
            out.append(
                {"from": a["k"], "to": b["k"], "slope": math.log(vb / va) / math.log(b["k"] / a["k"])}
            )
    return out


def fit_slope(rows, key, ks):
    """Least-squares log-log slope over the shells `ks` (the fit of analyze.py)."""
    points = [(r["k"], r[key]) for r in rows if r["k"] in ks and r[key] is not None and r[key] > 0]
    if len(points) < 2:
        return None
    xs = [math.log(k) for k, _ in points]
    ys = [math.log(v) for _, v in points]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return sxy / sxx if sxx else None


# ---------------------------------------------------------- the mean field


def unfold(octant):
    """The full box from an octant (6, n, n, n) whose index-0 planes are the
    mirror planes through the source: a heading's Port is swapped on every
    reflected axis."""
    n = octant.shape[1]
    size = 2 * n - 1
    full = np.zeros((6, size, size, size))
    c = n - 1
    for sx in (1, -1):
        for sy in (1, -1):
            for sz in (1, -1):
                block = octant
                if sx < 0:
                    block = block[[1, 0, 2, 3, 4, 5]][:, ::-1, :, :]
                if sy < 0:
                    block = block[[0, 1, 3, 2, 4, 5]][:, :, ::-1, :]
                if sz < 0:
                    block = block[[0, 1, 2, 3, 5, 4]][:, :, :, ::-1]
                xs = slice(0, n) if sx < 0 else slice(c, size)
                ys = slice(0, n) if sy < 0 else slice(c, size)
                zs = slice(0, n) if sz < 0 else slice(c, size)
                full[:, xs, ys, zs] = block
    return full


def mean_field(shape, centre, release, ticks, tol=1e-10):
    """The mean field in the same box: the transient after `ticks` intervals from
    the empty board and the box's steady state (a computation, not an engine
    run), as per-heading arrivals after the sink at the source took its share,
    the same instant the engine is read at; the effective source S and the
    absorbed per interval at steady state."""
    mf = load_mean_field()
    half = min(int(centre[a]) for a in range(3))
    if any(int(shape[a]) != 2 * int(centre[a]) + 1 for a in range(3)) or any(
        int(centre[a]) != half for a in range(3)
    ):
        raise ValueError("the mean field's octant needs the source at the centre of a cube")
    board = mf.Board(
        (half + 1,) * 3, (True,) * 3, (0, 0, 0), [(0, 0, 0)], release=release, table=mf.SPREAD
    )
    f = board.empty()
    absorbed_series = []
    for _ in range(ticks):
        arrivals = board.arrivals(f, board._out)
        absorbed_series.append(float(arrivals[(slice(None), 0, 0, 0)].sum()))
        board.absorb(arrivals)
        f[...] = arrivals
    transient = f.copy()
    started = time.time()
    steady, iterations = board.steady_state(tol)
    steady_arrivals = board.arrivals(steady)
    returned = float(steady_arrivals[(slice(None), 0, 0, 0)].sum())
    return {
        "transient": unfold(transient),
        "steady": unfold(steady),
        "absorbed_per_tick": absorbed_series,
        "steady_returned": returned,
        "effective_source": 6 * float(release) - returned,
        "iterations": iterations,
        "steady_seconds": time.time() - started,
    }


# ------------------------------------------------------------------ the run


def ledger_row(world, tick, registers_total):
    audit = world.audit()
    light = audit["fields"][FAMILY]
    momentum = audit["fields"].get("momentum")
    current = int(light["current"][0])
    return {
        "tick": tick,
        "sourced": int(light["sourced"][0]),
        "current": current,
        "flight": current - int(registers_total),
        "registers": int(registers_total),
        "escaped": int(light["escaped"][0]),
        "absorbed": int(light["absorbed"][0]),
        "momentum_sourced": [int(v) for v in momentum["sourced"]] if momentum else None,
        "momentum_current": [int(v) for v in momentum["current"]] if momentum else None,
        "momentum_escaped": [int(v) for v in momentum["escaped"]] if momentum else None,
        "momentum_absorbed": [int(v) for v in momentum["absorbed"]] if momentum else None,
        "body_momentum": [int(v) for v in audit["bodies"]["momentum"]],
        "balanced": bool(audit["balanced"]),
    }


def run_world(document, *, ticks=None, kmax=KMAX, window=WINDOW, log=print, with_mean_field=True):
    """Run the world in-process and read it: the record of part (b)."""
    initial = parse_initial_state(document)
    count = int(document["ticks"]) if ticks is None else int(ticks)
    shape = tuple(int(n) for n in initial.shape)
    (body,) = document["external_bodies"]
    centre = tuple(int(c) for c in body["position"])
    d = offsets(shape, centre)
    l1 = l1_level(d)
    l1_idx = shell_index(l1, kmax)
    counts_l1 = shell_counts(l1, kmax)
    counts_euclid = shell_counts(euclid_level(d), kmax)
    ledger = []
    shell_totals = []  # per tick: the L1 shells' totals k = 0 .. kmax
    stopped_by = "ticks"
    started = time.perf_counter()
    with Simulation(initial) as world:
        for tick in range(1, count + 1):
            world.step()
            arrays = read_arrays(world)
            if arrays is None:
                arrays = read_inventory(world)
            amounts, registers = arrays
            totals = np.bincount(
                l1_idx,
                weights=(amounts.sum(axis=0) + registers).ravel().astype(float),
                minlength=kmax + 2,
            )
            shell_totals.append([int(v) for v in totals[: kmax + 1]])
            ledger.append(ledger_row(world, tick, int(registers.sum())))
            if log is not None and (tick % 8 == 0 or tick <= 4 or tick == count):
                row = ledger[-1]
                log(
                    f"tick {tick:4d}  sourced {row['sourced']:9d}  flight {row['flight']:8d}"
                    f"  registers {row['registers']:7d}  escaped {row['escaped']:8d}"
                    f"  absorbed {row['absorbed']:7d}  body {row['body_momentum']}"
                    f"  balanced {row['balanced']}  {time.perf_counter() - started:5.0f}s"
                )
            if tick >= 2 * window and steady_shells(shell_totals, tick, window, kmax) == list(
                range(1, kmax + 1)
            ):
                stopped_by = "steady"
                break
        elapsed = time.perf_counter() - started
        final_tick = ledger[-1]["tick"]
        amounts, registers = read_inventory(world)
        check = read_arrays(world)
        arrays_agree = (
            None
            if check is None
            else bool(np.array_equal(check[0], amounts) and np.array_equal(check[1], registers))
        )
        final_audit = world.audit()
    profiles = {}
    for kind in ("l1", "euclid"):
        profiles[kind] = {"engine": shell_profile(amounts, registers, d, kind, kmax)}
    mean = None
    if with_mean_field:
        release = (
            int(body["amount"])
            * int(document_release(document)[0])
            // int(document_release(document)[1])
        )
        mean = mean_field(shape, centre, release, final_tick)
        zero = np.zeros(shape, dtype=np.int64)
        for kind in ("l1", "euclid"):
            profiles[kind]["mean_field_tick"] = shell_profile(mean["transient"], zero, d, kind, kmax)
            profiles[kind]["mean_field_steady"] = shell_profile(mean["steady"], zero, d, kind, kmax)
    for kind in ("l1", "euclid"):
        slopes = {}
        for label, rows in profiles[kind].items():
            slopes[label] = {
                "per_node": local_slopes(rows, "per_node"),
                "radial_per_node": local_slopes(rows, "radial_per_node"),
                "flux": local_slopes(rows, "flux"),
            }
        profiles[kind]["slopes"] = slopes
    last = ledger[-1]
    before = ledger[-2] if len(ledger) > 1 else None
    flux0 = (
        None
        if before is None
        else (last["sourced"] - before["sourced"]) - (last["absorbed"] - before["absorbed"])
    )
    return {
        "model": document["model_id"],
        "shape": list(shape),
        "centre": list(centre),
        "release_per_heading": int(body["amount"])
        * int(document_release(document)[0])
        // int(document_release(document)[1]),
        "ticks": final_tick,
        "requested_ticks": count,
        "stopped_by": stopped_by,
        "window": window,
        "steady_tolerance": STEADY_TOLERANCE,
        "steady_shells": steady_shells(shell_totals, final_tick, window, kmax),
        "shell_change_over_window": shell_change(shell_totals, final_tick, window, kmax),
        "kmax": kmax,
        "counts": {"l1": counts_l1, "euclid": counts_euclid},
        "source_sha256": source_fingerprint(),
        "elapsed_seconds": elapsed,
        "dense_field": bool(initial.dense_field),
        "arrays_agree_with_inventory": arrays_agree,
        "balanced_every_tick": all(row["balanced"] for row in ledger),
        "final_balanced": bool(final_audit["balanced"]),
        "shell_sum_equals_current": int(amounts.sum() + registers.sum()) == last["current"],
        "flux_0": flux0,
        "ledger": ledger,
        "shell_totals_l1": shell_totals,
        "profiles": profiles,
        "mean_field": None
        if mean is None
        else {
            "effective_source": mean["effective_source"],
            "steady_returned": mean["steady_returned"],
            "absorbed_at_tick": mean["absorbed_per_tick"][-1],
            "iterations": mean["iterations"],
            "steady_seconds": mean["steady_seconds"],
        },
    }


def document_release(document):
    for field in document["spatial_fields"]:
        if field.get("field_of"):
            return field["release"]
    raise ValueError("no released field in the world")


def steady_shells(shell_totals, tick, window, kmax):
    """The shells whose total changed by less than the tolerance over the last
    `window` ticks (relative to the last total); [] before two windows."""
    if tick < window + 1 or len(shell_totals) <= window:
        return []
    now, then = shell_totals[-1], shell_totals[-1 - window]
    return [
        k for k in range(1, kmax + 1) if now[k] > 0 and abs(now[k] - then[k]) < STEADY_TOLERANCE * now[k]
    ]


def shell_change(shell_totals, tick, window, kmax):
    if len(shell_totals) <= window:
        return None
    now, then = shell_totals[-1], shell_totals[-1 - window]
    return [((now[k] - then[k]) / now[k] if now[k] else None) for k in range(kmax + 1)]


# ------------------------------------------------------------- the tables


def fmt(value, digits=1):
    if value is None:
        return "-"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def print_tables(record, out=print):
    out(
        f"== {record['model']}  shape {record['shape']}  centre {record['centre']}  release"
        f" {record['release_per_heading']} per heading per interval  ticks {record['ticks']}"
        f" (stopped by {record['stopped_by']})  dense {record['dense_field']}  {record['elapsed_seconds']:.0f} s"
    )
    out(f"   source {record['source_sha256']}")
    out(
        f"   balanced every tick {record['balanced_every_tick']}; arrays agree with the inventory"
        f" {record['arrays_agree_with_inventory']}; the shells' sum equals the ledger's current"
        f" {record['shell_sum_equals_current']}; shells steady to {100 * record['steady_tolerance']:.0f} %"
        f" over the last {record['window']} ticks: {record['steady_shells']}"
    )
    mean = record["mean_field"]
    if mean:
        out(
            f"   mean field: effective source S = {mean['effective_source']:.1f} per interval at steady"
            f" state ({mean['steady_returned']:.1f} returns to the sink), BiCGSTAB {mean['iterations']}"
            f" iterations {mean['steady_seconds']:.0f} s; sink at tick {record['ticks']}: {mean['absorbed_at_tick']:.1f}"
        )
    last = record["ledger"][-1]
    out(
        f"   ledger at tick {last['tick']}: sourced {last['sourced']} = flight {last['flight']} +"
        f" registers {last['registers']} + escaped {last['escaped']} + absorbed {last['absorbed']};"
        f" flux through the surface about the body in the last interval {record['flux_0']}"
    )
    out(
        "\n   ledger per tick (every 16 ticks): sourced, in flight, registers, escaped, absorbed, body momentum"
    )
    for row in record["ledger"]:
        if row["tick"] % 16 == 0 or row["tick"] in (1, 2, 4, 8) or row is record["ledger"][-1]:
            out(
                f"   {row['tick']:4d} {row['sourced']:9d} {row['flight']:8d} {row['registers']:7d}"
                f" {row['escaped']:8d} {row['absorbed']:7d} {row['body_momentum']} {row['balanced']}"
            )
    for kind, title in (
        ("l1", "L1 shells |dx|+|dy|+|dz| = k"),
        ("euclid", "Euclidean shells round(|r|) = k"),
    ):
        prof = record["profiles"][kind]
        engine = prof["engine"]
        tick_rows = prof.get("mean_field_tick")
        steady_rows = prof.get("mean_field_steady")
        change = record["shell_change_over_window"]
        out(
            f"\n== {title}: content (engine at tick {record['ticks']}; the mean field at the same tick and at the box's steady state)"
        )
        out(
            f"   {'k':>2} {'Nodes':>5} {'<r>':>5} {'flight':>8} {'regs':>6} {'per Node':>9}"
            f" {'mf tick':>9} {'mf steady':>9} {'d32 %':>6}"
        )
        for i, row in enumerate(engine):
            mt = tick_rows[i]["per_node"] if tick_rows else None
            ms = steady_rows[i]["per_node"] if steady_rows else None
            c = change[row["k"]] if change and kind == "l1" else None
            out(
                f"   {row['k']:>2} {row['nodes']:>5} {fmt(row['mean_radius'], 2):>5} {row['flight']:>8} {row['registers']:>6}"
                f" {fmt(row['per_node']):>9} {fmt(mt):>9} {fmt(ms):>9} {fmt(None if c is None else 100 * c):>6}"
            )
        out(f"\n== {title}: radial momentum and flux")
        out(
            f"   {'k':>2} {'dot':>9} {'radial':>9} {'per Node':>8} {'mf tick':>8} {'mf stdy':>8}"
            f" {'flux':>8} {'mf tick':>8} {'mf stdy':>8} {'axis':>8} {'diag':>8} {'diag Node':>10}"
        )
        for i, row in enumerate(engine):
            mt = tick_rows[i] if tick_rows else None
            ms = steady_rows[i] if steady_rows else None
            out(
                f"   {row['k']:>2} {row['radial_dot']:>9} {fmt(row['radial']):>9} {fmt(row['radial_per_node']):>8}"
                f" {fmt(mt['radial_per_node'] if mt else None):>8} {fmt(ms['radial_per_node'] if ms else None):>8}"
                f" {row['flux']:>8} {fmt(mt['flux'] if mt else None):>8} {fmt(ms['flux'] if ms else None):>8}"
                f" {fmt(row['axis']['radial']):>8} {fmt(row['diagonal']['radial']):>8} {str(row['diagonal']['node']):>10}"
            )
        out(
            f"\n== {title}: local log-log slopes between consecutive shells (engine | mf tick | mf steady)"
        )
        out(f"   {'k':>5} {'per Node':>24} {'radial per Node':>24} {'flux':>24}")
        slopes = prof["slopes"]
        for i, s in enumerate(slopes["engine"]["per_node"]):
            cell = []
            for key in ("per_node", "radial_per_node", "flux"):
                vals = [
                    slopes[label][key][i]["slope"]
                    for label in ("engine", "mean_field_tick", "mean_field_steady")
                    if label in slopes
                ]
                cell.append(" ".join(f"{fmt(v, 2):>7}" for v in vals))
            out(f"   {s['from']:>2}-{s['to']:<2} {cell[0]:>24} {cell[1]:>24} {cell[2]:>24}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--world", type=Path, default=HERE / "point_source.json")
    parser.add_argument("--ticks", type=int)
    parser.add_argument("--record", type=Path, default=HERE / "record.json")
    parser.add_argument("--no-mean-field", action="store_true")
    args = parser.parse_args(argv)
    source = args.world.read_bytes()
    document = parse_json_document(source)
    record = run_world(document, ticks=args.ticks, with_mean_field=not args.no_mean_field)
    record["world"] = args.world.name
    record["initialization_sha256"] = hashlib.sha256(source).hexdigest()
    print_tables(record)
    if args.record:
        existing = {}
        if args.record.exists():
            existing = json.loads(args.record.read_text(encoding="utf-8"))
        existing["profile"] = record
        args.record.write_text(json.dumps(existing, indent=1) + "\n", encoding="utf-8")
        print(f"\nwrote {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
