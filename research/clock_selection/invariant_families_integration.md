# Invariant families within unchanged Rule3: research integration

Status: completed follow-up, 2026-11-08. The [exact algebra](invariant_families_algebra.md)
and four eigenpattern identities have a separate
[independent mathematical review](../invariant_families_v1/independent_math_review.md).
All [48 native family cases](../invariant_families_v1/results.md) and the
[four-mask overlap study](../invariant_families_v1/overlap_results.md) passed
independent replay. Their certificates cover respectively
[912 states and 864 transitions](../invariant_families_v1/evidence/independent_audit.json)
and [52 states and 48 transitions](../invariant_families_v1/evidence/overlap_independent_audit.json),
including every full rewind. The earlier clock-selection package and its
evidence are unchanged. The frozen prospective protocols remain the original
pre-run specifications, not current execution-status reports.

## Decision: retain the elementary rule

Every elementary channel update remains `num=den=1`. No per-channel coefficient
field is selected. The historical [fixed-ratio candidate](fixed_ratio_candidate.md)
is an unselected mathematical alternative, not an implementation roadmap.
The present route is to prepare different collective states of the existing
counters and remainders under one fixed tensor.

This answers a narrower, useful question: different exact reduced responses
can arise without changing a primitive parameter. It does not mean that a
counter chooses its own law or that a global preparation automatically becomes
a localized component.

## What the invariant family means

Let the fixed neighbor operator be `F`, and let `v` be a full-address pattern
with entries in `{-1,0,+1}` satisfying `Fv=lambda*v`. Encode one scalar state
`(a,b,r)` as follows:

| Pattern entry | Complete channel state |
| --- | --- |
| +1 | `(a,b,r)` |
| -1 | `(-a,-b,J(r))`, where `J(r)=4-r+2*(r mod 2)` |
| 0 | `(0,0,r_background)`, with a fixed valid remainder |

The signed remainder is essential. Negating only the two counters is not a
general sign symmetry of Euclidean division. The reviewed identity gives
exact closure for all integer counters, all six remainders and all durations:

```text
ell,r_next = divmod(2*lambda*b+r,6)
a_next = b
b_next = ell-a
```

At zero-pattern entries the total input is zero, but individual donor terms
may cancel. Such an entry is not necessarily an isolated quiet-clock halo.

Under the fixed `+++` tensor the following families are available:

| Prepared pattern | lambda | alpha_eff=lambda/6 | Scope |
| --- | ---: | ---: | --- |
| All addresses equal | 6 | 1 | Global coherent state; scalar counters can drift |
| Channel-uniform x-profile `(1,-1,0)` | 3 | 1/2 | Global periodic sheets; side length divisible by 3 |
| Channel-uniform x-profile `(1,0,-1,0)` | 4 | 2/3 | Global periodic sheets; side length divisible by 4 |
| Spatially uniform `v_g=(R(g)e_y)_y` | 4 | 2/3 | Internal channel pattern: eight positive, eight negative and 32 zero entries |

Here `alpha_eff` labels a reduced collective response. The coefficient of `b`
in the remainder-free comparison recurrence is `lambda/3`, not `lambda/6`.
The elementary denominator is still 6. A generalized scalar `p/q` comparison
can contain additional spectator remainder sectors; validating the six native
remainders alone does not validate every generalized `6q` state. An exact state
encoding also does not define a new effective `p/q` click classifier. All
reported C events use the unchanged native guard and class definition.

For lambda 3 the exact pair update is `(a,b)->(b,b-a)`, giving period 6 for a
nonzero pair. Lambda 6 gives `(a,b)->(b,2b-a)`, which need not oscillate.
Lambda 4 retains its nonlinear remainder dynamics. A linear comparison
frequency `arccos(lambda/6)` must not replace that exact integer trajectory.
In particular, the spatial patterns select finite lattice wave vectors;
their temporal frequency is not automatically a zero-wave-vector mass gap.

The 48-case audit confirms both seeds `(0,1)` and `(2,-1)`, all six base
remainders and 18 updates in each of the four families. Both lambda 4
realizations have identical scalar traces for matched seeds and remainders,
but those traces have first complete returns of 6, 8 or 15 updates, or no
return within 18. Lambda 3 returns after 6; the two uniform lambda 6 seeds
drift. Thus one fixed effective ratio does not imply one native period.
The same ratio can also describe a spatial standing pattern and an internal
channel pattern. Neither matching ratio nor matching temporal trace makes
those preparations physically equivalent or identifies an intrinsic mass.

## Coexistence is not general addition or scattering

An invariant sector survives when initialized exactly in that sector. This
does not establish robustness to perturbations, closure when two sectors
overlap, or formation from simple unrelated preparations. Cutting a periodic
pattern into a finite packet changes its boundary inputs and generally removes
the eigenpattern identity. Such a cut is a new preparation to test, not an
already-proved moving particle.

There is also an important transparent family. The reviewed exact diagonal
integer plane wave has input divisible by 3 at every address and time.
Adding its counters to any other `+++` trajectory while keeping that
trajectory's remainders gives an exact combined solution. Subtracting the known
plane leaves the original trajectory unchanged. The lambda 3 sheet family and
lambda 6 uniform family have the same divisible-input, constant-remainder
property. Their counter addition therefore supplies coexistence without a
residual state change.

