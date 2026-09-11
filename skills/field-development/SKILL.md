---
name: field-development
description: Implement or repair Universe24 local field transport and response candidates with explicit laws, bounded state and causal inputs.
---

# Field development

Read [the shared workflow](../workflow.md), [field interfaces](../../docs/FIELDS.md)
and [the physical feature procedure](../../docs/PHYSICAL_FEATURES.md).

**Scope:** reusable field/source/gradient calculations and candidate composition.
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

Check a minimal failing input first, then an external-source control so a cure
does not erase all interaction. Keep periodic return distinct from free-space
acceptance. Define any scalar/stream conversion before exposing an API for it;
reject unsupported input instead of silently ignoring it.

Use local source edits and the existing Python validation tools. Coordinate
schema edits with architecture. Hand the changed law and its dependency path to
[physics-rule-validation](../physics-rule-validation/SKILL.md), then tests and
simulation. Do not claim completion while a retained acceptance assertion fails;
return the precise remaining law/contract problem to Boss.
