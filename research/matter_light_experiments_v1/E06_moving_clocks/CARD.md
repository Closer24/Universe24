# E06 — Moving clocks: Einstein synchronisation of two co-moving glider clocks gives δ = (3/8)(D + 24)

## On the event board
- board: side 640, coupling (−,+,+) (reference), quiet vacuum (0,0,2), r06 line conventions
- prepared at t = 0: a rail (matter line, label 41 along y at x = 40) carrying two gliders A and B moving −y at
  v = 1/3, a distance D apart (co-moving clocks: each emits a light packet at every rail junction); three light
  rungs (label 1 along x) and a light collector line at x = 52 (h = 12) that copies a packet from rung to rung
- runs: D = 40, 64, 80 with both gliders; controls for D = 64 with A alone and with B alone; 210 to 300 updates
- after t = 0 only Rule3 acts; nothing is injected or read back

## In the clicks (click_decoder_v1 1.0, frozen 2026-11-09 01:29 UTC; official click logs only)
- detectors (detectors.json = r14's declaration): a glider passage at a rung = first rail click at the junction
  site (40, y, 3), channel 41, + 6; a light arrival = first click at (44, y, 4), channel 1, in a declared window
- decoded rail first clicks [A at rung j, B at rung m, A at rung m'] = [20, 116, 164], [20, 152, 218] and
  [20, 176, 254] for D = 40, 64, 80; so t1 = 26, t_B = 122 / 158 / 182, t2 = 170 / 224 / 260
- the light reaches rung m at t_B − 1 and rung m' at t2 − 1 (121/169, 157/223, 181/259): both receptions are
  click coincidences; controls: A alone, the light reaches rung m at 153 (4 earlier) and no B passage; B alone, the
  reply reaches rung m' at 219 (4 earlier) and no A passage

## Claim
- [SIMULATION] native, r14 (pre-registered 01:26 and 01:29): Einstein's rule applied by the moving pair gives
  δ = t_B − (t1 + t2)/2 = 24, 33, 39 for D = 40, 64, 80 (27 for D = 48 in the record), δ = (3/8)(D + 24) exactly.
  The slope 3/8 = v/(1 − v²) is the offset that Einstein's rule gives for clocks moving through a medium at rest
  (the Lorentz local-time form); the intercept 9 comes from the light's detour to the collector. The co-moving
  pair's Einstein rule does not reproduce the board's simultaneity; the board keeps its lattice frame.
- The lattice is a preferred frame: with three such modules the transitivity defect is 24 + 24 − 39 = 9 updates,
  not 0 (r14 E3, record only). The gliders are unchanged by the exchange (r14: joint rail clicks = union of the
  single runs).
- referee: r10e R10E-54 CONFIRMED
- limits: prepared rail, rungs and collector; one speed (v = 1/3); r14's transverse light clock (round trips 39 / 59
  against R0/(1−v) = 38 / 58.5) and D = 48 stay in the program record

Reproduce: python -m research.matter_light_experiments_v1.verify E06_moving_clocks
