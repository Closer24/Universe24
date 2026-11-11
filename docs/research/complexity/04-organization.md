# Spatial memory across repeated macrocycles

Production baseline: `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`.
This is a separate declared experiment in the isolated complexity worktree,
not an edit of the production tensor or an integration of PR #39.

## Result and boundary

A local, reversible, three-bank memory can retain spatial traces while its
carrier macrostate returns exactly, and the retained traces can change a
later local response. That narrow causal mechanism runs in the actual
fixed-six Engine. It is a deliberately designed delay archive, not learned
organization or a proof of a universe seeking complexity.

The candidate **fails the complete recurrent-burst protocol**. The three
phase slots fill and then repeated writes mostly increase integers. No
memory feedback changes the carrier reassembly; no stagnation detector acts;
the required persistent site patterns and sustained growth are absent.

## Fixed law and prepared sector

Ten gears are retained: six directed carrier lanes, three memory banks
`X,Y,Z`, and response `D`. Let `S` translate by one positive-x edge, and
let `J=sum_i p_i*n_i` be the on-site sum of opposite-lane products.
The carriers use the exact two-neighbor translation stencil, with complete
histories prepared for their respective directions. Their state repeats
after L updates on the periodic cube.

Define `R(X,Y,Z)=(Y,Z,SX)`, so `R^-1(X,Y,Z)=(S^-1 Z,X,Y)` and
`R^3=(S,S,S)`. The desired prepared-sector memory map is

```
m_next = R(m) + (J(carriers), 0, 0).
```

It is realized with the unchanged scalar divisor six by

```
u_X = 3*(b_Y + S^-1 b_Z + J(b_carriers))
u_Y = 3*(b_Z + b_X - J(a_carriers))
u_Z = 3*(S b_X + b_Y)
u_D = 3*b_X*sum(b_carriers).
```

Prepare memory `a=(S^-1 b_Z, b_X-J(a_carriers), b_Y)`. Algebraically,
`a_memory=R^-1(b_memory-(J(a_carriers),0,0))`; substitution into Rule3 gives
the first-order memory map exactly, and preserves this relation at the next
update. The actual execution independently checks that map at every step.
All monomials have degree at most two and one-face support. The only old-a
factors are carriers read by memory, so their dependency is acyclic.

The memory values merely permute between writes. They do not decay or require
host maintenance. The response is an actual retained dynamic field, not an
external journal or an observer-defined click count. Complete-state inverse
checks include carriers, all memory banks, response and every remainder.
All coefficients are multiples of three, so remainders are unchanged;
the observed events are C0. This construction does not force C2 by relabeling.

## Protocol declared before the grid

L=3,5,7; six L-step periods per run; bit stop128 checked after complete
updates. Each L uses these six fixed variants:

| Variant | Changed preparation or fixed law |
| --- | --- |
| Coherent | All six unit packets begin at the common center; memory empty |
| No write | Remove both memory-source terms, including their inverse term |
| No read | Remove the memory-to-response terms |
| Scaled | Double all carrier preparation amplitudes |
| Scrambled | Same six packets/mass, independently seeded initial positions |
| Noisy memory | Coherent packets, seeded sparse +/-1 initial memory, with its complete compatible history |

The bank count and response rule were not optimized after examining scores.
An initial NumPy oracle dtype mismatch was corrected before the complete
grid; it did not change the tensor or preparation. The proposed four-period
observation was extended to six periods **before the first run** so that the
three-phase memory capacity could be compared at periods3 and6.

A separately declared follow-up prepares two new complete states: the first
is the coherent macrocycle1 state, the second has identical carriers and
response but memory triples from macrocycle2. Both then evolve for L updates
under the same fixed law, with no edits after preparation. Every L is retained,
including the negative result. This is a matched initial-condition control,
not a reset performed within a trajectory.

## Executed results

