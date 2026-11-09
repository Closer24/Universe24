# E07 — collapse and entanglement candidates in clicks: an approval router and a common-past Z4 Bell test

## On the event board
- board: side 100, coupling +++ (reference), background (0,0,2); after t = 0 only Rule3 acts; native Engine, exact
  inverse at every update.
- prepared at t = 0 (composition.json, registry blocks only): r13's beam-splitter device (guide_net@1: input along +x,
  r04 degree-3 junction at x = 22, arms along +x and +y; phase_gate@2 dark clocks two sites below the arm nodes at path
  length 20 and 28); one unit pulse (1,0,−1) reaching the junction at t = 8; for (b) r12's approval router, one inward
  packet on arm A or B meeting the pulse at the junction; a pulse_train@1 light clock at z = 70 (ticks at t = 4 and 44).
- runs: (b) no approval, approval on A, on B, approval only, device only, clock on/off, four calibration phases; (c)
  settings θ_A, θ_B ∈ Z4 (gate orbit phases) and hidden λ ∈ Z4 (arrival shift), 64 runs. Every run is a control of the
  one composition.
- (b) the two pulses connect at one junction channel (one overflow) and one copy leaves. (c) the two copies share one
  past event (the junction passage), are decoupled on the arms, and each meets only its own gate.

## In the clicks (decoder click_decoder_v1 1.0, official click logs; detectors.json declared before the runs)
- (b) detector probes: no approval (1,1); approval on A (0,1); on B (1,0); the second pair repeats; α = 0 over the
  approval family; calibration open phases 1 and 2; light-clock ticks at 4 and 44, the selected detector's first click
  at 30, the other silent (one approved event at zero click-time); the clock changes no detector click.
- (c) over all 16 setting pairs (derives chsh, e_table, covariant_curve, best_chsh, tlm): E depends only on
  Δ = θ_A − θ_B, E(Δ) = 1, 0, −1, 0, marginals ½; E(Δ) deviates by 0 from both reference curves, cos(πΔ/2) and the
  triangle law 1 − |Δ| (cyclic); Fourier ℓ1 = 1; best CHSH over all 256 Z4 setting quadruples = 2; TLM at (0,1; 0,1) = π.

## Claim
- [SIMULATION] One approval gives exactly one outbound copy and one detector event (α = 0, repeatable). Its frequency
  is the measure of the hidden datum (which arm the approval comes from), not a Born rule.
- [THEOREM + SIMULATION] Clocks with a common past, decoupled afterwards, give a curve that at the four Z4 points
  coincides with both the quantum cosine and the local triangle law, so it does not tell quantum from local. For this
  table the best CHSH over every choice of Z4 settings is 2, the local bound, whatever source produces it; 2√2 needs
  setting differences off the Z4 grid (e.g. 45°), and both gates here have period 4.
- r13 G0 [THEOREM for carry-free gates only, R10E-2]: an autonomous gate whose channels and inputs have quotient 0 at
  every update has a period dividing 4; gates with silent carries or driven by a clicking clock are not covered.
- r12 Theorem 7 [THEOREM, R10E-8]: a phase-covariant ±1 correlation curve on Z_N is quantum-realisable iff
  Σ_k |Ê_k| ≤ 1; this curve has Σ = 1, as the triangle law does.
- referee: r10e R10E-55 CONFIRMED
- limits: prepared media; deterministic hidden-datum ensembles; zero click-time is a statement about the light clock (on
  the board, 22 updates from the junction merge to the detection); this is not quantum entanglement.

Reproduce: python -m research.matter_light_experiments_v1.verify E07_sce_collapse_entanglement
