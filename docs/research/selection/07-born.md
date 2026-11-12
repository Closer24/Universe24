# Exclusive native selection, invariant measures and the remaining Born gate

The new native gate does perform a reversible local choice in a precisely
specified sector. The independent audit establishes its criterion and the
measure it transports. It also constructs two stationary, translation-invariant
ensembles with the same particle number and different outcome probabilities.
Consequently stationarity and a shared board clock do not uniquely determine a
Born measure. This result concerns the new `G` and pulse-pointer mechanisms,
not the earlier one-way intensity readers.

## A constructive exclusive-choice criterion

Use the agreed Boolean input order `(m,x,y)`. The gate first stores

\[
m'=m\mathbin{\mathrm{XOR}}[y(1-x)]
\]

and then swaps the carrier lanes if `m'=1`. It is a permutation of all eight
states and preserves `x+y`. Exactly one collision output is occupied if and
only if `x+y=1`. On that sector the full result simplifies to

\[
x'=1-m,\qquad y'=m,\qquad m'=m\mathbin{\mathrm{XOR}}y.
\]

Thus ready memory `m=0` routes either single occupied input to the preferred
lane and preserves the original input lane in memory. This is a constructive
conditional selector. It does not remove a second particle or choose one of
two simultaneously occupied branches: input `x=y=1` retains both outputs.
The preferred-lane rule is the declared local routing feature; it is not a
proof of increasing global structural complexity.

The audit reads the moving output at its actual destination after `F=S_x G`.
It compares the Engine with an independently written Boolean/coordinate oracle,
not with the compiled polynomial. All 512 states of a periodic three-site row
embedded in the `L=3` board, each with all six uniform carry values, give
3,072 complete Engine transitions. The other rows are zero and stay zero.
The prepared old slice is independently checked to be `F^-1(b)`. Every retained
state inverts exactly. Arbitrary mixed carries also remain unchanged because
every tensor coefficient is divisible by three; the `6^81` mixed carry
assignments were not exhaustively enumerated.

## Uniform counting is invariant; ready conditioning is different

The full 512-state row map is bijective. Its uniform counting measure is
therefore invariant. At one designated collision its exact distribution is:

| Declared preparation sector | States | None | Preferred | Other | Multiple |
| --- | ---: | ---: | ---: | ---: | ---: |
| Entire row sector, uniform | 512 | 1/4 | 1/4 | 1/4 | 1/4 |
| All three memories ready, uniform | 64 | 1/4 | 1/2 | 0 | 1/4 |
| Entire row, conditioned on one local carrier | 256 | 0 | 1/2 | 1/2 | 0 |
| Ready row, conditioned on one local carrier | 32 | 0 | 1 | 0 | 0 |

These conditions are imposed before counting, and all four outcomes remain in
each stated denominator. They are not postselected physical detector samples.
Only 27 of the 64 all-ready row states remain all-ready after one update.
Preparation supplies the directional preference; it is consumed without a
reset, and cannot be equated to the invariant full-sector ensemble.

More generally, on the local one-particle sector a supplied distribution with
`P(m=0)=p` yields `P(preferred)=p`. Exact checks include
`p=0,1/3,1/2,9/10,1`. The same gate accommodates all these measures. Choosing
`p` equal to a desired squared-amplitude ratio would assume the missing
preparation law; no such sampler feeds the Engine here.

## Even stationarity and spatial symmetry do not pick one measure

The exact permutation of the 512 row states has cycles. Within the sector with
one particle over the whole row, take uniform counting on a cycle and average
that measure over the three spatial translations. Both measures below are
stationary and translation-invariant, and both always contain exactly one
particle:

| Cycle length | Probability particle occupies the preferred lane |
| ---: | ---: |
| 9 | 1/3 |
| 3 | 1 |

The code enumerates their states and verifies that pushing either weighted
measure through `F` leaves it unchanged. The observed lane is a passive global
diagnostic for this comparison, never a runtime controller. This is an exact
counterexample to uniqueness from stationarity, symmetry and particle number.
It is not a no-go theorem for a further justified physical preparation law.

Arithmetic memory events are also distinct from retained outcomes. Among the
512 row states, 64 preferred outcomes have a local memory event and 64 do not;
32 no-carrier outcomes still have a memory event. The event class is C0
throughout. A memory click cannot simply be renamed the selected outcome.

## The new causal pointer stores outcomes but does not resolve two sources

The independent pulse sweep uses amplitudes `-2..2` at both sources and all
six carries: 150 ready trials. Another 18 trials hold amplitudes `(1,1)` fixed
and vary the retained left history over `-1,0,1`. Each trial advances the actual
three-channel Engine for six updates on side five. Every update is checked
against the literal scalar monomial oracle and inverted.

