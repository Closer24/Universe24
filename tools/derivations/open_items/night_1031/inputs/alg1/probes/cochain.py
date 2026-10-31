"""ALG1 probe: the act on the clocks' coupling complex (cochains), against node-all's own act.

Args: <tree> <world dir> <rounds> <mode> [unit-strengths world dir]
  mode "compare": the cochain act beside step.act, round by round: board, every tooth read back, every click, the
    record's click lines (run.clicked, JSON text), the end line's teeth and digest read back; then the cochain run back
    from the cochain end alone; then the counts of state and of terms multiplied per Node-clock per round.
  mode "books": the cochain act alone; each clock's own work against its booked total, without and with the cone
    (one cone edge per coupled clock, booking the clock's share of the work no clock-pair carries); the residual
    against the couplings' two-slot potential.

The complex is read once from the structure: the coupling tensor's support at unit strengths (the world's files with
every CHOSEN strength set to 1, loaded by node-all's own loader; no strength of the world read for the support). The
factors, the weights and the key are the world's own. Whole numbers only; Rule3's carry the one division; paths by
joinpath."""
import json
import sys
from pathlib import Path

tree, world, rounds, mode = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
unit_world = Path(sys.argv[5]) if len(sys.argv) > 5 else None
sys.path.insert(0, str(tree.joinpath("src")))
import numpy as np  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import contract as C  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Plan, State  # noqa: E402
from tensor24.runner import files  # noqa: E402
from tensor24.runner import load as L  # noqa: E402
from tensor24.runner import run as R  # noqa: E402


