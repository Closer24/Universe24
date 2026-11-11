# STUDY 26 — CHANNELS.md: how many channels, exactly, and why; which constants are forced (CH-A, constructive)
v2 by CH-A, 2026-11-10 (`date -u` stamps are in CH-A_NOTES.md). v1 was frozen at 15:10:51 UTC (sha256 4c699d80…; copy in
CH-A_work/) before CH-A read CH-B's proposal. The v2 amendments adopted from CH-B are marked [v2, CH-B Tn] and listed in §9.
CH-B (rigorous) marks this document in AGREE_CH.md.
Package and engine read-only; every number below is either CENSUS (counted by a script in s26/CH-A_work/ from the live
package code), THEOREM (with its proof or citation), FORCED (symmetry + minimality, argument given), CHOSEN (with the
alternative), DATA, DERIVED (an estimate from stated rules; marked UNBUILT where the construction does not exist), or OPEN.
A "channel" is one gear type: one (a, b, r) counter triple per node (link gears are stored at their base node). So the count
is per node and does not depend on L. The whole board holds 382·L³ triples: 82,512 at L = 6.

## 0. The answer in seven points
1. The ONE version (Study 22, `layers/one.py`, hands ON + FIX-i + cosmic block) has **382 channels per node** [CENSUS].
   The package alone has 375. Route B (ONE v2 hook) has 444.
2. Every block's size follows from the representation it carries. For 318 channels it is the smallest real module the
   sector's algebra can act on with integer, reversible, local (B3), rank ≤ 4 updates, plus B3 relay copies (§3). For 16 it
   is a design gear: the readers, β, the background, Φ and the loads. The dark board L0 (48) is the regular module of 2O.
   It is minimal only under the contract's frame rule: an unsigned permutation module that carries spin ½ must have 48
   channels [v2, CH-B T1]. If signed permutations are allowed, the spin-½ half V− (24) would do [CH-B T2].
3. No principle forces the TOTAL. The cube forces the representation TYPES (spin ½, mirrors, an SU(2)-type commutant). It
   forces no U(1), no SU(3), no family number and no total. So the count is **forced per unit and chosen in content**.
4. 228 of the 382 channels (60 %) sit in three gauge layers (su2, su3, u1) that read nothing and are read by nothing
   [CENSUS, coupling graph]. Today the SU(3) gluon field acts on no quark. At gear level, 9 of the 10 metric gears are
   uncoupled too: only h00, the lapse, is coupled. So the connected physical core is **127** channels [P9 = CH-B B1]. In route B
   the visible doublet (138 channels with its U(2) sector) is not coupled to gravity at all [P9b; declared OPEN in
   electroweak_b].
5. Minimal node (built constructions): **143** channels (ONE v1 content: one lepton-like doublet, Higgs, weak + E1 links,
   gravity, L0, cosmic clock). Route-B form: **205**. Without the dark board: 95 / 157. One full SM family needs the quark
   links, which are UNBUILT. Rank ≤ 4 forces one link per irreducible multiplet (M6(C) for the quark doublet), which gives
   a DERIVED estimate of about **1,057** (as-built relay form) or **817** (3-relay form, UNTESTED). Three families add
   +256 matter and +4 Higgs, i.e. **1,317 / 1,077** (§4). JOINT with CH-B (AGREE_CH): under today's rules one family is
   ≈ 817–1,057 channels plus unbuilt parts (upper end open). With an NL4-type NEW LAW (rank-4 two-link hops) it is ≈ 353–461.
   CH-B's earlier 413 / 669 used three separate link factors (degree 5). CH-B now keeps it only as a rank-blind lower
   bound. The count stays OPEN until a quark hop is built.
6. Constants: Q odd, the 6 in D = 6Q, the cone VALUE c² = (Q−1)/(3Q), the 1+2 split of L0 and the lattice-scale 1:2:3
   ladders are FORCED. That every massless gear shares that one cone is CHOSEN [v2, CH-B §5].
   Every mass (Yukawa integer), α, θ_W at low energy, N_c, the family number and all couplings are CHOSEN or DATA (§5).
