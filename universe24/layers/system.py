"""INTEGRATOR (stage 3): the composed DEFAULT SYSTEM at ONE odd Q. TENSOR BLOCKS ONLY.

Every block is built by its own layer's builder, imported READ-ONLY. This module only chooses parameters and composes;
the one exception is a DATA-level copy of a block with different VACUUM remainders (Block.vacuum is initial data).

v2 DEFAULT (OWNER decisions 1, 2, 3, 4-as-prediction, 6, 7, 8; manager 11:1x-11:2x; pre-registered in NOTES_system.md
"PRE-REGISTRATION v2 DEFAULT"):
  Q        2^33 + 1 (D = 6Q); P = 2^20, k = (Q-1)/(2P) = 2^12
  (1)      l0_offset = Q - 1: ONE vacuum (0, 0, 3Q - 1) for every gear; uniform R' is THE mirror (odd Q). The q-lattice
           rule is retired (the validator is kept for literal time_reverse compositions and the legacy offset 0).
  (2)      body_signs = (1, -1, 1), the HANDED class: the linear L0 operator has a gap and Kramers structure.
           Its proposed dark-sector interpretation is not a physical identification. L0 clicks are AUDIT-ONLY
           by a passive convention (observe/readout.py). Alternative body signs: (1, 1, 1).
  (3)      l0_lapse = "W" = FORM C (layers/gravity_l0c.py): L0 in the port-difference form at the ONE headroom weight
           Q - 1 (+ on-site 6), clock factor (1 - 2U) on M0 = 6 - Sum W_d, link factor (1 - 4U) on the difference
           transport; reciprocal (L0 sources the wave lapse). Options: None, "R" (B1-GRAV rounded), "W_split"
           (B1-GRAV's site/hop split at weight Q - 1; contrast).
  (4)      em = "e1d": E1 sourced by the lapse/beta-DRESSED link current (layers/em_dressed.py); its lattice-scale
           departure from exact action = reaction is a PREDICTION (exact in symmetric preparations, reciprocal in the
           continuum; two verified no-go theorems). Variants "e1" (undressed), "compact".
  (5)      CLOSED (OWNER 13:09, "hands ON"): chiral=True and electroweak=True by DEFAULT (layers/chiral.py, HAND-M1;
           layers/electroweak.py, EW-BUILDER). EW removes "matter"'s mlapse/mbeta. The default FIX-i sets the Higgs
           and weak-link lapse coefficients to zero, retaining the singlet-half hop; universal rest-clock response
           is not established. Earlier nonzero coefficients are an optional contrast, not the current default.
           Both can be switched off: chiral=False, electroweak=False (electroweak alone raises).
  (6)      odd-Q one-shot routers (B1-CHOICE): router + gated exit pair; (7) no F7 (taxicab choice: mechanism test).
  (8)      gravity: lapse = "wave" (metric + reciprocal lapse + beta) + the R-a background gear "bgk" + the k = 0
           offset (initial data); OD2 = variant (its one-way lapse read has no exact time mirror: C8).
  GRAV-FIX beta_form = "detuned" (candidate A, manager 12:58; layers/gravity_beta_fix.py, B1-GRAV): w_G = (Q-1)/2 and
           source -(k/2) Lap(F^2) remove the beta-corner 1:1 resonance; "marginal" = contrast.
  R1       before EW composition, matter lapse = "C" (layers/matter_lapse_c.py, reciprocal): a clock factor on the mass term
           m W0 only; hops + the Wilson term in the DIFFERENCE form take the link factor; the beta = 1 read in the same
           split. B1-GRAV's site/hop split (rest clock 1 - 0.6875 U: a 31 % EP violation) = contrast "split".
  matter   B1-EM 16-channel Dirac pair WITH Wilson: hop 2^31, wilson 2^30, mass 4915 * 2^22 (the multiple of 2^22
           nearest 2.4 Q: cos w0 = mass/D = 0.39998, rotation number 0.18451, far from low-order rationals; R-P1/R-P2:
           a rational rest frequency, e.g. 3Q or 3 * 2^29 at 2^29 + 1, rounding-LOCKS weak potential shifts);
           mass + 12 wilson <= D (B1-EM's stability bound).
  E1       g_phi = 4, g_A = 1, sigma = 2^24 (dressing coefficients sigma ws/(2P) = 8 and 9 sigma ws/(16P) = 9).
  weak-field rule (R-P1/R-P2): matter amplitude x field >= D/(8 g_phi) in demos and seeds (info["weak_field_min"]).
  gauge    B1-GAUGE default family at this Q (default_regime: A = kappa = 2^16; c2 of links.py OFF, c1 not adopted)
  c2       option c2=True: ZQ8 base links with one OD4 spring per simple component (layers/c2_zq8.py), fine links
           (A = 2^14, kappa = 2^19 on the form-C L0), lam = 4; ON in the handed default only if RUN Z is bounded.
"""
from __future__ import annotations

