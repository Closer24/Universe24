# Waiting/confirmation candidates and a guided mobile packet

The strict waiting/confirmation component has **not** been established. Two
prospectively specified families completed 145 cases and 580 source-control
runs with zero accepted cases. The unchanged scalar rule admits the desired
local response to prescribed inputs, but those inputs were not realized as a
quiet retained record by the tested complete-board preparations.

A separate prepared guided packet passes exact complete-state translation
checks. Its algebraic construction and scope are given below. A mobile packet
is not by itself a waiting detector or an internally generated path approval.

## Fixed question and observer

At the central receiver define `M=(r0,r14)`. The initial pair is `(2,4)` and
both counter pairs are zero. A first incoming paired input `(1,-1)` gives
`M=(4,2)` with both quotients zero, so it writes a local remainder record
without a guarded arithmetic C event. A second identical input would give
`M=(0,0)`, with quotient 1 in channel 0 and quotient 0 in channel 14. Zero
input preserves the intermediate state exactly. This is a conditional local
calculation, not an autonomous complete-board construction.

The registered complete-board criterion requires a waiting interval of at
least four complete quiet updates, zero waiting counters and net input, and
exactly one C-bearing receiver update after the second arrival. **All 48
receiver channels** are included in the C observer. Neither source, source 1
only, source 2 only and both sources share the same apparatus and remainders;
only the initial source counters differ. Both single-source controls must
write the waiting record and have no receiver-node C event through the entire
horizon. The no-source board must remain stationary. Other nodes may click.

Both sources are prepared at time zero. No callback, signal insertion, reset,
click command or coupling change acts during evolution. A successful test
would establish a two-arrival confirmation or coincidence component. It would
not establish unique-path approval unless the confirming signal originated
inside a tested path apparatus in the same closed run.

## Completed finite negative results

| Family | Preparations | Complete runs | Accepted cases | Horizon |
| --- | --- | --- | --- | --- |
| Two guide modes, two source geometries, four distance pairs and four phase pairs | 64 | 256 | 0 | 40 |
| Two symmetric matching-buffer sites, each with nine even-remainder pairs | 81 | 324 | 0 | 40 |

All runs use side 201, fixed `(+,+,+)` coupling, all 48 channels and the
original Rule3. Every full state and every retained remainder is recorded.
Every production one-step inverse and complete rewind passed. Initial
boundary margins exceed the horizon. The first family consumed about 33.91
CPU seconds; the buffer family consumed about 46.41 CPU seconds. Neither
exhausted its declared budget.

The first family is frozen in
[confirmation_protocol.json](../research/component_studies/confirmation_protocol.json),
with [complete results](../research/component_studies/confirmation_search_evidence_v1/result.json).
The second has its own
[buffer protocol](../research/component_studies/confirmation_buffer_protocol.json)
and [complete results](../research/component_studies/confirmation_buffer_evidence_v1/result.json).
The first protocol and its source snapshot were preserved unchanged.

A concrete failure is `confirmation-000-s10`: the single signal changes the
receiver to `(4,2)` at step 8 without C. At old step 9 the actual input is
`(-2,+2)`, so step 10 already produces a guarded channel-14 event, with no
second source present. The following signal train continues to drive changes.
This is a transient record followed by repeat input, not a quiet latch.

The first implementation's isolated minimum-gap check uses `t2-t1>=4`.
Its complete acceptance predicate also requires the frozen arrival windows,
whose distance gaps are at least eight; together those conditions imply at
least six complete intervening quiet updates. Therefore this shorthand
cannot produce a false accepted case in that family. The second protocol
explicitly uses `t2-t1-1>=4`. No acceptance criterion was relaxed after seeing
results.

The buffer family is assembled through the generic component API:
`GuideSegment` reserves explicit sockets, `Receiver` supplies the central and
buffer remainder pairs, `SignalSource` supplies the initially present or
absent disturbances, and `finalize` produces a single immutable state and
engine. Assembly validity did not imply successful waiting behavior.

## A separate exact guided packet

Fix `(+,+,+)` coupling and a complete periodic X row. In that row, the
stationary guide has channel-0 remainder 0 and channel-14 remainder 4, with
all counters zero. All other channels have background `(0,0,2)`.

For `L>=5`, write local row coordinate `j` modulo L. In channel 0 prepare

`a_j = delta_(j,0) - delta_(j,2)`

`b_j = delta_(j,1) - delta_(j,3)`

`r_j = 4` for `j=0,1,2,3`, and `r_j=0` elsewhere on the row.

