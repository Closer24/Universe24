# E14 — exact two-beam interference of prepared board-filling plane light: dark planes spaced λ/(2 sin θ/2) in clicks

## On the event board
- board: side 8 (the smallest torus that fits p = 8 light), +++ (reference), quiet vacuum (0,0,2); 24 updates (three
  cycles; counts over updates 1–16); r26's p = 8 boards on L = 16 are exact 2×2×2 tilings of these
- prepared at t = 0 (composition.json, one placement of the registered generator plane_light@1): r26's exact light
  a = Σᵢ f(σᵢ·x + 1), b = Σᵢ f(σᵢ·x), r = 2 on all 48 channels, f = (3,2,0,−2,−3,−2,0,2), p = 8; beam A along (1,1,1),
  beam B along (1,−1,−1), (1,1,−1) or (−1,−1,−1) (θ = 109.47°, 70.53°, 180°); runs J109, J70, J180 (both beams) and
  A, B109, B70, B180 (one beam, as overrides); after t = 0 only Rule3 acts; nothing is injected or read back
- [THEOREM r26 T1] u = 3Σᵢ(f(sᵢ+1) + f(sᵢ−1)) is a multiple of 3, so r stays 2 and b_t = Σᵢ f(σᵢ·x − t): the joint
  board is the exact linear superposition A + B − background of two prepared board-filling waves at every update
- [THEOREM r26 T3] f(−m) = f(m), f(m+4) = −f(m): a = b = 0 for ever on the planes m·x ≡ 2 (mod 4), m = (σ_A − σ_B)/2,
  spaced p/|σ_A − σ_B| = λ/(2 sin θ/2), λ = p/√3
- [THEOREM] b = 0 on every channel gives u = 0 and S_t+1 = JR(S_t), JR(a,b,r) = (−b,−a,r): a state property whose only
  click signature is one empty update; the standing wave J180 has one at every t ≡ 2 (mod 4)
- clocks: gears never turn (θ = r/2 = 1); hands jump by the carry u/3 (C0); the beams are gear sets that never connect

## In the clicks (decoder 1.0; the declared detectors through its own correlations over [1, 16])
- every click is C0; the decoder reads every run as one period-8 source with no tracks (record period exactly 8)
- one beam: 576 clicks (12 of 16 updates × 48 channels) at every pixel (4,y,4), (4,4,z); both beams: 0 clicks at the
  predicted dark pixels (Y2 Y6 Z2 Z6 at 109° and 180°; Z2 Z6 at 70°), 576 elsewhere: every count = closed form
- planes m·x = c of the pair's own normal: 0 clicks at c = 2, 6 (period 4: spacing 4/|m| = 2.83, 4.00, 2.31 sites
  = λ/(2 sin θ/2)); no dark plane on the other two normals, nor for one beam alone
- opening the second beam: screen (15 sites) 6336 (109°, 180°) and 7488 (70°) clicks against 8640; board 221,184
  against 294,912. J180: no board click at updates 3, 7, …, 23, 18,432 at every other one; J109 clicks at every update

## Claim
- [THEOREM + SIMULATION] exact two-beam interference of prepared board-filling plane light, read in native clicks:
  zero clicks on the dark planes where each beam alone clicks, spaced λ/(2 sin θ/2) at three crossing angles; at
  p = 8 the native fringe is a step (0 or 12 of 16 updates); the brightness (|q| doubles at antinodes) is in the
  quotients, which decoder v1.0 does not count
- limits: classical linear-field interference of globally prepared beams (never emitted; no slits, paths or sources;
  four diagonal families only). [THEOREM r26 T4, exact light only] exact light keeps every gear at the middle notch,
  so nothing can connect to, record or alter it: a which-path mark, hence its erasure, cannot be shown here.
  [THEOREM r26 NB] no Born-weighted single-event registration, restricted to registration by the first connection
  of a notch-fixed absorber (R10G-61)
- referee: remote fresh-machine referee FRESH6-2 CONFIRMED (report 6, item 2); r10g R10G-84..88 CONFIRMED on these
  boards and R10G-57..59 CONFIRMED on r26's L = 16 boards

Reproduce: python -m research.matter_light_experiments_v1.verify E14_two_beam_interference
