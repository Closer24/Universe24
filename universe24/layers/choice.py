"""CHOICE-CLICK layer (Study 5 constructions, SYSTEM_DESIGN_v5 §1b, §7, §8 S5-O1…O4): TENSOR BLOCKS ONLY.

Every builder returns a ``core.tensor.Block`` with ``Q`` set (ONE divisor D = 6Q per composed experiment). Gears of
other designed divisors enter by the Q-scaling theorem (input and remainder x (6Q / D_design)). Nothing here holds a
state, runs the engine or observes; initial data live in ``prepare/choice.py``, read-outs in ``observe/choice.py``.

Carriers (remainder-free, C0):
* ``build_clock_ring``  period-6 ring (3 gears, u = 3Q b) or period-4 pair (2 gears, u = 0);
* ``build_fibre``       exact d'Alembert fibre, u = 3Q (b(x - e) + b(x + e)).
Choice gears:
* ``build_born_router``        rank-3 |psi|^2 detector pair (observer); "opposite" form = the PAIRED LINK CLOCK
                               (equal remainders, inputs +I+ and -I-), "mirror" form (tokens lam, D-1-lam);
* ``build_common_drive``       DC source feeding both detectors equally (the board-made token, Study 5 B6/T4);
* ``build_sequential_router``  ONE link gear visiting one carried remainder sequentially (S5-O2);
* ``build_parallel_router``    the parallel-read control (n exit gears, one update, one shared token);
* ``build_f7``                 the light-cone choice (Alice's choice click emits a front, Bob's Born reader);
* ``build_which_path_W``       Study-5 M2-2 nonlinear which-path gears (S5-P2R);
* ``build_gated_pair``         exit pair read once at the arrival of a gate flash (rank 4, observer);
* ``build_dec_toy``            S5-M2's D12b QM-deviation toy (P_dec) as gears;
* ``build_backaction_router``  (ii) BACK-ACTING reciprocal detectors from ONE potential (rank 3, or the rank-4
                               spring cross term alone: exploratory, NOT shippable as a force term, ruling 09:5x);
* ``build_spring_backaction_router``  (ii) the same with a COMPLETE OD4 spring (minus sign, self-quartics, X0 = 0).
Rank-4 terms: force (reciprocal) rank-4 terms may only be complete OD4 springs; the designated rank-4 terms of this
layer are the F7 photon-marker-gated front kick, the gated M2-2 exit pair and the D12b gated readout (TC.14 audit).
One-way terms carry ``{"designated_one_way": <why>}`` (core.reciprocity lists them).
"""
from __future__ import annotations

from ..core.tensor import Block, GearType

O = (0, 0, 0)
OBSERVER = "observer detector: records without back-action (Study 5 D3)"
DRIVE = ("common drive: the DC source sets the pair's shared remainder (token born from the vacuum, Study 5 B6/T4); "
         "it does not read the detectors")
SEQ = "sequential router link gear: reads the arriving intensity stream without back-action (observer, S5-O2)"
PAR = "parallel-read control exit gear: reads its intensity without back-action (observer, Study 5 B7 control)"
IMPRINT = ("choice-front imprint (F7): P2R's two-update kick q*(b_C - a_C), -q*a_C, gated by the photon marker on the "
           "neighbour link; one-way, the front does not push back on Alice's detectors or setting clock")
EMIT = ("choice-front emission (F7): Alice's front clock drives the front fibre one-way through an exact two-node "
        "source (b_F(x) - a_F(x+e)); the far side reads the front without back-action")
WPATH = ("which-path gear (Study 5 M2-2, S5-P2R): reads arm 1 at weight 3Q/Q_W and kicks it by one unit (3Q); the "
         "multi-divisor 3:3 symmetry is 3:3Q_W under ONE divisor, so not a gradient; kept for exact reproduction")
GATED = "observer detector: records without back-action (Study 5 D3); read once, gated by a flash (rank 4)"
DEC = ("observer detector with the D12b gated readout of the kicked arm (P_dec, rank 4): records without back-action "
       "on the arms (Study 5 D3); the 90-degree kick is in the readout (P_dec's declared equivalence)")


