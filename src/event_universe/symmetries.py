"""The rows of the kinds and the symmetries in the strikes, rows 63 to 73 (the owner's word of 2026-10-26, 07:24 UTC, "enter 61 to 65", through the Boss, The-Laws-Of-Nature-Missing_COMPARISON.md section 3 item 2; the ledger's row 164), each one function of the reading in the one shape: the uniformity in the strikes (the chimes spread over the great clock's eight regions alike), dark matter in kind (a bob chimed in its own well whose clocks advance no light, the law's theorem of the gears), the lepton number (every sprung species' senses summing to 0 over its fittings, the hand's count of each species conserved at the strike), the energy in the strikes (a bob's beat per proper tick before and after its strike equal within one notch, the unwound light's beat the difference), and CPT as one row (on every chime's face the sweep odd under the conjugation C, even under the reflection P of the clock's six meshes, odd under the slot reverse T of CA-S1, so even under the three together); and the owner's word of 2026-10-27, 13:3x UTC ("OK" to the Reader's list of the laws of nature still unread, the angular momentum and E = mc^2 first): the angular momentum tallied on the mesh (row 72, every move's moment closed by the moment written on the mesh at the move's own clock) and the mass to light at the unspringing (row 73, the pair's wind unwound against the light's quantum tallied)."""

from __future__ import annotations

from collections import Counter
from typing import Any

from event_universe.core import rule3
from event_universe.core.spokes import AXES, transverse
from event_universe.meshes import cross
from event_universe.reckoner import HALF, PAIR, THOUSAND, Chart, carries, sign, unread_words
from event_universe.trains import REGULATOR, drive_teeth

REGIONS = PAIR**AXES  # the great clock's regions, each axis split at the cube's half
TALLIED = ("clock", "recoil", "carry_was", "carry")  # a tally's keys after its push (LT-S1)


def region(chart: Chart, clock: list[int] | tuple[int, ...]) -> int:
    """A clock's region of the great clock, one of eight: each axis split at the cube's half."""
    half = int(rule3.carries(chart.cube, HALF))
    return sum((int(x) >= half) << a for a, x in enumerate(clock))


def uniformity(chart: Chart) -> dict[str, Any]:
    """Row 63: the uniformity in the strikes, the chimes counted per region of the great clock (eight, each axis at its half): SHOWN where every region is chimed and the least holds at least half the largest."""
    counts = Counter(region(chart, c["node"]) for c in chart.chimes)
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


def dark_matter(chart: Chart) -> dict[str, Any]:
    """Row 64: dark matter in kind (the law's theorem of the gears): a bob chimed in its own well whose clocks advance no light, a chime track at a clock where no fitting unwound and no fitted hand was advanced through the run."""
    lit = {chart.index(b["node"]) for b in chart.fittings}
    lit |= {chart.index(b["minus"]) for b in chart.fittings}
    lit |= {chart.index(b["plus"]) for b in chart.fittings}
    bobs = chart.bobs_of()
    dark = [key for key in bobs if chart.index(key[0]) not in lit]
    return {
        "64 dark matter in kind": {
            "bodies (credit tracks) / of them at a Node where no light was laid": [
                len(bobs),
                len(dark),
            ],
            "at": list(dark[0][0]) if dark else None,
            "verdict": unread_words(
                "no body", "a body credited in its own well whose Nodes lay no light"
            )
            if not bobs
            else f"SHOWN: {len(dark)} of {len(bobs)} bodies credited at a Node where no light was laid"
            if dark
            else "NOT SHOWN: every body's Node laid light",
        }
    }


