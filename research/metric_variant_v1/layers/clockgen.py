"""CLOCKGEN (Study 34, builder CLK-A): an OPT-IN candidate GENERIC clock law -- the cosmic hand reaches matter ONLY through
TIME (the lapse), never by a matter gear reading the hand. NEW file; DEFAULT OFF (nothing in the package calls it);
no existing package file is modified. TENSOR BLOCKS ONLY (no detector, no if, no clock, no posted schedule).

    clockgen = ONE v1 (layers/one.one_system(couple_doublet=False): FIX-i package + WIND cosmic block, block-diagonal)
             + block "clockgen" (0 gear types of its own; cross-block terms only, like lapseL0):

  mode "drive" (CG1: the ADDITIVE CONTRAST; exact and felt, but it cannot bound the uniform lapse):
      u[metric.h00](x) += kappa * b[cosmic.Th](x)                    rank 2 (one factor), on-site (B3), 1 monomial/node
  mode "param" (CG2: THE OPT-IN CANDIDATE, valid only inside CLOCK_VALIDITY; the composer one_system_clock builds it):
      u[metric.h00](x) += kappa * b[cosmic.Th](x) * b[metric.h00](x)   rank 3 (two factors), on-site (B3), 1 monomial/node

  New monomials, declared: target metric.h00 (the lapse F, U = F/(2P)); kind = one-way (DESIGNATED) source of the
  lapse by the hand (CG1: a source; CG2: a parametric stiffness); integer coefficient kappa (CHOSEN, declared before any
  run: kappa = 1, the unit weight, the same weight with which the declared background gear bgk.B already enters the lapse: u[h00] += -1 * b[bgk.B]).
  One-way justification (written): a reciprocal coupling Phi = kappa Theta F would put the additive source kappa F
  (mode drive) or kappa F^2/2 (mode param) into the hand's input; THEOREM O row Theta (s15 AGREE_COSMIC; s24
  THE_ALGEBRA 9.4) forbids any additive (even-in-Theta) source on the hand, so the hand may not feel the lapse back.
  This is the same reason as the 30 existing WIND designations (WHY_WIND / WHY_LTHETA).

  What is generic about it: ONE term per node, acting on ONE gear (the lapse) that every lapse-reading clock already
  reads with the SAME exact EP factor (form C: 1 - 2U on mass entries, 1 - 4U on transport entries; first-order
  clocks half of each, s24 THE_ALGEBRA 5.0-5.2). No matter gear (L0, Dirac pairs, Higgs, gauge links, E1, ...)
  reads the hand: theta_reader_census() checks it on the composed tensor.

  What it can NOT do (s34 CLK-A_NOTES, THEOREM rows): (i) a lapse-mediated turn never FOLDS any sector (the lapse
  factors are positive for U < 1/4 and are not one common factor on mass and transport entries); (ii) the k = 0
  identity D Sum[F(t+1) - 2F(t) + F(t-1)] = 2 Sum s + Sum (r - r') is linear in the source, so a zero-mean hand
  drive adds a bounded swing and does not remove the t^2 drift driven by the package's own net source.

STATUS (manager decision 17:15 UTC, Study 34): ONE v1 STAYS THE DEFAULT. CG2 at Theta0 = 2^21 is THE explicit OPT-IN NEW
  LAW candidate, DEFAULT OFF: one_system_clock(law="CG2"); CG1 is the additive contrast. Theta0 = 2^21 is CHOSEN
  (window-fitted, owner-approved 17:00 UTC), NOT forced; h = 2^10 is FORCED (band rule); kappa = 1 is CHOSEN (declared
  before the runs).
VALIDITY WINDOW (CLOCK_VALIDITY; DERIVED + NUMERIC): the k = 0 lapse under CG2 is a Mathieu oscillator at a = 0 with
  q_M = 4 kappa Theta0 / (D W^2); it is HELD (Kapitza) only for q_M < 0.908 and PUMPED (runaway) above. The hand's
  frequency obeys W^2 ~ g_w A_c^2 / (D N), so q_M ~ Theta0 N / (g_w A_c^2): EACH Theta0 HAS A MAXIMUM SAFE BOARD SIZE.
  At Theta0 = 2^21, g_w = 1310, kappa = 1: valid for L <= 6 with A_c >= ~0.82 x 2^10 (q_M = 0.18 at L = 4, 0.59-0.61 at
  L = 6). It FAILS at L = 8 (q_M = 1.43: CLK-B's board run K8w pumps the uniform lapse, alternating extrema growing
  x5.86 and x7.07 per hand period of ~588 updates) and at L = 7 (q_M = 0.96, toy Floquet e^0.68 per period). At today's
  Theta0 = 2^24 it fails already at L = 4 and L = 6 (q_M = 1.44, 4.74: runaway, Study 34 RC). Safe scale for kappa = 1,
  A_c = 2^10, g_w = 1310: Theta0_max(L) ~ 3.2e6 x 216/L^3 (2^23 at L = 4, 2^21 at L = 6, 2^20 at L = 7-8, 2^19 at L = 9-10,
  2^18 at L = 12), and the holdable mean source (ceiling ~ w_eff^2 P/4, w_eff^2 ~ W^2 ~ 1/N) falls like 1/N. An L0 lump is
  NOT held (Study 34 RL6w: blow-up delayed 272 -> 328 at L = 6). clock_window(L, ...) is the design arithmetic.
"""
from __future__ import annotations

