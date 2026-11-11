> **Historical research record.** This text describes its original configuration and contains superseded paths, defaults and interpretations. For the executable current construction and evidence boundaries, use the [system map](../docs/SYSTEM_MAP.md) and its linked algebra. Claims marked THEOREM or DERIVED below retain their original stated assumptions; they are not a certificate that the current default derives physical laws.

# metric_variant_v1: the composed system (DRAFT for the final freeze; README.md is replaced only by the manager)

Status: INTEGRATOR draft, Tue Nov 10 2026, ~12:30 UTC (R1 + R2 + RC2 batch 1 folded in).
Updated by DOC-UPDATER, Tue Nov 10 2026, 15:18 UTC: owner decisions v8 (approved 14:37 UTC) folded in. These are
FIX-i as the default, the gravity source, the ONE version (section 7e, per NOTES_one.md of 15:15), route B (section 7d)
and the binding owner rules (section 0). REV-ARCH's review fixes of 15:16 are included.
Second DOC-UPDATER update, 15:33 UTC: the owner decisions relayed by the manager (received 15:28 UTC) are folded in.
They are the coupled ONE default (section 7e, per NOTES_one.md of 15:33; superseded at about 16:13 UTC: ONE v1 is the default, see §0 and §7e), rank 4 final, a new seed at each bang, no
freeze and light route A (section 0). Section 10 now lists the 13 results that carry pre-FIX-i values (REV-VERIFY).
Study 33 patch (ONE-SWITCH, prepared 16:21 UTC, `date -u`): the owner rejected the coupled ONE (decision received about
16:13 UTC: matter must not read the cosmic clock). `one_system()` is ONE v1; the coupled build is an opt-in kept for the record
(sections 0, 7e).

This is the algebraic description of the composed default system `layers.system.default_system()`. Each statement
points to code and evidence (section 10). `universe24/` is untouched. The signed account Q (the divisor scale) and the
Noether charges are not established physical energy.

**Departures from AGENTS.md.** This package is a SEPARATE CANDIDATE VARIANT. The reference implementation and its
contract are unchanged; the departures below hold only in this package's declared layers:

* item 1 (one board of 48 channels): many gear types (375 in the hands-ON default, 319 with hands OFF) in declared
  layers;
* item 2 (r in {0, ..., 5}): r in {0, ..., D - 1};
* item 4 (exactly six spatial inputs per channel): layered tensors with on-site and rank <= 4 terms;
* item 5 (constant coupling from the fixed body actions): dynamic links and fields;
* item 6 (divmod by 6): divmod by D = 6Q, ONE divisor for every gear;
* item 8 (no extra gates, no hidden state): designated one-way terms and observer gears, all declared.

**HORIZON (R-P1; updated after GRAV-FIX A, 13:0x).**

* Before the fix, no claim relied on more than about 1500 updates. With the marginal beta, the default + S2\* at even L
  blew up at t ~ 1880 through the beta corner mode (BANG-2, B1-GRAV). This remains the contrast mode
  `v2_beta_marginal_contrast`.
* Fix A (adopted) removes the beta-corner blow-up. S2\* is bounded for 12,000 updates (B1-GRAV).
* Integrator check (S2\*, A = 2^16, L = 6, `results/system/horizon_s2star_detuned.json`): BOUNDED for 2,000 updates.
  At t = 2000, max |G_pi| = 3.55 and U_mean = 0.0020.
* The remaining slow k = 0 growth comes from the seed's NONLINEAR mean source (closed-board collapse): U_mean = 0.63 at
  t = 12,000, about 1.5e-4 per update (B1-GRAV).
* It is projected to reach U = 1, the clock reversal, near t ~ 14,500. In Study 8, clocks reverse in the clicks at U = 1.
* The runs above used the hands-OFF default; hands ON became the default at 13:17.
* With hands ON before FIX-i, bang runs ran away at t ~ 120-420 (s18/AGREE_STAB.md rows R1, R7, R18; section 7c).
* Under FIX-i (the default since owner decision v8-1), the L = 6 bang seeds stayed bounded until their wall budget
  (s18/AGREE_STAB.md A1, A7):
  * S2\* 2^16 to 1196 updates (U_mean -0.036, slowly accelerating);
  * J-pure 2^12 to 1263;
  * S2\* 2^12 to 1500.
* Behaviour beyond about 1200 updates with hands ON is OPEN.

## 0. Owner decisions and binding rules

**Binding owner rules.** Everything emerges from the channels, one tensor and the seed, in integers. Nothing is
posted by hand: no forcing, no fakes, no circularity. No-signalling must follow from the law.

**Owner decisions after Studies 22-23 (relayed by the manager; received 15:28 UTC, `date -u`).**

* **Matter must NOT read the cosmic clock** (owner decision received about 16:13 UTC, `date -u`). It reverses the
  coupling approved at 15:26:41 UTC (the coupled ONE as default). `one_system()` defaults to ONE v1
  (`couple_doublet=False`). The coupled doublet is a NEW LAW candidate, REJECTED by the owner, kept for the record as an
  opt-in only (section 7e). C2 (mass 4916 * 2^22, Θ0 = 256) is a coupled doublet too and stays unapproved.
* **Rank 4 is FINAL.** Rank 5 was considered and rejected (Study 23, s23/AGREE_R5.md).
* **Bangs do not return to the seed.** Each bang starts a NEW seed, the state at the turn. Information is never lost,
  because Rule3 on one tensor is an exact bijection. Echoes are data, not the goal.
* **No freeze on the board.** Light executes the clicks, and only the chosen path produces a click. The zero-time hold
  is excluded.
* **Light: route A**, E1 on the cone with hypercharge global. Route B stays opt-in, OFF (section 7d).

**v8 (14:37 UTC, all approved; s0/OWNER_DECISIONS_v8_he.md).** The items that change this package:

* **v8-1, FIX-i is the default** (s18/AGREE_STAB.md). The graviweak block is built with lam_H = lam_L = 0, and only
  its singlet-half hop is kept. Declared debt: EP for the doublet is OPEN (section 7c).
* **v8-2, gravity source:** the existing source plus GRAV-FIX A. The HYBRID source failed its reversor test, so it
  stays a candidate, default OFF (item 2 below).
* **v8-3, plaquette kind:** a second narrow rank-4 kind, "four links around one square, with no matter field". Only
  route B's opt-in plaquette option uses it (section 7d).
* **v8-8, cosmic clock = the WIND law.** It runs in the ONE version only (section 7e).

**13:09 (approved).** Items 1, 2, 4, 5, 7 and 8 carry later updates in brackets.

1. **Hands (decision 5): CLOSED, ON.** `chiral=True` and `electroweak=True` by default. This switches on Gamma5 V,
   the Higgs (Yukawa, Wilson-Yukawa, the hop that gives the W its mass), graviweak, and the clean seed that leaves the
   mirror world empty. [v8-1: graviweak at FIX-i, i.e. the singlet-half hop only.]
2. **HYBRID gravity source: approved NEW LAW.**
   * One-way: the rest-mass source for matter, and the Tolman two-time energy for the dark board.
   * It is built as a CANDIDATE switch (`layers/gravity_hybrid.py`, ST-2).
   * Final adoption follows a reversor test and a long run.
   * [v8-2: it FAILED the reversor test (NOTES_gravity_hybrid.md H2), so it stays default OFF.]
