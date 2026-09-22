# The moving detector, a cart with a click: the design, with the pins written before any run (the chief physicist, 2026-09-22)

The model owner's word of 2026-09-22 (06:33Z, by voice, through the chief
physicist, record 816 of [docs/LOG_2026-09-20.md](../../LOG_2026-09-20.md)):
"we no longer need a wall; we need a cart with a click", after record 745
(no wall is needed; define the two worlds and what a click is) and record
762 (a moving detector can be built). The Boss's frame (06:45Z): one
writer, the chief physicist; algebra first, the run only after, and only
on the owner's word (records 762 and 799); step 1 this design, docs only;
step 2 the physics-rule reviewer's ADMISSIBLE; step 3 the build of what
the pins need, under a key, off by default; step 4 the run on the owner's
word. Every number below is a closed form of the law as it stands on
`main` or a registered reading named by its kind (DETECTOR or GAMEBOARD);
nothing is fitted and no pin moves after a run.

The sources this design stands on, read first: the Einstein Mathematician's
`docs/designs/einstein_outside/DERIVATION.md` (branch `einstein-outside` at
69382c31, PR #792, not yet on `main`; section 2, the conversion: Theorem 1 the place-to-place factor, Theorem 2 the radar
reading; section 3, Theorem 3 the quantum of the Outside step; II.1 to
II.5 the pins of the special theory), the click frame
[click_frame/DERIVATION.md](../click_frame/DERIVATION.md) (section 0 the
click theorem and the locality-Outside clause; section 4 the missing
direction `k_AB`, its world and its pins), and the Light Mathematician's
`docs/designs/light_outside/DERIVATION.md` (branch `light-outside` at 54c01a59,
PR #791, not yet on `main`; II.4, the
Doppler of a moving detector, `1 + z = 1 / (1 -+ v)`). The two words of
record 768 are used throughout: **Inside** is the GameBoard, where no one
measures; **Outside** is the game above the board, the detectors and their
clicks, which represents reality and is not reality.

## 1. The two worlds and what the cart is

**Inside.** Nodes on the cubic lattice, rows on them, the tick. A row of a
light family crosses one Link every `T_h / Q` intervals on an axis (the
flight table's pace, `c = Q / T_h = 32 / 55` Node per interval on the axis,
exact over whole Links; DERIVATIONS_BEAM 2.2 and the crossing rule, BEAM_LAW
note 48). A body of content M with the momentum p on one axis hops one Node
every time its drive accumulator, gaining p per self-creation against the
wall `Q S M + p`, reaches the wall (`main`'s per-axis drive, `engine.step_axis`;
the pace `p / (Q S M + p)` Nodes per self-creation, DERIVATIONS_BEAM 2.1).
A body's own count is its `age`, advanced at every self-creation and not at
an interval it owes to the crowd at its Node (`engine._suspend`; ENGINE.md,
"the clock of a measured event"); in no crowd it advances every interval.
The tick is GAMEBOARD and no detector reads it.

