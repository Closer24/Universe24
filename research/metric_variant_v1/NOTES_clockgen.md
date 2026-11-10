# NOTES_clockgen — Study 34: the cosmic hand acts through the clocks only (candidate, DEFAULT OFF)
Builder CLK-A, Tue Nov 10 2026 (UTC). Verifier CLK-B (marks in scratchpad s34/AGREE_CLK.md). Pre-registration and evidence:
scratchpad s34/CLK-A_NOTES.md and s34/CLK-A_work/runs/. NEW files only: layers/clockgen.py, observe/clockgen.py,
tests/test_clockgen.py, this note. No existing package file is changed; nothing calls the new layer by default.
Labels: THEOREM / DERIVED / NUMERIC / BUILT / NEW LAW / IMPOSSIBLE / OPEN.

## 1. The owner's rule and what is built
- Rule (owner, Study 34): no matter gear may read the cosmic hand Θ; one generic rule acting on every clock the same way.
- BUILT, two modes of ONE new block `clockgen` (0 gear types; appended last, so the gear list and every v1 seed are
  unchanged), each ONE designated monomial per node on the lapse:
  - **CG2 = THE OPT-IN CANDIDATE** (`mode="param"`; composer `one_system_clock(law="CG2")`): `u[metric.h00](x) +=
    kappa * b[cosmic.Th](x) * b[metric.h00](x)` — rank 3, on-site (B3), the hand modulates the lapse's own stiffness;
    valid only inside its window (§4).
  - **CG1 = the ADDITIVE CONTRAST** (`mode="drive"`): `u[metric.h00](x) += kappa * b[cosmic.Th](x)` — rank 2; exact and
    felt by every lapse reader, but it cannot bound the uniform lapse (§3).
