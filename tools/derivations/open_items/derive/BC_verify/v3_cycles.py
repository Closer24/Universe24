"""BC verifier, part 3: (iii), the late settings carried back by the time reversal. A minimal two-cycle integer toy.

1D line. The fitting's Mesh: B end at site 0, A end at site 1. Detector A at site 1+d, detector B at site -d.
A twin is a hand moving one Mesh a tick with a twin pair (two Gaussian integers). In 1D at the causal speed the
one formula carries a pulse intact (field_check below), the case most favourable to the account.
Cycle 1: tick 0 the bang; tick tb the birth (Animate's act, four sizes N(det[fA^a, fB^b]) and one draw, against
what stands at the Mesh: ambient frames z, z, independent of the settings); tick tb+1 the late choices (x1, y1)
at the detectors; tick tb+d the far clicks (law 6; the click writes the taken part <f^x, psi> f^x).
Tick tT: the turnover T (every hand's direction reversed, every twin pair turned by perp, so S -> -S and T^2 = -1
on twin pairs; the detectors' frames too; the source scalar conjugated).
The reversed run, two readings:
  R1, the exact rewind: each act undone from its note in reverse order (S^-1 with notes); checked bit for bit
      against T(X_t) of the same branch at every tick; at 2 tT, T again; cycle 2 runs forward.
  R2, the Boss's account: after T the forward rule runs on: the twins retrace their paths, the detectors click them
      again (whole), they pass each other at the Mesh at 2tT - tb, T again at 2tT, and at 2tT + tb they stand at the
      Mesh's two ends again.  Cycle 2's birth: Animate's act against the twins standing there (the returned axes);
      the twins become the children.  Variants: R2-law6 (cycle 2's birth is law 6 on the twins' own product
      state); R2-merge (at 2tT - tb, law 6 between the twins' A1 part merging into the source, and passing).
Cycle 2: late choices (x2, y2) at 2tT + tb + 1, far clicks at 2tT + tb + d. Every draw counted (exact counts).
Run: python3 -I -B v3_cycles.py
"""
from fractions import Fraction as Fr
import importlib.util, os, copy, random

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("v1", os.path.join(here, "v1_algebra.py"))
v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
perp, det, ovl, gn, sc, rho = v1.perp, v1.det, v1.ovl, v1.gn, v1.sc, v1.rho
pick = v1.pick_counts
SET = v1.REAL
Z = ((1, 0), (0, 0))
K = (3, 2)
d, tb = 6, 2
tT = tb + d + 3
posA, posB = 1 + d, -d
T_BIRTH = {1: tb, 2: 2 * tT + tb}
T_CHOICE = {1: tb + 1, 2: 2 * tT + tb + 1}
T_CLICK = {1: tb + d, 2: 2 * tT + tb + d}

def neg2(u): return ((-u[0][0], -u[0][1]), (-u[1][0], -u[1][1]))
def proj(f, psi): return sc(ovl(f, psi), f)
def gconj(z): return None if z is None else (z[0], -z[1])

def snap(st):
    return copy.deepcopy({k: v for k, v in st.items() if k not in ("hist", "notes", "rec")})

def Tmap(st):
    st = copy.deepcopy(st)
    for tw in st["tw"]:
        tw["dir"] = -tw["dir"]; tw["psi"] = perp(tw["psi"])
    st["fr"] = {k: perp(v) for k, v in st["fr"].items()}
    st["src"] = gconj(st["src"])
    return st

def key(st):
    return (tuple(sorted((tw["id"], tw["pos"], tw["dir"], tw["psi"]) for tw in st["tw"])),
            tuple(sorted(st["fr"].items())), st["src"])

def at_ends(s, outward):
    dA, dB = (1, -1) if outward else (-1, 1)
    a = [tw for tw in s["tw"] if tw["pos"] == 1 and tw["dir"] == dA]
    b = [tw for tw in s["tw"] if tw["pos"] == 0 and tw["dir"] == dB]
    return (a[0], b[0]) if a and b else None

