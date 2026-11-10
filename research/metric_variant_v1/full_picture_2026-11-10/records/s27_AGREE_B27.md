# AGREE_B27 — STUDY 27 "Bell on the board, the owner's way, NO freeze": BELL-X (constructive) × BELL-Y (rigorous)
- Created by BELL-X at Tue Nov 10 16:01:34 UTC 2026 (`date -u`).
- Manager rule: BELL-X creates; **BELL-Y only APPENDS** below the marker "BELL-Y SECTION". Nothing above it is edited
  by BELL-Y. BELL-X will mark BELL-Y's rows in a later appended section and sign by 17:20.
- Paths are relative to the scratchpad S.
- BELL-X sources:
  - s27/BELL-X_PROPOSAL.md (freeze stamp + sha256 to be appended at 17:05);
  - s27/BELL-X_NOTES.md (pre-registrations P1–P11, every result, one FAILED prediction);
  - s27/BELL-X_work/ (code, JSON, SHA256_runs.txt).
- Independence: BELL-X read no BELL-Y file before creating this file.
- Labels: THEOREM / BUILT (exact board) / NUMERIC / DERIVED / NEW LAW / FAILS / OPEN.
- BELL-Y marks: ACCEPT / ACCEPT + EDIT / DISAGREE (with reason).
- Board B27X:
  - exact Rule3 on every gear, Q = 5, D = 30, NO freeze (click time = board time);
  - one fixed tensor, every u of degree ≤ 2 in face-neighbour b (rank ≤ 4); no on-site links, no a-reads;
  - the x-line of a 24³ torus (y, z entries zero, other lines inert vacuum). Checked on the genuine 3-D torus
    (h_3d.json: 0 mismatches, off-line vacuum kept, 3-D rewind exact 8/8).

## A. The owner's rule as a law (B1)
| # | claim (BELL-X) | label | evidence | BELL-Y |
|---|---|---|---|---|
| X1 | **LAW O (strongest legal form, no freeze).**<br>- O1: the quantum is an exact C0 wave on every path, with total intensity ΣK = D, carrying the emitting click's token t (a common-past datum loaded additively into every detector's vacuum remainder, never read).<br>- O2: the source detector carries once (emission click).<br>- O3: detector j carries iff loaded remainder + K_j ≥ D, with arcs anchored at opposite ends of the token range.<br>- O4: the exact inverse is the backward trace.<br>- O5: the "confirmation" has three candidates: (i) two-time boundary (the seed measure conditioned on the future), (ii) a forward confirmation front, (iii) completion (only completed pairs count) or, strictly, "only confirmed paths click" | DERIVED (formalisation) | PROPOSAL §1; b27x.py | |
| X2 | The inverse (backward trace) exists for EVERY history. As a "confirmation" it selects nothing. The bijection preserves the counting measure, so "the seed already encodes the future clicks" holds for every seed, including those with S ≤ 2 | THEOREM | PROPOSAL §4(i) | |

## B. One quantum (B2)
| # | claim | label | evidence | BELL-Y |
|---|---|---|---|---|
| X3 | ONE quantum, exact, no freeze (source 12; detectors 7 and 17; amplitudes (1, 2); K = 6, 24; t ∈ Z15).<br>- One emission click (ell = 1) in 15/15.<br>- Exactly one absorption click in 15/15 (L 3, R 12, none 0, double 0), so Born P = 1/5 and 4/5 EXACTLY.<br>- Rewind exact in 15/15 | BUILT | a_single.json (P1 PASS) | |
| X4 | "The path goes back from the clicking detector to the emitting click": the dependency set of the click (936 single-entry seed perturbations per token, 0 cone violations).<br>- Left click (site 7): sites 5–11, its own side back to the token's emission site 11.<br>- Right click (site 17): sites 12–20, its own side back to the source site 12.<br>- Neither depends on the other side | BUILT + THEOREM (cone) | a_single.json | |
| X5 | "One quantum" = ΣK = D:<br>- (1,1): 9/15 none;<br>- (2,2): 9/15 double;<br>- (1,2) and (2,1): exactly one click with no recalibration.<br>"The light chooses the path that is going to be" = the emitting click's token, a LOCAL hidden variable (enough for one quantum) | BUILT | f_norm.json (P7 PASS) | |

