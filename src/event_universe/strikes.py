"""The gates read from the strikes (the chime and the fitting lines), one function per row of UNIVERSE24's table: 2 the meshes lengthening in the strikes, 8 families forming and 8b the species over a bob's track, 10 the dilation in the reader's view, 15 the conservation at the strike, 16 the one-strike floor, 17 the charge, 19 the mass ratios in the strikes and 24 the unspringing from the fittings' unwound train and the sprung engagements' jams; the species reckoned by reckoner.py, memoized per chart."""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import cmp_to_key
from typing import Any

from event_universe.core.rates import sine_rim
from event_universe.great_clock import neighbours
from event_universe.reckoner import (
    FEW,
    HALF,
    HUNDRED,
    MIL,
    PAIR,
    SPANS,
    THOUSAND,
    Chart,
    Rational,
    carries,
    cmp_rat,
    middle,
    nearest,
    reckoned_chimes,
    unread_words,
)

Reckoned = list[tuple[dict[str, Any], str, Rational]]


def reckoned(chart: Chart) -> tuple[Reckoned, int, int, list[int | None]]:
    """The chart's chimes reckoned once per cut: the reckoned (chime, name, x), the count read right, the count within the floor, each chime's floor."""
    key = f"solved {chart.ticks} {len(chart.chimes)}"
    if key not in chart.memo:
        chart.memo[key] = reckoned_chimes(chart)
    found: tuple[Reckoned, int, int, list[int | None]] = chart.memo[key]
    return found


def tracks_of(
    chart: Chart,
) -> tuple[dict[tuple[Any, int], list[Rational]], int, Counter[tuple[str, str]]]:
    """A bob's track, its reckoned rationals by (clock, gear), the tracks read right by the middle reckoning, and the confusion truth -> reckoned per chime."""
    reckoning = reckoned(chart)[0]
    tracks: dict[tuple[Any, int], list[Rational]] = defaultdict(list)
    confusion: Counter[tuple[str, str]] = Counter()
    for c, name, x in reckoning:
        tracks[(tuple(c["node"]), c["line"])].append(x)
        confusion[(chart.gear_name[c["line"]], name)] += 1
    right = 0
    for (_clock, gear), xs in tracks.items():
        xs.sort(key=cmp_to_key(cmp_rat))
        right += nearest(chart, middle(xs), 1) == chart.gear_name[gear]
    return tracks, right, confusion


def species_track(chart: Chart) -> dict[str, Any]:
    """Row 8b: the species over a bob's track (the one-place view: the middle reckoning of the track's rationals)."""
    tracks, right, confusion = tracks_of(chart)
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


def families(chart: Chart) -> dict[str, Any]:
    """Gate 8: the species from the face of every chime (the whole view), every chime within the one-strike floor and every track read right, every lift the calibre names fitted (its sprung hands, the typed points of the rim's circle; the former constant 3 the toy calibre's count)."""
    reckoning, right, within, _floors = reckoned(chart)
    tracks, track_right, _confusion = tracks_of(chart)
    fitted = chart.fitted_of()
    if not reckoning:
        verdict = "NOT READ: no credit in the record"
    elif (
        within == len(reckoning) and track_right == len(tracks) and len(chart.lifts_fitted()) >= chart.NL
    ):
        verdict = "SHOWN (every credit within the one-click floor, every track read right)"
    elif within == len(reckoning):
        verdict = (
            f"SHOWN in part: every credit within the floor, tracks right {track_right} of {len(tracks)}"
        )
    else:
        verdict = f"NOT SHOWN: {len(reckoning) - within} credits beyond the floor"
    return {
        "8 families forming (whole view)": {
            "credits": len(chart.chimes),
            "species readable": len(reckoning),
            "decoded right per credit": right,
            "credits within the one-click floor": within,
            "tracks right": [track_right, len(tracks)],
            "births by species (decoder)": dict(fitted),
            "at": min(chart.chimes, key=lambda c: int(c["i"]))["node"] if chart.chimes else None,
            "verdict": verdict,
        }
    }


def leg_of(chart: Chart, x: Rational) -> int:
    """The leg of a reckoned rational x = pinion / rim on the rim's circle, sine_rim at the nearest integer pinion, 0 off the circle (|pinion| at or past the rim)."""
    pinion = abs(carries(x[0] * chart.rim, x[1]) or 0)
    return sine_rim(pinion, chart.rim) if pinion < chart.rim else 0


