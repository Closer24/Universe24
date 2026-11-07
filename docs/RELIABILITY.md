# Reliability and reproducibility — protocol U24-RELIABILITY-v1

This work implements the approved reliability plan.
It is based directly on `ed1556e202eb0f3cc60342c75d44012c2eeb71c3`, independently
of draft PR #1. It changes no file under `universe24/`, no coupling, no click
semantics, and no fundamental law. Tests and research oracles are not additional
stages of automaton evolution. No merge or repository protection setting is
performed by these tools.

## What is being established

The question is whether an independent implementation of the declared
mathematics agrees with the engine, and whether its evidence is reproducible.
Passing is finite implementation evidence, not empirical physical validation.
The constructive inverse and balance formulas are in [MODEL.md](MODEL.md).
No number of round trips alone proves those formulas for every integer state.

The baseline has 15 unittest methods; this change adds 28, for 43 total. Test
method counts must not be confused with the many prepared cases inside them.
The earlier reported “32 additional inverse tests” has not been identified as
an executable evidence package in the inspected source. It is not adopted as a
verified count. Checkpoint continuation now has explicit end-to-end regressions.

## Independent reference and coverage

[`research/reference/`](../research/reference/README.md) imports no production
code. It uses exact generic 4×4 matrix multiplication over rational polynomials
modulo x²−2. An explicit 48-matrix set is compared with generator closure.
Breadth-first Cx/Cy words only establish the documented channel numbering;
identity, generators, central element and rotations have fixed independent
anchors. Routing and signs are derived from the specification, not copied from
production tables. A dense gather executor independently updates all triples;
the production implementation uses sparse scatter. Both use exact Python
integers and the same mathematical specification: conceptual specification errors
remain a shared risk. An AST check supplements code review of import independence.

| Check | Fixed finite domain |
|---|---|
| Algebra | All 2,304 products, 48 inverse labels and 48 rotation labels; 24 distinct spatial rotations |
| Coupling | All eight sign triples; 6×48 routing/weight pairs each: 2,304 pairs |
| Scalar arithmetic | Eight hand-derived anchors and 1,350 signed/large-integer combinations; all six remainders; both inverse compositions |
| Complete trajectories | 8 sign choices × L=3,4,5 × sparse/dense × seeds 24001,24002 = 96 preparations, eight steps each |
| Backgrounds | All eight signs × six background remainders at L=3, seed 24003 |
| Compared forward triples | 2,654,208 in the 96 trajectories plus 62,208 in background checks; inverse and control comparisons additional |
| Geometry / order | Boundary-position fixtures, reversed traversal/insertion, translated nonwrapping neighborhoods at L=9,13 |
| Checkpoint continuation | 16 actual CLI split trajectories: eight signs × split at 2 or 5, ending at t=7 with nonrecurring fixture; full state and concatenated absolute-step events |
| Serialization | 48 sign/background combinations, counters exceeding 100 digits; zero-step resume |
| Observation | 1,134 scalar classifications; real zero-quotient hidden changes; unchanged-triple guard; all eight signs with/without event logging and audit |
| Input rejection | Invalid fields, versions, fingerprint, geometry, signs, counters/remainders, duplicate addresses, truncated JSON and output/input collision |
| Fault controls | Wrong single-port direction, wrong sign, lost remainder and in-place updates, confined to deliberately incorrect test executors |

Failures in independent table/state comparison save a first-difference report
under `U24_COUNTEREXAMPLE_DIR`, including preparation/generator, step, address,
expected/actual values and command. Original failures are retained; minimization
is not implemented and must not be claimed. Other unittest failures retain their
case/subtest context and traceback in the bundle. No new runtime dependency is
required.

The 96-case trajectory stage has a 300-CPU-second ceiling; the full bundle has a
600-second shared wall ceiling. CI also has a 10-minute job timeout. A budget
exhaustion is inconclusive, never an impossibility result. Timing is environment
dependent and is not compared as scientific evidence.

