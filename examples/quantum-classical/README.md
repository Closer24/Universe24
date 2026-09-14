# Quantum-to-classical probes: where the finite quantum rules meet the classical ones

Three measurements composed from existing rules only; no engine law is added
and no physical constant, unit or species is identified. Each probe puts one of
the repository's finite quantum rules next to the classical rule it turns into
and measures the seam at host coordinates: a read-only world/event audit, with
no operational observer and no ticket from a physical device.

```sh
python examples/quantum-classical/run_experiments.py --output artifacts/quantum-classical
```

## Mechanisms

**Walk.** One excitation on a line of 25 registers of the
[deferred event network](../../docs/QUANTUM_EVENTS.md). Each step applies the
equal-weight number-preserving mixer `(|10> +- |01>) / sqrt 2` to every even
bond, then to every odd bond. Coherently, the amplitudes interfere: this is a
discrete quantum walk. After every k-th step the position record of every
register is discarded by the `dephasing` channel, which selects, exposes and
resamples nothing. The classical comparison is the Markov chain that crosses the
active bond with probability one half, computed on the host from the same
initial occupation.

**Counting.** A source on the 21-cubed open world emits one quantum per tick on
the [straight-ray field](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1),
over 4,096 golden-spiral headings at scale 24 taken in golden-stride order so
that consecutive quanta go in unrelated directions. Six detector Nodes per
radius, one on each axis at host `r` = 2, 3, 4, 6 and 8, read their field value
every tick. A quantum is whole: a detector holds 0 or 1. The classical
comparison is the inverse-square flux the [inverse-square probe](../inverse-square/README.md)
measured for a dense field.

**Capture.** The [causal charge example](../quantum/causal_charge.json): one
charge is transferred into a three-register quantum domain, meets a 3:4 mixer,
is swapped to a detector register, and a continuously active detector attempts
the complete null/absorption instrument every cycle. A click localizes the
charge; a null result leaves the remaining amplitude to meet the mixer again
four ticks later. Each of the independent worlds draws its tickets from its own
seed. The classical comparison is the geometric decay law with click
probability 16/25 per pass and survival 9/25.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 `05f80cf02e37...` (full value in `summary.json`), Python
3.14, headless. `tests/test_quantum_classical.py` checks the walk equality, the
whole clicks and the pass ticks on smaller sizes.

### Walk: ballistic when coherent, diffusive when the record is discarded

| Record discarded | Width at steps 1, 5, 9, 13 | Width exponent from step 4 | Equals the classical chain |
| --- | --- | --- | --- |
| never | 0.50, 2.26, 4.08, 5.90 | 1.005 | no |
| every 4th step | 0.50, 2.06, 3.32, 4.44 | 0.778 | no |
| every 2nd step | 0.50, 2.06, 2.87, 3.50 | 0.558 | yes, at every step |
| every step | 0.50, 2.06, 2.87, 3.50 | 0.558 | yes, at every step |

The coherent width grows in proportion to time, and the coherent distribution at
step 14 is the two-peaked quantum-walk shape with weight 25/1024 at the center
and 841/16384 at the fronts. With the record discarded every step or every
second step, the occupation of every register equals the classical chain's
exactly at every step, and the variance is `t - 3/4`: the square-root law of a
random walk, exponent 1/2 up to the constant offset. Every second step suffices
because a register meets only one bond between two discards, so no amplitude is
left to interfere. Discarding every fourth step sits between the two laws. The
total occupation is 1 at every step in every run, and the mean stays within
0.01 of the start in the discarded runs.

### Counting: whole clicks whose rate is the inverse square

| Host r | Clicks over one 4,096-tick sweep, six detectors | Rate per detector | Rate x r^2 | Relative spread of counts per 64, 256, 1024 ticks |
| --- | --- | --- | --- | --- |
| 2 | 612 | 0.02490 | 0.100 | 0.19, 0.09, 0.04 |
| 3 | 221 | 0.00899 | 0.081 | 0.31, 0.16, 0.04 |
| 4 | 113 | 0.00460 | 0.074 | 0.56, 0.18, 0.09 |
| 6 | 45 | 0.00183 | 0.066 | 1.03, 0.52, 0.16 |
| 8 | 32 | 0.00130 | 0.083 | 1.22, 0.59, 0.15 |

Every detector value is 0 or 1: a quantum arrives whole or not at all. The
click rate falls with host `r` at log-log slope -2.17, and `rate x r^2` stays
between 0.066 and 0.100, the same band the dense inverse-square probe reports.
The spread of the counts in a window shrinks as the window grows, by about a
factor 2 for every factor 4 in window length: the square-root law of counting.
The count variance is below the mean (0.35 of it at `r` = 2 in 64-tick windows)
because the golden stride is more regular than a random sequence. After the
sweep, 4,077 quanta have left the open boundary and 20 are in flight or at the
source: every emitted quantum is accounted for.

### Capture: repeated attempts follow the geometric decay law

CAPTURE_TABLE

## Conclusion

The seam between the finite quantum rules and the classical ones is measurable
and sits where the record is: discarding the position record turns a
ballistic walk into the classical random walk, exactly; a field made of whole
quanta averages to the classical inverse square with the square-root counting
law; and a detector that keeps asking turns one amplitude into the classical
decay law over independent worlds. None of this derives a Hamiltonian, a
collapse criterion or a particle species; the mixers and instruments are
explicit configured laws.
