"""MIN2: every tooth side, plan term and product of one Node-clock split by cause, and the three forms run against the
engine's own act. The causes: (a) the act's form (the own diagonal; a term landing on the unit row); (b) the world's
structure (dead with every CHOSEN strength but the key set to 1, the loader's own load() run again); (c) dead only by a
strength the file chose as 0; live. The forms: AB = (a) and (b) dropped (teeth and terms), D3, S1 as like monomials
combined at the load; ABC = AB and (c); ABC+D1 = ABC with one tooth per live edge. Each is compared with the engine in
every round (a, b, r, rd, every tooth read back, every click read back, run.clicked's lines), then the end line's teeth
and the digest on the state read back, then each form's run back from its own reduced end alone.
Whole numbers only; Rule3's carry the one division. argv: tree world rounds [variant folder]."""
import copy
import json
import sys
from pathlib import Path

here = Path(sys.argv[0]).resolve().parent
sys.path.insert(0, str(here))
import world as W  # noqa: E402

tree, name, rounds = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
variant = Path(sys.argv[4]) if len(sys.argv) > 4 else None
W.tree_on(tree)
import numpy as np  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Plan, Read, State  # noqa: E402
from tensor24.runner import files, plans  # noqa: E402
from tensor24.runner import load as L  # noqa: E402
from tensor24.runner import run as R  # noqa: E402

wpath = variant if variant else tree.joinpath("examples", name)
u0, st, shape, kinds, ld0, lay0, s0 = W.loaded(tree, wpath)
u1 = copy.deepcopy(u0)
for nm in u1["chosen"]:
    if nm != "key":
        u1["chosen"][nm] = 1
kinds_, tables, square, lifted = main.ENGINE.made(files.star(len(shape)))
ld1, found = L.load(u1, st, files.sites_of(shape), kinds_, tables, square, lifted)
assert not found, found
lay1 = main.ENGINE.layout(u1, shape, ld1)
T = len(ld0.trains)
rows, sites = s0.a.shape
n = lay0.nb.shape[0]
K = int(lay0.click.key[0, 0])
senses, _ = carry(n, lay0.spokes.shape[1], 0)
birth, _ = carry(K - 1, senses, 0)
print("WORLD", name, wpath.name if variant else "", "chosen", u0["chosen"], "trains", T, "rows", rows, "sites", sites,
      "rounds", rounds)
print("KEY edge key", K, "(strengths at 1:", int(lay1.click.key[0, 0]), ") birth by the load's carry", birth,
      "; header's birth (the full k's [0, 0])", int(s0.k[0, 0]), "; header's dial", int(lay0.click.key[0, 0]),
      "; distinct keys over the sides", len(set(lay0.click.key.reshape(-1).tolist())))

# ---- the teeth by cause, per Node-clock
p0, p1 = R.joined(lay0.click, T), R.joined(lay1.click, T)
e0, e1 = set(R.crossed(lay0.click, T)), set(R.crossed(lay1.click, T))
own0 = {(t, v) for t, ps in enumerate(p0) for v in ps}
own1 = {(t, v) for t, ps in enumerate(p1) for v in ps}
assert own0 <= own1 and e0 <= e1
cls = {}
for reach in range(1 + n):
    for t in range(T):
        for v in range(T):
            i = (reach * T + t) * T + v
            if reach == 0 and t == v:
                cls[i] = "a"
            elif reach == 0:
                cls[i] = "live" if (t, v) in own0 else ("c" if (t, v) in own1 else "b")
            else:
                side = (reach - 1, t, v)
                cls[i] = "live" if side in e0 else ("c" if side in e1 else "b")
count = {c: sum(1 for x in cls.values() if x == c) for c in ("a", "b", "c", "live")}
print("TEETH per Node-clock: laid", len(cls), count)
two = np.flatnonzero(lay0.gearing.drive.reshape(-1) != 1)
print("STATE per Node-clock: engine", 4 * rows + len(cls), "; AB (a, b dropped, D3)", 3 * rows + len(two) + count["c"] + count["live"],
      "; ABC", 3 * rows + len(two) + count["live"])

