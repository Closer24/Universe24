# Complexity, recurrent bursts and the proposed universal clock

Audited main: `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`.
All active source/text files were checked against GitHub blobs by the coordinator.
This review changes no production tensor or seed. It distinguishes a shared
law, local communication, an evolving metric clock and a complexity mechanism.

**Finding:** current communication supports reversible transport and reception,
but still does not reassemble the reference board after its structural proxies
saturate. A genuinely recurrent control repeats the same structure. The new
FLRW sector expands with an increasing clock but no increasing spatial
structure. No implemented local stagnation detector connects these pieces.

## Fresh bounded runs

The case list and thresholds were selected from the existing registered
protocol before execution: one 600-update baseline, two 80-update negative
controls, the 70-update periodic calibration, and coefficient `+1` from each
of the three previously declared feedback families. This is a representative
recheck, not a new parameter search or a proof about every preparation.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python experiments/research/six_lens_complexity.py --out runs/six-lens/05-complexity-cycles/reproduced
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest universe24.tests.test_recurrent_bursts -v
```

The helper saves each actual tensor, complete initial/final state, passive
observations, hashes, source provenance and aggregate results. The existing
nine recurrent-burst tests passed. All eight dynamical controls below rewind
their full `(a,b,r)` state exactly; no reset or clipped arithmetic is used.

| Current construction | Completed updates | Carrier refocuses | Reference reassemblies | Structural outcome |
|---|---:|---:|---:|---|
| Communication, L=5 | 600 | 120 | 0 | Site count reaches 125 at update 15; final score `(125,375,0)` |
| No initial messages, L=5 | 80 | 0 | 0 | Reference remains empty |
| Reception disconnected, L=5 | 80 | 16 | 0 | Reference remains empty; full state returns every 5 updates |
| Periodic reference shell, L=7 | 70 | separate construction | 10 | Every reassembly has `(6,6,0)`; full return every 7 updates |
| Linear feedback, coefficient +1 | 98 | 0 | 0 | Stops after complete step at 129 bits |
| Cubic feedback, coefficient +1 | 8 | 0 | 1 | Stops after complete step at 231 bits; insufficient cycles |
| Spring feedback, coefficient +1 | 87 | 0 | 0 | Stops after complete step at 129 bits |

Here “score” is the predeclared triple of distinct nonzero site sign patterns,
undirected edge sign-pattern pairs, and sign patterns persistent at a site
over three observations. It is an exact, amplitude-scale-invariant proxy,
not physical entropy or a universal complexity definition. Reference
concentration uses absolute reference amplitudes, not a physical mass density.

The five cases with identical historical parameters reproduce all checked
historical outputs exactly, including tensor fingerprints, initial/final full
state hashes, reassembly events, carrier refocuses and maximum counter sizes.
The two shorter negative controls are explicitly reported as shorter runs.
Thus Frame48 and the newly merged Bell/Born work have not silently changed
the old communication dynamics. The intervention helper also confirms that
all 18 previously declared feedback wirings change messages after a one-site
reference intervention, while the one-way baseline does not. Wiring feedback
is weaker than demonstrating stagnation-triggered reassembly.

## What the new expanding clock does

A separate 32-update run of the eight-channel prepared FLRW tensor uses
`L=3`, `q0=2`, dust `(1,1,1)`, radiation `1`. Its decoded scale factor rises
from `14` to `3502`; the largest integer grows from 12 to 32 bits. The field
remains spatially homogeneous throughout. Its settled structural score is
`(1,1,1)`, unchanged after the observation history fills. The entire state
rewinds exactly.

This is a positive test of that sector's retained homogeneous expansion, and
a counterexample to identifying an increasing clock, larger integers or a
larger scale factor with new spatial structure. In the declared positive
sector, `a(eta)=A*eta^2+B*eta`, with `A,B>=0` and a nonzero source. Therefore
`da/deta=2*A*eta+B>0` for `eta>0`: future recollapse is absent from this
preparation by its own algebra. Extending it to a bounce would be a different
model and would require new metric/source tests.

The local causal-wave component has retained memory and a downstream response
field, but its monomials do not read a structural score or detect stagnation.
The response does not feed its transport lanes or a reassembly controller.
Frame48 is a separate vacuum frame candidate; it does not add the missing
matter/detector/memory feedback to these constructions. None of these separate
tensors may be combined merely by assigning their counters the same name.

## Exact limits of “one clock seeking complexity”

The following are mathematical statements about the proposed interpretation,
not empirical findings about all possible universes:

1. If the **entire retained state** returns to `S` after a cycle, every
   single-valued state score `C(S)` returns to the same value. A cycle counter
   stored only by the observer cannot supply newly retained board information.
   Repeating macroscopic concentration with accumulating memory is possible
   only if the complete microscopic state differs between cycles.
2. On a finite state space, a bijective update decomposes into cycles, so no
   state score can increase strictly on every step forever. This does not
   prove all Universe24 trajectories recur: its exact integers are unbounded.
   A reversible unbounded counter can increase, but that alone is not
   structural development.
3. The existing score components are bounded by `N`, `3N`, and `N` on an
   N-node cube. They cannot satisfy indefinite strict cycle growth even if
   the integer state is unbounded. They are useful finite gates, not an
   unlimited complexity law.
4. A bijection retains fine-grained information about an ensemble; changes
   in coarse-grained entropy or organized structure require a declared
   observation and preparation. Exact rewind alone supplies neither a
   thermodynamic arrow nor a preferred direction of structural change.

“One clock” can coherently mean a single dynamical universe in which apparatus
and clocks are interacting subsystems. It does not by itself specify a
single global tick accessible everywhere, an objective shared phase, a Born
measure, or a drive toward complexity. Those are separate hypotheses with
separate measurable consequences.

## A falsifiable next construction

This is a proposed experiment, not code that already passes:

| Needed element | Concrete operational requirement | Falsifying control |
|---|---|---|
| Local retained structural memory | Choose a finite observation alphabet and fixed neighborhood; retain past local motifs and receipt records inside `(a,b,r)` | Memory perturbation must alter later local messages after its cone permits |
| Stagnation sensor | Encode a finite-window no-novelty rule as a declared fixed reversible state machine/tensor, preserving replaced records | Same-size/amplitude controls with renewed motifs must not trigger on the same schedule |
| Reassembly coupling | Fixed local feedback must change actual reference concentration following locally propagated requests | Disconnect only this feedback; matching preparations must lose or shift reassemblies |
| Cumulative structure | At least four separated reassemblies with persistent, scale-invariant structure and distinct retained memories | Periodic shell, uniform amplitude growth, shuffled histories and noise controls must fail |

A local agent cannot instantly know that the entire board has stagnated.
A global assessment would need causal message aggregation and acknowledgments;
its latency must scale with graph distances. No host-side observer may inject
the answer, reset a counter, select a branch, or reschedule a burst. Any finite
memory capacity and its reversible reuse must be explicit.

For analysis, keep the current sign-pattern gates and add a separately
preregistered predictive-memory diagnostic: compare held-out prediction of
future local motifs using local past alone, then using received messages.
Count persistent motifs, estimate predictive information, and test spatially
or temporally shuffled controls. Fix windows, coarse-graining and sample
sizes before candidate runs. This can distinguish useful retained
correlations from raw diversity; it is not yet implemented or guaranteed
to define physical complexity. Statistical complexity has a research
tradition distinct from raw entropy/diversity [1]. Reversible information
processing and the thermodynamics of discarding records must also be kept
distinct [2].

Even a future passing recurrent-complexity model would still need the
independent Born/Bell/metric gates from the other audits. A rule favoring
more retained local structure does not determine coherent amplitude cross
terms, squared-amplitude normalization, or entangled joint probabilities.

## Evidence and primary references

- Reproducer: `experiments/research/six_lens_complexity.py`.
- Fresh aggregate: `runs/six-lens/05-complexity-cycles/reproduced/summary.json`.
- Focused test log: `runs/six-lens/05-complexity-cycles/tests.log`.
- Existing acceptance contract: `experiments/cosmology/PROTOCOL.md`.
- Dynamics inspected: `layers/communication.py`, `layers/causal_wave.py`,
  `layers/conformal_flrw.py`, `layers/frame48.py` under `universe24/`.
- [1] J. P. Crutchfield and K. Young, *Inferring Statistical Complexity*,
  Phys. Rev. Lett. 63, 105 (1989),
  https://doi.org/10.1103/PhysRevLett.63.105;
  primary full text: https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.63.105/fulltext.
- [2] C. H. Bennett, *Notes on Landauer's principle, reversible computation,
  and Maxwell's Demon* (2003), https://arxiv.org/abs/physics/0210005.

The new runs remain negative for recurrent bursts with growing structure.
Information recovery passes; the causal stagnation-to-reassembly mechanism
is absent, and no result here identifies complexity with Born weights.
