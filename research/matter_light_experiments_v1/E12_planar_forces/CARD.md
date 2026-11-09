# E12 — contact forces in a planar universe: one seed plane, + and − walls, a dark texture and a clock

## On the event board
- coupling +++ (reference), quiet vacuum (0,0,2); data only: composition.json, one board L = 16 of the registered
  generator all48_planes@1 (whole planes, all 48 channels): + wall (0,0,4) at x = 0 | seed (−1,−1,0) at 3 | clock
  (−1,−1,2) at 7 | dark texture (0,0,0)|(0,0,4) at 10, 11 | + wall at 13
- runs, masks of that board: main (32 updates); walls only (no clock, no texture); two textures (the clock plane
  replaced by a texture at 7, 8); no seed; dark (no seed, no clock); seed alone (12 updates); and the seed alone on
  2L = 32 (compositions/seed_L32.json, 12 updates: the shortest horizon at which v1.0 reads both tracks exactly);
  after t = 0 only Rule3 acts; nothing is injected or read back
- algebra: the planar reduction u(n) = b(n−1) + b(n+1) + 4b(n) is exact; Q = Σp and D = Σxp are conserved and
  nothing acts before a carry (r05; r18 T1, T2): every effect is a contact effect. The seed plane decays at t = 4
  into two gliders (1/2 plane per update) and a dark home mark (0,0,0) at x = 3
- prefix law [EXHAUSTIVE, 452 registered cases]: a glider passes a dark block iff no prefix seen from its side is
  positive (the block moves rigidly 2 planes toward its origin), else it reflects as its J-image (C2 → C1); a + wall
  and the − home mark at distance d confine a glider with period 4d − 2 (here d = 3: 10)
- the clock plane has period 6 (C2 at t ≡ 0, 1, C1 at t ≡ 3, 4 mod 6); a passing glider moves it 1 site toward the
  glider's origin and delays it by 2 updates. The boxed version, which re-bangs every 4d + 4, is E15b

## In the clicks (decoder 1.0 on the declared projection layer r18_line_y0z0_v1)
- the layer: the records with y = z = 0 of each official log, lossless on planar boards (exact y/z translation
  symmetry); on the full planar logs v1.0 reads no exact speeds (R10G-74)
- seed alone: the seed plane decays at t = 4 into two matter tracks at exact −1/2 (origin seed) and +1/2 (emitted),
  window [6, 12]; the free glider clicks only C2; on 2L = 32 the same velocity, exactness, birth origin, time, sites
- walls only: a period-10 source at x = 1 (the left glider between the + wall and the home mark); the right track
  reaches x = 12.0 at t = 20 and is back at 7.5 at t = 32 with 1,008 C1 clicks (label flip at the + wall)
- main: the same period-10 source at x = 1; the clock is a period-6 source at x = 6, window [9, 29], phases 0, 2, 3,
  5; with no seed it is the only source, at x = 7 from t = 1: pulled 1 site toward the seed and 2 updates late
- two textures (D = 4 and 7): the right track leaves the walls-only path only at t = 7, 10 (D = 4) and 13, 16
  (D = 7), and on the way back at 26, 29, 32: the same two-update kink at both; dark: no click

## Claim
- [SIMULATION, native, decoder-read] (r18b, PR-E12 declared 2026-11-09 03:40 UTC): an EM-like sign rule at contact
  (+ wall: reflection with a label flip; texture, − side first: passage with a kink), a confinement candidate between
  opposite signs, and a pull toward the seed (gravity-like candidate) without fall-off over D = 4 and 7
- limits: contact only (T2), no recoil, prepared walls, planar (board-wide) objects only; no equivalence principle
  (clocks move 1, marks 2); no transverse action (r18 T7); the textures' 2-plane shift is not itself decoder-read
- referee: remote fresh-machine referee FRESH6-1 CONFIRMED (report 6, item 1); r10g R10G-74, 76, 77 CONFIRMED

Reproduce: python -m research.matter_light_experiments_v1.verify E12_planar_forces
