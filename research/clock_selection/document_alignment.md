# Live research document and implemented Rule3: source alignment

This is a read-only alignment check made on 2026-11-08. It adds no experiment,
engine option, tensor family or Google Doc edit. The source is the exact
[Universe24 research document](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit),
whose connector metadata reports modification at
`2026-11-07T13:47:08.362Z`. The retrieved text, including its original byte-order
mark and line endings, has UTF-8 SHA-256
`082e024ed6a20956fd486b3a8d3bc0201c90ed1ac4adb9d3e52f3df59126852c`.
This identifies the returned readable text, not a native Google Docs revision
or its formatting. The [receipt](evidence/document_alignment/receipt.json) and
[scoped exact excerpts](evidence/document_alignment/excerpts.json) pin the
source metadata, line anchors and comparison code hashes.

## What was already in the document

H1 already gives the normalized general scalar recurrence:

```text
ell, r_next = divmod(2*num*Sum6(current) + r, 6*den)
previous_next = current
current_next = ell - previous
```

Here `den > 0` and `0 <= r < 6*den`. The remainder is added after multiplying
the neighbor sum; the old previous counter is subtracted after division. A2
gives the same placement for a separate signed-adjacency comparison with
`K = 2*num*A*b`. The general normalized formula is therefore not a newly
discovered correction to the living document.

| Scope | What the document says | Status of this work |
| --- | --- | --- |
| H1 uniform scalar comparisons | `0/1`, `1/2`, `2/3` and `1/1` are separate spatially uniform coefficient systems, with one scalar channel per node. | Historical comparisons, not the present 48-channel runs. |
| H1a and the current A2 appendix | Every elementary update has `num=den=1`; no channel independently chooses a ratio. | Matches the unchanged engine used by the clock-selection studies. |
| A11 effective families | A different collective recurrence needs an encoding and declared time comparison, or a controlled approximation. One frequency is insufficient. | Effective behavior remains distinct from changing primitive coefficients. |
| Fixed heterogeneous coefficient field | Different immutable ratios attached to different channel updates. | A separate proposed candidate in [fixed_ratio_candidate.md](fixed_ratio_candidate.md), not an implemented baseline option or a replay of H1's uniform comparisons. |
| A6b broader axial-action family | 512 exponent triples, or 4096 labeled signed tensors before symmetry equivalence. | Explicitly proposed and unimplemented; current code retains only the eight sign triples at body actions `(0,1,3)`. |

## Match to the actual code

At repository base `ff89e2ff661c8b60af84aff738f9040ad7f15bcc`, the inspected
`universe24/core/rule3.py` exposes `forward(old, neighbor_sum)` and calculates
`divmod(2*neighbor_sum + old.r, 6)`. It has no `num` or `den` argument.
`universe24/core/coupling.py` fixes the body actions to identity, the chosen
y lift and the third power of the z lift; it accepts three signs. Experiment
configuration accepts `coupling_signs`, not arbitrary exponent triples or a
coefficient field. The receipt hashes these exact inspected files because the
research worktree also contains uncommitted research artifacts.

A fixed heterogeneous coefficient proposal can retain a local reversible
integer update, but it changes the declared model when a coefficient differs
from 1/1. In particular, `den > 1` enlarges the channel remainder domain to
`0..6*den-1`. Holding such parameters constant during evolution is not enough
to make them an existing freedom of the current engine. No such extension was
executed in the clock-selection studies.

## Historical numerical claims are not newly verified here

The document reports eight prepared scalar plane-wave comparisons using 8,192
positions, width 160, amplitude 100,000,000, initially zero remainders and 600
updates. It reports a 1/1 packet displacement of 346.306 links, speed 0.577176,
small comparison error and exact inverse recovery. These are document-reported
historical results. They are neither evidence from the new 48-channel gate
studies nor verification of the heterogeneous-field proposal.

A targeted search of repository Python files, Markdown and protocol JSON under
`research/`, `docs/` and `README.md` for those distinctive values did not locate
a matching producer and complete evidence package. The only pre-existing
protocol hit was the digit sequence `8192` inside an unrelated SHA-256 string;
the other hit was the new ratio proposal's statement that this table has not
been verified. This bounded search is not proof that no evidence exists in
another archive. The historical table remains unverified in this session.
No new trajectory or replay was run for this alignment task.

## Consequence for the claim register

Keep four distinctions explicit: a formula already documented; an engine option
actually implemented; a finite result independently replayed; and a separate
candidate only proposed. The current evidence establishes none of the older
scalar table, all 512/4096 proposed tensors, or heterogeneous per-channel
coefficients. Those each need their own frozen specification and evidence.
