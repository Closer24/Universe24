# Bell probe: CHSH on two phased rays from one source

A configuration on the [Kerengonen candidate](../../docs/SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1)
with the lottery capture, directed emitters (`heading`), a per-detector
`capture_salt`, and [claims](../../docs/SPATIAL_FIELDS.md#claim-and-gather-claim-gather-ray-field-v1)
used only to read where each quantum landed. Every number is a read-only
world/event audit at host lattice coordinates. No angle unit or constant is
identified: a detector setting is a phase step of 64, and the quantum and
local reference values are printed beside the measurement, not used by it.

```sh
python examples/bell-chsh/run_experiments.py --output artifacts/bell-chsh
```

## Mechanism

Two records at the center of a 13 x 3 x 3 line each emit one quantum: Alice's
along `-x` with hidden phase `lambda`, Bob's along `+x` with `lambda` plus a
half turn (32 steps). Three links out on each side sits a "plus" detector
Node; a reference lamp one link above it lands one quantum per tick on that
Node at the detector's setting phase. When the particle's ray arrives, the two
rays are resident together and the coherence of the pair is `cos^2` of half
their phase difference; the lottery takes the particle's ray with that
probability, Malus's law on the Kerengonen coherence. A ray not taken walks
one link further to a "minus" detector alone, coherence one, taken surely.
Every detector claims what it takes, so the surviving root of each train says
where that quantum landed: plus is `+1`, minus is `-1`. Each detector has its
own `capture_salt`, so the four detectors draw four independent ticket
sequences from one field seed.

The settings are Alice `a = 0`, `a' = 16` (a quarter turn) and Bob `b = 8`,
`b' = 24`. For every hidden phase (64) and every capture seed (16) each of the
four setting pairs is run once: 1,024 pairs per correlation. With two
independent lotteries the model predicts `E(a, b) = -cos(a - b) / 2` and
`S = sqrt 2`; the local bound is 2 and the quantum singlet gives `2 sqrt 2`.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 in `summary.json`, Python 3.14, headless.
`tests/test_bell_chsh.py` checks the aligned and opposite phases, one seed
over every hidden phase, and the salt's validation.

| Settings | E measured | E predicted (two lotteries) | E quantum |
| --- | --- | --- | --- |
| a, b | -0.422 | -0.354 | -0.707 |
| a, b' | 0.326 | 0.354 | 0.707 |
| a', b | -0.387 | -0.354 | -0.707 |
| a', b' | -0.346 | -0.354 | -0.707 |

| Quantity | Value |
| --- | --- |
| S measured | 1.481 |
| S predicted by the two lotteries | 1.414 |
| Local bound | 2 |
| Quantum value | 2.828 |
| Same setting, E(0, 0) | -0.525 (predicted -0.5) |
| Plus rates, Alice and Bob | 0.47 to 0.51 |
| Missing pairs | 0 of 4,096 |
| Quanta closed | every run |

With `--capture threshold` the detectors are deterministic hidden-variable
devices: a ray is taken when its coherence with the reference reaches one
half. The outcome is then fixed by the hidden phase and the setting alone, and
the correlation is the triangle wave of the sign model:

| Quantity | Threshold value |
| --- | --- |
| E(a, b), E(a, b'), E(a', b), E(a', b') | -0.5, 0.5, -0.5, -0.5 (predicted the same) |
| S | 2.0 (predicted 2.0) |
| Same setting, E(0, 0) | -0.9375 (the half-turn boundary rounds one phase in sixteen) |
| Plus rates | 0.5156 on both sides |
| Missing pairs, closure | 0 of 256; every run closed |

With `--capture bond` the two rays share a bond, the plus detectors hold
their settings, there are no reference lamps, and the
[bond registry](../../docs/SPATIAL_FIELDS.md#bonded-rays-bonded-ray-field-v1)
answers for both ends with the singlet's law: the split of postulate 4, the
one influence that skips Nodes and carries nothing physical. 16 registry
seeds per hidden-phase slot, 1,024 pairs per correlation:

| Quantity | Bonded value |
| --- | --- |
| E(a, b), E(a, b'), E(a', b), E(a', b') | -0.719, 0.707, -0.719, -0.719 (quantum -0.707, 0.707, -0.707, -0.707) |
| S | 2.863 (quantum 2.828, local bound 2) |
| Same setting, E(0, 0) | -1.0 |
| Plus rates, Alice and Bob | 0.47 to 0.52, whatever the other side's setting |
| Missing pairs, closure | 0 of 4,096; every run closed |

Per detector Malus's law holds: over 32 seeds the plus rate at hidden phase
0, 8, 16, 24 and 32 steps reads 1.0, 0.84, 0.53, 0.12 and 0.0 against
`cos^2` 1.0, 0.85, 0.5, 0.15 and 0.0, and Bob's the complement. The first
measurement, with the lottery drawing its ticket state directly, gave
`E(0, 0) = -0.33` and `S = 1.38` because two detectors that had met the same
reference rays drew numbers a fixed distance apart; the draw now squares the
state, and the same-setting correlation reads its predicted `-0.5`.

## Conclusion

The ray gives Bell's test a local model's answer, twice. With the lottery
each detector obeys Malus's law and S lands near `sqrt 2`; with deterministic
hidden variables the equal-setting correlation becomes near perfect and S
rises to exactly 2, the bound itself, and not a step beyond it. Hidden
variables instead of dice buy the missing half of the correlation and stop
at the theorem's line, because the outcome at each side still depends only
on what is at that side. The bond gives the third answer: with the pair's
joint outcome answered once for both ends, S reaches the quantum value, the
equal-setting correlation is perfect, and each side alone still sees an even
coin, so nothing signals. The ray carries everything physical at link speed;
the bond carries the one thing the experiments say is not carried. What the
registry is, beyond a table the world shares, the model does not say.
