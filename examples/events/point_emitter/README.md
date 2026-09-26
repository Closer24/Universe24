# The point emitter: the first row

The point emitter (ALGEBRA.md 9.69 (2), 9.71 (1); the model owner's word of
2026-09-25 through the Boss, record 2054, "try to reduce them all to a Node";
BUILD.md section 26 item 50) is a hypothesis under its own identity, the world
key `point_emitter`, off by default. An emitting body is one Node, its seat: at
its giving click no train is written; a window opens, and every interval the
seat's rotation is added to the given row at the seat at the declared `weight`
g (a_given(seat) += g x a_seat), the norm leaving the seat is read as the
outward flux through the seat's six Ports and summed, and the window closes at
the first interval at which the sum reaches the excitation's action T (the
emitter's `norm` over its `norm_denominator`). What comes out is the law's: a
train of about n c_l Links (n the window's length in intervals, c_l the
coordinate speed of light) with the band 1 / n at the wave number light's
dispersion gives to the seat's frequency. No declared train, no declared
wavelength.

## The worlds

Both worlds are written by `make_worlds.py` (run from the repository root with
`PYTHONPATH=src`); the well is the one-Node mode [800, 802] of the kind
[800, 813] (its rotation omega = 0.178, its pair rich), seeded at 2^12, with a
stock of 64 light quanta; the weight g = 1 chosen by the generator's trial
(`point_weight`: the window at g = 1, then around sqrt(n_1 / target), the
nearest to 32 periods of the seat's rotation), the window's typical length
written beside it as `window_read` (HOST).

- `point_chain.json`: a chain of 1200 Nodes (x open, the face slabs 32 deep),
  the seat at 600, two receiver sets `left` and `right` of three light bodies
  each, 500 Links from the seat on each side; the window read 1009 intervals.
- `point_light_clock.json`: the light clock with a point emitter on a chain of
  400, the seat at 100, a mirror four Nodes deep 60 Links beyond it, the
  detector the seat's own set `at_well` named as the receiver; the window read
  1503 intervals.

The one command runs them in check mode (no pin, no verdict):

    PYTHONPATH=src python tools/run_inputs.py --out RUNS --jobs 2 \
        examples/events/point_emitter/point_chain.json \
        examples/events/point_emitter/point_light_clock.json
    PYTHONPATH=src python examples/events/point_emitter/read_runs.py RUNS
    PYTHONPATH=src python examples/events/point_emitter/read_runs.py \
        --wavelength examples/events/point_emitter/point_chain.json

## The readings beside the blind expectations (2026-09-25)

The expectations are the mathematician's of ALGEBRA.md 9.71 (1), written before
the runs; c_l = 0.573 at the long wave (9.62 (1)). Every reading is labelled by
kind; a reading outside its band goes to the mathematician before any word.

| Row | Expected (blind, 9.71 (1)) | Read | Direction |
| --- | --- | --- | --- |
| (i) The chain: the counts at the two sides | alike, 32 +- 4 each of 64 where the face receivers take all | DETECTOR left 24, right 19, the faces 21; all 64 records clicked | the sides alike (the difference 5 against a spread of about 7); the faces take a third because the sets are three Nodes each, not full receivers |
| (ii) The chain: the first click at each side | 500 / c_l = 873 intervals after the open, plus the window's share | DETECTOR the least waits 884 (left) and 914 (right); the means 1206 +- 47 and 1286 +- 53 (rms 230) | holds: 11 and 41 intervals after the flight; the means before the window's centroid (873 + 505 = 1378), the ladder reading the front of the train |
| (iii) The chain: the train's wavelength | light's dispersion at the seat's rotation 0.178: 20.4 Links | GAMEBOARD (a diagnostic, the light's rows summed on the chain at interval 1409, 100 to 500 Links from the seat) 20.3 Links (+x) and 20.4 Links (-x), 28 zero crossings each | holds |
| (iv) The light clock: the tick from the open | 2 x 60 / c_l + n / 2 = 209 + 752 = 961 at n = 1503, every tick within sqrt(n) = 39 | DETECTOR 63 clicks of 64 quanta (90 opens: the taken light re-given), the tick 1313 +- 93, rms 738, least 363; bimodal: 25 ticks in 250 to 1000, 29 in 1500 to 2500 | does not hold as written; see the question below |
| The unit test's window against the weight | the window shorter at a larger weight, about g^2 | COMPUTATION on the chain of 400 (tests/test_point_emitter.py): g = 1 1124 intervals, g = 4 64, the ratio 17.6 | holds: beside g^2 = 16 |

