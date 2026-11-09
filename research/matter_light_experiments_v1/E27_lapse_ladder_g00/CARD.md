# E27 — A prescribed Schwarzschild-lapse ladder (g00 only), read back from clicks: ring clocks of 120/N nodes give the static redshift f_r/f_e = N_e/N_r exactly to an observer given a declaration

## On the event board
- coupling +++, vacuum (0,0,2), L = 400 (2L = 800, same sites), T = 700; builder F's ladder as ONE guide_net@1 placement
  (registry wave 15; his init file byte for byte): five closed rectangle rings of fibre light (plane z = 20), one
  A-pulse (1,0,−1) (two elementary quanta) each, of node counts 120/N, N = 1, 5/6, 4/5, 3/4, 2/3: a PRESCRIBED lapse
  written into the node counts, nothing sourced; per ring a +z tap of 370 nodes (one copy of its pulse per lap onto a
  static guide of the same kind); three side taps carry S1's, S3's, S4's pulses past S3's, S1's, S2's ports
- "On a prescribed layout (κ relay nodes per proper length, set by hand, nothing sourced), fibre-light rings follow N =
  1/κ exactly, by construction (period = node count)." The stations are LABELLED by the Schwarzschild radius with this
  g00, r = 2M/(1 − N²) = ∞, 72/11, 50/9, 32/7, 18/5 M; nothing on the board measures r
- SHAPIRO chain, a separate abstract board (M = 60, rounded), not connected to the rings: one straight fibre, one
  A-pulse; ports S4 (node 200), S3, S2, a bare-end mirror after rounded segments 89, 98, 115 (flat 177); L = 800, 1600

## In the clicks (gr_observer_v1 run_declared; log_symmetry_v1; official click logs)
- a clicks-only observer GIVEN A DECLARATION (builder F's: every ring a standard clock of proper lap 120): ring periods
  exactly 120, 144, 150, 160, 180, rates 1, 5/6, 4/5, 3/4, 2/3; far ports f_r/f_e = 5/6, 4/5, 3/4, 2/3 against F
- Pound–Rebka: period ratio (received period / local lap) = 6/5, i.e. f_r/f_e = 5/6 (S1 → S3, red); 6/5 (S3 → S1, blue);
  10/9 (S4 → S2, blue); this equals lap_e/lap_r, already read at the two ring clocks
- control (R10ZI-16 (c)): the same logs, each ring declared at its own node count: all rates 1, all f_r/f_e = 1
- Shapiro: raw radar round trips 608 (curved) and 358 (flat); one-way delays 89, 98; Einstein offset −2 = −dwell/2 (no
  mirror_dwell declared); L = 2L: the same click records (0 differ) for the ladder and both chains

## Claim
- [SIMULATION, reproduced independently] owner sentence (item 32): "When a lapse is written into its clocks, Universe24
  reads it back exactly in clicks. Five light-ring clocks were prescribed with node counts 120/N, where N = 1, 5/6, 4/5,
  3/4 and 2/3 is Schwarzschild's lapse at r = infinity, 72/11, 50/9, 32/7 and 18/5 M. They tick with periods of exactly
  120, 144, 150, 160 and 180 updates, and static guide taps carry each ring's period unchanged. A clicks-only observer,
  told that all rings are standard clocks of the same proper size, finds the static redshift law f_r/f_e = N_e/N_r
  exactly. Against the far ring this gives 5/6, 4/5, 3/4 and 2/3. Between intermediate stations it gives 5/6 (S1->S3,
  red), 6/5 (S3->S1, blue) and 10/9 (S4->S2, blue). These come from official audited runs at two board sizes."
- the clicks fix only the five periods and their ratios; with each ring declared at its own node count the same log
  reads f_r/f_e = 1 everywhere (R10ZI-16; decoded here as a control); "proper lap 120" and S4's rate 5/6 (the Shapiro
  calibration) are declarations; the Shapiro excess 250 is the node-count difference of a separate, rounded 1-D chain
- not claimed: a lapse produced by matter; anything beyond g00 (no radial distance, areal radius, curvature, sourcing or
  geodesic); "N = √(1 − 2M/r) at 5 stations" (REFUTED as a result: r is defined from N); "exact Schwarzschild"; gravity
- referee: r10zi R10ZI-1..12, 14, 18, 19 CONFIRMED (3, 5, 19 by construction; 14 for v2 only), 13, 17, 20 PARTLY, 15
  REFUTED as a result, 16 a declaration, fixes 1–11 applied; fresh machine 2 GR-F12 (1)–(3) CONFIRMED, fixes 1–4 applied

Reproduce: python -m research.matter_light_experiments_v1.verify E27_lapse_ladder_g00