def birth(s, rule, t):
    """the birth act at the Mesh; returns [(prob, state)]."""
    out = []
    ends = at_ends(s, outward=True)
    if ends and rule.get("birth2") == "law6":
        fA, fB = ends[0]["psi"], ends[1]["psi"]
        sA, sB = {1: fA, -1: perp(fA)}, {1: fB, -1: perp(fB)}
        sizes = [((a, b), gn(ovl(sA[a], fA)) * gn(ovl(sB[b], fB))) for a in (1, -1) for b in (1, -1)]
        cnt, R = pick(sizes)
        for (a, b), n in cnt.items():
            if n:
                s2 = copy.deepcopy(s); e2 = at_ends(s2, True)
                e2[0]["psi"], e2[1]["psi"] = sA[a], sB[b]
                out.append((Fr(n, R), s2))
        return out
    if ends:
        fA, fB, ids, amp = ends[0]["psi"], ends[1]["psi"], {ends[0]["id"], ends[1]["id"]}, K
    else:
        fA, fB, ids, amp = s["amb"][0], s["amb"][1], set(), (s["src"] if s["src"] is not None else K)
    sA, sB = {1: fA, -1: perp(fA)}, {1: fB, -1: perp(fB)}
    sizes = [((a, b), gn(det(sA[a], sB[b]))) for a in (1, -1) for b in (1, -1)]
    cnt, R = pick(sizes)
    for (a, b), n in cnt.items():
        if n == 0:
            continue
        s2 = copy.deepcopy(s)
        s2["tw"] = [tw for tw in s2["tw"] if tw["id"] not in ids]
        s2["tw"].append(dict(id="A", pos=1, dir=1, psi=sc(amp, sA[a])))
        s2["tw"].append(dict(id="B", pos=0, dir=-1, psi=sc(amp, sB[b])))
        s2["notes"].append(("birth", t, s["src"]))
        s2["src"] = None
        out.append((Fr(n, R), s2))
    return out

def forward_tick(st, rule, cycle, choices):
    st = copy.deepcopy(st)
    st["t"] += 1
    t = st["t"]
    for tw in st["tw"]:                                   # 1. every hand one Mesh
        tw["pos"] += tw["dir"]
    br = [(Fr(1), st)]
    for side, pos in (("A", posA), ("B", posB)):          # 2. a hand at a detector is clicked (law 6)
        nb = []
        for p, s in br:
            hit = [tw for tw in s["tw"] if tw["pos"] == pos]
            if not hit:
                nb.append((p, s)); continue
            f, psi, tid = s["fr"][side], hit[0]["psi"], hit[0]["id"]
            cnt, R = pick([(1, gn(ovl(f, psi))), (-1, gn(ovl(perp(f), psi)))])
            for x, n in cnt.items():
                if n == 0:
                    continue
                s2 = copy.deepcopy(s)
                tw2 = [tw for tw in s2["tw"] if tw["id"] == tid][0]
                s2["notes"].append(("click", t, tid, psi))
                tw2["psi"] = proj(f if x == 1 else perp(f), psi)
                s2["rec"].append((cycle, t, side, x))
                nb.append((p * Fr(n, R), s2))
        br = nb
    out = []                                              # 3. the birth tick
    for p, s in br:
        if t == T_BIRTH[cycle]:
            out += [(p * q, s2) for q, s2 in birth(s, rule, t)]
        else:
            out.append((p, s))
    if rule.get("merge") and t == 2 * tT - tb:            # 3'. the merger at the reversed birth (R2-merge)
        res = []
        for p, s in out:
            ends = at_ends(s, outward=False)
            if not ends:
                res.append((p, s)); continue
            u, w = ends[0]["psi"], ends[1]["psi"]
            m = gn(det(u, w))
            cnt, R = pick([("merge", m), ("pass", 2 * rho(u) * rho(w) - m)])
            for kk, n in cnt.items():
                if n == 0:
                    continue
                s2 = copy.deepcopy(s)
                if kk == "merge":
                    s2["tw"] = [tw for tw in s2["tw"] if tw["id"] not in (ends[0]["id"], ends[1]["id"])]
                    s2["src"] = det(u, w)                 # one Gaussian number: no axis survives (P9)
                res.append((p * Fr(n, R), s2))
        out = res
    for p, s in out:                                      # 4. the late choices
        if t == T_CHOICE[cycle]:
            s["fr"] = {"A": SET[choices[cycle][0]], "B": SET[choices[cycle][1]]}
        s["hist"].append(snap(s))
    return out

