"""Read the records of experiment A5 (docs/EXPERIMENTS.md) and evaluate its
criterion clause by clause: the momentum transfer dp(b) of each ray from the
momentum register, the log-log least-squares exponent of |dp(b)| over b with
its standard error, the momentum sum per tick, the first return at each
releaser, the sign of the deflection, the neutral control and the self-meeting
count. A Renderer of records in the sense of Highlights 3.29: it reads only
what the runner wrote (``run.json``, ``events.jsonl``, ``initialization.json``)
and never the engine.

Run:  python examples/nature/a5_coulomb/analyze.py RUN [RUN ...] [--out summary.json] [--record record.json]
where RUN is a run directory (``run.json`` beside ``events.jsonl``) of one
world of ``make_worlds.py``. The per-tick table of every run and the clause
table are printed; ``--out`` writes the full summary and ``--record`` the small
committed record the test reads.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

PORT_HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
BAND = (-1.15, -0.85)


def heading_of_arrival(port):
    """A packet received through Port p travels on the heading opposite to p."""
    return PORT_HEADINGS[port ^ 1]


def add(u, v):
    return tuple(a + b for a, b in zip(u, v, strict=True))


def sub(u, v):
    return tuple(a - b for a, b in zip(u, v, strict=True))


def scale(v, k):
    return tuple(k * a for a in v)


def load(run):
    directory = Path(run)
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    return directory, metadata, world


def geometry(world):
    """The matter families, their lamps, the fields they release and b."""
    matter = {}
    for seed, emission in zip(world["seeds"], world["emissions"], strict=True):
        matter[emission["field"]] = {
            "start": tuple(seed["position"]),
            "heading": tuple(emission["heading"]),
            "amount": emission["amount"],
        }
    fields = {
        entry["field_of"]: entry["field"] for entry in world["spatial_fields"] if "field_of" in entry
    }
    charges = {entry["field"]: entry.get("charge", 0) for entry in world["spatial_fields"]}
    names = list(matter)
    ya, yb = matter[names[0]]["start"][1], matter[names[1]]["start"][1]
    b = abs(yb - ya)
    xa, xb = matter[names[0]]["start"][0], matter[names[1]]["start"][0]
    closest = (xa + xb) // 2 - min(xa, xb)
    spread = any("spread" in entry for entry in world["spatial_fields"])
    return {
        "matter": matter,
        "fields": fields,
        "charges": charges,
        "b": b,
        "closest_tick": closest,
        "read_off_tick": closest + 3 * b,
        "spread": spread,
        "coupled": bool(world.get("ray_interactions")),
    }


def analyze(run):
    directory, metadata, world = load(run)
    geo = geometry(world)
    matter, fields = geo["matter"], geo["fields"]
    own = {fields[name]: name for name in matter}
    ticks = int(metadata["completed_ticks"])
    pushes = []
    positions = {name: {} for name in matter}
    # Per tick: the field momentum of what arrived (amount x heading over every
    # received packet of a field family), the arrivals of each field family, and
    # the Nodes where a matter ray arrived together with its own field.
    field_momentum = {t: (0, 0, 0) for t in range(ticks + 1)}
    field_packets = {t: 0 for t in range(ticks + 1)}
    self_meetings = []
    with (directory / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            event = json.loads(line)
            kind = event.get("event")
            if kind == "ray_push":
                pushes.append(event)
            elif kind == "spatial_received":
                tick = event["tick"]
                node = tuple(event["position"])
                here = {}
                for port, packet in enumerate(event["received_fields"]):
                    for family, values in packet.items():
                        amount = values[0] if values else 0
                        if not amount:
                            continue
                        here[family] = here.get(family, 0) + amount
                        if family in own:
                            field_momentum[tick] = add(
                                field_momentum[tick], scale(heading_of_arrival(port), amount)
                            )
                            field_packets[tick] += 1
                for name in matter:
                    if here.get(name):
                        positions[name][tick] = node
                        if here.get(fields[name]):
                            self_meetings.append(
                                {
                                    "tick": tick,
                                    "position": list(node),
                                    "family": name,
                                    "own": here[fields[name]],
                                }
                            )
    # The register of each matter ray after tick T: amount x heading plus every
    # push whose cycle tick is below T (a push at tick t is applied in the step
    # that delivers tick t + 1).
    registers = {}
    for name, info in matter.items():
        initial = scale(info["heading"], info["amount"])
        per_tick = {}
        for t in range(ticks + 1):
            register = initial
            for push in pushes:
                if push["family"] == name and push["tick"] < t:
                    register = tuple(push["after"])
            per_tick[t] = register
        registers[name] = {"initial": initial, "per_tick": per_tick}
    audit = {entry["tick"]: entry for entry in metadata["audit"]}
    names = list(matter)
    rows = []
    for t in range(1, ticks + 1):
        line = audit[t]["fields"]["momentum"]
        matter_sum = (0, 0, 0)
        for name in names:
            matter_sum = add(matter_sum, registers[name]["per_tick"][t])
        rays_sum = add(matter_sum, field_momentum[t])
        light_in_flight = sum(audit[t]["fields"][fields[name]]["current"][0] for name in names)
        rows.append(
            {
                "tick": t,
                "registers": [list(registers[name]["per_tick"][t]) for name in names],
                "field_momentum": list(field_momentum[t]),
                "field_packets": field_packets[t],
                "field_amount": light_in_flight,
                "rays_sum": list(rays_sum),
                "ledger_current": list(line["current"]),
                "ledger_sourced": list(line["sourced"]),
                "ledger_escaped": list(line["escaped"]),
                "balanced": audit[t]["balanced"],
                "pushes": sum(1 for p in pushes if p["tick"] == t - 1),
            }
        )
    first_push = min((p["tick"] for p in pushes), default=None)
    first_push_by = {
        name: min((p["tick"] for p in pushes if p["family"] == name), default=None) for name in names
    }
    first_return = {
        name: min((m["tick"] for m in self_meetings if m["family"] == name), default=None)
        for name in names
    }
    read_off = min(geo["read_off_tick"], ticks)
    dp = {
        name: list(sub(registers[name]["per_tick"][read_off], registers[name]["initial"]))
        for name in names
    }
    dp_final = {
        name: list(sub(registers[name]["per_tick"][ticks], registers[name]["initial"])) for name in names
    }
    straight = {
        name: all(
            positions[name][t][1] == matter[name]["start"][1]
            and positions[name][t][2] == matter[name]["start"][2]
            for t in positions[name]
        )
        for name in names
    }
    return {
        "run": str(directory),
        "model": metadata["model"],
        "status": metadata["status"],
        "error": metadata.get("error"),
        "source_sha256": metadata["source_sha256"],
        "initialization_sha256": metadata["initialization_sha256"],
        "elapsed_seconds": metadata["elapsed_seconds"],
        "ticks": ticks,
        "b": geo["b"],
        "spread": geo["spread"],
        "coupled": geo["coupled"],
        "charges": {name: geo["charges"][name] for name in names},
        "matter": names,
        "fields": {name: fields[name] for name in names},
        "closest_tick": geo["closest_tick"],
        "read_off_tick": geo["read_off_tick"],
        "read_off_used": read_off,
        "dp": dp,
        "dp_final": dp_final,
        "pushes": len(pushes),
        "pushes_by": {name: sum(1 for p in pushes if p["family"] == name) for name in names},
        "first_push": first_push,
        "first_push_by": first_push_by,
        "first_return": first_return,
        "self_meetings": len(self_meetings),
        "self_meeting_list": self_meetings[:20],
        "straight": straight,
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "rays_sum_max_abs": max((max(abs(c) for c in row["rays_sum"]) for row in rows), default=0),
        "ledger_sourced_final": rows[-1]["ledger_sourced"] if rows else None,
        "final_totals": metadata["final_totals"],
        "escaped_totals": metadata["escaped_totals"],
        "rows": rows,
        "push_list": [
            {
                "tick": p["tick"],
                "position": p["position"],
                "family": p["family"],
                "before": p["before"],
                "after": p["after"],
                "field": p["field"],
                "field_amount": p["field_amount"],
                "field_heading": p["field_heading"],
            }
            for p in pushes
        ],
    }


def fit(points):
    """Least-squares slope of ln|dp| over ln b with its standard error; None when
    a |dp| is 0 (no logarithm) or fewer than three points remain."""
    usable = [(b, v) for b, v in points if v > 0]
    n = len(usable)
    if n < 3 or n != len(points):
        return {"exponent": None, "standard_error": None, "points": n, "zeros": len(points) - n}
    xs = [math.log(b) for b, _ in usable]
    ys = [math.log(v) for _, v in usable]
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    slope = sxy / sxx
    intercept = my - slope * mx
    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys, strict=True))
    se = math.sqrt(residual / (n - 2) / sxx) if n > 2 else None
    return {"exponent": slope, "standard_error": se, "intercept": intercept, "points": n, "zeros": 0}


def transverse(result, name):
    """The component of dp along the impact axis (y), the transverse transfer."""
    return result["dp"][name][1]


def clauses(results):
    """The criterion of A5, each clause with its verdict and its numbers."""
    by_case = {}
    for r in results:
        case = r["model"].split("-")[2]
        by_case.setdefault(case, []).append(r)
    series = {
        case: sorted(rs, key=lambda r: r["b"]) for case, rs in by_case.items() if case in ("ee", "ep")
    }
    main = [r for case in ("ee", "ep") for r in series.get(case, []) if r["spread"]]
    table = []
    # 1. The momentum sum over matter rays, field rays and returns equals the
    # initial sum at every tick exactly (and the ledger identity).
    sums = {r["model"]: r["rays_sum_max_abs"] for r in results}
    ledger = {r["model"]: r["conserved_at_every_completed_tick"] for r in results}
    table.append(
        {
            "clause": "momentum sum exact at every tick",
            "pass": all(v == 0 for v in sums.values()) and all(ledger.values()),
            "numbers": {"max_abs_rays_sum": sums, "ledger_identity": ledger},
        }
    )
    # 2. After all returns, dp equal and opposite exactly; before that, the
    # imbalance equals the field momentum in flight.
    opposite = {}
    for r in main:
        a, b = r["matter"]
        total = [x + y for x, y in zip(r["dp_final"][a], r["dp_final"][b], strict=True)]
        imbalance_matches_field = all(
            [x + y for x, y in zip(row["registers"][0], row["registers"][1], strict=True)]
            == row["field_momentum"]
            for row in r["rows"]
        )
        opposite[r["model"]] = {
            "dp_a": r["dp_final"][a],
            "dp_b": r["dp_final"][b],
            "sum": total,
            "imbalance_equals_field_momentum_every_tick": imbalance_matches_field,
        }
    table.append(
        {
            "clause": "dp equal and opposite after all returns; imbalance = field momentum in flight before",
            "pass": all(v["sum"] == [0, 0, 0] for v in opposite.values())
            and all(v["imbalance_equals_field_momentum_every_tick"] for v in opposite.values()),
            "numbers": opposite,
        }
    )
    # 3. The first recoil of each releaser arrives at exactly twice the transit.
    returns = {
        r["model"]: {
            "first_push": r["first_push_by"],
            "first_return": r["first_return"],
            "transit_of_axis_ray": r["b"],
            "expected_return_tick_if_at_rest": {
                name: (r["first_push_by"][name] + r["b"])
                if r["first_push_by"][name] is not None
                else None
                for name in r["matter"]
            },
        }
        for r in main
    }
    table.append(
        {
            "clause": "first recoil at each releaser at exactly twice the transit",
            "pass": all(
                v["first_return"][name] is not None
                and v["first_return"][name] == v["expected_return_tick_if_at_rest"][name]
                for v in returns.values()
                for name in v["first_return"]
            ),
            "numbers": returns,
        }
    )
    # 4. The log-log exponent of |dp(b)| over the five b, -1.0 +- 0.15.
    fits = {}
    for case, rs in series.items():
        rs = [r for r in rs if r["spread"]]
        for name_index in (0, 1):
            points = [(r["b"], abs(transverse(r, r["matter"][name_index]))) for r in rs]
            fits[f"{case}:{rs[0]['matter'][name_index] if rs else name_index}"] = {
                "points": points,
                **fit(points),
            }
    table.append(
        {
            "clause": "log-log exponent of |dp(b)| over b is -1.0 +- 0.15",
            "pass": bool(fits)
            and all(
                f["exponent"] is not None and BAND[0] <= f["exponent"] <= BAND[1] for f in fits.values()
            ),
            "numbers": fits,
        }
    )
    # 5. Like charges deflect apart, opposite charges together.
    signs = {}
    for r in main:
        a, b = r["matter"]
        like = r["charges"][a] * r["charges"][b] > 0
        # a is on the lower line (smaller y): apart means dp_y(a) < 0 and dp_y(b) > 0.
        da, db = transverse(r, a), transverse(r, b)
        apart = da < 0 < db
        together = db < 0 < da
        signs[r["model"]] = {"like": like, "dp_y": [da, db], "pass": apart if like else together}
    table.append(
        {
            "clause": "like charges apart, electron-positron together",
            "pass": all(v["pass"] for v in signs.values()),
            "numbers": signs,
        }
    )
    # 6. The neutral control goes straight.
    neutral = {
        r["model"]: {"straight": r["straight"], "pushes": r["pushes"], "dp": r["dp_final"]}
        for r in results
        if not r["coupled"]
    }
    table.append(
        {
            "clause": "neutral control straight",
            "pass": bool(neutral)
            and all(all(v["straight"].values()) and v["pushes"] == 0 for v in neutral.values()),
            "numbers": neutral,
        }
    )
    # 7. No ray meets a field ray of its own event.
    selfs = {r["model"]: r["self_meetings"] for r in results}
    table.append(
        {
            "clause": "no ray meets its own field",
            "pass": all(v == 0 for v in selfs.values()),
            "numbers": selfs,
        }
    )
    return table


def print_run(r):
    print(
        f"== {r['model']}  b={r['b']} ticks={r['ticks']} status={r['status']} spread={r['spread']} "
        f"elapsed={r['elapsed_seconds']:.0f}s"
    )
    print(f"   source {r['source_sha256']}  init {r['initialization_sha256']}")
    a, b = r["matter"]
    print(
        f"   dp at read-off tick {r['read_off_used']}: {a} {r['dp'][a]}  {b} {r['dp'][b]};"
        f" final tick {r['ticks']}: {r['dp_final'][a]} {r['dp_final'][b]}"
    )
    print(
        f"   pushes {r['pushes']} {r['pushes_by']}; first push {r['first_push_by']};"
        f" first return {r['first_return']}; self-meetings {r['self_meetings']}"
    )
    print(
        f"   rays-sum max |component| {r['rays_sum_max_abs']}; ledger {r['conserved_at_every_completed_tick']};"
        f" sourced final {r['ledger_sourced_final']}"
    )
    print("   tick  reg_a            reg_b            field_p        field_amt  pushes")
    for row in r["rows"]:
        if row["pushes"] or row["tick"] in (1, r["read_off_used"], r["ticks"]) or row["tick"] % 8 == 0:
            print(
                f"   {row['tick']:4d}  {str(row['registers'][0]):16s} {str(row['registers'][1]):16s} "
                f"{str(row['field_momentum']):14s} {row['field_amount']:8d}  {row['pushes']}"
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    results = [analyze(run) for run in args.runs]
    for r in results:
        print_run(r)
    table = clauses(results)
    print("\n== Criterion of A5, clause by clause")
    for entry in table:
        print(f"   {'PASS' if entry['pass'] else 'FAIL'}  {entry['clause']}")
        print("         " + json.dumps(entry["numbers"], default=str)[:1200])
    if args.out:
        args.out.write_text(
            json.dumps({"runs": results, "clauses": table}, indent=1) + "\n", encoding="utf-8"
        )
    if args.record:
        record = {
            "runs": [
                {k: r[k] for k in r if k not in ("rows", "push_list", "self_meeting_list", "run")}
                | {"pushes_list": r["push_list"]}
                for r in results
            ],
            "clauses": table,
        }
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
