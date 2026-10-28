"""The widened rows of UNIVERSE24's table (20 to 54, everything derived) as predicates on the chart, one function per row: read where the chart carries the row (the fittings' twists, Coulomb's sign from the chimed clocks' senses, the lifts and their beats, the whole unwinds, the exclusion's jams, the exact unwind, the decay's spacings), and NOT READ with the predicate named where it cannot (a held field, a cycle setting, a conversion, an unsprung chime, the 48 images); the rows restating a gate of the nineteen (29 to 31, 33) are gates.py's and the rows read from the clock lines (34, 37, 45, 46) great_clock.py's."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from event_universe.core import rule3
from event_universe.core.rule3 import largest_below
from event_universe.core.spokes import AXES
from event_universe.reckoner import (
    HALF,
    HUNDRED,
    LISTED,
    PAIR,
    QUARTERS,
    THIRDS,
    Chart,
    carries,
    unread_words,
)
from event_universe.trains import rows_of


def unread(key: str, why: str, predicate: str) -> dict[str, Any]:
    """A row the chart cannot carry, its verdict alone."""
    return {key: {"verdict": unread_words(why, predicate)}}


def twist_of_fitting(chart: Chart) -> dict[str, Any]:
    """Row 21: the C of the fitting, the fittings' twists: the + fitted hand advanced at the unwind's clock (the lead's end) or at the other end, read over the moving fittings alone (the fittings of a pair; an unspringing advances its light at both ends by the letter and carries no twist, counted beside: the Boss's 6413689341), fittings of both twists over the chart."""
    moving = [b for b in chart.fittings if "takes" not in b]
    right = sum(1 for b in moving if b["plus"] == b["node"])
    left = len(moving) - right
    return {
        "21 the C of the birth": {
            "moving births with the + child at the take's Node / at the other end": [right, left],
            "mergers beside (the light at both ends, no hand)": len(chart.fittings) - len(moving),
            "verdict": unread_words("no moving birth", "births of both hands over the record")
            if not moving
            else "SHOWN: births of both hands"
            if right and left
            else "NOT SHOWN: every moving birth of one hand",
        }
    }


def coulomb(chart: Chart) -> dict[str, Any]:
    """Row 22: Coulomb's sign from the chimed clocks' senses per tick: the mean distance between clocks of unlike senses at the first and the last tick holding such a pair, and between clocks of like senses; unlike approach, like part."""
    by_tick: dict[int, list[tuple[int, tuple[int, ...]]]] = defaultdict(list)
    for c in chart.chimes:
        if c["sense"]:
            by_tick[int(c["i"])].append((c["sense"], tuple(c["node"])))
    distance = chart.distance
    means: dict[bool, list[tuple[int, int]]] = {True: [], False: []}
    for i in sorted(by_tick):
        found = by_tick[i]
        for like in (True, False):
            pairs = [
                distance(a, b)
                for (sa, a), (sb, b) in zip(found, found[1:], strict=False)
                if a != b and (sa == sb) == like
            ]
            if pairs:
                means[like].append((sum(pairs), len(pairs)))

    def course(kind: bool) -> int | None:
        """The last mean against the first by cross multiplication: above 0 parting, below 0 approaching."""
        if len(means[kind]) < PAIR:
            return None
        (s0, n0), (s1, n1) = means[kind][0], means[kind][-1]
        return (s1 * n0 > s0 * n1) - (s1 * n0 < s0 * n1)

    unlike, likes = course(False), course(True)
    return {
        "22 Coulomb's sign": {
            "intervals with an unlike pair / a like pair credited": [
                len(means[False]),
                len(means[True]),
            ],
            "unlike senses: mean distance first / last (hundredths)": [
                carries(s, n, HUNDRED) for s, n in (means[False][:1] + means[False][-1:])
            ],
            "like senses: mean distance first / last (hundredths)": [
                carries(s, n, HUNDRED) for s, n in (means[True][:1] + means[True][-1:])
            ],
            "verdict": unread_words(
                "no two intervals hold a pair of credited senses",
                "unlike senses approach, like senses part",
            )
            if unlike is None and likes is None
            else "SHOWN: unlike senses approach and like senses part"
            if unlike == -1 and likes == 1
            else "SHOWN in part: unlike senses approach"
            if unlike == -1
            else "SHOWN in part: like senses part"
            if likes == 1
            else "NOT SHOWN: unlike senses do not approach, like senses do not part",
        }
    }


def lifts(chart: Chart) -> dict[str, Any]:
    """Row 26: the lifts born and their beats' ratios: every lift the calibre names fitted (its sprung hands, the typed points of the rim's circle, chart.NL; the former constant 3 the toy calibre's count; the unsprung hand is light and no lift), and the chimed hands' mean beats (ticks per period) ordered against their legs, the heavier the faster."""
    fitted, lifts = chart.fitted_of(), chart.lifts_fitted()
    beats: dict[int, tuple[int, int]] = {}
    for c in chart.chimes:
        s, n = beats.get(c["line"], (0, 0))
        beats[c["line"]] = (s + int(c["beat"]), n + 1)
    legs = {gear: chart.NAMES[chart.gear_pinion[gear]][1] for gear in beats}
    order = sorted(beats, key=lambda gear: legs[gear])
    ordered = all(
        beats[a][0] * beats[b][1] >= beats[b][0] * beats[a][1]
        for a, b in zip(order, order[1:], strict=False)
    )
    return {
        "26 the lifts born and their beats' ratios": {
            "planes born": dict(fitted),
            "mean beat per credited plane (hundredths), by the leg": [
                [chart.gear_name[gear], carries(*beats[gear], HUNDRED)] for gear in order
            ],
            "verdict": unread_words(
                "no birth and fewer than two planes credited",
                "every lift the universe names born, the beats ordered as the legs",
            )
            if not fitted and len(beats) < PAIR
            else f"SHOWN: {len(lifts)} of {chart.NL} lifts born, the beats ordered as the legs (the heavier the faster)"
            if len(lifts) >= chart.NL and len(beats) >= PAIR and ordered
            else "SHOWN in part: "
            + ", ".join(
                p
                for p, ok in (
                    (f"{len(lifts)} of {chart.NL} lifts born", len(lifts) >= chart.NL),
                    ("the beats ordered as the legs", len(beats) >= PAIR and ordered),
                )
                if ok
            )
            if (len(lifts) >= chart.NL) or (len(beats) >= PAIR and ordered)
            else f"NOT SHOWN: {len(lifts)} of {chart.NL} lifts born, the beats of {len(beats)} planes not ordered as the legs",
        }
    }


def confinement(chart: Chart) -> dict[str, Any]:
    """Row 27: confinement, no third alone: every fitted hand advanced where its hand stood at nothing carries the whole charge key div 2 and none a third of it; every unwind whole notches; NOT READ where no fitted hand advanced at nothing (a chart of unspringings alone fits no child; the former test on the fittings counted the unspringings and named a third where there was no child)."""
    half, third = chart.key // HALF, chart.key // (HALF * THIRDS)
    advanced = chart.advanced_at_nothing()
    whole, thirds = sum(w == half for w in advanced), sum(w == third for w in advanced)
    unwinds = [int(e["levels"]) for e in chart.unwinds]
    return {
        "27 confinement (no third alone)": {
            "children at the whole charge / at a third": [whole, thirds],
            "takes, every one whole levels": len(unwinds),
            "verdict": unread_words(
                "no fitted child", "no child carries a third of the charge, every take whole"
            )
            if not advanced
            else "SHOWN: every child the whole charge, no third alone, every take whole"
            if thirds == 0 and whole
            else "NOT SHOWN: a child at a third of the charge",
        }
    }


def photoelectric(chart: Chart) -> dict[str, Any]:
    """Row 40: the photoelectric strike, one whole quantum per strike: the notches a chime unwinds against the quantum's notches (the drift, the largest integer whose square is at most the key)."""
    drift = largest_below(chart.key)
    unwinds = [int(c["levels"]) for c in chart.chimes]
    whole = sum(1 for t in unwinds if t % drift == 0)
    return {
        "40 the photoelectric click": {
            "the quantum's levels (the drift)": drift,
            "credits taking whole quanta / fewer levels": [whole, len(unwinds) - whole],
            "verdict": unread_words("no credit", "one whole quantum per click")
            if not unwinds
            else "SHOWN: every click takes whole quanta"
            if whole == len(unwinds)
            else f"NOT SHOWN: {len(unwinds) - whole} clicks take fewer levels than one quantum (the exact take in levels, row 47)",
        }
    }