def loaded(wdir):
    paths = [wdir.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
    found = files.departures(*paths)
    assert not found, found
    universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
    shape = piece["shape"]
    kinds, tables, square, lifted = main.ENGINE.made(files.star(len(shape)))
    found = files.held_departures(universe, setting, files.vocabulary(kinds, square, lifted))
    assert not found, found
    ld, found = L.load(universe, setting, files.sites_of(shape), kinds, tables, square, lifted)
    assert not found, found
    return universe, ld, main.ENGINE.layout(universe, shape, ld)


universe, ld, lay = loaded(world)
uu, ldu, layu = loaded(unit_world) if unit_world else (universe, ld, lay)
s0 = State(*ld.state)
T = len(ld.trains)
rows, sites = s0.a.shape
n = lay.nb.shape[0]
nb = lay.nb
K = int(lay.click.key[0, 0])
B, left = carry(K - 1, 2, 0)
assert left == 0 and int(s0.k[0, 0]) == B, "the key odd, every tooth born at the middle"
opp = [1, 0, 3, 2, 5, 4]

# ---- the monomials: canonical (each multiset of legs once, its factors summed) and structural (support at unit
# strengths); the legs are the potential's four positions, -1 the unit
fac, legs = ld.potential
facu, legsu = ldu.potential
M = len(fac)
assert len(facu) == M and all((x == y).all() for x, y in zip(legs, legsu)), "the support lay has the same monomials"
legs4 = np.stack(legs)  # (4, M)
struct = [m for m in range(M) if facu[m] != 0]
assert all(facu[m] != 0 for m in range(M) if fac[m] != 0), "every live monomial is structural"
canon = {}
for m in struct:
    keyl = tuple(sorted(int(x) for x in legs4[:, m]))
    if keyl in canon:
        canon[keyl][1] += fac[m]
        canon[keyl][2] += 1
    else:
        canon[keyl] = [m, fac[m], 1]
reps = [v[0] for v in canon.values()]
cfac = np.array([v[1] for v in canon.values()], dtype=object)
merged = sum(v[2] - 1 for v in canon.values())
cleg = tuple(np.array([int(x) for x in legs4[p, reps]], dtype=np.intp) for p in range(4))
Mc = len(reps)
planC = C.pushes(cfac, cleg) if Mc else Plan(np.zeros((3, 0), dtype=np.intp), np.zeros(0, dtype=object),
                                              np.zeros(0, dtype=np.intp))
keepJ = np.flatnonzero(planC.target != -1)  # a push on the unit lands on no gear: no cell
planS = Plan(planC.legs[:, keepJ], planC.factor[keepJ], planC.target[keepJ])


def sparse(plan, planu):
    keep = np.flatnonzero(np.asarray(planu.factor != 0, dtype=bool) & np.asarray(plan.target != -1, dtype=bool))
    return Plan(plan.legs[:, keep], plan.factor[keep], plan.target[keep]), len(keep)


assert lay.mesh.factor.shape == layu.mesh.factor.shape and lay.push.factor.shape == layu.push.factor.shape
meshS, n_mesh = sparse(lay.mesh, layu.mesh)
pushS, n_push = sparse(lay.push, layu.push)
clockS, n_clock = sparse(lay.clock, layu.clock)
layS = lay._replace(plan=planS, mesh=meshS, push=pushS, clock=clockS)

# ---- the complex: clocks (trains at a place); own edges joined by a structural monomial with value legs in two
# trains or more; Mesh edges with a structural coupling, held at the + Spoke's end; triangles pairwise joined
from tensor24.runner.plans import rows_of  # noqa: E402

row_train = np.full(rows + 1, T, dtype=np.intp)
r_, of, _, _, _ = rows_of(ld.trains)
row_train[r_] = of
row_train_unit = row_train.copy()
mono_trains = [sorted({int(row_train[x]) for x in legs4[:, m] if x != -1}) for m in reps]
own_edges = sorted({(ts[i], ts[j]) for ts in mono_trains for i in range(len(ts)) for j in range(i + 1, len(ts))})
eidx = {e: i for i, e in enumerate(own_edges)}
cnt = np.zeros(T, dtype=np.intp)
across_u = layu.click.across
mesh_edges = []  # (spoke s even, t here, u across): the side held at the + end
for s_, r1, p1 in np.argwhere(np.asarray(across_u != 0, dtype=bool)):
    if s_ % 2 == 0:
        mesh_edges.append((int(s_), int(row_train[r1]), int(row_train[p1])))
mesh_edges = sorted(set(mesh_edges))
midx = {e: i for i, e in enumerate(mesh_edges)}
joined_pairs = set(own_edges)
tris = [(i, j, k) for i in range(T) for j in range(i + 1, T) for k in range(j + 1, T)
        if (i, j) in joined_pairs and (i, k) in joined_pairs and (j, k) in joined_pairs]

# ---- the passing on the own edges: per canonical term (position j of monomial m') its work, weighed onto the edge
W_eng = lay.click.weight  # (positions x M, trains), the engine's term order j M + m
Gt = []  # (edge, term index in planC, sign x weight)
for j in range(4):
    for mc, m in enumerate(reps):
        tau = j * M + m
        tc = j * Mc + mc
        t = int(row_train[legs4[j, m]]) if legs4[j, m] != -1 else T
        if t == T:
            continue
        for u in range(T):
            w = W_eng[tau, u]
            if w == 0 or u == t:
                continue
            e = (min(t, u), max(t, u))
            Gt.append((eidx[e], tc, w if t < u else -w))
edge_terms = sorted({tc for _, tc, _ in Gt})
tpos = {tc: i for i, tc in enumerate(edge_terms)}
Gm = np.zeros((len(own_edges), len(edge_terms)), dtype=object)
for e, tc, w in Gt:
    Gm[e, tpos[tc]] += w
eplan = Plan(planC.legs[:, edge_terms], planC.factor[edge_terms], planC.target[edge_terms])
# each edge term's clock (the train of the leg it pushes), for the books
term_clock = np.array([int(row_train[planC.target[tc]]) for tc in edge_terms], dtype=np.intp)
# Mesh couplings on the held sides: (spoke, r here, p across, c, edge)
mc_list = []
for s_, r1, p1 in np.argwhere(np.asarray(across_u != 0, dtype=bool)):
    if s_ % 2 == 0:
        mc_list.append((int(s_), int(r1), int(p1), lay.click.across[s_, r1, p1],
                        midx[(int(s_), int(row_train[r1]), int(row_train[p1]))]))


def pass_own(b, a, a1):
    va, vb, va1 = step.valued(a), step.valued(b), step.valued(a1)
    legs_, factor, target = eplan
    first = factor[None, :, None] + 0 * va[-1:, None]
    work = np.prod(np.concatenate((first, va[legs_])), axis=0) * (va1[target] - vb[target])
    return (Gm @ work if len(own_edges) else np.zeros((0, a.shape[-1]), dtype=object)), work


def pass_mesh(b, a, a1):
    out = np.zeros((len(mesh_edges), a.shape[-1]), dtype=object)
    moved = a1 - b
    for s_, r1, p1, c, e in mc_list:
        far, gone = a[p1][nb[s_]], moved[p1][nb[s_]]
        out[e] += c * (moved[r1] * far - a[r1] * gone)
    return out


two = np.flatnonzero(np.asarray(lay.gearing.drive.reshape(-1) != 1, dtype=bool))


def act_c(st):
    """One round on the complex: the board's lines as the engine's on the structural plans; the teeth a 1-cochain,
    balanced (born 0), turned by the balanced carry n + c = q K + c'."""
    a, b, tooth, rdh, ce, cm = st
    rd = np.zeros((rows, sites), dtype=object)
    rd[two] = rdh
    board = State(a, b, tooth, rd, None)
    gearing, clock = layS.gearing, layS.clock
    force, j1 = step.sources(layS, a)
    teeth = gearing.drive
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(layS, board, step.driven(gearing, force, step.kick(gearing, first)))
    q, kept = step.drive(j, teeth, rd)
    kicks = step.kick(gearing, q)
    senses, push = step.halves(layS), step.driven(gearing, force, kicks)
    wa, wb = step.dials(layS, board)
    first, _, _ = step.gear(a, b, tooth, wa + wb, wa + wb, push, senses)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb, wa + step.weight(gearing, clock, first), push, senses)
    po, work = pass_own(b, a, a1)
    pm = pass_mesh(b, a, a1)
    qo, ro = carry(po, K, ce + B)
    qm, rm = carry(pm, K, cm + B)
    return (a1, b1, s1, kept[two], ro - B, rm - B), (qo, qm, po, work)


