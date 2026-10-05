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

Since the owner's word of 2026-10-04 (ALGEBRA.md, The vacuum content, item 22: the vacuum content 60 declared in every universe file above the holders' swing over the declared run, a fence for the declared run and not a cure) `standing_15.json` declares its run at n = 400 intervals and not 1000: the fence of 60 covers about 470 intervals on this 25-cube (the advisor's run of the lay regenerated at the rest 60 by `tools/pixel_mode.py`, the first Node at or below the content 0 at interval 475, as at 471 on matter_alone; over 400 the lowest content 19 and no Node at or below 0), and the integer budget's least T for this lay (2,373 Nodes carrying 9,982 quanta, the largest count at a Node 36) at the tolerance [1, 32] is 16,384 at 400 intervals against the file's 32,768 (65,536 at 1,000), so the declared run moves and the vacuum content does not; the blind's numbers at n = 400 are re-derived at the control run and not here.

## The blind (167 with the advisor's second hand)

1. **The drift** (read 1, the centroid of the share): each component below
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

## The blind restated, 172 with the advisor's second hand

The mathematician's 172 (#1572 comment 5959853571) with the advisor's second hand (#1563 comment
5960096992), two hands on each part, under the owner's word of 2026-10-03, 00:47 (fix everything
that was found): reads 2 and 3 above were written for a uniformly rotating plane record, and this
body is a real mode, a_i(t) = A_i cos(omega t + phi) with every Node in one phase. The reads are
restated in `tools/body_standing.py` and the blind of each is written here and in `design.json`
(`form_deviation`, `rotation_windows`; the body's own numbers under `from_the_lay` in
`expectation.json`) before any re-run; the blind and the reading above stay as the dated record,
and the convention's reads stand beside the restated ones in the reader's one output.

