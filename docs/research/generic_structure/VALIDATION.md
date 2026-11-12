# Executed validation

Baseline: PR52 `8c53e69f4b466dcbd2da7dab7e3c365bd9731766`.
All results below were executed locally on the final research sources.
They establish the assertions scoped in each report, not general physical acceptance.

| Check | Result |
| --- | --- |
| `python -m validation.generic_structure.run_all` | All eight audits passed, including the independent review |
| `python -m unittest discover -s universe24/tests -t .` | 286 tests passed in 222.738 seconds |
| `python -m validation.system_smoke --out runs/generic-structure/system-smoke` | Generic forward/replay smoke passed |
| `python -m universe24 verify --run runs/generic-structure/system-smoke/run` | Saved run verified |
| Final source/evidence integrity | All nine research source hashes and eight evidence hashes matched; both compressed traces round-tripped exactly |
| `git diff --check` | Passed |

`runs/generic-structure/collection.json` binds every audit to its source,
evidence and execution log. The final independent-review evidence also hashes
all nine research modules. The full unit-test log is retained at
`runs/generic-structure/logs/unit-tests.txt`.

The large native-schedule and frame traces are stored as deterministic gzip
archives. The collector records both raw JSON and archive SHA256 hashes; running
the audit regenerates the plain JSON. The saved contract runs referenced in
`runs/generic_structure/contracts/06_contracts.json` are included under their
run-directory basenames. Absolute workspace prefixes in that report are original
execution provenance; resolve the `runs/` suffix in a different checkout.

Independent review found and retested three fixes: reject an overridden channel
budget above 48, reject illegal reduced-sector carries before embedding, and
rebuild the pure-gradient tensor instead of trusting mutable adapter metadata.
Its new counterexamples include noncommuting integer floors despite `BA=I`,
two individually null histories leaving their constraint, and a relabelled
inertial tensor that must not enter the force-only adapter.

The negative physical controls remain failures by design: the common45 source
constraint defect, the reduced Einstein history defect at tick two, the packet's
finite-lattice proper-time mismatch, and the missing fixed-physical-mass
refinement. Passing this suite means those boundaries are detected. The separate
three-channel packet, eleven-channel frame primitive and restricted six-channel
sector are not combined into a single accepted Einstein model.

`.github/workflows/generic-structure.yml` repeats the eight audits and generic
runtime verification on Python 3.11 and 3.12. CI results are reported separately
on the pull request; the table above records local execution only.
