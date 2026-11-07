# Opposing compact packets: transport, local cancellation, and retained information

This is a finite interaction study on the unchanged `+++` Universe24 model.
It does not demonstrate an approval/cancellation protocol, a complexity selector,
physical light, or entanglement. It supplies an exact preparation for a
left-moving guided packet and a reproducible example in which central activity
vanishes while signals still leave the region.

## Question and fixed contract

Can two opposite compact packets suppress an outgoing local signal or write a
quiet remainder record that lasts eight subsequent updates? The protocol was
written before this family's trajectories in
[`interaction_protocol.json`](interaction_protocol.json). Its SHA-256 is
`49f06de82b605e1bf22eeea5d073ef43fd70ceb9d1e23a2b63e0ccab1bba912c`.

All preparations use one periodic cube, 48 channels, six spatial neighbors,
background `(0,0,2)`, body signs `+++`, and unmodified scalar Rule3 with
`num=den=1`. Every forward state is produced by the existing `Engine`.
The source-presence masks `00`, `10`, `01`, `11` change initial counters only;
the prepared source remainder pads and complete transverse halos are retained
in every control. There are no runtime callbacks, injections, erasures, or
coupling changes.

`GuideSegment`, `GuidedPacketSource`, `Receiver`, `Patch`, and the existing
assembly finalizer supply the initial data. `reverse_patch` in
[`interaction_search.py`](interaction_search.py) creates a transformed data-only
source patch; it does not run a special particle update.

## Exact algebra: a reverse-moving preparation

In the even-remainder sector define the complete-state involution

\[
J(a,b,r)=(b,a,4-r).
\]

This must transform **every** prepared channel, including every retained halo.
The uniform background `(0,0,2)` is fixed by `J`.

Let `F` be one full synchronous update and let
`2u+r=6 ell+r'`. After `F` followed by `J`, the second counter at every channel
is the original `b`. Therefore the next actual input is again the original
`u`. The second carry obeys

\[
2u+4-r'=6\ell+4-r,
\]

where `4-r` is a valid even remainder. Hence `F J F = J`, or equivalently
`F J = J F^{-1}`. This is an exact time-reversal identity; it is not a procedure
that rewinds the running board. All actual runs still advance with `F` only.

If the existing complete compact packet satisfies `F(S)=T_+(S)`, then
`J` commutes with translation and

\[
F(JS)=J F^{-1}(S)=T_-(JS).
\]

Thus the right-moving packet on a `(0,4)` guide supplies a left-moving packet
on a `(4,0)` guide. Two full-state carrier checks confirmed exact translations
for eight updates each on a side-129 cube. The identity is mathematical; those
two trajectories are finite checks of the implementation and preparation.

## Frozen experiment family

The interaction runs use `L=129`, `H=32`, and the X row at `Y=Z=64`.
The left source occupies `X=48..51`; the right source occupies
`X=77+d..80+d`. The guide is `(0,4)` left of `X=64` and `(4,0)` right of it.
The center remainder pair is one of `(0,4)`, `(2,2)`, `(4,0)`.

| Part | Cases | Purpose |
|---|---:|---|
| Exact carriers | 2 | Verify whole-state translation in each direction |
| Delays `d=0,2,4` | 36 | Three seams, three delays, all four source controls |
| Prospective geometric holdouts `d=1,3` | 24 | Same definitions on intermediate delays |
| Total | 62 | 1,998 complete states; 1,936 transitions |

Every node trace keeps all 48 channels at `X=56,63,64,65,72`, including the
actual six signed input terms for the observed pair. All complete board states
are retained separately. The outbound observation window was fixed at updates
20 through 32. A `C` here means any event returned by the existing classifier,
with each original `C0/C1/C2` kind retained; no event semantics were changed.

A strict cancellation witness required an outgoing pair `C` for one singleton,
none for the other singleton or null control, and none when both sources were
present. A quiet record required all 48 counters at a center-region node to be
zero and all 48 triples to remain identical for eight subsequent updates,
with the observed pair changed from its preparation and the full node distinct
from the null control. These definitions were not relaxed after the runs.

