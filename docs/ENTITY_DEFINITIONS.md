# Reusable entity definitions

The model owner clarified on 2026-09-19, translated from Hebrew: "The detector
settings are in an entity definitions file, not in the engine; make sure the
workflow is in the appropriate skill." This is an authoring/loading contract,
not a new physical model. It supersedes the earlier assumption that inline world
data alone completed that request. The engine continues to receive the immutable
ordinary measured events and detectors specified by [the Beam Law](BEAM_LAW.md)
and [the engine](ENGINE.md). An external definition file is outside the
engine; the instantiated detector is physically on the GameBoard.

This document owns the definitions layer: how a reusable entity is
authored in a file and placed by a world. What the entities are, every
entity physics knows as one row of the law's keys with the world that
places it, and the honest list of what the law cannot yet place, is
[the catalog of the entities](ENTITY_CATALOG.md) (the model owner's
decision of 2026-09-20, Highlights 5.4).

## Ownership and supported composition

`event_universe.world_loading` is the single host owner of strict document
resolution, entity placement and portable input assembly. It uses
`json_documents.parse_json_document` for every JSON document, then
`events.world.parse_nature_beam_world` for the fully expanded world. That engine parser
remains the one owner of physical schema and domain validation. Physical modules
never open entity files, consult a catalog, branch on an entity name or retain
instance definitions as evolving memory. The loader executes no Python,
expressions, formulas, callbacks or network requests.

An ordinary inline world remains supported with identical loading and original
input bytes. New detector examples keep reusable apparatus definitions in a
separate file. Existing generic rule names select the already specified local
laws; family names, geometry, material parameters, directions, coverage and
thresholds are configuration data. Translation does not prove connectivity or
create a signal. Placement outside the GameBoard is invalid even on a periodic axis:
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

