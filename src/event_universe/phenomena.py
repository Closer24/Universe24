"""The four phenomena of the owner's words of 2026-10-27, 14:32 and 15:1x UTC, read on the one big bang after the chimes (the polarization of light, nuclear binding and fusion, temperature and the equipartition of energy, the baryon as a shape): each row one function of the chart with its verdict and its numbers, as gates.py's rows; the nuclear rows read the held field (DAVID-MEDIATOR.md, the owner's yes to the nuclear family through the Boss's recommendation), the baryon's the colour the universe would need (DAVID-FOUR-PHENOMENA.md section 4, the owner's word to wait)."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from typing import Any

from event_universe import predicates, swings
from event_universe.core import rule3
from event_universe.core.rates import sine_rim
from event_universe.core.spokes import AXES
from event_universe.reckoner import (
    HALF,
    LISTED,
    PAIR,
    QUARTERS,
    THOUSAND,
    Chart,
    carries,
    sign,
    unread_words,
)


def held_fields(chart: Chart) -> list[dict[str, Any]]:
    """The universe's held fields: its rows of one gear with a weight."""
    return [r for r in chart.run["universe"]["rows"] if int(r["shape"]) == 1 and "weight" in r]


def matter_by_tick(chart: Chart) -> dict[int, dict[int, set[tuple[int, ...]]]]:
    """The clocks chiming matter at every tick, line by line: the chimes on a line whose pinion stands below the rim."""
    found: dict[int, dict[int, set[tuple[int, ...]]]] = defaultdict(lambda: defaultdict(set))
    for c in chart.chimes:
        if chart.gear_pinion[int(c["line"])] != chart.rim:
            found[int(c["line"])][int(c["i"])].add(tuple(c["node"]))
    return found


def board_share(chart: Chart) -> tuple[int, int]:
    """The board's own share of clocks one mesh from a clock: the clocks one mesh from the first clock, and the board's other clocks."""
    origin = tuple(chart.clock(0))
    every = [tuple(chart.clock(i)) for i in range(chart.cube**AXES)]
    return sum(1 for c in every if chart.distance(origin, c) == 1), len(every) - 1


def well_at_matter(chart: Chart, by_tick: dict[int, set[tuple[int, ...]]]) -> tuple[int, int]:
    """The matter's chimes in the held field's well: of the matter's chimes whose tick has a clock line with the field, those whose clock's field stands above the board's mean at that tick (by cross multiplication), and all of them."""
    lines = {int(line["i"]): line["field"] for line in chart.clocks if "field" in line}
    deeper = read = 0
    for i, clocks in by_tick.items():
        field = lines.get(i)
        if field is None:
            continue
        total = sum(int(x) for x in field)
        for at in clocks:
            read += 1
            deeper += int(field[chart.index(at)]) * len(field) > total
    return deeper, read


def laid_pairs(chart: Chart) -> dict[int, set[tuple[tuple[int, ...], ...]]]:
    """A fitting's own two children, line by line: the two clock-nodes a birth laid one hand at, its - end and its + end, where the hand is its own twin."""
    found: dict[int, set[tuple[tuple[int, ...], ...]]] = defaultdict(set)
    for b in (b for b in chart.fittings if "plus_hand" not in b):
        found[int(b["line_pair"])].add(tuple(sorted((tuple(b["minus"]), tuple(b["plus"])))))
    return found


def bound_pairs(
    chart: Chart, by_tick: dict[int, set[tuple[int, ...]]], laid: set[tuple[tuple[int, ...], ...]]
) -> tuple[int, int]:
    """Of the distinct pairs of clock-nodes chiming one line at one tick, each counted once and a fitting's own two children left out (David's DAVID-THE-MIRRORS-FITTING.md: the former count read the children chiming where laid, at every tick), those one mesh apart, and all of them."""
    distinct = {p for clocks in by_tick.values() for p in combinations(sorted(clocks), PAIR)} - laid
    return sum(1 for a, b in distinct if chart.distance(a, b) == 1), len(distinct)


