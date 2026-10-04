# The which-way world: the blind and the reading

The experiment of the heart (the owner's word of 2026-10-03, 01:52 UTC, experiments that test that it
works in the engine; the advisor's matrix, #1563 comment 5964151108, T2): the two slits of
`examples/events/two_slits` with a declared region at one gap backed by a face. Behind the lower gap
(the rows 17 to 19) a channel of the rows 16 to 19 runs from the wall's far side to the screen's
column between two inner faces across y at the rows 15 and 20 (the channel's walls, over the columns
21 to 43), and the whole channel is one declared NodeReader, `which_way`, whose far end is the screen's
column before the receding face: everything that passes the lower gap leaves the declared board
through the channel and is credited there, and nothing of it reaches the rest of the screen, which is
read in regions of four rows as the two slits' screen is (`screen_0` to `screen_11`, the channel's
rows left to the channel). Three worlds from one design (`design.json`), built, laid and run alike by
`build_world.py` and `tools/pixel_mode.py`: `which_way.json` (both gaps open, the channel),
`one_gap.json` (the lower gap closed, the channel's walls standing) and `two_gaps.json` (both gaps
open, no channel: the two slits as shipped). The blind `expectation.json` was written by the builder
from the design before any lay and never touched after; the reading below is `tools/run_inputs.py`'s
output read per region (the `credit` lines, the clicks, labelled NODEREADER; the shares the `click`
lines' window inflows, a lattice reading beside them, labelled so); a miss is a finding by name and
never an adjustment of the blind.

## The blind (expectation.json)

1. The screen's regions behind the channel's lower wall (`screen_0` to `screen_3`, the rows 0 to 15)
   see nothing: 0 clicks exactly, shadowed by two faces.
2. The channel's clicks are the lower gap's quanta, half the two gaps' blind total (273 / 2 = 136.5,
   the gaps equal and the packet symmetric about the wall's centre), and the screen's clicks in the
   which-way world are down by them (136.5), within three times the draw's scatter.
3. The decisive comparison: the which-way world's screen row equals the one-gap world's screen row
   within the draw's scatter (the screen cannot tell the lower gap open and read from the lower gap
   closed; the two-slit interference term is gone exactly when the way is known), and both differ from
   the two-gaps world's row at the two slits' minima and maxima (the regions 4, 6 and 8).
