# E01 — Locally created atom candidates (D1) and twin atom candidates in exact phase

## On the event board
- board: (−,+,+) (reference), quiet vacuum (0,0,2); D1 on L = 100 and 2L = 200; twins on L = 160 and 2L = 320
- prepared at t = 0 (`composition.json`, registered blocks): matter lines A0 (x = 0) and A1 (x = 13); light lines
  B0 (y = 0, gauge phase 1) and B1 (y = 12, phase 0), so the junctions (0,0) and (13,12) are class 2 and (13,0) is
  class 0; two silent cores (−1,0,0) at x = 10 and 18 on B1 (d = 8); one SLOW seed glider on A0 moving −y.
  Twins: plus a light-line segment at y = −q2 (x = 3..150, phase 0) with two cores at x = 10 and 18
- runs: D1 main L100, size check L200, controls no seed / no cores / B0 at phase 0 (masks of the composition);
  twins q2 = 12 and q2 = 8 on L160 and L320 and the twin controls no seed / no lower cores, as published blocks
  (appended to research/matter_light_blocks_v1 at push time; verify after that append); horizons 140 to 260
- after t = 0 only Rule3 acts; nothing is injected or read back

## In the clicks (click_decoder_v1 1.0, frozen 2026-11-09 01:29 UTC; official click logs only)
- D1: one periodic source, period 20, created (born at t = 68 at (13,12,4), more than 4 sites from the seed);
  exact click-front speeds 1 and 1/3; the same birth update and sites on L = 100 and 2L = 200
- D1 controls: no seed, 0 clicks; no cores, no periodic source; B0 at phase 0, no periodic source
- twins (q2 = 12): two periodic sources of period 20, both born at t = 68, clicking in the same 16 phases of the
  period; the same birth on L = 160 and 2L = 320; controls: no seed, 0 clicks; no lower cores, one source
- twins (q2 = 8): two period-20 sources born at 56 and 68, 12 = 3(12 − q2) updates apart
- the decoder classes each source as a lamp (a periodic source that emits), not as a composite

## Claim
- [SIMULATION] One seed glider's light creates a glider pair (t = 29, 13 sites away); a created glider leaves a
  packet bound in a prepared trap: a created period-20 (= 2d+4) source, born at the same update on L and 2L
  (local, not torus-born). With a second trap on a segment, the pair's two members make two period-20 sources
  born at the same update and clicking in exact phase (q2 = 12, selected post hoc by equal birth times).
- The first declared hit, q2 = 8, gives births 12 updates apart (= 3(12 − q2), the created gliders' travel-time
  difference at speed 1/3).
- referee: r10e R10E-52 CONFIRMED
- limits: prepared lines, junctions and cores (structured vacuum); immobile; the atoms' end is set by the board
  (about L − 39 on L = 100); comparing the twins by light failed (r11: 0 complete Einstein triples in 900 trials)

Reproduce: python -m research.matter_light_experiments_v1.verify E01_local_atom_twins