def nuclear_binding(chart: Chart) -> dict[str, Any]:
    """Row 76: nuclear binding and fusion: with a held field in the universe, a family's chimes stand bound one mesh apart (of the distinct pairs of clock-nodes chiming its line at one tick, a fitting's own two children left out, the owner's yes of 2026-10-28, 02:2x UTC, the share one mesh apart above twice the board's own, by cross multiplication) in the field's well (most of its chimes at a clock whose field stands above the board's mean); NOT READ with no held field or no two clocks chiming one family at one tick; fusion NOT READ, no act joining two bound bobs into one (the merger's book first, DAVID-CLOSE-LAW.md item 2)."""
    fields, lines, laid = held_fields(chart), matter_by_tick(chart), laid_pairs(chart)
    neighbours, others = board_share(chart)
    found = {}
    for line, by_tick in sorted(lines.items()):
        near, pairs = bound_pairs(chart, by_tick, laid[line])
        deeper, read = well_at_matter(chart, by_tick)
        found[chart.gear_name[line]] = [near, pairs, deeper, read]
    bound = [
        name
        for name, (near, pairs, deeper, read) in found.items()
        if near * others > PAIR * neighbours * pairs and deeper * HALF > read
    ]
    if not fields:
        verdict = "NOT READ: no held field in the universe (a row of one gear with its weight)"
    elif not any(pairs for _near, pairs, _d, _r in found.values()):
        verdict = "NOT READ: no two clocks chiming one family at one tick"
    elif bound:
        verdict = f"SHOWN: {', '.join(bound)} chime bound one mesh apart in the held field's well, above twice the board's own share {neighbours} of {others}"
    else:
        verdict = f"NOT SHOWN: no family chimes bound one mesh apart in the held field's well above twice the board's own share {neighbours} of {others}"
    return {
        "76 nuclear binding and fusion": {
            "held fields (pair, weight)": [[r["pair"], r["weight"]] for r in fields],
            "by family: distinct pairs one mesh apart, distinct pairs, chimes in the field's well, chimes read": found,
            "the board's own share one mesh from a clock": [neighbours, others],
            "fusion": "NOT READ: no act joins two bound bobs into one (the merger's book first, DAVID-CLOSE-LAW.md item 2)",
            "verdict": verdict,
        }
    }


def baryon_shape(chart: Chart) -> dict[str, Any]:
    """Row 77: the baryon as a shape: NOT READ while the universe holds no colour: a third of the charge, a triplet of hands read from a train of six gears, the gluons' eight-gear train and the chime of a colour-neutral triple are new families and sentences (DAVID-FOUR-PHENOMENA.md section 4; the owner's word through the Boss's recommendation: wait)."""
    sizes = sorted({int(r["shape"]) for r in chart.run["universe"]["rows"]})
    return {
        "77 the baryon as a shape": {
            "the universe's row sizes": sizes,
            "verdict": "NOT READ: the universe holds no colour (a triplet of hands, the gluons' eight-gear train and the neutral chime are new families and sentences, DAVID-FOUR-PHENOMENA.md section 4)",
        }
    }


def face_light(chart: Chart) -> dict[tuple[int, int], list[int]]:
    """The light on each axis at every chimed clock and tick, from the chime's face: the face's odd sums at the axis's two spokes, odd[+b] - odd[-b] = A_b(clock + b) + 2 A_b(clock) + A_b(clock - b), the offset's odd gear b at the tick's start at the clock and its two neighbours along b (bobs.face_of; the same at every hand chiming there), keyed by (the clock's index, the tick)."""
    found: dict[tuple[int, int], list[int]] = {}
    for c in chart.chimes:
        odd = c["frame"]["odd"]
        found[(chart.index(c["node"]), int(c["i"]))] = [
            int(odd[b + b]) - int(odd[b + b + 1]) for b in range(AXES)
        ]
    return found


