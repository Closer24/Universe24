# E10 — prescribed, non-dynamical geometry, not gravity sourced by matter: a Schwarzschild relay lattice in clicks

## On the event board
- coupling +++ (reference), quiet vacuum (0,0,2), side 256, 200 updates; ONE board holding three lattices side by side
  (E at y 0, T at y 85, F at y 170) as a u24-composition-v1 of guide_net@1 (fibres, rings, taps, cavities); control
  "dark" (all packets removed); the lamp is an init file composed from all48_site@1 + guide_net@1 (side 128, 90 updates)
- the geometry is written into the initial remainder landscape: a coarse link of 16 sites carries 16·κ fibre
  nodes (extra nodes as z-bumps); κ_t = 1 (far shell), 3/2 (near shell); E: κ_r = κ_t², T (1911 twin): κ_r = κ_t,
  F: flat. Nothing in the coupling varies (r16: it cannot); no source, no counters, nothing acts after t = 0
- per lattice: tangential and radial ring clocks (16·κ nodes) with r04 taps and exit fibres to O; tangential and
  radial cavities (D = 8·κ, period 2D + 6); a radial probe; four rays (b = 8, 16, 24, 40); route A (through the
  near shell) and route B (around it, 6 flat links); exit fibres 200 nodes (no end reflection within 200 updates)

## In the clicks (click_decoder_v1 1.0, frozen 2026-11-09 01:29 UTC; probes = declared detectors and windows)
- redshift: 24 sources; ring periods E 16,24 (tangential) and 16,36 (radial); T 16,24 and 16,24; F all 16; cavities
  E 22,30 / 22,42, T 22,30 / 22,30, F 22. On the exit fibres, before any end reflection, the received light repeats
  at the same N (first clicks 24, 24+N, 24+2N), so the clocks are compared by light
- α from decoded periods: N_t = 16/24 = 2/3, N_r = 16/36 = 4/9 = N_t² in E, so α = ln N_r / ln N_t = 2; in T,
  N_r = N_t, α = 1. Two-clock criterion H = N_t/N_r = 3/2 = 1/N_t (E) vs 1 (T)
- Shapiro: radial probe first click E 84, T 72, F 64 (+20 vs +8)
- bending: ray first clicks E 186,186,146,130; T 162,162,146,130; F 130 (a tilted arrival profile)
- least click-time route: E: B first (108 vs 116); T and F: A first (92 vs 108; 76 vs 108)
- dark control: 0 clicks (the prescribed landscape is invisible; only light shows it); lamp: click period 2

## Claim
- [THEOREM + SIMULATION] r22 waves 2-3 (pre-registered 02:18 and 02:44 UTC): in a declared relay geometry the decoder
  recovers exactly the designed clock rates and link times; Einstein's α = 2 appears only where radial links carry
  κ_t² nodes, i.e. by declaration. Exact rationals follow from ring lap = node count, cavity 2D + 6 and arrival =
  path length (r04 guide lemma); every number above is a decoded click: 73 checks
- limits: the step-shell rays do not give GR's factor 2 in deflection (that needs a 1/r profile). No free fall:
  [THEOREM FF] no response before contact; [EXHAUSTIVE/catalog] every known response is a contact drift. Cavity
  clocks (period 2D + 6) are not slowed by N (E: 22 → 30 and 22 → 42 against rings 16 → 24 and 16 → 36), so
  universality holds for ring clocks only. On-site clocks do not see the geometry (lamp); no boosts; the lattice is
  the frame. The larger L = 512, three-shell version (κ_t = 1, 5/4, 3/2) passed 60/60 in r22 wave 2 (2.3 min per
  board, so not packaged)
- referee: r10f R10F-7 CONFIRMED

Reproduce: python -m research.matter_light_experiments_v1.verify E10_prescribed_schwarzschild_lattice