def mass_ratios(chart: Chart) -> dict[str, Any]:
    """Gate 19: the mass ratios in the strikes (MS-S1's predicate: per chimed hand the middle reckoning of its tracks' middles, its leg against the header's, the ratio of the two heaviest chimed hands' legs read right within the one-strike floor; NOT SHOWN where one hand alone is chimed) beside the rim's typed legs and the rim's circle."""
    reckoning, _right, _within, floor_mil = reckoned(chart)
    tracks, _track_right, _confusion = tracks_of(chart)
    names, gear_pinion = chart.NAMES, chart.gear_pinion
    legs = sorted(((name, leg) for name, leg in names.values() if leg), key=lambda kv: kv[1])
    found: dict[str, Any] = {f"{nm}/{legs[0][0]}": carries(leg, legs[0][1], MIL) for nm, leg in legs[1:]}
    by_hand: dict[int, list[Rational]] = defaultdict(list)
    for (_clock, gear), xs in tracks.items():
        by_hand[gear_pinion[gear]].append(middle(xs))
    chimed = sorted(
        (hand for hand in by_hand if hand != chart.rim), key=lambda hand: sine_rim(hand, chart.rim)
    )
    read_legs = {
        hand: leg_of(chart, middle(sorted(by_hand[hand], key=cmp_to_key(cmp_rat)))) for hand in chimed
    }
    for hand in chimed:
        found[f"{names[hand][0]} leg in the clicks / header (parts per million)"] = carries(
            read_legs[hand], sine_rim(hand, chart.rim) or 1, MIL
        )
    if len(chimed) < PAIR:
        read = (
            f"NOT SHOWN: {len(chimed)} plane credited, a ratio needs two"
            if reckoning
            else "NOT READ: no credit decoded"
        )
    else:
        heavy, light = chimed[-1], chimed[-PAIR]
        strikes = carries(read_legs[heavy], read_legs[light], MIL) if read_legs[light] else None
        header = carries(sine_rim(heavy, chart.rim), sine_rim(light, chart.rim), MIL)
        floors = [f for f in floor_mil if f is not None]
        found["the two heaviest credited planes' legs: clicks / header (parts per million)"] = [
            strikes,
            header,
        ]
        read = (
            "SHOWN: the mass ratio in the clicks reads the header's within the one-click floor"
            if strikes is not None and header is not None and abs(strikes - header) <= max(floors or [0])
            else "NOT SHOWN: the lighter plane's leg in the clicks is 0 (below the floor)"
            if strikes is None
            else "NOT SHOWN: the ratio in the clicks is off the header's beyond the floor"
        )
    points = chart.rim_points()
    least = min((s for _hand, s in points), default=0)
    found[
        "den's circle: the points' legs over the least (parts per million), the typed among them marked"
    ] = [[carries(s, least, MIL), hand in chart.NAMES] for hand, s in sorted(points, key=lambda p: p[1])]
    return {"19 mass ratios (parts per million)": found | {"verdict": read}}