def kick_tally(chart: Chart) -> tuple[list[list[int]], list[int], list[int]]:
    """The light's answer to the current's kicks at the kicked clock itself: every kick of the clock lines' `kick` (the hands' lead carried at the key on the offset's odd gear a at the tick's impulse) at a clock turned over and stopped at neither the tick nor the one before it (the turnover and the stop return the tick's kick with the pre-state), read on the clock lines' `odd` (the light's three odd gears' momentum at every clock at the tick's end, W (now - before) + fine - mid(W), the impulse's own reading of a stride, where the kick lands; the carry keeps it through the stretch's change, so the stride's rescaling by the wall, which ran against the kick on the axis the bang's wave runs along, is read away exactly, David's DAVID-THE-MERGERS-BOOK.md (a)): sign(kick) times the sign of the odd gear b's momentum change over the tick at the clock. Returns the tally [a][b], the kicks per axis and the kicks read per axis."""
    lines = {int(line["i"]): line for line in chart.clocks if "odd" in line}
    tally = [[0] * AXES for _ in range(AXES)]
    kicked, read = [0] * AXES, [0] * AXES
    for t, line in lines.items():
        before = lines.get(t - 1)
        if before is None:
            continue
        still = {int(k) for each in (line, before) for k in (*each["turned"], *each["frozen"])}
        for a, row in enumerate(line["kick"]):
            for k, q in enumerate(row):
                if int(q) == 0:
                    continue
                kicked[a] += 1
                if k in still:
                    continue
                read[a] += 1
                for b in range(AXES):
                    tally[a][b] += sign(int(q)) * sign(int(line["odd"][b][k]) - int(before["odd"][b][k]))
    return tally, kicked, read


def polarization(chart: Chart) -> dict[str, Any]:
    """Row 74: the polarization of light (David's DAVID-FOUR-PHENOMENA.md section 1, no new law: the photon's polarization is on the offset, the direction of its transverse odd gears, which the hands' current drives): the light's three odd gears are kicked by the current on their own axis alone (the hands' lead carried at the key at the impulse, the clock lines' `kick`), so the light a current lights is polarized along it: at every kick (`kick_tally`) the light's momentum at the kicked clock itself changes on the kick's axis with the kick's sign, and on the other two axes as often against as with it; SHOWN where on every axis with a kick read the own axis's tally is above 0 and above twice each cross tally in size, SHOWN in part where on some, NOT SHOWN where on none; NOT READ where the chart carries no kick or no light at the clocks (the writer's fields) or no kick falls at a clock running through the tick and the one before; beside it the light the chimes see, the faces' light summed per axis with its sign (the polarization seen, the named source's test read with the signs) and in size."""
    lines = chart.clocks
    light = face_light(chart)
    seen = [sum(f[b] for f in light.values()) for b in range(AXES)]
    size = [
        sum(
            abs(int(c["frame"]["odd"][b + b])) + abs(int(c["frame"]["odd"][b + b + 1]))
            for c in chart.chimes
        )
        for b in range(AXES)
    ]
    numbers: dict[str, Any] = {
        "the light at the chimes per axis, with its sign / in size": [seen, size],
    }
    if not lines or "kick" not in lines[0] or "odd" not in lines[0]:
        return {
            "74 the polarization of light": numbers
            | {
                "verdict": unread_words(
                    "the record carries no kick of the light or no light at the clocks (the clock lines' `kick`, the offset's carries of the hands' lead at the impulse, and `odd`, its odd gears)",
                    "at every kick of the light by the current the light's momentum at the kicked clock changes on the kick's axis with its sign, the other axes not",
                )
            }
        }
    tally, kicked, read = kick_tally(chart)
    axes = [a for a in range(AXES) if read[a]]
    along = [
        a
        for a in axes
        if tally[a][a] > 0 and all(PAIR * abs(tally[a][b]) < tally[a][a] for b in range(AXES) if b != a)
    ]
    numbers |= {
        "kicks per axis / read at clocks running through the tick and the one before": [kicked, read],
        "sign(kick on a) sign(the light's momentum change on b), [a][b]": tally,
    }
    words = ", ".join(f"{tally[a][a]} of {read[a]}" for a in axes)
    return {
        "74 the polarization of light": numbers
        | {
            "verdict": unread_words(
                "no kick of the light at a clock running through the tick and the one before it",
                "at every kick of the light by the current the light's momentum at the kicked clock changes on the kick's axis with its sign, the other axes not",
            )
            if not axes
            else f"SHOWN: the light kicked by the current is polarized along it, on every axis kicked: its momentum's change with the kick's sign on {words} kicks read, the cross axes under half of it"
            if len(along) == len(axes)
            else f"SHOWN in part: the light polarized along its kick on {len(along)} of {len(axes)} axes read ({words})"
            if along
            else f"NOT SHOWN: the light's momentum's change not along its kick on any axis read ({words})",
        }
    }