4. A crude Huygens row per world for the shape and no fence: `two_gaps` [31.3, 31.9, 21.1, 4.3, 7.8,
   37.6, 43.5, 14.1, 2.1, 16.7, 30.4, 32.2]; `one_gap` and `which_way` [0, 0, 0, 0, 0, 11.5, 40.0,
   10.2, 11.1, 32.9, 28.2, 12.3] (the upper gap with its image in the channel's upper wall).
5. One quantum one click per record: every credit moves the count by 1 and the count left falls by one
   per click; the clicks never exceed the record's count.

## The reading (branch draw-tests, 2026-10-03, about 02:10 UTC, the seed 24 of the design)

| region | two_gaps clicks | two_gaps share | one_gap clicks | one_gap share | which_way clicks | which_way share |
| --- | --- | --- | --- | --- | --- | --- |
| screen_0 | 23 | 20.5 | 0 | 0.0 | 0 | 0.0 |
| screen_1 | 18 | 19.5 | 0 | 0.0 | 0 | 0.0 |
| screen_2 | 34 | 26.8 | 0 | 0.0 | 0 | 0.0 |
| screen_3 | 13 | 16.4 | 0 | 0.0 | 0 | 0.0 |
| screen_4 | 5 | 9.4 | (the channel) | | (the channel) | |
| screen_5 | 35 | 40.4 | 9 | 14.6 | 15 | 13.7 |
| screen_6 | 52 | 47.4 | 42 | 35.2 | 34 | 35.1 |
| screen_7 | 19 | 14.4 | 17 | 14.6 | 6 | 14.4 |
| screen_8 | 9 | 12.4 | 28 | 22.2 | 29 | 22.4 |
| screen_9 | 27 | 26.6 | 19 | 18.8 | 15 | 18.7 |
| screen_10 | 22 | 21.4 | 9 | 14.3 | 18 | 14.2 |
| screen_11 | 21 | 23.2 | 15 | 19.4 | 14 | 19.5 |
| which_way | | | | | 145 | 138.3 |
| N | 278 | | 139 | | 276 | |

The shares are the window inflows in whole quanta (the inflow over 3 den T), a lattice reading;
the clicks are the measurement.

1. The shadow: `screen_0` to `screen_3` read 0 clicks and 0 share in both worlds with the channel.
   PASS, exact.
2. The channel: 145 clicks against the blind's 136.5 (one scatter of 8.3 above); the which-way
   screen 131 against 136.5; the sum 276 against the two gaps' 278. PASS within the scatter.
3. The decisive comparison: the which-way screen row [15, 34, 6, 29, 15, 18, 14] against the
   one-gap row [9, 42, 17, 28, 19, 9, 15] over the regions 5 to 11, two draws at the same shares (the
   shares agree within one quantum region by region: 13.7 against 14.6, 35.1 against 35.2, 14.4
   against 14.6, 22.4 against 22.2, 18.7 against 18.8, 14.2 against 14.3, 19.5 against 19.4), their
   chi-square distance 11.1 on 7 degrees (the 1 percent band reaches 18.5). PASS: the screen reads
   the lower gap open and read exactly as it reads the lower gap closed. Against the two-gaps row
   [35, 52, 19, 9, 27, 22, 21]: the two slits' minimum at the region 8 (9 clicks, the share 12.4) is
   filled (29 and 28 clicks, the share 22.4 and 22.2) and the central maximum at the region 6 (52,
   the share 47.4) is down (34 and 42, the share 35); the visibility about the regions 6 and 8 falls
   from (52 - 9) / (52 + 9) = 0.70 to (34 - 29) / (34 + 29) = 0.08. PASS: the two-slit fringes are
   gone when the way is known.
4. The crude Huygens rows: `two_gaps` misses the engine's shares by up to ten at the edges (31.3
   against 20.5), as the design says; `which_way` and `one_gap` miss at the regions 8 and 9 (11.1
   against 22.4, 32.9 against 18.7): the point-source sum with one mirror is no model of this lattice
   (the board's open faces reflect too, the gap's three Nodes are no point sources at lambda = 8 and
   the channel guides). A FINDING of the blind's crude row, by name, and no fence; the shape, the
   two-gap fringes against their absence, reads as predicted.
5. One quantum one click per record: every credit's count is 1 and the count left falls by one per
   click in every world (276, 139 and 278 clicks of a record of 1,989 quanta laid). PASS.
6. The two-gaps world reads the shipped gate's numbers bit for bit, N = 278 and the row [23, 18, 34,
   13, 5, 35, 52, 19, 9, 27, 22, 21] (the shipped world's bare region `gap` left out changes no
   number). PASS.

The test `tests/test_the_draw.py::test_the_which_way_world_reads_as_the_one_gap_world_and_the_fringes_are_gone`
builds the three worlds from the design, runs them and asserts 1, 2, 3, 5 and 6; 4 is printed and
fenced by nothing.

## What is not built, by name

A which-way NodeReader that absorbs without a channel (the engine's only absorber is a receding face);
the Huygens row by the law's own real line (the two slits' design has the advisor's row from it); a
second seed's reading (one seed, the design's).

## The readings' sources (the owner's word of 2026-10-03, 10:08 Israel)

Every number of the reading above is the NodeReader's: the clicks are the `credit` lines' counts per
region and the shares are the `click` lines' window inflows over 3 den T, both lines the NodeReader's
report by the engine's label (ENGINE.md section 5, `reports.click` and `reports.credit`; the folder's
own words call the shares a lattice reading beside the clicks, a stricter label than the engine's).
No number is read from a Node. The lines carry the board's `interval` and the `window` in board intervals
and nothing of the NodeReader's own clock. The crude Huygens rows of item 4 are the design's.

## On the lay without the uniform mode, 2026-10-04 (branch click-share-fix, PR #1862)