def one_strike_floor(chart: Chart) -> dict[str, Any]:
    """Gate 16: the one-strike floor on x per chime (the uncertainty floor), no chime reading beyond it."""
    reckoning, _right, within, floor_mil = reckoned(chart)
    fl = sorted(f for f in floor_mil if f is not None)
    if not fl:
        return {"16 uncertainty floor (one click)": {"verdict": "NOT READ: no credit decoded"}}
    names = chart.NAMES
    legs = sorted(((pinion, leg) for pinion, (_name, leg) in names.items() if leg), key=lambda kv: kv[1])
    spacing = carries(abs(legs[-1][0] - legs[-PAIR][0]), legs[-1][0], MIL) if len(legs) >= PAIR else None
    return {
        "16 uncertainty floor (one click)": {
            "floor on x per credit, parts per million: min / middle / max": [
                fl[0],
                fl[len(fl) // HALF],
                fl[-1],
            ],
            "species spacing of the two heaviest, parts per million": spacing,
            "credits beyond the floor": len(reckoning) - within,
            "verdict": "SHOWN as the law's floor: no credit reads beyond it"
            if within == len(reckoning)
            else "NOT SHOWN",
        }
    }


def charge(chart: Chart) -> dict[str, Any]:
    """Gate 17: the charge (each fitted hand's own sweep, its sense times half the key at a fitted hand's advance and 0 at an exact advance, Chart.sweeps_of, summed over every fitting, each pair opposite, an unspringing's two fitted hands 0 and 0 by MG-S1 and read by name; its magnitude one |sweep| on every fitted hand advanced where its hand stood at nothing, MS-S1, the fitted hands advanced on a residue counted by name; an unspringing's fitting (MG-S1, a pair at rest into light, the line carrying its unwinds per end) counted apart, the light's charge 0 and its reading row 24's)."""
    unspringings = [b for b in chart.fittings if "takes" in b]
    fittings = [b for b in chart.fittings if "takes" not in b]
    sweeps, signs = chart.sweeps_of(), chart.signs_of()
    pair_signs = [
        s for b, pair in zip(chart.fittings, sweeps, strict=True) if "takes" not in b for s in pair
    ]
    sizes = sorted(chart.advanced_at_nothing())
    residue = sum(1 for b in fittings for stood in b.get("stood", [[0], [0]]) if any(stood))
    sense_sum, summed = sum(signs), sum(a + c for a, c in sweeps)
    opposite = sum(1 for a, c in sweeps if a * c < 0)
    light = sum(
        1 for b, pair in zip(chart.fittings, sweeps, strict=True) if "takes" in b and pair == (0, 0)
    )
    verdict = (
        "NOT READ: no birth in the record"
        if not chart.fittings
        else "SHOWN: the senses sum to 0 over every birth, each pair opposite, each merger's children 0 and 0"
        if sense_sum == 0 and 0 not in pair_signs and light == len(unspringings)
        else f"NOT SHOWN: the children's own charges sum to {summed} over the births, {len(unspringings) - light} mergers with a charged child"
    ) + (
        "; the magnitude SHOWN: one |W| on every child laid where its plane stood at nothing"
        if sizes and sizes[0] == sizes[-1]
        else "; the magnitude NOT SHOWN: |W| differs between the children laid where their plane stood at nothing"
        if sizes
        else "; the magnitude NOT READ"
    )
    return {
        "17 charge conservation": {
            "senses sum over births (the children's own charges' signs)": sense_sum,
            "children's own charges summed over every birth": summed,
            "children with no charge (laid as light, the exact take at -1)": signs.count(0),
            "births with the two children at opposite signs": opposite,
            "the children's |W| least / largest where the plane stood at nothing (the charge's magnitude, one e for every row: MS-S1)": [
                sizes[0],
                sizes[-1],
            ]
            if sizes
            else None,
            "children laid on a residue of their plane (W the Node's, not the lay's)": residue,
            "mergers, a pair into light (MG-S1), and those whose two children carry 0 and 0": [
                len(unspringings),
                light,
            ],
            "at": fittings[0]["node"] if fittings else None,
            "verdict": verdict,
        }
    }


def conservation_at_strike(chart: Chart) -> dict[str, Any]:
    """Gate 15: the conservation at the strike, unwound against tallied over the fittings: where the fitting carries the unwind's slack (EX-S1, the slack kept at the clock) the identity unwound + the slack before - the slack after = tallied on every fitting, else the former identity unwound >= tallied (the exact form is row 47)."""
    fittings, (unwound, tallied) = chart.fittings, chart.unwinds_of()
    paid = [b for b in fittings if "remainder" in b]
    identity = all(
        b["taken"] + b["remainder_was"] - b["remainder"] == b["booked"] for b in paid
    ) and all(b["taken"] >= b["booked"] for b in fittings if "remainder" not in b)
    return {
        "15 conservation at the click": {
            "births": len(fittings),
            "births carrying the take's remainder (EX-S1)": len(paid),
            "taken per booked at the births (hundredths)": carries(unwound, tallied, HUNDRED),
            "verdict": "NOT READ: no birth in the record"
            if not fittings
            else "SHOWN exact: taken + the remainder before - the remainder after = booked on every birth (EX-S1)"
            if identity and len(paid) == len(fittings)
            else "SHOWN: taken + the remainder before - the remainder after = booked on every birth carrying the remainder (EX-S1), taken >= booked on the rest (the mergers' ends)"
            if identity and paid
            else "SHOWN as the identity taken >= booked on every birth; NOT SHOWN exact (the excess below one level of light)"
            if identity
            else "NOT SHOWN",
        }
    }


def halves(pairs: list[tuple[int, Any]]) -> tuple[list[Any], list[Any]]:
    """The values split at the middle key, shallow and deep."""
    med = sorted(p[0] for p in pairs)[len(pairs) // HALF]
    return [p[1] for p in pairs if p[0] <= med], [p[1] for p in pairs if p[0] > med]


def dilation(chart: Chart) -> dict[str, Any]:
    """Gate 10: a bob's dial against the ticks it stood, deep against shallow (the reader's view)."""
    reckoning = reckoned(chart)[0]
    if len(reckoning) <= FEW:
        return {"10 gravitational time dilation": {"verdict": "NOT READ: too few credits decoded"}}
    deepest = max(reckoning, key=lambda d: int(d[0]["content"]))[0]["node"]
    lo, hi = halves([(c["content"], (c["proper"], c["i"])) for c, _n, _x in reckoning])
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
                carries(*rate_lo, THOUSAND),
                carries(*rate_hi, THOUSAND),
            ],
            "at": deepest,
            "verdict": shown
            + "; NOT READ in the one-place view: two bodies' clocks compare only through the gap-0 plane between them (gate 7)",
        }
    }