## The question to the mathematician on row (iv)

Three things stand between the world as designed and the expectation.

1. The window at g = 1 is 1503 intervals of writing, a train of about 860
   Links; the arm is 60 Links, the return 209 intervals. So the record's own
   light comes back to the seat while its window is still open and the seat's
   own set books it (the outgoing emission itself books nothing: the bookings
   read the rows as the interval leaves them, both levels with their writes,
   and the emission is one-signed outward at the seat's Ports). Under the
   receiver by name the ladder's threshold is a fixed sixth of the norm; the
   click then closes the window short of T (as built: a record taken while
   its window is open closes it), the taken quantum is re-given and the next
   window opens after the rung. The two clusters are these two regimes.
2. The point emitter gives both ways. The half toward the open face at 0 (100
   Links from the seat) is booked by the face slab as a sink, but the rows
   return from the board's end: the earliest tick at the seat is 363 in this
   world and 382 in the diagnostic below, whose mirror cannot return before
   1745; both are the face's return (2 x 100 / c_l = 349) plus the write's
   build-up. A light clock with a point emitter needs its faces farther than
   the window's light plus the arm, or a receiving face.
3. The expectation n / 2 + 209 reads the click at the centroid's return, which
   needs the whole window returned before the threshold is reached: an arm
   longer than the window's light, and the threshold on the returned share.

Which reading is the row's: the rung's fixed sixth on the return, or the
centroid; does a taking close the window; and where do the faces stand?

Diagnostics beside it (not shipped worlds; DETECTOR, the tick from the open):

| Diagnostic | Read | Note |
| --- | --- | --- |
| The arm at 500 Links, the seat at 100 on a chain of 800 (the mirror's return 1745, after the close) | 99 clicks at the seat's set of 150 opens; the tick 1554 +- 60, rms 597, least 382; the ticks spread from 250 to 2500 with 43 of 99 in 1750 to 2250 | the earliest clicks are the face's return (349), the cluster at 1750 to 2250 the mirror's (1745) |
| The arm at 500 Links, the seat at 2000 on a chain of 4000 (the faces' return 6980, after every reading) | 218 clicks at the seat's set of 232 opens; the tick 1928 +- 34, rms 497, least 565; 128 of 218 in 1750 to 2500, 38 before the mirror's return at 1745 | the main cluster is the mirror's return; the early clicks are the finding below |

A finding of the diagnostics, not yet explained: on the later records of a long
run the seat's own set books the record's own rows before any return can
arrive. In the far-face world the record opened at interval 45966 had booked
0.12 of its norm at the seat 1691 intervals after its open, its mirror return
due at 1745; the record opened at 47007 clicked at the seat 748 intervals after
its open on a running total of 0.057 of its norm (its rung's draw), the
booking growing steadily from about 450 intervals after the open. On a fresh
chain the seat's set books nothing of the emission: the first record of the
unit world (the seat 200 Links from either face) booked 0.001 of its norm with
the stock 2 and 0.00001 with the stock 58, both from the opening's transient
alone. The runs differ in their history: by interval 47000 the chain carries
the rows of 46 earlier records and the content field's ripples from 90
takings and givings at the seat (light's pace Gamma - c reads the content at
every Node). Which of these turns the record's own outgoing rows back is the
next diagnostic; until then the light clock with a point emitter reads several
things at once, and its row waits.