def mirror_c(st):
    a, b, tooth, rdh, ce, cm = st
    _, _, _, teeth, even = layS.gearing
    tau = step.halves(layS) * even - 1
    e2, t2 = even[two], teeth[two]
    return (tau * b, tau * a, tooth - even * (step.halves(layS) * tooth + 1), rdh + e2 * (flip(rdh, t2) - rdh), ce, cm)


def untick_c(st):
    moved, _ = act_c(mirror_c(st))
    return mirror_c(moved)


def full_k(ce, cm, fill, neg):
    """Every side's tooth (or quotient) read back from the cochain: (t, u) t < u the cell, (u, t) its negation, the far
    end of a Mesh edge across its Mesh negated, every other side the birth (or 0)."""
    k = np.full(((1 + n) * T * T, sites), fill, dtype=object)
    kk = k.reshape(1 + n, T, T, sites)
    for i, (t, u) in enumerate(own_edges):
        kk[0, t, u] = ce[i]
        kk[0, u, t] = neg(ce[i])
    for i, (s_, t, u) in enumerate(mesh_edges):
        kk[1 + s_, t, u] = cm[i]
        far = np.full(sites, fill, dtype=object)
        far[nb[s_]] = neg(cm[i])
        kk[1 + opp[s_], u, t] = far
    return k


def reduce(st):
    a, b, r, rd, k = st
    kk = k.reshape(1 + n, T, T, sites)
    ce = np.array([kk[0, t, u] for t, u in own_edges], dtype=object).reshape(len(own_edges), sites) - B
    cm = np.array([kk[1 + s_, t, u] for s_, t, u in mesh_edges], dtype=object).reshape(len(mesh_edges), sites) - B
    return (a, b, r, rd[two], ce, cm)


def text(x):
    return json.dumps([np.asarray(y).tolist() for y in x])


def expand(st):
    a, b, r, rdh, ce, cm = st
    rd = np.zeros((rows, sites), dtype=object)
    rd[two] = rdh
    return State(a, b, r, rd, full_k(ce + B, cm + B, B, lambda x: K - 1 - x))


print("WORLD", world.name, "rounds", rounds, "edge key K", K, "birth B", B, "trains", T, "rows", rows, "sites", sites)
print("COMPLEX per place: own edges", own_edges, "; Mesh edges (+ end)", mesh_edges, "; triangles", tris)
print("MONOMIALS: laid", M, "; structural", len(struct), "; live", int(sum(1 for f in fac if f != 0)),
      "; canonical (each multiset once)", Mc, "(merged", merged, ")")
