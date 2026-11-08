# Collective activity, clock balance and fresh independent replay

**Status: exact algebra and bounded computation; no gravitational slowing law
has been derived from the activity tensor.** The current repository already
contains a restricted two-preparation `4/5` clock-rate coincidence. This package
adds the activity/balance bridge and an independent full-state replay of that
result, while preserving the unchanged engine.

The [proof](PROOF.md) derives

\[
p=3(b-a)+\lfloor r/2\rfloor-1,\quad
V=\sum_x\operatorname{tr}S(x)=\tfrac12b^T(6I-A)b,\quad
p'=p-\nabla_bV.
\]

It also gives the complete inverse coordinate map, the exact remaining
`b`/parity update, and the local bound
`sum_g (Delta p_(x,g))^2 <= 24 tr S(x)`. It supplies explicit counterexamples
to interpreting `p` as an automatic clock phase, `V` as a conserved energy,
or the values of `S` alone as a complete predictor of the next state.

## Reproduce

From the repository root, with Python 3.11+ and the standard library:

```sh
python -m research.collective_clock_geometry.audit --output runs/collective-clock-check
python -m unittest discover -s tests -p test_collective_clock_geometry.py -v
```

Choose a fresh output directory. Existing evidence is never overwritten.
The audit writes its [protocol](evidence/protocol.json) before computation and
produces [results](evidence/results.json) with source hashes, exact input
recipes and complete-state hashes. The independent gather and inverse use
`research.component_families.oracle`, whose routing is reconstructed from exact
reference matrices without production Engine, Coupling, State, Rule3 or event
classifier imports. Native evolution is used only as the implementation being
compared. Every remainder and the exact uniform background are included.

The audit checks:

* All six remainders with small positive/negative and very large integers in
  the scalar coordinate identities.
* One seeded dense board for every combination of side 3/4 and all eight sign
  triples: complete native/oracle forward and inverse agreement, reciprocal
  routing, the activity quadratic, its finite-difference gradient, and the
  local balance bound.
* Three explicit counterexamples, with full-state preparations.
* Fresh independent replay of all 24 current-main clock preparations: two
  all-48 probe seeds, six neighboring source directions and source on/off;
  side 7, 40 updates, all full-state hashes, one-step inverses and complete
  rewinds. The actual measured periods are checked separately from arithmetic
  validity.

## Relationship to existing gravity work

The [existing clock-prerequisite study](../einstein_clock_bricks_v1/README.md)
shows the same neighbor source changing the local recurrence periods of
`(-1,-1,0)` and `(0,-1,4)` from 4 to 5 while a distant reference retains period
4. These are two distinct preparations, not an equivalence-principle test over
all possible clocks. Its local continuity identity, period-mean constraint and
first-step balanced-substrate response retain their original evidence and
limits. This package does not relabel those results as a gravity derivation.

The observed rate uses exact recurrence periods indexed by board updates.
No accumulated local elapsed-time counter, moving-clock calibration, physical
light speed, metric, curvature, source energy or Einstein equation has been
derived by this audit. No click count is used as an external time gate.

The [gravity target sheet](../clock_selection/physics_targets/gravity.md) gives
the broader operational requirements. In particular, a common response across
different clock constructions and independent signal/trajectory predictions
must be established before a geometric interpretation is warranted.

## Provenance

The starting repository was commit
`37fe77be8f489ba722ac687ff544b3956352e62f`. Earlier local-only activity/Einstein
review files were unavailable after workspace maintenance. This package is a
**new reconstruction and new replay**, not a recovered copy of those files.
It does not republish their old numerical counts, signatures or unavailable
negative-run certificates. The proof is self-contained and the new inputs,
code and output are retained together. No engine, coupling or observer file is
modified. No additional state-changing law is introduced.
