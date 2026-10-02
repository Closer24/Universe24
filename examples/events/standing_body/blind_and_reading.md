# The standing world: the blind and the reading

The body round, part 1 (the owner's words of 2026-10-02, 17:40 to 17:55 and 19:28; HIGHLIGHTS.md):
the same neutral body of the matter family, 10,000 quanta at the centre of the open 25-cube, laid
at the integer fixed point under its own paces (`lay` of the kind `fixed_point`) and run for the
same n = 1000 intervals at T = 2^15 (`standing_15.json`, examples/events/rule.json) and at
T = 2^19 (`standing_19.json`, `rule_2_19.json`). The blind is the mathematician's 167 (#1572
comment 5955538687) with the advisor's second hand (#1563 comment 5955658812 (C)), written in
`design.json` and `expectation.json` before any run and never edited after; the body's own
expectations from the lay's profile stand under `from_the_lay` in `expectation.json`, written from
the mode file before any run. The reading is appended here after the run; every number a GameBoard
reading labelled so (`tools/body_standing.py`); a reading that misses the blind is a finding,
written as such and never adjusted.

## The blind (167 with the advisor's second hand)

1. **The drift** (read 1, the centroid as `tools/body_drift.py` reads it): each component below
   3 x its rms, 2 sigma sqrt(n) rho_x / (A sqrt(N_eff)); for this body from the lay's profile
   1.0 x 10^-3 Links at n = 1000 and T = 2^15; one draw, loose, no test.
2. **The share's deviation over the body** (read 2): rho_s = (2 sigma sqrt(n) / A) sqrt(SUM f^2 /
   SUM f^4), 5.66 sigma sqrt(n) / A for the exponential profile; for this body from the lay's
   profile 0.98 percent at n = 1000 and T = 2^15 (0.49 at n = 250); the two tests: rho_s(2^15) /
   rho_s(2^19) = 4 within 5 percent at equal n, and within one run rho_s(n) / rho_s(n / 4) = 2
   within 5 percent; a ratio near 1 in either, or a growth faster than sqrt(n), is a T-free
   systematic, the lay's or the convention's, a finding by name.
3. **The rotation** (read 3, the summed form): constant over the run to 10^-5 at both T.

## The lay (GameBoard readings of the generator, before any run)

- At the stop 1 (a fixed point to the unit) the lay at T = 2^15 was refused by name after 30
  passes: from the pass 16 the lay-and-rest map is a 2-cycle, the content's largest change 1 and the
  record's 2 at every pass, the count laid alternating 9,981 and 10,017 (the record's scale flipping
  between two neighbours); the lay-and-rest map has no fixed point to the unit for this body in
  integers. The 2^19 lay at the stop 1 was cut after 31 minutes, unfinished (the owner's word of
  19:28).
