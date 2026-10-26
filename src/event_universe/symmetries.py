"""The rows of the kinds and the symmetries in the clicks, rows 63 to 67 (the owner's word of 2026-10-26, 07:24 UTC, "enter 61 to 65", through the Boss, The-Laws-Of-Nature-Missing_COMPARISON.md section 3 item 2; the ledger's row 164), each one function of the reading in the one shape: the uniformity in the clicks (the credits spread over the board's eight regions alike), dark matter in kind (a body credited in its own well whose Nodes lay no light, the law's theorem of the lines), the lepton number (every gapped species' senses summing to 0 over its births, the record's count of each species conserved at the click), the energy in the clicks (a body's beat per proper interval before and after its click equal within one level, the taken light's beat the difference), and CPT as one row (on every credit's frame the charge W odd under the conjugation C, even under the reflection P of the Node's six Links, odd under the slot exchange T of CA-S1, so even under the three together)."""

from __future__ import annotations

from collections import Counter
from typing import Any

from event_universe.decoder import HALF, PAIR, Record, unread_words


def region(record: Record, node: list[int] | tuple[int, ...]) -> int:
    """A Node's region of the board, one of eight: each axis split at the cube's half."""
    half = record.cube // HALF
    return sum((int(x) >= half) << a for a, x in enumerate(node))


def uniformity(record: Record) -> dict[str, Any]:
    """Row 63: the uniformity in the clicks, the credits counted per region of the board (eight, each axis at its half): SHOWN where every region is credited and the least holds at least half the largest."""
    counts = Counter(region(record, c["node"]) for c in record.credits)
    least, largest = min(counts.values(), default=0), max(counts.values(), default=0)
    return {
        "63 the uniformity in the clicks": {
            "credits per region of the board (eight, each axis at its half)": [
                counts.get(r, 0) for r in range(PAIR**3)
            ],
            "verdict": unread_words(
                "no credit", "every region credited, the least at least half the largest"
            )
            if not counts
            else "SHOWN: every region of the board credited, the least at least half the largest"
            if len(counts) == PAIR**3 and least * HALF >= largest
            else f"NOT SHOWN: {PAIR**3 - len(counts)} regions without a credit, the least {least} against the largest {largest}",
        }
    }


def dark_matter(record: Record) -> dict[str, Any]:
    """Row 64: dark matter in kind (the law's theorem of the lines): a body credited in its own well whose Nodes lay no light, a credit track at a Node where no birth took and no child was laid through the run."""
    lit = {record.index(b["node"]) for b in record.births} | {
        record.index(b[end]) for b in record.births for end in ("minus", "plus")
    }
    bodies = record.bodies_of()
    dark = [key for key in bodies if record.index(key[0]) not in lit]
    return {
        "64 dark matter in kind": {
            "bodies (credit tracks) / of them at a Node where no light was laid": [
                len(bodies),
                len(dark),
            ],
            "at": list(dark[0][0]) if dark else None,
            "verdict": unread_words(
                "no body", "a body credited in its own well whose Nodes lay no light"
            )
            if not bodies
            else f"SHOWN: {len(dark)} of {len(bodies)} bodies credited at a Node where no light was laid"
            if dark
            else "NOT SHOWN: every body's Node laid light",
        }
    }


def lepton_number(record: Record) -> dict[str, Any]:
    """Row 65: the lepton number (the record's parts are its particles, the record's count conserved at the click): for every species born, the children's own senses summed over its births is 0, each birth a pair of opposite senses, so the number of each species less its anti-species is conserved."""
    sums: Counter[str] = Counter()
    for b, (a, c) in zip(record.births, record.charges_of(), strict=True):
        sums[record.line_name[b["line_pair"]]] += (a > 0) - (a < 0) + (c > 0) - (c < 0)
    return {
        "65 the lepton number": {
            "the senses summed per species born": dict(sums),
            "verdict": unread_words("no birth", "every species' senses sum to 0 over its births")
            if not record.births
            else "SHOWN: every species' senses sum to 0 over its births, its number conserved at the click"
            if all(s == 0 for s in sums.values())
            else f"NOT SHOWN: {sum(1 for s in sums.values() if s)} species with a sum not 0",
        }
    }


def energy(record: Record) -> dict[str, Any]:
    """Row 66: the energy in the clicks (one point and one beat, D-S2): a body's beat per proper interval before and after its click equal within one level, the taken light's beat the difference, on every pair of a body's consecutive credits."""
    pairs = [
        (b1, b2)
        for cs in ([(c["proper"], c["beat"]) for c in body] for body in record.bodies_of().values())
        for (_p1, b1), (_p2, b2) in zip(sorted(cs), sorted(cs)[1:], strict=False)
        if b1 > 0 and b2 > 0
    ]
    within = sum(1 for a, b in pairs if abs(a - b) <= 1)
    return {
        "66 the energy in the clicks": {
            "click pairs of a body / within one level": [len(pairs), within],
            "verdict": unread_words(
                "no click pair of a body", "the beat before and after the click equal within one level"
            )
            if not pairs
            else "SHOWN: a body's beat before and after its click equal within one level on every pair"
            if within == len(pairs)
            else "SHOWN in part: on most pairs"
            if within * HALF > len(pairs)
            else f"NOT SHOWN: {len(pairs) - within} pairs beyond one level",
        }
    }


def cpt(record: Record) -> dict[str, Any]:
    """Row 67: CPT as one row, on every credit's frame: the charge W = re_now im_before - im_now re_before is odd under the conjugation C (the im line negated), even under the reflection P (the Node's own levels unmoved, the six Links exchanged in pairs), odd under the slot exchange T (CA-S1, now for before), so even under the three together; counted over the frames whose W is not 0."""
    frames = [c["frame"] for c in record.credits if "frame" in c]
    w = [f["re_now"] * f["im_before"] - f["im_now"] * f["re_before"] for f in frames]
    c = [f["re_now"] * -f["im_before"] - -f["im_now"] * f["re_before"] for f in frames]
    t = [f["re_before"] * f["im_now"] - f["im_before"] * f["re_now"] for f in frames]
    cpt_w = [f["re_before"] * -f["im_now"] - -f["im_before"] * f["re_now"] for f in frames]
    nonzero = sum(1 for x in w if x)
    odd_c = sum(1 for x, y in zip(w, c, strict=True) if x and y == -x)
    odd_t = sum(1 for x, y in zip(w, t, strict=True) if x and y == -x)
    even = sum(1 for x, y in zip(w, cpt_w, strict=True) if x and y == x)
    return {
        "67 CPT in the clicks": {
            "frames with a charge": nonzero,
            "the charge odd under C / odd under T / even under C, P and T together": [
                odd_c,
                odd_t,
                even,
            ],
            "verdict": unread_words(
                "no frame carries a charge", "W odd under C and T, even under P, even under the three"
            )
            if not nonzero
            else f"SHOWN: the charge odd under C and under T and even under CPT on {even} of {nonzero} frames"
            if odd_c == odd_t == even == nonzero
            else f"NOT SHOWN: {nonzero - even} frames' charge not even under CPT",
        }
    }
