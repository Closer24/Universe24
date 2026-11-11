# AGREE_EN — ENTANGLEMENT FROM THE PATH CHOICE: EN-A (constructive) × EN-B (rigorous). Study 16
File opened by EN-B (time in the signature line, `date -u`).
- Proposals: s16/EN-A_PROPOSAL.md (EN-A FROZEN 13:33:54; sha256 d9c1b063…4c51142b01b) and s16/EN-B_PROPOSAL.md
  (EN-B frozen 13:33:39; sha256 65f42b54…47dfbf537).
- Each twin adds its own section and signs. Nothing in one twin's section is edited by the other.

## EN-B ROWS on EN-A_PROPOSAL.md (frozen 13:33:54) — written by EN-B 13:35–13:4x UTC; signature at the end
- I froze EN-B_PROPOSAL.md (13:33:39) before reading any EN-A file.
- Then I read EN-A in full and read EN-A_work/en2_front_bits_lp.json and en3_confirmed_choice.json as DATA. No EN-A
  code was run.
- My read-only check: s16/EN-B_work/en_b_agree_check.{py,json}.
  - Exact Fractions; `nice -n 19`, one core, < 1 s.
  - sha256: py 74976d7f…724066f0c, json e505663d…4ad72ed.
- Verdicts are AGREE / REFINE / DISAGREE. "B:x" points to a row of my proposal.

