# NOTES_chiral — CHIRAL-BUILDER (HAND-M1): the Γ5·V weak SU(2) block (written as a DECLARED CANDIDATE, DEFAULT OFF; now ON in the package default)

All stamps `date -u`. NEW FILES ONLY: layers/chiral.py, observe/chiral.py, prepare/chiral.py, tests/test_chiral.py,
demos/chiral/, results/chiral/, this file. No existing package file, core/ or universe24/ is modified; no git.
Source of the design: s7/AGREE_H.md (twin-signed HAND-M1 11:24:18 / HAND-M2 11:25:40 UTC; addenda 11:27, confirmed
11:29:53), rows E1–E7 and joint recommendations 1–2; prototype s7/HAND-M1_work/h3_chiral_board.py, h12, h13.
OWNER decision 5 status: CONDITIONAL (manager 11:58). layers/chiral.CHIRAL_DEFAULT_ON = False.
STATUS UPDATE (DOC-UPDATER, Tue Nov 10 15:41 UTC 2026, doc only): OWNER decision 5 CLOSED at 13:09 UTC, hands ON.
- Since RC2 batch 3 (13:17 UTC), `layers.system.default_system()` composes this block by default (`chiral=True`,
  together with `electroweak=True`, through `compose_electroweak`).
- The electroweak completion's graviweak block is at FIX-i (owner decision v8-1, 14:37 UTC; NOTES_electroweak.md).
- The module constant `CHIRAL_DEFAULT_ON = False` is unchanged. It is only the default of `compose_with_default(on=...)`,
  which the package default calls with `on=True`.
- Current defaults: README_v1_draft.md sections 0, 7b, 7b' and 7c. The text below is the 12:0x record.

## Design (written Tue Nov 10 12:01:28 UTC 2026, before any acceptance run)
- Doublet: the default "matter" (16-channel pair) + partner "matter2" (build_matter, same hop/wilson/mass).
- Weak links "wsu2": B1-GAUGE su2 link block (default_regime at Q = 2^33 + 1: A = 2^16, kappa_P = 256, c_P = 0,
  beta = 6Q − 2^33, OD4 spring lam = 4, 2-path gears) WITHOUT its psi gears.
- Coupling "chiral": Higgs quaternion H (4 audit gears/node, vev v = 2^16, OD4 spring lam_H = 4) and the deviation terms
  of: transport (kappa/2) b'ᵀ P_d ρ(conj W) Π_W b (kappa = hop/A = 2^15), Yukawa φ-part (ytot = y + 3w, y = mass/(2v) =
  4915·2^5, w = wilson/v = 2^14), Wilson–Yukawa φ-part; Π_W = 1 − Γ5V (package basis), t = {ε⊗1, σx⊗J′, σz⊗J′}.
- v2-default parameters: Q = 2^33 + 1, hop 2^31, wilson 2^30, mass 4915·2^22; vacuum (0, 0, 3Q − 1) for every gear.
- compose_with_default(system, on=False) is the switch; with on=True it appends (matter2, wsu2, chiral) and, for matter
  lapse "C", the partner's lapse/beta reads (matter_lapse_c builders) so both doublet members gravitate alike.

## PRE-REGISTRATION (Tue Nov 10 12:01:28 UTC 2026; written BEFORE the acceptance runs; tests/test_chiral.py implements them)
Systems: ALONE = compose(matter, matter2, wsu2, chiral); COMPOSED = layers.system.default_system() (v2 default) passed
through compose_with_default(on=True). Lattice L = 3 unless stated. Exact = bit for bit (Python ints where needed).
- CH1 algebra: check_chiral_algebra() all True.
- CH2 tensor: check_reciprocity(ALONE) ok with 0 designated monomials; rank ≤ 4 and every degree-3 (rank-4) monomial is an
  OD4-spring monomial (targets only wsu2 link/2-path gears or chiral.H gears, factors all in the same gear family);
  compose() succeeds (B3 locality enforced); census reported.
- CH2b COMPOSED: compose() of the composed blocks succeeds; designated monomials = exactly the default's own designations
  (the chiral blocks add none).