- Constants: kappa = 1 CHOSEN (declared before any run: the unit weight, as bgk.B's −1 into the lapse); for CG2,
  Θ0 = 2^21 is CHOSEN (window-fitted, owner-approved 17:00 UTC), NOT forced, and the safe Θ0 scales as ~1/L³; h = 2^10 is
  FORCED by the band rule 24 h Θ0 = D − 6.
- One-way, written reason: a reciprocal Φ = κΘF (or κΘF²/2) would put an additive source into the hand; THEOREM O row Θ
  forbids any additive source on the hand (the same reason as the WIND designations).
- Census: 382 gear types, 18,593 monomials, 737 designations, rank 4 (both modes); Θ is read by cosmic.Th (its own 9
  face/self terms), cosmic.M1/M2 (12 + 12, CC-A's readers) and metric.h00 (1). No package gear reads Θ.

## 2. Which clocks feel a cosmic turn (static read graph; DERIVED from the tensor)
- Direct lapse readers: L0 (form C: 1 − 2U on mass, 1 − 4U on transport, every k; 1,104 monomials), the doublet's gwb
  singlet-half hop (transport only: 384 + 384; its rest clock has 0 lapse reads, the FIX-i EP debt), E1 only through the
  designated source dressing (em 192), beta (7, designated). Downstream through the doublet: wsu2, chiral.
- Never (not downstream of h00): su2, su3, u1, the choice observers, bgk, the nine free metric gears, and the cosmic block
  itself (one-way: bit-identical to ONE v1 at every update).

## 3. What the clock law can and cannot do (THEOREM / DERIVED rows; proofs in s34/CLK-A_NOTES.md §4)
- No fold through time: a fold needs ONE sign-changing factor common to every input of a first-order sector (THEOREM O (A));
  the lapse factors (1 − U, 1 − 2U; 1 − 2U, 1 − 4U) are not proportional and stay positive for U < 1/4, where L0's
  transport flips (blow-up, not reversal). A turn reaches matter only as a common clock-rate (redshift) modulation.
- No drift cure (CG1): the k = 0 identity D Σ[F(t+1) − 2F(t) + F(t−1)] = 2Σs + Σ(r − r′) is linear in the source and the
  hand term κH(t) is state-independent (the hand is one-way and bit-identical to v1): it adds a bounded G(t) ≥ 0 and no
  restoring force.
- Multiplicative route (CG2): Mathieu at a = 0 for k = 0 with q_M = 4κΘ0/(DW²); stable only for q_M < 0.908, with the
  held frequency w_eff = ν W/2 < W/2 (ν(q_M) < 1 in the first zone; Kapitza ν ≈ q_M/√2 for small q_M). Integer grain (κ ≥ 1) at today's Θ0 = 2^24 gives q_M = 4.9 (L = 6): outside.
  Every k ≠ 0 lapse mode is adiabatic (w_k/W ≳ 15√L): no low Mathieu tongue and no mean mass; only k = 0 is pumped/held.
- Numbers: s34/CLK-A_NOTES.md §5 (runs RA, RB, RC, RL4, RL6, RW6, F1).

## 4. The owner-approved composer and its VALIDITY WINDOW
- DECISION (manager 17:15 UTC): **ONE v1 STAYS THE DEFAULT.** CG2 at Θ0 = 2^21 (owner-approved hand scale, 17:00 UTC) is an
  explicit **OPT-IN NEW LAW candidate, DEFAULT OFF**: `one_system_clock(law="CG2")`.
- `one_system_clock(law="CG2", theta0_log2=21, kappa=1)`: ONE v1's package + cosmic block with Θ0 = 2^21 (CHOSEN,
  window-fitted, owner-approved, not forced) and h = 2^10 (FORCED by 24 h Θ0 = D − 6; one_system's own rule) + `u[h00] += Θ F` per node. Unchanged: k_theta, g_w, c_pair, load_sum, A_c, Q, P.
  Dynamics fingerprint b5bff0f0…; 382 gear types / 18,593 monomials / 737 designations / rank 4. `law="off"` returns ONE v1
  exactly (77f6d251…). Note: ONE v1 at 2^21 is not bit-identical to v1 at 2^24 in the cosmic block (the WIND hand is
  nonlinear in its scale: turns 676.44 vs 672.05); the package of v1 is (block-diagonal).
- **VALIDITY WINDOW** (`CLOCK_VALIDITY`, `clock_window`): the k = 0 lapse is Mathieu at a = 0 with q_M = 4κΘ0/(D W²); held for
  q_M < 0.908, pumped above. W² ∝ g_w A_c²/(D N), so q_M ∝ Θ0 N/(g_w A_c²): **each Θ0 has a maximum safe board size.** At
  Θ0 = 2^21, g_w = 1310, κ = 1: **valid for L ≤ 6 with A_c ≥ ~0.82·2^10 (840)**. **It FAILS at L = 8** (q_M = 1.43; CLK-B's
  board run K8w: the uniform lapse is pumped, alternating extrema growing ×5.86 and ×7.07 per ~588-update hand period) and at
  L = 7 (q_M = 0.96). At today's Θ0 = 2^24 it fails at L = 4 and 6 (q_M = 1.44, 4.74; runaway, U = 2.5 at t = 1100, L = 4).
  Safe scale (κ = 1, A_c = 2^10, g_w = 1310): Θ0_max(L) ≈ 3.2e6·216/L³ → 2^23 (L 4), 2^21 (L 6), 2^20 (L 7–8), 2^19 (L 9–10),
  2^18 (L 12); the holdable mean source (~ w_eff² P/4, w_eff² ∝ W² ∝ 1/N) falls like 1/N.
- NUMERIC inside the window (Study 34, exact integers): L = 6 J-pure, 4,033 updates (D6): identity 81/81, click ledger
  3,382,992 checks, 0 failures; bits 29 (= v1); the uniform lapse stays within |U| ≤ 3.3e-3 (max at t = 3,604; −1.3e-3 at
  4,033) while ONE v1 rises to +0.024 by t ≈ 4,000 (and runs to −0.186 by 9,869, s30). The pre-registered absolute bound
  |U| ≤ 1.5e-3 FAILED as worded: after t ≈ 3,000 v1's own net source flips sign and grows (U'' ≈ −1.3e-8/update²) and the
  held lapse swings to a new equilibrium; the measured swing is ~3× the averaged linear response (OPEN). L = 4 (CLK-B K4w,
  1000 updates): rewind exact, identity 0 failures, bits 30 (= v1); the spring is weak there (q_M = 0.18) and U tracks v1.
  L0 lumps are not held (blow-up 272 → 328 at L = 6). Turn intervals of the 2^21 hand shorten slowly (193.1 → 184.4 by
  t ≈ 3,900; a property of the re-scaled hand, not of CG2, which the hand never reads).

## 5. Status
OPT-IN NEW LAW candidate (constants owner-approved), DEFAULT OFF. ONE v1 stays the default. Signed rows: s34/AGREE_CLK.md.
