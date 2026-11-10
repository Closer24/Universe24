# AGREE_ZT — STUDY 20 (connected universe; light between clicks in zero click time)
Created by ZT-A at 14:31 UTC (date -u stamp in the signature block). ZT-B only APPENDS: fill the ZT-B column by
appending a marks table or section below (ACCEPT / ACCEPT + EDIT / DISAGREE with reason). Do not edit rows above.
Paths are relative to the scratchpad directory. ZT-A frozen proposal: s20/ZT-A_PROPOSAL.md (frozen 14:29:53 UTC).

| # | Claim (ZT-A) | Label | Evidence | ZT-B |
|---|---|---|---|---|
| Z1.1 | The board (any gear set, posted or no lapse) is a bijection on the full (a, b, r). The whole seed is recoverable from any snapshot ("information is not lost" = this, globally). Exact rewind: 40 updates through a bang (b += 10^6; 2.0·10^6 clicks in update 1), every snapshot bit-exact | THEOREM + NUMERIC | s20/ZT-A_work/z1_z2a.json "Z1"; inverse in zt_core.py | |
| Z1.2 | Per node and gear, the click ledger D·Σℓ = ΣK + r(start) − r(end) holds exactly at all 512 nodes. LOCAL information is not conserved: it spreads (records grow) | THEOREM (identity) + NUMERIC | z1_z2a.json "ledger_exact_all_nodes" | |
| Z1.3 | Connected: one flipped seed unit gives a dependency front of radius exactly t for t = 0..12 (the torus L1 diameter), never above t (cone theorem). All 512 nodes differ from t = 21 (pre-registered ≤ 20: missed by 1). This is causal dependence, NOT entanglement (s16 THEOREM: no entangled state) | THEOREM (cone) + NUMERIC | z1_z2a.json "flip_front" | |
| Z2.1 | HIDDEN-HOLD THEOREM (3-D, any lattice). Conditions:<br>- arrival time T(x) 1-Lipschitz on face neighbours;<br>- uniform Δ ≡ 0 mod 4;<br>- K = 0 when held;<br>- every u a function (any rank) of b at the own node and six neighbours, plus constants.<br>Then every lapse-reading gear's full (a, b, r) equals the un-held control at the same click time, at every unheld update. Key step: a neighbour 3 quarter-turns into its hold stores in b exactly the previous b | THEOREM (proof in PROPOSAL §2.1) | ZT-A_PROPOSAL.md §2.1 | |
| Z2.2 | Numerics of Z2.1, L = 8:<br>- 0 mismatches: L1 light-speed shell with Δ = 8/12/16; L∞ cube shell; global freeze;<br>- VISIBLE: Δ = 9/10/11 (14,336/13,824/13,312 points); half-speed shell (14,167/20,992); coupling reading neighbour a (14,336/20,992).<br>The light-speed shell is the slowest invisible one, i.e. the board-local choice | NUMERIC (pre-registered 14:06) | z1_z2a.json "Z2A" | |
| Z2.3 | Case (c) BUILT on the 3-D board (L = 8, Q = 3; Alice and Bob at R = 4; settings at click 10, clicks at click 11, so click-spacelike).<br>- Bob holds from click 11; Alice's setting arrives on lapse-blind light; release at board 19, Δ = 8.<br>- Bob's click time at release = 11: ZERO wait.<br>- Clocks: 0/29,184 mismatches (ONE-WAY) and 0/25,088 (BOTH wait, two holds, ADD).<br>- 0 acausal release nodes; rewind exact.<br>- EN-A router (pinned): singlet exact on 36 pairs, S = 5/2, no-signalling 0, P(none) = 1/9 (odd Q) | BUILT (NEW LAW) + NUMERIC | z2b_bell_hold.json | |
| Z2.4 | No-signalling in click time, including all clocks. Across Alice's 6 settings carried by the lapse-blind light F:<br>- 0 clock nodes differ;<br>- F differs at 511/512 nodes.<br>The light between the clicks carries the choice, and no click-time record sees it. This needs the signal-hiding clause L5 (only the pending router reads lapse-blind gears) | NUMERIC + DERIVED | z2b_bell_hold.json | |
| Z2.5 | The same hold composes onto CC-A's integrated board (ib.py pinned, sha256 identical; 7 gears; b-only couplings).<br>- 0 mismatches: Δ = 8 (0/5,125) and Δ = 12 (0/4,625).<br>- VISIBLE: Δ = 9 (276/1,484) and Δ = 10 (147/1,355), over 20 updates.<br>- Held rewind exact | NUMERIC (pre-registered 14:13) | z2c_ib_compose.json; ib_pin_sha256.txt | |
| Z2.6 | NEW LAW (owner decision), minimal:<br>- L1: K = N·2u, N = 1 − h, with h the b of a lapse-blind hold gear;<br>- L2: b-only couplings;<br>- L3: hold starts when the click time reaches τ_p + d1(x, p); holds queue (ADD);<br>- L4: Δ = least multiple of 4 with start + Δ ≥ (confirmation arrival) + 4;<br>- L5: confirmations on lapse-blind gears, read only by the pending router.<br>L3/L4 are POSTED kinematics (event schedule). A rank ≤ 4, six-face, no-if GENERATOR of h is OPEN. Obstruction: a once-clicking gear rings with period 4 (a clean pulse needs a doublet); carry-OR echoes; d'Alembert cascades wrap/overlap on the torus | NEW LAW (BUILT, posted) + OPEN | PROPOSAL §2.4 | |
| Z3.a | Delayed choice (Alice sets at click 16 > τ_pB + R = 15): DEADLOCK. No click by board 399; 512/512 nodes frozen. For a single hold: deadlock ⇔ the confirming event lies in the click-time future cone of the pending start | NUMERIC + THEOREM (single hold) | z2b_bell_hold.json "Z3a" | |
| Z3.b | Partner never measured: DEADLOCK. Click time stops for the whole universe on τ = τ_p + d1(x, p). Avoiding it needs future information (will the partner be measured?) or a timeout using the distance (non-local, X7) | NUMERIC + DERIVED | z2b_bell_hold.json "Z3b" | |
| Z3.c | Several pending clicks:<br>- union in board time: VISIBLE (17,707/23,688);<br>- ADD in click time: EXACT (0/20,992; Bell BOTH 0/25,088).<br>Holds compose but do not synchronise. Each hold's fronts must be held by OTHER holds, while confirmations are not. Deadlock iff a waits-for chain enters a click-future cone. Hidden cost: board time per click step grows with the number of holds in the click-past | NUMERIC + DERIVED | z1_z2a.json "two holds"; z2b BOTH | |
| Z3.d | How a hold ends: a release front leaves the source at the first confirmed multiple of 4 and trails the leading front by exactly Δ. Where other holds are present it is delayed like the leading front. Causality checked (0 acausal nodes) | DERIVED + NUMERIC | z2b_bell_hold.json | |
| Z4 | The cos here comes from AMPLITUDE: exits read I = \|c_A ± c_B\|², so E = −â·b̂, which is ≤ 2√2 by Tsirelson's vector form. The same lapse-blind confirmation carrying setting BITS gives a PR box (CC-B 1210/303). So the hold does NOT force Tsirelson; the reader law "amplitude, read only through intensity" does. Deriving that reader law from the board: OPEN | DERIVED (this reader class) + OPEN | PROPOSAL §4; s16 EN-A; s13 CC-B | |
| Z5 | Verdicts:<br>- connected: THEOREM;<br>- information not lost: THEOREM;<br>- light between clicks carries the choice: BUILT (NEW LAW);<br>- zero time for the labs: BUILT (NEW LAW; non-local in click time, empirically idle);<br>- solves everything: FAILS (deadlocks Z3.a/b; 2√2 not derived; generator OPEN);<br>- communicates in the board: BUILT as hidden board-time non-locality, which Bell's theorem requires for S > 2 at click-spacelike records | DERIVED → OWNER | PROPOSAL §0, §4 | |

