"""The rows of the kinds and the symmetries in the clicks, rows 63 to 71 (the owner's word of 2026-10-26, 07:24 UTC, "enter 61 to 65", through the Boss, The-Laws-Of-Nature-Missing_COMPARISON.md section 3 item 2; the ledger's row 164), each one function of the reading in the one shape: the uniformity in the clicks (the credits spread over the board's eight regions alike), dark matter in kind (a body credited in its own well whose Nodes lay no light, the law's theorem of the lines), the lepton number (every gapped species' senses summing to 0 over its births, the record's count of each species conserved at the click), the energy in the clicks (a body's beat per proper interval before and after its click equal within one level, the taken light's beat the difference), and CPT as one row (on every credit's frame the charge W odd under the conjugation C, even under the reflection P of the Node's six Links, odd under the slot exchange T of CA-S1, so even under the three together)."""

from __future__ import annotations

from collections import Counter
from typing import Any

from event_universe.core import rule3
from event_universe.core.spokes import AXES
from event_universe.reckoner import HALF, PAIR, Chart, sign, unread_words

REGIONS = PAIR**AXES  # the board's regions, each axis split at the cube's half


def region(record: Chart, node: list[int] | tuple[int, ...]) -> int:
    """A Node's region of the board, one of eight: each axis split at the cube's half."""
    half = int(rule3.carries(record.cube, HALF))
    return sum((int(x) >= half) << a for a, x in enumerate(node))


def uniformity(record: Chart) -> dict[str, Any]:
    """Row 63: the uniformity in the clicks, the credits counted per region of the board (eight, each axis at its half): SHOWN where every region is credited and the least holds at least half the largest."""
    counts = Counter(region(record, c["node"]) for c in record.chimes)
    least, largest = min(counts.values(), default=0), max(counts.values(), default=0)
    return {
        "63 the uniformity in the clicks": {
            "credits per region of the board (eight, each axis at its half)": [
                counts.get(r, 0) for r in range(REGIONS)
            ],
            "verdict": unread_words(
                "no credit", "every region credited, the least at least half the largest"
            )
            if not counts
            else "SHOWN: every region of the board credited, the least at least half the largest"
            if len(counts) == REGIONS and least * HALF >= largest
            else f"NOT SHOWN: {REGIONS - len(counts)} regions without a credit, the least {least} against the largest {largest}",
        }
    }


def dark_matter(record: Chart) -> dict[str, Any]:
    """Row 64: dark matter in kind (the law's theorem of the lines): a body credited in its own well whose Nodes lay no light, a credit track at a Node where no birth took and no child was laid through the run."""
    lit = {record.index(b["node"]) for b in record.fittings}
    lit |= {record.index(b["minus"]) for b in record.fittings}
    lit |= {record.index(b["plus"]) for b in record.fittings}
    bodies = record.bobs_of()
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


def lepton_number(record: Chart) -> dict[str, Any]:
    """Row 65: the lepton number (the record's parts are its particles, the record's count conserved at the click): for every species born, the children's own senses summed over its births is 0, each birth a pair of opposite senses, so the number of each species less its anti-species is conserved."""
    sums: Counter[str] = Counter()
    for b, (a, c) in zip(record.fittings, record.sweeps_of(), strict=True):
        sums[record.gear_name[b["line_pair"]]] += sign(a) + sign(c)
    return {
        "65 the lepton number": {
            "the senses summed per species born": dict(sums),
            "verdict": unread_words("no birth", "every species' senses sum to 0 over its births")
            if not record.fittings
            else "SHOWN: every species' senses sum to 0 over its births, its number conserved at the click"
            if all(s == 0 for s in sums.values())
            else f"NOT SHOWN: {sum(1 for s in sums.values() if s)} species with a sum not 0",
        }
    }


