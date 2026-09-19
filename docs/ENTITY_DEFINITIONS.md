# Reusable entity definitions

The model owner clarified on 2026-09-19, translated from Hebrew: "The detector
settings are in an entity definitions file, not in the engine; make sure the
workflow is in the appropriate skill." This is an authoring/loading contract,
not a new physical model. It supersedes the earlier assumption that inline world
data alone completed that request. The engine continues to receive the immutable
ordinary Events and detector groups specified by [ENGINE.md](ENGINE.md) and
[the detector candidate](DETECTOR_REQUIREMENTS.md). An external definition file
is outside the engine; the instantiated detector is physically on the board.

## Ownership and supported composition

`event_universe.world_loading` is the single host owner of strict document
resolution, entity placement and portable input assembly. It uses
`json_documents.parse_json_document` for every JSON document, then
`events.world.parse_event_world` for the fully expanded world. That engine parser
remains the one owner of physical schema and domain validation. Physical modules
never open entity files, consult a catalog, branch on an entity name or retain
instance definitions as evolving memory. The loader executes no Python,
expressions, formulas, callbacks or network requests.

An ordinary inline world remains supported with identical loading and original
input bytes. New detector examples keep reusable apparatus definitions in a
separate file. Existing generic rule names select the already specified local
laws; family names, geometry, material parameters, routes, coverage, groups and
thresholds are configuration data. Translation does not prove connectivity or
create a signal. Placement outside the board is invalid even on a periodic axis:
periodicity governs Link transport, not silent initialization wrapping.

The first format supports one explicit definitions file and any finite ordered
list of placements within the stated host admission bounds. Definitions are
literal data, without inheritance, recursive imports, scaling, rotation, runtime
parameter substitution or instance-specific overrides. Different apparatus
settings are explicit definitions. A definition may describe a detector, a source
using an existing lamp rule, or another collection of ordinary measured Events;
the same generic expansion applies. This does not restore the deleted
`external_bodies`, entity evaluator or historical physical engine.

## Authored documents

An authored world adds exactly two host-only keys to the ordinary world object:

```json
{
  "entity_definitions": "entities/detectors.json",
  "entities": [
    {"name": "alice", "definition": "three_node_detector", "position": [3, 4, 0]},
    {"name": "bob", "definition": "three_node_detector", "position": [3, 6, 0]}
  ]
}
```

The shown fragment is added to a complete world declaring its model, families,
shape, timing, topology and physical candidate. Both added keys must occur
together. `entities` is a nonempty array. Each instance has exactly `name`,
`definition`, `position`; names are nonempty strings and instance names are
unique. Definition references must exist. Position is an exact three-integer
in-board origin; booleans are refused. The world may omit `measured` and
`detectors` when supplied entirely by instances; explicit inline arrays remain
supported and precede instance content. `in_transit` remains world preparation
data, with its ordinary numerical owner convention; there is no generated
incoming carrier or implicit owner rewrite.

The definitions document has exactly `format` and `entities`:

```json
{
  "format": "event-entities-v1",
  "entities": [
    {
      "name": "three_node_detector",
      "measured": [],
      "detectors": []
    }
  ]
}
```

The empty arrays above show the envelope only; an actual definition requires at
least one measured Event. Each definition has exactly `name`, `measured` and
`detectors`; names are nonempty and unique. Its measured entries use the existing
world measured schema, including explicit candidate tables and port maps when
applicable. `position` is relative to the instance origin. Detector entries use
the current selected world's detector schema; `positions`, group `positions`
and group `output` are also relative. All relative coordinates are exact integer
triples in -4095..4095. Every detector position and output in the definition must
refer to its own declared measured geometry. Family names refer to the world's
explicit family declarations; no familiar physical names are built in.

Host structural validation covers every definition, including unused ones.
Physical semantic validation applies when a definition is instantiated into its
world context: an unused definition is not certified for arbitrary `N`, families
or dynamics. Unsupported fields, executable extensions and duplicate relative
measured positions are refused. The host accepts the current union of ordinary
and candidate measured/detector fields; the selected world parser supplies their
actual domain, required-field and rule-combination checks.

