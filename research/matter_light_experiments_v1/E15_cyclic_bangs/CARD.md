# E15 — exactly periodic bang candidates: two time-symmetric moments per cycle (light only; created matter; a 720° spin ring)

## On the event board
- coupling (−,+,+) (reference); quiet vacuum (0,0,2); compositions/*.json of registered blocks, bare-ended segments:
  - C1: a 41-node light segment with a 5-cell JR seed at its middle (L = 64 and 2L = 128)
  - C2: the JR seed at one bare end of a 74-node light segment, crossed 36 sites away at a class-0 junction by a
    27-node matter segment (L = 256 and 2L = 512)
  - C3a: C2 plus a 78-node counter-circulating holonomy-z ring carrying two unit packets, meshed with T = 82
- [THEOREM] JR∘F∘JR = F⁻¹ with JR(a, b, r) = (−b, −a, r); two moments τ₁ < τ₂ (states with a = −b everywhere) force
  X(t + 2(τ₂ − τ₁)) = X(t): moments at 24ℤ (C1) and 82ℤ (C2, C3a), periods 48 and 164 (r36)
- each seed S is JR-fixed: C1 and C2 compose it directly (dark network plus literal moment patches); C3a composes the
  outgoing target JR(incoming) and rewinds it 11 exact steps; every prepared state equals the source's init file
- runs: C1 and C2 over 6 and 4 cycles on L and 2L; their expansion (P/2 updates from S) and contraction (S rewound P/2,
  the turnaround, then P/2); controls: C1 dark, one packet, asymmetric seed; C2 dark, no matter segment;
  C3a over 4 cycles on L and 2L; each main run ends exactly in its start state (same SHA-256); nothing acts after t = 0

## In the clicks (decoder 1.0; periods and mirrors: its released layer log_symmetry_v1)
- C1: ONE source of period 48 on the 41 sites (the same on 2L); expansion: two light tracks at exact ∓1 leave the seed;
  contraction: two at exact ±1 converge on it; controls: dark 0 clicks, one packet period 88, asymmetric seed 96
- C2: one source of period 164 on 101 sites; expansion: light at exact +1 from the seed, the creation burst at the
  junction at 43, a created light track at exact −1 and two created matter tracks at exact (0, ∓1/3, 0) born at 50;
  contraction: the matter tracks converge on the junction at exact 1/3, the light runs back into the seed; controls:
  dark 0 clicks, no matter segment period 154; 2L: the same source; created = True holds in the expansion halves only
- C3a: two sources of period 164, the network (101 sites) and the ring (78 sites), whose channel-free period 82 is the
  decoder's 720° signature; 2L: the same sources
- log_symmetry_v1: byte-identical cycles (C1 6 × 316 records, C2 4 × 1,372, C3a 4 × 2,612, also on 2L); each
  contraction the mirror of its expansion (48/48 and 164/164 updates; C1 silent at 1, 24, 25, 48); whole logs mirrored
  about 144 (C1) and 328 (C2), 0 unpaired; the asymmetric seed is 96- but not 48-periodic; the C3a ring's records 82
  updates later are their C-image (g → z·g) on 82/82 updates, never a plain repeat

## Claim
- [THEOREM + SIMULATION] a JR-fixed seed in prepared bare-ended segments bangs, expands, turns around at a synchronised
  mirror (every mover at a bare-end midpoint or head-on with its own time reverse) and contracts into itself, cycle
  after cycle, with no information lost; created matter (C2) and the lit ring (C3a) are un-created and re-created
- referee: remote fresh-machine referee FRESH4-B1..B4 and addendum CONFIRMED (C1, C2); r10h R10H-29..31 CONFIRMED (C3a)
- limits: prepared segments with bare-end mirrors, not a uniform background; no gravity station or atoms inside a cycle;
  v1.0's registered failures stay (a non-exact track over a whole cycle; C2's two forward packets not separated; the
  creation burst read as a non-exact front); the planar cyclic box needs +++ and is E15b

Reproduce: python -m research.matter_light_experiments_v1.verify E15_cyclic_bangs