No active counter reached a periodic boundary. The stationary guide remainder
preparation extends across the board, but carries no initial counters outside
the source regions. This protects the stated horizon against wraparound; it
does not establish infinite-board or indefinite-time behavior.

## Results

| Fixed question | Result | Interpretation |
|---|---:|---|
| Strict outgoing cancellation | 0 of 15 groups | No tested joint run made either observed outlet silent |
| Eligibility under isolated-other-null clause | 0 of 15 groups | Reflected singleton signals already activate their own-side outlet |
| Eight-update changed quiet remainder record | 0 of 15 groups | No record satisfying the frozen definition |
| Nonlinear counter interaction | 13 of 15 groups | Joint counters differ from `10 + 01 - 00` somewhere |
| Four controls have distinct final complete states | 15 of 15 groups | No full-state merging |
| Complete transition and whole-trajectory inverse checks | All 62 runs | Exact recovery of every preparation |

The independent audit recomputed initial preparations, the `J`-transformed
halos, every recorded full-state transition and inverse, the probe values and
actual input terms, and all fifteen four-control comparisons. The audit agrees
with these finite results. The full audit is maintained by the independent
reviewer in the parent message-mechanism study.

The 13 nonlinear cases establish interactions in this preparation family.
They do not establish logical authorization, a robust gate, a retained click,
or selection of the more complex path. The geometric holdouts do not test
amplitude robustness, arbitrary perturbations, or all tensor sign families.

## Illustration selected after analysis

The generic Presenter bundle contains the four controls for seam `(0,4)`,
delay `0`. This group was selected after examining results to illustrate the
distinction between local cancellation and complete-state erasure. It is not
a newly defined successful experiment.

| Initial sources | Pair C events at left outlet, updates 20–32 | Pair C events at right outlet, updates 20–32 |
|---|---:|---:|
| `00` | 0 | 0 |
| `10` | 4 | 8 |
| `01` | 8 | 4 |
| `11` | 4 | 4 |

For `11`, every center-node counter at `X=64` remains zero and there is no
center `C` throughout the recorded 32 updates. Each singleton does activate
the center. The joint run still has outgoing signals on both sides, and its
complete state differs from every other control. The center is unchanged from
its preparation, so it also fails the required **changed** remainder-memory
predicate. Silence at this node is neither a persistent result record nor
erasure of an alternative history.

Open [`interaction_evidence/interaction_presenter.html`](interaction_evidence/interaction_presenter.html)
in a normal browser. The experiment selector exposes all four controls.
The Presenter only replays the complete recorded states; it adds no dynamics.

## Reproduction and evidence

From the repository root, choose a new destination:

```sh
python -m research.message_mechanism.interaction_search --output /tmp/universe24-opposing-packets
```

The output includes the exact protocol, `summary.json`, complete Presenter
experiment records in `records/*.json.gz`, full probe traces in
`probes/*.json.gz`, and initial-data assembly manifests in
`assemblies/*.json.gz`. Compression is lossless and deterministic; canonical
content hashes are recorded. The summary records the checkout commit, all
engine/component/search source hashes, tensor signs, initial-state hashes,
all candidate parameters, horizons, full rewind results, and compute usage.
There is no random seed because the complete family is enumerated.

The initial run used approximately 23 CPU seconds. A second run with only
lossless output compression changed reproduced the same 62 complete-record
hashes and all scientific metrics. The packaging verification file preserves
that comparison; the final summary identifies the reproducible compressed
writer version. Both runs together remain within the 256-case/300-CPU-second
search budget.

## Decision

The reverse-moving guided packet is a constructive algebraic addition to the
available initial preparations. This collision family does **not** provide
the requested approval, cancellation, or persistent click mechanism.

The next decisive preparation experiment should combine a transported packet
with an initially asymmetric static converter or receiver and require a
changed quiet record with the same all-48-channel criterion. Any proposal
that instead switches coupling, injects a later signal externally, or deletes
the outgoing information would change the model contract and is outside this
candidate.