def _f(g, off=O, field="b"):
    return (g, tuple(off), field)


def _one_way(t, c, facs, why):
    return (t, c, tuple(facs), {"designated_one_way": why})


def _neg(off):
    return tuple(-v for v in off)


def _axis(axis):
    if axis not in (0, 1, 2):
        raise ValueError("axis must be 0, 1 or 2")
    e = [0, 0, 0]
    e[axis] = 1
    return tuple(e)


def _check_Q(Q):
    if type(Q) is not int or Q < 1:
        raise ValueError("Q must be a positive int")


def _square_terms(target, coeff, xs, ys, sign, why, extra=()):
    """coeff * extra * sum_j (x_j + sign*y_j)^2 as monomials (designated with ``why``)."""
    out = []
    ext = tuple(extra)
    for x, y in zip(xs, ys):
        out.append(_one_way(target, coeff, ext + (_f(x), _f(x)), why))
        out.append(_one_way(target, 2 * sign * coeff, ext + (_f(x), _f(y)), why))
        out.append(_one_way(target, coeff, ext + (_f(y), _f(y)), why))
    return out


# =============================================================================== carriers (C0)
def build_clock_ring(*, Q: int, period: int = 6, prefix: str = "X", name: str | None = "ring",
                     label: str = "official") -> Block:
    """Exact remainder-free clock ring.

    period 6: three gears ``<prefix>0..2`` with u = 3Q b (Q-scaled u = 3b, D = 6): (a, b) -> (b, b - a), period 6, r = 0
              stays; the ring phase offsets 0, 2, 4 make sum_j b_j^2 = 2A^2 and the cross sums ring invariants.
    period 4: two gears ``<prefix>0..1`` with u = 0: (a, b) -> (b, -a), period 4 (S5-M2's 90-degree grid).
    Reciprocal (self terms = gradient of (3Q/2) b^2). Vacuum (0, 0, 0)."""
    _check_Q(Q)
    if period == 6:
        gears = [f"{prefix}{j}" for j in range(3)]
        terms = [(g, 3 * Q, (_f(g),)) for g in gears]
    elif period == 4:
        gears = [f"{prefix}{j}" for j in range(2)]
        terms = []
    else:
        raise ValueError("period must be 6 or 4")
    return Block(tuple(GearType(g, label) for g in gears), tuple(terms), name=name, vacuum={g: 0 for g in gears},
                 params={"Q": Q, "period": period, "prefix": prefix}, Q=Q,
                 doc=f"period-{period} C0 clock ring (u = {'3Q b' if period == 6 else '0'})")


def build_fibre(*, Q: int, axis: int = 0, components=("F",), name: str | None = "fibre",
                label: str = "official") -> Block:
    """Exact d'Alembert fibre(s) along ``axis``: u = 3Q (b(x - e) + b(x + e)) for every component (Q-scaled
    u = 3(b_l + b_r), D = 6: ell = b_l + b_r, all C0). Reciprocal (gradient of 3Q sum_x b(x) b(x + e)). A right-moving
    profile b(x, t) = g(x - t) (prepared with a(x) = g(x + 1)) is transported exactly. Vacuum (0, 0, 0)."""
    _check_Q(Q)
    e = _axis(axis)
    terms = []
    for c in components:
        terms.append((c, 3 * Q, (_f(c, _neg(e)),)))
        terms.append((c, 3 * Q, (_f(c, e),)))
    return Block(tuple(GearType(c, label) for c in components), tuple(terms), name=name,
                 vacuum={c: 0 for c in components}, params={"Q": Q, "axis": axis, "components": tuple(components)},
                 Q=Q, doc="exact C0 d'Alembert fibre")