- CH3 vacuum: ALONE vacuum fixed for 20 steps; COMPOSED vacuum fixed for 5 steps and equal on the default gears to the
  default system's vacuum run. One-step identity: for random matter states with W = φ = 0 the matter rows of the ALONE
  inputs equal those of compose(matter, matter2) (= build_matter's free Wilson–Dirac) exactly. COMPOSED one-step identity:
  random default state + chiral gears at vacuum -> after ONE step the default gears equal the default system's step.
  Couplings-off control (A big, kappa → 0 not available) replaced by the one-step identity above.
- CH4 rewind: ALONE random state (moderate amplitudes), T = 6: rewind exact; COMPOSED random state T = 3: rewind exact.
- CH5 Noether/Gauss (ALONE): 3 local generators × all nodes × T = 6 updates: 0 failures (matter t_a Π_W/2 ×2, Higgs
  left mult, links/2-paths left on leaving, minus right on arriving). Non-triviality: matter-only charge changes.
- CH6 discrete symmetries (ALONE, T = 4–6): R* (inversion∘W0J′K∘Mp + conj links/2-paths) reversor: PASS (involution);
  T_phys = CK∘Mp: PASS with central Z = parity-preserving negation of matter (Kramers); board K∘M (J′K∘Mp): FAIL
  (expected); CP forward (inversion∘C·W0): EXACT; P forward (inversion∘W0) and C forward: BROKEN (expected).
- CH7 J-pure seed (prepare/chiral.py, h13 port) on the matter pair: exactly R*-fixed (a = G·b(−x)); J− fraction ≤ 1e−5
  at A = 2^10 and decreasing ∝ 1/A² (ratio ≥ 100 between A = 2^10 and 2^14); N_J ≠ 0; legal for ALONE (no constraint
  gears); for COMPOSED (E1 Gauss) legality needs prepared fields: reported, not claimed.
- CH8 int64 headroom: ALONE vacuum 20 steps and random-state runs report Engine.stats (int64 vs pyint steps); report
  the max |K + r| bound margin.
- CH9 matter-lapse independence: chiral_blocks do not reference any lapse gear (static check); COMPOSED builds with
  matter_lapse "C" and "split" (compose succeeds; partner lapse only for "C", stated).
Expected FAILS (declared, not bugs): local t1,t2 Gauss in COMPOSED (E1 couples only "matter": charged W, no hypercharge);
local SU(2) at O(U) in COMPOSED (lapse dresses the bare mass entry); W mass (no Higgs kinetic term in this candidate).

## RESULTS (written Tue Nov 10 12:08:03 UTC 2026; runs 12:04:40–12:07:42 UTC; FINAL SUITE on the final code 12:07:39–12:07:42: 10 tests OK, 2.6 s)
| test | result | file |
|---|---|---|
| CH1 algebra | all True (Γ5 = −PxPyPz; t_a quaternion units, antisymmetric, commute with P_d, W0, J, J′, Γ5, V; Π_W² = 2Π_W; W0Π_W = Π_SW0); CHIRAL_DEFAULT_ON = False | CH1_algebra.json |
| CH2 tensor (ALONE) | reciprocity OK, 0 designated; rank 4 with 64 rank-4 monomials, ALL OD4 springs (wsu2 link spring + Higgs spring); b-only; G = 72, 8084 monomials (404 node / 7680 link: B3) | CH2_tensor.json |
| CH2b COMPOSED | compose OK; G 319 → 375 (+matter2 16, wsu2 36, chiral 4); designations 1202 → 1698: the +496 are exactly mbeta2 (the partner's β = 1 one-way read, same count and type as the default's own mbeta = 496); matter2, wsu2, chiral, mlapse2 add 0 | CH2b_composed.json |
| CH3 vacuum | ALONE vacuum fixed 20/20; ALONE matter inputs at W = φ = 0 == build_matter's free Wilson–Dirac pair (3 random states, amplitude 2^20): bit for bit; COMPOSED vacuum fixed 5/5 and equal to the v2 default's vacuum; COMPOSED one-step identity on all default gears (random default state, chiral gears at vacuum): TRUE | CH3_vacuum.json |
| CH4 rewind | ALONE T = 6 exact; COMPOSED T = 2 exact; int64 only | CH4_rewind.json |
| CH5 Noether/Gauss (ALONE) | 0 failures / 486 checks (3 generators × 27 nodes × 6 updates); matter-only charge changes up to 2.4e15 (non-trivial) | CH5_noether.json |
| CH6 discrete (ALONE, n = 4, 2 random states) | R* reversor identity 2/2; T_phys = CK∘Mp central (Kramers X²) 2/2; board K∘M (J′K∘Mp) FAILS 2/2 (expected); forward CP EXACT, P BROKEN, C BROKEN | CH6_discrete.json |
| CH7 J-pure seed (L = 6) | exactly R*-fixed (matter and the FULL state, via the package R* map); J− fraction 1.34e−6 (A = 2^10), 5.3e−9 (2^14), ratio 251 ≈ 2^8; N_J −7.0e18 / −1.8e21 (≠ 0), conserved to 1e−5 over 3 updates. NOTE: with the chiral couplings active the FREE-pair J− measure rises to 4.8e−6 (2^10) and 6.0e−4 (2^14) after 3 updates (Higgs back-reaction; see WINDOW) | CH7_jpure_seed.json |
| CH8 int64 | ALONE vacuum 20 + random 10 steps: 30 int64 steps, 0 pyint; max state value 76 | CH8_int64.json |
| CH9 lapse independence | chiral blocks read no lapse/metric/β gear; COMPOSED builds with matter lapse "C" (partner lapse mlapse2 + mbeta2 added) and "split" (partner NOT lapsed: integrator item) | CH9_lapse_independence.json |
| DEMO (L = 6) | (a) J+ readout: J-pure seed (A = 2^12, J− 8.6e−8) W_J > 0 at 6/6 updates; its exact time mirror (Mp) W_J < 0 at 6/6 (exact negatives); N_J ∓1.12e20 conserved to 5e−5. (b) clicks: CP-image run 60,237 official clicks, 0 unpaired vs the CP-mapped original record; P-image run 104,381 unpaired: P broken, CP exact, click for click, on the FULL block | DEMO_summary.json |
| WINDOW | one-update kick of a random matter field of amplitude 2^8/2^10/2^12/2^14 per channel: max\|φ\|/v = 3e−5 / 7.6e−4 / 8.5e−3 / 0.17; max\|W\|/A = 0 / 6e−5 / 8.5e−4 / 1.9e−2. Weak-coupling window of the candidate: matter amplitude ≲ 2^12 per channel at v = 2^16 (Higgs back-reaction ∝ (b/2^17)²) | WINDOW_higgs_link_kick.json |
Expected/declared (not bugs): COMPOSED local t1, t2 Gauss broken by E1 (E1 couples only "matter"; charged W; hypercharge = integrator/owner);
local SU(2) broken at O(U) by the matter lapse on the BARE mass entry (graviweak = Study 9); no Higgs kinetic term (W has no
Higgs-mechanism mass: short range OPEN); heavy mirror doublers and the J− mirror world (AGREE_H E7). Not run here: long
runs, the COMPOSED Noether residual measurement, E1 legality of the seed in the COMPOSED system.

## THE SWITCH (one line for the integrator; layers/system.py NOT edited)
In layers/system.default_system add a keyword `chiral: bool = False` and, just before `return System(Q, tuple(blocks), info)`:
`if chiral: from .chiral import compose_with_default; return compose_with_default(System(Q, tuple(blocks), info), on=True)`
(DEFAULT OFF when written: layers/chiral.CHIRAL_DEFAULT_ON = False. Since 13:17 UTC `default_system()` has
`chiral=True` by default (owner decision 5; FIX-i since v8-1): see README_v1_draft.md section 7b.)

## FILES (sha256, Tue Nov 10 12:08:03 UTC 2026)
| file | sha256 |
|---|---|
| layers/chiral.py | 9bd2da62a16837685b56cb6b2f0ded791e53b9f3f3cea6487ee71d5e8f03fdcb |
| observe/chiral.py | 3efa45c3be9e2957d66520d954e1f9fc6ba32c6aa2235b65a50e9423f35f8d0d |
| prepare/chiral.py | 9edcc6417b717414373eae784b652b2fd84c90aadf4c3c08a4338d6caabba3f9 |
| tests/test_chiral.py | c078cbf019bdfd9583e76af6598aea1035e1d0c6d8dae345b48923172f276eaa |
| demos/chiral/demo_summary.py | 85e269da998728aac7ea2d4f9154043ebd0d83ddd05b26793fe51ddcabaa1dbb |
| demos/chiral/__init__.py | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| results/chiral/CH1_algebra.json | 269d99b9c20e86ab1dc6398be66763b000b6b7687c9b7af3a17055eb22920326 |
| results/chiral/CH2_tensor.json | fb7425370ecc1ffcd9e1d2131e3b5a0e63fac0514b72bc928c7b189169640641 |
| results/chiral/CH2b_composed.json | 371eb9e481a818809edf3e7aff6174ec068028fabd4eec600b4f61655e9e2d53 |
| results/chiral/CH3_vacuum.json | 2a470236f996b473c3ac9811f09c123796119c6f89c6c4c625ca287a6e0e7bb0 |
| results/chiral/CH4_rewind.json | b8968310feb27fdab20355261a135487e62b90a13e441d57e3f4ab6a8c2b8014 |
| results/chiral/CH5_noether.json | e9e9150575743d0a3e8a3334668b5a43088e0188b6f897eeeed3a3dbd1855034 |
| results/chiral/CH6_discrete.json | 93c2e65e587b0d6dbd563e0c3728b6d5ee9bbf3340ccc26ba81e27583007835d |
| results/chiral/CH7_jpure_seed.json | cdd7c8a4ed3811eee5c9a41e9ae5ee9a6492dd39f34241d1ce1796c5910af89b |
| results/chiral/CH8_int64.json | a74a7b4e713df7b316b9382ebe8f034ccecaeddf8721120bcb46ca6ee8e8499e |
| results/chiral/CH9_lapse_independence.json | 72888260691de121269250f74082dad32bd46ef6610e9bce5606c63880bd22d6 |
| results/chiral/DEMO_summary.json | a801592fb185679d08d23bb0fdfb513a1e9d43fa355c2ff7b10df3fa1ffbbd74 |
| results/chiral/WINDOW_higgs_link_kick.json | 0b588840ed9d1f6200c7cdce3d831b5f65133fd0071eec5abe5f7a6b5fa9cdb5 |
Package files modified: NONE (new files only); core/ and universe24/ untouched; no git.
