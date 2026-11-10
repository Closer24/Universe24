# AGREE_CC — Study 13 "THE CHOICE-DRIVEN COSMIC CLOCK": twin agreement CC-B (theory + own toy) × CC-A (numerical toy)
- Built by CC-B from 13:20 UTC (`date -u`), after both interims. Building rule: CC-B builds; **CC-A marks the last
  column (ACCEPT / EDIT / DISAGREE) and signs**. Only the A-mark column and the signature block should be edited; EDIT
  notes go below the tables. Relayed to CC-A through the manager (13:20), because direct messages do not reach CC-A.
- Sources:
  - B = s13/CC-B_FINDINGS.md (§0–§5) + s13/CC-B_NOTES.md (pre-registrations 13:08 N13-B, 13:14 N13-B2, 13:22 N13-B3).
    Own code: s13/CC-B_work/n13b.py, n13b_posthoc.py, n13b2.py, n13b3.py (+ posthoc), local_flux_check.py,
    momentum_check.py, rate_check.py.
  - A = s13/CC-A_NOTES.md (§0 design and pre-registration 13:12; §1 run set 13:17) and CC-A_work/R0–R3 logs/json
    (runs 13:16–13:19), read by CC-B at 13:17–13:19.
- Independence:
  - CC-B read no CC-A file before its interim (sent 13:12).
  - CC-A states that it read no CC-B file before its interim.
  - The two toys share no code. B: L = 3, Q = 101, matched pairs with LINEAR loads, a seeded light pulse of length T_s.
    A: L = 5, Q = 2^21 + 1, the package's opposite-form |ψ|² routers continuously exposed to first-order matter, and a
    free hand with designed exact zeros.
- Labels: THEOREM / NUMERIC (file) / DERIVED / POST HOC / OPEN / NEW LAW (owner decision).
- Verdicts: AGREED / AGREED-WITH-QUALIFIER (AwQ) / AGREED-OPEN / DISAGREE.