def exclusion(chart: Chart) -> dict[str, Any]:
    """Row 43: the exclusion, one quantum per full state at a clock: the striking's advances jammed where a quantum of the hand stood at the clock (the jammed lines with a wound and a winding)."""
    jammed = [e for e in chart.log if e["event"] == "refused" and "standing" in e]
    return {
        "43 the exclusion": {
            "lays refused where a quantum of the record stood": len(jammed),
            "verdict": "SHOWN: the lay refused where a quantum of the state stood, on every such Node"
            if jammed
            else unread_words("no lay met a standing quantum", "one quantum per full state at a Node"),
        }
    }


def exact_unwind(chart: Chart) -> dict[str, Any]:
    """Row 47: the exact unwind, unwound equal to tallied on every fitting of a pair (the excess 0), or, where the fitting carries the unwind's slack (EX-S1), the excess exactly the slack's rise at the clock; an unspringing's fitting (MG-S1, the line carrying its unwinds per end, the ends unwound whole by the wind fall) counted apart and read by row 24; the chimes' leak unread (a chime carries no tallied teeth)."""
    fittings = [b for b in chart.fittings if "takes" not in b]
    unsprings = len(chart.fittings) - len(fittings)
    unwound, tallied = sum(b["taken"] for b in fittings), sum(b["booked"] for b in fittings)
    exact = sum(
        1
        for b in fittings
        if b["taken"] - b["booked"] == b.get("remainder", 0) - b.get("remainder_was", 0)
    )
    kept = sum(1 for b in fittings if "remainder" in b)
    return {
        "47 the exact take": {
            "births taken exactly / in all": [exact, len(fittings)],
            "births with the excess kept as the remainder (EX-S1)": kept,
            "mergers apart (MG-S1, the ends taken whole by the share fall, row 24's reading)": unsprings,
            "taken per booked over the births (hundredths)": carries(unwound, tallied, HUNDRED),
            "verdict": unread_words("no birth", "taken equals booked on every line")
            if not fittings
            else "SHOWN: taken equals booked on every birth"
            if exact == len(fittings) and not kept
            else "SHOWN: the take exact on every birth, its excess kept as the remainder at the Node (EX-S1)"
            if exact == len(fittings)
            else f"NOT SHOWN exact: the excess above 0 on {len(fittings) - exact} births (EX-S1)",
        }
    }


