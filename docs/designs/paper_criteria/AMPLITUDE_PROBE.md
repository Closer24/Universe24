# The amplitude probe: the rays in flight, the clicks and the gathers of a run against the engine's own forms (the chief physicist, 2026-09-23)

The model owner's request of 2026-09-23, in his words: "Can you do a small
experiment and see that the amplitudes propagate correctly on the board?
The board has propagating amplitudes and also the propagating ray of the
event itself. Verify it, because many bugs may simply come from the
amplitudes not propagating there, or the ray not propagating correctly";
and then: "Check that the amplitudes propagate like a wave, and the
propagation of the events like a ray. That is what we need to see on the
GameBoard, that is the Inside." The Boss's order (2026-09-23, on the
owner's word, record 1251 as the Boss recorded it): ship the probe as a
diagnostic, `tools/amplitude_probe.py`, its output verbatim here, every
number by kind. Docs and one tool; no law change, no world change, no
registered world touched. Base commit `b76abb36` (`origin/main`, "Merge
pull request #1011").

**The kind of every number here: GAMEBOARD.** The probe reads a run's
`state.json` (the host's view of the rows in flight) and `events.jsonl`
(the click, record and gather lines) and checks them against the engine's
own forms; it verifies the engine against itself and compares nothing with
nature. No number here is a DETECTOR reading and none is pinned.

**The forms checked** (the record form of a massless family with the pair
form of phase per interval, one lamp, plain `rerelease` re-emitters):

1. **The rays in flight.** Every ray's Node is the one the flight table
   gives from its birth Node by the digital line of its direction at its
   age, m(tau) = (2 tau S_1 Q + T_D) // (2 T_D) (the two-slit map's walk,
   `docs/designs/fraction_free/two_slits_map.py`, reproduced in the tool);
   its phase is the pair form's from its birth phase (u plus the lamp's
   turn for a lamp row, u for a re-emitted row, plus the sum of `by_clock`
   over its age, `core/integer.py`); its amount 1 and its multiplicity the
   lamp's ways times the split's norm.
2. **The clicks, records and gathers.** Every screen click line's `exact`
   equals BEAM_LAW note 45's phi = phase - floor(age n / d) + floor(n made
   T_D / (d S_1 Q)) mod N from the row's age and its direction; the
   direction is recovered from the remainder's denominator d S_1 Q and the
   remainder itself, since the label at the scale Q = 64 does not tell a
   fan of 601 directions apart (two of them, (281, -37) and (283, -35),
   share the label (63, -8); the remainder separates them). Every `record`
   line's pointer is the sum of its clicks' unit vectors 32 x (C, S)[exact]
   per Node, its square the line's. Every `gather`'s rungs are the
   engine's `rungs` (`events/amplitude.py`) on the sets' squares (the
   faces' from their click lines, summed per face Node: the layer's offer
   per label, the label the Node, a coherent sum within a Node and an
   incoherent one across Nodes, as `slits_huygens_pin.py` models it), and
   its chosen cell is `cell_of` on the record's u.
3. **The wave and the ray.** The rows re-emitted at one Node, grouped by
   age: the distinct phases on the ring (the wave: one per age, floor(age n
   / d) mod N, a full turn every 8 intervals at the pair 8591334592 /
   2^30), the ring's radius against c x age = age / sqrt 3 (the front), and
   the distinct directions (the ray: one straight digital line per
   direction).

**The worlds read.** `docs/designs/fail_rows/opening_w9.json` (row 10's w
= 9 world, RUN_10.md): a 30-interval probe through the shipped runner
(`python -m event_universe --init ... --ticks 30`, 5 s) for checks 1 and 3
(its `state.json`); the full run's record of 2026-09-23 (the row 10 step 2
run, in progress when read; its first 60 completed records) for check 2.

## 1. The output, verbatim: checks 1 and 3 on the 30-interval probe