TEMPERATURE = "75 temperature and equipartition"
BALANCE = "every family exchanging at a click holding its wind per mode within a factor two of every other's at the last bang, the temperature their common mean"


def windings_of(chart: Chart) -> list[int]:
    """Every hand's winding as the clock reckons it (clock.windings: rule3.winding_of at the hand's sine, the rim at the spring 0), in the hands' order."""
    rim = chart.rim
    return [
        int(rule3.winding_of(sine_rim(p, rim) + rim * int(rule3.carries(p, rim)), chart.key))
        for p in chart.gear_pinion
    ]


def exchanging(chart: Chart) -> list[int]:
    """The hands that exchange wind at a click, the close being the only exchange between the modes (Rule3 is linear): a chime's hand and the light it unwinds, where the chime books its winding (a chime where nothing arrives is laid back, books nothing and exchanges nothing, CS7-S1), a birth's fitted hands (its line pair, and the plus hand of twin hands) and the hand its take unwinds."""
    light = chart.gear_pinion.index(chart.rim)
    booked = [c for c in chart.chimes if int(c["booked"]) > 0]
    found = {int(c["line"]) for c in booked} | ({light} if booked else set())
    for b in chart.fittings:
        found |= {int(b[k]) for k in ("line_pair", "plus_hand", "taken_row") if k in b}
    return sorted(found)