st = reduce(s0)
assert text(expand(st)) == text(s0), "the cochain lay reads back to the engine's lay"
n_state_eng = sum(int(x.shape[0]) for x in s0)
n_state_c = 3 * rows + len(two) + len(own_edges) + len(mesh_edges)
print("STATE per Node-clock: node-all", n_state_eng, "; cochain", n_state_c, "(a, b, r", rows, "each; rd", len(two),
      "; own edge teeth", len(own_edges), "; Mesh edge teeth", len(mesh_edges), ")")
# terms multiplied per Node-clock per round (each a product of a factor and 3 legs, MIN1's count of 3 products a term)
eng_terms = {"J plan": int(lay.plan.factor.shape[0]), "Mesh plan": int(lay.mesh.factor.shape[0]),
             "push plan": int(lay.push.factor.shape[0]), "clock plan (x5 reads)": int(lay.clock.factor.shape[0]),
             "passing terms": int(lay.plan.factor.shape[0]), "crossing pairs": int(lay.click.across.size),
             "teeth carries": int(s0.k.shape[0])}
c_terms = {"J plan": int(planS.factor.shape[0]), "Mesh plan": n_mesh, "push plan": n_push,
           "clock plan (x5 reads)": n_clock, "passing terms": len(edge_terms), "crossing pairs": len(mc_list),
           "teeth carries": len(own_edges) + len(mesh_edges)}
live = {"J plan": int(np.sum(np.asarray(lay.plan.factor != 0, dtype=bool) & np.asarray(lay.plan.target != -1, dtype=bool))),
        "Mesh plan": int(np.sum(np.asarray(lay.mesh.factor != 0, dtype=bool))),
        "push plan": int(np.sum(np.asarray(lay.push.factor != 0, dtype=bool))),
        "clock plan (x5 reads)": int(np.sum(np.asarray(lay.clock.factor != 0, dtype=bool)))}
print("TERMS per Node-clock per round: node-all", eng_terms)
print("                                cochain (structural)", c_terms)
print("                                live at the world's strengths", live)


def prods(d):
    # MIN1's count: 3 products a contract term; the clock plan read 5 times; 4 + T per passing term; 3 per Mesh pair
    # (x 2 at node-all, both ends; x 1 on the complex, the + end); no products for carries
    return 3 * (d["J plan"] + d["Mesh plan"] + d["push plan"] + 5 * d["clock plan (x5 reads)"]) + d["passing terms"] * 4 \
        + 3 * d["crossing pairs"]


print("PRODUCTS per Node-clock per round (MIN1's count): node-all about", prods(eng_terms) + eng_terms["passing terms"] * T,
      "; cochain about", prods(c_terms) + len(Gt))

if mode == "compare":
    s = s0
    off = {"a": 0, "b": 0, "r": 0, "rd": 0, "k": 0, "clicks": 0, "lines": 0}
    nlines, nclicks = 0, 0
    for at in range(1, rounds + 1):
        before, before_c = s, st
        s, c = step.act(lay, s)
        st, (qo, qm, _, _) = act_c(st)
        full = expand(st)
        prev = expand(before_c)
        cfull = full_k(qo, qm, 0, lambda x: -x)
        for nm, x, y in zip(("a", "b", "r", "rd", "k"), s, full):
            off[nm] += int(np.sum(np.asarray(x != y, dtype=bool)))
        off["clicks"] += int(np.sum(np.asarray(c != cfull, dtype=bool)))
        nclicks += int(np.sum(np.asarray(c != 0, dtype=bool)))
        partners, edges = R.joined(lay.click, T), R.crossed(lay.click, T)
        lo = R.clicked(at, before, s, c, partners, nb)
        lr = R.clicked(at, prev, full, cfull, partners, nb)
        nlines += len(lo)
        off["lines"] += int(json.dumps(lo) != json.dumps(lr))
    print("ROUND BY ROUND entries off (engine vs cochain read back):", off, "; click entries not 0:", nclicks,
          "; record click lines:", nlines)
    partners, edges = R.joined(lay.click, T), R.crossed(lay.click, T)
    endc = expand(st)
    print("END teeth line equal:", json.dumps(R.teeth_of(s, partners, edges, nb)) == json.dumps(R.teeth_of(endc, partners, edges, nb)),
          "; end digest (state read back) equal:", R.digest(R.stated(s)) == R.digest(R.stated(endc)))
    moved_teeth = int(np.sum(np.asarray(st[4] != 0, dtype=bool))) + int(np.sum(np.asarray(st[5] != 0, dtype=bool)))
    print("cochain teeth off the birth at the end (cells x places):", moved_teeth)
    back = st
    for _ in range(rounds):
        back = untick_c(back)
    print("RUN BACK on the complex from its end alone,", rounds, "rounds: start reached exactly:", text(back) == text(reduce(s0)))
    print("END")