def rewind_tick(st, t):
    """undo forward tick t from the notes (R1): st holds T(X_t); returns T(X_{t-1})."""
    st = copy.deepcopy(st)
    if t == T_CHOICE[1]:
        st["fr"] = {"A": perp(Z), "B": perp(Z)}
    for nt in [n for n in st["notes"] if n[0] == "birth" and n[1] == t]:
        st["tw"] = [tw for tw in st["tw"] if tw["id"] not in ("A", "B")]
        st["src"] = gconj(nt[2])
        st["notes"].remove(nt)
    for nt in [n for n in st["notes"] if n[0] == "click" and n[1] == t]:
        for tw in st["tw"]:
            if tw["id"] == nt[2]:
                tw["psi"] = perp(nt[3])
        st["notes"].remove(nt)
    for tw in st["tw"]:
        tw["pos"] += tw["dir"]
    return st

def start():
    st = dict(t=0, tw=[], fr={"A": Z, "B": Z}, src=K, amb=(Z, Z), notes=[], rec=[], hist=[])
    st["hist"].append(snap(st))
    return st

def run(choices, rule):
    """choices = {1: (x1, y1), 2: (x2, y2)}. Returns E1, E2, A2+, B2+, (checked, failed) for R1's rewind."""
    br = [(Fr(1), start())]
    for t in range(1, tT + 1):
        br = [(p * q, s2) for p, s in br for q, s2 in forward_tick(s, rule, 1, choices)]
    chk = [0, 0]
    if rule["rev"] == "R1":
        res = []
        for p, s in br:
            st = Tmap(s)
            for t in range(tT, 0, -1):
                st = rewind_tick(st, t)
                chk[0] += 1; chk[1] += (key(st) != key(Tmap(s["hist"][t - 1])))
            st = Tmap(st); st["t"] = 2 * tT; st["notes"] = []; st["hist"] = [snap(st)]
            res.append((p, st))
        br = res
    else:
        br = [(p, Tmap(s)) for p, s in br]
        for t in range(tT + 1, 2 * tT + 1):
            br = [(p * q, s2) for p, s in br for q, s2 in forward_tick(s, rule, 1, choices)]
        br = [(p, Tmap(s)) for p, s in br]
    for t in range(2 * tT + 1, T_CLICK[2] + 1):
        br = [(p * q, s2) for p, s in br for q, s2 in forward_tick(s, rule, 2, choices)]
    E1 = E2 = a2 = b2 = Fr(0)
    for p, s in br:
        r1 = {side: x for (c, t, side, x) in s["rec"] if c == 1 and t == T_CLICK[1]}
        r2 = {side: x for (c, t, side, x) in s["rec"] if c == 2 and t == T_CLICK[2]}
        E1 += p * r1["A"] * r1["B"]; E2 += p * r2["A"] * r2["B"]
        a2 += p * (r2["A"] == 1); b2 += p * (r2["B"] == 1)
    assert sum(p for p, _ in br) == 1
    return E1, E2, a2, b2, chk

def same(x2, y2): return [((x2, y2), Fr(1))]
def indep(x2, y2): return [((x1, y1), Fr(1, 4)) for x1 in ("a", "a'") for y1 in ("b", "b'")]
def persist(p):
    o = v1.OTHER
    return lambda x2, y2: [((xx, yy), px * py) for xx, px in ((x2, p), (o[x2], 1 - p)) for yy, py in ((y2, p), (o[y2], 1 - p))]

def chsh_over(rule, scenario):
    S1 = S2 = Fr(0); sig = set(); chk = [0, 0]
    for (x2, y2), c in zip(v1.PAIRS, (1, 1, 1, -1)):
        e1 = e2 = Fr(0)
        for (x1, y1), w in scenario(x2, y2):
            E1, E2, a2, b2, ck = run({1: (x1, y1), 2: (x2, y2)}, rule)
            e1 += w * E1; e2 += w * E2
            sig.add((str(a2), str(b2))); chk[0] += ck[0]; chk[1] += ck[1]
        S1 += c * e1; S2 += c * e2
    return S1, S2, sig, chk