Expansion order is inline measured entries, then instances in declaration order,
then each definition's measured declaration order. This fixes the ordinary
measured numbers 1, 2, ... without using labels to choose a rule. Detector order
is similarly inline then instance declaration order. A placed detector name is
`/INSTANCE/LOCAL`, with each component escaped as JSON Pointer text (`~` becomes
`~0`, then `/` becomes `~1`); group names remain local to their detector. Thus
renaming an instance changes labels only, and names containing `/`, `~`, schema
keywords or `__proto__` remain ordinary data. Collision with an inline name is
an error, not a rename. No field is silently overridden.

For every relative coordinate, add the instance origin once, reject an out-of-
board result and pass the result to the canonical world parser. Overlapping
instances, repeated detector coverage, invalid output ownership, integer bounds,
unknown families and unsupported local rules fail before a Simulation or output
directory is created. All existing candidate capacities remain binding.

## Resolution, public API and portable input

A file reference is a nonempty relative POSIX path with no absolute prefix,
backslash, colon, empty component, `.` or `..`. Resolution requires an explicit
`base_dir`; no current-working-directory or repository search is allowed. The
resolved file must remain within the resolved base directory, including through
symlinks. Read the dependency once, keep its bytes for validation and fingerprints,
and never reopen it while running. Entity authoring, definitions and bundle
documents are UTF-8 without a byte-order mark; the existing plain-world decoder
retains its prior behavior.
There are no nested dependency references.

The host public API is:

```
@dataclass(frozen=True)
class DefinitionSource:
    path: str
    source: bytes
    sha256: str

@dataclass(frozen=True)
class LoadedWorld:
    world: EventWorld
    portable_source: bytes
    expanded_source: bytes
    dependencies: tuple[DefinitionSource, ...]

load_world(source: str | bytes, *, base_dir: Path | None = None) -> LoadedWorld
```

`expanded_source` is deterministic JSON for the plain engine world after removing
the two authoring keys and adding the placed arrays. Serialize generated JSON as
UTF-8 with sorted object keys, compact separators, `ensure_ascii=False`, and one
terminal newline; array order is unchanged. For a plain world, `portable_source`
is exactly the input bytes (or the UTF-8 encoding of the input string), and the
parsed physical state follows the existing parser unchanged. Dependencies are
empty. No filesystem is touched for plain worlds or portable bundles.

The portable format has exactly `format`, `world` and `definitions`:

```json
{
  "format": "event-world-bundle-v1",
  "world": {},
  "definitions": {"entities/detectors.json": "THE EXACT UTF-8 DEFINITIONS JSON TEXT"}
}
```

Here `world` is the complete authored world object and `definitions` contains
exactly the one referenced path and its original source text, not executable
objects or resolved filesystem paths. Its document is decoded with the same
strict JSON decoder. Missing/extra dependencies, a nested bundle and a bundle
without entity placements are refused. The same path rules apply, but resolution
uses these supplied bytes only, never a file fallback. Bundling preserves the
exact dependency SHA-256; whitespace/key order changes in the authored world do
not change its expanded state. Loading a bundle and generating its portable form
is deterministic and idempotent.

Entity authoring inputs, each dependency and the generated portable bundle must
fit 1 MiB of UTF-8, matching the workspace input envelope. Expansion is limited
to 16 MiB of generated JSON; the loader must check projected instance expansion
before constructing a multiplied list and reject overflow. These are explicit
host input limits, not a physical saturation rule or a change to a quantum.
Plain CLI worlds retain their existing admission behavior. Invalid formats,
placements and limits raise `ValueError` with document/instance context; file
access failures retain `OSError` context. Preflight converts these into a
structured invalid report and never executes the world.

The module also provides a host command:

```bash
python -m event_universe.world_loading --input world.json --output portable.json
```

It validates and writes `portable_source` to a new file, refusing an existing
output. It does not run a world. This makes an external-file world importable
through the workspace's existing single-JSON import without granting browser
requests filesystem access.

## Required consumers and provenance

`validate_configuration` gains keyword-only `base_dir: Path | None = None` and
uses this loader. Its summary describes the expanded physical world; ordinary
summary fields and error categories remain compatible with current main
`ddb4470`, including its always-present normalized per-axis boundary summary.
Pass the authored native boundary schema through unchanged; do not restore the
superseded stricter all-axes schema. The CLI passes each input
path's parent explicitly. Source-only validation resolves a bundle without files
and refuses an unresolved file reference; it never searches implicitly.