def temperature(chart: Chart) -> dict[str, Any]:
    """Row 75: temperature and the equipartition of energy (David's DAVID-FOUR-PHENOMENA.md section 2: equipartition needs a conserved wind and an exchange between the modes; Rule3 is linear, so the close is the only exchange). Every hand is a family and its hand at every clock a mode. A family's wind per mode is its wind summed over the clocks at the tick's start over the count of clocks, from the clock lines' `winds` (the striking's own reading, PM-S1's unit). It is read per bang, the spans from the setting and from every exact return to the next (swings.exact_of; the whole run where there is none), in thousandths of the light's winding (rule3.winding_of at the rim: one unit for every family). The families in the balance are those exchanging at a click (`exchanging`). Equipartition is SHOWN where, at the last bang, every such family's wind per mode lies within a factor two of every other's, the temperature their common mean; SHOWN in part where the spread (the largest family's wind per mode over the least's) narrows from the first bang to the last; NOT SHOWN where it does not; NOT READ where no click exchanges wind (no birth, every chime laid back) or on a record without the winds. Beside it, the light's occupation in whole light windings at the credits' clocks by the credit's beat (row 48's predicate in David's words)."""
    per_tick = {
        int(line["i"]): [sum(int(x) for x in w) for w in line["winds"]]
        for line in chart.clocks
        if "winds" in line
    }
    if not per_tick:
        return predicates.unread(
            TEMPERATURE,
            "the record carries no wind of the modes (the clock lines' winds: the striking's wind of every hand at every clock at the tick's start)",
            BALANCE,
        )
    families = exchanging(chart)
    if len(families) < PAIR:
        return predicates.unread(
            TEMPERATURE,
            "no click of the record exchanges wind between the families (no birth, no chime booking its winding)",
            BALANCE,
        )
    lines = {int(line["i"]): line for line in chart.clocks if "winds" in line}
    modes = len(next(iter(lines.values()))["winds"][0])
    windings = windings_of(chart)
    light = chart.gear_pinion.index(chart.rim)
    unit = windings[light]
    names = [chart.gear_name[r] for r in families]
    bounds = [1] + [int(i) for i in swings.exact_of(chart)]
    spans = [(a, b) for a, b in zip(bounds, bounds[1:], strict=False) if b > a] or [(1, chart.ticks + 1)]
    sums = []
    for a, b in spans:
        ticks = [i for i in range(a, b) if i in per_tick]
        sums.append(([sum(per_tick[i][r] for i in ticks) for r in families], len(ticks) * modes))

    def means(k: int) -> list[int | None]:
        found, count = sums[k]
        return [carries(s * THOUSAND, count * unit) for s in found]

    def spread(k: int) -> tuple[int, int]:
        found, _count = sums[k]
        return max(found), min(found)

    first, last = spread(0), spread(-1)
    ratio_first = carries(first[0], first[1]) if first[1] > 0 else None
    ratio_last = carries(last[0], last[1]) if last[1] > 0 else None
    quarter = [means(k) for k in range(len(spans) - max(1, len(spans) // QUARTERS), len(spans))]
    by_beat: dict[int, list[int]] = {}
    for c in chart.chimes:
        line = lines.get(int(c["i"]))
        if line is not None:
            s, n = by_beat.get(int(c["beat"]), [0, 0])
            by_beat[int(c["beat"])] = [s + int(line["winds"][light][chart.index(c["node"])]), n + 1]
    found_last, count_last = sums[-1]
    if last[1] > 0 and last[0] <= PAIR * last[1]:
        common = carries(sum(found_last) * THOUSAND, len(families) * count_last * unit)
        verdict = f"SHOWN: the {len(families)} families exchanging at the clicks hold their wind per mode within a factor two of one another at the last bang, the temperature their common mean, {common} thousandths of the light's winding per mode"
    elif ratio_first is not None and ratio_last is not None and last[0] * first[1] < first[0] * last[1]:
        verdict = f"SHOWN in part: the families' spread narrows from {ratio_first} at the first bang to {ratio_last} at the last (the largest wind per mode over the least), no common mean"
    else:
        verdict = f"NOT SHOWN: no common temperature, the largest family's wind per mode {ratio_last if ratio_last is not None else 'unbounded over a family at no wind'} times the least's at the last bang ({ratio_first} at the first)"
    return {
        TEMPERATURE: {
            "families exchanging at the clicks": names,
            "bangs read (the spans between the exact returns)": len(spans),
            "wind per mode at the first and the last bang (thousandths of the light's winding)": {
                name: [a, b] for name, a, b in zip(names, means(0), means(-1), strict=True)
            },
            "wind per mode at the last bang in the family's own windings (the occupation)": {
                name: carries(s, count_last * windings[r])
                for name, r, s in zip(names, families, found_last, strict=True)
            },
            "course per bang at every eighth (the bang's first interval, the families' wind per mode)": [
                [spans[k][0], means(k)] for k in range(0, len(spans), max(1, len(spans) // LISTED))
            ],
            "least and largest wind per mode over the last quarter of the bangs": {
                name: [min(m[j] or 0 for m in quarter), max(m[j] or 0 for m in quarter)]
                for j, name in enumerate(names)
            },
            "the last bang per interval (the families' wind per mode)": [
                [i, [carries(per_tick[i][r] * THOUSAND, modes * unit) for r in families]]
                for i in range(*spans[-1])
                if i in per_tick
            ],
            "the light's occupation at the credits' Nodes by the credit's beat (whole light windings, the mean)": {
                beat: carries(s, n * unit) for beat, (s, n) in sorted(by_beat.items())
            },
            "the spread (the largest wind per mode over the least) at the first and the last bang": [
                ratio_first,
                ratio_last,
            ],
            "verdict": verdict,
        }
    }
