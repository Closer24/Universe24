"""THIRD5's fold probe, the triangle form (third5.act5, who "triangle"), for the readers' THIRD4 minors:
(a) the shear mutant's run back; (b) the largest |lam| over the window (the lay's regime condition); (c) the third click's
own record with honest fields (the schema's tooth the train's term-11 click tooth, the share tooth in a field of its
own, q the gears' move along the giver's give), read by C5 and from its lines alone: the takes per taker, the takes in a
row by one taker, the places' residues mod the old stride; (d) term 11's books with the triangle acting, place-wise by
C5 and in event order; (e) 2E' of the three hands against the plain act over 24,000 rounds; (f) an empty taker's wait.
Whole numbers only; Rule3's carry the one division; paths by joinpath."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np
import world_load
import third5
from tensor24.algebra.carry import carry
from tensor24.engine import step
from tensor24.engine.contract import contract
from tensor24.runner import run as R
from tensor24.decoder import records, shadow
universe, piece, setting, loaded, layout, start = world_load.world("world")
roles = world_load.roles(loaded, setting)
c4 = json.loads(HERE.joinpath("world", "third.json").read_text(encoding="utf-8"))["chosen4"]
c5 = json.loads(HERE.joinpath("world", "third.json").read_text(encoding="utf-8"))["chosen5"]
cfg = third5.Third(c5["strength"], c4["dial"], tuple(c4["weights"]), c4["share_dial"])
third5.TRIANGLE_DIAL[0] = c5["triangle_dial"]
out = HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "probe5x.txt").open("w", encoding="utf-8")
say = lambda *w: (out.write(" ".join(str(x) for x in w) + "\n"), out.flush())  # noqa: E731
same = lambda x, y: all(np.array_equal(p, q) for p, q in zip(x, y))  # noqa: E731
zr = 0 * start.a[roles.giver]
x0 = (zr, np.stack([zr] * roles.takers.shape[0]))
tr = loaded.trains
hands = [ti for ti in range(len(tr)) if int(tr.tied[ti]) == 1]
rows_of = {ti: np.arange(int(tr.first[ti]), int(tr.first[ti] + tr.size[ti]), dtype=np.intp) for ti in hands}
giver_t = [ti for ti in hands if int(tr.first[ti]) == int(roles.giver[0])][0]
taker_t = [ti for ti in hands if ti != giver_t]
# (a) the shear mutant's run back, from the warm board
s, x = start, x0
for _ in range(3000):
    s, x, _, _ = third5.act5(layout, roles, cfg, s, x, "triangle")
warm, warmx = s, x
s, x = warm, warmx
fail, first = 0, None
for r in range(1, 2001):
    s1, x1, _, rd = third5.act5(layout, roles, cfg, s, x, "triangle", "shear")
    b, bx, _, _ = third5.untick5(layout, roles, cfg, s1, x1, "triangle", "shear")
    bad = not (same(b, s) and same(bx, x)); fail += int(bad); first = r if (first is None and bad) else first
    s, x = s1, x1
say(f"(a) the shear mutant (the push written into the stored before slot), from the warm board: the one-round run back fails at {fail} of 2000 rounds, first at {first}")
# (b) to (f): 24,000 rounds from the lay, the triangle and the plain act side by side
def e2(a, b, a1):
    rows = np.concatenate((roles.giver, roles.takers.reshape(-1)))
    j = contract(layout.plan, step.valued(a), a)
    w = layout.gearing.rest[rows, 0]
    return int((w * (a1[rows, 0] - a[rows, 0]) * (a[rows, 0] - b[rows, 0]) - a[rows, 0] * j[rows, 0]).sum())
s, x, p = start, x0, start
lines3, lines11, big = [], [], 0
e_start = None
lo = hi = plo = phi = 0
first_land = {ti: None for ti in taker_t}
for r in range(1, 24001):
    s1, x1, c11, rd = third5.act5(layout, roles, cfg, s, x, "triangle")
    p1, _ = step.act(layout, p)
    big = max(big, int(np.abs(rd["lam"]).max()))
    u = rd["delta"][:, 0]  # the giver's give, SUM lam
    for ti in hands:
        qq = int(((s1.a[rows_of[ti], 0] - rd["a0"][rows_of[ti], 0]) * u).sum())
        if qq != 0:
            line = {"kind": "click", "round": r, "site": 0, "train": ti, "q": qq, "tooth": [int(s.k[ti, 0]), int(s1.k[ti, 0])]}
            if ti in taker_t:
                i = taker_t.index(ti)
                line["share tooth"] = [int(x[1][i, 0, 0]), int(x1[1][i, 0, 0])]
                first_land[ti] = r if first_land[ti] is None else first_land[ti]
            lines3.append(line)
    lines11 += R.clicked(r, s, s1, c11)
    ec, ep = e2(s.a, s.b, s1.a), e2(p.a, p.b, p1.a)
    if e_start is None:
        e_start, pe_start = ec, ep
    dc, _ = carry((ec - e_start) * 1000000, e_start, 0)
    dp, _ = carry((ep - pe_start) * 1000000, pe_start, 0)
    lo, hi, plo, phi = min(lo, dc), max(hi, dc), min(plo, dp), max(phi, dp)
    s, x, p = s1, x1, p1
say(f"(b) the largest |lam_i| over 24,000 rounds from the lay: {big} (the regime condition k max|a_giver| max s_i < D)")
files = [(pp, pp.read_text(encoding="utf-8")) for pp in (HERE.joinpath("world", n) for n in world_load.NAMES)]
kinds_, _, _ = world_load.made(3)
for name, lines in (("rec5x_third.jsonl", lines3), ("rec5x_term11.jsonl", lines11)):
    path = HERE.joinpath(name)
    head = R.header(path, files, universe, piece["shape"], kinds_, loaded, layout)
    endl = {"kind": "end", "rounds": 24000, "digest": R.digest(R.stated(s)), "undone": 0, "exact": 0}
    path.write_text("".join(json.dumps(y) + "\n" for y in [head, *lines, endl]), encoding="utf-8")
    rec, cause = records.read(str(path))
    v = shadow.shadow(rec) if rec is not None else None
    bk = v["the books at each click"] if v else None
    cn = v["the cone check by click (D8)"] if v else None
    say(f"(c/d) {name}: {len(lines)} lines; C5 books: {bk['kind'] if bk else 'NOT READ ' + cause}: {bk['cause'] if bk else ''}; cone: {cn['kind'] if cn else ''}")
# (c) the takes from the lines alone
takes = [ln for ln in lines3 if ln["train"] in taker_t]
per = {ti: sum(1 for ln in takes if ln["train"] == ti) for ti in taker_t}
places = sorted({ln["round"] for ln in lines3})
by_round = {}
for ln in takes:
    by_round.setdefault(ln["round"], []).append(ln["train"])
seq = [tuple(sorted(by_round[rr])) for rr in sorted(by_round)]
repeats = sum(1 for i in range(1, len(seq)) if seq[i] == seq[i - 1])
both = sum(1 for sq in seq if len(sq) > 1)
residues = sorted({carry(rr, 8, 0)[1] for rr in places})
gaps = [places[i] - places[i - 1] for i in range(1, len(places))]
say(f"(c) from the lines alone: takes per taker {per}; places {len(places)}; places where both takers take {both}; successive places taken by the same taker or takers {repeats} of {len(seq) - 1}; the places' residues mod 8 {residues}; the gaps from {min(gaps)} to {max(gaps)} rounds")
# (d) term 11's books in event order
run, lo11, hi11 = 0, 0, 0
for ln in lines11:
    run += ln["q"]; lo11 = min(lo11, run); hi11 = max(hi11, run)
say(f"(d) term 11 with the triangle acting, in event order: SUM q over the window {run}, the running sum within [{lo11}, {hi11}]")
say(f"(e) 2E' of the three hands about its start over 24,000 rounds, in ppm: with the triangle {lo} / +{hi}; the plain act {plo} / +{phi}")
say(f"(f) the first landing round per taker from the lay (the first taker laid empty): {first_land}")
say("done")
