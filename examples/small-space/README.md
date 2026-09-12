# Small-space physics comparisons

These 24 bounded experiments compare available entity behavior with selected
physical targets. All worlds are 9-cubed or 15-cubed. They use the active generic
engine and explicit configuration, without GIF generation or inserted continuum
force/collision equations. New output rules use copy, swap, add, subtract and
integer vector operations. Physical references are independent acceptance targets.

```sh
python examples/small-space/run.py --output artifacts/small-space-new
```

Use a fresh output directory. Each run uses the existing recorded HTML generator.
`report.html` embeds each original player and separates software accounting from
physical agreement. `summary.json` records inputs, runtime identity, outcomes and
the `recorded_output` directory for each accepted run. Input JSON and raw event
traces are retained alongside the report under the standard retention policy.
No renderer output feeds back into the simulator.

## Observed outcomes on 2026-09-12

Runtime source fingerprint:
`1695a4c8757b6493e5bf58613a6b6cd97e533df81d1f17f58723c9a9354d4fce`.
Base main: `2e753fed1f6922d9d2082d6d43c9e150f237bdd6`. Python 3.14.7.
No runtime source was modified. All 24 selected runs completed with exact
declared accounting and causal neighbor send/arrival times.

| Question | Measured result | Interpretation |
| --- | --- | --- |
| Rest | Electron proxy remains at its initial cell with zero momentum | Restricted rest agreement |
| Momentum magnitude / species | Momentum 1 and 2 both move two cells in four ticks; electron and proton proxies share the supplied rate | Missing derived inertia and mass-dependent motion |
| Photon | Catalog proxy moves two cells in four ticks | Half-rate record, not physical light |
| Ray-speed candidate | Changing only the transport denominator from 2 to 1 gives four cells in four ticks | Correct configured causal speed; no quantum photon dynamics |
| Charged response | Positive, negative and neutral records retain zero momentum in a nonzero electric background | No charge-to-field coupling in those catalog profiles |
| Electric-only pulse | E propagates, B remains zero | No Maxwell mixing/constraint law supplied; this is not a free EM wave |
| Equal masses | Configured head-on momentum swap returns both bodies | Restricted classical permutation |
| Unequal masses with existing guard | Masses 1 and 2 pass through without exchanging momentum | Equal-mass rule does not extend automatically |
| Unequal zero-total candidate | Opposite momenta reverse; positive masses, individual squared momenta and total momentum persist | Special classical idealization; general collision dynamics remain missing |
| Outward pulse | Shell stock 216 at radii 1/2/3 across 6/18/38 occupied nodes | Conservative dilution on Manhattan shells, not a gravitational force law |
| Equal Euclidean distance | Offsets (3,0,0) and (2,2,1), both squared distance 9, receive at ticks 3 and 5 | Microscopic directional anisotropy |
| Source response | Receiver momentum 0,0,36,72; opposite field reaction; opposite polarity gives the opposite response | Local causal exchange works with an explicit candidate rule |
| Source absent | Receiver stays at zero momentum | Response depends on delivered source information |
| Finite reservoir | Carrier stock 3,2,1,0,0; spatial stock 0,1,2,3,3; external injection zero | Closed owned-inventory transfer works |
| Domain size | Translated contact, pulse and source-response recorded trajectories/field stock match before relevant boundary differences | Finite domain independence, not a continuum limit |
| Higgs, strong and computational registers | Declared component stock propagates | Representations only; missing physical evolution remains explicit |

At tick 5 the open 9-cubed pulse has 208 units inside and 8 escaped; the 15-cubed
world still contains 216. This expected boundary difference does not invalidate
the earlier matched local evolution. Equal shell stock does not establish
Euclidean isotropy, an inverse-square force or emergent gravity.

## Tested generic solutions and remaining work

The finite reservoir is a joint carrier/field transaction: while the source owns
stock, transfer one unit to the same spatial field. The shared invariant prevents
creation or loss; at zero the guard stops transfer. This repairs the lack of an
owned debit in the separate `source: true` demonstration, whose emission remains
explicit external injection. The conserved stock has not been identified with
physical energy. It is not the computational clock merely because its initial
register profile came from the computational-field entry.

The unequal-mass candidate replaces the equal-mass guard with a zero-total-momentum
guard and retains the simple swap. It uses synthetic light/heavy labels, masses
1 and 2, supplied rates 1/2 and 1/4, and momentum scale 2. At tick 4, measured
displacements +2 and -1 agree with those declared classical units. Those rates
and units are inputs, not derived inertia. This is not relativistic scattering;
no special repair or continuum collision expression computes its output. A
nonzero-total unequal pair is deliberately outside this candidate.

The source-response candidate demonstrates a causal vector exchange with an
opposite field change; it does not supply Coulomb or gravitational dynamics.
The receiver is held, and no physical energy or supporting constraint model is
claimed. See [source notes](source-notes.md) for its units and ownership.

Remaining research needs explicit elementary local E/B mixing, compatible charge
transport, field/carrier energy ownership, inertial motion, general unequal-mass
scattering and long-wavelength isotropy. Preserving signed component sums alone
does not establish physical electromagnetic energy. Overlapping opposite pulses,
general self-field attribution and delayed transaction races are not covered by
these particular runs. Nothing here establishes confinement, Higgs mass generation,
spinor transformations, quantum photons, annihilation or gravity.

Primary acceptance references: [Tong's electrodynamics, wave and energy sections](https://davidtong.org/pdfs/teaching/electromagnetism/electro3.pdf),
[exact discrete charge continuity](https://arxiv.org/abs/1409.0854), and
[CERN on equal-mass matter/antimatter partners](https://home.cern/science/physics/antimatter/).
Their equations are not used to produce the new candidate updates.

Independent review checked recorded evidence and corrected synthetic labels and
momentum units. Earlier output directories remain historical evidence; the final
summary maps accepted cases to their exact recordings. Only changed cases were
rerun after those corrections. The 24 experiments exercise distinct questions;
they do not repeat identical carrier rules for all 35 particle labels.

The three necessary regression tests in `tests/test_small_space_experiments.py`
cover finite depletion, causal opposite reaction, and the new unequal-mass guard
including its excluded regime and measured unit calibration. The shared affected
check selector explicitly tracks the examples loaded through dynamic file paths.

The affected submission gate passed 90 tests, with two optional recorded-movie
visual checks skipped. Ruff passed four changed Python files. Mypy was not
selected because no production Python module changed. The 24 accepted HTML
recordings contain 145 frames; their inputs, fingerprints, conservation flags
and report-to-run identity were verified. Browser visual inspection was not
performed. Independent physics review passed within the stated scope.

Highlights was read on 2026-09-12 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
Boss, physics, fields and test/simulation Skills were reviewed; existing rules
already require unit checks and separation of hypotheses from verified results,
so no redundant Skill change was needed. The Google document was not edited.