# ---- S1: like monomials combined at the load, by their legs alone (sorted), every monomial, factors summed
def combined(pot):
    factor, legs = pot
    key_of, keep, f2 = {}, [], []
    for i in range(len(factor)):
        canon = tuple(sorted(int(x[i]) for x in legs))
        if canon in key_of:
            f2[key_of[canon]] = f2[key_of[canon]] + factor[i]
        else:
            key_of[canon] = len(keep)
            keep.append(i)
            f2.append(factor[i])
    keep = np.asarray(keep, dtype=np.intp)
    return (np.asarray(f2, dtype=object), tuple(x[keep] for x in legs))


def relaid(u, ld):
    pot = combined(ld.potential)
    click = plans.edging(ld.trains, pot, u["chosen"]["key"], lay0.spokes)
    ld2 = ld._replace(potential=pot, click=click)
    return main.layout(u, shape, ld2), len(ld.potential[0]), len(pot[0])


lay0c, m_before, m_after = relaid(u0, ld0)
lay1c, _, _ = relaid(u1, ld1)
print("S1 combine like monomials: monomials", m_before, "->", m_after, "; edge key unchanged",
      int(lay0c.click.key[0, 0]) == K, "; J terms", len(lay0.plan.factor), "->", len(lay0c.plan.factor))

# ---- the terms and the products by cause (per Node-clock per round)
def term_class(f0, f1, unit=None):
    f0, f1 = np.asarray(f0, dtype=object), np.asarray(f1, dtype=object)
    out = np.where(f1 == 0, "b", np.where(f0 == 0, "c", "live")).astype(object)
    if unit is not None:
        out = np.where(unit, "a", out).astype(object)
    return out


def tally(classes, cost):
    return {c: int((np.asarray(classes) == c).sum()) * cost for c in ("a", "b", "c", "live")}


def add(*ds):
    return {c: sum(d[c] for d in ds) for c in ("a", "b", "c", "live")}