from ..core.tensor import Block
from .one import COSMIC_NS, one_system
from .system import Q_DEFAULT, System

ZERO = (0, 0, 0)
CLOCKGEN_NS = "clockgen"
HAND = f"{COSMIC_NS}.Th"
LAPSE = "metric.h00"
KAPPA_DEFAULT = 1                    # CHOSEN (declared 16:3x UTC before any run): the unit weight (as bgk's -1)
MODES = ("drive", "param")
WHY_CLOCK_DRIVE = ("ADDITIVE CONTRAST (Study 34 CG1, CLK-A; default OFF): the cosmic hand is a one-way source of the "
                   "lapse, u[h00] += kappa Theta; the hand does not feel the lapse (THEOREM O row Theta: no additive "
                   "source on the hand); every lapse READER feels each turn, no matter gear reads Theta; it cannot "
                   "bound the uniform lapse")
WHY_CLOCK_PARAM = ("OPT-IN CANDIDATE NEW LAW (Study 34 CG2, CLK-A; default OFF; valid only inside CLOCK_VALIDITY): "
                   "the hand modulates the lapse's own stiffness, u[h00] += kappa Theta F (parametric); the hand "
                   "does not feel F^2/2 (THEOREM O row Theta: no additive source on the hand)")


def build_clockgen(Q: int = Q_DEFAULT, *, kappa: int = KAPPA_DEFAULT, mode: str = "drive",
                   hand: str = HAND, lapse: str = LAPSE, name: str = CLOCKGEN_NS) -> Block:
    """The clock-law block: 0 gear types, ONE designated term targeting the lapse (see the module docstring)."""
    if type(kappa) is not int or kappa == 0:
        raise ValueError("kappa must be a nonzero Python int (integer coefficient)")
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    if mode == "drive":
        terms = ((lapse, kappa, ((hand, ZERO, "b"),), {"designated_one_way": WHY_CLOCK_DRIVE}),)
        law = "u[h00] += kappa * Theta (rank 2, on-site, one-way)"
    else:
        terms = ((lapse, kappa, ((hand, ZERO, "b"), (lapse, ZERO, "b")), {"designated_one_way": WHY_CLOCK_PARAM}),)
        law = "u[h00] += kappa * Theta * F (rank 3, on-site, one-way)"
    return Block((), terms, name=name, vacuum={},
                 params={"Q": Q, "kappa": kappa, "mode": mode, "hand": hand, "lapse": lapse, "law": law},
                 doc="Study 34 clock law (CLK-A): the hand acts on the lapse only; default OFF", Q=Q)


