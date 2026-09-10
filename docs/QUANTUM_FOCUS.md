# Hierarchical quantum spatial focus experiment

This document defines an opt-in computational experiment built on Q-ORACLE-1.
It is not a claim that physical space is an octree or that nature performs this
algorithm.

## Idea

A focus request starts from one finite canonical 3D address region. The region is
represented as a half-open integer box `[x0,x1) × [y0,y1) × [z0,z1)`. Every
non-unit axis is split at its integer midpoint. A cubic region with all extents
greater than one therefore produces eight children; thin regions can produce
four or two. Odd extents produce floor/ceiling halves without gaps or overlap.

The quantum owner evaluates the weights of explicitly supplied event candidates
and one optional no-event outcome. One supplied integer ticket chooses between
no-event and the total event weight. If an event is selected, the same ticket is
narrowed through the region hierarchy. It is never redrawn at a finer level.
The search ends at one canonical cell and then one distinguishable outcome in
that cell is selected.

This preserves the same categorical weights as a flat selection while revealing
only the spatial path needed for the chosen event. The hierarchy changes the
order and granularity of evaluation, not the probability law.

## Model and host cost

One successful `focus_event` call has Q-ORACLE-1 model cost 1 and consumes zero
simulated-world ticks. Recursive spatial refinement and deferred-history
resolution are host computation and are reported separately. No claim is made
that host runtime is O(1).

The focus tree is not stored in physical cells. Regions and focus paths are
transient quantum-sidecar values. Physical cells retain their existing fixed
state and six-neighbor update rule. The focus result is an immutable quantum-side
candidate event; it is not yet committed to Engine state or the native event log.

## Inputs and limits

A focus request contains a bounded integer request ID, world tick, ticket,
no-event weight, one root region and an immutable tuple of candidate outcomes.
Each candidate contains a quantum root, canonical 3D address and outcome ID.
The candidate quantum root must be at the same address and not in the future.
Duplicate outcomes at one cell are rejected; histories that should interfere
must first be combined into one quantum root.

All amplitudes and weights use the existing bounded integer rules. The combined
history evaluation uses the existing `max_eval_nodes` budget. Exhaustion,
overflow, a ticket outside the total weight or zero total weight raises an error;
none is interpreted as no-event.

## Required tests

- An 8×8×8 cube splits into eight equal 4×4×4 children.
- A 5×7×3 region recursively covers all 105 cells exactly once.
- Degenerate non-unit shapes split only their non-unit axes.
- A 1024×1024×1024 cube reaches one cell in ten focus levels.
- Exhaustive integer tickets reproduce exact flat event and no-event weights.
- Candidate input order does not change the selected spatial event.
- Repeating the identical request does not resample.
- Future and address-mismatched roots are rejected.
- Combined host evaluation respects the existing node budget.
- The main simulator state and world tick are unchanged by a focus call.
- Focus, quantum owner and bridge pass the integer static audit.

## Related computational ideas

The spatial subdivision is structurally similar to an octree: 3D regions are
recursively divided into octants. Adaptive mesh refinement also refines only
regions that need more numerical detail. Those methods motivate the data
structure and refinement strategy only. They do not supply the quantum event law.

Quantum coarse-graining and coarse-grained measurements provide another useful
analogy: a question can first distinguish broad outcome classes and later resolve
finer distinctions. The present experiment preserves one global ticket so that
refinement itself never adds an independent measurement or random choice.