## C. The Bell pair without a freeze (B3) — the manager's (a), (b), (c)
| # | claim | label | evidence | BELL-Y |
|---|---|---|---|---|
| X6 | Setup.<br>- One emission: ring c(φ) to both sides, φ ∈ Z6.<br>- P(+ \| click) = cos²30°(φ − α) EXACTLY; P(click) = 4/5 for every (φ, α).<br>- Choosers: fresh ρ ∈ Z30 kicked by LOCAL trigger pulses (σ = 1 iff ρ ≥ 20).<br>- Timing: settings at update 3, clicks at 4, emission click at 1. Every pair of events is spacelike except each setting with its own click; settings are also spacelike to the emission | BUILT | b_pair.json (P2 PASS) | |
| X7 | **(a) EXACT S on one board**, max over all 1296 analyzer choices:<br>- independent path tokens: **5/4** on coincidences, 22/25 on all pairs;<br>- ONE shared path token (the emitting click decides both ends): **2 exactly** on all pairs, Clauser–Horne J_max = 0;<br>- the same, coincidences only (single clicks discarded): **22/9**;<br>- strict "only the confirmed path clicks" (sequential router, 0 single clicks): **2 exactly**.<br>Checks: δ = 0 exactly and far-setting marginal shift 0 exactly in every design. Three routes: factorised tables, 5,760 direct full-board runs, and a LITERAL enumeration of every seed (81,000 + 1,215,000 full-board runs, i_fullclass_*.json, P10 PASS). Rewind 472/472 | BUILT (exact) | b_pair.json, e_seq.json, c_twotime.json | |
| X8 | **THEOREM NF (no freeze ⇒ Bell holds).**<br>- (1) Click time = board time, so A's record is a function of seed data in A's past cone, which excludes B's setting event (cone).<br>- (2) Fresh chooser remainders are a pad (s14 X1), so δ = 0.<br>- Hence S ≤ 2 and J ≤ 0 on all emitted pairs.<br>- (3) If no station ever clicks without its partner ("only the confirmed path clicks"), then c_A(λ, a) = c_B(λ, b) for all a, b. Completion = c(λ) is then setting-free, measurement independence holds on the completed ensemble, and S ≤ 2 there.<br>- (4) Otherwise S_coinc ≤ 4/η − 2 (Garg–Mermin; η = 4/5 → 3) | THEOREM (+ BUILT instances X7) | PROPOSAL §3 | |
| X9 | **(c) Which of Bell's assumptions the rule keeps:**<br>- local causality, in click time = board time;<br>- measurement independence (δ = 0);<br>- definite outcomes;<br>- in its strict form, setting-independent completion.<br>It breaks only fair sampling, and only if unconfirmed single clicks are discarded (the detection loophole) | THEOREM + BUILT | X7, X8 | |
| X10 | **(b) The one S > 2 case (22/9, coincidences only).**<br>- No-signalling: a THEOREM for all emitted pairs (cone). Inside the coincidence ensemble the shift is measured 0, but that is NOT a general theorem: post-selection can fake signalling.<br>- Tsirelson: not derived (22/9 < 2√2 here; the room is 3).<br>- Label: FAILS as a loophole-free Bell test, because loophole-free tests score all pairs (CH/Eberhard), where the board gives J ≤ 0 exactly.<br>- P5 (FAILED prediction): S_coinc = 2, 20/9, 22/9 at η = 4/15, 8/15, 4/5; it never exceeds 2√2 for this reader | BUILT + FAILS (vs experiment) | c_twotime.json, d_eta.json | |

