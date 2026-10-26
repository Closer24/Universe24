"""The gates read from the clicks (the credit and the birth lines), one function per row of UNIVERSE24's table: 2 the Links lengthening in the clicks, 8 families forming and 8b the species over a body's track, 10 the dilation in the reader's view, 15 the conservation at the click, 16 the one-click floor, 17 the charge, 19 the mass ratios in the clicks and 24 the merger from the births' taken row and the gapped meetings' refusals; the species solved by decoder.py, memoized per record."""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import cmp_to_key
from typing import Any

from event_universe.board import neighbours
from event_universe.core.paces import sine_den
from event_universe.decoder import (
    FEW,
    HALF,
    HUNDRED,
    LIFTS,
    MIL,
    PAIR,
    SPANS,
    THOUSAND,
    Rational,
    Record,
    cmp_rat,
    decoded_credits,
    middle,
    nearest,
    quot,
    unread_words,
)

Decoded = list[tuple[dict[str, Any], str, Rational]]


def solved(record: Record) -> tuple[Decoded, int, int, list[int | None]]:
    """The record's credits solved once per cut: the decoded (credit, name, x), the count read right, the count within the floor, each credit's floor."""
    key = f"solved {record.intervals} {len(record.credits)}"
    if key not in record.memo:
        record.memo[key] = decoded_credits(record)
    found: tuple[Decoded, int, int, list[int | None]] = record.memo[key]
    return found


def tracks_of(
    record: Record,
) -> tuple[dict[tuple[Any, int], list[Rational]], int, Counter[tuple[str, str]]]:
    """A body's track, its decoded rationals by (Node, line), the tracks read right by the middle solve, and the confusion truth -> decoded per credit."""
    decoded = solved(record)[0]
    tracks: dict[tuple[Any, int], list[Rational]] = defaultdict(list)
    confusion: Counter[tuple[str, str]] = Counter()
    for c, name, x in decoded:
        tracks[(tuple(c["node"]), c["line"])].append(x)
        confusion[(record.line_name[c["line"]], name)] += 1
    right = 0
    for (_node, line), xs in tracks.items():
        xs.sort(key=cmp_to_key(cmp_rat))
        right += nearest(record, middle(xs), 1) == record.line_name[line]
    return tracks, right, confusion


def species_track(record: Record) -> dict[str, Any]:
    """Row 8b: the species over a body's track (the one-place view: the middle solve of the track's rationals)."""
    tracks, right, confusion = tracks_of(record)
    return {
        "8b species over the track (one-place view: the middle solve of the body's track)": {
            "tracks": len(tracks),
            "decoded right": right,
            "confusion (truth->decoded) per credit": {
                f"{a}->{b}": n for (a, b), n in confusion.items() if a != b
            },
            "verdict": "SHOWN: every track read right"
            if tracks and right == len(tracks)
            else f"NOT SHOWN: tracks right {right} of {len(tracks)}"
            if tracks
            else "NOT READ: no credit decoded",
        }
    }


def families(record: Record) -> dict[str, Any]:
    """Gate 8: the species from the frame of every credit (the whole view), every credit within the one-click floor and every track read right, three or more species born."""
    decoded, right, within, _floors = solved(record)
    tracks, track_right, _confusion = tracks_of(record)
    born = record.born_of()
    if not decoded:
        verdict = "NOT READ: no credit in the record"
    elif within == len(decoded) and track_right == len(tracks) and len(born) >= LIFTS:
        verdict = "SHOWN (every credit within the one-click floor, every track read right)"
    elif within == len(decoded):
        verdict = (
            f"SHOWN in part: every credit within the floor, tracks right {track_right} of {len(tracks)}"
        )
    else:
        verdict = f"NOT SHOWN: {len(decoded) - within} credits beyond the floor"
    return {
        "8 families forming (whole view)": {
            "credits": len(record.credits),
            "species readable": len(decoded),
            "decoded right per credit": right,
            "credits within the one-click floor": within,
            "tracks right": [track_right, len(tracks)],
            "births by species (decoder)": dict(born),
            "at": min(record.credits, key=lambda c: int(c["i"]))["node"] if record.credits else None,
            "verdict": verdict,
        }
    }


def leg_of(record: Record, x: Rational) -> int:
    """The leg of a decoded rational x = num / den on den's circle, sine_den at the nearest integer num, 0 off the circle (|num| at or past den)."""
    num = abs(quot(x[0] * record.den, x[1]) or 0)
    return sine_den(num, record.den) if num < record.den else 0


