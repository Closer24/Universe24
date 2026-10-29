"""The converter: the head's records written in the record's schema 1.1 (Animate's tool, outside src/tensor24).

A head record is one JSON object: the world and the universe, the per-interval nodes (the sites turned and frozen, X and
the winds) and the log (credit, birth, books, lay, refused). The schema 1.1 (src/tensor24/record/schema.py) is JSON Lines,
one object a line, in the order (round, kind, site, train): the header, then per round the whole clicks, the turnovers,
the rate lines and the books, and the end. A credit is a whole click at one Node-clock; a birth a fitting, its two
sites its children's, its books at the click where one end takes and in its ends where both take (a pair into light). No
refusal is written, and a field the head lacks is left out, so a reading that needs it reads not read, the cause named;
the header's runner names the record as converted. A whole click's train is the train its windings left, the taken
one, and its q is left out: the head counts its levels where its books count the amounts moved. The head ticks every
Node-clock once a round, so a click's count is its round. Its proper time, `proper`, is its dial summed: the ticks are its whole turns by the full rate (Rule3) and the
dial the remainder, and the rate lines are written so that they give exactly those ticks at each of its clicks (the head
records no beat between clicks). Its books are written as holdings of the amounts it moved: the taken train's windings
(amount, 0) and the laid train's (0, amount), the take's remainder as the taken holding's kept. Beside the record it
writes the ledger, <out>.ledger.jsonl: per round and train, the wind summed over every site, at "clicks" alone, since
the head writes its winds once a round, after the step and the clicks together.

Usage: python -I tools/tensor24_convert.py <head record .json> <out .jsonl> [engine commit]
"""

import hashlib
import json
import sys

KINDS = ("whole", "split", "turnover", "rate", "books")  # the events' order within a round, the schema's
SPOKES = (
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (1 + 1, 1),
    (1 + 1, -1),
)  # the six Spokes' order: +x, -x, +y, -y, +z, -z


def verbatim(name, obj):
    """One of the files, verbatim as the head holds it, with its digest."""
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return {"name": name, "text": text, "digest": hashlib.sha256(text.encode()).hexdigest()}


def holding(train, windings, kept=(0, 0)):
    """One train's holding at a click: its windings and its kept, before and after."""
    return {"train": train, "windings": list(windings), "kept": list(kept)}


def kept(e):
    """The take's remainder before and after a click, where the head writes both."""
    return (e["remainder_was"], e["remainder"]) if "remainder_was" in e and "remainder" in e else (0, 0)


def rate_lines(clicks):
    """(count, k) lines that give exactly the ticks t at each click's count c: each stretch's ticks first, then its rest."""
    lines, last, done_c, done_t = [], None, 0, 0
    for c, t in sorted(set(clicks)):
        ones, beats = t - done_t, c - done_c
        assert 0 <= ones <= beats, (c, t, done_c, done_t)
        for start, k, n in ((done_c + 1, 1, ones), (done_c + 1 + ones, 0, beats - ones)):
            if n and k != last:
                lines.append((start, k))
                last = k
        done_c, done_t = c, t
    return lines


def converted(head, engine):
    """The schema's lines for one head record, in the schema's order."""
    side = head["cube"]
    full = head["universe"]["integers"]["node_clock"]
    winding = head["T"]

    def site(node):
        x, y, z = node
        return (x * side + y) * side + z

    def spoke(near, far):
        """The Spoke's index in the six from the near end toward the far one, on the torus."""
        for axis, (a, b) in enumerate(zip(near, far, strict=True)):
            step = (b - a) % side
            if step:
                return SPOKES.index((axis, 1 if step == 1 else -1))
        return None

    header = {
        "kind": "header",
        "record": "tensor24",
        "major": 1,
        "minor": 1,
        "engine": engine,
        "runner": "converted from the head's record",
        "files": [verbatim("universe", head["universe"]), verbatim("world", head["world"])],
        "sides": [side, side, side],
        "order": "xyz",
        "classes": [],
        "kinds": [],
        "trains": [
            {"index": k, "label": f"plane {k}", "kinds": [], "part": 1, "winding": winding}
            for k, _ in enumerate(head["planes"])
        ],
        "couplings": [],
    }
    lines, ticked = [], {}
    for e in head["log"]:
        if e["event"] not in ("credit", "birth"):
            continue
        steps, dial = divmod(e["proper"], full)
        ticked.setdefault(site(e["node"]), []).append((e["i"], steps))
        line = {"kind": "whole", "round": e["i"], "site": site(e["node"]), "count": e["i"], "dial": dial}
        if e["event"] == "credit":
            line.update(
                train=e["taken_line"],
                winding=winding,
                sweep=e["sense"],
                push=e["dP_take"],
                taken=[holding(e["taken_line"], (e["taken"], 0), kept(e))],
                laid=[holding(e["line"], (0, e["booked"]))],
                ends=[],
                children=[],
            )
        else:
            ends = [e["minus"], e["plus"]]
            takes = e.get("takes", [])
            pushes = e.get("dP_lay_ends", [[0, 0, 0] for _ in ends])
            line.update(
                train=e["taken_row"],
                winding=winding,
                push=e["dP_take"],
                taken=[] if takes else [holding(e["taken_row"], (e["taken"], 0), kept(e))],
                laid=[] if takes else [holding(e["line_pair"], (0, e["booked"]))],
                ends=[
                    {
                        "site": site(t["node"]),
                        "spoke": spoke(t["node"], takes[1 - n]["node"]),
                        "taken": [holding(e["taken_row"], (t["taken"], 0), kept(t))],
                        "laid": [holding(e["line_pair"], (0, t["booked"]))],
                        "push": t["dP_take"],
                    }
                    for n, t in enumerate(takes)
                ],
                children=[
                    {"train": e["line_pair"], "site": site(end), "sweep": s, "push": p}
                    for end, s, p in zip(ends, e["senses"], pushes, strict=True)
                ],
            )
        lines.append(line)
    for e in head["log"]:
        if e["event"] == "books":
            for x, y, z, sign in e["booked"]:
                lines.append({"kind": "books", "round": e["i"], "site": site([x, y, z]), "kept": sign})
    for n in head["nodes"]:
        for s in n["turned"]:
            lines.append(
                {"kind": "turnover", "round": n["i"], "site": s, "count": n["i"], "q": 1, "x": n["X"][s]}
            )
    for s, clicks in ticked.items():
        for count, k in rate_lines(clicks):
            lines.append({"kind": "rate", "round": count, "site": s, "count": count, "k": k})
    lines.sort(key=lambda d: (d["round"], KINDS.index(d["kind"]), d["site"], d.get("train", 0)))
    back = head["run_back"]
    end = {"kind": "end", "rounds": head["intervals"], "undone": back["intervals"]}
    end["exact"] = 1 if back["exact"] == back["intervals"] else 0
    return [header, *lines, end]


def ledger(head):
    """The ledger beside the record: per round and train, the wind summed over every site, at "clicks" alone."""
    return [
        {"round": n["i"], "at": "clicks", "train": k, "wind": sum(int(w) for w in winds)}
        for n in head["nodes"]
        for k, winds in enumerate(n["winds"])
    ]


def write(lines, path):
    with open(path, "w") as f:
        for line in lines:
            f.write(json.dumps(line, separators=(",", ":")) + "\n")


def main():
    source, target, *rest = sys.argv[1:]
    engine = rest[0] if rest else "head"
    with open(source) as f:
        head = json.load(f)
    write(converted(head, engine), target)
    write(ledger(head), target.removesuffix(".jsonl") + ".ledger.jsonl")


if __name__ == "__main__":
    main()