if mode == "books":
    # each clock's own work on its edged terms (kappa times the works of the edge terms on its legs, the engine's
    # work form), its swept passing (the boundary of the edges' passing at the clock), its booked quanta; the cone:
    # one edge per coupled clock, carrying own - swept (the clock's share of the work no clock-pair carries), its tooth
    # balanced at K, born 0
    key_file = int(universe["chosen"]["key"])
    kappa, lft = carry(2 * K, key_file, 0)
    assert lft == 0
    coupled = sorted({t for e in own_edges for t in e})
    sgn = np.zeros((T, len(own_edges)), dtype=object)
    for i, (t, u) in enumerate(own_edges):
        sgn[t, i], sgn[u, i] = 1, -1
    own = np.zeros((T, sites), dtype=object)
    swept = np.zeros((T, sites), dtype=object)
    booked = np.zeros((T, sites), dtype=object)
    cone_c = np.zeros((T, sites), dtype=object)
    cone_q = np.zeros((T, sites), dtype=object)
    # the couplings' two-slot potential, per block (four value legs: the tie; two: the two-leg monomials)
    erep = sorted({tc % Mc for tc in edge_terms})
    nval = {mc: sum(1 for p in range(4) if cleg[p][mc] != -1) for mc in erep}

    def potential(a, which):
        va = step.valued(a)
        tot = np.zeros(sites, dtype=object)
        for mc in erep:
            if nval[mc] in which:
                v = cfac[mc] + 0 * va[-1]
                for p in range(4):
                    v = v * va[cleg[p][mc]]
                tot = tot + v
        return tot

    def place_work(work, which):
        tot = np.zeros(sites, dtype=object)
        for i, tc in enumerate(edge_terms):
            if nval[tc % Mc] in which:
                tot = tot + work[i]
        return tot

    a0, b0 = st[0], st[1]
    V4_0 = potential(a0, (3, 4)) + potential(b0, (3, 4))
    V2_0 = potential(a0, (2,)) + potential(b0, (2,))
    sumR4 = np.zeros(sites, dtype=object)
    sumR2 = np.zeros(sites, dtype=object)
    peak = {"own - swept at a clock": [0], "with the cone: K (booked + cone) - own at a clock": [0],
            "K booked - swept at a clock (David's identity, the teeth's part)": [0],
            "place: kappa sum R, four-leg": [0], "place: kappa sum R, two-leg": [0],
            "place: kappa (sum R + dV~), four-leg": [0], "place: kappa (sum R + dE), two-leg": [0],
            "place: kappa (sum R + dE4), four-leg, E4 the full polarization": [0]}

    def note(name, arr, at, lab):
        flat = [(abs(int(v)), int(v), idx) for idx, v in np.ndenumerate(arr)]
        m_ = max(flat)
        if m_[0] > abs(peak[name][0]):
            peak[name] = [m_[1], lab, m_[2], at]

    E2 = None
    for at in range(1, rounds + 1):
        before = st
        st, (qo, qm, po, work) = act_c(st)
        own_now = np.zeros((T, sites), dtype=object)
        np.add.at(own_now, term_clock, kappa * work)
        sw_now = sgn @ po if len(own_edges) else np.zeros((T, sites), dtype=object)
        bk_now = sgn @ qo if len(own_edges) else np.zeros((T, sites), dtype=object)
        own, swept, booked = own + own_now, swept + sw_now, booked + bk_now
        rho = own_now - sw_now  # the clock's share of the work no clock-pair carries, this round
        qc, rc = carry(rho, K, cone_c + B)
        cone_c, cone_q = rc - B, cone_q + qc
        note("own - swept at a clock", own - swept, at, "train, site")
        note("with the cone: K (booked + cone) - own at a clock", K * (booked + cone_q) - own, at, "train, site")
        note("K booked - swept at a clock (David's identity, the teeth's part)", K * booked - swept, at, "train, site")
        sumR4 = sumR4 + place_work(work, (3, 4))
        sumR2 = sumR2 + place_work(work, (2,))
        a1, b1 = st[0], st[1]
        V4 = potential(a1, (3, 4)) + potential(b1, (3, 4))
        note("place: kappa sum R, four-leg", kappa * sumR4, at, "site")
        note("place: kappa sum R, two-leg", kappa * sumR2, at, "site")
        note("place: kappa (sum R + dV~), four-leg", kappa * (sumR4 + V4 - V4_0), at, "site")
        # the two-leg exact polarized energy E = f (x_a y_b + x_b y_a): sum R + dE must be 0 exactly
        va, vb = step.valued(a1), step.valued(b1)
        E2n = np.zeros(sites, dtype=object)
        for mc in erep:
            if nval[mc] == 2:
                vl = [cleg[p][mc] for p in range(4) if cleg[p][mc] != -1]
                E2n = E2n + cfac[mc] * (va[vl[0]] * vb[vl[1]] + vb[vl[0]] * va[vl[1]])
        if E2 is None:
            va0, vb0 = step.valued(a0), step.valued(b0)
            E2 = np.zeros(sites, dtype=object)
            for mc in erep:
                if nval[mc] == 2:
                    vl = [cleg[p][mc] for p in range(4) if cleg[p][mc] != -1]
                    E2 = E2 + cfac[mc] * (va0[vl[0]] * vb0[vl[1]] + vb0[vl[0]] * va0[vl[1]])
        note("place: kappa (sum R + dE), two-leg", kappa * (sumR2 + E2n - E2), at, "site")
        # the four-leg's full polarization over the two slots, two positions at each: kappa E4 = (kappa / 3) f P with
        # P = SUM over the 6 pairs S of positions of PROD_S a PROD_(not S) b (E4(a, a) = 2 V(a), as E(a, a) = 2 V(a))
        P4n = np.zeros(sites, dtype=object)
        for mc in erep:
            if nval[mc] == 4:
                ps = [cleg[p][mc] for p in range(4)]
                for S_ in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
                    v = cfac[mc] + 0 * va[-1]
                    for i_ in range(4):
                        v = v * (va[ps[i_]] if i_ in S_ else vb[ps[i_]])
                    P4n = P4n + v
        if at == 1:
            va0, vb0 = step.valued(a0), step.valued(b0)
            P40 = np.zeros(sites, dtype=object)
            for mc in erep:
                if nval[mc] == 4:
                    ps = [cleg[p][mc] for p in range(4)]
                    for S_ in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
                        v = cfac[mc] + 0 * va0[-1]
                        for i_ in range(4):
                            v = v * (va0[ps[i_]] if i_ in S_ else vb0[ps[i_]])
                        P40 = P40 + v
        k3, kl = carry(kappa, 3, 0)
        assert kl == 0
        note("place: kappa (sum R + dE4), four-leg, E4 the full polarization", kappa * sumR4 + k3 * (P4n - P40), at, "site")
    print("BOOKS over", rounds, "rounds; kappa", kappa, "; coupled clocks", coupled, "; the cone's teeth per place",
          len(coupled), "; the deg of each clock", [int(np.sum(np.asarray(sgn[t] != 0, dtype=bool))) for t in range(T)])
    for name, v in peak.items():
        q_, r__ = carry(abs(v[0]), K, 0) if v[0] else (0, 0)
        print(" ", name, ":", v, "; in edge keys", int(q_), "and a tooth", int(r__))
    print("END by train, summed over the sites: own - swept in keys",
          [int(carry(int((own - swept)[t].sum()), K, 0)[0]) for t in range(T)],
          "; cone quanta", [int(cone_q[t].sum()) for t in range(T)], "; booked quanta", [int(booked[t].sum()) for t in range(T)])
    print("END the place's cone line (sum of its cone quanta) at each site:", [int(x) for x in cone_q.sum(axis=0)])
    print("END at site 0, round", rounds, ": sum R four-leg (no kappa)", int(sumR4[0]), "; its V~ change V(a)+V(b) (no kappa)",
          int((V4 - V4_0)[0]), "; V(a) alone change", int((potential(a1, (3, 4)) - potential(a0, (3, 4)))[0]),
          "; sum R two-leg", int(sumR2[0]), "; the two-leg E change", int((E2n - E2)[0]))
    print("END")