def census(l0, l1, label):
    unit = np.asarray(l0.plan.target) == -1
    j = term_class(l0.plan.factor, l1.plan.factor, unit)
    w0 = np.asarray([int((row != 0).any()) for row in l0.click.weight], dtype=object)
    w1 = np.asarray([int((row != 0).any()) for row in l1.click.weight], dtype=object)
    jp = np.where(unit, "a", np.where(w1 == 0, "b", np.where(w0 == 0, "c", "live"))).astype(object)
    mesh = term_class(l0.mesh.factor, l1.mesh.factor)
    push = term_class(l0.push.factor, l1.push.factor)
    clock = term_class(l0.clock.factor, l1.clock.factor)
    read = term_class(l0.stretch.factor, l1.stretch.factor)
    across = term_class(l0.click.across.reshape(-1), l1.click.across.reshape(-1))
    parts = {
        "J contract (3 / term)": tally(j, 3),
        "passing (4 + T / J term)": tally(jp, 4 + T),
        "Mesh plan (3 / term)": tally(mesh, 3),
        "push (3 / term)": tally(push, 3),
        "clocks' read (5 calls x 1 / term)": tally(clock, 5),
        "grips' read (1 / term)": tally(read, 1),
        "crossing (3 / coupling entry)": tally(across, 3),
    }
    for k_, v in parts.items():
        print(f"  {label} {k_}: {v}")
    total = add(*parts.values())
    per_row = 45 * rows
    allp = sum(total.values()) + per_row
    print(f"  {label} PRODUCTS: by cause {total}; the board's per-row work (45 R, live) {per_row}; all {allp}")
    share = {c: (1000 * total[c]) // allp for c in total}
    print(f"  {label} SHARE per mille of all: {share}; per-row {(1000 * per_row) // allp}")
    print(f"  {label} terms J {dict((c, int((j == c).sum())) for c in ('a', 'b', 'c', 'live'))}, Mesh plan"
          f" {dict((c, int((mesh == c).sum())) for c in ('b', 'c', 'live'))}, push {dict((c, int((push == c).sum())) for c in ('b', 'c', 'live'))},"
          f" clock {dict((c, int((clock == c).sum())) for c in ('b', 'c', 'live'))}, grips' read {dict((c, int((read == c).sum())) for c in ('b', 'live'))},"
          f" across {dict((c, int((across == c).sum())) for c in ('b', 'c', 'live'))}")
    return j, jp, mesh, push, clock, read


print("WORK as laid (engine):")
census(lay0, lay1, "engine")
print("WORK after S1 (like monomials combined):")
jc, jpc, meshc, pushc, clockc, readc = census(lay0c, lay1c, "S1")
print("CARRIES per Node-clock per round: the board's 6 R =", 6 * rows, "; the teeth by cause", count)


# ---- the pruned layouts (on the combined plans)
def cut(plan, keep):
    legs, factor, target = plan
    return Plan(legs[:, keep], factor[keep], target[keep])


def cut_read(rd_, keep):
    first, factor, target = rd_
    return Read(first[keep], factor[keep], target[keep])


def pruned(drop):
    keep_j = np.flatnonzero(~np.isin(jc, drop))
    cl = lay0c.click._replace(weight=lay0c.click.weight[keep_j], train=lay0c.click.train[keep_j])
    return lay0c._replace(
        plan=cut(lay0c.plan, keep_j), click=cl,
        mesh=cut(lay0c.mesh, np.flatnonzero(~np.isin(meshc, drop))),
        push=cut(lay0c.push, np.flatnonzero(~np.isin(pushc, drop))),
        clock=cut(lay0c.clock, np.flatnonzero(~np.isin(clockc, drop))),
        stretch=cut_read(lay0c.stretch, np.flatnonzero(~np.isin(readc, drop))))


opp = [lay0.spokes.tolist().index([-x for x in e]) for e in lay0.spokes.tolist()]
plus = [sp for sp, e in enumerate(lay0.spokes.tolist()) if sum(e) == 1]
nb = lay0.nb


def form(label, drop, d1):
    layp = pruned(drop)
    if d1:
        own = sorted({(min(t, v), max(t, v)) for t, v in own0})
        mesh = sorted(s_ for s_ in e0 if s_[0] in plus)
        held = [t * T + v for t, v in own] + [((1 + sp) * T + t) * T + v for sp, t, v in mesh]
        partners = [((t * T + v), (v * T + t), None) for t, v in own] + [
            (((1 + sp) * T + t) * T + v, ((1 + opp[sp]) * T + v) * T + t, sp) for sp, t, v in mesh]
    else:
        held = [i for i, c in cls.items() if c not in drop]
        partners = []
    print(f"FORM {label}: J terms {len(layp.plan.factor)}, Mesh plan {len(layp.mesh.factor)}, push {len(layp.push.factor)},"
          f" clock {len(layp.clock.factor)}, grips' read {len(layp.stretch.factor)}; teeth held per Node-clock {len(held)};"
          f" state per Node-clock {3 * rows + len(two) + len(held)}")
    return {"label": label, "lay": layp, "held": np.asarray(sorted(held), dtype=np.intp), "partners": partners}


forms = [form("AB", ("a", "b"), False), form("ABC", ("a", "b", "c"), False), form("ABC+D1", ("a", "b", "c"), True)]


def expand(f, kh, fill, neg):
    k = np.full(((1 + n) * T * T, sites), fill, dtype=object)
    k[f["held"]] = kh
    pos = {int(h): j for j, h in enumerate(f["held"])}
    for h, p, sp in f["partners"]:
        val = neg(kh[pos[h]])
        if sp is None:
            k[p] = val
        else:
            far = np.full(sites, fill, dtype=object)
            far[nb[sp]] = val
            k[p] = far
    return k


def reduce(f, s):
    return (s.a, s.b, s.r, s.rd[two], s.k[f["held"]])


def full(f, sr):
    rd = np.zeros((rows, sites), dtype=object)
    rd[two] = sr[3]
    return State(sr[0], sr[1], sr[2], rd, expand(f, sr[4], birth, lambda x: K - 1 - x))


def act_form(f, sr):
    layp = f["lay"]
    nb_, _, _, _, gearing, plan, clock, _, click, _, _ = layp
    a, b, tooth, rdh, kh = sr
    rd = np.zeros((rows, sites), dtype=object)
    rd[two] = rdh
    board = State(a, b, tooth, rd, None)
    force, j1 = step.sources(layp, a)
    teeth = gearing.drive
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(layp, board, step.driven(gearing, force, step.kick(gearing, first)))
    q, kept = step.drive(j, teeth, rd)
    kicks = step.kick(gearing, q)
    sn, push = step.halves(layp), step.driven(gearing, force, kicks)
    wa, wb = step.dials(layp, board)
    first, _, _ = step.gear(a, b, tooth, wa + wb, wa + wb, push, sn)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb, wa + step.weight(gearing, clock, first), push, sn)
    passed = np.concatenate((step.passing(click, plan, b, a, a1), step.crossing(click, nb_, b, a, a1)))
    qh, kh1 = carry(passed[f["held"]], K, kh)
    return (a1, b1, s1, kept[two], kh1), qh


