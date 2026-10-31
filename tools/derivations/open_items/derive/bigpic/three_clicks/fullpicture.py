"""The click world by the full picture (the owner's word of 04:2x UTC): every coupling at its table's entry, the key
the lay's own quantum, the hands laid apart below the key by the board's coordinates (VARY1's stand-in), the edge
teeth and their twins born at the birth (the earlier 'varied by the turn' was no change: the turn of the
birth is the birth); the three clicks read side by side: the books, the run back by the board's
law, and the law's own reading for one clock (one hidden unit in the giver-taker edge's tooth at Node-clock 0)."""
import sys
src, world, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, src); sys.path.insert(0, ".")
import edgeclick as E
for mode in [int(m) for m in (sys.argv[4] if len(sys.argv) > 4 else '02')]:
    a = E.run(src, world, rounds, mode, laid=True)
    b = E.run(src, world, rounds, mode, hidden=(0, 2), laid=True)
    la, lb = set(map(tuple, a["lines"])), set(map(tuple, b["lines"]))
    diff = sorted(la ^ lb)
    first = diff[0][0] if diff else None
    at = sorted({d[1] for d in diff})
    per_edge = [sum(abs(c) for (_, _, e, c) in a["sides"] if e == i) for i in range(len(a["pairs"]))]
    print(f"{world}, {E.NAMES[mode]}, {rounds} rounds: click places {a['places']}, books open {a['books_open']}; quanta per edge {per_edge};"
          f" run back {a['runback']}; digest {a['digest'][:16]}")
    print(f"   one hidden unit in the giver-taker edge's tooth at Node-clock 0: {len(diff)} click lines differ, the first at round {first}, at Node-clocks {at}")