def mass_ratios(record: Record) -> dict[str, Any]:
    """Gate 19: the mass ratios in the clicks (MS-S1's predicate: per credited plane the middle solve of its tracks' middles, its leg against the header's, the ratio of the two heaviest credited planes' legs read right within the one-click floor; NOT SHOWN where one plane alone is credited) beside den's typed legs and den's circle."""
    decoded, _right, _within, floor_mil = solved(record)
    tracks, _track_right, _confusion = tracks_of(record)
    names, line_num = record.NAMES, record.line_num
    legs = sorted(((name, leg) for name, leg in names.values() if leg), key=lambda kv: kv[1])
    found: dict[str, Any] = {f"{nm}/{legs[0][0]}": quot(leg, legs[0][1], MIL) for nm, leg in legs[1:]}
    by_plane: dict[int, list[Rational]] = defaultdict(list)
    for (_node, line), xs in tracks.items():
        by_plane[line_num[line]].append(middle(xs))
    credited = sorted(
        (num for num in by_plane if num != record.den), key=lambda num: sine_den(num, record.den)
    )
    read_legs = {
        num: leg_of(record, middle(sorted(by_plane[num], key=cmp_to_key(cmp_rat)))) for num in credited
    }
    for num in credited:
        found[f"{names[num][0]} leg in the clicks / header (parts per million)"] = quot(
            read_legs[num], sine_den(num, record.den) or 1, MIL
        )
    if len(credited) < PAIR:
        read = (
            f"NOT SHOWN: {len(credited)} plane credited, a ratio needs two"
            if decoded
            else "NOT READ: no credit decoded"
        )
    else:
        heavy, light = credited[-1], credited[-PAIR]
        clicks = quot(read_legs[heavy], read_legs[light], MIL) if read_legs[light] else None
        header = quot(sine_den(heavy, record.den), sine_den(light, record.den), MIL)
        floors = [f for f in floor_mil if f is not None]
        found["the two heaviest credited planes' legs: clicks / header (parts per million)"] = [
            clicks,
            header,
        ]
        read = (
            "SHOWN: the mass ratio in the clicks reads the header's within the one-click floor"
            if clicks is not None and header is not None and abs(clicks - header) <= max(floors or [0])
            else "NOT SHOWN: the lighter plane's leg in the clicks is 0 (below the floor)"
            if clicks is None
            else "NOT SHOWN: the ratio in the clicks is off the header's beyond the floor"
        )
    circle = record.circle()
    least = min((s for _num, s in circle), default=0)
    found[
        "den's circle: the points' legs over the least (parts per million), the typed among them marked"
    ] = [[quot(s, least, MIL), num in record.NAMES] for num, s in sorted(circle, key=lambda p: p[1])]
    return {"19 mass ratios (parts per million)": found | {"verdict": read}}


