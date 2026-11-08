# Native parallel inputs and division: bounded demonstration

The registered baseline run completed all90 cases in3.0105 CPU seconds and
3.9665 wall seconds. It retained1170 complete states and1080 transitions,
including all remainders, all guarded C events and full inverse checks.
Its complete output initially occupied1,080,413 bytes, below the16MiB budget.
No engine, coupling, rule, observer or Presenter source was changed.

The [protocol](parallel_division_protocol.json) was registered before evolution
with SHA256 `890abeac74ae4bc164b5cec832901230f2ddcc2c763ddb7d189cc9be459d662d`.
The [complete results](evidence/parallel_division_v1/result.json) identify every
case and its losslessly compressed native recording. Initial preparations,
source hashes and exact experiment definitions are retained beside the results.
Producer source verification passed throughout the run. A separate
[independent matrix-based audit](evidence/independent_audit/parallel_division_v1.json)
also passed:1170 full states,1080 forward/inverse transitions,90 complete rewinds,
every first-step state/event prediction, all world C records, Q, causal support
and13 cross-size trajectory comparisons. The audit used1.79 CPU seconds.

## What was checked

For26 cases, one channel starts at `(a,b,r)=(0,A,2)`, with A from−6 through6
on each of sides29 and33. All other channels are `(0,0,2)`. All six actual
recipients receive input A on the first transition. Their quotient, remainder
and C class agree exactly with Euclidean division in every case. Centered full
trajectories agree across both cube sizes for all13 amplitudes.

For64 cases, every subset of the six actual inputs of one center channel is
initialized with b1. All sources are ordinary initial board counters. There
is no later injection. For k selected donors, the center's first transition is:

| k | Quotient | New remainder | Guarded class |
| --- | --- | --- | --- |
| 0 | 0 | 2 | None |
| 1 | 0 | 4 | None |
| 2 | 1 | 0 | C2 |
| 3 | 1 | 2 | C0 |
| 4 | 1 | 4 | C1 |
| 5 | 2 | 0 | C2 |
| 6 | 2 | 2 | C0 |

Every mask matches this predeclared table. All world events are retained,
including events outside the center and after the first transition. The
background-relative algebraic Q is conserved in every recorded state; it is
not identified as physical charge or energy. Every trajectory stays inside
the predeclared causal margin and never touches a periodic boundary. Each
transition and each complete trajectory passes the native full-state inverse.

## The explicit limitation

A single b3 source produces six simultaneous first-step C0 events. Thus
unchanged remainder and classC0 do not establish selection of one route.
Likewise the center class cycles nonmonotonically as the number of unit inputs
increases. It does not order source count or demonstrate preference for a
complexity measure. The demonstration confirms native synchronous arithmetic
and spatial fanout; it establishes neither physical light nor a complexity
selection mechanism. No predicted arithmetic check failed in this finite run.

## View and reproduce

Open [The Presenter](evidence/parallel_division_v1/The_Presenter.html) in a browser.
Its experiment list contains eight examples selected in the protocol before
the run: three signed/small/splitting single donors, the empty six-source
control, and masks3,7,15,63. Rotate the cube, step through the recorded clocks,
and inspect channel values. Display controls are passive and cannot change
the saved trajectories. The complete90-case collection remains in `records/`;
the viewer bundle is a declared subset, not selected favorable evidence.

To register a fresh exact reproduction without evolution:

```sh
python -m research.clock_selection.parallel_division --prepare --output new-division-run
```

After checking that registration, run it once:

```sh
python -m research.clock_selection.parallel_division --run --output new-division-run
```

The runner rejects a repeated or overwritten run and source changes after
registration. This script uses the existing generic assembly and recording
pipeline. Its first-step comparisons and passive event analysis are separate
from evolution.
