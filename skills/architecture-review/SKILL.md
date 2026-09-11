---
name: architecture-review
description: Review Universe24 state schemas, component ownership, interface composition and cross-branch integration boundaries.
---

# Architecture review

Read [the shared workflow](../workflow.md) and the current
[architecture](../../docs/ARCHITECTURE.md). Input is a commit/diff, candidate
contract and dependent changes; output is a scoped compatibility verdict with
file references and required fixes.

Trace responsibilities across generic calculations, model assembly, engine
scheduling/commits, public API, scenario setup and read-only diagnostics. Models
must compose shared calculations; neither a new model nor a compatibility facade
may become a second owner of arithmetic. Review actual imports and data flow,
not just the directory names or a passing static gate.

For repository changes, use [monorepo ownership](../../docs/ARCHITECTURE.md#monorepo-ownership).
Check that a fresh checkout can find the active model, required commands and live
work through the root entry point. Keep path maps and rules in their single owners.
Do not split packages or processes merely to satisfy a directory convention.

For a schema/interface change, identify register owners, fixed sizes, bounds,
defaults and every consumer. Inspect movement, transit, field exchange,
recording/rendering and frozen-state projections when affected. Separate model
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
