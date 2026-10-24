"""The events' captions, the viewer's words for every event of a run read from the logs alone (the owner's word of 2026-10-24: when such a thing happens, mark it with a label so the viewer understands what happened): one caption per event with its interval and, where a log names them, its Nodes, from the eras log (the fifth act's fires per interval, the Links at the wall), the Nodes' log (the turned Nodes and their X against the floor, the horizon's Links), the clicks log (the births with their children and senses, the clicks with the reader and the families exchanged, the conversions) and the world file (a body's Nodes, for a body's click); the bangs and the tops as tools/look/eras_page.py and tools/look/torus_page.py number them. Nothing declared: a run with no event of a kind has no caption of that kind. What the logs cannot name: a body's click's Node where no world file is given (the credit line names the body by its number), whether a born record stands as a mass, and a record's identity across intervals (two records of one family at one Node are one count there)."""

from __future__ import annotations

from typing import Any


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
        count = f"{len(lines_at)} pairs were" if len(lines_at) > 1 else "a pair was"
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
            words = f"a click: two quanta of {first.get('absorbed')} met at the Node {place} and the pair was born"
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
