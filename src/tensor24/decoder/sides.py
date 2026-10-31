"""Clock: n/a: the decoder's guard on the edges between clocks, read from the record alone.
Algebra: per line holding sides, its sides' q, in its site and across a Mesh, summed to its q; per edge, at its place in the site or across the Mesh, its two sides' q summing to 0 and their teeth to the key less 1, before and after (the owner's word of 03:4x UTC: every transfer between two clocks carried on one pair of complementary teeth, each edge closing, so the place closes).
Board: n/a: no board is read; the key is the train card's, the edge key, and the teeth are the edge's, as written.
Clicks: a click line of schema 1.4 holds its sides, one per edge side of its train at its round and Node-clock once any side there carries, q 0 among them (DECODE3's rule, writer B's line), in the other trains' order, [u, q, tooth before, tooth after]: the other train, the side's q and its tooth, the far end's the key less 1 less it; and its sides across a Mesh that carried (the Boss's ruling of 05:2x UTC, writer B's field), in their places' order, [u, place, q, tooth before, tooth after], the far end the other train's line at that place, which names this line's site; one line serves the three clicks, told apart by the sides a place holds and never by a label; a line that breaks a rule of the edges is refused, its cause named.
"""

from typing import Any

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
    sides, across = e.get("sides"), e.get("across", [])  # no default: every click line carries its sides
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


def paired(lines: Lines) -> str:
    """The first click line of the record whose sides break a rule of the edges, its own or against its partners', named: the decoder's guard on schema 1.4's sides, in the site and across a Mesh, on every click line, as the schema gives every click line its sides, so a line with no sides field is refused (the Boss's Q3 of 09:59 UTC, the ninth code reader's MINOR 2 on node-fold)."""
    header = lines[0] if lines and isinstance(lines[0], dict) else {}
    keys = {
        card.get("index"): card.get("key") for card in header.get("trains", []) if isinstance(card, dict)
    }
    events = list(enumerate(lines, start=1))[1:-1]
    held = [(n, e) for n, e in events if isinstance(e, dict) and e.get("kind") == "click"]
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
    return ""