3. **Universality:** UNIV-BUILDER's "site" form for the gauge matter. The photon is pending.
4. **One rank-4 kind, NARROW:** an uncharged singlet x a gauge-covariant rank-3 composite. "Link x composite" is
   excluded (design rules, section 3). [v8-3 adds the plaquette kind, used by route B's option only.]
5. **Hypercharge, option (A):** E1 is the sole photon and Y is global only. This is recorded as a limitation. [Route B,
   with an exact local U(1)_Y, is built as an opt-in candidate, default OFF (section 7d). The default keeps (A).]
6. **Pati-Salam** is the next build target.
7. **Cosmic clock:** a separate variant (Study 15 in progress). The reference keeps one exact CPT bang. [v8-8: the
   WIND law, composed in the ONE version (section 7e). `default_system()` has no cosmic block.]
8. **Bell outside the cone:** OPEN (superdeterminism via the seed; a test is running). [v8-7: the owner's
   confirmation principle was tested exactly and does not survive the Bell timing data. Only correlation through the
   seed (superdeterminism) remains, a NEW LAW that is not recommended.]
9. **Push:** after the delta reviews.

## 1. The machine

* **One state:** at each site x of the periodic cube (Z/LZ)^3, every gear g carries (a, b, r): two Python-exact
  integers and one retained remainder r in {0, ..., D-1}.
* **One divisor:** D = 6Q, with ONE odd Q for every block (`Tensor.Q`; X1). The default is Q = 2^33 + 1.
* **One forward primitive (Rule3), for every gear:**
  `ell, r' = divmod(2u + r, D);  a' = b;  b' = ell - a`. Write K = 2u. Every update reads only the previous complete
  snapshot.
* **One tensor:** u_g(x) is a polynomial of rank <= 4 in v = (1, b, a) at x and its face neighbours. Rank 4 is final
  (owner decision; rank 5 was considered and rejected in Study 23).
  * `core.tensor.compose` builds it as ONE tensor from per-layer `Block`s.
  * B3 storage locality: each monomial touches at most one face link.
  * The ONE potential: u = dPhi/db (reciprocity). The only exceptions are DESIGNATED one-way terms (X7), each with a
    stated reason.
  * a-reads form an acyclic staged order, which gives the exact staged inverse.
* **Deviation form:** X = X0 + X~ with Phi~ = Phi(X0 + X~) - D X0 X~ - const, so there is no linear term and the vacuum
  has b = 0.
* **Exact inverse:** `Engine.inverse_step` / `rewind` (audit and recovery only; never a forward stage). Every mode in
  X4 rewinds bit for bit.
* **int64 headroom:** `Engine` uses int64 only when an exact Python-int bound on |K + r| fits, and Python ints
  otherwise.
  * Every v2 X-run at Q = 2^33 + 1 ran in int64: vacuum 20/20 steps, random-state 42/42 forward and 6/6 inverse steps,
    `pyint_steps = 0` in all 10 modes.
  * Python ints appear only past the bound: run-away runs (RUN Z) and bigint data.

## 2. Defaults and options (v2; owner decisions 1-8 approved, 5 closed 13:09; v8-1 and v8-2 applied, 14:37)

| item | DEFAULT | options | decision |
|---|---|---|---|
| Q, D | Q = 2^33 + 1, D = 6Q | any odd Q (gravity: Q - 1 = 2Pk; gauge regime Q = 2^(2n+1) + 1) | manager 11:1x |
| vacuum | ONE vacuum (0, 0, 3Q - 1) for every gear, `l0_offset = Q - 1` | legacy `l0_offset = 0` (L0 at 2Q, rhoL0, q-lattice validator) | [OWNER DECIDED: one vacuum, decision 1] |
| mirror | uniform R' (b, a, R'(r)), R'(r) = D - 2 - r (r even) / D - r (r odd); Kramers on matter; E1 staggered | | decision 1 |
| sign class | `body_signs = (1, -1, 1)` (handed): L0 = dark sector (neutral, massive, Kramers); L0 clicks AUDIT-ONLY | (1, 1, 1) | [OWNER DECIDED: sign class, decision 2] |
| L0 lapse | `l0_lapse = "W"` = FORM C (`layers/gravity_l0c.py`) | None, "R" (B1-GRAV rounded), "W_split" (B1-GRAV split; contrast) | [OWNER DECIDED: L0 EP mode = form C, decision 3] |
| EM | `em = "e1d"` (E1, lapse/beta-dressed source) | "e1" (undressed), "compact" | [OWNER DECIDED: E1 departure = PREDICTION, decision 4] |
| chirality ("hands") | ON: `chiral=True`, `electroweak=True` (sections 7b, 7c); EW removes "matter"'s mlapse/mbeta. Graviweak at FIX-i (`gwb_lam_H = gwb_lam_L = 0`): only the singlet-half hop takes a lapse factor. The doublet's mass and the doublet half of its transport take none (EP for the doublet OPEN) | `chiral=False, electroweak=False` (both off; electroweak alone raises); `compose_electroweak(..., gwb_lam_H=None, gwb_lam_L=4)` rebuilds the earlier L2(b) (contrast only: it runs away) | [OWNER DECIDED 13:09: decision 5 CLOSED, hands ON]; FIX-i: v8-1 (14:37) |
| gravity | `lapse = "wave"` (metric + reciprocal lapse + beta) + R-a background gear `bgk` + k = 0 offset (data); beta DETUNED (GRAV-FIX A: w_G = (Q-1)/2, source -(k/2) Lap(F^2), static law G = F^2/(2P) unchanged). Source: the existing reciprocal lapse source | "od2" variant; `beta_form="marginal"` (contrast); HYBRID source (`layers/gravity_hybrid.py`, `apply_hybrid`): default OFF, it failed its reversor test | decision 8; GRAV-FIX A (12:58); source: v8-2 (14:37) |
| choice | odd-Q near-matched router + ONE-SHOT gated exit pair + gate fibre; two period-6 C0 rings | no F7 (taxicab: mechanism test only) | decisions 6, 7 |
| gauge | su2, su3, u1 at `default_regime(Q)` (A = kappa = 2^16, lam = 4, 2-path gears, beta = 6Q - 2^33) | | stage 1-GAUGE |
| c2 base links | OFF | `c2=True`: ZQ8, one OD4 spring per simple component (`layers/c2_zq8.py`), T2 parameters A = 2^14, lam = 2 | RUN Z, C2-TUNE (section 8) |
| matter | B1-EM Dirac pair: hop 2^31, wilson 2^30, mass 4915 * 2^22 | `mass=` | manager 11:2x, R-P1/R-P2 |
| matter lapse | "C" (in effect with hands OFF; with hands ON the EW composer removes it, section 7b'): ONE clock factor on the mass term m W0 only; hops + Wilson in the DIFFERENCE form take the link factor; beta read in the same split (`layers/matter_lapse_c.py`, reciprocal) | "split" (B1-GRAV site/hop; contrast mode `v2_matter_split_contrast`) | manager R1 (11:43) |
| E1 parameters | g_phi = 4, g_A = 1, sigma = 2^24 (dressing coefficients 8, 9; times hs = 2: 16, 18) | | [OWNER/MANAGER DECIDED: sigma/P] |
| P | 2^20 (k = (Q - 1)/(2P) = 2^12) | any P with Q - 1 = 2Pk (sigma in 16P Z / ws) | sigma/P settled 11:1x |

**Mass rule (R-P1 C14 / R-P2):**

* A rational rest frequency rounding-LOCKS weak potential shifts. Locking cases:
  * 3Q (cos w0 = 1/2);
  * 3 * 2^29 at Q = 2^29 + 1 (cos w0 = 1/2 - 9.3e-10);
  * near-rational masses such as 3Q + 24690.
* The default mass is the multiple of 2^22 nearest 2.4 Q:
  * mass = 4915 * 2^22 = 20615004160;
  * cos w0 = mass/D = 0.3999837, w0 = 1.1592972, rest period 5.4198 updates, rotation number 0.1845079.
* Nearest rationals with q <= 40:
  * 7/38 (2.97e-4), 5/27 (6.8e-4), 2/11 (2.7e-3), 3/16 (3.0e-3);
  * nearest with q <= 6: 1/5 at 1.5e-2.
* Stability: mass + 12 wilson = 3.35e10 <= D = 5.15e10 (B1-EM's bound).
  [Corrected; an earlier draft said 2.31e10.]
* Lock check (`demos/system/mass_lock_check.py` -> `results/system/mass_lock.json`; R-P1's method, own script).
  Response ratio dcos_meas/dcos_pred:

  | mass | 0.08 quanta per update | 1 quantum | 2 quanta |
  |---|---|---|---|
  | default | 1.103 | 0.9985 | 0.9991 |
  | 3Q control | 0.000 (LOCKED) | 1.0000 | 1.0000 |

  So the lock is ABSENT for the default mass at 1-2 quanta (PASS). The 3Q control locks at 0.08 quanta. At 1 quantum,
  and at this Q, it is not locked, which differs from my registered expectation.

**Weak-field rule:** matter amplitude x field >= D/(8 g_phi) = 1.61e9 in demos and seeds
(`System.info["weak_field_min"]`). Below it a weak potential's effect can be rounded away.

## 3. The blocks (one tensor; census X9)

| default | gear types | monomials | rank | designations |
|---|---|---|---|---|
| hands ON (decision 5) + FIX-i (v8-1) | 375 | 18553 | 4 | 706 |
| hands OFF | 319 | 10549 | 4 | 1202 |

FIX-i removed 70 graviweak terms (gwb 1222 -> 1152), so the hands-ON count fell from 18,623 to 18,553 monomials. The
`default_system()` dynamics fingerprint changed from 473b7b9f... to b51d3f2c... (NOTES_system.md, owner decision v8-1
paragraph; ONE-B's independent census agrees, s22/ONE-B_NOTES.md).

Hands ON has fewer designations because the electroweak composer removes "matter"'s mlapse and mbeta (496 designated
G reads). The table below lists the hands-OFF blocks; the chiral and electroweak blocks are in sections 7b and 7c.

| block (namespace) | potential / polynomial | generator (symmetry) | Noether / Gauss (with remainder) | declared reversor | rank, degree-3 | designations |
|---|---|---|---|---|---|---|
| ref (L0, 48 gears) | form C: Phi = (D/2)\|b\|^2 - ((Q-1)/2)[b^T M0 b + b^T T b], M0 = 6 - Sum_d W_d, T = Sum_d W_d (1 - shift_d); u = 6b + (Q-1) S b | global 2O labels; right-Q8 (commutes with both sign classes' ports) | J^X(t+1) - J^X(t) = <b(t), T (r(t) - r(t+1))> for every quadratic generator | R' (M' per gear) | 2 (336 deg-1, 1104 deg-2) | 0 |
| lapseL0 (form C) | ((Q-1)/P)[F(x)(3\|b\|^2 - Sum w b_t b_s) + Sum_hops (F_x + F_{x+e}) w (b_t(x)b_s(x)/2 + b_t(y)b_s(y)/2 - b_t(x)b_s(y))] | - | reciprocal: L0 energy sources the wave lapse | R' | 3 (F b b) | 0 |
| su2, su3, u1 | B1-GAUGE compact layers: matter x links + 2-path + OD4 spring (lam = 4) | local Q8 / declared Delta96 / Z4 (bit-exact); continuous Gauss | Gauss/Noether 0 failures (X6) | R' | 4 via the spring only (48 / 1404 / 12 deg-3) | 0 |
| matter (16) | B1-EM sin-Dirac pair + Wilson: hop P_d, wilson W0 Laplacian, (mass + 6 wilson) W0 on site | J' (EM charge), Kramers K | exact link continuity in the free theory | Kramers K o M' | 2 | 0 (112 a-read monomials into matter: E1's centred Phi read, staged) |
| em (E1, 4) | E1: wave A_d, Lorenz accumulator Phi, source sigma s_d (exact hopping current), dressed by f_d = 1 - (F_x+F_y)/(2P) + (9/16)(G_x+G_y)/P | U(1) of J' | dressed continuity, Gauss step, Lorenz C, global charge: 0 failures (X6) | E1 staggered: A_d (a,b) -> (-b,-a,r); Phi (a,b) -> (-Phi_next,-b,r) | 4 (384 designated deg-3) | 662: source 96, dressed 384, on-site alpha.A 160, centred Phi read 16, accumulator 6 |
| metric, lapse, beta | B1-GRAV wave metric + beta = 1 auxiliary G (its source -k Lap(F^2)); the matter's lapse and G read are the C blocks below | - | wave identities (B1-GRAV) | R' | 3 | beta source 7 |
| mlapse (matter lapse C, R1) | -(1/2)(F/P)(m/2) b^T W0 b - (1/2)((F_x + F_y)/P)[hop b_y^T P_d b_x + (w/2)(b_x - b_y)^T W0 (b_x - b_y)] | - | reciprocal: the lapse source is the b-only mass + link gradient energy (section 8) | R' | 3 | 0 |
| mbeta (beta read C, R1) | +(G/(4P))(m/2) b^T W0 b + (9/16)((G_x + G_y)/P)[links as above] | - | one-way | R' | 3 | 496 (G read) |
| bgk | R-a background gear B (u = 6Q b), -b_B into metric.h00 | - | static | R' | 1 | 1 (R-a datum) |
| arm1, arm2, router, gate, exit | period-6 C0 rings; odd-Q near-matched router (kappa = near_matched_kappa(Q,1); P(none) = 1/Q per readout); ONE-SHOT gated exit pair (rank 4) | - | - | R' | router 2, exit 4 (18 designated) | 36 (observer detectors) |
| c2 (option) | ZQ8 Z[Q8] links, kappa A = port weight, one OD4 spring per simple component (4 sign characters eps + H) | LOCAL Q8 by permutations (bit-exact) | exact Noether (V- isospin) | R' | 4 (springs) | 0 |

Designations total 1202 in the v2 default (X7: `check_reciprocity` ok; 1106 in the split contrast). No constants.
Every degree-3 term is one of:

* an OD4 spring;
* the ONE approved narrow rank-4 kind (owner decision 4): an UNCHARGED SINGLET x a GAUGE-COVARIANT RANK-3 COMPOSITE.
  "Link x composite" is excluded;
* designated.

v8-3 approved a second narrow kind, the plaquette ("four links around one square, with no matter field"). No default
block uses it; only route B's opt-in plaquette option does (section 7d).

## 4. The vacuum

* Every gear sits at (0, 0, 3Q - 1).
* R' fixes this vacuum for odd Q.
* It is stationary: X3 shows 0 changed gear updates in 20 steps, in every mode.
* The L0 embedding (a, b, r) -> (a, b, Q r + s) with s = Q - 1 reproduces today's board bit for bit. X3 confirms it
  (offset embedding exact) when L0 is not form C.
* Form C changes L0's dynamics (ports at Q - 1, plus on-site 6). It keeps the vacuum.

## 5. The mirrors

**Joint mirror (X5).** X = R' on every gear, with two exceptions:

* Kramers K o M' on the Dirac matter;
* E1's staggered map on A and Phi.

It satisfies X F^n X F^n = N, with N = Jp on matter and the identity elsewhere. Results:

* exact on 2 random states;
* fixes the vacuum in every wave mode (v2 default, +++, no L0 lapse, W_split, compact, e1, P = 2^16, c2 on, legacy).

**Plain M' on the matter fails** (control): E1 needs Kramers.

**OD2 variant:**

* declared M' (NOT M) on h_ij (DEV-GR4);
* h0i (a, b) -> (-h0i_next, -b);
* h00 (a, b) -> (h00(t+2), h00(t+1)).

The OD2 one-way single-time lapse read has no exact time mirror under B3 (C8): its X5 fails, as recorded.

**R\* (Study 6 seed reversor; `observe/seed.py`, audit map).** It is the spatial inversion x -> c2 - x composed with the
time mirror. c2 = 2 x0 + e_y (link-centred S2*) or 2 x0 (node). It acts as:

* matter: Gamma = J'K W0;
* A_d: (-b, -a), re-based;
* Phi: staggered;
* every other gear: (b, a), with the vacuum-fixing remainder map.

It is declared EXACT on the matter + E1 sector (SD4: F^-t = R* F^t, 6/6).

**L0 under R\* (RC2; BANG-1, Study 8 T10d(ii)).** R\* needs L0's SIGNED RELABELLING S = chi o P, now composed in
(`observe.seed.l0_relabelling`, `r_star(..., body_signs=...)`).

* S solves S M_opp(d) S^-1 = M_d for all six directions. There are 8 solutions per class, the right-Q8 coset.
* +++: involutions exist (S^2 = 1).
* Handed class: the involutive choices square to S^2 = -1. This is Kramers, and no L0 datum is fixed. The package uses
  the order-8 solution, whose fixed space is 6-dimensional.
* P fixes no label, so R\*-fixed L0 seeds are S-symmetrised (`prepare.seed.l0_rstar_vector`).
* SD6 on the FULL v2 default: F^-t = R* F^t is exact for t = 1..6 for S2\* and both symmetrised L0 dark seeds.
* The old declared R\* (no relabelling) fails at t = 1 for the L0 seeds and still holds for S2\*.

## 6. The three readings

* **Board:** the full state (a, b, r), used for audit. Its audit identities are:
  * Noether currents J = D Sum a.(T b) and their remainder terms;
  * Lorenz C;
  * dressed Gauss Y;
  * OD2 constants.
* **Clocks:** sign-cycle CLICK rates. The click size is ell = b' + a, read at crossings (`observe.gravity.crossing_times`).
  * Form C makes every massive L0 band obey the EP half-angle law sin(w/2) = sqrt(1 - 2U) sin(w0/2) EXACTLY.
  * The +++ light keeps speed sqrt(1 - 4U) (gamma = 1).
* **Proper-time ticks (manager R2, `observe/readout.py`):** one tick = one sign cycle of the click sizes in the
  clock's OWN ROTATING FRAME.
  * The fixed carrier is identified FROM THE LAW, never from a species label.
    * "No species words" holds for the R2 readout functions (`carrier_from_law`, `own_frame_series`, `tick_rate`).
    * The readout-CLASS functions key on gear labels and namespaces by design (`dark_l0_violations` uses "ref").
  * Carrier fit: `carrier_from_law` fits the free k = 0
    operator as c 1 + kappa x (the lapse-touched operator) and returns theta = arccos(c/D).
    * Dirac: c = 0, so theta = pi/2 (residual 1.9e-16).
    * L0 (form C): c = D, so theta = 0 (residual 1.6e-15).
  * J^-t is applied to the consecutive click pair (l(t), l(t+1)), with J the zero-input Rule3 rotation (x, y) -> (y, -x).
  * The raw sign-cycle reading is kept as the contrast.
  * The ESTIMATOR is exactly `own_frame_series` followed by `tick_rate`, the least-squares slope of the
    interpolated sign crossings.
    * The own-frame series carries an image tone (relative amplitude ~0.21, R-P2).
    * A naive count of sign changes is biased by about +1.8e-4. The interpolated slope is not.
  * EP is exact in the tensor: one clock factor on every mass term (after R1).
    * N_rest = 1 - U is exact for the cos-ratio reading.
    * The own-frame tick ratio is 0.9894 at U = 0.01.
    * This holds for the hands-OFF R1 matter and for L0. With hands ON + FIX-i (the default), the doublet's mass has no
      clock factor, so EP for the doublet is OPEN (section 7c).
  * UNIVERSALITY LIMIT (R-P1 A1). "EP exact in the tensor" holds for the Dirac pair and L0 ONLY.
    * MISSING: the su2/su3/u1 layers' own matter and the E1 photon do not read the lapse.
    * MISSING: the E1 field energy does not gravitate.
    * gamma = 1 and Shapiro hold for L0 light in the +++ option only.
  * In clicks the EP is universal to O(U) for slow clocks.
  * A lattice-scale, frequency-dependent redshift proportional to U w0^2 is a PREDICTION. R-P2 verified its law:
    delta/(U w0^2) -> -1/3 (Dirac) and -1/12 (L0), where delta = tick ratio - slow-clock N.
    * Default Dirac rest clock: delta = -6.0e-4 (table: 0.989404 - 0.99 = -5.96e-4).
    * L0 mu = 0.536: delta = -1.52e-4.
  * Tick ratios at the default mass, U0 = 0.0100002 (`results/system/L0C_clock.json`; prediction vs measurement):

  | clock | own-frame w0 | predicted w/w0 | measured w/w0 | deviation |
  |---|---|---|---|---|
  | Dirac rest clock (sin w_d = (1 - U) sin w_d0, w_d = pi/2 - w_raw) | 0.41149 | 0.989404 | 0.989391 | -1.3e-5 |
  | L0 (+-+) mu = 0.536 (sin(w/2) = sqrt(1 - 2U) sin(w0/2)) | 0.42586 | 0.989797 | 0.989797 | 5e-8 |
  | L0 mu = 2 | 0.84107 | 0.989322 | 0.989322 | -2e-8 |
  | L0 mu = 4 | 1.23096 | 0.988482 | 0.988482 | -2e-8 |
  | L0 mu = 6 | 1.57080 | 0.987266 | 0.987267 | 2e-7 |
  | L0 mu = 7.46 | 1.81730 | 0.985926 | 0.985926 | -1e-7 |
  | L0 (+++) mu = 8 | 1.91063 | 0.985267 | 0.985267 | -5e-7 |
  | slow-clock limit N = sqrt(1 - 2U0) | -> 0 | 0.989949 | | |
  | contrast: raw Dirac sign cycles | 1.15930 | | 1.00376 (ticks FASTER) | |

  All 15 massive L0 bands of both classes and the Dirac clock agree with the prediction within 1e-4 (R2 PASS). These
  match the manager's estimates: Dirac 0.98940; L0 0.98980 / 0.98932 / 0.98527; raw Dirac 1.0038.
* **Clicks:** the official click stream (`Engine.clicks`, stream "official").
  * Readout labels are passive (`observe/readout.py`).
  * The readout class of every gear is its tensor label (RC2 F-R).
    * "audit" (OD1-type): metric and potential gears, gauge links and EM potentials, and, under the handed class, L0
      (the dark sector).
    * Hands-ON default: 320 audit gears and 55 official; +++: 272 audit and 103 official
      (`results/system/rc2_batch1_checks.json`). Hands OFF: 280 audit and 39 official; +++: 232 audit and 87 official.
  * L0 clicks are therefore AUDIT-ONLY in the default. This is a label, not a law.

## 7. The seed as data (`prepare/seed.py`; data only, AGENTS item 9)

* **S2\*:** b(x0) = A e_i, a(x0 + e_y) = A Gamma e_i (two integers).
* **node R\*:** the node-centred alternative.
* **L0 (dark) seed:** a(x0) = b(x0) = A v on L0 gears, as a separate datum.
  * It is legal (SD1) and R\*-fixed (SD2).
  * It bounces (F^-t = R\* F^t) ONLY with the relabelled R\* (section 5), on the S-symmetrised seeds from
    `l0_rstar_vector` (SD6).
  * The one-channel seed does not bounce.
* **R-a background datum:** bgk.B = (v, v).
  * `ra_free_mean` (prepare/seed.py, wrapping B1-GRAV's prepare/gravity_ra.py) gives the EXACT first-order time mean of
    the lapse source per Fourier mode, for seeds that excite L0.
  * For S2\* the first-order mean is exactly 0. Its positive mean source is nonlinear, so no cancellation is claimed.
* **k = 0 offset:** on metric.h00.
* **P+ seed:** documented TODO hook.

Tests SD1-SD5 (`tests/test_seed.py`) on the v2 default, L = 6, A = 2^12:

* Every seed is legal: Lorenz C = 0, charge density 0, Gauss Y = 0, and E1 still at vacuum after one update.
* Each seed is R*-fixed and rewinds exactly over 10 updates.
* The bounce F^-t(s0) = R*(F^t s0) is exact for t = 1..6 (S2*, node R*).
* The R-a gear stays static, and the offset appears only in metric.h00.

## 7b. Chirality (OWNER decision 5 CLOSED 13:09: ON by default)

**Status:** OWNER decision 5 CLOSED (13:09): ON by default, together with the electroweak completion.

**Switch.** `default_system(chiral=True, electroweak=False)` uses HAND-M1's one-line switch:
`from .chiral import compose_with_default; return compose_with_default(System(Q, tuple(blocks), info), on=True)`.
The default is now `chiral=True` (with `electroweak=True`). `chiral=False, electroweak=False` switches both off.

**The block** (`layers/chiral.py`, NOTES_chiral.md):

* A weak SU(2) acts on a species doublet: the default `matter` plus a partner `matter2`.
* It acts only on the components selected by P_W = (1 - G5 V)/2, with V = J J'. This is P-odd, C-odd, CP-even and
  CPT-even.
* Masses and the Wilson term are the vacuum imprint of a Higgs quaternion Phi = v + phi (Yukawa and Wilson-Yukawa).
* At phi = W = 0 the matter is build_matter's free Wilson-Dirac pair, bit for bit.
* With matter lapse C the partner takes the same universal lapse and beta read (`mlapse2`, `mbeta2`).

**Tests:**

* B0-VERIFY RC2: chiral AGREE.
* Integrator check (`results/system/rc2_batch1_checks.json`): `default_system(chiral=True, electroweak=False)`, the
  chiral-only build of RC2 batch 1 with `mlapse2`/`mbeta2`, builds (G = 375, 19665 monomials). The vacuum is fixed for
  3 updates, and rewind is exact over 3 updates.
* `tests/test_chiral.py`: see NOTES_system.md, RC2 results.

**Declared limits:**

* L1: there is no hypercharge, so the composed W Gauss laws break.
* L2: the matter lapse breaks local SU(2) at O(U).
* L3: there is no Higgs kinetic term, so the W is massless.
* L4: mirror doublers, and a J- world.
* L5: the weak window is <= 2^12.

## 7b'. Hands ON in the composed default (RC2 batch 3, `results/system/v2_default.json`)

**Exact properties.**

* X1 one Q.
* X3: vacuum unchanged over 20 updates.
* X4: rewind exact.
* X7: reciprocity ok, 706 designations.
* Gauge Noether: 0 failures.
* int64 only: vacuum 20/20 steps, random state 42 forward + 6 inverse.

These were measured before FIX-i. After FIX-i, test_system (X1-X10), test_seed, test_chiral and test_electroweak
passed in ONE-A's mirror run of the FIX-i code (14:56-15:03 UTC, s22/ONE-A_work/pkg_tests_rel9_mirror.log). The
official re-check is REV-VERIFY's (Study 25).

**Mirrors with hands ON (RC2 batch 4).** Both are composed from the chiral layer's own maps.

* **X5, joint time mirror** (`observe.system.joint_mirror_hands_on`):
  * X_on = T_phys = C K o M' on both pairs, with sig on the Higgs, the W links and the 2-paths;
  * E1's staggered map composed with the C-flip of the E1 fields: Phi (a, b, r) -> (+Phi_next, +b, R'(r)) and A_d
    (-b, -a, r);
  * M' elsewhere (rhoL0 on L0 at the legacy offset 0).
  * Result: X F^n X F^n = X^2 (Kramers) exactly on 2 random states (n = 6), and X fixes the vacuum, in the hands-ON
    default and in every hands-ON wave mode.
  * Exceptions: the OD2 variant (C8, as before) and compact EM. Compact EM's U(1) links need the conjugation
    U -> U\* under C, which is not composed in; that is the obstruction there.
* **R\*, seed reversor** (`observe.seed.r_star_hands_on`), all about the seed's own centre:
  * the chiral layer's inversion maps: Gamma = W0 J' K on both pairs, Higgs sig, W links and 2-paths sig o conj (links
    re-based, 2-paths reversed);
  * E1's inversion maps and L0's signed relabelling.
  * SD7 on the hands-ON default: F^-t = R\* F^t exact for t = 1..6 for S2\* and for the S-symmetrised L0 dark seed.

**Charge and E1 with hands ON (X6; checked against NOTES_electroweak.md EW4/EW4b/EW5b).**

* The TRUE electric charge Q = T3_L + T3_R + (B - L)/2 of matter + W is an exact GLOBAL Noether charge. EW4b found
  0/6 failures, including the adjoint action on links and 2-paths.
* E1's field is blind to the W's charge: it couples J' on pair 1 only (EW4).
* So E1's LOCAL Gauss law and continuity fail during weak processes. In X6, on a random state with the W excited,
  continuity and the Gauss step fail 162/162 and E1's own pair-1 charge fails 6/6. EW5b finds t1 and t2 failing
  54/81 each from the charged W. The Lorenz constraint stays exact.
* This is the decision 5(A) limitation. Closing it needs local hypercharge: route B, a NEW LAW (one U(2) link per
  face, NOTES_electroweak.md). Route B is now built as an opt-in candidate (section 7d).
* X10: 16 gears are written by several blocks (matter and matter2 by their own blocks plus the chiral, Higgs-hop and
  graviweak blocks). 0 are both designated and forced.

**R1.** With hands ON, the R1 matter lapse of "matter" (`mlapse`, `mbeta`) is removed, because it dresses the bare
mass and would break SU(2).

* Under FIX-i (v8-1) nothing replaces it for the doublet: only the singlet-half hop keeps a lapse factor.
* The doublet's mass and the doublet half of its transport get no lapse factor, so EP for the doublet is OPEN
  (declared debt, section 7c).
* The earlier lapse x |Phi|^2 dressing (EW3b: EP at O(U^2), adiabatic) is no longer the default, because it was
  linearly unstable (section 7c).

* R1's block tests (test_l0c C3) still test `matter_lapse_c` itself; it is used whenever hands are OFF.
* The hands-OFF configuration stays covered: the X5/X6 assertions run on `v2_handsOFF`.

**Seeds.** S2\* bounces exactly with hands ON using the composed R\*_on (SD7, above). The hands-OFF r_star without
the chiral maps fails from t = 2 (report). SD1-SD6 run hands OFF.

**Builders' tests.** test_chiral and test_electroweak build their own base. Since 13:25 they call
`default_system(Q, chiral=False, electroweak=False)`, a one-line fix in each file made by the integrator with the
manager's authorisation. All 18 tests pass.

## 7c. Electroweak completion (OWNER decision 5 CLOSED 13:09: ON by default)

**Status:** OWNER decision 5 CLOSED (13:09): ON by default. Graviweak at FIX-i since owner decision v8-1 (14:37).

**Switch.** `default_system(chiral=True, electroweak=True)` (the default) uses EW-BUILDER's line:
`from .electroweak import compose_electroweak; return compose_electroweak(System(Q, tuple(blocks), info), on=True)`.

* It REQUIRES `chiral=True`. `electroweak=True` with `chiral=False` raises ValueError.
* The composer builds the chiral candidate itself, with `partner_lapse=False`.
* It removes the default `mlapse` / `mbeta` of "matter", which would break SU(2), and adds its own lapse coupling
  (under FIX-i, the singlet-half hop only).

**BUILT** (`layers/electroweak.py`, NOTES_electroweak.md):

* The W mass via the Higgs hop: m_W proportional to v sqrt(kappa_H), to 1 %. FIX-i keeps it.
* Graviweak at FIX-i (owner decision v8-1, 14:37; s18/AGREE_STAB.md, signed by STAB-B and EW-BUILDER):
  * `compose_electroweak` builds the block with `gwb_lam_H = 0`, `gwb_lam_L = 0`, i.e.
    `build_graviweak_b(lam_H = 0, lam_L = 0)`. Only the singlet-half hop, with its link factor, is kept. It is
    SU(2)-covariant and rank 3, and it is not a new law (existing parameters).
  * Why: the earlier default, lapse x |Phi|^2 plus the link factor x |U|^2 (lam_H = lam_L = 4), was linearly
    unstable. The k = 0 lapse mode had lambda = 1.138 and the corner (pi, pi, pi) had lambda = -1.026, so bang runs
    ran away at t ~ 120-420 (AGREE_STAB rows R1, R2, R7, R18).
  * FIX-i is marginal at every k checked, the corner included. The vacuum, rewind and R\* are exact (L = 6). The L = 6
    bang seeds stayed bounded until their wall budget, 1196-1500 updates (rows R9-R11, addenda A1, A7). Behaviour
    beyond about 1200 updates is OPEN.
  * Cost (declared debt): "the Higgs sets the clocks" is OFF. The doublet's mass and the doublet half of its
    transport get no lapse factor, so EP for the doublet is OPEN. The doublet's mass and the W/Higgs energies do not
    source the lapse. The beta read of the doublet stays OPEN.
  * Contrast: `compose_electroweak(..., gwb_lam_H=None, gwb_lam_L=4)` rebuilds the earlier L2(b), which runs away.
  * L2(b) + FIX-C+ (tuned lapse counter-terms) is a NEW LAW candidate and is not in the package. v8-1 defers it
    until after long runs.

**NOT IN THE DEFAULT: local hypercharge.**

* E1 is the correct photon after the breaking.
* An exact local U(1)_Y needs a U(2) link per face. Route B builds it as an opt-in candidate (section 7d).

**Checks:**

* The integrator check (`results/system/rc2_batch1_checks.json`): the build, the vacuum fixed for 3 updates, exact
  rewind over 3 updates.
* `tests/test_electroweak.py` (EW-BUILDER).

## 7d. Route B: local hypercharge (opt-in candidate, default OFF; NOTES_electroweak_b.md)

`layers/electroweak_b.py` (EW-BUILDER) provides `compose_electroweak_b(base, on=True)` on the hands-OFF base. It
retires E1 and adds one U(2) link per face. `EWB_DEFAULT_ON = False`, so the default is unchanged.

* Exact LOCAL SU(2)_L x U(1)_Y: the Gauss laws of all four generators (t1, t2, t3, Y) hold exactly with the
  remainder term (EWB2, EWB4: 0 failures).
* Photon (the W3/B mix) <= 0.41 c_Q:
  * it is frozen in the 2-path build;
  * the relayed plaquette option (v8-3 kind) reaches 0.408 c_Q at its best band-legal point (EWB6c);
  * for the built layout the ceiling is c_Q/sqrt(3), from relay inertia: under B3 each link is carried by itself
    and two relay copies, each a full gear with inertia D (one divisor), so its inertia triples.
* ONE LIGHT is OPEN: a photon slower than gravity is contradicted by GW timing.
* Following FIX-i (v8-1), route B has no graviweak coupling at all, so the doublet has no lapse coupling (OPEN).

## 7e. ONE version (Study 22; NOTES_one.md)

ONE is one tensor, one Q, one seed and one run: the package default (hands ON + FIX-i + GRAV-FIX A) plus the cosmic
clock layer (owner decision v8-8: the WIND hand, matched choice pairs and Θ-reading matter). The doublet is NOT coupled to
the hand: `one_system()` is ONE v1. The coupling is a NEW LAW candidate, REJECTED by the owner (matter must not read the
clock); measured runaway at L = 6 t ≈ 1,547–1,554 and L = 4 t ≈ 662 (Study 30); kept for the record as the opt-in
`couple_doublet=True` (fingerprint 593753fa..., unchanged).

The account, the tests and the results are in NOTES_one.md; ONE-B's marks are in s22/AGREE_ONE.md.

* Code (new files, ONE-A): `layers/one.py` (`one_system`), `prepare/one.py` (the seed, data only), `observe/one.py`,
  `demos/one/` and `tests/test_one.py`. The cosmic layer is a NEW LAW approved by the owner; the coupling was approved,
  then rejected (opt-in only).
* **Opt-in only: the coupled ONE (C1)**, `one_system(couple_doublet=True)` (demo flag `--couple`). Approved 15:26:41 UTC,
  REJECTED by the owner about 16:13 UTC (`date -u`): the one-way first-order doublet x the hand, at today's mass (Θ0 = 64).
  * The doublet's first-order potential (matter, matter2, the chiral entries touching matter, gwb) carries the hand as
    one common factor. E1 and the second-order self terms are not scaled, so the echoes are approximate.
  * Tensor: dynamics fingerprint 593753fa..., G 382, rank 4, 27,040 monomials, 17,856 designations.
  * Rank-4 terms (ONE-B OB9): 18,254 degree-3 terms. The 1,528 undesignated ones are the pre-existing OD4 springs; all
    others are designated one-way. 17,120 package terms read Θ, all designated, and E1 reads Θ nowhere.
  * Cost of the coupling (ONE-B OB5, measured): E1 is not scaled and sources from the unscaled hopping
    current. Its dressed-continuity residual therefore grows up to ~475x the hands-ON baseline (L = 4, 200 updates),
    tracking (1 - Θ̄). The map stays exact (bijection, rewind), but E1 is not physically coherent with the Θ-scaled
    doublet (OPEN).
  * Θ0 = 64 is below the 2^8 grain bar (ONE-B OB6). C2 (Θ0 = 256 with the package mass 4916 * 2^22) meets the bar but
    is an option only: a mass change the owner has not approved.
* **ONE v1 (the default)**, `one_system()` = `one_system(couple_doublet=False)`: the block-diagonal version (the package ⊕
  the clock).
  * Fingerprint 77f6d251..., G 382, rank 4, 18,592 monomials, 736 designations (706 + 30).
  * 0 monomials cross the package/cosmic boundary, and the package evolves bit-identically to `default_system()`.
  * No package sector is an exact Θ reader at today's integer grain (ONE-B's verification; NOTES_one.md section 3).
    For the E1-charged pair this holds at any Q while E1 is its photon (rank 5).
  * T1-T4 were pre-registered and run on ONE v1; ONE-A reports PASS.
* **Bangs start new seeds** (owner decision). Each turn of the hand starts a NEW seed, the state at the turn, and no
  bang returns to the seed. Rule3 on one tensor is an exact bijection, so no information is lost. Echo distances are
  data, not the goal. Results (L = 6, J-pure, 1200 updates; ONE v1 and the coupled C1):
  * the rewind across every bang is exact;
  * the turns are at t = 96, 289, 481, 672, 863 and 1054 (C1: 673 and 864 for the fourth and fifth);
  * each new seed adds about 80 kB of new outcome record, the record grows linearly, and all turn states are distinct;
  * C1 data: the package seed distance is 0.038 and 0.037 at the first two bangs, then 0.16-0.52.
* Declarations (NOTES_one.md):
  * the time scale is an input: g_w is set for a target period, so the turn times are checked, not predicted;
  * no-signalling is law-preserved but seed-initiated: it holds in the matched seed sector;
  * the Born weights are seed data.
* No freeze and no hold: light executes the clicks, and only the chosen path produces a click.
* Not in ONE (NOTES_one.md section 7): the zero-time hold, the confirmation gate composed with folding, Pauli copies /
  three families, FIX-C+, and the cosmic matter's coupling to the lapse (OPEN). Route B is reachable with
  `one_system(route_b=True)`, OFF by default; the coupling is not designed for it.

## 7f. Opt-in layers added after the ONE freeze (default OFF)

* Linearised Einstein layer (Study 28; `layers/einstein.py`, `einstein_system(base=None, on=False)`; NOTES_einstein.md). It puts the
  ten metric gears in the integer DeWitt basis and couples them to L0 in the diagonal sector, reciprocally plus a one-way beta read.
  - With it on, gamma = 1 is derived for dust, given the layer's CHOSEN board reader. Board light bending and Shapiro delay come out
    at 2.08-2.16x and 2.02-2.06x Newton, measured with one-way test lights; E1 does not read the metric.
  - The source is not conserved.
  - The full Einstein equations remain impossible at rank 4 (THEOREM walls).
  - Signed: s28/AGREE_EINF.md, copied to full_picture_2026-11-10/records/.
* Clock law CG2 (Study 34; `layers/clockgen.py`, `one_system_clock(law="CG2", theta0_log2=21)`; NOTES_clockgen.md). It adds one
  designated one-way term per node, u[h00] += Theta*F. No package matter gear reads the hand; whether the cosmic block's own
  readers M1/M2 count as matter is an open owner question.
  - Theta0 = 2^21 is CHOSEN (window-fitted, owner-approved), not forced.
  - At L = 6 it holds the uniform lapse to |U| <= 4.1e-3 up to t = 8,900.
  - It is valid only inside CLOCK_VALIDITY (L <= 6); it fails at L = 7 and 8.
  - Not safe as the default.
  - Signed: s34/AGREE_CLK.md, copied to full_picture_2026-11-10/records/.
* The final synthesis is full_picture_2026-11-10/FULL_PICTURE_FINAL.md; the open problems are in FOLLOW_UP_RESEARCH.md.

## 8. Deviations, predictions and no-go theorems

* **E1 (OWNER decision 4: a PREDICTION, not an exception).** E1 gives:
  * light at the right speed;
  * exact charge conservation, also with gravity (e1d);
  * action = reaction exact in the continuum limit and in C∘P-symmetric states.

  For unequal (+,−) packets the board PREDICTS a lattice-scale Newton-III defect:
  * R = −⟨cos E⟩1/⟨cos E⟩2, so δ ≈ 4e-4·(2/w)^1.8 → 0 as O(1/w²). [DERIVED from the package's own EM-D1 force law]
  * Measured consistent within the 1–4 % readout floor at w = 2–4, and ~1e-4 in the cleanest runs; NOT yet
    demonstrated. [NUMERIC, ONE-P2 N14b/N14c]
  * The decisive test ONE-P2 N15 (pre-registered 11:47:31) is NOT DETERMINABLE. [NUMERIC, ONE-P2 N15, §14b]
    * Momentum readout at w = 2: R_p = -0.99847 +- 3.2e-3, i.e. delta = (1.5 +- 3.2)e-3 and |delta| <= 6e-3
      (2 sigma). This is 20-200x tighter than the position readout.
    * The setup's predicted lattice term, delta_pred = 8.6e-4, lies below that floor.
    * Status: consistent, NOT demonstrated. The exponent -1.8 is DERIVED only.
  * Field momentum: OPEN as an exact quantity, because E1 cross terms are designated and give no Noether split.

  Source: s7/ONE-P2_FINDINGS.md §14 and §14b.

  Two verified no-go theorems stand behind the designation:
  * the literal Peierls transpose breaks exact continuity/Gauss (s4 D4: 57,718/58,000 failures);
  * no finite rank closes it.

  The undressed variant ("e1") fails local continuity and the Gauss step with gravity on (162/162).
* **Cone no-go / one cone:**
  * Form C puts L0 on the ONE headroom stencil (Q - 1 ports + 6 on site, c_Q^2 = (Q - 1)/(3Q)), the same as every
    field.
  * The matter's own cone (hop 2^31) is not the field cone: the one-cone gap stays OPEN (manager 10:4x).
* **C8:** an exact centred link lapse read is impossible under B3 (B1-GRAV). Hence the wave lapse is the default.
* **TC.13, ZQ8 (stage 1):** no 4-component integer link carries bit-exact LOCAL Q8 on the 48 labels (NOTES_gauge.md
  theorem). Z[Q8] with 8 gears per link does.
* **L0 EP:**
  * With L0's ports at the odd weight Q no exact universal lapse exists, because the coefficients Q w/(2P) are not
    integers (ONE-P1).
  * Form C at weight Q - 1 is exact.
  * B1-GRAV's site/hop split is EP-correct only in the demodulated reading. In the official click reading it is off by
    0.9-6.0 % (low-w0 bands fastest).
* **Dirac universality: FIXED by R1 (adopted 11:43).**
  * The finding: B1-GRAV's matter lapse put the clock factor on the whole on-site entry (mass + 6 wilson) and the link
    factor on the Wilson hops. The Wilson rest clock therefore read N = 1 - U(1 - 6w/m) = 1 - 0.6875 U, a 31 % EP
    violation, measured 0.993125 at U0 = 0.01.
  * The default now uses `layers/matter_lapse_c.py`, the Wilson term in the difference form. This holds with hands
    OFF; with hands ON the EW composer removes it (section 7b'). Results:
    * N_dirac(demod) = 1 - U0 within 2e-7 on every run;
    * the gap to L0 form C is -5.05e-5, the predicted O(U^2) difference;
    * N_rest = 1 - U is exact for the cos-ratio reading;
    * the own-frame tick ratio is 0.9894 at U = 0.01, matching the prediction within 1.3e-5 (R2).
  * B1-GRAV's split is the contrast mode `v2_matter_split_contrast`.
* **Gravity source of the reciprocal matter lapse C (R1 check, `results/system/gravity_source.json`):**
  * The lapse field's source is b-only: the mass energy plus the link gradient energy (hops and the Wilson gradient).
  * On a uniform state it is exactly the mass energy, -(m/(4P)) b^T W0 b per node. B1-GRAV's split gave
    -((m - 6w)/(4P)) b^T W0 b.
  * Continuity/Noether: the exact conserved quantity is the two-time Noether energy
    E = D(|a|^2 + |b|^2) - 2 a^T H b. Its identity E(t+1) - E(t) = (b' - a).(r - r') holds in 0 of 200 failures (free
    matter, L = 4).
  * The b-only source total is NOT conserved: it oscillates by 1.74 x its mean (split: 1.79). This is the pi/2 carrier's
    doubled frequency.
  * An exactly conserved first-order stress stays OPEN (B1-GRAV).
* **ONE MATTER option (A):** U(6) on colour 3 (x) pair 2. U(6) is larger than the SM, and its breaking is OPEN. There is
  no C-odd hypercharge. EM is J' = 1_3 (x) i sigma_y.
* **c2 (RUN Z, pre-registered).** Setup: ZQ8 with one OD4 spring per simple component, fine links under offset Q - 1,
  10^4 updates, 3 seeds.

  | arm | (1,-1,1) | +++ |
  |---|---|---|
  | A: today's L0 at weight Q, A = 20857 | BOUNDED 3/3 | RUNAWAY at t = 440, 470, 471 |
  | B: form-C L0, A = 2^14 | RUNAWAY at t = 2000, 6330; 1 bounded | RUNAWAY at t = 420, 790, 60 |
  | B2 (exploratory): form-C L0, A = 2^15 | RUNAWAY at 510, 840, 870 | not run |

  * C2-TUNE final: the runaway was a 1:2 parametric resonance of the lam = 4 spring, not form C. Parameters T2 are
    A = 2^14, lam = 2.
  * c2 is exact and bounded on the handed class WITHOUT gravity (T2).
  * WITH gravity it shortens the horizon: about 1825 updates against 2843-3688 for the c2-OFF control. It fails at
    U_mean ~ 0.065 because c2's hop modulation is not lapse-dressed, while L0's is.
  * Re-test after GRAV-FIX A (short, L = 5): no shortening seen at 600 updates (section 9); a long re-test is OPEN.
  * Source: s0/C2TUNE/C2TUNE_FINDINGS.md (C2-TUNE scratchpad).
  * c2 stays OFF in the v2 default (C2_DEFAULT False).
  * Late limit: a ~2e4-update rounding-heating limit, common to both classes (Study 7). Remedy: scale the spring or A
    with the run length.

## 9. Open items

* An exactly conserved first-order stress is open.
  * The uniform-mode drift is O(U^2 t^2) (B1-GRAV).
  * BANG-2: the drift grows as t^2 early, with S2\* and datum 0.
* Gauge amplitude regime: u1 matter at amplitude 2^20 runs away at t = 3. The gauge layers' tested regime is far
  below it.
* HORIZON (after GRAV-FIX A):
  * S2\* is bounded for 12,000 updates (B1-GRAV) and for 2,000 at L = 6 (integrator check).
  * The slow k = 0 growth from the nonlinear mean source reaches U = 1 near t ~ 14,500.
  * These are hands-OFF runs. With hands ON + FIX-i, the L = 6 bang seeds are bounded to 1196-1500 updates (their
    wall budget). Behaviour beyond about 1200 updates is OPEN.
* EP for the doublet with hands ON (the FIX-i debt): the doublet's mass and the doublet half of its transport get no
  lapse factor. "The Higgs sets the clocks" can return only as a NEW LAW (L2(b) + FIX-C+), after long runs (v8-1).
* The uniform (k = 0) lapse mode has no spring, so it accumulates any residual source. With hands ON + FIX-i, U_mean
  drifts slowly (-0.036 at 1196 updates, S2\* 2^16, L = 6). A fix for this drift is OPEN (v8-1: the next task).
* Gravity source: no exact reversor is known for the HYBRID source at today's integers (NOTES_gravity_hybrid.md).
  "Action = reaction" in gravity remains a prediction (v8-2).
* Route B: ONE LIGHT is OPEN; the photon is at most 0.41 c_Q (section 7d).
* ONE: the coupled build (opt-in, REJECTED by the owner) is not an exact Θ reader, because E1 and the second-order fields are not
  scaled. Its echoes are approximate (data, not the goal), and E1 is not physically coherent with the Θ-scaled doublet
  (ONE-B OB5). An exact coupling that includes E1 is impossible at any Q (OB6), and it stays OPEN. Θ0 = 64 is below
  the 2^8 grain bar; C2 meets the bar but needs a mass change the owner has not approved (section 7e).
* c2 (T2) with gravity shortened the horizon before GRAV-FIX A (section 8). It is OFF.
* Re-test after GRAV-FIX A (L = 5, report only):
  * S2\* alone is bit-identical with c2 ON or OFF: S2\* never excites L0, so it cannot test c2.
  * With an L0-exciting weak datum (+ L0 seed a = b = 2^10 v), 600 updates: BOUNDED both ways. U_mean = 0.0130 (ON)
    vs 0.0136 (OFF).
  * At a = b = 2^16 v both run away (t = 5 / 58): outside the weak-field regime.
  * A long re-test is OPEN.
* The gravity source is b-only and not conserved. An exactly conserved first-order stress is OPEN (section 8).
* The frequency-dependent redshift proportional to U w0^2 is a PREDICTION. R-P1/R-P2 delta review is pending.
* The P+ seed is not ported (TODO hook).
* U(6) breaking is OPEN.
* The q-lattice docstring patch for core/tensor.py is drafted, not applied: `patches/core_tensor_qlattice_docstring.patch`.

## 10. Evidence index

* Paths that start with s<N>/ (for example s18/AGREE_STAB.md) are external working records in the study scratchpad,
  not repository files.
* 13 committed results were produced before FIX-i (14:45) and carry pre-FIX-i values (for example 18,623 monomials
  instead of 18,553):
  * `results/system/`: v2_default, v2_ppp, v2_noL0lapse, v2_c2_on, v2_compact, v2_P2p16, v2_od2_variant,
    v2_e1_undressed, v2_W_split_contrast, v2_beta_marginal_contrast, legacy_ppp_off0 and rc2_batch1_checks (`.json`);
  * `results/universality/T6_composed_default.json`.
* FIX-i is their sole cause. Every other suite output reproduces on the push code up to time stamps (REV-VERIFY, Study
  25: s25/REVIEW_VERIFY.md, s25/verify/logs/prefixi_solecause.txt).

| claim | code | evidence |
|---|---|---|
| composition, defaults | `layers/system.py` | `results/system/v2_default.json` (pre-FIX-i, 13:28: 18,623 monomials) |
| X1-X10, 10 modes | `tests/test_system.py` | `results/system/{v2_default, v2_ppp, v2_noL0lapse, v2_W_split_contrast, v2_od2_variant, v2_compact, v2_e1_undressed, v2_P2p16, v2_c2_on, legacy_ppp_off0}.json`, `e1_without_gravity.json` |
| form C | `layers/gravity_l0c.py` | `tests/test_l0c.py` -> `results/system/L0C_clock.json` |
| c2 ZQ8 per component | `layers/c2_zq8.py`, `demos/system/zq8_c2.py` | `results/system/Z_{A,B,B2}_{pmp,ppp}.json` |
| dressed E1 | `layers/em_dressed.py` | X6 in every e1d mode |
| one matter (A) at 2^33 + 1 | `layers/onematter.py` | `results/system/O1-O5_onematter_Q2p33.json` |
| seeds | `prepare/seed.py`, `observe/seed.py` | `tests/test_seed.py` -> `results/system/SEED.json` |
| GRAV-FIX A (detuned beta) | `layers/gravity_beta_fix.py` (B1-GRAV), `layers/system.py` (`beta_form`) | `results/system/horizon_s2star_detuned.json`, `v2_beta_marginal_contrast.json`, NOTES_gravity.md GRAV-FIX |
| R-a free mean | `prepare/gravity_ra.py` (B1-GRAV), `prepare/seed.py` (`ra_free_mean`) | NOTES_gravity.md GRAV-FIX T3 |
| readout labels (follow the tensor labels, RC2 F-R) | `observe/readout.py` | `results/system/rc2_batch1_checks.json` |
| R* with L0's signed relabelling | `observe/seed.py` (`l0_relabelling`, `r_star`), `prepare/seed.py` (`l0_rstar_vector`) | `results/system/SEED.json` (SD6) |
| mirrors with hands ON | `observe/system.py` (`joint_mirror_hands_on`), `observe/seed.py` (`r_star_hands_on`); prepare/chiral.py building blocks | `results/system/v2_*.json` (X5), `SEED.json` (SD7) |
| chirality + electroweak (default ON, decision 5) | `layers/chiral.py` (HAND-M1), `layers/system.py` (`chiral=`) | `results/system/rc2_batch1_checks.json`, NOTES_chiral.md |
| FIX-i graviweak (default, v8-1) | `layers/electroweak.py` (`compose_electroweak`: `gwb_lam_H = gwb_lam_L = 0`) | s18/AGREE_STAB.md (external working record; rows R2, R9-R11, addenda A1, A7), NOTES_system.md (owner decision v8-1 paragraph) |
| HYBRID gravity source (candidate, default OFF; v8-2) | `layers/gravity_hybrid.py`, `prepare/gravity_hybrid.py` | `tests/test_gravity_hybrid.py`, NOTES_gravity_hybrid.md (H2 reversor: FAIL) |
| route B (opt-in, default OFF) | `layers/electroweak_b.py`, `observe/electroweak_b.py` | `tests/test_electroweak_b.py` -> `results/electroweak_b/`, NOTES_electroweak_b.md |
| ONE version (Study 22): ONE v1 = `one_system()` (default); coupled C1 = `couple_doublet=True`, opt-in only (NEW LAW candidate, REJECTED by the owner) | `layers/one.py`, `prepare/one.py`, `observe/one.py`, `demos/one/` | `tests/test_one.py`, NOTES_one.md, s22/AGREE_ONE.md (OB5, OB6, OB9), s22/ONE-A_work/runs/, s30/runs/ (C1 runaway) |
| rank 4 final (rank 5 rejected) | - | s23/AGREE_R5.md (Study 23 joint verdict) |
| opt-in linearised Einstein layer (Study 28, default OFF) | `layers/einstein.py`, `observe/einstein.py`, `demos/einstein/` | `tests/test_einstein.py` (17), NOTES_einstein.md, full_picture_2026-11-10/records/s28_AGREE_EINF.md |
| opt-in clock law CG2 (Study 34, default OFF, L <= 6) | `layers/clockgen.py`, `observe/clockgen.py` | `tests/test_clockgen.py` (11), NOTES_clockgen.md, full_picture_2026-11-10/records/s34_AGREE_CLK.md |
| mass lock check | `demos/system/mass_lock_check.py` | `results/system/mass_lock.json` |
| matter lapse C (R1 default) | `layers/matter_lapse_c.py`, `demos/system/dirac_formc_check.py` | `results/system/DIRAC_C.json`, `L0C_clock.json`, `v2_matter_split_contrast.json` |
| gravity source of lapse C | `demos/system/gravity_source_check.py` | `results/system/gravity_source.json` |
| own-frame ticks (R2) | `observe/readout.py` (`carrier_from_law`, `own_frame_series`, `tick_rate`) | `results/system/L0C_clock.json` |
| pre-registrations, results | - | `NOTES_system.md` |
| stage 1 layers | `layers/{gauge, links, matter, em, em_compact, gravity, gravity_select, gravity_l0, choice, choice_oddq}.py` | NOTES_gauge/em/gravity/choice.md, STAGE1_MANIFEST.md |
