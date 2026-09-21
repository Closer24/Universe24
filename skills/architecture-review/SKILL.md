---
name: architecture-review
description: Review Universe24 state schemas, component ownership, interface composition and cross-branch integration boundaries.
---

# Architecture review

Apply [the published-design requirement](../workflow.md#implement-from-a-published-design). Own contract reconciliation and publish resolved revisions before dependent behavior changes; review the implementation against its cited design.

Read [the shared workflow](../workflow.md) and the current
[architecture](../../docs/ARCHITECTURE.md). Input is a commit/diff, candidate
contract and dependent changes; output is a scoped compatibility verdict with
file references and required fixes.

For the active API, read [the Beam Law](../../docs/BEAM_LAW.md) and
[the engine's bookkeeping](../../docs/ENGINE.md); the generic disturbance
contract (DISTURBANCES.md) was deleted on 2026-09-19.
Apply the [local integer operation contract](../../docs/ARCHITECTURE.md#local-integer-operation-contract)
to the complete physical dependency path. Report unsupported tensor shapes and
separately scoped historical paths instead of certifying all code as local.
Check the full initialization-to-expression-to-proposal path, fixed capacities,
positive payload coding, frozen pending ownership and lazy optional rendering.
Historical scalar records are not the universal schema. Missing initialization
must fail rather than silently selecting built-in physics.

Verify genericity by renaming labels through their semantic reference positions
and permuting declarations, then comparing actual states, events, costs and
ledgers. Include labels that resemble schema/operation keywords or JavaScript
prototype members when checking adapters. Preserve declared rule and axis order;
keyword searches alone cannot establish behavior independence. Require observed
activity in each comparison so an idle scenario cannot silently pass.

Trace responsibilities across generic calculations, model assembly, engine
scheduling/commits, public API, scenario setup and read-only diagnostics. Models
must compose shared calculations; neither a new model nor a compatibility facade
may become a second owner of arithmetic. Review actual imports and data flow,
not just the directory names or a passing static gate.

For energy/momentum auditing, trace the
measurement boundary: actual records, joint
node fields and actual packet owners must be counted once. Check nonlinear
packet changes and complete carrier commits, not only intermediate couplings.
Host-wide inventory snapshots are diagnostic inputs only; no residual, expression
cost or audit state may drive physical rules or model timing. Keep passive
postcommit failure distinct from a physical rule's precommit atomic guard.

For repository changes, use [monorepo ownership](../../docs/ARCHITECTURE.md#monorepo-ownership).
Check that a fresh checkout can find the active model, required commands and live
work through the root entry point. Keep path maps and rules in their single owners.
Do not split packages or processes merely to satisfy a directory convention.

For configuration tasks, keep diagnosis and implementation within the shared
[task scope](../workflow.md#configuration-tasks-and-implementation-scope).
An unsupported composition or suspected defect is a review finding; implement
changes only within an authorized implementation scope.

For configuration changes, apply the
validation boundary: one strict JSON
decoder, one semantic owner per format, and a thin dispatcher with explicit context.
Trace CLI, UI, runner and sidecar entry points. Preflight parses immutable world definitions but must not construct a Simulation,
execute a profile, select laws from physical names, or claim runtime/physics proof.
Keep runtime-dependent bounds in their owner and reject unsupported file formats.

For a schema/interface change, identify register owners, fixed sizes, bounds,
defaults and every consumer. Inspect movement, transit, field exchange,
recording/rendering and current state contracts when affected. Separate model
local cost from dictionary/frontier/history costs on the host.

Map PR overlaps before combining them. Preserve both sides of an API extension
when resolving an import conflict; do not overwrite a newer component with an
older full file. Recommend one writer for a shared interface during integration.

Use read-only source/diff inspection and the existing architecture/type gates;
edit only an assigned interface or integration scope. A pass applies to the
reviewed tree and stated scope. Send physical dependency concerns to the physics
reviewer, behavioral coverage gaps to tests, and unresolved ownership conflicts
to Boss. Pure test deduplication is acceptable when independent assertions and
contract coverage remain intact.


For naming/consolidation changes, inspect the
[canonical-copy and naming rules](../../AGENTS.md#repository-language-english).
Keep public exports distinguishable from historical internal owners, route shared
example inputs to one file, and recheck dynamic resource consumers as well as
imports. Preserve revision-specific evidence rather than rewriting it to resemble
the renamed source. The [documentation index](../../docs/README.md) must route each
contract without becoming another copy of its definitions.

For external entity definitions, trace [the canonical loading boundary](../../docs/ENTITY_DEFINITIONS.md)
from reusable data and placement to the immutable expanded world. Verify that all
entry points use that provider, portable inputs retain exact dependencies after
relocation, and names affect labels rather than physical rules. File ownership
outside the engine never supplies physical memory from outside the GameBoard. Review both source
and installed example paths and keep authoring limits distinct from physical
capacities.

## Notation (the owner, 2026-09-21, record 184)

Every symbol is named in English at its first use (never a Greek letter alone: "gamma (the Lorentz factor)"), and its kind is shown by its type: a scalar plain, a vector in bold lowercase (**p**), a tensor, matrix or operator in bold uppercase (**C**); skills/workflow.md, "Notation".
