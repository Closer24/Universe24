"""Toy: example lines of the record's schema 1.2 as proposed, written from the draws the one rule makes (Animate;
Sofer's owed line (5) of 6494833685, schema 1.2; decision 40 (b); ANIMATE-SCHEMA-1.2/README.md).

Two boards are run by ANIMATE-SCHEDULER's run(), the one rule, and written as 1.2 lines: a pair whose second setting
is a machine hearing its first take (two split clicks at its birth, layers 1 and 2), and two quanta at one free slot
(a split click at each birth, then the slot's own split click, which takes one and refuses the other). Every split
click has one form: its members (each member's lay and its party there, G5), its joint histories (per member, the
site that takes it and the line of its frame it is taken on: a twin's 0 is +, 1 is -; a spread quantum's k is its
k-th absorber; at a slot, the slot where it is taken, or its giver's site where the slot refuses it), its sizes
(sigma_f; a slot's all alike), c over room and drawn (law 9), and its layer. Each take is a whole click naming its lay
(G5), with the frame it took in and the part it wrote (1.1's detector and written: the frame's first line and the
line taken, in axis form), one form for every take. Each refusal is a Books line at the slot, one quantum laid back to
its giver (5.1's books line), naming its lay. The lines are read by the decoder's own reader (schema 1.1's guards, the
1.2 fields unnamed) and by three 1.2 checks: every take and refusal names a lay; every draw is law 9's over its
sizes; every member goes where its draw's history says, taken there or refused there and laid back to its giver.

usage: python -I lines.py
"""

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "src"))
sys.path.insert(0, str(HERE.parent / "ANIMATE-SCHEDULER"))
import scheduler  # noqa: E402  the one rule, with ANIMATE-B-RECORD's hands and sizes

from tensor24.decoder import records  # noqa: E402

KINDS = ("whole", "split", "turnover", "rate", "books")
LAID = 1  # the round of every lay; a tick t after it is the round LAID + t


def run_logged(board, digits):
    """The one rule's run (scheduler.run), each band's draw logged: band, its birth, histories, sizes (sigma_f), the
    history drawn, the layer (the draw's count at its birth) and the digit."""
    log, layers = [], {}
    original = scheduler.drawn_weights

    def logging(board_, band, frame, drawn, joint):
        histories, sizes, checked = original(board_, band, frame, drawn, joint)
        b = board_["parts"][band[0]]["birth"]
        layers[b] = layers.get(b, 0) + 1
        n = digits.get(("birth", b), 0)
        log.append((band, b, histories, sizes, scheduler.law9(sizes, n), layers[b], n))
        return histories, sizes, checked

    scheduler.drawn_weights = logging
    try:
        out = scheduler.run(board, False, lambda key: digits.get(key, 0))
    finally:
        scheduler.drawn_weights = original
    return out, log


def reading(board, out, i, end):
    """A line of the frame part i's setting set, in 1.1's axis form (rho, spin): the detector's frame is its first
    line, the part written the line taken."""
    birth = board["births"][board["parts"][i]["birth"]]
    rho, spin = scheduler.axis(birth["frames"][birth["parts"].index(i)][out["frame"][i]][end])
    return {"train": board["parts"][i]["birth"], "rho": rho, "spin": list(spin)}


def split(round_, site, train, members, rows, sizes, n, drawn, layer):
    """A split click's line, one form for every draw."""
    line = {"kind": "split", "round": round_, "site": site, "count": round_, "train": train}
    line |= {"members": members, "parts": rows, "sizes": list(sizes)}
    return line | {"c": n % sum(sizes), "room": sum(sizes), "drawn": drawn, "layer": layer}


def written(board, out, log, digits):
    """The 1.2 lines of one run: each birth's lay; each band's split click at its birth, from the run's log; each
    slot's split click, from the run's state; each take; each refusal, laid back to its giver."""
    births, parts = board["births"], board["parts"]
    lines = [
        {"kind": "whole", "round": LAID, "site": birth["site"], "count": LAID, "train": b, "q": 1}
        for b, birth in enumerate(births)
    ]

    def member(i):
        return [LAID, births[parts[i]["birth"]]["site"], births[parts[i]["birth"]]["parts"].index(i)]

    for band, b, histories, sizes, drawn, layer, n in log:
        rows = [[[parts[i]["ends"][e][0], e] for i, e in zip(band, h, strict=True)] for h in histories]
        lines.append(
            split(
                LAID + births[b]["tick"],
                births[b]["site"],
                b,
                [member(i) for i in band],
                rows,
                sizes,
                n,
                drawn,
                layer,
            )
        )
    for slot, kept in out["slots"].items():
        arrivals, sets = scheduler.slot_sets(board, slot, board["slots"][slot], out["drawn"])
        rows = [
            [
                [slot[0] if i in s else births[parts[i]["birth"]]["site"], out["drawn"][i]]
                for i in arrivals
            ]
            for s in sets
        ]
        train, n = parts[arrivals[0]]["birth"], digits.get(("slot", *slot), 0)
        members = [member(i) for i in arrivals]
        lines.append(
            split(LAID + slot[1], slot[0], train, members, rows, [1] * len(sets), n, sets.index(kept), 1)
        )
    for i, e in out["drawn"].items():
        site, tick = parts[i]["ends"][e]
        lay = [LAID, births[parts[i]["birth"]]["site"]]
        event = {"round": LAID + tick, "site": site}
        if i in out["refused"]:
            lines.append(
                {"kind": "books"} | event | {"train": parts[i]["birth"], "kept": 1, "birth": lay}
            )
            continue
        take = (
            {"kind": "whole"}
            | event
            | {"count": LAID + tick, "train": parts[i]["birth"], "q": 1, "birth": lay}
        )
        take |= {"detector": reading(board, out, i, 0), "written": reading(board, out, i, e)}
        lines.append(take)
    return lines