# =============================================================================== Born router / paired link clock
def build_born_router(*, Q: int, kappa: int, arm1, arm2, form: str = "opposite", name: str | None = "router",
                      vacuum_r: int = 0) -> Block:
    """Rank-3 |psi|^2 detector pair dP, dM reading two rings (qualified gear names ``arm1``, ``arm2``).

    form "opposite" (PAIRED LINK CLOCK): u_dP = +kappa sum_j (x_j + y_j)^2, u_dM = -kappa sum_j (x_j - y_j)^2; with
        EQUAL remainders the pair keeps r+ = r- whenever K+ - K- = D (matched: 2 kappa (I+ + I-) = 6Q) and gives
        exactly one click (dP: ell = +1 or dM: ell = -1).
    form "mirror": both +kappa sum (x_j +- y_j)^2; tokens lam and D - 1 - lam (S5-M2's M2-1).
    Matched quantization for rings of amplitude A: 16 kappa A^2 = 6Q (e.g. kappa = 3, Q = 8A^2).
    One-way OBSERVER terms (designated)."""
    _check_Q(Q)
    if form not in ("opposite", "mirror"):
        raise ValueError("form must be 'opposite' or 'mirror'")
    sm = -1 if form == "opposite" else 1
    terms = _square_terms("dP", kappa, arm1, arm2, +1, OBSERVER) + _square_terms("dM", sm * kappa, arm1, arm2, -1,
                                                                                  OBSERVER)
    return Block((GearType("dP"), GearType("dM")), tuple(terms), name=name, vacuum={"dP": vacuum_r, "dM": vacuum_r},
                 params={"Q": Q, "kappa": kappa, "form": form, "arm1": tuple(arm1), "arm2": tuple(arm2)}, Q=Q,
                 doc=f"rank-3 |psi|^2 detector pair ({form} form), observer")


def build_common_drive(*, Q: int, w: int, detectors, name: str | None = "drive") -> Block:
    """DC source gear S (u = 6Q b: (c, c) stays (c, c)) feeding every listed detector with u += w b_S: two detectors
    born at the vacuum with equal remainders keep r+ = r- and sweep their remainder class (the board-made token).
    The S self term is reciprocal; the drive terms are designated one-way."""
    _check_Q(Q)
    terms = [("S", 6 * Q, (_f("S"),))] + [_one_way(d, w, (_f("S"),), DRIVE) for d in detectors]
    return Block((GearType("S"),), tuple(terms), name=name, vacuum={"S": 0},
                 params={"Q": Q, "w": w, "detectors": tuple(detectors)}, Q=Q, doc="DC common drive")


# =============================================================================== n exits
def build_sequential_router(*, Q: int, kappa: int, stream: str, name: str | None = "seq") -> Block:
    """ONE link gear Lk with u = kappa * b_stream (on-site read of an intensity stream that arrives along a C0 fibre,
    one value per update). Visits k = 1..n deliver K = 2 kappa I_k to the SAME carried remainder; exit k = the first
    overflow at visit k. Matched: 2 kappa sum_k I_k = 6Q, so the n exits are consecutive arcs of the remainder
    circle (P(k) = I_k / sum I). Designated one-way (observer)."""
    _check_Q(Q)
    return Block((GearType("Lk"),), (_one_way("Lk", kappa, (_f(stream),), SEQ),), name=name, vacuum={"Lk": 0},
                 params={"Q": Q, "kappa": kappa, "stream": stream}, Q=Q, doc="sequential shared-remainder router")


def build_parallel_router(*, Q: int, kappa: int, streams, name: str | None = "par") -> Block:
    """Parallel-read CONTROL: exit gears E1..En read their own intensities in the same update with one shared token:
    E1 input -kappa I1 (clicks iff lam < 2 kappa I1), E2..En input +kappa I_k. Designated one-way (observer)."""
    _check_Q(Q)
    gears, terms = [], []
    for k, s in enumerate(streams):
        g = f"E{k + 1}"
        gears.append(GearType(g))
        terms.append(_one_way(g, -kappa if k == 0 else kappa, (_f(s),), PAR))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: 0 for g in gears},
                 params={"Q": Q, "kappa": kappa, "streams": tuple(streams)}, Q=Q, doc="parallel-read control")


# =============================================================================== F7 light-cone choice
EMIT_LIGHT = ("choice-front emission (F7, light carrier): Alice's front clock drives the headroom light one-way "
              "(u_P += gamma b_F); the far side reads the front without back-action")