`runner.run_initialization` passes the explicit input parent to `load_world`
before preparing the output directory. For dependency-bearing inputs it writes:

* `initialization.json`: original input bytes, as before;
* `initialization_bundle.json`: the portable dependency closure;
* `resolved_initialization.json`: the exact expanded engine document.

The existing `initialization_sha256` still hashes the original input.
`execute_event_run` gains the optional keyword-only
`initialization_record: dict[str, object] | None = None`, used only to copy
metadata under `run.json.initialization_resolution`. The runner supplies exactly
`format: "event-world-bundle-v1"`, `bundle_sha256`, `expanded_sha256`, and
`sources: [{"path": relative_path, "sha256": dependency_sha256}]` in declaration
order. It writes the two additional artifacts before stepping. They are preserved
on a recorded runtime failure. Plain runs supply no extra record or files, keeping
their artifact schema. The simulation never consumes this audit metadata.

`Workspace.templates` recursively discovers world JSON under its configured
folder, resolves each world using its own file's parent and returns portable text
for entity worlds. Definitions documents are not standalone run templates.
Template identifiers use the relative POSIX path without `.json` so nested names
do not collide; old top-level identifiers remain unchanged. Apply the existing
1 MiB request/draft limit to the generated portable source as well.

`validate_source`, Check, Export and Start accept source text or a portable bundle
through the canonical loader without a filesystem context. Templates, imported
bundles and saved drafts therefore keep their full dependency closure through
export, relocation and the subprocess input snapshot. They do not observe edits
to the original definitions file after preparation. A new template load or CLI
run may intentionally read an updated file as a new input. Expose the two extra
JSON artifacts through the same optional UI artifact allowlist/routes; the runner
still supplies the only execution path. No per-edit rebuild or new engine is used.

Ship the canonical detector definitions under
`examples/events/detector/entities/detectors.json`; example worlds reference
`entities/detectors.json`. Preserve that directory relationship in wheel and
source distributions. Convert the four detector examples to references rather
than maintain duplicate inline apparatus definitions. Definition files are
validated through their actual world consumers, not mistaken for standalone
worlds by example discovery. Update the check selector for this explicit data
dependency and preserve strict decoder and physical-parser tests.

## Independent acceptance and implementation ownership

Before code, the expected host results are fixed:

| Input or operation | Expected result |
| --- | --- |
| Definition positions `(0,0,0)`, `(1,0,0)`, `(2,0,0)` placed at `(3,4,0)` on a 9-by-9-by-1 board | Physical positions `(3,4,0)`, `(4,4,0)`, `(5,4,0)`; relative output `(2,0,0)` becomes `(5,4,0)` |
| A second placement at `(3,6,0)`, no inline material | Six measured Events numbered 1..6 in the stated order; two separate detector labels and original thresholds |
| Rename instance `alice` to `a/b~c` | Same physical payload/routing, detector prefix changes from `/alice/` to `/a~1b~0c/` |
| Separate files, their portable bundle, and the bundle copied to another directory | Equal EventWorld and expanded SHA-256; same raw definitions SHA-256; no dependency read for a bundle |
| File edited after a template was prepared | Already prepared bundle/export/Start retains its earlier state; a newly loaded template reflects the new bytes |
| Missing context/file/name, duplicate keys/names, unexpected dependency, traversal/symlink escape, overlaps or translated coordinate 9 on extent 9 | Concrete refusal before run/output creation; no clipping, fallback or silent redefinition |
| Plain legacy world | Same parsed world, original portable bytes, no dependency metadata/artifacts |

Tests isolate resolution, placement, strict failures, provenance and relocation;
use minimal generic states with independent expectations. A prepared example run
is dated evidence, not a test that pins example outputs. The loader must also
preserve the periodic extent-one detector case: replacing inline data with an
entity reference cannot alter its local law or introduce a second carrier.

The schema/authoring developer owns `world_loading.py`, the preflight adapter,
resolver tests, canonical definitions, example conversion and packaging/data-
dependency selection. The runner/workspace developer owns `runner.py`, the
metadata-only addition to `events/run.py`, `ui.py` and focused consumer tests.
The physical engine and topology provider need no entity-specific changes.
Architecture owns this contract and the skill/documentation links. The independent
test owner reviews and verifies file/bundle equivalence and portability after
both provider and consumer commits. Publish this contract's exact commit before
handing behavior implementation to either developer.
