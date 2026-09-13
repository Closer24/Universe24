# Shared named model definitions

Use one [definitions file](../examples/named-definitions/definitions.json) as the
authoring source for a model's fields, disturbance types and local rules. The
[near](../examples/named-definitions/near.json) and
[shifted](../examples/named-definitions/shifted.json) experiments both use that
file; neither repeats a field, type or coupling definition.

## One owner per definition

A definitions document has exactly `definitions_version: 1` and `model`.
The model uses the existing [initialization sections](DISTURBANCES.md), including
`schema_version`, `model_id`, `fields`, `disturbance_types` and optional physical
rule sections. Their schemas and ordered rule execution are unchanged.

| Edit | Single location |
| --- | --- |
| Add, rename or remove a field | `model.fields`; every entry has one unique `name` |
| Add, rename or remove a disturbance type | `model.disturbance_types`; every entry has one unique `name` |
| Select the fields carried by a disturbance | Its `fields` list references existing field names; at least one is required |
| Define a local physical coupling | The applicable existing rule section inside `model`, referencing field/type names |
| Place occurrences or change initial values | Experiment `world.seeds` references type names and supplies positions/value overrides |

A carried field is owned state, not an automatically activated interaction.
`couplings` exchanges between carriers; `emissions`, `spatial_couplings` and
`spatial_interactions` define explicit carrier/field behavior under their existing
contracts. A disturbance may respond to one or several fields. The example has
one type with one response and another with two responses. An uncoupled type
remains legal; adding a name never invents a force or an emission law.

Rename all references as part of the same edit, then validate. Deleting a field
or type while another definition, rule or placement still refers to it fails.
Unused definitions can be removed if the remaining model satisfies its existing
minimum capacities. No rule or placement is silently removed to make a file pass.
Validation reports the first error; it does not mutate or save the input files.

This version represents one complete bounded model, not an unlimited species
registry. The existing limits of 16 fields, 16 types and bounded rule counts
apply to the whole definition, including currently unplaced types. There is no
automatic subset resolver. Different historical research examples and the
descriptive physical catalog retain their separate contracts; they are not
silently converted into one physical theory.

## Experiments and validation

An experiment has exactly `experiment_version: 1` and `world`. World keys are
`shape`, `boundary`, `slots_per_cell`, `link_ticks`, `normal_budget`, `ticks`,
`operation_costs`, `seeds`, `spatial_seeds`, `observer` and `event_program`.
Required values and optional defaults follow ordinary initialization. Native
programs, including their operations and instruments, remain a separate
world-bound behavior input with their existing restrictions; this format
does not enable a previously unsupported mechanism composition.

Experiments cannot replace model-owned definitions. Definitions cannot contain
world-owned settings. Supply the definition dependency explicitly; file names,
adjacent files and Python imports are never searched automatically.

```sh
python -m event_universe.configuration_validation examples/named-definitions/definitions.json
python -m event_universe.configuration_validation examples/named-definitions/near.json --definitions examples/named-definitions/definitions.json
python -m event_universe.model_definitions --definitions examples/named-definitions/definitions.json --experiment examples/named-definitions/near.json --output-init artifacts/named-input.json
python -m event_universe --init artifacts/named-input.json --output artifacts/named-run
```

Use new output paths. The first two commands only validate. The third assembles
ordinary JSON; it does not compile or rebuild simulator code. The last command
uses the existing runner, which saves the fully resolved initialization. Later
source edits cannot change that saved input or an already initialized world.

The host adapter `model_definitions.py` owns document separation and composition.
`initialization.parse_initial_state` remains the single semantic validator for
names, field references, payloads, local expressions and compatible mechanisms.
Independent definition validation supplies a small empty context to that parser;
it neither creates a `Simulation` nor claims to be an authored experiment.
Combined validation checks the actual world, placements, observer and event
program before returning a detached input snapshot.

The APIs are `validate_model_definitions(document)`,
`prepare_experiment(definitions, experiment)` and
`compose_initialization(definitions, experiment)`. The first returns typed
validation context; the second returns the resolved dictionary and typed initial
state; the third returns only the dictionary. They read no files and mutate no
caller objects. Copies are temporary host authoring data, with no persistent
registry or per-tick lookup; dynamic cell and packet storage are unchanged.

The shared preflight accepts `definitions_source=` for experiment text/bytes and
reports dependency errors against `definitions`. A valid model is not proof that
every future run conserves a proposed physical quantity. Runtime bounds and
configured conservation guards remain in their current owners.
