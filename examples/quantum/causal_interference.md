# Two-arm interference with a classical field source

This experiment asks two questions of `causal-contact-fields-v1` without
changing the simulator or its laws. First, does a wave that is split, phase
shifted and recombined on the lattice reach a held detector with the
phase-dependent probability that the configured matrices predict, while the
ordinary classical field emitted along the way follows the local squared
amplitude. Second, does a detector placed on one arm remove that phase
dependence. Both answers below are exact integer readouts of the canonical
runner. The analytic targets are computed independently of the update code.

## Layout

[causal_interference.py](causal_interference.py) derives every input from the
checked-in [causal_charge.json](causal_charge.json): a 7 x 3 x 3 open world,
one Link per tick, and one domain with registers 0, 1 and 2 at S = (1,1,1),
M = (2,1,1) and D = (3,1,1). An `incoming_charge` record at S meets a held
`contact_probe` at tick 0 and becomes a unit source envelope. The repeating gate
schedule is:

1. A 3:4 mixer on (S, M): amplitudes (3/5, 4/5).
2. A one-mode phase gate on M with coefficient `exp(i phi)`, phi in {0, pi/2, pi, 3pi/2}.
3. The inverse mixer on (S, M).
4. A SWAP from M to D, where a held `contact_probe` attempts capture on every cycle.
5. Twelve empty phases, so no gate repeats inside the 14-tick run.

The inverse mixer sends `(9 + 16 e^{i phi})/25` to S and `(-12 + 12 e^{i phi})/25`
to M. The capture weight at D is therefore `288 (1 - cos phi) / 625`, and the
source weight that keeps emitting at S is `(337 + 288 cos phi) / 625`. Emission
allowances are raised to 1000 units per mode so that the finite budget does not
truncate the measurement; the integer emission amount stays 25 per full source.

## Reproduce

```sh
PYTHONPATH=src python examples/quantum/causal_interference.py --output artifacts/causal-interference
```

The harness writes each generated initialization file next to its run directory
and a combined `summary.json`. It is headless and records no frames.
`tests/test_causal_interference.py` runs the same harness in the fast gate.

## Observed results, 2026-09-14

Python 3.14.0rc2, runtime source fingerprint
`4916707db38c4f364552a24a727678698912f509a27969c4217ca02005ca6cf6`.

### The output detector sees the interference term

| phi | Analytic (S, D) weights x 625 | Recorded decision weights at D | Decision tick | Analytic S emission per tick | Mean measured S emission, ticks 8-13 |
| --- | --- | --- | --- | --- | --- |
| 0 | (625, 0) | none: capture weight is zero, no ticket drawn | none | 25 | 25 |
| pi/2 | (337, 288) | [337, 288] | 7 | 13.48 | 13.5 |
| pi | (49, 576) | [49, 576] | 7 | 1.96 | 2 |
| 3pi/2 | (337, 288) | [337, 288] | 7 | 13.48 | 13.5 |

The recorded weights match the exact rational prediction in all four cases.
At phi = 0 the quantum owner never issues an uncertain decision at D, because
the D amplitude is exactly zero; no random ticket is consumed. The classical
emission at S after recombination is the integer floor of `25 * |a_S|^2` with
carried fractional remainder: 13, 14, 13, 14, ... for 337/25, and 1, 2, 2, 2, ...
for 49/25. During the arms, S emits 9 and M emits 16 per tick in every case.

With a ticket that selects capture at phi = pi, one `localized_charge` record
appears at D at tick 7. M and D envelopes stop emitting immediately. S emits once
more at tick 8 and then stops: the terminal notice crossed two Links with local
delay. The localized output emits at full strength from its own allowance.

### A detector on the arm removes the phase dependence

The which-path variant adds a held `contact_probe` at M and lists register 1 as
a capture register. It is the same instrument as at D.

| phi | First uncertain decision | Weights | Later decisions at M | Uncertain decisions at D |
| --- | --- | --- | --- | --- |
| 0, pi/2, pi, 3pi/2 | tick 1, register M | [9, 16] | one more [9, 16] at tick 5 after a null | none |

The arm decision is identical for every phase. With the ticket selecting
capture, one localized record appears at M at tick 1 and all envelopes retire.
With the ticket selecting null, the M envelope is zeroed, the conditional
quantum state moves entirely to S, and no decision at D ever has a nonzero
capture weight in the 14-tick run.

### The retarded source approximation, measured

After the null at M, the exact conditional state has weight 1 at S. The
ordinary source envelope at S is not renormalized: it keeps its retarded value
3/5 and emits 9 of a possible 25 units per tick (tick 2 onward). This is the
documented [retarded, unnormalized source rule](../../docs/CAUSAL_QUANTUM_SOURCES.md#actual-interaction-and-causal-termination)
seen as a number: the classical field after a null result carries 9/25 of the
strength a globally conditioned source would carry. It is a limit of the
candidate, not a measurement error.

## What this does and does not show

- It shows that, in this candidate, the classical field emitted by a coherent
  wave follows the local squared amplitude exactly, including after
  recombination, so the classical field carries the interference term.
- It shows that an actual local instrument on one arm makes the later
  statistics phase independent, with only local and causally delivered inputs.
- It does not show a balanced beam splitter, field back-action on amplitudes,
  energy closure between field and matter, a continuum limit, or a derivation
  of the classical limit. The 3:4 mixer, the phase gate and the instrument are
  configured data. The retarded source rule is a known departure from the
  conditional Born weights and is left visible above.
