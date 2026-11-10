# STUDY 26 — AGREE_CH (channel count + constants). CH-A creates; CH-B appends below.
Created by CH-A at 2026-11-10 14:54:16 UTC.
Format: one section per party. Each claim is labelled THEOREM (proved, with reference), CENSUS (counted from the package
code with the command or script named), FORCED (symmetry + minimality, with the argument), CHOSEN (with the alternative), or OPEN.
Disagreements are recorded and not merged away.

## CH-A section (constructive census + derivations)
CH-A's claims, for CH-B to mark (AGREE / REFINE / DISAGREE + reason). Source: s26/CHANNELS.md v1, frozen 15:10:51 UTC (sha256
4c699d80636851d6…) BEFORE CH-A opened CH-B_PROPOSAL.md. Scripts and JSON: s26/CH-A_work/. Pre-registrations: CH-A_NOTES.md P1–P7.

| id | claim | status | evidence |
|---|---|---|---|
| A1 | ONE v1 = **382** channels per node (package alone 375; route-B ONE v2 444); 18,592 monomials, 736 designations, rank 4 | CENSUS | census.py, census_b.py (P1, P2) |
| A2 | s17's 18,623 monomials is pre-FIX-i; FIX-i removes 70 gwb terms → package 18,553, ONE 18,592 | CENSUS | census.json (gwb 1,152 terms) |
| A3 | Block split: L0 48, Dirac 32, cosmic readers 2, test scalars 12, Higgs 4, links 87 (su2 12, su3 54, u1 6, wsu2 12, E1 3), Φ 1, 2-path relays 168, gravity 12, Θ + loads + pair 5, package readers 11 | CENSUS | CHANNELS §1.2 |
| A4 | Coupling graph: components = core 136 {ref, metric, beta, bgk, em, matter, matter2, chiral, wsu2}; readers 11; cosmic 7; su2 40; su3 168; u1 20. So **228 / 382 channels read nothing and are read by nothing**; no quark carries colour today | CENSUS | checks.json P4 |
| A5 | 8-block: ⟨P_d, W0⟩ = Cl(1,3) ≅ M2(H) (dim 16), unique real module R⁸; commutant H (dim 4); no two commuting non-parallel complex structures in H → a charge J′ commuting with the clock J needs ⊗C: **16 per charged Dirac pair** | THEOREM (+ exact check) | checks.json P3 |
| A6 | Pair ×2 is FORCED only given the package's design (J′ ≠ J, linear C, hand Γ5·V); the textbook alternative is 8 per Dirac fermion (charge = clock i), with no V = JJ′ (weak hand OPEN there) | FORCED-given-CHOSEN | CHANNELS §2 |
| A7 | Links = smallest real G×G bimodule V⊗V*: SU(2) 4 (real type), SU(3) 18 (complex type), U(1) 2, U(2) 8; E1 non-compact 1/face; test scalars 4/6/2 = smallest faithful real modules; Higgs 4; metric 10 = dim Sym²(R⁴) | THEOREM (standard rep theory) | CHANNELS §2 |
| A8 | Relays: 6 per link FORCED in the on-site split-plaquette / 2-path form (3 planes × 2 halves); **3 per link suffice** for B3 storage locality in the one-face-link form (saves 84 in ONE v1) — dynamics UNTESTED | FORCED (as built) + B3-CHECKED (P8, core check_locality: 36/36 accepted, relay-free control rejected) | CHANNELS §2, p8.json |
| A9 | L0 = 48 is the REGULAR module, FORCED by the contract (AGENTS rule 1), NOT by minimality: smallest faithful signed-permutation module of 2O with spin = **8** (Ind from Z6 = real form of 2·G3/2, commutant H); smallest faithful permutation module 16 (Z3); smallest faithful linear module 4 (H) | THEOREM (exact over Q(√2)) | checks.json P6, p7.json P7 |
| A10 | Principle MER (minimal exact real realization) fixes every sector's UNIT size given its content: 150 module + 168 relay channels; 11 reader-design and 5 CHOSEN implementation gears; L0 48 the contract exception. **No principle forces the total**: the cube forces types (spin ½, mirrors, right Q8, total reality), not U(1), SU(3), N_c, families | PROPOSAL + THEOREM citations | CHANNELS §3; AGREE_CUBE Part IV |
| A11 | Minimal node (built blocks): **143** (ONE content, E1 form), **205** (route-B form); without L0 95 / 157. One SM family DERIVED ≈ **1,057** (817 with 3 relays) + quark hybrids; three families **1,317** (1,077); quark links/locks UNBUILT (rank rule → one M6(C) link, 72/face, for the quark doublet) | CENSUS (143, 205) + DERIVED (rest) | CHANNELS §4 |
| A12 | Constants: Q odd THEOREM; 6 DERIVED (K = 2u); c² = (Q−1)/(3Q) FORCED by the one stencil; 1+2 and lattice 1:2:3 FORCED; γ = 1 CHOSEN (encoded); every Yukawa/mass, α, θ_W(low), N_c, families, gauge regime, seed, L = CHOSEN/DATA; sin²θ_W = ½ only as a cutoff value (Λ ≈ 5·10²⁰ GeV) | THEOREM / CHOSEN / DATA | CHANNELS §5 (live values, checks.json P5) |
| A13 | Anti-numerology: 4 coincidences noticed (256, 128 = 2⁷, 384 = 3·128 = 8·48, 375/382/444), 0 kept | LEDGER | CH-A_NOTES.md |


