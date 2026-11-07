# Research decisions

## D001 — 2026-11-07: freeze the baseline, preserve the core

**Question:** Is there a sufficiently explicit and internally consistent map on
which to run mechanism experiments?

**Proved:** constructive complete-state inverse, graph locality, parity
invariance, exact signed balance; arbitrary-net-input blocking and universal
amplitude boundedness are excluded in the stated scopes.

**Observed:** all 36 upstream blobs match the pinned source; original 15 tests,
two inverse audits and reflection certificate reproduce. Supplemental dense and
sparse representations agree on their finite test domains. Prepared periods 4
and 5 reproduce for the listed sizes and sign triples.

**Failed / limited:** no contradiction to the core specification was found.
Historical packet speeds, comparator, disruption and effective-family claims
lack complete reproducible artifacts in the inspected tree. They remain
unverified here. Synchronous execution does not meet the physical-time target.

**Decision:** retain every `universe24/` source file unchanged. Use positive
candidate `U24-P013+++` for M1 and identify signed alternatives separately.

**Next decisive test:** whether a remote local record exists in the retained
state for at least 32 updates, with a fixed readout and no-source control.

Evidence: [source audit](SOURCE_AUDIT.md), [algebra](ALGEBRA_AUDIT_2026-11-07.md),
[independent review](INDEPENDENT_REVIEW_2026-11-07.md).

## D002 — 2026-11-07: reject the stronger v1 assertion; test a fresh finite window

**Question:** Does the A11 guide implement the prespecified record behavior?

**Proved:** parity invariance implies that the r=5 perturbation can never satisfy
this observer's required r=0 value. The observer's parity sensitivity is exact.

**Observed:** v1 has ordered receiver activation and a 34-state local record
window. The same observer succeeds on new N22 preparations under v2: t=6..39
is recorded, reset at40; local projected counters cycle with period4.
No-source/source-only/gap controls at N18 do not click. Complete normalized
traces agree between the paired sizes, and complete-state inversions pass.

**Failed / limited:** v1 scorer's stronger zero-memory-at-all-later-times
assertion fails (later click40). V2 also later clicks at52. Unit odd-remainder
perturbation destroys the chosen memory readout while the counter oscillation
persists. These are finite prepared fronts, not compact mobile particles or a
robust one-shot physical detector. V2 was registered after v1 and before its
fresh N22 runs; it is not an independent external preregistration.

**Decision:** accept only the **bounded M1-prepared construction** and preserve
v1's failed outcome. It meets the initial 32-update retention threshold in its
exact specified preparation. Do not accept M1-robust, generic emergence,
permanent storage, exclusivity or quantum measurement. No structural model
change is indicated by this result.

**Next decisive test:** whether even-parity perturbations and independently
prepared components preserve the first-window record, and whether a second
connected detector receives a specified signal without destroying it. Freeze
readouts and perturbation domain before this test. See M2 below.

Evidence: [experiment](SIGNAL_MEMORY_EXPERIMENT.md), v1/v2 protocols, traces,
checkpoints, information witness, and independent review linked there.

## D003 — next bounded study, not yet executed

**Question:** Is the assembly a reusable component across a meaningful declared
interface, rather than a single tuned preparation?

**Deliverable:** versioned M2 protocol and a table of all successes/failures.
Initial ceiling: 600 CPU seconds, 256 preparations, 128 updates per preparation,
200,000 active channels per run. Stop on whichever cap is reached first.

Before executing, specify: even-parity remainder changes at selected source,
guide and detector addresses; counter perturbations ±1; source phase and
amplitude sets; two spatial translations; two cube sizes with no causal wrap;
and the second detector's exact location and fixed observation. Separate
training from held-out preparations, with all explicit seeds saved. Odd-parity
changes remain a deliberately failing control for this fixed observer.

Success requires at least 95% exact first-window acceptance over the declared
admissible validation ensemble, all inverses, and all negative controls. A
failure narrows the component contract; a budget stop is inconclusive.
No numeric robustness claim is currently licensed because this test has not run.
If a different readout is proposed, it receives a new experiment ID and fresh
validation, never a rewrite of M1's negative result.

## Obstructions and minimal candidate changes

- **Arbitrary complete-state blocking:** the exact Rule3 input identity forbids
  it for an unchanged old triple. Keep the current search on restricted effective
  transmission. If absolute blocking becomes essential, at least input coupling
  or the primitive must change; that would be a separate, unproved candidate
  requiring retained control/inverse information. No such candidate is adopted.
- **The signed Q residual:** the smallest already defined structural comparison
  is signs `(1,1,1)`, with its own candidate ID. This removes this residual;
  it still does not identify Q as physical energy.
- **Odd-parity observer failure:** no structural change is necessary to examine
  an even-parity preparation family. A parity-insensitive observer is a different
  measurement protocol requiring fresh validation; it does not repair M1
  retrospectively.
- **Bell:** under the local-response, setting-independent ensemble and exhaustive
  outcome assumptions, the CHSH bound cannot be overcome by a larger search.
  A proposed exception must name the exact changed premise and operational
  consequence; it cannot be credited as a Rule3 derivation of quantum statistics.

No work beyond the recorded runs is claimed to continue automatically.