1. **Read 2 on the form** (172 (2)): the law's own static quantity per Node is the form
   D_i = now^2 - next x before (the count is the record's share), A_i^2 sin^2 omega exactly for one
   real mode at every interval, Node by Node, with no 2 omega term, where the levels' squares
   breathe at 2 omega (the maxima 4.1 intervals apart read above are that breathing and no drift).
   The read: rho_D = sqrt(SUM (D_i(k) - D_i(0))^2 / SUM D_i(0)^2) over the body's declared Nodes at
   every form centre k (the form at k from z_(k - 1), z_k and z_(k + 1); the lay's own form at 0
   the reference; the window's last centre 999, the form at 1000 needing z_1001) and at the
   quarters, exact integers and the root at the scale T by the division act's fixed point. The
   blind, from the walk alone: twice the levels' relative walk, D being quadratic,
   rho_D = 11.3 sigma sqrt(n) / A for the exponential profile, 3.3, 4.7, 5.7 and 6.6 percent at
   n = 250, 500, 750 and 1000 at T = 2^15 for 163's body and a quarter of each at 2^19; for this
   world's own lay (A = 1865, N_eff = 148, the shape factor 1.84) twice rho_s's expectation at each
   quarter, 0.98, 1.39, 1.70 and 1.96 percent (`rho_d_expected`); the sqrt(n) law
   rho_D(n) / rho_D(n / 4) = 2 within 5 percent; the T ratio 4 within 5 percent on the walk's part,
   unread while standing_19 stands unlaid. What is not the walk and does not scale with T: the lay's
   admixture, a second mode of the well the lay also carries, beating with the first at
   Delta omega = 2 pi / 185 = 0.034 per interval (the envelope of 185 intervals read above), read on
   the series' envelope (the local maxima of rho_D^2 at every interval and of its means over
   successive windows of one period, with their spacings) as crests spaced at the beat's period, the
   same at both T; the start's rest short of its own static line (the advisor's 137 fine units,
   fixed on the engine's fix round) shifts omega_b by about 10^-4 and rings in the board's lowest
   mode at about 52 intervals, a spacing near 52 naming it if present. A growth faster than sqrt(n)
   with no beat is a systematic of the lay or of the step, a finding by name.
2. **Read 3 over a window of whole periods** (172 (3)): for a real mode every Node crosses 0 at
   once, so the per-interval summed read has two near-singular intervals per period, and the spread
   7.2 x 10^-3 read above is those intervals, not a drift and not the beat (the advisor's second hand
   correcting his own line of 5959617991 (2)). The read:
   2 cos omega_read = SUM over the window of SUM over the body of z_t (z_(t + 1) + z_(t - 1)) / the
   same double sum of z_t^2, exact as a fraction, the window of whole periods from the mode file's
   clock pair (2 cos omega = clock[0] / clock[1] = 2566 / 1865 at this lay; the period the whole
   intervals nearest 2 pi / omega by the rotation's own recurrence, 8), per successive window, over
   the whole run, with the windows' least, largest and spread and the window series' envelope; the
   per-interval read kept for the record, labelled near-singular. The blind: exact for one mode with
   no singular interval, constant over the windows to 10^-5 at both T away from the beat, its noise
   1 / (A sqrt(N_eff n_W)), 3 x 10^-7 over 10^3 intervals at 2^15 for 163's body and for this lay
   1.4 x 10^-6 over the whole run and 1.6 x 10^-5 over one window of 8 (`rotation_window_noise`);
   the whole run's read against the lay's clock pair, 1.3759; the series over successive windows
   swinging at the beat where two modes are laid, the same at both T; a drift of the whole run's read
   beyond the noise and the beat is a finding by name.
3. **Reads 1 and 4** stand as written above.

### The reading on today's engine (main 3f2cc9bd), T = 2^15, n = 1000 (GameBoard, `tools/body_standing.py`; 2.6 minutes)

- **Read 2 restated, rho_D at the quarters** (the centres 250, 500, 750 and 999): 1.16, 2.85, 4.15
  and 4.13 percent against the lay's own blind from the walk alone, 0.98, 1.39, 1.70 and 1.96;
  rho_D(999) / rho_D(250) = 3.56 against the sqrt(n) law's 2 within 5 percent, a finding by name.
  The series over windows of one period (the means over 8 intervals): 0.24 percent at the centre 1,
  rising to 6.3 at 129, falling to 1.45 at 241 to 249, 4.2 at 313, 2.1 at 353, a plateau of 3.1 to
  3.5 from 369 to 449, 2.2 at 529, 6.2 at 593, 3.2 at 633, 3.1 at 713, 7.4 at 833 and 3.3 at 985: an
  envelope swinging by about 5 percent about a slow rise, the quarters landing on it (250 in a trough,
  750 and 999 in its middle), so the sqrt(n) ratio reads the swing and not the walk. The beat's
  period as read: the crests at 129, 313, 593 and 833, spaced 184, 280 and 240 (the first the first
  reading's 185), no one period; the window series' maxima 88, 96, 72, 40, 48, 24, 24, 72, 64, 32,
  64, 24, 56, 16, 40, 24 and 48 apart; no spacing holds at 52. At the interval scale the series'
  local maxima are 3.80 intervals apart on the mean (261 of them; half the period 7.73, as rho_s's
  4.1): the reader's note, one hand, that one real mode's form has no breathing and that the one
  interval's rounding enters the form as D(k) = Q(k) - e_(k + 1) z_(k - 1), Q the exact form of the
  recurrence and |e| below one unit, a jitter of the order 1 / A, 0.1 percent, riding at the period
  on the slow envelope and accumulating nothing. The restated blind's walk, 1.96 percent at the end,
  is not read apart from the swing: a finding of the lay (the admixture, T-free by 172) and not of
  the step as far as this run reads; the T ratio stands unread. rho_s beside it as in the first
  reading, 1.58, 2.07, 5.20 and 3.94 percent, its maxima 4.1 apart.
- **Read 3 restated, the windows** (the period 8 from the clock pair 2566 / 1865 by the recurrence;
  125 windows): the whole run's 2 cos omega_read 1.38146 against the lay's clock pair 1.37587,
  +5.6 x 10^-3; the windows' least 1.37581 (from the centre 96) and largest 1.38840 (from 896), the
  spread 1.26 x 10^-2 against the blind's 10^-5 and the lay's own noise 1.6 x 10^-5 per window, a
  finding by name: the window series rises through the run, 1.3758 to 1.3796 over the first 100
  intervals, 1.3780 to 1.3857 over the middle and 1.3806 to 1.3884 over the last 100, about
  +7 x 10^-3 between the means of the first and the last ten windows, the rotation slowing while the
  books' share drifts +332 quanta (+3.3 percent) over the same run; on the rise a swing of about
  2 x 10^-3 with maxima at the windows from 24, 72, 128, 176, 232, 280 and 328, spaced 48, 56, 48,
  56, 48 and 48, about 50 intervals, the board's lowest mode's period of about 52: the line the blind
  named for the start's rest short of its own static line, present on read 3's window series and
  absent on rho_D's envelope; in the second half the maxima 16 to 56 apart. The per-interval read as
  in the first reading, least 0.68755 at 102, largest 0.69478 at 989, the spread 7.2 x 10^-3 over
  493 intervals, the accumulated 0.69073: the near-singular intervals hid the drift the window read
  shows.
- **Reads 1 and 4 and the books** as in the first reading: the centroid's drift exactly 0 on every
  axis; the 48 images kept to the bit through 515 and departing at 516 on gravity's row under the
  exchange of y and z; the share 6,244,274,537,235, 10,587 quanta, the drift +195,991,024,483, the
  least pace 4,961, no frozen Node.

## The blind restated again before the re-read on the fixed engine, 175 with the advisor's hand

The mathematician's 175 (#1572 comment 5962582859, items 3 and 7) with the advisor's 5962061454
(the rest's remedy, the write's one division and what the re-read must show), relayed by the Boss
for the standing world before the re-read on the fixed engine (the start's rest corrected to its
own static line by the scaled residual, the write's factor one division; branch fix-round). Written
here before the re-read; the readings above stand as the dated record.

1. **What the two fixes must show.** After the rest's fix the line at 1 / 52 vanishes (the swing of
   about 50 intervals on read 3's window series above); after the write's fix the 48 images hold to
   the bit over the whole run of 1000 intervals (166's theorem as the diagnostic; the departure at
   516 above was the three ordered roundings). A departure at any interval, or the 52 line
   remaining, is a finding by name.
2. **Read 2 in two parts.** What remains in rho_D is the walk, 11.3 sigma sqrt(n) / A within 5
   percent (3.3, 4.7, 5.7, 6.6 percent at the quarters at 2^15 for 163's body; 0.98, 1.39, 1.70 and
   1.96 for this lay, `rho_d_expected`) with the sqrt(n) ratio rho_D(1000) / rho_D(250) = 2 within 5
   percent, the blind, pass or fail; and the lay's beat at 1 / 185 (Delta omega = 0.034, the
   neighbouring mode's admixture, T-free), reported as the Fourier weight of that line and not
   blinded, since the lay at today's integer fixed point carries it by construction (160 (a) closes
   the static part, not the mode's purity). Read 2 passes when the walk's part, the series less the
   beat's line, sits within 5 percent of 11.3 sigma sqrt(n) / A; a third part is a finding by name.
   The reader takes the beat's period on its command line (`--beat-period 185`, the first reading's
   envelope) and reads the Fourier line of the rho_D^2 series at it in floats, labelled so, the
   line's weight by the division act's fixed point and the series less the line at the quarters.
3. **The T ratio at 2^17, not 2^19.** The 2^19 lay cost 89 minutes of CPU unfinished; `standing_17`
   is declared instead on `rule_2_17.json` (rule.json's rows at T = 2^17), the tolerance [1, 64]
   (rho_s's expectation halves as A doubles; the least T by the budget's line 2^16 at c_i = 79) and
   the stop 4 (the same fraction of the amplitude), to be laid and run on the fixed engine when
   fix-round lands: A grows by 2, the blind's ratio rho_D(2^15) / rho_D(2^17) = 2.00 within 5
   percent on the walk's part and 1 on the beat's. If the 2^17 lay is still long, the sqrt(n) law
   within the 2^15 run alone separates the walk from the beat with the Fourier line, and the T ratio
   is left for the morning by name.

### The Fourier line read on today's engine (main 3f2cc9bd), before the re-read

The same run re-read with `--beat-period 185` (5.5 minutes on the shared machine; every other
number bit for bit the reading above):

- **rho_D^2's line at 1 / 185:** the components -2.5 x 10^-4 and -3.7 x 10^-4, the weight
  4.5 x 10^-4 in rho_D^2 (the series' mean 1.53 x 10^-3, rho_D's rms over the run 3.9 percent), so
  the line swings rho_D between about 3.3 and 4.4 percent about its rms where the series swings
  between 1.45 and 7.4: the line at 185 is a small part of the swing. The series less the line at
  the quarters, the walk's part by 175 (3): 1.69, 1.95, 4.57 and 4.14 percent at 250, 500, 750 and
  999 against the walk's blind 0.98, 1.39, 1.70 and 1.96, within 5 percent at none (1.7, 1.4, 2.7
  and 2.1 times it), the residual's ratio 999 / 250 = 2.46 against 2: a third part, by name, the
  swing whose crests stand 184, 280 and 240 apart (not one line at 1 / 185), which on today's engine
  carries the start's rest short of its own line (the 52-interval swing on read 3's series, the
  well's rotation drifting +7 x 10^-3 over the run with the share +3.3 percent); whether it is the
  rest's and the write's, or the lay's, is the re-read's on the fixed engine, by name.
- **Read 3's window series at 1 / 185:** the components 3.3 x 10^-5 and -2.5 x 10^-5, the weight
  4 x 10^-5, at the noise; the window series carries no beat at 185, only its rise and the swing at
  about 50 intervals.
## On the fixed engine (the fix round, 2026-10-03)

The engine of branch `fix-round` (on main 3f2cc9bd): the write's factor booked as one rounding
of the count times p_x p_y p_z over the one wall, the product exact beyond the width
(`paces.write_factor`; the advisor's and the mathematician's lines, #1563 comments 5959617991
and 5960096992, #1572 comment 5959853571), and the start's rest refined to the row's static
line within one fine unit at every Node by the scaled residual in integers (`features/start`,
`refined`; the advisor's finding and remedy, #1563 comments 5958624379 and 5959617991). The
world re-laid by the generator on this engine and the blind rebuilt byte for byte by the
builder; every number below a GameBoard reading labelled so (`tools/body_standing.py`); a miss
against the blind is a finding by name, never adjusted.

- **The lay** (`standing_15`, the stop 2, the generator's reading before any run): converged at
  the pass 8 (16 on the engine before; the trajectory in the mode file: the content's largest
  change 96, 17, 16, 9, 3, 2, 1, 1 and the record's 131, 79, 47, 24, 9, 4, 2 from the pass 2),
  the amplitude 1,885 (the clock pair [2596, 1885], 2 cos omega_b = 1.3772, against 1,865 and
  [2566, 1865] = 1.3759 before), 9,992 quanta over 1,527 Nodes, 82 at the centre (9,987 over
  1,551 Nodes, 79 at the centre, before), the mode file's record over 11,249 Nodes (11,441);
  62 minutes of wall time on a shared box (about 9 minutes of CPU). `standing_19` stays
  declared without a mode file, refused at load by name.
- **The reading at T = 2^15, n = 1000** (`tools/body_standing.py`, 11.6 minutes of wall time on
  the shared box): **read 1**, the centroid 12, 12, 12 at the start and at the end on every
  axis, the drift exactly 0 (the blind's 3 x 10^-3 Links: pass). **Read 2**, rho_s 1.83 percent at
  n = 250, 3.82 at 500, 4.18 at 750, 3.61 at 1000 (1.58, 2.07, 5.20 and 3.94 on the engine
  before) against the lay's expected 0.49 and 0.98 percent: a finding by name, as before; the
  ratio rho_s(1000) / rho_s(250) = 1.97, within the blind's 2 by 5 percent (2.49 before), but the
  series is no sqrt(n) walk: the deviation rises to 9.3 percent at the interval 130, falls to 1.3
  at 240 and swings between 1.5 and 7.6 after, the local maxima 4.2 intervals apart on the mean
  (half the rotation's period, the real mode's own breathing, as the second reading named it) and
  no line at the lowest mode's period of 52; the 2^19 world not laid, the ratio between the two T
  unread. **Read 3**, cos omega_read over the 495 intervals of at least half the record's largest
  weight: least 0.68826 at the interval 121, largest 0.69490 at 879, the spread 6.6 x 10^-3 against
  the blind's 10^-5 (7.2 x 10^-3 before), a finding by name as before (the mathematician's 172 and
  the advisor's second hand name it the real mode's near-singular intervals, the restated read 3
  being another worker's); the accumulated ratio 0.69062; the first interval's 2 cos omega 1.37715
  against the lay's clock pair 1.3772. **Read 4, the 48 images**: every line of every family kept
  its 48 images about the centre to the bit, levels, remainders and write remainders, through the
  interval 1000, the whole run, no departure (515 and the departure at 516 on gravity's tension
  lines before): the finding of the body round's read 4 is closed by the write's one rounding
  (`tests/test_the_bound_body.py` asserts it on this world). **The books at the end**: the share
  6,222,824,121,666, 10,550 quanta, the drift +156,330,765,293 in the current's units (+265 quanta
  over 1000 intervals, 2.6 percent of the count; +332 before), the least pace 4,938, no frozen Node.
- **The known cause above, closed**: the start's rest is refined to the row's static line within
  one fine unit at every Node (ENGINE.md section 3; on the point source of 3,000 quanta at this
  cube's centre the massless row's rest stands at 1682 against the exact line's 1682.19 and the
  binding row's at 1677 against 1676.55, where the stop alone left them 1677 and 1674,
  `tests/test_the_features.py`); the body's holders rest on that line, so no ringing at the lowest
  mode's period is left to find in this series, and none is read.

## The restated reads on the fixed engine (main 7c9a170e), T = 2^15, n = 1000

The restated reads (`tools/body_standing.py --beat-period 185`, 6.1 minutes) on the lay the fix round
made (the section above: the amplitude 1,885, the clock pair [2596, 1885] = 1.37719, 9,992 quanta
over 1,527 Nodes, 82 at the centre; N_eff = 145, the shape factor 1.84; the blind's own numbers
rebuilt by the builder: rho_D's walk 0.97, 1.37, 1.68 and 1.94 percent at the quarters, read 3's
noise 1.4 x 10^-6 over the run and 1.6 x 10^-5 per window of 8) on the engine of main 7c9a170e
as squashed. The books of this run differ from the fix round's reading above (the share
6,258,897,615,428, 10,611 quanta, the drift +192,560,448,685, +326 quanta, the least pace 4,960,
against 6,222,824,121,666, +265 quanta and 4,938 there), so the engine read here is not the one
that reading ran on (the branch before its squash), by name; every number below is of 7c9a170e.

- **Read 1:** the centroid 12, 12, 12 at both ends, the drift exactly 0 on every axis: pass.
- **Read 2 restated, rho_D at the quarters** (the centres 250, 500, 750, 999): 2.36, 4.13, 3.18
  and 4.07 percent against the walk's 0.97, 1.37, 1.68 and 1.94 (2.4, 3.0, 1.9 and 2.1 times);
  rho_D(999) / rho_D(250) = 1.73 against 2 within 5 percent: a finding by name. The window-mean
  envelope: 0.25 percent at the centre 1, rising to 8.8 at 129, falling to 1.8 at 273, 5.9 at 409,
  3.8 at 457, 4.3 at 489, 2.6 at 521, 4.3 at 561 to 585, 2.5 at 641, 3.3 at 721, 2.7 at 769, 6.6 at
  825, 4.3 at 873, 5.6 at 897, 2.7 at 969: the crests at 129, 409 and 825, spaced 280 and 416, with
  lesser maxima 16 to 104 apart; no one beat period and no spacing at 52. The Fourier line at 1 / 185:
  the components -0.8 x 10^-4 and -6.1 x 10^-4, the weight 6.1 x 10^-4 in rho_D^2 (the series' mean
  1.83 x 10^-3, rho_D's rms 4.3 percent); the series less the line at the quarters, the walk's part
  by 175 (3): 3.16, 3.31, 3.59 and 4.42 percent, 3.3, 2.4, 2.1 and 2.3 times the walk's blind,
  within 5 percent at none, the residual's ratio 999 / 250 = 1.40 against 2: read 2 does not pass;
  the third part, by name, is the swing whose crests stand 280 and 416 apart, not a line at 1 / 185
  and not the walk, with the rest refined and the 48 images kept (read 4): the lay's, or the step's
  under the well's drift (the books +3.3 percent). At the interval scale the maxima are 3.98 apart on
  the mean (250 of them, half the period 7.74), the one interval's rounding in the form as noted
  above. rho_s beside it, 167's convention: 2.15, 3.19, 2.91 and 4.68 percent, its maxima 4.0 apart.
- **Read 3 restated, the windows** (the period 8 from [2596, 1885]; 125 windows): the whole run's
  2 cos omega_read 1.381235 against the clock pair 1.37719 (+4.0 x 10^-3); the windows' least
  1.376655 (from the centre 120) and largest 1.390098 (from 872), the spread 1.34 x 10^-2 against
  the blind's 10^-5 and the lay's noise 1.6 x 10^-5 per window: a finding by name. The series holds
  within 1.3767 to 1.3781 over the first 190 intervals, then rises, 1.379 at 240, 1.380 at 300,
  1.381 at 420 to 470, 1.382 at 500 to 550, 1.385 at 600, 1.387 at 712, 1.388 at 816, 1.390 at 872,
  1.385 at 984, about +7.5 x 10^-3 between the means of the first and the last ten windows, the
  rotation slowing while the books' share drifts +326 quanta; and on the rise a swing absent in the
  first 300 intervals and growing to about 3 x 10^-3 by the end, its maxima at the windows from 496,
  552, 608, 664, 712, 768, 816, 872, 920 and 976, spaced 56, 56, 56, 48, 56, 48, 56, 48 and 56,
  about 53 intervals, the board's lowest mode's period: the line the blind said must vanish with the
  rest's fix is here, but not from the start (the start's rest is refined to the line, the section
  above) and growing through the run, so it is not the start's miss but a ringing of the lowest
  mode fed during the run, by name; the Fourier line at 1 / 185 on this series 1.4 x 10^-4, at the
  noise. The per-interval read: least 0.68831 at 118, largest 0.69551 at 876, the spread
  7.2 x 10^-3 over 493 intervals, the accumulated 0.69062, the first interval's 2 cos omega 1.37711
  against the clock pair 1.37719.
- **Read 4, the 48 images:** every line of every family kept its 48 images to the bit, levels,
  remainders and write remainders, through the interval 1000, the whole run, no departure: the
  engine worker's claim read and confirmed on 7c9a170e; pass.
- **The T ratio** stands unread: standing_17 declared and not laid (the Boss's word of 09:10 Israel,
  not tonight), standing_19 not laid.

## The readings' sources (the owner's word of 2026-10-03, 10:08 Israel)

Every number of every reading in this file is a GameBoard reading (`tools/body_standing.py`: the
centroids of the share, the deviations of the share and of the form over the body's Nodes, the
rotation from the levels, the 48 images of every line, the books). The world declares no NodeReader,
so no number is a NodeReader's line and no verdict rests on one. Nothing here is stamped by a
NodeReader's clock; the intervals are the board's.
