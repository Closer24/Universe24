# The Bell run A2 under the Beam Law

Ten worlds of one design, the settings the only difference between the files,
written by `make_worlds.py`; the register entry is
[A2, under the Beam Law (2026-09-19)](../../../docs/EXPERIMENTS.md#a2-under-the-beam-law-2026-09-19)
and the evidence is in [validation](../../../docs/VALIDATION.md). The model
owner asked for "a Bell experiment with an emitter and two detectors, Alice
and Bob, on a small GameBoard" ([Highlights 5.4](../../../docs/HIGHLIGHTS.md#54-the-detector)),
and the physicist and the mathematician pinned the verdict before the first
run under the law of events: with a deterministic local phase window each
click is a function of the arriving phase and the local setting alone, so
CHSH is at most 2 as an identity on the record, the correlation is the
triangle 1 - 4 k / N, and the CHSH settings give S = 2 exactly, the model's
limit. The design of [the Beam Law](../../../docs/BEAM_LAW.md), section
8, pinned the same verdict for `beam-v1` ("unchanged: S = 2 exactly"). The
run is made and registered as that limit, never as a confrontation the model
could pass. The registered run of the law of events (offsets 9 and 10, 138
intervals, fingerprint `53a70962...`) keeps its scope below.

## The design

One bar of 21 x 1 x 1 Nodes, open, `"law": "beam"`, K 2^20, N 64 (the
phase tables read a single arrival's step exactly only up to N = 64),
`release` [0, 1], `suspension` 0, the families `light` and `counter`, both
paid (`quantum` 1; the kind follows from the quantum), every measured event
`fixed`.

- The lamp of `light` at x = 10: content K + 2 = 1048578 (the smallest
  content that turned once per self-creation over the run under the count
  off the clock; since the fraction-free law of 2026-09-20, BEAM_LAW note
  41 (vii), a paid lamp paying 2 per birth keeps one birth per interval
  over T intervals from the least content K + T - 1, K + 159 here, the
  frame reading the content before the birth pays (K + 2 (T - 1), K + 318,
  suffices and is twice the least addition), and this lamp's exact
  clock, paying 2 per birth, stalls once, at tick 4: 159 births in 160
  intervals, the age of a pair its birth ordinal read off the record),
  `phase` 0, one ray per self-creation on +X and on -X
  (`lamp.directions`), no window: the source cycles the whole circle. Its
  two recoils cancel at each self-creation, so its momentum stays [0, 0, 0].
- Four counters of content 1, each its own detector of threshold 1, the
  table `{"light": {"phase_window": s}}` (the rule `measure` is what the
  keys give a paid family; the world declares only the window): `alice_plus`
  at x = 2 (s = a), `alice_minus` at x = 1 (s = a + 32 mod 64), `bob_plus`
  at x = 18 (s = b), `bob_minus` at x = 19 (s = b + 32 mod 64). A ray
  flies at 1 / sqrt 3 by the flight table: released at tick t it first
  walks at t + 1, the eight Links to a plus Node take 13 walks and the
  ninth two more. Outside the window a it passes (a `pass` record, the
  phase read and the setting) and reaches the minus Node two intervals
  later, where the complement takes it. The two windows of a side cover the
  circle exactly, so every ray clicks exactly once per side and nothing
  escapes.
- A pair is the two rows of one record of the lamp (one birth: the
  record's identity the lamp's number x 2^32 + the birth's ordinal,
  carried on every click and pass line). A = +1 for a click at
  `alice_plus`, -1 at `alice_minus`; B likewise. The age of a pair is its
  birth ordinal less one, read off the record on the line, and its phase
  is that age mod 64 (the record's u); the tick of a birth is not the age
  of the lamp's clock once the lamp pays (the stall at tick 4), so the
  reader never pairs by a tick offset. The tick offsets are reported as
  the flight's smallest tick - age at each Node (until the fraction-free
  law: the age read as the tick less the Node's offset, found plus tick =
  age + 14, minus tick = age + 16, one value per Node).
- 128 pairs analysed, the ages 0..127 (two full circles: E is exact for any
  multiple of N / 2); `ticks` 160, so that the last minus click of age 127
  (tick 143) is on the record; the ages 128 and after, still in flight or
  just arrived when the run ends, are excluded.

E(a, b) = (same - different) / 128, expected 1 - 4 k / 64 with
d = (a - b) mod 64 and k = min(d, 64 - d).

| World | a | b | k | Expected E | same / different | Reads |
| --- | --- | --- | --- | --- | --- | --- |
| `a0_b8.json` | 0 | 8 | 8 | +1/2 | 96 / 32 | CHSH, and S' |
| `a0_b24.json` | 0 | 24 | 24 | -1/2 | 32 / 96 | CHSH |
| `a16_b8.json` | 16 | 8 | 8 | +1/2 | 96 / 32 | CHSH |
| `a16_b24.json` | 16 | 24 | 8 | +1/2 | 96 / 32 | CHSH |
| `a0_b0.json` | 0 | 0 | 0 | +1 | 128 / 0 | control: equal settings |
| `a0_b32.json` | 0 | 32 | 32 | -1 | 0 / 128 | control: opposite settings |
| `a0_b16.json` | 0 | 16 | 16 | 0 | 64 / 64 | control: a quarter circle |
| `a0_b12.json` | 0 | 12 | 12 | +1/4 | 80 / 48 | S' |
| `a4_b8.json` | 4 | 8 | 4 | +3/4 | 112 / 16 | S' |
| `a4_b12.json` | 4 | 12 | 8 | +1/2 | 96 / 32 | S' |

S = E(0, 8) - E(0, 24) + E(16, 8) + E(16, 24) = 2 exactly, the CHSH bound;
S' = E(0, 8) - E(0, 12) + E(4, 8) + E(4, 12) = 3/2 exactly, a quadruple
that does not saturate the bound (the cosine of the phase difference at the
same settings would give 2 sqrt 2 = 2.828 and 1.739). Every run must also
show: the books balanced at every completed tick, `escaped` 0 for both
families, only `click`, `pass` and `record` records, the lamp's momentum
[0, 0, 0] at the end, each windowed Node clicking on exactly 64 of the 128
analysed pairs, exactly one outcome per side per age, every click's phase
equal to its age mod 64 and inside its Node's window, every pass at a plus
Node outside its window and clicking at the minus Node next; and, exact
no-signalling, the set of ages at which `alice_plus` clicks identical across
all runs with the same a whatever b, and Bob's likewise for the same b.

## Run and analyse

```bash
python examples/events/bell/make_worlds.py   # rewrites the ten worlds, unchanged
for s in a0_b8 a0_b24 a16_b8 a16_b24 a0_b0 a0_b32 a0_b16 a0_b12 a4_b8 a4_b12; do
  python -m event_universe --init examples/events/bell/$s.json --output artifacts/bell/$s
done
python tools/bell_chsh.py artifacts/bell
```

`tools/bell_chsh.py` (standard library, `fractions.Fraction`, no float in a
criterion) reads each run's `run.json`, `initialization.json` and
`events.jsonl`, prints per run the four counts, E and the expected E, then
S, S', the offsets and the fingerprint, and every criterion with its
verdict; a failed criterion exits nonzero. Every expectation is exact: a
deviation is a defect of the engine, the width or the bookkeeping, to be
reproduced minimally and reported, never tuned away. `tests/test_nature_beam_worlds.py`
(b) runs the ten worlds through the same tool as a check that the engine
does what the law says.

## Result under the Beam Law (2026-09-19)

Branch `claude/universe24-new-3ytqde`, the Beam Law's commits on the base
`ce0b22af`, source fingerprint `703f9427d9f70e6c619218e457edca0b7647381a8cc7a20d140e4a3d9dd3f671`, Python 3.14, headless,
about 0.2 s per run. Every count as pinned above: E +1/2, -1/2, +1/2, +1/2
at the CHSH settings, S = 2 exactly; the controls +1, -1, 0; E +1/4, +3/4,
+1/2 on the non-saturating quadruple, S' = 3/2 exactly; the offsets plus 14,
minus 16 in every run (the flight table's pace); no-signalling exact; 326
criteria checked, 0 failed. The model's limit, outcome 1 of A2 against the
2015 data, as the reviewers predicted and as BEAM_LAW section 8 expected; not
a law of nature. Limits: static settings declared in the world, no
last-moment choice; single rays one per interval per direction, the trivial
regime of the law (no collision between rays of one number on one line, no
suspension, a set of one at threshold 1); N = 64.

## Result under the law of events (2026-09-19, history)

Commit `1f9f280` on `main`, source fingerprint
`53a70962c5f2c8c860a0895dbc9d6cb7cf125d53aa3d5f0ce6aa5464c79a87f9`, Python
3.14.0rc2, 138 intervals, the offsets plus 9 and minus 10 (one Link per
interval): the same counts, S = 2 and S' = 3/2 exactly, 326 criteria, 0
failed. The engine of that run is deleted
([migration](../../../docs/MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1));
the reading keeps its scope.

## The choosers on the GameBoard (issue #363, 2026-09-20)

Seven more worlds of one design, written by `make_chooser_worlds.py` (its
docstring is the derivation); the register entry is
[A2 with the choosers on the GameBoard (2026-09-20)](../../../docs/EXPERIMENTS.md#a2-with-the-choosers-on-the-gameboard-2026-09-20).
The model owner's question ("Alice and Bob are part of the GameBoard, no?"):
in A2 the settings are numbers in the file, a hand from outside the
universe, so its S = 2 is established only given a free choice from
outside, and a deterministic model is suspect of superdeterminism (the
settings and the pairs correlated through a common past). Here each
counter's window is read from the phase of a ray arriving from a third
source (Alice's) and a fourth (Bob's), the key `phase_window` `{"reads":
"<family>", "offset": s}` ([ENGINE](../../../docs/ENGINE.md#the-beam-law-beam-v1),
[BEAM_LAW note 34](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
the settings are events of the GameBoard with a past of their own, and
the question is whether the law carries a correlation from the initial
state to things that never met. The prediction, written before the run:
S = 2 exactly with every E on the triangle, the marginals 1/2.

### The design

The bar of 21 x 1 x 1 and the pair lamp of `light` at x = 10 as in A2
(content K + 2, the phase a mod 64 on the release of age a), K = 15 x 2^20
(divisible by 15, and large enough that the pair lamp's turn stays exactly
1 over 1940 intervals), N 64, `suspension` 0, `release` [1, 2^26], the
families `light` and `counter` (paid) and `sa` and `sb` (free, a phase
circle each; different families never collide). Two setting lamps, free
measured events held in place: `sa` at x = 0 (content 64 K / 5, phase 7,
one row of 3 units per interval toward +X: its clock turns 12, 13, 13, 13,
13 steps per interval, the phases 7, 19, 32, 45, 58 and again, the period
5) and `sb` at x = 20 (content 64 K / 3, phase 40, one row of 5 units per
interval toward -X: the turns 21, 21, 22, the period 3). A free release
costs nothing, so the turns stay exactly periodic; a paid lamp's content
falls and its turn drifts. The three lamps share nothing: different
strides (1, 12.8, 21.3), different starting phases (0, 7, 40), and no
suspension (no clock reads another's rays). Four counters of content 1,
each its own `wave` detector of threshold 1, passing `sa` and `sb`
(`pass`: no push, no record, the rays go on to the faces) and measuring
`light` through a window read from the stream of their side:

| Counter | x | Links from its lamp | `sa` / `sb` rows at its Node | `light` entry | Reads |
| --- | --- | --- | --- | --- | --- |
| `alice_plus` | 7 | 7 | 1 (the flight age 12) | `{"reads": "sa", "offset": 57}` | the ray's phase + 57 |
| `alice_minus` | 4 | 4 | 1 (the age 7) | `{"reads": "sa", "offset": 25}` | the same + 32 |
| `bob_plus` | 17 | 3 | 2 (the ages 5, 6) | `{"reads": "sb", "offset": 0}` | the pointer of two consecutive releases |
| `bob_minus` | 18 | 2 | 2 (the ages 3, 4) | `{"reads": "sb", "offset": 32}` | the same + 32 |

Why these Nodes and periods: a ray of a heading dwells one or two
intervals at a Node (32 Links per 55 intervals), so a stream of one row
per interval holds a constant one or two rows at each Node; the plus and
minus counters of a side must read the SAME setting for one pair, or the
minus window is not the complement of the plus window and pairs are lost,
so the stream's phase must be periodic in the releases with a period that
divides the shift between the two readings (10 releases for Alice, 3 for
Bob); and the periods must be odd, coprime to each other and to the
circle of 64, so that every (a, b) combination meets every phase of the
pair lamp equally (the joint period 15, the pair's 64: over 960 pairs each
of the 15 combinations sees each phase once). A two-valued setting from
one clock (0 / 16) has a period that divides 64 and would share a residue
of the interval with the pair's phase: a correlation built by the file.
The offsets put Alice's settings at 0, 12, 25, 38, 51 and Bob's at 8, 29,
51 (the bisectors of 40/61, 61/18 and 18/40, read with the engine's
tables); the quadruple read is Alice's 0 and 25 with Bob's 8 and 29
(0 < 8 < 25 < 29, within a half circle: the triangle gives S = 2 on it).
The pair ray of age a reaches x = 7 at tick a + 6, x = 4 at a + 11, x = 17
at a + 13 and x = 18 at a + 14; the first `sa` ray reaches x = 7 at tick
13, so the pairs 0..6 are the warm-up (no setting at Alice's plus counter)
and the ages 7..1926, 1920 pairs (128 per combination), are analysed;
1940 intervals.

| World | What differs | Reads |
| --- | --- | --- |
| `read.json` | the run | every E, S, the largest S over the 5 x 3 settings' quadruples, the marginals |
| `written_a0_b8.json`, `written_a0_b29.json`, `written_a25_b8.json`, `written_a25_b29.json` | control 1: the streams present, the windows written in the file (A2's form), 128 pairs each | S = 2 over the four |
| `fixed.json` | control 2: the streams released with the settings fixed (the lamps' contents 3 and 5 at `release` [1, 1], the turn 0; Alice's phase 0, Bob's 8) | E(0, 8) = 1/2, A2's |
| `one_clock.json` | control 3: the three lamps fed from one clock (the setting lamps with the pair lamp's stride 1 and phase 0, content K at `release` [1, K]) | a correlation built in on purpose, seen |

### Run and analyse

```bash
python examples/events/bell/make_chooser_worlds.py   # rewrites the seven worlds, unchanged
for w in read written_a0_b8 written_a0_b29 written_a25_b8 written_a25_b29 fixed one_clock; do
  python -m event_universe --init examples/events/bell/$w.json --output artifacts/bell363/$w
done
python tools/bell_choosers.py artifacts/bell363/read --replay 20
python tools/bell_choosers.py artifacts/bell363/written_a0_b8 artifacts/bell363/written_a0_b29 \
    artifacts/bell363/written_a25_b8 artifacts/bell363/written_a25_b29
python tools/bell_choosers.py artifacts/bell363/fixed
python tools/bell_choosers.py artifacts/bell363/one_clock
```

`tools/bell_choosers.py` (standard library and the engine's own functions
for the replay; `fractions.Fraction`, no float in a criterion) reads the
offsets off the record (tick - phase mod 64, one value per counter), bins
the pairs by the window carried on the plus counters' click and pass
lines, checks that every minus window is the plus window's complement,
that every analysed age has exactly one outcome per side, that every
click is inside its window and every pass outside, and prints per bin the
counts, E, the triangle and the marginals, S on the quadruple, the largest
S over every quadruple that occurred (the four placements of the minus
sign) against the triangle's own, and no-signalling (each side's marginal
per own setting, equal across the other side's settings), every line
labelled DETECTOR or GAMEBOARD (`--replay`: the rows of the streams at the
counters' Nodes per interval). `tests/test_bell_choosers.py` pins the tool
to the engine on a minimal case; no test pins these worlds' numbers.

### Result (2026-09-20)

The worktree of `claude/universe24-new-3ytqde` from its tip `9379b01c`
with the key added, source fingerprint
`38792132301970e7c276cfee4184534dcd2223fe3a4d906c78be3714afd5c142`,
Python 3.14.0rc2, numpy 2.5.3, headless, about 5 s for 1940 intervals.
`read`: the offsets 6, 11, 13, 14; the warm-up 7; 1920 pairs in 15 bins of
128; every E the triangle exactly (E(0, 8) = 1/2 with 48 / 16 / 16 / 48,
E(0, 29) = -13/16, E(25, 8) = -1/16, E(25, 29) = 3/4, E(51, 51) = 1, and
the ten others); S = 2 exactly on (0, 25) x (8, 29); the largest S over
the 5 x 3 settings' quadruples 2, on (0, 12) x (8, 29), the triangle's
own; every marginal 1/2 exactly; 46 criteria, 0 failed. The controls: the
four written worlds S = 2 exactly, 91 criteria, 0 failed; `fixed`
E(0, 8) = 1/2 (48 / 16 / 16 / 48), 24 criteria, 0 failed; `one_clock` 64
bins of one phase each, E = 1 in every bin (both plus counters click every
pair, the minus counters never), no quadruple of settings occurs, 68 of
214 criteria failed: the correlation built by the file is seen. The
verdict: the law does not correlate what never met; Bell's assumption is
a measurement here, not an assumption; S = 2 stands with the choosers on
the GameBoard, the model's limit as before.
