"""Toy: example lines of the record's schema 1.2 as proposed, written from bands the one rule draws (Animate; Sofer's
owed line (5) of 6494833685, schema 1.2; ANIMATE-SCHEMA-1.2/README.md).

Two bands are drawn by ANIMATE-SCHEDULER's run(), the one rule, and written as 1.2 lines: a pair whose second setting
is a machine hearing its first take (two split clicks at its birth, layers 1 and 2), and two quanta joined by one free
slot (one split click at the absorber where they are one). Each band's split click names its members (each member's
lay and its party there, G5), its joint histories (per member, the site that takes it and the line of its frame it is
taken on: a twin's 0 is +, 1 is -; a spread quantum's k is its k-th absorber), sigma_f (sizes) and sigma_b (back,
G6), c over room and drawn (law 9), and its layer. Each take is a whole click naming its lay (G5), with the frame it
took in and the part it wrote (1.1's detector and written: the frame's first line and the line taken, in axis form),
one form for every take. The lines are read by the decoder's own reader (schema 1.1's guards, the 1.2 fields unnamed)
and by three 1.2 checks: every take names a lay; every draw is law 9's over sizes times back; every member is taken
where its band's drawn history says.

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
    """The one rule's run (scheduler.run), each band's draw logged: band, nodes, histories, products, sigma_f alone,
    the history drawn, and the layer (the draw's count at its birth)."""
    log, layers = [], {}
    original = scheduler.drawn_weights

    def logging(board_, band, nodes, frame, taken, joint):
        histories, weights, checked = original(board_, band, nodes, frame, taken, joint)
        bare = dict(board_) | {"slots": {}}  # sigma_f alone: the same products with no slot's sigma_b
        sizes = scheduler.band_weights(bare, band, frame, taken)[1]
        b = board_["parts"][band[0]]["birth"]
        layers[b] = layers.get(b, 0) + 1
        n = sum(digits.get(node, 0) for node in nodes)
        log.append((band, nodes, histories, weights, sizes, scheduler.law9(weights, n), layers[b], n))
        return histories, weights, checked

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


def written(board, out, log):
    """The 1.2 lines of one run: each birth's lay, each band's split click from the run's log, each take."""
    births, parts = board["births"], board["parts"]
    lines = [
        {"kind": "whole", "round": LAID, "site": birth["site"], "count": LAID, "train": b, "q": 1}
        for b, birth in enumerate(births)
    ]
    place = {("birth", b): (birth["site"], birth["tick"]) for b, birth in enumerate(births)}
    place |= {
        ("slot", *slot): slot for slot in board.get("slots", {})
    }  # each Node-clock that draws, and its tick
    for band, nodes, histories, weights, sizes, drawn, layer, n in log:
        members = [
            [LAID, births[parts[i]["birth"]]["site"], births[parts[i]["birth"]]["parts"].index(i)]
            for i in band
        ]
        rows = [[[parts[i]["ends"][e][0], e] for i, e in zip(band, h, strict=True)] for h in histories]
        back = []  # sigma_b: 0 where a history fills a slot past its free count
        for h in histories:
            ends = [parts[i]["ends"][e] for i, e in zip(band, h, strict=True)]
            back.append(
                int(all(ends.count(slot) <= free for slot, free in board.get("slots", {}).items()))
            )
        assert [s * b for s, b in zip(sizes, back, strict=True)] == list(weights), (
            "sizes times back are the products"
        )
        site, tick = place[nodes[0]]
        line = {
            "kind": "split",
            "round": LAID + tick,
            "site": site,
            "count": LAID + tick,
            "train": parts[band[0]]["birth"],
        }
        line |= {"members": members, "parts": rows, "sizes": list(sizes), "back": back}
        lines.append(
            line | {"c": n % sum(weights), "room": sum(weights), "drawn": drawn, "layer": layer}
        )
    for i, e in out["taken"].items():
        site, tick = parts[i]["ends"][e]
        lay = births[parts[i]["birth"]]["site"]
        take = {
            "kind": "whole",
            "round": LAID + tick,
            "site": site,
            "count": LAID + tick,
            "train": parts[i]["birth"],
        }
        take |= {"q": 1, "birth": [LAID, lay]}
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
        ("two quanta, one free slot at z", tie, {("slot", 20, 10): 13}),
    )


def checks(lines):
    """Every take names a lay; every draw is law 9's over sizes times back; every member is taken at the site, and on
    the line of its frame, its band's drawn history says (a frame of two lines: the first where the part written is
    the detector's own line, the second where it is the other)."""
    lays = {(e["round"], e["site"]) for e in lines if e["kind"] == "whole" and "birth" not in e}
    takes = [e for e in lines if e["kind"] == "whole" and "birth" in e]
    named = all(tuple(t["birth"]) in lays for t in takes)
    lawful, placed = True, True
    for e in (e for e in lines if e["kind"] == "split"):
        products = [w * b for w, b in zip(e["sizes"], e["back"], strict=True)]
        lawful &= e["room"] == sum(products) and scheduler.law9(products, e["c"]) == e["drawn"]
        for member, (site, end) in zip(e["members"], e["parts"][e["drawn"]], strict=True):
            found = [t for t in takes if t["birth"] == member[:2] and t["site"] == site]
            taken = [int(t["written"] != t["detector"]) for t in found]
            placed &= taken == [end]
    return named, lawful, placed


def main():
    print("Schema 1.2's lines, written from bands the one rule draws, and read back")
    for name, board, digits in boards():
        out, log = run_logged(board, digits)
        lines = written(board, out, log)
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
        print(f"{name}: the decoder's reader: {cause or 'read'}; every take names a lay: {named};")
        print(
            f"  every draw law 9's over sizes times back: {lawful}; every member taken where its history says: {placed}"
        )
        for e in lines:
            print(f"  {json.dumps(e)}")


if __name__ == "__main__":
    main()
