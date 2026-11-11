# Detector records, arithmetic C2 and the missing quantum instrument

Baseline: GitHub main `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`, including
Frame48 and the merged Bell/Born audit. The local source/text snapshot was
verified against the remote blobs. This investigation changes no production
Engine, tensor, seed API or event classifier.

## What a click currently means

`universe24/core/engine.py:extract_clicks` is a passive readout of two complete
snapshots. An official arithmetic click requires both a nonzero quotient
`ell = after.b + before.a` and a changed `(a,b,r)` triple. The kind reads the
remainder turn. The Engine never branches on that kind or on a readout label.
In the unified runtime the optional causal-wave owner is labelled `audit`;
its component events are not automatically physical photodetector events.

The fixed-six recurrence gives an exact identity for every legal transition:

```text
r_next - r = 2u - 6 ell, hence delta_r mod 6 = 2u mod 6.
```

Consequently only the even remainder turns occur. Conditional on a click:

| u modulo 3 | Remainder turn modulo 6 | Kind |
| --- | --- | --- |
| 0 | 0 | C0 |
| 1 | 2 | C1 |
| 2 | 4 | C2 |

This is an algebraic classification of the integer input, not an ordinal
third click, a complexity comparison, or a stochastic choice. The residue
and histories affect whether an event satisfies the click predicate. There
is no complexity objective or competing-outcome selector in this definition.
The experiment checks 78 input/remainder combinations, including negative
inputs, against this identity and exact inverse evolution.

## C2 without accumulating structure

Use one uncoupled gear per site on the minimum side-three cube, constant
`u=2`, and the same initial triple `(0,0,2)` at all 27 sites. The complete
state at every site follows exactly:

```text
(0,0,2) -> (0,1,0) -> (1,0,4) -> (0,0,2).
```

The first and third transitions are C2; the middle transition has quotient
zero and is not an official click. In 48 updates there are **32 C2 events
per node, three distinct complete states, exact period three**, and no
spatial differentiation. All nodes remain identical; full rewind is exact.
The counterexample establishes that recurring C2 is insufficient for
accumulating structural complexity. It does not forbid a different coupling
from producing structure.

## Fresh tests of the current causal detector

The packet experiment uses the unchanged nine-gear `with_causal_wave`
construction on L=13. A directed packet starts at `(0,6,6)` and the first
receiver is `(3,6,6)`. All initial histories are prepared before evolution;
there is no callback or time gate. The declared detector reads the upstream
lane, so its first reception is update three.

| Check | Fresh result |
| --- | --- |
| Six payloads (-2,-1,0,1,2,3), all six memory residues | 36 cases; no detector-memory change or click before update three; exact rewind |
| Positive unit packet, initial r=0 or 1 | Arrival changes r to 4 or 5, with no official click |
| Positive unit packet, initial r=2,3,4,5 | One C2 reception at update three |
| Signed unit packets, initial r=2 | +1 produces C2 with ell=+1; -1 produces C1 with ell=-1 |
| No packet | No reception or memory change through eight updates |
| Equal opposite signed arms arriving together | No memory response through eight updates; lane information remains elsewhere |
| Two marked receivers at x=3 and x=6 | The same unit packet triggers both, at updates three and six |
| Marked versus unmarked receiver control | Every packet-lane a,b,r value agrees at every checked update |

The two-sided sign control concerns real signed lanes. It is not a complex
phase sweep or a claim that these lane values already represent quantum
probability amplitudes. Similarly, the null case is a quiet preparation;
unrelated locally generated activity elsewhere need not wait for this packet.

For the periodic packet, four consecutive arrivals at one receiver give:

| Arrival update | Memory before | Memory after | Official event |
| --- | --- | --- | --- |
| 3 | (0,0,2) | (0,1,0) | C2 |
| 16 | (0,1,0) | (1,0,4) | None; ell=0 |
| 29 | (1,0,4) | (0,0,2) | C2 |
| 42 | (0,0,2) | (0,1,0) | C2 |

The local memory can return to its initial triple even while registering a
C2. Between isolated arrivals its `(a,b)` rotates with period four; its b
coordinate is not a stable latched outcome. Nevertheless the **complete**
state rewinds through all 45 updates, including response and remainders.
The event stream alone is not a complete state history: quotient-zero
transitions can still carry changed state and arrival information.

## What is missing for a physical detector interpretation

The tested receiver is explicitly a one-way observer probe. Its signal
lanes do not depend on the detector or memory, so the detector neither
absorbs nor redirects the packet. The sequential two-receiver result is
therefore expected from the wiring. It is evidence about this construction,
not an impossibility theorem about other detector tensors or all quantum
measurements. Nondemolition measurement is a distinct possible target, but
no corresponding quantum instrument or conditional state law is derived here.

An absorbing single-photon target needs a declared single-excitation
preparation, a quantitative detector coupling, branch-exclusive records,
and the correct state of the remaining apparatus after the outcome. One
must measure double counts and nondetections on every prepared trial, rather
than silently renormalizing a selected event set. Real efficiency, dark
counts and dead time are additional specified observables, not reasons to
erase inconvenient model events.

A concrete experimental target is Grangier, Roger and Aspect's triggered
beam-splitter anticorrelation together with their single-photon interference.
Their experiment distinguishes nonclassical counting statistics from
interference alone. A classical unit packet that passes unchanged through
our observer must not simply be relabelled an absorbed single photon.
See the [original 1986 paper](https://verga.cpt.univ-mrs.fr/pdfs/Grangier-1986.pdf),
EPL 1, 173-179, [doi:10.1209/0295-5075/1/4/004](https://doi.org/10.1209/0295-5075/1/4/004).

Information retention is compatible with record formation only when the
relevant correlations and apparatus degrees of freedom remain in the full
model. Exact inverse evolution by itself proves neither a Born distribution
nor a measurement instrument. A displayed click label supplies neither.

## Decisive next gates

1. Specify the observable and its outcome record independently of C0/C1/C2:
   define what the prepared excitation is, whether the detector is absorbing
   or nondemolition, and what complete state encodes a durable outcome.
2. Demonstrate one declared detector law across phase, amplitude, remainder
   and repeated-interaction controls. Check single, double and zero outcomes,
   conditional subsequent measurements, and all full-state rewinds. Do not
   change the preparation distribution after seeing each target ratio.
3. Reproduce single-excitation anticorrelation and interference with that
   same law, before calling arithmetic clicks photon detections. Reversible
   field-plus-apparatus dynamics must explicitly account for the record and
   any effective loss of observable coherence.
4. Supply an operational structural-complexity measure and a causal coupling
   to it. Reject the period-three C2 counterexample as a success under that
   measure. Bell and Born gates remain separate and cannot be inferred from
   the existence of a third class or a local cone.

## Reproduction and validation

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  python -m experiments.research.six_lens_clicks --out runs/six-lens/02-clicks
```

`report.json` retains initial conditions, observed triples, event kinds,
complete-state hashes and source hashes. `summary.json` is the captured CLI
summary. The custom audit passed all assertions, and its source compiles.
The existing core tests plus the seven standalone causal-wave tests passed:
**19 tests in 40.311 seconds** (`runs/six-lens/02-clicks/tests.log`). These
overlap the parent's full discovery and must not be added to its unique test
count. No production change was needed for these results.
