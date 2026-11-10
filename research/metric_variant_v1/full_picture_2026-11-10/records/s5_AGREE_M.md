# AGREE_M — Study 5 mathematicians S5-M and S5-M2: twin agreement
Format (manager): claim | S5-M | S5-M2 | verdict | diagnosis. Single editor: S5-M (agreed by S5-M2 at 07:20). Merge begun
after 07:28:19 (`date -u`), from M_FINDINGS.md (S5-M) and M2_FINDINGS.md §0–§14 plus S5-M2's 07:24 message.
STATUS: FINAL, CO-SIGNED by both twins (S5-M2 at 07:32, reconfirmed at 07:37; S5-M at 07:31:15). The later edits are
listed under Signatures.
S5-M2 checked every row (07:30) and co-signs A1–E5 as written. The F rows were agreed and stamped by S5-M at 07:31:15
(`date -u`). The final co-signature of the whole file is S5-M2's. One D3 diagnosis note may follow (S5-M2's m2_fibre_recip,
the reciprocal back-action variant).
Labels: THEOREM / NUMERIC / DERIVED / CONJECTURE / OPEN / MECHANISM. "6 face neighbours: YES" holds for EVERY row; no row
uses a non-face port.

## A. The board and the click
| # | claim | S5-M | S5-M2 | verdict | diagnosis |
|---|---|---|---|---|---|
| A1 | Event space is an exact bijection with two exact reversals: M (the repo's time_reverse, up to the inert parity bit), always, for single-time inputs; and JR = J∘M where J commutes with F (rank-2 inputs). With rank-3 inputs, M and J_arm∘M are the reversors (S5-P E6) | THEOREM (S5M-14; check H) | THEOREM (§10, §11) | AGREED | — |
| A2 | A click is causally active (ℓ enters b' = ℓ − a) and is fixed by its backward taxicab cone | THEOREM (S5M-1) | accepts (07:24) | AGREED | — |
| A3 | Every non-trivial choice needs remainder turns δ != 0 in BOTH participants: C1/C2, or the half-turn δ = D/2 (labelled C0) at an exact even split (D >= 8). On the D = 6 reference board the turns are always C1/C2 | THEOREM (S5M-2, r12 Th 13, with the half-turn qualification) | proposes this wording (07:24) | AGREED, S5-M2's wording | S5-M's first draft said "C1/C2" without the half-turn |
| A4 | "Cancelling" a path = relocating its information (bijection) | THEOREM (S5M-3) | accepts | AGREED | — |
| A5 | The owner's "cooperation of clocks selecting one path" already exists as the escorted-junction coincidence (E20/E22), with a counting law (K3) | DERIVED + program NUMERIC | S5-M2's choice = the paired detector clock (§2); K3 is a rank-2 timing router (§11) | AGREED (two realisations) | S5-M2 confirmed (07:30) on the program record (K3, README) without re-running E20/E22 |
| A6 | The click map is many-to-one (inert parity bit; dark rotor), and a click past does not fix the click future | THEOREM + NUMERIC (S5M-9; checks B, F, F2) | accepts | AGREED | — |
| A7 | Kinds are J-ODD and time-EVEN: M keeps them, JR swaps them. Φ = N(C1) − N(C2) is NOT a time arrow | THEOREM + NUMERIC (S5M-14, corrected 07:13) | THEOREM (T7 correction, 07:12) | AGREED | both corrected after the manager's derivation and S5-P2R c3 (official engine) |
| A8 | The click arrow = growth of the record: the footprint (S5-P2R c3), with H(p) bits copied per choice from the click-invisible λ into the record (T13). A data-processing bound (T13b): H(record) <= H(the click-invisible data it reads). With ONE shared λ and the drive off, H(record of n choices) <= log2(D/2) for every n, so it SATURATES (a Beatty sequence). With FRESH hidden phases it grows by Σ_k H(p_k), linearly in n. It is TRANSIENT: bounded orbits are periodic (S5M-15) | NUMERIC + THEOREM (S5M-15) | THEOREM (T13, T13b) | AGREED (combined) | T13/T13b give the growth and its source; S5M-15 bounds it by recurrence. This answers G8's "is there a growing click entropy?" |
| A9 | Collapse = conditioning the counting measure on the records. Nothing is erased on the board; the eraser works by conditioning; it is consistent with K1 | DERIVED (§4) | THEOREM/DERIVED (T13, §10) | AGREED | — |
| A10 | Einstein invariants of a choice: taxicab causality; λ = a local clock phase (proper time); \|ψ\|² inputs are U(1)-invariant; only relative kinds are physical | DERIVED (§4.1) | DERIVED (§5) | AGREED | — |

## B. Born rule and single outcomes
| # | claim | S5-M | S5-M2 | verdict | diagnosis |
|---|---|---|---|---|---|
| B1 | Remainder law: over a uniform remainder E[ℓ] = K/D, P(click) = \|K\|/D for \|K\| <= D; exactly in time, Σℓ = (ΣK + r0 − rT)/D | THEOREM (S5M-4; check A) | THEOREM (T1) | AGREED | — |
| B2 | Rank-2 (linear) readouts of a uniform phase give sawtooth/tent laws (K3). Phase-invariant (U(1)) frequencies need rank 3. Single-party Born (cos²) is EXACT with rank-3 thresholds | THEOREM (S5M-5, scope corrected 07:24:55) | THEOREM (T2, T3) + NUMERIC (T3b travelling, amplitude 1; TWO CODES: S5-P's P_fibre.log reproduces it exactly) | AGREED | S5-M's draft 2 and interim called the sawtooth "a theorem-level obstacle" to Born: WITHDRAWN. It is an obstacle only for rank 2 and for two-party correlations (C3) |
| B3 | Two exits: exclusive and Born iff the two click sets are complementary (antitone remainders with same-sign inputs, or equal remainders with opposite-sign inputs) | THEOREM (S5M-6a; check G) | THEOREM (T4) | AGREED | — |
| B4 | Mismatch S != D: P(both) = max(0, S − D)/D, P(none) = max(0, D − S)/D; Born-conditional iff S <= D | consistent (S5M-4; S5-P PR-6) | THEOREM (T5) | AGREED | — |
| B5 | Repeated pulses stay exclusive iff S \| D. The first-passage race is exact iff S \| D, otherwise O(S/D) with ties. Matched quantization is a TUNING; with the drive off, outcomes form Beatty sequences | NUMERIC (check I) | THEOREM (T5b) + DERIVED | AGREED | the same arc arithmetic on Z_D. S5-M2: symmetric splits are not exact either unless S \| D (I± = 50, D = 144: 25/72 vs 1/2, 22 ties), so "iff" stands |
| B6 | The uniform λ is native: an invariant counting measure plus CRT sampling. The board makes the shared λ from the vacuum by a common DC drive. Creating a pairing from uncorrelated remainders needs a low-entropy resource (the vacuum's zeros) | THEOREM (S5M-7, -8) | THEOREM + NUMERIC (T6) | AGREED | — |
| B7 | n >= 3 exits with PARALLEL (same-update) own-intensity thresholds: impossible for ANY joint remainder law (a pointwise proof) | THEOREM (S5M-6b; check G exhaustive D = 3, 5, 6, 30) | THEOREM (T8); S5-P2R E7 exhaustive D <= 4 | AGREED, with the "parallel / same-update" qualifier (manager 07:27) | two independent proofs |
| B8 | n >= 3 exits EXACT by a sequential visit to one shared remainder: a carried-remainder tree (arithmetic decoding), light-delayed partial sums, or a sequential fixed-divisor gear | THEOREM + NUMERIC (F6c; check J c: 400 trees, <= 16 exits, exact; a fresh remainder fails) | NUMERIC (D19, m2_link: 0/360, 0/1320) | AGREED | three realisations (plus S5-P2R b2: 45/45, 91/91, 561/561). Costs: a carried integer or a light-crossing delay. D19's timing prediction (middle exits delayed) is decisive against QM |
| B9 | The choice = ONE click plus ONE silent remainder turn. Convention-free: \|Δr_click\| = I_other and \|Δr_silent\| = I_own (mod D). The kind relation (neutral C1/C2 pair, or same kind) is the sign convention of the second detector | THEOREM (S5M-16 with caveat; check H) | THEOREM (T7) | AGREED, merged wording | S5-M's "neutral pair" holds in the same-sign convention. S5-M2's Δr signs are that convention; the magnitudes are convention-free |
| B10 | One unit quantum is routed or copied, never split; there is no exact integer 50/50 amplitude splitter for a unit | DERIVED (program theorems) | OPEN/caveat (T3) | AGREED | OPEN lead (S5-M2): a Grover-type 4-port junction (D = 12, weight-3 ports, exact on even-sum data, scattering −1/2, +1/2, +1/2, +1/2) would split an AMPLITUDE-2 pulse into ±1 parts exactly. Not built; a unit still cannot be split |
| B11 | HOM fails: coincidence 1 − \|cos θ\| (mean 1 − 2/π) with a shared token; sin²θ/2 (mean 1/4) with one token PER QUANTUM; mean 1/6 with independent DETECTOR remainders. QM gives 0 | S5-M checked the shared-token formula analytically | DERIVED (D17) + NUMERIC (m2_hom.py, Z6: shared token per θ 0, 1/2, 1/2, 0, 1/2, 1/2, mean 1/3 = the Z6 mean of 1 − \|cos θ\|) | AGREED | needs two-particle amplitudes; every model stays above 0 |
| B12 | Partition noise is sub-binomial with one token per pulse (Var N+ <= 1/4); binomial needs one token per quantum | accepts (DERIVED) | DERIVED (D18) | AGREED (DERIVED) | — |
| B13 | Spatial version: the shared λ must be frozen in flight, or the arrival times equal | accepts | DERIVED (D16) | AGREED | — |

## C. Bell and the routes
| # | claim | S5-M | S5-M2 | verdict | diagnosis |
|---|---|---|---|---|---|
| C1 | K1: \|S\| <= 2 for taxicab-separated settings with measurement independence; every choice mechanism here (rank 3, tokens, links, trees) is a local hidden variable | THEOREM | THEOREM (T9) | AGREED | — |
| C2 | Cusp: locality + measurement independence + perfect correlation force a cusp at δ = 0 (E(1) <= 1 − 4/N on Z_N); the cos CORRELATION is impossible for N >= 5 | THEOREM + NUMERIC (S5M-10; check D) | THEOREM (T15) | AGREED | — |
| C3 | Measurement independence on the board iff the setting-clock periods are COPRIME to the source (CRT); a shared factor gives S up to 4 | THEOREM + NUMERIC (S5M-11; check E) | THEOREM + NUMERIC (T14) | AGREED | — |
| C4 | S <= 2 + 2Σ_ab TV. Measurement dependence overshoots (2, 3, 4), can make marginals signal, and is TUNED by the mechanism. For a common past nothing selects 2√2. REFINED by F7: when the second click reads a light front from the first with an exact Born (rank-3) receiver (exact weights; integer-rounded weights give 2√2 + O(1/D)), S <= 2√2 is a THEOREM (F2), but only for TIMELIKE clicks | THEOREM + NUMERIC (S5M-12) | DERIVED (T10); S5-P2R b3, b4, M2-3; refinement from S5-M2's column row 16 | AGREED | the quantum set is selected by Born READERS of a front, not by any spacelike principle |
| C5 | Handshake (route iii): two-time conditioning = an initial sub-ensemble. The advanced partner exists formally (the reversed history) and adds no freedom; a setting-dependent future boundary = measurement dependence | THEOREM (S5M-13) | DERIVED (D20) | AGREED | S5-P2R (c): no C1→C2 pairing beyond chance |
| C6 | Route (ii), non-local links: CLOSED by the owner. Face-local links (node + link systems) leave Theorem 1's cone, and K1, unchanged | THEOREM (F6d) | THEOREM (§6, §14d) | AGREED | — |
| C7 | The cone gap: the board's taxicab cone is wider than the round light cone (sqrt3 along the axes, none on the diagonals); Bell separation must use the taxicab cone | THEOREM (cone) + DERIVED | accepts | AGREED | — |
| C8 | Route (v), click-time hiding (E02), gives exact singlet correlations by a designed exchange, but needs stopped (approval) clocks: CLOSED by proper time = running clocks | DERIVED (§3.4b) | accepts | AGREED | see the F7 rows |

## D. Decoherence and complementarity
| # | claim | S5-M | S5-M2 | verdict | diagnosis |
|---|---|---|---|---|---|
| D1 | Remainder-free (linear) sector: no decoherence; ensemble = single run; the record does not depend on the microstate | DERIVED at large A; THEOREM for remainder-free sets | THEOREM (T11) | AGREED | S5-P2R a |
| D2 | Genuine (erasable) decoherence needs hidden-dependent back-action. V = V0·\|E e^{iχ}\|; in the kick toy V = 4A²/(4A² + N) exactly, so N_c ∝ A²; the eraser needs ALL records | DERIVED + NUMERIC (S5-P rank 4: 0.652 vs 0.654, eraser 0.756) | DERIVED + NUMERIC (D12, D12b) + S5-P2R M2-2 | AGREED | rank-3 parametric back-action is unstable at zero headroom; stable at rank 4 (D4). Information (m2_info_dec): I(s; exit) 0.5 → 0 bits under the 90° back-action, while I(s; exit, record) stays 0.8113 bits: the information moves into the correlation |
| D3 | The "window" depends on the coupling. Reference board or reciprocal coupling: none (all-or-nothing, a record means >= 1 unit of disturbance). One-way read: a record with ZERO disturbance. Exit records after interference at A = 1 with rank 3: YES | THEOREM + NUMERIC (corrected 07:24:55; S5-P a2 h = 0, 1) | proposes this row (07:24); T3, T3b | AGREED | the first drafts answered different premises (which-path vs exit records; reciprocal vs one-way) |
| D3-note | D3 diagnosis (S5-M2, 07:37), m2_fibre_recip: an exact-fibre router with RECIPROCAL back-action of the detector pair on the fibres (the Hamiltonian partner of the rank-3 read, weight w). w = 0 control: identical to m2_fibre (one click per pulse, zero disturbance, exact rewind). w = 2 (rounding back-action): after the choice click the fibres are disturbed by >= 1 unit (max\|b\| 1 → 2–3), and exclusivity can break (3 clicks in one passage at s = 3, λ = 40). w = 6 (exact unit kicks): 30–40 clicks per passage, max\|b\| up to 6; the record keeps kicking the wave. No exponential blow-up within 100 updates. So the window is OPEN with a one-way read and CLOSED with reciprocal coupling, as D3 states | S5-M predicted this (07:36 message) | NUMERIC (spot checks: 3 trajectories per w, m2_fibre_recip_diag.py; the full-ensemble run was cut by its 600 s timeout) | AGREED | recorded by S5-M at 07:37:11 |
| D4 | Complementarity fails without back-action: Englert's V² + D² <= 1 is broken (2 and 1.93). The owner's "the click affects the board" is NECESSARY for complementarity. QM-deviating prediction: P(+ \| arm-1 click) = 1, 1, 1, 0 against QM's 1/2 | NUMERIC (S5-P) | DERIVED (D12b) | AGREED | — |

## E. F6: the link (owner 07:17)
| # | claim | S5-M | S5-M2 | verdict | diagnosis |
|---|---|---|---|---|---|
| E1 | The board-made choice = ONE remainder shared by two ends (the lock is kept by the conservation S ≡ 0 mod D); the sign of the single nonzero quotient picks the end | THEOREM + NUMERIC (check J a) | THEOREM (§14a) | AGREED | — |
| E2 | One divmod gives ADJACENT quotients, so a single gear cannot output ±1 by itself (0 sign rules, exhaustive). The choice is either one link gear's overflow (0/1) with the signed records written to the end nodes, or two half-gears sharing one remainder (the T4 pair). Both are exact, even-K, exactly rewound, and use 6 face neighbours | NUMERIC (check J b) | THEOREM + NUMERIC (§14b, m2_link) | AGREED, merged | the two "entity" counts differ only in where the end records live |
| E3 | n ends EXACT by a sequential visit to one remainder (see B8) | THEOREM + NUMERIC | NUMERIC | AGREED | — |
| E4 | Bell unchanged by face-local links | THEOREM | THEOREM | AGREED | — |
| E5 | ONE line: "A link can be where the choice happens: one shared remainder at its two ends, and the sign of a single overflow, sends the one record to one end. That gives exact Born weights for two ends, and for n ends through sequential visits (a carried remainder or light-delayed partial sums). It is local, integer, reversible and uses six neighbours. But it is a local hidden variable, so Bell stays <= 2." | proposed | §14e (same content) | AGREED, merged | — |

## F. F7: "the choice is made only AT the click; the far side waits for the light" (owner 07:23)
| # | claim | S5-M | S5-M2 | verdict | diagnosis |
|---|---|---|---|---|---|
| F1 | (a) The cost: the far side's click waits for the light front. By the triangle inequality the wait is W = (d_A + d_AB − d_B)/c >= 0, and W = 0 only in the timelike (collinear) geometry. So in every spacelike geometry the wait SHOWS in the far side's running clock, and the clicks become timelike (not a Bell test). "Instant in clicks" needs a STOPPED (approval) clock, which breaks proper time | DERIVED (§5d) | AGREE, DERIVED (§15) | AGREED | — |
| F2 | (b) Conjecture PROVED as a mechanism: a one-way front (phase a, or a + π) plus a rank-3 Born receiver gives P(B \| A) = (1 ± A cos(a − b))/2, so E = cos(a − b), exact no-signalling, and S → 2√2. S5-M2's THEOREM: with EXACT Born weights and ANY front encoding f(a, A), E = Re(c_a e^{−iβ_b}) with \|c_a\| <= 1, so S <= \|u + v\| + \|u − v\| <= 2√2. TSIRELSON IS A PROPERTY OF THE BORN RECEIVER. Integer-rounded weights give 2√2 + O(1/D) (check K: 2.8333 at D = 720), never near 4. Exact weights exist on the exact-clock grids (periods 1, 2, 3, 4, 6). It is the principle E02 lacks (a bit-reading rank-2 gate gives 4); a constraint on READERS, not a dynamical selection | THEOREM + NUMERIC (check K) | AGREE, merged (§15, m2_front.py: Z6 exact, E = cos(60°Δ), max S = 5/2 EXACTLY = QM's maximum on Z6; marginals unbiased; no-signalling) | AGREED | TWO CODES: S5-M's check K on Z6 (D = 12, 72, 7200) also gives max S = 5/2 EXACTLY, E = cos exactly and signalling 0 (07:32:02). Rounded weights (Z8) vs exact-grid weights (Z6) explain the 2.8333 overshoot |
| F3 | (c) Spacelike registrations: the mechanism predicts \|S\| <= 2 (no wait possible), or a hidden wait visible in proper time. The 2015 tests (both clicks inside the spacelike window) FALSIFY it if the board cone = the physical cone. The only board escape is the cone gap (O4), which breaks the light cone | DERIVED | AGREE + NUMERIC (Bob reads the source's own copy, spacelike: E = (1/2)cos(60°Δ), max S = 5/4) | AGREED | — |
| F4 | (d) "Nothing is chosen before the click": true in click space (λ is click-invisible, T13), false in event space (S5M-1). The front puts the near click in the far click's backward cone | DERIVED | AGREE | AGREED | — |
| F5 | (e) ONE line: "Your mechanism is local, and with a Born detector reading the light front of the first click it gives exactly the quantum cos law and 2√2, never the impossible 4. But it does so only because the far side waits for that light. The wait shows in its own running clock, so the clicks are not spacelike. In the 2015-type tests, where both clicks happen before light can connect them, the board predicts \|S\| <= 2." | proposed | AGREE (adds "never the impossible 4") | AGREED | — |

## G. K1–K5 and the owner decisions
- K1–K5 stand.
  - K2 holds for JR. The repo's time_reverse is M-type and keeps kinds (A7).
  - K3 holds for its device class (rank-2 timing routers); rank-3 thresholds are a different class (B2).
  - K4, refined: in event space a click reveals λ's coarse bit. "Single outcomes need amplitude ~1" holds for rank-2
    detectors. With rank-3 detectors one click = one detector quantum D at any amplitude (S5-M2 §11).
  - K5: nothing is erased.
- Owner decisions, smallest first; all keep 6 face neighbours, integers and reversibility:
  - O1 Rank-3 on-site intensity detectors and the paired detector clock (new gear types). They give |ψ|² click rates and
    exact two-exit Born choices.
  - O2 Sequential shared-remainder routing (carried remainder, or light-delayed partial sums), for exact n-exit Born.
  - O3 Bell: either accept |S| <= 2 for spacelike (taxicab-separated) registrations as the board's falsifiable prediction,
    or adopt a PRESCRIBED common-past (resonant-clock) ensemble, which overshoots and is tuned.
  - O4 Back-action for complementarity: stable only at RANK 4 on the zero-headroom reference light (D4).
  - Not recommended: the cone gap, and stopped/approval clocks (route v / F7 "instant").

## Signatures
- S5-M: merged; co-signs every row A1–F5 at 07:31:15 (`date -u`).
- S5-M2: co-signed A1–E5 at 07:30 (by message), and co-signed THE WHOLE FILE, rows A1–F5, at 07:32 (`date -u`), by
  message ("I CO-SIGN THE WHOLE FILE AGREE_M.md, rows A1–F5, at 07:32"). Recorded by S5-M, the single editor, at 07:32:51.
- After that co-signature, S5-M made two edits:
  - the B11 precision, at S5-M2's own request;
  - C4 refined at 07:32:38 from S5-M2's OWN column row 16 (M2_AGREE_COLUMN.md: Born readers of a front select 2√2 for
    timelike clicks). S5-M2: "OK on C4 as worded" (07:33), with the exact/rounded qualifier added at 07:33:36.
  - A8 extended at 07:33:36 with S5-M2's T13b (data-processing bound), proposed by S5-M2 (07:33).
- The D3 diagnosis note (m2_fibre_recip) was received at 07:37 and recorded as row D3-note at 07:37:11. S5-M2: "I co-sign the
  final file as recorded" (07:37).
- FINAL. S5-M makes no further edits after 07:37:11.
- ADDENDUM by S5-M2 at 07:39 (`date -u`), after S5-M's final hand-back (S5-M allowed one appended line). This is a twin of row
  D3-note and changes no verdict. S5-P's ensemble (P_fibre_recip.log, PR-20) reproduces S5-M2's three trajectories exactly.
  Over all 48 even tokens, reciprocal coupling gives exactly-one 1/12–1/2 at w = 2 and ≤ 7/48 at w = 6, with up to 7/48
  tokens blowing up (int64). So the window closes AND part of the ensemble is unstable (zero headroom).
