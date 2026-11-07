# Independent baseline review — 2026-11-07

Reviewed upstream snapshot: `ed1556e202eb0f3cc60342c75d44012c2eeb71c3` of
[Closer24/Universe24](https://github.com/Closer24/Universe24/tree/ed1556e202eb0f3cc60342c75d44012c2eeb71c3).
The audit did not change `universe24/`, existing tests, or the committed reflection report.
This is an independent agent review; acceptance into the project claim register still
requires the project lead to inspect the evidence. No physical interpretation was validated.

## Executed verification

Run records, commands, interpreter version, runtime and SHA-256 hashes of all engine
Python files are in [results.json](../research/baseline_audit/results.json).
All 36 fetched upstream files match their Git blob SHA-1 identifiers exactly;
[upstream_blob_verification.json](../research/baseline_audit/upstream_blob_verification.json)
records the independent comparison against the fetched commit tree.

| Check | Observed outcome | Scope |
| --- | --- | --- |
| `python -m unittest discover -s tests -v` | All 15 tests passed; 13.994 s reported by unittest | Existing suite, not all integer states |
| `python -m universe24 --config examples/impulse.json --audit` | Exit 0; every step passed inverse and balance checks | L=9, positive signs, specified impulse, 12 steps |
| `python -m universe24 --config examples/signed_impulse.json --audit` | Exit 0; every step passed inverse and balance checks | L=9, signs `(1,-1,1)`, specified impulse, 12 steps |
| Existing reflection audit | Exit 0; generated JSON exactly equals committed JSON | 24 improper spatial maps, 8 structural sign choices; uniform signed channel lifts |
| Sparse executor versus complete node interface | Exact equality in 48 prepared runs | All 8 signs × 6 uniform background remainders, L=3, all 27 nodes, 1 update |
| Single prepared clock pair | First full-state return at t=4 | L=5,7,11; signs `(1,1,1)` and `(1,-1,1)` |
| Two prepared pairs at adjacent x sites | First full-state return at t=5 | Same sizes and sign choices |

The reflection audit was invoked through its unchanged `main()` with only its module
`__file__` redirected to `research/baseline_audit/reflection_audit.py`; this places its
report in the review directory. No dynamics or search code was altered. Exact invocation
is retained in `results.json`.

The additional checks are reproducible with:

```bash
python -m research.baseline_audit.additional_checks
```

[additional_checks.py](../research/baseline_audit/additional_checks.py) fixes the generator,
random seed `20261107`, ranges, preparations and observations. The complete result is
[additional_results.json](../research/baseline_audit/additional_results.json). The random
node checks use 40 attempted channel-address overrides per run; collisions can reduce
the number of distinct overrides. Every generated state has its exact one-step inverse
checked. The clock preparation is the documented pair `(-1,-1,0)` at channel 0 and
`(1,1,4)` at channel 14, with background `(0,0,2)`; the second copy is one x-site away.
Full sparse-state equality includes remainder-only deviations. These are finite exact
computations, not robustness or generic-emergence evidence. Determinism makes an exact
return repeat indefinitely for that exact preparation, conditional on correct execution.

Both CLI examples end with signed account 12, equal to the initial value. That endpoint
equality does not prove conservation of this account for arbitrary signed trajectories.
The CLI output `logged_arithmetic_events: 0` is caused by omitting `--events`; it is not
an observation that no arithmetic events occurred.

## Coverage limits and missing evidence

- `tests/test_universe24.py:34` checks scalar inversion on 360 combinations, including
  large negative counters and all six remainders. A universal inverse claim needs the
  algebraic argument, not this finite sample.
- `tests/test_universe24.py:49` checks eight-step trajectories for only two signs and a
  single impulse on L=5. Its name mentions equal snapshots, but it does not independently
  compare a dense synchronous implementation. The new node-interface comparison narrows
  that gap; it is still a bounded implementation check sharing the scalar primitive.
- `tests/test_reflection_audit.py:56` checks one generated full-state preparation per
  sign choice at L=5. Uniform signed coupling identities and contradiction certificates
  supply the broader algebraic argument; random-state tests alone do not.
- Existing tests do not certify a moving localized full-state object, persistent detector
  memory, composition of components, a state-dependent effective clutch, generic
  self-assembly, physical conservation laws, quantum measurement, Bell violations or
  gravity. No such conclusion follows from a passing baseline.
- Research document A14 reports 200 historical random node comparisons and inverse checks
  on 27 sites. Their original program, seed manifests and raw results are absent from this
  36-file upstream snapshot. Do not count those historical numbers as rerun here. The new
  48 node-equivalence preparations are separately identified evidence.
- Research document A11 mentions disruption experiments, finite guide records, binary
  cost selection and homogeneous effective `1/2` and `2/3` encodings. The baseline
  snapshot does not include complete executable experiments for these claims. They stay
  reported/unverified until reconstructed with explicit seeds and readouts. The small
  clock checks above verify only the two stated recurrence motifs.

## Document alignment

The [research document](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI),
especially A11–A14, distinguishes positive-reference examples from the signed family.
The implemented one-board, 48-channel, six-spatial-input, fixed-coupling, scalar Rule3
contract agrees with that specification on inspection. Its NumPy matrix example and
the standard-library sparse engine are different representations; this review found
no disagreement in the 1,296 node comparisons across 48 prepared states.

The signed-reflection result in `docs/REFLECTION_AUDIT.md` agrees with the main
document's A6a, including the signed lift and order-four qualification. Its executable
certificate supplies additional verification. Likewise, the newly
reproduced periods for signs `(1,-1,1)` are narrower than extending all positive-reference
claims to signed couplings. They do not establish mobile clocks, detector records or
spinor/parity physics.

## Decision

The baseline passes implementation consistency checks. No core change is justified by
this review. Next decisive test: freeze a source–receiver–record preparation and a local
readout, then compare source-present and source-absent trajectories on several sizes,
checking every retained component, a declared record duration and exact reversal. A
temporary record must retain its duration qualifier. Failure of its declared persistence
window is a negative result even when attractive arithmetic click plots remain.

## Follow-up review: prepared signal–clock–record experiment

Reviewed `research/signal_memory/protocol.json`, `protocol_v2.json`, `run.py`,
`confirm.py`, their saved results, `tests/test_signal_memory.py` and the M1 gates
in `docs/PROJECT_PLAN.md`. Reran both complete scripts with their output root
redirected to a disposable directory, leaving the recorded artifacts intact.
Both result objects matched their saved versions exactly after excluding runtime
measurements. All four `test_signal_memory.py` tests passed in 0.065 s.

- The observer is a local function of two retained remainder values, not an
  external log: `M = (r_0 == 0 and r_14 == 4)`. A click is its rising edge.
  It only reads states already produced by the unchanged engine. Initialization
  is the only place where source, receivers, gap or perturbation are installed.
- For N=22, j=6, the first memory window is exactly the 34 sampled states
  t=6,...,39; reset is observed at t=40. The counter projection follows the
  declared four-phase cycle. A second autonomous click occurs at t=52.
  This is finite temporary storage in a prepared guide, not permanent memory,
  a unique detector outcome, or a rigidly translating full-state packet.
- First activation reaches every guide receiver j at t=j. Source-absent,
  source-only and interrupted-guide controls in v1 have no target click.
  The later-click failure of v1 remains visible as `ideal_cases_pass=false`;
  v2 prospectively narrows the requirement to the first window and tests a
  new guide length. It keeps the observer unchanged and does not erase the
  earlier failure.
- The one-unit remainder perturbation preserves activation and the counter
  cycle but prevents this particular memory predicate from ever firing.
  Parity invariance explains that failure. This is evidence against robustness
  to the declared perturbation, not absence of transmitted influence.
- Every transition and complete rewind in the recorded experiments passes
  full-state inverse checks. The normalized complete-state trajectories agree
  between L=141 and L=161. An additional direct scan during the independent
  rerun found every nonbackground address at least 58 sites from a coordinate
  boundary for L=141, and 68 for L=161, throughout t=0,...,60. Thus no actual
  active update in these trajectories requires a wrapped edge. This is stronger
  evidence for these runs than merely calling both cubes large; it does not
  claim all future trajectories are boundary-independent.

Review finding: `confirm.py` initially computed its top-level `all_pass` from
per-case predicates without including `size_trace_exact`, although v2 requires
cross-size equality. `size_trace_exact` is true in the reviewed results, so the
present scientific conclusion is unaffected. The acceptance conjunction was corrected to include it. The project lead reran both
protocols and the complete 19-test suite after this correction; see
`research/baseline_audit/final_validation.json`.

The demonstrated scope supports **M1-prepared** with the finite duration and
prepared-front qualifiers in the project plan. It does not satisfy M1-robust.
The next decisive work is a frozen perturbation and component-composition
matrix, including a readout that is intentionally tested across parity sectors;
any changed readout requires a new protocol and fresh validation preparations.
