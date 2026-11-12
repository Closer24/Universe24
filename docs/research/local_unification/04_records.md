# Retained records and repeated local encounters

This reader follows the **same eight-channel conservative tensor** defined in
`validation/local_unification/native.py`. It adds no pointer channel, clock,
scheduler, runtime callback or physical energy assignment. Both banks and every
`(a,b,r)` triple remain counted.

## Record and inverse theorem

At a collision, write the four Boolean rails as `(r+,r-,c+,c-)`. The local
involution exchanges `1001` and `0110` and fixes every other Boolean input.
Consequently a ready record `10` with a single carrier has exactly two cases:

| Input record | Input carrier | Output record | Output carrier |
|---|---|---|---|
| 10 | 10 | 10 | 10 |
| 10 | 01 | 01 | 10 |

The outgoing record identifies the original carrier direction while the
carrier is routed into the positive rail. Reapplying the same collision recovers
the complete input. Selection therefore retains the distinction that disappeared
from the selected carrier subsystem.

The domain is part of the theorem. A pre-existing `01` record is not evidence of
a new event. An absent record `00`, ready record `10`, used record `01` and double
record `11` are distinct retained states. The fixed reader keeps all detector
opportunities, including absent/double carriers and unready records; it never
normalizes only over successful trials. A record particle count is read from the
actual rails, not reconstructed from a passive arithmetic click count.

## Transport and lifetime theorem

The shared first-order map is `F(A,B)=(G(B),S(A))`. The four velocities of S are
`(+d,-d,+d,-d)`, so a used record leaves in direction `-d` while the selected
carrier leaves in direction `+d`.

Suppose a new used record is in bank A at node x immediately after update t.
As long as every subsequent collision on its route has no carrier in either
carrier rail, G acts as the identity on that record. Induction gives its location
after k further updates:

`bank = A if k even else B`,
`node = x - floor((k+1)/2) d` (modulo the periodic side length).

The reader checks the carrier-free input hypothesis at every later collision.
It stops the lifetime certificate when that hypothesis ends, even if the bit
happens to remain unchanged. Complete reversibility may preserve the information
after a new collision, but this simple independent-particle location theorem no
longer applies. No permanent record or infinite lifetime is inferred from a
finite empty corridor.

This calibrates mechanical transport at one lattice edge per two Engine
updates. It does **not** prove a material clock measures GR proper time. The
pipeline's two banks are retained state, not two independent universes or a
passive external time counter.

## Four encounters under one tensor

The predeclared L=7 fixture contains four ready record particles and four
incoming negative-direction carrier particles. In bank B, records start at
0 and -2d, with carriers at 0 and +2d. In bank A, records start at -d and -3d,
with carriers at +d and +3d. All other current rails vanish; complete old
histories are prepared as `a=F^-1(b)`, with all six legal carry classes retained.

The same receiver at node0 has successful encounters at updates **1,2,5,6**.
The two cohorts each return for a second selection: updates1/5 and2/6. There is
no reset, supplied runtime input or postselected event schedule. The retained
used-record count is `0,1,2,2,2,3,4`; the total record count remains4.
Every emitted used record follows the proved corridor through update6.

The collision-off control creates no used records. Disabling record transport
gives only the first receiver success; every later detector opportunity is still
reported. These are explicitly different control tensors, not extra stages
secretly inserted into the successful run. At subsequent times on a finite
periodic board, record/carrier encounters and recurrences can invalidate the
empty-corridor hypothesis. This fixture demonstrates finite repeated use, not
indefinite organization growth.

## Executed interface and scope

`inspect_saved_run` first invokes the existing saved-run verifier, matches the
exact declared native tensor fingerprint, then reads all complete transitions.
An independent literal collision table and explicit scalar shifts verify both
banks, prepared old histories, every transition and unchanged carries. The
reader rejects a correct runtime trace belonging to a different collision law.
The connected run and controls are saved by the unchanged bundle/runtime.

An explicit `allow_native_prefix=True` permits a larger joint tensor only when
its first eight channel names and target polynomials are exactly the declared
native tensor, with no dependency on extra fields. The entire larger saved run
is verified before extracting the eight-channel histories. The report retains
the full tensor/bundle/run identity and actual total channel count; this reader
certifies record behavior, not the physical meaning of the extra fields.

```bash
python -m validation.local_unification.records --out runs/local_unification/records-new
python -m unittest universe24.tests.test_local_unification_records -v
```

The tests exercise all six directions, full rewind, used-record lifetime,
missing/incorrect histories, wrong-law readback, absent/double outcomes and the
depletion control. The source and complete tensor/bundle/run identities are
recorded in `records.json`. Positive energy/momentum and metric/source claims
belong to their independently checked common-law ledgers; this reader does not
convert an arithmetic record into a physical clock, Born outcome or Einstein
source by naming it.