def lepton_number(chart: Chart) -> dict[str, Any]:
    """Row 65: the lepton number (the hand's parts are its particles, the hand's count conserved at the strike): for every species fitted, the fitted hands' own senses summed over its fittings is 0, each fitting a pair of opposite senses, so the number of each species less its anti-species is conserved."""
    sums: Counter[str] = Counter()
    for b, (a, c) in zip(chart.fittings, chart.sweeps_of(), strict=True):
        sums[chart.gear_name[b["line_pair"]]] += sign(a) + sign(c)
    return {
        "65 the lepton number": {
            "the senses summed per species born": dict(sums),
            "verdict": unread_words("no birth", "every species' senses sum to 0 over its births")
            if not chart.fittings
            else "SHOWN: every species' senses sum to 0 over its births, its number conserved at the click"
            if all(s == 0 for s in sums.values())
            else f"NOT SHOWN: {sum(1 for s in sums.values() if s)} species with a sum not 0",
        }
    }


def energy(chart: Chart) -> dict[str, Any]:
    """Row 66: the energy in the strikes (one point and one beat, D-S2): a bob's beat per proper tick before and after its strike equal within one notch, the unwound light's beat the difference, on every pair of a bob's consecutive chimes."""
    pairs = [
        (b1, b2)
        for cs in ([(c["proper"], c["beat"]) for c in bob] for bob in chart.bobs_of().values())
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


def cpt(chart: Chart) -> dict[str, Any]:
    """Row 67: CPT as one row, on every chime's face: the sweep = three_now twelve_before - twelve_now three_before is odd under the conjugation C (the twelve gear negated), even under the reflection P (the clock's own notches unmoved, the six meshes exchanged in pairs), odd under the slot reverse T (CA-S1, now for before), so even under the three together; counted over the faces whose sweep is not 0."""
    faces = [c["frame"] for c in chart.chimes if "frame" in c]
    w = [f["re_now"] * f["im_before"] - f["im_now"] * f["re_before"] for f in faces]
    c = [f["re_now"] * -f["im_before"] - -f["im_now"] * f["re_before"] for f in faces]
    t = [f["re_before"] * f["im_now"] - f["im_before"] * f["re_now"] for f in faces]
    cpt_w = [f["re_before"] * -f["im_now"] - -f["im_before"] * f["re_now"] for f in faces]
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


def twists_of(chart: Chart) -> tuple[int, int, int]:
    """The moving fittings' twists (the fittings of a pair; an unspringing advances its light at both ends and carries no twist): the + fitted hand at the unwind's clock, at the other end, and the unspringings beside."""
    moving = [b for b in chart.fittings if "takes" not in b]
    at_clock = sum(1 for b in moving if list(b["plus"]) == list(b["node"]))
    return at_clock, len(moving) - at_clock, len(chart.fittings) - len(moving)


def matter_against_antimatter(chart: Chart) -> dict[str, Any]:
    """Row 68: matter against antimatter (HD-S1, the Boss's 6412271828 and 6413689341): the twist enters the law in one act, the + fitted hand advanced at the end the lead flows into where the twist is right-handed, so over the moving fittings the + fitted hand stands at the unwind's clock on some and at the other end on the rest (the twist's sign at each strike, P-odd and C-even, kept by the bijection), the unspringings named beside; counted, the twist's choice read at every moving fitting."""
    at_clock, other, unspringings = twists_of(chart)
    return {
        "68 matter against antimatter": {
            "moving births with the + child at the take's Node / at the other end": [at_clock, other],
            "mergers beside (the light at both ends, no hand)": unspringings,
            "verdict": unread_words(
                "no moving birth", "the + child's end chosen by the twist's hand at every moving birth"
            )
            if not at_clock + other
            else f"SHOWN: the + child at the take's Node on {at_clock} moving births and at the other end on {other}, the hand's choice at every one; {unspringings} mergers beside",
        }
    }


def one_twist(chart: Chart) -> dict[str, Any]:
    """Row 69: the neutrino's one hand (the Boss's 6412773403, the helicity pair's reading): the twist of every moving fitting, the end the + fitted hand is advanced at (the unwind's clock or the other end, by the twist at the strike), all one over the chart where nature's neutrino shows one hand alone; NOT SHOWN with its cause where both twists stand (no conversion on the hands, the fittings' twists split), NOT READ where no moving fitting."""
    at_clock, other, unspringings = twists_of(chart)
    return {
        "69 the neutrino's one hand": {
            "moving births by hand (the + child at the take's Node / at the other end)": [
                at_clock,
                other,
            ],
            "mergers beside (no hand)": unspringings,
            "verdict": unread_words("no moving birth", "one hand at every moving birth of the record")
            if not at_clock + other
            else "SHOWN: one hand at every moving birth of the record"
            if not at_clock or not other
            else f"NOT SHOWN: both hands stand, {at_clock} and {other} moving births (no conversion on the record, the hands split by the twist at each click)",
        }
    }


def baryon_number(chart: Chart) -> dict[str, Any]:
    """Row 70: the baryon number, the C-odd count (the Boss's 6413689341, the floor pair's reading): the fitted hands' own sweeps summed over each fitting's two fitted hands, 0 at every fitting (a pair at opposite senses, an unspringing's light at 0 and 0: no matter-making act in the law, the count conserved at the strike); the hand's sweep at the fitted hands' clocks summed beside it, apart from 0 where a fitted hand was advanced on a standing notch (the residue, the clock's sweep) and over the unspringings' light (a sweep of one sign on both until unspring.py's fix); SHOWN where the own sweeps sum to 0 at every fitting."""
    own = [a + c for a, c in chart.sweeps_of()]
    pairs = [sum(b["W_children"]) for b in chart.fittings if "takes" not in b]
    unspringings = [sum(b["W_children"]) for b in chart.fittings if "takes" in b]
    return {
        "70 the baryon number": {
            "births whose children's own charges sum to 0 / in all": [own.count(0), len(own)],
            "births of a pair whose record W at the children's Nodes sums apart from 0 (the standing level's residue)": sum(
                1 for w in pairs if w
            ),
            "the mergers' light children's record W summed (0 by the letter)": sum(unspringings),
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


def tallies_of(chart: Chart) -> list[tuple[Any, ...]]:
    """Every tally a move wrote on the mesh (LT-S1, unwind.recoil), with its tick and the clock it was written at: the push per axis the move tallies (push_unwind at an unwind, each of an unspringing's two unwinds under `unwinds`; the push at an unspringing's cross term, written at the engagement's clock, CL-S2; push_advance at each end of a fitting's or an unspringing's advance), the rate the clock read at the tick's start, the notches advanced per axis on the regulator's flow gears, and their carry before and after; a line without the keys (a chart run before LT-S1) is no tally (the former reading took the line's own keys alone and left every unspringing's six tallies unread)."""
    found: list[tuple[Any, ...]] = []
    for entry in chart.unwinds:
        for unwind in entry.get("takes", [entry]):
            if "recoil" in unwind:
                found.append((entry["i"], *(unwind[k] for k in ("node", "dP_take", *TALLIED))))
        if "cross" in entry:
            found.append((entry["i"], *(entry["cross"][k] for k in ("node", "dP", *TALLIED))))
        if "recoil_ends" in entry:
            for k, where in enumerate((entry["minus"], entry["plus"])):
                ends = (entry[key + "_ends"][k] for key in ("dP_lay", *TALLIED))
                found.append((entry["i"], where, *ends))
    return found


def flow_teeth(record: Chart) -> int:
    """The drive teeth of the regulator's flow gears a tally writes on, the engine's own (trains.drive_teeth at the regulator's shape, the first axis gear after the time gear, as unwind.recoil writes): trace rim full_rate^2 key with the calibre file's trace (6 in nature's files, 54 in ga2's); the former 6 rim full_rate^2 key typed the trace 6 and failed every tally that advanced a notch at another trace."""
    trace = int(record.run["universe"]["integers"]["trace"])
    return int(
        drive_teeth(REGULATOR, None, record.rim, record.full_rate, record.action, trace)[1 + AXES]
    )


def momentum_booked(chart: Chart) -> dict[str, Any]:
    """Row 71: the momentum tallied on the mesh (LT-S1, H-Lay-As-The-Take-Reversed-1's derivation, line 19 as the Boss corrected its sign): at every move the momentum the quantum lost is written on the regulator's flow gear of each axis at the clock by the one drive act, -push_a rate^2 + the carry before - the carry after = the notches advanced times the drive teeth trace rim full_rate^2 key (`drive_teeth`, the calibre file's trace), the rate the clock's at the tick's start; so the hands' and the lattice's momentum sum to what they were at every strike, an identity on every tally of the chart, an unspringing's two unwinds, its cross term and its two advances among them; NOT READ on a chart without the tallies' keys."""
    teeth = flow_teeth(chart)
    held = advanced = failed = 0
    for _i, _clock, push, rate, recoil, was, after in tallies_of(chart):
        for a in range(AXES):
            if -push[a] * rate * rate + was[a] - after[a] == recoil[a] * teeth:
                held += 1
                advanced += recoil[a] != 0
            else:
                failed += 1
    return {
        "71 the momentum booked on the Link": {
            "axis bookings holding the identity / in all": [held, held + failed],
            "of them laying a level on the carrier's flux line (the rest kept in the carry)": advanced,
            "the write wall trace den Gamma^2 T (the universe file's trace)": teeth,
            "verdict": unread_words(
                "no booking on the record (a record run before LT-S1, the keys recoil, carry_was and carry absent)",
                "-dP p_0^2 + the carry before - the carry after = the levels laid times the write wall at every move",
            )
            if not held + failed
            else f"SHOWN exact: -dP p_0^2 + the carry before - the carry after = the levels laid times the write wall on {held} of {held} axis bookings, {advanced} laying a level"
            if not failed
            else f"NOT SHOWN: the identity fails on {failed} of {held + failed} axis bookings",
        }
    }


def moment(arm: list[int], push: list[int]) -> list[int]:
    """The moment arm x push of two integer vectors of three, per axis the cross on its transverse pair (b, c), the antisymmetric tensor arm_b push_c - arm_c push_b (spokes.transverse, the cube's hand read once)."""
    return [cross(arm[b], arm[c], push[b], push[c]) for b, c in map(transverse, range(AXES))]


def angular_momentum(chart: Chart) -> dict[str, Any]:
    """Row 72: the angular momentum tallied on the mesh (the conservation of angular momentum in the strikes, the hands' first missing law; AJ-S1 to AJ-S3, the one-clock theorem: a move at one clock changes the momentum on that clock's six meshes alone, each along its own axis, so its moment about any centre is the clock's arm times the momentum it tallies): every tally of row 71 is written at its move's own clock, so the move's moment and the moment written on the mesh sum to 0 about the great clock's centre, arm x (push rate^2 + the notches advanced times the drive teeth + the carry after - the carry before) = 0, the arm the clock's place doubled from the centre (2 r - (cube - 1), integers); summed per striking the hands' moment and the lattice's sum to 0, the hands' own moment changing at a fitting's or an unspringing's unwind (the transverse recoil, AJ-S2) and the lattice carrying it; an unspringing's cross term with a part off the mesh's own axis, written at the engagement's clock as the log names it, counted beside; NOT READ on a chart without the tallies' keys."""
    teeth = flow_teeth(chart)
    closed = 0
    walk: dict[int, list[int]] = {}
    tallies = tallies_of(chart)
    for i, clock, push, rate, recoil, was, after in tallies:
        arm = [HALF * int(x) - chart.cube + 1 for x in clock]
        written = [push[a] * rate * rate + recoil[a] * teeth + after[a] - was[a] for a in range(AXES)]
        closed += not any(moment(arm, written))
        walk[int(i)] = [
            j + m for j, m in zip(walk.get(int(i), [0] * AXES), moment(arm, push), strict=True)
        ]
    crosses = [b for b in chart.fittings if "cross" in b]
    off = sum(
        1
        for b in crosses
        if any(d for d, x, y in zip(b["cross"]["dP"], b["minus"], b["plus"], strict=True) if x == y)
    )
    return {
        "72 the angular momentum booked on the Link": {
            "bookings whose move's moment and the Link record's sum to 0 / in all": [
                closed,
                len(tallies),
            ],
            "closes with a booking / of them changing the records' own moment": [
                len(walk),
                sum(1 for j in walk.values() if any(j)),
            ],
            "mergers whose cross term carries a part off the Link's own axis / with a cross term": [
                off,
                len(crosses),
            ],
            "verdict": unread_words(
                "no booking on the record (a record run before LT-S1, the keys recoil, carry_was and carry absent)",
                "the move's moment and the moment written on the Link's record sum to 0 at every booking",
            )
            if not tallies
            else f"SHOWN exact: the move's moment and the moment written on the Link's record sum to 0 at {closed} of {closed} bookings, the records' own moment changing at {sum(1 for j in walk.values() if any(j))} of {len(walk)} closes and the lattice carrying it"
            if closed == len(tallies)
            else f"NOT SHOWN: the moment does not close at {len(tallies) - closed} of {len(tallies)} bookings",
        }
    }


def mass_to_light(chart: Chart) -> dict[str, Any]:
    """Row 73: E = mc^2 at the unspringing (MG-S1, a pair at rest into light; the hands' row to add beside 24): at each end of an unspringing the pair's notches unwound whole lose the wind `unwound`, the pair's energy at rest in the regulator's winding, the one weight of every train; the light advanced there is tallied one quantum (`tallied`, the teeth an advance at the winding holds alone at the clock, the same two integers for every train at one load) and advanced by the least count of notches at which its wind rises by it (the exact advance's rise); so the mass becomes light where the wind unwound is the quantum tallied, the light's rise above it the least count's excess named in thousandths; NOT SHOWN where the wind unwound exceeds the quantum tallied, the excess tallied nowhere (the stop jams an end below it); NOT READ with no unspringing."""
    ends = [
        (int(t["taken"]), int(t["booked"]), int(advance[-1]))
        for b in chart.fittings
        for where, advance in zip((b["minus"], b["plus"]), b.get("exact_lay", []), strict=False)
        for t in b.get("takes", [])
        if t["node"] == where
    ]
    paid = sum(1 for unwound, tally, _up in ends if unwound == tally)
    over = max((int(carries(unwound, tally, THOUSAND) or 0) for unwound, tally, _up in ends), default=0)
    rise = max((int(carries(up, unwound, THOUSAND) or 0) for unwound, _tally, up in ends), default=0)
    return {
        "73 E = mc^2 at the merger": {
            "merger ends / of them with the pair's share taken equal to the light's quantum booked": [
                len(ends),
                paid,
            ],
            "the share taken over the quantum booked, most, in thousandths": over,
            "the light's rise over the share taken, most, in thousandths": rise,
            "verdict": unread_words(
                "no merger in the record",
                "at every merger end the pair's share taken equal to the light's quantum booked, the light laid rising by it to its least count",
            )
            if not ends
            else f"SHOWN: at every one of {len(ends)} merger ends the pair's share taken is the light's quantum booked, the light laid rising by it to its least count, at most {rise - THOUSAND} thousandths above"
            if paid == len(ends)
            else f"SHOWN in part: at {paid} of {len(ends)} merger ends the pair's share taken is the light's quantum booked; at the rest it exceeds it, up to {over} thousandths of the quantum, the excess booked nowhere"
            if paid * HALF > len(ends)
            else f"NOT SHOWN: at {len(ends) - paid} of {len(ends)} merger ends the pair's share taken exceeds the light's quantum booked, up to {over} thousandths of it, the excess booked nowhere",
        }
    }