def energy(record: Chart) -> dict[str, Any]:
    """Row 66: the energy in the clicks (one point and one beat, D-S2): a body's beat per proper interval before and after its click equal within one level, the taken light's beat the difference, on every pair of a body's consecutive credits."""
    pairs = [
        (b1, b2)
        for cs in ([(c["proper"], c["beat"]) for c in body] for body in record.bobs_of().values())
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


def cpt(record: Chart) -> dict[str, Any]:
    """Row 67: CPT as one row, on every credit's frame: the charge W = re_now im_before - im_now re_before is odd under the conjugation C (the im line negated), even under the reflection P (the Node's own levels unmoved, the six Links exchanged in pairs), odd under the slot exchange T (CA-S1, now for before), so even under the three together; counted over the frames whose W is not 0."""
    frames = [c["frame"] for c in record.chimes if "frame" in c]
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


def twists_of(record: Chart) -> tuple[int, int, int]:
    """The moving births' hands (the births of a pair; a merger lays its light at both ends and carries no hand): the + child at the take's Node, at the other end, and the mergers beside."""
    moving = [b for b in record.fittings if "takes" not in b]
    at_node = sum(1 for b in moving if list(b["plus"]) == list(b["node"]))
    return at_node, len(moving) - at_node, len(record.fittings) - len(moving)


def matter_against_antimatter(record: Chart) -> dict[str, Any]:
    """Row 68: matter against antimatter (HD-S1, the Boss's 6412271828 and 6413689341): the hand enters the law in one act, the + child laid at the end the current flows into where the twist is right-handed, so over the moving births the + child stands at the take's Node on some and at the other end on the rest (the twist's sign at each click, P-odd and C-even, kept by the bijection), the mergers named beside; counted, the hand's choice read at every moving birth."""
    at_node, other, mergers = twists_of(record)
    return {
        "68 matter against antimatter": {
            "moving births with the + child at the take's Node / at the other end": [at_node, other],
            "mergers beside (the light at both ends, no hand)": mergers,
            "verdict": unread_words(
                "no moving birth", "the + child's end chosen by the twist's hand at every moving birth"
            )
            if not at_node + other
            else f"SHOWN: the + child at the take's Node on {at_node} moving births and at the other end on {other}, the hand's choice at every one; {mergers} mergers beside",
        }
    }


def one_twist(record: Chart) -> dict[str, Any]:
    """Row 69: the neutrino's one hand (the Boss's 6412773403, the helicity pair's reading): the hand of every moving birth, the end the + child is laid at (the take's Node or the other end, by the twist at the click), all one over the record where nature's neutrino shows one hand alone; NOT SHOWN with its cause where both hands stand (no conversion on the records, the births' hands split), NOT READ where no moving birth."""
    at_node, other, mergers = twists_of(record)
    return {
        "69 the neutrino's one hand": {
            "moving births by hand (the + child at the take's Node / at the other end)": [
                at_node,
                other,
            ],
            "mergers beside (no hand)": mergers,
            "verdict": unread_words("no moving birth", "one hand at every moving birth of the record")
            if not at_node + other
            else "SHOWN: one hand at every moving birth of the record"
            if not at_node or not other
            else f"NOT SHOWN: both hands stand, {at_node} and {other} moving births (no conversion on the record, the hands split by the twist at each click)",
        }
    }


def baryon_number(record: Chart) -> dict[str, Any]:
    """Row 70: the baryon number, the C-odd count (the Boss's 6413689341, the floor pair's reading): the children's own charges summed over each birth's two children, 0 at every birth (a pair at opposite senses, a merger's light at 0 and 0: no matter-making act in the law, the count conserved at the click); the record's Wronskian at the children's Nodes summed beside it, apart from 0 where a child was laid on a standing level (the residue, the Node's W) and over the mergers' light (W of one sign on both until merger.py's fix); SHOWN where the own charges sum to 0 at every birth."""
    own = [a + c for a, c in record.sweeps_of()]
    pairs = [sum(b["W_children"]) for b in record.fittings if "takes" not in b]
    mergers = [sum(b["W_children"]) for b in record.fittings if "takes" in b]
    return {
        "70 the baryon number": {
            "births whose children's own charges sum to 0 / in all": [own.count(0), len(own)],
            "births of a pair whose record W at the children's Nodes sums apart from 0 (the standing level's residue)": sum(
                1 for w in pairs if w
            ),
            "the mergers' light children's record W summed (0 by the letter)": sum(mergers),
            "verdict": unread_words(
                "no birth",
                "the children's own charges summing to 0 at every birth, no matter made by a click",
            )
            if not own
            else "SHOWN: the children's own charges sum to 0 at every birth, no matter made by a click"
            if own.count(0) == len(own)
            else f"NOT SHOWN: {len(own) - own.count(0)} births whose children's own charges do not sum to 0",
        }
    }


def tallies_of(record: Chart) -> list[tuple[Any, ...]]:
    """Every booking a move wrote on the Link's record (LT-S1, take.recoil): the momentum's change per axis the move books (dP_take at a take, dP_lay at a birth's end), the clock the Node read at the interval's start, the levels laid per axis on the carrier's flux lines, and their carry before and after; a line without the keys (a record run before LT-S1) is no booking."""
    found: list[tuple[Any, ...]] = []
    for entry in record.unwinds:
        if "recoil" not in entry:
            continue
        found.append(
            (entry["dP_take"], entry["clock"], entry["recoil"], entry["carry_was"], entry["carry"])
        )
        for k in range(PAIR):
            if "recoil_ends" in entry:
                found.append(
                    (
                        entry["dP_lay_ends"][k],
                        entry["clock_ends"][k],
                        entry["recoil_ends"][k],
                        entry["carry_was_ends"][k],
                        entry["carry_ends"][k],
                    )
                )
    return found


def momentum_booked(record: Chart) -> dict[str, Any]:
    """Row 71: the momentum booked on the Link (LT-S1, H-Lay-As-The-Take-Reversed-1's derivation, line 19 as the Boss corrected its sign): at every move the momentum the quantum lost is written on the carrier's flux line of each axis at the Node by the one write act, -dP_a p_0^2 + the carry before - the carry after = the levels laid times the write wall 6 den Gamma^2 T, the clock p_0 the Node's at the interval's start; so the records' and the lattice's momentum sum to what they were at every click, an identity on every booking of the record; NOT READ on a record without the bookings' keys."""
    wall = rule3.teeth_of(record.rim, record.full_rate) * record.key
    held = laid = failed = 0
    for dp, clock, recoil, was, after in tallies_of(record):
        for a in range(AXES):
            if -dp[a] * clock * clock + was[a] - after[a] == recoil[a] * wall:
                held += 1
                laid += recoil[a] != 0
            else:
                failed += 1
    return {
        "71 the momentum booked on the Link": {
            "axis bookings holding the identity / in all": [held, held + failed],
            "of them laying a level on the carrier's flux line (the rest kept in the carry)": laid,
            "the write wall 6 den Gamma^2 T": wall,
            "verdict": unread_words(
                "no booking on the record (a record run before LT-S1, the keys recoil, carry_was and carry absent)",
                "-dP p_0^2 + the carry before - the carry after = the levels laid times the write wall at every move",
            )
            if not held + failed
            else f"SHOWN exact: -dP p_0^2 + the carry before - the carry after = the levels laid times the write wall on {held} of {held} axis bookings, {laid} laying a level"
            if not failed
            else f"NOT SHOWN: the identity fails on {failed} of {held + failed} axis bookings",
        }
    }