```
amplitude probe of ../wt_runs/artifacts/probe/probe_w9 (model beam-row10-opening-w9-v1): N = 64, phase_per_link 8591334592 / 1073741824, the lamp measured 1 on 9 directions, the re-emitters [78, 79, 80, 81, 82, 83, 84, 85, 86] with the norms [601]
1. THE RAYS IN FLIGHT at the tick 30 (GAMEBOARD): 98061 rays ({'lamp rows': 98, 're-emitted rows': 97963}); Node off the flight table's walk from the birth Node: 0; phase off the pair form from the birth phase: 0; amount or multiplicity off: 0; rows per record: {9: 10, 1809: 1, 4209: 1, 5409: 17}
3. THE WAVE AND THE RAY: the rows emitted at (8, 76) (measured 78) at the tick 30, by age (GAMEBOARD): age | rays | distinct phases less the birth phase (the wave: one) | that phase and floor(age n / d) mod N | the ring's radius min / mean / max in Links against c x age | distinct directions (the ray: one each)
     0 |   601 | 1 | [0] and 0 | 0.00 / 0.00 / 0.00 against 0.00 | 601
     1 |   601 | 1 | [8] and 8 | 1.00 / 1.00 / 1.00 against 0.58 | 601
     2 |   601 | 1 | [16] and 16 | 1.00 / 1.22 / 1.41 against 1.15 | 601
     3 |   601 | 1 | [24] and 24 | 1.41 / 1.65 / 2.00 against 1.73 | 601
     4 |   601 | 1 | [32] and 32 | 2.00 / 2.32 / 3.00 against 2.31 | 601
     5 |   601 | 1 | [40] and 40 | 2.24 / 2.96 / 3.16 against 2.89 | 601
     6 |   601 | 1 | [48] and 48 | 3.00 / 3.55 / 4.12 against 3.46 | 601
     7 |   601 | 1 | [56] and 56 | 3.61 / 4.11 / 4.47 against 4.04 | 601
     8 |   601 | 1 | [0] and 0 | 4.12 / 4.63 / 5.10 against 4.62 | 601
     9 |   601 | 1 | [8] and 8 | 5.00 / 5.16 / 6.00 against 5.20 | 601
    10 |   601 | 1 | [16] and 16 | 5.10 / 5.79 / 6.32 against 5.77 | 601
    11 |   601 | 1 | [24] and 24 | 5.83 / 6.40 / 7.07 against 6.35 | 601
    12 |   601 | 1 | [32] and 32 | 6.08 / 6.99 / 7.28 against 6.93 | 601
    13 |   601 | 1 | [40] and 40 | 7.07 / 7.54 / 8.25 against 7.51 | 601
    14 |   601 | 1 | [48] and 48 | 7.62 / 8.04 / 9.00 against 8.08 | 601
    15 |   601 | 1 | [56] and 56 | 8.06 / 8.67 / 9.22 against 8.66 | 601
    17 |   601 | 1 | [8] and 8 | 9.06 / 9.85 / 10.44 against 9.81 | 601
```

## 2. The output, verbatim: check 2 on the w = 9 run's record, the first 60 completed records

```
amplitude probe of ../wt_runs/artifacts/fail_rows/opening_w9 (model beam-row10-opening-w9-v1): N = 64, phase_per_link 8591334592 / 1073741824, the lamp measured 1 on 9 directions, the re-emitters [78, 79, 80, 81, 82, 83, 84, 85, 86] with the norms [601]
2. THE CLICKS, RECORDS AND GATHERS of the first 60 completed records (GAMEBOARD): 428842 screen click lines, the exact phase off note 45's formula: 0 (0 whose remainder fits no direction); 83920 face click lines (no age on the line, read through the gathers); 9660 record lines, the pointer off the sum of its clicks' unit vectors: 0, the square off: 0; 60 gathers, the rungs off the engine's rungs on the sets' squares: 0, the chosen cell off cell_of(u): 0
```

## 3. What it says

- The rays propagate exactly as the flight table says and the phases
  exactly as the pair form says: 0 of 98061 rays off the Node, 0 off the
  phase, 0 off the amount or the multiplicity; every record that has
  split holds 9 x 601 = 5409 rows (the records mid-split, 1809 and 4209,
  are those whose later legs had not yet reached the opening at the tick
  30).
- The amplitudes at the detectors are exactly the sums of the rows' unit
  vectors at the exact phase: 428842 screen click lines at note 45's
  phase, 9660 record lines at the pointer sum and its square, 0 off.
- The click is exactly the ladder on u: 60 gathers with the engine's rungs
  on the sets' squares and the chosen cell `cell_of`(u), 0 off.
- The wave and the ray on the Inside: at every age the 601 rays of one
  re-emission carry ONE phase, equal to floor(age n / d) mod 64 (0, 8, 16,
  ..., 56, 0, ...), on 601 distinct directions, on a ring of mean radius c
  x age within one Link (the digital line's rounding): a front of one phase
  advancing at c on every direction, one straight ray per direction. The
  interference (bright and dark) is not on the board, where two rows in
  phases opposite pass each other unchanged; it is in the click's sum.
- Two apparent mismatches met while writing the probe were the probe's
  and not the engine's, and are recorded so that the next reader does not
  meet them again: the label at the scale 64 does not identify a fine
  fan's direction (the remainder does), and a face's weight is summed
  coherently within a Node and incoherently across Nodes.
- What the probe does not test: a massive family's turn by momentum, a
  weighted or rotated re-emitter, a gate, a body's drive; the same tool
  runs on any run folder.

## 4. The command

```bash
PYTHONPATH=src python tools/amplitude_probe.py <run folder> [--records 60] [--emitter NUMBER] [--no-clicks] [--no-state]
```

## 5. Links

- [RUN_10.md](../fail_rows/RUN_10.md): the world, the chain of steps, the pins.
- [slits_huygens_pin.py](slits_huygens_pin.py): the pin machinery whose forms the probe checks the engine against.
- [BEAM_LAW.md note 45](../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation): the exact phase at the click.
- [two_slits_map.py](../fraction_free/two_slits_map.py): the walk on the engine's digital line and flight table.
