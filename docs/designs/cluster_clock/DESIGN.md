# Series Q, a cluster of crowds read by one detector: the design, with the expectation pinned before any run

The G2 experimenter, 2026-09-21, on the model owner's word after series P
([a lamp inside a crowd](../crowd_clock/DESIGN.md)). The owner (in
conversation, translated): "so is it possible that this is the matter with
galaxy clusters that look as if at a constant speed when they should have
flown apart?", and, on the experimenter's proposal of this test, "start
the additional test you proposed". Sections 1 to 6 are written before any
run; section 7 after. Nothing here is registered in
[docs/EXPERIMENTS.md](../../EXPERIMENTS.md); the register entry is drafted
in the folder's [README](../../../examples/events/cluster_clock/README.md)
for the owner's word.

Sources: series P's design and measured section (k = 4 F / 2^16 exact to
the rung; a slowed lamp moves at v / (1 + k) and falls behind an unslowed
crowd; 1 + z = (1 + k)(1 + v / c) at a detector for a lamp inside a crowd);
[BEAM_LAW](../../BEAM_LAW.md) step 4 and notes 17, 41, 48.

## 1. The question, on the board

A cluster's "velocity dispersion" is the spread of the members' redshifts
along the line of sight, read as speeds by 1 + z = 1 + v / c. Zwicky's
argument: the spread is too large for the visible mass to bind, so the
cluster should have flown apart. Under the law as built a member's reading
has a second term that is no speed: 1 + z = (1 + k)(1 + v / c) with k the
presence of its own crowd's rows at its Node over the suspension's wall
(series P). Members of different densities have different k, so a cluster
of members at rest reads a spread of z with nothing moving. The two
questions this series pins:

