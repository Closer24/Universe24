# Shared agent workflow

These skills implement the project roles requested in issue #16. They are
repository instructions, not a background service or a grant of permissions.
Read [AGENTS.md](../AGENTS.md) from the current checkout first. Explicit user
instructions take precedence; the postulates, definitions and feature procedure
remain the authoritative physical contracts. Skills route work without copying
or weakening those contracts.

## Repository knowledge and restart

Use [monorepo ownership](../docs/ARCHITECTURE.md#monorepo-ownership) and the
[restart guide](../docs/PROJECT_STATUS.md) to recover context without chat history.
Read only affected contracts and Skills after the root entry point. Use one
authoritative definition per concept; Skills link to laws rather than copy them.

Keep model rules, hypotheses to test and verified results distinct. A hypothesis
needs a test and pass condition; a verified result needs an identified tree and
completed evidence. A high-level target or a passing detector is not proof that
the underlying physical law works.

Keep durable procedures in Skills and architectural decisions in their responsible
documents. Put temporary task state, assignments, blocked checks and next actions
in Issues/PRs. For permitted publishing, persist the handoff there rather than only
in chat. If publishing is unavailable or unauthorized, report the unsaved handoff.
Do not claim personal Skills were installed merely because repository files exist.

## Inputs and handoff

Give each owner a bounded task with the repository, base commit, candidate/model,
acceptance target and owned files. Include relevant earlier findings and the
current user's constraints. Use isolated branches/worktrees for concurrent edits;
one owner writes each shared interface until the coordinator reconciles changes.

Return a concise handoff with:

- status: pass, blocked or incomplete; distinguish code checks from physical acceptance;
- reviewed commit/tree, changed files, and any dependent branch;
- result and evidence: commands with outcomes, not-run checks, and relevant HTML/trace;
- violated or satisfied contract, remaining limitation, and next owner/action.

Do not reuse a pass after its relevant inputs change without assessing the diff.
An unchanged tree can reuse its verified results; record that equality. Different
conversations do not synchronize automatically. Read current GitHub state before
integrating their work, and never overwrite unrelated edits.

## Checks proportional to the change

For a physics-engine behavior change, completion requires physics-rule validation,
necessary tests, an affected simulator run, and regression comparison. Architecture
reviews interface/schema changes; visualization reviews changed output. Reuse the
same run as evidence for several checks when its inputs and assertions match.

Use independent numerical/behavioral expectations and retain boundary cases that
exercise distinct risks. Consolidate identical worlds rather than multiplying
tests. Do not remove a failing requirement, change a frozen source, or turn failure
into an expected pass to achieve a green gate. A candidate's passing tests do not
repair another model's failure or establish a real-world law.

Pure documentation/skill changes need skill/link/language and packaging validation,
not newly invented physical tests. The repository's existing submission and CI
gate still applies. Every world actually executed uses the existing HTML renderer;
diagnostics may reject a run but may not repair physical state.

## Tools and authority

Use the available local Git/Python tools and discover the connected GitHub tools
when needed. Read access does not imply merge authority. Use existing user
authorization for edits, publishing and merges; do not ask again for an already
authorized action. A skill never supplies otherwise missing authorization or
permits bypassing an access control or failed gate. Do not send messages to people
unless the user authorized that communication.

The PR owner records the tested head, current base and relevant results. The
coordinator is the final merge owner for a coordinated task. Skills do not claim
that GitHub enforces a branch protection rule unless it was actually verified.
