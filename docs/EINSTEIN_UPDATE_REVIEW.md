# Einstein update review: 11 November 2026

At the 15:33 Asia/Jerusalem review, `main` remained at
`8d3f15074d3f9a9344ec587dbab0222243505187`. [PR #27](https://github.com/Closer24/Universe24/pull/27)
advanced by one commit from `ba8b6c12066b0dbdf3f2001c9fa75571d7cff49b` to
[`335eb3c1b625075dbcca01f9cd61faffdd614600`](https://github.com/Closer24/Universe24/commit/335eb3c1b625075dbcca01f9cd61faffdd614600).
PR #29 and the prior PR #30 research result were unchanged when reviewed.

The update adds a finite-horizon arithmetic compiler for nonlinear ADM,
a real scalar field and optional pressureless dust, plus its equation and
initial-data modules and 16 focused tests. It is an optional equation-driven
construction, not a modification of the default 54-channel communication
model. This review checks compatibility and the requested local timing;
it does not independently certify every physical equation or long-time GR.

## Compatibility result

Eight exact upstream dependency files were fetched into a separate checkout
of the current research branch. The original construction fails at
`Tensor(..., Q=Q)`: the current fixed-six tensor rejects the removed argument.
The runner also passes a removed second argument to `Engine`.

The [review-only compatibility patch](../experiments/cosmology/adm_fixed_six_review.patch)
removes `Q` from the compiler and compiled program, fixes the divisor and
remainders at six, and calls `Engine(program.tensor)`. It does not modify the
common engine, change the equations or restore a scale parameter. It preserves
the upstream Q=1 law. The unchanged 16 focused upstream tests pass against the
patched experiment and the current engine, including exact arithmetic,
reversal, trace replay and the tested matter/geometry response directions.

The patch is supplied for the isolated comparison. The ADM source is **not**
installed into this branch's default construction; its scheduling mechanism
still conflicts with the requested message-driven design.

## The clock issue is still present

The compiler creates `clock.c0` through `clock.cN` at **every** spatial node,
with identical prepared `a` and `b` pulse arrays. Clock-target monomials read
only clock gears at the same node. They do not read a neighboring node or the
arithmetic/physical state. Spatial relays carry arithmetic data, not a
stagnation-dependent scheduling signal.

The [reproducible control](../experiments/cosmology/review_adm_scheduler.py)
compiles `(x*x + 3)**2` with `x=2` on 27 nodes:

| Check | Observed result |
|---|---|
| Declared computation | Six engine updates, output 49 |
| Clock bank | Nine gears per node, identical initial timing at every node |
| Perturb the arithmetic input | Clock history remains unchanged |
| Remove clock `a,b` at one node | That node outputs 0; another still outputs 49 |
| Read beyond the declared horizon | Output changes from 49 to 373 at update 14 |
| Invert the clock-removal and beyond-horizon runs | Complete seeds recovered exactly |
| Independent scalar oracle on the small circuit | 78 transitions, zero mismatches |

The past-horizon value is a counterexample to treating a wrapped compiler
clock as a new physical step. It is not a claimed fault inside the compiler's
declared horizon, nor a burst or increased structural complexity. The upstream
documentation itself limits the construction to a precompiled finite horizon.

## Actual two-step scalar and dark-dust run

The adapted current-core construction completed the upstream nonuniform L=3
case with `steps=2`, `dt=1/128`: 9,727 gears per node, 21,372 monomials and 164
engine updates. Every arithmetic register matched its independent retained
DAG evaluation, and full rewind was exact. The largest integer reached
97,980 bits. This run took about 259 seconds excluding compilation; it kept
states in memory and did not export the optional full delta journal. The
focused tests separately exercised that journal's exact replay.

The sampled maximum Hamiltonian residual grew from `7.36557e-7` initially to
`5.77058e-6`; final maximum momentum residual was `3.17397e-6`. These are
measured discretization/quantization errors, not zero-constraint claims.

A separately labelled **post-hoc** [physical-readout audit](../experiments/cosmology/audit_adm_readouts.py)
uses the saved density extrema, rounded outward to exact rational bounds.
For each snapshot, the dust fraction in any face ball is at most
`7 * maximum_density / (27 * minimum_density)`. The three upper bounds are
`0.370371`, `0.370429`, and `0.370487`, all below the dispersal threshold 1/2.
Thus none of the three sampled dust configurations can be compact by the
3/4 concentration test. Events between these samples remain unresolved.

All nodes have one common joint sign pattern of the 19 physical fields at
each sampled time. The site/edge pattern counts are `(1,1)` throughout;
three-snapshot persistence is zero because Pi changes from zero to negative.
These coarse diagnostics do not exhaust geometric complexity. They supply
no evidence of structural growth across bursts, and three completed physical
snapshots cannot establish four recurrent reassemblies. No arithmetic
workspace or compiler clock is counted as a physical structure. Three
additional tests check exact density enclosures and reject uncertain signs,
underflow and incomplete physical histories.

## Consequence for recurrent bursts

The [burst protocol](../experiments/cosmology/PROTOCOL.md) requires a local
feedback cause, recurring reference-board reassembly, structural growth and
exact information recovery. The ADM example has a different tensor, fields
and preparation, with no `ref.*`/`comm.*` coupling to that board. Counting its
arithmetic workspace or cloned clock pulses as reference bursts would change
the meaning of the test. No combined model has been demonstrated here.

A proper integration must provide a retained local readiness/stagnation
mechanism whose messages affect the next computation and reassembly, together
with an observation map from the evolving fields to the tested structures.
Extending the precompiled horizon, copying the existing clock bank into every
node, or treating more workspace registers as complexity does not establish
that mechanism. The preceding 25-case negative result remains applicable to
the unchanged communication model.

## Reproduce in a separate checkout

Start with this research commit checked out and preserve any unrelated work:

```bash
git fetch origin refs/pull/27/head
git worktree add --detach ../Universe24-adm-review HEAD
git -C ../Universe24-adm-review restore --source=335eb3c1b625075dbcca01f9cd61faffdd614600 -- \
  experiments/geometry/integer_circuit.py \
  experiments/geometry/adm_integer.py \
  experiments/geometry/adm_equations.py \
  experiments/geometry/adm_initial_data.py \
  experiments/geometry/full_gr_audit.py \
  experiments/geometry/simplex_metric.py \
  docs/INTEGER_ADM.md \
  universe24/tests/test_adm_integer.py
# This should expose the removed-Q incompatibility before applying the patch.
(cd ../Universe24-adm-review && python -m unittest universe24.tests.test_adm_integer -v)
git -C ../Universe24-adm-review apply --unidiff-zero experiments/cosmology/adm_fixed_six_review.patch
(cd ../Universe24-adm-review && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest universe24.tests.test_adm_integer -v)
python experiments/cosmology/review_adm_scheduler.py --source-root ../Universe24-adm-review
(cd ../Universe24-adm-review && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python experiments/geometry/adm_integer.py --case dark --steps 2 --dt 1/128 --out runs/adm-review-dark)
python experiments/cosmology/audit_adm_readouts.py ../Universe24-adm-review/runs/adm-review-dark/report.json
python -m unittest universe24.tests.test_adm_readout_bounds -v
```

The [evidence record](evidence/einstein_update_20261111.json) includes the exact
upstream and adapted source hashes, the compatibility failure, test outcomes
and clock-control observations. Nothing was merged to `main` or to the live
Einstein branch during this review.