def build_f7(*, Q: int, kappa: int, axis: int = 0, name: str | None = "f7", bob_gate: bool = False,
             carrier: str = "fibre", gamma: int = 0) -> Block:
    """The owner's light-cone choice (Study 5 F7) as ONE block of C0 carriers and choice gears.

    WARNING (manager ruling 10:2x, Study 7 ONE-P2): with carrier="fibre" the front moves on exact d'Alembert fibres at
    1 site/update along the axis = sqrt(3) c, i.e. on the TAXICAB cone (the cone gap the owner did NOT adopt). It is a
    MECHANISM TEST ONLY, not the approved form. carrier="light" carries the front on the headroom light gear
    u = (Q-1) Sum_6 b + 6b (round cone c_Q = sqrt((Q-1)/(3Q))) with a one-way source u_P += gamma b_F (status probe
    TC.17; exact only to O(1/A)). At odd Q use bob_gate=True: readers must be one-shot.

    Gears (every node holds all; roles come from the initial data):
      PH0..2  Alice's photon flash, three ring components (fibres along ``axis``); PG its unit marker (fibre, audit);
      C0..2   Alice's setting ring (u = 3Q b);
      dAp,dAm Alice's photon-gated rank-3 router: u = +-kappa sum_j b_PH (b_PH +- b_C) (zero without the photon);
      F0..2   Alice's front clock (u = 3Q b) + the GATED two-update kick (P2R):
              u_Fj += 3Q [ b_PG(x-e) (b_dAp + b_dAm)(b_Cj - a_Cj) - a_PG(x-e) (a_dAp + a_dAm) a_Cj ]
              (the marker passes x-e at snapshots t_A+1 (b) and t_A+2 (a) only, so the kick acts exactly twice and
              F = q * (Alice's setting clock) afterwards, q = the click quotient);
      P0..2   front fibres (C0) + exact one-way two-node source u_Pj(x) += 3Q (b_Fj(x) - a_Fj(x+e)): emits the
              right-moving copy b_P(x, t) = F(t - 1 - (x - x_A)), nothing to the left;
      B0..2   Bob's setting ring (u = 3Q b);
      dBp,dBm Bob's setting-gated rank-3 Born pair: u = +-kappa sum_j b_B (b_B +- b_P) (exactly one click per update;
              P(+) = (1 + q cos)/2 once the front is present, 1/2 before).
    Matched: 8 kappa A^2 = 6Q (A = 1: kappa = 3, Q = 4, D = 24). Detectors, kick and emission are designated one-way.
    ``bob_gate=True`` (odd-Q variant, TC.15b): Bob's pair is exposed ONCE, when his gate flash (fibre BG, audit) is at
    his node: u_dB+- = +-kappa sum_j b_BG b_B (b_B +- b_P) (rank 4, designated observer). Needed at odd Q, where the
    continuously exposed pair cannot be matched (parity) and loses its equal-remainder lock."""
    _check_Q(Q)
    e = _axis(axis)
    me = _neg(e)
    PH, C, F, P, B = ([f"{s}{j}" for j in range(3)] for s in ("PH", "C", "F", "P", "B"))
    gears = [GearType(g) for g in PH] + [GearType("PG", "audit")] + [GearType(g) for g in C]
    gears += [GearType("dAp"), GearType("dAm")] + [GearType(g) for g in F] + [GearType(g) for g in P]
    gears += [GearType(g) for g in B] + [GearType("dBp"), GearType("dBm")]
    if bob_gate:
        gears.append(GearType("BG", "audit"))
    if carrier not in ("fibre", "light"):
        raise ValueError("carrier must be 'fibre' or 'light'")
    terms = []
    fibres = PH + ["PG"] + (P if carrier == "fibre" else []) + (["BG"] if bob_gate else [])
    for g in fibres:                               # C0 fibres
        terms += [(g, 3 * Q, (_f(g, me),)), (g, 3 * Q, (_f(g, e),))]
    if carrier == "light":                         # headroom light: (Q-1) Sum_6 b + 6 b (reciprocal)
        from ..core.lattice import DIRECTIONS
        for g in P:
            terms += [(g, Q - 1, (_f(g, d),)) for d in DIRECTIONS] + [(g, 6, (_f(g),))]
    for g in C + F + B:                            # period-6 clocks
        terms.append((g, 3 * Q, (_f(g),)))
    for j in range(3):                             # Alice's photon-gated router
        terms.append(_one_way("dAp", kappa, (_f(PH[j]), _f(PH[j])), OBSERVER))
        terms.append(_one_way("dAp", kappa, (_f(PH[j]), _f(C[j])), OBSERVER))
        terms.append(_one_way("dAm", -kappa, (_f(PH[j]), _f(PH[j])), OBSERVER))
        terms.append(_one_way("dAm", kappa, (_f(PH[j]), _f(C[j])), OBSERVER))
    for j in range(3):                             # gated two-update kick (rank 4)
        for d in ("dAp", "dAm"):
            terms.append(_one_way(F[j], 3 * Q, (_f("PG", me), _f(d), _f(C[j])), IMPRINT))
            terms.append(_one_way(F[j], -3 * Q, (_f("PG", me), _f(d), _f(C[j], O, "a")), IMPRINT))
            terms.append(_one_way(F[j], -3 * Q, (_f("PG", me, "a"), _f(d, O, "a"), _f(C[j], O, "a")), IMPRINT))
    for j in range(3):                             # one-way emission into the front carrier
        if carrier == "fibre":
            terms.append(_one_way(P[j], 3 * Q, (_f(F[j]),), EMIT))
            terms.append(_one_way(P[j], -3 * Q, (_f(F[j], e, "a"),), EMIT))
        else:
            terms.append(_one_way(P[j], gamma, (_f(F[j]),), EMIT_LIGHT))
    gB = (_f("BG"),) if bob_gate else ()
    whyB = GATED if bob_gate else OBSERVER
    for j in range(3):                             # Bob's setting-gated (optionally flash-gated) Born pair
        terms.append(_one_way("dBp", kappa, gB + (_f(B[j]), _f(B[j])), whyB))
        terms.append(_one_way("dBp", kappa, gB + (_f(B[j]), _f(P[j])), whyB))
        terms.append(_one_way("dBm", -kappa, gB + (_f(B[j]), _f(B[j])), whyB))
        terms.append(_one_way("dBm", kappa, gB + (_f(B[j]), _f(P[j])), whyB))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: 0 for g in gears},
                 params={"Q": Q, "kappa": kappa, "axis": axis, "bob_gate": bob_gate, "carrier": carrier,
                         "gamma": gamma}, Q=Q,
                 doc="F7 light-cone choice" + (" (one-shot gated Bob)" if bob_gate else ""))


