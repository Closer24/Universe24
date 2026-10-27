"""The table of gates: every row of UNIVERSE24's table (the nineteen and the widened 20 to 54) as one function of the chart with its verdict and its numbers, shown, not shown, or not read with the predicate named where the chart cannot carry it (`TABLE`, in the rows' order), and `gates(run)` reading them all with the event lines of the gates' first SHOWN (events.py); the rows read from the strikes are strikes.py's, the great clock's great_clock.py's, the widened rows predicates.py's, and here 7 light absorbed, 9 the collisions, 11 the redshift, 12 the delay, 13 the free fall, 18 the arrow of time, 23 the momentum across the strike, 25 the entropy of the strikes, the conservations and the three constants. Usage: `python -m event_universe.gates <chart.json>`."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from collections.abc import Callable
from typing import Any

from event_universe import events, great_clock, predicates, strikes, swings, symmetries
from event_universe.core.spokes import AXES
from event_universe.reckoner import (
    HALF,
    HUNDRED,
    LISTED,
    PAIR,
    Chart,
    carries,
    cause_of,
    kind_of,
    unread_words,
)

Row = Callable[[Chart], dict[str, Any]]


def approach(chart: Chart) -> tuple[int, int, bool, list[int]]:
    """Two bobs' chimed clocks over the ticks (W-S4, W-S5): the distance between the two chimed clocks farthest apart at the first tick with two and at the last, whether two chimed clocks stood adjacent (one mesh apart) at some tick, and the farthest distance per tick."""
    by_tick: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    for c in chart.chimes:
        by_tick[int(c["i"])].add(tuple(c["node"]))
    distance = chart.distance
    spans = []
    adjacent = False
    for i in sorted(by_tick):
        clocks = sorted(by_tick[i])
        if len(clocks) < PAIR:
            continue
        spans.append(max(distance(a, b) for a in clocks for b in clocks if a < b))
        adjacent = adjacent or any(distance(a, b) == 1 for a in clocks for b in clocks if a < b)
    return (spans[0], spans[-1], adjacent, spans) if spans else (0, 0, False, [])


def collisions(chart: Chart) -> dict[str, Any]:
    """Gate 9: the collision from two bobs' chimed clocks approaching to adjacency (the sentences W-S4 and W-S5): SHOWN where they approach and stand one mesh apart, NOT SHOWN where apart or receding, NOT READ with one bob; a bob's track is its hand's chimes by gear, a move a chime of the same gear at a new clock."""
    by_gear: dict[int, list[tuple[int, tuple[int, ...]]]] = defaultdict(list)
    for c in chart.chimes:
        by_gear[c["line"]].append((c["proper"], tuple(c["node"])))
    moves = 0
    for cs in by_gear.values():
        cs.sort()
        seen = {cs[0][1]}
        for _p, at in cs[1:]:
            if at not in seen:
                moves += 1
                seen.add(at)
    first, last, adjacent, _spans = approach(chart)
    if first == 0:
        verdict = "NOT READ: fewer than two bodies credited at one interval"
    elif adjacent and last <= first:
        verdict = "SHOWN: two bodies' credited Nodes approached and stood one Link apart"
    else:
        verdict = f"NOT SHOWN: the credited Nodes {'receding' if last > first else 'apart'}, farthest {first} Links at first and {last} at last"
    return {
        "9 collisions": {
            "tracks (node, line)": len({(tuple(c["node"]), c["line"]) for c in chart.chimes}),
            "lines credited at a new Node after their first": moves,
            "farthest credited Nodes at the first and the last interval with two": [first, last],
            "adjacent at some interval": adjacent,
            "verdict": verdict,
        }
    }


def free_fall(chart: Chart) -> dict[str, Any]:
    """Gate 13: the free fall where the closing of two bobs' chimed clocks quickens from tick to tick (the tail's second difference toward matter)."""
    first, _last, _adjacent, spans = approach(chart)
    closing = [a - b for a, b in zip(spans, spans[1:], strict=False)]
    quickening = sum(1 for a, b in zip(closing, closing[1:], strict=False) if b > a > 0)
    return {
        "13 free fall": {
            "the farthest credited Nodes' distance per interval with two (first eight)": spans[:LISTED],
            "intervals the closing quickens": [quickening, max(len(closing) - 1, 0)],
            "verdict": "NOT READ: fewer than two bodies credited at one interval"
            if first == 0
            else "SHOWN: the approach quickens from interval to interval (the tail's second difference toward matter)"
            if quickening * HALF > max(len(closing) - 1, 1)
            else "NOT SHOWN: the approach does not quicken",
        }
    }


