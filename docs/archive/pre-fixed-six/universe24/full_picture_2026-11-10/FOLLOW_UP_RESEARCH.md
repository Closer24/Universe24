# FOLLOW-UP RESEARCH AND RECOMMENDATIONS — the ONE version of metric_variant_v1 (Study 32)

Writer: FOLLOW-UP (Study 32). Written 16:10–17:50 UTC, 2026-11-10 (`date -u`). Status: **FINAL.** Studies 27, 28 and 35 are filled
from their signed agreements, Study 30 from its final results, Study 34 from its signed agreement (both signatures at 17:42 UTC).

- **Scope.** `research/metric_variant_v1`, a separately named candidate variant, in its default "ONE version". The reference engine
  `universe24/` is unchanged and out of scope. Light, gravity, Einstein, Born, Bell and Pauli name declared constructions of this
  variant and their listed tests; they are not physical claims.
- **Sources (signed records only).** In this folder: `THE_ALGEBRA.md` (§10 lists), `GRAND_UNIFICATION.md` (GU, §11.3), `CHANNELS.md`;
  sanitized signed agreements `records/s<N>_AGREE_*.md`; package files `../README_v1_draft.md`, `../NOTES_one.md`,
  `../NOTES_einstein.md`, `../NOTES_electroweak_b.md`, `../AGREE_STAB_2026-11-10.md`. Paths `s<N>/…` without `records/` are research
  records outside the repository.
- **Labels** (one per claim, never upgraded): THEOREM, NUMERIC, DERIVED, CHOSEN, NEW LAW, OPEN, as in `THE_ALGEBRA.md`; TUNED and
  POSTED only when quoting a source's exclusion label; POST HOC marks a diagnosis made after a run; "DERIVED (this note)" marks an
  inference first made here; OPINION (manager) marks the assessment lines of §5, which are not results.
- **Fields.** Problem; Known (label + source); Why it matters; Next step, inside the owner's rules (rank 4; one tensor + seed + Rule3;
  nothing posted, forced, faked, circular or tuned; no-signalling from the law; no freeze; a new seed per bang; matter does not read
  the cosmic clock; runs only in scratch mirrors); Needs (NEW LAW and/or OWNER); Difficulty S (a check or a small run), M (one
  study), L (several studies, or a new law + verification). Q is the divisor parameter (D = 6Q), not the engine's signed account;
  "C1"/"C2" are Study 22 run labels, not the arithmetic class C2 of AGENTS.md and not the ZQ8 spring "c2".

---------------------------------------------------------------------------------------------------------------------
## 1. Status in one paragraph