The shown fragment is added to a complete world declaring its law (`"law":
"beam"`), model identity, families, shape, timing and topology. Both added
keys must occur together. `entities` is a nonempty array. Each instance has exactly `name`,
`definition`, `position`; names are nonempty strings and instance names are
unique. Definition references must exist. Position is an exact three-integer
origin on the GameBoard; booleans are refused. The world may omit `measured` and
`detectors` when supplied entirely by instances; explicit inline arrays remain
supported and precede instance content. `in_transit` remains world preparation
data, with its ordinary `number` convention (the measured event whose
continuation a ray is); placement generates no ray and renumbers nothing.

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
`detectors`; names are nonempty and unique. Its measured entries use the world's
measured schema of [the Beam Law](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
(`MEASURED_KEYS`: `position`, `family`, `amount`, `phase`, `momentum`, `fixed`,
`directions`, `table`, `lamp`), including explicit `table` entries and a `lamp`
when applicable; a declared `momentum` is in label units, the momentum label of
a ray being content x amount x u_d with u_d the unit vector of its direction at
the scale Q = 64 (`nature_beam.unit_label`, exactly Q e_d on a heading). The
charge is a family key, the charge per unit of content: a definition's measured
entry names its family and carries the family's charge with its content; it
declares no charge of its own. `position` is relative to the instance origin.
Detector entries use the world's detector schema (`DETECTOR_KEYS`: `name`,
`positions`, `threshold`, `reading`): a detector is a set of Nodes with ONE
record (`DetectorSet` at run time; a click says "here, in one of these" and not
which), its `positions` the Nodes of its measured events, relative, its
`threshold` on the amount arriving over the whole set in one interval and its
`reading` `wave` (the default: the record the square of the coherent pointer
over the set) or `beam` (the rays paired by opposite phase over the set, the
record the plain count). The keys of the deleted reversible detector
(`groups`, `output`, `port_map`, `capacity`, `reference_phase`) are refused by
name, and a detector may not take a face detector's name (`face:+x` and the
five others). All relative coordinates are exact integer triples in
-4095..4095. Every detector position in the definition must refer to its own
declared measured geometry. Family names refer to the world's explicit family
declarations; no familiar physical names are built in. Which keys of this
schema place a given thing (a lamp, a laser, a mirror, a wall, a slit, a
screen, a clock, a probe, a star, a planet, a neutron star) is one row of
[the catalog of the entities](ENTITY_CATALOG.md#the-external-things): a
definition carries the row's measured entries and detectors, and the world
that places it declares the row's families and world keys. The catalog's
own worlds (`examples/events/catalog/`) are plain inline worlds; a
definition of any placeable row is authored the same way.

Host structural validation covers every definition, including unused ones.
Physical semantic validation applies when a definition is instantiated into its
world context: an unused definition is not certified for arbitrary `N`, families
or tables. Unsupported fields, executable extensions and duplicate relative
measured positions are refused. The host accepts the world parser's measured,
lamp, table-entry and detector keys (`MEASURED_KEYS`, `LAMP_KEYS`,
`TABLE_ENTRY_KEYS`, `DETECTOR_KEYS`); the world parser supplies their actual
domain, required-field and rule-combination checks.

Expansion order is inline measured entries, then instances in declaration order,
then each definition's measured declaration order. This fixes the ordinary
measured numbers 1, 2, ... without using labels to choose a rule. Detector order
is similarly inline then instance declaration order. A placed detector name is
`/INSTANCE/LOCAL`, with each component escaped as JSON Pointer text (`~` becomes
`~0`, then `/` becomes `~1`). Thus
renaming an instance changes labels only, and names containing `/`, `~`, schema
keywords or `__proto__` remain ordinary data. Collision with an inline name is
an error, not a rename. No field is silently overridden.

For every relative coordinate, add the instance origin once, reject an out-of-
GameBoard result and pass the result to the canonical world parser. Overlapping
instances, a Node in two detectors, a detector position without a measured
event, integer bounds, unknown families and unsupported table entries fail
before a Simulation or output directory is created. The world parser's bounds
remain binding.

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
    world: NatureBeamWorld
    portable_source: bytes
    expanded_source: bytes
    dependencies: tuple[DefinitionSource, ...]

load_world(source: str | bytes, *, base_dir: Path | None = None) -> LoadedWorld
```

`expanded_source` is deterministic JSON for the plain engine world after removing
the two authoring keys and adding the placed arrays. Serialize generated JSON as
UTF-8 with sorted object keys, compact separators, `ensure_ascii=False`, and one
terminal newline; array order is unchanged. Preserve previously accepted escaped
unpaired surrogate code points as JSON Unicode escapes when encoding generated
UTF-8; do not reject their original valid escaped input or change its meaning.
For a plain world, `portable_source`
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
`execute_nature_beam_run` (until 2026-09-19 `execute_event_run`) gains the optional keyword-only
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
| Definition positions `(0,0,0)`, `(1,0,0)`, `(2,0,0)` placed at `(3,4,0)` on a 9-by-9-by-1 GameBoard | Physical positions `(3,4,0)`, `(4,4,0)`, `(5,4,0)`; relative output `(2,0,0)` becomes `(5,4,0)` |
| A second placement at `(3,6,0)`, no inline material | Six measured Events numbered 1..6 in the stated order; two separate detector labels and original thresholds |
| Rename instance `alice` to `a/b~c` | Same physical payload/routing, detector prefix changes from `/alice/` to `/a~1b~0c/` |
| Separate files, their portable bundle, and the bundle copied to another directory | Equal NatureBeamWorld and expanded SHA-256; same raw definitions SHA-256; no dependency read for a bundle |
| File edited after a template was prepared | Already prepared bundle/export/Start retains its earlier state; a newly loaded template reflects the new bytes |
| Missing context/file/name, duplicate keys/names, unexpected dependency, traversal/symlink escape, overlaps or translated coordinate 9 on extent 9 | Concrete refusal before run/output creation; no clipping, fallback or silent redefinition |
| Plain legacy world | Same parsed world, original portable bytes, no dependency metadata/artifacts |

Tests isolate resolution, placement, strict failures, provenance and relocation;
use minimal generic states with independent expectations. A prepared example run
is dated evidence, not a test that pins example outputs. The loader must also
preserve the periodic extent-one detector case: replacing inline data with an
entity reference cannot alter its local law or introduce a second ray.

The schema/authoring developer owns `world_loading.py`, the preflight adapter,
resolver tests, canonical definitions, example conversion and packaging/data-
dependency selection. The runner/workspace developer owns `runner.py`, the
metadata-only addition to `events/run.py`, `ui.py` and focused consumer tests.
The physical engine and topology provider need no entity-specific changes.
Architecture owns this contract and the skill/documentation links. The independent
test owner reviews and verifies file/bundle equivalence and portability after
both provider and consumer commits. Publish this contract's exact commit before
handing behavior implementation to either developer.

## Proposed, not built: one canonical definition per family (2026-09-20)

The model owner, 2026-09-20 ([record 103](LOG_2026-09-20.md#103-the-owners-next-two-the-transmission-experiment-after-the-landing-and-every-known-family-as-an-entity-with-its-defining-keys)):
"make sure all the known families are in entities with what is needed to
define them." The architect's audit of the same day ([the catalog's
family-name table](ENTITY_CATALOG.md#the-family-names-of-the-register);
the cleanup plan, section 7): a definition of `event-entities-v1` carries
`measured` and `detectors` only, so no family is defined in a definitions
file today; the 158 registered worlds declare their families inline,
written by their series' `make_worlds.py`, and a family used by two series
is two literals (`light` in four spellings, `p` in six charges, seven names
for the inert paid material). This section is the proposal for the owner's
decision; nothing of it is built.

**The change.** A definitions document gains an optional `families` list
per definition, the world's family schema verbatim (`FAMILY_KEYS`: `name`,
`quantum`, `charge`, `columns`, `lifetime`, `phase`, `phase_per_link`):

```json
{
  "format": "event-entities-v2",
  "entities": [
    {
      "name": "photon",
      "families": [{"name": "light", "quantum": 1}],
      "measured": [],
      "detectors": []
    }
  ]
}
```

A world that places an instance of the definition gets its families
merged into the expanded world's `families` by name, in the order of the
instances then of the definition; a family the world already declares is
kept when every key agrees and refused when one differs (one owner of a
value, no silent override, as an inline detector name colliding with an
instance's is refused today). A definition of a family alone (an empty
`measured`) is admitted, so that `families.json` can hold the catalog's
rows with no apparatus. The engine's parser is untouched: it receives the
expanded world as it does now. The physics is untouched: a family's keys
are the same keys with the same bounds.

**The cost.** One host module, `world_loading.py` (the format's version,
the `families` key, the merge by name, about 60 lines and their tests in
`tests/test_entity_definitions.py`: a family placed, a family agreeing, a
family differing, a definition of a family alone, the portable bundle
carrying it); one contract section here; one file
`examples/events/entities/families.json` with the catalog's rows in the
atom's units (`light`, `e`, `p`, `n`, `nuclear`, `nu`, `w`, `beta`,
`apparatus`, `mass`, `probe`; the muon and the tau with `become`) and one
`examples/events/entities/apparatus.json` with the external things and
the sources of `amplitude-v1` (the lamp, the laser, the mirror, the wall,
the slit, the screen, the probe, the clock, the pair source, the GHZ
source, the splitter, the label rotation, the gate, the counter pair, the
chooser); the check selector's `RESOURCE_CONSUMERS` gains the two files.

**The migration.** Per series, its `make_worlds.py` writes
`entity_definitions` and `entities` in place of the inline `families` and
the inline apparatus it places, and the shipped worlds are written again;
the loader's contract makes the expanded world byte-identical to the inline
one where the definition equals the literal, so `events.jsonl` and
`state.json` of every registered world stay identical and `run.json`
differs only by `initialization_resolution` (the bundle's provenance),
checked by the gate set replayed with `tools/run_series.py --list
--compare`. The series whose families differ from the catalog's row by a
unit convention (the proton's charge `4` in the nucleus and the weak
series against `[1, 1]` in the atom's; the coupling series' test charges
named `p` and `q`) keep their inline families and say so in their README,
or rename their test charges, the owner's call: a family name is a record
key on every line of `events.jsonl`, so a rename moves the digests. Order:
the loader and its tests first (one pull request, host only), then the two
definition files, then one series per commit with its replay.

**What it does not do.** It does not define the content of a thing (a
measured event's `amount` stays the world's), it does not add a key to the
law, and it does not give a family whose defining key the law lacks (colour,
oscillation, a hand) a definition: those stay on [the gap list](ENTITY_CATALOG.md#the-gap-list).