def decay(chart: Chart) -> dict[str, Any]:
    """Row 49: the exponential decay, a bob's chimes' spacing in its dial geometric: the spacings' counts falling from the least spacing; periodic where one spacing holds the majority."""
    spacings: Counter[int] = Counter()
    for bob in chart.bobs_of().values():
        ps = sorted(int(c["proper"]) for c in bob)
        spacings.update(b - a for a, b in zip(ps, ps[1:], strict=False) if b > a)
    counts = [spacings[s] for s in sorted(spacings)]
    falling = all(a >= b for a, b in zip(counts, counts[1:], strict=False))
    total = sum(counts)
    return {
        "49 the exponential decay": {
            "spacings between a body's credits (proper count: how many)": dict(
                sorted(spacings.items())[:LISTED]
            ),
            "verdict": unread_words("fewer than two spacings", "the spacing geometric")
            if total < PAIR
            else "SHOWN: the spacings' counts fall from the least spacing (geometric)"
            if falling and len(counts) > 1
            else "NOT SHOWN: the body's clicks periodic at its beat (one spacing holds the majority)"
            if max(counts) * HALF > total
            else "NOT SHOWN: the spacings' counts do not fall from the least",
        }
    }


def two_slits(chart: Chart) -> dict[str, Any]:
    """Row 55: the two slits (QG-S2), two unsprung settings at one centre with one stride mirrored on one axis, read from the setting; the fringe (the unsprung train's engagements at the dark offsets 4 C_d^2 < rim^2 none and at the bright many over the beams' overlap) is counted by the hand's reader alone (H-Quantum-Gates-2/predicates_qg.py), the count owed to the reckoner where a setting carries the beams."""
    trains, setting = rows_of(chart.run["universe"]), chart.run["world"].get("seed", [])
    settings = [s for s in setting if s.get("wave") and int(trains[s["row"]]["pair"][0]) == chart.rim]
    beams = [(a, b) for a in settings for b in settings if a is not b and a["centre"] == b["centre"]]
    mirrored = [
        (a, b)
        for a, b in beams
        if sum(x == -y != 0 for x, y in zip(a["wave"], b["wave"], strict=True)) == 1
        and sum(x == y for x, y in zip(a["wave"], b["wave"], strict=True)) == AXES - 1
    ]
    why = (
        "two gap-0 beams mirrored at one centre in the seed, their fringe the hand's count"
        if mirrored
        else "no two gap-0 packets at one centre with one wave mirrored on one axis in the seed"
    )
    return unread(
        "55 the two slits",
        why,
        "the gap-0 row's meetings at the dark offsets 0 over the beams' overlap, at the bright offsets many",
    )