import hashlib
from fractions import Fraction
from dataclasses import dataclass, field
from pathlib import Path

from ..core.tensor import Block

Q_DEFAULT = (1 << 33) + 1
P_GRAV, K_GRAV = 1 << 20, 1 << 12
HOP, WILSON = 1 << 31, 1 << 30
MASS_DEFAULT = 4915 << 22          # nearest multiple of 2^22 to 2.4 Q: cos w0 = 0.39998 (irrational-type rest clock)
MASS_PROPOSED = MASS_DEFAULT       # (old name kept for importers)
E1_PARAMS = {"g_phi": 4, "g_A": 1, "sigma": 1 << 24}
BODY_SIGNS_DEFAULT = (1, -1, 1)    # OWNER decision 2: the handed class
C2_PARAMS = {"A": 1 << 14, "lam": 2}   # c2 ZQ8 fine links on the form-C L0 (kappa = (Q - 1)/A); T2 (C2-TUNE final:
                                       # lam = 4 sat on a 1:2 parametric resonance of the spring)
C2_DEFAULT = False                 # RUN Z: lam = 4 ran away on the form-C L0 (a 1:2 spring resonance, C2-TUNE); T2
                                   # (lam = 2) is exact and bounded on the handed class WITHOUT gravity; with gravity
                                   # it shortens the horizon (~1825 vs 2843-3688): OFF; re-test after GRAV-FIX A
RA_WHY = ("R-a: the declared uniform k = 0 background (-kappa E/N per node, Study 6 D(d)) as a prescribed static gear "
          "B feeding -b_B into the lapse field; B holds its value and does not feel F (data, one-way)")
E1D_SIGMA = E1_PARAMS["sigma"]    # lapse-dressed E1 (C5 fix): integer dressing for sigma in 16P Z / ws
LAYER_FILES = ("layers/reference.py", "layers/gauge.py", "layers/matter.py", "layers/em.py", "layers/em_compact.py",
               "layers/gravity.py", "layers/choice.py", "layers/choice_oddq.py", "layers/em_dressed.py",
               "layers/gravity_l0.py", "layers/gravity_l0c.py", "layers/c2_zq8.py", "layers/links.py",
               "layers/matter_lapse_c.py", "layers/gravity_select.py",
               "core/tensor.py", "core/engine.py", "core/reversors.py")
ROOT = Path(__file__).resolve().parent.parent


@dataclass
class System:
    """The blocks (in composition order) and the integration record (parameters, conflicts, matter spec)."""
    Q: int
    blocks: tuple
    info: dict = field(default_factory=dict)

    def by_name(self, name: str) -> Block:
        for b in self.blocks:
            if b.name == name:
                return b
        raise KeyError(name)


def with_vacuum(block: Block, value: int, params_extra: dict | None = None) -> Block:
    """DATA-level copy of a block with every vacuum remainder set to ``value`` (dynamics unchanged)."""
    return Block(block.gears, block.terms, name=block.name, vacuum={k: value for k in block.vacuum},
                 params={**block.params, **(params_extra or {})}, doc=block.doc, Q=block.Q)


def file_hashes() -> dict:
    out = {}
    for rel in LAYER_FILES:
        p = ROOT / rel
        out[rel] = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    return out