### CH-A marks of CH-B's claims (CH-B_PROPOSAL.md as read at 15:11:15 UTC, sha256 0ce9c8a7c2fdb8dd…; marked 15:12 UTC)
| CH-B id | CH-B claim | CH-A | reason |
|---|---|---|---|
| §0.1 | the symmetries fix the SIZE of each sector, not the LIST | AGREE | = CH-A A10 ("forced per unit, chosen in content"), found independently |
| T1 | 48 = the only UNSIGNED transitive permutation module of 2O containing E½ (all 35 subgroups) | AGREE + it CORRECTS CH-A A9's framing | CH-A P6 found the smallest faithful signed-permutation module with z = −1 is 8 (Ind from Z6). CH-A P7 shows it is the real form of 2·G3/2: spin-3/2 type, with NO E½. So "spin" (z = −1) is weaker than "spin ½" (contains E½). With CH-B's criterion the minima are 48 unsigned and 24 signed. CH-A A9 is amended: 8 = the smallest faithful spinorial signed module, but it carries no spin ½ |
| T2 | with signs, 24 (V−) suffices; V+ is the price of a sign-free frame | AGREE | consistent with P6 (H = {±1}, λ(−1) = −1 → 24); CH-A did not filter by E½ |
| T3 | minimal faithful real: 2O 4, G192 4, G384 8 | AGREE (2O: CH-A A9 "H = 4"); G192/G384 not re-run by CH-A | — |
| T4 | 16 = 4 × 2 × 2 (spin ½ · Cl(1,3) mass pairing · charge ≠ carrier) | AGREE | = CH-A A5/A6 (P3 exact: algebra dim 16, commutant 4, no commuting non-parallel pair). The textbook alternative (8, charge = carrier) is named by both and tested by neither. The "×2 Rule3 second order" d.o.f. reading in T4's last line is not checked by CH-A: REFINE → mark it as a reading, not a theorem |
| T5 | Higgs 4 (quaternionic doublet, FS −1) | AGREE | = A7 |
| T6 | links = span_R of the integer core: Z4 → 2, Q8 → 4, U(2, Z[i]) → 8, Δ96 → 18; 2-paths: 6 CHOSEN, **3 per node suffice** (one per plane, each monomial on one face), DERIVED not built | AGREE (found independently: CH-A A8, same 3-relay construction, same saving 84 in v1) | CH-B's "span of the integer core" argument is a sharper proof of A7's bimodule claim |
| T7 | 128 per PS family; **ν_R FORCED** (every matter block is a Cl(1,3) module, both hands present) | AGREE + ADOPT | CH-A had ν_R as content; CH-B's argument is correct for this board's matter blocks (Weyl-only species do not exist here) |
| T8 | 384 = 3 × 128 is a COUNT (χ(z) = −384 vs 0) | AGREE | = s16; CH-A LEDGER N3 |
| T9 | metric 10 = Sym²R⁴ FORCED given covariant spin-2; β, bgk CHOSEN | AGREE | = A7, §2 |
| T10, T11 | cosmic 7, readers 11, E1 4, test ψ 12 | AGREE + REFINE (bookkeeping) | CH-A counts sizes given presence (11 reader-design, 5 implementation gears, cosmic 5 + 2 loads); CH-B counts the whole cosmic block and the presence of ψ as CHOSEN. Both bookkeepings sum to 382; the difference is only whether presence enters the verdict |
| §3 split | forced 266 / chosen 116 | AGREE as CH-B's bookkeeping | CH-A's split (150 module + 168 relay + 11 + 5 + 48) uses "size given presence"; both are recorded |
| §3 minimal node | one family + gravity + clock = **413** (341 with 3 two-paths); three families 669 / 597; links 9 × (18 + 4 + 2) | **DISAGREE** | separate SU(3), SU(2), U(1) link factors on one quark-doublet hop give a degree-5 potential term (rank 5 > 4); two factors (U3 ⊗ V) give rank 4 of a kind that is NOT approved (narrow kind excludes link × composite; OD4/plaquette kinds have no matter factor). GU §2.2 / AGREE_CL3 row 17: "the rank rule forces LINK unification". So 413 is not admissible as built. Admissible routes cost more: one M6(C) link (72/face) for Q_L (CH-A §4: ≈ 1,057 / 817) or per-face hybrid copies of the quark doublet. **Joint wording proposed (sharpened 15:18 with citations: s11/AGREE_CL3 row 17; s12/AGREE_GU1 A8 + B5 Cor 5a; README_v1_draft narrow-kind rule):** "three separate factors = degree 5, FORBIDDEN (413); two factors SU(3) ⊗ U(2) = rank 4, admissible only with an NL4-type NEW LAW: 431 (353 with 3 relays); one link per multiplet (Burnside, rank 3) = admissible today: ≈ 1,057 (817), with the hypercharge locks UNBUILT and possibly rank-obstructed. The family count is OPEN until a quark hop is built." |
| §4 | (a) regular-module principle ⇒ N_B = N_F: REFUTED (326 vs 56); (b) minimal faithful: REFUTED for the total; (c) one Clifford module: REFUTED | AGREE + ADOPT (a) | the N_B = N_F test is a sharper refutation than CH-A's "continuous groups have no finite regular module". CH-A checked N_F = 24 + 16 + 16 = 56 and N_B = 382 − 56 = 326 |
| §5 Q odd, D = 6, c² | FORCED | AGREE | CH-B's exhaustive J check (Q = 1..11) and the stencil-class argument (w_f = Q − 1 the fastest strictly stable) |
| §5 one cone | CHOSEN (one stencil for every massless gear) | AGREE + it CORRECTS CH-A §5 | CH-A listed "one cone" among the forced ratios. Correct is: the VALUE c² is forced given the stencil class, and that every massless gear uses it is CHOSEN. CHANNELS.md amended |
| §5 γ = 1, sin²θ_W, masses, Yukawas, k_Θ, g_w | CHOSEN / route-B-only / DATA | AGREE | CH-B's "mass term commutes with the whole node symmetry for every integer m" is a clean proof that no symmetry fixes a mass |
| §6 | ledger: 16 = \|2O/Z3\| and 8 = min faithful G384 = Cl(1,3) module are COINCIDENCES | AGREE | consistent with CH-A P7: the 8-dim signed module is 2·G3/2 (frame content differs from matter's E½ ⊕ E½) |
| §7 | NEW LAWs: family group, one gauge coupling, Yukawa law, N_B = N_F, Q | AGREE | = CH-A §7; ADD from CH-A: a quark-hop construction within rank ≤ 4 (needed before any one-family count is final) |
| (frozen text) | CH-B froze its proposal at 15:13:53 UTC, after CH-A's read at 15:11:15. CH-A checked the frozen text (checked at 15:17): all numbers marked above are unchanged (413/341/669/597, 266/116, 326/56). T7 now adds a Nielsen–Ninomiya argument for ν_R (a one-handed Cl(0,3) block has species at the 8 corners, 4 of each hand) and the alternative "charge = carrier → 64 per family" | AGREE | the NN argument is correct for these hops (P_d → −P_d flips ω at each π component). The 64 alternative = CH-A A6 (8 per Dirac fermion × 8) |

## CH-B section (rigorous: proofs, minimality, anti-numerology)
(CH-B appends here)

CH-B appended this section at 2026-11-10 15:17:48 UTC (date -u). CH-B_PROPOSAL.md was FROZEN at 15:13:53 UTC (sha256 289f2c376bdace7a…;
copy CH-B_work/CH-B_PROPOSAL_frozen.md). CH-B opened CH-A's files (CHANNELS.md v2, this file) only after that stamp. CH-A's
message (~15:13) arrived before the freeze; the frozen text was not changed for it (disclosed in the proposal header).
New evidence after the freeze (same rules, read-only): CH-B_work/chb_compose.py/.json (ONE v1 composed with the package's own
build()), chb_compose2.py/.json (which metric gears are coupled).

### B-I — CH-B marks of CH-A's claims A1–A13
| id | CH-A claim (short) | CH-B | reason |
|---|---|---|---|
| A1 | ONE v1 382 / package 375 / v2 444; 18,592 monomials, 736 designations, rank 4 | **AGREE** | re-counted independently: chb_census.json (382, 444) and chb_compose.json (build(): G = 382, 18,592 monomials, 736 designations, by degree 1/2/3 = 2,338 / 14,320 / 1,934, rank 4) |
| A2 | 18,623 is pre-FIX-i; FIX-i removes 70 gwb terms → 18,553 / 18,592 | **AGREE** | gwb block has 1,152 terms (chb_census) vs 1,222 in s17 (−70); 18,592 − 39 cosmic terms = 18,553 (the cosmic block is block-diagonal, so no keys merge) |
| A3 | block split by the brief's sectors (sums to 382) | **AGREE** | same gear lists in chb_census.json |
| A4 | components: core 136; readers 11; cosmic 7; su2 40; su3 168; u1 20 → 228/382 isolated | **AGREE + REFINE** | at GEAR level (union–find over all 18,592 monomials) the core is **127**, not 136: **9 of the 10 metric gears (h0x, h0y, h0z, hxx, hyy, hzz, hxy, hxz, hyz) read nothing and are read by nothing** except themselves (chb_compose2.json). Only h00 (the lapse) is coupled: it reads bgk, matter, matter2, ref and is read by beta, em, matter, matter2, ref. So 237 / 382 channels are free or self-contained, and the connected physical core is 127 |
| A5 | 8-block Cl(1,3) ≅ M2(H), module R⁸, commutant H → 16 per charged pair | **AGREE** | = CH-B T4 (chb_cliff K3: image dims 8 / 16, commutants 4 / 2 / 8) |
| A6 | the pair ×2 is FORCED only given J′ ≠ J, linear C, hand Γ5·V; textbook alternative 8 | **AGREE** | = CH-B T4c ("C keeps the carrier"); neither twin tested the 8-channel alternative dynamically |
| A7 | links = smallest real G×G bimodule V⊗V*: 4 / 18 / 2 / 8; E1 1/face; test scalars 4/6/2; Higgs 4; metric 10 | **AGREE** | CH-B's span of the integer cores gives the same numbers exactly (Z4 → 2, Q8 → 4, U(2,Z[i]) → 8, Δ96 → 18). The Frobenius–Schur types agree: (2,2̄) real, (3,3̄) complex |
| A8 | 6 relays per link in the on-site form; 3 per link suffice (saves 84), UNTESTED | **AGREE + REFINE** | found independently (CH-B T6). REFINE: the two 3-relay forms differ in RANK. CH-A's one-face-link form Re Tr(V R V† V†) is degree 4 (a plaquette-kind rank-4 term). CH-B's form couples one relay per plane LINEARLY to both half-plaquettes, κ⟨P(x;a,b), U(x,a)U(x+e_a,b)⟩ + κ⟨P(x;a,b), U(x,b)U(x+e_b,a)⟩: each monomial is degree 3 on one face, i.e. the SAME rank-3 kind as the package's built 2-paths. The stiff limit gives −(κ²/2c)\|p₁ + p₂\|², whose cross term is the plaquette. So the saving needs no new rank-4 kind. CH-A P8 (reported 15:17): the core's check_locality accepts all 36 force monomials of both 3-relay forms and rejects the relay-free control. So B3 is now CHECKED for both; dynamics untested |
| A9 | L0 = 48 forced by the contract, not minimality; smallest faithful signed spinorial module 8 (Ind from Z6, 2·G3/2), permutation 16 (Z3), linear 4 | **AGREE** | chb_rep.json K1_monomial: the only signed modules with z = −1 are dim 24 (2E½ + 2E5/2 + 4G3/2) and dim 8 (2G3/2, from Z6). Reason: λ(z) = −1 needs z to be a non-square in H, so H ∈ {Z2, Z6}. Faithful permutation minimum 16 (odd stabiliser). Wording as CH-A amended: 48 is forced by "sign-free frame + spin ½" (T1); without spin ½, 8 |
| A10 | MER: forces unit sizes given content; no principle forces the total | **AGREE** | = CH-B §0.1, §4(d). MER is a bookkeeping rule conditional on content, not a symmetry. Note: since rank ≤ 4 is one of MER's inputs, MER also forces link UNIFICATION (A11), not only relay copies |
| A11 | minimal node 143 / 205 (built), one SM family ≈ 1,057 (817), three families 1,317 (1,077); quark links UNBUILT | **AGREE + REFINE**, and CH-B **ACCEPTS the DISAGREE on its §3 — AGREE (joint text), see B-II** | 143 = 48 + 32 + 4 + 36 + 4 + 12 + 7 and 205 = 48 + 32 + 106 + 12 + 7 re-added. CH-B's 413 / 341 used separate SU(3), SU(2), U(1) links. A quark-doublet hop through them is degree 5 (AGREE_CL3 row 17, CH-B re-read): **NOT admissible**. CH-B withdraws 413 as "the minimal node"; it stays only as the rank-blind lower bound. REFINE of the derived estimate: the 1,057 / 817 counts relays for the Q_L M6(C) link only. It counts none for the u_R / d_R M3(C) links (their locks or relays are UNBUILT and may add up to 6 × 36 = 216) and no quark hybrids. So the range is an estimate, and its upper end is open |
| A12 | constants: Q odd THEOREM; 6 DERIVED; c² FORCED; 1+2, 1:2:3 FORCED; γ = 1 CHOSEN; masses etc. DATA; sin²θ_W = ½ cutoff only | **AGREE + REFINE** | UPGRADE "6": THEOREM given K = 2u and six unit ports. \|λ\| ≤ 6 by the triangle inequality on six signed permutations, and the flat class attains 6, so D = 6 is the smallest divisor with \|cos w\| ≤ 1 for every sign class. CH-A's mass rows (mass + 12·wilson ≤ D; mass ∈ 2²²Z given P) were not re-checked by CH-B |
| A13 | ledger: 4 noticed, 0 kept | **AGREE + ADD** | CH-B's ledger adds 16 = \|2O/Z3\| (no spin ½ in R[2O/Z3]), 8 = min faithful G384 = Cl(1,3) module (different G192 content), D = 6 = \|S3\|. Joint: 7 noticed, 0 kept |

### B-II — CH-B on CH-A's marks of CH-B's claims
- **§3 minimal node (CH-A DISAGREE): ACCEPTED — AGREE (joint text)**, CH-A's three-part text of ~15:17, with CH-B's EDITs in
  brackets:
  (1) Three separate factors SU(3)·SU(2)·U(1) on a quark hop have degree 5: FORBIDDEN (s11 AGREE_CL3 row 17). This is CH-B's 413
      (341 with 3 relays), which stays only as the rank-blind lower bound.
  (2) Two factors SU(3) ⊗ U(2) give rank 4, which is NOT an approved kind (the narrow kind excludes link × composite; s12 AGREE_GU1
      B5 Cor 5a, re-read by CH-B). They are admissible only with an NL4-type NEW LAW: 48 + 128 + 9×26 + 4 + 10 + 7 = 431 (353 with
      3 relays). [EDIT: plus route B's det-shadow 6 and hybrids 24 if its built lepton constructions are used: 461 / 383.]
  (3) One link per irreducible multiplet (Burnside, rank 3) is admissible today: ≈ 1,057 (817). The hypercharge locks are UNBUILT
      and possibly rank-obstructed. [EDIT: these figures carry relays for the Q_L M6(C) link only. The u_R/d_R links' locks or
      relays (up to 6 × 36 = 216) and the quark hybrids are not counted, so the upper end is open.]
  So: one family ≈ 817–1,057 [+ unbuilt parts] under today's rules, ≈ 353–431 [383–461] with NL4. OPEN until a quark hop is built.
- **T4 last line (CH-A REFINE: mark the "×2 Rule3 second order" d.o.f. reading as a reading): ACCEPTED, and already
  self-corrected before the freeze.** The draft CH-A read at 15:11:15 had "8 per Weyl = … × 2 (Rule3 is second order)". That was
  WRONG as a channel count. CH-B replaced it at 15:11 with "the 8-block is one Dirac 4-spinor in real components; the pair
  doubles it for J′; Rule3 being second order doubles the PHASE SPACE (the two carrier senses e^{∓Jπt/2}), not the channel count".
  The phase-space statement is a DERIVED reading (linear algebra of the leapfrog with B(k) commuting with J), not a checked theorem.
- T10/T11 and §3-split bookkeeping (CH-A REFINE: "size given presence" vs "presence chosen"): ACCEPTED. Both bookkeepings are
  recorded; both sum to 382.
- All other CH-A marks on CH-B (AGREE / ADOPT) are acknowledged. CH-B adopts CH-A's census findings A4 (as refined above) and
  CH-A's §7 OPEN item (a quark-hop construction within rank ≤ 4 is needed before any one-family count is final).

### B-III — CH-B's new rows (for CH-A to mark)
| id | claim | status | evidence |
|---|---|---|---|
| B1 | In ONE v1 only h00 of the 10 metric gears is coupled; the 9 others are free self-stencils. The connected physical core is 127 channels. With the 228 isolated gauge-layer channels, 11 readers and 7 cosmic channels, 255 / 382 channels lie outside that core. So "metric 10 = Sym²R⁴" is today a SIZE statement: γ = 1 does not come from h_ij (consistent with γ ENCODED) | CENSUS | chb_compose2.json |
| B2 | Regular-module test, sharpened: R[G384] (384 channels) would have exactly 192 channels with z = +1 and 192 with z = −1, since z is central of order 2. Three families are 384 channels with z = −1. So 3 × 128 ≇ R[G384] for a second, independent reason (the N_B = N_F count), besides "χ(z) = −384 vs 0" | THEOREM (one line) | z central in G384: z commutes with (h, k) and with θ (θ(−g) = −θ(g)) |
| B3 | ν_R FORCED, in board form (Nielsen–Ninomiya). A one-handed block (one Cl(0,3) module, 4 channels) has massless species at all 8 corners, and ω flips with each π component (P_d → −P_d): 4 corners of each hand. Removing them needs W0, i.e. both hands | THEOREM (lattice) | CH-B T7 (frozen) |
| B4 | The 3-relay saving can be made at rank 3 (A8 REFINE). If built, ONE v1 → 298 and the one-family estimate → 817 without a new rank-4 kind | DERIVED, UNTESTED | A8 row above |
| B5 | Joint owner sentence (proposed): "The cube and the Clifford algebra fix how big each kind of channel must be: 48 for the dark board (given a sign-free frame), 16 per charged Dirac fermion, 4 for the Higgs, 2 / 4 / 8 / 18 per link, 10 for the metric. They do not fix which kinds exist, how many copies (colours, families), or the total. Today there are 382 per node, and only 127 of them form the connected physical core. A full Standard-Model family needs about 820–1,060 per node or more, because the rank rule forces one merged link for the quarks; that link is not built. With a new rank-4 law (NL4) it would be about 350–460. Q odd, the 6, the cone c² = (Q−1)/(3Q) and the 1:2:3 ladders are theorems. Masses, α, the Yukawas and θ_W at low energy are data: no symmetry of the node can fix them. Fixing them needs a new law: a family group, one gauge coupling, or a Yukawa law." | PROPOSAL | — |

### B-IV — open disagreements
None. CH-A's one DISAGREE (CH-B §3) is accepted by CH-B. CH-B's marks on A1–A13 are AGREE or AGREE + REFINE (A4, A8, A11, A12,
A13); none is DISAGREE.

**CH-B SIGNATURE: 2026-11-10 15:17:48 UTC (date -u).** Rows B-I (13), B-II (4), B-III (B1–B5).
- [CH-B addendum 15:18:21 UTC] B2 computed: chb_zcentral.json: z = (g ↦ −g) is in G384, central, order 2; so R[G384] splits 192 (z = +1) + 192 (z = −1). The B2 row is CHECKED, not only a one-line argument.

## CH-A final section (after CH-B signed at 15:17:48) — CH-A marks of CH-B's B-I edits, B-II and B-III rows
| item | CH-B | CH-A | reason / evidence |
|---|---|---|---|
| A4 REFINE | the core is 127 at gear level: 9 of 10 metric gears are free self-stencils | **ACCEPT** (verified) | P9 (p9.json, pre-registered): 15 gear-level components; the core is 127 = ref 48 + matter 16 + matter2 16 + wsu2 36 + em 4 + chiral 4 + h00 + beta + bgk; h0x … hyz are singletons. CH-A's 136 was a namespace-level count. CHANNELS.md §0, §1.3 and §2 are amended |
| A8 REFINE | CH-B's 3-relay form is rank 3, the same kind as the built 2-paths; no new rank-4 kind is needed | **ACCEPT** | P8 checked both forms (rank-4 one-face-link and rank-3 two-path): B3 holds for all 36 monomials |
| A11 REFINE + edits (2), (3) | 431/353 → 461/383 with det-shadow 6 + hybrids 24; the upper end of 817–1,057 is open (u_R/d_R locks or relays up to 216, quark hybrids) | **ACCEPT** | arithmetic: 431 + 6 + 24 = 461, 353 + 30 = 383; 6 × 36 = 216 (two M3(C) links × 6 relays × 18 = 216). CHANNELS.md §4 note (iv) now carries the joint text with both edits |
| A12 upgrade | "6" is a THEOREM given K = 2u (triangle bound attained by the flat class) | **ACCEPT** | CHANNELS.md §5 amended |
| A13 | joint ledger: 7 noticed, 0 kept | **ACCEPT** | CHANNELS.md §6 amended |
| T4 self-correction | Rule3's second order doubles the PHASE SPACE, not the channel count; this is a DERIVED reading | **ACCEPT** | the frozen T4 says exactly this |
| B1 | only h00 is coupled; core 127; 255/382 outside it; "metric 10" is a size statement and γ is encoded | **AGREE + ADD** | P9 confirms. ADD (P9b, new, pre-registered): in **route B (ONE v2) the visible doublet is not coupled to gravity at all**. Its components are {matter, matter2, ewb} 138 and {ref, h00, beta, bgk} 51, plus the same 9 metric singletons. This confirms electroweak_b's own declaration ("leaves the doublet without a lapse coupling (OPEN)"). So route B's 205 is a sum of built blocks, not a coupled family + gravity node |
| B2 | R[G384] has 192 z-even + 192 z-odd channels (z central of order 2), so 3 × 128 (all z-odd) ≇ R[G384] | **AGREE** | z acts freely on G384 by multiplication, so R[G](1 ± z)/2 each have dim \|G\|/2. One line, correct |
| B3 | ν_R FORCED (Nielsen–Ninomiya on the board) | **AGREE** | = CH-A's adopted T7 |
| B4 | 3-relay saving at rank 3: ONE v1 → 298; one family → 817 without a new rank-4 kind | **AGREE** | 382 − 84 = 298; B3-checked (P8); dynamics UNTESTED (both) |
| B5 | joint owner sentence | **AGREE + one EDIT** | EDIT: after "only 127 of them form the connected physical core" add: "(and in route B the visible doublet is not yet coupled to gravity)". With that edit CH-A signs B5 as the joint owner sentence |

**JOINT STATUS:** no open disagreement. CH-A's one DISAGREE (CH-B §3, 413) is resolved by the joint three-tier text (B-II).
Every CH-A claim carries AGREE or AGREE + REFINE from CH-B, and CH-A accepts every REFINE above.
Joint headline: ONE v1 = 382 channels per node (CENSUS, both twins). The connected physical core is 127. Sizes are forced per sector
by the minimal real module of each sector's algebra (+ B3 relays). The content and the total are CHOSEN. No principle forces the
total: the regular-module, minimal-faithful and Clifford candidates are refuted. One SM family is ≈ 817–1,057+ under today's
rules (≈ 353–461 with NL4), and it stays OPEN until a quark hop is built. Constants: Q odd, 6, c², 1+2 and 1:2:3 are THEOREMS;
masses, α, θ_W(low), Yukawas, N_c and families are DATA/CHOSEN.

**CH-A SIGNATURE: 2026-11-10 15:20:10 UTC (date -u).** CHANNELS.md final v2 sha256 ad8265fd7a551db9… (re-stamped below if changed).

## CH-B final confirmation (after CH-A signed at 15:20:10)
- **B1 ADD (CH-A P9b): VERIFIED independently.** chb_compose3.py/.json: build() of ONE v2 (route_b=True), gear-level union-find.
  The components are {ewb, matter, matter2} 138; {ref, metric.h00, beta, bgk} 51; su3 168; su2 40; u1 20; readers 11; cosmic 7;
  and the 9 metric singletons h0x … hyz. So in route B the visible doublet has NO path to the lapse. This is the same as
  electroweak_b's declared OPEN.
- **B5 EDIT (CH-A): ACCEPTED.** The joint owner sentence (final) reads: "The cube and the Clifford algebra fix how big each kind of
  channel must be: 48 for the dark board (given a sign-free frame), 16 per charged Dirac fermion, 4 for the Higgs, 2 / 4 / 8 / 18
  per link, 10 for the metric. They do not fix which kinds exist, how many copies (colours, families), or the total. Today there
  are 382 per node, and only 127 of them form the connected physical core (and in route B the visible doublet is not yet coupled
  to gravity). A full Standard-Model family needs about 820–1,060 per node or more, because the rank rule forces one merged link
  for the quarks; that link is not built. With a new rank-4 law (NL4) it would be about 350–460. Q odd, the 6, the cone
  c² = (Q−1)/(3Q) and the 1:2:3 ladders are theorems. Masses, α, the Yukawas and θ_W at low energy are data: no symmetry of the
  node can fix them. Fixing them needs a new law: a family group, one gauge coupling, or a Yukawa law."
- CH-B confirms CH-A's JOINT STATUS paragraph above. Open disagreement: none.

**CH-B FINAL SIGNATURE: 2026-11-10 15:20:35 UTC (date -u).**

**CH-A RE-STAMP (2026-11-10 15:20:59 UTC):** CHANNELS.md FINAL v2, sha256 af5422122398c490… The changes after the 15:20:10 signature are wording only: §0 item 5 and
§4 note (iv) now state the dispute as resolved, and §0 item 7 holds the joint owner sentence (B5 with CH-A's edit) verbatim. No
number changed. AGREE_CH is closed: both twins signed, and there is no open disagreement.
