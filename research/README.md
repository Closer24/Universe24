# Research index

The engine is [`../universe24/`](../universe24/). These tools do not add another
evolution law to the selected engine. Recipes prepare complete initial data; experiment runners invoke
that engine; observers and the Presenter read determined states.

## Current entry points

| Purpose | Start here |
| --- | --- |
| Place compatible components on one board | [Component API](../docs/COMPONENTS.md), `components/` |
| Use local period-five/six clocks, packets and a scoped register | [API and algebra](../docs/LOCAL_BUILDING_BLOCKS.md), [compact replay](component_families/README.md) |
| Prepare clocks and signal-mediated assemblies | [Clock interfaces and limits](../docs/CLOCK_SELECTION.md), `clock_selection/quiet_clock.py`, `staged_blocks/` |
| Compare clock-rate and gravity claims | [Current evidence and limits](../docs/GRAVITY_STATUS.md) |
| Build an autonomous guided source/record/echo | [Finite-guide clock link](clock_link_v1/README.md) |
| Run a JSON experiment and export recordings | [Detailed walkthrough](../docs/COMPONENT_WALKTHROUGH.md), `experiments/run.py` |
| Replay clocks and gears | [Presenter](../docs/PRESENTER.md), `presenter/` |
| Verify mathematics independently | [Independent reference](reference/README.md), `reference/` |
| Restore evidence and run the full tests | [Validation setup](../docs/QUICKSTART.md#full-research-validation) |

A recipe's constructor is not a guarantee of behavior in an arbitrary assembly.
All components must share the fixed tensor, background and compatible initial
assignments. Functional composition requires a new controlled native run.

## Results and protocols

| Research line | Status and evidence |
| --- | --- |
| Component assembly | [API results](../docs/COMPONENT_RESULTS.md) and [review](../docs/COMPONENT_REVIEW.md); prepared signals, finite memory and route controls |
| Local family components | [31-case replay](component_families/README.md); exact prepared clocks, guided scattering, source-overlap single read and failed two-read composition |
| Clock-mediated signals | [Clock research](clock_selection/README.md); verified phase responses alongside failed unique-record and formation targets |
| Effective scalar families | [Invariant families](invariant_families_v1/README.md); exact global encodings under `num=den=1`, 48 native cases and four nonlinear-overlap controls |
| Clock-rate prerequisites | [All-48-channel audit](einstein_clock_bricks_v1/README.md); restricted two-probe `4/5` recurrence-rate coincidence, arithmetic continuity and mean-field limits; no gravity derivation |
| Collective activity and clocks | [Exact identities and independent replay](collective_clock_geometry/README.md); quadratic activity, counterexamples to an activity-only update and scoped verification of the rate result |
| Autonomous clock link | [Finite-guide construction](clock_link_v1/README.md); local launch, endpoint return and cyclic records under unchanged Rule3 |
| Light-approval hypothesis | [Study record](light_approval/README.md); explicit hypotheses and negative controls, not a physical approval mechanism |
| Message mechanism | [Study record](message_mechanism/README.md); preparations, interfaces and limits |
| Algorithm comparisons | [Analogue review](algorithm_analogues/README.md); conceptual comparisons, not imported dynamics |

The [current claim addendum](clock_selection/invariant_families_claims.md)
supplements the [earlier register](clock_selection/claim_register.md); it does
not replace its failures. The [exact-sector limit](clock_selection/invariant_sector_limit.md)
excludes first entry into an exact global invariant family from outside it,
while leaving local and approximate formation open.

The [per-channel rational-coefficient proposal](clock_selection/fixed_ratio_candidate.md)
is an **unselected, unimplemented comparison**, outside the current model.
The [broader coupling families](../docs/COUPLING_FAMILIES.md) likewise distinguish
mathematical options from the eight tensors accepted by the engine.

## Preserved experiments and frozen evidence

`building_blocks/`, `signal_clocks/`, `component_studies/`, `component_review/`,
`light_approval/` and `message_mechanism/` include earlier study producers and
review tools. Several are still imported by later experiments, independent
audits and tests. Age is not evidence that code is unused. They are not
additional installed engines or recommended substitutes for the interfaces
above. Source snapshots under evidence and publication directories reproduce
specific past runs; use their associated protocol and commit.

| Evidence | Storage and access |
| --- | --- |
| Earlier component studies | [`artifacts/Universe24_Components.parts/manifest.json`](artifacts/Universe24_Components.parts/manifest.json); `python -m research.experiments.materialize_evidence` |
| Clock-selection studies | [`clock_selection/artifacts/evidence_v1.parts/manifest.json`](clock_selection/artifacts/evidence_v1.parts/manifest.json); `python -m research.clock_selection.archive materialize` |
| Invariant-family and overlap follow-up | [`invariant_families_v1/`](invariant_families_v1/); directly tracked, verified by `python -m research.invariant_families_v1.verify_evidence` |

Restore archives before reviewing their linked historical recordings. Frozen
protocols, failed outcomes, source identities and full-state evidence remain
unchanged. Do not delete or move them merely to shorten the repository listing;
check import, test, manifest and documentation dependencies first.