- **At rest.** Five members of k = 0, 0.1, 0.3, 0.6, 1 before one detector
  read 1 + z_i = 1 + k_i: a spread that a reader would call a velocity
  dispersion of 0.36 c around a mean of 0.4 c, with every body fixed; and
  the spread is one-sided (k >= 0: a member is never bluer than the
  cluster's frame).
- **Moving as one.** The same five thrown together at 0.2 c away from the
  detector. Series P found that a slowed lamp moves at v / (1 + k) and its
  unslowed crowd leaves it behind. A crowd slowed alike (every star in the
  crowd of all the others) moves at v / (1 + k) as a whole; the law then
  reads 1 + z = (1 + k)(1 + v / ((1 + k) c)) = 1 + k + v / c, the clock's
  term and the Doppler adding, so every member's z shifts by the same
  v / c and the spread is untouched by the motion. The alternative, a
  lamp behind an unslowed crowd, reads the product (1 + k)(1 + v / c) and
  the spread grows with v. This series emulates the crowd slowed alike:
  the sources of each member are thrown at v / (1 + k_i), the speed their
  lamp has on the GameBoard while it waits, so that they keep pace with it
  and the lamp stays on the heading of its fan. The emulation is by
  momentum, not by slowing the sources (nothing crosses them); what the
  run tests is the addition at the detector and the pace, not the sources'
  clocks.

## 2. The worlds

`examples/events/cluster_clock/make_worlds.py` (importing series P's
generator for the fan, the speeds and the pinned k) writes two worlds on a
bar of 201 x 9 x 9 Nodes (open), `ticks` 500, `suspension` [1, 2^16],
`release` [1, 2^16], `width` 2^20, N = 64.

- **The detector**, fixed at x = 3, measuring `s_px1` with `reads: "age"`.
- **Five members**, each a lamp of `s_px1` (2^20 units, one unit per
  self-creation on -x toward the detector, the wheel [1, 64], letting the
  crowd's rows and the other lamps' light pass) with two `mass` sources
  three Links up +y and +z sending series P's fan of nine directions
  across its line at F units per interval (the sources let the light
  pass):

| Member | lamp's number | lamp's x | F per source | pinned k | at rest 1 + z | moving as one 1 + z (the product would read) |
| --- | --- | --- | --- | --- | --- | --- |
| `m0` | 2 | 40 | none | 0 | 1.000 | 1.200 (1.200) |
| `m01` | 3 | 60 | 1638 | 0.1 | 1.100 | 1.300 (1.320) |
| `m03` | 6 | 80 | 4915 | 0.3 | 1.300 | 1.500 (1.560) |
| `m06` | 9 | 100 | 9830 | 0.6 | 1.600 | 1.800 (1.920) |
| `m1` | 12 | 120 | 16384 | 1 | 2.000 | 2.200 (2.400) |

`cluster_rest.json` (`rays-cluster-clock-cluster-rest-v1`): every body
fixed. `cluster_moving.json` (`rays-cluster-clock-cluster-moving-v1`): the
lamps at the momentum of 0.2 c along +x, the sources of member i at the
momentum of 0.2 c / (1 + k_i).

## 3. What the run reads, pinned before it

The reading window is 250 to 500 for every member (the farthest light,
117 Links, arrives after 201 intervals at rest; the receding lamp at
x = 120 is seen at the window's end as it was at tick 250). 1 + z is the
inverse slope of the birth ordinal against the click's tick, per lamp
number; the tolerance 0.02.

**(a) At rest.** 1 + z_i = 1.000, 1.100, 1.300, 1.600, 2.000. Read as
speeds these are 0, 0.1, 0.3, 0.6 and 1.0 c: a mean of 0.4 c and a
dispersion of 0.36 c, every body fixed; the least is the bare member's 1.000
and none is below it. The click rate of each is 1 / (1 + k_i) per interval;
the age read is each member's flight (64, 98, 132, 167, 201 intervals);
every birth up to the last click arrives.

**(b) Moving as one.** 1 + z_i = 1.200, 1.300, 1.500, 1.800, 2.200: each
member shifted by 0.200 from its reading at rest, the dispersion of the
five unchanged at 0.36. The product form would read 1.200, 1.320, 1.560,
1.920, 2.400: distinguishable from the sum at every member but the bare
one by 0.02 to 0.20, beyond the tolerance from k = 0.3 up. The lag between
each lamp and its sources stays within 2 Links through the run (the
sources at v / (1 + k), the lamp waiting k intervals per self-creation);
the k read from each lamp's births stays within 20 % of the pin (the lamp
on its fan's heading). The age read grows through the window (the lamps
recede).

**(c) The bare member.** `m0` reads 1.000 at rest and 1.200 moving: the
Doppler alone, series O's lab reading, the control.

## 4. What would refute the reading

- A member at rest reading off 1 + k_i by more than 0.02: k is not the
  member's own (the other members' rows or light reach it: their light
  does cross the nearer lamps' Nodes, one unit per interval, a presence
  of 2 to 6 units against F's thousands; the pin counts it as nothing).
- The dispersion at rest below 0.3: the crowd does not read as a speed.
- The moving members reading the product (1.32, 1.56, 1.92, 2.40) or a lag
  beyond 2 Links: the lamp does not move at v / (1 + k), or the Doppler is
  not by the speed on the GameBoard.
- The bare member reading other than 1.000 and 1.200: the detector's
  reading is not series O's.

## 5. What the run cannot decide, and what it is for

The worlds pin the law's arithmetic for a cluster, not nature's clusters:
the run cannot say whether any observed dispersion is a spread of clocks.
It says what the law as built offers: a dispersion with nothing moving,
one-sided (never bluer than the frame), of the size of the spread of k
among the members; and that for a cluster moving as one the clock's term
and the Doppler add, so a cluster's motion does not widen the spread. Two
signatures follow for a reader of nature's clusters, if the mapping of
units were known (it is not): the members' z around the mean skewed to
the red with the denser members redder; and the dependence of k on the
flux of rows through the member's Node (about the sum of M / r^2 over its
crowd), where gravitational redshift depends on the potential. The
emulation of the crowd slowed alike is by momentum; a run in which the
sources are slowed by rows of their own is a further series.

## 6. The run, when ordered

    PYTHONPATH=src python examples/events/cluster_clock/make_worlds.py
    PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/cluster_clock examples/events/cluster_clock/cluster_rest.json examples/events/cluster_clock/cluster_moving.json

The readings are the detector's `click` lines per lamp number (the birth
ordinal against the tick, the `age`), the lamps' `birth` lines (their
clocks) and the `step` lines of every lamp and source (the lag).
`tests/test_cluster_clock.py` pins the shipped worlds to the generator,
the presence 4 F at every lamp once the rows arrive, the pace of the
emulated sources and the algebra of the sum against the product.

