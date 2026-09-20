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

- The lamp of `light` at x = 10: content K + 2 = 1048578 (so that the
  release of age a is stamped with the phase a mod 64 exactly for every age
  of the run), `phase` 0, one ray per self-creation on +X and on -X
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
- A pair is the two releases of one age of the lamp, both stamped with the
  same phase. A = +1 for a click at `alice_plus`, -1 at `alice_minus`; B
  likewise. The age of a click is its tick less its Node's offset, read off
  the record itself: the earliest click at a Node is the smallest age its
  window admits, whose phase is that age, so the offset is that click's
  tick less its phase (found: plus tick = age + 14, minus tick = age + 16).
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
