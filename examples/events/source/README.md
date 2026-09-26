# The run files of the source verb

The ledger's primitive "source" (docs/designs/generic_engine/ENGINE_LEDGER.md, section 3), given
to Nature24 by the Boss's record 2217 of 2026-09-26 on the model owner's word: the run files
first, the algebraic line checked with the mathematician, the function on the short branch
`feature/source` against Main Loop's interface once it is agreed, no engine code before. The
generator is `make_worlds.py`; the test is `tests/test_source_worlds.py`. No pin (9.59 (6)); every
number is labelled: GAMEBOARD (a diagnostic the run writes), COMPUTATION (the declaration's
arithmetic), HOST (the machine's cost).

    PYTHONPATH=src python examples/events/source/make_worlds.py

## 1. What is under test, and what is not

The source verb alone: a family declared `sourced` by a record family gains, at every Node of the
record's support, the record's local count each interval, and nowhere else; the unsourced family
beside stays exactly zero; the stationary level is the static response of the sourced family's own
pair; the inverse subtracts the same integers. Nothing reads the sourced family back: the matter
family keeps the shipped reads (gravity, charge), so there is no well and no binding here. The
well is closed as beyond the rule (record 2199; ALGEBRA.md 9.113 item 3 (a)) and its run files
are not written.

## 2. The declarations

The words are the check-mode generator's (record 2128: `universe` a path, `q`, `stocks`; no
momentum or spin on a body; a moving body is its record with its tail). Two declarations the
loader lacks today are written as the ledger's table names them, for Main Loop's interface:

| Declaration | Where | Form | Meaning |
| --- | --- | --- | --- |
| `sourced` | the sourced family's entry of the universe file | `{"of": "matter", "weight": 1, "scale": 18910}`, with `"cap": 60` on the table form | the family gains weight x s_i at every Node of a `matter` record; s_i = D_i div E_s with E_s the scale; with the cap s_i = cap D_i div (cap E_s + D_i) |
| `readings` | the world file | a list of `{name, kind, ...,  every}`, the name unique in the world (`level_field_16_16_16`, `support_field`, `total_control`, `centre_body_0`) | what the run writes under its name, each a GameBoard reading: `level` (a family's level at a Node), `total` (a family's sum of absolute levels), `support` (the count of Nodes with a nonzero level), `centre` (a family's or a body's centre) |

THE ONE UNIVERSE (record 2075): every world names the shipped `examples/events/universe.json`,
and the three families of these runs are the folder's fragment `universe_entries.json`, the
entries to append to the shipped file the day the loader reads `sourced` (never a second universe
file; the test checks the fragment and that no universe file lies in the folder):

| Family | `parts` | `phase` | `pair` | `reads` | `self_source` | `sourced` |
| --- | --- | --- | --- | --- | --- | --- |
| `field` | [1] | 2 | [1000, 1019] | [] | {unit 0} | by `matter`, weight 1, scale 18,910: the plain count |
| `field_table` | [1] | 2 | [1000, 1019] | [] | {unit 0} | by `matter`, weight 1, scale 18,910, cap 60: the saturating table |
| `control` | [1] | 2 | [1000, 1019] | [] | {unit 0} | none: the leak test's family (record 2075 (3)) |

The pair [1000, 1019] (COMPUTATION): kappa^2 = 6 den / num - 6 = 0.114, the range 1 / kappa =
2.96 Links, the gap omega_0 = arccos(num / den) = 0.193 per interval (a period of 32.5
intervals). The numbers are ALGEBRA.md 9.108 item 11's, used here for the short range alone: a
level that falls by e every three Links shows the source's locality on a small GameBoard.

## 3. The worlds