## D. The readings
| # | claim | label | evidence | BELL-Y |
|---|---|---|---|---|
| X11 | **(i) Natural two-time boundary.** The seed conditioned on "both clicks happen" IS the coincidence ensemble. It is measurement dependent:<br>- shared token: δ = 4/9 → S = 22/9;<br>- independent tokens: δ = 5/16 → 5/4.<br>2 + 6δ holds. It needs single clicks that are thrown away, against "only confirmed paths click" | BUILT | c_twotime.json | |
| X12 | **(i) Tuned two-time boundary = minimal lawful change (seed law).** On the board's own responses (8 one-wrong strategies realised; EN-B Z10 law):<br>- exact 60°-grid quantum CHSH E = (½, ½, ½, −1), S = 5/2, every pairwise TV = 1/12 (minimal: 2 + 6δ tight);<br>- marginals ½, every trial clicks;<br>- seed–setting mutual information 0.0354 bits per trial;<br>- support 1/3 of the class; KL to the board's counting measure 2.06 bits per trial, so weight ≈ 2^(−2.06·N) for N trials.<br>Floor for ANY all-click seed law on this board: ≥ log2(5/3) = 0.74 bits per trial (DERIVED).<br>**Minimal seed–setting information** (convex optimum, attained by the board's own realised strategies): 0.01776 bits per trial for S = 5/2, 0.04627 for Tsirelson. So any such law over N trials weighs ≤ 2^(−I_min·N) of the board's counting measure (≤ 2^(−178) at N = 10⁴).<br>Fresh choosers give δ = 0, so the correlation must be written into the seed: FINE-TUNED | NEW LAW (superdeterminism) + BUILT | c_twotime.json (P3 PASS); j_minmi.json (P11 PASS) | |
| X13 | In the seed law, no-signalling and Tsirelson are NOT theorems. On the board's own responses the same family gives, with marginals exactly ½: S = 5/2, 2√2, 3, 4 at δ = 1/12, 0.138, 1/6, 1/3. So 2√2 must be posted (circular) | BUILT + THEOREM (2 + 6δ tight, s14 X2) | g_x2.json (P8 PASS) | |
| X14 | On a deterministic bijective board, "the confirmation runs back from the absorber to the emitter" and "the seed is correlated with the future settings" are the same statement. Retrocausal = superdeterministic here (Wharton–Argaman's two exits merge; lit., from memory) | DERIVED | PROPOSAL §4(i) | |
| X15 | **(ii) Forward confirmation** (pinned s16 EN-A router, sha256 identical): CONFIRMED S = 5/2 (singlet exact 36/36), UNCONFIRMED 2.<br>On B27X a record using B's setting exists at A only at update ≥ 14, i.e. ≥ 10 updates after A's photon (update 4).<br>Without a freeze the wait is in click time, so confirmed records are TIMELIKE to the far setting. Completing a transaction after a spacelike click can only relabel or veto it (AGENTS rule 8) | BUILT (s16, re-run) + THEOREM (cone) → FAILS as a spacelike Bell account | en3_confirmed_choice.json; PROPOSAL §4(ii) | |
| X16 | **(iii) Other legal forms:**<br>- a non-local tensor is impossible under six-face, rank ≤ 4 reads (cone THEOREM);<br>- a hidden freeze is excluded by the owner;<br>- choosers fed by the emitted token = freedom-of-choice loophole (settings in the emission's future cone; B27X keeps them spacelike), DERIVED, not built | DERIVED | PROPOSAL §4(iii) | |

| X17 | **(iii-c) Literal Cramer handshake, forward in board time:** an offer to the absorbers, their confirmation (settings) back to the source, then the emission of the pair.<br>- Legal without a freeze; gives the singlet or up to S = 4 (s20 ZT-B T4).<br>- But the settings must lie in the emission's PAST cone. Settings switched in flight act on stale data, giving S ≤ 2 (X8).<br>- Fast-switching and loophole-free tests choose settings spacelike to the emission, so this FAILS vs experiment | DERIVED (+ cited) → FAILS | PROPOSAL §4(iii-c) | |

## E. Joint answer to the owner (BELL-X proposal; BELL-Y please mark)
- **Built.** One quantum works exactly as the owner says, with no freeze:
  - one emission click, the wave on both paths, exactly one absorption click;
  - Born exact; the backward trace exact;
  - the click depends only on its own path back to the emitting click.
- **Bell.** With the same rule and a typical seed, S = 5/4, or at most 2, exactly. The reason is a THEOREM: without a
  freeze the board keeps Bell's locality and measurement independence.
  - S = 22/9 appears only if unconfirmed single clicks are thrown away. That is the detection loophole, and loophole-free
    scoring gives J ≤ 0.
- **Minimal change.** A seed law that correlates the emission's token with the future settings (two-time boundary =
  superdeterminism).
  - Cost: δ ≥ 1/12 and ≥ 0.018 bits per trial for S = 5/2 (0.138 and 0.046 bits for Tsirelson); fine-tuned (weight ≤ 2^(−0.018·N)).
  - No-signalling and 2√2 must be posted by hand, since the same law reaches S = 4.
- **Verdict.** Bell does NOT stand on the board without a freeze. On this the push gate "Bell stands" is NOT met.

## Signatures
- BELL-X signs rows X1–X16 and section E as written: Tue Nov 10 16:01:34 UTC 2026 (`date -u`).
- Row X17 added by BELL-X at Tue Nov 10 16:03 UTC 2026, before BELL-Y opened the file; signed with X1–X16.
- X12 and E updated by BELL-X at Tue Nov 10 16:08 UTC 2026 (P11 minimal-information numbers), before BELL-Y opened the file.
- X7 evidence updated at Tue Nov 10 16:19 UTC 2026 (P10 literal enumeration), before BELL-Y opened the file.
- BELL-X will append: the proposal freeze stamp/sha (17:05), marks on BELL-Y's rows, final signature (≤ 17:20).

---------------------------------------------------------------------------------------------------------------------
## BELL-Y SECTION (BELL-Y: APPEND ONLY below this line — marks on X1–X16 and E, own rows, signature)

### BELL-Y MARKS on BELL-X rows X1–X17 and section E (appended by BELL-Y; nothing above this section edited)
- Independence:
  - BELL-Y froze s27/BELL-Y_PROPOSAL.md at Tue Nov 10 17:04:51 UTC 2026 (sha256 fa75cb451a9954eb…38839a84; copy
    BELL-Y_work/BELL-Y_PROPOSAL_frozen.md) BEFORE opening any BELL-X file.
  - First opened this file at 17:04:58; copy as read: BELL-Y_work/AGREE_B27_as_read_by_Y_before_marks.md (sha256
    5f6cca56…c4d8de, 12,273 bytes).
  - No BELL-X code was re-run (time). Marks rest on the rows' content, my own checks P1–P6 and the cited studies.
- Cross-checks that agree INDEPENDENTLY:
  - BELL-X's minimal seed–setting information equals BELL-Y's P2 KL minimum: 0.01776 vs 0.017763 bits (S = 5/2 grid)
    and 0.04627 vs 0.0462738 bits (Tsirelson).
  - X14 = BELL-Y Lemma 2.1(i) (retrocausal = superdeterministic on a bijection).
  - X17 = BELL-Y Corollary 3.2′ (F0, absorber-first request).
  - X10's S_coinc rising with η = BELL-Y P5's monotone arc scan.

| # | BELL-Y mark | reason |
|---|---|---|
| X1 | **ACCEPT + EDIT** | The formalisation is legal: the token is a common-past amplitude loaded into vacuum remainders and never read (s16 row 14). EDIT: the three O5 candidates sit inside BELL-Y's exhaustive classification (THEOREM 2.0: D/S/F/H):<br>- (i) = S;<br>- (ii) = F;<br>- (iii) "only completed pairs count" = S1 (observer) or S2 (LAW);<br>- "only confirmed paths click", when it is a property of the DYNAMICS (ΣK = D router), is D-type: a design, no selection |
| X2 | **ACCEPT + EDIT** | = BELL-Y Lemma 2.2, first half. EDIT (BELL-Y P3.a, NEW):<br>- the converse fails: under Rule3 (K = 2u, D = 6Q) r mod 2 is conserved and never acts, so 2^(48L³) seeds share every click history (reference engine: 0 mismatches, rewinds exact);<br>- the backward trace (O4) needs the final FULL STATE, not the clicks;<br>- the README line "the final clicks and the seed determine each other" should read "the final full state …" |
| X3 | **ACCEPT** (not re-run) | Consistent with BELL-Y P1 design R: a shared-remainder router with arcs summing to D gives P(exactly one click) = 1 for every remainder. Born exact (P = 1/5, 4/5 at D = 30 needs no 4 \| Q) |
| X4 | **ACCEPT** | The cone THEOREM; this is BELL-Y reading D1 ("the path back" = dependence/rewind, description only) |
| X5 | **ACCEPT** | = BELL-Y Lemma 2.3: one path = one click per quantum, by calibration ΣK = D. The token is a LOCAL hidden variable: determinism, not superdeterminism |
| X6 | **ACCEPT** (not re-run) | Design noted. Settings spacelike to the far clicks AND to the emission is the right test |
| X7 | **ACCEPT + EDIT** | Exact values noted; consistent in kind with BELL-Y P1 (independent exits, D = 30: coincidences 271800/110143 = 2.4677 on the CHSH grid; router 806/675 on the 60° grid). EDIT: "strict, sequential router: 2 exactly" is the D-type (dynamical) one-click law, where completion is setting-free. It is not the S2 LAW (selection), which keeps the 2.4677-type value WITHOUT any discarded clicks in the realised world (see X8, X11) |
| X8 | **ACCEPT (1), (2), (4) + EDIT (3), substantive** | (1)–(2) = BELL-Y THEOREM 3.1.<br>(3) is correct when "no station clicks without its partner" holds for EVERY setting, i.e. a property of the dynamics. Then c_A(λ,a) = c(λ), MI holds and S ≤ 2 (= BELL-Y Lemma 2.4 with setting-free c_A).<br>It does NOT cover the owner's rule as a LAW on seeds (BELL-Y S2: only histories confirmed under their ACTUAL settings exist). There the realised world also has no single clicks, yet MI fails (δ_C = 149/527 = 0.283) and S = 271800/110143 = 2.4677 (D = 30; 2.5122 at D = 606). The counterfactual step "for all a, b" is exactly what a seed law breaks. So NF should read "no freeze AND typical seed ⇒ Bell holds"; the seed law is the door (X12).<br>(4) ACCEPT + EDIT: with a setting-independent coincidence rate p, the exact TIGHT frontier is S ≤ 2/p (BELL-Y THEOREM 3.3(c), exact LP P6). 4/η − 2 (conditional efficiency η ≥ p) is also valid. "4/η − 2" is usually attributed to Larsson 1998; Garg–Mermin 1987 gave the 2(√2−1) threshold (lit., from memory) |
| X9 | **ACCEPT + EDIT** | For a typical seed: agreed (= BELL-Y THEOREM 3.1: PI and OI hold, MI holds, PI is never dropped on a forward board). EDIT: under the S2 seed law MI is broken. Under F2 the records are timelike (locality loophole), not a Bell test |
| X10 | **ACCEPT + EDIT** | Agreed: NS inside the coincidence ensemble is not a theorem. BELL-Y's explicit counterexample (P1 I-asym, '−' exit at half efficiency): S_C = 2.27 with a far-setting marginal shift of 0.147. Under the S2 LAW that is a REAL faster-than-light signal. Tsirelson not derived: agreed (BELL-Y THEOREM 3.5). The η-monotone S_coinc matches BELL-Y P5 |
| X11 | **ACCEPT + EDIT** | Numbers noted (δ = 4/9 → 22/9; δ = 5/16 → 5/4, a nice case of δ necessary but not sufficient). EDIT: the last sentence holds for S1 (singles discarded by the observer). As a LAW (S2) the singles never exist in the realised world, so S2 IS compatible with "only confirmed paths click" in the world. It pays instead with:<br>- MI (δ_C = 0.28);<br>- a seed measure P(C)^N (0.544^N at D = 30);<br>- E(0) = 0.83 (wrong curve);<br>- 100 % detector efficiency predicted;<br>- NS only by detector symmetry |
| X12 | **ACCEPT + EDIT** | Agreed in full; the KL/information numbers match BELL-Y P2 independently. EDIT, add BELL-Y's rigorous floors:<br>- (a) μ0{N-trial CHSH estimator ≥ 2√2} ≤ e^(−0.021447N) (Azuma–Hoeffding, any seed law);<br>- (c) an all-or-nothing confirmation with fair rates needs a confirmed fraction ≤ 2/S, so seeds ≤ 2^(−N/2) for 2√2.<br>The "log2(5/3) = 0.74 bits" all-click floor was not checked by BELL-Y |
| X13 | **ACCEPT** | = s14 X2 family = BELL-Y THEOREMS 3.4–3.5. 2√2 must be posted: agreed |
| X14 | **ACCEPT** | Found independently (BELL-Y Lemma 2.1(i), pullback). BELL-Y adds (ii)–(iii): full two-end data over-determine; half data (the Lagrangian reading) is ill-posed (isolated K = 0 gear: b_T = ±b_0 at even T) |
| X15 | **ACCEPT + EDIT** | = BELL-Y THEOREM 3.2. EDIT: the board's L1 cone is up to 1.73 c along an axis (≤ 3.5 c with plaquettes; s14 X4). So F-type readings are excluded only by tests whose timing margin exceeds that factor (Weihs 1998, lit.); Delft alone allows ≈ 1.2 c. The verdict FAILS stands |
| X16 | **ACCEPT + EDIT** | Agreed. EDIT, add the rest of BELL-Y's classification:<br>- D3, cyclic order: a bounded orbit of a bijection is periodic, so "there is always an earlier click" holds, but idly;<br>- S3, the half-data Lagrangian reading: ill-posed;<br>- the literal backward process: FAILS (AGENTS 7). |
| X17 | **ACCEPT + EDIT** | = BELL-Y F0 (Corollary 3.2′), found independently. EDIT: the records are then also timelike to the far setting (y reaches A's record via the source: t_A − t_y ≥ d(A,src) + d(src,B) ≥ d(A,B)) |
| E | **ACCEPT + EDIT** | Verdict agreed: **Bell does NOT stand on the board without a freeze; the push gate "Bell stands" is NOT met.** EDITs:<br>- (i) "S = 22/9 appears only if unconfirmed single clicks are thrown away" → "… only if they are thrown away (S1, detection loophole) or forbidden by a seed LAW (S2, = superdeterminism). As a law the owner's strongest outcome-blind rule gives S = 2.4677 (D = 30) with every trial confirmed, but δ = 0.28, seeds 0.544^N, E(0) = 0.83, and NS only by detector symmetry (0.147 signal otherwise)";<br>- (ii) add the rigorous floor e^(−0.0214N) and the price list S ≤ 2/p;<br>- (iii) "the backward trace exact" holds from the final FULL state; the clicks alone do not fix the seed (inert r mod 2);<br>- (iv) forward confirmation fails against tests with timing margin > 1.73 (board cone) |

### BELL-Y ROWS (for BELL-X to mark: ACCEPT / ACCEPT + EDIT / DISAGREE + reason). Source: s27/BELL-Y_PROPOSAL.md (frozen 17:04:51 UTC; sha256 fa75cb451a9954eb759f814d41ea1ed1485ac39100ba1a917481eaae38839a84)
| # | claim (BELL-Y) | label | evidence | BELL-X mark |
|---|---|---|---|---|
| Y1 | **Where a confirmation can live (THEOREM 2.0).** On the board a law is (U, μ), and board time is the only time. Every reading of "the path goes back from the receiving click to the emitting click" is one of four types:<br>- (D) a re-description (rewind, retrodiction, cyclic order);<br>- (S) a seed selection or reweighting by future clicks;<br>- (F) a forward board signal inside the cone;<br>- (H) a hidden time, which needs a hold/freeze or a second board: excluded.<br>A literal backward process FAILS (AGENTS 7). (S + F) mixtures fall under Y5 | THEOREM | PROPOSAL §2 | |
| Y2 | **Pullback (Lemma 2.1).** {σ : U^T σ ∈ F} = U^(−T)F.<br>- "Two-time boundary", "retrocausal selection" and "superdeterministic seed" are ONE object on this board.<br>- Full data at both ends over-determine the history.<br>- Half data at each end (the Lagrangian reading) is ill-posed: an isolated K = 0 gear has b_T = ±b_0 at even T, whatever a_0 is | THEOREM | §2 | |
| Y3 | **Inert parity (Lemma 2.2).** With K = 2u and D = 6Q, r mod 2 is conserved and never acts: ℓ = ⌊(⌊r/2⌋ + u)/3Q⌋.<br>- Clicks do NOT determine the seed: 2^(48L³) seeds share every click history.<br>- EDIT to the README THEOREM line: "the final FULL STATE and the seed determine each other".<br>- "The seed encodes the future clicks" holds for EVERY seed (determinism), and is not superdeterminism | THEOREM + NUMERIC | p3_results.json: arithmetic 0/2,204,022; REFERENCE engine (D = 6, L = 4, 12 updates, 2 sign sets): 0 a/b mismatches, 0 click mismatches, rewinds exact | |
| Y4 | **One path = one click; confirmation by selection = a collider (Lemmas 2.3–2.4).**<br>- The router (shared remainder, inputs ±2u±, u+ + u− = 3Q) gives EXACTLY one click per quantum for every remainder, with no confirmation.<br>- Selecting on a confirmation C gives P(λ\|x,y,C) ∝ P(λ)c_A(λ,x)c_B(λ,y). MI breaks iff the weights depend jointly on λ and the setting; with the ratio router, δ_C = 0 | THEOREM + BUILT | p1_results.json (design R: P(C) = 1, δ_C = 0 exactly) | |
| Y5 | **No freeze ⇒ only MI can give S > 2 (THEOREM 3.1).**<br>- Click time = board time.<br>- At board-spacelike records, PI and OI hold (cone + determinism), so S ≤ 2 + 6δ.<br>- Typical seeds with fresh choosers give δ = 0, so S ≤ 2. Fresh choosers exist: a quiet gear (a = b = u = 0) holds r exactly and emits nothing until triggered.<br>- PI ("locality on the board") is never dropped | THEOREM | §3 | |
| Y6 | **Forward confirmation ⇒ visible delay (THEOREM 3.2 + Cor. 3.2′).**<br>- F1/F2: a record that depends on y waits ≥ d/v_max after y. With no freeze every lab clock shows it (s14 V1: partner decision + 2R; s20 hid it only with the now-forbidden hold).<br>- F0 (absorber-first request): no click waits, but y must precede the emission by ≥ d/v. y then reaches A's record via the source, so the records are not spacelike to it. FAILS vs fast switching / freedom of choice (lit.) | THEOREM + cited NUMERIC | §3; s14 C1/X4; s16 row 11; s20 Z2/ZB6 | |
| Y7 | **The owner's rule in its strongest outcome-blind form, exact on one board.** S1/S2 = "exactly one click per station", independent exits, CHSH grid:<br>- D = 30: **S = 271800/110143 = 2.4677**; δ_C = 149/527; P(C) = 110143/202500 = 0.544 for all 4 pairs; E(0) = 2025/2441 = 0.830; marginals ½ EXACTLY.<br>- D = 606: 2.5122. Continuum max 16√2/9 = 2.514; E(0) = 16/19.<br>- 60° grid, D = 30: 2.1757, with setting-dependent P(C).<br>- Asymmetric exits: S_C = 2.27, **signalling 0.147**.<br>- Router: 302/225 (CHSH grid), 806/675 (60°).<br>- Arc scan: S_C > 2 only for arc fraction η > 5/8 | BUILT + NUMERIC (exact Fractions, divmod over all r) | p1_results.json, p4 (POST HOC), p5_results.json | |
| Y8 | **Fine-tuning of the seed door (THEOREM 3.3).**<br>- (a) μ0{N-trial CHSH estimator ≥ 2√2} ≤ e^(−0.021447N) (Azuma–Hoeffding).<br>- (b) i.i.d. Tsirelson records need D(μ‖μ0) ≥ 0.0320746·N nats (0.0462738 bits per trial, = lit.).<br>- (c) An all-or-nothing confirmation with setting-independent rate p has S ≤ 2/p, TIGHT (exact LP). So 2√2 needs ≤ 2^(−N/2) of the seeds.<br>- Typical seeds: δ = 0. A mod-D conservation law gives δ = 0.<br>- Simple seed laws are erased by mixing pads or ECHO at t ≡ 0 mod 4 (P3.b) | THEOREM + NUMERIC | p2_results.json, p3_results.json, p6_results.json | |
| Y9 | **No-signalling and Tsirelson (THEOREMS 3.4–3.5).**<br>- NS is a THEOREM of the law in NO reading with S > 2:<br>  - S: a design symmetry (τ: φ → φ + 90°). Asymmetric exits signal 0.147, which under the S2 law is a REAL FTL signal;<br>  - F2: reader design (relabelling lemma; a theorem only under a reader-class NEW LAW, s23 N1/RB8);<br>  - D/F1: the cone, but S ≤ 2.<br>- Tsirelson is derived in NO reading:<br>  - selection reaches 4;<br>  - the natural rule gives 2.514 with E(0) = 16/19;<br>  - an exact singlet among confirmed pairs needs a designed confirmation function, which is circular;<br>  - F2 reaches it only via the s20 reader class L0–L3 (OPEN) | THEOREM + NUMERIC | §3; p1 (I-asym) | |
| Y10 | **Owner verdict.**<br>- "Bell stands" (spacelike, typical seed, no freeze): FAILS.<br>- The only door is the seed law S2: a NEW LAW, superdeterministic (= retrocausal here). It needs no freeze and no tensor change, and is outcome-blind (not circular), but it forces the seed by its own future. Costs:<br>  - δ ≥ 0.138 for 2√2;<br>  - seeds ≤ e^(−0.0214N);<br>  - natural form: S = 2.47 (D = 30) with E(0) = 0.83;<br>  - no NS theorem (asymmetric exits ⇒ FTL), no Tsirelson;<br>  - it predicts 100 % detector efficiency.<br>- Forward confirmation: a visible delay | DERIVED → OWNER | PROPOSAL §0, §4 | |
| Y11 | **Literature (lit., from memory) and the board mapping:**<br>- Cramer TI (1986) → S2 or H; Wheeler–Feynman (1945/49) → D or S2; TSVF/ABL (1964) → D2 or S2;<br>- 't Hooft CAI (2016) → S2 with δ forced into the seed;<br>- Wharton–Argaman (2020), Leifer–Pusey (2017): retrocausal ≡ superdeterministic on a bijective board;<br>- detection loophole (Pearle 1970; Garg–Mermin 1987; Larsson 1998; Eberhard 1993; Gisin–Gisin 1999) → S1; loophole-free 2015 tests close it;<br>- van Dam–Gill–Grünwald (2005) = P2 | lit. + DERIVED | §5 | |
- Honesty ledger (BELL-Y):
  - P3.b PARTLY FAILED: δ came back to 1 at t = 4 (a period-4 echo).
  - P6's registered frontier form FAILED: the frontier is 2/p, not 4/p − 2.
  - Both are kept and sharpen Y8.

### BELL-Y SIGNATURE
- Marks on BELL-X rows:
  - ACCEPT: X3, X4, X5, X6, X13, X14.
  - ACCEPT + EDIT: X1, X2, X7, X9, X10, X11, X12, X15, X16, X17, E.
  - X8: ACCEPT (1), (2), (4), with a substantive EDIT on (3). Setting-free completion covers the DYNAMICAL one-click
    law, not the owner's rule as a seed LAW (S2), where MI fails and S = 2.4677 (D = 30) with no discarded clicks.
  - **DISAGREE: none.**
- Own rows Y1–Y11 are above for BELL-X to mark. Until marked they are BELL-Y claims, not joint rows.
- **Joint verdict (BELL-Y):**
  - With NO freeze and a typical seed, Bell does NOT stand (THEOREM; S ≤ 2 exactly).
  - The owner's rule's only lawful door is a seed law (two-time boundary = retrocausal = superdeterministic on this
    bijective board). It is fine-tuned: ≤ e^(−0.0214N) of seeds for 2√2, rigorous.
  - It has no no-signalling theorem and no Tsirelson.
  - A forward confirmation makes the records wait, visibly.
  - Push gate "Bell stands": NOT met.
- Evidence:
  - s27/BELL-Y_PROPOSAL.md (frozen 17:04:51, sha256 fa75cb45…38839a84; copy BELL-Y_work/BELL-Y_PROPOSAL_frozen.md);
  - s27/BELL-Y_NOTES.md (PRE-REGISTRATIONS 1–3, every result, two FAILED predictions kept);
  - s27/BELL-Y_work/ (p1–p6 *.py and *_results.json, SHA256.txt).
- **Signed by BELL-Y: Tue Nov 10 17:06:50 UTC 2026 (date -u).**

---------------------------------------------------------------------------------------------------------------------
## BELL-X FINAL SECTION (appended by BELL-X; nothing above edited)
- BELL-X_PROPOSAL.md FROZEN at Tue Nov 10 17:05:02 UTC 2026, sha256 4d49ed7faf08f5f5307ddf995c1238b64f5e9cecd6b81c724a6234103bfd999e
  (copy BELL-X_work/BELL-X_PROPOSAL_frozen.md). BELL-X opened no BELL-Y file before that stamp.
- File as read after BELL-Y's signature: BELL-X_work/AGREE_B27_as_read_by_X_after_Y_1708.md.
- New BELL-X check for BELL-Y's Y3 (k_parity.py, registered in NOTES §10 before the run): flipping the parity of every
  remainder leaves every a, b and click identical (45 runs, 0 mismatches), the parity survives to the end, and the
  rewinds are exact.

### BELL-X response to BELL-Y's EDITs on X-rows
| # | BELL-X response |
|---|---|
| X1 | **ACCEPT.** O5 sits inside BELL-Y's D/S/F/H: (i) = S, (ii) = F, (iii) = S1 (observer) or S2 (law). My sequential "only confirmed clicks" router is D-type: a design, no selection |
| X2 | **ACCEPT** (confirmed on B27X by k_parity). The backward trace needs the final FULL state. The README line should read "the final full state and the seed determine each other" |
| X7 | **ACCEPT.** "Strict, sequential router: 2" is the DYNAMICAL one-click law. The seed-LAW version (S2) is a different object (X8, X11) |
| X8 | **ACCEPT the substantive EDIT to (3).** THEOREM NF now reads "no freeze AND typical seed (MI) ⇒ Bell holds".<br>- (3) covers the dynamical one-click law only.<br>- Under BELL-Y's S2 seed law the realised world has no single clicks, yet MI fails and S > 2. On B27X the same object is my X11 shared-token ensemble taken as a law: δ = 4/9, S = 22/9, every realised trial confirmed.<br>- (4): ACCEPT the tight frontier S ≤ 2/p (setting-independent rate p) and the attribution of 4/η − 2 to Larsson 1998 (Garg–Mermin 1987: the threshold; lit., from memory). B27X: p = 3/5 gives ≤ 10/3, and 22/9 is below it |
| X9 | **ACCEPT** (S2: MI broken; F2: timelike records, the locality loophole, not a Bell test) |
| X10 | **ACCEPT** (BELL-Y's asymmetric-exit counterexample, signal 0.147, makes "not a theorem" explicit) |
| X11 | **ACCEPT.** My last sentence holds for S1 only. As a LAW (S2) the singles never exist. It pays with MI (δ = 4/9 on B27X, 0.28 on BELL-Y's board), P(C)^N of the seeds (0.6^N on B27X), the wrong curve, 100 % detector efficiency, and no-signalling by symmetry only |
| X12 | **ACCEPT.** Rigorous floors added: μ0{CHSH estimator ≥ 2√2} ≤ e^(−0.021447N) (re-derived: Azuma–Hoeffding with range 8, t = 2√2 − 2, gives exponent t²/32 = (3 − 2√2)/8). An all-or-nothing fair-rate confirmation needs ≤ 2^(−N/2) of the seeds for 2√2 |
| X15 | **ACCEPT** (B27X is the x-line, 1 site per update; on the 3-D board the L1 cone is up to 1.73 c along an axis, so F fails only against margins > 1.73; s14 X4) |
| X16 | **ACCEPT** (add D3 cyclic order (idle), S3 half-data Lagrangian (ill-posed), literal backward process (FAILS, AGENTS 7)) |
| X17 | **ACCEPT** (records also timelike to the far setting via the source) |
| E | **ACCEPT edits (i)–(iv).** Final joint text below |

### BELL-X MARKS on BELL-Y rows Y1–Y11
| # | BELL-X mark | reason |
|---|---|---|
| Y1 | **ACCEPT** | Exhaustive by construction (a law is (U, μ), and board time is the only time). My O5 (i)/(ii)/(iii) and the handshake X17 fall in S/F/S/F; the freeze is H |
| Y2 | **ACCEPT** | = my X14, found independently. The half-data counterexample checked by hand: K = 0 gives (a, b) → (b, −a), so b_T = ±b_0 at even T for any a_0 |
| Y3 | **ACCEPT** (+ independent NUMERIC on B27X) | k_parity.json: 45/45 runs, 0 a/b/click mismatches, parity survives, rewinds exact. Hence "clicks ⇏ seed" (2 seeds per remainder pattern at least) |
| Y4 | **ACCEPT** | = my X3/X5 (one click per quantum by ΣK = D, no confirmation) and X11 (collider: δ = 4/9 shared-token and 5/16 independent on B27X) |
| Y5 | **ACCEPT** | = my X8 (1)–(2) with the "typical seed" qualifier now in NF. B27X's choosers are exactly such quiet gears kicked by a local trigger |
| Y6 | **ACCEPT** | = my X15 + X17 |
| Y7 | **ACCEPT** (not re-run) | Consistent in kind with B27X: the post-selected / S2 value is 22/9 = 2.444 (shared-token exits, 60° grid, D = 30) vs 2.4677 (independent exits, CHSH grid, D = 30). Both are below 2√2. Both have all-pairs S ≤ 2 (B27X: max exactly 2, CH J_max = 0) |
| Y8 | **ACCEPT** | (b) matches my P11 to 5 digits (0.04627 / 0.01776 bits). (a) re-derived. (c) consistent with B27X (22/9 ≤ 2/p = 10/3) |
| Y9 | **ACCEPT** | = my X10, X13 (on B27X's own responses the seed-law family gives 5/2, 2√2, 3, 4 with exact ½ marginals) |
| Y10 | **ACCEPT + EDIT** | Agreed. EDIT, add the BUILT positive part: for ONE quantum the owner's picture is realised exactly on B27X with no freeze (one emission click, the wave on both paths, exactly one absorption click, Born 1/5 : 4/5, the click depends only on its own side back to the emitting click, rewind exact) |
| Y11 | **ACCEPT** | lit., from memory on both sides; not checked online |

### JOINT ANSWER TO THE OWNER (final; both twins' edits included)
- **Built (no freeze, exact).** One quantum works exactly as the owner says:
  - one emission click, the wave on all paths, exactly one absorption click;
  - Born exact;
  - the click depends only on its own path back to the emitting click;
  - rewind exact from the final FULL state (the clicks alone do not fix the seed: the remainder parity is inert).
  "The light chooses the path" = the token of the emitting click: a local hidden variable, which is enough for one
  quantum. One click per quantum comes from ΣK = D; it needs no confirmation.
- **Bell, typical seed, no freeze.** S ≤ 2 (THEOREM: no freeze makes click time = board time, so the cone gives
  locality and fresh choosers give MI). Exactly, on B27X over the whole seed class (1.3M full-board runs):
  - S = 5/4 (independent path tokens);
  - S = 2 at most (one shared path token; also the dynamical "only confirmed clicks" router), with CH J_max = 0.
- **S > 2 only by selection.**
  - S1: the observer discards unconfirmed pairs. This is the detection loophole: 22/9 on B27X, 2.4677 on BELL-Y's
    board. The tight frontier is S ≤ 2/p. Loophole-free tests close it.
  - S2: a LAW that only confirmed histories exist. This is a seed law: two-time boundary = retrocausal =
    superdeterministic on this bijective board. It needs no freeze and no new tensor term, but it costs:
    - MI broken (δ = 4/9 on B27X, 0.28 on BELL-Y's board; ≥ 0.138 for 2√2);
    - fine-tuning: seeds ≤ e^(−0.0214N) for any law reaching 2√2 (rigorous); ≥ 0.0463 bits per trial for Tsirelson
      statistics and ≥ 0.0178 for the grid's 5/2;
    - no no-signalling theorem (asymmetric exits signal) and no Tsirelson (the same family reaches 4);
    - the natural form has the wrong curve (E(0) ≈ 0.83) and predicts 100 % detector efficiency.
- **Forward confirmation** (a front after the absorption, or a request before the emission): it works on one board,
  but every record that uses the far setting is timelike to it. Without a freeze the wait is visible. FAILS against
  timing-margin and fast-switching tests.
- **Verdict.** Bell does NOT stand on the board without a freeze. The push-gate item "Bell stands" is NOT met.

### BELL-X FINAL SIGNATURE
- Marks: Y1–Y9 and Y11 ACCEPT; Y10 ACCEPT + EDIT (adds the built one-quantum result). All of BELL-Y's edits on X1–X17
  and E: ACCEPTED. **DISAGREE: none.**
- Every row is AGREED or AGREED with an accepted EDIT. The joint answer above incorporates both twins' edits.
- **Signed by BELL-X: Tue Nov 10 17:08:24 UTC 2026 (date -u).**

### BELL-Y FINAL CONFIRMATION (appended Tue Nov 10 17:09:03 UTC 2026; nothing above edited)
- **JOINT ANSWER TO THE OWNER (final): CONFIRMED as written.**
  - BELL-X's Y10 EDIT (adds the built one-quantum result) is ACCEPTED: = BELL-Y Lemma 2.3 / P1 design R.
  - BELL-X's responses to all my edits are noted.
  - **DISAGREE: none, in either direction.**
- Precision note, changes no verdict: "E(0) ≈ 0.83" and "100 % detector efficiency" were derived on BELL-Y's
  independent-exit board (D = 30). BELL-Y did not compute B27X's S2 curve.
- File as read before this line: 35926 bytes, sha256 56d030140ffc54f5… (copy BELL-Y_work/AGREE_B27_as_read_by_Y_before_confirm.md).
- **BELL-Y FINAL SIGNATURE: Tue Nov 10 17:09:03 UTC 2026 (date -u).**

### BELL-X note on BELL-Y's precision note (appended Tue Nov 10 17:09:45 UTC 2026; POST HOC, changes no verdict)
- ACCEPTED. The B27X S2 curve is now computed (l_e0.py → l_e0.json, POST HOC, exact): shared-token "both click"
  ensemble, E_C(Δ = 0°, 30°, 60°, 90°) = 1, 7/9, 1/5, −1/9 against the quantum 1, 1/2, −1/2, −1.
- So on B27X the wrong-curve fingerprint is at 90° (−1/9 instead of −1), not at 0°. "E(0) ≈ 0.83" belongs to
  BELL-Y's independent-exit board. "100 % detector efficiency" follows from the S2 law on any board (no miss can exist).
