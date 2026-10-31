"""DECODE3e's board records for the seed test's click part of (ii), made by the run tool's side, not the decoder's.

Big Pic's stage 1 edgeclick.py (st1/, copied unchanged from decode3d_frozen) runs node-live 1794d474b's src (nl/src)
on the shipped click world, 200 rounds, the first click (carried) and the third (turned), each from the lay as laid
and from the lay with one hidden unit in edge 1's tooth at Node-clock 0 (edgeclick's own hidden option, as Big Pic's
cmp.py). Each record is written with a header naming the world, the rounds, the sites, the edges, the dial and the
hidden unit (a board field, carried for the check), its click lines and sides (the click world's content), and the
board's passing per round, site and edge (edgeclick's flows: a board field, carried for the checks against the board's
passing). argv: the src, the output folder (relative to this file)."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("st1")))
import edgeclick as E  # noqa: E402  (its import puts argv[1], the src, on the path)

OUT = HERE.joinpath(sys.argv[2])
OUT.mkdir(exist_ok=True)
for turned in (0, 1):
    for hidden in (None, (0, 1)):
        rec = E.run(sys.argv[1], "tensor24-click", 200, turned, hidden)
        head = {"world": "tensor24-click", "rounds": 200, "sites": rec["sites"], "edges": rec["pairs"],
                "dial": rec["dial"], "born": rec["born"], "turned": turned,
                "hidden": None if hidden is None else list(hidden)}
        name = f"click_200_{turned}_{'hidden01' if hidden else 'laid'}.json"
        body = {"header": head, "lines": rec["lines"], "sides": rec["sides"], "passing": rec["flows"],
                "digest": rec["digest"]}
        OUT.joinpath(name).write_text(json.dumps(body), encoding="utf-8")
        print(f"{name}: lines {len(rec['lines'])}, sides {len(rec['sides'])}, books open {rec['books_open']} of"
              f" {rec['places']}, run back {rec['runback']}, digest {rec['digest'][:16]}")