def bell(chart: Chart) -> dict[str, Any]:
    """Row 56: Bell (QG-S3, BK-S1; the reading of The-Setting-From-The-Frame_COMPARISON.md section 3, the Boss's 6411759969): S as the count over the fitted pairs' four cells, each end read at its detector's own click, a click of the second kind (the owner's word of 2026-10-28, 02:2x UTC: the detector's reading is a type-2 click): the setting the detector's datum at its click (its dial's parity, two-valued) and the outcome the click's own sense (the chiming hand's sweep at the clock-node at the tick's start, bobs' `sense`), the product of the two ends' outcomes per pair; nature's band 4 < S^2 <= 8 SHOWN as nature, else NOT SHOWN with the cause named (the former outcome the fitted hand's own sense from the fitting line, E = -1 in every filled cell and S^2 = 4, kept by name)."""
    cells: dict[tuple[int, int], list[int]] = {}
    for b, (a, c) in zip(chart.fittings, chart.sweeps_of(), strict=True):
        if not a or not c:
            continue
        ends = [
            next(
                (
                    (int(rule3.odd(int(k["proper"]))), int(k["sense"]))
                    for k in chart.chimes
                    if k["node"] == where and k["line"] == b["line_pair"] and int(k["i"]) > int(b["i"])
                ),
                None,
            )
            for where in (b["minus"], b["plus"])
        ]
        if ends[0] is not None and ends[1] is not None and ends[0][1] * ends[1][1]:
            cells.setdefault((ends[0][0], ends[1][0]), []).append(ends[0][1] * ends[1][1])
    if len(cells) < PAIR * PAIR:
        return unread(
            "56 Bell",
            f"{len(chart.fittings)} births, {len(cells)} of the four setting cells filled by pairs clicked at both ends",
            "S from the pairs' two ends under the detector's own setting at each (the proper clock's parity at its click), 4 < S^2 <= 8 as nature",
        )
    e = {
        key: (sum(1 for x in v if x > 0) - sum(1 for x in v if x < 0), len(v))
        for key, v in cells.items()
    }
    den = 1
    for _n, d in e.values():
        den = den * d // rule3.pitch(den, d)
    s = sum((num * den // d) * (-1 if key == (0, 1) else 1) for key, (num, d) in e.items())
    n = den
    verdict = (
        f"SHOWN as nature: 4 < S^2 <= 8 at the pairs' clicks, S = {s} / {n} (above the local bound 2, within Tsirelson's 2 sqrt 2)"
        if QUARTERS * n * n < s * s <= PAIR * QUARTERS * n * n
        else f"SHOWN in part: the law's own bound met exactly, S = {s} / {n}, S squared 4 (an outcome that factorizes into the child's own sign times the setting's bit is bounded by 2 and meets it: the hands' derivation, the Boss's task of 19:1x UTC); nature's 4 < S^2 <= 8 not shown (the child has no axis, BS-S1 owed)"
        if s * s == QUARTERS * n * n
        else f"NOT SHOWN as nature: |S| <= 2 at the pairs' clicks, S = {s} / {n} (the outcome the detector's own click, its sense at its setting: the local bound)"
    )
    return {
        "56 Bell": {
            "births": len(chart.fittings),
            "pairs clicked at both ends": sum(d for _num, d in e.values()),
            "E per cell of the detectors' settings (same - opposite, pairs)": {
                f"{k[0]}{k[1]}": list(v) for k, v in sorted(e.items())
            },
            "S as a rational": (s, n),
            "verdict": verdict,
        }
    }


def ghz(chart: Chart) -> dict[str, Any]:
    """Row 57: the GHZ gate (QG-S4), three ends with one root; a fitting gives two fitted hands at one mesh's ends and a shared unwind at one clock four, so no three-ended strike is in the chart."""
    shared = dict(sorted(Counter(int(b.get("children_at_node", 1)) for b in chart.fittings).items()))
    return {
        "57 GHZ": {
            "births": len(chart.fittings),
            "births by the pairs taken at one Node in one close": shared,
            "verdict": unread_words(
                "a birth gives two ends at one Link and a shared take four, no three ends with one root in the record",
                "M = E(xyy) + E(yxy) + E(yyx) - E(xxx) over three-ended births, M^2 > 4 as nature (|M| <= 2 for every local reading)",
            ),
        }
    }


def arrow_of_time(chart: Chart) -> dict[str, Any]:
    """Row 62: the arrow of time in the strikes (CA-S1, the owner's word of 2026-10-26, the direction is the slot): on every chime's face the sweep = three_now twelve_before - twelve_now three_before is negated exactly by the reverse of the two slots (now for before), so the sweep records the going, odd under the reverse; counted over the faces whose sweep is not 0, the faces at sweep 0 named apart (a notch on one slot alone carries no sweep)."""
    faces = [c["frame"] for c in chart.chimes if "frame" in c]
    sweeps = [f["re_now"] * f["im_before"] - f["im_now"] * f["re_before"] for f in faces]
    reverse = [f["re_before"] * f["im_now"] - f["im_before"] * f["re_now"] for f in faces]
    nonzero = sum(1 for w in sweeps if w)
    odd = sum(1 for w, x in zip(sweeps, reverse, strict=True) if w and x == -w)
    return {
        "62 the arrow of time in the clicks": {
            "frames at the credits": len(faces),
            "frames with a charge (W not 0)": nonzero,
            "frames whose charge is negated by the slot exchange": odd,
            "frames at W = 0": len(faces) - nonzero,
            "verdict": unread_words(
                "no frame carries a charge", "W negated by the exchange of the slots"
            )
            if not nonzero
            else f"SHOWN: the charge odd under the slot exchange, {odd} of {nonzero} frames"
            if odd == nonzero
            else f"NOT SHOWN: {nonzero - odd} frames' charge not negated by the exchange",
        }
    }