if mode == "turn":
    # the 24 on the cochain teeth, on a line board (sides sx x 1 x 1): the turns diag(-1,-1,1) and diag(-1,1,-1), each
    # reversing the Mesh's axis; on the engine every side moves to the turned side (g s, t, u) at g x; on the complex
    # the turn is the cellular map with its orientation sign: an own edge's tooth moves with its site, and a Mesh edge
    # whose + end the turn sends to its - end is read from its other end, negated (MIN1's flip)
    from tensor24.runner.files import star as star_of
    made = main.ENGINE.made(star_of(3))
    kinds_ = made[0]
    spokes = lay.spokes
    matrix, wt = __import__("tensor24.engine.kinds", fromlist=["turns"]).turns(star_of(3))
    shape = json.loads(world.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    assert shape[1] == 1 and shape[2] == 1 and all(int(nb[0][x]) == (x + 1) % shape[0] for x in range(sites))
    tr = ld.trains
    names = [t["name"] for t in universe["trains"]]
    order = ["A1", "A2", "E", "T1", "T2"]
    for gm in ([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], [[-1, 0, 0], [0, 1, 0], [0, 0, -1]]):
        g = np.array(gm, dtype=object)
        idx = [i for i in range(len(matrix)) if wt[i] == 1 and (matrix[i] == g).all()]
        assert len(idx) == 1
        gi = idx[0]
        rho = np.zeros((rows, rows), dtype=object)
        for ti, tdef in enumerate(universe["trains"]):
            blocks = [np.asarray(getattr(kinds_, kd.lower())[gi], dtype=object) for kd in tdef["kinds"]]
            dim = sum(bk.shape[0] for bk in blocks)
            bd = np.zeros((dim, dim), dtype=object)
            o_ = 0
            for bk in blocks:
                bd[o_:o_ + bk.shape[0], o_:o_ + bk.shape[0]] = bk
                o_ += bk.shape[0]
            part = int(tdef["part"])
            first = int(tr.first[ti])
            rho[first:first + dim * part, first:first + dim * part] = np.kron(bd, np.eye(part, dtype=object))
        neg = np.array([int(rho[i, i]) == -1 for i in range(rows)])
        assert all(int(abs(rho[i]).sum()) == 1 for i in range(rows)), "a signed permutation of the rows"
        gx = np.array([(-x) % shape[0] for x in range(sites)], dtype=np.intp)
        # Spokes: g s, found by the star's directions
        gs = [int(np.flatnonzero([(spokes[j] == g @ spokes[s_]).all() for j in range(n)])[0]) for s_ in range(n)]
        perm_rows = [int(np.flatnonzero(rho[i] != 0)[0]) for i in range(rows)]  # a'[i] = rho[i, p] a[p]
        sg = np.array([int(rho[i, perm_rows[i]]) for i in range(rows)], dtype=object)

        def g_full(s):
            a, b, r, rd, k = s
            a2, b2, r2, rd2 = (np.zeros_like(x) for x in (a, b, r, rd))
            for i in range(rows):
                p_ = perm_rows[i]
                a2[i, gx] = sg[i] * a[p_]
                b2[i, gx] = sg[i] * b[p_]
                r2[i, gx] = r[p_] if sg[i] == 1 else -1 - r[p_]
                rd2[i, gx] = rd[p_]
            kk = k.reshape(1 + n, T, T, sites)
            k2 = np.zeros_like(kk)
            for reach in range(1 + n):
                r2_ = 0 if reach == 0 else 1 + gs[reach - 1]
                k2[r2_][:, :, gx] = kk[reach]
            return State(a2, b2, r2, rd2, k2.reshape(k.shape))

        def g_c(st_):
            a, b, r, rdh, ce, cm = st_
            a2, b2, r2 = (np.zeros_like(x) for x in (a, b, r))
            for i in range(rows):
                p_ = perm_rows[i]
                a2[i, gx] = sg[i] * a[p_]
                b2[i, gx] = sg[i] * b[p_]
                r2[i, gx] = r[p_] if sg[i] == 1 else -1 - r[p_]
            ce2 = np.zeros_like(ce)
            ce2[:, gx] = ce
            cm2 = np.zeros_like(cm)
            for i, (s_, t, u) in enumerate(mesh_edges):
                if gs[s_] % 2 == 0:  # the + end stays the + end: the tooth moves with its site
                    cm2[midx[(gs[s_], t, u)]][gx] = cm[i]
                else:  # the + end goes to the - end: the cell is held at the far site, read from its other end
                    j = midx[(opp[gs[s_]], u, t)]
                    cm2[j][nb[gs[s_]][gx]] = -cm[i]
            return (a2, b2, r2, rdh * 0 + rdh if len(two) == 0 else None, ce2, cm2)

        assert len(two) == 0, "this test reads a world whose drive's teeth are all 1"
        s = s0
        eng_off, c_off, map_off, moved = 0, 0, 0, 0
        stc = reduce(s0)
        for at in range(1, rounds + 1):
            # the engine: act(g s) against g act(s)
            s_next, _ = step.act(lay, s)
            gs_next, _ = step.act(lay, g_full(s))
            eng_off += int(text(gs_next) != text(g_full(s_next)))
            # the complex: the cellular map against the engine's turn read back, and act_c(g_c st) against g_c act_c(st)
            map_off += int(text(g_c(stc)) != text(reduce(g_full(expand(stc)))))
            c1, _ = act_c(stc)
            c2, _ = act_c(g_c(stc))
            c_off += int(text(c2) != text(g_c(c1)))
            moved += int(np.sum(np.asarray(c1[5] != 0, dtype=bool)))
            s, stc = s_next, c1
        print("TURN", gm, ": rounds", rounds, "; engine act(g s) != g act(s) in", eng_off, "rounds; the cellular map with "
              "its sign != the engine's turn read back in", map_off, "rounds; act_c(g c) != g act_c(c) in", c_off,
              "rounds; Mesh cells x places off the birth, summed over the rounds", moved)
    print("END")

if mode == "coneback":
    # the cone's teeth with the run back: the state is the cochain state and one balanced tooth per coupled clock (the
    # cone edge to the place), turned by the clock's own work less its swept passing; the mirror keeps every tooth;
    # the run back from the end alone, nothing saved
    key_file = int(universe["chosen"]["key"])
    kappa, lft = carry(2 * K, key_file, 0)
    sgn = np.zeros((T, len(own_edges)), dtype=object)
    for i, (t, u) in enumerate(own_edges):
        sgn[t, i], sgn[u, i] = 1, -1

    def cone_round(stc, cone):
        st2, (qo, qm, po, work) = act_c(stc)
        own_now = np.zeros((T, sites), dtype=object)
        np.add.at(own_now, term_clock, kappa * work)
        rho = own_now - sgn @ po
        qc, rc = carry(rho, K, cone + B)
        return st2, rc - B, qc

    stc, cone = reduce(s0), np.zeros((T, sites), dtype=object)
    start = text(stc) + text([cone])
    qsum = np.zeros((T, sites), dtype=object)
    for _ in range(rounds):
        stc, cone, qc = cone_round(stc, cone)
        qsum = qsum + qc
    print("CONE forward", rounds, "rounds: cone quanta by train summed over the sites", [int(qsum[t].sum()) for t in range(T)],
          "; cone teeth off the birth", int(np.sum(np.asarray(cone != 0, dtype=bool))))
    back, bcone = stc, cone
    for _ in range(rounds):
        m = mirror_c(back)
        m2, bcone, _ = cone_round(m, bcone)
        back = mirror_c(m2)
    print("CONE RUN BACK from the end alone,", rounds, "rounds: board, edge teeth and cone teeth at the start exactly:",
          text(back) + text([bcone]) == start)
    print("END")
