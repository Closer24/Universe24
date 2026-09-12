---
name: simulation-configuration
description: Author and explain Universe24 JSON configurations for space, reusable entities, fields, interactions, run controls and display settings. Use when preparing or modifying an experiment, without adding simulator laws implicitly.
---

# Configure a simulation

Produce a validated initialization file, the reusable definitions it depends on,
an exact run command, and display settings when requested. Follow the repository's
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
   fields. Native event programs currently cannot compose with spatial fields.
3. Define the space and run envelope. For nondefault links, use the
   [configured topology contract](../../docs/CONFIGURED_TOPOLOGY.md): supply offsets
   and the site pattern, rather than a neighbor count alone. Check seed membership,
   supported field laws and reciprocal links. Distinguish three vector components
   from D ports, and graph transit from Euclidean speed. Set boundary explicitly
   and distinguish transit time, computation delay and playback speed.
4. Define field structure and units once, then reusable disturbance types or catalog
   profiles. Place repeated occurrences through seeds with value overrides. A name
   such as electron, mass or electric_field does not select a force or formula.
5. Choose carried-record or spatial-field ownership for each amount. Add explicit
   source, response or encounter rules only as needed. Count resident and actual
   in-flight stock once; received projections and display vectors are not new stock.
6. Write the rule's expected result and conservation definitions. `conserved: true`
   is a linear amount declaration, not proof of kinetic or field energy. For a new
   physical hypothesis, assign a new model identity and use the existing field
   development and physics review workflow; do not invent an unsupported JSON key.
7. For reusable files, use the [experiment package](../../docs/EXPERIMENTS.md)
   manifest and typed parts. Use [explicit SI dimensions](../../docs/UNITS.md)
   when dimensional validation is required. Validate packages with
   `--experiment ... --validate`. For initialization, catalogs, profiles and
   observers, use the [configuration preflight](../../docs/CONFIGURATION_VALIDATION.md)
   with explicit dependencies. Validate all supplied profiles, then the final
   compiled initialization. For a check-only request, return its report without
   constructing `Simulation`. When behavior needs verification, run a separate
   small headless acceptance case and inspect completion, source/config identity,
   events and declared balances.
8. When visualization is requested, record the same configured run and render only
   its saved state. Keep camera, arrows and playback in the selected display format.
   Inspect the encounter and boundary frames and decode the exported GIF.

## Deliver reusable files

Keep reusable definitions and experiment inputs separate from disposable run outputs.
Use `--experiment` or the existing authoring adapters to assemble ordinary initialization JSON; this is
data preparation, not a Python/native-code compilation step. The final file is
self-contained: local includes belong to versioned package parts, not runtime laws.
Export the formal schemas with `--schema`; canonical validation also checks names,
integer JSON tokens, dimensions and semantic constraints beyond JSON Schema.
Preserve unknown user-owned metadata in its authoring document, but do not insert it
into the strict runtime schema. Record labels in the supported display format or
authoring metadata; seeds accept only position, type and values.

Give the user the source configuration, dependent catalog/law/display paths, the
exact command, accepted outcome and remaining physical limits. Clearly distinguish
a configuration that parses, a run that completes, and a law that meets its stated
acceptance test. Report any unsupported requested composition rather than silently
substituting a different model. Repository files remain English; explain to the user
in their conversation language.