The packet lay's uniform mode (the experimenter's bug report, #1827 comment 5975131359; ALGEBRA.md, The
packet lay, the sentence of 2026-10-04): the charge line's sums over the board at the lay were 0 and
-24,442 for now and before, a velocity of the uniform mode that Rule3 carries exactly, the level's mean
growing by 11 per interval over the board; the fix takes the uniform content out of each level at the
lay, so both sums are 0, and the lay's count moves from 1,998 to 1,805 at the world file's amplitude
1,328, the design's number; 996 the largest level the mode file lays under the envelope (the amplitude
the design's number, the count a reading; R252). The three worlds re-run on the branch, the
blind untouched, the seed 24 of the design (`tools/run_inputs.py`, the clicks per region from the
output files as `tests/test_the_draw.py` reads them, NODEREADER):

| region | two_gaps clicks | one_gap clicks | which_way clicks |
| --- | --- | --- | --- |
| 0 to 4 (shadowed) | 28, 15, 24, 18, 7 | 0, 0, 0, 0, 0 | 0, 0, 0, 0, 0 |
| 5 | 37 | 14 | 13 |
| 6 | 44 | 36 | 32 |
| 7 | 13 | 9 | 16 |
| 8 | 13 | 25 | 19 |
| 9 | 25 | 16 | 25 |
| 10 | 24 | 16 | 9 |
| 11 | 22 | 19 | 13 |
| N | 270 | 135 | 269 (the screen 127, the channel 142) |

The shadowed regions 0 exactly (PASS); the channel 142 against the blind's 136.5 within the draw's
scatter (PASS); the which-way screen against the one-gap row, one draw against another at the same
shares, chi-square 8.1 on 7 regions (PASS); the two slits' minimum at the region 8 read as the one gap's
within the scatter (19 against 25) and above the two gaps' 13, the visibility about the regions 6 and 8
below half the two slits' (PASS); the two-gaps row the two slits' gate row at this lay, N 270 against the
blind's 273. The night's table above stands as history at its commit.

## The statement, 2026-10-04 (main d00aa9e; two hands, the advisor's #1827 comment 5976031061 and the mathematician's 5976051758)

When everything that passes the lower gap is credited in the channel, the screen reads the lower gap
open and read as it reads the lower gap closed, two draws at the same shares, and both differ from the
two gaps' row at the two slits' extrema: the two-slit interference term is gone when the way is known
(the experimenter's statement, #1827 comment 5975980838 item 1; the advisor's (a) to (d)). The
statement does not say the screen is flat: the one gap's own row has its minimum near the region 8
(the gap's diffraction with the channel's upper wall as its image), so the which-way row's visibility
0.25 about the regions 6 and 8 is the one gap's shape and no remnant of the two slits' interference;
and it does not say the way was measured: the channel is a declared NodeReader that credits
everything passing the lower gap.

The fence is the test's and no wider (`tests/test_the_draw.py`, the which-way test): the shadowed
regions 0 exactly; the channel and the which-way screen each within three scatters (24.8) of the
blind's 136.5; the two rows' chi-square over the regions 5 to 11 under the one percent band 18.5 on 7
degrees (the reading 8.1 at the seed 24); the region-8 minimum above the two gaps' and within three
scatters of the one gap's, the scatter of the difference of two draws at the counts a and b being
sqrt(a + b) (the test's |a - b| < 3 sqrt(a + b); 19 against 25, the two gaps' 13; the mathematician's
word, 5976051758 (b)); the visibility about the regions 6 and 8 under half
the two slits' (0.25 against 0.54); one quantum one click exact. The chi-squares against the two-gaps
row (24.0 and 19.5) are the reading and no fence.

