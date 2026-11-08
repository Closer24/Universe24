# Interaction of two exact invariant families

Status: completed and independently audited. Four registered preparations on
the unchanged 48-channel Rule3 board reproduce the predicted nonlinear carry
when two exact invariant patterns overlap initially. This result concerns an
interaction throughout a prepared periodic board. It does not establish a
localized collision, detector memory, a force or preferred-route selection.

## Registered question and preparation

The [frozen protocol](../clock_selection/invariant_overlap_protocol.json) asked
whether two independently verified eigenpatterns with eigenvalue 4 produce the
exact predicted division carry under ordinary Rule3, with all four input masks.
The cube has side `L=4`, periodic boundaries, tensor `+++`, and 12 updates.
There is no random seed, runtime injection, projection, coefficient change or
observation feedback. Every update reads the same complete previous state.

At address `(x,y,z,g)`, the two patterns are

```text
vS = (1, 0, -1, 0)[x mod 4]
vI = R(g)[1][1]
```

`R(g)` is reconstructed with independent exact matrices using the documented
channel convention. The fixed six-input operator satisfies `F vS = 4 vS` and
`F vI = 4 vI` at all 3,072 addresses. Per node, `vI` has eight entries +1, eight
entries -1 and 32 zeros. These operator and complete preparation identities
passed [independent static preflight](evidence/overlap_independent_preflight.json)
before the native run.

| Mask | Initial previous counter a | Initial current counter b | Initial remainder r |
| --- | --- | --- | --- |
| 00 | 0 | 0 | 2 |
| 10 | 0 | vS | 2 |
| 01 | 0 | vI | 2 |
| 11 | 0 | vS + vI | 2 |

The counters are added only during preparation; the remainder is assigned
once. All four initial boards have identical remainders and the same tensor.
Both patterns occupy the board initially, so this is not an experiment with
separated objects approaching one another. Side 4 deliberately contains the
complete spatial period; no free-space or size-robustness claim follows.

## Primary prediction and result

Each singleton follows the scalar recurrence

```text
ell, r_next = divmod(8*b + r, 6)
(a_next, b_next) = (b, ell-a)
```

starting at `(0,1,2)`. A negative pattern entry uses the exact signed encoding
`J(a,b,r)=(-a,-b,4-r+2*(r mod 2))`; zero entries remain `(0,0,2)`. This is an
encoded collective behavior of primitive Rule3 with `num=den=1`, not a changed
channel coefficient. The complete singleton boards matched this oracle at
every recorded state; the null board was stationary.

For any mask, the first native input is `u=4*(sS*vS+sI*vI)`. With initial `a=0`
and `r=2`, the next `(b,r)` is therefore `divmod(8*(sS*vS+sI*vI)+2,6)`.
Define, using ordinary integer subtraction,

```text
D_a = a11-a10-a01+a00
D_b = b11-b10-b01+b00
D_r = r11-r10-r01+r00
```

The first-state predictions and observations were identical at every address:

| Quantity at state 1 | Expected counts | Observed counts |
| --- | --- | --- |
| D_a | 0 at 3,072 addresses | 0 at 3,072 addresses |
| D_b | +1 at 128; -1 at 128; 0 at 2,816 | +1 at 128; -1 at 128; 0 at 2,816 |
| D_r | -6 at 128; +6 at 128; 0 at 2,816 | -6 at 128; +6 at 128; 0 at 2,816 |

Positive counter defects occur where `vS=vI=+1`; negative defects occur where
`vS=vI=-1`. The full relation is `D_r=-6*D_b`. Individual remainders stay in
`0..5`: the values +/-6 are differences between four preparations, not an
out-of-range remainder. The joint evolution is thus not the additive sum of
the singleton evolutions, despite their identical initial remainder fields.

All four captures completed. There were no counterexamples to the registered
first-step prediction, singleton/null checks, input comparisons or native C
comparisons. The [independent replay](evidence/overlap_independent_audit.json)
verified all 52 complete states, 48 transitions, every inverse transition and
four full rewinds. It independently reconstructed all 13 complete defect
arrays, not only their histograms.

## Fixed finite follow-up and raw arithmetic events

