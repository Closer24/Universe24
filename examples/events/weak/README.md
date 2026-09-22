# Series J: the weak force

The worlds of series J, written by `make_worlds.py`; the register entry is
[J, the weak force (2026-09-20)](../../../docs/EXPERIMENTS.md#j-the-weak-force-2026-09-20)
and the evidence is in [validation](../../../docs/VALIDATION.md). The
question, in the model owner's words (Highlights 5.4, 2026-09-20): "Arrange
the weak force according to our world, and check whether we predict more
things", and the decision "go on everything; just make sure again that it
is good and generic": the neutrino first with the table-entry key
`phase_width` and no change of law (J2), then the transformation `become`
(J1, J3), then the W world. Under the owner's standing principle, "our
laws are on the GameBoard; in the detector one sees other laws": the
GameBoard gets the generic mechanism only, and the laws of nature (the
half-life law, the cross-section's rise with energy) are compared with
detector readings only. A research run, made once, never a test; every
expectation below was written before the run (the physicist's design,
`WEAK.md` sections 1, 2 and 4.5, with its integers; the counts computed
from the engine's own flight table by the generator); a reading outside
its expectation is reported with its numbers, never moved. Every number is
one of two kinds ([the register](../../../docs/EXPERIMENTS.md), "Two kinds
of readings"): a DETECTOR reading (a reader's clicks and passes, a shell's
clicks: the only kind reality has) or a GAMEBOARD reading (the expectation
from the flight table, a body's clock tick: the host's view). The readings
tool is `tools/weak_readings.py`, every line labelled by its kind.

## J2: the neutrino's passage through a filled bar

**What was added on the law's side** ([BEAM_LAW note 36](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(i)): the table-entry key `phase_width`, the width w of a window in phase
steps, N / 2 by default (the half circle as it was: every registered world
bit-identical). A window admits the w consecutive steps centred on its
setting, `(d + floor(w / 2)) mod N < w` with d the phase's distance from
the setting: the one floor of the window and its width
(`nature_beam.window_admits`). No law changes: the neutrino is a free
family with a phase circle, no charge and no content on its rays, and a
reader's window is what gates it.

**The base.** A bar of 200 x 1 x 1, `"law": "beam"`, K 4096, N 64,
`release` [1, 4096], `suspension` 0, 1037 intervals. A fixed source of the
free family `nu` of content 4096 at x = 0 releasing one ray per
self-creation on +x (the release 4096 / 4096), its clock turning 4096 /
4096 = 1 phase step per self-creation, so the ray born at tick t carries
the phase (t - 1) mod 64: the source's stride over the circle is 1 (with
K 2048 the turn is 2: the stride 2, the even residues only). 128 fixed
readers of the paid family `d` (content 1, no lamp: they release nothing)
at x = 8 .. 135, each measuring `nu` under a window (its `phase_window`
centre and its `phase_width`); a far detector of `d` at x = 190 measuring
`nu` without a window, counting every ray that reaches it. A reader
outside every declared detector is a detector of one Node (`wave`): the
pointer of one arriving ray is its own phase, so the window reads the
ray's phase. The first reader's arrivals over the run are the rays born at
the ticks 1 .. 1024 (the first-arrival age at 8 Links is 13 off the flight
table), sixteen turns of the circle exactly; the far detector's are the
rays born at the ticks 1 .. 711 (the first-arrival age at 190 Links is 326).

## The expectations, pinned before the runs (the physicist's integers)

| World | What | Expected |
| --- | --- | --- |
| `j2_filter` | every centre 0, width 1, stride 1 | the first reader takes every phase-0 ray, exactly 1 / 64 of its arrivals (16 of 1024); the 127 readers behind it take nothing (a filter, not an attenuation); the far detector reads 63 / 64 of the rays that reach it: 699 of 711 (DETECTOR, the counts; GAMEBOARD, the 711 from the flight table) |
| `j2_ladder` | the centre x mod 64, width 1, stride 1 | each reader takes its own residue: the readers at x = 8 .. 71 take the 64 residues (16 each) and the beam is exhausted; the readers at x = 72 .. 135 take nothing; the far detector reads 0 (DETECTOR) |
| `j2_default` | every centre 0, the default width (the half circle), stride 1 | the first reader takes 32 of the 64 residues, 512 of 1024, the others nothing; the far detector reads the other half, 352 of 711 (DETECTOR) |
| `j2_stride2` | every centre 0, width 1, stride 2 (K 2048) | the phases 0, 2, 4, ...: the first reader takes 1 / 32 of its arrivals (32 of 1024); the far detector 31 / 32, 688 of 711 (DETECTOR) |
| `j2_stride2_odd` | every centre 1, width 1, stride 2 | the centre misses the coset: no reader clicks; the far detector reads every ray that reaches it, 711 (DETECTOR) |

Against nature (PREDICTIONS entries 7 and 8, the law's own predictions,
registered as such): the admitted fraction is w / N whatever the emitter's
rate (the window reads the phase alone; a free ray carries no content), a
plain disagreement with nature's cross-section rising linearly with the
neutrino's energy; and a beam that survived one reader survives every
identical reader behind it (a filter set by the spread of the centres, not
an attenuation set by the depth), where nature attenuates exponentially in
the depth. The cross-section flat in energy is stated as a limit of the
law, not tuned.

## The worlds

`j2_<name>.json` for the five names above (the model ids
`beam-weak-j2_<name>-v1`). Run them in parallel and read the records:

```bash
python examples/events/weak/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/weak examples/events/weak/j2_*.json
PYTHONPATH=src python tools/weak_readings.py artifacts/weak
```

Each run takes about 3 s.

## What was measured (2026-09-20)

`tools/weak_readings.py`: 0 record checks failed, 13 readings inside, 0
outside, nothing moved (the numbers in the register entry). `j2_filter`:
the first reader 16 clicks of 1024 arrivals (1 / 64 exactly), the 127
behind it 0, the far detector 699 of 711; `j2_ladder`: the readers at
x = 8 .. 71 16 clicks each, the readers at 72 .. 135 none, the far
detector 0; `j2_default`: 512 of 1024 at the first reader, the far
detector 352; `j2_stride2`: 32 of 1024, the far detector 688;
`j2_stride2_odd`: no click at any reader, the far detector 711. The
detector's world sees a cross-section where the GameBoard has a stride: a
deterministic fraction, no draw, a filter and not an attenuation.

## J1 and J3: the neutron's decay against its clock

**What was added on the law's side** ([BEAM_LAW note 36](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(iii)): the transformation `become`, the identity `weak-v1`, one table
rule on the one-way side of the border: a measured event becomes an event
of another family and releases the rest as products, born as a re-release
is with the recoil over all of them; the clock trigger (the measured-event
key `become`: `at`, `into`, `products`, `crowd`) fires at the
self-creation whose clock reaches `at` while the count the clock read is
below the gate `crowd`; the click trigger (a `become` table entry) on an
arrival within a window. The charges balance at load, the key and the
entries are consumed, the books' `became` line and the record's `become`
line. The clock is slowed by the count it reads as every clock is
(`by_clock` at the world's suspension): a neutron in a crowd fires later,
a neutron alone at `at` exactly.

**J1, the free neutron's decay count.** 64 neutrons of the register's `n`
(content 1839, fixed, no strong unit held) on a lattice of pitch 4
(4 x 4 x 4) about the centre of an open 41^3 GameBoard, K 2^20, N 64,
`release` [1, 1], `suspension` [1, 2^20], each with `become` at 512 into
`p` (the charge 4 per unit on 1836) with the products `beta` (1, 3; the
charge -7344 per unit of amount, D-1) and `nu` (1, 0), each passing every
family; a shell of the paid family `d` at r = 18 (4170 Nodes) as one
`beam` detector set measuring `beta` with `reads` `age` (the flight time
on the click) and passing everything else; 650 intervals. `j1_lattice`:
the neutrons alone, each clock reading its line-mates' rows (the rows of
the other neutrons on its three axis lines at 4, 8 and 12 Links, each
dwelling one or two intervals at its Node: 12 rows at an inner neutron,
13 at a face, 14 at an edge, 15 at a corner). `j1_source`: with a fixed
source `s` of content 4096 at the centre releasing one row per direction
of the 290 primitive directions with |a| + |b| + |c| <= 6 per interval (a
crowd with a gradient). The design's 512 neutrons at `at` 2048 were cut
to 64 at 512 for the record's budget (the law is linear in the key, the
reading its ratio).

**J3, the bound neutron.** The deuteron of series I (`p` 1836 and `n`
1839 each holding one unit of `nuclear`, the strong column G = 10000 with
the lifetime 3, the whole fan of 290 directions, the width of the push
2^28, at one Link about the centre of an open 21^3 GameBoard) with
`become` at 512 on the neutron, a shell of `d` at r = 8 (762 Nodes) as a
`beam` set measuring `beta`. `j3_deuteron` (700 intervals),
`j3_deuteron_crowd` (the same with `crowd` 65536) and `j3_neutron_free`
(the neutron alone, 600 intervals).

## The expectations of J1 and J3, pinned before the runs (`expectations.json`)

The generator writes `expectations.json`: for every neutron the count its
clock read at tick 100 of a warm run of the same world without its
`become` keys (a GAMEBOARD reading of the engine's own presence) and the
tick that count gives by the clock's rule, at + floor(at x c / 2^20)
(a clock reading a constant count c owes `by_clock(a, c, 2^20)` after
every self-creation and the owed counts telescope), the reading inside
when the neutron fires at that tick or up to three intervals before it
(the crowd's build-up), never after.

| World | What | Expected |
| --- | --- | --- |
| `j1_lattice` | the neutrons alone | the trigger ticks 522 .. 524 (the warm counts 22068, 23907 and 25746: 12, 13 and 14 rows of 1839; GAMEBOARD); the shell's 64 beta clicks a step, the 10th-to-90th-percentile width of the click ticks over their median below 0.1 (nature's memoryless decay: ln 9 / ln 2 = 3.17); every click the content 3 (a line); the count 64 (DETECTOR) |
| `j1_source` | the source's fan on the lattice | the trigger ticks 524 .. 529 (the warm counts 25746 .. 36195, the neutrons on the fan's lines counting more and firing later; GAMEBOARD); the step, the line and the count 64 (DETECTOR) |
| `j3_deuteron` | the bound neutron | the transformation at 574 (the warm count 128590 at one Link from the proton; later than the free neutron's 512, not never; GAMEBOARD); the pair then two protons at one Link, holding (no step; GAMEBOARD); one beta click at the shell with the content 3 (DETECTOR) |
| `j3_deuteron_crowd` | the gate | no transformation in 700 intervals, the count above the gate 65536 at every pulse of the key (GAMEBOARD); no beta click (DETECTOR) |
| `j3_neutron_free` | the neutron alone | the transformation at 512 exactly, its clock counting nothing (GAMEBOARD); one beta click with the content 3 (DETECTOR) |

Against nature (PREDICTIONS entries 10 and 18, the law's own predictions,
registered as such): a step where the survival is exponential, a line
where the beta spectrum is continuous, a bound neutron that decays later
or is held by a gate on the count where nature's is stable by its binding
energy. Nothing is tuned.

Run them and read the records:

```bash
python examples/events/weak/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/weak examples/events/weak/j1_*.json examples/events/weak/j3_*.json
PYTHONPATH=src python tools/weak_readings.py artifacts/weak
```

The J1 runs take about 4 minutes each, the J3 runs about one; their
records are large (the fan's rows at the border).

## What was measured in J1 and J3 (2026-09-20)

`tools/weak_readings.py`: 0 record checks failed, 15 readings inside, 3
outside, nothing moved (the numbers in the register entry). Inside: the
shell's 64 clicks a step in both J1 worlds (from tick 541 to 563 in
`j1_lattice`, the median 549, the width over the median 0.036; 541 to
571 in `j1_source`, 0.038), every click the content 3, the count 64; the
deuteron's neutron firing at 577 (65 intervals after the free neutron's
512) with the pair holding after (0 steps of 39 and 21 attempted, every
attempt a hand-over); the gated neutron never firing; the free neutron at
512 exactly; every beta reaching its shell. Outside, the trigger tick
against the pinned tick in three worlds: the 8 corners of `j1_lattice`
fired at 524 against the pinned 522 (the warm run had read 12 rows at
tick 100 where their steady count is 15 rows, 27585, a gap of their
line-mates' rows at that tick; 15 rows give 525 by the clock's rule), 48
of the 64 neutrons of `j1_source` and the deuteron's neutron fired 1 to
3 intervals after their pinned ticks (the count a clock reads under a
fan's dwells is not one number over its history; the count at the trigger
was the warm count). The estimator was one tick's count; the lesson for
the next series is a range from the count's history over a dwell period.

## The W world: the exchange at one Link

**What was added on the law's side** ([BEAM_LAW note 36](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(iv)): nothing. The W is a paid family with a whole charge per unit of
amount (D-1) and the family key `lifetime` 1, no column: a row born at a
self-creation is at one Link at the age 1 and is measured there by the
keys' rule for a paid arrival (its units clicked, its label the push), or
booked on the border `lifetime` where no table took it. L = 0 is no
family at all: the contact form of the weak force is the `become` entry
itself (series J1 and J3); no Z family.

**The world.** A bar of 7 x 1 x 1, K 2^20, N 64, `release` [1, 2^20] (no
free release of 1839 before the age 570), `suspension` 0; `n` (1839,
charge 0), `p` (charge 4 per unit of content: 7344 on 1836), `w` (paid,
charge -7344 per unit of amount, `lifetime` 1); the neutron fixed at
x = 2 with `become` at 8 into `p` with the one product `[["w", 1, 3]]`
(the charges 4 x 1836 - 7344 = 0) on `directions` `[[1, 0, 0]]`, the
proton of 1836 fixed at x = 3; 16 intervals.

| World | What | Expected |
| --- | --- | --- |
| `w_exchange` | the exchange at one Link | the neutron's `become` at tick 8 with the W on +x, the recoil -192 (GAMEBOARD); the proton's click of `w` at tick 9, one Link and one interval later (DETECTOR); the proton's charge 0 and content 1839 after, a neutron's in the detector's terms (DETECTOR); no W on the border `lifetime` (DETECTOR); the momentum exchanged, -192 and +192 (GAMEBOARD) |

```bash
PYTHONPATH=src python tools/run_series.py --out artifacts/weak examples/events/weak/w_exchange.json
PYTHONPATH=src python tools/weak_readings.py artifacts/weak
```

**What was measured (2026-09-20).** 5 readings inside, 0 outside: the
`become` at tick 8 with [["w", 1, 3, [1, 0, 0]]] and the recoil [-192, 0,
0]; the click at tick 9; the charge [0, 1] and the content 1839; the
border {n: 0, p: 0, w: 0}; the momenta [-192, 0, 0] and [192, 0, 0]. The
exchange is complete at the click. The design's sketch of a `become`
entry on the proton (`into n` with a beta product) is refused by the
law's balance and balances only with a positive product
(`tests/test_w_world.py` (c)); the register does not use it.

## Re-read under the step drive (2026-09-20)

`j3_neutron_free` reads the same (no push). Under the step drive (a body's count
of Links is the whole part of the distance its momentum has driven)
`j3_deuteron`'s neutron fires at tick 572 (577 registered; the pinned 574
or up to 3 before it, inside now) and its beta clicks the shell at 583
with the content 3, but the pair does not hold: each body makes 3 steps
of 33 and 27 attempted (registered 0, every attempt refused), the
GAMEBOARD reading "the pair holds" outside; `j3_deuteron_crowd` still
never fires, its bodies 2 steps each. 9 readings inside and 1 outside (10
and 0). The register entry has the numbers ([migration](../../../docs/MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).

## Re-read under the signed drive (2026-09-20)

Under the signed drive (record 126) the deuteron holds again:
`j3_deuteron`'s nucleons make 0 steps of 33 and 29 attempted, the neutron
fires at 577 and its beta clicks the shell at 590 with the content 3 (the
first registration's numbers to the digit; the 3 steps under the unsigned
drive were the reversal defect's, the case that found it), and
`j3_deuteron_crowd` never fires with 0 steps; 9 readings inside and 1
outside (the trigger tick, as registered). The register entry has the
numbers ([migration](../../../docs/MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).

## Re-read under the fraction-free law (2026-09-20)

Under the fraction-free law ([BEAM_LAW note 41](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
records 147 and 148) the owed count is the count of each clock's
accumulator, exact over the crowd's history, where the count off the
clock had credited the whole age at the current crowd: `j3_deuteron`'s
nucleons wait 69 intervals of 700 each (80), attempt 33 and 31 steps
every one a refused contact (the pair holds), the neutron fires at 568
(577) and its beta clicks the shell at 581 (590) with the content 3 at
the same Node; `j3_deuteron_crowd` never fires (69 waited, 36 and 33
attempted); the J1 neutrons fire at 522 to 524 and 523 to 528 with the
shell's step as registered (the medians 551.5 and 553.5, the widths 0.036
and 0.038); `j3_neutron_free`, `w_exchange` and J2 are identical. 34
readings inside and 2 outside (the trigger ticks of the lattice's corners
and of the deuteron, as before). The register entry has the numbers
([migration](../../../docs/MIGRATION.md#the-fraction-free-law-on-2026-09-20-every-count-an-accumulator-on-the-bodys-record)).

## Re-pinned under the fraction-free law (2026-09-21)

The fraction-free batch re-read the runs above but left the register's
`become` entries as the first registration's warm run had written them
(the count each clock read at tick 100 of the engine before
[BEAM_LAW note 41](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
the architect's root cause, record 254: the first commit whose warm run
differs is e7ba13c6, the owed count on its accumulator). Re-pinned by the
generator at `main` as the lesson of the first registration asked: for
every neutron the range of the count over the dwell period, the ticks 61
to 120 of a warm run of 120 intervals (the transient over by tick 36, the
window longer than one cycle of the owed count, 2^20 / c intervals), and
the trigger ticks at both ends of the range; the reading inside when the
neutron fires within them or up to 3 intervals before. The old integers,
kept as history (the full maps in git before this re-pin):

| World | The first registration (2026-09-20) |
| --- | --- |
| `j1_lattice` | the counts 22068, 23907, 25746 at tick 100; the ticks 522 .. 524 |
| `j1_source` | the counts 25746, 26164, 31681, 32099, 36195 at tick 100; the ticks 524 .. 529 |
| `j3_deuteron` | the counts 128590 at tick 100; the ticks 574 .. 574 |
| `j3_deuteron_crowd` | never (the gate 65536) |
| `j3_neutron_free` | the counts 0 at tick 100; the ticks 512 .. 512 |

The re-pin: `j1_lattice` the counts 11034 to 27585 in four ranges, the
ticks 517 to 525; `j1_source` 20647 to 36195 in five ranges, 522 to 529;
`j3_deuteron` the range 23881 to 128590 (the proton's rows dwell at the
neutron's Node), 523 to 574; `j3_neutron_free` 0, 512; the gate as it was.
Against the runs at `main` every neutron of both J1 worlds and the
deuteron's fire within their ranges (522 to 524, 523 to 528 and 568):
the two readings outside since the first registration, the lattice's
corners and the deuteron, are inside under the range, 36 readings inside
and 0 outside; nothing else moves. `tests/test_weak_readings.py` (e)
replays the generator's warm run on the shipped worlds against the
register.

## Re-read under clock-age-v1 (2026-09-21)

The model owner's word of record 394: a clock counts the age moment by
default, and the neutrons' clocks (their entries for the other families
without a word) count it, so the `become` at the count 512 fires later
wherever a crowd is read. The five worlds run again on the head of branch
`clock-age-v1` (`tools/run_series.py --jobs 2`) and read by
`tools/weak_readings.py` (13 readings inside, 5 outside; the registered
36 inside under the range estimator); the registered reading beside the
new, every line labelled:

- `j1_lattice` (GAMEBOARD): 56 of 64 neutrons transformed within the 650
  intervals, the trigger ticks 602 to 642 (was 64 of 64 at 522 to 525 for
  the pinned 517 to 525), the counts read at the trigger 154476 to 338172
  (was the warm counts 22068 to 27585); DETECTOR: the shell's beta clicks
  20 within the run (was 64), from tick 629 to 646, the median 641, the
  10th-to-90th-percentile width over the median 0.0265 (was 0.036); every
  click the content 3.
- `j1_source`: 32 of 64 transformed, the trigger ticks 607 to 641 (was 64
  of 64 at the pinned 524 to 529 and up to 3 after), the counts read
  171027 to 303435; the shell's clicks 8 within the run (was 64), the
  median 634, the width 0.0110 (was 0.038); the content 3.
- The two J1 worlds at the cap 1024 (2026-09-21, N check's run on `main`
  c47c5fcd, record 545; the 650-interval lines above are kept as they
  were, the reading at its own cap beside them, one line per reading with
  its cap, no pin moved; entered by the Replicator, item 4 of the Boss's
  order, the numbers verbatim from the record): the 650 intervals reached
  56 of 64 and 32 of 64 as the declared duration reached them, not the
  lifetime's count; at 1024 every neutron fires, 64 of 64 in both worlds
  (GAMEBOARD), the last trigger ticks 671 (`j1_lattice`) and 689
  (`j1_source`); DETECTOR: the shell's 64 beta clicks in each; the
  10th-to-90th-percentile width over the median 0.0787 in `j1_lattice`,
  inside the step reading (below 0.1), and 0.1147 in `j1_source`, OUTSIDE
  it (above 0.1), from the wider spread of its trigger ticks (6 distinct
  against 4); the digests of the runs `j1_lattice` state c6f9e354...,
  events 75b7e537..., audit 9a812656...; `j1_source` state b1bdb151...,
  events 2008b437..., audit 44642763... (the full digests in N check's
  report). Whether the step's 0.1 is the lifetime's own bracket or the
  run's spread is a question for the chief physicist, not decided here;
  the outside reading is recorded as it is. `expectations.json` is the
  generator's warm-run output (the `become` ranges) and carries no run
  block, so this reading lives in this README and in EXPERIMENTS.md.
- `j3_deuteron`: the transformation at 577 (568 on main's engine, the
  register's tick under the fraction-free law; 577 was the first stage's),
  the count read at the trigger 152471 (was 128590): the trigger moved 9
  intervals under the word, and the count moved with it because the
  proton's fan at the neutron's Node is not all at the age 1: at tick 100
  it holds 57 lines at age 1 and 13 dwelling a second interval at age 2,
  the presence 70 x 1837 = 128590 and the age moment 152471, the excess
  23881 the register's own warm-up low count (the physics-rule review of
  1716b922, docs/designs/clock_age/REVIEW_1716B922.md: the stretch per
  self-creation 1.1226 against 1.1454, 9 intervals read while the fan
  fills); one beta click at 590, the pair holding after, every attempted
  step a hand-over.
- `j3_deuteron_crowd`: no transformation in 700 intervals, the count above
  the gate 65536 at every pulse, no beta click: unchanged in its reading.
- `j3_neutron_free`: the transformation at 512 exactly, its clock counting
  nothing, one beta click at 526 with the content 3: unchanged.

Against nature's rows ([NATURE row 8a](../../../docs/NATURE.md)): the
survival is still a step, the width 0.0265 and 0.0110 against the
memoryless 3.17, so the row's FAIL stands in form; but the row's registered
numbers 0.036 and 0.038 were read on 64 clicks and the age word's on 20 and
8, the rest of the population firing at or after the run's end (the
trigger 602 to 642 plus the flight to the shell, against 650 intervals).
Whether the row is re-read on a longer run or the J1 worlds re-declared for
the age word's count is a question for the model owner, flagged to the Boss
with this re-registration; nothing in NATURE moved on this branch.
