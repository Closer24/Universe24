"""The table of gates: every row of UNIVERSE24's table (the nineteen and the widened 20 to 54) as one function of the record with its verdict and its numbers, shown, not shown, or not read with the predicate named where the record cannot carry it (`TABLE`, in the rows' order), and `gates(run)` reading them all with the event lines of the gates' first SHOWN (events.py); the rows read from the clicks are clicks.py's, the board's board.py's, the widened rows predicates.py's, and here 7 light absorbed, 9 the collisions, 11 the redshift, 12 the delay, 13 the free fall, 18 the arrow of time, 23 the momentum across the click, 25 the entropy of the clicks, the conservations and the three constants. Usage: `python -m event_universe.gates <record.json>`."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from collections.abc import Callable
from typing import Any

from event_universe import board, clicks, predicates
from event_universe.core.ports import AXES
from event_universe.decoder import HALF, HUNDRED, LISTED, PAIR, WIDTH, Record, quot

Row = Callable[[Record], dict[str, Any]]


def approach(record: Record) -> tuple[int, int, bool, list[int]]:
    """Two bodies' credited Nodes over the intervals (W-S4, W-S5): the distance between the two credited Nodes farthest apart at the first interval with two and at the last, whether two credited Nodes stood adjacent (one Link apart) at some interval, and the farthest distance per interval."""
    by_interval: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    for c in record.credits:
        by_interval[int(c["i"])].add(tuple(c["node"]))
    cube = int(record.run["cube"])

    def distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
        return sum(min(abs(x - y), cube - abs(x - y)) for x, y in zip(a, b, strict=True))

    spans = []
    adjacent = False
    for i in sorted(by_interval):
        nodes = sorted(by_interval[i])
        if len(nodes) < PAIR:
            continue
        spans.append(max(distance(a, b) for a in nodes for b in nodes if a < b))
        adjacent = adjacent or any(distance(a, b) == 1 for a in nodes for b in nodes if a < b)
    return (spans[0], spans[-1], adjacent, spans) if spans else (0, 0, False, [])


def collisions(record: Record) -> dict[str, Any]:
    """Gate 9: the collision from two bodies' credited Nodes approaching to adjacency (the sentences W-S4 and W-S5): SHOWN where they approach and stand one Link apart, NOT SHOWN where apart or receding, NOT READ with one body; a body's track is its record's credits by line, a move a credit of the same line at a new Node."""
    by_line: dict[int, list[tuple[int, tuple[int, ...]]]] = defaultdict(list)
    for c in record.credits:
        by_line[c["line"]].append((c["proper"], tuple(c["node"])))
    moves = 0
    for cs in by_line.values():
        cs.sort()
        seen = {cs[0][1]}
        for _p, at in cs[1:]:
            if at not in seen:
                moves += 1
                seen.add(at)
    first, last, adjacent, _spans = approach(record)
    if first == 0:
        verdict = "NOT READ: fewer than two bodies credited at one interval"
    elif adjacent and last <= first:
        verdict = "SHOWN: two bodies' credited Nodes approached and stood one Link apart"
    else:
        verdict = f"NOT SHOWN: the credited Nodes {'receding' if last > first else 'apart'}, farthest {first} Links at first and {last} at last"
    return {
        "9 collisions": {
            "tracks (node, line)": len({(tuple(c["node"]), c["line"]) for c in record.credits}),
            "lines credited at a new Node after their first": moves,
            "farthest credited Nodes at the first and the last interval with two": [first, last],
            "adjacent at some interval": adjacent,
            "verdict": verdict,
        }
    }


def free_fall(record: Record) -> dict[str, Any]:
    """Gate 13: the free fall where the closing of two bodies' credited Nodes quickens from interval to interval (the tail's second difference toward matter)."""
    first, _last, _adjacent, spans = approach(record)
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


