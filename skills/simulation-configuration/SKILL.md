---
name: simulation-configuration
description: Check, author and explain Universe24 JSON configurations for space, reusable entities, fields, interactions, run controls and display settings. Use when checking, preparing or modifying an experiment, without changing simulator code during configuration work.
---

# Configure a simulation

For a check request, return the existing file's validation report. For authoring,
produce a validated initialization file, its reusable dependencies, an exact run
command, and display settings when requested. Apply the shared
[configuration task scope](../workflow.md#configuration-tasks-and-implementation-scope)
before choosing a workflow; a validation failure does not authorize simulator edits.
Follow the repository's
[shared workflow](../workflow.md). This skill owns experiment authoring;
[simulation-runner](../simulation-runner/SKILL.md) owns execution and evidence.
Apply the [local integer operation contract](../../docs/ARCHITECTURE.md#local-integer-operation-contract)
to configured laws, intermediate bounds and the origin of physical inputs.

Read the [configuration guide](references/configuration-guide.md) for the complete
file map, supported choices, commands and troubleshooting. It links the maintained
schema contracts rather than creating a second schema. Start from the included
[two-stream template](assets/two-streams.json) for basic periodic motion, or select
the example family in the guide for fields, catalog entities or native events.

## Author the requested experiment

1. Establish the desired observation and a bounded acceptance case: which entities
   meet, where, duration, quantities to measure and whether visual output is wanted.
   Reuse explicit user choices. Resolve routine defaults from an existing example.
2. Choose the supported schema and mechanism before assigning physical labels.
   Use schema 1 for local field rules, schema 2 for finite dissipative outward
   fields. The classical causal graph supports both; native quantum programs
   still reject spatial fields. Follow the [graph contract](../../docs/EVENT_GRAPH_CONFIGURATION.md)
   for provenance granularity, capacity and failure behavior.
3. Define the space and run envelope. Set boundary explicitly, keep every seed
   in range, and distinguish transit time, computation delay and playback speed.
   Select [shared field computation delay](../../docs/SPATIAL_COMPUTATION_DELAY.md)
   explicitly when fields must wait under the same budget as carriers.
4. Define field structure and units once, then reusable disturbance types or catalog
   profiles. Place repeated occurrences through seeds with value overrides. A name
   such as electron, mass or electric_field does not select a force or formula.
   For known physical numbers, use the shared [reference units](../../docs/REFERENCE_UNITS.md)
   registry and explicit Scalar/Vector encoder. Preserve reported rounding error,
   distinguish model timing from Planck h, and do not repeat defining constants
   in per-entity profiles or treat unit conversion as a new interaction law.
5. Choose carried-record or spatial-field ownership for each amount. Add explicit
   source, response or encounter rules only as needed. Count resident and actual
   in-flight stock once; received projections and display vectors are not new stock.
6. Write the rule's expected result and conservation definitions. `conserved: true`
   is a linear amount declaration, not proof of kinetic or field energy. For a new
   physical hypothesis, assign a new model identity and use the existing field
   development and physics review workflow; do not invent an unsupported JSON key.
7. Use the [configuration preflight](../../docs/CONFIGURATION_VALIDATION.md) for
   the exact file kind and explicit dependencies. Validate all supplied profiles,
   then the final compiled initialization. For a check-only request, return its
   report without constructing `Simulation`. When behavior needs verification,
   run the smallest useful headless acceptance case separately and inspect
   completion, source/config identity, events and declared balances.
8. When visualization is requested, record the same configured run and render only
   its saved state. Keep camera, arrows and playback in the selected display format.
   Inspect the encounter and boundary frames and decode the exported GIF.

For explicit energy/momentum acceptance, use the supported
[`conservation` declaration](../../docs/LOCAL_CONSERVATION.md). Declare physical
owners and units independently of labels, and preserve the requested source and
boundary scope. A source rejected by the closed audit is an unsupported
composition, not permission to remove that source or invent a residual reservoir.
Measurement expressions do not supply the physical law; a passing configuration
or audit is not a derivation of catalog interactions.

## Deliver reusable files

Keep reusable definitions and experiment inputs separate from disposable run outputs.
Use existing authoring adapters to assemble ordinary initialization JSON; this is
data preparation, not a Python/native-code compilation step. The final file is
self-contained: the engine does not implement generic include/import directives.
Preserve unknown user-owned metadata in its authoring document, but do not insert it
into the strict runtime schema. Record labels in the supported display format or
authoring metadata; seeds accept only position, type and values.

Give the user the source configuration, dependent catalog/law/display paths, the
exact command, accepted outcome and remaining physical limits. Clearly distinguish
a configuration that parses, a run that completes, and a law that meets its stated
acceptance test. Report any unsupported requested composition rather than silently
substituting a different model. Repository files remain English; explain to the user
in their conversation language.
