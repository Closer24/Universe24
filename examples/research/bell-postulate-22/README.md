# Bell and postulate 22: four experiments on the bonded pair

Current builders and new result stamps explicitly select
`historical-autonomous-v1` under the
[sampling admission contract](../../../docs/DETECTOR_SAMPLING.md).
These bonded-registry experiments do not implement canonical external Detector
ownership. The dated results below remain unchanged historical evidence.

Exploration evidence of 2026-09-16 at commit `e5b5911`, source fingerprint
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`
(Python 3.14.0rc2, headless). Nothing here changes the engine; every world is a
research configuration (`model_id` `bell-chsh-ray-probe-v1-exploration`)
built by `common.py` on the pattern of the [Bell probe](../../bell-chsh/README.md)
with `capture = "bond"`, and every number is a read-only audit of the world's
inventory and of the questions asked to the
[bond registry](../../../docs/QUANTUM_CLASSICAL_COUPLING.md), logged through a
wrapper around one registry instance owned by one `Simulation` object.

The question, in the words of
[hypothesis 1](../../../docs/HYPOTHESES.md#1-the-lottery-is-the-only-door-for-outside-information)
and [historical postulate 22](../../../POSTULATES.md#22-historical-autonomous-sampling-candidates):
if every uncertain outcome is the value of one bounded integer read by both
ends of a bonded pair, then (E1) the integer's influence must stay inside the
light cone of the asking ends, (E2) the outcome must not depend on which end
asks first nor on a setting chosen after the ask, (E3) settings drawn from the
world's own number generator must not correlate with the pair's number, and
(E4) each pair must own exactly one number, drawn once.

## Files

| file | role |
| --- | --- |
| `common.py` | world builder, logged registry wrapper, statistics (CHSH, chi-square, mutual information), `--output` handling |
| `e1_lightcone.py`, `e1_strict_check.py` | E1 run and its post-hoc strict cone check |
| `e2_order_delayed.py`, `e2_marginal_check.py` | E2 run and the registry-only marginal follow-up |
| `e3_free_choice.py`, `e3_salted_followup.py` | E3 run and the 16-seed registry follow-up |
| `e4_birthcode.py` | E4 run |
| `summarize.py` | compiles the four result files into `summary.json` |
| `results/summary.json` | the recorded compilation |
| `results/e*/expectations.json` | pre-registered predictions and pass/fail rules, written before each run |
| `results/e1_lightcone/strict_check.json`, `results/e2_order_delayed/{results,marginal_check}.json`, `results/e3_free_choice/{results,salted_followup}.json`, `results/e4_birthcode/results.json` | recorded outputs |

Not committed: `results/e1_lightcone/results.json` (1.3 MB of per-tick world
diffs; `e1_lightcone.py` regenerates it in 19 s).

## Commands

```sh
export PYTHONPATH=src
OUT=artifacts/research/bell-postulate-22
python examples/research/bell-postulate-22/e1_lightcone.py --output $OUT          # 18.7 s
python examples/research/bell-postulate-22/e1_strict_check.py --output $OUT
python examples/research/bell-postulate-22/e2_order_delayed.py --workers 4 --output $OUT   # 1578 s
python examples/research/bell-postulate-22/e2_marginal_check.py --output $OUT     # 3 s
python examples/research/bell-postulate-22/e3_free_choice.py --workers 4 --output $OUT     # 656 s lattice; --skip-lattice 6 s
python examples/research/bell-postulate-22/e3_salted_followup.py --output $OUT    # 30 s
python examples/research/bell-postulate-22/e4_birthcode.py --workers 4 --output $OUT       # 807 s
python examples/research/bell-postulate-22/summarize.py --output $OUT
```

Re-run at packaging (commit `d5d2427`): `e1_lightcone.py` (all 144 pairs pass
again, 18.1 s), `e1_strict_check.py`, `e3_free_choice.py --skip-lattice`,
`e2_marginal_check.py`, `e3_salted_followup.py` and `summarize.py`, all with
the recorded numbers reproduced. Not re-run: `e2_order_delayed.py`,
`e4_birthcode.py` and the lattice half of `e3_free_choice.py` (26, 13 and 11
minutes of host time).

## E1: the light cone of one integer

Two worlds identical except the single pair's registry number, supplied
through `bond.stream = [n]`; every tick's snapshot and inventory of both worlds
is diffed. Variants per case: `control_same_number` (the world's own number),
`coin_flip` (upper half flipped, lower half kept within one unit) and
`agreement_flip` (coin kept, lower half moved across the agreement threshold
of the settings' difference). Cases: 3 geometries (plus detectors at 3 and 3,
3 and 5, 5 and 3 links) x 2 setting pairs ((0, 8), (16, 24)) x 8 seeds = 48
cases, 144 world pairs.

| measurement | N | result |
| --- | --- | --- |
| control diff empty at every tick | 48 cases | 48 of 48 |
| differing Nodes outside the union of forward cones (loose check) | 96 variant pairs | 0 |
| differing Nodes outside the cone of an end whose **answer** changed (strict check) | 96 variant pairs | 0 |
| ends whose answer changed | 96 variant pairs | both 48, Bob only 32, Alice only 16, none 0 |
| first differing tick | 96 variant pairs | `coin_flip`: 4 in 48 of 48; `agreement_flip`: 4 in the 16 symmetric cases, 6 in the 32 asymmetric ones (the second asker at 5 links asks in the step from tick 5) |
| slack of the front (Manhattan distance minus cone radius; 0 = on the edge) | 37,824 differing Node-ticks | 0: 8,640; -1: 8,352; ... -8: 32; none positive |

Pass against `expectations.json`: yes (no difference outside the cones, none
before the first ask, control empty).

## E2: who asks first, and delayed choice

(a) Alice's plus detector at 3 links and Bob's at 5 (Alice asks in the step
from tick 3, Bob from tick 5), the mirror, and the symmetric 3 and 3. 1,024
fresh registry seeds per setting pair, the same seeds in every ordering.

| ordering | first asker (of 4,096 pairs) | S | z from 724/256 |
| --- | --- | --- | --- |
| Alice first | Alice 4,096 | 2.86329 +/- 0.04362 | +0.81 |
| Bob first | Bob 4,096 | 2.86329 +/- 0.04362 | +0.81 |
| symmetric | same tick 4,096 | 2.86329 +/- 0.04362 | +0.81 |

| setting pair (1,024 each) | E | expected | product identical, Alice first vs Bob first | plus rate, first asker / second asker |
| --- | --- | --- | --- | --- |
| a, b | -0.72266 +/- 0.0216 | -0.70703 | 1,024 of 1,024 | 0.5059 / 0.5000 |
| a, b2 | +0.73828 +/- 0.02108 | +0.70703 | 1,024 of 1,024 | 0.4961 / 0.4883 |
| a2, b | -0.67383 +/- 0.02309 | -0.70703 | 1,024 of 1,024 | 0.4707 / 0.5498 |
| a2, b2 | -0.72852 +/- 0.02141 | -0.70703 | 1,024 of 1,024 | 0.4727 / 0.5205 |

Every pair closed its quanta and consumed one number for two questions. The
product of the two outcomes is the same pair by pair in every ordering; the
individual outcomes swap roles with the ordering (the first asker's answer is
the coin, the second asker's is the agreement), so the plus rates swap. The
pre-fixed criterion also asked every rate difference between orderings to stay
within 3 combined standard errors: at (a2, b) the second asker's rate 0.5498
differs from the first asker's 0.4707 by z = 3.59, so that criterion **fails**
on one cell (`a_prefixed_criterion_pass = false`).

Follow-up (`e2_marginal_check.py`, registry alone, which reproduces the lattice
pair by pair): over the very 1,024 seeds of that cell the registry gives the
same 0.5498 (z = 3.19 from one half); over 262,144 consecutive seeds per
setting pair the second asker's plus rate is 0.50043 +/- 0.00098 (z = 0.44)
and the first asker's 0.49881 (z = -1.22); over 256 blocks of 1,024
consecutive seeds the spread of the block rate is 0.0163 against the binomial
0.0156, with 2 blocks beyond 3 sigma (largest |z| 3.25). The z = 3.59 cell is
one of those blocks; it is recorded as a fluctuation of one block of
consecutive seeds, not as a bias of the second asker.

(b) Delayed choice. The engine offers no legal in-world rule that rewrites a
detector's setting between steps (`field_rules` and `spatial_interactions` are
rejected on ray transport; `DisturbanceRecord` is frozen), so two things were
measured:

| measurement | N | result |
| --- | --- | --- |
| legal two-world comparison at identical seed: Alice's outcome changes with her own setting | 256 seeds | 0 of 256 (the first asker's answer is the coin) |
| ... Bob's outcome changes with Alice's setting | 256 | 178 of 256 |
| ... Alice's outcome changes with Bob's setting | 256 | 0 of 256 |
| flagged private-state variant, settings written after tick 2 (after emission, before arrival) | 4,096 pairs | identical to the world built with the final settings 4,096 of 4,096; S = 2.86329 +/- 0.04362 |
| ... written after tick 3 (last state before the asking step) | 4,096 | identical to the final-settings world 4,096 of 4,096; S = 2.86329 |
| ... written after tick 4 (after the ask; control) | 4,096 | identical to the initial-settings world 4,096 of 4,096; S = 1.40431 +/- 0.0439 (every pair asked at (0, 8)) |

The private-state variant replaces the frozen detector record in
`world._nodes[...]` between steps without touching `src/`; it is flagged as
such in the result file. Pass against the pre-fixed (b) condition: yes (pairwise
identity 100 % and S within 3 sigma).

## E3: free choice from inside the world

Each pair's two settings are chosen by a ticket from the world's own generator
family (`next_ticket` / `ticket_draw` of `core/spatial_state.py`, seeded from
the registry seed family): `salted` (the capture-salt pattern, salts 0 and 1),
`bond` (the registry's own two-step number at salts bond + 1 and bond + 2),
`state` (parity of the raw affine state, no square), `state_hi` and
`state_hi_far` (high bit of the raw state at salts 0 and 1, or 0 and M/3), and
the control `random.Random(seed ^ 0xABCDEF)`. Tests: CHSH within 3 sigma, and
chi-square independence between the pair's number (its coin half; its
agreement half in four quantiles) and the chosen setting pair, p > 0.01.

Lattice, 4,096 pairs per variant:

| chooser | setting pairs a,b / a,b2 / a2,b / a2,b2 | S | z | coin p | agreement p | pass |
| --- | --- | --- | --- | --- | --- | --- |
| control (Python random) | 1031 / 1052 / 1031 / 982 | 2.80981 +/- 0.0445 | -0.41 | 0.35 | 0.083 | yes |
| salted | 1410 / 596 / 588 / 1502 | 2.84187 +/- 0.04787 | +0.29 | 0.48 | 0.88 | yes |
| bond | 1001 / 1034 / 1059 / 1002 | 2.81926 +/- 0.04436 | -0.20 | 0.72 | 0.17 | yes |
| state | 0 / 2048 / 2048 / 0 | undefined | - | 0.73 | 0.58 | no (degenerate) |
| state_hi | 500 / 0 / 0 / 3596 | undefined | - | 0.84 | 0.030 | no (degenerate) |
| state_hi_far | 0 / 500 / 0 / 3596 | undefined | - | 0.84 | 0.030 | no (degenerate) |

The raw affine state is a degenerate chooser: its parity at salts 0 and 1 is
always opposite (consecutive integers) and its high bit differs only at one
seed in 2^29, so two of the four setting pairs never occur and S cannot be
formed. The `salted` chooser's two bits are correlated (the counts above), which
does not by itself break the independence tests. Every lattice run closed its
quanta and consumed one number per pair.

Registry alone, 65,536 pairs per seed with consecutive birth codes:

| chooser, seed | S | z | coin p | agreement p | pass |
| --- | --- | --- | --- | --- | --- |
| control, 11 / 12345 | 2.81609 +/- 0.0111 / 2.84326 +/- 0.01099 | -1.09 / +1.38 | 0.49 / 0.69 | 0.74 / 0.29 | yes / yes |
| salted, 11 / 12345 | 2.81658 +/- 0.0111 / 2.8122 +/- 0.01111 | -1.04 / -1.43 | 0.68 / 0.38 | **0.0020** / 0.17 | **no** / yes |
| bond, 11 / 12345 | 2.83529 +/- 0.01103 / 2.83177 +/- 0.01104 | +0.65 / +0.33 | 0.37 / 0.96 | 0.30 / 0.85 | yes / yes |
| state, state_hi (both seeds) | undefined | - | - | - | no (degenerate) |
| state_hi_far, 11 / 12345 | 2.82478 +/- 0.01168 / 2.82379 +/- 0.0119 | -0.29 / -0.36 | 0.65 / 0.65 | 0.64 / 0.95 | yes / yes |

Follow-up (`e3_salted_followup.py`): 16 seeds x 65,536 = 1,048,576 pairs per
chooser; per-seed statistics pooled (chi-square summed, degrees of freedom
summed).

| chooser | seeds with agreement p <= 0.01 | pooled agreement chi2 / df, p | pooled coin chi2 / df, p | mean S | max abs z of S |
| --- | --- | --- | --- | --- | --- |
| salted | 1 of 16 (seed 11) | 145.7 / 144, **0.44** | 50.1 / 48, 0.39 | 2.8275 | 2.03 |
| bond | 0 of 16 | 146.6 / 144, 0.42 | 37.3 / 48, 0.87 | 2.8299 | 1.56 |
| control | 0 of 16 | 174.2 / 144, 0.044 | 43.2 / 48, 0.67 | 2.8322 | 1.78 |

The p = 0.002 at seed 11 is recorded as a one-seed fluctuation: it does not
persist across seeds and the pooled test over 2^20 pairs gives p = 0.44.
`all_pass` in the result file is `false` because of that seed and because the
degenerate choosers cannot form S; the pre-fixed rule is applied as written.

## E4: birth-code uniqueness and one number per pair

(a) Two bonded pairs born at the same Node and tick (13 x 9 x 3 lattice; pair 1
along x, pair 2 along y) against a control where pair 2 is born at the
neighbouring Node; 1,024 seeds each, settings A1 = A2 = 0, B1 = B2 = 8.

| case | E(A1,B1) | E(A2,B2) | E(A1,A2) | E(B1,B2) | E(A1,B2) | E(A2,B1) | numbers / distinct values per world | pass (theory) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| collision (same Node, same tick) | -1.0 | -1.0 | -1.0 | -1.0 | +1.0 | +1.0 | 2 / 1 (one bond asked four times) | no: the pre-registered implementation prediction |
| control (neighbour Node) | -0.72266 +/- 0.0216 | -0.70703 +/- 0.0221 | -0.0293 +/- 0.0312 | -0.0293 +/- 0.0312 | +0.0098 +/- 0.0313 | +0.0566 +/- 0.0312 | 2 / 2 | yes |

`origin_bond = (index * 1048573 + tick) mod 1073741789 + 1`: the modulus is
prime and the multiplier coprime to it, so two different Nodes collide only
when their ticks differ by at least 1,048,573 for neighbouring addresses; the
only reachable collision is the same Node and tick, which is the case above.
It is recorded as an implementation limit, exactly as `expectations.json`
predicted (`a_prediction_implementation`).

(b) Replay: Bob's plus detector at 5 links, a second bonded detector with
Alice's setting one link past her plus detector; 1,024 seeds.

| measurement | result |
| --- | --- |
| worlds where Alice's ray walked on (first answer -1) and met the replay detector | 503 of 1,024 |
| replay answer equal to the first and no number drawn | 503 of 503 |
| numbers per world | 1 in 1,024 of 1,024 |
| E(Alice's first answer, Bob) | -0.67578 +/- 0.02303 (expected -0.70703, z = 1.36) |
| variant: replay detector at setting 16 | numbers 2 in 503 worlds (the registry treats it as the second end, releases the pair and reopens it with the same number), replay answer equal to the first in 261 of 503; recorded as the registry's stated limit, no pass criterion |
| registry API asked 11 times with identical arguments | 1 number, 11 identical answers |

Pass against the pre-fixed (b) condition: yes.

(c) A missing end: Bob's detectors removed, his ray escapes the open boundary;
1,024 seeds with the absent Bob's setting parameter 8 and 24, and the full
world at the same seeds.

| measurement | result |
| --- | --- |
| Alice's plus rate with Bob absent | 0.49609 +/- 0.01562 (z = -0.25 from one half) |
| Alice identical pair by pair between Bob-setting 8 and 24 | 1,024 of 1,024 |
| Alice identical to the full world at the same seed | 1,024 of 1,024 (full-world rate 0.49609) |
| Bob outcome, escaped quanta, numbers, questions, open pairs per world | none, 1, 1, 1, 1 in every world |

Pass against the pre-fixed (c) condition: yes.

## Controls

E1 `control_same_number` (empty diff 48 of 48); E2 the symmetric ordering and
the after-the-ask write (identical to the initial-settings world 4,096 of
4,096); E3 the Python-random chooser (lattice and registry, 18 runs); E4 the
neighbour-Node birth and the full world at the same seeds.

## Pass and fail against the pre-fixed conditions

| experiment | pre-fixed condition | outcome |
| --- | --- | --- |
| E1 | no difference outside the cones or before the first ask; control empty | pass |
| E2 (a) | S within 3 sigma in both orderings; every E and rate difference within 3 combined sigma | S and E pass; one rate cell at z = 3.59 fails; traced to a block fluctuation by the registry-only follow-up |
| E2 (b) | pairwise identity 100 % and S within 3 sigma | pass |
| E3 | S within 3 sigma and p > 0.01 for every dependence test, every variant | lattice: 3 pass, 3 degenerate; registry: salted seed 11 p = 0.002 fails; follow-up pooled p = 0.44 |
| E4 (a) | control matches theory; collision reported as a limit if it deviates | control pass; collision is the predicted limit |
| E4 (b), (c) | as stated in the file | pass, pass |

## Limits

- Research worlds on a 13 x 3 x 3 (E4a: 13 x 9 x 3) open lattice with one pair;
  1,024 pairs per correlation on the lattice, 65,536 per seed in the registry.
- The registry is observed by replacing the bound `draw` method of one
  registry instance with a logging wrapper; E2 (b)(ii) replaces frozen records
  in private engine state. Both are flagged in the result files and neither
  touches `src/`.
- The E1 cone check uses Manhattan distance on the lattice, which is the
  causal speed of one link per tick on this configuration.
- The follow-ups that explain the two deviations use the registry alone (which
  reproduces the lattice outcomes pair by pair in E2 and E3); no additional
  lattice blocks were run.

## What is not established

- Nothing about nature: the worlds, the registry and the choosers are the
  model's own. The measurements say what the engine does at this revision.
- That the two deviations are fluctuations is supported by the long registry
  runs, not proven; the pre-fixed criteria are reported as failed where they
  failed.
- No claim that the bond registry is local physics: E1 measures that its
  answers do not leak outside the cone, not that the registry is a lattice
  rule; hypothesis 1 remains a hypothesis.
- The birth-code collision is a limit of `origin_bond`, not a physical effect.
