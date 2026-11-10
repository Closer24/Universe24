"""ONE (Study 22, builder ONE-A): THE composed candidate version of the package. TENSOR BLOCKS ONLY. NEW file; no
existing package file is modified by it.

    ONE = default_system(Q)          hands ON (chiral + electroweak, OWNER decision 5) with FIX-i (OWNER decision v8-1:
                                     build_graviweak_b(lam_H = 0, lam_L = 0), singlet-half hop kept) and GRAV-FIX A
                                     (beta detuned, already the default)
        + block "cosmic"             NEW LAW (OWNER decision 8, WIND): the cosmic clock as a tensor layer

in ONE tensor, at ONE odd Q, on ONE periodic L^3 cube with six faces, run by Rule3 only. Only the fixed tensor + the seed
(initial data, prepare/one.py) + Rule3: no prescribed f(t), no posted hold, no run-time intervention, no comparison or
branch in the law (OWNER rule, manager 14:47 UTC). Every coefficient below is a fixed integer of the tensor.

The cosmic block (7 gear types per node; s15/AGREE_COSMIC E2, s13/AGREE_INTEGRATED, CC-A s13/INTEGRATED_work/ib.py)
    u_Th = (D - 6 kTh) b_Th + kTh Sum_6 b_Th(y) - g_w (b_dp - b_dm) b_Th     WIND hand: no bare spring, rigid face
                                                                            coupling, parametric stiffness (rank 3)
    u_Mj = h Sum_{y~x} (b_Th(x) + b_Th(y)) b_Mj(y),  j = 1, 2              L-Theta: complex first-order matter reading the
                                                                            link-averaged hand as ONE common factor
    u_dp = c (b_M1^2 + b_M2^2) b_Lp,   u_dm = -c (b_M1^2 + b_M2^2) b_Lm      matched shared-remainder choice pair (CC-B form),
                                                                            loaded by the intensity of Theta-READING matter
    u_Lp = D b_Lp,   u_Lm = D b_Lm                                          static Born loads (initial data p, Q - p)
  K+ - K- = 2 (u_dp - u_dm) = 2c I (b_Lp + b_Lm) = D I when b_Lp + b_Lm = S_L = 3Q/c (c | 3Q; CC-A/CC-B: c = 3, S_L = Q).
  Here c = the smallest divisor of 3Q with D S_L < 2^60 (int64 headroom of the static loads u_L = D b_L; Q = 2^33 + 1 =
  3^2 67 683 20857 gives c = 1809, S_L = 14,245,331). Exactly I unit choices per update and node,
  r+ - r- invariant (the shared-remainder lock), N+ = floor((r0 + Sum K+)/D) (Born ledger).
  Ranks: the hand and the matter rank 3; the pair rank 4 of the approved NARROW kind (uncharged singlet b_L x the covariant
  composite |psi|^2). B3: every monomial on one node or one face link. b-only (no two-time read). Deviation form: every
  input vanishes at the vacuum (0, 0, 3Q - 1).
  One-way (DESIGNATED, each with its reason): the hand's read of Delta (2 monomials), the matter's read of the hand
  (24), the pair's read of matter and load (4): 30 designations. They are one-way by THEOREM O: the hand may carry no
  additive source (row Theta) and the pair load must come only from Theta readers (row (a)).

Which package sectors read Theta?  NONE (exact census: theta_reading_census). A Theta reader must have EVERY input equal to
  Theta x (odd in the reader), with the package's own coefficients recovered at Theta = Theta0: every on-site coefficient
  c must be divisible by Theta0 and every link coefficient by 2 Theta0 (link-averaged factor). The first-order package
  sectors fail this integer-grain condition by many orders of magnitude (L0: on-site entries 6; matter: E1's g_A = 1;
  matter2: Yukawa/Wilson-Yukawa entries), while a hand needs Theta0 >> 1 (its resolution; CC-A: 2^29). In addition the
  E1-charged pair "matter" would need Theta x E1 entries (link x composite: outside the narrow rank-4 kind) and an exact E1
  source for its Theta-dressed current, i.e. Theta x lapse x link x matter = rank 5 (FORBIDDEN). Second-order sectors
  (links, Higgs, E1 fields, lapse/beta/background, choice rings) are THEOREM-O class (C): they cannot be readers.
  Therefore ONE adds CC-A's own Theta-reading species (M1, M2) as extra gears in the same tensor, and the cosmic block
  neither reads nor is read by any package gear: the tensor is BLOCK-DIAGONAL between the package and the cosmic clock.
  The package sectors do not read Theta and will not fold; the cosmic matter folds approximately (THEOREM O (b)-(d)).

COUPLING (couple_doublet=True; OPT-IN ONLY, DEFAULT OFF): NEW LAW candidate, REJECTED by the owner (matter must not read
  the clock); measured runaway at L = 6 t ~ 1,547-1,554 and L = 4 t ~ 662 (Study 30); kept for the record. Time labels
  (date -u): the owner decisions were received at 15:24:47 / 15:26:41 UTC (the coupling was approved in the second; the
  older "owner 15:4x UTC" stamps were relay stamps), the rejection at about 16:13 UTC. The opt-in build is bit-identical to
  Study 22's run C1 (dynamics fingerprint 593753fa...): the doublet's FIRST-ORDER potential
  (blocks matter, matter2, the chiral entries touching matter, gwb) carries the hand as ONE common factor (theta_scale_block),
  E1 unscaled, second-order self terms unscaled. Integral only for Theta0 <= 64 at today's constants (Yukawa on-site entries
  2^6 * 6451); Theta0 = 256 with the package mass m * 2^22, 4 | m. It is not an exact (A) reader (E1, (C) fields): the package
  bang then recurs APPROXIMATELY (Study 22 run C1). The DEFAULT, couple_doublet=False, is ONE v1, BLOCK-DIAGONAL (described
  above; dynamics fingerprint 77f6d251...).

Hooks: route_b (ONE v2: EW-BUILDER's layers/electroweak_b.compose_electroweak_b on the hands-OFF base, or any callable
  base -> System), families (ONE v3: three families / Pauli copies, NOT approved: raises).
"""
from __future__ import annotations

