# Instructions for every project contributor

These instructions apply to the entire monorepo. Start here from the current
checkout; do not rely on a previous conversation.

## Start a task

1. Read [project status](docs/PROJECT_STATUS.md), then verify the actual checkout,
   current main and relevant open PRs. A status snapshot is not live evidence.
2. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for every edit, validation and Git
   operation. Record the base commit and preserve unrelated local work.
3. Use the [README project map](README.md#project-map) to locate the owner.
   Read the applicable contracts below and only the specialist Skills needed.
4. Keep changes within the user's scope. An explanation or diagnosis does not
   authorize implementation; a Skill does not grant additional permissions.

## Monorepo and one source of truth

[Monorepo ownership](docs/ARCHITECTURE.md#monorepo-ownership) defines boundaries.
The active implementation lives only in `src/event_universe/`.
`src/persistent_source_field.py` is a compatibility facade, not a second engine.
`tests/reference/` is a historical archive, not an active compatibility gate;
never edit it to make a test pass.
Generated artifacts, distributions and backups are outputs or history.
One repository does not require one runtime process or a new package hierarchy.

## Canonical simulation terminology

Use [Canonical simulation terminology](docs/TERMINOLOGY.md) throughout the active
simulator, documentation, tests and diagnostics.

The physical location is a **Node**. Its complete local information is its
**NodeState**. NodeState contains configured Scalars and Vectors plus only the
minimal ownership, Port and timing metadata required for local transport. Input
and output are roles of Scalars/Vectors, not additional physical value types.
Nodes are connected by **Links** through directional **Ports**; local changes are
**Events** and configured local logic is a **LocalRule**.

Do not introduce `Site` or any other alternative noun for an active physical
location. `Site` may appear only as an external standard term or as a clearly
non-physical mathematical/register term whose meaning is distinct from Node.
New active location identifiers use `node`, `nodes` and `NodeState`.

## Read the contract for the affected scope

| Scope | Authoritative source |
| --- | --- |
| Canonical names and state vocabulary | [docs/TERMINOLOGY.md](docs/TERMINOLOGY.md) |
| Any physical behavior or hypothesis | [POSTULATES.md](POSTULATES.md) and [SIMULATOR_DEFINITIONS.md](SIMULATOR_DEFINITIONS.md) |
| Generic initialization, disturbance laws or local delay | [docs/DISTURBANCES.md](docs/DISTURBANCES.md) |
| State, interfaces, dependencies or repository layout | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Any edit, validation, publishing or merge | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Test coverage and numerical expectations | [docs/TEST_EXPECTATIONS.md](docs/TEST_EXPECTATIONS.md) |
| New physical feature | [docs/PHYSICAL_FEATURES.md](docs/PHYSICAL_FEATURES.md) |
| Rendering and run outputs | Display contracts in [SIMULATOR_DEFINITIONS.md](SIMULATOR_DEFINITIONS.md) |
| Agent handoffs and durable knowledge | [skills/workflow.md](skills/workflow.md) |

Follow linked requirements for the affected path. Do not load every Skill for a
small task. Keep each technical rule in its responsible document and link to its
implementation and tests; do not copy it into each agent's instructions.
An unresolved contradiction never authorizes a silent physical-law change.

## Agent skills

Use [Boss orchestration](skills/boss-orchestrator/SKILL.md) for coordinated work,
or a matching specialist directly. Every role follows the
[shared workflow](skills/workflow.md). Skills are repository instructions, not
always-running agents. Use bounded assignments and one writer per shared interface.
Review Boss and affected Skills for useful durable lessons; record either the
authorized update or why none is needed. Keep temporary task state in Issues/PRs.

## Repository language: English

All repository comments, docstrings, documentation, contributor instructions,
test descriptions, diagnostic messages and newly written identifiers must be in
English. This applies to every directory and every contributor, including files
brought in from an older branch. Keep English simple and precise. Mathematical
symbols and established technical names are allowed. This is a documentation and
architecture rule; it does not change physical laws or the language of conversation
with the user. The user's explicit request replaces the previous Hebrew-documentation
preference.

Before submitting a change, translate any non-English prose it introduces and run
`tests/test_repository_language.py`. The script check catches the legacy Hebrew
text and several other non-Latin scripts; it does not prove that Latin-script prose
is English. Reviewers must check the language as well. Do not exempt a directory,
disable the gate, or encode non-English prose as escapes to evade this rule.

Names must identify a component's actual responsibility in simple English.
Use portable ASCII file names, `snake_case` Python modules/functions and explicit
class names. Do not call a historical model "current" or imply that it is the
active default. Keep one canonical copy of each nonempty file and JSON
configuration; consumers must reference it rather than copy it. Empty package
markers are not duplicated implementations. Preserve scoped historical evidence.
The language and repository-hygiene gates check paths, identifiers and exact or
JSON-normalized copies; reviewers still check semantic clarity and overlapping
responsibilities. Keep renames, consumers, migration notes and the
[documentation index](docs/README.md) together.

## Change boundaries

- Apply the [local integer operation contract](docs/ARCHITECTURE.md#local-integer-operation-contract)
  to every physical change, including entity data and prototypes intended for
  the active engine. It defines generic law ownership, integer intermediates,
  causal inputs, formula-free payloads and the current tensor-support limit.
- Enforce LOCALITY-1 in SIMULATOR_DEFINITIONS.md for every physical dependency,
  including self-field estimation and subtraction. Audit the origin of every
  input end-to-end: a local subtraction cannot legalize a global estimator.
  Require fixed local work and storage for fixed K; report total host costs
  separately. Q-ORACLE-1 is confined to the explicit quantum owner and cannot
  supply an exception for ordinary fields, forces, movement or geometry.
- Physical calculations use bounded integers, fixed local NodeState and six
  neighboring Nodes. Measure host computation and storage separately from the
  model's local cost.
- Field, response, movement and transit calculations belong in generic components.
  Models select policies and compose components without copying formulas. The engine
  schedules work and validates contracts.
- The active Simulation requires initialization-defined disturbance types and
  fields. Do not branch on physical field names or reintroduce an implicit scalar
  default. Named historical research APIs retain their own contracts.
- Displays and measurements only read state. Runs and tests are headless unless
  visualization is explicitly requested. Do not capture frames or load render
  dependencies in the ordinary runner path; see the definitions display contract.
- A behavior change needs a dedicated test with inputs, an expected result and an
  edge case. Preserve current physical contract coverage. A new physical
  hypothesis needs an explicit model identity.
- Run `python tools/check.py` before delivery. Inspect metadata/events for runs
  and inspect visual artifacts only when visualization was requested. Static
  checks are partial enforcement, not proof of locality or correct physics.

For physics changes, validation also requires the physics-rule reviewer, necessary
tests, an affected simulator run and regression evidence. Reuse matching runs.
A new hypothesis needs an explicit model identity and independent expectations.
Passing code checks does not establish a real-world physical law.

## Completion

Use `python tools/check.py` before submission. It selects changed files and
affected consumers, rather than running unrelated suites. Inspect its reported
scope; use `--tests` to add a related test whose dependency is not statically
visible. See CONTRIBUTING.md for base selection and non-import dependencies.
Full validation requires explicit `--full`; do not select it routinely.
Ordinary checks are headless; `pytest --visualize-runs` is explicit visual validation.
State the selected checks and remaining blockers.
Keep provider, consumers, tests and documentation together when an interface
changes. Follow the merge conditions in CONTRIBUTING.md; never bypass failed CI.