7. JOINT owner sentence (CH-B B5 with CH-A's edit; both signed in AGREE_CH): "The cube and the Clifford algebra fix how big
   each kind of channel must be: 48 for the dark board (given a sign-free frame), 16 per charged Dirac fermion, 4 for the
   Higgs, 2 / 4 / 8 / 18 per link, 10 for the metric. They do not fix which kinds exist, how many copies (colours, families),
   or the total. Today there are 382 per node, and only 127 of them form the connected physical core (in route B the visible
   doublet is not yet coupled to gravity). A full Standard-Model family needs about 820–1,060 per node or more, because the
   rank rule forces one merged link for the quarks; that link is not built. With a new rank-4 law (NL4) it would be about
   350–460. Q odd, the 6, the cone c² = (Q−1)/(3Q) and the 1:2:3 ladders are theorems. Masses, α, the Yukawas and θ_W at low
   energy are data: no symmetry of the node can fix them. Fixing them needs a new law: a family group, one gauge coupling, or a
   Yukawa law."

## 1. CENSUS of the ONE version (scripts: CH-A_work/census.py → census.json; census_b.py → census_b.json; checks.py → checks.json)
Live package code, read-only, `one_system()` at Q = 2³³ + 1. layers/one.py sha256 087de46a… (mtime 14:58:39; it changed
during this study, but the census is identical before and after, CH-A_NOTES P1 re-run).

| quantity | ONE v1 (default) | package alone (cosmic off) | ONE v2 (route B) |
|---|---|---|---|
| channels (gear types) per node | **382** | 375 | **444** |
| monomials | 18,592 | 18,553 | 21,867 |
| designations (one-way) | 736 (= 706 + 30) | 706 | 74 |
| rank | 4 | 4 | 4 |

Correction to the s17 baseline: the s17 package count of 18,623 monomials was taken before FIX-i. FIX-i (λ_H = λ_L = 0)
removes 70 gwb terms, so the package now has 18,553 and ONE has 18,592 [CENSUS, CH-A_NOTES P1, E2 refuted as worded].

### 1.1 Block by block (ONE v1)
| block | ch. | what the channels are (gear names) | official / audit |
|---|---|---|---|
| ref (L0, dark board) | 48 | R00…R47: one per element of 2O | 0 / 48 |
| matter | 16 | X0–X7, Y0–Y7: one charged Dirac pair (8-block × 2) | 16 / 0 |
| matter2 | 16 | the weak partner pair (doublet index) | 16 / 0 |
| chiral | 4 | H_1, H_i, H_j, H_k: the Higgs doublet as a quaternion | 0 / 4 |
| wsu2 | 36 | weak SU(2) links U_d (3 × 4) + 2-path relays P_ab (6 × 4) | 0 / 36 |
| em (E1) | 4 | A_x, A_y, A_z (one per face, non-compact) + Φ | 0 / 4 |
| su2 | 40 | test doublet ψ (4) + links (3 × 4) + 2-paths (6 × 4) | 4 / 36 |
| su3 | 168 | test triplet ψ (6) + links (3 × 18) + 2-paths (6 × 18) | 6 / 162 |
| u1 | 20 | test scalar ψ (2) + links (3 × 2) + 2-paths (6 × 2) | 2 / 18 |
| metric | 10 | h00 (= THE lapse), h0i (3, link), hij (6) | 0 / 10 |
| beta | 1 | G (the β gear, GRAV-FIX A) | 0 / 1 |
| bgk | 1 | B (the R-a background, data gear) | 0 / 1 |
| arm1, arm2 | 3 + 3 | period-6 clock rings X0–X2 | 6 / 0 |
| router, gate, exit | 2 + 1 + 2 | dP, dM; fibre F; gated pair dP, dM | 5 / 0 |
| cosmic | 7 | Θ hand; M1, M2 (Θ readers); Lp, Lm (Born loads); dp, dm (matched pair) | 4 / 3 |
| lapse, lapseL0, ehop, gwb | 0 | coupling blocks only (0 / 1,728 / 232 / 1,152 terms) | — |
| **total** | **382** | | **59 / 323** |

### 1.2 By the brief's sectors (ONE v1)
| sector | channels | of which |
|---|---|---|
| dark board L0 | 48 | |
| Dirac matter pairs | 32 | matter 16 + matter2 16 (one lepton-like weak doublet) |
| Θ-reading cosmic matter | 2 | M1, M2 (complex first-order, not Dirac) |
| gauge-layer test scalars | 12 | su2 4 + su3 6 + u1 2 |
| Higgs | 4 | chiral |
| links (one per face, 3 faces per node) | 87 | su2 12, su3 54, u1 6, wsu2 12, E1 3 |
| E1 scalar potential Φ | 1 | |
| relays (2-paths, 6 ordered axis pairs) | 168 | su2 24, su3 108, u1 12, wsu2 24 |
| det-shadow | 0 | route B only: B link locked to det V, 6; hybrids Ξ, Ξ′, 24 |
| lapse/metric gears | 12 | metric 10, β 1, background 1 |
| cosmic hand Θ + loads + pair | 5 | Θ 1, Lp/Lm 2, dp/dm 2 |
| package choice readers | 11 | 2 rings × 3, router 2, gate 1, exit 2 |
| **total** | **382** | |

### 1.3 Who talks to whom [CENSUS, checks.json P4: connected components of the "reads" graph of the 18,592 monomials]
| component | channels | members |
|---|---|---|
| the physical core (gear level, P9) | **127** | ref 48, matter 16, matter2 16, wsu2 36, em 4, chiral 4, metric.h00 1, beta 1, bgk 1 |
| uncoupled metric gears | 9 × 1 | h0x, h0y, h0z, hxx, hyy, hzz, hxy, hxz, hyz: each reads only itself (namespace level counted them in a 136 "core"; CH-B B1 corrected this, P9 confirms) |
| package choice readers | 11 | arm1, arm2, router, gate, exit (they read only their own clock rings) |
| cosmic clock | 7 | cosmic (block-diagonal, as one.py states) |
| isolated gauge layers | 40 + 168 + 20 = 228 | su2, su3, u1 (each reads only itself; no gravity coupling either) |

FINDING (CENSUS): 60 % of the node (228 / 382) is three gauge layers that carry only their own test scalars. The SU(3)
layer is not coupled to any quark (there are none) and not coupled to the lapse. The Dirac doublet couples to E1, to the weak
links (wsu2) and to the Higgs (chiral). It also couples to the metric: 384 monomials each way (P4 edge counts). This is a statement about the composed
tensor, not a defect report: the layers were built as demonstrations of exact local Gauss (GU §2.1).

## 2. C1 — Each count derived from the representation it carries
Notation: dim_R = real dimension; type = Frobenius–Schur type (real / complex / quaternionic).

| sector (ch./node) | algebra and module | why this dimension | verdict | the alternative |
|---|---|---|---|---|
| **L0 (48)** | the group algebra R[2O] = R² ⊕ M2(R) ⊕ M3(R)² ⊕ H² ⊕ M2(H), with 2O acting on the left (frame) and on the right (internal) [GU §1.1] | regular module: one channel per element. Signed-permutation ports force a permutation module (the labels are permuted); one free orbit has \|2O\| = 48 elements; 48 = \|Aut 2O\| = \|O_h\| is structural [AGREE_CUBE N1] | FORCED given the contract's frame rule (AGENTS rule 1: channels = 2O labels, frame = unsigned left multiplication) + spin ½ [v2, CH-B T1]. Not forced by symmetry alone | **THEOREM (CENSUS P6 + P7, exact over Q(√2)):** the smallest faithful signed-permutation module with z = −1 has dim 8 (induced from Z6). P7: it is the real form of 2·G3/2, i.e. spin-3/2 type with **no E½**. The smallest faithful pure permutation module has dim 16 (from Z3), also without E½. The smallest faithful linear module is H (dim 4, not monomial). **[v2, CH-B T1/T2]** With the criterion "carries spin ½ (E½)": unsigned → only 48; signed → 48 or **24** (V−, an exact invariant set of the law, GU §1.3). So 48 is FORCED by "unsigned frame + spin ½". It is not forced by symmetry alone. |
| **Dirac pair (16)** | 8-block H ⊗ R² with P_d = L_d⊗σz, W0 = 1⊗σx; pair = 8-block ⊗ C(J′) | **THEOREM (P3, package matrices):** ⟨P_x, P_y, P_z, W0⟩ has dim 16 = Cl(1,3) ≅ M2(H), whose unique irreducible real module is R⁸. Its commutant is H (dim 4: J, K, JK). In H two complex structures commute only if they are ±equal (0 non-parallel commuting pairs, P3). So a charge J′ that commutes with the clock J needs a second factor: ⊗C → 16 | 8: FORCED once massive first-order Dirac hops are CHOSEN. ×2: FORCED once a charge J′ ≠ J with linear C and the CP-even hand Γ5·V (V = JJ′) is CHOSEN [GU §1.4; matter.py: "pair = the charged species, single = neutral"] | the textbook field ψ ∈ C⁴ = R⁸ with charge = clock i: 8 per Dirac fermion. Then no V = JJ′ exists, and the built weak hand needs a new construction (OPEN) |
| **weak doublet (×2)** | (matter, matter2) = C² with i = J′ | SU(2) fundamental, dim_C 2 | FORCED once the weak doublet is CHOSEN [AGREE_CUBE: "the WEAK doublet of matter CHOSEN"] | — |
| **Higgs (4)** | C² of SU(2)_L × U(1)_Y as one quaternion; SU(2)_L × SU(2)_R real (2,2) | minimal real faithful module carrying the doublet: R⁴ = H | FORCED once the Higgs doublet is CHOSEN | complex bidoublet (8) for the three-family spec (GU §5.5) |
| **test scalars (4 / 6 / 2)** | fundamentals of SU(2) (H, quaternionic), SU(3) (C³, complex), U(1) (C) | smallest faithful real modules: 4, 6, 2 (the adjoints are not faithful: centres ±1, Z3) | FORCED (given the layers) | drop the layers (§1.3: nothing reads them) |
| **compact link (per face)** SU(2) 4, SU(3) 18, U(1) 2; route B U(2) 8 | parallel transporter U ∈ Hom(V_y, V_x) = V ⊗ V*, a bimodule U ↦ g U h⁻¹ | (2, 2̄) is real type (pseudo-real ⊗ pseudo-real): real form H = R⁴; (3, 3̄) is complex type: R¹⁸; U(1): C = R²; U(2) on a hypercharged doublet: End(C²) = M2(C) = R⁸ (Burnside rank-3: one link per face per irreducible multiplet [GU §2.2]) | FORCED (smallest linear space on which the gauge group acts linearly by both sides with the group as an orbit; needed for polynomial rank ≤ 4 updates) | the group manifold has dims 3 / 8 / 1, but no linear space of that size carries the two-sided action |
| **E1 photon (4)** | A_d ∈ u(1) = R on each face + Φ | non-compact U(1): 1 per face; Φ: the Lorenz-gauge time component (SO(3,1) vector 3 + 1) | A_d FORCED (non-compact); Φ CHOSEN (Lorenz gauge) | route B retires E1 (photon = W3/B mix) |
| **relays / 2-paths (6 per link)** | P(x; a, b) ~ U(x, a) U(x+e_a, b): transforms like a diagonal link G(x) P G(x+e_a+e_b)^† | a plaquette touches 3 storage nodes (x, x+e_a, x+e_b); B3 allows one node or one face link per monomial, and rank ≤ 4 forbids the 4-link product with a matter factor. The ON-SITE split form ‖V(x,a)R(a,b) − V(x,b)R(b,a)‖² needs both halves per plane: 3 planes × 2 = 6 copies of the link module | 6: FORCED in the on-site form (as built: B1-GAUGE 2-paths; route-B plaquette option) | **B3-CHECKED (P8: the core's check_locality accepts all 36 force monomials; the relay-free control is rejected), dynamics UNTESTED:** the one-face-link form Re Tr(V(x,a) R(x;a,b) V(x+e_b,a)† V(x,b)†) touches only x and x+e_b, so one relay per plane suffices: **3** per link. The rank-3 two-path variant (one P per plane, locked to both 2-paths) also passes. That would save 84 channels in ONE v1 (168 → 84). CH-B T6 found the same independently |
| **metric (10)** | h̄^{μν}: Sym² of the 4-vector | dim Sym²(R⁴) = 10; physical (TT) content 2 | FORCED for a local, gauge-fixed (harmonic) linear spin-2 field with all components as Rule3 gears. **Today only h00 is coupled (P9).** So "10" is a SIZE statement, and γ = 1 is encoded, not produced by h_ij (CH-B B1) | lapse only (1 gear; the scalar OD2-type variant): static gravity only, with no gravitational waves. γ = 1 can still be encoded through the link factor (correction after CH-B T9; v1 wrongly said it is lost). 6 (synchronous gauge) needs constraints that Rule3 cannot impose exactly (OPEN) |
| **β (1), background (1)** | implementation gears (β = 1 static law with detuning; the declared k = 0 background) | one scalar each | CHOSEN (GRAV-FIX A; R-a data gear) | — |
| **clock ring (3 each)** | three gears with u = 3Q b: (a, b) → (b, b − a), period 6, phases 0, 2, 4 | constant intensity Σ b_j² on the Z6 phase grid needs offsets that sum to zero: 0°, 120°, 240° → 3. A 90° pair is not on the 60° grid | FORCED given period 6 | period-4 ring with 2 gears (90° grid) [choice.py] |
| **router / exit pairs (2), gate (1)** | matched shared-remainder pair (dP, dM); a d'Alembert fibre | a binary outcome needs 2; a one-sided gate needs 1 | FORCED given the reader design | — |
| **cosmic (7)** | Θ (a real scalar hand), M1 + i M2 (complex first-order Θ reader), Lp, Lm (static loads), dp, dm (matched pair) | 1 + 2 + 2 + 2 | Θ, M, pair: FORCED given the WIND design; Lp, Lm: CHOSEN (loads stored as gears so that they are seed DATA, not tensor constants) | loads as tensor coefficients: 5 channels |

## 3. Is there ONE principle that forces the whole count?
**CH-A proposal: MER (minimal exact real realization).** Each sector's channel count is
  n = dim_R(smallest real module on which its algebra acts by integer, reversible (one potential), b-only updates)
      × (1 + number of B3 relay copies its rank ≤ 4 couplings need).
Applied block by block (§2), the 382 channels split as follows:
- MER modules: 150 (Dirac 32, Higgs 4, test scalars 12, links 87, metric 10, cosmic Θ + readers + pair 5);
- MER relays: 168 (2-paths, on-site form);
- reader designs: 11 (rings 6, pairs 4, gate 1), forced by their own design rules;
- CHOSEN implementation gears: 5 (β, background, Φ, Lp, Lm);
- L0: 48.
**L0** is MER-minimal only under the contract's frame rule. An unsigned permutation module carrying spin ½ has exactly 48
channels [v2, CH-B T1]. With signed permutations, 24 (V−) suffice [CH-B T2]. Without the spin-½ requirement, 8 (2·G3/2, P7)
or 4 (H, linear) suffice.

The brief's candidates, tested:
| candidate | what it forces | where it fails |
|---|---|---|
| regular representation | L0 = 48 | **[v2, CH-B §4a]** a regular module has χ(z) = 0, i.e. as many boson as fermion channels. ONE v1 has N_F = 56 (V− 24 + 32 Dirac) and N_B = 326: REFUTED for the total. (Also: continuous groups have no finite regular module.) |
| minimal faithful real rep | Higgs 4, test scalars 4/6/2, links as bimodules, Dirac 8 | L0 (48: the minimal faithful module is 4 linear or 8 signed, and neither carries the regular content); the pair's ×2 (needs the second complex structure, a design premise) |
| Cl(0,3) = H ⊕ H | the 8-block structure, the orientation bit Γ5 = −PxPyPz, one hand | it says nothing about gauge, gravity or clock counts |
| Pati–Salam 128 = 2⁷ | nothing beyond the count 8 Dirac × 16 | a power of 2 because the multiplet dimensions (4, 2) are; Cl(0,7)'s module is 8, not 128 (LEDGER N2) |

**Verdict (CH-A):** there is no single principle that forces 382, 375 or 444. The cube forces the TYPES: spin ½ (one
involution), mirrors = the outer automorphism, an exact SU(2)-type commutant (right Q8), total reality (no native U(1) or SU(3))
[AGREE_CUBE Part IV]. MER forces the UNIT SIZE of every chosen sector. The CONTENT is chosen: N_c = 3, U(1)_Y, the weak doublet,
the number of Dirac fermions, the number of families, which gauge layers are present, and the regular L0.
**A NEW LAW would be needed to force the content.** None is known. s16 AGREE_FA: no natural family 3; s17: no SU(3) from the cube.

## 4. The minimal node
Rules: the package rules (Rule3, one D, B3, rank ≤ 4, six faces); MER unit sizes; the contract keeps L0 (48) unless stated.

| sector | ONE v1 as built | minimal, ONE content (E1 form) | minimal, ONE content (route-B form) | one SM family (DERIVED) | three families (DERIVED) |
|---|---|---|---|---|---|
| L0 dark board | 48 | 48 | 48 | 48 | 48 |
| Dirac matter (×16 each) | 32 | 32 | 32 | **128** (8 Dirac incl. ν_R) | **384** |
| Higgs | 4 | 4 | 4 (in ewb) | 4 | 8 (complex bidoublet, GU §5.5) |
| electroweak links + relays + locks | wsu2 36 + E1 4 | 40 | ewb 102 (V 24, 2-paths 48, det-locked B 6, hybrids 24) | 102 | 102 (links are family-blind) |
| quark links | — | — | — | Q_L: M6(C) = 72/face → 216; u_R, d_R: M3(C) 18/face each → 108 (locks OPEN, UNBUILT) | same |
| quark relays | — | — | — | 6 × 72 = 432 (on-site form) or 3 × 72 = 216 (3-relay form, UNTESTED) | same |
| quark hybrids (Wilson–Yukawa) | — | — | — | UNBUILT, not counted | UNBUILT |
| gravity (metric 10, β 1, background 1) | 12 | 12 | 12 | 12 | 12 |
| cosmic clock | 7 | 7 | 7 | 7 | 7 |
| isolated gauge layers su2/su3/u1 | 228 | 0 | 0 | 0 (the quark links carry colour) | 0 |
| package choice readers | 11 | 0 (the cosmic pair suffices) | 0 | 0 | 0 |
| **total** | **382** | **143** | **205** | **1,057** (817 with 3 relays) + hybrids | **1,317** (1,077) + hybrids |
| without L0 (variant) | 334 | 95 | 157 | 1,009 (769) | 1,269 (1,029) |

Notes. (i) 143 and 205 are CENSUS sums of built blocks. As USED by today's dynamics (only h00 of the metric is coupled, P9) they
are 134 and 196. In the route-B form the doublet and gravity are separate components (P9b), so 205 is a sum of built blocks,
not a coupled node. (ii) The one-family column is DERIVED: the rank rule (GU §2.2) forbids
separate SU(3), SU(2), U(1) link factors on one quark hop (degree 5). So the quark doublet's hop needs ONE link in
End(C³ ⊗ C²) = M6(C), which is complex type, 72 real per face. The locks that tie u_R, d_R (and e_R, already built as det V) to
one gauge field are OPEN and may be obstructed by rank. These quark numbers are the largest uncertainty in the whole census.
(iii) The matter count is the robust part: 16 per Dirac fermion, 128 per family, 384 for three families (= GU §1.4/§5.5).
ν_R is FORCED, not chosen: every matter block is a Cl(1,3) module containing both hands [v2, CH-B T7].
(iv) CH-B's frozen §3 counted one family at 413 (341 with 3 relays) using separate SU(3), SU(2) and U(1) links, 9 × 24 = 216.
CH-A disagreed that this is admissible, and CH-B ACCEPTED (AGREE_CH B-II, 15:17:48): a quark-doublet hop through separate link factors has degree 5 (rank 5), or rank 4
of a non-approved kind with two factors. GU §2.2 says the rank rule forces link unification. 413 is therefore a lower bound
that ignores the rank rule. Precise three-tier statement (citations: s11/AGREE_CL3 row 17; s12/AGREE_GU1 A8, B5 Cor 5a;
README_v1_draft "one rank-4 kind, NARROW: uncharged singlet × gauge-covariant rank-3 composite"):
  - three separate factors (SU(3)·SU(2)·U(1)) on a quark hop: degree 5, FORBIDDEN under any rank ≤ 4 rule. This is CH-B's 413.
  - two factors (SU(3) link ⊗ U(2) link): rank 4, NOT an approved kind (the narrow kind excludes link × composite; Cor 5a). It
    becomes admissible only with a NEW LAW of the NL4 type. CH-B's U(2) variant, 9 × 26 = 234 link channels, gives
    48 + 128 + 234 + 4 + 10 + 7 = **431** (353 with 3 relays). This is the cheapest family node, and it requires that NEW LAW.
  - one link per irreducible multiplet (Burnside, rank 3): admissible today, gives **≈1,057 / 817**. The hypercharge locks between
    multiplets are UNBUILT and may be obstructed: Y-ratios such as Q_L : L = 1/6 : −1/2 would need powers of det V above
    rank 4.
  **JOINT (AGREE_CH, accepted by CH-B 15:17:48, with CH-B's edits):** one family ≈ 817–1,057 channels under today's rules,
  plus unbuilt parts: the u_R/d_R locks or relays (up to 6 × 36 = 216) and the quark hybrids, so the upper end is open. With an
  NL4-type NEW LAW it is ≈ 353–431, or 383–461 with route B's det-shadow (6) and hybrids (24). The construction is OPEN.
(v) MER's one-relay-per-plane saving is counted only in parentheses because its dynamics is untested.

## 5. C2 — The constants of the ONE version (live values from checks.json P5)
| constant | value in ONE v1 | status | reason / allowed range |
|---|---|---|---|
| Q odd | 2³³ + 1 = 8,589,934,593 | odd: **THEOREM** (CUBE-B R10: R′ fixes the vacuum 3Q − 1 only for odd Q); size: CHOSEN | resolution; needs Q − 1 = 2Pk (gravity), D·Θ0 < 2⁶¹ (int64) |
| D = 6Q | 51,539,607,558 | 6: **THEOREM given K = 2u** (\|λ\| ≤ 6 by the triangle inequality on six signed permutations; the flat class attains 6; so 6 is the smallest divisor stable for every sign class; upgraded at CH-B's request); one D for all gears: CHOSEN (owner rule) | — |
| c² (one cone of the field gears) | (Q − 1)/(3Q) = 8,589,934,592 / 25,769,803,779 | the VALUE: **FORCED** within the stencil class u = w_f Σ6 b + w_s b at one D (w_f = Q − 1 is the fastest strictly stable integer choice; s19 T1, CH-B §5). That EVERY massless gear uses it ("one cone"): CHOSEN [v2, CH-B §5] | → 1/3 as Q → ∞. Compact gauge waves: c² < c_U/(4D) < 1/4 (THEOREM), so they are slower; one light on c_Q with exact Gauss is impossible under the current rules (s19) |
| γ = 1 | clock factor 1 − 2U, link factor 1 − 4U | CHOSEN (encoded to match GR), not derived | only the Dirac pair and L0 read the lapse today |
| L0 levels | cos w = ((Q−1)λ + 6)/(6Q), λ_x = 2s_x, λ_{y,z} ∈ {2s_x ± 2} | the **1 + 2** split: FORCED (THEOREM N2 + mirror); the lattice-scale 1:2:3 (carrier-0): FORCED [AGREE_MASS B4] | bosonic, isospin-distinct: not the families |
| body actions, signs | (0, 1, 3); (1, −1, 1) | twist class {0, ±¼}: FORCED (connected + mirror); the lift and the signs: CHOSEN | 4 sign classes |
| matter hop, Wilson, mass | 2³¹, 2³⁰, 4915·2²² (cos w0 = 0.39998) | CHOSEN | mass + 12·wilson ≤ D: FORCED (stability); mass ∈ 2²²Z: FORCED given P (gravity's lapse rule) |
| gauge regime | A = κ = 2¹⁶, λ = 4, κ_P = 256, c_P = 0, β = D − 2³³ = 5Q + 1, c_U = 2¹⁷ | CHOSEN (linearly stable, Gauss exact) | photon/gluon speed follows from the regime (frozen, v ≈ 8·10⁻⁴ c_Q in route B's default) |
| E1 | g_φ = 4, g_A = 1, σ = 2²⁴ | CHOSEN | weak-field rule amplitude × field ≥ D/(8g_φ) = 1,610,612,736 (DERIVED) |
| Higgs / Yukawa | v = A = 2¹⁶, κ = 2¹⁵, w = 2¹⁴, y = 157,280, y_tot = 206,432, λ_H = 4, k_H = 2¹⁰ | **DATA** (masses = Yukawa integers; ≈ 39 bits for the leptons) [AGREE_MASS] | Koide is representable (Z[i] circulant), not forced |
| FIX-i | λ_H = λ_L = 0 in gwb | CHOSEN (owner v8-1, stability) | the earlier λ = 4 runs away (s18) |
| gravity | P = 2²⁰, k = 2¹², w_G = (Q − 1)/2, k_G = 2¹¹ | Q − 1 = 2Pk: FORCED relation; values CHOSEN; the detuning ½: CHOSEN (GRAV-FIX A, avoids a 1:1 resonance) | the static law G = F²/(2P) (β = 1) is fixed by construction |
| cosmic | Θ0 = 2²⁴, h = 2⁷ (24hΘ0 = D − 6), k_Θ = 2³², g_w = 1310, c_pair = 1809, load sum 3Q/c_pair = 14,245,331 | 6k_Θ < D: FORCED (stability); 24hΘ0 ≤ D: FORCED (inside the band); c_pair \| 3Q: FORCED; the values: CHOSEN; g_w: from CC-A's pre-registered rule (Tq = 100, L = 6, A = 2¹⁰) | the matched pair gives K⁺ − K⁻ = D·I exactly (initial data) |
| choice readers | router κ = 3·2³⁰ | DERIVED (near-matched: P_none = 1/Q per readout) | — |
| seed amplitudes, Θ0, loads p | DATA | DATA | norm-matched seeds |
| L | 6 in the runs | DATA (L ≥ 3) | — |

**Physical ratios that ARE forced on this board:** the cone value c² = (Q−1)/(3Q) of the fastest strictly stable stencil
(sharing it across all field gears is CHOSEN); compact gauge waves slower (THEOREM); the 1 + 2 split and the lattice-scale 1:2:3 ladders (L0 triple; Wilson doublers); the exact Koide SHAPE of
the handed board's spinor levels at the lattice scale (δ ∈ {0, π}; it is not the lepton spectrum); exact local Gauss (Z4 / Q8 /
Δ96); one hand (Cl(0,3) = H ⊕ H). sin²θ_W = ½ (route B, one norm for the U(2) link) is FORCED only as a CUTOFF value. As a
low-energy relation it is FALSIFIED; as a cutoff it needs Λ ≈ 5·10²⁰ GeV [AGREE_MASS B17/A12].
**Free (data):** every fermion mass, α, θ_W at low energy, m_W/m_Z, m_p/m_e, N_c, the number of families, the gauge regime.
So on this board "nature's constants" split cleanly into integer-arithmetic facts (Q odd, 6, the cone value, the 1+2 /
1:2:3 lattice ladders) and seed / tensor DATA (all masses and couplings).

## 6. Anti-numerology ledger (s21 protocol; pre-registered in CH-A_NOTES.md before drafting)
No numerical-coincidence claim is made. Noticed and REJECTED: N1 48 + 40 + 168 = 256 (block subsets, 2¹⁸ trials); N2 128 = 2⁷
(a count); N3 384 = 3·128 = 8·48 (s16: a count); N4 375, 382, 444 (no structure). 4 noticed, 0 kept. CH-B adds 3 more:
16 = |2O/Z3| (no spin ½ in R[2O/Z3]); 8 = the minimal faithful module of G384 = the Cl(1,3) module (different frame content);
D = 6 = |S3|. **Joint ledger: 7 noticed, 0 kept** (AGREE_CH A13). The derivations in §2
are theorems about module dimensions (checked exactly in P3, P6, P7), not fits.

## 7. What would force more (NEW LAW needed) and what is OPEN
- A content law that selects SU(3) × SU(2) × U(1), N_c = 3 and three families. Nothing in the cube does this (total reality;
  the internal triple is bosonic and 1+2).
- A law that fixes the Yukawa integers (none known; masses are DATA).
- A smaller dark board (24 = V− with signed frame permutations, CH-B T2) would CHANGE the fixed model (AGENTS rule 1). Not
  proposed. It is recorded only to answer "is 48 forced". It is forced by the contract's unsigned frame together with spin ½
  (CH-B T1), not by symmetry alone. (The 8-dim spinorial module of P6/P7 carries no spin ½, so it is not a candidate board.)
- OPEN: the quark links and their locks (§4 ii); the stability of the 3-relay plaquette form; a textbook-size (8-channel)
  charged Dirac field with a CPT-safe weak hand; whether the three isolated gauge layers should stay in ONE (an owner decision,
  not a census question).

## 8. Owner summary
The Hebrew owner summary of this section is kept in the scratchpad record (s26/CHANNELS.md §8); the repository copy is English-only per CONTRIBUTING.

## 9. Amendments after reading CH-B (v2; every item is in AGREE_CH.md "CH-A marks")
1. L0: P6's 8-dim signed module (Ind from Z6) is spin-3/2 type (P7: the real form of 2·G3/2, no E½). With "carries spin ½",
   the minima are 48 (unsigned, CH-B T1) and 24 (signed, V−, CH-B T2). CH-A's v1 sentence "48 is the regular choice, not the
   minimal one" is withdrawn. It now reads: 48 is minimal given an unsigned frame and spin ½.
2. "One cone" moved from FORCED to CHOSEN. The VALUE c² stays FORCED within the stencil class (CH-B §5).
3. ν_R: FORCED (CH-B T7), not content.
4. The regular-module principle is refuted by the boson/fermion count N_B = 326 ≠ N_F = 56 (CH-B §4a).
5. DISAGREE, RESOLVED (CH-B accepted at 15:17:48): CH-B's one-family node of 413 ignores the rank rule for quark hops (§4 note iv). It is sharpened into
   three tiers: 413 forbidden (degree 5); 431 / 353 only with an NL4-type NEW LAW; ≈1,057 / 817 admissible today.
6. Metric alternative: a lapse-only gravity keeps γ = 1 (encoded through the link factor) but loses the waves (CH-B T9).
7. 3 relays per link: now B3-checked by the core's check_locality (P8, 36/36 accepted). Dynamics is still untested.
8. After CH-B signed (15:17:48): the connected core is 127 at gear level (CH-B B1; P9 confirms). Only h00 of the metric is coupled.
   In route B the doublet is not coupled to gravity (P9b, new). The minimal-node "as used" counts are 134 / 196.
9. The one-family joint text carries CH-B's edits: 383–461 with route B's det-shadow and hybrids, and the upper end of 817–1,057
   is open (u_R/d_R locks and relays, quark hybrids).
10. "6" upgraded to THEOREM given K = 2u (CH-B A12). The ledger is now joint: 7 noticed, 0 kept (CH-B A13).
