# Series P: the hand

The worlds of series P, written by `make_worlds.py`; the register entry is
[P, the hand (2026-09-20)](../../../docs/EXPERIMENTS.md#p-the-hand-2026-09-20).
The decision, in the model owner's words (record 128 of
[the log](../../../docs/LOG_2026-09-20.md), "the hand's three choices
confirmed"): `hand-v1` built with the three choices of the physicist's
design (hand/DESIGN.md, record 122; the mathematician's integer form,
record 120) taken as physics over convention: (i) a left-handed product
leaves AGAINST the parent's axis, Wu's side; (ii) the strict hemisphere
only, the equator not admitted; (iii) the hand's home on the family as
`charge` is, with a lamp's and a transit row's hand, an unpolarised parent
lawful. The law's side is [BEAM_LAW note 39](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation):
one column `hand` on the row (-1, 0, +1; 0 everywhere without a
declaration), one axial record `axis` on the measured event (one of the six
headings), the right-hand rule at the birth of a `become` product
(sign(A . u_d) = h), the parity filter `hand` on a table entry, `hand` on
the click and `become` lines, `left` and `right` per family in the books.
A research run, made once, never a test (`tests/test_hand.py` pins the rule
on minimal GameBoards and runs the parity test on these worlds as a
comparison of two runs of one world, not a number); every expectation
below was written before the run, from the design's integers and the
engine's own documented rules, and a reading outside its expectation is
reported with its numbers, never moved. Every number is one of two kinds
([the register](../../../docs/EXPERIMENTS.md), "Two kinds of readings"): a
DETECTOR reading (a reader's clicks and passes, a face's click) or a
GAMEBOARD reading (a body's `become` line, the flight table's first
arrival, the recoil).

## The worlds

| World | The bar | What it re-states |
| --- | --- | --- |
| `w_hand` | 7 x 1 x 1, K 2^20, N 64, `release` [1, 2^20], `suspension` 0, 16 intervals | the W world (`weak/w_exchange`) with a second proton: `p` (free, charge 4 per unit of content) of 1836 fixed at x = 1 and at x = 3, each with the entry `w: {rule measure, hand -1}`; the neutron `n` (1839, fixed) at x = 2 with `directions` `[[1, 0, 0], [-1, 0, 0]]`, `axis` `[-1, 0, 0]` and `become` `{at 8, into p, products [["w", 1, 3]]}`; the W family `w` (paid, quantum 1, charge -7344 per unit of amount, `lifetime` 1, `hand` -1) |
| `w_two_sides` | the same bar | the control: the same world with `axis` and every `hand` removed (the protons then read the W by the keys' `measure`) |
| `wu` | 17 x 1 x 1, K 2^20, N 64, `release` [1, 2^20], `suspension` 0, 40 intervals | Wu's experiment: the neutron (1839, fixed) at x = 8 with `axis` `[1, 0, 0]`, the six headings, `become` `{at 8, into p, products [["beta", 1, 3], ["nubar", 1, 0]]}` (the charges 7344 - 7344 = 0 against 0); `beta` (paid, quantum 1, charge -7344, `hand` -1), `nubar` (free, `hand` +1); readers of `d` (paid, content 1) at x = 0 and x = 16 measuring `beta` by the keys' rule and passing `nubar` (`nubar: pass`) |
| `nu_hand` | 200 x 1 x 1, K 4096, N 64, `release` [1, 4096], `suspension` 0, 1037 intervals | J2's bar (`weak/j2_default`): the fixed source of `nu` (content 4096, one ray per self-creation on +x, the phase (t - 1) mod 64) with the family `nu` given `hand` -1; readers of `d` at x = 8 (`nu: {rule measure, phase_window 0, phase_width 64, hand +1}`: the full circle, the right hand only) and at x = 9 (the same with `hand` -1); the far detector at x = 190 measuring `nu` without a window |

## The expectations, pinned before the runs

The right-hand rule: a product of hand h at a parent with the axis A is
born only on the parent's directions d with sign(A . u_d) = h; a
left-handed product leaves against the axis. The tie rule of the
apportioning at a self-creation is the engine's as documented (BEAM_LAW
note 36 (iii), `tests/test_become.py` (a): the leftover counted from
(clock age + k) mod n, the clock age at the self-creation that fires `at`
being at - 1). The first-arrival ages off the flight table on a heading
(`weak/make_worlds.py`, `first_arrival_age`): 8 Links at the age 13,
9 Links at 15, 190 Links at 326.

| World | Reading | Expected |
| --- | --- | --- |
| `w_hand` | the `become` line at tick 8 (GAMEBOARD) | trigger "clock", from `n` into `p`, the products `[["w", 1, 3, [1, 0, 0], -1]]` (A = -e_x, h = -1: sign(A . u_{+x}) = -1 admits +x, sign(A . u_{-x}) = +1 refuses -x; the admitted set is one direction, the tie has nothing to choose), the recoil `[-192, 0, 0]` |
| `w_hand` | the click (DETECTOR) | tick 9 at measured 3 (x = 3): `w`, amount 1, content 3, push `[192, 0, 0]`, `hand` -1; measured 1 (x = 1): 0 clicks of `w`; the border `lifetime`: 0 |
| `w_hand` | the charge line (GAMEBOARD) | `[14688, 1]` at every tick: two protons of 7344 (the design's table wrote `[7344, 1]` "unchanged from `w_exchange`", which has one proton; the second proton the design adds carries its own 7344, an arithmetic of the declaration, not of the run) |
| `w_hand` | the books | `w`: released 1, measured 3 (the content line), `left` 1, `right` 0; `hypotheses` `["columns-v1", "weak-v1", "hand-v1"]` |
| `w_two_sides` | the click (DETECTOR) | one W unit apportioned over the two declared directions with the leftover at (clock age 7 + 0) mod 2 = 1, the second declared direction `[-1, 0, 0]`: the click at measured 1 (x = 1) at tick 9, push `[-192, 0, 0]`, the recoil `[192, 0, 0]`; no `hand` on any line; `hypotheses` `["columns-v1", "weak-v1"]` (the design's 3.1 read the clock age as 8 and pinned measured 3; the engine's documented tie reads at - 1 = 7, a derivation before the run, and the control's verdict under the mirror below does not depend on which side the tie takes) |
| `wu` | the `become` line at tick 8 (GAMEBOARD) | `beta` on `[-1, 0, 0]` with `hand` -1 (h = -1: against the axis +x; among the six headings one direction is admitted, the four perpendicular ones refused with the one along), `nubar` on `[1, 0, 0]` with `hand` +1; the labels (-192, 0, 0) and (64, 0, 0); the recoil `[128, 0, 0]` |
| `wu` | the beta's click (DETECTOR) | tick 8 + 13 = 21 at the reader at x = 0: `beta`, amount 1, content 3, `hand` -1, push `[-192, 0, 0]`; the reader at x = 16: 0 clicks of `beta` |
| `wu` | the antineutrino (DETECTOR) | a `pass` line at the reader at x = 16 at tick 21 (`hand` +1), then the click on `face:+x` at tick 8 + 15 = 23 (9 Links: the reader is 8 from the neutron, the face one beyond), momentum `[64, 0, 0]`, `hand` +1 |
| `wu` | the books | `beta`: released 1, `left` 1, `right` 0; `nubar`: released 1, escaped 1, `left` 0, `right` 0; the charge line `[0, 1]` at every tick; `hypotheses` `["weak-v1", "hand-v1"]` |
| `nu_hand` | the reader at x = 8, hand +1 (DETECTOR) | 0 clicks: every ray is left-handed and passed (a `pass` line per arrival, 1024 of them, each `hand` -1) |
| `nu_hand` | the reader at x = 9, hand -1 (DETECTOR) | 1022 clicks (the rays born at the ticks 1 .. 1037 - 15), every click `hand` -1 |
| `nu_hand` | the far detector at x = 190 (DETECTOR) | 0 |
| `nu_hand` | the books | `nu`: `left` 1022, `right` 0; `hypotheses` `["hand-v1"]` |

**The parity test** (the design's 1.3 and 3.2; `tests/test_hand.py` (d)):
under a signed axis permutation g every polar thing goes by g (positions,
directions, momenta), the `axis` as an axial vector det(g) g A, and every
`hand` is copied verbatim (the law's data); the readings mapped back by the
Node map. Under the probe's mirror in x (positions x -> shape_x - 1 - x,
every polar vector negated in x; an axis along x its own image, so its
axial transform is a verbatim copy on these worlds). Pinned before the run: `w_hand` DIFFERENT, by exactly the click moving from
measured 3 (x = 3) to measured 1 (x = 1), the product's direction
`[1, 0, 0]` against the mapped-back `[-1, 0, 0]`, the recoil `[-192, 0, 0]`
against `[192, 0, 0]` and the push `[192, 0, 0]` against `[-192, 0, 0]`; the
tick 9, the amounts, the contents, the charge line and the border equal.
`w_two_sides` EQUAL (its tie is on the declared list order, which the
mirror keeps). `wu` DIFFERENT: the beta's click at x = 16 against x = 0,
the antineutrino's face `-x` against `+x`. `nu_hand` EQUAL (a hand without
an axis is a datum a mirror cannot see). Over all 48 signed axis
permutations: the parity image differs under exactly the 24 improper
elements (det -1) and under none of the 24 proper ones on `w_hand` and
`wu`, and under none of the 48 on `w_two_sides` and `nu_hand`; and the
full transform (every hand by det(g) too: the law's data mirrored with the
state) is EQUAL under all 48 on every one of the four. A world in which the
full transform differs, or the parity image differs under a proper
rotation, is a defect of the build, not a parity reading.

## What was measured (2026-09-20)

Every reading inside its pin (the four runs through `tools/run_series.py`,
all balanced): `w_hand` the `become` line at tick 8 with the products
`[["w", 1, 3, [1, 0, 0], -1]]` and the recoil `[-192, 0, 0]`, the click at
tick 9 at measured 3 with the push `[192, 0, 0]` and `hand` -1, nothing at
measured 1, the border 0, the charge line `[14688, 1]` at every tick, the
books `w` released 1, measured 3, `left` 1, `right` 0, `hypotheses`
`["columns-v1", "weak-v1", "hand-v1"]`; `w_two_sides` the product on
`[-1, 0, 0]`, the click at measured 1 at tick 9 with the push
`[-192, 0, 0]`, no `hand` on any line; `wu` the `become` line with
`[["beta", 1, 3, [-1, 0, 0], -1], ["nubar", 1, 0, [1, 0, 0], 1]]` and the
recoil `[128, 0, 0]`, the beta's click at x = 0 at tick 21 (`hand` -1, the
push `[-192, 0, 0]`), the antineutrino's click on `face:+x` at tick 23
(`hand` +1, momentum `[64, 0, 0]`), the charge line `[0, 1]`, `beta` `left`
1; `nu_hand` 1024 `pass` lines (`hand` -1) and 0 clicks at x = 8, 1022
clicks at x = 9 every one `hand` -1, 0 at the far detector, `nu` `left`
1022, `right` 0. One line of the pins is outside its written form and
inside its physics: the antineutrino's passage at the reader at x = 16
writes no `pass` line, because a `pass` rule never writes one (the rows at
a `pass` entry are not met by the table, in every registered world since
the Beam Law's first day; the `pass` lines of the record are the rows a
`read`, `measure`, `rerelease` or `become` entry did not take); the passage
is shown by the face click at tick 23 as pinned. The cause is the record's
form, read wrongly by the design's 3.4 and by the pin above; the pin is
kept as written and the reading reported. The parity test on the four
worlds gave the verdicts pinned above (`tests/test_hand.py` (d)), the
full mirror and the rotation equal on all four.

## Running

```bash
python examples/events/hand/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/hand examples/events/hand/*.json
```

Each run takes a few seconds; `nu_hand` about 3 s.
