# Bell test in CHSH form with two separated wings

This experiment runs the Clauser-Horne-Shimony-Holt form of Bell's test on the
lattice, through the canonical runner under `local-quantum-events-v2`, without
changing the simulator or its laws. A Bell pair is prepared at the center,
carried by configured gates to two wings nine Links apart, and read at both
wings at the same tick by detector bodies that arrive there. The question is
whether the recorded local outcomes, combined over four setting pairs, exceed
the bound 2 that any local hidden-variable model must obey. The exact answer
below is `14/5 = 2.8`. The analytic targets are computed independently of the
update code from the configured matrices.

## Layout

[bell_chsh.py](bell_chsh.py) derives every input from the checked-in
[bell_chsh.json](bell_chsh.json): a 26 x 3 x 3 open world, one Link per tick,
and ten binary registers at x = 8 ... 17 on the line y = z = 1. The schedule is:

1. Tick 1: a Hadamard `[[1, 1], [1, -1]]` on the register at x = 12.
2. Tick 2: a controlled-NOT on (12, 13). The pair is now `(|00> + |11>) / sqrt(2)`.
3. Tick 3: nothing in the Bell runs; in the control runs a dephasing channel
   `[P0, P1]` on x = 12 discards the basis record of one member.
4. Ticks 4 to 7: SWAP gates on (11, 12) and (13, 14), then (10, 11) and
   (14, 15), (9, 10) and (15, 16), (8, 9) and (16, 17). Each SWAP joins
   nearest neighbors and respects the one-Link transit rule.
5. Tick 8: `Detector A`, seeded at x = 0 with momentum +1, reaches x = 8, and
   `Detector B`, seeded at x = 25 with momentum -1, reaches x = 17. Each wing's
   binding fires once on that arrival, with its own instrument, and writes the
   outcome code (1 for eigenvalue +1, 2 for eigenvalue -1) into the detector's
   `outcome` field.

Settings are integer observables with a positive scale: Alice measures
`a0 = Z` or `a1 = X`; Bob measures `b0 = (3Z + 4X)/5` or `b1 = (3Z - 4X)/5`.
The instrument for observable `O` with scale `s` is the Kraus pair
`(sI + O, sI - O)`, which satisfies `sum K*K = 4 s^2 I` exactly. The 3-4-5
settings are the closest integer stand-ins for the optimal `(Z +/- X)/sqrt(2)`.

The exact table needs two runs per setting pair: tickets `[0, 0]` select
Alice's first outcome and read Bob's conditional weights; tickets equal to
Alice's first weight select her second outcome. The joint distribution is
Alice's weights times Bob's conditional weights. The sampled table runs one
seeded world per trial and counts coincidences, as a counting experiment does.

## Reproduce

```sh
PYTHONPATH=src python examples/quantum/bell_chsh.py --output artifacts/bell-chsh --trials 100
```

The harness writes each generated initialization file next to its run
directory and a combined `summary.json`. It is headless and records no frames.
`tests/test_bell_chsh.py` runs the same harness with five trials per setting
in the fast gate.

## Observed results, 2026-09-14

Python 3.14.0rc2, runtime source fingerprint
`fcd527461961e59fd1295547db9318716245303b7384aa15612a4d7ca23f387a`. No source
module changed; the experiment is configuration on the existing program.

### Exact joint distributions from recorded weights

| Setting | Alice weights | Bob weights given Alice 0, 1 | Joint (00, 01, 10, 11) | Correlation |
| --- | --- | --- | --- | --- |
| a0 b0 | [4, 4] | [80, 20], [20, 80] | 2/5, 1/10, 1/10, 2/5 | 3/5 |
| a0 b1 | [4, 4] | [80, 20], [20, 80] | 2/5, 1/10, 1/10, 2/5 | 3/5 |
| a1 b0 | [4, 4] | [360, 40], [40, 360] | 9/20, 1/20, 1/20, 9/20 | 4/5 |
| a1 b1 | [4, 4] | [40, 360], [360, 40] | 1/20, 9/20, 9/20, 1/20 | -4/5 |

`S = E(a0 b0) + E(a0 b1) + E(a1 b0) - E(a1 b1) = 3/5 + 3/5 + 4/5 + 4/5 = 14/5`.
Every recorded weight equals the exact rational prediction. Both decisions in
every run are at tick 8, at registers nine Links apart; a Link signal from one
wing would reach the other at tick 17, after the nine-tick run ends. Each run
draws exactly two tickets, one per wing, and the classical `outcome` code in
each detector record equals the recorded quantum outcome plus one.

### No signalling

Alice's weights are `[4, 4]` in all eight Bell runs, whatever Bob measures.
Bob's marginal, summed over Alice's outcomes, is `1/2, 1/2` whatever Alice
measures. Bob's conditional weights do depend on Alice's outcome, which is the
correlation, not a signal: nothing at Bob's wing selects which of Alice's
outcomes occurred.

### Seeded coincidence counts, 100 trials per setting

| Setting | N(00) | N(01) | N(10) | N(11) | Estimated correlation |
| --- | --- | --- | --- | --- | --- |
| a0 b0 | 46 | 8 | 8 | 38 | 17/25 |
| a0 b1 | 46 | 8 | 8 | 38 | 17/25 |
| a1 b0 | 41 | 4 | 7 | 48 | 39/50 |
| a1 b1 | 5 | 51 | 40 | 4 | -41/50 |

Estimated `S = 74/25 = 2.96` from 400 runs, against the exact 2.8. The two
`a0` rows have the same joint distribution (Bob's `b0` and `b1` share their
diagonal), and with these seeds their counts coincide; their per-trial
outcome sequences, kept in `summary.json`, differ. The statistical spread of
400 trials is about 0.2 in `S`, so the estimate is consistent with 14/5 and
well above 2.

### Control: a classically correlated source stays below 2

With the dephasing channel at tick 3, the source is the mixture
`(|00><00| + |11><11|) / 2`, a shared classical bit.

| Setting | Bob weights given Alice 0, 1 | Correlation |
| --- | --- | --- |
| a0 b0 | [80, 20], [20, 80] | 3/5 |
| a0 b1 | [80, 20], [20, 80] | 3/5 |
| a1 b0 | [200, 200], [200, 200] | 0 |
| a1 b1 | [200, 200], [200, 200] | 0 |

`S = 6/5`, inside the local bound. The Z rows are unchanged because the shared
bit is a Z record; the X rows lose all correlation. This is the same layout,
detectors and settings, with one channel added.

## What this does and does not show

- It shows that the native register program, run through the ordinary engine
  with detector bodies as the only triggers, reproduces the CHSH value 14/5
  that the quantum owner gives when called directly, and that the value comes
  from decisions at two wings that no Link signal can connect within the run.
- It shows that the recorded statistics are no-signalling and that discarding
  the coherence of one member brings the same setup under the local bound.
- It does not show a loophole-free Bell test on nature. The tickets come from
  a simulated RNG or from the configured stream; the settings are fixed per
  run rather than chosen freely at the wings; every detector fires.
- The Tsirelson value `2 sqrt(2) = 2.828...` is not representable in the
  integer contract. `14/5` is the value of the best 3-4-5 settings, not the
  quantum maximum.
- The joint state is held by one owner and queried at each local contact;
  locality here is the contract on operations and triggers, not a claim that
  the joint state is stored locally.