def mirror_form(f, sr):
    a, b, tooth, rdh, kh = sr
    _, _, _, teeth, even = f["lay"].gearing
    tau = senses * even - 1
    return (tau * b, tau * a, tooth - even * (senses * tooth + 1), rdh + even[two] * (flip(rdh, teeth[two]) - rdh), kh)


def text(x):
    return json.dumps([np.asarray(y).tolist() for y in x])


s = s0
red = [reduce(f, s0) for f in forms]
starts = [text(r_) for r_ in red]
for f, r_ in zip(forms, red):
    assert text(full(f, r_)) == text(s0), f["label"]
off = [dict(a=0, b=0, r=0, rd=0, k=0, clicks=0, lines=0) for _ in forms]
nclicks = nlines = 0
for at in range(1, rounds + 1):
    before = s
    s, c = step.act(lay0, s)
    lo = json.dumps(R.clicked(at, before, s, c, p0, nb))
    nclicks += int((c != 0).sum())
    nlines += len(R.clicked(at, before, s, c, p0, nb))
    for i, f in enumerate(forms):
        prev = full(f, red[i])
        red[i], qh = act_form(f, red[i])
        now = full(f, red[i])
        cf = expand(f, qh, 0, lambda x: -x)
        for nm, x, y in zip(("a", "b", "r", "rd", "k"), s, now):
            off[i][nm] += int((x != y).sum())
        off[i]["clicks"] += int((c != cf).sum())
        off[i]["lines"] += int(lo != json.dumps(R.clicked(at, prev, now, cf, p0, nb)))
print("RUN engine: click entries not 0", nclicks, "; record click lines", nlines)
for i, f in enumerate(forms):
    end = full(f, red[i])
    teeth_eq = json.dumps(R.teeth_of(s, p0, sorted(e0), nb)) == json.dumps(R.teeth_of(end, p0, sorted(e0), nb))
    dig = R.digest(R.stated(s)) == R.digest(R.stated(end))
    back = red[i]
    for _ in range(rounds):
        moved, _ = act_form(f, mirror_form(f, back))
        back = mirror_form(f, moved)
    print(f"FORM {f['label']}: entries off over {rounds} rounds {off[i]}; end teeth equal {teeth_eq}; end digest on the"
          f" state read back equal {dig}; run back from its reduced end alone exact {text(back) == starts[i]}")
print("END")
