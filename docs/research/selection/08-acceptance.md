# Independent review: local selection, retained apparatus and physical limits

The new native Boolean construction supplies a real local history-to-routing
mechanism. The previous one-way phase readers could not do that. The physical
47/48-channel apparatus also shows causal record feedback, but it does not
embed the Boolean selector as physical matter, nor complete the record's stress
source. These are distinct scoped constructions through the same Engine.

## Independent native certificate

`validation/selection/acceptance.py` specifies the collision as the literal
cycle `001 -> 110 -> 101 -> 001`, with all other three-bit states fixed. It
does not call the candidate's sorting function, first-order evolution or
preparation helper to obtain expected outputs. It independently streams the
moving lane by scalar coordinate arithmetic and reverses the permutation.
The compiled tensor is tested against that oracle and a separate scalar
evaluation of every fixed-six monomial.

The invariant sector is **complete** `a=F^-1(b)`, Boolean `b`, and arbitrary
valid retained carries. It is not the broader condition that `b` alone happens
to be Boolean. Changing one old memory value outside this preparation produces
`b_memory=-1` in an explicit test, while the full integer state still reverses.
The first-order interpretation is correctly withheld there.

Fresh independent results:

| Check | Result |
| --- | --- |
| Explicit collision | Eight distinct outputs, one three-cycle; ready-memory outputs sorted |
| Integer Engine comparisons | 576 complete states, 139,968 retained integer comparisons |
| Prepared-sector coverage | Six directions, six carries; nonuniform spatial preparations and 24 twelve-step rewinds |
| Retained history interventions | 24 side/direction/seam cases, equal complete initial carrier `(a,b,r)`; future carrier differs in two components at each of four checked updates |
| Complete causality | Every retained bank agrees outside the corresponding computational cone |
| Finite ring | All 512 complete states of a three-site ring form 90 cycles; longest period 39 |
| Initial saved-data review | 16 runs independently replayed: 244,044 retained integer comparisons and 27,720 canonical records |
| Focused tests | Five independent acceptance tests pass |

This initial saved-data total includes the review's own native run, the complexity and
pointer reference runs, all ten 47-channel source cases, and three 48-channel
record variants. Their existing saved inputs and transitions are inspected;
the reviewer does not substitute a newly generated trajectory. Full runtime
verification, independent scalar evaluation and exact canonical-record parity
all pass. Every report includes exact bundle/run/tensor identity. The final
combined collector additionally requires the three texture-pointer runs,
bringing its required population to 19; its fresh summary reports the expanded
comparison counts separately.

Final combined evidence in `runs/retained-selection-final/summary.json` passed
the identity and source-freshness collector: **19 distinct saved runtime runs,
302,364 independently compared retained integers, and 43,188 canonical
records**. The additional three textured 48-channel pointer runs retain the
mechanical phase-response result and the same missing source/stress caveat.
The separate Born population contains 4,080 saved transitions (3,072 gate and
1,008 pointer), with full contiguous chains, independent scalar replay,
complete inverse and canonical-record parity. These are different audit
populations and are not pooled as physical experimental trials.

The gate conserves the two carrier occupancies `x+y`. It does **not** conserve
the Hamming weight of all three channels: `001 -> 110` changes that weight from
one to two. No physical energy or momentum invariant follows from the carrier
count. The ready-memory sector is not replenished or reset by the rule, and
the nontrivial finite cycles prevent indefinite strict growth of any state
score on this finite sector. This finite-sector statement does not apply to
all unbounded-integer Rule3 trajectories.

The local feature `y*(1-x)` is computed from the actual carrier values; no
external score is supplied to runtime. Nevertheless, ready-memory sorting is
an explicitly constructed preference for a port, not a proof of preference
for increasing structural complexity. The complexity lane's 30 failed and
six blocked growth cases remain part of the result.

## Physical 47/48-channel review

The source builder is separately pinned to PR50 commit
`62202fdccdd9a40d5dbbec104de6f97d9587a999`. The four homogeneous sign/control
cases and the two zero/massless controls have their initial flat homogeneous
Hamiltonian constraint checked independently from the **current** retained
numerators divided by the current positive denominator. Old `D=0` is retained
boundary memory, not an earlier physical ratio. The four texture cases do not
inherit the homogeneous constraint calculation.

