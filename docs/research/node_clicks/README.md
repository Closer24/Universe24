# Internal faces, click observations and the common-law boundary

This integration adds usable node and observer interfaces, preserves the
earlier local work, and tests the requested common interpretation of light,
matter, dark matter and gravitational waves. The software interfaces work;
the tested tensors do not establish that common physical interpretation.

The prior restoring/phase audit was merged in
[PR #73](https://github.com/Closer24/Universe24/pull/73), on top of the retained
light-memory detector from PR #72. Independent reviews initially ran at local
commit `43b63f2f00525de580c92f20a05b83f74c99cc00`; its complete committed tree
is identical to public merge `535a4b7f6a65e7b9769a711db8ce99703b240b72`
(`8aabc8b84ad663d820c7eef0a1b2e855f06ba174`). Source hashes in individual
receipts identify any additional uncommitted modules used in their runs.

## The node and its six internal mechanisms

`universe24.node.NodeView(state, index)` is a passive view of one complete
48-channel node. `.faces` returns six `FacePort` objects. Each face groups
eight existing channel labels, or four central pairs, by its propagation
frame. `.values(bank)`, `.triples()`, `.central_contrasts(bank)` and
`.pair_sums(bank)` return immutable Python-integer readouts.

`port.opposite` names the neighbor's facing port. Both return the same
`EdgeRef(L, base, axis)`, including across periodic boundaries. This is one
shared adjacency identity, not two separately stored geometric lengths. The
reference has no dynamic state. Endpoint values need not agree, and a label
on one face may read either neighboring face in a legal tensor term.

No Engine code, extra state bank, hidden delay queue, external updater or
channel allocation is added. The node contains exactly 144 retained integers.
A view is bound to its supplied snapshot; a new Engine result needs a new
view. It is an auditor/developer view, not the click observer's information.

The gears-and-clocks analogy has a precise scope:

| Analogy | Implemented quantity | What it does not establish |
| --- | --- | --- |
| Gear state | A channel's complete `(a,b,r)` | A physical angular velocity or clock calibration |
| Six face mechanisms | Six groups of eight retained channels | Interaction among all six groups |
| Connecting contact | Shared `EdgeRef` identity | Shared metric length or delay variable |
| Restoring phase | Central contrast cycle in the prepared phase sector | Gravity or an ordinary-matter oscillator |
| Observer's ticks | Canonical quotient/class/sign click records | Photon number, material proper time or metric coordinates |

## Observer boundary and calibrated retained memory

`universe24.observer` reads a standalone compressed click file. It exposes
`read_clicks`, `inspect_click_file`, `compare_click_files` and
`reconstruct_memory_from_clicks`. The installed CLI is:

```bash
python -m universe24 observe-clicks --clicks PATH/clicks.jsonl.gz
python -m universe24 observe-clicks --clicks PATH/clicks.jsonl.gz \
  --memory-channel 1 --nodes 125 --steps 8 --out NEW_OBSERVATION.json
```

The second command is the public calibration for the registered root-zero
5-cube detector fixture, not parameters inferred from an unseen seed. It
requires zero initial memory histories, the nonnegative detector sector,
constant carries and a complete eight-update observation window. The output
reports all capture/release changes, including quiet-tick inference. It does
not read incoming fields, arming state, hidden spacetime or proper clocks.

The parser rejects malformed fields, mixed provenance, duplicate or reordered
event keys, invalid calibration and negative inferred memory. It supports
unbounded integer quotients without changing interpreter-global limits.
An intact-looking file by itself cannot prove that valid events were not
deleted; authenticity and completeness remain independent replay concerns.

In the registered detector control, 100 memory arithmetic clicks reconstruct
25 captures and 25 releases. The no-light and unarmed controls each have 400
arithmetic clicks but no captures. Distinct stationary states give identical
empty streams. Different hidden remainders give identical nonempty measured
payloads while their provenance identifiers differ. Thus the full state and
event geometry cannot be inferred uniquely from arbitrary clicks.

## What the coupling audits establish

| Target | Measured result | Disposition |
| --- | --- | --- |
| Six internal face views, reciprocal adjacency, no added state | Core contracts and Engine integration pass | Passed software interface |
| Prepared axis light with phase-dependent delay | Exact move/hold transport on the homogeneous matching-history sector | Passed restricted optical control |
| Retained detection observed only through clicks | Calibrated memory histories match independent full-state validation | Passed restricted observation |
| Stable localized rest object | Tested point pulse moves; its raw vector readout violates source-free divergence constraints | This preparation fails; rest mass/dispersion untested |
| Dark matter | EM-dark contrasts emit clicks; localized contrasts leave positive integers; no stress or clustering account | Blocked |
| Light sources the phase variable | Exact contrast recurrence is independent of optical pair sums | Failed for this tensor |
| One clock-plus-detector tensor | The 912-term candidate passes algebra but leaves both component domains | Failed candidate; common law blocked |
| Einstein geodesics / gravitational waves | Homogeneous axis click histograms agree; no retained proper-time round-trip experiment | GW identification fails; full Einstein response untested |

The phase tensor has 24 independent central-pair components, further separated
into axial lines. A six-face accessor cannot create missing cross-direction
scattering. An independent contrast disturbance crosses a face during an
optical hold, so the prepared average optical displacement is not yet a
universal causal speed measured by a physical clock.

The common-law attempt is explicitly
`T_phase + T_detector - T_light`. It retains 48 channels and degree three,
with strict one-face support and exact 2O covariance. On the detector seed,
the first negative appears at update 3. On the phase seed, it appears at
update 1. The two component invariant preparation sectors are disjoint:
the phase construction needs nonzero contrast in all 24 pairs, while the
installed detector admits only four occupied role rows. Adding successful
controls cannot substitute for a shared invariant sector and one valid law.

The GW reference is passive and independent: weak transverse-traceless strain
predicts opposite changes in x/y round-trip proper times. It is never fed to
the Engine. The current click comparison has no retained emitter/reflector
clock assignment and is not a calibrated measurement of that reference.
Six axis lengths alone also leave spatial shear undetermined. No source-based
Einstein constraint or convergence certificate is inferred from these audits.

## Concrete requirements for the next physical law

1. Derive a joint retained clock/transport/memory map and its invariant seed
   domain before compiling the unchanged Rule3 tensor. Keep all 48 channels,
   remainders and degree/locality/covariance checks; no concatenated banks.
2. Supply reciprocal source terms and justified cross-frame interactions.
   Test their influence by intervening on optical amplitudes and sources,
   not by renaming central contrasts or stored memory as matter.
3. Establish one endpoint-consistent geometric quantity, shear/directional
   response and retained material clocks. Compare actual emission, reflection
   and reception records against independently predicted null/timelike paths.
4. Test nonuniform perturbations, positivity, constraints, bit growth and
   refinement with the same law. Distinguish instability from large but exact
   arithmetic, and preserve every failed preparation.
5. Define a physical mass/stress and detector account before classifying
   ordinary matter or dark matter from observer records. Optical cancellation
   alone supplies neither gravitational mass nor cold clustering behavior.

## Reproduce and inspect

```bash
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/new-node-smoke
python -m validation.click_observer_audit --out runs/new-click-observer
python -m validation.matter_dark_audit --out runs/new-matter-dark
python -m validation.detector_clock_integration --out runs/new-common-law
python -m validation.light_link_resonance --out runs/new-phase-panel
python -m validation.geodesic_link_audit --runs runs/new-phase-panel --out runs/new-geodesics
```

The three new saved-run collectors execute 20 runs and 127 forward updates
(10/64 click controls, 6/40 matter controls and 4/23 composition controls).
The geodesic audit replays two existing 64-update histories; those 128 replayed
updates are not counted again as new evolution. The earlier phase panel has
31 runs and 917 updates. All reports preserve passed/failed/not_tested/blocked.
The final local software suite passes 139 tests (50.453 seconds); the generic
six-update scalar/replay smoke and standalone click-only CLI check pass.

The `evidence/` directory contains exact result JSON, run receipts, source
hashes and the final software verification record. Raw bulk traces remain
local and can be regenerated by these commands; their hashes are inventoried.
The [historical archive](../historical_local_work/README.md) preserves older
local source and evidence against its original base, outside current imports.

Detailed reviews: [optical law](light_review.md), [click observer](observer.md),
[matter/dark controls](matter_dark.md), [geodesic reference](geodesics.md),
[clock/detector composition](detector_integration.md) and
[independent integration review](independent_review.md).
