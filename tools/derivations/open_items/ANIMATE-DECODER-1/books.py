"""Row 15, the conservation at the click: its first reading, K3, the books at every whole click (Animate's part C, read
on the schema's whole line): the windings taken + the remainder before - the remainder after = the windings laid, at the
click, or at each of its ends where it takes at both (a pair into light).

The second reading, K1 summed over every train before and after the click's round, is the ledger's. A record read
without its ledger reads it not read, and the row with it, the cause named.
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


def row_15(record, ledger):
    """The row's verdict from its two readings."""
    first = books_at_clicks(record)
    every = (
        first["closed"] == first["with their books"] == first["whole clicks"] and first["whole clicks"]
    )
    if ledger is None:
        cause = "the ledger is absent, so the second reading (K1 over every train) is not read"
        reading = "closed at every whole click" if every else "open at some whole click"
        return {"kind": "NOT READ", "cause": f"{cause}; the first reads {reading}", "first": first}
    return {"kind": "SHOWN" if every else "NOT SHOWN", "first": first}
