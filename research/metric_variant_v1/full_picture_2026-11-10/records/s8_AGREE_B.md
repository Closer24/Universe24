# AGREE_B — Study 8 "CYCLIC BANGS": twin agreement BANG-1 (theory) × BANG-2 (numerics)
- Built by BANG-1 at Tue Nov 10 12:35:57 UTC 2026 (file mtime of the build), from:
- FILE-COLLISION NOTE (BANG-1, Tue Nov 10 12:37:46 UTC 2026). This build overwrote BANG-2's simultaneous build (created 12:35:49) 8 s
  later; it was unintended. BANG-2 then chose this build as the master, marked every row and signed (12:37:11). BANG-2's
  own build is summarised in BANG-2_NOTES §19: 21 AGREE, 5 REFINE, the same recommendation, no DISAGREE.
  - B1 = s8/BANG-1_FINDINGS.md (DRAFT v1 on disk 12:15:16, before any BANG-2 file was read) + s8/BANG-1_NOTES.md;
  - B2 = s8/BANG-2_FINDINGS.md (DRAFT v1, 12:29–12:31; written without reading BANG-1) + s8/BANG-2_NOTES.md.
- Independence: BANG-1 first read BANG-2's files at 12:33, on the manager's permission (12:33 relay). BANG-2 states it
  read no BANG-1 file before its draft.
- Pins (both read-only, separate copies):
  - B1: s8/BANG-1_work/pin (layers/system.py 7a660dad…; hashes in pin_sha256.txt);
  - B2: s8/BANG-2_work/pin1 (MANIFEST e88ab47a…, layers/system.py 37251ae6…);
  - both: core/engine.py 9dc8f53d…, layers/gravity.py d75f4802…, prepare/seed.py 8357ea4e…, observe/seed.py 57e8da87….
- Labels: THEOREM / NUMERIC (file) / DERIVED / MECHANISM (prescribed field or a non-approved law: never evidence for the
  approved system) / OPEN. Anything new = NEW LAW (owner decision).
- Verdicts: AGREED / AGREED-WITH-QUALIFIER (AwQ) / AGREED-OPEN / DISAGREE. **BANG-2: please mark the last column
  (ACCEPT / EDIT / DISAGREE) and sign.**

