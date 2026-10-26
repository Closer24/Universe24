"""The widened rows of UNIVERSE24's table (20 to 54, everything derived) as predicates on the record, one function per row: read where the record carries the row (the births' hands, Coulomb's sign from the credited Nodes' senses, the lifts and their beats, the whole takes, the exclusion's refusals, the exact take, the decay's spacings), and NOT READ with the predicate named where it cannot (a held field, a wave lay, a conversion, a light credit, the 48 images); the rows restating a gate of the nineteen (29 to 31, 33) are gates.py's and the rows read from the Node lines (34, 37, 45, 46) board.py's."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from event_universe.core.ports import AXES
from event_universe.core.rule3 import largest_below
from event_universe.decoder import (
    HALF,
    HUNDRED,
    LIFTS,
    LISTED,
    PAIR,
    QUARTERS,
    THIRDS,
    Record,
    quot,
    unread_words,
)


def unread(key: str, why: str, predicate: str) -> dict[str, Any]:
    """A row the record cannot carry, its verdict alone."""
    return {key: {"verdict": unread_words(why, predicate)}}


def hand_of_birth(record: Record) -> dict[str, Any]:
    """Row 21: the C of the birth, the births' hands: the + child laid at the take's Node (the current's end) or at the other end, births of both hands over the record."""
    right = sum(1 for b in record.births if b["plus"] == b["node"])
    left = len(record.births) - right
    return {
        "21 the C of the birth": {
            "births with the + child at the take's Node / at the other end": [right, left],
            "verdict": unread_words("no birth", "births of both hands over the record")
            if not record.births
            else "SHOWN: births of both hands"
            if right and left
            else "NOT SHOWN: every birth of one hand",
        }
    }


def coulomb(record: Record) -> dict[str, Any]:
    """Row 22: Coulomb's sign from the credited Nodes' senses per interval: the mean distance between Nodes of unlike senses at the first and the last interval holding such a pair, and between Nodes of like senses; unlike approach, like part."""
    by_interval: dict[int, list[tuple[int, tuple[int, ...]]]] = defaultdict(list)
    for c in record.credits:
        if c["sense"]:
            by_interval[int(c["i"])].append((c["sense"], tuple(c["node"])))
    distance = record.distance
    means: dict[bool, list[tuple[int, int]]] = {True: [], False: []}
    for i in sorted(by_interval):
        found = by_interval[i]
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
                quot(s, n, HUNDRED) for s, n in (means[False][:1] + means[False][-1:])
            ],
            "like senses: mean distance first / last (hundredths)": [
                quot(s, n, HUNDRED) for s, n in (means[True][:1] + means[True][-1:])
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


def lifts(record: Record) -> dict[str, Any]:
    """Row 26: the three lifts born and their beats' ratios: three or more distinct planes born, and the credited planes' mean beats (intervals per period) ordered against their legs, the heavier the faster."""
    born = record.born_of()
    beats: dict[int, tuple[int, int]] = {}
    for c in record.credits:
        s, n = beats.get(c["line"], (0, 0))
        beats[c["line"]] = (s + int(c["beat"]), n + 1)
    legs = {line: record.NAMES[record.line_num[line]][1] for line in beats}
    order = sorted(beats, key=lambda line: legs[line])
    ordered = all(
        beats[a][0] * beats[b][1] >= beats[b][0] * beats[a][1]
        for a, b in zip(order, order[1:], strict=False)
    )
    return {
        "26 the three lifts born and their beats' ratios": {
            "planes born": dict(born),
            "mean beat per credited plane (hundredths), by the leg": [
                [record.line_name[line], quot(*beats[line], HUNDRED)] for line in order
            ],
            "verdict": unread_words(
                "no birth and fewer than two planes credited",
                "three lifts born, the beats ordered as the legs",
            )
            if not born and len(beats) < PAIR
            else "SHOWN: three lifts born, the beats ordered as the legs (the heavier the faster)"
            if len(born) >= LIFTS and len(beats) >= PAIR and ordered
            else "SHOWN in part: "
            + ", ".join(
                p
                for p, ok in (
                    (f"{len(born)} lifts born", len(born) >= LIFTS),
                    ("the beats ordered as the legs", len(beats) >= PAIR and ordered),
                )
                if ok
            )
            if (len(born) >= LIFTS) or (len(beats) >= PAIR and ordered)
            else f"NOT SHOWN: {len(born)} lifts born, the beats of {len(beats)} planes not ordered as the legs",
        }
    }


def confinement(record: Record) -> dict[str, Any]:
    """Row 27: confinement, no third alone: every child laid where its plane stood at nothing carries the whole charge T div 2 and none a third of it; every take whole levels."""
    half, third = record.T // HALF, record.T // (HALF * THIRDS)
    laid = record.laid_at_nothing()
    whole, thirds = sum(w == half for w in laid), sum(w == third for w in laid)
    takes = [int(e["levels"]) for e in record.takes]
    return {
        "27 confinement (no third alone)": {
            "children at the whole charge / at a third": [whole, thirds],
            "takes, every one whole levels": len(takes),
            "verdict": unread_words(
                "no birth", "no child carries a third of the charge, every take whole"
            )
            if not record.births
            else "SHOWN: every child the whole charge, no third alone, every take whole"
            if thirds == 0 and whole
            else "NOT SHOWN: a child at a third of the charge",
        }
    }


def photoelectric(record: Record) -> dict[str, Any]:
    """Row 40: the photoelectric click, one whole quantum per click: the levels a credit takes against the quantum's levels (the drift, the largest integer whose square is at most T)."""
    drift = largest_below(record.T)
    takes = [int(c["levels"]) for c in record.credits]
    whole = sum(1 for t in takes if t % drift == 0)
    return {
        "40 the photoelectric click": {
            "the quantum's levels (the drift)": drift,
            "credits taking whole quanta / fewer levels": [whole, len(takes) - whole],
            "verdict": unread_words("no credit", "one whole quantum per click")
            if not takes
            else "SHOWN: every click takes whole quanta"
            if whole == len(takes)
            else f"NOT SHOWN: {len(takes) - whole} clicks take fewer levels than one quantum (the exact take in levels, row 47)",
        }
    }


def exclusion(record: Record) -> dict[str, Any]:
    """Row 43: the exclusion, one quantum per full state at a Node: the close's lays refused where a quantum of the record stood at the Node (the refused lines with a standing and a unit)."""
    refused = [e for e in record.log if e["event"] == "refused" and "standing" in e]
    return {
        "43 the exclusion": {
            "lays refused where a quantum of the record stood": len(refused),
            "verdict": "SHOWN: the lay refused where a quantum of the state stood, on every such Node"
            if refused
            else unread_words("no lay met a standing quantum", "one quantum per full state at a Node"),
        }
    }


def exact_take(record: Record) -> dict[str, Any]:
    """Row 47: the exact take, taken equal to booked on every birth (the excess 0); the credits' leak unread (a credit carries no booked walls)."""
    births, (taken, booked) = record.births, record.takes_of()
    exact = sum(1 for b in births if b["taken"] == b["booked"])
    return {
        "47 the exact take": {
            "births taken exactly / in all": [exact, len(births)],
            "taken per booked over the births (hundredths)": quot(taken, booked, HUNDRED),
            "verdict": unread_words("no birth", "taken equals booked on every line")
            if not births
            else "SHOWN: taken equals booked on every birth"
            if exact == len(births)
            else f"NOT SHOWN exact: the excess above 0 on {len(births) - exact} births (EX-S1)",
        }
    }


def decay(record: Record) -> dict[str, Any]:
    """Row 49: the exponential decay, a body's credits' spacing in its proper count geometric: the spacings' counts falling from the least spacing; periodic where one spacing holds the majority."""
    spacings: Counter[int] = Counter()
    for body in record.bodies_of().values():
        ps = sorted(int(c["proper"]) for c in body)
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


SETTINGS = (
    (1, 0),
    (1, 1),
    (4, 3),
    (3, 4),
)  # Bell's (p, q), two per end, the outcome sign(p re + q im): the axis and the diagonal for one end, the 3-4-5 triple's two directions for the other (exact cosines 4/5 and 3/5), every integer among the law's free ones


def two_slits(record: Record) -> dict[str, Any]:
    """Row 55: the two slits (QG-S2), two gap-0 lays at one centre with one wave mirrored on one axis, read from the seed; the fringe (the gap-0 row's meetings at the dark offsets 4 C_d^2 < den^2 none and at the bright many over the beams' overlap) is counted by the hand's reader alone (H-Quantum-Gates-2/predicates_qg.py), the count owed to the decoder where a seed carries the beams."""
    rows, seed = record.run["universe"]["rows"], record.run["world"].get("seed", [])
    lays = [s for s in seed if s.get("wave") and int(rows[s["row"]]["pair"][0]) == record.den]
    beams = [(a, b) for a in lays for b in lays if a is not b and a["centre"] == b["centre"]]
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


def bell(record: Record) -> dict[str, Any]:
    """Row 56: Bell (QG-S3), S = E(a, b) - E(a, b') + E(a', b) + E(a', b') over the born pairs' two ends at their first clicks after the birth, each end's outcome the sign of p re_now + q im_now of its frame under two settings; nature's 2 sqrt 2 as the integer inequality num^2 > 8 den^2 on S = num / den over the pairs; the law's bound |S| <= 2 (every outcome a function of its own Node, the one-Link reach) with the senses' E = -1 beside it."""
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for b in record.births:
        ends = [
            next(
                (
                    c["frame"]
                    for c in record.credits
                    if c["node"] == where
                    and c["line"] == b["line_pair"]
                    and int(c["i"]) > int(b["i"])
                    and "re_now" in c["frame"]
                ),
                None,
            )
            for where in (b["minus"], b["plus"])
        ]
        if ends[0] is not None and ends[1] is not None:
            pairs.append((ends[0], ends[1]))
    if not pairs:
        return unread(
            "56 Bell",
            f"{len(record.births)} births, no born pair clicked at both ends",
            "S from the pairs' two ends under two settings each, S^2 > 8 as nature",
        )
    e = [
        sum(
            ((u := (p * m["re_now"] + q * m["im_now"]) * (r * n["re_now"] + t * n["im_now"])) > 0)
            - (u < 0)
            for m, n in pairs
        )
        for p, q in SETTINGS[:PAIR]
        for r, t in SETTINGS[PAIR:]
    ]
    s, opposite = (
        e[0] - e[1] + e[2] + e[3],
        sum(b["W_children"][0] * b["W_children"][1] < 0 for b in record.births),
    )
    verdict = (
        "SHOWN as nature: S^2 > 8 at the pairs' clicks"
        if s * s > PAIR * QUARTERS * len(pairs) ** PAIR
        else f"NOT SHOWN as nature: |S| <= 2 at the pairs' clicks, S = {s} / {len(pairs)} (the law's bound by the one-Link reach, every end's outcome a function of its own Node; the senses' E = -1 SHOWN on {opposite} of {len(record.births)} births)"
    )
    return {
        "56 Bell": {
            "births": len(record.births),
            "pairs clicked at both ends": len(pairs),
            "E per setting pair (same - opposite)": e,
            "S as a rational": (s, len(pairs)),
            "verdict": verdict,
        }
    }


def ghz(record: Record) -> dict[str, Any]:
    """Row 57: the GHZ gate (QG-S4), three ends with one root; a birth gives two children at one Link's ends and a shared take at one Node four, so no three-ended click is in the record."""
    shared = dict(sorted(Counter(int(b.get("children_at_node", 1)) for b in record.births).items()))
    return {
        "57 GHZ": {
            "births": len(record.births),
            "births by the pairs taken at one Node in one close": shared,
            "verdict": unread_words(
                "a birth gives two ends at one Link and a shared take four, no three ends with one root in the record",
                "M = E(xyy) + E(yxy) + E(yyx) - E(xxx) over three-ended births, M^2 > 4 as nature (|M| <= 2 for every local reading)",
            ),
        }
    }
