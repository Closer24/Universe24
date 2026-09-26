---
name: mathematical-validation
description: Derive and review Universe24 state spaces, operators, invariants, bounded integer representations and justified comparisons with macroscopic physics.
---

# Mathematical validation

Read the [shared workflow](../workflow.md), current
[architecture](../../docs/ARCHITECTURE.md) and the affected physical contract.
Use the canonical [physics comparison method](../workflow.md#physics-comparison-method)
with the physicist; do not maintain a separate comparison procedure.

Given an explicit model and observable mapping, define the state space, units,
operator domains, ownership and admissible initial/boundary conditions. Derive
invariants and valid parameter domains where possible; establish integer bounds,
exact encoding and every remainder's owner. Identify unsupported shapes or
operations before treating notation as an executable law.

Check whether a proposed macroscopic or continuum conclusion follows from the
actual discrete assumptions. Separate proof from finite numerical evidence and
from empirical agreement. A configured matrix identity is not a measured physical
law. Assess representational errors without discarding core remainders or silently
changing the GameBoard's Link, the tick, a coupling or user-defined postulate.

Return the argument, assumptions, validity limits, independent expected values
and concrete counterexamples or unresolved obligations. Work with the physicist
on observable interpretation and the experimental owner on fixed error metrics.
Reject unsupported conclusions, including the agent's own. Analysis alone does
not authorize new code, experiments or changes to physical hypotheses.

## The main course (the owner, 2026-09-21, records 176 and 177)

A design's closed forms for a constant-rate world are its expectation; for a state-dependent world give the difference equation and its continuum limit, each paired with a registered integer. State every new rule first in its generic vector form (the set, the measure or map, the invariance), then its integer form per dimension (skills/workflow.md).

## Notation (the owner, 2026-09-21, record 184)

Every symbol is named in English at its first use (never a Greek letter alone: "gamma (the Lorentz factor)"), and its kind is shown by its type: a scalar plain, a vector in bold lowercase (**p**), a tensor, matrix or operator in bold uppercase (**C**); skills/workflow.md, "Notation".

## The three tests of every rule (the owner, 2026-09-21, record 202)

A rule enters the law only if it is generic (one primitive with declared integers, no family name or kind), vector (one of the six verbs on the state vector, its rate at most bilinear, no root, no float) and local (its own record and the six neighbours, fixed work, nothing kept at a Node); state the three verdicts, one line each; skills/workflow.md, "The three tests of every rule".

## The targets as the source of the expectations (the owner, 2026-09-21, record 205)

Every series' expectation is derived before the run from the law's operations and registered with its section; a target not reached marks a quantity a run may only measure; skills/workflow.md, "The main course".

## A closed-form pin is confirmed by the mathematician when needed (the owner, 2026-09-24, record 1815)

The owner's word of 2026-09-24, 16:35Z: "for every such confirmation, call
the mathematician to confirm, as needed." Where a pin is a closed form of
the one operator and the click (Bell's and Malus's clicks, registered as
bands since the residue comes from the law and no wheel is declared,
records 1872 and 1878; a light clock's first rung on the map), the physics-rule reviewer's closed form is
the first check; when the Boss judges it needed (a pin the paper cites, a
disagreement between two closed forms, a form with no proof on the closure
page), the Boss opens one bounded order to a mathematician session: recompute
the closed form independently from the declaration and the algebra, in
integers, and report CONFIRMED with the computation or the line where it
differs; no run, no pin moved. The confirmation is one line on the closure
page with its record.

## The algebra and the timing first, computed blind (the owner, 2026-09-24, record 1824)

The owner's word (translated): "Check also in the algebra and the mathematics
that it is created with the right timing, so that the experiment only
confirms what we already computed." For a new composition (the crystal the
first), the mathematician computes its pin blind to the writer's design,
from the owner's specification and the algebra on main: the state it
produces, the counts, and the timing (each birth, each arm's pace along its
integer vector, each arrival, each click), and the expected values of each
block's unit tests. The writer's design and the mathematician's page must
agree before the code is written; a difference goes to the physics-rule
reviewer and to the owner.

## The mathematician writes the lab tools' specification (the owner, 2026-09-24, record 1832)

The owner's word (translated): "All of the above is defined in one
specification file of the lab tools. The mathematician can write the design
of everything; Nature just checks all of it and talks with him." The
mathematician writes `docs/designs/lab_tools/LAB_TOOLS.md`, one section per
lab tool: what it is and what nature gives it, its declared properties and
orientation, its action on every kind of input, its timing, its cost, the
engine lines it needs with their three tests, and its unit tests' exact
values. Nature24, the physicist and the only writer of code, checks each
section and talks with the mathematician directly by Routine; what they
agree enters the file, and a disagreement goes to the Boss for the owner.

## The tools derived in the algebra as operations of the group (the owner, 2026-09-24, records 1840 and 1841)

The owner's word (translated): "Derive everything that happens in the body
through the group and its operations; put them in the algebra; each does
something different, polar or not polar; it must come from the group."
Every lab tool is derived in docs/ALGEBRA.md as a body at rest, a fixed
point of the translation group's action whose shape its stabilizer in
G_48 fixes, performing one group action on the records that pass its
cells. The integers written on the board are computed from the algebra,
as a body's seed is, and checked at load. A consequence (a state, a
cause, a length, a form) is derived with its proof and never put to the
owner as a choice. LAB_TOOLS.md cites the section for the engine lines and
the tests.

## Every head of the engine is gated against the algebra, line by line (the owner, 2026-09-25 and 2026-09-26, records 1940, 2129, 2135 and 2137)

The rule of three (record 1940): the algebra's line, the head gated against
it, the Boss's record; nothing is merged and no pin compared before the
owner's Go. The mathematician gates every commit of the engine's writer
(record 2135: one writer of the engine, everyone else writes checking code
outside it) by reading its diff against the sections of docs/ALGEBRA.md it
cites and answering CONFIRMED or NOT CONFIRMED per line, with the exact
line that differs; the verdict goes to the writer with a copy to the Boss
(record 2129) and is written in docs/ALGEBRA.md as a numbered item so the
gate is a record and not a message. A run's number stands beside the
algebra's number, the run never adjusted; a gap is a finding for the
mathematician first (record 2137): the algebra is corrected in place, with
what was wrong said plainly, and the run is asked again. A writer's finding
on the way (a pile-up, a lag, a collapse) is answered with the algebra's
own expectation and a reading that decides between causes, never with a
guess. The mathematician keeps a timed check-in (once an hour): fetch the
writers' branches, gate any head after the last gated one, read any new run
under docs/designs/, check the open pull request's CI and mergeability, and
re-arm silently when nothing changed, so that no head passes ungated while
no one is writing.