# =============================================================================== decoherence / back-action
def build_which_path_W(*, Q: int, Q_W: int, arm, N: int, name: str | None = "W") -> Block:
    """N nonlinear which-path gears W0..W(N-1) of S5-P2R's M2-2 (designed divisor 6 Q_W): W_j reads arm gear
    arm[j % 3] (designed K_W = 6 b_X: u = 3 (Q/Q_W) b_X) and kicks it by one unit (designed K_X += 6 b_W: u = 3Q b_W).
    Requires Q_W | Q. The hidden remainder r_W (designed 0..6Q_W-1) is prepared as (Q/Q_W) r_W. Designated (WPATH)."""
    _check_Q(Q)
    if Q % Q_W:
        raise ValueError("Q_W must divide Q")
    m = Q // Q_W
    gears, terms = [], []
    for j in range(N):
        w, x = f"W{j}", arm[j % len(arm)]
        gears.append(GearType(w))
        terms.append(_one_way(w, 3 * m, (_f(x),), WPATH))
        terms.append(_one_way(x, 3 * Q, (_f(w),), WPATH))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: 0 for g in gears},
                 params={"Q": Q, "Q_W": Q_W, "arm": tuple(arm), "N": N}, Q=Q, doc="M2-2 which-path gears")


def build_gated_pair(*, Q: int, kappa: int, arm1, arm2, gate: str, name: str | None = "exit") -> Block:
    """Exit pair (mirror form) read ONCE, when the gate flash is at the node: u_dP = kappa g sum (x + y)^2,
    u_dM = kappa g sum (x - y)^2 (rank 4, g = b of the gate fibre). With 16 kappa = 6Q the outcome is S5-P2R's
    ell+ = floor((I+ + lam)/8), ell- = floor((I- + 7 - lam)/8) for tokens 2 kappa lam, 2 kappa (7 - lam).
    Designated observer."""
    _check_Q(Q)
    g = (_f(gate),)
    terms = _square_terms("dP", kappa, arm1, arm2, +1, GATED, g) + _square_terms("dM", kappa, arm1, arm2, -1, GATED, g)
    return Block((GearType("dP"), GearType("dM")), tuple(terms), name=name, vacuum={"dP": 0, "dM": 0},
                 params={"Q": Q, "kappa": kappa, "arm1": tuple(arm1), "arm2": tuple(arm2), "gate": gate}, Q=Q,
                 doc="gated exit pair (observer)")


