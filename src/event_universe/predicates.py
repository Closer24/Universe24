"""The widened rows of UNIVERSE24's table (20 to 54, everything derived) as predicates on the record, one function per row: read where the record carries the row (the births' hands, Coulomb's sign from the credited Nodes' senses, the lifts and their beats, the whole takes, the exclusion's refusals, the exact take, the decay's spacings), and NOT READ with the predicate named where it cannot (a held field, a wave lay, a conversion, a light credit, the 48 images); the rows restating a gate of the nineteen (29 to 31, 33) are gates.py's and the rows read from the Node lines (34, 37, 45, 46) board.py's."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from event_universe.core import rule3
from event_universe.core.ports import AXES
from event_universe.core.rule3 import largest_below
from event_universe.decoder import (
    HALF,
    HUNDRED,
    LISTED,
    PAIR,
    QUARTERS,
    THIRDS,
    Record,
    quot,
    sign,
    unread_words,
)


def unread(key: str, why: str, predicate: str) -> dict[str, Any]:
    """A row the record cannot carry, its verdict alone."""
    return {key: {"verdict": unread_words(why, predicate)}}


def hand_of_birth(record: Record) -> dict[str, Any]:
    """Row 21: the C of the birth, the births' hands: the + child laid at the take's Node (the current's end) or at the other end, read over the moving births alone (the births of a pair; a merger lays its light at both ends by the letter and carries no hand, counted beside: the Boss's 6413689341), births of both hands over the record."""
    moving = [b for b in record.births if "takes" not in b]
    right = sum(1 for b in moving if b["plus"] == b["node"])
    left = len(moving) - right
    return {
        "21 the C of the birth": {
            "moving births with the + child at the take's Node / at the other end": [right, left],
            "mergers beside (the light at both ends, no hand)": len(record.births) - len(moving),
            "verdict": unread_words("no moving birth", "births of both hands over the record")
            if not moving
            else "SHOWN: births of both hands"
            if right and left
            else "NOT SHOWN: every moving birth of one hand",
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
    """Row 26: the lifts born and their beats' ratios: every lift the universe names born (its gapped planes, the typed points of den's circle, record.NL; the former constant 3 the toy universe's count; the plane at the gap 0 is light and no lift), and the credited planes' mean beats (intervals per period) ordered against their legs, the heavier the faster."""
    born, lifts = record.born_of(), record.lifts_born()
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
        "26 the lifts born and their beats' ratios": {
            "planes born": dict(born),
            "mean beat per credited plane (hundredths), by the leg": [
                [record.line_name[line], quot(*beats[line], HUNDRED)] for line in order
            ],
            "verdict": unread_words(
                "no birth and fewer than two planes credited",
                "every lift the universe names born, the beats ordered as the legs",
            )
            if not born and len(beats) < PAIR
            else f"SHOWN: {len(lifts)} of {record.NL} lifts born, the beats ordered as the legs (the heavier the faster)"
            if len(lifts) >= record.NL and len(beats) >= PAIR and ordered
            else "SHOWN in part: "
            + ", ".join(
                p
                for p, ok in (
                    (f"{len(lifts)} of {record.NL} lifts born", len(lifts) >= record.NL),
                    ("the beats ordered as the legs", len(beats) >= PAIR and ordered),
                )
                if ok
            )
            if (len(lifts) >= record.NL) or (len(beats) >= PAIR and ordered)
            else f"NOT SHOWN: {len(lifts)} of {record.NL} lifts born, the beats of {len(beats)} planes not ordered as the legs",
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
    """Row 47: the exact take, taken equal to booked on every birth of a pair (the excess 0), or, where the birth carries the take's remainder (EX-S1), the excess exactly the remainder's rise at the Node; a merger's birth (MG-S1, the line carrying its takes per end, the ends taken whole by the share fall) counted apart and read by row 24; the credits' leak unread (a credit carries no booked walls)."""
    births = [b for b in record.births if "takes" not in b]
    mergers = len(record.births) - len(births)
    taken, booked = sum(b["taken"] for b in births), sum(b["booked"] for b in births)
    exact = sum(
        1
        for b in births
        if b["taken"] - b["booked"] == b.get("remainder", 0) - b.get("remainder_was", 0)
    )
    kept = sum(1 for b in births if "remainder" in b)
    return {
        "47 the exact take": {
            "births taken exactly / in all": [exact, len(births)],
            "births with the excess kept as the remainder (EX-S1)": kept,
            "mergers apart (MG-S1, the ends taken whole by the share fall, row 24's reading)": mergers,
            "taken per booked over the births (hundredths)": quot(taken, booked, HUNDRED),
            "verdict": unread_words("no birth", "taken equals booked on every line")
            if not births
            else "SHOWN: taken equals booked on every birth"
            if exact == len(births) and not kept
            else "SHOWN: the take exact on every birth, its excess kept as the remainder at the Node (EX-S1)"
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
    """Row 56: Bell (QG-S3, BK-S1; the reading of The-Setting-From-The-Frame_COMPARISON.md section 3, the Boss's 6411759969): S as the count over the born pairs' four cells, the setting at each end the detector's own datum at its click (the proper clock's parity, two-valued) and the outcome the child's own sense from the birth line; nature's band 4 < S^2 <= 8 SHOWN as nature, else NOT SHOWN with the cause named: the outcome reads no datum of the detector, the child has no axis (BS-S1 owed), so every filled cell reads E = -1 and S^2 = 4."""
    cells: dict[tuple[int, int], list[int]] = {}
    for b, (a, c) in zip(record.births, record.charges_of(), strict=True):
        if not a or not c:
            continue
        ends = [
            next(
                (
                    int(rule3.odd(int(k["proper"])))
                    for k in record.credits
                    if k["node"] == where and k["line"] == b["line_pair"] and int(k["i"]) > int(b["i"])
                ),
                None,
            )
            for where in (b["minus"], b["plus"])
        ]
        if ends[0] is not None and ends[1] is not None:
            cells.setdefault((ends[0], ends[1]), []).append(sign(a) * sign(c))
    if len(cells) < PAIR * PAIR:
        return unread(
            "56 Bell",
            f"{len(record.births)} births, {len(cells)} of the four setting cells filled by pairs clicked at both ends",
            "S from the pairs' two ends under the detector's own setting at each (the proper clock's parity at its click), 4 < S^2 <= 8 as nature",
        )
    e = {
        key: (sum(1 for x in v if x > 0) - sum(1 for x in v if x < 0), len(v))
        for key, v in cells.items()
    }
    den = 1
    for _n, d in e.values():
        den = den * d // rule3.lattice(den, d)
    s = sum((num * den // d) * (-1 if key == (0, 1) else 1) for key, (num, d) in e.items())
    n = den
    verdict = (
        f"SHOWN as nature: 4 < S^2 <= 8 at the pairs' clicks, S = {s} / {n} (above the local bound 2, within Tsirelson's 2 sqrt 2)"
        if QUARTERS * n * n < s * s <= PAIR * QUARTERS * n * n
        else f"SHOWN in part: the law's own bound met exactly, S = {s} / {n}, S squared 4 (an outcome that factorizes into the child's own sign times the setting's bit is bounded by 2 and meets it: the hands' derivation, the Boss's task of 19:1x UTC); nature's 4 < S^2 <= 8 not shown (the child has no axis, BS-S1 owed)"
        if s * s == QUARTERS * n * n
        else f"NOT SHOWN as nature: |S| <= 2 at the pairs' clicks, S = {s} / {n} (the outcome the child's sense fixed at the birth, reading no datum of the detector: the child has no axis, BS-S1 owed; every filled cell E = -1)"
    )
    return {
        "56 Bell": {
            "births": len(record.births),
            "pairs clicked at both ends": sum(d for _num, d in e.values()),
            "E per cell of the detectors' settings (same - opposite, pairs)": {
                f"{k[0]}{k[1]}": list(v) for k, v in sorted(e.items())
            },
            "S as a rational": (s, n),
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


def arrow_of_time(record: Record) -> dict[str, Any]:
    """Row 62: the arrow of time in the clicks (CA-S1, the owner's word of 2026-10-26, the direction is the slot): on every credit's frame the charge W = re_now im_before - im_now re_before is negated exactly by the exchange of the two slots (now for before), so the charge is the record of the direction, odd under the exchange; counted over the frames whose W is not 0, the frames at W = 0 named apart (a level on one slot alone carries no charge)."""
    frames = [c["frame"] for c in record.credits if "frame" in c]
    charges = [f["re_now"] * f["im_before"] - f["im_now"] * f["re_before"] for f in frames]
    exchanged = [f["re_before"] * f["im_now"] - f["im_before"] * f["re_now"] for f in frames]
    nonzero = sum(1 for w in charges if w)
    odd = sum(1 for w, x in zip(charges, exchanged, strict=True) if w and x == -w)
    return {
        "62 the arrow of time in the clicks": {
            "frames at the credits": len(frames),
            "frames with a charge (W not 0)": nonzero,
            "frames whose charge is negated by the slot exchange": odd,
            "frames at W = 0": len(frames) - nonzero,
            "verdict": unread_words(
                "no frame carries a charge", "W negated by the exchange of the slots"
            )
            if not nonzero
            else f"SHOWN: the charge odd under the slot exchange, {odd} of {nonzero} frames"
            if odd == nonzero
            else f"NOT SHOWN: {nonzero - odd} frames' charge not negated by the exchange",
        }
    }
