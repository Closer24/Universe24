# E18 — C3c, a cyclic universe candidate (period 320): created light, created matter at exact ∓1/3, a 720° spin ring, a ring clock at N = 3/5 and twin cavity atom candidates

## On the event board
- board: L = 256 and 2L = 512, 960 updates (3 cycles); coupling (−,+,+) (reference); quiet vacuum (0,0,2); one
  composition per side of registered blocks: the zero-counter hardware of six parts (the C2′ light and matter
  segments, the spin box loop, the lamp ring with its tap fibre, the ring clock, the free line, and the twin-cavity
  module: data line with doors, two ℓ = 8 cavities, escort arms) plus literal moment patches with 8 counter cells
- [THEOREM] JR∘F∘JR = F⁻¹ with JR(a, b, r) = (−b, −a, r): the seed is JR-fixed and the turnaround at 160 is a second
  moment, so the history has period 320 (r36, r36b); the composed seed equals r36b's init file on L and 2L
- runs: C3c over 3 cycles on L and 2L; the expansion (160 updates) and contraction (the seed rewound 160, the
  turnaround, then 160); the atom module alone (AT, 3 cycles) with controls K5 (no escorts) and K6 (right in-arm one
  node longer); the ring-clock calibration (one packet, counter pair); nothing acts after t = 0

## In the clicks (decoder 1.0 and its released layer log_symmetry_v1, official click logs)
- twin cavity atom candidates: two created period-20 sources of 7 sites, born at 22, both over [23, 298]: they form
  after each bang and un-form before the next; the same in AT alone
- the other parts: the network (period 160), the ring clock (20, 12 sites; 12 for one free packet, so N = 12/20 = 3/5),
  the lamp (32) and the spin ring (period 64 on 28 sites, channel-free 32: the 720° signature)
- expansion: created light at exact (−1, 0, 0) from 88 and the created glider pair at exact (0, ∓1/3, 0), born at 89;
  contraction: both atoms present over [1, 138] and the matter tracks converging at exact 1/3
- log_symmetry_v1: 3 byte-identical cycles of 18,244 records on L and 2L (AT: 3 × 4,140); the mirror about 160 on
  320/320 updates; the whole log mirrored about 480, 0 unpaired; the spin ring's C-image after 32 updates on 288/288
- controls: K5 gives only a period-44 antechamber bounce (no atoms); K6 gives no source; 2L: the same readouts and
  54,732 records

## Claim
- [THEOREM + SIMULATION] one exactly periodic universe candidate holds created light, created matter (exact ∓1/3), a
  720° spin ring, a ring clock slowed to N = 3/5 and twin cavity atom candidates formed after each bang from the
  bang's packet pair, in prepared zero-counter cavities, with prepared escorts (wall seeds that carry counters at t = 0)
- the ring clock (slowed by its counter packet, 12 → 20) is the clock of r36b's matched α_in = 1 instrument pair
  (UPDATE 21); its probe (3/5 against the stream on the tap fibre) is read on a difference layer that this package
  does not compute, so α_in = 1 is not claimed here (FRESH 8 confirmed it on the stations P53..P11)
- referee: remote fresh-machine referee, report 8 (05:22 UTC), FRESH8 CONFIRMED in every listed claim; K6 PARTLY:
  outcome confirmed (right cavity never filled, decoder reports no source); the explanation is refuted, since the left
  atom is byte-identical to the main run; why v1.0 then reports no source is unexplained
- limits: prepared segments, rings and cavities, not a uniform background; W4: the expansion-phase decode reports one
  twin only, a track-linking tie-break of v1.0, not a physical asymmetry (FRESH 8); no forces signatures (the variant
  cycle C4 holds them); v1.0 keeps one periodic run per site

Reproduce: python -m research.matter_light_experiments_v1.verify E18_cyclic_universe_c3c
