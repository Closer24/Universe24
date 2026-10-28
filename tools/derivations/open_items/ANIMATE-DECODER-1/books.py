"""Row 15, the conservation at the click: its first reading, K3, the books at every whole click (Animate's part C, read
on the schema's whole line): the windings taken + the remainder before - the remainder after = the windings laid, at the
click, or at each of its ends where it takes at both (a pair into light).

The second reading, K1 summed over every train before and after the click's round, is the ledger's: per round, the
wind over every train against the round's clicks' net. A record read without its ledger reads it not read, and the row
with it, the cause named.
"""


def windings(parts):
    return sum(p["windings"] for p in parts)


def booked(part):
    """Whether a click, or one of its ends, carries its books."""
    return "ends" in part or ("remainder" in part and "taken" in part and "laid" in part)


def closes(part):
    """Whether one whole click's books close: at each end where it takes at both (a pair into light), else at the click."""
    if "ends" in part:
        return all(booked(end) and closes(end) for end in part["ends"])
    r = part["remainder"]
    return windings(part["taken"]) + r["before"] - r["after"] == windings(part["laid"])


def books_at_clicks(record):
    """The first reading over every whole click of a record, and the fittings apart (the head's reader read those)."""
    clicks = record.of("whole")
    held = [c for c in clicks if booked(c)]
    fittings = [c for c in held if "children" in c]
    return {
        "whole clicks": len(clicks),
        "with their books": len(held),
        "closed": sum(closes(c) for c in held),
        "fittings": len(fittings),
        "fittings closed": sum(closes(c) for c in fittings),
        "pairs into light, books per end": sum("ends" in c for c in fittings),
    }


def wind_over_rounds(record, ledger):
    """The second reading, from the ledger: per round, the wind over every train against the round's clicks' net (laid
    - taken, which the books make the remainders' fall). Rounds with no click are counted apart: there the wind over
    every train can move by the tick alone."""
    totals, trains = {}, {}
    for line in ledger:
        totals[line["round"]] = totals.get(line["round"], 0) + line["wind"]
        trains[(line["round"], line["train"])] = line["wind"]
    nets = {}
    for c in record.of("whole"):
        if booked(c):
            nets[c["round"]] = nets.get(c["round"], 0) + windings(c["laid"]) - windings(c["taken"])
    clicked = {e["round"] for e in record.events if e["kind"] in ("whole", "books")}
    rounds = sorted(totals)
    held, quiet, moved, worst, by_train = 0, 0, 0, None, {}
    for before, now in zip(rounds, rounds[1:], strict=False):
        change, net = totals[now] - totals[before], nets.get(now, 0)
        held += change == net
        quiet += now not in clicked
        moved += now not in clicked and change != 0
        for train in sorted({k for r, k in trains if r == now}):
            if now not in clicked and trains[(now, train)] != trains.get(
                (before, train), trains[(now, train)]
            ):
                by_train[train] = by_train.get(train, 0) + 1
        if worst is None or abs(change - net) > worst["gap"]:
            worst = {"gap": abs(change - net), "round": now, "change": change, "net": net}
    return {
        "rounds read": len(rounds) - 1 if rounds else 0,
        "held": held,
        "rounds with no click": quiet,
        "of them the wind moved": moved,
        "trains moved on rounds with no click": by_train,
        "the largest gap": worst,
    }


def row_15(record, ledger):
    """The row's verdict from its two readings."""
    first = books_at_clicks(record)
    every = (
        first["closed"] == first["with their books"] == first["whole clicks"] and first["whole clicks"]
    )
    reading = "closed at every whole click" if every else "open at some whole click"
    if ledger is None:
        cause = "the ledger is absent, so the second reading (K1 over every train) is not read"
        return {"kind": "NOT READ", "cause": f"{cause}; the first reads {reading}", "first": first}
    second = wind_over_rounds(record, ledger)
    agree = second["held"] == second["rounds read"]
    if every and agree:
        return {
            "kind": "SHOWN",
            "cause": "the books close at every whole click, and the ledger agrees",
            "first": first,
            "second": second,
        }
    w = second["the largest gap"]
    light = [t["index"] for t in record.header["trains"] if t.get("light")]
    moved = ", ".join(
        f"{'light' if k in light else 'train'} {k} on {n}"
        for k, n in second["trains moved on rounds with no click"].items()
    )
    cause = (
        f"the first reads {reading}; the second holds at {second['held']} of {second['rounds read']} rounds, since the "
        f"tick itself moves the wind: it moved on {second['of them the wind moved']} of "
        f"{second['rounds with no click']} rounds with no click ({moved}; the largest gap {w['gap']} at round "
        f"{w['round']}, the wind moved by {w['change']} against the clicks' {w['net']}). The tick, not the click, parts "
        "the two readings"
    )
    return {"kind": "NOT SHOWN", "cause": cause, "first": first, "second": second}
