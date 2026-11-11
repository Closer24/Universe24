# Historical records before the fixed-six migration

This directory preserves superseded research notes, configurations and
validation evidence. It is not part of the active model specification.

The historical source supported an adjustable integer divisor scale, larger
remainder alphabets and a 382-channel field/cosmic assembly. Those construction
choices have been retired. Their original notation and numerical records are
preserved so the history remains interpretable; they must not be treated as
current parameters, current test results or claims about the fixed-six law.

The source immediately before the migration is available at commit
`1d18ef9`. Reproduce a historical record with its corresponding historical
source and assumptions, rather than reinterpreting it using the current
engine. In particular, never silently replace a stored divisor or reduce a
stored remainder while calling that operation an exact replay.

The `universe24/` subtree retains the old package-relative organization.
The `docs/` subtree retains selected earlier public documentation versions.
`README_before_migration.md` records the former public entry point. Original
record dates and failed claims are evidence metadata, not new results.
Source-relative links in copied records refer to the original source tree;
use the corresponding historical revision when a moved link no longer resolves.

The active specification is [MODEL](../../MODEL.md), the current repository
[README](../../../README.md), and [research status](../../RESEARCH_STATUS.md).
