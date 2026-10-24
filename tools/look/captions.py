"""The events' captions, the viewer's words for every event of a run read from the logs alone (the owner's word of 2026-10-24: when such a thing happens, mark it with a label so the viewer understands what happened): one caption per event with its interval and, where a log names them, its Nodes, from the eras log (the fifth act's fires per interval, the Links at the wall), the Nodes' log (the turned Nodes and their X against the floor, the horizon's Links), the clicks log (the births with their children and senses, the clicks with the reader and the families exchanged, the conversions) and the world file (a body's Nodes, for a body's click); the bangs and the tops as tools/look/eras_page.py and tools/look/torus_page.py number them. Nothing declared: a run with no event of a kind has no caption of that kind. What the logs cannot name: a body's click's Node where no world file is given (the credit line names the body by its number), whether a born record stands as a mass, and a record's identity across intervals (two records of one family at one Node are one count there).

The legend of kinds and the per-bang ledger (the owner's word of 2026-10-24, 08:0x UTC: one sees everything from the run, with labels of what one sees, black holes, electrons, protons, bound bodies, everything; in every bang there must be more things): `legend_of` lists every kind of thing the law can show, each with its viewer's name, its clause in the law and its count in the run read from the logs alone, zeros included with the cause the logs give; `ledger_of` one row per bang (the cycle from a bang to the next) with the top, the births by family, the matter standing at the top, the light left, the horizon's Links and the Node turns, and the one sentence the rows show; `legend_html` the two blocks both pages carry. A log cut mid-run (its last line half written) is read to the last whole line by `parse_log`."""

from __future__ import annotations

import html
import json
from collections import Counter
from typing import Any

from event_universe.loader.circle import vector_of

READINGS = (
    "point",
    "kind",
    "sense",
    "support",
    "beat",
    "identity",
)  # the click's view's six keys on a credit line (src/event_universe/reports.READINGS; absent on the logs before 2026-10-24, read as absent)


