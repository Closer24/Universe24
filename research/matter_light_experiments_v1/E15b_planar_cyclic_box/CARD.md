# E15b — a cyclic planar box: the seed plane between two + planes re-bangs exactly every 4d + 4 = 16 updates

## On the event board
- coupling +++ (reference); quiet vacuum (0,0,2); compositions/*.json: r18b's box of registered all48_planes@1
  planes, the seed plane (−1,−1,0) at x = 3 between two + planes (0,0,4) at x = 0 and 6 (d = 3); L = 8 and 2L = 16
  (plane-wide, board-spanning objects; the L = 16 board is the initial state of r18b's own box run)
- [THEOREM] with F⁻¹ = JR∘F∘JR, JR(a, b, r) = (−b, −a, r), the box history is JR-symmetric about two half-integer
  times, −3/2 (the bang) and 2d + ½ (both gliders reflected at once), so 2(2d + ½ + 3/2) = 4d + 4 is a period (r18b);
  4d + 4 is the minimal period, numerically for d = 2..20 on the ring; the proof gives a period
- runs: L over 2 cycles (32 updates), 2L over 1 cycle (16 updates; the 2L planar board is 4× the work); both end
  exactly in their initial state (equal SHA-256); after t = 0 only Rule3 acts; nothing is injected or read back

## In the clicks (the released layer log_symmetry_v1 of decoder 1.0)
- 2 byte-identical cycles of 16 updates, 110,592 records each (L = 8)
- each cycle mirrored about the moment 2d + ½ = 6.5 (records at t paired with 14 − t, −k mod 3, −q): 13/13 updates,
  update 7 silent; the same on 2L, with 4× the records (442,368: the same record on every plane site)
- the moment read from the 2L log alone is 6.5, unique

## Claim
- [THEOREM + SIMULATION] a cyclic planar box: the gliders born at the seed plane reflect at the + walls (label
  C2 → C1), come back, merge into the seed at its dark home mark and re-bang, exactly, cycle after cycle
- referee: remote fresh-machine referee, report 6 (05:07 UTC), FRESH6-1 CONFIRMED; r10g R10G-74..77 CONFIRMED
- limits: contact only, prepared walls, planar objects; no decoder-1.0 tracks (the full planar log has 27,648 records
  per update, and the plain verifier cannot read exact speeds there); the 2L run is one cycle

Reproduce: python -m research.matter_light_experiments_v1.verify E15b_planar_cyclic_box