ONE is one integer tensor at one odd Q = 2^33+1 (D = 6Q) on one periodic L³ cube with six face neighbours, updated only by Rule3
from one seed [CHOSEN inputs]. Its default, by the owner's decision, is ONE v1 (`one_system()`, couple_doublet off): the package
default (hands ON; FIX-i, λ_H = λ_L = 0; GRAV-FIX A) beside the cosmic-clock layer (the WIND hand, matched choice pairs, the
layer's own Θ-reading species) [NEW LAW for the layer, owner-approved], with 0 monomials across the boundary: G 382, rank 4, 18,592
monomials, 736 designations, dynamics fingerprint 77f6d251… [NUMERIC; `records/s22_AGREE_ONE.md`]. Matter does not read the clock:
the doublet × hand coupling is rejected, runs away, and is kept only as an explicit opt-in (P4). Rule3 is an exact bijection; every
gear is a clock, a click is a carry, every ledger closes with 0 failures, and every completed rewind was exact (the long high-bit
v1 rewinds were not completed) [THEOREM; NUMERIC]. ONE v1 shows no runaway in what could be run (to t = 9,869 at L = 6), but it is
not quiet: E1, β and the metric grow slowly (E1 at the 32-bit bound by t ≈ 8,000), and its massless uniform lapse is not small: it
rises to +0.024 near t ≈ 4,150, crosses 0 near 6,050 and accelerates to −0.186 at t = 9,869, as the exact identity explains
[NUMERIC; Study 30]. The hand turns about every 192 updates at L = 6 (an INPUT via g_w; the quarter
period scales as √N, to 1 %); each turn starts a new seed with ≈ 80 kB of new outcome record; the history does not depend on the
outcomes in the matched seed sector [NUMERIC, POST HOC framing]. In the continuum limit the tensor carries Einstein's weak-field
kinematics (one cone given the chosen stencil; γ = 1 via the CHOSEN link factor; the EP of the factor, live only for the dark board
L0; Lorentz symmetry at O(k²)); its gravity is a Newtonian-level sourced scalar lapse [DERIVED; `THE_ALGEBRA.md` §5]. An opt-in,
default-OFF layer adds linearised Einstein in harmonic gauge (diagonal sector, L0 only), with bending and Shapiro 2× on the board;
the full Einstein equations do not hold at rank 4 [THEOREM + NUMERIC; Study 28]. No-signalling is the B3 cone theorem; the owner's
no-freeze rule for the clicks is built exactly for one quantum, but for a Bell pair with a typical seed S ≤ 2 exactly, so "Bell
stands" is not met [THEOREM + NUMERIC; Studies 14, 27]. Only the nine dark lattice-scale rest levels (and 0) come out of the clicks
by themselves; every visible mass value is a tensor integer or seed data, about 39 bits for the leptons [THEOREM + NUMERIC;
Study 35]. Missing by theorem on one board: Pauli exclusion and true entanglement. Open: gravity of visible matter (the FIX-i debt),
connected quarks and colour. A clock law through time alone (CG2: one designated lapse term per node, no matter reading Θ) holds
the uniform lapse only for L ≤ 6 at the CHOSEN Θ0 = 2^21 (|U| ≤ 4.1·10⁻³ to t = 8,900 at L = 6); it is pumped at L = 8, does not hold
L0 lumps, and stays an opt-in [THEOREM + NUMERIC; Study 34, `records/s34_AGREE_CLK.md`].

---------------------------------------------------------------------------------------------------------------------
## 2. Open problems, prioritized

### 2.0 Overview (ordered by importance; §3 orders the next studies)
| # | problem | status today | needs | size |
|---|---|---|---|---|
| [P1](#p1) | a generic clock law: the hand acting on time (Study 34) | NUMERIC (CG2 holds \|U\| for L ≤ 6 only); THEOREM (no fold, not every clock); OPEN (size-independent law) | NEW LAW + OWNER | L |
| [P2](#p2) | the default's massless uniform (k = 0) lapse: \|U\| = 0.186 at t = 9,869, accelerating | THEOREM (identity, massless); NUMERIC (Study 30); OPEN (a bounding law) | OWNER (± NEW LAW) | M–L |
| [P3](#p3) | masses from the clicks vs masses as data (Study 35) | THEOREM (only dark levels come out; THEOREM E, K); CHOSEN (visible values) | NEW LAW + OWNER | L |
| [P4](#p4) | the coupled build C1: rejected by the owner, runs away; kept for the record | NUMERIC (runaway, OB5, grain); CHOSEN (rejection) | nothing (switched in this release) | S |
| [P5](#p5) | the doublet's FIX-i EP debt | NUMERIC (no lapse factor, no source; grain wall); DERIVED (trilemma) | NEW LAW + OWNER | L |
| [P6](#p6) | full Einstein: G-NOGO-a, no exact Bianchi; the opt-in linearised layer | THEOREM (no exact form); NUMERIC (layer, Study 28) | NEW LAW + OWNER | L |
| [P7](#p7) | light bending: run on the opt-in layer, not in the default | NUMERIC (2.08–2.16×); OPEN (b ≥ 10; default carrier) | OWNER (choice) | M |
| [P8](#p8) | frame dragging and gravitational waves | THEOREM (no felt h0i, second-order matter); OPEN (radiation) | NEW LAW | L |
| [P9](#p9) | remainder freshness (Born statistics) | THEOREM (Born given freshness); OPEN (freshness) | nothing (test); NEW LAW (fix) | S–M |
| [P10](#p10) | Bell, entanglement, Pauli; free choice vs determinism | THEOREM (S ≤ 2 on one board, Study 27); NEW LAW (separate variant) | NEW LAW + OWNER | L |
| [P11](#p11) | quarks and gluons unconnected | NUMERIC (census 228/382); OPEN (quark hop) | NEW LAW (route-B link) + OWNER | L |
| [P12](#p12) | three families | THEOREM (no natural 3); NEW LAW (target, unbuilt) | NEW LAW (separate variant) | L |
| [P13](#p13) | route B: photon slower than c_Q | THEOREM (no one light under current rules); NUMERIC (0.408 c_Q) | OWNER (a fixed rule) | M–L |
| [P14](#p14) | falsifiable predictions never measured | DERIVED; NUMERIC on the law | nothing | S–M |
| [P15](#p15) | 13 committed results with pre-FIX-i values | NUMERIC | write authorisation | S |
| [P16](#p16) | code-label and doc cleanups | NUMERIC (review) | nothing | S |

Other OPEN items of GU §11.3: the slow compact cone (6), the L0 dark seed (9), cosmological expansion (10; P2), strong dynamics (11; P11).

### <a id="p1"></a>P1. A generic clock law: the cosmic hand acting on time itself (Study 34)
- **Problem.** The owner asks for "a generic solution that solves everything through the clocks only". Study 34's lawful candidate
  (CG2) holds the default's uniform lapse only inside a size window (L ≤ 6 at Θ0 = 2^21); a size-independent law is OPEN.
- **Known.**
  - CHOSEN (owner): matter must not read the cosmic clock; "generic" = one universal rule acting on every clock alike, as the lapse
    does under the EP. — s34/README_STUDY.md (research record).
  - THEOREM (Study 34, signed by both, no DISAGREE): one-way is forced (a reciprocal Θ–lapse term puts an additive source into the
    hand's input, forbidden by THEOREM O's Θ row; this refines my earlier R5-lemma reading); through time a turn reaches matter only
    as a common clock-rate (redshift) change, never as a fold or an echo; "every clock reads the lapse" is IMPOSSIBLE at rank 4
    (quartic potentials would become rank 5), and the doublets' rest clocks do not feel a turn (0/16); an additive drive (CG1,
    u[h00] += κ·b_Θ) is felt exactly but cannot bound the uniform lapse. — `records/s34_AGREE_CLK.md` A2, A3, A8, A13, B3, B4.
  - NUMERIC (Study 34): the multiplicative law CG2 (u[h00] += Θ·F, one designated monomial per node, rank 3, no matter gear reads Θ)
    at Θ0 = 2^24 hits the Mathieu wall at k = 0 (runaway at t = 1,124 at L = 4, Higgs first); k ≠ 0 lapse tongues are not reachable
    (resonance orders 56 and 71). — A10, A11, B5.
  - NUMERIC (Study 34): at the CHOSEN Θ0 = 2^21 (owner-approved, window-fitted, not forced; h = 2^10 forced by the band rule) CG2 holds
    the J-pure uniform lapse at L = 6: |U| ≤ 4.1·10⁻³ to t = 8,900 (identity 89/89, bits 31), against ONE v1's +0.024 and −0.070 at
    t = 8,000; on S2* it turns the lapse back at 0.0197; every completed CG2 rewind is exact (400 and 1,200 updates at L = 6; 1,000
    and 2,000 at L = 4). Both pre-registered absolute bounds (1.5·10⁻³ and 3·10⁻³) FAIL as worded. — A12, A19, A21′, A23, B6, L6LONG.
  - NUMERIC + DERIVED (Study 34): the size wall: q_M ∝ N, so each Θ0 has a largest safe L, Θ0_max(L) ≈ 3.2·10⁶ × 216/L³ (2^21: L ≤ 6).
    At L = 8 the uniform lapse is pumped (extrema ×5.86, then ×7.07 per hand period); at L = 4 the spring only halves v1's excursion
    in 2,000 updates (−0.0295 against −0.0627; bounded not shown); L0 lumps are not held; the 2^21 hand's turn intervals drift from
    193 to 178 by t ≈ 8,750 (v1 at 2^24: 186–193). — A17, A19′, A20, A24, B7, B8.
  - CHOSEN (both signatures): SAFE AS DEFAULT: NO. ONE v1 stays the default; CG2 at Θ0 = 2^21 is an opt-in NEW LAW candidate, default
    OFF, valid only inside CLOCK_VALIDITY (L ≤ 6, cosmic packet A_c ≥ ~840, Θ0 = 2^21); files `layers/clockgen.py`,
    `../NOTES_clockgen.md`. — CLK-B and CLK-A signatures.
  - OPEN: a size-independent law (Θ0 or g_w scaling with L as seed data, or another restoring mechanism, e.g. a loop of two
    non-reciprocal designated arms and a new gear); whether the M1/M2 readers count as clock parts (an owner question); L0-rich seeds.
    — A14, A15, verdict.
  - DERIVED (this note, checked by Study 34): my design constraints held as follows: (ii) the additive drive cannot bound k = 0
    (confirmed); (iii) the Mathieu concern is real at k = 0 and sets the size wall, while k ≠ 0 tongues are out of reach; (iv) the law
    reaches only lapse readers, not the doublet's rest clock (P5).
- **Why it matters.** It is the owner's chosen direction (one law, through the clocks only), and the only candidate fix found for the
  default's main open stability problem (P2); today it works in a window, not generically.
- **Next step.** Rec 1. **Needs.** NEW LAW + OWNER (the size rule; the M1/M2 question). **Difficulty.** L.

### <a id="p2"></a>P2. The default's main open stability problem: the massless uniform (k = 0) lapse
- **Problem.** In ONE v1 the uniform lapse has no restoring force and integrates the board's net source twice; the source changes
  sign and grows, so |U| reaches 0.186 by t = 9,869 at L = 6 and is still accelerating; |U| = 1/4 ends any run.
- **Known.**
  - THEOREM (identity B6′): D·Σ_x[F(t+1) − 2F(t) + F(t−1)] = 2Σ_x s + Σ_x(r − r′); the k = 0 lapse is exactly massless (c_self = D),
    so any net source drives it with no restoring force; by G-NOGO-a, Σ_x s(t) is not constant. — `THE_ALGEBRA.md` §5.5a, §5.5e,
    §6.1; `records/s11_AGREE_CL2.md` row 6.
  - NUMERIC (Study 30, final; s30/ONE-LONG_RESULTS.md, research record): ONE v1, J-pure, L = 6: no runaway in what could be run
    (to t = 9,869), but not quiet: the pre-registered 4-bit onset metric fired for em (t = 2,621), β (2,931) and the metric (6,752),
    and E1 reaches the 32-bit bound by t ≈ 8,000. U rises ≈ t² to +0.0243 near t ≈ 4,150, crosses 0 near t ≈ 6,050, then accelerates:
    −0.070 (t = 8,000), −0.123 (9,000), −0.186 (9,869). The net source is positive up to t ≈ 3,000, then negative and growing
    (−7.7·10¹⁰ to −3.8·10¹¹ per update). The identity holds with 0 failures; c_fit/c_pred = 0.96 (t ≤ 3,000) and 1.07 (whole run).
    S2*: −0.037 at t = 1,200, faster than t². L = 8: ≤ 0.0038 to t = 1,998 (c roughly ∝ S/N). POST HOC extrapolation, not run:
    |U| = 1/4 near t ≈ 10,500 at L = 6.
  - NUMERIC: the long v1 rewinds (6,300 and 1,200 high-bit updates) were not completed, so their exactness is not determined; every
    completed rewind was exact (1,200 updates at L = 6 in Study 22; 720 at L = 4 in Study 30).
  - NUMERIC (Study 28): with an L0 lump (A = 2^12) at L = 6 the uniform lapse reaches U = 0.043 by t = 400, with or without the
    Einstein layer, which adds two more uncompensated uniform modes (a2, a3). — `records/s28_AGREE_EINF.md` A-V1R-a, B12. NUMERIC
    (Study 30): in the rejected coupled build the Θ-scaled source averaged out (|U| ≤ 3.2·10⁻⁵ up to its runaway).
  - DERIVED: the drift makes the sourced field non-static (the sourced-field redshift test FAILED by 34 %); a spring on the uniform
    lapse screens gravity (an on-site margin of 0.009 D gave a Yukawa range of 4.3 sites and pushed the corner mode out); a static
    background datum (R-a) cancels at most the time mean of the source (this note); cosmological deceleration FAILS in the approved
    law. — `THE_ALGEBRA.md` §5.3a, §5.5e, §5.6(iii); `records/s8_AGREE_B.md` B3, B8; STAB R14; `../NOTES_gravity.md` F4b.
  - OPEN: a law that bounds the k = 0 lapse at every L without screening gravity (P1: CG2 does so only for L ≤ 6).
- **Why it matters.** Every gravity observable sits on the moving mean, U = 1/4 ends any run (L0's link factor flips there), and with
  L0 matter the run lasts only hundreds of updates.
- **Next step.** Rec 2 (measure and attribute), Rec 1 (the candidate fix). **Needs.** OWNER; a k = 0 law is a NEW LAW.
  **Difficulty.** M (diagnosis), L (fix).

### <a id="p3"></a>P3. Masses from the clicks (the owner's principle) versus masses as data
- **Problem.** The owner's principle is that masses must come out by themselves in the clicks; the signed records say that only the
  dark lattice-scale levels do, and that every visible mass value is written in.
- **Known.**
  - CHOSEN (owner): masses must come out by themselves, i.e. be measured as rest click rates, never read off a parameter.
    THEOREM: a mass is a rest clock rate (cos w0 = μ(0)/2); NUMERIC: at amplitude ~1 the rate locks to a rational, so a clock shows
    its rest rate only at amplitude ≫ 1. — s35/README_STUDY.md (research record); `THE_ALGEBRA.md` §4.3, X38.
  - THEOREM + NUMERIC (Study 35, signed by both, 0 disagreements): with nothing put in, the board makes nine rest levels, all dark
    and at the lattice scale (the lightest 0.068 per update), fixed by the cube's group and the signs and measured in the clicks to
    10⁻⁷; the 90° level is click-silent. "Comes out by itself" applies only to these levels and 0. — `records/s35_AGREE_MASS2.md`
    Part III 1–2, 8.
  - THEOREM (THEOREM E): identical clocks with symmetric data stay identical bit for bit, so they cannot split themselves; couplings
    split a rate only by the integer written; nonlinear dressing is seed data; a FORCED Koide relation is impossible (it can only be
    written in). — Part III 3, 7.
  - NUMERIC: the doublet's mass is the integer 2yv = 4915·2^22, seen exactly in the clicks; the clocks reach no vev (from Φ = 0 the
    Higgs runs away). NUMERIC (built): a massless clock riding a seed condensate ticks at a light rate (within 1 %), but its value is
    the chosen coupling × the seed amplitude², i.e. data. — Part III 4–5.
  - THEOREM (THEOREM K): the wall is information: the ≈ 39 bits that fix the lepton ratios must be written in once, as tensor
    integers (today) or as seed amplitudes. — Part III 6; `records/s21_AGREE_MASS.md` Part III 3.
  - NUMERIC + THEOREM (Study 21): Koide holds to 2·10⁻⁶ (−0.43σ; chance p ≈ 10⁻⁴–10⁻³) but cannot be placed on the approved board;
    a one-number NEW LAW (cyclic copies + a (1+i) √-Yukawa + a gauged family index; m_τ = 1776.969 MeV) is not recommended.
    — `records/s21_AGREE_MASS.md` Part III 4–8.
  - OPEN: the click reading of the silent λ = 0 level; the dressing mechanism (≈ 89 % through the doublet's own weak current,
    ≈ 11 % through the Higgs; the value stays data); a stabilized flat-Higgs variant (the naive one fails). — Study 35 closing items.
- **Why it matters.** It is the owner's principle and the widest gap to nature: ~39 bits of lepton data and twelve decades of scale
  are inputs, and Study 35 shows where they must be written.
- **Next step.** Rec 3. **Needs.** NEW LAW + OWNER for any law that fixes values. **Difficulty.** L.

### <a id="p4"></a>P4. The coupled build C1: rejected by the owner, runs away; kept for the record
- **Problem (record).** The doublet × hand coupling, approved at 15:26 UTC and the default until the owner rejected it (matter must
  not read the cosmic clock), runs away. Switched in this release: ONE v1 is the default; the coupled build is an explicit opt-in.
- **Known (for the record).**
  - NUMERIC (Study 30; s30/ONE-LONG_RESULTS.md): at L = 6, J-pure, C1 is bit-identical to Study 22's run for 1,200 updates, stays at
    24 package bits to t = 1,530, then runs away (433 bits at t = 1,554, after 8 turns), chiral/Higgs first; at L = 4 it runs away
    at t = 666 (reproduced by both Study 28 twins). Both rewinds across the runaway are exact, ledgers 0. The package alone and ONE
    v1 do not run away. POST HOC diagnosis: a forced 1:1 pumping of the Higgs by the sign-changing Θ factor against the unscaled
    Higgs spring, then a quartic blow-up; not a 2:1 parametric resonance. — also `records/s28_AGREE_EINF.md` A19.
  - THEOREM + NUMERIC: the coupling wall is E1 (rank 5 for the dressed source; g_A = ±1 on links; the odd coefficient 9), so E1 was
    left unscaled, and its dressed-continuity residual grew up to ~475× the hands-ON baseline; exact coherence including E1 fails at
    any Q. Only Θ0 = 64 was integral at today's mass (below the 2^8 bar); option C2 (Θ0 = 256, mass 4916·2^22) cut the copy split
    to 0.06–0.24 Θ0 (C1: 0.19–0.94) but needed an unapproved mass change. — `records/s22_AGREE_ONE.md` R3, R22, OB3–OB6.
  - DERIVED (this note), the lesson for P1: a time-dependent factor on couplings whose second-order partners are unscaled can pump
    those partners, so every clock law needs a Floquet check over one hand period before any long run.
- **Why it matters.** It is the negative result that shapes the clock law (P1).
- **Next step.** None for the switch: in this release (Study 33) `one_system()` defaults to `couple_doublet=False` (77f6d251…), the
  opt-in still builds C1 bit for bit (593753fa…; test O12), and the code, NOTES_one and README call it a rejected candidate kept for
  the record. **Needs.** Nothing new. **Difficulty.** S.

### <a id="p5"></a>P5. The doublet's FIX-i equivalence-principle debt
- **Problem.** In the default the visible Dirac doublet neither feels nor sources the lapse at rest, so the equivalence principle
  holds only for the dark board L0.
- **Known.**
  - NUMERIC: under a uniform U = ±1/128 the live Dirac rest input changes by exactly 0 (the bare m + 6w and the Yukawa × Higgs terms
    are undressed); its rest-energy source into h00 is exactly 0; all 768 lapse reads into the doublet are hop terms.
    — `THE_ALGEBRA.md` §5.2, §4.7.
  - CHOSEN: FIX-i (λ_H = λ_L = 0) is a coefficient choice, adopted as a declared trade: stable, with this first-order debt. THEOREM
    + NUMERIC: the earlier lapse × |Φ|² dressing coupled the marginal uniform lapse bilinearly and ran away (k = 0 eigenvalue 1.138).
    — `THE_ALGEBRA.md` §7.5, X33–X34; `records/s18_AGREE_STAB.md` R5, R18.
  - DERIVED: the trilemma at today's integers: an untuned stable lapse, the EP at O(U) for Higgs-generated masses, exact local SU(2)
    with gravity on; pick two (FIX-i keeps the first and the third). Form C on the doublet is EP-exact but breaks SU(2) at O(U);
    route (c) is below the integer grain; FIX-C / FIX-C+ are TUNED. — §7.5; `../AGREE_STAB_2026-11-10.md` R12–R17.
  - NUMERIC (Study 28): the covariant lapse × Yukawa dressing exists in the approved narrow kind at rank 4, but its coefficient is
    0.197 per unit Higgs, below the integer grain in ONE v1 (a GRAIN wall); in the coupled build it would be degree 5 (a RANK wall).
    — `records/s28_AGREE_EINF.md` (both-bases table).
  - Also outside the lapse: gauge-layer matter and E1 (η = 1), OD4 spring energy (THEOREM, degree count), the cosmic matter (OPEN).
    Free fall read from clicks FAILS (12 %); β_click = 1.0059 is a marginal FAIL. — `THE_ALGEBRA.md` §5.2, §5.3d.
- **Why it matters.** Visible matter is outside the gravitational sector of the default: Einstein tests with visible matter are void,
  and a clock law through the lapse (P1) cannot reach the doublet's rest clock, until the debt is resolved or declared permanent.
- **Next step.** Rec 4. **Needs.** NEW LAW + OWNER (any re-parametrisation). **Difficulty.** L.

### <a id="p6"></a>P6. Full Einstein: G-NOGO-a, the missing Bianchi identity, and the opt-in linearised layer
- **Problem.** The full Einstein equations G_μν = 8πG·T_μν are not reproduced; two theorems of Rule3 forbid their exact form, and the
  opt-in layer holds only their linearised, diagonal, gauge-fixed form for L0.
- **Known.**
  - THEOREM (G-NOGO-a, four proofs): no reciprocal (b-only, one-potential) gravity coupling of ANY rank has an exactly conserved
    source. THEOREM: the fixed kinetic coefficient D admits no time-dependent gauge symmetry, hence no exact Bianchi identity and no
    exact Hamiltonian constraint; both hold at any rank. — `THE_ALGEBRA.md` §5.5a–b; `records/s10_AGREE_ST.md` S1;
    `records/s11_AGREE_CL2.md` rows 2, 5; `records/s23_AGREE_R5.md` RB2.
  - THEOREM + NUMERIC (Study 28, signed by both twins, no DISAGREE): the opt-in, default-OFF layer (`layers/einstein.py`,
    `../NOTES_einstein.md`) carries linearised Einstein in harmonic gauge for all ten metric components on the one cone, exact as
    integer identities (dispersion, reader factors, reciprocity of every new reciprocal coupling, constraint propagation), coupled
    to the dark L0 only, in the diagonal sector; law audit PASS on both bases (rank 4, B3, 5,328 new terms).
    — `records/s28_AGREE_EINF.md` A21, verdict.
  - NUMERIC: it agrees with GR only for constraint-satisfying data and a conserved source, and neither holds: the constraint is not
    imposed, and the measured source defect is 0.44–0.82 of the source per update in the time part (0.004–0.019 in the space part),
    so sourced waves carry up to 6 polarisations (GR: 2). DERIVED + NUMERIC: γ = 1 for dust, given the CHOSEN board reader; β = 1
    for static fields for L0 through a one-way read (perihelion 1 × GR with it, 4/3 without). — A6′, A10, A11, verdict.
  - THEOREM walls: felt gravitomagnetism and off-diagonal stress for second-order matter (any rank); springs and plaquettes as
    sources (rank 5); the visible doublet (P5). NUMERIC + OPEN: the ghost-sign gears (DeWitt signs −1 on a3 and h0i) propagate
    with no ghost-specific growth in the Krein test of record; Krein at lattice-scale k is OPEN. — A14, A22, B5.
  - OPEN: the finite-rank Deser question; the gravity-source re-decision (the HYBRID source failed its reversor test H2 and stays
    default OFF). — `THE_ALGEBRA.md` §5.5b, §5.5d.
- **Why it matters.** "Full Einstein" is the owner's stated goal; the honest target is a quantified approximation (§5), and the layer
  stays default OFF until its open stability items are settled.
- **Next step.** Rec 5. **Needs.** NEW LAW for any coupling beyond the layer; OWNER for the gravity source and for switching the
  layer on. **Difficulty.** L.

### <a id="p7"></a>P7. Light bending: run on the opt-in layer, not in the default
- **Problem.** The default has no massless field that reads the lapse; bending now runs only with the opt-in layer's test lights.
- **Known.**
  - DERIVED: n − 1 = 2U + 6U² with the link factor 1 − 4U, against U + (3/2)U² for the 1911 control; the deflection ratio is exactly
    2 at first order. THEOREM: exact Gauss + bending at E1's stencil is impossible (exact over Q). — `THE_ALGEBRA.md` §5.3b.
  - NUMERIC (Study 28, pre-registered, base-independent): L = 56, the field built by the board from a static dust load (a designated
    one-way load), one-way test lights (full reader vs an h00-only control): Shapiro ratio 2.02–2.06 (b = 2–8) and bending ratio
    2.08 (b 2–6) and 2.16 (b 4–8), both PASS, the excess over 2 being the predicted O(U) term; beyond b = 10 the ratio falls to
    1.95–1.85 (OPEN). — `records/s28_AGREE_EINF.md` A6′, A8.
  - OPEN: whether the default should carry a lapse-reading light: bending with a Gauss ledger, or exact Gauss with flat light for E1.
- **Why it matters.** Bending separates γ = 1 from the 1911 value; it is now checked on the board, but only with test lights.
- **Next step.** Rec 5: the large-b fall-off at larger L. **Needs.** OWNER (a light that reads the lapse in the default). **Difficulty.** M.

### <a id="p8"></a>P8. Frame dragging and gravitational waves
- **Problem.** Frame dragging is impossible for second-order matter, and the board's own radiation differs from GR's.
- **Known.**
  - THEOREM (Study 28, any rank): felt h0i for second-order matter (L0, light) would close an a-read cycle, so there is no
    gravitomagnetism and no frame dragging for L0 or light; a designated one-way SOURCE of h0i is legal but not built (CHOSEN).
    — `records/s28_AGREE_EINF.md` A14, A14′.
  - NUMERIC: two polarisations in lattice momenta for constraint-satisfying data, up to six for sourced waves (P6). Earlier, with a
    prescribed quadrupole in the default: front 0.583 against c_Q = 0.577, 1/R within 10 %, h×/h+ 0.86–0.99 (FAILS ±5 %).
    — A21; `THE_ALGEBRA.md` §5.5f.
  - DERIVED (Study 28 verifier, not run): a single L0 clock at rest radiates h̄00 waves at 2w0 from its oscillating one-time source
    (GR: none, by Birkhoff); parallel co-moving light beams attract on the board (2EE′; GR: 0). — EINF-B proposals M-1, B-1.
  - OPEN: emission by the board's own matter, the quadrupole formula, energy loss, back-reaction; frame dragging for first-order
    matter (not built). — `THE_ALGEBRA.md` §5.5f.
- **Why it matters.** Radiation is where the board's non-conserved source shows directly, and where it departs from GR.
- **Next step.** Rec 5 (monopole radiation, polarisation content, the beam–beam test). **Needs.** NEW LAW for any further coupling of
  h0i or hij. **Difficulty.** L.

### <a id="p9"></a>P9. Remainder freshness (Born statistics)
- **Problem.** Born's rule is exact on the board only for a fresh, uniform remainder, and nothing in the law supplies freshness.
- **Known.**
  - THEOREM: with a uniform remainder P(carry) = K/D exactly; one shared remainder and one overflow give P(both) = 0. THEOREM +
    NUMERIC: re-reading one circle gives the Fréchet joint P11 = max(0, 2p − 1) and Sturmian (bounded, not √n) noise. OPEN:
    freshness, and one quantum ↔ one click. — `THE_ALGEBRA.md` §4.6; `records/s12_AGREE_GU4.md` rows 2, 5, 6, Y1; GU X10.
  - CHOSEN: in ONE the Born weights p/S_L are seed data (static loads). NUMERIC: max |N+/(N+ + N−) − p/S_L| = 3.2·10⁻⁷ over 216
    nodes, each with ≥ 10⁴ events. — `../NOTES_one.md` declaration 3; `records/s22_AGREE_ONE.md` R12.
  - DERIVED (this note, from R12's numbers; no new run): for any p not extremely close to 0 or 1, independent draws would scatter the
    frequency by ~10⁻³–10⁻² at 10⁴ events, so a maximum of 3.2·10⁻⁷ means the pair counts are deterministic rates
    (N+ = ⌊(tok + ΣK+)/D⌋), i.e. sub-binomial: exact frequencies, not independent outcomes.
- **Why it matters.** "Born" in the picture means exact frequencies; quantum statistics also need independent outcomes (X10).
- **Next step (cheap, read-only).** On ONE v1's pair records: per node Δ_N = N+ − (p/S_L)·N against N, the lag-1…10 autocorrelation
  of outcomes, and an i.i.d. control with the same p and N. PASS ("Born statistics"): Δ_N/√(N·p(1 − p)) has an across-node variance
  in [0.8, 1.25] and |lag-1 autocorrelation| < 3/√N. FAIL (expected): record "exact frequencies, sub-binomial statistics" as
  NUMERIC, then ask in a separate variant whether a symmetric chaotic input into both pair arms (K+ − K− = D·I kept exact) makes
  the remainder walk fresh.
- **Needs.** Nothing for the test; a NEW LAW for any freshness source. **Difficulty.** S (test), M (design).

### <a id="p10"></a>P10. Bell, entanglement and Pauli; free choice versus determinism
- **Problem.** On one board spacelike Bell correlations cannot exceed 2, and Pauli exclusion and true entanglement are missing.
- **Known.**
  - THEOREM: |S| ≤ 2 under measurement independence; no-signalling is the B3 cone theorem; Tsirelson's 2√2 follows only from four
    declared reader laws. NUMERIC: S = 1.18–1.26 with and without Θ, against 2.07–2.42 in loophole-free experiments.
    — `records/s14_AGREE_BELL.md` D-final; `records/s20_AGREE_ZT.md` T4; `THE_ALGEBRA.md` §8.
  - THEOREM + NUMERIC (Study 27, signed by both, 0 disagreements): the owner's no-freeze rule is built exactly for one quantum (one
    emission click, the wave on both paths, exactly one absorption click, Born exact, the backward trace exact). For a Bell pair
    with a typical seed S ≤ 2 exactly (5/4 with independent path tokens; 1.3M full-board runs): without a freeze, click time is board
    time, so the cone gives locality and fresh choosers give measurement independence. — `records/s27_AGREE_B27.md`, joint answer.
  - THEOREM + NUMERIC (Study 27): S > 2 appears only by selection. Discarding unconfirmed pairs is the detection loophole (22/9 and
    2.4677 on two boards). A seed law that only confirmed histories exist is retrocausal = superdeterministic on this bijective
    board: it breaks measurement independence (δ = 4/9 and 0.28), is fine-tuned (at most e^(−0.0214N) of seeds for 2√2), has no
    no-signalling theorem and no Tsirelson bound in any reading, and in its natural form gives the wrong curve (E(0) ≈ 0.83) with
    100 % detector efficiency. A forward confirmation makes every record that uses the far setting timelike to it, so it FAILS
    against timing-margin tests (margin > 1.73, the board cone along an axis). — joint answer; s27/BELL-Y_PROPOSAL.md.
  - CHOSEN (the owner's position): "there is a choice for the click, so the universe is not deterministic", unlike 't Hooft's
    deterministic cellular automaton. NUMERIC: the click outcomes are set by free seed data (tokens) that nothing else fixes: the
    hand, the matter, Δ and every package gear stay bit-identical for 1,200 updates while 98.2 % of the pair outcomes differ.
    THEOREM: Rule3 is a bijection, so the full seed fixes every click; the freedom is the free seed data. THEOREM: free local
    choices alone do not lift S ≤ 2 (outcomes that depend only on local settings and local free data form a local model).
    — `records/s22_AGREE_ONE.md` R13; `THE_ALGEBRA.md` §1.3, §9.5; `records/s23_AGREE_R5.md` N1 (corollary).
  - THEOREM: Pauli, the exchange sign and spin–statistics are missing on one board; true entanglement needs a joint amplitude on
    configuration space (×1.26·10⁷ per added quantum at L = 64), which is not B3-local. NEW LAW (approved target, separate variant
    first): Pauli by orbital copies with wedge readers, then configuration space. — `records/s16_AGREE_PA.md`;
    `records/s16_AGREE_EN.md` Z8; `THE_ALGEBRA.md` §7.6.
- **Why it matters.** "Bell stands" is the owner's explicit goal; under the owner's own rules (no freeze, no-signalling from the law,
  a free choice for the click) one board cannot deliver it.
- **Next step.** A separate configuration-space candidate at L = 3: two quanta (1,296² ≈ 1.7·10⁶ exact amplitudes), non-diagonal
  readers, a joint Born read; tests: S at the optimal settings against 2√2, both marginals exactly setting-free, rewind exact; Pauli
  copies (ONE v3) first, in the approved order. Study 27's other open items: the forward-confirmation timing test on the board and
  the absorber-first variant F0, each recorded as FAILS-or-PASS against the published timing margins.
- **Needs.** NEW LAW + OWNER: a configuration space is a second board, excluded from the reference model (AGENTS.md item 8) and
  allowed only as an explicitly separate candidate. **Difficulty.** L.

### <a id="p11"></a>P11. Quarks and gluons are not connected
- **Problem.** The colour (su3), weak (su2) and hypercharge (u1) gauge layers are built but isolated; no quark carries colour.
- **Known.**
  - NUMERIC (census): 228 of the 382 channels per node (≈ 60 %) read nothing and are read by nothing (su3 168, su2 40, u1 20).
    THEOREM: separate SU(3), SU(2), U(1) link factors on one quark-doublet hop give a degree-5 term (rank 5, FORBIDDEN); the rank
    rule forces ONE merged M6(C) link (72 per face). — `records/s26_AGREE_CH.md` A4, B-II; `records/s11_AGREE_CL3.md` row 17.
  - OPEN: no quark hop is built; one Standard-Model family needs ≈ 817–1,057+ channels per node (≈ 353–461 with a new rank-4 kind,
    NL4); strong dynamics. NUMERIC: the gauge layers' tested amplitude regime is low (u1 matter at 2^20 runs away at t = 3).
    — `records/s26_AGREE_CH.md` A11; GU §11.3 (11); `../README_v1_draft.md` §9.
- **Why it matters.** About 60 % of the node is inert, and the hadronic world (confinement, colour singlets) is absent.
- **Next step.** Build the merged M6(C) quark-doublet link as a separate default-OFF block; pre-registered checks: B3, rank 4, vacuum,
  rewind, local SU(3)/SU(2)/U(1) Gauss with 0 failures, a marginal linear spectrum; then one quark doublet on it at small amplitude.
- **Needs.** The M6(C) link belongs to the approved route-B law; connecting quarks to the default is an OWNER decision. **Difficulty.** L.

### <a id="p12"></a>P12. Three families
- **Problem.** The node carries one family; three families can only be added as chosen copies, not derived.
- **Known.**
  - THEOREM: no natural family 3 on the node (every 3 is the axis triple, giving (m1, m2, m2) and no mixing, or the bosonic triple
    split 1 + 2); three is the minimum for CP (Im det[H_u, H_d] is an exact even integer, ≡ 0 for two families).
    — `records/s16_AGREE_FA.md` Part III; X3.
  - NEW LAW (approved build target ONE v3, separate variant first): three copies (384 = 128 × 3 channels) + a complex bidoublet;
    links family-blind, rank unchanged; +256 channels per node, 18 or 36 Yukawa integers; not built (the `families` hook raises).
    Reading (accepted by the manager): approved for a separate variant, not for ONE, which reconciles `../NOTES_one.md` §7 ("not
    approved") with `THE_ALGEBRA.md` §7.6 and §10.4 ("approved build target").
- **Why it matters.** CP violation in the quark sector needs three families; without them the flavour sector is empty.
- **Next step.** Build ONE v3 as a separate variant; checks: rank 4, B3, rewind, GIM exact in the gauge sector, the CP invariant as
  an exact integer. **Needs.** NEW LAW (approved as a target for a separate variant). **Difficulty.** L.

### <a id="p13"></a>P13. Route B: the photon is slower than c_Q
- **Problem.** The route with exact local SU(2) × U(1)_Y has no photon on the one cone.
- **Known.**
  - THEOREM: one light on c_Q with exact Gauss is impossible under the current rules (T3 rank obstruction; T4 a non-compact B cannot
    gauge a charged Higgs; T5 compact links exactly on c_Q melt). — `THE_ALGEBRA.md` §7.4; GU §6.2b.
  - NUMERIC: the route-B build has a frozen photon (7.6·10⁻⁴ c_Q); the best band-legal relayed plaquette gives 0.408 c_Q; the
    ceiling is c_Q/√3 for the built layout; sin²θ_W(on-shell) = 0.161; in route B the visible doublet has no path to the lapse. OPEN
    (unfrozen scratch): a cyclic-plane layout needs one relay (ceiling c_Q/√2). — `../NOTES_electroweak_b.md` EWB5, EWB6c;
    `records/s26_AGREE_CH.md` B1; s25/REVIEW_ARCH.md R-c.
  - DERIVED: a photon slower than gravity is contradicted by GW/light timing (~10⁻¹⁵); the missing law (a plaquette without relay
    inertia) needs a B3 exception or a second divisor, both against fixed rules. — `../NOTES_electroweak_b.md` (trade-off C).
- **Why it matters.** It forces the route-A / route-B trade-off: E1 on the cone with only global hypercharge (local t1/t2 Gauss fail,
  54/81), or exact local electroweak symmetry with slow light.
- **Next step.** Scan the one-relay cyclic-plane layout (exact, band-legal; report v_γ/c_Q) and give the route-B doublet the FIX-i
  singlet-half lapse hop (an existing kind; STAB battery); take the fixed-rule question to the owner only with those numbers.
- **Needs.** OWNER (a fixed rule) for light on c_Q; the scan needs nothing new. **Difficulty.** M (scan), L (law).

### <a id="p14"></a>P14. Falsifiable predictions that were never measured
- **Problem.** Several predictions of the law are derived but have not been measured.
- **Known.** DERIVED: P(no click) = 1/Q at odd Q (`THE_ALGEBRA.md` §4.6). DERIVED + NUMERIC (two codes, on the law): the
  lattice-scale redshift δ/(U·w0²) → −1/12 for L0 and −1/3 for Dirac (§5.3e). DERIVED: E1's Newton-III lattice defect
  δ ≈ 4·10⁻⁴·(2/w)^1.8, whose decisive test N15 is NOT DETERMINABLE (floor 6·10⁻³ against δ_pred = 8.6·10⁻⁴;
  `../README_v1_draft.md` §8). DERIVED (Study 28): monopole radiation at 2w0 and parallel-beam attraction (P8). The candidates of §5.
- **Why it matters.** They are the cheapest way to expose the board to falsification without a new law.
- **Next step.** Count P(no click) exactly at small odd Q (3, 5, 101) on a matched pair; repeat N15 with a readout floor below
  δ_pred (smaller w and longer averaging); pre-register each. **Needs.** Nothing. **Difficulty.** S–M.

### <a id="p15"></a>P15. Thirteen committed results with pre-FIX-i values
- **Problem.** 13 tracked result files predate FIX-i (14:45 UTC) and carry its old values (e.g. 18,623 monomials instead of 18,553).
- **Known.** NUMERIC: `results/system/` v2_default, v2_ppp, v2_noL0lapse, v2_c2_on, v2_compact, v2_P2p16, v2_od2_variant,
  v2_e1_undressed, v2_W_split_contrast, v2_beta_marginal_contrast, legacy_ppp_off0, rc2_batch1_checks, and
  `results/universality/T6_composed_default`; FIX-i is the sole cause; 123 other outputs reproduce up to stamps. CHOSEN (manager
  decision, Study 25): keep them, labelled pre-FIX-i in README §10. The FIX-i stability evidence (k-scan, bounded bang seeds) is a
  record (`../AGREE_STAB_2026-11-10.md`), not a package test. — s25/REVIEW_VERIFY.md row 4b; s25/REVIEW_ARCH.md S6.
- **Why it matters.** Re-running the suite gives numbers that differ from the committed evidence.
- **Next step.** At the next authorised results write: regenerate the 13 in a scratch mirror with `-t .`, copy them back in one
  reviewed commit, re-manifest, drop the label; add one package test of the FIX-i linear spectrum at L = 3 (max |λ| ≤ 1 + 10⁻⁶ at
  all 27 momenta). **Needs.** Manager/owner authorisation to write tracked evidence. **Difficulty.** S.

### <a id="p16"></a>P16. Code-label and documentation cleanups
- **Problem.** Frozen code and some docs carry stale labels or metadata; none affects the law or the tests.
- **Known** (s25/REVIEW_ARCH.md S1–S14 and its 15:45 addendum):
  - "owner 15:4x UTC" relay stamps in `layers/one.py`, `tests/test_one.py` and `demos/one/run_one.py` (by `date -u` the owner
    decisions arrived at 15:24:47 and 15:26:41 UTC): relabelled in this release by Study 33, except the WHY_COUPLE designation
    reason, which stays verbatim because the tensor fingerprint hashes it (the current status is a separate COUPLING_STATUS).
  - `layers/electroweak.py`: `info["electroweak_lapse"]`, the gwb `params["option"]` and the "Higgs sets the clocks" docstring still
    describe the norm terms FIX-i zeroes (S2); `layers/system.py`: `beta_form="detuned"` silently stays marginal when
    `matter_lapse="split"` (S3); `demos/system/zq8_c2.py` has `LAM = 2` while its evidence `Z_*.json` used lam = 4 (S4).
  - The package tests write evidence into `results/` in place (test_core, test_em, test_gravity, test_choice, test_system,
    test_seed, test_l0c, …), so an in-place run re-stamps tracked files (S5). Also: a hard-coded absolute checkout path in
    `o6_u6_stability.py` (S7); one non-English character in `STAGE1_MANIFEST.md` line 45 (S12); the unapplied q-lattice docstring
    patch for the package's `core/tensor.py` (README §9).
- **Why it matters.** Wrong stamps and stale metadata are the drift that later reads as a fake; test side effects rewrite evidence.
- **Next step.** One reviewed edit of the kinds AGENTS.md allows (tests, docs, labels): the electroweak strings fixed; tests write to
  a temporary directory unless a flag asks for `results/`; `zq8_c2.py` reproduces its evidence (or the evidence is regenerated at
  lam = 2, saying so); no tensor changed. PASS: fingerprints b51d3f2c… (package), 77f6d251… (ONE v1) and 593753fa… (the rejected
  opt-in) unchanged; test_one and the package suite (`-t .`) green in a mirror. **Needs.** Nothing (no law change). **Difficulty.** S.

---------------------------------------------------------------------------------------------------------------------
## 3. Recommendations: the five most valuable next studies, in order

**<a id="rec1"></a>Rec 1. A size-independent clock law, or Θ0(L) derived from seed data (P1, P2; L).**
- Plan: (1) two pre-registered routes: (a) set the hand scale (Θ0, or g_w) from seed data by a written rule, so that q_M stays
  inside the Kapitza window at every L (Θ0_max(L) ≈ 3.2·10⁶ × 216/L³), never fitted to a run; (b) a restoring mechanism that does not
  depend on N (e.g. a loop of two non-reciprocal designated arms and a new gear). (2) Law checks first: B3, rank ≤ 4, vacuum, rewind,
  the census showing that no matter gear reads Θ, and a Floquet check at every L tested (k = 0 Mathieu and k ≠ 0 tongues). (3) Runs
  beside ONE v1 on the same seeds (J-pure, S2*, an L0-rich seed) at L = 4, 6 and 8 for ≥ 10,000 updates; observables: U_mean(t), the
  turn intervals, L0 tick rates, bits; the static-load Poisson field with and without the law. (4) The owner's M1/M2 question.
- PASS: |U| bounded (≤ 0.01) at L = 4, 6 and 8 over ≥ 10,000 updates on every seed, with exact rewinds, 0 ledger failures, the
  Floquet check, and the static-load field unchanged within 1 % for r ≤ L/2.
- FAIL: any L pumped or unbounded; the law then stays an opt-in with a stated validity window (as CG2 today), and Rec 2's owner
  options remain. A PASS reaches visible matter only together with Rec 4 (P1, P5).

**<a id="rec2"></a>Rec 2. The default's massless uniform lapse: attribute the source, measure the horizon (P2; M).**
- Plan: (1) ONE v1 at L = 6 past |U| = 1/4 (J-pure and S2*) and at L = 8, 10 to ≥ 6,000 updates, with the exact lapse ledger every
  update and Σs split by block (L0, singlet-half hop, bgk, E1 dressing, gauge and other nonlinear sources). (2) Name the block whose
  net source turns negative near t ≈ 3,000 and keeps growing. (3) Measure (not extrapolate) t(|U| = 0.1) and t(|U| = 0.25) per L
  and seed, including an L0-rich seed. (4) Complete the long rewinds Study 30 could not finish. (5) If Rec 1 fails, an owner choice:
  (a) the k = 0 mode as the board's cosmological mode (confront the deceleration FAIL); (b) a k = 0 restoring law with a declared
  range ≫ L (a massive lapse; NEW LAW; it must vanish at the band corner, as the link form (F_x + F_{x+e})² does, since the on-site
  margin pushed the corner out, and its coefficient must come from the declared range, never from the couplings, since FIX-C was
  TUNED); (c) a declared horizon of the default, written in README §9.
- PASS: the identity with 0 failures; ≥ 90 % of the change in Σs attributed to named blocks; every horizon measured; every long
  rewind completed and exact.
- FAIL: an unattributed source, a ledger failure or a non-exact rewind (a bug: stop and diagnose).

**<a id="rec3"></a>Rec 3. Masses out of the clicks: Study 35's open items under a strict information test (P3; M–L).**
- Plan: (1) Study 35's three open items: the click reading of the silent λ = 0 level (S); the dressing mechanism, i.e. whether the
  ≈ 89 % weak-current channel fixes any ratio by law or only by seed (M); a stabilized flat-Higgs variant (M–L; a NEW LAW). (2) For
  any mechanism, register before the run the ratio(s) it must produce, the tolerance, and the bits it is given: tensor integers AND
  seed amplitudes both count (THEOREM K). (3) Read every mass only as a rest click rate at amplitude ≫ 1; keep a trial ledger as
  Study 21 did, and compute the look-elsewhere-corrected p-value.
- PASS ("a mass came out of the clicks"): the registered ratio is reproduced within its tolerance from inputs carrying fewer bits
  than the ratio's measured precision demands (e.g. ~20 bits for m_μ/m_e at 10⁻⁶), with a corrected p ≤ 10⁻³. Moving the bits from
  tensor integers into seed amplitudes (a condensate, a flat Higgs) does not pass: it relocates the data.
- FAIL: the verdicts of Studies 21 and 35 stand (only the dark lattice-scale levels come out by themselves; visible values are data);
  the attempt goes into the ledger, and the owner chooses where the ≈ 39 bits are written.

**<a id="rec4"></a>Rec 4. Gravity for visible matter: the FIX-i EP debt (P5; M, then L).**
- Plan: (1) an Eötvös test: one static seeded lapse (U ≤ 0.02, k = 0 mean removed), an L0 packet and a doublet packet side by side;
  observables: own-frame (R2) tick ratio and fall acceleration; the tensor predicts √(1 − 2U) for L0 and 1 for the doublet's rest
  clock. (2) The covariant lapse × Yukawa dressing that Study 28 found in the narrow kind (0.197 per unit Higgs): search the integer
  re-parametrisations that make it integral, each an owner decision. (3) Three pre-registered legs per candidate: (i) linear
  spectrum marginal at every L = 6 momentum, corner included (max |λ| ≤ 1 + 10⁻⁶); (ii) no SU(2) breaking beyond the declared E1
  baseline under a non-uniform lapse (t3 0/81; t1, t2 not worse than 54/81); (iii) the doublet's rest input under a uniform
  U = ±1/128 carries the factor 1 − U to first order; then bang seeds to ≥ 1,200 updates.
- PASS: a candidate meets (i)–(iii) with integer coefficients and stays bounded; it goes to the owner as a NEW LAW.
- FAIL: none; the trilemma is recorded as NUMERIC over that class, the owner declares the debt permanent, and gravity tests use L0 or
  test carriers only.

**<a id="rec5"></a>Rec 5. Study 28's open Einstein tests, on the opt-in layer (P6–P8; M–L).**
- Plan (the verifier's proposals): K-2, Bloch–Floquet of the linearised map around a standing-wave L0 background across the
  cone/L0-band crossings, against the sign-flipped control; D-1, the a2/a3 and F uniform-mode growth against the exact k = 0 shift
  law; D-2, the source defect averaged over one 2w0 period; M-1, the far field of a single L0 clock at rest; P-1, the non-TT
  fraction of sourced waves; B-1, parallel against antiparallel test beams; plus bending at b ≥ 10 on a larger L.
- PASS: K-2 max |λ| ≤ 1 + 10⁻⁶ at every k (else the layer stays OFF); D-1 0 failures of the shift law; D-2 the period-averaged
  residual scales as 1/A under A → 2A; M-1 a far-field amplitude ∝ swing/r within 10 %; B-1 the board's own prediction (2EE′ for both
  beam pairs; GR: 0 and 4EE′) within 10 %.
- FAIL: any result outside these bands is a FAIL and is kept; B-1 and M-1 test the board's predictions, which differ from GR, so a
  PASS there confirms the board, not GR.

**Next in line:** the Born-statistics test (P9; S, read-only); the configuration-space Bell variant (P10); the merged M6(C) quark
link (P11); ONE v3 (P12); the one-relay route-B scan (P13); the prediction checks (P14); P15 and P16 (S).

---------------------------------------------------------------------------------------------------------------------
## 4. Settled: do NOT reopen
| settled | label | source |
|---|---|---|
| Rank 4 is final. Rank 5 lifts one degree wall (Θ × lapse-dressed first-order matter hop) to an approximate echo and solves no item exactly; every other item meets a rank-free wall or the integer grain | CHOSEN (owner O1) on a joint THEOREM + NUMERIC verdict | `records/s23_AGREE_R5.md`; `THE_ALGEBRA.md` §3.11 |
| Matter does not read the cosmic clock: the doublet × hand coupling is rejected (and it runs away) | CHOSEN (owner) + NUMERIC | P4; Study 30 (s30, research record) |
| Q odd, given a mirror-fixed vacuum (one vacuum pair {3Q − 1, 3Q}); the value 2^33+1 is chosen | THEOREM (conditional) + CHOSEN | `THE_ALGEBRA.md` §1.6, X30, X39 |
| D = 6 (reference), given K = 2u and six unit ports | THEOREM (conditional) | `records/s26_AGREE_CH.md` A12; X30 |
| The reference engine `universe24/` is unchanged; the variant imports it read-only | NUMERIC (13/13 blobs = origin) | s25/REVIEW_VERIFY.md row 3 |
| Rule3 is an exact bijection with a staged inverse; click = carry; the ledger telescopes | THEOREM | `THE_ALGEBRA.md` §1.3, §4 |
| No exactly conserved reciprocal source and no exact Bianchi identity at any rank: the full Einstein equations cannot hold exactly; work on quantified approximations | THEOREM | `THE_ALGEBRA.md` §5.5; `records/s23_AGREE_R5.md` RB2; `records/s28_AGREE_EINF.md` |
| No felt gravitomagnetism (h0i) and no off-diagonal stress for second-order matter, at any rank | THEOREM | `records/s28_AGREE_EINF.md` A14 |
| Through time alone a cosmic turn is only a universal clock-rate change (no fold or echo of matter); "every clock reads the lapse" is impossible at rank 4; an additive drive cannot bound the uniform lapse; a reciprocal Θ–lapse coupling is forbidden (THEOREM O's Θ row) | THEOREM | `records/s34_AGREE_CLK.md` A2, A3, A8, A13 |
| No freeze: the zero-time hold is dropped (a posted schedule; no b-only rule of any degree generates it on the periodic cube) | CHOSEN (owner O3) + NUMERIC | `records/s23_AGREE_R5.md` B1, RB4; `records/s20_AGREE_ZT.md` |
| One exact CPT bang (THEOREM D); later bangs start new seeds; echoes are data, never targets; an interacting composition never folds exactly (THEOREM O) | THEOREM + CHOSEN (owner O2) | `THE_ALGEBRA.md` §9 |
| FIX-C / FIX-C+ counter-terms are fitted to the couplings and not adopted | TUNED (excluded) | `THE_ALGEBRA.md` §7.5, X27, X35 |
| Bell on one board without a freeze: S ≤ 2 for a typical seed, even with free local choices; superdeterminism predicts nothing (over all seeds S = 4) and is fine-tuned; a settings-only confirmation gives S = 5/4 | THEOREM | X13, X25; `records/s14_AGREE_BELL.md`; `records/s27_AGREE_B27.md` |
| Identical clocks cannot split themselves (THEOREM E): no forced Koide; "three families because three axes" is circular; C0/C1/C2 are arithmetic classes, not evidence | THEOREM | `records/s35_AGREE_MASS2.md`; X3, X4; AGENTS.md item 10 |
| α, θ_W at low energy, the Yukawas and N_c are inputs; 6π⁵, 137 and Wyler-type formulas are numerology, falsified (masses: P3) | CHOSEN + NUMERIC | `records/s21_AGREE_MASS.md` Part III 6 |
| Impossible under the current rules: one light on c_Q with exact Gauss (route B); exact Gauss + bending at E1's stencil; an exact Θ coupling including E1 at rank 4 (any Q); compact links exactly on c_Q (any finite rank) | THEOREM | `THE_ALGEBRA.md` §7.4, §5.3b; OB3, OB6; RB2 |
| Pauli and the exchange sign are missing on one board; the node has no natural family 3 | THEOREM | `records/s16_AGREE_PA.md`; `records/s16_AGREE_FA.md` |
| Odd-Q parity: no carry event has probability exactly 1/2 | THEOREM | `THE_ALGEBRA.md` §4.6, §8 |
| Information: \|K(X_t) − K(X_0)\| ≤ 2 log2 t + O(1); growth beyond that is only in the record (coarse-grained) | THEOREM | `THE_ALGEBRA.md` §9.5 |

---------------------------------------------------------------------------------------------------------------------
## 5. Outlook: can this reach nature?
Lines marked OPINION (manager) are the manager's assessment, not results; every other line keeps its record label.

- **"Exactly", within today's framework: no.** OPINION (manager), resting on two theorems and one fact:
  - THEOREM: no exactly conserved reciprocal source and no exact Bianchi identity, at any rank, so the full Einstein equations cannot
    hold exactly (P6); the opt-in layer holds their linearised, diagonal, gauge-fixed form for L0, with a non-conserved source
    (Study 28). OPINION (manager): nature only requires agreement to experimental precision, so a continuum-limit approximation
    with a Planck-scale grain may suffice; showing that is a research target, not a result.
  - THEOREM: on one board |S| ≤ 2 under measurement independence (P10). Loophole-free experiments violate the bound, so one board
    would need a seed–setting correlation (superdeterminism, as in 't Hooft's cellular-automaton interpretation). OPINION (manager):
    that correlation must be shown to be natural, not tuned, and must give exactly 2√2. THEOREM + NUMERIC (Study 27): with no freeze
    and a typical seed Bell does not stand; the seed-law reading is fine-tuned superdeterminism, and Tsirelson's bound follows in no
    reading. CHOSEN (the owner's position, P10): the click involves a free choice, so the universe is not deterministic; THEOREM:
    free local choices alone keep S ≤ 2.
  - CHOSEN: the constants (Q, the weights, the Yukawas, N_c, the seed) are data, not outputs (X16–X17). THEOREM (Study 35): only the
    dark lattice-scale levels come out by themselves; the ≈ 39 lepton bits must be written in, as integers or seed amplitudes (P3).
- **What would show that nature COULD work this way.** OPINION (manager): one new testable prediction that is then confirmed.
  Candidates in the signed records:
  - subluminal high-energy dispersion with a definite sign: on the one stencil the group velocity is below c_Q in every direction
    near k = 0 (the k⁴ coefficient is negative), with a cubic (Σk_d⁴) anisotropy. — DERIVED (all directions, O(k⁴)) + NUMERIC
    (three directions); `THE_ALGEBRA.md` §5.1a;
  - no gauge-mediated proton decay. — DERIVED, given the CHOSEN Pati–Salam ceiling; `THE_ALGEBRA.md` §7.3;
    `records/s11_AGREE_CL3.md` row 14; `records/s12_AGREE_GU1.md` A13;
  - a forced right-handed neutrino: every matter block is a Cl(1,3) module with both hands (Nielsen–Ninomiya on the board).
    — THEOREM (lattice); `records/s26_AGREE_CH.md` B3; `CHANNELS.md`. Neutrino masses still need a Majorana (J′-flip) NEW LAW or
    more Higgs fields (`records/s16_AGREE_FA.md` Part III 6);
  - "action = reaction" in gravity is not exact: Newton III holds for the reciprocal lapse coupling, fails by definition for the
    designated one-way lapse reads, and an exact Newton III excludes an exactly conserved source. — THEOREM; `THE_ALGEBRA.md` §5.5a,
    §5.6(i), §6.3; `../README_v1_draft.md` §9 (v8-2).
  - Board predictions that DIFFER from GR, i.e. falsifiers of the board: parallel co-moving light beams attract (2EE′; GR: 0) and
    antiparallel ones get 2EE′ (GR: 4EE′); a single clock at rest radiates monopole waves at twice its rest rate (GR: none, by
    Birkhoff). — DERIVED, not run (Study 28 verifier); `records/s28_AGREE_EINF.md` (findings, OPEN list).
- DERIVED (this note): the dispersion's size scales with the lattice spacing, which is an input, so today it predicts a sign and an
  anisotropy pattern, not a size; the proton-decay item is a null prediction, which experiments can falsify but not confirm.
