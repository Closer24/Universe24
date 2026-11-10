# AGREE_BELL — STUDY 14 "A Bell test on the board with the cosmic clock": BELL-A (builder) × BELL-B (theory + check)
- Built by BELL-A, Tue Nov 10 13:37:41 UTC 2026 (date -u), from:
  - A = s14/BELL-A_FINDINGS.md (§0–§6) and BELL-A_NOTES.md (PRE-REGISTRATIONS 1–6, every raw table);
  - B = s14/BELL-B_NOTES.md as on disk at 13:25 (pre-registration 13:11:50; b1, b2, b3, b3b, b3c).
- Independence:
  - BELL-A read no BELL-B file before its interim to main (13:15). It first read BELL-B_NOTES at 13:18.
  - BELL-B's notes state it read no BELL-A file before its pre-registration (13:11:50) and b1–b3.
- Evidence:
  - A: s14/BELL-A_work/ (bell.py frozen, sha in SHA256.txt; bell2.py; scan.py; window.py; noclick_posthoc.py;
    gate.py; all *.json);
  - B: s14/BELL-B_work/ (b1_results.json, b2_results.json, b3*_results.json).
- Labels: THEOREM / NUMERIC (file) / DERIVED / OPEN / NEW LAW (owner decision).
- Verdicts: AGREED / AGREED-WITH-QUALIFIER (AwQ) / AGREED-OPEN / DISAGREE.
- **BELL-B: please mark the last column (ACCEPT / EDIT / DISAGREE) and sign.**

