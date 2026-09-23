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

The rule of record 817 (the model owner, 2026-09-22): the paper shows how
we arrived at Einstein, Lorentz and the step above without deriving from
them. So every pin here is written from the Inside step and the conversion
alone, and Einstein's and Lorentz's forms are named only as the thing the
readings are compared with. The Inside step: A births one row per
self-creation (its ordinal advances one per interval, no crowd); the row
crosses 32 Links per 55 intervals (the flight table); the cart hops one
Node per k self-creations (the drive's pattern) and its own count advances
one per interval (no owed interval). The conversion: a factor is a ratio
of two counts apart, the receiver's over the emitter's ordinals. Counting
the rows that reach the cart in one of its counts gives, for a lamp A at
rest and the cart D receding along the axis at the pace v (Nodes per count)
with beta = v / c, exactly in the mean over whole periods (the same
arithmetic the Einstein Mathematician's Theorem 1 states in general, with
`r_A = r_D = 1`; the click frame :244 and :252):

    k_AB = (D's counts apart) / (A's ordinals apart) = 1 / (1 - beta)        (the missing direction, NOT READ on main),
    k_BA = (R's counts apart) / (D's ordinals apart) = 1 + beta              (READ on main: NATURE row 4b, series G2),
    k_BA / k_AB = 1 - beta^2                                                  (the law's number; the comparison: 1 is what Lorentz's one symmetric factor would give, (1 + beta) / (1 - beta) the resident loop's),
    k_AB k_BA  = (1 + beta) / (1 - beta)                                      (the round trip, a ratio of the cart's own counts; the rate r cancels in it),

where R is a transponder at rest behind the cart. The cart's radar reading
of R is two of its own counts, its pulse's birth ordinal `n_e` and its count
`n_r` at the return, made into `x_D = c (n_r - n_e) / 2` Links and `t_D =
(n_r + n_e) / 2` counts; the two legs of the chain of clicks (out at c
against a cart receding at v, back at c toward it) give `delta x_D / delta
t_D = -v` exactly, and the rate r cancels because both numbers are the
cart's own (the arithmetic of the Einstein Mathematician's Theorem 2); the
comparison is Einstein's radar, which gives the same -v. From the drive's
pattern the cart's place changes by one Node per hop and by nothing between
hops, the counts between two hops are `k` exactly when `1 / v = k` is a
whole number and only `k` and `k + 1` when `1 / v` lies between them (the
quantum of velocity `1 / (k (k + 1))`, his Theorem 3 in the same words).
Superseded on 2026-09-22 by [PREREGISTRATION_V2.md](PREREGISTRATION_V2.md) section 1 (the radar coordinate `x_D = c (n_r - n_e) / 2` gives `+v`; the five FAILs of version 1 preserved in its section 4).

The world reads the three things that are NOT READ on main (the click
frame section 4; the Einstein Mathematician's II.3 to II.5 "NOT READ"): the
missing direction `k_AB` and with it the ratio, whose law's number is
`1 - beta^2` and whose comparisons are Lorentz's 1 and the loop's `(1 +
beta) / (1 - beta)`; the radar velocity; the least step and its quantum. It
reads them on the law with r = 1 and no crowd; what it cannot read is r
itself (section 6). Nothing of Einstein's enters a pin: every number of
section 5 is the count of rows and hops of section 1 made into a ratio.

## 3. The world

A bar of 240 x 3 x 3 Nodes (320 x 3 x 3 for the quantum world), open on
every face, no crowd, no `mass`,
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
hops are 2, 2, 3 repeating and never another number. 600 intervals; the cart
ends at x = 20 + 600 / k (220 at k = 3) and at x = 277 in the quantum world,
within its longer bar. The windows: `k_AB` and `k_BA` from the cart's 60th
count to its last click; the round trip and the radar from the first return,
which reaches the receding cart at 2 x 19 / (c - v) intervals after the
start, 153, 100, 81, 73 and 248 for k3, k5, k9, k17 and the quantum world
(the physics-rule reviewer's correction of the 65 intervals of a cart at
rest). The cart's own births are never measured by its own table: a row
of the event's own number that arrives goes home and is created again
(ENGINE.md, "what comes home"); R's re-stamping of the returned pulse with
its own number is what makes the return a click at the cart, which is the
first registered event whose table names its own family. Every world file
is written by
`examples/events/moving_detector/make_worlds.py` (to be written at step 3)
and pinned to it by a test, as series O's are; nothing by hand.

The model identity of the series: `beam-moving-detector-k<k>-v1` and
`beam-moving-detector-quantum-v1`; the hypothesis list of the run's record
carries nothing but the amplitude identity every lamp carries (`amplitude-v1`,
ENGINE.md), the law as it stands and no key of a hypothesis, so that every
reading is the law's own; the key `clock_stamp` of section 7 enters neither
the model identity nor the hypothesis list, since it changes no physics; the
run's record names it as a record field.

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
  window; the cart's place at every click, its change against the counts
  between two clicks (the least step, section 5) and the pace over the
  window.
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
carries the rates: `k_AB` carries `r_D`, `k_BA` carries `r_R / r_D`, so the
ratio carries `r_R / r_D^2` (as section 6 uses it); the round trip and the
radar velocity are ratios of the cart's own counts alone and carry no r.

## 5. The pins, from the formulas, before any run

**Superseded on the radar velocity's sign (2026-09-22, issue #937): the
frozen coordinate `x_D = c (n_r - n_e) / 2` gives `+ v`, not the `- v`
pinned below; the versioned preregistration is
[PREREGISTRATION_V2.md](PREREGISTRATION_V2.md) (the coordinate kept, the
prediction `+ v`, the batch-933 failures preserved, the round-trip band
answered by kind). The text of sections 5 and 6 below is kept verbatim as
version 1.**

At r = 1 (the law), beta = 55 / (32 k), each ratio read over a window of W
counts apart with the tolerance 2 / W (the hop's one-count remainder at
each end; the click frame: within 1 / T of the count and 1 / T_D of the
pace). Every pin is the Inside step's count made into a ratio by the
conversion (section 2); Lorentz's one-way factor, `sqrt((1 + beta) / (1 -
beta))`, is written beside as the comparison only, the one the law fails at
second order (NATURE row 4b), and enters no pin.

| World | k | beta | `k_AB` = 1/(1 - beta), the law | `k_BA` = 1 + beta, the law | the ratio, the law `1 - beta^2` | the comparison: Lorentz's one-way factor, both directions | the round trip `(1 + beta)/(1 - beta)` | the radar velocity | the counts between hops (the drive's pattern; read from the `step` lines, GAMEBOARD; the DETECTOR pin of the least step is the paragraph below) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `k3` | 3 | 55/96 = 0.5729 | 96/41 = 2.3415 | 151/96 = 1.5729 | 6191/9216 = 0.6718 | 1.9191 | 151/41 = 3.6829 | -1/3 | 3 only |
| `k5` | 5 | 11/32 = 0.34375 | 32/21 = 1.5238 | 43/32 = 1.34375 | 903/1024 = 0.8818 | 1.4310 | 43/21 = 2.0476 | -1/5 | 5 only |
| `k9` | 9 | 55/288 = 0.1910 | 288/233 = 1.2361 | 343/288 = 1.1910 | 79919/82944 = 0.9635 | 1.2133 | 343/233 = 1.4721 | -1/9 | 9 only |
| `k17` | 17 | 55/544 = 0.1011 | 544/489 = 1.1125 | 599/544 = 1.1011 | 292911/295936 = 0.9898 | 1.1068 | 599/489 = 1.2249 | -1/17 | 17 only |
| `quantum` | 7/3 (the pace 3/7) | 165/224 = 0.7366 | 224/59 = 3.7966 | 389/224 = 1.7366 | 22951/50176 = 0.4574 | 2.5677 | 389/59 = 6.5932 | -3/7 | 2 and 3 only, the pattern 2, 2, 3 |

The radar velocity is in Nodes per count of the cart (`-v`, R receding
behind it). The least step (Theorem 3 (a) and (c)) is a statement per count,
not per click, and is pinned so: between any two clicks of the cart the Node
changes by at most one per count, `abs(delta node) <= delta count`; in the k
worlds, where A's rows click every 1 / (1 - beta) = 2.34, 1.52, 1.24, 1.11
counts, fewer than the k counts between hops, the Node at two consecutive
clicks of A's rows differs by 0 or 1 and never more; for consecutive returns
alone (3.68 counts apart at k = 3 against hops every 3) it may differ by 2,
and no pin is written on them. In the quantum world A's rows click every
224 / 59 = 3.80 counts while the hops come at gaps 2 and 3, so two hops fall
between consecutive clicks: the pin there is 1 or 2 Nodes between
consecutive clicks of A's rows, never 0 and never 3, and the pace over the
window 3 / 7 within the tolerance; the single gaps 2 and 3 themselves are
not resolved by clicks 3.80 counts apart and are read from the `step` lines,
GAMEBOARD, reported beside the pin and not pinned as a detector's number.
The round trip's pin is r-free and holds under every r, so it is the tool's
consistency check of the two one-way factors as well as a reading.
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

## 7. The code path: what carries a moving body detector today, what is missing for consecutive clicks, and the smallest change

The model owner's order of record 824 ("make sure we know how to run in
the code Outside with a moving detector, consecutive clicks"), read with
the Boss's frame: the engine must carry a moving body detector that reads
consecutive clicks on its own record, and we must show it runs. Line
numbers are `main`'s at 412f5c61.

**(a) What exists.** A body with a detector role and its own count is
already three declarations and one count:

- `world.py`: a measured event's keys `MEASURED_KEYS` (:640; `position`,
  `family`, `amount`, `held`, `momentum`, `fixed`, `table`, `lamp`, ...),
  parsed by `_measured` (:2577); the lamp by `_lamp` (:1990; `rate`,
  `wheel`, `directions`); the declared detector sets by `_detectors`
  (:3584; the `detectors` list, named sets of Nodes with a threshold and a
  reading, the one set object a body is too). A measured event that is not
  `fixed` may carry a table and a lamp: the only refusals on a moving body
  are a declared `E` (:2936) and a momentum on more than one axis (:2945;
  form B's directional drive is not on `main`, and the cart's momentum lies
  on the x axis). Series O's stars are exactly this (a thrown
  body, a lamp of one unit per self-creation, a `measure` table on the
  other's light, `examples/events/two_stars/symmetric.json`).
- `engine.py`: the per-axis drive `step_axis` (:119; one Link when
  `drive + p` reaches `Q S M + |p|`, `by_drive` with `at_most` 1), the
  body's step in `_move` (:743), and the body's own count in `_suspend`
  (:708): `entry.age += 1` at every self-creation and not at an interval it
  owes (:704-705); the body's own face click (:903).
- `measured.py`: `Measured` (:477) with `number` (:490), `position`
  (:491), `momentum` (:500), `fixed` (:501), `age` (:553, the own count),
  `births` (:627, the lamp's ordinal), `clock_age` (:654), `counted`
  (:659, the interval's arrivals); `clicks` (:600) is the total of units
  clicked per family, not a list.
- `nature_beam.py`: step 4, `_measure` (:5437) and `_apply_plans` (:5373):
  the rules `read` (:5127), `rerelease` (:5210, the transponder: the
  arriving rows of another number re-created at the entry's next
  self-creation on its declared directions, stamped with its number, the
  record kept), the click line at a body (:5284: `tick`, `node`,
  `measured`, `detector`, `family`, `number`, `amount`, `push`, `phase`,
  `content`, `reading`, and for a record's row `record`, `branch`,
  `multiplicity`, `u`, `share`, `age`), the `become` line (:6057, with the
  trigger's `counted`) and the pair's click (:6187); the record's identity
  `record_identity(entry.number, entry.births)` (:5605, :5800), the
  emitter's ordinal on every row it births.
- PR #777 (the clock audit's tier (b)) changed no engine line: its
  re-reads took r off the detector's own state in-process; the
  transponding rule is `rerelease`, on `main` since the law of events.

So the world of section 3 loads and runs on `main` as it is; the cart's
clicks are written on its record, one line each, with its Node.

**(b) What is missing for consecutive clicks read on the moving body's own
record.** Three things a reader needs at every click: the body's Node (the
line's `node`: present), the body's own count (absent: the line carries the
`tick`, GAMEBOARD, and the row's `age`, not the body's `age`), and the
count of what arrived (the ordinal in `record`: present). No list per body
is needed, since the record is the list (every line names `measured`); the
one absent number is the body's own count at the click.

**(c) The smallest change, under a key, off by default.** The world key
`clock_stamp` (true or false, false by default; `world.py`'s parse beside
the other world keys, `massive_rows` at :3803): when true, every line a measured event writes carries
`"clock": entry.age`, the event's own count at that interval: the click,
`read` and `rerelease` lines of `_apply_plans` (:5127, :5210, :5284), the
`become` line (:6057), the pair's click (:6187) and the body's face click
in the engine (:903); about eight lines, one field, no new state, no rule,
no verb; ENGINE.md's line description names the field as the measured
event's own count of self-creations (its `age`; not the row's `age` on the
same line, not `clock_age`), and the key enters neither the model identity
nor the hypothesis list. Without the key no field is written, so every registered record
stands byte for byte (`tests/test_amplitude_click.py` (d) and
`tests/test_covariant_readings.py` pin `events_sha256`); the deciding
worlds declare it. One test: a moving body at v = 1 / k in no crowd
(`clock` at each click equals the interval count since its birth, its Node
advances one per k counts, the ordinals it reads advance one per interval
of the lamp) and a fixed body in a crowd (`clock` falls behind the tick by
the owed count, `clock_age` and `age` as the engine keeps them). The
readings tool (`tools/moving_detector_readings.py`) prints, per body and
per click j, DETECTOR: `clock_j`, `node_j`, the sender's `number` and the
ordinal `record mod 2^32`; then the consecutive differences `count_(j+1) -
count_j` and `place_(j+1) - place_j`, the Outside step of record 803; and
GAMEBOARD, labelled: the tick of each line and the body's `age` in the
final state. The alternative, if the reviewer prefers no key for a record
field: the tool replays the world in-process and reads `entry.age` at each
click, as PR #777's tier (b) read r; the reviewer decides at step 2.

The three tests of every rule (skills/workflow.md): generic (no family
name, no kind; the field is the event's own integer), vector (no verb
touched), local (the event's own record; the tick read by nothing).
LOCALITY-1: the cart reads only what arrives at its Node and its own
count; the post re-emits from its own Node at its own next self-creation;
the host reads the records after the run. The host's cost: three measured
events, at most three rows born per interval, at most `3 x 600` rows in
flight on 2160 Nodes, fixed local work per Node per interval; the tool
linear in the number of clicks.

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
3. Step 4, the capability check, on the owner's word given by record 824:
   ONE run of the smallest world, `cart_k5` without the post (the lamp A at
   rest and the cart D at v = 1 / 5, N = 64 as the register's, 300
   intervals on a bar of 120), its consecutive clicks printed as DETECTOR
   (the count between clicks, the Node at each click, the ordinal read),
   nothing pinned as nature's; the design's pins for that world (`k_AB` =
   32 / 21; the Node at consecutive clicks of A's rows changing by 0 or 1
   and by at most one per count; the pace 1 / 5 over the window; the hops
   every 5 counts on the `step` lines, GAMEBOARD) compared as "read / not
   read" only.
4. Step 5: the transponder worlds of section 3 (the post added), the pins
   of section 5 declared before, run on the owner's word
   (`tools/run_series.py`), the readings written under `runs` in
   `expectations.json` by the tool, the pins untouched; the comparison
   against Einstein's forms only then; the day's record by the Boss.

## 10. Links

- [The click frame](../click_frame/DERIVATION.md): section 0 (the click
  theorem, locality Outside), section 4 (the missing direction and its pins).
- Einstein Outside, `docs/designs/einstein_outside/DERIVATION.md` on branch
  `einstein-outside` (PR #792): section 2 (Theorems 1 and 2), section 3
  (Theorem 3, the quantum), II.1 to II.5.
- Light Outside, `docs/designs/light_outside/DERIVATION.md` on branch
  `light-outside` (PR #791): II.4, the Doppler of a moving detector as a
  passage of clicks.
- Series O, two stars (`docs/designs/two_stars/DESIGN.md`, deleted on
  2026-09-22 with its worlds, record 871; in the tree's history at 59c6b811) and
  [series S, the reader's clock](../reader_clock/DESIGN.md): the templates
  of the star as a detector and of the reader's own lamp.
- [ENGINE.md](../../ENGINE.md): the measured event's rules (`measure`,
  `rerelease`), the record's ordinal, the clock of a measured event.
- [NATURE.md](../../NATURE.md) row 4b and [EXPERIMENTS.md](../../EXPERIMENTS.md),
  series G2: the direction already read.
- [PREDICTIONS.md](../../PREDICTIONS.md): a FAIL stated so that it fails.