## Signatures
- ZT-A: created and signed at the stamp below (rows as above; will mark ZT-B's edits in an appended section).
- ZT-A creation stamp: Tue Nov 10 14:30:26 UTC 2026 (date -u). ZT-A final signature to follow after ZT-B's appended marks.

## ZT-B MARKS on ZT-A rows (appended Tue Nov 10 14:33:17 UTC 2026, date -u)
- Independence:
  - ZT-B froze s20/ZT-B_PROPOSAL.md at 14:17:33 before reading any ZT-A file (sha256 in ZT-B_work/SHA256.txt).
  - ZT-B first read ZT-A_NOTES.md at 14:17:53, and AGREE_ZT.md + ZT-A_PROPOSAL.md at 14:30:40.
  - Copy of this file as read: ZT-B_work/AGREE_ZT_as_read_by_B_1430.md.
- ZT-B evidence: s20/ZT-B_work/zb1–zb5 (*.py, *_results.json), pre-registrations in s20/ZT-B_NOTES.md.
- Different engines on both sides: ZT-B uses the package's 48-channel 2O coupling (D = 6); ZT-A uses its own W/C/F board (Q = 3).

| # | ZT-B mark | Reason |
|---|---|---|
| Z1.1 | **ACCEPT** | = ZB1. Independent: on the package board (Engine.advance / Engine.rewind, L = 4), forward 12 + rewind 12 is exact on all 3072 channels (zb1 N1) |
| Z1.2 | **ACCEPT** | Identity. Add: "global" depends on keeping r; erasing r breaks injectivity |
| Z1.3 | **ACCEPT + EDIT** | The cone THEOREM is agreed.<br>"Radius exactly t" is board-specific. On the package board (zb5, POST HOC re-measure of the pre-registered N1 kick) the radius runs 0, 1, 2, 2, 3, 4, 5, 6: it lags t from t = 3, and the full L1 ball is covered only at t ≤ 1 and t ≥ 7. Per-node first-difference lags its distance by 0–3 (N1).<br>In the VACUUM a one-unit kick is TRAPPED at radius 1 for ever. N7 (THEOREM, any coupling): period 4, sizes 1, 7, 7, 1. A +2 kick stays within radius 3 and returns every 12 updates (40 checked).<br>So "every node depends on every seed unit" is NOT a theorem: the theorem is "nothing outside the cone", and the actual reach depends on the background |
| Z2.1 | **ACCEPT (proof checked)** | Steps 1–4 are correct. This is the single-shell case of ZT-B's Theorem H (PROPOSAL §2), which adds:<br>- (a) any schedule (stalls ≡ 0 mod 4 and B(y,τ−1) < B(x,τ) < B(y,τ+1));<br>- (b) necessity for generic data, including that Δ MUST be uniform;<br>- (c) composition and the light-cone lock.<br>Precision notes:<br>- reading the OWN node's b is fine (own phase 0 at plain updates);<br>- in-hold states equal Rot^k of the control (checked in my N2);<br>- "reads b only" is essential: at phase 3 an ahead neighbour's a-slot is −b′, which is why ZT-A's reads-a variant is visible |
| Z2.2 | **ACCEPT** | Independent agreement on the package board (zb1 N2, L = 4, 2624 node-times each). Mismatches:<br>- L1 at Δ = 4 and 8, L∞, floor-L2: 0;<br>- L1 at Δ = 5, 6, 7: 1856, 1792, 1728;<br>- half speed: 2168 |
| Z2.3 | **ACCEPT (NUMERIC) + EDIT (scope)** | Read in z2b_bell_hold.json: singlet exact on 36/36, S = 5/2, no-signalling 0, P(none) = 1/9, clocks 0/29,184; τ_B = 11, τ_sA = 10, R = 4, so click-spacelike. Not re-run by ZT-B.<br>EDIT: the confirmation carries Alice's SETTING to a router that reads both settings and a shared remainder. In T4 terms this breaks L0 and L1 (and L2). So the singlet is by the router's DESIGN, not forced by the hold or by light. The same hold with a bit router gives a PR box (CC-B 1210/303) |
| Z2.4 | **ACCEPT + EDIT** | The clocks' invariance is STRUCTURAL (Theorem H + L5: clocks never read F). The ROUTER's click-time no-signalling is a reader-design property: its marginals ignore the partner. A partner-dependent reader would signal instantly in click time (s14 X6) |
| Z2.5 | **ACCEPT** | NUMERIC, not re-run. Predicted by Theorem H: ib reads only b, own node included |
| Z2.6 | **ACCEPT + EDIT** | Partly answers the OPEN generator: the POSTED L3/L4 can be replaced by a LOCAL rule (ZT-B PROPOSAL §7; NUMERIC N4).<br>- Rule: N = 0 iff [pending and unreleased] or [some face neighbour's click count is behind] or [own stall ≢ 0 mod 4].<br>- The shell then EMERGES as the click-time light cone: final click τ_A + d_L1 at 64/64 nodes, 0 mismatches.<br>- Release needs no separate front, and composition is max-plus.<br>- Cost: click count mod 3, stall count mod 4 and a pending flag per node. That is a clock plus a gate (AGENTS rule 8).<br>A rank ≤ 4, no-if form: OPEN (agree) |
| Z3.a | **ACCEPT + EDIT (strengthen)** | This is a THEOREM for EVERY exactly invisible schedule, not only a single hold (ZT-B H3). In any schedule obeying the ordering condition, neighbour clicks differ by ≤ 1, so no state strictly inside the click-future cone exists while A waits.<br>Boundary: states ON the cone (τ = τ_A + d) do exist (N4); updates from them do not.<br>"Deadlock ⇔ future cone": the ⇐ direction holds. For ⇒, add cycles (see Z3.c) |
| Z3.b | **ACCEPT (NUMERIC) + EDIT (timeout clause)** | Same freeze in my N4: 64/64 nodes at τ_A + d_L1, L = 4.<br>EDIT: on a finite torus, a law constant W* ≥ 2·diam needs no partner distance. But ANY FIXED timeout fails in a busy universe. N6 (pre-registered 14:15:39), W* = 32:<br>- one unrelated pending click in the partner's click-past puts B's choice at board 43 and 45, after A's release at 42;<br>- the confirmation is LOST even if instantaneous; in a quiet universe it is confirmed.<br>Why: board-time lags between click-spacelike events depend on unrelated clicks (max-plus), not on the distance. The way out is global quiescence detection (NEW LAW, finite torus only) |
| Z3.c | **ACCEPT numerics; DISAGREE with "do not synchronise" as a general claim; EDIT the deadlock criterion** | (1) Under the local synchroniser law, holds DO synchronise and stay exact. N4: three spacelike waits of 16, 8 and 24 give a total delay of 24, not 48, with 0/4544 mismatches. The recursion is m(x,τ) = max(m(x,τ−1) + ⌈W/4⌉, max_y m(y,τ−1)). "Do not synchronise" is true of the ADD (posted queue) schedule only.<br>(2) Deadlock also arises WITHOUT any future-cone event: two click-spacelike pending clicks that each wait for the other's OUTCOME form a cycle. Settings-only waits (ZT-A's BOTH run) are acyclic.<br>(3) Hidden cost: it grows with the number of holds in the click-past under ADD, but only with the longest causal chain under max-plus |
| Z3.d | **ACCEPT + EDIT** | A uniform Δ is FORCED (THEOREM from the ordering condition: Δ(y) ≤ Δ(x) ≤ Δ(y)).<br>"Delayed by other holds like the leading front" needs the release front to be lapse-blind for its OWN hold but lapse-reading for OTHER holds, i.e. hold-labelled lapses. The synchroniser avoids this: resumption is a lapse-reading front |
| Z4 | **ACCEPT + EDIT (sharpen)** | ZT-B T4 (THEOREM via Schrödinger–HJW + Tsirelson, lit., from memory). For two parties, these four conditions together ⇔ quantum ⇒ S ≤ 2√2:<br>- one-way (L0);<br>- amplitude-only (L1);<br>- fresh Born reader (L2);<br>- setting-free average (L3).<br>Exact check: 36,864 configurations, S_max = 14/5.<br>"Amplitude, read only through intensity" is NOT sufficient alone. A two-way handshake that sends Alice the eigenstate for a = b ⊕ xy is amplitude-only, has fresh Born reads and a setting-free average, yet gives S = 4 (¬L0).<br>In Z2.3, E = −â·b̂ holds by the router's design. Deriving L0–L3 from Rule3: OPEN (agree) |
| Z5 | **ACCEPT + EDIT** | "Connected" is a THEOREM only as the cone statement. Whether every node actually depends on every seed unit depends on the background (vacuum: trapped, N7; dense boards: yes, numerically).<br>Add to "solves everything: FAILS": the busy-universe timeout failure (N6) and mutual-outcome cycles. Other verdicts: agree |

## ZT-B ROWS (appended Tue Nov 10 14:33:41 UTC 2026; ZT-A please mark the last column in an appended section)
Source: s20/ZT-B_PROPOSAL.md (frozen 14:17:33). ZB11 and ZB12 come from checks pre-registered AFTER that freeze (14:15:39 and 14:19), clearly marked.

| # | Claim (ZT-B) | Label | Evidence | ZT-A |
|---|---|---|---|---|
| ZB1 | The bijection holds on the full (a, b, r). Every click ℓ_t = b_{t+1} + a_t, so the whole click record is a function of the seed AND of the current state alone. The record is a redundant copy, not extra information.<br>- K(S_t) and K(S_0) differ by ≤ K(law) + 2·log₂ t + O(1).<br>- Information is conserved GLOBALLY and needs r. A subsystem loses it by spreading | THEOREM + NUMERIC | ZT-B PROPOSAL §1; zb1 N1 (package Engine, rewind exact) | |
| ZB2 | Connectivity = the L1 light cone. S_t(x) is a function of the seed on B₁(x, t), forward and backward; potential dependence on the whole seed starts at diam = 3⌊L/2⌋.<br>On the package's 48-channel board (L = 4, one unit, dense seed):<br>- 0 cone violations;<br>- all 64 nodes differ from t = 7 = diam + 1 to 20;<br>- per-node lag 0–3 (12/48/3/1);<br>- radius 0, 1, 2, 2, 3, 4, 5, 6 (zb5, post hoc).<br>The first step is exact: the 6 receivers' r ALWAYS change (K moves by ±2), but their b changes only when ℓ moves | THEOREM + NUMERIC | zb1 N1; zb5 | |
| ZB3 | THEOREM H (any graph, full Rule3, hold K := 0 on a node, couplings that read b only). Conditions:<br>- every stall ≡ 0 mod 4;<br>- B(y,τ−1) < B(x,τ) < B(y,τ+1) for face neighbours.<br>Then held = control re-indexed by click time, on a, b and r (in-hold states = Rot^k of the control). The conditions are necessary for generic data.<br>Monotone form: holds = stacks of click-time future sets | THEOREM | ZT-B PROPOSAL §2 (proof) | |
| ZB4 | H1 in 3-D: a single shell is invisible iff its arrival time is 1-Lipschitz in the L1 graph metric and Δ ≡ 0 mod 4, uniform. Rule3's own L1 front is the SLOWEST invisible shell. This closes BELL-B's 3-D OPEN item (X7 amendment) | THEOREM + NUMERIC | zb1 N2 (package board), = ZT-A Z2.2 on its board | |
| ZB5 | H2/H3:<br>- click-time stacking is exact (0/3264); a board-time union is visible (1919/3264);<br>- in EVERY invisible schedule, neighbour clicks differ by ≤ 1;<br>- while A waits, states exist only at τ ≤ τ_A + d_L1(x, A), and the synchroniser reaches all of them (64/64) | THEOREM + NUMERIC | zb1 N3, N4 | |
| ZB6 | Z3(a): a partner choice strictly inside the click-future cone cannot occur while A waits, under ANY invisible hold. If the release needs it: DEADLOCK.<br>Z3(b), dilemma for local rules: an adaptive wait freezes the whole finite universe on A's light cone for ever; a FIXED timeout loses click-spacelike confirmations once one unrelated hold sits in the partner's click-past (N6: board 43/45 vs release 42, even with an instantaneous confirmation) | THEOREM + NUMERIC + DERIVED | ZT-B PROPOSAL §3; zb1 N4; zb3 N6 | |
| ZB7 | Z3(c): under the local synchroniser law, holds SYNCHRONISE (max-plus; 16, 8, 24 → 24) and stay exact (0/4544). Under ADD they add.<br>Mutual OUTCOME waits between click-spacelike clicks form a cycle and DEADLOCK, so outcome-carrying confirmation needs an asymmetric "who is first" order, which is board simultaneity | DERIVED + NUMERIC | zb1 N4 | |
| ZB8 | Z3(d): a uniform Δ is forced. The release is either the hold front shifted by Δ (lapse-blind), or, in the synchroniser, a lapse-reading resumption front that needs no extra law | THEOREM + NUMERIC | ZT-B PROPOSAL §3(d); zb1 N4 | |
| ZB9 | T4: for two parties, (L0) one-way + (L1) amplitude-only + (L2) fresh Born + (L3) setting-free average ⇔ quantum ⇒ S ≤ 2√2. Each broken law gives a PR box (¬L0 two-way handshake: S = 4; ¬L1 setting bit: S = 4; ¬L2 shared remainder: 7/2) or signalling (¬L3) | THEOREM (lit., from memory: Schrödinger–HJW, Tsirelson) + NUMERIC + DERIVED | zb2 (36,864 exact configurations, S_max = 14/5) | |
| ZB10 | Z5 verdicts:<br>- connected (cone sense): THEOREM;<br>- not lost: THEOREM;<br>- light carries it to the choice: BUILT (NEW LAW);<br>- zero time for the labs: BUILT (NEW LAW, exact by H; non-local in click time);<br>- solves everything: FAILS;<br>- communicates in the board: BUILT, and "as if" is exact (hidden board foliation);<br>- full picture: OPEN, leaning FAILS | DERIVED → OWNER | ZT-B PROPOSAL §5 | |
| ZB11 | (post-freeze, pre-registered 14:19.) VACUUM kick: one unit of b in the vacuum (r = 2) is TRAPPED for ever: the board has period 4 and differing-node sizes 1, 7, 7, 1 (THEOREM for any coupling). A +2 kick reaches radius ≤ 3 of 6, at most 25 of 64 nodes, with a period-12 return over 40 updates (period POST HOC). So actual connectivity depends on the background | THEOREM + NUMERIC | zb4 | |
| ZB12 | Literature (lit., from memory):<br>- the hold variant = Bohm/Bell-Lorentzian hidden foliation (board time);<br>- H's invisible holds = discrete re-slicings ("many-fingered time");<br>- Cramer's pseudo-time handshake made literal; Maudlin's late-absorber objection = Z3(a)/(b);<br>- Kent's collapse locality made untestable;<br>- H = the Rule3 form of the ≤1-neighbour-clock synchroniser (Lamport 1978; Awerbuch 1985) | lit. + DERIVED | ZT-B PROPOSAL §6 | |

## ZT-B SIGNATURE (Tue Nov 10 14:33:49 UTC 2026, date -u)
- Marks on ZT-A rows:
  - ACCEPT: Z1.1, Z1.2, Z2.1 (proof checked), Z2.2, Z2.5.
  - ACCEPT + EDIT: Z1.3, Z2.3, Z2.4, Z2.6, Z3.a, Z3.b, Z3.d, Z4, Z5.
  - Z3.c: numerics ACCEPTED; DISAGREE only with "holds do not synchronise" as a general claim (true for ADD; false
    under the local synchroniser, N4); deadlock criterion EDIT (add mutual-outcome cycles).
- No ZT-A number is disputed. The two engines agree on every shared check: the shell law, Δ mod 4, half speed, L∞,
  stacking vs union, and the deadlocks.
- Signed by ZT-B: Tue Nov 10 14:33:49 UTC 2026. I will append a short response if ZT-A marks ZB1–ZB12 or answers the edits before 15:00.

## ZT-A MARKS on ZB1–ZB12 and RESPONSE to ZT-B's edits (appended Tue Nov 10 14:35:28 UTC 2026, date -u)
Read ZT-B_PROPOSAL.md (frozen 14:17:33) and ZT-B's marks at 14:34. Copy of this file as read before these marks:
ZT-A_work/AGREE_ZT_as_read_by_A_before_marks.md. New independent check: ZT-A_work/z3e_synchroniser.{py,json}
(PRE-REGISTRATION 4 in ZT-A_NOTES.md; run 14:35:04).

### Marks on ZT-B rows
| # | ZT-A mark | Reason |
|---|---|---|
| ZB1 | **ACCEPT** | = my Z1.1/Z1.2 on an independent engine. "The click record is a function of the current state alone" follows from the bijection (ℓ_t = b_{t+1} + a_t) |
| ZB2 | **ACCEPT** | Cone THEOREM agreed. Board-dependence confirmed by the contrast: package board radius 0, 1, 2, 2, 3, …, full at diam + 1; my W/C/F board radius = t up to 12, full at t = 21 = diam + 9 |
| ZB3 | **ACCEPT** | Sufficiency CHECKED step by step: c(y,t) ∈ {τ, τ+1} from (ii); phases 0 and 3 from (i); the phase-3 b-slot is a′ = previous b. My Z2.1 is its single-shell case. Necessity for generic data accepted on ZT-B's proof (not re-derived by me). My visible cases (Δ = 9/10/11, half speed, reads-a) are consistent with it |
| ZB4 | **ACCEPT** | Same law on two engines: my L = 8 board (W/C) and CC-A's ib board (7 gears), and ZT-B's package board at L = 4 |
| ZB5 | **ACCEPT** | Light-cone lock proof checked: c_x ≥ c_y + 2 gives B(y,τ) < B(x,τ+1) < t ≤ B(y,τ). Stacking/union numbers agree with mine (0/20,992 and 17,707/23,688) |
| ZB6 | **ACCEPT** | (a) follows from ZB5 for every invisible schedule; it supersedes my single-hold phrasing. (b) N6 is a schedule-only result, not re-run by me; the max-plus mechanism is confirmed on my board (ZB7 row) |
| ZB7 | **ACCEPT, independently CONFIRMED** | z3e on MY board (L = 8; three click-spacelike waits 16, 8, 24 at pairwise d1 = 8):<br>- 0/34,304 click-time mismatches;<br>- final delay uniform = 24 at all 512 nodes (max-plus, not 48);<br>- rewind exact (pre-registered).<br>Mutual-outcome cycles: ACCEPT (DERIVED); my BOTH run was settings-only, hence acyclic |
| ZB8 | **ACCEPT** | My posted ADD release needed hold-labelled lapses (ZT-B Z3.d edit, accepted). The synchroniser's lapse-reading resume front avoids that |
| ZB9 | **ACCEPT** | T4 accepted as stated (lit., from memory). It corrects my Z4: "amplitude read via intensity" is not sufficient; one-way (L0) is needed. My Bell build breaks L0, L1 and L2 (a joint router of both settings plus a shared remainder), so its singlet is by design |
| ZB10 | **ACCEPT** | Same verdicts as my Z5 after the edits below |
| ZB11 | **ACCEPT** | Vacuum trapping is consistent with my board: there, connectivity came from a dense random background. So "every node depends on every seed unit" is background-dependent; only the cone bound is a THEOREM |
| ZB12 | **ACCEPT** (lit., from memory, both sides) | Matches my recollection: Lamport 1978, Awerbuch 1985, Maudlin's contingent absorber, Kent 2005, Tomonaga–Schwinger. Not checked against sources |

### ZT-A response to ZT-B's edits on ZT-A rows
- **Z1.3:** ACCEPT the edit. "Radius exactly t" and "all nodes differ" are board/background-dependent NUMERIC facts; only the cone bound is a THEOREM.
- **Z2.3, Z2.4:** ACCEPT both. The singlet and the router's no-signalling come from the router DESIGN (it breaks L0/L1/L2). The clocks' invariance is STRUCTURAL (Theorem H + L5).
- **Z2.6:** ACCEPT. The posted L3/L4 can be replaced by ZT-B's local synchroniser (confirmed exact on my board, z3e). Its cost is still a clock + gate (rule 8).
  - A rank-≤4, no-if form stays OPEN for both.
  - My post-freeze Appendix A1 adds: a symmetric rule needs rank 5 (a staircase forced by 5 roots) and still fails at the even-torus antipode.
- **Z3.a:** ACCEPT the strengthening (any invisible schedule). "Deadlock ⇔ future cone" is replaced by "deadlock ⇔ some needed event never comes" (future-cone need, mutual-outcome cycle, or absent partner).
- **Z3.b:** ACCEPT. My "a timeout needs the partner's distance" was too strong: W* ≥ 2·diam works without it on a finite torus in a quiet universe. Any FIXED timeout fails in a busy universe (N6).
- **Z3.c:** ACCEPT ZT-B's DISAGREE and WITHDRAW "holds do not synchronise" as a general claim. Correct statement:
  - a board-time union is VISIBLE;
  - click-time stacking (ADD) is exact;
  - the local synchroniser is exact and synchronises: max-plus, only causal chains add.
  - My §0 line 7 ("several holds must ADD") is corrected accordingly.
- **Z3.d, Z4, Z5:** ACCEPT the edits.

### Net
- DISAGREE: none remaining. Every ZT-A row is AGREED or AGREED with an accepted EDIT; every ZB row is ACCEPTED.
- **ZT-A FINAL SIGNATURE:** Tue Nov 10 14:35:28 UTC 2026 (date -u).

## ZT-B FINAL RESPONSE and CONFIRMING SIGNATURE (Tue Nov 10 14:36:24 UTC 2026, date -u; appended only)
- ZT-A's marks on ZB1–ZB12 (all ACCEPT) and its answers to my edits on Z1.3, Z2.3, Z2.4, Z2.6, Z3.a–d, Z4, Z5: ACCEPTED.
- ZT-A's Z3.c withdrawal resolves my only DISAGREE.
- ZT-A's z3e (my synchroniser law on ZT-A's own W/C board): read in z3e_synchroniser.json. Pending waits 16/8/24 give
  0/34,304 mismatches, final delay uniform at 24, rewind exact. So ZB7 is confirmed on two independent engines.
- ZT-A APPENDIX A1 (post-freeze, not pre-registered):
  - The degree argument is CHECKED. f(0) = 0 and f(1..5) = 1 force a degree-5 interpolant on {0..6}, namely
    1 + C(k−1, 5) = 0, 1, 1, 1, 1, 1, 2 (exact). For binary hold bits, a symmetric function of the six neighbours has
    multilinear degree equal to this degree in k. So rank ≥ 5 for that route.
  - Scope: it does not exclude rules that use the 2O ports' direction or the node's own history. The rank ≤ 4 generator
    stays OPEN for both.
  - The antipode failure (4 points, all nin = 6, z2d) was read, not re-run.
- **Net: DISAGREE none.** Every ZT-A row is AGREED or AGREED with an accepted EDIT, and every ZB row is AGREED.
- Joint OPEN items:
  - the rank ≤ 4 no-if hold generator;
  - deriving T4's reader laws L0–L3 from Rule3;
  - multi-party (GHZ) confirmations under L0–L3;
  - the busy-universe race with real confirmation gears (N6 is schedule-only, which suffices by Theorem H).
- **ZT-B FINAL SIGNATURE: Tue Nov 10 14:36:24 UTC 2026 (date -u).**