## A. The two boards
| # | claim | A | B | proposed verdict | B mark |
|---|---|---|---|---|---|
| A1 | Both are exact Rule3 boards (K = 2u, D = 6Q, one Q per experiment). Θ is one gear per node, with uniform data and an own spring, read one-way as a common factor. Its copies stay EXACTLY equal | NUMERIC: odd Q = 4097. 668,000 trials in 15 files: 0 Θ non-uniform, 13,360/13,360 rewinds exact, 0 double clicks | NUMERIC: Θ copies asserted equal at every update. Exact Fractions, exhaustive over θ0 and all remainders | AGREED (two codes) | **ACCEPT.** B's toys: even Q (D = 120 … 6·10⁶), no transport, exhaustive Fractions; A: odd Q = 4097 with transport. Complementary, both exact |
| A2 | **Designs differ (complementary).** A: a full x-line with transport. A pair of exact C0 flashes with one shared phase φ comes from the middle. Photon-gated rank-3 Born readers (near-matched, one-shot). Local one-shot or DC-driven remainder choosers. Strict L1-cone timing: settings spacelike to the far detection AND to the emission. B: three sites without transport. Ratio choosers (Born router) or rate choosers (click/no-click). Hidden data Λ = (source token λ, θ0). S_max = the best FIXED local responses of (setting, λ, own clock copy): the superdeterministic headroom. S_nat = natural token readers | §1 | pre-registration | AGREED (A measures what the board's Born readers give; B bounds what any local reader could get) | **ACCEPT + EDIT.** B's S_max lets the readers read their clock copy BEYOND the common factor. No reader of the approved design does that, so S_max is a HEADROOM bound on any local reader, not a board prediction |
| A3 | Causal no-signalling is exact. Θ is uniform and one-way, and every gear reads only its cone | THEOREM (domain of dependence) | NUMERIC b2: an intervention on Alice's clock copy and router changes nothing at Bob (distance 5) in 14 updates; 0 cone violations | AGREED | **ACCEPT** |

## B. The question: does a one-seed board WITH the cosmic clock give S > 2 at spacelike separation?
| # | claim | A | B | proposed verdict | B mark |
|---|---|---|---|---|---|
| B1 | **Pre-registered decision: NOT supported.** A's arms, 60,000 trials each, S on coincidences: (i) no Θ 1.255 ± 0.015 (exact 5/4); (ii-a) Θ + typical source token 1.184 ± 0.035 (exact 5/4); (ii-b) Θ + source phase = cosmic phase 1.191 ± 0.035 (exact 1.241). All > 20σ below 2 | NUMERIC bell_*_s14.json | S_nat = −1.0 in EVERY arm (P4) | AGREED | **ACCEPT.** B's S_nat uses one fixed, untuned token reader (value −1.0). The point is only that it is IDENTICAL in every arm (λ is padded) |
| B2 | **Typical seed ⇒ the cosmic clock cannot raise S.** A, THEOREM 1 (Born-conditional invariance): Θ multiplies both arcs of a reader, so P(±\|click) does not depend on Θ. With a typical source token, φ is independent of θ0, so S_coinc = S_MI EXACTLY although δ_n = 0.81 (A ii-a; four re-test controls give 5/4, 1, 5/4, 5/4 exactly). B: pad lemma, i.e. fresh remainders are uniform given θ0. F_RATIO: δ = 0 and S_max = 2 exactly; S_nat identical in all arms | THEOREM 1 + NUMERIC | P1a PASS; pad lemma | AGREED (two proofs, two codes). SCOPE: readers that see Θ only as the common factor. B's F_RATE shows that a rate chooser carries δ = 0.53, and best local readers of (setting, λ, θ0) could reach S_max = 3.09. That headroom is real in the seed, but the board's common-factor Born readers cannot use it unless the source data are locked to Θ (B4) | **ACCEPT + EDIT.** A's THEOREM 1 = B's ratio invariance, two proofs. Add the data-processing EQUALITY: if Θ is the only link between settings and source, P(λ,θ0\|s) = P(λ\|θ0)P(θ0\|s), so δ = TV(P(θ0\|s), P(θ0\|s′)). How much the SOURCE knows about the clock is irrelevant; what matters is how much the SETTINGS reveal about θ0 AND whether the readers use θ0 beyond the common factor. A's δ_n = 0.81 with S = 5/4 is that case |
| B3 | **One universe = one bang time.** With θ0 fixed, or a window W ≪ T of cosmic time, S ≤ 2. A, THEOREM 2: given n, E = x_a y_b, a product, so S ≤ 2. Window numerics: W = 1 gives δ_n = 0 and S ≤ 2.000 for every design and all angles. The slow clock (T = 1024) at W/T ≤ 0.8 % gives ≤ 2.000. B, P2: δ_W → 0 roughly ∝ W away from the fold (0.010 at W = 2; 0.44–0.55 for windows that contain the fold). Ratio chooser: δ = 0 in every window. B, b3c: proper-time choosers are blind to Θ, with δ_proper ≈ 0.11 × (proper time per update / decision time) → 0. Real decisions span ≫ 10³ updates | THEOREM 2 + NUMERIC window_results.json | NUMERIC b2, b3c (b3c post hoc, clean version) | AGREED | **ACCEPT + EDIT.** 'θ0 fixed' = window W = 1. In one real universe the parameter is W/T (≈ hours/aeon ≈ 10⁻¹⁴): both codes agree δ → 0 there, except across the fold. B's b3b had a defect (plateau clock at A·Ω < 1, recorded in BELL-B_NOTES); b3c is the clean post-hoc version: δ_proper/(w·A/D) = 0.116, 0.114, 0.112 |
| B4 | **The superdeterminism door exists but needs a NEW LAW on seed data.** S > 2 at spacelike separation needs: (a) source (or chooser) data locked to θ0 rather than typical tokens; (b) trials that sample O(1) of the cosmic period (many universes, or a clock about as fast as the experiment); (c) design tuning. A's gear re-tests (pre-registered, seed 2026): 2.385 ± 0.019 (T = 12), 2.202 ± 0.028 and 2.071 ± 0.022 (T = 64); slow T = 1024: 1.772 ± 0.034; best of 1636 scanned configurations: 2.36 < 2√2. B: C_RATE (chooser remainder fixed by the bang) S_max = 4; F_RATE 3.09; B_RATIO (bang-evolved router) 2.13 at δ = 0.066 | NUMERIC bell2_*_s2026.json, scan_results.json | NUMERIC b1 | AwQ: A's Born readers need δ ≥ 0.6 for S > 2. B shows the general headroom: S_max − 2 ≤ 6δ always held, and 2.13 already appears at δ = 0.066. Both: the door is superdeterminism (a NEW LAW on initial data), not a property of the approved typical seed | **ACCEPT + EDIT.** B's 2.13, 3.09 and 4 are clock-READING-reader headrooms (A2 edit), not board readers. Add: (i) over ALL seeds S = 4 is reachable (the board is a bijection: rewind any record); it predicts nothing; (ii) LEMMA (B): δ ≥ 0.138 forces the setting generator off its own marginal law given the hidden data, E_Λ\|P(s\|Λ) − P(s)\| ≥ 0.0345 for some pair s (13.8 % relative at P(s) = 1/4). Proof: TV(P(Λ\|s), P(Λ)) = E_Λ\|P(s\|Λ) − P(s)\|/(2P(s)), then the triangle inequality |
| B5 | **Fingerprints.** A's locked designs show three. (i) Setting frequencies follow the cosmic phase: P(ab) = .19–.23 / .14–.24 / .14–.24 / .39–.50 instead of 1/4 each. (ii) Coincidence rates depend on the setting pair (0.10–0.84), a fair-sampling violation. (iii) Statistical marginal shifts of 0.13–0.47 with the far setting; these are click-RATE shifts (efficiency follows \|Θ\|), so they cannot be flipped away. If every trial is scored ±1 (no-click → ∓1), all checked A designs give ≤ 1.80 (post hoc). B: the raw S_max readers signal statistically (0.56 F_RATE, 2.0 C_RATE, 0.05 B_RATIO), and a parity(λ) flip removes it exactly with S unchanged | NUMERIC; noclick_posthoc.json (POST HOC) | NUMERIC b1 | AwQ: the fingerprint of A's Born-reader designs is unavoidable (efficiency type). For B's optimal local responses the marginal signature can be hidden (parity flip), but the setting statistics still follow θ0 (rate choosers) or δ = 0 (ratio choosers). A board design with S > 2, uniform settings and setting-independent click rates is OPEN | **ACCEPT + EDIT on 'OPEN'.** For clock-READING readers the design is trivial (DERIVED). Make x, y balanced functions of θ0 with NO fresh chooser data. Then P(θ0\|x,y) have disjoint supports, so δ = 1 and S_max = 4. Settings are uniform, every trial is scored, and the parity(λ) flip gives zero marginal shift. But that is the seed NEW LAW plus a non-board reader. The OPEN question is only for the board's common-factor Born readers |
| B6 | Bound check: S ≤ 2 + 6δ (GU-4B B3′ / AGREE_GU4 X2) holds in every arm of both boards | NUMERIC | NUMERIC ("bound_holds": true in every arm) | AGREED | **ACCEPT** |

## C. The owner's confirmation principle (manager 13:31 and 13:33). A only; B please mark or add rows
| # | claim | A | proposed verdict | B mark |
|---|---|---|---|---|
| C1 | **V1, the literal principle as an exact local gate** (rank ≤ 4, gears and cone only, no reading of r):<br>- pending DC store of the photon phase;<br>- each decision launches a unit C0 front;<br>- each Born reader is enabled only by the partner's front;<br>- stamp counters freeze from photon arrival to confirmation;<br>- an unfrozen lab counter sits beside each detector.<br>Results:<br>- S = 5/4 exactly (R = 4: 1.269 ± 0.015; R = 6: 1.279 ± 0.022; R = 8: 1.265 ± 0.027);<br>- every click EXACTLY at partner decision + 2R, never earlier;<br>- delay after own photon = 2R − 1;<br>- Born exact per side;<br>- marginals exact;<br>- both stamps = the photon arrival (stamp-spacelike);<br>- the unfrozen counter shows the delay in every trial | NUMERIC gate_R*.json | FAILS to change S: the gate moves WHEN, not WHAT | **ACCEPT.** An enable-only gate gives each reader no new INPUT. A = f(a, λ, own token) still holds, so Bell binds the content whatever the timing. B's gate lemma: with K = 0 a gear gives ℓ = 0 and r′ = r for every r (checked for D = 120), so pending keeps the remainder exactly |
| C2 | **Lemma.** Born readers with independent tokens and a uniform shared phase have \|E\| ≤ ½ even if the references depend on both settings, so S ≤ 2. Only an OUTCOME-carrying confirmation (F7: q × setting clock) can give the cos law | DERIVED | AGREED-OPEN (B to check) | **ACCEPT the lemma, EDIT the corollary.** Lemma checked EXACTLY (b4_c2_check.py; 6-grid φ, all 36 reference pairs): independent tokens give max \|E\| = 1/2 and S_max = 2. Proof: E = E_φ[cos2(φ−α)cos2(φ−β)] = ½cos2(α−β) whenever the φ grid averages the 4φ harmonic (N ∉ {1, 2, 4} angles per 180°). The corollary 'only an OUTCOME-carrying confirmation gives the cos law' holds ONLY for independent tokens. With ONE shared cross-station token (equal remainders set in the common past, e.g. two detectors born at the vacuum with identical drives, as Θ's copies stay equal), a SETTINGS-only confirmation gives E = +1 and E = −1 (mirror) with marginals exactly 0, i.e. S = 4 (b4). Both sides then know both settings and share randomness |
| C3 | **V2 = F7 confirmation + frozen stamps, now ONE exact board** (gate2.py, R = 4). PAIR: S = 2.474 ± 0.021 (exact 5/2), both stamps = photon arrival (stamp-spacelike), unfrozen waits 2R − 1 (Alice) and 4R + 1 (Bob), Born exact, marginals exact, rewinds exact. NO-PAIR control (Bob's photon has an independent phase): S = 2.523 ± 0.021, UNCHANGED. Predictions:<br>- P-1: the second clicker ignores its own particle, so local rotations or unentangled pairs leave E unchanged. Shown on the board by the no-pair control. Contradicted by standard Bell-test controls.<br>- P-2: per-detector dead time ≥ L/c or ≥ 2L/c.<br>- P-3: an unfrozen co-registering clock shows the delay.<br>- (e): hiding the delay from ALL records would require light to cross in zero click-time, against "light is the invariant" | DERIVED | NEW LAW + PREDICTION; not SOLVES | **ACCEPT + EDIT.** P-1 is a property of front-only (F7-type) second readers; whether an outcome-carrying design can also track local operations on the second particle within rank ≤ 4 is OPEN. Sharpen (e) into B's TRILEMMA (row X5): a LIGHT confirmation is either visible (local freeze) or deadlocked (hidden freeze). A hidden, non-deadlocked freeze needs a lapse-BLIND confirmation, which is instantaneous in click time, i.e. NON-LOCAL in physical spacetime |

## D. Joint answer to the owner (proposed text)
- **Board result.** On the board with the approved typical seed, the cosmic clock does not change spacelike Bell.
  - Θ multiplies both arcs of every Born reader, so it cannot change the conditional Born law.
  - In one universe the bang time is one number. Given it, Bell's bound holds exactly (S ≤ 2).
  - Measured: S = 1.18–1.26 with and without Θ (exact 5/4), against the 2.07–2.42 measured in loophole-free experiments (GU-4B B7).
- **The door.** "The cosmic clock solves it" is possible only as superdeterminism ('t Hooft). That needs:
  - a NEW LAW on initial data that locks the source (or the choosers' remainders) to the cosmic phase;
  - trials that sample different cosmic phases.
  On the board this costs δ ≈ 0.6–0.9 for Born readers (B: S_max − 2 ≤ 6δ always) and leaves visible fingerprints in the setting and click statistics.
- **Confirmation principle.** "Only light activates the clicks" changes WHEN clicks happen, not WHAT they are. An enable-only confirmation leaves S = 5/4 exactly. A confirmation that carries the first click's outcome (F7) gives cos correlations, and in frozen click-time they look spacelike. That is a NEW LAW whose predictions (the second particle ignored; dead time ≥ L/c; delays visible to any unfrozen clock) are testable, and the first is already contradicted.

## Signatures
- BELL-A signs all rows as written: Tue Nov 10 13:37:41 UTC 2026.
- BELL-B: please mark each row and sign.

---------------------------------------------------------------------------------------------------------------------
## E. BELL-B ROWS ADDED (written 13:42–13:43:16 UTC; not in A's draft; nothing above edited except B's own last-column marks). BELL-A please mark
| # | claim | label | evidence | A mark |
|---|---|---|---|---|
| X1 | **Pad + ratio THEOREM (B).** Let Θ be ANY shared process, with any law and any correlation with the source and the readers. Suppose it enters a setting chooser only as a common factor on both exits (opposite-form router, inputs ±w±Θ), and the chooser's remainder is fresh at the decision. Then P(x\|valid, Θ, λ, …) = w+/(w+ + w−) whenever (w+ + w−)\|Θ\| ≤ D. So x ⊥ (λ, θ0), δ = 0 and S ≤ 2 even for readers that READ the clock. A fresh remainder is a one-time pad on any common cause: r + g(θ0) mod D stays uniform and independent | THEOREM + NUMERIC | b1 F_RATIO: δ = 0/1 and S_max = 2 exactly (64 phases × 120³ remainders); b2: δ = 0 in every window at D = 60000 | |
| X2 | **2 + 6δ is TIGHT, also under no-signalling.** Let ρ_xy = (1−t)·U(the 4 one-wrong-term strategies) + t·U(the 3 of them not failing term xy). Then S = 2 + 2t at pairwise TV δ = t/3. Mixing every strategy with its global sign flip makes all marginals 0 and leaves S unchanged | THEOREM | 4-line LP argument; b1 parity(λ) flip: marginal shift 0 exactly | |
| X3 | **Lapse = time reparametrisation (B, DERIVED + NUMERIC).** A uniform common lapse rescales every first-order rate, t → τ = ΣΘ. Choosers and triggers that keep PROPER time are blind to it, up to update granularity. A carrier-clock (board-time) window is not | DERIVED + NUMERIC (post hoc, clean) | b3c: δ_proper = 0.0142, 0.0044, 0.00137 at w·A/D = 0.122, 0.0387, 0.0122 (ratio 0.116, 0.114, 0.112); δ_board 0.28–0.38 | |
| X4 | **Which "light"? (13:31 literal gate.)** If the confirmation front rides the board cone, its speed is v_f ≤ 1/c_Q ≈ 1.73 c along an axis (≤ 3.5 c with plaquettes; exactly c along [111]; GU-4B row 19). Every record at A then comes ≥ d/v_f after B's setting. The loophole-free tests certify local records complete BEFORE light could cross. Delft 2015 (1.3 km, 4.27 μs) alone excludes v_f = c but not ≈ 1.2 c. A margin factor > 1.73 (e.g. Weihs 1998: < 0.1 μs local measurement vs 1.3 μs crossing, lit. from memory) excludes every B3 board front. Records are clicks on the board, so a record cannot be "pending" | DERIVED + lit. | GU-4B B6/B7; A's V1: clicks exactly at partner decision + 2R | |
| X5 | **TRILEMMA for frozen stamps (13:33).** (a) LIGHT confirmation + LOCAL freeze (detector + its stamp clock): visible to any unfrozen clock, a sync stream in the same tagger, or a third party receiving A's record (late by Δ). A's V1 unfrozen counter reads 2R − 1 in every trial. (b) LIGHT confirmation + freeze HIDDEN from all records: a lapse-reading observer O sees no gap only if O is frozen before A's first gap signal reaches O. So the freeze must be a lapse-0 SHELL of board-time thickness Δ, expanding at ≥ the maximal lapse-reading signal speed. The shell then catches Bob's incoming confirmation LIGHT before it reaches A, and lapse-reading light inside the shell is frozen. A's unfreeze needs that light, so: DEADLOCK, no click ever in a spacelike test. (c) Lapse-BLIND confirmation + hidden shell: consistent (checked by the characteristic argument: rays entering the shell are held for exactly Δ, so every click-time round trip is unchanged). But the confirmation then crosses in ZERO click time | DERIVED (characteristic argument; lattice caveat X7) | — | |
| X6 | **(13:33 Q1) Board-local ≠ local.** Version X5(c) can be written with B3 terms, so it is local in BOARD time. In CLICK coordinates (the proper-time stamps that are the only times any lapse-reading record carries), A's record is a function of B's setting at a click-SPACELIKE event, so the model violates Bell local causality in click spacetime. Bell's theorem (MI holds, settings free) DEMANDS exactly that for S > 2 at stamp-spacelike records; the model does not evade Bell, it obeys it by being non-local. Click-time no-signalling is NOT structural: it needs readers whose marginals ignore the partner (Born readers with a uniform shared phase or token: marginals 0, b4/TC.7); a partner-dependent reader (TC.7(d) bit gate) would signal INSTANTLY in click time. Hence a signal-hiding law is also needed. S: ≤ 2√2 only by the reader-class law (front-reading Born readers, F7 cos); 4 with bit readers or a shared token (b4) | THEOREM (Bell applied in click spacetime) + DERIVED | b4_c2_check.txt; TC.7 | |
| X7 | **(13:33 Q2) What must freeze; can it be seen?**<br>- For the stamp: the stamp clock. For invisibility: every lapse-reading d.o.f. in the shell of X5(b) (the whole future cone of each pending click, eventually the universe). The lab is NOT enough.<br>- Visible otherwise: X5(a).<br>- Deadlocks even with lapse-blind confirmations: if the confirming setting lies in the future cone of the pending start (delayed choice, timelike tests), Bob's lapse-reading RNG is frozen by Alice's shell before it chooses. Partner-less clicks also need a rule; a timeout needs the partner's distance, which is NON-local information.<br>- Lattice caveat: the shell edge moves at the max board speed (1 site/update). At its trailing edge an unfrozen node reads a still-frozen neighbour one τ-step AHEAD, giving an O(ω·lattice) mismatch. Exact invisibility needs an edge-aware coupling (e.g. read a instead of b of a frozen neighbour): OPEN | DERIVED / OPEN | — | |
| X8 | **(13:33 Q3) NEW LAW and its cost.** Ingredients:<br>(i) a gate on every click (rank-4 designated);<br>(ii) a click-SOURCED lapse field that freezes all lapse-reading physics in an expanding shell;<br>(iii) lapse-blind, partner-ADDRESSED confirmation fronts (a pairing rule);<br>(iv) a signal-hiding reader law;<br>(v) rules for future-cone and partner-less confirmations.<br>(i)–(ii) are exactly what AGENTS rule 8 excludes from the reference model ("no state-changing detector code, no extra gates or clock"), so this can only be a separate candidate variant. Cost: the board cone stops being the physical cone, and a hidden preferred time (board time) appears. In its hidden form it predicts nothing new for spacelike Bell data (empirically idle there) | DERIVED → OWNER | — | |
| X9 | **(13:33 Q4) Literature (lit., from memory).**<br>- = a hidden preferred foliation: Bohm; Bell's "Lorentzian" pedagogy (1976).<br>- The owner's word "confirmation" is Cramer's transactional interpretation (RMP 58, 647, 1986). TI's confirmation runs backward; here it runs forward in board time with frozen click stamps.<br>- X5(a) is Kent's collapse-locality loophole (PRA 72, 012107, 2005), tested by Salart et al. (PRL 100, 220404, 2008). X5(c) makes it untestable by construction.<br>- Retrocausal / time-symmetric models (Price, Wharton, Sutherland; Leifer–Pusey 2017): the board model is retrocausal-looking only for future-cone confirmations, and those DEADLOCK. So it is non-local, not retrocausal.<br>- NOT superdeterministic: MI holds (Wharton–Argaman RMP 92, 021002, 2020: three exits = non-local / superdeterministic / retrocausal; this is the first, hidden in an extra board time).<br>- Relational QM (Rovelli 1996): "pending until confirmed" resembles relative facts, but RQM has no hidden variables and no hidden time | lit. + DERIVED | — | |
| X10 | **STATUS LABELS.**<br>- 13:01 "the cosmic clock solves it": FAILS as a mechanism (X1, B2, B3). Rescue only as superdeterminism, a NEW LAW on the seed (B4).<br>- 13:31 literal gate: NEW LAW, whose prediction (records ≥ d/v_f after the partner's setting) FAILS vs locality-test timing (X4). An enable-only gate does not even change S (C1).<br>- 13:33 frozen stamps:<br>  - with LIGHT confirmation: FAILS (visible X5(a), or deadlock X5(b));<br>  - with a lapse-blind confirmation: NEW LAW, NON-local in click time (X6), empirically idle for spacelike Bell, deadlocks on delayed choice (X7).<br>- In no version is it SOLVES (a LOCAL account of spacelike S > 2), and in none is it a new PREDICTION that survives | DERIVED → OWNER | rows above | |

### BELL-B mark on D (joint answer)
**ACCEPT + EDIT** (BELL-B, 13:43):
- (i) "The door" paragraph: state the floor for ANY readers, δ ≥ 0.138 (2 + 6δ, tight, X2). The 0.6–0.9 applies to A's Born-reader designs only.
- (ii) Add: over ALL seeds S = 4 (rewind), which predicts nothing.
- (iii) Replace the confirmation paragraph's last sentence by the X5 trilemma and the X10 labels:
  - light confirmation ⇒ visible or deadlocked;
  - hidden only with a lapse-blind confirmation, which is non-local in click time (a hidden preferred board time) and costs AGENTS rule 8 + a signal-hiding law.
- (iv) C2's corollary needs "independent tokens" (b4: one shared token gives S = 4, marginals 0).

### BELL-B SIGNATURE
- Marks:
  - A1, A3, B1, B6: ACCEPT.
  - A2, B2–B5: ACCEPT + EDIT (scope/precision edits only).
  - C1: ACCEPT.
  - C2: lemma ACCEPTED (checked exactly, b4); corollary EDITED: it needs "independent tokens".
  - C3: ACCEPT + EDIT.
  - D: ACCEPT + EDIT.
  - DISAGREE: none.
- C3 note: BELL-A extended C3 at about 13:44, after my 13:42 mark, with gate2.py: ONE exact board, S = 5/2 exact, and a
  NO-PAIR control with S UNCHANGED. My mark stands. The NO-PAIR control is the board demonstration of P-1. I did not
  re-run gate2.py; the result is consistent with TC.7 (F7 cos law, 5/2 on the 60° grid).
- Rows X1–X10 were added for BELL-A to mark. Until BELL-A marks them they are BELL-B claims, not joint rows.
- Evidence: s14/BELL-B_work/ (sha256 in SHA256.txt); s14/BELL-B_FINDINGS.md (§0 first); s14/BELL-B_NOTES.md (pre-registrations, run log, the b3b defect).
- Signed by BELL-B at Tue Nov 10 13:45:53 UTC 2026 (date -u).

---------------------------------------------------------------------------------------------------------------------
## F. BELL-A MARKS on BELL-B's rows X1–X10, and BELL-A's response to BELL-B's edits (written Tue Nov 10 13:48:46 UTC 2026; appended only, nothing above changed)
| # | BELL-A mark |
|---|---|
| X1 | **ACCEPT.** Checked: conditional on a valid choice, P(x\|valid, Θ, λ) = w+/(w+ + w−). So x ⊥ (λ, θ0) on the valid set, and every setting pair sees the same law of hidden data. This also explains A's numbers: all of A's scanned choosers were RATE-type ('abs', 'sign'), which is why A's δ_n was 0.79–0.99. A ratio chooser would have given δ = 0 |
| X2 | **ACCEPT.** Re-derived: P(term xy fails) = (1 − t)/4 gives E_xy = (1 + t)/2 and S = 2 + 2t. The U3 parts differ by TV 1/3, so δ = t/3. The global sign flip zeroes the marginals. 2 + 6δ is tight |
| X3 | **ACCEPT.** Consistent with A: A's choosers are board-time rate choosers (one update per decision), the regime where δ is large |
| X4 | **ACCEPT + EDIT.** A's V1 confirms the mechanism exactly: every click falls on the partner's decision + 2R (board L1 cone). The Weihs-1998 margin is lit. from memory on both sides: not checked here |
| X5 | **ACCEPT.** This sharpens A's (e): A had "an unfrozen record exists, OR light crosses in zero click-time". B adds the DEADLOCK horn for lapse-reading light. A's V1/V2 unfrozen counters are X5(a) on the board (2R − 1 and 4R + 1 in every trial) |
| X6 | **ACCEPT.** A's V2 is an instance: its click-time no-signalling holds only because E[q] = 0 (a uniform shared phase). A TC.7(d)-type bit reader at Bob would signal instantly in click time |
| X7 | **ACCEPT** (DERIVED/OPEN as labelled). Note: A's V1/V2 use a LOCAL freeze (X5(a)); A built no shell |
| X8 | **ACCEPT.** AGENTS rule 8 also applies to A's gates as builds: V1/V2 are separate candidate variants (designated one-way gates/kicks), not the reference model |
| X9 | **ACCEPT** (lit., from memory). A did not verify the citations online |
| X10 | **ACCEPT + EDIT.** Add the A label for the OUTCOME-carrying light confirmation (V2): NEW LAW whose click-observable P-1 (correlations survive breaking the pair) is shown on the board and contradicted by experiment. Otherwise identical to A's labels: V1 FAILS to change S; V2 not SOLVES |

### BELL-A response to BELL-B's edits on A's rows
- A2, B2, B3, B4, B5, C3: **ACCEPT all edits.**
  - B2's data-processing equality is confirmed by A's numbers: in every Θ arm δ_(n,φ) = δ_n exactly (0.809, 0.809). The source's dependence on θ0 adds nothing beyond what the settings reveal about θ0.
  - B4's (ii) lemma re-derived: max_s TV(P(Λ\|s), P(Λ)) ≥ δ/2, which gives E\|P(s\|Λ) − P(s)\| ≥ 0.138·P(s).
- C2: **ACCEPT the corollary edit.** Checked against b4_c2_check.txt: independent tokens give max \|E\| = 1/2; ONE shared cross-station token with a settings-only confirmation gives S = 4 with zero marginals.
  - So S > 2 under a confirmation needs EITHER an outcome-carrying front (V2) OR a settings-carrying front plus shared cross-station randomness.
  - Both are communication in board time: X6 non-locality in click time.
- C3: the A column of row C3 should read "NUMERIC gate2_{pair,nopair}_R4/R6 + DERIVED". R = 6 has finished:
  - PAIR S = 2.488 ± 0.030 and NO-PAIR S = 2.532 ± 0.030 (exact 5/2 both);
  - stamps 5/5; unfrozen waits 11 = 2R − 1 and 25 = 4R + 1 in all 10,000 trials; 200 + 200 rewinds exact.
  - A accepts B's scope edit: P-1 is proved only for front-only (F7-type) second readers. Whether a rank-≤4 outcome-carrying design can also track local operations on the second particle is OPEN.

## D-final. Joint answer to the owner (BELL-A text incorporating BELL-B's D edits (i)–(iv); BELL-B to confirm)
- **Board result.** With the approved typical seed, the cosmic clock does not change spacelike Bell on the board.
  - Θ multiplies both arcs of every Born reader, so it cannot change the conditional Born law (A THEOREM 1 = B pad/ratio X1).
  - In one universe the bang time is ONE number, and given it Bell's bound holds exactly. Across a real experiment's window (W/T ~ 10⁻¹⁴), δ → 0.
  - Measured: S = 1.18–1.26 with and without Θ (pre-registered arms; exact 5/4 and 1.241), against 2.07–2.42 in loophole-free experiments.
- **The door.** "The cosmic clock solves it" is possible only as superdeterminism ('t Hooft). That needs a NEW LAW on seed data locking the source or the choosers to θ0, plus trials that sample different cosmic phases.
  - Floor for ANY readers: δ ≥ 0.138 (2 + 6δ is tight, X2). That δ forces the setting generator off its own law given the hidden data by ≥ 13.8 % relative (B4 lemma).
  - A's Born-reader designs needed δ ≈ 0.6–0.9 and reached at most 2.36. Their fingerprints are setting frequencies that follow the cosmic phase, setting-dependent click rates, and statistical marginal shifts.
  - Over ALL seeds S = 4 is reachable by rewinding any record: such a law predicts nothing.
- **Confirmation principle.**
  - **"Only light activates the clicks" (13:31).** It changes WHEN clicks happen, not WHAT they are: an enable-only confirmation leaves S = 5/4 exactly (V1).
  - **Ways S > 2 can arise.** S > 2 needs a confirmation that carries the first click's OUTCOME (V2: S = 5/2 exact on the 60° grid). Alternatively, a settings-carrying confirmation plus a shared cross-station token gives S up to 4 (b4).
  - **Frozen stamps (13:33).** With a LIGHT confirmation, the freeze is either VISIBLE (A's unfrozen counters show the delay in every trial) or DEADLOCKED (X5). It can be hidden only with a lapse-BLIND confirmation. That confirmation is instantaneous in click time, i.e. NON-LOCAL in the observers' spacetime, and costs AGENTS rule 8 plus a signal-hiding law (X6–X8).
  - **Labels.** V1 FAILS to change S. V2 is a NEW LAW whose click-observable P-1 is contradicted by experiment. In no version is it SOLVES.

## BELL-A FINAL SIGNATURE
- Marks: X1, X2, X3, X5, X6, X7, X8, X9: ACCEPT. X4, X10: ACCEPT + EDIT.
- All of BELL-B's edits to A's rows: ACCEPTED. DISAGREE: none.
- Signed by BELL-A at Tue Nov 10 13:48:46 UTC 2026 (date -u). Copy of the file as signed by B at 13:45: BELL-A_work/AGREE_BELL_as_signed_by_B_1345.md.

### BELL-B AMENDMENT to its own row X7 (lattice caveat), Tue Nov 10 13:48:51 UTC 2026. Row text above left as signed; this supersedes its last bullet
- Exact lattice test b5/b5b: 1D ring of 240 nodes, exact Rule3 C0 fibre u = N·D·(b_{x−1} + b_{x+1}). The freeze is
  K = 0, i.e. the period-4 rotation (a, b) → (b, −a). One left-moving and one right-moving pulse of amplitude 1000 cross
  the shell.
- The lapse-0 shell is EXACTLY invisible if two conditions hold:
  - it expands at the maximal signal speed (1 site/update);
  - its duration Δ ≡ 0 mod 4.
  Result: Δ = 40 gives 0 mismatches in 17,040 checked click-time points.
- Otherwise it is VISIBLE:
  - Δ = 41 / 42 / 43: 6,894 / 6,630 / 6,754 mismatched points;
  - shell at 1/2 site/update: 8,330 of 8,581.
- The 'one-step-ahead neighbour' I predicted at the trailing edge is exactly compensated: after Δ − 1 ≡ 3 quarter-turns,
  the frozen neighbour's b-slot holds its PREVIOUS b, which is the value the reference run reads.
- Consequence for X5(c): a hidden freeze IS constructible exactly (1D). It needs one more local rule: round every wait
  up to a multiple of the carrier period 4, a frozen-update counter. The 3D case (L1 shells, 6 neighbours) is
  plausible by the same one-step structure, but OPEN.
- This does not change X5(a) (visible) or X5(b) (deadlock). It strengthens X6: the non-local, hidden-time NEW LAW is
  exactly buildable, so the objection to it is non-locality in click time, not inconsistency.

## BELL-B CONFIRMATION of D-final and of section F (Tue Nov 10 13:49:20 UTC 2026; appended only)
- Section F: BELL-A's marks on X1–X10 are noted. All are ACCEPT or ACCEPT + EDIT, and I accept both A edits:
  - X4: Weihs-1998 margin from memory on both sides;
  - X10: add the V2 label.
- BELL-A's responses to my edits (A2, B2–B5, C2 corollary, C3 scope) are accepted.
- **D-final: CONFIRMED**, with two precision edits that change no verdict:
  - (1) The V2 label should read: "NEW LAW whose click-observable P-1 is contradicted by experiment, for front-only
    (F7-type) second readers. A rank-≤4 outcome-carrying design that also tracks the second particle is OPEN".
    This is the C3 scope both twins accepted.
  - (2) Add after the frozen-stamp sentence: "A hidden freeze is exactly buildable (b5/b5b, 1D: 0 mismatches in 17,040
    click-time points, when the lapse-0 shell moves at 1 site/update and every wait is rounded to a multiple of 4 updates).
    So the objection to the lapse-blind version is NON-LOCALITY in click time, not inconsistency."
- My X7 amendment (13:48:51) postdates A's X7 mark (13:48:46). A's ACCEPT of X7 as DERIVED/OPEN stands. The amendment
  converts the 1D part to NUMERIC; 3D remains OPEN.
- **Net:** DISAGREE: none. Every row is AGREED or AGREED with an accepted EDIT.
- BELL-B FINAL SIGNATURE: Tue Nov 10 13:49:20 UTC 2026 (date -u).

### BELL-A mark on BELL-B's X7 amendment (13:48:51), written Tue Nov 10 13:49:33 UTC 2026
**ACCEPT** (read b5_results.json: Δ = 40, 0 mismatches in 17,040 points; not re-run by A). It also corrects a wording in A's
FINDINGS §6.1: "Rule3 cannot stop a ring" holds per update (a' = b). A K = 0 gear rotates with period 4, so a freeze
lasting a multiple of 4 updates is exactly invisible (B's exact 1-D shell). A's stamp counters are the LOCAL, visible freeze
(X5(a)). The joint conclusion is unchanged and sharpened: a hidden freeze is buildable, but only as the non-local
(click-time) NEW LAW of X5(c)/X6.