At the declared decision tick two, and through tick six before the next write,

\[
v_L=h+A_L^2,\qquad v_R=A_R^2,\qquad v=b_m-a_m.
\]

For ready history `h=0`, an exclusive positive record occurs exactly when one
prepared amplitude is nonzero. The 150 ready engineering controls contain
48 single, 96 multiple and six no-record trials. These varied preparations
are not treated as a physical probability ensemble. With two unit amplitudes,
history `h=-1` cancels the left record and leaves the right one; identical
current source amplitudes therefore do not identify an outcome law without
the apparatus preparation.

A single source writes one persistent velocity record but emits an arithmetic
memory event on each of ticks two through six. Counting those events would
count repeated updates of the same retained record. No-source and multiple
outcomes are retained, and no C2 filter is used.

## What the primary papers supply—and the missing correspondence

| Primary source | Assumptions relevant here | Native correspondence still needed |
| --- | --- | --- |
| [Busch, quant-ph/9909073v3](https://arxiv.org/html/quant-ph/9909073v3), conditions P1–P3 and theorem | Positive normalized probability assignments additive on the full set of Hilbert-space effects lead to density-operator probabilities. | A Boolean state permutation does not supply the quantum effect space, its noncommuting measurement contexts or that probability assignment. |
| [Zurek, quant-ph/0211037v1](https://arxiv.org/html/quant-ph/0211037v1), equations 1–3 | Composite Hilbert states, Schmidt coefficients and local unitary/counter-unitary symmetries motivate probabilities. | Retained classical provenance and equal counting on a cycle are not an identified entangled state with those transformations. |
| [Schlosshauer–Fine, quant-ph/0312058v3](https://arxiv.org/html/quant-ph/0312058v3) | Their analysis identifies probability and state-space assumptions entering envariance arguments. | Keep a separate ledger of dynamical symmetry and the rule relating symmetry to probabilities. |
| [Barnum, quant-ph/0312150v1](https://arxiv.org/html/quant-ph/0312150v1) | Distinguishes envariance of states from envariance of probabilities and analyzes auxiliary/no-signalling assumptions. | Demonstrating a reversible swap does not by itself establish the corresponding invariance of experimental probabilities. |
| [CHSH, Physical Review Letters 23, 880](https://doi.org/10.1103/PhysRevLett.23.880) | Bell-type experimental bounds compare local hidden-variable responses under the requisite common preparation and measurement assumptions. | Need a physical source, two analyzer settings, complete trials and independently encoded choices. |

These are requirements for a mathematical correspondence, not objections to
implementing the next mechanism. The rational Hilbert lifts and relational
instruments in lanes five and six are useful explicit reference structures;
their extra state-space and norm assumptions remain visible.

For completeness the new gate's local response table is checked with settings
that toggle the local memory bit. In the one-particle sector its output sign is
`1-2*(m XOR setting)`. All four setting pairs give CHSH magnitude two for each
shared memory pair. Another 6,561 exact stochastic response-mean tables satisfy
the same bound. The continuous proof is
`|a0(b0+b1)+a1(b0-b1)| <= |b0+b1|+|b0-b1| <= 2` for means in `[-1,1]`.
An independent common preparation measure preserves it after averaging.
This is a factorization control, not a late-choice/spacelike Engine Bell
experiment. Putting more clock history into the common state does not remove
the stated assumptions.

## Next falsifying construction

The positive next target is a map from physically prepared carrier amplitudes
and apparatus histories into a declared native ready sector, with a conserved
or transported preparation measure. It must predict the outcome basin measure
across held-out amplitudes and analyzer contexts; setting it to the desired
Born ratio is insufficient. The sector must also connect to the same metric,
stress/current accounting and the three available physical-model slots.
The pulse memory can provide a lasting record and later feedback, but its
two-source double record remains a required negative control.

## Reproduce

```bash
python -m validation.selection.born --out runs/selection/born
python -m unittest universe24.tests.test_selection_born -v
```

Use a fresh output directory. `born.json` records 3,072 gate transitions and
1,008 pointer transitions. All **4,080 saved complete transitions** are reread,
recomputed with the independent scalar oracle, inverted, and checked against
the canonical event stream and each contiguous trial chain. Complete tensors, compressed transitions, exact
counts, cycle witnesses and source/artifact hashes are saved alongside it.
Seven focused tests pass, including rejection of individually valid but
disconnected saved pointer steps. Exclusive conditional routing is established; a
physical Born measure, Engine Bell violation and integration of this Boolean
sector with the 45-field geometry remain unestablished.
