---
name: field-development
description: Implement or repair Universe24 local field transport and response candidates with explicit laws, bounded state and causal inputs.
---

# Field development

Before behavior edits, apply [the published-design requirement](../workflow.md#implement-from-a-published-design). Implement the cited design revision; return missing laws or interface decisions to its owner before adding behavior.

Read [the shared workflow](../workflow.md), [field interfaces](../../docs/SCALAR_FIELDS.md)
and [the physical feature procedure](../../docs/PHYSICAL_FEATURES.md).

The active field contract is [DISTURBANCES.md](../../docs/DISTURBANCES.md).
Configure identities and supported laws in JSON; do not add field-name branches
or Python execution to the loader. Whole-record movement, extensive splitting,
source accounting and paired exchange are distinct contracts.

**Scope:** reusable local calculations and candidate composition.
The engine owns scheduling and commits; models select laws rather than copying
arithmetic. Inputs are the task's candidate, required behavior and local contract.
Output is an implementation plus numerical examples, tests and a review handoff.

Before editing, distinguish law, local inputs and causal provenance, fixed
evolving state, immutable parameters, derived quantities and output proposals.
Use the current [definitions](../../SIMULATOR_DEFINITIONS.md) for bounds and model
exceptions. A new physical hypothesis needs its own explicit identity.

For self-field work, inspect every upstream dependency. A local subtraction is
not local physics if its estimator uses a shadow world, source history or global
knowledge. Keep persistent source behavior, causal delivery and equal/opposite
momentum exchange explicit; disabling response is not a self-force solution.
The two existing ordering policies, `field_phase_first` and `arrival_port_blind`
in [spatial couplings](../../docs/SPATIAL_COUPLINGS.md#field-phase-first-ordering),
show the required test shape: an isolated straight emitter, a maximum-speed
turn, a held external-source control and rejected combinations.

Check a minimal failing input first, then an external-source control so a cure
does not erase all interaction. Keep periodic return distinct from free-space
acceptance. Define any scalar/stream conversion before exposing an API for it;
reject unsupported input instead of silently ignoring it.

When moving sources and field packets share explicit transit times, test
coarrival, turns with alternate paths, and periodic return before asserting
self exclusion. Field-first callback order alone is not an attribution proof.
Keep illustrative uniform shells separate from the actual local branching law.

For rotating field response, distinguish conserved combined vector components
from preserved carrier norm. Require an external transverse-source control when
parallel self flux produces no rotation. Price delayed atomic reactions without
rewriting old in-flight packets or claiming reservation tariffs are measured host
instruction counts; see [spatial response](../../docs/SPATIAL_COUPLINGS.md).

For shared computation timing, keep original stock, frozen proposals and later
input distinct. Test input arriving during a wait and at the ready tick,
including empty intervals. Price bounded physical merges before freezing the
ready time; revalidate joint guards before ownership changes. See the
[shared-cycle contract](../../docs/SPATIAL_COMPUTATION_DELAY.md).

When a candidate claims energy and momentum conservation, define all owner
contributions and actual six-port flux under the
[local conservation contract](../../docs/LOCAL_CONSERVATION.md). Show that the
same quantities survive scattering, transport, merging and the complete coupled
update. A component transformation ledger is not an energy reservoir. Keep the
elementary state-generating rule independent of the measurement and of any
repair that would force its residual to zero.

Use local source edits and the existing Python validation tools. Coordinate
schema edits with architecture. Hand the changed law and its dependency path to
[physics-rule-validation](../physics-rule-validation/SKILL.md), then tests and
simulation. Do not claim completion while a retained acceptance assertion fails;
return the precise remaining law/contract problem to Boss.