from math import gcd

from ..core.lattice import DIRECTIONS
from ..core.tensor import Block, GearType
from .system import Q_DEFAULT, System, default_system

ZERO = (0, 0, 0)
COSMIC_NS = "cosmic"
COSMIC_GEARS = ("Th", "M1", "M2", "Lp", "Lm", "dp", "dm")
COSMIC_LABELS = {"Th": "audit", "M1": "official", "M2": "official", "Lp": "audit", "Lm": "audit", "dp": "official",
                 "dm": "official"}
THETA0_DEFAULT = 1 << 24       # hand amplitude (initial data scale); D * Theta0 < 2^61 keeps the board int64
H_DEFAULT = 1 << 7             # L-Theta hop: 24 h Theta0 = D - 6 (the matter band 2 cos w = (1/3) Sum cos k, inside)
K_THETA_DEFAULT = 1 << 32      # rigid face coupling: 2 kTh / D = 1/6 (CC-A's 2^30 at Q = 2^31 + 1)
G_W_DEFAULT = 1310             # CC-A's pre-registered rule round((pi/200)^2 D N / (2 A^2)), L = 6, A = 2^10 (Tq = 100)
A_COSMIC_DEFAULT = 1 << 10     # cosmic matter packet amplitude (seed data; prepare/one.py)
LOAD_HEADROOM = 1 << 60        # static loads: D * S_L < 2^60 (int64 engine path)
ONE_VERSION = "ONE v1 (Study 22, ONE-A)"
COUPLED_THETA0 = 64            # largest power of 2 dividing the doublet's Yukawa grain 2^6 * 6451 (today's mass 4915 * 2^22)
DOUBLET_BLOCKS = ("matter", "matter2", "chiral", "gwb")