Every body is the check-mode body: a well of side 5 with the pair [800, 801], 2000 quanta of the
kind [800, 850], the record seeded on its bound mode at the amplitude 2^12 (HOST, the massive
generator's operator); the GameBoard open on six faces (the faces the counters, `face_depth` 1).
The run is 300 intervals.

| World | GameBoard | The body | The readings |
| --- | --- | --- | --- |
| `source_rest.json` | 32 x 32 x 32 | at rest, centre [16, 16, 16] | `field` and `field_table` at the centre and at the far Node [28, 16, 16] every interval, their supports; `control`'s total |
| `source_moving.json` | 48 x 32 x 32 | moving along +x at v = 0.1 from the centre [10, 16, 16] (its record with its tail, K = 0.10723 per Link, omega_K = 0.34312, the rotation at the moving centre 0.3324 per interval; HOST) | the same at the start's centre and its far Node [22, 16, 16], and the centres of `field` and of the body every 10 intervals |

Both sourced families act in both worlds (everything on in every run, record 2075): `field` by
the plain count s_i = D_i div 18,910, `field_table` by the table s_i = 60 D_i div (60 x 18,910 +
D_i); neither is read by anything, so their levels are independent.

## 4. The numbers (COMPUTATION, the generator's)

The record's count at the start: the seed writes both levels the profile p_i (the rotation's
symmetric point), so D_i = now^2 - next x before = p_i^2 (2 b - a) div b with the mode's clock
[a, b] (2 cos omega = a / b; the rest world's [1978960, 1048576], omega = 0.337 per interval).

| Number | Rest, `field` | Rest, `field_table` (cap 60) | Moving, `field` | Moving, `field_table` |
| --- | --- | --- | --- | --- |
| the profile's peak | 4096 | 4096 | 4096 | 4096 |
| D at the peak Node | 1,891,072 | 1,891,072 | 1,895,312 | 1,895,312 |
| E_s (the universe's integer, D_peak div 100 of the rest world) | 18,910 | 18,910 | 18,910 | 18,910 |
| the count at the peak Node per interval | 100 | 37 | 100 | 37 |
| Nodes with a count of 1 or more (the source's support; a ball of radius 8.0) | 2169 | 2109 | 2068 | 2062 |
| the total count per interval | 14,887 | 10,431 | 14,698 | 10,335 |
| the static level at the centre (the stationary equation below) | 596.4 | 309.8 | 596.4 at the start | 309.3 at the start |
| the static level at the far Node, 12 Links along +x | 7.0 | 5.2 | 7.3 | 5.4 |
| the static level summed over the GameBoard | 387,334 | 270,945 | 374,413 | 262,461 |

The stationary equation (ALGEBRA.md 9.108 item 11, the combine line of 9.112 item 2 at rest with
the count added after every step, w = 2 num Gamma^2 and W = 6 den Gamma^2): SUM over the six
neighbours of (a_j - a_i) - kappa^2 a_i = -(3 den / num) s_i, the level zero beyond the open
faces, solved on the GameBoard by a sparse direct solve (HOST floats; the run's integers differ
by the remainders, under one level unit per Node).

## 5. What the readings should show (the blind expectations, no pin)

1. **Locality (`support`).** At interval t the Nodes with a nonzero `field` level lie within the
   source's support grown by t Links along the axes (the rule moves a level one Link per interval);
   the far Node of the rest world, 4 Links beyond the support's radius, reads exactly 0 for the
   first intervals and then rises toward 7.0.
2. **The leak (`total` of `control`).** Exactly 0 at every interval; the runner's leak test
   (record 2075 (3)) says the same.
3. **The level at the centre (`level`).** From 0 at the start toward the static level 596.4 (the
   table: 309.8); an undamped family switched on from zero rings about its static level at the
   gap's period, up to twice the static level (9.108 item 11's reason for the stationary start);
   the mean over the intervals 100 to 300 within 10 percent of the static level. The `start`
   "stationary" declaration of the ledger's run table, when it lands, removes the ringing.
4. **The moving record (`centre`).** The centre of `field` follows the centre of the body: the
   difference along x under one Link over the run, the body 30 Links further at the end.
5. **The inverse (the small test, not a reading).** A run of n intervals forward and n backward
   returns the start bit for bit, the source's writes subtracted where they were added (the form
   of the reversibility test of tests/test_ledger_items.py item 7).

## 6. The algebraic line, as it stands, and the questions to the mathematician

The line the run files declare (ALGEBRA.md 9.116 item 4b; 9.108 items 11 and 13; 9.112 row 6;
the ledger's source row):

- the argument: D_i = now_i^2 - next_i x before_i of the sourcing record at Node i, read at the
  end of the record's step from the three levels the Node has at that moment (9.108 item 13; A^2
  sin^2 omega for one rotation, never negative for a bounded level);
- the count: s_i = D_i div E_s, the remainder 0 <= r_i < E_s on the record; the table form s_i =
  s_cap D_i div (s_cap E_s + D_i);
- the write: the sourced family's level at Node i gains weight x s_i, entering at t + 1 (9.111
  item 6); the inverse subtracts the same integer;
- the place: (iv), beside the hold.

The five questions, each one line, sent to the mathematician with this page (his answer decides
the function, not these files):

1. **Whole or divided.** 9.108 item 11 adds s_i to the level after the family's step (level += w
   s_i); 9.112 row 6 and 9.116 list the source among the combine line's loads, which are divided
   by W = 6 den Gamma^2. Which? These files and section 4 take item 11's form.
2. **The remainder.** r_i = D_i mod E_s "on the record": added to the next interval's D_i (a state
   of the record, restored by the inverse), or dropped each interval (nothing stored)?
3. **The timing.** D_i needs next, so the first write follows step 0 and enters the level at
   interval 1; the writes of interval t are applied after all families' steps of t and read from
   t + 1 (9.111 item 6). Confirmed?
4. **The table's remainder.** With the varying modulus s_cap E_s + D_i, no remainder is kept, the
   quotient alone (the table a declaration beyond the rule). Confirmed?
5. **The moving record.** The field's centre trails the body's by under one Link at v = 0.1 with
   the gap 0.193 per interval (section 5 item 4): the algebra's number, or another?

## 7. State

- The two worlds load in no loader today: the world is refused at `readings`, then at the
  residue keys K, N, release (the check-mode worlds' state, record 2199 item 2 and the acceptance
  test (e3)); the fragment's `sourced` is refused by the universe file's reader until the word
  lands, so the fragment is appended to the shipped file that day and not before (every shipped
  world would be refused). `tests/test_source_worlds.py` reads the structure and holds the load
  as an expected failure (strict) that turns green with the words.
- The function of the source is not written here: it waits for Main Loop's interface (record
  2217 (2)); its red test is tests/test_ledger_items.py test 3a; APPROVED-MATH and the Boss's
  merge follow the cut.