def field_check():
    """the 1D one formula at the causal speed, new = left + right - before, T = (swap now and before, perp):
    T S^7 T S^7 = -1 on random fields, and a laid right-mover stays one."""
    rnd = random.Random(11); bad_rev = bad_pulse = 0; N = 200; L = 30
    zero = ((0, 0), (0, 0))
    def S(st):
        bef, now = st
        return (now, [tuple(v1.gs(v1.ga(now[x - 1][i] if x > 0 else (0, 0), now[x + 1][i] if x < L - 1 else (0, 0)),
                                  bef[x][i]) for i in range(2)) for x in range(L)])
    def T(st):
        bef, now = st
        return ([perp(u) for u in now], [perp(u) for u in bef])
    rv = lambda: tuple((rnd.randint(-5, 5), rnd.randint(-5, 5)) for _ in range(2))
    for _ in range(N):
        st = ([rv() for _ in range(L)], [rv() for _ in range(L)])
        a = st
        for _ in range(7): a = S(a)
        a = T(a)
        for _ in range(7): a = S(a)
        a = T(a)
        bad_rev += (a != ([neg2(u) for u in st[0]], [neg2(u) for u in st[1]]))
    for _ in range(N):
        psi = rv()
        bef = [zero] * L; now = [zero] * L
        now[5] = psi; bef[4] = psi
        st = (bef, now)
        for k in range(1, 15):
            st = S(st)
            bad_pulse += any((st[1][x] != (psi if x == 5 + k else zero)) for x in range(L))
    return N, bad_rev, bad_pulse

def main():
    N, br_, bp = field_check()
    print(f"== 1D one formula at the causal speed: T S^7 T S^7 = -1 failed in {br_} of {N} random fields; "
          f"a laid right-mover lost its shape in {bp} of {N * 14} ticks")
    rules = [("R1 exact rewind (notes)", {"rev": "R1"}),
             ("R2 the account (forward rule after T)", {"rev": "R2"}),
             ("R2-law6 (cycle-2 birth: law 6 on the twins)", {"rev": "R2", "birth2": "law6"}),
             ("R2-merge (A1 merger at the reversed birth)", {"rev": "R2", "merge": True})]
    for rname, rule in rules:
        for sname, sfun in (("choices repeat", same), ("choices independent", indep)):
            S1, S2, sig, chk = chsh_over(rule, sfun)
            extra = f"; rewind bit for bit {chk[0] - chk[1]} of {chk[0]} states" if rule["rev"] == "R1" else ""
            print(f"  {rname} | {sname}: S_1 = {S1} ({float(S1):+.4f}); S_2 = {S2} ({float(S2):+.4f}); "
                  f"cycle-2 marginals {sorted(sig)}{extra}")
    for p in (Fr(9, 10), Fr(85, 100), Fr(84, 100), Fr(3, 4)):
        S1, S2, sig, _ = chsh_over({"rev": "R2"}, persist(p))
        print(f"  R2 | choices persist with p = {p} per side: S_2 = {float(S2):+.4f}; marginals {sorted(sig)}")
    # what stands at the birth's Mesh at the reversed birth tick, for x1 = a', y1 = b (every branch)
    ch = {1: ("a'", "b"), 2: ("a'", "b")}
    for rname, rule in rules[:2]:
        br = [(Fr(1), start())]
        for t in range(1, tT + 1):
            br = [(p * q, s2) for p, s in br for q, s2 in forward_tick(s, rule, 1, ch)]
        rows = set()
        for p, s in br:
            if rule["rev"] == "R1":
                st = Tmap(s)
                for t in range(tT, tb, -1):
                    st = rewind_tick(st, t)
            else:
                st = Tmap(s)
                for t in range(tT + 1, 2 * tT - tb + 1):
                    st = forward_tick(st, rule, 1, ch)[0][1]
            got = tuple(sorted((tw["id"], v1.axis(tw["psi"])) for tw in st["tw"]))
            want = tuple(sorted((tw["id"], v1.axis(perp(tw["psi"]))) for tw in s["hist"][tb]["tw"]))
            rows.add((got == want, got))
        print(f"  {rname}: at the reversed birth tick, (equals T(X_birth), axes held): {sorted(rows)}")
    print(f"  late frames' axes: a' {v1.axis(SET[chr(97) + chr(39)])}, b {v1.axis(SET['b'])}; birth frames z (0, 0, 1)")

if __name__ == "__main__":
    main()