def light(record: Record) -> dict[str, Any]:
    """Gate 7: light present and absorbed, the gap-0 line's quanta taken at the births and the credits (PC-S2); the gap-0 plane's own credits none in the engine's record (a detector is the toy's reading)."""
    takes = [entry for entry in record.log if entry["event"] in ("birth", "credit")]
    return {
        "7 light present and absorbed": {
            "gap-0 credits in the record": sum(1 for e in record.log if e["event"] == "detector"),
            "absorbed: the takes of the gap-0 line at births and credits (PC-S2)": len(takes),
            "levels taken in all": sum(int(entry["levels"]) for entry in takes),
            "at": takes[0]["node"] if takes else None,
            "verdict": "SHOWN: the gap-0 line's quanta absorbed at the takes, at matter (the credits) and at the births; its credit the taker's line (PC-S2)"
            if takes
            else "NOT READ: no take in the record",
        }
    }


UNREAD_LIGHT = "NOT READ: the record carries no credit of the gap-0 row (light has no period on the sea); the predicate: "


def redshift(record: Record) -> dict[str, Any]:
    """Gate 11: the gravitational redshift, the gap-0 credits' period longer where the content is deeper, by the clocks squared (EM-S4's predicate)."""
    return {
        "11 gravitational redshift": {
            "verdict": UNREAD_LIGHT
            + "the gap-0 credits' period longer where the content is deeper, by the clocks squared"
        }
    }


def delay(record: Record) -> dict[str, Any]:
    """Gate 12: light's delay or deflection, the gap-0 credits' first interval against the Link distance from the emitter (EM-S4's predicate)."""
    return {
        "12 light's delay or deflection": {
            "verdict": UNREAD_LIGHT
            + "the gap-0 credits' first interval against the Link distance from the emitter, later or off the line where deeper"
        }
    }


def arrow(record: Record) -> dict[str, Any]:
    """Gate 18: the arrow of time on the run back, exact bit for bit or not; read on the whole record alone."""
    rb = record.run.get("run_back")
    if record.intervals < int(record.run["intervals"]):
        verdict = "NOT READ: the run back is the whole record's"
    elif not rb:
        verdict = "NOT READ: the record carries no run back (the writer with back N)"
    elif rb["exact"] == rb["intervals"]:
        verdict = f"SHOWN: the run back exact bit for bit, {rb['exact']} of {rb['intervals']} intervals"
    else:
        verdict = f"NOT SHOWN: {rb['exact']} of {rb['intervals']}"
    return {"18 the arrow of time": {"run back on the record": rb, "verdict": verdict}}


def restated(key: str, source: Row, record: Record) -> dict[str, Any]:
    """A widened row that restates a gate of the nineteen: its verdict is that gate's, named."""
    gate, out = next(iter(source(record).items()))
    return {key: {"verdict": f"as gate {gate.split()[0]}: " + out["verdict"]}}


def redshift_of_light(record: Record) -> dict[str, Any]:
    """Row 29: the redshift of light, as gate 11."""
    return restated("29 the redshift of light", redshift, record)


def dilation_of_bodies(record: Record) -> dict[str, Any]:
    """Row 30: the dilation of two bodies' clocks, as gate 10."""
    return restated("30 the dilation", clicks.dilation, record)


def track_of_light(record: Record) -> dict[str, Any]:
    """Row 31: the deflection and the Shapiro delay, light's track, as gate 12."""
    return restated("31 the deflection and the Shapiro delay", delay, record)


def fall_by_tail(record: Record) -> dict[str, Any]:
    """Row 33: free fall by the tail, as gate 13."""
    return restated("33 free fall by the tail", free_fall, record)


