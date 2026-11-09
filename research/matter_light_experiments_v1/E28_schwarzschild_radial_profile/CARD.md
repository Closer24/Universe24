# E28 — The radial static profile of a PRESCRIBED Schwarzschild relay tree read in clicks: ring clocks tick their node counts and every one-way light time equals its node count (GS-2b, M = 64)

## On the event board
- coupling +++, vacuum (0,0,2), L = 1024, T = 4334; GS2b_S, M = 64: seven ring clocks and ONE relay tree of fibre light,
  a spoke with an A-pulse (1,0,−1) (two elementary quanta) and six junctions, at each "an open spiral branch fibre whose
  A→B node count is C_i = round(2πr_i/N_i) (prescribed; it does not close and encircles nothing)", r_i = 2M/(1 − N_i²)

## In the clicks (gr_observer_v1 run_declared with builder C's declaration; the official log 73f73002…)
- "a clicks-only observer GIVEN A DECLARATION (ports, the clock-to-shell assignment, lap 480)": the seven clock periods
  = node counts (480; 800, 684, 626, 592, 570, 554), rates N_i = 480/n_i (3/5, …, 240/277)
- the one-way light times = node counts: A_i → B_i C_i = 2094, 2258, 2545, 2895, 3284, 3723, × N_i = 6282/5 … 893520/277
  (the circumference: "a ONE-WAY A→B light time × the station rate, not a radar in local ticks"); radial A_i → A_i+1 =
  122, 108, 101, 97, 100; the 12 source → port first arrivals = the tree distances (E-3)

## Claim
- [SIMULATION, reproduced independently] "the only simulated content is that ring periods and first-arrival delays equal
  node counts"; prescribed metric data read back from clicks: not gravity, not produced by matter, not a test of the
  board's dynamics; no redshift exits, rays or closed loops yet; not claimed: "certifies vacuum Schwarzschild",
  "Einstein exactly", "the board reflects Schwarzschild exactly in its optical sector", "a vacuum test resolving 0.1",
  "at the stencil floor", "closed circumference loops", "a shell network", "Regge", "four independent masses agree",
  "gravity", "curved space made by the board"
- [SIMULATION + reported; r69 12:13] "What is read back is Schwarzschild's RADIAL static profile r(s), N(s), in clicks,
  by a declared observer; r_i is a DECLARED areal radius (the open spiral branch fibres encircle nothing); the angular
  geometry is untested (R10ZJ-19); much of the agreement is built in (one M in the design); GX-5 PARTLY within
  node-rounding noise (σ 0.07–0.30); the overall GX verdict is NOT REACHED"
- [by construction; GR-F11 (e), R10ZJ-9] the m_i spread measures the loop rounding; the r* check is built in (cumulative
  rounds of r*): its only non-trivial content is that the clicks return link counts exactly and the no-free-parameter
  chain closes; a resolved R[h] test needs 4–10× more nodes per link, or a GX-5 tolerance stated as k·σ (r68)
- reported, not computed by this package's checks: m_i spread 0.033 % (R10ZJ-9); r* within 0.3 %, the 1911 law missed by
  14–35 % (normalised by the measured delay; 17–53 % by the twin prediction) (R10ZJ-11); Misner–Sharp, K_t/K_r, m(rods),
  N·H_r (R10ZJ-7); excess radius 90.54 vs exact 91.47 (−1.0 %); stencil control 90.72 (R10ZJ-12); four estimators within
  1.3 % of m̂; Misner–Sharp and m(rods) are one quantity, and the Komar pair is a function of the clock masses; no ray
  mass (R10ZJ-14); GX-5: board − control R[h] ≤ 0.10 of 3m/r³ against σ = 0.07–0.30, scale selected from a scan, 18 of
  193 pass 0.1 (R10ZJ-13); curvature only in the declared static spherical chart; the twin T (R10ZJ-8); S2L = S (GR-F11
  2b); members (R10ZJ-15); GX-10 PARTLY at GS-2b scale; D silent and F null shown at GS-2 scale only (R10ZJ-17)
- referee: r10zj R10ZJ-1..12, 16, 18 CONFIRMED (3 for S; 6 with caveats; 7 own reader, own log; 8 arithmetic; 10 and
  stronger; 12 one wording fix; 16 shipped read), 13, 14, 17, 19 PARTLY, 15 CONFIRMED (verdicts) / PARTLY (attribution),
  20 NOT REACHED, fixes 1–12 applied; fresh machine 1 GR-F11 1–5 with the S2L addendum CONFIRMED, (a)–(e) applied

Reproduce: python -m research.matter_light_experiments_v1.verify E28_schwarzschild_radial_profile