def lengthening(chart: Chart) -> dict[str, Any]:
    """Gate 2: the spacing of a bob's chimes longer where the load is deeper (the reader's view)."""
    by_clock: dict[tuple[int, ...], list[dict[str, Any]]] = defaultdict(list)
    for c in chart.chimes:
        by_clock[tuple(c["node"])].append(c)
    spans = []
    longest: tuple[int, Any] = (0, [])
    for at, cs in by_clock.items():
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
    shallow, deep = carries(sum(lo), len(lo), HUNDRED), carries(sum(hi), len(hi), HUNDRED)
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


def unspring(chart: Chart) -> dict[str, Any]:
    """Row 24 (the Boss's 6400767119, the premise reader): the unspringing, a pair into light, from the log: a sprung hand's engagement (SL-S1: both ends whole, the lead's end, the twist) fits the unsprung hand's fitted hands from the sprung hand's unwind, so a fitting whose unwound train is a sprung hand is an unspringing; the sprung engagements jammed by name counted per cause (the orientation F = 0, the twist h = 0, the sense where the ends' sweeps are not opposite (SL-S2), the advance where the unsprung hand stands, the stop where an end cannot pay)."""
    light = chart.gear_pinion.index(chart.rim)
    unspringings = [b for b in chart.fittings if int(b.get("taken_row", light)) != light]
    jams: Counter[str] = Counter(
        e["cause"] for e in chart.log if e["event"] == "refused" and int(e.get("row", light)) != light
    )
    reached = len(unspringings) + sum(jams.values())
    return {
        "24 the merger (a pair into light)": {
            "births taken from a gapped record (a pair into light)": len(unspringings),
            "gapped meetings refused by cause": dict(jams),
            "verdict": unread_words(
                "no gapped record's meeting in the record",
                "two conjugate records' credits ending at one Node with the gap-0 line rising there by their quanta, the charge kept",
            )
            if not reached
            else f"SHOWN: {len(unspringings)} pairs into light (the gap-0 children born from a gapped record's take)"
            if unspringings
            else f"NOT SHOWN: {reached} gapped meetings reached the premise and every one was refused by name",
        }
    }


def horizon_radiates(chart: Chart) -> dict[str, Any]:
    """Row 61: the horizon radiates (hp2's predicate, the Boss's 6408295798, the owner's word of 03:4x UTC: Hawking's radiation as nature looks in the clicks): after a clock's first stop, a fitting at that clock or at one of its six neighbours, and a chime two or more meshes from every clock stopped at the chime's own tick, the horizon standing then (the Reader's form of 6416667138 for the great clock stopped at every clock, the Boss's 6416342006: no chime passes while the whole great clock is the horizon, and the chimes after a release are beyond the horizon as it shrinks; the former read against every clock ever stopped); NOT READ with no stopped clock."""
    first = chart.first_stopped()
    if not first:
        return {
            "61 the horizon radiates": {
                "verdict": unread_words(
                    "no frozen Node in the record (as gate 14)",
                    "a birth at a frozen Node or its neighbour after its freeze, with a credit two or more Links from every Node frozen at the credit's interval",
                )
            }
        }
    near = {at: i for at, i in first.items()} | {
        n: i for at, i in first.items() for n in neighbours(chart, at)
    }
    fittings = [b for b in chart.fittings if int(b["i"]) > near.get(chart.index(b["node"]), int(b["i"]))]
    stopped = {int(line["i"]): [int(at) for at in line["frozen"]] for line in chart.clocks}
    far = [
        c
        for c in chart.chimes
        if int(c["i"]) > min(first.values())
        and all(
            chart.distance(tuple(c["node"]), tuple(chart.clock(at))) >= PAIR
            for at in stopped.get(int(c["i"]), [])
        )
    ]
    released = sum(1 for c in far if not stopped.get(int(c["i"])))
    whole = any(len(ats) == len(chart.clocks[0]["X"]) for ats in stopped.values())
    return {
        "61 the horizon radiates": {
            "Nodes frozen": len(first),
            "the whole board frozen at once": whole,
            "births at a frozen Node or its neighbour after the freeze": len(fittings),
            "credits two or more Links from every Node frozen at the credit's interval": len(far),
            "of them after the whole board's release (no Node frozen at the interval)": released,
            "at": list(fittings[0]["node"]) if fittings else None,
            "verdict": f"SHOWN: a birth at the horizon and a credit beyond it, {len(fittings)} births and {len(far)} credits"
            if fittings and far
            else f"NOT SHOWN: {len(fittings)} births at a frozen Node or its neighbour after the freeze, {len(far)} credits beyond the horizon standing at the credit's interval",
        }
    }