def recoil(record: Record) -> dict[str, Any]:
    """Row 23: the momentum across the click (Compton's recoil), the close's dP_a on the click lines: the takes' and the lays' sums per axis and the births where the recoil passed to the laid pair (take + lay = 0)."""
    takes = [c["dP_take"] for c in record.credits + record.births if c.get("dP_take")]
    lays = [b["dP_lay"] for b in record.births if b.get("dP_lay")]
    passed = sum(
        1
        for b in record.births
        if b.get("dP_lay") and all(b["dP_take"][a] + b["dP_lay"][a] == 0 for a in range(AXES))
    )
    return {
        "23 the momentum across the click": {
            "clicks booking dP": len(takes),
            "takes dP_a summed": [sum(t[a] for t in takes) for a in range(AXES)],
            "lays dP_a summed": [sum(lay[a] for lay in lays) for a in range(AXES)],
            "recoil passed to the laid pair (take + lay = 0 per birth)": [passed, len(lays)],
            "verdict": "NOT READ: no click booked its momentum"
            if not takes
            else "NOT READ: no birth; the predicate: the take's dP and the lay's sum to 0 at every birth"
            if not lays
            else "SHOWN: the recoil passed to the laid pair at every birth"
            if passed == len(lays)
            else f"NOT SHOWN: the recoil passed at {passed} of {len(lays)} births (the lay's form owed)",
        }
    }


def constants(record: Record) -> dict[str, Any]:
    """The three constants: the count of integers per Node constant, every integer of the state and every transient within the width."""
    rows = record.rows
    counts_seen = sorted({r["integers"] for r in rows})
    state_bits = max((r["max bits"] for r in rows), default=0)
    transient_bits = max((r["max transient bits"] for r in rows), default=0)
    lacks = ("the count changes; " if len(counts_seen) != 1 else "") + (
        "the state past the width; " if state_bits > WIDTH else ""
    )
    lacks += "a transient past the width" if transient_bits > WIDTH else ""
    return {
        "the three constants": {
            "integers per Node": counts_seen,
            "max state bits": state_bits,
            "max transient bits": transient_bits,
            "first interval past the width": next(
                (r["i"] for r in rows if r["max transient bits"] > WIDTH or r["max bits"] > WIDTH), None
            ),
            "verdict": "SHOWN: the count constant, every integer and transient within the width"
            if not lacks and rows
            else "NOT SHOWN: " + lacks
            if rows
            else "NOT READ: no row",
        }
    }


def conservations(record: Record) -> dict[str, Any]:
    """The conservations in the clicks (the owner's word: what the lattice conserves is shown conserved in the clicks): the charge, the count, the energy as the beat unchanged from one click to the next, the momentum (row 23)."""
    births = record.births
    signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    booked, taken = sum(b["booked"] for b in births), sum(b["taken"] for b in births)
    beats: dict[tuple[tuple[int, ...], int], list[tuple[int, int]]] = defaultdict(list)
    for c in record.credits:
        beats[(tuple(c["node"]), c["line"])].append((c["proper"], c["beat"]))
    pairs = [
        (b1, b2)
        for cs in beats.values()
        for (_p1, b1), (_p2, b2) in zip(sorted(cs), sorted(cs)[1:], strict=False)
        if b1 > 0 and b2 > 0
    ]
    unchanged = sum(1 for a, b in pairs if a == b)
    return {
        "the conservations in the clicks": {
            "charge: the senses summed over the births": sum(signs),
            "count: taken against booked over the births (hundredths)": quot(taken, booked, HUNDRED),
            "energy: the beat (intervals per period) of a body unchanged from one click to the next": {
                "click pairs": len(pairs),
                "unchanged": unchanged,
                "changed by one": sum(1 for a, b in pairs if abs(a - b) == 1),
                "changed by more": sum(1 for a, b in pairs if abs(a - b) > 1),
            },
            "verdict": "SHOWN: the charge 0 over the births and the beat unchanged on most click pairs"
            if births and sum(signs) == 0 and pairs and unchanged * HALF > len(pairs)
            else "NOT SHOWN"
            if births and pairs
            else "NOT READ: no birth or no click pair",
        }
    }


