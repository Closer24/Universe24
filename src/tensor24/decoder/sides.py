"""Clock: n/a: the decoder's guard on the edges between clocks, read from the record alone.
Algebra: per line holding sides, its sides' q summed to its q; per edge at a place, its two sides' q summing to 0 and their teeth to the key less 1, before and after (the owner's word of 03:4x UTC: every transfer between two clocks carried on one pair of complementary teeth, each edge closing, so the place closes).
Board: n/a: no board is read; the key is the train card's, the edge key, and the teeth are the edge's, as written.
Clicks: a click line of schema 1.4 holds its sides, one per edge side of its train at its round and Node-clock once any side there carries, q 0 among them (DECODE3's rule, writer B's line), in the other trains' order, [u, q, tooth before, tooth after]: the other train, the side's q and its tooth, the far end's the key less 1 less it; one line serves the three clicks, told apart by the sides a place holds and never by a label; a line that breaks a rule of the edges is refused, its cause named.
"""

from typing import Any

from tensor24.record import schema

Line = dict[str, Any]
Lines = list[Line | str]
Side = list[Any]  # [u, q, tooth before, tooth after]
Place = tuple[Any, Any, Any, Any]  # a side's round, site, train and other train


def whole(value: Any) -> bool:
    """A whole number, and not a truth value."""
    return isinstance(value, int) and not isinstance(value, bool)


def formed(side: Any) -> bool:
    """A side of the form [u, q, tooth before, tooth after], the schema's fields (schema.SIDE), each entry whole."""
    return isinstance(side, list) and len(side) == len(schema.SIDE) and all(map(whole, side))


def sided(n: int, e: Line, keys: dict[Any, Any]) -> str:
    """The first rule of its own one line's sides break: a tooth beside them or none, one off its form, a line naming no train whose card holds a whole key, one naming the line's own train or a train no card names, their trains out of order or one twice, their q not summing to the line's, or a tooth outside [0, K)."""
    t, sides, key = e.get("train"), e["sides"], keys.get(e.get("train"))
    if "tooth" in e or not isinstance(sides, list) or not sides:
        return f"line {n} holds a tooth beside its sides, or no sides"
    if not all(map(formed, sides)):
        return f"line {n}'s sides have not the form [u, q, tooth before, tooth after]"
    if not (whole(t) and whole(key)):
        return f"line {n} names no train whose card holds a whole key"
    us, total = [side[0] for side in sides], sum(side[1] for side in sides)
    found = [f"line {n}'s side names its own train {t}"] if t in us else []
    found += [f"line {n}'s side names train {u}, which no train card names" for u in us if u not in keys]
    found += (
        [f"line {n}'s sides stand out of their trains' order or name one twice"]
        if us != sorted(set(us))
        else []
    )
    found += [f"line {n}'s sides sum to {total}, not its q {e.get('q')}"] if total != e.get("q") else []
    found += (
        [f"line {n} holds a side's tooth outside [0, {key})"]
        if any(k < 0 or k >= key for _, _, before, after in sides for k in (before, after))
        else []
    )
    return found[0] if found else ""


def mirrored(n: int, e: Line, sides: dict[Place, Side], keys: dict[Any, Any]) -> str:
    """The first rule its sides break against their partners at their place: a partner absent, the two q not summing to 0, or the two teeth not summing to the key less 1, before or after."""
    key = keys.get(e["train"], 0)  # the edge key, the train card's
    for u, q, before, after in e["sides"]:
        partner = sides.get((e["round"], e["site"], u, e["train"]))
        if partner is None:
            return f"line {n}'s side to train {u} has no partner at its place"
        _, far, far_before, far_after = partner
        if q + far != 0:
            return f"line {n}'s side to train {u} and its partner hold q {q} and {far}, not 0 summed"
        if before + far_before != key - 1 or after + far_after != key - 1:
            return f"line {n}'s side to train {u} and its partner hold teeth not summing to the key less 1, {key - 1}"
    return ""


def paired(lines: Lines) -> str:
    """The first click line of the record whose sides break a rule of the edges, its own or against its partners', named: the decoder's guard on schema 1.4's sides."""
    header = lines[0] if lines and isinstance(lines[0], dict) else {}
    keys = {
        card.get("index"): card.get("key") for card in header.get("trains", []) if isinstance(card, dict)
    }
    events = list(enumerate(lines, start=1))[1:-1]
    held = [
        (n, e) for n, e in events if isinstance(e, dict) and e.get("kind") == "click" and "sides" in e
    ]
    for n, e in held:
        cause = sided(n, e, keys)
        if cause:
            return cause
    sides = {(e["round"], e["site"], e["train"], s[0]): s for _, e in held for s in e["sides"]}
    for n, e in held:
        cause = mirrored(n, e, sides, keys)
        if cause:
            return cause
    return ""
