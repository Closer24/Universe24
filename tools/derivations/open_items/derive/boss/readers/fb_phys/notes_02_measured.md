# Notes 02: what the probes measured, and where they overturned notes_01 (2026-10-30)

All on t24b (9067de20d) with -I -B; whole numbers, the engine's carry the one division.

## P1 (one site): notes_01 s.1, s.2, s.6 CONFIRMED
- The release-sampled test gear against the standing act: 0 misses in all 15 cases (rising, falling, swinging; free
  v_p = 1, sub-notch momentum rest - 1, hairspring g = 1 at a0 = 3, g = 100 at a0 = 10, constant push 1).
  The end states are identical across courses (e.g. (3, 3, 5102) rising and falling). No lock-in of its own.
- The free gear at v_p = 1 read in rounds: L v / L_0 = 999..1000 permille by windows of 1000 rounds while the
  coordinate velocity falls from 976 to 503 counts per 1000 rounds (below one count a round, continuously).
- The 00 gear's own free course from u = 1: L^2 / (L_0^2 + 2 L_0 t) = 999..1000 permille at t = 10^3 .. 10^6
  (W_eff x101); k = 0: 197, k = 1/4: 175 (in L^3), k = 1: 6722 permille at 10^6. So k = 1/2, at the count level.
  A sub-notch proper momentum of the clock (u = 1/2) is frozen for 10^5 rounds (L = 20000 against L^2 = 2.4e9 of its
  class): the standing act's freeze.
- Two clocks at one site: proper-step periods 62..63 and 31..32 on every course, the amplitudes identical across
  courses; in rounds 317 beats against 634 over the same window (2000 permille). The text's 2012..2016 are spans of
  ten periods each, of different lengths, on a rising clock: a window artefact.

## P2, P2b (the half-step phase): notes_01 s.4 CORRECTED by my own measurement
- First run read n (an integer) against tau_now: the +-1 step noise of the release count hid everything; re-read as
  n + tau / D (the escapement's own continuous phase).
- My paper sum S = SUM (L_n - L_(n-1)) / (2 L_n) is not the whole offset: the exact identity is
  n + tau/D - tau_now = 1/2 + S' - T + (end terms), T = SUM tau_k (L_k - L_(k-1)) / (2 L_(k-1) L_k), tau_k the tooth
  after release k. P2b checks it term by term: equal to a few milli-steps at every mark of three courses.
- Monotone courses: the offset moves by +95 (L x2), -100 (L / 2), +701 (L x10.05) milli-steps against the text's
  bound (1/2) ln(L_end / L_start) = 347, 347, 1151: within the text's bound (T has S's sign and eats into it).
- Swinging courses (the 00 gear on its own spring, L about 30000 +- 27 % and +- 13 %, swings of 363 and 115 proper
  steps, and 14): the offset drifts SECULARLY: -1.94, +1.20, +5.7 (per 2e5 rounds) steps a window of 4e5 rounds,
  steady over 2.4e6 rounds (no reversal); +41 steps over 1e5 rounds at the 14-step swing. Per swing: -2.6, +1.6,
  +4.9, +8.6 milli-steps; as a fraction of the rate 7e-6, 5e-6, 4e-5, 6e-4. The text's "no secular rate; a swing
  moves it back and forth" is false against the clock read at the now slot each round. Against the clock's own course
  in proper steps (t = SUM D_k / (2 L_0), the trapezoid) it is bounded by construction (telescoping). Second order
  in the clock's change per proper step: nothing at the calibre's clock, something at a notch.

## P3 (neighbours at different depths): notes_01 s.3 CONFIRMED where measured, and a far larger finding
- A: the ring model against fb_lib.tick_board on the example universe (1 x 1 x 8, the 00 row moving): 0 misses in 60
  rounds, 82 site-releases. The model is the text's act on the light row.
- C: reflection at a sharp step N 1 -> 1/2: escapement -284 permille (transmitted 710), as built -335 (659), nature
  -4 (989). Paper: -333 / 667 for both lapse-only forms, 0 / 1000 for nature. CONFIRMED (the escapement's sample and
  hold at the step moves it from -333 to -284).
- D: Shapiro delay through 200 sites at N = 4/5: 123 rounds in all three acts (delay^2 15129 against the paper's
  15000): every lapse-only form gives the gamma = 0 delay, half of GR's at weak field. Not the escapement's own fault
  (the spatial metric, the ii slots, is G2's), but not "nature's" for light either.
- B and E: on a STANDING two-depth ring (64 sites, deep half at 2 L_0 or 7/5 L_0) the escapement's field GROWS
  EXPONENTIALLY: max |a| 1e6 -> 1.9e6 (2000 rounds) -> 1.3e10 (10^4) -> 5.7e14 (2 x 10^4); the energy H x2.6e21 in
  the second window of 2e4 rounds at 2 L_0, x5.6e14 at 7/5 L_0; the uniform control 999 permille in every window;
  the act as built's and nature's books exact (0 drift) and their fields bounded on the same lays.
  So the "drift" of SUM P is not a force at all at these contrasts: it is a runaway. notes_01 predicted a bounded
  SUM (L/L_0) P on average; that prediction (the continuum's) is overturned by the discrete multi-rate act: the
  continuum limit is stable, the act is not. Checked twice in P5.
- F: the text's case H: the clocks went from 12 and 24 grips to 770 and 838 grips (the 00 row's own pull); the lay is
  not "two sites at c = 0 and 12 grips". Held standing at L_0 and 2 L_0 (the model) the row's SUM P grows from 0 to
  4.2e9 grips in 400 rounds (from a momentum of order 5e3 grips): the same runaway; nature's SUM pi exactly 0.