## A. The mechanism (C1): exact algebra of a factor crossing zero
| # | claim | B1 | B2 | proposed verdict | evidence | B2 mark |
|---|---|---|---|---|---|---|
| A1 | Rule3 stays an exact bijection for every coefficient sign and time dependence, gear-valued coefficients included; the plain mirror Mp (a↔b, R′) is an exact reversor of every b-only input. No crossing loses information | THEOREM (§1.1); every rewind exact (T1–T10f) | THEOREM (§2.1 scope); every rewind exact (B1 1800, U1, U3, M, M2 2048) | AGREED | both codes | ACCEPT (+ J1.json: rewind exact even through a runaway to > 2^87) |
| A2 | **THEOREM F = BANG-2's lapse-zero bounce (derived independently: B2 11:47, B1 draft 12:00).** If ONE common factor multiplies the whole first-order operator and is odd about an integer zero t_f, then every history satisfies b(t_f+j) = (−1)^j b(t_f−j) at the linear level. The seed returns at 2t_f; the clicks are mirrored, with C1↔C2 on odd steps and kinds kept on even steps | THEOREM (§1.5) + toy NUMERIC T4/T4b (crossing step exact; δ_max 11–15 units, ∝ 1/A relative; σ = 1.5 packet ×10.4 then refocused to 1.3e−3) | THEOREM T2 + MECHANISM T-M 1911 on the package's Dirac matter (mirror defect ≤ 1.7e−5; footprint 1 → 618 → 1; click mirror 90 % / 88 %) | AGREED (two proofs, two codes) | b1_c1_results.json, b1_c2c3c4_results.json; M_1911.json | ACCEPT |
| A3 | Integers: the crossing step is EXACT (K = 0 ⇒ ℓ = 0, r′ = r). After it the mirror breaks at O(1) unit per update (relative O(1/A)). The exact condition is δr(t*+s) = (−1)^(s+1) δr(t*−s) for the remainder increments; it first fails at u = 1, so the b-mirror first fails at s = 2 | THEOREM + POST HOC T4c | "rounding breaks it at O(1) unit per update" (§2.1) | AGREED (B1's exact condition added) | b1_t4c_posthoc.json | ACCEPT |
| A4 | Second-order (carrier) gears cannot fold. The carrier term is even in time, the lapse enters the deviation squared, and a negative factor is an inverted oscillator growing at g = m + √(m²−1) per update. Exact, reversible, unbounded | THEOREM (§1.3) + NUMERIC T2 (0.19875 vs 0.19974; rewind exact) | DERIVED (§2.1 scope; D1) | AGREED | b1_c1_results.json | ACCEPT (seeded-L0 check T-L0 registered, NOTES §18; see D5) |
| A5 | No J+ → J− transfer through any crossing. N_J(t+1) − N_J(t) = b(t)ᵀJ(r(t) − r(t+1)) exactly. What reverses is the clock sense INSIDE J+ | THEOREM + NUMERIC T3 (1.3e−4 at 2^14) | THEOREM + NUMERIC T-MJ (N_J 1 ± 1.6e−5, J− ≤ 2.1e−6, W_J sign kept, both arms) | AGREED (two codes) | b1_c1_results.json; MJ_GR.json, MJ_1911.json | ACCEPT + EDIT: in the FULL v2 default (J1.json) the J− fraction reaches 0.13–0.29 near U ≈ 1 while N_J stays within 7e−6. It tracks the β corner mode (G/P → O(1): a period-2 (π,π,π) modulation coupling ε ↔ π − ε), not the crossing; the β-free T-MJ gives ≤ 2.1e−6 |
| A6 | "The clocks reverse" has exactly two meanings. (i) The DEMODULATED π/2-carrier sense: ε → −ε, read in clicks by c_W's sign. (ii) Click kinds C1↔C2 at fixed b. The PHASE-SPACE rotation sense never flips while stable: orientation = −(leapfrog energy) < 0 at every step | THEOREM + NUMERIC T1 (4000/4000 steps, through a crossing) | c_W crosses 0 at the clock-factor zero (T-M, U1, U3) | AwQ (complementary: B2 measures (i), B1 proves the phase-space statement) | b1_c1_results.json; U1.json | ACCEPT |
| A7 | The owner's two guesses are the two halves of one fold. Flipping the LINKS only gives a Loschmidt velocity reversal: positions retrace (width 10.9 → 1.065) but the clock phase advances (+2.54 rad), a crunch in clocks. Flipping links AND clocks (one common factor) gives the fold: the phase returns too (−1.8e−4 rad) | DERIVED + NUMERIC T9 (+ T9b POST HOC) | T-M GR vs 1911 arms; U1: the matter "stops spreading at U = 1/2 and partly re-contracts" (link flip first) | AGREED | b1_t9_results.json, b1_t9b_posthoc.json; M_GR.json, U1.json | ACCEPT |
| A8 | **Approved law (γ = 1): the flip is real but is TWO events.** The links (transport) reverse at U = 1/2 and the clocks at U = 1. Hence NO exact bounce (GR arm m = O(1)), only a partial re-contraction (spread 2.21 → 1.60). The evolution is exact and stable through both zeros to U = 2, and the R* bounce is exact across them | DERIVED (§1.3: γ = 1 zeros differ; no total flip) | NUMERIC U1, U3, M_GR | AGREED, with a **B1 CORRECTION** (next column) | U1.json, U3.json, M_GR.json | ACCEPT |
|  | **B1 CORRECTION (accepted from B2's runs).** B1's draft said the approved system "cannot perform the flip" and predicted a light freeze at U = 1/4. In the v2 default the photon (E1 A-gears) and the metric gears do NOT read the lapse; only E1's source is dressed. Only matter (first order) and L0 (form C) carry lapse factors. So an L0-free history passes U = 1/4, 1/2 and 1 stably. The U = 1/4 freeze holds for the package's test light (F4/D7) and for an EXCITED L0 (B2 T-L0 registered) | | | | NOTES (B1, 12:34) | ACCEPT |
| A9 | Minimal ingredients of an EXACT recurring fold, each a NEW LAW: (a) one COMMON factor on clock and link entries, odd about its zeros (a γ = 0 uniform lapse: it must be a separate cosmic gear, since the gravitational lapse has γ = 1); (b) every lapse-reading sector first-order (no carrier gears read it); (c) a restoring term so that its zeros recur; read one-way (designated). B2 adds (d) a repair: remove the β corner-mode resonance (even L) | DERIVED (§1.6) | DERIVED (§0.7) | AGREED | — | ACCEPT |

## B. The Big Bang with all approved decisions (C3) and the duality (C2)
| # | claim | B1 | B2 | proposed verdict | evidence | B2 mark |
|---|---|---|---|---|---|---|
| B1 | R* (the package's declared link-centred map) is an EXACT reversor of the WHOLE v2 default along S2*. The bang is exactly two-headed | NUMERIC T10–T10e: t ≤ 200 at A = 2^18 with gravity (from t = 4) and β (from t = 52) excited; t ≤ 10 at 2^12 with and without bgk + offset | NUMERIC B1 (t ≤ 20, 0 mismatches on every namespace), U3 (t ≤ 100 across both zeros) | AGREED (two codes, two pins) | b1_t10*_results.json; B1.json, U3.json | ACCEPT |
| B2 | One bang, no recurrence. The uniform mode is exactly symmetric about the bang and rises ∝ t² on both sides, because S2*'s own b-only source is positive (the Ē = 0 datum does not cancel it). So the bang is the MINIMUM of U, and both halves accelerate apart in clicks. No exact recurrence in 1800 updates | NUMERIC T10e: M(−1−s) = M(s) exact, M(0) = 0, M = 968 → 2.29e6 (t = 10 → 200) | NUMERIC probe2, probe_L5, B1: U_mean ∝ t²; no repeated hash in 1800 | AGREED | b1_t10e_results.json; B1.json, probe_L5.log | ACCEPT + EDIT: '∝ t²' holds early only. Later it is faster on L = 5 (U = 3.9e−3, 5.4e−2, 0.43 at t = 1000, 2600, 6100; probe_L5.log, probe3_L5.log) and slower on L = 6 (2.7e−4 → 4.6e−4 over t = 1000 → 1600) before the β runaway |
| B3 | The background datum (data) sets only the SIGN and size of the uniform drift. Under-cancelled: convex. Near-cancelled: ≤ 2.5 %. Over-cancelled: concave, the mirror image. No datum gives the uniform mode a restoring force. B1's registered "at most one sign change" failed at v*: two, forced by the time dependence of the source | DERIVED + NUMERIC T10f | U3 uses a negative background to accelerate U (consistent) | AGREED (B1 numeric; B2 consistent) | b1_t10f_results.json; U3.json | ACCEPT |
| B4 | On an even board the v2 default with S2* runs away at t ≈ 1830–1880 (L = 6) through the β corner mode (π,π,π), ω ≈ π, resonantly driven by F_uniform × F_staggered. It is stable to t = 2600 on L = 5 | not run (B1's runs stop at t = 200) | NUMERIC + DERIVED | AGREED (B2 single code; B1 accepts the mechanism) | probe2.log, probe_L5.log, ckpt_L6_t1600.pkl | ACCEPT |
| B5 | Per-update click complexity saturates within ~50 updates. The record keeps growing (≈ 216 new node-words per update; zlib +14.5 kB per update). The arrow is two-headed (footprint and entropy minimal at the bang) | THEOREM (two-headed arrow, §2.2) | NUMERIC B1 | AGREED | B1.json | ACCEPT |
| B6 | **C2, same history read two ways.** (a) At any exact moment the half in which the board contracts toward a bang is read by its own observers as an expansion (records grow away from the bang). (b) In the fold, mirrored board times have the same footprint at the same CLICK proper time (τ_click). (c) Kinematics: the click scale factor is a = √(g/f) for second-order gears (= √((1−2U)/(1−4U)) with GR factors) and (1−U)/(1−2U) for first-order matter, so 1 + z = a(t_r)/a(t_e) | THEOREM (a) + DERIVED/NUMERIC T5 (c; MECHANISM, 8/8 windows ≤ 2.1e−4) | NUMERIC (b) M_1911_tau; U1: N_click tracks 1−U through zero | AGREED | b1_c2c3c4_results.json; M_1911_tau.json, U1.json | ACCEPT |
| B7 | **B2's U1 (the owner's sentence in the approved law).** With a k = 0 velocity datum the clocks reverse in the clicks at U = 1 (c_W follows 0.525(1−U) through 0). After this click-bang (a = 0) the clicks read a NEW expansion (a_click 0.16 → 0.36; board (1−U)/(1−2U) 0.08 → 0.32), while on the board both factors keep falling (f = −1.06 → −2.8) | DERIVED kinematics: a = (1−U)/(1−2U) (§2.1) | NUMERIC U1 + c2fit | AwQ. B1 qualifiers: (i) between U = 1/2 and U = 1, a_click < 0 (light and clocks counter-rotate), so this expansion starts at the click-bang U = 1 and saturates at a → 1/2 as U → ∞; (ii) f_click is unresolved near f = 0 (B2's own caveat); (iii) U = 1 needs a datum here; from S2*'s own source it is extrapolated at ~11,000 updates on L = 5 (B2), beyond the β/heating horizon | U1.json | ACCEPT the AwQ + EDIT (iii): the free L = 5 run with NO datum (probe3_L5.log) passed U = 1/4 at t ≈ 4700 and reached U = 0.43 at t = 6100, with c_W = 0.32 ≈ 0.525(1 − U) and no runaway. Whether it reaches U = 1 is appended under the signatures when the run ends |
| B8 | The approved uniform-mode drift is not GR cosmology. With exact constraints (OD2) the k = 0 mode is frozen; the wave-lapse drift violates the k = 0 constraint and ACCELERATES comoving nodes apart, against Raychaudhuri's deceleration for dust. A Friedmann k = 0 law needs nonlinear gravity | DERIVED (§2.3) | "no restoring force for the k = 0 mode" (§5) | AGREED-OPEN | F4b, F4d; probe_L5.log | ACCEPT |
| B9 | Penrose CCC. The board is the regular "bridging" frame in which the click metric degenerates (partial match). But the board's degenerate limit is Carrollian (light frozen, clocks tick) or a big-rip-type finite-time end, and exact reversibility forbids CCC's entropy reset. The other side of each exact moment is the reversor image (CPT-symmetric universe; Janus point) | DERIVED + literature (§2.4) | — | AGREED (B1; B2 to mark) | — | ACCEPT (no B2 numerics) |

## C. Cycles and complexity (C3)
| # | claim | B1 | B2 | proposed verdict | evidence | B2 mark |
|---|---|---|---|---|---|---|
| C1 | **THEOREM P.** A bounded orbit of the exact bijection is exactly periodic. If it contains a state fixed by a reversor R (R F R⁻¹ = F⁻¹; involutivity not needed), it has EXACTLY one more symmetric moment, at p/2: R-fixed if p is even, a half-integer F∘R moment if p is odd. The next bang is an exact copy | THEOREM + NUMERIC T8 (15/15, Mp) and T8b (link-centred PT reversor exact 10/10; 28 recurrent orbits, moments exactly at p/2 and p) | THEOREM T1 (T-REC registered, not run) | AGREED | b1_t8_results.json, b1_t8b_results.json | ACCEPT (B2's T-REC not run) |
| C2 | Boundedness is NOT automatic. Two 10-gear toy orbits heat ~√t with no recurrence in 2·10⁶ updates. The approved S2* run is unbounded at even L (β runaway) and drifts in U at odd L | NUMERIC T8b + T8c (POST HOC) | NUMERIC probe2, probe_L5 | AGREED | b1_t8b_results.json, b1_t8c_diag.json; probe2.log | ACCEPT |
| C3 | **THEOREM C.** On an exactly (or twisted-) periodic history every symmetry-invariant measure repeats each cycle (footprint, per-cycle record entropy, distinct structures). Complexity can grow from bang to bang only through what does NOT recur | THEOREM (§3.5) | THEOREM (§1.3) | AGREED | — | ACCEPT |
| C4 | **Oscillating common lapse (the fold with its own clock).** Bangs recur: B2 8/8 on the package's Dirac matter (period 512, footprint 1 at every bang, seed distance 1.4e−5 → 1.3e−4); B1 100 cycles in toys (cosmic gear exactly periodic, 2Δ = 298) | NUMERIC T6/T6b (toy, one-way cosmic Rule3 gear) | MECHANISM T-M2 | AGREED (two codes) | b1_c2c3c4_results.json, b1_t7b_t6b_results.json; M2_A16/A12_1911.json | ACCEPT |
| C5 | **Complexity rises from bang to bang ONLY through the O(1/A) remainder debris**, monotonically in the clicks, while the board stays exactly reversible (rewind exact).<br>B2: debris 14 → 637 entries; per-aeon clicks +31 %, entropy 8.80 → 9.02 bits, zlib +35 %; seed distance ×300 at A = 2^12 (∝ 1/A).<br>B1: defect 12, 39, 71, 156 units at n = 1, 10, 30, 100 (exponent 0.54–0.56, A-independent in units); bang width error 0.43 (2^14) vs 2.5e−3 (2^18) after 100 cycles.<br>The two growth laws agree: defect ∝ √n ⇔ squared distance ∝ n | NUMERIC T6b | MECHANISM T-M2 | AGREED | as C4 | ACCEPT |
| C6 | With odd Δ every next bang is the global NEGATIVE of the last: click kinds C1↔C2 alternate per cycle, N_J unchanged. With even Δ (B2's 256) the bangs repeat with the same sign | NUMERIC T6 (Δ = 149) | consistent (Δ = 256, even) | AGREED | b1_c2c3c4_results.json | ACCEPT + EDIT: B2's fold has Δ = 128 (bangs every 256 = 2Δ), even; b(256) = +b(0), as THEOREM F gives for even Δ |
| C7 | **"ONE BIG CLOCK whose complexity rises from bang to bang" (owner, 12:28), joint reading.** On a finite board the whole history is ONE big clock: every bounded orbit is a single exact cycle, and inside it complexity cannot rise from cycle to cycle (C3). It CAN rise from bang to bang inside the grand cycle, between the short bangs of a cosmic clock (C4), carried only by the reversible O(1/A) debris (C5). So the "ever more complex boards, expressed in the clicks" are a long reversible transient, readable only in the clicks; the board itself loses nothing and returns exactly at the grand recurrence (if bounded) | DERIVED from C1–C5 | DERIVED from §1.3, §2.3 | AGREED (proposed joint text) | — | ACCEPT |

## D. Connect everything (C4)
| # | claim | B1 | B2 | proposed verdict | evidence | B2 mark |
|---|---|---|---|---|---|---|
| D1 | The J− mirror world is NOT the other side of the bang. N_J is R*-even, and a lapse zero keeps N_J, the J± split and the sign of W_J. S2* bounces both J-worlds together | THEOREM (§4.1) | NUMERIC T-MJ + THEOREM | AGREED | MJ_*.json | ACCEPT |
| D2 | Across an Mp bang the board's J-labels swap, but each side read with its OWN arrow is identical to the other (the click Wronskian is odd under time-order reversal) | THEOREM + NUMERIC T7b (exact, half by half) | — | AGREED (B1 single code; THEOREM) | b1_t7b_t6b_results.json | ACCEPT (B1 code only) |
| D3 | **CPT anti-aeon.** The other side of the approved bang (and each second half-cycle, by C1) is the CPT image of our aeon. Its own observers see the CP image (matter↔antimatter, hand CP-mapped). With Γ5·V, CP is an exact forward symmetry, so that aeon is one-handed in its own clicks. Each cycle = aeon + anti-aeon; the history is CPT-balanced | THEOREM given full-system R* (now NUMERIC: B1/B2 rows above) | "its board history retraces (the CPT-type mirror of the same sector)" (§4) | AGREED | T10e; B1.json, U3.json | ACCEPT |
| D4 | Decision 5 is NOT closed by the cycle: the hand still needs the Γ5·V chiral block (NEW LAW, AGREE_H). The cycle adds the anti-aeon as a third home for mirror partners, besides the per-aeon J− dark mirror and the heavy doublers | DERIVED (§4.4) | "Decision 5 is not closed by this mechanism" (§4) | AGREED | AGREE_H | ACCEPT |
| D5 | L0 (dark) is the same dark sector in every aeon, since there is no mixing block. Along S2* it stays exactly at vacuum, so R* holds on it trivially. The package's declared R* FAILS for its own L0 dark seed at t = 1: it lacks the signed relabelling P∘χ, so L0's own P∘χ∘T must be composed in. An excited L0 is second-order (form C) and inverts past 1 − 4U = 0 | NUMERIC T10d(ii) + DERIVED | B1.json (L0 at vacuum, R* holds); T-L0 registered (DERIVED to invert) | AGREED-OPEN | b1_t10d_results.json | ACCEPT (AGREED-OPEN; T-L0 result appended if run) |

## E. ONE recommendation: the minimal law for recurring bangs (joint proposal)
**Recommendation: the FOLD, as ONE new block. The "cosmic spring" is part of it.**
- A single uniform cosmic-clock gear (one Rule3 rotation gear: its own restoring term, hence its own spring). It is read
  one-way (designated), as ONE COMMON factor (γ = 0), by the whole input of every first-order sector.
- Its zeros are exactly antisymmetric: a linear gear at an integer zero is JR-symmetric. So every history folds at
  every zero (THEOREM F): bangs recur every 2Δ for ANY first-order content (C4).
- The click complexity rises from aeon to aeon only through the O(1/A) debris (C5).

**Why not the alternatives** (each shown above):
- **Data only:** exact cycles only on bounded orbits, after the astronomically long recurrence time (C1/C2). The
  approved S2* history is not bounded (B2/B4). Designed hardware (E15/E18) recurs only for its designed content.
- **A cosmic spring on the GRAVITATIONAL lapse (screened lapse):** γ = 1 splits the zeros, so there is no return (A8,
  GR arm m = O(1)). It also changes long-range gravity, and any excited second-order lapse-reader (L0) inverts (A4).

**Costs to state to the owner:**
- a preferred cosmic time (a designated one-way uniform gear, not GR);
- γ = 0 for this mode, kept separate from the γ = 1 gravitational lapse;
- no carrier gear (L0 form C, field gears) may read it;
- an O(1/A) debris that grows ~√(number of bangs);
- exactness only at the linear level for the mirror, while the board itself stays exactly reversible.

**Status:** an explicitly separate candidate variant (AGENTS: separate variants), NOT the reference. Without it the
approved system's statement is: ONE exact two-headed (CPT) bang, the clocks reversing at U = 1 when U gets there, and a
partial re-contraction; no recurring bangs.


**BANG-2 EDIT to E (how the rise appears in clicks; numbers from C5).**
- Each aeon's official click record is longer than the one before (+31 % over 8 aeons).
- Its symbol entropy is higher (8.80 → 9.02 bits) and it compresses worse (+35 %).
- On the board the only growth is the debris: 14 → 637 entries above 16.
- At A = 2^12 the debris is ×300 larger (amplitude ∝ 1/A), so the rise vanishes as A → ∞.
- **BANG-2 ACCEPTS E as the joint recommendation.**

## Signatures
- BANG-1: built every row from both drafts; B1 column from s8/BANG-1_FINDINGS.md; proposed verdicts above. I accept
  B2's evidence on B4 (β corner runaway) and B7 (U1), and record my correction in A8.
  **BANG-1 SIGNS all rows, and ACCEPTS BANG-2's EDITs on A5 (J− leak = β corner mode, N_J kept), B2 (∝ t² early only),
  B7 (iii) (the free L = 5 run passes U = 1/4 with no datum and no freeze, confirming A8), C6 (B2's Δ = 128) and E
  (click-side numbers): Tue Nov 10 12:37:46 UTC 2026 (`date -u`).**
- BANG-2: please mark each row (ACCEPT / EDIT / DISAGREE), edit E if needed, and sign.
- **BANG-2 SIGNS all rows as marked: Tue Nov 10 12:37:11 UTC 2026 (`date -u`).**
  - Marked every row: ACCEPT, with EDITs on A5, B2, B7, C6 and E. No DISAGREE.
  - The β-free J-pure control (T-MJ) is done (A5, D1).
