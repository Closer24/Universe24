"""The converter: the head's records written in the record's schema version 1 (Animate's tool, outside src/tensor24;
TENSOR24.md section 31; the schema as posted to the Boss in 6474766574, with its two corrections: a click's steps beside
its dial, and a books line).

A head record is one JSON object: the world and the universe, the per-interval nodes (the sites turned and frozen, X) and
the log (credit, birth, books, lay, refused). The schema is JSON Lines, one object a line, integers only, in the order
(round, kind, site, train):
  - the header: the record and its version, the engine, the runner, the files verbatim with their digests, the shape,
    the trains (the head's planes, light the plane whose pinion is the rim) and the seed as laid;
  - whole: a whole click; a credit is a chime at one Node-clock, a birth a fitting at two ends (a pair into light where
    the train taken is not light, its books then per end, in ends);
  - books: a remainder booked at a Node-clock, signed;
  - turnover: a Node-clock turned over, with its time gear's reading X;
  - rate: a Node-clock stops ticking (k 0) or is released (k 1);
  - end: the rounds and the rewind.
No refusal is written. A field the head lacks is left absent, so the decoder's rows that need it read not read, the cause
named. The head ticks every Node-clock once a round, so a click's count is its round; its proper time, the head's
`proper`, is the dial's whole turns and remainder by the Node-clock's full rate (Rule3).

Usage: python -I tools/tensor24_convert.py <head record .json> <out .jsonl> [engine commit]
"""

import hashlib
import json
import sys

RECORD = "tensor24.record"
VERSION = [1, 0]
KINDS = ("whole", "split", "books", "turnover", "rate")


def verbatim(obj):
    """The file as the head holds it, with its digest."""
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return {"text": text, "digest": hashlib.sha256(text.encode()).hexdigest()}


def present(**fields):
    """The fields the head holds; one it lacks stays absent."""
    return {k: v for k, v in fields.items() if v is not None}


def remainder(e):
    """The remainder before and after a click, where the head writes both."""
    if "remainder_was" in e and "remainder" in e:
        return {"before": e["remainder_was"], "after": e["remainder"]}
    return None


def converted(head, engine):
    """The schema's lines for one head record, in the schema's order."""
    side = head["cube"]
    full = head["universe"]["integers"]["node_clock"]
    winding = head["T"]
    planes = [int(p) for p in head["planes"]]

    def site(node):
        x, y, z = node
        return (x * side + y) * side + z

    def coordinates(index):
        rest, z = divmod(index, side)
        x, y = divmod(rest, side)
        return [x, y, z]

    def spoke(near, far):
        """The axis and the sense from the near end to the far one, on the torus."""
        for axis, (a, b) in enumerate(zip(near, far, strict=True)):
            step = (b - a) % side
            if step:
                return {"axis": axis, "sense": 1 if step == 1 else -1}
        return None

    def proper(e, round_):
        steps, dial = divmod(e["proper"], full)
        return {"round": round_, "count": round_, "steps": steps, "dial": dial}

    header = {
        "kind": "header",
        "record": RECORD,
        "version": VERSION,
        "engine": engine,
        "runner": "synchronous",
        "files": {"universe": verbatim(head["universe"]), "world": verbatim(head["world"])},
        "shape": {
            "sides": [side, side, side],
            "wrap": "torus",
            "sites": side * side * side,
            "order": "xyz",
        },
        "trains": [
            {
                "index": k,
                "label": f"plane {k}",
                "pinion": p,
                "winding": winding,
                "light": p == int(head["den"]),
            }
            for k, p in enumerate(planes)
        ],
        "seed": [e for e in head["log"] if e["event"] == "lay"],
    }
    lines = []
    for e in head["log"]:
        if e["event"] == "credit":
            line = {"kind": "whole", "site": site(e["node"]), **proper(e, e["i"])}
            line.update(
                present(
                    train=e["line"],
                    q=e.get("levels"),
                    winding=winding,
                    wind={"after": e["content"]},
                    sweep=e.get("sense"),
                    push=e.get("dP_take"),
                    taken=[{"windings": e["taken"]}] if "taken" in e else None,
                    laid=[{"train": e["line"], "windings": e["booked"]}] if "booked" in e else None,
                    remainder=remainder(e),
                )
            )
            lines.append(line)
        elif e["event"] == "birth":
            near, ends = e["node"], [e["minus"], e["plus"]]
            far = ends[0] if ends[1] == near else ends[1]
            line = {"kind": "whole", "site": site(near), **proper(e, e["i"])}
            pushes = e.get("dP_lay_ends", [None for _ in ends])
            line.update(
                present(
                    far=site(far),
                    spoke=spoke(near, far),
                    train=e["taken_row"],
                    q=e.get("levels"),
                    winding=winding,
                    wind={"after": e["content"]},
                    push=e.get("dP_take"),
                    taken=[{"train": e["taken_row"], "windings": e["taken"]}] if "taken" in e else None,
                    laid=[{"train": e["line_pair"], "windings": e["booked"]}] if "booked" in e else None,
                    remainder=remainder(e),
                    room=e.get("room"),
                    ends=[
                        present(
                            site=site(t["node"]),
                            taken=[{"train": e["taken_row"], "windings": t["taken"]}],
                            laid=[{"train": e["line_pair"], "windings": t["booked"]}],
                            remainder=remainder(t),
                            push=t.get("dP_take"),
                        )
                        for t in e["takes"]
                    ]
                    if "takes" in e
                    else None,
                    children=[
                        present(train=e["line_pair"], site=site(end), sweep=s, winding=w, push=p)
                        for end, s, w, p in zip(ends, e["senses"], e["W_children"], pushes, strict=True)
                    ],
                )
            )
            lines.append(line)
        elif e["event"] == "books":
            for x, y, z, sign in e["booked"]:
                lines.append({"kind": "books", "round": e["i"], "site": site([x, y, z]), "left": sign})
    stopped = set()
    for n in head["nodes"]:
        for s in n["turned"]:
            lines.append(
                {"kind": "turnover", "round": n["i"], "site": s, "count": n["i"], "q": 1, "x": n["X"][s]}
            )
        frozen = set(n["frozen"])
        for s in sorted(frozen - stopped):
            lines.append({"kind": "rate", "round": n["i"], "site": s, "count": n["i"], "k": 0})
        for s in sorted(stopped - frozen):
            lines.append({"kind": "rate", "round": n["i"], "site": s, "count": n["i"], "k": 1})
        stopped = frozen
    lines.sort(key=lambda d: (d["round"], KINDS.index(d["kind"]), d["site"], d.get("train", 0)))
    back = head["run_back"]
    end = {"kind": "end", "rounds": head["intervals"], "rewind": {"rounds": back["intervals"]}}
    end["rewind"]["exact"] = back["exact"] == back["intervals"]
    assert all(coordinates(site(c)) == c for c in ([0, 0, 0], [side - 1, 0, 1]))
    return [header, *lines, end]


def main():
    source, target, *rest = sys.argv[1:]
    engine = rest[0] if rest else "head"
    with open(source) as f:
        head = json.load(f)
    with open(target, "w") as f:
        for line in converted(head, engine):
            f.write(json.dumps(line, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
