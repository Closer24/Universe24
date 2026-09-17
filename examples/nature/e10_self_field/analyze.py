"""Read the records of experiment E10 (docs/EXPERIMENTS.md), the ring meets its
own field, and evaluate its criterion per world: the group reading tick by
tick (the record's group reader, the ray viewer's extractor with the
recording), the ring rays on and off the ring, the light met at the corners,
every push with the register before and after, the recoils, the ledger, and
the verdict "closed" or "dispersed at tick t"; then the table content ->
verdict for the coupled worlds beside the controls, and whether a coupled
record is the control's event for event. A Renderer of records in the sense
of Highlights 3.29: it reads only what the runner and the Recorder wrote
(``run.json``, ``events.jsonl``, ``initialization.json``,
``ray-recording.json``) and never the engine.

Run:  python examples/nature/e10_self_field/analyze.py RUN [RUN ...] [--out summary.json] [--record record.json]
where RUN is a run directory of one world of ``make_worlds.py`` (``run.json``
beside ``events.jsonl``; ``ray-recording.json`` written by
``tools/ray_viewer/record_sidecar.py`` for the group reading).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PORT_HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
# The window of the criterion: the last 32 ticks of the run, four periods of
# the ring's clock at rate 1 (period 8).
WINDOW = 32


def tool(name):
    spec = importlib.util.spec_from_file_location(
        "tools.ray_viewer." + name, ROOT / "tools/ray_viewer" / (name + ".py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def heading_of_arrival(port):
    """A packet received through Port p travels on the heading opposite to p."""
    return PORT_HEADINGS[port ^ 1]


def load(run):
    directory = Path(run)
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    return directory, metadata, world


def components(value):
    return [value] if isinstance(value, int) else list(value)


def line(ledger, family):
    entry = ledger["fields"][family]
    return {key: components(entry[key]) for key in ("initial", "sourced", "current", "escaped")}


def geometry(world):
    corners = sorted({tuple(seed["position"]) for seed in world["seeds"]})
    amount = world["emissions"][0]["amount"]
    rules = [rule["name"] for rule in world.get("ray_interactions", [])]
    variant = "control"
    if "electron_field_turn" in rules:
        variant = "corner_first" if rules[0] == "corner" else "turn_first"
    return {
        "corners": corners,
        "amount": amount,
        "content": amount * len(world["seeds"]),
        "rules": rules,
        "variant": variant,
    }


def group_reading(directory, metadata):
    """The record's group reader: the extractor's document (``runs.json``
    beside the record, written by ``tools/ray_viewer/extract.py`` from the
    record and its recording) when it lies there, else the extractor run over
    the record with its recording; None when neither exists."""
    document = directory / "runs.json"
    sidecar = directory / "ray-recording.json"
    if document.exists():
        runs = json.loads(document.read_text(encoding="utf-8"))["runs"]
        (run,) = [
            run for run in runs if run["record"]["source_sha256"] == metadata["source_sha256"]
        ] or runs
    elif sidecar.exists():
        extract = tool("extract")
        run = extract.extract_record(directory, sidecar=sidecar)
    else:
        return None
    return {
        "groups": run["groups"],
        "bound": [row["bound"] for row in run["ticks_data"]],
        "rays": len(run["rays"]),
        "event_kinds": run["event_kinds"],
    }


def analyze(run):
    directory, metadata, world = load(run)
    geo = geometry(world)
    corners = set(geo["corners"])
    content = geo["content"]
    ticks = int(metadata["completed_ticks"])
    events_path = directory / "events.jsonl"
    events_sha256 = hashlib.sha256(events_path.read_bytes()).hexdigest()
    # The physical record's digest: every event line without the host's `cost`
    # (the operation count of a cycle, which counts the rays a meeting reads and
    # so differs between one layer and two even when nothing meets).
    physical = hashlib.sha256()
    pushes = []
    kinds = {}
    on_ring = {t: 0 for t in range(ticks + 1)}
    off_ring = {t: 0 for t in range(ticks + 1)}
    off_ring_first = None
    light_at_corners = {t: {} for t in range(ticks + 1)}
    corner_sources = {t: {} for t in range(ticks + 1)}
    with events_path.open(encoding="utf-8") as stream:
        for text in stream:
            event = json.loads(text)
            kind = event.get("event")
            kinds[kind] = kinds.get(kind, 0) + 1
            physical.update(
                json.dumps(
                    {k: v for k, v in event.items() if k != "cost"},
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode()
            )
            physical.update(b"\n")
            if kind == "ray_push":
                pushes.append(event)
            elif kind == "spatial_received":
                tick = event["tick"]
                node = tuple(event["position"])
                by_port = [0] * 6
                electrons = 0
                for port, packet in enumerate(event["received_fields"]):
                    for family, values in packet.items():
                        amount = values[0] if values else 0
                        if not amount:
                            continue
                        if family == "electron":
                            electrons += amount
                        elif family == "light":
                            by_port[port] += amount
                if electrons:
                    if node in corners:
                        on_ring[tick] += electrons
                    else:
                        off_ring[tick] += electrons
                        if off_ring_first is None or tick < off_ring_first:
                            off_ring_first = tick
                if node in corners and any(by_port):
                    light_at_corners[tick][str(list(node))] = by_port
            elif kind == "spatial_cycle" and tuple(event["position"]) in corners:
                corner_sources[event["tick"]][str(event["position"])] = event["source_delta"]
    reading = group_reading(directory, metadata)
    audit = {entry["tick"]: entry for entry in metadata["audit"]}
    rows = []
    for t in range(1, ticks + 1):
        ledger = audit[t]
        electron = line(ledger, "electron")
        light = line(ledger, "light")
        momentum = line(ledger, "momentum")
        bound = reading["bound"][t] if reading is not None and t < len(reading["bound"]) else None
        rows.append(
            {
                "tick": t,
                "on_ring": on_ring[t],
                "off_ring": off_ring[t],
                "light_at_corners": sum(sum(v) for v in light_at_corners[t].values()),
                "light_by_corner": light_at_corners[t],
                "pushes": sum(1 for p in pushes if p["tick"] == t),
                "bound": bound,
                "electron_current": electron["current"][0],
                "electron_escaped": electron["escaped"][0],
                "light_sourced": light["sourced"][0],
                "light_current": light["current"][0],
                "light_escaped": light["escaped"][0],
                "momentum_sourced": momentum["sourced"],
                "momentum_current": momentum["current"],
                "balanced": ledger["balanced"],
            }
        )
    # The verdict. Closed: the reader reads exactly one group on the ring's
    # four Nodes with the content, its window covering the last WINDOW ticks
    # (to the last recorded tick T - 1), every tick row of that window bound at
    # the content, and no ring ray received off the ring. Else dispersed at the
    # first tick a ring ray is received off the ring, or, if none, the first
    # tick of the last WINDOW ticks whose bound row lacks the content.
    verdict = None
    group = None
    last_recorded = ticks - 1
    window_from = ticks - WINDOW
    if reading is not None:
        rings = [g for g in reading["groups"] if sorted(map(tuple, g["ring"])) == geo["corners"]]
        if len(reading["groups"]) == 1 and len(rings) == 1:
            group = rings[0]
        window_bound = (
            all(
                reading["bound"][t] == {"electron": [content]}
                for t in range(window_from, last_recorded + 1)
            )
            if len(reading["bound"]) > last_recorded
            else False
        )
        closed = (
            group is not None
            and group["families"] == {"electron": content}
            and group["from_tick"] <= window_from
            and group["to_tick"] == last_recorded
            and window_bound
            and off_ring_first is None
        )
        if closed:
            verdict = "closed"
        elif off_ring_first is not None:
            verdict = f"dispersed at tick {off_ring_first}"
        else:
            lost = next(
                (
                    t
                    for t in range(1, last_recorded + 1)
                    if reading["bound"][t] != {"electron": [content]}
                ),
                None,
            )
            verdict = f"dispersed at tick {lost}" if lost is not None else "unread"
    elif off_ring_first is not None:
        verdict = f"dispersed at tick {off_ring_first} (no recording, ring Nodes only)"
    per_tick_pushes = {}
    for p in pushes:
        per_tick_pushes[p["tick"]] = per_tick_pushes.get(p["tick"], 0) + 1
    push_list = [
        {
            "tick": p["tick"],
            "position": p["position"],
            "family": p["family"],
            "amount": p.get("amount"),
            "before": p["before"],
            "after": p["after"],
            "field": p["field"],
            "field_amount": p["field_amount"],
            "field_heading": p["field_heading"],
        }
        for p in pushes
    ]
    first_push = min((p["tick"] for p in pushes), default=None)
    final = rows[-1] if rows else None
    return {
        "run": str(directory),
        "model": metadata["model"],
        "status": metadata["status"],
        "error": metadata.get("error"),
        "source_sha256": metadata["source_sha256"],
        "initialization_sha256": metadata["initialization_sha256"],
        "events_sha256": events_sha256,
        "events_without_cost_sha256": physical.hexdigest(),
        "elapsed_seconds": metadata["elapsed_seconds"],
        "ticks": ticks,
        "content": content,
        "amount": geo["amount"],
        "variant": geo["variant"],
        "rules": geo["rules"],
        "corners": [list(c) for c in geo["corners"]],
        "ray_layer_families": metadata["ray_layer_families"],
        "ray_momentum_turn": metadata.get("ray_momentum_turn"),
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "balanced_every_tick": all(row["balanced"] for row in rows),
        "verdict": verdict,
        "group": group,
        "groups": reading["groups"] if reading is not None else None,
        "recorded_rays": reading["rays"] if reading is not None else None,
        "off_ring_first": off_ring_first,
        "pushes": len(pushes),
        "recoils": len(pushes),
        "pushes_per_tick": {str(k): v for k, v in sorted(per_tick_pushes.items())},
        "first_push": first_push,
        "pushes_on_ring": sum(1 for p in pushes if tuple(p["position"]) in corners),
        "pushes_off_ring": sum(1 for p in pushes if tuple(p["position"]) not in corners),
        "push_list": push_list,
        "near_field_first_16": {
            str(t): rows[t - 1]["light_by_corner"] for t in range(1, min(16, ticks) + 1)
        },
        "near_field_per_corner_max": max(
            (max(sum(v) for v in row["light_by_corner"].values()) if row["light_by_corner"] else 0)
            for row in rows
        )
        if rows
        else 0,
        "near_field_transverse_max": transverse_max(rows, geo["corners"]),
        "corner_sources_tick_2": corner_sources.get(2, {}),
        "ledger": {
            str(t): {
                k: rows[t - 1][k]
                for k in (
                    "electron_current",
                    "electron_escaped",
                    "light_sourced",
                    "light_current",
                    "light_escaped",
                    "momentum_sourced",
                    "momentum_current",
                    "balanced",
                )
            }
            for t in sorted({2, 3, 8, 16, 32, 64, ticks} & set(range(1, ticks + 1)))
        },
        "final_totals": metadata["final_totals"],
        "escaped_totals": metadata["escaped_totals"],
        "source_totals": metadata.get("source_totals"),
        "event_kinds": dict(sorted(kinds.items())),
        "final": final,
        "rows": rows,
    }


def transverse_max(rows, corners):
    """The largest light amount received at one corner in one interval on the
    two Ports of one axis (the transverse push a ray on another axis could get
    from one interval's arrivals, an upper bound: arrivals on opposite faces
    push opposite ways)."""
    best = 0
    for row in rows:
        for by_port in row["light_by_corner"].values():
            for axis in range(3):
                best = max(best, by_port[2 * axis] + by_port[2 * axis + 1])
    return best


def table(results):
    """The verdict table content -> control, corner first, turn first, with the
    pushes and whether the coupled record is the control's event for event."""
    by_content = {}
    for r in results:
        by_content.setdefault(r["content"], {})[r["variant"]] = r
    entries = []
    for content in sorted(by_content):
        variants = by_content[content]
        control = variants.get("control")
        entry = {"content": content}
        for variant in ("control", "corner_first", "turn_first"):
            r = variants.get(variant)
            if r is None:
                entry[variant] = None
                continue
            entry[variant] = {
                "verdict": r["verdict"],
                "pushes": r["pushes"],
                "first_push": r["first_push"],
                "ledger_exact": r["conserved_at_every_completed_tick"] and r["balanced_every_tick"],
                "events_identical_to_control": (
                    control is not None and r["events_sha256"] == control["events_sha256"]
                )
                if variant != "control"
                else None,
                "events_identical_to_control_without_cost": (
                    control is not None
                    and r["events_without_cost_sha256"] == control["events_without_cost_sha256"]
                )
                if variant != "control"
                else None,
                "elapsed_seconds": r["elapsed_seconds"],
            }
        entries.append(entry)
    return entries