**Outside.** Detectors and clicks only. A click is a row's arrival at a
measured event whose table says `measure` for the row's family: one line on
the record with the Node, the family and the number of what arrived, and
the arriving record's identity, whose low 32 bits are the ordinal of the
birth at its lamp (`Measured.births`, ENGINE.md: "the event's number x
2^32 + the ordinal"), so every click carries the emitter's own count at the
emission, as the Einstein Mathematician's definition of the conversion
requires ("the emitter's count rides on the packet; the detector's count is
stamped at the click", section 2). A detector's velocity Outside is Nodes
apart over counts apart between two of its clicks (the click frame, section
0). LOCALITY OUTSIDE (the click frame, :53-69): every Outside passage is a
chain of clicks between neighbouring places; nothing is read at a place no
chain of clicks reaches.

**The cart.** A body carrying a detector: one measured event of a paid
family with a momentum on the x axis, a lamp of its own (one row per
self-creation, so its birth ordinals are its own count), and a table that
measures what arrives at it. It is series O's star (`two_stars`, "the star
is the detector", record 162: "a moving body is a detector moving over the
Nodes") and series S's reader (`reader_clock`, the reader's own lamp as its
clock) in one event, moving. Its clicks are written on its own record; it
reads only its own count between clicks and the ordinals the packets bring;
it reads nothing of the tick and nothing at a distance. A detector of one
Node without a body has no count of its own (record 768), so the cart must
be a body.

## 2. The question the world answers, in the algebra's words

For a lamp A at rest and the cart D receding along the axis at the pace v
(Nodes per count) with beta = v / c, the law as it stands (every count at
the rate r = 1, DERIVATIONS_BEAM 4.3: "a clock slows by what it reads, never
by its speed") predicts, by Theorem 1 with `r_A = r_D = 1` (the click frame
:244 and :252):

    k_AB = (D's counts apart) / (A's ordinals apart) = 1 / (1 - beta)        (the missing direction, NOT READ on main),
    k_BA = (R's counts apart) / (D's ordinals apart) = 1 + beta              (READ on main: NATURE row 4b, series G2),
    k_BA / k_AB = 1 - beta^2                                                  (the law; 1 under Lorentz; (1 + beta) / (1 - beta) for the resident loop),
    k_AB k_BA  = (1 + beta) / (1 - beta)                                      (the round trip, r-free under every r),

where R is a transponder at rest behind the cart. By Theorem 2 the cart's
radar reading of R (its pulse's birth ordinal `n_e` and its own count `n_r`
at the return, `x_D = c (n_r - n_e) / 2` Links, `t_D = (n_r + n_e) / 2`
counts) gives R's velocity `delta x_D / delta t_D = -v`, r-free, Einstein's
already on the law as it stands. By Theorem 3 the cart's place changes by
one Node per hop and by nothing between hops, the counts between two hops
are `k` exactly when `1 / v = k` is a whole number and only `k` and `k + 1`
when `1 / v` lies between them (the quantum of velocity `1 / (k (k + 1))`).

The world reads the three things that are NOT READ on main (the click
frame section 4; the Einstein Mathematician's II.3 to II.5 "NOT READ"): the
missing direction `k_AB` and with it the ratio that decides between the
law's `1 - beta^2`, Lorentz's 1 and the loop's `(1 + beta) / (1 - beta)`;
the radar velocity; the least step and its quantum. It reads them on the
law with r = 1 and no crowd; what it cannot read is r itself (section 6).

## 3. The world

A bar of 240 x 3 x 3 Nodes, open on every face, no crowd, no `mass`,
`suspension` 0, N = 64, K as series O (4202496), Q = 64, the width S =
2^20, the release [1, 65536] (series O's numbers, `examples/events/two_stars/
symmetric.json`; the massive rows off, no key of any hypothesis). Three
measured events on the axis y = z = 1 and three paid families of one unit
of content (`quantum` 1), named by their role:

| Event | Family | Node | Momentum | Lamp | Table | Role |
| --- | --- | --- | --- | --- | --- | --- |
| R, the post | `post` | x = 1, fixed | 0 | none; `directions` [[1, 0, 0]] | `cart`: `rerelease`; `lamp`: `pass` | the transponder at rest: every row of the cart's lamp that arrives is re-emitted on +x at R's next self-creation, stamped with R's number, the row's record kept (ENGINE.md, "a `rerelease` entry does the same with another number's rows"); its line carries R's own count |
| A, the lamp | `lamp` | x = 3, fixed | 0 | rate [1, 1], wheel [1, 64], `directions` [[1, 0, 0]] | `cart`: `pass` | the lamp at rest, one row per self-creation on +x toward the cart; the returning pulses pass through it |
| D, the cart | `cart` | x = 20 at the start, free | (p, 0, 0), p = Q S M / (k - 1) | rate [1, 1], wheel [1, 64], `directions` [[-1, 0, 0]] | `lamp`: `measure`, `reads: "age"`; `cart`: `measure` | the moving body detector: it clicks A's rows (the missing direction) and its own pulses returned by R (the radar and the round trip); its lamp shines -x toward R |

The cart holds `mass` 2^22 as series O's star does (M = 2^22 the content of
the drive's wall, `Q S M = 2^48`), so that `p = 2^48 / (k - 1)` is a whole
number for `k - 1` a power of two: the four deciding worlds are `k` = 3, 5,
9, 17, the pace `v = 1 / k` Nodes per count exactly (the accumulator's
pattern of period k, the drive's closed form), and beta = `v / c = 55 / (32
k)` = 55/96, 11/32, 55/288, 55/544. The fifth world, the quantum's, declares
`p = 3 x 2^46` (the pace 3/7, between 1/3 and 1/2): the accumulator hops at
its 3rd, 5th, 7th and 10th self-creation and so on, so the counts between
hops are 2, 2, 3 repeating and never another number. 600 intervals; the cart ends at x = 20
+ 600 / k (220 at k = 3), within the bar. The window of every ratio is the
cart's clicks from its 60th count to its last click (the first sixty counts
let the first pulses return; the round trip from x = 20 to R and back takes
2 x 19 / c = 65 intervals). Every world file is written by
`examples/events/moving_detector/make_worlds.py` (to be written at step 3)
and pinned to it by a test, as series O's are; nothing by hand.

The model identity of the series: `beam-moving-detector-k<k>-v1` and
`beam-moving-detector-quantum-v1`; the hypothesis list of the run's record
carries nothing but the amplitude identity every lamp carries (`amplitude-v1`,
ENGINE.md), the law as it stands and no key of a hypothesis, so that every
reading is the law's own.

## 4. The readings, by kind

The reading tool (`tools/moving_detector_readings.py`, step 3) reads the
record `events.jsonl` and forms, from the cart's clicks and the post's
lines only:

- DETECTOR, on the cart's record (its `click` lines with `measured` = D's
  number): the Node of each click (`node`), the cart's own count at the
  click (section 7), the ordinal of what arrived (`record` mod 2^32) and who
  sent it (`number`: A for the lamp's rows, R for the returned pulses).
  From them: `k_AB` (the cart's counts apart over A's ordinals apart, over
  the window); the round trip (the cart's counts apart between two returns
  over its own ordinals apart between the two births they carry); the
  radar pair `(x_D, t_D)` of every return and the radar velocity over the
  window; the cart's place at every click, its changes (0 or 1 Node) and
  the counts between two changes.
- DETECTOR, on the post's record (its `rerelease` lines with `measured` =
  R's number): R's own count at each arrival and the ordinal of the cart's
  birth it carries. From them: `k_BA` (R's counts apart over the cart's
  ordinals apart, over the window). On this world R's count equals the
  tick (no crowd, R fixed from tick 0 at an empty Node), which the tool
  checks against R's `age` in `state.json` and states; it is a check of the
  identity, not a reading of the tick.
- GAMEBOARD, labelled and never pinned: every `tick`, the `step` lines of
  the cart (the drive accumulators, the Node it steps to), the books, the
  cart's `age` in the final state (checked equal to the number of intervals
  since no interval was owed), the row counts in flight.

The ratio `k_BA / k_AB` is a DETECTOR reading of two detectors' counts (the
cart's and the post's), and by the Einstein Mathematician's sorting fact it
carries `r_R / r_D`; the round trip and the radar velocity are ratios of the
cart's own counts alone and carry no r.

## 5. The pins, from the formulas, before any run

At r = 1 (the law), beta = 55 / (32 k), each ratio read over a window of W
counts apart with the tolerance 2 / W (the hop's one-count remainder at
each end; the click frame: within 1 / T of the count and 1 / T_D of the
pace). Lorentz's one-way factor, `sqrt((1 + beta) / (1 - beta))`, is written
beside as the comparison the law fails at second order (NATURE row 4b).

| World | k | beta | `k_AB` = 1/(1 - beta), the law | `k_BA` = 1 + beta, the law | the ratio, the law `1 - beta^2` | Lorentz's one-way factor, both | the round trip `(1 + beta)/(1 - beta)` | the radar velocity | the counts between hops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `k3` | 3 | 55/96 = 0.5729 | 96/41 = 2.3415 | 151/96 = 1.5729 | 6191/9216 = 0.6718 | 1.9191 | 151/41 = 3.6829 | -1/3 | 3 only |
| `k5` | 5 | 11/32 = 0.34375 | 32/21 = 1.5238 | 43/32 = 1.34375 | 903/1024 = 0.8818 | 1.4310 | 43/21 = 2.0476 | -1/5 | 5 only |
| `k9` | 9 | 55/288 = 0.1910 | 288/233 = 1.2361 | 343/288 = 1.1910 | 79919/82944 = 0.9635 | 1.2133 | 343/233 = 1.4721 | -1/9 | 9 only |
| `k17` | 17 | 55/544 = 0.1011 | 544/489 = 1.1125 | 599/544 = 1.1011 | 292911/295936 = 0.9898 | 1.1068 | 599/489 = 1.2249 | -1/17 | 17 only |
| `quantum` | 7/3 (the pace 3/7) | 165/224 = 0.7366 | 224/59 = 3.7966 | 389/224 = 1.7366 | 22951/50176 = 0.4574 | 2.5677 | 389/59 = 6.5932 | -3/7 | 2 and 3 only, the pattern 2, 2, 3 |

The radar velocity is in Nodes per count of the cart (`-v`, R receding
behind it); the least step is pinned in every world as: the cart's Node at
two consecutive clicks differs by 0 or 1 and never more (Theorem 3 (a) and
(c)); the round trip's pin is r-free and holds under every r, so it is the
tool's consistency check of the two one-way factors as well as a reading.
Every ratio is exact in the mean over whole periods of the accumulators (k
counts for the hops, 55 intervals for 32 Links of a row); within a window
the reading differs from the closed form by at most the tolerance.

## 6. What would refute, and what the world cannot decide

- A radar velocity off `-1 / k` beyond the tolerance, or a round trip off
  `(1 + beta) / (1 - beta)`, under the law's r = 1, refutes A1 on the board
  (the Einstein Mathematician's words: a round-trip velocity or a radar
  angle off Einstein's under ANY r refutes A1): a packet would not be
  passing one Node per interval at the table's pace, or the re-emission
  would not keep the record.
- Counts between hops other than k in the k worlds, or other than 2 and 3
  in the quantum world, or a place changing by two Nodes in one count,
  refute the drive's closed form (Theorem 3 (a)).
- The ratio `k_BA / k_AB`: the law's number is `1 - beta^2`, stated so that
  it fails against Lorentz's 1 (PREDICTIONS.md; NATURE row 4b's FAIL at
  second order restated in one world at one speed with both directions
  read). A reading of 1 within the tolerance would mean `r_D^2 = 1 - beta^2`
  on this world, which nothing on the law supplies (no crowd, no key), and
  would refute the law's r = 1 as built. Either outcome is a reading, not
  a number to move.
- What the world cannot decide: r itself. Every count on this world equals
  the tick (no crowd), so the world reads the law's forms at r = 1 and
  nothing of what would make r `sqrt(1 - beta^2)`; the click theorem's (A2)
  and the identity covariant-readings-v1 are the two named candidates and
  neither is declared here. A crowd world (the cart in a crowd, its count
  stretched by the owed count) is the extension, not built.

## 7. The one thing the design adds to the engine, and the gate

Everything the world needs exists on `main`: a thrown body with a lamp and
a `measure` table reading another body (series O), the reader's own lamp as
its clock (series S), the `rerelease` rule stamping another number's rows
with its own and keeping the record (the catalog's `sun_planet`), the
record's ordinal on every click. One thing is missing: a measured event's
line (`click`, `rerelease`, `read`, `become`) carries the tick and not the
event's own count, so the cart's count at its click is today read only
through the tick (equal to it on this world, GAMEBOARD by label). The design
adds one field, `clock`, the event's `age` at that interval (its own count
of self-creations, already on its record; the detector's own count is the
measurement, record 768 and the Boss's word of 06:15Z), on every line a
measured event writes, under the world key `clock_stamp` (true or false,
false by default) so that every registered record's digest stands
(`tests/test_amplitude_click.py` (d) and `tests/test_covariant_readings.py`
pin `events_sha256`). No new state, no rule, no verb: a field written from
the record. The five worlds declare the key; the tool refuses a record
without the field. If the reviewer prefers no key for a record field, the
alternative is an in-process reading of the event's `age` at each click by
the tool, as PR #777's tier (b) read r off the detector's own state; the
reviewer decides at step 2.

The three tests of every rule (skills/workflow.md): generic (no family
name, no kind; the field is the event's own integer), vector (no verb
touched; the six verbs act as before), local (the event's own record, the
tick read by nothing). LOCALITY-1: the cart reads only what arrives at its
Node and its own count; the post re-emits from its own Node at its own next
self-creation; the host reads the records after the run. The host's cost:
three measured events, at most three rows born per interval, at most `3 x
600` rows in flight on 2160 Nodes, fixed local work per Node per interval;
the tool linear in the number of clicks.

## 8. What is not built

No crowd and no `mass` on the axis (r = 1 by the law; the crowd world is
the extension of section 6). No key of a hypothesis (`covariant_readings`,
`optical`, `drive_b`, `massive_rows` all absent; the drive is `main`'s
per-axis drive on one axis). No second moving body: the composition of
velocities (the Einstein Mathematician's pins 2/5 and -1/3), the length
contraction (3/4, 15/16, 63/64 under the law; 0.8660, 0.9682, 0.9922 under
the line) and the aberration (120 degrees) are his pins for further worlds
of the same kind (a second cart, a rod of two transponders, a transverse
lamp) and are not declared here. No ground detector beside the post: the
post's own count on its re-release line serves, and a reading of the cart's
lamp at a second rest detector is the register's series G2 already. No
Lorentz line declared, no r declared, no fit.

## 9. The steps after this design

1. Step 2: the physics-rule reviewer's read (ADMISSIBLE, or the corrections
   folded here before any build).
2. Step 3: the build of what the pins need, on this branch: `clock_stamp`
   in `world.py` and the four line writers, one test with a moving body in
   no crowd (the field equals the tick) and a fixed body in a crowd (the
   field falls behind the tick by the owed count); `make_worlds.py` and the
   five worlds with `expectations.json` holding the pins of section 5 as
   written; the reading tool; the register entry drafted in
   `examples/events/moving_detector/README.md`; `tools/check.py` exit 0.
3. Step 4: the run on the owner's word only (`tools/run_series.py`), the
   readings written under `runs` in `expectations.json` by the tool, the
   pins untouched; the day's record by the Boss.

## 10. Links

- [The click frame](../click_frame/DERIVATION.md): section 0 (the click
  theorem, locality Outside), section 4 (the missing direction and its pins).
- Einstein Outside, `docs/designs/einstein_outside/DERIVATION.md` on branch
  `einstein-outside` (PR #792): section 2 (Theorems 1 and 2), section 3
  (Theorem 3, the quantum), II.1 to II.5.
- Light Outside, `docs/designs/light_outside/DERIVATION.md` on branch
  `light-outside` (PR #791): II.4, the Doppler of a moving detector as a
  passage of clicks.
- [Series O, two stars](../two_stars/DESIGN.md) and
  [series S, the reader's clock](../reader_clock/DESIGN.md): the templates
  of the star as a detector and of the reader's own lamp.
- [ENGINE.md](../../ENGINE.md): the measured event's rules (`measure`,
  `rerelease`), the record's ordinal, the clock of a measured event.
- [NATURE.md](../../NATURE.md) row 4b and [EXPERIMENTS.md](../../EXPERIMENTS.md),
  series G2: the direction already read.
- [PREDICTIONS.md](../../PREDICTIONS.md): a FAIL stated so that it fails.
