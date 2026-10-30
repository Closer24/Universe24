"""Clock: the example world (examples/tensor24, the one bang on main: a cube of 4, light and the metric family, one gear
set, 10 rounds) run by the act as built through the runner itself, and by the edge act beside it, the record's end
digest and the ledger's count lines compared.
Algebra: the runner's digest, SHA-256 of the state's integers as one JSON text (runner/run.py, stated and digest).
Board: the metric family at 0, so every clock stands at its rest 6 den Gamma^2: a still clock.
Clicks: n/a; the record's click lines come with G5.

Run: <t24b>/.venv/bin/python -I probe_record.py > probe_record.txt
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import edge_lib as E  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load, run  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

HERE = Path(__file__).resolve().parent
WORLD = HERE.parent.joinpath("t24b", "examples", "tensor24")
PATHS = [WORLD.joinpath(name) for name in ("universe.json", "piece.json", "setting.json")]


def loaded_layout():
    """The example's layout and start as the runner lays them."""
    universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in PATHS)
    shape = piece["shape"]
    kinds, tables, square = main.made(load.star(len(shape)))
    held, found = load.load(universe, setting, sites_of(shape), kinds, tables, square)
    assert not found, found
    return main.layout(universe, shape, held), State(*held.state), held.trains, setting["ticks"]


def main_probe():
    record = HERE.joinpath("example.jsonl")
    found = run.run(main.ENGINE, PATHS, record)
    assert not found, found
    lines = [json.loads(line) for line in record.read_text(encoding="utf-8").splitlines()]
    end = lines[-1]
    ledger = [json.loads(line) for line in run.ledger_of(record).read_text(encoding="utf-8").splitlines()]
    layout, start, trains, ticks = loaded_layout()
    print("The example world (examples/tensor24): the act as built through the runner, and the edge act beside it")
    print(f"   The runner's record: rounds {end['rounds']}, exact {end['exact']}, digest {end['digest']}; ledger lines {len(ledger)}.")
    # the act as built, replicated here, to show the digest is the state's
    s = start
    for _ in range(ticks):
        s = step.tick(layout, s)
    built_digest = run.digest(run.stated(s))
    print(f"   The act as built, stepped here {ticks} rounds: digest {built_digest} ({'the same' if built_digest == end['digest'] else 'DIFFERENT'}).")
    w = step.teeth(layout, start)
    print(f"   The teeth at rest: {int(w[0, 0])} ({int(w[0, 0]).bit_length()} bits); the metric family's counts all 0: {bool((start.a[2:] == 0).all())}.")
    # the edge act, on the layout cut acyclic, from the corresponding state t = 4 r + 2 - D (r = 0 at every gear)
    cut = E.acyclic(layout)
    for name, t0 in (("t = 4 r + 2 - D, the built lay's tooth 0 read on the edge", None), ("t = 0, the edge's own birth at the middle", 0)):
        if t0 is None:
            se = E.to_edge(cut, start)
        else:
            se = State(start.a, start.b, start.r * 0, start.rd)
        states = [se]
        for _ in range(ticks):
            states.append(E.edge_tick(cut, states[-1]))
        e = states[-1]
        edge_digest = run.digest(run.stated(e))
        counts_built = [line["count"] for line in ledger]
        counts_edge = []
        for at, st in enumerate(states[1:], start=1):
            counts_edge.extend(line["count"] for line in run.counts(at, st, trains))
        same_counts = sum(int(list(x) == list(y)) for x, y in zip(counts_built, counts_edge, strict=True))
        back = e
        for _ in range(ticks):
            back = E.edge_untick(cut, back)
        exact = int(E.same(back, se))
        a_same = bool((e.a == s.a).all() and (e.b == s.b).all())
        print(f"   The edge act, {name}: digest {edge_digest}; the ledger's {len(counts_edge)} count lines equal the runner's in"
              f" {same_counts}; a and b at the end equal the act as built's: {a_same}; the run back exact: {exact};"
              f" the counts reach {E.bits(states)} bits (the law's 128).")
    print("   The record writes no tooth: the end's digest alone changes with the tooth's form; the count lines read a.")


if __name__ == "__main__":
    main_probe()