def clockgen_system(Q: int = Q_DEFAULT, *, kappa: int = KAPPA_DEFAULT, mode: str = "drive",
                    one_kw: dict | None = None) -> System:
    """ONE v1 (couple_doublet=False) + the clock-law block, appended LAST (0 gear types: the gear list, the vacuum
    and every seed of ONE v1 are unchanged, so v1 and clockgen runs start from the SAME state arrays)."""
    kw = dict(one_kw or {})
    if kw.get("couple_doublet"):
        raise ValueError("clockgen replaces the coupled doublet: the doublet must NOT read Theta (owner rule)")
    kw["couple_doublet"] = False
    S = one_system(Q, **kw)
    blk = build_clockgen(Q, kappa=kappa, mode=mode)
    info = dict(S.info)
    one = dict(info["one"])
    one["clockgen"] = {"kappa": kappa, "mode": mode, "law": blk.params["law"],
                       "why": WHY_CLOCK_DRIVE if mode == "drive" else WHY_CLOCK_PARAM, "default": "OFF"}
    one["coupling"] = ("ONE v1 + clockgen: the hand acts on the lapse only (one-way); no package gear reads Theta; the "
                       "package reads the lapse as before")
    info["one"] = one
    return System(Q, tuple(S.blocks) + (blk,), info)


# ======================================================================== the clock composer (owner 17:00 UTC)
THETA0_LOG2_CLOCK = 21           # CHOSEN (window-fitted, owner-approved 17:00 UTC), NOT forced: hand scale 2^24 -> 2^21 so
                                 # that CG2 sits in its Mathieu window at L = 6 (q_M = 4 kappa Theta0/(D W^2) = 0.59 <
                                 # 0.908, W = 2 pi/379); the safe Theta0 scales as ~1/L^3 (CLOCK_VALIDITY, clock_window)
CLOCK_LAWS = ("CG2", "CG1", "off")
CLOCK_CHANGED_CONSTANTS = {
    "theta0": "2^24 -> 2^21: CHOSEN (window-fitted, owner-approved 17:00 UTC), NOT forced: it puts CG2's k = 0 Mathieu "
              "parameter inside the window at L = 6 (integer grain kappa >= 1 at 2^24 gives q_M = 4.74 at L = 6: parametric "
              "runaway, Study 34 A10); the safe Theta0 scales as ~1/L^3",
    "kappa": "1: CHOSEN (declared before any run; the unit weight)",
    "h": "2^7 -> 2^10: FORCED by CC-A's band rule 24 h Theta0 = D - 6 (one_system computes h = (D // 24) // Theta0): the "
         "readers' link-averaged hop h Theta0 is unchanged, so the cosmic matter's band is unchanged",
    "k_theta, g_w, c_pair, load_sum, A_c, Q, P": "UNCHANGED (none depends on Theta0)",
    "new monomial": "u[metric.h00] += 1 * b[cosmic.Th] * b[metric.h00] per node (CG2, rank 3, designated one-way)",
}