- At the stop 2 (the least the trajectory reached) the 2^15 lay converged at the pass 16: the
  amplitude 1,865 (the clock pair [2566, 1865], 2 cos omega_b = 1.3759), 9,987 quanta over 1,551
  Nodes, 79 at the centre, N_eff = SUM f^2 = 148, sqrt(SUM f^2 / SUM f^4) = 1.84, rho_x = 2.38 Links.
  The 2^19 lay at the stop 8 (the same fraction of the amplitude) was stopped at the Boss's deadline
  of 22:15 Israel after 110 minutes of wall time and 89 minutes of CPU on a shared machine, unfinished
  (the owner's word of 19:28, whatever takes a lot of time, cut it); its world is shipped declared with
  its tolerance [1, 125] and without a mode file, refused at load by name, and the blind's ratio between
  the two T stands unread until the lay is run to its end.
- The budget's gate (`loader/lay.py`): at the lay's c_i = 79 over 1000 intervals the least T is
  2^14 at the tolerance [1, 32] and 2^18 at [1, 125], under the worlds' T; the gate refuses by name
  when the tolerance asks more (tests/test_pixel_mode.py).

## The reading at T = 2^15, n = 1000 (GameBoard, `tools/body_standing.py`; 2.8 minutes)

- **Read 1, the drift:** the centroid along x, y and z 12, 12, 12 at the start and 12, 12, 12 at
  the end, the drift exactly 0 on every axis (below the blind's 3 x 10^-3 Links; a symmetric lay
  stepped bit for bit, read 4 below).
- **Read 2, rho_s at the quarters:** 1.58 percent at n = 250, 2.07 at 500, 5.20 at 750, 3.94 at
  1000, against the lay's expected 0.49 and 0.98 percent; rho_s(1000) / rho_s(250) = 2.49 against
  the blind's 2 within 5 percent (a finding by name); the ratio between the two T not read, the
  2^19 run not run.
  What the series shows at every interval (`breathing`): the deviation's local maxima are spaced
  4.1 intervals apart on the mean, half the body's rotation period 2 pi / omega_b = 7.7 intervals,
  and its envelope rises and falls slowly, 0.33 percent at n = 10, 1.1 at 60, 6.4 at 120, 1.4 at
  220, 5.3 at 320, 2.2 at 360, about 185 intervals between the envelope's crests. The convention's
  systematic, by name: 167 defines rho_s for a uniformly rotating plane record, whose |z|^2 is the
  standing quantity; this world's body is a real standing mode (no sign holder, the owner's
  neutral body), whose share per Node is not constant in time but carried between its Nodes by
  Rule3's currents at twice the rotation's frequency, so rho_s against the lay's share at the
  interval 0 reads the mode's own share breathing first and the rounding walk under it; the
  standing quantity of a real mode is its share averaged over a period, or its form. The slow
  envelope is a breathing of the body about its lay; the advisor's known cause (below) names one
  source of it.
- **Read 3, the rotation:** cos omega_read over the intervals of at least half the record's
  largest weight (493 of 1000, the real mode's zero crossings excluded): least 0.68755 at the
  interval 102, largest 0.69478 at 989, the spread 7.2 x 10^-3 against the blind's 10^-5 (a
  finding by name); the accumulated ratio over the window 0.69073; the first interval's 2 cos omega
  1.37569 against the lay's clock pair 1.3759.
- **Read 4, the 48 images** (the body round's part 2, 166's theorem as a GameBoard diagnostic):
  every line of every family kept its 48 images about the centre to the bit, levels, remainders and
  write remainders, from the lay through the interval 515; at 516 gravity's row departed under the
  axes permutation (0, 2, 1), y and z exchanged, with and without reflections: its tension lines,
  whose one write is scaled per proper volume by the three axes' paces divided one at a time in
  the order x, y, z (ENGINE.md section 3, act 5; `paces.write_factor`), a booking that is not a
  symmetric function of the axes once the Links' paces differ by axis, where 166's proof takes every
  act as a symmetric function of the Node's and its Ports' integers. A finding by name for the
  one-domain step, which would be exact only with the write's factor booked symmetrically in the
  axes; nothing patched.
- **The books at the end:** the share 6,244,274,537,235, 10,587 quanta, the drift +195,991,024,483
  in the current's units (+332 quanta over 1000 intervals, 3.3 percent of the count), the least pace
  4,961, no frozen Node.

**A known cause outside the blind** (the advisor, #1563 comment 5958624379, carried by the Boss):
the start's `rest` (features/start, `settled`) stops at the first state the act returns
unchanged, so on the board's lowest mode it misses its own static line by up to one fine unit over
(1 - rho), rho = (num / den) cos(pi / (n + 1)) on an open n-cube: 137 fine units at n = 25, 9
levels at the massless row's unit 15 and 3.6 at the binding row's unit 38. The generator rests
the body's holders with the same `rest`, so the well the body was laid in may be short by that
amount and ring at that mode's period (2 pi / omega_min, about 52 intervals on the 25-cube by the
advisor's number); the series above shows the body's own breathing at half its period and a slow
envelope of about 185 intervals, no clear line at 52. The stopping rule is not changed in this
round (a round of its own: a stopping rule on the residual, its test the rest against the exact
solve to one level on a point source, both pairs).

What the short run does not test (163 (2), 165): the body's standing over long runs and the line
as a click.
