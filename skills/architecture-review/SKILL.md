---
name: architecture-review
description: Review Universe24 state schemas, component ownership, interface composition and cross-branch integration boundaries.
---

# Architecture review

Read [the shared workflow](../workflow.md) and the current
[architecture](../../docs/ARCHITECTURE.md). Input is a commit/diff, candidate
contract and dependent changes; output is a scoped compatibility verdict with
file references and required fixes.

Reconcile the affected system capabilities using the shared
[live specification procedure](../workflow.md#live-system-specification). For
Focus and quantum work, distinguish the spatial hierarchy used to locate or
refine a request from the causal dependency graph used to resolve quantum history.
Review their common event identity/request/result boundaries through the
[native event contract](../../docs/NATIVE_QUANTUM_EVENTS.md) and the
[Focus experiment contract](../../docs/QUANTUM_FOCUS.md). Reading or traversing a
hierarchy is not itself a measurement; an explicit instrument owns outcome
selection. Shared event metadata does not make quantum state and an event the
same object. Full Focus/quantum/spatial-field composition remains a hypothesis
until the actual contracts, implementation and acceptance evidence support it;
do not infer that capability from a unified explanation in Highlights.

For the active API, read [DISTURBANCES.md](../../docs/DISTURBANCES.md).
Apply the [local integer operation contract](../../docs/ARCHITECTURE.md#local-integer-operation-contract)
to the complete physical dependency path. Report unsupported tensor shapes and
separately scoped historical/quantum paths instead of certifying all code as local.
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

For repository changes, use [monorepo ownership](../../docs/ARCHITECTURE.md#monorepo-ownership).
Check that a fresh checkout can find the active model, required commands and live
work through the root entry point. Keep path maps and rules in their single owners.
Do not split packages or processes merely to satisfy a directory convention.

For configuration tasks, keep diagnosis and implementation within the shared
[task scope](../workflow.md#configuration-tasks-and-implementation-scope).
An unsupported composition or suspected defect is a review finding; implement
changes only within an authorized implementation scope.

For configuration changes, apply the
[validation boundary](../../docs/CONFIGURATION_VALIDATION.md): one strict JSON
decoder, one semantic owner per format, and a thin dispatcher with explicit context.
Trace CLI, UI, runner and sidecar entry points. Preflight must not construct a world,
execute a profile, select laws from physical names, or claim runtime/physics proof.
Keep runtime-dependent bounds in their owner and reject unsupported file formats.

For a schema/interface change, identify register owners, fixed sizes, bounds,
defaults and every consumer. Inspect movement, transit, field exchange,
recording/rendering and current state contracts when affected. Separate model
local cost from dictionary/frontier/history costs on the host.

Apply the [per-change memory and system review](../workflow.md#memory-and-system-architecture)
to every change. Use [the memory contract](../../docs/MEMORY.md) to distinguish
live state, reserved capacity, retained metadata, worker copies and disk archives.
The permanent tests complement source review; neither a worker limit nor fixed
local registers establish bounded total host memory.

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