Reproduce:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python experiments/complexity/cycle_organization.py --out runs/complexity-research/04-organization
```

The 18 main runs completed 540 updates, all rewound exactly; all six additional
counterfactual trajectories also rewound. No resource stop occurred. Peak
integer size over the main grid was6 bits. They recorded17,802 C0 events,
zero C1 and zero C2. Every tensor has zero single-edge support violations.

At exact coherent carrier returns, the following sequences include the seed
and macrocycles1 through6:

| Measure | L=3 | L=5 | L=7 |
| --- | --- | --- | --- |
| Occupied memory cells | 0,1,2,3,3,3,3 | 0,1,2,3,3,3,3 | 0,1,2,3,3,3,3 |
| Nonzero site-sign types | 0,1,1,1,1,1,1 | 0,1,2,3,3,3,3 | 0,1,2,3,3,3,3 |
| Face-edge sign types | 0,2,3,3,3,3,3 | 0,2,5,7,7,7,7 | 0,2,4,6,6,6,6 |
| Memory absolute mass | 0,3,6,9,12,15,18 | same | same |
| Three-observation fixed-site persistence | 0 throughout | 0 throughout | 0 throughout |
| Minimum carrier radius-one focus | 1 | 1/3 | 1/6 |

The memory primitive-vector fingerprints at macrocycles3 and6 are identical
for all three L. Therefore the magnitude doubling9 to18 is not an additional
pattern. L=3 cannot even pass the dispersion threshold; larger boards do
disperse and refocus. The listed sampling times are exact carrier returns,
not a replacement of the registered threshold-based episode detector.

The coherent complete state does not return within the window. In contrast,
the no-write control's *entire* state returns with periodL. This is a concrete
distinction between macrorecurrence and complete-state recurrence. It does
not imply unlimited structural capacity: after three source phases fill,
the same pattern is repeatedly written with larger values.

### Causal effects and scaling controls

No-read retains identical carriers and memory while its response remains zero.
No-write removes memory and response while the carriers still recur unchanged.
The same-law memory-only intervention yields later response differences at
updates2 and3 for L=3, and updates3–7 for L=7. **For L=5 it produces no response
difference within the next L updates.** That negative case is retained; no
longer window or favorable replacement was selected.

Thus some retained spatial information is causally effective in a later
interaction even when the carrier macrostate is identical. We have not shown
general predictive improvement, learning or task usefulness. Predicting the
specific memory trajectory by its exact map is an algebra check, not learned
prediction. The absence of an effect on L=5 in the declared window also shows
why merely counting nonzero memory is an inadequate utility measure.

The doubled preparation gives exactly4 times every memory value and8 times
every response value, with identical sign patterns and normalized fingerprints.
That excludes pure amplitude scaling as the cause of the reported pattern
differences. The sparse random initial memory produces substantially larger
raw site/edge diversity than the coherent archive; for L=7 its final counts
are14/64 versus3/6. Diversity alone would rank the unstructured control higher.
The scrambled L=5/7 sources never create a collision write and exhibit full
L-period recurrence. All controls use fixed declared seeds/laws.

## What would need to change

The carrier map has no memory input. Consequently even a perfect local archive
cannot cause an additional contraction here: no amount of longer running fixes
that missing dependency. The next mechanism must supply a reversible
memory-to-scattering interaction, not an observer-triggered burst.

The rotor reviewer supplies a bounded Boolean collision that does change
later density episodes. This archive supplies unrestricted integer values,
so it is **not** a compatible Boolean control port. A host threshold or a
silent substitution into a Boolean polynomial would change the model and
invalidate its invariant-domain proof. The smaller candidate interface is
the stagnation reviewer's proved Boolean alarm and the motif reviewer's
bounded memory, incorporated in the rotor's explicit inverse.

After any such integration, retain (i) the same carrier/different-memory
preparation pair, (ii) disconnected feedback controls, (iii) the period-two
no-new-pattern counterexample to one-step stagnation, and (iv) the original
reference-board growth/persistence criterion. The finite Boolean domain
permits useful finite sequences, but any identical complete-state return
necessarily repeats every single-valued state score. A larger integer range
alone does not remove finite bounds on the chosen sign-pattern metrics.

No Born, Bell, Einstein, physical cosmological bounce or open-ended complexity
claim follows from these results. The positive result is a narrow retained-
history causal mechanism and an explicit demonstration of its capacity limit.

## Evidence and coordination

`report.json` contains every main-grid observation, disconnected/scaling
comparison, same-law memory intervention and current source hash. Each case
directory saves its actual tensor, complete seed/final, every full state in
a compressed trace, and hashes. Counterfactual directories save both complete
seeds/finals and their paired traces. Observers never feed back into evolution.

- [Result in issue17](https://github.com/Closer24/Universe24/issues/17#issuecomment-6802194807)
- [Response to rotor/sensor interface](https://github.com/Closer24/Universe24/issues/17#issuecomment-6802201049)

These are construction identities and bounded computational results, not
external empirical evidence. The registered cosmology protocol remains the
acceptance authority and was not weakened to accommodate this candidate.
