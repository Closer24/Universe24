# The order channel: the pins before any run

The Order Channel Runner's assignment from the Boss on the model owner's
word (the Boss's records 952 (3) and 955 of `docs/LOG_2026-09-20.md`, cited
from the assignment; the log on `main` at `02147ed5` ends at record 951):
turn the third referee read's computation
(record 938 (2) of [the log of 2026-09-20](../../LOG_2026-09-20.md))
into a DETECTOR reading of the click ORDER, which no reading of the register
has made. Written before any run of the protocol; no pin here moves after
the run (`RUN.md`, step 2, reads against it). Every number is labelled by
kind: DETECTOR (a click outcome, its order, a window read at a counter, the
wheel value on a line of `events.jsonl`), COMPUTATION (a pin from the law's
algebra, printed by [order_pins.py](order_pins.py) into
[order_pins.out](order_pins.out)), or nature (the value compared with;
record 817's rule: Einstein's, Bell's and nature's numbers appear only as
the thing compared with). Notation per skills/workflow.md: rows and
records, a click, the wheel; fractions written n / m.

## 1. The finding to test

The referee's computation (record 938 (2)): under the sequential wheel
[1, 64] and Bob at b = 0, Alice at a = 0 gives B_t = A_t and Alice at
a = N / 2 = 32 gives B_t = -A_t for every birth t (Theorem 5's cells).
Bob's counts over a cycle are 32 / 32 either way (Theorem 5, the paper's
"Exact marginals; no-signalling"), but Bob's SEQUENCE carries Alice's
setting sequence: his serial correlation at lag 1 reads 15 / 16 when Alice
holds a = 0 and -5 / 16 when Alice cycles a = 32, 0, 0 with period 3, over
192 births, the marginal 96 / 96 in both. Nature's outcome order is random
and carries nothing: 0. The referee's numbers were a computation on the
written rules; the register has read the counts of the cells (the CHSH
worlds, the plateau worlds) and, in
[CRITERIA item (a)](../paper_criteria/CRITERIA.md#item-a-bell-measurement-independence-the-assumption-and-the-reading-that-tests-it),
the first party's serial correlation 1 - 4 / W from the registered
sequence, never Bob's order under a setting sequence of Alice's after a
detector.

## 2. The registered world, its law and its reader

- **The world.** The paper's pair worlds under `amplitude-v1`
  (`examples/events/amplitude/bell_0_8.json`, `bell_0_24`, `bell_16_8`,
  `bell_16_24`, the generator `examples/events/amplitude/make_worlds.py`
  `bell()`; the register's L3 entry): the A2 bar of 21 x 1 x 1, the lamp
  of `light` at x = 10 with the wheel [1, 64] at the rate [1, 1] (one
  birth per interval, u = (ordinal - 1) mod 64 the record's coordinate on
  the ladder), `arms` 2 and `branches` [[0, 1], [3, 1]] (the pair, the
  joint labels 00 and 11 of equal weight), N = 64, K = 15 x 2^20, the
  counters at x = 7 and 4 (Alice's arm, the direction -X, arm 0) and at
  x = 17 and 18 (Bob's, +X, arm 1), each its own detector of threshold 1
  reading `sum`, the windows the integers a and b. The chooser form of the
  same world, `examples/events/amplitude/bell_choosers.json`, reads
  Alice's window from the rows of the free family `sa` (a lamp at x = 0
  toward +X, the window `{"reads": "sa", "offset": s}`) and Bob's from
  `sb`; the register reads "the 960 births from tick 8 see the choosers'
  15 setting pairs with every u" (its L3 entry;
  `examples/events/bell/README.md`, "The choosers on the GameBoard").
- **The law's rule (the click).** One click per record by the ladder
  (BEAM_LAW note 46): the record lands in the first cell k with u < b_k,
  the rungs b_k = (2 N C_k + T) // (2 T) over the cells (++, +-, -+, --)
  in the layer's order, C_k the cumulative weight of the joint amplitude
  (the generator's `joint`, the rotation on the half-angle tables of 2N),
  T the total. The wheel is a counter (P4, no draw): the click is a
  function of (a, b, u) alone. Theorem 5 (the paper's `th:marginals`):
  the first party's outcome is + exactly for u < 32, and the second
  party's + count is exactly 32 per 64 births for every (a, b) at N = 64
  (no tie). The cells at b = 0 (COMPUTATION, `order_pins.out`): at a = 0
  Bob is + for u < 32 (B = A); at a = 32 for u >= 32 (B = -A); at a = 21
  for u in 0 .. 7 and 32 .. 55; at a = 42 for u in 0 .. 6 and 32 .. 56.
- **The reader.** The register's readers of these worlds are
  `tests/test_amplitude_pair.py` (`gathers_of`: the gathers of the lamp's
  records by birth ordinal, the record's identity 2^32 + ordinal) and
  `tools/amplitude_path.py`; the A2 worlds' tools are `tools/bell_chsh.py`
  and `tools/bell_choosers.py` (no `tools/click_readings/` exists on
  `main` at `02147ed5`). Under the pair form the record's one click is
  its `gather` line in `events.jsonl` (`chosen`: the channel + or - per
  arm in the arms' order, Alice first; `u`; `born`; `record`), and the
  arm's arrival at its counter is a `click` line carrying `window` (the
  setting read at that counter), `u` and `record`; the minus counters are
  silent under the one click (the register's `expectations.json`). The
  reading of this run, `order_reading.py` (step 2),
  reads exactly those lines: the outcome order from the `gather` lines
  by birth ordinal, Alice's setting sequence from the `click` lines'
  `window` at `alice_plus`, both DETECTOR; integers and Fractions only.
  The assumption CRITERIA item (a) names (the settings independent of the
  wheel) holds in both worlds below by construction: a constant setting,
  or a period coprime to 64 (each setting meets every u once in 192).

## 3. Why the referee's 32, 0, 0 cannot be declared, and what can

The register's keys give a counter's window as an integer or as a reading
from a family (`world.py`, `_window` and `_window_reading`); there is no
per-birth sequence of windows. A chooser's rows carry its clock's phase,
a constant stride of content / K steps per interval, so the settings met
by consecutive births are an arithmetic progression on the circle: two
equal consecutive settings (0, 0) need the stride 0 mod 64, a constant.
The alternation 32, 0 (the stride 32) is refused by the loader's guard
"2 x content must stay below K x N" (checked on the loader without a run:
`measured[5].amount` at 32 K refused). So the referee's protocol is a
COMPUTATION only; `order_pins.py` reproduces its numbers (P0: -5 / 16 at
every shift of the cycle; 15 / 16 at a = 0). The protocol of the
referee's shape that the register's own keys declare: Alice's window read
from `sa` at the register's `sb` clock, the stride 64 / 3 (content
64 K / 3 = 335544320, phase 0: the turns 21, 21, 22, the phases 0, 21, 42
and again, the period 3, coprime to 64), the offset 0, so Alice cycles
a = 0, 21, 42 in the clock's order; Bob at the integer 0. No engine code
changes; no registered world, pin or rule moves. The new worlds, off the
gate set (`examples/events/gate_set.json` unchanged) and outside both
generators' lists, under `examples/events/bell/` as the assignment names:

| World | A copy of | The settings only |
| --- | --- | --- |
| `examples/events/bell/order_a0_b0.json` | `examples/events/amplitude/bell_0_8.json` | the four windows the integer 0 (a = b = 0); `ticks` 212 (192 births and the flight of 13 intervals); `model_id` `beam-order-a0_b0-v1` |
| `examples/events/bell/order_a0_21_42_b0.json` | `examples/events/amplitude/bell_choosers.json` | `sb` removed and Bob's two windows the integer 0; Alice's plus window `{"reads": "sa", "offset": 0}` (the minus 32, silent); `sa` at content 335544320 (64 K / 3) and phase 0; `ticks` 220 (the warm-up before the first `sa` row at x = 7, 192 births, the flight); `model_id` `beam-order-a0_21_42_b0-v1` |

Both load through `event_universe.world_loading.load_world` (checked, no
run). The run's tools: the shipped runner `python -m event_universe --init
<world> --output <dir>`, Python 3.14, headless, no frames.

## 4. The protocol and the analysed births

- **First reading** (`order_a0_b0`): Alice constant a = 0, Bob b = 0;
  the births of ordinal 1 .. 192 (u = 0 .. 63 three times), in birth
  order.
- **Second reading** (`order_a0_21_42_b0`): Alice a = 0, 21, 42 with
  period 3 in the clock's order, Bob b = 0; the analysed births are the
  first 192 consecutive ordinals from the first ordinal whose Alice click
  carries a window (the register's warm-up: the pairs before the first
  `sa` row at x = 7 meet no setting and go to `alice_minus`); the tool
  reports the first ordinal and the shift (which of 0, 21, 42 the first
  analysed birth meets), both DETECTOR. The pins below are the same at
  every shift and every start u (`order_pins.out`: 192 births are one
  joint period of the wheel and the cycle, and the pinned statistic is
  cyclic).
- **The statistic.** Bob's serial correlation at lag 1 over the L = 192
  analysed births in birth order, cyclic: (1 / L) sum over t of
  B_t B_{(t + 1) mod L}, an exact fraction (the referee's 15 / 16 is this
  form: 1 - 4 / W over whole turns of the wheel). The open-chain mean over
  the 191 adjacent pairs is printed beside it, unpinned (it depends on the
  start: 181 / 191 for the square wave from u = 0).

## 5. The pins

| Reading (DETECTOR after the run) | Kind of the pin | First reading, a = 0 | Second reading, a = 0, 21, 42 | Nature |
| --- | --- | --- | --- | --- |
| Bob's serial correlation at lag 1 (cyclic, 192 births) | COMPUTATION, exact | 15 / 16 | -1 / 16 | 0 |
| Bob's marginal (+ / -) | COMPUTATION, exact (Theorem 5) | 96 / 96 | 96 / 96 | 96 / 96 (no signalling in the counts) |
| Alice's marginal (+ / -) | COMPUTATION, exact (Theorem 5) | 96 / 96 | 96 / 96 | 96 / 96 |
| Alice's serial correlation at lag 1 (cyclic) | COMPUTATION, exact | 15 / 16 | 15 / 16 | 0 |
| Same-sign pairs (A_t = B_t) of 192 | COMPUTATION, exact | 192 | 94 | (not compared) |
| Alice's setting sequence read at `alice_plus` | DETECTOR (the protocol's check) | 0 at every birth | the cycle (0, 21, 42) in the clock's order, one shift | (not compared) |
| The referee's a = 32, 0, 0 (no world) | COMPUTATION only | 15 / 16 | -5 / 16 | 0 |

Tolerance: exact. The wheel is a counter and the click a function of
(a, b, u) with no draw (P4), so every DETECTOR reading is an integer and
the fractions are exact; a deviation of one birth is a NO MATCH.

## 6. The refutation line

- A serial correlation of Bob's that is not the pinned value (15 / 16 or
  -1 / 16), or a marginal that is not 96 / 96, or Alice's sequence not
  the declared protocol, is **NO MATCH**: it refutes the algebra (the
  ladder as computed, or the register's reading of the chooser's stride),
  and the run is reported as such, no pin moved.
- A pinned value that is not 0 is the **FAIL** of the law against nature
  in the order: Bob's outcome sequence carries Alice's setting sequence,
  15 / 16 against -1 / 16 (and the referee's -5 / 16 by computation),
  while his counts stay 96 / 96. **PASS** would be Bob's serial
  correlation 0 under both settings sequences, which the algebra excludes.
- The counts' no-signalling (Theorem 5) is not at stake here and is not
  refuted by a FAIL in the order; the paper's claim "no signalling" is
  what the row candidate of RUN.md's last section narrows.