WHY_WIND = ("NEW LAW (owner decision 8, WIND; s15 AGREE_COSMIC E2): the hand reads the pair record Delta = b_dp - b_dm "
            "as a parametric stiffness -g_w Delta Theta; the pair does not feel the hand (one-way: THEOREM O row Theta, "
            "no additive source)")
WHY_LTHETA = ("NEW LAW (owner decision 8, L-Theta; s13 CC-A): the matter reads the link-averaged hand as ONE common "
              "factor; the hand does not feel the matter's energy (one-way: THEOREM O row Theta, no additive source)")
WHY_PAIR = ("NEW LAW (owner decision 8, matched shared-remainder pair, CC-B form): loaded by the intensity of "
            "Theta-reading matter times its static Born load; the matter does not feel the pair (one-way: THEOREM O (a))")

# WHY_COUPLE is TENSOR METADATA: theta_scale_block writes it into every Theta-scaled (designated) entry and
# Tensor.fingerprint hashes it. It is kept VERBATIM so that one_system(couple_doublet=True) stays bit-identical to Study 22's
# C1 (dynamics fingerprint 593753fa..., canonical fingerprint 1a3f998e...). Its "APPROVED ... owner 15:4x UTC" is historical:
# approved 15:26:41 UTC, REJECTED by the owner at about 16:13 UTC (date -u). The current status is COUPLING_STATUS.
WHY_COUPLE = ("APPROVED NEW LAW (owner 15:4x UTC; Study 22 coupling, manager 15:06): the package Dirac doublet's FIRST-ORDER potential "
              "(free Wilson-Dirac pairs, chiral transport / Yukawa / Wilson-Yukawa, FIX-i singlet-half lapse hop) carries the "
              "cosmic hand as ONE common factor (link-averaged on link terms); the hand does not feel it (one-way: THEOREM O "
              "row Theta). E1 entries are NOT scaled (integer grain: g_A = 1 on links).")
COUPLING_STATUS = ("NEW LAW candidate, REJECTED by the owner (matter must not read the clock); measured runaway at L = 6 "
                   "t ~ 1,547-1,554 and L = 4 t ~ 662 (Study 30); kept for the record")

NEW_LAWS = (
    "WIND hand Th: per-node gear, no bare spring, rigid face coupling kTh, stiffness -g_w Delta Theta (owner decision 8)",
    "L-Theta: CC-A's complex first-order matter (M1, M2) hops only through the link-averaged hand (owner decision 8)",
    "matched shared-remainder choice pair (dp, dm) loaded by |psi|^2 of the Theta readers, with static Born loads "
    "(Lp, Lm) (owner decision 8; narrow rank-4 kind, owner decision 4)",
    "FIX-i (owner decision v8-1): coefficient choice lam_H = lam_L = 0 in gwb; NOT a new law (existing parameters)",
)
EXCLUDED = {
    "zero-time hold (ZT)": "a posted schedule; its tensor generation is OPEN, and the owner rule forbids hand-placed "
                           "schedules",
    "confirmation gate composed with folding": "light-gated pairs read by the hand break THEOREM O (a); OPEN",
    "Pauli copies / three families / configuration space": "NEW LAWs not approved (ONE v3 hook: families)",
    "route B (U(2) links, plaquette)": "being built by EW-BUILDER (ONE v2 hook: route_b)",
    "FIX-C+ (two tuned lapse counter-terms)": "NEW LAW candidate; tuned counter-terms are not solutions (owner rule)",
    "package sectors as Theta readers": "integer grain + rank 5 / non-narrow (theta_reading_census); NOT possible",
    "cosmic matter <-> lapse (universality for the Theta readers)": "legal at rank 4 (Theta x F x b' is narrow) but a "
                                                                     "(C)-field defect and a new coupling: OPEN, not built",
    "Theta-coupled doublet (matter reads the clock; opt-in couple_doublet=True)": COUPLING_STATUS,
}