## Reproduce from a clean checkout

From the repository root, using Python 3.11 or 3.12:

```bash
python -m research.reproducibility.run --output runs/first
python -m research.reproducibility.run --output runs/second --skip-tests
python -m research.reproducibility.run --compare runs/first runs/second --compare-experiments
```

The first command runs all tests, the frozen example experiments, a negative Q
witness, and the historical reflection certificate. The second reruns the
experiments without rerunning all tests; its explicit scope is `bundle_only`.
The comparison requires identical source/input identities and experiment outputs;
`--compare-experiments` excludes only suite/scope differences, not failure status
or scientific outcomes. Without that flag the suite/scope must also agree.

For the baseline audit commands independently:

```bash
python -m unittest discover -s tests -v
python -m universe24 --config examples/impulse.json --audit
python -m universe24 --config examples/signed_impulse.json --audit
```

Output directories must be new. Existing evidence is never overwritten. `runs/`
is already ignored by Git; keep accepted evidence separately under version control
when publishing a result. A dirty checkout is rejected unless `--allow-dirty`
explicitly marks an exploratory run; its dirty state and all source hashes are
recorded. Source hashes are checked again at completion; edits during execution
invalidate acceptance. A clean checkout commit and the immutable engine baseline
are separate manifest fields. The source hash map also includes the independent
reference, tests, schemas, protocol, input fixtures, reflection script/certificate
and workflow. Different checkout metadata or Python versions may be compared
only when those source hashes and deterministic evidence agree.

## Bundle contract

The reference [model specification](MODEL.md) is byte-pinned by the frozen
protocol. Keep explanatory scope extensions in [candidate guides](COUPLING_FAMILIES.md)
and their README/proposal links; even an added cross-reference inside the frozen
specification changes its digest. The release integration check caught such a
documentation-only mismatch after PR #4, and the duplicate cross-reference was
removed without changing the protocol, expected results or engine.

The frozen [protocol](../research/reproducibility/protocol.json) records the
question, observation, baseline and specification digest, cases, success
criterion and budget. [`research/schemas/`](../research/schemas/) contains v1
JSON schemas. The stdlib validator implements and checks the explicitly used
subset; it rejects unsupported keywords rather than claiming general JSON Schema
support. Semantic checks reject duplicate case IDs and contradictory/empty
successful results. JSON and JSONL readers reject duplicate keys and non-finite
constants; filenames and state ordering have deterministic representations.

| File | Meaning |
|---|---|
| `protocol.json` | Exact declared protocol copied into the run |
| `manifest.json` | Code identity, source hashes, coupling fingerprints, environment and command |
| `result.json` | Execution, implementation and scientific outcomes in distinct fields |
| `runtime.json` | Nondeterministic wall duration and budget, excluded from equality |
| `cases/<id>/input.json` | Complete input configuration copied from the fixture |
| `cases/<id>/initial.json`, `final.json` | Complete retained-state checkpoints |
| `cases/<id>/trace.jsonl` | Step, full checkpoint digest, Q and cumulative arithmetic event count |
| `cases/<id>/result.json` | Exact expected/observed period and acceptance fields |
| `tests.*.txt`, `reflection.*.txt` | Raw execution logs |
| `counterexamples/` | First-difference artifacts if a comparison fails |

State hashes facilitate checking; they are not a replacement for the retained
initial/final states and deterministic generator. Event logs alone cannot invert
the automaton. The runner exits nonzero for failure or inconclusive execution.
The negative Q witness is an expected scientific refutation, not a failing
implementation regression. Updating expected periods, readouts or source pins
requires a new reviewed protocol; there is no auto-accept/update-baseline switch.

## Findings and limitations

The two exact impulse fixtures, L=9 with source `(0,2,2)` in channel 0, return to
full initial state first at t=6; the clock fixture at L=7 first returns at t=4.
These are facts about those complete seeds, not a universal impulse law or
sustained free wave. The positive and signed impulse runs each log 28 arithmetic
events over 12 steps; the clock example logs zero over 16 steps under the
unchanged guard. Zero logged events here is measured with the observer enabled;
it does not mean that the clock's retained state is static.

