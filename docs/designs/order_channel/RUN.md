# The order channel: the run and its readings

The run of [PINS.md](PINS.md) (the Order Channel Runner, 2026-09-22, on the
third referee read, record 938 (2) of [the log of 2026-09-20](../../LOG_2026-09-20.md)):
Bob's outcome ORDER after a detector under Alice's setting sequence, read
against the pins declared before the run. No pin moved after the run; no
engine code, registered pin, rule or world changed. Every number is
labelled by kind: DETECTOR (read off `events.jsonl` by
[order_reading.py](order_reading.py), its output [order_reading.out](order_reading.out)),
COMPUTATION (the pins, [order_pins.out](order_pins.out)), or nature (the
thing compared with).

## 1. The run

Branch `order-channel-run` from `main` at `02147ed5` (the pins committed
at `55788dc7` before the run); the shipped runner `python -m
event_universe --init <world> --output <dir>`, Python 3.14.0rc2 (the
project venv), headless, no frames, the outputs in the session's
scratchpad (the 24-hour retention; the readings are the record); source
sha256 `d537d4435b921895446b6ea36574b9c8d7b699ca028194c6ab8e344af9c2410e`
(the `src` tree of `02147ed5`, unchanged on the branch).

| World | World sha256 (`run.json`) | Intervals | Host time | Births analysed (ordinals; first u) |
| --- | --- | --- | --- | --- |
| `examples/events/bell/order_a0_b0.json` (Alice a = 0, Bob b = 0) | `4a61939a97d70ea7082b2dfed041aa0d026efff7ffe0ae64102451649c2cc716` | 212 of 212, completed | about 1 s | 192: the ordinals 1 .. 192, u = 0 |
| `examples/events/bell/order_a0_21_42_b0.json` (Alice a = 0, 21, 42 with period 3 from the chooser `sa`, Bob b = 0) | `b5dbfb48c76a5fb5a24dfffd8db984ec597239ecbcd77aaeb3164c3a07824df7` | 220 of 220, completed | about 1.4 s | 192: the ordinals 7 .. 198, u = 6 (the register's warm-up: six births meet no setting) |

The reading tool reads the record's one click (its `gather` line, the
channel per arm in `chosen`, Alice's arm first) in birth order (the
record's identity less 2^32), Alice's setting from the `window` on the
arm's `click` line at `alice_plus`, and the wheel value `u`; integers and
`fractions.Fraction` only. Each run: `escaped` 0 for every family, the
books balanced at every completed interval (`run.json`), only `birth`,
`click`, `record`, `gather` lines (and the chooser world's 12 `pass`
lines of the warm-up rows at `alice_plus`).

## 2. The readings against the pins

| Reading | Kind | Alice a = 0 (read) | Pin | Alice a = 0, 21, 42 (read) | Pin | Nature |
| --- | --- | --- | --- | --- | --- | --- |
| Alice's settings read at `alice_plus` | DETECTOR | 0 at all 192 births (period 1) | 0 | the values 0, 21, 42, the period 3, the first three 0, 21, 42 (the shift 0) | the cycle (0, 21, 42), one shift | (not compared) |
| u = (ordinal - 1) mod 64 on every analysed record; Alice + exactly for u < 32 | DETECTOR | yes; yes | Theorem 5 | yes; yes | Theorem 5 | (not compared) |
| Bob's marginal (+ / -) | DETECTOR | 96 / 96 | 96 / 96 | 96 / 96 | 96 / 96 | 96 / 96 |
| Alice's marginal (+ / -) | DETECTOR | 96 / 96 | 96 / 96 | 96 / 96 | 96 / 96 | 96 / 96 |
| Same-sign pairs of 192 | DETECTOR | 192 | 192 | 94 | 94 | (not compared) |
| **Bob's serial correlation at lag 1** (cyclic over 192) | DETECTOR | **15 / 16** | 15 / 16 | **-1 / 16** | -1 / 16 | **0** |
| Bob's serial correlation, open chain (191 pairs) | DETECTOR, unpinned | 181 / 191 | (start-dependent) | -13 / 191 | (start-dependent) | 0 |
| Alice's serial correlation at lag 1 (cyclic) | DETECTOR | 15 / 16 | 15 / 16 | 15 / 16 | 15 / 16 | 0 |

Bob's sequence over the first turn of the wheel, as read (DETECTOR):
under a = 0, 32 plus then 32 minus (`++++...----`, the square wave of
the first party); under a = 0, 21, 42, the first turn from u = 6 reads
`++-+--+--+--+--+--+--+--+-+-++-++-++-++-++-++-++-++-------++++++`.

**Verdicts.** Against the algebra: MATCH on every pinned reading of both
runs (16 of 16 checks; `order_reading.py` exit 0). Against nature: FAIL
in both runs. Bob's counts are 96 / 96 under both of Alice's sequences
(Theorem 5 holds after a detector, no signalling in the counts), and
Bob's ORDER is not: his serial correlation at lag 1 reads 15 / 16 when
Alice holds a = 0 and -1 / 16 when she cycles a = 0, 21, 42, nature's
value being 0 under either. The law's determinism (the wheel a counter,
P4's no draw) shows in the order of the outcomes, not in the counts: Bob's
outcome sequence carries Alice's setting sequence, one bit per 192 births
at these two sequences. The referee's own protocol a = 32, 0, 0 (-5 / 16)
is not declarable by the register's keys (PINS.md section 3) and stays a
COMPUTATION reproduced by `order_pins.py`; the expressible period-3
protocol reads the same channel with a smaller swing.

**Limits.** The A2 bar, N = 64, one pair per interval, the wheel [1, 64]
(u = the birth ordinal mod 64); a period-3 chooser whose stride the
register already used (`sb`); 192 births (one joint period). A longer run
repeats the sequence exactly (the wheel is a counter): more births add no
information. Whether a wheel that is not a counter (a draw, which P4
forbids) would close the channel is the physicist's and the owner's
question of record 938 (2), not this run's.