def one_click_floor(record: Record) -> dict[str, Any]:
    """Gate 16: the one-click floor on x per credit (the uncertainty floor), no credit reading beyond it."""
    decoded, _right, within, floor_mil = solved(record)
    fl = sorted(f for f in floor_mil if f is not None)
    if not fl:
        return {"16 uncertainty floor (one click)": {"verdict": "NOT READ: no credit decoded"}}
    names = record.NAMES
    legs = sorted(((num, leg) for num, (_name, leg) in names.items() if leg), key=lambda kv: kv[1])
    spacing = quot(abs(legs[-1][0] - legs[-PAIR][0]), legs[-1][0], MIL) if len(legs) >= PAIR else None
    return {
        "16 uncertainty floor (one click)": {
            "floor on x per credit, parts per million: min / middle / max": [
                fl[0],
                fl[len(fl) // HALF],
                fl[-1],
            ],
            "species spacing of the two heaviest, parts per million": spacing,
            "credits beyond the floor": len(decoded) - within,
            "verdict": "SHOWN as the law's floor: no credit reads beyond it"
            if within == len(decoded)
            else "NOT SHOWN",
        }
    }


def charge(record: Record) -> dict[str, Any]:
    """Gate 17: the charge (each child's sense the sign of its own Wronskian at its Node, summed over the births; its magnitude one |W| on every child laid where its plane stood at nothing, MS-S1, the children laid on a residue counted by name)."""
    births = record.births
    signs, sizes = record.signs_of(), sorted(record.laid_at_nothing())
    residue = sum(1 for b in births for stood in b.get("stood", [[0], [0]]) if any(stood))
    sense_sum = sum(signs)
    opposite = sum(
        1
        for b in births
        if (b["W_children"][0] > 0) != (b["W_children"][1] > 0) and 0 not in b["W_children"]
    )
    verdict = (
        "NOT READ: no birth in the record"
        if not births
        else "SHOWN: the senses sum to 0"
        if sense_sum == 0 and 0 not in signs
        else "NOT SHOWN: the senses"
    ) + (
        "; the magnitude SHOWN: one |W| on every child laid where its plane stood at nothing"
        if sizes and sizes[0] == sizes[-1]
        else "; the magnitude NOT SHOWN: |W| differs between the children laid where their plane stood at nothing"
        if sizes
        else "; the magnitude NOT READ"
    )
    return {
        "17 charge conservation": {
            "senses sum over births (from the children's Wronskian signs)": sense_sum,
            "children with W = 0": signs.count(0),
            "births with the two children at opposite signs": opposite,
            "the children's |W| least / largest where the plane stood at nothing (the charge's magnitude, one e for every row: MS-S1)": [
                sizes[0],
                sizes[-1],
            ]
            if sizes
            else None,
            "children laid on a residue of their plane (W the Node's, not the lay's)": residue,
            "at": births[0]["node"] if births else None,
            "verdict": verdict,
        }
    }


def conservation_at_click(record: Record) -> dict[str, Any]:
    """Gate 15: the conservation at the click, taken against booked over the births (the identity taken >= booked on every birth; the exact form is row 47)."""
    births, (taken, booked) = record.births, record.takes_of()
    exact = all(b["taken"] >= b["booked"] for b in births)
    return {
        "15 conservation at the click": {
            "births": len(births),
            "taken per booked at the births (hundredths)": quot(taken, booked, HUNDRED),
            "verdict": "NOT READ: no birth in the record"
            if not births
            else "SHOWN as the identity taken >= booked on every birth; NOT SHOWN exact (the excess below one level of light)"
            if exact
            else "NOT SHOWN",
        }
    }


def halves(pairs: list[tuple[int, Any]]) -> tuple[list[Any], list[Any]]:
    """The values split at the middle key, shallow and deep."""
    med = sorted(p[0] for p in pairs)[len(pairs) // HALF]
    return [p[1] for p in pairs if p[0] <= med], [p[1] for p in pairs if p[0] > med]


def dilation(record: Record) -> dict[str, Any]:
    """Gate 10: a body's proper count against the intervals it stood, deep against shallow (the reader's view)."""
    decoded = solved(record)[0]
    if len(decoded) <= FEW:
        return {"10 gravitational time dilation": {"verdict": "NOT READ: too few credits decoded"}}
    deepest = max(decoded, key=lambda d: int(d[0]["content"]))[0]["node"]
    lo, hi = halves([(c["content"], (c["proper"], c["i"])) for c, _n, _x in decoded])
    rate_lo = (sum(p for p, _i in lo), sum(i for _p, i in lo))
    rate_hi = (sum(p for p, _i in hi), sum(i for _p, i in hi))
    shown = (
        "SHOWN in the reader's view"
        if cmp_rat(rate_hi, rate_lo) < 0
        else "NOT SHOWN in the reader's view"
    )
    return {
        "10 gravitational time dilation": {
            "reader's view: proper per thousand intervals, shallow / deep": [
                quot(*rate_lo, THOUSAND),
                quot(*rate_hi, THOUSAND),
            ],
            "at": deepest,
            "verdict": shown
            + "; NOT READ in the one-place view: two bodies' clocks compare only through the gap-0 plane between them (gate 7)",
        }
    }


def lengthening(record: Record) -> dict[str, Any]:
    """Gate 2: the spacing of a body's credits longer where the content is deeper (the reader's view)."""
    by_node: dict[tuple[int, ...], list[dict[str, Any]]] = defaultdict(list)
    for c in record.credits:
        by_node[tuple(c["node"])].append(c)
    spans = []
    longest: tuple[int, Any] = (0, [])
    for at, cs in by_node.items():
        cs.sort(key=lambda c: int(c["i"]))
        spans += [
            ((a["content"] + b["content"]) // HALF, b["i"] - a["i"])
            for a, b in zip(cs, cs[1:], strict=False)
            if b["i"] > a["i"]
        ]
        span = max((b["i"] - a["i"] for a, b in zip(cs, cs[1:], strict=False)), default=0)
        longest = max(longest, (span, list(at)), key=lambda p: p[0])
    key = "2 the Links lengthening in the clicks"
    if len(spans) <= SPANS:
        return {key: {"verdict": "NOT READ: too few spans between a Node's credits"}}
    lo, hi = halves(spans)
    shallow, deep = quot(sum(lo), len(lo), HUNDRED), quot(sum(hi), len(hi), HUNDRED)
    shown = (
        "SHOWN in the reader's view"
        if deep is not None and shallow is not None and deep > shallow
        else "NOT SHOWN in the reader's view"
    )
    return {
        key: {
            "reader's view: spans": len(spans),
            "spacing in hundredths of a board interval, shallow / deep": [shallow, deep],
            "at": longest[1],
            "verdict": shown
            + "; NOT READ in the one-place view (the gap-0 plane between two bodies, gate 7)",
        }
    }


def merger(record: Record) -> dict[str, Any]:
    """Row 24 (the Boss's 6400767119, the premise reader): the merger, a pair into light, from the log: a gapped record's meeting (SL-S1: both ends whole, the current's end, the twist) births the gap-0 record's children from the gapped record's take, so a birth whose taken row is a gapped record is a merger; the gapped meetings refused by name counted per cause (the orientation F = 0, the twist h = 0, the sense where the ends' charges are not opposite (SL-S2), the lay where the gap-0 record stands, the stop where an end cannot pay)."""
    gap0 = record.line_num.index(record.den)
    mergers = [b for b in record.births if int(b.get("taken_row", gap0)) != gap0]
    refusals: Counter[str] = Counter(
        e["cause"] for e in record.log if e["event"] == "refused" and int(e.get("row", gap0)) != gap0
    )
    reached = len(mergers) + sum(refusals.values())
    return {
        "24 the merger (a pair into light)": {
            "births taken from a gapped record (a pair into light)": len(mergers),
            "gapped meetings refused by cause": dict(refusals),
            "verdict": unread_words(
                "no gapped record's meeting in the record",
                "two conjugate records' credits ending at one Node with the gap-0 line rising there by their quanta, the charge kept",
            )
            if not reached
            else f"SHOWN: {len(mergers)} pairs into light (the gap-0 children born from a gapped record's take)"
            if mergers
            else f"NOT SHOWN: {reached} gapped meetings reached the premise and every one was refused by name",
        }
    }


def horizon_radiates(record: Record) -> dict[str, Any]:
    """Row 61: the horizon radiates (hp2's predicate, the Boss's 6408295798, the owner's word of 03:4x UTC: Hawking's radiation as nature looks in the clicks): after a Node's first freeze, a birth at that Node or at one of its six neighbours, and a credit two or more Links from every frozen Node (the radiation leaving the horizon); NOT READ with no frozen Node."""
    first: dict[int, int] = {}
    for line in record.nodes:
        for at in line["frozen"]:
            first.setdefault(at, int(line["i"]))
    if not first:
        return {
            "61 the horizon radiates": {
                "verdict": unread_words(
                    "no frozen Node in the record (as gate 14)",
                    "a birth at a frozen Node or its neighbour after its freeze, with a credit two or more Links from every frozen Node",
                )
            }
        }
    near = {at: i for at, i in first.items()} | {
        n: i for at, i in first.items() for n in neighbours(record, at)
    }
    births = [b for b in record.births if int(b["i"]) > near.get(record.index(b["node"]), int(b["i"]))]
    far = [
        c
        for c in record.credits
        if int(c["i"]) > min(first.values())
        and all(record.distance(tuple(c["node"]), tuple(record.node(at))) >= PAIR for at in first)
    ]
    return {
        "61 the horizon radiates": {
            "Nodes frozen": len(first),
            "births at a frozen Node or its neighbour after the freeze": len(births),
            "credits two or more Links from every frozen Node after the first freeze": len(far),
            "at": list(births[0]["node"]) if births else None,
            "verdict": f"SHOWN: a birth at the horizon and a credit beyond it, {len(births)} births and {len(far)} credits"
            if births and far
            else f"NOT SHOWN: {len(births)} births at a frozen Node or its neighbour after the freeze, {len(far)} credits beyond the horizon",
        }
    }