def one_system_clock(Q: int = Q_DEFAULT, *, law: str = "CG2", theta0_log2: int = THETA0_LOG2_CLOCK, kappa: int = 1,
                     one_kw: dict | None = None) -> System:
    """THE clock composer (Study 34): an OPT-IN NEW LAW candidate, DEFAULT OFF (nothing in the package calls it; ONE v1
    stays the default, manager 17:15 UTC); law "CG2" is THE candidate, law "CG1" the additive contrast. Theta0 = 2^21 is
    CHOSEN (window-fitted, owner-approved 17:00 UTC), not forced; h = 2^10 is FORCED by the band rule; kappa = 1 is CHOSEN.
    VALID ONLY inside CLOCK_VALIDITY (L <= 6, A_c >= 840, Theta0 = 2^21; the safe Theta0 scales as ~1/L^3): outside
    it the uniform lapse is PUMPED (L = 8 runs away). law = "CG2": ONE v1's package + cosmic block with the hand re-scaled to 2^theta0_log2
    (h re-derived by one_system's own band rule) + the CG2 monomial u[h00] += kappa Theta F. law = "CG1": the same hand
    scale + the additive term u[h00] += kappa Theta (contrast). law = "off": EXACTLY one_system(couple_doublet=False)
    (ONE v1 at its own constants; fingerprint 77f6d251...), i.e. OFF == v1. No matter gear reads Theta in any law."""
    if law not in CLOCK_LAWS:
        raise ValueError(f"law must be one of {CLOCK_LAWS}")
    kw = dict(one_kw or {})
    if law == "off":
        if kw.get("couple_doublet"):
            raise ValueError("the clock composer never couples the doublet to Theta (owner rule)")
        kw["couple_doublet"] = False
        return one_system(Q, **kw)
    if type(theta0_log2) is not int or not 1 <= theta0_log2 <= 24:
        raise ValueError("theta0_log2 must be an int in [1, 24]")
    kw["theta0"] = 1 << theta0_log2
    S = clockgen_system(Q, kappa=kappa, mode={"CG2": "param", "CG1": "drive"}[law], one_kw=kw)
    info = dict(S.info)
    one = dict(info["one"])
    one["clock_composer"] = {"law": law, "theta0_log2": theta0_log2, "kappa": kappa,
                             "changed_constants": CLOCK_CHANGED_CONSTANTS, "default": "OFF (package default unchanged)"}
    info["one"] = one
    return System(S.Q, S.blocks, info)


CLOCK_VALIDITY = {
    "status": "OPT-IN NEW LAW candidate, DEFAULT OFF; ONE v1 stays the default (manager 17:15 UTC, Study 34)",
    "theta0": 1 << THETA0_LOG2_CLOCK,   # CHOSEN (window-fitted, owner-approved 17:00 UTC), not forced
    "theta0_label": "CHOSEN (window-fitted, owner-approved 17:00 UTC), NOT forced; safe Theta0 ~ 1/L^3",
    "L_max": 6,
    "A_c_min": 840,               # ~0.82 x 2^10: q_M ~ 1/A_c^2 and q_M(L = 6, A_c = 2^10) ~ 0.61 < 0.908
    "q_star": 0.908,              # first stability zone of Mathieu at a = 0
    "rule": "q_M = 4 kappa Theta0/(D W^2) < 0.908 with W^2 ~ g_w A_c^2/(D N): each Theta0 has a maximum safe L",
    "fails": {"L = 8 at 2^21": "pumped (CLK-B K8w: extrema x5.86, x7.07 per ~588-update hand period)",
              "L = 7 at 2^21": "q_M = 0.96 (toy Floquet e^0.68 per period)",
              "2^24 at L = 4, 6": "q_M = 1.44, 4.74: runaway (Study 34 RC)",
              "L0 lump": "not held (Study 34 RL6w: blow-up 272 -> 328 at L = 6)"},
}


def clock_window(L: int, theta0: int = 1 << THETA0_LOG2_CLOCK, kappa: int = 1, Q: int = Q_DEFAULT,
                 A_c: int = 1 << 10, g_w: int = 1310, W6: float = 0.01658) -> dict:
    """DESIGN CHECK (read-only arithmetic, not the law): the k = 0 Mathieu parameter q_M = 4 kappa Theta0/(D W^2) of CG2
    for the WIND hand, whose frequency scales as W^2 ~ g_w A_c^2/(D N): W = W6 sqrt((216/L^3) (A_c/2^10)^2 (g_w/1310)),
    W6 = 0.01658 measured at L = 6 (Study 34 F1; L = 4: 0.0301; L = 8: period ~588, s30 R3b). in_window iff q_M < 0.908
    AND L <= the validated L_max (6); theta0_max is the largest Theta0 with q_M < 0.908 at this L, A_c, g_w."""
    D = 6 * Q
    W = W6 * ((216.0 / L ** 3) * (A_c / 1024.0) ** 2 * (g_w / 1310.0)) ** 0.5
    qM = 4.0 * kappa * theta0 / (D * W * W)
    return {"L": L, "A_c": A_c, "g_w": g_w, "W": W, "q_M": qM, "in_window": qM < 0.908,
            "validated": qM < 0.908 and L <= CLOCK_VALIDITY["L_max"] and theta0 == CLOCK_VALIDITY["theta0"],
            "theta0_max": 0.908 * D * W * W / (4.0 * kappa), "kapitza_w_eff": W * qM / (2 * 2 ** 0.5)}


