# Instructions for every contributor

The project keeps three current documents, the reviewer's ledger, the skills and
the entry files, and nothing else. Start from the current checkout, never from a previous conversation.

| What | Where |
| --- | --- |
| The law: one algebraic line per rule, the families, the bodies, the clicks, every experiment's formula and blind expectation | [docs/ALGEBRA.md](docs/ALGEBRA.md) |
| The engine as the code holds it on `main`: the words, the main loop and Rule3, the folders and the register, the loader and the files, the output, the gates, how to run a world and how to add a feature | [docs/ENGINE.md](docs/ENGINE.md) |
| The decisions in force, one line each; a decision of the model owner replaces the line it changes | [docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md) |
| The reviewer's ledger: every finding of the paper and the law with its state, changed by the pull request that prints it | [docs/REVIEW_LEDGER.md](docs/REVIEW_LEDGER.md) |
| The team's roles, the short procedure and every shared way of working | [skills/workflow.md](skills/workflow.md), [the Boss's card](skills/boss-orchestrator/SKILL.md) and [the advisor's card](skills/advisor/SKILL.md) |
| Every edit, check and Git operation | [CONTRIBUTING.md](CONTRIBUTING.md) |

Keep changes within the user's scope: an explanation or diagnosis does not
authorize implementation, and a skill grants no additional permission.
The active implementation lives only in `src/event_universe/`.

## Canonical simulation terminology

The physical location is a **Node**; its complete local information is its
**NodeState**, the law's own numbers and nothing else. Nodes are connected by
**Links** through directional **Ports**, six per Node; a local change is an
**Event** and configured local logic is a **LocalRule**. The lattice of Nodes is
the **Lattice** (`Lattice` in code, `lattice` in module and function names; the
readings' label `LATTICE`), the paper's word and the code's, one vocabulary (the
owner's word of 2026-10-04). Do not introduce `Site`, GameBoard, board, grid or
any other noun for these; new location identifiers use `node`, `nodes` and
`NodeState`. The words of the engine (Family, Record, Body, NodeReader, Click,
Primitive, Interval) are defined in [docs/ENGINE.md](docs/ENGINE.md#1-the-words).
The nouns detector, instrument,
emitter, absorber, observer and measurer have left the repository (the owner's
word of 2026-10-03): the NodeReader, with Nodes alone or with a record of its
own, is the one declaration kind; do not reintroduce them.

## Repository language: English

All repository comments, docstrings, documentation, contributor instructions,
test descriptions, diagnostic messages and newly written identifiers are in
English, in every directory and by every contributor, including files brought in
from an older branch and external documents of the project. Keep English simple
and precise; mathematical symbols and established technical names are allowed.
Every symbol is named in English at its first use and never stands alone as a
Greek letter ("gamma (the Lorentz factor)"); its kind is shown by its type: a
scalar plain, a vector in bold lowercase (**p**), a matrix or an operator in bold
uppercase (**C**). Names identify a component's actual responsibility; no code
letter or number stands for a thing. Use portable ASCII file names, `snake_case`
Python modules and functions and explicit class names.

Use Hebrew for conversation with the user unless he explicitly requests another
language; a message written in another language alone is not a request to switch.
Before submitting a change, translate any non-English prose it introduces and run
`tests/test_repository_language.py`; reviewers check the language as well. Do not
exempt a directory, disable the gate or encode non-English prose as escapes.

## Change boundaries

- The law is [docs/ALGEBRA.md](docs/ALGEBRA.md); the engine is its implementation
  and nothing else. Every rule passes the three tests (generic, vector, local)
  before it enters; a hypothesis that needs more is stated under its own identity.
- The engine holds no number, no formula, no family name and no flag: every
  physical value comes from the run's files, and every primitive is one folder
  found by its name ([docs/ENGINE.md](docs/ENGINE.md)).
- Physical calculations use bounded integers, fixed local NodeState and the six
  neighbouring Nodes; nothing is kept at a Node beyond the law's own numbers.
- Only a NodeReader's click is a measurement; a lattice reading is a diagnostic
  and is labelled so. Runs and tests are headless.
- A behavior change needs a dedicated test; a physics change needs the law's line
  first and the procedure in [CONTRIBUTING.md](CONTRIBUTING.md).

## Completion

Run `python tools/check.py` before delivery; it selects the changed files and
their consumers, and `--full` is explicit. State the selected checks and the
remaining blockers. Keep provider, consumers, tests and documents together when an
interface changes; a change to a document replaces what it touches and deletes
what no longer holds in the same pull request.
