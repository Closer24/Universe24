# Four candidate new rows of the comparison table, the pins before any run: the no-signalling marginals (R1), the Sagnac ratio (R2), Malus at three new settings (R3) and the round-trip Doppler (R4) (the New Rows Scout, 2026-09-23; step 1, docs only, no run)

The Boss's order of 2026-09-23 (about 02:3xZ, by Routine; the owner's
word that the experiments are to be arranged, the Boss's record 1173, and
the scout's table, record 1168, both cited by the Boss's numbering and
unread here: the fetched log ends at record 1163): step 1 on the branch
`new-rows` off `origin/main` at `beae0a4` (PR #982 merged), docs only, one
commit, then hold. For each of the four rows: the claim it stands beside,
the chain click to click by kind with its code lines, nature's number with
its source, the pin as an integer or an exact fraction before any run, the
falsifier, the world, the HOST cost, and whether the law as built makes it.
The worlds under existing keys are written beside this file by
[new_rows_worlds.py](new_rows_worlds.py) into [worlds/](worlds/), validated
at load through the shipped loader and never run; the pins are its print
[new_rows_pins.out](new_rows_pins.out) and its file
[new_rows_pins.json](new_rows_pins.json). Nothing here runs, nothing here
edits `docs/NATURE.md` (one writer per shared interface: the two rows of R1
and R4 stand below as a PROPOSAL block for the Register Architect to fold
on his branch after PR #979 merges).

Notation ([the workflow's rule](../../../skills/workflow.md#notation-every-symbol-named-its-kind-shown-the-model-owner-2026-09-21-record-184)):
a scalar plain, a vector in bold lowercase (**p** the momentum vector),
a Greek letter written as a word and named at its first use (beta, the
speed as a fraction of c; gamma, the Lorentz factor). Every number is
labelled by kind: DETECTOR (a click line's stamped count, a cell's count),
GAMEBOARD (the host's view: a tick, a row's column), COMPUTATION (the
algebra's, before any run), CONVERSION (a ratio formed from readings by a
named definition), HOST (the machine's cost); NATURE marks the thing
compared with. The three statuses of the comparison table since the
Boss's record 1166 (unread here, as relayed): agrees (with the number);
disagrees (with the number); not predicted (with the missing piece). A
new row enters as agrees or disagrees only, and may stand beside an old
row of the same claim.

**What the four rows share.** Each is a count of clicks or a ratio of two
counts at a declared detector, read off the stamped lines (`clock`,
`record`, `node`, `number`; `nature_beam.py` :5177-5179 and :6322, the
world key `clock_stamp`), the tick read by nothing; each is exact on the
law's integers (the rungs, the tables, the flight table) with no shell
mean, no tick and no body's own record in the chain, which is what the
three measured passes of Table 2 share
([WHAT_IS_MISSING.md section 0b](../fail_rows/WHAT_IS_MISSING.md#0b-the-rows-that-passed-and-why-by-the-algebra));
and in each the law as built makes the prediction (no key of a
hypothesis; the four worlds' keys are `boundary`, `clock_stamp`, a lamp's
`directions` and `phase_window`, all on `main`). Parameters added: 0 in
every row.

**One correction to the scout's table (record 1168).** R3's pin at 28.125
degrees is 199 of 256, not the 200 the table said: the click's rung is
`b = (2 W C + T) // (2 T)` on the cells' own total T = C'^2 + S'^2
(`amplitude.py` :241, `rungs`; BEAM_LAW note 46), not on 65 536; the
table's 246 and 177 at 11.25 and 33.75 degrees stand. The tables' rounding
is largest at 22.5 degrees (+0.0019, the registered row 9), not at 28.125
(-0.0004).

## 1. R1: the no-signalling marginals of the pair (the count form), beside row 1c (the order form) and row 1a

**The claim it stands beside.** Row 1c (the paper's Table 2, "no
signalling in the order": FAIL, the wheel a counter) and row 1a (the CHSH
sum, PASS). R1 is the count form of the same claim: each party's marginal
is independent of the other party's setting. It stands beside 1c as the
Boss's rule allows (a new row beside an old row of the same claim).

**The chain click to click, by kind.**

1. Declaration: the pair world of series L (`examples/events/amplitude/bell_0_8.json`,
   `bell_0_24.json`, `bell_16_8.json`, `bell_16_24.json`; N = 64, the lamp's
   `branches` `[[0, 1], [3, 1]]` on two arms, the counters' windows the
   settings 0, 16 and 8, 24). The arrangement, not the number.
2. GAMEBOARD: the lamp births one record of rank 2 per self-creation, one
   row per label per arm (`nature_beam.py` :6066, the `birth` line; the
   ladder's u = the birth ordinal mod N).
3. GAMEBOARD: the two arms fly on their digital lines by the flight table
   (`direction_flight`, `nature_beam.py` :909; ALGEBRA.md 4.1).
4. The one gather of the one record from both settings at its completion
   interval (`gather_records`, `nature_beam.py` :6537; P6, the law's one
   non-local operation): the joint weight J(o_A, o_B) = sum over l of
   U_a[o_A][l] U_b[o_B][l] on the half-angle tables (`amplitude.py` :191,
   `half_angle`), the cell's offer R = J^2 (Theorem 4, ALGEBRA.md 4.8).
5. COMPUTATION inside the click: the rungs over the four cells
   (`amplitude.py` :241 `rungs`, :275 `cell_of`) and the wheel's u choose
   one cell; the record is deleted.
6. DETECTOR: the two counters' click cells over the 64 births
   (`nature_beam.py` :4333 and :5536, the `click` lines): the cells
   `pair.chsh.<a>_<b>.counts` of `amplitude/expectations.json`, replayed at
   head by the tests.
7. CONVERSION: the first party's + fraction at the setting a under the
   second's b, and under b'; their difference. The marginal is the sum of
   two cells over the births.

Theorem 5 (ALGEBRA.md 4.9; the click frame section 10 (2)): the first
party's outcome is + exactly for u < N/2 and - for u >= N/2 for every (a,
b) and every N; the second party's count of + is exactly N/2 unless 2 N
R(+, +) / C_K is an odd integer (a tie), and no tie occurs at N = 64 at the
CHSH labels. The law as built makes it: yes.

**Nature's number.** NATURE: the difference of one party's + fraction
between the other party's two settings is 0 within the statistical error,
in every Bell test that reports its marginals; the loophole-free test of
Hensen et al. 2015, Nature 526, 682 (the register's source of row 1a; the
marginals in its supplement, to verify against the source); Weihs et al.
1998, Phys. Rev. Lett. 81, 5039 (to verify against the source). The
register's rule (c): the row enters with its figure verified or marked
"to verify" as here; no precision is invented.

**The pin.** Registered, DETECTOR, repeated and not recomputed
(`amplitude/expectations.json`, `pair.marginal` = 32 and `pair.chsh`):
at every one of the four settings pairs the cells are 27, 5, 5, 27 (or 5,
27, 27, 5 at (0, 24)), so the first party's + count is 27 + 5 = 32 of 64
and the second party's is 27 + 5 = 32 of 64 at (0, 8), (0, 24), (16, 8) and
(16, 24); the difference between the other party's settings is 0 exactly
(COMPUTATION from the cells: 32 - 32 at each). Tolerance: none needed (the
count is exact by Theorem 5 off a tie); the comparison's tolerance is
nature's statistical error on 0.

**The falsifier.** Any marginal off 32 by one at N = 64 (a rung tie, which
Theorem 5 excludes at these labels), or a difference between the other
party's two settings at any grain of the seven registered (`pair_n` at N =
512 to 16384, the same cells' identity).

**The world.** Existing: the four pair worlds of series L and the seven
grains; nothing to write. HOST: 0 minutes (registered; the tests replay
the cells at head).

**What a FAIL would and would not show.** The chain, not the number: a
marginal off N/2 would refute step 5's rung arithmetic at a tie the
computation missed (Theorem 5's tie clause), or step 4's gather reading a
setting on the wrong arm; it would not touch the correlation E(a, b) of
row 1a, which is a difference of the same cells, nor the order channel of
row 1c, which is the wheel's sequence and not the counts. It would show
nothing about nature's no-signalling, which the theorem makes exact.

## 2. R2: the Sagnac ratio on a closed loop, beside rows 4a, 4b and 5b (the kinematics of a moving thing)

**The claim it stands beside.** Rows 4a, 4b and 5b (the moving body's
clock, the moving lamp's redshift, the arms' anisotropy: the kinematics of
a moving thing, all FAIL on the law at second order by the absent r =
sqrt(1 - v^2)). R2 is the r-free member of the same kinematics: the
difference of the two counter-propagating arrivals at one moving detector
on a closed loop, as a ratio of that detector's own counts, which reads
nothing of r (the click frame section 2 (a); ALGEBRA.md 5.1, the r-free
lines). It stands beside them as the Boss's rule allows, and it is the
one member of the family the law can meet at every order. The same
family and NOT the same observable: R2 is r-free by construction and
reads nothing of the second order where rows 4a, 4b and 5b fail, so the
paper must never list it as evidence on those rows (the physics-rule
reviewer's line on PR #988).

**The chain click to click, by kind.**

1. Declaration: the cart of RUN_4AB (`docs/designs/fail_rows/worlds/cart_k3_law.json`,
   series O's numbers) with three declarations changed and nothing added:
   the x axis periodic (`boundary: {"x": "periodic"}`, the loop: a
   declaration of the arrangement, not of the number), the cart's lamp on
   both headings (`lamp.directions` `[[1, 0, 0], [-1, 0, 0]]`), the post and
   the source removed; the cart D of the family `cart` from x = 20 with the
   momentum p = Q S M / (k - 1) on +x (M = 4 202 496, S = 2^20), its table
   `measure` on its own family's rows; `clock_stamp` true; the bar 240 x 3
   x 3; 1500 intervals; k = 3, 5, 9, 17.
2. GAMEBOARD: the cart's lamp births one record per self-creation with
   one row on +x and one on -x, both carrying the cart's number and the
   birth's ordinal j, the `birth` line stamped with the cart's own count
   n_0(j) (`nature_beam.py` :6066; the lamp's count row `measured.py`
   :429, whose first remainder RUN_8BC 5 found: a lamp holding exactly K
   births nothing at its second self-creation, so the ordinals may skip
   one tick; the ratio below is per ordinal and reads nothing of it).
3. COMPUTATION, the law's pace: the cart steps one Link per k intervals
   on +x (`engine.py` :759 `_move`, the per-axis drive p / (Q S M + p) = 1 /
   k), v = 1 / k Links per interval; the rows fly at the heading's pace c =
   32 / 55 Links per interval (the flight table `direction_flight`,
   `nature_beam.py` :909; ALGEBRA.md 4.2), beta = v / c = 55 / (32 k).
4. GAMEBOARD: the +x row runs ahead of the receding cart around the loop
   (the wrap on the periodic axis, `nature_beam.py` :1411 and :1426, the
   coordinates mod the extent) and closes on it from behind at c - v: the
   return t_+ = L / (c - v) intervals after the birth, exactly in the mean
   (ALGEBRA.md 4.1, the accumulator's carries); the -x row meets the cart
   coming the other way at c + v: t_- = L / (c + v).
5. DETECTOR: the cart's `measure` on its own family stamps each return
   with its own count n_D and the row's ordinal j (`nature_beam.py` :4333,
   the `click` line with `clock`, `record`, `node`, `number` under
   `clock_stamp` :5179): two click lines per ordinal, n_+(j) and n_-(j).
6. CONVERSION: the ratio (n_+ - n_-) / (n_+ + n_- - 2 n_0) per ordinal over
   the window from the cart's count 60, and its mean; r cancels (the
   cart's own count is r times the interval at every step of the chain, r
   = 1 on the law; the ratio is the same under every r).
7. COMPUTATION, the closed form: (n_+ - n_-) / (n_+ + n_- - 2 n_0) = (1 / (c
   - v) - 1 / (c + v)) / (1 / (c - v) + 1 / (c + v)) = v / c = beta, exactly
   in the mean, r-free.

The law as built makes it: yes (the same arithmetic as RUN_4AB 1.2 steps 4
and 8, met at k = 3 and 5 within the lattice's meeting remainder, RUN_4AB
6.3; no key).

**Nature's number.** NATURE: the Sagnac effect. On a loop of perimeter L
moving at v the two counter-propagating arrival times at the moving
detector differ by 2 L v / c^2 at first order (the rotating ring's 4 A
Omega / c^2, A the loop's area, Omega the angular rate), and as a ratio of
the detector's own counts the difference over the mean is v / c exactly
in the moving-loop form, the same to all orders in Einstein's and in the
ether form (a ratio of one detector's own counts, r-free). Michelson,
Gale and Pearson 1925, ApJ 61, 140: the observed shift 0.230 +- 0.005
fringe against the computed 0.236 for the Earth's rotation, the ratio 0.97
+- 0.02 (to verify against the source); Sagnac 1913, C. R. Acad. Sci. 157,
708 and 1410 (to verify). Every modern ring-laser gyroscope reads the same
form.

**The pin, before any run** (COMPUTATION, `new_rows_pins.out`; c = 32 / 55
from the engine's own flight table on the loaded world; L = 240):

| World | k | beta = 55 / (32 k) | t_+ = L / (c - v) intervals (GAMEBOARD) | t_- = L / (c + v) | ordinals with both returns inside 1500 | the ratio's pin (DETECTOR) | the band on the ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sagnac_k3` | 3 | 55/96 = 0.57292 | 39600/41 = 965.85 | 39600/151 = 262.25 | 534 | 55/96 | 0.0077 (4.72 counts per end) |
| `sagnac_k5` | 5 | 11/32 = 0.34375 | 4400/7 = 628.57 | 13200/43 = 306.98 | 871 | 11/32 | 0.0144 (6.72 per end) |
| `sagnac_k9` | 9 | 55/288 = 0.19097 | 118800/233 = 509.87 | 118800/343 = 346.36 | 990 | 55/288 | 0.0250 (10.72 per end) |
| `sagnac_k17` | 17 | 55/544 = 0.10110 | 74800/163 = 458.90 | 224400/599 = 374.62 | 1041 | 55/544 | 0.0449 (18.72 per end) |

The band: the lattice's meeting remainder of RUN_4AB 6.3 (one hop of k
intervals plus one dwell of 55 / 32 intervals at each return, in the
cart's counts) over the sum of the two returns; the mean over the window's
ordinals narrows it. The pin is the exact fraction; a mean inside the
band meets it; the falsifiers below are stated against the band.

**The falsifier.** The mean ratio off beta by more than the band (at k =
3: outside 0.565 .. 0.581); the two returns of one ordinal not both
stamped at the cart (a row lost at the wrap, or the cart's `measure` not
reading its own family from both Ports); the returns' spacing not t_+ and
t_- within the remainder; the books unbalanced at any tick (GAMEBOARD, the
check). A ratio at beta under the law says nothing of r and is not a
reading of rows 4a, 4b or 5b, which stay as they are.

**The world.** New, under existing keys, written by `new_rows_worlds.py`:
`worlds/sagnac_k3.json`, `sagnac_k5.json`, `sagnac_k9.json`,
`sagnac_k17.json`, each validated at load by the shipped loader
(`load_world`, the model ids `beam-new-rows-sagnac-k<k>-v1`), none run.
The reviewer's items, named for his gate: the periodic axis under a
hopping body (`nature_beam.py` :3351-3354, `adjacent_node` with
`world.periodic`; a body wraps as a row does) and a lamp's two directions
on one self-creation (the amount per direction `min(by_clock(rate), held
// (h s))`, the cost 2 per self-creation on the cart's 8192, 3000 over
1500 intervals, M falling by 0.07 percent: the pace's drift 3 x 10^-4,
inside the band). The cart's count is its own age, one per interval
(`clock_stamp`); this world declares `suspension` 0, so it owes no count
for the crowd at its Node (`count_owed` returns 0 at a zero numerator,
`engine.py` :157) and its count equals the tick in number; the ratio is a
ratio of that one clock's stamps, r-free at r = 1 by declaration, and a
world with a nonzero suspension would need `reads: presence` or the
returns' age stretch in its pin.

**HOST.** About 10 seconds per world on the register's timings (the cart
worlds 5 s for 600 intervals, RUN_4AB section 4); the four worlds under a
minute; the reader seconds.

**What a FAIL would and would not show.** The chain, not the number: a
ratio off beta beyond the band would show a rule the chain forgot at the
wrap (step 4: a row's return on a periodic axis not the accumulator's
line) or at the cart's own click (step 5: its `measure` reading one Port
only), never a rate r, since r cancels in step 6 under every value; a
missing return would show the wrap dropping a row. It would not touch
rows 4a, 4b or 5b, whose one-way readings carry r, nor row 4b's first
order, which is the same crossing count read at a rest detector. It could
not show anything of the second order in v, where the Sagnac ratio is the
same under every r and nature reads no difference.

## 3. R3: Malus at three new settings, beside row 9

**The claim it stands beside.** Row 9 (Malus's law, PASS: exact at 45 and
90 degrees, 219 of 256 at 22.5). R3 is the same claim at three settings
the register has not read, chosen where the tables' rounding was said to
be largest below 45 degrees and where it is nearly zero; a re-reading of
row 9's identity (ALGEBRA.md 4.12), so it does not add to the referee's
count of independent predictions; its worth is a rounding predicted
before the run at the tables' grain 1 / 256.

**The chain click to click, by kind** (the malus note's section 3, as
registered for row 9):

1. Declaration: `malus_22_5.json` as registered (the lamp of the family
   `light` on the wheel [159, 256], one row per self-creation on +x, born
   on label 0; the which-path `read` at x = 4 with no rotation before it,
   the whole beam on label 0; the `sum` set at x = 6 whose `phase_window`
   is the setting s), the setting the one declaration changed: 16, 40, 48
   (the angles 180 s / 256 = 11.25, 28.125, 33.75 degrees); N = 256, 300
   intervals, 256 births read (u = ordinal x 159 mod 256, every residue
   once).
2. GAMEBOARD: the lamp's `birth` line per self-creation (`nature_beam.py`
   :6066), the row's flight on the heading (`direction_flight` :909).
3. The which-path `read` at the first `sum` set (the design's 4.1): the
   cells split by the label; born on label 0, one cell.
4. COMPUTATION inside the click at the window s: the channels + and -
   weigh (256 C'[s])^2 and (256 S'[s])^2 on the half-angle tables of 2N
   (`amplitude.py` :191 `half_angle`; `phase_cosines(512)`,
   `phase_sines(512)`), the rungs b = (2 W C + T) // (2 T) on the cumulative
   weight C and the total T = (256^2)(C'^2 + S'^2) at W = 256 (`amplitude.py`
   :241 `rungs`, :275 `cell_of`; BEAM_LAW note 46).
5. DETECTOR: the cells 0+ and 0- over the records 1 to 256 (the `click`
   lines of the set `second`, `nature_beam.py` :4333), the counts the
   rungs' widths.
6. CONVERSION: the pass fraction, the cell 0+ over 256.

The law as built makes it: yes (no key; the entries in force since row
9).

**Nature's number.** NATURE: cos^2 theta (Malus 1809, the register's
citation of row 9, to verify the citation): 0.96194 at 11.25 degrees,
0.77779 at 28.125, 0.69134 at 33.75; times 256: 246.26, 199.11, 176.98.

**The pin, before any run** (COMPUTATION, `new_rows_pins.out`, the
engine's own tables):

| World | s | angle | C'[s], S'[s] | the rungs | the counts 0+, 0- (DETECTOR) | the pass fraction | cos^2 | the departure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `malus_s16` | 16 | 11.250 degrees | 251, 50 | 0, 246, 256 | 246, 10 | 246 / 256 = 0.96094 | 0.96194 | -0.00100 |
| `malus_s40` | 40 | 28.125 degrees | 226, 121 | 0, 199, 256 | 199, 57 | 199 / 256 = 0.77734 | 0.77779 | -0.00044 |
| `malus_s48` | 48 | 33.750 degrees | 213, 142 | 0, 177, 256 | 177, 79 | 177 / 256 = 0.69141 | 0.69134 | +0.00006 |

The departures are the tables' rounding at the scale 256 (the owner's
declared input, record 328), each below 1 / 256; the pin is the integer
count, met exactly or not at all.

**The falsifier.** A count off its integer by one (the rung arithmetic or
the wheel's coverage); a cell 1+ or 1- (a label the read did not keep on
0); the books not conserved at every tick; the 256 records not all
gathered by the tick 300 (the registered run gathered 289 of 299 born, the
last ten open: the reading is over the records 1 to 256, as row 9's).

**The world.** New, under existing keys, written by `new_rows_worlds.py`
from `malus_22_5.json` with the window's setting changed and the
catalog's two families (`light`, `counter`) inlined so that the file is a
portable input from this folder: `worlds/malus_s16.json`, `malus_s40.json`,
`malus_s48.json`, each validated at load (the model ids
`beam-new-rows-malus-s<s>-v1`), none run. The registered generator
(`amplitude/make_worlds.py`) is not edited: a new setting there would
change the shipped world list that `tests/test_amplitude_malus.py` pins.

**HOST.** Seconds per world (7 x 1 x 1 Nodes, 300 intervals; the
registered 22.5-degree worlds).

**What a FAIL would and would not show.** The chain, not the number: a
count off by one would refute step 4's rung on this total (the ladder's
nearest integer) or step 1's coverage of the residues by the wheel [159,
256], never cos^2, which the tables carry by declaration (the half-angle
tables at 1 / 256); a cell on label 1 would show the read at x = 4 not
keeping the label. It would not touch row 9's three exact fractions at 45
and 90 degrees, which carry no rounding.

## 4. R4: the round-trip (radar) Doppler off a receding transponder, beside rows 4a, 4b and 5b

**The claim it stands beside.** Rows 4a, 4b and 5b again (the kinematics
of a moving thing). R4 is the round trip k_AB k_BA = (1 + beta) / (1 -
beta) of the click frame (section 2 (a), the k-calculus), a ratio of the
cart's own counts that reads nothing of r under any r (ALGEBRA.md 5.1, the
r-free lines), read for the first time by RUN_4AB at k = 3 and 5 and in no
row of Table 2 (the table has the one-way 4b only). The same family and
NOT the same observable: R4 is r-free by construction and reads nothing
of the second order where rows 4a, 4b and 5b fail, so the paper must
never list it as evidence on those rows (the reviewer's line on PR
#988).

**The chain click to click, by kind** (RUN_4AB 1.2 steps 7 to 12, as
registered):

1. Declaration: the cart worlds `cart_k3_law` and `cart_k5_law` of
   RUN_4AB (the post R fixed at x = 1 with `rerelease` on the cart's rows,
   the cart D from x = 20 at p = Q S M / (k - 1), its lamp on -x, its
   `measure` on its own family's returned rows; `clock_stamp` true; the key
   absent).
2. GAMEBOARD: the cart's rows born at its own counts j (the `birth` line,
   `nature_beam.py` :6066) fly -x to R at c: the arrival (1 + beta) j / r +
   const (the lamp moving away from R).
3. The post's `rerelease` line (`nature_beam.py` :2488, the pending rows;
   :5812-5815, the re-emission at R's next self-creation on +x, the record
   kept, the ordinal j carried).
4. GAMEBOARD: the re-emitted row flies +x and closes on the receding cart
   at c - v.
5. DETECTOR: the cart's `click` line of the returned row, `clock` = n_D at
   the return, `record` the cart's own ordinal j (`nature_beam.py` :4333,
   :5179).
6. CONVERSION: q = (the cart's counts apart between two returns) / (the
   cart's ordinals apart between the births they carry) over the window
   from the cart's count 100: k_AB k_BA, r-free.
7. COMPUTATION: q = (1 + beta) / (1 - beta) = (32 k + 55) / (32 k - 55):
   151 / 41 at k = 3, 43 / 21 at k = 5.

The law as built makes it: yes (read on the law's worlds; the identity's
worlds read the same form at their own beta).

**Nature's number.** NATURE: the two-way Doppler (1 + beta) / (1 - beta)
to all orders, the same in Einstein's and in the ether form, the form
every radar and every two-way spacecraft tracking reads; no single
dimensionless figure from one paper is at hand (Ives and Stilwell 1938
read the one-way shift, not this), so R4 enters as a FORM row, as row 11b
entered by a pin, until a nature source is named under the register's
rule (c).

**The pin and the reading** (registered by RUN_4AB 6.3, DETECTOR, repeated
here and not recomputed; `new_rows_pins.out`):

| World | read | over (counts; returns) | the pin | counts off; the remainder per end | against the band as pinned (2 / W) | against the preregistration's band |
| --- | --- | --- | --- | --- | --- | --- |
| `cart_k3_law` | 3.70833 | 445; 120 | 151 / 41 = 3.68293 | +3.05; 8.44 | FAIL | PASS |
| `cart_k5_law` | 2.05372 | 497; 241 | 43 / 21 = 2.04762 | +1.48; 10.44 | FAIL | PASS |
| `cart_k3_key` | 4.77419 | 296; 62 | 4.70819 | +4.09; 6.35 | FAIL | FAIL (off by 0.002) |
| `cart_k5_key` | 2.30769 | 450; 195 | 2.30201 | +1.11; 9.07 | FAIL | PASS |

Every miss lies inside the lattice's meeting remainder (RUN_4AB 6.3: one
hop plus one dwell per end, a return adding the birth's count and the
post's next self-creation), so the closed form is met and the FAILs are
the version-1 band's; the row's tolerance is the remainder per end over
the window, stated so before the row enters, and the number the row
carries is the law's worlds' 3.708 for 151 / 41 and 2.054 for 43 / 21.

**The falsifier.** The ratio off (1 + beta) / (1 - beta) beyond the
remainder (a re-emission not keeping the record, a packet not passing
one Node per interval at the table's pace); already read: none.

**The world.** Existing (`docs/designs/fail_rows/worlds/cart_k3_law.json`,
`cart_k5_law.json`, run on 2026-09-23 by RUN_4AB step 2). HOST: 0 minutes.

**What a FAIL would and would not show.** The chain, not the number: a
round trip off its closed form would show step 3's re-emission not
keeping the ordinal or step 4's closing not at c - v, never the rate r,
which the round trip carries under no value (the check RUN_4AB used to
know its two one-way factors were read on one world). It would not touch
the one-way rows 4a and 4b, whose ratio k_BA / k_AB is where r shows.

## 5. PROPOSAL: the two rows of R1 and R4 for `docs/NATURE.md`, in the register's column order (not applied here)

For the Register Architect to fold on his branch after PR #979 merges;
the columns as the register's table has them (Row; the dimensionless
observable; nature's value and its one source; the model's registered
reading (world; register key; value); grain; verdict with the number),
the verdict written in the three statuses of record 1166 (agrees;
disagrees; not predicted). The row numbers are proposals beside the
rows they stand with (1c and 4b); the Architect numbers them.

| Row | The dimensionless observable | Nature's value and its one source | The model's registered reading (world; register key; value) | Grain | Status, with the number |
| --- | --- | --- | --- | --- | --- |
| 1d (beside 1c) | The no-signalling marginals of the pair, the count form: each party's + fraction at its setting, and its difference between the other party's two settings | 0 within the statistical error, in every Bell test that reports its marginals; the loophole-free Hensen et al. 2015, Nature 526, 682 (the marginals in the supplement; to verify against the source); Weihs et al. 1998, Phys. Rev. Lett. 81, 5039 (to verify against the source) | `examples/events/amplitude/bell_0_8.json`, `bell_0_24.json`, `bell_16_8.json`, `bell_16_24.json`; `amplitude/expectations.json` `pair.marginal` = 32 and `pair.chsh.*.counts` 27, 5, 5, 27 (5, 27, 27, 5 at (0, 24)): each party's + count 32 of 64 at every setting pair (DETECTOR, replayed at head by the tests); the difference between the other party's settings 0 exactly (COMPUTATION from the cells); Theorem 5 (ALGEBRA.md 4.9) | N = 64; K = 15 x 2^20: not under the one set (K), as row 1a | agrees: 0 against 0, exact, by Theorem 5 (ALGEBRA.md 4.9): a theorem of the click's form, a consistency check the law must pass and not an independent prediction, outside the referee's count of predictions; the tolerance nature's statistical error on 0; the same at the seven grains 512 to 16384 (`pair_n`) |
| 4c (beside 4b) | The round-trip Doppler off a receding transponder, the cart's counts apart between two returns over its ordinals apart between the births they carry, (1 + beta) / (1 - beta), r-free | (1 + beta) / (1 - beta) to all orders, the two-way form of every radar and two-way tracking, the same in Einstein's and in the ether form; a FORM row until a nature source is named (the register's rule (c)), as row 11b entered by a pin | `docs/designs/fail_rows/worlds/cart_k3_law.json`, `cart_k5_law.json`; RUN_4AB.md 6.3 (`run_4ab_readings.json`, `runs.<world>.readings.round_trip`): 3.70833 over 445 counts (120 returns) for the pin 151 / 41 = 3.68293 at k = 3 (beta 55/96), 2.05372 over 497 (241 returns) for 43 / 21 = 2.04762 at k = 5 (beta 11/32) (DETECTOR); under the key 4.774 for 4.708 and 2.308 for 2.302 at the identity's beta (DETECTOR, the hypothesis's, beside) | N = 64; K = 4 202 496, S = 2^20 (series O's numbers): not under the one set (K) | FORM row, outside the count until a nature source with a number is named (the register's rule (c)): the law's worlds read 3.708 and 2.054 for 151 / 41 and 2.048 [43 / 21], +3.05 and +1.48 counts off the closed form over the window, outside the version-1 band 2 / W as pinned in RUN_4AB (FAIL there) and inside the preregistration's band in ordinals and the meeting remainder of 8.44 and 10.44 counts per end (RUN_4AB 6.3); reads nothing of r, so it changes nothing in rows 4a, 4b and 5b |

## 6. The three tests, on the two new arrangements (nothing enters the law)

Nothing here is a rule: no identity, no key, no verb. R2's world declares
a periodic axis and a lamp's two directions (declarations of the
arrangement on entries in force); R3's a window's setting. Generic: no
family name read by any step. Vector: the translation of the accumulators
(the flight, the drive, the lamp's count), the bilinear form at the click,
the division with the remainder kept (the rungs); no root, no float.
Local: each click reads its own Node's arrivals; nothing kept at a Node.

## 7. Links

- The scout's table: the Boss's record 1168 (unread here); the owner's
  word, record 1173; the three statuses, record 1166.
- [ALGEBRA.md](../../ALGEBRA.md) (on main since PR #982, beae0a4, the
  merge base): [4.9, Theorem 5](../../ALGEBRA.md#4-the-exact-identities-one-line-each-and-the-link-to-the-proof),
  4.12 (Malus), [5.1, the r-free lines](../../ALGEBRA.md#51-the-click-theorem-lorentzs-factors-from-the-clicks); [the click frame](../click_frame/DERIVATION.md)
  sections 2 to 4; [RUN_4AB.md](../fail_rows/RUN_4AB.md) 1.2, 3.2, 6.3;
  [RUN_8BC.md](../fail_rows/RUN_8BC.md) 5 (the lamp's first remainder);
  [the malus note](../malus/NOTE.md) section 3; [WHAT_IS_MISSING.md](../fail_rows/WHAT_IS_MISSING.md)
  0b; [NATURE.md](../../NATURE.md) rows 1a, 1c, 4a, 4b, 5b, 9, 11b.
- The files beside this one: [new_rows_worlds.py](new_rows_worlds.py),
  [new_rows_pins.json](new_rows_pins.json), [new_rows_pins.out](new_rows_pins.out),
  [worlds/](worlds/).