def boards():
    """A pair at site 50: its first twin taken at 45 (tick 5), its second at 70 (tick 35), the second's frame set by
    the first's outcome, heard by light (25 sites in 30 ticks). Two quanta at sites 10 and 30, over x (4) and z (20),
    and over y (36) and z, both reaching z at tick 10, where one slot is free."""
    pair = {
        "site": 50,
        "tick": 0,
        "hand": scheduler.PAIR_HAND,
        "frames": scheduler.PAIR_BASES,
        "parts": [0, 1],
    }
    first = scheduler.detector(pair, 0, 45, 0)
    second = scheduler.detector(pair, 0, 70, 15, ((0, scheduler.RULE),))
    assert first["take"] + abs(first["site"] - second["site"]) < second["take"] - 1, (
        "heard outside the past cone"
    )
    tie = scheduler.quanta([[(4, 2), (20, 3)], [(36, 3), (20, 2)]], {(20, 10): 1})
    return (
        (
            "a pair, its second frame set by its first take",
            {"births": [pair], "parts": [first, second]},
            {("det", 0): 1, ("birth", 0): 3},
        ),
        (
            "two quanta, one free slot at z, both drawn to it",
            tie,
            {("birth", 0): 3, ("birth", 1): 4, ("slot", 20, 10): 1},
        ),
    )


def checks(lines):
    """Every take and every refusal names a lay; every draw is law 9's over its sizes; every member goes where its
    draw's drawn history says: taken there on the line it says (a frame of two lines: the first where the part
    written is the detector's own line, the second where it is the other), or refused there and laid back to its
    giver, or, at a slot that refuses it, sent back to its giver's site."""
    lays = {(e["round"], e["site"]) for e in lines if e["kind"] == "whole" and "birth" not in e}
    takes = [e for e in lines if e["kind"] == "whole" and "birth" in e]
    backs = [e for e in lines if e["kind"] == "books"]
    named = all(tuple(e["birth"]) in lays for e in takes + backs)
    lawful, placed = True, True
    for e in (e for e in lines if e["kind"] == "split"):
        lawful &= e["room"] == sum(e["sizes"]) and scheduler.law9(e["sizes"], e["c"]) == e["drawn"]
        for member, (site, end) in zip(e["members"], e["parts"][e["drawn"]], strict=True):
            taken = [
                int(t["written"] != t["detector"])
                for t in takes
                if t["birth"] == member[:2] and t["site"] == site
            ]
            refused = [b for b in backs if b["birth"] == member[:2] and b["site"] == site]
            sent = [
                b
                for b in backs
                if b["birth"] == member[:2] and b["site"] == e["site"] and site == member[1]
            ]
            placed &= taken == [end] or len(refused + sent) == 1
    return named, lawful, placed


def main():
    print(
        "Schema 1.2's lines, written from the draws the one rule makes (decision 40 (b)), and read back"
    )
    for name, board, digits in boards():
        out, log = run_logged(board, digits)
        lines = written(board, out, log, digits)
        lines.sort(key=lambda e: (e["round"], KINDS.index(e["kind"]), e["site"], e["train"]))
        head = {
            "kind": "header",
            "record": "lines.jsonl",
            "major": 1,
            "minor": 2,
            "engine": "a toy: ANIMATE-SCHEMA-1.2",
        }
        end = {"kind": "end", "rounds": max(e["round"] for e in lines)}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "lines.jsonl"
            path.write_text("".join(json.dumps(e) + "\n" for e in [head, *lines, end]), encoding="utf-8")
            _, cause = records.read(str(path))
        named, lawful, placed = checks(lines)
        print()
        print(
            f"{name}: the decoder's reader: {cause or 'read'}; every take and refusal names a lay: {named};"
        )
        print(
            f"  every draw law 9's over its sizes: {lawful}; every member where its draw's history says: {placed}"
        )
        for e in lines:
            print(f"  {json.dumps(e)}")


if __name__ == "__main__":
    main()
