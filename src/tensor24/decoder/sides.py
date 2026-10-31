"""Clock: n/a: the decoder's guard on the edges between clocks, read from the record alone.
Algebra: per line holding sides, its sides' q, in its site and across a Mesh, summed to its q; per edge, at its place in the site or across the Mesh, its two sides' q summing to 0 and their teeth to the key less 1, before and after (the owner's word of 03:4x UTC: every transfer between two clocks carried on one pair of complementary teeth, each edge closing, so the place closes).
Board: n/a: no board is read; the key is the train card's, the edge key, the teeth are the edge's, as written, and the header's dial is read against the universe file's key, a whole multiple of it where the end lists an edge and the key itself where it lists none.
Clicks: a click line of schema 1.4 holds its sides, one per edge side of its train at its round and Node-clock once any side there carries, q 0 among them (DECODE3's rule, writer B's line), in the other trains' order, [u, q, tooth before, tooth after]: the other train, the side's q and its tooth, the far end's the key less 1 less it; and its sides across a Mesh that carried (the Boss's ruling of 05:2x UTC, writer B's field), in their places' order, [u, place, q, tooth before, tooth after], the far end the other train's line at that place, which names this line's site; one line serves the three clicks, told apart by the sides a place holds and never by a label; a line that breaks a rule of the edges, or holds a side on an edge the end line does not list, is refused, its cause named.
"""

import json
from typing import Any

from tensor24.algebra.carry import carry
from tensor24.record import schema

Line = dict[str, Any]
Lines = list[Line | str]
Side = tuple[
    Any, Any, Any, Any, Any
]  # the other clock's site and train, q, tooth before and tooth after
Place = tuple[
    Any, Any, Any, Any, Any
]  # a side's round, site and train, and the other clock's site and train


def whole(value: Any) -> bool:
    """A whole number, and not a truth value."""
    return isinstance(value, int) and not isinstance(value, bool)


def formed(side: Any, fields: tuple[str, ...] = schema.SIDE) -> bool:
    """A side of the form its schema's fields name (schema.SIDE, or schema.ACROSS across a Mesh), each entry whole."""
    return isinstance(side, list) and len(side) == len(fields) and all(map(whole, side))


def edged(e: Line) -> list[Side]:
    """Each side of a formed click line as the other clock's site and train, q, tooth before and after: its sides in its own site, then its sides across a Mesh at their places."""
    within = [(e["site"], u, q, before, after) for u, q, before, after in e.get("sides", [])]
    return within + [(at, u, q, before, after) for u, at, q, before, after in e.get("across", [])]


def sided(n: int, e: Line, keys: dict[Any, Any]) -> str:
    """The first rule of its own one line's sides break: a tooth beside them or none, one off its form, a line naming no train whose card holds a whole key, one naming the line's own train or a train no card names, their trains, or across a Mesh their places and trains, out of order or one twice, their q not summing to the line's, or a tooth outside [0, K)."""
    t, key = e.get("train"), keys.get(e.get("train"))
    sides, across = e.get("sides", []), e.get("across", [])
    if "tooth" in e or not (isinstance(sides, list) and isinstance(across, list)) or not sides + across:
        return f"line {n} holds a tooth beside its sides, or no sides"
    if not all(map(formed, sides)):
        return f"line {n}'s sides have not the form [u, q, tooth before, tooth after]"
    if not all(formed(side, schema.ACROSS) for side in across):
        return (
            f"line {n}'s sides across a Mesh have not the form [u, place, q, tooth before, tooth after]"
        )
    if not (whole(t) and whole(key)):
        return f"line {n} names no train whose card holds a whole key"
    us, total = [u for u, _, _, _ in sides], sum(q for _, _, q, _, _ in edged(e))
    places = [(at, u) for u, at, _, _, _ in across]
    found = [f"line {n}'s side names its own train {t}"] if t in us else []
    found += [
        f"line {n}'s side names train {u}, which no train card names"
        for _, u, _, _, _ in edged(e)
        if u not in keys
    ]
    found += (
        [f"line {n}'s sides stand out of their trains' order or name one twice"]
        if us != sorted(set(us))
        else []
    )
    found += (
        [f"line {n}'s sides across a Mesh stand out of their places' order or name one twice"]
        if places != sorted(set(places))
        else []
    )
    found += [f"line {n}'s sides sum to {total}, not its q {e.get('q')}"] if total != e.get("q") else []
    found += (
        [f"line {n} holds a side's tooth outside [0, {key})"]
        if any(k < 0 or k >= key for *_, before, after in edged(e) for k in (before, after))
        else []
    )
    return found[0] if found else ""


