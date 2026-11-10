# E07b — superposition and interference candidates in clicks: two exact C0 fronts on one screen

## On the event board
- board: side 6, coupling +++ (reference), background (0,0,2); native Engine, exact inverse at every update; horizon 6
  (one front period).
- prepared at t = 0 (composition.json, registry blocks only): two exact (111)-type C0 fronts written as all48_site@1
  placements (every front site is all 48 channels at one triple): A along x+y+z (= the published block
  exact_front_111_box), B along x+y−z with amplitude −M (M = 1000); a same-sign partner; for part (d) an r08 dark clock
  (all-48 (−1,−1,0)) at (3,3,3).
- runs: a_A, a_B, a_AB, a_ABplus, d_both (A + clock), d_clock; every run is a control of the one composition.
- [THEOREM] r12 Theorem 13 (R10E-37): a rounding-free field X (it never changes a remainder, and its remainders are the
  landscape's) superposes exactly with any Y: the joint state is X + Y − background at every update, so Y's history,
  any record included, does not depend on X. Here a_AB and a_ABplus are A + B − background and d_both is front + clock
  − background at every update (also checked on the complete states): the front writes no record in the clock.

## In the clicks (decoder click_decoder_v1 1.0; detectors = the six screen planes z and the clock site)
- A alone and B alone: 6,912 clicks on every plane. A + B (opposite signs): 0, 6912, 6912, 0, 6912, 6912, i.e. dark
  planes z = 0 and 3 (spacing L/2 = 2π/|k₁ − k₂|) and half of A + B elsewhere: P₁₂ ≠ P₁ + P₂.
- derive plane_spectrum of the A + B screen: period 3 = L/2, Fourier magnitudes 4608, 0, 2304, 0, 2304, 0.
- same-sign partner: exactly A's native counts on every plane.
- clock site: 0 clicks with the clock alone; with the front present, exactly the front's own clicks (192).

## Claim
- [THEOREM + SIMULATION] These states superpose exactly (above), and clicks are the threshold readout of the added
  carries, so the native record interferes on overlaps (cancelled, merged or silent coincidences). For these C0
  fronts the joint counts never exceed P₁ + P₂. That is not general: a silent carry in one part beside a dark change
  in the other can make a click in the sum where neither part clicks (R10E-9). Fringe positions and spacing are
  exact wave kinematics.
- [THEOREM + SIMULATION] A rounding-free field never connects, so it writes no record in a detector (Theorem 13). With
  r12's Theorem 12 [THEOREM for unit packets on an extreme-notch guide, R10E-37: two such passages at one guide channel
  in one update always overflow, so their click records either add or the boards connect], this is complementarity in
  an all-or-nothing form.
- referee: r10e R10E-56 CONFIRMED
- limits: classical linear waves (q is a field amplitude, not a probability amplitude); no Born-weighted single events;
  a periodic box of side 6. Not read here: the carry layer (silent-carry ratio 0.75 same-sign against 0.5 opposite-sign
  at partial overlap) and Σq², which need decoder layers that do not exist yet; Σq² = Σq_A² + Σq_B² ± 2Σq_A q_B is the
  identity (q_A + q_B)² for exactly additive q (R10E-38), not an independent test.

Reproduce: python -m research.matter_light_experiments_v1.verify E07b_sce_superposition_interference