def _divisors(n: int) -> list[int]:
    f, m, p = {}, n, 2
    while p * p <= m:
        while m % p == 0:
            f[p] = f.get(p, 0) + 1
            m //= p
        p += 1
    if m > 1:
        f[m] = f.get(m, 0) + 1
    divs = [1]
    for q, e in f.items():
        divs = [d * q ** k for d in divs for k in range(e + 1)]
    return sorted(divs)


def default_pair_c(Q: int) -> int:
    """Smallest divisor c >= 3 of 3Q with D (3Q/c) < 2^60 (construction-time choice of the load scale; c = 3 if none)."""
    D = 6 * Q
    for c in _divisors(3 * Q):
        if c >= 3 and D * (3 * Q // c) < LOAD_HEADROOM:
            return c
    return 3


def cosmic_params(Q: int = Q_DEFAULT, *, theta0: int = THETA0_DEFAULT, h: int = H_DEFAULT,
                  k_theta: int = K_THETA_DEFAULT, g_w: int = G_W_DEFAULT, c_pair: int | None = None) -> dict:
    """Validated integer parameters of the cosmic block (raises on a violated design rule)."""
    c_pair = default_pair_c(Q) if c_pair is None else c_pair
    for nm, x in (("Q", Q), ("theta0", theta0), ("h", h), ("k_theta", k_theta), ("g_w", g_w), ("c_pair", c_pair)):
        if type(x) is not int or x < 1:
            raise ValueError(f"{nm} must be a positive Python int")
    if (3 * Q) % c_pair:
        raise ValueError("c_pair must divide 3Q (matched pair: b_Lp + b_Lm = 3Q/c_pair)")
    if Q < 3 or Q % 2 == 0:
        raise ValueError("ONE ODD Q (the vacuum 3Q - 1 is R'-fixed only for odd Q)")
    D = 6 * Q
    if not 6 * k_theta < D:
        raise ValueError("kTh too large: the hand's corner mode needs 6 kTh < D (stability)")
    if 24 * h * theta0 > D:
        raise ValueError("24 h Theta0 > D: the Theta-reading matter leaves CC-A's inside-the-band design")
    return {"Q": Q, "D": D, "theta0": theta0, "h": h, "k_theta": k_theta, "g_w": g_w, "c_pair": c_pair,
            "load_sum": 3 * Q // c_pair,
            "band_24_h_theta0_over_D": f"{24 * h * theta0}/{D}", "rigidity_2kTh_over_D": f"{2 * k_theta}/{D}",
            "int64_headroom_bits_D_theta0": (D * theta0).bit_length(),
            "matched_pair": "K+ - K- = 2 c_pair I (b_Lp + b_Lm) = D I for b_Lp + b_Lm = load_sum = 3Q/c_pair (data)",
            "g_w_rule": "CC-A pre-registered: round((pi/(2 Tq))^2 D N / Sum I0), Tq = 100, L = 6, A = 2^10 -> 1310"}


def build_cosmic(Q: int = Q_DEFAULT, *, theta0: int = THETA0_DEFAULT, h: int = H_DEFAULT,
                 k_theta: int = K_THETA_DEFAULT, g_w: int = G_W_DEFAULT, c_pair: int | None = None,
                 name: str = COSMIC_NS) -> Block:
    """The cosmic clock as ONE tensor block (see the module docstring). Vacuum (0, 0, 3Q - 1) on every gear."""
    prm = cosmic_params(Q, theta0=theta0, h=h, k_theta=k_theta, g_w=g_w, c_pair=c_pair)
    D, c = prm["D"], prm["c_pair"]
    terms = [("Th", D - 6 * k_theta, (("Th", ZERO, "b"),))]
    terms += [("Th", k_theta, (("Th", e, "b"),)) for e in DIRECTIONS]
    terms += [("Th", -g_w, (("dp", ZERO, "b"), ("Th", ZERO, "b")), {"designated_one_way": WHY_WIND}),
              ("Th", g_w, (("dm", ZERO, "b"), ("Th", ZERO, "b")), {"designated_one_way": WHY_WIND})]
    for mj in ("M1", "M2"):
        for e in DIRECTIONS:
            terms.append((mj, h, (("Th", ZERO, "b"), (mj, e, "b")), {"designated_one_way": WHY_LTHETA}))
            terms.append((mj, h, (("Th", e, "b"), (mj, e, "b")), {"designated_one_way": WHY_LTHETA}))
    for mj in ("M1", "M2"):
        terms.append(("dp", c, ((mj, ZERO, "b"), (mj, ZERO, "b"), ("Lp", ZERO, "b")), {"designated_one_way": WHY_PAIR}))
        terms.append(("dm", -c, ((mj, ZERO, "b"), (mj, ZERO, "b"), ("Lm", ZERO, "b")), {"designated_one_way": WHY_PAIR}))
    terms += [("Lp", D, (("Lp", ZERO, "b"),)), ("Lm", D, (("Lm", ZERO, "b"),))]
    gears = tuple(GearType(g, COSMIC_LABELS[g]) for g in COSMIC_GEARS)
    return Block(gears, tuple(terms), name=name, vacuum={g: 3 * Q - 1 for g in COSMIC_GEARS},
                 params=dict(prm, law="WIND hand + L-Theta matter + matched pairs (NEW LAW, owner decision 8)"),
                 doc="cosmic clock (Study 22 ONE): WIND hand, L-Theta matter, matched shared-remainder choice pairs",
                 Q=Q)


def _is_doublet_term(block: Block, t) -> bool:
    names = [block.qualify(t[0])] + [block.qualify(f[0]) for f in t[2]]
    return any(n.startswith("matter.") or n.startswith("matter2.") for n in names)


def theta_scale_block(block: Block, theta0: int, hand: str = f"{COSMIC_NS}.Th", select=None) -> Block:
    """COPY of ``block`` whose selected terms carry the hand as ONE common factor: an on-site term c * prod -> (c/Theta0)
    Theta_x * prod; a link term (factors on {0, e}) -> (c/(2 Theta0)) (Theta_x + Theta_{x+e}) * prod. Each scaled entry is
    designated one-way (the hand does not feel it). Raises if a coefficient is not divisible (integer grain) or if a term
    would reach rank 5 (it already has 3 factors). Unselected terms are kept unchanged (construction-time only)."""
    out = []
    for t in block.terms:
        if select is not None and not select(block, t):
            out.append(t)
            continue
        target, c, facs = t[0], int(t[1]), tuple(t[2])
        if len(facs) >= 3:
            raise ValueError(f"block {block.name!r}: Theta x a degree-3 entry would be rank 5 (FORBIDDEN)")
        offs = {tuple(f[1]) for f in facs if tuple(f[1]) != ZERO}
        why = WHY_COUPLE + ((" | " + t[3]["designated_one_way"]) if len(t) > 3 and t[3] else "")
        if not offs:
            if c % theta0:
                raise ValueError(f"block {block.name!r}: on-site coefficient {c} not divisible by Theta0 = {theta0}")
            out.append((target, c // theta0, facs + ((hand, ZERO, "b"),), {"designated_one_way": why}))
        else:
            (e,) = offs
            if c % (2 * theta0):
                raise ValueError(f"block {block.name!r}: link coefficient {c} not divisible by 2 Theta0 = {2 * theta0}")
            for off in (ZERO, e):
                out.append((target, c // (2 * theta0), facs + ((hand, off, "b"),), {"designated_one_way": why}))
    return Block(block.gears, tuple(out), name=block.name, vacuum=dict(block.vacuum),
                 params=dict(block.params, theta_scaled={"theta0": theta0, "hand": hand}),
                 doc=block.doc + " [Theta-scaled first-order entries: Study 22 coupling option]", Q=block.Q)


# ======================================================================== the Theta-reading census (static, exact)
def _ns(name: str) -> str:
    return name.split(".", 1)[0]


def theta_reading_census(tensor, theta0: int = THETA0_DEFAULT, exclude=(COSMIC_NS,)) -> dict:
    """Exact census of which namespaces COULD read Theta as an (A)-class sector (THEOREM O): every gear's input must be
    Theta x (its present input) with integer coefficients at Theta0, i.e. each on-site coefficient c with Theta0 | c and
    each link coefficient with 2 Theta0 | c (link-averaged factor). Per gear type: first-order iff its own-gear inertia
    s_g = Sum of its degree-1 self coefficients (any offset) is < D/2. Reported per namespace: first-order gear count,
    max admissible Theta0 (gcd rule; 0 = impossible), entries that would become rank 5 (degree 3 already), entries reading
    E1 gears (Theta x E1 link/potential x matter: not the narrow kind), entries reading any link gear, two-time reads, and
    the E1 dressed-source entries reading the namespace (they would need Theta: rank 5), and LOAD-DRIVEN entries (no
    factor from a first-order node gear: e.g. a choice pair; not (A)-class: THEOREM O row A, AGREE_COSMIC C5)."""
    D = 6 * tensor.Q
    names = tensor.names
    gears = tensor.gears
    inertia = [0] * tensor.G
    for m in tensor.monomials:
        if m.degree == 1 and m.factors[0].gear == m.target and m.factors[0].field == "b":
            inertia[m.target] += m.coeff
    first = [i for i in range(tensor.G) if abs(inertia[i]) < D // 2]
    per: dict[str, dict] = {}
    for i, nm in enumerate(names):
        ns = _ns(nm)
        if ns in exclude:
            continue
        rec = per.setdefault(ns, {"gear_types": 0, "first_order_types": 0, "second_order_types": 0, "g_site": 0,
                                  "g_link_half": 0, "odd_link_coeff": 0, "deg3_terms": 0, "em_reads": 0,
                                  "link_reads": 0, "a_reads": 0, "terms": 0, "dressed_source_terms_reading_it": 0,
                                  "load_terms": 0})
        rec["gear_types"] += 1
        rec["first_order_types" if i in first else "second_order_types"] += 1
    fo = set(first)
    fo_node = {i for i in fo if gears[i].link is None}
    cross = {"cosmic_reads_package": 0, "package_reads_cosmic": 0}
    for m in tensor.monomials:
        tns = _ns(names[m.target])
        if tns in exclude:
            cross["cosmic_reads_package"] += int(any(_ns(names[f.gear]) not in exclude for f in m.factors))
            continue
        if any(_ns(names[f.gear]) in exclude for f in m.factors):
            cross["package_reads_cosmic"] += 1
            continue                     # an already Theta-scaled entry (coupling option): not re-counted below
        if tns == "em" and m.degree == 3:
            for f in m.factors:
                fns = _ns(names[f.gear])
                if fns != "em" and fns in per and f.gear in fo:
                    per[fns]["dressed_source_terms_reading_it"] += 1
                    break
        if m.target not in fo:
            continue
        rec = per[tns]
        rec["terms"] += 1
        link = any(f.offset != ZERO for f in m.factors)
        c = abs(m.coeff)
        if link:
            if c % 2:
                rec["odd_link_coeff"] += 1
            rec["g_link_half"] = gcd(rec["g_link_half"], c // 2)
        else:
            rec["g_site"] = gcd(rec["g_site"], c)
        rec["deg3_terms"] += int(m.degree == 3)
        rec["em_reads"] += int(any(_ns(names[f.gear]) == "em" for f in m.factors))
        rec["link_reads"] += int(any(gears[f.gear].link is not None for f in m.factors))
        rec["a_reads"] += int(any(f.field == "a" for f in m.factors))
        rec["load_terms"] += int(not any(f.gear in fo_node for f in m.factors))
    readers, non_readers = [], []
    for ns, rec in sorted(per.items()):
        if rec["first_order_types"] == 0:
            rec["theta0_max"] = 0
            rec["verdict"] = "second-order (THEOREM O class C): cannot be a Theta reader"
        else:
            tmax = 0 if rec["odd_link_coeff"] else gcd(rec["g_site"], rec["g_link_half"])
            rec["theta0_max"] = tmax
            why = []
            if tmax < theta0:
                why.append(f"integer grain: max Theta0 = {tmax} < {theta0}")
            if rec["deg3_terms"]:
                why.append(f"{rec['deg3_terms']} entries would become rank 5 (FORBIDDEN)")
            if rec["em_reads"]:
                why.append(f"{rec['em_reads']} E1 entries (Theta x E1 x matter: not the narrow kind)")
            if rec["dressed_source_terms_reading_it"]:
                why.append(f"its exact E1 source would need Theta x lapse x link x matter: "
                           f"{rec['dressed_source_terms_reading_it']} rank-5 entries (FORBIDDEN)")
            if rec["load_terms"]:
                why.append(f"{rec['load_terms']} load-driven entries (no factor from a first-order node field: not "
                           f"(A)-class, THEOREM O row A / AGREE_COSMIC C5)")
            if rec["second_order_types"]:
                why.append(f"{rec['second_order_types']} second-order gear types in the namespace")
            rec["verdict"] = "CAN read Theta" if not why else "cannot read Theta: " + "; ".join(why)
        (readers if rec["verdict"] == "CAN read Theta" else non_readers).append(ns)
    return {"theta0": theta0, "D": D, "per_namespace": per, "readers": readers, "non_readers": non_readers,
            "first_order_gear_types": len(first), "cross_reads": cross,
            "block_diagonal": cross["cosmic_reads_package"] == 0 and cross["package_reads_cosmic"] == 0}


# ======================================================================== the ONE composer
def one_system(Q: int = Q_DEFAULT, *, fix_i: bool = True, cosmic: bool = True, route_b=False, families: int = 1,
               theta0: int | None = None, h: int | None = None, k_theta: int = K_THETA_DEFAULT,
               g_w: int = G_W_DEFAULT, c_pair: int | None = None, couple_doublet: bool = False,
               package_kw: dict | None = None) -> System:
    """THE composed ONE system (module docstring). fix_i=False rebuilds the earlier L2(b) gwb (contrast only: it runs
    away, s18/AGREE_STAB). route_b: False (default), True (layers/electroweak_b.compose_electroweak_b on the hands-OFF
    base; ONE v2) or a callable base -> System. families: 1 only (ONE v3 hook). cosmic=False: the package alone.
    couple_doublet: False (DEFAULT) gives ONE v1 (block-diagonal, dynamics fingerprint 77f6d251...). True is OPT-IN ONLY
    (COUPLING_STATUS: NEW LAW candidate, REJECTED by the owner; runaway measured in Study 30; kept for the record) and
    builds Study 22's C1 bit-identically (593753fa...): the doublet blocks matter, matter2, chiral (matter entries only)
    and gwb are Theta-scaled (theta_scale_block) with theta0 = COUPLED_THETA0 = 64 (today's mass) unless given; E1 is not
    scaled. The coupling is not designed for route B (explicit couple_doublet=True with route_b raises). theta0 None -> 64 when coupled, else
    THETA0_DEFAULT; h None -> (D // 24) // theta0. Option C2: theta0=256 with package_kw={"mass": 4916 << 22} (a mass change
    the owner has NOT approved)."""
    if families != 1:
        raise NotImplementedError("ONE v3 (three families / Pauli copies / configuration space): NEW LAWs not approved")
    if couple_doublet and route_b:
        raise NotImplementedError("the Theta coupling is designed for route A only (ONE v2 with route B: not designed)")
    if theta0 is None:
        theta0 = COUPLED_THETA0 if couple_doublet else THETA0_DEFAULT
    if h is None:
        h = ((6 * Q) // 24) // theta0
    kw = dict(package_kw or {})
    if route_b:
        base = default_system(Q, **dict(kw, chiral=False, electroweak=False))
        if callable(route_b):
            S = route_b(base)
        else:
            try:
                from .electroweak_b import compose_electroweak_b
            except ImportError as exc:      # construction-time only; the law has no branch
                raise NotImplementedError("ONE v2 (route B) needs layers/electroweak_b.py (EW-BUILDER)") from exc
            S = compose_electroweak_b(base, on=True)
        ew = "route B (EW-BUILDER)"
    elif fix_i:
        S = default_system(Q, **kw)
        ew = "hands ON + FIX-i (lam_H = lam_L = 0, singlet-half hop kept)"
    else:
        from .electroweak import compose_electroweak
        S = compose_electroweak(default_system(Q, **dict(kw, chiral=False, electroweak=False)), on=True,
                                gwb_lam_H=None, gwb_lam_L=4)
        ew = "hands ON + earlier L2(b) gwb (lam_H = lam_L = 4): CONTRAST ONLY (runs away, s18)"
    names = [b.name for b in S.blocks]
    if fix_i and not route_b and "gwb" in names:
        gp = S.by_name("gwb").params
        if (gp["lam_H"], gp["lam_L"]) != (0, 0):
            raise ValueError("FIX-i expected in the package default (owner decision v8-1)")
    blocks = list(S.blocks)
    info = dict(S.info)
    one = {"version": ONE_VERSION, "electroweak": ew, "fix_i": bool(fix_i and not route_b), "route_b": bool(route_b),
           "families": families, "grav_fix_A": info.get("beta_note"), "cosmic": bool(cosmic),
           "new_laws": NEW_LAWS, "excluded": EXCLUDED,
           "owner_rule": ("only the fixed tensor + the seed + Rule3: no forcing, no faking, no hand-placed schedules, "
                          "no f(t), no posted holds, no run-time intervention, no comparison/if in the law "
                          "(manager 14:47 UTC)")}
    if cosmic:
        if COSMIC_NS in names:
            raise ValueError("namespace 'cosmic' is taken")
        blk = build_cosmic(Q, theta0=theta0, h=h, k_theta=k_theta, g_w=g_w, c_pair=c_pair)
        if couple_doublet:
            blocks = [theta_scale_block(b, theta0, select=(None if b.name != "chiral" else _is_doublet_term))
                      if b.name in DOUBLET_BLOCKS else b for b in blocks]
            one["coupling"] = ("COUPLED (opt-in couple_doublet=True; " + COUPLING_STATUS + "): the doublet's first-order "
                               "potential carries the hand; E1 not scaled; the cosmic pairs are loaded by the cosmic matter only")
            one["couple_doublet"] = {"theta0": theta0, "blocks": DOUBLET_BLOCKS, "why": WHY_COUPLE, "status": COUPLING_STATUS}
        blocks.append(blk)
        one["cosmic_params"] = blk.params
        one["theta_readers"] = "the cosmic matter (M1, M2) only; no package sector (layers.one.theta_reading_census)"
        one.setdefault("coupling", "block-diagonal: the cosmic block reads no package gear and no package gear reads it")
    info["one"] = one
    return System(Q, tuple(blocks), info)


__all__ = ["theta_scale_block", "COUPLED_THETA0", "DOUBLET_BLOCKS", "WHY_COUPLE", "COUPLING_STATUS", "default_pair_c", "LOAD_HEADROOM", "COSMIC_NS", "COSMIC_GEARS", "THETA0_DEFAULT", "H_DEFAULT", "K_THETA_DEFAULT", "G_W_DEFAULT",
           "A_COSMIC_DEFAULT", "ONE_VERSION", "NEW_LAWS", "EXCLUDED", "WHY_WIND", "WHY_LTHETA", "WHY_PAIR",
           "cosmic_params", "build_cosmic", "theta_reading_census", "one_system"]