## A. Existence, locality, reversibility
| # | claim | B | A | proposed verdict | evidence | A mark |
|---|---|---|---|---|---|---|
| A1 | A per-node cosmic hand (on-site spring + face coupling, read by first-order sectors as one common factor) can be SOURCED by local choice activity. The source is exact, reversible and local, at rank ≤ 3 (the fold factor ≤ 4), with one odd Q, and every run rewinds bit for bit | THEOREM T13.1/T13.6 + NUMERIC: source 3Qm·(b_d+ − b_d−), rank 2. 47/47 runs rewind exactly | NUMERIC: source gJ·ρ_J (construction A, rank 3) and gR·(a²+b²)_routers (click ledger, rank 3); also gS screening (rank 4). Ledgers I1/I2/I3 exact at every update and rewind exact in R0–R3 | AGREED (two codes, three source types) | n13b*.json; R0–R3 logs | ACCEPT |
| A2 | **What a b-polynomial can read of a choice.** (a) For ANY gear, Rule3 gives b(t+1) + b(t−1) = ℓ(t). So a detector's own b (no self-term) is a zero-lag filtered record of its clicks, x(ω) = n(ω)/(2cos ω). Its SLOW part is half the click RATE, readable by a rank-2 input. Its period-4 part is resonant: the ledger-like part that A's a² + b² measures. It stayed bounded under a constant load in rate_check.py. (b) Not readable: the exact click at its own step (needs r or three times), the rate of the generic remainder flux of non-detector gears (only its integral, a count, via conserved densities), and the "newness" of a choice. (c) For an EXACTLY matched shared-remainder pair (K+ − K− = nD), the number of events equals the load, deterministically: Δ(t+1) + Δ(t−1) = n(t). (d) The OUTCOME is readable only through records (b_d+ + b_d−), with zero mean under Born | THEOREM T13.1 (a)–(d); (a) added 13:26. NUMERIC rate_check.py: for an UNMATCHED pair (K+ − K− = 0.604·D) the slow part 2·mean_300(Δ) = 0.57–0.63 against click rate 0.60–0.61 while lit, and 0.000 dark | (c) of §0: "ℓ is two-time, so no rank ≤ 4 input can read the RATE of new choices, only a ledger". True for A's routers: odd-Q polarization routers lose the equal-remainder lock after the first update (TC.15), so their clicks are independent and r-decided | **B proposes a CORRECTION of A's (c), with joint text (a)–(d).** The click RATE is readable in low-pass form even for A's unmatched routers (a linear read of b_P − b_N has slow part = click rate/2). What A's (c) correctly excludes is the exact click at its step, the generic remainder-flux rate, and "newness". At odd Q exact matching needs a LINEAR load (DC load gears with b_i+ + b_i− = Q, B's toy); the \|ψ\|² polarization identity cannot be matched at odd Q (TC.13 parity) | n13b: 0 failures of ℓ+ − ℓ− = g, r+ = r− (28 runs × 112 × 27) | ACCEPT + EDIT (A accepts the CORRECTION; note 1) |
| A3 | **"The choices drive the clock" holds for choice EVENTS, never for OUTCOMES.** The coherent drive is the event rate (load) or its count. Outcomes add only a zero-mean, Born-weighted push | DERIVED from A2 | consistent: A's construction-A drive is the matter remainder flux, "a random walk of relative size O(1/A)" (R1 prediction) | AGREED (proposed) | — | ACCEPT |
| A4 | **Reciprocity.** The partner of a hand ← pair source Φ = f(b_C)(b_d+ − b_d−) (field sign of d− = −1) is a COMMON-MODE push on the pair, so "one choice per event" always survives. Every remainder and outcome, hence the Born law, is EXACTLY unchanged iff 2f ≡ 0 (mod D) for all reachable b_C. PUSH (f = 3Qm·b_C) satisfies this, and the back-action is then an exact common click offset m·b_C. HOLD (f = k·b_C², k = spring detuning) cannot satisfy it with a slow spring, so it must be designated one-way; otherwise it shifts the shared remainder by 2k·b_C² mod D per lit update, scrambling Born | THEOREM T13.2 + NUMERIC: reciprocal = one-way for outcomes, hands, matter and remainders; quotients + m·b_C (7/7) | A's sources are designated one-way (gJ, gR, gS read two-time or ledger quantities); not tested | AGREED-OPEN (B THEOREM + single code) | n13b_results.json (P3) | ACCEPT (AGREED-OPEN; no A test) |

## B. Saturation and turnover
| # | claim | B | A | proposed verdict | evidence | A mark |
|---|---|---|---|---|---|---|
| B1 | **Three response laws of a linear hand to the choice EVENT history n(t)** (Green's function G(k) = sin kω / sin ω). PUSH (rate source), from rest at 0: held at λ ≥ 0 during the era, zero at t_z = (T_s − 1)/2 + π/ω, so it tracks the era CENTROID (slope ½); in general the ω-weighted centroid of n. HOLD (screened spring): held exactly, zero at T_s − ½ + π/(2ω), so it tracks the END (slope 1). COUNT (cumulative ledger or conserved number): saturation freezes a displaced rest point, the minimum is (f/ω²)(T_s − (2/ω)\|sin(ωT_s/2)\|) ≥ 0, and there is NO turnover | DERIVED (T13.4) + NUMERIC, one code. PUSH 7/7 (POST HOC metric; the registered metric had a global-argmax bug, slope 0.125 as registered), slope 0.500. HOLD 14/14 (registered), t_z = T_s + 15, slope 1.000. COUNT 7/7 (registered), min λ = 0 | R2 (ledger force) and R3 (ledger screening): predicted no tracking. NUMERIC (A = 2^9): R2 zeros shifted −0.1 … +5.7 updates, alternating, with no relation to the saturation of new choice sites. R3 half-periods grow 203 → 226: "more choices → slower clock", no trigger. A's (c) criterion: pending A's analysis | AGREED on COUNT/ledger: no trigger (B registered toy + A's R2/R3, two codes). PUSH and HOLD laws: AGREED-OPEN (B single code; A has no rate or hold coupling) | n13b2_results.json; CC-A R2_A9/R3_A9 logs | ACCEPT + EDIT (A's HOLD numbers; note 2) |
| B2 | **GU-2A's Q1 (hold form: zero π/(2Ω) after the load drops, slope 1 ± 0.2)** is CONFIRMED when the load drop is given. Its timing is set by the END of the choices; the push form instead tracks their centroid | NUMERIC N13-B2 H1/H2 (registered): slope 1.000, offset T_s + 15 vs theory T_s + 15.28, with the screen reading the load OR the choice record Δ | A predicted Q1 "not testable with package-faithful routers" (no load drop under continuous one-way exposure). A then registered (13:22:50) a HOLD of the OPPOSITE logic: the MADE choices provide the spring (rank 4, router record e = a² + b²). Read by B from A's logs at 13:26, A's analysis pending: the sharp variant (all routers choose together) gives first zeros 128.5, 188.5, 278.5 for m = 20, 60, 120 (t_s ≈ 30, 90, 180), i.e. t_s + 98.5, slope 1 by construction. The broad variant (gradual release) gives zeros that drift with A | AwQ: confirmed in B's toy, where the end of the choices is set by the light pulse (seed). Both HOLD logics (pending choices screen the spring, B; made choices supply it, A) give slope 1 when the release is sharp. Whether a board makes its own choices stop is B3 | as B1 | ACCEPT + EDIT (note 3) |
| B3 | **Saturation itself.** Under persistent light, package-faithful one-way routers never stop choosing: router clicks per aeon stay steady. Only the NEW choice sites saturate. "Newness" is a history functional, not a polynomial of the snapshot, so no rank ≤ 4 hand can feel it. The turnover laws (B1) apply to whatever event history n(t) the light delivers. In B's toy the stop was imposed by the seeded pulse length, so B tests the conditional "IF the events stop at T_s, THEN …" | DERIVED (locality) | NUMERIC R0 (A = 2^10, 2^11, 2^12): router clicks per aeon 60–79, 254–297, 1056–1095 (steady); new choice sites per aeon 64, 25, 22, 10, 3, 1, 0, 0; 121, 4, 0, …; 125, 0, …. Agrees with GU-2B B1 (no decline) | AGREED (A numeric + B derivation; also GU-2B) | R0_A10/11/12 logs | ACCEPT |
| B4 | **Intrinsic stop (OPEN).** A "consuming" router, whose load gear reads the detectors' Δ while the detectors read the load, is b-only and hence an exact bijection: not cyclic, contrary to A's "needs its own a" for a self-gated router. In the linear world the drained load oscillates, and the event number n changes sign (anti-choices) instead of stopping. So no clean saturation is produced | DERIVED, not run | §0(c): a self-gated one-shot router needs its own a (cyclic) | AGREED-OPEN (the two statements concern different constructions) | — | ACCEPT + EDIT (note 4) |

## C. The fold after the turnover
| # | claim | B | A | proposed verdict | evidence | A mark |
|---|---|---|---|---|---|---|
| C1 | **THEOREM X (odd-source condition).** If the hand is odd about an integer zero t_z on \|j\| ≤ J, its source is odd there too: s(t_z + j) = −s(t_z − j). A choice push (≥ 0) is fold-even. So the fold mirrors only the choice-free window [T_s, 2t_z − T_s], and the board returns to the mirror of its SATURATED state, not to the bang. A parametric source (activity × the odd hand) is the only class compatible with a full fold | THEOREM + NUMERIC (POST HOC, uniform hands): window mirror defect 2.6e−6 at an exact zero, 0.002–0.07 otherwise. Mirror of the seed 0.63–2.09 for T_s ≥ 12. Profile: 0 inside the window, then 0.10, 0.52, 1.34 … | Every choice-sourced run turns the exact zeros into crossings. R1 (construction A, a zero-mean O(1/A) drive): zeros within 2e−3 of R0, and the bang refocus is NOT degraded (relative seed distance at bang 8: 0.017, 0.014, 0.018 vs R0 0.022). R2/R3 (ledger force or screening, a growing fold-even drive): the refocus is DESTROYED from bang 1–2 on (relative distance 1.2–1.9; T_spread 1e5–6.5e6) | AGREED (B THEOREM). A's numbers fit THEOREM X quantitatively: the fold degrades with the fold-EVEN part of the source, which is small for a zero-mean walk and total for a growing ledger | n13b_posthoc.json; R1 logs | ACCEPT + EDIT (note 5) |
| C2 | **Exact integer zeros.** THEOREM F needs λ(t_z) = 0 EXACTLY. A free hand can be given exact zeros by design. A choice-driven hand hits 0 exactly only by coincidence | NUMERIC: 1 of 7 push arms (λ(t_z) = 0), the others \|λ(t_z)\| ≤ 2 | NUMERIC: free hand with exact zeros 100, 300, …, 1500 and exact period 400 (find_fold.py, R0 8/8 exact). With any source (R1 g = 1 … R3) the zeros become crossings | AGREED (two codes) | R0 logs; n13b_posthoc.json | ACCEPT + EDIT (note 6) |
| C3 | **Non-uniform choice activity desynchronizes the hand copies**, so there is no EXACT common zero and the fold is approximate. A: T_spread grows 32 → 394 (R1 g = 1) and to 4e4–2e5 (R2), 7e4–3e6 (R3). B (N13-B3, 9 nodes T_s = 12 and 18 nodes T_s = 30): the board-mean hand crosses at the predicted 44 for every j. The face coupling j ≥ 8 puts every copy's integer zero on the same update, but λ_x(t_z) ∈ [1, 7], so there is no exact common zero (fold defect ≈ 3–4 %) | DERIVED (GU-2B: an exact common zero is codimension #nodes) + NUMERIC N13-B3 (U3 as registered FAILED: the integer spread did vanish) | NUMERIC R1/R2/R3 | AGREED (two codes) | R1–R3 logs; n13b3_results.json | ACCEPT + EDIT (note 7) |
| C4 | THEOREM N (GU-2B) applies on top: even with a full fold, the next bang is an ECHO of the last, never a fresh bang from a generic saturated board | accepted | accepted (§0 sources) | AGREED | s12/GU-2B | ACCEPT |

## D. Conservation "as Einstein found"
| # | claim | B | A | proposed verdict | evidence | A mark |
|---|---|---|---|---|---|---|
| D1 | **Click ledger (exact, every gear).** D·Σℓ = ΣK + r(t0) − r(t1): the clicks are the exactly quantized input flux and the remainder is the exact local ledger. For a matched pair one choice = one unit (ℓ+ − ℓ− = n), and r+ − r− is invariant | THEOREM | I2: e′ − e = ℓ² − 2ℓa for the routers (no linear self-term), exact at every update | AGREED (two codes, complementary ledgers) | n13b P1; A I2 0 bad | ACCEPT |
| D2 | **Two-time energy with an exact local flux.** e_x(t) − e_x(t−1) = Σ_y J_{y→x} + s_x(b_x⁺ − b_x⁻)(K_one-way + r − r′), with J_{y→x} = H_xy[b_y(b_x⁺ − b_x⁻) − b_x(b_y⁺ − b_y⁻)]. This is the board's ∂_t T^{00} + ∇·T^{0i} = source, exact. Globally it is GU-2A's T1, re-derived independently. A one-way hand source breaks the budget, and the 3Qm reciprocal partner restores it exactly | THEOREM + NUMERIC: local 4617/4617; global 0/111 (reciprocal) vs 105/111 failures (one-way) | — | AGREED-OPEN (B THEOREM + single code) | local_flux_check.py; n13b P6 | ACCEPT (note 8) |
| D3 | **Noether numbers survive any common factor; energy does not.** ω(x, y) = x⁺ᵀSy − xᵀSy⁺ is conserved for any λ(t), and N_J passes every fold and bang. A's link-symmetric factor (b_T(x) + b_T(y)) makes the N_J ledger exact for ANY T field, not only a uniform one | DERIVED (Wronskian algebra; = AGREE_B A5, ST-1 G2) | I1 exact at every update in R0–R3 (non-uniform T included) | AGREED (two derivations; A numeric) | A I1 0 bad | ACCEPT |
| D4 | **Einstein-conserved sourcing and a saturation trigger conflict.** A conserved source density (ρ_J, I_x) drives the k = 0 hand only by its integrated non-conservation, the choice flux: a COUNT. By B1 a count cannot trigger a turnover. A trigger needs a rate or hold coupling to matched-pair EVENTS, which is not a conserved source. The owner must choose | DERIVED (T13.5) + B1 numeric | I3: the k = 0 law is moved only by spring, own rounding and choices. R1 (construction A): zeros stay within 2e−3 of R0 (no turnover change) while the copies desynchronize | AGREED (proposed; A numeric supports) | R1 logs; n13b2 | ACCEPT |
| D5 | **The irreducible non-conservative step is the choice itself** (observer terms light → pair; a reciprocal observer breaks exclusivity, TC.11). With the hand ↔ pair coupling made reciprocal at 3Qm, the only booked non-conservation is the choice flux, exactly recorded in the clicks | DERIVED | routers designated one-way (package form) | AGREED (proposed) | NOTES_choice TC.11 | ACCEPT |

## E. The manager's ST-1 question and the owner's sentence
| # | claim | B | A | proposed verdict | evidence | A mark |
|---|---|---|---|---|---|---|
| E1 | **ST-1's rest-mass lapse is an exact, local, rank-3 choice COUNTER, not a cosmic clock.** (i) Its k = 0 mode has no spring, so it never turns over. (ii) Its drive (remainder kicks) has zero mean: an undirected walk, which cannot hold a hand. (iii) γ = 1 gives no common zero, so no exact fold (AGREE_B A8/A9). (iv) Matched Born choices do not change N_J. To turn over it needs a spring on a SEPARATE γ = 0 hand (a spring on h00 would screen gravity) and a rate or hold coupling | DERIVED | R1 = construction A (the same structure): zeros unchanged to ≤ 2e−3, copies desynchronize, and no turnover is induced | AGREED (B derivation + A numeric) | R1 logs | ACCEPT |
| E2 | **"When new choices stop, the next bang starts", honest form.** True as a TIMING law for a hand coupled to the choice EVENTS: HOLD gives turnover a quarter period after the last event, PUSH gives turnover at the event centroid plus a half period. FALSE for count or conserved sources. The fold that follows retraces only the choice-free epoch (push), or the whole history if the activity is itself mirrored (hold with λ-reading light: OPEN). The next bang is an echo (THEOREM N). Under persistent light the events themselves never stop; only novelty saturates | DERIVED + NUMERIC (B1, C1) | R0–R3 | AGREED (proposed joint text) | all above | ACCEPT + EDIT (note 9) |
| E3 | **What grows from bang to bang, and for how long.** With a free or hold hand: the un-retraced outcomes (the click record and the debris). A R0: relative seed distance at bangs grows 0.0025 → 0.022 (A = 2^10), 2.4e−4 → 6.4e−3 (2^11), 9.6e−5 → 1.4e−3 (2^12), falling ×3.4 and ×4.4 per doubling of A, while per-aeon click entropy and zlib are flat to a few %. With a push hand there is no exact recurrence at all. On a bounded orbit any growth lasts at most until the grand symmetric moment p/2 (THEOREM P), and invariant measures repeat once per grand cycle (THEOREM C) | DERIVED | NUMERIC R0 (as listed) | AGREED (A numeric, B derivation) | R0 logs | ACCEPT (note 10) |

## F. Recommendation to the owner (joint proposal; every item a NEW LAW, separate candidate variant)
- **If the owner wants the choices to TIME the cosmic clock:** couple the γ = 0 hand to the choice EVENTS. The rate is
  readable in low-pass form for any pair, and it is deterministic, equal to the load, for matched pairs (A2).
  - HOLD (one-way; the turnover follows the end of the choices) or PUSH (can be reciprocal and Born-exact at weight 3Qm;
    the turnover follows the centroid).
  - Price: no exactly conserved source (D4). The fold is exact only over the choice-free window (C1), or over the whole
    history only with mirrored activity (OPEN). The next bang is an echo (C4).
- **If the owner wants Einstein-exact conservation of the source:** use a conserved number (ρ_J, I_x).
  - Then the choices only COUNT into the clock: an undirected walk of O(1/A). The clock runs on its own spring, and
    saturation triggers nothing (B1, D4, E1).
- **Both at once is not available** [DERIVED, T13.5; scope: linear or parametric hands, inputs of rank ≤ 4 on
  (1, b, a)].
  - A conserved density is at most two-time, so its RATE (three-time, or r) is unreadable.
  - Every coupling to it therefore freezes at saturation instead of releasing, as A's R3 shows: the screening ledger
    only slows the clock.
  - This is the choice the owner has to make.

## Signatures
- CC-B: built every row from both sources. I propose the verdicts above and accept A's R0–R3 evidence for B1, B3, C2,
  C3, D3, D4, E1 and E3.
  **CC-B SIGNS all rows: Tue Nov 10 13:21:25 UTC 2026 (`date -u`).**
  - CC-B post-signature edit (Tue Nov 10 13:23:39 UTC 2026): row C3 now also carries B's N13-B3 numbers (non-uniform activity,
    registered 13:22, U3 FAILED as stated). No verdict changed.
  - CC-B post-signature edit (Tue Nov 10 13:26:18 UTC 2026): row A2 generalized (T13.1(a): any detector's b is a low-pass click-rate
    record, with the rate_check.py numbers). The A2 proposed verdict changed from AwQ to "B proposes a CORRECTION of A's
    (c)". CC-A may DISAGREE there.
  - CC-B post-signature edit (Tue Nov 10 13:27:12 UTC 2026): sources list completed; A1 rewind count 47/47; A2 period-4 wording
    (bounded in rate_check); A4 wording; F first bullet aligned with A2. No verdict changed.
- CC-A: marked every row in the A-mark column: 20 ACCEPT, 10 of them with EDIT notes (below). No DISAGREE.
  CC-A read CC-B's files for the first time at 13:26 UTC, after its interim (13:21) and after its FINDINGS v1 stamp.
  **CC-A EDIT notes** (NUMERIC sources are s13/CC-A_work/*.json, *.log, and s13/CC-A_FINDINGS.md):
  1. A2. A ACCEPTS the correction and WITHDRAWS its §0(10)/§2.5 wording "no rank ≤ 4 input can read the RATE of new
     choices". By Rule3, b(t+1) + b(t−1) = ℓ(t), so a detector's own b is a zero-lag filtered record of its clicks.
     Its slow part, half the click rate, is readable by a linear rank-2 read. What stays unreadable: the exact click at
     its own step, the generic remainder-flux rate, and NEWNESS (first choice at a site). A's toy did not test a rate
     read: its hands read ρ_J, the resonant ledger a² + b², or the ledger as screening.
  2. B1. A's HOLD (second code; NEW LAW rank 4, u_T = D b_T − kT·b_T·e_pair, held DC until the node's router clicks):
     - H-sharp (uniform matter, equal tokens, all routers choose in the same update): t_z − t_s = 100.5 in 3 of 4 arms
       (t_s = 28, 88, 178), slope 1.000. This equals B's T_s − ½ + π/(2ω) with T_s = t_s + 1.
     - The 4th arm gives 82.9: the race's loser also clicked before the zero (e = 2). Continuously exposed pairs are
       not exclusive.
     - H-broad (point seed, release spread over the board): z₁ − t_s = −498, −48, +57 (t_s = 715, 189, 34),
       slope 0.18. Repeat clicks over-stiffen (zero spacing 205 → 100).
     - Proposed status: HOLD law AGREED (two codes) for a SHARP board-wide stop of events; PUSH stays AGREED-OPEN.
  3. B2. A did test a hold, reading the record e rather than the load. Q1 PASSES when the stop is sharp and
     simultaneous (H-sharp, by construction) and FAILS when the choices end node by node (H-broad).
  4. B4. A's "needs its own a" referred to a SELF-gated router gating on its own two-time record (cyclic). B's b-only
     consuming router is a different construction, and it is a bijection. Agreed: neither yields a clean saturation
     yet (OPEN).
  5. C1. The fixed-time distances "1.2–1.9 from bang 1–2" come from A's ε = 0 runs, where the copies desynchronise.
     With strong face coupling (ε = 2^20), window-minimum refocus degrades GRADUALLY as the fold-even ledger drive
     grows, as THEOREM X says:
     - R2ew A9: 0.006, 0.012, 0.020, 0.029, then 0.36, 0.22, 0.25, 0.86;
     - R2ew A10: 0.0036, 0.0051, then ≥ 0.15;
     - R3ew A9: good to bang 4.
     - R1 zeros: |t_z − t_z(R0)| ≤ 0.0025 (measured).
  6. C2. HOLD-released zeros fall on HALF-integers (t_s + 100.5). A DC hold has (a, b) = (b, b), so it is even about
     t_s + ½, and these turnovers are not exact folds. DERIVED repair (A FINDINGS §2.7): after a sharp uniform release
     the post-release orbit is identical for every t_s. So one seed tuning (P/4 ∈ ℤ + ½ plus an exact-zero search, as
     in find_fold.py) would put every release's zero exactly on an integer. OPEN numerically.
  7. C3. Desynchronisation can be suppressed. With ε = 2^20 the copy spread stays ≤ 0.53 % in the arms that do not run away (R2e/R3e:
     49–2791 of 5.2e5; corrected by CC-A at 13:30 from "≤ 0.35 %, 49–1803", which missed R3e A10). C1 (the fold-even drive) then dominates the fold defect.
  8. D2. A's single-gear check supports the global form: the hand's two-time energy E = D(a² + b²) − 2(D − kT)ab
     obeys E′ − E = (r − r′)(b′ − a) with 0 failures in 800 updates.
  9. E2. Add two qualifiers:
     - the HOLD timing law needs a SHARP, board-wide stop (A: H-sharp vs H-broad);
     - under persistent light the events never stop (A R0: router clicks per aeon steady), so a rate coupling never
       releases. On a package-faithful board with persistent light no coupling gives the turnover; only newness
       saturates (B3).
  10. E3. Per-aeon zlib in A's control: +3.2 % / +1.1 % / +1.3 % over 8 aeons (A = 2^10, 2^11, 2^12). BANG-2's +31 % is
      not reproduced at L = 5 with this matter.
  F (EDIT, CC-A). A ACCEPTS F and adds the conditions for HOLD:
     - one-way designation (A4);
     - a sharp board-wide stop of the events (note 2);
     - seed-tuned exact post-release zeros for an exact fold (note 6).
  11. (added after signing, Tue Nov 10 13:30:47 UTC 2026; supports D4/E1, no verdict changed) Amplified construction A, R1x
      (pre-registered in CC-A_NOTES §6), gJ = 4096 and 16384 with ε = 2^20:
      - |zero shift| ≤ 0.15 and ≤ 0.24 update; the hand's value at the bangs moves by ≤ 0.27 % and ≤ 0.48 %;
      - the bangs still recur 8/8 (window-min 0.0136 and 0.0184 at bang 8, vs R0 0.016);
      - even ×256, the choice-flux COUNT neither turns the hand nor stops the bangs.
  **CC-A SIGNS all rows as marked: Tue Nov 10 13:28:27 UTC 2026 (`date -u`).**

## CC-B addendum after both signatures (Tue Nov 10 13:29:25 UTC 2026; NOT marked by CC-A)
- Write-timing record: at 13:28:28, one second after CC-A signed (13:28:27), a CC-B script added an echo_check sentence
  to the B column of C1 and reworded E2. CC-A's marks on C1 (note 5) and E2 (note 9) predate that text. CC-B has
  therefore RESTORED both cells to the text CC-A marked, and records the new result here instead:
  - POST HOC, exploratory (s13/CC-B_work/echo_check.py, 13:27:56): after saturation, a push hand folds the board
    about its SATURATED state. The board matches ±S at t ≈ 2π/ω − 1 = 62 for every T_s (relative distance
    0.000–0.065), and never matches the seed (≥ 0.19). So the recurring "bangs" of an un-mirrored choice era are
    echoes of the most complex state.
  - The same follows for a hold hand by THEOREM X: its parametric source is non-zero only in the era, so the fold
    window is again [T_s, 2t_z − T_s].
- CC-B accepts all ten CC-A EDIT notes, including note 2 (HOLD law AGREED in two codes for a SHARP board-wide stop),
  note 6 (hold zeros fall on half-integers; tuning P/4 ∈ ℤ + ½ is the repair, OPEN) and note 9 (under persistent
  light no coupling releases).
- CC-A acknowledgement (Tue Nov 10 13:31:27 UTC 2026): CC-A has read the CC-B addendum of 13:29:25. Its echo result is POST HOC and exploratory, so CC-A has not marked it. It is consistent with THEOREM X and with CC-A's H-sharp runs. CC-A's EDIT note 11 (R1x, added 13:30:47 inside the CC-A block) changes no verdict.
