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
`f12f349495c0bfd156390a79a7f49fc5df9c368117b25604e212fe68798e676a` (with the
opt-in null notice, field phase and funded emission extensions; the default rules are unchanged).

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

### A balanced splitter is available in the integer contract

The Hadamard block `[[1, 1], [1, -1]]` with vacuum coefficient `1 + i` satisfies
`U*U = 2I`, so the exact integer contract admits a balanced splitter. Replacing
both 3:4 mixers with it gives full visibility:

| phi | Analytic (S, D) weights x 4 | Recorded capture probability at D | Arm emission (S, M) per tick | Mean S emission, ticks 8-13 |
| --- | --- | --- | --- | --- |
| 0 | (4, 0) | none: weight zero | (12, 12) | 25 |
| pi/2 | (2, 2) | 1/2 | (12, 12) | 12.5 |
| pi | (0, 4) | 1 | (12, 12) | 0 |
| 3pi/2 | (2, 2) | 1/2 | (12, 12) | 12.5 |

At `phi = pi` the whole wave reaches D and S stops emitting entirely. In the
`phi = 0` balanced run four field units left the open boundary; escape is
accounted separately and the harness requires balanced accounting rather than
the strict no-escape flag.

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

### Null notices restore the conditional weight after one Link

With `"null_notices": true` the Node that records a null sends its own factor
`1/(1 - p)` through its Links. In the which-path variant, M's null at tick 1 has
`p = 16/25`, so the factor is 25/9:

| Tick | Default rule, S emission | With notices, S emission | With notices, M emission |
| --- | --- | --- | --- |
| 1 | 9 | 9 | 16 |
| 2, 3, 4 | 9 | 25 | 0 |
| 5 (next gate) | 3 | 9 | 16 |
| 6 onward | 3 or 4 | 25 | 0 |

At tick 5 the scaled envelopes give 9 and 16: the exact conditional Born
weights of the state after the first null, where the default rule gave 3 and 5.
After the second null every scale is `(25/9)^2 = 625/81`. In the plain
interferometer at `phi = pi/2`, the output null at D at tick 7 sends 625/337; it
reaches M at tick 8 and S at tick 9, and S emits 25 from tick 9. Notices cost
Link transit: the source recovers one tick after a one-Link null and two ticks
after a two-Link null. This is the candidate's causal residual.

### An external field on one arm shifts the fringe

With `"field_phase"` in place of the fixed phase gate on M, the gate reads the
Node's own value of a second spatial field, `vector_potential`, at its
schedule tick (tick 2) and applies `((3 + 4i) / 5)^n` with
`n = floor(value / 25)`. A held `coil` record at (2, 2, 1), next to M, sources
that field; nothing else emits it. The wave's own `electric_signal` is not read.

| Coil emission per tick | Coil position | Exponent n | Recorded (S, D) weights | Capture probability at D | Mean S emission, ticks 8-13 |
| --- | --- | --- | --- | --- | --- |
| 0 | none | 0 | none: weight zero | 0 | 25 |
| 200 | (2, 2, 1) | 0 | none: weight zero | 0 | 25 |
| 400 | (2, 2, 1) | 1 | [12745, 2880] | 576/3125 | 20.33 |
| 800 | (2, 2, 1) | 2 | [160225, 230400] | 9216/15625 | 10.33 |
| 400 | (1, 2, 1), beside S | 0 | none: weight zero | 0 | 25 |

The recorded weights equal `144 ((a - 5^n)^2 + b^2)` for the D port with
`a + bi = (3 + 4i)^n`, computed independently. The control row shows that a
field of the same strength on the far side of the source, which does not reach
M by the schedule tick, selects no phase. This is the classical field acting on
the wave: a local phase at one Node, read once, with the same matrix used by
the ordinary envelope and by the quantum owner.

### The wave pays for its own field

With `"source": false` on both emission rules, `electric_signal` stock 3000 on
the source and output types and budget 1000 per mode, every emitted unit is
paid from the wave's own stock:

| Variant | Paid by the wave | Sources recorded | Final total | Quantum inventory at the end |
| --- | --- | --- | --- | --- |
| phi = pi, no capture | 211 | 0 | 3000 | 2789 |
| phi = pi, capture at tick 7 | 199 | 2 | 3002 | 0; the localized record holds 2801 and then pays 25 per tick |

The runner's strict conservation flag holds in both runs. The two units of
sources in the capture run are the source Node's one emission committed after
the capture, before the terminal notice reached it: the same causal residual
that the null notice shows, now as an energy term.

## What this does and does not show

- It shows that, in this candidate, the classical field emitted by a coherent
  wave follows the local squared amplitude exactly, including after
  recombination, so the classical field carries the interference term.
- It shows that an actual local instrument on one arm makes the later
  statistics phase independent, with only local and causally delivered inputs.
- It shows, with the opt-in field phase, that an external classical field on
  one arm shifts the fringe by an exact configured phase per field unit, and
  that the shift is local: the same field elsewhere does nothing.
- It shows, with funded emission, that the field can be paid from the wave's
  own stock with constant totals and a measured residual.
- It does not show momentum exchange, the field acting back on the stock, a
  continuum limit, or a derivation of the classical limit.
  The mixers, the phase gate and the instrument are configured data. The
  default retarded source rule is a known departure from the conditional Born
  weights and is left visible above; the opt-in null notice removes it for one
  excitation at the cost of Link transit, and not for entangled registers.
