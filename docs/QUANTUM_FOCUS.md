# Hierarchical quantum spatial focus experiment

This document defines an opt-in computational experiment built on Past is Present Calc (Q-ORACLE-1).
It is not a claim that physical space is an octree or that nature performs this
algorithm.

## Idea

A focus set starts from one finite canonical 3D address region. The region is
represented as a half-open integer box `[x0,x1) × [y0,y1) × [z0,z1)`. Every
non-unit axis is split at its integer midpoint. A cubic region with all extents
greater than one therefore produces eight children; thin regions can produce
four or two. Odd extents produce floor/ceiling halves without gaps or overlap.

The quantum owner holds a bounded candidate set and one optional no-event weight.
A physical-side request contains only four bounded integers: request ID, focus-set
ID, world tick and one ticket. The ticket chooses between no-event and the total
event weight. If an event is selected, the same ticket is narrowed through the
region hierarchy. It is never redrawn at a finer level. The search ends at one
canonical cell and then one distinguishable outcome in that cell is selected.

This preserves the same categorical weights as a flat selection while revealing
only the spatial path needed for the chosen event. The hierarchy changes the
order and granularity of evaluation, not the probability law.

## Model and host cost

One successful `focus_event` call has Past is Present Calc (Q-ORACLE-1) model cost 1 and consumes zero
simulated-world ticks. Recursive spatial refinement and deferred-history
resolution are host computation and are reported separately. No claim is made
that host runtime is O(1).

The focus tree is not stored in physical cells. Candidate sets are quantum-owned
configuration with explicit `max_focus_sets` and `max_focus_candidates` budgets.
The refinement path is retained only as the last host diagnostic trace; it is not
part of the physical-side oracle reply. Physical cells retain their existing
fixed state and six-neighbor update rule. The reply is fixed-size, and its event
is a fixed-size immutable candidate record. It is not yet committed to Engine
state or the native event log.

## Inputs and limits

Binding a focus set is a quantum-side configuration operation, not a per-cell
physical query. Each candidate contains a quantum root, canonical 3D address and
outcome ID. The candidate root must be at the same address. Duplicate outcomes at
one cell are rejected; histories that should interfere must first be combined
into one quantum root.

A focus request cannot read a candidate root from the future. One request ID
represents one decision: repeating the identical request returns the same result
without reevaluation, while trying to reuse that ID with a different ticket,
time or focus set is rejected.

All amplitudes and weights use the existing bounded integer rules. The combined
history evaluation uses `max_eval_nodes`. Candidate and set storage have their
own explicit budgets. Exhaustion, overflow, a ticket outside the total weight or
zero total weight raises an error; none is interpreted as no-event.

## Required tests

- An 8×8×8 cube splits into eight equal 4×4×4 children.
- A 5×7×3 region recursively covers all 105 cells exactly once.
- Degenerate non-unit shapes split only their non-unit axes.
- A 1024×1024×1024 cube reaches one cell in ten focus levels.
- Exhaustive integer tickets reproduce exact flat event and no-event weights.
- Candidate binding order does not change the selected spatial event.
- One request ID cannot resample or be rewritten.
- Physical-side request and reply records remain fixed-size.
- Future and address-mismatched roots are rejected.
- Combined host evaluation and focus storage respect explicit budgets.
- The main simulator state and world tick are unchanged by a focus call.
- Focus, quantum owner and bridge pass the integer static audit.

## Related computational ideas

The spatial subdivision is structurally similar to an octree: 3D regions are
recursively divided into octants. Adaptive mesh refinement also refines only
regions that need more numerical detail. Those methods motivate the data
structure and refinement strategy only. They do not supply the quantum event law.

Quantum coarse-graining and hierarchical generalized-measurement constructions
provide another useful analogy: a question can distinguish broad outcome classes
before finer ones. The present experiment preserves one global ticket so that
refinement itself never adds an independent measurement or random choice.
