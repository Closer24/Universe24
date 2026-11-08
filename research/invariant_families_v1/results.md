# Exact invariant families: registered native verification

All 48 registered native runs matched their complete scalar-encoding oracle, every actual input sum, every raw C event, every inverse check and the complete final rewind. Independent full replay passed for all 912 complete states, 864 transitions and 48 full rewinds. The fundamental rule remains `num=den=1`, with the fixed baseline `+++` tensor.

This is an independent registered replication family. The earlier reported runs did not supply their exact sizes and seeds, so these results do not claim to reproduce those unprovided inputs.

## What is mathematically established

The [algebraic derivation](../clock_selection/invariant_families_algebra.md) gives an exact full-state invariant encoding. For a fixed ternary pattern `v` satisfying `Fv=lambda*v`, place one scalar triple according to:

| Pattern value | Stored triple |
|---|---|
| +1 | `(a,b,r)` |
| -1 | `(-a,-b,4-r+2*(r mod 2))` |
| 0 | `(0,0,2)` in this registered family |

The negative remainder assignment matters. The involution exchanges `0↔4` and `1↔5`, while fixing 2 and 3. Using the even formula `4-r` for an odd remainder is incorrect.

Every native channel then continues to use the same Rule3. The entire encoded board evolves according to the scalar oracle

```text
ell, r_next = divmod(2*lambda*b+r, 6)
a_next = b
b_next = ell-a
```

This closure follows for every integer scalar `a,b`, every valid remainder and every time under the stated eigenpattern assumptions. The finite native checks below corroborate its implementation; they are not substituted for that proof. Zero-pattern counters remain zero because their total input cancels. Their individual donor terms need not vanish, so these global preparations are not isolated QuietClock modules.

The actual 48-channel operator was independently reconstructed with exact 4×4 matrices. No production routing table was used to generate the expected eigenpatterns. Its six rows were compared to the unchanged native tensor, and `Fv=lambda*v` was checked at every address of each registered cube.

| Family | Fixed pattern | Side | Eigenvalue | Effective homogeneous ratio |
|---|---|---:|---:|---:|
| Uniform | `v=1` | 3 | 6 | 1/1 |
| Spatial period 3 | `(1,-1,0)[x mod 3]`, identical in all channels | 3 | 3 | 1/2 |
| Spatial period 4 | `(1,0,-1,0)[x mod 4]`, identical in all channels | 4 | 4 | 2/3 |
| Internal y/y | `v_g=(R(g)e_y)_y`, identical at every site | 3 | 4 | 2/3 |

The internal vector has exactly eight positive, eight negative and 32 zero channels. `R(g)` uses the repository's documented channel orientation and label order, independently reconstructed from the exact matrix group.

A separate static identity distinguishes signed tensors: under `+-+`, the same y/y pattern has eigenvalue 0, while the rotated z/z pattern has eigenvalue 4. These identities were checked algebraically and with the independent operator; **no signed-tensor native trajectory is part of this 48-case batch**. They do not change the baseline coupling used here.

The effective ratio is a full recurrence correspondence, not a frequency fit. If `lambda/6=p/q` in lowest terms, the generalized homogeneous remainder `rho=q*r+j`, with fixed `0≤j<q`, satisfies

```text
ell, rho_next = divmod(12*p*b+rho, 6*q)
rho_next = q*r_next+j
```

The native six-remainder preparations cover the `j=0` slice under this mapping. They do not test all `6q` generalized remainder states. No generalized-coefficient update was installed in the native engine. This state correspondence also does not automatically assign a new click interpretation to a different-denominator model; all events below retain the original native classifier.

## Registered computational domain

Each family used both exact counter seeds `(0,1)` and `(2,-1)`, all six base remainders `0..5`, and 18 updates. There was no random seed or adaptive search. All zero-pattern addresses had fixed initial remainder 2. The count is **4 families × 2 seeds × 6 remainders = 48 runs**, or 912 complete board states and 864 transitions.

The small periodic cubes are intentional. Period-3 and period-4 preparations require compatible periodic sizes, while uniform and internal patterns use the minimum supported side 3. These are global periodic preparations, not tests of boundary-independent localized propagation.

Every one of the **1,586,880 channel-state positions** matched the full encoded triple, including remainders. The actual input sum at every address for every update was retained and matched `lambda*b*v`: **1,503,360 input values**. All **793,632 native C events** were retained with their quotient, input sum and six separate signed donor values. Donor addresses are determined exactly by the archived tensor and recipient address.

## Periods are not a single fitted frequency

The horizon was fixed at 18 updates and was not extended after seeing a return. A reported return is equality of the complete board state, including all remainders.

