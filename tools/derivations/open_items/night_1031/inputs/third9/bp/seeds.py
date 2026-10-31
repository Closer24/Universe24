"""The owner's test (#2187, the owner's word of 05:3x UTC): a start seed and an end seed, past meeting future.

- From the start seed (the world's lay, every edge tooth and twin at the birth) the act runs forward and the clicks fall
  as they fall; the end seed is what it reaches: the board and the teeth.
- From the end seed alone, nothing kept from the forward run, everything runs back: the board by the engine's own run
  back (untick, the tick on the mirrored state mirrored), each round's passing read again from the board running back,
  and the teeth by the same act on the mirrored state (the twins flipped, every passing negated). It must reach the start
  seed exactly, board and teeth.
- Lays alike in every board count, one hidden unit apart in one edge tooth, write different clicks (the third click's
  choice), yet reach one end board, since the click writes nothing into the gears; the first click reaches it too.

Usage: python3 -I seeds.py <src> <world> <rounds> [mode, 4 unless given; 11 the triangle's own tooth, its hidden unit laid
in the twin of the edge's triangle]
"""
import hashlib
import sys

src, world_dir, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
mode = int(sys.argv[4]) if len(sys.argv) > 4 else 4
sys.path.insert(0, src)
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

universe, shape, held, lay, s0, world = E.load_world(src, world_dir)
kinds_of = [t["kinds"] for t in universe["trains"]]
rows, sites = s0.a.shape
ed = E.Edges(world, int(lay.click.key[0, 0]), sites, kinds_of)
B, n = ed.born, len(ed.pairs)


def board_digest(s):
    return hashlib.sha256(repr([x.tolist() for x in s]).encode()).hexdigest()


def flows(s, s1, x):
    b = [int(s.b[r, x]) for r in range(rows)]
    a = [int(s.a[r, x]) for r in range(rows)]
    a1 = [int(s1.a[r, x]) for r in range(rows)]
    return world.split_flows(0, b, a, a1)


def forward11(hidden=None):
    import circ

    st = circ.Stepper(ed)
    teeth = [st.born() for _ in range(sites)]
    if hidden is not None:
        x, e = hidden
        for t in [t for t in range(len(st.sign)) if e in st.sign[t]][:1]:
            teeth[x][2][t] = st.B3 + st.cen(teeth[x][2][t] - st.B3 + 1)
    s, lines = s0, []
    for t in range(rounds):
        s1, _ = step.act(lay, s)
        for x in range(sites):
            fl = flows(s, s1, x)
            qe = st.step([fl.get(pr, 0) for pr in ed.pairs], *teeth[x])
            lines += [(t, x, e, c) for e, c in enumerate(qe) if c]
        s = s1
    return s, teeth, st, lines


def backward11(st, s_end, teeth):
    back = [(list(gs), list(ts), st.flip(es)) for gs, ts, es in teeth]
    s = s_end
    for _ in range(rounds):
        sp = step.untick(lay, s)
        for x in range(sites):
            fl = flows(sp, s, x)
            st.step([-fl.get(pr, 0) for pr in ed.pairs], *back[x])
        s = sp
    return s, [(gs, ts, st.flip(es)) for gs, ts, es in back]


def forward(m, hidden=None):
    if m == 11:
        s, teeth, _, lines = forward11(hidden)
        return s, teeth, None, lines
    teeth = [[B] * n for _ in range(sites)]
    twins = [[B] * n for _ in range(sites)]
    if hidden is not None:
        x, e = hidden
        teeth[x][e] = B + ed.cen(teeth[x][e] - B + 1)
    fw = ed.forward(m) if m >= 2 else []
    bw = list(reversed(fw))
    s, lines = s0, []
    for t in range(rounds):
        s1, _ = step.act(lay, s)
        for x in range(sites):
            fl = flows(s, s1, x)
            u, w = teeth[x], twins[x]
            ed.shear_all(u, w, fw)
            for e, pr in enumerate(ed.pairs):
                c, u[e] = carry(fl.get(pr, 0), ed.dial, u[e])
                if c:
                    lines.append((t, x, e, c))
            ed.shear_all(u, w, bw)
        s = s1
    return s, teeth, twins, lines


def backward(m, s_end, teeth, twins):
    fw = ed.forward(m) if m >= 2 else []
    bw = list(reversed(fw))
    u_all = [list(u) for u in teeth]
    w_all = [[B + ed.cen(-(v - B)) for v in w] for w in twins]
    s = s_end
    for _ in range(rounds):
        sp = step.untick(lay, s)
        for x in range(sites):
            fl = flows(sp, s, x)
            u, w = u_all[x], w_all[x]
            ed.shear_all(u, w, fw)
            for e, pr in enumerate(ed.pairs):
                _, u[e] = carry(-fl.get(pr, 0), ed.dial, u[e])
            ed.shear_all(u, w, bw)
        s = sp
    w_all = [[B + ed.cen(-(v - B)) for v in w] for w in w_all]
    return s, u_all, w_all


print(f"{world_dir}, {rounds} rounds, {E.NAMES[mode]}: key {int(lay.click.key[0, 0])}, dial {ed.dial}, edges {ed.pairs}")
if mode == 11:
    end, teeth11, st11, lines = forward11()
    start_digest, end_digest = board_digest(s0), board_digest(end)
    print(f"  the start seed's board {start_digest[:16]}; the end seed's board {end_digest[:16]}; {len(lines)} click sides on the way")
    back, teeth_back = backward11(st11, end, teeth11)
    board_ok = board_digest(back) == start_digest
    teeth_ok = teeth_back == [tuple(list(v) for v in st11.born()) for _ in range(sites)]
else:
    end, teeth, twins, lines = forward(mode)
    start_digest, end_digest = board_digest(s0), board_digest(end)
    print(f"  the start seed's board {start_digest[:16]}; the end seed's board {end_digest[:16]}; {len(lines)} click sides on the way")
    back, u_back, w_back = backward(mode, end, teeth, twins)
    board_ok = board_digest(back) == start_digest
    teeth_ok = u_back == [[B] * n for _ in range(sites)] and w_back == [[B] * n for _ in range(sites)]
print(f"  from the end seed alone, run back: the board reaches the start seed: {board_ok}; every tooth and twin reaches the birth: {teeth_ok}")
first_end, _, _, first_lines = forward(0)
print(f"  the first click from the same start: the end board is the same: {board_digest(first_end) == end_digest};"
      f" its click sides differ from the third click's at {len(set(first_lines) ^ set(lines))}")
ok = board_ok and teeth_ok and board_digest(first_end) == end_digest
for e in range(n):
    h_end, _, _, h_lines = forward(mode, hidden=(0, e))
    same_end = board_digest(h_end) == end_digest
    moved = set(h_lines) ^ set(lines)
    at = sorted({d[1] for d in moved})
    print(f"  one hidden unit in edge {ed.pairs[e]}'s tooth at Node-clock 0: the click sides differ at {len(moved)}"
          f" (at Node-clocks {at}), and the end board is the same: {same_end}")
    ok = ok and same_end
print(f"the clicks differ, the end is the same, and the end runs back to the start: {ok}")
sys.exit(0 if ok else 1)