## 7. Measured (2026-09-21, one run on main d8cb46e, after the pins above)

The run is `tools/run_series.py --jobs 2` over the two worlds (four seconds
each, the books balanced, 500 intervals), read by the experimenter's script
in the window 250 to 500 per lamp number. Every one of the ten readings of
1 + z is inside the tolerance of 0.02; every birth ordinal up to the last
click arrived (no light lost); the lag between each lamp and its emulated
sources stayed within one Link through the run.

| Member | pinned k | k read from the lamp's births | at rest 1 + z (pinned) | click rate | age | moving as one 1 + z (pinned; the product) | click rate | age first .. last | shift from rest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `m0` | 0 | 0.000 | 1.0000 (1.000) | 1.000 | 63 | 1.2007 (1.200; 1.200) | 0.836 | 94 .. 135 | +0.2007 |
| `m01` | 0.1 | 0.101 | 1.0999 (1.100) | 0.912 | 98 | 1.3022 (1.300; 1.320) | 0.764 | 120 .. 158 | +0.2023 |
| `m03` | 0.3 | 0.302 | 1.3001 (1.300) | 0.768 | 132 | 1.5066 (1.500; 1.560) | 0.664 | 147 .. 180 | +0.2066 |
| `m06` | 0.6 | 0.592 / 0.613 | 1.6000 (1.600) | 0.628 | 166 | 1.8092 (1.800; 1.920) | 0.552 | 175 .. 202 | +0.2092 |
| `m1` | 1 | 1.000 / 1.016 | 2.0000 (2.000) | 0.500 | 201 | 2.2147 (2.200; 2.400) | 0.452 | 206 .. 228 | +0.2147 |

The cluster at rest: z mean 0.4000 (pinned 0.400), dispersion 0.3633
(pinned 0.363), minimum 0.0000 (pinned 0). Moving as one: z mean 0.6067,
dispersion 0.3683 against 0.3633 at rest.

**What the run decides.**

1. **A cluster at rest reads a velocity dispersion.** Five bodies fixed to
   the GameBoard read 1 + z = 1.000, 1.100, 1.300, 1.600, 2.000 to the
   fourth digit: a reader of speeds would call it 0.36 c of dispersion
   around 0.4 c, with nothing moving, and one-sided (no member below the
   bare one's 1.000). The spread is the spread of the members' crowds.
2. **A cluster moving as one adds the Doppler; the spread stays.** Each
   member's z shifted by 0.201 to 0.215 for the pinned 0.200; the product
   form (0.220, 0.260, 0.320, 0.400 for k = 0.1 to 1) is refuted at every
   member from k = 0.3 up (2.2147 read where the product would be 2.400).
   The dispersion moved from 0.363 to 0.368. A small excess over the sum
   grows with k (+0.002, +0.007, +0.009, +0.015 for k = 0.1, 0.3, 0.6, 1)
   and follows the k read from the lamps' births (1.016 for the pinned 1;
   0.613 for 0.6): the moving lamp counts a little more presence than the
   fixed one (its crowd's rows are released from a source that has moved on
   since), inside the tolerance and the k bracket; not a term of the
   reading.
3. **The emulation held.** The sources at v / (1 + k) kept within one Link
   of their waiting lamp for 500 intervals at every k: a body that waits k
   intervals per self-creation moves at v / (1 + k) on the GameBoard, as
   series P found, to the Link.
4. **The control.** The bare member read 1.0000 and 1.2007: series O's lab
   reading, the Doppler alone.

**For the owner's question.** Under the law as built, yes: a cluster's
velocity dispersion can be a spread of the members' clocks, of the size of
the spread of their crowds' k, with no motion and no mass to bind it; the
cluster's own motion adds the same Doppler to every member and does not
widen the spread. What would tell it apart in nature, if the mapping of
units were known (it is not, section 5): the members' z around the mean
skewed to the red and never bluer than the frame's, the denser members
redder; and k by the flux of rows through the member's Node (about the sum
of M / r^2 over its crowd) where gravitational redshift goes by the
potential. The rotation curve of a single galaxy is not touched: both sides
of a radius share one k, and the half-difference of their readings gives the
speed without it.