def entropy(record: Record) -> dict[str, Any]:
    """Row 25: the entropy of the clicks as the law's integer: each birth's draw has its room (the count of numbers the one-Link read could give); H(t) = SUM over the births to t of bit_length(room - 1), read from the record alone, never falling."""
    total = last = 0
    found = []
    for b in sorted(record.births, key=lambda b: int(b["i"])):
        total += (int(b["room"]) - 1).bit_length()
        if b["i"] != last:
            found.append((b["i"], total))
            last = b["i"]
    return {
        "25 the entropy of the clicks rising": {
            "births with a room": len(record.births),
            "H at the end (bits)": total,
            "course (interval, H) at every eighth": found[:: max(1, len(found) // LISTED)],
            "verdict": f"SHOWN: H never falls (a sum of bit lengths), {total} bits over {len(record.births)} births"
            if record.births
            else "NOT READ: no birth",
        }
    }


TABLE: tuple[Row, ...] = (
    board.recurring_bang,
    board.tops,
    board.returns,
    clicks.lengthening,
    board.shortening,
    board.era,
    board.acceleration,
    board.contraction,
    light,
    clicks.families,
    clicks.species_track,
    collisions,
    clicks.dilation,
    redshift,
    delay,
    free_fall,
    board.horizon,
    clicks.conservation_at_click,
    clicks.one_click_floor,
    clicks.charge,
    arrow,
    clicks.mass_ratios,
    predicates.twist,
    predicates.hand_of_birth,
    predicates.coulomb,
    recoil,
    clicks.merger,
    entropy,
    predicates.lifts,
    predicates.confinement,
    predicates.conversion,
    redshift_of_light,
    dilation_of_bodies,
    track_of_light,
    predicates.perihelion,
    fall_by_tail,
    board.stopped_clock,
    predicates.dragging,
    predicates.shears,
    board.maxwell,
    predicates.aharonov_bohm,
    predicates.zeeman,
    predicates.photoelectric,
    predicates.two_beats,
    predicates.stern_gerlach,
    predicates.exclusion,
    predicates.velocity,
    board.well,
    board.same_gates,
    predicates.exact_take,
    predicates.black_body,
    predicates.decay,
    predicates.light_on_light,
    predicates.casimir,
    predicates.neutrino,
    predicates.binds,
    predicates.scattering,
    conservations,
    constants,
)


def verdicts(record: Record) -> dict[str, Any]:
    """Every row of the table read on the record (or on its cut)."""
    out: dict[str, Any] = {}
    for row in TABLE:
        out |= row(record)
    return out


def kind_of(verdict: str) -> str:
    """A verdict's kind (SHOWN, SHOWN in part, or NOT with SHOWN, READ or REACHED), a restated row's by the gate it restates."""
    words = (
        (verdict.split(": ", 1)[1] if verdict.startswith("as gate") else verdict)
        .replace(":", " ")
        .split()
    )
    in_part = ["in", "part"]
    whole = words[1 : 1 + len(in_part)] != in_part
    return (
        words[0]
        if words[0] == "SHOWN" and whole
        else " ".join(words[: PAIR if whole else 1 + len(in_part)])
    )


def gates(run: dict[str, Any]) -> dict[str, Any]:
    """Every gate's verdict with its numbers from the record alone, the decoder's line (the rows of the gates of the phenomena and their count by the verdict's kind, the count of SHOWN in Universe24), and the event lines of the gates' first SHOWN (events.first_shown)."""
    from event_universe import events  # the events read the table, after it

    record = Record(run)
    out = verdicts(record)
    out["the decoder"] = {
        "floats used": 0,
        "rows of the gates of the phenomena": len(TABLE),
        "rows by the verdict's kind (the numbered rows)": dict(
            Counter(kind_of(v["verdict"]) for k, v in out.items() if k.split()[0].isdigit())
        ),
        "readings": "quotients at a named scale, counts, bit lengths; rationals compared by cross multiplication",
    }
    out["events"] = events.first_shown(record, TABLE)
    return out


def main(argv: list[str]) -> None:
    """The gates of a record file, one line each."""
    with open(argv[1], encoding="utf-8") as record:
        for k, v in gates(json.load(record)).items():
            print(json.dumps({k: v}))


if __name__ == "__main__":
    main(sys.argv)