States 0 through 12 were retained without early stopping. The first-step carry
is the primary interaction result. Later defect arrays and recurrence
observations are descriptive; no later joint outcome was required for success.
The singleton boards first returned at state 8 and matched the same lag over
the rest of the recorded window. The joint board had no equal pair of complete
states among states 0 through 12. That finite absence does not establish
aperiodicity or long-term behavior. Nothing beyond update 12 was observed.

All native C events were retained with their address, class, quotient, before
and after triples, actual input sum and six individual signed donor values.
The ordinary nonzero-quotient and changed-triple guard was unchanged.

| Mask | C0 | C1 | C2 |
| --- | ---: | ---: | ---: |
| 00 | 0 | 0 | 0 |
| 10 | 0 | 6,912 | 6,912 |
| 01 | 0 | 4,608 | 4,608 |
| 11 | 2,304 | 7,360 | 7,360 |

These are descriptive arithmetic event counts over updates 1 through 12. They
are not detector approvals, mutually exclusive outcomes or a selection rule.
The differing counts do not by themselves demonstrate memory or measurement.

## Reproducibility, resource limits and evidence

The registered limits were 20 CPU seconds for the complete producer workflow,
10 CPU seconds for independent replay, 30 combined CPU seconds, 120 seconds
wall time and 16 MiB of recorded study data. The dedicated processes include
startup/imports, preparation, capture, inverses, passive analysis, compression,
export and hashing. Separate earlier static preflight receipts remain distinct
from these measured native workflows.

| Dedicated workflow | Measured CPU | Limit |
| --- | ---: | ---: |
| Producer including wrapper | 4.510947 seconds | 20 seconds |
| Independent audit including wrapper | 3.114972 seconds | 10 seconds |
| Combined | 7.625919 seconds | 30 seconds |

Producer wall time was 4.498309 seconds; independent audit wall time was
3.083279 seconds. The completed producer directory, including its budget
receipt, occupies 1,822,460 bytes; the audit and preflight certificates add less
than 20 KiB, remaining below the 16 MiB limit. The unchanged producer receipt
correctly says its audit was pending when written; the later
[audit budget certificate](evidence/overlap_independent_audit_budget.json)
establishes the combined total. No native run was repeated or extended.

The [study directory](evidence/overlap_v1/) contains complete compressed native
recordings under `native/`, passive input/event records under `records/`, all
defect arrays in `interaction_defects.json.gz`, source snapshots and hashes,
the complete initial states and tensor in `registration.json`, and all four
complete Presenter experiments in `experiments.json`. An immutable native
checkpoint was written before each passive observation step. No case was
missing or captured without its observation record.

| Identity | SHA-256 or commit |
| --- | --- |
| Core baseline commit | `ff89e2ff661c8b60af84aff738f9040ad7f15bcc` |
| Checked-out research base commit | `3204576de7c2234b5568ba9efe18859821526247` |
| Protocol | `1c6851a118c1141e5ad983dc2c736f35a858d8c416a7e63caf04ba1ba4339e32` |
| Producer `overlap.py` | `7efd85923de1b4d832d455ae8c5a2a1df5394b1c19c657d87bd1ffc20525ebd1` |
| Producer wrapper `overlap_budget.py` | `7912467c54893d2bfcbe7116675acb98995d132aa41e2770ad4a14c6a6840c95` |
| Independent audit certificate | `9d4ed12c7c829c7fe5e2373c3363a71dcdbbbee20f7eb0c598df40935f36e4e7` |

From the repository root, use new output paths; existing evidence must remain
immutable. These commands reproduce the registered native study and its audit:

```bash
python -m research.invariant_families_v1.overlap_budget \
  --output research/invariant_families_v1/evidence/overlap_reproduction
python -m research.invariant_families_v1.audit_overlap_budget \
  --study research/invariant_families_v1/evidence/overlap_reproduction \
  --output research/invariant_families_v1/evidence/overlap_reproduction_audit.json
```

To build a local read-only Presenter page from the already recorded four
controls, without evolving the board again:

```bash
python -m research.presenter.build \
  --input research/invariant_families_v1/evidence/overlap_v1/experiments.json \
  --output research/invariant_families_v1/overlap_presenter.html
```

The result supplies an exact interaction example between two global invariant
families. Localized composition, persistence under new preparations and
interaction-generated memory require separately registered tests. Those
questions were not silently added to this completed four-case study.