def _rot(names, c):
    """(R^c X)_j as (sign, gear name) for the 90-degree pair rotation R: (X0, X1) -> (X1, -X0)."""
    v = [(1, names[0]), (1, names[1])]
    for _ in range(c % 4):
        v = [v[1], (-v[0][0], v[0][1])]
    return v


def build_dec_toy(*, Q: int, c: int, name: str | None = "dec") -> Block:
    """S5-M2's D12b toy (P_dec) as gears. Arms X1 = (X1_0, X1_1), X2 = (X2_0, X2_1): exact period-4 clocks (u = 0).
    W1, W2: u = 6 sum_j X_kj^2 (K = D/2 for A^2 = sum X^2, D = 24 A^2, Q = 4A^2). Exit pair (mirror form):
    u_dP = 3 [b_W1 I+(R^c X1, X2) + b_W2 I+(X1, R^c X2)], u_dM the same with I- (rank 4: the which-path click gates
    the readout of the arm kicked by c x 90 degrees). W and the exit pair are designated (observer / D12b readout)."""
    _check_Q(Q)
    X1, X2 = ["X1_0", "X1_1"], ["X2_0", "X2_1"]
    gears = [GearType(g) for g in X1 + X2] + [GearType(g) for g in ("W1", "W2", "dP", "dM")]
    terms = []
    for wn, arm in (("W1", X1), ("W2", X2)):
        for x in arm:
            terms.append(_one_way(wn, 6, (_f(x), _f(x)), OBSERVER))
    for target, sgn in (("dP", 1), ("dM", -1)):
        for wn, U, V in (("W1", _rot(X1, c), [(1, X2[0]), (1, X2[1])]), ("W2", [(1, X1[0]), (1, X1[1])], _rot(X2, c))):
            for (su, u), (sv, v) in zip(U, V):          # 3 b_W (s_u u + sgn s_v v)^2
                terms.append(_one_way(target, 3, (_f(wn), _f(u), _f(u)), DEC))
                terms.append(_one_way(target, 3, (_f(wn), _f(v), _f(v)), DEC))
                terms.append(_one_way(target, 6 * sgn * su * sv, (_f(wn), _f(u), _f(v)), DEC))
    return Block(tuple(gears), tuple(terms), name=name, vacuum={g.name: 0 for g in gears},
                 params={"Q": Q, "c": c}, Q=Q, doc="D12b QM-deviation toy (P_dec)")


def _pmul(p, q):
    """product of two polynomials {tuple(sorted gear names): int coeff}."""
    out = {}
    for k1, c1 in p.items():
        for k2, c2 in q.items():
            k = tuple(sorted(k1 + k2))
            out[k] = out.get(k, 0) + c1 * c2
    return {k: c for k, c in out.items() if c}


def _padd(*ps):
    out = {}
    for p in ps:
        for k, c in p.items():
            out[k] = out.get(k, 0) + c
    return {k: c for k, c in out.items() if c}