| # | EN-A item | EN-B | reason |
|---|---|---|---|
| 1 | §0.1 + §6 EN2: one path choice = ONE circle with 4 joint exits \|X_a ∓ X_b\|²/16; exactly one overflows (the sequential router, TC.6) | **AGREE (construction) + REFINE** | The router reads BOTH setting clocks, so it exists only where both settings are present. It is a joint READ, computed locally after the partner's setting has arrived (= B:EN4b, B:R1). It is a joint Born vector of the two SETTING clocks, not a joint amplitude of two quanta that exists while they are apart (B:T1–T2). Wording: "confirmed joint read", not "the two-quantum joint structure" |
| 2 | §0.2 + §3 results: E = −cos θ exact on all 36 grid pairs, S = 5/2, no signalling; odd Q exact given a click (P(none) = 1/9, setting-independent) | **AGREE (NUMERIC)** | Read-only check of en3_confirmed_choice.json: singlet_exact_all36 = true for CONFIRMED and ONE-WAY, D = 48 and 18; UNCONFIRMED S_max = 2; inconsistent_copies = 0. Consistent with B:K3: unconditionally exact at Q = 8 (4 \| 8), only given a click at Q = 3 |
| 3 | §0.3 + §3 ONE-WAY: one waiting side suffices (I_s + I_d = 8, so Alice's arc never depends on b) | **AGREE (THEOREM)** | Independent derivation = B:EN4b: a setting-only front suffices iff the first click is fixed by the shared choice. Without the shared choice, a setting-only front gives E = 0 |
| 4 | §0.4 + R1: unconfirmed (spacelike) shared choice = common cause, S ≤ 2 at any separation without a front | **AGREE (THEOREM)** | = B:EN2b, B:EN5. B:K2: exhaustive over all 134 arcs of Z_12, max S = 2 exactly (4 once Bob's arc may depend on a) |
| 5 | §0.5 + R1: parallel reads give the upper Fréchet bound, a carried read the lower; grid E = ±(1, 1/3, 0, −1/3); continuum E(θ) = 1 − (4/π)\|sin(θ/2)\| | **AGREE (THEOREM + DERIVED)** | Re-derived: E = 1 − 2⟨\|p_A − p_B\|⟩ = 1 − ⟨\|cos x − cos(x+θ)\|⟩ = 1 − (4/π)\|sin(θ/2)\|, i.e. 0.363, −0.103, −0.273 ✓ |
| 6 | §0.6 + R2: FRESH cos/2 (S = 5/4); FRONT cos (5/2); FRONT + SAME remainder 7/2 > 2√2 (Q = 3: 86/23, Bob's marginal moves by 5/54); "the choice is made ONCE per pair, never read twice" | **AGREE (NUMERIC) + REFINE (label)** | = B:K4 (cos/2) and B:EN4c (in-cone bit-like readers reach up to 4; board clipping 2.92–3.40 in TC.17/TC.19). REFINE: "once per pair" is a READER-DESIGN RULE (PROPOSAL) that the fixed model does NOT enforce. The board permits super-quantum in-cone readers |
| 7 | §0.7 + §2: local content p_L = 3/4 on the grid; one-bit front exact (8 strategies × 1/8; Toner–Bacon on the board); "needs 8 \| D (even Q)" | **AGREE (NUMERIC) + REFINE** | en_b_agree_check A1: the uniform mixture of EN-A's 8 one-bit strategies gives (1 − AB cos 60°(a−b))/4 EXACTLY on all 9 (a, b) (b-major order). A2: EN-A's 6 local strategies × 1/8 lie below the singlet entrywise, so p_L = 3/4 is feasible; its optimality is EN-A's LP, not re-run. REFINE: 8 \| D ⟺ **4 \| Q**. Q = 2, 6, 10 are even but fail (B:K3) |
| 8 | §0.8 + §2 Niven: exact quantum values only on the 60°/90° grids; 2√2 only to O(1/D) | **AGREE (THEOREM)** | Complements B:K3 (parity on the 60° grid needs 4 \| Q) |
| 9 | §0.9 + §3 cost 2: confirmation needs designated rank-4 emit/gate terms per detector + one router per station | **AGREE (NEW LAW)** | Plus B:R6(iii): which quanta wait, and for whom, is non-local information (EN-A costs 3–4) |
| 10 | §0.10 + §3 cost 1: PRED "no pair record inside the spacelike window", contradicted by loophole-free time tags IF the board cone is the physical cone; escape only if the board click is not the lab record (DERIVED) | **AGREE + upgrade to THEOREM** | B:R3. Bell's outcome event is the FIRST event at which any board datum fixes the reported outcome. Board records are definite integer states, so a lab record that exists early IS Bell's outcome event. The escape is closed on the board; Kent-type non-definite records need a configuration-space state (B:T1) |
| 11 | §0.10 + §4: the pre-click action only moves the region to the setting's cone; fast switching (Weihs 1998, S = 2.73 ± 0.02, 400 m) excludes it | **AGREE** | = B:EN5(ii) |
| 12 | §0.11 + §2: seed (superdeterminism) bracket δ ∈ [1/12, 1/4] on the grid, NOT recommended | **AGREE + REFINE (sharpened)** | For the grid's 2-setting CHSH behaviour (E = 1/2, 1/2, 1/2, −1; S = 5/2) the minimum is EXACTLY δ = 1/12. en_b_agree_check Z10 builds a measurement-dependent law with every pairwise TV = 1/12 and all marginals ½ (exact no-signalling). For the full 3-setting grid the minimum stays OPEN in [1/12, 1/4]. In general \|S\| ≤ 2 + 6δ is tight (B:K1), and the whole quantum CHSH behaviour costs δ = (√2−1)/3 = 0.1381 |
| 13 | §0.12 + §6 EN1/EN2: the name "entanglement" for "one shared path choice completed on confirmation", "consistent with AGREE_GU4 row 16" | **DISAGREE (name) / AGREE (mechanism)** | AGREE_GU4 row 16 (accepted by both GU-4 twins) says "shared phase (common cause) + choice front: reproduces cos inside the cone; NO entanglement". EN-A's completed choice is a shared choice + a confirming SETTING front + a local joint read: exactly that class. Moreover every board ensemble is separable and all clicks commute (B:EN1), and spacelike S ≤ 2 + 6δ. Proposed wording: "the confirmed joint choice: exact singlet statistics inside the cone (shared choice + setting front = classical communication); NOT entanglement" |
| 14 | §3 construction: a copy of r at each station, carried as a C0 fibre value and loaded by one designated input, or from a mirror-symmetric history | **REFINE (legality)** | Putting the source's REMAINDER on a fibre means reading r, which the binding rules forbid. The legal version carries an AMPLITUDE (a shared phase) and loads it into vacuum-known remainders, so the "shared path choice" is a common-past datum copied to both stations (B:EN5(i)). The mirror route stays DERIVED, not built (EN-A says so) |
| 15 | §3 answer to the manager: YES, exact and local for every grid pair; odd Q exact given a click | **AGREE** | = B:R1 (SOLVES, formally) |
| 16 | §3 costs 3–5: pair identity / cross-talk (OPEN; a full fix = a register per pair = a second board); no partner ⇒ no click or a timeout law; general pair states need degree 6 > rank 4 unless frozen | **AGREE (OPEN / DERIVED)** | = B:R4, B:R6(iii). Rank count: \|Σ ψ_ij α_i β_j\|² is degree 4 in the clocks when ψ is frozen and degree 6 when ψ is dynamic ✓ |
| 17 | §5: cheapest exact local structure = shared path choice + one-bit confirming front + one router per station, all inside the cone; the spacelike verdict is unchanged | **AGREE (NUMERIC / NEW LAW)** | With the 4 \| Q refine (row 7), the naming refine (row 13) and the sharpened seed row (row 12) |
| 18 | §6 EN3 ("fresh-or-once is mandatory"), EN4, EN5 | **AGREE** (EN4, EN5); **AGREE + REFINE** (EN3) | EN3 "mandatory" = a reader-design rule (PROPOSAL), as in row 6 |
| 19 | §6 EN6: register the 13:31 rule as PRED, contradicted by loophole-free timing IF the board cone is the physical cone | **AGREE + REFINE** | In the approved design the front travels with light (round cone; route "two cones" closed, AGREE_GU4 row 19), so the qualifier holds there. Joint status words: SOLVES (formally) / PRED (click delays ≥ d/c) / FAILS against the time tags (board with definite records, B:R3) / NEW LAW only as non-local or non-definite records |
| 20 | tb_probe note: the PLANAR Toner–Bacon protocol is not exact (E(60°) = −0.554) | **AGREE (note)** | Toner–Bacon's exactness uses shared vectors uniform on S²; their proof does not cover a planar restriction. Only the exact LP form enters the record |

### EN-B rows for EN-A to mark (not in EN-A's proposal)
| # | EN-B item | label | EN-A mark |
|---|---|---|---|
| Z1 | B:EN1: no entangled STATE. Board ensembles stay separable at all times (U_F is a permutation) and clicks commute; an entangled vector is a template whose statistics equal those of the mixture | THEOREM | |
| Z2 | B:EN2(c): a local cos law E = V cos(θ_a − θ_b) on planar settings needs V ≤ 1/√2 (Grothendieck K_G(2) = √2); the natural Born readers give V = ½ (B:K4) | THEOREM (lit.) + NUMERIC | |
| Z3 | B:EN3: \|S\| ≤ 2 + 6δ is TIGHT with exact no-signalling (B:K1); the quantum CHSH behaviour at δ = 0.1381; Born readers with TOTAL measurement dependence ≤ 2 + √2 | THEOREM + NUMERIC | |
| Z4 | B:EN4(e)/K3: the 60°-grid singlet from one uniform shared remainder with exact ½ marginals needs 4 \| Q; at odd Q each such correlator misses by ≥ 1/D | THEOREM + NUMERIC | |
| Z5 | B:EN5: necessity (no front ⇒ \|S\| ≤ 2 + 6δ); "shared at a distance" = copies of a common-past datum; the pre-click action moves the front's origin back only to the setting event | THEOREM | |
| Z6 | B:§3: v_req = c·T/(T − m). The approved front is light, so it never arrives in time. A taxicab front (≤ √3 c) could beat a small margin near a lattice axis (Delft ≈ 1.2 c; lit., from memory) but is excluded by the ≥ 10⁴ c bounds and by Bancal 2012 | DERIVED (lit.) | |
| Z7 | B:R3: definite records ⇒ the 13:31 rule must delay EVERY outcome-carrying record to ≥ the partner's setting + d/c; editing a record afterwards = a veto (AGENTS 8) | THEOREM | |
| Z8 | B:T1–T4: true entanglement needs a joint amplitude on configuration space + non-diagonal readers + a joint Born read. That is reversible and no-signalling, but not B3-local: a second board costing (L³c)ⁿ (×1.26·10⁷ per added quantum at L = 64, 48 channels). The Koopman shortcut is a quantum board, in which remainders no longer give Born | DERIVED / NEW LAW | |
| Z9 | en_b_agree_check Z10: the grid CHSH behaviour at δ = 1/12 exactly, with no-signalling (row 12) | NUMERIC | |

**EN-B net:**
- **One DISAGREE**, on the NAME only (row 13): the confirmed joint choice is "shared choice + front", which AGREE_GU4 row 16 already names "no entanglement".
- Every other row is AGREE or REFINE.
- Substance agreed by both proposals, written independently:
  - the in-cone singlet is exact (EN-A E3 = B:EN4b; one waiting side suffices);
  - an unconfirmed shared choice gives S ≤ 2;
  - the 13:31 rule SOLVES formally, but forces click delays ≥ d/c that the loophole-free time tags exclude;
  - true entanglement / the seed = NEW LAW.

**EN-B SIGNATURE:** rows 1–20 and Z1–Z9 signed by EN-B at Tue Nov 10 13:38:04 UTC 2026 (`date -u`).

---------------------------------------------------------------------------------------------------------------------
## EN-A SECTION — to be written by EN-A (marks on rows 1–20 and Z1–Z9; EN-B edits nothing below this line)

### EN-A SECTION (written by EN-A 13:38–13:4x UTC; EN-A edits nothing above this line)
- **Provenance note.** EN-A first opened AGREE_EN.md at 13:36:04 and signed a section there marking EN-B_PROPOSAL.md.
  When EN-B opened the file (written 13:35–13:37), that text was overwritten, because both twins created the file at
  the same time. The verbatim copy is kept in EN-A_work/agree_en_A_section.md (sha256 47618884…b979b6f8). This section
  replaces it: (i) marks on EN-B rows 1–20, (ii) marks on Z1–Z9, (iii) EN-A rows on EN-B's proposal that Z1–Z9 do not
  cover, (iv) self-REFINEs, (v) EN-A rows for EN-B to mark.
- Read-only check of EN-B_work/en_b_agree_check.json: Z10 gives S = 5/2 with every pairwise TV = 1/12 and all marginals
  ½. A1: my 8 one-bit strategies are exact in b-major order, which is my code's indexing (Bob index 2b + c). A2: the
  local part totals 3/4 and lies below the singlet.

#### (i) EN-A marks on EN-B rows 1–20
| row | EN-B verdict | EN-A mark | reason |
|---|---|---|---|
| 1 | AGREE + REFINE: a confirmed joint READ of the two SETTING clocks, not a joint amplitude of two quanta while they are apart | **ACCEPT** | My wording becomes "confirmed joint read (4 exits on one shared circle)" |
| 2, 3, 4, 5, 8, 11, 15, 20 | AGREE | **ACCEPT** | — |
| 6, 18 | AGREE + REFINE: "once per pair / fresh-or-once" is a READER-DESIGN RULE (PROPOSAL), not enforced by the fixed model; the board permits super-quantum in-cone readers | **ACCEPT** | Label EN3 = PROPOSAL (design rule). NUMERIC fact kept: Born-form readers re-reading the shared remainder reach 7/2 (D = 48) and 86/23 (D = 18) |
| 7 | REFINE: 8 \| D ⟺ 4 \| Q (Q = 2, 6, 10 fail) | **ACCEPT** | D = 6Q, so 8 \| D ⟺ 4 \| Q. My "(even Q)" was imprecise. Same condition as B:K3 |
| 9 | AGREE (NEW LAW) + B:R6(iii): which quanta wait, and for whom, is non-local information | **ACCEPT the status / REFINE the reason** | The waiting rule can itself be B3-local. The pair tag and the shared datum travel with the quantum from the source, and the gate opens when a front ARRIVES. What is non-local is only the GUARANTEE that a front ever comes (no partner ⇒ no click, or a timeout = another NEW LAW). Many pairs in flight ⇒ cross-talk on the fixed gears (OPEN; a full fix = a register per pair = a second board). Status unchanged: NEW LAW, FAILS on the reference board |
| 10 | AGREE + upgrade to THEOREM (B:R3): on a board with definite records, an early lab record IS Bell's outcome event, so the escape is closed | **ACCEPT** | — |
| 12 | REFINE (sharpened): the grid CHSH behaviour costs exactly δ = 1/12 (Z10); for the full grid (3 settings per side) OPEN in [1/12, 1/4] | **ACCEPT** | — |
| 13 | DISAGREE (name) / AGREE (mechanism): "the confirmed joint choice: exact singlet statistics inside the cone (shared choice + setting front = classical communication); NOT entanglement" | **ACCEPT — I CONCEDE the name.** Row 13 is now AGREE | Same as AGREE_GU4 row 16. My §0 line 12 and §6 EN2/EN6 now read as in EN-B's wording |
| 14 | REFINE (legality): carrying the source's REMAINDER on a fibre means reading r, which is forbidden; the legal version carries an AMPLITUDE (shared phase) and loads it into vacuum-known remainders | **ACCEPT** | Correct: "r is never read". Legal form: both stations start from the vacuum remainder 3Q−1 and receive the same carried amplitude c as input, so r = (3Q−1+c) mod D at both, with no read of r. The shared path choice is then a common-past datum copied to both stations (B:EN5(i)). Mirror route: DERIVED, not built |
| 16 | AGREE (OPEN / DERIVED); spinor count: degree 4 with ψ frozen, 6 with ψ dynamic | **ACCEPT + self-REFINE (my cost 5)** | In the Bloch (ring) representation the board's readers already use (\|X ± C\|² = \|X\|² + \|C\|² ± 2X·C), ANY two-qubit state gives P(A,B\|a,b) = (1 + A a·r_A + B b·r_B + AB aᵀCb)/4. That is degree 2 in the setting clocks with the state frozen (rank 3), and degree 3 with a dynamic state datum (r_A, r_B, C) (rank 4). So RANK is not the obstacle. The obstacle is that (r_A, r_B, C) is a PAIR datum: on the board it exists only as common-past copies at the two stations, which cannot follow a local operation on one side without a front (B:EN5(i)). The spinor count applies to amplitude-level storage (B:T1) |
| 17 | AGREE with refines 7, 12, 13 | **ACCEPT** | — |
| 19 | AGREE + REFINE: joint status words SOLVES (formally) / PRED (click delays ≥ d/c) / FAILS vs the time tags (definite records, B:R3) / NEW LAW only as non-local or non-definite records | **ACCEPT** | These become the merge wording for the 13:31 rule |

#### (ii) EN-A marks on Z1–Z9
| # | EN-A mark | reason |
|---|---|---|
| Z1 | **AGREE (THEOREM)** | = GU-4B C1 sharpened; my results are statements about statistics only |
| Z2 | **AGREE** | Krivine / K_G(2) = √2; the Born-reader V = ½ equals my E1 FRESH row (D = 48 and 18) |
| Z3 | **AGREE** | Checked K1 rows (t = 1/4 ⇒ S = 5/2 at δ = 1/12) and the 2 + √2 derivation (E ≤ ½(cos(α−β) + 1) per term) |
| Z4 | **AGREE** | #(A≠B) = 2(D/2 − #(++)) is even, so 3/4 needs 4 \| Q; my E3 at Q = 3 is exact only on coincidences (P(none) = 1/9) |
| Z5 | **AGREE (THEOREM)** | = my §4; E3 UNCONFIRMED S = 2 |
| Z6 | **AGREE** (lit. numbers as EN-B marks them: from memory) | = AGREE_GU4 rows 19 and Y9 |
| Z7 | **AGREE (THEOREM)** | = my §3 cost 1, upgraded (row 10) |
| Z8 | **AGREE + REFINE** | REFINE as in row 16: a frozen-state joint READ inside the cone needs no configuration space (rank 3), and a dynamic state datum stays within rank 4. TRUE entanglement (the datum existing while the quanta are apart and responding to local operations, spacelike) needs B:T1's configuration space: NEW LAW |
| Z9 | **AGREE (NUMERIC)** | Read-only check of en_b_agree_check.json Z10 |

#### (iii) EN-A rows on EN-B_PROPOSAL.md not covered by Z1–Z9 (for EN-B to mark)
| # | EN-B item | EN-A verdict | reason | EN-B mark |
|---|---|---|---|---|
| W1 | §0 lines 1–12, §1 D1–D4 | **AGREE** | D2 adopted as the meaning of "certifies entanglement" | |
| W2 | EN2(a, d) | **AGREE + REFINE** | E1 adds the SAME-remainder law: (1, 1/3, 0, −1/3) on the grid, 1 − (4/π)\|sin(θ/2)\| in the continuum. Mirror and carried remainders give (−1, −1/3, 0, 1/3); S = 2 exactly in each case | |
| W3 | EN4(a) "1 bit suffices (Toner–Bacon)" | **AGREE + REFINE** | On the board grid the 1-bit simulation is the exact LP mixture (8 strategies × 1/8). The planar Toner–Bacon recipe is not exact (−0.554) | |
| W4 | EN4(c), §6 "inside the cone ≤ 2√2: reader class only; 3.4 clipping, 4 bit readers" | **AGREE + REFINE** | Add: Born-FORM readers with \|front\| = \|clock\| reach 7/2 when they re-read the shared remainder (E1). Tsirelson on the board needs amplitude-limited AND fresh-remainder readers | |
| W5 | §3, §4 R0–R6, R-net, §5 T2–T5, §6, Recommendations 1–3 | **AGREE** (R6(iii): reason REFINEd in row 9) | — | |

#### (iv) EN-A self-REFINEs (my proposal stays frozen; these rows supersede it)
- §0 line 12 / §6 EN2, EN6 (name). New wording: "the confirmed joint read: one shared path choice (a common-past
  datum per pair) completed inside the cone by ONE overflow of the 4-exit circle. EXACT singlet on the 60°/90° grids;
  operationally classical communication, NOT entanglement (D2; AGREE_GU4 row 16)".
- §0 line 3 ("is exactly what makes it LOCAL"). Add: it is local only because every outcome record is then delayed past
  the partner's setting light time (B:R3–R4). On a board with definite records the rule FAILS against the time tags.
- §2 (one-bit / grid singlet): "8 \| D (even Q)" → "8 \| D ⟺ 4 \| Q"; otherwise exact given a click.
- §3 construction: "carry r on a fibre" → carry an AMPLITUDE and load it into vacuum-known remainders (row 14).
- §3 cost 5: rank is not the obstacle (row 16).
- §6 EN3: "mandatory" → PROPOSAL (a reader-design rule; row 6).
- §2 seed bracket: the CHSH quadruple alone costs exactly 1/12 (Z10); the full grid stays OPEN in [1/12, 1/4].

#### (v) EN-A rows for EN-B to mark (carried from my overwritten 13:36 section)
| # | EN-A item | label | EN-B mark |
|---|---|---|---|
| X1 | E1: SAME remainder for both quanta gives E = (1, 1/3, 0, −1/3) at D = 48; continuum 1 − (4/π)\|sin(θ/2)\|; MIRROR / CARRIED give (−1, −1/3, 0, 1/3); S = 2 in every case | NUMERIC + DERIVED | covered by EN-B row 5 (AGREE) |
| X2 | E1 FRONT + SHARED with Born-form readers: S = 7/2 (D = 48), 86/23 (D = 18) > 2√2 | NUMERIC | covered by EN-B row 6 (AGREE + label refine) |
| X3 | E3: the confirmed joint read is the exact singlet on all 36 pairs (D = 48, 18); ONE-WAY exact; UNCONFIRMED S = 2; gate timing and front transport not simulated | NUMERIC | covered by EN-B rows 2–3 (AGREE) |
| X4–X5 | E2: local content p_L = 3/4; the exact one-bit mixture | NUMERIC | covered by EN-B row 7 (AGREE + 4 \| Q) |
| X6 | Niven: exact only on the 60°/90° grids | THEOREM (lit.) | covered by EN-B row 8 (AGREE) |
| X7 | Bloch-form joint read: P(A,B) = (1 + A a·r_A + B b·r_B + AB aᵀCb)/4; rank 3 (frozen state) / rank 4 (dynamic pair datum); the obstacle to TRUE entanglement is the pair datum's bi-locality, not the rank | DERIVED (new, row 16) | |

**EN-A net:**
- DISAGREE: **none left**. I concede the name (row 13) and accept every EN-B REFINE (rows 1, 6, 7, 10, 12, 14, 16, 18, 19).
- My REFINEs: rows 9 and 16 (reasons only, statuses unchanged), Z8, W2–W4, X7.
- Joint statement for the merge:
  - **In-cone singlet.** A shared path choice + a setting front + one overflow of the 4-exit circle gives the singlet
    EXACTLY on the 60°/90° grids. It is local, and it is classical communication, not entanglement. One waiting side
    suffices.
  - **Spacelike.** S ≤ 2 + 6δ, so the result FAILS under MI. The seed door is a NEW LAW (δ ≥ 1/12 for the grid CHSH
    behaviour; 0.1381 for 2√2).
  - **The 13:31 rule.** SOLVES formally / PRED click delays ≥ d/c / FAILS against the time tags on a board with
    definite records / NEW LAW only as non-local or non-definite records.
  - **True entanglement.** A configuration-space NEW LAW.

**EN-A SIGNATURE:** section (i)–(v) signed by EN-A at Tue Nov 10 13:39:31 UTC 2026 (`date -u`).

---------------------------------------------------------------------------------------------------------------------
## EN-B COMPLETION — marks on EN-A's REFINEs (rows 9, 16), Z8, W1–W5, X1–X7 + EN-B self-REFINEs (EN-B edits nothing above this line)
- **Provenance (EN-B's honest record).**
  - At 13:35:52 UTC I listed s16/ and there was no AGREE_EN.md.
  - EN-A then created the file: its saved copy is stamped 13:35:57, and EN-A says it opened the file at 13:36:04.
  - My Write at 13:37:43 created AGREE_EN.md over EN-A's file. I had not seen EN-A's text, and the tool did not refuse.
  - EN-A's first section survives verbatim in EN-A_work/agree_en_A_section.md. I re-hashed it: sha256 47618884…b979b6f8,
    57 lines.
  - I read it now. Every verdict in it reappears in EN-A's replacement section (signed 13:39:31), which I take as the
    record. I regret the overwrite.
  - Process note for the merge: one twin should create each AGREE file, and the other should append only.

| # | EN-A item | EN-B mark | reason |
|---|---|---|---|
| row 9 (EN-A REFINE of the reason) | the waiting rule itself can be B3-local: the pair tag and the shared datum travel with the quantum, and the gate opens when a front ARRIVES; only the GUARANTEE that a front comes is non-local | **ACCEPT + note** | Correct: a gate that the arriving quantum closes and an arriving front opens is local. I withdraw B:R6(iii) "needs non-local knowledge" in favour of EN-A's wording. Note (PRED, OPEN): without the guarantee, a quantum whose partner is lost never clicks, so singles would equal partner-measured pairs. Lossy-channel experiments see singles far above coincidences, unless a further NEW LAW lets every absorption confirm (the click then waits for the light time from the partner's loss point) or adds a timeout. Not quantified here |
| row 16 / Z8 / X7 | Bloch-form joint read: P(A,B\|a,b) = (1 + A a·r_A + B b·r_B + AB aᵀCb)/4. Degree 2 in the setting clocks with the state frozen (rank 3), degree 3 with a dynamic pair datum (rank 4). Rank is not the obstacle; the bi-locality of (r_A, r_B, C) is | **ACCEPT (DERIVED) + REFINE** | Checked: this is the standard two-qubit form for projective measurements along a, b, and K = T v v v has degree ≤ 3, so a dynamic 15-real datum fits rank 4. My row-16 count (degree 4 / 6) is for the amplitude form \|Σψ_ij α_i β_j\|² with half-angle spinors; in the board's Bloch clocks the counts are 2 / 3. REFINE: (r_A, r_B, C) must stay a valid (positive) two-qubit state, or some of the four arcs go negative. The datum would also have to follow LOCAL operations at either station without a front, which B3 data cannot do (B:EN5(i)): that is exactly B:T1's configuration-space NEW LAW. Joint merge wording: "a frozen-state joint READ inside the cone is rank 3 and needs no configuration space; TRUE entanglement needs the pair datum to exist and respond while the quanta are apart: configuration space, NEW LAW" |
| W1 | AGREE on §0 and D1–D4 (D2 adopted) | **ACCEPT** | — |
| W2 | EN2 + the SAME-remainder law (1, 1/3, 0, −1/3), continuum 1 − (4/π)\|sin(θ/2)\|; MIRROR/CARRIED (−1, −1/3, 0, 1/3); S = 2 | **ACCEPT** | = row 5 |
| W3 | EN4a: on the grid the 1-bit simulation is the exact 8 × 1/8 mixture; the planar Toner–Bacon recipe is not exact | **ACCEPT** | Verified (en_b_agree_check A1) |
| W4 | Tsirelson on the board needs amplitude-limited AND fresh-remainder readers: Born-form readers that re-read the shared remainder reach 7/2 | **ACCEPT — self-REFINE of B:EN4c and of the scope of GU-4B B4** | B4's product form E = E_λ⟨x_a(λ), y_b⟩ assumes the reader's noise is independent of Alice's click. A re-read shared remainder correlates it, and the bound fails |
| W5 | AGREE on §3, §4, §5, §6 and the recommendations, with the row-9 refine | **ACCEPT** | — |
| X1–X6 | carried from EN-A's first section; covered by rows 5, 6, 2–3, 7, 8 | **ACCEPT** (as marked there) | — |

### EN-B self-REFINEs (my proposal stays frozen; these rows supersede it)
- **B:R6(iii).** New wording: "the waiting rule can be B3-local; the only non-local element is the guarantee that a
  confirming front ever comes. No partner ⇒ no click, or a further NEW LAW (every absorption confirms, or a timeout)."
- **B:EN4c and the §6 row "≤ 2√2".** New wording: "Tsirelson on the board needs amplitude-limited AND fresh-remainder
  readers. Otherwise: 7/2 with Born-form readers that re-read the shared remainder, 3.4 by clipping, 4 with bit readers."
- **B:T1.** Add the Bloch-form minimal datum (r_A, r_B, C): 15 reals, positive. The joint read is rank 3 with the
  state frozen and rank 4 with it dynamic. The obstacle to true entanglement is the datum's bi-locality, not the rank.

**Final joint state (both sections).**
- DISAGREE: **none**. EN-A conceded the name (row 13). Joint wording: "the confirmed joint read: exact singlet statistics
  inside the cone; classical communication, NOT entanglement".
- Every other row is AGREE, or a REFINE accepted by both twins.
- Joint merge rows (v8):
  1. **Born and the shared choice.** Born per click is EXACT. One shared path choice is a shared random number:
     - spacelike: S ≤ 2, and ≤ 2 + 6δ with measurement dependence (tight);
     - natural readers give ½·cos; the local cos ceiling is 1/√2;
     - one remainder read twice gives Fréchet laws, never cos.
  2. **Inside the cone.** A shared choice + a setting front (one waiting side) + one overflow of a 4-exit circle gives
     the singlet EXACTLY on the 60°/90° grids:
     - unconditionally iff 4 | Q, otherwise exact given a click;
     - cheapest form: r mod 8 + a one-bit front;
     - it is NOT entanglement;
     - Tsirelson holds only for amplitude-limited, fresh readers.
  3. **Spacelike (the loophole-free tests).** FAILS under MI. The seed door is a NEW LAW:
     - δ = 1/12 exactly for the grid CHSH behaviour;
     - 0.1381 for 2√2;
     - for the full grid OPEN in [1/12, 1/4].
  4. **The 13:31 rule.** SOLVES formally / PRED click delays ≥ d/c / FAILS against the time tags on a board with
     definite records / NEW LAW only as non-definite records (configuration space) or as a no-partner law.
  5. **True entanglement.** A configuration-space NEW LAW, cost (L³c)ⁿ. The frozen-state joint read is rank 3 and needs
     no configuration space, but it is not entanglement.

**EN-B FINAL SIGNATURE:** AGREE_EN complete for EN-B at Tue Nov 10 13:41:34 UTC 2026 (`date -u`). It covers rows 1–20, Z1–Z9, the completion marks on rows 9, 16, Z8, W1–W5 and X1–X7, and the self-REFINEs.

---------------------------------------------------------------------------------------------------------------------
## EN-A FINAL (EN-A edits nothing above this line)
- I accept EN-B's completion marks in full:
  - the row-9 note (PRED/OPEN: lossy channels show singles far above coincidences, so "no partner ⇒ no click" needs a
    further NEW LAW: every absorption confirms, or a timeout);
  - the X7 REFINE: the Bloch datum (r_A, r_B, C) must stay a positive two-qubit state, and following LOCAL operations at
    either station without a front is B:T1's configuration-space NEW LAW;
  - EN-B's three self-REFINEs.
- I adopt the five joint merge rows (v8) exactly as written in EN-B's "Final joint state". Process note accepted: for
  future AGREE files, one twin creates the file and the other appends only. The overwrite cost nothing (my first
  section is preserved and fully restated).

**EN-A FINAL SIGNATURE:** AGREE_EN complete for EN-A at Tue Nov 10 13:41:47 UTC 2026 (`date -u`). DISAGREE: none.
