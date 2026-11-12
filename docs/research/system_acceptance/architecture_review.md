# Independent architecture review

## Decision

The execution architecture is suitable for a single supported system: complete
immutable input bundle, fixed Rule3 Engine, passive canonical decoder, saved
trace and exact verification. Research integration should extend preparation,
independent acceptance and documentation around this boundary. It does not need
a second Engine, runtime selector or callback that supplies a future state.

This review accepts that software boundary and the final source-only acceptance
collector. It does not certify one combined
physical universe, recurrent cosmological bursts or sustained complexity growth.
Those conclusions require their own same-law evidence. A source merge and a
successful audit collector cannot substitute for that evidence.

## Inspected boundary

| Layer | Responsibility | Review result |
| --- | --- | --- |
| `universe24/runtime.py` | `status`, `prepare`, `run`, `verify` | One supported command surface; no implicit physical model |
| `universe24/system/bundle.py` | Exact schemas, exhaustive channel ownership, immutable data, content identity and admissibility | Revalidates inputs and detached mutable values; enforces the total 48-channel budget |
| `universe24/core/` | Complete integer transition and inverse | Preserve the fixed divisor-six rule and old-snapshot semantics |
| `universe24/system/decoder.py` | Canonical transition observations | Passive output; no detector feedback hidden in the observer |
| `universe24/system/runtime.py` | Saved execution, complete transition replay, inverse and canonical-click comparison | Same runtime for every supplied bundle; histories are external evidence |
| `validation/` | Research construction, independent oracles and acceptance experiments | Source-only; separate candidate laws must remain separately identified |

The public package does not import the source-only `validation` tree. The
package configuration includes `universe24` and excludes its tests; historical
construction helpers under `layers`, `prepare` and `observe` remain research
dependencies rather than additional public runtime entry points.

Bundle hashes detect changed content; they are not author authentication or a
physics certificate. Saved-run verification also checks the executing source
hashes. A report produced by a different core/runtime source must not silently
be relabeled as current evidence.

## Integration decisions

The final decision ledger must distinguish these categories for every retained
research family:

1. Supported execution infrastructure.
2. Included restricted physical construction, with exact domain and omissions.
3. Included mechanical building block or negative control.
4. Excluded from a proposed physical assembly because its law, domain, source,
   history, channel budget or evidence does not match.
5. Open research requirement with an explicit acceptance test.

Excluding a proposal from the physical assembly does not require deleting its
counterexample or historical evidence. These are useful regression controls.
Conversely, retaining its source does not give it production-model status.

The massless native sourced construction and the massive constrained-coordinate
construction have different tensors, preparation domains and readouts. They
may share the same execution architecture, but their successful results cannot
be pooled into a single physical certificate. The same restriction applies to
standalone native routing, retained apparatus and burst experiments.

An acceptance collector may execute several declared candidates. Its report
must say that it is collecting research results rather than evolving all those
candidates as one coupled state. Each claimed same-run relationship must bind
the tensor, complete seed, protocol, runtime source and horizon. Matching a
field ratio or a metadata name is not enough: old histories and carries matter.

## Release conditions

- Update the public status wording to distinguish unresolved general spatial
  Einstein/clock/detector physics from validated restricted homogeneous results.
  Keep `accepted_physical_model` unset and full acceptance blocked unless the
  complete claim is independently established.
- Use one visible acceptance entry point and one decision ledger. Keep internal
  audit modules available for reproduction, without presenting them as a menu
  of competing production universes.
- Give every new run a fresh output directory. Imported historical snapshots
  must retain their source identity. Several research runners write fixed
  `runs` paths, so orchestration must explicitly avoid reusing committed or
  previous-run evidence as a fresh result.
- Keep broad CI and independent negative controls. Expected physical failures
  should remain failures in the report even when the audit process exits
  successfully because it reproduced them.
- Validate the final source tree, not an earlier parent. Publish the exact
  source pin and source hashes; do not infer running work from an open PR.
- Keep user-facing documentation free of a competing default or hidden model
  switch. State the exact positive scope and resource cost before discussing
  broader targets.

## Burst and complexity acceptance boundary

A recurrence, a phase wrap, periodic routing or a threshold crossing is not
automatically a cosmological burst. A new burst claim needs a declared event
definition, one immutable tensor, complete preparation and retained transitions
through several episodes. The same definitions and thresholds must be fixed
before comparing preparations or selecting favorable runs.

Sustained complexity growth additionally needs a declared structural measure,
enough post-transient episodes, controls for passive translation and trivial
amplitude/bit growth, and continued operation without resetting ready memory.
Every clock, scheduler, recorder and energy source must fit the same counted
state. The final report must distinguish a finite positive example, repeated
mechanical activity and a physical cosmological interpretation.

These criteria are release boundaries for a claim, not a reason to suppress a
well-identified failed experiment. A working runtime with a failed growth gate
is a valid software result and an incomplete physical result.

## Executed checks and scope

The review executed the two focused public-boundary test modules:

```text
python -m unittest universe24.tests.test_system_cli universe24.tests.test_system_runtime -v
```

All 13 tests passed. They cover the 48/49 boundary, exact scalar oracle,
causal perturbations in every retained bank, malformed preparation, arbitrary
precision, deterministic saved files, inverse/replay, changed or incomplete
traces/clicks, and forged physics/source claims.

A wheel was built without downloading dependencies. Inspection confirmed that
the 115 packaged files exclude `validation` and the test tree and expose only
the `universe24` console entry. An isolated interpreter loaded the unpacked
wheel outside the checkout import path, created a complete bundle, executed
three ticks and verified its saved trace and clicks. It retained the unset
physical default. This checks the installed execution boundary rather than
assuming that checkout-only imports will work after packaging.

The initial review inspected the public runtime, bundle, decoder/package
boundary, existing CI, proposal inventory and the incoming sourced-map and
unified-law runner interfaces. Full mathematical review and final combined
CI remain separate acceptance responsibilities. The review does not describe
unexecuted tests as completed.

## Final source-level review

The final `validation/system_acceptance` collector satisfies the reviewed
boundary. It executes native massless, massive constrained-coordinate and
Boolean selection controls through the existing saved-run runtime, and labels
their laws and physical domains separately. It rejects joins between different
tensors, complete seeds, protocols, horizons and source identities. Its output
explicitly leaves the combined physical model and same-law burst/growth target
unestablished. No runtime model selector or new retained state was introduced.

Review found an incomplete source-hash set: the initial collector omitted
locality and indirect preparation/oracle dependencies. This was corrected to
cover all repository-owned Python under `universe24` and `validation`, excluding
tests. A regression checks important indirect paths. Receipts explicitly check
compatibility, not authentication; their dataclass type is not represented as
an unforgeable proof of origin.

The burst audit preserves the existing three-channel law and structural score.
Its complete 512-state ring enumeration supplies the recurrence conclusion;
the illustrative recurrent witness does not replace the population result or
the preselected single-pulse control. Recurring memory-event peaks are reported
separately from failed structural growth and unidentified cosmological bursts.

The public status now acknowledges the restricted homogeneous results while
retaining blocked general acceptance and an unset physical default. Its
`--require-physics` behavior is unchanged. The 13 public-boundary tests passed
again after that wording change. The four collector adversarial tests and four
burst tests also passed independently, eight tests in total. They retain the
same-field/different-carry rejection, corrupt-byte rejection, provenance closure,
fresh-output refusal and exhaustive recurrence/growth negative controls.

No unresolved software-architecture blocker was found in these final changes.
The coordinator must still validate the final published source tree and its
complete CI before a merge claim. Software approval does not convert the open
physical gates into successful results.
