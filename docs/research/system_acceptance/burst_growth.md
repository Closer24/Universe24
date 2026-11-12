# Recurrent activity and structural growth

The final bounded search reuses the existing three-channel native selection
law. It does not add a new tensor, reset memory, change the structural score,
or concatenate a positive recurrence control with an Einstein construction.
The same fixed-six Engine and canonical transition decoder execute its saved
runs.

## Fixed construction and population

The channels are retained memory, transported carrier and local carrier. Each
has its complete old/current/carry triple. There are three channels, nine
integers per node and 27 actual nodes. The tensor fingerprint is
`e198bd03db97d7bf55396c6db07c4926d6a161783f399caaccd48ebbbc2858da`.

The local reversible Boolean collision is the existing `SORT_GATE`. The first
carrier then streams one positive x edge. Its prepared first-order domain is
`a=F^-1(b)`. Every retained remainder is present, with all six classes represented.
The fixed tensor implements `u=3(F(b)+F^-1(b))`; Rule3 therefore follows `F`
exactly on this prepared domain without clipping or information loss.

The search enumerates all 512 Boolean current configurations of a three-site
periodic x ring, repeated over the nine y/z lines of the cube. This includes
all 64 ready-memory configurations and all 448 other memory configurations.
The tensor is unchanged across the entire population. Independent explicit
Boolean algebra and periodic indexing supply the transition oracle, rather
than calling the polynomial compiler or its first-order helper.

Each of the 512 actual Engine transitions is compared in every retained
register, with inverse, particle-count and canonical memory-event checks.
That is 124,416 complete-register comparisons. The legacy structural score
and strict-peak episode definition are retained. Each preparation is assessed
both in the original 24-update window and over `max(24,4*period)` updates.
Four complete cycles expose recurrent scores rather than accumulating an
activity counter and calling it complexity.

## Executed results

| Population and window | Growth passes | Growth failures with enough episodes | Insufficient episodes |
| --- | ---: | ---: | ---: |
| All 512, original 24 updates | 0 | 24 | 488 |
| All 512, complete-cycle window | 0 | 72 | 440 |
| Ready-memory 64, original 24 updates | 0 | 0 | 64 |
| Ready-memory 64, complete-cycle window | 0 | 3 | 61 |

The preselected single-pulse preparation has period five. Its complete state
returns at updates 5, 10, 15 and 20. Its memory-event activity is nonzero and
recurs, but the activity plateaus do not satisfy the unchanged strict-peak
criterion. This control stays `blocked`; its definition is not weakened to
manufacture a success.

There are 72 preparations with at least four actual canonical memory-event
peaks in their complete-cycle windows. The lowest numeric qualifying code,
77, is saved as an explanatory witness from the exhaustive population. It is
not a new held-out prediction or a replacement for the preselected control.
Its period is six, its episode updates are 4, 10, 16 and 22, and its structural
scores at those episodes are 0, 0, 0 and 0. Thus recurrent peaks pass as a
mechanical result, while increasing structure fails on that same law and run.
Both saved experiments pass ordinary runtime verification and complete rewind.

Changing only an old memory register while preserving the current values
breaks the declared prepared-domain condition. The audit rejects that handoff.
The altered state still evolves reversibly, illustrating why invertibility
alone cannot certify the specific dynamical interpretation.

## Exact recurrence boundary

The 512-state ring map is a permutation with 90 cycles. Its cycle-length
histogram is:

| Period | Number of cycles |
| ---: | ---: |
| 1 | 35 |
| 3 | 3 |
| 4 | 6 |
| 5 | 3 |
| 6 | 6 |
| 7 | 12 |
| 8 | 6 |
| 9 | 10 |
| 13 | 3 |
| 15 | 1 |
| 17 | 3 |
| 27 | 1 |
| 39 | 1 |

Every cycle closes without a transient basin. In the prepared Boolean sector,
old history is uniquely determined by current state and each carry remains
constant. Return of a ring's current state therefore returns its complete
retained state. The tensor has no y/z dependencies, so the full three-cube is
a product of nine independent rings. Its complete-state period divides the
least common multiple of these periods, 1,670,760. This is an exact finite-map
argument, not a claim that a 1,670,760-update simulation was performed.

Any structural observable that is a fixed function of the complete state
must recur too. Indefinite strictly increasing structure is consequently
impossible in this finite Boolean sector. The exhaustive finite-window search
covers the replicated-ring preparations, not all nonuniform combinations of
nine rings. Transient growth in other Boolean preparations is not excluded.
Neither statement rules out sustained growth on another law with unbounded
integer states, increasing effective capacity or an explicitly modeled source.

## Integration decision

Include the existing selector as an exact recurrence, retained-feedback and
negative-growth control. Exclude it as evidence for physical cosmological
bursts or an indefinitely growing universe. Its three channels have no joined
Einstein matter/metric source interpretation. No successful physical gate may
be borrowed from the separate six-channel cosmological candidates.

The next construction would need a same-law source of renewed usable memory
or structure, explicit accounting of its state and energy/momentum, a declared
physical burst observable, and a growth criterion that rejects mere recurrence
and integer magnitude. A reset, external reseeding or cumulative click counter
would not supply those missing ingredients.

## Reproduction

```sh
python -m validation.system_acceptance.burst_growth --out runs/burst-growth-fresh
python -m unittest universe24.tests.test_system_burst_growth -v
```

Use a fresh output directory. The report records all 512 results, exact source
hashes, representative and recurrence-witness identities, retained bit cost,
and the passed, failed, blocked and untested acceptance gates separately.