For the declared joint homogeneous potential

`V = m²*(phi²+chi²)/2 + omega²*q²/2 + g*q*(phi²+chi²)`,

the independent symbolic calculation gives

`d(rho_total)/dt = tr(K)*(Pi_phi² + Pi_chi² + p²)`

and `d(charge)/dt = tr(K)*charge`. Reciprocal exchange and neutral torque cancel
exactly in those continuum equations. This is neither an exact conserved
integer energy nor a general spatial apparatus conservation theorem.

Two independent failure controls are retained:

* Eliminating `q` produces `m²*I/2 - g²*I²/(2*omega²)`, unbounded below for
  nonzero coupling. At `phi=8, chi=0, q=-16, m²=omega²=1, g=1/4`, the potential
  is `-96`.
* With spatially varying `p`, `q=0`, no carrier and assigned apparatus momentum
  zero, `p=1, partial_x(p)=1` gives a pressure-gradient defect of one. The missing
  spatial momentum dynamics cannot be inferred from homogeneous exchange.

The one extra pointer has exact raw recurrence `v_next=v+writer`, where
`v=b_memory-a_memory`. Source-preserving recording leaves the first 47 states
unchanged. The active variant feeds its raw retained record back into the
apparatus numerator and changes later source dynamics. Its stress and its
continuum calibration are explicitly unsupplied. Its five-step feedback trace
is an exploratory extension of the original four-update protocol, not a
predeclared long-duration validation.

## Quantum and measurement review

The QCA comparison distinguishes a permutation on basis states from supplying
a coherent Hilbert-space input. Its exact rational state/norm and reduced-state
calculations remain references; they do not arise from one Boolean Engine
trajectory. Its integral-unitary restriction applies to ordinary orthonormal
linear amplitude coordinates, not every integer encoding.

The relational-clock reference counts its clock, source, first pointer and
fresh probe explicitly. Its global finite permutation is reversible; its
pointer is later uncomputed. It neither selects one coherent branch nor
derives the squared-norm measure by conditioning on a clock. Native trial
readout retains no-record and double-record cases and declares its ensemble.

The independent Born lane's complete-sector and stationary-cycle calculations
were reviewed against the same explicit collision. A ready one-particle input
routes preferentially, but changing the retained-memory preparation changes
the outcome measure. Even stationary translation-invariant measures at the
same particle count need not agree. A shared deterministic clock therefore
does not select a unique Born measure. Review requested contiguous saved
pointer traces and exact family accounting in addition to per-step scalar
replay. Both were implemented and all 4,080 saved native transitions were
verified again; those checks must remain enabled in final collection.

## Primary-source scope check

Fredkin and Toffoli, *Conservative Logic* (1982), sections 2 and 4,
[primary paper](https://gwern.net/doc/cs/hardware/1982-fredkin.pdf), distinguish
invertible processing, explicit signal-routing composition, additive
conservation, and auxiliary constant/garbage resources. Their universal-logic
construction is not a theorem that every reversible gate conserves physical
energy. This review accordingly counts all retained memory and tests the
actual additive invariant, while withholding a physical energy interpretation.
The finite permutation recurrence result above is separately proved by
exhaustion for the closed ring and by the elementary finite-state argument.

## Reproduction and final handoff

```bash
python -m unittest universe24.tests.test_selection_acceptance -v
python -m validation.selection.acceptance --out runs/selection/acceptance-new \
  --run runs/selection/complexity-frozen/representative-run \
  --run runs/selection/pointer/native-run \
  --run runs/selection/coupled-pinned-final/connected-homogeneous-+1 \
  --run runs/selection/pointer48/raw_record_feedback
```

Repeat `--run` for every saved run to reproduce the complete table. The output
directory must be new. Final combined collection must check source hashes,
tensor fingerprints, base/current bundle identities and observation horizons.
Passing software gates is compatible with the explicit physical failures and
unresolved growth/measure requirements above.