For signs `(1,-1,1)`, a single `(0,1,2)` source at L=3 gives Delta Q=-8. The full
inverse still succeeds. This refutes universal conservation of that particular
account, as required by its signed balance identity. Q remains unidentified as
physical energy.

Review caught and corrected gaps in the new research tooling: reflection files
were initially missing from provenance; JSONL parsing initially tolerated duplicate
keys; schema-only checking allowed duplicate case IDs or contradictory success.
All are covered by final validation. A source change during a run now invalidates
its provenance. None required changing the reference engine.

An initial fault-control attempt swapped both opposite inputs. Equal opposite
weights make that only a reordering of the same sum, so it was not detected and
must not be called a dynamics error. It is retained as an equivalent-operation
control; the actual wrong-direction fault duplicates one opposite input and is
detected. This illustrates why mutation controls need their own mathematical
review.

No engine mismatch was found in the completed local development suite. Final
clean-source and CI evidence are linked from the PR and acceptance report.
Agreement does not establish particles, autonomous physical time, measurement,
Born probabilities, physical conservation, gravity, or independent correctness of
all historic experiments. PR #1's finite guide result is outside this branch's
acceptance scope.

## CI, review and decision

The [workflow](../.github/workflows/ci.yml) runs on pull requests, pushes to this
research branch and manual dispatch, with Python 3.11/3.12, read-only contents
permission and SHA-pinned actions. It does not merge, publish releases or edit
repository settings. Each job uploads logs/evidence, including failure artifacts,
for 30 days. Those artifacts are temporary; accepted summaries and counterexamples
must be preserved in a reviewed research commit. Job success must not replace
review of the mathematical or physical scope.

Acceptance requires all tests, unchanged core hashes, complete-state equality,
checkpoint/event continuation, the expected negative Q result, reflection report
agreement and deterministic repeat agreement. A concrete unexplained mismatch
blocks acceptance. Next research direction remains the initiator's decision;
this task supplies an auditable basis for it.

In a restricted environment Python may fall back to the checkout for temporary
files. The bundle runner explicitly places test scratch files under its output
directory so temporary inputs cannot dirty source and block a clean rerun.

### Known serialization limit — separate observed negative result

A [reproducible diagnostic](../research/reliability/known_limits/serialization_probe.py)
constructs a counter `10**5000`. On local Python 3.12.14 with the default integer
string-conversion limit 4300, construction and exact forward/inverse succeed,
but `json.dumps(checkpoint_data(...))` raises `ValueError`. The
[recorded result](../research/reliability/known_limits/serialization_result.json)
retains the exact generator, source hashes and runtime limit. Reproduce with
`python -m research.reliability.known_limits.serialization_probe`.

Thus the complete mathematical state domain is wider than the default JSON I/O
domain. This is outside the registered 100-digit checkpoint cases, and is not
hidden by their success. No guard was disabled and no core/CLI change was made.
The minimal engineering follow-up is an explicitly reviewed I/O policy: bounded
accepted counter size or a deliberate conversion-limit policy with resource
bounds. It need not alter Rule3; the choice remains a separate decision. Python
configurations with a different/disabled limit may give a different diagnostic
outcome, which is why the actual limit is recorded. Reliability acceptance is
bounded and is not approval of unrestricted serialization of every valid state.

## Recorded acceptance

The [acceptance summary](../research/reliability/acceptance_summary.json) and
[complete evidence](../research/reliability/evidence/) preserve the final local
clean-source run: all 43 tests passed in a bundle taking approximately 66 seconds,
with identical deterministic experiment evidence on a separate rerun. The core
file hashes remain equal to the pinned baseline. The initial implementation also
passed GitHub CI on Python 3.11 and 3.12; the PR's latest checks are authoritative
for its final head. The serialization limitation above remains open and explicit.
