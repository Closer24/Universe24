# Source baseline and document–implementation comparison

Read on 2026-11-07:

- [Repository at ed1556e202eb0f3cc60342c75d44012c2eeb71c3](https://github.com/Closer24/Universe24/tree/ed1556e202eb0f3cc60342c75d44012c2eeb71c3).
  All 36 file blobs were materialized and verified against their Git blob SHA-1;
  the reconstructed tree is `fe5b84261d6573b24f80b1f795df14e5182dfa5d`.
- [Universe24 research document](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI),
  modified `2026-11-07T01:37:38.239Z`. This is a live-document snapshot, not an
  immutable Drive revision. The normalized text digest and normalization method
  are in [source_manifest.json](../research/baseline_audit/source_manifest.json).
  No prior-chat statement is used as evidence. The companion document referenced
  in A13 has not been independently audited in this work.

The baseline package version `0.1.0` is not a sufficient experimental revision.
Always use the source commit plus hashes of new research scripts. The local
snapshot Git commit is not represented as the upstream commit; its tree matches.

## Comparison

| Document location | Implementation / actual scope | Finding |
|---|---|---|
| A1–A2, A12: one board, 48 triples, six old spatial inputs, exact Rule3 | `core/state.py`, `core/rule3.py`, `core/engine.py` | Formula matches; no extra evolution stage found. |
| A6: generated signed matrices | `core/coupling.py`, `core/group_2o.py` | Sparse immutable routing/sign arrays represent the same tensor; dense versus sparse comparison is audited. |
| A12: NumPy object-array illustration | Standard-library Python integers in core | Representation difference, not a second law; no NumPy runtime dependency. |
| A0/A6: positive reference and seven other sign triples | `Coupling()` and omitted config signs default to `(1,1,1)` | Reflection documentation calls `(1,-1,1)` “current”; this is an experiment choice, not the engine default. Candidate IDs must separate them. |
| A2 inverse, A9 parity, A10 account | Explicit inverse, immutable states, passive balance functions | Algebra matches. `Q` is shifted by chosen background remainder in code; the constant offset does not change its balance. |
| P6 autonomous physical ordering | Synchronous old-snapshot engine | An acknowledged missing physical realization, not established autonomous physical time. |
| A6a reflections | `research/reflection_audit.py`, tests and report | Matched by rerun; class is uniform signed channel permutations, not all possible mirror maps or physical parity. |
| A11 period-four and period-five pairs | clock seed exists; original tests do not assert both periods | Now independently checked with complete state and several sizes; see audit. No generic robustness inference. |
| A11 temporary guide memory, binary cost comparator, signal disruption | No corresponding complete experiment suite in baseline tree | Reported document claims need explicit reconstruction and tests. This change investigates the guide separately; comparator/disruption remain unverified here. |
| Section 6 wave-packet speeds and 8192-site comparisons | No scripts, seeds or logs for these numbers in baseline tree | Reported finite results, not reproduced evidence for this code revision. Different microscopic ratios are separate comparison models. |
| A11 effective 1/2 and 2/3 homogeneous encodings | Encoding and family-proof artifacts absent from this repo | Pending verification; no general effective field law is established. |
| H9a and historical G | Absent from current forward engine | Correct separation: not permitted extra stages in Rule3-only runs. |
| P8/H15 physical energy, momentum, etc. | Arithmetic balance/residuals only | Open identification and calibration obligations. |
| H6–H7/H16–H17 detector/selection/quantum claims | Passive C0/C1/C2 classification | No collapse, winning detector, Born probabilities or maximizing-history implementation demonstrated. |

## What the baseline tests establish

The original 15 tests and positive/signed CLI audits check implementation
properties for finite cases. The reflection audit additionally exhausts its
finite permutation search class and verifies exact finite tensor identities;
its covariance conclusion for arbitrary state follows from the separate algebra.
A finite scalar test cannot replace the constructive global inverse proof.
Full logs and runtime metadata are under `research/baseline_audit/`.

The sparse representation omits only triples equal to a declared fixed
background. Every omitted channel still has a defined retained triple; this is
not deletion of microscopic information. Dense state coverage, all six remainder
backgrounds and all sign choices were separately exercised by the review.
