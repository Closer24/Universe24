# Claim register — evidence, scope and uncertainty

Baseline `ed1556e202eb0f3cc60342c75d44012c2eeb71c3`, 2026-11-07.
Types: **P** mathematical proof; **C** finite computational result in an explicit
domain; **H** hypothesis; **T** future target. A reported but unreproduced C claim
is marked **unverified** and is not an accepted project result. Definitions of
the model are premises, not evidence that nature satisfies them.

The research-document section references use the snapshot in
[SOURCE_AUDIT.md](SOURCE_AUDIT.md). New computation is on the unchanged baseline
core plus separately hashed research scripts. No claim is imported from a chat.

| ID | Claim / type | Candidate and scope | Evidence and verification |
|---|---|---|---|
| P01 | Complete-state map is a bijection — P | Every valid full state; every L>=3; any fixed allowed signs | Constructive two-sided inverse, [algebra proof](ALGEBRA_AUDIT_2026-11-07.md), A2; root reviewed proof and reran supplemental audit. |
| P02 | Influence radius is at most t graph links after t updates — P | Full lattice state, torus distance; not physical light speed | Induction on old-snapshot dependencies in algebra audit; A1–A2. |
| P03 | Every channel retains r mod 2 — P | All states, every coupling | Reduce `6 ell+r'=2u+r` modulo 2; algebra audit, A9. |
| P04 | `Delta Q=2(A-6I)b`; total Q conserved for positive signs — P | Periodic complete state, fixed background offset | Algebra audit and A10; eight finite signed balance tests supplement proof. |
| P05 | Universal conservation of the same Q under all signs is false — P | Any sign triple containing a negative sign admits a counterexample | `(1,-1,1)`, one b=1: Delta Q=-8, [audit results](../research/algebra_audit_results.json). Q is not identified with energy. |
| P06 | Complete local output cannot block arbitrary nonzero net input — P | Equal old triple, input sums differing by delta!=0 | `6 Delta b'+Delta r'=2 delta`; A9 and algebra audit. Does not exclude restricted effective clutches. |
| P07 | Universal bounded amplitudes are false — P | Positive reference, spatially/channel-uniform preparation | Exact solution `(a,b,r)=(t,t+1,0)`; A14 and algebra audit. |
| P08 | Proper cube covariance — P | Simultaneous position/channel action of 2O, fixed body signs | A6 group identity; `coupling.py`, rotation identity checks in reflection audit. Does not prove SO(3) or Lorentz covariance. |
| P09 | Improper cube maps have signed channel lifts commuting with W — P | Finite tensor certificate plus arbitrary-state scalar proof; all eight signs | [reflection proof](REFLECTION_AUDIT.md); exhaustive finite search class reproduced byte-for-byte by independent audit. |
| P10 | Chosen x-mirror lift has order 4, and no order-2 lift in the searched class — P | Uniform signed channel permutations; stated body signs | Reflection certificate and proof; not a no-go for nonlinear/position-dependent maps or physical parity. |
| C01 | Baseline implementation suite/audits pass — C | Original 15 tests; two L9, 12-step impulse audits | [raw audit metadata](../research/baseline_audit/results.json); signed residual is checked rather than assumed zero. |
| C02 | Dense gather and sparse scatter agree — C | Root rerun: 10,368 channels, all 8 signs, L3; independent review additionally all 6 backgrounds | [algebra results](../research/algebra_audit_results.json), [additional checks](../research/baseline_audit/additional_results.json). Finite implementation validation. |
| C03 | Prepared clock period 4 and adjacent pair period 5 — C | Exact full-state repeats; L5,7,11; signs +++ and +-+; specific A11 seeds | [independent review](INDEPENDENT_REVIEW_2026-11-07.md), runnable [additional_checks.py](../research/baseline_audit/additional_checks.py). Signed examples are new finite checks, not inherited claims. |
| C04 | Prepared front activates a local clock and finite record — C | Positive reference only; N18/j2, N20/j4, N22/j6; specified sizes/windows | [protocol and report](SIGNAL_MEMORY_EXPERIMENT.md), [v1](../research/signal_memory/results.json), [fresh v2 confirmation](../research/signal_memory/results_v2.json). Exact readout/controls; acceptance limited to reported window. |
| C05 | One-shot/permanent record and parity robustness fail for this preparation — C | v1 first record resets and later re-clicks; r+1 perturbation | Same experiment; failures retained. A finite failure rejects the corresponding universal robustness assertion, not every possible memory preparation. |
| C06 | Published planar packet speeds and <8e-6 relative discrepancy — C, unverified | Document Section 6: 8192 positions, 600 steps, separate coefficients | Numbers reported in document; source experiment files absent from pinned repo; not rerun here. No current signed-model or photon inference. |
| C07 | Signal disrupts a local clock beyond simple superposition — C, unverified | A11 refers to a specified historical finite experiment | Full seed/control artifacts not in pinned baseline. Independent reconstruction required. |
| C08 | Prepared binary-cost comparator selects one branch, ties to A — C, unverified | Restricted costs supplied in seed; positive reference A11 | Quotient formula alone is not a composable full assembly; no reproduced complete fixture here. |
| H01 | Homogeneous 1/2 and 2/3 effective encodings are valid families — H pending proof-artifact verification | A11 reports exact limited encodings; no general spatial fields | Recover encoding and all-family conjugacy proof before promotion. A matched oscillation frequency is insufficient. |
| H02 | Operational H16-C: higher joint response predicts selected records — H | Fixed ensemble/readout, independent matched controls | Defined prospectively in [PHYSICS_GATES.md](PHYSICS_GATES.md); no supporting experiment yet. |
| H03 | Discrete reversible Rule3 model describes nature — H | Physical inference, not mathematical premise | No empirical validation supplied by this audit. |
| T01 | Robust reusable signal–clock–memory assembly — T | Declared perturbations, phases, interconnected apparatus | M1-prepared is narrower; M2 acceptance gate in [project plan](PROJECT_PLAN.md). |
| T02 | Compact moving full-state pattern — T | Exact nonzero spatial shift, no wrap artifact | S2 search; a propagating activation front is not this certificate. |
| T03 | Reusable effective clutch, bound assembly and breakup — T | Same law; state-conditioned transfer and autonomous transitions | K1/B1 with restricted input alphabet; P06 excludes arbitrary full-state blocking. |
| T04 | Physical energy/momentum/charge/angular momentum — T | Local storage/flux, recoil and calibration | P8/H15; arithmetic Q or reversibility alone does not establish these. |
| T05 | Light, matter, quantum measurement and gravity — T | Separate observable prediction gates, including nulls | [physics gates](PHYSICS_GATES.md); scalar/spinor/tensor naming is not evidence. |
| P11 | Bell/CHSH bound under local responses and setting independence — P | Binary exhaustive outcomes and one setting-independent hidden-state distribution | Elementary algebra in physics gates. Mapping observed separation to lattice separation is still required. |
| T06 | Autonomous physical time and observer independence — T | Local state-derived timing and consistent operational calibration | P6/Section6; global simulator layers do not establish this. |

## Promotion and retirement rules

A new result needs a candidate, exact claim/domain, proof or frozen protocol,
reproducible artifact and independent verification. Historical result reports
remain unverified until their actual experiments or proofs are recovered.
A failed criterion stays visible; a revised protocol gets a new ID and new
validation data. Negative results may retire a search objective without retiring
the full model. Only empirical click comparisons can support a physical claim.