# ======================================================================== static censuses (exact, read-only)
def _ns(name: str) -> str:
    return name.split(".", 1)[0]


def theta_reader_census(tensor, hand: str = HAND) -> dict:
    """Every gear (and namespace) whose input contains the hand as a factor. The owner rule (Study 34) holds iff no
    package MATTER gear is among them; the allowed set is the hand itself (face terms), the cosmic block's own
    reader gears M1/M2 (CC-A's species, see G5) and the lapse (the universal clock)."""
    names = tensor.names
    th = tensor.gear_index(hand)
    by_target: dict[str, int] = {}
    for m in tensor.monomials:
        if any(f.gear == th for f in m.factors):
            by_target[names[m.target]] = by_target.get(names[m.target], 0) + 1
    allowed = {hand, f"{COSMIC_NS}.M1", f"{COSMIC_NS}.M2", LAPSE}
    bad = {k: v for k, v in by_target.items() if k not in allowed}
    return {"readers_of_theta": by_target, "outside_allowed": bad, "no_matter_reads_theta": not bad,
            "allowed": sorted(allowed)}


def lapse_reader_census(tensor, lapse: str = LAPSE) -> dict:
    """Which namespaces read the lapse (= which clocks can feel a cosmic turn through time), with monomial counts,
    split by degree and designation. Read-only."""
    names = tensor.names
    F = tensor.gear_index(lapse)
    desig = set(tensor.designations.keys()) if hasattr(tensor, "designations") else set()
    out: dict[str, dict] = {}
    for m in tensor.monomials:
        if m.target == F:
            continue
        if any(f.gear == F for f in m.factors):
            rec = out.setdefault(_ns(names[m.target]), {"monomials": 0, "by_degree": {}, "designated": 0,
                                                        "target_gears": set()})
            rec["monomials"] += 1
            rec["by_degree"][m.degree] = rec["by_degree"].get(m.degree, 0) + 1
            rec["designated"] += int((m.target, m.factors) in desig)
            rec["target_gears"].add(names[m.target])
    for rec in out.values():
        rec["target_gear_count"] = len(rec.pop("target_gears"))
    return out


def lapse_source_census(tensor, lapse: str = LAPSE) -> dict:
    """Which namespaces SOURCE the lapse (monomials targeting the lapse, by the namespace of their factors)."""
    names = tensor.names
    F = tensor.gear_index(lapse)
    out: dict[str, int] = {}
    for m in tensor.monomials:
        if m.target != F:
            continue
        nss = sorted({_ns(names[f.gear]) for f in m.factors})
        key = "+".join(nss)
        out[key] = out.get(key, 0) + 1
    return out


__all__ = ["CLOCKGEN_NS", "HAND", "LAPSE", "KAPPA_DEFAULT", "MODES", "WHY_CLOCK_DRIVE", "WHY_CLOCK_PARAM",
           "build_clockgen", "clockgen_system", "theta_reader_census", "lapse_reader_census", "lapse_source_census",
           "THETA0_LOG2_CLOCK", "CLOCK_LAWS", "CLOCK_CHANGED_CONSTANTS", "CLOCK_VALIDITY", "one_system_clock",
           "clock_window"]