def answer(entries):
    """Section 7's question: does the self-field select contents (a ladder)?"""
    coupled = [
        (e["content"], variant, e[variant]["verdict"])
        for e in entries
        for variant in ("corner_first", "turn_first")
        if e[variant] is not None
    ]
    by_variant = {}
    for content, variant, verdict in coupled:
        by_variant.setdefault(variant, []).append((content, verdict))
    result = {}
    for variant, items in by_variant.items():
        verdicts = {v for _, v in items}
        if verdicts == {"closed"}:
            result[variant] = "every content survives: no ladder from this coupling"
        elif all(v.startswith("dispersed") for v in verdicts):
            result[variant] = (
                "every content disperses: the loop needs the field not to push its own rays"
            )
        else:
            result[variant] = "the self-field selects contents: " + ", ".join(
                f"{c} {v}" for c, v in items
            )
    return result


def print_run(r):
    print(
        f"== {r['model']}  content {r['content']} ({r['variant']}, rules {r['rules']})"
        f"  ticks {r['ticks']} status {r['status']} {r['elapsed_seconds']:.1f}s"
    )
    print(f"   source {r['source_sha256']}  init {r['initialization_sha256']}")
    print(
        f"   events {r['events_sha256']}  layers {r['ray_layer_families']}  turn {r['ray_momentum_turn']}"
    )
    print(
        f"   verdict {r['verdict']}; pushes {r['pushes']} (on ring {r['pushes_on_ring']}, off"
        f" {r['pushes_off_ring']}), first {r['first_push']}; recoils {r['recoils']};"
        f" ledger {r['conserved_at_every_completed_tick']} balanced {r['balanced_every_tick']}"
    )
    if r["group"] is not None:
        g = r["group"]
        print(
            f"   group ring {g['ring']} content {g['content']} {g['families']} period {g['period']}"
            f" clock {g['clock']} from {g['from_tick']} to {g['to_tick']}"
        )
    else:
        print(f"   groups read: {r['groups']}")
    print(
        f"   near field per corner per interval: max {r['near_field_per_corner_max']},"
        f" max on one axis {r['near_field_transverse_max']} (amount per ray {r['amount']})"
    )
    print(
        "   tick  on  off  light@corners  pushes  bound            e_cur e_esc  l_src  l_cur  l_esc  p_cur"
    )
    shown = set(range(1, 9)) | {16, 32, 64, r["ticks"]} | {p["tick"] for p in r["push_list"][:12]}
    for row in r["rows"]:
        if row["tick"] in shown:
            print(
                f"   {row['tick']:4d} {row['on_ring']:4d} {row['off_ring']:4d}  {row['light_at_corners']:12d}"
                f"  {row['pushes']:6d}  {str(row['bound']):16s} {row['electron_current']:5d}"
                f" {row['electron_escaped']:5d} {row['light_sourced']:6d} {row['light_current']:6d}"
                f" {row['light_escaped']:6d}  {row['momentum_current']}"
            )
    for p in r["push_list"][:16]:
        print(
            f"   push t{p['tick']} at {p['position']} {p['family']} {p['before']} -> {p['after']}"
            f" by {p['field']} {p['field_amount']} on {p['field_heading']}"
        )
    if len(r["push_list"]) > 16:
        print(f"   ... {len(r['push_list']) - 16} more pushes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    results = [analyze(run) for run in args.runs]
    for r in results:
        print_run(r)
    entries = table(results)
    print("\n== Verdict table (content -> control / corner first / turn first)")
    for e in entries:
        cells = []
        for variant in ("control", "corner_first", "turn_first"):
            cell = e[variant]
            if cell is None:
                cells.append(f"{variant}: -")
            else:
                same = (
                    ""
                    if cell["events_identical_to_control"] is None
                    else (
                        " =control"
                        if cell["events_identical_to_control"]
                        else (
                            " =control but cost"
                            if cell["events_identical_to_control_without_cost"]
                            else " !=control"
                        )
                    )
                )
                cells.append(f"{variant}: {cell['verdict']} ({cell['pushes']} pushes{same})")
        print(f"   {e['content']:4d}  " + " | ".join(cells))
    verdicts = answer(entries)
    print("== Section 7's question, per declared order")
    for variant, text in verdicts.items():
        print(f"   {variant}: {text}")
    if args.out:
        args.out.write_text(
            json.dumps({"runs": results, "table": entries, "answer": verdicts}, indent=1) + "\n",
            encoding="utf-8",
        )
    if args.record:
        record = {
            "runs": [
                {k: r[k] for k in r if k not in ("rows", "run", "final")}
                | {"push_list": r["push_list"][:24], "pushes_listed": min(24, len(r["push_list"]))}
                for r in results
            ],
            "table": entries,
            "answer": verdicts,
        }
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