def _pscale(p, a):
    return {k: a * c for k, c in p.items() if a * c}


def build_spring_backaction_router(*, Q: int, kappa: int, lam: int, arm1, arm2, name: str | None = "bs") -> Block:
    """(ii) BACK-ACTING reciprocal detector pair with a COMPLETE OD4 spring (manager ruling 2, 09:5x):

        Phi = kappa b_dP |U|^2 + kappa b_dM |V|^2 - (lam/4) [ (b_dP^2 + |U|^2)^2 + (b_dM^2 + |V|^2)^2 ],

    U = X1 + X2, V = X1 - X2, field signs s(dP) = +1, s(dM) = -1, X0 = 0 (deviation form: no constant, vacuum fixed).
    u = s dPhi/db for every gear (the self-quartics -lam b_d^3 and -lam |U|^2 U_j are included). No designation."""
    _check_Q(Q)
    if type(lam) is not int or lam < 0:
        raise ValueError("lam must be a non-negative int")
    U = [{(x,): 1, (y,): 1} for x, y in zip(arm1, arm2)]
    V = [{(x,): 1, (y,): -1} for x, y in zip(arm1, arm2)]
    U2 = _padd(*[_pmul(u, u) for u in U])
    V2 = _padd(*[_pmul(v, v) for v in V])
    P, M = {("dP",): 1}, {("dM",): 1}
    sP = _padd(_pmul(P, P), U2)                 # b_dP^2 + |U|^2
    sM = _padd(_pmul(M, M), V2)
    u = {}
    u["dP"] = _padd(_pscale(U2, kappa), _pscale(_pmul(sP, P), -lam))
    u["dM"] = _pscale(_padd(_pscale(V2, kappa), _pscale(_pmul(sM, M), -lam)), -1)       # s = -1
    for j, (x, y) in enumerate(zip(arm1, arm2)):
        back_U = _padd(_pscale(_pmul(P, U[j]), 2 * kappa), _pscale(_pmul(sP, U[j]), -lam))   # dPhi/dU_j
        back_V = _padd(_pscale(_pmul(M, V[j]), 2 * kappa), _pscale(_pmul(sM, V[j]), -lam))   # dPhi/dV_j
        u[x] = _padd(back_U, back_V)                     # dU_j/dx = 1, dV_j/dx = 1
        u[y] = _padd(back_U, _pscale(back_V, -1))        # dU_j/dy = 1, dV_j/dy = -1
    terms = [(t, c, tuple(_f(gn) for gn in key)) for t, poly in u.items() for key, c in sorted(poly.items())]
    gears = (GearType("dP"), GearType("dM", sign=-1, sign_why=(
        "opposite-sign detector of the paired link clock: its input is -kappa|X1-X2|^2 (equal remainders, Study 5 "
        "B3/T4); s = -1 makes the pair the gradient of one potential")))
    return Block(gears, tuple(terms), name=name, vacuum={"dP": 0, "dM": 0},
                 params={"Q": Q, "kappa": kappa, "lam": lam, "arm1": tuple(arm1), "arm2": tuple(arm2)}, Q=Q,
                 doc="back-acting reciprocal detector pair with a complete OD4 spring (rank 4)")