The two rows over thirty seeds (the advisor's (d); the world's generator at each seed, `credit.state`,
the seed 24 reproducing the rows above; the worlds and the blind untouched; LATTICE over the seeds,
each seed's rows NODEREADER): the which-way screen row against the one-gap row, two draws at the same
shares, chi-square on 7 degrees per seed [8.1, 2.8, 10.5, 4.6, 3.0, 6.3, 7.8, 15.5, 5.9, 3.1, 3.4, 5.8, 7.4, 1.4, 4.8, 6.4, 10.2, 11.8, 11.5, 3.7, 5.5, 7.1, 3.7, 7.2, 3.3, 1.1, 5.6, 4.4, 9.2, 9.1], the mean 6.33 against the expectation 7 (the
scatter 3.35 against sqrt 14 = 3.74), none above the one percent band 18.5; the channel 135.0 on the mean against the
blind's 136.5 (the seeds' least 116 and most 144); the shadowed regions 0 at every
seed in both worlds; N 269 and 135 at every seed (N is the shares', the draw places it). The one seed's
8.1 is the folder's fence, the thirty seeds' mean its reading beside it.

## The gate's table

Every row is a reading of the experimenter's run on the current tree (main d00aa9e, 2026-10-04), re-run and
compared bit for bit by `tools/reading_gate.py`: the label the reading's own (NODEREADER for the credit
lines' clicks and the trials' coincidences, LATTICE for the verdict, the intervals, the line counts, the
end's books and the back-in-time pass), the world the folder's file, `by` the tool that re-runs it, the
reading in the gate's words and the value as its report prints it.

| label | world | by | reading | value |
| --- | --- | --- | --- | --- |
| LATTICE | which_way.json | run_inputs | verdict | LAWFUL |
| LATTICE | which_way.json | run_inputs | intervals | 130 |
| NODEREADER | which_way.json | run_inputs | clicks | 269 |
| NODEREADER | which_way.json | run_inputs | clicks screen_0 | 0 |
| NODEREADER | which_way.json | run_inputs | clicks screen_1 | 0 |
| NODEREADER | which_way.json | run_inputs | clicks screen_2 | 0 |
| NODEREADER | which_way.json | run_inputs | clicks screen_3 | 0 |
| NODEREADER | which_way.json | run_inputs | clicks screen_5 | 13 |
| NODEREADER | which_way.json | run_inputs | clicks screen_6 | 32 |
| NODEREADER | which_way.json | run_inputs | clicks screen_7 | 16 |
| NODEREADER | which_way.json | run_inputs | clicks screen_8 | 19 |
| NODEREADER | which_way.json | run_inputs | clicks screen_9 | 25 |
| NODEREADER | which_way.json | run_inputs | clicks screen_10 | 9 |
| NODEREADER | which_way.json | run_inputs | clicks screen_11 | 13 |
| NODEREADER | which_way.json | run_inputs | clicks which_way | 142 |
| LATTICE | which_way.json | run_inputs | lines click | 1062 |
| LATTICE | which_way.json | run_inputs | lines credit | 269 |
| LATTICE | one_gap.json | run_inputs | verdict | LAWFUL |
| LATTICE | one_gap.json | run_inputs | intervals | 130 |
| NODEREADER | one_gap.json | run_inputs | clicks | 135 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_0 | 0 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_1 | 0 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_2 | 0 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_3 | 0 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_5 | 14 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_6 | 36 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_7 | 9 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_8 | 25 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_9 | 16 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_10 | 16 |
| NODEREADER | one_gap.json | run_inputs | clicks screen_11 | 19 |
| NODEREADER | one_gap.json | run_inputs | clicks which_way | 0 |
| LATTICE | one_gap.json | run_inputs | lines click | 888 |
| LATTICE | one_gap.json | run_inputs | lines credit | 135 |
| LATTICE | two_gaps.json | run_inputs | verdict | LAWFUL |
| LATTICE | two_gaps.json | run_inputs | intervals | 130 |
| NODEREADER | two_gaps.json | run_inputs | clicks | 270 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_0 | 28 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_1 | 15 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_2 | 24 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_3 | 18 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_4 | 7 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_5 | 37 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_6 | 44 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_7 | 13 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_8 | 13 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_9 | 25 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_10 | 24 |
| NODEREADER | two_gaps.json | run_inputs | clicks screen_11 | 22 |
| LATTICE | two_gaps.json | run_inputs | lines click | 1086 |
| LATTICE | two_gaps.json | run_inputs | lines credit | 270 |
| LATTICE | which_way.json | back_in_time | intervals 40 | MATCH |
