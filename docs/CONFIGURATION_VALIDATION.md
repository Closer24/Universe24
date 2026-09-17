# Configuration validation

Validation is a read-only host operation. It checks declared data and supported
composition; it does not construct `Simulation`, allocate a causal world, execute
an experiment, render output or create artifacts. A valid configuration, a run
that completes, and a physically accepted hypothesis are three separate results.

## Ownership and flow

`JSON text -> json_documents -> configuration_validation -> format owner -> report`

| Layer | Owner | Responsibility |
| --- | --- | --- |
| JSON decoding | `json_documents.parse_json_document` | Reject duplicate keys at every depth, malformed JSON, nonfinite constants and exponent overflow; preserve ordinary integers and finite metadata floats |
| Dispatch and composition | `configuration_validation` | Select an explicit format, require supplied dependencies, coordinate initialization/observer exclusivity, return a report |
| Initialization | `initialization.parse_initial_state` | Schema versions 1/2, fields, bounded values, references, placements and supported mechanism composition |
| Physical reference | `entity_catalog.validate_catalog` | Version 2 metadata, measurements, reciprocal identities and possible interaction references; reject executable catalog content |
| Representation profiles | `entities.validate_profiles` | Version 1 bindings against an explicit version 2 catalog; compile every present classical profile independently through the existing owner |
| Observer | `observer_configuration.ObserverDefinition.parse` | Position within the supplied world's shape and receipt capacity |
| Entry points | CLI, UI, runner | Explicit file reading, transport limits, output/exit formatting and actual execution when requested |

The facade delegates semantic rules; it must not become a second schema or
physical-law implementation. `initialization.parse_json_document` remains an
explicit re-export for existing callers. All external observer reads use the same
strict decoder. Domain parsers remain independently usable and keep their typed
results and exceptions. The facade converts known input errors into reports;
programmer errors are not swallowed as ordinary invalid configurations.

`prepare_initialization(document, observer_document=...)` returns parsed initial
state and the optional observer. It is shared by preflight and the runner. An
explicit sidecar, including JSON `null`, is validated as supplied. Declaring both
an inline observer and a sidecar fails. `validate_observer_selection` shares this
source-conflict check with the runner before it reads any external sidecar. The UI's 1 MiB request limit remains a UI
policy. Runner paths, tick overrides, output ownership and retention remain runner
policies. The runner preserves the exact initialization bytes it actually reads.

## Supported files and explicit context

| Kind | Detection in auto mode | Extra context |
| --- | --- | --- |
| `initialization` | `schema_version` | None |
| `catalog` | `catalog_version` | None; only the physical reference version 2 is supported by this facade |
| `profiles` | `profile_version` | `--catalog` or `catalog_source` |
| `observer` | Never inferred | Explicit kind and `--initialization` or `initialization_source` |

Auto mode requires exactly one of the three discriminator keys. It does not infer
semantics from a filename, `model_id`, or merely valid JSON. Explicit kinds still
run their owner's complete schema checks. Unused dependency arguments fail rather
than silently ignoring a mistaken command. Dependencies are supplied explicitly;
there are no include directives, automatic neighboring-file searches or imports
of configuration-selected Python. Existing legacy embedded catalog compilation is
unchanged and is not certified by this version 2 reference validator.

Profile validation covers every representation present in the supplied file,
including rows not selected for an experiment. It permits a subset and a single
representation per entity. Passing individual profiles does not establish that
all profiles can be combined into one bounded world: validate the final compiled
initialization as well.

Example-specific authoring and display formats remain owned by their adapters.
In particular, `directional-wave/{definition,experiments,display}.json` and
`particle-contracts/entities.json` are reported as unsupported here. Use their
documented authoring contract and validate the generated initialization. Adding a
format requires one clear owner, an explicit discriminator/context contract, and
positive, negative and no-execution tests; do not add a permissive JSON fallback.

## Commands and API

Use the configured Python environment from the repository root (editable install
or `PYTHONPATH=src`). These commands only read their explicit inputs:

```sh
python -m event_universe.configuration_validation examples/basic.json
python -m event_universe.configuration_validation examples/basic.json examples/finite_fields.json --json
python -m event_universe.configuration_validation examples/known-entities/catalog.json
python -m event_universe.configuration_validation examples/known-entities/representation-probes.json --catalog examples/known-entities/catalog.json
python -m event_universe.configuration_validation observer.json --kind observer --initialization examples/basic.json
```

`validate_configuration(source, *, kind="auto", catalog_source=None,
initialization_source=None)` accepts text or bytes and returns `ValidationReport`.
It performs no filesystem access. `valid`, resolved `kind`, success `summary` and
`issues` are available as attributes; `to_dict()` produces serializable data.

The CLI reports every requested path and exits 0 if all are valid, 1 on invalid or
unreadable input, and 2 for invalid command syntax. With `--json`, stdout contains
one object with `report_version: 1`, overall `valid`, and `results`. Each result
contains `path`, `kind`, `valid`, `summary`, and `issues`. Each issue has `code`,
`document` (`input`, `catalog`, or `initialization`), `message`, and nullable
`line`/`column`. JSON syntax errors carry locations when the decoder supplies
them; semantic errors do not invent JSON pointers. Codes distinguish `syntax`,
`unsupported_kind`, `missing_dependency`, `unexpected_dependency`, `validation`
and `io`. A failed file reports its first concrete error, not an exhaustive list
of faults in a partially parsed document. Nesting that exceeds decoder or semantic
traversal depth is an invalid-input report, so later files still receive reports.
A failure before kind detection retains
`auto` or the requested kind.

## Guarantees and remaining runtime checks

Static validation checks schema structure, bounded declared inputs, references,
supported compositions and determinable initial requirements. It does not prove
future occupancy, exact divisibility of future intermediates, future event-space
sufficiency, conservation of a chosen equation, or agreement with physical data.
Keep transactional and runtime bounds in their existing owners. Do not weaken a
law, increase a capacity silently, or infer formulas from reference measurements
to obtain a passing report.

The behavioral expectations are recorded in
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md#configuration-preflight). Reuse existing
parser and runtime regressions when changing a shared validation boundary.