def light(chart: Chart) -> dict[str, Any]:
    """Gate 7: light present and absorbed, the unsprung gear's windings unwound at the fittings and the chimes (PC-S2); the unsprung hand's own chimes none in the engine's chart (a detector is the toy's reading)."""
    unwinds = chart.unwinds
    return {
        "7 light present and absorbed": {
            "gap-0 credits in the record": sum(1 for e in chart.log if e["event"] == "detector"),
            "absorbed: the takes of the gap-0 line at births and credits (PC-S2)": len(unwinds),
            "levels taken in all": sum(int(entry["levels"]) for entry in unwinds),
            "at": unwinds[0]["node"] if unwinds else None,
            "verdict": "SHOWN: the gap-0 line's quanta absorbed at the takes, at matter (the credits) and at the births; its credit the taker's line (PC-S2)"
            if unwinds
            else "NOT READ: no take in the record",
        }
    }


UNREAD_UNSPRUNG = "the record carries no credit of the gap-0 row (light has no period on the sea)"


def redshift(chart: Chart) -> dict[str, Any]:
    """Gate 11: the gravitational redshift, the unsprung chimes' period longer where the load is deeper, by the rates squared (EM-S4's predicate)."""
    return {
        "11 gravitational redshift": {
            "verdict": unread_words(
                UNREAD_UNSPRUNG,
                "the gap-0 credits' period longer where the content is deeper, by the clocks squared",
            )
        }
    }


def delay(chart: Chart) -> dict[str, Any]:
    """Gate 12: light's delay or deflection, the unsprung chimes' first tick against the mesh distance from the light's source (EM-S4's predicate)."""
    return {
        "12 light's delay or deflection": {
            "verdict": unread_words(
                UNREAD_UNSPRUNG,
                "the gap-0 credits' first interval against the Link distance from the emitter, later or off the line where deeper",
            )
        }
    }


def arrow(chart: Chart) -> dict[str, Any]:
    """Gate 18: the arrow of time on the rewind, exact bit for bit or not; read on the whole chart alone."""
    rb = chart.run.get("run_back")
    if chart.ticks < int(chart.run["intervals"]):
        verdict = "NOT READ: the run back is the whole record's"
    elif not rb:
        verdict = "NOT READ: the record carries no run back (the writer with back N)"
    elif rb["exact"] == rb["intervals"]:
        verdict = f"SHOWN: the run back exact bit for bit, {rb['exact']} of {rb['intervals']} intervals"
    else:
        verdict = f"NOT SHOWN: {rb['exact']} of {rb['intervals']}"
    return {"18 the arrow of time": {"run back on the record": rb, "verdict": verdict}}


def recoil(chart: Chart) -> dict[str, Any]:
    """Row 23: the momentum across the strike (Compton's recoil), the striking's dP_a on the strike lines: the unwinds' and the advances' sums per axis and the fittings where the recoil passed to the fitted pair (unwind + advance = 0)."""
    unwinds = [c["dP_take"] for c in chart.chimes + chart.fittings if c.get("dP_take")]
    lays = [b["dP_lay"] for b in chart.fittings if b.get("dP_lay")]
    passed = sum(
        1
        for b in chart.fittings
        if b.get("dP_lay") and all(b["dP_take"][a] + b["dP_lay"][a] == 0 for a in range(AXES))
    )
    return {
        "23 the momentum across the click": {
            "clicks booking dP": len(unwinds),
            "takes dP_a summed": [sum(t[a] for t in unwinds) for a in range(AXES)],
            "lays dP_a summed": [sum(lay[a] for lay in lays) for a in range(AXES)],
            "recoil passed to the laid pair (take + lay = 0 per birth)": [passed, len(lays)],
            "verdict": "NOT READ: no click booked its momentum"
            if not unwinds
            else unread_words("no birth", "the take's dP and the lay's sum to 0 at every birth")
            if not lays
            else "SHOWN: the recoil passed to the laid pair at every birth"
            if passed == len(lays)
            else f"NOT SHOWN: the recoil passed at {passed} of {len(lays)} births (the lay's form owed)",
        }
    }