Channel 14 has opposite counters and remainder `4-r_j`. The complete
preparation also contains a transverse halo: at each of the four face-neighbor
rows in the Y/Z directions, in the channel selected from a channel-0 source,
set remainder 0 at `j=1,2`; in the channel selected from channel 14, set it to
4 there. The halo counters are zero. Its other remainders remain 2.

### Complete-state translation proof

Let `T_x` translate the full state one site in positive X. On the channel-0
row, transverse inputs are zero because the halo counters stay zero. Thus

`u_j = b_(j-1) + b_(j+1) = a_(j-2) + a_j`.

The prepared remainder satisfies

`r_j-r_(j-1) = 4(a_j+a_(j-2)) = 4u_j`.

Consequently `2u_j+r_j = 6u_j+r_(j-1)`, with `r_(j-1)` an allowed remainder.
Rule3 therefore has quotient `u_j` and gives

`a'_j=a_(j-1), b'_j=b_(j-1), r'_j=r_(j-1)`.

Channel 14 obeys the same translation by negating the counters and replacing
each even remainder r with `4-r`. For a transverse halo channel with source
sign `sigma=+1` or `-1`, its input is

`u_j=sigma*(delta_(j,1)-delta_(j,3))`.

Its remainder differences satisfy `r_j-r_(j-1)=-2u_j`. Hence
`2u_j+r_j=r_(j-1)` remains in `{0,2,4}`: the quotient is zero, the halo
counters remain zero, and its entire remainder pattern translates. All other
channels receive no nonzero input and remain at background. This accounts
for the complete six-port neighborhood, not only the visible row.

Thus `W(S)=T_x(S)` for this preparation. Translation covariance of the fixed
engine gives `W^t(S)=T_x^t(S)` for every nonnegative integer t. The unique
channel-0 value `a=+1` returns to its initial position only after a multiple
of L shifts, so the first complete return is exactly L. This proof is for
the declared periodic guide and preparation; it does not describe propagation
through an arbitrary environment.

### Finite checks and scope

The [packet protocol](../research/component_studies/confirmation_packet_protocol.json)
was frozen before checks at L=5,17,31. Source-present and source-absent controls
produce six runs and 106 forward updates. All source-present steps exactly
match the translated **complete** previous state, including the halo; first
returns are 5,17,31. All source-absent boards stay stationary while retaining
the same prepared remainders. Every one-step inverse and complete rewind
passes. The source-present packet has four guarded arithmetic events per
update; it is not a global no-click motion.

[Recorded results](../research/component_studies/confirmation_packet_evidence_v1/result.json)
include full traces, exact generic assembly manifests, all individual events,
source hashes and the fixed tensor fingerprint. The
[independent matrix-based audit](../research/component_review/packet_review.json)
reconstructs every preparation and checks all 112 retained states, 106 forward
and inverse transitions, and 212 individual guarded events. It passes. The
[independent proof review](../research/component_review/packet_proof_review.md)
separately verifies the all-L algebra; finite replay alone is not that proof.

This experiment deliberately uses a periodic, translation-invariant guide.
Its recurrence is not a no-wrap causal measurement. The result establishes a
prepared guided mobile pattern in board units, not physical light, physical
time, free-vacuum propagation or the waiting/confirmation milestone.

### Conditional limit on a quiet remainder record

For one actual channel trajectory, Rule3 gives the exact identity

`r_T-r_0 = 2 sum_(t=0)^(T-1) u_t - 6 sum_(t=0)^(T-1) ell_t`.

Therefore `r_T-r_0 = 2 sum u_t (mod 6)`. If the integrated incoming signed
input is zero, the two remainders must be equal: both lie in `{0,...,5}` and
their difference is a multiple of six. If the endpoint counters also return
to their initial values, the complete local triple is unchanged. In
particular, a channel starting and ending with `a=b=0` cannot retain a
different local remainder under this zero-integrated-input condition.

A fixed, unmodified site of the translating guide sees canceling incoming
inputs over one complete packet passage. The halo inputs likewise cancel.
The bare packet therefore does not itself establish a persistent quiet
remainder latch. A detector interaction can change the actual incoming
waveform, leave a counter record, or distribute information across other
channels and sites. The identity is conditional on the actual complete-board
input history; it is not an impossibility theorem for an interacting detector
or for memory in the whole board.

## Next decisive connection

A strict waiting device remains a research target. A new protocol can test
whether the compact packet, an initially prepared conversion region, or a
larger memory apparatus can create a quiet record and later accept a second
signal. Signal phase, full receiver-node events and the complete source
counterfactuals must remain fixed and visible. The current negative families
do not prove that such a component is impossible, and the mobile packet does
not retrospectively make either family pass.
