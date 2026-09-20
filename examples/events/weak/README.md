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