This limits the proposed role of such a plane as an activating signal. Raw C
events can change because their quotient and changed-triple guards depend on
the total state, even though the residual counters and remainders do not.
Those changed event guards alone do not demonstrate a written clock memory.
The arithmetic class `u mod 3` is unchanged by a divisible-input addition;
that does not imply identical guarded C events.

When the added planar counters have passed a detector region and are zero
there, that region is exactly its original residual trajectory's state,
including every remainder. This additive mechanism cannot leave a retained
native record there. This limitation applies to the specified transparent
family. It does not apply to all possible signals: the previously audited
guided packets have inputs that are not everywhere divisible by 3 and do
write local clock phases.

Two lambda 4 modes can instead interact through native division. For initial
`a=0,b=v,r=2`, at an address where both patterns equal +1, each singleton has
`u=4`, quotient 1 and next remainder 4. Their jointly prepared counter sum has
`u=8`, quotient 3 and next remainder 0. The counter-additivity defect is +1
after one update. The corresponding shared negative entry gives defect -1.
This is an exact arithmetic interaction, not an attraction, a preferred route
or a detector approval. No signal is added after initialization.

## Completed test: controlled nonlinear overlap

The [four-mask overlap result](../invariant_families_v1/overlap_results.md)
answers the question frozen in the [protocol](invariant_overlap_protocol.json):
the full native engine reproduces the exact predicted interaction of two
otherwise closed lambda 4 families, with their complete controls. The
preparations overlap from the start; this is not a localized meeting or a
long-term coexistence test.

Use the spatial x-period-4 pattern and the internal `R_yy` pattern on a side-4
periodic cube. All four masks start with `a=0,r=2` everywhere and
`b=s_spatial*v_spatial+s_internal*v_internal`. A remainder is assigned once,
not added. The horizon is 12 updates. There are no remainder ghosts in these
source-off controls because all complete initial remainder fields are identical.

The first-step prediction is exact: the b-counter defect
`b11-b10-b01+b00` is +1 at 128 shared positive entries, -1 at 128 shared
negative entries and zero at the other 2,816 addresses. The a-counter defect
is zero. The ordinary integer remainder contrast is minus six times the
b-counter defect. That contrast is a diagnostic across four different
trajectories, not a definition of adding complete remainder states.

Both singletons matched their scalar oracle at every frame. Independent replay
verified all four complete trajectories, actual input sums, raw C events,
inverse transitions, full rewinds and all 13 full defect arrays. The predicted
first-step counts and values passed exactly. Later joint-state contrasts remain
descriptive output; no later event was promoted to an approval or memory
outcome. The [resource receipt](../invariant_families_v1/evidence/overlap_independent_audit_budget.json)
reports 7.626 CPU seconds for the dedicated producer and independent auditor
together, within the 30-second limit; prior static preflight checks are
separately accounted.

This confirms intrinsic nonlinear interaction under unchanged Rule3. The
one-step carry is also an amplitude-threshold effect: a doubled singleton can
give the same local input 8 and quotient 3. The defect therefore does not by
itself establish cooperation preference or complexity selection. This study
did not contain amplitude-matched preference controls and makes no such claim.
No attraction, localized moving family or retained detector record follows.
A subsequent scattering study requires separately validated mobile
preparations and frozen incoming/outgoing identity tests, which these global
eigenpatterns do not yet supply.

## Connection to clocks, clicks and the longer objective

The audited baseline already supplies [local phase mediation](evidence/independent_audit/clock_region_mediation.json)
and a [conditional write/cancel chain](carrier_memory_results.md). The latter
has zero of eight strong terminal records: its joint final receiver equals the
null and probe-only receiver, despite a reproducible bounded pause and restart.
The new exact families do not retroactively remove that limitation.

The next mechanism still needs an internally generated input, a state-dependent
local response, a distinct persistent register, and a later response affected
by that register. Every part must be a native state and transition. A prepared
oscillator, transparent coexistence or a nonlinear carry supplies only part of
that chain. Ordinary C0/C1/C2 readout remains unchanged; no class becomes a
force, approval command or collapse operation by naming it so.

Complexity preference and evolution require additional, separately declared
tests: internal variation, retained distinctions, differential propagation
under one read-only metric, and repeated renewal without external selection.
More modes, a longer period, more C events or larger counters are not that
metric. Natural generation would require recurrence across a preregistered
ensemble of simple initial states; success in an exact manufactured eigenpattern
is a different result. A physical mass interpretation additionally requires
the dispersion, localization, motion and calibrated click relations described
in [the mass-family tests](physics_targets/mass_families.md).

The next decisions have three separate gates. First, a localized preparation
must retain an identifiable full-state pattern under motion and perturbations;
cutting an eigenpattern is an experiment, not preservation of its theorem.
Second, an interacting signal must leave a distinct native register for a
fixed hold after it passes, with null and complete single-source controls.
The known guided-packet phase gates remain candidates for that route; the
transparent planar family does not supply the same mechanism. Third, any
complexity-preference claim requires competing outcomes, a metric fixed before
execution, matched input/amplitude controls and retained evidence for the
unobserved alternatives. None of those three gates is passed merely by the
audited invariant encoding or immediate nonlinear overlap.

The baseline families and their intrinsic overlap can now be used as verified
research ingredients within those limits. No new coefficient field, physical
equivalence or additional runtime action is selected by this result.