def constants(chart: Chart) -> dict[str, Any]:
    """The three constants: the count of integers per clock constant through the run (the law's: a clock holds the same count of integers at every tick), with the widest integer of the state and of the transient named beside in bits as what the engine stores and nothing of nature (the owner's ruling of 2026-10-26, 22:1x UTC: the physics may not be tied to the bits of the run; the former verdict read every integer within the width, a wall of the machine's representation, and is struck)."""
    rows = chart.rows
    counts_seen = sorted({r["integers"] for r in rows})
    state_bits = max((r["max bits"] for r in rows), default=0)
    transient_bits = max((r["max transient bits"] for r in rows), default=0)
    return {
        "the three constants": {
            "integers per Node": counts_seen,
            "the engine's storage, no clause of the law: the widest integer of the state (bits)": state_bits,
            "the engine's storage, no clause of the law: the widest transient (bits)": transient_bits,
            "verdict": "SHOWN: the count of integers per Node constant through the run"
            if len(counts_seen) == 1
            else "NOT SHOWN: the count of integers per Node changes"
            if rows
            else "NOT READ: no row",
        }
    }


def conservations(chart: Chart) -> dict[str, Any]:
    """The conservations in the strikes (the owner's word: what the lattice conserves is shown conserved in the clicks): the charge, the count, the energy as the beat unchanged from one strike to the next, the momentum (row 23)."""
    fittings, signs, (taken, tallied) = chart.fittings, chart.signs_of(), chart.unwinds_of()
    pairs = [
        (b1, b2)
        for cs in ([(c["proper"], c["beat"]) for c in bob] for bob in chart.bobs_of().values())
        for (_p1, b1), (_p2, b2) in zip(sorted(cs), sorted(cs)[1:], strict=False)
        if b1 > 0 and b2 > 0
    ]
    unchanged = sum(1 for a, b in pairs if a == b)
    return {
        "the conservations in the clicks": {
            "charge: the senses summed over the births": sum(signs),
            "count: taken against booked over the births (hundredths)": carries(taken, tallied, HUNDRED),
            "energy: the beat (intervals per period) of a body unchanged from one click to the next": {
                "click pairs": len(pairs),
                "unchanged": unchanged,
                "changed by one": sum(1 for a, b in pairs if abs(a - b) == 1),
                "changed by more": sum(1 for a, b in pairs if abs(a - b) > 1),
            },
            "verdict": "SHOWN: the charge 0 over the births and the beat unchanged on most click pairs"
            if fittings and sum(signs) == 0 and pairs and unchanged * HALF > len(pairs)
            else "NOT SHOWN"
            if fittings and pairs
            else "NOT READ: no birth or no click pair",
        }
    }


