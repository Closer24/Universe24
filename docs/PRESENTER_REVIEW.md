# The Presenter: independent review

The Presenter is a generic read-only representation of complete recorded states
of the existing Universe24 reference model. Its scope is the fixed 48-channel,
six-port tensor family, including all eight body-sign choices, and finite
recordings within the stated resource limits. It is not a universal viewer for
unregistered changes to the model or an unlimited data set.

This review treats the initial full state as the reproducible preparation.
A seed or a narrative about how that preparation was discovered is additional
provenance. A state digest verifies equality of data; it does not certify that
an optimizer, a random preparation procedure, or an observer was specified
before a run. Imported source metadata is a claim until independently checked.

## Independently checked behavior

The executable review is `tests/test_presenter_review.py`. It imports the
production engine only to produce recorded states. Expected complete updates
and exported tensors are compared with the separately constructed exact
matrix oracle in `research/reference/`. No previous guide geometry, designated
channel pair, experiment name or expected visual result supplies that oracle.

| Check | Finite scope and acceptance condition |
|---|---|
| Exact tensor and dynamics | All eight sign choices and all six zero-counter background remainders; 48 distributed preparations on an L=3 cube with every channel represented; two updates per preparation. Every dense triple and serialized routing/sign entry must match the matrix oracle. |
| Retained information | Remainder-only changes outside the selected channel must remain in complete sparse states, hashes and transition validation. |
| Python-to-browser parity | 49 fresh captures, including all 48 sign/background cases and a huge-counter case; 189,216 address/frame checks across all 48 channels. JavaScript `BigInt` values and every inspected completed transition must agree with the exported exact states. |
| Large signed counters | Positive and negative 5001-digit counters, including a raw native JSON integer checkpoint; exact decimal strings and independently calculated SHA-256 values must survive without changing Python's process-wide conversion guard. |
| Passive observation | Different initial views and declared readouts must produce identical trajectories. The exported readout declaration must not alias a subsequently changed caller-owned declaration. |
| Snapshot scope | A single checkpoint at nonzero recorded time must have no claimed incoming transition. A multi-frame trace must have consecutive update indices. |
| Adversarial data | A changed hidden remainder must be rejected even after its state digest is recomputed and its audit flag remains true. A missing intermediate update must be rejected. |
| Resource refusal | Too few allowed frames, cells or bytes must raise an explicit error rather than return a truncated experiment. Existing output files must not be overwritten. |
| Core integrity | Every Python file under `universe24/` must match the pinned baseline manifest in `research/reproducibility/base_engine.json`. |

The final commands, exit codes, test counts, artifact digests and core comparison
are recorded in `research/presenter/verification.json`. That file distinguishes
the independent data checks from browser interaction and visual evidence.

The final frozen-source run passed all 70 Python tests, including the 11 tests
in this independent review, in 103.932 seconds. The separate JavaScript data
suite passed 18 groups over 51 generated experiments and 103 transitions.
The final DOM/native-canvas harness passed 10 groups with no reported script
errors. All 13 core file hashes matched the pinned baseline. An earlier
120-second full-suite deadline expired; that incomplete attempt is recorded
separately and is not counted as a pass.

## Findings that affect interpretation

The complete state includes the default background and all deviations from it.
A counter-only view is a projection. A zero counter pair can retain a different
remainder, and signed input cancellation can conceal active contributions.
Neither is a deletion of microscopic information.

The dial depicts the direction of `(a,b)` and therefore discards amplitude from
its picture. The exact integers remain available in the inspector. The phase
uses an approximate finite graphical normalization; hashes, readouts and Rule3
arithmetic use the exact integers. The six remainder classes, or equivalently
the three-position remainder wheel and its parity bit, must both remain
accessible. See [PRESENTER_ALGEBRA.md](PRESENTER_ALGEBRA.md).

A rendered revolution is not an established oscillator period. A period of a
selected projection is not recurrence of the complete board. A playback rate
is not physical time, and a drawn interaction is not evidence for light,
matter, a detector, the Born rule or gravity. These claims require separately
declared experiments and evidence.

Fixed readout definitions remain fixed during navigation, but an imported
declaration alone does not prove preregistration. Its initial true value has
no observed rising edge. Arithmetic C0/C1/C2 classifications are separate from
those experiment-specific records and never modify the recorded states.

## Review findings and release conditions

The first source review identified that the browser's native importer ignored
unsupported checkpoint fields and a checkpoint's `steps` type, although the
Python loader rejects these inputs. It also identified that imported audit
flags could describe a first snapshot as an audited transition. Both findings
were corrected by the data implementation owner. Nine independent rejection
cases cover unsupported fields, a negative or floating-token `steps` value and
false first-frame audit claims, including extra coupling semantics and quoted
native counters. A snapshot carrying unverified provenance
claiming physical validation still receives zero validated transitions and
`physical_validation: false`. The final verification record records these
checks alongside the later integration results.

Release requires a self-contained local HTML artifact; generic rendering with
no experiment-ID or selected-channel special cases; simple spatial navigation
with optional exact details; complete import validation; and unchanged core
hashes. Camera movement, file selection, filters and playback may change only
the presentation. They must never alter a frame, coupling or recorded observer.

All work is local on the research branch. This review does not authorize a
push, pull request, merge, deployment, model change or an intervention in an
experiment.

The local Chromium launch investigation did not produce a running browser.
The suspected environment restriction is not a proven root cause. Any
DOM/native-canvas harness evidence must therefore be identified as such;
it does not establish a browser-rendered CSS layout or a successful Chromium
acceptance run. The final verification record preserves this limitation.

## Limits and next decisive checks

The default portable limits are 64 MiB, 10,000 frames per experiment, 500,000
stored cell rows across a bundle, 64 experiments, 100,000 decimal digits per
counter, 256 readouts and 1,024 clauses per experiment. Coordinates and update
indices must be exact safe integers in the browser. These are engineering
limits, not mathematical bounds on Rule3. A larger experiment must be exported
as a smaller complete recorded segment; no missing updates may be invented.

The review establishes finite agreement and checks important failure cases.
It is not a formal proof of all JavaScript, parsing, graphics or engine behavior,
nor evidence of physical validity. Very large admitted data can still be slow
to validate or draw. Graphics may overlap or hide nodes under a filter, so exact
coordinate and channel inspection must remain available.

The next scientific decision is whether a separately specified signal,
clock and persistent-memory assembly survives predeclared perturbation and
composition tests under the unchanged Rule3 dynamics. The Presenter makes
such evidence inspectable; it cannot supply the missing physical result by
changing the picture.
