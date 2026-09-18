"""The books between release and meeting: part (a) of experiment E11
(docs/EXPERIMENTS.md), the field's books.

Runs `books.json` (the spreading field of a body A and one free electron ray at
impact parameter 4, the catalog's rule) and `books_axis.json` (the same without
`spread`, A's field on its six axis lines, the picture of Highlights 3.5 in
words) in-process and prints, per completed tick, where the energy (the
amount) and the momentum are: the light released this tick and the source line
(cumulative), the light in flight and in the remainder registers, the momentum
of the light in flight (amount x heading over the light rays, the reading the
ledger uses; the recoils among them, the light rays a push returned reversed and
not yet spread, counted apart), the pushes of the tick with the electron's
change and the reversal they book, the electron's register and its change from
its launch, A's register (the bodies' momentum line) and what its sink absorbed
(the absorbed line), what escaped, and the identity at every tick:

    momentum: sourced = light in flight + (electron - its launch) + absorbed + escaped light
    amount:   light sourced = in flight + registers + absorbed + escaped;
              electron: 64 in the world or escaped

both read from the world ledger of `ray-event-audit-v1` (the `balanced` flag
re-checked here from the integers) with the light's part of the momentum read
from the inventory, so that "in flight" is a column and not a residual. The
lamp that launched the electron keeps the launch's recoil, (-64, 0, 0), in its
own register (a funded emission), which is why the electron's change and not
its register enters the identity; once the electron has escaped, its register
sits on the ledger's `escaped` line beside the escaped light's and the identity
reads it there. Events are labelled by the engine with the
tick at the start of their interval (a push in the interval that completes tick
T is labelled T - 1; an absorption, an arrival or an escape at the end of that
interval is labelled T); the table's row T is the state after interval T with
that interval's events. The marks: t0, the release of the field ray that first
meets the electron (in the axis world exactly, the ray's Links walked; in the
spread world the front, released at tick 1 and spread at every Node since, as a
spread erases a ray's history); t1, the tick of the first push; t2, the first
tick at which A's register moves, the arrival of recoil momentum at A.

Run:  PYTHONPATH=src python examples/nature/e11_field_books/books.py [--world books.json books_axis.json] [--record record.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from event_universe import Simulation
from event_universe.core.spatial_state import ray_momentum_vector
from event_universe.initialization import parse_initial_state
from event_universe.json_documents import parse_json_document
from event_universe.runner import source_fingerprint

HERE = Path(__file__).resolve().parent
PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
LIGHT = "light"
ELECTRON = "electron"
CYCLE_EVENTS = {"ray_push", "field_spread", "spatial_cycle", "field_returned"}


def add(u, v):
    return [a + b for a, b in zip(u, v, strict=True)]


def sub(u, v):
    return [a - b for a, b in zip(u, v, strict=True)]


def scale(s, v):
    return [s * a for a in v]


def family_index(initial, name):
    names = [field.name for field in initial.fields]
    return [field.field for field in initial.spatial_fields].index(names.index(name))


def read_rays(world, light, electron):
    """The light's momentum in flight (every light ray as the ledger reads it),
    the recoils among them (event-stamped light rays, returned by a push and not
    yet spread) and the electron ray, from the inventory view."""
    initial = world.initial
    light_definition = initial.spatial_fields[light]
    electron_definition = initial.spatial_fields[electron]
    light_momentum = [0, 0, 0]
    light_amount = 0
    recoil_momentum = [0, 0, 0]
    recoil_amount = 0
    recoils = 0
    electron_ray = None
    view = world.inventory_view()
    owners = [(node.position, node.rays) for node in view.nodes if node.rays]
    owners.extend(
        (("link", packet.origin, packet.port), packet.rays) for packet in view.packets if packet.rays
    )
    for where, rays in owners:
        for ray in rays[light]:
            sign = 1 if ray.outbound else -1
            vector = scale(sign, ray_momentum_vector(ray, light_definition))
            light_momentum = add(light_momentum, vector)
            light_amount += ray.amount
            if ray.event_ports:
                recoils += 1
                recoil_amount += ray.amount
                recoil_momentum = add(recoil_momentum, vector)
        for ray in rays[electron]:
            electron_ray = {
                "where": list(where) if not isinstance(where[0], str) else list(where),
                "amount": ray.amount,
                "register": list(ray_momentum_vector(ray, electron_definition)),
                "heading": list(electron_definition.headings[ray.heading]),
                "accumulators": list(ray.accumulators),
            }
    return {
        "light_momentum": light_momentum,
        "light_amount": light_amount,
        "recoils": recoils,
        "recoil_amount": recoil_amount,
        "recoil_momentum": recoil_momentum,
        "electron": electron_ray,
    }


def registers_total(world, light):
    initial = world.initial
    definition = initial.spatial_fields[light]
    if not definition.spread:
        return 0
    total = sum(definition.spread)
    held = 0
    spatial = world._spatial
    if spatial.dense is not None:
        family = spatial.dense.families[light]
        held += int(family.reg.sum()) // family.total
    for node in spatial.nodes.values():
        if node.remainders and node.remainders[light]:
            held += sum(node.remainders[light]) // total
    return held


def run_world(document, *, ticks=None, log=print):
    initial = parse_initial_state(document)
    count = int(document["ticks"]) if ticks is None else int(ticks)
    light = family_index(initial, LIGHT)
    electron = family_index(initial, ELECTRON)
    launch = [int(v) for v in document["emissions"][0]["heading"]]
    amount = int(document["emissions"][0]["amount"])
    launch_momentum = scale(amount, launch)
    (body,) = document["external_bodies"]
    centre = [int(c) for c in body["position"]]
    events = {"ray_push": [], "external_body_absorbed": [], "spatial_escaped": [], "electron_at": []}

    def observe(event):
        kind = event.get("event")
        if kind in events:
            events[kind].append(event)
        elif kind == "spatial_received":
            for readings in event["received_fields"]:
                if readings and readings.get(ELECTRON, [0])[0]:
                    events["electron_at"].append(
                        {"tick": event["tick"], "position": list(event["position"])}
                    )

    rows = []
    started = time.perf_counter()
    previous_body = [0, 0, 0]
    previous = None
    # The electron's register wherever it is: in the world (read from the
    # inventory) or, once it escaped, the register it carried out (the last
    # push's `after` in the interval of the escape, else the last one read),
    # which the ledger's `escaped` line holds beside the escaped light's.
    last_register = list(launch_momentum)
    escaped_register = None
    with Simulation(initial, observer=observe) as world:
        for tick in range(1, count + 1):
            world.step()
            audit = world.audit()
            light_line = audit["fields"][LIGHT]
            electron_line = audit["fields"][ELECTRON]
            momentum = audit["fields"]["momentum"]
            rays = read_rays(world, light, electron)
            held = registers_total(world, light)
            pushes = [e for e in events["ray_push"] if e["tick"] == tick - 1]
            absorbed_now = [e for e in events["external_body_absorbed"] if e["tick"] == tick]
            escaped_now = [e for e in events["spatial_escaped"] if e["tick"] == tick]
            at = [e["position"] for e in events["electron_at"] if e["tick"] == tick]
            push_delta = [0, 0, 0]
            reversal = [0, 0, 0]
            for push in pushes:
                push_delta = add(push_delta, sub(list(push["after"]), list(push["before"])))
                reversal = add(
                    reversal, scale(-2 * int(push["field_amount"]), list(push["field_heading"]))
                )
            body_momentum = [int(v) for v in audit["bodies"]["momentum"]]
            sourced = [int(v) for v in momentum["sourced"]]
            current = [int(v) for v in momentum["current"]]
            escaped = [int(v) for v in momentum["escaped"]]
            absorbed = [int(v) for v in momentum["absorbed"]]
            sourced_delta = sourced if previous is None else sub(sourced, previous["momentum_sourced"])
            spreads = sub(sub(sourced_delta, push_delta), reversal)
            e = rays["electron"]
            if e:
                last_register = list(e["register"])
            elif escaped_register is None:
                escaped_register = list(pushes[-1]["after"]) if pushes else list(last_register)
            e_register = e["register"] if e else None
            carried = e_register if e else escaped_register
            e_change = sub(carried, launch_momentum)
            escaped_light = escaped if e else sub(escaped, escaped_register)
            lamp = sub(sub(current, rays["light_momentum"]), e_register if e else [0, 0, 0])
            row = {
                "tick": tick,
                "electron_at": at[-1] if at else None,
                "electron_register": e_register,
                "electron_carried": carried,
                "electron_change": e_change,
                "light_escaped_momentum": escaped_light,
                "electron_current": int(electron_line["current"][0]),
                "electron_escaped": int(electron_line["escaped"][0]),
                "electron_absorbed": int(electron_line["absorbed"][0]),
                "pushes": len(pushes),
                "push_delta": push_delta,
                "reversal": reversal,
                "spreads_booking": spreads,
                "light_released": int(light_line["sourced"][0])
                - (0 if previous is None else previous["light_sourced"]),
                "light_sourced": int(light_line["sourced"][0]),
                "light_current": int(light_line["current"][0]),
                "light_flight": int(light_line["current"][0]) - held,
                "light_registers": held,
                "light_escaped": int(light_line["escaped"][0]),
                "light_absorbed": int(light_line["absorbed"][0]),
                "light_absorbed_now": sum(int(x["amount"]) for x in absorbed_now),
                "light_momentum": rays["light_momentum"],
                "recoils": rays["recoils"],
                "recoil_amount": rays["recoil_amount"],
                "recoil_momentum": rays["recoil_momentum"],
                "momentum_sourced": sourced,
                "momentum_current": current,
                "momentum_escaped": escaped,
                "momentum_absorbed": absorbed,
                "body_momentum": body_momentum,
                "body_push": sub(body_momentum, previous_body),
                "lamp_register": lamp,
                "escapes": len(escaped_now),
                "balanced": bool(audit["balanced"]),
                "identity_momentum": sourced
                == add(add(add(rays["light_momentum"], e_change), absorbed), escaped_light),
                "identity_light": int(light_line["sourced"][0])
                == int(light_line["current"][0])
                + int(light_line["escaped"][0])
                + int(light_line["absorbed"][0]),
                "identity_electron": int(electron_line["current"][0])
                + int(electron_line["escaped"][0])
                + int(electron_line["absorbed"][0])
                == amount,
                "inventory_light_amount": rays["light_amount"],
            }
            rows.append(row)
            previous = row
            previous_body = body_momentum
            if log is not None:
                log(
                    f"tick {tick:3d} e@{str(row['electron_at']):>14} reg {str(e_register):>16}"
                    f" pushes {len(pushes):2d} d{str(push_delta):>14} | light flight {row['light_flight']:6d}"
                    f" regs {held:5d} p {str(rays['light_momentum']):>16} recoils {rays['recoils']:2d}"
                    f" | A {str(body_momentum):>14} abs {str(absorbed):>14} esc {str(escaped):>14}"
                    f" | ok {row['balanced']} {row['identity_momentum']} {row['identity_light']}"
                )
    elapsed = time.perf_counter() - started
    marks = mark_ticks(rows, events, centre, document)
    return {
        "model": document["model_id"],
        "shape": [int(n) for n in document["shape"]],
        "centre": centre,
        "spread": bool(any(f.get("spread") for f in document["spatial_fields"])),
        "dense_field": bool(initial.dense_field),
        "ticks": count,
        "electron_amount": amount,
        "launch": launch_momentum,
        "coupling_sign": document["ray_interactions"][0]["momentum_table"][LIGHT],
        "source_sha256": source_fingerprint(),
        "elapsed_seconds": elapsed,
        "balanced_every_tick": all(r["balanced"] for r in rows),
        "identity_momentum_every_tick": all(r["identity_momentum"] for r in rows),
        "identity_light_every_tick": all(r["identity_light"] for r in rows),
        "identity_electron_every_tick": all(r["identity_electron"] for r in rows),
        "lamp_register_constant": all(r["lamp_register"] == scale(-1, launch_momentum) for r in rows),
        "inventory_matches_ledger": all(r["inventory_light_amount"] == r["light_flight"] for r in rows),
        "marks": marks,
        "pushes": [
            {
                "tick": int(e["tick"]) + 1,
                "label": int(e["tick"]),
                "position": list(e["position"]),
                "before": list(e["before"]),
                "after": list(e["after"]),
                "field_amount": int(e["field_amount"]),
                "field_heading": list(e["field_heading"]),
            }
            for e in events["ray_push"]
        ],
        "absorptions_with_push": [
            {
                "tick": int(e["tick"]),
                "port": int(e["port"]),
                "amount": int(e["amount"]),
                "momentum_after": list(e["momentum"]),
            }
            for e in events["external_body_absorbed"]
        ],
        "electron_escape_tick": next(
            (int(e["tick"]) for e in events["spatial_escaped"] if e["escaped"].get(ELECTRON)), None
        ),
        "rows": rows,
    }


def mark_ticks(rows, events, centre, document):
    """t0, t1, t2 as the module docstring defines them."""
    pushes = sorted(events["ray_push"], key=lambda e: (e["tick"], 0))
    if not pushes:
        return {"t0": None, "t1": None, "t2": None, "first_push": None}
    first = pushes[0]
    t1 = int(first["tick"]) + 1
    position = [int(c) for c in first["position"]]
    heading = [int(h) for h in first["field_heading"]]
    spread = any(f.get("spread") for f in document["spatial_fields"])
    if spread:
        # The front: content at L1 distance k after tick T was released at tick
        # T - k + 1 at the latest; the first-met rays are the front's.
        distance = sum(abs(p - c) for p, c in zip(position, centre, strict=True))
        t0 = (t1 - 1) - distance + 1
        how = "the front, A's release spread at every Node since"
    else:
        # On A's line through the field heading: the Links walked since the release,
        # (P - A) . h for the push Node P and the field heading h.
        walked = sum((p - c) * h for p, c, h in zip(position, centre, heading, strict=True))
        t0 = t1 - walked if walked > 0 else None
        how = f"the ray's {walked} Links walked on A's line"
    t2 = next((r["tick"] for r in rows if any(r["body_momentum"])), None)
    return {
        "t0": t0,
        "t1": t1,
        "t2": t2,
        "how_t0": how,
        "first_push": {
            "tick": t1,
            "position": position,
            "field_amount": int(first["field_amount"]),
            "field_heading": heading,
            "before": list(first["before"]),
            "after": list(first["after"]),
        },
    }


def print_timeline(record, out=print):
    m = record["marks"]
    out(
        f"== {record['model']}  shape {record['shape']}  A at {record['centre']}  spread {record['spread']}"
        f"  dense {record['dense_field']}  coupling sign {record['coupling_sign']}  ticks {record['ticks']}"
        f"  {record['elapsed_seconds']:.1f} s"
    )
    out(f"   source {record['source_sha256']}")
    out(
        f"   balanced every tick {record['balanced_every_tick']}; momentum identity with the source line"
        f" every tick {record['identity_momentum_every_tick']}; light amount identity {record['identity_light_every_tick']};"
        f" electron amount constant {record['identity_electron_every_tick']}; lamp register constant"
        f" {record['lamp_register_constant']}; inventory light equals the ledger's in flight {record['inventory_matches_ledger']}"
    )
    out(
        f"   t0 = {m['t0']} ({m.get('how_t0')}), t1 = {m['t1']} (first push at {m['first_push']['position'] if m['first_push'] else None}"
        f" by {m['first_push']['field_amount'] if m['first_push'] else None} on {m['first_push']['field_heading'] if m['first_push'] else None}),"
        f" t2 = {m['t2']}; pushes {len(record['pushes'])}; electron escaped at tick {record['electron_escape_tick']}"
    )
    out(
        "   tick  mark  e at         e register       pushes d(e)           light flight regs  p(light)         recoils(n,a)"
        "  sourced p        absorbed p       A register       escaped p        light src cur esc abs"
    )
    for r in record["rows"]:
        mark = "".join(
            label for label, t in (("t0", m["t0"]), ("t1", m["t1"]), ("t2", m["t2"])) if t == r["tick"]
        )
        out(
            f"   {r['tick']:4d}  {mark:4s}  {str(r['electron_at']):12s} {str(r['electron_register']):16s}"
            f" {r['pushes']:2d} {str(r['push_delta']):16s} {r['light_flight']:6d} {r['light_registers']:5d}"
            f" {str(r['light_momentum']):16s} ({r['recoils']},{r['recoil_amount']})"
            f" {str(r['momentum_sourced']):16s} {str(r['momentum_absorbed']):16s} {str(r['body_momentum']):16s}"
            f" {str(r['momentum_escaped']):16s} {r['light_sourced']} {r['light_current']} {r['light_escaped']} {r['light_absorbed']}"
        )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--world", type=Path, nargs="*", default=[HERE / "books.json", HERE / "books_axis.json"]
    )
    parser.add_argument("--ticks", type=int)
    parser.add_argument("--record", type=Path, default=HERE / "record.json")
    args = parser.parse_args(argv)
    records = {}
    for path in args.world:
        source = path.read_bytes()
        document = parse_json_document(source)
        record = run_world(document, ticks=args.ticks)
        record["world"] = path.name
        record["initialization_sha256"] = hashlib.sha256(source).hexdigest()
        print_timeline(record)
        records[path.stem] = record
    if args.record:
        existing = {}
        if args.record.exists():
            existing = json.loads(args.record.read_text(encoding="utf-8"))
        existing["books"] = records
        args.record.write_text(json.dumps(existing, indent=1) + "\n", encoding="utf-8")
        print(f"\nwrote {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
