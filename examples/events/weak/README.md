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

**What was added on the law's side** ([BEAM_LAW note 34](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
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