def spans_of(counts: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    """Runs of intervals with a count above 0, each (first, last, the largest count), from (interval, count) pairs in order."""
    found: list[tuple[int, int, int]] = []
    first, most, last = None, 0, 0
    for at, count in counts:
        if count > 0:
            first, most, last = (at if first is None else first), max(most, count), at
        elif first is not None:
            found.append((first, last, most))
            first, most = None, 0
    if first is not None:
        found.append((first, last, most))
    return found


def returns_of(rows: list[tuple[int, Any, int]]) -> list[int]:
    """The bangs' intervals: the first logged interval, then every interval the volume's velocity turns from falling to rising after the fifth act fired since the last bang; `rows` the (interval, volume, fires) of the held row, the volume None where not read."""
    volumes = [(at, volume, fires) for at, volume, fires in rows if volume is not None]
    if not volumes:
        return []
    found, fired = [volumes[0][0]], 0
    for i in range(2, len(volumes)):
        fired += volumes[i - 1][2]
        if volumes[i - 1][1] - volumes[i - 2][1] < 0 < volumes[i][1] - volumes[i - 1][1] and fired > 0:
            found.append(volumes[i - 1][0])
            fired = 0
    return found


def tops_of(rows: list[tuple[int, Any, int]]) -> list[tuple[int, Any]]:
    """The volume's tops, the weak maxima of the held row's volume (the larger kept where two follow each other), as (interval, volume)."""
    volumes = [(at, volume) for at, volume, _fires in rows if volume is not None]
    found: list[tuple[int, Any]] = []
    for i in range(1, len(volumes) - 1):
        p, q, r = volumes[i - 1][1], volumes[i][1], volumes[i + 1][1]
        if q >= p and q >= r and (q > p or q > r):
            if found and not any(v < q for _a, v in volumes[volumes.index(found[-1]) : i]):
                found[-1] = volumes[i] if q > found[-1][1] else found[-1]
            else:
                found.append(volumes[i])
    return found


def node_words(nodes: list[Any], most: int = 4) -> str:
    """A few Nodes written out and the count of the rest."""
    shown = ", ".join(str(list(n)) for n in nodes[:most])
    return shown + (f" and {len(nodes) - most} more" if len(nodes) > most else "")


def reader_order(item: tuple[tuple[int, str], Any]) -> tuple[int, int, int, str]:
    """A credit's place among an interval's: the board's own clicks by the Node's index first, the readers by name after."""
    (at, reader), _lines = item
    return (at, 0, int(reader), "") if reader.isdigit() else (at, 1, 0, reader)


def captions_of(
    eras: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    clicks: list[dict[str, Any]],
    world: dict[str, Any] | None,
    floor: int | None,
) -> list[dict[str, Any]]:
    """Every event's caption, sorted by interval: {"at", "words", "nodes"} with the Nodes where a log names them (the births' and the board's own clicks' Nodes, the turned Nodes, a body's Node from the world file); `eras` the eras log with its header first, `nodes` the Nodes' log (may be empty), `clicks` the clicks log (may be empty), `world` the world file (None where none), `floor` the floor X_f (None where no Nodes' log)."""
    found: list[dict[str, Any]] = []
    held = eras[0]["held"][0] if eras and eras[0].get("held") else None
    lines = [line for line in eras[1:] if "rows" in line]
    rows = [
        (
            line["interval"],
            line["rows"][held].get("volume") if held else None,
            int(line.get("fires", 0) or 0),
        )
        for line in lines
    ]
    for number, at in enumerate(returns_of(rows), start=1):
        words = (
            "bang 1: the seed at rest, the board's volume rising from it"
            if number == 1
            else f"bang {number}: the board's volume turns from falling to rising"
        )
        found.append({"at": at, "words": words, "nodes": []})
    for number, (at, volume) in enumerate(tops_of(rows), start=1):
        found.append(
            {
                "at": at,
                "words": f"top {number}: the board's volume at its largest, {volume}",
                "nodes": [],
            }
        )
    shape = world["shape"] if world else (eras[0]["shape"] if eras else None)
    turned_at = {line["interval"]: line.get("turned", []) for line in nodes}
    x_at = {line["interval"]: line.get("X") for line in nodes}
    for first, last, _most in spans_of([(at, fires) for at, _v, fires in rows]):
        fired = sum(fires for at, _v, fires in rows if first <= at <= last)
        span = f"at {first}" if first == last else f"from {first} to {last}"
        at_floor: list[Any] = []
        for at in range(first, last + 1):
            xs = x_at.get(at)
            if floor is not None and xs is not None and shape is not None:
                for k in turned_at.get(at, []):
                    if xs[k] <= floor:
                        at_floor.append(k)
        words = f"the swap at the top fired {span}: {fired} Node turns, time reversed at each"
        turned = [k for at in range(first, last + 1) for k in turned_at.get(at, [])]
        found.append({"at": first, "words": words, "nodes": turned[:64]})
        if at_floor:
            found.append(
                {
                    "at": first,
                    "words": f"crunch: the turn at the floor {span} at {len(at_floor)} Node turns",
                    "nodes": at_floor[:64],
                }
            )
    horizon = [(line["interval"], int(line.get("horizon", 0) or 0)) for line in lines]
    for first, last, most in spans_of(horizon):
        links = next((line.get("horizon") for line in nodes if line["interval"] == first), None)
        at_first = dict(horizon)[first]
        found.append(
            {
                "at": first,
                "words": f"a black hole formed: {at_first} Links held at the wall"
                + (f", growing to {most} Links" if most > at_first else ""),
                "nodes": [n for link in (links or []) for n in link][:64]
                if isinstance(links, list)
                else [],
            }
        )
        if last > first or last < lines[-1]["interval"]:
            found.append(
                {
                    "at": last,
                    "words": f"the black hole dissolved after {last - first + 1} intervals",
                    "nodes": [],
                }
            )
    births: dict[int, list[dict[str, Any]]] = {}
    for line in clicks:
        if line.get("event") == "birth":
            births.setdefault(int(line["interval"]), []).append(line)
    for at, lines_at in sorted(births.items()):
        kinds = sorted({(" and ".join(b["children"]), tuple(b["senses"])) for b in lines_at})
        places = [n for b in lines_at for n in b["nodes"]]
        pairs = "; ".join(
            f"{names}, the senses {list(senses)} (matter and antimatter)" for names, senses in kinds
        )
        count = f"{len(lines_at)} lists were" if len(lines_at) > 1 else "a list was"
        found.append(
            {"at": at, "words": f"{count} born: {pairs}, at {node_words(places)}", "nodes": places[:64]}
        )
    bodies = world.get("bodies", []) if world else []
    credits: dict[tuple[int, Any], list[dict[str, Any]]] = {}
    for line in clicks:
        if (
            line.get("event") == "credit"
            and line.get("count")
            and line.get("before") != line.get("realised")
        ):
            credits.setdefault((int(line["interval"]), str(line.get("node_detector"))), []).append(line)
    for (at, reader), lines_at in sorted(credits.items(), key=reader_order):
        first = lines_at[0]
        if isinstance(first.get("node_detector"), int) and shape is not None:
            k = int(first["node_detector"])
            place = [k // (shape[1] * shape[2]), (k // shape[2]) % shape[1], k % shape[2]]
            words = f"a click: two quanta of {first.get('absorbed')} met at the Node {place} and its list of children was born"
            found.append({"at": at, "words": words, "nodes": [place]})
            continue
        if reader.startswith("body ") and reader[5:].isdigit() and int(reader[5:]) < len(bodies):
            where = [entry["node"] for entry in bodies[int(reader[5:])]["nodes"]]
        else:
            where = []
        for line in lines_at:
            taken, given = line.get("absorbed"), line.get("emitted")
            act = (
                f"{taken} absorbed by {reader}"
                if taken
                else f"{given} emitted by {reader}"
                if given
                else f"a write by {reader}"
            )
            parts = f" ({line.get('before')} to {line.get('realised')})" if line.get("realised") else ""
            found.append(
                {
                    "at": at,
                    "words": f"a click: {act}{parts}"
                    + (f" at the Node {where[0]}" if len(where) == 1 else ""),
                    "nodes": where[:64],
                }
            )
    for line in clicks:
        if line.get("event") == "conversion":
            found.append(
                {
                    "at": int(line["interval"]),
                    "words": f"a conversion: {line.get('family')} let go into {' and '.join(line.get('into', []))}, the senses {line.get('senses')}",
                    "nodes": [],
                }
            )
    found.sort(key=lambda c: c["at"])
    return found


def parse_log(text: str) -> list[dict[str, Any]]:
    """The log's lines, one JSON object per line; a last line cut mid-write (a log read while its run goes on) is left out, a cut anywhere else raises."""
    lines = [line for line in text.splitlines() if line.strip()]
    found: list[dict[str, Any]] = []
    for k, line in enumerate(lines):
        try:
            found.append(json.loads(line))
        except json.JSONDecodeError:
            if k == len(lines) - 1:
                break
            raise
    return found


def held_rows(eras: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[tuple[int, Any, int]]]:
    """The eras log's lines with rows and the held row's (interval, volume, fires), as `captions_of` reads them."""
    held = eras[0]["held"][0] if eras and eras[0].get("held") else None
    lines = [line for line in eras[1:] if "rows" in line]
    rows = [
        (
            int(line["interval"]),
            line["rows"][held].get("volume") if held else None,
            int(line.get("fires", 0) or 0),
        )
        for line in lines
    ]
    return lines, rows


def families_of(eras: list[dict[str, Any]]) -> tuple[list[str], list[str], str | None]:
    """The families the logs name: the families of quanta (the held row's writes), the holders (the eras' quanta beside them, the sign holder) and the seed family (the one with quanta at the first logged interval, the massless family the engine seeds)."""
    lines, _rows = held_rows(eras)
    if not lines:
        return [], [], None
    held = eras[0]["held"][0]
    quanta = list(lines[0]["rows"][held].get("writes", {}))
    holders = [name for name in lines[0].get("quanta", {}) if name not in quanta]
    seeded = [name for name, q in lines[0].get("quanta", {}).items() if q.get("quanta", 0) > 0]
    return quanta, holders, seeded[0] if len(seeded) == 1 else None


def captions_for(header: dict[str, Any] | None) -> dict[str, str]:
    """The pages' captions read from the header's integers alone (the owner's word of 2026-10-24: the names become labels of the record's pages, never input): the seed row, the massless point, captioned "light"; among the points of den's circle (the header's `points`, each row's num and s under its vector label) the lifts of den's primes, the vectors with twice the prime's exponent at one of den's primes 1 mod 4 and 0 elsewhere, captioned by rising sine, the leg s over den, "electron", "proton" and "neutron" (the neutron's candidate point; the owner's word of 2026-10-24 on the born-amplitude hand's reading at the PeV den, where the proton's point 2 0 0 is the lightest prime's lift and the electron's point 0 0 2 the heaviest's: the former rule, the least leg electron and the heaviest prime's own point proton, was the top tier's accident, kept by name), the top point and the composite points their label alone; every other row its label alone; a log with no points (the record to 2026-10-24, its rows named) captions nothing."""
    header = header or {}
    found: dict[str, str] = {}
    if header.get("seed"):
        found[str(header["seed"])] = "light"
    points = {name: pair for name, pair in (header.get("points") or {}).items() if vector_of(name)}
    primes = header.get("primes") or []
    lifts = []
    for place, (_prime, power) in enumerate(primes):
        lift = tuple(2 * int(power) if i == place else 0 for i in range(len(primes)))
        lifts += [name for name in points if vector_of(name) == lift]
    kinds = ("electron", "proton", "neutron")
    for name, kind in zip(sorted(lifts, key=lambda name: int(points[name][1])), kinds, strict=False):
        found[name] = kind
    return found


def shown(name: str, captions: dict[str, str]) -> str:
    """A row's name on the pages, its caption beside it where the integers give one ("point 0 0 2 (proton)"), the name alone otherwise."""
    return f"{name} ({captions[name]})" if name in captions else name


def n(value: Any) -> str:
    """A whole number with its thousands marked, anything else written out."""
    return f"{value:,}" if isinstance(value, int) and not isinstance(value, bool) else str(value)


def standing_of(line: dict[str, Any] | None, family: str) -> tuple[int, int, int, int]:
    """A family's quanta at one Nodes' log line: (total, Nodes above 0, least per Node, largest per Node)."""
    counts = list((line or {}).get("quanta", {}).get(family, []))
    if not counts:
        return 0, 0, 0, 0
    return sum(counts), sum(1 for c in counts if c > 0), min(counts), max(counts)


def standing_words(line: dict[str, Any] | None, family: str) -> str:
    """A family's quanta at a line in words: the count per Node where every Node reads alike, the least and largest otherwise."""
    total, where, least, most = standing_of(line, family)
    if total == 0:
        return "0"
    per = f"{n(least)} per Node" if least == most else f"from {n(least)} to {n(most)} per Node"
    return f"{n(total)} quanta, {per}, at {n(where)} Nodes"


def legend_of(
    eras: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    clicks: list[dict[str, Any]],
    floor: int | None,
) -> dict[str, Any]:
    """The legend of kinds: every kind of thing the law can show, as {"reached", "declared", "rows": [{"kind", "law", "count", "words"}]}, the count an integer read from the logs (None where the logs cannot name it) and the words its reading with the cause where it is 0; nothing declared."""
    lines, rows = held_rows(eras)
    quanta, holders, seed = families_of(eras)
    captions = captions_for(eras[0] if eras else None)
    reached = lines[-1]["interval"] if lines else None
    last_nodes = nodes[-1] if nodes else None
    found: list[dict[str, Any]] = []
    bangs = returns_of(rows)
    found.append(
        {
            "kind": "bangs",
            "law": "the seed at rest bang 1, then every interval the board's volume turns from falling to rising after the swap at the top fired (the return)",
            "count": len(bangs),
            "words": f"at {', '.join(n(b) for b in bangs)}"
            if bangs
            else "none: no row of the held family in the eras log",
        }
    )
    tops = tops_of(rows)
    found.append(
        {
            "kind": "tops",
            "law": "the board's volume at its largest, where the fifth act, the swap at the top, fires",
            "count": len(tops),
            "words": "; ".join(f"{n(at)} at the volume {n(v)}" for at, v in tops)
            if tops
            else "none reached in the intervals logged",
        }
    )
    horizon = [
        (at, int(line.get("horizon", 0) or 0))
        for at, line in zip((r[0] for r in rows), lines, strict=True)
    ]
    holes = spans_of(horizon)
    found.append(
        {
            "kind": "black holes",
            "law": "a Link whose tension reaches the wall Gamma is read at the wall, its two ends decoupled: the horizon",
            "count": len(holes),
            "words": "; ".join(
                f"formed at {n(a)} with {n(dict(horizon)[a])} Links, the most {n(m)}, "
                + (f"dissolved at {n(b)}" if b < (reached or b) else f"standing at {n(b)}")
                for a, b, m in holes
            )
            if holes
            else f"0 in this run: the eras log's horizon 0 at every interval to {n(reached)}",
        }
    )
    turned_at_floor = 0
    least_x = None
    for line in nodes:
        xs = line.get("X")
        if xs:
            least_x = min(xs) if least_x is None else min(least_x, min(xs))
            if floor is not None:
                turned_at_floor += sum(1 for k in line.get("turned", []) if xs[k] <= floor)
    found.append(
        {
            "kind": "turns at the floor (the crunch)",
            "law": "a Node whose time line's output would fall below the floor X_f turns as at the top",
            "count": turned_at_floor if nodes else None,
            "words": (
                f"{n(turned_at_floor)} Node turns at or under the floor {n(floor)}; the least X over the run {n(least_x)}"
                if nodes and floor is not None
                else "not readable: no Nodes' log"
            ),
        }
    )
    fired = sum(f for _a, _v, f in rows)
    firings = spans_of([(at, f) for at, _v, f in rows])
    found.append(
        {
            "kind": "Node turns (the swap at the top)",
            "law": "each Node reads three levels of its own time line and, where the middle is the largest, ends the interval at the state it started from with the levels exchanged: time reversed there",
            "count": fired,
            "words": f"{n(fired)} turns in {n(len(firings))} firings, the first at {n(firings[0][0])}"
            if firings
            else "0: the eras log's fires 0 at every interval",
        }
    )
    births = [line for line in clicks if line.get("event") == "birth"]
    children = Counter(" and ".join(b["children"]) for b in births)
    for family in [f for f in quanta if f != seed]:
        born = [b for b in births if b["children"] and b["children"][0] == family]
        if born:
            ats = sorted({int(b["interval"]) for b in born})
            places = {tuple(node) for b in born for node in b["nodes"]}
            senses = sorted({tuple(b["senses"]) for b in born})
            words = f"{n(len(born))} births at {', '.join(n(a) for a in ats)}, at {n(len(places))} Nodes, the senses {' and '.join(str(list(s)) for s in senses)} (matter and antimatter)"
        elif births:
            words = f"none born: every birth line's children are {' or '.join(shown(c, captions) for c in children)}, the heaviest list within the two meeting quanta's energy at every Node (the law's sentence)"
        else:
            words = "none born: no birth line in the clicks log"
        found.append(
            {
                "kind": f"{shown(family, captions)} births",
                "law": "two whole quanta of the seed family meeting at one Node make the heaviest exact list of children within their energy, one record each, the two quanta taken by the hole at that Node",
                "count": len(born),
                "words": words,
            }
        )
    conversions = [line for line in clicks if line.get("event") == "conversion"]
    found.append(
        {
            "kind": "conversions",
            "law": "a click that absorbs a quantum of one family and gives it as quanta of others, the rotations adding (the weak force)",
            "count": len(conversions),
            "words": "; ".join(
                f"at {n(c['interval'])}: {c.get('family')} into {' and '.join(c.get('into', []))}"
                for c in conversions
            )
            if conversions
            else "0: no conversion line in the clicks log",
        }
    )
    credits = [
        line
        for line in clicks
        if line.get("event") == "credit"
        and line.get("count")
        and line.get("before") != line.get("realised")
    ]
    if credits:
        counts = sorted({int(c["count"]) for c in credits})
        own = sum(1 for c in credits if isinstance(c.get("node_detector"), int))
        absorbed = sorted({str(c.get("absorbed")) for c in credits if c.get("absorbed")})
        realised = sorted({str(c.get("realised")) for c in credits if c.get("realised")})
        ats = sorted({int(c["interval"]) for c in credits})
        null = [
            key
            for key in ("momentum", "lost", "source", "kept", "left")
            if all(c.get(key) is None for c in credits)
        ]
        words = (
            f"{n(len(credits))} at {', '.join(n(a) for a in ats)}, {n(own)} the board's own (node_detector the Node's index), count {' or '.join(n(c) for c in counts)} each, "
            f"{' and '.join(absorbed) or 'nothing'} absorbed, {' and '.join(realised) or 'nothing'} realised; "
            + (
                f"the click's view {', '.join(READINGS)} on every line; "
                if all(all(key in c for key in READINGS) for c in credits)
                else ""
            )
            + f"the fields {', '.join(null)} null in every line: every click counted whole, no part drawn"
        )
    else:
        words = "0: no credit line with a count and a changed part in the clicks log"
    found.append(
        {
            "kind": "clicks",
            "law": "the meeting of the future and the past at one Node, Rule3's division act on the families, two whole quanta received",
            "count": len(credits),
            "words": words,
        }
    )
    lays = [line for line in clicks if line.get("event") == "lay"]
    by_line = Counter((str(line.get("family")), int(line.get("line", 0) or 0)) for line in lays)
    found.append(
        {
            "kind": "lays (the records laid)",
            "law": "a record's levels set at a Node by a birth or the seed, the lines' two levels written whole",
            "count": len(lays),
            "words": "; ".join(
                f"{fam}'s line {ln} at {n(c)} Nodes" for (fam, ln), c in sorted(by_line.items())
            )
            + (
                f", at {', '.join(n(a) for a in sorted({int(line['interval']) for line in lays}))}"
                if lays
                else ""
            )
            if lays
            else "0: no lay line in the clicks log",
        }
    )
    for family in quanta + holders:
        since = next((line["interval"] for line in nodes if standing_of(line, family)[0] > 0), None)
        carried = since is not None and all(
            standing_of(line, family)[0] > 0 for line in nodes if line["interval"] >= since
        )
        gone = next(
            (
                line["interval"]
                for line in nodes
                if since is not None and line["interval"] > since and standing_of(line, family)[0] == 0
            ),
            None,
        )
        total = standing_of(last_nodes, family)[0]
        if not nodes:
            words = "not readable: no Nodes' log"
        elif total:
            words = (
                f"{standing_words(last_nodes, family)} at {n(last_nodes['interval'] if last_nodes else None)}, standing since {n(since)}"
                + (" (carried through every top)" if carried and len(tops) else "")
            )
        elif since is None:
            words = "0: no quantum of the family at any Node at any logged interval"
        else:
            words = f"0 from {n(gone)}: standing from {n(since)}, spent at the holes"
        kind = (
            f"standing {shown(family, captions)} (the seed family: light left)"
            if family == seed
            else f"standing {shown(family, captions)}"
            if family in quanta
            else f"standing {family} (a holder, beside the families of quanta: the held row writes none of it)"
        )
        found.append(
            {
                "kind": kind,
                "law": "a family's quanta as the Nodes' log reads them at the last interval, a record standing where its family's quanta stay above 0",
                "count": total if nodes else None,
                "words": words,
            }
        )
    found.append(
        {
            "kind": "bound bodies",
            "law": "a record standing as a mass in a holder's well, the atom a bound body of bound bodies",
            "count": None,
            "words": "not readable from the logs: whether a born record stands as a mass, and a record's identity across intervals, the logs do not name (two records of one family at one Node are one count there)",
        }
    )
    declared = eras[0].get("intervals") if eras else None
    return {"reached": reached, "declared": declared, "rows": found}


def ledger_of(
    eras: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    clicks: list[dict[str, Any]],
) -> dict[str, Any]:
    """The per-bang ledger: one row per bang, the cycle from that bang to the interval before the next (the last to the log's last interval), as {"rows": [...], "finding": the one sentence the rows show}; each row {"bang", "at", "to", "top", "volume", "births": {family: pairs}, "standing": {family: words at the top}, "light", "horizon", "turns", "open"}, every value read from the logs."""
    lines, rows = held_rows(eras)
    quanta, _holders, seed = families_of(eras)
    bangs = returns_of(rows)
    tops = tops_of(rows)
    reached = int(lines[-1]["interval"]) if lines else 0
    by_interval = {line["interval"]: line for line in nodes}
    births = [line for line in clicks if line.get("event") == "birth"]
    found: list[dict[str, Any]] = []
    for k, at in enumerate(bangs):
        to: int = bangs[k + 1] - 1 if k + 1 < len(bangs) else reached
        inside = [(a, v) for a, v in tops if at <= a <= to]
        top = max(inside, key=lambda t: t[1]) if inside else None
        read_at = top[0] if top else to
        line = by_interval.get(read_at) or next(
            (by_interval[a] for a in sorted(by_interval, reverse=True) if a <= read_at), None
        )
        born = Counter(
            b["children"][0] for b in births if at <= int(b["interval"]) <= to and b["children"]
        )
        cycle = [(a, ln) for (a, _v, _f), ln in zip(rows, lines, strict=True) if at <= a <= to]
        found.append(
            {
                "bang": k + 1,
                "at": at,
                "to": to,
                "top": top[0] if top else None,
                "volume": top[1] if top else None,
                "births": {family: born.get(family, 0) for family in quanta if family != seed},
                "standing": {
                    family: standing_words(line, family) for family in quanta if family != seed
                },
                "read_at": line["interval"] if line else None,
                "light": standing_of(line, seed)[0] if seed and line else None,
                "horizon": max((int(ln.get("horizon", 0) or 0) for _a, ln in cycle), default=0),
                "turns": sum(int(ln.get("fires", 0) or 0) for _a, ln in cycle),
                "open": k + 1 == len(bangs),
            }
        )
    spent = None
    if seed:
        lit = [(line["interval"], standing_of(line, seed)[0]) for line in nodes]
        spent = next(
            (a for (a, q), (_b, before) in zip(lit[1:], lit, strict=False) if q == 0 and before > 0),
            None,
        )
    later = found[1:]
    if not found:
        finding = "No bang read: the eras log holds no row of the held family."
    elif not later:
        finding = f"One bang in the intervals logged, to {n(reached)}: the births of its cycle {', '.join(f'{v} {f} pairs' for f, v in found[0]['births'].items())}."
    elif all(sum(row["births"].values()) == 0 for row in later):
        first = ", ".join(f"{n(v)} {f} pairs" for f, v in found[0]["births"].items() if v) or "none"
        finding = (
            f"The logs show nothing new after bang 1: {n(len(later))} cycles after the first with 0 births each, "
            f"the first cycle's births {first}"
            + (f", the light spent at {n(spent)} and 0 from then on" if spent else "")
            + "; what stands at every later top is the first cycle's matter carried."
        )
    else:
        with_births = [
            f"bang {row['bang']} ({', '.join(f'{n(v)} {f}' for f, v in row['births'].items() if v)})"
            for row in later
            if sum(row["births"].values())
        ]
        finding = f"Births after bang 1 at {', '.join(with_births)}; the other cycles 0."
    return {"rows": found, "finding": finding}


def legend_html(legend: dict[str, Any], ledger: dict[str, Any], wide: bool = True) -> str:
    """The two blocks both pages carry, rendered as HTML rows: the legend of kinds and the per-bang ledger."""
    e = html.escape
    cls = "panel wide" if wide else "panel"
    reached = f"to the interval {n(legend['reached'])}" + (
        f" of {n(legend['declared'])} declared" if legend.get("declared") else ""
    )
    kinds = "".join(
        f"<tr><td><b>{e(str(row['kind']))}</b></td><td>{e(str(row['law']))}</td>"
        f'<td class="num">{e(n(row["count"])) if row["count"] is not None else "not readable"}</td><td>{e(str(row["words"]))}</td></tr>'
        for row in legend["rows"]
    )
    cycles = "".join(
        f'<tr><td class="num">{row["bang"]}</td><td class="num">{e(n(row["at"]))}</td>'
        f'<td class="num">{e(n(row["to"]))}{" (the log's last interval)" if row["open"] else ""}</td>'
        f'<td class="num">{e(n(row["top"])) + " at the volume " + e(n(row["volume"])) if row["top"] is not None else "none reached"}</td>'
        f"<td>{e('; '.join(f'{n(v)} {f} pairs' for f, v in row['births'].items()) or 'none')}</td>"
        f"<td>{e('; '.join(f'{f}: {w}' for f, w in row['standing'].items()))} (read at {e(n(row['read_at']))})</td>"
        f'<td class="num">{e(n(row["light"]))}</td><td class="num">{e(n(row["horizon"]))}</td><td class="num">{e(n(row["turns"]))}</td></tr>'
        for row in ledger["rows"]
    )
    return (
        f'<section class="{cls}" id="kinds-box"><h2>The legend of kinds: every kind of thing the law can show, its count in this run read from the logs alone, {e(reached)}</h2>'
        '<div class="scroll"><table id="kinds"><tr><th>kind (the viewer\'s name)</th><th>in the law</th><th>count</th><th>read from the logs</th></tr>'
        f"{kinds}</table></div></section>\n"
        f'<section class="{cls}" id="ledger-box"><h2>The per-bang ledger: one row per bang, the cycle from the bang to the next</h2>'
        f'<p class="words" id="ledger-finding"><b>{e(ledger["finding"])}</b></p>'
        '<div class="scroll"><table id="ledger"><tr><th>bang</th><th>at</th><th>to</th><th>top (interval, volume)</th><th>births in the cycle</th><th>matter standing at the top</th><th>light left</th><th>horizon Links</th><th>Node turns</th></tr>'
        f"{cycles}</table></div></section>"
    )