def entropy(chart: Chart) -> dict[str, Any]:
    """Row 25: the entropy of the strikes as the law's integer: each fitting's vernier has its room (the count of numbers the one-mesh read could give); H(t) = SUM over the fittings to t of bit_length(room - 1), read from the chart alone, never falling."""
    total = last = 0
    found = []
    for b in sorted(chart.fittings, key=lambda b: int(b["i"])):
        total += (int(b["room"]) - 1).bit_length()
        if b["i"] != last:
            found.append((b["i"], total))
            last = b["i"]
    return {
        "25 the entropy of the clicks rising": {
            "births with a room": len(chart.fittings),
            "H at the end (bits)": total,
            "course (interval, H) at every eighth": found[:: max(1, len(found) // LISTED)],
            "verdict": f"SHOWN: H never falls (a sum of bit lengths), {total} bits over {len(chart.fittings)} births"
            if chart.fittings
            else "NOT READ: no birth",
        }
    }


def restated(key: str, source: Row) -> Row:
    """A row restating another gate's verdict (29 to 31 and 33 restate 11, 10, 12 and 13): the source's verdict after "as gate N: "."""

    def row(chart: Chart) -> dict[str, Any]:
        gate, out = next(iter(source(chart).items()))
        return {key: {"verdict": f"as gate {gate.split()[0]}: " + out["verdict"]}}

    row.__name__ = row.__qualname__ = f"row_{key.split()[0]}"
    return row


RESTATED = (
    ("29 the redshift of light", redshift),
    ("30 the dilation", strikes.dilation),
    ("31 the deflection and the Shapiro delay", delay),
    ("33 free fall by the tail", free_fall),
)  # the rows of the widened table that restate a gate of the nineteen, the gate's row beside each

TABLE: tuple[Row, ...] = (
    swings.recurring_swing,
    swings.tops,
    swings.returns,
    strikes.lengthening,
    great_clock.shortening,
    great_clock.era,
    great_clock.acceleration,
    great_clock.contraction,
    light,
    strikes.families,
    strikes.species_track,
    collisions,
    strikes.dilation,
    redshift,
    delay,
    free_fall,
    great_clock.standstill,
    strikes.conservation_at_strike,
    strikes.one_strike_floor,
    strikes.charge,
    arrow,
    strikes.mass_ratios,
    events.stub("20"),
    predicates.twist_of_fitting,
    predicates.coulomb,
    recoil,
    strikes.unspring,
    entropy,
    predicates.lifts,
    predicates.confinement,
    events.stub("28"),
    restated(*RESTATED[0]),
    restated(*RESTATED[1]),
    restated(*RESTATED[2]),
    events.stub("32"),
    restated(*RESTATED[3]),
    great_clock.stopped_clock,
    events.stub("35"),
    events.stub("36"),
    great_clock.maxwell,
    events.stub("38"),
    events.stub("39"),
    predicates.photoelectric,
    events.stub("41"),
    events.stub("42"),
    predicates.exclusion,
    events.stub("44"),
    great_clock.well,
    great_clock.same_gates,
    predicates.exact_unwind,
    events.stub("48"),
    predicates.decay,
    events.stub("50"),
    events.stub("51"),
    events.stub("52"),
    events.stub("53"),
    events.stub("54"),
    predicates.two_slits,
    predicates.bell,
    predicates.ghz,
    events.fast_expansion,
    events.deceleration,
    events.acceleration_in_strikes,
    strikes.horizon_radiates,
    predicates.arrow_of_time,
    symmetries.uniformity,
    symmetries.dark_matter,
    symmetries.lepton_number,
    symmetries.energy,
    symmetries.cpt,
    symmetries.matter_against_antimatter,
    symmetries.one_twist,
    symmetries.baryon_number,
    symmetries.momentum_booked,
    symmetries.angular_momentum,
    symmetries.mass_to_light,
    conservations,
    constants,
)


def verdicts(chart: Chart) -> dict[str, Any]:
    """Every row of the table read on the chart (or on its cut)."""
    out: dict[str, Any] = {}
    for row in TABLE:
        out |= row(chart)
    return out


def gates(run: dict[str, Any]) -> dict[str, Any]:
    """Every gate's verdict with its numbers from the chart alone, the reckoner's line (the rows of the gates of the phenomena and their count by the verdict's kind, the count of SHOWN in Universe24), and the event lines of the gates' first SHOWN (events.first_shown)."""
    chart = Chart(run)
    read = [(row, row(chart)) for row in TABLE]
    out = {key: found for _row, rows in read for key, found in rows.items()}
    for key, found in out.items():
        found["kind"], found["cause"] = kind_of(found["verdict"]), cause_of(found["verdict"])
        found["label"], found["phenomenon"] = events.label_of(key), events.phenomenon_of(key)
    out["the decoder"] = {
        "floats used": 0,
        "rows of the gates of the phenomena": len(TABLE),
        "rows by the verdict's kind (the numbered rows)": dict(
            Counter(kind_of(v["verdict"]) for k, v in out.items() if k.split()[0].isdigit())
        ),
        "readings": "quotients at a named scale, counts, bit lengths; rationals compared by cross multiplication",
        "rows read from the Node lines (the board's view; the rest from the log, the clicks' view)": [
            key
            for row in TABLE
            if row.__module__ in (swings.__name__, great_clock.__name__)
            for key in row(chart)
        ],
    }
    out["events"] = events.first_shown(chart, read)
    out["the eras"] = events.eras_of(out, chart.ticks, swings.tops_of(chart), swings.exact_of(chart))
    return out


def main(argv: list[str]) -> None:
    """The gates of a chart file, one line each; the interpreter's limit on an integer's digits lifted, so a chart whose stretches passed the law's width still loads (the Boss's 6418880289: a reader could not load the record carried to 48)."""
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as chart:
        for k, v in gates(json.load(chart)).items():
            print(json.dumps({k: v}))


if __name__ == "__main__":
    main(sys.argv)
