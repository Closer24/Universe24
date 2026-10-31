"""Clock: n/a: the decoder's guard on the edges between clocks, read from the record alone.
Algebra: per line holding sides, its sides' q, in its site and across a Mesh, summed to its q; per edge, at its place in the site or across the Mesh, its two sides' q summing to 0 (the owner's word of 03:4x UTC: every transfer between two clocks carried on one pair of complementary teeth, each edge closing, so the place closes; the teeth are the board's and stand in no record, the owner's word on Q11).
Board: n/a: no board is read; the key is the train card's, the edge key.
Clicks: a click line of schema 3.0 holds its sides, one per edge side of its train at its round and Node-clock once any side there carries, q 0 among them (DECODE3's rule, writer B's line), in the other trains' order, [u, q]: the other train and the side's q, the far end's its negative; and its sides across a Mesh that carried (the Boss's ruling of 05:2x UTC, writer B's field), in their places' order, [u, place, q], the far end the other train's line at that place, which names this line's site; one line serves the three clicks, told apart by the sides a place holds and never by a label; a line that breaks a rule of the edges is refused, its cause named.
"""

from typing import Any

from tensor24.record import schema

Line = dict[str, Any]
Lines = list[Line | str]
Side = tuple[Any, Any, Any]  # the other clock's site and train, and q
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
    """Each side of a formed click line as the other clock's site and train, and q: its sides in its own site, then its sides across a Mesh at their places."""
    within = [(e["site"], u, q) for u, q in e.get("sides", [])]
    return within + [(at, u, q) for u, at, q in e.get("across", [])]


def sided(n: int, e: Line, keys: dict[Any, Any]) -> str:
    """The first rule of its own one line's sides break: no sides, one off its form, a line naming no train whose card holds a whole key, one naming the line's own train or a train no card names, their trains, or across a Mesh their places and trains, out of order or one twice, or their q not summing to the line's."""
    t, key = e.get("train"), keys.get(e.get("train"))
    sides, across = e.get("sides", []), e.get("across", [])
    if not (isinstance(sides, list) and isinstance(across, list)) or not sides + across:
        return f"line {n} holds no sides"
    if not all(map(formed, sides)):
        return f"line {n}'s sides have not the form [u, q]"
    if not all(formed(side, schema.ACROSS) for side in across):
        return f"line {n}'s sides across a Mesh have not the form [u, place, q]"
    if not (whole(t) and whole(key)):
        return f"line {n} names no train whose card holds a whole key"
    us, total = [u for u, _ in sides], sum(q for _, _, q in edged(e))
    places = [(at, u) for u, at, _ in across]
    found = [f"line {n}'s side names its own train {t}"] if t in us else []
    found += [
        f"line {n}'s side names train {u}, which no train card names"
        for _, u, _ in edged(e)
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
    return found[0] if found else ""


def mirrored(n: int, e: Line, sides: dict[Place, Side]) -> str:
    """The first rule its sides break against their partners at their place, in its site or across a Mesh: a partner absent, or the two q not summing to 0."""
    for at, u, q in edged(e):
        partner = sides.get((e["round"], at, u, e["site"], e["train"]))
        if partner is None:
            return f"line {n}'s side to train {u} has no partner at its place"
        _, _, far = partner
        if q + far != 0:
            return f"line {n}'s side to train {u} and its partner hold q {q} and {far}, not 0 summed"
    return ""


def paired(lines: Lines) -> str:
    """The first click line of the record whose sides break a rule of the edges, its own or against its partners', named: the decoder's guard on schema 3.0's sides, in the site and across a Mesh."""
    header = lines[0] if lines and isinstance(lines[0], dict) else {}
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
        (e["round"], e["site"], e["train"], at, u): (at, u, q) for _, e in held for at, u, q in edged(e)
    }
    for n, e in held:
        cause = mirrored(n, e, sides)
        if cause:
            return cause
    return ""
