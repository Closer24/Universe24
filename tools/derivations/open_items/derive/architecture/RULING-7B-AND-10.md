# The architect's ruling at stages 7b and 10 (the owner's decision 27: the architect approves every two stages that the whole stands)

Read at tensor24-review 20e8a8bf2, before the owner's decision 28 (two boards). Probes: the reader's scratch,
architect_s16/probes/ (every_count.py, tst.py, size.py, with their outputs).

**Verdict: the whole stands; approved with changes.** One act per gear, the state fixed, the run back from the out
alone, the runner never importing the engine. Three changes, none touching the act.

## Required changes

1. **The round loop written twice:** runner/run.py's ran and runner/rounds.py's rounds (the tests' alone). One loop:
   ran calling rounds one round at a time, or the tests calling ran.
2. **The design text naming acts decision 27 cancelled** (text, before stage 8): plan section 11 item 1 (the
   turnover in engine/step.py), item 7 (one barrier, at the top), item 11 (T^q as a choice), item 3 (5G + H + 3,
   where 5G + 3 is built); engine/__init__.py's and carry.flip's docstrings; the schema's Turnover record and the
   decoder's "turnover" kind, which no act can write. The third place restated as T = J K, each kind's time
   reversal, one per-row sign built at load and read by the tests alone.
3. **Stage 7c with no place in the order** (plan section 12): the regulator's block, the strides before and after with
   their mirror, U_j on the hands' Meshes, E beside A1 in the tensions, the head compared act by act on every train;
   runner/load.py refuses inputs "until 7c". Placed before stage 8.

## Before each remaining stage

- **Stage 8:** one per-row sign array in the layout from the kind and the part (the hand's im row odd); T on an even
  row (a, b, r, go, rd) -> (b, a, W - 1 - r, 1 - go, T_d - 1 - rd), on an odd row (-b, -a, r, go, rd); probe:
  T tick T = untick on every gear array, 12 of 12 rounds, in range and past the ruler's last count, the mutant
  without the going failing at 5 and 10 of 12; the 24 on the state as a (24, N) site permutation from
  runner/board.py with each row block's matrices in its train's basis, r, go and rd flipped where a turn negates.
- **Stage 9:** the click events carry the time gear's count (the record's dial is the beat dial, so the decoder reads
  no time dilation); the Out carries the drive's q per row and the books' counts; the drive's signed q against the
  guard's q of at least 1 reconciled before the first click; light's winding (a zero divisor where s is 0) by M2;
  the take on the Node-clock's own gears alone, a two-ended click two one-ended acts, a take on a gradient or force
  coupling refused by the load; the draw's digits the neighbours' notches as of the count, a neighbour's r or rd
  in a slot of its own; the windings and the take's kept as new state arrays, State, lay, the records' order test
  and section 11 item 3 changing together.
- **Stage 10b:** the ledger's "after the step" and "after the clicks" are one state when the click is inside the act:
  the Out exposes the click's writes, or the ledger reads before and after the round against the books' work; the
  ledger keyed by count and written where the runner holds the board at one count (172 of 297 clock-count pairs never
  stand together under masks; the held masked run equals the synchronous one at 12 of 12 counts); readings/ given
  the stencil gathers by the runner; regions and halos named or dropped.
- **Stage 11:** the bang rows counted from the time gear's count swing, not from Turnover lines; the tops found by the
  runner from the state as a reading.

## Follow-ups

Records built by keyword; the header's winding published by the load; choose written by hand four times in load.py;
the tick computing every gear twice; two meanings of "count"; the operand "pull" being the force; docstrings with
provenance (the widest 500 characters); the Tensor24 tests at 39 and 46 s against the plan's 30 s; the run test named
"at every count" comparing the end alone (the probe shows it holds at every count); the ruler's two ends booked among
law 11's exceptions.

## What holds

The closed list; the imports (algebra the standard library, the engine algebra and numpy, the runner no engine, the
decoder no numpy, main.py the one joint); the state 5G + 3 with the time gear one A1 row no file names; the one act per
gear with the time gear first; the due bit and the past read; locality. With rates parted the masked run equals the
synchronous run in the whole state at every count, 12 of 12, and its outs ran back exactly. Engine with algebra 426
lines against the design's 425; the load 317, the checker 217, the schema 205, the decoder 709.