def build_backaction_router(*, Q: int, kappa: int, g: int, arm1, arm2, name: str | None = "ba") -> Block:
    """(ii) BACK-ACTING reciprocal detector pair from ONE potential (no designation):

        Phi = kappa b_dP |U|^2 + kappa b_dM |V|^2 - (g/2) (b_dP^2 |U|^2 + b_dM^2 |V|^2),  U = X1 + X2, V = X1 - X2,

    field signs s(dP) = +1, s(dM) = -1 (u_dM = -dPhi/db_dM = -kappa |V|^2 + g b_dM |V|^2: the opposite-sign detector).
    The arms feel u_x = dPhi/dx: the click pushes back. g = 0: rank 3 (Study 5's reciprocal coupling, D3); g = 2 kappa:
    rank 4 and sign-definite (2(kappa b - (g/2) b^2) <= 0 for every integer b, OD4 / S5-O4). Matched as the router."""
    _check_Q(Q)
    terms = []
    gears = (GearType("dP"), GearType("dM", sign=-1, sign_why=(
        "opposite-sign detector of the paired link clock: its input is -kappa|X1-X2|^2 (equal remainders, Study 5 "
        "B3/T4); s = -1 makes the pair the gradient of one potential")))
    for x, y in zip(arm1, arm2):
        # detectors: u_dP = kappa |U|^2 - g b_dP |U|^2 ; u_dM = -kappa |V|^2 + g b_dM |V|^2
        for tgt, s_y, s_t in (("dP", 1, 1), ("dM", -1, -1)):
            for fac, cf in (((_f(x), _f(x)), 1), ((_f(x), _f(y)), 2 * s_y), ((_f(y), _f(y)), 1)):
                terms.append((tgt, s_t * kappa * cf, fac))
                terms.append((tgt, -s_t * g * cf, (_f(tgt),) + fac))
        # arms: u_x = 2k b_dP U + 2k b_dM V - g b_dP^2 U - g b_dM^2 V ; u_y = 2k b_dP U - 2k b_dM V - g b_dP^2 U + g b_dM^2 V
        for tgt, s_v in ((x, 1), (y, -1)):
            for src in (x, y):
                s_src = 1 if src == x else -1             # V = x - y
                terms.append((tgt, 2 * kappa, (_f("dP"), _f(src))))
                terms.append((tgt, 2 * kappa * s_v * s_src, (_f("dM"), _f(src))))
                terms.append((tgt, -g, (_f("dP"), _f("dP"), _f(src))))
                terms.append((tgt, -g * s_v * s_src, (_f("dM"), _f("dM"), _f(src))))
    return Block(gears, tuple(terms), name=name, vacuum={"dP": 0, "dM": 0},
                 params={"Q": Q, "kappa": kappa, "g": g, "arm1": tuple(arm1), "arm2": tuple(arm2)}, Q=Q,
                 doc=f"back-acting reciprocal detector pair (rank {4 if g else 3})")


# Reversor declarations (binding stage-1 condition 3; data, checked in tests/test_choice.py TC.2, TC.10, TC.12):
MIRROR = {
    "build_clock_ring": "Mp (M', parity-preserving) per gear; exact (b-only); C0: any constant remainder works",
    "build_fibre": "Mp per gear; exact (b-only)",
    "build_born_router": "Mp per gear (and M); exact (b-only); kinds are mirror-even (TC.2 log check with M)",
    "build_common_drive": "Mp per gear; exact (b-only)",
    "build_sequential_router": "Mp per gear; exact (b-only)",
    "build_parallel_router": "Mp per gear; exact (b-only)",
    "build_which_path_W": "Mp per gear; exact (b-only)",
    "build_gated_pair": "Mp per gear; exact (b-only)",
    "build_dec_toy": "M (and Mp) per gear; exact (b-only)",
    "build_backaction_router": "Mp per gear; exact (b-only); NOT J-odd (even-degree terms), so no JR/JM",
    "build_spring_backaction_router": "Mp per gear; exact (b-only); NOT J-odd",
    "build_f7": ("NONE KNOWN: a-read gears (gated kick, emission); per-gear M/Mp are NOT reversors (TC.12); the staged "
                 "inverse is exact (rewind in every run); a staggered map for these a-read gears is OPEN"),
}
VACUUM_NOTE = ("M'-fixed vacuum remainder exists only for ODD Q (r0 = 3Q - 1 or 3Q); even Q (forced by matched "
               "quantization in the Born routers, F7 and M2-2) has NO mirror-fixed vacuum")

__all__ = ["MIRROR", "VACUUM_NOTE", "OBSERVER", "build_clock_ring", "build_fibre", "build_born_router", "build_common_drive",
           "build_sequential_router", "build_parallel_router", "build_f7", "build_which_path_W", "build_gated_pair",
           "build_dec_toy", "build_backaction_router", "build_spring_backaction_router"]
