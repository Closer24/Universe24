# Arithmetic click classes and an explicitly defined body boundary

Status: exact Rule3 identities, explicit counterexamples and a passive reading
of an existing finite recorded trace. No new forward trajectory is generated
here. No click class acts back on the board.

## Exact classification

For one channel write its old triple as `(a,b,r)` and its actual six-neighbor
signed input as u. The sole update is

```text
ell, r_next = divmod(2*u+r,6)
a_next = b
b_next = ell-a.
```

The existing passive classifier emits an event only if `ell != 0` AND the
complete triple changes. Its class is

```text
k = ((r_next-r)//2) mod 3 = u mod 3.
```

This follows directly from `r_next-r=2*u-6*ell`. Remainder parity is unchanged,
so the division by two is exact even for negative differences. Class0,1,2
exhaust the possible arithmetic residues; none changes the update rule.

| Class | Additional arithmetic condition, after the event guard |
| --- | --- |
| C0 | `r_next=r` and `u=3*ell` |
| C1 | `u=1 mod 3`; remainder changes by +2 or -4 |
| C2 | `u=2 mod 3`; remainder changes by +4 or -2 |

For C0 an unchanged triple occurs exactly when `a=b` and `ell=2*a`; the
existing guard then emits no event. Thus even a nonzero quotient and input
multiple of three do not automatically produce C0. If `|u|<=2`, C0 is
impossible: its input would have to be zero, and valid r then gives ell0.

Concrete arithmetic examples, each with a resting old target `(0,0,r)`:

| Old r | Actual u | ell | New target | Class |
| --- | --- | --- | --- | --- |
| 2 | 3 | 1 | `(0,1,2)` | C0 |
| 4 | 1 | 1 | `(0,1,0)` | C1 |
| 0 | -1 | -1 | `(0,-1,4)` | C2 |
| 2 | 1 | 0 | `(0,0,4)` | None |
| 2 | -1 | 0 | `(0,0,0)` | None |

These are input-contract examples, not permission to inject u during a run.
Every physical realization must obtain u from the six actual old neighbors.
The last two rows also show why a remainder change alone is not a guarded C.

## C0 does not algebraically select one route

There is an exact whole-board one-update counterexample. On an otherwise
background `(0,0,2)` board, prepare one source channel at `(0,3,2)` under +++
coupling. Each of its six distinct spatial recipient addresses receives u3.
Every recipient becomes `(0,1,2)` and emits C0 at the same update. The source
itself rotates with zero quotient. No runtime modification is involved.

Thus a C0 can accompany simultaneous six-way local spreading; its label does
not imply exclusive output. A particular engineered interaction may later use
C0 as a reliable marker of routing, but that implication requires controls
and an independently defined output predicate. It is not part of Rule3.

A single address has at most one C class per update. Different addresses can
emit different classes during the same board update. Mere co-occurrence does
not show causation or approval. A routing claim must specify which prior
state supplied the approving influence, its propagation delay, the output
alternatives and the matched absent/changed-approval outcomes.

## What 'spontaneous' can mean here

All zero counters on the complete board imply u0, ell0 and an unchanged state
for every valid initial remainder field. This stationary preparation cannot
spontaneously generate any C class.

A prepared clock cluster can produce events without an incoming external
packet because its constituent counters already interact. Such events are
internally generated relative to a declared source-absent control. That
interpretation applies only to the specified preparation and source masks;
it is not an intrinsic distinction separating C1/C2 from C0. All three
classes are arithmetic consequences of local old states.

The isolated shielded four-cycle has ell0 everywhere and no C, even though
its counter pointers and halo remainders change. Accordingly, moving clock
hands do not by themselves imply spontaneous clicks.

## Declare inner boundary and outer halo separately

Let B be the fixed, preregistered set of body-core sites. Define:

- Inner boundary: sites in B with at least one face neighbor outside B.
- Outer halo: sites outside B adjacent to at least one site in B.

Inspect every channel at these sites and preserve all three C classes. For
a two-site body the inner boundary can include both active clock sites;
the outer halo is a different set of channels. Calling both sets 'skin'
without specifying which one can reverse the apparent conclusion.

If every outer-halo counter is zero at every retained state in an interval,
then `ell=b_next+a_old=0` there for each intervening update. Therefore that
halo has **no guarded C**, even if its remainders change. This is an exact
finite-interval implication. Do not infer a halo click from counter activity
inside B or from a changed halo remainder alone.

## Existing recorded example, not a new simulation

The existing file `research/building_blocks/structure_results_v2.json` contains
side31, +++, canonical counter pair `(1,1)` examples. A passive reclassification
of its `target_trace` through42 updates gives:

| Prepared motif | Full-state return reported by old study | Guarded events at recorded core channels0/14 |
| --- | --- | --- |
| One site | 4 | 0 |
| Two adjacent identical sites | 5 | 64 total: 32 C1,32 C2,0 C0 |

For the adjacent pair, events occur at cycle offsets3 and5, on both sites and
both paired channels. The old artifact reports that its halo counters remain
zero, so its outer halo meets the no-C implication above. This supports a
finite example of internally clicking core clocks with a nonclicking retained
halo. It neither establishes spontaneous activity from vacuum nor a routing
function for a third class. These values are a read-only interpretation of
stored traces; they are not a fresh independent full-board replay.

For new studies, register B and both boundary masks before capture, retain
actual six-term inputs and the complete full-state inverse, and compare
packet-absent with packet-present trajectories. Test source dependence,
class occurrence and routing behavior as separate predicates. Keep failed
predicates and every other event visible in the Presenter.