def default_system(Q: int = Q_DEFAULT, *, l0_offset: int | None = None, body_signs=BODY_SIGNS_DEFAULT,
                   em: str | None = "e1d", gauge: bool = True, gravity: bool = True, lapse: str = "wave",
                   background: bool = True, beta: bool = True, l0_lapse: str | None = "W", choice: bool = True,
                   mass: int | None = None, P: int = P_GRAV, c2: bool | None = None,
                   matter_lapse: str = "C", chiral: bool = True, electroweak: bool = True,
                   beta_form: str = "detuned") -> System:
    """Compose the v2 default system (see the module docstring). Every parameter is recorded in System.info.
    l0_offset None -> Q - 1 (OWNER decision 1); c2 None -> C2_DEFAULT; matter_lapse "C" (R1: Wilson in difference form,
    layers/matter_lapse_c.py) or "split" (B1-GRAV's site/hop split; contrast)."""
    from .reference import build_reference
    if type(Q) is not int or Q < 3 or Q % 2 == 0:
        raise ValueError("ONE ODD Q is required (the joint vacuum 3Q - 1 is R'-fixed only for odd Q)")
    l0_offset = Q - 1 if l0_offset is None else l0_offset
    if l0_offset not in (0, Q - 1):
        raise ValueError("l0_offset must be 0 (legacy vacuum 2Q, rhoL0) or Q - 1 (vacuum 3Q - 1, R' everywhere)")
    mass = MASS_DEFAULT if mass is None else mass
    c2 = C2_DEFAULT if c2 is None else c2
    if type(P) is not int or P < 1 or (Q - 1) % (2 * P):
        raise ValueError("P must divide (Q - 1)/2 (gravity: Q - 1 = 2Pk)")
    K = (Q - 1) // (2 * P)
    sigma = E1_PARAMS["sigma"]
    body_signs = tuple(body_signs)
    handed = body_signs != (1, 1, 1)
    lapse_field = {"od2": "od2.h00", "wave": "metric.h00"}[lapse]
    D = 6 * Q
    info = {"Q": Q, "D": D, "l0_offset": l0_offset, "body_signs": body_signs, "em": em, "gauge": gauge,
            "gravity": gravity, "lapse": lapse, "lapse_field": lapse_field, "background": background, "beta": beta,
            "l0_lapse": l0_lapse, "choice": choice, "P": P, "k": K, "sigma": sigma, "sigma_dressed": sigma, "c2": c2,
            "matter_lapse": matter_lapse,
            "matter": {"hop": HOP, "wilson": WILSON, "mass": mass, "species": "pair",
                       "cos_w0": str(Fraction(mass, D)), "cos_w0_float": mass / D,
                       "stability_mass_plus_12_wilson_le_D": mass + 12 * WILSON <= D},
            "weak_field_min": {"rule": "matter amplitude x field >= D/(8 g_phi) (R-P1/R-P2 rounding lock)",
                               "value": D // (8 * E1_PARAMS["g_phi"])},
            "mirror": {"declared": ("R' (Mp: (b, a, R'(r))) on EVERY gear, vacuum (0, 0, 3Q - 1)" if l0_offset else
                                    "rhoL0 on ref (legacy offset 0), R' elsewhere"),
                       "matter": "Kramers K o M' (X F X F = Jp on matter)",
                       "em": ("E1 (prepare.em.x_reversor_core, the implemented joint mirror): M' on A_d "
                              "(a, b, r) -> (b, a, R'(r)); Phi (a, b, r) -> (-Phi_next, -b, r) (staggered); the matter "
                              "K o M'. (R* of the seed uses (-b, -a, r) on A_d together with the spatial inversion; "
                              "that map is not a time mirror on its own)"),
                       "od2_variant": ("hij: M' (NOT M; DEV-GR4); h0i (a, b) -> (-h0i_next, -b); h00 (a, b) -> "
                                       "(h00(t+2), h00(t+1)); the one-way OD2 lapse read breaks it (C8)")},
            "readout": {"L0": ("AUDIT-ONLY (dark sector; passive OD1-type label, not a law)" if handed
                               else "official")},
            "owner_decisions": "all approved 13:09 (decision 5 CLOSED: hands ON = chiral + electroweak by default)",
            "chiral": chiral, "electroweak": electroweak, "beta_form": beta_form,
            "conflicts": [], "file_hashes": file_hashes()}
    blocks = []
    l0_label = "audit" if handed else "official"
    if l0_lapse == "W":
        from .gravity_l0c import build_l0c
        if l0_offset != Q - 1:
            raise ValueError("form C needs l0_offset = Q - 1 (fine couplings into L0; R' everywhere)")
        ref = build_l0c(Q=Q, body_signs=body_signs, name="ref", label=l0_label)
    elif l0_lapse == "W_split":
        from .gravity_l0 import build_l0_weight
        ref = build_l0_weight(Q=Q, body_signs=body_signs, name="ref")
    else:
        ref = build_reference(Q=Q, body_signs=body_signs, label=l0_label)
        if l0_offset:
            ref = with_vacuum(ref, 2 * Q + l0_offset, {"l0_offset": l0_offset})
    blocks.append(ref)
    # ---------------------------------------------------------------- gauge (B1-GAUGE defaults; links.py c2 OFF)
    if gauge:
        from .gauge import build_default, default_regime
        reg = default_regime(Q)
        info["gauge_regime"] = reg
        for g in ("su2", "su3", "u1"):
            blocks.append(build_default(g, Q=Q))
    # ---------------------------------------------------------------- c2 ZQ8 base links (RUN Z)
    if c2:
        from .c2_zq8 import build_c2_zq8
        if l0_offset != Q - 1:
            raise ValueError("c2 fine links need l0_offset = Q - 1")
        if l0_lapse == "W":
            wp, A2 = Q - 1, C2_PARAMS["A"]
        elif l0_lapse is None:
            wp, A2 = Q, 20857 if Q == Q_DEFAULT else None
            if A2 is None:
                raise ValueError("c2 on today's L0 weight Q needs A | Q (set for Q = 2^33 + 1 only)")
        else:
            raise ValueError("c2 is built for l0_lapse 'W' (form C) or None")
        blocks.append(build_c2_zq8(Q=Q, kappa=wp // A2, lam=C2_PARAMS["lam"], body_signs=body_signs,
                                   port_weight=wp, name="c2"))
        info["c2_params"] = {"A": A2, "kappa": wp // A2, "lam": C2_PARAMS["lam"], "port_weight": wp,
                             "note": ("late ~2e4-update rounding-heating limit common to both sign classes (Study 7); "
                                      "remedy: scale the spring or A with the run length")}
    # ---------------------------------------------------------------- matter + EM (B1-EM)
    matter = None
    if em is not None or gravity:
        from .matter import build_matter
        if em == "compact":
            from .em_compact import build_compact_coupling, build_u1_links
            from .gauge import default_regime
            reg = default_regime(Q)
            Ac = reg["A"]
            if HOP % Ac or WILSON % Ac:
                raise ValueError("compact: hop and wilson must be multiples of the regime's A")
            kd, kw = HOP // Ac, WILSON // Ac
            matter = build_matter(Q=Q, hop=HOP, mass=mass, wilson=WILSON, species="pair", name="matter")
            links = build_u1_links(Q=Q, A=Ac, lam=4, kappa_P=256, c_P=0, beta=reg["beta"], name="emu1")
            coupling = build_compact_coupling(Q=Q, matter=matter, links=links, kd=kd, kw=kw, name="cem")
            blocks += [matter, links, coupling]
            info["compact"] = {"A": Ac, "kd": kd, "kw": kw, "beta": reg["beta"]}
        else:
            matter = build_matter(Q=Q, hop=HOP, mass=mass, wilson=WILSON, species="pair", name="matter")
            blocks.append(matter)
            if em == "e1":
                from .em import build_em
                blocks.append(build_em(Q=Q, matter=matter, name="em", **E1_PARAMS))
            elif em == "e1d":
                if not (gravity and beta):
                    raise ValueError("em='e1d' (lapse-dressed source) needs gravity=True and beta=True")
                from .em_dressed import build_em_dressed
                emb = build_em_dressed(Q=Q, matter=matter, g_phi=E1_PARAMS["g_phi"], g_A=E1_PARAMS["g_A"],
                                       sigma=sigma, P=P, lapse=lapse_field, beta="beta.G", name="em")
                blocks.append(emb)
                hs, ws = emb.params["hs"], emb.params["ws"]
                info["e1d_dressing"] = {"hs": hs, "ws": ws, "lapse_coeff_ws": str(Fraction(sigma * ws, 2 * P)),
                                        "beta_coeff_ws": str(Fraction(9 * sigma * ws, 16 * P)),
                                        "lapse_coeff_hs": str(Fraction(sigma * hs, 2 * P)),
                                        "beta_coeff_hs": str(Fraction(9 * sigma * hs, 16 * P)),
                                        "status": "PREDICTION: lattice-scale departure from exact action = reaction"}
            elif em is not None:
                raise ValueError("em must be 'e1', 'e1d', 'compact' or None")
        if mass % (1 << 22):
            info["conflicts"].append(f"matter mass {mass} is not in 2^22 Z: gravity's first-order lapse rule fails")
        if mass + 12 * WILSON > D:
            info["conflicts"].append("mass + 12 wilson > D: B1-EM's stability bound fails")
    # ---------------------------------------------------------------- gravity (B1-GRAV: ONE lapse)
    if gravity:
        from . import gravity as gr
        from .gravity_select import gravity_blocks
        if Q - 1 != 2 * P * K:
            raise ValueError("gravity needs Q - 1 = 2Pk")
        spec = gr.spec_from_block(matter, Q=Q, order=1)
        info["matter_spec"] = {"name": spec.name, "order": spec.order, "n_site": len(spec.site),
                               "n_hops": len(spec.hops)}
        if matter_lapse == "split":
            blocks += gravity_blocks(Q=Q, P=P, k=K, matters=[spec], lapse=lapse, stress_spec=None, beta=beta)
        elif matter_lapse == "C":
            # R1 (manager 11:43): ONE clock factor on the mass term only; the Wilson term in the difference form takes
            # the link factor (layers/matter_lapse_c.py). B1-GRAV's metric / beta field blocks without a matter read.
            from .gravity_select import ONEWAY_LAPSE_WHY
            from .matter_lapse_c import build_matter_beta_read_c, build_matter_lapse_c
            blocks += gravity_blocks(Q=Q, P=P, k=K, matters=[], lapse=lapse, stress_spec=None, beta=beta)
            blocks.append(build_matter_lapse_c(Q=Q, P=P, field=lapse_field, matter=matter, oneway=(lapse == "od2"),
                                               name="mlapse", why=ONEWAY_LAPSE_WHY))
            if beta:
                blocks.append(build_matter_beta_read_c(Q=Q, P=P, G="beta.G", matter=matter, name="mbeta"))
            info["matter_lapse_form"] = ("C: clock factor (1 - U) on the mass term m W0 only; hops + Wilson difference "
                                         "(w/2)(b_x - b_y)^T W0 (b_x - b_y) take the link factor; beta read in the same "
                                         "split (R1)")
        else:
            raise ValueError("matter_lapse must be 'C' or 'split'")
        if beta and beta_form == "detuned" and matter_lapse == "C":
            # GRAV-FIX candidate A (B1-GRAV, manager 12:58): G detuned from the lapse field, w_G = (Q-1)/2, source
            # -(k/2) Lap(F^2): G's corner mode moves to w ~ pi/2 (no 1:1 resonance with F's marginal corner); the static
            # law G = F^2/(2P) (beta = 1) is unchanged
            from .gravity_beta_fix import build_beta_detuned, replace_beta
            blocks = list(replace_beta(tuple(blocks), build_beta_detuned(Q=Q, P=P, k=K, field=lapse_field, num=1, den=2)))
            info["beta_note"] = "GRAV-FIX A: beta detuned, w_G = (Q-1)/2, source -(k/2) Lap(F^2) (B1-GRAV)"
        elif beta and beta_form not in ("detuned", "marginal"):
            raise ValueError("beta_form must be 'detuned' or 'marginal'")
        elif beta:
            info["beta_note"] = ("marginal beta (B1-GRAV build_beta; w_G = Q - 1): contrast"
                                 + (" (the split matter-lapse contrast keeps it: its block carries the split G read)"
                                    if matter_lapse == "split" else ""))
        if background and lapse == "wave":
            from ..core.tensor import GearType
            bgk = Block((GearType("B", "audit"),),
                        tuple(gr.gradient_terms(gr.wave_potential("B", 0, 6 * Q))) +
                        (("metric.h00", -1, (("bgk.B", (0, 0, 0), "b"),), {"designated_one_way": RA_WHY}),),
                        name="bgk", vacuum={"B": 3 * Q - 1}, params={"Q": Q, "source": "demos/gravity/f4d_background.py"},
                        doc="R-a background gear (B1-GRAV F4d)", Q=Q)
            blocks.append(bgk)
            info["gravity_open"] = ("uniform-mode drift O(U^2 t^2) (+0.08 at U3 = 0.02, t = 700; passes at 4x weaker "
                                    "load, F4e); root cause: the non-conserved b-only stress; an exactly conserved "
                                    "first-order stress is OPEN (B1-GRAV)")
        info["gravity_note"] = (f"ONE lapse = {lapse_field} ({'one-way designated read of the OD2 accumulator' if lapse == 'od2' else 'reciprocal wave lapse'}); "
                                "OD2 stress OFF (B1-GRAV: b-only first-order stress is not conserved)")
        if l0_lapse is not None:
            if l0_offset != Q - 1:
                raise ValueError("l0_lapse needs l0_offset = Q - 1 (fine couplings into L0; R' everywhere)")
            if l0_lapse == "W":
                from .gravity_l0c import build_l0c_lapse
                blocks.append(build_l0c_lapse(Q=Q, P=P, field=lapse_field, body_signs=body_signs,
                                              oneway=(lapse == "od2")))
                info["l0_lapse_form"] = ("C: (1 - 2U) on M0 = 6 - Sum W_d, (1 - 4U) on the difference transport, "
                                         "ports Q - 1 + on-site 6 (owner decision 3)")
            elif l0_lapse in ("R", "W_split"):
                from .gravity_l0 import build_l0_lapse
                blocks.append(build_l0_lapse(Q=Q, P=P, field=lapse_field, body_signs=body_signs,
                                             oneway=(lapse == "od2")))
            else:
                raise ValueError("l0_lapse must be None, 'W' (form C), 'R' or 'W_split'")
    elif l0_lapse is not None:
        raise ValueError("l0_lapse needs gravity=True")
    # ---------------------------------------------------------------- choice observers (B1-CHOICE, odd Q)
    if choice:
        from . import choice as ch
        from .choice_oddq import build_odd_q_router, near_matched_kappa, predicted_non_detection
        r0 = 3 * Q - 1
        a1 = with_vacuum(ch.build_clock_ring(Q=Q, period=6, prefix="X", name="arm1"), r0)
        a2 = with_vacuum(ch.build_clock_ring(Q=Q, period=6, prefix="X", name="arm2"), r0)
        arm1 = tuple(f"arm1.X{j}" for j in range(3))
        arm2 = tuple(f"arm2.X{j}" for j in range(3))
        router = with_vacuum(build_odd_q_router(Q=Q, A=1, arm1=arm1, arm2=arm2, form="opposite", name="router"), r0)
        gate = with_vacuum(ch.build_fibre(Q=Q, axis=0, components=("F",), name="gate"), r0)
        exitp = with_vacuum(ch.build_gated_pair(Q=Q, kappa=near_matched_kappa(Q, 1), arm1=arm1, arm2=arm2,
                                                gate="gate.F", name="exit"), r0)
        blocks += [a1, a2, router, gate, exitp]
        info["choice"] = {"router_kappa": near_matched_kappa(Q, 1),
                          "P_none_per_readout": str(predicted_non_detection(Q, 1)),
                          "readers": "odd-Q near-matched router (rank 3) + ONE-SHOT gated exit pair (rank 4, gate fibre)",
                          "not_included": "F7 (taxicab light-cone choice: mechanism test only), drive, sequential router"}
    if electroweak and not chiral:
        raise ValueError("electroweak=True requires chiral=True (the electroweak completion is built on the chiral "
                         "candidate; layers.electroweak.compose_electroweak composes it itself)")
    if electroweak:  # EW-BUILDER's line (RC2 BATCH 2a); DEFAULT ON since OWNER decision 5 (13:09)
        from .electroweak import compose_electroweak; return _decided(compose_electroweak(System(Q, tuple(blocks), info), on=True))  # noqa: E702
    if chiral:   # HAND-M1's line (RC2 BATCH 1); with electroweak=False: the chiral layer alone
        from .chiral import compose_with_default; return _decided(compose_with_default(System(Q, tuple(blocks), info), on=True))  # noqa: E702
    return System(Q, tuple(blocks), info)


def _decided(system: System) -> System:
    """Metadata only: the chiral/electroweak status after OWNER decision 5 (CLOSED 13:09, hands ON)."""
    for key in ("chiral", "electroweak"):
        if isinstance(system.info.get(key), dict):
            system.info[key] = {**system.info[key], "status": "ON BY DEFAULT (OWNER decision 5 CLOSED 13:09)"}
    return system


__all__ = ["System", "default_system", "with_vacuum", "file_hashes", "Q_DEFAULT", "P_GRAV", "K_GRAV", "HOP",
           "WILSON", "MASS_DEFAULT", "MASS_PROPOSED", "E1_PARAMS", "E1D_SIGMA", "BODY_SIGNS_DEFAULT", "C2_PARAMS",
           "C2_DEFAULT"]