| Family or scalar sector | Seed | Base remainders | First complete return within 18 |
|---|---|---|---|
| Uniform, lambda 6 | Both seeds | All six | None |
| Spatial period 3, lambda 3 | Both seeds | All six | 6 |
| Either lambda-4 family | `(0,1)` | 0, 1 | 6 |
| Either lambda-4 family | `(0,1)` | 2, 3, 4, 5 | 8 |
| Either lambda-4 family | `(2,-1)` | 2, 3 | 15 |
| Either lambda-4 family | `(2,-1)` | 0, 1, 4, 5 | None within 18 |

The uniform family has `b_next=2b-a` and constant remainder. These two seeds therefore drift linearly; they are not periodic clocks. The lambda-3 family has the exact period-six recurrence `b_next=b-a` for nonzero counter pairs. The two lambda-4 preparations share the same complete scalar recurrence but have remainder- and seed-dependent behavior. “No return within 18” does not assert nonperiodicity for a lambda-4 case.

## Native clicks

The event guard is unchanged: a nonzero quotient and a changed triple are both required. For the negative branch, the input changes sign, so C1 and C2 exchange. Zero-pattern addresses emit no C while their counters remain zero, even if their individual donor terms cancel.

The totals below sum all 12 registered cases in each family; the different spatial supports and sizes mean they are not normalized physical rates.

| Family | C0 | C1 | C2 |
|---|---:|---:|---:|
| Uniform | 279,936 | 0 | 0 |
| Spatial period 3 | 155,520 | 0 | 0 |
| Spatial period 4 | 55,296 | 112,128 | 112,128 |
| Internal y/y | 15,552 | 31,536 | 31,536 |

A separate observer regression uses an exactly stationary uniform triple `(1,1,2)` with input 6 and quotient 2. It emits no C because the triple is unchanged. This is a constructed observer fixture, not an additional native trajectory or a 49th registered case.

## Reproduction and evidence

Run a fresh, bounded capture without overwriting evidence:

```bash
python -m research.invariant_families_v1.run --preflight-output NEW_PREFLIGHT.json
python -m research.invariant_families_v1.budget --output NEW_EVIDENCE_DIRECTORY
python -m unittest discover -s tests -p test_invariant_families_v1.py -v
```

- [Frozen protocol](protocol.json): SHA-256 `f0340b86b689d681cc37cfd76e9e8617cd4f400ea1cb868fa94d00ff7471f523`.
- [Executed producer](run.py): SHA-256 `556b7adc1bff1a0cefc420c9e796f3fa19e35059f04c1857c4289dd87487c6be`.
- [Whole-process wrapper](budget.py): SHA-256 `8758a85953d0fd925fb7658a2c1d592adca7af2cdadf0f86ea1611fdb345eef4`.
- [Independent initial preflight](evidence/independent_preflight.json): all complete preparations, scalar traces/inverses, signed encoding and independent operator identities passed before capture.
- [Independent full audit](evidence/independent_audit.json): all 912 complete states, 864 transitions and inverses, 48 full rewinds, every input array, all raw C and six donor values, full-state returns and source archives passed. Independent audit CPU: 36.911 seconds, recorded separately from the producer budget.
- [Complete native evidence](evidence/native_v1/): immutable native checkpoints, observed records, exact executed dependency sources, protocol, registration and archive hashes.
- [Native result ledger](evidence/native_v1/result.json): all 48 cases and every outcome.
- [Whole-workflow resource receipt](evidence/native_v1/outer_budget.json).
- [Five prospectively selected Presenter examples](evidence/native_v1/experiments.json): all four families at `(a,b,r)=(0,1,2)`, plus the internal family with odd remainder 1.

The capture workflow used **57.357 CPU seconds**, 57.269 wall seconds and approximately **9.12 MB**, within the registered 180 CPU-second / 300 wall-second / 64 MiB budget. Timing covers imports, independent preflight, source preservation, capture, inverses, observation, compression, export and archive hashing. No case was skipped or left unobserved. All three focused regression tests passed.

The exact local base was `3204576de7c2234b5568ba9efe18859821526247`, with tree `09840e0ffdf158950332e10b05334212ab652378`. The manager and integration agent verified that remote commit `88700611ef307cb560f43957fc2dcb8be60c36b6` has the same tree. The native core still matches baseline `ff89e2ff661c8b60af84aff738f9040ad7f15bcc`. Frozen prior research evidence was not changed.

## Limits and next decision

These are exact, deliberately prepared invariant families. They do not demonstrate spontaneous formation, localized particles, physical mass, propagation, generic linear superposition, an autonomous detector or a preference for greater complexity. A global standing pattern and an internal channel pattern are distinct realizations of a common scalar evolution; matching that evolution is not evidence that either is physical matter.

No mathematical encoding or native oracle failed within this registered family. The uniform clock interpretation fails for the selected drifting seeds, and a single universal temporal period is not supported for lambda 4. The next separate question is whether independently valid sectors can coexist or interact under a common initial remainder assignment. Any overlap study has its own frozen protocol and must retain deviations from counter addition rather than assuming superposition.