def mirrored(n: int, e: Line, sides: dict[Place, Side], keys: dict[Any, Any]) -> str:
    """The first rule its sides break against their partners at their place, in its site or across a Mesh: a partner absent, the two q not summing to 0, or the two teeth not summing to the key less 1, before or after."""
    key = keys.get(e["train"], 0)  # the edge key, the train card's
    for at, u, q, before, after in edged(e):
        partner = sides.get((e["round"], at, u, e["site"], e["train"]))
        if partner is None:
            return f"line {n}'s side to train {u} has no partner at its place"
        _, _, far, far_before, far_after = partner
        if q + far != 0:
            return f"line {n}'s side to train {u} and its partner hold q {q} and {far}, not 0 summed"
        if before + far_before != key - 1 or after + far_after != key - 1:
            return f"line {n}'s side to train {u} and its partner hold teeth not summing to the key less 1, {key - 1}"
    return ""


def filed(header: Line) -> Any:
    """The file's key: the CHOSEN key the universe file holds, the first of the header's files in the run's order (universe, piece, setting), or None where the header holds none."""
    files = header.get("files")
    first = files[0] if isinstance(files, list) and files and isinstance(files[0], dict) else {}
    text = first.get("text")
    try:
        held = json.loads(text) if isinstance(text, str) else None
    except ValueError, RecursionError:  # no JSON, past the interpreter's digits or depth
        return None
    chosen = held.get("chosen") if isinstance(held, dict) else None
    return chosen.get("key") if isinstance(chosen, dict) else None


def dialed(header: Line, end: Line) -> str:
    """The header's dial off the file's key, where the header holds a whole dial and its universe file a whole key of 1 or more: not a whole multiple of the key, once or more, where the end lists an edge (the node's dial D = (kappa div senses) K), nor the key itself where it lists none (the Boss's ruling of 08:5x)."""
    dial, key = header.get("dial"), filed(header)
    if not (whole(dial) and whole(key) and key >= 1):
        return ""
    times, left = carry(dial, key, 0)
    if end.get("teeth") or end.get("across"):
        off = left != 0 or times < 1
        return f"the header's dial {dial} is no whole multiple of the file's key {key}" if off else ""
    return (
        f"the header's dial {dial} is not the file's key {key}, the end listing no edge"
        if dial != key
        else ""
    )


def listed(end: Line, held: list[tuple[int, Line]]) -> str:
    """The first side of a click line on an edge the end line does not list, where the end lists the record's edges (it holds its teeth or its across): a side in its site whose two trains no entry of the end's teeth names; a side across a Mesh at a far place the end's across does not name at the line's site for its two trains, or where the end holds no across (two trains its across names in no entry are records.crossed's to name)."""
    if "teeth" not in end and "across" not in end:
        return ""
    own = {(t, u) for t, u, _ in end.get("teeth", [])}
    pairs = {(t, u) for t, u, _, _ in end.get("across", [])}
    far = {(t, u, x, p) for t, u, places, _ in end.get("across", []) for x, p in enumerate(places)}
    for n, e in held:
        t, x = e["train"], e["site"]
        for u, *_ in e.get("sides", []):
            if (t, u) not in own:
                return f"line {n}'s side to train {u} stands on no edge the end line lists"
        for u, at, *_ in e.get("across", []):
            if (t, u, x, at) not in far and ((t, u) in pairs or "across" not in end):
                return f"line {n}'s side across a Mesh to train {u} at place {at} stands on no edge the end line lists"
    return ""


def paired(lines: Lines) -> str:
    """The header's dial off the file's key, or the first click line of the record whose sides break a rule of the edges, its own or against its partners', or stand on an edge the end line does not list, named: the decoder's guard on schema 2.0's sides, in the site and across a Mesh."""
    header = lines[0] if lines and isinstance(lines[0], dict) else {}
    end = lines[-1] if lines and isinstance(lines[-1], dict) else {}
    cause = dialed(header, end)
    if cause:
        return cause
    keys = {
        card.get("index"): card.get("key") for card in header.get("trains", []) if isinstance(card, dict)
    }
    events = list(enumerate(lines, start=1))[1:-1]
    held = [
        (n, e)
        for n, e in events
        if isinstance(e, dict) and e.get("kind") == "click" and ("sides" in e or "across" in e)
    ]
    for n, e in held:
        cause = sided(n, e, keys)
        if cause:
            return cause
    sides = {
        (e["round"], e["site"], e["train"], at, u): (at, u, q, before, after)
        for _, e in held
        for at, u, q, before, after in edged(e)
    }
    for n, e in held:
        cause = mirrored(n, e, sides, keys)
        if cause:
            return cause
    return listed(end, held)
